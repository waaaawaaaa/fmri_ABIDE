from glob import glob
import numpy as np

import sys
sys.path.append("../")

def getSubjects(dataset, seed, fold, isTrain):   #读取受试者的路径
    
    datasetNameToFolderDict = {
        "hcpRest" : "./Analysis/Data/hcpRest",
        "hcpTask" : "./Analysis/Data/hcpTask",
        "abide1" : "./Analysis/Data/abide1"
    }

    targetFolder = datasetNameToFolderDict[dataset]
    targetFolder += "/seed_{}/FOLD_{}".format(seed, fold)

    if(isTrain):
        targetFolder += "/TRAIN"
    else:
        targetFolder += "/TEST"

    print(targetFolder)

    subjects = glob(targetFolder + "/*")   #使用 glob 函数获取指定路径下的所有文件或文件夹，并将它们存储在 subjects 列表中

    return subjects

def readSubject(folder):  #读入4层的注意力图，label，clsRelevancyMap，时间序列数据每个时间点的roi，196个400
    attentionMaps = []
    for i in range(4):
        attentionMaps.append(np.load(folder + "/attentionMaps_layer{}.npy".format(i)))  #4层的注意力图
    clsRelevancyMap = np.load(folder + "/clsRelevancyMap.npy")
    label = np.load(folder + "/label.npy")
    inputTokens = np.load(folder + "/token_layerIn.npy")

    return attentionMaps, clsRelevancyMap, label, inputTokens