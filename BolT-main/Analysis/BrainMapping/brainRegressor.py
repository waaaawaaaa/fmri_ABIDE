from re import sub
import numpy as np
import nilearn as nil
import nilearn.image
import nilearn.datasets
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib
from statistics import mode

from sklearn.linear_model import LogisticRegression


matplotlib.use('Agg')

roi = nil.datasets.fetch_atlas_schaefer_2018()  #获取了Schaefer 2018功能区域的数据，并将其赋值给变量 roi
roiMap = nil.image.load_img(roi["maps"])  #加载了功能区域地图，并将其赋值给变量 roiMap。
roiMap_array = roiMap.get_fdata()    #[182,218,182]将功能区域地图转换为Numpy数组，并将结果存储在变量 roiMap_array


def getSubjectwiseAccuracy(y_predicts, ys, subjectIds):  #该函数接受三个参数 y_predicts（预测结果列表）、ys（实际标签列表）和 subjectIds（受试者名），使用五个时间点预测的众数和label比较

    results_subjectWise = {}

    for i, y in enumerate(ys):  #遍历实际标签 ys，同时获取索引 i 和对应的真实标签 y
        subjectId = subjectIds[i] #提取第 i 个样本对应的subjectId和预测结果
        yPredict = y_predicts[i]

        if(not subjectId in results_subjectWise): #subjectId，如果不存在，则将其添加到字典中，并初始化对应的键值对（包括真实标签和预测结果
            results_subjectWise[subjectId] = {"groundTruth" : y, "predictions" : []}

        results_subjectWise[subjectId]["predictions"].append(yPredict)#subjectId如果存在，添加预测结果

    totalSubject = len(results_subjectWise.keys()) #计算总过有多少个受试者

    totalCorrectPredicts = 0

    for subjectId in results_subjectWise:
        
        if(mode(results_subjectWise[subjectId]["predictions"]) == results_subjectWise[subjectId]["groundTruth"]):#mode 函数计算该主题下所有预测结果的众数（即出现次数最多的值）
            totalCorrectPredicts += 1

    return totalCorrectPredicts / totalSubject

def saveImportanceResults(importances, saveFolderName):

    for i, importance in enumerate(importances):#[2,400]


        np.save(saveFolderName + "/importance_{}.npy".format(i), importance)

        plt.figure()# 保存为Importance_0或_1.npy格式，并画图保存成.png格式
        plt.plot(importance)
        plt.savefig(saveFolderName + "/importance_{}.png".format(i))

        topPercent = 2  #前 2% 的重要区域 topRois  取出前2%的重要roi的索引(400×2%=8)

        topRois = np.nonzero(importance>np.percentile(importance,100-topPercent))[0] #计算重要性值中排在前 98% 的阈值,获取大于这一阈值的重要性值所对应的索引  8个值

        # first save for female, ladies first i guess
        os.makedirs(saveFolderName, exist_ok=True)
        for j, roi in enumerate(topRois):
            volume = np.zeros_like(roiMap_array) #创建一个与 roiMap_array 相同形状的全零数组 volume [182,218,182]
            impact = importance[roi]  #获取当前区域的重要性值 impact
            volume[roiMap_array==(roi+1)] = 1 # constant coloring of all important rois  #将 volume 中对应当前区域的数值设为 1，以便将所有重要的区域标记出来,将该ROI区域设置为1
            savePrepend = "class_{}_roi_{}_top_{}.nii.gz".format(i, roi+1, len(importance) - sorted(importance.tolist()).index(impact)) #保存为哪个import的哪个roi的第几重要的ROI
            nil.image.new_img_like(roiMap, volume, roiMap.affine).to_filename(saveFolderName + "/" + savePrepend)
            

def generateImportanceFromCoefs(coefs):
    
    importances = []
    
    if(coefs.shape[0] == 1): # binary classification  检查系数 coefs 的形状是否为 (1, n)，即是否为二元分类模型
        coef = coefs[0]  #获取二元分类模型中的系数,取值[-1,1]
        logOdds = np.exp(coef)  #计算系数的指数函数，得到对数几率（log odds）

        importance_0 = 1-logOdds
        importance_1 = logOdds-1

        importances.append(importance_0)
        importances.append(importance_1)

    else:

        for coef in coefs: #多分类只计算对数-1
            logOdds = np.exp(coef)
            importance = logOdds-1

            importances.append(importance)

    return importances

