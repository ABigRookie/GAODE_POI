# -*- coding:utf-8 -*-
import pymongo
#连接数据库
connection = pymongo.MongoClient()
POI = connection.POI
school = POI.school

#获取大学名单
fp = open('高校大学名单.txt', "r")
datas = []#存储处理后的数据
lines = fp.readlines()#读取整个文件数据
for line in lines:
    row = line.strip('\n').split()
    datas.extend(row)
fp.close()
print(datas)
#进行匹配去掉多余数据
for data in datas:
    print(data)
    school.update_many({"name": {'$regex':'^'+str(data)}}, {"$set":{"flag":0}})
result = school.delete_many({'flag':1})
print(result.deleted_count)