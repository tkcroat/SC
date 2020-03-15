# -*- coding: utf-8 -*-
"""
Sponsors club billing main program
Created on Sat Oct  1 13:53:36 2016

@author: tkc
"""

#%% 
import pandas as pd
import os, sys

import pkg.SC_signup_functions as SC
import pkg.SC_billing_functions as SCbill
import pkg.SC_signup_google_API_functions as SCapi
import pkg.SC_config as cnf
#%%
from importlib import reload
reload(SCbill)

#%%
paylog = SCapi.readPaylog()

payPygSheet, paylog = readPaylog() # Return as pyg sheet and as dataframe
paylog_mod, newplayers=SCbill.matchpayment(paylog, players)

new=paylog[paylog['Paykey']>=349]

players, famcontact = SC.loadProcessPlayerInfo()
Mastersignups = pd.read_csv(cnf._INPUT_DIR +'\\master_signups.csv', encoding='cp437') 
teams=pd.read_csv(cnf._INPUT_DIR +'\\Teams_2019.csv', encoding='cp437')
coaches=pd.read_csv(cnf._INPUT_DIR +'\\coaches.csv', encoding='cp437') 
season='Winter'
year=2019
#%%  New method w/ pygsheets
pygSheet, paylog = readPaylog()


#%%
# Backup of paylog to local excel file 

# load old teams from any prior season/ year combination (overwrites current teams)
teams=SCbill.loadoldteams('Spring', 2017) 
teams=SCbill.loadoldteams(['Fall','Winter'], [2015,2016]) # load a bunch of old teams
# Family Billing 

# assign existing payments to players (needed every time new payment is entered)... does not autosave
paylog_mod, newplayers=SCbill.matchpayment(paylog, players)

# save modified paylog to tab of xls file (not autosaved )
SC.writetoxls(paylog,'Paylog','Payment_logbook.xlsx') 

# load teams from prior sports season

teams=SCbill.loadoldteams('Fall', 2017) # load prior season's teams
teams=SCbill.loadoldteams(['Fall','Winter'], [2016,2017])

# New tk interface for send/test ebills
ebilllist, skiplist=SCbill.sendbills_tk(Mastersignups, paylog, famcontact, players, season, year, teams)

# Create billing list for current sports season (auto-saved to file)
kwargs={}
kwargs.update({'olduni':True}) # make message about uni return 
kwargs.update({'newuni':True}) # include info about new uni pick-up (skip for later send)
bills=SCbill.createbilllist(Mastersignups, paylog, famcontact, players, season, year, 
                            teams, priorseasons=1, fname='Billlist_26Sept18.csv', **kwargs)
# Reload if any manual edist are made
bills=pd.read_csv('Billlist_26Sept18.csv', encoding='cp437')

# Save above mastersignups after copy over of uniform night info (STILL TESTING... ensure same length)
Mastersignups.to_csv('master_signups.csv',index=False)
# Check master signups against master uniform log and update this

# Load billing test list
billlist=pd.read_csv('billlist_12Aug17.csv', encoding='cp437')\
# unilist ... is this missing uniforms list?
unilist=pd.read_csv('uni_return_no_fee_12May17.csv', encoding='cp437')

# EMAIL BILLING
messagefile='messages\\ebill_uninight_fall.txt' # longer text file with some find replace strings
messagefile='messages\\ebill_spring.txt'
messagefile='messages\\ebill_spring_uni_only_no_fee.txt'
coachmessage='messages\\ebill_uninight_coaches.txt'

emailtitle='Cabrini Sports Uniforms tomorrow at Open House 2-4 PM'
emailtitle='Cabrini Sports Fees for Spring (and Winter) are due.'
emailtitle='Info for your team on Cabrini Uniform Night Wed Jan 4 6-8PM' # for e-mail to coaches

textheader='On Jan 4th from 6-7:30PM at the Cabrini gym, please '
textheader='Please ' # generic payment or return request (but need to remove pick up of unis)

# E-MAIL LOGIC for who gets an SMS gateway or email message...
# If olduni, newuni or fees are true, having outstanding uniform, needing new uni or owing fees will trigger a message
# Last 3 true only skips people who have nothing to be contacted about (i.e. paid up junior team player)

# TEST OF FAMILY SPECIFIC E-MAIL AND SMS (write to two separate txt log files)
kwargs={}
kwargs.update({'SMS':textheader}) # if sending SMS bills, pass beginning of text message
kwargs.update({'fees':True}) # send e-mail to subset that owe fees 
kwargs.update({'olduni':True}) # send e-mail to those with old uniform issues
kwargs.update({'newuni':True}) # send e-mail to those with new uniforms to pick up
             
SCbill.testautobilling(billlist, Mastersignups, season, year, emailtitle, messagefile, **kwargs)

skiplist=testautobilling(unilist, Mastersignups, season, year, emailtitle, messagefile, **kwargs)

billlist, skiplist=SCbill.sendebills(billlist, Mastersignups, season, year, emailtitle, messagefile, **kwargs)

# Send e-mail message to skiplist (fees paid but do have unis to return)
billlist, skiplist=sendebills(unilist, Mastersignups, season, year, emailtitle, messagefile, **kwargs)
# E-mail list of outstanding team fees to team's coach

