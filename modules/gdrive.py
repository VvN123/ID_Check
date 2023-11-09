from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# SI SE MODIFICAN LOS SCOPES DE DEBE BORRAR EL TOKEN.JSON
SCOPES = ['https://www.googleapis.com/auth/drive']

def auth():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\VvN\Desktop\Mega\Vicente\Python\Project_ID\ID_Check\data\drive\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def upload_to_gd(path_to_src_file, save_name):
    file_metadata = {'name': save_name,'parents':['1idnCeKNnvn9fEwrMnEfJtizUSborJ54K']}
    media = MediaFileUpload(path_to_src_file,
                                mimetype='image/jpg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get("id")

def recuperar_pendientes():
    list_recuperadas = []
    try:
        files = []
        page_token = None
        while True:
            response = service.files().list(q="mimeType='image/jpeg' and parents in '1idnCeKNnvn9fEwrMnEfJtizUSborJ54K'",
                                            spaces='drive',
                                            fields='nextPageToken, '
                                                    'files(id, name)',
                                            pageToken=page_token).execute()
            for file in response.get('files', []):
                list_recuperadas.append((file.get("name"),file.get("id")))
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None
    return list_recuperadas

creds = auth()
service = build('drive', 'v3', credentials=creds)





















