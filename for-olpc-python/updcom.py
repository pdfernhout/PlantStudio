# unit updcom

from conversion_common import *
import delphi_compatability
import ucommand
from ucommand import PdCommand
import ubreedr
import ucollect
import ugener

"""
import utimeser
import umath
import ucursor
import umain
import uplantmn
import uamendmt
import u3dexport
import uturtle
import udomain
import ubrstrat
import utdo
import uplant
import uparams
import usupport
"""

# const
kRotateNotInitialized = 0
kRotateX = 1
kRotateY = 2
kRotateZ = 3
kCopyToClipboard = True
kDontCopyToClipboard = False
kNewPlantAge = 5
kNewPlantPosition = 100
kHide = True
kShow = False
kSendBackward = True
kBringForward = False
kPasteMoveDistance = 40
kCreateFirstGeneration = True
kDontCreateFirstGeneration = False
kAddAtEnd = -1
kUp = 0
kDown = 1
kLeft = 2
kRight = 3
kChangeWidth = True
kChangeHeight = False

# var
numPlantsCreatedThisSession = 0L

# ------------------------------------------------------------------------ local functions 
def plantNamesForDescription(aList):
    result = ""
    firstPlant = PdPlant()
    
    result = ""
    if (aList == None) or (aList.Count <= 0):
        return result
    firstPlant = aList[0]
    if firstPlant != None:
        result = " plant \"" + firstPlant.getName() + "\""
        if aList.Count > 1:
            result = result + ", others"
    return result

# const
kGapBetweenArrangedPlants = 5

def nameForDirection(direction):
    result = ""
    result = ""
    if direction == kRotateX:
        result = "X"
    elif direction == kRotateY:
        result = "Y"
    elif direction == kRotateZ:
        result = "Z"
    return result

# value classes to save information about each plant in list 
class PdBooleanValue:
    def __init__(self):
        self.saveBoolean = False
    
    # ------------------------------------------------------------------------ value objects 
    def createWithBoolean(self, aBoolean):
        self.saveBoolean = aBoolean
        return self
    
class PdPointValue:
    def __init__(self):
        self.savePoint = TPoint()
    
    def createWithPoint(self, aPoint):
        self.savePoint = aPoint
        return self
    
class PdSingleValue:
    def __init__(self):
        self.saveSingle = 0.0
    
    def createWithSingle(self, aSingle):
        self.saveSingle = aSingle
        return self
    
class PdSinglePointValue:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
    
    def createWithSingleXY(self, anX, aY):
        self.x = anX
        self.y = aY
        return self
    
class PdXYZValue:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    
    def createWithXYZ(self, anX, aY, aZ):
        self.x = anX
        self.y = aY
        self.z = aZ
        return self
    
class PdSmallintValue:
    def __init__(self):
        self.saveSmallint = 0
    
    def createWithSmallint(self, aSmallint):
        self.saveSmallint = aSmallint
        return self

class PdLongintValue:
    def __init__(self):
        self.saveLongint = 0L
    
    def createWithLongint(self, aLongint):
        self.saveLongint = aLongint
        return self
    
class PdColorValue:
    def __init__(self):
        self.saveColor = TColorRef()
    
    def createWithColor(self, aColor):
        self.saveColor = aColor
        return self
    
# -------------------------------------- commands that affect only the drawing area (and domain options) 
class PdScrollCommand(PdCommand):
    def __init__(self):
        self.dragStartPoint = TPoint()
        self.oldOffset_mm = SinglePoint()
        self.newOffSet_mm = SinglePoint()
    
    # ------------------------------------------------------------ PdScrollCommand 
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        result = self
        if aTrackPhase == ucommand.TrackPhase.trackPress:
            self.dragStartPoint = nextPoint
            self.oldOffset_mm = udomain.domain.plantDrawOffset_mm()
        elif aTrackPhase == ucommand.TrackPhase.trackMove:
            if mouseDidMove:
                self.newOffSet_mm.x = self.oldOffset_mm.x + (nextPoint.X - self.dragStartPoint.X) / udomain.domain.plantDrawScale_PixelsPerMm()
                self.newOffSet_mm.y = self.oldOffset_mm.y + (nextPoint.Y - self.dragStartPoint.Y) / udomain.domain.plantDrawScale_PixelsPerMm()
                udomain.domain.plantManager.plantDrawOffset_mm = self.newOffSet_mm
                umain.MainForm.recalculateAllPlantBoundsRectsForOffsetChange()
                umain.MainForm.invalidateEntireDrawing()
        elif aTrackPhase == ucommand.TrackPhase.trackRelease:
            pass
        return result
    
    # PdDragCommand.doCommand should do nothing
    def redoCommand(self):
        #not redo
        PdCommand.doCommand(self)
        udomain.domain.plantManager.plantDrawOffset_mm = self.newOffSet_mm
        umain.MainForm.recalculateAllPlantBoundsRectsForOffsetChange()
        umain.MainForm.invalidateEntireDrawing()
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        udomain.domain.plantManager.plantDrawOffset_mm = self.oldOffset_mm
        umain.MainForm.recalculateAllPlantBoundsRectsForOffsetChange()
        umain.MainForm.invalidateEntireDrawing()
    
    def description(self):
        result = ""
        result = "scroll in main window"
        return result
    
class PdChangeMagnificationCommand(PdCommand):
    def __init__(self):
        self.startDragPoint = TPoint()
        self.oldScale_PixelsPerMm = 0.0
        self.newScale_pixelsPerMm = 0.0
        self.oldOffset_mm = SinglePoint()
        self.newOffset_mm = SinglePoint()
        self.clickPoint = SinglePoint()
        self.shift = False
    
    # -------------------------------------------------------- PdChangeMagnificationCommand 
    def createWithNewScaleAndPoint(self, aNewScale, aPoint):
        PdCommand.create(self)
        self.newScale_pixelsPerMm = aNewScale
        self.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
        self.oldOffset_mm = udomain.domain.plantDrawOffset_mm()
        self.clickPoint.x = aPoint.X
        self.clickPoint.y = aPoint.Y
        return self
    
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        size = TPoint()
        newScaleX = 0.0
        newScaleY = 0.0
        
        result = self
        if aTrackPhase == ucommand.TrackPhase.trackPress:
            self.startDragPoint = nextPoint
        elif aTrackPhase == ucommand.TrackPhase.trackMove:
            pass
        elif aTrackPhase == ucommand.TrackPhase.trackRelease:
            size = Point(abs(nextPoint.X - self.startDragPoint.X), abs(self.startDragPoint.Y - nextPoint.Y))
            if (size.X > 10) and (size.Y > 10):
                # have min size in case they move the mouse by mistake
                self.clickPoint.x = umath.min(nextPoint.X, self.startDragPoint.X) + abs(nextPoint.X - self.startDragPoint.X) / 2
                self.clickPoint.y = umath.min(nextPoint.Y, self.startDragPoint.Y) + abs(nextPoint.Y - self.startDragPoint.Y) / 2
                newScaleX = umath.safedivExcept(udomain.domain.plantDrawScale_PixelsPerMm() * umain.MainForm.drawingPaintBox.Width, size.X, 1.0)
                newScaleY = umath.safedivExcept(udomain.domain.plantDrawScale_PixelsPerMm() * umain.MainForm.drawingPaintBox.Height, size.Y, 1.0)
                self.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
                self.oldOffset_mm = udomain.domain.plantDrawOffset_mm()
                self.newScale_pixelsPerMm = umath.min(newScaleX, newScaleY)
            else:
                self.clickPoint.x = nextPoint.X
                self.clickPoint.y = nextPoint.Y
                self.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
                self.oldOffset_mm = udomain.domain.plantDrawOffset_mm()
                if self.shift:
                    self.newScale_pixelsPerMm = self.oldScale_PixelsPerMm * 0.75
                else:
                    self.newScale_pixelsPerMm = self.oldScale_PixelsPerMm * 1.5
        return result
    
    def doCommand(self):
        clickTPoint = TPoint()
        
        PdCommand.doCommand(self)
        if self.newScale_pixelsPerMm != 0.0:
            clickTPoint.X = intround(self.clickPoint.x)
            clickTPoint.Y = intround(self.clickPoint.y)
            umain.MainForm.magnifyOrReduce(self.newScale_pixelsPerMm, clickTPoint, umain.kDrawNow)
        self.newOffset_mm = udomain.domain.plantDrawOffset_mm()
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        udomain.domain.plantManager.plantDrawOffset_mm = self.oldOffset_mm
        if self.oldScale_PixelsPerMm != 0.0:
            umain.MainForm.magnifyOrReduce(self.oldScale_PixelsPerMm, Point(0, 0), umain.kDrawNow)
    
    def description(self):
        result = ""
        if self.newScale_pixelsPerMm > self.oldScale_PixelsPerMm:
            result = "enlarge in main window"
        else:
            result = "reduce in main window"
        return result
    
class PdCenterDrawingCommand(PdCommand):
    def __init__(self):
        self.oldScale_PixelsPerMm = 0.0
        self.newScale_pixelsPerMm = 0.0
        self.oldOffset_mm = SinglePoint()
        self.newOffset_mm = SinglePoint()
    
    # -------------------------------------------------------- PdCenterDrawingCommand 
    def doCommand(self):
        PdCommand.doCommand(self)
        self.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
        self.oldOffset_mm = udomain.domain.plantDrawOffset_mm()
        umain.MainForm.fitVisiblePlantsInDrawingArea(umain.kDrawNow, umain.kScaleAndMove, umain.kAlwaysMove)
        umain.MainForm.recalculateAllPlantBoundsRects(uplant.kDontDrawNow)
        self.newScale_pixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
        self.newOffset_mm = udomain.domain.plantDrawOffset_mm()
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        udomain.domain.plantManager.plantDrawOffset_mm = self.oldOffset_mm
        umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow)
        if self.oldScale_PixelsPerMm != 0.0:
            umain.MainForm.magnifyOrReduce(self.oldScale_PixelsPerMm, Point(0, 0), umain.kDrawNow)
    
    def redoCommand(self):
        PdCommand.doCommand(self)
        udomain.domain.plantManager.plantDrawOffset_mm = self.newOffset_mm
        umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow)
        if self.newScale_pixelsPerMm != 0.0:
            umain.MainForm.magnifyOrReduce(self.newScale_pixelsPerMm, Point(0, 0), umain.kDrawNow)
    
    def description(self):
        result = ""
        result = "scale to fit in main window"
        return result
    
class PdChangeMainWindowOrientationCommand(PdCommand):
    def __init__(self):
        self.oldScale_PixelsPerMm = 0.0
        self.newScale_pixelsPerMm = 0.0
        self.oldOffset_mm = SinglePoint()
        self.newOffset_mm = SinglePoint()
        self.oldWindowOrientation = 0
        self.newWindowOrientation = 0
    
    # ------------------------------------------------------------ PdChangeMainWindowOrientationCommand 
    def createWithNewOrientation(self, aNewOrientation):
        PdCommand.create(self)
        #hidden flag not saved
        self.commandChangesPlantFile = False
        self.newWindowOrientation = aNewOrientation
        self.oldWindowOrientation = udomain.domain.options.mainWindowOrientation
        return self
    
    def doCommand(self):
        PdCommand.doCommand(self)
        try:
            ucursor.cursor_startWait()
            udomain.domain.options.mainWindowOrientation = self.newWindowOrientation
            umain.MainForm.updateForChangeToOrientation()
        finally:
            ucursor.cursor_stopWait()
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        try:
            ucursor.cursor_startWait()
            udomain.domain.options.mainWindowOrientation = self.oldWindowOrientation
            umain.MainForm.updateForChangeToOrientation()
        finally:
            ucursor.cursor_stopWait()
    
    def description(self):
        result = ""
        result = "change top/side orientation in main window"
        return result
    
# ------------------------------------------------------------------ commands that affect only the domain 
class PdChangeDomainOptionsCommand(PdCommand):
    def __init__(self):
        self.oldOptions = DomainOptionsStructure()
        self.newOptions = DomainOptionsStructure()
    
    # -------------------------------------------------------- PdChangeDomainOptionsCommand 
    def createWithOptions(self, aNewOptions):
        PdCommand.create(self)
        self.commandChangesPlantFile = False
        self.newOptions = aNewOptions
        self.oldOptions = udomain.domain.options
        return self
    
    def doCommand(self):
        PdCommand.doCommand(self)
        udomain.domain.options = self.newOptions
        umain.MainForm.updateForChangeToDomainOptions()
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        udomain.domain.options = self.oldOptions
        umain.MainForm.updateForChangeToDomainOptions()
    
    def description(self):
        result = ""
        result = "change preferences"
        return result
    
class PdChangeDomain3DOptionsCommand(PdCommand):
    def __init__(self):
        self.outputType = 0
        self.oldOptions = FileExport3DOptionsStructure()
        self.newOptions = FileExport3DOptionsStructure()
    
    # -------------------------------------------------------- PdChangeDomain3DOptionsCommand 
    def createWithOptionsAndType(self, aNewOptions, anOutputType):
        PdCommand.create(self)
        self.outputType = anOutputType
        self.commandChangesPlantFile = False
        self.newOptions = aNewOptions
        self.oldOptions = udomain.domain.exportOptionsFor3D[self.outputType]
        return self
    
    def doCommand(self):
        PdCommand.doCommand(self)
        udomain.domain.exportOptionsFor3D[self.outputType] = self.newOptions
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        udomain.domain.exportOptionsFor3D[self.outputType] = self.oldOptions
    
    def description(self):
        result = ""
        result = "change " + usupport.nameStringForFileType(u3dexport.fileTypeFor3DExportType(self.outputType)) + " output options"
        return result
    
# ------------------------------------------------------------------- commands that affect one plant only 
class PdRenameCommand(PdCommand):
    def __init__(self):
        self.plant = PdPlant()
        self.oldName = ""
        self.newName = ""
    
    # ------------------------------------------------------------ PdRenameCommand 
    def createWithPlantAndNewName(self, aPlant, aNewName):
        PdCommand.create(self)
        self.plant = aPlant
        self.oldName = self.plant.getName()
        self.newName = aNewName
        return self
    
    def doCommand(self):
        PdCommand.doCommand(self)
        self.plant.setName(self.newName)
        umain.MainForm.updateForRenamingPlant(self.plant)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        self.plant.setName(self.oldName)
        umain.MainForm.updateForRenamingPlant(self.plant)
    
    def description(self):
        result = ""
        result = "rename \"" + self.oldName + "\" to \"" + self.newName + "\""
        return result
    
class PdEditNoteCommand(PdCommand):
    def __init__(self):
        self.plant = PdPlant()
        self.oldStrings = TStringList()
        self.newStrings = TStringList()
    
    # ------------------------------------------------------------ PdEditNoteCommand 
    def createWithPlantAndNewTStrings(self, aPlant, aNewStrings):
        PdCommand.create(self)
        self.plant = aPlant
        self.oldStrings = self.plant.noteLines
        # we take ownership of this list and delete it if undone
        self.newStrings = aNewStrings
        return self
    
    def destroy(self):
        if self.done:
            self.oldStrings.free
            self.oldStrings = None
        else:
            self.newStrings.free
            self.newStrings = None
    
    def doCommand(self):
        PdCommand.doCommand(self)
        self.plant.noteLines = self.newStrings
        umain.MainForm.updateForChangeToPlantNote(self.plant)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        self.plant.noteLines = self.oldStrings
        umain.MainForm.updateForChangeToPlantNote(self.plant)
    
    def description(self):
        result = ""
        result = "change note for \"" + self.plant.getName() + "\""
        return result
    
