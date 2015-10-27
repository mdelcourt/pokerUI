#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, random,pickle,datetime
import config
from copy import *

class player:
  def __init__(self,id=-1,name="unnamed"):
    self.id=int(id)
    self.table=-1
    self.name=name
    #self.lastMove=-1
    self.nMoves=0
    
class table:
  def __init__(self,id=-1):
    self.id=id
    self.players=[]
    
  def getTotalMoves(self):
    totalMoves=0
    for p in self.players:
      totalMoves+=p.nMoves
    return(totalMoves)
    
  def removePlayer(self,toRemove):
    for p in self.players:
      if p.id==toRemove.id:
	self.players.remove(p)
  def addPlayer(self,p):
    self.players.append(p)
  
class tournoi:
  def __init__(self):
    assert not config.MIN_MOVE_ON_DEL or not config.MIN_MOVE_ON_DEL == config.MIN_MAX_ON_DEL, "Can't have MIN_MOVE_ON_DEL and MIN_MAX_ON_DEL set at the same time."
    self.tables=[]
    self.playerList=[]
    self.nextId=-1
    
    self.message=[]
    
    self.tablesBackup=[]
    self.playerListBackup=[]
  def getPlayerById(self,id=-1):
    for p in self.playerList:
      if p.id==id:
	return(p)
    return(None)
  def printTables(self):
    txt=""
    if config.UI==True:
      return()
    else:
      for t in self.tables:
	txt+="#### Table %s : %s players ####\n"%(t.id,len(t.players))
	for p in t.players:
	    txt+="%s - %s (%s moves)\n"%(p.id,p.name,p.nMoves)
    if not config.SILENT:
      print txt
    #self.message.append(txt)
    return txt
  
  def printPlayers(self):
    self.message.append("#### Player list ####")
    if not config.SILENT:
      print "#### Player list ####"
    for p in self.playerList:
	self.message.append("%s - %s (%s moves)"%(p.id,p.name,p.nMoves))
	if not config.SILENT:
	  print "%s - %s (%s moves)"%(p.id,p.name,p.nMoves)
      
  def tSave(self):
    if config.UI:
      return 0
    self.tablesBackup=deepcopy(self.tables)
    self.playerListBackup=deepcopy(self.playerList)

       
  def loadList(self,filename):
     """loads list of players from file 'filename' """
     folderName=""
     for folder in filename.split("/")[:-1]:
       folderName+=folder+"/"
     if folderName=="":
       folderName="."
     txt=""
     if not filename.split("/")[-1] in os.listdir(folderName):
       self.message.append("Error: file %s not found!"%filename)
       return(-1)
     else:
       self.tSave()
       self.playerList=[]
       self.tables=[]
       self.nextId=0
       myFile=open(filename,"r")
       content=myFile.read()
       content=content.split('\n')
       for line in content:
	 if not config.SILENT:
	  print "-%s-"%line
	 if len(line.split("	"))==2:
	   p=player(line.split("	")[0],line.split("	")[1])
	   self.playerList.append(p)
	#Generates self.nextId
       for p in self.playerList:
	 if p.id>=self.nextId:
	   self.nextId=p.id+1
       #print self.nextId
	 #TODO List with only names
       myFile.close()
       return(1)

  def generateTables(self):
    nTables=1
    PlayPerTable=len(self.playerList)
    while PlayPerTable>config.MAX_PER_TABLE and nTables<config.MAX_TABLE:
      nTables+=1
      PlayPerTable=len(self.playerList)*1./nTables
    #nTables=int((len(self.playerList)/config.maxPlayer-0.1))+1
    #PlayPerTable=len(self.pList)/nTables
    self.message.append("Nombre de joueurs: %s et nombre de tables: %s => nombre de joueurs par table: %s"%(len(self.playerList),nTables,PlayPerTable))
    if not config.SILENT:
      print "Nombre de joueurs: %s et nombre de tables: %s => nombre de joueurs par table: %s"%(len(self.playerList),nTables,PlayPerTable)
    self.tables=[]
    playToAssign=copy(self.playerList)
    for i in range(nTables):
      t=table(i)
      for j in range(int(PlayPerTable)):
	player=random.choice(playToAssign)
	t.addPlayer(player)
	playToAssign.remove(player)
      self.tables.append(t)
    for player in playToAssign:
      loopBreak=0
      while loopBreak<1000:
	loopBreak+=1
	candidat=random.choice(self.tables)
	if not len(candidat.players)>PlayPerTable:
	  candidat.addPlayer(player)
	  playToAssign.remove(player)
	  break
      if loopBreak>900:
	if not config.SILENT:
	  print "ERROR, loopBreak too big!"
      self.printTables()
     
     
   
  def equi(self):
    #Get number of tables that should exist
    nTables=1
    PlayPerTable=len(self.playerList)
    while PlayPerTable>config.MAX_PER_TABLE:
      nTables+=1
      PlayPerTable=len(self.playerList)*1./nTables
    
    if len(self.tables)>nTables:
      #print "DEBUG REMOVING A TABLE"
      shortest=[]
      shLen=10
      for table in self.tables:
	if len(table.players)<shLen:
	  shortest.append(table)
	  shLen=len(table.players)
      #print "DEBUG  : shortest tables : %s (len = %s)"%(shortest,shLen)
      
      if config.SOFT_SEL_ON_DEL:
	avail=shortest
      else:
	avail=self.tables
	
      if config.MIN_MOVE_ON_DEL:
	#print "DEBUG : MIN_MOVE_ON_DEL is TRUE"
	minMoves=1000
	minMoveTables=[]
	for t in avail:
	  if t.getTotalMoves() < minMoves:
	    minMoves=t.getTotalMoves()
	for t in avail:
	  if t.getTotalMoves() == minMoves:
	    minMoveTables.append(t)
	#print "DEBUG : MIN_MOVE TABLES : %s with %s moves"%(minMoveTables,minMoves)
	toRemove=random.choice(minMoveTables)
	print "Chose to remove table %s"%toRemove
      elif config.MIN_MAX_ON_DEL:
	minMax=1000
	minMaxTables=[]
	for t in avail:
	  tMax=-1
	  for p in t.players:
	    if p.nMoves>tMax:
	      tMax=p.nMoves
	  if tMax<minMax:
	    minMax=tMax
	#print minMax
	for t in avail:
	  tMax=-1
	  for p in t.players:
	    if p.nMoves>tMax:
	      tMax=p.nMoves
	  if tMax==minMax:
	    minMaxTables.append(t)
	finalSelection=[]
	#print "DEBUG : MIN_MAX tables :%s with max = %s"%(minMaxTables,minMax)
	minTotMoves=1000
	#print len(minMaxTables)
	for t in minMaxTables:
	  if t.getTotalMoves() <minTotMoves:
	    minTotMoves=t.getTotalMoves()
	for t in minMaxTables:
	  if t.getTotalMoves()==minTotMoves:
	    finalSelection.append(t)
	#print "DEBUG : FINAL SELECTION :%s with total moves= %s"%(minMax,minTotMoves)
	toRemove=random.choice(finalSelection)
      else:
	#print "DEBUG : NO DEL FLAG -> RANDOM FROM SHORTEST TABLES"
	toRemove=random.choice(shortest)
      self.tables.remove(toRemove)
      txt="Removed table %s "%toRemove.id
      
      for player in toRemove.players:
	loopBreak=0
	while loopBreak<1000:
	  candi=random.choice(self.tables)
	  if len(candi.players)<PlayPerTable:
	    candi.addPlayer(player)
	    txt+=("\n %s moved to table %s"%(player.name,candi.id))
	    player.nMoves+=1
	    break
	if loopBreak>950:
	  self.message.append( "Error, loopBreak too big!")
	  if not config.SILENT:
	    print "Error, loopBreak too big!"
      if not config.SILENT:
	print txt
      self.message.append(txt)
      if not config.SILENT:
	print "New table arrangement:"
	self.printTables()
    else:
      #If appropriate amount of tables, equilibrates players
      shortest=[]
      shLen=10
      shNum=-1
      for table in self.tables:
	if len(table.players)<shLen:
	  shLen=len(table.players)
	  shNum=table.id
      for table in self.tables:
	if len(table.players)==shLen:
	  shortest.append(table)
      
      
      longest=[]
      lgLen=-1
      lgNum=-1
      for table in self.tables:
	if len(table.players)>lgLen:
	  lgLen=len(table.players)
	  lgNum=table.id
      for table in self.tables:
	if len(table.players)==lgLen:
	  longest.append(table)
      
      maxdiff = config.MAX_DIFF_gt_6 if PlayPerTable>6 else config.MAX_DIFF_lt_6
      if lgLen-shLen>maxdiff:
	#print "DEBUG : lgLen = %s, shLen  = %s , maxdiff = %s -> MOVE A PLAYER"%(lgLen,shLen,maxdiff)
	tableTo=random.choice(shortest)
	#print "DEBUG : WILL MOVE TO TABLE %s"%tableTo
	#Necessary to move a player.
	if config.GLOBAL_MIN_MOVE:
	  #print "DEBUG : FOUND GLOBAL_MIN_MOVE FLAG"
	  if config.SOFT_GLMM_SEL:
	    avail=longest
	  else:
	    avail=self.tables

	  globalMinMove=1000
	  toMoveCandi=[]
	  for t in avail:
	    if t == tableTo:
	      continue
	    for p in t.players:
	      if p.nMoves<globalMinMove:
		globalMinMove=p.nMoves
	  #print "DEBUG : MIN OF MOVES : %s"%globalMinMove
	  for t in avail:
	    if t == tableTo:
	      continue
	    for p in t.players:
	      if p.nMoves==globalMinMove:
		toMoveCandi.append(t)
		break
	  #print globalMinMove
	  #print "DEBUG : CANDIDATES : %s "%toMoveCandi
	  tableFrom=random.choice(toMoveCandi)
	else:
	  tableFrom=random.choice(longest)
	
	toMove=[]
	if config.MIN_MOVE:
	  #print "DEBUG : FOUND FLAG MIN_MOVE"
	  minMove=1000
	  for p in tableFrom.players:
	    if p.nMoves<minMove:
	      minMove=p.nMoves
	  #print "DEBUG : MIN_MOVE ON TABLE IS %s"%minMove
	  candidates=[]
	  for p in tableFrom.players:
	    if p.nMoves==minMove:
	      candidates.append(p)
	  #print "DEBUG : FINAL SELECTION : %s"%candidates
	  toMove=random.choice(candidates)
	else:
	  toMove=random.choice(tableFrom.players)
	
	if tableFrom==tableTo:
	  print "ERROR, TABLE FROM AND TABLE TO IS THE SAME"
	  if self.equi_loopbreak<1000:
	    self.equi_loopbreak+=1
	    self.equi()
	  else:
	    self.equi_loopbreak=0
	else:
	  tableFrom.players.remove(toMove)
	  tableTo.players.append(toMove)
	  toMove.nMoves+=1
	  if not config.SILENT:
	    print "Moved %s from table %s to %s"%(toMove.name,tableFrom.id,tableTo.id)
	  self.message.append("Moved %s from table %s to %s"%(toMove.name,tableFrom.id,tableTo.id))
    
  def removePlayer(self,playerId):
    self.tSave()
    found=False
    toReturn=1
    for p in self.playerList:
      if p.id==playerId:
	self.playerList.remove(p)
	found=True
	self.message.append("Removed player %s (%s) from player list"%(p.id,p.name))
	if not config.SILENT:
	  print "Removed player %s (%s) from player list"%(p.id,p.name)
    if not found:
      self.message.append("Error, unable to find player %s in player list"%playerId)
      if not config.SILENT:
	print "Error, unable to find player %s in player list"%playerId
      toReturn = -1
    found=False
    for t in self.tables:
      for p in t.players:
	if p.id==playerId:
	  t.removePlayer(p)
	  found=True
    if not found:
      self.message.append("Error, unable to find player in table list")
      if not config.SILENT:
	print "Error, unable to find player in table list"
      toReturn=-1
    if config.autoEqui==True:
      self.equi()
    return(toReturn)
     
     
  def saveState(self,message="auto"):
    #TODO
    print "Not implemented."
  
  def loadState(self,fileName=config.DEFAULT_SAVE):
    #TODO
    print "Not implemented. will load : @%s@"%fileName
    pass
  
  def undo(self):
    self.tables=deepcopy(self.tablesBackup)
    self.playerList=deepcopy(self.playerListBackup)
    
  
  def addPlayer(self,name="unNamed",table=-1,initial=False):
    p=player(self.nextId,name)
    self.nextId+=1
    self.playerList.append(p)
    if table<0:
      if config.autoEqui:
	self.equi()
    else:
      foundTable=False
      for t in self.tables:
	if t.id==table and not foundTable:
	  t.addPlayer(p)
	  foundTable=True
      if not foundTable:
	self.message.append("Error, table %s not found !"%table)
	if not config.SILENT:
	  print "Error, table %s not found !"%table
	#TODO handle new table creation
	
  def movePlayer(self,id=-1,tableId=-1):
    
    tableTo=None
    player=None
    tableFrom=None
    reason=""
    
    for t in self.tables:
      if t.id==int(tableId):
	if len(t.players)<config.MAX_PER_TABLE:
	  tableTo=t
	else:
	  reason+=" Table %s too full"%t.id
      for p in t.players:
	if p.id==id:
	  tableFrom=t
	  player=p
    try:
      tableFrom.players.remove(player)
      tableTo.players.append(player)
      txt="Moved player %s from table %s to table %s"%(player.name,tableFrom.id,tableTo.id)
      self.message.append(txt)
      if not config.SILENT:
	print txt
    except:
      print tableTo
      print tableFrom
      print player
      if not tableFrom:
	reason+=" Can't find origin table"
      if not player:
	reason+=" Can't find player"
      txt="Can't move player num %s to table %s %s"%(id,tableId,reason)
      self.message.append(txt)
      if not config.SILENT:
	print txt
	
	
	
	
    pass