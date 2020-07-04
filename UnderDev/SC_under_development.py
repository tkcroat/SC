# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:13:53 2016

@author: tkcplayers['DOB'] =  pd.to_datetime(players['DOB'], format='%Y-%m-%d')
"""
import numpy as np
import pandas as pd
import glob, math
import datetime
from datetime import date
from PIL import Image, ImageDraw, ImageFont

import csv
import glob
import tkinter as tk
import numpy as np
from pkg.SC_signup_functions import findcards
from email.mime.text import MIMEText
import os

import string
import re
import flask

import sys
from datetime import datetime

import numpy as np


# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 08:39:33 2020

@author: Kevin
"""

#%% New pygsheets method of finding/processing new signups 

def assignGsignupKey(numkeys):
    '''
    '''
    if 'Gkey' not in headers:
        # first time assignment/addition of gkey column
    
    usedkeys=np.ndarray.tolist(usedkeys)
    availkeys=[i for i in allnums if i not in usedkeys]
    if len(availkeys)<numkeys: # get more keys starting at max+1
        needed=numkeys-len(availkeys)
        for i in range(0,needed):
            nextval=int(max(usedkeys)+1) # if no interior vals are available find next one
            availkeys.append(nextval+i)

def processNewGsignups(myPygSheet, newrownums):
    '''
    '''

def downloadSignups(sheetID, rangeName):
    ''' Download all from current season's signups
    Using pygsheets version w/ assigned Gkey.. original forms only gets addition
    of Gkey and Processed cols (no rename of others)
    processed signups w/ Plakey/Famkey in separate sheet
    
    pygsheets short tutorial
    https://medium.com/game-of-data/play-with-google-spreadsheets-with-python-301dd4ee36eb
    
    '''
    creds = getGoogleCreds() # google.oauth2.credentials
    gc = pyg.authorize(custom_credentials=creds) # pygsheets client
    sh = gc.open_by_key(sheetID)
    myPygSheet=sh[0]
    mycols=myPygSheet.get_row(1)
    # Can't necessarily count on rows not getting renumbered or resorted
    if 'Gkey' not in mycols: # Initialize spreadsheet key (Gkey)
        myPygSheet.add_cols(2) # auto adds to gsheet
        # initialize this new row for each occupied column 
        myPygSheet.update_col(len(mycols+1),['Gkey', 1,2,3])
        # Find numbers of occupied rows .. timestamp always occupied for entries
        # pygsheets is zero-indexed, but worksheet addresses start w/ 1
        occRows = [i+1 for i,val in enumerate(myPygSheet.get_col(1)) if val !='']
        gkeyvals=['Gkey']
        gkeyvals.extend([str(i) for i in range(2, len(occRows)+1)])
        # add Gkeys to this newly-added column
        myPygSheet.update_col(len(mycols)+1,gkeyvals)
        myPygSheet.update_col(len(mycols)+2,['Processed') # col to track processing status
    
    else:
        
        # Find rows w/ occupied timestamp entry
        tstampRows = [i+1 for i,val in enumerate(myPygSheet.get_col(1)) if val !='']
        # get column w/ Gkeys
        gkeys=myPygSheet.get_col(mycols.index('Gkey'))
        keyRows = [i+1 for i,val in enumerate(gkeys) if val !='']
        newrownums=[i for i in tstampRows if i not in keyRows]
        for i, nr in enumerate(newrownums):
            if nr > max(gkeys):
                
            
        if len(newrownums)>0:

            
        # Gkey and Processed cols already present
        headers = changeColNames(mycols)        
        gsignups=pd.DataFrame(myPygSheet.get_all_records()[1:], columns=headers)
        newSus=gsignups[gsignups['Processed']==''] # null strings in gsheet 
            
            

    creds = getGoogleCreds() # google.oauth2.credentials
    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheetID,
                                range=rangeName).execute()
    sh = gc.open_by_key(sheetID)
    myPygSheet=sh[0]

    mycols=myPygSheet.get_row(1) # gets column names
    myPygSheet=sh[0]
    mycols=myPygSheet.get_row(1) # gets column names

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

#%%

def writeGsheetChanges(df, pygSheet):
    ''' 
    
    '''
    pygSheet.set_dataframe(df, 'A1')

wks1.get_row(2)
wks1.update_value('C12','testval')
# Get pygsheet as pandas (screws up col order but is actively linked)

# write pandas as pygsheet
wks1.set_dataframe(test)

df1 = SCapi.readPaylog() # direct download version

df2= pd.DataFrame(wks1.get_all_records()) # cols out of order

wks1.set_dataframe(teams, 'A1')


# Strategy for alteration of online gsheets
# pygsheets is actively linked ... use update_value method? 
# Google sheets undo button only works for browser made changes (not programmatic)
# Check for differences between 2 dataframes
# pygsheets tutorial 
# https://medium.com/game-of-data/play-with-google-spreadsheets-with-python-301dd4ee36eb
# Revert to prior by clicking "last edit..." 

def diffDf(df1,df2):
    
    bothdf=pd.concat([df1,df2])
    altrows=bothdf.drop_duplicates(keep=False)
    altrows=altrows.sort_values(['First','Last'])

def modGsheet(df):
    # perform datetime and int/nan conversions on assorted columns
    def convInt(val):
        try:
            return int(val)
        except:
            return np.nan
        
    def convDate(val):
        try:
            return datetime.strptime(val, '%m/%d/%Y')
        except:
            try:
                return datetime.strptime(val, '%m/%d/%y')
            except:
                try:
                    return datetime.strptime(val.split(' ')[0], '%Y-%m-%d')
                except:
                    print('Error converting', val)
                    return val

def write2Sheet(sheetID, rangeName):
    '''
    
    '''
        {
      "range": "Sheet1!A1:D5",
      "majorDimension": "ROWS",
      "values": [
        ["Item", "Cost", "Stocked", "Ship Date"],
        ["Wheel", "$20.50", "4", "3/1/2016"],
        ["Door", "$15", "2", "3/15/2016"],
        ["Engine", "$100", "1", "3/20/2016"],
        ["Totals", "=SUM(B2:B4)", "=SUM(C2:C4)", "=MAX(D2:D4)"]
      ],
    }
