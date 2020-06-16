from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# from apiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

base_query = "'%s' in parents"


def retaining_folder_structure(query):
    results = DRIVE.files().list(fields="nextPageToken, files(id, name, kind, mimeType)", q=query).execute()
    items = results.get('files', [])
    sub_folders = []
    for item in items:
        sub_folders.append({"id": item['id'], "name": item['name'], "type": item['mimeType']})
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            query = base_query % item["id"]
            sub_folders[-1]["sub_folders"] = retaining_folder_structure(query)
    return sub_folders


folder_architecture = retaining_folder_structure(base_query % '1laP1s0Xz0qvRbOCCFNMZmFTLg1-oZOfD')  # function for running above code
print(folder_architecture)
