#coding:utf-8
from sklearn.preprocessing import PolynomialFeatures
from tools import *

##截取部分训练数据
pay_count = pd.read_csv('new_shop_pay_count.csv')
view_count = pd.read_csv('new_shop_view_count.csv')

all_date = get_date_list('2015-07-01', '2016-11-14', '%Y-%m-%d')
week1 = get_date_list('2016-10-25', '2016-10-31', '%Y-%m-%d')
week2 = get_date_list('2016-10-18', '2016-10-24', '%Y-%m-%d')
week3 = get_date_list('2016-10-11', '2016-10-17', '%Y-%m-%d')
week4 = get_date_list('2016-10-04', '2016-10-10', '%Y-%m-%d')
week5 = get_date_list('2016-09-27', '2016-10-03', '%Y-%m-%d')
week6 = get_date_list('2016-09-20', '2016-09-26', '%Y-%m-%d')


week1_index = get_index(all_date, week1)
week2_index = get_index(all_date, week2)
week3_index = get_index(all_date, week3)
week4_index = get_index(all_date, week4)
week5_index = get_index(all_date, week5)
week6_index = get_index(all_date, week6)

train_day_index = []
train_day_index.extend(week1_index + week2_index + week3_index)


#截取pay数据
train_pay1 = pay_count.iloc[week1_index,:]
train_pay2 = pay_count.iloc[week2_index,:]
train_pay3 = pay_count.iloc[week3_index,:]
train_pay4 = pay_count.iloc[week4_index,:]
train_pay5 = pay_count.iloc[week5_index,:]
train_pay6 = pay_count.iloc[week6_index,:]
train_pay_count = pd.concat([train_pay1, train_pay2, train_pay3])


#截取view数据
train_view1 = view_count.iloc[week1_index,:]
train_view2 = view_count.iloc[week2_index,:]
train_view3 = view_count.iloc[week3_index,:]
train_view4 = view_count.iloc[week4_index,:]
train_view5 = view_count.iloc[week5_index,:]
train_view6 = view_count.iloc[week6_index,:]
train_view_count = pd.concat([train_view1, train_view2, train_view3])



##处理商家信息
title = ['shop_id','city_name','location_id','per_pay','score','comment_cnt', 'shop_level','category_1','category_2','category_3']
shop_info = pd.read_csv('shop_info.txt', header=None, names=title)

#将城市,人均消费,品类等因子化,作为哑变量
city = pd.get_dummies(shop_info['city_name'])
per_pay = pd.get_dummies(shop_info['per_pay'])
score = pd.get_dummies(shop_info['score'])
shop_level = pd.get_dummies(shop_info['shop_level'])
category_1 = pd.get_dummies(shop_info['category_1'])
category_2 = pd.get_dummies(shop_info['category_2'])
category_3 = pd.get_dummies(shop_info['category_3'])

Score_ShopLevel = pd.concat([score, shop_level], axis=1)

poly = PolynomialFeatures(2, interaction_only=True, include_bias=False)
Score_ShopLevel = pd.DataFrame(poly.fit_transform(Score_ShopLevel))

shop_info = pd.concat([shop_info, city, per_pay, Score_ShopLevel, category_1, category_2, category_3], axis=1)

#地区消费统计特征
location_perpay_mean = shop_info['per_pay'].groupby(shop_info['location_id']).mean()
location_perpay_median = shop_info['per_pay'].groupby(shop_info['location_id']).median()
location_perpay_max = shop_info['per_pay'].groupby(shop_info['location_id']).max()
location_perpay_min = shop_info['per_pay'].groupby(shop_info['location_id']).min()

location_perpay_stat = pd.concat([location_perpay_mean, location_perpay_median, location_perpay_max, location_perpay_min], axis=1)
location_perpay_stat.columns = ['location_perpay_mean', 'location_perpay_median', 'location_perpay_max', 'location_perpay_min']
shop_info = pd.merge(shop_info, location_perpay_stat, left_on='location_id', right_index=True).sort_values(by='shop_id')

#地区商店水平
location_shoplevel_mean = shop_info['shop_level'].groupby(shop_info['location_id']).mean()
location_shoplevel_median = shop_info['shop_level'].groupby(shop_info['location_id']).median()
location_shoplevel_max = shop_info['shop_level'].groupby(shop_info['location_id']).max()
location_shoplevel_min = shop_info['shop_level'].groupby(shop_info['location_id']).min()

