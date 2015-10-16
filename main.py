#! /usr/bin/python
# -*- coding: utf-8 -*-
##############################################
### Import definitions                    ####
##############################################
### Python Default modules ###################
from sys import argv,exit
import os
from datetime import datetime

## Beatiful soup import
from bs4 import BeautifulSoup,SoupStrainer

## For opening urls (better than urllib2)
from urlgrabber import urlread

### Regular expressions
import re

### SQL ORM
from sqlobject import *

### ComicBook classes ########################
from ComicBook import *
from BeautifulSoup import ResultSet

##############################################
### Global values                         ####
##############################################
authors_list = ("Editor-in-chief","Cover Artists","Writers","Pencilers","Inkers","Colourists","Letterers","Editors")
                
                

##############################################
### Compiled regex                        ####
## TODO : Move to own regexp              ####
##############################################
""" This regular expression parses the title.
^                   => Begining of string
\s                  => Spaces and co.
\d                  => Number
.                   => Any Character
(?P<name>sub-regex) => matches of the sub regular expression can be
                        accessed throug match.group("name")
.                   => Any character
$                   => End of the string
See https://docs.python.org/2/library/re.html
"""
title_re  = re.compile("^\s*(?P<order_n>\d+)\s*:\s*(?P<title>.+)\s*\#(?P<number>\d+)(?P<part>\w?)\s*\(v(?P<vol_n>\d+)\)\s*$")

""" This regular expression parses a value key par 
    It counts to match greedily the groups .+
"""
key_value_re = re.compile("^\s*(.+)\s*:\s*\n*\s*(.+)\s*$")

##############################################
### Defined methods                       ####
##############################################
def get_comic_title (main_table_item):
    """ Get the info in the comic title from the html main_table  returns a tuple containing: 
        Title  => Title of the comic book serie
        number => Number of the comic book in current Volume
        part   => Part inside the comic book (For comic books with 2 or 3 different stories
        volume => Volume of the comic book title
        order  => Number in reading order (optional)
    """
    
    ## Define an empty dictionary
    comic_kwargs = {}
    
    ## Title is the only h1 tag within the main table html
    comic_title_tags = main_table_item.select("h1")
    
    ## If we found  an h1 on the html
    if (comic_title_tags) :
        
        ## Parse the whole text with a regular expresion
        match = title_re.match(comic_title_tags[0].get_text())

        ## Check if there was a match or not
        if ( not match):
            print "No match for title found in %s" % (comic_title_tags[0].get_text())
            return None
        
        ## Process the match and create the dict for initializating the comic book  
        comic_kwargs['comicTitle']  = match.group("title")
        comic_kwargs['issue']       = int(match.group("number"))
        comic_kwargs['part']        = match.group("part")
        comic_kwargs['volume']      = int(match.group("vol_n"))
        comic_kwargs['orderNumber'] = int(match.group("order_n"))
        
        ### Return the dict
        return comic_kwargs
    
    else:
        print "No h1 found on following table html %s" % (main_table_item)
        return None

def comic2string (comic_kwargs):
    """ Take comic kwargs and convert it to a nice string for reporting """
    string_out = comic_kwargs['comicTitle'] + " " + str(comic_kwargs['issue'])
    string_out += "#"+comic_kwargs['part']+" (v"+ str(comic_kwargs['volume']) + ")"
    return string_out

def get_comic_story (story_table_item):
    """ Get story description from main table """
    
    ## Define an empty dictionary
    comic_kwargs = {}
        
    try:
        story_name_tags = story_table_item.td.div
    except Exception as e:
        print e
        print "Error : False story table item \n %s" % (story_table_item)
        return
            
    ## If found add history
    if (story_name_tags):
        comic_kwargs['storyName'] = story_name_tags.get_text().replace('"','').strip()
        
    return comic_kwargs

