# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 06:46:15 2017

@author: tkc
"""
import pandas as pd
import re
from datetime import datetime
import tkinter as tk

def writeCabSchedule(sched):
    '''
    Convert date format to correct string and save as csv
    '''
    def convDate(val):
        try:
            return val.strftime('%m/%d/%Y')
        except:
            return None
    sched['Date']=sched['Date'].apply(lambda x:convDate(x))
    def askSavename(sched):
        # save as via pop-up
        root=tk.Tk() # creates pop-up window
        root.update() # necessary to close tk dialog after askopenfilename is finished
        # tk dialog asks for a single station file
        full_path = tk.filedialog.asksaveasfile(title = 'Save schedule',
                                filetypes=[ ('csv','*.csv')] )
        root.destroy() # closes pop up window
        return full_path
        
    return

def convertDts(sched):
    '''
    
    '''
    # sometimes imports as 10/30/2018 0:00
    sched['Date']=sched['Date'].str.split(' ').str[0]
    # TODO finish me
    return 

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
        sched=pd.read_csv(myPath, encoding='cp437')
    elif myPath.endswith('.xls) or myPath.endswith('.xlsx):
        sched=pd.read_excel(myPath)
    else:
        print('Schedule file must be CSV or Excel')
    return sched

def compareSched(sched, oldsch):
    '''
    Detect schedules which have altered games, print teams and return changed
    games
    '''
    bothsch=pd.concat([sched,oldsch])
    changed=bothsch.drop_duplicates(['Date','Time','Location'],keep=False)
    changed=changed.sort_values(['Division','Date','Time'])
    if len(list(changed.Team.unique()))>0:
        print('Changed schedule for ', ', '.join(list(changed.Team.unique())))
    return changed
    
def getTeamsDict(teams, sport):
    '''
    CYC sched has Cab teams with embedded coach name and division 
    make dict w/ coach name, div and team name as value 
    '''
    tdict={}
    cteams=teams[~teams['Team'].str.contains('#')]
    coachlist=list(cteams.Coach.unique())
    for i, coac in enumerate(coachlist):
        tdict[coac]=list(cteams[cteams['Coach']==coac].Team.unique())
    # TODO implement sport filter
    cteams=cteams[cteams['Team'].str.contains('-')] # CYC teams w/ division
    # TODO finish me 
    return
    
def getTeamDicts(teams, sport):
    '''
    Need dict for lookup of team name (Team col) by sport
    Key is 3B, 5G and val is team name, coach last name
    '''
    teams2=teams[ teams['Sport']==sport]
    teamdivdict={}
    coachdict={}
    # Ensure no duplicates for division
    grouped=teams2.groupby(['Gender','Grade'])
    for (gend, gr), group in grouped:
        if len(group)!=1:
            print('Multiple teams for ', gr, gend)
            continue
        else:
            try:
                coachdict[group.iloc[0]['Coach']]=group.iloc[0]['Team']
            except:
                pass
            if gend=='m':
                # division should match that from Pat Moore schedule
                mykey=str(group.iloc[0]['Grade'])+'B'
                teamdivdict[mykey]=group.iloc[0]['Team']
            elif gend=='f':
                mykey=str(group.iloc[0]['Grade'])+'G'
                teamdivdict[mykey]=group.iloc[0]['Team']
            else:
                print('Gend problem for', gr, gend)
    return teamdivdict, coachdict

def prepGdSchedule(sched, teams, sport):
    '''
    Convert allteams schedule (from Pat Moore/CYC google drive) usually Excel to usable Cabrini 
    teams format
    Need to find matching Cabrini team name
    '''
    
    #sched.columns=['Gamenum','Visitor', 'Vis', 'Home', 'Home2', 'Date','Time', 'Venue','Ven','Days']
    if len(sched.columns)==10:
        sched.columns=['GameNum','Away', 'Vis', 'Home', 'Home2', 'Date','Time', 'Location','Ven','Days']
    elif len(sched.columns)==9:
        sched.columns=['GameNum','Away', 'Vis', 'Home', 'Home2', 'Date','Time', 'Location','Ven']
    elif len(sched.columns)==13: # 8/2019 Pat Moore structure
        sched.columns=['GameNum','Date','Time','Day','Home','Away','Location','HScore','VScore', 'Division','Status','Assignments','Notes']
    else:
        print('Examine for new column structure')
        return
    # Filter for Cabrini teams only
    sched=sched[sched['Home'].str.contains('Cabrini') | sched['Away'].str.contains('Cabrini') ]
    ''' no longer needed w/ new division column 
    sched['Division']=''
    # Find division from within name field
    for index, row in sched.iterrows():
        if re.match('\d{1}\w{2}',row.Vis):
            sched.loc[index]['Division']=re.match('\d{1}\w{2}',row.Vis).group(0)
            # sched=sched.set_value(index, 'Div', re.match('\d{1}\w{2}',row.Vis).group(0) )
    # Needed because all schedule games listed under both teams (no longer true)
    sched=sched.drop_duplicates(['Date','Time','Vis','Home2'])
    '''
    # Sorting by date requires datetime
    # TESTING val=sched.iloc[0]['Date']  datetime.strptime(val, '%m/%d/%Y')
    if isinstance(sched.iloc[0]['Date'],str):
        sched['Date']=sched['Date'].str.split(' ').str[0] # strip of time string
        sched.Date=sched.Date.apply(lambda x:datetime.strptime(x,'%m/%d/%Y'))
    elif isinstance(sched.iloc[0]['Date'],datetime):
        sched.Date=sched.Date.apply(lambda x:x.date()) # just convert to date 
    # TODO check formatting of time column 
    # Drop duplicates... can pick up same game twice (from Cab schedule and opposing team)
    sched=sched.sort_values(['Division','Date','Time'])
    # lookup of cabrini teams from division and/or coach name
    teamdivdict, coachdict=getTeamDicts(teams, sport)
    # Find day of week from date
    sched['Team']=''
    
    def setWeekDay(val):
        # determine day of week from date
        days=['Mon','Tues','Wed','Thurs','Fri','Sat','Sun'] # day order for .weekday()
        try:
            return days[val.weekday()]
        except:
            return ''
    sched['Day']=sched['Date'].apply(lambda x:setWeekDay(x))
    def setTeam(div):
        # Set Team column to match Cabrini team name (used by SC_messaging)
        # div will be "2BD" but teamdict match for Cabrini teams is "2B"
        try:
            if div[0:2] in teamdivdict:
                return teamdivdict.get(div[0:2])
            else:
                return ''
        except:
            print('Problem setting Cabrini team name')
    sched['Team']=sched['Division'].apply(lambda x:setTeam(x))
    sched=sched[['Date','Day','Time','Home','Away','Division','Location','Team']]
    return sched

