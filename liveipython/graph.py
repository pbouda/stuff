# coding: utf-8
from PySide import QtDeclarative, QtGui
class Graph(QtDeclarative.QDeclarativeItem):
  def __init__(self, parent = None):
    QtDeclarative.QDeclarativeItem.__init__(self, parent)
    # need to disable this flag to draw inside a QDeclarativeItem
    self.setFlag(QtGui.QGraphicsItem.ItemHasNoContents, False)
    self.width = 0
    self.height = 0

  #This function creates the whole graph
  def paint(self, paint, options, widget):    
    global data
    global max_value

    self.width=800
    self.height=120
    
    paint.setRenderHints(QtGui.QPainter.Antialiasing, True);

    paint.setPen(QtGui.QColor("gray"))
    paint.setBrush(QtGui.QColor("black"))
    paint.setFont(QtGui.QFont('Decorative', 12))

    #show graph border, background
    paint.drawRect(0,0,self.width,2*self.height)           
    
    #Formating X axis
    #Small Y lines
    for i in range(self.height, 2*self.height, 10): 
        paint.drawLine(0,i,5,i) #1 line per degree
        paint.drawLine(0,2*self.height-i,5,2*self.height-i)
        paint.drawLine(self.width-5,i,self.width,i)
        paint.drawLine(self.width-5,2*self.height-i,self.width,2*self.height-i)

    #Big Y lines
    for i in range(self.height, 2*self.height, 50): 
        paint.drawLine(0,i,self.width,i) #line per degree
        paint.drawLine(0,2*self.height-i,self.width,2*self.height-i)
        paint.drawText(10, i-4, str((i-self.height)/10))
        paint.drawText(10, 2*self.height-i-4, str(-1*(i-self.height)/10))

    #Formating Y axis
    #Small X lines
    for i in range(self.width, 0, -40): 
        paint.drawLine(i,self.height-5,i,self.height+5)
      
    #Big X lines
    for i in range(0, self.width, 120): 
        paint.drawLine(self.width-i,self.height-20,self.width-i,self.height+20)
        if(i==0): j=i+25 
        else:j=i
        paint.drawText(self.width-j+5, self.height+20, str(i/4))

    #Zero line
    paint.setPen(QtGui.QColor("white"))
    paint.drawLine(0,self.height,self.width,self.height) 

    #Draw graph   
    for i in range(0,self.width-1):        
        idx = int((i/self.width)*len(data))
        value = data[idx]
        print len(data)
        print idx
      
        paint.setPen(QtGui.QColor("green"))
        paint.drawLine(self.width-1-i, 0, self.width-1-i+1, int((value/max_value)*self.height))
    
    #root.updateGraphWidth(self.width, 2*self.height) 