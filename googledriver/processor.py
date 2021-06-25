import requests
import os
import io

database = 'https://www.googleapis.com/drive/v3/files/'
params = {
    'access_token' : "no",
    'fields' : "*"
}

class Processor:
    # create_folders
    # download_files

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
        header = {'Authorization': 'Bearer {}'.format(access_token)}
        for item in self.metadata:

            if not item['mimeType'] == "application/vnd.google-apps.folder":
                if 'size' in item:
                    if int(item['size']) > 2000000000:
                        print('ignore large file(issue fixing) : ' + item['name'])
                        continue

                if not os.path.isfile(item['path']):
                    url = database + item['id'] + '?alt=media'
                    response = requests.get(url, headers=header)
                    try:
                        CHUNK_SIZE = 32768
                        if item["mimeType"] == "application/vnd.google-apps.spreadsheet":
                            file = open(to_path + item['path'] , "w")
                            print("downloading spread : {}".format(item['name']))
                            for chunk in response.iter_content(CHUNK_SIZE):
                                if chunk:
                                    file.write(chunk)

                        #if not google spreadsheet use "wb"
                        else:
                            file = open(to_path + item['path'] , "wb")
                            print("downloading : {}".format(item['name']))
                            for chunk in response.iter_content(CHUNK_SIZE):
                                if chunk:
                                    file.write(chunk)           
                    except Exception:
                        print("already exist or already delete")

        return
#=======================================================================================
