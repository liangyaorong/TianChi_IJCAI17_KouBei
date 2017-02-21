#coding:utf-8
import numpy as np
from scipy import sparse
from sklearn.model_selection import KFold

class two_stage_stacking(object):
    '''this is a two stage stacking'''
    def __init__(self, base_models, predict_model, n_splits = 5):
        self.n_splits = n_splits
        self.base_models = base_models#第一阶段模型
        self.predict_model = predict_model#第二阶段模型

    def fit(self, train_X, train_Y, test_X):
        self.train_Y = train_Y
        train_X = sparse.csr_matrix(train_X)
        test_X = sparse.csr_matrix(test_X)
        train_feature_row_num = train_X.shape[0]#原始训练集的第一层特征的行
        feature_col_num = len(self.base_models)#原始训练集的第一层特征的列
        test_feature_row_num = test_X.shape[0]#原始测试集的第一层特征的列
        self.train_feature = np.zeros((train_feature_row_num, feature_col_num))#原始训练集的第一层特征
        self.test_feature = np.zeros((test_feature_row_num, feature_col_num))#原始测试集的第一层特征

        kf = KFold(self.n_splits)
        # print 'fitting...'
        for i, model in enumerate(self.base_models):
            test_model_pred = np.zeros((test_feature_row_num, self.n_splits))
            for j, (train_index, test_index) in enumerate(kf.split(train_X)):
                train_XX = train_X[train_index] #K折后划分的训练特征集
                train_YY = train_Y[train_index] #K折后划分的训练目标集
                test_XX = train_X[test_index] #K折后划分的测试特征集

                model.fit(train_XX, train_YY)
                self.train_feature[test_index, i] = model.predict(test_XX.toarray())[:]
                test_model_pred[:,j] = model.predict(test_X.toarray())[:]
            self.test_feature[:,i] = test_model_pred.mean(1)
            # print 'model%s finished!'%i
        # print 'fitting finished!'

    def concat(self,train_concat_feature, test_concat_feature):
        self.train_feature = np.concatenate((self.train_feature, train_concat_feature), axis=1)
        self.test_feature = np.concatenate((self.test_feature, test_concat_feature), axis=1)

    def predict(self):
        # print 'predicting...'
        model = self.predict_model
        model.fit(self.train_feature, self.train_Y)
        pred = model.predict(self.test_feature)
        # print 'predict finished!'
        return pred