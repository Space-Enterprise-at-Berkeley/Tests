from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive']

def pt(size):
    return {
        'magnitude': size,
        'unit': 'PT'
    }

def create_text_shape(page_id,element_id,text,type,x,y):
    type = type.lower()
    if "text" in type:
        width_factor = 15
    elif type == "title":
        width_factor = 18
    return  {
            'createShape': {
                'objectId': element_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': pt(35),
                        'width': pt(width_factor*len(text))
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': x,
                        'translateY': y,
                        'unit': 'PT'
                    }
                }
            }
        }

def insert_text(element_id,text):
    return {
        'insertText': {
            'objectId': element_id,
            'insertionIndex': 0,
            'text': text
        }
    }

def style_text(element_id,target_type,target):
    if "page" in target_type.lower():
        target_type = "pageObjectId"
    elif target_type.lower() == "url":
        target_type = "url"

    return {
        'updateTextStyle': {
            'objectId': element_id,
            'fields': 'link,foregroundColor,underline,fontFamily,fontSize',
            'style': {
              "foregroundColor": {
                "opaqueColor": {
                  "themeColor": "HYPERLINK"
                }
              },
              "link": {
                target_type: target
              },
              "underline": True,
              'fontFamily': 'Lato',
              'fontSize': {
                'magnitude': 18,
                'unit': 'PT'
              }
            }
        }
    }

def style_title(element_id):

    return {
        'updateTextStyle': {
            'objectId': element_id,
            'fields': 'fontFamily,fontSize,foregroundColor,bold',
            'style': {
              'foregroundColor': {
                "opaqueColor": {
                    "rgbColor": {
                        "blue": 1,
                        "green": 1,
                        "red": 1
                    }
                }
              },
              'fontFamily': 'Playfair Display',
              'fontSize': {
                'magnitude': 32,
                'unit': 'PT'
              },
              'bold': True
            }
        }
    }

def create_text(company,text,type,url=None,x=100,y=100,id=1):
    type = type.lower()
    page_id = company_id(company)
    element_id = "{}_{}_{}".format(page_id,type,id)
    if type == "text_page_ref":
        target_type = "page"
        target = url
    elif type == "text":
        target_type = "url"
        target = url


    commands = [create_text_shape(page_id,element_id,text,type,x,y),
            insert_text(element_id,text)]
    if "text" in type:
        commands.append(style_text(element_id,target_type,target))
    elif type == "title":
        commands.append(style_title(element_id))
    return commands

def delete_text(element_id):
    return {
        'deleteObject': {
            'objectId': element_id
        }
    }

def create_company_slide(company,idx=1):
    # Not sure how to get existing layoutId
    page_id = company_id(company)
    return {
        'createSlide': {
            'objectId': page_id,
            'insertionIndex': idx,
            'slideLayoutReference': {
                'predefinedLayout': "TITLE_AND_BODY"
            }
        }
    }

def create_image(company,url,x=500,y=300):
    page_id = company_id(company)
    element_id = "{}_image".format(page_id)
    return {
        'createImage' : {
            'objectId': element_id,
            'elementProperties': {
                'pageObjectId': page_id,
                'size': {
                    'height': pt(210),
                    'width': pt(210)
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': x,
                    'translateY': y,
                    'unit': 'PT'
                }
            },
            'url': url
        }
    }


def send_commands(slides_service,commands, presentation_id):
    # Execute the request.
    body = {
        'requests': commands
    }
    response = slides_service.presentations().batchUpdate(presentationId=presentation_id, body=body).execute()


def company_id(company):
    ret = "_".join(company.split(" "))
    ret = ret.replace("(","_")
    ret = ret.replace(")","_")
    ret = ret.replace(".","_")
    ret = ret.replace("&","_")
    if len(ret) < 5:
        ret += (5-len(ret))*"_"
    return ret


