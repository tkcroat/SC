# -*- coding: utf-8 -*-
"""
Created on Sun May 22 10:30:01 2016
SC billing functions
@author: tkc
"""
#%%
import pandas as pd
import datetime
import smtplib
import re
import numpy as np
from email.mime.text import MIMEText
import tkinter as tk
import math
import glob

#%%

def sendbills_tk(Mastersignups, paylog, famcontact, players, season, year, teams):
    ''' Inteface for billing email messages to parents (non-generic)
    TODO test recruit, missing unis, unireturn
    '''
    # first print out existing info in various lines
    root = tk.Tk()
    root.title('Send e-mail bills to parents')

    unifilename=tk.StringVar()
    billfilename=tk.StringVar()
    # Look for most recent missing uniform list
    try:
        unifiles=glob.glob('missingunilist*') # find most recent uniform file name
        if len(unifiles)>1:
            unifile=findrecentfile(unifiles) # return single most recent file
        else:
            unifile=unifiles[0]
        # find most recent missing uni file name
        unifilename.set(unifile)
    except: # handle path error
        unifilename.set('missingunilist.csv')
    # Look for most recent billing files
    try:
        billfiles=glob.glob('billlist*') # find most recent uniform file name
        if len(billfiles)>1:
            billfile=findrecentfile(billfiles) # return single most recent file
        else:
            billfile=billfiles[0]
        # find most recent missing uni file name
        billfilename.set(billfile)
    except: # handle path error
        billfilename.set('billlist.csv')
                
    emailtitle=tk.StringVar()  # e-mail title 
    messfile=tk.StringVar() # text of e-mail message
    SMSmessfile=tk.StringVar()  # find replace text for SMS message?  
    mtype=tk.StringVar() # uniform night or generic
    ''' Already baked into billlist creation
    pastseasons=tk.IntVar()
    pastseasons.set(1)
    '''
    oldunibool=tk.BooleanVar()
    oldunibool.set(True)
    newunibool=tk.BooleanVar()
    newunibool.set(True)
    feesbool=tk.BooleanVar() # 
    feesbool.set(True)
    extraname=tk.StringVar() # name for additional text entry box (various uses mostly filenames)
    extraname.set('Extra file name') # default starting choice
    extravar=tk.StringVar() # name for additional text entry box (various uses mostly filenames)
    sendemailbool=tk.BooleanVar() # regular send e-mail option
    sendemailbool.set(True)
    sendSMSbool=tk.BooleanVar() # send e-mail to SMS option
    sendSMSbool.set(False)
    choice=tk.StringVar()  # test or send -mail 
    
    # E-mail title and message file name
    tk.Label(root, text='Title for e-mail').grid(row=0, column=0)
    titleentry=tk.Entry(root, textvariable=emailtitle)
    titleentry.config(width=50)
    titleentry.grid(row=0, column=1)
    tk.Label(root, text='messagefile').grid(row=1, column=0)
    messentry=tk.Entry(root, textvariable=messfile)
    messentry.config(width=50)
    messentry.grid(row=1, column=1)
    tk.Label(root, text='SMSmessagefile').grid(row=2, column=0)
    messentry=tk.Entry(root, textvariable=SMSmessfile)
    messentry.config(width=50)
    messentry.grid(row=2, column=1)
    #tk.Label(root, text='# of past seasons to include').grid(row=3, column=0)
    #tk.Entry(root, textvariable=pastseasons).grid(row=3, column=1)
    
    tk.Label(root, text='Uniform file name').grid(row=3, column=0)
    unientry=tk.Entry(root, textvariable=unifilename)
    unientry.grid(row=3, column=1)

    tk.Label(root, text='Billing file name').grid(row=4, column=0)
    billentry=tk.Entry(root, textvariable=billfilename)
    billentry.grid(row=4, column=1)

    extranameentry= tk.Entry(root, text=extraname)
    extranameentry.grid(row=5, column=0)
    extravalentry=tk.Entry(root, textvariable=extravar)
    extravalentry.grid(row=5, column=1)
    
    def Olduniopts():
        ''' Display relevant choices for old uniforms'''
        if oldunibool.get()==True:
            unientry.config(state=tk.NORMAL)
        else:
            unientry.config(state=tk.DISABLED)
    def Feesopts():
        ''' Display relevant choices for fees '''
        if feesbool.get()==True:
            billentry.config(state=tk.NORMAL)
        else:
            billentry.config(state=tk.DISABLED)
        
    tk.Checkbutton(root, variable=feesbool, text='Ask for fees?', command=Feesopts).grid(row=0, column=2)
    tk.Checkbutton(root, variable=oldunibool, text='Ask for old uni return?', command=Olduniopts).grid(row=1, column=2)
    tk.Checkbutton(root, variable=newunibool, text='Inform about new unis needed?').grid(row=2, column=2)
    tk.Checkbutton(root, variable=sendemailbool, text='Send email bills?').grid(row=3, column=2)
    tk.Checkbutton(root, variable=sendSMSbool, text='Send email bills via SMS?').grid(row=4, column=2)
    
    def Uninightopts():
        ''' Display relevant choices for team assignment notification/cyc card/ short team recruiting '''
        messfile.set('ebill_uninight_allseasons.txt')
        SMSmessfile.set('ebill_uninight_allseasons_SMS.txt')
        emailtitle.set('Cabrini Sports Uniform Night Info for $UNIDATETIME')
        extranameentry.config(state=tk.NORMAL)
        extravalentry.config(state=tk.NORMAL)
        extraname.set('Uniform night date-time')
        extravar.set('Sun 11/15/17 from 12-2 PM')
        
    def Ebillopts():
        ''' Display relevant choices for generic e-billing'''
        messfile.set('ebill_generic.txt')
        emailtitle.set('Please pay your Cabrini sports fees.')
        extranameentry.config(state=tk.DISABLED)
        extravalentry.config(state=tk.DISABLED)
        SMSmessfile.set('ebill_generic_SMS.txt')
        extraname.set('n/a')
        extravar.set('n/a')
        
    # Choose generic billing or uniform night billing
    tk.Radiobutton(root, text='Uniform night billing', value='Uninight', variable = mtype, command=Uninightopts).grid(row=7, column=0)
    tk.Radiobutton(root, text='Generic ebilling', value='Ebill', variable = mtype, command=Ebillopts).grid(row=7, column=1)
    
    # Specific team selector section using checkboxes
    teamdict=shortnamedict(teams)
    teamlist=[] # list of tk bools for each team
    # Make set of bool/int variables for each team
    for i, val in enumerate(teamdict):
        teamlist.append(tk.IntVar())
        if '#' not in val:
            teamlist[i].set(1) # Cabrini teams checked by default
        else:
            teamlist[i].set(0) # transfer team
    rownum=8
    # make checkbuttons for each team
    for i, val in enumerate(teamdict):
        thisrow=i%5+1+rownum # three column setup
        thiscol=i//5
        thisname=teamdict.get(val,'')
        tk.Checkbutton(root, text=thisname, variable=teamlist[i]).grid(row=thisrow, column=thiscol)
    rownum+=math.ceil(len(teamlist)/5)+2
    # Decision buttons bottom row
    def chooseall(event):
        ''' Select all teams '''
        for i, val in enumerate(teamdict):
            teamlist[i].set(1)
    def clearall(event):
        ''' deselect all teams '''
        for i, val in enumerate(teamdict):
            teamlist[i].set(0)
    def abort(event):
        choice.set('abort')        
        root.destroy()
        
    def test(event):
        choice.set('test')        
        root.destroy()  

    def KCsend(event):
        ''' Live send but only send to kcroat@gmail or tkc@wustl '''
        choice.set('kcsendtest')
        root.destroy()
        
    def send(event):
        choice.set('send')        
        root.destroy()  
    rownum+=1
    d=tk.Button(root, text='All teams')
    d.bind('<Button-1>', chooseall)
    d.grid(row=rownum, column=0)
    
    d=tk.Button(root, text='Clear teams')
    d.bind('<Button-1>', clearall)
    d.grid(row=rownum, column=1)
    
    d=tk.Button(root, text='Abort')
    d.bind('<Button-1>', abort)
    d.grid(row=rownum, column=2)

    d=tk.Button(root, text='Test')
    d.bind('<Button-1>', test)
    d.grid(row=rownum, column=3)

    d=tk.Button(root, text='KC send test')
    d.bind('<Button-1>', KCsend)
    d.grid(row=rownum, column=4)

    d=tk.Button(root, text='Send')
    d.bind('<Button-1>', send)
    d.grid(row=rownum, column=5)

    root.mainloop()

    mychoice=choice.get()
    
    if mychoice!='abort':
        kwargs={}
        if mychoice=='kcsendtest':
            mychoice='send'
            kwargs.update({'kcsendtest':True})
        kwargs.update({'choice':mychoice})  # test, kcsendtest, or send
        emailtitle=emailtitle.get()
        # load blank message
        messagefile='messages\\'+messfile.get()
        try:
            with open(messagefile,'r') as file:
                blankmessage=file.read()
        except:
            print("Couldn't open message file(s)")
            
        if sendSMSbool.get():
            messagefile='messages\\'+SMSmessfile.get()
            try:
                with open(messagefile,'r') as file:
                    blankSMS=file.read()
                kwargs.update({'SMS':blankSMS})
            except:
                print('Failed load of alt SMS message.')
        try:
            billlist=pd.read_csv(billfilename.get(), encoding='cp437')
        except:
            print("Couldn't open billing list")

        '''
        # Filter bill list using teams?  Necessary?
        selteams=[]
        for i, val in enumerate(teamdict):
            if teamlist[i].get()==1:
                selteams.append(val)
        # Filter teams based on checkbox input
        teams=teams[teams['Team'].isin(selteams)]
        # drop duplicates in case of co-ed team (m and f entries)
        teams=teams.drop_duplicates('Team')
        '''
        # handle the boolean options
        if oldunibool.get():
            kwargs.update({'oldunis':True})
        if newunibool.get():
            kwargs.update({'newunis':True})
        if feesbool.get():
            kwargs.update({'fees':True})
        if sendemailbool.get():
            kwargs.update({'ebills':True})
        if sendSMSbool.get():
            messagefile='messages\\'+SMSmessfile.get()
            with open(messagefile,'r') as file:
                blankSMS=file.read()
            kwargs.update({'SMS':blankSMS}) # pass blank alt SMS message in kwargs
        ebilllist, skiplist = sendebills(billlist, Mastersignups, season, year, emailtitle, blankmessage, **kwargs)
    return ebilllist, skiplist


