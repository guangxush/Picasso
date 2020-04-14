# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt


def draw_histogram():
    input_file = '../result/score.md'
    start_line = 3 - 1
    end_line = 12 - 1
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    item = solution  # ['A', 'B', 'C']
    num1 = f1  # [0.5, 0.6, 0.7]
    num2 = precision  # [0.75, 0.85, 0.95]  # 这里对数据进行了截断，所有值都减去了2，只画从2开始的部分
    x = list(range(len(num1)))  # 横坐标
    print(num1)
    print(num2)
    width = 0.4  # 每一根“柱”的宽度
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], [0, 0.2, 0.4, 0.6, 0.8, 1.0])
    # 设置y坐标，实际数值是前一组，标记数值为后一组
    plt.bar(x, num1, width=width, label='f1', fc='#B0C4DE')  # 画第一组
    for i in range(len(x)):
        x[i] = x[i] + width  # 横坐标移动
    plt.bar(x, num2, width=width, label='acc', fc='#4682B4')  # 画第二组

    y = []
    for i in range(len(x)):
        y.append(x[i] - width / 2)
    ax.set_xticks(y)  # 令对象名称出现在相邻两"柱"中间位置
    ax.set_xticklabels(item)

    plt.tick_params(labelsize=6)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]  # 坐标轴字体设置

    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 16,
             }
    plt.legend(prop=font1)  # 图例字体设置

    plt.grid(axis="y")
    plt.xlabel('Item', font1)
    plt.ylabel('Value', font1)
    plt.title('Parallel Histogram', font1)
    plt.show()


def draw_line():
    input_file = '../result/score.md'
    start_line = 3 - 1
    end_line = 13 - 1
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    # x = solution[1:]  # ['A', 'B', 'C']
    num1 = f1[1:]  # [0.5, 0.6, 0.7]
    num2 = auc[1:]  # [0.75, 0.85, 0.95]  # 这里对数据进行了截断，所有值都减去了2，只画从2开始的部分
    time = time[1:]

    plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    plt.plot(x, num1, label='SRT F1', linestyle='--', color='r', marker='D')
    plt.plot(x, num2, label='SRT AUC', linestyle='--', color='g', marker='o')

    for a, b, c in zip(x, num1, time):
        plt.text(a, b, '%s' % c, ha='center', va='bottom', fontsize=6, wrap=True, rotation=45)

    plt.ylim(0.7, 0.9)
    plt.xticks(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 8,
             }
    plt.legend(prop=font1, loc=4)

    plt.grid(axis="y")
    plt.xlabel('Forecast Indicator', font1)
    plt.ylabel('Iterator Count', font1)
    plt.title('Training f1 and auc of iterative incremental learning', font1)
    plt.show()
    return


def draw_line_new():
    input_file = '../result/score_temp.md'
    start_line = 3 - 1
    end_line = 33 - 1
    figure, ax = plt.subplots()
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num1 = f1[:10]
    num2 = auc[:10]
    time1 = time[:10]

    num3 = f1[10:20]
    num4 = auc[10:20]
    time2 = time[10:20]

    num5 = f1[20:]
    num6 = auc[20:]
    time3 = time[20:]

    # plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    # plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    plt.plot(x, num1, label='S+T F1', linestyle='-', color='r', marker='D')
    plt.plot(x, num2, label='S+T AUC', linestyle='-', color='g', marker='o')

    plt.plot(x, num3, label='S+R+T F1', linestyle='--', color='b', marker='h')
    plt.plot(x, num4, label='S+R+T AUC', linestyle='--', color='m', marker='v')

    plt.plot(x, num5, label='One-Time F1', linestyle=':', color='k', marker='s')
    plt.plot(x, num6, label='One-Time AUC', linestyle=':', color='y', marker='d')

    # for a, b, c in zip(x, num1, time1):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='r')
    #
    # for a, b, c in zip(x, num3, time2):
    #     plt.text(a, b+0.005, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='b')
    #
    # for a, b, c in zip(x, num5, time3):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')

    plt.ylim(0.75, 0.9)
    plt.xticks(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 12,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 8,
             }
    plt.legend(prop=font2, loc=4)

    plt.grid(axis="y")
    plt.xlabel('Iterations', font1)
    plt.ylabel('Prediction Indicator', font1)
    plt.title('The F1 and AUC of Different Methods', font1)
    plt.show()
    return


