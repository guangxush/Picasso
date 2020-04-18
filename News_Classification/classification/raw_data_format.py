# coding:utf-8
import codecs
import json


# 生成json格式的数据
def generate_data(file_input, file_output, corpus_output):
    print("******* " + file_input + " process start *******")
    fr = codecs.open(file_input, 'r', encoding='utf-8')
    fw = codecs.open(file_output, 'w', encoding='utf-8')
    fw_corpus = codecs.open(corpus_output, 'w', encoding='utf-8')
    json_dict = {}
    count = 0
    for line in fr:
        line_data = line.rstrip('\n')
        count += 1
        try:
            json_dict['id'] = count
            json_dict['label'] = line_data.split('_!_')[1]
            json_dict['title'] = line_data.split('_!_')[3]
        except IndexError:
            continue
        fj = json.dumps(json_dict, ensure_ascii=False)
        fw.write(fj + '\n')
        fw_corpus.write(line_data.split('_!_')[3] + '\n')
    fr.close()
    print("the count of data is :" + str(len(open(file_output, 'r').readlines())))
    fw.close()
    print("******* " + file_input + " process end *******")


# 划分数据为训练集和验证集
def divide_data(input_file, train_file, test_file):
    print("******* " + input_file + " divide start *******")
    fr = codecs.open(input_file, 'r', encoding='utf-8')
    fw_train = codecs.open(train_file, 'w', encoding='utf-8')
    fw_test = codecs.open(test_file, 'w', encoding='utf-8')
    train_range = 70
    test_range = 100
    lines = 0
    for line in fr:
        lines += 1
        line_data = line.rstrip('\n')
        if lines <= train_range:
            fw_train.write(line_data + '\n')
        elif train_range < lines <= test_range:
            fw_test.write(line_data + '\n')
        else:
            break
    print("******* " + input_file + " divide end *******")


if __name__ == '__main__':
    file_input = './data/toutiao_cat_data.txt'
    file_output = './data/news_data.txt'
    corpus_output = './data/corpus.txt'
    generate_data(file_input=file_input, file_output=file_output, corpus_output=corpus_output)
    input_file = './data/news_data.txt'
    train_file = './data/train_data.txt'
    test_file = './data/test_data.txt'
    divide_data(input_file=input_file, train_file=train_file, test_file=test_file)
