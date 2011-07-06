// unit updcom

from conversion_common import *;
import umath;
import ubreedr;
import umain;
import uamendmt;
import u3dexport;
import uturtle;
import udomain;
import ugener;
import utdo;
import uplant;
import uparams;
import ucommand;
import usupport;
import ucollect;
import delphi_compatability;

// const
kRotateNotInitialized = 0;
kRotateX = 1;
kRotateY = 2;
kRotateZ = 3;
kCopyToClipboard = true;
kDontCopyToClipboard = false;
kNewPlantAge = 5;
kNewPlantPosition = 100;
kHide = true;
kShow = false;
kSendBackward = true;
kBringForward = false;
kPasteMoveDistance = 40;
kCreateFirstGeneration = true;
kDontCreateFirstGeneration = false;
kAddAtEnd = -1;
kUp = 0;
kDown = 1;
kLeft = 2;
kRight = 3;
kChangeWidth = true;
kChangeHeight = false;


// var
long numPlantsCreatedThisSession = 0;


// ------------------------------------------------------------------------ local functions 
public String plantNamesForDescription(TList aList) {
    result = "";
    PdPlant firstPlant = new PdPlant();
    
    result = "";
    if ((aList == null) || (aList.Count <= 0)) {
        return result;
    }
    firstPlant = uplant.PdPlant(aList.Items[0]);
    if (firstPlant != null) {
        result = " plant \"" + firstPlant.getName() + "\"";
        if (aList.Count > 1) {
            result = result + ", others";
        }
    }
    return result;
}

// const
kGapBetweenArrangedPlants = 5;


public String nameForDirection(short direction) {
    result = "";
    result = "";
    switch (direction) {
        case kRotateX:
            result = "X";
            break;
        case kRotateY:
            result = "Y";
            break;
        case kRotateZ:
            result = "Z";
            break;
    return result;
}


// value classes to save information about each plant in list 
class PdBooleanValue extends TObject {
    public boolean saveBoolean;
    
    // ------------------------------------------------------------------------ value objects 
    public void createWithBoolean(boolean aBoolean) {
        this.saveBoolean = aBoolean;
    }
    
}
class PdPointValue extends TObject {
    public TPoint savePoint;
    
    public void createWithPoint(TPoint aPoint) {
        this.savePoint = aPoint;
    }
    
}
class PdSingleValue extends TObject {
    public float saveSingle;
    
    public void createWithSingle(float aSingle) {
        this.saveSingle = aSingle;
    }
    
}
class PdSinglePointValue extends TObject {
    public float x;
    public float y;
    
    public void createWithSingleXY(float anX, float aY) {
        this.x = anX;
        this.y = aY;
    }
    
}
class PdXYZValue extends TObject {
    public float x;
    public float y;
    public float z;
    
    public void createWithXYZ(float anX, float aY, float aZ) {
        this.x = anX;
        this.y = aY;
        this.z = aZ;
    }
    
}
class PdSmallintValue extends TObject {
    public short saveSmallint;
    
    public void createWithSmallint(short aSmallint) {
        this.saveSmallint = aSmallint;
    }
    
}
class PdLongintValue extends TObject {
    public long saveLongint;
    
    public void createWithLongint(long aLongint) {
        this.saveLongint = aLongint;
    }
    
}
class PdColorValue extends TObject {
    public TColorRef saveColor;
    
    public void createWithColor(TColorRef aColor) {
        this.saveColor = aColor;
    }
    
}
// -------------------------------------- commands that affect only the drawing area (and domain options) 
class PdScrollCommand extends PdCommand {
    public TPoint dragStartPoint;
    public SinglePoint oldOffset_mm;
    public SinglePoint newOffSet_mm;
    
    // ------------------------------------------------------------ PdScrollCommand 
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        result = this;
        if (aTrackPhase == ucommand.TrackPhase.trackPress) {
            this.dragStartPoint = nextPoint;
            this.oldOffset_mm = udomain.domain.plantDrawOffset_mm();
        } else if (aTrackPhase == ucommand.TrackPhase.trackMove) {
            if (mouseDidMove) {
                this.newOffSet_mm.x = this.oldOffset_mm.x + (nextPoint.X - this.dragStartPoint.X) / udomain.domain.plantDrawScale_PixelsPerMm();
                this.newOffSet_mm.y = this.oldOffset_mm.y + (nextPoint.Y - this.dragStartPoint.Y) / udomain.domain.plantDrawScale_PixelsPerMm();
                udomain.domain.plantManager.plantDrawOffset_mm = this.newOffSet_mm;
                umain.MainForm.recalculateAllPlantBoundsRectsForOffsetChange();
                umain.MainForm.invalidateEntireDrawing();
            }
        } else if (aTrackPhase == ucommand.TrackPhase.trackRelease) {
            pass
        }
        return result;
    }
    
    // PdDragCommand.doCommand should do nothing
    public void redoCommand() {
        //not redo
        super.doCommand();
        udomain.domain.plantManager.plantDrawOffset_mm = this.newOffSet_mm;
        umain.MainForm.recalculateAllPlantBoundsRectsForOffsetChange();
        umain.MainForm.invalidateEntireDrawing();
    }
    
    public void undoCommand() {
        super.undoCommand();
        udomain.domain.plantManager.plantDrawOffset_mm = this.oldOffset_mm;
        umain.MainForm.recalculateAllPlantBoundsRectsForOffsetChange();
        umain.MainForm.invalidateEntireDrawing();
    }
    
    public String description() {
        result = "";
        result = "scroll in main window";
        return result;
    }
    
}
class PdChangeMagnificationCommand extends PdCommand {
    public TPoint startDragPoint;
    public float oldScale_PixelsPerMm;
    public float newScale_pixelsPerMm;
    public SinglePoint oldOffset_mm;
    public SinglePoint newOffset_mm;
    public SinglePoint clickPoint;
    public boolean shift;
    
    // -------------------------------------------------------- PdChangeMagnificationCommand 
    public void createWithNewScaleAndPoint(float aNewScale, TPoint aPoint) {
        super.create();
        this.newScale_pixelsPerMm = aNewScale;
        this.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
        this.oldOffset_mm = udomain.domain.plantDrawOffset_mm();
        this.clickPoint.x = aPoint.X;
        this.clickPoint.y = aPoint.Y;
    }
    
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        TPoint size = new TPoint();
        float newScaleX = 0.0;
        float newScaleY = 0.0;
        
        result = this;
        if (aTrackPhase == ucommand.TrackPhase.trackPress) {
            this.startDragPoint = nextPoint;
        } else if (aTrackPhase == ucommand.TrackPhase.trackMove) {
            pass
        } else if (aTrackPhase == ucommand.TrackPhase.trackRelease) {
            size = Point(abs(nextPoint.X - this.startDragPoint.X), abs(this.startDragPoint.Y - nextPoint.Y));
            if ((size.X > 10) && (size.Y > 10)) {
                // have min size in case they move the mouse by mistake
                this.clickPoint.x = umath.min(nextPoint.X, this.startDragPoint.X) + abs(nextPoint.X - this.startDragPoint.X) / 2;
                this.clickPoint.y = umath.min(nextPoint.Y, this.startDragPoint.Y) + abs(nextPoint.Y - this.startDragPoint.Y) / 2;
                newScaleX = umath.safedivExcept(udomain.domain.plantDrawScale_PixelsPerMm() * umain.MainForm.drawingPaintBox.Width, size.X, 1.0);
                newScaleY = umath.safedivExcept(udomain.domain.plantDrawScale_PixelsPerMm() * umain.MainForm.drawingPaintBox.Height, size.Y, 1.0);
                this.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
                this.oldOffset_mm = udomain.domain.plantDrawOffset_mm();
                this.newScale_pixelsPerMm = umath.min(newScaleX, newScaleY);
            } else {
                this.clickPoint.x = nextPoint.X;
                this.clickPoint.y = nextPoint.Y;
                this.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
                this.oldOffset_mm = udomain.domain.plantDrawOffset_mm();
                if (this.shift) {
                    this.newScale_pixelsPerMm = this.oldScale_PixelsPerMm * 0.75;
                } else {
                    this.newScale_pixelsPerMm = this.oldScale_PixelsPerMm * 1.5;
                }
            }
        }
        return result;
    }
    
    public void doCommand() {
        TPoint clickTPoint = new TPoint();
        
        super.doCommand();
        if (this.newScale_pixelsPerMm != 0.0) {
            clickTPoint.X = intround(this.clickPoint.x);
            clickTPoint.Y = intround(this.clickPoint.y);
            umain.MainForm.magnifyOrReduce(this.newScale_pixelsPerMm, clickTPoint, umain.kDrawNow);
        }
        this.newOffset_mm = udomain.domain.plantDrawOffset_mm();
    }
    
    public void undoCommand() {
        super.undoCommand();
        udomain.domain.plantManager.plantDrawOffset_mm = this.oldOffset_mm;
        if (this.oldScale_PixelsPerMm != 0.0) {
            umain.MainForm.magnifyOrReduce(this.oldScale_PixelsPerMm, Point(0, 0), umain.kDrawNow);
        }
    }
    
    public String description() {
        result = "";
        if (this.newScale_pixelsPerMm > this.oldScale_PixelsPerMm) {
            result = "enlarge in main window";
        } else {
            result = "reduce in main window";
        }
        return result;
    }
    
}
class PdCenterDrawingCommand extends PdCommand {
    public float oldScale_PixelsPerMm;
    public float newScale_pixelsPerMm;
    public SinglePoint oldOffset_mm;
    public SinglePoint newOffset_mm;
    
    // -------------------------------------------------------- PdCenterDrawingCommand 
    public void doCommand() {
        super.doCommand();
        this.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
        this.oldOffset_mm = udomain.domain.plantDrawOffset_mm();
        umain.MainForm.fitVisiblePlantsInDrawingArea(umain.kDrawNow, umain.kScaleAndMove, umain.kAlwaysMove);
        umain.MainForm.recalculateAllPlantBoundsRects(uplant.kDontDrawNow);
        this.newScale_pixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
        this.newOffset_mm = udomain.domain.plantDrawOffset_mm();
    }
    
    public void undoCommand() {
        super.undoCommand();
        udomain.domain.plantManager.plantDrawOffset_mm = this.oldOffset_mm;
        umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow);
        if (this.oldScale_PixelsPerMm != 0.0) {
            umain.MainForm.magnifyOrReduce(this.oldScale_PixelsPerMm, Point(0, 0), umain.kDrawNow);
        }
    }
    
    public void redoCommand() {
        super.doCommand();
        udomain.domain.plantManager.plantDrawOffset_mm = this.newOffset_mm;
        umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow);
        if (this.newScale_pixelsPerMm != 0.0) {
            umain.MainForm.magnifyOrReduce(this.newScale_pixelsPerMm, Point(0, 0), umain.kDrawNow);
        }
    }
    
    public String description() {
        result = "";
        result = "scale to fit in main window";
        return result;
    }
    
}
class PdChangeMainWindowOrientationCommand extends PdCommand {
    public float oldScale_PixelsPerMm;
    public float newScale_pixelsPerMm;
    public SinglePoint oldOffset_mm;
    public SinglePoint newOffset_mm;
    public short oldWindowOrientation;
    public short newWindowOrientation;
    
    // ------------------------------------------------------------ PdChangeMainWindowOrientationCommand 
    public void createWithNewOrientation(short aNewOrientation) {
        super.create();
        //hidden flag not saved
        this.commandChangesPlantFile = false;
        this.newWindowOrientation = aNewOrientation;
        this.oldWindowOrientation = udomain.domain.options.mainWindowOrientation;
    }
    
