# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 16:42:40 2019

@author: kevin
"""

crtStmt=tkcreateTable(Mastersignups)
# Create statement for players table 
stmt =''' CREATE TABLE players (
    Plakey FLOAT NOT NULL,
    First VARCHAR NOT NULL,
    Last VARCHAR NOT NULL,
    DOB VARCHAR NOT NULL,
    Gender VARCHAR NOT NULL,
    School VARCHAR NOT NULL,
    Grade int32 NOT NULL,
    Gradeadj FLOAT,
    Uni# FLOAT,
    Famkey FLOAT NOT NULL,
    Family VARCHAR,
    Alias VARCHAR,
    PRIMARY KEY (Plakey),
    FOREIGN KEY (Plakey)
        REFERENCES mastersignups (Plakey),
    FOREIGN KEY (Famkey)
        REFERENCES families (Famkey),
); '''
# Creation of families table
stmt='''CREATE TABLE families (
    Famkey INT NOT NULL,
    Family VARCHAR NOT NULL,
    Address VARCHAR NOT NULL,
    City VARCHAR NOT NULL,
    State VARCHAR NOT NULL,
    Zip VARCHAR NOT NULL,
    Parish_registration VARCHAR,
    Parish_residence VARCHAR,
    Pfirst1 VARCHAR,
    Plast1 VARCHAR,
    Pfirst2 VARCHAR,
    Plast2 VARCHAR,
    Pfirst3 VARCHAR,
    Plast3 VARCHAR,
    Playerlist FLOAT NOT NULL,
    Phone1 VARCHAR NOT NULL,
    Text1 VARCHAR,
    Phone2 VARCHAR,
    Text2 VARCHAR,
    Phone3 VARCHAR,
    Text3 VARCHAR,
    Phone4 VARCHAR,
    Text4 FLOAT,
    Email1 VARCHAR,
    Email2 VARCHAR,
    Email3 VARCHAR,
PRIMARY KEY (Famkey),
);'''
# Create mastersignups table
stmt='''CREATE TABLE mastersignups (
    SUkey FLOAT NOT NULL,
    First VARCHAR NOT NULL,
    Last VARCHAR NOT NULL,
    Grade INT NOT NULL,
    Gender VARCHAR NOT NULL,
    Sport VARCHAR NOT NULL,
    Year VARCHAR NOT NULL,
    Team VARCHAR,
    Plakey FLOAT NOT NULL,
    Famkey FLOAT NOT NULL,
    Family VARCHAR,
    SUdate VARCHAR NOT NULL,
    Issue date VARCHAR,
    Uniform# VARCHAR,
    UniReturnDate VARCHAR,
PRIMARY KEY (SUkey),
FOREIGN KEY (Plakey)
    REFERENCES players (Plakey),
FOREIGN KEY (Famkey)
    REFERENCES families (Famkey),
);'''
# Create teams table
stmt='''CREATE TABLE teams (
    Teamkey INT NOT NULL,
    Year INT NOT NULL,
    Sport VARCHAR NOT NULL,
    Grade VARCHAR NOT NULL,
    Gender VARCHAR NOT NULL,
    Division VARCHAR NOT NULL,
    Level VARCHAR,
    Team VARCHAR NOT NULL,
    Coach ID VARCHAR NOT NULL,
    Coach VARCHAR,
    Graderange int32 NOT NULL,
    AssistantIDs VARCHAR,
    Uniforms VARCHAR NOT NULL,
    Number FLOAT,
    Lower FLOAT,
    Upper FLOAT,
    Playerlist VARCHAR,
    Location VARCHAR,
    Slot VARCHAR,
PRIMARY KEY (Teamkey),
FOREIGN KEY (Coach ID)
    REFERENCES coaches (Coach ID),
);'''
# Create coaches table
stmt='''CREATE TABLE coaches (
    Fname VARCHAR NOT NULL,
    Lname VARCHAR NOT NULL,
    Street VARCHAR NOT NULL,
    City VARCHAR NOT NULL,
    State VARCHAR NOT NULL,
    Zip INT NOT NULL,
    Phone VARCHAR NOT NULL,
    Email VARCHAR NOT NULL,
    Sex VARCHAR NOT NULL,
    School VARCHAR NOT NULL,
    Parish of Registration VARCHAR NOT NULL,
    Parish of Residence VARCHAR NOT NULL,
    Coach ID VARCHAR NOT NULL,
PRIMARY KEY (Coach ID),
);'''