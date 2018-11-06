
import pymongo
import json

settings = {
    'MONGODB_HOST': '127.0.0.1',
    'MONGODB_PORT': 27017,
    'MONGODB_DBNAME': 'nav',
    'MONGODB_DOCNAME': 'nav_name04',
}

class MongoDB(object):
    def __init__(self):
        # 获取setting主机名、端口号和数据库名
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host, port=port)

        # 指向指定的数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb[settings['MONGODB_DOCNAME']]


    def save_json(self, data):
        # data = json.load(jsondata)
        # 向指定的表里添加数据
        self.post.insert(data)

if __name__ == "__main__":
    file = 'E:\cmltest\\nav_name04.json'
    with open(file, 'r', encoding='utf8') as fr:
        jsonData = json.load(fr)
    a = MongoDB()
    a.save_json(jsonData)