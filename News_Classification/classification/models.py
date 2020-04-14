from abc import abstractmethod

from keras.engine import Input
from keras.layers import Embedding, Conv1D, MaxPooling1D, Flatten, Lambda, LSTM, Dense, \
    concatenate, TimeDistributed, GlobalMaxPooling1D, Dropout, BatchNormalization, SpatialDropout1D, \
    Bidirectional, GRU, ZeroPadding1D, ReLU, Activation, Masking, GlobalAveragePooling1D, Add, MaxPool1D
from keras.models import Model
from layers.callbacks import F1Metrics, SeqF1Metrics, BertF1Metrics, Log
from keras.callbacks import ModelCheckpoint, EarlyStopping, Callback
from keras_bert import load_trained_model_from_checkpoint, Tokenizer
import numpy as np
from callbacks.ensemble import *
from util.evaluate_score import score
from layers.kmaxpooling import KMaxPooling
from layers.folding import Folding
from layers.attention import SelfAttention


class LanguageModel:
    def __init__(self, config):
        self.config = config
        self.model = None
        self.callbacks = []

    @abstractmethod
    def build(self):
        raise NotImplementedError

    def compile(self, **kwargs):
        inputs, outputs = self.build()
        self.model = Model(inputs, outputs, name='model')
        self.model.summary()
        self.model.compile(optimizer=self.config.optimizer,
                           loss='categorical_crossentropy',
                           metrics=['acc'],
                           )

    def init_callbacks(self, input_num, swa=False, input_valid=None, y_valid=None, model_name=None):
        if self.config.seq:
            self.callbacks.append(SeqF1Metrics(self.config.num_classes, input_num=input_num))

        if swa:
            self.add_swa(swa_start=self.config.swa_start)

        # if input_valid is not None and y_valid is not None:
        self.callbacks.append(F1Metrics(input_valid, y_valid))

        self.callbacks.append(
            Log(input_valid, y_valid, model_name, os.path.join(self.config.logs_dir, '%s.txt' % model_name)))

        self.callbacks.append(
            EarlyStopping(
                monitor=self.config.early_stopping_monitor,
                patience=self.config.early_stopping_patience,
                mode=self.config.early_stopping_mode
            )
        )

        self.callbacks.append(
            ModelCheckpoint(
                filepath=os.path.join(self.config.checkpoint_dir, '%s.hdf5' % model_name),
                monitor=self.config.checkpoint_monitor,
                mode=self.config.checkpoint_mode,
                save_best_only=self.config.checkpoint_save_best_only,
                save_weights_only=self.config.checkpoint_save_weights_only,
                verbose=self.config.checkpoint_verbose,
            )
        )

    def fit(self, train_input, train_label, valid_input, valid_output, model_name, swa=False, **kwargs):
        assert self.model is not None, 'Must compile the model before fitting data'
        self.init_callbacks(input_num=2, swa=swa, input_valid=valid_input, y_valid=valid_output, model_name=model_name)
        return self.model.fit(train_input, train_label,
                              validation_data=(valid_input, valid_output),
                              epochs=self.config.num_epochs,
                              verbose=self.config.verbose_training,
                              batch_size=self.config.batch_size,
                              callbacks=self.callbacks,
                              **kwargs)

    def evaluate(self, results, x_label, model_name):
        num = 0.
        correct = 0.
        score(x_label, results, model_name + "_all", os.path.join(self.config.logs_dir, '%s.txt' % model_name))
        results = np.argmax(results, axis=-1)
        x_label = np.argmax(x_label, axis=-1)
        for i in range(len(results)):
            if results[i] == x_label[i]:
                correct += 1
            num += 1
        acc = correct / num
        print('\n- **Evaluation results of %s model**' % self.config.exp_name)
        print('acc:', acc)
        return acc

    def predict(self, x_sent):
        assert self.model is not None and isinstance(self.model, Model)

        results = self.model.predict(x_sent, verbose=1)
        return results

    def save_weights(self, **kwargs):
        assert self.model is not None, 'Must compile the model before saving weights'
        check_point_path = os.path.join(self.config.checkpoint_dir, '%s.hdf5' % self.config.exp_name)
        print('save %s' % check_point_path)
        self.model.save_weights(check_point_path, **kwargs)

    def load_weights(self, **kwargs):
        assert self.model is not None, 'Must compile the model loading weights'
        check_point_path = os.path.join(self.config.checkpoint_dir, '%s.hdf5' % self.config.exp_name)
        self.model.load_weights(check_point_path, **kwargs)

    def add_swa(self, swa_start=5):
        self.callbacks.append(SWA(self.config.checkpoint_dir, self.config.exp_name, swa_start=swa_start))
        print('Logging Info - Callback Added: SWA')

    def load_swa_weight(self):
        print('Logging Info - Loading SWA model checkpoint: %s_swa.hdf5\n' % self.config.exp_name)
        self.model.load_weights(
            os.path.join(self.config.checkpoint_dir, '%s_swa.hdf5' % self.config.exp_name))
        print('Logging Info - SWA Model loaded')