def loadoldteams(seasons, years):
    ''' For retroactive billing, load teams from any prior season/year combination or from 
    lists of seasons & years
    '''    
    teams=pd.read_excel('Teams_coaches.xlsx', sheetname='Oldteams')
    sportsdict={'Fall':['VB','Soccer'], 'Winter':['Basketball'],'Spring':['Track','Softball','Baseball','T-ball']}
    if isinstance(seasons,str):
        sportlist=sportsdict.get(seasons)
    else: # construct sport list from list of seasons
        sportlist=[]
        for i, seas in enumerate(seasons):
            sportlist.extend(sportsdict.get(seas))
    if isinstance(years,int):
        years=[years] # convert single year to list of years
    teams=teams.loc[(teams['Sport'].isin(sportlist)) & (teams['Year'].isin(years))]
    return teams

def getpayments(thispay, priorpay):
    '''df rows with lists of this and prior season's payments '''
    # thispay is df with one families payments from this season/year
    # TODO convert paykey permanently to int (avoid possible conversion problems)
    # TODO also maybe check if payment date in expected range (in getpayments)
    paykeys=[]
    currpayment=0.0 # set default amount for return
    priorpayment=0.0 
    paydetail=''
    paytext=[] # for string with SMS 
    if len(thispay)>0:
        paykeys=list(thispay.Paykey.unique())
        paykeys=[int(i) for i in paykeys] # convert list to integers
        currpayment=thispay.Amount.sum()
        for index, row in thispay.iterrows():
            paydate=thispay.loc[index]['Date'].to_pydatetime() # get timestamp as datetime obj
            paydetail+=thispay.loc[index]['Season']+' '+str(thispay.loc[index]['Year'])+' payment: $'
            paydetail+=str(int(thispay.loc[index]['Amount']))+' on '
            paydetail+=datetime.datetime.strftime(paydate, "%m/%d/%Y")+' \n'
    if len(priorpay)>0:
        priorkeys=list(priorpay.Paykey.unique())
        priorkeys=[int(i) for i in priorkeys] # convert list to integers
        paykeys.extend(priorkeys)
        priorpayment+=priorpay.Amount.sum() # add past payments
        for index, row in priorpay.iterrows():
            paydate=priorpay.loc[index]['Date'].to_pydatetime() # get timestamp as datetime obj
            paydetail+=priorpay.loc[index]['Season']+' '+str(int(priorpay.loc[index]['Year'])) +' payment: $'
            paydetail+=str(int(priorpay.loc[index]['Amount']))+' on '
            paydetail+=datetime.datetime.strftime(paydate, "%m/%d/%Y")+' \n'
    if priorpayment+currpayment>0: # make SMS string with current and prior season payments
        paytext.append('minus $'+str(int(priorpayment+currpayment))+' prior payments received')
    return paykeys, currpayment, priorpayment, paydetail, paytext

