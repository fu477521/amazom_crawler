#-*-coding:utf-8-*-
import csv
import json
import sys
import codecs

def trans(path):
    jsonData = codecs.open(path+'.json', 'r', 'utf-8')
    # csvfile = open(path+'.csv', 'w') # 此处这样写会导致写出来的文件会有空行
    # csvfile = open(path+'.csv', 'wb') # python2下
    csvfile = open(path+'.csv', 'w', newline='') # python3下
    writer = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_ALL)
    dic = json.load(jsonData)
    print(dic)
    def for_circle(dic):
        for k, v in dic.items():
            if len(v) > 1 and isinstance(type(v), type(dict())):
                for_circle(v)
                # 获取属性列表
                keys = list(v.keys())
                print(keys)
                writer.writerow(keys+'\n')  # 将属性列表写入csv中
            # 读取json数据的每一行，将values数据一次一行的写入csv中
            writer.writerow(list(v.values()))
    for_circle(dic)
    """                    
    flag = True
    for line in jsonData:
        dic = json.loads(line[0:-1])
        if flag:
            # 获取属性列表
            keys = list(dic.keys())
            print(keys)
            writer.writerow(keys)   # 将属性列表写入csv中
            flag = False
        # 读取json数据的每一行，将values数据一次一行的写入csv中
        writer.writerow(list(dic.values()))
    """
    jsonData.close()
    csvfile.close()



if __name__ == '__main__':

    #运行指令：第三个参数为需要转换的文件的路径和其名称，将其后缀删除
    #python C:\Users\Documents\json_to_CSV.py C:\Users\Documents\data\xxx

    path = str(sys.argv[1])  # 获取path参数
    print(path)
    trans(path)
