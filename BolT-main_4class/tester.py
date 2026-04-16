
# parse the arguments

import argparse
import torch
from datetime import datetime


from utils import Option, metricSummer, calculateMetrics, dumpTestResults
# 创建了一个解析器，并添加了一些命令行参数。这些参数包括数据集名称、模型名称、是否进行分析、设备编号和模型名称
parser = argparse.ArgumentParser()

parser.add_argument("-d", "--dataset", type=str, default="abide1")
parser.add_argument("-m", "--model", type=str, default="bolT")
parser.add_argument("-a", "--analysis", type=bool, default=False)
parser.add_argument("--device", type=int, default=3)  #GPU
parser.add_argument("--name", type=str, default="noname")


argv = parser.parse_args()



from Dataset.datasetDetails import datasetDetailsDict
# 数据集信息，所用的数据集，做几分类，epoch，foldCount，batchSize

# import model runners

from Models.SVM.run import run_svm
from Models.BolT.run import run_bolT 
# import hyper param fetchers

from Models.SVM.hyperparams import getHyper_svm
from Models.BolT.hyperparams import getHyper_bolT

hyperParamDict = {

        "svm" : getHyper_svm,
        "bolT" : getHyper_bolT,   #网络中的一些超参数，学习率，移动窗什么的

}

modelDict = {

        "svm" : run_svm,
        "bolT" : run_bolT,
}


getHyper = hyperParamDict[argv.model]  #ABIDE
runModel = modelDict[argv.model]     #bolT

print("\nTest model is {}".format(argv.model))


datasetName = argv.dataset
datasetDetails = datasetDetailsDict[datasetName]
hyperParams = getHyper()

print("Dataset details : {}".format(datasetDetails))

# test

if(datasetName == "abide1"):
    seeds = [0,1,2,3,4]
else:
    seeds = [0]
    
resultss = []

for i, seed in enumerate(seeds):

    # for reproducability
    torch.manual_seed(seed) #设置CPU生成随机数的种子，方便下次复现实验结果。将随机种子放进数据集

    print("Running the model with seed : {}".format(seed))
    if(argv.model == "bolT"):
        results = runModel(hyperParams, Option({**datasetDetails,"datasetSeed":seed}), device="cuda:{}".format(argv.device), analysis=argv.analysis)
    else:
        results = runModel(hyperParams, Option({**datasetDetails,"datasetSeed":seed}), device="cuda:{}".format(argv.device))

    resultss.append(results)
    


metricss = calculateMetrics(resultss) 
meanMetrics_seeds, stdMetrics_seeds, meanMetric_all, stdMetric_all = metricSummer(metricss, "test")

# now dump metrics
dumpTestResults(argv.name, hyperParams, argv.model, datasetName, metricss)

print("\n \ n meanMetrics_all : {}".format(meanMetric_all))
print("stdMetric_all : {}".format(stdMetric_all))