def getmissingunis(df, famkey):
    '''Called by main billing loop... get signup keys with missing uniforms  ''' 
    df=df.dropna(subset=['Issue date']) # only signups with uniform issued
    mask=pd.isnull(df['UniReturnDate'])
    df=df.loc[mask] # keeps only unreturned uniforms
    df=df[df['Famkey']==famkey] # this family's outstanding uniforms
    unikeys=np.ndarray.tolist(df.SUkey.unique()) # list of signup keys with outstanding uniforms
    # create string for e-bill with outstanding uniforms
    unistr=''
    oldunilist=[]
    oldunitext=[]
    if len(df)>0:
        unistr+='Old uniforms to return\n'
        unistr+='Player\tSport\tUni #\tTeam\n'
        for index, row in df.iterrows():
            first=df.loc[index]['First']
            sport=df.loc[index]['Sport']
            oldunilist.append(first+' '+sport.lower())
            num=df.loc[index]['Uniform#']        
            team=df.loc[index]['Team']
            unistr+=first + '\t' + sport + '\t' +str(num) + '\t'+ team +'\n'
        ending=' uniform' # for SMS string
        if len(oldunilist)>1:
            tempstr=' and '+str(oldunilist[-1]) # prepend and to last list item
            oldunilist[-1]=tempstr
            ending+='s'
        oldunitext=[' return '+', '.join(oldunilist)+ending] # construct SMS string 
        # SMS string "return Ben soccer and Ethan VB uniforms"
    return unistr, unikeys, oldunitext    
    
def getnamesschool(plalist, players):
    '''Return school(s) associated with a list of players from players.csv (with Cabrini listed first)... called by 
    createbilllist'''
    match=players[players['Plakey'].isin(plalist)]
    schoollist=match.School.unique()
    schoollist=np.ndarray.tolist(schoollist)
    if "Cabrini" in schoollist:
        schoollist.insert(0,schoollist.pop(schoollist.index('Cabrini'))) # move Cabrini to first entry
    # now shorted player name list
    namelist=[]
    for index, row in match.iterrows():
        first=match.loc[index]['First']
        last=match.loc[index]['Last']
        strname=first+' ' +last[0]
        namelist.append(strname)
    return schoollist, namelist

def calccharges(df, season):
    '''Pass signups for single family for season and return charges and text fragment for SMS '''    
    totalcharge=0.0
    cheapsports=['T-ball','Track']
    cheapmask=df['Sport'].isin(cheapsports)
    cheapSU=df.loc[cheapmask]
    regularSU=df.loc[~cheapmask] # signup not in cheap list
    totalcharge=10*len(cheapSU)+30*len(regularSU)    
    if len(df)>2 and totalcharge>75: # use max family bill amount
        totalcharge=75.0 
    currtext='$'+str(int(totalcharge))+' for '+ season
    return totalcharge, currtext
    
def calcpriorcharges(df):
    '''Pass signups for single family for season and return charges and detailed about charges'''
    # Need to determine seasons and sort by season-year
    sportsdict={'Fall':['VB','Soccer'], 'Winter':['Basketball'],'Spring':['Track','Softball','Baseball','T-ball']}
    cheapsports=['T-ball','Track']    
    df['Season']='' # new
    totalcharge=0
    paystr=''
    for index, row in df.iterrows():
        sport=df.loc[index]['Sport']
        seasonlist=[seas for seas,key in sportsdict.items() if sport in key] # key is list of sports in this case
        df=df.set_value(index,'Season',seasonlist[0])
    
    # now calculate charges for each season-year separately
    yrs=np.ndarray.tolist(df.Year.unique()) # list of years represented
    yrs=[int(i) for i in yrs]
    priortext=[] # list of strings describing all prior season fees (not current)
    for i, year in enumerate(yrs):
        yeardf=df[df['Year']==year]
        seasons=np.ndarray.tolist(yeardf.Season.unique())
        for j, seas in enumerate(seasons): # calc for each season separately
            thisseason=yeardf[yeardf['Season']==seas] # signups from this season
            thismask=thisseason['Sport'].isin(cheapsports)
            cheapsports=thisseason.loc[thismask]
            normalsports=thisseason.loc[~thismask]
            # count and list sports from cheap and normal
            sportstr=[]
            tempdf=cheapsports['Sport'].value_counts()
            for ind, val in tempdf.iteritems():
                sportstr.append(str(val)+'x '+ind)
            tempdf=normalsports['Sport'].value_counts()
            for ind, val in tempdf.iteritems():
                sportstr.append(str(val)+'x '+ind)
            sportstr=', '.join(sportstr)
            thischarge=10*len(cheapsports)+30*len(normalsports)
            if thischarge>75:
                thischarge=75 # reduce to max family charge per season
            totalcharge+=thischarge # grand total of all prior seasons (but not current season charges)
            priortext.append('$'+str(int(thischarge))+' for '+ seas + str(year))
            paystr+=' '+seas+' '+str(year)+' '+sportstr+': $'+str(thischarge)+';'
    return totalcharge, paystr, priortext