    public void doCommand() {
        super.doCommand();
        try {
            UNRESOLVED.cursor_startWait;
            udomain.domain.options.mainWindowOrientation = this.newWindowOrientation;
            umain.MainForm.updateForChangeToOrientation();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void undoCommand() {
        super.undoCommand();
        try {
            UNRESOLVED.cursor_startWait;
            udomain.domain.options.mainWindowOrientation = this.oldWindowOrientation;
            umain.MainForm.updateForChangeToOrientation();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public String description() {
        result = "";
        result = "change top/side orientation in main window";
        return result;
    }
    
}
// ------------------------------------------------------------------ commands that affect only the domain 
class PdChangeDomainOptionsCommand extends PdCommand {
    public DomainOptionsStructure oldOptions;
    public DomainOptionsStructure newOptions;
    
    // -------------------------------------------------------- PdChangeDomainOptionsCommand 
    public void createWithOptions(DomainOptionsStructure aNewOptions) {
        super.create();
        this.commandChangesPlantFile = false;
        this.newOptions = aNewOptions;
        this.oldOptions = udomain.domain.options;
    }
    
    public void doCommand() {
        super.doCommand();
        udomain.domain.options = this.newOptions;
        umain.MainForm.updateForChangeToDomainOptions();
    }
    
    public void undoCommand() {
        super.undoCommand();
        udomain.domain.options = this.oldOptions;
        umain.MainForm.updateForChangeToDomainOptions();
    }
    
    public String description() {
        result = "";
        result = "change preferences";
        return result;
    }
    
}
class PdChangeDomain3DOptionsCommand extends PdCommand {
    public short outputType;
    public FileExport3DOptionsStructure oldOptions;
    public FileExport3DOptionsStructure newOptions;
    
    // -------------------------------------------------------- PdChangeDomain3DOptionsCommand 
    public void createWithOptionsAndType(FileExport3DOptionsStructure aNewOptions, short anOutputType) {
        super.create();
        this.outputType = anOutputType;
        this.commandChangesPlantFile = false;
        this.newOptions = aNewOptions;
        this.oldOptions = udomain.domain.exportOptionsFor3D[this.outputType];
    }
    
    public void doCommand() {
        super.doCommand();
        udomain.domain.exportOptionsFor3D[this.outputType] = this.newOptions;
    }
    
    public void undoCommand() {
        super.undoCommand();
        udomain.domain.exportOptionsFor3D[this.outputType] = this.oldOptions;
    }
    
    public String description() {
        result = "";
        result = "change " + usupport.nameStringForFileType(u3dexport.fileTypeFor3DExportType(this.outputType)) + " output options";
        return result;
    }
    
}
// ------------------------------------------------------------------- commands that affect one plant only 
class PdRenameCommand extends PdCommand {
    public PdPlant plant;
    public String oldName;
    public String newName;
    
    // ------------------------------------------------------------ PdRenameCommand 
    public void createWithPlantAndNewName(PdPlant aPlant, String aNewName) {
        super.create();
        this.plant = aPlant;
        this.oldName = this.plant.getName();
        this.newName = aNewName;
    }
    
    public void doCommand() {
        super.doCommand();
        this.plant.setName(this.newName);
        umain.MainForm.updateForRenamingPlant(this.plant);
    }
    
    public void undoCommand() {
        super.undoCommand();
        this.plant.setName(this.oldName);
        umain.MainForm.updateForRenamingPlant(this.plant);
    }
    
    public String description() {
        result = "";
        result = "rename \"" + this.oldName + "\" to \"" + this.newName + "\"";
        return result;
    }
    
}
class PdEditNoteCommand extends PdCommand {
    public PdPlant plant;
    public TStringList oldStrings;
    public TStringList newStrings;
    
    // ------------------------------------------------------------ PdEditNoteCommand 
    public void createWithPlantAndNewTStrings(PdPlant aPlant, TStrings aNewStrings) {
        super.create();
        this.plant = aPlant;
        this.oldStrings = this.plant.noteLines;
        // we take ownership of this list and delete it if undone
        this.newStrings = (delphi_compatability.TStringList)aNewStrings;
    }
    
    public void destroy() {
        if (this.done) {
            this.oldStrings.free;
            this.oldStrings = null;
        } else {
            this.newStrings.free;
            this.newStrings = null;
        }
    }
    
    public void doCommand() {
        super.doCommand();
        this.plant.noteLines = this.newStrings;
        umain.MainForm.updateForChangeToPlantNote(this.plant);
    }
    
    public void undoCommand() {
        super.undoCommand();
        this.plant.noteLines = this.oldStrings;
        umain.MainForm.updateForChangeToPlantNote(this.plant);
    }
    
    public String description() {
        result = "";
        result = "change note for \"" + this.plant.getName() + "\"";
        return result;
    }
    
}
class PdNewCommand extends PdCommand {
    public PdPlant newPlant;
    public boolean useWizardPlant;
    public PdPlant wizardPlant;
    public TList oldSelectedList;
    
    // v2.0
    // --------------------------------------------------------------------------------------------- PdNewCommand 
    public void createWithWizardPlantAndOldSelectedList(PdPlant aPlant, TList anOldSelectedList) {
        int i = 0;
        
        super.create();
        this.useWizardPlant = true;
        this.wizardPlant = aPlant;
        // selected list is just pointers, this doesn't take control of them
        this.oldSelectedList = delphi_compatability.TList().Create();
        if ((anOldSelectedList != null) && (anOldSelectedList.Count > 0)) {
            for (i = 0; i <= anOldSelectedList.Count - 1; i++) {
                this.oldSelectedList.Add(anOldSelectedList.Items[i]);
            }
        }
    }
    
    public void destroy() {
        this.oldSelectedList.free;
        this.oldSelectedList = null;
        if ((!this.done) && (this.newPlant != null)) {
            // free created plant if change was undone 
            this.newPlant.free;
            this.newPlant = null;
        }
        if ((this.useWizardPlant) && (this.wizardPlant != null)) {
            this.wizardPlant.free;
            this.wizardPlant = null;
        }
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        result = 0;
        if ((!this.done) && (this.newPlant != null)) {
            result += 1;
        }
        if ((this.useWizardPlant) && (this.wizardPlant != null)) {
            result += 1;
        }
        return result;
    }
    
    public void doCommand() {
        super.doCommand();
        this.newPlant = uplant.PdPlant().create();
        try {
            UNRESOLVED.cursor_startWait;
            if ((this.useWizardPlant) && (this.wizardPlant != null)) {
                this.wizardPlant.copyTo(this.newPlant);
            } else {
                this.newPlant.defaultAllParameters();
                this.newPlant.setName("New plant " + IntToStr(numPlantsCreatedThisSession + 1));
                numPlantsCreatedThisSession += 1;
            }
            this.newPlant.randomize();
            this.newPlant.moveTo(umain.MainForm.standardPastePosition());
            this.newPlant.calculateDrawingScaleToLookTheSameWithDomainScale();
            this.newPlant.recalculateBounds(umain.kDrawNow);
            // put new plant at end of plant manager list 
            udomain.domain.plantManager.plants.add(this.newPlant);
            // make new plant the only selected plant 
            umain.MainForm.deselectAllPlants();
            umain.MainForm.addSelectedPlant(this.newPlant, kAddAtEnd);
            umain.MainForm.updateForChangeToPlantList();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void undoCommand() {
        int i = 0;
        
        super.undoCommand();
        udomain.domain.plantManager.plants.remove(this.newPlant);
        umain.MainForm.removeSelectedPlant(this.newPlant);
        if (this.oldSelectedList.Count > 0) {
            for (i = 0; i <= this.oldSelectedList.Count - 1; i++) {
                // put back selections from before new plant was added
                umain.MainForm.selectedPlants.Add(this.oldSelectedList.Items[i]);
            }
        }
        umain.MainForm.updateForChangeToPlantList();
    }
    
    public void redoCommand() {
        super.doCommand();
        umain.MainForm.deselectAllPlants();
        udomain.domain.plantManager.plants.add(this.newPlant);
        umain.MainForm.addSelectedPlant(this.newPlant, kAddAtEnd);
        umain.MainForm.updateForChangeToPlantList();
    }
    
    public String description() {
        result = "";
        result = "create new plant";
        return result;
    }
    
}
class PdSendBackwardOrForwardCommand extends PdCommand {
    public boolean backward;
    
    // ----------------------------------------------------------- PdSendBackwardOrForwardCommand 
    public void createWithBackwardOrForward(boolean aBackward) {
        super.create();
        this.backward = aBackward;
    }
    
    public void doCommand() {
        if (this.backward) {
            // assumption here is that selected plants list doesn't change between this command and undo 
            umain.MainForm.moveSelectedPlantsDown();
        } else {
            umain.MainForm.moveSelectedPlantsUp();
        }
    }
    
    public void undoCommand() {
        if (this.backward) {
            umain.MainForm.moveSelectedPlantsUp();
        } else {
            umain.MainForm.moveSelectedPlantsDown();
        }
    }
    
    public String description() {
        result = "";
        if (this.backward) {
            result = "send backward in main window";
        } else {
            result = "bring forward in main window";
        }
        return result;
    }
    
}
class PdCreateAmendmentCommand extends PdCommand {
    public PdPlant plant;
    public PdPlantDrawingAmendment newAmendment;
    
    // ------------------------------------------------------------ PdCreateAmendmentCommand 
    public void createWithPlantAndAmendment(PdPlant aPlant, PdPlantDrawingAmendment aNewAmendment) {
        super.create();
        this.plant = aPlant;
        if (aNewAmendment == null) {
            throw new GeneralException.create("Problem: Nil new amendment; in PdCreateAmendmentCommand.createWithPlantAndAmendment.");
        }
        // we take ownership of this and delete it if undone
        this.newAmendment = aNewAmendment;
    }
    
    public void destroy() {
        if (!this.done) {
            this.newAmendment.free;
            this.newAmendment = null;
        }
    }
    
    public void doCommand() {
        super.doCommand();
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        this.plant.addAmendment(this.newAmendment);
        this.plant.recalculateBounds(umain.kDrawNow);
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        umain.MainForm.addAmendedPartToList(this.newAmendment.partID, this.newAmendment.typeOfPart);
    }
    
    public void undoCommand() {
        super.undoCommand();
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        this.plant.removeAmendment(this.newAmendment);
        this.plant.recalculateBounds(umain.kDrawNow);
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        umain.MainForm.removeAmendedPartFromList(this.newAmendment.partID, this.newAmendment.typeOfPart);
    }
    
    public String description() {
        result = "";
        result = "pose part " + IntToStr(this.newAmendment.partID) + " in plant \"" + this.plant.getName() + "\"";
        return result;
    }
    
}
class PdDeleteAmendmentCommand extends PdCommand {
    public PdPlant plant;
    public PdPlantDrawingAmendment amendment;
    
    // ------------------------------------------------------------ PdDeleteAmendmentCommand 
    public void createWithPlantAndAmendment(PdPlant aPlant, PdPlantDrawingAmendment anAmendment) {
        super.create();
        this.plant = aPlant;
        if (anAmendment == null) {
            throw new GeneralException.create("Problem: Nil amendment; in PdDeleteAmendmentCommand.createWithPlantAndAmendment.");
        }
        // we take ownership of this and delete it if done
        this.amendment = anAmendment;
    }
    
    public void destroy() {
        if (this.done) {
            this.amendment.free;
            this.amendment = null;
        }
    }
    
    public void doCommand() {
        super.doCommand();
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        this.plant.removeAmendment(this.amendment);
        this.plant.recalculateBounds(umain.kDrawNow);
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        umain.MainForm.removeAmendedPartFromList(this.amendment.partID, this.amendment.typeOfPart);
    }
    
    public void undoCommand() {
        super.undoCommand();
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        this.plant.addAmendment(this.amendment);
        this.plant.recalculateBounds(umain.kDrawNow);
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        umain.MainForm.addAmendedPartToList(this.amendment.partID, this.amendment.typeOfPart);
    }
    
    public String description() {
        result = "";
        result = "unpose part " + IntToStr(this.amendment.partID) + " in plant \"" + this.plant.getName() + "\"";
        return result;
    }
    
}
class PdEditAmendmentCommand extends PdCommand {
    public PdPlant plant;
    public String field;
    public PdPlantDrawingAmendment oldAmendment;
    public PdPlantDrawingAmendment newAmendment;
    
    // ------------------------------------------------------------ PdEditAmendmentCommand 
    public void createWithPlantAndAmendmentAndField(PdPlant aPlant, PdPlantDrawingAmendment aNewAmendment, String aField) {
        super.create();
        this.plant = aPlant;
        this.field = aField;
        if (aNewAmendment == null) {
            throw new GeneralException.create("nil new amendment");
        }
        // we take ownership of this and delete it if undone
        this.newAmendment = aNewAmendment;
        this.oldAmendment = this.plant.amendmentForPartID(this.newAmendment.partID);
    }
    
    public void destroy() {
        if (this.done) {
            this.oldAmendment.free;
            this.oldAmendment = null;
        } else {
            this.newAmendment.free;
            this.newAmendment = null;
        }
    }
    
    public void doCommand() {
        int index = 0;
        int oldItemIndex = 0;
        
        super.doCommand();
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        if (this.oldAmendment != null) {
            this.plant.removeAmendment(this.oldAmendment);
        }
        this.plant.addAmendment(this.newAmendment);
        this.plant.recalculateBounds(umain.kDrawNow);
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        umain.MainForm.updatePoseInfo();
    }
    
    public void undoCommand() {
        String oldString = "";
        int index = 0;
        int oldItemIndex = 0;
        
        super.undoCommand();
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        this.plant.removeAmendment(this.newAmendment);
        if (this.oldAmendment != null) {
            this.plant.addAmendment(this.oldAmendment);
        }
        this.plant.recalculateBounds(umain.kDrawNow);
        umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
        umain.MainForm.updatePoseInfo();
    }
    
    public String description() {
        result = "";
        String fullString = "";
        
        if (this.field == "hide") {
            if (this.newAmendment.hide) {
                fullString = "hide";
            } else {
                fullString = "show";
            }
        } else if (this.field == "rotate") {
            if (this.newAmendment.addRotations) {
                fullString = "rotate";
            } else {
                fullString = "remove rotation for";
            }
        } else if (this.field == "scale") {
            if (this.newAmendment.multiplyScale) {
                fullString = "scale";
            } else {
                fullString = "remove scaling for";
            }
        } else if (this.field == "scale above") {
            if (this.newAmendment.propagateScale) {
                fullString = "scale-this-part-and-above";
            } else {
                fullString = "remove scale-this-part-and-above for";
            }
        } else {
            fullString = "change " + this.field + " for";
        }
        result = "posing: " + fullString + " part " + IntToStr(this.newAmendment.partID) + " in plant \"" + this.plant.getName() + "\"";
        return result;
    }
    
}
class PdSelectPosingPartCommand extends PdCommand {
    public PdPlant plant;
    public long newPartID;
    public long oldPartID;
    public String oldPartType;
    public String newPartType;
    
    // ------------------------------------------------------------ PdSelectPosingPartCommand 
    public void createWithPlantAndPartIDsAndTypes(PdPlant aPlant, long aNewPartID, long anOldPartID, String aNewPartType, String anOldPartType) {
        short i = 0;
        
        super.create();
        // selected posed part not saved
        this.commandChangesPlantFile = false;
        this.plant = aPlant;
        this.newPartID = aNewPartID;
        this.oldPartID = anOldPartID;
        this.newPartType = aNewPartType;
        this.oldPartType = anOldPartType;
    }
    
    public void doCommand() {
        // selected posed part not saved
        this.commandChangesPlantFile = false;
        super.doCommand();
        umain.MainForm.selectedPlantPartID = this.newPartID;
        umain.MainForm.selectedPlantPartType = this.newPartType;
        umain.MainForm.updatePosingForSelectedPlantPart();
        umain.MainForm.redrawFocusedPlantOnly(umain.kDrawNow);
    }
    
    public void undoCommand() {
        super.undoCommand();
        umain.MainForm.selectedPlantPartID = this.oldPartID;
        umain.MainForm.selectedPlantPartType = this.oldPartType;
        umain.MainForm.updatePosingForSelectedPlantPart();
        umain.MainForm.redrawFocusedPlantOnly(umain.kDrawNow);
    }
    
    public String description() {
        result = "";
        if (this.newPartID < 0) {
            result = "deselect all parts of plant " + this.plant.getName();
        } else {
            result = "select part " + IntToStr(this.newPartID) + " of plant " + this.plant.getName();
        }
        return result;
    }
    
}
// ---------------------------------- commands that affect a list of plants, usually in a minor way 
class PdCommandWithListOfPlants extends PdCommand {
    public TList plantList;
    public TListCollection values;
    public PdPlant plant;
    public boolean removesPlantAmendments;
    public TList listOfAmendmentLists;
    
    //for temporary use
    // ------------------------------------------------------------ PdCommandWithListOfPlants 
    public void createWithListOfPlants(TList aList) {
        short i = 0;
        
        super.create();
        this.plantList = delphi_compatability.TList().Create();
        if (aList.Count > 0) {
            for (i = 0; i <= aList.Count - 1; i++) {
                this.plantList.Add(aList.Items[i]);
            }
        }
        this.values = ucollect.TListCollection().Create();
        this.listOfAmendmentLists = null;
    }
    
    public void setUpToRemoveAmendmentsWhenDone() {
        int i = 0;
        int j = 0;
        PdPlant plant = new PdPlant();
        TList aList = new TList();
        
        // call this method after create method if the command should remove amendments
        this.removesPlantAmendments = true;
        this.listOfAmendmentLists = delphi_compatability.TList().Create();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                plant = uplant.PdPlant(this.plantList.Items[i]);
                aList = delphi_compatability.TList().Create();
                if (plant.amendments.Count > 0) {
                    for (j = 0; j <= plant.amendments.Count - 1; j++) {
                        aList.Add(uamendmt.PdPlantDrawingAmendment(plant.amendments.Items[j]));
                    }
                }
                this.listOfAmendmentLists.Add(aList);
            }
        }
    }
    
    public void destroy() {
        int i = 0;
        int j = 0;
        PdPlantDrawingAmendment amendment = new PdPlantDrawingAmendment();
        TList aList = new TList();
        
        this.plantList.free;
        this.plantList = null;
        this.values.free;
        this.values = null;
        if ((this.done) && (this.removesPlantAmendments)) {
            if ((this.listOfAmendmentLists != null) && (this.listOfAmendmentLists.Count > 0)) {
                for (i = 0; i <= this.listOfAmendmentLists.Count - 1; i++) {
                    aList = delphi_compatability.TList(this.listOfAmendmentLists.Items[i]);
                    if (aList.Count > 0) {
                        for (j = 0; j <= aList.Count - 1; j++) {
                            amendment = uamendmt.PdPlantDrawingAmendment(aList.Items[j]);
                            amendment.free;
                        }
                    }
                    aList.free;
                }
            }
        }
        this.listOfAmendmentLists.free;
        this.listOfAmendmentLists = null;
        super.destroy();
    }
    
    public void doCommand() {
        int i = 0;
        boolean atLeastOnePlantHadAmendments = false;
        TList aList = new TList();
        
        super.doCommand();
        if (!this.removesPlantAmendments) {
            return;
        }
        atLeastOnePlantHadAmendments = false;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                aList = delphi_compatability.TList(this.listOfAmendmentLists.Items[i]);
                if (aList.Count > 0) {
                    atLeastOnePlantHadAmendments = true;
                    uplant.PdPlant(this.plantList.Items[i]).clearPointersToAllAmendments();
                }
            }
        }
        if (atLeastOnePlantHadAmendments) {
            umain.MainForm.updatePosingForFirstSelectedPlant();
        }
    }
    
    public void undoCommand() {
        int i = 0;
        boolean atLeastOnePlantHadAmendments = false;
        TList aList = new TList();
        
        super.undoCommand();
        if (!this.removesPlantAmendments) {
            return;
        }
        atLeastOnePlantHadAmendments = false;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                aList = delphi_compatability.TList(this.listOfAmendmentLists.Items[i]);
                if (aList.Count > 0) {
                    atLeastOnePlantHadAmendments = true;
                    uplant.PdPlant(this.plantList.Items[i]).restoreAmendmentPointersToList(aList);
                }
            }
        }
        if (atLeastOnePlantHadAmendments) {
            umain.MainForm.updatePosingForFirstSelectedPlant();
        }
    }
    
    public void invalidateCombinedPlantRects() {
        TRect redrawRect = new TRect();
        short i = 0;
        
        redrawRect = delphi_compatability.Bounds(0, 0, 0, 0);
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                delphi_compatability.UnionRect(redrawRect, redrawRect, uplant.PdPlant(this.plantList.Items[i]).boundsRect_pixels());
            }
        }
        umain.MainForm.invalidateDrawingRect(redrawRect);
    }
    
}
class PdChangeSelectedPlantsCommand extends PdCommandWithListOfPlants {
    public TList newList;
    
