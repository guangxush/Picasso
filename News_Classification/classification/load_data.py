# -*- coding: utf-8 -*-
import codecs
import json
import os
import pickle

import jieba
import numpy as np
from keras_bert import Tokenizer
from config import Config
from util.utils import pad


# 数据转换
def load_tags(tag_file):
    tags2id = {}
    id2tags = {}
    with codecs.open(os.path.join('data', tag_file), encoding='utf-8') as f:
        for line in f:
            tags2id[line.strip()] = len(tags2id)
            id2tags[len(id2tags)] = line.strip()
    return tags2id, id2tags


def load_data(raw_file):
    # 统计字符串长度
    tags2id, id2tags = load_tags('tags.txt')
    with open('data/word_level/vocabulary_all.pkl', 'rb') as f_vocabulary:
        vocabulary = pickle.load(f_vocabulary)
    print('vocab_len_word:', len(vocabulary))
    with open('data/char_level/vocabulary_all.pkl', 'rb') as f_vocabulary:
        vocabulary_char = pickle.load(f_vocabulary)
    print('vocab_len_char:', len(vocabulary_char))
    x_sent = list()
    x_label = list()
    x_sent_char = list()
    max_len = 0.
    max_char_len = 0.
    avg_len = 0.
    avg_char_len = 0.
    with codecs.open(raw_file, encoding='utf-8') as f:
        for line in f:
            x = json.loads(line)
            input_sent = x['title']

            words_sent = jieba.lcut(input_sent)
            x_sent.append([vocabulary.get(word, len(vocabulary) + 1) for word in words_sent])
            try:
                labels = x['intents'][0]['action']['value'].strip()
                y = [0] * len(tags2id)
                y[tags2id[labels]] = 1
                x_label.append(y)
            except (IndexError, KeyError):
                y = [0] * len(tags2id)
                y[0] = 1
                x_label.append(y)
            if len(words_sent) > max_len:
                max_len = len(words_sent)
            avg_len += len(words_sent)
            l = 0.
            for word in words_sent:
                if len(word) > max_char_len:
                    max_char_len = len(word)
                l += len(word)
            avg_char_len += l / len(words_sent)
            x_sent_char.append(
                [[vocabulary_char.get(char, len(vocabulary_char) + 1) for char in word] for word in words_sent])
    print('max_len:', max_len, 'max_char_len:', max_char_len)
    print('avg_len:', avg_len / len(x_sent_char), 'avg_char_len:', avg_char_len / len(x_sent_char))
    x_label = np.asarray(x_label)
    return x_sent, x_sent_char, x_label, vocabulary


def load_label(x, tags2id):
    y = [0] * len(tags2id)
    try:
        label = x['label'].strip()
        y[tags2id[label]] = 1
    except (IndexError, KeyError):
        y[0] = 1  # 视情况而定
    return y


def load_word_data(raw_file, train=True):
    config = Config()
    tags2id, id2tags = load_tags('tags.txt')
    with open('data/word_level/vocabulary_all.pkl', 'rb') as f_vocabulary:
        vocabulary = pickle.load(f_vocabulary)
    print('vocab_len_word:', len(vocabulary))
    x_sent = list()
    x_label = list()
    with codecs.open(raw_file, encoding='utf-8') as f:
        for line in f:
            x = json.loads(line)
            input_sent = x['title']
            words_sent = jieba.cut(input_sent)
            x_sent.append([vocabulary.get(word, len(vocabulary) + 1) for word in words_sent])
            if train:
                y = load_label(x, tags2id)
                x_label.append(y)
    x_label = np.asarray(x_label)
    x_sent = pad(x_sent, 'word', config.max_len_word)
    return x_sent, x_label, id2tags, vocabulary


def load_char_data(raw_file, train=True):
    config = Config()
    tags2id, id2tags = load_tags('tags.txt')
    with open('data/word_level/vocabulary_all.pkl', 'rb') as f_vocabulary:
        vocabulary = pickle.load(f_vocabulary)
    print('vocab_len_word:', len(vocabulary))
    with open('data/char_level/vocabulary_all.pkl', 'rb') as f_vocabulary:
        vocabulary_char = pickle.load(f_vocabulary)
    print('vocab_len_char:', len(vocabulary_char))
    x_sent = list()
    x_label = list()
    x_sent_char = list()
    with codecs.open(raw_file, encoding='utf-8') as f:
        for line in f:
            x = json.loads(line)
            input_sent = x['title']
            words_sent = jieba.lcut(input_sent)
            x_sent.append([vocabulary.get(word, len(vocabulary) + 1) for word in words_sent])
            x_sent_char.append(
                [[vocabulary_char.get(char, len(vocabulary_char) + 1) for char in word] for word in words_sent])
            if train:
                y = load_label(x, tags2id)
                x_label.append(y)
    x_label = np.asarray(x_label)
    x_sent = pad(x_sent, 'word', config.max_len_word)
    x_sent_char = pad(x_sent_char, 'char', config.max_len_word, config.char_per_word)
    return x_sent, x_sent_char, x_label, id2tags, vocabulary


def load_bert_data(raw_file, train=True):
    config = Config()
    dict_path = './corpus/vocab.txt'
    token_dict = {}
    with codecs.open(dict_path, 'r', 'utf8') as reader:
        for line in reader:
            token = line.strip()
            token_dict[token] = len(token_dict)
    tags2id, id2tags = load_tags('tags.txt')
    x_ids = list()
    x_segments = list()
    x_label = list()
    with codecs.open(raw_file, encoding='utf-8') as f:
        for line in f:
            x = json.loads(line)
            input_sent = x['title']
            tokenizer = Tokenizer(token_dict)
            x_sent_id, x_sent_segment = tokenizer.encode(input_sent, max_len=config.max_len_word)
            x_ids.append(x_sent_id)
            x_segments.append(x_sent_segment)
            if train:
                y = load_label(x, tags2id)
                x_label.append(y)
    x_label = np.asarray(x_label)
    return x_ids, x_segments, x_label, id2tags, None


if __name__ == '__main__':
    load_data('data/train_data.txt')