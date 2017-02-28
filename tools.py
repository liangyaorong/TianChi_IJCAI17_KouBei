#coding:utf-8
import numpy as np
import datetime
import pandas as pd
import requests
from matplotlib import pyplot as plt
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

def calculate_score(pred, real):
    pred = np.round(pred)
    return np.mean(np.abs((pred-real)/(pred+real)))

def plot_two_answers(old_pred_file_name, new_pred_file_name, shop_id):
    pay_count = pd.read_csv('shop_pay_count.csv')
    shop_pay = pay_count[str(shop_id)]

    new_pred = pd.read_csv(new_pred_file_name, header=None, index_col=False).ix[shop_id-1][1:]
    old_pred = pd.read_csv(old_pred_file_name, header=None, index_col=False).ix[shop_id-1][1:]

    new_all = np.concatenate([shop_pay,new_pred])
    old_all = np.concatenate([shop_pay,old_pred])
    plt.plot(range(len(new_all)),new_all,'--')
    plt.plot(range(len(old_all)),old_all,'green')
    plt.show()

def plot_shop_count(filename, shop_id, show=True):
    pay_count = pd.read_csv(filename)
    shop_pay = pay_count[str(shop_id)]
    shop_pay.index = get_date_list('2015-07-01','2016-10-31', '%Y-%m-%d')
    shop_pay.plot()
    if show==True:
        plt.show()


'''对某个商家数据进行异常值平滑并用上一周数据填充缺失值
进出都是array()
'''
def clean_data(shop_count, sigma):
    shop_count = np.asarray(shop_count)
    shop_pay_count = shop_count
    shop_weekly_pay_count = shop_pay_count[6:].reshape(-1, 7)
    index = range(64, 69)
    while index[0] != 0:
        now_weekly_pay_count = shop_weekly_pay_count[index, :]
        mean = now_weekly_pay_count.mean(axis=0)
        std = now_weekly_pay_count.std(axis=0)
        last_weekly_count = shop_weekly_pay_count[index[0] - 1, :]
        last_weekly_count[last_weekly_count <= 0] = shop_weekly_pay_count[index[0], :]\
            [last_weekly_count <= 0]#部分缺失值填充
        last_weekly_count[last_weekly_count - mean > sigma * std] = shop_weekly_pay_count[index[0], :]\
            [last_weekly_count - mean > sigma * std]#异常值平滑
        index = (np.asarray(index) - 1).tolist()
    shop_weekly_pay_count = pd.DataFrame(shop_weekly_pay_count)
    all_mean = shop_weekly_pay_count.mean()
    shop_weekly_pay_count = shop_weekly_pay_count[shop_weekly_pay_count>0].fillna(all_mean)
    shop_weekly_pay_count = shop_weekly_pay_count.values
    shop_pay_count[6:] = shop_weekly_pay_count.reshape(1, -1)
    return shop_pay_count

def cheak_answer_is_nonegative(ans_filename):
    pred_file_name = ans_filename
    new_pred = pd.read_csv(pred_file_name, header=None, index_col=False)
    print (new_pred > 0).all().all()

def judge_cycle(shop_count, corr_baseline):
    shop_weekly_count = pd.DataFrame(shop_count[6:].values.reshape(-1, 7))
    train_weekly_count = shop_weekly_count[-3:]
    week_corr =  train_weekly_count.T.corr()
    return (np.abs(week_corr)>corr_baseline).all().all()
