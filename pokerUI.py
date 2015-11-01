#!/usr/bin/env python
# -*- coding: utf-8 -*-

# On importe Tkinter
from Tkinter import *
from pokerlib import *
import sys, Tkinter,os
sys.modules['tkinter'] = Tkinter
#from tkinter.Tk import *
import copy
import pickle

class scrollTxtArea:
    def __init__(self,root):
        frame=Frame(root)
        frame.pack()
        self.textPad(frame)
        return
 
    def textPad(self,frame):
        #add a frame and put a text area into it
        textPad=Frame(frame)
        self.text=Text(textPad,height=20,width=110)
         
        # add a vertical scroll bar to the text area
        scroll=Scrollbar(textPad)
        self.text.configure(yscrollcommand=scroll.set)
         
        #pack everything
        self.text.pack(side=LEFT)
        scroll.pack(side=RIGHT,fill=Y)
        scroll.pack(side=RIGHT)
        textPad.pack(side=TOP)
        return


class saveClass:
  def __init__(self):
    self.saves=[]
    self.savePosition=0
    self.stack=False
    
class UI(Tk):
  def __init__(self,window):
    self.w=window
    self.w.geometry("%sx%s+300+300"%(config.MAIN_WIDTH,config.MAIN_HEIGHT))

    self.topFrame=Frame(self.w,width=config.MAIN_WIDTH,height=500,borderwidth=1)
    self.topFrame.pack(fill=BOTH)
    self.tableFrame=Frame(self.w,width=config.MAIN_WIDTH,height=300,borderwidth=1,relief=RAISED)
    self.tableFrame.pack(fill=BOTH,expand=1)
    
    
    self.messageFrame=Frame(self.w,width=config.MAIN_WIDTH,height=100,borderwidth=1)
    self.messageFrame.pack(side="bottom")
    
    self.b2=Button(self.topFrame,text="Start default tournament",command=self.generateTournament)
    self.b2.pack(side="left")
    self.b3=Button(self.topFrame,text="Print tables",command=self.printTables)
    self.b3.pack(side="left")
    self.b4=Button(self.topFrame,text="Refresh tables",command=self.refreshTableButtons)
    self.b4.pack(side="left")
    self.undoButton=Button(self.topFrame,text="undo",command=self.undo)
    self.undoButton.pack(side="left")
    self.redoButton=Button(self.topFrame,text="redo",command=self.redo)
    self.redoButton.pack(side="left")
    
    self.b5=Button(self.topFrame,text="Save to file",command=self.saveToFile)
    self.b5.pack(side="left")

    
    self.tV=TableViewer(self)
    self.menuBar=Menu(self.w)
    self.fileMenu=Menu(self.menuBar,tearoff=0)
    self.fileMenu.add_command(label="Open...",command=self.loadFileWindow)
    self.fileMenu.add_command(label="Save...",command=self.saveFileWindow)
    self.menuBar.add_cascade(label="File",menu=self.fileMenu)
    self.w.config(menu=self.menuBar)
    
    self.textPad = scrollTxtArea(self.messageFrame)    
    self.t=[]
    self.saves=[[]]
    self.savePosition=0
    
    
    self.tableButtons=[]  
    self.fillTableFrame(self.tableFrame)    
    self.undoRedoColourUpdate()
    self.w.mainloop()
    
  def save(self):
    print "Saving"
    self.savePosition+=1
    print "Save position : %s"%self.savePosition
    for saved in self.saves[self.savePosition:]:
      self.saves.remove(saved)
    self.saves.append(copy.deepcopy(self.t))
    print "New save length : %s"%len(self.saves)
    self.undoRedoColourUpdate()
    print "%s"%self.saves
    
  def undo(self):
    if self.savePosition<1 :
      self.savePosition=0
      self.echo("Can't undo. First instance.")
    else:
      self.echo("Undo. New position : %s"% self.savePosition)
      self.savePosition-=1
      self.t = self.saves[self.savePosition]
      self.refreshMessage()
      self.refreshTableButtons()
      
  def redo(self):
    if self.savePosition<len(self.saves)-1:
      self.savePosition+=1
      self.t=self.saves[self.savePosition]
      self.refreshTableButtons()
      self.echo("Redo to position %s"%self.savePosition)
      print self.savePosition
      print len(self.saves)
    else:
      self.echo("Last instance. Can't redo.")
      print self.savePosition
      print len(self.saves)
    
    
  def fillTableFrame(self,f):
    buttonWidth=25
    buttonHeight=10
    self.nPlayerText=Label(f,text="")
    self.nPlayerText.pack(side="top",fill="both")
    f1=Frame(f)
    f1.pack(side="top")
    for tableId in range(0,4):
      b=Button(f1,text="Table %s \n Not initialized"%tableId,width=buttonWidth,height=buttonHeight)
      b.pack(side="left")
      self.tableButtons.append(b)
    f2=Frame(f)
    f2.pack(side="top")
    for tableId in range(4,8):
      b=Button(f2,text="Table %s \n Not initialized"%tableId,width=buttonWidth,height=buttonHeight)
      b.pack(side="left")
      self.tableButtons.append(b)
    f3=Frame(f,width=config.MAIN_WIDTH)
    f3.pack(side="top")
    for tableId in range(9,11):
      b=Button(f3,text="Table %s \n Not initialized"%tableId,width=buttonWidth,height=buttonHeight)
      b.pack(side="left")
      self.tableButtons.append(b)
    
    self.refreshTableButtons()
  
  def undoRedoColourUpdate(self):
    if self.savePosition<len(self.saves)-1:
      self.redoButton["foreground"]="black"
      self.redoButton["activeforeground"]="black"
    else:
      self.redoButton["foreground"]="grey"
      self.redoButton["activeforeground"]="grey"
    if self.savePosition>0:
      self.undoButton["foreground"]="black"
      self.undoButton["activeforeground"]="black"
    else:
      self.undoButton["foreground"]="grey"
      self.undoButton["activeforeground"]="grey"

  def saveToFile(self,filename='autosave.sav',stack=True):
    s=saveClass()
    s.saves=self.saves
    s.savePosition=self.savePosition
    s.stack=stack
    pickle.dump(s,open(filename,'wb'))
    self.echo("Saved %sto file (%s)"%("whole stack " if stack else "",filename))
    
  def loadFromFile(self,filename='autosave.sav'):
    s=saveClass()
    s = pickle.load( open( filename, "rb" ) )
    if s.stack:
      self.saves=s.saves
      self.savePosition=s.savePosition
      self.t=s.saves[self.savePosition]
    self.echo("Loaded from file (%s)"%filename)
    self.refreshTableButtons()
  
  def refreshTableButtons(self):
    self.undoRedoColourUpdate()
    self.refreshMessage()

    bv=self.tableButtons
    txt=""
    if type(self.t)==list:
      self.nPlayerText["text"]="No tournament loaded"
    else:
      self.nPlayerText["text"]="Total number of player = %s"%len(self.t.playerList)

    for i in range(len(bv)):
      if type(self.t)==list:
	txt="Table %s \n Tournament not loaded"%i
	c=lambda :self.echo("No tournament loaded")
      else:
	table=None
	for t in self.t.tables:
	  if t.id==i:
	    table=t
	if not table:
	  txt="Table %s \n No such table."%i
	  c=lambda :self.echo("No such table")
	else:
	  txt="Table %s (%s):"%(table.id,len(table.players))
	  for p in table.players:
	    txt+=("\n%s : %s (%s)"%(p.id,p.name,p.nMoves))
	  c=lambda t=table: self.tV.loadTable(t)
      bv[i]["text"]=txt
      bv[i]["command"]=c
      
  def loadFileWindow(self):
    self.loadWindow=Tk()
    #self.loadWindow.geometry("%sx%s+300+300"%(300,100))
    txt=Label(self.loadWindow,width=10,text="Open file :")
    txt.pack(side="top")
    f=Frame(self.loadWindow)
    txt=Label(f,text="Name list :")
    txt.pack(side="left",fill=X)
    f.pack(side="top",fill=X)
    f=Frame(self.loadWindow)
    nameWidget = Entry(f,width=30)
    nameWidget.insert(0,config.DEFAULT_FILE)
    nameWidget.pack(side="left")
    c=lambda: self.generateTournament(nameWidget.get())
    b = Button(f,text="ok",command=c)
    b.pack(side="left")
    f.pack(side="top",fill=X)
    f=Frame(self.loadWindow)
    txt=Label(f,text="Save file :")
    txt.pack(side="left",fill=X)
    f.pack(side="top",fill=X)
    f=Frame(self.loadWindow)
    saveWidget = Entry(f,width=30)
    saveWidget.insert(0,config.DEFAULT_SAVE)
    saveWidget.pack(side="left")
    c2=lambda: self.loadState(saveWidget.get())
    b = Button(f,text="ok",command=c2)
    b.pack(side="left")
    f.pack(side="top",fill=X)
    
  def saveFileWindow(self):
    self.saveWindow=Tk()
    #self.loadWindow.geometry("%sx%s+300+300"%(300,100))
    txt=Label(self.saveWindow,width=10,text="Save to file :")
    txt.pack(side="top")
    f=Frame(self.saveWindow)
    txt=Label(f,text="Name list :")
    txt.pack(side="left",fill=X)
    f.pack(side="top",fill=X)
    f=Frame(self.saveWindow)
    nameWidget = Entry(f,width=30)
    nameWidget.insert(0,config.DEFAULT_FILE)
    nameWidget.pack(side="left")
    c=lambda: self.savePlayerList(nameWidget.get())
    b = Button(f,text="ok",command=c)
    b.pack(side="left")
    f.pack(side="top",fill=X)
    f=Frame(self.saveWindow)
    txt=Label(f,text="Save file :")
    txt.pack(side="left",fill=X)
    f.pack(side="top",fill=X)
    f=Frame(self.saveWindow)
    saveWidget = Entry(f,width=30)
    saveWidget.insert(0,config.DEFAULT_SAVE)
    saveWidget.pack(side="left")
    c2=lambda: self.saveToFile(saveWidget.get())
    b = Button(f,text="ok",command=c2)
    b.pack(side="left")
    f.pack(side="top",fill=X)
  
  def savePlayerList(self,sName="data/liste.txt"):
    if type(self.t)==list:
      self.echo("No tournament to save!")
    elif not os.path.isdir("./"+sName[:-len(sName.split("/")[-1])]):
      self.echo("%s not a directory!"%("./"+sName[:-len(sName.split("/")[-1])]))
    else:
      self.echo("Saving to %s..."%sName)
    toSave=""
    for i in range(len(self.t.playerList)):
      toSave+="%s\t%s\n"%(i+1,self.t.playerList[i].name)
    with open(sName,"w") as f:
      f.write(toSave)
  def echo(self,message):
    if "__POPUP__" in message[:9]:
      message=message.replace("__POPUP__","")
      if config.POPUP:
	self.popup(message)
    self.textPad.text.insert(1.0,message+'\n')
    
  def popup(self,message = "Error, no message specified"):
    popupWindow=Tk()
    txt=Label(popupWindow,text=message,fg="red",font=("Helvetica", 20))
    txt.pack(side="top")
    c=lambda: popupWindow.destroy()
    b = Button(popupWindow,text="ok",command=c)
    b.pack(side="top")

  def refreshMessage(self):
    if not type(self.t)==list:
      messageList=self.t.message
      for m in messageList:
	self.echo(m+'\n')
      self.t.message=[]
      
  def loadState(self,sName="data/save.sav"):
    self.b2.pack_forget()
    self.loadFromFile(sName)
    #self.save()
    #self.t=tournoi()
    #self.t.loadState(sName)
    #self.t.generateTables()
    #self.b2.pack_forget()
    #self.refreshTableButtons()

  def generateTournament(self,fName="data/liste.txt"):
    self.t=tournoi()
    self.t.loadList(fName)
    self.t.generateTables()
    self.b2.pack_forget()
    self.refreshTableButtons()
    self.save()
    
  def showTableWindow(self,id=-1):   
    if type(self.t)==list:
      self.echo("ERROR, tournament not initialized yet !")
    else:
      self.tV.loadTable(self.t.tables[0])
  def printTables(self):
    if type(self.t)==list:
      self.echo("ERROR, tournament not initialized yet !")
    else:
      print self.t.printTables()
      self.echo(self.t.printTables())
      
      
      