    // ------------------------------------------------------------ PdChangeSelectedPlantsCommand 
    public void createWithOldListOFPlantsAndNewList(TList aList, TList aNewList) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        //which plants are selected not saved
        this.commandChangesPlantFile = false;
        this.newList = delphi_compatability.TList().Create();
        if (aNewList.Count > 0) {
            for (i = 0; i <= aNewList.Count - 1; i++) {
                this.newList.Add(aNewList.Items[i]);
            }
        }
    }
    
    public void destroy() {
        this.newList.free;
        this.newList = null;
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        
        //which plants are selected not saved
        this.commandChangesPlantFile = false;
        super.doCommand();
        // MainForm.deselectAllPlants; // don't want this, it updates, and we will be updating soon
        umain.MainForm.selectedPlants.Clear();
        if (this.newList.Count > 0) {
            umain.MainForm.selectedPlants.Add(this.newList.Items[0]);
            if (udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
                umain.MainForm.showOnePlantExclusively(umain.kDontDrawYet);
            } else {
                if (this.newList.Count > 1) {
                    for (i = 1; i <= this.newList.Count - 1; i++) {
                        umain.MainForm.selectedPlants.Add(this.newList.Items[i]);
                    }
                }
            }
        }
        umain.MainForm.updateForChangeToPlantSelections();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        // MainForm.deselectAllPlants; // don't want this, it updates, and we will be updating soon
        umain.MainForm.selectedPlants.Clear();
        if (this.plantList.Count > 0) {
            umain.MainForm.selectedPlants.Add(this.plantList.Items[0]);
            if (udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
                umain.MainForm.showOnePlantExclusively(umain.kDontDrawYet);
            } else {
                if (this.plantList.Count > 1) {
                    for (i = 1; i <= this.plantList.Count - 1; i++) {
                        umain.MainForm.selectedPlants.Add(this.plantList.Items[i]);
                    }
                }
            }
        }
        umain.MainForm.updateForChangeToPlantSelections();
    }
    
    public String description() {
        result = "";
        if (this.newList.Count <= 0) {
            result = "deselect all plants";
        } else {
            result = "select" + plantNamesForDescription(this.newList);
        }
        return result;
    }
    
}
class PdSelectOrDeselectAllCommand extends PdCommandWithListOfPlants {
    public boolean deselect;
    
    // ------------------------------------------------------------ PdSelectOrDeselectAllCommand 
    public void doCommand() {
        short i = 0;
        
        //which plants are selected not saved
        this.commandChangesPlantFile = false;
        super.doCommand();
        if (this.deselect) {
            // MainForm.deselectAllPlants;
            umain.MainForm.deselectAllPlants();
        } else {
            umain.MainForm.selectedPlants.Clear();
        }
        if (!this.deselect) {
            //FIX unresolved WITH expression: udomain.domain.plantManager.plants
            if (UNRESOLVED.count > 0) {
                for (i = 0; i <= UNRESOLVED.count - 1; i++) {
                    umain.MainForm.selectedPlants.Add(UNRESOLVED.items[i]);
                }
            }
        }
        umain.MainForm.updateForChangeToPlantSelections();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (!this.deselect) {
            // MainForm.deselectAllPlants;
            umain.MainForm.deselectAllPlants();
        } else {
            umain.MainForm.selectedPlants.Clear();
        }
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                umain.MainForm.selectedPlants.Add(this.plantList.Items[i]);
            }
        }
        umain.MainForm.updateForChangeToPlantSelections();
    }
    
    public String description() {
        result = "";
        if (this.deselect) {
            result = "deselect all plants";
        } else {
            result = "select all plants";
        }
        return result;
    }
    
}
class PdResizePlantsCommand extends PdCommandWithListOfPlants {
    public boolean initialized;
    public boolean doneInMouseCommand;
    public TListCollection newValues;
    public TListCollection oldSizes;
    public TListCollection aspectRatios;
    public TPoint dragStartPoint;
    public TPoint offset;
    public float multiplier;
    public float newValue;
    
    // ------------------------------------------------------------ PdResizePlantsCommand 
    public void createWithListOfPlants(TList aList) {
        super.createWithListOfPlants(aList);
        this.newValues = ucollect.TListCollection().Create();
        this.oldSizes = ucollect.TListCollection().Create();
        this.aspectRatios = ucollect.TListCollection().Create();
    }
    
    public void createWithListOfPlantsAndMultiplier(TList aList, float aMultiplier) {
        this.createWithListOfPlants(aList);
        this.saveInitialValues();
        this.multiplier = aMultiplier;
    }
    
    public void createWithListOfPlantsAndNewValue(TList aList, float aNewValue) {
        this.createWithListOfPlants(aList);
        this.saveInitialValues();
        this.newValue = aNewValue;
    }
    
