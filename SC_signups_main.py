
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
import pkg.SC_signup_google_API_functions as SCapi

# /from pandas_ods_reader import read_ods # too slow

#%%
from importlib import reload
reload(SC)
reload(cnf)
#%% Load and process raw signup file from Fall2016_signups.xlsx
# raw tab contains unprocessed google drive signups plus selected info from paper
os.chdir('C:\\Users\\kevin\\Documents\\Python_Scripts\\SC\\')
os.chdir(cnf._OUTPUT_DIR)
signupfile='Winter2017_signups.xlsx'
signupfile='Spring2019_signups.xlsx'
signupfile='Fall2018_signups.xlsx'
signupfile=cnf._INPUT_DIR +'\\Fall2019_signups.csv'
signupfile=cnf._INPUT_DIR +'\\Fall2019_signups.xlsx'
signupfile=cnf._INPUT_DIR +'Spring2019_signups.xlsx'


#%% Testing new google sheets API download
# ID and range of Fall 2020 (up to Gkey)
sheetID = '1mexU5HW8Va1QXN43eN2zvHQysJINw6tdwJ7psOKmQng'
rangeName = 'Form Responses!A:AX' # get allinclude plakey/famkey manual mode'

# ID and range of Winter 2019 basketball
sheetID = '182QFOXdz0cjQCTlxl2Gb9b_oEqInH93Peo6EKkKod-g'
rangeName = 'Form Responses 1!A:AC' # include plakey/famkey manual mode'

# spring signups
sheetID='1lppbr8srsVbN48RYrfRr58sd7yfUnJM21sSSx2C0mG8'
rangeName = 'Form Responses!A:Z' # include plakey/famkey manual mode'

gsignups = SCapi.downloadSignups(sheetID, rangeName)
# TODO write unique Gkey column... assign values 
season='Fall'
year=2020
# Load signups,player and family contact info; format names/numbers, eliminate duplicates
players, famcontact, gsignups = SC.loadProcessGfiles(gsignups, season, year)
players, famcontact = SC.loadProcessPlayerInfo() # version w/o signup processing

# Preliminary summary of signups (w/o ID or master signups assignments)

coach=SC.findCoaches(gsignups, **{'gradeGenders':
    [ [0,'m'],[0,'f'],[1,'m'],[1,'f']] }) # Co-ed K-1 team
coach=SC.findCoaches(gsignups) # coach candidates all grade/genders

#%%

# Find player number and assign to signup rows
# SCsignup, players, famcontact =SC.findplayers(SCsignup, players, famcontact)
# test w/ gsignups
gsignups, players, famcontact =SC.findplayers(gsignups, players, famcontact, year)

# Save SC signups back to xls file (incl. altered names)
SC.writetoxls(SCsignup,'Raw', signupfile)
os.chdir(cnf._INPUT_DIR)
SCsignup.to_csv(signupfile,index=False) # CSV version

#TODO save method back to google signups? 

# Update missing info for manually entered players (no full google drive entry info)
SCsignup = SC.findmissinginfo(gsignups, players, famcontact)
SCsignup = findmissinginfo(SCsignup, players, famcontact)

unmatch=gsignups[pd.isnull(gsignups['Plakey'])]

#%% Process data changes from google drive info... works but check/correct using log
# email, phone, parent names, address changes (house # detection)
players, famcontact=SC.processdatachanges(gsignups, players, famcontact, year)

players, famcontact=processdatachanges(gsignups, players, famcontact, year)

# load Mastersignups and add signups to master signups list (duplicates eliminated so no danger with re-run)
Mastersignups = pd.read_csv(cnf._INPUT_DIR +'\\\master_signups.csv', encoding='cp437') 
Mastersignups = SC.createsignups(gsignups, Mastersignups, season, year) # new signups are auto-saved

# Summarize signups by sport-gender-grade (written into signup file)
# TODO fix... redirect to output_dir
SC.summarizesignups(Mastersignups, season, year, **{'XLSpath':signupfile}) # write to tab in excel signup file
SC.summarizesignups(Mastersignups, season, year, **{'saveCSV':True}) # save to season_yr_signup_summary.csv (not Excel)
# gsignups version
# TODO make a summary tool before/without adding to master signups
# Feasibility before official signup, but needs split of multiple signups
sportsumm=SC.summarizesignups(gsignups, season, year, **{'toDf':True})
SC.summarizesignups(gsignups, season, year) # save to csv
SC.summarizesignups(gsignups, season, year, **{'XLSpath':signupfile}) # save to sheet in xls signup


# Manually create desired teams in Teams_coaches.xlsx (teams tab should only have this sport season not older teams)
# TODO really slow... find a replacement method for .ods reads
teams=pd.read_csv(cnf._INPUT_DIR +'\\Teams_2019.csv', encoding='cp437')
#teams=pd.read_excel('Teams_coaches.xlsx', sheetname='Teams') # 
# teams = read_ods(cnf._INPUT_DIR +'\\Teams_coaches.ods', 'Teams') # read ods team file


#coaches = read_ods(cnf._INPUT_DIR +'\\Teams_coaches.ods', 'Coaches') # read ods team file
#coaches=pd.read_excel('private\\Teams_coaches.xlsx', sheetname='Coaches') # load coach info
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
messfile=cnf._INPUT_DIR+'\\messages\\player_transfer_director.txt'
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
myroster=pd.read_csv(cnf._OUTPUT_DIR+'\\Cabrini_Basketballroster2019.csv',encoding='cp437')
PMroster=pd.read_csv(cnf._OUTPUT_DIR+'\\Cabrini_Basketballroster2019_PM.csv',encoding='cp437')

myroster=pd.read_csv('Cabrini_VBroster2019.csv',encoding='cp437')
PMroster=pd.read_csv('Cabrini_VBroster2019_PM.csv',encoding='cp437')

alteredrows=SC.detectrosterchange(PMroster,myroster)
alteredrows.to_csv(cnf._OUTPUT_DIR+'\\roster_changes.csv', index=False)

test=alteredrows[alteredrows['Lname']=='Chavez']

# Make CYC card images for 3rd and up teams
missing = SC.makeCYCcards(Mastersignups, players, teams, coaches, season, year) # only good cards
missing = SC.makeCYCcards(Mastersignups, players, teams, coaches, season, year, **{'showmissing':True} )
