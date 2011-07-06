# unit utdomove

from conversion_common import *
import utdoedit
import uturtle
import umath
import usupport
import ucursor
import umain
import udomain
import ucollect
import updform
import updcom
import ucommand
import utdo
import uplantmn
import delphi_compatability

# const
kLeft = 0
kRight = 1
kNewTdoFileName = "untitled.tdo"
kThisList = true
kOtherList = false

# var
TdoMoverForm = TTdoMoverForm()

# const
kBetweenGap = 4

class TTdoMoverForm(PdForm):
    def __init__(self):
        self.leftTdoFileNameEdit = TEdit()
        self.leftOpenClose = TButton()
        self.rightTdoFileNameEdit = TEdit()
        self.rightOpenClose = TButton()
        self.newFile = TButton()
        self.transfer = TButton()
        self.close = TButton()
        self.previewImage = TImage()
        self.undo = TButton()
        self.redo = TButton()
        self.rename = TButton()
        self.duplicate = TButton()
        self.delete = TButton()
        self.leftTdoFileChangedIndicator = TImage()
        self.rightTdoFileChangedIndicator = TImage()
        self.leftTdoList = TDrawGrid()
        self.rightTdoList = TDrawGrid()
        self.editTdo = TButton()
        self.helpButton = TSpeedButton()
        self.leftTdoFileName = ""
        self.rightTdoFileName = ""
        self.leftList = TListCollection()
        self.rightList = TListCollection()
        self.leftTdoFileChanged = false
        self.rightTdoFileChanged = false
        self.lastLeftSingleClickTdoIndex = 0
        self.lastRightSingleClickTdoIndex = 0
        self.leftOrRight = 0
        self.commandList = PdCommandList()
        self.selectedTdos = TList()
        self.dragItemsY = 0
        self.justDoubleClickedOnLeftGrid = false
        self.justDoubleClickedOnRightGrid = false
    
    #$R *.DFM
    # -------------------------------------------------------------------------------------------- *creation/destruction 
    def create(self, AOwner):
        PdForm.create(self, AOwner)
        TdoMoverForm = self
        self.leftList = ucollect.TListCollection().Create()
        self.rightList = ucollect.TListCollection().Create()
        self.commandList = ucommand.PdCommandList().create()
        self.selectedTdos = delphi_compatability.TList().Create()
        self.commandList.setNewUndoLimit(udomain.domain.options.undoLimit)
        self.commandList.setNewObjectUndoLimit(udomain.domain.options.undoLimitOfPlants)
        self.updateButtonsForUndoRedo()
        if len(udomain.domain.defaultTdoLibraryFileName) > 0:
            # load current tdo file into left side to start 
            self.openTdoFileForList(self.leftList, udomain.domain.defaultTdoLibraryFileName)
        else:
            self.closeTdoFileForList(self.leftList)
        # right side is empty to start 
        self.closeTdoFileForList(self.rightList)
        return self
    
    def FormCreate(self, Sender):
        self.leftTdoList.DragCursor = ucursor.crDragTdo
        self.rightTdoList.DragCursor = ucursor.crDragTdo
    
    def destroy(self):
        self.leftList.free
        self.leftList = None
        self.rightList.free
        self.rightList = None
        self.selectedTdos.free
        self.selectedTdos = None
        self.commandList.free
        self.commandList = None
        PdForm.destroy(self)
    
    def FormClose(self, Sender, Action):
        if self.ModalResult == mrOK:
            return
        # same as exit, but can't call exit because we have to set the action flag 
        Action = delphi_compatability.TCloseAction.caNone
        if not self.askToSaveListAndProceed(self.leftList):
            return
        if not self.askToSaveListAndProceed(self.rightList):
            return
        Action = delphi_compatability.TCloseAction.caFree
    
    def FormKeyDown(self, Sender, Key, Shift):
        if Key == delphi_compatability.VK_DELETE:
            self.deleteClick(self)
        if not (delphi_compatability.TShiftStateEnum.ssCtrl in Shift):
            return Key
        if chr(Key) == "Z":
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
        self.updateForChangeToSelectedTdos()
    
    def redoClick(self, Sender):
        self.commandList.redoLast()
        self.updateButtonsForUndoRedo()
        self.updateForChangeToSelectedTdos()
    
    def closeClick(self, Sender):
        if not self.askToSaveListAndProceed(self.leftList):
            return
        if not self.askToSaveListAndProceed(self.rightList):
            return
        # cannot cancel 
        self.ModalResult = mrOK
    
    def leftOpenCloseClick(self, Sender):
        if self.haveLeftFile():
            #file open
            #no file
            self.closeTdoFileForList(self.leftList)
        else:
            self.openTdoFileForList(self.leftList, "")
    
    def rightOpenCloseClick(self, Sender):
        if self.haveRightFile():
            #file open
            #no file
            self.closeTdoFileForList(self.rightList)
        else:
            self.openTdoFileForList(self.rightList, "")
    
    def newFileClick(self, Sender):
        self.newTdoFileForList(self.rightList)
    
    def transferClick(self, Sender):
        list = TListCollection()
        otherList = TListCollection()
        newCommand = PdCommand()
        newTdos = TList()
        tdo = KfObject3D()
        newTdo = KfObject3D()
        i = 0
        
        list = self.selectedList(kThisList)
        otherList = self.selectedList(kOtherList)
        if (list == None) or (otherList == None) or (self.selectedTdos.Count <= 0):
            return
        if self.selectedTdos.Count > 0:
            #command will free
            newTdos = delphi_compatability.TList().Create()
            for i in range(0, self.selectedTdos.Count):
                tdo = utdo.KfObject3D(self.selectedTdos.Items[i])
                newTdo = utdo.KfObject3D().create()
                tdo.copyTo(newTdo)
                newTdos.Add(newTdo)
            newCommand = PdTdoMoverTransferCommand().createWithSelectedTdosAndList(newTdos, otherList)
            self.doCommand(newCommand)
            #command has its own list, so we need to free this one
            newTdos.free
    
    def duplicateClick(self, Sender):
        list = TListCollection()
        newCommand = PdCommand()
        
        list = self.selectedList(kThisList)
        if (list == None) or (self.selectedTdos.Count <= 0):
            return
        newCommand = PdTdoMoverDuplicateCommand().createWithSelectedTdosAndList(self.selectedTdos, list)
        self.doCommand(newCommand)
    
    def renameClick(self, Sender):
        tdo = KfObject3D()
        list = TListCollection()
        newName = ansistring()
        newCommand = PdCommand()
        
        # can only rename one tdo at a time 
        list = self.selectedList(kThisList)
        tdo = self.focusedTdo()
        if (tdo == None) or (list == None):
            return
        newName = tdo.getName()
        if not InputQuery("Enter new name", "Type a new name for " + newName + ".", newName):
            return
        newCommand = PdTdoMoverRenameCommand().createWithTdoNewNameAndList(tdo, newName, list)
        self.doCommand(newCommand)
    
    def deleteClick(self, Sender):
        list = TListCollection()
        newCommand = PdCommand()
        
        list = self.selectedList(kThisList)
        if (list == None) or (self.selectedTdos.Count <= 0):
            return
        newCommand = PdTdoMoverRemoveCommand().createWithSelectedTdosAndList(self.selectedTdos, list)
        self.doCommand(newCommand)
    
    def editTdoClick(self, Sender):
        tdoEditorForm = TTdoEditorForm()
        response = 0
        newCommand = PdCommand()
        tempTdo = KfObject3D()
        
        if self.focusedTdo() == None:
            return
        tdoEditorForm = utdoedit.TTdoEditorForm().create(self)
        if tdoEditorForm == None:
            raise GeneralException.create("Problem: Could not create 3D object editor window.")
        tempTdo = utdo.KfObject3D().create()
        try:
            tempTdo.copyFrom(self.focusedTdo())
            tdoEditorForm.initializeWithTdo(tempTdo)
            response = tdoEditorForm.ShowModal()
            if response == mrOK:
                # v1.6b1
                tempTdo.copyFrom(tdoEditorForm.tdo)
                newCommand = PdTdoMoverEditCommand().createWithTdoNewTdoAndList(self.focusedTdo(), tempTdo, self.selectedList(kThisList))
                self.doCommand(newCommand)
        finally:
            tdoEditorForm.free
            tdoEditorForm = None
            tempTdo.free
            tempTdo = None
    
    def sortListClick(self, Sender):
        pass
    
    # -------------------------------------------------------------------------------------- *list box actions 
    def leftTdoListDrawCell(self, Sender, Col, Row, Rect, State):
        self.drawLineInGrid(self.leftTdoList, self.leftList, Row, Rect, State)
    
    def rightTdoListDrawCell(self, Sender, Col, Row, Rect, State):
        self.drawLineInGrid(self.rightTdoList, self.rightList, Row, Rect, State)
    
    def drawLineInGrid(self, grid, list, index, rect, state):
        tdo = KfObject3D()
        selected = false
        cText = [0] * (range(0, 255 + 1) + 1)
        
        if delphi_compatability.Application.terminated:
            return
        grid.Canvas.Brush.Color = grid.Color
        grid.Canvas.FillRect(Rect)
        if (list.Count <= 0) or (index < 0) or (index > list.Count - 1):
            return
        # set up tdo pointer 
        tdo = utdo.KfObject3D(list.Items[index])
        if tdo == None:
            return
        selected = (list == self.selectedList(kThisList)) and (self.selectedTdos.IndexOf(tdo) >= 0)
        grid.Canvas.Font = grid.Font
        if selected:
            grid.Canvas.Brush.Color = UNRESOLVED.clHighlight
            grid.Canvas.Font.Color = UNRESOLVED.clHighlightText
        else:
            grid.Canvas.Brush.Color = grid.Color
            grid.Canvas.Font.Color = UNRESOLVED.clBtnText
        grid.Canvas.FillRect(Rect)
        UNRESOLVED.strPCopy(cText, tdo.getName())
        # margin for text 
        Rect.left = Rect.left + 2
        UNRESOLVED.winprocs.drawText(grid.Canvas.Handle, cText, len(cText), Rect, delphi_compatability.DT_LEFT)
        if tdo == self.focusedTdo():
            # put back 
            Rect.left = Rect.left - 2
            UNRESOLVED.drawFocusRect(Rect)
    
    # left list mouse handling
    def leftTdoListMouseDown(self, Sender, Button, Shift, X, Y):
        col = 0
        row = 0
        
        if self.justDoubleClickedOnLeftGrid:
            self.justDoubleClickedOnLeftGrid = false
            return
        else:
            self.justDoubleClickedOnLeftGrid = false
        if self.leftList.Count > 0:
            if self.leftOrRight == kRight:
                self.selectedTdos.Clear()
                self.lastRightSingleClickTdoIndex = -1
                self.rightTdoList.Invalidate()
            self.leftOrRight = kLeft
            col, row = self.leftTdoList.MouseToCell(X, Y, col, row)
            self.selectTdoAtIndex(Shift, row)
            self.leftTdoList.Invalidate()
            self.updateForChangeToSelectedTdos()
            self.leftTdoList.BeginDrag(false)
    
    def leftTdoListDragOver(self, Sender, Source, X, Y, State, Accept):
        Accept = (Source != None) and (Sender != None)
        if Source == self.rightTdoList:
            Accept = Accept and self.haveLeftFile()
        else:
            Accept = Accept and (Source == Sender)
        return Accept
    
    def leftTdoListEndDrag(self, Sender, Target, X, Y):
        if (Target == self.rightTdoList):
            self.transferClick(self)
    
    def leftTdoListDblClick(self, Sender):
        self.renameClick(self)
        self.leftTdoList.endDrag(false)
        self.justDoubleClickedOnLeftGrid = true
    
    # right list mouse handling
    def rightTdoListMouseDown(self, Sender, Button, Shift, X, Y):
        col = 0
        row = 0
        
        if self.justDoubleClickedOnRightGrid:
            self.justDoubleClickedOnRightGrid = false
            return
        else:
            self.justDoubleClickedOnRightGrid = false
        if self.rightList.Count > 0:
            if self.leftOrRight == kLeft:
                self.selectedTdos.Clear()
                self.lastLeftSingleClickTdoIndex = -1
                self.leftTdoList.Invalidate()
            self.leftOrRight = kRight
            col, row = self.rightTdoList.MouseToCell(X, Y, col, row)
            self.selectTdoAtIndex(Shift, row)
            self.rightTdoList.Invalidate()
            self.updateForChangeToSelectedTdos()
            self.rightTdoList.BeginDrag(false)
    
    def rightTdoListDragOver(self, Sender, Source, X, Y, State, Accept):
        Accept = (Source != None) and (Sender != None)
        if Source == self.leftTdoList:
            Accept = Accept and self.haveRightFile()
        else:
            Accept = Accept and (Source == Sender)
        return Accept
    
    def rightTdoListEndDrag(self, Sender, Target, X, Y):
        if (Target == self.leftTdoList):
            self.transferClick(self)
    
    def rightTdoListDblClick(self, Sender):
        self.renameClick(self)
        self.rightTdoList.endDrag(false)
        self.justDoubleClickedOnRightGrid = true
    
    def selectTdoAtIndex(self, Shift, index):
        i = 0
        tdo = KfObject3D()
        list = TListCollection()
        lastSingleClickTdoIndex = 0
        lastRow = 0
        grid = TDrawGrid()
        
        if delphi_compatability.Application.terminated:
            return
        list = self.selectedList(kThisList)
        if list == None:
            return
        if (index < 0):
            self.selectedTdos.Clear()
            return
        tdo = utdo.KfObject3D(list.Items[index])
        if tdo == None:
            return
        if (delphi_compatability.TShiftStateEnum.ssCtrl in Shift):
            if self.selectedTdos.IndexOf(tdo) >= 0:
                self.selectedTdos.Remove(tdo)
            else:
                self.selectedTdos.Add(tdo)
        elif (delphi_compatability.TShiftStateEnum.ssShift in Shift):
            if self.leftOrRight == kLeft:
                lastSingleClickTdoIndex = self.lastLeftSingleClickTdoIndex
            else:
                lastSingleClickTdoIndex = self.lastRightSingleClickTdoIndex
            if (lastSingleClickTdoIndex >= 0) and (lastSingleClickTdoIndex <= list.Count - 1) and (lastSingleClickTdoIndex != index):
                if lastSingleClickTdoIndex < index:
                    for i in range(lastSingleClickTdoIndex, index + 1):
                        if self.selectedTdos.IndexOf(list.Items[i]) < 0:
                            self.selectedTdos.Add(list.Items[i])
                elif lastSingleClickTdoIndex > index:
                    for i in range(lastSingleClickTdoIndex, index + 1):
                        if self.selectedTdos.IndexOf(list.Items[i]) < 0:
                            self.selectedTdos.Add(list.Items[i])
            # just a click
        else:
            if self.selectedTdos.IndexOf(tdo) <= 0:
                self.selectedTdos.Clear()
                self.selectedTdos.Add(tdo)
                if self.leftOrRight == kLeft:
                    self.lastLeftSingleClickTdoIndex = index
                else:
                    self.lastRightSingleClickTdoIndex = index
            grid = self.gridForList(list)
            if grid == None:
                return
            lastRow = grid.TopRow + grid.VisibleRowCount - 1
            if index > lastRow:
                grid.TopRow = grid.TopRow + (index - lastRow)
            if index < grid.TopRow:
                grid.TopRow = index
    
    def leftTdoListKeyDown(self, Sender, Key, Shift):
        Key = self.listKeyDown(Key, Shift)
        return Key
    
    def rightTdoListKeyDown(self, Sender, Key, Shift):
        Key = self.listKeyDown(Key, Shift)
        return Key
    
    def listKeyDown(self, Key, Shift):
        if Key == delphi_compatability.VK_DOWN:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.moveSelectedTdosDown()
            else:
                Key = 0
                self.moveUpOrDownWithKey(self.focusedTdoIndexInList() + 1)
        elif Key == delphi_compatability.VK_RIGHT:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.moveSelectedTdosDown()
            else:
                Key = 0
                self.moveUpOrDownWithKey(self.focusedTdoIndexInList() + 1)
        elif Key == delphi_compatability.VK_UP:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.moveSelectedTdosUp()
            else:
                Key = 0
                self.moveUpOrDownWithKey(self.focusedTdoIndexInList() - 1)
        elif Key == delphi_compatability.VK_LEFT:
            if (delphi_compatability.TShiftStateEnum.ssShift in Shift):
                #swallow key
                Key = 0
                self.moveSelectedTdosUp()
            else:
                Key = 0
                self.moveUpOrDownWithKey(self.focusedTdoIndexInList() - 1)
        elif Key == delphi_compatability.VK_RETURN:
            Key = 0
            self.renameClick(self)
        return Key
    
    def moveUpOrDownWithKey(self, indexAfterMove):
        list = TListCollection()
        
        list = self.selectedList(kThisList)
        if list == None:
            return
        if indexAfterMove > list.Count - 1:
            # loop around 
            indexAfterMove = 0
        if indexAfterMove < 0:
            indexAfterMove = list.Count - 1
        if (indexAfterMove >= 0) and (indexAfterMove <= list.Count - 1):
            self.deselectAllTdos()
            #no shift
            self.selectTdoAtIndex([], indexAfterMove)
            self.drawPreview(self.focusedTdo())
    
    def moveSelectedTdosDown(self):
        list = TListCollection()
        i = 0
        tdo = KfObject3D()
        
        if self.selectedTdos.Count <= 0:
            return
        list = self.selectedList(kThisList)
        if list == None:
            return
        if list.Count > 1:
            # start at next to last one because you can't move last one down any more 
            i = list.Count - 2
            while i >= 0:
                tdo = utdo.KfObject3D(list.Items[i])
                if self.selectedTdos.IndexOf(tdo) >= 0:
                    list.Move(i, i + 1)
                i -= 1
        self.redrawSelectedGrid()
        # reordering makes change flag true
        self.setChangedFlagForTdoList(true, self.selectedList(kThisList))
    
    def moveSelectedTdosUp(self):
        list = TListCollection()
        i = 0
        tdo = KfObject3D()
        
        if self.selectedTdos.Count <= 0:
            return
        list = self.selectedList(kThisList)
        if list == None:
            return
        if list.Count > 1:
            # start at 1 because you can't move first one up any more 
            i = 1
            while i <= list.Count - 1:
                tdo = utdo.KfObject3D(list.Items[i])
                if self.selectedTdos.IndexOf(tdo) >= 0:
                    list.Move(i, i - 1)
                i += 1
        self.redrawSelectedGrid()
        # reordering makes change flag true
        self.setChangedFlagForTdoList(true, self.selectedList(kThisList))
    
    def redrawSelectedGrid(self):
        if self.leftOrRight == kLeft:
            self.leftTdoList.Invalidate()
        else:
            self.rightTdoList.Invalidate()
    
    # -------------------------------------------------------------------------------------------- *updating 
    def updateForNewFile(self, newFileName, list):
        self.clearCommandList()
        self.setFileNameForList(newFileName, list)
        self.updateTdoListForList(list)
        self.setChangedFlagForTdoList(false, list)
        self.deselectAllTdos()
        if newFileName != "":
            if list == self.leftList:
                self.leftOrRight = kLeft
            else:
                self.leftOrRight = kRight
        self.updateForChangeToSelectedTdos()
    
    def deselectAllTdos(self):
        self.selectedTdos.Clear()
        self.leftTdoList.Invalidate()
        self.rightTdoList.Invalidate()
    
    def leftRightString(self, leftString, rightString):
        result = ""
        if self.leftOrRight == kLeft:
            result = leftString
        else:
            result = rightString
        return result
    
    def updateForChangeToSelectedTdos(self):
        atLeastOneTdoSelected = false
        atLeastOneFile = false
        
        self.leftTdoList.Invalidate()
        self.rightTdoList.Invalidate()
        if self.leftOrRight == kLeft:
            if self.haveLeftFile():
                self.leftOpenClose.Caption = "&Close"
            else:
                self.leftOpenClose.Caption = "&Open..."
            self.leftTdoFileNameEdit.Color = delphi_compatability.clAqua
            self.leftTdoFileNameEdit.Refresh()
            self.rightTdoFileNameEdit.Color = UNRESOLVED.clBtnFace
            self.rightTdoFileNameEdit.Refresh()
            self.drawPreview(self.focusedTdo())
        else:
            if self.haveRightFile():
                self.rightOpenClose.Caption = "&Close"
            else:
                self.rightOpenClose.Caption = "&Open..."
            self.leftTdoFileNameEdit.Color = UNRESOLVED.clBtnFace
            self.leftTdoFileNameEdit.Refresh()
            self.rightTdoFileNameEdit.Color = delphi_compatability.clAqua
            self.rightTdoFileNameEdit.Refresh()
            self.drawPreview(self.focusedTdo())
        atLeastOneFile = self.haveLeftFile() or self.haveRightFile()
        atLeastOneTdoSelected = (self.selectedTdos.Count > 0)
        self.transfer.Enabled = self.haveLeftFile() and self.haveRightFile() and atLeastOneTdoSelected
        self.transfer.Caption = self.leftRightString("&Transfer >>", "<< &Transfer")
        self.duplicate.Enabled = atLeastOneFile and atLeastOneTdoSelected
        self.delete.Enabled = atLeastOneFile and atLeastOneTdoSelected
        self.rename.Enabled = atLeastOneFile and atLeastOneTdoSelected
    
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
    
    def updateTdoListForList(self, list):
        grid = TDrawGrid()
        
        grid = self.gridForList(list)
        if grid == None:
            return
        grid.RowCount = list.Count
        grid.Invalidate()
    
    def drawPreview(self, tdo):
        turtle = KfTurtle()
        xScale = 0.0
        yScale = 0.0
        tdoBoundsRect = TRect()
        currentPosition = TPoint()
        currentScale = 0.0
        
        self.previewImage.Picture.Bitmap.Canvas.Brush.Color = delphi_compatability.clWindow
        self.previewImage.Picture.Bitmap.Canvas.FillRect(Rect(0, 0, self.previewImage.Width, self.previewImage.Height))
        self.previewImage.Picture.Bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        if tdo != None:
            turtle = uturtle.KfTurtle.defaultStartUsing()
            try:
                currentScale = 100.0
                currentPosition = Point(self.previewImage.Width / 2, self.previewImage.Height - self.previewImage.Height / 10)
                turtle.drawingSurface.pane = self.previewImage.Picture.Bitmap.Canvas
                turtle.setDrawOptionsForDrawingTdoOnly()
                turtle.drawOptions.draw3DObjects = false
                # draw first to get new scale
                # must be after pane and draw options set 
                turtle.reset()
                turtle.xyz(currentPosition.X, currentPosition.Y, 0)
                turtle.drawingSurface.recordingStart()
                tdo.draw(turtle, currentScale, "", "", 0, 0)
                turtle.drawingSurface.recordingStop()
                turtle.drawingSurface.recordingDraw()
                turtle.drawingSurface.clearTriangles()
                # calculate new scale to fit
                tdoBoundsRect = turtle.boundsRect()
                xScale = umath.safedivExcept(0.95 * currentScale * self.previewImage.Width, usupport.rWidth(tdoBoundsRect), 0.1)
                yScale = umath.safedivExcept(0.95 * currentScale * self.previewImage.Height, usupport.rHeight(tdoBoundsRect), 0.1)
                currentScale = umath.min(xScale, yScale)
                currentPosition = tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(self.previewImage.Width, self.previewImage.Height), currentScale)
                # draw second time for real
                turtle.drawOptions.draw3DObjects = true
                # must be after pane and draw options set 
                turtle.reset()
                turtle.xyz(currentPosition.X, currentPosition.Y, 0)
                turtle.drawingSurface.recordingStart()
                tdo.draw(turtle, currentScale, "", "", 0, 0)
                turtle.drawingSurface.recordingStop()
                turtle.drawingSurface.recordingDraw()
                turtle.drawingSurface.clearTriangles()
            finally:
                uturtle.KfTurtle.defaultStopUsing()
        self.previewImage.Picture.Bitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.previewImage.Picture.Bitmap.Canvas.Pen.Color = UNRESOLVED.clBtnText
        self.previewImage.Picture.Bitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        self.previewImage.Picture.Bitmap.Canvas.Rectangle(0, 0, self.previewImage.Width, self.previewImage.Height)
    
    def previewImageMouseUp(self, Sender, Button, Shift, X, Y):
        pass
    
    # ------------------------------------------------------------------------------------------ *selecting 
    def focusedTdo(self):
        result = KfObject3D()
        result = None
        if self.selectedTdos.Count > 0:
            result = utdo.KfObject3D(self.selectedTdos.Items[0])
        return result
    
    def focusedTdoIndexInList(self):
        result = 0
        list = TListCollection()
        
        result = -1
        list = self.selectedList(kThisList)
        if list == None:
            return result
        if self.selectedTdos.Count > 0:
            result = list.IndexOf(self.selectedTdos.Items[0])
        return result
    
    def haveLeftFile(self):
        result = false
        result = len(self.leftTdoFileName) != 0
        return result
    
    def haveRightFile(self):
        result = false
        result = len(self.rightTdoFileName) != 0
        return result
    
    def selectedList(self, thisList):
        result = TListCollection()
        result = None
        if self.leftOrRight == kLeft:
            if thisList:
                result = self.leftList
            else:
                result = self.rightList
        else:
            if thisList:
                result = self.rightList
            else:
                result = self.leftList
        return result
    
    def getFileNameForList(self, list):
        result = ""
        if list == self.leftList:
            result = self.leftTdoFileName
        else:
            result = self.rightTdoFileName
        return result
    
    def getFileNameForOtherList(self, list):
        result = ""
        if list == self.rightList:
            result = self.leftTdoFileName
        else:
            result = self.rightTdoFileName
        return result
    
    def setFileNameForList(self, newName, list):
        if list == self.leftList:
            self.leftTdoFileName = newName
            self.leftTdoFileNameEdit.Text = newName
            self.leftTdoFileNameEdit.SelStart = len(newName)
        else:
            self.rightTdoFileName = newName
            self.rightTdoFileNameEdit.Text = newName
            self.rightTdoFileNameEdit.SelStart = len(newName)
    
    def gridForList(self, list):
        result = TDrawGrid()
        result = None
        if list == self.leftList:
            result = self.leftTdoList
        elif list == self.rightList:
            result = self.rightTdoList
        return result
    
    def listHasChanged(self, list):
        result = false
        if list == self.leftList:
            result = self.leftTdoFileChanged
        else:
            result = self.rightTdoFileChanged
        return result
    
    def setChangedFlagForTdoList(self, value, list):
        if list == self.leftList:
            self.leftTdoFileChanged = value
            if self.leftTdoFileChanged:
                self.leftTdoFileChangedIndicator.Picture = umain.MainForm.fileChangedImage.Picture
            else:
                self.leftTdoFileChangedIndicator.Picture = umain.MainForm.fileNotChangedImage.Picture
        else:
            self.rightTdoFileChanged = value
            if self.rightTdoFileChanged:
                self.rightTdoFileChangedIndicator.Picture = umain.MainForm.fileChangedImage.Picture
            else:
                self.rightTdoFileChangedIndicator.Picture = umain.MainForm.fileNotChangedImage.Picture
    
    # ------------------------------------------------------------------------ *opening, closing and saving 
    def openTdoFileForList(self, list, fileNameToStart):
        fileNameWithPath = ""
        
        if not self.askToSaveListAndProceed(list):
            return
        if fileNameToStart == "":
            fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypeTdo, usupport.kNoSuggestedFile, "Choose a tdo file")
        else:
            fileNameWithPath = fileNameToStart
        if fileNameWithPath == "":
            self.updateForNewFile(fileNameWithPath, list)
        else:
            if fileNameWithPath == self.getFileNameForOtherList(list):
                ShowMessage("The file you chose is already open on the other side.")
                return
            try:
                ucursor.cursor_startWait()
                if FileExists(fileNameWithPath):
                    self.loadTdosFromFile(list, fileNameWithPath)
                else:
                    self.newTdoFileForList(list)
                # PDF PORT -- added semicolon
                self.updateForNewFile(fileNameWithPath, list)
            finally:
                ucursor.cursor_stopWait()
    
    def closeTdoFileForList(self, list):
        if not self.askToSaveListAndProceed(list):
            return
        list.clear()
        self.updateForNewFile("", list)
    
    def newTdoFileForList(self, list):
        if not self.askToSaveListAndProceed(list):
            return
        list.clear()
        self.updateForNewFile(kNewTdoFileName, list)
    
    def loadTdosFromFile(self, list, fileName):
        newTdo = KfObject3D()
        inputFile = TextFile()
        
        if list == None:
            return
        list.clear()
        if fileName == "":
            return
        if not FileExists(fileName):
            return
        AssignFile(inputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Reset(inputFile)
            while not UNRESOLVED.eof(inputFile):
                newTdo = utdo.KfObject3D().create()
                newTdo.readFromFileStream(inputFile, utdo.kInTdoLibrary)
                list.Add(newTdo)
        finally:
            CloseFile(inputFile)
    
    def saveTdosToFile(self, list, fileName):
        outputFile = TextFile()
        i = 0
        tdo = KfObject3D()
        
        if list == None:
            return
        # assume caller has already verified file name
        AssignFile(outputFile, fileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(outputFile)
            if list.Count > 0:
                for i in range(0, list.Count):
                    tdo = UNRESOLVED.TObject(list.Items[i]) as utdo.KfObject3D
                    if tdo == None:
                        continue
                    tdo.writeToFileStream(outputFile, utdo.kInTdoLibrary)
        finally:
            CloseFile(outputFile)
    
    def listSaveOrSaveAs(self, list, askForFileName):
        fileInfo = SaveFileNamesStructure()
        fileName = ""
        askForFileNameConsideringUntitled = false
        
        fileName = self.getFileNameForList(list)
        if fileName == kNewTdoFileName:
            askForFileNameConsideringUntitled = true
        else:
            askForFileNameConsideringUntitled = askForFileName
        if not usupport.getFileSaveInfo(usupport.kFileTypeTdo, askForFileNameConsideringUntitled, fileName, fileInfo):
            return
        try:
            ucursor.cursor_startWait()
            self.saveTdosToFile(list, fileInfo.tempFile)
            fileInfo.writingWasSuccessful = true
        finally:
            ucursor.cursor_stopWait()
            usupport.cleanUpAfterFileSave(fileInfo)
            self.updateForNewFile(kNewTdoFileName, list)
    
    def askToSaveListAndProceed(self, list):
        result = false
        response = 0
        prompt = ""
        
        # returns false if user cancelled action 
        result = true
        if not self.listHasChanged(list):
            return result
        prompt = "Save changes to " + ExtractFileName(self.getFileNameForList(list)) + "?"
        response = MessageDialog(prompt, mtConfirmation, mbYesNoCancel, 0)
        if response == mrYes:
            self.listSaveOrSaveAs(list, usupport.kDontAskForFileName)
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
        if self.leftList == None:
            return
        if self.rightList == None:
            return
        if self.selectedTdos == None:
            return
        midWidth = self.ClientWidth / 2
        #same as right
        listBoxWidth = self.leftTdoList.Width
        listBoxTop = kBetweenGap + self.leftTdoFileNameEdit.Height + kBetweenGap + self.leftOpenClose.Height + kBetweenGap
        # list boxes 
        self.leftTdoList.SetBounds(kBetweenGap, listBoxTop, listBoxWidth, umath.intMax(0, self.ClientHeight - listBoxTop - kBetweenGap))
        self.leftTdoList.DefaultColWidth = self.leftTdoList.ClientWidth
        self.rightTdoList.SetBounds(umath.intMax(0, self.ClientWidth - listBoxWidth - kBetweenGap), listBoxTop, listBoxWidth, umath.intMax(0, self.ClientHeight - listBoxTop - kBetweenGap))
        self.rightTdoList.DefaultColWidth = self.rightTdoList.ClientWidth
        # edits and buttons at top 
        self.leftTdoFileNameEdit.SetBounds(kBetweenGap, kBetweenGap, listBoxWidth - kBetweenGap * 2, self.leftTdoFileNameEdit.Height)
        self.leftTdoFileChangedIndicator.SetBounds(kBetweenGap, self.leftTdoFileNameEdit.Top + self.leftTdoFileNameEdit.Height + kBetweenGap, self.leftTdoFileChangedIndicator.Width, self.leftTdoFileChangedIndicator.Height)
        self.rightTdoFileNameEdit.SetBounds(self.rightTdoList.Left, kBetweenGap, listBoxWidth - kBetweenGap * 2, self.rightTdoFileNameEdit.Height)
        self.rightTdoFileChangedIndicator.SetBounds(self.rightTdoList.Left, self.rightTdoFileNameEdit.Top + self.rightTdoFileNameEdit.Height + kBetweenGap, self.rightTdoFileChangedIndicator.Width, self.rightTdoFileChangedIndicator.Height)
        openCloseTop = self.leftTdoFileNameEdit.Top + self.leftTdoFileNameEdit.Height + kBetweenGap
        self.leftOpenClose.SetBounds(self.leftTdoFileChangedIndicator.Left + self.leftTdoFileChangedIndicator.Width + kBetweenGap, openCloseTop, self.leftOpenClose.Width, self.leftOpenClose.Height)
        self.rightOpenClose.SetBounds(self.rightTdoFileChangedIndicator.Left + self.rightTdoFileChangedIndicator.Width + kBetweenGap, openCloseTop, self.rightOpenClose.Width, self.rightOpenClose.Height)
        self.newFile.SetBounds(self.rightOpenClose.Left + self.rightOpenClose.Width + kBetweenGap, openCloseTop, self.newFile.Width, self.newFile.Height)
        # buttons in middle 
        self.close.SetBounds(midWidth - self.close.Width / 2, umath.intMax(0, self.ClientHeight - self.close.Height - kBetweenGap), self.close.Width, self.close.Height)
        self.helpButton.SetBounds(self.close.Left, umath.intMax(0, self.close.Top - self.helpButton.Height - kBetweenGap), self.helpButton.Width, self.helpButton.Height)
        self.editTdo.SetBounds(self.close.Left, umath.intMax(0, self.helpButton.Top - self.editTdo.Height - kBetweenGap), self.editTdo.Width, self.editTdo.Height)
        self.redo.SetBounds(self.close.Left, umath.intMax(0, self.editTdo.Top - self.redo.Height - kBetweenGap), self.redo.Width, self.redo.Height)
        self.undo.SetBounds(self.close.Left, umath.intMax(0, self.redo.Top - self.undo.Height - kBetweenGap), self.undo.Width, self.undo.Height)
        self.rename.SetBounds(self.close.Left, umath.intMax(0, self.undo.Top - self.rename.Height - kBetweenGap), self.rename.Width, self.rename.Height)
        self.delete.SetBounds(self.close.Left, umath.intMax(0, self.rename.Top - self.delete.Height - kBetweenGap), self.delete.Width, self.delete.Height)
        self.duplicate.SetBounds(self.close.Left, umath.intMax(0, self.delete.Top - self.duplicate.Height - kBetweenGap), self.duplicate.Width, self.duplicate.Height)
        self.transfer.SetBounds(self.close.Left, umath.intMax(0, self.duplicate.Top - self.transfer.Height - kBetweenGap), self.transfer.Width, self.transfer.Height)
        self.previewImage.SetBounds(listBoxWidth + kBetweenGap * 2, kBetweenGap, umath.intMax(0, self.ClientWidth - listBoxWidth * 2 - kBetweenGap * 4), self.transfer.Top - kBetweenGap * 2)
        self.resizePreviewImage()
    
    def resizePreviewImage(self):
        try:
            self.previewImage.Picture.Bitmap.Height = self.previewImage.Height
            self.previewImage.Picture.Bitmap.Width = self.previewImage.Width
        except:
            self.previewImage.Picture.Bitmap.Height = 1
            self.previewImage.Picture.Bitmap.Width = 1
        self.drawPreview(self.focusedTdo())
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 400
        UNRESOLVED.ptMinTrackSize.y = 315
    
    # ----------------------------------------------------------------------------------------- command list 
    def clearCommandList(self):
        self.commandList.free
        self.commandList = None
        self.commandList = ucommand.PdCommandList().create()
        self.updateButtonsForUndoRedo()
    
    def doCommand(self, command):
        self.commandList.doCommand(command)
        self.updateButtonsForUndoRedo()
        self.updateForChangeToSelectedTdos()
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Using_the_3D_object_mover")
    
class PdTdoMoverRenameCommand(PdCommand):
    def __init__(self):
        self.tdo = KfObject3D()
        self.oldName = ""
        self.newName = ""
        self.list = TListCollection()
        self.listChangedBeforeCommand = false
    
    # ------------------------------------------------------------------------------ *commands 
    # ------------------------------------------------------------------- PdTdoMoverRenameCommand 
    def createWithTdoNewNameAndList(self, aTdo, aNewName, aList):
        PdCommand.create(self)
        self.commandChangesPlantFile = false
        self.tdo = aTdo
        self.oldName = self.tdo.getName()
        self.newName = aNewName
        self.list = aList
        self.listChangedBeforeCommand = TdoMoverForm.listHasChanged(self.list)
        return self
    
    def doCommand(self):
        #not redo
        PdCommand.doCommand(self)
        self.tdo.setName(self.newName)
        TdoMoverForm.setChangedFlagForTdoList(true, self.list)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        self.tdo.setName(self.oldName)
        TdoMoverForm.setChangedFlagForTdoList(self.listChangedBeforeCommand, self.list)
    
    def description(self):
        result = ""
        result = "rename"
        return result
    
class PdTdoMoverEditCommand(PdCommand):
    def __init__(self):
        self.tdo = KfObject3D()
        self.oldTdo = KfObject3D()
        self.newTdo = KfObject3D()
        self.list = TListCollection()
        self.listChangedBeforeCommand = false
    
    # ----------------------------------------------------------------------- PdTdoMoverEditCommand 
    def createWithTdoNewTdoAndList(self, aTdo, aNewTdo, aList):
        PdCommand.create(self)
        self.commandChangesPlantFile = false
        self.tdo = aTdo
        self.oldTdo = utdo.KfObject3D().create()
        self.oldTdo.copyFrom(aTdo)
        self.newTdo = utdo.KfObject3D().create()
        self.newTdo.copyFrom(aNewTdo)
        self.list = aList
        self.listChangedBeforeCommand = TdoMoverForm.listHasChanged(self.list)
        return self
    
    def destroy(self):
        self.oldTdo.free
        self.oldTdo = None
        self.newTdo.free
        self.newTdo = None
        PdCommand.destroy(self)
    
    def doCommand(self):
        #not redo
        PdCommand.doCommand(self)
        self.tdo.copyFrom(self.newTdo)
        TdoMoverForm.updateTdoListForList(self.list)
        TdoMoverForm.setChangedFlagForTdoList(true, self.list)
    
    def undoCommand(self):
        PdCommand.undoCommand(self)
        self.tdo.copyFrom(self.oldTdo)
        TdoMoverForm.updateTdoListForList(self.list)
        TdoMoverForm.setChangedFlagForTdoList(self.listChangedBeforeCommand, self.list)
    
    def description(self):
        result = ""
        result = "edit"
        return result
    
class PdCommandWithListOfTdos(PdCommand):
    def __init__(self):
        self.tdoList = TList()
        self.values = TListCollection()
        self.tdo = KfObject3D()
    
    #for temporary use
    # ----------------------------------------------------------------------- PdCommandWithListOfTdos 
    def createWithListOfTdos(self, aList):
        i = 0
        
        PdCommand.create(self)
        self.tdoList = delphi_compatability.TList().Create()
        if aList.Count > 0:
            for i in range(0, aList.Count):
                self.tdoList.Add(aList.Items[i])
        self.values = ucollect.TListCollection().Create()
        return self
    
    def destroy(self):
        self.tdoList.free
        self.tdoList = None
        self.values.free
        self.values = None
        PdCommand.destroy(self)
    
#use for cut and delete
class PdTdoMoverRemoveCommand(PdCommandWithListOfTdos):
    def __init__(self):
        self.removedTdos = TList()
        self.list = TListCollection()
        self.listChangedBeforeCommand = false
    
    # ----------------------------------------------------------------------- PdTdoMoverRemoveCommand 
    def createWithSelectedTdosAndList(self, listOfTdos, aList):
        PdCommandWithListOfTdos.createWithListOfTdos(self, listOfTdos)
        self.commandChangesPlantFile = false
        self.list = aList
        self.listChangedBeforeCommand = TdoMoverForm.listHasChanged(self.list)
        self.removedTdos = delphi_compatability.TList().Create()
        return self
    
    def destroy(self):
        i = 0
        
        if (self.done) and (self.removedTdos != None) and (self.removedTdos.Count > 0):
            for i in range(0, self.removedTdos.Count):
                # free copies of cut tdos if change was done 
                self.tdo = utdo.KfObject3D(self.removedTdos.Items[i])
                self.tdo.free
        self.removedTdos.free
        self.removedTdos = None
        PdCommandWithListOfTdos.destroy(self)
    
    def doCommand(self):
        i = 0
        
        #not redo
        PdCommandWithListOfTdos.doCommand(self)
        if self.tdoList.Count <= 0:
            return
        # save copy of tdos before deleting 
        self.removedTdos.Clear()
        for i in range(0, self.tdoList.Count):
            # don't remove tdos from list until all indexes have been recorded 
            self.tdo = utdo.KfObject3D(self.tdoList.Items[i])
            self.removedTdos.Add(self.tdo)
            self.tdo.indexWhenRemoved = self.list.IndexOf(self.tdo)
            self.tdo.selectedIndexWhenRemoved = TdoMoverForm.selectedTdos.IndexOf(self.tdo)
        for i in range(0, self.tdoList.Count):
            self.list.Remove(utdo.KfObject3D(self.tdoList.Items[i]))
        for i in range(0, self.tdoList.Count):
            TdoMoverForm.selectedTdos.Remove(utdo.KfObject3D(self.tdoList.Items[i]))
        TdoMoverForm.updateTdoListForList(self.list)
        TdoMoverForm.setChangedFlagForTdoList(true, self.list)
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfTdos.undoCommand(self)
        if self.removedTdos.Count > 0:
            for i in range(0, self.removedTdos.Count):
                self.tdo = utdo.KfObject3D(self.removedTdos.Items[i])
                if (self.tdo.indexWhenRemoved >= 0) and (self.tdo.indexWhenRemoved <= self.list.Count - 1):
                    self.list.Insert(self.tdo.indexWhenRemoved, self.tdo)
                else:
                    self.list.Add(self.tdo)
                if (self.tdo.selectedIndexWhenRemoved >= 0) and (self.tdo.selectedIndexWhenRemoved <= TdoMoverForm.selectedTdos.Count - 1):
                    # all removed tdos must have been selected, so also add them to the selected list 
                    TdoMoverForm.selectedTdos.Insert(self.tdo.selectedIndexWhenRemoved, self.tdo)
                else:
                    TdoMoverForm.selectedTdos.Add(self.tdo)
            TdoMoverForm.updateTdoListForList(self.list)
            TdoMoverForm.setChangedFlagForTdoList(self.listChangedBeforeCommand, self.list)
    
    def description(self):
        result = ""
        result = "delete"
        return result
    
class PdTdoMoverTransferCommand(PdCommandWithListOfTdos):
    def __init__(self):
        self.isTransfer = false
        self.list = TListCollection()
        self.listChangedBeforeCommand = false
    
    # ------------------------------------------------------------------ PdTdoMoverTransferCommand 
    def createWithSelectedTdosAndList(self, listOfTdos, aList):
        PdCommandWithListOfTdos.createWithListOfTdos(self, listOfTdos)
        self.commandChangesPlantFile = false
        self.list = aList
        self.listChangedBeforeCommand = TdoMoverForm.listHasChanged(self.list)
        return self
    
    def destroy(self):
        i = 0
        
        if (not self.done) and (self.tdoList != None) and (self.tdoList.Count > 0):
            for i in range(0, self.tdoList.Count):
                # free copies of pasted tdos if change was undone 
                self.tdo = utdo.KfObject3D(self.tdoList.Items[i])
                self.tdo.free
        #will free tdoList
        PdCommandWithListOfTdos.destroy(self)
    
    def doCommand(self):
        i = 0
        
        #not redo
        PdCommandWithListOfTdos.doCommand(self)
        if self.tdoList.Count > 0:
            TdoMoverForm.deselectAllTdos()
            for i in range(0, self.tdoList.Count):
                self.tdo = utdo.KfObject3D(self.tdoList.Items[i])
                self.list.Add(self.tdo)
                TdoMoverForm.selectedTdos.Add(self.tdo)
            TdoMoverForm.updateTdoListForList(self.list)
            TdoMoverForm.setChangedFlagForTdoList(true, self.list)
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfTdos.undoCommand(self)
        if self.tdoList.Count > 0:
            for i in range(0, self.tdoList.Count):
                self.tdo = utdo.KfObject3D(self.tdoList.Items[i])
                self.list.Remove(self.tdo)
                TdoMoverForm.selectedTdos.Remove(self.tdo)
            TdoMoverForm.updateTdoListForList(self.list)
            TdoMoverForm.setChangedFlagForTdoList(self.listChangedBeforeCommand, self.list)
    
    def description(self):
        result = ""
        result = "transfer"
        return result
    
class PdTdoMoverDuplicateCommand(PdCommandWithListOfTdos):
    def __init__(self):
        self.newTdos = TList()
        self.list = TListCollection()
        self.listChangedBeforeCommand = false
    
    # ------------------------------------------------------------------------------ PdTdoMoverDuplicateCommand 
    def createWithSelectedTdosAndList(self, listOfTdos, aList):
        PdCommandWithListOfTdos.createWithListOfTdos(self, listOfTdos)
        self.commandChangesPlantFile = false
        self.newTdos = delphi_compatability.TList().Create()
        self.list = aList
        self.listChangedBeforeCommand = TdoMoverForm.listHasChanged(self.list)
        return self
    
    def destroy(self):
        i = 0
        
        if (not self.done) and (self.newTdos != None) and (self.newTdos.Count > 0):
            for i in range(0, self.newTdos.Count):
                # free copies of created tdos if change was undone 
                self.tdo = utdo.KfObject3D(self.newTdos.Items[i])
                self.tdo.free
        self.newTdos.free
        self.newTdos = None
        #will free tdoList
        PdCommandWithListOfTdos.destroy(self)
    
    def doCommand(self):
        i = 0
        tdoCopy = KfObject3D()
        
        PdCommandWithListOfTdos.doCommand(self)
        if self.tdoList.Count > 0:
            TdoMoverForm.deselectAllTdos()
            for i in range(0, self.tdoList.Count):
                self.tdo = utdo.KfObject3D(self.tdoList.Items[i])
                tdoCopy = utdo.KfObject3D().create()
                self.tdo.copyTo(tdoCopy)
                tdoCopy.setName("Copy of " + tdoCopy.getName())
                self.newTdos.Add(tdoCopy)
                self.list.Add(tdoCopy)
                TdoMoverForm.selectedTdos.Add(tdoCopy)
            TdoMoverForm.updateTdoListForList(self.list)
            TdoMoverForm.setChangedFlagForTdoList(true, self.list)
    
    def undoCommand(self):
        i = 0
        
        PdCommandWithListOfTdos.undoCommand(self)
        if self.newTdos.Count > 0:
            for i in range(0, self.newTdos.Count):
                self.tdo = utdo.KfObject3D(self.newTdos.Items[i])
                self.list.Remove(self.tdo)
                TdoMoverForm.selectedTdos.Remove(self.tdo)
            TdoMoverForm.updateTdoListForList(self.list)
            TdoMoverForm.setChangedFlagForTdoList(self.listChangedBeforeCommand, self.list)
    
    def redoCommand(self):
        i = 0
        
        #not redo
        PdCommandWithListOfTdos.doCommand(self)
        if self.newTdos.Count > 0:
            TdoMoverForm.deselectAllTdos()
            for i in range(0, self.newTdos.Count):
                self.tdo = utdo.KfObject3D(self.newTdos.Items[i])
                self.list.Add(self.tdo)
                TdoMoverForm.selectedTdos.Add(self.tdo)
            TdoMoverForm.updateTdoListForList(self.list)
            TdoMoverForm.setChangedFlagForTdoList(true, self.list)
    
    def description(self):
        result = ""
        result = "duplicate"
        return result
    
