#!/usr/bin/env python

#import pango
#import pangocairo
#import atk

import pygtk
pygtk.require('2.0')
import gtk
#import cairo
from gtk_helpers import *

import math

import uturtle
import gtkdrawingsurface
import delphi_compatability
import utdo

import uplant
import ucursor
    
class PlantDrawingArea(gtk.DrawingArea):
    def __init__(self, mouseDownMethod):
        gtk.DrawingArea.__init__(self)
        self.connect("expose_event", self.expose)
        self.connect("configure_event", self.configure)
        self.selectedCultivar = None
        self.plants = []
        if mouseDownMethod:
            self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.POINTER_MOTION_MASK)
            self.connect("button_press_event", mouseDownMethod)
            self.connect("motion_notify_event", self.trackMouseWithGlove)
        self.glove = gtk.Image()
        #self.glove.set_from_file("images/glove.png")
        self.glove.set_from_file("images/glove_with_seedpacket.png")
        self.gloveX = 100
        self.gloveY = 100
        #self.gloveOffsetX = 64
        #self.gloveOffsetY = 20
        self.gloveOffsetX = 79
        self.gloveOffsetY = 53  
        self.backingPixmap = None
        self.outOfDate = 1
        self.backgroundImage = gtk.gdk.pixbuf_new_from_file("images/chalk_garden.png")
        #self.backgroundImage = gtk.Image()
        #self.backgroundImage.set_from_file("images/chalk_garden.png")
        
    def configure(self, widget, event):
        x, y, width, height = widget.get_allocation()
        self.backingPixmap = gtk.gdk.Pixmap(widget.window, width, height)
        self.outOfDate = 1
        self.backingPixmap.widget = self.window
                     
    def expose(self, widget, event):
        x , y, width, height = event.area   
        gc = widget.window.new_gc()
        if self.outOfDate:
            ucursor.cursor_startWait()
            try:
                context = (self.backingPixmap, gc)
                if self.backgroundImage:
                     self.backingPixmap.draw_rectangle(widget.get_style().white_gc, True, 0, 0, width, height)
                     self.backingPixmap.draw_pixbuf(gc, self.backgroundImage, 0, 0, 0, 0)
                else:
                    self.backingPixmap.draw_rectangle(widget.get_style().white_gc, True, 0, 0, width, height) 
                self.draw(context, width, height)
            finally:
                ucursor.cursor_stopWait()
                self.outOfDate = 0

        widget.window.draw_drawable(gc, self.backingPixmap, x, y, x, y, width, height)
        widget.window.draw_pixbuf(gc, self.glove.get_pixbuf(), 0, 0, self.gloveX - self.gloveOffsetX, self.gloveY - self.gloveOffsetY)

    def draw(self, context, width, height):    
        turtle = uturtle.KfTurtle()
        turtle.drawingSurface = gtkdrawingsurface.GTKDrawingSurface()
        turtle.drawingSurface.setDrawingContext(context)
        turtle.drawOptions.drawStems = True
        turtle.drawOptions.draw3DObjects = True
        self.drawPlants(turtle, width, height)
       
    def drawPlants(self, turtle, width, height): 
        for plant in self.plants:
            turtle.reset()
            #turtle.xyz(width / 2, height - 50, 100)
            turtle.xyz(plant.x, plant.y, 100)
            #turtle.setScale_pixelsPerMm(0.5)
            turtle.setScale_pixelsPerMm(plant.drawingScale_PixelsPerMm)
            plant.turtle = turtle
            plant.draw()
            plant.turtle = None
            
    def trackMouseWithGlove(self, widget, event):
        self.gloveX = int(event.x)
        self.gloveY = int(event.y)
        InvalidateWidget(self)
        
    def setOutOfDate(self):
        self.outOfDate = 1
        InvalidateWidget(self)
        #Cursor_StartWait()
        #gobject.idle_add(newCommand.doCommand)
        #gobject.idle_add(Cursor_StopWait)
  
############################################################
    
