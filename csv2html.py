#!/usr/bin/python
# coding: utf-8

import sys
import ast
import csv
import urllib as URL
import xml.etree.ElementTree as ET
import HTMLParser
import math
import codecs

parades = []
restaurants = []
query = []

class coord:
    def __init__(self):
        self.lat = None
        self.lon = None

    def afegirLat(self, latitud):
        self.lat = latitud

    def afegirLon(self, longitud):
        self.lon = longitud

    def getLat(self):
        return self.lat

    def getLon(self):
        return self.lon

    def to_list(self):
        l = []
        l.append(self.lat) if self.lat else l.append("---")
        l.append(self.lon) if self.lon else l.append("---")
        return l

    def __nonzero__(self):
        if self.lat is None and self.lon is None:
            return False
        return True

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

    def afegirCarrer(self, carrer):
        self.carrer = carrer

    def afegirNum(self, num):
        self.num = num

    def afegirDistricte(self, districte):
        self.districte = districte

    def afegirBarri(self, barri):
        self.barri = barri

    def afegirCPostal(self, cpostal):
        self.cpostal = cpostal

    def afegirLocalitat(self, localitat):
        self.localitat = localitat

    def afegirRegio(self, regio):
        self.regio = regio

    def afegirPais(self, pais):
        self.pais = pais

    def getCarrer(self):
        return self.carrer

    def getNum(self):
        return self.num

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

class restaurant():
    def __init__(self):
        self.nom = None
        self.adreca = None
        self.telf1 = None
        self.telf2 = None
        self.email = None
        self.coord = None
        self.near = None

    def afegirNom(self, nom):
        self.nom = nom

    def afegirAdreca(self, adreca):
        self.adreca = adreca

    def afegirTelf(self, telf):
        if not self.telf1:
            self.telf1 = telf
        elif not self.telf2:
            self.telf2 = telf

    def afegirEmail(self, email):
        self.email = email

    def afegirCoord(self, lat, lon):
        if not self.coord:
            self.coord = coord()
        self.coord.afegirLat(lat)
        self.coord.afegirLon(lon)

    def afegirNear(self, near):
        self.near = near

    def getLat(self):
        return self.coord.getLat()

    def getLon(self):
        return self.coord.getLon()

    def getNom(self):
        return self.nom

    def getCarrer(self):
        return self.adreca.getCarrer()

    def getNum(self):
        return self.adreca.getNum()

    def getTelfs(self):
        return (self.telf1, self.telf2)

    def to_listForHtml(self):
        l = []
        l.append(self.nom)
        l.extend(self.adreca.to_list())
        l.extend(self.coord.to_list())
        l.append(self.telf1) if self.telf1 else l.append("---")
        l.append(self.telf2) if self.telf2 else l.append("---")
        l.append(self.email) if self.email else l.append("---")
        if not self.near:
            l.append("---")
            l.append("---")
        else:
            if not self.near[0]:
                listaBicis = "No hi ha."
            else:
                listaBicis = "<ul>"
                for bici in self.near[0]:
                    d = '%.3f' % bici[1]
                    listaBicis += "\n<li>" + bici[0] + " (a " + d + " km):\n"
                    listaBicis += str(bici[2]) + " disponibles</li>"
                listaBicis += "\n</ul>"
            if not self.near[1]:
                listaSlots = "No hi ha."
            else:
                listaSlots = "<ul>"
                for slot in self.near[1]:
                    d = '%.3f' % slot[1]
                    listaSlots += "\n<li>" + slot[0] + " (a " + d + " km)</li>"
                    listaSlots += str(slot[2]) + " disponibles</li>"
                listaSlots += "\n</ul>"
        l.append(listaBicis)
        l.append(listaSlots)
        return l

class bicing():
    def __init__(self):
        self.iden = None
        self.carrer = None
        self.num = None
        self.bicis = None
        self.slots = None
        self.coord = None

    def afegirIden(self, iden):
        self.iden = iden

    def afegirCarrer(self, carrer):
        self.carrer = carrer

    def afegirNum(self, num):
        self.num = num

    def afegirBicis(self, bicis):
        self.bicis = bicis

    def afegirSlots(self, slots):
        self.slots = slots

    def afegirCoord(self, lat, lon):
        if not self.coord:
            self.coord = coord()
        self.coord.afegirLat(lat)
        self.coord.afegirLon(lon)

    def getLat(self):
        return self.coord.getLat()

    def getLon(self):
        return self.coord.getLon()

    def getIden(self):
        return self.iden

    def getCarrer(self):
        return self.carrer

    def getNum(self):
        return self.num

    def getBicis(self):
        return self.bicis

    def getSlots(self):
        return self.slots

