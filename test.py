if __name__ == "__main__":
    orders = pd.read_csv("rd 2/orders.csv", index_col="orderid", low_memory=False)
    possible_fakes = []
    filtered = []
    for row in orders.itertuples():
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
            filtered.append(row)

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