def getdepositinfo(df, famkey, depneeded):
    '''Called by main billing loop... gets family's deposits (by paykey) from paylog (passed as df)
    returns list of paykeys to quickly find info on deposit
    differs from makemissingunilog in that this also deals with new uniforms to issue ''' 
    depmatch=df[df['Famkey']==famkey]
    depmatch=depmatch.dropna(subset=['Deposit']) # drop payments w/o associated deposits
    # find last negative value in payments logbook deposit col 
    # Take all positive deposits after that (although should be only one)
    for j in range(len(depmatch)-1,-1,-1): # backwards through the rows
        if depmatch.iloc[j]['Deposit']<0: # stop at negative value
            depmatch.drop(depmatch.index[0:j+1], inplace=True) # drops negative row and all preceding it
            break
    depamt=0
    depstr=''
    depkeys=[]
    deptext=[] # List for SMS text message
    # Grab total deposit amount on file
    depamt=depmatch.Amount.sum() # works even on empty lists
    if depamt==0: # handle both no deposit on file situations
        if depneeded==0: # dispense with those without Cabrini uniform issues
            return depkeys, depamt, depstr, deptext
        if depneeded>0: # new uniform deposit required
            depstr+='$'+str(int(depneeded))+' refundable uniform deposit required (separate check is preferred)'
            deptext.append('deliver a $'+str(int(depneeded))+' uniform deposit')
            return depkeys, depamt, depstr, deptext
    # now handle cases with uniform deposit on file (depamt>0 and thus len(depmatch)>0)
    # get details about existing deposits (skip for SMS when more deposit not required)
    depkeys.extend(np.ndarray.tolist(depmatch.Paykey.unique())) 
    depstr+='Uniform deposits on file:\n' # no-deposit on file cases already handled
    for index, row in depmatch.iterrows(): # construct and print details on all existing deposits
        depstr+=str(int(depmatch.loc[index]['Amount']))+'\t'
        depstr+=depmatch.loc[index]['Deptype']+'\t' # deposit type (cash, check, paypal, etc.)
        depdate=depmatch.loc[index]['Date'].to_pydatetime() # deposit date conv to datetime object
        depstr+=datetime.date.strftime(depdate,'%m/%d/%Y')+'\t' # formatted deposit date
        if str(depmatch.loc[index]['Depcomment'])!='nan': # skip nan comments
            depstr+=depmatch.loc[index]['Depcomment']+'\n' #     
        else:
            depstr+='\n'
    if depneeded==depamt: # deposit on file matches required deposit
        depstr+='No additional deposit required if all outstanding uniforms are returned'
    elif depamt>depneeded: # refund, hold or destroy check situation
        # check if type of existing deposits are all cash
        deptypelist=np.ndarray.tolist(depmatch.Deptype.unique())
        if len(depmatch.Deptype.unique())==1 and 'cash' in deptypelist: # all cash deposits
            refundamt=int(depamt-depneeded)
            depstr+='$'+str(refundamt)+' cash deposit refunded if all old uniforms are returned.' 
    elif depneeded>depamt: # some deposits on file but more is needed
        extradep=int(depneeded-depamt)
        depstr+='Additional $'+str(extradep)+' deposit needed: separate check preferred.'
    return depkeys, depamt, depstr, deptext # list of unique keys to active deposits in paylog for this family

def makenewunistring(curmatch, uniteams, transferteams):
    '''Curmatch is given family's list of current signups with team assignment.. check team against uniteams (subset
    with Y in uniforms col)
    Return detailed string for new unis to be issued and total deposit needed on file '''
    # get subset of current signups that require issuing a new uniform
    depneeded=0
    newunikeys=[]
    depstr=''
    if len(curmatch)>0: # new uniforms to be issued
        depstr='New uniforms for this season:\n'
    cabunis=pd.merge(curmatch,uniteams, how='inner', on=['Team'], suffixes=('','_r')) 
    transferunis=pd.merge(curmatch,transferteams, how='inner', on=['Team'], suffixes=('','_r')) 
    unitext=[] # return as list item
    if len(cabunis)>0: # Cabrini uniforms will be issued
        unitextlist=[] # string(s) for SMS 
        # return required deposit amount     
        depneeded=25*len(cabunis) # update required deposit amount
        newunikeys=np.ndarray.tolist(cabunis.SUkey.unique())
        # Make SMS string (saying pick up Ben's soccer and Ethan's VB uniform)
        for index, row in cabunis.iterrows():
            unitextlist.append(cabunis.loc[index]['First']+' '+cabunis.loc[index]['Sport'])
            depstr+=cabunis.loc[index]['First']+' \t'
            depstr+=cabunis.loc[index]['Sport'].lower()+'\t'
            depstr+='- Pick up at Cabrini Uniform Night\n'
        ending=' uniform'
        if len(unitextlist)>1:
            unitextlist[-1]='and '+ unitextlist[-1] # prepend and to last item
            ending+='s'
        unitext=['pick up '+', '.join(unitextlist)+ending] 
        # easier to construct entire string if passed as list item        
    # now mention transfer and junior team uniform requirements
    if len(transferunis)>0:
        for index, row in transferunis.iterrows():
            depstr+=transferunis.loc[index]['First']+'\t'
            depstr+=transferunis.loc[index]['Sport']+'\t'
            depstr+='- Pick up from '
            school=transferunis.loc[index]['Team'].split('#')[0]
            depstr+=school+'\n'
    # Now find Cabrini junior team signups
    jrteamlist=np.ndarray.tolist(curmatch.Team.unique()) # assigned teams
    uniteamlist=np.ndarray.tolist(uniteams.Team.unique())
    transferteamlist=np.ndarray.tolist(transferteams.Team.unique())
    jrteamlist=[str(team) for team in jrteamlist if team not in uniteamlist and team not in transferteamlist]
    jrunis=curmatch[curmatch['Team'].isin(jrteamlist)]
    if len(jrunis)>0:
        for index, row in jrunis.iterrows():
            depstr+=jrunis.loc[index]['First']+'\t'
            depstr+=jrunis.loc[index]['Sport']+'\t'
            depstr+='- Use Cabrini navy uniform T-shirt (available for $10 at Uniform Night)\n'        
    # depneeded -- amount of required deposit (passed to getdepositinfo for handling) 
    return depstr, depneeded, newunikeys, unitext
    