def getBicing():
    socket = URL.urlopen('http://wservice.viabicing.cat/getstations.php?v=1')
    xmlsrc = socket.read()
    socket.close()
    root = ET.fromstring(xmlsrc)

    for station in root.findall('station'):
        st = bicing()
        st.afegirIden(station.find('id').text)
        st.afegirCarrer(station.find('street').text)
        if station.find('streetNumber') is not None:
            st.afegirNum(station.find('streetNumber').text)
        st.afegirBicis(int(station.find('bikes').text))
        st.afegirSlots(int(station.find('slots').text))
        st.afegirCoord(float(station.find('lat').text), float(station.find('long').text))
        if st: parades.append(st)

def getDistance(lat1, lon1, lat2, lon2):
    r = 6371.009
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    l1 = math.radians(lat1)
    l2 = math.radians(lat2)

    a = (math.sin(delta_lat/2) ** 2) + (math.sin(delta_lon/2) ** 2) * math.cos(l1) * math.cos(l2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return r * c

def getCloseStations(res):

    haySlots = []
    hayBicis = []

    for st in parades:
        d = getDistance(res.getLat(), res.getLon(), st.getLat(), st.getLon())

        if (d < 1):
            if st.getNum():
                address = codecs.decode(st.getCarrer() + ", " + st.getNum(), "unicode_escape")
            else:
                address = codecs.decode(st.getCarrer(), "unicode_escape")
            if st.getBicis() > 0:
                hayBicis.append((address, d, st.getBicis()))
            if st.getSlots() > 0:
                haySlots.append((address, d, st.getBicis()))

    hayBicis = sorted(hayBicis, key=lambda x: x[1])
    haySlots = sorted(haySlots, key=lambda x: x[1])

    return (hayBicis, haySlots)

def getTransports(path):
    ifile  = open(path, 'r')
    reader = csv.reader(ifile, delimiter=';')
    reader.next()
    trans = [ t for t in map(Transport, reader) if t.valid() ]
    ifile.close()
    return trans

def query(s):
    if s is None:
        return restaurants
    #isinstance(stuff,list) // tuple, str, bool, ...
    res = []
    if isinstance(s, list):
        for member in s:
            r1 = query(member)
            for r in r1:
                if r not in res:
                    res.append(r)
    elif isinstance(s, tuple):
        current = restaurants
        for member in s:
            r1 = query(member)
            for r in r1:
                if r in current:
                    res.append(r)
            current = res
            res = []
        res = current
    elif isinstance(s, str):
        for r in restaurants:
            if s in r.getNom():
                res.append(r)
    else:
        print "Wrong query."
    return res

def htmlTableHeadline(l):
    row = "<tr>"
    for e in l:
        row += "\n<th>" + e + "</th>"
    "\n</tr>"
    return row

def htmlTableRow(l):
    row = "<tr>"
    for e in l:
        row +=  "\n<td>" + str(e) + "</td>"
    row += "\n</tr>"
    return row

# START
print "Leyendo..."
getBicing()
f = open('restaurants.csv', 'rb')
csvReader = csv.reader(f, delimiter='\t')
headline = next(csvReader, None)
for row in csvReader:
    cres = restaurant()
    cadreca = adreca()
    if row[0] != "---": cres.afegirNom(row[0])
    if row[1] != "---": cadreca.afegirCarrer(row[1])
    if row[2] != "---": cadreca.afegirNum(row[2])
    if row[3] != "---": cadreca.afegirDistricte(row[3])
    if row[4] != "---": cadreca.afegirBarri(row[4])
    if row[5] != "---": cadreca.afegirCPostal(row[5])
    if row[6] != "---": cadreca.afegirLocalitat(row[6])
    if row[7] != "---": cadreca.afegirRegio(row[7])
    if row[8] != "---": cadreca.afegirPais(row[8])
    if cadreca: cres.afegirAdreca(cadreca)
    if row[9] != "---" and row[10] != "---": cres.afegirCoord(float(row[9]), float(row[10]))
    if row[11] != "---": cres.afegirTelf(row[11])
    if row[12] != "---": cres.afegirTelf(row[12])
    if row[13] != "---": cres.afegirEmail(row[13])
    if cres: restaurants.append(cres)

f.close()

headline.append("ESTACIONS DE BICING PROPERES AMB BICIS")
headline.append("ESTACIONS DE BICING PROPERES AMB APARCAMENT")

print "Query: "
if len(sys.argv) < 2:
    consulta = None
    print "No query - Outputing everything"
else:
    consulta = ast.literal_eval(sys.argv[1])
    print consulta
print "Buscando..."
query = query(consulta)
for q in query:
    q.afegirNear(getCloseStations(q))

output = """<!DOCTYPE html>
<meta charset="UTF-8">
<head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
}
</style>
</head>
<body>
<table style="width:100%">"""
output += htmlTableHeadline(headline)
for q in query:
    output += htmlTableRow(q.to_listForHtml())
output += """
</table>
</body>
</html>"""

f = open('restaurants.html', 'w')
f.write(output)
f.close()
print "Fini"