    public void saveInitialValues() {
        short i = 0;
        float aspectRatio = 0.0;
        
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                if (usupport.rHeight(this.plant.boundsRect_pixels()) != 0) {
                    aspectRatio = 1.0 * usupport.rWidth(this.plant.boundsRect_pixels()) / usupport.rHeight(this.plant.boundsRect_pixels());
                } else {
                    aspectRatio = 1.0;
                }
                this.aspectRatios.Add(PdSingleValue().createWithSingle(aspectRatio));
                this.values.Add(PdSingleValue().createWithSingle(this.plant.drawingScale_PixelsPerMm));
                this.oldSizes.Add(PdPointValue().createWithPoint(Point(usupport.rWidth(this.plant.boundsRect_pixels()), usupport.rHeight(this.plant.boundsRect_pixels()))));
            }
        }
    }
    
    public void destroy() {
        this.newValues.free;
        this.newValues = null;
        this.oldSizes.free;
        this.oldSizes = null;
        this.aspectRatios.free;
        this.aspectRatios = null;
        super.destroy();
    }
    
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        result = this;
        if (aTrackPhase == ucommand.TrackPhase.trackPress) {
            this.dragStartPoint = nextPoint;
        } else if ((aTrackPhase == ucommand.TrackPhase.trackMove) && (mouseDidMove)) {
            if (!this.initialized) {
                this.saveInitialValues();
                this.initialized = true;
                this.doneInMouseCommand = true;
                this.offset = Point(0, 0);
                super.doCommand();
                return result;
            }
            if (this.initialized) {
                this.offset.X = nextPoint.X - this.dragStartPoint.X;
                this.offset.Y = nextPoint.Y - this.dragStartPoint.Y;
                this.doCommand();
            }
        } else if (aTrackPhase == ucommand.TrackPhase.trackRelease) {
            if ((!mouseDidMove) || (!this.initialized)) {
                result = null;
                this.free;
            }
        }
        return result;
    }
    
    public void doCommand() {
        short i = 0;
        TPoint newSize = new TPoint();
        TPoint oldSize = new TPoint();
        float aspectRatio = 0.0;
        float oldScale = 0.0;
        
        if (!this.doneInMouseCommand) {
            super.doCommand();
        }
        if (this.plantList.Count <= 0) {
            return;
        }
        if ((this.offset.X == 0) && (this.offset.Y == 0) && (this.multiplier == 0) && (this.newValue == 0)) {
            return;
        }
        try {
            if (!this.doneInMouseCommand) {
                UNRESOLVED.cursor_startWait;
            }
            this.invalidateCombinedPlantRects();
            this.newValues.clear();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    if (this.multiplier != 0) {
                        this.plant.drawingScale_PixelsPerMm = this.plant.drawingScale_PixelsPerMm * this.multiplier;
                    } else if (this.newValue != 0) {
                        this.plant.drawingScale_PixelsPerMm = this.newValue;
                    } else {
                        oldSize = PdPointValue(this.oldSizes.Items[i]).savePoint;
                        aspectRatio = PdSingleValue(this.aspectRatios.Items[i]).saveSingle;
                        oldScale = PdSingleValue(this.values.Items[i]).saveSingle;
                        // 10 pixels is arbitrary minimum
                        newSize.Y = umath.intMax(10, oldSize.Y - this.offset.Y);
                        newSize.X = intround(newSize.Y * aspectRatio);
                        this.plant.calculateDrawingScaleToFitSize(newSize);
                        if ((this.plant.drawingScale_PixelsPerMm > oldScale) && (this.offset.Y > 0)) {
                            // this is to counteract a bug that when you resize down, it resizes up the first mouse move, then down
                            // can't figure out why, just putting in this ugly fix to stop it from doing that
                            this.plant.drawingScale_PixelsPerMm = oldScale;
                        }
                    }
                    this.newValues.Add(PdSingleValue().createWithSingle(this.plant.drawingScale_PixelsPerMm));
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
        } finally {
            if (!this.doneInMouseCommand) {
                UNRESOLVED.cursor_stopWait;
            }
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        try {
            UNRESOLVED.cursor_startWait;
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.drawingScale_PixelsPerMm = PdSingleValue(this.values.Items[i]).saveSingle;
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void redoCommand() {
        short i = 0;
        
        if (!this.initialized) {
            return;
        }
        super.undoCommand();
        try {
            UNRESOLVED.cursor_startWait;
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.drawingScale_PixelsPerMm = PdSingleValue(this.newValues.Items[i]).saveSingle;
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public String description() {
        result = "";
        result = "resize" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdResizePlantsToSameWidthOrHeightCommand extends PdCommandWithListOfPlants {
    public TListCollection newValues;
    public TListCollection oldSizes;
    public float newWidth;
    public float newHeight;
    public boolean changeWidth;
    
    // ------------------------------------------------------------ PdResizePlantsToSameWidthOrHeightCommand 
    public void createWithListOfPlantsAndNewWidthOrHeight(TList aList, float aNewWidth, float aNewHeight, boolean aChangeWidth) {
        super.createWithListOfPlants(aList);
        this.newValues = ucollect.TListCollection().Create();
        this.oldSizes = ucollect.TListCollection().Create();
        this.saveInitialValues();
        this.newWidth = aNewWidth;
        this.newHeight = aNewHeight;
        this.changeWidth = aChangeWidth;
    }
    
    public void saveInitialValues() {
        short i = 0;
        
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.values.Add(PdSingleValue().createWithSingle(this.plant.drawingScale_PixelsPerMm));
                this.oldSizes.Add(PdPointValue().createWithPoint(Point(usupport.rWidth(this.plant.boundsRect_pixels()), usupport.rHeight(this.plant.boundsRect_pixels()))));
            }
        }
    }
    
    public void destroy() {
        this.newValues.free;
        this.newValues = null;
        this.oldSizes.free;
        this.oldSizes = null;
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        float newScaleX = 0.0;
        float newScaleY = 0.0;
        
        super.doCommand();
        if (this.plantList.Count <= 0) {
            return;
        }
        try {
            UNRESOLVED.cursor_startWait;
            this.invalidateCombinedPlantRects();
            this.newValues.clear();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.recalculateBounds(umain.kDontDrawYet);
                    if (this.changeWidth) {
                        this.plant.drawingScale_PixelsPerMm = umath.safedivExcept(this.plant.drawingScale_PixelsPerMm * this.newWidth, usupport.rWidth(this.plant.boundsRect_pixels()), 0.1);
                    } else {
                        this.plant.drawingScale_PixelsPerMm = umath.safedivExcept(this.plant.drawingScale_PixelsPerMm * this.newHeight, usupport.rHeight(this.plant.boundsRect_pixels()), 0.1);
                    }
                    this.newValues.Add(PdSingleValue().createWithSingle(this.plant.drawingScale_PixelsPerMm));
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.drawingScale_PixelsPerMm = PdSingleValue(this.values.Items[i]).saveSingle;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
        umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
    }
    
    public void redoCommand() {
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.drawingScale_PixelsPerMm = PdSingleValue(this.newValues.Items[i]).saveSingle;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
        umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
    }
    
    public String description() {
        result = "";
        result = "scale" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdPackPlantsCommand extends PdCommandWithListOfPlants {
    public TListCollection newScales;
    public TListCollection oldSizes;
    public TListCollection newPoints;
    public TListCollection oldPoints;
    public TRect focusRect;
    
    // ------------------------------------------------------------ PdPackPlantsCommand 
    public void createWithListOfPlantsAndFocusRect(TList aList, TRect aFocusRect) {
        super.createWithListOfPlants(aList);
        this.newScales = ucollect.TListCollection().Create();
        this.oldSizes = ucollect.TListCollection().Create();
        this.newPoints = ucollect.TListCollection().Create();
        this.oldPoints = ucollect.TListCollection().Create();
        this.saveInitialValues();
        this.focusRect = aFocusRect;
    }
    
    public void saveInitialValues() {
        short i = 0;
        
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.values.Add(PdSingleValue().createWithSingle(this.plant.drawingScale_PixelsPerMm));
                this.oldPoints.Add(PdPointValue().createWithPoint(this.plant.basePoint_pixels()));
                this.oldSizes.Add(PdPointValue().createWithPoint(Point(usupport.rWidth(this.plant.boundsRect_pixels()), usupport.rHeight(this.plant.boundsRect_pixels()))));
            }
        }
    }
    
    public void destroy() {
        this.newScales.free;
        this.newScales = null;
        this.oldSizes.free;
        this.oldSizes = null;
        this.newPoints.free;
        this.newPoints = null;
        this.oldPoints.free;
        this.oldPoints = null;
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        float newScaleX = 0.0;
        float newScaleY = 0.0;
        int widestBox = 0;
        int tallestBox = 0;
        int tallestHeight = 0;
        TPoint offset = new TPoint();
        TPoint newPoint = new TPoint();
        PdPlant lastPlant = new PdPlant();
        int totalHeight = 0;
        int averageHeight = 0;
        int remainingX = 0;
        boolean plantScaleChanged = false;
        float newScale = 0.0;
        
        super.doCommand();
        if (this.plantList.Count <= 0) {
            return;
        }
        this.invalidateCombinedPlantRects();
        this.newScales.clear();
        this.newPoints.clear();
        lastPlant = null;
        totalHeight = 0;
        tallestHeight = 0;
        try {
            UNRESOLVED.cursor_startWait;
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    totalHeight = totalHeight + usupport.rHeight(this.plant.boundsRect_pixels());
                }
            }
            averageHeight = totalHeight / this.plantList.Count;
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.recalculateBounds(umain.kDontDrawYet);
                    plantScaleChanged = false;
                    // calculate new scale (resize based on average height)
                    newScale = umath.safedivExcept(this.plant.drawingScale_PixelsPerMm * averageHeight, usupport.rHeight(this.plant.boundsRect_pixels()) * 1.0, 0.1);
                    if (abs(newScale - this.plant.drawingScale_PixelsPerMm) > this.plant.drawingScale_PixelsPerMm / 20.0) {
                        // don't rescale and redraw plant if scale hardly changes
                        plantScaleChanged = true;
                        this.plant.drawingScale_PixelsPerMm = newScale;
                        this.plant.recalculateBounds(umain.kDontDrawYet);
                    }
                    this.newScales.Add(PdSingleValue().createWithSingle(this.plant.drawingScale_PixelsPerMm));
                    // calculate new position
                    offset.X = this.plant.basePoint_pixels().X - this.plant.boundsRect_pixels().Left;
                    offset.Y = this.plant.basePoint_pixels().Y - this.plant.boundsRect_pixels().Top;
                    remainingX = usupport.rWidth(this.plant.boundsRect_pixels()) - offset.X;
                    if ((i <= 0) || (lastPlant == null)) {
                        newPoint.X = offset.X + kGapBetweenArrangedPlants;
                        newPoint.Y = offset.Y + kGapBetweenArrangedPlants;
                    } else {
                        newPoint.X = lastPlant.boundsRect_pixels().Right + kGapBetweenArrangedPlants + offset.X;
                        newPoint.Y = lastPlant.boundsRect_pixels().Top + offset.Y;
                    }
                    if (newPoint.X + remainingX > umain.MainForm.drawingPaintBox.Width) {
                        newPoint.X = offset.X + kGapBetweenArrangedPlants;
                        newPoint.Y = tallestHeight + kGapBetweenArrangedPlants + offset.Y;
                    }
                    this.plant.moveTo(newPoint);
                    this.newPoints.Add(PdPointValue().createWithPoint(this.plant.basePoint_pixels()));
                    if (plantScaleChanged) {
                        this.plant.recalculateBounds(umain.kDrawNow);
                    } else {
                        this.plant.recalculateBoundsForOffsetChange();
                    }
                    lastPlant = this.plant;
                    if (this.plant.boundsRect_pixels().Bottom > tallestHeight) {
                        tallestHeight = this.plant.boundsRect_pixels().Bottom;
                    }
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void undoCommand() {
        short i = 0;
        float oldScale = 0.0;
        
        super.undoCommand();
        try {
            UNRESOLVED.cursor_startWait;
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    oldScale = this.plant.drawingScale_PixelsPerMm;
                    this.plant.drawingScale_PixelsPerMm = PdSingleValue(this.values.Items[i]).saveSingle;
                    this.plant.moveTo(PdPointValue(this.oldPoints.Items[i]).savePoint);
                    if (abs(this.plant.drawingScale_PixelsPerMm - oldScale) > this.plant.drawingScale_PixelsPerMm / 20.0) {
                        // don't rescale and redraw plant if scale hardly changes
                        this.plant.recalculateBounds(umain.kDrawNow);
                    } else {
                        this.plant.recalculateBoundsForOffsetChange();
                    }
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void redoCommand() {
        short i = 0;
        float oldScale = 0.0;
        
        super.undoCommand();
        try {
            UNRESOLVED.cursor_startWait;
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    oldScale = this.plant.drawingScale_PixelsPerMm;
                    this.plant.drawingScale_PixelsPerMm = PdSingleValue(this.newScales.Items[i]).saveSingle;
                    this.plant.moveTo(PdPointValue(this.newPoints.Items[i]).savePoint);
                    if (abs(this.plant.drawingScale_PixelsPerMm - oldScale) > this.plant.drawingScale_PixelsPerMm / 20.0) {
                        // don't rescale and redraw plant if scale hardly changes
                        this.plant.recalculateBounds(umain.kDrawNow);
                    } else {
                        this.plant.recalculateBoundsForOffsetChange();
                    }
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public String description() {
        result = "";
        result = "pack" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdChangeMainWindowViewingOptionCommand extends PdCommandWithListOfPlants {
    public TList selectedList;
    public float oldScale_PixelsPerMm;
    public float newScale_pixelsPerMm;
    public SinglePoint oldOffset_mm;
    public SinglePoint newOffset_mm;
    public short oldMainWindowViewingOption;
    public short newMainWindowViewingOption;
    
    // ------------------------------------------------------------ PdChangeMainWindowViewingOptionCommand 
    public void createWithListOfPlantsAndSelectedPlantsAndNewOption(TList aList, TList aSelectedList, short aNewOption) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        //hidden flag not saved
        this.commandChangesPlantFile = false;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.values.Add(PdBooleanValue().createWithBoolean(uplant.PdPlant(this.plantList.Items[i]).hidden));
            }
        }
        this.selectedList = delphi_compatability.TList().Create();
        if (aSelectedList.Count > 0) {
            for (i = 0; i <= aSelectedList.Count - 1; i++) {
                this.selectedList.Add(uplant.PdPlant(aSelectedList.Items[i]));
            }
        }
        this.oldMainWindowViewingOption = udomain.domain.options.mainWindowViewMode;
        this.newMainWindowViewingOption = aNewOption;
    }
    
    public void destroy() {
        this.selectedList.free;
        this.selectedList = null;
        super.destroy();
    }
    
    public void doCommand() {
        super.doCommand();
        try {
            UNRESOLVED.cursor_startWait;
            udomain.domain.options.mainWindowViewMode = this.newMainWindowViewingOption;
            switch (this.newMainWindowViewingOption) {
                case udomain.kViewPlantsInMainWindowOneAtATime:
                    this.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
                    this.oldOffset_mm = udomain.domain.plantDrawOffset_mm();
                    umain.MainForm.deselectAllPlantsButFirst();
                    //hides all plants but first; calls fitVisiblePlantsInDrawingArea
                    umain.MainForm.showOnePlantExclusively(umain.kDontDrawYet);
                    umain.MainForm.recalculateSelectedPlantsBoundsRects(umain.kDrawNow);
                    umain.MainForm.invalidateEntireDrawing();
                    umain.MainForm.updateForChangeToPlantSelections();
                    this.newScale_pixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
                    this.newOffset_mm = udomain.domain.plantDrawOffset_mm();
                    break;
                case udomain.kViewPlantsInMainWindowFreeFloating:
                    this.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
                    this.oldOffset_mm = udomain.domain.plantDrawOffset_mm();
                    umain.MainForm.hideOrShowSomePlants(this.plantList, null, kShow, umain.kDontDrawYet);
                    umain.MainForm.fitVisiblePlantsInDrawingArea(umain.kDontDrawYet, umain.kScaleAndMove, umain.kAlwaysMove);
                    // first drawing gets correct bounds rects so numbers get counted for progress bar - messy
                    umain.MainForm.recalculateAllPlantBoundsRects(umain.kDontDrawYet);
                    umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow);
                    umain.MainForm.invalidateEntireDrawing();
                    this.newScale_pixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
                    this.newOffset_mm = udomain.domain.plantDrawOffset_mm();
                    break;
            umain.MainForm.updateMenusForChangeToViewingOption();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            UNRESOLVED.cursor_startWait;
            udomain.domain.options.mainWindowViewMode = this.oldMainWindowViewingOption;
            switch (this.newMainWindowViewingOption) {
                case udomain.kViewPlantsInMainWindowOneAtATime:
                    umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow);
                    umain.MainForm.invalidateSelectedPlantRectangles();
                    udomain.domain.plantManager.plantDrawScale_PixelsPerMm = this.oldScale_PixelsPerMm;
                    udomain.domain.plantManager.plantDrawOffset_mm = this.oldOffset_mm;
                    // restore original hidden flags - all plants 
                    //not used
                    umain.MainForm.hideOrShowSomePlants(this.plantList, this.values, false, umain.kDontDrawYet);
                    umain.MainForm.fitVisiblePlantsInDrawingArea(umain.kDontDrawYet, umain.kScaleAndMove, umain.kAlwaysMove);
                    umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow);
                    //MainForm.invalidateSelectedPlantRectangles;
                    umain.MainForm.invalidateEntireDrawing();
                    // restore original selection - selected plants only 
                    umain.MainForm.selectedPlants.Clear();
                    if (this.selectedList.Count > 0) {
                        for (i = 0; i <= this.selectedList.Count - 1; i++) {
                            umain.MainForm.selectedPlants.Add(uplant.PdPlant(this.selectedList.Items[i]));
                        }
                    }
                    umain.MainForm.updateForChangeToPlantSelections();
                    break;
                case udomain.kViewPlantsInMainWindowFreeFloating:
                    udomain.domain.plantManager.plantDrawScale_PixelsPerMm = this.oldScale_PixelsPerMm;
                    udomain.domain.plantManager.plantDrawOffset_mm = this.oldOffset_mm;
                    // restore original hidden flags - all plants 
                    //not used
                    umain.MainForm.hideOrShowSomePlants(this.plantList, this.values, false, umain.kDontDrawYet);
                    umain.MainForm.fitVisiblePlantsInDrawingArea(umain.kDontDrawYet, umain.kScaleAndMove, umain.kAlwaysMove);
                    umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow);
                    //MainForm.invalidateSelectedPlantRectangles;
                    umain.MainForm.invalidateEntireDrawing();
                    umain.MainForm.updateForChangeToPlantSelections();
                    break;
            umain.MainForm.updateMenusForChangeToViewingOption();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public String description() {
        result = "";
        result = "change view all/one option in main window";
        return result;
    }
    
}
class PdDragCommand extends PdCommandWithListOfPlants {
    public boolean initialized;
    public boolean doneInMouseCommand;
    public boolean dragAllPlantsToOnePoint;
    public TPoint dragStartPoint;
    public TPoint offset;
    public TPoint newPoint;
    
    // ------------------------------------------------------------ PdDragCommand 
    public void createWithListOfPlantsAndDragOffset(TList aList, TPoint anOffset) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.values.Add(PdPointValue().createWithPoint(this.plant.basePoint_pixels()));
            }
        }
        this.offset = anOffset;
        this.initialized = true;
    }
    
    public void createWithListOfPlantsAndNewPoint(TList aList, TPoint aNewPoint) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        this.dragAllPlantsToOnePoint = true;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.values.Add(PdPointValue().createWithPoint(this.plant.basePoint_pixels()));
            }
        }
        this.newPoint = aNewPoint;
        this.initialized = true;
    }
    
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        short i = 0;
        
        result = this;
        if (aTrackPhase == ucommand.TrackPhase.trackPress) {
            this.dragStartPoint = nextPoint;
        } else if (aTrackPhase == ucommand.TrackPhase.trackMove) {
            if ((!this.initialized) && mouseDidMove) {
                if (this.plantList.Count > 0) {
                    for (i = 0; i <= this.plantList.Count - 1; i++) {
                        this.plant = uplant.PdPlant(this.plantList.Items[i]);
                        this.values.Add(PdPointValue().createWithPoint(this.plant.basePoint_pixels()));
                    }
                }
                this.initialized = true;
                super.doCommand();
            }
            if (this.initialized) {
                this.offset.X = nextPoint.X - this.dragStartPoint.X;
                this.offset.Y = nextPoint.Y - this.dragStartPoint.Y;
                this.invalidateCombinedPlantRects();
                if (this.plantList.Count > 0) {
                    for (i = 0; i <= this.plantList.Count - 1; i++) {
                        this.plant = uplant.PdPlant(this.plantList.Items[i]);
                        this.plant.moveTo(PdPointValue(this.values.Items[i]).savePoint);
                        this.plant.moveBy(this.offset);
                        if (udomain.domain.options.cachePlantBitmaps) {
                            this.plant.recalculateBoundsForOffsetChange();
                        }
                    }
                }
                umain.MainForm.updateForChangeToSelectedPlantsLocation();
                this.invalidateCombinedPlantRects();
                this.doneInMouseCommand = true;
            }
        } else if (aTrackPhase == ucommand.TrackPhase.trackRelease) {
            if (!mouseDidMove) {
                result = null;
                this.free;
            }
        }
        return result;
    }
    
    public void doCommand() {
        short i = 0;
        
        if (this.doneInMouseCommand) {
            //only used if not done by mouse command-otherwise done in trackMouse
            return;
        }
        super.doCommand();
        this.invalidateCombinedPlantRects();
        if (this.dragAllPlantsToOnePoint) {
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.moveTo(this.newPoint);
                    if (udomain.domain.options.cachePlantBitmaps) {
                        this.plant.recalculateBoundsForOffsetChange();
                    }
                }
            }
        } else {
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.moveBy(this.offset);
                    if (udomain.domain.options.cachePlantBitmaps) {
                        this.plant.recalculateBoundsForOffsetChange();
                    }
                }
            }
        }
        umain.MainForm.updateForChangeToSelectedPlantsLocation();
        this.invalidateCombinedPlantRects();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.moveTo(PdPointValue(this.values.Items[i]).savePoint);
                if (udomain.domain.options.cachePlantBitmaps) {
                    this.plant.recalculateBoundsForOffsetChange();
                }
            }
        }
        umain.MainForm.updateForChangeToSelectedPlantsLocation();
        this.invalidateCombinedPlantRects();
    }
    
    public void redoCommand() {
        short i = 0;
        
        if (!this.initialized) {
            return;
        }
        super.doCommand();
        this.invalidateCombinedPlantRects();
        if (this.dragAllPlantsToOnePoint) {
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.moveTo(this.newPoint);
                    if (udomain.domain.options.cachePlantBitmaps) {
                        this.plant.recalculateBoundsForOffsetChange();
                    }
                }
            }
        } else {
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.moveBy(this.offset);
                    if (udomain.domain.options.cachePlantBitmaps) {
                        this.plant.recalculateBoundsForOffsetChange();
                    }
                }
            }
        }
        umain.MainForm.updateForChangeToSelectedPlantsLocation();
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        if (this.dragAllPlantsToOnePoint) {
            result = "make bouquet";
        } else {
            result = "drag" + plantNamesForDescription(this.plantList);
        }
        return result;
    }
    
}
class PdAlignPlantsCommand extends PdCommandWithListOfPlants {
    public TListCollection newPoints;
    public TRect focusRect;
    public short alignDirection;
    
