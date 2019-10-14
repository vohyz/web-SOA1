from flask import Flask, render_template, request, session
import requests
import json, urllib
from urllib import parse
from urllib.request import urlopen
from threading import Thread

from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials


app = Flask(__name__)
appkey1 = "SqDC76itesKz0z_uF"
subscription_key = "b7959ce83d8d4d778e11a93f92dab4de"

weather = {}
live = {}
air = {}
news = []
baike = {}

@app.route('/', methods=["GET","POST"])
def hello_world():
    Data = {"city" : "上海"}
    if request.method == "POST":
        form_data = request.form
        city = form_data.get("search")
        t1 = Thread(target=request1, args=(appkey1, city))
        t2 = Thread(target=request2, args=(appkey1, city))
        t3 = Thread(target=request3, args=(appkey1, city))
        t4 = Thread(target=request4, args=(" ", city))
        t5 = Thread(target=web_results_with_count_and_offset, args=(subscription_key, city))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
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
            "news" : news,
            "webPage" : baike["page"],
            "webUrl" : baike["url"],
            "webSnippet" : baike["snippet"],
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
    
    global weather
    if res:
        rst = res["results"][0]["now"]
        weather = rst
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
    global live
     
    if res:
        rst = res["results"][0]["suggestion"]
        live = rst
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
    global air
      
    if res:
        rst = res["results"][0]["air"]["city"]
        air = rst
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
    global news
     
    if res:
        rst = res["showapi_res_body"]["pagebean"]["contentlist"]
        n = 0
        prm = []
        for i in rst:
            if n < 6:
                prm.append([i["title"],i["link"].strip('"')])
            else:
                break
            n += 1
    
        news = prm
    else:
        return {"error" : "lost api"}

#必应搜索百科
def web_results_with_count_and_offset(subscription_key, city):
     client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))
     global baike
     try:
         '''
         Set the query, offset, and count using the SDK's search method. See:
         https://docs.microsoft.com/python/api/azure-cognitiveservices-search-websearch/azure.cognitiveservices.search.websearch.operations.weboperations?view=azure-python.
         '''
         city = city
         web_data = client.web.search(query=city, offset=0, count=5)

         if web_data.web_pages.value:
             '''
             If web pages are available, print the # of responses, and the first and second
             web pages returned.
             '''
             #print("Webpage Results#{}".format(len(web_data.web_pages.value)))

             for i in web_data.web_pages.value:
                 if "百科" in format(i.name):
                     webPage = format(i.name)
                     webUrl = format(i.url)
                     webSnippet = format(i.snippet)
             
             baike = {
                 "page" : webPage,
                 "url" : webUrl,
                 "snippet" : webSnippet
             }
             #print("First web page name: {} ".format(first_web_page.name))
             #print("First web page URL: {} ".format(first_web_page.url))

         else:
             print("Didn't find any web pages...")

     except Exception as err:
         print("Encountered exception. {}".format(err))

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug = True)
    #print(request4("f598ed3b6a2b4b67834bccf4ef48057a", "北京"))