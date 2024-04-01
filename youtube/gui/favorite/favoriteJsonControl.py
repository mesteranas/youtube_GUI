import json
from settings import app
import os
path=os.path.join(os.getenv('appdata'),app.appName,"favorite.json")
if not os.path.exists(path):
    with open(path,"w",encoding="utf-8") as file:
        file.write('{"videos":{},"playlists":{},"channels":{}}')
with open(path,"r",encoding="utf-8")as data:
    data=data.read()
def get(type):
    with open(path,"r",encoding="utf-8") as file :
        return json.load(file)[type]
def save(type,result):
    with open(path,"r",encoding="utf-8")as file:
        dat=json.load(file)
    dat[type]=result
    with open(path,"w",encoding="utf-8")as files:
        files.write(str(dat).replace("'",'"'))