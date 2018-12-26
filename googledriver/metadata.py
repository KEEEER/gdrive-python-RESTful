import requests
import os.path

database = 'https://www.googleapis.com/drive/v3/files'

#Class==================================================================================
class Metadata:
    def __init__(self , params):
        self.params = params
        paramst = params

    def get_user_data_info(self):
        datas=[]
        metadata = requests.get(database , params = self.params).json()
        for item in metadata['files']:
            datas.append(item.copy())
        return datas

    def get_data_root(self , metadata):
        roots=[]
        ids={}
        for item in metadata:
            ids[item['id']] = item['name']
        for item in metadata:
            if 'parents' in item:
                for parents in item['parents']:
                    if not parents in ids:
                        parentsItem = requests.get(database + '/' + parents , params = self.params).json()                       
                        if not 'parents' in parents:
                            roots.append(parentsItem.copy())
                        ids[parentsItem['id']] = parentsItem['name']
        return roots

    def get_full_data_with_path(self , roots):
        full_data=[]
        for root in roots:
            _get_data_and_path_from_root(root , full_data , '/' + root['name'] , self.params)
        return full_data

    def get_edited_files(self , metadatas):
        file = "edit_date_saver.txt"
        edited_files = []
        last_edit_date = {}
        if not os.path.isfile(file):
            print("first download!!!")
            return metadatas
        f = open(file , 'r')
        for line in f:
            if ',' in line:                    
                item_id , item_date = line.split(",", 1)
                item_id = item_id.strip()
                item_date = item_date.strip()
                last_edit_date[item_id] = item_date                                 
        f.close()
        for item in metadatas:
            if not item['id'] in last_edit_date:
                edited_files.append(item.copy())
            else:
                if not item['modifiedTime'] == last_edit_date[item['id']]:
                    edited_files.append(item.copy())
        for item in edited_files:
            print("new edit : " + item['name'])
        return edited_files

    def save_edit_date(self , metadata):
        file = "edit_date_saver.txt"
        f = open(file , "w")
        for item in metadata:
            f.write(item['id'] + "," + item['modifiedTime'])
            f.write('\n')
        f.close()
        return

#=======================================================================================

def _get_data_and_path_from_root(root , fill_list , path , params):

    query = "?q='{}' in parents".format(root['id'])
    children = requests.get(database + query , params = params).json()
    for child in children['files']:
        child_name = _fileNameCheck(child['name'])
        child['path'] = path + '/' + child_name
        fill_list.append(child.copy())
        if child['mimeType'] == "application/vnd.google-apps.folder":       
            _get_data_and_path_from_root(child , fill_list , path + '/' + child_name , params)
    return

def _fileNameCheck(fileName):
    for s in range(len(fileName)) :
        if fileName[s] == '/':
            name = list(fileName)
            name[s] = '／'
            fileName = "".join(name)
        if fileName[s] == ':':
            name = list(fileName)
            name[s] = '：'
            fileName = "".join(name)
    return fileName