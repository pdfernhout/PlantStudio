unit utimeser;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, Grids,
  updform, ucollect, uplant, Menus, ExtCtrls, StdCtrls, Buttons;

const
  kRecalculateScale = true; kDontRecalculateScale = false; 
  kMaxTimeSeriesStages = 100;

type
  TTimeSeriesForm = class(PdForm)
    grid: TDrawGrid;
    MainMenu1: TMainMenu;
    TimeSeriesMenuEdit: TMenuItem;
    TimeSeriesMenuUndo: TMenuItem;
    TimeSeriesMenuRedo: TMenuItem;
    N1: TMenuItem;
    TimeSeriesMenuCopy: TMenuItem;
    TimeSeriesMenuPaste: TMenuItem;
    TimeSeriesMenuBreed: TMenuItem;
    TimeSeriesPopupMenu: TPopupMenu;
    TimeSeriesPopupMenuBreed: TMenuItem;
    TimeSeriesPopupMenuCopy: TMenuItem;
    TimeSeriesPopupMenuPaste: TMenuItem;
    N2: TMenuItem;
    emptyWarningPanel: TPanel;
    Label1: TLabel;
    N3: TMenuItem;
    TimeSeriesMenuDelete: TMenuItem;
    N4: TMenuItem;
    TimeSeriesMenuOptions: TMenuItem;
    TimeSeriesMenuOptionsStages: TMenuItem;
    TimeSeriesMenuHelp: TMenuItem;
    TimeSeriesMenuHelpOnTimeSeries: TMenuItem;
    TimeSeriesMenuHelpTopics: TMenuItem;
    N5: TMenuItem;
    TimeSeriesMenuOptionsDrawAs: TMenuItem;
    TimeSeriesMenuOptionsFastDraw: TMenuItem;
    TimeSeriesMenuOptionsMediumDraw: TMenuItem;
    TimeSeriesMenuOptionsBestDraw: TMenuItem;
    TimeSeriesMenuOptionsCustomDraw: TMenuItem;
    TimeSeriesMenuUndoRedoList: TMenuItem;
    TimeSeriesMenuSendCopy: TMenuItem;
    TimeSeriesPopupMenuSendCopy: TMenuItem;
    procedure FormCreate(Sender: TObject);
    procedure FormDestroy(Sender: TObject);
    procedure gridDrawCell(Sender: TObject; Col, Row: Longint; Rect: TRect;
      State: TGridDrawState);
    procedure gridMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure gridDragOver(Sender, Source: TObject; X, Y: Integer;
      State: TDragState; var Accept: Boolean);
    procedure gridEndDrag(Sender, Target: TObject; X, Y: Integer);
    procedure FormResize(Sender: TObject);
    procedure TimeSeriesMenuUndoClick(Sender: TObject);
    procedure TimeSeriesMenuRedoClick(Sender: TObject);
    procedure TimeSeriesMenuCopyClick(Sender: TObject);
    procedure TimeSeriesMenuPasteClick(Sender: TObject);
    procedure TimeSeriesMenuBreedClick(Sender: TObject);
    procedure TimeSeriesPopupMenuCopyClick(Sender: TObject);
    procedure TimeSeriesPopupMenuPasteClick(Sender: TObject);
    procedure TimeSeriesPopupMenuBreedClick(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure TimeSeriesMenuDeleteClick(Sender: TObject);
    procedure TimeSeriesMenuHelpTopicsClick(Sender: TObject);
    procedure TimeSeriesMenuHelpOnTimeSeriesClick(Sender: TObject);
    procedure TimeSeriesMenuOptionsStagesClick(Sender: TObject);
    procedure TimeSeriesMenuOptionsFastDrawClick(Sender: TObject);
    procedure TimeSeriesMenuOptionsMediumDrawClick(Sender: TObject);
    procedure TimeSeriesMenuOptionsBestDrawClick(Sender: TObject);
    procedure TimeSeriesMenuOptionsCustomDrawClick(Sender: TObject);
    procedure TimeSeriesMenuUndoRedoListClick(Sender: TObject);
    procedure TimeSeriesMenuSendCopyClick(Sender: TObject);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
  public
    { Public declarations }
    parentPlant: PdPlant;
    plants: TListCollection;
    numStages: smallint;
    selectedPlant: PdPlant;
    dragPlantStartPoint: TPoint;
    numTimeSeriesPlantsCopiedThisSession: smallint;
    internalChange: boolean;
    percentsOfMaxAge: array[0..kMaxTimeSeriesStages] of single;
    ages: array[0..kMaxTimeSeriesStages] of smallint;
    drawing: boolean;
    drawProgressMax: longint;
    resizing: boolean;
    needToRedrawFromChangeToDrawOptions: boolean;
    procedure initializeWithPlant(aPlant: PdPlant; drawNow: boolean);
    procedure updateForChangeToDomainOptions;
    procedure invalidateGridCell(column: longint);
    function plantForIndex(index: smallint): PdPlant;
    function plantAtMouse(x, y: smallint): PdPlant;
    procedure updateForChangeToPlants(recalcScale: boolean);
    procedure copyPlantToPoint(aPlant: PdPlant; x, y: integer);
    procedure recalculateCommonDrawingScaleAndPosition;
    procedure redrawPlants;
    procedure updateMenusForChangeToSelectedPlant;
    procedure updatePasteMenuForClipboardContents;
    procedure updateForNewNumberOfStages;
    procedure updatePlantsFromParent(aPlant: PdPlant);
		function GetPalette: HPALETTE; override;
		function PaletteChanged(Foreground: Boolean): Boolean; override;
  end;

var
  TimeSeriesForm: TTimeSeriesForm;

implementation

{$R *.DFM}

uses 
  udomain, umath, usupport, ucursor, updcom, ucommand, umain, ubreedr, ubmpsupport;

const
  kStageNumberTextHeight = 16;

procedure TTimeSeriesForm.FormCreate(Sender: TObject);
  var
    tempBoundsRect: TRect;
  begin
  plants := TListCollection.create;
  grid.dragCursor := crDragPlant;
  self.position := poDesigned;
  { keep window on screen - left corner of title bar }
  tempBoundsRect := domain.timeSeriesWindowRect;
  with tempBoundsRect do
    if (left <> 0) or (right <> 0) or (top <> 0) or (bottom <> 0) then
      begin
      if left > screen.width - kMinWidthOnScreen then left := screen.width - kMinWidthOnScreen;
      if top > screen.height - kMinHeightOnScreen then top := screen.height - kMinHeightOnScreen;
      self.setBounds(left, top, right, bottom);
      end;
  case domain.options.drawSpeed of
    kDrawFast: TimeSeriesMenuOptionsFastDraw.checked := true;
    kDrawMedium: TimeSeriesMenuOptionsMediumDraw.checked := true;
    kDrawBest: TimeSeriesMenuOptionsBestDraw.checked := true;
    kDrawCustom: TimeSeriesMenuOptionsCustomDraw.checked := true;
    end;
  MainForm.updateMenusForUndoRedo; {to get redo messages}
  self.updateForChangeToDomainOptions;
  self.updateMenusForChangeToSelectedPlant;
  self.updatePasteMenuForClipboardContents;
  emptyWarningPanel.sendToBack;
  emptyWarningPanel.hide;
  end;

procedure TTimeSeriesForm.FormDestroy(Sender: TObject);
  begin
  plants.free;
  plants := nil;
  end;

procedure TTimeSeriesForm.FormActivate(Sender: TObject);
  begin
  if Application.terminated then exit;
  if plants.count <= 0 then
    begin
    emptyWarningPanel.bringToFront;
    emptyWarningPanel.show;
    end
  else if self.needToRedrawFromChangeToDrawOptions then
    begin
    self.redrawPlants;
    self.needToRedrawFromChangeToDrawOptions := false;
    end;
  end;

procedure TTimeSeriesForm.initializeWithPlant(aPlant: PdPlant; drawNow: boolean);
  var
    newPlant: PdPlant;
    i: smallint;
  begin
  if aPlant = nil then exit;
  if not self.visible then self.show;
  self.bringToFront;
  plants.clear;
  parentPlant := aPlant;
  cursor_startWait;
  try
    for i := 0 to numStages - 1 do
      begin
      newPlant := PdPlant.create;
      parentPlant.copyTo(newPlant);
      ages[i] := round(max(0.0, min(1.0, percentsOfMaxAge[i] / 100.0)) * newPlant.pGeneral.ageAtMaturity);
      newPlant.setAge(ages[i]);
      plants.add(newPlant);
      end;
  finally
    cursor_stopWait;
  end;
  if drawNow then
    self.redrawPlants;
  end;

{ ----------------------------------------------------------------------------------- updating }
procedure TTimeSeriesForm.updateForChangeToDomainOptions;
  var
    i: smallint;
  begin
  if domain.breedingAndTimeSeriesOptions.numTimeSeriesStages <> numStages then
    begin
    numStages := domain.breedingAndTimeSeriesOptions.numTimeSeriesStages;
    for i := 0 to numStages - 1 do percentsOfMaxAge[i] := intMin(100, intMax(0, (i + 1) * 100 div numStages));
    if grid.colCount <> numStages then
      grid.colCount := numStages;
    self.updateForNewNumberOfStages;
    end;
  if grid.defaultColWidth <> domain.breedingAndTimeSeriesOptions.thumbnailWidth then
    grid.defaultColWidth := domain.breedingAndTimeSeriesOptions.thumbnailWidth;
  if grid.defaultRowHeight <> domain.breedingAndTimeSeriesOptions.thumbnailHeight then
    begin
    grid.defaultRowHeight := domain.breedingAndTimeSeriesOptions.thumbnailHeight;
    grid.rowHeights[1] := kStageNumberTextHeight;
    end;
  self.redrawPlants;
  end;

procedure TTimeSeriesForm.updateForNewNumberOfStages;
  var
    i: smallint;
    firstPlant, keepPlant: PdPlant;
  begin
  keepPlant := nil;
  try
    if plants.count > 0 then
      begin
      firstPlant := PdPlant(plants.items[0]);
      if firstPlant <> nil then
        begin
        keepPlant := PdPlant.create;
        firstPlant.copyTo(keepPlant);
        plants.clear;
        end;
      end;
    if keepPlant <> nil then
      self.initializeWithPlant(keepPlant, kDontDrawYet);
  finally
    keepPlant.free;
  end;
  self.redrawPlants;
  end;

procedure TTimeSeriesForm.updateForChangeToPlants(recalcScale: boolean);
  begin
  self.selectedPlant := nil;
  if plants.count <= 0 then
    parentPlant := nil;
  self.updateMenusForChangeToSelectedPlant;
  if not self.visible then self.show;
  self.bringToFront;
  if self.windowState = wsMinimized then self.windowState := wsNormal;
  self.redrawPlants;
  end;

procedure TTimeSeriesForm.updateMenusForChangeToSelectedPlant;
  begin
  TimeSeriesMenuCopy.enabled := (self.selectedPlant <> nil);
  TimeSeriesPopupMenuCopy.enabled := TimeSeriesMenuCopy.enabled;
  TimeSeriesMenuBreed.enabled := (self.selectedPlant <> nil);
  TimeSeriesPopupMenuBreed.enabled := TimeSeriesMenuBreed.enabled;
  end;

procedure TTimeSeriesForm.updatePasteMenuForClipboardContents;
  begin
  TimeSeriesMenuPaste.enabled := (domain.plantManager.privatePlantClipboard.count > 0);
  TimeSeriesPopupMenuPaste.enabled := (domain.plantManager.privatePlantClipboard.count > 0);
  end;

procedure TTimeSeriesForm.updatePlantsFromParent(aPlant: PdPlant);
	begin
  if (aPlant = nil) or (aPlant <> self.parentPlant) or (plants.count <= 0) then exit;
  self.initializeWithPlant(aPlant, kDrawNow);
  end;

{ ----------------------------------------------------------------------------------- plants }
function TTimeSeriesForm.plantForIndex(index: smallint): PdPlant;
  begin
  result := nil;
  if index < 0 then exit;
  if index > plants.count - 1 then exit;
  if plants.items[index] = nil then exit;
  result := PdPlant(plants.items[index]);
  end;

function TTimeSeriesForm.plantAtMouse(x, y: smallint): PdPlant;
  var
    col, row: longint;
  begin
  result := nil;
  grid.mouseToCell(x, y, col, row);
  if (col < 0) or (col > plants.count - 1) then exit;
  result := self.plantForIndex(col);
  end;

{ -------------------------------------------------------------------------------------- drawing }
procedure TTimeSeriesForm.redrawPlants;
  begin
  if plants.count <= 0 then
    begin
    emptyWarningPanel.bringToFront;
    emptyWarningPanel.show;
    end
  else
    begin
    emptyWarningPanel.sendToBack;
    emptyWarningPanel.hide;
    end;
  self.recalculateCommonDrawingScaleAndPosition;
  grid.invalidate;
  end;

procedure TTimeSeriesForm.recalculateCommonDrawingScaleAndPosition;
  var
    plant: PdPlant;
    i: smallint;
    minScale: single;
    plantPartsToDraw, partsDrawn: longint;
    bestPosition: TPoint;
    widestWidth, tallestHeight: longint;
  begin
  if plants = nil then exit;
  if plants.count <= 0 then exit;
  // find smallest scale
  minScale := 0.0;
  for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    plant.fixedPreviewScale := false;
    plant.fixedDrawPosition := false;
    plant.drawPreviewIntoCache(Point(grid.defaultColWidth, grid.defaultRowHeight),
      kDontConsiderDomainScale, kDontDrawNow);
    if (i = 0) or (plant.drawingScale_PixelsPerMm < minScale) then
      minScale := plant.drawingScale_PixelsPerMm;
    end;
  // find common draw position
  widestWidth := 0;
  tallestHeight := 0;
  for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    plant.fixedPreviewScale := true;
    plant.drawingScale_PixelsPerMm := minScale;
    plant.fixedDrawPosition := false;
    plant.drawPreviewIntoCache(Point(grid.defaultColWidth, grid.defaultRowHeight),
      kDontConsiderDomainScale, kDontDrawNow);
    if (i = 0) or (rWidth(plant.boundsRect_pixels) > widestWidth) then
      begin
      widestWidth := rWidth(plant.boundsRect_pixels);
      bestPosition.x := plant.drawPositionIfFixed.x;
      end;
    if (i = 0) or (rHeight(plant.boundsRect_pixels) > tallestHeight) then
      begin
      tallestHeight := rHeight(plant.boundsRect_pixels);
      bestPosition.y := plant.drawPositionIfFixed.y;
      end;
    end;
  // set draw position to use when repaint - don't draw now
  for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    plant.fixedPreviewScale := true;
    plant.drawingScale_PixelsPerMm := minScale;
    plant.fixedDrawPosition := true;
    plant.drawPositionIfFixed := bestPosition;
    plant.previewCacheUpToDate := false;
    end;
  end;

{ -------------------------------------------------------------------------------------- grid }
procedure TTimeSeriesForm.gridDrawCell(Sender: TObject; Col, Row: Longint; Rect: TRect; State: TGridDrawState);
  var
    plant: PdPlant;
    textDrawRect: TRect;
    textToDraw: string;
  begin
  grid.canvas.brush.color := clWhite;
  grid.canvas.pen.width := 1;
  if (plants.count > 0) and (row = 0) then
    grid.canvas.pen.color := clSilver
  else
    grid.canvas.pen.color := clWhite;
  grid.canvas.rectangle(rect.left, rect.top, rect.right, rect.bottom);
  if row = 1 then
    begin
    if plants.count <= 0 then exit;
    textToDraw := intToStr(ages[col]);
    if rWidth(rect) > 50 then textToDraw := textToDraw + ' days';  // 50 is fixed size
    textDrawRect.left := rect.left + rWidth(rect) div 2 - grid.canvas.textWidth(textToDraw) div 2;
    textDrawRect.top := rect.top + rHeight(rect) div 2 - grid.canvas.textHeight('0') div 2;
    grid.canvas.textOut(textDrawRect.left, textDrawRect.top, textToDraw);
    exit;
    end;
  plant := nil;
  plant := self.plantForIndex(col);
  if plant = nil then exit;
  { draw plant }
  if not plant.previewCacheUpToDate then
    begin
    // draw gray solid box to show delay for drawing plant cache
    grid.canvas.brush.style := bsSolid;
    grid.canvas.brush.color := clSilver;
    grid.canvas.pen.color := clSilver;
    with rect do grid.canvas.rectangle(left+1, top+1, right, bottom);
    plant.drawPreviewIntoCache(Point(grid.defaultColWidth, grid.defaultRowHeight),
      kDontConsiderDomainScale, kDrawNow);
    end;
  plant.previewCache.transparent := false;
  copyBitmapToCanvasWithGlobalPalette(plant.previewCache, grid.canvas, rect);
  { draw selection rectangle }
  grid.canvas.brush.style := bsClear;
  grid.canvas.pen.width := 2;
  if plant = selectedPlant then
    grid.canvas.pen.color := domain.options.firstSelectionRectangleColor
  else
    grid.canvas.pen.color := clSilver;     
  with rect do grid.canvas.rectangle(left+1, top+1, right, bottom);
  end;

procedure TTimeSeriesForm.gridMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  selectedPlant := self.plantAtMouse(x, y);
  self.updateMenusForChangeToSelectedPlant;
  grid.invalidate;
  // start drag of plant
  if (button = mbRight) or (ssShift in shift) then exit;
  if selectedPlant = nil then exit;
  dragPlantStartPoint := Point(x, y);
  grid.beginDrag(false);
  end;

procedure TTimeSeriesForm.gridDragOver(Sender, Source: TObject; X, Y: Integer; State: TDragState; var Accept: Boolean);
  begin
  accept := (source <> nil) and (sender <> nil)
    and (
      (source = MainForm.drawingPaintBox)
      or (source = MainForm.plantListDrawGrid)
      or (source = BreederForm.plantsDrawGrid));
  end;

procedure TTimeSeriesForm.gridEndDrag(Sender, Target: TObject; X, Y: Integer);
  var
    plant: PdPlant;
    newCommand: PdCommand;
    newPlants: TList;
    newPlant: PdPlant;
  begin
  if application.terminated then exit;
  if target = nil then exit;
  { get plant being dragged }
  plant := self.plantAtMouse(dragPlantStartPoint.x, dragPlantStartPoint.y);
  if plant = nil then exit;
  if target = BreederForm.plantsDrawGrid then
    begin
    BreederForm.copyPlantToPoint(plant, x, y);
    end
  else if (target = MainForm.drawingPaintBox) or (target =  MainForm.plantListDrawGrid) then
    begin
    { make paste command - wants list of plants }
    newPlant := PdPlant.create;
    plant.copyTo(newPlant);
    inc(numTimeSeriesPlantsCopiedThisSession);
    newPlant.setName('Time series plant ' + intToStr(numTimeSeriesPlantsCopiedThisSession));
    if target = MainForm.drawingPaintBox then
      newPlant.moveTo(Point(x,y))
    else
      newPlant.moveTo(MainForm.standardPastePosition);
    if not domain.viewPlantsInMainWindowOnePlantAtATime then // v2.1
      newPlant.calculateDrawingScaleToLookTheSameWithDomainScale;
    newPlant.shrinkPreviewCache; {to save memory - don't need it in main window}
    newPlants := TList.create;
    newPlants.add(newPlant);
    newCommand := PdPasteCommand.createWithListOfPlantsAndOldSelectedList(newPlants, MainForm.selectedPlants);
    PdPasteCommand(newCommand).useSpecialPastePosition := true;
    {command will free plant if paste is undone}
    try
      cursor_startWait;
      MainForm.doCommand(newCommand);
    finally
      newPlants.free; {command has another list, so we must free this one}
      cursor_stopWait;
    end;
    end;
  end;

procedure TTimeSeriesForm.copyPlantToPoint(aPlant: PdPlant; x, y: integer);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdMakeTimeSeriesCommand.createWithNewPlant(aPlant);
  MainForm.doCommand(newCommand);
  end;

procedure TTimeSeriesForm.invalidateGridCell(column: longint);
  var
    cellRectOver: TRect;
  begin
  if (column < 0) then exit;
  cellRectOver := grid.cellRect(column, 0);
  invalidateRect(grid.handle, @cellRectOver, true);
  end;

{ ------------------------------------------------------------------------------- menu }
procedure TTimeSeriesForm.TimeSeriesMenuUndoClick(Sender: TObject);
  begin
  MainForm.menuEditUndoClick(MainForm);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuRedoClick(Sender: TObject);
  begin
  MainForm.menuEditRedoClick(MainForm);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuUndoRedoListClick(Sender: TObject);
  begin
  MainForm.UndoMenuEditUndoRedoListClick(MainForm);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuCopyClick(Sender: TObject);
  var
    plant: PdPlant;
    copyList: TList;
    saveName: string;
  begin
  plant := self.selectedPlant;
  if plant = nil then exit;
  copyList := TList.create;
  copyList.add(plant);
  { temporarily change plant name, position, scale to make copy, then put back }
  saveName := plant.getName;
  inc(numTimeSeriesPlantsCopiedThisSession);
  plant.setName('Time series plant ' + intToStr(numTimeSeriesPlantsCopiedThisSession));
  domain.plantManager.copyPlantsInListToPrivatePlantClipboard(copyList);
  plant.setName(saveName);
  MainForm.updatePasteMenuForClipboardContents; {sets our paste menu also}
  end;

procedure TTimeSeriesForm.TimeSeriesMenuPasteClick(Sender: TObject);
  var
    newPlant: PdPlant;
    newCommand: PdCommand;
  begin
  if domain.plantManager.privatePlantClipboard.count <= 0 then exit;
  newPlant := PdPlant.create;
  try
    domain.plantManager.pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant);
    newCommand := PdMakeTimeSeriesCommand.createWithNewPlant(newPlant);
    (newCommand as PdMakeTimeSeriesCommand).isPaste := true;
    MainForm.doCommand(newCommand);
  finally
    newPlant.free; {command makes copies from plant, but we must free it}
  end;
  end;

procedure TTimeSeriesForm.TimeSeriesMenuSendCopyClick(Sender: TObject);
  begin
  self.TimeSeriesMenuCopyClick(self);
  MainForm.MenuEditPasteClick(MainForm);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuBreedClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if self.selectedPlant = nil then exit;
  { check if there is room in the breeder - this command will make two new generations }
  if BreederForm.selectedRow >= domain.breedingAndTimeSeriesOptions.maxGenerations - 2 then
    BreederForm.fullWarning
  else
    begin
    newCommand := PdBreedFromParentsCommand.createWithInfo(BreederForm.generations,
      self.selectedPlant, nil, -1,
      domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, kCreateFirstGeneration);
    MainForm.doCommand(newCommand);
    end;
  end;

procedure TTimeSeriesForm.TimeSeriesMenuDeleteClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdDeleteTimeSeriesCommand.create;
  MainForm.doCommand(newCommand);
  end;

procedure TTimeSeriesForm.TimeSeriesPopupMenuCopyClick(Sender: TObject);
  begin
  self.TimeSeriesMenuCopyClick(self);
  end;

procedure TTimeSeriesForm.TimeSeriesPopupMenuPasteClick(Sender: TObject);
  begin
  self.TimeSeriesMenuPasteClick(self);
  end;

procedure TTimeSeriesForm.TimeSeriesPopupMenuBreedClick(Sender: TObject);
  begin
  self.TimeSeriesMenuBreedClick(self);
  end;

{ ------------------------------------------------------------------------------- resizing }
procedure TTimeSeriesForm.FormResize(Sender: TObject);
  begin
  if Application.terminated then exit;
  if plants = nil then exit;
  with grid do setBounds(0, 0, self.clientWidth, intMax(0, self.clientHeight));
  with emptyWarningPanel do
    setBounds(self.clientWidth div 2 - width div 2, self.clientHeight div 2 - height div 2, width, height);
  end;

procedure TTimeSeriesForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 280;
    ptMinTrackSize.y := 120;
    end;
  end;

{ ----------------------------------------------------------------------------- *palette stuff }
function TTimeSeriesForm.GetPalette: HPALETTE;
  begin
  result := MainForm.paletteImage.picture.bitmap.palette;
  end;

function TTimeSeriesForm.PaletteChanged(Foreground: Boolean): Boolean;
	var
  	oldPalette, palette: HPALETTE;
  	windowHandle: HWnd;
  	DC: HDC;
	begin
  palette := getPalette;
  if palette <> 0 then
  	begin
    DC := getDeviceContext(WindowHandle);
    oldPalette := selectPalette(DC, palette, not foreground);
    { if palette changed, repaint drawing }
    if (realizePalette(DC) <> 0) and (not Application.terminated)
      and (grid <> nil) then
        begin
    	  grid.invalidate;
        end;
    selectPalette(DC, oldPalette, True);
    realizePalette(DC);
    releaseDC(windowHandle, DC);
  	end;
  result := inherited paletteChanged(foreground);
	end;

procedure TTimeSeriesForm.TimeSeriesMenuHelpTopicsClick(Sender: TObject);
  begin
  application.helpCommand(HELP_FINDER, 0);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuHelpOnTimeSeriesClick(Sender: TObject);
  begin
  application.helpJump('Making_time_series');
  end;

procedure TTimeSeriesForm.TimeSeriesMenuOptionsStagesClick(Sender: TObject);
  begin
  BreederForm.changeBreederAndTimeSeriesOptions(0);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuOptionsFastDrawClick(Sender: TObject);
  begin
  MainForm.MenuOptionsFastDrawClick(MainForm);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuOptionsMediumDrawClick(Sender: TObject);
  begin
  MainForm.MenuOptionsMediumDrawClick(MainForm);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuOptionsBestDrawClick(Sender: TObject);
  begin
  MainForm.MenuOptionsBestDrawClick(MainForm);
  end;

procedure TTimeSeriesForm.TimeSeriesMenuOptionsCustomDrawClick(Sender: TObject);
  begin
  MainForm.MenuOptionsCustomDrawClick(MainForm);
  end;

end.
