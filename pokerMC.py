"""This function computes the number of moves and maximum number of moves for random tournaments.
Uses the ROOT library."""

from ROOT import *
import config
import pokerlib
from random import choice


config.UI=False
config.SWAP=False

nMoves = TH1I("nMoves","nMoves",20,0,20)
hMaxMoves= TH1I("nMaxMoves","nMaxMoves",20,0,20)
nTries = 1000
nPlayer = 7*9
for i in range(nTries):
  print i
  nMaxMoves=0
  t=pokerlib.tournoi()
  for i in range(nPlayer):
    t.addPlayer(initial=True)
  t.generateTables()
  #for p in t.playerList:
    #print "%s - %s"%(p.id,p.name)

  for i in range(nPlayer):
    p=choice(t.playerList)
    nMoves.Fill(p.nMoves)
    if (p.nMoves>nMaxMoves):
      nMaxMoves=p.nMoves
    t.removePlayer(p.id)
  hMaxMoves.Fill(nMaxMoves)

c=TCanvas()  
nMoves.Draw()
c2=TCanvas()
hMaxMoves.Draw()
