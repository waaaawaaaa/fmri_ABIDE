import sklearn
from sklearn.svm import SVC
import numpy as np



class Model():

    def __init__(self, hyperParams):

        self.hyperParams = hyperParams
        
        self.model = SVC(C=hyperParams.C, probability=True)  #模型使用了SVC类，它是Scikit-learn库中实现的支持向量分类器。C是正则化参数，控制模型的复杂度,probability是一个布尔值，表示是否启用概率估计。如果设置为True，模型会启用概率估计

    def flattenFCs(self, FCs):  #功能连接（FC）矩阵展平为一维数组

        triuIndices = np.triu_indices(FCs.shape[1], k=1)  #triu_indices函数获取矩阵的上三角部分的索引。行索引和列索引 200*399=79800
        FCs = FCs[:, triuIndices[0], triuIndices[1]]

        return FCs

    def fit(self, FCs, labels):
        
        """
            FCs : (#ofTrains, N, N)
            labels : (#ofTrains)
        """

        # flatten the FCs
        FCs = self.flattenFCs(FCs)
        self.model.fit(FCs, labels)  

    def predict(self, FCs):#返回预测的类别标签
        
        FCs = self.flattenFCs(FCs)
        return self.model.predict(FCs)
      
    def predict_proba(self, FCs):#返回每个类别的概率估计值

        FCs = self.flattenFCs(FCs)
        return self.model.predict_proba(FCs)


