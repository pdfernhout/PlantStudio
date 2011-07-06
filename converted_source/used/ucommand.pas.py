# unit Ucommand

from conversion_common import *
import updcom
import umain
import usupport
import ucollect
import delphi_compatability

# enumerated type TrackPhase
class TrackPhase:
    trackPress, trackMove, trackRelease = range(3)

# const
kMaxDescriptionLength = 40

def limitDescription(description):
    result = ""
    result = description
    if len(description) > kMaxDescriptionLength:
        result = UNRESOLVED.copy(description, 1, kMaxDescriptionLength - 4) + " ..."
    return result

# const
kMinMoveDistance = 2

class PdCommand(TObject):
    def __init__(self):
        self.canUndo = false
        self.done = false
        self.commandChangesPlantFile = false
        self.plantFileChangedBeforeCommand = false
    
    def create(self):
        TObject.create(self)
        self.canUndo = true
        self.done = false
        # default commandChangesPlantFile to true, since most commands change file,
        #    if command does not change file, set to false after call to inherited create 
        self.commandChangesPlantFile = true
        self.plantFileChangedBeforeCommand = false
        return self
    
    def destroy(self):
        #sublass could override
        TObject.destroy(self)
    
    def doCommand(self):
        self.done = true
        if self.commandChangesPlantFile:
            self.plantFileChangedBeforeCommand = umain.plantFileChanged
            if umain.MainForm != None:
                umain.MainForm.setPlantFileChanged(true)
        #subclass should override and call inherited
    
    def undoCommand(self):
        self.done = false
        if self.commandChangesPlantFile:
            if umain.MainForm != None:
                umain.MainForm.setPlantFileChanged(self.plantFileChangedBeforeCommand)
        #sublass should override and call inherited
    
    def redoCommand(self):
        self.doCommand()
        #sublass may override and call inherited doCommand
    
    def description(self):
        result = ""
        result = "*command description*"
        return result
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        result = 0
        #subclasses may override but only if they keep copies of large objects
        return result
    
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        #sublasses should override if needed
        result = self
        return result
    
