import csv
import math
import time
from copy import deepcopy

import pandas as pd

raw_orders = pd.read_csv("rd 2/orders.csv", low_memory=False)
raw_credit = pd.read_csv("rd 2/credit_cards.csv", index_col='userid', low_memory=False)
raw_bank = pd.read_csv("rd 2/bank_accounts.csv", low_memory=False)
raw_devices = pd.read_csv("rd 2/devices.csv", low_memory=False)


def slow_solution_and_incorrect(orders, credit, bank, devices):
    def combine_userid(row):
        if row.name == 'nan':
            return int(row.name)
        else:
            return int(row['userid'])

    credit_bank = credit.join(bank, on='userid', how='outer', rsuffix='_right')
    credit_bank['userid'] = credit_bank.apply(func=combine_userid, axis=1)
    credit_bank = credit_bank.set_index('userid')

    credit_bank_devices = credit_bank.join(devices, on='userid', how='outer')
    credit_bank_devices['userid'] = credit_bank_devices.apply(func=combine_userid, axis=1)
    credit_bank_devices = credit_bank_devices.set_index('userid')

    orders_buyers_all = orders.merge(credit_bank_devices, left_on='buyer_userid', right_on='userid', how='left')
    orders_complete = orders_buyers_all.merge(credit_bank_devices, left_on='seller_userid', right_on='userid',
                                              suffixes=('_buyer', '_seller'), how='left')

    def filter_fake_orders(row):
        if row['buyer_userid'] == row['seller_userid'] \
                or row['device_buyer'] == row['device_seller'] \
                or row['credit_card_buyer'] == row['credit_card_seller'] \
                or row['bank_account_buyer'] == row['bank_account_seller']:
            return 0
        else:
            return 1

    orders_complete['is_fraud'] = orders_complete.apply(func=filter_fake_orders, axis=1)
    orders = orders_complete[['orderid', 'is_fraud']]
    print(orders)
    results = orders.groupby('orderid').max()
    results.to_csv('result_rd2.csv')
    print(results)


def hopefully_faster_solution(orders, credit, bank_accs, devices):
    print(len(orders.index))

    # filter same userid
    all_fake_orders = orders.loc[orders['buyer_userid'] == orders['seller_userid']]
    possible_authentic = orders.loc[orders['buyer_userid'] != orders['seller_userid']]
    print(len(possible_authentic.index))
    print('filtered by userid\n')

    def filter_dataframe(left_table, right_table, right_table_name):
        print('filtering by', right_table_name)
        joined = left_table.merge(right_table, left_on='buyer_userid', right_on='userid', how='left')
        joined = joined.merge(right_table, left_on='seller_userid', right_on='userid', how='left',
                                                suffixes=('_buyer', '_seller'))
        print('after joining', len(joined.index))
        fakes = joined.loc[joined[right_table_name + '_buyer'] == joined[right_table_name + '_seller']]
        fakes = fakes[orders.columns].drop_duplicates()  # remove unnecessary columns
        print('distinct', len(fakes.index))
        if len(fakes.index) == 0:
            authentic = left_table
        else:
            merged = left_table.merge(fakes, on=['orderid', 'buyer_userid', 'seller_userid'], how='left',
                                      indicator=True)
            # print(merged)
            authentic = merged.loc[merged['_merge'] == 'left_only']
            del authentic['_merge']
        print('possible authentic', len(authentic.index))
        # print(authentic)
        print('filtered by ' + right_table_name + '\n')
        return authentic, fakes

    # filter same credit card
    possible_authentic, fake_orders = filter_dataframe(possible_authentic, credit, 'credit_card')
    all_fake_orders = all_fake_orders.append(fake_orders)

    # filter same devices
    possible_authentic, fake_orders = filter_dataframe(possible_authentic, devices, 'device')
    all_fake_orders = all_fake_orders.append(fake_orders)

    # filter same bank_accounts
    possible_authentic, fake_orders = filter_dataframe(possible_authentic, bank_accs, 'bank_account')
    all_fake_orders = all_fake_orders.append(fake_orders)

    print(possible_authentic.head())
    print(all_fake_orders.head())
    assert len(possible_authentic.index) + len(all_fake_orders.index) == len(orders.index)

    possible_authentic.loc[:, 'is_fraud'] = 0
    authentic = possible_authentic[['orderid', 'is_fraud']]
    print('\nset authentic orders')
    print(authentic.head())

    all_fake_orders.loc[:, 'is_fraud'] = 1
    fakes = all_fake_orders[['orderid', 'is_fraud']]
    print('\nset fake orders')
    print(fakes.head())

    results = fakes.append(authentic)
    results.to_csv('[sub] result_rd2.csv', index=False)
    print(results)


start_time = time.time()
# slow_solution(raw_orders, raw_credit, raw_bank, raw_devices)
hopefully_faster_solution(raw_orders, raw_credit, raw_bank, raw_devices)
end_time = time.time()

time_taken = (end_time - start_time) / 60
print("time taken =  " + str(time_taken))
