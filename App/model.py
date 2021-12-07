import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import edge as ed
from DISClib.DataStructures import bst
from DISClib.DataStructures import rbt
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT import graph as gr
from math import radians, cos, sin, asin, sqrt
import sys
assert cf

# ==============================
# DATA MODEL
# ==============================


global analyzer
analyzer = {}

class iatamodel:
    def __init__(self,pack) -> None:
        self.name = pack['Name'].strip()
        self.city = pack['City'].strip()
        self.country = pack['Country'].strip()
        self.code = pack['IATA'].strip()
        self.lati = round(float(pack['Latitude'].strip()),2)
        self.long = round(float(pack['Longitude'].strip()),2)
    def printmodel(self):
        divup = '_'*70+'_'*(len(self.city)+len(self.country)+len(str(self.lati))+len(str(self.long))+len(self.name))
        divdown = '-'*70+'-'*(len(self.city)+len(self.country)+len(str(self.lati))+len(str(self.long))+len(self.name))
        print(divup)
        print(f'| IATA: {self.code} | name: {self.name} | city: {self.city} | country: {self.country} | latitude: {self.lati} | longitude: {self.long} |')
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
        self.airport = None
        self.closestAirport()
    def printmodel(self):
        populationstr = '{:4e}'.format(self.population)
        divup = '_'*64+'_'*(len(self.city)+len(self.country)+len(str(self.lati))+len(str(self.long))+len(populationstr))
        divdown = '-'*64+'-'*(len(self.city)+len(self.country)+len(str(self.lati))+len(str(self.long))+len(populationstr))
        print(divup)
        print(f'| city: {self.city} | country: {self.country} | latitude: {self.lati} | longitude: {self.long} | population: {populationstr} |')
        print(divdown)

    def closestAirport(self):
        keylati = round((self.lati%10)/10)*10 + self.lati//10
        keylong = round((self.long%10)/10)*10 + self.long//10
        entrylati = mp.get(analyzer['airports-tree-lati'],keylati)
        entrylong = mp.get(analyzer['airports-tree-long'],keylong)

        if entrylati != None and entrylong != None:
            latilst = entrylati['value']
            longlst = entrylong['value']
            
            lowest = 9999999
            best = None

            for airport in lt.iterator(latilst):
                distance = haversine(self.lati,self.long,airport.lati,airport.long)
                if distance < lowest:
                    lowest = distance
                    best = airport
            for airport in lt.iterator(longlst):
                distance = haversine(self.lati,self.long,airport.lati,airport.long)
                if distance < lowest:
                    lowest = distance
                    best = airport
            self.airport = best
                    
# ==============================
# CHARGE DATA
# ==============================

def init():
    analyzer['airports-dir'] = gr.newGraph(datastructure='ADJ_LIST',directed=True, size=10700, comparefunction=cmpairport)
    analyzer['airports-nodir'] = gr.newGraph(datastructure='ADJ_LIST',directed=False, size=10700, comparefunction=cmpairport)
    analyzer['airports-map'] = mp.newMap(numelements=10700)
    analyzer['airports-tree-lati'] = mp.newMap(comparefunction=cmpairport)
    analyzer['airports-tree-long'] = mp.newMap(comparefunction=cmpairport)

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
    loadtree(iata)
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

def loadtree(airport):
    lati = airport.lati
    key = round((lati%10)/10)*10 + lati//10
    entry = mp.get(analyzer['airports-tree-lati'],key)
    if entry == None:
        lst = lt.newList()
        lt.addLast(lst,airport)
        mp.put(analyzer['airports-tree-lati'],key,lst)
    else:
        lst = entry['value']
        lt.addLast(lst,airport)

    long = airport.long
    key = round((long%10)/10)*10 + long//10
    entry = mp.get(analyzer['airports-tree-long'],key)
    if entry == None:
        lst = lt.newList()
        lt.addLast(lst,airport)
        mp.put(analyzer['airports-tree-long'],key,lst)
    else:
        lst = entry['value']
        lt.addLast(lst,airport)

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
    try:
        if iatai.code == iataj.code:
            return 0
        elif iatai.code > iatai.code:
            return 1
        return -1
    except:
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

def cmptop(i,j):
    if i == j:
        return 0
    if i[1] == j[1]:
        if i[0].code > j[0].code:
            return 1
        return -1
    if i[1] > j[1]:
        return -1
    return 1

def cmptree(i,j):
    if i == j:
        return 0
    if i > j:
        return -1
    return 1

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

def findAirport(city:citymodel):
    return city.closestAirport


# ==============================
# REQUIREMENTS
# ==============================

def req1():
    top = bst.newMap(cmptop)
    vertexlst = mp.keySet(analyzer['airports-map'])
    total = 0
    for vertex in lt.iterator(vertexlst):
        inbound = gr.indegree(analyzer['airports-dir'],vertex)
        outbound = gr.degree(analyzer['airports-dir'],vertex)
        count = outbound + inbound
        airport = me.getValue(mp.get(analyzer['airports-map'],vertex))
        bst.put(top,(airport,count,outbound,inbound),0)
        if count != 0:
            total += 1
    return bst.keySet(top),total

def req2(code1,code2):
    sccpack = scc.KosarajuSCC(analyzer['airports-dir'])
    return sccpack,scc.stronglyConnected(sccpack,code1,code2)

def req3(city1:str,city2:str,chosen: list):
    # chosen star value: (None,None)
    entry1 = mp.get(analyzer['cities']['map'],city1)
    entry2 = mp.get(analyzer['cities']['map'],city2)
    if entry1 == None or entry2 == None:   
        return False

    lst1 = me.getValue(entry1)['lst']
    lst2 = me.getValue(entry2)['lst']
    if chosen[0] == None or chosen[1] == None:
        return lst1,lst2

    city1 = lt.getElement(lst1,chosen[0])
    city2 = lt.getElement(lst2,chosen[1])
    search = djk.Dijkstra(analyzer['airports-dir'],city1.airport.code)
    cost = djk.distTo(search,city2.airport.code)

    pathstack = djk.pathTo(search,city2.airport.code)
    path = lt.newList()
    current = 0
    while current != None:
        current = pathstack.pop(pathstack)
        print(current)
        lt.addLast(path,current)
    sys.exit(0)
    stops = None
    return city1,city2,cost,path,stops

def req4(city, milles):
    #graph = djk.Dijkstra(None, city)
    pass

def req5(iata):
    lst = lt.newList()
    top = top = bst.newMap()
    if gr.containsVertex(analyzer['airports-nodir'], iata):
        edges = gr.adjacentEdges(analyzer['airports-dir'],iata)
        for edgefound in lt.iterator(edges):
            vertex = ed.other(edgefound,iata)
            lt.addLast(lst, vertex)
        
        first = lt.firstElement(lst)
        second = lt.getElement(lst, 1)
        third = lt.getElement(lst, 2)
        lastminus2 = lt.getElement(lst, len(lst)-2)        
        lastminus1 = lt.getElement(lst, len(lst)-1)        
        last = lt.lastElement(lst)        
        bst.put(top,(first,second,third,lastminus2,lastminus1,last),0)
    
        return len(lst), top
    else:
        return None

def req6():
    pass
def req7():
    pass
