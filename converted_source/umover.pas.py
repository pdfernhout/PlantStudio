# unit Umover

from conversion_common import *
import ubmpsupport
import uturtle
import umath
import usupport
import ucursor
import umain
import udomain
import updform
import updcom
import ucommand
import uplant
import uplantmn
import delphi_compatability

# const
kLeft = 0
kRight = 1
kNewPlantFileName = "untitled.pla"
kThisManager = true
kOtherManager = false

# var
MoverForm = TMoverForm()

# const
kBetweenGap = 4

class TMoverForm(PdForm):
    def __init__(self):
        self.leftPlantFileNameEdit = TEdit()
        self.leftOpenClose = TButton()
        self.rightPlantFileNameEdit = TEdit()
        self.rightOpenClose = TButton()
        self.newFile = TButton()
        self.transfer = TButton()
        self.close = TButton()
        self.previewImage = TImage()
        self.undo = TButton()
        self.redo = TButton()
        self.cut = TButton()
        self.copy = TButton()
        self.paste = TButton()
        self.rename = TButton()
        self.duplicate = TButton()
        self.delete = TButton()
        self.leftPlantFileChangedIndicator = TImage()
        self.rightPlantFileChangedIndicator = TImage()
        self.leftPlantList = TDrawGrid()
        self.rightPlantList = TDrawGrid()
        self.helpButton = TSpeedButton()
        self.leftPlantFileName = ""
        self.rightPlantFileName = ""
        self.leftManager = PdPlantManager()
        self.rightManager = PdPlantManager()
        self.leftPlantFileChanged = false
        self.rightPlantFileChanged = false
        self.lastLeftSingleClickPlantIndex = 0
        self.lastRightSingleClickPlantIndex = 0
        self.leftOrRight = 0
        self.changedCurrentPlantFile = false
        self.commandList = PdCommandList()
        self.selectedPlants = TList()
        self.untitledDomainFileSavedAs = ""
        self.dragItemsY = 0
        self.justDoubleClickedOnLeftGrid = false
        self.justDoubleClickedOnRightGrid = false
    
    #$R *.DFM
    # -------------------------------------------------------------------------------------------- *creation/destruction 
    def create(self, AOwner):
        PdForm.create(self, AOwner)
        MoverForm = self
        self.leftManager = uplantmn.PdPlantManager().create()
        self.rightManager = uplantmn.PdPlantManager().create()
        self.commandList = ucommand.PdCommandList().create()
        self.selectedPlants = delphi_compatability.TList().Create()
        self.commandList.setNewUndoLimit(udomain.domain.options.undoLimit)
        self.commandList.setNewObjectUndoLimit(udomain.domain.options.undoLimitOfPlants)
        self.updateButtonsForUndoRedo()
        if len(udomain.domain.plantFileName) > 0:
            # load current plant file into left side to start 
            self.openPlantFileForManager(self.leftManager, udomain.domain.plantFileName)
        else:
            self.closePlantFileForManager(self.leftManager)
        # right side is empty to start 
        self.closePlantFileForManager(self.rightManager)
        self.updatePasteButtonForClipboardContents()
        return self
    
    def FormCreate(self, Sender):
        self.leftPlantList.DragCursor = ucursor.crDragPlant
        self.rightPlantList.DragCursor = ucursor.crDragPlant
    
    def destroy(self):
        self.leftManager.free
        self.leftManager = None
        self.rightManager.free
        self.rightManager = None
        self.selectedPlants.free
        self.selectedPlants = None
        self.commandList.free
        self.commandList = None
        PdForm.destroy(self)
    
    def FormClose(self, Sender, Action):
        if self.ModalResult == mrOK:
            return
        # same as exit, but can't call exit because we have to set the action flag 
        Action = delphi_compatability.TCloseAction.caNone
        if not self.askToSaveManagerAndProceed(self.leftManager):
            return
        if not self.askToSaveManagerAndProceed(self.rightManager):
            return
        Action = delphi_compatability.TCloseAction.caFree
    
    def FormKeyDown(self, Sender, Key, Shift):
        if Key == delphi_compatability.VK_DELETE:
            self.deleteClick(self)
        if not (delphi_compatability.TShiftStateEnum.ssCtrl in Shift):
            return Key
        if chr(Key) == "C":
            self.copyClick(self)
            Key = 0
        elif chr(Key) == "c":
            self.copyClick(self)
            Key = 0
        elif chr(Key) == "X":
            self.cutClick(self)
            Key = 0
        elif chr(Key) == "x":
            self.cutClick(self)
            Key = 0
        elif chr(Key) == "V":
            self.pasteClick(self)
            Key = 0
        elif chr(Key) == "v":
            self.pasteClick(self)
            Key = 0
        elif chr(Key) == "Z":
            if delphi_compatability.TShiftStateEnum.ssShift in Shift:
                self.redoClick(self)
            else:
                self.undoClick(self)
            Key = 0
        elif chr(Key) == "z":
            if delphi_compatability.TShiftStateEnum.ssShift in Shift:
                self.redoClick(self)
            else:
                self.undoClick(self)
            Key = 0
        return Key
    
    # ----------------------------------------------------------------------------------------- *buttons 
    def undoClick(self, Sender):
        self.commandList.undoLast()
        self.updateButtonsForUndoRedo()
        self.updateForChangeToSelectedPlants()
    
    def redoClick(self, Sender):
        self.commandList.redoLast()
        self.updateButtonsForUndoRedo()
        self.updateForChangeToSelectedPlants()
    
    def cutClick(self, Sender):
        manager = PdPlantManager()
        newCommand = PdCommand()
        
        manager = self.selectedManager(kThisManager)
        if (manager == None) or (self.selectedPlants.Count <= 0):
            return
        newCommand = PdMoverRemoveCommand().createWithListOfPlantsManagerAndClipboardFlag(self.selectedPlants, manager, updcom.kCopyToClipboard)
        self.doCommand(newCommand)
    
    def copyClick(self, Sender):
        self.copySelectedPlantsToClipboard()
    
    def pasteClick(self, Sender):
        manager = PdPlantManager()
        newCommand = PdCommand()
        newPlants = TList()
        
        manager = self.selectedManager(kThisManager)
        if manager == None:
            return
        newPlants = delphi_compatability.TList().Create()
        udomain.domain.plantManager.pastePlantsFromPrivatePlantClipboardToList(newPlants)
        newCommand = PdMoverPasteCommand().createWithListOfPlantsAndManager(newPlants, manager)
        self.doCommand(newCommand)
        #command has its own list, so we need to free this one
        newPlants.free
    
    def closeClick(self, Sender):
        if not self.askToSaveManagerAndProceed(self.leftManager):
            return
        if not self.askToSaveManagerAndProceed(self.rightManager):
            return
        # cannot cancel 
        self.ModalResult = mrOK
    
    def leftOpenCloseClick(self, Sender):
        if self.haveLeftFile():
            #file open
            #no file
            self.closePlantFileForManager(self.leftManager)
        else:
            self.openPlantFileForManager(self.leftManager, "")
    
    def rightOpenCloseClick(self, Sender):
        if self.haveRightFile():
            #file open
            #no file
            self.closePlantFileForManager(self.rightManager)
        else:
            self.openPlantFileForManager(self.rightManager, "")
    
    def newFileClick(self, Sender):
        self.newPlantFileForManager(self.rightManager)
    
    def transferClick(self, Sender):
        manager = PdPlantManager()
        otherManager = PdPlantManager()
        newCommand = PdCommand()
        newPlants = TList()
        plant = PdPlant()
        newPlant = PdPlant()
        i = 0
        
        manager = self.selectedManager(kThisManager)
        otherManager = self.selectedManager(kOtherManager)
        if (manager == None) or (otherManager == None) or (self.selectedPlants.Count <= 0):
            return
        if self.selectedPlants.Count > 0:
            #command will free
            newPlants = delphi_compatability.TList().Create()
            for i in range(0, self.selectedPlants.Count):
                plant = uplant.PdPlant(self.selectedPlants.Items[i])
                newPlant = uplant.PdPlant().create()
                plant.copyTo(newPlant)
                newPlants.Add(newPlant)
            newCommand = PdMoverPasteCommand().createWithListOfPlantsAndManager(newPlants, otherManager)
            (newCommand as PdMoverPasteCommand).isTransfer = true
            self.doCommand(newCommand)
            #command has its own list, so we need to free this one
            newPlants.free
    
    def duplicateClick(self, Sender):
        manager = PdPlantManager()
        newCommand = PdCommand()
        
        manager = self.selectedManager(kThisManager)
        if (manager == None) or (self.selectedPlants.Count <= 0):
            return
        newCommand = PdMoverDuplicateCommand().createWithListOfPlantsAndManager(self.selectedPlants, manager)
        self.doCommand(newCommand)
    
    def renameClick(self, Sender):
        plant = PdPlant()
        manager = PdPlantManager()
        newName = ansistring()
        newCommand = PdCommand()
        
        # can only rename one plant at a time 
        manager = self.selectedManager(kThisManager)
        plant = self.focusedPlant()
        if (plant == None) or (manager == None):
            return
        newName = plant.getName()
        if not InputQuery("Enter new name", "Type a new name for " + newName + ".", newName):
            return
        newCommand = PdMoverRenameCommand().createWithPlantNewNameAndManager(plant, newName, manager)
        self.doCommand(newCommand)
    
    def deleteClick(self, Sender):
        manager = PdPlantManager()
        newCommand = PdCommand()
        
        manager = self.selectedManager(kThisManager)
        if (manager == None) or (self.selectedPlants.Count <= 0):
            return
        newCommand = PdMoverRemoveCommand().createWithListOfPlantsManagerAndClipboardFlag(self.selectedPlants, manager, updcom.kDontCopyToClipboard)
        self.doCommand(newCommand)
    
    # -------------------------------------------------------------------------------------- *list box actions 
    def leftPlantListDrawCell(self, Sender, Col, Row, Rect, State):
        self.drawLineInGrid(self.leftPlantList, self.leftManager, Row, Rect, State)
    
    def rightPlantListDrawCell(self, Sender, Col, Row, Rect, State):
        self.drawLineInGrid(self.rightPlantList, self.rightManager, Row, Rect, State)
    
    def drawLineInGrid(self, grid, manager, index, rect, state):
        plant = PdPlant()
        selected = false
        cText = [0] * (range(0, 255 + 1) + 1)
        
        if delphi_compatability.Application.terminated:
            return
        grid.Canvas.Brush.Color = grid.Color
        grid.Canvas.FillRect(Rect)
        if (manager.plants.Count <= 0) or (index < 0) or (index > manager.plants.Count - 1):
            return
        # set up plant pointer 
        plant = uplant.PdPlant(manager.plants.Items[index])
        if plant == None:
            return
        selected = self.selectedPlants.IndexOf(plant) >= 0
        grid.Canvas.Font = grid.Font
        if selected:
            grid.Canvas.Brush.Color = UNRESOLVED.clHighlight
            grid.Canvas.Font.Color = UNRESOLVED.clHighlightText
        else:
            grid.Canvas.Brush.Color = grid.Color
            grid.Canvas.Font.Color = UNRESOLVED.clBtnText
        grid.Canvas.FillRect(Rect)
        UNRESOLVED.strPCopy(cText, plant.getName())
        # margin for text 
        Rect.left = Rect.left + 2
        UNRESOLVED.winprocs.drawText(grid.Canvas.Handle, cText, len(cText), Rect, delphi_compatability.DT_LEFT)
        if plant == self.focusedPlant():
            # put back 
            Rect.left = Rect.left - 2
            UNRESOLVED.drawFocusRect(Rect)
    
    # left list mouse handling
    def leftPlantListMouseDown(self, Sender, Button, Shift, X, Y):
        col = 0
        row = 0
        
        if self.justDoubleClickedOnLeftGrid:
            self.justDoubleClickedOnLeftGrid = false
            return
        else:
            self.justDoubleClickedOnLeftGrid = false
        if self.leftManager.plants.Count > 0:
            if self.leftOrRight == kRight:
                self.selectedPlants.Clear()
                self.lastRightSingleClickPlantIndex = -1
                self.rightPlantList.Invalidate()
            self.leftOrRight = kLeft
            col, row = self.leftPlantList.MouseToCell(X, Y, col, row)
            self.selectPlantAtIndex(Shift, row)
            self.updateForChangeToSelectedPlants()
            self.leftPlantList.BeginDrag(false)
    
    def leftPlantListDragOver(self, Sender, Source, X, Y, State, Accept):
        Accept = (Source != None) and (Sender != None)
        if Source == self.rightPlantList:
            Accept = Accept and self.haveLeftFile()
        else:
            Accept = Accept and (Source == Sender)
        return Accept
    
    def leftPlantListEndDrag(self, Sender, Target, X, Y):
        if (Target == self.rightPlantList):
            self.transferClick(self)
    
    def leftPlantListDblClick(self, Sender):
        self.renameClick(self)
        self.leftPlantList.endDrag(false)
        self.justDoubleClickedOnLeftGrid = true
    
    # right list mouse handling
    def rightPlantListMouseDown(self, Sender, Button, Shift, X, Y):
        col = 0
        row = 0
        
        if self.justDoubleClickedOnRightGrid:
            self.justDoubleClickedOnRightGrid = false
            return
        else:
            self.justDoubleClickedOnRightGrid = false
        if self.rightManager.plants.Count > 0:
            if self.leftOrRight == kLeft:
                self.selectedPlants.Clear()
                self.lastLeftSingleClickPlantIndex = -1
                self.leftPlantList.Invalidate()
            self.leftOrRight = kRight
            col, row = self.rightPlantList.MouseToCell(X, Y, col, row)
            self.selectPlantAtIndex(Shift, row)
            self.updateForChangeToSelectedPlants()
            self.rightPlantList.BeginDrag(false)
    
    def rightPlantListDragOver(self, Sender, Source, X, Y, State, Accept):
        Accept = (Source != None) and (Sender != None)
        if Source == self.leftPlantList:
            Accept = Accept and self.haveRightFile()
        else:
            Accept = Accept and (Source == Sender)
        return Accept
    
    def rightPlantListEndDrag(self, Sender, Target, X, Y):
        if (Target == self.leftPlantList):
            self.transferClick(self)
    
    def rightPlantListDblClick(self, Sender):
        self.renameClick(self)
        self.rightPlantList.endDrag(false)
        self.justDoubleClickedOnRightGrid = true
    
    def selectPlantAtIndex(self, Shift, index):
        i = 0
        plant = PdPlant()
        manager = PdPlantManager()
        lastSingleClickPlantIndex = 0
        lastRow = 0
        grid = TDrawGrid()
        
        if delphi_compatability.Application.terminated:
            return
        manager = self.selectedManager(kThisManager)
        if manager == None:
            return
        if (index < 0):
            self.selectedPlants.Clear()
            self.redrawSelectedGrid()
            return
        plant = uplant.PdPlant(manager.plants.Items[index])
        if plant == None:
            return
        if (delphi_compatability.TShiftStateEnum.ssCtrl in Shift):
            if self.selectedPlants.IndexOf(plant) >= 0:
                self.selectedPlants.Remove(plant)
            else:
                self.selectedPlants.Add(plant)
        elif (delphi_compatability.TShiftStateEnum.ssShift in Shift):
            if self.leftOrRight == kLeft:
                lastSingleClickPlantIndex = self.lastLeftSingleClickPlantIndex
            else:
                lastSingleClickPlantIndex = self.lastRightSingleClickPlantIndex
            if (lastSingleClickPlantIndex >= 0) and (lastSingleClickPlantIndex <= manager.plants.Count - 1) and (lastSingleClickPlantIndex != index):
                if lastSingleClickPlantIndex < index:
                    for i in range(lastSingleClickPlantIndex, index + 1):
                        if self.selectedPlants.IndexOf(manager.plants.Items[i]) < 0:
                            self.selectedPlants.Add(manager.plants.Items[i])
                elif lastSingleClickPlantIndex > index:
                    for i in range(lastSingleClickPlantIndex, index + 1):
                        if self.selectedPlants.IndexOf(manager.plants.Items[i]) < 0:
                            self.selectedPlants.Add(manager.plants.Items[i])
            # just a click
        else:
            if self.selectedPlants.IndexOf(plant) <= 0:
                self.selectedPlants.Clear()
                self.redrawSelectedGrid()
                self.selectedPlants.Add(plant)
                if self.leftOrRight == kLeft:
                    self.lastLeftSingleClickPlantIndex = index
                else:
                    self.lastRightSingleClickPlantIndex = index
                grid = self.gridForManager(manager)
                if grid == None:
                    return
                lastRow = grid.TopRow + grid.VisibleRowCount - 1
                if index > lastRow:
                    grid.TopRow = grid.TopRow + (index - lastRow)
                if index < grid.TopRow:
                    grid.TopRow = index
        self.redrawSelectedGrid()
    
    def leftPlantListKeyDown(self, Sender, Key, Shift):
        Key = self.listKeyDown(Key, Shift)
        return Key
    
    def rightPlantListKeyDown(self, Sender, Key, shift):
        Key = self.listKeyDown(Key, shift)
        return Key
    
    def listKeyDown(self, Key, Shift):
        if Key == delphi_compatability.VK_DOWN:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.moveSelectedPlantsDown()
            else:
                Key = 0
                self.moveUpOrDownWithKey(self.focusedPlantIndexInManager() + 1)
        elif Key == delphi_compatability.VK_RIGHT:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.moveSelectedPlantsDown()
            else:
                Key = 0
                self.moveUpOrDownWithKey(self.focusedPlantIndexInManager() + 1)
        elif Key == delphi_compatability.VK_UP:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.moveSelectedPlantsUp()
            else:
                Key = 0
                self.moveUpOrDownWithKey(self.focusedPlantIndexInManager() - 1)
        elif Key == delphi_compatability.VK_LEFT:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.moveSelectedPlantsUp()
            else:
                Key = 0
                self.moveUpOrDownWithKey(self.focusedPlantIndexInManager() - 1)
        elif Key == delphi_compatability.VK_RETURN:
            Key = 0
            self.renameClick(self)
        return Key
    
    def moveUpOrDownWithKey(self, indexAfterMove):
        manager = PdPlantManager()
        
        manager = self.selectedManager(kThisManager)
        if manager == None:
            return
        if indexAfterMove > manager.plants.Count - 1:
            # loop around 
            indexAfterMove = 0
        if indexAfterMove < 0:
            indexAfterMove = manager.plants.Count - 1
        if (indexAfterMove >= 0) and (indexAfterMove <= manager.plants.Count - 1):
            self.deselectAllPlants()
            #no shift
            self.selectPlantAtIndex([], indexAfterMove)
            self.drawPreview(self.focusedPlant())
    
    def moveSelectedPlantsDown(self):
        manager = PdPlantManager()
        i = 0
        plant = PdPlant()
        
        if self.selectedPlants.Count <= 0:
            return
        manager = self.selectedManager(kThisManager)
        if manager == None:
            return
        if manager.plants.Count > 1:
            # start at next to last one because you can't move last one down any more 
            i = manager.plants.Count - 2
            while i >= 0:
                plant = uplant.PdPlant(manager.plants.Items[i])
                if self.selectedPlants.IndexOf(plant) >= 0:
                    manager.plants.Move(i, i + 1)
                i -= 1
        self.redrawSelectedGrid()
        # reordering makes change flag true
        self.setChangedFlagForPlantManager(true, self.selectedManager(kThisManager))
    
    def moveSelectedPlantsUp(self):
        manager = PdPlantManager()
        i = 0
        plant = PdPlant()
        
        if self.selectedPlants.Count <= 0:
            return
        manager = self.selectedManager(kThisManager)
        if manager == None:
            return
        if manager.plants.Count > 1:
            # start at 1 because you can't move first one up any more 
            i = 1
            while i <= manager.plants.Count - 1:
                plant = uplant.PdPlant(manager.plants.Items[i])
                if self.selectedPlants.IndexOf(plant) >= 0:
                    manager.plants.Move(i, i - 1)
                i += 1
        self.redrawSelectedGrid()
        # reordering makes change flag true
        self.setChangedFlagForPlantManager(true, self.selectedManager(kThisManager))
    
    def redrawSelectedGrid(self):
        if self.leftOrRight == kLeft:
            self.leftPlantList.Invalidate()
        else:
            self.rightPlantList.Invalidate()
    
    # -------------------------------------------------------------------------------------------- *updating 
    def updateForNewFile(self, newFileName, manager):
        self.clearCommandList()
        self.setFileNameForManager(newFileName, manager)
        self.updatePlantListForManager(manager)
        self.setChangedFlagForPlantManager(false, manager)
        self.deselectAllPlants()
        if newFileName != "":
            if manager == self.leftManager:
                self.leftOrRight = kLeft
            else:
                self.leftOrRight = kRight
        self.updateForChangeToSelectedPlants()
    
    def deselectAllPlants(self):
        self.selectedPlants.Clear()
        self.redrawSelectedGrid()
    
    def updatePasteButtonForClipboardContents(self):
        self.paste.Enabled = (udomain.domain.plantManager.privatePlantClipboard.Count > 0)
    
    def leftRightString(self, leftString, rightString):
        result = ""
        if self.leftOrRight == kLeft:
            result = leftString
        else:
            result = rightString
        return result
    
    def updateForChangeToSelectedPlants(self):
        atLeastOnePlantSelected = false
        atLeastOneFile = false
        
        self.leftPlantList.Invalidate()
        self.rightPlantList.Invalidate()
        if self.leftOrRight == kLeft:
            if self.haveLeftFile():
                self.leftOpenClose.Caption = "&Close"
            else:
                self.leftOpenClose.Caption = "&Open..."
            self.leftPlantFileNameEdit.Color = delphi_compatability.clAqua
            self.leftPlantFileNameEdit.Refresh()
            self.rightPlantFileNameEdit.Color = UNRESOLVED.clBtnFace
            self.rightPlantFileNameEdit.Refresh()
            self.drawPreview(self.focusedPlant())
        else:
            if self.haveRightFile():
                self.rightOpenClose.Caption = "&Close"
            else:
                self.rightOpenClose.Caption = "&Open..."
            self.leftPlantFileNameEdit.Color = UNRESOLVED.clBtnFace
            self.leftPlantFileNameEdit.Refresh()
            self.rightPlantFileNameEdit.Color = delphi_compatability.clAqua
            self.rightPlantFileNameEdit.Refresh()
            self.drawPreview(self.focusedPlant())
        atLeastOneFile = self.haveLeftFile() or self.haveRightFile()
        atLeastOnePlantSelected = (self.selectedPlants.Count > 0)
        self.transfer.Enabled = self.haveLeftFile() and self.haveRightFile() and atLeastOnePlantSelected
        self.transfer.Caption = self.leftRightString("&Transfer >>", "<< &Transfer")
        self.cut.Enabled = atLeastOneFile and atLeastOnePlantSelected
        self.copy.Enabled = atLeastOneFile and atLeastOnePlantSelected
        self.duplicate.Enabled = atLeastOneFile and atLeastOnePlantSelected
        self.delete.Enabled = atLeastOneFile and atLeastOnePlantSelected
        self.rename.Enabled = atLeastOneFile and atLeastOnePlantSelected
    
    def updateButtonsForUndoRedo(self):
        if self.commandList.isUndoEnabled():
            self.undo.Enabled = true
            self.undo.Caption = "Undo " + self.commandList.undoDescription()
        else:
            self.undo.Enabled = false
            self.undo.Caption = "Can't undo"
        if self.commandList.isRedoEnabled():
            self.redo.Enabled = true
            self.redo.Caption = "Redo " + self.commandList.redoDescription()
        else:
            self.redo.Enabled = false
            self.redo.Caption = "Can't redo"
    
    def updatePlantListForManager(self, manager):
        grid = TDrawGrid()
        
        grid = self.gridForManager(manager)
        if grid == None:
            return
        grid.RowCount = manager.plants.Count
        grid.Invalidate()
    
    def drawPreview(self, plant):
        if plant == None:
            self.previewImage.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
            self.previewImage.Canvas.Brush.Color = delphi_compatability.clWindow
        else:
            if not plant.previewCacheUpToDate:
                try:
                    ucursor.cursor_startWait()
                    plant.drawPreviewIntoCache(Point(self.previewImage.Width, self.previewImage.Height), uplant.kDontConsiderDomainScale, umain.kDrawNow)
                finally:
                    ucursor.cursor_stopWait()
            plant.previewCache.Transparent = false
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(plant.previewCache, self.previewImage.Canvas, Rect(0, 0, 0, 0))
            UNRESOLVED.realizePalette(self.previewImage.Canvas.Handle)
            self.previewImage.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.previewImage.Canvas.Pen.Color = UNRESOLVED.clBtnText
        self.previewImage.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        self.previewImage.Canvas.Rectangle(0, 0, self.previewImage.Width, self.previewImage.Height)
    
    # ------------------------------------------------------------------------------------------ *selecting 
    def focusedPlant(self):
        result = PdPlant()
        result = None
        if self.selectedPlants.Count > 0:
            result = uplant.PdPlant(self.selectedPlants.Items[0])
        return result
    
    def focusedPlantIndexInManager(self):
        result = 0
        manager = PdPlantManager()
        
        result = -1
        manager = self.selectedManager(kThisManager)
        if manager == None:
            return result
        if self.selectedPlants.Count > 0:
            result = manager.plants.IndexOf(self.selectedPlants.Items[0])
        return result
    
    def haveLeftFile(self):
        result = false
        result = len(self.leftPlantFileName) != 0
        return result
    
    def haveRightFile(self):
        result = false
        result = len(self.rightPlantFileName) != 0
        return result
    
    def selectedManager(self, thisManager):
        result = PdPlantManager()
        result = None
        if self.leftOrRight == kLeft:
            if thisManager:
                result = self.leftManager
            else:
                result = self.rightManager
        else:
            if thisManager:
                result = self.rightManager
            else:
                result = self.leftManager
        return result
    
    def getFileNameForManager(self, manager):
        result = ""
        if manager == self.leftManager:
            result = self.leftPlantFileName
        else:
            result = self.rightPlantFileName
        return result
    
    def getFileNameForOtherManager(self, manager):
        result = ""
        if manager == self.rightManager:
            result = self.leftPlantFileName
        else:
            result = self.rightPlantFileName
        return result
    
    def setFileNameForManager(self, newName, manager):
        if manager == self.leftManager:
            self.leftPlantFileName = newName
            self.leftPlantFileNameEdit.Text = newName
            self.leftPlantFileNameEdit.SelStart = len(newName)
        else:
            self.rightPlantFileName = newName
            self.rightPlantFileNameEdit.Text = newName
            self.rightPlantFileNameEdit.SelStart = len(newName)
    
    def gridForManager(self, manager):
        result = TDrawGrid()
        result = None
        if manager == self.leftManager:
            result = self.leftPlantList
        elif manager == self.rightManager:
            result = self.rightPlantList
        return result
    
    def managerHasChanged(self, manager):
        result = false
        if manager == self.leftManager:
            result = self.leftPlantFileChanged
        else:
            result = self.rightPlantFileChanged
        return result
    
    def setChangedFlagForPlantManager(self, value, manager):
        if manager == self.leftManager:
            self.leftPlantFileChanged = value
            if self.leftPlantFileChanged:
                self.leftPlantFileChangedIndicator.Picture = umain.MainForm.fileChangedImage.Picture
            else:
                self.leftPlantFileChangedIndicator.Picture = umain.MainForm.fileNotChangedImage.Picture
        else:
            self.rightPlantFileChanged = value
            if self.rightPlantFileChanged:
                self.rightPlantFileChangedIndicator.Picture = umain.MainForm.fileChangedImage.Picture
            else:
                self.rightPlantFileChangedIndicator.Picture = umain.MainForm.fileNotChangedImage.Picture
    
    # ------------------------------------------------------------------------------------------- *copying 
    def copyPlantToPlantManager(self, plant, toPlantManager):
        result = PdPlant()
        if plant == None:
            result = None
        else:
            result = toPlantManager.copyFromPlant(plant)
        return result
    
    def copySelectedPlantsToClipboard(self):
        if self.selectedPlants.Count <= 0:
            return
        udomain.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(self.selectedPlants)
        self.updatePasteButtonForClipboardContents()
    
    # ------------------------------------------------------------------------ *opening, closing and saving 
    def openPlantFileForManager(self, manager, fileNameToStart):
        fileNameWithPath = ""
        
        if not self.askToSaveManagerAndProceed(manager):
            return
        if fileNameToStart == "":
            fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypePlant, usupport.kNoSuggestedFile, "Choose a plant file")
        else:
            fileNameWithPath = fileNameToStart
        if fileNameWithPath == "":
            self.updateForNewFile(fileNameWithPath, manager)
        else:
            if fileNameWithPath == self.getFileNameForOtherManager(manager):
                ShowMessage("The file you chose is already open on the other side.")
                return
            try:
                ucursor.cursor_startWait()
                if FileExists(fileNameWithPath):
                    manager.loadPlantsFromFile(fileNameWithPath, udomain.kInPlantMover)
                else:
                    self.newPlantFileForManager(manager)
                # PDF PORT -- added semicolon
                self.updateForNewFile(fileNameWithPath, manager)
            finally:
                ucursor.cursor_stopWait()
    
    def closePlantFileForManager(self, manager):
        if not self.askToSaveManagerAndProceed(manager):
            return
        manager.plants.clear()
        self.updateForNewFile("", manager)
    
    def newPlantFileForManager(self, manager):
        if not self.askToSaveManagerAndProceed(manager):
            return
        manager.plants.clear()
        self.updateForNewFile(kNewPlantFileName, manager)
    
    def managerSaveOrSaveAs(self, manager, askForFileName):
        fileInfo = SaveFileNamesStructure()
        fileName = ""
        askForFileNameConsideringUntitled = false
        
        fileName = self.getFileNameForManager(manager)
        if fileName == kNewPlantFileName:
            askForFileNameConsideringUntitled = true
        else:
            askForFileNameConsideringUntitled = askForFileName
        if not usupport.getFileSaveInfo(usupport.kFileTypePlant, askForFileNameConsideringUntitled, fileName, fileInfo):
            return
        try:
            ucursor.cursor_startWait()
            manager.savePlantsToFile(fileInfo.tempFile, udomain.kInPlantMover)
            fileInfo.writingWasSuccessful = true
        finally:
            ucursor.cursor_stopWait()
            usupport.cleanUpAfterFileSave(fileInfo)
            self.updateForNewFile(kNewPlantFileName, manager)
            if (fileInfo.newFile == udomain.domain.plantFileName):
                self.changedCurrentPlantFile = true
            if (fileName == kNewPlantFileName) and (udomain.domain.plantFileName == kNewPlantFileName):
                # deal with case of: started mover with untitled file, changed file, returned
                self.changedCurrentPlantFile = true
                self.untitledDomainFileSavedAs = fileInfo.newFile
    
    def askToSaveManagerAndProceed(self, manager):
        result = false
        response = 0
        prompt = ""
        
        # returns false if user cancelled action 
        result = true
        if not self.managerHasChanged(manager):
            return result
        prompt = "Save changes to " + ExtractFileName(self.getFileNameForManager(manager)) + "?"
        response = MessageDialog(prompt, mtConfirmation, mbYesNoCancel, 0)
        if response == mrYes:
            self.managerSaveOrSaveAs(manager, usupport.kDontAskForFileName)
        elif response == mrNo:
            result = true
        elif response == mrCancel:
            result = false
        return result
    
    # ------------------------------------------------------------------------------------------ *resizing 
    def FormResize(self, Sender):
        midWidth = 0
        listBoxWidth = 0
        listBoxTop = 0
        openCloseTop = 0
        
        if delphi_compatability.Application.terminated:
            return
        if self.leftManager == None:
            return
        if self.rightManager == None:
            return
        if self.selectedPlants == None:
            return
        midWidth = self.ClientWidth / 2
        #same as right
        listBoxWidth = self.leftPlantList.Width
        listBoxTop = kBetweenGap + self.leftPlantFileNameEdit.Height + kBetweenGap + self.leftOpenClose.Height + kBetweenGap
        # list boxes 
        self.leftPlantList.SetBounds(kBetweenGap, listBoxTop, listBoxWidth, umath.intMax(0, self.ClientHeight - listBoxTop - kBetweenGap))
        self.leftPlantList.DefaultColWidth = self.leftPlantList.ClientWidth
        self.rightPlantList.SetBounds(umath.intMax(0, self.ClientWidth - listBoxWidth - kBetweenGap), listBoxTop, listBoxWidth, umath.intMax(0, self.ClientHeight - listBoxTop - kBetweenGap))
        self.rightPlantList.DefaultColWidth = self.rightPlantList.ClientWidth
        # edits and buttons at top 
        self.leftPlantFileNameEdit.SetBounds(kBetweenGap, kBetweenGap, listBoxWidth - kBetweenGap * 2, self.leftPlantFileNameEdit.Height)
        self.leftPlantFileChangedIndicator.SetBounds(kBetweenGap, self.leftPlantFileNameEdit.Top + self.leftPlantFileNameEdit.Height + kBetweenGap, self.leftPlantFileChangedIndicator.Width, self.leftPlantFileChangedIndicator.Height)
        self.rightPlantFileNameEdit.SetBounds(self.rightPlantList.Left, kBetweenGap, listBoxWidth - kBetweenGap * 2, self.rightPlantFileNameEdit.Height)
        self.rightPlantFileChangedIndicator.SetBounds(self.rightPlantList.Left, self.rightPlantFileNameEdit.Top + self.rightPlantFileNameEdit.Height + kBetweenGap, self.rightPlantFileChangedIndicator.Width, self.rightPlantFileChangedIndicator.Height)
        openCloseTop = self.leftPlantFileNameEdit.Top + self.leftPlantFileNameEdit.Height + kBetweenGap
        self.leftOpenClose.SetBounds(self.leftPlantFileChangedIndicator.Left + self.leftPlantFileChangedIndicator.Width + kBetweenGap, openCloseTop, self.leftOpenClose.Width, self.leftOpenClose.Height)
        self.rightOpenClose.SetBounds(self.rightPlantFileChangedIndicator.Left + self.rightPlantFileChangedIndicator.Width + kBetweenGap, openCloseTop, self.rightOpenClose.Width, self.rightOpenClose.Height)
        self.newFile.SetBounds(self.rightOpenClose.Left + self.rightOpenClose.Width + kBetweenGap, openCloseTop, self.newFile.Width, self.newFile.Height)
        # buttons in middle 
        self.close.SetBounds(midWidth - self.close.Width / 2, umath.intMax(0, self.ClientHeight - self.close.Height - kBetweenGap), self.close.Width, self.close.Height)
        self.helpButton.SetBounds(self.close.Left, umath.intMax(0, self.close.Top - self.helpButton.Height - kBetweenGap), self.helpButton.Width, self.helpButton.Height)
        self.redo.SetBounds(self.close.Left, umath.intMax(0, self.helpButton.Top - self.redo.Height - kBetweenGap), self.redo.Width, self.redo.Height)
        self.undo.SetBounds(self.close.Left, umath.intMax(0, self.redo.Top - self.undo.Height - kBetweenGap), self.undo.Width, self.undo.Height)
        self.rename.SetBounds(self.close.Left, umath.intMax(0, self.undo.Top - self.rename.Height - kBetweenGap), self.rename.Width, self.rename.Height)
        self.delete.SetBounds(self.close.Left, umath.intMax(0, self.rename.Top - self.delete.Height - kBetweenGap), self.delete.Width, self.delete.Height)
        self.duplicate.SetBounds(self.close.Left, umath.intMax(0, self.delete.Top - self.duplicate.Height - kBetweenGap), self.duplicate.Width, self.duplicate.Height)
        self.paste.SetBounds(self.close.Left, umath.intMax(0, self.duplicate.Top - self.paste.Height - kBetweenGap), self.paste.Width, self.paste.Height)
        self.copy.SetBounds(self.close.Left, umath.intMax(0, self.paste.Top - self.copy.Height - kBetweenGap), self.copy.Width, self.copy.Height)
        self.cut.SetBounds(self.close.Left, umath.intMax(0, self.copy.Top - self.cut.Height - kBetweenGap), self.cut.Width, self.cut.Height)
        self.transfer.SetBounds(self.close.Left, umath.intMax(0, self.cut.Top - self.transfer.Height - kBetweenGap), self.transfer.Width, self.transfer.Height)
        self.previewImage.SetBounds(listBoxWidth + kBetweenGap * 2, kBetweenGap, umath.intMax(0, self.ClientWidth - listBoxWidth * 2 - kBetweenGap * 4), self.transfer.Top - kBetweenGap * 2)
        self.resizePreviewImage()
    
    def resizePreviewImage(self):
        i = 0
        manager = PdPlantManager()
        
        try:
            self.previewImage.Picture.Bitmap.Height = self.previewImage.Height
            self.previewImage.Picture.Bitmap.Width = self.previewImage.Width
        except:
            self.previewImage.Picture.Bitmap.Height = 1
            self.previewImage.Picture.Bitmap.Width = 1
        # must invalidate preview cache for both sets of plants
        manager = self.selectedManager(kThisManager)
        if manager.plants.Count > 0:
            for i in range(0, manager.plants.Count):
                uplant.PdPlant(manager.plants.Items[i]).previewCacheUpToDate = false
        manager = self.selectedManager(kOtherManager)
        if manager.plants.Count > 0:
            for i in range(0, manager.plants.Count):
                uplant.PdPlant(manager.plants.Items[i]).previewCacheUpToDate = false
        self.drawPreview(self.focusedPlant())
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 400
        UNRESOLVED.ptMinTrackSize.y = 420
    
    # ----------------------------------------------------------------------------------------- command list 
    def clearCommandList(self):
        self.commandList.free
        self.commandList = None
        self.commandList = ucommand.PdCommandList().create()
        self.updateButtonsForUndoRedo()
    
    def doCommand(self, command):
        self.commandList.doCommand(command)
        self.updateButtonsForUndoRedo()
        self.updateForChangeToSelectedPlants()
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Using_the_plant_mover")
    
