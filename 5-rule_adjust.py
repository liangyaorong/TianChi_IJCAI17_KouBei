#coding:utf-8

from tools import *

pay_count = pd.read_csv('new_shop_pay_count.csv')
answer_file_name = 'ExtRandomTree_n1000_pred.csv'
answer = pd.read_csv(answer_file_name, header=None)

shop23_pay = pay_count[str(23)]
shop23_new_pay = pd.DataFrame(shop23_pay[6:].values.reshape(-1,7))[-10:-7].mean().values.round().astype(int).tolist()*2
answer.iloc[22,1:] = shop23_new_pay

shop810_pay = pay_count[str(810)]
shop810_new_pay = pd.DataFrame(shop810_pay[6:].values.reshape(-1,7))[-1:].values.round().astype(int).tolist()[0]*2
answer.iloc[809,1:] = shop810_new_pay

answer.to_csv('ExtRandomTree_n1000_fix23810_pred.csv', header=None, index=False)