unit Ubreedr;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, StdCtrls, Grids, ExtCtrls,
  ucollect, uplant, ugener, Buttons, Menus,
  updform, Spin;

type
  TBreederForm = class(PdForm)
    plantsDrawGrid: TDrawGrid;
    BreederMenu: TMainMenu;
    BreederMenuEdit: TMenuItem;
    BreederMenuCopy: TMenuItem;
    BreederMenuPaste: TMenuItem;
    N2: TMenuItem;
    BreederMenuPlant: TMenuItem;
    BreederMenuBreed: TMenuItem;
    BreederMenuUndo: TMenuItem;
    BreederMenuRedo: TMenuItem;
    N1: TMenuItem;
    BreederMenuDeleteRow: TMenuItem;
    BreederMenuDeleteAll: TMenuItem;
    BreederPopupMenu: TPopupMenu;
    BreederPopupMenuBreed: TMenuItem;
    BreederPopupMenuCopy: TMenuItem;
    BreederPopupMenuPaste: TMenuItem;
    BreederPopupMenuDeleteRow: TMenuItem;
    N4: TMenuItem;
    BreederMenuRandomize: TMenuItem;
    BreederMenuRandomizeAll: TMenuItem;
    BreederMenuMakeTimeSeries: TMenuItem;
    BreederPopupMenuRandomize: TMenuItem;
    N5: TMenuItem;
    emptyWarningPanel: TPanel;
    Label1: TLabel;
    BreederPopupMenuMakeTimeSeries: TMenuItem;
    BreederMenuVariation: TMenuItem;
    BreederMenuVariationLow: TMenuItem;
    BreederMenuVariationMedium: TMenuItem;
    BreederMenuVariationHigh: TMenuItem;
    BreederMenuVariationCustom: TMenuItem;
    BreederMenuOptions: TMenuItem;
    BreederMenuOtherOptions: TMenuItem;
    MenuBreederHelp: TMenuItem;
    BreederMenuHelpOnBreeding: TMenuItem;
    BreederMenuHelpTopics: TMenuItem;
    N3: TMenuItem;
    BreederMenuOptionsDrawAs: TMenuItem;
    BreederMenuOptionsFastDraw: TMenuItem;
    BreederMenuOptionsMediumDraw: TMenuItem;
    BreederMenuOptionsBestDraw: TMenuItem;
    BreederMenuOptionsCustomDraw: TMenuItem;
    N6: TMenuItem;
    BreederMenuVaryColors: TMenuItem;
    BreederMenuVary3DObjects: TMenuItem;
    breederToolbarPanel: TPanel;
    variationLow: TSpeedButton;
    variationMedium: TSpeedButton;
    variationCustom: TSpeedButton;
    varyColors: TSpeedButton;
    vary3DObjects: TSpeedButton;
    helpButton: TSpeedButton;
    variationHigh: TSpeedButton;
    BreederMenuVariationNone: TMenuItem;
    variationNoneNumeric: TSpeedButton;
    BreederMenuSendCopyToMainWindow: TMenuItem;
    N7: TMenuItem;
    BreederPopupMenuSendCopytoMainWindow: TMenuItem;
    N8: TMenuItem;
    breedButton: TSpeedButton;
    BreederMenuUndoRedoList: TMenuItem;
    procedure FormCreate(Sender: TObject);
    procedure FormDestroy(Sender: TObject);
    procedure FormResize(Sender: TObject);
    procedure plantsDrawGridDrawCell(Sender: TObject; Col, Row: Longint;
      Rect: TRect; State: TGridDrawState);
    procedure plantsDrawGridMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure plantsDrawGridDragOver(Sender, Source: TObject; X,
      Y: Integer; State: TDragState; var Accept: Boolean);
    procedure plantsDrawGridMouseDown(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure plantsDrawGridEndDrag(Sender, Target: TObject; X,
      Y: Integer);
    procedure BreederMenuBreedClick(Sender: TObject);
    procedure BreederMenuCopyClick(Sender: TObject);
    procedure BreederMenuPasteClick(Sender: TObject);
    procedure BreederMenuUndoClick(Sender: TObject);
    procedure BreederMenuRedoClick(Sender: TObject);
    procedure BreederMenuDeleteRowClick(Sender: TObject);
    procedure BreederMenuDeleteAllClick(Sender: TObject);
    procedure BreederPopupMenuBreedClick(Sender: TObject);
    procedure BreederPopupMenuCopyClick(Sender: TObject);
    procedure BreederPopupMenuPasteClick(Sender: TObject);
    procedure BreederPopupMenuDeleteRowClick(Sender: TObject);
    procedure BreederMenuRandomizeClick(Sender: TObject);
    procedure BreederMenuRandomizeAllClick(Sender: TObject);
    procedure plantsDrawGridDblClick(Sender: TObject);
    procedure BreederMenuMakeTimeSeriesClick(Sender: TObject);
    procedure BreederPopupMenuRandomizeClick(Sender: TObject);
    procedure helpButtonClick(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure BreederPopupMenuMakeTimeSeriesClick(Sender: TObject);
    procedure BreederMenuVariationLowClick(Sender: TObject);
    procedure BreederMenuVariationMediumClick(Sender: TObject);
    procedure BreederMenuVariationHighClick(Sender: TObject);
    procedure BreederMenuVariationCustomClick(Sender: TObject);
    procedure BreederMenuOtherOptionsClick(Sender: TObject);
    procedure BreederMenuHelpOnBreedingClick(Sender: TObject);
    procedure BreederMenuHelpTopicsClick(Sender: TObject);
    procedure BreederMenuOptionsFastDrawClick(Sender: TObject);
    procedure BreederMenuOptionsMediumDrawClick(Sender: TObject);
    procedure BreederMenuOptionsBestDrawClick(Sender: TObject);
    procedure BreederMenuOptionsCustomDrawClick(Sender: TObject);
    procedure BreederMenuVaryColorsClick(Sender: TObject);
    procedure BreederMenuVary3DObjectsClick(Sender: TObject);
    procedure variationLowClick(Sender: TObject);
    procedure variationMediumClick(Sender: TObject);
    procedure variationHighClick(Sender: TObject);
    procedure variationCustomClick(Sender: TObject);
    procedure varyColorsClick(Sender: TObject);
    procedure vary3DObjectsClick(Sender: TObject);
    procedure BreederMenuVariationNoneClick(Sender: TObject);
    procedure variationNoneNumericClick(Sender: TObject);
    procedure BreederMenuSendCopyToMainWindowClick(Sender: TObject);
    procedure BreederPopupMenuSendCopytoMainWindowClick(Sender: TObject);
    procedure breedButtonClick(Sender: TObject);
    procedure BreederMenuUndoRedoListClick(Sender: TObject);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
  public
    { Public declarations }
    selectedRow: smallint;
    generations: TListCollection;
    dragPlantStartPoint, lightUpCell: TPoint;
    numBreederPlantsCopiedThisSession: longint;
    internalChange: boolean;
    drawing: boolean;
    needToRedrawFromChangeToDrawOptions: boolean;
    function selectedGeneration: PdGeneration;
    function primarySelectedPlant: PdPlant;
    function plantAtMouse(x, y: smallint): PdPlant;
    function generationForIndex(index: smallint): PdGeneration;
    function plantForRowAndColumn(row, column: smallint): PdPlant;
    procedure replacePlantInRow(oldPlant, newPlant: PdPlant; row: smallint);
    procedure forgetGenerationsListBelowRow(aRow: smallint);
    procedure addGenerationsFromListBelowRow(aRow: smallint; aGenerationsList: TList);
    procedure forgetLastGeneration;
    procedure addGeneration(newGeneration: PdGeneration);
    procedure selectGeneration(aGeneration: PdGeneration);
    procedure deselectAllGenerations;
    procedure updateForChangeToGenerations;
    procedure updateForChangeToPlant(aPlant: PdPlant);
    procedure updateForChangeToSelections(selectionIsInFirstColumn: boolean);
    procedure redoCaption;
    procedure updateMenusForChangeToGenerations;
    procedure updateMenusForChangeToSelection;
    procedure updatePasteMenuForClipboardContents;
    procedure copyPlantToPoint(aPlant: PdPlant; x,y: integer);
    function inGrid(row, column: smallint): boolean;
    procedure fullWarning;
    procedure updateForChangeToDomainOptions;
    procedure invalidateGridCell(column, row: longint);
    procedure invalidateGridRow(row: longint);
    procedure redrawPlants(considerIfPreviewCacheIsUpToDate: boolean);
    procedure changeBreederAndTimeSeriesOptions(tabIndexToShow: smallint);
		function GetPalette: HPALETTE; override;
		function PaletteChanged(Foreground: Boolean): Boolean; override;
    end;

var
  BreederForm: TBreederForm;

const
  kRedrawPlants = true; kDontRedrawPlants = false;
  kConsiderIfPreviewCacheIsUpToDate = true; kDontConsiderIfPreviewCacheIsUpToDate = false;

implementation

{$R *.DFM}

uses 
  udomain, ubrdopt, usupport, ucursor, umath, umain, ucommand, updcom, utimeser, ubmpsupport;

const
  kSelectionIsInFirstColumn = true; kSelectionIsNotInFirstColumn = false;
  kFirstColumnWidth = 20;
  kBetweenGap = 4;
  kOptionTabSize = 0; kOptionTabMutation = 1; kOptionTabBlending = 2; kOptionTabNonNumeric = 3; kOptionTabTdos = 4;

{ ---------------------------------------------------------------------------- creation/destruction }
procedure TBreederForm.FormCreate(Sender: TObject);
  var
    tempBoundsRect: TRect;
  begin
  generations := TListCollection.create;
  plantsDrawGrid.dragCursor := crDragPlant;
  self.position := poDesigned;
  { keep window on screen - left corner of title bar }
  tempBoundsRect := domain.breederWindowRect;
  with tempBoundsRect do
    if (left <> 0) or (right <> 0) or (top <> 0) or (bottom <> 0) then
      begin
      if left > screen.width - kMinWidthOnScreen then left := screen.width - kMinWidthOnScreen;
      if top > screen.height - kMinHeightOnScreen then top := screen.height - kMinHeightOnScreen;
      self.setBounds(left, top, right, bottom);
      end;
  case domain.options.drawSpeed of
    kDrawFast: BreederMenuOptionsFastDraw.checked := true;
    kDrawMedium: BreederMenuOptionsMediumDraw.checked := true;
    kDrawBest: BreederMenuOptionsBestDraw.checked := true;
    kDrawCustom: BreederMenuOptionsCustomDraw.checked := true;
    end;
  self.updateForChangeToDomainOptions;
  self.updateMenusForChangeToGenerations;
  MainForm.updateMenusForUndoRedo; {to get redo messages}
  lightUpCell := Point(-1, -1);
  emptyWarningPanel.sendToBack;
  end;

procedure TBreederForm.FormDestroy(Sender: TObject);
  begin
  generations.free;
  generations := nil;
  end;

procedure TBreederForm.FormActivate(Sender: TObject);
  begin
  if Application.terminated then exit;
  if generations.count <= 0 then
    emptyWarningPanel.bringToFront                        
  else if self.needToRedrawFromChangeToDrawOptions then
    begin
    self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate);
    self.needToRedrawFromChangeToDrawOptions := false;
    end;
  end;

{ -------------------------------------------------------------------------------------- grid }
procedure TBreederForm.updateForChangeToDomainOptions;
  var
    generation: PdGeneration;
    plant: PdPlant;
    genCount, plCount: smallint;
    newAge: integer;
    atLeastOnePlantHasChangedAge: boolean;
  begin
  if plantsDrawGrid.colCount <> domain.breedingAndTimeSeriesOptions.plantsPerGeneration + 1 then
    plantsDrawGrid.colCount := domain.breedingAndTimeSeriesOptions.plantsPerGeneration + 1;
  with plantsDrawGrid do
    begin
    if ((defaultColWidth <> domain.breedingAndTimeSeriesOptions.thumbnailWidth)
        or (defaultRowHeight <> domain.breedingAndTimeSeriesOptions.thumbnailHeight)) then
      begin
      defaultColWidth := domain.breedingAndTimeSeriesOptions.thumbnailWidth;
      colWidths[0] := kFirstColumnWidth;
      defaultRowHeight := domain.breedingAndTimeSeriesOptions.thumbnailHeight;
      self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate);
      end;
    end;
  case domain.breedingAndTimeSeriesOptions.variationType of
    kBreederVariationLow:
      begin
      BreederMenuVariationLow.checked := true;
      variationLow.down := true;
      end;
    kBreederVariationMedium:
      begin
      BreederMenuVariationMedium.checked := true;
      variationMedium.down := true;
      end;
    kBreederVariationHigh:
      begin
      BreederMenuVariationHigh.checked := true;
      variationHigh.down := true;
      end;
    kBreederVariationCustom:
      begin
      BreederMenuVariationCustom.checked := true;
      variationCustom.down := true;
      end;
    kBreederVariationNoNumeric:
      begin
      BreederMenuVariationNone.checked := true;
      variationNoneNumeric.down := true;
      end;
    end;
  BreederMenuVaryColors.checked := domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues;
  varyColors.down := domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues;
  BreederMenuVary3DObjects.checked := domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary;
  vary3DOBjects.down := domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary;
  self.redoCaption;
  atLeastOnePlantHasChangedAge := false;
  if generations.count > 0 then for genCount := 0 to generations.count - 1 do
    begin
    generation := PdGeneration(generations.items[genCount]);
    if generation.plants.count > 0 then for plCount := 0 to generation.plants.count - 1 do
      begin
      plant := PdPlant(generation.plants.items[plCount]);
      newAge := round(domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0 * plant.pGeneral.ageAtMaturity);
      if plant.age <> newAge then
        begin
        plant.setAge(newAge);
        atLeastOnePlantHasChangedAge := true;
        end;
      end;
    end;
  if atLeastOnePlantHasChangedAge then
    self.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate);
  end;

