import config as cf
import model
import csv
import sys

# EMPTY 

global analyzer

def init():
  analyzer = model.init()
  return analyzer

# LOAD DATA

def loaddata():
  loadairports()
  loadcities()
  loadroutes()

def loadairports():
  filedir = cf.data_dir + 'Skylines/airports-utf8-small.csv'
  file = csv.DictReader(open(filedir, encoding='utf-8'))
  for airportdata in file:
    model.loadair(airportdata)

def loadcities():
  filedir = cf.data_dir + 'Skylines/worldcities-utf8.csv'
  file = csv.DictReader(open(filedir, encoding='utf-8'))
  for citydata in file:
    model.loadcity(citydata)

def loadroutes():
  filedir = cf.data_dir + 'Skylines/routes-utf8-small.csv'
  file = csv.DictReader(open(filedir, encoding='utf-8'))
  for routedata in file:
    model.loadroute(routedata)

# REQUIREMENTS

def req1():
  return model.req1()

def req2(code1,code2):
  return model.req2(code1,code2)

def req3(city1,city2,chosen):
  return model.req3(city1,city2,chosen)

def req4():
  return model.req4()

def req5():
  return model.req5()

def req6():
  return model.req6()

def req7():
  return model.req7()