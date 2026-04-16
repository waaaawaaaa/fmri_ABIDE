from sklearn.linear_model import LogisticRegression
import numpy as np
from tqdm import tqdm

import os

from subjectReader import getSubjects, readSubject


def tokenExtractor(dataset, seed, topK, startK):

    targetDataset = dataset

    foldCount = 5
    if(targetDataset == "abide1"):
        foldCount = 10

    targetFolds = range(foldCount)    


    for targetFold in targetFolds:
        #构建用于存储训练数据的文件夹
        saveFolder_train = "./Analysis/DataExtracted/{}/seed_{}/{}/TRAIN/startK_{}".format(targetDataset, seed, targetFold, startK)
        saveFolder_test = "./Analysis/DataExtracted/{}/seed_{}/{}/TEST/startK_{}".format(targetDataset, seed, targetFold, startK)

        if(os.path.exists(saveFolder_train + "/x_train_static.npy") and os.path.exists(saveFolder_test + "/x_test_static.npy")):
            continue

        os.makedirs(saveFolder_train, exist_ok=True)
        os.makedirs(saveFolder_test, exist_ok=True)


        trainSubjectDirs = getSubjects(targetDataset, seed, targetFold, True) #读入训练集数据的所有文件路径
        testSubjectDirs = getSubjects(targetDataset, seed, targetFold, False)#读入测试集数据

        train_random_subjIds = []   #随机
        test_random_subjIds = []

        x_train_random = []
        x_train_random_relevancyScore = []

        y_train_random = []

        x_test_random = []
        
        x_test_random_relevancyScore = []

        y_test_random = []



        train_static_subjIds = []   #统计
        test_static_subjIds = []

        x_train_static = []
        x_train_static_relevancyScore = []

        y_train_static = []

        x_test_static = []
        x_test_static_relevancyScore = []

        y_test_static = []


        print("Extracting train subjects...")

        for subjectDir in tqdm(trainSubjectDirs, ncols=60):  #显示进度条

            subjId = subjectDir.split("/")[-1]  #通过将路径按 "/" 分割成列表，并取最后一个元素作为主题的ID

            attentionMaps, clsRelevancyMap, label, inputTokens = readSubject(subjectDir)   ##读入4层的注意力图，label，clsRelevancyMap，时间序列数据每个时间点的roi，196个400
            attentionMap = attentionMaps[-1].mean(axis=1)  #  [4,6,36,21,69]  计算最后一个注意力图的平均值，沿着第一个轴（axis=1）进行计算，head上平均了 [6,21,69]
        

            clsRelevancyMap = clsRelevancyMap.mean(axis=0)  #[6,60]或者[23,196]  在窗口上平均了,还剩时间T

            if(startK + topK <= clsRelevancyMap.shape[0]):

                if(startK != 0):  #如果起始索引 startK 不为0
                    target_ind_static = np.argsort(clsRelevancyMap)[-startK - topK: -startK]  #对 clsRelevancyMap 数组进行排序，并选择从倒数第 startK + topK 个到倒数第 startK 个之间的索引  排序，取后面几个
                else:   #从小到大排序
                    target_ind_static = np.argsort(clsRelevancyMap)[-topK:]  #选择倒数前 topK 个索引

            else: 

                target_ind_static = np.argsort(clsRelevancyMap)[0:topK]  #选择前 topK 个索引

            # STATIC
            targetTokens = inputTokens[target_ind_static]  #inputTokens[196,400]提取时间序列前最大前K个的索引  [5,400]为什么在时间上提取？？？？提取出TOKEN
            
            averageRelScore = np.mean(clsRelevancyMap[target_ind_static]) / np.min(clsRelevancyMap)#clsmap最大5个的平均值除以最小值

            for token in targetTokens:  #在时间上，取最有鉴别力的前几个时间
                x_train_static.append(token)
                y_train_static.append(label)
                x_train_static_relevancyScore.append(averageRelScore)
                train_static_subjIds.append(subjId)

            # RANDOM  随机取几个时间点
            randomIdx = np.random.choice(range(len(clsRelevancyMap)), len(targetTokens))
            averageRelScore = np.mean(clsRelevancyMap[randomIdx]) / np.min(clsRelevancyMap)

            for idx in randomIdx:
                x_train_random.append(inputTokens[idx])
                y_train_random.append(label)
                x_train_random_relevancyScore.append(averageRelScore)
                train_random_subjIds.append(subjId)

                    

        print("Extracting test subjects...")
        for subjectDir in tqdm(testSubjectDirs, ncols=60):
            attentionMaps, clsRelevancyMap, label, inputTokens = readSubject(subjectDir)
            attentionMap = attentionMaps[-1].mean(axis=1)

            subjId = subjectDir.split("/")[-1]
            

            clsRelevancyMap = clsRelevancyMap.mean(axis=0)


            if(startK + topK <= clsRelevancyMap.shape[0]):

                if(startK != 0):
                    target_ind_static = np.argsort(clsRelevancyMap)[-startK - topK: -startK]
                else:
                    target_ind_static = np.argsort(clsRelevancyMap)[-topK:]
            else: 
                target_ind_static = np.argsort(clsRelevancyMap)[0:topK]                    

            # STATIC
            targetTokens = inputTokens[target_ind_static]    
            averageRelScore = np.mean(clsRelevancyMap[target_ind_static]) / np.min(clsRelevancyMap)

            for token in targetTokens:
                x_test_static.append(token)
                y_test_static.append(label)
                x_test_static_relevancyScore.append(averageRelScore)
                test_static_subjIds.append(subjId)

            # RANDOM
            randomIdx = np.random.choice(range(len(clsRelevancyMap)), len(targetTokens))
            averageRelScore = np.mean(clsRelevancyMap[randomIdx]) / np.min(clsRelevancyMap)

            for idx in randomIdx:
                x_test_random.append(inputTokens[idx])
                y_test_random.append(label)        
                x_test_random_relevancyScore.append(averageRelScore)
                test_random_subjIds.append(subjId)

                        
        np.save(saveFolder_train + "/x_train_static.npy", x_train_static)  #x y 和x的一个系数
        np.save(saveFolder_train + "/x_train_static_relevancyScore.npy", x_train_static_relevancyScore)
        np.save(saveFolder_train + "/x_train_random.npy", x_train_random)
        np.save(saveFolder_train + "/x_train_random_relevancyScore.npy", x_train_random_relevancyScore)
        np.save(saveFolder_train + "/y_train_static.npy", y_train_static)
        np.save(saveFolder_train + "/y_train_random.npy", y_train_random)                

        np.save(saveFolder_test + "/x_test_static.npy", x_test_static)
        np.save(saveFolder_test + "/x_test_static_relevancyScore.npy", x_test_static_relevancyScore)
        np.save(saveFolder_test + "/x_test_random.npy", x_test_random)
        np.save(saveFolder_test + "/x_test_random_relevancyScore.npy", x_test_random_relevancyScore)
        np.save(saveFolder_test + "/y_test_static.npy", y_test_static)
        np.save(saveFolder_test + "/y_test_random.npy", y_test_random)


        np.save(saveFolder_train + "/train_random_subjIds.npy", train_random_subjIds)  #训练测试的受试者名
        np.save(saveFolder_test + "/test_random_subjIds.npy", test_random_subjIds)

        np.save(saveFolder_train + "/train_static_subjIds.npy", train_static_subjIds)
        np.save(saveFolder_test + "/test_static_subjIds.npy", test_static_subjIds)


    #clf = LogisticRegression(random_state=0).fit(x_train, y_train)