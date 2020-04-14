import codecs
import json
from collections import defaultdict


def generate_test_data():
    fr = open('../data/test_data_raw.txt', 'r')
    fw = open('../data/test_data.txt', 'w')
    for line in fr:
        fw.write(line.split('	')[1])
    fr.close()
    fw.close()


def statistics_tags(train_file, test_file):
    tags_action = defaultdict(int)
    tags_target = defaultdict(int)
    with codecs.open(train_file, encoding='utf-8') as f_train:
        for line in f_train:
            x = json.loads(line)
            try:
                action = x['intents'][0]['action']['value'].strip()
                target = x['intents'][0]['target']['value'].strip()
                tags_action[action] += 1
                tags_target[target] += 1
            except (IndexError, KeyError):
                continue

    with codecs.open(test_file, encoding='utf-8') as f_train:
        for line in f_train:
            x = json.loads(line)
            try:
                action = x['intents'][0]['action']['value'].strip()
                target = x['intents'][0]['target']['value'].strip()
                tags_action[action] += 1
                tags_target[target] += 1
            except (IndexError, KeyError):
                continue

    for key, value in tags_action.items():
        print(key, value)
    print('-----------')
    for key, value in tags_target.items():
        print(key, value)
    return


if __name__ == '__main__':
    statistics_tags('../data/train_data.txt', '../data/test_data.txt')
