#!/usr/bin/python
# -*- coding:utf8 -*-
from scipy.io import loadmat,savemat
from sklearn.model_selection import StratifiedShuffleSplit  #每次分成类似于分层抽样分成训练和测试，分10次
import numpy as np
from sklearn.metrics import accuracy_score,precision_score, recall_score, f1_score


def load_data_kfold(k,datatype,path,random_state=111):
    data = loadmat(path)  #读取mat文件
    if datatype == 'sfc':
        X = data.get('data')
    elif datatype == 'tc':
        X = data.get('tc_data_170')
    y = data.get('label').T    #疾病或健康
    folds = list(StratifiedShuffleSplit(n_splits=k,random_state=random_state).split(X, y))#n_splits分成10组
    return folds, X, y

from sklearn.metrics import auc
from sklearn import metrics
def acc_pre_recall_f(y_true,y_pred,y_score):
    tp = float(sum(y_true & y_pred))
    fp = float(sum((y_true == 0) & (y_pred == 1)))
    tn = float(sum((y_true == 0) & (y_pred == 0)))
    fn = float(sum((y_true == 1) & (y_pred == 0)))
    acc = accuracy_score(y_true,y_pred)  # 准确率，即正确预测样本数占总样本数的比例
    sensitivity = tp/(tp + fn)
    f1 = f1_score(y_true,y_pred)
    specificity = tn / (fp + tn)
    fpr, tpr, thresholds = metrics.roc_curve(y_true,y_score)
    roc_auc = auc(fpr, tpr)
    return acc,specificity,sensitivity,f1,roc_auc


def metricSummer(metricss):
    # meanMetrics_seeds = [] #定义两个空列表和字典
    # meanMetric_all = {}
    #
    # stdMetrics_seeds = []
    # stdMetric_all = {}

    # for metrics in metricss:  # this is over different seeds
    #
    meanMetric = {}
    stdMetric = {}

    for metric in metricss:  # this is over different folds

        # metric = metric[type]  # get results from the specified type

        for key in metric.keys():  #提取出关键值
            if (key not in meanMetric):
                meanMetric[key] = []

            meanMetric[key].append(metric[key])

    for key in meanMetric:  #求均值和标准差
        stdMetric[key] = np.std(meanMetric[key])
        meanMetric[key] = np.mean(meanMetric[key])

    # meanMetrics_seeds.append(meanMetric)
    # stdMetrics_seeds.append(stdMetric)

    # for key in meanMetrics_seeds[0].keys():
    #     meanMetric_all[key] = np.mean([metric[key] for metric in meanMetrics_seeds])
    #     stdMetric_all[key] = np.mean([metric[key] for metric in stdMetrics_seeds])

    return meanMetric, stdMetric
