#! /usr/bin/python                                                              
# -*- coding: utf-8 -*-                                                         
#                                                                               
# Simple XML&XSLT transformer.

import lxml                                                                     
from lxml import etree                                                          
                                                                                
if __name__ == "__main__":                                                      
    import sys, os                                                              
                                                                                
    if len(sys.argv) != 3:                                                      
        print "Usage: %s document.xml transform.xsl" % (sys.argv[0])               
        exit(0)                                                                 
                                                                                
    with open(sys.argv[2]) as f:                                                
        doc = etree.parse(f)                                                    
                                                                                
    try:                                                                        
        transform = etree.XSLT(doc)                                           
    except Exception as e:                                 
        print e                                                                 
        exit(1)                                                                 
                                                                                                                                                                               
    with open(sys.argv[1]) as f:                                                
        doc = etree.parse(f)                                                    
                                                                               
    try:                                                                        
        result_dom = transform(doc)                                          
    except lxml.etree.DocumentInvalid as e:                                     
        print e                                                                 
        exit(1)                                                                 
                                                                                
    print etree.tostring(result_dom, pretty_print=True)
