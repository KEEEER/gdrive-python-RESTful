from oauth2client.client import GoogleCredentials

import httplib2
import requests
import os

client_id = "fill"
client_secret = "fill"
refresh_token = "fill"
database = 'https://www.googleapis.com/drive/v3/files'
downloadTo = "C:/Users/user/Desktop/google photo/python/gdrive-download/dl-folders_and_files"
metadata_list = {}
params = {
        'access_token' : "no",
        'fields' : "*"
}
headers ={
    'Authorization' : 'Bearer '
}
def auth():
    print(refresh_token)
    credentials = GoogleCredentials(None,client_id,client_secret,
                                          refresh_token,None,"https://accounts.google.com/o/oauth2/token",None)
    return credentials

def refresh(cred):
    http = cred.authorize(httplib2.Http())
    cred.refresh(http)
    return cred

def fileNameCheck(fileName):
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

def list_files_path(item , path):
    metadata_list[item['name']] = path
  #  print(path)
    #get children of this folder
    query = "?q='{}' in parents".format(item['id'])
    children = requests.get(database + query , params = params).json()

    #if not empty
    for child in children['files']:
        #if folder do DFS
        if child['mimeType'] == "application/vnd.google-apps.folder":         
            nextName = fileNameCheck(child['name']) 
            list_files_path(child , path + '/' + nextName)      
        #if not folder do make folder and download file       
        else:
            nextName = fileNameCheck(child['name'])
            metadata_list[nextName] = path + '/' + nextName

    return

def downloadDriveItem(cred):
    
    # prepare access_token to use GET method
    params['access_token'] = cred.access_token
    #headers['Authorization'] = cred.access_token
    metadata = requests.get(database , params = params).json()
    #metadata = requests.get(database , headers = headers).json()
        

    store = {}
    if 'files' in metadata:

        print("checking all files......")
        #get unhidden item id and name
        for item in metadata['files']:
            store[item['id']] = item['name']
            print(item['modifiedTime'])
        #get hidden items
        for item in metadata['files']:
            if 'parents' in item:
                for parents in item['parents']:
                    #if this item in google drive and not appears in LIST method
                    if not parents in store:
                        parentsItem = requests.get(database + '/' + parents , params = params).json()
                        store[parentsItem['id']] = parentsItem['name']
                        metadata['files'].append(parentsItem)          
        
        #find all files path
        for item in metadata['files']:
            if not 'parents' in item:
                if item['mimeType'] == "application/vnd.google-apps.folder":
                    
                    list_files_path(item , downloadTo)
    return "error : cant get Ids!"

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
    read_properties('local.properties')
    newCred = auth()
    newCred = refresh(newCred)
    downloadDriveItem(newCred)
    for k in metadata_list:
        print(k + " ------> " + metadata_list[k])

if __name__ == '__main__':
  main()
