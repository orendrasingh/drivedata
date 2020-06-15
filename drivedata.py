from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import os, io
# from apiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

def retaining_folder_structure(query):
    # global cousre
    # print(query)
    list=[]
    results = DRIVE.files().list(fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
    items = results.get('files', [])
    for item in items:

        if(item['mimeType'] == 'application/vnd.google-apps.folder'):
            print(item['name'])
            print(item['id'])
            list.append({"id":item['id'],"name":item['name'],"type":item['mimeType']})  #first append to the list
            query="'%s' in parents"%(item["id"])
            def retaining_folder_structure(query, list):
                results = DRIVE.files().list(fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
                items = results.get('files', [])
                for item in items:
                    if (item['mimeType'] == 'application/vnd.google-apps.folder'):
                        print(item['name'])
                        print(item['id'])
                        length_of_list=len(list)-1
                        list[length_of_list]["folders"]=[{"id":item['id'],"name":item['name'],"type":item['mimeType']}] #check if user have internt folder then it will create folders key in the list item we appended
                        query = "'%s' in parents" % (item["id"]) #passing the folder id into the another loop
                        def retaining_folder_structure(query, list):
                            results = DRIVE.files().list(fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
                            items = results.get('files', [])
                            for item in items:
                                if (item['mimeType'] == 'application/vnd.google-apps.folder'):
                                    length_of_list = len(list) - 1
                                    list[length_of_list]["folders"] = [{"id": item['id'], "name": item['name'], "type": item['mimeType']}]
                                    query = "'%s' in parents" % (item["id"])
                                    print(list)
                                else:
                                    length_of_list = len(list) - 1
                                    list[length_of_list]["folders"]["files"] = [{"id": item['id'], "name": item['name'], "type": item['mimeType']}]
                                    # print(item['name'])
                                    # print(item['id'])
                    else:
                        length_of_list = len(list) - 1
                        list[length_of_list]["files"] = [{"id": item['id'], "name": item['name'], "type": item['mimeType']}]
                        # print(item['name'])
                        # print(item['id'])
            # print(True)
        else:
            print(item['name'])
            print(item['id'])

retaining_folder_structure("'1laP1s0Xz0qvRbOCCFNMZmFTLg1-oZOfD' in parents") # function for running above code