def getthisperiod(df, season, year, priorseasons):
    ''' Return subset of df from this sports season and also n prior seasons, year is starting school year 
    date-based slicing of dfs would be easier, but not a good match for season-year based accounting normally used
    typically pass either paylog or mastersignups to get payments or signups respectively'''
	# first grab current signups
    mycols=df.dtypes.index
    priordf=pd.DataFrame(columns=mycols) # frame for returned data subset
    seasonorder={'Fall':0, 'Winter':1,'Spring':2}
    seasonnum=seasonorder.get(season)
    # this year's allowed seasons
    thisyrseasons=[seas for seas,num in seasonorder.items() if num<seasonnum and seasonnum-num<priorseasons+1] # prior seasons in range from this year (not including current one)
    numlastseasons=priorseasons-len(thisyrseasons)
    # Now return any seasons in range from last year (again based on # of priorseasons)
    lastyrseasons=['Spring','Winter','Fall'] # looking back so these seasons in reverse
    lastyrseasons=lastyrseasons[0:numlastseasons]
    if 'Season' in df: # paylog or some other dfs have direct season column
        tempdf=df[df['Year']==year]
        currentdf=tempdf[tempdf['Season']==season] # i.e for this season's payments
        tempdf=tempdf[tempdf['Season'].isin(thisyrseasons)] # prior ones from this year but not this season
        priordf=pd.concat([tempdf,priordf]) # add rows from this year (usually payments from paylog)
        tempdf=df[df['Year']==year-1]
        tempdf=tempdf[tempdf['Season'].isin(lastyrseasons)]
        priordf=pd.concat([tempdf,priordf])
        return currentdf, priordf # 
    elif 'Sport' in df: # usually for Mastersignups
        sportsdict={'Fall':['VB','Soccer'], 'Winter':['Basketball'],'Spring':['Track','Softball','Baseball','T-ball']}
        currentsports=sportsdict.get(season) # this season's signups separate
        thisyrsports=[val for key,val in sportsdict.items() if key in thisyrseasons] # other signups this year prior seasons
        thisyrsports=[item for sublist in thisyrsports for item in sublist] # flatten if it's a list of lists
        tempdf=df[df['Year']==year]
        currentdf=tempdf[tempdf['Sport'].isin(currentsports)]
        tempdf=tempdf[tempdf['Sport'].isin(thisyrsports)]
        priordf=pd.concat([tempdf,priordf]) # add rows from this year (usually payments from paylog)
        # now get allowed row (usually signups) from last year 
        lastyrsports=[val for key,val in sportsdict.items() if key in lastyrseasons]
        lastyrsports=[item for sublist in lastyrsports for item in sublist] # flatten if it's a list of lists
        tempdf=df[df['Year']==year-1]
        tempdf=tempdf[tempdf['Sport'].isin(lastyrsports)]
        priordf=pd.concat([tempdf,priordf]) # add rows from this year (usually payments from paylog)
        return currentdf, priordf
    else:
        print('Error: Season and Sport columns missing from passed dataframe')
        return