#%%
def write2Sheet(sheetID, rangeName):
    ''' Write to google sheet from current season's signups
    
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
#%% 

# custom mod after removal of unis from mastersignups
mastersign=Mastersignups.copy()
mycols=mastersign.columns
mycols=[i for i in mycols if i not in ['Issue date','Uniform#','UniReturnDate']]

                                       
def writeuniformlog(mastersign, teams, unilist, players, season, year, paylog):
    ''' From mastersignups and teams, output contact lists for all teams/all sports 
    separately into separate tabs of xls file 
    autosaves to "Fall2016"_uniform_log.xls
    args:
        mastersign - list of signups and team assignments
        teams - tab w/ uniform setname for this team
        unilist - check if number/size already checked out for player
        
    '''    
    mastersign=mastersign[mastersign['Year']==year] # remove prior years in case of duplicate name
    mastersign=mastersign.reset_index(drop=True)
    # keep track of needed cols
    mycols=list(mastersign.columns)
    # Just need school from players.csv
    mastersign=pd.merge(mastersign, players, how='left', on=['Plakey'], suffixes=('','_r'))
    mycols.append('School')
    mastersign=mastersign[mycols]
    # rename uniforms col from teams to setname (matches other uni tracking sheets)
    teams=teams.rename(columns={'Uniforms':'Setname'})
    # Only need teams w/ issued uniforms
    teams=teams[ (pd.notnull(teams['Setname'])) & (teams['Setname']!='') & (teams['Setname']!='N') ]
    uniformlist= list(teams.Team.unique())
    # Can just eliminate any entries not in uniform deposit list
    mastersign=mastersign[mastersign['Team'].isin(uniformlist)] # only players on teams needing uniforms
    
    # Need uniform set name (from team tab)
    mastersign=pd.merge(mastersign, teams, how='left', on=['Year','Sport','Team'], suffixes=('','_r'))
    mycols.append('Setname')
    mastersign=mastersign[mycols]
    # Now see if any team players already have checked out uniform of correct type
    outset=unilist[(unilist['Location']=='out') & (unilist['Plakey']!=0)]
    outset=outset.rename(columns={'Number':'Uniform#'})
    mycols.append('Number','Size')
    # Now find existing uniform deposits from paylog
    
    # Handle deposits by family (and need single entry per family)
    # returns mastersign w/ deposit info interpolated
    mastersign=processDeposits(paylog, mastersign)
    # single uniform log per season 
    contactfile='\\'+str(season)+'_'+str(year)+'_uniform_log.xlsx'
    writer=pd.ExcelWriter(cnf._OUTPUT_DIR+contactfile, engine='openpyxl',date_format='mm/dd/yy')
    # Columns needed for log output

    outcols=['First', 'Last', 'School', 'Issue date', 'Uniform#', 'Size', 'Deposit date',
            'Amount', 'Deptype', 'DepComment', 'UniReturnDate', '$ returned', 
            'Comments', 'Plakey', 'Famkey']
    
    mycols=['First', 'Last', 'School', 'Issue date', 'Uniform#', 'Size', 'Amount', 
            'Deposit type', 'Deposit date', 'UniReturnDate', '$ returned', 
            'Comments', 'Plakey', 'Famkey']
    tabnamelist=[]
    # TODO Find size from this year's sport signup
    for team in uniformlist:
        thismask = mastersign['Team'].str.contains(team, case=False, na=False)
        thisteam=mastersign.loc[thismask] # this team's signups
        sport=thisteam.iloc[0]['Sport'].lower()
        thisteam=finddeposits(thisteam, paylog) # thisteam is this team's slice of info from master_signups
        missing=[i for i in mycols if i not in thisteam.columns]
        for miss in missing:
            thisteam[miss]=''
        thisteam=thisteam[mycols] # organize in correct format for xls file
        tabname=sport[0:3]+team[0:3] # name tab with team's name..
        if tabname in tabnamelist:
            tabname+='2' # handles two teams per grade
        tabnamelist.append(tabname)
        thisteam.to_excel(writer, sheet_name=tabname,index=False) # this overwrites existing file
    writer.save()
    return

def processDeposits(paylog, mastersign):
    ''' For uniform issue, need to handle multiple players from family and multiple
    historical deposits together
    
    args:
        paylog - payment logbook w/ non-deposit transactions filtered out
        mastersign - signups for this season, uni issue only subset
        
    '''
    fams=list(mastersign.Famkey.unique())  
    paylog=paylog.dropna(subset=['Deposit']) # only need deposit info
    # Need to handle the deposits by family
    paylog=paylog[paylog['Famkey'].isin(fams)]
    # Handle multiple entries from same family
    dups=paylog[paylog.duplicated('Famkey')]
    
    # plakey merge would be easiest
    
    master
    dupPlayers=
    test=paylog[paylog.duplicated('Famkey', keep=False)]
    famgroup=mastersign.groupby(['Famkey'])
    famDepGroup=paylog.groupby(['Famkey'])
    for fk, gr in famgroup:
        # see if famkey is present in famDep
        if fk in list(famDepGroup.groups.keys()):
            deps=famDepGroup.get_group(fk)
            
        
    

#%% 
    
def findOpponents(teamName, badDay, sched, **kwargs):
    ''' Finds opponent(s) on day
    args:
        teamName - name as string (as in schedule)
        date - datetime of game in question (usually problematic one)
        sched - full schedule
    
    returns:
        opponents - opponents as list 
    
    kwargs:
        badTime:  if only 1 game of multiples on day is a problem   
    '''

    # Find bad game(s) in question
    match=sched[ (sched['Date']==badDay) & ( (sched['Home']==teamName) | (sched['Visitor']==teamName)) ]
    if 'badTime' in kwargs:
        bt=kwargs.get('badTime')
        # TODO make more robust using time conversion from string?  
        match=match[match['Start']==bt]
        if len(match)!=1:
            print('Time matched game not found')
            return
    opponents = [i for i in match.Home.to_list() + match.Visitor.to_list() if i != teamName]
    return opponents
    
def findTeamSwap(teamName, badDay, sched, gamerank=0, **kwargs):
    ''' Swap team1 (with conflict) into another existing game (find opponent switching existing
    away team)... 
    args:
        teamName=' Cabrini-Clavin-6GD' # name as listed on schedule not traditional league name
        badDay=datetime(2020,1,11)
        sched -  full game schedule    
        gamerank -- index in list of games to choose (defaults 0 for best match)
            used if first run unsatisfactory for some reason
    kwargs:
        'badTime' -- string matching single game to change (not double game).. '7:30 PM'
    
    returns:
        swapOld -- original offending set of games
        swapNew -- replacement w/ opponents rearranged
    '''
    # first check for proper team name (as printed in schedule)
    allTeams=list(set(list(sched.Home.unique())+list(sched.Visitor.unique())))
    if teamName not in allTeams:
        print('Faulty team name not found in full schedule')
        return
    league=teamName.split('-')[2] # full league 7BD1 (grade/gender/letter and sublevel)
    leagueTeams=[i for i in allTeams if league in str(i)]
    # Find teams w/ bye that weekend
    weekend=sched[ (sched['Date']>badDay-timedelta(days=3)) & (sched['Date']<badDay+timedelta(days=3)) ]
    teamInAction = list(set(list(weekend.Home.unique())+list(weekend.Visitor.unique())))
    bestAvailTeams = [i for i in leagueTeams if i not in teamInAction]
    # Preference for teams w/o full/half schedule 
    bestAvailTeams = [i for i in bestAvailTeams if not i.endswith('-H')]
    bestAvailTeams = [i for i in bestAvailTeams if not i.endswith('-F')]
    rankedSwaps={} # dict to hold possible games and assigned score
    # Find timespan of bye weekend for team1 (best swap)
    byeWeeks=findByeWeek(teamName, sched)
    for byeWeek in byeWeeks:
        # Find possible swap/replacement games in first bye week
        swapGames=sched[ (sched['Date']>=byeWeek[0]) & (sched['Date']<=byeWeek[1])]
        # Find games for best swap team candidates while ensuring original team doesn't play itself
        swapGames=swapGames[ (swapGames['Visitor'].isin(bestAvailTeams)) & (swapGames['Home']!=teamName) ]
        theseSwaps=rankSwaps(teamName, badDay, bestAvailTeams, sched, swapGames, **kwargs)
        rankedSwaps.update(theseSwaps)
    # find more possible swaps ..not necessarily during bye week 
    swapOld, swapNew, swapTeam = pickBestSwap(rankedSwaps, gameRank)
    return swapOld, swapNew, swapTeam 

def findAllOpponents(teamName, sched):
    ''' Return list of all of given teams opponents
    '''
    thisSched=sched[ (sched['Home']==teamName) | (sched['Visitor']==teamName) ]
    opponents = [i for i in thisSched.Home.to_list() + thisSched.Visitor.to_list() if i !=teamName]
    return opponents

def findBadGames(teamName, badDay, sched, **kwargs):
    ''' Find offending game or games
    args:
        teamName - name as string (as in schedule)
        date - datetime of game in question (usually problematic one)
        sched - full schedule    
    kwargs:
        'badTime' -- offensive time as string (for picking single game)
    returns:
        badGames- dataframes with offending game or games
    '''
    match=sched[ (sched['Date']==badDay) & ( (sched['Home']==teamName) | (sched['Visitor']==teamName)) ]
    if 'badTime' in kwargs:
        bt=kwargs.get('badTime')
        # TODO make more robust using time conversion from string?  
        match=match[match['Start']==bt]
        if len(match)!=1:
            print('Time matched game not found')
    return match

def rankSwaps(teamName, badDay, bestAvailTeams, sched, swapGames, **kwargs):
    ''' if multiple possible swap games available, choose best swap by maximizing 
    schedule diversity of opponents (simultaneous for both swapped teams)
    adds large penalty (+3) for setting up 3rd game against same team
    adds small penalty (+1) for swapping team out of one of its home games
    args:
        teamName - original team name w/ conflict (string)
        badDay - date of conflicting game or games
        bestAvailTeams - list of possible swap teams
        gamerank - index of game to choose from ranked list (defaults 0)
        sched - full CYC schedule
        swapGames -- dataframe w/ possible swap/replacement games
    kwargs:
        'badTime' -- offensive time as string (for picking single game)
    returns:
        swapOld - offending set of games
        swapNew - new game alteration to replace above
    '''
    # Find list of team 1 opponents (includes duplicates)
    opponents1 = findAllOpponents(teamName, sched)
    # opponents in original swapped game (len 2 if solving game conflict)
    badGames = findBadGames(teamName, badDay, sched, **kwargs)
    # Team overlap counts for each possibility
    overlapScore={}
    for ind, row in swapGames.iterrows():
        for ind2, row2 in badGames.iterrows():
            # Possible swapping team already chosen as visitor
            ct1=opponents1.count(row.Home) # existing games against this oppo 
            # new opponent for original swapped team will be home in swap candidate 
            # Now find min in # of games of swap team against potential new opponents
            oppos=findAllOpponents(row.Visitor, sched) # other opponents 
            # Drop opponent (once) from this swap game
            oppos.remove(row.Home)
            # Now calculate minimum overlap w/ new opponent (from chosen badGame(s))
            newOpp=[i for i in [row2.Home, row2.Visitor] if i !=teamName][0]
            ct2=oppos.count(newOpp)
            # Add large triple play penalties (already playing team twice) but allow single repeat
            if ct1>=2:
               ct1=5
            if ct2>=2:
               ct2=5
            # add small penalty for switching original team out of its home game
            if row2.Home==teamName:
                ct2+=1
            # key is indices of games to swap and name of team to swap from other game
            overlapScore[ind, ind2, row.Visitor]= ct1+ct2
    return overlapScore

#%%

def pickBestSwap(rankedSwaps,gameRank=0):
    ''' After evaluating all possible swaps across all available bye
    weeks for original team, sort by rank and pick first (or pick
    one based on gameRank index if original doesn't work for some 
    other reason)
    
    args:
        rankedSwaps -- dict w/ game score (val) and key (list w/ 2 game indices and 
           affected swap team
    gameRank -- which one to choose
    
    '''
    rankSwapList=[]
    for i in range( min(rankedSwaps.values()), max(rankedSwaps.values())+1):
        theseSwaps = [key for key, val in rankedSwaps.items() if val ==i]
        rankSwapList.extend(theseSwaps)
    bestSwap=rankSwapList[gameRank] # choice from ranked list (index 0 unless overridden
    swapTeam=bestSwap[-1] # pull out swap team name
    bestSwap=bestSwap[0:2] # indices of swapped games
    swapOld = sched[sched.index.isin(bestSwap)]
    # Also return new arrangement of games 
    swapNew = swapOld.copy()
    # Find/replace teamName w/ swapteam 
    if teamName in [swapOld.iloc[0]['Home'],swapOld.iloc[0]['Visitor'] ]:
        if teamName==swapOld.iloc[0]['Home']:
            swapNew.at[swapOld.index[0],'Home']=swapTeam # avoids chained indexing & assignment problems
            swapNew.at[swapOld.index[1], 'Visitor']=teamName
        else:
            swapNew.at[swapOld.index[0], 'Visitor']=swapTeam
            swapNew.at[swapOld.index[1],'Visitor']=teamName
    else:
        if teamName==swapOld.iloc[1]['Home']:
            swapNew.at[swapOld.index[1], 'Home']=swapTeam
            swapNew.at[swapOld.index[0], 'Visitor']=teamName
        else:
            swapNew.at[swapOld.index[1], 'Visitor']=swapTeam
            swapNew.at[swapOld.index[0], 'Visitor']=teamName
    return swapOld, swapNew, swapTeam
#%%    
    # turn rankedSwaps into list 
#TODO wrap in the final picker/ game alterer 
    # Produce sorted list from dict in best to worst order
    # Best swapping games combo will have minimum overlap score

def findResched(team1, team2, gymsched):
    ''' Find a date and venue for a game ... for full reschedule not swapping
    method
    TESTING team1='6-F-6GD-Clavin'  team2='St Peter-Long-6GD-F'
    '''
    league=team1.split('-')[2][0:3]
    # Best match (open date both teams and venue)
    bestAvails=gymsched[ gymsched['Assignments'].str.contains(league) ]
    
    # Could also swap games/ opponents (but don't swap home team)
    
def plotAvailSlots(gymsched):
    ''' Create histogram with # of available slots by date
    '''
    

avail7 =  gymsched[ gymsched['Assignments'].str.contains('7') & pd.isnull(gymsched['Home'])]
allAvail=gymsched[ pd.isnull(gymsched['Home'])]


def findGymSlot(gymsched, thisDate):
    ''' Return empty available gym slots for given day
    '''
    def convDate(val):
        try:
            return datetime.strptime(val,'%m/%d/%Y')
        except:
            return val
    gymsched['Date']=gymsched['Date'].apply(lambda x:convDate(x))            
    avail= gymsched[ pd.isnull(gymsched['Home']) & ( gymsched['Date']== thisDate)]
    return avail

def getSchedule(sched, teamname):
    ''' Returns full schedule for given team name 
    args:
        sched - full CYC schedule
        teamname - exact unique team string
    returns:
        teamsched
    '''
    teamsched=sched[(sched['Home'].str.contains(teamname)) | (sched['Visitor'].str.contains(teamname))]
    return teamsched
    
    
#%% Vectorized version of find players


#%%

# TODO interface directly w/ google form
# TODO smarter file rename tool

Temp=players['DOB']


players.to_csv('players.csv',index=False)


def loadSchedule():
	''' Choose schedule file and open
	'''
	def get_file_path():
        '''
        Popup dialog box to find db path if non-standard
        '''
        root=tk.Tk() # creates pop-up window
        root.update() # necessary to close tk dialog after askopenfilename is finished
        # tk dialog asks for a single station file
        full_path = tk.filedialog.askopenfilename(title = 'Choose schedule name',
                                filetypes=[ ('XLS','*.xls*'), ('csv','*.csv')] )
        root.destroy() # closes pop up window
        return full_path
	myPath = get_file_path()
	if myPath.endswith('.csv'):
		sched=pd.read_csv(myPath, , encoding='cp437')
	elif myPath.endswith('.xls) or myPath.endswith('.xlsx):
		sched=pd.read_excel(myPath)
	else:
		print('Schedule file must be CSV or Excel')
	return sched
	
def openSmtpObj():
    '''
    Open and return smtp connection for gmail send
    TODO rearrange messaging scripts to make single call 
    '''
    try:
        mailserver = smtplib.SMTP('smtp.gmail.com', 587) # port 587
        mailserver.set_debuglevel(True)
        mailserver.starttls() # enable encryption for send 
        print('Enter password for sponsors club gmail ')
        passwd=input()
        mailserver.login('sfcasponsorsclub@gmail.com', passwd)
        mailserver.ehlo() # say hello
    except:
        print("Mail Server Error:", sys.exc_info()[0])
        mailserver=np.nan
    return mailserver

def removeOldKids(players):
    '''
    Remove if >16 
    '''
    

    
def prepPMSchedule(allteams):
    '''
    
    '''
    allteams=allteams[pd.notnull(allteams['Visitor Name'])]


def finddiv(sched):
    '''
    
    '''
    
# TODO modify for possibility of multiple teams per grade
df=findmissinginfo(df, players, famcontact)
index=2  row=df.loc[index]

kwargs={}
kwargs.update({'Comment':'Pay direct to OLS league'})

test=maketracksummary(Mastersignups, 2017, players)
test.to_csv('track_summ.csv', index=False)    
unilogfile=pd.read_excel('Fall_2017_uniform_log.xlxs') 

def sync_unilogs(unilist, Mastersignups, teams, oldteams):
    '''
    Both are primary sources so discrepancies should be resolved (i.e. after 
    inventory)
    Check-out or Check-in options if conflicting
    '''
    # need 
    


def update_uniinfo(unilogfile, unilist, Mastersignups):
    ''' 
    After uniform night or other event, use unilogfile with possible new info
    and update both unilogfile and mastersignups in self-consistent manner 
    
    Need to synchronize master unilist, mastersignups and uniform log (often 
    read back with unique information )
    Assumes unique size/number/uniset 
    '''
    
    
def display_conflict(group):
    ''' In cases of conflicting uniform info send to gui for display/resolution
    '''

'''TESTING 
teams=SCbill.loadoldteams(['Winter'], [2017]) 
unilogfile='Winter_2017_uniform_log.xlsx'
row=alluniplayers.iloc[1]
index=row.name
year=2017
'''


# TESTING  test=grouped.get_group(('Postup','13'))
#  unis.groupby(['Uniforms','Year','Gender']).size()
# unis[unis['Year']==2016].groupby(['Uniforms','Year','Gender']).size()
# unis[(unis['Year']==2016) & (unis['Uniforms']=="Y")].groupby(['Uniforms','Year','Gender','Team','Sport']).size()

def mark_return_tk():
    '''
    Interactive stamping of return date on suspected returned unis in mastersignups
    maybe not necessary eventually if master unilist takes off
    '''
    
    pass

def matchunisets(Mastersignups, teams, oldteams):
    '''
    Get uniset for all uniforms issued in mastersignups... needed before compare
    w/ master unilist 
    '''
    unis=Mastersignups.dropna(subset=['Issue date']) # only signups with uniform issued
    # mycols=teams.columns
    teams=pd.concat([teams,oldteams])
    unis=pd.merge(unis, teams, how='left', on=['Year','Sport', 'Team'], suffixes=('','_2'))
    # Y or nan for uniform set not useful for uniform tracking
    unis=unis[pd.notnull(unis['Uniforms'])] # probably old ones we don't care about
    # without knowing the set, also not useful
    unis=unis[unis['Uniforms']!='Y']
    # remove ?? in uniform number
    unis=unis[unis['Uniform#']!='??']
    # Drop returned uniforms?
    unis=unis[pd.notnull(unis['UniReturnDate'])] 
    grouped=unis.groupby(['Uniforms','Uniform#'])
    for (uniset, num), group in grouped:
        if len(group)>1:
            gr=group.groupby('Plakey')
            for key, gro in gr:
                if len(gro)>1:
                    mark_return_tk(gro)
                    print(uniset, num, len(group))
                else: # multiple checkouts to same player (mark older returned)
                    
                    
            print(uniset, num, len(group))
            # multiple reports on same .. 
            # keep most recent issue date, ensure older ones marked returned
            test=test.sort_values(['Issue date'], ascending=False)
            older=test.iloc[1:]
            older=older[pd.isnull(older['Return date'])]
            
            test.iloc[0]['Issue date']
            test.iloc[1]['Issue date']
        

    unisets=np.ndarray.tolist(unis.Uniforms.unique())
    unisets=[i for i in unisets if str(i)!='nan']
    unisets=[i for i in unisets if i!='Y']
    
    grouped=unis.groupby(['Uniforms','Uniform#'])
    
    for (uniset, num), group in grouped:
        print(uniset, num, len(group))
    # Keeps only unreturned uniforms
    outunis=outunis.loc[pd.isnull(outunis['Uni return date'])] 



# Finish DOB timestamp to formatted string conversion
def maketrackroster(df, players, year):
    ''' Pat moore format for track rosters autosaved
    I;Smith;Mary;;F;04/01/2008;SGM;St. Gerard Majella
    ''' 
    temp=df[(df['Year']==year) & (df['Sport']=='Track')]
    temp=temp[temp['Team']!='drop'] # drop the drops
    # Get DOB
    temp=pd.merge(temp, players, on=['Plakey'], how='left', suffixes=('','_2'))
    temp['Type']='I'
    temp['Teamcode']='SFC'
    temp['Blank']=''
    temp['Teamname']='St. Frances Cabrini'
    mycols=['Type','Last','First','Blank','Gender','DOB','Teamcode','Teamname']
    temp=temp[mycols]
    temp['DOB']=pd.to_datetime(temp['DOB'], format="%m/%d/%Y", errors='coerce')
    temp['NewDOB']=temp['DOB'].date()
    temp['DOB']=temp.loc[index]['DOB'].date()
    fname='Cabrini_trackroster_'+str(year+1)+'.csv.'
    temp.to_csv(fname, index=False)
    return

def creditOLS(df, season, year, paylog, **kwargs):
    ''' Enter a credit/waiver into paylog for various types of signups
    i.e. OLS league direct pay 
    df is mastersignups'''
    
    # Convert Timestamp to datetime (default value on import)
    paylog.Date=paylog.Date.apply(lambda x:x.date())
    # Remove players than have dropped (drop as team assignment) 
    thismask=df['Team'].str.contains('drop',na=False,case=False)
    df=df.loc[~thismask]
    df=df.dropna(subset=['Team']) # also drop those not yet assigned to a team
    CurrentSU, PriorSU =getthisperiod(df, season, year, 0) # returns subset of signups in specified period
    for index, row in CurrentSU.iterrows():
        if 'OLS' in row.Team:
            payrow=makecredit(paylog, season, row, 30, **kwargs)
            print('Credit added for', row.First, row.Last)
            paylog=paylog.append(payrow, ignore_index=True)
    paylog.Date
    
datetime.datetime.today()
datetime.datetime.now()

datetime.date(row.Date)


def makecredit(paylog, season, row, amount, **kwargs):
    ''' Make credit row for addition to paylog for given selected row (of specified amount) '''
    row=row.set_value('Amount', 30)
    row=row.set_value('Season', season)
    row=row.set_value('Delivered', 'n/a')
    row=row.set_value('Paytype', 'credit')
    row=row.set_value('Comment', kwargs.get('Comment',''))
    thisdate=datetime.datetime.strftime(datetime.datetime.now(),format="%m/%d/%Y")
    row=row.set_value('Date', thisdate)
    row.Date=row.Date.apply()
    row.Date=row.Date.apply(lambda x:datetime.datetime.strptime(x, "%m/%d/%Y"))
    pd.to_datetime.strptime(row.Date, "%m/%d/%Y")
    row=row.set_value('Paykey', int(paylog.Paykey.max()+1))
    return row[paylog.columns]
    

unilog=pd.read_excel('Master_uniform_logbook.xlsx', sheetname='Uniforms')
unilist=pd.read_excel('Master_uniform_logbook.xlsx', sheetname='Unilist')

def update_unilist():
    ''' Update uniform in/out and plakey based on current season's
    uniform log  '''
    # Change size in master signups if issued size different than requested
    
    # interactive conflicts handling
    
def getsizedists(Mastersignups, season, year, teams, unilog,):
    ''' Get size distributions desired by team's players 
    After team is assigned a uniform set, change unavailable sizes 
    move up or down based on availability  '''
    sportsdict={'Fall':['VB','Soccer'], 
            'Winter':['Basketball'],'Spring':['Track','Softball','Baseball','T-ball']}
    sportlist=sportsdict.get(season,[])
    SUs=Mastersignups[(Mastersignups['Year']==year) & (Mastersignups['Sport'].isin(sportlist))]
    uniteams=teams[teams['Uniforms']!='N']
    # Get size distribution of players needing uniforms 
    for i, team in enumerate(uniteams.Team.tolist()):
        thisteam=SUs[SUs['Team']==team]
        print(len(thisteam))
    
    sizedist

# TESTING index=0  row=unilog.loc[index]
sizes=['YM','YL','YXL','S','M','L','XL','2XL']

for index, row in unilog.iterrows():
    thisset=unilist[unilist['Setname']==row.Setname]
    grouped=thisset.groupby(['Location','Size'])
    for []
    thisset.groupby(['Location','Size']).count()
    for     
    
    print(len(thisset))

thisset.Number.tolist()

def updateunilog():
    ''' Using unilist update in, out, missing totals in unilog first page
    in is instock (closet) after inventory
    out includes missing & assigned (make assigned plakey list and missing
    '''


    
def assigntotwoteams(df, Twoteams):
    ''' Randomly pick a team if two are available  '''
    

def assigntoteams(df, season, year, teams, overwrite=False):
    '''From mastersignups finds CYC team name based on year, grade, gender and sport from teams tab 
    (which only contains names from this season/year to avoid screwing up old custom team assignments''' 
    # teamsmult has multi grade range teams with duplicates for merge matching
    # twoteams is multiple teams for same grade
    Teamsmult, Twoteams=makemultiteam(teams) # makes duplicates team entries to match both grades
    # Compare grades as ints with K=0 
    df.Grade=df.Grade.replace('K','0', regex=True) # convert Ks to zeros
    df=df[pd.notnull(df['Grade'])] # shouldn't happen
    df['Grade']=df['Grade'].astype('int')
    Teamsmult['Grade']=Teamsmult['Grade'].astype('int') # ensure these are ints
    # First deal with gender, grade, sport w/ multiple team options (twoteams)
    df=assigntotwoteams(df, )
    # left merge keeps all master_signups oentries
    df=pd.merge(df, Teamsmult, how='left', on=['Year','Grade','Gender','Sport'], suffixes=('','_r'))
    # need to drop SUkey duplicates (keeping first)... occurs if >1 team per grade
    df=df.drop_duplicates(subset=['SUkey']) # drops any duplicates by unique SUkey
    # Consider all sports except Track (team assignment done separately by DOB)
    sportsdict={'Fall':['VB','Soccer'], 'Winter':['Basketball'],'Spring':['Softball','Baseball','T-ball']}
    sportlist=sportsdict.get(season)
    # this is post-merge so no chance of getting indices screwed up 
    # select current sports & year and subset with new team assignment
    CurrentSU=df.loc[(df['Sport'].isin(sportlist)) & (df['Year']==year) & (pd.notnull(df['Team_r']))]
    if overwrite==False: # if no overwrite, keep only those with nan for team
        CurrentSU=CurrentSU.loc[pd.isnull(CurrentSU['Team'])]
    # Never overwrite team assignment for known drops
    CurrentSU=CurrentSU[CurrentSU['Team']!='drop']
    counter=0
    for index, row in CurrentSU.iterrows(): 
        # all remaining can be overwritted (those w/ existing team dropped above)
        match=df[df['SUkey']==CurrentSU.loc[index]['SUkey']]
        if len(match)==1:
            thisind=match.index[0]
            # add new team assignment to correct index in original master signups
            df=df.set_value(thisind, 'Team', CurrentSU.loc[index]['Team_r'])
            counter+=1
    print(str(counter),' player(s) newly assigned to teams')
    # now drop extra columns and sort 
    mycols=['SUkey','First', 'Last', 'Grade', 'Gender', 'Sport', 'Year', 'Team', 'Plakey','Famkey', 'Family', 
    'SUdate', 'Issue date', 'Uniform#','Uni return date'] 
    df.Grade=df.Grade.replace('K',0)
    df=df.sort_values(['Year','Sport', 'Gender', 'Grade'], ascending=True)
    df.Grade=df.Grade.replace('0','K', regex=True) # make sure any 0 grades are again replaced with K
    df=df[mycols]
    autocsvbackup(df,'master_signups', newback=True) # autobackup of master signups
    df.to_csv('master_signups.csv', index=False) # save/overwrite existing csv
    return df
# Team splitter/ rearranger



'''TESTING
sport, team, school, graderange, gender, coachinfo, playerlist=teamlist[1]
'''

duration=1.5
kwargs={}
kwargs.update({'sport':'soccer'})
kwargs.update({'subject':'Ethan soccer game'})

tempstr='10:30 AM'
pd.to_datetime(tempstr).strftime('%H:%M:%S')

famcontact=update_contact(ser, famcontact)

# from twilio.rest import TwilioRestClient # text messaging ($10/mo)
#%%
thissched=getgameschedule(sched, sport, team, school, graderange, coachinfo)

kwargs={}
kwargs.update({'teams':teams})  # all teams with Cabrini kids assigned (Cabrini + transfers)        
teams=SCbill.loadoldteams('Fall', 2016) # load prior season's teams
teamlist=findschteams(df, teams)

teamnamedict=findschteams(sched, teams, coaches)

teaminfo=getteaminfo(teams)

thissched=getthissched(schname, sched)
getgameschedule(schname, sched)

for key, [div,name] in teamnamedict.items():
    thissched=getgameschedule(div, name, sched)
    print(div, name)
    print(len(thissched))
    
schname=teamnamedict.get(team,'')
thissched=getthissched(schname, sched)

# TODO need a dictionary of real name and scheduled name

def getCYCschedules(df, **kwargs):
    '''Get Cabrini team schedules from Pat Moore jumbo spreadsheet 
    kwargs div  ... 
    probably legacy as output format has changed
    '''
    df=df.rename(columns={'Game Time':'Time','Field Name':'Location','AwayTeam':'Away','Home Team':'Home'})    
    # return only passed grade (can be used in combo with other options)
    if 'div' in kwargs:
        div=kwargs.get('div','')
        df=df[pd.notnull(df['Division Name'])]
        df=df[df['Division Name'].str.contains(div)]
    if 'school' in kwargs: # get only passed school name
        school=kwargs.get('school','')
        df=df[df['Home'].str.contains(school) | df['Away'].str.contains(school)]
    # get all from Cabrini teams list (including non-Cabrini transfers)
    elif 'teams' in kwargs:
        teams=kwargs.get('teams',pd.DataFrame())
        teamlist=findschteams(df, teams)
        df=df[df['Home'].isin(teamlist) | df['Away'].isin(teamlist)]
    df=df[pd.notnull(df['Date'])] # removes unscheduled games
    # split day/date field
    df['Day']=df['Date'].str.split(' ').str[0].str.strip()
    df['Date']=df['Date'].str.split(' ').str[1].str.strip()
    mycols=['Date','Day','Time','Location','Home','Away']
    df=df[mycols]
    # shorten team names 
    df.Home=df.Home.str.replace('St Frances Cabrini','Cabrini')
    df.Home=df.Home.str.replace('St ','')
    df.Away=df.Away.str.replace('St Frances Cabrini','Cabrini')
    df.Away=df.Away.str.replace('St ','')
    return df

test=df[df['Home'].isin(teamlist)]

               
def getschoolnames(df):
    ''' '''
    df=df[pd.notnull(df['Home Team'])]
    teams=np.ndarray.tolist(df['Home Team'].unique())
    schools=[s.split('/')[0] for s in teams]
    schools=set(schools)
    schools=list(schools)

test=famcontact[famcontact['Family']=='Lehrer']
# TODO summary by gender/grade also needed (preliminary)
mytab=zipgroups.to_html()


import tkinter as tk


rows=Recs.get_group(('Vance','Delong'))


test=players[players['Last']=='Norwood']

messfile='messages\\CYCcard_needed.txt'

def findmissingcards(Mastersignups, season, year):
    ''' Find all players on CYC level teams, search for card and return list
    without scan on file... send prompt/ reminder incl. team assignment 
    grouped by famkey  '''

def updateteam():
    ''' Send confirmation about signup + current team summary; ask about other players 
    include ideal #; mention missing players  '''

    


# TODO .. how about a more sophisticated imperfect matcher via tk... currently only used for very likely new 
#  player     
    

def checkalias_gui(first, last, DOB, match):
    ''' Confirm ID of some player and possibly add alias to players.csv
    passing both match rows?  '''
    root = tk.Tk()
    yesvar=tk.IntVar()
    novar=tk.IntVar()
    aliasvar=tk.IntVar()
    yesvar=0
    novar=0
    aliasvar=0
    def choosea():
        yesvar=1
        root.destroy()
    def chooseb():
        aliasvar=1
        root.destroy()
    def choosec():
        novar=1
        root.destroy()
    T=tk.Text(root, height=4, width=5)
    mystr='Associate player', first, last, DOB ' with existing player', first
    T.insert(END, 'some string')
    a=tk.Button(root, text='ID player but skip alias').pack()
    b=tk.Button(root, text='ID and add name as alias').pack()
    c=tk.Button(root, text='Do not ID player').pack()
    a.bind("<Button-1>", choosea)
    b.bind("<Button-1>", chooseb)
    c.bind("<Button-1>", choosec)
    # add alias first to player's info?
    root.mainloop()
    vallist=[yesvar, aliasvar, novar]
    

def moveplayers(df, team):
    ''' In case of multiple teams for same gender grade, use listbox to shift/reassign players from one 
    team to another;  initial assignment can be random '''from Tkinter import *
    # Use global variables to get thes
    
    master = Tk() # creates window object
    master.title('Team tinkering')
    # can set sizing
    listbox = Listbox(master)
    listbox.pack() # embeds this on page 
    
    listbox2 = Listbox(master)
    
    def moveDown():
    
        move_text = listbox.selection_get()
        curindex = int(listbox.curselection()[0])
        listbox.delete(curindex)
        listbox2.insert(END, move_text)
    
    moveBtn = Button(master, text="Move Down", command=moveDown)
    moveBtn.pack()
        
    listbox2.pack()
    
    for item in ["one", "two", "three", "four"]:
        listbox.insert(END, item)
    
    mainloop() # continuous run 
     
# This option would also send paper bill summary subsection for each family who still owes to coach
# current e-bill to coach only has brief summary table for each player
# maybe worth adding this later
def messagecoachbill(teams, coaches, billlist, players, emailtitle, messageheader):
    '''Aggregate info about text/call only players and send to coaches in single file'''
    noemaillist=billlist.loc[billlist['Email1'].isnull()] # subset with no working e-mail address
    teamlist=np.ndarray.tolist(teams.Team.unique())
    for i, team in enumerate(teamlist):
        # get head coach e-mail address
        coachemail=getcoachemail(team, teams, coaches)
        if coachemail=='':
            continue
        thisteam=noemaillist[noemaillist['Teams'].str.contains(team)]
        if len(thisteam)==0: # Skip team if all players have working e-mail addresses
            # could send a different message
            continue
        papermessage=makecoachmessage(thisteam)
        fullmessage=messageheader+papermessage
        # insert coach e-mail address and e-mail title
        fullmessage=fullmessage.replace('$RECIPIENTSTR', coachemail)
        fullmessage=fullmessage.replace('$EMAILTITLE', emailtitle)
        # re-structure to allow testing to log (similar to ebill structure)

def makecoachmessage(thisteam, players):
    '''Passed subset of text-only players for this team (df with rows from main bill); make summary for e-mail to 
    coach '''
    thisstring=''
    for index, row in thisteam.iterrows():
        thisstring+='Family:'+thisteam.loc[index]['Family']+'\n'
        plakeys=thisteam.loc[index]['Plakeys']
        plakeys=[int(s) for s in plakeys.split(',')]
        tempstr=getplayers(plakeys, players)
        thisstring+='Players:'+tempstr+'\n'
        thisstring+='Fees for this season: '+str(thisteam.loc[index]['Charges'])+'\n'
        thisstring+='Payments for this season: '+str(thisteam.loc[index]['CurrPayment'])+'\n'
        thisstring+='Fees/Payments from prior season(s): ' + thisteam.loc[index]['Feepaydetail']
        thisstring+='Total fees due: '+str(-thisteam.loc[index]['Balance'])
        thisstring+=thisteam.loc[index]['Unidetail'] # family's uniform situation
        thisstring+="Text message for player's family (optional):\n"
        thisstring+=thisteam.loc[index]['Textmessage']+'\n'
    return thisstring

# formatting of xls files using xlsxwriter
format2 = workbook.add_format({'num_format': 'mm/dd/yy'})
worksheet.write('A2', number, format2) 

def writeuniformlog(df, teams, players, season, year, paylog):
    ''' From mastersignups and teams, output contact lists for all teams/all sports separately into separate tabs of xls file
    autosaves to "Fall2016"_uniform_log.xls'''
    # Slice by sport: Basketball (null for winter?), Soccer, Volleyball, Baseball, T-ball, Softball, Track) 
    
    df=df[df['Year']==year] # remove prior years in case of duplicate name
    df=df.reset_index(drop=True)
    # get school from players.csv
    df=pd.merge(df, players, how='left', on=['Plakey'], suffixes=('','_r'))
    # find Cabrini teams from this season needing uniforms
    thismask = teams['Uniforms'].str.contains('y', case=False, na=False)
    uniformteams=teams.loc[thismask]
    uniformlist= uniformteams.Team.unique() 
    uniformlist=np.ndarray.tolist(uniformlist)
    # single uniform log per season 
    contactfile=str(season)+'_'+str(year)+'_uniform_log.xlsx'
    writer=pd.ExcelWriter(contactfile, engine='xlxswriter',date_format='mm/dd/yy')
    # Can just eliminate any entries not in uniform deposit list
    df=df[df['Team'].isin(uniformlist)] # only players on teams needing uniforms
    # columns needed for log output
    mycols=['First', 'Last', 'School', 'Issue date', 'Uniform#', 'Amount', 'Deposit type', 'Deposit date', 'Uni return date', '$ returned', 'Comments', 'Plakey', 'Famkey'] 
    tabnamelist=[]
    for i, team in enumerate(uniformlist):
        thismask = df['Team'].str.contains(team, case=False, na=False)
        thisteam=df.loc[thismask] # this team's signups
        sport=thisteam.iloc[0]['Sport'].lower()
        thisteam=finddeposits(thisteam, paylog) # thisteam is this team's slice of info from master_signups
        dropcollist=[s for s in thisteam.dtypes.index if s not in mycols]
        thisteam.drop(dropcollist, axis=1, inplace=True) # drops extraneous columns
        thisteam=thisteam[mycols] # organize in correct format for xls file
        tabname=sport[0:3]+team[0:3] # name tab with team's name..
        if tabname in tabnamelist:
            tabname+='2' # handles two teams per grade
        tabnamelist.append(tabname)
        thisteam.to_excel(writer,sheet_name=tabname,index=False) # this overwrites existing file
        # Now need to retrieve to allow header modification
        workbook=writer.book
        worksheet=writer.sheets(tabname) # retrieves this team
        worksheet.set_header([header=tabname+team],) # set tab header to tab + team name
    writer.save()
    return

billlist=pd.read_csv('Billlist_18Jan17.csv')

def getplayers(plakeys, players):
    ''' Returns player first last name list for entire family (from passed list of player keys)'''
    theseplayers=players[players['Plakey'].isin(plakeys)]
    tempstr=''
    for index, row in theseplayers.iterrows():
        tempstr+=theseplayers.loc[index]['First']
        tempstr+=theseplayers.loc[index]['Last']+'; '
    return tempstr
        
def transferunistr(df, season, year, famkey):
    '''Reminder to return uniforms from transfer teams from just prior season 
    current setup for old uniform e-mail and SMS deals with Cabrini only''' 
    df=df.dropna(subset=['Issue date']) # only signups with uniform issued
    mask=pd.isnull(df['Uni return date'])
    df=df.loc[mask] # keeps only unreturned uniforms
    df=df[df['Famkey']==famkey] # this family's outstanding uniforms
    unikeys=np.ndarray.tolist(df.SUkey.unique()) # list of signup keys with outstanding uniforms
    # create string for e-bill with outstanding uniforms
    unistr=''
    if len(df)>0:
        unistr+='Old uniforms to return\n'
        unistr+='Player\tSport\tUni #\tTeam\n'
        for index, row in df.iterrows():
            first=df.loc[index]['First']
            sport=df.loc[index]['Sport']
            num=df.loc[index]['Uniform#']        
            team=df.loc[index]['Team']
            unistr+=first + '\t' + sport + '\t' +str(num) + '\t'+ team +'\n'
    return unistr, unikeys

messagename='messages\\ebill_uninight.txt'

# various modules to attempt direct read-write from google drive                
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def readGDsignups():
    '''Read file from google drive and compare with Excel version ... find new entries  '''

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('GoogleAPI_credential.json', scope)
docid = "182QFOXdz0cjQCTlxl2Gb9b_oEqInH93Peo6EKkKod-g" # winter signups file
client = gspread.authorize(credentials)
spreadsheet = client.open_by_key(docid)
for i, worksheet in enumerate(spreadsheet.worksheets()):
    filename = docid + '-worksheet' + str(i) + '.csv'
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(worksheet.get_all_values())
        
year=2016
season='Winter'
df=Mastersignups
thissum= summarizesignups(df, season, year)

def autocsvbackup(df, filename, newback=True):
    ''' Pass df (i.e players for backup and basename (i.e. "family_contact" for file.. finds list of existing backups and keeps ones of 
    certain ages based on targetdates list; 
    can't remember why was newback=False was needed (always true here to make new backup)

    ''' 
    # targetdates gives ideal ages of list of backup files
    targetdates=[datetime.timedelta(120,0,0),datetime.timedelta(7,0,0)]
    now=datetime.datetime.now()
    mystr='*'+ filename +'*.csv'
    filelist=glob.glob(mystr)
    dates=[] # list of file backup dates
    fileage=[] # age of backup
    for i,name in enumerate(filelist):        
        if '_' not in name:
            continue
        try:
            thisdate=name.split(filename+'_')[1] # splits at players_
            thisdate=thisdate.split('.csv')[0]
            thisdate=datetime.datetime.strptime(thisdate, "%d%b%y")
            age=now-thisdate
            fileage.append(age)
            dates.append([thisdate, age, name])
        except:
            print('Problem getting date from file', name)
    dates.sort() # sort earliest to latest
    fileage.sort(reverse=True) # list of datetimes doesn't show in var list
    if newback==True: 
        if len(dates)==0:  # no existing backups so make one
            fname=filename+'_'+datetime.date.strftime(now, "%d%b%y")+'.csv'
            df.to_csv(fname,index=False)
            print(fname + ' saved to file')
            dates.append([now, now-now,fname])
            fileage.append(now)
        if dates[-1][1]>datetime.timedelta(2,0,0): # also make if no backup in last 2 days (checks youngest file)
            fname=filename+'_'+datetime.date.strftime(now, "%d%b%y")+'.csv'
            df.to_csv(fname,index=False)
            print(fname + ' saved to file')
            dates.append([now, datetime.timedelta(0,0,100),fname]) 
            # enter 100ms as timedelta for new backup
            fileage.append(datetime.timedelta(0,0,100)) # fileage needs to be a timedelta
    # find list of files closest to ~4 mo old backup, 1 week old, and recent backup (2 days ish)
    #  keep at 4 mo and 1 week 
    keepindices=[] # finds index of which backup is closest to target dates (can be duplicates)
    for i,thisage in enumerate(targetdates):
        # find closest entry to each
        ind, age = min(enumerate(fileage), key=lambda x: abs(x[1]-thisage))
        keepindices.append(ind)
    keepindices.append(len(dates)-1) # always keep most recent backup
    
    # for list of lists, any way to just make list of element 1 
    for i, datelist in enumerate(dates):
        if i not in keepindices: # deletes those entries that are not closest to target dates
            os.remove(datelist[2])
    return
 
def standardizeparish(ser):
    ''' Clean up and standardize all the acronyms ... just run on entire series'''
    # Parse standard names/ parse raw input ... fuzzy match then pass to tkinter
    df=stripwhite(df)
    for index, row in df.iterrows()
        
# TODO standardize parish names as done in standardizeschool

# Saving of various files
famcontact.to_csv('family_contact.csv', index=False)  
SCsignup.to_csv('current_signups.csv', index=False) 
Mastersignups.to_csv('master_signups.csv', index=False)
players.to_csv('players.csv', index=False, date_format='%m/%d/%Y') # use consistent datetime format
# need to specify date format... autoconverts datetime to string

def getCYCname(plakey, players):
    ''' Returns exact first and last names of player as found on CYC card from player key'''
    match = players[(players['Plakey']==plakey)]
    if len(match)==0:
        print('Player key # ', plakey, 'not found in database.')
        return   
    elif len(match)>1:
        print('Multiple matches for player key # ', plakey, 'in database.')
        return
    else:
        first=match.iloc[0]['First']
        last=match.iloc[0]['Last']
        return first, last