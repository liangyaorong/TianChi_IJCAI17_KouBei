#coding:utf-8
import numpy as np
import datetime
import pandas as pd
import requests

#获取时间列表
def get_date_list(start, end, toFormat):
    date_list = []
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    while date <= end:
        date_list.append(date.strftime(toFormat))
        date = date + datetime.timedelta(1)
    return date_list

def get_index(all_list, to_get_list):
    index = []
    for i in to_get_list:
        index.append(all_list.index(i))
    return index

## api获取假期特征
def isHoliday(date):
    return requests.get('http://www.easybots.cn/api/holiday.php?d=%s'%date).content

def get_shop_city_name_list():
    title = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt',
             'shop_level', 'category_1', 'category_2', 'category_3']
    shop_info = pd.read_csv('shop_info.txt', header=None, names=title)
    return shop_info['city_name'].values

def get_lag_feature(all_label, train_begin_index=-21, lag=1):
    all_label = np.array(all_label)
    return all_label[(train_begin_index-lag):-1*lag]

def get_n_days_before_mean_feature(all_label, day_index=-1, n = 3):
    all_label = np.array(all_label)
    return all_label[(day_index-n):day_index].mean()



