# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 10:24:49 2016
SC legacy funct
@author: tkc
"""
import pandas as pd

# Testing option now built in to sendebills
def testautobilling(billlist, Mastersignups, season, year, emailtitle, messagefile, **kwargs):
    ''' Test e-billing and SMSbilling by writing each to log file using payment and uniform info strings made by 
    createbilllist and saved in columns Feepaydetail and Unidetail (for e-mail) and Textmessage (for SMS)
    run and check these logs (autonamed by date) before live send of e-mail bills or SMS bills
    kwargs: SMS -- contains header for text messages if SMS via e-mail is chosen
       sendemaillogic kwargs (incl. newuni, olduni, fees)
        newuni, olduni-- bool flag to decide to send email to those with new or old uniform issues 
             however message with old, new or both is constructed by createbilllist
        fees- bool to include fee payment (defaults True)
    '''
    # autonaming of testing text log files as emaillog_date and SMSlog_date
    now=datetime.datetime.now()
    emailfile='email_test_log'+datetime.date.strftime(now, "%d%b%y")+'.txt'
    SMSfile='SMS_test_log'+datetime.date.strftime(now, "%d%b%y")+'.txt'
    paperfile='paper_bills'+datetime.date.strftime(now, "%d%b%y")+'.txt'
    thismask=billlist['Email1'].isnull()
    paperlist=billlist.loc[thismask] # just write to paper log file if no e-mail and bad SMS gateway
    ebilllist=billlist.loc[~thismask] # includes e-mail addresses and SMS gateways
    ebilllist, skiplist=sendemaillogic(ebilllist, **kwargs) # decides who gets e-mail depending on fees/uniforms/ etc.
    with open(emailfile,'w+') as emaillog, open(SMSfile,'w+') as SMSlog:
        for index, row in ebilllist.iterrows():
            # Skip send if zero balance and no info in unidetail(no outstanding unis, none to be issued)
            if ebilllist.loc[index]['Balance']>0 and str(ebilllist.loc[index]['Unidetail'])=='nan':
                thisfam=ebilllist.loc[index]['Family']
                message='Skip send for family '+ thisfam+'. No outstanding balance or uniform issues.\n'
                emaillog.write(message)
                continue            
            # determine if SMSgateway or e-mail address 
            thisaddress=ebilllist.loc[index]['Email1'].split('@')[0]
            # if 9 or 10 digit number it's an SMS gateway (send short text message)
            thismatch=re.match(r'\d{9}', thisaddress) # if 9 or 10 digit # it's SMS gateway
            if thismatch:
                if 'SMS' in kwargs: # switch to include or exclude SMS sending (otherwise skipped)
                    textheader=kwargs.get('SMS','Message from Cabrini')
                    message=ebilllist.loc[index]['Family']+ ' '+str(ebilllist.loc[index]['Famkey'])+'\n'
                    SMSlog.write(message) # output family name and key
                    customSMS=ebilllist.loc[index]['Textmessage'] # pulls family specific SMS from bill list
                    mySMS=textheader+customSMS+'; to '+thismatch.group(0) +'via SMS gateway\n'  # combined with passed header
                    SMSlog.write(mySMS)                
                    # also throw longer detail e-mail formatted message into text log file   
                    thisbillrow=ebilllist.loc[index]
                    recipients=getemailadds(thisbillrow) # list of recipients
                    message=makemessage(thisbillrow, Mastersignups, season, year, recipients, emailtitle, messagefile)
                    SMSlog.write(message)
            else: # normal e-mail address(es)
                message=ebilllist.loc[index]['Family']+ ' '+str(ebilllist.loc[index]['Famkey'])+'\n'
                emaillog.write(message) # family name for log file only 
                thisbillrow=ebilllist.loc[index] # this family's bill info as series 
                recipients=getemailadds(thisbillrow) # list of recipients
                # create custom email message
                message=makemessage(thisbillrow, Mastersignups, season, year, recipients, emailtitle, messagefile)
                emaillog.write(message)
    with open(paperfile,'w+') as paperlog: # now process paper only ones
        for index, row in paperlist.iterrows():
            # Skip send if zero balance and no info in unidetail(no outstanding unis, none to be issued)
            message=paperlist.loc[index]['Family']+ ' '+str(paperlist.loc[index]['Famkey'])
            paperlog.write(message) # family name for log file only 
            if paperlist.loc[index]['Balance']>0 and str(paperlist.loc[index]['Unidetail'])=='nan':
                thisfam=paperlist.loc[index]['Family']
                message='Skip send for family '+ thisfam+'. No outstanding balance or uniform issues.\n'
                paperlog.write(message)
                continue
            else:
                thisbillrow=paperlist.loc[index] # this family's bill info as series 
                recipients='None' # list of recipients
                # create custom email message
                message=makemessage(thisbillrow, Mastersignups, season, year, recipients, emailtitle, messagefile)
                paperlog.write(message)
    return skiplist


def changeaddresses(newadd, famcontact):
    '''Pass newadd after visual check, the merge/alter that subset and set parish of residence to nan  '''
    autocsvbackup(famcontact,'family_contact', newback=True) # Run file backup script
    for index,row in newadd.iterrows():
        famcontact=famcontact.set_value(index,'Address',newadd.loc[index]['Address_n']) # change address
        famcontact=famcontact.set_value(index,'Zip',newadd.loc[index]['Zip_n']) # change Zip
        famcontact=famcontact.set_value(index,'Parish_residence','nan') # delete parish of res and manually re-enter
    famcontact.to_csv('family_contact.csv', index=False)
    return famcontact
       
def checkaddresses(df, famcontact):
    '''Pass SCsignups, compare address #s and zip to detect true address changes from entire frame  '''
    df.Timestamp=pd.to_datetime(df.Timestamp, errors='coerce') # converts to naT or timestamp 
    gdsignups=df.dropna(subset=['Timestamp']) # drops manual entries (no google drive timestamp)
    faminfo=gdsignups.drop_duplicates(subset=['Famkey']) # only process first kid from family 
    tempfam=pd.merge(famcontact, faminfo, how='left', on=['Famkey'], suffixes=('','_n')) # same indices as famcontact
    tempfam=tempfam.dropna(subset=['Zip_n']) # drops values with no gd info
    changelist=[] 
    for index, row in tempfam.iterrows():
        match=re.search(r'\d+',tempfam.loc[index]['Address'])
        num1=match.group(0)
        match=re.search(r'\d+',tempfam.loc[index]['Address_n'])
        num2=match.group(0)
        if num1!=num2: # change in address number strongly suggestive of actual change
            changelist.append(tempfam.loc[index]['Famkey'])
        else:
            continue
    newadd=tempfam[tempfam.Famkey.isin(changelist)] # subset with different address number
    mycols=['Famkey', 'Family', 'Address', 'Zip', 'Address_n', 'Zip_n'] # drop extraneous cols and reorder
    dropcollist=[s for s in newadd.dtypes.index if s not in mycols]
    newadd=newadd.drop(dropcollist, axis=1) # drops extraneous columns
    newadd=newadd[mycols]
    return newadd # create list of indices with suspected changes

# old version before interactive tk approval
def update_contact(ser):
    '''Update phone and textable list from google drive entries; existing entries from fam_contact listed first;
    pass/modify/return series for family; reorder/replace numbers '''
    # [phone, text, order]
    thisfam=ser.Family
    phonelist=[] # list of lists with number and textable Y/N
    for i in range(1,5): # get 4 existing phone entries (phone1, phone2, etc.)
        phname='Phone'+str(i)
        txtname='Text'+str(i)
        if str(ser[phname])!='nan':
            phonelist.append([ser[phname],ser[txtname]]) # as phone and text y/N
    # New google drive entries will be Phone1_n.. look for phone/text pair in existing list
    if str(ser['Phone1_n'])!='nan' and [ser['Phone1_n'],ser['Text1_n']] not in phonelist: # new ones phone is required entry
        if [ser['Phone1_n'],np.nan] in phonelist: # remove if # present but w/o text indication
            phonelist.remove([ser['Phone1_n'],np.nan])
        phonelist.insert(0,[ser['Phone1_n'],ser['Text1_n']]) # insert in first position
        print ('Added phone ', str(ser['Phone1_n']), 'for family', thisfam)
        # TODO look for same phone but nan for text and remove it
    else: # move this pair to first position in existing list (already in list)
        phonelist.insert(0,phonelist.pop(phonelist.index([ser['Phone1_n'],ser['Text1_n']])))
        # Inserts desired primary in first position while simultaneously removing other entry
    if str(ser.Phone2_n)!='nan': # check for phone2 entry (with _n suffix)
        if [ser['Phone2_n'],ser['Text2_n']] not in phonelist: # add second phone to 2nd position if not present
           if [ser['Phone2_n'],np.nan] in phonelist: # remove if # present but w/o text indication
              phonelist.remove([ser['Phone2_n'],np.nan]) 
           phonelist.insert(1,[ser['Phone2_n'],ser['Text2_n']])
           print ('Added phone ', str(ser['Phone2_n']), 'for family', thisfam)
    # Truncate list to max 4 entries (older ones lost)
    phonelist=phonelist[0:3]
    while len(phonelist)<4:
        phonelist.append([np.nan,np.nan]) # pad with nan entries if necessary    
    # now reset phone number/text combos in series
    for i in range(1,5): # reset 4 existing phone entries
        phname='Phone'+str(i)
        txtname='Text'+str(i)
        ser=ser.set_value(phname,phonelist[i-1][0])
        ser=ser.set_value(txtname,phonelist[i-1][1])
    # Construct existing list of known email addresses
    emaillist=[] 
    for i in range(1,4): # get 3 existing email entries
        emailname='Email'+str(i)
        if str(ser[emailname])!='nan':
            emaillist.append(ser[emailname].lower())
    # Find new email1 entry in google drive data
    if str(ser.Email)!='nan' and '@' in ser.Email: # real primary gd named email
        if ser.Email.lower() not in emaillist: # add in first position if not present
            emaillist.insert(0,ser.Email.lower())
            print ('Added email ', str(ser.Email.lower()), 'for family', thisfam)
        else: # if already present move to first position
            emaillist.insert(0,emaillist.pop(emaillist.index(ser['Email'])))
    # look for new email in email2 position and add 
    if str(ser.Email2_n)!='nan' and '@' in ser.Email2_n:
        if ser.Email2_n.lower() not in emaillist: # add second phone to 2nd position if not present
            emaillist.insert(1,ser.Email2_n.lower())
            print('Added email', ser.Email2_n.lower(),'for family', thisfam)
    # Construct and record updated email list 
    emaillist=emaillist[0:3] # limit to 3 entries
    while len(emaillist)<3:
        emaillist.append(np.nan) # pad with nan entries if necessary 
    for i in range(1,4): # reset 3 email entries
        emailname='Email'+str(i)
        ser=ser.set_value(emailname,emaillist[i-1])
    # Update list of parent names (max 3 entries)
    parlist=[] # construct existing list from family contacts
    for i in range(1,4):
        fname='Pfirst'+str(i)
        lname='Plast'+str(i)
        if str(ser[fname])!='nan':
            parlist.append([ser[fname],ser[lname]]) # list of lists [first, last]
    if [ser['Pfirst1_n'],ser['Plast1_n']] not in parlist: # phone 1 is required entry
        parlist.insert(0,[ser['Pfirst1_n'],ser['Plast1_n']]) # insert in first position
        print ('added parent', ser['Pfirst1_n'], ser['Plast1_n'], 'for family', thisfam)        
    else: # move this pair to first position in existing list
        parlist.insert(0,parlist.pop(parlist.index([ser['Pfirst1_n'],ser['Plast1_n']])))
        # inserts in first position while simultaneously removing other entry
    if str(ser.Pfirst2_n!='nan'): # check for parent 2 entry
        if [ser['Pfirst2_n'],ser['Plast2_n']] not in parlist: # add second phone to 2nd position if not present
            parlist.insert(1,[ser['Pfirst2_n'],ser['Plast2_n']])
    parlist=parlist[0:3] # limit to 3 entries
    while len(parlist)<3:
        parlist.append([np.nan,np.nan]) # pad with nan entries if necessary 
    # now reset parent name entries
    for i in range(1,4): # reset 3 existing parents entries
        fname='Pfirst'+str(i)
        lname='Plast'+str(i)
        ser=ser.set_value(fname,parlist[i-1][0])
        ser=ser.set_value(lname,parlist[i-1][1])
    # update parish of registration (if new gd entry and no existing entry)
    # otherwise changes are skipped to keep parish names consistent
    if str(ser.Parish_registration)=='nan' and str(ser.Parish)!='nan':
        ser['Parish_registration']=ser['Parish'] # Set parish of registration
    return ser

# used before tk confirmation when siblings were added simultaneously (now done sequentially w/ famcontact update)
def processsiblings(newfams, newplayers):
    ''' Finds multiple kids from same family (siblings/step-siblings) via phone match and assigns single 
    famkey, generates common family name (before entering this info into family contacts)
    probably no longer called since using tkinter select method
    '''
    # Phone contact match is probably most robust 
    phonenums=np.ndarray.tolist(newfams.Phone.unique())
    phonenums.extend(np.ndarray.tolist(newfams.Phone2.unique()))
    phonenums=[str(s) for s in phonenums if str(s) != 'nan']
    processed=[] # keep track of plakeys that are already combined
    for i, num in enumerate(phonenums):
        # Matches gets player list from same family (phone match)
        matches=newfams[(newfams['Phone']==num) | (newfams['Phone2']==num)] 
        matches=matches[~matches['Plakey'].isin(processed)] # drop if already processed 
        if len(matches)>0: # skips if already processed on different common family number
            # generate new family name
            lasts=np.ndarray.tolist(matches.Last.unique())
            lasts.extend(np.ndarray.tolist(matches.Plast1.unique())) # also include primary parent
            lasts=[s.strip() for s in lasts if str(s) !='nan'] # drop nan
            family=' '.join(lasts) # Just concat with space for entire family name
            # Assign first famkey and to all players
            famkey=matches.iloc[0]['Famkey'] # grab first one
            plakeys=np.ndarray.tolist(matches.Plakey.unique())
            plakeys=[int(i) for i in plakeys]
            # now just reassign famkey and family for subset of plakeys in both newfams and newplayers
            match=newfams[newfams['Plakey'].isin(plakeys)]
            for index, row in match.iterrows():
                newfams=newfams.set_value(index,'Famkey',famkey)
                newfams=newfams.set_value(index,'Family',family)
            # same for newplayers
            match=newplayers[newplayers['Plakey'].isin(plakeys)]
            for index, row in match.iterrows():
                newplayers=newplayers.set_value(index,'Famkey',famkey)
                newplayers=newplayers.set_value(index,'Family',family)
            processed.extend(plakeys) # Add keys to processed list
    newfams=newfams.drop_duplicates(subset='Famkey') # only need one entry for fam, not duplicate
    # TODO This might drop a step-dad phone # for kids w/ same mom, different dad
    return newfams, newplayers
    
# old way of finding associated families ... now using phonedict and last name tuple list
def findfamily(newplayers,famcontact):
    ''' For confirmed new players, find existing family name and key (if it exists)''' 
    newplayers=newplayers.reset_index(drop=True) # reset index to avoid problems
    if 'Famkey' not in newplayers: # add player key column to sign-ups file if not present
        newplayers.insert(1,'Famkey',0)
    if 'Family' not in newplayers: # add player key column to sign-ups file if not present
        newplayers.insert(0,'Family','')
    for index, row in newplayers.iterrows():
        first=newplayers.loc[index]['First']         
        last=newplayers.loc[index]['Last']
        phstr='' # build phone matching string
        if pd.notnull(newplayers.loc[index]['Phone']):
            phstr+='|' + newplayers.loc[index]['Phone']
        if pd.notnull(newplayers.loc[index]['Phone2']):
            phstr+='|' + newplayers.loc[index]['Phone2']
        mask = famcontact['Phone1'].str.contains(phstr, na=False, case=False) | famcontact['Phone2'].str.contains(phstr, na=False) | famcontact['Phone3'].str.contains(phstr, na=False)
        match=famcontact.loc[mask] # filter df with above phone matching mask
        if len(match)==1:
            print('Phone match of player ', first, last,' to family ', match.iloc[0]['Family'])
            newplayers=newplayers.set_value(index,'Family',match.iloc[0]['Family']) # 
            newplayers=newplayers.set_value(index,'Famkey',match.iloc[0]['Famkey'])
            continue # famkey assigned and move to next if phone match
        mask = famcontact['Family'].str.contains(last, na=False, case=False) # check for last name match
        match=famcontact.loc[mask] # filter df with above phone matching mask
        if len(match)>0: # check for possible family matches (even though no phone match)
            for i in range(0,len(match)):
                tempstr=''
                tempstr=tempstr+str(match.iloc[i]['Famkey'])+' ' 
                tempstr=tempstr+str(match.iloc[i]['Family'])+' ' # string with family key # and name for all possibles
            print('Possible match of player ', first, last,' to family ', tempstr,'not yet assigned') # lists all
            # don't assign number but can be done manually if reasonable
        else:
            print('No match for player ', first, last)
    return newplayers # send back same df with family name and key

def organizesignups(df, year):
    ''' takes SCsignup file subset (split by sport) and organizes for output into master signup file ''' 
    mycols=['SUkey','First', 'Last', 'Grade', 'Gender', 'Sport', 'Year', 'Team', 'Plakey','Famkey', 'Family', 'SUdate', 'Issue date', 'Uniform #','Uni return date'] 
    df.Grade=df.Grade.replace('K',0)
    df=df.sort_values(['Gender','Grade'], ascending=True) # nested sort gender then grade
    df.Grade=df.Grade.replace(0,'K') # replace K with zero to allow sorting
    # add missing columns to df
    df['Team']=''
    df['Issue date']=''
    df['Uniform #']=''
    df['Uni return date']=''
    df['Year']= int(year)
    df['SUkey']=0 # column for unique signup key (zero means not yet assigned)
    df=df[mycols] # put back in desired order
    return df

def organizesignups2(df):
    ''' Adding teams to master signups (all cols already present ''' 
    mycols=['SUkey','First', 'Last', 'Grade', 'Gender', 'Sport', 'Year', 'Team', 'Plakey','Famkey', 'Family', 'SUdate', 'Issue date', 'Uniform #','Uni return date'] 
    dropcollist=[s for s in df.dtypes.index if s not in mycols] # 
    df=df.drop(dropcollist, axis=1) # unnecessary columns dropped 
    df.Grade=df.Grade.replace('K',0)
    df=df.sort_values(['Year','Sport', 'Gender', 'Grade'], ascending=True)
    df.Grade=df.Grade.replace('0','K', regex=True) # make sure any 0 grades are again replaced with K
    df=df[mycols] # put back in desired order
    return df
# older way of organizing output from dataframes after merges and such 
def organizelog(df):
    ''' takes a sport-gender and organizes in manner for output to excel signup summary file ''' 
    mycols=['First', 'Last', 'School', 'Issue date', 'Uniform #', 'Amount', 'Deposit type', 'Deposit date', 'Uni return date', '$ returned', 'Comments', 'Plakey', 'Famkey'] 
    thisdf=pd.DataFrame(columns=mycols) # temp df for dropping unnecessary columns
    df=dropcolumns(df,thisdf) # drop columns not working
    df=df[mycols] # put back in desired order
    return df

# old version before more comprehensive, sophisticated find-replace version	
def makemessage(thisbillrow, signups, recipients, emailtitle, longmessage, Paylog):
    ''' Make and send email bill with amounts, signup details 
    pass family's row from bill, signup details, payment logbook, and list of email recipients '''
    balance=-thisbillrow.Balance  # int or float
    SUstring='' 
    for index,row in signups.iterrows():
        first=signups.loc[index]['First']
        last=signups.loc[index]['Last']
        sport=signups.loc[index]['Sport']
        thisstr=first + ' ' + last + ' - ' + sport + '\n'
        SUstring+=thisstr
    paystring=thisbillrow.Feepaydetail # string with prior fees, prior payment details
    recipientstr=','.join(recipients)   # convert list to string
    message='From: Cabrini Sponsors Club <sfcasponsorsclub@gmail.com>\nTo: '+ recipientstr + '\nSubject: '+ emailtitle +'\n' \
    'Please pay your outstanding balance of $'+ str(balance) +' for Cabrini sports ($30 per player ' \
    + 'per sport; $75 family max). \n\nPlayers signed up from your family this school year:\n' + SUstring +'\nPayments received ' \
    'this year: \n'+ paystring +'\nOutstanding balance: $'+str(balance) +'\n' + longmessage
    return message

# find yearseason ... now wrapped in with loadprocessfiles
def findyearseason(df):
    ''' Pass raw signups and determine year and sports season '''
    # get year from system clock and from google drive timestamp    
    now=datetime.datetime.now()
    val=df.Timestamp[0] # grab first timestamp    
    if val!=datetime.datetime: # if not a timestamp (i.e. manual string entry find one
        while type(val)!=datetime.datetime:
            for i in range(0,len(df)):
                val=df.Timestamp[i]
    year=val.year # use year value from signup timestamps
    if now.year!=val.year:
        print ('Possible year discrepancy: Signups are from ',str(val.year))
    # now find sports season
    mask = np.column_stack([df['Sport'].str.contains("occer", na=False)])
    if len(df.loc[mask.any(axis=1)])>0:
        season='Fall'
    mask = np.column_stack([df['Sport'].str.contains("rack", na=False)])
    if len(df.loc[mask.any(axis=1)])>0:
        season='Spring'
    mask = np.column_stack([df['Sport'].str.contains("asket", na=False)])
    if len(df.loc[mask.any(axis=1)])>0:
        season='Winter'   
    return season, year

def dropcolumns(df1,df2):
    ''' Pass two dfs with df2 being the template.. extra unnecessary columns dropped from df1
    inplace=True modifies both passed and returned df  '''
    cols1=df1.columns.tolist()
    if type(df2)==list:
        cols2=df2
    else: # should be dataframe
        cols2=df2.columns.tolist()
    newdf=df1 # avoids modification of passed df
    uniquelist=[i for i in cols1 if i not in cols2]
    for i,colname in enumerate(uniquelist): # remove cols from df1 that are absent from df2
        # newdf.drop(colname, axis=1, inplace=True) # this modifies both passed and returned dfs
        newdf=newdf.drop(colname, axis=1)
    return newdf

	
# older method of calculating age in loop 
def calculateage(df):
    '''pass df such as Juniorteams with birthdate column/timestamp format 
    return with an added column containing age in years (e.g. 6.1 yrs)'''  
    mytime=datetime.datetime.now() 
    mytime=datetime.datetime.date(mytime) # convert time to datetime.date
    for index, row in df.iterrows():
        dob=df.loc[index]['Birthdate']  
        if str(dob)=='NaT' or str(dob)=='nan': # skip age calc if DOB is missing
            continue        
        dob=datetime.datetime.date(dob) # convert pandas timestamp dob to datetime.date 
        age=mytime-dob # datetime timedelta
        age = round((age.days + age.seconds/86400)/365.2425,1) # get age as float
        df=df.set_value(index,'Age',age)
    return df 

# Old way of doing grade adjustment (now direct from SCsignup by row)
def updategradeadjust(df, year):
    '''Recalc grade adjustment if blank in players.csv 
    only really needs to be run every new school year
    '''    
    now=datetime.datetime.now()
    for index, row in df.iterrows():        
        grade=df.loc[index]['Grade'] # assume all grades present in players.csv
        gradeadj=df.loc[index]['Gradeadj']
        dob=df.loc[index]['DOB']
        if str(dob)=='NaT' or grade=='nan': # skip players with no DOB on file
            continue
        dob=datetime.datetime.date(dob) # conver
        if str(gradeadj)=='nan': # calc gradeadj only for those with missing values
            if grade=='K':
                grade=0
            tempyear=now.year-int(grade) # year player entered K
            entryage=datetime.date(tempyear,8,1)-dob # age at Aug 1 school cutoff in year kid entered K
            entryage = (entryage.days + entryage.seconds/86400)/365.2425 # age entering K
            if 5 < entryage <6: # normal K age
                gradeadj=0
            elif 4 < entryage <5: # ahead of schedule
                gradeadj=1
            elif 6 < entryage <7: # 1 year back
                gradeadj=-1       
            elif 7 < entryage <8: # working on grade school mustache
                gradeadj=-2
            else: # probably some entry error
                first= df.loc[index]['First']
                last= df.loc[index]['Last']
                print('Suspected DOB or grade error for ', first, ' ', last,' Grade ', grade, 'DOB', datetime.date.strftime(dob, "%m/%d/%y") )
                continue # don't make gradeadj entry
            # now update grade and gradeadj in players database
            df=df.set_value(index,'Gradeadj',gradeadj)
    return df # updated with grades and grade adjustments