class Bert(LanguageModel):

    def bert_model(self):
        config_path = './corpus/bert_config.json'
        checkpoint_path = './corpus/bert_model.ckpt'
        bert_model = load_trained_model_from_checkpoint(config_path, checkpoint_path)
        for i, l in enumerate(bert_model.layers):
            l.trainable = True
        return bert_model

    def build(self):
        sent_id = Input(shape=(self.config.max_len_bert,), dtype='int32', name='sent_id_base')
        sent_segment = Input(shape=(self.config.max_len_bert,), dtype='int32', name='sent_segment_base')

        sent_bert = self.bert_model()([sent_id, sent_segment])

        sent_bert = Lambda(lambda x: x[:, 0])(sent_bert)
        output = Dense(self.config.num_classes, activation='softmax', name='output')(sent_bert)
        return [sent_id, sent_segment], output


class BiLSTM_Att(LanguageModel):
    def char_embedding(self, weights):
        sent_char = Input(shape=(self.config.max_len_word, self.config.char_per_word), dtype='int32')

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='char_embedding_layer', trainable=True)
        sent_char_embedding = TimeDistributed(embedding_layer)(sent_char)
        conv_layer = Conv1D(filters=100, kernel_size=5, padding='same', activation='relu', strides=1)
        sent_conv = TimeDistributed(conv_layer)(sent_char_embedding)
        max_pooling = GlobalMaxPooling1D()
        sent_mp = TimeDistributed(max_pooling)(sent_conv)
        return Model(sent_char, sent_mp)

    def build(self):
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)

        if self.config.level == 'char':
            weights_char = np.load(os.path.join(self.config.embedding_path, 'char_level', self.config.embedding_file))
            char_emb = self.char_embedding(weights_char)
            sent_char = Input(shape=(self.config.max_len, self.config.char_per_word), dtype='int32',
                              name='sent_char_base')
            sent_char_embedding = char_emb(sent_char)
            sent_embedding = concatenate([sent_embedding, sent_char_embedding])

        LSTM_Left = LSTM(100, return_sequences=True, go_backwards=True)(sent_embedding)
        LSTM_Left = BatchNormalization()(LSTM_Left)
        LSTM_Left = Dropout(0.15)(LSTM_Left)

        LSTM_Right = LSTM(100, return_sequences=True, go_backwards=False)(sent_embedding)
        LSTM_Right = BatchNormalization()(LSTM_Right)
        LSTM_Right = Dropout(0.15)(LSTM_Right)
        CNN_Input = concatenate([LSTM_Left, sent_embedding, LSTM_Right], axis=-1)

        filter_lengths = [2, 3, 4, 5]
        sent_conv_layers = []
        for filter_length in filter_lengths:
            conv_layer = Conv1D(filters=200, kernel_size=filter_length, padding='same',
                                activation='relu', strides=1)
            sent_c = conv_layer(CNN_Input)
            sent_maxpooling = MaxPooling1D(pool_size=self.config.max_len)(sent_c)
            sent_flatten = Flatten()(sent_maxpooling)
            sent_conv_layers.append(sent_flatten)
        representation = concatenate(inputs=sent_conv_layers)
        dropout = Dropout(0.15)(representation)

        # MLP2 - target1
        mlp2_hidden0 = Dense(256, activation='relu')(dropout)
        mlp2_hidden0 = Dropout(0.25)(mlp2_hidden0)
        mlp2_hidden1 = Dense(128, activation='relu')(mlp2_hidden0)
        mlp2_hidden2 = Dense(64, activation='relu')(mlp2_hidden1)
        # mlp2_hidden3 = Dense(32, activation='relu')(mlp2_hidden2)
        output = Dense(self.config.label_size, activation='softmax', name='target')(mlp2_hidden2)
        return input_sent, output