location_shoplevel_stat = pd.concat([location_shoplevel_mean, location_shoplevel_median, location_shoplevel_max, location_shoplevel_min], axis=1)
location_shoplevel_stat.columns = ['location_shoplevel_mean', 'location_shoplevel_median', 'location_shoplevel_max', 'location_shoplevel_min']
shop_info = pd.merge(shop_info, location_shoplevel_stat, left_on='location_id', right_index=True).sort_values(by='shop_id')

#城市消费
city_perpay_mean = shop_info['per_pay'].groupby(shop_info['city_name']).mean()
city_perpay_median = shop_info['per_pay'].groupby(shop_info['city_name']).median()
city_perpay_max = shop_info['per_pay'].groupby(shop_info['city_name']).max()
city_perpay_min = shop_info['per_pay'].groupby(shop_info['city_name']).min()

city_perpay_stat = pd.concat([city_perpay_mean, city_perpay_median, city_perpay_max, city_perpay_min], axis=1)
city_perpay_stat.columns = ['city_perpay_mean', 'city_perpay_median', 'city_perpay_max', 'city_perpay_min']
shop_info = pd.merge(shop_info, city_perpay_stat, left_on='city_name', right_index=True).sort_values(by='shop_id')

#城市商店水平
city_shoplevel_mean = shop_info['shop_level'].groupby(shop_info['city_name']).mean()
city_shoplevel_median = shop_info['shop_level'].groupby(shop_info['city_name']).median()
city_shoplevel_max = shop_info['shop_level'].groupby(shop_info['city_name']).max()
city_shoplevel_min = shop_info['shop_level'].groupby(shop_info['city_name']).min()

city_shoplevel_stat = pd.concat([city_shoplevel_mean, city_shoplevel_median, city_shoplevel_max, city_shoplevel_min], axis=1)
city_shoplevel_stat.columns = ['city_shoplevel_mean', 'city_shoplevel_median', 'city_shoplevel_max', 'city_shoplevel_min']
shop_info = pd.merge(shop_info, city_shoplevel_stat, left_on='city_name', right_index=True).sort_values(by='shop_id')


shop_info.drop(['shop_id', 'city_name', 'shop_level', 'score', 'category_1', 'category_2', 'category_3'],axis=1, inplace=True)
shop_info = shop_info.fillna(0)



##提取商家客流量统计特征
shop_info['week1_sum'] = train_pay1.sum().values
shop_info['week1_mean'] = train_pay1.mean().values
shop_info['week1_median'] = train_pay1.median().values
shop_info['week1_max'] = train_pay1.max().values
shop_info['week1_min'] = train_pay1.min().values

shop_info['week2_sum'] = train_pay2.sum().values
shop_info['week2_mean'] = train_pay2.mean().values
shop_info['week2_median'] = train_pay2.median().values
shop_info['week2_max'] = train_pay2.max().values
shop_info['week2_min'] = train_pay2.min().values

shop_info['week3_sum'] = train_pay3.sum().values
shop_info['week3_mean'] = train_pay3.mean().values
shop_info['week3_median'] = train_pay3.median().values
shop_info['week3_max'] = train_pay3.max().values
shop_info['week3_min'] = train_pay3.min().values

shop_info['weeks_sum'] = train_pay_count.sum().values
shop_info['weeks_mean'] = train_pay_count.mean().values
shop_info['weeks_median'] = train_pay_count.median().values
shop_info['weeks_max'] = train_pay_count.max().values
shop_info['weeks_min'] = train_pay_count.min().values



#提取商家浏览统计特征
shop_info['view_week1_sum'] = train_view1.sum().values
shop_info['view_week1_mean'] = train_view1.mean().values
shop_info['view_week1_median'] = train_view1.median().values
shop_info['view_week1_max'] = train_view1.max().values
shop_info['view_week1_min'] = train_view1.min().values

shop_info['view_week2_sum'] = train_view2.sum().values
shop_info['view_week2_mean'] = train_view2.mean().values
shop_info['view_week2_median'] = train_view2.median().values
shop_info['view_week2_max'] = train_view2.max().values
shop_info['view_week2_min'] = train_view2.min().values