def get_comic_details (details_table_item):
    """ Get comic details from main table """
    ## Define an empty dictionary
    details_dict = {}
    
    ## Check for TDs on the tr, the second one is the one with the tr
    details_td = details_table_item.find_all("td", recursive=False)
    
    try:
        details_table = details_td[1].table
        details_items = details_table.find_all("td")
    except Exception as e:
        print e
        print "Error : False details section selected \n %s" %(details_table_item)
        return
    
    for detail in (details_items) :
        detail_match = key_value_re.match(detail.get_text())
        if (detail_match):
            details_dict[detail_match.group(1)] = detail_match.group(2)
        
    return details_dict

def get_comic_synopsys (story_table_item):
    """ Get story synopsys from main table """
    
    ## Define an empty dictionary
    comic_kwargs = {}
        
    try:
        synopsys_tags = story_table_item.td
    except Exception as e:
        print e
        print "Error : False synposys table item \n %s" % (story_table_item)
        return
            
    ## If found add history
    if (synopsys_tags):
        comic_kwargs['storySynopsys'] = synopsys_tags.get_text().strip()
                   
    return comic_kwargs

def get_characters_groups (char_table_item):
    """ Get characters from main table """
    
    ## Define an empty dictionary
    char_group_kwargs = {}
        
    try:
        ## This is the Main Sub  Table for characters and comments
        sub_main_table = char_table_item.td.div.table
        sub_main_item = sub_main_table.find_all("tr",recursive=False)
        
        ## This is the Main Character Table
        char_main_table = sub_main_item[1].td.table
        char_main_items = char_main_table.find_all("tr",recursive=False)
        
        ## Find the character and group subtables
        key = ""
        char_group_table = {}
        for tr in (char_main_items):
            char_text = tr.get_text()
            char_text = char_text.strip()
            if (char_text == "Character Appearances"):
                key = "characters"
            elif (char_text == "Group Appearances"):
                key = "groups"
            else:
                if (key):
                    ## There are one table for each type of char/group
                    char_group_table[key] = []
                    tables = tr.find_all("table")
                    for table in (tables):
                        char_group_table[key].append(table) 
                    key = None
        
        ## Loop into the characters table to get characters
        if ("characters" in char_group_table):
            char_group_kwargs["characters"] = {}
            for table in (char_group_table["characters"]):
                tr_items = table.find_all("tr",recursive=False)
                title = tr_items[0].get_text().strip()
                del tr_items[0]
                char_group_kwargs["characters"][title] = []
                ## Get pairs of name and desc for characters
                for tr in (tr_items):
                    tr_text = tr.get_text().strip()
                    if (tr_text and tr_text !="\n"): 
                        char_group_kwargs["characters"][title].append(tr_text)
        
        ## Loop into the groups to get the groups
        if ("groups" in char_group_table):
            char_group_kwargs["groups"] = []
            table  = char_group_table["groups"][0]
            tr_items = table.tr.td.table.find_all("tr",recursive=False)
            ## Get pairs of name and desc for groups (Roster can be processed later)
            for tr in (tr_items):
                tr_text = tr.get_text().strip()
                if (tr_text and tr_text !="\n"): 
                    char_group_kwargs["groups"].append(tr_text)
                    
    ## TODO: Improve Exception handling
    except Exception as e:
        print e
        print "Error : False character table  \n %s" % (char_table_item)
        return
    
    return char_group_kwargs

def get_next_issue_id (table_item):
    """ Get the id for the next comic in full order """
    
    ## Default variables
    links_div = None
    issues_dict = {}
    
    
    ## Try finding the divs with the links on the piece of HTML
    try:
        order_tr = table_item.td.table.tr
        links_div = order_tr.find_all('div')           
    except Exception as e:
        print e
        print "Error : False order section selected \n %s" %(table_item)
        return
    
    ## First Key for previous issues
    key = "previous"
    issues_dict[key] = []
    if (links_div):
        ## Iterate through the divs
        for link_item in (links_div):
            ## Get the anchor HTML with the link to the issue
            anchors = link_item.find_all("a")
            ## If not an anchor we are in actual issue, change key to next issues
            if (not anchors):
                key = "next"
                issues_dict[key] = []
            ## Else search for the id in the href and append it to the corresponding list
            else:
                id_match = re.search("detail\.php\?idvalue\=(\d*)",anchors[0]['href'])
                issues_dict[key].append(id_match.group(1))
            
            
    return issues_dict

