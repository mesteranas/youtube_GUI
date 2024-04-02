import json
from settings import app
import os
path=os.path.join(os.getenv('appdata'),app.appName,"history.json")
if not os.path.exists(path):
    with open(path,"w",encoding="utf-8") as file:
        file.write('{}')
def get(name):
    with open(path,"r",encoding="utf-8") as file :
        file=json.load(file)
    if file.get(name):
        return True,file[name]["position"],file[name]["url"]
    else:
        return False,0,None
def save(name,position,url):
    with open(path,"r",encoding="utf-8")as file:
        dat=json.load(file)
    dat[name]={"position":position,"url":url}
    with open(path,"w",encoding="utf-8")as files:
        files.write(str(dat).replace("'",'"'))