class TextCNN(LanguageModel):

    def build(self):
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)
        text_embed = SpatialDropout1D(0.2)(sent_embedding)

        filter_lengths = [2, 3, 4, 5]
        conv_layers = []
        for filter_length in filter_lengths:
            conv_layer = Conv1D(filters=300, kernel_size=filter_length, padding='valid',
                                strides=1, activation='relu')(text_embed)
            maxpooling = MaxPool1D(pool_size=self.config.max_len_word - filter_length + 1)(conv_layer)
            flatten = Flatten()(maxpooling)
            conv_layers.append(flatten)
        sentence_embed = concatenate(inputs=conv_layers)

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)
        return input_sent, output


class CNN(LanguageModel):

    def char_embedding(self, weights):
        sent_char = Input(shape=(self.config.max_len, self.config.char_per_word), dtype='int32')

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='char_embedding_layer', trainable=True)
        sent_char_embedding = TimeDistributed(embedding_layer)(sent_char)
        conv_layer = Conv1D(filters=100, kernel_size=5, padding='same', activation='relu', strides=1)
        sent_conv = TimeDistributed(conv_layer)(sent_char_embedding)
        max_pooling = GlobalMaxPooling1D()
        sent_mp = TimeDistributed(max_pooling)(sent_conv)
        return Model(sent_char, sent_mp)

    def build(self):
        sent = Input(shape=(self.config.max_len,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(sent)

        if self.config.level == 'char':
            sent_char = Input(shape=(self.config.max_len, self.config.char_per_word), dtype='int32',
                              name='sent_char_base')
            weights_char = np.load(os.path.join(self.config.embedding_path, 'char_level', self.config.embedding_file))
            char_emb = self.char_embedding(weights_char)
            sent_char_embedding = char_emb(sent_char)
            sent_embedding = concatenate([sent_embedding, sent_char_embedding])

        filter_lengths = [2, 3, 4, 5]
        sent_conv_layers = []
        for filter_length in filter_lengths:
            conv_layer = Conv1D(filters=200, kernel_size=filter_length, padding='same',
                                activation='relu', strides=1)
            sent_c = conv_layer(sent_embedding)
            sent_maxpooling = MaxPooling1D(pool_size=self.config.max_len)(sent_c)
            sent_flatten = Flatten()(sent_maxpooling)
            sent_conv_layers.append(sent_flatten)
        representation = concatenate(inputs=sent_conv_layers)

        # MLP2 - target1
        mlp2_hidden0 = Dense(256, activation='relu')(representation)
        mlp2_hidden0 = Dropout(0.25)(mlp2_hidden0)
        mlp2_hidden1 = Dense(128, activation='relu')(mlp2_hidden0)
        mlp2_hidden2 = Dense(64, activation='relu')(mlp2_hidden1)
        # mlp2_hidden3 = Dense(32, activation='relu')(mlp2_hidden2)
        output1 = Dense(self.config.label1_size, activation='softmax', name='target1')(mlp2_hidden2)

        # MLP1 - target1&target2
        # mlp1_hidden0 = Flatten()(representation)
        mlp1_hidden0 = Dense(256, activation='relu')(representation)
        mlp1_hidden0 = Dropout(0.25)(mlp1_hidden0)
        mlp1_hidden1 = Dense(128, activation='relu')(mlp1_hidden0)
        # mlp1_concat = concatenate([mlp2_hidden2, mlp1_hidden1], axis=-1)
        mlp1_hidden2 = Dense(64, activation='relu')(mlp1_hidden1)

        # mlp1_hidden3 = Dense(32, activation='relu')(mlp1_hidden2)
        output12 = Dense(self.config.label2_size, activation='softmax', name='target12')(mlp1_hidden2)
        return sent, [output1, output12]

    def compile(self, **kwargs):
        input_sent, outputs = self.build()
        self.model = Model(input_sent, outputs, name='model')
        self.model.summary()
        self.model.compile(optimizer=self.config.optimizer,
                           loss={'target12': 'categorical_crossentropy',
                                 'target1': 'categorical_crossentropy'},
                           loss_weights={'target12': 1., 'target1': 1.},
                           metrics={'target12': ['acc'], 'target1': ['acc']}
                           )


class DPCNN(LanguageModel):

    def build(self):
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)
        text_embed = SpatialDropout1D(0.2)(sent_embedding)

        repeat = 3
        size = self.config.max_len_word
        region_x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(text_embed)
        x = Activation(activation='relu')(region_x)
        x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(x)
        x = Activation(activation='relu')(x)
        x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(x)
        x = Add()([x, region_x])

        for _ in range(repeat):
            px = MaxPooling1D(pool_size=3, strides=2, padding='same')(x)
            size = int((size + 1) / 2)
            x = Activation(activation='relu')(px)
            x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(x)
            x = Activation(activation='relu')(x)
            x = Conv1D(filters=250, kernel_size=3, padding='same', strides=1)(x)
            x = Add()([x, px])

        x = MaxPooling1D(pool_size=size)(x)
        sentence_embed = Flatten()(x)

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_sent, output


class DCNN(LanguageModel):

    def build(self):
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)
        text_embed = SpatialDropout1D(0.2)(sent_embedding)

        # wide convolution
        zero_padded_1 = ZeroPadding1D((6, 6))(text_embed)
        conv_1 = Conv1D(filters=128, kernel_size=7, strides=1, padding='valid')(zero_padded_1)
        # dynamic k-max pooling
        k_maxpool_1 = KMaxPooling(int(self.config.max_len_word / 3 * 2))(conv_1)
        # non-linear feature function
        non_linear_1 = ReLU()(k_maxpool_1)

        # wide convolution
        zero_padded_2 = ZeroPadding1D((4, 4))(non_linear_1)
        conv_2 = Conv1D(filters=128, kernel_size=5, strides=1, padding='valid')(zero_padded_2)
        # dynamic k-max pooling
        k_maxpool_2 = KMaxPooling(int(self.config.max_len_word / 3 * 1))(conv_2)
        # non-linear feature function
        non_linear_2 = ReLU()(k_maxpool_2)

        # wide convolution
        zero_padded_3 = ZeroPadding1D((2, 2))(non_linear_2)
        conv_3 = Conv1D(filters=128, kernel_size=5, strides=1, padding='valid')(zero_padded_3)
        # folding
        folded = Folding()(conv_3)
        # dynamic k-max pooling
        k_maxpool_3 = KMaxPooling(k=10)(folded)
        # non-linear feature function
        non_linear_3 = ReLU()(k_maxpool_3)

        sentence_embed = Flatten()(non_linear_3)

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_sent, output