class PdMoverRenameCommand(PdCommand):
    def __init__(self):
        self.plant = PdPlant()
        self.oldName = ""
        self.newName = ""
        self.manager = PdPlantManager()
        self.managerChangedBeforeCommand = false
    
    # ------------------------------------------------------------------------------ *commands 
    # ------------------------------------------------------------------- PdMoverRenameCommand 
    def createWithPlantNewNameAndManager(self, aPlant, aNewName, aManager):
        PdCommand.create(self)
        self.commandChangesPlantFile = false
        self.plant = aPlant
        self.oldName = self.plant.getName()
        self.newName = aNewName
        self.manager = aManager
        self.managerChangedBeforeCommand = MoverForm.managerHasChanged(self.manager)
        return self
    
    def doCommand(self):
        #not redo
        PdCommand.doCommand(self)
        self.plant.setName(self.newName)
        MoverForm.setChangedFlagForPlantManager(true, self.manager)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        self.plant.setName(self.oldName)
        MoverForm.setChangedFlagForPlantManager(self.managerChangedBeforeCommand, self.manager)
    
    def description(self):
        result = ""
        result = "rename"
        return result
    
#use for cut and delete
class PdMoverRemoveCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.removedPlants = TList()
        self.copyToClipboard = false
        self.manager = PdPlantManager()
        self.managerChangedBeforeCommand = false
    
    # ----------------------------------------------------------------------- PdMoverRemoveCommand 
    def createWithListOfPlantsManagerAndClipboardFlag(self, aList, aManager, aCopyToClipboard):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.commandChangesPlantFile = false
        self.manager = aManager
        self.managerChangedBeforeCommand = MoverForm.managerHasChanged(self.manager)
        self.copyToClipboard = aCopyToClipboard
        self.removedPlants = delphi_compatability.TList().Create()
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
    
    def doCommand(self):
        i = 0
        
        #not redo
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count <= 0:
            return
        if self.copyToClipboard:
            # copy plants 
            MoverForm.copySelectedPlantsToClipboard()
        # save copy of plants before deleting 
        self.removedPlants.Clear()
        for i in range(0, self.plantList.Count):
            # don't remove plants from manager until all indexes have been recorded 
            self.plant = uplant.PdPlant(self.plantList.Items[i])
            self.removedPlants.Add(self.plant)
            self.plant.indexWhenRemoved = self.manager.plants.IndexOf(self.plant)
            self.plant.selectedIndexWhenRemoved = MoverForm.selectedPlants.IndexOf(self.plant)
        for i in range(0, self.plantList.Count):
            self.manager.plants.Remove(uplant.PdPlant(self.plantList.Items[i]))
        for i in range(0, self.plantList.Count):
            MoverForm.selectedPlants.Remove(uplant.PdPlant(self.plantList.Items[i]))
        MoverForm.updatePlantListForManager(self.manager)
        MoverForm.setChangedFlagForPlantManager(true, self.manager)
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        if self.removedPlants.Count > 0:
            for i in range(0, self.removedPlants.Count):
                self.plant = uplant.PdPlant(self.removedPlants.Items[i])
                if (self.plant.indexWhenRemoved >= 0) and (self.plant.indexWhenRemoved <= self.manager.plants.Count - 1):
                    self.manager.plants.Insert(self.plant.indexWhenRemoved, self.plant)
                else:
                    self.manager.plants.Add(self.plant)
                if (self.plant.selectedIndexWhenRemoved >= 0) and (self.plant.selectedIndexWhenRemoved <= MoverForm.selectedPlants.Count - 1):
                    # all removed plants must have been selected, so also add them to the selected list 
                    MoverForm.selectedPlants.Insert(self.plant.selectedIndexWhenRemoved, self.plant)
                else:
                    MoverForm.selectedPlants.Add(self.plant)
            MoverForm.updatePlantListForManager(self.manager)
            MoverForm.setChangedFlagForPlantManager(self.managerChangedBeforeCommand, self.manager)
    
    def description(self):
        result = ""
        if self.copyToClipboard:
            result = "cut"
        else:
            result = "delete"
        return result
    