def connect_database(db_filename=":memory:"):
    """ Connect to database and create tables if needed """
    ## Connect SQL Lite
    connection_string = 'sqlite:' + db_filename
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection

    ## Create Comic Book table if not present
    ## ifNotExist was not working properly
    if (not ComicBook.tableExists()):
        ComicBook.createTable()
    ## Create Author table if not present
    if (not Author.tableExists()):
        Author.createTable()
    if (not ComicAuthors.tableExists()):
        ComicAuthors.createTable()
    if (not Character.tableExists()):    
        Character.createTable()
    if (not ComicCharacters.tableExists()):
        ComicCharacters.createTable()
    if (not CharGroup.tableExists()):
        CharGroup.createTable()
    if (not ComicChargroups.tableExists()):
        ComicChargroups.createTable()
    if (not CMRO.tableExists()):
        CMRO.createTable()

def search_for_last():
    """ Try to get the last comic processed to resume the downloading """
    
    ## As we process the comics by reading order search for the max order number
    lastComic_ordernum = ComicBook.select().max(ComicBook.q.orderNumber)
    lastComic_search = ComicBook.selectBy(orderNumber=lastComic_ordernum)
    myLastComic = lastComic_search.getOne(default=None)
    
    ## Deafult values
    next_id = 1
    prev_id = 0

    ## If last comic found get the CMRO
    if (myLastComic):
        myLastCMRO_search = CMRO.selectBy(id=myLastComic.id)
        myLastCMRO = myLastCMRO_search.getOne(default=None)
        if (myLastCMRO):
            next_id = myLastCMRO.nextCmroId
            prev_id = myLastCMRO.prevCmroId
    
    return (next_id,prev_id)
    
##############################################
### Main                                  ####
##############################################
## Create connection to database
db_filename = os.path.abspath('comicdatabase.sqlite')
#os.unlink(db_filename)
    
## Check if exist and get the max value
if os.path.exists(db_filename):
    connect_database(db_filename)
    #os.unlink(db_filename)
    (next_id,prev_id) = search_for_last()
else:
    ## Begin with issue id 1
    connect_database(db_filename)
    next_id = 1
    prev_id = 0
    

## This is for comparisson
last_issue_ids = {}

## Loop while ids available
while (next_id):
## Process each file
#for file_path in (argv[1:]):
#    if os.path.isfile(file_path):
        
        ## Open file and process it with beatiful Soup
        ############################################################################