class BiLSTM(LanguageModel):

    def build(self):
        input_text = Input(shape=(self.config.max_len_word,))

        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)(input_text)
        text_embed = SpatialDropout1D(0.2)(embedding_layer)

        hidden_states = Bidirectional(LSTM(units=self.config.rnn_units, return_sequences=True))(text_embed)
        global_max_pooling = Lambda(lambda x: K.max(x, axis=1))  # GlobalMaxPooling1D didn't support masking
        sentence_embed = global_max_pooling(hidden_states)

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_text, output


class CNNRNN(LanguageModel):

    def build(self):
        input_text = Input(shape=(self.config.max_len_word,))

        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)(input_text)
        text_embed = SpatialDropout1D(0.2)(embedding_layer)

        conv_layer = Conv1D(300, kernel_size=3, padding="valid", activation='relu')(text_embed)
        conv_max_pool = MaxPooling1D(pool_size=2)(conv_layer)

        gru_layer = Bidirectional(GRU(self.config.rnn_units, return_sequences=True))(conv_max_pool)
        sentence_embed = GlobalMaxPooling1D()(gru_layer)

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        if self.config.loss_function == 'binary_crossentropy':
            output = Dense(1, activation='sigmoid')(dense_layer)
        else:
            output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_text, output


class HAN(LanguageModel):

    def build(self):
        input_text = Input(shape=(self.config.han_max_sent, self.config.han_max_sent))

        sent_encoded = TimeDistributed(self.word_encoder())(input_text)  # word encoder
        sent_vectors = TimeDistributed(SelfAttention(bias=True))(sent_encoded)  # word attention

        doc_encoded = self.sentence_encoder()(sent_vectors)  # sentence encoder
        doc_vector = SelfAttention(bias=True)(doc_encoded)  # sentence attention

        dense_layer = Dense(256, activation='relu')(doc_vector)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_text, output

    def word_encoder(self):
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)
        text_embed = SpatialDropout1D(0.2)(sent_embedding)
        sent_encoded = Bidirectional(GRU(self.config.rnn_units, return_sequences=True))(text_embed)
        return Model(input_sent, sent_encoded)

    def sentence_encoder(self):
        input_sents = Input(shape=(self.config.han_max_sent, self.config.rnn_units * 2))
        sents_masked = Masking()(input_sents)  # support masking
        doc_encoded = Bidirectional(GRU(self.config.rnn_units, return_sequences=True))(sents_masked)
        return Model(input_sents, doc_encoded)