class MainWindow:
    def __init__(self):
        self.plants = None
        
        self.window = MakeWindow("Garden Simulator for OLPC", 750, 500)
        
        hbox = MakeHorizontalBox(self.window)
        self.plantList = MakeList(hbox, "Plant name", self.selectionChanged)
        
        vbox = MakeVerticalBox(hbox)
        
        self.drawingArea = PlantDrawingArea(self.mouseDown)
        PackBox(vbox, self.drawingArea)
 
        hbox = MakeHorizontalBox(vbox)
        MakeButton(hbox, "=0", self.grow, -1)
        MakeButton(hbox, "+1", self.grow, 1)
        MakeButton(hbox, "+5", self.grow, 5)
        MakeButton(hbox, "+10", self.grow, 10)
        MakeButton(hbox, "+30", self.grow, 30)
        MakeButton(hbox, "+100", self.grow, 100)
                        
        hbox = MakeHorizontalBox(vbox)
        MakeButton(hbox, "Clear", self.clear, -8)
        #MakeButton(hbox, ">>", self.turn, 8)
        
        MakeButton(vbox, "Open library...", self.openLibrary)

        self.fileName = "test.pla"
        #self.fileName = "test tree.pla"
        #self.fileName = "Garden flowers.pla"
        #self.fileName = "Garden flowers.pla"
        plants = uplant.PlantLoader().loadPlantsFromFile(self.fileName, inPlantMover=1, justLoad=1)
        self.setPlantListContents(plants)
        
        ShowWindow(self.window)
        ucursor.windowsToWaitWith.append(self.window.window)
        
    def setPlantListContents(self, plants):
        self.plants = plants
        plantListContents = []
        for plant in self.plants:
            tuple = (plant.name, plant)
            plantListContents.append(tuple)
        FillList(self.plantList, plantListContents)  
        if self.plants:
            self.drawingArea.selectedCultivar = self.plants[0] 
        else:
             self.drawingArea.selectedCultivar = None
        self.drawingArea.setOutOfDate()
        
    def grow(self, widget, days):
        ucursor.cursor_startWait()
        try:
            for plant in self.drawingArea.plants:
                if days == -1:
                    plant.reset()
                else:
                    for day in range(days):
                        plant.nextDay()
        finally:
            ucursor.cursor_stopWait()
        self.drawingArea.setOutOfDate()
        
    def selectionChanged(self, widget):
        plant = GetListSelection(self.plantList, 1)
        self.drawingArea.selectedCultivar = plant
        #self.drawingArea.setOutOfDate()
            
    def openLibrary(self, widget):
        fileName = ChooseFile(self.window, "Plant files", ["*.pla"])
        if fileName == None:
            return
        print "Opening", fileName
        ucursor.cursor_startWait()
        try:
            plants = uplant.PlantLoader().loadPlantsFromFile(fileName, inPlantMover=1, justLoad=1)
            self.fileName = fileName
            self.setPlantListContents(plants)
        finally:
            ucursor.cursor_stopWait()
        #self.drawingArea.setOutOfDate()
        
    def mouseDown(self, widget, event):
        # GTK BUG __ SEEMS TO CALL THREE TIMES IF DOUBLE CLICK 9only last is double click)
        isDoubleClick = event.type == gtk.gdk._2BUTTON_PRESS
        if isDoubleClick:
            self.mouseDoubleClick(event)
            return
        x = event.x
        y = event.y
        if self.drawingArea.selectedCultivar:
            ucursor.cursor_startWait()
            try:
                newPlant = self.drawingArea.selectedCultivar.makeCopy()
                newPlant.x = x
                newPlant.y = y
                newPlant.setAge(1)
                newPlant.randomize()
                self.drawingArea.plants.append(newPlant)
                self.drawingArea.setOutOfDate()
            finally:
                ucursor.cursor_stopWait()     
                
    def clear(self, widget, event):  
        self.drawingArea.plants = []
        self.drawingArea.setOutOfDate()
               
def main(): 
    application = MainWindow()
    gtk.main()
    
if __name__ == "__main__":
    main()
    




