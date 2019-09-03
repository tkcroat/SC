# -*- coding: utf-8 -*-
"""
Created on Sun May 22 10:25:19 2016
Process signups from google drive
@author: tkc
"""
#%% 
import pandas as pd
import os
import pkg.SC_signup_functions as SC
import pkg.SC_config as cnf
#%%
from importlib import reload
reload(SC)
reload(cnf)
#%% Load and process raw signup file from Fall2016_signups.xlsx
# raw tab contains unprocessed google drive signups plus selected info from paper
os.chdir('C:\\Users\\kevin\\Documents\\Python_Scripts\\SC\\')
os.chdir(cnf._OUTPUT_DIR)
signupfile='Winter2017_signups.xlsx'
signupfile='Spring2017_signups.xlsx'
signupfile='Fall2018_signups.xlsx'
signupfile=cnf._INPUT_DIR +'\\Fall2019_signups.csv'
signupfile=cnf._INPUT_DIR +'\\Fall2019_signups.xlsx'


# Load signups,player and family contact info; format names/numbers, eliminate duplicates
players, famcontact, SCsignup, season, year = SC.loadprocessfiles(signupfile)

# Find player number and assign to signup rows
SCsignup, players, famcontact =SC.findplayers(SCsignup, players, famcontact)

# Save SC signups back to xls file (incl. altered names)
SC.writetoxls(SCsignup,'Raw', signupfile)
os.chdir(cnf._INPUT_DIR)
SCsignup.to_csv(signupfile,index=False) # csv version

# Update missing info for manually entered players (no full google drive entry info)
SCsignup = SC.findmissinginfo(SCsignup, players, famcontact)
SCsignup = findmissinginfo(SCsignup, players, famcontact)

#%% Process data changes from google drive info... works but check/correct using log
# email, phone, parent names, address changes (house # detection)
players, famcontact=SC.processdatachanges(SCsignup, players, famcontact, year)

players, famcontact=processdatachanges(SCsignup, players, famcontact, year)

# load Mastersignups and add signups to master signups list (duplicates eliminated so no danger with re-run)
Mastersignups = pd.read_csv(cnf._INPUT_DIR +'\\\master_signups.csv', encoding='cp437') 
Mastersignups = SC.createsignups(SCsignup, Mastersignups, season, year) # new signups are auto-saved

# Summarize signups by sport-gender-grade (written into signup file)
# TODO fix... redirect to output_dir
SC.summarizesignups(Mastersignups, season, year, signupfile)
SC.summarizesignups(Mastersignups, season, year, signupfile, **{'saveCSV':True}) # save to season_yr_signup_summary.csv (not Excel)

# Manually create desired teams in Teams_coaches.xlsx (teams tab should only have this sport season not older teams)
teams=pd.read_excel('Teams_coaches.xlsx', sheetname='Teams')
teams=pd.read_csv(cnf._INPUT_DIR +'\\Teams_2019.csv', encoding='cp437')
coaches=pd.read_excel('private\\Teams_coaches.xlsx', sheetname='Coaches') # load coach info
coaches=pd.read_csv(cnf._INPUT_DIR +'\\coaches.csv', encoding='cp437') # common excel file encoding

coaches.to_csv('coaches.csv', index=False)

# Update teams (manual edit or using update script)
teams=SC.updateoldteams(teams,year)
teams.to_csv('private\\Teams_2019.csv', index=False)
SC.writetoxls(teams,'Teams','teams_coaches.xlsx') # save fsupdated teams to tab in teams_coaches xls file

# Now assign this season/years players to teams based on Teams xls file
# Overwrite=True resets all existing custom player assignment (i.e. single 2nd grader playing on 3rd team)
# Overwrite=False will not change any existing team assignments (only finds team for new signups)
Mastersignups=SC.assigntoteams(Mastersignups, season, year, teams, overwrite=False)
Mastersignups=assigntoteams(Mastersignups, season, year, teams, overwrite=False)