    // ------------------------------------------------------------ PdAlignPlantsCommand 
    public void createWithListOfPlantsRectAndDirection(TList aList, TRect aRect, short aDirection) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.values.Add(PdPointValue().createWithPoint(this.plant.basePoint_pixels()));
            }
        }
        this.newPoints = ucollect.TListCollection().Create();
        this.focusRect = aRect;
        this.alignDirection = aDirection;
    }
    
    public void destroy() {
        this.newPoints.free;
        this.newPoints = null;
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        TPoint newPoint = new TPoint();
        TPoint offset = new TPoint();
        
        super.doCommand();
        this.newPoints.clear();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                newPoint = this.plant.basePoint_pixels();
                offset.X = this.plant.basePoint_pixels().X - this.plant.boundsRect_pixels().Left;
                offset.Y = this.plant.basePoint_pixels().Y - this.plant.boundsRect_pixels().Top;
                switch (this.alignDirection) {
                    case kUp:
                        newPoint.Y = this.focusRect.Top + offset.Y;
                        break;
                    case kDown:
                        newPoint.Y = this.focusRect.Bottom - (usupport.rHeight(this.plant.boundsRect_pixels()) - offset.Y);
                        break;
                    case kLeft:
                        newPoint.X = this.focusRect.Left + offset.X;
                        break;
                    case kRight:
                        newPoint.X = this.focusRect.Right - (usupport.rWidth(this.plant.boundsRect_pixels()) - offset.X);
                        break;
                this.plant.moveTo(newPoint);
                this.newPoints.Add(PdPointValue().createWithPoint(this.plant.basePoint_pixels()));
                if (udomain.domain.options.cachePlantBitmaps) {
                    this.plant.recalculateBoundsForOffsetChange();
                }
            }
        }
        umain.MainForm.updateForChangeToSelectedPlantsLocation();
        this.invalidateCombinedPlantRects();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.moveTo(PdPointValue(this.values.Items[i]).savePoint);
                if (udomain.domain.options.cachePlantBitmaps) {
                    this.plant.recalculateBoundsForOffsetChange();
                }
            }
        }
        umain.MainForm.updateForChangeToSelectedPlantsLocation();
        this.invalidateCombinedPlantRects();
    }
    
    public void redoCommand() {
        short i = 0;
        
        super.doCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.moveTo(PdPointValue(this.newPoints.Items[i]).savePoint);
                if (udomain.domain.options.cachePlantBitmaps) {
                    this.plant.recalculateBoundsForOffsetChange();
                }
            }
        }
        umain.MainForm.updateForChangeToSelectedPlantsLocation();
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        result = "align" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdRotateCommand extends PdCommandWithListOfPlants {
    public short rotateDirection;
    public float newRotation;
    public float offsetRotation;
    public TPoint startDragPoint;
    
    // ------------------------------------------------------------ PdRotateCommand 
    public void createWithListOfPlantsDirectionAndNewRotation(TList aList, short aRotateDirection, short aNewRotation) {
        short i = 0;
        
        // create using this constructor if this is from clicking on a spinEdit 
        super.createWithListOfPlants(aList);
        this.rotateDirection = aRotateDirection;
        this.newRotation = aNewRotation;
        if (this.newRotation < -360) {
            this.newRotation = -360;
        }
        if (this.newRotation > 360) {
            this.newRotation = 360;
        }
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                switch (this.rotateDirection) {
                    case kRotateX:
                        this.values.Add(PdSingleValue().createWithSingle(this.plant.xRotation));
                        break;
                    case kRotateY:
                        this.values.Add(PdSingleValue().createWithSingle(this.plant.yRotation));
                        break;
                    case kRotateZ:
                        this.values.Add(PdSingleValue().createWithSingle(this.plant.zRotation));
                        break;
            }
        }
    }
    
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        short i = 0;
        float newRotation = 0.0;
        
        result = this;
        if (aTrackPhase == ucommand.TrackPhase.trackPress) {
            // assume that if this function is called, the command was not already initialized
            //    from clicking on a spinEdit, so we have no values and no rotateDirection 
            this.startDragPoint = nextPoint;
            this.invalidateCombinedPlantRects();
            super.doCommand();
        } else if (aTrackPhase == ucommand.TrackPhase.trackMove) {
            if (this.rotateDirection == kRotateNotInitialized) {
                if (rightButtonDown) {
                    this.rotateDirection = kRotateZ;
                } else if (abs(nextPoint.X - this.startDragPoint.X) > abs(nextPoint.Y - this.startDragPoint.Y)) {
                    this.rotateDirection = kRotateX;
                } else {
                    this.rotateDirection = kRotateY;
                }
                if (this.plantList.Count > 0) {
                    for (i = 0; i <= this.plantList.Count - 1; i++) {
                        this.plant = uplant.PdPlant(this.plantList.Items[i]);
                        switch (this.rotateDirection) {
                            case kRotateX:
                                this.values.Add(PdSingleValue().createWithSingle(this.plant.xRotation));
                                break;
                            case kRotateY:
                                this.values.Add(PdSingleValue().createWithSingle(this.plant.yRotation));
                                break;
                            case kRotateZ:
                                this.values.Add(PdSingleValue().createWithSingle(this.plant.zRotation));
                                break;
                    }
                }
            }
            this.invalidateCombinedPlantRects();
            switch (this.rotateDirection) {
                case kRotateX:
                    this.offsetRotation = (nextPoint.X - this.startDragPoint.X) * 0.5;
                    break;
                case kRotateY:
                    this.offsetRotation = (nextPoint.Y - this.startDragPoint.Y) * 0.5;
                    break;
                case kRotateZ:
                    this.offsetRotation = (nextPoint.X - this.startDragPoint.X) * 0.5;
                    break;
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    newRotation = PdSingleValue(this.values.Items[i]).saveSingle + this.offsetRotation;
                    if (newRotation < -360) {
                        newRotation = 360 - (abs(newRotation) - 360);
                    }
                    if (newRotation > 360) {
                        newRotation = -360 + (newRotation - 360);
                    }
                    switch (this.rotateDirection) {
                        case kRotateX:
                            this.plant.xRotation = newRotation;
                            break;
                        case kRotateY:
                            this.plant.yRotation = newRotation;
                            break;
                        case kRotateZ:
                            this.plant.zRotation = newRotation;
                            break;
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToPlantRotations();
        } else if (aTrackPhase == ucommand.TrackPhase.trackRelease) {
            if (!mouseDidMove) {
                // if they just clicked, rotate ten degrees anyway
                this.invalidateCombinedPlantRects();
                if (this.plantList.Count > 0) {
                    for (i = 0; i <= this.plantList.Count - 1; i++) {
                        this.plant = uplant.PdPlant(this.plantList.Items[i]);
                        this.values.Add(PdSingleValue().createWithSingle(this.plant.xRotation));
                    }
                }
                this.rotateDirection = kRotateX;
                if (rightButtonDown) {
                    // v2.0 if they just clicked with the right mouse button, rotate -10 degrees
                    // v2.0 use the domain rotation increment instead of always 10 degrees
                    this.offsetRotation = -udomain.domain.options.rotationIncrement;
                } else {
                    this.offsetRotation = udomain.domain.options.rotationIncrement;
                }
                if (this.plantList.Count > 0) {
                    for (i = 0; i <= this.plantList.Count - 1; i++) {
                        this.plant = uplant.PdPlant(this.plantList.Items[i]);
                        newRotation = PdSingleValue(this.values.Items[i]).saveSingle + this.offsetRotation;
                        if (newRotation < -360) {
                            newRotation = 360 - (abs(newRotation) - 360);
                        }
                        if (newRotation > 360) {
                            newRotation = -360 + (newRotation - 360);
                        }
                        this.plant.xRotation = newRotation;
                        this.plant.recalculateBounds(umain.kDrawNow);
                    }
                }
                this.invalidateCombinedPlantRects();
                umain.MainForm.updateForChangeToPlantRotations();
            }
        }
        return result;
    }
    
    public void doCommand() {
        short i = 0;
        
        if (this.done) {
            //if done in mousemove 
            return;
        }
        super.doCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                switch (this.rotateDirection) {
                    case kRotateX:
                        if (this.offsetRotation != 0) {
                            this.plant.xRotation = umath.min(360, umath.max(-360, PdSingleValue(this.values.Items[i]).saveSingle + this.offsetRotation));
                        } else {
                            this.plant.xRotation = this.newRotation;
                        }
                        break;
                    case kRotateY:
                        if (this.offsetRotation != 0) {
                            this.plant.yRotation = umath.min(360, umath.max(-360, PdSingleValue(this.values.Items[i]).saveSingle + this.offsetRotation));
                        } else {
                            this.plant.yRotation = this.newRotation;
                        }
                        break;
                    case kRotateZ:
                        if (this.offsetRotation != 0) {
                            this.plant.zRotation = umath.min(360, umath.max(-360, PdSingleValue(this.values.Items[i]).saveSingle + this.offsetRotation));
                        } else {
                            this.plant.zRotation = this.newRotation;
                        }
                        break;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        umain.MainForm.updateForChangeToPlantRotations();
        this.invalidateCombinedPlantRects();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                switch (this.rotateDirection) {
                    case kRotateX:
                        this.plant.xRotation = PdSingleValue(this.values.Items[i]).saveSingle;
                        break;
                    case kRotateY:
                        this.plant.yRotation = PdSingleValue(this.values.Items[i]).saveSingle;
                        break;
                    case kRotateZ:
                        this.plant.zRotation = PdSingleValue(this.values.Items[i]).saveSingle;
                        break;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        umain.MainForm.updateForChangeToPlantRotations();
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        result = nameForDirection(this.rotateDirection) + " rotate" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdResetRotationsCommand extends PdCommandWithListOfPlants {
    public float oldX;
    public float oldY;
    public float oldZ;
    
    // ------------------------------------------------------------ PdResetRotationsCommand 
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.values.Add(PdXYZValue().createWithXYZ(this.plant.xRotation, this.plant.yRotation, this.plant.zRotation));
                this.plant.xRotation = 0;
                this.plant.yRotation = 0;
                this.plant.zRotation = 0;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
        umain.MainForm.updateForChangeToPlantRotations();
    }
    
    public void redoCommand() {
        short i = 0;
        
        super.doCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.xRotation = 0;
                this.plant.yRotation = 0;
                this.plant.zRotation = 0;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
        umain.MainForm.updateForChangeToPlantRotations();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.xRotation = PdXYZValue(this.values.Items[i]).x;
                this.plant.yRotation = PdXYZValue(this.values.Items[i]).y;
                this.plant.zRotation = PdXYZValue(this.values.Items[i]).z;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
        umain.MainForm.updateForChangeToPlantRotations();
    }
    
    public String description() {
        result = "";
        result = "reset rotation for" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdChangeDrawingScaleCommand extends PdCommandWithListOfPlants {
    public float newScale;
    
    // ------------------------------------------------------------ PdChangeDrawingScaleCommand 
    public void createWithListOfPlantsAndNewScale(TList aList, float aNewScale) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        this.newScale = aNewScale;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.values.Add(PdSingleValue().createWithSingle(uplant.PdPlant(this.plantList.Items[i]).drawingScale_PixelsPerMm));
            }
        }
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.drawingScale_PixelsPerMm = this.newScale;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.drawingScale_PixelsPerMm = PdSingleValue(this.values.Items[i]).saveSingle;
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        result = "change scale for" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdChangePlantAgeCommand extends PdCommandWithListOfPlants {
    public short newAge;
    
    // ----------------------------------------------------------------------- PdChangePlantAgeCommand 
    public void createWithListOfPlantsAndNewAge(TList aList, short aNewAge) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        this.newAge = aNewAge;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.values.Add(PdSmallintValue().createWithSmallint(uplant.PdPlant(this.plantList.Items[i]).age));
            }
        }
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            UNRESOLVED.cursor_startWait;
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    // if primary selected plant has longer lifespan than other selected plants, cut off age
                    //        at max for those plants 
                    this.plant.setAge(umath.intMin(this.newAge, this.plant.pGeneral.ageAtMaturity));
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsLocation();
            // changing age causes life cycle panel to need to redraw 
            umain.MainForm.updateLifeCyclePanelForFirstSelectedPlant();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        try {
            UNRESOLVED.cursor_startWait;
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.setAge(PdSmallintValue(this.values.Items[i]).saveSmallint);
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsLocation();
            // changing age causes life cycle panel to need to redraw 
            umain.MainForm.updateLifeCyclePanelForFirstSelectedPlant();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    // redo is same as do 
    public String description() {
        result = "";
        result = "change age to " + IntToStr(this.newAge) + " for" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdAnimatePlantCommand extends PdCommandWithListOfPlants {
    public short age;
    public short oldestAgeAtMaturity;
    
    // ----------------------------------------------------------------------- PdAnimatePlantCommand 
    public void createWithListOfPlants(TList aList) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.values.Add(PdSmallintValue().createWithSmallint(uplant.PdPlant(this.plantList.Items[i]).age));
            }
        }
    }
    
    public void doCommand() {
        short i = 0;
        PdPlant plant = new PdPlant();
        
        super.doCommand();
        if (this.plantList.Count <= 0) {
            return;
        }
        this.age = 0;
        // find oldest age 
        this.oldestAgeAtMaturity = 0;
        for (i = 0; i <= this.plantList.Count - 1; i++) {
            plant = uplant.PdPlant(this.plantList.Items[i]);
            if ((i == 0) || (plant.pGeneral.ageAtMaturity > this.oldestAgeAtMaturity)) {
                this.oldestAgeAtMaturity = plant.pGeneral.ageAtMaturity;
            }
        }
        // reset all plants to age zero and draw them 
        udomain.domain.temporarilyHideSelectionRectangles = true;
        this.invalidateCombinedPlantRects();
        try {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                plant = uplant.PdPlant(this.plantList.Items[i]);
                plant.reset();
                plant.recalculateBounds(umain.kDrawNow);
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForPossibleChangeToDrawing();
        } finally {
            udomain.domain.temporarilyHideSelectionRectangles = false;
        }
        umain.MainForm.animateCommand = this;
        umain.MainForm.startAnimation();
    }
    
    public void animateOneDay() {
        short i = 0;
        PdPlant plant = new PdPlant();
        
        // grow all plants one day 
        udomain.domain.temporarilyHideSelectionRectangles = true;
        try {
            this.invalidateCombinedPlantRects();
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                plant = uplant.PdPlant(this.plantList.Items[i]);
                if (this.age < plant.pGeneral.ageAtMaturity) {
                    plant.nextDay();
                    plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            if (umain.MainForm.lifeCycleShowing()) {
                // don't want to update params, because they don't change during animation 
                umain.MainForm.updateLifeCyclePanelForFirstSelectedPlant();
            } else if (umain.MainForm.statsShowing()) {
                umain.MainForm.updateStatisticsPanelForFirstSelectedPlant();
            }
            umain.MainForm.updateForPossibleChangeToDrawing();
            this.age += 1;
        } finally {
            udomain.domain.temporarilyHideSelectionRectangles = false;
        }
        if (this.age >= this.oldestAgeAtMaturity) {
            umain.MainForm.stopAnimation();
        }
        umain.MainForm.updateForChangeToSelectedPlantsLocation();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        try {
            UNRESOLVED.cursor_startWait;
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.plant.setAge(PdSmallintValue(this.values.Items[i]).saveSmallint);
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
            umain.MainForm.updateForChangeToSelectedPlantsLocation();
            // changing age causes life cycle panel to need to redraw 
            umain.MainForm.updateLifeCyclePanelForFirstSelectedPlant();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    // redo is same as do 
    public String description() {
        result = "";
        result = "animate" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdHideOrShowCommand extends PdCommandWithListOfPlants {
    public boolean hide;
    public TListCollection newValues;
    
    // ------------------------------------------------------------ PdHideOrShowCommand 
    public void createWithListOfPlantsAndHideOrShow(TList aList, boolean aHide) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        //hidden flag not saved
        this.commandChangesPlantFile = false;
        this.hide = aHide;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.values.Add(PdBooleanValue().createWithBoolean(uplant.PdPlant(this.plantList.Items[i]).hidden));
            }
        }
    }
    
    public void createWithListOfPlantsAndListOfHides(TList aList, TListCollection aHideList) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        //hidden flag not saved
        this.commandChangesPlantFile = false;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.values.Add(PdBooleanValue().createWithBoolean(uplant.PdPlant(this.plantList.Items[i]).hidden));
            }
        }
        this.newValues = ucollect.TListCollection().Create();
        if (aHideList.Count > 0) {
            for (i = 0; i <= aHideList.Count - 1; i++) {
                this.newValues.Add(PdBooleanValue().createWithBoolean(PdBooleanValue(aHideList.Items[i]).saveBoolean));
            }
        }
    }
    
    public void destroy() {
        this.newValues.free;
        this.newValues = null;
        super.destroy();
    }
    
    public void doCommand() {
        super.doCommand();
        umain.MainForm.hideOrShowSomePlants(this.plantList, this.newValues, this.hide, umain.kDontDrawYet);
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        umain.MainForm.hideOrShowSomePlants(this.plantList, this.values, this.hide, umain.kDontDrawYet);
    }
    
    public String description() {
        result = "";
        if ((this.newValues != null) && (this.newValues.Count > 0)) {
            result = "hide others";
        } else if (this.hide) {
            result = "hide" + plantNamesForDescription(this.plantList);
        } else {
            result = "show" + plantNamesForDescription(this.plantList);
        }
        return result;
    }
    
}
class PdRandomizeCommand extends PdCommandWithListOfPlants {
    public TListCollection oldSeeds;
    public TListCollection oldBreedingSeeds;
    public TListCollection newSeeds;
    public TListCollection newBreedingSeeds;
    public TListCollection oldXRotations;
    public TListCollection newXRotations;
    public boolean isInBreeder;
    public boolean isRandomizeAllInBreeder;
    
    // ----------------------------------------------------------------------- PdRandomizeCommand 
    public void createWithListOfPlants(TList aList) {
        super.createWithListOfPlants(aList);
        this.oldSeeds = ucollect.TListCollection().Create();
        this.oldBreedingSeeds = ucollect.TListCollection().Create();
        this.newSeeds = ucollect.TListCollection().Create();
        this.newBreedingSeeds = ucollect.TListCollection().Create();
        this.oldXRotations = ucollect.TListCollection().Create();
        this.newXRotations = ucollect.TListCollection().Create();
        this.setUpToRemoveAmendmentsWhenDone();
    }
    
    public void destroy() {
        this.oldSeeds.free;
        this.oldSeeds = null;
        this.oldBreedingSeeds.free;
        this.oldBreedingSeeds = null;
        this.newSeeds.free;
        this.newSeeds = null;
        this.newBreedingSeeds.free;
        this.newBreedingSeeds = null;
        this.oldXRotations.free;
        this.oldXRotations = null;
        this.newXRotations.free;
        this.newXRotations = null;
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            UNRESOLVED.cursor_startWait;
            if (!this.isInBreeder) {
                this.invalidateCombinedPlantRects();
            }
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.oldSeeds.Add(PdSmallintValue().createWithSmallint(this.plant.pGeneral.startingSeedForRandomNumberGenerator));
                    this.oldBreedingSeeds.Add(PdLongintValue().createWithLongint(this.plant.breedingGenerator.seed));
                    this.oldXRotations.Add(PdSingleValue().createWithSingle(this.plant.xRotation));
                    this.plant.randomize();
                    this.newSeeds.Add(PdSmallintValue().createWithSmallint(this.plant.pGeneral.startingSeedForRandomNumberGenerator));
                    this.newBreedingSeeds.Add(PdLongintValue().createWithLongint(this.plant.breedingGenerator.seed));
                    this.newXRotations.Add(PdSingleValue().createWithSingle(this.plant.xRotation));
                    if (this.isInBreeder) {
                        this.plant.previewCacheUpToDate = false;
                    } else {
                        this.plant.recalculateBounds(umain.kDrawNow);
                    }
                }
            }
            if (this.isInBreeder) {
                if (this.plantList.Count == 1) {
                    this.plant = uplant.PdPlant(this.plantList.Items[0]);
                    ubreedr.BreederForm.updateForChangeToPlant(this.plant);
                } else {
                    ubreedr.BreederForm.updateForChangeToGenerations();
                }
            } else {
                this.invalidateCombinedPlantRects();
                umain.MainForm.updateForChangeToPlantRotations();
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void undoCommand() {
        short i = 0;
        short seed = 0;
        long breedingSeed = 0;
        float xRotation = 0.0;
        
        super.undoCommand();
        try {
            UNRESOLVED.cursor_startWait;
            if (!this.isInBreeder) {
                this.invalidateCombinedPlantRects();
            }
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    seed = PdSmallintValue(this.oldSeeds.Items[i]).saveSmallint;
                    breedingSeed = PdLongintValue(this.oldBreedingSeeds.Items[i]).saveLongint;
                    xRotation = PdSingleValue(this.oldXRotations.Items[i]).saveSingle;
                    this.plant.randomizeWithSeedsAndXRotation(seed, breedingSeed, xRotation);
                    if (this.isInBreeder) {
                        this.plant.previewCacheUpToDate = false;
                    } else {
                        this.plant.recalculateBounds(umain.kDrawNow);
                    }
                }
            }
            if (this.isInBreeder) {
                if (this.plantList.Count == 1) {
                    this.plant = uplant.PdPlant(this.plantList.Items[0]);
                    ubreedr.BreederForm.updateForChangeToPlant(this.plant);
                } else {
                    ubreedr.BreederForm.updateForChangeToGenerations();
                }
            } else {
                this.invalidateCombinedPlantRects();
                umain.MainForm.updateForChangeToPlantRotations();
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void redoCommand() {
        short i = 0;
        short seed = 0;
        long breedingSeed = 0;
        float xRotation = 0.0;
        
        super.doCommand();
        try {
            UNRESOLVED.cursor_startWait;
            if (!this.isInBreeder) {
                this.invalidateCombinedPlantRects();
            }
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    seed = PdSmallintValue(this.newSeeds.Items[i]).saveSmallint;
                    breedingSeed = PdLongintValue(this.newBreedingSeeds.Items[i]).saveLongint;
                    xRotation = PdSingleValue(this.newXRotations.Items[i]).saveSingle;
                    this.plant.randomizeWithSeedsAndXRotation(seed, breedingSeed, xRotation);
                    if (this.isInBreeder) {
                        this.plant.previewCacheUpToDate = false;
                    } else {
                        this.plant.recalculateBounds(umain.kDrawNow);
                    }
                }
            }
            if (this.isInBreeder) {
                if (this.plantList.Count == 1) {
                    this.plant = uplant.PdPlant(this.plantList.Items[0]);
                    ubreedr.BreederForm.updateForChangeToPlant(this.plant);
                } else {
                    ubreedr.BreederForm.updateForChangeToGenerations();
                }
            } else {
                this.invalidateCombinedPlantRects();
                umain.MainForm.updateForChangeToPlantRotations();
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public String description() {
        result = "";
        if (this.isRandomizeAllInBreeder) {
            result = "randomize all in breeder";
        } else if (this.isInBreeder) {
            result = "randomize in breeder";
        } else {
            result = "randomize" + plantNamesForDescription(this.plantList);
        }
        return result;
    }
    
}
// -------------------------------------------------------------- commands that add plants, no special superclass 
class PdPasteCommand extends PdCommandWithListOfPlants {
    public boolean useSpecialPastePosition;
    public TList oldSelectedList;
    
    // doesn't use values, but uses plantList 
    // v2.0
    // --------------------------------------------------------------------------------------------- PdPasteCommand 
    public void createWithListOfPlantsAndOldSelectedList(TList aList, TList anOldSelectedList) {
        short i = 0;
        
        super.createWithListOfPlants(aList);
        // selected list is just pointers, this doesn't take control of them
        this.oldSelectedList = delphi_compatability.TList().Create();
        if ((anOldSelectedList != null) && (anOldSelectedList.Count > 0)) {
            for (i = 0; i <= anOldSelectedList.Count - 1; i++) {
                this.oldSelectedList.Add(anOldSelectedList.Items[i]);
            }
        }
    }
    
    public void destroy() {
        short i = 0;
        
        this.oldSelectedList.free;
        this.oldSelectedList = null;
        if ((!this.done) && (this.plantList != null) && (this.plantList.Count > 0)) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                // free copies of pasted plants if change was undone 
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                this.plant.free;
            }
        }
        //will free plantList TList
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        result = 0;
        if ((!this.done) && (this.plantList != null)) {
            result = this.plantList.Count;
        }
        return result;
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        if (this.plantList.Count <= 0) {
            return;
        }
        // make new plants the only selected plants 
        umain.MainForm.deselectAllPlants();
        for (i = 0; i <= this.plantList.Count - 1; i++) {
            this.plant = uplant.PdPlant(this.plantList.Items[i]);
            // put new plants at end of plant manager list 
            udomain.domain.plantManager.plants.add(this.plant);
            if (!this.useSpecialPastePosition) {
                if (!udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
                    this.plant.moveTo(umain.MainForm.standardPastePosition());
                    if (!this.plant.justCopiedFromMainWindow) {
                        this.plant.calculateDrawingScaleToLookTheSameWithDomainScale();
                    }
                }
            }
            this.plant.recalculateBounds(umain.kDrawNow);
            umain.MainForm.addSelectedPlant(this.plant, kAddAtEnd);
        }
        umain.MainForm.updateForChangeToPlantList();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.plantList.Count <= 0) {
            return;
        }
        for (i = 0; i <= this.plantList.Count - 1; i++) {
            this.plant = uplant.PdPlant(this.plantList.Items[i]);
            udomain.domain.plantManager.plants.remove(this.plant);
            umain.MainForm.removeSelectedPlant(this.plant);
        }
        if (this.oldSelectedList.Count > 0) {
            for (i = 0; i <= this.oldSelectedList.Count - 1; i++) {
                // put back selections from before paste
                umain.MainForm.selectedPlants.Add(this.oldSelectedList.Items[i]);
            }
        }
        umain.MainForm.updateForChangeToPlantList();
    }
    
    public String description() {
        result = "";
        result = "paste" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdDuplicateCommand extends PdCommandWithListOfPlants {
    public TPoint startDragPoint;
    public TPoint offset;
    public TList newPlants;
    public boolean inTrackMouse;
    
    // ------------------------------------------------------------------------ PdDuplicateCommand 
    public void createWithListOfPlants(TList aList) {
        super.createWithListOfPlants(aList);
        this.newPlants = delphi_compatability.TList().Create();
    }
    
    public void destroy() {
        short i = 0;
        
        if ((!this.done) && (this.newPlants != null) && (this.newPlants.Count > 0)) {
            for (i = 0; i <= this.newPlants.Count - 1; i++) {
                // free copies of created plants if change was undone 
                this.plant = uplant.PdPlant(this.newPlants.Items[i]);
                this.plant.free;
            }
        }
        this.newPlants.free;
        this.newPlants = null;
        //will free plantList
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        result = 0;
        if ((!this.done) && (this.newPlants != null)) {
            result = this.newPlants.Count;
        }
        return result;
    }
    
    public PdCommand TrackMouse(TrackPhase aTrackPhase, TPoint anchorPoint, TPoint previousPoint, TPoint nextPoint, boolean mouseDidMove, boolean rightButtonDown) {
        result = new PdCommand();
        short i = 0;
        PdPlant originalPlant = new PdPlant();
        
        result = this;
        if (aTrackPhase == ucommand.TrackPhase.trackPress) {
            pass
        } else if (aTrackPhase == ucommand.TrackPhase.trackMove) {
            if (!this.done && mouseDidMove) {
                this.startDragPoint = nextPoint;
                this.inTrackMouse = true;
                this.doCommand();
            }
            if (!this.done) {
                return result;
            }
            if (!delphi_compatability.PtInRect(umain.MainForm.drawingPaintBox.ClientRect, nextPoint)) {
                this.undoCommand();
                result = null;
                this.free;
            } else {
                this.offset.X = nextPoint.X - this.startDragPoint.X;
                this.offset.Y = nextPoint.Y - this.startDragPoint.Y;
                if (this.newPlants.Count > 0) {
                    for (i = 0; i <= this.newPlants.Count - 1; i++) {
                        this.plant = uplant.PdPlant(this.newPlants.Items[i]);
                        if ((i <= this.plantList.Count - 1)) {
                            originalPlant = uplant.PdPlant(this.plantList.Items[i]);
                            umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
                            this.plant.moveTo(originalPlant.basePoint_pixels());
                            this.plant.moveBy(this.offset);
                            // only draw if don't have picture yet
                            this.plant.recalculateBounds(this.plant.previewCache.Width < 5);
                            umain.MainForm.invalidateDrawingRect(this.plant.boundsRect_pixels());
                        }
                    }
                }
            }
        } else if (aTrackPhase == ucommand.TrackPhase.trackRelease) {
            if (!mouseDidMove) {
                result = null;
                this.free;
            }
        }
        return result;
    }
    
    public void doCommand() {
        short i = 0;
        PdPlant plantCopy = new PdPlant();
        
        if (this.done) {
            // should have been done in the mouse down, unless it was done by a menu command 
            return;
        }
        super.doCommand();
        if (this.plantList.Count <= 0) {
            return;
        }
        // make new plants only selected plants 
        umain.MainForm.deselectAllPlants();
        for (i = 0; i <= this.plantList.Count - 1; i++) {
            this.plant = uplant.PdPlant(this.plantList.Items[i]);
            plantCopy = uplant.PdPlant().create();
            this.plant.copyTo(plantCopy);
            plantCopy.shrinkPreviewCache();
            plantCopy.setName("Copy of " + plantCopy.getName());
            if (!this.inTrackMouse) {
                plantCopy.moveBy(Point(kPasteMoveDistance, 0));
            }
            plantCopy.recalculateBounds(umain.kDrawNow);
            this.newPlants.Add(plantCopy);
            udomain.domain.plantManager.addPlant(plantCopy);
            umain.MainForm.addSelectedPlant(plantCopy, kAddAtEnd);
        }
        umain.MainForm.updateForChangeToPlantList();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.newPlants.Count <= 0) {
            return;
        }
        for (i = 0; i <= this.newPlants.Count - 1; i++) {
            this.plant = uplant.PdPlant(this.newPlants.Items[i]);
            udomain.domain.plantManager.plants.remove(this.plant);
            umain.MainForm.removeSelectedPlant(this.plant);
        }
        umain.MainForm.updateForChangeToPlantList();
    }
    
    public void redoCommand() {
        short i = 0;
        
        super.doCommand();
        if (this.newPlants.Count <= 0) {
            return;
        }
        umain.MainForm.deselectAllPlants();
        for (i = 0; i <= this.newPlants.Count - 1; i++) {
            this.plant = uplant.PdPlant(this.newPlants.Items[i]);
            udomain.domain.plantManager.addPlant(this.plant);
            umain.MainForm.addSelectedPlant(this.plant, kAddAtEnd);
        }
        umain.MainForm.updateForChangeToPlantList();
    }
    
    public String description() {
        result = "";
        result = "duplicate" + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
// -------------------------------------------------------------------------------- remove command is unique 
class PdRemoveCommand extends PdCommandWithListOfPlants {
    public TList removedPlants;
    public boolean copyToClipboard;
    
    // doesn't use values, but uses plantList 
    // --------------------------------------------------------------------------------------------- PdRemoveCommand 
    public void createWithListOfPlantsAndClipboardFlag(TList aList, boolean aCopyToClipboard) {
        super.createWithListOfPlants(aList);
        this.removedPlants = delphi_compatability.TList().Create();
        this.copyToClipboard = aCopyToClipboard;
    }
    
    public void destroy() {
        short i = 0;
        
        if ((this.done) && (this.removedPlants != null) && (this.removedPlants.Count > 0)) {
            for (i = 0; i <= this.removedPlants.Count - 1; i++) {
                // free copies of cut plants if change was done 
                this.plant = uplant.PdPlant(this.removedPlants.Items[i]);
                this.plant.free;
            }
        }
        this.removedPlants.free;
        this.removedPlants = null;
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        result = 0;
        if ((this.done) && (this.removedPlants != null)) {
            result = this.removedPlants.Count;
        }
        return result;
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        if (this.plantList.Count <= 0) {
            return;
        }
        if (this.copyToClipboard) {
            // copy plants 
            umain.MainForm.copySelectedPlantsToClipboard();
        }
        // save copy of plants before deleting 
        this.removedPlants.Clear();
        for (i = 0; i <= this.plantList.Count - 1; i++) {
            // don't remove plants from plant manager and MainForm.selectedPlants until all indexes have been recorded 
            this.plant = uplant.PdPlant(this.plantList.Items[i]);
            this.removedPlants.Add(this.plant);
            this.plant.indexWhenRemoved = udomain.domain.plantManager.plants.indexOf(this.plant);
            this.plant.selectedIndexWhenRemoved = umain.MainForm.selectedPlants.IndexOf(this.plant);
        }
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                udomain.domain.plantManager.plants.remove(this.plant);
                umain.MainForm.removeSelectedPlant(this.plant);
            }
        }
        umain.MainForm.updateForChangeToPlantList();
        if (udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
            // if only looking at one, select first in list so you are not left with nothing
            umain.MainForm.selectFirstPlantInPlantList();
            umain.MainForm.showOnePlantExclusively(umain.kDrawNow);
        }
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
            // remove selection if created
            umain.MainForm.deselectAllPlants();
        }
        if (this.removedPlants.Count > 0) {
            for (i = 0; i <= this.removedPlants.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.removedPlants.Items[i]);
                if ((this.plant.indexWhenRemoved >= 0) && (this.plant.indexWhenRemoved <= udomain.domain.plantManager.plants.count - 1)) {
                    udomain.domain.plantManager.plants.insert(this.plant.indexWhenRemoved, this.plant);
                } else {
                    udomain.domain.plantManager.plants.add(this.plant);
                }
                // all removed plants must have been selected, so also add them to the selected list 
                umain.MainForm.addSelectedPlant(this.plant, this.plant.selectedIndexWhenRemoved);
            }
        }
        umain.MainForm.updateForChangeToPlantList();
    }
    
    public String description() {
        result = "";
        if (this.copyToClipboard) {
            result = "cut" + plantNamesForDescription(this.plantList);
        } else {
            result = "delete" + plantNamesForDescription(this.plantList);
        }
        return result;
    }
    
}
// ---------------------------------------------------------------------------------- domain change commands 
class PdChangeValueCommand extends PdCommandWithListOfPlants {
    public short fieldNumber;
    public boolean regrow;
    
