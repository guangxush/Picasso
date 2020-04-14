# -*- coding: utf-8 -*-
import codecs

import keras.backend.tensorflow_backend as ktf
import tensorflow as tf
from sklearn.model_selection import train_test_split
from models import *

from config import Config
from load_data import load_word_data, load_char_data, load_bert_data

train = True
level = 'word'
fasttext = False
overwrite = False
swa = False
bert = True
model_name = 'bilstm_att'

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
ktf.set_session(sess)
os.environ['CUDA_VISIBLE_DEVICES'] = '1'


def get_train_data(train_file=None, test_file=None):
    if level == 'word':
        x_sent, x_label, id2tags, vocabulary = load_word_data(train_file)
        x_valid_sent, x_valid_label, _, _ = load_word_data(test_file)
        return [x_sent, x_label], [x_valid_sent, x_valid_label], id2tags
    elif level == 'char':
        x_sent, x_sent_char, x_label, id2tags, vocabulary_char = load_char_data(train_file)
        x_valid_sent, x_valid_sent_char, x_valid_label, _, _ = load_char_data(test_file)
        return [x_sent, x_sent_char, x_label], [x_valid_sent, x_valid_sent_char,
                                                x_valid_label], id2tags
    elif level == 'bert':
        x_sent_ids, x_sent_segments, x_label, id2tags = load_bert_data(train_file)
        x_valid_sent_ids, x_valid_sent_segments, x_valid_label, _ = load_bert_data(test_file)
        return [x_sent_ids, x_sent_segments, x_label], [x_valid_sent_ids, x_valid_sent_segments,
                                                        x_valid_label], id2tags
    else:
        return None


def get_test_data(test_file=None):
    if level == 'word':
        x_test_sent, _, id2tags, vocabulary = load_word_data(test_file, train=False)
        return x_test_sent, id2tags
    elif level == 'char':
        x_test_sent, x_test_sent_char, _, id2tags, vocabulary_char = load_char_data(test_file, train=False)
        return [x_test_sent, x_test_sent_char], id2tags
    elif level == 'bert':
        x_test_ids, x_test_segments, x_label, id2tags = load_bert_data(test_file, train=False)
        return [x_test_ids, x_test_segments], id2tags
    else:
        return None


class Train(object):
    def __init__(self, train_data, test_data, id2tags, model_name='only_bert'):
        self.model_name = model_name
        self.id2tags = id2tags
        self.get_config()
        self.get_model()
        if level == 'word':
            self.x_sent, self.x_label = train_data
            self.x_valid_sent, self.x_valid_label = test_data
        elif level == 'char':
            self.x_sent, self.x_sent_char, self.x_label = train_data
            self.x_valid_sent, self.x_valid_sent_char, self.x_valid_label = test_data
        elif level == 'bert':
            self.x_sent_ids, self.x_sent_segments, self.x_label = train_data
            self.x_valid_sent_ids, self.x_valid_sent_segments, self.x_valid_label = test_data
        else:
            self.x_sent, self.x_sent_char, self.x_label = train_data
            self.x_valid_sent, self.x_valid_sent_char, self.x_valid_label = test_data

    def train(self):
        train_index, valid_index = train_test_split(range(self.x_sent.shape[0]))
        train_input, train_label = self.x_sent[train_index], self.x_label[train_index]
        valid_input, valid_label = self.x_sent[valid_index], self.x_label[valid_index]
        print(train_input.shape)
        print(train_label.shape)
        if overwrite or not os.path.exists(
                os.path.join(self.config.checkpoint_dir, '%s.hdf5' % self.config.exp_name)):
            print('Start training the ' + model_name + ' model...')
            self.model.fit(train_input, train_label, valid_input, valid_label, self.config.exp_name, swa=swa)
        self.model.load_weights()
        results = self.model.predict(self.x_valid_sent)
        self.model.evaluate(results, self.x_valid_label, self.config.exp_name)
        if swa:
            self.model.load_swa_weight()
            print('Start evaluate the %s_swa model...' % self.config.exp_name)
            results_swa = self.model.predict(self.x_valid_sent)
            self.model.evaluate(results_swa, self.x_valid_label)
        if not os.path.exists('result/'):
            os.makedirs('result')
        self.write_results(results)

    def write_results(self, results):
        results = np.asarray(results)
        with codecs.open('result/output.txt', 'w', encoding='utf8') as f:
            for i in range(len(results)):
                result = np.argmax(results[i])
                f.write(str(self.id2tags[result]) + "\n")

    def get_model(self):
        self.name2model()
        self.model = self.M(self.config)
        print('Create the %s model...' % self.config.exp_name)
        self.model.compile()

    def name2model(self):
        m = {'only_bert': Bert,
             'cnn': CNN,
             'bilstm_att': BiLSTM_Att}
        self.M = m[self.model_name]

    def get_config(self):
        self.config = Config()
        self.config.level = level
        self.config.max_len = self.config.max_len_word
        self.config.exp_name = self.model_name + '_' + level
        if not os.path.exists(self.config.checkpoint_dir):
            os.makedirs(self.config.checkpoint_dir)
        if fasttext:
            self.config.embedding_file += 'fasttext'
            self.config.exp_name += '_fasttext'
        else:
            self.config.embedding_file += 'embeddings'


