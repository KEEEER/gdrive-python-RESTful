from oauth2client.client import GoogleCredentials

import httplib2
import requests
import os

client_id = ""
client_secret = ""
refresh_token = ""

def auth():
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

def downloadDriveItem(cred):
    
    # prepare access_token to use GET method
    params = {
        'access_token' : cred.access_token
    }

    #get all file metadatas
    metadata = requests.get('https://www.googleapis.com/drive/v3/files', params = params).json()
    #get item ids from metadatas    
    if 'files' in metadata:
        for item in metadata['files']:

            #this project down only files
            if item["mimeType"] == "application/vnd.google-apps.folder":
                continue
            
            #define download url
            url = 'https://www.googleapis.com/drive/v3/files/' + item["id"] + '?alt=media&access_token=' + cred.access_token 

            #Http GET
            responds = requests.get(url)

            #Check if fileName is valid
            fileName = fileNameCheck(item["name"])
            print("downloading : " + fileName)

            #download files to specified location
            fileStorePath = "C:/Users/user/Desktop/google photo/python/gdrive-download/dl-files/"
            if item["mimeType"] == "application/vnd.google-apps.spreadsheet":
                file = open(fileStorePath + fileName , "w")
                file.write(responds.text)
            else :
                file = open(fileStorePath + fileName , "wb")
                file.write(responds.content)
            file.close()
    return "error : cant get Ids!"

def main():
    newCred = auth()
    newCred = refresh(newCred)
    downloadDriveItem(newCred)
  #  dlPath = 'https://www.googleapis.com/drive/v3/files/' + ids + '?alt=media&access_token=' + newCred.access_token
  #  responds = requests.get(dlPath)
   

if __name__ == '__main__':
  main()
