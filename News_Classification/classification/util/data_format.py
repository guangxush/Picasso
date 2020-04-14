# coding:utf-8
import codecs
import json
import jieba


def generate_json_data(file_input, file_output):
    print("******* " + file_input + " process start *******")
    fr = codecs.open(file_input, 'r', encoding='utf-8')
    fw = codecs.open(file_output, 'w', encoding='utf-8')
    json_dict = {}
    label_data = set()
    for line in fr:
        line_data = line.rstrip('\n')
        try:
            json_dict['label'] = line_data.split('_!_')[1]
            json_dict['sent'] = line_data.split('_!_')[3]
            label_data.add(line_data.split('_!_')[1])
        except IndexError:
            continue
        fj = json.dumps(json_dict, ensure_ascii=False)
        fw.write(fj + '\n')
    fr.close()
    print("the count of data is :" + str(len(open(file_output, 'r').readlines())))
    fw.close()
    fw_set = codecs.open('../data/tags.txt', 'w', encoding='utf-8')
    for label in label_data:
        fw_set.write(label+"\n")
    fw_set.close()
    print("******* " + file_input + " process end *******")


def generate_data(file_input, file_output, corpus_output):
    print("******* " + file_input + " process start *******")
    fr = codecs.open(file_input, 'r', encoding='utf-8')
    fw = codecs.open(file_output, 'w', encoding='utf-8')
    fw_corpus = codecs.open(corpus_output, 'w', encoding='utf-8')
    json_dict = {}
    for line in fr:
        line_data = line.rstrip('\n')
        try:
            json_dict['label'] = line_data.split('_!_')[1]
            document_cut = jieba.cut(line_data.split('_!_')[3])
            result = '@+@'.join(document_cut)
            results = result.split('@+@')
            wordlist = []
            for w in results:
                wordlist.append(w)
            json_dict['title'] = wordlist
        except IndexError:
            continue
        fj = json.dumps(json_dict, ensure_ascii=False)
        fw.write(fj + '\n')
        fw_corpus.write(line_data.split('_!_')[3] + '\n')
    fr.close()
    print("the count of data is :" + str(len(open(file_output, 'r').readlines())))
    fw.close()
    print("******* " + file_input + " process end *******")


def divide_data(input_file, train_file, test_file, real_file):
    print("******* " + input_file + " divide start *******")
    fr = codecs.open(input_file, 'r', encoding='utf-8')
    fw_train = codecs.open(train_file, 'w', encoding='utf-8')
    fw_test = codecs.open(test_file, 'w', encoding='utf-8')
    fw_real = codecs.open(real_file, 'w', encoding='utf-8')
    train_range = 10000
    test_range = 11000
    real_range = 12000
    lines = 0
    for line in fr:
        lines += 1
        line_data = line.rstrip('\n')
        if lines <= train_range:
            fw_train.write(line_data + '\n')
        elif train_range < lines <= test_range:
            fw_test.write(line_data + '\n')
        elif test_range < lines <= real_range:
            fw_real.write(line_data + '\n')
        else:
            break
    print("******* " + input_file + " divide end *******")


if __name__ == '__main__':
    file_input = '../raw_data/toutiao_cat_data.txt'
    file_output = '../data/news_data.txt'
    corpus_output = '../data/corpus.txt'
    generate_data(file_input=file_input, file_output=file_output, corpus_output=corpus_output)
    file_output = '../data/new_json_data.txt'
    generate_json_data(file_input=file_input, file_output=file_output)

    input_file = '../data/new_json_data.txt'
    train_file = '../data/train_data.txt'
    test_file = '../data/valid_data.txt'
    real_file = '../data/real_data.txt'
    divide_data(input_file=input_file, train_file=train_file, test_file=test_file, real_file=real_file)
