from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from collections import Counter
import pandas as pd
import pkg.SC_config as cnf
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/spreadsheets.readonly']
# SCOPES=[]

def readUniList():
    ''' Read of current version of unilist (master list w each unique uniform ahd 
    person to whom it is assigned)
    '''
    sheetID ='14oedZ7BVwLP4VXMqlWnAg3nwvgW-keBfXCu17rTkNhk' # 
    rangeName = 'Unilist!A:I'
    # Read of current version of unilist from google sheets
    unilist = downloadSheet(sheetID, rangeName)
    def convDate(val):
        try:
            return datetime.strptime(val, '%m/%d/%Y')
        except:
            try:
                return datetime.strptime(val, '%m/%d/%y')
            except:
                print('Error converting', val)
                return val
    unilist['Date']=unilist['Date'].apply(lambda x: convDate(x))
    unilist['Number']=unilist['Number'].astype(int)
    return unilist

def readInventory():
    ''' Read results of recent inventories 
    '''
    sheetID ='14oedZ7BVwLP4VXMqlWnAg3nwvgW-keBfXCu17rTkNhk' # 
    rangeName = 'Inventory!A:E'
    inventory = downloadSheet(sheetID, rangeName)
    # Transform inventory into Setname, Size, Number, Date, Location =in
    
    grouped=inventory.groupby(['Setname','Size'])
    unis=[]
    for (sn, size), gr in grouped:
        # TODO keep only most recent version of inventory (by date)
        thisDate=gr.iloc[0]['Date']
        try:
            thisDate=datetime.strptime(thisDate,'%m/%d/%y')
        except:
            pass
        nums=gr.iloc[0]['Numberlist']
        if ',' in nums:
            nums=nums.split(',')
            try:
                nums=[int(i) for i in nums]
            except:
                # Maybe a trailing comma problem
                print('error for', nums)
        else:
            nums=[nums] # single valued list
        for num in nums:
            thisUni={'Setname':sn, 'Size':size, 'Number':num,'Date': thisDate,'Location':'in'}
            unis.append(thisUni)
    unis=pd.DataFrame(unis)  
    return unis

def getGoogleCreds():
    ''' Load and process credentials.json (generated by Google API)
    Enables creation of google Service object to access online google sheets
    
    '''

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    tokenFile=cnf._INPUT_DIR+'\\token.pickle'
    if os.path.exists(tokenFile):
        with open(tokenFile, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cnf._INPUT_DIR +
                '\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(tokenFile, 'wb') as token:
            pickle.dump(creds, token)
    return creds
 
def changeColNames(headers):
    ''' Transform column names (google form questions) to standard abbrev versions 
    after Google Sheets API file download
    
    '''
    # Find header entries (google form questions) that are duplicates
    dups = [k for k,v in Counter(headers).items() if v>1]
    for dup in dups:
        matchinds=[i for i, val in enumerate(headers) if val==dup]        
        # Replace 2nd instance in header list with val_2
        headers=[val if i !=matchinds[1] else val+'_2' for i, val in enumerate(headers) ]
    # handle duplicates
    renameDict={'Player First Name':'First','Player Last Name':'Last', 'Player Date of Birth':'DOB',
            'School Player Attends':'School', 'Grade Level':'Grade','Street Address':'Address',
            'Zip Code':'Zip','Parish of Registration':'Parish','Alternate Placement':'AltPlacement',
            'Other Roster Status':'Ocstatus', 'Other Contact':'Othercontact',
            'Parent/Guardian First Name':'Pfirst1', 'Parent/Guardian First Name_2':'Pfirst2',
            'Parent/Guardian Last Name':'Plast1','Parent/Guardian Last Name_2':'Plast2',
            'Primary Phone':'Phone1','Primary Phone_2':'Phone2','Textable':'Text1','Textable_2':'Text2',
            'Primary Email':'Email1','Primary Email_2':'Email2',
            'Would you be willing to act as a coach or assistant':'Coach',
            'Would you be willing to act as a coach or assistant_2':'Coach2',
            "Player's Uniform Size":'Unisize', 
            "Does your child already have an":'Unineed'}
    newNames=[]
    for val in headers:
        if val in renameDict:
            newNames.append(renameDict.get(val))
        else:
            newNames.append(val)
    unchanged=['Timestamp','Gender','Sport','Plakey','Famkey']
    # check for invalid header names
    validNames=list(renameDict.values()) + unchanged
    badNames=[i for i in newNames if i not in validNames]
    if len(badNames)>0:
        print('Invalid column names:',', '.join(badNames))
    return newNames

    
def downloadSignups(sheetID, rangeName):
    ''' Download all from current season's signups
    
    '''
    creds = getGoogleCreds() # google.oauth2.credentials
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheetID,
                                range=rangeName).execute()
    values = result.get('values', []) # list of lists
    if len(values)==0:
        print('Signup data not found')
        return pd.DataFrame()    
    headers = changeColNames(values[0])
    # Google API retrieved rows each become lists truncated at last value
    newValList=[]
    for vallist in values[1:]:
        while len(vallist)<len(headers):
            vallist.append('') # add blanks for missing/optional answer
        newEntry={}
        for i, val in enumerate(vallist):
            newEntry[headers[i]]= val
        newValList.append(newEntry)
    signups=pd.DataFrame(newValList, columns=headers)            
    return signups    

def downloadSheet(sheetID, rangeName):
    ''' Generic google sheets download
    
    '''
    creds = getGoogleCreds() # google.oauth2.credentials
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheetID,
                                range=rangeName).execute()
    values = result.get('values', []) # list of lists
    if len(values)==0:
        print('No data found for google sheet')
        return pd.DataFrame()
    headers = values[0]
    # Google API retrieved rows each become lists truncated at last value
    newValList=[]
    for vallist in values[1:]:
        while len(vallist)<len(headers):
            vallist.append('') # add blanks for missing/optional answer
        newEntry={}
        for i, val in enumerate(vallist):
            newEntry[headers[i]]= val
        newValList.append(newEntry)
    mySheet=pd.DataFrame(newValList, columns=headers)            
    return mySheet