# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 10:10:08 2018

@author: tkc
"""
import os, sys
import pandas as pd

import pkg.SC_billing_functions as SCbill
import pkg.SC_uniform_functions as SCuni
import pkg.SC_signup_google_API_functions as SCapi
import pkg.SC_config as cnf
import pkg.SC_signup_functions as SC

#%%
import pandas_utilities as pdutil
from importlib import reload
reload(SCuni)

#%% Load of commonly-needed files
teams=pd.read_csv(cnf._INPUT_DIR+'\\teams_2019.csv')
Mastersignups = pd.read_csv(cnf._INPUT_DIR+'\\master_signups.csv', encoding='cp437')
players, famcontact = SC.loadProcessPlayerInfo() # version w/o signup processing
paylog=SCapi.readPaylog()
#%% Uniform inventory prior to uniform night
# Read results of uniform inventory (
# g-docs inventory sheet with setname, size and list of numbers (in closet)
unis = SCapi.readInventory()

unilist= SCapi.readUniList() # read master list of unique unis and checkout info

# Inventory
SCuni.checkuni_duplicates(unilist) # check for non-unique uniforms from master unilist

# 
# Older stuff... legacy
# Load an inventory file
inventory=pd.read_excel('uniform_inventory.xlsx')
unilist=pd.read_excel(cnf._INPUT_DIR+'\\Master_uniform_logbook.xlsx',sheetname='Unilog')
unisumm=pd.read_excel(cnf._INPUT_DIR+'\\Master_uniform_logbook.xlsx',sheetname='Summary')
#%% 
''' For uniform night or issue, work from season_uniform_log multi-tabbed xls like (or
 google sheet format), then after event read back number/size/setname combos into 
master unilist; 
financial info separately entered into master payment log file (fees and deposits)... separate
process so financials in uniform_log is just a view-only (or convenient way to copy o

'''

# ISSUING UNIFORMS

# teams=pd.read_excel(cnf._INPUT_DIR+'\\Teams_coaches.xlsx', sheetname='Teams')
oldteams=SCbill.loadoldteams(['Fall','Winter'], [2015,2016,2017, 2018]) 

# Read back new info entered into uniform logs

# Transfer unreturned unis from prior season's signup (if unreturned) to this season's signup
Mastersignups=SCbill.transferunis(Mastersignups, season, year)
# Transfer VB uniforms to BB (for those playing both sports)
Mastersignups=SCbill.transferunisVBBB(Mastersignups, year)
# TODO double check to ensure that this works
Mastersignups.to_csv('master_signups_test.csv', index=False) # Needs manual save


# Summary of currently available uniforms (after inventory)
# (totals, in (in closet/out(with player)/ miss (missing and unassigned), sh (shorts)
unisumm=updateunisumm(unisumm,unilist)
pdutil.writetoxls(unisumm,  'Summary', 'Master_uniform_logbook.xlsx')

# New uniform log ... get/copy requested size from signup

# After team assignment get desired shirt size distributions from signups (by team)
# Possible difference between requested and assigned sizes?


# Update unilist (and unilog summary) based on master signups
# Maybe interactive comparison here (i.e uniform checked out in mastersignups)
# but inventory shows it as returned

# Uniform tracking -auto output of uniform log .. autosaved to seasonyear_uniform_log.xlsx
# uniform logs for temp storage/convenience; info stored in mastersignups w/ player and payment log (deposits)
SCuni.writeuniformlog(Mastersignups, teams, players, season, year, paylog)

# output csv file with list of outstanding uniforms (along w/ available deposit info)
missing=SCuni.makemissingunilog(Mastersignups, paylog, players, fname='missingunilist_29Dec17.csv')

# Update master signups w/ issued uniform info after uniform night (works!)
# TODO also need to update unilist in uniform log 
# TODO needs conflict resolution and priority of information
Mastersignups=SCuni.getuniinfo(teams, Mastersignups,'Winter_2017_uniform_log.xlsx', year)
# TODO added print statement if numbers conflict but needs testing 

# Check out uniforms from unilist (based on recent master signups)
unilist=checkoutunis(Mastersignups, teams, season, year)

# Check out uniforms from unilist (based on recent master signups)
unilist=checkoutunis(Mastersignups, teams, season, year)

# Update unilist (and unilog summary) based on master signups
# Maybe interactive comparison here (i.e uniform checked out in mastersignups)
# but inventory shows it as returned

# Update master signups w/ issued uniform info after uniform night (works!)
Mastersignups=getuniinfo(teams, Mastersignups,'Winter_2017_uniform_log.xlsx', year)