#use for transfer and paste
class PdMoverPasteCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.isTransfer = false
        self.manager = PdPlantManager()
        self.managerChangedBeforeCommand = false
    
    # ------------------------------------------------------------------ PdMoverPasteCommand 
    def createWithListOfPlantsAndManager(self, aList, aManager):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.commandChangesPlantFile = false
        self.manager = aManager
        self.managerChangedBeforeCommand = MoverForm.managerHasChanged(self.manager)
        return self
    
    def destroy(self):
        i = 0
        
        if (not self.done) and (self.plantList != None) and (self.plantList.Count > 0):
            for i in range(0, self.plantList.Count):
                # free copies of pasted plants if change was undone 
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.plant.free
        #will free plantList
        PdCommandWithListOfPlants.destroy(self)
    
    def doCommand(self):
        i = 0
        
        #not redo
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count > 0:
            MoverForm.deselectAllPlants()
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.manager.plants.Add(self.plant)
                MoverForm.selectedPlants.Add(self.plant)
            MoverForm.updatePlantListForManager(self.manager)
            MoverForm.setChangedFlagForPlantManager(true, self.manager)
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        if self.plantList.Count > 0:
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                self.manager.plants.Remove(self.plant)
                MoverForm.selectedPlants.Remove(self.plant)
            MoverForm.updatePlantListForManager(self.manager)
            MoverForm.setChangedFlagForPlantManager(self.managerChangedBeforeCommand, self.manager)
    
    def description(self):
        result = ""
        if self.isTransfer:
            result = "transfer"
        else:
            result = "paste"
        return result
    
