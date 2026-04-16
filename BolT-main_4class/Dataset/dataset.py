
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import StratifiedKFold
from random import shuffle, randrange
import numpy as np
import random

#from .DataLoaders.hcpRestLoader import hcpRestLoader
#from .DataLoaders.hcpTaskLoader import hcpTaskLoader
from .DataLoaders.abide1Loader import abide1Loader
# 用于映射不同的数据集名称到相应的加载函数。
loaderMapper = {
    #"hcpRest" : hcpRestLoader,
    #"hcpTask" : hcpTaskLoader,
    "abide1" : abide1Loader,
}

def getDataset(options):
    return SupervisedDataset(options)

class SupervisedDataset(Dataset):
    
    def __init__(self, datasetDetails):

        self.batchSize = datasetDetails.batchSize
        self.dynamicLength = datasetDetails.dynamicLength
        self.foldCount = datasetDetails.foldCount

        self.seed = datasetDetails.datasetSeed

        loader = loaderMapper[datasetDetails.datasetName]
        # 根据传入的数据集折数，创建一个StratifiedKFold对象
        self.kFold = StratifiedKFold(datasetDetails.foldCount, shuffle=False, random_state=None) if datasetDetails.foldCount is not None else None
        self.k = None

        self.data, self.labels, self.subjectIds = loader(datasetDetails.atlas, datasetDetails.targetTask)  #会≤871，因为前面去掉了roi为0的数据

        random.Random(self.seed).shuffle(self.data)   #打乱顺序
        random.Random(self.seed).shuffle(self.labels)
        random.Random(self.seed).shuffle(self.subjectIds)

        self.targetData = None
        self.targetLabel = None
        self.targetSubjIds = None

        self.randomRanges = None

        self.trainIdx = None
        self.testIdx = None

    def __len__(self):
        return len(self.data) if isinstance(self.targetData, type(None)) else len(self.targetData)


    def get_nOfTrains_perFold(self):
        if(self.foldCount != None):
            return int(np.ceil(len(self.data) * (self.foldCount - 1) / self.foldCount))           
        else:
            return len(self.data)        

    def setFold(self, fold, train=True):

        self.k = fold
        self.train = train


        if(self.foldCount == None): # if this is the case, train must be True
            trainIdx = list(range(len(self.data)))#创建一个包含从 0 到 self.data 的长度的索引列表，存储在变量 trainIdx 中
        else:  #10分类里面第fold个
            trainIdx, testIdx = list(self.kFold.split(self.data, self.labels))[fold]      

        self.trainIdx = trainIdx
        self.testIdx = testIdx

        random.Random(self.seed).shuffle(trainIdx) #将列表中的元素顺序打乱
        # 根据索引，提取数据，label，SubjId
        self.targetData = [self.data[idx] for idx in trainIdx] if train else [self.data[idx] for idx in testIdx]
        self.targetLabels = [self.labels[idx] for idx in trainIdx] if train else [self.labels[idx] for idx in testIdx]
        self.targetSubjIds = [self.subjectIds[idx] for idx in trainIdx] if train else [self.subjectIds[idx] for idx in testIdx]

        if(train and not isinstance(self.dynamicLength, type(None))):
            np.random.seed(self.seed+1)
            #列表中的每个元素都是一个列表，表示对于训练数据集中的每个索引 idx，在区间 [0, timepoint - 60) 中生成 9999 个随机数。
            self.randomRanges = [[np.random.randint(0, self.data[idx].shape[-1] - self.dynamicLength) for k in range(9999)] for idx in trainIdx]

    def getFold(self, fold, train=True):
        
        self.setFold(fold, train)

        if(train):
            return DataLoader(self, batch_size=self.batchSize, shuffle=False)
        else:
            return DataLoader(self, batch_size=1, shuffle=False)            


    def __getitem__(self, idx):
        
        subject = self.targetData[idx]
        label = self.targetLabels[idx]
        subjId = self.targetSubjIds[idx]


        # normalize timeseries
        timeseries = subject # (numberOfRois, time)

        timeseries = (timeseries - np.mean(timeseries, axis=1, keepdims=True)) / np.std(timeseries, axis=1, keepdims=True)  #z-score
        timeseries = np.nan_to_num(timeseries, 0) #将 timeseries 数组中的 NaN 值替换为 0

        # dynamic sampling if train
        if(self.train and not isinstance(self.dynamicLength, type(None))):
            if(timeseries.shape[1] < self.dynamicLength):
                print(timeseries.shape[1], self.dynamicLength)

            samplingInit = self.randomRanges[idx].pop()

            timeseries = timeseries[:, samplingInit : samplingInit + self.dynamicLength]

        return {"timeseries" : timeseries.astype(np.float32), "label" : label, "subjId" : subjId}







