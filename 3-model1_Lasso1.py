#coding:utf-8

import datetime
import requests
import os
import re
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import tree
from stacking import two_stage_stacking

####提取时间特征(day_info包括了test_day14天)
days_info = pd.read_csv('days_info.txt', header=None, index_col=False,names=['weekdays','holiday'])
days_info = pd.concat([pd.get_dummies(days_info['weekdays']), pd.get_dummies(days_info['holiday'])],axis=1)

pay_count = pd.read_csv('shop_pay_count.csv')

####模型出答案
weeks_before = 3
answer = np.zeros([2000,15])
for shop_id in range(1,2001):
    print shop_id

    shop_pay = np.asarray(pay_count[str(shop_id)])

    # 对数据中的0值用去零周均值填充.若存在周均值仍为0，则用全数据周均值填充
    all_weekly_DF = pd.DataFrame(shop_pay[6:].reshape(-1, 7))
    non_zeros_all_weekly_DF = all_weekly_DF[all_weekly_DF > 0]
    all_weekly_mean = non_zeros_all_weekly_DF.mean()
    filled_shop_pay = non_zeros_all_weekly_DF.fillna(all_weekly_mean).values.reshape(1, -1)[0].tolist()

    weekly_DF = all_weekly_DF[-weeks_before:]  # 取前三星期的数据提取特征
    weekly_DF = weekly_DF[weekly_DF > 0]
    weekly_DF = weekly_DF.fillna(weekly_DF.mean()).fillna(all_weekly_mean)

    train_Y = weekly_DF.values.reshape(1, -1)[0]
    train_X = days_info[-(weeks_before * 7 + 14):-14].values
    test_X = days_info[-14:].values

    model = linear_model.Lasso(alpha=1)  # baseline
    model.fit(train_X, train_Y)
    pred = np.round(model.predict(test_X))

    answer[shop_id - 1, 0] = shop_id
    answer[shop_id - 1, 1:] = pred

final_pred =  pd.DataFrame(answer, dtype=int)
final_pred.to_csv('3WeekDayLasso1_pred.csv', header=None, index=False)