procedure TBreederForm.redrawPlants(considerIfPreviewCacheIsUpToDate: boolean);
  var
    generation: PdGeneration;
    plant: PdPlant;
    genCount, plCount: smallint;
  begin
  if not considerIfPreviewCacheIsUpToDate then
    begin
    for genCount := 0 to generations.count - 1 do
      begin
      generation := PdGeneration(generations.items[genCount]);
      if generation.plants.count > 0 then for plCount := 0 to generation.plants.count - 1 do
        begin
        plant := PdPlant(generation.plants.items[plCount]);
        plant.previewCacheUpToDate := false;
        end;
      end;
    end;
  plantsDrawGrid.invalidate;
  plantsDrawGrid.update;
  end;

procedure TBreederForm.plantsDrawGridDrawCell(Sender: TObject; Col, Row: Longint; Rect: TRect; State: TGridDrawState);
  var
    generation: PdGeneration;
    plant: PdPlant;
    textDrawRect: TRect;
  begin
  try
  plantsDrawGrid.canvas.font := plantsDrawGrid.font;
  plantsDrawGrid.canvas.font.color := clBlack;
  if col = 0 then
    begin
    //if (row = selectedRow) and (generations.count > 0) then
      //plantsDrawGrid.canvas.brush.color := clBlue
    //else
      plantsDrawGrid.canvas.brush.color := clWhite;
    plantsDrawGrid.canvas.pen.color := plantsDrawGrid.canvas.brush.color;
    plantsDrawGrid.canvas.rectangle(rect.left, rect.top, rect.right, rect.bottom);
    if row > generations.count - 1 then exit;
    //if row = selectedRow then
      //plantsDrawGrid.canvas.font.color := clWhite;
    textDrawRect.left := rect.left + rWidth(rect) div 2 - plantsDrawGrid.canvas.textWidth(intToStr(row+1)) div 2;
    textDrawRect.top := rect.top + rHeight(rect) div 2 - plantsDrawGrid.canvas.textHeight('0') div 2;
    plantsDrawGrid.canvas.textOut(textDrawRect.left, textDrawRect.top, intToStr(row+1));
    exit;
    end
  else
    begin
    plantsDrawGrid.canvas.brush.color := clWhite;
    plantsDrawGrid.canvas.pen.width := 1;
    plantsDrawGrid.canvas.pen.color := clWhite;
    plantsDrawGrid.canvas.rectangle(rect.left, rect.top, rect.right, rect.bottom);
    end;
  generation := nil;
  generation := self.generationForIndex(row);
  if generation = nil then exit;
  plant := nil;
  plant := generation.plantForIndex(col-1);
  if plant = nil then exit;
  { draw plant }
  if not plant.previewCacheUpToDate then
    begin
    // draw gray solid box to show delay for drawing plant cache
    plantsDrawGrid.canvas.brush.style := bsSolid;
    plantsDrawGrid.canvas.brush.color := clSilver;
    plantsDrawGrid.canvas.pen.color := clSilver;
    with rect do plantsDrawGrid.canvas.rectangle(left+1, top+1, right, bottom);
    // draw plant preview cache
    plant.fixedPreviewScale := false;
    plant.fixedDrawPosition := false;
    plant.drawPreviewIntoCache(
      Point(plantsDrawGrid.defaultColWidth, plantsDrawGrid.defaultRowHeight),
      kDontConsiderDomainScale, kDrawNow);
    end;
  plant.previewCache.transparent := false;
  copyBitmapToCanvasWithGlobalPalette(plant.previewCache, plantsDrawGrid.canvas, rect);
  { draw selection rectangle }
  plantsDrawGrid.canvas.brush.style := bsClear;
  plantsDrawGrid.canvas.pen.width := 2;
  if (col = lightUpCell.x) and (row = lightUpCell.y) then
    plantsDrawGrid.canvas.pen.color := clAqua
  else if row = selectedRow then
    begin
    if plant = generation.firstSelectedPlant then
      plantsDrawGrid.canvas.pen.color := domain.options.firstSelectionRectangleColor
    else if plant = generation.secondSelectedPlant then
      plantsDrawGrid.canvas.pen.color := domain.options.multiSelectionRectangleColor
    else
      plantsDrawGrid.canvas.pen.color := clSilver;
    end
  else
    plantsDrawGrid.canvas.pen.color := clSilver;
  with rect do plantsDrawGrid.canvas.rectangle(left+1, top+1, right, bottom);

  { draw parent indicator }
  if plant = generation.firstParent then
    plantsDrawGrid.canvas.textOut(rect.left+4, rect.top+2, 'p1')
  else if plant = generation.secondParent then
    plantsDrawGrid.canvas.textOut(rect.left+4, rect.top+2, 'p2');
  finally
    cursor_stopWait;
  end;
  end;

