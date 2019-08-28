# -*- coding: utf-8 -*-
"""
Created on Wed May 10 08:58:05 2017
Implementation of database model (players, families) using SQLAlchemy 
@author: tkc
"""
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
# new base class.. triggers creation of Table and mapper 
# accessible using class.__table__ and class.__mapper__
Base = declarative_base()
 
class Player(Base):
    # definition of player table
    __tablename__ = 'player'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    plakey = Column(Integer, primary_key=True)
    first = Column(String(250), nullable=False)
    last = Column(String(250), nullable=False)
    alias = Column(String(250), nullable=False) # alt first name
    family = Column(String(250), nullable=False) # family name (necessary?)
    DOB = Column(String(250))
    gender = Column(String(250))
    school = Column(String(250))
    grade= Column(Integer) # K=0 
    gradeadj= Column(Integer) # ahead or behind of expected grade
    uninum = Column(Integer) # Tshirt uniform
    famkey = Column(Integer, ForeignKey('family.famkey'))    
 
class Family(Base):
    __tablename__ = 'family'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    famkey = Column(Integer, primary_key=True)
    family = Column(String(250), nullable=False)
    address = Column(String(250)) # number and name as string
    city = Column(String(250))
    state = Column(String(250))
    post_code = Column(String(250), nullable=False)
    parish_registration = Column(String(250))
    parish_residence = Column(String(250))
    pfirst1 = Column(String(250), nullable=False)
    plast1 = Column(String(250), nullable=False)
    pfirst2 = Column(String(250), nullable=False)
    plast2 = Column(String(250), nullable=False)
    pfirst3 = Column(String(250), nullable=False)
    plast3 = Column(String(250), nullable=False)

    # How to associate multiple players w/ family 
    player = relationship(Player)
    
# Create engine to store above declarative data definitions
engine = create_engine('sqlite:///SC_sqlalchemy.db')