class MultiCNN(LanguageModel):

    def build(self):
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)
        text_embed = SpatialDropout1D(0.2)(sent_embedding)

        filter_lengths = [2, 3, 4, 5]
        conv_layers = []
        for filter_length in filter_lengths:
            conv_layer_1 = Conv1D(filters=300, kernel_size=filter_length, strides=1,
                                  padding='valid', activation='relu')(text_embed)
            bn_layer_1 = BatchNormalization()(conv_layer_1)
            conv_layer_2 = Conv1D(filters=300, kernel_size=filter_length, strides=1,
                                  padding='valid', activation='relu')(bn_layer_1)
            bn_layer_2 = BatchNormalization()(conv_layer_2)
            maxpooling = MaxPooling1D(pool_size=self.config.max_len_word - 2 * filter_length + 2)(bn_layer_2)
            flatten = Flatten()(maxpooling)
            conv_layers.append(flatten)
        sentence_embed = concatenate(inputs=conv_layers)

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_sent, output


class RCNN(LanguageModel):
    def build(self):
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)
        text_embed = SpatialDropout1D(0.2)(sent_embedding)

        # We shift the document to the right to obtain the left-side contexts
        l_embedding = Lambda(lambda x: K.concatenate([K.zeros(shape=(K.shape(x)[0], 1, K.shape(x)[-1])),
                                                      x[:, :-1]], axis=1))(text_embed)
        # We shift the document to the left to obtain the right-side contexts
        r_embedding = Lambda(lambda x: K.concatenate([K.zeros(shape=(K.shape(x)[0], 1, K.shape(x)[-1])),
                                                      x[:, 1:]], axis=1))(text_embed)
        # use LSTM RNNs instead of vanilla RNNs as described in the paper.
        forward = LSTM(self.config.rnn_units, return_sequences=True)(l_embedding)  # See equation (1)
        backward = LSTM(self.config.rnn_units, return_sequences=True, go_backwards=True)(
            r_embedding)  # See equation (2)
        # Keras returns the output sequences in reverse order.
        backward = Lambda(lambda x: K.reverse(x, axes=1))(backward)
        together = concatenate([forward, text_embed, backward], axis=2)  # See equation (3).

        # use conv1D instead of TimeDistributed and Dense
        semantic = Conv1D(self.config.rnn_units, kernel_size=1, activation="tanh")(together)  # See equation (4).
        sentence_embed = Lambda(lambda x: K.max(x, axis=1))(semantic)  # See equation (5).

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_sent, output


class RNNCNN(LanguageModel):

    def build(self):
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)
        text_embed = SpatialDropout1D(0.2)(sent_embedding)
        gru_layer = Bidirectional(GRU(self.config.rnn_units, return_sequences=True))(text_embed)

        conv_layer = Conv1D(64, kernel_size=2, padding="valid", kernel_initializer="he_uniform")(gru_layer)

        avg_pool = GlobalAveragePooling1D()(conv_layer)
        max_pool = GlobalMaxPooling1D()(conv_layer)
        sentence_embed = concatenate([avg_pool, max_pool])

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_sent, output


