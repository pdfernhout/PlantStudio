// unit Ucommand

from conversion_common import *;
import updcom;
import umain;
import usupport;
import ucollect;
import delphi_compatability;

// FIX enumerated type TrackPhase
class TrackPhase:
    trackPress, trackMove, trackRelease = range(3)


// const
kMaxDescriptionLength = 40;


public String limitDescription(String description) {
    result = "";
    result = description;
    if (len(description) > kMaxDescriptionLength) {
        result = UNRESOLVED.copy(description, 1, kMaxDescriptionLength - 4) + " ...";
    }
    return result;
}

// const
kMinMoveDistance = 2;



class PdCommand extends TObject {
    public boolean canUndo;
    public boolean done;
    public boolean commandChangesPlantFile;
    public boolean plantFileChangedBeforeCommand;
    
    public void create() {
        super.create();
        this.canUndo = true;
        this.done = false;
        // default commandChangesPlantFile to true, since most commands change file,
        //    if command does not change file, set to false after call to inherited create 
        this.commandChangesPlantFile = true;
        this.plantFileChangedBeforeCommand = false;
    }
    
    public void destroy() {
        //sublass could override
        super.destroy();
    }
    
    public void doCommand() {
        this.done = true;
        if (this.commandChangesPlantFile) {
            this.plantFileChangedBeforeCommand = umain.plantFileChanged;
            if (umain.MainForm != null) {
                umain.MainForm.setPlantFileChanged(true);
            }
        }
        //subclass should override and call inherited
    }
    
    public void undoCommand() {
        this.done = false;
        if (this.commandChangesPlantFile) {
            if (umain.MainForm != null) {
                umain.MainForm.setPlantFileChanged(this.plantFileChangedBeforeCommand);
            }
        }
        //sublass should override and call inherited
    }
    
    public void redoCommand() {
        this.doCommand();
        //sublass may override and call inherited doCommand
    }
    
    public String description() {
        result = "";
        result = "*command description*";
        return result;
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        result = 0;
        //subclasses may override but only if they keep copies of large objects
        return result;
    }
    
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        //sublasses should override if needed
        result = this;
        return result;
    }
    
}
class PdCommandList extends TObject {
    public TListCollection commands;
    public long lastDoneCommandIndex;
    public long undoLimit;
    public long objectUndoLimit;
    public PdCommand mouseCommand;
    public TPoint anchorPoint;
    public TPoint previousPoint;
    public boolean rightButtonDown;
    
    //PdCommandList
    public void create() {
        super.create();
        this.commands = ucollect.TListCollection().Create();
        this.lastDoneCommandIndex = -1;
        this.undoLimit = 50;
        this.objectUndoLimit = 10;
    }
    
    public void destroy() {
        this.commands.free;
        this.commands = null;
        //if mouseCoOmmand <> nil then error condition - ignoring for now - not released
        //could only happend if quitting somehow in middle of action
        super.destroy();
    }
    
    public PdCommand command(long index) {
        result = new PdCommand();
        result = PdCommand(this.commands.Items[index]);
        return result;
    }
    
    public void setNewUndoLimit(long newLimit) {
        if (newLimit != this.undoLimit) {
            this.undoLimit = newLimit;
            this.freeCommandsAboveLimit(this.undoLimit);
        }
    }
    
    public void setNewObjectUndoLimit(long newObjectLimit) {
        if (newObjectLimit != this.objectUndoLimit) {
            this.objectUndoLimit = newObjectLimit;
            this.freeCommandsAboveObjectLimit(this.objectUndoLimit);
        }
    }
    
    //free any command more than the number passed in
    public void freeCommandsAboveLimit(long theLimit) {
        PdCommand theCommand = new PdCommand();
        
        while ((this.commands.Count > theLimit) && (this.commands.Count > 0)) {
            theCommand = this.command(0);
            this.commands.Delete(0);
            theCommand.free;
            this.lastDoneCommandIndex -= 1;
            if (this.lastDoneCommandIndex < -1) {
                this.lastDoneCommandIndex = -1;
            }
        }
    }
    
    public void freeCommandsAboveObjectLimit(long objectLimit) {
        PdCommand theCommand = new PdCommand();
        long objectCount = 0;
        
        objectCount = this.objectCountInCommandList();
        while ((objectCount > objectLimit) && (this.commands.Count > 0)) {
            theCommand = this.command(0);
            this.commands.Delete(0);
            theCommand.free;
            this.lastDoneCommandIndex -= 1;
            if (this.lastDoneCommandIndex < -1) {
                this.lastDoneCommandIndex = -1;
            }
            objectCount = this.objectCountInCommandList();
        }
    }
    
    public long objectCountInCommandList() {
        result = 0;
        long i = 0;
        
        result = 0;
        if (this.commands.Count <= 0) {
            return result;
        }
        for (i = 0; i <= this.commands.Count - 1; i++) {
            result = result + this.command(i).numberOfStoredLargeObjects();
        }
        return result;
    }
    
