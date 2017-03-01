#coding:utf-8
from tools import *
pay_count = pd.read_csv('shop_pay_count.csv')
view_count = pd.read_csv('shop_view_count.csv')


new_pay_count = np.zeros(pay_count.shape)
for shop_id in range(1,2001):
    shop_pay_count = pay_count[str(shop_id)]
    shop_pay_count = clean_data(shop_pay_count)
    new_pay_count[:,shop_id-1] = shop_pay_count
new_pay_count = pd.DataFrame(new_pay_count, dtype=int)
new_pay_count.columns = range(1,2001)
new_pay_count.to_csv('new_shop_pay_count.csv', index=False)


new_view_count = np.zeros(view_count.shape)
for shop_id in range(1,2001):
    shop_view_count = view_count[str(shop_id)]
    shop_view_count = clean_data(shop_view_count)
    new_view_count[:,shop_id-1] = shop_view_count
new_view_count = pd.DataFrame(new_view_count, dtype=int)
new_view_count.columns = range(1,2001)
new_view_count.to_csv('new_shop_view_count.csv', index=False)

