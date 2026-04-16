import os
import nilearn as nil
import nilearn.datasets
import nilearn.image
import pandas
import torch
from glob import glob
from tqdm import tqdm
from joblib import Parallel, delayed
from nilearn.input_data import NiftiLabelsMasker

from .prep_atlas import prep_atlas

datadir = "./Dataset/Data"

def process_file(scanImage_fileName, atlasImage, phenoInfos):
    if ".gz" in scanImage_fileName:
        scanImage = nil.image.load_img(scanImage_fileName)
        roiTimeseries = NiftiLabelsMasker(atlasImage).fit_transform(scanImage)
        subjectId = scanImage_fileName.split("_")[-3][2:]
        return {
            "roiTimeseries": roiTimeseries,
            "pheno": {
                "subjectId": subjectId, **phenoInfos[subjectId]
            }
        }
    else:
        return None

def prep_abide(atlas):

    # bulkDataDir = "{}/Bulk/ABIDE".format(datadir)
    bulkDataDir = "/DATA2024/zmy/BolT-main_2023/Dataset/Data/Bulk/ABIDE"
    atlasImage = prep_atlas(atlas)

    if not os.path.exists(bulkDataDir):
        nil.datasets.fetch_abide_pcp(data_dir=bulkDataDir, pipeline="cpac", band_pass_filtering=False, global_signal_regression=False, derivatives="func_preproc", quality_checked=True)

    dataset = []

    temp = pandas.read_csv(bulkDataDir + "/ABIDE_pcp/Phenotypic_V1_0b_preprocessed1.csv").to_numpy()
    phenoInfos = {}
    for row in temp:
        phenoInfos[str(row[2])] = {"site": row[5], "age" : row[9], "disease" : row[7], "disease_class" : row[8], "gender" : row[10]}

    print("\n\nExtracting ROIS...\n\n")

    # 使用 Parallel 并行处理文件
    results = Parallel(n_jobs=-1)(delayed(process_file)(scanImage_fileName, atlasImage, phenoInfos) for scanImage_fileName in tqdm(glob("G:/BolT-main/Dataset/Data/Bulk/ABIDE/"+"/ABIDE_pcp/cpac/nofilt_noglobal/*"), ncols=60) if ".gz" in scanImage_fileName)

    # 过滤掉返回值为 None 的结果并添加到数据集中
    for result in results:
        if result is not None:
            dataset.append(result)

    # 将数据集保存到本地。
    torch.save(dataset, datadir + "/dataset_abide_5class_{}.save".format(atlas) )

# 提取出roi