class PdMoverDuplicateCommand(PdCommandWithListOfPlants):
    def __init__(self):
        self.newPlants = TList()
        self.manager = PdPlantManager()
        self.managerChangedBeforeCommand = false
    
    # ------------------------------------------------------------------------------ PdMoverDuplicateCommand 
    def createWithListOfPlantsAndManager(self, aList, aManager):
        PdCommandWithListOfPlants.createWithListOfPlants(self, aList)
        self.commandChangesPlantFile = false
        self.newPlants = delphi_compatability.TList().Create()
        self.manager = aManager
        self.managerChangedBeforeCommand = MoverForm.managerHasChanged(self.manager)
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
    
    def doCommand(self):
        i = 0
        plantCopy = PdPlant()
        
        PdCommandWithListOfPlants.doCommand(self)
        if self.plantList.Count > 0:
            MoverForm.deselectAllPlants()
            for i in range(0, self.plantList.Count):
                self.plant = uplant.PdPlant(self.plantList.Items[i])
                plantCopy = uplant.PdPlant().create()
                self.plant.copyTo(plantCopy)
                plantCopy.setName("Copy of " + plantCopy.getName())
                self.newPlants.Add(plantCopy)
                self.manager.plants.Add(plantCopy)
                MoverForm.selectedPlants.Add(plantCopy)
            MoverForm.updatePlantListForManager(self.manager)
            MoverForm.setChangedFlagForPlantManager(true, self.manager)
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfPlants.undoCommand(self)
        if self.newPlants.Count > 0:
            for i in range(0, self.newPlants.Count):
                self.plant = uplant.PdPlant(self.newPlants.Items[i])
                self.manager.plants.Remove(self.plant)
                MoverForm.selectedPlants.Remove(self.plant)
            MoverForm.updatePlantListForManager(self.manager)
            MoverForm.setChangedFlagForPlantManager(self.managerChangedBeforeCommand, self.manager)
    
    def redoCommand(self):
        i = 0
        
        #not redo
        PdCommandWithListOfPlants.doCommand(self)
        if self.newPlants.Count > 0:
            MoverForm.deselectAllPlants()
            for i in range(0, self.newPlants.Count):
                self.plant = uplant.PdPlant(self.newPlants.Items[i])
                self.manager.plants.Add(self.plant)
                MoverForm.selectedPlants.Add(self.plant)
            MoverForm.updatePlantListForManager(self.manager)
            MoverForm.setChangedFlagForPlantManager(true, self.manager)
    
    def description(self):
        result = ""
        result = "duplicate"
        return result
    
