import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import graphstructure as graph
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT.graph import gr
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
        print('\n---------------------------------------------------------------------------------------------------------------------')
        print(f'| name: {self.name} | city: {self.city} | country: {self.country} | latitude: {self.lati} | longitude: {self.long} |')
        print('---------------------------------------------------------------------------------------------------------------------')

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
        print('\n---------------------------------------------------------------------------------------------------------------------')
        print(f'| city: {self.city} | country: {self.country} | latitude: {self.lati} | longitude: {self.long} | iso3: {self.iso3} |')
        print('---------------------------------------------------------------------------------------------------------------------')

# ==============================
# CHARGE DATA
# ==============================

global analyzer
analyzer = {}

def init():

    analyzer['airports-dir'] = gr.newGraph(datastructure='ADJ_LIST',directed=True, size=10700, comparefunction=cmpairport)
    #analyzer['airports-nodir'] = gr.newGraph(datastructure='ADJ_LIST',directed=False, size=10700, comparefunction=cmpairport)
    analyzer['cities-dir'] = gr.newGraph(datastructure='ADJ_LIST',directed=True, size=41001, comparefunction=cmpcity)
    #nalyzer['cities-nodir'] = gr.newGraph(datastructure='ADJ_LIST',directed=False, size=41001, comparefunction=cmpcity)
    analyzer['cities-map'] = mp.newMap(numelements=41001)
    analyzer['airports-map'] = mp.newMap(numelements=10700)
    analyzer['exhibition'] = None
    return analyzer

def loadair(airportdata):
    iata = iatamodel(airportdata)
    key = iata.code
    gr.insertVertex(analyzer['airports-dir'],key)
    mp.put(analyzer['airports-map'],key,iata)
    # ADD EXHIBITION
    if analyzer['exhibition'] == None:
        analyzer['exhibition'] = iata

def loadcity(citydata):
    city = citymodel(citydata)
    key = city.city
    gr.insertVertex(analyzer['cities-dir'],key)
    # ADD TO CITIES-MAP BUT VERIFY IF IT'S BEEN ADDED
    found = mp.get(analyzer['cities-map'],city.city)
    if found != None:
        # HAS BEEN ADDED, SO WE ADD THE CITY TO THE LIST OF THAT KEY
        found = found['value']
        lt.addLast(found,city)
    else:
        # HASN'T BEEN ADDED
        lst = lt.newList()
        lt.addLast(lst,city)
        mp.put(analyzer['cities-map'],city.city,lst)

def loadroute(routedata):
    start = routedata['Departure'].strip()
    end = routedata['Destination'].strip()
    weight = round(float(routedata['distance_km'].strip()),2)
    # LOAD FOR AIRPORT
    found = gr.getEdge(analyzer['airports-dir'],start,end)
    if found == None:
        # THE ROUTE HAS NOT BEEN ADDED
        gr.addEdge(analyzer['airports-dir'],start,end,weight)
    # LOAD FOR CITY
    startobj = mp.get(analyzer['airports-map'],start)['value']
    endobj = mp.get(analyzer['airports-map'],end)['value']

    lat1 = startobj.lati
    lat2 = endobj.lati
    lon1 = startobj.long
    lon2 = endobj.long

    startcitylst = mp.get(analyzer['cities-map'],startobj.city)
    endcitylst = mp.get(analyzer['cities-map'],endobj.city)

    if startcitylst == None:
        # HASN'T BEEN ADDED
        lst = lt.newList()
        lt.addLast(lst,startobj)
        mp.put(analyzer['cities-map'],startobj.city,lst)
        gr.insertVertex(analyzer['cities-dir'],startobj.city)
        startcitylst = lst
    else:
        startcitylst = startcitylst['value']

    if endcitylst == None:
        # HASN'T BEEN ADDED
        lst = lt.newList()
        lt.addLast(lst,endobj)
        mp.put(analyzer['cities-map'],endobj.city,lst)
        gr.insertVertex(analyzer['cities-dir'],endobj.city)
        endcitylst = lst
    else:
        endcitylst = endcitylst['value']

    if lt.size(startcitylst) > 1:
        least = 99999999999999999
        best = None
        for cityobj in lt.iterator(startcitylst):
            lat = cityobj.lati
            lon = cityobj.long
            distance = haversine(lat1,lon1,lat,lon)
            if distance < least:
                least = distance
                best = cityobj
        startcity = best
    elif lt.size(startcitylst) == 1:
        startcity = lt.firstElement(startcitylst)

    if lt.size(endcitylst) > 1:
        least = 99999999999999999
        best = None
        for cityobj in lt.iterator(endcitylst):
            lat = cityobj.lati
            lon = cityobj.long
            distance = haversine(lat2,lon2,lat,lon)
            if distance < least:
                least = distance
                best = cityobj
        endcity = best
    elif lt.size(endcitylst) == 1:
        endcity = lt.firstElement(endcitylst)    

    found = gr.getEdge(analyzer['cities-dir'],startcity.city,endcity.city)
    if found == None:
        # THE ROUTE HAS NOT BEEN ADDED
        gr.addEdge(analyzer['cities-dir'],startcity.city,endcity.city,weight)

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
    elif iatai > iataj:
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
