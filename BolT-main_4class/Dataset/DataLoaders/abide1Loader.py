import torch
import numpy as np
import os
import sys



datadir = "./Dataset/Data"


def healthCheckOnRoiSignal(roiSignal):
    """
        roiSignal : (N, T)
    """

    # 第一个维度 N 表示 ROI 的数量，第二个维度 T 表示每个 ROI 在时间上采样的数据点的数量
    # remove subjects with dead rois,有没有时间序列求和后为0的roi，有的话返回false
    if(np.sum(np.sum(np.abs(roiSignal), axis=1) == 0) > 0):
        return False

    return True    

def abide1Loader(atlas, targetTask):

    """
        x : (#subjects, N)
    """
#加载前面整理好的roi文件，save格式，871×roitimeseries,pheno{id,site,age,disease,gender}
    dataset = torch.load(datadir + "/dataset_abide_5class_{}.save".format(atlas))
    x = []
    y = []
    subjectIds = []

    for data in dataset:
        
        if(targetTask == "disease"):
            label = int(data["pheno"]["disease_class"]) # 0健康人，1 2 3 4患者

        if label != 4 and label != -9999:  # 忽略 disease_class 为 -9999 的受试者
            if(healthCheckOnRoiSignal(data["roiTimeseries"].T)):#有没有时间序列求和后为0的roi
                # AAL:799;schaefer:786
                x.append(data["roiTimeseries"].T)   #[400,196]roi,timepoint
                y.append(label)
                subjectIds.append(int(data["pheno"]["subjectId"]))

    # import scipy.io as sio #保存为mat文件，用于 HDLFCA
    # # 获取最长子数组的长度
    # max_length = max(len(sub_array) for sub_array in x)

    # # 将子数组填充至最长长度，并转换为NumPy数组
    # padded_x = np.array([sub_array + [0] * (max_length - len(sub_array)) for sub_array in x])
    #
    # AAL_116_799 = {'roiTimeseries': padded_x, 'label': y}
    # sio.savemat('F:\OneDrive - stu.xmu.edu.cn\capa_hdlfca\AAL_116_799.mat', AAL_116_799)

    return x, y, subjectIds
