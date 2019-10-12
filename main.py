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
        news = request4("", city)
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
            "news_title0" : news["title"][0],
            "news_title1" : news["title"][1],
            "news_title2" : news["title"][2],
            "news_title3" : news["title"][3],
            "news_title4" : news["title"][4],
            "news_link0" : news["link"][0],
            "news_link1" : news["link"][1],
            "news_link2" : news["link"][2],
            "news_link3" : news["link"][3],
            "news_link4" : news["link"][4],
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
        rst = res["showapi_res_body"]["pagebean"]["contentlist"][:5]
        return {"title" : [i["title"] for i in rst], "link" : [i["link"] for i in rst]}
    else:
        return {"error" : "lost api"}
if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug = True)
    #print(request4("f598ed3b6a2b4b67834bccf4ef48057a", "北京"))