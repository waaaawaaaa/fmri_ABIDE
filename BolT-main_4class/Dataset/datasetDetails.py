
datasetDetailsDict = {

    "hcpRest" : {
        "datasetName" : "hcpRest",
        "targetTask" : "gender",
        "taskType" : "classification",
        "nOfClasses" : 2,   #性别检测
        "dynamicLength" : 600,
        "foldCount" : 5,
        "atlas" : "schaefer7_400",
        "nOfEpochs" : 20,
        "batchSize" : 32       
    },

    "hcpTask" : {
        "datasetName" : "hcpTask",
        "targetTask" : "taskClassification",
        "nOfClasses" : 7,   #任务检测
        "dynamicLength" : 150,
        "foldCount" : 5,
        "atlas" : "schaefer7_400",
        "nOfEpochs" : 20,
        "batchSize" : 16
    },

    "abide1" : {
        "datasetName" : "abide1",
        "targetTask" : "disease",
        "nOfClasses" : 4,   #2分类，疾病检测
        "dynamicLength" : 60,
        "foldCount" : 10,
        # "atlas" : "schaefer7_400",
        "atlas" : "AAL_116",
        "nOfEpochs" : 20,
        "batchSize" : 32        
    },

 }



