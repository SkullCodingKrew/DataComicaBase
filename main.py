#! /usr/bin/python
# -*- coding: utf-8 -*-
##############################################
### Import definitions                    ####
##############################################
### Python Default modules ###################
from sys import argv
import os
## Beatiful soup import
from bs4 import BeautifulSoup

## For opening urls
import urllib2

### Regular expressions
import re

### SQL ORM
from sqlobject import *

### ComicBook classes ########################
from ComicBook import ComicBook

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
def get_comic_title (text_string):
    """ Parses string and returns a tuple containing: 
        Title  => Title of the comic book serie
        number => Number of the comic book in current Volume
        part   => Part inside the comic book (For comic books with 2 or 3 different stories
        volume => Volume of the comic book title
        order  => Number in reading order (optional)
    """
      
    match = title_re.match(text_string)

    if (match):
        return match.group("title"),match.group("number"),match.group("part"),match.group("vol_n"),match.group("order_n")
    else:
        print "No match for title in %s" % (text_string)
        return None,None,None,None

##############################################
### Main                                  ####
##############################################
## Create connection to database
db_filename = os.path.abspath('comicdatabase.sqlite')
if os.path.exists(db_filename):
    os.unlink(db_filename)

connection_string = 'sqlite:' + db_filename
connection = connectionForURI(connection_string)
sqlhub.processConnection = connection

## Process each file
for file_path in (argv[1:]):
    if os.path.isfile(file_path):
        fh = open(file_path,'r')
        print "Processing : %s" % (file_path)
        soup = BeautifulSoup(fh,'lxml')

        ## Main table containing issue and ratings
        main_table, = soup.select("body > table:nth-of-type(2)")

        ## Main Comic table containing all comic info
        main_comic_table = main_table.tr.td.table

        ## Get Title and order number
        comic_title_tags = main_table.select("h1")
        title,number,part,volume,order = get_comic_title(comic_title_tags[0].get_text())
        number = int(number)
        volume = int(volume)
        order  = int(order)

        ## Get StoryName needs a better navigation 
        story_name_tags = main_comic_table.select('div')

        story_name = story_name_tags[0].get_text().replace('"','')


        ## Create Comic Book table if not present
        ComicBook.createTable(ifNotExists=True)

        ## Create Comic Book object
        ## TODO: Implement directly as a tuple
        myComic = ComicBook(comicTitle=title,issue=number,volume=volume,orderNumber=order,storyName=story_name,part=part)

        ## Get all issues details
        issue_details = main_comic_table.select('.issue_detail_section')
        for span in issue_details:
            ## Match Key: Value pattern
            detail_match = key_value_re.match(span.parent.get_text())

            ## Check if match happened
            if (detail_match):
                ## TODO: Check for subdetails in value for key: value key: value strings

                ## Add first and second parenthesized subgroup as key value
                myComic.add_info(detail_match.group(1),detail_match.group(2))


        ## Print comic info
        myComic.print_info()

## THE END of main
print "Finished parsing the html files"