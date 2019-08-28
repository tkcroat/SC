# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 11:06:45 2018

@author: tkc
"""
import pandas as pd
import numpy as np
import datetime

def checkuni_duplicates(unilist):
    ''' Check uniform set to see if numbers are unique '''
    grouped=unilist.groupby(['Setname','Size','Number'])
    for [sname, size, num],group in grouped:
        if len(group)>1:
            print(len(group),' unis from', sname, size, num)
    return 



def getuniinfo(teams, unilogfile, Mastersignups, unilist, year):
    '''Readback of uniform numbers, sizes, issue dates from uniform night forms/log 
    and return date after season
    all financial info goes manually into paylog
    '''
    thisyearSU=Mastersignups[Mastersignups['Year']==year]
    # find Cabrini teams from this season needing uniforms
    uniteams=teams[teams['Uniforms']!='N']
    uniteamlist=np.ndarray.tolist(uniteams.Team.unique() )
    # regenerate name of tab in which these are stored (lower case, 3 letter name of sport)
    mycols=['First', 'Last', 'School', 'Issue date', 'Uniform#', 'Size', 'Amount', 
            'Deposit type', 'Deposit date', 'UniReturnDate', '$ returned',
            'Comments', 'Plakey', 'Famkey','Sport']
    alluniplayers=pd.DataFrame(columns=mycols)

    for i,team in enumerate(uniteamlist): # find team's tab and import new uni # info
        match=teams[teams['Team']==team]
        sport=match.iloc[0]['Sport'].lower()
        tabname=sport[0:3]+team[0:3] # must match name when log was generated
        thisteam=pd.read_excel(unilogfile, sheetname=tabname)
        thisteam['Sport']=sport # add associated sport needed to match signup
        alluniplayers=pd.concat([alluniplayers,thisteam], ignore_index=True) 
    # remove entries with nan in uniform number (no info) .. will be a number or 'xx'
    # nan here should mean uniform not issued (unreported drop)
    alluniplayers=alluniplayers.dropna(subset=['Uniform#'])
    nonum==alluniplayers[pd.isnull(alluniplayers['Uniform#'])]
    # TODO replace loop with merge --> then inspect each row
    uniinfo=pd.merge(alluniplayers, thisyearSU, how='left', on=['Sport','Plakey'], 
             suffixes=('','_2'))
    mycols=['First', 'Last', 'Uniform#', 'Uniform#_2','Size', 'Issue date', 'School',  'Amount',
       'Deposit type', 'Deposit date', 'UniReturnDate', '$ returned',
       'Comments', 'Plakey', 'Famkey', 'Sport', 'SUkey', 
       'Grade', 'Gender', 'Year', 'Team', 'SUdate',
       'Issue date_2', 'UniReturnDate_2']
    uniinfo=uniinfo[mycols]
    # now update the associated signups in mastersignups
    for index, row in alluniplayers.iterrows():
        pd.merge(row.to_frame(), thisyearSU, how='left', on=['Plakey','Sport'], suffixes=('','_2'))
        
        plakey=int(alluniplayers.loc[index]['Plakey'])
        sport=alluniplayers.loc[index]['Sport']
        # match plakey and sport  and find associated index (year already filtered)
        thisplay=thisyearSU[thisyearSU['Plakey']==plakey]
        mask=thisplay['Sport'].str.contains(sport, case=False)
        match=thisplay.loc[mask]
        try:
            number=int(alluniplayers.loc[index]['Uniform#'])
            size=alluniplayers.loc[index]['Size']
        except: # could be 'xx' if uniform definitely issued but number unknown
            number=alluniplayers.loc[index]['Uniform#']
            size=alluniplayers.loc[index]['Size']
        issuedate=alluniplayers.loc[index]['Issue date']
        if type(issuedate)==datetime.datetime:    
            issuedate=datetime.date.strftime(issuedate,'%m/%d/%Y')
        returndate=alluniplayers.loc[index]['UniReturnDate']
        if type(returndate)==datetime.datetime:    
            returndate=datetime.date.strftime(issuedate,'%m/%d/%Y')
        # Now write Uniform#, issue date and return date from log
        if len(match==1): # match is between alluni and mastersignups
            # compare numbers if uni # not np.nan or '??'
            if str(match.iloc[0]['Uniform#'])!='nan' and str(match.iloc[0]['Uniform#'])!='??':
                if match.iloc[0]['Uniform#']!=str(number):
                    print('Player', match.iloc[0]['First'], match.iloc[0]['Last'],' assigned uni#', 
                          match.iloc[0]['Uniform#'],' or', str(number))
                    # Interactive conflict resolution??
                else: # assign new number, size, date, etc. 
                    # match.index is original row in Mastersignups
                    Mastersignups=Mastersignups.set_value(match.index,'Uniform#',number)
                    Mastersignups=Mastersignups.set_value(match.index,'Size', size)
                    Mastersignups=Mastersignups.set_value(match.index,'Issue date',issuedate)
                    Mastersignups=Mastersignups.set_value(match.index,'UniReturnDate',returndate)
        else:
            print('Error: Matching signup not found for player key and sport:', plakey, sport)
    return Mastersignups


def makemissingunilog(df, paylog, players, fname='missingunilist.csv'):
    '''Pass master signups and find unreturned uniforms... return as long single lists'''
    df=df.dropna(subset=['Issue date']) # only signups with uniform issued
    df=df.loc[pd.isnull(df['UniReturnDate'])] # keeps only unreturned uniforms
    df['Amount']=''
    df['Deposit type']=''
    df['Deposit date']=''
    df['Deposit date']=pd.to_datetime(df['Deposit date'], format='%d%b%Y:%H:%M:%S.%f', errors='ignore') # force this to datetime format first
    df['Comments']=''
    df['$ returned']='' # this field always blank in uni-logs.. 
    # get families with outstanding uniforms
    famlist=np.ndarray.tolist(df.Famkey.unique()) # deal with family's deposits and unis simultaneously
    paylog=paylog.sort_values(['Date'], ascending=True) # chronological so deposit check works correctly
    for i, famkey in enumerate(famlist): # now find associated deposits from family
        unis=df[df['Famkey']==famkey] # this family's outstanding uniforms
        depmatch=paylog[paylog['Famkey']==famkey]
        depmatch=depmatch.dropna(subset=['Deposit']) # drop payments w/o associated deposits
        # find last negative value and take the positive deposits after that
        for j in range(len(depmatch)-1,-1,-1): # backwards through the rows
            if depmatch.iloc[j]['Deposit']<0: # stop at negative value
                depmatch=depmatch.drop(depmatch.index[0:j+1]) # drops negative row and all preceding it
                break
        if len(depmatch)==0: # fully handle no deposits case (no entries or last entry negative for returned deposit)
            unis['Comments']='No deposit on file'
            unis['Amount']=0            
        # if any deposits exist, just spread total amt over all outstanding uniforms (even if inadequate)
        else:
            unis['Deposit date']=depmatch.iloc[0]['Date'] # date of oldest deposit if multiple
            unis['Comments']=depmatch.iloc[0]['Depcomment'] # may miss 2nd comment in rare case of multiple
            unis['Amount']=depmatch.Deposit.sum()/len(unis) # split amount across all uniforms
        # check to ensure not deposits are not of different type (i.e. all cash or all check)
            if len(depmatch.Deptype.unique())==1: # all same type    
                unis['Deposit type']=depmatch.iloc[0]['Deptype'] # generally cash or check
            else:
                unis['Deposit type']='mixed' # oddball case of some cash/ some check
        df.loc[unis.index,unis.columns]=unis # Copy altered subset back to main df
        
    # this is probably sufficient for uniform log... if further info needed can just check paylog directly
    for index,row in df.iterrows(): # get school for each player with issued uniform
        plakey=df.loc[index]['Plakey']
        match=players[players['Plakey']==plakey]
        if len(match)!=1:
            print('Error locating school for player ', plakey)
        else:
            df=df.set_value(index,'School',match.iloc[0]['School'])
    # organize output from this file
    mycols=['First', 'Last', 'Gender', 'Grade','School', 'Issue date', 'Sport','Year', 
            'Uniform#', 'Team', 'Amount', 'Deposit type', 'Deposit date', 
            'UniReturnDate', '$ returned', 'Comments', 'Plakey', 'Famkey'] 
    df=df[mycols] 
    df=df.sort_values(['Last'])
    df.to_csv(fname, index=False, date_format='%m-%d-%y')
    return df

def writeuniformlog(df, teams, players, season, year, paylog):
    ''' From mastersignups and teams, output contact lists for all teams/all sports separately into separate tabs of xls file
    autosaves to "Fall2016"_uniform_log.xls'''
    # Slice by sport: Basketball (null for winter?), Soccer, Volleyball, Baseball, T-ball, Softball, Track) 
    # Load missing uniforms 
    missing=df.dropna(subset=['Issue date']) # only signups with uniform issued
    missing=missing.loc[pd.isnull(missing['UniReturnDate'])] # keeps only unreturned uniforms
    # Groupby plakey and sport for missing unis
    
    df=df[df['Year']==year] # remove prior years in case of duplicate name
    df=df.reset_index(drop=True)
    # get school from players.csv
    df=pd.merge(df, players, how='left', on=['Plakey'], suffixes=('','_r'))
    # Find Cabrini teams from this season needing uniforms
    thismask = teams['Uniforms'].str.contains('y', case=False, na=False)
    uniformteams=teams.loc[ teams['Uniforms']!='N']
    uniformlist= uniformteams.Team.unique() 
    uniformlist=np.ndarray.tolist(uniformlist)
    # single uniform log per season 
    contactfile=str(season)+'_'+str(year)+'_uniform_log.xlsx'
    writer=pd.ExcelWriter(contactfile, engine='openpyxl',date_format='mm/dd/yy')
    # Can just eliminate any entries not in uniform deposit list
    df=df[df['Team'].isin(uniformlist)] # only players on teams needing uniforms
    # Columns needed for log output
    mycols=['First', 'Last', 'School', 'Issue date', 'Uniform#', 'Size', 'Amount', 
            'Deposit type', 'Deposit date', 'UniReturnDate', '$ returned', 
            'Comments', 'Plakey', 'Famkey'] 
    tabnamelist=[]

    for i, team in enumerate(uniformlist):
        thismask = df['Team'].str.contains(team, case=False, na=False)
        thisteam=df.loc[thismask] # this team's signups
        sport=thisteam.iloc[0]['Sport'].lower()
        thisteam=finddeposits(thisteam, paylog) # thisteam is this team's slice of info from master_signups
        thisteam=thisteam[mycols] # organize in correct format for xls file
        tabname=sport[0:3]+team[0:3] # name tab with team's name..
        if tabname in tabnamelist:
            tabname+='2' # handles two teams per grade
        tabnamelist.append(tabname)
        thisteam.to_excel(writer,sheet_name=tabname,index=False) # this overwrites existing file
    writer.save()
    return

def finddeposits(df, paylog):
    ''' Pass a single team and look up most recent uniform deposit ... 
    if positive we have deposit on file and copy this to uniform log '''
    # find matching family in paylog
    # add columns pertaining to financials of deposits (pulled from paylog)
    df['Amount']=''
    df['Deposit type']=''
    df['Deposit date']=''
    df['Comments']=''
    df['$ returned']='' # this field always blank in uni-logs.. 
    # pen entries for money returned go into paylog as negative numbers in deposit field
    for index,row in df.iterrows():
        famkey=df.loc[index]['Famkey']
        last=df.loc[index]['Last']
        match=paylog[paylog['Famkey']==famkey]
        # Knock out entries without deposits (int or float)... doesn't get nans?
        match=match.dropna(subset=['Deposit']) # drop those w/o values
        # require int or float (probably shouldn't happen)
        match=match[match['Deposit'].apply(lambda x: isinstance(x, (int, np.int64, float)))]
        if len(match)==0:        
            print('No deposit for player ', last)
            df=df.set_value(index,'Comments','No deposit on file')
            continue
        elif match.iloc[-1]['Deposit']>0: # gets last matching value (if positive then not a deposit return)
            df=df.set_value(index,'Deposit date',match.iloc[-1]['Date'])
            df=df.set_value(index,'Amount',match.iloc[-1]['Deposit'])
            df=df.set_value(index,'Deposit type',match.iloc[-1]['Deptype'])
            df=df.set_value(index,'Comments',match.iloc[-1]['Depcomment'])
            print('$', match.iloc[-1]['Deposit'],' for player ',last)   
        else: # last deposit entry is negative (returned deposit) so none on file
            print('Last deposit returned for player ', last)
            # formatting of return date
            retdate=match.iloc[-1]['Date']
            commstr='$'+str(match.iloc[-1]['Deposit'])+' returned on ', retdate
            df=df.set_value(index,'Comments',commstr)
    return df

def updateunisumm(unisumm, unilist):
    ''' Using info in unilist update the excel summary sheet
    unilist is master for this, summary is just an updatable view
    '''
    # First compare overall numbers 
    unisets=np.ndarray.tolist(unisumm.Setname.unique())
    # Drop nan, ensure compatible names
    unisets=[i for i in unisets if str(i)!='nan']
    unisets2=np.ndarray.tolist(unilist.Setname.unique())
    miss=[i for i in unisets if i not in unisets2]
    if miss:
        print('Uniform set(s) missing:', ",".join(miss))
    miss2=[i for i in unisets2 if i not in unisets]
    if miss2:
        print('Uniform set(s) missing:', ",".join(miss2))

    # Compare total counts        
    for i, val in enumerate(unisets):
        match=unisumm[unisumm['Setname']==val]
        match2=unilist[unilist['Setname']==val] # holds number of unis
        if match.iloc[0]['Total']!=len(match2):
            print('Totals discrepancy for ', val)
            unisumm=unisumm.set_value(match.index[0],'Total',len(match2))
        # Now go over these as function of size
        sizes=['YM','YL','YXL', 'S','M','L','XL','2XL']
        # testing size=sizes[2]
        for i, size in enumerate(sizes):
            thissize=match2[match2['Size']==size]
            if match.iloc[0][size+'total']!=len(thissize):
                print('Size discrepancy for ', val, size)
                unisumm=unisumm.set_value(match.index[0],size+'total',len(thissize))
            # now groupby in/out/miss and update summary
            status=['in','out','miss'] # in closet, out to player or missing/unassigned
            # testing stat=status[0]
            for i, stat in enumerate(status):
                thisstat=thissize[thissize['Location']==stat]
                if match.iloc[0][size+stat]!=len(thisstat):
                    print('Size discrepancy for ', val, size, stat)
                    unisumm=unisumm.set_value(match.index[0],size+stat,len(thisstat))
    # Now update totals by type
    unisumm['Total in']=unisumm['YMin']+unisumm['YLin']+unisumm['YXLin']+unisumm['Sin']+unisumm['Min']+unisumm['Lin']+unisumm['XLin']+unisumm['2XLin']
    unisumm['Total out']=unisumm['YMout']+unisumm['YLout']+unisumm['YXLout']+unisumm['Sout']+unisumm['Mout']+unisumm['Lout']+unisumm['XLout']+unisumm['2XLout']
    unisumm['Total miss']=unisumm['YMmiss']+unisumm['YLmiss']+unisumm['YXLmiss']+unisumm['Smiss']+unisumm['Mmiss']+unisumm['Lmiss']+unisumm['XLmiss']+unisumm['2XLmiss']
    return unisumm

def transferunis(df, season, year):
    ''' Transfer unreturned uniform from last season to next season's signup if never returned (using mastersignups)'''
    sportsdict={'Fall':['VB','Soccer'], 'Winter':['Basketball'],'Spring':['Track','Softball','Baseball','T-ball']}
    sportlist=sportsdict.get(season)
    # Current signups with uniform not yet assigned
    currentSU=df[(df['Sport'].isin(sportlist)) & (df['Year']==year) & (pd.isnull(df['Issue date']))]
    # Previously issued, unreturned uniforms from this sport-season
    priorSU=df[(df['Sport'].isin(sportlist)) & (df['Year']==year-1) & (pd.notnull(df['Issue date'])) & (pd.isnull(df['UniReturnDate']))]
    # Find player-sport combos in both currentSU and priorSU (unreturned uni);
    tranunis=pd.merge(priorSU, currentSU, how='inner', on=['Plakey','Sport'], suffixes=('','_2'))
    thisdate=datetime.datetime.strftime(datetime.datetime.now(), '%m/%d/%y')
    for index, row in tranunis.iterrows():
        old=df[df['SUkey']==tranunis.loc[index]['SUkey']]
        new=df[df['SUkey']==tranunis.loc[index]['SUkey_2']]
        if len(old)==1 and len(new)==1:
            oldind=old.index[0]
            newind=new.index[0]
            # copy old uni info over to new signup
            df=df.set_value(newind, 'Issue date', df.loc[oldind]['Issue date'])
            df=df.set_value(newind, 'Uniform#', df.loc[oldind]['Uniform#'])
            # Mark old signup as effectively having uniform returned
            df=df.set_value(oldind, 'UniReturnDate', thisdate)
            print('Uni info transferred for', tranunis.loc[index]['First'],tranunis.loc[index]['Last'], tranunis.loc[index]['Sport'])
        else:
            print('Problem transferring uni info for', tranunis.loc[index]['First'],tranunis.loc[index]['Last'])
    return df

def transferunisVBBB(df, year):
    ''' Transfer VB uniforms over to basketball in same year for common players'''
    # Current signups with uniform not yet assigned
    currseas=df[(df['Sport'].isin(['Basketball'])) & (df['Year']==year) & (pd.isnull(df['Issue date']))]
    # Previously issued, unreturned uniforms from this sport-season
    priorseas=df[(df['Sport'].isin(['VB'])) & (df['Year']==year) & (pd.notnull(df['Issue date'])) & (pd.isnull(df['UniReturnDate']))]
    # Find player-sport combos in both currentSU and priorSU (unreturned uni);
    tranunis=pd.merge(priorseas, currseas, how='inner', on=['Plakey'], suffixes=('','_2'))
    thisdate='01/01/'+str(year) # use artificial date of 1/1 for return/reissue
    for index, row in tranunis.iterrows():
        old=df[df['SUkey']==row.SUkey]
        new=df[df['SUkey']==row.SUkey_2]
        if len(old)==1 and len(new)==1:
            oldind=old.index[0]
            newind=new.index[0]
            # copy old uni info over to new signup
            df=df.set_value(newind, 'Issue date', thisdate) # use artificial 1/1 date
            df=df.set_value(newind, 'Uniform#', df.loc[oldind]['Uniform#'])
            # Mark old signup as effectively having uniform returned
            df=df.set_value(oldind, 'UniReturnDate', thisdate)
            print('Uni info transferred for', tranunis.loc[index]['First'],tranunis.loc[index]['Last'], tranunis.loc[index]['Sport'])
        else:
            print('Problem transferring uni info for', tranunis.loc[index]['First'],tranunis.loc[index]['Last'])
    return df