def createbilllist(df, Paylog, famcontact, players, season, year, teams, priorseasons=1, fname='Billlist8Dec16.csv', **kwargs):
    ''' Pass mastersignsups and charges/signups from current season and n priorseasons, output billing list by family 
    priorseason is chronological lookback incl last seasons
    unikeys/depkeys are SUkey and paykey containing outstanding uniforms and uniform deposit (since uni info is 
    stored in master_signups and deposit info in paylog
    calls calccharges and calcpriorcharges separately for set of included season-years
    kwargs: olduni - ask for old missing uniforms
            newuni - info about new uniforms to be issued
        '''
    season=season.title()
    season=season.strip() # remove any spaces
    Paylog['Season']=Paylog['Season'].str.title()
    Paylog['Season']=Paylog['Season'].str.strip() # remove spaces
    if len(Paylog.Season.unique())!=3:
        print('Check payment logbook season column for improper entry.. must be Fall, Winter, or Spring')
    # Remove players than have dropped (drop as team assignment) 
    thismask=df['Team'].str.contains('drop',na=False,case=False)
    df=df.loc[~thismask]
    df=df.dropna(subset=['Team']) # also drop those not yet assigned to a team
    CurrentSU, PriorSU =getthisperiod(df, season, year, priorseasons) # returns subset of signups in specified period
    AllSU=pd.concat([CurrentSU,PriorSU])
    Currentpay,Priorpay=getthisperiod(Paylog, season, year, priorseasons) # returns payments in specified period
    # Copy currentsu df ... drop duplicates using famkey
    # Selects only active families in this billing period
    fambills=AllSU # copy and use as template for family bills 
    fambills=fambills.drop_duplicates('Famkey') # single row per family
    fambills=fambills.reset_index(drop=True)
    # depkey is paykey containing deposit, unikey is SUkey with issued outstanding uniform
    # signups split into this season and prior season(s) with lookback set by priorseasons
    newcols=['Feepaydetail','Plakeys','SUkeys','PriorSUkeys','Paykeys','Depkeys','Newunikeys','Oldunikeys','Unidetail','Textmessage','Teams','Comments','School','Players']
    for i, col in enumerate(newcols):
        fambills[col]='' # init to np.nan causes later write problems so use ''
    fambills['Charges']=0.0
    fambills['PriorCharges']=0.0 # From prior sports season
    fambills['Balance']=0.0
    fambills['PriorBalance']=0.0
    fambills['CurrPayments']=0.0
    fambills['PriorPayments']=0.0
    # Get subset of teams that'll be issued new uniforms
    uniteams=teams[teams['Uniforms']=='Y'] # Cabrini uniform teams (also typically with hyphen)
    transferteams=teams[teams['Team'].str.contains('#')]
    # now merge in contact info from famcontact
    fambills=pd.merge(fambills, famcontact, how='inner', on=['Famkey'], suffixes=('','_r'))
    fambills['Family']=fambills['Family_r'] # missing from some entries in AllSU

    for index, row in fambills.iterrows():
        # get playerkeys and signup keys for this family
        famkey=fambills.iloc[index]['Famkey']
        match=AllSU[AllSU['Famkey']==famkey] # find this family in current signups
        curmatch=CurrentSU[CurrentSU['Famkey']==famkey]
        plalist=np.ndarray.tolist(match.Plakey.unique()) # add keys with recently active players
        plalist=[i for i in plalist if str(i)!='nan'] # shouldn't be nan but somehow occurred
        plalist=[int(i) for i in plalist] # ensure conversion to ints
        schools, planames =getnamesschool(plalist, players) # Determine if at least one kid is from Cabrini
        tempstr=', '.join([str(i) for i in plalist]) # convert to comma separated str and save
        fambills=fambills.set_value(index,'Plakeys', tempstr)        
        sukeys=np.ndarray.tolist(curmatch.SUkey.unique()) # add signup keys for this season only
        sukeys=[int(i) for i in sukeys]
        fambills=fambills.set_value(index,'School',', '.join(schools))
        fambills=fambills.set_value(index,'Players',', '.join(planames)) # list of abbrev player names
        if len(sukeys)>0:
            tempstr=', '.join([str(i) for i in sukeys])        
            fambills=fambills.set_value(index,'SUkeys',tempstr) # save string of keys (current season only)
        teamlist=list(match.Team.unique()) # full team list for these players in specified period
        fambills=fambills.set_value(index,'Teams',', '.join(teamlist)) # save teams as string
        
        textfee=[] # list of strings for fees text message
        currentcharge, currtext=calccharges(curmatch, season) # returns cost for this sports season
        textfee.append(currtext) # info on this seasons charges for text message
        priormatch=PriorSU[PriorSU['Famkey']==famkey] # prior signups within specified period
        textmess=[] # list of strings for text message uniform details
        priorcharge, priorfeestr, priortext =calcpriorcharges(priormatch) # 
        # priortext is a list of strings (one for each prior season)
        textfee.extend(priortext) # info on prior fees for text message; merge both lists
        priorSUkeys=np.ndarray.tolist(priormatch.SUkey.unique())
        priorSUkeys=[int(i) for i in priorSUkeys]
        if len(priorSUkeys)>0:
            tempstr=', '.join([str(i) for i in priorSUkeys]) # convert int to str and then comma sep. list
            fambills=fambills.set_value(index,'PriorSUkeys',tempstr) 
        fambills=fambills.set_value(index,'Charges',currentcharge) # store in billing df
        fambills=fambills.set_value(index,'PriorCharges',priorcharge) 
        # Call function to generate uniform/deposit messages strings if desired
        unistuff={} # blank dictionary to check for optional returns
        if kwargs.get('newuni', False) or kwargs.get('olduni', False):
            textmess, unistuff = makeunidepstring(df, famkey, Paylog, curmatch, uniteams, transferteams, textmess, **kwargs)
        # note: uniforms if required are associated with each signup in mastersignups
        # Write all the optional uniform keys and such to fambills
        if 'depkeys' in unistuff: # uniform key values from mastersignups optionally returned in list
            depkeys=unistuff.get('depkeys',[])
            tempstr=tempstr=", ".join([str(i) for i in depkeys])
            fambills=fambills.set_value(index,'Depkeys',tempstr)
        if 'oldunikeys' in unistuff: # keys from mastersignup for old uniforms
            oldunikeys=unistuff.get('oldunikeys',[])
            tempstr=tempstr=", ".join([str(i) for i in oldunikeys])
            fambills=fambills.set_value(index,'Oldunikeys',tempstr)
        if 'newunikeys' in unistuff:
            newunikeys=unistuff.get('newunikeys',[])
            tempstr=tempstr=", ".join([str(i) for i in newunikeys])
            fambills=fambills.set_value(index,'Newunikeys',tempstr)
        if 'fullunistr' in unistuff:
            fullunistr=unistuff.get('fullunistr','')
            fambills=fambills.set_value(index,'Unidetail',fullunistr) # string w/ all unis for return (will be use by ebill)
        # Get payment amounts, paykeys, and paystring from current and priorpay for this family 
        thispay=Currentpay[Currentpay['Famkey']==famkey] # df rows with this family's current payments
        priorpay=Priorpay[Priorpay['Famkey']==famkey] # df rows with this family's prior payments
        paykeys, currpayment, priorpayment, paydetails, paytext = getpayments(thispay, priorpay)
        textfee.extend(paytext) # add info about prior payment to text message
        if len(paykeys)!=0: # keep as nan if no payments
            tempstr=', '.join([str(i) for i in paykeys])
            fambills=fambills.set_value(index,'Paykeys',tempstr) # list of payment keys (usually 1 or 0)
        fambills=fambills.set_value(index,'CurrPayments',currpayment) # total of rec'd payments for this season
        fambills=fambills.set_value(index,'PriorPayments',priorpayment)
        fambills=fambills.set_value(index,'PriorBalance',priorpayment-priorcharge)
        balance=currpayment+priorpayment-priorcharge-currentcharge # total fee balance (negative if amt owed)
        fambills=fambills.set_value(index,'Balance',balance) # update balance
        # Feepaydetail has fees from prior seasons and payment detail for current and prior 
        fambills=fambills.set_value(index,'Feepaydetail', priorfeestr+paydetails) # prior charges and pay
        # construct custom portion of text message
        # "on jan 4th from 6-7:30 at the Cabrini gym please"... message header
        # if money owed, add fee portion to long text message (includes textfee)
        if balance<0:
            tempstr='pay your sports fee balance of $'+str(int(-balance)) +' ' 
            tempstr+='('+', '.join(textfee)+')'
            textmess.append(tempstr) # add phrase with fees
        if len(textmess)>1: # prepend and to last phrase
            tempstr=' and '+ str(textmess[-1])
            textmess[-1]=tempstr
        tempstr=', '.join(textmess)
        fambills=fambills.set_value(index,'Textmessage',tempstr)        
        # TODO 
    mycols=['Family', 'Charges', 'PriorCharges','CurrPayments', 'PriorPayments', 'PriorBalance','Balance','Feepaydetail', 'Email1','Email2','Phone1','Phone2','Pfirst1','Plast1','Teams', 'SUkeys', 'PriorSUkeys', 'Plakeys', 'Paykeys','Depkeys','Newunikeys','Oldunikeys','Unidetail','Textmessage','Famkey','School','Players','Comments']
    fambills=fambills[mycols]
    fambills=fambills.sort_values(['Balance'], ascending=True)
    fambills.to_csv(fname, index=False)
    return fambills

def makeunidepstring(df, famkey, Paylog, curmatch, uniteams, transferteams, textmess, **kwargs):
    ''' Optional call to make message string about old, new uniforms and deposit on file info 
    unistuff dictionary can include:  newunikeys, oldunikeys -- key values from mastersignups for this uniform
    depneeded - amount of new deposit required '''
    # Uniform and deposits section (depending on kwargs)
    # Now generate new unistring containing info about new uniforms to be issued (curmatch and assigned team)
    # deposit info needed if for old or new unis (and fnct not called unless 1 of 2 is true)
    unistuff={} # optional returns of various items to createbilllist
    if kwargs.get('newuni', False): # new uniforms and deposit info required are linked
        newunistr, depneeded, newunikeys, unitext =makenewunistring(curmatch, uniteams, transferteams)
        depkeys, depamt, depstr, deptext=getdepositinfo(Paylog, famkey, depneeded) # retrieve active deposits (independent of current period)
        textmess.extend(unitext) # extend list with info about new unis to pick up
        textmess.extend(deptext) # add info about deposit
        unistuff.update({'newunikeys':newunikeys}) # list of keys for new uniforms to be issued
        unistuff.update({'depneeded':depneeded}) # amount of deposit required
        unistuff.update({'newunistr':newunistr})
        unistuff.update({'depkeys':depkeys})
        unistuff.update({'depamt':depamt}) 
        unistuff.update({'depstr':depstr}) 
    if kwargs.get('olduni', False):    
        # returns key from paylog containing uni deposit and unistr w/ details on outstanding uniforms
        oldunistr, oldunikeys, oldunitext=getmissingunis(df, famkey) # df from master_signups
        textmess.extend(oldunitext)
        unistuff.update({'oldunistr':oldunistr})
        unistuff.update({'oldunikeys':oldunikeys})
    # TODO reminder to return unis from transfer teams
    # Unistr, newunis and deposit info rolled into single text string (stored in Unidetail)
    # now construct full uniform info string for message 
    fullunistr=''
    if 'oldunistr' in unistuff:
        fullunistr+=unistuff.get('oldunistr','') # append stuff about old uniforms
    if 'newunistr' in unistuff:
        fullunistr+=unistuff.get('newunistr','') # append stuff about new uni pickup
    if 'depstr' in unistuff:
        fullunistr+=unistuff.get('depstr','') # definitely needed if makeunidepstring is called
    unistuff.update({'fullunistr':fullunistr})
    return textmess, unistuff

