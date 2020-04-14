# coding:utf-8
import os
import re
import time
import codecs
from sklearn.metrics import *
import keras.backend as K
from sklearn.preprocessing import LabelBinarizer


def calculate(result_file):
    fr = open(result_file, 'r')
    acc_count = 0
    all_count = 0
    for line in fr:
        line_data = line.split('\t')
        label = line_data[1]
        true_label = line_data[2]
        if label == true_label:
            acc_count += 1
        all_count += 1
    acc_rate = acc_count / all_count
    return acc_rate


# 统计模型的预测结果
# 输入是类比数组
def score(valid_y_true, valid_y_pred, model_solution, score_path):
    precision = precision_score(valid_y_true, valid_y_pred, average='weighted')
    recall = recall_score(valid_y_true, valid_y_pred, average='weighted')
    f1 = f1_score(valid_y_true, valid_y_pred, average='weighted')
    accuracy = accuracy_score(valid_y_true, valid_y_pred)
    auc = multiclass_roc_auc_score(valid_y_true, valid_y_pred, average='weighted')
    fw = codecs.open(score_path, 'a', encoding='utf-8')
    md_path = './result/score.md'
    fw2 = codecs.open(md_path, 'a', encoding='utf-8')
    print('- ** Evaluation results of ' + model_solution + ' model ** -')
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', f1)
    print('Accuracy:', accuracy)
    print('Auc:', auc)
    fw.write("\n- ** Evaluation results of %s model ** -\n" % model_solution)
    fw.write("Precision: %f \n" % precision)
    fw.write("Recall: %f\n" % recall)
    fw.write("F1: %f\n" % f1)
    fw.write("Accuracy: %f\n" % accuracy)
    fw.write("Auc: %f \n" % auc)
    fw.write("|%s|%f|%f|%f|%f|%f|\n" % (model_solution, precision, recall, f1, accuracy, auc))
    fw2.write("|%s|%f|%f|%f|%f|%f|\n" % (model_solution, precision, recall, f1, accuracy, auc))
    fw.close()
    fw2.close()
    return precision, recall, f1, accuracy, auc


# calculate the error ratio of model
def cal_err_ratio(file_name, label, y_test):
    err_count = 0
    sum_count = 0
    t = str(int(time.time()))
    fw = codecs.open("./result/" + file_name+ "_result_" + t[0:6] +".txt", 'a', encoding='utf-8')
    for i in label:
        if i != y_test[sum_count]:
            err_count += 1
        sum_count += 1
    err_ratio = float(err_count) / float(sum_count)
    print("the error ratio: "+str(err_ratio))
    fw.write("pred_result:"+str(label)+'\n')
    fw.write("true_result:"+str(y_test)+'\n')
    fw.write("err_ratio:"+str(err_ratio)+'\n')
    fw.close()


def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def f1(y_true, y_pred):
    precision_re = precision(y_true, y_pred)
    recall_re = recall(y_true, y_pred)
    return 2 * ((precision_re * recall_re) / (precision_re + recall_re))


def multiclass_roc_auc_score(truth, pred, average="macro"):
    lb = LabelBinarizer()
    lb.fit(truth)

    truth = lb.transform(truth)
    pred = lb.transform(pred)
    return roc_auc_score(truth, pred, average=average)


if __name__ == '__main__':

    file_dir = '../result'
    file_list = os.listdir(file_dir)

    for file in file_list:
        tt_match = re.search(r'classify_result_(.*)_mlp_(\d*)_task.txt', file)
        if tt_match:
            print(file)
            acc_rate = calculate('../result/' + file)
            print(acc_rate)