#        comic_html = open(file_path,'r')
#        print "Processing : %s" % (file_path)
        
        comic_url = "http://cmro.travis-starnes.com/detail.php?idvalue=%s" % (next_id)
        print "Proccessing : %s" % (comic_url)
        
        try:
            comic_html = urlread(comic_url)
            #time.sleep(2)
        except Exception as e:
            print "Error : Fetching from %s did not worked out due to: "
            print e
            
        ## Use a parser to get rid of everything but the tables we want
        only_tables = SoupStrainer('table')
        soup = BeautifulSoup(comic_html,'lxml', parse_only=only_tables)
        
        ## Main table containing issue and ratings
        try:
            main_table = None
            for content in (soup.children):
                ## Search for the one containing the title detail
                if (not content.string and content.find_all("a",href=re.compile("title_detail.php"))):
                    main_table = content
                    break
            if (main_table):
                main_comic_tables = main_table.find_all("table",bgcolor="#D8D8D8")
            if (not main_comic_tables or len(main_comic_tables)>1):
                raise Exception("Main comic table not found on HTML")
        except Exception as e:
            print "Error : No well formed CMRO html"
            print e
            exit()
        
        ### Get all items from main comic table for next process
        main_comic_items = main_comic_tables[0].find_all("tr",recursive=False)
        
        ## Check if essential issue is there (used for recalculate tr index)
        ############################################################################
        idx_inc = 0
        if (re.search("Essential\s*Issue",main_comic_items[1].get_text())):
            idx_inc = 1

        ## Get the intial ComicBook keyword arguments from the main comic table
        ############################################################################
        comic_kwargs = get_comic_title(main_comic_items[2+idx_inc])
        
        if (not comic_kwargs) :
            print "Error : No comic found for id: %s" % (next_id)
            next
        else:
            print "Processing comic %s" % (comic2string(comic_kwargs))
            
        ## Add the Story (4 tr on main table)
        ############################################################################
        add_kwargs = get_comic_story(main_comic_items[3+idx_inc])
        
        if (not add_kwargs):
            print "Error : No story found for: %s" % (comic2string(comic_kwargs))
        else:    
            comic_kwargs.update(add_kwargs)
        
        ## Add the details (7 tr on main table)
        ############################################################################
        details_dict = get_comic_details(main_comic_items[6+idx_inc])
        authors_dict = {}
        
        ## Parse details
        for detail,value in (details_dict.items()):
            value = value.strip()
            ## Check if it is an author
            if (detail in authors_list):
                ## Save for later
                authors_dict[detail] = value
            else:
                ## Convert to specific formats
                if (detail =="Cover Date"):
                    comic_kwargs["coverDate"] = datetime.strptime(value, "%B %Y")
                elif (detail == "Release Date"):
                    comic_kwargs["releaseDate"] = datetime.strptime(value, "%B %Y")
                elif (detail == "Pages"):
                    comic_kwargs["numberOfPages"] = int(value)
                elif (detail == "Cover Price"):
                    value = value.replace("$","")
                    comic_kwargs["coverPrice"] = float(value)  
                elif (detail == "Story Arc"):
                    if (value != "-"):
                        comic_kwargs["storyArc"] = value
                elif (detail == "Universes"):
                        comic_kwargs["universes"] = value.replace(u'\xa0', u' ')

        ## Add the Synopsys (15 tr on table)
        ############################################################################
        add_kwargs = get_comic_synopsys(main_comic_items[13+idx_inc])

        if (not add_kwargs):
            print "Error : No story found for: %s" % (comic2string(comic_kwargs))
        else:
            comic_kwargs.update(add_kwargs)

        ## Add the Characters (17 tr on table)
        ############################################################################
        char_grp_dict = get_characters_groups(main_comic_items[15+idx_inc])
        
        ## Create Comic Book object
        ############################################################################
        myComic = ComicBook(**comic_kwargs)
        
        ## Add authors
        ############################################################################
        myComic.add_authors(authors_dict)
        
        ## Add characters
        ############################################################################
        if ("characters" in char_grp_dict):
            myComic.add_characters(char_grp_dict["characters"])

        ## Add groups
        ############################################################################
        if ("groups" in char_grp_dict):
            myComic.add_groups(char_grp_dict["groups"])
            
        ## Find next comic to parse in the normal order, create CMRO entry
        ############################################################################
        cmro_kwargs = {}
        ## Try to find order and get indexes
        issues_id = None
        if ("ORDER" in main_comic_items[8+idx_inc].get_text()):
            issues_id = get_next_issue_id(main_comic_items[9+idx_inc])
        
        ## Create the arguments for myCMRO
        cmro_kwargs['id'] = myComic.id
        cmro_kwargs['cmroId'] = next_id
            
        ## Check if found and get previous and next id        
        if (issues_id):
            
            ## Check if there is a next_id and get the first item
            if (issues_id['next'] and len(issues_id['next'])>0):
                cmro_kwargs['nextCmroId'] = int(issues_id['next'][0])
            
            ## Check if there is a previous id and get the last item
            if (issues_id['previous'] and len(issues_id['previous'])>0):
                cmro_kwargs['prevCmroId'] = int(issues_id['previous'][-1])

        else:
            print "No next comic found on list for : %s" % (comic2string(comic_kwargs))    
        
        ## Create the CMRO item
        myCMRO = CMRO(**cmro_kwargs)
        
        ## Set next id
        if (myCMRO.nextCmroId):
            next_id = myCMRO.nextCmroId
        
## THE END of main
print "Finished parsing CMRO"