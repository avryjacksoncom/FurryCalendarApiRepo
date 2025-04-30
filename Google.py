
# Google funtions like uploading a photo and video to the drive
# Uploading an event to the google calendar
# and some other helper functions.

#create service for google drive api
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

#upload photo and video to  google drive api
from googleapiclient.http import MediaFileUpload

#for file searching in the google drive
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# to get the latest file used in media download
import random
import time
import os.path


SCOPES = ["https://www.googleapis.com/auth/calendar"]

class Google:
    def __init__(self):
        pass

#Google Drive Api Service
    def Create_Service(self,client_secret_file, api_name, api_version, *scopes):

        print(client_secret_file, api_name, api_version, scopes, sep='-')
        CLIENT_SECRET_FILE = client_secret_file
        API_SERVICE_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scope for scope in scopes[0]]
        print(SCOPES)

        cred = None

        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
        # print(pickle_file)

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None


#Upload photo from telegram message to Google drive
    def uploadToGoogleDrive(self,photoFileArr,structEvent,clientSecret,folderId):
        photoFileName = photoFileArr[0]
        mediaFileName = structEvent[0]
        #GOOGLE DRIVE API SCOPE AND INFO FOR GOOGLE DRIVE SERVICE
        CLIENT_SECRET_FILE = clientSecret
        API_NAME = 'drive'
        API_VERSION = 'v3'
        DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

        service = self.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,DRIVE_SCOPES)

        folder_id = folderId
        file_names = [mediaFileName]
        mime_types = ['image/jpeg']

        for file_name, mime_type in zip(file_names, mime_types):
            file_metadata = {
                'name': mediaFileName,
                'parents': [folder_id]
            }

            # media = MediaFileUpload(f'{file_name}', mimetype=mime_type)
            media = MediaFileUpload(f'{photoFileName}', mimetype=mime_type)
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

    """Search file in drive location

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    def search_file(self,clientSecret):

        CLIENT_SECRET_FILE = clientSecret
        API_NAME = 'drive'
        API_VERSION = 'v3'
        DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]
        service = self.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,DRIVE_SCOPES)

        try:
            # create drive api client
            files = []
            page_token = None

            while True:
                # pylint: disable=maybe-no-member
                response = (
                    service.files()
                    .list(
                        q="mimeType='image/jpeg'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )

                for file in response.get("files", []):
                    # Process change
                    print(f'Found file: {file.get("name")}, {file.get("id")}')
                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)

                if page_token is None:
                    break

        except HttpError as error:
            print(f"An error occurred: {error}")
            files = None

        return files


    def getGoogleDriveLink(self,clientSecret):
        driveFile = self.search_file(clientSecret)
        # print("THIS IS MY DRIVE FILE?", driveFile)
        first_id = driveFile[0]['id']
        name_id = driveFile[0]['name']
        # print("THIS IS THE DRIVE FILE ID",first_id)
        link = "https://drive.google.com/file/d/" + first_id + "/view"
        driveLinkArr = []
        driveLinkArr.append(first_id)
        driveLinkArr.append(name_id)
        driveLinkArr.append(link)
        return driveLinkArr

    """

    Uploading a video to google Drive

    """  

    def uploadToGoogleDriveMP4(self,photoFileArr,structEvent,clientSecret,folderId):
        photoFileName = photoFileArr[0]
        mediaFileName = structEvent[0]

        #GOOGLE DRIVE API SCOPE AND INFO FOR GOOGLE DRIVE SERVICE
        CLIENT_SECRET_FILE = clientSecret
        API_NAME = 'drive'
        API_VERSION = 'v3'
        DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

        service = self.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,DRIVE_SCOPES)

        folder_id = folderId
        file_names = [mediaFileName]
        mime_types = ['video/mp4']

        for file_name, mime_type in zip(file_names, mime_types):
            file_metadata = {
                'name': mediaFileName,
                'parents': [folder_id]
            }

            # media = MediaFileUpload(f'{file_name}', mimetype=mime_type)
            media = MediaFileUpload(f'{photoFileName}', mimetype=mime_type)
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

    """

        Uploading a gif to google Drive

    """  

    def uploadToGoogleDriveGIF(self,photoFileArr,structEvent,clientSecret,folderId):
        photoFileName = photoFileArr[0]
        mediaFileName = structEvent[0]

        #GOOGLE DRIVE API SCOPE AND INFO FOR GOOGLE DRIVE SERVICE
        CLIENT_SECRET_FILE = clientSecret
        API_NAME = 'drive'
        API_VERSION = 'v3'
        DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

        service = self.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION,DRIVE_SCOPES)

        folder_id = folderId
        file_names = [mediaFileName]
        mime_types = ['image/gif']

        for file_name, mime_type in zip(file_names, mime_types):
            file_metadata = {
                'name': mediaFileName,
                'parents': [folder_id]
            }

            # media = MediaFileUpload(f'{file_name}', mimetype=mime_type)
            media = MediaFileUpload(f'{photoFileName}', mimetype=mime_type)
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()


    def toGoogleCalendar(self,eventArray,drivePhotoArr,tokenFile,credentialJson):
  
        furryUsPrompt = "MESSAGE PROMPT FOR THE DESCRIPTION IN EVENT"
        summary = eventArray[0]
        location = eventArray[1]
        description = eventArray[2]
        eventTimeNotSpecified = eventArray[3]
        startTime = eventArray[4]
        endTime = eventArray[5]
        descriptionAndPrompt = description + furryUsPrompt

        if drivePhotoArr:
              fileId = drivePhotoArr[0]
              fileName = drivePhotoArr[1]
              fileIdMedia = drivePhotoArr[2]
        else:
              fileId = ""
              fileName = ""
              fileIdMedia = ""

        creds = None

        if os.path.exists(tokenFile):
          creds = Credentials.from_authorized_user_file(tokenFile, SCOPES) # type: ignore
        if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
          else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialJson, SCOPES  # type: ignore
      
            )
            creds = flow.run_local_server(port=0)
          with open("token.json", "w") as token:
            token.write(creds.to_json())

        try:
          time.sleep(2)
          service = build("calendar", "v3", credentials=creds)

          random_color_id = str(random.randint(1, 11))

          if eventTimeNotSpecified == "Y":
              event = {
                  'summary': summary,
                  'location': location,
                  'description': descriptionAndPrompt,
                  'start': {
                      'date': startTime,
                  },
                  'end': {
                      'date': endTime,
                  },
                  'colorId': random_color_id,
                  'attachments': [
                      {
                          'fileUrl': fileIdMedia,  # URL to the file
                          'title': fileName , # Display name of the attachment
                          'mimeType': 'image/jpeg',
                          'fileId':fileId
                      }

                  ]
              }  

          else:
              event = {
                  'summary': summary,
                  'location': location,
                  'description': descriptionAndPrompt,
                  'start': {
                      'dateTime': startTime,
                  },
                  'end': {
                      'dateTime': endTime,
                  },
                  'colorId': random_color_id,
                  'attachments': [
                      {
                          'fileUrl': fileIdMedia,  # URL to the file
                          'title': fileName , # Display name of the attachment
                          'mimeType': 'image/jpeg',
                          'fileId':fileId

                      }

                  ]
              }


          print("---------------------------------------------------------------------------------------------------------------")
          print("Now calling Google Api please wait.....")
          time.sleep(2)
          # Change the "eevnet" to event to insert event in google calendar
          event = service.events().insert(calendarId='primary', body=event,supportsAttachments=True).execute()
          print("Event Status Below: ")
          print()
          print(f"Event created: {event.get('htmlLink')}")
          print()

        except HttpError as error:
          print(f"An Http error occurred: {error}")