# -*- coding: utf-8 -*-
"""
Created on Thu Aug 18 11:06:34 2016

@author: tkc
"""

from lxml import html
import requests
import urllib.request

#%%
# xml.etree.ElementTree -- flexible container 
page = requests.get('http://www.judgedowdsoccer.com/content/schedules/Grade_kg.htm')
etree = html.fromstring(page.content) # pulls entire page as html element

# find stop and start of tables ... return list of tables (some nested)

mytables=etree.xpath('//table') # gets 5 tables

for table in mytables:
    text=table.xpath('//tr/text()')
    

tab3=mytables[2]

teamrows=tab3.xpath('//tr') # now extract 23 team entries

thisteam=teamrows[0]

for team in thisteam:
    text=team.xpath('//td/text()')
    print(text)    
    
for team in teamrows:

    for child in text:
        print(child.attrib)
    
rowlist=[]
for row in teamrows:
    # rowlist=row.xpath('//td//text()')
    # print(etree.tostring(row, pretty_print=True))
    str=''.join(row) # list to string conversion
    print(str)
    
thisteam=teamrows[3] 

for child in teamrows:
    print(child.tag, child.attrib)



namelist=[]
for name in names:
    namelist.append([c.text for c in tabl.getchildren()])
    
namelist=[]
for name in names:
    namelist.append([c.tag for c in tabl.getchildren()])

for tabl in mytables:
    rowlist.append([c.tag for c in tabl.getchildren()])
    

rows = mytables.xpath(xpath1)[0].findall("tr")

data=list()

tables=tree.xpath('//table//tr')

print(htmlobjects)

rows=tree.xpath('tbody/tr')
# could find #. to identify all the teams
# table_03 has teams/coachs/numbers and tables_04 and _05 have schedules (parse with id=Table_03)

Teams=[] # list of number, team names
Dates=[]

for tbl in tree.xpath('//table'):  # finds tables
