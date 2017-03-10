#coding:utf-8

from scipy import sparse


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.feature_selection import SelectKBest,chi2,f_classif,mutual_info_classif
from tools import *
from stacking import two_stage_stacking
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, scale


if __name__ == '__main__':

    ##线下测试
    train_label = pd.read_csv('train_label.csv', index_col=False, header=None).values
    print train_label.shape
    train_data = pd.read_csv('train_feature.csv', index_col=False).values
    print train_data.shape



    pca = PCA(n_components=100, random_state=1)
    pca_X = pca.fit_transform(train_data)
    scaler = MinMaxScaler()
    scaled_pca_X = scaler.fit_transform(pca_X)
    train_data = np.concatenate([train_data, scaled_pca_X], axis=1)
    print train_data.shape
    # train_data = scale(train_data)

    train_X = train_data[-7*2000:]
    train_Y = train_label[-7*2000:]
    test_X = train_data[:-7*2000]
    test_Y = train_label[:-7*2000]

    # selector = SelectKBest(chi2, k=200)
    # train_X = selector.fit_transform(train_X, train_Y)
    # test_X = selector.transform(test_X)


    model1 = ExtraTreesRegressor(n_estimators=300, random_state=1, n_jobs=-1,
                                min_samples_split=3, min_samples_leaf=1, max_depth=100)

    model = model1
    model.fit(train_X, train_Y)
    # print model.feature_importances_
    pred = model.predict(test_X)
    pred = pd.DataFrame(pred.reshape(-1,2000).T)
    real = pd.DataFrame(test_Y.reshape(-1,2000).T)
    score = np.sum(np.sum(np.abs((np.round(pred)-real)/(np.round(pred)+real))))/(2000*14)
    print score



    # ####出答案
    # train_Y = pd.read_csv('train_label.csv', index_col=False, header=None).values
    # print train_Y.shape
    #
    # train_X = pd.read_csv('train_feature.csv', index_col=False).values
    # print train_X.shape
    #
    # test_X = pd.read_csv('test_feature.csv', index_col=False).values
    # print test_X.shape
    #
    # #models
    #
    # model1 = ExtraTreesRegressor(n_estimators=1000, random_state=1, n_jobs=-1,
    #                             min_samples_split=3, min_samples_leaf=1, max_depth=100)
    # model2 = ExtraTreesRegressor(n_estimators=200, random_state=1, n_jobs=-1,
    #                             min_samples_split=2, min_samples_leaf=5, max_depth=100)
    # model3 = ExtraTreesRegressor(n_estimators=200, random_state=1, n_jobs=-1,
    #                             min_samples_split=2, min_samples_leaf=10, max_depth=100)
    # # model3 = RandomForestRegressor(n_estimators=300, n_jobs = -1, random_state=0,
    # #                               min_samples_leaf=1,max_depth=100)
    # # model4 = RandomForestRegressor(n_estimators=300, n_jobs = -1, random_state=0,
    # #                               min_samples_leaf=1,max_depth=100)
    #
    # # base_models = [model1, model2]
    # # predict_model = model1
    # # stacking = two_stage_stacking(base_models=base_models, predict_model = predict_model, n_splits=3)
    # # stacking.fit(train_X, train_Y, test_X)
    # # pred = stacking.predict()
    #
    # model = model1
    # model.fit(train_X, train_Y)
    # pred = model.predict(test_X)
    #
    # pred = np.round(pred).reshape((-1,2000)).T
    # answer = np.zeros([2000, 15])
    # answer[:,0] = range(1,2001)
    # answer[:,1:] = pred
    # pd.DataFrame(answer, dtype=int).to_csv('new_preOneWeek2_n1000_pred.csv', header=None, index=False)
    #
    #
    #