def draw_line_new_f1():
    input_file = '../result/score_temp.md'
    start_line = 3 - 1
    end_line = 33 - 1
    # figure, ax = plt.subplots()
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    num1 = f1[:10]
    # num2 = auc[:10]
    # time1 = time[:10]

    num3 = f1[10:20]
    # num4 = auc[10:20]
    # time2 = time[10:20]

    num5 = f1[20:]
    # num6 = auc[20:]
    # time3 = time[20:]

    # plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    # plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    plt.plot(x, num1, label='S+T F1', linestyle='-', color='dimgray', marker='D')
    # plt.plot(x, num2, label='S+T AUC', linestyle='-', color='g', marker='o')

    plt.plot(x, num3, label='S+R+T F1', linestyle='--', color='deeppink', marker='h')
    # plt.plot(x, num4, label='S+R+T AUC', linestyle='--', color='m', marker='v')

    plt.plot(x, num5, label='One-Time F1', linestyle=':', color='darkcyan', marker='s')
    # plt.plot(x, num6, label='One-Time AUC', linestyle=':', color='y', marker='d')

    # for a, b, c in zip(x, num1, time1):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='r')
    #
    # for a, b, c in zip(x, num3, time2):
    #     plt.text(a, b+0.005, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='b')
    #
    # for a, b, c in zip(x, num5, time3):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')

    plt.ylim(0.76, 0.85)
    plt.xticks(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 12,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 10,
             }
    plt.legend(prop=font2, loc=4)

    plt.grid(axis="y")
    plt.xlabel('Iterations', font1)
    plt.ylabel('Prediction Indicator', font1)
    plt.title('The F1 of Different Methods', font1)
    plt.savefig('../result/image/F1_10.pdf')
    plt.show()
    return


def draw_line_new_auc():
    input_file = '../result/score_temp.md'
    start_line = 3 - 1
    end_line = 33 - 1
    # figure, ax = plt.subplots()
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # num1 = f1[:10]
    num2 = auc[:10]
    # time1 = time[:10]

    # num3 = f1[10:20]
    num4 = auc[10:20]
    # time2 = time[10:20]

    # num5 = f1[20:]
    num6 = auc[20:]
    # time3 = time[20:]

    # plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    # plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    # plt.plot(x, num1, label='S+T F1', linestyle='-', color='r', marker='D')
    plt.plot(x, num2, label='S+T AUC', linestyle='-', color='dimgray', marker='o')

    # plt.plot(x, num3, label='S+R+T F1', linestyle='--', color='b', marker='h')
    plt.plot(x, num4, label='S+R+T AUC', linestyle='--', color='deeppink', marker='v')

    # plt.plot(x, num5, label='One-Time F1', linestyle=':', color='k', marker='s')
    plt.plot(x, num6, label='One-Time AUC', linestyle=':', color='darkcyan', marker='d')

    # for a, b, c in zip(x, num1, time1):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='r')
    #
    # for a, b, c in zip(x, num3, time2):
    #     plt.text(a, b+0.005, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='b')
    #
    # for a, b, c in zip(x, num5, time3):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')

    plt.ylim(0.84, 0.9)
    plt.xticks(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 12,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 10,
             }
    plt.legend(prop=font2, loc=4)

    plt.grid(axis="y")
    plt.xlabel('Iterations', font1)
    plt.ylabel('Prediction Indicator', font1)
    plt.title('The AUC of Different Methods', font1)
    plt.savefig('../result/image/AUC_10.pdf')
    plt.show()
    return


def draw_20():
    input_file = '../result/score_temp.md'
    start_line = 34 - 1
    end_line = 54 - 1
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    num1 = f1[:20]
    num2 = auc[:20]
    time1 = time[:20]

    time1_value = time1
    for i in range(0, len(time1)):
        time1_value[i] = time_convert_str(time1[i])

    # plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    # plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    plt.plot(x, num1, label='S+R+T+D F1', linestyle='--', color='b', marker='h')
    plt.plot(x, num2, label='S+R+T+D AUC', linestyle='--', color='m', marker='v')

    # index = 0
    # for a, b, c in zip(x, num1, time1_value):
    #     if index == 0:
    #         plt.text(a, b-0.006, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     elif index % 2 == 0:
    #         plt.text(a, b+0.005, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     else:
    #         plt.text(a, b-0.007, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     index += 1
    plt.ylim(0.75, 0.9)
    plt.xticks(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 12,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 10,
             }
    plt.legend(prop=font2, loc=4)

    plt.grid(axis="y")
    plt.xlabel('Iterations', font1)
    plt.ylabel('Prediction Indicator', font1)
    plt.title('The F1 and AUC of Learn# Method', font1)
    plt.show()
    return


