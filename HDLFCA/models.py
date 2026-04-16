#!/usr/bin/python
# -*- coding:utf8 -*-

import keras
from keras.models import Sequential
from keras import regularizers
from keras.layers import Dense, Activation, Dropout,Lambda, Concatenate,Input
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.utils import np_utils
from keras.initializers import he_normal
from keras.models import load_model
import os
from keras.layers.recurrent import GRU
from keras import backend as K
from keras.regularizers import l1_l2
from keras.models import Model
from keras.layers.convolutional import Conv1D,MaxPooling1D,Conv2D
from keras.layers import  Reshape,multiply,Permute

def attach_attention_module(net):
    net_transpose = Permute((2,3,1))(net)  #（50,170,1）
    print(net_transpose.shape)
    avg_pool = Lambda(lambda x:K.mean(x,axis=3,keepdims=True))(net_transpose)#最后一维平均池化
    assert avg_pool._keras_shape[-1] == 1 #最后一维平均池化后应该为1，检查是否为1
    max_pool = Lambda(lambda x: K.max(x, axis=3, keepdims=True))(net_transpose)#最后一维最大池化
    assert max_pool._keras_shape[-1] == 1
    concat = Concatenate(axis=3)([avg_pool, max_pool]) #第三个维度上进行拼接
    assert concat._keras_shape[-1] == 2
    #filters=50: the number of ICs(brain regions)
    feature = Conv2D(filters=50, kernel_size=(50, 1),  activation='sigmoid',
                                       kernel_initializer='he_normal', use_bias=False)(concat)
    feature_map = Permute((1, 3, 2))(feature)
    #[1,170, 1, 1]:170 is the time points
    feature = Lambda(lambda x: K.tile(x, [1,170, 1, 1]))(feature_map)  #复制50次
    return multiply([net,feature]), feature_map

def cnn_attention_2(Config,X_train,y_train,X_test,k=None,train_fold = None):
    y_train = np_utils.to_categorical(y_train, 2)
    seq_length = 170
    features_length = 50
    batch_size = 64
    nb_epoch = 1000

    input_shape = (seq_length, features_length)
    input_layer = Input(shape= input_shape)  #输入层
    reshape_1 = Reshape((seq_length, features_length, 1))(input_layer)  #（170,50,1）
    attention_layer,attention_map = attach_attention_module(reshape_1)
    reshape_2 = Reshape((seq_length, features_length))(attention_layer)
    conv_1_1 = Conv1D(32, 2, activation='relu', padding='same')(reshape_2)
    conv_1_2 = Conv1D(16, 4, activation='relu', padding='same')(reshape_2)
    conv_1_3 = Conv1D(16, 8, activation='relu', padding='same')(reshape_2)

    concat_1 = Concatenate()([conv_1_1, conv_1_2, conv_1_3])
    max_pool_1 = MaxPooling1D(3)(concat_1)
    gru_layer_1 = GRU(32, return_sequences=True, dropout=0.3,
                      kernel_regularizer=l1_l2(0.0001, 0.0001),
                      recurrent_regularizer=l1_l2(0.0001, 0.0001)
                      )(max_pool_1)
    gru_concat = Concatenate()([max_pool_1, gru_layer_1])
    gru_layer = GRU(32, return_sequences=True, dropout=0.3,
                    kernel_regularizer=l1_l2(0.0001, 0.0001),
                    recurrent_regularizer=l1_l2(0.0001, 0.0001)
                    )(gru_concat)
    last_step_layer = Lambda(lambda x: K.mean(x[:, 10:, :], axis=1))(
        gru_layer)
    print('====== Averaged state =========')
    dense_last_step = Dense(32)(last_step_layer)
    drop_last_step = Dropout(0.5)(dense_last_step)
    output_layer = Dense(2, activation='softmax')(drop_last_step)
    model = Model(input=input_layer, output=output_layer)
    model.compile(
        optimizer=Adam(lr=0.001,decay=1e-2),
        loss='categorical_crossentropy',
        metrics=['accuracy'], )
    model.summary()

    model_save_path = os.path.join(Config.model_path, 'crnnam_fold_' + str(k + 1) + '_' + str(train_fold) + '.hdf5')
    checkpoint = ModelCheckpoint(
        model_save_path,
        verbose=1,
        save_best_only=True,
        save_weights_only=False,
    )
    early_stopping = EarlyStopping(patience=50)
    model.fit(X_train,y_train,batch_size=batch_size,validation_split=0.1,
        verbose=1,callbacks=[checkpoint, early_stopping],epochs=nb_epoch)


    model_save = load_model(model_save_path)
    y_submission = model_save.predict(X_test)
    prediction = y_submission[:, 1]
    return prediction, model, attention_map



def dnn_model(Config,X_train,y_train,X_test,k=None,train_fold = None):

    batch_size = 64
    epochs = 200
    size = 1225
    y_train = np_utils.to_categorical(y_train, 2) #用于分类，将标签转为one-hot编码。label转换为0,1

    model = Sequential([
        Dense(32, input_dim=size, kernel_regularizer=regularizers.l2(0.001),   #输出维数，输入维数（第一层才要），全连接层在keras中叫dence
              kernel_initializer=keras.initializers.he_normal(seed=None)),  #He 正态分布初始化器。
        Activation('relu'),
        # Dense(16, kernel_regularizer=regularizers.l2(0.1), kernel_initializer=he_normal(seed=None)),
        Dense(16, kernel_regularizer=regularizers.l2(0.1), kernel_initializer=keras.initializers.he_normal(seed=None)),
        Activation('relu'),
        Dropout(0.5),
        Dense(2),
        Activation('softmax'), ])

    model.compile(
        optimizer=Adam(lr=0.001),#优化函数，梯度下降（求导）
        loss='categorical_crossentropy',#分类模型损失函数，后面一般加激活函数softmax（给出概率分布）可以做多分类
        metrics=['accuracy'], ) #指标，准确性
    model.summary() #用summary方法可以查看模型内部的参数
    model_save_path = os.path.join(Config.model_path,'dnn_fold_' + str(k + 1) + '_'+str(train_fold)+ '.hdf5')
    checkpoint = ModelCheckpoint(
        model_save_path,
        verbose=1,
        save_best_only=True,
        save_weights_only=False,
        period=1
    )
    earlystopping = EarlyStopping(monitor='val_acc', patience=50, verbose=0, mode='auto') #验证集准确率50个epoch没有提升，停止  防止过拟合
    model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1,callbacks=[checkpoint,earlystopping]) #训练模型
    model_save = load_model(model_save_path)  #读入训练结束保存的模型，加载验证集上性能最好的模型，也就是最后一个保存的模型
    y_submission = model_save.predict(X_test)
    prediction = y_submission[:,1]  #二分类，每一个分类都有一个概率。对二分类，取第一个概率就够了
    return prediction, model   #返回的模型不是加载进来的模型，但性能是差不多的


import joblib
from sklearn.linear_model import LogisticRegression
def LR_model(Config,X_train,y_train,X_test):   #逻辑回归
    model = LogisticRegression()
    model.fit(X_train, y_train)
    model_save_path = os.path.join(Config.model_path, "LR")
    joblib.dump(model, model_save_path)
    model = joblib.load(model_save_path)
    pro = model.predict_proba(X_test)[:, 1]
    prediction = model.predict(X_test)
    return pro, prediction, model
