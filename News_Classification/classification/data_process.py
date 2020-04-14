# -*- coding: utf-8 -*-
import codecs
import json
import logging
import os
import pickle

import jieba
import numpy as np
# from fasttext import load_model, train_unsupervised
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence


# 文本数据向量化
def generate_embedding(level):
    data_path = 'data/%s_level' % level

    embedding_size = 100
    # configure logging
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)

    # prepare corpus
    sentences = LineSentence(os.path.join(data_path, 'corpus_all.txt'))
    vocabulary = pickle.load(open(os.path.join(data_path, 'vocabulary_all.pkl'), 'rb'))

    # run model
    model = Word2Vec(sentences, size=embedding_size, min_count=1, window=5, sg=1, iter=10)
    # model.wv.save_word2vec_format('data/word_level/word2vec.txt', binary=False)
    weights = model.wv.syn0
    d = dict([(k, v.index) for k, v in model.wv.vocab.items()])
    emb = np.zeros(shape=(len(vocabulary) + 2, embedding_size), dtype='float32')

    for w, i in vocabulary.items():
        if w not in d:
            continue
        # print(d)
        emb[i, :] = weights[d[w], :]

    np.save(open(os.path.join(data_path, 'intent_100_dim.embeddings'), 'wb'), emb)


# def generate_fasttext_embedding(level):
#     data_path = 'data/%s_level' % level
#
#     model = train_unsupervised(input=os.path.join(data_path, 'corpus_all.txt'),
#                                model='skipgram', epoch=10, minCount=1, wordNgrams=3, dim=300)
#
#     vocab = pickle.load(open(os.path.join(data_path, 'vocabulary_all.pkl'), 'rb'))
#     d = dict([(w, 0) for w in model.get_words()])
#     print(len(d))
#     emb = np.zeros(shape=(len(vocab) + 2, 300), dtype='float32')
#     print(len(vocab))
#     for w, i in vocab.items():
#         if w not in d:
#             continue
#         emb[i, :] = model.get_word_vector(w)
#     np.save(open(os.path.join(data_path, 'toutiao_300_dim.fasttext'), 'wb'), emb)


def build_word_level_corpus_all(train_file, valid_file=None, test_file=None):
    sentences = list()

    with codecs.open(train_file, "r", encoding="utf8") as f_train:
        for line in f_train:
            x = json.loads(line)
            sentences.extend([x['title'].strip()])

    if valid_file:
        with codecs.open(valid_file, encoding='utf-8') as f_valid:
            for line in f_valid:
                x = json.loads(line)
                sentences.extend([x['title'].strip()])

    if test_file:
        with codecs.open(test_file, encoding='utf-8') as f_test:
            for line in f_test:
                x = json.loads(line)
                sentences.extend([x['title'].strip()])

    target_lines = [' '.join(jieba.cut(sentence)) + '\n' for sentence in sentences]

    with codecs.open('data/word_level/corpus_all.txt', 'w', encoding='utf-8') as f_corpus:
        f_corpus.writelines(target_lines)


def build_char_level_corpus_all(train_file, valid_file=None, test_file=None):
    sentences = list()

    with codecs.open(train_file, encoding='utf-8') as f_train:
        for line in f_train:
            x = json.loads(line)
            sentences.extend([x['title'].strip()])

    if valid_file:
        with codecs.open(valid_file, encoding='utf-8') as f_valid:
            for line in f_valid:
                x = json.loads(line)
                sentences.extend([x['title'].strip()])

    if test_file:
        with codecs.open(test_file, encoding='utf-8') as f_test:
            for line in f_test:
                x = json.loads(line)
                sentences.extend([x['title'].strip()])

    target_lines = list()
    for sentence in sentences:
        target_lines.append(' '.join([char for char in sentence]) + '\n')

    with codecs.open('data/char_level/corpus_all.txt', 'w', encoding='utf-8') as f_corpus:
        f_corpus.writelines(target_lines)


def build_word_level_vocabulary_all(train_file, valid_file=None, test_file=None):
    sentences = list()

    with codecs.open(train_file, encoding='utf-8') as f_train:
        for line in f_train:
            x = json.loads(line)
            sentences.extend([x['title'].strip()])
    if valid_file:
        with codecs.open(valid_file, encoding='utf-8') as f_valid:
            for line in f_valid:
                x = json.loads(line)
                sentences.extend([x['title'].strip()])
    if test_file:
        with codecs.open(test_file, encoding='utf-8') as f_test:
            for line in f_test:
                x = json.loads(line)
                sentences.extend([x['title'].strip()])
    corpus = u''.join(sentences)
    word_list = list(set([tk[0] for tk in jieba.tokenize(corpus)]))
    return dict((word, idx+1) for idx, word in enumerate(word_list))


def build_char_level_vocabulary_all(train_file, valid_file=None, test_file=None):
    sentences = list()

    with codecs.open(train_file, encoding='utf-8') as f_train:
        for line in f_train:
            x = json.loads(line)
            sentences.extend([x['title'].strip()])
    if valid_file:
        with codecs.open(valid_file, encoding='utf-8') as f_valid:
            for line in f_valid:
                x = json.loads(line)
                sentences.extend([x['title'].strip()])
    if test_file:
        with codecs.open(test_file, encoding='utf-8') as f_test:
            for line in f_test:
                x = json.loads(line)
                sentences.extend([x['title'].strip()])

    corpus = u''.join(sentences)
    char_list = list(set([char for char in corpus]))

    return dict((char, idx+1) for idx, char in enumerate(char_list))


# 生成单任务标签
def generate_label(train_file, valid_file=None, test_file=None):
    tags = set()
    with codecs.open(train_file, encoding='utf-8') as f_train:
        for line in f_train:
            x = json.loads(line)
            try:
                label = x['label'].strip()
                tags.add(label)
            except (IndexError, KeyError):
                continue
    if valid_file:
        with codecs.open(valid_file, encoding='utf-8') as f_valid:
            for line in f_valid:
                x = json.loads(line)
                try:
                    label = x['label'].strip()
                    tags.add(label)
                except (IndexError, KeyError):
                    continue
    if test_file:
        with codecs.open(test_file, encoding='utf-8') as f_test:
            for line in f_test:
                x = json.loads(line)
                try:
                    label = x['label'].strip()
                    tags.add(label)
                except IndexError:
                    continue

    char_list = list(tags)
    with codecs.open(os.path.join('data', 'tags.txt'), mode='w', encoding='utf-8') as fw:
        for item in char_list:
            fw.write(item+'\n')

    return


if __name__ == '__main__':

    generate_label('data/train_data.txt', valid_file='data/test_data.txt')
    vocab = build_word_level_vocabulary_all('data/train_data.txt')
    with open('data/word_level/vocabulary_all.pkl', 'wb') as vocabulary_pkl:
        pickle.dump(vocab, vocabulary_pkl, -1)
        print(len(vocab))
    build_word_level_corpus_all('data/train_data.txt')
    generate_embedding('word')
    # generate_fasttext_embedding('word')

    vocab = build_char_level_vocabulary_all('data/train_data.txt')
    with open('data/char_level/vocabulary_all.pkl', 'wb') as vocabulary_pkl:
        pickle.dump(vocab, vocabulary_pkl, -1)
        print(len(vocab))
    build_char_level_corpus_all('data/train_data.txt')
    generate_embedding('char')
    # generate_fasttext_embedding('char')

    with open('data/bert_level/vocabulary_all.pkl', 'wb') as vocabulary_pkl:
        pickle.dump(vocab, vocabulary_pkl, -1)
        print(len(vocab))