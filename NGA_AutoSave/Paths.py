import json


settingFolderPath='.\Settings'
cookieTxtPath=settingFolderPath+'\cookie.txt'
settingJsonPath=settingFolderPath+'\setting.json'

saveHtmlFolderPath=''
if(len(saveHtmlFolderPath)==0):
    with open(settingJsonPath, 'r', encoding='utf-8') as f:  
        settings = json.load(f)
        saveHtmlFolderPath=settings['saveHtmlFolderPath']