class TableViewer():
  def __init__(self,master):
    self.master=master
        
    self.root=None
    self.f=None
    self.mainFrame=None
    
    self.pFrames=[]
    self.table=None
    
  def loadTable(self,t):
      self.master.echo("Loaded table %s"%t)
      self.table=t
      self.drawTable()
      
  def drawTable(self):
    try:
      assert self.root.state()=='normal'
      self.mainFrame.pack_forget()
      self.mainFrame=Frame(self.root)
      #self.root.lift()
      #self.root.attributes('-topmost', 1)
      #self.root.attributes('-topmost', 0)
      #print "try done correctly"
      #self.root.destroy()
    except:
      try:
	self.root.destroy()
      except:
	pass
      self.root=Tk()
      self.root.geometry=("%sx%s+300+300"%(config.TABLE_WIDTH,config.TABLE_HEIGHT))
      self.mainFrame=Frame(self.root)
    
    self.pFrames=[]  
    if not self.table:
      self.master.echo("Error, no table loaded.")
      return ()
    
    
    #Check if table exists:
    tExists=False
    for tab in self.master.t.tables:
      if self.table.id == tab.id:
	tExists=True
	break
    if  not tExists:
      f=Frame(self.mainFrame)
      x=Label(f,text="Table no longer existing.")
      x.pack(side="left")
      b1=Button(self.mainFrame,text="Close",command=self.root.destroy)
      b1.pack(side="top")
      f.pack(side="bottom")
    else:
      f=Frame(self.mainFrame)
      self.f=f
      x=Label(f,text="Table %s (%s players)"%(self.table.id,len(self.table.players)))
      x.pack()
      f.pack(side="top",expand=1,fill=X)
      for p in self.table.players:
	f=Frame(self.mainFrame)
	x=Label(f,text="%s - %s"%(p.id,p.name),width=30)
	x.pack(side="left",fill=X)
	c=lambda pl=p:self.delPlayer(pl)
	b1=Button(f,text="Remove",command=c)
	b1.pack(side="left")
	
	options=[" "]
	default=StringVar(f)
	default.set(options[0])
	c2=lambda var=default,pl=p.id:self.movePlayer(var,pl)
	b2=Button(f,text="Move to table",command=c2)
	for table in self.master.t.tables:
	  if len(table.players)<config.MAX_PER_TABLE:
	    options.append("%s"%table.id)
	l = apply(OptionMenu, (f, default) + tuple(options))
	b2.pack(side="left")
	l.pack(side="left")
	f.pack(side="top")
	self.pFrames.append(f)
      if len(self.table.players)<config.MAX_TO_ADD:
	f=Frame(self.mainFrame)
	c=lambda table=self.table.id:self.addPlayerWin(table)
	b=Button(f,text="Add player",command=c)
	b.pack(side="top")
	f.pack(side="top")
    self.mainFrame.pack()
    
  def addPlayerWin(self,table=0):
    self.addPlayerWindow=Tk()
    txt=Label(self.addPlayerWindow,width=10,text="Add player to table %s:"%table)
    txt.pack(side="top")
    f=Frame(self.addPlayerWindow)
    txt=Label(f,text="Player name :")
    txt.pack(side="left",fill=X)
    f.pack(side="top",fill=X)
    f=Frame(self.addPlayerWindow)
    nameWidget = Entry(f,width=30)
    nameWidget.insert(0,"Herp Derp")
    nameWidget.pack(side="left")
    c=lambda: self.addPlayer(addPlayerWindow=self.addPlayerWindow,name=nameWidget.get(),table=table)
    b = Button(f,text="ok",command=c)
    b.pack(side="left")
    f.pack(side="top",fill=X)
    
  def addPlayer(self,addPlayerWindow,name,table):
    self.master.t.addPlayer(name=name,table=table,initial=False)
    self.master.refreshTableButtons()
    addPlayerWindow.destroy()
    for t in self.master.t.tables:
      if t.id==table:
	self.loadTable(t)
	break
    
  def movePlayer(self,variable,playerId):
    if not variable.get()=="":
      destNum=int(variable.get())
      self.master.t.movePlayer(playerId,variable.get())
      self.master.save()
    else:
      self.master.echo("No table selected.")
    self.drawTable()
    self.master.refreshTableButtons()
    
  def delPlayer(self,p):
    self.master.t.removePlayer(p.id)
    self.master.save()
    self.drawTable()
    self.master.refreshTableButtons()
if __name__=="__main__":
  u=UI(Tk())
  

