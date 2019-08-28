# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 11:42:21 2017

@author: tkc
"""
import pandas as pd
import os

os.chdir('C:\\Users\\tkc\\Documents\\Python_Scripts\\SC')

roster=pd.read_csv('Track_2016_rosters.csv', encoding='cp437')
results=pd.read_excel('Cabrini_track_results.xlsx', sheetname='2017')
qualtimes=pd.read_excel('Cabrini_track_results.xlsx', sheetname='Qual')

# Gets team, gender after first name match
fullresult=pd.merge(results, roster, on=['First'], how='left', suffixes=('','_2'))

# Compute estimated qualifying times based on new 2017 age groups
newqual=converttimes(qualtimes)

fullresult=pd.merge(fullresult, newqual, on=['Gender','Distance','Team'], how='left', suffixes=('','_2'))
mycols=['First','Distance','Time','Team','Qualtime']
fullresult=fullresult[mycols]
fullresult['Diff']=fullresult['Time']-fullresult['Qualtime']
fullresult['Difffract']=fullresult['Time']/fullresult['Qualtime']
fullresult=fullresult.sort_values(['Difffract'])
fullresult.to_csv('track_results.csv', index=False)
# return qualifying time for gender, distance and team/group 
gettime(qualtimes, 'M', 2300, 'Team7')

def normaltimes(results)

def converttimes(qualtimes):
    ''' Get qualifying times for new track groups via averaging'''
    teams=['Track7', 'Track89','Track1011', 'Track1213', 'Track1415']
    matchstr=['6|7','8|9','10|11','12|13','14|15']
    genders=['M','F']
    distances=[50,  100,  200,  400,  800, 1600]
    newqual=pd.DataFrame()
    thisqual=pd.Series()
    for i, team in enumerate(teams):
        for j, sex in enumerate(genders):
            for k, dist in enumerate(distances):
                thistime=qualtimes[(qualtimes['Distance']==dist) & (qualtimes['Gender']==sex)]
                thistime=thistime[thistime['Group'].str.contains(matchstr[i])]
                thisqual=thisqual.set_value('Gender', sex)
                thisqual=thisqual.set_value('Distance', dist)
                thisqual=thisqual.set_value('Team', team)
                thisqual=thisqual.set_value('Matches', len(thistime))
                if len(thistime)>0:
                    thisqual=thisqual.set_value('Qualtime',thistime.Qualtime.mean())
                newqual=newqual.append(thisqual, ignore_index=True)
    return newqual
             
def gettime(qualtime, sex, dist, team):
    ''' return qualifying time for gender, distance, age/team '''
    match=qualtime[(qualtime['Gender']==sex) & (qualtime['Distance']==dist) & (qualtime['Team']==team)]
    return match.Qualtime.mean()
    
        
    

