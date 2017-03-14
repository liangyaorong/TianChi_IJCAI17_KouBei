#coding:utf-8

from sklearn.ensemble import ExtraTreesRegressor
from tools import *

if __name__ == '__main__':

    # ##线下测试
    # train_label = pd.read_csv('train_label.csv', index_col=False, header=None).values
    # print train_label.shape
    # train_data = pd.read_csv('train_feature.csv', index_col=False).values
    # print train_data.shape
    #
    #
    # train_X = train_data[7*2000:]
    # train_Y = train_label[7*2000:]
    # test_X = train_data[:7*2000]
    # test_Y = train_label[:7*2000]
    #
    #
    # model1 = ExtraTreesRegressor(n_estimators=300, random_state=1, n_jobs=-1,
    #                             min_samples_split=3, min_samples_leaf=1, max_depth=100)
    #
    #
    # model = model1
    # model.fit(train_X, train_Y)
    # pred = model.predict(test_X)
    #
    #
    # pred = pd.DataFrame(pred.reshape(-1,2000).T)
    # real = pd.DataFrame(test_Y.reshape(-1,2000).T)
    # score = np.sum(np.sum(np.abs((np.round(pred)-real)/(np.round(pred)+real))))/(2000*7)
    # print score



    ####出答案
    train_Y = pd.read_csv('train_label.csv', index_col=False, header=None).values
    print train_Y.shape

    train_X = pd.read_csv('train_feature.csv', index_col=False).values
    print train_X.shape

    test_X = pd.read_csv('test_feature.csv', index_col=False).values
    print test_X.shape

    model = ExtraTreesRegressor(n_estimators=1000, random_state=1, n_jobs=-1,
                                min_samples_split=3, min_samples_leaf=1, max_depth=100)


    model.fit(train_X, train_Y)
    pred = model.predict(test_X)

    pred = np.round(pred).reshape((-1,2000)).T
    answer = np.zeros([2000, 15])
    answer[:,0] = range(1,2001)
    answer[:,1:] = pred
    pd.DataFrame(answer, dtype=int).to_csv('ExtRandomTree_n1000_pred.csv', header=None, index=False)