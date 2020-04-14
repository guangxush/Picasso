# -*- coding: utf-8 -*-
from keras.callbacks import Callback
import numpy as np
from tqdm import tqdm

from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report
from util.evaluate_score import score


class BertF1Metrics(Callback):
    """
    callback for evaluating text classification model
    """

    def __init__(self, x_ids, x_segments, x_labels):
        self.x_ids = x_ids
        self.x_segments = x_segments
        self.valid_labels = x_labels
        super(BertF1Metrics, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        pred_labels = self.model.predict([self.x_ids, self.x_segments])
        pred_labels = np.argmax(pred_labels, axis=1)
        valid_labels = np.argmax(self.valid_labels, axis=1)
        # r = recall_score(self.valid_labels, pred_labels, average='macro')
        # p = precision_score(self.valid_labels, pred_labels, average='macro')
        f1 = f1_score(valid_labels, pred_labels, average='macro')

        # logs['val_r'] = r
        # logs['val_p'] = p
        logs['val_f1'] = f1
        print('Epoch {}: val_f1: {}'.format(epoch + 1, f1))


class F1Metrics_Multi(Callback):
    """
    callback for evaluating text classification model
    """

    def __init__(self, x_sent, x_labels):
        self.x_sent = x_sent
        self.valid_labels = x_labels
        super(F1Metrics_Multi, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        pred_labels = self.model.predict(self.x_sent)
        for i in range(len(pred_labels)):
            self.on_epoch_end_single(pred_labels[i], self.valid_labels[i], epoch, logs)

    def on_epoch_end_single(self, pred_labels, valid_labels, epoch, logs=None):
        pred_labels = np.argmax(pred_labels, axis=1)
        valid_labels = np.argmax(valid_labels, axis=1)
        # r = recall_score(self.valid_labels, pred_labels, average='macro')
        # p = precision_score(self.valid_labels, pred_labels, average='macro')
        f1 = f1_score(valid_labels, pred_labels, average='macro')

        # logs['val_r'] = r
        # logs['val_p'] = p
        logs['val_f1'] = f1
        print('Epoch {}: val_f1: {}'.format(epoch + 1, f1))


class F1Metrics(Callback):
    """
    callback for evaluating text classification model
    """

    def __init__(self, x_sent, x_labels):
        self.x_sent = x_sent
        self.valid_labels = x_labels
        super(F1Metrics, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        pred_labels = self.model.predict(self.x_sent)
        pred_labels = np.argmax(pred_labels, axis=-1)
        valid_labels = np.argmax(self.valid_labels, axis=-1)
        # r = recall_score(self.valid_labels, pred_labels, average='macro')
        # p = precision_score(self.valid_labels, pred_labels, average='macro')
        f1 = f1_score(valid_labels, pred_labels, average='macro')

        # logs['val_r'] = r
        # logs['val_p'] = p
        logs['val_f1'] = f1
        print('Epoch {}: val_f1: {}'.format(epoch + 1, f1))


class Log(Callback):
    """
        callback for evaluating text classification model
    """
    def __init__(self, x_sent, x_labels, model_solution, score_path):
        self.x_sent = x_sent
        self.valid_labels = x_labels
        self.model_solution = model_solution
        self.score_path = score_path
        super(Log, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        pred_labels = self.model.predict(self.x_sent)
        pred_labels = np.argmax(pred_labels, axis=-1)
        valid_labels = np.argmax(self.valid_labels, axis=-1)
        score(valid_labels, pred_labels, self.model_solution, self.score_path)


class F1Metrics_Old(Callback):
    def __init__(self, num_classes, input_num=2):
        self.num_classes = num_classes
        self.input_num = input_num
        super(F1Metrics_Old, self).__init__()

    def on_train_begin(self, logs={}):
        self.val_f1s = []

    def get_value(self, res):
        if res["TP"] == 0:
            if res["FP"] == 0 and res["FN"] == 0:
                precision = 1.0
                recall = 1.0
                f1 = 1.0
            else:
                precision = 0.0
                recall = 0.0
                f1 = 0.0
        else:
            precision = 1.0 * res["TP"] / (res["TP"] + res["FP"])
            recall = 1.0 * res["TP"] / (res["TP"] + res["FN"])
            f1 = 2 * precision * recall / (precision + recall)

        return precision, recall, f1

    def on_epoch_end(self, epoch, logs={}):
        valid_y_pred = self.model.predict(self.validation_data[: self.input_num])
        print(valid_y_pred)
        # valid_y_pred = [valid_result[0] > 0.5 for valid_result in valid_results]
        valid_y_true = self.validation_data[self.input_num]

        results = []
        for i in range(self.num_classes):
            results.append({'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0})
        for i in range(len(valid_y_pred)):
            for j in range(self.num_classes):
                if valid_y_pred[i][j] > 0.5:
                    if valid_y_true[i][j] > 0:
                        results[j]['TP'] += 1
                    else:
                        results[j]['FP'] += 1
                else:
                    if valid_y_true[i][j] > 0:
                        results[j]['FN'] += 1
                    else:
                        results[j]['TN'] += 1

        sumf = 0
        y = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
        for x in results:
            p, r, f = self.get_value(x)
            sumf += f
            for z in x.keys():
                y[z] += x[z]

        _, __, f_ = self.get_value(y)

        _val_f1 = (f_ + sumf * 1.0 / len(results)) / 2.0

        logs['val_f1'] = _val_f1
        self.val_f1s.append(_val_f1)
        print('- val_f1: %.4f' % (_val_f1))
        return


class SeqF1Metrics(Callback):
    def __init__(self, num_classes, input_num=2, topk=3):
        self.num_classes = num_classes
        self.input_num = input_num
        self.max_len = num_classes + 1
        self.topk = topk
        super(SeqF1Metrics, self).__init__()

    def on_train_begin(self, logs={}):
        self.val_f1s = []

    def get_value(self, res):
        if res["TP"] == 0:
            if res["FP"] == 0 and res["FN"] == 0:
                precision = 1.0
                recall = 1.0
                f1 = 1.0
            else:
                precision = 0.0
                recall = 0.0
                f1 = 0.0
        else:
            precision = 1.0 * res["TP"] / (res["TP"] + res["FP"])
            recall = 1.0 * res["TP"] / (res["TP"] + res["FN"])
            f1 = 2 * precision * recall / (precision + recall)

        return precision, recall, f1

    def pad(self, x_data, max_len=None):
        return pad_sequences(x_data, maxlen=max_len, padding='post', truncating='post')

    def on_epoch_end(self, epoch, logs={}):
        y_true = self.validation_data[self.input_num - 1]
        valid_y_true = []
        for i in range(len(y_true)):
            last = 0
            for j in range(len(y_true[i])):
                if y_true[i][j] == 0:
                    last = j - 1
                    break
            y = y_true[i][1: last]
            yy = [0] * self.num_classes
            # print i, last, y
            for l in y:
                yy[l - 3] = 1
            # if len(y) == 0:
            #     yy[0] = 1
            valid_y_true.append(yy)
        valid_y_pred = []
        for n in tqdm(range(len(valid_y_true))):
            # print n
            data = []
            for i in range(self.input_num - 1):
                data.append(np.array([self.validation_data[i][n]] * self.topk))
            yid = np.array([[1]] * self.topk)
            scores = [0] * self.topk
            for i in range(self.max_len):
                label = self.pad(yid, max_len=self.num_classes + 2)
                proba = self.model.predict(data + [label])[:, i, 2:]  # 直接忽略<padding>、<start>
                log_proba = np.log(proba + 1e-6)  # 取对数，方便计算
                arg_topk = log_proba.argsort(axis=1)[:, -self.topk:]  # 每一项选出topk
                _yid = []  # 暂存的候选目标序列
                _scores = []  # 暂存的候选目标序列得分
                if i == 0:
                    for j in range(self.topk):
                        _yid.append(list(yid[j]) + [arg_topk[0][j] + 2])
                        _scores.append(scores[j] + log_proba[0][arg_topk[0][j]])
                else:
                    for j in range(self.topk):
                        for k in range(self.topk):  # 遍历topk*topk的组合
                            _yid.append(list(yid[j]) + [arg_topk[j][k] + 2])
                            _scores.append(scores[j] + log_proba[j][arg_topk[j][k]])
                    _arg_topk = np.argsort(_scores)[-self.topk:]  # 从中选出新的topk
                    _yid = [_yid[k] for k in _arg_topk]
                    _scores = [_scores[k] for k in _arg_topk]
                yid = np.array(_yid)
                scores = np.array(_scores)
                ends = np.where(yid[:, -1] == 3)[0]
                if len(ends) > 0:
                    k = ends[scores[ends].argmax()]
                    y = yid[k][1: -1]
                    yy = [0] * self.num_classes
                    for l in y:
                        yy[l - 3] = 1
                    if len(y) == 0:
                        yy[0] = 1
                    valid_y_pred.append(yy)
                    break
                elif i == self.max_len - 1:
                    y = yid[np.argmax(scores)][1:]
                    yy = [0] * self.num_classes
                    for l in y:
                        yy[l - 3] = 1
                    if len(y) == 0:
                        yy[0] = 1
                    valid_y_pred.append(yy)

        results = []
        for i in range(self.num_classes):
            results.append({'TP': 0, 'FP': 0, 'TN': 0, 'FN': 0})
        for i in range(len(valid_y_pred)):
            for j in range(self.num_classes):
                if valid_y_pred[i][j] > 0:
                    if valid_y_true[i][j] > 0:
                        results[j]['TP'] += 1
                    else:
                        results[j]['FP'] += 1
                else:
                    if valid_y_true[i][j] > 0:
                        results[j]['FN'] += 1
                    else:
                        results[j]['TN'] += 1

        sumf = 0
        y = {"TP": 0, "FP": 0, "FN": 0, "TN": 0}
        for x in results:
            p, r, f = self.get_value(x)
            sumf += f
            for z in x.keys():
                y[z] += x[z]

        _, __, f_ = self.get_value(y)

        _val_f1 = (f_ + sumf * 1.0 / len(results)) / 2.0

        logs['val_f1'] = _val_f1
        self.val_f1s.append(_val_f1)
        print('- val_f1: %.4f' % (_val_f1))
        return
