from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive']


# def main():
"""Shows basic usage of the Slides v1 API.
"""


#--------GSUITE Access-------------------------

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
        print("Refreshing may cause error. If you have existing creds but are getting a refresh error, try deleting them so new creds will be generated and stored")
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

#--------Sheets Access-------------------------

sheets_service = build('sheets', 'v4', credentials=creds)


# Matlab Sim Output
spreadsheet_id = "1zYhxw0cgixufa7rebq_MpbsxcVRX0SZbtALCIbQWUqA"
ranges = ["Sheet1!A1:Q121"]

# True if grid data should be returned.
# This parameter is ignored if a field mask was set in the request.
include_grid_data = True

request = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response = request.execute()


data = []

rowData = response['sheets'][0]['data'][0]['rowData']


# iterate over each row, and if cell dict has 'formattedValue' key, that is the actual text we care about
for rowNum, row in enumerate(rowData):
    for colNum, item in enumerate(row['values']):
        if 'formattedValue' in item.keys():
            val = item['formattedValue']
            if rowNum == 0:
                data.append({'title':val, 'values':[]})
            else:
                data[colNum]['values'].append(val)
                
                
for thing in data:
    print(f"{thing['title']} - {len(thing['values'])} values")



# if __name__ == '__main__':
#     main()