def draw_20_F1():
    input_file = '../result/score_temp.md'
    start_line = 34 - 1
    end_line = 74 - 1
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    num1 = f1[:20]
    num2 = f1[20:41]
    # time1 = time[:20]
    #
    # time1_value = time1
    # for i in range(0, len(time1)):
    #     time1_value[i] = time_convert_str(time1[i])

    # plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    # plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    plt.plot(x, num1, label='S+R+T+D F1', linestyle='--', color='deeppink', marker='h')
    plt.plot(x, num2, label='S+R+T F1', linestyle='--', color='royalblue', marker='v')

    # index = 0
    # for a, b, c in zip(x, num1, time1_value):
    #     if index == 0:
    #         plt.text(a, b-0.006, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     elif index % 2 == 0:
    #         plt.text(a, b+0.005, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     else:
    #         plt.text(a, b-0.007, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     index += 1
    plt.ylim(0.75, 0.85)
    plt.xticks(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 12,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 10,
             }
    plt.legend(prop=font2, loc=4)

    plt.grid(axis="y")
    plt.xlabel('Iterations', font1)
    plt.ylabel('Prediction Indicator', font1)
    plt.title('The F1 of Learn# Method', font1)
    plt.savefig('../result/image/F1_20.pdf')
    plt.show()
    return


def draw_20_AUC():
    input_file = '../result/score_temp.md'
    start_line = 34 - 1
    end_line = 74 - 1
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    num1 = auc[:20]
    num2 = auc[20:41]

    # plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    # plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    plt.plot(x, num1, label='S+R+T+D AUC', linestyle='--', color='deeppink', marker='h')
    plt.plot(x, num2, label='S+R+T AUC', linestyle='--', color='royalblue', marker='v')

    # index = 0
    # for a, b, c in zip(x, num1, time1_value):
    #     if index == 0:
    #         plt.text(a, b-0.006, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     elif index % 2 == 0:
    #         plt.text(a, b+0.005, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     else:
    #         plt.text(a, b-0.007, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')
    #     index += 1
    plt.ylim(0.85, 0.9)
    plt.xticks(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 12,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 10,
             }
    plt.legend(prop=font2, loc=4)

    plt.grid(axis="y")
    plt.xlabel('Iterations', font1)
    plt.ylabel('Prediction Indicator', font1)
    plt.title('The AUC of Learn# Method', font1)
    plt.savefig('../result/image/AUC_20.pdf')
    plt.show()
    return


def get_data_with_storage(input_file, start_line, end_line):
    fr = open(input_file, 'r')
    solution = []
    precision = []
    recall = []
    f1 = []
    accuracy = []
    auc = []
    time = []
    storage = []
    line_num = 0
    temp = []
    for line in fr:
        if line_num >= start_line:
            if line_num >= end_line:
                break
            line = line.strip('|').split('|')
            solution.append(line[0])
            precision.append(float(line[1]))
            recall.append(float(line[2]))
            f1.append(float(line[3]))
            accuracy.append(float(line[4]))
            auc.append(float(line[5]))
            # time.append(float(line[6][-2:]) / 2.0)
            time.append(str(line[6]))
            if len(line) > 7:
                storage.append(str(line[7]))
            temp.append(line)
        line_num += 1
    if len(temp) > 7:
        return solution, precision, recall, f1, accuracy, auc, time, storage
    return solution, precision, recall, f1, accuracy, auc, time


def get_data(input_file, start_line, end_line):
    fr = open(input_file, 'r')
    solution = []
    precision = []
    recall = []
    f1 = []
    accuracy = []
    auc = []
    time = []
    storage = []
    line_num = 0
    for line in fr:
        if line_num >= start_line:
            if line_num >= end_line:
                break
            line = line.strip('|').split('|')
            solution.append(line[0])
            precision.append(float(line[1]))
            recall.append(float(line[2]))
            f1.append(float(line[3]))
            accuracy.append(float(line[4]))
            auc.append(float(line[5]))
            # time.append(float(line[6][-2:]) / 2.0)
            time.append(str(line[6]))
        line_num += 1
    return solution, precision, recall, f1, accuracy, auc, time


