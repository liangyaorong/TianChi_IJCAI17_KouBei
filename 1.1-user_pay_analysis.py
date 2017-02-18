#coding:utf-8

'''统计 user_pay， 获取各商家支付数量的时间序列
'''

import datetime
import pandas as pd

##读取user_pay
def get_user_pay():
    fr = open('user_pay.txt')
    content = fr.readlines()
    fr.close()
    return content

def get_shop_id():
    return range(1,2001)

def get_date_list(start, end):
    date_list = []
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    while date <= end:
        date_list.append(date.strftime('%Y-%m-%d'))
        date = date + datetime.timedelta(1)
    return date_list

##初始化{商家:{日期:0}}。注意shop_id在字典中的排列顺序是按字符排列
def get_shop_pay_dict():
    shop_pay_dict = {}
    for shop_id in get_shop_id():
        shop_pay_dict[shop_id] = {}
        for date in get_date_list('2015-07-01','2016-10-31'):
            shop_pay_dict[shop_id][date] = 0
    return shop_pay_dict

####统计{商家:{日期:支付数}} (只能一行一行地统计,因为内存不够)
def get_shop_pay_count():
    days_list = get_date_list('2015-07-01','2016-10-31')
    shop_pay_count = get_shop_pay_dict()
    user_pay = get_user_pay()
    for pay_info in user_pay:
        line = pay_info.strip().split(',')
        shop_id = int(line[1])
        date = datetime.datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        if date in days_list:
            shop_pay_count[shop_id][date] += 1
    return shop_pay_count



if __name__ == '__main__':

    #把统计数据写入本地
    shop_pay_count = get_shop_pay_count()
    pd.DataFrame(shop_pay_count).to_csv('shop_pay_count.csv')#注意shop_id的编号排列
