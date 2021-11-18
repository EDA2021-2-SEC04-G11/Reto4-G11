import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
import time

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
  start_time = time.process_time()
  print('\n\n ... LOADING DATA ...\n\n')
  analyzer = init()
  loaddata(analyzer)
  print('\n\n ... DATA LOADED ...\n\n')
  stop_time = time.process_time()
  elapsed_time_mseg = round((stop_time - start_time)*1000,2)
  input('\nPRESS ENTER TO CONTINUE') 
  return analyzer

def init(): 
    return controller.init()

def loaddata(analyzer):
  controller.loaddata(analyzer)

def req1(analyzer):
  print('+-+-+-+-+-+-+-+-+ REQ 2 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req1(analyzer)
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req2(analyzer):
  print('+-+-+-+-+-+-+-+-+ REQ 2 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req2(analyzer)
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req3(analyzer):
  print('+-+-+-+-+-+-+-+-+ REQ 2 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req3(analyzer)
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req4(analyzer):
  print('+-+-+-+-+-+-+-+-+ REQ 2 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req4(analyzer)
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req5(analyzer):
  print('+-+-+-+-+-+-+-+-+ REQ 2 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req5(analyzer)
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req6(analyzer):
  print('+-+-+-+-+-+-+-+-+ REQ 2 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req6(analyzer)
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

def req7(analyzer):
  print('+-+-+-+-+-+-+-+-+ REQ 2 +-+-+-+-+-+-+-+-+\n')
  # INPUTS
  # DATA
  start_time = time.process_time()
  pack = controller.req7(analyzer)
  stop_time = time.process_time()
  timef = round((stop_time - start_time)*1000,2)
  # PRINT
  print(f"TIME REQUIRED : {timef}")

"""
Menu 
"""
analyzer = charge()
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
    req1(analyzer)
  elif option == 2:
    req2(analyzer)
  elif option == 3:
    req3(analyzer)
  elif option == 4:
    req4(analyzer)
  elif option == 5:
    req5(analyzer)
  elif option == 6:
    req6(analyzer)
  elif option == 7:
    req7(analyzer)
  elif option == 0:
    sys.exit(0)
  input('\nPRESS ENTER TO CONTINUE')
sys.exit(0)