    // ------------------------------------------------------------------------------- value change commands 
    // -------------------------------------------------------------------------------- PdChangeValueCommand 
    public void createCommandWithListOfPlants(TList aList, short aFieldNumber, boolean aRegrow) {
        super.createWithListOfPlants(aList);
        this.fieldNumber = aFieldNumber;
        this.regrow = aRegrow;
        if (this.regrow) {
            this.setUpToRemoveAmendmentsWhenDone();
        }
    }
    
    public String description() {
        result = "";
        PdParameter param = new PdParameter();
        
        result = "";
        param = null;
        if ((udomain.domain != null) && (udomain.domain.parameterManager != null)) {
            // subclasses may want to call 
            param = udomain.domain.parameterManager.parameterForFieldNumber(this.fieldNumber);
            if ((param != null)) {
                result = "\"" + param.getName() + "\"";
            }
        }
        return result;
    }
    
}
class PdChangeRealValueCommand extends PdChangeValueCommand {
    public float newValue;
    public short arrayIndex;
    
    // ------------------------------------------------------------ PdChangeRealValueCommand 
    public void createCommandWithListOfPlants(TList aList, float aNewValue, short aFieldNumber, short anArrayIndex, boolean aRegrow) {
        float oldValue = 0.0;
        short i = 0;
        
        super.createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
        this.newValue = aNewValue;
        this.arrayIndex = anArrayIndex;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = this.plant.editTransferField(umath.kGetField, oldValue, this.fieldNumber, uparams.kFieldFloat, this.arrayIndex, this.regrow);
                this.values.Add(PdSingleValue().createWithSingle(oldValue));
            }
        }
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            if (this.regrow) {
                UNRESOLVED.cursor_startWait;
            }
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.newValue = this.plant.editTransferField(umath.kSetField, this.newValue, this.fieldNumber, uparams.kFieldFloat, this.arrayIndex, this.regrow);
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
        } finally {
            if (this.regrow) {
                UNRESOLVED.cursor_stopWait;
            }
        }
    }
    
    public void undoCommand() {
        float oldValue = 0.0;
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = PdSingleValue(this.values.Items[i]).saveSingle;
                oldValue = this.plant.editTransferField(umath.kSetField, oldValue, this.fieldNumber, uparams.kFieldFloat, this.arrayIndex, this.regrow);
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        result = super.description();
        result = "change " + result;
        if (this.arrayIndex != -1) {
            result = result + " (" + IntToStr(this.arrayIndex + 1) + ")";
        }
        result = result + " to " + usupport.digitValueString(this.newValue) + " in " + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdChangeSCurvePointValueCommand extends PdChangeValueCommand {
    public float newX;
    public float newY;
    public short pointIndex;
    
    // ------------------------------------------------------------ PdChangeSCurvePointValueCommand 
    public void createCommandWithListOfPlants(TList aList, float aNewX, float aNewY, short aFieldNumber, short aPointIndex, boolean aRegrow) {
        float oldX = 0.0;
        float oldY = 0.0;
        short i = 0;
        
        super.createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
        this.newX = aNewX;
        this.newY = aNewY;
        this.pointIndex = aPointIndex;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldX = this.plant.editTransferField(umath.kGetField, oldX, this.fieldNumber, uparams.kFieldFloat, this.pointIndex * 2, this.regrow);
                oldY = this.plant.editTransferField(umath.kGetField, oldY, this.fieldNumber, uparams.kFieldFloat, this.pointIndex * 2 + 1, this.regrow);
                this.values.Add(PdSinglePointValue().createWithSingleXY(oldX, oldY));
            }
        }
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            if (this.regrow) {
                UNRESOLVED.cursor_startWait;
            }
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    // first time, set values without calculating
                    this.plant.changingWholeSCurves = true;
                    this.newX = this.plant.editTransferField(umath.kSetField, this.newX, this.fieldNumber, uparams.kFieldFloat, this.pointIndex * 2, this.regrow);
                    this.newY = this.plant.editTransferField(umath.kSetField, this.newY, this.fieldNumber, uparams.kFieldFloat, this.pointIndex * 2 + 1, this.regrow);
                    // second time, now that both values are set, set first one again to calc s curve
                    this.plant.changingWholeSCurves = false;
                    this.newX = this.plant.editTransferField(umath.kSetField, this.newX, this.fieldNumber, uparams.kFieldFloat, this.pointIndex * 2, this.regrow);
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
        } finally {
            if (this.regrow) {
                UNRESOLVED.cursor_stopWait;
            }
        }
    }
    
    public void undoCommand() {
        float oldX = 0.0;
        float oldY = 0.0;
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldX = PdSinglePointValue(this.values.Items[i]).x;
                oldY = PdSinglePointValue(this.values.Items[i]).y;
                oldX = this.plant.editTransferField(umath.kSetField, oldX, this.fieldNumber, uparams.kFieldFloat, this.pointIndex * 2, this.regrow);
                oldY = this.plant.editTransferField(umath.kSetField, oldY, this.fieldNumber, uparams.kFieldFloat, this.pointIndex * 2 + 1, this.regrow);
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        result = super.description();
        result = "change " + result + " point " + IntToStr(this.pointIndex + 1) + " to (" + usupport.digitValueString(this.newX) + ", " + usupport.digitValueString(this.newY) + ")" + " in " + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdChangeColorValueCommand extends PdChangeValueCommand {
    public TColorRef newColor;
    
    // ------------------------------------------------------------ PdChangeColorValueCommand 
    public void createCommandWithListOfPlants(TList aList, TColorRef aNewValue, short aFieldNumber, short anArrayIndex, boolean aRegrow) {
        TColorRef oldValue = new TColorRef();
        short i = 0;
        
        super.createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
        this.newColor = aNewValue;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = this.plant.editTransferField(umath.kGetField, oldValue, this.fieldNumber, uparams.kFieldColor, uparams.kNotArray, this.regrow);
                this.values.Add(PdColorValue().createWithColor(oldValue));
            }
        }
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            if (this.regrow) {
                UNRESOLVED.cursor_startWait;
            }
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.newColor = this.plant.editTransferField(umath.kSetField, this.newColor, this.fieldNumber, uparams.kFieldColor, uparams.kNotArray, this.regrow);
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
        } finally {
            if (this.regrow) {
                UNRESOLVED.cursor_stopWait;
            }
        }
    }
    
    public void undoCommand() {
        TColorRef oldValue = new TColorRef();
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = PdColorValue(this.values.Items[i]).saveColor;
                oldValue = this.plant.editTransferField(umath.kSetField, oldValue, this.fieldNumber, uparams.kFieldColor, uparams.kNotArray, this.regrow);
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        result = super.description();
        result = "change " + result + " to (R " + IntToStr(UNRESOLVED.getRValue(this.newColor)) + ", G " + IntToStr(UNRESOLVED.getGValue(this.newColor)) + ", B " + IntToStr(UNRESOLVED.getBValue(this.newColor)) + ")" + " in " + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdChangeTdoValueCommand extends PdChangeValueCommand {
    public KfObject3D newTdo;
    
    // ------------------------------------------------------------ PdChangeTdoValueCommand 
    public void createCommandWithListOfPlants(TList aList, KfObject3D aNewValue, short aFieldNumber, boolean aRegrow) {
        KfObject3D valueTdo = new KfObject3D();
        short i = 0;
        
        super.createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
        this.newTdo = utdo.KfObject3D().create();
        this.newTdo.copyFrom(aNewValue);
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                valueTdo = utdo.KfObject3D().create();
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                valueTdo = this.plant.editTransferField(umath.kGetField, valueTdo, this.fieldNumber, uparams.kFieldThreeDObject, uparams.kNotArray, this.regrow);
                this.values.Add(valueTdo);
            }
        }
    }
    
    public void destroy() {
        this.newTdo.free;
        this.newTdo = null;
        // value tdos will be freed by values listCollection 
        super.destroy();
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            if (this.regrow) {
                UNRESOLVED.cursor_startWait;
            }
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.newTdo = this.plant.editTransferField(umath.kSetField, this.newTdo, this.fieldNumber, uparams.kFieldThreeDObject, uparams.kNotArray, this.regrow);
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
        } finally {
            if (this.regrow) {
                UNRESOLVED.cursor_stopWait;
            }
        }
    }
    
    public void undoCommand() {
        KfObject3D oldValue = new KfObject3D();
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = utdo.KfObject3D(this.values.Items[i]);
                oldValue = this.plant.editTransferField(umath.kSetField, oldValue, this.fieldNumber, uparams.kFieldThreeDObject, uparams.kNotArray, this.regrow);
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        result = super.description();
        result = "change " + result + " to \"" + this.newTdo.getName() + "\" in " + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdChangeSmallintValueCommand extends PdChangeValueCommand {
    public short newValue;
    public short arrayIndex;
    
    // ------------------------------------------------------------ PdChangeSmallintValueCommand 
    public void createCommandWithListOfPlants(TList aList, short aNewValue, short aFieldNumber, short anArrayIndex, boolean aRegrow) {
        short oldValue = 0;
        short i = 0;
        
        super.createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
        this.newValue = aNewValue;
        this.arrayIndex = anArrayIndex;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = this.plant.editTransferField(umath.kGetField, oldValue, this.fieldNumber, uparams.kFieldSmallint, this.arrayIndex, this.regrow);
                this.values.Add(PdSmallintValue().createWithSmallint(oldValue));
            }
        }
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            if (this.regrow) {
                UNRESOLVED.cursor_startWait;
            }
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.newValue = this.plant.editTransferField(umath.kSetField, this.newValue, this.fieldNumber, uparams.kFieldSmallint, this.arrayIndex, this.regrow);
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
        } finally {
            if (this.regrow) {
                UNRESOLVED.cursor_stopWait;
            }
        }
    }
    
    public void undoCommand() {
        short oldValue = 0;
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = PdSmallintValue(this.values.Items[i]).saveSmallint;
                oldValue = this.plant.editTransferField(umath.kSetField, oldValue, this.fieldNumber, uparams.kFieldSmallint, this.arrayIndex, this.regrow);
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        result = super.description();
        result = "change " + result + " to " + IntToStr(this.newValue) + " in " + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
class PdChangeBooleanValueCommand extends PdChangeValueCommand {
    public boolean newValue;
    public short arrayIndex;
    
    // ------------------------------------------------------------ PdChangeBooleanValueCommand 
    public void createCommandWithListOfPlants(TList aList, boolean aNewValue, short aFieldNumber, short anArrayIndex, boolean aRegrow) {
        boolean oldValue = false;
        short i = 0;
        
        super.createCommandWithListOfPlants(aList, aFieldNumber, aRegrow);
        this.newValue = aNewValue;
        this.arrayIndex = anArrayIndex;
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = this.plant.editTransferField(umath.kGetField, oldValue, this.fieldNumber, uparams.kFieldBoolean, this.arrayIndex, this.regrow);
                this.values.Add(PdBooleanValue().createWithBoolean(oldValue));
            }
        }
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        try {
            if (this.regrow) {
                UNRESOLVED.cursor_startWait;
            }
            this.invalidateCombinedPlantRects();
            if (this.plantList.Count > 0) {
                for (i = 0; i <= this.plantList.Count - 1; i++) {
                    this.plant = uplant.PdPlant(this.plantList.Items[i]);
                    this.newValue = this.plant.editTransferField(umath.kSetField, this.newValue, this.fieldNumber, uparams.kFieldBoolean, this.arrayIndex, this.regrow);
                    this.plant.recalculateBounds(umain.kDrawNow);
                }
            }
            this.invalidateCombinedPlantRects();
        } finally {
            if (this.regrow) {
                UNRESOLVED.cursor_stopWait;
            }
        }
    }
    
    public void undoCommand() {
        boolean oldValue = false;
        short i = 0;
        
        super.undoCommand();
        this.invalidateCombinedPlantRects();
        if (this.plantList.Count > 0) {
            for (i = 0; i <= this.plantList.Count - 1; i++) {
                this.plant = uplant.PdPlant(this.plantList.Items[i]);
                oldValue = PdBooleanValue(this.values.Items[i]).saveBoolean;
                oldValue = this.plant.editTransferField(umath.kSetField, oldValue, this.fieldNumber, uparams.kFieldBoolean, this.arrayIndex, this.regrow);
                this.plant.recalculateBounds(umain.kDrawNow);
            }
        }
        this.invalidateCombinedPlantRects();
    }
    
    public String description() {
        result = "";
        String newValueString = "";
        
        result = super.description();
        if (this.newValue) {
            newValueString = "yes";
        } else {
            newValueString = "no";
        }
        result = "change " + result + " to " + newValueString + " in " + plantNamesForDescription(this.plantList);
        return result;
    }
    
}
// ---------------------------------------------------------------------------- breeder commands 
class PdBreedFromParentsCommand extends PdCommand {
    public PdPlant firstParent;
    public PdPlant secondParent;
    public float fractionOfMaxAge;
    public short row;
    public TList oldGenerations;
    public PdGeneration newGeneration;
    public PdGeneration firstGeneration;
    public boolean createFirstGeneration;
    public short rowSelectedAtStart;
    