shop_info['view_week3_sum'] = train_view3.sum().values
shop_info['view_week3_mean'] = train_view3.mean().values
shop_info['view_week3_median'] = train_view3.median().values
shop_info['view_week3_max'] = train_view3.max().values
shop_info['view_week3_min'] = train_view3.min().values

shop_info['view_weeks_sum'] = train_view_count.sum().values
shop_info['view_weeks_mean'] = train_view_count.mean().values
shop_info['view_weeks_median'] = train_view_count.median().values
shop_info['view_weeks_max'] = train_view_count.max().values
shop_info['view_weeks_min'] = train_view_count.min().values



##提取时间特征
days_info = pd.read_csv('days_info.txt', header=None, index_col=False, names=['weekdays','holiday'])
days_info = pd.concat([pd.get_dummies(days_info['weekdays']), pd.get_dummies(days_info['holiday'])],axis=1)

poly = PolynomialFeatures(2, interaction_only=True, include_bias=False)
days_info = pd.DataFrame(poly.fit_transform(days_info))
# print days_info.shape



##提取天气特征
title = ['city', 'date', 'high_temp', 'low_temp', 'early_weather', 'late_weather']
weather_info = pd.read_csv('weather_info.txt', header=None, names=title)



##客流量week_lag特征(横向)
#train
train_pay_lag_week_1 = pd.concat([train_pay2, train_pay3, train_pay4]).values.reshape(-1)
train_pay_lag_week_2 = pd.concat([train_pay3, train_pay4, train_pay5]).values.reshape(-1)
train_pay_lag_week_3 = pd.concat([train_pay4, train_pay5, train_pay6]).values.reshape(-1)
train_pay_lag_week_feature = pd.DataFrame({'lag_week_1':train_pay_lag_week_1, 'lag_week_2':train_pay_lag_week_2, 'lag_week_3':train_pay_lag_week_3})

train_pay_lag_week_mean = train_pay_lag_week_feature.mean(axis=1)
train_pay_lag_week_median = train_pay_lag_week_feature.median(axis=1)
train_pay_lag_week_max = train_pay_lag_week_feature.max(axis=1)
train_pay_lag_week_min = train_pay_lag_week_feature.min(axis=1)

train_pay_lag_week_feature['lag_week_mean'] = train_pay_lag_week_mean
train_pay_lag_week_feature['lag_week_median'] = train_pay_lag_week_median
train_pay_lag_week_feature['lag_week_max'] = train_pay_lag_week_max
train_pay_lag_week_feature['lag_week_min'] = train_pay_lag_week_min

#test
test_pay_lag_week_1 = pd.concat([train_pay1]).values.reshape(-1)
test_pay_lag_week_2 = pd.concat([train_pay2]).values.reshape(-1)
test_pay_lag_week_3 = pd.concat([train_pay3]).values.reshape(-1)
test_pay_lag_week_feature = pd.DataFrame({'lag_week_1':test_pay_lag_week_1, 'lag_week_2':test_pay_lag_week_2, 'lag_week_3':test_pay_lag_week_3})

test_pay_lag_week_mean = test_pay_lag_week_feature.mean(axis=1)
test_pay_lag_week_median = test_pay_lag_week_feature.median(axis=1)
test_pay_lag_week_max = test_pay_lag_week_feature.max(axis=1)
test_pay_lag_week_min = test_pay_lag_week_feature.min(axis=1)

test_pay_lag_week_feature['lag_week_mean'] = test_pay_lag_week_mean
test_pay_lag_week_feature['lag_week_median'] = test_pay_lag_week_median
test_pay_lag_week_feature['lag_week_max'] = test_pay_lag_week_max
test_pay_lag_week_feature['lag_week_min'] = test_pay_lag_week_min



##浏览lag特征(横向)
#train
train_view_lag_week_1 = pd.concat([train_view2, train_view3, train_view4]).values.reshape(-1)
train_view_lag_week_2 = pd.concat([train_view3, train_view4, train_view5]).values.reshape(-1)
train_view_lag_week_3 = pd.concat([train_view4, train_view5, train_view6]).values.reshape(-1)
train_view_lag_week_feature = pd.DataFrame({'view_lag_week_1':train_view_lag_week_1, 'view_lag_week_2':train_view_lag_week_2, 'view_lag_week_3':train_view_lag_week_3})

train_view_lag_week_mean = train_view_lag_week_feature.mean(axis=1)
train_view_lag_week_median = train_view_lag_week_feature.median(axis=1)
train_view_lag_week_max = train_view_lag_week_feature.max(axis=1)
train_view_lag_week_min = train_view_lag_week_feature.min(axis=1)

