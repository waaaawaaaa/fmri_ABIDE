from brainRegressor import brainRegressor, saveImportanceResults
from impTokenExtractor import tokenExtractor
import torch
import os
import numpy as np
import argparse
import shutil
import sys

os.chdir("../../")   #将当前工作目录更改为上层目录的上层目录。
sys.path.append("./")

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dataset", type=str, default="abide1")   #默认数据集为 "abide1"
argv = parser.parse_args()



saveFolder = "./Analysis/DataExtracted/{}/Results".format(argv.dataset)
if(os.path.exists(saveFolder)):
    shutil.rmtree()  #如果路径存在，则递归删除该路径下的所有文件和文件夹。
os.makedirs(saveFolder, exist_ok=True)

#设置从哪个值开始取   设置目标targetSeeds，统计在哪个随机种子下
if(argv.dataset == "abide1"):
    targetSeeds = [0]#,1,2,3,4] 
    startKs = [0]#, 10, 15, 20, 25, 30, 35, 40, 45, 50]
elif(argv.dataset == "hcpRest"):
    targetSeeds = [0]
    startKs = [0]#, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
elif(argv.dataset == "hcpTask"):
    targetSeeds = [0]
    startKs = [0]#, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]


topK = 5  #做统计取前5个和随机取5个时间点，比较正确率


results_mean = []
results_std = []

testAccs_s_k = []
averageRelevancies_s_k = []
allImportance_0_k = []
allImportance_1_k = []
allImportances_k = []

for startK in startKs:
    
    testAccs_s = []
    averageRelevancies_s = []

    allImportances_s = []   #测试准确率、平均相关性和所有重要性的数据

    for seed in targetSeeds:
        tokenExtractor(argv.dataset, seed, topK, startK)  #以最优或者随机取几个时间点
        test_accuracies_static, averageRelevancies, allImportances = brainRegressor(argv.dataset, seed, startK)

        testAccs_s.append(test_accuracies_static)# 在每一个随机种子下记录受试者级别测试统计的正确率[1，10,1]， 测试统计平均cls系数[1，10,1]，重要性（统计）[1，2,400]
        averageRelevancies_s.append(averageRelevancies)

        allImportances_s.append(allImportances)

    testAccs_s_k.append(testAccs_s) # 在每一个startK开始K记录正确率[1，1，10,1]， 测试统计平均cls系数[1，1，10,1]，重要性在随机种子下的均值[1，2,400]
    averageRelevancies_s_k.append(averageRelevancies_s)

    allImportances_k.append(np.array(allImportances_s).mean(axis=0))

allImportances_final = np.array(allImportances_k).mean(axis=0)#重要性在每个startK下的均值[2,400]

saveImportanceResults(allImportances_final, saveFolder)


pandaResults_acc = []  #测试准确率
pandaResults_relScore = []  #平均相关性得分

for i, testAccs_s in enumerate(testAccs_s_k): # 开始K  [1，1，10,1]  提取在开始K时fold平均的正确率
    for testAccs in testAccs_s:    #随机种子[1，10,1]  testAccs [10,1]
        for testAcc in testAccs:
            pandaResults_acc.append([startKs[i], testAcc]) #[10,2],将开始K也插进去了

for i, averageRelevancies_s in enumerate(averageRelevancies_s_k):  #提取在开始K时fold平均的相关系数
    for averageRelevancies in averageRelevancies_s:    
        for averageRelevancy in averageRelevancies:
            pandaResults_relScore.append([startKs[i], averageRelevancy])#[10,2],将开始K也插进去了
                
import pandas as pd
import torch


pandaResults_acc = pd.DataFrame(data = pandaResults_acc, columns=["Group Index", "Accuracy"])
pandaResults_relScore = pd.DataFrame(data = pandaResults_relScore, columns=["Group Index", "Relevancy Score"])



torch.save(testAccs_s_k, saveFolder+"/testAccs_s_k.save")
torch.save(pandaResults_acc, saveFolder+"/pandaResults_acc.save")
torch.save(pandaResults_relScore, saveFolder+"/pandaResults_relScore.save")



figSave = "./Analysis/Figures/{}".format(argv.dataset)

import matplotlib.pyplot as plt
import seaborn as sns  #导入 Seaborn 库，用于数据可视化


sns.set(font_scale = 2)  #设置 Seaborn 库中字体的大小为 2 倍，这会影响后续图表的字体大小

fig1 = sns.relplot(data=pandaResults_acc, x="Group Index", y="Accuracy", color="b", kind="line", aspect=12/8.0)
fig1.savefig(figSave + "/{}_acc.png".format(argv.dataset), dpi=600)

fig2 = sns.relplot(data=pandaResults_relScore, x="Group Index", y="Relevancy Score", color="r", kind="line", aspect=12/8.0)
fig2.savefig(figSave + "/{}_relScore.png".format(argv.dataset), dpi=600)















