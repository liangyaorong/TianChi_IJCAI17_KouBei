from tools import *

pay_count = pd.read_csv('shop_pay_count.csv')
weekly_cycle_shop = []
for shop_id in range(1,2001):
    shop_pay = pay_count[str(shop_id)]
    if judge_cycle(shop_pay, 0.9) == True:
        weekly_cycle_shop.append(shop_id)
print weekly_cycle_shop

# answer_file_name = 'sigma3_preOneWeek_n1000_pred.csv'
# pay_count = pd.read_csv('shop_pay_count.csv')
# answer = pd.read_csv(answer_file_name, header=None)
# for shop_id in range(2000):
#     shop_pay = pay_count[str(shop_id+1)]
#     if judge_cycle(shop_pay, 0.9) == True:
#         print shop_id
#         new_answer = shop_pay[-14:].values.reshape(2,-1).mean(axis=0).round().astype(int).tolist()*2
#         answer.iloc[shop_id,1:] = new_answer
# answer.to_csv('model_with_WeeklyCycleFillLastTwoWeek_pred.csv',header = None, index=False)