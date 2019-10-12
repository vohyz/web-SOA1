from flask import Flask, render_template, request, session
import requests
import json

app = Flask(__name__)
'''
url1 = 'http://www.baidu.com/s'
r = requests.post(url1)
print(r.status_code)
response = r.json()

print(response.keys())
'''
@app.route('/', methods=["GET","POST"])
def hello_world():
    Data = {"city" : "上海"}
    if request.method == "POST":
        form_data = request.form
        city = form_data.get("search")
        Data = {"city" : city}
    return render_template('index.html', Data = Data)

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug = True)