    // ---------------------------------------------------------------------------- PdBreedFromTwoParentsCommand 
    public void createWithInfo(TListCollection existingGenerations, PdPlant aFirstParent, PdPlant aSecondParent, short aRow, float aFractionOfMaxAge, boolean aCreateFirstGeneration) {
        short i = 0;
        
        super.create();
        this.commandChangesPlantFile = false;
        this.firstParent = aFirstParent;
        if (this.firstParent == null) {
            throw new GeneralException.create("Problem: Need at least one parent in method PdBreedFromParentsCommand.createWithInfo.");
        }
        this.secondParent = aSecondParent;
        this.fractionOfMaxAge = aFractionOfMaxAge;
        this.row = aRow;
        this.createFirstGeneration = aCreateFirstGeneration;
        if (this.row < 0) {
            //from main window 
            this.row = ubreedr.BreederForm.selectedRow;
        }
        this.oldGenerations = delphi_compatability.TList().Create();
        if (existingGenerations.Count > 0) {
            for (i = 0; i <= existingGenerations.Count - 1; i++) {
                this.oldGenerations.Add(ugener.PdGeneration(existingGenerations.Items[i]));
            }
        }
    }
    
    public void destroy() {
        PdGeneration lastGeneration = new PdGeneration();
        
        if (this.done) {
            while (this.oldGenerations.Count - 1 > this.row) {
                // free all generations below row 
                lastGeneration = ugener.PdGeneration(this.oldGenerations.Items[this.oldGenerations.Count - 1]);
                this.oldGenerations.Remove(lastGeneration);
                lastGeneration.free;
            }
            // free new generation (and first generation if created, if not it will be nil) 
        } else {
            this.firstGeneration.free;
            this.firstGeneration = null;
            this.newGeneration.free;
            this.newGeneration = null;
        }
        this.oldGenerations.free;
        this.oldGenerations = null;
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        short i = 0;
        PdGeneration generation = new PdGeneration();
        
        result = 0;
        if (this.done) {
            if (this.oldGenerations.Count > 0) {
                for (i = 0; i <= this.oldGenerations.Count - 1; i++) {
                    generation = ugener.PdGeneration(this.oldGenerations.Items[i]);
                    result = result + generation.plants.Count;
                }
            }
        } else {
            if (this.firstGeneration != null) {
                result = this.firstGeneration.plants.Count;
            }
            if (this.newGeneration != null) {
                result = this.newGeneration.plants.Count;
            }
        }
        return result;
    }
    
