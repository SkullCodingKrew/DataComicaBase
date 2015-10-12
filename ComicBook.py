# -*- coding: utf-8 -*-
"""This module contains a basic ComicBook Class
related methods and types
"""
##############################################
### Imports                                ###
##############################################

### Python Default modules ###################
### Regular expressions
import re

### Python SQLObject #########################
from sqlobject import *
from sqlobject.col import StringCol, ForeignKey
from sqlobject.sresults import SelectResults

##############################################
### Classes                                ###
##############################################
### Author ###################################
class Author(SQLObject):
    """ Author class, to be explained ;) """
    
    ## Name Columns Middle is optional
    firstName  = StringCol()
    middleName = StringCol(default=None)
    lastName   = StringCol()
  
    comicBook  = SQLRelatedJoin('ComicBook',
            intermediateTable='comic_authors',
            createRelatedTable=False)
    
    def print_info (self):
        """ Print the comic object to the terminal """

        print "############################################"
        print "First Name: "        + self.firstName
        if self.middleName:
            print "Middle Name: "        + self.middleName
        print "Last Name: "         + self.lastName

### Character ################################
class Character(SQLObject):
    """ Character class, to be explained ;) """
    
    ## Alias (name of the character)
    alias = StringCol()
    
    ## To be added like above?
    real_name = StringCol(default=None) 

    ## N to N relationship
    comicBook  = SQLRelatedJoin('ComicBook',
            intermediateTable='comic_characters',
            createRelatedTable=False)
    
    def print_info (self):
        """ Print the comic object to the terminal """
        print "############################################"
        print "Alias: "        + self.alias

### Groups ####################################
class CharGroup(SQLObject):
    """ Group class, to be explained ;) """
    
    ## Alias (name of the character)
    name = StringCol()
    
    ## To be added like above?
    roster = StringCol(default=None) 

    ## N to N relationship
    comicBook  = SQLRelatedJoin('ComicBook',
            intermediateTable='comic_groups',
            createRelatedTable=False)
    
    def print_info (self):
        """ Print the comic object to the terminal """
        print "############################################"

### StoryArc ##################################
class StoryArc(SQLObject):
    """ Author class, to be explained ;) """
    
    ## Name Columns Middle is optional
    name  = StringCol()

    comicBook  = RelatedJoin('ComicBook')
    
    def print_info (self):
        """ Print the comic object to the terminal """

### Universe ##################################
class Universe(SQLObject):
    """ Author class, to be explained ;) """
    
    ## Name Columns Middle is optional
    name  = StringCol()

    comicBook  = RelatedJoin('ComicBook')
    
    def print_info (self):
        """ Print the comic object to the terminal """