def main():
    """Shows basic usage of the Slides v1 API.
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

    #------------------------

    company_names = []
    company_links = {}
    company_id_to_name = {}

    with open("Company Contacts - Website Links.csv","r") as f:
        data = f.read().splitlines()
        for row in data[1:]:
            vals = row.split(",")
            if len(vals[0]) > 0 and len(vals[1]) > 0:
                company_names.append(vals[0])
                company_id_to_name[company_id(vals[0])] = vals[0]
                company_links[vals[0]] = vals[1:]
                if len(vals[4]) == 0:
                    company_links[vals[0]][4] = None #indicate that there is no image
    company_names.sort()
    #------------

    #--------Sheets Access-------------------------

    sheets_service = build('sheets', 'v4', credentials=creds)

    # The spreadsheet to request.
    # spreadsheet_id = '1zm2wblOg5R3g4CjgJ3ppR0bpQOYG_eDyecNh6tuoooQ'
    # The ranges to retrieve from the spreadsheet.
    # For company links
    # ranges = ["Website Links Raw!A2:J123"]
    # For Resources
    # ranges = ["Sector Information!A2:J10"]

    # For company categorization
    spreadsheet_id = "1ctNdb_Qn29jL6V6m2Zr1qDmLklTpr9UbyPDnuFcrN_s"
    ranges = ["Copy of Refined!A1:AN9"]

    # True if grid data should be returned.
    # This parameter is ignored if a field mask was set in the request.
    include_grid_data = True


    request = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=ranges, includeGridData=include_grid_data)
    response = request.execute()


    data = {}
    columns = []
    for i,row in enumerate(response['sheets'][0]['data'][0]['rowData']):
        line = []

        for j,item in enumerate(row['values']):
            pair = []
            if 'formattedValue' in item.keys():
                name = item['formattedValue']
                line.append(name)
                pair.append('') # set as default for second item, and only override if there is a separate hyperlink
                # if "hyperlink" in item.keys():
                #     link = item["hyperlink"]
                #     if name != link:
                #         pair[1] += item['hyperlink']
                # # line.append(pair)
            else:
                if j < 4:  # make sure there is a correct spacer for first 4 vals if it is empty
                    line.append(['',''])
        company = line[0]
        company2 = company + " Sector 2"
        company += " Sector"

        line = line[1:]
        line.sort()

        # company_id_to_name[company_id(company)] = company
        if len(line) <= 24:
            data[company_id(company)] = line
        else:
            data[company_id(company)] = line[:24]
            data[company_id(company2)] = line[24:]



    company_names = list(data.keys())
    # company_names.sort()

    print(len(company_names))
    table_of_contents_num = (len(company_names)//14) + 1
    toc_names = []
    # for i in range(table_of_contents_num):
    #     toc_names.append(company_id("Table of Contents:{}".format(i)))
    toc_names = company_names
    companies = toc_names

    print(toc_names)

    return

if __name__ == '__main__':
    main()

'''
#-------Slides Access

# Old rough draft
# PRESENTATION_ID = "1LrqQOmD8PUw4O7HhhNXsLFVCFu7WN2TXgk-VIW4n3Vg"

# # Version with new theme
# PRESENTATION_ID = "18IorK8GV8RMiHzh7KigX4Cs8Ja2VZbt7wjyXMc8cqPQ"

# Testing version
# PRESENTATION_ID = "1aMx5shEGRfmS0-uYusqgAjO58UhmV2qN-jd1ZGgTZrQ"
PRESENTATION_ID = "1JjjovB9SR4arfNR_313UAXq0NmBCh1vyWzjA64sXdoE"




slides_service = build('slides', 'v1', credentials=creds)

# companies = ["Blue Origin"]
# company_links = {"Blue Origin":["https://www.blueorigin.com/","https://www.blueorigin.com/our-mission","https://www.blueorigin.com/careers","https://cdn.geekwire.com/wp-content/uploads/2016/10/161024-blue-origin-feather-300x180.jpg"]}

# requests = [create_company_slide("Blue Origin",4)]
# requests2.extend(create_text("Blue Origin","testing",type="text",x=100,y=150))
# requests2.extend(create_text("Blue Origin","Blue Origin",type="title",x=100,y=75))

requests = []
idx = 2
for company in companies:
    requests += [create_company_slide(company,idx)]
    idx += 1
print(companies)

# Execute the request.
body = {
    'requests': requests
}
response = slides_service.presentations().batchUpdate(presentationId=PRESENTATION_ID, body=body).execute()


# send_commands(slides_service,PRESENTATION_ID, requests)

#------------------------
# Clean up created slides & add text links
# Access updated version of slides
presentation = slides_service.presentations().get(presentationId=PRESENTATION_ID).execute()
slides = presentation.get("slides")

titles = ["Website Homepage","Company Overview","Career Page"]
requests = []
print('The presentation contains {} slides:'.format(len(slides)))
toc_company_idx_offset = 0
for i, slide in enumerate(slides):
    print('- Slide #{} contains {} elements.'.format(
        i + 1, len(slide.get('pageElements'))))
    if i > 0 and len(slide["pageElements"]) > 1:
        title_obj = slide["pageElements"][0]["objectId"]
        text_obj = slide["pageElements"][1]["objectId"]
        commands = [] #[delete_text(text_obj)]
        company_idx = 0
        if slide["objectId"] in company_id_to_name.keys():
            pass
            # company = company_id_to_name[slide["objectId"]]
            # links = data[company]
            # commands += [insert_text(title_obj,company)]
            # for i in range(3):
            #     if links[i][0] != '':
            #         commands += create_text(company,titles[i],url=links[i][0],type="text",x=35,y=120+i*60,id=i)
            # # commands += [create_text(company,"Website Homepage",url=links[0][0],type="text",x=35,y=120,id=0),
            # #             create_text(company,"Company Overview",url=links[1][0],type="text",x=35,y=180,id=1),
            # #             create_text(company,"Career Page",url=links[2][0],type="text",x=35,y=240,id=2)]
            # # if len(links) > 4:
            # for j,item in enumerate(links[3:]):
            #     if item[1] == '':
            #         print(item)
            #     commands += [create_text(company,item[0],url=item[1],type="text",x=335,y=120 + 42*j,id=(3+j))]
            #
            # # if links[4] != None:
            # #         print("Creating an image for {}".format(company))
            # #         commands += [create_image(company,links[3],x=330,y=100)]
        elif slide["objectId"] in toc_names:
            commands += [delete_text(text_obj)]
            name = slide["objectId"].split("_")[0]
            if "2" in slide["objectId"]:
                name += " (cont.)"
            commands += [insert_text(title_obj,name)]
            print(slide["objectId"])
            company_people = data[slide["objectId"]]
            idx = 0
            for i in range(3):
                for j in range(8):
                    loc = toc_company_idx_offset+idx
                    if idx < len(company_people):
                        x = 35 + 200*i
                        y = 100 + j*35
                        company = company_people[idx]
                        commands += create_text(slide["objectId"],company,url=company_id(company),type="text_page_ref",x=x,y=y,id=idx)
                        idx += 1
            print(idx)
            toc_company_idx_offset += 14
        requests += commands


body = {
    'requests': requests
}
response = slides_service.presentations().batchUpdate(presentationId=PRESENTATION_ID, body=body).execute()

'''






#----------------Old Stuff------------------
'''
# Create a new square textbox, using the supplied element ID.
page_id = "ga66c04ea02_0_59"
element_id = 'MyTextBox_01'
pt350 = {
    'magnitude': 350,
    'unit': 'PT'
}
text = "Blue Origin SUCKSSS"
requests = [
    {
        'createShape': {
            'objectId': element_id,
            'shapeType': 'TEXT_BOX',
            'elementProperties': {
                'pageObjectId': page_id,
                'size': {
                    'height': pt(35),
                    'width': pt(12*len(text))
                },
                'transform': {
                    'scaleX': 1,
                    'scaleY': 1,
                    'translateX': 100,
                    'translateY': 100,
                    'unit': 'PT'
                }
            }
        }
    },

    # Insert text into the box, using the supplied element ID.
    {
        'insertText': {
            'objectId': element_id,
            'insertionIndex': 0,
            'text': text
        }
    },
    {
        'updateTextStyle': {
            'objectId': element_id,
            'fields': 'link,foregroundColor,underline,fontFamily,fontSize',
            'style': {
              "foregroundColor": {
                "opaqueColor": {
                  "themeColor": "HYPERLINK"
                }
              },
              "link": {
                "pageObjectId": "ga66c04ea02_0_69"
              },
              "underline": True,
              'fontFamily': 'Lato',
              'fontSize': {
                'magnitude': 18,
                'unit': 'PT'
              }
            }
        }
    },
    style_text(element_id,"page","ga66c04ea02_0_69")
]
'''