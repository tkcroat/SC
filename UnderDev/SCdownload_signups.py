# -*- coding: utf-8 -*-
"""
Created on Sun May 22 10:12:03 2016

@author: tkc
"""

import gspread
import pandas as pd
#%% Authorization
oauthfile = '/path/to/file/your-api-key.json',                 
scope = ['https://spreadsheets.google.com/feeds']
json_key = json.load(open(oauthfile))
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
 
gspreadclient = gspread.authorize(credentials) # Authorize





#%%
gc = gspread.login('tkc@gmail.com', 'tI60cR30')
book = gc.open('Spreadsheet name')
sheet = book.sheet1 #choose the first sheet
dataframe = pandas.DataFrame(sheet.get_all_records())
