import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
import os
assert cf
import time

global analyzer

def printMenu():
    print("<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>")
    print("Welcome")
    print("1- REQ 1")
    print("2- REQ 2")
    print("3- REQ 3")
    print("4- REQ 4")
    print("5- REQ 5")
    print("6- REQ 6")
    print("7- REQ 7")
    print("0- EXIT")

def charge():
  clear()
  start_time = time.process_time()
  print('\n\n ... LOADING DATA ...\n\n')
  analyzer = init()
  loaddata()
  print('\n\n ... DATA LOADED ...\n\n')
  stop_time = time.process_time()
  elapsed_time_mseg = round((stop_time - start_time)*1000,2)
  exhibition(analyzer)
  input('\nPRESS ENTER TO CONTINUE')
  clear()
  return analyzer

def init(): 
  analyzer = controller.init()
  return analyzer

def loaddata():
  controller.loaddata()

def exhibition(analyzer):
  print('\n\n')
  print("== Airports-Routes Digraph ==")
  print(f"Total airports: {gr.numVertices(analyzer['airports-dir'])}")
  print(f"Total of airport edges: {gr.numEdges(analyzer['airports-dir'])}")
  print('First and last airport loaded:')
  for i in lt.iterator(analyzer['exhibition']['airports-dir']):
    i.printmodel()

  print('\n\n')
  print("== Airports-Routes Graph ==")
  print(f"Total airports: {gr.numVertices(analyzer['airports-nodir'])}")
  print(f"Total of airport edges: {gr.numEdges(analyzer['airports-nodir'])}")
  print('First and last airport loaded:')
  for i in lt.iterator(analyzer['exhibition']['airports-nodir']):
    i.printmodel()

  print('\n\n')
  print("== City network ==")
  print(f"Total cities: {analyzer['cities']['count']}")
  print('First and last city loaded:')
  for i in lt.iterator(analyzer['exhibition']['cities']):
    i.printmodel()

def req1():
  print('+-+-+-+-+-+-+-+-+ REQ 1 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req1()
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req2():
  print('+-+-+-+-+-+-+-+-+ REQ 2 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req2()
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req3():
  print('+-+-+-+-+-+-+-+-+ REQ 3 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req3()
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req4():
  print('+-+-+-+-+-+-+-+-+ REQ 4 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req4()
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req5():
  print('+-+-+-+-+-+-+-+-+ REQ 5 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req5()
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req6():
  print('+-+-+-+-+-+-+-+-+ REQ 6 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req6()
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req7():
  print('+-+-+-+-+-+-+-+-+ REQ 7 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req7()
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

"""
Menu 
"""
clear = lambda: os.system('cls')
charge()
while True:
  printMenu()
  while True:
    try:
      option = int(input('Choose an option to continue\n').strip()[0])
      print('<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>')
      break
    except:
      continue
  if option == 1:
    req1()
  elif option == 2:
    req2()
  elif option == 3:
    req3()
  elif option == 4:
    req4()
  elif option == 5:
    req5()
  elif option == 6:
    req6()
  elif option == 7:
    req7()
  elif option == 0:
    sys.exit(0)
  input('\nPRESS ENTER TO CONTINUE')
  clear()
  #print('\n'*5)
sys.exit(0)