# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 11:30:49 2017

@author: tkc
"""
os.chdir('C:\\Users\\tkc\\Documents\\Python_Scripts\\SC')

resfile='C:\\Users\\tkc\\Documents\\Sponsors_Club\\League Request Template_BBall_2018.xlsx'
stats=pd.read_excel(resfile, sheetname='Results by League')
stats['Level']=''
for index, row in stats.iterrows():
    if row.Grade<5:
        stats=stats.set_value(index,'Level','X')
    else:
        stats=stats.set_value(index,'Level',row.League[2])

# Normalize scoring to grade/gender/level average
grgengroup=stats.groupby(['Gender','Grade','Level'])
for [gen,gr, lev], group in grgengroup:
    avgsc=group['Avg Scrd'].mean()
    avgal=group['Avg Allwed'].mean()
    for index, row in group.iterrows():
        stats=stats.set_value(index,'Avg Scrd', row['Avg Scrd']-avgsc)
        stats=stats.set_value(index,'Avg Allwed', row['Avg Allwed']-avgal)

stats=stats[ (stats['Gender']=='G') & (stats['Grade']==5)]

lggroup=stats.groupby(['League'])


# Pts scored/allowed vs gender/grade/level
grgengroup=stats.groupby(['Gender','Grade','Level'])
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(16,9), squeeze=False)
colorlist=['b','r','g','c','m','y','k', 'olive','pink','purple']
marklist=['o','v','^','<','>','s','p','*','h','+','x','X','D','.']
grnum=0
mylegend=[]
for [gen,gr, lev], group in grgengroup:
    mylegend.append(str(gr)+gen+lev)
    avgsc=group['Avg Scrd'].mean()
    stdsc=group['Avg Scrd'].std()
    avgal=group['Avg Allwed'].mean()
    stdal=group['Avg Allwed'].std()
    plt.errorbar(x=avgsc, y=avgal, xerr=stdsc, yerr=stdal, color=colorlist[grnum%10], marker=marklist[grnum//10])
    grnum+=1

axes[0,0].legend(mylegend, loc='best', fontsize=8)

# Look at PF, PD (differential) by league
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(16,9), squeeze=False)
colorlist=['b','r','g','c','m','y','k', 'olive','pink','purple']
marklist=['.','o','v','^','<','>','s','p','*','h','+','x','X','D']
grnum=0
for key, group in lggroup:
    group.plot.scatter(x='Avg Scrd',y='Avg Allwed', color=colorlist[grnum%10], marker=marklist[grnum//10], ax=axes[0,0])
    grnum+=1


# Results by parish 
lggroup=stats.groupby(['Parish'])

lg.scatt

markers =['s','v','o','x']
for (name, group), marker in zip(lg, cycle(markers)):
    ax.plot(group.x, group.y, marker=marker, linestyle='', ms=12, label=name)
    
# Setting up leagues (weigh past result, geography, coach request)
