# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 09:43:09 2017

@author: tkc
"""
import pandas as pd
import smtplib
import numpy as np
import datetime
import tkinter as tk
import glob
import sys
import textwrap
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
if 'C:\\Users\\tkc\\Documents\\Python_Scripts\\SC' not in sys.path:
    sys.path.append('C:\\Users\\tkc\\Documents\\Python_Scripts\\SC')
from SC_signup_functions import findcards
import math
#%%

emailparent_tk(teams, signupfile, year)
    

# 8/11/17  updating interactive approval of family contact changes
# not sure about status
    
def updatefamcon_tk(row, famcontact, **upkwargs):
    ''' Interactive approval of family contact changes
    changes directly made to famcontacts (but not yet autosaved)
    upkwargs: phone, email, address
    '''    
    root = tk.Tk()
    root.title('Update family contact info')
    choice=tk.StringVar() # must be define outside of event called functions
    rownum=0
    mytxt='Family: '+row.Family+' # '+str(row.Plakey)
    tk.Label(root, text=mytxt).grid(row=rownum, column=0)
    rownum+=1
    # Use listbox of common schools?
    if 'parlist' in upkwargs: # indicates new parent found
        parlist=upkwargs.get('parlist',[])
        p=tk.Listbox(master=root, listvariable=parlist)
        
        # create and display DOB variables
        def add1(event):
            DOB.set(datetime.datetime.strftime(DOB1,'%m/%d/%y'))
        def add2(event):
            DOB.set(datetime.datetime.strftime(DOB2,'%m/%d/%y'))  
        DOB=tk.StringVar()
        DOB.set(datetime.datetime.strftime(DOB1,'%m/%d/%y')) # defaults to original
        tk.Label(root, text='Update date of birth?').grid(row=rownum, column=0)
        mytxt='current DOB:'+datetime.datetime.strftime(DOB1,'%m/%d/%y')
        b=tk.Button(master=root, text=mytxt)
        b.bind('<Button-1>', ChooseDOB1)
        b.grid(row=rownum, column=1)
        mytxt='New DOB:'+datetime.datetime.strftime(DOB2,'%m/%d/%y')
        b=tk.Button(master=root, text=mytxt)
        b.bind('<Button-1>', ChooseDOB2)
        b.grid(row=rownum, column=2)            
        tk.Entry(master=root, textvariable=DOB).grid(row=rownum, column=3)
        rownum+=1
    if 'school' in upkwargs:
        school=tk.StringVar()
        school.set(row.School) # default to existing value
        tk.Label(root, text='Update school?').grid(row=rownum, column=0)
        rownum+=1
        def newschool(event):
            school.set(row.School_n)
        def oldschool(event):
            school.set(row.School)
        def pickschool(event):
            # double-click to pick standard school choice
            items=lb.curselection()[0] # gets selected position in list
            school.set(commonschools[items])
        tk.Entry(root, textvariable=school).grid(row=rownum, column=2)
        mytxt='new school:'+str(row.School_n)
        b=tk.Button(master=root, text=mytxt)
        b.bind('<Button-1>', newschool)
        b.grid(row=rownum, column=1)
        mytxt='existing school:'+str(row.School)
        b=tk.Button(master=root, text=mytxt)
        b.bind('<Button-1>', oldschool)
        b.grid(row=rownum, column=0)
        # also include selectable listbox of common school choices
        lb=tk.Listbox(master=root, selectmode=tk.SINGLE)
        lb.bind("<Double-Button-1>", pickschool)
        lb.grid(row=rownum, column=3)
        for i,sch in enumerate(commonschools):
            lb.insert(tk.END, sch)
        rownum+=1
    # Now set up select/close buttons
    def skip(event):
        choice.set('skip')        
        root.destroy()        
    def change(event):
        choice.set('change')        
        root.destroy() 
    
    f=tk.Button(root, text='Skip')
    f.bind('<Button-1>', skip)
    f.grid(row=rownum, column=0)
    g=tk.Button(root, text='Change')
    g.bind('<Button-1>', change)
    g.grid(row=rownum, column=1)
    root.mainloop()
    
    mychoice=choice.get()
    if mychoice=='change':
        # Find matching row for family (needed for all changes below)
        famkey=row.Famkey
        match=famcontact[famcontact['Famkey']==famkey]
        if len(match)==0:
            thisind=match.index[0]
        else: 
            print('Problem finding unique entry for famkey', str(famkey))
            return famcontact # return unaltered
        
        # Direct update of parent list
        parlist=parlist[0:3] # limit to 3 entries
        while len(parlist)<3:
            parlist.append([np.nan,np.nan]) # pad with nan entries if necessary 
        # now reset parent name entries
        for i in range(1,4): # reset 3 existing parents entries
            fname='Pfirst'+str(i)
            lname='Plast'+str(i)
            ser=ser.set_value(fname,parlist[i-1][0])
            ser=ser.set_value(lname,parlist[i-1][1])

        try:
            # make changes directly to players after finding correct index using plakey
            plakey=row.Plakey
            match=players[players['Plakey']==plakey]
            thisind=match.index[0]
            if 'school' in upkwargs:
                players=players.set_value(thisind,'School',school.get())
            if 'DOB' in upkwargs:
                newDOB=datetime.datetime.strptime(DOB.get(),'%m/%d/%y')
                players=players.set_value(thisind,'DOB',newDOB)
        except:
            print('Error updating info for', row.Plakey, row.First, row.Last)
    return famcontact

def update_contact(ser, famcontact):
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
    if str(ser.Phone1_n)!='nan' and [ser.Phone1_n,ser.Text1_n] not in phonelist: # new ones phone is required entry
        if [ser.Phone1_n, np.nan] in phonelist: # remove if # present but w/o text indication
            phonelist.remove([ser.Phone1_n,np.nan])
            phonelist.insert(0,[ser.Phone1_n,ser.Text1_n]) # insert in first position
        else:
            upkwargs.update({'phone1':[ser.Phone1_n,ser.Text1_n]})
    else: # move this pair to first position in existing list (already in list)
        phonelist.insert(0,phonelist.pop(phonelist.index([ser.Phone1_n,ser.Text1_n])))
        # Inserts desired primary in first position while simultaneously removing other entry
    if str(ser.Phone2_n)!='nan': # check for phone2 entry (with _n suffix)
        if [ser.Phone2_n,ser.Text2_n] not in phonelist: # add second phone to 2nd position if not present
            if [ser.Phone2_n,np.nan] in phonelist: # remove if # present but w/o text indication
                phonelist.remove([ser.Phone2_n,np.nan]) 
                phonelist.insert(1,[ser.Phone2_n,ser.Text2_n])
                print ('Added phone ', str(ser.Phone2_n), 'for family', thisfam)
            else: # get approval for phone 2 addition
                upkwargs.update({'phone2':[ser.Phone2_n,ser.Text2_n]})
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
            emaillist.insert(0,emaillist.pop(emaillist.index(ser.Email)))
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
    if [ser.Pfirst1_n,ser.Plast1_n] not in parlist: # phone 1 is required entry
        upkwargs.update('newpar1':[ser.Pfirst1_n,ser.Plast1_n])
        upkwargs.update('parlist':parlist)
        parlist.insert(0,[ser.Pfirst1_n, ser.Plast1_n]) # insert in first position
        print ('added parent', ser.Pfirst1_n, ser.Plast1_n, 'for family', thisfam)        
    else: # move this pair to first position in existing list
        parlist.insert(0,parlist.pop(parlist.index([ser.Pfirst1_n,ser.Plast1_n])))
        # inserts in first position while simultaneously removing other entry
    if str(ser.Pfirst2_n!='nan'): # Check for parent 2 entry
        if [ser.Pfirst2_n,ser.Plast2_n] not in parlist: # add second phone to 2nd position if not present
            upkwargs.update('newpar2':[ser.Pfirst2_n,ser.Plast2_n])
            upkwargs.update('parlist':parlist)
            parlist.insert(1,[ser.Pfirst2_n,ser.Plast2_n])
    # now run interactive approval if necessary 
    if len(upkwargs)>0: # something needs interactive approval            
        if 'phone1' in upkwargs or 'phone2' in upkwargs:
            upkwargs.update({'phonelist':phonelist}) # add phonelist after any alterations
    # TODO need to be careful about incorporating both auto-approved and tk approved changes 
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
    
    # update parish of registration (if new gd entry and no existing entry)
    # otherwise changes are skipped to keep parish names consistent
    if str(ser.Parish_registration)=='nan' and str(ser.Parish)!='nan':
        ser.Parish_registration=ser.Parish # Set parish of registration
    return ser
            

# TODO separate e-mail recruits script... hasn't this been done already     
    for in
    Recruits=Recruits[pd.notnull(Recruits['Email1'])]
    Recs=Recruits.groupby(['First','Last'])
    for pla, rows in Recs:
        recipients=getemailadds(rows.iloc[0]) # list of recipients
        first=rows.iloc[0]['First']
        thistitle=emailtitle.replace('$FIRST', first)
        # create custom email message (can have multiple sports in df)
        thismess=makerecmessage(rows, recipients, thistitle, messagefile)
        thismess=thismess.encode('utf-8')
        for i,addr in enumerate(recipients): # Send message to each in list
            try:
                smtpObj.sendmail('sfcasponsorsclub@gmail.com', addr, thismess)
                print ('Message sent to ', addr)
            except:
                print('Message to ', addr, ' failed.')
    return

