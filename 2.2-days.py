#coding:utf-8
import pandas as pd
import datetime
import requests
import re


def get_date_list(start, end, toFormat):
    date_list = []
    date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end = datetime.datetime.strptime(end, '%Y-%m-%d')
    while date <= end:
        date_list.append(date.strftime(toFormat))
        date = date + datetime.timedelta(1)
    return date_list

## api获取假期特征
def isHoliday(date):
    return requests.get('http://www.easybots.cn/api/holiday.php?d=%s'%date).content


weekdays = pd.DataFrame(get_date_list('2015-07-01', '2016-11-14', '%A'), columns=['weekdays'])
content = isHoliday(','.join(get_date_list('2015-07-01','2016-11-14','%Y%m%d')))
holiday = pd.DataFrame(re.findall('"(\d{1})"',content),columns = ['isHoliday'])
days_info = pd.concat([weekdays['weekdays'],holiday],axis=1)
days_info.to_csv('days_info.txt', header=None, index=False)


days_info = pd.read_csv('days_info.txt', header=None, index_col=False,
                           names=['weekdays','holiday'])
days_info = pd.concat([pd.get_dummies(days_info['weekdays']), days_info['holiday']],axis=1)
print days_info
