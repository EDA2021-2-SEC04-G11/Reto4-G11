import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import edge as ed
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import graphstructure as graph
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT.graph import addEdge, gr
from math import radians, cos, sin, asin, sqrt
import sys
assert cf

# ==============================
# DATA MODEL
# ==============================

class iatamodel:
    def __init__(self,pack) -> None:
        self.name = pack['Name'].strip()
        self.city = pack['City'].strip()
        self.country = pack['Country'].strip()
        self.code = pack['IATA'].strip()
        self.lati = round(float(pack['Latitude'].strip()),2)
        self.long = round(float(pack['Longitude'].strip()),2)
    def printmodel(self):
        divup = '_'*58+'_'*(len(self.city)+len(self.country)+len(str(self.lati))+len(str(self.long))+len(self.name))
        divdown = '-'*58+'-'*(len(self.city)+len(self.country)+len(str(self.lati))+len(str(self.long))+len(self.name))
        print(divup)
        print(f'| name: {self.name} | city: {self.city} | country: {self.country} | latitude: {self.lati} | longitude: {self.long} |')
        print(divdown)

class citymodel:
    def __init__(self,pack) -> None:
        self.city = pack['city_ascii'].strip()
        self.lati = round(float(pack['lat'].strip()),2)
        self.long = round(float(pack['lng'].strip()),2)
        self.country = pack['country']
        self.iso2 = pack['iso2'].strip()
        self.iso3 = pack['iso3'].strip()
        self.admin = pack['admin_name'].strip()
        self.capital = pack['capital'].strip()
        try:
            self.population = round(float(pack['population'].strip()))
        except:
            self.population = 0
        self.id = float(pack['id'].strip())
    def printmodel(self):
        divup = '_'*58+'_'*(len(self.city)+len(self.country)+len(str(self.lati))+len(str(self.long))+len(self.iso3))
        divdown = '-'*58+'-'*(len(self.city)+len(self.country)+len(str(self.lati))+len(str(self.long))+len(self.iso3))
        print(divup)
        print(f'| city: {self.city} | country: {self.country} | latitude: {self.lati} | longitude: {self.long} | iso3: {self.iso3} |')
        print(divdown)

# ==============================
# CHARGE DATA
# ==============================

global analyzer
analyzer = {}

def init():
    analyzer['airports-dir'] = gr.newGraph(datastructure='ADJ_LIST',directed=True, size=10700, comparefunction=cmpairport)
    analyzer['airports-nodir'] = gr.newGraph(datastructure='ADJ_LIST',directed=False, size=10700, comparefunction=cmpairport)
    analyzer['airports-map'] = mp.newMap(numelements=10700)

    analyzer['routes'] = {'map':mp.newMap(numelements=round(92593/2)),'temp':mp.newMap(numelements=round(92593/2))}

    mapcity = mp.newMap(numelements=41001)
    analyzer['cities'] = {'map':mapcity,'count':0}

    analyzer['exhibition'] = {'airports-dir':lt.newList(),'airports-nodir':lt.newList(),'cities':lt.newList()}
    return analyzer

def loadair(airportdata):
    iata = iatamodel(airportdata)
    key = iata.code
    gr.insertVertex(analyzer['airports-dir'],key)
    gr.insertVertex(analyzer['airports-nodir'],key)
    mp.put(analyzer['airports-map'],key,iata)
    # ADD EXHIBITION IN DIR
    if lt.size(analyzer['exhibition']['airports-dir']) < 2:
        lt.addLast(analyzer['exhibition']['airports-dir'],iata)
    elif lt.size(analyzer['exhibition']['airports-dir']) == 2:
        lt.removeLast(analyzer['exhibition']['airports-dir'])
        lt.addLast(analyzer['exhibition']['airports-dir'],iata)
    # ADD EXHIBITION IN NODIR
    if lt.size(analyzer['exhibition']['airports-nodir']) < 2:
        lt.addLast(analyzer['exhibition']['airports-nodir'],iata)
    elif lt.size(analyzer['exhibition']['airports-nodir']) == 2:
        lt.removeLast(analyzer['exhibition']['airports-nodir'])
        lt.addLast(analyzer['exhibition']['airports-nodir'],iata)

def loadcity(citydata):
    city = citymodel(citydata)
    analyzer['cities']['count'] += 1
    entry = mp.get(analyzer['cities']['map'],city.city)
    if entry == None:
        lst = lt.newList(datastructure='ARRAY_LIST')
        lt.addLast(lst,city)
        newvalue = {'lst':lst,'count':1}
        mp.put(analyzer['cities']['map'],city.city,newvalue)
    else:
        found = entry['value']
        found['count']+=1
        lt.addLast(found['lst'],city)
    # ADD EXHIBITION IN CITIES
    if lt.size(analyzer['exhibition']['cities']) < 2:
        lt.addLast(analyzer['exhibition']['cities'],city)
    elif lt.size(analyzer['exhibition']['cities']) == 2:
        lt.removeLast(analyzer['exhibition']['cities'])
        lt.addLast(analyzer['exhibition']['cities'],city)

def loadroute(routedata):
    loadrouteDir(routedata)
    loadrouteNodir(routedata)  

def loadrouteDir(routedata):
    a = routedata['Departure'].strip()
    b = routedata['Destination'].strip()
    distance = float(routedata['distance_km'].strip())
    airline = routedata['Airline'].strip()
    weight = (airline,distance)
    gr.addEdge(analyzer['airports-dir'],a,b,weight)

def loadrouteNodir(routedata):
    # Vertexa and vertexb can have multiple edges from different airports
    # In the edges, they must be connected by the same airline
    a = routedata['Departure'].strip()
    b = routedata['Destination'].strip()
    distance = float(routedata['distance_km'].strip())
    airline = routedata['Airline'].strip()
    weight = (airline,distance)
    edges = gr.adjacentEdges(analyzer['airports-dir'],b)
    for edgefound in lt.iterator(edges):
        vertexb = ed.other(edgefound,b)
        if vertexb == a:
            weightfound = ed.weight(edgefound)
            if weightfound == weight:
                gr.addEdge(analyzer['airports-nodir'],a,b,weight)

# ==============================
# COMPARE FUNCTIONS
# ==============================

def cmpairport(iatai,iataj):
    if type(iataj) == dict:
        iataj = iataj['key']
    if type(iatai) == dict:
        iatai = iatai['key']
    if iatai == iataj:
        return 0
    elif iatai > iatai:
        return 1
    return -1

def cmpcity(idi,idj):
    if type(idj) == dict:
        idj = idj['key']
    if type(idi) == dict:
        idi = idi['key']
    if idi == idj:
        return 0
    elif idi > idj:
        return 1
    return -1

# ==============================
# COMPLEMENTARY
# ==============================

def haversine(lat1, lon1, lat2, lon2):
    R = 3959.87433 # this is in miles.  For Earth radius in kilometers use 6372.8 km
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
    c = 2*asin(sqrt(a))
    
    return R * c

# ==============================
# REQUIREMENTS
# ==============================

def req1():
    pass
def req2():
    pass
def req3():
    pass
def req4():
    pass
def req5():
    pass
def req6():
    pass
def req7():
    pass