class PdNewCommand(PdCommand):
    def __init__(self):
        self.newPlant = PdPlant()
        self.useWizardPlant = False
        self.wizardPlant = PdPlant()
        self.oldSelectedList = TList()
    
    # v2.0
    # --------------------------------------------------------------------------------------------- PdNewCommand 
    def createWithWizardPlantAndOldSelectedList(self, aPlant, anOldSelectedList):
        i = 0
        
        PdCommand.create(self)
        self.useWizardPlant = True
        self.wizardPlant = aPlant
        # selected list is just pointers, this doesn't take control of them
        self.oldSelectedList = delphi_compatability.TList().Create()
        if (anOldSelectedList != None) and (anOldSelectedList.Count > 0):
            for i in range(0, anOldSelectedList.Count):
                self.oldSelectedList.Add(anOldSelectedList.Items[i])
        return self
    
    def destroy(self):
        self.oldSelectedList.free
        self.oldSelectedList = None
        if (not self.done) and (self.newPlant != None):
            # free created plant if change was undone 
            self.newPlant.free
            self.newPlant = None
        if (self.useWizardPlant) and (self.wizardPlant != None):
            self.wizardPlant.free
            self.wizardPlant = None
        PdCommand.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        result = 0
        if (not self.done) and (self.newPlant != None):
            result += 1
        if (self.useWizardPlant) and (self.wizardPlant != None):
            result += 1
        return result
    
    def doCommand(self):
        PdCommand.doCommand(self)
        self.newPlant = None
        try:
            ucursor.cursor_startWait()
            if (self.useWizardPlant) and (self.wizardPlant != None):
                self.newPlant = self.wizardPlant.makeCopy()
            else:
                self.newPlant = uplant.PdPlant()
                self.newPlant.defaultAllParameters()
                self.newPlant.setName("New plant " + IntToStr(numPlantsCreatedThisSession + 1))
                numPlantsCreatedThisSession += 1
            self.newPlant.randomize()
            self.newPlant.moveTo(umain.MainForm.standardPastePosition())
            self.newPlant.calculateDrawingScaleToLookTheSameWithDomainScale()
            self.newPlant.recalculateBounds(umain.kDrawNow)
            # put new plant at end of plant manager list 
            udomain.domain.plantManager.plants.Add(self.newPlant)
            # make new plant the only selected plant 
            umain.MainForm.deselectAllPlants()
            umain.MainForm.addSelectedPlant(self.newPlant, kAddAtEnd)
            umain.MainForm.updateForChangeToPlantList()
        finally:
            ucursor.cursor_stopWait()
    
    def undoCommand(self):
        i = 0
        
        PdCommand.undoCommand(self)
        udomain.domain.plantManager.plants.Remove(self.newPlant)
        umain.MainForm.removeSelectedPlant(self.newPlant)
        if self.oldSelectedList.Count > 0:
            for i in range(0, self.oldSelectedList.Count):
                # put back selections from before new plant was added
                umain.MainForm.selectedPlants.Add(self.oldSelectedList.Items[i])
        umain.MainForm.updateForChangeToPlantList()
    
    def redoCommand(self):
        PdCommand.doCommand(self)
        umain.MainForm.deselectAllPlants()
        udomain.domain.plantManager.plants.Add(self.newPlant)
        umain.MainForm.addSelectedPlant(self.newPlant, kAddAtEnd)
        umain.MainForm.updateForChangeToPlantList()
    
    def description(self):
        result = ""
        result = "create new plant"
        return result
    
class PdSendBackwardOrForwardCommand(PdCommand):
    def __init__(self):
        self.backward = False
    
    # ----------------------------------------------------------- PdSendBackwardOrForwardCommand 
    def createWithBackwardOrForward(self, aBackward):
        PdCommand.create(self)
        self.backward = aBackward
        return self
    
    def doCommand(self):
        if self.backward:
            # assumption here is that selected plants list doesn't change between this command and undo 
            umain.MainForm.moveSelectedPlantsDown()
        else:
            umain.MainForm.moveSelectedPlantsUp()
    
    def undoCommand(self):
        if self.backward:
            umain.MainForm.moveSelectedPlantsUp()
        else:
            umain.MainForm.moveSelectedPlantsDown()
    
    def description(self):
        result = ""
        if self.backward:
            result = "send backward in main window"
        else:
            result = "bring forward in main window"
        return result
    
class PdCreateAmendmentCommand(PdCommand):
    def __init__(self):
        self.plant = PdPlant()
        self.newAmendment = PdPlantDrawingAmendment()
    
    # ------------------------------------------------------------ PdCreateAmendmentCommand 
    def createWithPlantAndAmendment(self, aPlant, aNewAmendment):
        PdCommand.create(self)
        self.plant = aPlant
        if aNewAmendment == None:
            raise GeneralException.create("Problem: Nil new amendment; in PdCreateAmendmentCommand.createWithPlantAndAmendment.")
        # we take ownership of this and delete it if undone
        self.newAmendment = aNewAmendment
        return self
    
    def destroy(self):
        if not self.done:
            self.newAmendment.free
            self.newAmendment = None
    
    def doCommand(self):
        PdCommand.doCommand(self)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        self.plant.addAmendment(self.newAmendment)
        self.plant.recalculateBounds(umain.kDrawNow)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        umain.MainForm.addAmendedPartToList(self.newAmendment.partID, self.newAmendment.typeOfPart)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        self.plant.removeAmendment(self.newAmendment)
        self.plant.recalculateBounds(umain.kDrawNow)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        umain.MainForm.removeAmendedPartFromList(self.newAmendment.partID, self.newAmendment.typeOfPart)
    
    def description(self):
        result = ""
        result = "pose part " + IntToStr(self.newAmendment.partID) + " in plant \"" + self.plant.getName() + "\""
        return result
    
class PdDeleteAmendmentCommand(PdCommand):
    def __init__(self):
        self.plant = PdPlant()
        self.amendment = PdPlantDrawingAmendment()
    
    # ------------------------------------------------------------ PdDeleteAmendmentCommand 
    def createWithPlantAndAmendment(self, aPlant, anAmendment):
        PdCommand.create(self)
        self.plant = aPlant
        if anAmendment == None:
            raise GeneralException.create("Problem: Nil amendment; in PdDeleteAmendmentCommand.createWithPlantAndAmendment.")
        # we take ownership of this and delete it if done
        self.amendment = anAmendment
        return self
    
    def destroy(self):
        if self.done:
            self.amendment.free
            self.amendment = None
    
    def doCommand(self):
        PdCommand.doCommand(self)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        self.plant.removeAmendment(self.amendment)
        self.plant.recalculateBounds(umain.kDrawNow)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        umain.MainForm.removeAmendedPartFromList(self.amendment.partID, self.amendment.typeOfPart)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        self.plant.addAmendment(self.amendment)
        self.plant.recalculateBounds(umain.kDrawNow)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        umain.MainForm.addAmendedPartToList(self.amendment.partID, self.amendment.typeOfPart)
    
    def description(self):
        result = ""
        result = "unpose part " + IntToStr(self.amendment.partID) + " in plant \"" + self.plant.getName() + "\""
        return result
    
class PdEditAmendmentCommand(PdCommand):
    def __init__(self):
        self.plant = PdPlant()
        self.field = ""
        self.oldAmendment = PdPlantDrawingAmendment()
        self.newAmendment = PdPlantDrawingAmendment()
    
    # ------------------------------------------------------------ PdEditAmendmentCommand 
    def createWithPlantAndAmendmentAndField(self, aPlant, aNewAmendment, aField):
        PdCommand.create(self)
        self.plant = aPlant
        self.field = aField
        if aNewAmendment == None:
            raise GeneralException.create("nil new amendment")
        # we take ownership of this and delete it if undone
        self.newAmendment = aNewAmendment
        self.oldAmendment = self.plant.amendmentForPartID(self.newAmendment.partID)
        return self
    
    def destroy(self):
        if self.done:
            self.oldAmendment.free
            self.oldAmendment = None
        else:
            self.newAmendment.free
            self.newAmendment = None
    
    def doCommand(self):
        index = 0
        oldItemIndex = 0
        
        PdCommand.doCommand(self)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        if self.oldAmendment != None:
            self.plant.removeAmendment(self.oldAmendment)
        self.plant.addAmendment(self.newAmendment)
        self.plant.recalculateBounds(umain.kDrawNow)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        umain.MainForm.updatePoseInfo()
    
    def undoCommand(self):
        oldString = ""
        index = 0
        oldItemIndex = 0
        
        PdCommand.undoCommand(self)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        self.plant.removeAmendment(self.newAmendment)
        if self.oldAmendment != None:
            self.plant.addAmendment(self.oldAmendment)
        self.plant.recalculateBounds(umain.kDrawNow)
        umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        umain.MainForm.updatePoseInfo()
    
    def description(self):
        result = ""
        fullString = ""
        
        if self.field == "hide":
            if self.newAmendment.hide:
                fullString = "hide"
            else:
                fullString = "show"
        elif self.field == "rotate":
            if self.newAmendment.addRotations:
                fullString = "rotate"
            else:
                fullString = "remove rotation for"
        elif self.field == "scale":
            if self.newAmendment.multiplyScale:
                fullString = "scale"
            else:
                fullString = "remove scaling for"
        elif self.field == "scale above":
            if self.newAmendment.propagateScale:
                fullString = "scale-this-part-and-above"
            else:
                fullString = "remove scale-this-part-and-above for"
        else:
            fullString = "change " + self.field + " for"
        result = "posing: " + fullString + " part " + IntToStr(self.newAmendment.partID) + " in plant \"" + self.plant.getName() + "\""
        return result
    
class PdSelectPosingPartCommand(PdCommand):
    def __init__(self):
        self.plant = PdPlant()
        self.newPartID = 0L
        self.oldPartID = 0L
        self.oldPartType = ""
        self.newPartType = ""
    
    # ------------------------------------------------------------ PdSelectPosingPartCommand 
    def createWithPlantAndPartIDsAndTypes(self, aPlant, aNewPartID, anOldPartID, aNewPartType, anOldPartType):
        i = 0
        
        PdCommand.create(self)
        # selected posed part not saved
        self.commandChangesPlantFile = False
        self.plant = aPlant
        self.newPartID = aNewPartID
        self.oldPartID = anOldPartID
        self.newPartType = aNewPartType
        self.oldPartType = anOldPartType
        return self
    
    def doCommand(self):
        # selected posed part not saved
        self.commandChangesPlantFile = False
        PdCommand.doCommand(self)
        umain.MainForm.selectedPlantPartID = self.newPartID
        umain.MainForm.selectedPlantPartType = self.newPartType
        umain.MainForm.updatePosingForSelectedPlantPart()
        umain.MainForm.redrawFocusedPlantOnly(umain.kDrawNow)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        umain.MainForm.selectedPlantPartID = self.oldPartID
        umain.MainForm.selectedPlantPartType = self.oldPartType
        umain.MainForm.updatePosingForSelectedPlantPart()
        umain.MainForm.redrawFocusedPlantOnly(umain.kDrawNow)
    
    def description(self):
        result = ""
        if self.newPartID < 0:
            result = "deselect all parts of plant " + self.plant.getName()
        else:
            result = "select part " + IntToStr(self.newPartID) + " of plant " + self.plant.getName()
        return result
    
# ---------------------------------- commands that affect a list of plants, usually in a minor way 
class PdCommandWithListOfPlants(PdCommand):
    def __init__(self):
        self.plantList = TList()
        self.values = TListCollection()
        self.plant = PdPlant()
        self.removesPlantAmendments = False
        self.listOfAmendmentLists = TList()
    
    #for temporary use
    # ------------------------------------------------------------ PdCommandWithListOfPlants 
    def createWithListOfPlants(self, aList):
        i = 0
        
        PdCommand.create(self)
        self.plantList = delphi_compatability.TList().Create()
        if aList.Count > 0:
            for i in range(0, aList.Count):
                self.plantList.Add(aList.Items[i])
        self.values = ucollect.TListCollection().Create()
        self.listOfAmendmentLists = None
        return self
    
    def setUpToRemoveAmendmentsWhenDone(self):
        i = 0
        j = 0
        plant = PdPlant()
        aList = TList()
        
        # call this method after create method if the command should remove amendments
        self.removesPlantAmendments = True
        self.listOfAmendmentLists = delphi_compatability.TList().Create()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                plant = uplant.PdPlant(self.plantList.Items[i])
                aList = delphi_compatability.TList().Create()
                if plant.amendments.Count > 0:
                    for j in range(0, plant.amendments.Count):
                        aList.Add(uamendmt.PdPlantDrawingAmendment(plant.amendments.Items[j]))
                self.listOfAmendmentLists.Add(aList)
    
    def destroy(self):
        i = 0
        j = 0
        amendment = PdPlantDrawingAmendment()
        aList = TList()
        
        self.plantList.free
        self.plantList = None
        self.values.free
        self.values = None
        if (self.done) and (self.removesPlantAmendments):
            if (self.listOfAmendmentLists != None) and (self.listOfAmendmentLists.Count > 0):
                for i in range(0, self.listOfAmendmentLists.Count):
                    aList = delphi_compatability.TList(self.listOfAmendmentLists.Items[i])
                    if aList.Count > 0:
                        for j in range(0, aList.Count):
                            amendment = uamendmt.PdPlantDrawingAmendment(aList.Items[j])
                            amendment.free
                    aList.free
        self.listOfAmendmentLists.free
        self.listOfAmendmentLists = None
        PdCommand.destroy(self)
    
    def doCommand(self):
        i = 0
        atLeastOnePlantHadAmendments = False
        aList = TList()
        
        PdCommand.doCommand(self)
        if not self.removesPlantAmendments:
            return
        atLeastOnePlantHadAmendments = False
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                aList = delphi_compatability.TList(self.listOfAmendmentLists.Items[i])
                if aList.Count > 0:
                    atLeastOnePlantHadAmendments = True
                    uplant.PdPlant(self.plantList.Items[i]).clearPointersToAllAmendments()
        if atLeastOnePlantHadAmendments:
            umain.MainForm.updatePosingForFirstSelectedPlant()
    
    def undoCommand(self):
        i = 0
        atLeastOnePlantHadAmendments = False
        aList = TList()
        
        PdCommand.undoCommand(self)
        if not self.removesPlantAmendments:
            return
        atLeastOnePlantHadAmendments = False
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                aList = delphi_compatability.TList(self.listOfAmendmentLists.Items[i])
                if aList.Count > 0:
                    atLeastOnePlantHadAmendments = True
                    uplant.PdPlant(self.plantList.Items[i]).restoreAmendmentPointersToList(aList)
        if atLeastOnePlantHadAmendments:
            umain.MainForm.updatePosingForFirstSelectedPlant()
    
    def invalidateCombinedPlantRects(self):
        redrawRect = TRect()
        i = 0
        
        redrawRect = delphi_compatability.Bounds(0, 0, 0, 0)
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                delphi_compatability.UnionRect(redrawRect, redrawRect, uplant.PdPlant(self.plantList.Items[i]).boundsRect_pixels())
        umain.MainForm.invalidateDrawingRect(redrawRect)
    
class PdChangeSelectedPlantsCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.newList = TList()
    
    # ------------------------------------------------------------ PdChangeSelectedPlantsCommand 
    def createWithOldListOFPlantsAndNewList(self, aList, aNewList):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        #which plants are selected not saved
        self.commandChangesPlantFile = False
        self.newList = delphi_compatability.TList().Create()
        if aNewList.Count > 0:
            for i in range(0, aNewList.Count):
                self.newList.Add(aNewList.Items[i])
        return self
    
    def destroy(self):
        self.newList.free
        self.newList = None
        PdCommandWithListOfPlants.destroy(self)
    
    def doCommand(self):
        i = 0
        
        #which plants are selected not saved
        self.commandChangesPlantFile = False
        PdCommandWithListOfPlants.doCommand(self)
        # MainForm.deselectAllPlants; // don't want this, it updates, and we will be updating soon
        umain.MainForm.selectedPlants.Clear()
        if self.newList.Count > 0:
            umain.MainForm.selectedPlants.Add(self.newList.Items[0])
            if udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
                umain.MainForm.showOnePlantExclusively(umain.kDontDrawYet)
            else:
                if self.newList.Count > 1:
                    for i in range(1, self.newList.Count):
                        umain.MainForm.selectedPlants.Add(self.newList.Items[i])
        umain.MainForm.updateForChangeToPlantSelections()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        # MainForm.deselectAllPlants; // don't want this, it updates, and we will be updating soon
        umain.MainForm.selectedPlants.Clear()
        if self.plantList.Count > 0:
            umain.MainForm.selectedPlants.Add(self.plantList.Items[0])
            if udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
                umain.MainForm.showOnePlantExclusively(umain.kDontDrawYet)
            else:
                if self.plantList.Count > 1:
                    for i in range(1, self.plantList.Count):
                        umain.MainForm.selectedPlants.Add(self.plantList.Items[i])
        umain.MainForm.updateForChangeToPlantSelections()
    
    def description(self):
        result = ""
        if self.newList.Count <= 0:
            result = "deselect all plants"
        else:
            result = "select" + plantNamesForDescription(self.newList)
        return result
    
class PdSelectOrDeselectAllCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.deselect = False
    
    # ------------------------------------------------------------ PdSelectOrDeselectAllCommand 
    def doCommand(self):
        i = 0
        
        #which plants are selected not saved
        self.commandChangesPlantFile = False
        PdCommandWithListOfPlants.doCommand(self)
        if self.deselect:
            # MainForm.deselectAllPlants;
            umain.MainForm.deselectAllPlants()
        else:
            umain.MainForm.selectedPlants.Clear()
        if not self.deselect:
            if udomain.domain.plantManager.plants.Count > 0:
                for i in range(0, udomain.domain.plantManager.plants.Count):
                    umain.MainForm.selectedPlants.Add(udomain.domain.plantManager.plants.Items[i])
        umain.MainForm.updateForChangeToPlantSelections()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        if not self.deselect:
            # MainForm.deselectAllPlants;
            umain.MainForm.deselectAllPlants()
        else:
            umain.MainForm.selectedPlants.Clear()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                umain.MainForm.selectedPlants.Add(self.plantList.Items[i])
        umain.MainForm.updateForChangeToPlantSelections()
    
    def description(self):
        result = ""
        if self.deselect:
            result = "deselect all plants"
        else:
            result = "select all plants"
        return result
    
class PdResizePlantsCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.initialized = False
        self.doneInMouseCommand = False
        self.newValues = TListCollection()
        self.oldSizes = TListCollection()
        self.aspectRatios = TListCollection()
        self.dragStartPoint = TPoint()
        self.offset = TPoint()
        self.multiplier = 0.0
        self.newValue = 0.0
    
    # ------------------------------------------------------------ PdResizePlantsCommand 
    def createWithListOfPlants(self, aList):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.newValues = ucollect.TListCollection().Create()
        self.oldSizes = ucollect.TListCollection().Create()
        self.aspectRatios = ucollect.TListCollection().Create()
        return self
    
    def createWithListOfPlantsAndMultiplier(self, aList, aMultiplier):
        self.createWithListOfPlants(aList)
        self.saveInitialValues()
        self.multiplier = aMultiplier
        return self
    
    def createWithListOfPlantsAndNewValue(self, aList, aNewValue):
        self.createWithListOfPlants(aList)
        self.saveInitialValues()
        self.newValue = aNewValue
        return self
    
    def saveInitialValues(self):
        i = 0
        aspectRatio = 0.0
        
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                if usupport.rHeight(self.plant.boundsRect_pixels()) != 0:
                    aspectRatio = 1.0 * usupport.rWidth(self.plant.boundsRect_pixels()) / usupport.rHeight(self.plant.boundsRect_pixels())
                else:
                    aspectRatio = 1.0
                self.aspectRatios.Add(PdSingleValue().createWithSingle(aspectRatio))
                self.values.Add(PdSingleValue().createWithSingle(self.plant.drawingScale_PixelsPerMm))
                self.oldSizes.Add(PdPointValue().createWithPoint(Point(usupport.rWidth(self.plant.boundsRect_pixels()), usupport.rHeight(self.plant.boundsRect_pixels()))))
    
    def destroy(self):
        self.newValues.free
        self.newValues = None
        self.oldSizes.free
        self.oldSizes = None
        self.aspectRatios.free
        self.aspectRatios = None
        PdCommandWithListOfPlants.destroy(self)
    
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        result = self
        if aTrackPhase == ucommand.TrackPhase.trackPress:
            self.dragStartPoint = nextPoint
        elif (aTrackPhase == ucommand.TrackPhase.trackMove) and (mouseDidMove):
            if not self.initialized:
                self.saveInitialValues()
                self.initialized = True
                self.doneInMouseCommand = True
                self.offset = Point(0, 0)
                PdCommandWithListOfPlants.doCommand(self)
                return result
            if self.initialized:
                self.offset.X = nextPoint.X - self.dragStartPoint.X
                self.offset.Y = nextPoint.Y - self.dragStartPoint.Y
                self.doCommand()
        elif aTrackPhase == ucommand.TrackPhase.trackRelease:
            if (not mouseDidMove) or (not self.initialized):
                result = None
                self.free
        return result
    
    def doCommand(self):
        i = 0
        newSize = TPoint()
        oldSize = TPoint()
        aspectRatio = 0.0
        oldScale = 0.0
        
        if not self.doneInMouseCommand:
            PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count <= 0:
            return
        if (self.offset.X == 0) and (self.offset.Y == 0) and (self.multiplier == 0) and (self.newValue == 0):
            return
        try:
            if not self.doneInMouseCommand:
                ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            self.newValues.clear()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    if self.multiplier != 0:
                        self.plant.drawingScale_PixelsPerMm = self.plant.drawingScale_PixelsPerMm * self.multiplier
                    elif self.newValue != 0:
                        self.plant.drawingScale_PixelsPerMm = self.newValue
                    else:
                        oldSize = PdPointValue(self.oldSizes.Items[i]).savePoint
                        aspectRatio = PdSingleValue(self.aspectRatios.Items[i]).saveSingle
                        oldScale = PdSingleValue(self.values.Items[i]).saveSingle
                        # 10 pixels is arbitrary minimum
                        newSize.Y = umath.intMax(10, oldSize.Y - self.offset.Y)
                        newSize.X = intround(newSize.Y * aspectRatio)
                        self.plant.calculateDrawingScaleToFitSize(newSize)
                        if (self.plant.drawingScale_PixelsPerMm > oldScale) and (self.offset.Y > 0):
                            # this is to counteract a bug that when you resize down, it resizes up the first mouse move, then down
                            # can't figure out why, just putting in this ugly fix to stop it from doing that
                            self.plant.drawingScale_PixelsPerMm = oldScale
                    self.newValues.Add(PdSingleValue().createWithSingle(self.plant.drawingScale_PixelsPerMm))
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
        finally:
            if not self.doneInMouseCommand:
                ucursor.cursor_stopWait()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        try:
            ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.drawingScale_PixelsPerMm = PdSingleValue(self.values.Items[i]).saveSingle
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
        finally:
            ucursor.cursor_stopWait()
    
    def redoCommand(self):
        i = 0
        
        if not self.initialized:
            return
        PdCommandWithListOfPlants.undoCommand(self)
        try:
            ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.drawingScale_PixelsPerMm = PdSingleValue(self.newValues.Items[i]).saveSingle
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
        finally:
            ucursor.cursor_stopWait()
    
    def description(self):
        result = ""
        result = "resize" + plantNamesForDescription(self.plantList)
        return result
    
class PdResizePlantsToSameWidthOrHeightCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.newValues = TListCollection()
        self.oldSizes = TListCollection()
        self.newWidth = 0.0
        self.newHeight = 0.0
        self.changeWidth = False
    
    # ------------------------------------------------------------ PdResizePlantsToSameWidthOrHeightCommand 
    def createWithListOfPlantsAndNewWidthOrHeight(self, aList, aNewWidth, aNewHeight, aChangeWidth):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.newValues = ucollect.TListCollection().Create()
        self.oldSizes = ucollect.TListCollection().Create()
        self.saveInitialValues()
        self.newWidth = aNewWidth
        self.newHeight = aNewHeight
        self.changeWidth = aChangeWidth
        return self
    
    def saveInitialValues(self):
        i = 0
        
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.values.Add(PdSingleValue().createWithSingle(self.plant.drawingScale_PixelsPerMm))
                self.oldSizes.Add(PdPointValue().createWithPoint(Point(usupport.rWidth(self.plant.boundsRect_pixels()), usupport.rHeight(self.plant.boundsRect_pixels()))))
    
    def destroy(self):
        self.newValues.free
        self.newValues = None
        self.oldSizes.free
        self.oldSizes = None
        PdCommandWithListOfPlants.destroy(self)
    
    def doCommand(self):
        i = 0
        newScaleX = 0.0
        newScaleY = 0.0
        
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count <= 0:
            return
        try:
            ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            self.newValues.clear()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.recalculateBounds(umain.kDontDrawYet)
                    if self.changeWidth:
                        self.plant.drawingScale_PixelsPerMm = umath.safedivExcept(self.plant.drawingScale_PixelsPerMm * self.newWidth, usupport.rWidth(self.plant.boundsRect_pixels()), 0.1)
                    else:
                        self.plant.drawingScale_PixelsPerMm = umath.safedivExcept(self.plant.drawingScale_PixelsPerMm * self.newHeight, usupport.rHeight(self.plant.boundsRect_pixels()), 0.1)
                    self.newValues.Add(PdSingleValue().createWithSingle(self.plant.drawingScale_PixelsPerMm))
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
        finally:
            ucursor.cursor_stopWait()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.drawingScale_PixelsPerMm = PdSingleValue(self.values.Items[i]).saveSingle
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
        umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
    
    def redoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.drawingScale_PixelsPerMm = PdSingleValue(self.newValues.Items[i]).saveSingle
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
        umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
    
    def description(self):
        result = ""
        result = "scale" + plantNamesForDescription(self.plantList)
        return result
    
class PdPackPlantsCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.newScales = TListCollection()
        self.oldSizes = TListCollection()
        self.newPoints = TListCollection()
        self.oldPoints = TListCollection()
        self.focusRect = TRect()
    
    # ------------------------------------------------------------ PdPackPlantsCommand 
    def createWithListOfPlantsAndFocusRect(self, aList, aFocusRect):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.newScales = ucollect.TListCollection().Create()
        self.oldSizes = ucollect.TListCollection().Create()
        self.newPoints = ucollect.TListCollection().Create()
        self.oldPoints = ucollect.TListCollection().Create()
        self.saveInitialValues()
        self.focusRect = aFocusRect
        return self
    
    def saveInitialValues(self):
        i = 0
        
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.values.Add(PdSingleValue().createWithSingle(self.plant.drawingScale_PixelsPerMm))
                self.oldPoints.Add(PdPointValue().createWithPoint(self.plant.basePoint_pixels()))
                self.oldSizes.Add(PdPointValue().createWithPoint(Point(usupport.rWidth(self.plant.boundsRect_pixels()), usupport.rHeight(self.plant.boundsRect_pixels()))))
    
    def destroy(self):
        self.newScales.free
        self.newScales = None
        self.oldSizes.free
        self.oldSizes = None
        self.newPoints.free
        self.newPoints = None
        self.oldPoints.free
        self.oldPoints = None
        PdCommandWithListOfPlants.destroy(self)
    
    def doCommand(self):
        i = 0
        newScaleX = 0.0
        newScaleY = 0.0
        widestBox = 0
        tallestBox = 0
        tallestHeight = 0
        offset = TPoint()
        newPoint = TPoint()
        lastPlant = PdPlant()
        totalHeight = 0
        averageHeight = 0
        remainingX = 0
        plantScaleChanged = False
        newScale = 0.0
        
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count <= 0:
            return
        self.invalidateCombinedPlantRects()
        self.newScales.clear()
        self.newPoints.clear()
        lastPlant = None
        totalHeight = 0
        tallestHeight = 0
        try:
            ucursor.cursor_startWait()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    totalHeight = totalHeight + usupport.rHeight(self.plant.boundsRect_pixels())
            averageHeight = totalHeight / self.plantList.Count
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.recalculateBounds(umain.kDontDrawYet)
                    plantScaleChanged = False
                    # calculate new scale (resize based on average height)
                    newScale = umath.safedivExcept(self.plant.drawingScale_PixelsPerMm * averageHeight, usupport.rHeight(self.plant.boundsRect_pixels()) * 1.0, 0.1)
                    if abs(newScale - self.plant.drawingScale_PixelsPerMm) > self.plant.drawingScale_PixelsPerMm / 20.0:
                        # don't rescale and redraw plant if scale hardly changes
                        plantScaleChanged = True
                        self.plant.drawingScale_PixelsPerMm = newScale
                        self.plant.recalculateBounds(umain.kDontDrawYet)
                    self.newScales.Add(PdSingleValue().createWithSingle(self.plant.drawingScale_PixelsPerMm))
                    # calculate new position
                    offset.X = self.plant.basePoint_pixels().X - self.plant.boundsRect_pixels().Left
                    offset.Y = self.plant.basePoint_pixels().Y - self.plant.boundsRect_pixels().Top
                    remainingX = usupport.rWidth(self.plant.boundsRect_pixels()) - offset.X
                    if (i <= 0) or (lastPlant == None):
                        newPoint.X = offset.X + kGapBetweenArrangedPlants
                        newPoint.Y = offset.Y + kGapBetweenArrangedPlants
                    else:
                        newPoint.X = lastPlant.boundsRect_pixels().Right + kGapBetweenArrangedPlants + offset.X
                        newPoint.Y = lastPlant.boundsRect_pixels().Top + offset.Y
                    if newPoint.X + remainingX > umain.MainForm.drawingPaintBox.Width:
                        newPoint.X = offset.X + kGapBetweenArrangedPlants
                        newPoint.Y = tallestHeight + kGapBetweenArrangedPlants + offset.Y
                    self.plant.moveTo(newPoint)
                    self.newPoints.Add(PdPointValue().createWithPoint(self.plant.basePoint_pixels()))
                    if plantScaleChanged:
                        self.plant.recalculateBounds(umain.kDrawNow)
                    else:
                        self.plant.recalculateBoundsForOffsetChange()
                    lastPlant = self.plant
                    if self.plant.boundsRect_pixels().Bottom > tallestHeight:
                        tallestHeight = self.plant.boundsRect_pixels().Bottom
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
        finally:
            ucursor.cursor_stopWait()
    
    def undoCommand(self):
        i = 0
        oldScale = 0.0
        
        PdCommandWithListOfPlants.undoCommand(self)
        try:
            ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    oldScale = self.plant.drawingScale_PixelsPerMm
                    self.plant.drawingScale_PixelsPerMm = PdSingleValue(self.values.Items[i]).saveSingle
                    self.plant.moveTo(PdPointValue(self.oldPoints.Items[i]).savePoint)
                    if abs(self.plant.drawingScale_PixelsPerMm - oldScale) > self.plant.drawingScale_PixelsPerMm / 20.0:
                        # don't rescale and redraw plant if scale hardly changes
                        self.plant.recalculateBounds(umain.kDrawNow)
                    else:
                        self.plant.recalculateBoundsForOffsetChange()
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
        finally:
            ucursor.cursor_stopWait()
    
    def redoCommand(self):
        i = 0
        oldScale = 0.0
        
        PdCommandWithListOfPlants.undoCommand(self)
        try:
            ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    oldScale = self.plant.drawingScale_PixelsPerMm
                    self.plant.drawingScale_PixelsPerMm = PdSingleValue(self.newScales.Items[i]).saveSingle
                    self.plant.moveTo(PdPointValue(self.newPoints.Items[i]).savePoint)
                    if abs(self.plant.drawingScale_PixelsPerMm - oldScale) > self.plant.drawingScale_PixelsPerMm / 20.0:
                        # don't rescale and redraw plant if scale hardly changes
                        self.plant.recalculateBounds(umain.kDrawNow)
                    else:
                        self.plant.recalculateBoundsForOffsetChange()
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsDrawingScale()
        finally:
            ucursor.cursor_stopWait()
    
    def description(self):
        result = ""
        result = "pack" + plantNamesForDescription(self.plantList)
        return result
    
class PdChangeMainWindowViewingOptionCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.selectedList = TList()
        self.oldScale_PixelsPerMm = 0.0
        self.newScale_pixelsPerMm = 0.0
        self.oldOffset_mm = SinglePoint()
        self.newOffset_mm = SinglePoint()
        self.oldMainWindowViewingOption = 0
        self.newMainWindowViewingOption = 0
    
    # ------------------------------------------------------------ PdChangeMainWindowViewingOptionCommand 
    def createWithListOfPlantsAndSelectedPlantsAndNewOption(self, aList, aSelectedList, aNewOption):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        #hidden flag not saved
        self.commandChangesPlantFile = False
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.values.Add(PdBooleanValue().createWithBoolean(uplant.PdPlant(self.plantList.Items[i]).hidden))
        self.selectedList = delphi_compatability.TList().Create()
        if aSelectedList.Count > 0:
            for i in range(0, aSelectedList.Count):
                self.selectedList.Add(uplant.PdPlant(aSelectedList.Items[i]))
        self.oldMainWindowViewingOption = udomain.domain.options.mainWindowViewMode
        self.newMainWindowViewingOption = aNewOption
        return self
    
    def destroy(self):
        self.selectedList.free
        self.selectedList = None
        PdCommandWithListOfPlants.destroy(self)
    
    def doCommand(self):
        PdCommandWithListOfPlants.doCommand(self)
        try:
            ucursor.cursor_startWait()
            udomain.domain.options.mainWindowViewMode = self.newMainWindowViewingOption
            if self.newMainWindowViewingOption == udomain.kViewPlantsInMainWindowOneAtATime:
                self.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
                self.oldOffset_mm = udomain.domain.plantDrawOffset_mm()
                umain.MainForm.deselectAllPlantsButFirst()
                #hides all plants but first; calls fitVisiblePlantsInDrawingArea
                umain.MainForm.showOnePlantExclusively(umain.kDontDrawYet)
                umain.MainForm.recalculateSelectedPlantsBoundsRects(umain.kDrawNow)
                umain.MainForm.invalidateEntireDrawing()
                umain.MainForm.updateForChangeToPlantSelections()
                self.newScale_pixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
                self.newOffset_mm = udomain.domain.plantDrawOffset_mm()
            elif self.newMainWindowViewingOption == udomain.kViewPlantsInMainWindowFreeFloating:
                self.oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
                self.oldOffset_mm = udomain.domain.plantDrawOffset_mm()
                umain.MainForm.hideOrShowSomePlants(self.plantList, None, kShow, umain.kDontDrawYet)
                umain.MainForm.fitVisiblePlantsInDrawingArea(umain.kDontDrawYet, umain.kScaleAndMove, umain.kAlwaysMove)
                # first drawing gets correct bounds rects so numbers get counted for progress bar - messy
                umain.MainForm.recalculateAllPlantBoundsRects(umain.kDontDrawYet)
                umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow)
                umain.MainForm.invalidateEntireDrawing()
                self.newScale_pixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm()
                self.newOffset_mm = udomain.domain.plantDrawOffset_mm()
            umain.MainForm.updateMenusForChangeToViewingOption()
        finally:
            ucursor.cursor_stopWait()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        try:
            ucursor.cursor_startWait()
            udomain.domain.options.mainWindowViewMode = self.oldMainWindowViewingOption
            if self.newMainWindowViewingOption == udomain.kViewPlantsInMainWindowOneAtATime:
                umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow)
                umain.MainForm.invalidateSelectedPlantRectangles()
                udomain.domain.plantManager.plantDrawScale_PixelsPerMm = self.oldScale_PixelsPerMm
                udomain.domain.plantManager.plantDrawOffset_mm = self.oldOffset_mm
                # restore original hidden flags - all plants 
                #not used
                umain.MainForm.hideOrShowSomePlants(self.plantList, self.values, False, umain.kDontDrawYet)
                umain.MainForm.fitVisiblePlantsInDrawingArea(umain.kDontDrawYet, umain.kScaleAndMove, umain.kAlwaysMove)
                umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow)
                #MainForm.invalidateSelectedPlantRectangles;
                umain.MainForm.invalidateEntireDrawing()
                # restore original selection - selected plants only 
                umain.MainForm.selectedPlants.Clear()
                if self.selectedList.Count > 0:
                    for i in range(0, self.selectedList.Count):
                        umain.MainForm.selectedPlants.Add(uplant.PdPlant(self.selectedList.Items[i]))
                umain.MainForm.updateForChangeToPlantSelections()
            elif self.newMainWindowViewingOption == udomain.kViewPlantsInMainWindowFreeFloating:
                udomain.domain.plantManager.plantDrawScale_PixelsPerMm = self.oldScale_PixelsPerMm
                udomain.domain.plantManager.plantDrawOffset_mm = self.oldOffset_mm
                # restore original hidden flags - all plants 
                #not used
                umain.MainForm.hideOrShowSomePlants(self.plantList, self.values, False, umain.kDontDrawYet)
                umain.MainForm.fitVisiblePlantsInDrawingArea(umain.kDontDrawYet, umain.kScaleAndMove, umain.kAlwaysMove)
                umain.MainForm.recalculateAllPlantBoundsRects(umain.kDrawNow)
                #MainForm.invalidateSelectedPlantRectangles;
                umain.MainForm.invalidateEntireDrawing()
                umain.MainForm.updateForChangeToPlantSelections()
            umain.MainForm.updateMenusForChangeToViewingOption()
        finally:
            ucursor.cursor_stopWait()
    
    def description(self):
        result = ""
        result = "change view all/one option in main window"
        return result
    
class PdDragCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.initialized = False
        self.doneInMouseCommand = False
        self.dragAllPlantsToOnePoint = False
        self.dragStartPoint = TPoint()
        self.offset = TPoint()
        self.newPoint = TPoint()
    
    # ------------------------------------------------------------ PdDragCommand 
    def createWithListOfPlantsAndDragOffset(self, aList, anOffset):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.values.Add(PdPointValue().createWithPoint(self.plant.basePoint_pixels()))
        self.offset = anOffset
        self.initialized = True
        return self
    
    def createWithListOfPlantsAndNewPoint(self, aList, aNewPoint):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.dragAllPlantsToOnePoint = True
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.values.Add(PdPointValue().createWithPoint(self.plant.basePoint_pixels()))
        self.newPoint = aNewPoint
        self.initialized = True
        return self
    
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        i = 0
        
        result = self
        if aTrackPhase == ucommand.TrackPhase.trackPress:
            self.dragStartPoint = nextPoint
        elif aTrackPhase == ucommand.TrackPhase.trackMove:
            if (not self.initialized) and mouseDidMove:
                if self.plantList.Count > 0:
                    for i in range(0, self.plantList.Count):
                        self.plant = uplant.PdPlant(self.plantList.Items[i])
                        self.values.Add(PdPointValue().createWithPoint(self.plant.basePoint_pixels()))
                self.initialized = True
                PdCommandWithListOfPlants.doCommand(self)
            if self.initialized:
                self.offset.X = nextPoint.X - self.dragStartPoint.X
                self.offset.Y = nextPoint.Y - self.dragStartPoint.Y
                self.invalidateCombinedPlantRects()
                if self.plantList.Count > 0:
                    for i in range(0, self.plantList.Count):
                        self.plant = uplant.PdPlant(self.plantList.Items[i])
                        self.plant.moveTo(PdPointValue(self.values.Items[i]).savePoint)
                        self.plant.moveBy(self.offset)
                        if udomain.domain.options.cachePlantBitmaps:
                            self.plant.recalculateBoundsForOffsetChange()
                umain.MainForm.updateForChangeToSelectedPlantsLocation()
                self.invalidateCombinedPlantRects()
                self.doneInMouseCommand = True
        elif aTrackPhase == ucommand.TrackPhase.trackRelease:
            if not mouseDidMove:
                result = None
                self.free
        return result
    
    def doCommand(self):
        i = 0
        
        if self.doneInMouseCommand:
            #only used if not done by mouse command-otherwise done in trackMouse
            return
        PdCommandWithListOfPlants.doCommand(self)
        self.invalidateCombinedPlantRects()
        if self.dragAllPlantsToOnePoint:
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.moveTo(self.newPoint)
                    if udomain.domain.options.cachePlantBitmaps:
                        self.plant.recalculateBoundsForOffsetChange()
        else:
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.moveBy(self.offset)
                    if udomain.domain.options.cachePlantBitmaps:
                        self.plant.recalculateBoundsForOffsetChange()
        umain.MainForm.updateForChangeToSelectedPlantsLocation()
        self.invalidateCombinedPlantRects()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.moveTo(PdPointValue(self.values.Items[i]).savePoint)
                if udomain.domain.options.cachePlantBitmaps:
                    self.plant.recalculateBoundsForOffsetChange()
        umain.MainForm.updateForChangeToSelectedPlantsLocation()
        self.invalidateCombinedPlantRects()
    
    def redoCommand(self):
        i = 0
        
        if not self.initialized:
            return
        PdCommandWithListOfPlants.doCommand(self)
        self.invalidateCombinedPlantRects()
        if self.dragAllPlantsToOnePoint:
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.moveTo(self.newPoint)
                    if udomain.domain.options.cachePlantBitmaps:
                        self.plant.recalculateBoundsForOffsetChange()
        else:
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.moveBy(self.offset)
                    if udomain.domain.options.cachePlantBitmaps:
                        self.plant.recalculateBoundsForOffsetChange()
        umain.MainForm.updateForChangeToSelectedPlantsLocation()
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        if self.dragAllPlantsToOnePoint:
            result = "make bouquet"
        else:
            result = "drag" + plantNamesForDescription(self.plantList)
        return result
    
class PdAlignPlantsCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.newPoints = TListCollection()
        self.focusRect = TRect()
        self.alignDirection = 0
    
    # ------------------------------------------------------------ PdAlignPlantsCommand 
    def createWithListOfPlantsRectAndDirection(self, aList, aRect, aDirection):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.values.Add(PdPointValue().createWithPoint(self.plant.basePoint_pixels()))
        self.newPoints = ucollect.TListCollection().Create()
        self.focusRect = aRect
        self.alignDirection = aDirection
        return self
    
    def destroy(self):
        self.newPoints.free
        self.newPoints = None
        PdCommandWithListOfPlants.destroy(self)
    
    def doCommand(self):
        i = 0
        newPoint = TPoint()
        offset = TPoint()
        
        PdCommandWithListOfPlants.doCommand(self)
        self.newPoints.clear()
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                newPoint = self.plant.basePoint_pixels()
                offset.X = self.plant.basePoint_pixels().X - self.plant.boundsRect_pixels().Left
                offset.Y = self.plant.basePoint_pixels().Y - self.plant.boundsRect_pixels().Top
                if self.alignDirection == kUp:
                    newPoint.Y = self.focusRect.Top + offset.Y
                elif self.alignDirection == kDown:
                    newPoint.Y = self.focusRect.Bottom - (usupport.rHeight(self.plant.boundsRect_pixels()) - offset.Y)
                elif self.alignDirection == kLeft:
                    newPoint.X = self.focusRect.Left + offset.X
                elif self.alignDirection == kRight:
                    newPoint.X = self.focusRect.Right - (usupport.rWidth(self.plant.boundsRect_pixels()) - offset.X)
                self.plant.moveTo(newPoint)
                self.newPoints.Add(PdPointValue().createWithPoint(self.plant.basePoint_pixels()))
                if udomain.domain.options.cachePlantBitmaps:
                    self.plant.recalculateBoundsForOffsetChange()
        umain.MainForm.updateForChangeToSelectedPlantsLocation()
        self.invalidateCombinedPlantRects()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.moveTo(PdPointValue(self.values.Items[i]).savePoint)
                if udomain.domain.options.cachePlantBitmaps:
                    self.plant.recalculateBoundsForOffsetChange()
        umain.MainForm.updateForChangeToSelectedPlantsLocation()
        self.invalidateCombinedPlantRects()
    
    def redoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.moveTo(PdPointValue(self.newPoints.Items[i]).savePoint)
                if udomain.domain.options.cachePlantBitmaps:
                    self.plant.recalculateBoundsForOffsetChange()
        umain.MainForm.updateForChangeToSelectedPlantsLocation()
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        result = "align" + plantNamesForDescription(self.plantList)
        return result
    
class PdRotateCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.rotateDirection = 0
        self.newRotation = 0.0
        self.offsetRotation = 0.0
        self.startDragPoint = TPoint()
    
    # ------------------------------------------------------------ PdRotateCommand 
    def createWithListOfPlantsDirectionAndNewRotation(self, aList, aRotateDirection, aNewRotation):
        i = 0
        
        # create using this constructor if this is from clicking on a spinEdit 
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.rotateDirection = aRotateDirection
        self.newRotation = aNewRotation
        if self.newRotation < -360:
            self.newRotation = -360
        if self.newRotation > 360:
            self.newRotation = 360
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                if self.rotateDirection == kRotateX:
                    self.values.Add(PdSingleValue().createWithSingle(self.plant.xRotation))
                elif self.rotateDirection == kRotateY:
                    self.values.Add(PdSingleValue().createWithSingle(self.plant.yRotation))
                elif self.rotateDirection == kRotateZ:
                    self.values.Add(PdSingleValue().createWithSingle(self.plant.zRotation))
        return self
    
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        i = 0
        newRotation = 0.0
        
        result = self
        if aTrackPhase == ucommand.TrackPhase.trackPress:
            # assume that if this function is called, the command was not already initialized
            #    from clicking on a spinEdit, so we have no values and no rotateDirection 
            self.startDragPoint = nextPoint
            self.invalidateCombinedPlantRects()
            PdCommandWithListOfPlants.doCommand(self)
        elif aTrackPhase == ucommand.TrackPhase.trackMove:
            if self.rotateDirection == kRotateNotInitialized:
                if rightButtonDown:
                    self.rotateDirection = kRotateZ
                elif abs(nextPoint.X - self.startDragPoint.X) > abs(nextPoint.Y - self.startDragPoint.Y):
                    self.rotateDirection = kRotateX
                else:
                    self.rotateDirection = kRotateY
                if self.plantList.Count > 0:
                    for i in range(0, self.plantList.Count):
                        self.plant = uplant.PdPlant(self.plantList.Items[i])
                        if self.rotateDirection == kRotateX:
                            self.values.Add(PdSingleValue().createWithSingle(self.plant.xRotation))
                        elif self.rotateDirection == kRotateY:
                            self.values.Add(PdSingleValue().createWithSingle(self.plant.yRotation))
                        elif self.rotateDirection == kRotateZ:
                            self.values.Add(PdSingleValue().createWithSingle(self.plant.zRotation))
            self.invalidateCombinedPlantRects()
            if self.rotateDirection == kRotateX:
                self.offsetRotation = (nextPoint.X - self.startDragPoint.X) * 0.5
            elif self.rotateDirection == kRotateY:
                self.offsetRotation = (nextPoint.Y - self.startDragPoint.Y) * 0.5
            elif self.rotateDirection == kRotateZ:
                self.offsetRotation = (nextPoint.X - self.startDragPoint.X) * 0.5
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    newRotation = PdSingleValue(self.values.Items[i]).saveSingle + self.offsetRotation
                    if newRotation < -360:
                        newRotation = 360 - (abs(newRotation) - 360)
                    if newRotation > 360:
                        newRotation = -360 + (newRotation - 360)
                    if self.rotateDirection == kRotateX:
                        self.plant.xRotation = newRotation
                    elif self.rotateDirection == kRotateY:
                        self.plant.yRotation = newRotation
                    elif self.rotateDirection == kRotateZ:
                        self.plant.zRotation = newRotation
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToPlantRotations()
        elif aTrackPhase == ucommand.TrackPhase.trackRelease:
            if not mouseDidMove:
                # if they just clicked, rotate ten degrees anyway
                self.invalidateCombinedPlantRects()
                if self.plantList.Count > 0:
                    for i in range(0, self.plantList.Count):
                        self.plant = uplant.PdPlant(self.plantList.Items[i])
                        self.values.Add(PdSingleValue().createWithSingle(self.plant.xRotation))
                self.rotateDirection = kRotateX
                if rightButtonDown:
                    # v2.0 if they just clicked with the right mouse button, rotate -10 degrees
                    # v2.0 use the domain rotation increment instead of always 10 degrees
                    self.offsetRotation = -udomain.domain.options.rotationIncrement
                else:
                    self.offsetRotation = udomain.domain.options.rotationIncrement
                if self.plantList.Count > 0:
                    for i in range(0, self.plantList.Count):
                        self.plant = uplant.PdPlant(self.plantList.Items[i])
                        newRotation = PdSingleValue(self.values.Items[i]).saveSingle + self.offsetRotation
                        if newRotation < -360:
                            newRotation = 360 - (abs(newRotation) - 360)
                        if newRotation > 360:
                            newRotation = -360 + (newRotation - 360)
                        self.plant.xRotation = newRotation
                        self.plant.recalculateBounds(umain.kDrawNow)
                self.invalidateCombinedPlantRects()
                umain.MainForm.updateForChangeToPlantRotations()
        return result
    
    def doCommand(self):
        i = 0
        
        if self.done:
            #if done in mousemove 
            return
        PdCommandWithListOfPlants.doCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                if self.rotateDirection == kRotateX:
                    if self.offsetRotation != 0:
                        self.plant.xRotation = umath.min(360, umath.max(-360, PdSingleValue(self.values.Items[i]).saveSingle + self.offsetRotation))
                    else:
                        self.plant.xRotation = self.newRotation
                elif self.rotateDirection == kRotateY:
                    if self.offsetRotation != 0:
                        self.plant.yRotation = umath.min(360, umath.max(-360, PdSingleValue(self.values.Items[i]).saveSingle + self.offsetRotation))
                    else:
                        self.plant.yRotation = self.newRotation
                elif self.rotateDirection == kRotateZ:
                    if self.offsetRotation != 0:
                        self.plant.zRotation = umath.min(360, umath.max(-360, PdSingleValue(self.values.Items[i]).saveSingle + self.offsetRotation))
                    else:
                        self.plant.zRotation = self.newRotation
                self.plant.recalculateBounds(umain.kDrawNow)
        umain.MainForm.updateForChangeToPlantRotations()
        self.invalidateCombinedPlantRects()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                if self.rotateDirection == kRotateX:
                    self.plant.xRotation = PdSingleValue(self.values.Items[i]).saveSingle
                elif self.rotateDirection == kRotateY:
                    self.plant.yRotation = PdSingleValue(self.values.Items[i]).saveSingle
                elif self.rotateDirection == kRotateZ:
                    self.plant.zRotation = PdSingleValue(self.values.Items[i]).saveSingle
                self.plant.recalculateBounds(umain.kDrawNow)
        umain.MainForm.updateForChangeToPlantRotations()
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        result = nameForDirection(self.rotateDirection) + " rotate" + plantNamesForDescription(self.plantList)
        return result
    
class PdResetRotationsCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.oldX = 0.0
        self.oldY = 0.0
        self.oldZ = 0.0
    
    # ------------------------------------------------------------ PdResetRotationsCommand 
    def doCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.values.Add(PdXYZValue().createWithXYZ(self.plant.xRotation, self.plant.yRotation, self.plant.zRotation))
                self.plant.xRotation = 0
                self.plant.yRotation = 0
                self.plant.zRotation = 0
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
        umain.MainForm.updateForChangeToPlantRotations()
    
    def redoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.xRotation = 0
                self.plant.yRotation = 0
                self.plant.zRotation = 0
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
        umain.MainForm.updateForChangeToPlantRotations()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.xRotation = PdXYZValue(self.values.Items[i]).x
                self.plant.yRotation = PdXYZValue(self.values.Items[i]).y
                self.plant.zRotation = PdXYZValue(self.values.Items[i]).z
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
        umain.MainForm.updateForChangeToPlantRotations()
    
    def description(self):
        result = ""
        result = "reset rotation for" + plantNamesForDescription(self.plantList)
        return result
    
class PdChangeDrawingScaleCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.newScale = 0.0
    
    # ------------------------------------------------------------ PdChangeDrawingScaleCommand 
    def createWithListOfPlantsAndNewScale(self, aList, aNewScale):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.newScale = aNewScale
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.values.Add(PdSingleValue().createWithSingle(uplant.PdPlant(self.plantList.Items[i]).drawingScale_PixelsPerMm))
        return self
    
    def doCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.drawingScale_PixelsPerMm = self.newScale
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.drawingScale_PixelsPerMm = PdSingleValue(self.values.Items[i]).saveSingle
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        result = "change scale for" + plantNamesForDescription(self.plantList)
        return result
    
class PdChangePlantAgeCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.newAge = 0
    
    # ----------------------------------------------------------------------- PdChangePlantAgeCommand 
    def createWithListOfPlantsAndNewAge(self, aList, aNewAge):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.newAge = aNewAge
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.values.Add(PdSmallintValue().createWithSmallint(uplant.PdPlant(self.plantList.Items[i]).age))
        return self
    
    def doCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        try:
            ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    # if primary selected plant has longer lifespan than other selected plants, cut off age
                    #        at max for those plants 
                    self.plant.setAge(umath.intMin(self.newAge, self.plant.pGeneral.ageAtMaturity))
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsLocation()
            # changing age causes life cycle panel to need to redraw 
            umain.MainForm.updateLifeCyclePanelForFirstSelectedPlant()
        finally:
            ucursor.cursor_stopWait()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        try:
            ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.setAge(PdSmallintValue(self.values.Items[i]).saveSmallint)
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsLocation()
            # changing age causes life cycle panel to need to redraw 
            umain.MainForm.updateLifeCyclePanelForFirstSelectedPlant()
        finally:
            ucursor.cursor_stopWait()
    
    # redo is same as do 
    def description(self):
        result = ""
        result = "change age to " + IntToStr(self.newAge) + " for" + plantNamesForDescription(self.plantList)
        return result
    
class PdAnimatePlantCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.age = 0
        self.oldestAgeAtMaturity = 0
    
    # ----------------------------------------------------------------------- PdAnimatePlantCommand 
    def createWithListOfPlants(self, aList):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.values.Add(PdSmallintValue().createWithSmallint(uplant.PdPlant(self.plantList.Items[i]).age))
        return self
    
    def doCommand(self):
        i = 0
        plant = PdPlant()
        
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count <= 0:
            return
        self.age = 0
        # find oldest age 
        self.oldestAgeAtMaturity = 0
        for i in range(0, self.plantList.Count):
            plant = uplant.PdPlant(self.plantList.Items[i])
            if (i == 0) or (plant.pGeneral.ageAtMaturity > self.oldestAgeAtMaturity):
                self.oldestAgeAtMaturity = plant.pGeneral.ageAtMaturity
        # reset all plants to age zero and draw them 
        udomain.domain.temporarilyHideSelectionRectangles = True
        self.invalidateCombinedPlantRects()
        try:
            for i in range(0, self.plantList.Count):
                plant = uplant.PdPlant(self.plantList.Items[i])
                plant.reset()
                plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForPossibleChangeToDrawing()
        finally:
            udomain.domain.temporarilyHideSelectionRectangles = False
        umain.MainForm.animateCommand = self
        umain.MainForm.startAnimation()
    
    def animateOneDay(self):
        i = 0
        plant = PdPlant()
        
        # grow all plants one day 
        udomain.domain.temporarilyHideSelectionRectangles = True
        try:
            self.invalidateCombinedPlantRects()
            for i in range(0, self.plantList.Count):
                plant = uplant.PdPlant(self.plantList.Items[i])
                if self.age < plant.pGeneral.ageAtMaturity:
                    plant.nextDay()
                    plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            if umain.MainForm.lifeCycleShowing():
                # don't want to update params, because they don't change during animation 
                umain.MainForm.updateLifeCyclePanelForFirstSelectedPlant()
            elif umain.MainForm.statsShowing():
                umain.MainForm.updateStatisticsPanelForFirstSelectedPlant()
            umain.MainForm.updateForPossibleChangeToDrawing()
            self.age += 1
        finally:
            udomain.domain.temporarilyHideSelectionRectangles = False
        if self.age >= self.oldestAgeAtMaturity:
            umain.MainForm.stopAnimation()
        umain.MainForm.updateForChangeToSelectedPlantsLocation()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        try:
            ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.plant.setAge(PdSmallintValue(self.values.Items[i]).saveSmallint)
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
            umain.MainForm.updateForChangeToSelectedPlantsLocation()
            # changing age causes life cycle panel to need to redraw 
            umain.MainForm.updateLifeCyclePanelForFirstSelectedPlant()
        finally:
            ucursor.cursor_stopWait()
    
    # redo is same as do 
    def description(self):
        result = ""
        result = "animate" + plantNamesForDescription(self.plantList)
        return result
    
class PdHideOrShowCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.hide = False
        self.newValues = TListCollection()
    
    # ------------------------------------------------------------ PdHideOrShowCommand 
    def createWithListOfPlantsAndHideOrShow(self, aList, aHide):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        #hidden flag not saved
        self.commandChangesPlantFile = False
        self.hide = aHide
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.values.Add(PdBooleanValue().createWithBoolean(uplant.PdPlant(self.plantList.Items[i]).hidden))
        return self
    
    def createWithListOfPlantsAndListOfHides(self, aList, aHideList):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        #hidden flag not saved
        self.commandChangesPlantFile = False
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.values.Add(PdBooleanValue().createWithBoolean(uplant.PdPlant(self.plantList.Items[i]).hidden))
        self.newValues = ucollect.TListCollection().Create()
        if aHideList.Count > 0:
            for i in range(0, aHideList.Count):
                self.newValues.Add(PdBooleanValue().createWithBoolean(PdBooleanValue(aHideList.Items[i]).saveBoolean))
        return self
    
    def destroy(self):
        self.newValues.free
        self.newValues = None
        PdCommandWithListOfPlants.destroy(self)
    
    def doCommand(self):
        PdCommandWithListOfPlants.doCommand(self)
        umain.MainForm.hideOrShowSomePlants(self.plantList, self.newValues, self.hide, umain.kDontDrawYet)
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        umain.MainForm.hideOrShowSomePlants(self.plantList, self.values, self.hide, umain.kDontDrawYet)
    
    def description(self):
        result = ""
        if (self.newValues != None) and (self.newValues.Count > 0):
            result = "hide others"
        elif self.hide:
            result = "hide" + plantNamesForDescription(self.plantList)
        else:
            result = "show" + plantNamesForDescription(self.plantList)
        return result
    
class PdRandomizeCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.oldSeeds = TListCollection()
        self.oldBreedingSeeds = TListCollection()
        self.newSeeds = TListCollection()
        self.newBreedingSeeds = TListCollection()
        self.oldXRotations = TListCollection()
        self.newXRotations = TListCollection()
        self.isInBreeder = False
        self.isRandomizeAllInBreeder = False
    
    # ----------------------------------------------------------------------- PdRandomizeCommand 
    def createWithListOfPlants(self, aList):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.oldSeeds = ucollect.TListCollection().Create()
        self.oldBreedingSeeds = ucollect.TListCollection().Create()
        self.newSeeds = ucollect.TListCollection().Create()
        self.newBreedingSeeds = ucollect.TListCollection().Create()
        self.oldXRotations = ucollect.TListCollection().Create()
        self.newXRotations = ucollect.TListCollection().Create()
        self.setUpToRemoveAmendmentsWhenDone()
        return self
    
    def destroy(self):
        self.oldSeeds.free
        self.oldSeeds = None
        self.oldBreedingSeeds.free
        self.oldBreedingSeeds = None
        self.newSeeds.free
        self.newSeeds = None
        self.newBreedingSeeds.free
        self.newBreedingSeeds = None
        self.oldXRotations.free
        self.oldXRotations = None
        self.newXRotations.free
        self.newXRotations = None
    
    def doCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        try:
            ucursor.cursor_startWait()
            if not self.isInBreeder:
                self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.oldSeeds.Add(PdSmallintValue().createWithSmallint(self.plant.pGeneral.startingSeedForRandomNumberGenerator))
                    self.oldBreedingSeeds.Add(PdLongintValue().createWithLongint(self.plant.breedingGenerator.seed))
                    self.oldXRotations.Add(PdSingleValue().createWithSingle(self.plant.xRotation))
                    self.plant.randomize()
                    self.newSeeds.Add(PdSmallintValue().createWithSmallint(self.plant.pGeneral.startingSeedForRandomNumberGenerator))
                    self.newBreedingSeeds.Add(PdLongintValue().createWithLongint(self.plant.breedingGenerator.seed))
                    self.newXRotations.Add(PdSingleValue().createWithSingle(self.plant.xRotation))
                    if self.isInBreeder:
                        self.plant.previewCacheUpToDate = False
                    else:
                        self.plant.recalculateBounds(umain.kDrawNow)
            if self.isInBreeder:
                if self.plantList.Count == 1:
                    self.plant = uplant.PdPlant(self.plantList.Items[0])
                    ubreedr.BreederForm.updateForChangeToPlant(self.plant)
                else:
                    ubreedr.BreederForm.updateForChangeToGenerations()
            else:
                self.invalidateCombinedPlantRects()
                umain.MainForm.updateForChangeToPlantRotations()
        finally:
            ucursor.cursor_stopWait()
    
    def undoCommand(self):
        i = 0
        seed = 0
        breedingSeed = 0L
        xRotation = 0.0
        
        PdCommandWithListOfPlants.undoCommand(self)
        try:
            ucursor.cursor_startWait()
            if not self.isInBreeder:
                self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    seed = PdSmallintValue(self.oldSeeds.Items[i]).saveSmallint
                    breedingSeed = PdLongintValue(self.oldBreedingSeeds.Items[i]).saveLongint
                    xRotation = PdSingleValue(self.oldXRotations.Items[i]).saveSingle
                    self.plant.randomizeWithSeedsAndXRotation(seed, breedingSeed, xRotation)
                    if self.isInBreeder:
                        self.plant.previewCacheUpToDate = False
                    else:
                        self.plant.recalculateBounds(umain.kDrawNow)
            if self.isInBreeder:
                if self.plantList.Count == 1:
                    self.plant = uplant.PdPlant(self.plantList.Items[0])
                    ubreedr.BreederForm.updateForChangeToPlant(self.plant)
                else:
                    ubreedr.BreederForm.updateForChangeToGenerations()
            else:
                self.invalidateCombinedPlantRects()
                umain.MainForm.updateForChangeToPlantRotations()
        finally:
            ucursor.cursor_stopWait()
    
    def redoCommand(self):
        i = 0
        seed = 0
        breedingSeed = 0L
        xRotation = 0.0
        
        PdCommandWithListOfPlants.doCommand(self)
        try:
            ucursor.cursor_startWait()
            if not self.isInBreeder:
                self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    seed = PdSmallintValue(self.newSeeds.Items[i]).saveSmallint
                    breedingSeed = PdLongintValue(self.newBreedingSeeds.Items[i]).saveLongint
                    xRotation = PdSingleValue(self.newXRotations.Items[i]).saveSingle
                    self.plant.randomizeWithSeedsAndXRotation(seed, breedingSeed, xRotation)
                    if self.isInBreeder:
                        self.plant.previewCacheUpToDate = False
                    else:
                        self.plant.recalculateBounds(umain.kDrawNow)
            if self.isInBreeder:
                if self.plantList.Count == 1:
                    self.plant = uplant.PdPlant(self.plantList.Items[0])
                    ubreedr.BreederForm.updateForChangeToPlant(self.plant)
                else:
                    ubreedr.BreederForm.updateForChangeToGenerations()
            else:
                self.invalidateCombinedPlantRects()
                umain.MainForm.updateForChangeToPlantRotations()
        finally:
            ucursor.cursor_stopWait()
    
    def description(self):
        result = ""
        if self.isRandomizeAllInBreeder:
            result = "randomize all in breeder"
        elif self.isInBreeder:
            result = "randomize in breeder"
        else:
            result = "randomize" + plantNamesForDescription(self.plantList)
        return result
    
# -------------------------------------------------------------- commands that add plants, no special superclass 
class PdPasteCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.useSpecialPastePosition = False
        self.oldSelectedList = TList()
    
    # doesn't use values, but uses plantList 
    # v2.0
    # --------------------------------------------------------------------------------------------- PdPasteCommand 
    def createWithListOfPlantsAndOldSelectedList(self, aList, anOldSelectedList):
        i = 0
        
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        # selected list is just pointers, this doesn't take control of them
        self.oldSelectedList = delphi_compatability.TList().Create()
        if (anOldSelectedList != None) and (anOldSelectedList.Count > 0):
            for i in range(0, anOldSelectedList.Count):
                self.oldSelectedList.Add(anOldSelectedList.Items[i])
        return self
    
    def destroy(self):
        i = 0
        
        self.oldSelectedList.free
        self.oldSelectedList = None
        if (not self.done) and (self.plantList != None) and (self.plantList.Count > 0):
            for i in range(0, self.plantList.Count):
                # free copies of pasted plants if change was undone 
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.free
        #will free plantList TList
        PdCommandWithListOfPlants.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        result = 0
        if (not self.done) and (self.plantList != None):
            result = self.plantList.Count
        return result
    
    def doCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count <= 0:
            return
        # make new plants the only selected plants 
        umain.MainForm.deselectAllPlants()
        for i in range(0, self.plantList.Count):
            self.plant = uplant.PdPlant(self.plantList.Items[i])
            # put new plants at end of plant manager list 
            udomain.domain.plantManager.plants.Add(self.plant)
            if not self.useSpecialPastePosition:
                if not udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
                    self.plant.moveTo(umain.MainForm.standardPastePosition())
                    if not self.plant.justCopiedFromMainWindow:
                        self.plant.calculateDrawingScaleToLookTheSameWithDomainScale()
            self.plant.recalculateBounds(umain.kDrawNow)
            umain.MainForm.addSelectedPlant(self.plant, kAddAtEnd)
        umain.MainForm.updateForChangeToPlantList()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        if self.plantList.Count <= 0:
            return
        for i in range(0, self.plantList.Count):
            self.plant = uplant.PdPlant(self.plantList.Items[i])
            udomain.domain.plantManager.plants.Remove(self.plant)
            umain.MainForm.removeSelectedPlant(self.plant)
        if self.oldSelectedList.Count > 0:
            for i in range(0, self.oldSelectedList.Count):
                # put back selections from before paste
                umain.MainForm.selectedPlants.Add(self.oldSelectedList.Items[i])
        umain.MainForm.updateForChangeToPlantList()
    
    def description(self):
        result = ""
        result = "paste" + plantNamesForDescription(self.plantList)
        return result
    
class PdDuplicateCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.startDragPoint = TPoint()
        self.offset = TPoint()
        self.newPlants = TList()
        self.inTrackMouse = False
    
    # ------------------------------------------------------------------------ PdDuplicateCommand 
    def createWithListOfPlants(self, aList):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.newPlants = delphi_compatability.TList().Create()
        return self
    
    def destroy(self):
        i = 0
        
        if (not self.done) and (self.newPlants != None) and (self.newPlants.Count > 0):
            for i in range(0, self.newPlants.Count):
                # free copies of created plants if change was undone 
                self.plant = uplant.PdPlant(self.newPlants.Items[i])
                self.plant.free
        self.newPlants.free
        self.newPlants = None
        #will free plantList
        PdCommandWithListOfPlants.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        result = 0
        if (not self.done) and (self.newPlants != None):
            result = self.newPlants.Count
        return result
    
    def TrackMouse(self, aTrackPhase, anchorPoint, previousPoint, nextPoint, mouseDidMove, rightButtonDown):
        result = PdCommand()
        i = 0
        originalPlant = PdPlant()
        
        result = self
        if aTrackPhase == ucommand.TrackPhase.trackPress:
            pass
        elif aTrackPhase == ucommand.TrackPhase.trackMove:
            if not self.done and mouseDidMove:
                self.startDragPoint = nextPoint
                self.inTrackMouse = True
                self.doCommand()
            if not self.done:
                return result
            if not delphi_compatability.PtInRect(umain.MainForm.drawingPaintBox.ClientRect, nextPoint):
                self.undoCommand()
                result = None
                self.free
            else:
                self.offset.X = nextPoint.X - self.startDragPoint.X
                self.offset.Y = nextPoint.Y - self.startDragPoint.Y
                if self.newPlants.Count > 0:
                    for i in range(0, self.newPlants.Count):
                        self.plant = uplant.PdPlant(self.newPlants.Items[i])
                        if (i <= self.plantList.Count - 1):
                            originalPlant = uplant.PdPlant(self.plantList.Items[i])
                            umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
                            self.plant.moveTo(originalPlant.basePoint_pixels())
                            self.plant.moveBy(self.offset)
                            # only draw if don't have picture yet
                            self.plant.recalculateBounds(self.plant.previewCache.Width < 5)
                            umain.MainForm.invalidateDrawingRect(self.plant.boundsRect_pixels())
        elif aTrackPhase == ucommand.TrackPhase.trackRelease:
            if not mouseDidMove:
                result = None
                self.free
        return result
    
    def doCommand(self):
        i = 0
        plantCopy = PdPlant()
        
        if self.done:
            # should have been done in the mouse down, unless it was done by a menu command 
            return
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count <= 0:
            return
        # make new plants only selected plants 
        umain.MainForm.deselectAllPlants()
        for i in range(0, self.plantList.Count):
            self.plant = uplant.PdPlant(self.plantList.Items[i])
            plantCopy = self.plant.makeCopy()
            plantCopy.shrinkPreviewCache()
            plantCopy.setName("Copy of " + plantCopy.getName())
            if not self.inTrackMouse:
                plantCopy.moveBy(Point(kPasteMoveDistance, 0))
            plantCopy.recalculateBounds(umain.kDrawNow)
            self.newPlants.Add(plantCopy)
            udomain.domain.plantManager.addPlant(plantCopy)
            umain.MainForm.addSelectedPlant(plantCopy, kAddAtEnd)
        umain.MainForm.updateForChangeToPlantList()
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        if self.newPlants.Count <= 0:
            return
        for i in range(0, self.newPlants.Count):
            self.plant = uplant.PdPlant(self.newPlants.Items[i])
            udomain.domain.plantManager.plants.Remove(self.plant)
            umain.MainForm.removeSelectedPlant(self.plant)
        umain.MainForm.updateForChangeToPlantList()
    
    def redoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        if self.newPlants.Count <= 0:
            return
        umain.MainForm.deselectAllPlants()
        for i in range(0, self.newPlants.Count):
            self.plant = uplant.PdPlant(self.newPlants.Items[i])
            udomain.domain.plantManager.addPlant(self.plant)
            umain.MainForm.addSelectedPlant(self.plant, kAddAtEnd)
        umain.MainForm.updateForChangeToPlantList()
    
    def description(self):
        result = ""
        result = "duplicate" + plantNamesForDescription(self.plantList)
        return result
    
# -------------------------------------------------------------------------------- remove command is unique 
class PdRemoveCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.removedPlants = TList()
        self.copyToClipboard = False
    
    # doesn't use values, but uses plantList 
    # --------------------------------------------------------------------------------------------- PdRemoveCommand 
    def createWithListOfPlantsAndClipboardFlag(self, aList, aCopyToClipboard):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.removedPlants = delphi_compatability.TList().Create()
        self.copyToClipboard = aCopyToClipboard
        return self
    
    def destroy(self):
        i = 0
        
        if (self.done) and (self.removedPlants != None) and (self.removedPlants.Count > 0):
            for i in range(0, self.removedPlants.Count):
                # free copies of cut plants if change was done 
                self.plant = uplant.PdPlant(self.removedPlants.Items[i])
                self.plant.free
        self.removedPlants.free
        self.removedPlants = None
        PdCommandWithListOfPlants.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        result = 0
        if (self.done) and (self.removedPlants != None):
            result = self.removedPlants.Count
        return result
    
    def doCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count <= 0:
            return
        if self.copyToClipboard:
            # copy plants 
            umain.MainForm.copySelectedPlantsToClipboard()
        # save copy of plants before deleting 
        self.removedPlants.Clear()
        for i in range(0, self.plantList.Count):
            # don't remove plants from plant manager and MainForm.selectedPlants until all indexes have been recorded 
            self.plant = uplant.PdPlant(self.plantList.Items[i])
            self.removedPlants.Add(self.plant)
            self.plant.indexWhenRemoved = udomain.domain.plantManager.plants.IndexOf(self.plant)
            self.plant.selectedIndexWhenRemoved = umain.MainForm.selectedPlants.IndexOf(self.plant)
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                udomain.domain.plantManager.plants.Remove(self.plant)
                umain.MainForm.removeSelectedPlant(self.plant)
        umain.MainForm.updateForChangeToPlantList()
        if udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
            # if only looking at one, select first in list so you are not left with nothing
            umain.MainForm.selectFirstPlantInPlantList()
            umain.MainForm.showOnePlantExclusively(umain.kDrawNow)
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        if udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
            # remove selection if created
            umain.MainForm.deselectAllPlants()
        if self.removedPlants.Count > 0:
            for i in range(0, self.removedPlants.Count):
                self.plant = uplant.PdPlant(self.removedPlants.Items[i])
                if (self.plant.indexWhenRemoved >= 0) and (self.plant.indexWhenRemoved <= udomain.domain.plantManager.plants.Count - 1):
                    udomain.domain.plantManager.plants.Insert(self.plant.indexWhenRemoved, self.plant)
                else:
                    udomain.domain.plantManager.plants.Add(self.plant)
                # all removed plants must have been selected, so also add them to the selected list 
                umain.MainForm.addSelectedPlant(self.plant, self.plant.selectedIndexWhenRemoved)
        umain.MainForm.updateForChangeToPlantList()
    
    def description(self):
        result = ""
        if self.copyToClipboard:
            result = "cut" + plantNamesForDescription(self.plantList)
        else:
            result = "delete" + plantNamesForDescription(self.plantList)
        return result
    
# ---------------------------------------------------------------------------------- domain change commands 
class PdChangeValueCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.fieldNumber = 0
        self.regrow = False
    
    # ------------------------------------------------------------------------------- value change commands 
    # -------------------------------------------------------------------------------- PdChangeValueCommand 
    def createCommandWithListOfPlants(self, aList, aFieldNumber, aRegrow):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.fieldNumber = aFieldNumber
        self.regrow = aRegrow
        if self.regrow:
            self.setUpToRemoveAmendmentsWhenDone()
        return self
    
    def description(self):
        result = ""
        param = PdParameter()
        
        result = ""
        param = None
        if (udomain.domain != None) and (udomain.domain.parameterManager != None):
            # subclasses may want to call 
            param = udomain.domain.parameterManager.parameterForFieldNumber(self.fieldNumber)
            if (param != None):
                result = "\"" + param.getName() + "\""
        return result
    
class PdChangeRealValueCommand(PdChangeValueCommand):
    def __init__(self):
        self.newValue = 0.0
        self.arrayIndex = 0
    
    # ------------------------------------------------------------ PdChangeRealValueCommand 
    def createCommandWithListOfPlants(self, aList, aNewValue, aFieldNumber, anArrayIndex, aRegrow):
        oldValue = 0.0
        i = 0
        
        PdChangeValueCommand.createCommandWithListOfPlants(self, aList, aFieldNumber, aRegrow)
        self.newValue = aNewValue
        self.arrayIndex = anArrayIndex
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = self.plant.editTransferField(umath.kGetField, oldValue, self.fieldNumber, uparams.kFieldFloat, self.arrayIndex, self.regrow)
                self.values.Add(PdSingleValue().createWithSingle(oldValue))
        return self
    
    def doCommand(self):
        i = 0
        
        PdChangeValueCommand.doCommand(self)
        try:
            if self.regrow:
                ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.newValue = self.plant.editTransferField(umath.kSetField, self.newValue, self.fieldNumber, uparams.kFieldFloat, self.arrayIndex, self.regrow)
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
        finally:
            if self.regrow:
                ucursor.cursor_stopWait()
    
    def undoCommand(self):
        oldValue = 0.0
        i = 0
        
        PdChangeValueCommand.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = PdSingleValue(self.values.Items[i]).saveSingle
                oldValue = self.plant.editTransferField(umath.kSetField, oldValue, self.fieldNumber, uparams.kFieldFloat, self.arrayIndex, self.regrow)
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        result = PdChangeValueCommand.description(self)
        result = "change " + result
        if self.arrayIndex != -1:
            result = result + " (" + IntToStr(self.arrayIndex + 1) + ")"
        result = result + " to " + usupport.digitValueString(self.newValue) + " in " + plantNamesForDescription(self.plantList)
        return result
    