temp=Mastersignups[(Mastersignups['Year']==2017) & (Mastersignups['Sport']=='Track')]
# Track sub-team assigned based on DOB calculation (TEAM ASSIGNMENTS NOT AUTOSAVED)
Mastersignups=SC.assigntrackgroup(Mastersignups, year, players)
Mastersignups.to_csv(cnf._INPUT_DIR + '\\master_signups.csv',index=False)

# if any players are playing up at different grade, just manually change team name in master_signups.csv (and use overwrite False)
# also manually edit select players to open status

# team contact lists to separate sport Excel tabs (Warning... this overwrites existing version)
SC.writecontacts(Mastersignups, famcontact, players, season, year)

# Make google compatible contacts list for all Cabrini teams (auto-save to csv)
SC.makegoogcont(Mastersignups, famcontact, players, season, year)

# Find missing players and add to recruits tab of signupfile
# after all new signups added, just looks for those signed up last year but not this
SC.findrecruits(Mastersignups, players, famcontact, season, year, signupfile)

# TODO fix countteamplayers for co-ed teams
teams=SC.countteamplayers(Mastersignups, teams, season, year) # summarizes players assigned to teams, autosaved to teams tab

Mastersignups.to_csv('master_signups.csv', index=False)

# Create 5 separate rosters (Cabrini CYC soccer & VB, soccer & VB transfers, junior teams (incl. age) incl. coaches
acronyms=pd.read_csv(cnf._INPUT_DIR+'\\acronyms.csv') # parish and school acronyms
SC.createrosters(Mastersignups, season, year, players, teams, coaches, famcontact, acronyms)
# Create contact lists for each team's coach

# Package transferred player info and create email messages to other directors/schools
messfile='messages\\player_transfer_director.txt'
SC.packagetransfers(teams, Mastersignups, famcontact, players, season, year, acronyms, messfile)

# Load transfers from other schools
transroster=pd.read_excel('Cecilia_to_Cabrini_fall_2017.xls')
SCsignup=loadtransfers(transroster, SCsignup)
SC.writetoxls(SCsignup,'Raw', signupfile) # saves changes to master Excel file
# TODO Add fake payments for transferred players ... done manually

# Track event registration (Pat Moore spreadsheet)
os.chdir('C:\\Users\\tkc\\Documents\\Python_Scripts\\SC')
trackevents=pd.read_excel('track_summary_2018.xlsx', sheetname='Summary')
# output file for Pat Moore (not needed but check consistency)
regsheet=pd.read_excel('Track_Registration_Form_2018.xlsx', 
                       sheetname='RegistrationSheet', skiprows=2)

# using track summary input sheet, translate into Pat Moore format
regfile=SC.readbackevents(trackevents)
# Copy and paste this file into 
regfile.to_csv('track_reg_file.csv', index=False)

# TODO finish this
SC.maketrackroster(Mastersignups, players, year) 

# rename team in teams_coaches, mastersignups, 

# Detect any roster changes made by Pat Moore
myroster=pd.read_csv('Cabrini_Soccerroster2019.csv',encoding='cp437')
PMroster=pd.read_csv('Cabrini_Soccerroster2019_PM.csv',encoding='cp437')

myroster=pd.read_csv('Cabrini_VBroster2019.csv',encoding='cp437')
PMroster=pd.read_csv('Cabrini_VBroster2019_PM.csv',encoding='cp437')

alteredrows=SC.detectrosterchange(PMroster,myroster)
alteredrows.to_csv('changed_players.csv', index=False)

test=alteredrows[alteredrows['Lname']=='Chavez']

# Make CYC card images for 3rd and up teams
missingcards=SC.makeCYCcards(Mastersignups, players, teams, coaches, season, year)
missingcards=makeCYCcards(Mastersignups, players, teams, coaches, season, year)
