#测试用例，以交大周边奶茶店搜索，判断数据是否存在明显误差
import requests
import pymongo
import time
import re

#连接数据库
connection = pymongo.MongoClient()
POI = connection.POI
school = POI.school

#获取POI数量以及该类POI类型
def Get_POI_Num(POIlist,url,name,id):
    try:
        header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36",
        }
        for list in POI_list:
            sum=0
            for child in list['children']:
                finurl = url + '&types=' + str(child)
                r = requests.get(finurl,headers=header)
                mes = r.text
                count = re.findall('"count":"(.*?)"', mes)[0]
                sum+=int(count)
            school.update({"ID": id}, {"$set": {str(list['type']): sum}})
            school.update({"ID": id}, {"$set": {'flag':'0'}})
            print(str(name)+"共有"+str(list['type'])+str(sum)+"个")
    except:
        return 'GETMES ERROR'

if __name__ == '__main__':
    start=time.time()
    #定义POI列表
    catering = {"type":"catering","children":['050100','050200','050300','050400','050500','050600','050700','050800','050900']}
    shopping = {"type":"shopping","children":['060100','060200','060400','061000']}
    lifeservice = {"type":"lifeservice","children":['070300','070400','070500']}
    entertainment ={"type":"entertainment","children":['080100','080200','080300','080500','080600']}
    medical ={"type":"medical","children":['090100','090200']}
    hotel_industry={"type":"hotel_industry","children":['100100','100200']}
    traffic ={"type":"traffic","children":['150500','150600','150700']}
    POI_list=[catering,shopping,lifeservice,entertainment,medical,hotel_industry,traffic]
    for item in school.find():
        if item['flag']=='1':
            url = 'https://restapi.amap.com/v3/place/around?key=****************&location=' + str(item['location']) + '&radius=1500'
            Get_POI_Num(POI_list, url, item['name'], item['ID'])
        else:
            print(str(item['name']) + "信息已获取，跳过")
    end=time.time()
    print('程序运行时间为'+str(end-start)+'seconds')

#餐饮 050000 050100（1-23） 050200 050300 050400 050500 050600 050700 050800 050900
#购物 060000 060100 060200 060300---061400
#生活服务 070000 ---070500
#体育休闲 080000 --080600
#医疗 090000
#住宿 100000
#交通 150000