class VDCNN(LanguageModel):

    def build(self):
        depth = [4, 4, 10, 10]
        pooling_type = 'maxpool'
        use_shortcut = False
        input_sent = Input(shape=(self.config.max_len_word,), dtype='int32', name='sent_base')
        weights = np.load(
            os.path.join(self.config.embedding_path, self.config.level + '_level', self.config.embedding_file))

        embedding_layer = Embedding(input_dim=weights.shape[0],
                                    output_dim=weights.shape[-1],
                                    weights=[weights], name='embedding_layer', trainable=True)
        sent_embedding = embedding_layer(input_sent)
        text_embed = SpatialDropout1D(0.2)(sent_embedding)

        # first temporal conv layer
        conv_out = Conv1D(filters=64, kernel_size=3, kernel_initializer='he_uniform', padding='same')(text_embed)
        shortcut = conv_out

        # temporal conv block: 64
        for i in range(depth[0]):
            if i < depth[0] - 1:
                shortcut = conv_out
                conv_out = self.conv_block(inputs=conv_out, filters=64, use_shortcut=use_shortcut, shortcut=shortcut)
            else:
                # shortcut is not used at the last conv block
                conv_out = self.conv_block(inputs=conv_out, filters=64, use_shortcut=use_shortcut, shortcut=None)

        # down-sampling
        # shortcut is the second last conv block output
        conv_out = self.dowm_sampling(inputs=conv_out, pooling_type=pooling_type, use_shortcut=use_shortcut,
                                      shortcut=shortcut)
        shortcut = conv_out

        # temporal conv block: 128
        for i in range(depth[1]):
            if i < depth[1] - 1:
                shortcut = conv_out
                conv_out = self.conv_block(inputs=conv_out, filters=128, use_shortcut=use_shortcut, shortcut=shortcut)
            else:
                # shortcut is not used at the last conv block
                conv_out = self.conv_block(inputs=conv_out, filters=128, use_shortcut=use_shortcut, shortcut=None)

        # down-sampling
        conv_out = self.dowm_sampling(inputs=conv_out, pooling_type=pooling_type, use_shortcut=use_shortcut,
                                      shortcut=shortcut)
        shortcut = conv_out

        # temporal conv block: 256
        for i in range(depth[2]):
            if i < depth[1] - 1:
                shortcut = conv_out
                conv_out = self.conv_block(inputs=conv_out, filters=256, use_shortcut=use_shortcut, shortcut=shortcut)
            else:
                # shortcut is not used at the last conv block
                conv_out = self.conv_block(inputs=conv_out, filters=256, use_shortcut=use_shortcut, shortcut=None)

        # down-sampling
        conv_out = self.dowm_sampling(inputs=conv_out, pooling_type=pooling_type, use_shortcut=use_shortcut,
                                      shortcut=shortcut)

        # temporal conv block: 512
        for i in range(depth[3]):
            if i < depth[1] - 1:
                shortcut = conv_out
                conv_out = self.conv_block(inputs=conv_out, filters=128, use_shortcut=use_shortcut, shortcut=shortcut)
            else:
                # shortcut is not used at the last conv block
                conv_out = self.conv_block(inputs=conv_out, filters=128, use_shortcut=use_shortcut, shortcut=None)

        # 8-max pooling
        conv_out = KMaxPooling(k=8)(conv_out)
        flatten = Flatten()(conv_out)

        fc1 = Dense(2048, activation='relu')(flatten)
        sentence_embed = Dense(2048, activation='relu')(fc1)

        dense_layer = Dense(256, activation='relu')(sentence_embed)
        output = Dense(self.config.num_classes, activation='softmax')(dense_layer)

        return input_sent, output

    def conv_block(self, inputs, filters, use_shortcut, shortcut):
        conv_1 = Conv1D(filters=filters, kernel_size=3, kernel_initializer='he_uniform', padding='same')(inputs)
        bn_1 = BatchNormalization()(conv_1)
        relu_1 = ReLU()(bn_1)
        conv_2 = Conv1D(filters=filters, kernel_size=3, kernel_initializer='he_uniform', padding='same')(relu_1)
        bn_2 = BatchNormalization()(conv_2)
        relu_2 = ReLU()(bn_2)

        if shortcut is not None and use_shortcut:
            return Add()([inputs, shortcut])
        else:
            return relu_2

    def dowm_sampling(self, inputs, pooling_type, use_shortcut, shortcut):
        if pooling_type == 'kmaxpool':
            k = math.ceil(K.int_shape(inputs)[1] / 2)
            pool = KMaxPooling(k)(inputs)
        elif pooling_type == 'maxpool':
            pool = MaxPooling1D(pool_size=3, strides=2, padding='same')(inputs)
        elif pooling_type == 'conv':
            pool = Conv1D(filters=K.int_shape(inputs)[-1], kernel_size=3, strides=2,
                          kernel_initializer='he_uniform', padding='same')(inputs)
        else:
            raise ValueError('pooling_type `{}` not understood'.format(pooling_type))
        if shortcut is not None and use_shortcut:
            shortcut = Conv1D(filters=K.int_shape(inputs)[-1], kernel_size=3, strides=2,
                              kernel_initializer='he_uniform', padding='same')(shortcut)
            return Add()([pool, shortcut])
        else:
            return pool
