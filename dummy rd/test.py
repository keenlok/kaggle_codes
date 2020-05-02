import sys
import matplotlib
import pandas as pd
import csv
import seaborn as sns
import numpy as np

if __name__ == "__main__":
    df = pd.read_csv("Dummy data.csv", index_col="id")
    print(df.head())


    new_list = []
    for data in df["number"].items():
    # for data in df".items():
        print("What is this")
        print(data)
        newData = (data[1], data[0] + 1)
        # print(newData)
        new_list.append(newData)

    csv.register_dialect('myDialect',
                         delimiter=',',
                         quotechar='"',
                         quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)

    with open("Dummy.csv", "w") as csvFile:
        writer = csv.writer(csvFile, dialect='myDialect')
        writer.writerows([["id", "new_number"]])
        writer.writerows(new_list)

    csvFile.close()




