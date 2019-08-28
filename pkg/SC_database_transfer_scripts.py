# -*- coding: utf-8 -*-
"""
Created on Wed May 25 08:44:02 2016

@author: tkc
"""

#%% Transfer database tables to new pandas dataframe structure (probably one time use)
import pandas as pd


#%%
# Transfer parent names/numbers/textable from parents to famcontact
# Using phonelist and check for unique numbers
parents=pd.read_csv('parents.csv', encoding='cp437') # use Excel compatible encoding cp437 instead of utf-8 
players=pd.read_csv('players.csv', encoding='cp437') # use Excel compatible encoding cp437 instead of utf-8 
famcontact=pd.read_csv('family_contact.csv', encoding='cp437')
mmparfam=pd.read_csv('mm_par_fam.csv', encoding='cp437') # many-to-many table for parent to family
mmplafam=pd.read_csv('mm_pla_fam.csv', encoding='cp437') # many-to-many table for player to family
#%%

# add family # to parents
for i in range(0,len(parents)):
    parkey=parents.iloc[i]['Parkey'] # get parent number
    match= mmparfam[(mmparfam['Parkey']==parkey)]
    if len(match)!=1:
        print('Error: Parent # ',parkey,' matches ',len(match),' families.')
        continue
    famkey=match.iloc[0]['Famkey'] 
    parents=parents.set_value(i,'Famkey',famkey)

# add family # to players
for i in range(0,len(parents)):
    plakey=players.iloc[i]['Plakey'] # get parent number
    match= mmplafam[(mmplafam['Plakey']==plakey)]
    if len(match)!=1:
        print('Error: Parent # ',plakey,' matches ',len(match),' families.')
        continue
    famkey=match.iloc[0]['Famkey']
    players=players.set_value(i,'Famkey',famkey)

# add family name to players
for i in range(0,len(players)):
    famkey=players.iloc[i]['Famkey'] # get parent number
    match= famcontact[(famcontact['Famkey']==famkey)]
    if len(match)!=1:
        print('Error: Player # ',i,' matches ',len(match),' families.')
        continue
    if len(match)==1:
        family=match.iloc[0]['Family']
        players=players.set_value(i,'Family',family)

# Add family name to parents
for i in range(0,len(parents)):
    famkey=parents.iloc[i]['Famkey'] # get parent number
    match= famcontact[(famcontact['Famkey']==famkey)]
    if len(match)!=1:
        print('Error: Player # ',i,' matches ',len(match),' families.')
        continue
    if len(match)==1:
        family=match.iloc[0]['Family']
        players=players.set_value(i,'Family',family)

# Check if parents are at different addresses (only one address allowed per player)
for i in range(0,len(parents)):
    famkey=parents.iloc[i]['Famkey'] # get family key
    match= parents[(parents['Famkey']==famkey)]
    if len(match)>1:
        add1=match.iloc[0]['Address']
        add2=match.iloc[1]['Address']
        if add1!=add2 and type(add2)==str:
            print('Different addresses for famkey ',famkey," ", add1," ",add2)

# Check for consistent parish information between parents 
for i in range(0,len(parents)):
    famkey=parents.iloc[i]['Famkey'] # get family key
    match= parents[(parents['Famkey']==famkey)]
    if len(match)>1:
        par1=match.iloc[0]['Zip']
        par2=match.iloc[1]['Zip']
        if type(par1)==str and type(par2)==str: # eliminate nan
            if par1!=par2:
                print("Family # ", famkey,' ', par1, ' ', par2)
        if type(par1)!=str and type(par2)==str: # eliminate nan
            print("Family # ", famkey,' ', par1, ' ', par2)                
        if type(par2)==str and not type(par1)==str: 
            parents=parents.set_value(i,'Parish_Residence',par1)
        if add1!=add2 and type(add2)==str:
            print('Different addresses for famkey ',famkey," ", add1," ",add2)