    public void doCommand(PdCommand newCommand) {
        long i = 0;
        PdCommand theCommand = new PdCommand();
        
        if (this.isRedoEnabled()) {
            for (i = this.commands.Count - 1; i >= this.lastDoneCommandIndex + 1; i--) {
                //remove any extra commands after the current
                //do this first to free memory for command
                theCommand = this.command(i);
                this.commands.Delete(i);
                theCommand.free;
            }
        }
        // first see if there are too many objects and if so, scroll them 
        this.freeCommandsAboveObjectLimit(this.objectUndoLimit - 1);
        //see if too many commands are stored and if so, scroll them
        this.freeCommandsAboveLimit(this.undoLimit - 1);
        //now do this command
        //may fail in which case won't add
        newCommand.doCommand();
        this.commands.Add(newCommand);
        this.lastDoneCommandIndex += 1;
    }
    
    //added nextMouseCommand in these three functions to deal with unhandled exceptions occurring
    //during mouse commands.  This way, the command will not be further processed.
    //This may occasionally leak - the mouse command should be the one responsible for freeing
    //itself and returning nil if a problem occurs
    //returns whether the command finished tracking without freeing itself
    public boolean mouseDown(PdCommand newCommand, Tpoint point) {
        result = false;
        PdCommand nextMouseCommand = new PdCommand();
        
        result = false;
        if (this.mouseCommand != null) {
            //check if need to clear mouse command
            this.mouseUp(Point);
        }
        this.mouseCommand = null;
        if (newCommand != null) {
            //save mouse command and start it
            this.anchorPoint = Point;
            this.previousPoint = Point;
            nextMouseCommand = newCommand;
            this.mouseCommand = nextMouseCommand.TrackMouse(TrackPhase.trackPress, this.anchorPoint, this.previousPoint, Point, false, this.rightButtonDown);
            result = (this.mouseCommand != null);
        }
        return result;
    }
    
    public void mouseMove(TPoint point) {
        PdCommand nextMouseCommand = new PdCommand();
        
        nextMouseCommand = this.mouseCommand;
        this.mouseCommand = null;
        if (nextMouseCommand != null) {
            this.mouseCommand = nextMouseCommand.TrackMouse(TrackPhase.trackMove, this.anchorPoint, this.previousPoint, Point, this.didMouseMove(Point), this.rightButtonDown);
        }
        this.previousPoint = Point;
    }
    
    public void mouseUp(TPoint point) {
        PdCommand nextMouseCommand = new PdCommand();
        
        nextMouseCommand = this.mouseCommand;
        this.mouseCommand = null;
        if (nextMouseCommand != null) {
            nextMouseCommand = nextMouseCommand.TrackMouse(TrackPhase.trackRelease, this.anchorPoint, this.previousPoint, Point, this.didMouseMove(Point), this.rightButtonDown);
            if (nextMouseCommand != null) {
                this.doCommand(nextMouseCommand);
            }
        }
    }
    
    public boolean didMouseMove(TPoint point) {
        result = false;
        result = (abs(Point.x - this.anchorPoint.X) > kMinMoveDistance) || (abs(Point.y - this.anchorPoint.Y) > kMinMoveDistance);
        return result;
    }
    
    public boolean isUndoEnabled() {
        result = false;
        result = this.lastDoneCommandIndex >= 0;
        return result;
    }
    
    public boolean isRedoEnabled() {
        result = false;
        result = this.lastDoneCommandIndex < (this.commands.Count - 1);
        return result;
    }
    
    public String undoDescription() {
        result = "";
        if (this.lastDoneCommandIndex >= 0) {
            result = this.command(this.lastDoneCommandIndex).description();
            result = limitDescription(result);
        } else {
            result = "";
        }
        return result;
    }
    
    public String redoDescription() {
        result = "";
        if (this.lastDoneCommandIndex < (this.commands.Count - 1)) {
            result = this.command(this.lastDoneCommandIndex + 1).description();
            result = limitDescription(result);
        } else {
            result = "";
        }
        return result;
    }
    
    public void undoLast() {
        if (this.lastDoneCommandIndex >= 0) {
            this.command(this.lastDoneCommandIndex).undoCommand();
            this.lastDoneCommandIndex -= 1;
        }
    }
    
    public void redoLast() {
        if (this.lastDoneCommandIndex < (this.commands.Count - 1)) {
            this.command(this.lastDoneCommandIndex + 1).redoCommand();
            this.lastDoneCommandIndex += 1;
        }
    }
    
    public void fillListWithUndoableStrings(TStringList aList) {
        int i = 0;
        
        if (aList == null) {
            return;
        }
        if (this.lastDoneCommandIndex >= 0) {
            for (i = this.lastDoneCommandIndex; i >= 0; i--) {
                aList.Add(usupport.capitalize(this.command(i).description()));
            }
        }
    }
    
    public void fillListWithRedoableStrings(TStringList aList) {
        int i = 0;
        
        if (aList == null) {
            return;
        }
        if (this.lastDoneCommandIndex < (this.commands.Count - 1)) {
            for (i = this.lastDoneCommandIndex + 1; i <= this.commands.Count - 1; i++) {
                aList.Add(usupport.capitalize(this.command(i).description()));
            }
        }
    }
    
    public PdCommand lastCommandDone() {
        result = new PdCommand();
        result = null;
        if (this.lastDoneCommandIndex < (this.commands.Count - 1)) {
            result = this.command(this.lastDoneCommandIndex + 1);
        }
        return result;
    }
    
    public void removeCommand(PdCommand aCommand) {
        if (aCommand.done) {
            // assume this command has been undone previously 
            throw new GeneralException.create("Problem: Command not undone; in PdCommandList.removeCommand.");
        }
        this.commands.Remove(aCommand);
    }
    
}