def matchpayment(df,players):
    '''Find famkey (and plakeys secondarily) associated with a given payment by matching player and family names
    First field can have multiple names;  '''
    # match only needed for payments not yet assigned to family 
    needmatch=df[df['Famkey'].isnull()]
    # make frame for payments with no obvious match
    newplayers=pd.DataFrame(columns=['Paykey', 'Date', 'First', 'Last', 'Amount', 'Paytype', 'Comment',
       'Sport', 'Season', 'Year', 'Famkey', 'Family name', 'Plakey', 'Email',
       'Phone', 'Delivered', 'Notes'])
    for index, row in needmatch.iterrows():
        last=needmatch.loc[index]['Last']
        last=last.title() # title case
        first=needmatch.loc[index]['First'] # shouldn't have any nan values
        first=first.title() # switch to title case
        if ',' in first: # sometimes multiple first names in paylog entry
            first=first.split(',')[0] # just take first of the first names
        # Check for last name match
        match = players[(players['Last']==last)]
        if len(match)==0:
            print ('No last name match for player', last, '. Check for consistency')
            newplayers=newplayers.append(df.loc[index])
            continue
        # Check for first and last match
        match = players[(players['Last']==last) & (players['First'].str.contains(first, na=False, case=False))]
        if len(match)==1: # first/last match with players.csv
            df=df.set_value(index,'Plakey',match.iloc[0]['Plakey'])
            df=df.set_value(index,'Famkey',match.iloc[0]['Famkey'])
            df=df.set_value(index,'Family',match.iloc[0]['Family'])
            print('Payment processed for family',match.iloc[0]['Family'])                   
            continue
        elif len(match)>1: # first/last matches multiple players (name is too common?)
            print('First and last matches multiple players:',first, ' ',last)
        else:
            print('Recheck name against players db.. no match for player :',first,' ',last,'.' ) #no first/last match, no last/DOB match
            newplayers=newplayers.append(df.loc[index])       
            continue
    return df, newplayers # same df but with all available player numbers added in playkey column

def sendemaillogic(billlist, **kwargs):
    '''Filtering criteria that decides who gets an e-mail (using flags set by kwargs
    if any flag is true (i.e. outstanding uniform, new uni to issue, owes money then e-mail is sent
    kwargs are: olduni, newuni,fees booleans, defaulting to False, False, True '''
    # Now check for fees (negative balance), new unis(newunikeys col), old unis (oldunikeys) depending on passed flags
    # concat multiple masks together via or (if any are true, text is sent)
    # replace nan with blank strings
    billlist.Oldunikeys=billlist.Oldunikeys.fillna(value='')
    billlist.Newunikeys=billlist.Newunikeys.fillna(value='')
    billlist.Newunikeys=billlist.Newunikeys.astype(str)
    billlist.Oldunikeys=billlist.Oldunikeys.astype(str)
    if kwargs.get('olduni', False):
        oldmask1=billlist['Oldunikeys']!='' # must deal with possible blanks or nans (depending on reimport or not)
        oldmask2=~billlist['Oldunikeys'].isnull()
        oldmask=(~oldmask1 |oldmask2) # true means has old uni to return
        # oldmask=~billlist['Oldunikeys'].isnull()
    else: # if arg is false, pass mask that is always false (since combined with pandas OR)
        oldmask=pd.Series(data=False, index=billlist.index)
    if kwargs.get('newuni', False):
        newmask1=billlist['Newunikeys']!='' 
        newmask2=~billlist['Newunikeys'].isnull()
        newmask=(~newmask1 | newmask2) # true means new uni to pick up
    else: # if arg is false, pass mask that is always false (since combined with pandas OR)
        newmask=pd.Series(data=False, index=billlist.index)
    if kwargs.get('fees', True):
        feemask=billlist['Balance']<0 # negative balance means fees owed
    else: # if arg is false, pass mask that is always false (since combined with pandas OR)
        feemask=pd.Series(data=False, index=billlist.index)
    fullmask=(oldmask | newmask | feemask) # combine multiple boolean series with OR
    emaillist=billlist.loc[fullmask] # if any are true (old uni, new uni, owes money)
    skiplist=billlist.loc[~fullmask] # if all are false
    return emaillist, skiplist
  
def getemailadds(thisbillrow):
    '''Find email address(es) from series (single family row from bill and return as list ''' 
    email1=str(thisbillrow.Email1)
    email2=str(thisbillrow.Email2)
    recipients=[]
    if '@' in email1:
        recipients.append(email1)
    if '@' in email2:
        recipients.append(email2)
    return recipients
    
