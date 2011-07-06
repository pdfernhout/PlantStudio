// unit Ubreedr

from conversion_common import *;
import updcom;
import ucommand;
import umain;
import umath;
import usupport;
import ubrdopt;
import udomain;
import ugener;
import uplant;
import ucollect;
import delphi_compatability;

// var
TBreederForm BreederForm = new TBreederForm();


// const
kRedrawPlants = true;
kDontRedrawPlants = false;
kConsiderIfPreviewCacheIsUpToDate = true;
kDontConsiderIfPreviewCacheIsUpToDate = false;


// const
kSelectionIsInFirstColumn = true;
kSelectionIsNotInFirstColumn = false;
kFirstColumnWidth = 20;
kBetweenGap = 4;
kOptionTabSize = 0;
kOptionTabMutation = 1;
kOptionTabBlending = 2;
kOptionTabNonNumeric = 3;
kOptionTabTdos = 4;



class TBreederForm extends PdForm {
    public TDrawGrid plantsDrawGrid;
    public TMainMenu BreederMenu;
    public TMenuItem BreederMenuEdit;
    public TMenuItem BreederMenuCopy;
    public TMenuItem BreederMenuPaste;
    public TMenuItem N2;
    public TMenuItem BreederMenuPlant;
    public TMenuItem BreederMenuBreed;
    public TMenuItem BreederMenuUndo;
    public TMenuItem BreederMenuRedo;
    public TMenuItem N1;
    public TMenuItem BreederMenuDeleteRow;
    public TMenuItem BreederMenuDeleteAll;
    public TPopupMenu BreederPopupMenu;
    public TMenuItem BreederPopupMenuBreed;
    public TMenuItem BreederPopupMenuCopy;
    public TMenuItem BreederPopupMenuPaste;
    public TMenuItem BreederPopupMenuDeleteRow;
    public TMenuItem N4;
    public TMenuItem BreederMenuRandomize;
    public TMenuItem BreederMenuRandomizeAll;
    public TMenuItem BreederMenuMakeTimeSeries;
    public TMenuItem BreederPopupMenuRandomize;
    public TMenuItem N5;
    public TPanel emptyWarningPanel;
    public TLabel Label1;
    public TMenuItem BreederPopupMenuMakeTimeSeries;
    public TMenuItem BreederMenuVariation;
    public TMenuItem BreederMenuVariationLow;
    public TMenuItem BreederMenuVariationMedium;
    public TMenuItem BreederMenuVariationHigh;
    public TMenuItem BreederMenuVariationCustom;
    public TMenuItem BreederMenuOptions;
    public TMenuItem BreederMenuOtherOptions;
    public TMenuItem MenuBreederHelp;
    public TMenuItem BreederMenuHelpOnBreeding;
    public TMenuItem BreederMenuHelpTopics;
    public TMenuItem N3;
    public TMenuItem BreederMenuOptionsDrawAs;
    public TMenuItem BreederMenuOptionsFastDraw;
    public TMenuItem BreederMenuOptionsMediumDraw;
    public TMenuItem BreederMenuOptionsBestDraw;
    public TMenuItem BreederMenuOptionsCustomDraw;
    public TMenuItem N6;
    public TMenuItem BreederMenuVaryColors;
    public TMenuItem BreederMenuVary3DObjects;
    public TPanel breederToolbarPanel;
    public TSpeedButton variationLow;
    public TSpeedButton variationMedium;
    public TSpeedButton variationCustom;
    public TSpeedButton varyColors;
    public TSpeedButton vary3DObjects;
    public TSpeedButton helpButton;
    public TSpeedButton variationHigh;
    public TMenuItem BreederMenuVariationNone;
    public TSpeedButton variationNoneNumeric;
    public TMenuItem BreederMenuSendCopyToMainWindow;
    public TMenuItem N7;
    public TMenuItem BreederPopupMenuSendCopytoMainWindow;
    public TMenuItem N8;
    public TSpeedButton breedButton;
    public TMenuItem BreederMenuUndoRedoList;
    public short selectedRow;
    public TListCollection generations;
    public TPoint dragPlantStartPoint;
    public TPoint lightUpCell;
    public long numBreederPlantsCopiedThisSession;
    public boolean internalChange;
    public boolean drawing;
    public boolean needToRedrawFromChangeToDrawOptions;
    
    //$R *.DFM
    // ---------------------------------------------------------------------------- creation/destruction 
    public void FormCreate(TObject Sender) {
        TRect tempBoundsRect = new TRect();
        
        this.generations = ucollect.TListCollection().Create();
        this.plantsDrawGrid.DragCursor = UNRESOLVED.crDragPlant;
        this.position = delphi_compatability.TPosition.poDesigned;
        // keep window on screen - left corner of title bar 
        tempBoundsRect = udomain.domain.breederWindowRect;
        if ((tempBoundsRect.Left != 0) || (tempBoundsRect.Right != 0) || (tempBoundsRect.Top != 0) || (tempBoundsRect.Bottom != 0)) {
            if (tempBoundsRect.Left > delphi_compatability.Screen.Width - umain.kMinWidthOnScreen) {
                tempBoundsRect.Left = delphi_compatability.Screen.Width - umain.kMinWidthOnScreen;
            }
            if (tempBoundsRect.Top > delphi_compatability.Screen.Height - umain.kMinHeightOnScreen) {
                tempBoundsRect.Top = delphi_compatability.Screen.Height - umain.kMinHeightOnScreen;
            }
            this.setBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom);
        }
        switch (udomain.domain.options.drawSpeed) {
            case udomain.kDrawFast:
                this.BreederMenuOptionsFastDraw.checked = true;
                break;
            case udomain.kDrawMedium:
                this.BreederMenuOptionsMediumDraw.checked = true;
                break;
            case udomain.kDrawBest:
                this.BreederMenuOptionsBestDraw.checked = true;
                break;
            case udomain.kDrawCustom:
                this.BreederMenuOptionsCustomDraw.checked = true;
                break;
        this.updateForChangeToDomainOptions();
        this.updateMenusForChangeToGenerations();
        //to get redo messages
        umain.MainForm.updateMenusForUndoRedo();
        this.lightUpCell = Point(-1, -1);
        this.emptyWarningPanel.SendToBack();
    }
    
