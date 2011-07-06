// unit utimeser

from conversion_common import *;
import ubmpsupport;
import ucursor;
import updform;
import delphi_compatability;

// const
kRecalculateScale = true;
kDontRecalculateScale = false;
kMaxTimeSeriesStages = 100;


// var
TTimeSeriesForm TimeSeriesForm = new TTimeSeriesForm();


// const
kStageNumberTextHeight = 16;



class TTimeSeriesForm extends PdForm {
    public TDrawGrid grid;
    public TMainMenu MainMenu1;
    public TMenuItem TimeSeriesMenuEdit;
    public TMenuItem TimeSeriesMenuUndo;
    public TMenuItem TimeSeriesMenuRedo;
    public TMenuItem N1;
    public TMenuItem TimeSeriesMenuCopy;
    public TMenuItem TimeSeriesMenuPaste;
    public TMenuItem TimeSeriesMenuBreed;
    public TPopupMenu TimeSeriesPopupMenu;
    public TMenuItem TimeSeriesPopupMenuBreed;
    public TMenuItem TimeSeriesPopupMenuCopy;
    public TMenuItem TimeSeriesPopupMenuPaste;
    public TMenuItem N2;
    public TPanel emptyWarningPanel;
    public TLabel Label1;
    public TMenuItem N3;
    public TMenuItem TimeSeriesMenuDelete;
    public TMenuItem N4;
    public TMenuItem TimeSeriesMenuOptions;
    public TMenuItem TimeSeriesMenuOptionsStages;
    public TMenuItem TimeSeriesMenuHelp;
    public TMenuItem TimeSeriesMenuHelpOnTimeSeries;
    public TMenuItem TimeSeriesMenuHelpTopics;
    public TMenuItem N5;
    public TMenuItem TimeSeriesMenuOptionsDrawAs;
    public TMenuItem TimeSeriesMenuOptionsFastDraw;
    public TMenuItem TimeSeriesMenuOptionsMediumDraw;
    public TMenuItem TimeSeriesMenuOptionsBestDraw;
    public TMenuItem TimeSeriesMenuOptionsCustomDraw;
    public TMenuItem TimeSeriesMenuUndoRedoList;
    public TMenuItem TimeSeriesMenuSendCopy;
    public TMenuItem TimeSeriesPopupMenuSendCopy;
    public PdPlant parentPlant;
    public TListCollection plants;
    public short numStages;
    public PdPlant selectedPlant;
    public TPoint dragPlantStartPoint;
    public short numTimeSeriesPlantsCopiedThisSession;
    public boolean internalChange;
    public  percentsOfMaxAge;
    public  ages;
    public boolean drawing;
    public long drawProgressMax;
    public boolean resizing;
    public boolean needToRedrawFromChangeToDrawOptions;
    
    //$R *.DFM
    public void FormCreate(TObject Sender) {
        TRect tempBoundsRect = new TRect();
        
        this.plants = UNRESOLVED.TListCollection.create;
        this.grid.DragCursor = ucursor.crDragPlant;
        this.Position = delphi_compatability.TPosition.poDesigned;
        // keep window on screen - left corner of title bar 
        tempBoundsRect = UNRESOLVED.domain.timeSeriesWindowRect;
        if ((tempBoundsRect.Left != 0) || (tempBoundsRect.Right != 0) || (tempBoundsRect.Top != 0) || (tempBoundsRect.Bottom != 0)) {
            if (tempBoundsRect.Left > delphi_compatability.Screen.Width - UNRESOLVED.kMinWidthOnScreen) {
                tempBoundsRect.Left = delphi_compatability.Screen.Width - UNRESOLVED.kMinWidthOnScreen;
            }
            if (tempBoundsRect.Top > delphi_compatability.Screen.Height - UNRESOLVED.kMinHeightOnScreen) {
                tempBoundsRect.Top = delphi_compatability.Screen.Height - UNRESOLVED.kMinHeightOnScreen;
            }
            this.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom);
        }
        switch (UNRESOLVED.domain.options.drawSpeed) {
            case UNRESOLVED.kDrawFast:
                this.TimeSeriesMenuOptionsFastDraw.checked = true;
                break;
            case UNRESOLVED.kDrawMedium:
                this.TimeSeriesMenuOptionsMediumDraw.checked = true;
                break;
            case UNRESOLVED.kDrawBest:
                this.TimeSeriesMenuOptionsBestDraw.checked = true;
                break;
            case UNRESOLVED.kDrawCustom:
                this.TimeSeriesMenuOptionsCustomDraw.checked = true;
                break;
        //to get redo messages
        UNRESOLVED.MainForm.updateMenusForUndoRedo;
        this.updateForChangeToDomainOptions();
        this.updateMenusForChangeToSelectedPlant();
        this.updatePasteMenuForClipboardContents();
        this.emptyWarningPanel.SendToBack();
        this.emptyWarningPanel.Hide();
    }
    