class PdChangeSCurvePointValueCommand(PdChangeValueCommand):
    def __init__(self):
        self.newX = 0.0
        self.newY = 0.0
        self.pointIndex = 0
    
    # ------------------------------------------------------------ PdChangeSCurvePointValueCommand 
    def createCommandWithListOfPlants(self, aList, aNewX, aNewY, aFieldNumber, aPointIndex, aRegrow):
        oldX = 0.0
        oldY = 0.0
        i = 0
        
        PdChangeValueCommand.createCommandWithListOfPlants(self, aList, aFieldNumber, aRegrow)
        self.newX = aNewX
        self.newY = aNewY
        self.pointIndex = aPointIndex
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldX = self.plant.editTransferField(umath.kGetField, oldX, self.fieldNumber, uparams.kFieldFloat, self.pointIndex * 2, self.regrow)
                oldY = self.plant.editTransferField(umath.kGetField, oldY, self.fieldNumber, uparams.kFieldFloat, self.pointIndex * 2 + 1, self.regrow)
                self.values.Add(PdSinglePointValue().createWithSingleXY(oldX, oldY))
        return self
    
    def doCommand(self):
        i = 0
        
        PdChangeValueCommand.doCommand(self)
        try:
            if self.regrow:
                ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    # first time, set values without calculating
                    self.plant.changingWholeSCurves = True
                    self.newX = self.plant.editTransferField(umath.kSetField, self.newX, self.fieldNumber, uparams.kFieldFloat, self.pointIndex * 2, self.regrow)
                    self.newY = self.plant.editTransferField(umath.kSetField, self.newY, self.fieldNumber, uparams.kFieldFloat, self.pointIndex * 2 + 1, self.regrow)
                    # second time, now that both values are set, set first one again to calc s curve
                    self.plant.changingWholeSCurves = False
                    self.newX = self.plant.editTransferField(umath.kSetField, self.newX, self.fieldNumber, uparams.kFieldFloat, self.pointIndex * 2, self.regrow)
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
        finally:
            if self.regrow:
                ucursor.cursor_stopWait()
    
    def undoCommand(self):
        oldX = 0.0
        oldY = 0.0
        i = 0
        
        PdChangeValueCommand.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldX = PdSinglePointValue(self.values.Items[i]).x
                oldY = PdSinglePointValue(self.values.Items[i]).y
                oldX = self.plant.editTransferField(umath.kSetField, oldX, self.fieldNumber, uparams.kFieldFloat, self.pointIndex * 2, self.regrow)
                oldY = self.plant.editTransferField(umath.kSetField, oldY, self.fieldNumber, uparams.kFieldFloat, self.pointIndex * 2 + 1, self.regrow)
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        result = PdChangeValueCommand.description(self)
        result = "change " + result + " point " + IntToStr(self.pointIndex + 1) + " to (" + usupport.digitValueString(self.newX) + ", " + usupport.digitValueString(self.newY) + ")" + " in " + plantNamesForDescription(self.plantList)
        return result
    
class PdChangeColorValueCommand(PdChangeValueCommand):
    def __init__(self):
        self.newColor = TColorRef()
    
    # ------------------------------------------------------------ PdChangeColorValueCommand 
    def createCommandWithListOfPlants(self, aList, aNewValue, aFieldNumber, anArrayIndex, aRegrow):
        oldValue = TColorRef()
        i = 0
        
        PdChangeValueCommand.createCommandWithListOfPlants(self, aList, aFieldNumber, aRegrow)
        self.newColor = aNewValue
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = self.plant.editTransferField(umath.kGetField, oldValue, self.fieldNumber, uparams.kFieldColor, uparams.kNotArray, self.regrow)
                self.values.Add(PdColorValue().createWithColor(oldValue))
        return self
    
    def doCommand(self):
        i = 0
        
        PdChangeValueCommand.doCommand(self)
        try:
            if self.regrow:
                ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.newColor = self.plant.editTransferField(umath.kSetField, self.newColor, self.fieldNumber, uparams.kFieldColor, uparams.kNotArray, self.regrow)
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
        finally:
            if self.regrow:
                ucursor.cursor_stopWait()
    
    def undoCommand(self):
        oldValue = TColorRef()
        i = 0
        
        PdChangeValueCommand.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = PdColorValue(self.values.Items[i]).saveColor
                oldValue = self.plant.editTransferField(umath.kSetField, oldValue, self.fieldNumber, uparams.kFieldColor, uparams.kNotArray, self.regrow)
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        result = PdChangeValueCommand.description(self)
        result = "change " + result + " to (R " + IntToStr(UNRESOLVED.getRValue(self.newColor)) + ", G " + IntToStr(UNRESOLVED.getGValue(self.newColor)) + ", B " + IntToStr(UNRESOLVED.getBValue(self.newColor)) + ")" + " in " + plantNamesForDescription(self.plantList)
        return result
    
class PdChangeTdoValueCommand(PdChangeValueCommand):
    def __init__(self):
        self.newTdo = KfObject3D()
    
    # ------------------------------------------------------------ PdChangeTdoValueCommand 
    def createCommandWithListOfPlants(self, aList, aNewValue, aFieldNumber, aRegrow):
        valueTdo = KfObject3D()
        i = 0
        
        PdChangeValueCommand.createCommandWithListOfPlants(self, aList, aFieldNumber, aRegrow)
        self.newTdo = utdo.KfObject3D().create()
        self.newTdo.copyFrom(aNewValue)
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                valueTdo = utdo.KfObject3D().create()
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                valueTdo = self.plant.editTransferField(umath.kGetField, valueTdo, self.fieldNumber, uparams.kFieldThreeDObject, uparams.kNotArray, self.regrow)
                self.values.Add(valueTdo)
        return self
    
    def destroy(self):
        self.newTdo.free
        self.newTdo = None
        # value tdos will be freed by values listCollection 
        PdChangeValueCommand.destroy(self)
    
    def doCommand(self):
        i = 0
        
        PdChangeValueCommand.doCommand(self)
        try:
            if self.regrow:
                ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.newTdo = self.plant.editTransferField(umath.kSetField, self.newTdo, self.fieldNumber, uparams.kFieldThreeDObject, uparams.kNotArray, self.regrow)
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
        finally:
            if self.regrow:
                ucursor.cursor_stopWait()
    
    def undoCommand(self):
        oldValue = KfObject3D()
        i = 0
        
        PdChangeValueCommand.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = utdo.KfObject3D(self.values.Items[i])
                oldValue = self.plant.editTransferField(umath.kSetField, oldValue, self.fieldNumber, uparams.kFieldThreeDObject, uparams.kNotArray, self.regrow)
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        result = PdChangeValueCommand.description(self)
        result = "change " + result + " to \"" + self.newTdo.getName() + "\" in " + plantNamesForDescription(self.plantList)
        return result
    
class PdChangeSmallintValueCommand(PdChangeValueCommand):
    def __init__(self):
        self.newValue = 0
        self.arrayIndex = 0
    
    # ------------------------------------------------------------ PdChangeSmallintValueCommand 
    def createCommandWithListOfPlants(self, aList, aNewValue, aFieldNumber, anArrayIndex, aRegrow):
        oldValue = 0
        i = 0
        
        PdChangeValueCommand.createCommandWithListOfPlants(self, aList, aFieldNumber, aRegrow)
        self.newValue = aNewValue
        self.arrayIndex = anArrayIndex
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = self.plant.editTransferField(umath.kGetField, oldValue, self.fieldNumber, uparams.kFieldSmallint, self.arrayIndex, self.regrow)
                self.values.Add(PdSmallintValue().createWithSmallint(oldValue))
        return self
    
    def doCommand(self):
        i = 0
        
        PdChangeValueCommand.doCommand(self)
        try:
            if self.regrow:
                ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.newValue = self.plant.editTransferField(umath.kSetField, self.newValue, self.fieldNumber, uparams.kFieldSmallint, self.arrayIndex, self.regrow)
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
        finally:
            if self.regrow:
                ucursor.cursor_stopWait()
    
    def undoCommand(self):
        oldValue = 0
        i = 0
        
        PdChangeValueCommand.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = PdSmallintValue(self.values.Items[i]).saveSmallint
                oldValue = self.plant.editTransferField(umath.kSetField, oldValue, self.fieldNumber, uparams.kFieldSmallint, self.arrayIndex, self.regrow)
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        result = PdChangeValueCommand.description(self)
        result = "change " + result + " to " + IntToStr(self.newValue) + " in " + plantNamesForDescription(self.plantList)
        return result
    
class PdChangeBooleanValueCommand(PdChangeValueCommand):
    def __init__(self):
        self.newValue = False
        self.arrayIndex = 0
    
    # ------------------------------------------------------------ PdChangeBooleanValueCommand 
    def createCommandWithListOfPlants(self, aList, aNewValue, aFieldNumber, anArrayIndex, aRegrow):
        oldValue = False
        i = 0
        
        PdChangeValueCommand.createCommandWithListOfPlants(self, aList, aFieldNumber, aRegrow)
        self.newValue = aNewValue
        self.arrayIndex = anArrayIndex
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = self.plant.editTransferField(umath.kGetField, oldValue, self.fieldNumber, uparams.kFieldBoolean, self.arrayIndex, self.regrow)
                self.values.Add(PdBooleanValue().createWithBoolean(oldValue))
        return self
    
    def doCommand(self):
        i = 0
        
        PdChangeValueCommand.doCommand(self)
        try:
            if self.regrow:
                ucursor.cursor_startWait()
            self.invalidateCombinedPlantRects()
            if self.plantList.Count > 0:
                for i in range(0, self.plantList.Count):
                    self.plant = uplant.PdPlant(self.plantList.Items[i])
                    self.newValue = self.plant.editTransferField(umath.kSetField, self.newValue, self.fieldNumber, uparams.kFieldBoolean, self.arrayIndex, self.regrow)
                    self.plant.recalculateBounds(umain.kDrawNow)
            self.invalidateCombinedPlantRects()
        finally:
            if self.regrow:
                ucursor.cursor_stopWait()
    
    def undoCommand(self):
        oldValue = False
        i = 0
        
        PdChangeValueCommand.undoCommand(self)
        self.invalidateCombinedPlantRects()
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                oldValue = PdBooleanValue(self.values.Items[i]).saveBoolean
                oldValue = self.plant.editTransferField(umath.kSetField, oldValue, self.fieldNumber, uparams.kFieldBoolean, self.arrayIndex, self.regrow)
                self.plant.recalculateBounds(umain.kDrawNow)
        self.invalidateCombinedPlantRects()
    
    def description(self):
        result = ""
        newValueString = ""
        
        result = PdChangeValueCommand.description(self)
        if self.newValue:
            newValueString = "yes"
        else:
            newValueString = "no"
        result = "change " + result + " to " + newValueString + " in " + plantNamesForDescription(self.plantList)
        return result
    
# ---------------------------------------------------------------------------- breeder commands 
class PdBreedFromParentsCommand(PdCommand):
    def __init__(self):
        self.firstParent = None
        self.secondParent = None
        self.fractionOfMaxAge = 0.0
        self.row = 0
        self.oldGenerations = None
        self.newGeneration = None
        self.firstGeneration = None
        self.createFirstGeneration = False
        self.rowSelectedAtStart = 0
    
    # ---------------------------------------------------------------------------- PdBreedFromTwoParentsCommand 
    def createWithInfo(self, existingGenerations, aFirstParent, aSecondParent, aRow, aFractionOfMaxAge, aCreateFirstGeneration):
        PdCommand.create(self)
        self.commandChangesPlantFile = False
        self.firstParent = aFirstParent
        if self.firstParent == None:
            raise GeneralException.create("Problem: Need at least one parent in method PdBreedFromParentsCommand.createWithInfo.")
        self.secondParent = aSecondParent
        self.fractionOfMaxAge = aFractionOfMaxAge
        self.row = aRow
        self.createFirstGeneration = aCreateFirstGeneration
        if self.row < 0:
            #from main window 
            self.row = ubreedr.BreederForm.selectedRow
        self.oldGenerations = ucollect.TListCollection()
        for generation in existingGenerations:
            self.oldGenerations.Add(generation)
        return self
    
    def destroy(self):
        lastGeneration = PdGeneration()
        
        if self.done:
            while self.oldGenerations.Count - 1 > self.row:
                # free all generations below row 
                lastGeneration = ugener.PdGeneration(self.oldGenerations.Items[self.oldGenerations.Count - 1])
                self.oldGenerations.Remove(lastGeneration)
                lastGeneration.free
            # free new generation (and first generation if created, if not it will be nil) 
        else:
            self.firstGeneration.free
            self.firstGeneration = None
            self.newGeneration.free
            self.newGeneration = None
        self.oldGenerations.free
        self.oldGenerations = None
        PdCommand.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        i = 0
        generation = PdGeneration()
        
        result = 0
        if self.done:
            if self.oldGenerations.Count > 0:
                for i in range(0, self.oldGenerations.Count):
                    generation = ugener.PdGeneration(self.oldGenerations.Items[i])
                    result = result + generation.plants.Count
        else:
            if self.firstGeneration != None:
                result = self.firstGeneration.plants.Count
            if self.newGeneration != None:
                result = self.newGeneration.plants.Count
        return result
    
    def doCommand(self):
        PdCommand.doCommand(self)
        try:
            ucursor.cursor_startWait()
            self.rowSelectedAtStart = ubreedr.BreederForm.selectedRow
            if self.createFirstGeneration:
                # if command created from main window, create first generation to put in breeder 
                self.firstGeneration = ugener.PdGeneration().createWithParents(self.firstParent, self.secondParent, self.fractionOfMaxAge)
            # create generation that is outcome of breeding and do breeding 
            self.newGeneration = ugener.PdGeneration()
            self.newGeneration.breedFromParents(self.firstParent, self.secondParent, self.fractionOfMaxAge)
            # tell breeder to forget about other generations below the selected row  
            ubreedr.BreederForm.forgetGenerationsListBelowRow(self.row)
            if self.firstGeneration != None:
                ubreedr.BreederForm.addGeneration(self.firstGeneration)
                ubreedr.BreederForm.selectGeneration(self.firstGeneration)
            ubreedr.BreederForm.updateForChangeToGenerations()
            if self.row < len(self.oldGenerations):
                # set the firstParent and secondParent pointers in the generation that was bred (either the firstGeneration
                #      or the generation selected in the breeder) 
                generationBred = self.oldGenerations[self.row]
                generationBred.firstParent = generationBred.firstSelectedPlant()
                generationBred.secondParent = generationBred.secondSelectedPlant()
            # add and select the new generation in the breeder 
            ubreedr.BreederForm.addGeneration(self.newGeneration)
            ubreedr.BreederForm.selectGeneration(self.newGeneration)
            ubreedr.BreederForm.updateForChangeToGenerations()
        finally:
            ucursor.cursor_stopWait()
    
    def undoCommand(self):
        generationBred = PdGeneration()
        
        PdCommand.undoCommand(self)
        # tell the breeder to forget about the generation(s) created by this command, and if there were any generations
        #    wiped out by it, tell the breeder to restore pointers to all generations that were forgotten 
        ubreedr.BreederForm.forgetLastGeneration()
        if self.firstGeneration != None:
            ubreedr.BreederForm.forgetLastGeneration()
        ubreedr.BreederForm.updateForChangeToGenerations()
        ubreedr.BreederForm.addGenerationsFromListBelowRow(self.row, self.oldGenerations)
        ubreedr.BreederForm.selectedRow = self.rowSelectedAtStart
        if self.row <= self.oldGenerations.Count - 1:
            # set parent pointers of generation that was bred (firstGeneration or generation selected) to nil 
            generationBred = ugener.PdGeneration(self.oldGenerations.Items[self.row])
            generationBred.firstParent = None
            generationBred.secondParent = None
        ubreedr.BreederForm.updateForChangeToGenerations()
    
    def redoCommand(self):
        generationBred = PdGeneration()
        
        PdCommand.doCommand(self)
        # tell breeder to forget about other generations below the selected row (the whole list if from the main window) 
        ubreedr.BreederForm.forgetGenerationsListBelowRow(self.row)
        if self.firstGeneration != None:
            ubreedr.BreederForm.addGeneration(self.firstGeneration)
            ubreedr.BreederForm.selectGeneration(self.firstGeneration)
        ubreedr.BreederForm.updateForChangeToGenerations()
        if self.row <= self.oldGenerations.Count - 1:
            # set the firstParent and secondParent pointers in the generation that was bred (either the firstGeneration
            #    or the generation selected in the breeder) 
            generationBred = ugener.PdGeneration(self.oldGenerations.Items[self.row])
            generationBred.firstParent = generationBred.firstSelectedPlant()
            generationBred.secondParent = generationBred.secondSelectedPlant()
        # add and select the new generation in the breeder 
        ubreedr.BreederForm.addGeneration(self.newGeneration)
        ubreedr.BreederForm.selectGeneration(self.newGeneration)
        ubreedr.BreederForm.updateForChangeToGenerations()
    
    def description(self):
        result = ""
        if self.createFirstGeneration:
            # plant(s) from main window
            result = "breed"
            if self.firstParent != None:
                result = result + " \"" + self.firstParent.getName() + "\""
            if self.secondParent != None:
                result = result + ", \"" + self.secondParent.getName() + "\""
        else:
            result = "breed from breeder row " + IntToStr(self.row + 1)
        return result
    
