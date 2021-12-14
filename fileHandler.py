import pandas as pd
import numpy as np
import json

class csvHandler:
    def __init__(self,fileName):
        self.fileName = fileName
        df = pd.read_csv(fileName)
        self.data = {}
        for i in df:
            self.data[i]=df[i].tolist()
        self.dataFrame = df
    def csvToJson(self,jsonFile):
        df = pd.read_csv(self.fileName)
        li = []
        for i in range(len(df)):
            row = {}
            for j in df:
                try :
                    a = float(df[j][i])
                except:
                    a = str(df[j][i]) 
                row[j] = a
            li.append(row)
        with open("{}.json".format(jsonFile), "w") as write_file:
            json.dump(li,write_file)

class jsonHandler:
    def __init__(self,fileName):
        self.fileName = fileName
        with open(fileName, "r") as read_file:
            self.data = json.load(read_file)
        dic = {}
        key_li = list(self.data[0].keys())
        for key in key_li:
            dic[key] = []
        for i in self.data:
            for key in key_li:
                dic[key].append(i[key])
        self.dataFrame = pd.DataFrame(dic)
    def jsonToCsv(self,csvFile):
        self.dataFrame.to_csv('{}.csv'.format(csvFile),index=False) 
        


# a = csvHandler('produksi_minyak_mentah.csv')
# a.csvToJson('tes')

# a = jsonHandler('kode_negara_lengkap.json')
# print(a.dataFrame)
