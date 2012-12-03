#!/usr/bin/env python
'''
Created on 25.09.2012

@author: Christoph Gerneth
@contact: if1184@haw-ingolstadt.de
@license: CC-BY-SA
@version: 0.2
list Mensa-Menues for Studentenwerk Erlangen-Nuernberg

Data by Bytewerk Ingolstadt - http://namnam.bytewerk.org/
'''

#change this, if you are not interested in Mensa Ingolstadt:
default_mensa = "Ingolstadt"


usage = '''
    ____                          _____                      
   / __ )_____delicious   ______ / ___/____ ___  __________   
  / __  / ___/ __ \ | /| / / __ \\\__ \/ __ `/ / / / ___/ _ \ 
 / /_/ / /  / /_/ / |/ |/ / / / /__/ / /_/ / /_/ / /__/  __/  
/_____/_/   \____/|__/|__/_/ /_/____/\__,_/\__,_/\___/\___/   

pro-tip: if you use Linux, add the following line to your ~/.bashrc:
alias lsmensa='python pathtothisfile/lsmensa.py'                                                  
'''
import xml.dom.minidom as md
import urllib2
from datetime import datetime
import sys

def updatexml(url):
    #@TODO: check for new updates only - write tempfile, so no internetaccess is required
    try:
        file = urllib2.urlopen(url, timeout=4)
    except:
        print "Konnte die XML nicht laden"
        sys.exit()
    dom = md.parse(file)
    file.close()
    return dom

def printList(foodlist, mensa, listall=False):
    #@TODO: flexible width
    datestamp = datetime(year=1990, month=1, day=1)
    print "%-59s %5s %5s %1s %1s %1s" % ("Heute in der Mensa " + mensa, "Stud", "Norm", "V", "M", "R")
    for essen in foodlist:
        if (datetime.date(datetime.now()) == datetime.date(essen.date)) or listall == True:
            if listall == True and datestamp != essen.date:
                print
                print datetime.date(essen.date)
            print "%-59s %5.2f %5.2f %1s %1s %1s" \
            % (essen.name, int(essen.price_student) / 100.0, int(essen.price_normal) / 100.0, "X" if essen.veggie else "", "X" if essen.muslim else "", "X" if essen.rind else "")
            datestamp = essen.date

class Essen(object):
    def __init__(self, knoten):
        if knoten.nodeName == "Mensaessen":
            self.veggie = True if knoten.getAttribute("vegetarisch") == "true" else False
            self.muslim = True if knoten.getAttribute("moslem") == "true" else False
            self.rind = True if knoten.getAttribute("rind") == "true" else False
            try:
                self.name = knoten.getElementsByTagName("beschreibung")[0].firstChild.data
            except:
                self.name = "Essen ohne Namen"
            try:
                self.price_student = knoten.getElementsByTagName("studentenPreis")[0].firstChild.data
            except:
                self.price_student = "0"
            try:
                self.price_normal = knoten.getElementsByTagName("normalerPreis")[0].firstChild.data
            except:
                self.price_normal = "0"
            date = knoten.parentNode.getElementsByTagName("tag")[0].firstChild.data
            self.date = datetime.strptime(date, "%Y-%m-%d")
            
    def __repr__(self):
        return "%s: %s fuer %.2f Euro" % (datetime.strftime(self.date, "%A, %d.%m"), self.name, int(self.price_student) / 100.0)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--mensa", default=default_mensa, dest="mensa", help="Alternative Mensa angeben")
    parser.add_option("-a", "--all", action="store_true", help="list all", dest="la", default=False)
    
    (options, args) = parser.parse_args()
    
    xml = {"Ingolstadt" : "http://namnam.bytewerk.org/files/Studiwerk-Erlangen-Nuernberg-Mensa-IN.xml",
           "Erlangen_Sued" : "http://namnam.bytewerk.org/files/Studiwerk-Erlangen-Nuernberg-Mensa-Sued-Erlangen.xml",
           "Erlangen_Langemarckplatz" : "http://namnam.bytewerk.org/files/Studiwerk-Erlangen-Nuernberg-Mensa-Erlangen-Langemarckplatz.xml",
           "Ansbach" : "http://namnam.bytewerk.org/files/Studiwerk-Erlangen-Nuernberg-Mensa-Ansbach.xml",
           "Eichstaett": "http://namnam.bytewerk.org/files/Studiwerk-Erlangen-Nuernberg-Mensa-EI.xml",
           "Nuernberg_Mensateria": "http://namnam.bytewerk.org/files/Studiwerk-Erlangen-Nuernberg-Mensa-Mensateria-N.xml",
           "Nuernberg_Regensburgerstr": "http://namnam.bytewerk.org/files/Studiwerk-Erlangen-Nuernberg-Mensa-Regensburgerstr.-N.xml",
           "Nuernberg_Schuett": "http://namnam.bytewerk.org/files/Studiwerk-Erlangen-Nuernberg-Mensa-Schuett-N.xml",
           }
    
    if xml.has_key(options.mensa):
        dom = updatexml(xml[options.mensa])
    else:
        print "Mensa nicht gefunden. Versuchen Sie:"
        for mensa in xml.iterkeys():
            print mensa
        sys.exit(1)
        
    essensliste = []
    for essen in dom.getElementsByTagName("Mensaessen"):
        food_object = Essen(essen)
        #print food_object
        essensliste.append(food_object)
    printList(essensliste, options.mensa, options.la)  