class PdReplaceBreederPlant(PdCommand):
    def __init__(self):
        self.originalPlant = PdPlant()
        self.newPlant = PdPlant()
        self.plantDraggedFrom = PdPlant()
        self.row = 0
        self.column = 0
    
    # ------------------------------------------------------------------- PdReplaceBreederPlant 
    def createWithPlantRowAndColumn(self, aPlant, aRow, aColumn):
        PdCommand.create(self)
        self.commandChangesPlantFile = False
        self.plantDraggedFrom = aPlant
        if self.plantDraggedFrom == None:
            raise GeneralException.create("Problem: Nil plant dragged from in method PdReplaceBreederPlant.createWithPlantRowAndColumn.")
        self.row = aRow
        self.column = aColumn
        return self
    
    def destroy(self):
        if self.done:
            self.originalPlant.free
            self.originalPlant = None
        else:
            self.newPlant.free
            self.newPlant = None
        PdCommand.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        #has one plant in either case (done or undone)
        result = 1
        return result
    
    def doCommand(self):
        PdCommand.doCommand(self)
        self.originalPlant = ubreedr.BreederForm.plantForRowAndColumn(self.row, self.column)
        if self.originalPlant == None:
            raise GeneralException.create("Problem: Invalid row and column in method PdReplaceBreederPlant.doCommand.")
        self.newPlant = self.plantDraggedFrom.makeCopy()
        ubreedr.BreederForm.replacePlantInRow(self.originalPlant, self.newPlant, self.row)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        ubreedr.BreederForm.replacePlantInRow(self.newPlant, self.originalPlant, self.row)
    
    def redoCommand(self):
        PdCommand.doCommand(self)
        ubreedr.BreederForm.replacePlantInRow(self.originalPlant, self.newPlant, self.row)
    
    def description(self):
        result = ""
        result = "replace breeder plant in row " + IntToStr(self.row + 1) + ", column " + IntToStr(self.column)
        return result
    
class PdMakeTimeSeriesCommand(PdCommand):
    def __init__(self):
        self.oldPlants = TList()
        self.newPlants = TList()
        self.newPlant = PdPlant()
        self.isPaste = False
    
    # ------------------------------------------------------------------- PdMakeTimeSeriesCommand 
    def createWithNewPlant(self, aNewPlant):
        PdCommand.create(self)
        self.commandChangesPlantFile = False
        self.newPlant = aNewPlant
        if self.newPlant == None:
            raise GeneralException.create("Problem: Nil plant in method PdMakeTimeSeriesCommand.createWithNewPlant.")
        self.oldPlants = delphi_compatability.TList().Create()
        self.newPlants = delphi_compatability.TList().Create()
        return self
    
    def destroy(self):
        i = 0
        
        if self.done:
            if (self.oldPlants != None) and (self.oldPlants.Count > 0):
                for i in range(0, self.oldPlants.Count):
                    uplant.PdPlant(self.oldPlants.Items[i]).free
        else:
            if (self.newPlants != None) and (self.newPlants.Count > 0):
                for i in range(0, self.newPlants.Count):
                    uplant.PdPlant(self.newPlants.Items[i]).free
        self.oldPlants.free
        self.oldPlants = None
        self.newPlants.free
        self.newPlants = None
        PdCommand.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        result = 0
        if self.done:
            if self.oldPlants != None:
                result = self.oldPlants.Count
        else:
            if self.newPlants != None:
                result = self.newPlants.Count
        return result
    
    def doCommand(self):
        i = 0
        
        PdCommand.doCommand(self)
        if utimeser.TimeSeriesForm.plants.Count > 0:
            for i in range(0, utimeser.TimeSeriesForm.plants.Count):
                self.oldPlants.Add(utimeser.TimeSeriesForm.plants.Items[i])
        utimeser.TimeSeriesForm.plants.clearPointersWithoutDeletingObjects()
        #redraws in updateForChangeToPlants
        utimeser.TimeSeriesForm.initializeWithPlant(self.newPlant, umain.kDontDrawYet)
        if utimeser.TimeSeriesForm.plants.Count > 0:
            for i in range(0, utimeser.TimeSeriesForm.plants.Count):
                self.newPlants.Add(utimeser.TimeSeriesForm.plants.Items[i])
        utimeser.TimeSeriesForm.updateForChangeToPlants(utimeser.kRecalculateScale)
    
    def undoCommand(self):
        i = 0
        
        PdCommand.undoCommand(self)
        utimeser.TimeSeriesForm.plants.clearPointersWithoutDeletingObjects()
        if self.oldPlants.Count > 0:
            for i in range(0, self.oldPlants.Count):
                utimeser.TimeSeriesForm.plants.Add(self.oldPlants.Items[i])
        utimeser.TimeSeriesForm.updateForChangeToPlants(utimeser.kDontRecalculateScale)
    
    def redoCommand(self):
        i = 0
        
        PdCommand.doCommand(self)
        utimeser.TimeSeriesForm.plants.clearPointersWithoutDeletingObjects()
        if self.newPlants.Count > 0:
            for i in range(0, self.newPlants.Count):
                utimeser.TimeSeriesForm.plants.Add(self.newPlants.Items[i])
        utimeser.TimeSeriesForm.updateForChangeToPlants(utimeser.kDontRecalculateScale)
    
    def description(self):
        result = ""
        if self.isPaste:
            result = "paste into time series window"
        else:
            result = "make time series"
            if self.newPlant != None:
                result = result + " for plant \"" + self.newPlant.getName() + "\""
        return result
    
class PdChangeBreedingAndTimeSeriesOptionsCommand(PdCommand):
    def __init__(self):
        self.oldOptions = BreedingAndTimeSeriesOptionsStructure()
        self.newOptions = BreedingAndTimeSeriesOptionsStructure()
        self.oldDomainOptions = DomainOptionsStructure()
        self.newDomainOptions = DomainOptionsStructure()
    
    # -------------------------------------------------------------- PdChangeBreederOptionsCommand 
    def createWithOptionsAndDomainOptions(self, anOptions, aDomainOptions):
        PdCommand.create(self)
        self.commandChangesPlantFile = False
        self.newOptions = anOptions
        self.oldOptions = udomain.domain.breedingAndTimeSeriesOptions
        self.newDomainOptions = aDomainOptions
        self.oldDomainOptions = udomain.domain.options
        return self
    
    def doCommand(self):
        PdCommand.doCommand(self)
        udomain.domain.breedingAndTimeSeriesOptions = self.newOptions
        udomain.domain.options = self.newDomainOptions
        ubreedr.BreederForm.updateForChangeToDomainOptions()
        utimeser.TimeSeriesForm.updateForChangeToDomainOptions()
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        udomain.domain.breedingAndTimeSeriesOptions = self.oldOptions
        udomain.domain.options = self.oldDomainOptions
        ubreedr.BreederForm.updateForChangeToDomainOptions()
        utimeser.TimeSeriesForm.updateForChangeToDomainOptions()
    
    # redo is same as do 
    def description(self):
        result = ""
        result = "change breeding and time series options"
        return result
    
class PdDeleteBreederGenerationCommand(PdCommand):
    def __init__(self):
        self.generation = PdGeneration()
        self.row = 0
    
    # ------------------------------------------------------------------------ PdDeleteBreederGenerationCommand 
    def createWithGeneration(self, aGeneration):
        PdCommand.create(self)
        self.commandChangesPlantFile = False
        self.generation = aGeneration
        if self.generation == None:
            raise GeneralException.create("Problem: Nil generation in method PdDeleteBreederGenerationCommand.createWithGeneration.")
        self.row = ubreedr.BreederForm.generations.IndexOf(self.generation)
        if self.row < 0:
            raise GeneralException.create("Problem: Generation not in list in method PdDeleteBreederGenerationCommand.createWithGeneration.")
        return self
    
    def destroy(self):
        if self.done:
            self.generation.free
            self.generation = None
        PdCommand.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        result = 0
        if (self.done) and (self.generation != None):
            result = self.generation.plants.Count
        return result
    
    def doCommand(self):
        index = 0
        
        PdCommand.doCommand(self)
        index = ubreedr.BreederForm.generations.IndexOf(self.generation)
        ubreedr.BreederForm.generations.Remove(self.generation)
        if index > 0:
            ubreedr.BreederForm.selectedRow = index - 1
        ubreedr.BreederForm.updateForChangeToGenerations()
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        ubreedr.BreederForm.generations.Insert(self.row, self.generation)
        ubreedr.BreederForm.selectedRow = ubreedr.BreederForm.generations.IndexOf(self.generation)
        ubreedr.BreederForm.updateForChangeToGenerations()
    
    def description(self):
        result = ""
        result = "delete breeder generation"
        return result
    
class PdDeleteAllBreederGenerationsCommand(PdCommand):
    def __init__(self):
        self.generations = TListCollection()
    
    # ------------------------------------------------------------------- PdDeleteAllBreederGenerationsCommand 
    def create(self):
        i = 0
        
        self.generations = ucollect.TListCollection().Create()
        if ubreedr.BreederForm.generations.Count > 0:
            for i in range(0, ubreedr.BreederForm.generations.Count):
                self.generations.Add(ubreedr.BreederForm.generations.Items[i])
        return self
    
    def destroy(self):
        if not self.done:
            self.generations.clearPointersWithoutDeletingObjects()
        self.generations.free
        self.generations = None
        PdCommand.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        i = 0
        generation = PdGeneration()
        
        result = 0
        if self.done:
            if self.generations.Count > 0:
                for i in range(0, self.generations.Count):
                    generation = ugener.PdGeneration(self.generations.Items[i])
                    result = result + generation.plants.Count
        return result
    
    def doCommand(self):
        PdCommand.doCommand(self)
        ubreedr.BreederForm.generations.clearPointersWithoutDeletingObjects()
        ubreedr.BreederForm.updateForChangeToGenerations()
    
    def undoCommand(self):
        i = 0
        
        PdCommand.undoCommand(self)
        if self.generations.Count > 0:
            for i in range(0, self.generations.Count):
                ubreedr.BreederForm.generations.Add(self.generations.Items[i])
        ubreedr.BreederForm.updateForChangeToGenerations()
    
    #redo same as do
    def description(self):
        result = ""
        result = "delete all breeder generations"
        return result
    
# ------------------------------------------------------------------------ time series 
class PdChangeNumberOfTimeSeriesStagesCommand(PdCommand):
    def __init__(self):
        self.newNumber = 0
        self.oldNumber = 0
    
    # -------------------------------------------------------- PdChangeNumberOfTimeSeriesStagesCommand 
    def createWithNewNumberOfStages(self, aNumber):
        PdCommand.create(self)
        self.commandChangesPlantFile = False
        self.newNumber = aNumber
        self.oldNumber = udomain.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages
        return self
    
    def doCommand(self):
        PdCommand.doCommand(self)
        udomain.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages = self.newNumber
        utimeser.TimeSeriesForm.updateForChangeToDomainOptions()
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        udomain.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages = self.oldNumber
        utimeser.TimeSeriesForm.updateForChangeToDomainOptions()
    
    def description(self):
        result = ""
        result = "change number of time series stages"
        return result
    
class PdDeleteTimeSeriesCommand(PdCommand):
    def __init__(self):
        self.plants = TListCollection()
    
    # -------------------------------------------------------- PdDeleteTimeSeriesCommand 
    def create(self):
        i = 0
        
        self.plants = ucollect.TListCollection().Create()
        if utimeser.TimeSeriesForm.plants.Count > 0:
            for i in range(0, utimeser.TimeSeriesForm.plants.Count):
                self.plants.Add(utimeser.TimeSeriesForm.plants.Items[i])
        return self
    
    def destroy(self):
        if not self.done:
            self.plants.clearPointersWithoutDeletingObjects()
        self.plants.free
        self.plants = None
        PdCommand.destroy(self)
    
    def numberOfStoredLargeObjects(self):
        result = 0L
        if self.done:
            result = self.plants.Count
        else:
            result = 0
        return result
    
    def doCommand(self):
        PdCommand.doCommand(self)
        utimeser.TimeSeriesForm.plants.clearPointersWithoutDeletingObjects()
        utimeser.TimeSeriesForm.updateForChangeToPlants(utimeser.kDontRecalculateScale)
    
    def undoCommand(self):
        i = 0
        
        PdCommand.undoCommand(self)
        if self.plants.Count > 0:
            for i in range(0, self.plants.Count):
                utimeser.TimeSeriesForm.plants.Add(self.plants.Items[i])
        utimeser.TimeSeriesForm.updateForChangeToPlants(utimeser.kDontRecalculateScale)
    
    #redo same as do
    def description(self):
        result = ""
        result = "delete time series"
        return result
    
