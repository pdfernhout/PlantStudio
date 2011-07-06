# unit upicktdo

from conversion_common import *
import utdomove
import updcom
import utdoedit
import umain
import uturtle
import udomain
import usupport
import updform
import uparams
import utdo
import ucollect
import delphi_compatability

class TPickTdoForm(PdForm):
    def __init__(self):
        self.grid = TDrawGrid()
        self.Close = TButton()
        self.cancel = TButton()
        self.newTdo = TButton()
        self.libraryGroupBox = TGroupBox()
        self.fileChangedImage = TImage()
        self.libraryFileName = TEdit()
        self.apply = TButton()
        self.helpButton = TSpeedButton()
        self.sectionTdosChangeLibrary = TSpeedButton()
        self.editTdo = TButton()
        self.mover = TButton()
        self.copyTdo = TButton()
        self.deleteTdo = TButton()
        self.tdos = TComboBox()
        self.param = PdParameter()
        self.originalTdo = KfObject3D()
        self.tdoSelectionChanged = false
        self.libraryChanged = false
        self.editedTdo = false
        self.internalChange = false
    
    #$R *.DFM
    def initializeWithTdoParameterAndPlantName(self, aTdo, aParam, aName):
        result = false
        # returns false if user canceled action
        result = true
        if not self.readTdosFromFile():
            MessageDialog("You cannot change or edit this 3D object" + chr(13) + "until you choose a 3D object library.", mtWarning, [mbOK, ], 0)
            result = false
            return result
        self.libraryFileName.Text = udomain.domain.defaultTdoLibraryFileName
        self.libraryFileName.SelStart = len(self.libraryFileName.Text)
        self.originalTdo = aTdo
        if self.originalTdo == None:
            raise GeneralException.create("Problem: Nil 3D object in method TPickTdoForm.initializeWithTdoParameterAndPlantName.")
        self.param = aParam
        if self.param == None:
            raise GeneralException.create("Problem: Nil parameter in method TPickTdoForm.initializeWithTdoParameterAndPlantName.")
        self.Caption = self.param.name + " for " + aName
        return result
    
    def FormActivate(self, Sender):
        self.selectTdoBasedOn(self.originalTdo)
    
    def selectTdoBasedOn(self, aTdo):
        indexToSelect = 0
        i = 0
        tdo = KfObject3D()
        
        # assumes initialize already called and tdos already in list
        indexToSelect = -1
        if self.tdos.Items.Count > 0:
            for i in range(0, self.tdos.Items.Count):
                tdo = utdo.KfObject3D(self.tdos.Items.Objects[i])
                if tdo.isSameAs(aTdo):
                    indexToSelect = i
                    break
        if indexToSelect < 0:
            if MessageDialog("This 3D object is not in the current library." + chr(13) + "Its name or shape is different from the 3D objects in the list." + chr(13) + chr(13) + "Do you want to add this 3D object to the library?", mtWarning, [mbYes, mbNo, ], 0) == delphi_compatability.IDNO:
                return
            tdo = utdo.KfObject3D().create()
            tdo.copyFrom(aTdo)
            self.tdos.Items.AddObject(tdo.name, tdo)
            self.grid.RowCount = self.tdos.Items.Count / self.grid.ColCount + 1
            self.libraryGroupBox.Caption = "The current library has " + IntToStr(self.tdos.Items.Count) + " object(s)"
            self.setLibraryChanged(true)
            indexToSelect = self.tdos.Items.Count - 1
        if indexToSelect >= 0:
            self.selectTdoAtIndex(indexToSelect)
    
    def selectTdoAtIndex(self, indexToSelect):
        gridRect = TGridRect()
        lastRow = 0
        
        self.chooseTdoFromList(indexToSelect)
        if (indexToSelect < 0) or (indexToSelect > self.tdos.Items.Count - 1):
            gridRect.left = -1
            gridRect.top = -1
        else:
            gridRect.left = indexToSelect % self.grid.ColCount
            gridRect.top = indexToSelect / self.grid.ColCount
        gridRect.right = gridRect.left
        gridRect.bottom = gridRect.top
        self.grid.Selection = gridRect
        # keep selection in view
        lastRow = self.grid.TopRow + self.grid.VisibleRowCount - 1
        if gridRect.top > lastRow:
            self.grid.TopRow = self.grid.TopRow + (gridRect.top - lastRow)
    
    def selectedTdo(self):
        result = KfObject3D()
        index = 0
        
        result = None
        index = self.grid.Selection.top * self.grid.ColCount + self.grid.Selection.left
        if (index >= 0) and (index <= self.tdos.Items.Count - 1):
            result = UNRESOLVED.TObject(self.tdos.Items.Objects[index]) as utdo.KfObject3D
        return result
    
    def chooseTdoFromList(self, index):
        if (index >= 0) and (index <= self.tdos.Items.Count - 1):
            self.tdos.ItemIndex = index
    
    def CloseClick(self, Sender):
        if (self.tdoSelectionChanged or self.editedTdo) and (self.selectedTdo() != None):
            self.applyClick(self)
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def applyClick(self, Sender):
        if self.selectedTdo() != None:
            umain.MainForm.doCommand(updcom.PdChangeTdoValueCommand().createCommandWithListOfPlants(umain.MainForm.selectedPlants, self.selectedTdo(), self.param.fieldNumber, self.param.regrow))
    
    def loadNewTdoLibrary(self):
        fileNameWithPath = ""
        
        fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypeTdo, udomain.domain.defaultTdoLibraryFileName, "Choose a 3D object library (tdo) file")
        if fileNameWithPath == "":
            return
        udomain.domain.defaultTdoLibraryFileName = fileNameWithPath
        self.readTdosFromFile()
    
    def readTdosFromFile(self):
        result = false
        newTdo = KfObject3D()
        inputFile = TextFile()
        
        # returns false if file could not be found and user canceled finding another
        result = true
        self.tdos.Clear()
        if udomain.domain == None:
            return result
        if not udomain.domain.checkForExistingDefaultTdoLibrary():
            result = false
            return result
        AssignFile(inputFile, udomain.domain.defaultTdoLibraryFileName)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Reset(inputFile)
            while not UNRESOLVED.eof(inputFile):
                newTdo = utdo.KfObject3D().create()
                newTdo.readFromFileStream(inputFile, utdo.kInTdoLibrary)
                self.tdos.Items.AddObject(newTdo.name, newTdo)
        finally:
            CloseFile(inputFile)
            self.grid.RowCount = self.tdos.Items.Count / self.grid.ColCount + 1
            self.libraryGroupBox.Caption = "The current library has " + IntToStr(self.tdos.Items.Count) + " object(s)"
        return result
    
    def saveTdosToLibrary(self):
        fileInfo = SaveFileNamesStructure()
        suggestedName = ""
        outputFile = TextFile()
        i = 0
        tdo = KfObject3D()
        
        suggestedName = udomain.domain.defaultTdoLibraryFileName
        if not usupport.getFileSaveInfo(usupport.kFileTypeTdo, usupport.kDontAskForFileName, suggestedName, fileInfo):
            return
        AssignFile(outputFile, fileInfo.tempFile)
        try:
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(outputFile)
            usupport.startFileSave(fileInfo)
            if self.tdos.Items.Count > 0:
                for i in range(0, self.tdos.Items.Count):
                    tdo = UNRESOLVED.TObject(self.tdos.Items.Objects[i]) as utdo.KfObject3D
                    if tdo == None:
                        continue
                    tdo.writeToFileStream(outputFile, utdo.kInTdoLibrary)
            fileInfo.writingWasSuccessful = true
        finally:
            CloseFile(outputFile)
            usupport.cleanUpAfterFileSave(fileInfo)
            self.setLibraryChanged(false)
    
    def setLibraryChanged(self, fileChanged):
        self.libraryChanged = fileChanged
        if self.libraryChanged:
            self.fileChangedImage.Picture = umain.MainForm.fileChangedImage.Picture
        else:
            self.fileChangedImage.Picture = umain.MainForm.fileNotChangedImage.Picture
    
    def tdoForIndex(self, index):
        result = KfObject3D()
        result = None
        if (index >= 0) and (index <= self.tdos.Items.Count - 1):
            result = utdo.KfObject3D(self.tdos.Items.Objects[index])
        return result
    
    def gridDrawCell(self, Sender, Col, Row, Rect, State):
        tdo = KfObject3d()
        turtle = KfTurtle()
        selected = false
        index = 0
        bitmap = TBitmap()
        bestPoint = TPoint()
        
        self.grid.Canvas.Brush.Color = self.grid.Color
        self.grid.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear
        self.grid.Canvas.FillRect(Rect)
        selected = UNRESOLVED.gdSelected in State
        tdo = None
        index = Row * self.grid.ColCount + Col
        tdo = self.tdoForIndex(index)
        if tdo == None:
            return
        # draw tdo 
        turtle = uturtle.KfTurtle.defaultStartUsing()
        bitmap = delphi_compatability.TBitmap().Create()
        try:
            bitmap.Width = self.grid.DefaultColWidth
            bitmap.Height = self.grid.DefaultRowHeight
        except:
            bitmap.Width = 1
            bitmap.Height = 1
        if not selected:
            bitmap.Canvas.Brush.Color = delphi_compatability.clWhite
        else:
            bitmap.Canvas.Brush.Color = UNRESOLVED.clHighlight
        bitmap.Canvas.FillRect(UNRESOLVED.classes.Rect(0, 0, bitmap.Width, bitmap.Height))
        try:
            #grid.canvas;
            turtle.drawingSurface.pane = bitmap.Canvas
            turtle.setDrawOptionsForDrawingTdoOnly()
            # must be after pane and draw options set 
            turtle.reset()
            # v1.6b1 added method for centering tdo
            bestPoint = tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(bitmap.Width, bitmap.Height), 0.3)
            turtle.xyz(bestPoint.X, bestPoint.Y, 0)
            turtle.drawingSurface.recordingStart()
            #0.15);
            tdo.draw(turtle, 0.3, "", "", 0, 0)
            turtle.drawingSurface.recordingStop()
            turtle.drawingSurface.recordingDraw()
            turtle.drawingSurface.clearTriangles()
            self.grid.Canvas.Draw(Rect.left, Rect.top, bitmap)
            self.grid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
            self.grid.Canvas.Pen.Color = delphi_compatability.clSilver
            self.grid.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
            # FIX unresolved WITH expression: Rect
            self.grid.Canvas.Rectangle(self.Left, self.Top, UNRESOLVED.right, UNRESOLVED.bottom)
        finally:
            uturtle.KfTurtle.defaultStopUsing()
            bitmap.free
    
    def gridSelectCell(self, Sender, Col, Row, CanSelect):
        if self.internalChange:
            return CanSelect
        self.tdoSelectionChanged = true
        self.chooseTdoFromList(Row * self.grid.ColCount + Col)
        return CanSelect
    
    def tdosChange(self, Sender):
        self.internalChange = true
        self.tdoSelectionChanged = true
        self.grid.Row = self.tdos.ItemIndex / self.grid.ColCount
        self.grid.Col = self.tdos.ItemIndex % self.grid.ColCount
        self.internalChange = false
    
    def hintForTdosDrawGridAtPoint(self, aComponent, aPoint, cursorRect):
        raise "method hintForTdosDrawGridAtPoint had assigned to var parameter cursorRect not added to return; fixup manually"
        result = ""
        col = 0
        row = 0
        index = 0
        tdo = KfObject3D()
        
        result = ""
        col, row = self.grid.MouseToCell(aPoint.X, aPoint.Y, col, row)
        index = row * self.grid.ColCount + col
        tdo = self.tdoForIndex(index)
        if tdo == None:
            return result
        result = tdo.getName()
        # change hint if cursor moves out of the current item's rectangle 
        cursorRect = self.grid.CellRect(col, row)
        return result
    
    def sectionTdosChangeLibraryClick(self, Sender):
        self.loadNewTdoLibrary()
        self.grid.Invalidate()
        self.libraryFileName.Text = udomain.domain.defaultTdoLibraryFileName
        self.libraryFileName.SelStart = len(self.libraryFileName.Text)
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Using_3D_object_parameter_panels")
    
    def FormClose(self, Sender, Action):
        response = 0
        
        if self.libraryChanged:
            if self.ModalResult == mrOK:
                self.saveTdosToLibrary()
            elif self.ModalResult == mrCancel:
                response = MessageDialog("Do you want to save the changes you made" + chr(13) + "to the 3D object library?", mtConfirmation, [mbYes, mbNo, mbCancel, ], 0)
                if response == delphi_compatability.IDYES:
                    self.saveTdosToLibrary()
                    Action = delphi_compatability.TCloseAction.caFree
                elif response == delphi_compatability.IDNO:
                    Action = delphi_compatability.TCloseAction.caFree
                elif response == delphi_compatability.IDCANCEL:
                    Action = delphi_compatability.TCloseAction.caNone
    
    def gridDblClick(self, Sender):
        self.applyClick(self)
    
    def editTdoClick(self, Sender):
        tdoEditorForm = TTdoEditorForm()
        response = 0
        
        if self.selectedTdo() == None:
            return
        tdoEditorForm = utdoedit.TTdoEditorForm().create(self)
        if tdoEditorForm == None:
            raise GeneralException.create("Problem: Could not create 3D object editor window.")
        try:
            tdoEditorForm.initializeWithTdo(self.selectedTdo())
            response = tdoEditorForm.ShowModal()
            if response == mrOK:
                self.selectedTdo().copyFrom(tdoEditorForm.tdo)
                self.editedTdo = true
                self.grid.Invalidate()
                self.setLibraryChanged(true)
                self.chooseTdoFromList(self.tdos.Items.IndexOfObject(self.selectedTdo()))
        finally:
            tdoEditorForm.free
            tdoEditorForm = None
    
    def newTdoClick(self, Sender):
        tdoEditorForm = TTdoEditorForm()
        response = 0
        newTdo = KfObject3D()
        newName = ""
        
        newName = ""
        newTdo = utdo.KfObject3D().create()
        newTdo.setName("New 3D object")
        tdoEditorForm = utdoedit.TTdoEditorForm().create(self)
        if tdoEditorForm == None:
            raise GeneralException.create("Problem: Could not create 3D object editor window.")
        try:
            tdoEditorForm.initializeWithTdo(newTdo)
            response = tdoEditorForm.ShowModal()
            if response == mrOK:
                if newTdo.getName() == "New 3D object":
                    if InputQuery("Name 3D object", "Enter a name for the new 3D object", newName):
                        newTdo.setName(newName)
                    else:
                        newTdo.setName("Unnamed 3D object")
                newTdo.copyFrom(tdoEditorForm.tdo)
                self.editedTdo = true
                self.tdos.Items.AddObject(newTdo.name, newTdo)
                self.grid.RowCount = self.tdos.Items.Count / self.grid.ColCount + 1
                self.selectTdoAtIndex(self.tdos.Items.Count - 1)
                self.libraryGroupBox.Caption = "The current library has " + IntToStr(self.tdos.Items.Count) + " object(s)"
                self.setLibraryChanged(true)
                self.chooseTdoFromList(self.tdos.Items.IndexOfObject(self.selectedTdo()))
        finally:
            tdoEditorForm.free
            tdoEditorForm = None
    
    def copyTdoClick(self, Sender):
        newTdo = KfObject3D()
        newName = ""
        
        if self.selectedTdo() == None:
            return
        newName = "Copy of " + self.selectedTdo().getName()
        if not InputQuery("Enter name for copy", "Type a name for the copy of " + self.selectedTdo().getName(), newName):
            return
        newTdo = utdo.KfObject3D().create()
        self.selectedTdo().copyTo(newTdo)
        newTdo.setName(newName)
        self.tdos.Items.AddObject(newTdo.name, newTdo)
        self.grid.RowCount = self.tdos.Items.Count / self.grid.ColCount + 1
        self.selectTdoAtIndex(self.tdos.Items.Count - 1)
        self.libraryGroupBox.Caption = "The current library has " + IntToStr(self.tdos.Items.Count) + " object(s)"
        self.setLibraryChanged(true)
        self.chooseTdoFromList(self.tdos.Items.IndexOfObject(self.selectedTdo()))
    
    def deleteTdoClick(self, Sender):
        oldIndex = 0
        nameToShow = ""
        
        if self.selectedTdo() == None:
            return
        nameToShow = self.selectedTdo().getName()
        if nameToShow == "":
            nameToShow = "[unnamed]"
        if MessageDialog("Really delete the 3D object named " + nameToShow + "?" + chr(13) + chr(13) + "(You cannot undo this action," + chr(13) + "but you can close the window and not save your changes" + chr(13) + "if you need to get this 3D object back.)", mtConfirmation, [mbYes, mbNo, ], 0) == delphi_compatability.IDNO:
            return
        oldIndex = self.tdos.Items.IndexOfObject(self.selectedTdo())
        self.tdos.Items.Delete(oldIndex)
        self.grid.RowCount = self.tdos.Items.Count / self.grid.ColCount + 1
        self.selectTdoAtIndex(oldIndex)
        self.libraryGroupBox.Caption = "The current library has " + IntToStr(self.tdos.Items.Count) + " object(s)"
        self.setLibraryChanged(true)
        self.chooseTdoFromList(self.tdos.Items.IndexOfObject(self.selectedTdo()))
        self.grid.Invalidate()
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 404
        # only resizes vertically
        UNRESOLVED.ptMaxTrackSize.x = 404
        UNRESOLVED.ptMinTrackSize.y = 303
    
    def FormResize(self, Sender):
        resizeGridHeight = 0
        rowsToShow = 0
        integralGridHeight = 0
        
        if delphi_compatability.Application.terminated:
            # only resizes vertically
            return
        if self.param == None:
            return
        if self.originalTdo == None:
            return
        self.tdos.SetBounds(self.tdos.Left, 4, self.tdos.Width, self.tdos.Height)
        resizeGridHeight = self.ClientHeight - self.libraryGroupBox.Height - self.tdos.Height - 4 * 4
        rowsToShow = resizeGridHeight / self.grid.DefaultRowHeight
        integralGridHeight = self.grid.DefaultRowHeight * rowsToShow + self.grid.GridLineWidth * (rowsToShow - 1) + 2
        self.grid.SetBounds(self.grid.Left, self.tdos.Top + self.tdos.Height + 4, self.grid.Width, integralGridHeight)
        self.libraryGroupBox.SetBounds(self.libraryGroupBox.Left, self.ClientHeight - self.libraryGroupBox.Height - 4, self.libraryGroupBox.Width, self.libraryGroupBox.Height)
    
    def moverClick(self, Sender):
        tdoMoverForm = TTdoMoverForm()
        response = 0
        
        if self.libraryChanged:
            response = MessageDialog("Do you want to save your changes to " + ExtractFileName(udomain.domain.defaultTdoLibraryFileName) + chr(13) + "before you use the 3D object mover?" + chr(13) + chr(13) + "If not, they will be lost.", mtConfirmation, mbYesNoCancel, 0)
            if response == delphi_compatability.IDCANCEL:
                return
            elif response == delphi_compatability.IDYES:
                self.saveTdosToLibrary()
            elif response == delphi_compatability.IDNO:
                pass
        tdoMoverForm = utdomove.TTdoMoverForm().create(self)
        if tdoMoverForm == None:
            raise GeneralException.create("Problem: Could not create 3D object mover window.")
        try:
            tdoMoverForm.ShowModal()
            self.readTdosFromFile()
            self.selectTdoAtIndex(-1)
        finally:
            tdoMoverForm.free
            tdoMoverForm = None
    
