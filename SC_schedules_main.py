# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:22:49 2017

@author: tkc
"""
import pandas as pd
import os
import datetime
import sys
import numpy as np

import pkg.SC_messaging_functions as SCmess
import pkg.SC_schedule_functions as SCsch
import pkg.SC_config as cnf # specifies input/output file directories
#%%
from importlib import reload
reload(SCsch)
reload(SCmess)
#%% Download from google sheets Cabrini basketball schedule
sheetID = '1-uX2XfX5Jw-WPw3YBm-Ao8d2DOzou18Upw-Jb6UiPWg'
rangeName = 'Cabrini!A:G'
cabsched = SCapi.downloadSheet(sheetID, rangeName)

#%% Load of other commonly needed info sheets
teams=pd.read_csv(cnf._INPUT_DIR +'\\Teams_2019.csv', encoding='cp437')
coaches=pd.read_csv(cnf._INPUT_DIR +'\\coaches.csv', encoding='cp437')
fields=pd.read_csv(cnf._INPUT_DIR+'\\fields.csv', encoding='cp437')
Mastersignups = pd.read_csv(cnf._INPUT_DIR +'\\\master_signups.csv', encoding='cp437') 
players, famcontact = SC.loadProcessPlayerInfo() # version w/o signup processing
season='Winter'
year=2019
#%% Create all schedules and write to text log (non-auto emailed version)
emailtitle='Game Schedules for $TEAMNAME'
blankmess=SCmess.readMessage() # choose and read blank message from chosen *.txt
cabsched=SCsch.alterSchedule(cabsched) # day and division changes for consistency to previous
# write of all team schedules to parent_email_log (default choice)
SCmess.sendschedule(teams, cabsched, fields, Mastersignups, coaches, year, famcontact, emailtitle, blankmess)

#%%

# Read tentative google drive Pat Moore schedules (after delete of cols before header row)
sched=pd.read_csv(cnf._OUTPUT_DIR+'\\Schedules\\Bball2019_full_schedule.csv')
# Read of full xlxs by league file... good format for schedule extraction
# However csv file has separated schedules
sched=pd.read_csv(cnf._OUTPUT_DIR+'\\Schedules\\Bball2019_full_schedule.csv')

sched=pd.read_excel('C:\\Temp\\allTeams.xlsx')
sched=pd.read_excel(cnf._OUTPUT_DIR+'\\Schedules\\BB2019_full_schedule.xlsx')
fullsched=pd.read_excel('CYC_soccer_2019.xlsx')

# Load full schedule (Pat moore excel format)
fullsched=pd.read_excel('Soccer2019 By League.xlsx')
fullsched=pd.read_csv('Soccer.csv')
fullsched=SCsch.prepGdSchedule(fullsched, teams, 'Soccer')

# Find changed schedules, return altered games
sched=SCsch.loadSchedule()  # Reload existing Cabrini-only schedule (post-processing)
sched=pd.read_csv('Cab_soccer_schedule_30Aug18.csv')
oldsch=pd.read_csv('Cab_soccer_schedule_26Aug18.csv')
changed=SCsch.compareSched(sched, oldsch)

# Load CYC full schedule and produce sub-schedule
fullsched=pd.read_excel('BB2018_schedule.xlsx')
sched=pd.read_csv('Cab_Bball_schedule_24Dec18.csv')
sched=pd.read_csv('Cabrini_2017_VB_soccer_schedule.csv')
sched2=pd.read_csv('Cabrini_VB2017_schedule.csv')

# load old teams

# Get subset of full schedule for Cabrini teams (and Cab transfer teams)
kwargs={}
kwargs.update({'div':'5G'}) # optional sub-sch for only 
kwargs.update({'school':'Cabrini'}) # get cabrini schedules by school
kwargs.update({'sport':'Soccer'}) 
kwargs.update({'sport':'VB'}) 
cabsched=SCmess.getcabsch(fullsched, teams, coaches, fields, **kwargs)
cabsched.to_csv(cnf._OUTPUT_DIR + '\\Cab_Basketball2019_schedule_26Dec19.csv', index=False) # save (used for sendschedule, maketextsch, gcal, etc.)

# Compare schedule to previous and return altered rows
#%% CYC game rescheduler (prior to release)... swapping team opponents
sched=pd.read_excel(cnf._OUTPUT_DIR+'\\Schedules\\BB2019_full_schedule.xlsx')
sched=SCsch.prepSched(sched)

teamName='St Frances Cabrini-Clavin-6GD'
badDay=datetime(2020,1,11) # Team has two impossible to play games

teamName='St Frances Cabrini-Croat-7BD1'
badDay=datetime(2020,1,25) # Team has two impossible to play games

swapOld, swapNew, swapTeam = findTeamSwap(teamName, badDay, sched, gameRank=0)

swapOld, swapNew, swapTeam = findTeamSwap(teamName, badDay, sched, **{'badTime':'7:30 PM'})

# swapping same teams to new datetime/venue.. harder
gymsched=pd.read_excel(cnf._OUTPUT_DIR+'\\Schedules\BB2019_Schedule_ByGym.xlsx')

avail = findGymSlot(gymsched, datetime(2020,2,15)) #Sun

thisSched=getSchedule(sched, 'Annunciation-Handal-6GD')


#%%
# Make sports google calendars
kwargs={}
kwargs.update({'splitcal':False}) # single jumbo calendar option 
kwargs.update({'school':'Cabrini'}) # Cabrini teams only
kwargs.update({'division':'6B'})
SCmess.makegcals(cabsched, teams, coaches, fields, season, year, duration=1, **kwargs)

# make game cards from given schedule
sched=pd.read_csv('Cab_soccer_schedule_23Aug18.csv') # reload
gctemplate=cnf._INPUT_DIR+'\\game_card_soccer_template.xlsx' # for soccer
gctemplate='game_card_VB_template.xlsx'
gctemplate='game_card_bball_template.xlsx' # for soccer

pastelist=pd.read_excel(cnf._INPUT_DIR+'\\excel_python_insert_template.xlsx', sheet_name=1) # currently same for soccer and VB
pastelist=pd.read_excel('excel_python_insert_template.xlsx', sheet_name='bball')
SCmess.gamecardmaker(teams, coaches, Mastersignups, sched, pastelist, gctemplate)

# Make all available game schedules for SMS (save to txt file for send to SMS email addresses or direct text)
messagefile='parent_game_scheduleSMS.txt'
logfile='basketball_gameschedules_SMS.txt'
logfile='test.txt'
SCmess.maketextsched(sched, teams, coaches, fields, messagefile, logfile, **kwargs)

# Look for changed games between two versions
altered=SCmess.detectschchange(cabsched, sched2)
altered.to_csv('altered_games.csv',index=False)

# other optional subsets of schedule
cabsched.to_csv('Cabrini_2017_soccer_schedule_8sep17.csv', index=False)
cabsched=pd.read_csv('Cabrini_2017_soccer_schedule.csv')

# Make Cabrini sports calendar from extracted CYC schedule

makegcalCYC(thisteam,'Ethan baseball', 1.5) # single team

# Venue list
venues=np.ndarray.tolist(cabsched.Location.unique())

thisteam=SCmess.getCYCschedules(cabsched, **kwargs)
#%%
# Older version 
league='4B' # grade and B or G
school='Heller' # coach or school name
thisteam=schedule[(schedule['League']==league) & (schedule['Home'].str.contains(school)|schedule['Visitor'].str.contains(school))]
thisteam.to_csv('Ethan_4B_schedule.csv', index=False)

# Load league results

# Create google calendar from single team
makegcalCYC(thisteam,'Ethan baseball', 1.5)

# Load and read from standard Epiphany Tball schedule
Tball=pd.read_excel('Epiphany_1B_Tball.xlsx')
schedule=Tball[(Tball['HOME'].str.contains('frances',case=False)) | (Tball['AWAY'].str.contains('frances',case=False))]
schedule.to_csv('Tball_2017.csv',index=False)

Tballgcal=makegcal(schedule)
#%%  Pulling schedules for SFC teams from OLS 
fname='C:\\Users\\tkc\\Documents\\Python_Scripts\\SC\\OLS_2017.xlsx'
Ols2017=parseOls(fname) # makes flattened OLS schedule
team='OLS/SFC/SSP KDG-1ST G'
team='OLS 2ND G'
team='OLS/SFC 1ST B 1'
team='OLS/SFC/SSP 2ND B 2'
team='OLS/SFC KDG B'

# Getting subset of Cabrini teams
team=teams[2]
thisteam=makeOLS(team,Ols)

teams=np.ndarray.tolist(Ols.Home.unique())+np.ndarray.tolist(Ols.Visitor.unique())
teams=set(teams)
teams=list(teams)
cabteams=[n for n in teams if 'SFC' in n]

Ols=Ols[Ols['Date']>datetime.date(2017, 3, 11)] # schedule going forward
Olsold=pd.read_csv('OLS_2017.csv', encoding='cp437')
thisteam=makeOLS(team,Olsold)
duration=1.5
df=thisteam

test=makegcalCYC(thisteam,'Ethan baseball', 1.5)
test.to_csv('test_cal.csv', index=False)

def makegcal(schedule):
    ''' Turn Epiphany Tball schedule into google calendar  '''
    mycols=['Start Date', 'Start Time', 'End Time', 'All Day Event', 'Description', 'Location','Private']    
    df=schedule.copy()
    df=df.rename(columns={'DATE':'Start Date','TIME':'Start Time'})
    df['HOME']=df['HOME'].str.title()
    df['AWAY']=df['AWAY'].str.title()
    df['All Day Event']='False'
    df['Location']='Epiphany '+ df['FIELD']
    df['Private']='FALSE'
    df['End Time']=df['Start Time'] + datetime.timedelta(hours=1)
    df['End Time']=pd.to_datetime(df['Start Time']) + datetime.timedelta(hours=1)
    df['All Day Event']='FALSE'
    df['End Time']=df['Start Time'].topydatetime 
    df['Description']='K-1 coed Tball: '+df['HOME']+' vs '+df['AWAY']
    df=df[mycols]
    return df

    
def makeOLS(team, Ols):
    ''' Make team schedule from OLS master schedule (after flattening structure into DB style)
    columns are ['Date', 'Time', 'Home', 'Visitor', 'Court'] '''
    team=team.strip()
    mask=Ols['Home'].str.contains(team) |Ols['Visitor'].str.contains(team)
    thisteam=Ols.loc[mask]
    fname=team.replace('/','-') +'.csv'
    thisteam.to_csv(fname, index=False)
    return thisteam

# Need to finish combination scripts 
pd.to_datetime(df['Start Date']+ ' ' + df['Start Time'])

df['Datetime']=datetime.datetime.combine(pd.to_datetime(df['Start Date']), df['Start Time'])
df['Start Date']+df['Start Time']

df['End Time']=df['Start Time'] + pd.Timedelta(hours=1)
val
df['End Time']=pd.to_datetime(df['Start Time']) + pd.Timedelta(hours=1)