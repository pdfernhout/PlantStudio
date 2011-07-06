# unit utimeser

from conversion_common import *
import ubmpsupport
import ubreedr
import umain
import ucommand
import updcom
import ucursor
import usupport
import umath
import udomain
import uplant
import ucollect
import updform
import delphi_compatability

# const
kRecalculateScale = true
kDontRecalculateScale = false
kMaxTimeSeriesStages = 100

# var
TimeSeriesForm = TTimeSeriesForm()

# const
kStageNumberTextHeight = 16

class TTimeSeriesForm(PdForm):
    def __init__(self):
        self.grid = TDrawGrid()
        self.MainMenu1 = TMainMenu()
        self.TimeSeriesMenuEdit = TMenuItem()
        self.TimeSeriesMenuUndo = TMenuItem()
        self.TimeSeriesMenuRedo = TMenuItem()
        self.N1 = TMenuItem()
        self.TimeSeriesMenuCopy = TMenuItem()
        self.TimeSeriesMenuPaste = TMenuItem()
        self.TimeSeriesMenuBreed = TMenuItem()
        self.TimeSeriesPopupMenu = TPopupMenu()
        self.TimeSeriesPopupMenuBreed = TMenuItem()
        self.TimeSeriesPopupMenuCopy = TMenuItem()
        self.TimeSeriesPopupMenuPaste = TMenuItem()
        self.N2 = TMenuItem()
        self.emptyWarningPanel = TPanel()
        self.Label1 = TLabel()
        self.N3 = TMenuItem()
        self.TimeSeriesMenuDelete = TMenuItem()
        self.N4 = TMenuItem()
        self.TimeSeriesMenuOptions = TMenuItem()
        self.TimeSeriesMenuOptionsStages = TMenuItem()
        self.TimeSeriesMenuHelp = TMenuItem()
        self.TimeSeriesMenuHelpOnTimeSeries = TMenuItem()
        self.TimeSeriesMenuHelpTopics = TMenuItem()
        self.N5 = TMenuItem()
        self.TimeSeriesMenuOptionsDrawAs = TMenuItem()
        self.TimeSeriesMenuOptionsFastDraw = TMenuItem()
        self.TimeSeriesMenuOptionsMediumDraw = TMenuItem()
        self.TimeSeriesMenuOptionsBestDraw = TMenuItem()
        self.TimeSeriesMenuOptionsCustomDraw = TMenuItem()
        self.TimeSeriesMenuUndoRedoList = TMenuItem()
        self.TimeSeriesMenuSendCopy = TMenuItem()
        self.TimeSeriesPopupMenuSendCopy = TMenuItem()
        self.parentPlant = PdPlant()
        self.plants = TListCollection()
        self.numStages = 0
        self.selectedPlant = PdPlant()
        self.dragPlantStartPoint = TPoint()
        self.numTimeSeriesPlantsCopiedThisSession = 0
        self.internalChange = false
        self.percentsOfMaxAge = [0] * (range(0, kMaxTimeSeriesStages + 1) + 1)
        self.ages = [0] * (range(0, kMaxTimeSeriesStages + 1) + 1)
        self.drawing = false
        self.drawProgressMax = 0L
        self.resizing = false
        self.needToRedrawFromChangeToDrawOptions = false
    
    #$R *.DFM
    def FormCreate(self, Sender):
        tempBoundsRect = TRect()
        
        self.plants = ucollect.TListCollection().Create()
        self.grid.DragCursor = ucursor.crDragPlant
        self.Position = delphi_compatability.TPosition.poDesigned
        # keep window on screen - left corner of title bar 
        tempBoundsRect = udomain.domain.timeSeriesWindowRect
        if (tempBoundsRect.Left != 0) or (tempBoundsRect.Right != 0) or (tempBoundsRect.Top != 0) or (tempBoundsRect.Bottom != 0):
            if tempBoundsRect.Left > delphi_compatability.Screen.Width - umain.kMinWidthOnScreen:
                tempBoundsRect.Left = delphi_compatability.Screen.Width - umain.kMinWidthOnScreen
            if tempBoundsRect.Top > delphi_compatability.Screen.Height - umain.kMinHeightOnScreen:
                tempBoundsRect.Top = delphi_compatability.Screen.Height - umain.kMinHeightOnScreen
            self.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom)
        if udomain.domain.options.drawSpeed == udomain.kDrawFast:
            self.TimeSeriesMenuOptionsFastDraw.checked = true
        elif udomain.domain.options.drawSpeed == udomain.kDrawMedium:
            self.TimeSeriesMenuOptionsMediumDraw.checked = true
        elif udomain.domain.options.drawSpeed == udomain.kDrawBest:
            self.TimeSeriesMenuOptionsBestDraw.checked = true
        elif udomain.domain.options.drawSpeed == udomain.kDrawCustom:
            self.TimeSeriesMenuOptionsCustomDraw.checked = true
        #to get redo messages
        umain.MainForm.updateMenusForUndoRedo()
        self.updateForChangeToDomainOptions()
        self.updateMenusForChangeToSelectedPlant()
        self.updatePasteMenuForClipboardContents()
        self.emptyWarningPanel.SendToBack()
        self.emptyWarningPanel.Hide()
    
    def FormDestroy(self, Sender):
        self.plants.free
        self.plants = None
    
    def FormActivate(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        if self.plants.Count <= 0:
            self.emptyWarningPanel.BringToFront()
            self.emptyWarningPanel.Show()
        elif self.needToRedrawFromChangeToDrawOptions:
            self.redrawPlants()
            self.needToRedrawFromChangeToDrawOptions = false
    
    def initializeWithPlant(self, aPlant, drawNow):
        newPlant = PdPlant()
        i = 0
        
        if aPlant == None:
            return
        if not self.Visible:
            self.Show()
        self.BringToFront()
        self.plants.clear()
        self.parentPlant = aPlant
        ucursor.cursor_startWait()
        try:
            for i in range(0, self.numStages):
                newPlant = uplant.PdPlant().create()
                self.parentPlant.copyTo(newPlant)
                self.ages[i] = intround(umath.max(0.0, umath.min(1.0, self.percentsOfMaxAge[i] / 100.0)) * newPlant.pGeneral.ageAtMaturity)
                newPlant.setAge(self.ages[i])
                self.plants.Add(newPlant)
        finally:
            ucursor.cursor_stopWait()
        if drawNow:
            self.redrawPlants()
    
    # ----------------------------------------------------------------------------------- updating 
    def updateForChangeToDomainOptions(self):
        i = 0
        
        if udomain.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages != self.numStages:
            self.numStages = udomain.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages
            for i in range(0, self.numStages):
                self.percentsOfMaxAge[i] = umath.intMin(100, umath.intMax(0, (i + 1) * 100 / self.numStages))
            if self.grid.ColCount != self.numStages:
                self.grid.ColCount = self.numStages
            self.updateForNewNumberOfStages()
        if self.grid.DefaultColWidth != udomain.domain.breedingAndTimeSeriesOptions.thumbnailWidth:
            self.grid.DefaultColWidth = udomain.domain.breedingAndTimeSeriesOptions.thumbnailWidth
        if self.grid.DefaultRowHeight != udomain.domain.breedingAndTimeSeriesOptions.thumbnailHeight:
            self.grid.DefaultRowHeight = udomain.domain.breedingAndTimeSeriesOptions.thumbnailHeight
            self.grid.RowHeights[1] = kStageNumberTextHeight
        self.redrawPlants()
    
    def updateForNewNumberOfStages(self):
        i = 0
        firstPlant = PdPlant()
        keepPlant = PdPlant()
        
        keepPlant = None
        try:
            if self.plants.Count > 0:
                firstPlant = uplant.PdPlant(self.plants.Items[0])
                if firstPlant != None:
                    keepPlant = uplant.PdPlant().create()
                    firstPlant.copyTo(keepPlant)
                    self.plants.clear()
            if keepPlant != None:
                self.initializeWithPlant(keepPlant, umain.kDontDrawYet)
        finally:
            keepPlant.free
        self.redrawPlants()
    
    def updateForChangeToPlants(self, recalcScale):
        self.selectedPlant = None
        if self.plants.Count <= 0:
            self.parentPlant = None
        self.updateMenusForChangeToSelectedPlant()
        if not self.Visible:
            self.Show()
        self.BringToFront()
        if self.WindowState == delphi_compatability.TWindowState.wsMinimized:
            self.WindowState = delphi_compatability.TWindowState.wsNormal
        self.redrawPlants()
    
    def updateMenusForChangeToSelectedPlant(self):
        self.TimeSeriesMenuCopy.enabled = (self.selectedPlant != None)
        self.TimeSeriesPopupMenuCopy.enabled = self.TimeSeriesMenuCopy.enabled
        self.TimeSeriesMenuBreed.enabled = (self.selectedPlant != None)
        self.TimeSeriesPopupMenuBreed.enabled = self.TimeSeriesMenuBreed.enabled
    
    def updatePasteMenuForClipboardContents(self):
        self.TimeSeriesMenuPaste.enabled = (udomain.domain.plantManager.privatePlantClipboard.Count > 0)
        self.TimeSeriesPopupMenuPaste.enabled = (udomain.domain.plantManager.privatePlantClipboard.Count > 0)
    
    def updatePlantsFromParent(self, aPlant):
        if (aPlant == None) or (aPlant != self.parentPlant) or (self.plants.Count <= 0):
            return
        self.initializeWithPlant(aPlant, umain.kDrawNow)
    
    # ----------------------------------------------------------------------------------- plants 
    def plantForIndex(self, index):
        result = PdPlant()
        result = None
        if index < 0:
            return result
        if index > self.plants.Count - 1:
            return result
        if self.plants.Items[index] == None:
            return result
        result = uplant.PdPlant(self.plants.Items[index])
        return result
    
    def plantAtMouse(self, x, y):
        result = PdPlant()
        col = 0L
        row = 0L
        
        result = None
        col, row = self.grid.MouseToCell(x, y, col, row)
        if (col < 0) or (col > self.plants.Count - 1):
            return result
        result = self.plantForIndex(col)
        return result
    
    # -------------------------------------------------------------------------------------- drawing 
    def redrawPlants(self):
        if self.plants.Count <= 0:
            self.emptyWarningPanel.BringToFront()
            self.emptyWarningPanel.Show()
        else:
            self.emptyWarningPanel.SendToBack()
            self.emptyWarningPanel.Hide()
        self.recalculateCommonDrawingScaleAndPosition()
        self.grid.Invalidate()
    
    def recalculateCommonDrawingScaleAndPosition(self):
        plant = PdPlant()
        i = 0
        minScale = 0.0
        plantPartsToDraw = 0L
        partsDrawn = 0L
        bestPosition = TPoint()
        widestWidth = 0L
        tallestHeight = 0L
        
        if self.plants == None:
            return
        if self.plants.Count <= 0:
            return
        # find smallest scale
        minScale = 0.0
        for i in range(0, self.plants.Count):
            plant = uplant.PdPlant(self.plants.Items[i])
            plant.fixedPreviewScale = false
            plant.fixedDrawPosition = false
            plant.drawPreviewIntoCache(Point(self.grid.DefaultColWidth, self.grid.DefaultRowHeight), uplant.kDontConsiderDomainScale, uplant.kDontDrawNow)
            if (i == 0) or (plant.drawingScale_PixelsPerMm < minScale):
                minScale = plant.drawingScale_PixelsPerMm
        # find common draw position
        widestWidth = 0
        tallestHeight = 0
        for i in range(0, self.plants.Count):
            plant = uplant.PdPlant(self.plants.Items[i])
            plant.fixedPreviewScale = true
            plant.drawingScale_PixelsPerMm = minScale
            plant.fixedDrawPosition = false
            plant.drawPreviewIntoCache(Point(self.grid.DefaultColWidth, self.grid.DefaultRowHeight), uplant.kDontConsiderDomainScale, uplant.kDontDrawNow)
            if (i == 0) or (usupport.rWidth(plant.boundsRect_pixels()) > widestWidth):
                widestWidth = usupport.rWidth(plant.boundsRect_pixels())
                bestPosition.X = plant.drawPositionIfFixed.X
            if (i == 0) or (usupport.rHeight(plant.boundsRect_pixels()) > tallestHeight):
                tallestHeight = usupport.rHeight(plant.boundsRect_pixels())
                bestPosition.Y = plant.drawPositionIfFixed.Y
        for i in range(0, self.plants.Count):
            # set draw position to use when repaint - don't draw now
            plant = uplant.PdPlant(self.plants.Items[i])
            plant.fixedPreviewScale = true
            plant.drawingScale_PixelsPerMm = minScale
            plant.fixedDrawPosition = true
            plant.drawPositionIfFixed = bestPosition
            plant.previewCacheUpToDate = false
    
    # -------------------------------------------------------------------------------------- grid 
    def gridDrawCell(self, Sender, Col, Row, Rect, State):
        plant = PdPlant()
        textDrawRect = TRect()
        textToDraw = ""
        
        self.grid.Canvas.Brush.Color = delphi_compatability.clWhite
        self.grid.Canvas.Pen.Width = 1
        if (self.plants.Count > 0) and (Row == 0):
            self.grid.Canvas.Pen.Color = delphi_compatability.clSilver
        else:
            self.grid.Canvas.Pen.Color = delphi_compatability.clWhite
        self.grid.Canvas.Rectangle(Rect.left, Rect.top, Rect.right, Rect.bottom)
        if Row == 1:
            if self.plants.Count <= 0:
                return
            textToDraw = IntToStr(self.ages[Col])
            if usupport.rWidth(Rect) > 50:
                # 50 is fixed size
                textToDraw = textToDraw + " days"
            textDrawRect.Left = Rect.left + usupport.rWidth(Rect) / 2 - self.grid.Canvas.TextWidth(textToDraw) / 2
            textDrawRect.Top = Rect.top + usupport.rHeight(Rect) / 2 - self.grid.Canvas.TextHeight("0") / 2
            self.grid.Canvas.TextOut(textDrawRect.Left, textDrawRect.Top, textToDraw)
            return
        plant = None
        plant = self.plantForIndex(Col)
        if plant == None:
            return
        if not plant.previewCacheUpToDate:
            # draw plant 
            # draw gray solid box to show delay for drawing plant cache
            self.grid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
            self.grid.Canvas.Brush.Color = delphi_compatability.clSilver
            self.grid.Canvas.Pen.Color = delphi_compatability.clSilver
            # FIX unresolved WITH expression: Rect
            self.grid.Canvas.Rectangle(self.Left + 1, self.Top + 1, UNRESOLVED.right, UNRESOLVED.bottom)
            plant.drawPreviewIntoCache(Point(self.grid.DefaultColWidth, self.grid.DefaultRowHeight), uplant.kDontConsiderDomainScale, umain.kDrawNow)
        plant.previewCache.Transparent = false
        ubmpsupport.copyBitmapToCanvasWithGlobalPalette(plant.previewCache, self.grid.Canvas, Rect)
        # draw selection rectangle 
        self.grid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        self.grid.Canvas.Pen.Width = 2
        if plant == self.selectedPlant:
            self.grid.Canvas.Pen.Color = udomain.domain.options.firstSelectionRectangleColor
        else:
            self.grid.Canvas.Pen.Color = delphi_compatability.clSilver
        # FIX unresolved WITH expression: Rect
        self.grid.Canvas.Rectangle(self.Left + 1, self.Top + 1, UNRESOLVED.right, UNRESOLVED.bottom)
    
    def gridMouseDown(self, Sender, Button, Shift, X, Y):
        self.selectedPlant = self.plantAtMouse(X, Y)
        self.updateMenusForChangeToSelectedPlant()
        self.grid.Invalidate()
        if (Button == delphi_compatability.TMouseButton.mbRight) or (delphi_compatability.TShiftStateEnum.ssShift in Shift):
            # start drag of plant
            return
        if self.selectedPlant == None:
            return
        self.dragPlantStartPoint = Point(X, Y)
        self.grid.BeginDrag(false)
    
    def gridDragOver(self, Sender, Source, X, Y, State, Accept):
        Accept = (Source != None) and (Sender != None) and ((Source == umain.MainForm.drawingPaintBox) or (Source == umain.MainForm.plantListDrawGrid) or (Source == ubreedr.BreederForm.plantsDrawGrid))
        return Accept
    
    def gridEndDrag(self, Sender, Target, X, Y):
        plant = PdPlant()
        newCommand = PdCommand()
        newPlants = TList()
        newPlant = PdPlant()
        
        if delphi_compatability.Application.terminated:
            return
        if Target == None:
            return
        # get plant being dragged 
        plant = self.plantAtMouse(self.dragPlantStartPoint.X, self.dragPlantStartPoint.Y)
        if plant == None:
            return
        if Target == ubreedr.BreederForm.plantsDrawGrid:
            ubreedr.BreederForm.copyPlantToPoint(plant, X, Y)
        elif (Target == umain.MainForm.drawingPaintBox) or (Target == umain.MainForm.plantListDrawGrid):
            # make paste command - wants list of plants 
            newPlant = uplant.PdPlant().create()
            plant.copyTo(newPlant)
            self.numTimeSeriesPlantsCopiedThisSession += 1
            newPlant.setName("Time series plant " + IntToStr(self.numTimeSeriesPlantsCopiedThisSession))
            if Target == umain.MainForm.drawingPaintBox:
                newPlant.moveTo(Point(X, Y))
            else:
                newPlant.moveTo(umain.MainForm.standardPastePosition())
            if not udomain.domain.viewPlantsInMainWindowOnePlantAtATime():
                # v2.1
                newPlant.calculateDrawingScaleToLookTheSameWithDomainScale()
            #to save memory - don't need it in main window
            newPlant.shrinkPreviewCache()
            newPlants = delphi_compatability.TList().Create()
            newPlants.Add(newPlant)
            newCommand = updcom.PdPasteCommand().createWithListOfPlantsAndOldSelectedList(newPlants, umain.MainForm.selectedPlants)
            updcom.PdPasteCommand(newCommand).useSpecialPastePosition = true
            try:
                #command will free plant if paste is undone
                ucursor.cursor_startWait()
                umain.MainForm.doCommand(newCommand)
            finally:
                #command has another list, so we must free this one
                newPlants.free
                ucursor.cursor_stopWait()
    
    def copyPlantToPoint(self, aPlant, x, y):
        newCommand = PdCommand()
        
        newCommand = updcom.PdMakeTimeSeriesCommand().createWithNewPlant(aPlant)
        umain.MainForm.doCommand(newCommand)
    
    def invalidateGridCell(self, column):
        cellRectOver = TRect()
        
        if (column < 0):
            return
        cellRectOver = self.grid.CellRect(column, 0)
        UNRESOLVED.invalidateRect(self.grid.Handle, cellRectOver, true)
    
    # ------------------------------------------------------------------------------- menu 
    def TimeSeriesMenuUndoClick(self, Sender):
        umain.MainForm.MenuEditUndoClick(umain.MainForm)
    
    def TimeSeriesMenuRedoClick(self, Sender):
        umain.MainForm.MenuEditRedoClick(umain.MainForm)
    
    def TimeSeriesMenuUndoRedoListClick(self, Sender):
        umain.MainForm.UndoMenuEditUndoRedoListClick(umain.MainForm)
    
    def TimeSeriesMenuCopyClick(self, Sender):
        plant = PdPlant()
        copyList = TList()
        saveName = ""
        
        plant = self.selectedPlant
        if plant == None:
            return
        copyList = delphi_compatability.TList().Create()
        copyList.Add(plant)
        # temporarily change plant name, position, scale to make copy, then put back 
        saveName = plant.getName()
        self.numTimeSeriesPlantsCopiedThisSession += 1
        plant.setName("Time series plant " + IntToStr(self.numTimeSeriesPlantsCopiedThisSession))
        udomain.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(copyList)
        plant.setName(saveName)
        #sets our paste menu also
        umain.MainForm.updatePasteMenuForClipboardContents()
    
    def TimeSeriesMenuPasteClick(self, Sender):
        newPlant = PdPlant()
        newCommand = PdCommand()
        
        if udomain.domain.plantManager.privatePlantClipboard.Count <= 0:
            return
        newPlant = uplant.PdPlant().create()
        try:
            udomain.domain.plantManager.pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant)
            newCommand = updcom.PdMakeTimeSeriesCommand().createWithNewPlant(newPlant)
            (newCommand as updcom.PdMakeTimeSeriesCommand).isPaste = true
            umain.MainForm.doCommand(newCommand)
        finally:
            #command makes copies from plant, but we must free it
            newPlant.free
    
    def TimeSeriesMenuSendCopyClick(self, Sender):
        self.TimeSeriesMenuCopyClick(self)
        umain.MainForm.MenuEditPasteClick(umain.MainForm)
    
    def TimeSeriesMenuBreedClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedPlant == None:
            return
        if ubreedr.BreederForm.selectedRow >= udomain.domain.breedingAndTimeSeriesOptions.maxGenerations - 2:
            # check if there is room in the breeder - this command will make two new generations 
            ubreedr.BreederForm.fullWarning()
        else:
            newCommand = updcom.PdBreedFromParentsCommand().createWithInfo(ubreedr.BreederForm.generations, self.selectedPlant, None, -1, udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, updcom.kCreateFirstGeneration)
            umain.MainForm.doCommand(newCommand)
    
    def TimeSeriesMenuDeleteClick(self, Sender):
        newCommand = PdCommand()
        
        newCommand = updcom.PdDeleteTimeSeriesCommand().create()
        umain.MainForm.doCommand(newCommand)
    
    def TimeSeriesPopupMenuCopyClick(self, Sender):
        self.TimeSeriesMenuCopyClick(self)
    
    def TimeSeriesPopupMenuPasteClick(self, Sender):
        self.TimeSeriesMenuPasteClick(self)
    
    def TimeSeriesPopupMenuBreedClick(self, Sender):
        self.TimeSeriesMenuBreedClick(self)
    
    # ------------------------------------------------------------------------------- resizing 
    def FormResize(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        if self.plants == None:
            return
        self.grid.SetBounds(0, 0, self.ClientWidth, umath.intMax(0, self.ClientHeight))
        self.emptyWarningPanel.SetBounds(self.ClientWidth / 2 - self.emptyWarningPanel.Width / 2, self.ClientHeight / 2 - self.emptyWarningPanel.Height / 2, self.emptyWarningPanel.Width, self.emptyWarningPanel.Height)
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 280
        UNRESOLVED.ptMinTrackSize.y = 120
    
    # ----------------------------------------------------------------------------- *palette stuff 
    def GetPalette(self):
        result = HPALETTE()
        result = umain.MainForm.paletteImage.Picture.Bitmap.Palette
        return result
    
    def PaletteChanged(self, Foreground):
        result = false
        oldPalette = HPALETTE()
        palette = HPALETTE()
        windowHandle = HWnd()
        DC = HDC()
        
        palette = self.GetPalette()
        if palette != 0:
            DC = self.GetDeviceContext(windowHandle)
            oldPalette = UNRESOLVED.selectPalette(DC, palette, not Foreground)
            if (UNRESOLVED.realizePalette(DC) != 0) and (not delphi_compatability.Application.terminated) and (self.grid != None):
                # if palette changed, repaint drawing 
                self.grid.Invalidate()
            UNRESOLVED.selectPalette(DC, oldPalette, true)
            UNRESOLVED.realizePalette(DC)
            UNRESOLVED.releaseDC(windowHandle, DC)
        result = PdForm.PaletteChanged(self, Foreground)
        return result
    
    def TimeSeriesMenuHelpTopicsClick(self, Sender):
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_FINDER, 0)
    
    def TimeSeriesMenuHelpOnTimeSeriesClick(self, Sender):
        delphi_compatability.Application.HelpJump("Making_time_series")
    
    def TimeSeriesMenuOptionsStagesClick(self, Sender):
        ubreedr.BreederForm.changeBreederAndTimeSeriesOptions(0)
    
    def TimeSeriesMenuOptionsFastDrawClick(self, Sender):
        umain.MainForm.MenuOptionsFastDrawClick(umain.MainForm)
    
    def TimeSeriesMenuOptionsMediumDrawClick(self, Sender):
        umain.MainForm.MenuOptionsMediumDrawClick(umain.MainForm)
    
    def TimeSeriesMenuOptionsBestDrawClick(self, Sender):
        umain.MainForm.MenuOptionsBestDrawClick(umain.MainForm)
    
    def TimeSeriesMenuOptionsCustomDrawClick(self, Sender):
        umain.MainForm.MenuOptionsCustomDrawClick(umain.MainForm)
    
