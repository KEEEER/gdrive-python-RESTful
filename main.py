from googledriver.token_refresher import refresh
from googledriver.metadata import Metadata
from googledriver.processor import Processor
from googledriver.read_properties import read
import requests
import os

client_id = "fill"
client_secret = "fill"
refresh_token = "fill"
database = 'https://www.googleapis.com/drive/v3/files'

# (v)issue 01 : write read local.properties function
# (v)issue 02 : merge metadata class from use three instruction to get path reduce to only one instruction
# (v)issue 03 : make every folder-type file's path end up adding '/' 
# (v)issue 04 : create Metadata class now need only access_token
# (v)issue 05 : rename 'edit_date_saver' to 'edit_date_save'
# issue 06 :

def main():

    to_path = "your download path"
    
    meta_list = read('local.properties')
    client_id = meta_list['client_id']
    client_secret = meta_list['client_secret']
    refresh_token = meta_list['refresh_token']

    print("step1 ------> set access_token")
    access_token = refresh(client_id , client_secret , refresh_token)
    metadata = Metadata(access_token)

    print("step2 ------> get metadata")
    file_metadatas = metadata.get_data_with_path()

    print("step3 ------> find edited items")
    edited_files_metadatas = metadata.get_edited_files(file_metadatas)

    print("step4 ------> save item edit date")
    metadata.save_edit_date(file_metadatas)

    print("step5 ------> create folders")
    processor = Processor(edited_files_metadatas)
    processor.create_folders(to_path)

    print("step6 ------> download files")
    processor.download_files(access_token , to_path)

    print("step7 ------> update complete!")
if __name__ == '__main__':
  main()