def brainRegressor(dataset, seed, startK):


    targetDataset = dataset


    foldCount = 5
    if(targetDataset == "abide1"):
        foldCount = 10

    targetFolds = range(foldCount)

    relevancyScores = []

    allImportances = []

    train_accuracies_static_subjectWise = []
    test_accuracies_static_subjectWise = []

    train_accuracies_random_subjectWise = []
    test_accuracies_random_subjectWise = []

    train_accuracies_point_subjectWise = []
    test_accuracies_point_subjectWise = []

    train_accuracies_static_tokenWise = []
    test_accuracies_static_tokenWise = []

    train_accuracies_random_tokenWise = []
    test_accuracies_random_tokenWise = []

    train_accuracies_point_tokenWise = []
    test_accuracies_point_tokenWise = []


    for targetFold in targetFolds:

        saveFolder_train = "./Analysis/DataExtracted/{}/seed_{}/{}/TRAIN/startK_{}".format(targetDataset, seed, targetFold, startK)
        saveFolder_test = "./Analysis/DataExtracted/{}/seed_{}/{}/TEST/startK_{}".format(targetDataset, seed, targetFold, startK)
        saveFolder_results = "./Analysis/DataExtracted/{}/seed_{}/{}/RESULTS/startK_{}".format(targetDataset, seed, targetFold, startK) 

        os.makedirs(saveFolder_train, exist_ok=True)
        os.makedirs(saveFolder_test, exist_ok=True)
        os.makedirs(saveFolder_results, exist_ok=True)

        # 读入训练集，测试集和label 受试者名，x的系数
        train_static_subjIds = np.load(saveFolder_train + "/train_static_subjIds.npy")  #Train（707*5=3535）个数据
        test_static_subjIds = np.load(saveFolder_test + "/test_static_subjIds.npy")  #test（79*5=395）个数据

        train_random_subjIds = np.load(saveFolder_train + "/train_random_subjIds.npy")
        test_random_subjIds = np.load(saveFolder_test + "/test_random_subjIds.npy")



        x_train_static = np.array(np.load(saveFolder_train + "/x_train_static.npy"))
        x_train_static_relevancyScore = np.array(np.load(saveFolder_train + "/x_train_static_relevancyScore.npy"))
        
        x_train_random = np.array(np.load(saveFolder_train + "/x_train_random.npy"))
        x_train_random_relevancyScore = np.array(np.load(saveFolder_train + "/x_train_random_relevancyScore.npy"))


        y_train_static = np.array(np.load(saveFolder_train + "/y_train_static.npy"))
        y_train_random = np.array(np.load(saveFolder_train + "/y_train_random.npy"))    

        x_test_static = np.array(np.load(saveFolder_test + "/x_test_static.npy"))
        x_test_static_relevancyScore = np.array(np.load(saveFolder_test + "/x_test_static_relevancyScore.npy"))

        x_test_random = np.array(np.load(saveFolder_test + "/x_test_random.npy"))
        x_test_random_relevancyScore = np.array(np.load(saveFolder_test + "/x_test_random_relevancyScore.npy"))
    
        y_test_static = np.array(np.load(saveFolder_test + "/y_test_static.npy"))
        y_test_random = np.array(np.load(saveFolder_test + "/y_test_random.npy"))

        # FOR STATIC
        # • 计算随机的正确率，包括训练模型，得到token级别准确率，预测结果，得到预测后计算受试者级别的准确率
        clf_static = LogisticRegression().fit(x_train_static, y_train_static) #使用 Logistic 回归模型对X Y进行拟合，得到分类器
        static_train_acc_tokenWise = clf_static.score(x_train_static, y_train_static) #计算训练集上基于 token 的准确率   （5个时间点对应5个label，是分开的）
        static_test_acc_tokenWise = clf_static.score(x_test_static, y_test_static) #计算测试集上基于 token 的准确率
        
        y_predict_train_static = clf_static.predict(x_train_static)  #对训练集进行预测，得到预测结果
        y_predict_test_static = clf_static.predict(x_test_static)

        static_train_acc_subjectWise = getSubjectwiseAccuracy(y_predict_train_static, y_train_static, train_static_subjIds) #输入预测，label，受试者ID，受试者5个时间点token的众数与label比较，计算总的正确率
        static_test_acc_subjectWise = getSubjectwiseAccuracy(y_predict_test_static, y_test_static, test_static_subjIds)        

        print("Rel - Train accuracy token wise : {}, train accuracy subject wise : {}, Test accuracy token wise : {}, test accuracy subject wise : {}".format(static_train_acc_tokenWise, static_train_acc_subjectWise, static_test_acc_tokenWise, static_test_acc_subjectWise))
        train_accuracies_static_subjectWise.append(static_train_acc_subjectWise)
        test_accuracies_static_subjectWise.append(static_test_acc_subjectWise)
        train_accuracies_static_tokenWise.append(static_train_acc_tokenWise)
        test_accuracies_static_tokenWise.append(static_test_acc_tokenWise)
        # FOR RANDOM

        clf_random = LogisticRegression().fit(x_train_random, y_train_random)
        
        random_train_acc_tokenWise = clf_random.score(x_train_random, y_train_random)
        random_test_acc_tokenWise = clf_random.score(x_test_random, y_test_random)    

        y_predict_train_random = clf_random.predict(x_train_random)
        y_predict_test_random = clf_random.predict(x_test_random)

        random_train_acc_subjectWise = getSubjectwiseAccuracy(y_predict_train_random, y_train_random, train_random_subjIds)
        random_test_acc_subjectWise = getSubjectwiseAccuracy(y_predict_test_random, y_test_random, test_random_subjIds)

        print("Random - Train accuracy token wise : {}, train accuracy subject wise : {}, Test accuracy token wise : {}, test accuracy subject wise : {}".format(random_train_acc_tokenWise, random_train_acc_subjectWise, random_test_acc_tokenWise, random_test_acc_subjectWise))
        train_accuracies_random_subjectWise.append(random_train_acc_subjectWise)
        test_accuracies_random_subjectWise.append(random_test_acc_subjectWise)
        train_accuracies_random_tokenWise.append(random_train_acc_tokenWise)
        test_accuracies_random_tokenWise.append(random_test_acc_tokenWise)


        coefs = clf_static.coef_ #[1，400]（二分类），从名为 clf_static 统计的分类器模型中获取系数（coefficients）的值，通过查看 coefs 变量，可以了解模型中各个特征的重要性

        importances = generateImportanceFromCoefs(coefs) #[2,400]

        allImportances.append(importances)

        relevancyScores.append(np.mean(x_test_static_relevancyScore))

        # plot and save the importance values
        saveImportanceResults(importances, saveFolder_results)

    # find best rois average across all folds now  在所有fold中做平均找到最佳的ROI
    if(len(allImportances) > 1): #不止一个fold

        resultMessage = "\n STATIC RESULTS \n \n"
        for i in range(len(train_accuracies_static_subjectWise)): #几个fold，train_accuracies_static_subjectWise一个fold有一个值
            resultMessage += "STATIC SUBJECTWISE - Fold : {}, train acc : {}, test acc : {}\n".format(i, train_accuracies_static_subjectWise[i], test_accuracies_static_subjectWise[i])
        resultMessage += "\n STATIC SUBJECTWISE - Total, train acc : {} +- {}, test acc : {} +- {} \n \n".format(np.mean(train_accuracies_static_subjectWise), np.std(train_accuracies_static_subjectWise), np.mean(test_accuracies_static_subjectWise), np.std(test_accuracies_static_subjectWise))
        for i in range(len(train_accuracies_static_tokenWise)):
            resultMessage += "STATIC TOKENWISE - Fold : {}, train acc : {}, test acc : {}\n".format(i, train_accuracies_static_tokenWise[i], test_accuracies_static_tokenWise[i])
        resultMessage += "\n STATIC TOKENWISE - Total, train acc : {} +- {}, test acc : {} +- {} \n \n".format(np.mean(train_accuracies_static_tokenWise), np.std(train_accuracies_static_tokenWise), np.mean(test_accuracies_static_tokenWise), np.std(test_accuracies_static_tokenWise))



        resultMessage += "\n \n \n RANDOM RESULTS \n \n"
        for i in range(len(test_accuracies_random_subjectWise)):
            resultMessage += "RANDOM SUBJECTWISE - Fold : {}, train acc : {}, test acc :  {}\n".format(i, train_accuracies_random_subjectWise[i], test_accuracies_random_subjectWise[i])
        resultMessage += "\n RANDOM SUBJECTWISE - Total, train acc : {} +- {}, test acc : {} +- {} \n \n".format(np.mean(train_accuracies_random_subjectWise), np.std(train_accuracies_random_subjectWise), np.mean(test_accuracies_random_subjectWise), np.std(test_accuracies_random_subjectWise))
        for i in range(len(test_accuracies_random_tokenWise)):
            resultMessage += "RANDOM TOKENWISE - Fold : {}, train acc : {}, test acc :  {}\n".format(i, train_accuracies_random_tokenWise[i], test_accuracies_random_tokenWise[i])
        resultMessage += "\n RANDOM TOKENWISE - Total, train acc : {} +- {}, test acc : {} +- {}".format(np.mean(train_accuracies_random_tokenWise), np.std(train_accuracies_random_tokenWise), np.mean(test_accuracies_random_tokenWise), np.std(test_accuracies_random_tokenWise))
        
        
        saveFolder_results = "./Analysis/DataExtracted/{}/seed_{}/RESULTS/startK_{}".format(targetDataset, seed, startK) 

        # make sure to delete previous results
        shutil.rmtree(saveFolder_results, ignore_errors=True)

        os.makedirs(saveFolder_results, exist_ok=True)

        resultFile = open(saveFolder_results + "/results.txt", 'w') #将正确率信息保存
        resultFile.write(resultMessage)
        resultFile.close()

        allImportances = np.array(allImportances).mean(axis=0) #• 对全部的重要性在fold下求平均，保存平均重要性结果

        averageRelevancies = np.array(relevancyScores)

        saveImportanceResults(allImportances, saveFolder_results)


    return test_accuracies_static_subjectWise, averageRelevancies, allImportances #test_accuracies_static_subjectWise：[10,1],averageRelevancies:[10,1],allImportances:[2,400]
