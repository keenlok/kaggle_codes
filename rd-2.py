import sys
import pandas as pd
import csv

def hasSameCreditCard(buyer, seller, data):
    #print(data)
    for d1 in data[data['userid'] == buyer]["credit_card"]:
        for d2 in data[data['userid'] == seller]["credit_card"]:
            if d1 == d2:
                return True
    return False

def hasSameBankAcc(buyer, seller, data):
    #print(data)
    for d1 in data[data['userid'] == buyer]["bank_account"]:
        for d2 in data[data['userid'] == seller]["bank_account"]:
            if d1 == d2:
                return True
    return False

def hasSameDevice(buyer, seller, data):
    #print(data)
    for d1 in data[data['userid'] == buyer]["device"]:
        for d2 in data[data['userid'] == seller]["device"]:
            if d1 == d2:
                return True
    return False

def filterIndirectOrders(orders):
    credit = pd.read_csv("rd 2/credit_cards.csv", index_col="userid", low_memory=False)
    bank = pd.read_csv("rd 2/bank_accounts.csv", index_col="userid", low_memory=False)
    devices = pd.read_csv("rd 2/devices.csv", index_col="userid", low_memory=False)

    result = pd.merge(bank, credit, how='left', on='userid')
    print(result)
    finalusers = pd.merge(result, devices, how="left", on='userid')
    print(finalusers)
    ordersBuyers = pd.merge(orders, finalusers, how="left", left_on='buyer_userid', right_on='userid')
    print(ordersBuyers)
    orderBuyersSellers = pd.merge(ordersBuyers, finalusers, how="left", left_on='seller_userid', right_on='userid')
    print(orderBuyersSellers)

    print(ordersBuyers.head())

    return fakes, authentic

if __name__ == "__main__":
    orders = pd.read_csv("rd 2/orders.csv", index_col="orderid", low_memory=False)
    possible_fakes = []
    filtered = []
    '''for row in orders.itertuples():
        index = getattr(row, "Index")
        #print(index)
        #print(row)
        buyer = getattr(row, "buyer_userid")
        seller = getattr(row, "seller_userid")
        #print("What is this", buyer, seller)
        if buyer == seller:
            possible_fakes.append((index, 1))
        else:
            print("What is added here?", index)
            filtered.append(row)'''

    fakes, authentic = filterIndirectOrders(orders)
    possible_fakes += fakes
    final_result = possible_fakes + authentic

    csv.register_dialect('myDialect',
                         delimiter=',',
                         quotechar='"',
                         quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)

    with open("dummy.csv", "w") as csvFile:
        writer = csv.writer(csvFile, dialect='myDialect')
        writer.writerows([["orderid", "is_fraud"]])
        writer.writerows(final_result)

    csvFile.close()
