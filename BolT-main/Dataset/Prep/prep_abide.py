import os

import nilearn as nil
import nilearn.datasets
import nilearn.image
from glob import glob
import pandas
import torch
from tqdm import tqdm

from .prep_atlas import prep_atlas
from nilearn.input_data import NiftiLabelsMasker


datadir = "./Dataset/Data"


def prep_abide(atlas):

    bulkDataDir = "{}/Bulk/ABIDE".format(datadir)    #定义了从网站下载的原始数据所在的目录。

    atlasImage = prep_atlas(atlas)  #返回指定解剖学模板的MRI图像。



    if(not os.path.exists(bulkDataDir)):   #判断原始数据是否已经下载，如果没有则执行下载命令。
        nil.datasets.fetch_abide_pcp(data_dir=bulkDataDir, pipeline="cpac", band_pass_filtering=False, global_signal_regression=False, derivatives="func_preproc", quality_checked=True)

    # 如果没有数据就下载

    dataset = []

    # 读取原始数据中的表格文件，记录每个被试的基本信息。
    temp = pandas.read_csv(bulkDataDir + "/ABIDE_pcp/Phenotypic_V1_0b_preprocessed1.csv").to_numpy()
    phenoInfos = {}
    for row in temp:
        phenoInfos[str(row[2])] = {"site": row[5], "age" : row[9], "disease" : row[7], "gender" : row[10]}

    print("\n\nExtracting ROIS...\n\n")

    for scanImage_fileName in tqdm(glob(bulkDataDir+"/ABIDE_pcp/cpac/nofilt_noglobal/*"), ncols=60):
        # 遍历原始数据中每个被试的MRI图像。
        
        if(".gz" in scanImage_fileName):#判断该文件是否为MRI图像，如果是则进行下一步处理。

            scanImage = nil.image.load_img(scanImage_fileName)#读取MRI图像。
            roiTimeseries =  NiftiLabelsMasker(atlasImage).fit_transform(scanImage)
            # 利用指定的解剖学模板，提取出该被试的每个感兴趣区域（ROI）的时间序列。

            subjectId = scanImage_fileName.split("_")[-3][2:] #从文件名中提取出该被试的编号。
            # 将该被试的ROI时间序列以及基本信息添加到数据集列表中。
            dataset.append({
                "roiTimeseries": roiTimeseries,
                "pheno": {
                    "subjectId" : subjectId, **phenoInfos[subjectId]
                }
            })
    # 将数据集保存到本地。
    torch.save(dataset, datadir + "/dataset_abide_{}.save".format(atlas) )
# 提取出roi
    
