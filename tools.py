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
    plt.figure(shop_id)
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


'''对数据进行多项式拟合，使缺失值填充尽可能平滑'''
def poly_fit(shop_count, n):
    x = np.linspace(0,1,len(shop_count))
    cof = np.polyfit(x,shop_count,n)
    p = np.poly1d(cof)
    return p(x)


'''进出都是array()
'''
def clean_data(shop_count):
    shop_count = np.asarray(shop_count)
    shop_pay_count = shop_count
    shop_weekly_pay_count = pd.DataFrame(shop_pay_count[6:].reshape(-1, 7))
    all_week_mean = shop_weekly_pay_count[shop_weekly_pay_count>0].dropna()[-3:].mean()#周均值
    shop_weekly_pay_count = shop_weekly_pay_count[shop_weekly_pay_count>0].fillna(all_week_mean)#用均值填充
    shop_weekly_pay_count = shop_weekly_pay_count.values.reshape(1, -1)[0]
    shop_pay_count[6:] = shop_weekly_pay_count
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

def judge_trend(shop_count):
    shop_weekly_count = pd.DataFrame(shop_count[6:].values.reshape(-1, 7))
    train_weekly_count = shop_weekly_count[-3:]
    mean = train_weekly_count.mean(axis=1).values
    # print mean
    if mean[-1] > mean[-2] and mean[-2] > mean[-3]:
        percent = ((mean[-1]-mean[-2])/mean[-2] + (mean[-2]-mean[-3])/mean[-3])/2
        return 'accend', percent
    if mean[-1] < mean[-2] and mean[-2] < mean[-3]:
        percent = ((mean[-1]-mean[-2])/mean[-2] + (mean[-2]-mean[-3])/mean[-3])/2
        return 'deccent', percent
    else:
        return None

def judge_normal(shop_count):
    shop_weekly_count = pd.DataFrame(shop_count[6:].values.reshape(-1, 7))
    train_weekly_count = shop_weekly_count[-6:]
    mean = train_weekly_count.mean(axis=1)
    return (mean>30).all()

