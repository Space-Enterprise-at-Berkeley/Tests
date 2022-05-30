from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from pprint import pprint

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive']


# def main():
"""Shows basic usage of the Sheets v4 API.
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
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)




# --------------------------------------------------

sheets_service = build('sheets', 'v4', credentials=creds)

# For company links
# The spreadsheet to request.
# spreadsheet_id = '1zm2wblOg5R3g4CjgJ3ppR0bpQOYG_eDyecNh6tuoooQ'  # TODO: Update placeholder value.
# The ranges to retrieve from the spreadsheet.
# ranges = ["Website Links Raw!A2:J123"]

# For company sorting
spreadsheet_id = "1ctNdb_Qn29jL6V6m2Zr1qDmLklTpr9UbyPDnuFcrN_s"
ranges = ["Website Links Raw!A2:I40"]

# True if grid data should be returned.
# This parameter is ignored if a field mask was set in the request.
include_grid_data = True  # TODO: Update placeholder value.


request = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
response = request.execute()

# TODO: Change code below to process the `response` dict:
# pprint(response)

data = []
for i,row in enumerate(response['sheets'][0]['data'][0]['rowData']):
    line = []
    for j,item in enumerate(row['values']):
        pair = []
        if 'formattedValue' in item.keys():
            name = item['formattedValue']
            pair.append(name)
            pair.append('') # set as default for second item, and only override if there is a separate hyperlink
            if "hyperlink" in item.keys():
                link = item["hyperlink"]
                if name != link:
                    pair[1] += item['hyperlink']
            line.append(pair)
        else:
            if j < 4:  # make sure there is a correct spacer for first 4 vals if it is empty
                line.append(['',''])
    data.append(line)
