# -*- coding: utf-8 -*-
"""
SC maintenance main/workflow ... assorted functions that are run annually or thereabouts
Created on Wed Aug 23 09:14:51 2017

@author: tkc
"""


# Run these occasionally to possibly clean up underlying data
# Update grades based on school year and gradeadj (run at beginning of school year)
players=SC.graduate_players(players, year)
players.to_csv('private\\players.csv',index=False)

# Updates grade adjustment based on current grade (which must be correct) and DOB (constant)
players=updategradeadjust(players, year)

# Remove high school kids
players=SC.removeHSkids(players)
players.to_csv('private\\players.csv',index=False)

# remove families w/ no associated players (e.g. graduated)
famcontact=SC.removeEmptyFams(players, famcontact)

test=Mastersignups[pd.isnull(Mastersignups['SUkey'])]

players=SC.formatnamesnumbers(players) # format phone numbers, names to title case, standardize schools, etc.

comparefamkeys(players,famcontact) # checks for consistency in family names/keys between main lists

# TODO   removedeadfamilies function
# Update family contact w/ associated players 