train_view_lag_week_feature['view_lag_week_mean'] = train_view_lag_week_mean
train_view_lag_week_feature['view_lag_week_median'] = train_view_lag_week_median
train_view_lag_week_feature['view_lag_week_max'] = train_view_lag_week_max
train_view_lag_week_feature['view_lag_week_min'] = train_view_lag_week_min

#test
test_view_lag_week_1 = pd.concat([train_view1]).values.reshape(-1)
test_view_lag_week_2 = pd.concat([train_view2]).values.reshape(-1)
test_view_lag_week_3 = pd.concat([train_view3]).values.reshape(-1)
test_view_lag_week_feature = pd.DataFrame({'view_lag_week_1':test_view_lag_week_1, 'view_lag_week_2':test_view_lag_week_2, 'view_lag_week_3':test_view_lag_week_3})

test_view_lag_week_mean = test_view_lag_week_feature.mean(axis=1)
test_view_lag_week_median = test_view_lag_week_feature.median(axis=1)
test_view_lag_week_max = test_view_lag_week_feature.max(axis=1)
test_view_lag_week_min = test_view_lag_week_feature.min(axis=1)

test_view_lag_week_feature['view_lag_week_mean'] = test_view_lag_week_mean
test_view_lag_week_feature['view_lag_week_median'] = test_view_lag_week_median
test_view_lag_week_feature['view_lag_week_max'] = test_view_lag_week_max
test_view_lag_week_feature['view_lag_week_min'] = test_view_lag_week_min

#合并客流量lag特征与浏览lag特征
train_lag_week_feature = pd.concat([train_pay_lag_week_feature, train_view_lag_week_feature], axis=1)
test_lag_week_feature = pd.concat([test_pay_lag_week_feature, test_view_lag_week_feature], axis=1)

#对lag特征进行交叉
poly = PolynomialFeatures(2, interaction_only=True, include_bias=False)
train_lag_week_feature = pd.DataFrame(poly.fit_transform(train_lag_week_feature))
test_lag_week_feature = pd.DataFrame(poly.transform(test_lag_week_feature))

#-----------------------------------------------------------------------------------------------------

##生成训练label
print 'writting train label...'
train_label = np.asarray(train_pay_count.values).reshape(-1)#按行reshape,即内循环商家,外循环日期
pd.Series(train_label).to_csv('train_label.csv', index=False)

city_list = get_shop_city_name_list()

#生成训练特征矩阵并写入本地train_feature.csv
print 'getting train feature...'
train_feature =[]
for day_index in train_day_index:
    for shop_id in range(2000):
        city_weather_info = weather_info[weather_info['city']==city_list[shop_id]].iloc[:,2:]
        row = []
        shop_feature = shop_info.ix[shop_id].tolist()
        day_feature = days_info.ix[day_index].tolist()
        weather_feature = city_weather_info.iloc[day_index, :].tolist()
        row.extend(day_feature + shop_feature + weather_feature)
        train_feature.append(row)
train_feature_DF = pd.DataFrame(train_feature)
train_feature_DF = pd.concat([train_feature_DF, train_lag_week_feature], axis=1)
print 'writting train feature...'
train_feature_DF.to_csv('train_feature.csv', index=False)


##生成测试集特征并写入test_feature.csv
test_day_index=get_index(all_date, get_date_list('2016-11-01', '2016-11-07', '%Y-%m-%d'))
print 'getting test feature...'
test_feature =[]
for day_index in test_day_index:
    for shop_id in range(2000):
        city_weather_info = weather_info[weather_info['city'] == city_list[shop_id]].iloc[:, 2:]
        row = []
        shop_feature = shop_info.ix[shop_id].tolist()
        day_feature = days_info.ix[day_index].tolist()
        weather_feature = city_weather_info.iloc[day_index, :].tolist()
        row.extend(day_feature + shop_feature + weather_feature)
        test_feature.append(row)
test_feature_DF = pd.DataFrame(test_feature)
test_feature_DF = pd.concat([test_feature_DF, test_lag_week_feature], axis=1)
test_feature_DF = pd.concat([test_feature_DF, test_feature_DF])
print 'writting test feature...'
test_feature_DF.to_csv('test_feature.csv', index=False)