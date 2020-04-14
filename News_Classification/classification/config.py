# -*- coding: utf-8 -*-


# 配置文件
class Config(object):
    def __init__(self):
        self.level = "word"
        self.checkpoint_dir = 'models'
        self.logs_dir = 'logs'
        self.exp_name = None
        self.embedding_path = None
        self.embedding_path_word = None
        self.embedding_path_char = None
        self.max_len = 10
        self.vocab_len = None
        self.num_epochs = 60
        self.num_classes = 15
        self.seq = False
        self.swa_start = 10
        self.loss_function = 'multi_crossentropy'
        # bert learning rate is low
        self.learning_rate = 0.00001
        self.optimizer = "adam"
        self.batch_size = 50
        self.verbose_training = 1
        self.checkpoint_monitor = "val_f1"
        self.checkpoint_mode = "max"
        self.checkpoint_save_best_only = True
        self.checkpoint_save_weights_only = True
        self.checkpoint_verbose = 1
        self.early_stopping_monitor = 'val_acc'
        self.early_stopping_patience = 5
        self.early_stopping_mode = 'max'
        self.max_len_word = 10
        self.max_len_char = 20
        self.label1_size = 13
        self.label2_size = 40
        self.label_size = 14
        self.vocab_len_word = 22512
        self.vocab_len_char = 3541
        self.char_per_word = 5
        self.embedding_path = "data"
        self.embedding_file = 'intent_100_dim.'
        self.embedding_dim = 100
        self.margin = 0.15
        self.dropout = 0.2
