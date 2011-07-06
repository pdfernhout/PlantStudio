# unit Ubreedr

from conversion_common import *
import ubmpsupport
import utimeser
import updcom
import ucommand
import umain
import umath
import ucursor
import usupport
import ubrdopt
import udomain
import updform
import ugener
import uplant
import ucollect
import delphi_compatability

# var
BreederForm = TBreederForm()

# const
kRedrawPlants = true
kDontRedrawPlants = false
kConsiderIfPreviewCacheIsUpToDate = true
kDontConsiderIfPreviewCacheIsUpToDate = false

# const
kSelectionIsInFirstColumn = true
kSelectionIsNotInFirstColumn = false
kFirstColumnWidth = 20
kBetweenGap = 4
kOptionTabSize = 0
kOptionTabMutation = 1
kOptionTabBlending = 2
kOptionTabNonNumeric = 3
kOptionTabTdos = 4

class TBreederForm(PdForm):
    def __init__(self):
        self.plantsDrawGrid = TDrawGrid()
        self.BreederMenu = TMainMenu()
        self.BreederMenuEdit = TMenuItem()
        self.BreederMenuCopy = TMenuItem()
        self.BreederMenuPaste = TMenuItem()
        self.N2 = TMenuItem()
        self.BreederMenuPlant = TMenuItem()
        self.BreederMenuBreed = TMenuItem()
        self.BreederMenuUndo = TMenuItem()
        self.BreederMenuRedo = TMenuItem()
        self.N1 = TMenuItem()
        self.BreederMenuDeleteRow = TMenuItem()
        self.BreederMenuDeleteAll = TMenuItem()
        self.BreederPopupMenu = TPopupMenu()
        self.BreederPopupMenuBreed = TMenuItem()
        self.BreederPopupMenuCopy = TMenuItem()
        self.BreederPopupMenuPaste = TMenuItem()
        self.BreederPopupMenuDeleteRow = TMenuItem()
        self.N4 = TMenuItem()
        self.BreederMenuRandomize = TMenuItem()
        self.BreederMenuRandomizeAll = TMenuItem()
        self.BreederMenuMakeTimeSeries = TMenuItem()
        self.BreederPopupMenuRandomize = TMenuItem()
        self.N5 = TMenuItem()
        self.emptyWarningPanel = TPanel()
        self.Label1 = TLabel()
        self.BreederPopupMenuMakeTimeSeries = TMenuItem()
        self.BreederMenuVariation = TMenuItem()
        self.BreederMenuVariationLow = TMenuItem()
        self.BreederMenuVariationMedium = TMenuItem()
        self.BreederMenuVariationHigh = TMenuItem()
        self.BreederMenuVariationCustom = TMenuItem()
        self.BreederMenuOptions = TMenuItem()
        self.BreederMenuOtherOptions = TMenuItem()
        self.MenuBreederHelp = TMenuItem()
        self.BreederMenuHelpOnBreeding = TMenuItem()
        self.BreederMenuHelpTopics = TMenuItem()
        self.N3 = TMenuItem()
        self.BreederMenuOptionsDrawAs = TMenuItem()
        self.BreederMenuOptionsFastDraw = TMenuItem()
        self.BreederMenuOptionsMediumDraw = TMenuItem()
        self.BreederMenuOptionsBestDraw = TMenuItem()
        self.BreederMenuOptionsCustomDraw = TMenuItem()
        self.N6 = TMenuItem()
        self.BreederMenuVaryColors = TMenuItem()
        self.BreederMenuVary3DObjects = TMenuItem()
        self.breederToolbarPanel = TPanel()
        self.variationLow = TSpeedButton()
        self.variationMedium = TSpeedButton()
        self.variationCustom = TSpeedButton()
        self.varyColors = TSpeedButton()
        self.vary3DObjects = TSpeedButton()
        self.helpButton = TSpeedButton()
        self.variationHigh = TSpeedButton()
        self.BreederMenuVariationNone = TMenuItem()
        self.variationNoneNumeric = TSpeedButton()
        self.BreederMenuSendCopyToMainWindow = TMenuItem()
        self.N7 = TMenuItem()
        self.BreederPopupMenuSendCopytoMainWindow = TMenuItem()
        self.N8 = TMenuItem()
        self.breedButton = TSpeedButton()
        self.BreederMenuUndoRedoList = TMenuItem()
        self.selectedRow = 0
        self.generations = TListCollection()
        self.dragPlantStartPoint = TPoint()
        self.lightUpCell = TPoint()
        self.numBreederPlantsCopiedThisSession = 0L
        self.internalChange = false
        self.drawing = false
        self.needToRedrawFromChangeToDrawOptions = false
    
    #$R *.DFM
    # ---------------------------------------------------------------------------- creation/destruction 
    def FormCreate(self, Sender):
        tempBoundsRect = TRect()
        
        self.generations = ucollect.TListCollection().Create()
        self.plantsDrawGrid.DragCursor = ucursor.crDragPlant
        self.Position = delphi_compatability.TPosition.poDesigned
        # keep window on screen - left corner of title bar 
        tempBoundsRect = udomain.domain.breederWindowRect
        if (tempBoundsRect.Left != 0) or (tempBoundsRect.Right != 0) or (tempBoundsRect.Top != 0) or (tempBoundsRect.Bottom != 0):
            if tempBoundsRect.Left > delphi_compatability.Screen.Width - umain.kMinWidthOnScreen:
                tempBoundsRect.Left = delphi_compatability.Screen.Width - umain.kMinWidthOnScreen
            if tempBoundsRect.Top > delphi_compatability.Screen.Height - umain.kMinHeightOnScreen:
                tempBoundsRect.Top = delphi_compatability.Screen.Height - umain.kMinHeightOnScreen
            self.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom)
        if udomain.domain.options.drawSpeed == udomain.kDrawFast:
            self.BreederMenuOptionsFastDraw.checked = true
        elif udomain.domain.options.drawSpeed == udomain.kDrawMedium:
            self.BreederMenuOptionsMediumDraw.checked = true
        elif udomain.domain.options.drawSpeed == udomain.kDrawBest:
            self.BreederMenuOptionsBestDraw.checked = true
        elif udomain.domain.options.drawSpeed == udomain.kDrawCustom:
            self.BreederMenuOptionsCustomDraw.checked = true
        self.updateForChangeToDomainOptions()
        self.updateMenusForChangeToGenerations()
        #to get redo messages
        umain.MainForm.updateMenusForUndoRedo()
        self.lightUpCell = Point(-1, -1)
        self.emptyWarningPanel.SendToBack()
    
    def FormDestroy(self, Sender):
        self.generations.free
        self.generations = None
    
    def FormActivate(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        if self.generations.Count <= 0:
            self.emptyWarningPanel.BringToFront()
        elif self.needToRedrawFromChangeToDrawOptions:
            self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate)
            self.needToRedrawFromChangeToDrawOptions = false
    
    # -------------------------------------------------------------------------------------- grid 
    def updateForChangeToDomainOptions(self):
        generation = PdGeneration()
        plant = PdPlant()
        genCount = 0
        plCount = 0
        newAge = 0
        atLeastOnePlantHasChangedAge = false
        
        if self.plantsDrawGrid.ColCount != udomain.domain.breedingAndTimeSeriesOptions.plantsPerGeneration + 1:
            self.plantsDrawGrid.ColCount = udomain.domain.breedingAndTimeSeriesOptions.plantsPerGeneration + 1
        if ((self.plantsDrawGrid.DefaultColWidth != udomain.domain.breedingAndTimeSeriesOptions.thumbnailWidth) or (self.plantsDrawGrid.DefaultRowHeight != udomain.domain.breedingAndTimeSeriesOptions.thumbnailHeight)):
            self.plantsDrawGrid.DefaultColWidth = udomain.domain.breedingAndTimeSeriesOptions.thumbnailWidth
            self.plantsDrawGrid.ColWidths[0] = kFirstColumnWidth
            self.plantsDrawGrid.DefaultRowHeight = udomain.domain.breedingAndTimeSeriesOptions.thumbnailHeight
            self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate)
        if udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationLow:
            self.BreederMenuVariationLow.checked = true
            self.variationLow.Down = true
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationMedium:
            self.BreederMenuVariationMedium.checked = true
            self.variationMedium.Down = true
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationHigh:
            self.BreederMenuVariationHigh.checked = true
            self.variationHigh.Down = true
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationCustom:
            self.BreederMenuVariationCustom.checked = true
            self.variationCustom.Down = true
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationNoNumeric:
            self.BreederMenuVariationNone.checked = true
            self.variationNoneNumeric.Down = true
        self.BreederMenuVaryColors.checked = udomain.domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues
        self.varyColors.Down = udomain.domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues
        self.BreederMenuVary3DObjects.checked = udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary
        self.vary3DObjects.Down = udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary
        self.redoCaption()
        atLeastOnePlantHasChangedAge = false
        if self.generations.Count > 0:
            for genCount in range(0, self.generations.Count):
                generation = ugener.PdGeneration(self.generations.Items[genCount])
                if generation.plants.Count > 0:
                    for plCount in range(0, generation.plants.Count):
                        plant = uplant.PdPlant(generation.plants.Items[plCount])
                        newAge = intround(udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0 * plant.pGeneral.ageAtMaturity)
                        if plant.age != newAge:
                            plant.setAge(newAge)
                            atLeastOnePlantHasChangedAge = true
        if atLeastOnePlantHasChangedAge:
            self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate)
    
    def redrawPlants(self, considerIfPreviewCacheIsUpToDate):
        generation = PdGeneration()
        plant = PdPlant()
        genCount = 0
        plCount = 0
        
        if not considerIfPreviewCacheIsUpToDate:
            for genCount in range(0, self.generations.Count):
                generation = ugener.PdGeneration(self.generations.Items[genCount])
                if generation.plants.Count > 0:
                    for plCount in range(0, generation.plants.Count):
                        plant = uplant.PdPlant(generation.plants.Items[plCount])
                        plant.previewCacheUpToDate = false
        self.plantsDrawGrid.Invalidate()
        self.plantsDrawGrid.Update()
    
    def plantsDrawGridDrawCell(self, Sender, Col, Row, Rect, State):
        generation = PdGeneration()
        plant = PdPlant()
        textDrawRect = TRect()
        
        try:
            self.plantsDrawGrid.Canvas.Font = self.plantsDrawGrid.Font
            self.plantsDrawGrid.Canvas.Font.Color = delphi_compatability.clBlack
            if Col == 0:
                #if (row = selectedRow) and (generations.count > 0) then
                #plantsDrawGrid.canvas.brush.color := clBlue
                #else
                self.plantsDrawGrid.Canvas.Brush.Color = delphi_compatability.clWhite
                self.plantsDrawGrid.Canvas.Pen.Color = self.plantsDrawGrid.Canvas.Brush.Color
                self.plantsDrawGrid.Canvas.Rectangle(Rect.left, Rect.top, Rect.right, Rect.bottom)
                if Row > self.generations.Count - 1:
                    return
                #if row = selectedRow then
                #plantsDrawGrid.canvas.font.color := clWhite;
                textDrawRect.Left = Rect.left + usupport.rWidth(Rect) / 2 - self.plantsDrawGrid.Canvas.TextWidth(IntToStr(Row + 1)) / 2
                textDrawRect.Top = Rect.top + usupport.rHeight(Rect) / 2 - self.plantsDrawGrid.Canvas.TextHeight("0") / 2
                self.plantsDrawGrid.Canvas.TextOut(textDrawRect.Left, textDrawRect.Top, IntToStr(Row + 1))
                return
            else:
                self.plantsDrawGrid.Canvas.Brush.Color = delphi_compatability.clWhite
                self.plantsDrawGrid.Canvas.Pen.Width = 1
                self.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clWhite
                self.plantsDrawGrid.Canvas.Rectangle(Rect.left, Rect.top, Rect.right, Rect.bottom)
            generation = None
            generation = self.generationForIndex(Row)
            if generation == None:
                return
            plant = None
            plant = generation.plantForIndex(Col - 1)
            if plant == None:
                return
            if not plant.previewCacheUpToDate:
                # draw plant 
                # draw gray solid box to show delay for drawing plant cache
                self.plantsDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
                self.plantsDrawGrid.Canvas.Brush.Color = delphi_compatability.clSilver
                self.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clSilver
                # FIX unresolved WITH expression: Rect
                self.plantsDrawGrid.Canvas.Rectangle(self.Left + 1, self.Top + 1, UNRESOLVED.right, UNRESOLVED.bottom)
                # draw plant preview cache
                plant.fixedPreviewScale = false
                plant.fixedDrawPosition = false
                plant.drawPreviewIntoCache(Point(self.plantsDrawGrid.DefaultColWidth, self.plantsDrawGrid.DefaultRowHeight), uplant.kDontConsiderDomainScale, umain.kDrawNow)
            plant.previewCache.Transparent = false
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(plant.previewCache, self.plantsDrawGrid.Canvas, Rect)
            # draw selection rectangle 
            self.plantsDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
            self.plantsDrawGrid.Canvas.Pen.Width = 2
            if (Col == self.lightUpCell.X) and (Row == self.lightUpCell.Y):
                self.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clAqua
            elif Row == self.selectedRow:
                if plant == generation.firstSelectedPlant():
                    self.plantsDrawGrid.Canvas.Pen.Color = udomain.domain.options.firstSelectionRectangleColor
                elif plant == generation.secondSelectedPlant():
                    self.plantsDrawGrid.Canvas.Pen.Color = udomain.domain.options.multiSelectionRectangleColor
                else:
                    self.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clSilver
            else:
                self.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clSilver
            # FIX unresolved WITH expression: Rect
            self.plantsDrawGrid.Canvas.Rectangle(self.Left + 1, self.Top + 1, UNRESOLVED.right, UNRESOLVED.bottom)
            if plant == generation.firstParent:
                # draw parent indicator 
                self.plantsDrawGrid.Canvas.TextOut(Rect.left + 4, Rect.top + 2, "p1")
            elif plant == generation.secondParent:
                self.plantsDrawGrid.Canvas.TextOut(Rect.left + 4, Rect.top + 2, "p2")
        finally:
            ucursor.cursor_stopWait()
    
    def invalidateGridCell(self, column, row):
        cellRectOver = TRect()
        
        if (column < 0) and (row < 0):
            return
        cellRectOver = self.plantsDrawGrid.CellRect(column, row)
        UNRESOLVED.invalidateRect(self.plantsDrawGrid.Handle, cellRectOver, true)
    
    def invalidateGridRow(self, row):
        rowRectOver = TRect()
        
        if row < 0:
            return
        rowRectOver = self.plantsDrawGrid.CellRect(0, row)
        rowRectOver.Right = self.plantsDrawGrid.Width
        UNRESOLVED.invalidateRect(self.plantsDrawGrid.Handle, rowRectOver, true)
    
    def plantsDrawGridMouseUp(self, Sender, Button, Shift, X, Y):
        col = 0L
        row = 0L
        generation = PdGeneration()
        plant = PdPlant()
        
        if delphi_compatability.Application.terminated:
            return
        # had selection here, moved to mouse down because double-click makes extra mouse up, seems okay so far
    
    def plantsDrawGridDblClick(self, Sender):
        self.BreederMenuBreedClick(self)
    
    # ------------------------------------------------------------------------ dragging 
    def plantsDrawGridMouseDown(self, Sender, Button, Shift, X, Y):
        plant = PdPlant()
        col = 0
        row = 0
        oldSelectedRow = 0
        generation = PdGeneration()
        
        col, row = self.plantsDrawGrid.MouseToCell(X, Y, col, row)
        if (row >= 0) and (row <= self.generations.Count - 1):
            generation = ugener.PdGeneration(self.generations.Items[row])
            if generation != None:
                self.selectGeneration(generation)
                if (col >= 1) and (col - 1 <= generation.plants.Count - 1):
                    plant = uplant.PdPlant(generation.plants.Items[col - 1])
                    if plant != None:
                        generation.selectPlant(plant, (delphi_compatability.TShiftStateEnum.ssShift in Shift))
                    else:
                        generation.deselectAllPlants()
                    # in first column or past them on right 
                else:
                    generation.deselectAllPlants()
            else:
                self.deselectAllGenerations()
        else:
            self.deselectAllGenerations()
        self.updateForChangeToGenerations()
        if (Button == delphi_compatability.TMouseButton.mbRight) or (delphi_compatability.TShiftStateEnum.ssShift in Shift):
            # start drag of plant
            return
        plant = self.plantAtMouse(X, Y)
        if plant == None:
            return
        self.dragPlantStartPoint = Point(X, Y)
        self.plantsDrawGrid.BeginDrag(false)
    
    def plantsDrawGridDragOver(self, Sender, Source, X, Y, State, Accept):
        col = 0L
        row = 0L
        plant = PdPlant()
        
        Accept = (Source != None) and (Sender != None) and ((Sender == Source) or (Source == umain.MainForm.drawingPaintBox) or (Source == umain.MainForm.plantListDrawGrid) or (Source == utimeser.TimeSeriesForm.grid))
        if (Accept):
            plant = self.plantAtMouse(X, Y)
            if plant == None:
                Accept = false
                return Accept
            col, row = self.plantsDrawGrid.MouseToCell(X, Y, col, row)
            if (col != self.lightUpCell.X) or (row != self.lightUpCell.Y):
                self.invalidateGridCell(self.lightUpCell.X, self.lightUpCell.Y)
                self.lightUpCell = Point(col, row)
                self.invalidateGridCell(col, row)
        return Accept
    
    def plantsDrawGridEndDrag(self, Sender, Target, X, Y):
        col = 0L
        row = 0L
        plant = PdPlant()
        plantToReplace = PdPlant()
        newCommand = PdCommand()
        newPlants = TList()
        newPlant = PdPlant()
        
        if delphi_compatability.Application.terminated:
            return
        # remove lightup on cell before resetting cell
        self.invalidateGridCell(self.lightUpCell.X, self.lightUpCell.Y)
        self.lightUpCell = Point(-1, -1)
        if Target == None:
            return
        # get plant being dragged 
        plant = self.plantAtMouse(self.dragPlantStartPoint.X, self.dragPlantStartPoint.Y)
        if plant == None:
            return
        if (Target == umain.MainForm.drawingPaintBox) or (Target == umain.MainForm.plantListDrawGrid):
            # make paste command - wants list of plants 
            newPlant = uplant.PdPlant().create()
            plant.copyTo(newPlant)
            self.numBreederPlantsCopiedThisSession += 1
            newPlant.setName("Breeder plant " + IntToStr(self.numBreederPlantsCopiedThisSession))
            if (Target == umain.MainForm.drawingPaintBox):
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
                ucursor.cursor_startWait()
                umain.MainForm.doCommand(newCommand)
            finally:
                #command has another list, so we must free this one
                newPlants.free
                ucursor.cursor_stopWait()
            #command will free plant if paste is undone
        elif Target == utimeser.TimeSeriesForm.grid:
            utimeser.TimeSeriesForm.copyPlantToPoint(plant, X, Y)
        elif Target == Sender:
            # get plant being replaced 
            col, row = self.plantsDrawGrid.MouseToCell(X, Y, col, row)
            if not self.inGrid(row, col):
                return
            plantToReplace = self.plantForRowAndColumn(row, col)
            if plantToReplace == None:
                return
            if plantToReplace == plant:
                return
            # make replace command 
            newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(plant, row, col)
            try:
                ucursor.cursor_startWait()
                umain.MainForm.doCommand(newCommand)
            finally:
                ucursor.cursor_stopWait()
    
    def copyPlantToPoint(self, aPlant, x, y):
        col = 0L
        row = 0L
        plant = PdPlant()
        newCommand = PdCommand()
        
        col, row = self.plantsDrawGrid.MouseToCell(x, y, col, row)
        plant = self.plantForRowAndColumn(row, col)
        if plant == None:
            return
        newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(aPlant, row, col)
        umain.MainForm.doCommand(newCommand)
    
    # ------------------------------------------------------------- responding to commands 
    def replacePlantInRow(self, oldPlant, newPlant, row):
        generation = PdGeneration()
        
        generation = self.generationForIndex(row)
        if generation == None:
            raise GeneralException.create("Problem: Invalid row in method TBreederForm.replacePlantInRow.")
        generation.replacePlant(oldPlant, newPlant)
        self.updateForChangeToPlant(newPlant)
    
    def forgetGenerationsListBelowRow(self, aRow):
        while self.generations.Count - 1 > aRow:
            self.forgetLastGeneration()
    
    def addGenerationsFromListBelowRow(self, aRow, aGenerationsList):
        i = 0
        
        if aRow + 1 <= aGenerationsList.Count - 1:
            for i in range(aRow + 1, aGenerationsList.Count):
                self.addGeneration(ugener.PdGeneration(aGenerationsList.Items[i]))
    
    def addGeneration(self, newGeneration):
        self.generations.Add(newGeneration)
    
    def forgetLastGeneration(self):
        lastGeneration = PdGeneration()
        
        if self.generations.Count <= 0:
            return
        lastGeneration = ugener.PdGeneration(self.generations.Items[self.generations.Count - 1])
        self.generations.Remove(lastGeneration)
    
    def selectGeneration(self, aGeneration):
        lastFullyVisibleRow = 0
        
        self.selectedRow = self.generations.IndexOf(aGeneration)
        lastFullyVisibleRow = self.plantsDrawGrid.TopRow + self.plantsDrawGrid.VisibleRowCount - 1
        if self.selectedRow > lastFullyVisibleRow:
            self.plantsDrawGrid.TopRow = self.plantsDrawGrid.TopRow + (self.selectedRow - lastFullyVisibleRow)
        if self.selectedRow < self.plantsDrawGrid.TopRow:
            self.plantsDrawGrid.TopRow = self.selectedRow
    
    def deselectAllGenerations(self):
        genCount = 0
        generation = PdGeneration()
        
        self.selectedRow = -1
        for genCount in range(0, self.generations.Count):
            generation = ugener.PdGeneration(self.generations.Items[genCount])
            generation.deselectAllPlants()
    
    def updateForChangeToGenerations(self):
        self.updateMenusForChangeToGenerations()
        self.internalChange = true
        if not self.Visible:
            #calls resize
            self.Show()
        self.BringToFront()
        if self.WindowState == delphi_compatability.TWindowState.wsMinimized:
            self.WindowState = delphi_compatability.TWindowState.wsNormal
        self.internalChange = false
        if self.plantsDrawGrid.RowCount < self.generations.Count:
            self.plantsDrawGrid.RowCount = self.generations.Count
        self.plantsDrawGrid.Invalidate()
        self.plantsDrawGrid.Update()
        self.redoCaption()
        if self.generations.Count <= 0:
            self.emptyWarningPanel.BringToFront()
        else:
            self.emptyWarningPanel.SendToBack()
    
    def updateForChangeToPlant(self, aPlant):
        genCount = 0
        plCount = 0
        generation = PdGeneration()
        plant = PdPlant()
        cellRectOver = TRect()
        
        for genCount in range(0, self.generations.Count):
            generation = ugener.PdGeneration(self.generations.Items[genCount])
            if generation.plants.Count > 0:
                for plCount in range(0, generation.plants.Count):
                    plant = uplant.PdPlant(generation.plants.Items[plCount])
                    if plant == aPlant:
                        cellRectOver = self.plantsDrawGrid.CellRect(plCount + 1, genCount)
                        self.plantsDrawGridDrawCell(self, plCount + 1, genCount, cellRectOver, [UNRESOLVED.gdFocused, UNRESOLVED.gdSelected, ])
                        return
    
    def updateForChangeToSelections(self, selectionIsInFirstColumn):
        i = 0
        plant = PdPlant()
        
        self.updateMenusForChangeToSelection()
        #
        #  if selectedPlants.count > 0 then
        #    for i := 0 to selectedPlants.count - 1 do
        #      begin
        #      plant := PdPlant(selectedPlants.items[i]);
        #      self.updateForChangeToPlant(plant);
        #      end;
        #      
        #if selectionIsInFirstColumn then
        self.plantsDrawGrid.Invalidate()
    
    #
    #procedure TBreederForm.updateForChangeToSelections;
    #  begin
    #  for genCount := 0 to generations.count - 1 do
    #    begin
    #    generation := PdGeneration(generations.items[genCount]);
    #    if generation.plants.count > 0 then for plCount := 0 to generation.plants.count - 1 do
    #      begin
    #      plant := PdPlant(generation.plants.items[plCount]);
    #      if generation.plantWasSelected(plant) then
    #        self.plantsDrawGridDrawCell(self, plCount+1, genCount, plantsDrawGrid.cellRect(plCount+1, genCount), []);
    #      if generation.plantIsSelected(plant) then
    #        self.plantsDrawGridDrawCell(self, plCount+1, genCount, plantsDrawGrid.cellRect(plCount+1, genCount), []);
    #      end;
    #    end;
    #  end;
    #    
    def redoCaption(self):
        if self.generations.Count == 1:
            # new v1.4
            self.Caption = "Breeder (1 generation)"
        else:
            self.Caption = "Breeder (" + IntToStr(self.generations.Count) + " generations)"
        #
        #  self.caption := self.caption + ', numbers ';
        #  case domain.breedingAndTimeSeriesOptions.variationType of
        #    kBreederVariationNoNumeric: self.caption := self.caption + none ;
        #    kBreederVariationLow:     self.caption := self.caption + 'low' ;
        #    kBreederVariationMedium:  self.caption := self.caption + 'medium' ;
        #    kBreederVariationHigh:    self.caption := self.caption + 'high' ;
        #    kBreederVariationCustom:  self.caption := self.caption + 'custom' ;
        #    end;
        #  if domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues then
        #    self.caption := self.caption + ', colors on'
        #  else
        #    self.caption := self.caption + ', colors off'
        #  if domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary then
        #    self.caption := self.caption + ', 3D objects on'
        #  else
        #    self.caption := self.caption + ', 3D objects off'
        #    
    
    def updateMenusForChangeToGenerations(self):
        havePlants = false
        
        havePlants = self.generations.Count > 0
        self.BreederMenuDeleteAll.enabled = havePlants
        self.BreederMenuRandomizeAll.enabled = havePlants
        self.updateMenusForChangeToSelection()
    
    def updateMenusForChangeToSelection(self):
        haveSelection = false
        
        haveSelection = (self.primarySelectedPlant() != None)
        self.BreederMenuRandomize.enabled = haveSelection
        self.BreederMenuDeleteRow.enabled = haveSelection
        self.BreederPopupMenuDeleteRow.enabled = haveSelection
        self.BreederMenuBreed.enabled = haveSelection
        self.BreederMenuMakeTimeSeries.enabled = haveSelection
        self.BreederMenuCopy.enabled = haveSelection
        self.BreederPopupMenuBreed.enabled = self.BreederMenuBreed.enabled
        self.breedButton.Enabled = self.BreederMenuBreed.enabled
        self.BreederPopupMenuMakeTimeSeries.enabled = self.BreederMenuMakeTimeSeries.enabled
        self.BreederPopupMenuCopy.enabled = self.BreederMenuCopy.enabled
        self.BreederPopupMenuRandomize.enabled = self.BreederMenuRandomize.enabled
        self.updatePasteMenuForClipboardContents()
        # must paste onto a selected plant 
        self.BreederMenuPaste.enabled = self.BreederMenuPaste.enabled and haveSelection
        self.BreederPopupMenuPaste.enabled = self.BreederMenuPaste.enabled
    
    def updatePasteMenuForClipboardContents(self):
        self.BreederMenuPaste.enabled = (self.primarySelectedPlant() != None) and (udomain.domain.plantManager.privatePlantClipboard.Count > 0)
        self.BreederPopupMenuPaste.enabled = self.BreederMenuPaste.enabled
    
    def selectedGeneration(self):
        result = PdGeneration()
        result = None
        if (self.selectedRow < 0) or (self.selectedRow > self.generations.Count - 1):
            return result
        result = ugener.PdGeneration(self.generations.Items[self.selectedRow])
        return result
    
    def primarySelectedPlant(self):
        result = PdPlant()
        generation = PdGeneration()
        
        result = None
        generation = self.selectedGeneration()
        if generation == None:
            return result
        result = generation.firstSelectedPlant()
        return result
    
    def plantAtMouse(self, x, y):
        result = PdPlant()
        col = 0L
        row = 0L
        
        result = None
        col, row = self.plantsDrawGrid.MouseToCell(x, y, col, row)
        if not self.inGrid(row, col):
            return result
        result = self.plantForRowAndColumn(row, col)
        return result
    
    # ----------------------------------------------------------------------------- menu 
    def BreederMenuUndoClick(self, Sender):
        umain.MainForm.MenuEditUndoClick(Sender)
    
    def BreederMenuRedoClick(self, Sender):
        umain.MainForm.MenuEditRedoClick(Sender)
    
    def BreederMenuCopyClick(self, Sender):
        plant = PdPlant()
        copyList = TList()
        saveName = ""
        
        plant = self.primarySelectedPlant()
        if plant == None:
            return
        copyList = delphi_compatability.TList().Create()
        copyList.Add(plant)
        # temporarily change plant name to make copy, then put back 
        saveName = plant.getName()
        self.numBreederPlantsCopiedThisSession += 1
        plant.setName("Breeder plant " + IntToStr(self.numBreederPlantsCopiedThisSession))
        udomain.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(copyList)
        plant.setName(saveName)
        #sets our paste menu also
        umain.MainForm.updatePasteMenuForClipboardContents()
    
    def BreederMenuSendCopyToMainWindowClick(self, Sender):
        self.BreederMenuCopyClick(self)
        umain.MainForm.MenuEditPasteClick(umain.MainForm)
    
    def BreederMenuUndoRedoListClick(self, Sender):
        umain.MainForm.UndoMenuEditUndoRedoListClick(umain.MainForm)
    
    def BreederMenuPasteClick(self, Sender):
        generation = PdGeneration()
        plant = PdPlant()
        newPlant = PdPlant()
        newCommand = PdCommand()
        column = 0
        
        if udomain.domain.plantManager.privatePlantClipboard.Count <= 0:
            return
        generation = self.selectedGeneration()
        if generation == None:
            return
        plant = generation.firstSelectedPlant()
        if plant == None:
            return
        column = generation.plants.IndexOf(plant) + 1
        newPlant = uplant.PdPlant().create()
        udomain.domain.plantManager.pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant)
        newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(newPlant, self.selectedRow, column)
        umain.MainForm.doCommand(newCommand)
        #command will free plant if paste is undone
    
    def BreederMenuBreedClick(self, Sender):
        generationToBreed = PdGeneration()
        newCommand = PdCommand()
        
        if (self.selectedRow < 0) or (self.selectedRow > self.generations.Count - 1):
            return
        if self.selectedRow >= udomain.domain.breedingAndTimeSeriesOptions.maxGenerations - 1:
            # check if there is room in the breeder - this command will make one new generation 
            self.fullWarning()
            return
        generationToBreed = ugener.PdGeneration(self.generations.Items[self.selectedRow])
        if generationToBreed.selectedPlants.Count <= 0:
            return
        newCommand = updcom.PdBreedFromParentsCommand().createWithInfo(self.generations, generationToBreed.firstSelectedPlant(), generationToBreed.secondSelectedPlant(), self.selectedRow, udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, updcom.kDontCreateFirstGeneration)
        generationToBreed.firstParent = generationToBreed.firstSelectedPlant()
        generationToBreed.secondParent = generationToBreed.secondSelectedPlant()
        umain.MainForm.doCommand(newCommand)
    
    def BreederMenuMakeTimeSeriesClick(self, Sender):
        newCommand = PdCommand()
        
        if self.primarySelectedPlant() == None:
            return
        newCommand = updcom.PdMakeTimeSeriesCommand().createWithNewPlant(self.primarySelectedPlant())
        umain.MainForm.doCommand(newCommand)
    
    def fullWarning(self):
        MessageDialog("The breeder is full. " + chr(13) + chr(13) + "You must delete some rows" + chr(13) + "(or increase the number of rows allowed in the breeder options) " + chr(13) + "before you can breed more plants.", mtWarning, [mbOK, ], 0)
    
    def BreederMenuDeleteRowClick(self, Sender):
        newCommand = PdCommand()
        
        if self.selectedGeneration() == None:
            return
        newCommand = updcom.PdDeleteBreederGenerationCommand().createWithGeneration(self.selectedGeneration())
        umain.MainForm.doCommand(newCommand)
    
    def BreederMenuDeleteAllClick(self, Sender):
        newCommand = PdCommand()
        
        if self.generations.Count <= 0:
            return
        newCommand = updcom.PdDeleteAllBreederGenerationsCommand().create()
        umain.MainForm.doCommand(newCommand)
    
    def BreederMenuRandomizeClick(self, Sender):
        newCommand = PdCommand()
        randomizeList = TList()
        aGeneration = PdGeneration()
        i = 0
        plant = PdPlant()
        
        aGeneration = self.selectedGeneration()
        if aGeneration == None:
            return
        if aGeneration.selectedPlants.Count <= 0:
            return
        randomizeList = delphi_compatability.TList().Create()
        try:
            for i in range(0, aGeneration.selectedPlants.Count):
                plant = uplant.PdPlant(aGeneration.selectedPlants.Items[i])
                randomizeList.Add(plant)
            newCommand = updcom.PdRandomizeCommand().createWithListOfPlants(randomizeList)
            (newCommand as updcom.PdRandomizeCommand).isInBreeder = true
            ucursor.cursor_startWait()
            umain.MainForm.doCommand(newCommand)
        finally:
            #command has another list, so we must free this one
            randomizeList.free
            ucursor.cursor_stopWait()
    
    def BreederMenuRandomizeAllClick(self, Sender):
        generation = PdGeneration()
        i = 0
        j = 0
        newCommand = PdCommand()
        randomizeList = TList()
        
        if self.generations.Count <= 0:
            return
        randomizeList = None
        try:
            ucursor.cursor_startWait()
            randomizeList = delphi_compatability.TList().Create()
            if self.generations.Count > 0:
                for i in range(0, self.generations.Count):
                    generation = ugener.PdGeneration(self.generations.Items[i])
                    if generation.plants.Count > 0:
                        for j in range(0, generation.plants.Count):
                            randomizeList.Add(uplant.PdPlant(generation.plants.Items[j]))
            newCommand = updcom.PdRandomizeCommand().createWithListOfPlants(randomizeList)
            (newCommand as updcom.PdRandomizeCommand).isInBreeder = true
            (newCommand as updcom.PdRandomizeCommand).isRandomizeAllInBreeder = true
            umain.MainForm.doCommand(newCommand)
        finally:
            randomizeList.free
            ucursor.cursor_stopWait()
    
    def BreederMenuVariationNoneClick(self, Sender):
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationNoNumeric
        self.BreederMenuVariationNone.checked = true
        self.redoCaption()
    
    def BreederMenuVariationLowClick(self, Sender):
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationLow
        self.BreederMenuVariationLow.checked = true
        self.redoCaption()
    
    def BreederMenuVariationMediumClick(self, Sender):
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationMedium
        self.BreederMenuVariationMedium.checked = true
        self.redoCaption()
    
    def BreederMenuVariationHighClick(self, Sender):
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationHigh
        # this is to deal with if it was turned off by not having a library
        # v2.0 removed - this is separate now
        # domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary := true;
        self.BreederMenuVariationHigh.checked = true
        self.redoCaption()
    
    def BreederMenuVariationCustomClick(self, Sender):
        self.changeBreederAndTimeSeriesOptions(kOptionTabMutation)
    
    def BreederMenuOtherOptionsClick(self, Sender):
        self.changeBreederAndTimeSeriesOptions(kOptionTabSize)
    
    def BreederMenuVaryColorsClick(self, Sender):
        newCommand = PdCommand()
        options = BreedingAndTimeSeriesOptionsStructure()
        
        self.BreederMenuVaryColors.checked = not self.BreederMenuVaryColors.checked
        options = udomain.domain.breedingAndTimeSeriesOptions
        options.mutateAndBlendColorValues = self.BreederMenuVaryColors.checked
        newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(options, udomain.domain.options)
        umain.MainForm.doCommand(newCommand)
    
    def BreederMenuVary3DObjectsClick(self, Sender):
        newCommand = PdCommand()
        options = BreedingAndTimeSeriesOptionsStructure()
        
        self.BreederMenuVary3DObjects.checked = not self.BreederMenuVary3DObjects.checked
        options = udomain.domain.breedingAndTimeSeriesOptions
        options.chooseTdosRandomlyFromCurrentLibrary = self.BreederMenuVary3DObjects.checked
        newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(options, udomain.domain.options)
        umain.MainForm.doCommand(newCommand)
    
    def changeBreederAndTimeSeriesOptions(self, tabIndexToShow):
        optionsForm = TBreedingOptionsForm()
        newCommand = PdCommand()
        domainCommand = PdCommand()
        response = 0
        
        if tabIndexToShow == kOptionTabMutation:
            udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationCustom
            self.BreederMenuVariationCustom.checked = true
            self.redoCaption()
        optionsForm = ubrdopt.TBreedingOptionsForm().create(self)
        if optionsForm == None:
            raise GeneralException.create("Problem: Could not create breeding options window.")
        try:
            optionsForm.breedingOptions.pageIndex = tabIndexToShow
            optionsForm.initializeWithBreedingAndTimeSeriesOptionsAndDomainOptions(udomain.domain.breedingAndTimeSeriesOptions, udomain.domain.options)
            response = optionsForm.ShowModal()
            if response == mrOK:
                newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(optionsForm.options, optionsForm.domainOptions)
                umain.MainForm.doCommand(newCommand)
        finally:
            optionsForm.free
            optionsForm = None
    
    def variationLowClick(self, Sender):
        self.BreederMenuVariationLowClick(self)
    
    def variationNoneNumericClick(self, Sender):
        self.BreederMenuVariationNoneClick(self)
    
    def variationMediumClick(self, Sender):
        self.BreederMenuVariationMediumClick(self)
    
    def variationHighClick(self, Sender):
        self.BreederMenuVariationHighClick(self)
    
    def variationCustomClick(self, Sender):
        self.BreederMenuVariationCustomClick(self)
    
    def varyColorsClick(self, Sender):
        self.BreederMenuVaryColorsClick(self)
    
    def vary3DObjectsClick(self, Sender):
        self.BreederMenuVary3DObjectsClick(self)
    
    def BreederPopupMenuRandomizeClick(self, Sender):
        self.BreederMenuRandomizeClick(self)
    
    def BreederPopupMenuBreedClick(self, Sender):
        self.BreederMenuBreedClick(self)
    
    def breedButtonClick(self, Sender):
        self.BreederMenuBreedClick(self)
    
    def BreederPopupMenuMakeTimeSeriesClick(self, Sender):
        self.BreederMenuMakeTimeSeriesClick(self)
    
    def BreederPopupMenuCopyClick(self, Sender):
        self.BreederMenuCopyClick(self)
    
    def BreederPopupMenuPasteClick(self, Sender):
        self.BreederMenuPasteClick(self)
    
    def BreederPopupMenuSendCopytoMainWindowClick(self, Sender):
        self.BreederMenuSendCopyToMainWindowClick(self)
    
    def BreederPopupMenuDeleteRowClick(self, Sender):
        self.BreederMenuDeleteRowClick(self)
    
    # --------------------------------------------------------------------------- utilities 
    def inGrid(self, row, column):
        result = false
        result = true
        if (row < 0) or (row > self.generations.Count - 1):
            result = false
        if (column < 1) or (column - 1 > self.plantsDrawGrid.ColCount - 1):
            result = false
        return result
    
    def generationForIndex(self, index):
        result = PdGeneration()
        result = None
        if index < 0:
            return result
        if index > self.generations.Count - 1:
            return result
        if self.generations.Items[index] == None:
            return result
        result = ugener.PdGeneration(self.generations.Items[index])
        return result
    
    def plantForRowAndColumn(self, row, column):
        result = PdPlant()
        generation = PdGeneration()
        
        result = None
        generation = self.generationForIndex(row)
        if generation == None:
            return result
        result = generation.plantForIndex(column - 1)
        return result
    
    # ---------------------------------------------------------------------------- resizing 
    def FormResize(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        if self.generations == None:
            return
        self.breederToolbarPanel.SetBounds(0, 0, self.ClientWidth, self.breederToolbarPanel.Height)
        self.helpButton.SetBounds(self.breederToolbarPanel.Width - self.helpButton.Width - 4, self.helpButton.Top, self.helpButton.Width, self.helpButton.Height)
        self.plantsDrawGrid.SetBounds(0, self.breederToolbarPanel.Height, self.ClientWidth, self.ClientHeight - self.breederToolbarPanel.Height)
        self.emptyWarningPanel.SetBounds(self.ClientWidth / 2 - self.emptyWarningPanel.Width / 2, self.ClientHeight / 2 - self.emptyWarningPanel.Height / 2, self.emptyWarningPanel.Width, self.emptyWarningPanel.Height)
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 250
        UNRESOLVED.ptMinTrackSize.y = 150
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Breeding_plants_using_the_breeder")
    
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
            if (UNRESOLVED.realizePalette(DC) != 0) and (not delphi_compatability.Application.terminated) and (self.plantsDrawGrid != None):
                # if palette changed, repaint drawing 
                self.plantsDrawGrid.Invalidate()
            UNRESOLVED.selectPalette(DC, oldPalette, true)
            UNRESOLVED.realizePalette(DC)
            UNRESOLVED.releaseDC(windowHandle, DC)
        result = PdForm.PaletteChanged(self, Foreground)
        return result
    
    def BreederMenuHelpOnBreedingClick(self, Sender):
        delphi_compatability.Application.HelpJump("Breeding_plants_using_the_breeder")
    
    def BreederMenuHelpTopicsClick(self, Sender):
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_FINDER, 0)
    
    def BreederMenuOptionsFastDrawClick(self, Sender):
        umain.MainForm.MenuOptionsFastDrawClick(umain.MainForm)
    
    def BreederMenuOptionsMediumDrawClick(self, Sender):
        umain.MainForm.MenuOptionsMediumDrawClick(umain.MainForm)
    
    def BreederMenuOptionsBestDrawClick(self, Sender):
        umain.MainForm.MenuOptionsBestDrawClick(umain.MainForm)
    
    def BreederMenuOptionsCustomDrawClick(self, Sender):
        umain.MainForm.MenuOptionsCustomDrawClick(umain.MainForm)
    
