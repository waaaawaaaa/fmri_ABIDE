
import os 
import nilearn as nil
import nilearn.datasets

# nilearn库中的Schaefer 2018大脑功能区域分布图谱，并返回该分布图谱的图像

datadir = "./Dataset/Data"



def prep_atlas(atlas):

    if(atlas == "schaefer7_400"):
        if(not os.path.exists(datadir + "/Atlasses/{}".format(atlas))):  #判断指定的模板是否已经存在，如果不存在则执行下载命令。
            atlasInfo = nil.datasets.fetch_atlas_schaefer_2018(n_rois=400, yeo_networks=7, resolution_mm=1, data_dir=datadir + "/Atlasses")
            # 下载或加载名为"schaefer7_400"的解剖学模板。
            atlasImage = nil.image.load_img(atlasInfo["maps"])
    #         将解剖学模板的MRI图像加载到变量atlasImage中。

    elif atlas == "AAL_116":
        if not os.path.exists(datadir + "/Atlasses/{}".format(atlas)):
            atlasInfo = nil.datasets.fetch_atlas_aal(data_dir=datadir + "/Atlasses")
            atlasImage = nil.image.load_img(atlasInfo["maps"])  #maps用的是\atlas\AAL.nii

    return atlasImage


    