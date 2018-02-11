#!/usr/bin/python
# coding: utf-8

import sys
import csv

from HTMLParser import HTMLParser

allrest=[]

class adreca:

    def __init__(self):
        self.carrer = None
        self.num = None
        self.districte = None
        self.barri = None
        self.cpostal = None
        self.localitat = None
        self.regio = None
        self.pais = None

    def afegir_carrer(self, carrer):
        self.carrer = carrer

    def afegir_num(self, num):
        self.num = num

    def afegir_districte(self, districte):
        self.districte = districte

    def afegir_barri(self, barri):
        self.barri = barri

    def afegir_cpostal(self, cpostal):
        self.cpostal = cpostal

    def afegir_localitat(self, localitat):
        self.localitat = localitat

    def afegir_regio(self, regio):
        self.regio = regio

    def afegir_pais(self, pais):
        self.pais = pais

    def to_list(self):
        l = []
        l.append(self.carrer) if self.carrer else l.append("---")
        l.append(self.num) if self.num else l.append("---")
        l.append(self.districte) if self.districte else l.append("---")
        l.append(self.barri) if self.barri else l.append("---")
        l.append(self.cpostal) if self.cpostal else l.append("---")
        l.append(self.localitat) if self.localitat else l.append("---")
        l.append(self.regio) if self.regio else l.append("---")
        l.append(self.pais) if self.pais else l.append("---")
        return l

class coord:

    def __init__(self):
        self.lat = None
        self.lon = None

    def afegir_lat(self, latitud):
        self.lat = latitud

    def afegir_lon(self, longitud):
        self.lon = longitud

    def to_list(self):
        l = []
        l.append(self.lat) if self.lat else l.append("---")
        l.append(self.lon) if self.lon else l.append("---")
        return l

    def __nonzero__(self):
        if self.lat is None and self.lon is None:
            return False
        return True

class restaurant:

    def __init__(self):
        self.nom = ""
        self.adreca = None
        self.coord = None
        self.telfs = []
        self.email = None

    def afegir_nom(self,nom):
        self.nom += nom

    def afegir_adreca(self, adreca):
        self.adreca = adreca

    def afegir_coord(self, coord):
        self.coord = coord

    def afegir_telf(self, telf):
        self.telfs.append(telf)

    def afegir_email(self, email):
        self.email = email

    def to_list(self):
        l = []
        l.append(self.nom)
        l.extend(self.adreca.to_list())
        l.extend(self.coord.to_list())
        for i in range(2):
            l.append(self.telfs[i]) if i < len(self.telfs) else l.append("---")
        l.append(self.email) if self.email else l.append("---")
        return l


# creem una subclasse i sobreescribim el metodes del han
class MHTMLParser(HTMLParser):

    ctag = ""
    csect = ""
    crest = restaurant()
    cadreca = adreca()
    ccoord = coord()

    def handle_starttag(self, tag, attrs):
        self.ctag = tag
        if tag == 'v:vcard':
            self.crest = restaurant()
            self.cadreca = None
            self.ccoord = None
            csect = ""
        elif tag == 'v:adr':
            self.cadreca = adreca()
        elif tag == 'v:geo':
            self.ccoord = coord()
        elif tag == 'v:tel':
            self.csect = tag
        elif tag == 'v:email':
            self.csect = tag
        elif tag == 'rdf:description' and self.csect == 'v:email':
            if attrs:
                name, value = attrs[0]
                if value.startswith('mailto:'):
                    value = value[len('mailto:'):]
                self.crest.afegir_email(value)

    def handle_endtag(self, tag):
        self.ctag = ""
        if tag == 'v:vcard':
            if self.cadreca:
                self.crest.afegir_adreca(self.cadreca)
            if self.ccoord:
                self.crest.afegir_coord(self.ccoord)
            allrest.append(self.crest)

    def handle_data(self, data):
        if self.ctag == 'v:fn':
            self.crest.afegir_nom(data)
        elif self.ctag == 'xv:streetname':
            self.cadreca.afegir_carrer(data)
        elif self.ctag == 'xv:streetnumber':
            self.cadreca.afegir_num(data)
        elif self.ctag == 'xv:district':
            self.cadreca.afegir_districte(data)
        elif self.ctag == 'xv:neighborhood':
            self.cadreca.afegir_barri(data)
        elif self.ctag == 'v:postal-code':
            self.cadreca.afegir_cpostal(data)
        elif self.ctag == 'v:locality':
            self.cadreca.afegir_localitat(data)
        elif self.ctag == 'v:region':
            self.cadreca.afegir_regio(data)
        elif self.ctag == 'v:country-name':
            self.cadreca.afegir_pais(data)
        elif self.ctag == 'v:latitude':
            self.ccoord.afegir_lat(data)
        elif self.ctag == 'v:longitude':
            self.ccoord.afegir_lon(data)
        elif self.ctag == 'rdf:value':
            if self.csect == 'v:tel':
                self.crest.afegir_telf(data)

    def handle_charref(self, ref):
        self.handle_entityref('#'+ref)

    def handle_entityref(self, ref):
        cref = self.unescape('&'+ref+';')
        cref = cref.encode('utf8')
        self.handle_data(cref)

print "Leyendo..."
f = open('restaurants.rdf', 'rb') # obre l'arxiu
rdfSource = f.read()
f.close()

parser = MHTMLParser()
parser.feed(rdfSource)
print len(allrest)
f = open('restaurants.csv', 'wb')
writer = csv.writer(f, delimiter="\t")
writer.writerow(["NOM", "CARRER", "NÚM.", "DISTRICTE", "BARRI", "CODI POSTAL",
                 "LOCALITAT", "REGIÓ", "PAÍS", "LATITUD", "LONGITUD",
                 "TELÈFON 1", "TELÈFON 2", "EMAIL"])
for r in allrest:
    writer.writerow(r.to_list())
f.close()
print "Fini"
