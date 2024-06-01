from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

link=["https://www.googleapis.com/auth/spreadsheets"]

id="1JC8fkFlf2VQTLvgoxAl_51OWesmHjgQnuMUAeVBRjhs"

def append_csv(nombre_casa,arr):

    creds=None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", link)
    
    if(not creds or not creds.valid):
        
        if creds and creds.expired and creds.refresh_token: creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", link
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:

        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        for i in arr:
        
            sheet.values().append(spreadsheetId=id,
                range=f'{nombre_casa}!A1',
                valueInputOption="USER_ENTERED",
                body={"values": [i]}).execute()

    except:
        pass