    public void doCommand() {
        PdGeneration generationBred = new PdGeneration();
        
        super.doCommand();
        try {
            UNRESOLVED.cursor_startWait;
            this.rowSelectedAtStart = ubreedr.BreederForm.selectedRow;
            if (this.createFirstGeneration) {
                // if command created from main window, create first generation to put in breeder 
                this.firstGeneration = ugener.PdGeneration().createWithParents(this.firstParent, this.secondParent, this.fractionOfMaxAge);
            }
            // create generation that is outcome of breeding and do breeding 
            this.newGeneration = ugener.PdGeneration().create();
            this.newGeneration.breedFromParents(this.firstParent, this.secondParent, this.fractionOfMaxAge);
            // tell breeder to forget about other generations below the selected row  
            ubreedr.BreederForm.forgetGenerationsListBelowRow(this.row);
            if (this.firstGeneration != null) {
                ubreedr.BreederForm.addGeneration(this.firstGeneration);
                ubreedr.BreederForm.selectGeneration(this.firstGeneration);
            }
            ubreedr.BreederForm.updateForChangeToGenerations();
            if (this.row <= this.oldGenerations.Count - 1) {
                // set the firstParent and secondParent pointers in the generation that was bred (either the firstGeneration
                //      or the generation selected in the breeder) 
                generationBred = ugener.PdGeneration(this.oldGenerations.Items[this.row]);
                generationBred.firstParent = generationBred.firstSelectedPlant();
                generationBred.secondParent = generationBred.secondSelectedPlant();
            }
            // add and select the new generation in the breeder 
            ubreedr.BreederForm.addGeneration(this.newGeneration);
            ubreedr.BreederForm.selectGeneration(this.newGeneration);
            ubreedr.BreederForm.updateForChangeToGenerations();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void undoCommand() {
        PdGeneration generationBred = new PdGeneration();
        
        super.undoCommand();
        // tell the breeder to forget about the generation(s) created by this command, and if there were any generations
        //    wiped out by it, tell the breeder to restore pointers to all generations that were forgotten 
        ubreedr.BreederForm.forgetLastGeneration();
        if (this.firstGeneration != null) {
            ubreedr.BreederForm.forgetLastGeneration();
        }
        ubreedr.BreederForm.updateForChangeToGenerations();
        ubreedr.BreederForm.addGenerationsFromListBelowRow(this.row, this.oldGenerations);
        ubreedr.BreederForm.selectedRow = this.rowSelectedAtStart;
        if (this.row <= this.oldGenerations.Count - 1) {
            // set parent pointers of generation that was bred (firstGeneration or generation selected) to nil 
            generationBred = ugener.PdGeneration(this.oldGenerations.Items[this.row]);
            generationBred.firstParent = null;
            generationBred.secondParent = null;
        }
        ubreedr.BreederForm.updateForChangeToGenerations();
    }
    
    public void redoCommand() {
        PdGeneration generationBred = new PdGeneration();
        
        super.doCommand();
        // tell breeder to forget about other generations below the selected row (the whole list if from the main window) 
        ubreedr.BreederForm.forgetGenerationsListBelowRow(this.row);
        if (this.firstGeneration != null) {
            ubreedr.BreederForm.addGeneration(this.firstGeneration);
            ubreedr.BreederForm.selectGeneration(this.firstGeneration);
        }
        ubreedr.BreederForm.updateForChangeToGenerations();
        if (this.row <= this.oldGenerations.Count - 1) {
            // set the firstParent and secondParent pointers in the generation that was bred (either the firstGeneration
            //    or the generation selected in the breeder) 
            generationBred = ugener.PdGeneration(this.oldGenerations.Items[this.row]);
            generationBred.firstParent = generationBred.firstSelectedPlant();
            generationBred.secondParent = generationBred.secondSelectedPlant();
        }
        // add and select the new generation in the breeder 
        ubreedr.BreederForm.addGeneration(this.newGeneration);
        ubreedr.BreederForm.selectGeneration(this.newGeneration);
        ubreedr.BreederForm.updateForChangeToGenerations();
    }
    
    public String description() {
        result = "";
        if (this.createFirstGeneration) {
            // plant(s) from main window
            result = "breed";
            if (this.firstParent != null) {
                result = result + " \"" + this.firstParent.getName() + "\"";
            }
            if (this.secondParent != null) {
                result = result + ", \"" + this.secondParent.getName() + "\"";
            }
        } else {
            result = "breed from breeder row " + IntToStr(this.row + 1);
        }
        return result;
    }
    
}
class PdReplaceBreederPlant extends PdCommand {
    public PdPlant originalPlant;
    public PdPlant newPlant;
    public PdPlant plantDraggedFrom;
    public short row;
    public short column;
    
    // ------------------------------------------------------------------- PdReplaceBreederPlant 
    public void createWithPlantRowAndColumn(PdPlant aPlant, short aRow, short aColumn) {
        super.create();
        this.commandChangesPlantFile = false;
        this.plantDraggedFrom = aPlant;
        if (this.plantDraggedFrom == null) {
            throw new GeneralException.create("Problem: Nil plant dragged from in method PdReplaceBreederPlant.createWithPlantRowAndColumn.");
        }
        this.row = aRow;
        this.column = aColumn;
    }
    
    public void destroy() {
        if (this.done) {
            this.originalPlant.free;
            this.originalPlant = null;
        } else {
            this.newPlant.free;
            this.newPlant = null;
        }
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        //has one plant in either case (done or undone)
        result = 1;
        return result;
    }
    
    public void doCommand() {
        super.doCommand();
        this.originalPlant = ubreedr.BreederForm.plantForRowAndColumn(this.row, this.column);
        if (this.originalPlant == null) {
            throw new GeneralException.create("Problem: Invalid row and column in method PdReplaceBreederPlant.doCommand.");
        }
        this.newPlant = uplant.PdPlant().create();
        this.plantDraggedFrom.copyTo(this.newPlant);
        ubreedr.BreederForm.replacePlantInRow(this.originalPlant, this.newPlant, this.row);
    }
    
    public void undoCommand() {
        super.undoCommand();
        ubreedr.BreederForm.replacePlantInRow(this.newPlant, this.originalPlant, this.row);
    }
    
    public void redoCommand() {
        super.doCommand();
        ubreedr.BreederForm.replacePlantInRow(this.originalPlant, this.newPlant, this.row);
    }
    
    public String description() {
        result = "";
        result = "replace breeder plant in row " + IntToStr(this.row + 1) + ", column " + IntToStr(this.column);
        return result;
    }
    
}
class PdMakeTimeSeriesCommand extends PdCommand {
    public TList oldPlants;
    public TList newPlants;
    public PdPlant newPlant;
    public boolean isPaste;
    
    // ------------------------------------------------------------------- PdMakeTimeSeriesCommand 
    public void createWithNewPlant(PdPlant aNewPlant) {
        super.create();
        this.commandChangesPlantFile = false;
        this.newPlant = aNewPlant;
        if (this.newPlant == null) {
            throw new GeneralException.create("Problem: Nil plant in method PdMakeTimeSeriesCommand.createWithNewPlant.");
        }
        this.oldPlants = delphi_compatability.TList().Create();
        this.newPlants = delphi_compatability.TList().Create();
    }
    
    public void destroy() {
        short i = 0;
        
        if (this.done) {
            if ((this.oldPlants != null) && (this.oldPlants.Count > 0)) {
                for (i = 0; i <= this.oldPlants.Count - 1; i++) {
                    uplant.PdPlant(this.oldPlants.Items[i]).free;
                }
            }
        } else {
            if ((this.newPlants != null) && (this.newPlants.Count > 0)) {
                for (i = 0; i <= this.newPlants.Count - 1; i++) {
                    uplant.PdPlant(this.newPlants.Items[i]).free;
                }
            }
        }
        this.oldPlants.free;
        this.oldPlants = null;
        this.newPlants.free;
        this.newPlants = null;
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        result = 0;
        if (this.done) {
            if (this.oldPlants != null) {
                result = this.oldPlants.Count;
            }
        } else {
            if (this.newPlants != null) {
                result = this.newPlants.Count;
            }
        }
        return result;
    }
    
    public void doCommand() {
        short i = 0;
        
        super.doCommand();
        if (UNRESOLVED.TimeSeriesForm.plants.count > 0) {
            for (i = 0; i <= UNRESOLVED.TimeSeriesForm.plants.count - 1; i++) {
                this.oldPlants.Add(UNRESOLVED.TimeSeriesForm.plants.items[i]);
            }
        }
        UNRESOLVED.TimeSeriesForm.plants.clearPointersWithoutDeletingObjects;
        //redraws in updateForChangeToPlants
        UNRESOLVED.TimeSeriesForm.initializeWithPlant(this.newPlant, umain.kDontDrawYet);
        if (UNRESOLVED.TimeSeriesForm.plants.count > 0) {
            for (i = 0; i <= UNRESOLVED.TimeSeriesForm.plants.count - 1; i++) {
                this.newPlants.Add(UNRESOLVED.TimeSeriesForm.plants.items[i]);
            }
        }
        UNRESOLVED.TimeSeriesForm.updateForChangeToPlants(UNRESOLVED.kRecalculateScale);
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        UNRESOLVED.TimeSeriesForm.plants.clearPointersWithoutDeletingObjects;
        if (this.oldPlants.Count > 0) {
            for (i = 0; i <= this.oldPlants.Count - 1; i++) {
                UNRESOLVED.TimeSeriesForm.plants.add(this.oldPlants.Items[i]);
            }
        }
        UNRESOLVED.TimeSeriesForm.updateForChangeToPlants(UNRESOLVED.kDontRecalculateScale);
    }
    
    public void redoCommand() {
        short i = 0;
        
        super.doCommand();
        UNRESOLVED.TimeSeriesForm.plants.clearPointersWithoutDeletingObjects;
        if (this.newPlants.Count > 0) {
            for (i = 0; i <= this.newPlants.Count - 1; i++) {
                UNRESOLVED.TimeSeriesForm.plants.add(this.newPlants.Items[i]);
            }
        }
        UNRESOLVED.TimeSeriesForm.updateForChangeToPlants(UNRESOLVED.kDontRecalculateScale);
    }
    
    public String description() {
        result = "";
        if (this.isPaste) {
            result = "paste into time series window";
        } else {
            result = "make time series";
            if (this.newPlant != null) {
                result = result + " for plant \"" + this.newPlant.getName() + "\"";
            }
        }
        return result;
    }
    
}
class PdChangeBreedingAndTimeSeriesOptionsCommand extends PdCommand {
    public BreedingAndTimeSeriesOptionsStructure oldOptions;
    public BreedingAndTimeSeriesOptionsStructure newOptions;
    public DomainOptionsStructure oldDomainOptions;
    public DomainOptionsStructure newDomainOptions;
    
    // -------------------------------------------------------------- PdChangeBreederOptionsCommand 
    public void createWithOptionsAndDomainOptions(BreedingAndTimeSeriesOptionsStructure anOptions, DomainOptionsStructure aDomainOptions) {
        super.create();
        this.commandChangesPlantFile = false;
        this.newOptions = anOptions;
        this.oldOptions = udomain.domain.breedingAndTimeSeriesOptions;
        this.newDomainOptions = aDomainOptions;
        this.oldDomainOptions = udomain.domain.options;
    }
    
    public void doCommand() {
        super.doCommand();
        udomain.domain.breedingAndTimeSeriesOptions = this.newOptions;
        udomain.domain.options = this.newDomainOptions;
        ubreedr.BreederForm.updateForChangeToDomainOptions();
        UNRESOLVED.TimeSeriesForm.updateForChangeToDomainOptions;
    }
    
    public void undoCommand() {
        super.undoCommand();
        udomain.domain.breedingAndTimeSeriesOptions = this.oldOptions;
        udomain.domain.options = this.oldDomainOptions;
        ubreedr.BreederForm.updateForChangeToDomainOptions();
        UNRESOLVED.TimeSeriesForm.updateForChangeToDomainOptions;
    }
    
    // redo is same as do 
    public String description() {
        result = "";
        result = "change breeding and time series options";
        return result;
    }
    
}
class PdDeleteBreederGenerationCommand extends PdCommand {
    public PdGeneration generation;
    public short row;
    
    // ------------------------------------------------------------------------ PdDeleteBreederGenerationCommand 
    public void createWithGeneration(PdGeneration aGeneration) {
        super.create();
        this.commandChangesPlantFile = false;
        this.generation = aGeneration;
        if (this.generation == null) {
            throw new GeneralException.create("Problem: Nil generation in method PdDeleteBreederGenerationCommand.createWithGeneration.");
        }
        this.row = ubreedr.BreederForm.generations.IndexOf(this.generation);
        if (this.row < 0) {
            throw new GeneralException.create("Problem: Generation not in list in method PdDeleteBreederGenerationCommand.createWithGeneration.");
        }
    }
    
    public void destroy() {
        if (this.done) {
            this.generation.free;
            this.generation = null;
        }
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        result = 0;
        if ((this.done) && (this.generation != null)) {
            result = this.generation.plants.Count;
        }
        return result;
    }
    
    public void doCommand() {
        short index = 0;
        
        super.doCommand();
        index = ubreedr.BreederForm.generations.IndexOf(this.generation);
        ubreedr.BreederForm.generations.Remove(this.generation);
        if (index > 0) {
            ubreedr.BreederForm.selectedRow = index - 1;
        }
        ubreedr.BreederForm.updateForChangeToGenerations();
    }
    
    public void undoCommand() {
        super.undoCommand();
        ubreedr.BreederForm.generations.Insert(this.row, this.generation);
        ubreedr.BreederForm.selectedRow = ubreedr.BreederForm.generations.IndexOf(this.generation);
        ubreedr.BreederForm.updateForChangeToGenerations();
    }
    
    public String description() {
        result = "";
        result = "delete breeder generation";
        return result;
    }
    
}
class PdDeleteAllBreederGenerationsCommand extends PdCommand {
    public TListCollection generations;
    
    // ------------------------------------------------------------------- PdDeleteAllBreederGenerationsCommand 
    public void create() {
        short i = 0;
        
        this.generations = ucollect.TListCollection().Create();
        if (ubreedr.BreederForm.generations.Count > 0) {
            for (i = 0; i <= ubreedr.BreederForm.generations.Count - 1; i++) {
                this.generations.Add(ubreedr.BreederForm.generations.Items[i]);
            }
        }
    }
    
    public void destroy() {
        if (!this.done) {
            this.generations.clearPointersWithoutDeletingObjects();
        }
        this.generations.free;
        this.generations = null;
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        short i = 0;
        PdGeneration generation = new PdGeneration();
        
        result = 0;
        if (this.done) {
            if (this.generations.Count > 0) {
                for (i = 0; i <= this.generations.Count - 1; i++) {
                    generation = ugener.PdGeneration(this.generations.Items[i]);
                    result = result + generation.plants.Count;
                }
            }
        }
        return result;
    }
    
    public void doCommand() {
        super.doCommand();
        ubreedr.BreederForm.generations.clearPointersWithoutDeletingObjects();
        ubreedr.BreederForm.updateForChangeToGenerations();
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.generations.Count > 0) {
            for (i = 0; i <= this.generations.Count - 1; i++) {
                ubreedr.BreederForm.generations.Add(this.generations.Items[i]);
            }
        }
        ubreedr.BreederForm.updateForChangeToGenerations();
    }
    
    //redo same as do
    public String description() {
        result = "";
        result = "delete all breeder generations";
        return result;
    }
    
}
// ------------------------------------------------------------------------ time series 
class PdChangeNumberOfTimeSeriesStagesCommand extends PdCommand {
    public short newNumber;
    public short oldNumber;
    
    // -------------------------------------------------------- PdChangeNumberOfTimeSeriesStagesCommand 
    public void createWithNewNumberOfStages(short aNumber) {
        super.create();
        this.commandChangesPlantFile = false;
        this.newNumber = aNumber;
        this.oldNumber = udomain.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages;
    }
    
    public void doCommand() {
        super.doCommand();
        udomain.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages = this.newNumber;
        UNRESOLVED.TimeSeriesForm.updateForChangeToDomainOptions;
    }
    
    public void undoCommand() {
        super.undoCommand();
        udomain.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages = this.oldNumber;
        UNRESOLVED.TimeSeriesForm.updateForChangeToDomainOptions;
    }
    
    public String description() {
        result = "";
        result = "change number of time series stages";
        return result;
    }
    
}
class PdDeleteTimeSeriesCommand extends PdCommand {
    public TListCollection plants;
    
    // -------------------------------------------------------- PdDeleteTimeSeriesCommand 
    public void create() {
        short i = 0;
        
        this.plants = ucollect.TListCollection().Create();
        if (UNRESOLVED.TimeSeriesForm.plants.count > 0) {
            for (i = 0; i <= UNRESOLVED.TimeSeriesForm.plants.count - 1; i++) {
                this.plants.Add(UNRESOLVED.TimeSeriesForm.plants.items[i]);
            }
        }
    }
    
    public void destroy() {
        if (!this.done) {
            this.plants.clearPointersWithoutDeletingObjects();
        }
        this.plants.free;
        this.plants = null;
        super.destroy();
    }
    
    public long numberOfStoredLargeObjects() {
        result = 0;
        if (this.done) {
            result = this.plants.Count;
        } else {
            result = 0;
        }
        return result;
    }
    
    public void doCommand() {
        super.doCommand();
        UNRESOLVED.TimeSeriesForm.plants.clearPointersWithoutDeletingObjects;
        UNRESOLVED.TimeSeriesForm.updateForChangeToPlants(UNRESOLVED.kDontRecalculateScale);
    }
    
    public void undoCommand() {
        short i = 0;
        
        super.undoCommand();
        if (this.plants.Count > 0) {
            for (i = 0; i <= this.plants.Count - 1; i++) {
                UNRESOLVED.TimeSeriesForm.plants.add(this.plants.Items[i]);
            }
        }
        UNRESOLVED.TimeSeriesForm.updateForChangeToPlants(UNRESOLVED.kDontRecalculateScale);
    }
    
    //redo same as do
    public String description() {
        result = "";
        result = "delete time series";
        return result;
    }
    
}