''' script to transfer address, phone, email, names from parent table to matching famcontact dataframe  
probably only for one time use '''
for i in range(0,len(famcontact)):
    famkey=famcontact.iloc[i]['Famkey'] # get family key
    match= parents[(parents['Famkey']==famkey)]    
    phonelist=[]
    textlist=[]
    emaillist=[]
    '''
    famcontact=famcontact.set_value(i,'Zip',match.iloc[0]['Zip'])
    famcontact=famcontact.set_value(i,'Address',match.iloc[0]['Address'])
    famcontact=famcontact.set_value(i,'Parish_residence',match.iloc[0]['Parish_residence'])
    famcontact=famcontact.set_value(i,'Parish_registration',match.iloc[0]['Parish_registration'])
    famcontact=famcontact.set_value(i,'City',match.iloc[0]['City'])
    famcontact=famcontact.set_value(i,'State',match.iloc[0]['State'])
    '''
    if type(match.iloc[0]['Phone1'])== str: # numbers from parent 1
        phonelist.append(match.iloc[0]['Phone1'].strip())
        textlist.append(match.iloc[0]['Text1'])
    if type(match.iloc[0]['Phone2'])== str:
        if match.iloc[0]['Phone2'].strip() not in phonelist:
            phonelist.append(match.iloc[0]['Phone2'].strip())
            textlist.append(match.iloc[0]['Text2'])
    if type(match.iloc[0]['Phone3'])== str:
        if match.iloc[0]['Phone3'].strip() not in phonelist:
            phonelist.append(match.iloc[0]['Phone3'].strip())
            textlist.append(match.iloc[0]['Text3'])
    if type(match.iloc[0]['Email1'])== str: # emails from parent 1
        emaillist.append(match.iloc[0]['Email1'].strip())
    if type(match.iloc[0]['Email2'])== str: # emails from parent 1
        if match.iloc[0]['Email2'].strip() not in emaillist:
            emaillist.append(match.iloc[0]['Email2'].strip())        
    famcontact=famcontact.set_value(i,'Pfirst',match.iloc[0]['Pfirst'])
    famcontact=famcontact.set_value(i,'Plast',match.iloc[0]['Plast'])
    if(len(match)>1):# numbers from parent 1
        if type(match.iloc[1]['Phone1'])== str:
            if match.iloc[1]['Phone1'].strip() not in phonelist:
                phonelist.append(match.iloc[1]['Phone1'].strip())
                textlist.append(match.iloc[1]['Text1'])
        if type(match.iloc[1]['Phone2'])== str:
            if match.iloc[1]['Phone2'].strip() not in phonelist:
                phonelist.append(match.iloc[1]['Phone2'].strip())
                textlist.append(match.iloc[1]['Text2'])
        if type(match.iloc[1]['Phone3'])== str:
            if match.iloc[1]['Phone3'].strip() not in phonelist:
                phonelist.append(match.iloc[1]['Phone3'].strip())
                textlist.append(match.iloc[1]['Text3'])
        if type(match.iloc[1]['Email1'])== str: # email 1 from parent 2
            if match.iloc[1]['Email1'].strip() not in emaillist:
                emaillist.append(match.iloc[1]['Email1'].strip())        
        if type(match.iloc[1]['Email2'])== str: # email 2 from parent 2
            if match.iloc[1]['Email2'].strip() not in emaillist:
                emaillist.append(match.iloc[1]['Email2'].strip())        
        famcontact=famcontact.set_value(i,'Pfirst2',match.iloc[1]['Pfirst']) # add 2nd parent name to famcontact
        famcontact=famcontact.set_value(i,'Plast2',match.iloc[1]['Plast'])
    if(len(match)>2):# numbers from parent 3
        if type(match.iloc[2]['Phone1'])== str:
            if match.iloc[2]['Phone1'].strip() not in phonelist:
                phonelist.append(match.iloc[2]['Phone1'].strip())
                textlist.append(match.iloc[2]['Text1'])
        if type(match.iloc[2]['Phone2'])== str:
            if match.iloc[2]['Phone2'].strip() not in phonelist:
                phonelist.append(match.iloc[2]['Phone2'].strip())
                textlist.append(match.iloc[2]['Text2'])
        if type(match.iloc[2]['Phone3'])== str:
            if match.iloc[2]['Phone3'].strip() not in phonelist:
                phonelist.append(match.iloc[2]['Phone3'].strip())
                textlist.append(match.iloc[2]['Text3'])
        famcontact=famcontact.set_value(i,'Pfirst3',match.iloc[2]['Pfirst']) # add 2nd parent name to famcontact
        famcontact=famcontact.set_value(i,'Plast3',match.iloc[2]['Plast'])
    
    for num in range(0,len(phonelist)): # write phonelist and textlist to famcontact
        phonecol='Phone'+str(num+1)
        textcol='Text'+str(num+1)
        famcontact=famcontact.set_value(i,phonecol,phonelist[num])
        famcontact=famcontact.set_value(i,textcol,textlist[num])
    
    for num in range(0,len(emaillist)): # write phonelist and textlist to famcontact
        emailcol='Email'+str(num+1)
        famcontact=famcontact.set_value(i,emailcol,emaillist[num])

