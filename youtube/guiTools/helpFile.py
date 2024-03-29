import settings
import os
def HelpFile():
    try:
        os.startfile(os.path.join(os.getcwd(),"data","help",settings.settings_handler.get("g","lang"),"readme.html"))
    except:
        os.startfile(os.path.join(os.getcwd(),"data","help","en","readme.html"))