class PdCommandList(TObject):
    def __init__(self):
        self.commands = TListCollection()
        self.lastDoneCommandIndex = 0L
        self.undoLimit = 0L
        self.objectUndoLimit = 0L
        self.mouseCommand = PdCommand()
        self.anchorPoint = TPoint()
        self.previousPoint = TPoint()
        self.rightButtonDown = false
    
    #PdCommandList
    def create(self):
        TObject.create(self)
        self.commands = ucollect.TListCollection().Create()
        self.lastDoneCommandIndex = -1
        self.undoLimit = 50
        self.objectUndoLimit = 10
        return self
    
    def destroy(self):
        self.commands.free
        self.commands = None
        #if mouseCoOmmand <> nil then error condition - ignoring for now - not released
        #could only happend if quitting somehow in middle of action
        TObject.destroy(self)
    
    def command(self, index):
        result = PdCommand()
        result = PdCommand(self.commands.Items[index])
        return result
    
    def setNewUndoLimit(self, newLimit):
        if newLimit != self.undoLimit:
            self.undoLimit = newLimit
            self.freeCommandsAboveLimit(self.undoLimit)
    
    def setNewObjectUndoLimit(self, newObjectLimit):
        if newObjectLimit != self.objectUndoLimit:
            self.objectUndoLimit = newObjectLimit
            self.freeCommandsAboveObjectLimit(self.objectUndoLimit)
    
    #free any command more than the number passed in
    def freeCommandsAboveLimit(self, theLimit):
        theCommand = PdCommand()
        
        while (self.commands.Count > theLimit) and (self.commands.Count > 0):
            theCommand = self.command(0)
            self.commands.Delete(0)
            theCommand.free
            self.lastDoneCommandIndex -= 1
            if self.lastDoneCommandIndex < -1:
                self.lastDoneCommandIndex = -1
    
    def freeCommandsAboveObjectLimit(self, objectLimit):
        theCommand = PdCommand()
        objectCount = 0L
        
        objectCount = self.objectCountInCommandList()
        while (objectCount > objectLimit) and (self.commands.Count > 0):
            theCommand = self.command(0)
            self.commands.Delete(0)
            theCommand.free
            self.lastDoneCommandIndex -= 1
            if self.lastDoneCommandIndex < -1:
                self.lastDoneCommandIndex = -1
            objectCount = self.objectCountInCommandList()
    
    def objectCountInCommandList(self):
        result = 0L
        i = 0L
        
        result = 0
        if self.commands.Count <= 0:
            return result
        for i in range(0, self.commands.Count):
            result = result + self.command(i).numberOfStoredLargeObjects()
        return result
    
    def doCommand(self, newCommand):
        i = 0L
        theCommand = PdCommand()
        
        if self.isRedoEnabled():
            for i in range(self.commands.Count - 1, self.lastDoneCommandIndex + 1 + 1):
                #remove any extra commands after the current
                #do this first to free memory for command
                theCommand = self.command(i)
                self.commands.Delete(i)
                theCommand.free
        # first see if there are too many objects and if so, scroll them 
        self.freeCommandsAboveObjectLimit(self.objectUndoLimit - 1)
        #see if too many commands are stored and if so, scroll them
        self.freeCommandsAboveLimit(self.undoLimit - 1)
        #now do this command
        #may fail in which case won't add
        newCommand.doCommand()
        self.commands.Add(newCommand)
        self.lastDoneCommandIndex += 1
    
    #added nextMouseCommand in these three functions to deal with unhandled exceptions occurring
    #during mouse commands.  This way, the command will not be further processed.
    #This may occasionally leak - the mouse command should be the one responsible for freeing
    #itself and returning nil if a problem occurs
    #returns whether the command finished tracking without freeing itself
    def mouseDown(self, newCommand, point):
        result = false
        nextMouseCommand = PdCommand()
        
        result = false
        if self.mouseCommand != None:
            #check if need to clear mouse command
            self.mouseUp(Point)
        self.mouseCommand = None
        if newCommand != None:
            #save mouse command and start it
            self.anchorPoint = Point
            self.previousPoint = Point
            nextMouseCommand = newCommand
            self.mouseCommand = nextMouseCommand.TrackMouse(TrackPhase.trackPress, self.anchorPoint, self.previousPoint, Point, false, self.rightButtonDown)
            result = (self.mouseCommand != None)
        return result
    
    def mouseMove(self, point):
        nextMouseCommand = PdCommand()
        
        nextMouseCommand = self.mouseCommand
        self.mouseCommand = None
        if nextMouseCommand != None:
            self.mouseCommand = nextMouseCommand.TrackMouse(TrackPhase.trackMove, self.anchorPoint, self.previousPoint, Point, self.didMouseMove(Point), self.rightButtonDown)
        self.previousPoint = Point
    
    def mouseUp(self, point):
        nextMouseCommand = PdCommand()
        
        nextMouseCommand = self.mouseCommand
        self.mouseCommand = None
        if nextMouseCommand != None:
            nextMouseCommand = nextMouseCommand.TrackMouse(TrackPhase.trackRelease, self.anchorPoint, self.previousPoint, Point, self.didMouseMove(Point), self.rightButtonDown)
            if nextMouseCommand != None:
                self.doCommand(nextMouseCommand)
    
    def didMouseMove(self, point):
        result = false
        result = (abs(Point.x - self.anchorPoint.X) > kMinMoveDistance) or (abs(Point.y - self.anchorPoint.Y) > kMinMoveDistance)
        return result
    
    def isUndoEnabled(self):
        result = false
        result = self.lastDoneCommandIndex >= 0
        return result
    
    def isRedoEnabled(self):
        result = false
        result = self.lastDoneCommandIndex < (self.commands.Count - 1)
        return result
    
    def undoDescription(self):
        result = ""
        if self.lastDoneCommandIndex >= 0:
            result = self.command(self.lastDoneCommandIndex).description()
            result = limitDescription(result)
        else:
            result = ""
        return result
    
    def redoDescription(self):
        result = ""
        if self.lastDoneCommandIndex < (self.commands.Count - 1):
            result = self.command(self.lastDoneCommandIndex + 1).description()
            result = limitDescription(result)
        else:
            result = ""
        return result
    
    def undoLast(self):
        if self.lastDoneCommandIndex >= 0:
            self.command(self.lastDoneCommandIndex).undoCommand()
            self.lastDoneCommandIndex -= 1
    
    def redoLast(self):
        if self.lastDoneCommandIndex < (self.commands.Count - 1):
            self.command(self.lastDoneCommandIndex + 1).redoCommand()
            self.lastDoneCommandIndex += 1
    
    def fillListWithUndoableStrings(self, aList):
        i = 0
        
        if aList == None:
            return
        if self.lastDoneCommandIndex >= 0:
            for i in range(self.lastDoneCommandIndex, 0 + 1):
                aList.Add(usupport.capitalize(self.command(i).description()))
    
    def fillListWithRedoableStrings(self, aList):
        i = 0
        
        if aList == None:
            return
        if self.lastDoneCommandIndex < (self.commands.Count - 1):
            for i in range(self.lastDoneCommandIndex + 1, self.commands.Count):
                aList.Add(usupport.capitalize(self.command(i).description()))
    
    def lastCommandDone(self):
        result = PdCommand()
        result = None
        if self.lastDoneCommandIndex < (self.commands.Count - 1):
            result = self.command(self.lastDoneCommandIndex + 1)
        return result
    
    def removeCommand(self, aCommand):
        if aCommand.done:
            # assume this command has been undone previously 
            raise GeneralException.create("Problem: Command not undone; in PdCommandList.removeCommand.")
        self.commands.Remove(aCommand)
    