def addfamilies(df, famcontact, fambills):
    ''' Old version of addfamilies when fambills was also used... new version generates bill summaries in real-time from paylog and signups
	df contains new families to add to master family contact and family billing tables '''
    df=df.reset_index(drop=True) # first reset index for proper for loops
    dfcon=df # make copy of original for famcontact below
    # backup existing family contact and billing tables    
    mytime=datetime.datetime.now()
    datestr='_' + str(mytime.day) + mytime.strftime("%B") + str(mytime.year)[2:] # current date as in 3Jun16
    filestr='family_contact'+datestr+'.bak'
    famcontact.to_csv(filestr, index=False) # backup existing players master list
    filestr='family_bill'+datestr+'.bak'
    fambills.to_csv(filestr, index=False) # backup existing players master list
    
    # update family billing
    datestr=str(mytime.month)+'/'+str(mytime.day)+'/'+str(mytime.year)
    df=dropcolumns(df,fambills) # drops all cols from df that are not in fambills
    # df=df.iloc[:,0:3]
    # df.drop('Plakey', axis=1, inplace=True)
    df['Startdate']=datestr # add and initialize other necessary columns
    df['Lastupdate']=datestr
    df['Startbal']=0
    df['Currbalance']=0
    df['Billing_note']=''
    colorder=fambills.columns.tolist()
    fambills=pd.concat([fambills,df]) # concat the two frames (if same names, column order doesn't matter)
    fambills=fambills[colorder] # put back in original order
    fambills=fambills.reset_index(drop=True)
    fambills=fambills.to_csv('family_bill.csv',index =False)
    
    # update family contact
    dfcon.rename(columns={'Plakey': 'Players', 'Parish': 'Parish_registration', 'Phone': 'Phone1', 'Text': 'Text1', 'Email': 'Email1',}, inplace=True)
    dfcon=dropcolumns(dfcon, famcontact) # drop unnecessary columns from dfcon (not in famcontact)
    #dfcon.drop('Timestamp', axis=1, inplace=True)
    #dfcon.drop('First', axis=1, inplace=True)
    #dfcon.drop('Last', axis=1, inplace=True)
    #dfcon.drop('DOB', axis=1, inplace=True)
    #dfcon.drop('Gender', axis=1, inplace=True)
    #dfcon.drop('School', axis=1, inplace=True)
    #dfcon.drop('Grade', axis=1, inplace=True)
    #dfcon.drop('AltPlacement', axis=1, inplace=True)
    #dfcon.drop('Ocstatus', axis=1, inplace=True)
    #dfcon.drop('Othercontact', axis=1, inplace=True)
    #dfcon.drop('Coach', axis=1, inplace=True)
    #dfcon.drop('Coach2', axis=1, inplace=True)
    #dfcon.drop('Sport', axis=1, inplace=True)
    dfcon['City']='St. Louis'
    dfcon['State']='MO'
    dfcon['Parish_residence']=''
    dfcon['Pfirst3']=''
    dfcon['Plast3']=''
    dfcon['Phone3']=''
    dfcon['Text3']=''
    dfcon['Phone4']=''
    dfcon['Text4']=''
    dfcon['Email3']=''
    
    colorder=fambills.columns.tolist()
    famcontact=pd.concat([famcontact,dfcon]) # concat the two frames (if same names, column order doesn't matter)
    famcontact=famcontact[colorder] # put back in original order
    famcontact=famcontact.reset_index(drop=True)
    famcontact=famcontact.to_csv('family_contact.csv',index =False)
    return famcontact, fambills 

