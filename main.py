from googledriver.token_refresher import refresh
from googledriver.metadata import Metadata
from googledriver.processor import Processor

import httplib2
import requests
import os

client_id = "fill"
client_secret = "fill"
refresh_token = "fill"
database = 'https://www.googleapis.com/drive/v3/files'

metadata_list = {}

params = {
        'access_token' : "no",
        'fields' : "*"
}

def read_properties(name):
    global client_id , client_secret , refresh_token
    with open(name) as f:
        for line in f:
            if '=' in line:
                name, value = line.split("=", 1)
                name = name.strip()
                value = value.strip()
                if 'client_id' == name:
                    client_id = str(value)            
                if 'client_secret' == name:
                    client_secret = str(value)                    
                if 'refresh_token' == name:
                    refresh_token = str(value)                 
    f.close()
    return

def main():
    to_path = "C:/Users/user/Desktop/google photo/python/gdrive-download/dl-folders_and_files"

    read_properties('local.properties')
    access_token = refresh(client_id , client_secret , refresh_token)
    params['access_token'] = access_token

    print("step1 ------> create Metadata Object")
    metadata = Metadata(params)

    print("step2 ------> get metadata Ids and get all metadatas")
    files = metadata.get_user_data_info()
    roots = metadata.get_data_root(files)
    files = metadata.get_full_data_with_path(roots)

    print("step3 ------> find edited items")
    edited_files = metadata.get_edited_files(files)

    print("step4 ------> save item edit date")
    metadata.save_edit_date(files)

    print("step5 ------> create folders")
    processor = Processor(edited_files)
    processor.create_folders(to_path)

    print("step6 ------> download files")
    processor.download_files(params['access_token'] , to_path)

    print("step7 ------> update complete!")
if __name__ == '__main__':
  main()
