#!/usr/bin/python
# -*- coding:utf8 -*-
from fuction_utility import *
from models import dnn_model,cnn_attention_2,LR_model
from sklearn.model_selection import StratifiedKFold
from args import *

#set gpu
import tensorflow as tf
import os
from keras.backend.tensorflow_backend import set_session
os.environ["CUDA_VISIBLE_DEVICES"] = '1'
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
set_session(tf.Session(config=config))

def HDLFCA(Config):
    #load data  数据 label  fold有10个list，每个里面都是9:1
    folds, X_train, y_train = load_data_kfold(k = 10,datatype='sfc',path = Config.sfc_path,random_state=Config.random_state)
    fold, X_train_tc, y_train_tc = load_data_kfold(k = 10,datatype='tc',path = Config.tc_path,random_state=Config.random_state)

    #y:true label; prediction: predicted label; y_sore: probability to compute auc
    y = np.array([1]).reshape(-1, 1)
    prediction = np.array([1]).reshape(-1, 1)
    y_score = np.array([1]).reshape(-1, 1)

    #10-fold
    for k, (train_idx, val_idx) in enumerate(folds):
        print('Fold', k + 1)
        #training data
        X_train_cv = X_train[train_idx]#(990,1225)
        y_train_cv = y_train[train_idx]   #label
        X_train_cv_tc = X_train_tc[train_idx]#(990,170,50)
        #testing data
        X_test_cv = X_train[val_idx]#(110,1225)
        y_test_cv = y_train[val_idx]
        X_test_cv_tc = X_train_tc[val_idx]#(110,170,50)

        y = np.hstack((y, y_test_cv.T))#true label to evaluated  相当于在label前面＋了个1

        #training data was divided into three folds further in the training stage,
        # where two folds were used for training and validation,
        # and the remaining one was used for prediction, to avoid overfitting避免过拟合(section 2.6 in paper)
        clfs = ['dnn_model','rnn_model']
        dataset_blend_train = np.zeros((X_train_cv.shape[0], len(clfs)))#(990,2)   混合训练集
        dataset_blend_test = np.zeros((X_test_cv.shape[0], len(clfs)))#(110,2)
        n_folds = 3
        skf = list(StratifiedKFold(n_splits=n_folds, random_state=127).split(X_train_cv, y_train_cv))#分层抽样为2:1，三次

        for j, clf in enumerate(clfs):
            dataset_blend_test_j = np.zeros((X_test_cv.shape[0], len(skf)))#(110,3)
            for i, (train, test) in enumerate(skf):
                #xx_train:(660,1225);xx_test:(330,1225)
                xx_train, yy_train, xx_test, yy_test = X_train_cv[train], y_train_cv[train], X_train_cv[test], y_train_cv[test]
                #xx_train_tc:(660,170,50);xx_test_tc:(330,170,50)
                xx_train_tc, xx_test_tc = X_train_cv_tc[train], X_train_cv_tc[test]
                if j==0:
                    #dnn training and give the predict on the other fold(3-fold)
                    #y_submission:(330,)
                    y_submission,model = dnn_model(Config,xx_train,yy_train,xx_test,k=k,train_fold = i)
                elif j==1:
                    # crnnam training and give the predict on the other fold(3-fold)
                    # y_submission:(330,)
                    y_submission, model, map = cnn_attention_2(Config,xx_train_tc, yy_train, xx_test_tc,  k = k, train_fold = i)
                dataset_blend_train[test, j] = y_submission  #3-fold里面的测试  990全算完了 有FNC和TC
                if j == 1:
                    # crnnam give the predict on testing data(10-fold)
                    dataset_blend_test_j[:, i], map_test = model.predict(X_test_cv_tc)[:, 1]
                else:
                    # dnn give the predict on testing data(10-fold)
                    dataset_blend_test_j[:, i] = model.predict_proba(X_test_cv)[:, 1]
            #in the testing stage, the outputs of three DNN models and three C-RNN models were first averaged respectively
            dataset_blend_test[:, j] = dataset_blend_test_j.mean(1)

        pro, y_submission, model = LR_model(Config,dataset_blend_train,y_train_cv,dataset_blend_test)
        #dataset_blend_train（990,2（fnc,tc））,y_train_cv:labeldataset_blend_test:（330,2（fnc,tc））
        prediction = np.hstack((prediction, y_submission.reshape(1, -1))) #水平拼接 10-fold  1101，因为最开头给了个1
        y_score = np.hstack((y_score, pro.reshape(1, -1)))
    prediction = prediction[:, 1:] #1100个   1or0
    y_score = y_score[:, 1:]  #属于0的概率
    y = y[:, 1:]   #label
    #evaluation
    acc, spe, sen, f1, roc_auc= acc_pre_recall_f(y.T, prediction.T, y_score.T)
    print(acc, spe, sen, f1, roc_auc)




if __name__ == '__main__':
   Config = args
   Config.sfc_path = 'data/tz_sfc.mat'#(1100,1225)558+542  （受试者数，FC）
   Config.tc_path = 'data/tz_tc_norm.mat'#(1100,170,50)  np.corrcoef  （受试者数，volumes，ICs）
   Config.alg = 'HDLFCA'
   Config.random_state = 10
   Config.workspace = os.path.join('workspace', Config.alg)
   Config.model_path = os.path.join(Config.workspace, 'models')
   Config.result_path = os.path.join(Config.workspace, 'result')
   os.makedirs(Config.model_path, exist_ok=True)
   os.makedirs(Config.result_path, exist_ok=True)
   HDLFCA(Config)