def comparefamkeys(players,famcontact, fambills):
    '''Old version of utility script to compare family contacts, family bills and players list
	fambills has now been removed 	'''
    fams_pla=players.Famkey.unique()
    fams_pla=np.ndarray.tolist(fams_pla)
    fams_con=famcontact.Famkey.unique()
    fams_con=np.ndarray.tolist(fams_con)
    fams_bill=fambills.Famkey.unique()
    fams_bill=np.ndarray.tolist(fams_bill)
    # compare contacts and billing ... should be identical
    billonly=[i for i in fams_bill if i not in fams_con]
    cononly=[i for i in fams_con if i not in fams_bill]
    noplayers=[i for i in fams_con if i not in fams_pla]
    for i,val in enumerate(billonly):
        print("Famkey ", val, " in family billing but not in family contacts.")
    for i,val in enumerate(cononly):
        print("Famkey ", val, " in family contacts but not in family billing.")
    for i,val in enumerate(noplayers):
        print("Famkey ", val, " in family contacts but not found among players.")
    # look for different names between family contacts and family bills
    for i in range(0,len(famcontact)):
        famkey=famcontact.iloc[i]['Famkey'] # grab this key
        family=famcontact.iloc[i]['Family']
        family=family.title()   # switch to title case
        family=family.strip() # remove whitespace
        match=fambills[fambills['Famkey']==famkey]
        if len(match)==1: # should be a match already assuming above section finds no discrepancies
            family2=match.iloc[0]['Family']
            family2=family2.title()   # switch to title case
            family2=family2.strip() # remove whitespace
            if family!=family2: # different family names with same key
                print("Family key ", str(famkey), ": ", family, " or ", family2)
    # Now check for family name discrepancies between players and famcontact
    for i in range(0,len(famcontact)):
        famkey=famcontact.iloc[i]['Famkey'] # grab this key
        family=famcontact.iloc[i]['Family']
        family=family.title()   # switch to title case
        family=family.strip() # remove whitespace
        match=players[players['Famkey']==famkey]
        if len(match)==1: # should be a match already assuming above section finds no discrepancies
            family2=match.iloc[0]['Family']
            family2=family2.title()   # switch to title case
            family2=family2.strip() # remove whitespace
            if family!=family2: # different family names with same key
                print("Family key ", str(famkey), ": ", family, " or ", family2)
    return

