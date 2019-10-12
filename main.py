from flask import Flask, render_template, request, session
import requests
import json, urllib
from urllib import parse
from urllib.request import urlopen

app = Flask(__name__)
appkey1 = "SqDC76itesKz0z_uF"
@app.route('/', methods=["GET","POST"])
def hello_world():
    Data = {"city" : "上海"}
    if request.method == "POST":
        form_data = request.form
        city = form_data.get("search")
        weather = request1(appkey1, city)
        live = request2(appkey1, city)
        air = request3(appkey1, city)
        Data = {
            "city" : city,
            "temperature" : weather["temperature"],
            "weather" : weather["text"],
            "air_aqi" : air["aqi"],
            "air_quality" : live["air_pollution"]["brief"],
            "air_pm25" : air["pm25"],
            "air_primary" : air["primary_pollutant"],
            "air_suggestion" : live["air_pollution"]["details"],
            "live_comfort" : live["comfort"]["brief"],
        }
        
    return render_template('index.html', Data = Data)

#天气信息查询
def request1(appkey, city, m="GET"):
    url = "https://api.seniverse.com/v3/weather/now.json"
    params = {
        "key" : appkey, #你申请的key
        "location" : city,
        "unit" : "c"
    }
    params = parse.urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    #print(res)  
    if res:
        rst = res["results"][0]["now"]
        return rst
    else:
        return {"error" : "lost api"}

#生活指数信息查询
def request2(appkey, city, m="GET"):
    url = "https://api.seniverse.com/v3/life/suggestion.json"
    params = {
        "key" : appkey, #你申请的key
        "location" : city,
    }
    params = parse.urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    #print(res)  
    if res:
        rst = res["results"][0]["suggestion"]
        return rst
    else:
        return {"error" : "lost api"}

#空气质量信息查询
def request3(appkey, city, m="GET"):
    url = "https://api.seniverse.com/v3/air/now.json"
    params = {
        "key" : appkey, #你申请的key
        "location" : city,
    }
    params = parse.urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    #print(res)  
    if res:
        rst = res["results"][0]["air"]["city"]
        return rst
    else:
        return {"error" : "lost api"}

#新闻查询
def request4(appkey, city, m="GET"):
    appkey = "f598ed3b6a2b4b67834bccf4ef48057a"
    url = "http://route.showapi.com/170-47"
    params = {
        "showapi_appid" : "106801",
        "showapi_sign" : appkey, #你申请的key
        "areaName" : city,
    }
    params = parse.urlencode(params)
    if m =="GET":
        f = urlopen("%s?%s" % (url, params))
    else:
        f = urlopen(url, params)
 
    content = f.read()
    res = json.loads(content)
    #print(res)  
    if res:
        rst = res
        return rst
    else:
        return {"error" : "lost api"}
if __name__ == "__main__":
    #app.run(host="127.0.0.1",port=5000,debug = True)
    print(request4("f598ed3b6a2b4b67834bccf4ef48057a", "北京"))

    {
    'showapi_res_error': '', 
    'showapi_res_id': '12a9f17831a74cdebd930b56c85aa0cb', 
    'showapi_res_code': 0, 
    'showapi_res_body': {'ret_code': 0, 
    'pagebean': {'allPages': 72, 
    'contentlist': [
     {'id': '97ebd75d3ccc42df677540bae30c1e65', 
     'pubDate': '2019-10-11 10:56:00', 
     'title': '朝阳不动产登记大厅“人脸识别” ', 
     'imageurls': [], 
     'desc': '', 
     'areaName': '北京', 
     'source': '中国新闻网', 
     'link': 'http://www.bj.chinanews.com/news/2019/1011/73582.html', 
     'img': '', 
     'ct': '2019-10-12 15:31:37.107', 
     'areaId': '55818af5085b7bc0c73836b4'}, 
     {'id': '174dee6c1a97720da4c62941575d07c5', 
     'pubDate': '2019-10-11 09:52:00', 
     'title': '421个老旧小区配电网陆续改造 ', 
     'imageurls': [], 
     'desc': '', 
     'areaName': '北京', 
     'source': '中国新闻网', 
     'link': 'http://www.bj.chinanews.com/news/2019/1011/73580.html', 
     'img': '', 
     'ct': '2019-10-12 15:31:37.130', 
     'areaId': '55818af5085b7bc0c73836b4'}, 
     {'id': '109e5231150f2d415417010dad8a9ed7', 
     'pubDate': '2019-10-10 23:51:00', 
     'title': '国庆群众游行“高定服装”:10万套一月制 细节处显用心', 
     'imageurls': [], 'desc': '', 'areaName': '北京', 'source': '', 
     'link': 'http://www.bj.chinanews.com/news/2019/1010/73578.html', 
     'img': '', 'ct': '2019-10-11 00:02:01.076', 'areaId': '55818af5085b7bc0c73836b4'}, 
     ], 
     'currentPage': 1, 'allNum': 718, 'maxResult': 10}}}