### ComicBook ################################
class ComicBook(SQLObject):
    """ Comic Book class, to be explained ;) """
    ###################################
    ## SQL Columns for SQL object
    ###################################

    ## Comic Collection related
    comicTitle    = StringCol()
    volume        = IntCol()
    issue         = IntCol()
    part          = StringCol(default=None)
    
    ## Story Related
    storyName     = StringCol()
    storyArc      = StringCol(default=None)
    ## TODO: Do we need an extra table?
    #storyArc      = ForeignKey("StoryArc", default=None)
    storySynopsys = StringCol(default=None)
    character     = SQLRelatedJoin('Character',
                                   intermediateTable='comic_characters',
                                   createRelatedTable=False)

    group         = SQLRelatedJoin('CharGroup',
                                   intermediateTable='comic_groups',
                                   createRelatedTable=False)
    
    universes      = StringCol(default=None)
    ## TODO: Do we need an extra table?
    #Universe      = ForeignKey("Universe")
    
    ## Order of the Comic for reading
    orderNumber   = IntCol()
    
    ## Author link info (n-n relationship)
    authors = SQLRelatedJoin('Author',
            intermediateTable='comic_authors',
            createRelatedTable=False)
    
    ## Publishing info 
    coverDate     = DateCol(default=None)
    releaseDate   = DateCol(default=None)
    numberOfPages = IntCol(default=None)
    coverPrice    = CurrencyCol(default=None) ## Beware of problems with Real numbers
    publisher     = StringCol(default='Marvel')
            
    ## Readed already
    readed    = BoolCol(default=False)

    def add_authors (self,authors_dict):
        """ Add authors to the comicbook """
        ### Split for authors
        for key,value in (authors_dict.items()):
            authors = value.split(",")
        
            ## Loop for each author
            for author_str in authors:
                ## Create arguments for Author Object
                name_args = {}
            
                ## Strip spaces at the beguining and end
                author_str = author_str.strip()
            
                #Split the name in its components
                if (not author_str):
                    print "Author is missing %s" % (key)
                if (author_str):
                    names = author_str.split(" ")
                    name_args['firstName'] = names[0]
                    if (len(names) == 2):
                        name_args['lastName'] = names[1]
                    elif (len(names) == 3):
                        name_args['lastName'] = names[2]
                        name_args['middleName'] = names[1]
                
                    ## Search for Author in database
                    Author_search = Author.selectBy(**name_args)
                    try:
                        myAuthor = Author_search.getOne(None)
                    except Exception as e:
                        ## Catch duplicates entry and report
                        print e
                        print "Error : Duplicated entry for %s" % name_args
            
                    ## If Author not found create a new entry 
                    if (not myAuthor):
                        myAuthor = Author(**name_args)
            
                    ## Add relationship author/comic
                    myComicAuthor = ComicAuthors(comic=self.id,
                                             author=myAuthor.id,
                                             role=key)   

    def add_characters (self,characters_dict):
        """ Add characters to the comicbook """
        
        ### Loop through the characters type
        for role,characters in (characters_dict.items()):
            
            ## Loop for each character
            for idx in range(len(characters)/2):
                ## Create arguments for Author Object
                char_args = {}
                
                ## Alias & Description
                char_args["alias"] = characters[idx*2]
                comment = characters[idx*2+1] 
                       
                ## Search for Author in database
                Character_search = Character.selectBy(**char_args)
                try:
                    myCharacter = Character_search.getOne(None)
                except Exception as e:
                    ## Catch duplicates entry and report
                    print e
                    print "Error : Duplicated entry for %s" % char_args
            
                ## If Character not found create a new entry 
                if (not myCharacter):
                    myCharacter = Character(**char_args)
            
                ## Add relationship author/comic
                myComicCharacter = ComicCharacters(comic=self.id,
                                                   character=myCharacter.id,
                                                   comment=comment,
                                                   role=role)   

    def add_groups (self,groups_list):
        """ Add groups to the comicbook """
        
        ## Loop for each character
        for idx in range(len(groups_list)/2):
                
                ## Create arguments for Group Object
                group_args = {}
                
                ## Check if roster defined
                roster = None
                name = groups_list[idx*2]
                match_roster = re.search("\((.*)\)",name)
                if (match_roster):
                    roster = match_roster.group(1)
                    name = name.replace(match_roster.group(0),"")
                
                ## Create arguments    
                group_args['name'] = name.strip()
                group_args['roster'] = roster
                comment = groups_list[idx*2+1] 
                       
                ## Search for Group in database
                Group_search = CharGroup.selectBy(**group_args)
                try:
                    myGroup = Group_search.getOne(None)
                except Exception as e:
                    ## Catch duplicates entry and report
                    print e
                    print "Error : Duplicated entry for %s" % group_args
            
                ## If Character not found create a new entry 
                if (not myGroup):
                    myGroup = CharGroup(**group_args)
            
                ## Add relationship author/comic
                myComicGroup = ComicChargroups(comic=self.id,
                                               group=myGroup.id,
                                               comment=comment)   


    def print_info (self):
        """ Print the comic object to the terminal """

        print "############################################"
        print "Title: "        + self.comicTitle
        print "Issue number: " + str(self.issue)
        print "Volume: "       + str(self.volume)
        print "Order number: " + str(self.orderNumber)

        print "### Story Info #############################"
        print "Story: "        + self.storyName
        if (self.storySynopsys):
            print "Synopsys: " + self.storySynopsys
    
        ## Iterate through the comic info
        #for key,val in self.info.iteritems():
        #    print key + ": " + val

### ComicAuthors ###################################
class ComicAuthors(SQLObject):
    """ Comic Author relationship class, to be explained ;) """
    class sqlmeta:
         table = "comic_authors"
    
    ## Correlation table rows
    comic  = ForeignKey('ComicBook', notNull=True, cascade=True)
    author = ForeignKey('Author', notNull=True, cascade=True)
    role   = StringCol(notNull=True)
    unique = index.DatabaseIndex(comic, author, role, unique=True)
    
### ComicCharacter ###################################
class ComicCharacters(SQLObject):
    """ Comic Author relationship class, to be explained ;) """
    class sqlmeta:
         table = "comic_characters"
    
    ## Correlation table rows
    comic     = ForeignKey('ComicBook', notNull=True, cascade=True)
    character = ForeignKey('Character', notNull=True, cascade=True)
    role      = StringCol(notNull=True)
    comment   = StringCol(default=None)
    unique    = index.DatabaseIndex(comic, character, unique=True)

### ComicCharacter ###################################
class ComicChargroups(SQLObject):
    """ Comic Groups relationship class, to be explained ;) """
    class sqlmeta:
         table = "comic_chargroups"
    
    ## Correlation table rows
    comic     = ForeignKey('ComicBook', notNull=True, cascade=True)
    group     = ForeignKey('CharGroup', notNull=True, cascade=True)
    comment   = StringCol(default=None)
    unique    = index.DatabaseIndex(comic, group, unique=True)
    