    public void FormDestroy(TObject Sender) {
        this.plants.free;
        this.plants = null;
    }
    
    public void FormActivate(TObject Sender) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.plants.count <= 0) {
            this.emptyWarningPanel.BringToFront();
            this.emptyWarningPanel.Show();
        } else if (this.needToRedrawFromChangeToDrawOptions) {
            this.redrawPlants();
            this.needToRedrawFromChangeToDrawOptions = false;
        }
    }
    
    public void initializeWithPlant(PdPlant aPlant, boolean drawNow) {
        PdPlant newPlant = new PdPlant();
        short i = 0;
        
        if (aPlant == null) {
            return;
        }
        if (!this.Visible) {
            this.Show();
        }
        this.BringToFront();
        this.plants.clear;
        this.parentPlant = aPlant;
        ucursor.cursor_startWait();
        try {
            for (i = 0; i <= this.numStages - 1; i++) {
                newPlant = UNRESOLVED.PdPlant.create;
                this.parentPlant.copyTo(newPlant);
                this.ages[i] = intround(UNRESOLVED.max(0.0, UNRESOLVED.min(1.0, this.percentsOfMaxAge[i] / 100.0)) * newPlant.pGeneral.ageAtMaturity);
                newPlant.setAge(this.ages[i]);
                this.plants.add(newPlant);
            }
        } finally {
            ucursor.cursor_stopWait();
        }
        if (drawNow) {
            this.redrawPlants();
        }
    }
    
    // ----------------------------------------------------------------------------------- updating 
    public void updateForChangeToDomainOptions() {
        short i = 0;
        
        if (UNRESOLVED.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages != this.numStages) {
            this.numStages = UNRESOLVED.domain.breedingAndTimeSeriesOptions.numTimeSeriesStages;
            for (i = 0; i <= this.numStages - 1; i++) {
                this.percentsOfMaxAge[i] = UNRESOLVED.intMin(100, UNRESOLVED.intMax(0, (i + 1) * 100 / this.numStages));
            }
            if (this.grid.ColCount != this.numStages) {
                this.grid.ColCount = this.numStages;
            }
            this.updateForNewNumberOfStages();
        }
        if (this.grid.DefaultColWidth != UNRESOLVED.domain.breedingAndTimeSeriesOptions.thumbnailWidth) {
            this.grid.DefaultColWidth = UNRESOLVED.domain.breedingAndTimeSeriesOptions.thumbnailWidth;
        }
        if (this.grid.DefaultRowHeight != UNRESOLVED.domain.breedingAndTimeSeriesOptions.thumbnailHeight) {
            this.grid.DefaultRowHeight = UNRESOLVED.domain.breedingAndTimeSeriesOptions.thumbnailHeight;
            this.grid.RowHeights[1] = kStageNumberTextHeight;
        }
        this.redrawPlants();
    }
    
    public void updateForNewNumberOfStages() {
        short i = 0;
        PdPlant firstPlant = new PdPlant();
        PdPlant keepPlant = new PdPlant();
        
        keepPlant = null;
        try {
            if (this.plants.count > 0) {
                firstPlant = UNRESOLVED.PdPlant(this.plants.items[0]);
                if (firstPlant != null) {
                    keepPlant = UNRESOLVED.PdPlant.create;
                    firstPlant.copyTo(keepPlant);
                    this.plants.clear;
                }
            }
            if (keepPlant != null) {
                this.initializeWithPlant(keepPlant, UNRESOLVED.kDontDrawYet);
            }
        } finally {
            keepPlant.free;
        }
        this.redrawPlants();
    }
    
    public void updateForChangeToPlants(boolean recalcScale) {
        this.selectedPlant = null;
        if (this.plants.count <= 0) {
            this.parentPlant = null;
        }
        this.updateMenusForChangeToSelectedPlant();
        if (!this.Visible) {
            this.Show();
        }
        this.BringToFront();
        if (this.WindowState == delphi_compatability.TWindowState.wsMinimized) {
            this.WindowState = delphi_compatability.TWindowState.wsNormal;
        }
        this.redrawPlants();
    }
    
    public void updateMenusForChangeToSelectedPlant() {
        this.TimeSeriesMenuCopy.enabled = (this.selectedPlant != null);
        this.TimeSeriesPopupMenuCopy.enabled = this.TimeSeriesMenuCopy.enabled;
        this.TimeSeriesMenuBreed.enabled = (this.selectedPlant != null);
        this.TimeSeriesPopupMenuBreed.enabled = this.TimeSeriesMenuBreed.enabled;
    }
    
    public void updatePasteMenuForClipboardContents() {
        this.TimeSeriesMenuPaste.enabled = (UNRESOLVED.domain.plantManager.privatePlantClipboard.count > 0);
        this.TimeSeriesPopupMenuPaste.enabled = (UNRESOLVED.domain.plantManager.privatePlantClipboard.count > 0);
    }
    
    public void updatePlantsFromParent(PdPlant aPlant) {
        if ((aPlant == null) || (aPlant != this.parentPlant) || (this.plants.count <= 0)) {
            return;
        }
        this.initializeWithPlant(aPlant, UNRESOLVED.kDrawNow);
    }
    
    // ----------------------------------------------------------------------------------- plants 
    public PdPlant plantForIndex(short index) {
        result = new PdPlant();
        result = null;
        if (index < 0) {
            return result;
        }
        if (index > this.plants.count - 1) {
            return result;
        }
        if (this.plants.items[index] == null) {
            return result;
        }
        result = UNRESOLVED.PdPlant(this.plants.items[index]);
        return result;
    }
    
    public PdPlant plantAtMouse(short x, short y) {
        result = new PdPlant();
        long col = 0;
        long row = 0;
        
        result = null;
        col, row = this.grid.MouseToCell(x, y, col, row);
        if ((col < 0) || (col > this.plants.count - 1)) {
            return result;
        }
        result = this.plantForIndex(col);
        return result;
    }
    
    // -------------------------------------------------------------------------------------- drawing 
    public void redrawPlants() {
        if (this.plants.count <= 0) {
            this.emptyWarningPanel.BringToFront();
            this.emptyWarningPanel.Show();
        } else {
            this.emptyWarningPanel.SendToBack();
            this.emptyWarningPanel.Hide();
        }
        this.recalculateCommonDrawingScaleAndPosition();
        this.grid.Invalidate();
    }
    
    public void recalculateCommonDrawingScaleAndPosition() {
        PdPlant plant = new PdPlant();
        short i = 0;
        float minScale = 0.0;
        long plantPartsToDraw = 0;
        long partsDrawn = 0;
        TPoint bestPosition = new TPoint();
        long widestWidth = 0;
        long tallestHeight = 0;
        
        if (this.plants == null) {
            return;
        }
        if (this.plants.count <= 0) {
            return;
        }
        // find smallest scale
        minScale = 0.0;
        for (i = 0; i <= this.plants.count - 1; i++) {
            plant = UNRESOLVED.PdPlant(this.plants.items[i]);
            plant.fixedPreviewScale = false;
            plant.fixedDrawPosition = false;
            plant.drawPreviewIntoCache(Point(this.grid.DefaultColWidth, this.grid.DefaultRowHeight), UNRESOLVED.kDontConsiderDomainScale, UNRESOLVED.kDontDrawNow);
            if ((i == 0) || (plant.drawingScale_PixelsPerMm < minScale)) {
                minScale = plant.drawingScale_PixelsPerMm;
            }
        }
        // find common draw position
        widestWidth = 0;
        tallestHeight = 0;
        for (i = 0; i <= this.plants.count - 1; i++) {
            plant = UNRESOLVED.PdPlant(this.plants.items[i]);
            plant.fixedPreviewScale = true;
            plant.drawingScale_PixelsPerMm = minScale;
            plant.fixedDrawPosition = false;
            plant.drawPreviewIntoCache(Point(this.grid.DefaultColWidth, this.grid.DefaultRowHeight), UNRESOLVED.kDontConsiderDomainScale, UNRESOLVED.kDontDrawNow);
            if ((i == 0) || (UNRESOLVED.rWidth(plant.boundsRect_pixels) > widestWidth)) {
                widestWidth = UNRESOLVED.rWidth(plant.boundsRect_pixels);
                bestPosition.X = plant.drawPositionIfFixed.x;
            }
            if ((i == 0) || (UNRESOLVED.rHeight(plant.boundsRect_pixels) > tallestHeight)) {
                tallestHeight = UNRESOLVED.rHeight(plant.boundsRect_pixels);
                bestPosition.Y = plant.drawPositionIfFixed.y;
            }
        }
        for (i = 0; i <= this.plants.count - 1; i++) {
            // set draw position to use when repaint - don't draw now
            plant = UNRESOLVED.PdPlant(this.plants.items[i]);
            plant.fixedPreviewScale = true;
            plant.drawingScale_PixelsPerMm = minScale;
            plant.fixedDrawPosition = true;
            plant.drawPositionIfFixed = bestPosition;
            plant.previewCacheUpToDate = false;
        }
    }
    
    // -------------------------------------------------------------------------------------- grid 
    public void gridDrawCell(TObject Sender, long Col, long Row, TRect Rect, TGridDrawState State) {
        PdPlant plant = new PdPlant();
        TRect textDrawRect = new TRect();
        String textToDraw = "";
        
        this.grid.Canvas.Brush.Color = delphi_compatability.clWhite;
        this.grid.Canvas.Pen.Width = 1;
        if ((this.plants.count > 0) && (Row == 0)) {
            this.grid.Canvas.Pen.Color = delphi_compatability.clSilver;
        } else {
            this.grid.Canvas.Pen.Color = delphi_compatability.clWhite;
        }
        this.grid.Canvas.Rectangle(Rect.left, Rect.top, Rect.right, Rect.bottom);
        if (Row == 1) {
            if (this.plants.count <= 0) {
                return;
            }
            textToDraw = IntToStr(this.ages[Col]);
            if (UNRESOLVED.rWidth(Rect) > 50) {
                // 50 is fixed size
                textToDraw = textToDraw + " days";
            }
            textDrawRect.Left = Rect.left + UNRESOLVED.rWidth(Rect) / 2 - this.grid.Canvas.TextWidth(textToDraw) / 2;
            textDrawRect.Top = Rect.top + UNRESOLVED.rHeight(Rect) / 2 - this.grid.Canvas.TextHeight("0") / 2;
            this.grid.Canvas.TextOut(textDrawRect.Left, textDrawRect.Top, textToDraw);
            return;
        }
        plant = null;
        plant = this.plantForIndex(Col);
        if (plant == null) {
            return;
        }
        if (!plant.previewCacheUpToDate) {
            // draw plant 
            // draw gray solid box to show delay for drawing plant cache
            this.grid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
            this.grid.Canvas.Brush.Color = delphi_compatability.clSilver;
            this.grid.Canvas.Pen.Color = delphi_compatability.clSilver;
            //FIX unresolved WITH expression: Rect
            this.grid.Canvas.Rectangle(this.Left + 1, this.Top + 1, UNRESOLVED.right, UNRESOLVED.bottom);
            plant.drawPreviewIntoCache(Point(this.grid.DefaultColWidth, this.grid.DefaultRowHeight), UNRESOLVED.kDontConsiderDomainScale, UNRESOLVED.kDrawNow);
        }
        plant.previewCache.transparent = false;
        ubmpsupport.copyBitmapToCanvasWithGlobalPalette(plant.previewCache, this.grid.Canvas, Rect);
        // draw selection rectangle 
        this.grid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        this.grid.Canvas.Pen.Width = 2;
        if (plant == this.selectedPlant) {
            this.grid.Canvas.Pen.Color = UNRESOLVED.domain.options.firstSelectionRectangleColor;
        } else {
            this.grid.Canvas.Pen.Color = delphi_compatability.clSilver;
        }
        //FIX unresolved WITH expression: Rect
        this.grid.Canvas.Rectangle(this.Left + 1, this.Top + 1, UNRESOLVED.right, UNRESOLVED.bottom);
    }
    
    public void gridMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.selectedPlant = this.plantAtMouse(X, Y);
        this.updateMenusForChangeToSelectedPlant();
        this.grid.Invalidate();
        if ((Button == delphi_compatability.TMouseButton.mbRight) || (delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
            // start drag of plant
            return;
        }
        if (this.selectedPlant == null) {
            return;
        }
        this.dragPlantStartPoint = Point(X, Y);
        this.grid.BeginDrag(false);
    }
    
    public void gridDragOver(TObject Sender, TObject Source, int X, int Y, TDragState State, boolean Accept) {
        Accept = (Source != null) && (Sender != null) && ((Source == UNRESOLVED.MainForm.drawingPaintBox) || (Source == UNRESOLVED.MainForm.plantListDrawGrid) || (Source == UNRESOLVED.BreederForm.plantsDrawGrid));
        return Accept;
    }
    
    public void gridEndDrag(TObject Sender, TObject Target, int X, int Y) {
        PdPlant plant = new PdPlant();
        PdCommand newCommand = new PdCommand();
        TList newPlants = new TList();
        PdPlant newPlant = new PdPlant();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (Target == null) {
            return;
        }
        // get plant being dragged 
        plant = this.plantAtMouse(this.dragPlantStartPoint.X, this.dragPlantStartPoint.Y);
        if (plant == null) {
            return;
        }
        if (Target == UNRESOLVED.BreederForm.plantsDrawGrid) {
            UNRESOLVED.BreederForm.copyPlantToPoint(plant, X, Y);
        } else if ((Target == UNRESOLVED.MainForm.drawingPaintBox) || (Target == UNRESOLVED.MainForm.plantListDrawGrid)) {
            // make paste command - wants list of plants 
            newPlant = UNRESOLVED.PdPlant.create;
            plant.copyTo(newPlant);
            this.numTimeSeriesPlantsCopiedThisSession += 1;
            newPlant.setName("Time series plant " + IntToStr(this.numTimeSeriesPlantsCopiedThisSession));
            if (Target == UNRESOLVED.MainForm.drawingPaintBox) {
                newPlant.moveTo(Point(X, Y));
            } else {
                newPlant.moveTo(UNRESOLVED.MainForm.standardPastePosition);
            }
            if (!UNRESOLVED.domain.viewPlantsInMainWindowOnePlantAtATime) {
                // v2.1
                newPlant.calculateDrawingScaleToLookTheSameWithDomainScale;
            }
            //to save memory - don't need it in main window
            newPlant.shrinkPreviewCache;
            newPlants = delphi_compatability.TList().Create();
            newPlants.Add(newPlant);
            newCommand = UNRESOLVED.PdPasteCommand.createWithListOfPlantsAndOldSelectedList(newPlants, UNRESOLVED.MainForm.selectedPlants);
            UNRESOLVED.PdPasteCommand(newCommand).useSpecialPastePosition = true;
            try {
                //command will free plant if paste is undone
                ucursor.cursor_startWait();
                UNRESOLVED.MainForm.doCommand(newCommand);
            } finally {
                //command has another list, so we must free this one
                newPlants.free;
                ucursor.cursor_stopWait();
            }
        }
    }
    
    public void copyPlantToPoint(PdPlant aPlant, int x, int y) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = UNRESOLVED.PdMakeTimeSeriesCommand.createWithNewPlant(aPlant);
        UNRESOLVED.MainForm.doCommand(newCommand);
    }
    
    public void invalidateGridCell(long column) {
        TRect cellRectOver = new TRect();
        
        if ((column < 0)) {
            return;
        }
        cellRectOver = this.grid.CellRect(column, 0);
        UNRESOLVED.invalidateRect(this.grid.Handle, cellRectOver, true);
    }
    
    // ------------------------------------------------------------------------------- menu 
    public void TimeSeriesMenuUndoClick(TObject Sender) {
        UNRESOLVED.MainForm.menuEditUndoClick(UNRESOLVED.MainForm);
    }
    
    public void TimeSeriesMenuRedoClick(TObject Sender) {
        UNRESOLVED.MainForm.menuEditRedoClick(UNRESOLVED.MainForm);
    }
    
    public void TimeSeriesMenuUndoRedoListClick(TObject Sender) {
        UNRESOLVED.MainForm.UndoMenuEditUndoRedoListClick(UNRESOLVED.MainForm);
    }
    
    public void TimeSeriesMenuCopyClick(TObject Sender) {
        PdPlant plant = new PdPlant();
        TList copyList = new TList();
        String saveName = "";
        
        plant = this.selectedPlant;
        if (plant == null) {
            return;
        }
        copyList = delphi_compatability.TList().Create();
        copyList.Add(plant);
        // temporarily change plant name, position, scale to make copy, then put back 
        saveName = plant.getName;
        this.numTimeSeriesPlantsCopiedThisSession += 1;
        plant.setName("Time series plant " + IntToStr(this.numTimeSeriesPlantsCopiedThisSession));
        UNRESOLVED.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(copyList);
        plant.setName(saveName);
        //sets our paste menu also
        UNRESOLVED.MainForm.updatePasteMenuForClipboardContents;
    }
    
    public void TimeSeriesMenuPasteClick(TObject Sender) {
        PdPlant newPlant = new PdPlant();
        PdCommand newCommand = new PdCommand();
        
        if (UNRESOLVED.domain.plantManager.privatePlantClipboard.count <= 0) {
            return;
        }
        newPlant = UNRESOLVED.PdPlant.create;
        try {
            UNRESOLVED.domain.plantManager.pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant);
            newCommand = UNRESOLVED.PdMakeTimeSeriesCommand.createWithNewPlant(newPlant);
            ((UNRESOLVED.PdMakeTimeSeriesCommand)newCommand).isPaste = true;
            UNRESOLVED.MainForm.doCommand(newCommand);
        } finally {
            //command makes copies from plant, but we must free it
            newPlant.free;
        }
    }
    
    public void TimeSeriesMenuSendCopyClick(TObject Sender) {
        this.TimeSeriesMenuCopyClick(this);
        UNRESOLVED.MainForm.MenuEditPasteClick(UNRESOLVED.MainForm);
    }
    
    public void TimeSeriesMenuBreedClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlant == null) {
            return;
        }
        if (UNRESOLVED.BreederForm.selectedRow >= UNRESOLVED.domain.breedingAndTimeSeriesOptions.maxGenerations - 2) {
            // check if there is room in the breeder - this command will make two new generations 
            UNRESOLVED.BreederForm.fullWarning;
        } else {
            newCommand = UNRESOLVED.PdBreedFromParentsCommand.createWithInfo(UNRESOLVED.BreederForm.generations, this.selectedPlant, null, -1, UNRESOLVED.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, UNRESOLVED.kCreateFirstGeneration);
            UNRESOLVED.MainForm.doCommand(newCommand);
        }
    }
    
    public void TimeSeriesMenuDeleteClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = UNRESOLVED.PdDeleteTimeSeriesCommand.create;
        UNRESOLVED.MainForm.doCommand(newCommand);
    }
    
    public void TimeSeriesPopupMenuCopyClick(TObject Sender) {
        this.TimeSeriesMenuCopyClick(this);
    }
    
    public void TimeSeriesPopupMenuPasteClick(TObject Sender) {
        this.TimeSeriesMenuPasteClick(this);
    }
    
    public void TimeSeriesPopupMenuBreedClick(TObject Sender) {
        this.TimeSeriesMenuBreedClick(this);
    }
    
    // ------------------------------------------------------------------------------- resizing 
    public void FormResize(TObject Sender) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.plants == null) {
            return;
        }
        this.grid.SetBounds(0, 0, this.ClientWidth, UNRESOLVED.intMax(0, this.ClientHeight));
        this.emptyWarningPanel.SetBounds(this.ClientWidth / 2 - this.emptyWarningPanel.Width / 2, this.ClientHeight / 2 - this.emptyWarningPanel.Height / 2, this.emptyWarningPanel.Width, this.emptyWarningPanel.Height);
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 280;
        UNRESOLVED.ptMinTrackSize.y = 120;
    }
    
    // ----------------------------------------------------------------------------- *palette stuff 
    public HPALETTE GetPalette() {
        result = new HPALETTE();
        result = UNRESOLVED.MainForm.paletteImage.picture.bitmap.palette;
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
            DC = this.GetDeviceContext(windowHandle);
            oldPalette = UNRESOLVED.selectPalette(DC, palette, !Foreground);
            if ((UNRESOLVED.realizePalette(DC) != 0) && (!delphi_compatability.Application.terminated) && (this.grid != null)) {
                // if palette changed, repaint drawing 
                this.grid.Invalidate();
            }
            UNRESOLVED.selectPalette(DC, oldPalette, true);
            UNRESOLVED.realizePalette(DC);
            UNRESOLVED.releaseDC(windowHandle, DC);
        }
        result = super.PaletteChanged(Foreground);
        return result;
    }
    
    public void TimeSeriesMenuHelpTopicsClick(TObject Sender) {
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_FINDER, 0);
    }
    
    public void TimeSeriesMenuHelpOnTimeSeriesClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Making_time_series");
    }
    
    public void TimeSeriesMenuOptionsStagesClick(TObject Sender) {
        UNRESOLVED.BreederForm.changeBreederAndTimeSeriesOptions(0);
    }
    
    public void TimeSeriesMenuOptionsFastDrawClick(TObject Sender) {
        UNRESOLVED.MainForm.MenuOptionsFastDrawClick(UNRESOLVED.MainForm);
    }
    
    public void TimeSeriesMenuOptionsMediumDrawClick(TObject Sender) {
        UNRESOLVED.MainForm.MenuOptionsMediumDrawClick(UNRESOLVED.MainForm);
    }
    
    public void TimeSeriesMenuOptionsBestDrawClick(TObject Sender) {
        UNRESOLVED.MainForm.MenuOptionsBestDrawClick(UNRESOLVED.MainForm);
    }
    
    public void TimeSeriesMenuOptionsCustomDrawClick(TObject Sender) {
        UNRESOLVED.MainForm.MenuOptionsCustomDrawClick(UNRESOLVED.MainForm);
    }
    
}
