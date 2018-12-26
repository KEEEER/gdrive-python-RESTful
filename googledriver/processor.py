import requests
import os

database = 'https://www.googleapis.com/drive/v3/files/'
download = '?alt=media&access_token='

class Processor:


    def __init__(self , metadata):
        self.metadata = metadata
        
    def create_folders(self , to_path):
        for item in self.metadata:
            if item['mimeType'] == "application/vnd.google-apps.folder":
                try:
                    os.makedirs(to_path + item['path'])
                    print("create new folder : {}".format(item['name']))
                except Exception:
                    pass
                    
        return

    def download_files(self , access_token , to_path):
        for item in self.metadata:
            #if not folder
            if not item['mimeType'] == "application/vnd.google-apps.folder":
                #if file not downloaded
                if not os.path.isfile(item['path']):       
                    url = database + item['id'] + download + access_token 
                    responds = requests.get(url)
                    print("downloading : {}".format(item['name']))
                    try:
                        if item["mimeType"] == "application/vnd.google-apps.spreadsheet":
                            file = open(to_path + item['path'] , "w")
                            file.write(responds.text)
                        #if not google spreadsheet use "wb"
                        else :
                            file = open(to_path + item['path'] , "wb")
                            file.write(responds.content)
                        file.close()
                    except Exception:
                        print("already exist or already delete")
                    
                #if download check edit date

        return
#=======================================================================================