    public void FormDestroy(TObject Sender) {
        this.generations.free;
        this.generations = null;
    }
    
    public void FormActivate(TObject Sender) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.generations.Count <= 0) {
            this.emptyWarningPanel.BringToFront();
        } else if (this.needToRedrawFromChangeToDrawOptions) {
            this.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate);
            this.needToRedrawFromChangeToDrawOptions = false;
        }
    }
    
    // -------------------------------------------------------------------------------------- grid 
    public void updateForChangeToDomainOptions() {
        PdGeneration generation = new PdGeneration();
        PdPlant plant = new PdPlant();
        short genCount = 0;
        short plCount = 0;
        int newAge = 0;
        boolean atLeastOnePlantHasChangedAge = false;
        
        if (this.plantsDrawGrid.ColCount != udomain.domain.breedingAndTimeSeriesOptions.plantsPerGeneration + 1) {
            this.plantsDrawGrid.ColCount = udomain.domain.breedingAndTimeSeriesOptions.plantsPerGeneration + 1;
        }
        if (((this.plantsDrawGrid.DefaultColWidth != udomain.domain.breedingAndTimeSeriesOptions.thumbnailWidth) || (this.plantsDrawGrid.DefaultRowHeight != udomain.domain.breedingAndTimeSeriesOptions.thumbnailHeight))) {
            this.plantsDrawGrid.DefaultColWidth = udomain.domain.breedingAndTimeSeriesOptions.thumbnailWidth;
            this.plantsDrawGrid.ColWidths[0] = kFirstColumnWidth;
            this.plantsDrawGrid.DefaultRowHeight = udomain.domain.breedingAndTimeSeriesOptions.thumbnailHeight;
            this.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate);
        }
        switch (udomain.domain.breedingAndTimeSeriesOptions.variationType) {
            case udomain.kBreederVariationLow:
                this.BreederMenuVariationLow.checked = true;
                this.variationLow.Down = true;
                break;
            case udomain.kBreederVariationMedium:
                this.BreederMenuVariationMedium.checked = true;
                this.variationMedium.Down = true;
                break;
            case udomain.kBreederVariationHigh:
                this.BreederMenuVariationHigh.checked = true;
                this.variationHigh.Down = true;
                break;
            case udomain.kBreederVariationCustom:
                this.BreederMenuVariationCustom.checked = true;
                this.variationCustom.Down = true;
                break;
            case udomain.kBreederVariationNoNumeric:
                this.BreederMenuVariationNone.checked = true;
                this.variationNoneNumeric.Down = true;
                break;
        this.BreederMenuVaryColors.checked = udomain.domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues;
        this.varyColors.Down = udomain.domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues;
        this.BreederMenuVary3DObjects.checked = udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary;
        this.vary3DObjects.Down = udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary;
        this.redoCaption();
        atLeastOnePlantHasChangedAge = false;
        if (this.generations.Count > 0) {
            for (genCount = 0; genCount <= this.generations.Count - 1; genCount++) {
                generation = ugener.PdGeneration(this.generations.Items[genCount]);
                if (generation.plants.Count > 0) {
                    for (plCount = 0; plCount <= generation.plants.Count - 1; plCount++) {
                        plant = uplant.PdPlant(generation.plants.Items[plCount]);
                        newAge = intround(udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0 * plant.pGeneral.ageAtMaturity);
                        if (plant.age != newAge) {
                            plant.setAge(newAge);
                            atLeastOnePlantHasChangedAge = true;
                        }
                    }
                }
            }
        }
        if (atLeastOnePlantHasChangedAge) {
            this.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate);
        }
    }
    
    public void redrawPlants(boolean considerIfPreviewCacheIsUpToDate) {
        PdGeneration generation = new PdGeneration();
        PdPlant plant = new PdPlant();
        short genCount = 0;
        short plCount = 0;
        
        if (!considerIfPreviewCacheIsUpToDate) {
            for (genCount = 0; genCount <= this.generations.Count - 1; genCount++) {
                generation = ugener.PdGeneration(this.generations.Items[genCount]);
                if (generation.plants.Count > 0) {
                    for (plCount = 0; plCount <= generation.plants.Count - 1; plCount++) {
                        plant = uplant.PdPlant(generation.plants.Items[plCount]);
                        plant.previewCacheUpToDate = false;
                    }
                }
            }
        }
        this.plantsDrawGrid.Invalidate();
        this.plantsDrawGrid.Update();
    }
    
    public void plantsDrawGridDrawCell(TObject Sender, long Col, long Row, TRect Rect, TGridDrawState State) {
        PdGeneration generation = new PdGeneration();
        PdPlant plant = new PdPlant();
        TRect textDrawRect = new TRect();
        
        try {
            this.plantsDrawGrid.Canvas.Font = this.plantsDrawGrid.Font;
            this.plantsDrawGrid.Canvas.Font.Color = delphi_compatability.clBlack;
            if (Col == 0) {
                //if (row = selectedRow) and (generations.count > 0) then
                //plantsDrawGrid.canvas.brush.color := clBlue
                //else
                this.plantsDrawGrid.Canvas.Brush.Color = delphi_compatability.clWhite;
                this.plantsDrawGrid.Canvas.Pen.Color = this.plantsDrawGrid.Canvas.Brush.Color;
                this.plantsDrawGrid.Canvas.Rectangle(Rect.left, Rect.top, Rect.right, Rect.bottom);
                if (Row > this.generations.Count - 1) {
                    return;
                }
                //if row = selectedRow then
                //plantsDrawGrid.canvas.font.color := clWhite;
                textDrawRect.Left = Rect.left + usupport.rWidth(Rect) / 2 - this.plantsDrawGrid.Canvas.TextWidth(IntToStr(Row + 1)) / 2;
                textDrawRect.Top = Rect.top + usupport.rHeight(Rect) / 2 - this.plantsDrawGrid.Canvas.TextHeight("0") / 2;
                this.plantsDrawGrid.Canvas.TextOut(textDrawRect.Left, textDrawRect.Top, IntToStr(Row + 1));
                return;
            } else {
                this.plantsDrawGrid.Canvas.Brush.Color = delphi_compatability.clWhite;
                this.plantsDrawGrid.Canvas.Pen.Width = 1;
                this.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clWhite;
                this.plantsDrawGrid.Canvas.Rectangle(Rect.left, Rect.top, Rect.right, Rect.bottom);
            }
            generation = null;
            generation = this.generationForIndex(Row);
            if (generation == null) {
                return;
            }
            plant = null;
            plant = generation.plantForIndex(Col - 1);
            if (plant == null) {
                return;
            }
            if (!plant.previewCacheUpToDate) {
                // draw plant 
                // draw gray solid box to show delay for drawing plant cache
                this.plantsDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
                this.plantsDrawGrid.Canvas.Brush.Color = delphi_compatability.clSilver;
                this.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clSilver;
                //FIX unresolved WITH expression: Rect
                this.plantsDrawGrid.Canvas.Rectangle(UNRESOLVED.left + 1, UNRESOLVED.top + 1, UNRESOLVED.right, UNRESOLVED.bottom);
                // draw plant preview cache
                plant.fixedPreviewScale = false;
                plant.fixedDrawPosition = false;
                plant.drawPreviewIntoCache(Point(this.plantsDrawGrid.DefaultColWidth, this.plantsDrawGrid.DefaultRowHeight), uplant.kDontConsiderDomainScale, umain.kDrawNow);
            }
            plant.previewCache.Transparent = false;
            UNRESOLVED.copyBitmapToCanvasWithGlobalPalette(plant.previewCache, this.plantsDrawGrid.Canvas, Rect);
            // draw selection rectangle 
            this.plantsDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
            this.plantsDrawGrid.Canvas.Pen.Width = 2;
            if ((Col == this.lightUpCell.X) && (Row == this.lightUpCell.Y)) {
                this.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clAqua;
            } else if (Row == this.selectedRow) {
                if (plant == generation.firstSelectedPlant()) {
                    this.plantsDrawGrid.Canvas.Pen.Color = udomain.domain.options.firstSelectionRectangleColor;
                } else if (plant == generation.secondSelectedPlant()) {
                    this.plantsDrawGrid.Canvas.Pen.Color = udomain.domain.options.multiSelectionRectangleColor;
                } else {
                    this.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clSilver;
                }
            } else {
                this.plantsDrawGrid.Canvas.Pen.Color = delphi_compatability.clSilver;
            }
            //FIX unresolved WITH expression: Rect
            this.plantsDrawGrid.Canvas.Rectangle(UNRESOLVED.left + 1, UNRESOLVED.top + 1, UNRESOLVED.right, UNRESOLVED.bottom);
            if (plant == generation.firstParent) {
                // draw parent indicator 
                this.plantsDrawGrid.Canvas.TextOut(Rect.left + 4, Rect.top + 2, "p1");
            } else if (plant == generation.secondParent) {
                this.plantsDrawGrid.Canvas.TextOut(Rect.left + 4, Rect.top + 2, "p2");
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void invalidateGridCell(long column, long row) {
        TRect cellRectOver = new TRect();
        
        if ((column < 0) && (row < 0)) {
            return;
        }
        cellRectOver = this.plantsDrawGrid.CellRect(column, row);
        UNRESOLVED.invalidateRect(this.plantsDrawGrid.Handle, cellRectOver, true);
    }
    
    public void invalidateGridRow(long row) {
        TRect rowRectOver = new TRect();
        
        if (row < 0) {
            return;
        }
        rowRectOver = this.plantsDrawGrid.CellRect(0, row);
        rowRectOver.Right = this.plantsDrawGrid.Width;
        UNRESOLVED.invalidateRect(this.plantsDrawGrid.Handle, rowRectOver, true);
    }
    
    public void plantsDrawGridMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        long col = 0;
        long row = 0;
        PdGeneration generation = new PdGeneration();
        PdPlant plant = new PdPlant();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        // had selection here, moved to mouse down because double-click makes extra mouse up, seems okay so far
    }
    
    public void plantsDrawGridDblClick(TObject Sender) {
        this.BreederMenuBreedClick(this);
    }
    
    // ------------------------------------------------------------------------ dragging 
    public void plantsDrawGridMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        PdPlant plant = new PdPlant();
        int col = 0;
        int row = 0;
        int oldSelectedRow = 0;
        PdGeneration generation = new PdGeneration();
        
        col, row = this.plantsDrawGrid.MouseToCell(X, Y, col, row);
        if ((row >= 0) && (row <= this.generations.Count - 1)) {
            generation = ugener.PdGeneration(this.generations.Items[row]);
            if (generation != null) {
                this.selectGeneration(generation);
                if ((col >= 1) && (col - 1 <= generation.plants.Count - 1)) {
                    plant = uplant.PdPlant(generation.plants.Items[col - 1]);
                    if (plant != null) {
                        generation.selectPlant(plant, (delphi_compatability.TShiftStateEnum.ssShift in Shift));
                    } else {
                        generation.deselectAllPlants();
                    }
                    // in first column or past them on right 
                } else {
                    generation.deselectAllPlants();
                }
            } else {
                this.deselectAllGenerations();
            }
        } else {
            this.deselectAllGenerations();
        }
        this.updateForChangeToGenerations();
        if ((Button == delphi_compatability.TMouseButton.mbRight) || (delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
            // start drag of plant
            return;
        }
        plant = this.plantAtMouse(X, Y);
        if (plant == null) {
            return;
        }
        this.dragPlantStartPoint = Point(X, Y);
        this.plantsDrawGrid.BeginDrag(false);
    }
    
    public void plantsDrawGridDragOver(TObject Sender, TObject Source, int X, int Y, TDragState State, boolean Accept) {
        long col = 0;
        long row = 0;
        PdPlant plant = new PdPlant();
        
        Accept = (Source != null) && (Sender != null) && ((Sender == Source) || (Source == umain.MainForm.drawingPaintBox) || (Source == umain.MainForm.plantListDrawGrid) || (Source == UNRESOLVED.TimeSeriesForm.grid));
        if ((Accept)) {
            plant = this.plantAtMouse(X, Y);
            if (plant == null) {
                Accept = false;
                return Accept;
            }
            col, row = this.plantsDrawGrid.MouseToCell(X, Y, col, row);
            if ((col != this.lightUpCell.X) || (row != this.lightUpCell.Y)) {
                this.invalidateGridCell(this.lightUpCell.X, this.lightUpCell.Y);
                this.lightUpCell = Point(col, row);
                this.invalidateGridCell(col, row);
            }
        }
        return Accept;
    }
    
    public void plantsDrawGridEndDrag(TObject Sender, TObject Target, int X, int Y) {
        long col = 0;
        long row = 0;
        PdPlant plant = new PdPlant();
        PdPlant plantToReplace = new PdPlant();
        PdCommand newCommand = new PdCommand();
        TList newPlants = new TList();
        PdPlant newPlant = new PdPlant();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        // remove lightup on cell before resetting cell
        this.invalidateGridCell(this.lightUpCell.X, this.lightUpCell.Y);
        this.lightUpCell = Point(-1, -1);
        if (Target == null) {
            return;
        }
        // get plant being dragged 
        plant = this.plantAtMouse(this.dragPlantStartPoint.X, this.dragPlantStartPoint.Y);
        if (plant == null) {
            return;
        }
        if ((Target == umain.MainForm.drawingPaintBox) || (Target == umain.MainForm.plantListDrawGrid)) {
            // make paste command - wants list of plants 
            newPlant = uplant.PdPlant().create();
            plant.copyTo(newPlant);
            this.numBreederPlantsCopiedThisSession += 1;
            newPlant.setName("Breeder plant " + IntToStr(this.numBreederPlantsCopiedThisSession));
            if ((Target == umain.MainForm.drawingPaintBox)) {
                newPlant.moveTo(Point(X, Y));
            } else {
                newPlant.moveTo(umain.MainForm.standardPastePosition());
            }
            if (!udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
                // v2.1
                newPlant.calculateDrawingScaleToLookTheSameWithDomainScale();
            }
            //to save memory - don't need it in main window
            newPlant.shrinkPreviewCache();
            newPlants = delphi_compatability.TList().Create();
            newPlants.Add(newPlant);
            newCommand = updcom.PdPasteCommand().createWithListOfPlantsAndOldSelectedList(newPlants, umain.MainForm.selectedPlants);
            updcom.PdPasteCommand(newCommand).useSpecialPastePosition = true;
            try {
                UNRESOLVED.cursor_startWait;
                umain.MainForm.doCommand(newCommand);
            } finally {
                //command has another list, so we must free this one
                newPlants.free;
                UNRESOLVED.cursor_stopWait;
            }
            //command will free plant if paste is undone
        } else if (Target == UNRESOLVED.TimeSeriesForm.grid) {
            UNRESOLVED.TimeSeriesForm.copyPlantToPoint(plant, X, Y);
        } else if (Target == Sender) {
            // get plant being replaced 
            col, row = this.plantsDrawGrid.MouseToCell(X, Y, col, row);
            if (!this.inGrid(row, col)) {
                return;
            }
            plantToReplace = this.plantForRowAndColumn(row, col);
            if (plantToReplace == null) {
                return;
            }
            if (plantToReplace == plant) {
                return;
            }
            // make replace command 
            newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(plant, row, col);
            try {
                UNRESOLVED.cursor_startWait;
                umain.MainForm.doCommand(newCommand);
            } finally {
                UNRESOLVED.cursor_stopWait;
            }
        }
    }
    
    public void copyPlantToPoint(PdPlant aPlant, int x, int y) {
        long col = 0;
        long row = 0;
        PdPlant plant = new PdPlant();
        PdCommand newCommand = new PdCommand();
        
        col, row = this.plantsDrawGrid.MouseToCell(x, y, col, row);
        plant = this.plantForRowAndColumn(row, col);
        if (plant == null) {
            return;
        }
        newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(aPlant, row, col);
        umain.MainForm.doCommand(newCommand);
    }
    
    // ------------------------------------------------------------- responding to commands 
    public void replacePlantInRow(PdPlant oldPlant, PdPlant newPlant, short row) {
        PdGeneration generation = new PdGeneration();
        
        generation = this.generationForIndex(row);
        if (generation == null) {
            throw new GeneralException.create("Problem: Invalid row in method TBreederForm.replacePlantInRow.");
        }
        generation.replacePlant(oldPlant, newPlant);
        this.updateForChangeToPlant(newPlant);
    }
    
    public void forgetGenerationsListBelowRow(short aRow) {
        while (this.generations.Count - 1 > aRow) {
            this.forgetLastGeneration();
        }
    }
    
    public void addGenerationsFromListBelowRow(short aRow, TList aGenerationsList) {
        short i = 0;
        
        if (aRow + 1 <= aGenerationsList.Count - 1) {
            for (i = aRow + 1; i <= aGenerationsList.Count - 1; i++) {
                this.addGeneration(ugener.PdGeneration(aGenerationsList.Items[i]));
            }
        }
    }
    
    public void addGeneration(PdGeneration newGeneration) {
        this.generations.Add(newGeneration);
    }
    
    public void forgetLastGeneration() {
        PdGeneration lastGeneration = new PdGeneration();
        
        if (this.generations.Count <= 0) {
            return;
        }
        lastGeneration = ugener.PdGeneration(this.generations.Items[this.generations.Count - 1]);
        this.generations.Remove(lastGeneration);
    }
    
    public void selectGeneration(PdGeneration aGeneration) {
        short lastFullyVisibleRow = 0;
        
        this.selectedRow = this.generations.IndexOf(aGeneration);
        lastFullyVisibleRow = this.plantsDrawGrid.TopRow + this.plantsDrawGrid.VisibleRowCount - 1;
        if (this.selectedRow > lastFullyVisibleRow) {
            this.plantsDrawGrid.TopRow = this.plantsDrawGrid.TopRow + (this.selectedRow - lastFullyVisibleRow);
        }
        if (this.selectedRow < this.plantsDrawGrid.TopRow) {
            this.plantsDrawGrid.TopRow = this.selectedRow;
        }
    }
    
    public void deselectAllGenerations() {
        int genCount = 0;
        PdGeneration generation = new PdGeneration();
        
        this.selectedRow = -1;
        for (genCount = 0; genCount <= this.generations.Count - 1; genCount++) {
            generation = ugener.PdGeneration(this.generations.Items[genCount]);
            generation.deselectAllPlants();
        }
    }
    
    public void updateForChangeToGenerations() {
        this.updateMenusForChangeToGenerations();
        this.internalChange = true;
        if (!this.visible) {
            //calls resize
            this.show;
        }
        this.bringToFront;
        if (this.windowState == delphi_compatability.TWindowState.wsMinimized) {
            this.windowState = delphi_compatability.TWindowState.wsNormal;
        }
        this.internalChange = false;
        if (this.plantsDrawGrid.RowCount < this.generations.Count) {
            this.plantsDrawGrid.RowCount = this.generations.Count;
        }
        this.plantsDrawGrid.Invalidate();
        this.plantsDrawGrid.Update();
        this.redoCaption();
        if (this.generations.Count <= 0) {
            this.emptyWarningPanel.BringToFront();
        } else {
            this.emptyWarningPanel.SendToBack();
        }
    }
    
    public void updateForChangeToPlant(PdPlant aPlant) {
        int genCount = 0;
        int plCount = 0;
        PdGeneration generation = new PdGeneration();
        PdPlant plant = new PdPlant();
        TRect cellRectOver = new TRect();
        
        for (genCount = 0; genCount <= this.generations.Count - 1; genCount++) {
            generation = ugener.PdGeneration(this.generations.Items[genCount]);
            if (generation.plants.Count > 0) {
                for (plCount = 0; plCount <= generation.plants.Count - 1; plCount++) {
                    plant = uplant.PdPlant(generation.plants.Items[plCount]);
                    if (plant == aPlant) {
                        cellRectOver = this.plantsDrawGrid.CellRect(plCount + 1, genCount);
                        this.plantsDrawGridDrawCell(this, plCount + 1, genCount, cellRectOver, {UNRESOLVED.gdFocused, UNRESOLVED.gdSelected, });
                        return;
                    }
                }
            }
        }
    }
    
    public void updateForChangeToSelections(boolean selectionIsInFirstColumn) {
        int i = 0;
        PdPlant plant = new PdPlant();
        
        this.updateMenusForChangeToSelection();
        //
        //  if selectedPlants.count > 0 then
        //    for i := 0 to selectedPlants.count - 1 do
        //      begin
        //      plant := PdPlant(selectedPlants.items[i]);
        //      self.updateForChangeToPlant(plant);
        //      end;
        //      
        //if selectionIsInFirstColumn then
        this.plantsDrawGrid.Invalidate();
    }
    
    //
    //procedure TBreederForm.updateForChangeToSelections;
    //  begin
    //  for genCount := 0 to generations.count - 1 do
    //    begin
    //    generation := PdGeneration(generations.items[genCount]);
    //    if generation.plants.count > 0 then for plCount := 0 to generation.plants.count - 1 do
    //      begin
    //      plant := PdPlant(generation.plants.items[plCount]);
    //      if generation.plantWasSelected(plant) then
    //        self.plantsDrawGridDrawCell(self, plCount+1, genCount, plantsDrawGrid.cellRect(plCount+1, genCount), []);
    //      if generation.plantIsSelected(plant) then
    //        self.plantsDrawGridDrawCell(self, plCount+1, genCount, plantsDrawGrid.cellRect(plCount+1, genCount), []);
    //      end;
    //    end;
    //  end;
    //    
    public void redoCaption() {
        if (this.generations.Count == 1) {
            // new v1.4
            this.caption = "Breeder (1 generation)";
        } else {
            this.caption = "Breeder (" + IntToStr(this.generations.Count) + " generations)";
        }
        //
        //  self.caption := self.caption + ', numbers ';
        //  case domain.breedingAndTimeSeriesOptions.variationType of
        //    kBreederVariationNoNumeric: self.caption := self.caption + none ;
        //    kBreederVariationLow:     self.caption := self.caption + 'low' ;
        //    kBreederVariationMedium:  self.caption := self.caption + 'medium' ;
        //    kBreederVariationHigh:    self.caption := self.caption + 'high' ;
        //    kBreederVariationCustom:  self.caption := self.caption + 'custom' ;
        //    end;
        //  if domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues then
        //    self.caption := self.caption + ', colors on'
        //  else
        //    self.caption := self.caption + ', colors off'
        //  if domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary then
        //    self.caption := self.caption + ', 3D objects on'
        //  else
        //    self.caption := self.caption + ', 3D objects off'
        //    
    }
    
    public void updateMenusForChangeToGenerations() {
        boolean havePlants = false;
        
        havePlants = this.generations.Count > 0;
        this.BreederMenuDeleteAll.enabled = havePlants;
        this.BreederMenuRandomizeAll.enabled = havePlants;
        this.updateMenusForChangeToSelection();
    }
    
    public void updateMenusForChangeToSelection() {
        boolean haveSelection = false;
        
        haveSelection = (this.primarySelectedPlant() != null);
        this.BreederMenuRandomize.enabled = haveSelection;
        this.BreederMenuDeleteRow.enabled = haveSelection;
        this.BreederPopupMenuDeleteRow.enabled = haveSelection;
        this.BreederMenuBreed.enabled = haveSelection;
        this.BreederMenuMakeTimeSeries.enabled = haveSelection;
        this.BreederMenuCopy.enabled = haveSelection;
        this.BreederPopupMenuBreed.enabled = this.BreederMenuBreed.enabled;
        this.breedButton.Enabled = this.BreederMenuBreed.enabled;
        this.BreederPopupMenuMakeTimeSeries.enabled = this.BreederMenuMakeTimeSeries.enabled;
        this.BreederPopupMenuCopy.enabled = this.BreederMenuCopy.enabled;
        this.BreederPopupMenuRandomize.enabled = this.BreederMenuRandomize.enabled;
        this.updatePasteMenuForClipboardContents();
        // must paste onto a selected plant 
        this.BreederMenuPaste.enabled = this.BreederMenuPaste.enabled && haveSelection;
        this.BreederPopupMenuPaste.enabled = this.BreederMenuPaste.enabled;
    }
    
    public void updatePasteMenuForClipboardContents() {
        this.BreederMenuPaste.enabled = (this.primarySelectedPlant() != null) && (udomain.domain.plantManager.privatePlantClipboard.count > 0);
        this.BreederPopupMenuPaste.enabled = this.BreederMenuPaste.enabled;
    }
    
    public PdGeneration selectedGeneration() {
        result = new PdGeneration();
        result = null;
        if ((this.selectedRow < 0) || (this.selectedRow > this.generations.Count - 1)) {
            return result;
        }
        result = ugener.PdGeneration(this.generations.Items[this.selectedRow]);
        return result;
    }
    
    public PdPlant primarySelectedPlant() {
        result = new PdPlant();
        PdGeneration generation = new PdGeneration();
        
        result = null;
        generation = this.selectedGeneration();
        if (generation == null) {
            return result;
        }
        result = generation.firstSelectedPlant();
        return result;
    }
    
    public PdPlant plantAtMouse(short x, short y) {
        result = new PdPlant();
        long col = 0;
        long row = 0;
        
        result = null;
        col, row = this.plantsDrawGrid.MouseToCell(x, y, col, row);
        if (!this.inGrid(row, col)) {
            return result;
        }
        result = this.plantForRowAndColumn(row, col);
        return result;
    }
    
    // ----------------------------------------------------------------------------- menu 
    public void BreederMenuUndoClick(TObject Sender) {
        umain.MainForm.MenuEditUndoClick(Sender);
    }
    
    public void BreederMenuRedoClick(TObject Sender) {
        umain.MainForm.MenuEditRedoClick(Sender);
    }
    
    public void BreederMenuCopyClick(TObject Sender) {
        PdPlant plant = new PdPlant();
        TList copyList = new TList();
        String saveName = "";
        
        plant = this.primarySelectedPlant();
        if (plant == null) {
            return;
        }
        copyList = delphi_compatability.TList().Create();
        copyList.Add(plant);
        // temporarily change plant name to make copy, then put back 
        saveName = plant.getName();
        this.numBreederPlantsCopiedThisSession += 1;
        plant.setName("Breeder plant " + IntToStr(this.numBreederPlantsCopiedThisSession));
        udomain.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(copyList);
        plant.setName(saveName);
        //sets our paste menu also
        umain.MainForm.updatePasteMenuForClipboardContents();
    }
    
    public void BreederMenuSendCopyToMainWindowClick(TObject Sender) {
        this.BreederMenuCopyClick(this);
        umain.MainForm.MenuEditPasteClick(umain.MainForm);
    }
    
    public void BreederMenuUndoRedoListClick(TObject Sender) {
        umain.MainForm.UndoMenuEditUndoRedoListClick(umain.MainForm);
    }
    
    public void BreederMenuPasteClick(TObject Sender) {
        PdGeneration generation = new PdGeneration();
        PdPlant plant = new PdPlant();
        PdPlant newPlant = new PdPlant();
        PdCommand newCommand = new PdCommand();
        short column = 0;
        
        if (udomain.domain.plantManager.privatePlantClipboard.count <= 0) {
            return;
        }
        generation = this.selectedGeneration();
        if (generation == null) {
            return;
        }
        plant = generation.firstSelectedPlant();
        if (plant == null) {
            return;
        }
        column = generation.plants.IndexOf(plant) + 1;
        newPlant = uplant.PdPlant().create();
        udomain.domain.plantManager.pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant);
        newCommand = updcom.PdReplaceBreederPlant().createWithPlantRowAndColumn(newPlant, this.selectedRow, column);
        umain.MainForm.doCommand(newCommand);
        //command will free plant if paste is undone
    }
    
    public void BreederMenuBreedClick(TObject Sender) {
        PdGeneration generationToBreed = new PdGeneration();
        PdCommand newCommand = new PdCommand();
        
        if ((this.selectedRow < 0) || (this.selectedRow > this.generations.Count - 1)) {
            return;
        }
        if (this.selectedRow >= udomain.domain.breedingAndTimeSeriesOptions.maxGenerations - 1) {
            // check if there is room in the breeder - this command will make one new generation 
            this.fullWarning();
            return;
        }
        generationToBreed = ugener.PdGeneration(this.generations.Items[this.selectedRow]);
        if (generationToBreed.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdBreedFromParentsCommand().createWithInfo(this.generations, generationToBreed.firstSelectedPlant(), generationToBreed.secondSelectedPlant(), this.selectedRow, udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, updcom.kDontCreateFirstGeneration);
        generationToBreed.firstParent = generationToBreed.firstSelectedPlant();
        generationToBreed.secondParent = generationToBreed.secondSelectedPlant();
        umain.MainForm.doCommand(newCommand);
    }
    
    public void BreederMenuMakeTimeSeriesClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.primarySelectedPlant() == null) {
            return;
        }
        newCommand = updcom.PdMakeTimeSeriesCommand().createWithNewPlant(this.primarySelectedPlant());
        umain.MainForm.doCommand(newCommand);
    }
    
    public void fullWarning() {
        MessageDialog("The breeder is full. " + chr(13) + chr(13) + "You must delete some rows" + chr(13) + "(or increase the number of rows allowed in the breeder options) " + chr(13) + "before you can breed more plants.", mtWarning, {mbOK, }, 0);
    }
    
    public void BreederMenuDeleteRowClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedGeneration() == null) {
            return;
        }
        newCommand = updcom.PdDeleteBreederGenerationCommand().createWithGeneration(this.selectedGeneration());
        umain.MainForm.doCommand(newCommand);
    }
    
    public void BreederMenuDeleteAllClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.generations.Count <= 0) {
            return;
        }
        newCommand = updcom.PdDeleteAllBreederGenerationsCommand().create();
        umain.MainForm.doCommand(newCommand);
    }
    
    public void BreederMenuRandomizeClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        TList randomizeList = new TList();
        PdGeneration aGeneration = new PdGeneration();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        aGeneration = this.selectedGeneration();
        if (aGeneration == null) {
            return;
        }
        if (aGeneration.selectedPlants.Count <= 0) {
            return;
        }
        randomizeList = delphi_compatability.TList().Create();
        try {
            for (i = 0; i <= aGeneration.selectedPlants.Count - 1; i++) {
                plant = uplant.PdPlant(aGeneration.selectedPlants.Items[i]);
                randomizeList.Add(plant);
            }
            newCommand = updcom.PdRandomizeCommand().createWithListOfPlants(randomizeList);
            ((updcom.PdRandomizeCommand)newCommand).isInBreeder = true;
            UNRESOLVED.cursor_startWait;
            umain.MainForm.doCommand(newCommand);
        } finally {
            //command has another list, so we must free this one
            randomizeList.free;
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void BreederMenuRandomizeAllClick(TObject Sender) {
        PdGeneration generation = new PdGeneration();
        short i = 0;
        short j = 0;
        PdCommand newCommand = new PdCommand();
        TList randomizeList = new TList();
        
        if (this.generations.Count <= 0) {
            return;
        }
        randomizeList = null;
        try {
            UNRESOLVED.cursor_startWait;
            randomizeList = delphi_compatability.TList().Create();
            if (this.generations.Count > 0) {
                for (i = 0; i <= this.generations.Count - 1; i++) {
                    generation = ugener.PdGeneration(this.generations.Items[i]);
                    if (generation.plants.Count > 0) {
                        for (j = 0; j <= generation.plants.Count - 1; j++) {
                            randomizeList.Add(uplant.PdPlant(generation.plants.Items[j]));
                        }
                    }
                }
            }
            newCommand = updcom.PdRandomizeCommand().createWithListOfPlants(randomizeList);
            ((updcom.PdRandomizeCommand)newCommand).isInBreeder = true;
            ((updcom.PdRandomizeCommand)newCommand).isRandomizeAllInBreeder = true;
            umain.MainForm.doCommand(newCommand);
        } finally {
            randomizeList.free;
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void BreederMenuVariationNoneClick(TObject Sender) {
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationNoNumeric;
        this.BreederMenuVariationNone.checked = true;
        this.redoCaption();
    }
    
    public void BreederMenuVariationLowClick(TObject Sender) {
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationLow;
        this.BreederMenuVariationLow.checked = true;
        this.redoCaption();
    }
    
    public void BreederMenuVariationMediumClick(TObject Sender) {
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationMedium;
        this.BreederMenuVariationMedium.checked = true;
        this.redoCaption();
    }
    
    public void BreederMenuVariationHighClick(TObject Sender) {
        udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationHigh;
        // this is to deal with if it was turned off by not having a library
        // v2.0 removed - this is separate now
        // domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary := true;
        this.BreederMenuVariationHigh.checked = true;
        this.redoCaption();
    }
    
    public void BreederMenuVariationCustomClick(TObject Sender) {
        this.changeBreederAndTimeSeriesOptions(kOptionTabMutation);
    }
    
    public void BreederMenuOtherOptionsClick(TObject Sender) {
        this.changeBreederAndTimeSeriesOptions(kOptionTabSize);
    }
    
    public void BreederMenuVaryColorsClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        BreedingAndTimeSeriesOptionsStructure options = new BreedingAndTimeSeriesOptionsStructure();
        
        this.BreederMenuVaryColors.checked = !this.BreederMenuVaryColors.checked;
        options = udomain.domain.breedingAndTimeSeriesOptions;
        options.mutateAndBlendColorValues = this.BreederMenuVaryColors.checked;
        newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(options, udomain.domain.options);
        umain.MainForm.doCommand(newCommand);
    }
    
    public void BreederMenuVary3DObjectsClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        BreedingAndTimeSeriesOptionsStructure options = new BreedingAndTimeSeriesOptionsStructure();
        
        this.BreederMenuVary3DObjects.checked = !this.BreederMenuVary3DObjects.checked;
        options = udomain.domain.breedingAndTimeSeriesOptions;
        options.chooseTdosRandomlyFromCurrentLibrary = this.BreederMenuVary3DObjects.checked;
        newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(options, udomain.domain.options);
        umain.MainForm.doCommand(newCommand);
    }
    
    public void changeBreederAndTimeSeriesOptions(short tabIndexToShow) {
        TBreedingOptionsForm optionsForm = new TBreedingOptionsForm();
        PdCommand newCommand = new PdCommand();
        PdCommand domainCommand = new PdCommand();
        int response = 0;
        
        if (tabIndexToShow == kOptionTabMutation) {
            udomain.domain.breedingAndTimeSeriesOptions.variationType = udomain.kBreederVariationCustom;
            this.BreederMenuVariationCustom.checked = true;
            this.redoCaption();
        }
        optionsForm = ubrdopt.TBreedingOptionsForm.create(this);
        if (optionsForm == null) {
            throw new GeneralException.create("Problem: Could not create breeding options window.");
        }
        try {
            optionsForm.breedingOptions.pageIndex = tabIndexToShow;
            optionsForm.initializeWithBreedingAndTimeSeriesOptionsAndDomainOptions(udomain.domain.breedingAndTimeSeriesOptions, udomain.domain.options);
            response = optionsForm.showModal;
            if (response == mrOK) {
                newCommand = updcom.PdChangeBreedingAndTimeSeriesOptionsCommand().createWithOptionsAndDomainOptions(optionsForm.options, optionsForm.domainOptions);
                umain.MainForm.doCommand(newCommand);
            }
        } finally {
            optionsForm.free;
            optionsForm = null;
        }
    }
    
    public void variationLowClick(TObject Sender) {
        this.BreederMenuVariationLowClick(this);
    }
    
    public void variationNoneNumericClick(TObject Sender) {
        this.BreederMenuVariationNoneClick(this);
    }
    
    public void variationMediumClick(TObject Sender) {
        this.BreederMenuVariationMediumClick(this);
    }
    
    public void variationHighClick(TObject Sender) {
        this.BreederMenuVariationHighClick(this);
    }
    
    public void variationCustomClick(TObject Sender) {
        this.BreederMenuVariationCustomClick(this);
    }
    
    public void varyColorsClick(TObject Sender) {
        this.BreederMenuVaryColorsClick(this);
    }
    
    public void vary3DObjectsClick(TObject Sender) {
        this.BreederMenuVary3DObjectsClick(this);
    }
    
    public void BreederPopupMenuRandomizeClick(TObject Sender) {
        this.BreederMenuRandomizeClick(this);
    }
    
    public void BreederPopupMenuBreedClick(TObject Sender) {
        this.BreederMenuBreedClick(this);
    }
    
    public void breedButtonClick(TObject Sender) {
        this.BreederMenuBreedClick(this);
    }
    
    public void BreederPopupMenuMakeTimeSeriesClick(TObject Sender) {
        this.BreederMenuMakeTimeSeriesClick(this);
    }
    
    public void BreederPopupMenuCopyClick(TObject Sender) {
        this.BreederMenuCopyClick(this);
    }
    
    public void BreederPopupMenuPasteClick(TObject Sender) {
        this.BreederMenuPasteClick(this);
    }
    
    public void BreederPopupMenuSendCopytoMainWindowClick(TObject Sender) {
        this.BreederMenuSendCopyToMainWindowClick(this);
    }
    
    public void BreederPopupMenuDeleteRowClick(TObject Sender) {
        this.BreederMenuDeleteRowClick(this);
    }
    
    // --------------------------------------------------------------------------- utilities 
    public boolean inGrid(short row, short column) {
        result = false;
        result = true;
        if ((row < 0) || (row > this.generations.Count - 1)) {
            result = false;
        }
        if ((column < 1) || (column - 1 > this.plantsDrawGrid.ColCount - 1)) {
            result = false;
        }
        return result;
    }
    
    public PdGeneration generationForIndex(short index) {
        result = new PdGeneration();
        result = null;
        if (index < 0) {
            return result;
        }
        if (index > this.generations.Count - 1) {
            return result;
        }
        if (this.generations.Items[index] == null) {
            return result;
        }
        result = ugener.PdGeneration(this.generations.Items[index]);
        return result;
    }
    
    public PdPlant plantForRowAndColumn(short row, short column) {
        result = new PdPlant();
        PdGeneration generation = new PdGeneration();
        
        result = null;
        generation = this.generationForIndex(row);
        if (generation == null) {
            return result;
        }
        result = generation.plantForIndex(column - 1);
        return result;
    }
    
    // ---------------------------------------------------------------------------- resizing 
    public void FormResize(TObject Sender) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.generations == null) {
            return;
        }
        this.breederToolbarPanel.SetBounds(0, 0, this.clientWidth, this.breederToolbarPanel.Height);
        this.helpButton.SetBounds(this.breederToolbarPanel.Width - this.helpButton.Width - 4, this.helpButton.Top, this.helpButton.Width, this.helpButton.Height);
        this.plantsDrawGrid.SetBounds(0, this.breederToolbarPanel.Height, this.clientWidth, this.clientHeight - this.breederToolbarPanel.Height);
        this.emptyWarningPanel.SetBounds(this.clientWidth / 2 - this.emptyWarningPanel.Width / 2, this.clientHeight / 2 - this.emptyWarningPanel.Height / 2, this.emptyWarningPanel.Width, this.emptyWarningPanel.Height);
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 250;
        UNRESOLVED.ptMinTrackSize.y = 150;
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Breeding_plants_using_the_breeder");
    }
    
    // ----------------------------------------------------------------------------- *palette stuff 
    public HPALETTE GetPalette() {
        result = new HPALETTE();
        result = umain.MainForm.paletteImage.Picture.Bitmap.Palette;
        return result;
    }
    
    public boolean PaletteChanged(boolean Foreground) {
        result = false;
        HPALETTE oldPalette = new HPALETTE();
        HPALETTE palette = new HPALETTE();
        HWnd windowHandle = new HWnd();
        HDC DC = new HDC();
        
        palette = this.GetPalette();
        if (palette != 0) {
            DC = UNRESOLVED.getDeviceContext(windowHandle);
            oldPalette = UNRESOLVED.selectPalette(DC, palette, !Foreground);
            if ((UNRESOLVED.realizePalette(DC) != 0) && (!delphi_compatability.Application.terminated) && (this.plantsDrawGrid != null)) {
                // if palette changed, repaint drawing 
                this.plantsDrawGrid.Invalidate();
            }
            UNRESOLVED.selectPalette(DC, oldPalette, true);
            UNRESOLVED.realizePalette(DC);
            UNRESOLVED.releaseDC(windowHandle, DC);
        }
        result = super.PaletteChanged(Foreground);
        return result;
    }
    
    public void BreederMenuHelpOnBreedingClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Breeding_plants_using_the_breeder");
    }
    
    public void BreederMenuHelpTopicsClick(TObject Sender) {
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_FINDER, 0);
    }
    
    public void BreederMenuOptionsFastDrawClick(TObject Sender) {
        umain.MainForm.MenuOptionsFastDrawClick(umain.MainForm);
    }
    
    public void BreederMenuOptionsMediumDrawClick(TObject Sender) {
        umain.MainForm.MenuOptionsMediumDrawClick(umain.MainForm);
    }
    
    public void BreederMenuOptionsBestDrawClick(TObject Sender) {
        umain.MainForm.MenuOptionsBestDrawClick(umain.MainForm);
    }
    
    public void BreederMenuOptionsCustomDrawClick(TObject Sender) {
        umain.MainForm.MenuOptionsCustomDrawClick(umain.MainForm);
    }
    
}
