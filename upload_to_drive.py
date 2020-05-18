import pprint
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_or_create_folder(folder_name, parent, drive_service):
    folders = drive_service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and '{parent}' in parents"
    ).execute()
    
    if len(folders['files']) == 0:
        print(f"Creating Folder {folder_name}")
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent]
        }

        folder = drive_service.files().create(
            body=folder_metadata,
            fields='id, name'
        ).execute()
        return (folder.get('id'), folder.get('name'))
    else:
        print(f"{folder_name=} already exists")
        pprint.pprint(folders)
        return (folders['files'][0]['id'], folders['files'][0]['name'])

def export_to_folder(folder_structure, file_path, mime_type="text/csv"):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive']

    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    folders = folder_structure.split('/')
    curr_parent = 'root'
    folder_id = 'root'
    for sub_dir in folders:
        print(f"adding {sub_dir=} to {curr_parent=}, {folder_id=}")
        folder_id, curr_parent = get_or_create_folder(sub_dir, folder_id, service)

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    print(f"FIle ID: {file.get('id')}")


filename="sample"
clean_file = f"./data/{filename}/clean.csv"
dirty_file = f"./data/{filename}/incomplete.csv"
export_to_folder(f"try_again_munge/{filename}", clean_file, "text/csv")
export_to_folder(f"try_again_munge/{filename}", dirty_file, "text/csv")