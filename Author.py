# -*- coding: utf-8 -*-
"""This module contains a basic Author Class
related methods and types
"""
##############################################
### Imports                                ###
##############################################

### Python Default modules ###################

##############################################
### Classes                                ###
##############################################

### ComicBook ################################
class Author(object):
    """ Author class, to be explained ;) """

    def __init__(self,name):
        """ Initialize object. If no volume is pass down 1 is asume, 
            if no order 0 for checking against positive integers 
        """
        self.name    = name

    def add_info (self,key,value):
        """ Add some info to the Comic with a key/value par """
        self.info[key] = value

    def print_info (self):
        """ Print the comic object to the terminal """

        print "############################################"
        print "Title: "        + self.title
        print "Issue number: " + self.number
        print "Volume: "       + self.volume
        print "Order number: " + self.order_n

        print "### Other Info #############################"
    
        ## Iterate through the comic info
        for key,val in self.info.iteritems():
            print key + ": " + val

    