def writecontactsold(df, Teams, season, signupfile):
    ''' Default data frame with shortened names into which google drive sheets are read; sheets are created with google
    form and contain fresh player data from forms; For paper signups some data will be missing and will be found 
    from existing player database 
	New version starts with mastersignups with team already assigned'''
    # Slice by sport (also find season) Basketball (null for winter?), Soccer, Volleyball, Baseball, T-ball, Softball, Track) 
    from openpyxl import load_workbook #
    book=load_workbook(signupfile)
    writer=pd.ExcelWriter(signupfile, engine='openpyxl')
    writer.book=book
    writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
    
    if season=='Fall':    
        thismask = df['Sport'].str.contains('soccer', case=False, na=False) & df['Gender'].str.contains('f', case=False, na=False)
        Girlsoccer=df.loc[thismask]
        Girlsoccer['Sport']='Soccer' # set to standard value
        Girlsoccer=assignteams(Girlsoccer, Teams) # add team assignment
        Girlsoccer=organizecontacts(Girlsoccer) # organize in correct format for xls file        
        Girlsoccer.to_excel(writer,sheet_name='Girlsoccer',index=False) # this overwrites existing file
        thismask = df['Sport'].str.contains('soccer', case=False, na=False) & df['Gender'].str.contains('m', case=False, na=False)
        Boysoccer=df.loc[thismask]
        Boysoccer['Sport']='Soccer'
        Boysoccer=assignteams(Boysoccer, Teams) # add team assignment
        Boysoccer=organizecontacts(Boysoccer) # organize in correct format for xls file         
        Boysoccer.to_excel(writer,sheet_name='Boysoccer',index=False) # this overwrites existing file
        thismask = df['Sport'].str.contains('v', case=False, na=False) & df['Gender'].str.contains('m', case=False, na=False)
        BoyVB=df.loc[thismask]
        BoyVB['Sport']='VB'
        BoyVB=assignteams(BoyVB, Teams) # add team assignment                
        BoyVB=organizecontacts(BoyVB) # organize in correct format for xls file         
        BoyVB.to_excel(writer,sheet_name='BoyVB',index=False) # this overwrites existing file
        thismask = df['Sport'].str.contains('v', case=False, na=False) & df['Gender'].str.contains('f', case=False, na=False)
        GirlVB=df.loc[thismask]
        GirlVB['Sport']='VB'
        GirlVB=assignteams(GirlVB, Teams) # add team assignment                
        GirlVB=organizecontacts(GirlVB) # organize in correct format for xls file 
        GirlVB.to_excel(writer,sheet_name='GirlVB',index=False) # this overwrites existing file
         
    if season=='Spring': 
        thismask = df['Sport'].str.contains('baseball', case=False, na=False)
        Baseball=df.loc[thismask]
        Baseball['Sport']='Baseball' # set to std value
        Baseball=assignteams(Baseball, Teams) # add team assignment                                
        Baseball=organizecontacts(Baseball) # organize in correct format for xls file         
        Baseball.to_excel(writer,sheet_name='Baseball',index=False) # this overwrites existing file
 
        thismask = df['Sport'].str.contains('softball', case=False, na=False)
        Softball=df.loc[thismask]
        Softball['Sport']='Softball' # set to std value
        Softball=assignteams(Softball, Teams) # add team assignment                        
        Softball=organizecontacts(Softball) # organize in correct format for xls file 
        Softball.to_excel(writer,sheet_name='Softball',index=False) # this overwrites existing file
 
        thismask = df['Sport'].str.contains('t-ball', case=False, na=False)
        Tball=df.loc[thismask]
        Tball['Sport']='Tball' # set to std value
        Tball=assignteams(Tball, Teams) # add team assignment                        
        Tball=organizecontacts(Tball) # organize in correct format for xls file 
        Tball.to_excel(writer,sheet_name='Tball',index=False) # this overwrites existing file

        thismask = df['Sport'].str.contains('track', case=False, na=False)
        Track=df.loc[thismask]
        Track['Sport']='Track' # set to std value
        Track=assignteams(Track, Teams) # add team assignment                        
        Track=organizecontacts(Track) # organize in correct format for xls file 
        Track.to_excel(writer,sheet_name='Track',index=False) # this overwrites existing file
    
    if season=='Winter': # currently only basketball (no mask by sport)
        df['Sport']='Basketball' # set to std name
        Basketball=assignteams(df, Teams, sport='Basketball') # add team assignment        
        thismask = Basketball['Gender'].str.contains('f', case=False, na=False)
        Girlbasketball=Basketball.loc[thismask]   
        Girlbasketball=organizecontacts(Girlbasketball) # organize in correct format for xls file         
        Girlbasketball.to_excel(writer,sheet_name='GirlBasketball',index=False) # this overwrites existing file
        thismask = Basketball['Gender'].str.contains('m', case=False, na=False)
        Boybasketball=Basketball.loc[thismask]   
        Boybasketball=organizecontacts(Boybasketball) 
        Boybasketball.to_excel(writer,sheet_name='BoyBasketball',index=False) # this overwrites existing file
 
    writer.save() # saves xls file with all modified data   
    return 

def organizecontacts(df):
    ''' Corresponding old version of organizecontacts takes a sport-gender and organizes in manner for output to excel signup summary file ''' 
    mycols=['First', 'Last', 'Grade', 'Gender', 'School', 'Phone', 'Text','Email', 'Phone2', 'Text2', 'Email2', 'Team', 'Plakey', 'Famkey', 'Family'] 
    thisdf=pd.DataFrame(columns=mycols) # temp df for dropping unnecessary columns
    df['Team']=''    
    df=dropcolumns(df,thisdf) # drop columns not working
    df.Grade=df.Grade.replace('K',0)
    df=df.sort_values(['Grade'], ascending=True)
    df.Grade=df.Grade.replace(0,'K') # replace K with zero to allow sorting
    df=df[mycols] # put back in desired order
    return df
	
#%% Saving of various files
famcontact.to_csv('family_contact.csv', index=False)  
parents.to_csv('parents.csv', index=False)  
players.to_csv('players.csv', index=False)