class Test(object):
    def __init__(self, test_data, id2tags, model_name='siamese_cnn'):
        self.model_name = model_name
        self.id2tags = id2tags
        self.get_config()
        self.get_model()
        if level == 'word':
            self.x_sent_test = test_data
        elif level == 'char':
            self.x_test_sent, self.x_test_sent_char = test_data
        elif level == 'bert':
            self.x_test_ids, self.x_test_segments = test_data
        else:
            self.x_sent_test, self.x_sent_char_test = test_data

    def get_model(self):
        self.name2model()
        self.model = self.M(self.config)
        print('Create the %s model...' % self.config.exp_name)
        self.model.compile()

    def name2model(self):
        m = {'only_bert': Bert,
             'cnn': CNN,
             'bilstm_att': BiLSTM_Att}
        self.M = m[self.model_name]

    def get_config(self):
        self.config = Config()
        self.config.level = level
        self.config.max_len = self.config.max_len_word
        self.config.exp_name = self.model_name + '_' + level
        if not os.path.exists(self.config.checkpoint_dir):
            os.makedirs(self.config.checkpoint_dir)
        if fasttext:
            self.config.embedding_file += 'fasttext'
            self.config.exp_name += '_fasttext'
        else:
            self.config.embedding_file += 'embeddings'

    def test(self):
        self.model.load_weights()
        results = self.model.predict(self.x_sent_test)
        if not os.path.exists('result/'):
            os.makedirs('result')
        self.write_results(results)

    def write_results(self, results):
        results = np.asarray(results)
        with codecs.open('result/output.txt', 'w', encoding='utf8') as f:
            for i in range(len(results)):
                result = np.argmax(results[i])
                f.write(str(self.id2tags[result]) + "\n")


def controller(train):
    if train == 'train':
        train_data, valid_data, id2tags = get_train_data('data/train_data.txt', 'data/test_data.txt')
        train = Train(train_data, valid_data, id2tags, model_name=model_name)
        train.train()
    elif train == 'test':
        test_data, id2tags = get_test_data('data/test_data.txt')
        test = Test(test_data, id2tags, model_name=model_name)
        test.test()
    else:
        return


if __name__ == '__main__':
    if train:
        train_data, valid_data, id2tags = get_train_data('data/train_data.txt', 'data/test_data.txt')
        train = Train(train_data, valid_data, id2tags, model_name=model_name)
        train.train()

    else:
        test_data, id2tags = get_test_data('data/test_data.txt')
        test = Test(test_data, id2tags, model_name=model_name)
        test.test()
