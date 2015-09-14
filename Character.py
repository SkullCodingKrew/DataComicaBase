# -*- coding: utf-8 -*-
"""This module contains a basic ComicBook Class
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
class ComicBook(object):
  """ Comic Book class, to be explained ;) """

  def __init__(self,title,number,volume=1,order_n=-1):
    """ Initialize object. If no volume is pass down 1 is asume, 
        if no order 0 for checking against positive integers 
    """
    self.title   = title
    self.number  = number
    self.volume  = volume
    self.order_n = order_n
    self.info    = {}

    

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

    

