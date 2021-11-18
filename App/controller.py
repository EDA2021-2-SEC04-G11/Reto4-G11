import config as cf
import model
import csv

# FILE:
#

# EMPTY analyzer

def init():
  return model.init()

# LOAD DATA

def loaddata(analyzer):
  loadairports(analyzer)

def loadairports(analyzer):
  filedir = cf.data_dir + 'Skylines/airports_full.csv'
  file = csv.DictReader(open(filedir, encoding='utf-8'))
  for test in file:
    pass

def loadroutes(analyzer):
  filedir = cf.data_dir + 'Skylines/routes_full.csv'
  file = csv.DictReader(open(filedir, encoding='utf-8'))
  for test in file:
    pass

def loadcities(analyzer):
  filedir = cf.data_dir + 'Skylines/worldcities_full.csv'
  file = csv.DictReader(open(filedir, encoding='utf-8'))
  for test in file:
    pass

# REQUIREMENTS

def req1(analyzer):
  return model.req1(analyzer)

def req2(analyzer):
  return model.req2(analyzer)

def req3(analyzer):
  return model.req3(analyzer)

def req4(analyzer):
  return model.req4(analyzer)

def req5(analyzer):
  return model.req5(analyzer)

def req6(analyzer):
  return model.req6(analyzer)

def req7(analyzer):
  return model.req7(analyzer)