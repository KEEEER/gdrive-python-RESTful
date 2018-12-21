from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from oauth2client.client import GoogleCredentials


import json
import os

import argparse
import httplib2
import urllib.request

token = ""
client_id = ""
client_secret = ""
refresh_token = ""

def auth(tokens , scopes):
    credentials = Credentials(tokens,refresh_token,None,None,client_id,client_secret,None)
    return credentials
def refresh():
    cred = GoogleCredentials(None,client_id,client_secret,
                                          refresh_token,None,"https://accounts.google.com/o/oauth2/token",None)
    http = cred.authorize(httplib2.Http())
    cred.refresh(http)
    return cred

def get_authorized_session(newCred):
    scopes=['https://www.googleapis.com/auth/photoslibrary',
            'https://www.googleapis.com/auth/photoslibrary.sharing',
            'https://www.googleapis.com/auth/drive']

    cred = auth(newCred.access_token , scopes)
    session = AuthorizedSession(cred)
    print(type(session))
    return session

def get(session , appCreatedOnly=False):
    params = {
            
    }
    while True:
        print("hello world!")
        driver = session.get('https://www.googleapis.com/drive/v3/files/', params=params).json()
        if 'files' in driver:
            for b in driver["files"]:
                print(b["id"])
                yield b


            if 'nextPageToken' in driver:
                params["pageToken"] = driver["nextPageToken"]
            else:
                return

        else:
            return

def main():
    newCred = refresh()
    session = get_authorized_session(newCred)
    for b in get(session):
        #dlPath = 'https://www.googleapis.com/drive/v3/files/' + b["id"] + '?alt=media&access_token=' + newCred.access_token
        dlPath = 'https://www.googleapis.com/drive/v3/files/' + b["id"] + '?alt=media'
        
        if b["mimeType"] == "application/vnd.google-apps.spreadsheet":
            print("File type is spreadsheet. Skip download it.")            
        else:
            temp = session.get(dlPath)
            print("downloading : " + b["name"])
            print(b["name"]  , " |and|  " , b["mimeType"])
            fileName = b["name"]
            for s in range(len(fileName)) :
                if fileName[s] == '/':
                    name = list(fileName)
                    name[s] = '／'
                    fileName = "".join(name)

                
            fileStorePath = "C:/Users/user/Desktop/google photo/python/gdrive-download/dl-files/"
            file = open(fileStorePath + fileName , "wb")
            file.write(temp.content)
            file.close()
if __name__ == '__main__':
  main()
