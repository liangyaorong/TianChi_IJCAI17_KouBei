#coding:utf-8
import os
import re
import pandas as pd
import numpy as np
import datetime


def get_city_pinyin():
    city_name_dict = {}
    fr = open('city_pinyin')
    list = [i.strip().split(',') for i in fr.readlines()]
    fr.close()
    for i in list:
        city_name_dict[i[1]] = i[0]
    return city_name_dict

def get_weather_list():
    city_pinyin = get_city_pinyin()
    weather_list = []
    dir_list = os.listdir('weather')
    for dir in dir_list:
        fr = open('weather/%s'%dir)
        content = [i.strip().split(',') for i in fr.readlines()]
        for weather in content:
            day_weather = []
            day_weather.append(city_pinyin[dir])
            day_weather.extend(weather)
            weather_list.append(day_weather)
    return weather_list

def get_date_list(start, end, toFormat):
    date_list = []
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    while date <= end:
        date_list.append(date.strftime(toFormat))
        date = date + datetime.timedelta(1)
    return date_list

def judge_weather_good_or_not():
    fr = open('weather_good_or_not.txt')
    content = fr.readlines()
    fr.close()
    weather_good_or_not = []
    for i in content:
        i = i.strip()
        weather = []
        weather.append(i[0])
        weather.append(i[1])
        weather.append(i[2:])
        weather_good_or_not.append(weather)
    return pd.DataFrame(weather_good_or_not,columns=['early_weather','late_weather','weather'])

if __name__ == '__main__':

    df = pd.DataFrame(get_weather_list(),columns=['city','date','high','low','weather','wind','windlevel'],dtype=float)
    df = df[df['date'].isin(get_date_list('2015-07-01','2016-11-14','%Y-%m-%d'))]#截取需要的天气数据
    df['high2'] = np.power(df['high'],2)
    df['low2'] = np.power(df['low'],2)


    weather_good_or_not = judge_weather_good_or_not()
    df = df.join(weather_good_or_not.set_index('weather'), on='weather')

    df.drop(['wind'],axis=1,inplace=True)
    df.drop(['windlevel'],axis=1,inplace=True)
    df.drop(['weather'],axis=1,inplace=True)

    df = df.fillna(0)
    df.to_csv('weather_info.txt', header=None, index=False)


    # ##检查天气数据是否完整
    # title = ['shop_id','city_name','location_id','per_pay','score','comment_cnt',
    #          'shop_level','category_1','category_2','category_3']
    # shop_info = pd.read_csv('shop_info.txt', header=None, names=title)
    # city_list = shop_info['city_name'].values
    # day_list = get_date_list('2015-07-01','2016-10-31','%Y-%m-%d')
    # weather_info = pd.read_csv('weather_info.txt',header=None)
    # weather_info.fillna(0)
    # for city in set(city_list):
    #     try:
    #         print weather_info[(weather_info[0]==city)&(weather_info[1]=='2016-06-22')].values[0][2:]
    #     except:
    #         print city