def draw_time():
    input_file = '../result/score_temp.md'
    start_line = 3 - 1
    end_line = 33 - 1
    solution, precision, recall, f1, accuracy, auc, time = get_data(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    item = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    time1 = time[:10]

    time2 = time[10:20]

    time3 = time[20:]

    time1_value, time2_value, time3_value = time1, time2, time3

    for i in range(0, len(time1)):
        time1_value[i] = float(time_convert(time1[i]))

    for i in range(0, len(time2)):
        time2_value[i] = float(time_convert(time2[i]))

    for i in range(0, len(time3)):
        time3_value[i] = float(time_convert(time3[i]))

    # plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    # plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    # for a, b, c in zip(x, time1_value, time1):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='r')
    #
    # for a, b, c in zip(x, time2_value, time2):
    #     plt.text(a, b+0.005, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='b')
    #
    # for a, b, c in zip(x, time3_value, time3):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')

    width = 0.2  # 每一根“柱”的宽度
    plt.yticks([0, 300, 600, 900, 1200, 1500, 1800, 2100], ['0', '5min', '10min', '15min', '20min', '25min', '30min', '35min'])
    # 设置y坐标，实际数值是前一组，标记数值为后一组
    plt.bar(x, time1_value, width=width, label='S+T', fc='slategrey')  # 画第一组
    for i in range(len(x)):
        x[i] = x[i] + width  # 横坐标移动
    plt.bar(x, time2_value, width=width, label='S+R+T', fc='deeppink')  # 画第二组
    for i in range(len(x)):
        x[i] = x[i] + width  # 横坐标移动
    plt.bar(x, time3_value, width=width, label='One-Time', fc='deepskyblue')  # 画第三组

    # y = []
    # for i in range(len(x)):
    #     y.append(x[i])
    ax.set_xticks(item)  # 令对象名称出现在相邻两"柱"中间位置
    # ax.set_xticklabels(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 12,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 10,
             }
    plt.legend(prop=font2, loc=0)

    plt.grid(axis="y")
    plt.xlabel('Iterations', font1)
    plt.ylabel('Training time (min)', font1)
    plt.title('The Training time of Different Methods', font1)
    plt.savefig('../result/image/time.pdf')
    plt.show()


def draw_storage():
    input_file = '../result/score_temp.md'
    start_line = 3 - 1
    end_line = 33 - 1
    solution, precision, recall, f1, accuracy, auc, time, storage = get_data_with_storage(input_file, start_line, end_line)
    figure, ax = plt.subplots()
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    item = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    storage1 = storage[:10]

    storage2 = storage[10:20]

    storage3 = storage[20:]

    storage1_value, storage2_value, storage3_value = storage1, storage2, storage3

    for i in range(0, len(storage1)):
        storage1_value[i] = int((storage1[i]))

    for i in range(0, len(storage2)):
        storage2_value[i] = int((storage2[i]))

    for i in range(0, len(storage3)):
        storage3_value[i] = int((storage3[i]))

    # plt.hlines(f1[0], 0, 10, linestyle='-.', colors="r", label='One-Time F1')
    # plt.hlines(auc[0], 0, 10, linestyle='-.', colors="g", label='One-Time AUC')

    # for a, b, c in zip(x, time1_value, time1):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='r')
    #
    # for a, b, c in zip(x, time2_value, time2):
    #     plt.text(a, b+0.005, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='b')
    #
    # for a, b, c in zip(x, time3_value, time3):
    #     plt.text(a, b-0.01, '%s' % c, ha='center', va='bottom', fontsize=7, wrap=True, rotation=0, color='k')

    width = 0.2  # 每一根“柱”的宽度
    plt.yticks([0, 100, 200, 300, 400, 500], ['0', '100M', '200M', '300M', '400M', '500M'])
    # 设置y坐标，实际数值是前一组，标记数值为后一组
    plt.bar(x, storage1_value, width=width, label='S+T', fc='slategrey')  # 画第一组
    for i in range(len(x)):
        x[i] = x[i] + width  # 横坐标移动
    plt.bar(x, storage2_value, width=width, label='S+R+T', fc='deeppink')  # 画第二组
    for i in range(len(x)):
        x[i] = x[i] + width  # 横坐标移动
    plt.bar(x, storage3_value, width=width, label='One-Time', fc='deepskyblue')  # 画第三组

    # y = []
    # for i in range(len(x)):
    #     y.append(x[i])
    ax.set_xticks(item)  # 令对象名称出现在相邻两"柱"中间位置
    # ax.set_xticklabels(x)

    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    font1 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 12,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'heavy',
             'size': 10,
             }
    plt.legend(prop=font2, loc=0)

    plt.grid(axis="y")
    plt.xlabel('Iterations', font1)
    plt.ylabel('Storage Space (M)', font1)
    plt.title('The Storage Space of Different Methods', font1)
    plt.savefig('../result/image/storage.pdf')
    plt.show()


def time_convert(time):
    time_new = time.split(':')
    time_value = int(time_new[1])*60 + int(time_new[2])
    return time_value


def time_convert_str(time):
    time_new = time.split(':')
    time_value = time_new[1][1]+'min'+time_new[2]+'s'
    return time_value


if __name__ == '__main__':
    # draw_histogram()
    # https://blog.csdn.net/u012328159/article/details/79240652
    # 颜色 https://www.cnblogs.com/darkknightzh/p/6117528.html
    # draw_20()
    # draw_storage()
    # draw_time()
    # draw_20()
    # draw_20_F1()
    # draw_20_AUC()
    # draw_line_new_f1()
    draw_line_new_auc()
