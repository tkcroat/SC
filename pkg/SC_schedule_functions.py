# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 06:46:15 2017

@author: tkc
"""
import pandas as pd
import re
from datetime import datetime

def convertDts(sched):
    '''
    
    '''
    # sometimes imports as 10/30/2018 0:00
    sched['Date']=sched['Date'].str.split(' ').str[0]

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
        sched.columns=['Gamenumber','Away', 'Vis', 'Home', 'Home2', 'Date','Time', 'Location','Ven','Days']
    elif len(sched.columns)==9:
        sched.columns=['Gamenumber','Away', 'Vis', 'Home', 'Home2', 'Date','Time', 'Location','Ven']
    else:
        print('Examine for new column structure')
        return
    sched=sched[sched['Home'].str.contains('Cabrini') | sched['Away'].str.contains('Cabrini') ]
    sched['Division']=''
    for index, row in sched.iterrows():
        if re.match('\d{1}\w{2}',row.Vis):
            sched.loc[index]['Division']=re.match('\d{1}\w{2}',row.Vis).group(0)
            # sched=sched.set_value(index, 'Div', re.match('\d{1}\w{2}',row.Vis).group(0) )
    # Find team name (from division)... 
    # Needed because all schedule games listed under both teams
    sched=sched.drop_duplicates(['Date','Time','Vis','Home2'])
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
    sched['Day']=''
    sched['Team']=''
    days=['Mon','Tues','Wed','Thurs','Fri','Sat','Sun']
    for index, row in sched.iterrows():
        # keep only grade/gender
        divval=row.Division[0:2]
        if divval in teamdivdict:
            sched.loc[index]['Team']=teamdivdict.get(divval)
        else:
            print("Couldn't find team for div", divval)
        # Get weekday
        sched.loc[index]['Day']=days[row.Date.weekday()]

    sched=sched[['Date','Day','Time','Home','Away','Division','Location','Team']]
    #TODO need to make Cabrini team column matching teams xls file
    # currently doing this manually
    return sched

