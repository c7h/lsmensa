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

def printList(foodlist, mensa):
    #@TODO: flexible width
    datestamp = datetime(year=1990, month=1, day=1)
    print "%-59s %5s %5s %-10s" % ("Heute in der Mensa " + mensa, "Stud", "Norm", "Typ")
    for essen in foodlist:
        if datestamp != essen.date:
            print
            print essen.date
        print "%-59s %5.2f %5.2f %-10s" \
            % (essen.name, int(essen.price_student) / 100.0, int(essen.price_normal) / 100.0, essen.foodtype)
        datestamp = essen.date

class Essen(object):
    def __init__(self, knoten):
        if knoten.nodeName == "Mensaessen":
            try:
                self.foodtype = knoten.getElementsByTagName("token")[0].firstChild.data
            except:
                self.foodtype = ""
            '''
            self.veggie = True if foodtype == "Vegetarisch" else False
            self.vegan  = True if foodtype == "Vegan" else False
            self.chicken= True if foodtype == "Gefluegel" else False
            self.pork   = True if foodtype == "Schwein" else False
            self.rind   = True if foodtype == "Rind" else False
            self.fish   = True if foodtype == "Fisch" else False
            self.deer   = True if foodtype == "Wild" else False
            '''
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
            date_node = knoten.parentNode.getElementsByTagName("tag")[0].firstChild.data
            date = datetime.strptime(date_node, "%Y-%m-%d")
            self.date = datetime.date(date)
            
    def __repr__(self):
        return "%s: %s fuer %.2f Euro" % (datetime.strftime(self.date, "%A, %d.%m"), self.name, int(self.price_student) / 100.0)


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage=usage)
    parser.add_option("-m", "--mensa", default=default_mensa, dest="mensa", help="Alternative Mensa angeben")
    parser.add_option("-a", "--all", action="store_true", help="list all", dest="la", default=False)
    
    (options, args) = parser.parse_args()

    today = datetime.date(datetime.now())
    
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

    if options.la:
        printliste = filter(lambda x: x.date >= today, essensliste) #  filter old meals
    else:
        printliste = filter(lambda x: x.date == today, essensliste)
    printList(printliste, options.mensa)  
