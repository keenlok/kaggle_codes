import sys
import pandas as pd
import csv

def parse_keywords(keyword_grp):
    keyword_dict = {}
    for keywords in keyword_grp["Keywords"].items():
        arr = keywords[1].split(", ")
        keyword_dict[keywords[0]] = arr
    print(keyword_dict)
    return keyword_dict


if __name__ == "__main__":
    keyword_grp = pd.read_csv("Extra Material 2 - keyword list_with substring.csv", index_col="Group")
    keywords = parse_keywords(keyword_grp)
    results = []
    parsedData = []
    df = pd.read_csv("Keyword_spam_question.csv", index_col="index")
    for data in df["name"].items():
        # print(data)
        parsedData.append((data[0], data[1].lower()))


    for data in parsedData:
        print(data[0])
        name = data[1]
        temp = []
        for key, item in keywords.items():
            #print(key)
            #print(item)
            for words in item:
                if name.find(words) != -1:
                    temp.append(key)
                    break

        for i in temp:
            isSubset = False
            for j in temp:
                if i != j:
                    try:
                        keywords[i].index(keywords[j][0])
                        isSubset = True
                    except ValueError:
                        continue

            if isSubset:
                temp.remove(i)
        results.append((data[0], temp))

    csv.register_dialect('myDialect',
                         delimiter=',',
                         quotechar='"',
                         quoting=csv.QUOTE_ALL,
                         skipinitialspace=True)

    with open("dum.csv", "w") as csvFile:
        writer = csv.writer(csvFile, dialect='myDialect')
        writer.writerows([["index", "groups_found"]])
        writer.writerows(results)

    csvFile.close()








