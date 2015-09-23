# -*- coding: utf-8 -*-
"""This module contains a basic ComicBook Class
related methods and types
"""
##############################################
### Imports                                ###
##############################################

### Python Default modules ###################

### Python SQLObject #########################
from sqlobject import *
from sqlobject.col import StringCol

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
  
    comicBook  = RelatedJoin('ComicBook')
    
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
    
    ## Name Columns Middle is optional
    alias = StringCol()
    
    ## To be added like above?
    real_name = StringCol(default=None) 

    ## N to N relationship
    comicBook  = RelatedJoin('ComicBook')
    
    def print_info (self):
        """ Print the comic object to the terminal """
        print "############################################"
        print "Alias: "        + self.alias

### StoryArc ##################################
class StoryArc(SQLObject):
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
    storyArc      = ForeignKey("StoryArc", default=None)
    storySynopsys = StringCol(default=None)
    character     = RelatedJoin('Character')
    
    ## Order of the Comic for reading
    orderNumber   = IntCol()
    
    ## Author link info (n-n relationship)
    writer    = RelatedJoin('Author') 
    penciller = RelatedJoin('Author')
    inker     = RelatedJoin('Author')
    collorist = RelatedJoin('Author')
    letterer  = RelatedJoin('Author')
    
    ## Publishing info 
    coverDate     = DateCol(default=None)
    releaseDate   = DateCol(default=None)
    numberOfPages = IntCol(default=None)
    coverPrice    = CurrencyCol(default=None) ## Beware of problems with Real numbers
    publisher     = StringCol(default='Marvel')
            
    ## Readed already
    readed    = BoolCol(default=False)

    def add_info (self,key,value):
    #    """ Add some info to the Comic with a key/value par """
    #    self.info[key] = value
        True

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

    