procedure TBreederForm.invalidateGridCell(column, row: longint);
  var
    cellRectOver: TRect;
  begin
  if (column < 0) and (row < 0) then exit;
  cellRectOver := plantsDrawGrid.cellRect(column, row);
  invalidateRect(plantsDrawGrid.handle, @cellRectOver, true);
  end;

procedure TBreederForm.invalidateGridRow(row: longint);
  var
    rowRectOver: TRect;
  begin
  if row < 0 then exit;
  rowRectOver := plantsDrawGrid.cellRect(0, row);
  rowRectOver.right := plantsDrawGrid.width;
  invalidateRect(plantsDrawGrid.handle, @rowRectOver, true);
  end;

procedure TBreederForm.plantsDrawGridMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    col, row: longint;
    generation: PdGeneration;
    plant: PdPlant;
  begin
  if application.terminated then exit;
  // had selection here, moved to mouse down because double-click makes extra mouse up, seems okay so far
  end;

procedure TBreederForm.plantsDrawGridDblClick(Sender: TObject);
  begin
  self.BreederMenuBreedClick(self);
  end;

{ ------------------------------------------------------------------------ dragging }
procedure TBreederForm.plantsDrawGridMouseDown(Sender: TObject;
    Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    plant: PdPlant;
    col, row, oldSelectedRow: integer;
    generation: PdGeneration;
  begin
  plantsDrawGrid.mouseToCell(x, y, col, row);
  if (row >= 0) and (row <= generations.count - 1) then
    begin
    generation := PdGeneration(generations.items[row]);
    if generation <> nil then
      begin
      self.selectGeneration(generation);
      if (col >= 1) and (col - 1 <= generation.plants.count - 1) then
        begin
        plant := PdPlant(generation.plants.items[col - 1]);
        if plant <> nil then
          generation.selectPlant(plant, (ssShift in shift))
        else
          generation.deselectAllPlants;
        end
      else { in first column or past them on right }
        generation.deselectAllPlants;
      end
    else
      self.deselectAllGenerations;
    end
  else
    self.deselectAllGenerations;
  self.updateForChangeToGenerations;
  // start drag of plant
  if (button = mbRight) or (ssShift in shift) then exit;
  plant := self.plantAtMouse(x, y);
  if plant = nil then exit;
  dragPlantStartPoint := Point(x, y);
  plantsDrawGrid.beginDrag(false);
  end;

procedure TBreederForm.plantsDrawGridDragOver(Sender, Source: TObject; X,
    Y: Integer; State: TDragState; var Accept: Boolean);
  var
    col, row: longint;
    plant: PdPlant;
  begin
  accept := (source <> nil) and (sender <> nil)
    and (
      (sender = source)
      or (source = MainForm.drawingPaintBox)
      or (source = MainForm.plantListDrawGrid)
      or (source = TimeSeriesForm.grid));
  if (accept) then
    begin
    plant := self.plantAtMouse(x, y);
    if plant = nil then
      begin
      accept := false;
      exit;
      end;
    plantsDrawGrid.mouseToCell(x, y, col, row);
    if (col <> lightUpCell.x) or (row <> lightUpCell.y) then
      begin
      self.invalidateGridCell(lightUpCell.x, lightUpCell.y);
      lightUpCell := Point(col, row);
      self.invalidateGridCell(col, row);
      end;
    end;
  end;

procedure TBreederForm.plantsDrawGridEndDrag(Sender, Target: TObject; X, Y: Integer);
  var
    col, row: longint;
    plant, plantToReplace: PdPlant;
    newCommand: PdCommand;
    newPlants: TList;
    newPlant: PdPlant;
  begin
  if application.terminated then exit;
  // remove lightup on cell before resetting cell
  self.invalidateGridCell(lightUpCell.x, lightUpCell.y);
  lightUpCell := Point(-1, -1);
  if target = nil then exit;
  { get plant being dragged }
  plant := self.plantAtMouse(dragPlantStartPoint.x, dragPlantStartPoint.y);
  if plant = nil then exit;
  if (target = MainForm.drawingPaintBox) or (target = MainForm.plantListDrawGrid) then
    begin
    { make paste command - wants list of plants }
    newPlant := PdPlant.create;
    plant.copyTo(newPlant);
    inc(numBreederPlantsCopiedThisSession);
    newPlant.setName('Breeder plant ' + intToStr(numBreederPlantsCopiedThisSession));
    if (target = MainForm.drawingPaintBox) then
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
    try
      cursor_startWait;
      MainForm.doCommand(newCommand);
    finally
      newPlants.free; {command has another list, so we must free this one}
      cursor_stopWait;
    end;
    {command will free plant if paste is undone}
    end
  else if target = TimeSeriesForm.grid then
    begin
    TimeSeriesForm.copyPlantToPoint(plant, x, y);
    end
  else if target = sender then
    begin
    { get plant being replaced }
    plantsDrawGrid.mouseToCell(x, y, col, row);
    if not inGrid(row, col) then exit;
    plantToReplace := plantForRowAndColumn(row, col);
    if plantToReplace = nil then exit;
    if plantToReplace = plant then exit;
    { make replace command }
    newCommand := PdReplaceBreederPlant.createWithPlantRowAndColumn(plant, row, col);
    try
      cursor_startWait;
      MainForm.doCommand(newCommand);
    finally
      cursor_stopWait;
    end;
    end;
  end;

procedure TBreederForm.copyPlantToPoint(aPlant: PdPlant; x,y: integer);
  var
    col, row: longint;
    plant: PdPlant;
    newCommand: PdCommand;
  begin
  plantsDrawGrid.mouseToCell(x, y, col, row);
  plant := plantForRowAndColumn(row, col);
  if plant = nil then exit;
  newCommand := PdReplaceBreederPlant.createWithPlantRowAndColumn(aPlant, row, col);
  MainForm.doCommand(newCommand);
  end;

{ ------------------------------------------------------------- responding to commands }
procedure TBreederForm.replacePlantInRow(oldPlant, newPlant: PdPlant; row: smallint);
  var
    generation: PdGeneration;
  begin
  generation := self.generationForIndex(row);
  if generation = nil then
    raise Exception.create('Problem: Invalid row in method TBreederForm.replacePlantInRow.');
  generation.replacePlant(oldPlant, newPlant);
  self.updateForChangeToPlant(newPlant);
  end;

procedure TBreederForm.forgetGenerationsListBelowRow(aRow: smallint);
  begin
  while generations.count - 1 > aRow do
    self.forgetLastGeneration;
  end;

procedure TBreederForm.addGenerationsFromListBelowRow(aRow: smallint; aGenerationsList: TList);
  var
    i: smallint;
  begin
  if aRow + 1 <= aGenerationsList.count - 1 then for i := aRow + 1 to aGenerationsList.count - 1 do
    self.addGeneration(PdGeneration(aGenerationsList.items[i]));
  end;

procedure TBreederForm.addGeneration(newGeneration: PdGeneration);
  begin
  generations.add(newGeneration);
  end;

procedure TBreederForm.forgetLastGeneration;
  var
    lastGeneration: PdGeneration;
  begin
  if generations.count <= 0 then exit;
  lastGeneration := PdGeneration(generations.items[generations.count - 1]);
  generations.remove(lastGeneration);
  end;

procedure TBreederForm.selectGeneration(aGeneration: PdGeneration);
  var
    lastFullyVisibleRow: smallint;
  begin
  self.selectedRow := generations.indexOf(aGeneration);
  with plantsDrawGrid do
    begin
    lastFullyVisibleRow := topRow + visibleRowCount - 1;
    if selectedRow > lastFullyVisibleRow then
      topRow := topRow + (selectedRow - lastFullyVisibleRow);
    if selectedRow < topRow then
      topRow := selectedRow;
    end;
  end;

procedure TBreederForm.deselectAllGenerations;
  var
    genCount: integer;
    generation: PdGeneration;
  begin
  self.selectedRow := -1;
  for genCount := 0 to generations.count - 1 do
    begin
    generation := PdGeneration(generations.items[genCount]);
    generation.deselectAllPlants;
    end;
  end;

procedure TBreederForm.updateForChangeToGenerations;
  begin
  self.updateMenusForChangeToGenerations;
  internalChange := true;
  if not self.visible then self.show; {calls resize}
  self.bringToFront;
  if self.windowState = wsMinimized then self.windowState := wsNormal;
  internalChange := false;
  if plantsDrawGrid.rowCount < generations.count then
    plantsDrawGrid.rowCount := generations.count;
  plantsDrawGrid.invalidate;
  plantsDrawGrid.update;
  self.redoCaption;
  if generations.count <= 0 then
    emptyWarningPanel.bringToFront
  else
    emptyWarningPanel.sendToBack;
  end;

procedure TBreederForm.updateForChangeToPlant(aPlant: PdPlant);
  var
    genCount, plCount: integer;
    generation: PdGeneration;
    plant: PdPlant;
    cellRectOver: TRect;
  begin
  for genCount := 0 to generations.count - 1 do
    begin
    generation := PdGeneration(generations.items[genCount]);
    if generation.plants.count > 0 then for plCount := 0 to generation.plants.count - 1 do
      begin
      plant := PdPlant(generation.plants.items[plCount]);
      if plant = aPlant then
        begin
        cellRectOver := plantsDrawGrid.cellRect(plCount+1, genCount);
        self.plantsDrawGridDrawCell(self, plCount+1, genCount, cellRectOver, [gdFocused, gdSelected]);
        exit;
        end;
      end;
    end;
  end;

procedure TBreederForm.updateForChangeToSelections(selectionIsInFirstColumn: boolean);
  var
    i: integer;
    plant: PdPlant;
  begin
  self.updateMenusForChangeToSelection;
  {
  if selectedPlants.count > 0 then
    for i := 0 to selectedPlants.count - 1 do
      begin
      plant := PdPlant(selectedPlants.items[i]);
      self.updateForChangeToPlant(plant);
      end;
      }
  //if selectionIsInFirstColumn then
    plantsDrawGrid.invalidate;
  end;

    {
procedure TBreederForm.updateForChangeToSelections;
  begin
  for genCount := 0 to generations.count - 1 do
    begin
    generation := PdGeneration(generations.items[genCount]);
    if generation.plants.count > 0 then for plCount := 0 to generation.plants.count - 1 do
      begin
      plant := PdPlant(generation.plants.items[plCount]);
      if generation.plantWasSelected(plant) then
        self.plantsDrawGridDrawCell(self, plCount+1, genCount, plantsDrawGrid.cellRect(plCount+1, genCount), []);
      if generation.plantIsSelected(plant) then
        self.plantsDrawGridDrawCell(self, plCount+1, genCount, plantsDrawGrid.cellRect(plCount+1, genCount), []);
      end;
    end;
  end;
    }
procedure TBreederForm.redoCaption;
  begin
  if generations.count = 1 then  // new v1.4
    self.caption := 'Breeder (1 generation)'
  else
    self.caption := 'Breeder (' + intToStr(generations.count) + ' generations)';
  {
  self.caption := self.caption + ', numbers ';
  case domain.breedingAndTimeSeriesOptions.variationType of
    kBreederVariationNoNumeric: self.caption := self.caption + none ;
    kBreederVariationLow:     self.caption := self.caption + 'low' ;
    kBreederVariationMedium:  self.caption := self.caption + 'medium' ;
    kBreederVariationHigh:    self.caption := self.caption + 'high' ;
    kBreederVariationCustom:  self.caption := self.caption + 'custom' ;
    end;
  if domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues then
    self.caption := self.caption + ', colors on'
  else
    self.caption := self.caption + ', colors off'
  if domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary then
    self.caption := self.caption + ', 3D objects on'
  else
    self.caption := self.caption + ', 3D objects off'
    }
  end;

procedure TBreederForm.updateMenusForChangeToGenerations;
  var
    havePlants: boolean;
  begin
  havePlants := generations.count > 0;
  BreederMenuDeleteAll.enabled := havePlants;
  BreederMenuRandomizeAll.enabled := havePlants;
  self.updateMenusForChangeToSelection;
  end;

procedure TBreederForm.updateMenusForChangeToSelection;
  var
    haveSelection: boolean;
  begin
  haveSelection := (self.primarySelectedPlant <> nil);
  BreederMenuRandomize.enabled := haveSelection;
  BreederMenuDeleteRow.enabled := haveSelection;
  BreederPopupMenuDeleteRow.enabled := haveSelection;
  BreederMenuBreed.enabled := haveSelection;
  BreederMenuMakeTimeSeries.enabled := haveSelection;
  BreederMenuCopy.enabled := haveSelection;
  BreederPopupMenuBreed.enabled := BreederMenuBreed.enabled;
  breedButton.enabled := BreederMenuBreed.enabled;
  BreederPopupMenuMakeTimeSeries.enabled := BreederMenuMakeTimeSeries.enabled;
  BreederPopupMenuCopy.enabled := BreederMenuCopy.enabled;
  BreederPopupMenuRandomize.enabled := BreederMenuRandomize.enabled;
  self.updatePasteMenuForClipboardContents;
  { must paste onto a selected plant }
  BreederMenuPaste.enabled := BreederMenuPaste.enabled and haveSelection;
  BreederPopupMenuPaste.enabled := BreederMenuPaste.enabled;
  end;

procedure TBreederForm.updatePasteMenuForClipboardContents;
  begin
  BreederMenuPaste.enabled := (self.primarySelectedPlant <> nil)
      and (domain.plantManager.privatePlantClipboard.count > 0);
  BreederPopupMenuPaste.enabled := BreederMenuPaste.enabled;
  end;

function TBreederForm.selectedGeneration: PdGeneration;
  begin
  result := nil;
  if (selectedRow < 0) or (selectedRow > generations.count - 1) then exit;
  result := PdGeneration(generations.items[selectedRow]);
  end;

function TBreederForm.primarySelectedPlant: PdPlant;
  var
    generation: PdGeneration;
  begin
  result := nil;
  generation := self.selectedGeneration;
  if generation = nil then exit;
  result := generation.firstSelectedPlant;
  end;

function TBreederForm.plantAtMouse(x, y: smallint): PdPlant;
  var
    col, row: longint;
  begin
  result := nil;
  plantsDrawGrid.mouseToCell(x, y, col, row);
  if not inGrid(row, col) then exit;
  result := plantForRowAndColumn(row, col);
  end;

{ ----------------------------------------------------------------------------- menu }
procedure TBreederForm.BreederMenuUndoClick(Sender: TObject);
  begin
  MainForm.menuEditUndoClick(sender);
  end;

procedure TBreederForm.BreederMenuRedoClick(Sender: TObject);
  begin
  MainForm.menuEditRedoClick(sender);
  end;

procedure TBreederForm.BreederMenuCopyClick(Sender: TObject);
  var
    plant: PdPlant;
    copyList: TList;
    saveName: string;
  begin
  plant := self.primarySelectedPlant;
  if plant = nil then exit;
  copyList := TList.create;
  copyList.add(plant);
  { temporarily change plant name to make copy, then put back }
  saveName := plant.getName;
  inc(numBreederPlantsCopiedThisSession);
  plant.setName('Breeder plant ' + intToStr(numBreederPlantsCopiedThisSession));
  domain.plantManager.copyPlantsInListToPrivatePlantClipboard(copyList);
  plant.setName(saveName);
  MainForm.updatePasteMenuForClipboardContents; {sets our paste menu also}
  end;

procedure TBreederForm.BreederMenuSendCopyToMainWindowClick(Sender: TObject);
  begin
  self.BreederMenuCopyClick(self);
  MainForm.MenuEditPasteClick(MainForm);
  end;

procedure TBreederForm.BreederMenuUndoRedoListClick(Sender: TObject);
  begin
  MainForm.UndoMenuEditUndoRedoListClick(MainForm);
  end;

procedure TBreederForm.BreederMenuPasteClick(Sender: TObject);
  var
    generation: PdGeneration;
    plant, newPlant: PdPlant;
    newCommand: PdCommand;
    column: smallint;
  begin
  if domain.plantManager.privatePlantClipboard.count <= 0 then exit;
  generation := self.selectedGeneration;
  if generation = nil then exit;
  plant := generation.firstSelectedPlant;
  if plant = nil then exit;
  column := generation.plants.indexOf(plant) + 1;
  newPlant := PdPlant.create;
  domain.plantManager.pasteFirstPlantFromPrivatePlantClipboardToPlant(newPlant);
  newCommand := PdReplaceBreederPlant.createWithPlantRowAndColumn(newPlant, selectedRow, column);
  MainForm.doCommand(newCommand);
  {command will free plant if paste is undone}
  end;

procedure TBreederForm.BreederMenuBreedClick(Sender: TObject);
  var
    generationToBreed: PdGeneration;
    newCommand: PdCommand;
  begin
  if (selectedRow < 0) or (selectedRow > generations.count - 1) then exit;
  { check if there is room in the breeder - this command will make one new generation }
  if selectedRow >= domain.breedingAndTimeSeriesOptions.maxGenerations - 1 then
    begin
    self.fullWarning;
    exit;
    end;
  generationToBreed := PdGeneration(generations.items[selectedRow]);
  if generationToBreed.selectedPlants.count <= 0 then exit;
  newCommand := PdBreedFromParentsCommand.createWithInfo(generations,
    generationToBreed.firstSelectedPlant, generationToBreed.secondSelectedPlant,
    selectedRow, domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, kDontCreateFirstGeneration);
  generationToBreed.firstParent := generationToBreed.firstSelectedPlant;
  generationToBreed.secondParent := generationToBreed.secondSelectedPlant;
  MainForm.doCommand(newCommand);
  end;

procedure TBreederForm.BreederMenuMakeTimeSeriesClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if self.primarySelectedPlant = nil then exit;
  newCommand := PdMakeTimeSeriesCommand.createWithNewPlant(self.primarySelectedPlant);
  MainForm.doCommand(newCommand);
  end;

procedure TBreederForm.fullWarning;
  begin
  messageDlg('The breeder is full. ' + chr(13) + chr(13)
    + 'You must delete some rows' + chr(13)
    + '(or increase the number of rows allowed in the breeder options) ' + chr(13)
    + 'before you can breed more plants.', mtWarning, [mbOK], 0);
  end;

procedure TBreederForm.BreederMenuDeleteRowClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if self.selectedGeneration = nil then exit;
  newCommand := PdDeleteBreederGenerationCommand.createWithGeneration(selectedGeneration);
  MainForm.doCommand(newCommand);
  end;

procedure TBreederForm.BreederMenuDeleteAllClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if generations.count <= 0 then exit;
  newCommand := PdDeleteAllBreederGenerationsCommand.create;
  MainForm.doCommand(newCommand);
  end;

procedure TBreederForm.BreederMenuRandomizeClick(Sender: TObject);
  var
    newCommand: PdCommand;
    randomizeList: TList;
    aGeneration: PdGeneration;
    i: smallint;
    plant: PdPlant;
  begin
  aGeneration := self.selectedGeneration;
  if aGeneration = nil then exit;
  if aGeneration.selectedPlants.count <= 0 then exit;
  randomizeList := TList.create;
  try
    for i := 0 to aGeneration.selectedPlants.count - 1 do
      begin
      plant := PdPlant(aGeneration.selectedPlants.items[i]);
      randomizeList.add(plant);
      end;
    newCommand := PdRandomizeCommand.createWithListOfPlants(randomizeList);
    (newCommand as PdRandomizeCommand).isInBreeder := true;
    cursor_startWait;
    MainForm.doCommand(newCommand);
  finally
    randomizeList.free; {command has another list, so we must free this one}
    cursor_stopWait;
  end;
  end;

procedure TBreederForm.BreederMenuRandomizeAllClick(Sender: TObject);
  var
    generation: PdGeneration;
    i, j: smallint;
    newCommand: PdCommand;
    randomizeList: TList;
  begin
  if generations.count <= 0 then exit;
  randomizeList := nil;
  try
    cursor_startWait;
    randomizeList := TList.create;
    if generations.count > 0 then for i := 0 to generations.count - 1 do
      begin
      generation := PdGeneration(generations.items[i]);
      if generation.plants.count > 0 then for j := 0 to generation.plants.count - 1 do
        randomizeList.add(PdPlant(generation.plants.items[j]));
      end;
    newCommand := PdRandomizeCommand.createWithListOfPlants(randomizeList);
    (newCommand as PdRandomizeCommand).isInBreeder := true;
    (newCommand as PdRandomizeCommand).isRandomizeAllInBreeder := true;
    MainForm.doCommand(newCommand);
  finally
    randomizeList.free;
    cursor_stopWait;
  end;
  end;

procedure TBreederForm.BreederMenuVariationNoneClick(Sender: TObject);
  begin
  domain.breedingAndTimeSeriesOptions.variationType := kBreederVariationNoNumeric;
  BreederMenuVariationNone.checked := true;
  self.redoCaption;
  end;

procedure TBreederForm.BreederMenuVariationLowClick(Sender: TObject);
  begin
  domain.breedingAndTimeSeriesOptions.variationType := kBreederVariationLow;
  BreederMenuVariationLow.checked := true;
  self.redoCaption;
  end;

procedure TBreederForm.BreederMenuVariationMediumClick(Sender: TObject);
  begin
  domain.breedingAndTimeSeriesOptions.variationType := kBreederVariationMedium;
  BreederMenuVariationMedium.checked := true;
  self.redoCaption;
  end;

procedure TBreederForm.BreederMenuVariationHighClick(Sender: TObject);
  begin
  domain.breedingAndTimeSeriesOptions.variationType := kBreederVariationHigh;
  // this is to deal with if it was turned off by not having a library
  // v2.0 removed - this is separate now
  // domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary := true;
  BreederMenuVariationHigh.checked := true;
  self.redoCaption;
  end;

procedure TBreederForm.BreederMenuVariationCustomClick(Sender: TObject);
  begin
  self.changeBreederAndTimeSeriesOptions(kOptionTabMutation);
  end;

procedure TBreederForm.BreederMenuOtherOptionsClick(Sender: TObject);
  begin
  self.changeBreederAndTimeSeriesOptions(kOptionTabSize);
  end;

procedure TBreederForm.BreederMenuVaryColorsClick(Sender: TObject);
  var
    newCommand: PdCommand;
    options: BreedingAndTimeSeriesOptionsStructure;
  begin
  BreederMenuVaryColors.checked := not BreederMenuVaryColors.checked;
  options := domain.breedingAndTimeSeriesOptions;
  options.mutateAndBlendColorValues := BreederMenuVaryColors.checked;
  newCommand := PdChangeBreedingAndTimeSeriesOptionsCommand.createWithOptionsAndDomainOptions(options, domain.options);
  MainForm.doCommand(newCommand);
  end;

procedure TBreederForm.BreederMenuVary3DObjectsClick(Sender: TObject);
  var
    newCommand: PdCommand;
    options: BreedingAndTimeSeriesOptionsStructure;
  begin
  BreederMenuVary3DObjects.checked := not BreederMenuVary3DObjects.checked;
  options := domain.breedingAndTimeSeriesOptions;
  options.chooseTdosRandomlyFromCurrentLibrary := BreederMenuVary3DObjects.checked;
  newCommand := PdChangeBreedingAndTimeSeriesOptionsCommand.createWithOptionsAndDomainOptions(options, domain.options);
  MainForm.doCommand(newCommand);
  end;

procedure TBreederForm.changeBreederAndTimeSeriesOptions(tabIndexToShow: smallint);
  var
  	optionsForm: TBreedingOptionsForm;
    newCommand, domainCommand: PdCommand;
    response: integer;
  begin
  if tabIndexToShow = kOptionTabMutation then
    begin
    domain.breedingAndTimeSeriesOptions.variationType := kBreederVariationCustom;
    BreederMenuVariationCustom.checked := true;
    self.redoCaption;
    end;
  optionsForm := TBreedingOptionsForm.create(self);
  if optionsForm = nil then
    raise Exception.create('Problem: Could not create breeding options window.');
  try
    optionsForm.breedingOptions.pageIndex := tabIndexToShow;
    optionsForm.initializeWithBreedingAndTimeSeriesOptionsAndDomainOptions(
      domain.breedingAndTimeSeriesOptions, domain.options);
    response := optionsForm.showModal;
    if response = mrOK then
      begin
      newCommand := PdChangeBreedingAndTimeSeriesOptionsCommand.createWithOptionsAndDomainOptions(
        optionsForm.options, optionsForm.domainOptions);
      MainForm.doCommand(newCommand);
      end;
  finally
    optionsForm.free;
    optionsForm := nil;
  end;
  end;

procedure TBreederForm.variationLowClick(Sender: TObject);
  begin
  self.BreederMenuVariationLowClick(self);
  end;

procedure TBreederForm.variationNoneNumericClick(Sender: TObject);
  begin
  self.BreederMenuVariationNoneClick(self);
  end;

procedure TBreederForm.variationMediumClick(Sender: TObject);
  begin
  self.BreederMenuVariationMediumClick(self);
  end;

procedure TBreederForm.variationHighClick(Sender: TObject);
  begin
  self.BreederMenuVariationHighClick(self);
  end;

procedure TBreederForm.variationCustomClick(Sender: TObject);
  begin
  self.BreederMenuVariationCustomClick(self);
  end;

procedure TBreederForm.varyColorsClick(Sender: TObject);
  begin
  self.BreederMenuVaryColorsClick(self);
  end;

procedure TBreederForm.vary3DObjectsClick(Sender: TObject);
  begin
  self.BreederMenuVary3DObjectsClick(self);
  end;

procedure TBreederForm.BreederPopupMenuRandomizeClick(Sender: TObject);
  begin
  self.BreederMenuRandomizeClick(self);
  end;

procedure TBreederForm.BreederPopupMenuBreedClick(Sender: TObject);
  begin
  self.BreederMenuBreedClick(self);
  end;

procedure TBreederForm.breedButtonClick(Sender: TObject);
  begin
  self.BreederMenuBreedClick(self);
  end;

procedure TBreederForm.BreederPopupMenuMakeTimeSeriesClick(Sender: TObject);
  begin
  self.BreederMenuMakeTimeSeriesClick(self);
  end;

procedure TBreederForm.BreederPopupMenuCopyClick(Sender: TObject);
  begin
  self.BreederMenuCopyClick(self);
  end;

procedure TBreederForm.BreederPopupMenuPasteClick(Sender: TObject);
  begin
  self.BreederMenuPasteClick(self);
  end;

procedure TBreederForm.BreederPopupMenuSendCopytoMainWindowClick(Sender: TObject);
  begin
  self.BreederMenuSendCopyToMainWindowClick(self);
  end;

procedure TBreederForm.BreederPopupMenuDeleteRowClick(Sender: TObject);
  begin
  self.BreederMenuDeleteRowClick(self);
  end;

{ --------------------------------------------------------------------------- utilities }
function TBreederForm.inGrid(row, column: smallint): boolean;
  begin
  result := true;
  if (row < 0) or (row > generations.count - 1) then result := false;
  if (column < 1) or (column - 1 > plantsDrawGrid.colCount - 1) then result := false;
  end;

function TBreederForm.generationForIndex(index: smallint): PdGeneration;
  begin
  result := nil;
  if index < 0 then exit;
  if index > generations.count - 1 then exit;
  if generations.items[index] = nil then exit;
  result := PdGeneration(generations.items[index]);
  end;

function TBreederForm.plantForRowAndColumn(row, column: smallint): PdPlant;
  var
    generation: PdGeneration;
  begin
  result := nil;
  generation := self.generationForIndex(row);
  if generation = nil then exit;
  result := generation.plantForIndex(column-1);
  end;

{ ---------------------------------------------------------------------------- resizing }
procedure TBreederForm.FormResize(Sender: TObject);
  begin
  if Application.terminated then exit;
  if generations = nil then exit;
  with breederToolbarPanel do setBounds(0, 0, self.clientWidth, height);
  with helpButton do setBounds(breederToolbarPanel.width - width - 4, top, width, height);
  with plantsDrawGrid do setBounds(0, breederToolbarPanel.height,
      self.clientWidth, self.clientHeight - breederToolbarPanel.height);
  with emptyWarningPanel do
    setBounds(self.clientWidth div 2 - width div 2, self.clientHeight div 2 - height div 2, width, height);
  end;

procedure TBreederForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 250;
    ptMinTrackSize.y := 150;
    end;
  end;

procedure TBreederForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Breeding_plants_using_the_breeder');
  end;

{ ----------------------------------------------------------------------------- *palette stuff }
function TBreederForm.GetPalette: HPALETTE;
  begin
  result := MainForm.paletteImage.picture.bitmap.palette;
  end;

function TBreederForm.PaletteChanged(Foreground: Boolean): Boolean;
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
      and (plantsDrawGrid <> nil) then
        begin
    	  plantsDrawGrid.invalidate;
        end;
    selectPalette(DC, oldPalette, True);
    realizePalette(DC);
    releaseDC(windowHandle, DC);
  	end;
  result := inherited paletteChanged(foreground);
	end;

procedure TBreederForm.BreederMenuHelpOnBreedingClick(Sender: TObject);
  begin
  application.helpJump('Breeding_plants_using_the_breeder');
  end;

procedure TBreederForm.BreederMenuHelpTopicsClick(Sender: TObject);
  begin
  application.helpCommand(HELP_FINDER, 0);
  end;

procedure TBreederForm.BreederMenuOptionsFastDrawClick(Sender: TObject);
  begin
  MainForm.MenuOptionsFastDrawClick(MainForm);
  end;

procedure TBreederForm.BreederMenuOptionsMediumDrawClick(Sender: TObject);
  begin
  MainForm.MenuOptionsMediumDrawClick(MainForm);
  end;

procedure TBreederForm.BreederMenuOptionsBestDrawClick(Sender: TObject);
  begin
  MainForm.MenuOptionsBestDrawClick(MainForm);
  end;

procedure TBreederForm.BreederMenuOptionsCustomDrawClick(Sender: TObject);
  begin
  MainForm.MenuOptionsCustomDrawClick(MainForm);
  end;


end.

