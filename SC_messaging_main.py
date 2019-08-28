# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:41:41 2017

@author: tkc
"""
import pandas as pd
import os, sys
if 'C:\\Users\\tkc\\Documents\\Python_Scripts\\SC' not in sys.path:
    sys.path.append('C:\\Users\\tkc\\Documents\\Python_Scripts\\SC')
    print ('SC folder added')
import pkg.SC_signup_functions as SC
import pkg.SC_messaging_functions as SCmess

#%%
from importlib import reload
reload(SCmess)
#%%

os.chdir('C:\\Users\\tkc\\Documents\\Python_Scripts\\SC')
signupfile='Winter2017_signups.xlsx'
signupfile='Spring2017_signups.xlsx'
signupfile='Fall2018_signups.xlsx'
# Load signups,player and family contact info; format names/numbers, eliminate duplicates
players, famcontact, SCsignup, season, year = SC.loadprocessfiles(signupfile)
teams=pd.read_excel('Teams_coaches.xlsx', sheetname='Teams')
coaches=pd.read_excel('Teams_coaches.xlsx', sheetname='Coaches') # load coach info
Mastersignups = pd.read_csv('private\\master_signups.csv', encoding='cp437') 
# Teams folder under each season? 
gdrivedict={
    '$GDRIVEWINTER':'https://drive.google.com/open?id=0B9k6lJXBTjfiLVFBMlN1aWpoSEk',
    '$GDRIVEFALL':'https://drive.google.com/open?id=1DU-6x6wqOkiiAh5OvlzKAsombspgYAnq',
    '$GDRIVE_SCHEDULING':'https://docs.google.com/forms/d/e/1FAIpQLSf_f7d1eHXn8Kfm75sqM0Wvv3CKPUemI-GWRWddSkIAqdd_6Q/viewform'
    }
#%% 
''' Messages to parents: 1) team assignment 2) Recruit missing players 3) missing unis 
    4) send schedule 5) other message 6) all parent message
    
'''

SCmess.emailparent_tk(teams, signupfile, season, year)

# testing ssl connections/ troubleshooting
from urllib.request import urlopen
res = urlopen('https://www.howsmyssl.com/a/check').read()  # tls version is 1.2
#%% Messages to coaches
# 1) missing uniforms (coach summary) 2) send team contact lists 3) send bill summary 
#    4) other/generic
# missing unis will auto-load old teams
# TODO add sendschedule option
SCmess.emailcoach_tk(teams, coaches, gdrivedict)

# Testing
notifyfamilies(teams, Mastersignups, year, famcontact, emailtitle, blankmess, **kwargs)

teams=teams.drop_duplicates('Team')
mtype='recruit'
mtype='teamassign' # notification of team assignment and CYC card status 
#%% Messages to recruits  (load after editing)
Recruits=pd.read_excel(signupfile, sheetname='Recruits')

emailtitle='Cabrini-Soulard sports for $FIRST this fall?'
messagefile='messages\\player_recruiting.txt'
SCmess.emailrecruits(Recruits, emailtitle, messagefile)

#%% Messages to all sports parents (typically last 3 seasons) 
# Return email list for all players this season and up to prior year of same season
emaillist=SCmess.makeemaillist(Mastersignups, famcontact, season, year, SMS=False)

emailstr=', \r\n'.join(emaillist)
emaillist.to_csv('email_list_3Oct18.csv')
#%% Messages to coaches
SCmess.emailcoach_tk(teams, coaches, gdrivedict)

# Send team billing summary to (head) coaches: team bill summary, contact list,
mtype='bills'; mtype='contacts'; mtype='unis';  # choose message type

kwargs={}
# needed for billing 
emailtitle='Fees still owed by your Cabrini team'
messagefile='messages\\coach_email_outstanding_bills.txt'
kwargs.update({'asst':False}) # Optional send to asst. coaches if set to True
billlist=pd.read_csv('Billlist_18Jan17.csv', encoding='cp437') # pruned bill list current season only balances owed
Mastersignups = pd.read_csv('master_signups.csv', encoding='cp437')
kwargs.update({'bills':billlist, 'SUs':Mastersignups})

# needed for team contacts (mtype contacts)
emailtitle='Contact list for your Cabrini team'
messagefile='messages\\coach_email_contacts.txt'
gdrive='https://drive.google.com/open?id=0B9k6lJXBTjfiVDJ3cU9DRkxEMVU' # Sharable link for this season
kwargs.update({'asst':True}) # Optional send to asst. coaches if set to True
kwargs.update({'SUs':Mastersignups,'players':players,'famcontact':famcontact})
kwargs.update({'gdrive':gdrive}) # google drive link for this season

# Needed for outstanding uniform return
kwargs={}
mtype='unis'
missing=pd.read_csv('missingunilist_27Apr17.csv', encoding='cp437')
oldteams=pd.read_excel('Teams_coaches.xlsx', sheetname='Oldteams') # loads all old teams in list
kwargs.update({'mformat':'txt'}) # html or string/text message format (testing only)
kwargs.update({'oldteams':oldteams,'missing':missing})
kwargs.update({'asst':False}) # Optional send to asst. coaches if set to True
messagefile='messages\\coach_email_outstanding_unis.txt'
emailtitle='Return of uniforms for your Cabrini team'

messagefile='coach_email_log_29Apr17.html' # test send
# Write batch e-mails to coaches into html log file
SCbill.testcoachemail(teams, coaches, mtype, emailtitle, messagefile, **kwargs)

SCbill.emailcoaches(teams, coaches, mtype, emailtitle, messagefile, **kwargs)

