import time
import numpy as np
from Models.BolT.run import train
from utils import Option

from Models.SVM.model import Model
from Models.SVM.util import corrcoef, ledoit_wolf_corrcoef
from Dataset.dataset import getDataset


def calculateFC(timeseries):
    # 有很多个timeseries，滑动时间窗做的？？

    FCs = []

    for timeseries_ in timeseries:
        timeseries_ = np.array(timeseries_)
        FCs.append(corrcoef(timeseries_))
    #     求相关得到FC

    return np.array(FCs)


def extractDataLoader(dataLoader):#提取其中的时间序列和标签，并将它们分别返回

    timeseries = []
    labels = []

    for data in dataLoader:
        timeseries.extend(data["timeseries"].tolist())
        labels.extend(data["label"].tolist())

    labels = np.array(labels)

    return timeseries, labels


def run_svm(hyperParams, datasetDetails, device=None): # here device is added for compatibility with other deep learning gang 
    
    # extract datasetDetails
    foldCount = datasetDetails.foldCount


    dataset = getDataset(datasetDetails)

    results = []

    for fold in range(foldCount):

        print("Running svm fold : {}".format(fold))
        # 读出训练集和测试集
        train_dataLoader = dataset.getFold(fold, train=True)
        train_timeseries, train_labels = extractDataLoader(train_dataLoader)  #[659,400,60]
        
        test_dataLoader = dataset.getFold(fold, train=False)
        test_timeseries, test_labels = extractDataLoader(test_dataLoader)
        # 计算FC
        train_FCs = calculateFC(train_timeseries)  #[659,400,400]
        test_FCs = calculateFC(test_timeseries)

        model = Model(hyperParams)
        
        model.fit(train_FCs, train_labels)  #训练模型

        train_probs = model.predict_proba(train_FCs)  #返回每个类别的概率估计值，二分类的话有两个概率，左边属于类别1
        test_probs = model.predict_proba(test_FCs)

        train_predictions = train_probs.argmax(axis=1) #对训练数据的概率估计值沿着列方向（即类别方向）取最大值的索引，得到训练数据的类别预测结果
        test_predictions = test_probs.argmax(axis=1)

        result = {
            
                "train" : {
                   
                    "labels" : train_labels,
                    "predictions" : train_predictions,
                    "probs" : train_probs
                    
                    },

                "test" : {
                    
                    "labels": test_labels,
                    "predictions" : test_predictions,
                    "probs" : test_probs

                    }
        }

        results.append(result) 

    return results