def sendebills(billlist, Mastersignups, season, year, emailtitle, blankmessage, **kwargs):
    '''From bill list of payments, balances, and signups, generate and send email bill
    currently not including SMS 
    kwargs: olduni, newuni, fees  -- passed through to sendemaillogic  
    '''
    choice=kwargs.get('choice','test')
    if choice=='send':
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587) # port 587
        smtpObj.ehlo() # say hello
        smtpObj.starttls() # enable encryption for send 
        print('Enter password for sponsors club gmail ')
        passwd=input()
        smtpObj.login('sfcasponsorsclub@gmail.com', passwd)
        # string to record in comments that bill was sent
        commstring='email '+ datetime.date.strftime(datetime.datetime.now(), "%m/%d/%y") 
        # email generation and send loop
        billlist.Comments=billlist.Comments.astype(str) # info about send recorded in comments
    else: # testing only... open log file
        logfile=open('ebilling_log.txt','w', encoding='utf-8')
    # somewhat redundant though since emails/texts recorded to text log files
    ebilllist=billlist[(pd.notnull(billlist['Email1'])) & (billlist['Balance']<0)] # only families with valid email1
    ebilllist, skiplist=sendemaillogic(ebilllist, **kwargs) # Decides who gets an e-mail
    if 'kcsendtest' in kwargs:
        # Filter bill list and only send to Croat (internal send testing option)
        ebilllist=ebilllist[ebilllist['Family']=='Croat']
        print('Send test to KC only.')
    if 'SMS' in kwargs:
        blankSMS=kwargs.get('SMS','') # get blank alternate SMS message
    for index, billrow in ebilllist.iterrows():
        recipients=getemailadds(billrow) # list of recipients
        # create custom email message
        if detectSMS(recipients) and 'SMS' in kwargs:
            # use alternate SMS message if SMS address indicated
            thismessage=makebillmessage(billrow, Mastersignups, season, year, blankSMS)
        else:
            thismessage=makebillmessage(billrow, Mastersignups, season, year, blankmessage)
        msg=MIMEText(thismessage,'plain')
        msg['Subject'] = emailtitle
        msg['From'] = 'Cabrini Sponsors Club <sfcasponsorsclub@gmail.com>'  
        msg['To']=','.join(recipients)
        if choice=='send': 
            # single message to both parents
            try:
                smtpObj.sendmail('sfcasponsorsclub@gmail.com', recipients, msg.as_string())
                print ('Message sent to ', ','.join(recipients))
            except:
                print('Message to ', ','.join(recipients), ' failed.')
            # append comment when bill is sent to valid email address
            comm=ebilllist.loc[index]['Comments']
            if str(comm)!='nan':
                thiscomm=comm+commstring
            else:
                thiscomm=commstring
            # TODO maybe return billlist (not ebilllist) with comments
            ebilllist=ebilllist.set_value(index,'Comments',thiscomm)
        else: # testing mode
            logfile.write(msg.as_string()+'\n')
            
    # now copy altered ebilllist back to main billlist (with added comment about e-mail sent)
    billlist.loc[ebilllist.index,ebilllist.columns]=ebilllist
    return ebilllist, skiplist

def makebillmessage(thisbillrow, Mastersignups, season, year, blankmessage):
    ''' Make e-mail message for family from billrow (passed as Series)
    pass family's detailed bill row (already contains signups, payments, etc,'''
	
    balance=-thisbillrow.Balance  # int or float (negative means family owes money)  
    # Make current signups string from SUkeys (if applicable)
    SUstring='' 
    tempstr=str(thisbillrow.SUkeys) # signups for this season as string
    if tempstr!='nan' and tempstr!='':
        currSUkeys=[int(s) for s in tempstr.split(',')] # convert str of int(s) to list ofints
    else:
        currSUkeys=[] # no current signups (this season)
    #TODO replace CR-LF ...\r\n didn't seem to work
    if len(currSUkeys)>0:
        SUstring+='Sports signups for this season:\n'
        for i, SU in enumerate(currSUkeys):
            thisSU=Mastersignups[Mastersignups['SUkey']==SU] # returns single row match
            first=thisSU.iloc[0]['First']
            last=thisSU.iloc[0]['Last']
            sport=thisSU.iloc[0]['Sport']
            thisstr=first + ' ' + last + ' - ' + sport + '\n'
            SUstring+=thisstr
        message=blankmessage.replace('$SUSTRING',SUstring)
        # add current season charges
        currcharge=int(thisbillrow.Charges)
        tempstr='Current charges: $'
        tempstr+=str(currcharge)
        message=message.replace('$CURRENT_CHARGES',tempstr)
        # add current payments 
        currpay=int(thisbillrow.CurrPayments)
        tempstr='Payments for ' + season + ' '+ str(int(year))+': $'
        tempstr+=str(currpay)+'\n'
        message=message.replace('$CURRENT_PAYMENTS',tempstr)
    else: # zero out stuff about current charges 
        message=blankmessage.replace('$SUSTRING','')
        message=message.replace('$CURRENT_CHARGES','')
        message=message.replace('$CURRENT_PAYMENTS','')
    # If family has prior charges, insert details here
    # TODO add players to prior fee list? 
    if thisbillrow.PriorCharges>thisbillrow.PriorPayments:
        tempstr='Fees and payments from prior seasons:\n'
        tempstr+=thisbillrow.Feepaydetail+'\n'
        message=message.replace('$FEEPAYDETAIL',tempstr)
    else:
        message=message.replace('$FEEPAYDETAIL','')
    # Now insert outstanding balance for all
    tempstr='$ '+ str(balance)
    message=message.replace('$BALANCE',tempstr)
    # insert section with old uni return, new unis to use, deposits needed or on file
    #TODO mention return of unis for transferred players
    unistring=thisbillrow.Unidetail
    if str(unistring)!='nan':
        message=message.replace('$UNIDETAIL',unistring)
    else:
        message=message.replace('$UNIDETAIL','')
    return message

def shortnamedict(teams):
    ''' From teams list, make shortened name dictionary for tk display (i.e. 1G-Croat or 3G-Ambrose)'''
    teamdict={}
    for index, row in teams.iterrows():
        # Get coach name or school
        if '#' in teams.loc[index]['Team']:
            name=teams.loc[index]['Team'].split('#')[0]
        else:
            name=str(teams.loc[index]['Coach'])
        if teams.loc[index]['Gender']=='m':
            gend='B'
        else:
            gend='G'
        grrange=str(teams.loc[index]['Graderange'])
        grrange=grrange.replace('0','K')
        thisname=grrange+gend+'-'+name
        teamdict.update({teams.loc[index]['Team']:thisname})
    return teamdict

def findrecentfile(filelist):
    ''' Return most recently dated file from list of autonamed files .. date format is always 27Jan17 '''
    dates=[s.split('_')[1].split('.')[0] for s in filelist]
    try:
        dates=[datetime.datetime.strptime(val, "%d%b%y") for val in dates]
        datepos=dates.index(max(dates)) # position of newest date (using max)
        newfile=filelist[datepos]
    except:
        print('File date comparison failed... using first one')
        newfile=filelist[0]
    return newfile

def detectSMS(recipients):
    '''Determine if primary (first) e-mail address is very likely SMS (9 to 10 leading numbers)'''
    if len(recipients)==0:
        return False
    tempstr=recipients[0].split('@')[0]
    SMSmatch=re.match(r'\d{9}', tempstr) 
    if SMSmatch:
        return True
    else:
        return False