# tried this - big mess
#procedure TMoverForm.drawDragItemLine(listBox: TListBox; y: integer);
#  begin
#  if listBox = leftPlantList then
#    begin
#    leftDragItemLastDrawY := y;
#    self.drawOrUndrawDragItemLine(listBox, y);
#    self.leftDragItemLineNeedToRedraw := true;
#    end
#  else
#    begin
#    rightDragItemLastDrawY := y;
#    self.drawOrUndrawDragItemLine(listBox, y);
#    self.rightDragItemLineNeedToRedraw := true;
#    end;
#  end;
#
#procedure TMoverForm.undrawDragItemLine(listBox: TListBox);
#  begin
#  if listBox = leftPlantList then
#    begin
#    if not leftDragItemLineNeedToRedraw then exit;
#    self.drawOrUndrawDragItemLine(listBox, leftDragItemLastDrawY);
#    self.leftDragItemLineNeedToRedraw := false;
#    end
#  else
#    begin
#    if not rightDragItemLineNeedToRedraw then exit;
#    self.drawOrUndrawDragItemLine(listBox, rightDragItemLastDrawY);
#    self.rightDragItemLineNeedToRedraw := false;
#    end;
#  end;
#
#procedure TMoverForm.drawOrUndrawDragItemLine(listBox: TListBox; y: integer);
#  var
#    theDC: HDC;
#    drawRect: TRect;
#  begin
#  theDC := getDC(0);
#  with drawRect do
#    begin
#    left := self.clientOrigin.x + listBox.left;
#    right := self.clientOrigin.x + listBox.left + listBox.width;
#    top := self.clientOrigin.y + listBox.top + y;
#    end;
#  with drawRect do
#    patBlt(theDC, left, top, right - left, 1, dstInvert);
#  releaseDC(0, theDC);
#  end;
#
#{ -------------------------------------------------------------------------------------------- *up and down }
#procedure TMoverForm.moveItemsUpOrDown(listBox: TListBox; y: integer);
#  var
#    rows, i: integer;
#  begin
#  if self.dragItemsY <> 0 then
#    begin
#    rows := abs(y - self.dragItemsY) div listBox.itemHeight;
#    if rows > 0 then
#      begin
#      if (y - self.dragItemsY) > 0 then
#        for i := 0 to rows - 1 do self.moveItemsDown(listBox)
#      else
#        for i := 0 to rows - 1 do self.moveItemsUp(listBox);
#      end;
#    self.dragItemsY := y;
#    end;
#  end;
#
#procedure TMoverForm.moveItemsDown(listBox: TListBox);
#  var
#    i: integer;
#  begin
#  if listBox.items.count > 1 then
#    begin
#    i := listBox.items.count - 2;  { start at next to last one because you can't move last one down any more }
#    while i >= 0 do
#      begin
#      if listBox.selected[i] then
#        begin
#        listBox.items.move(i, i + 1);
#        listBox.selected[i+1] := true;
#        end;
#      dec(i);
#      end;
#    end;
#  end;
#
#procedure TMoverForm.moveItemsUp(listBox: TListBox);
#  var
#    i: integer;
#  begin
#  if listBox.items.count > 1 then
#    begin
#    i := 1;  { start at 1 because you can't move first one up any more }
#    while i <= listBox.items.count - 1 do
#      begin
#      if listBox.selected[i] then
#        begin
#        listBox.items.move(i, i - 1);
#        listBox.selected[i-1] := true;
#        end;
#      inc(i);
#      end;
#    end;
#  end;
#
#
