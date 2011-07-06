unit Ustats;

interface

uses WinTypes, WinProcs, Controls, ExtCtrls, Graphics, Forms, Classes, 
  uplant, uppanel, utravers;

type

PdStatsPanel = class(PdParameterPanel)
	public
  drawBitmap: TBitmap;
  statistics: PdPlantStatistics;
  graphRect, percentRect: TRect;
  labelRects: array[0..kStatisticsPartTypeLast] of TRect;
  maxLabelWidth: smallint;
  constructor create(anOwner: TComponent); override;
  destructor destroy; override;
  procedure updateHint;
  procedure updatePlantValues; override;
  procedure updateCurrentValue(aFieldIndex: integer); override;
  procedure updatePlant(newPlant: PdPlant); override;
  procedure updateDisplay; override;
  procedure paint; override;
  procedure resizeElements; override;
  procedure drawGraph;
  procedure drawBar(index: integer; amount_pctMPB: single);
  function maxSelectedItemIndex: integer; override;
  procedure collapseOrExpand(y: integer); override;
  procedure drawTextLabel(text: string; drawRect: TRect; active, drawLine, drawBox: boolean);
  function collapsedHeight: integer; override;
  function nameForPartType(partType: smallint; isSingular: boolean): string;
  function partTypeForIndex(partType: smallint): smallint;
  function labelStringForPartType(index: smallint): string;
  function displayPercentForPartType(partType: smallint; livingDeadOrBoth: smallint): single;
  function numNonZeroPlantParts: smallint;
  end;

implementation

uses SysUtils, Dialogs,
  usupport, umath, udomain, ubmpsupport;

const
  kLive = 0; kDead = 1; kBothLiveAndDead = 2;

constructor PdStatsPanel.create(anOwner: TComponent);
  begin
  inherited create(anOwner);
  self.plant := nil;
  self.popupMenu := nil;
  drawBitmap := TBitmap.create;
  statistics := PdPlantStatistics.create;
  self.parentFont := true;
  self.onMouseUp := self.doMouseUp;
  self.onKeyDown := self.doKeyDown;
  self.tabStop := true;
  self.enabled := true;
  self.selectedItemIndex := kItemNone;
  self.bevelInner := bvNone;
  self.bevelOuter := bvNone;
  self.updateHint;
  end;

procedure PdStatsPanel.updateHint;
  begin
  if domain.options.showLongHintsForButtons then
    self.hint := 'Parts of the plant showing counts and percent of total biomass taken up by'
      + ' each plant part. You can''t change anything here; it is for display only.'
      + ' See the help system for details.'
  else
    self.hint := '';
  self.showHint := true;
  end;

destructor PdStatsPanel.destroy;
  begin
  drawBitmap.free;
  drawBitmap := nil;
  statistics.free;
  statistics := nil;
  inherited destroy;
  end;

function PdStatsPanel.maxSelectedItemIndex: integer;
  begin
  result := kItemNone;
  end;

function PdStatsPanel.collapsedHeight: integer;
  begin
  result := self.textHeight + kTopBottomGap;
  end;

procedure PdStatsPanel.collapseOrExpand(y: integer);
  begin
  { do nothing }
  end;

procedure PdStatsPanel.updatePlant(newPlant: PdPlant);
  begin
  if plant <> newPlant then
  	begin
    plant := newPlant;
    updateCurrentValue(0);
    end;
  end;

procedure PdStatsPanel.updatePlantValues;
  begin
  updateCurrentValue(0);
  repaint; { NOT refresh }
  end;

procedure PdStatsPanel.updateCurrentValue;
  begin
  statistics.zeroAllFields;
  self.enabled := false;
  if plant = nil then exit;
  plant.getPlantStatistics(statistics);
  self.enabled := true;
  self.updateDisplay;
  end;

procedure PdStatsPanel.updateDisplay;
  begin
  if plant = nil then exit;
  self.invalidate;
  end;

const
  kMinGraphWidth = 50;

procedure PdStatsPanel.resizeElements;
  var
    fullRect: TRect;
  begin
  if self.textHeight = 0 then self.calculateTextDimensions;
  if self.maxLabelWidth = 0 then self.paint;
  fullRect := rect(0, 0,
    kMinGraphWidth + maxLabelWidth + kLeftRightGap * 2 + kBetweenGap,
    (self.numNonZeroPlantParts + 2) * self.textHeight + kTopBottomGap * 2 + kBetweenGap * 2);
  self.clientHeight := intMax(0, intMax(rHeight(fullRect), parent.clientHeight));
  self.clientWidth := intMax(0, intMax(rWidth(fullRect), parent.clientWidth));
  try
    drawBitmap.width := self.clientWidth;
    drawBitmap.height := self.clientHeight;
  except
    drawBitmap.width := 1;
    drawBitmap.height := 1;
  end;
  self.updateDisplay;
  end;

function PdStatsPanel.labelStringForPartType(index: smallint): string;
  var
    partType: smallint;
    hasStuff: boolean;
  begin
  result := '';
  with statistics do
    begin
    partType := self.partTypeForIndex(index);
     with statistics do
      hasStuff := (liveBiomass_pctMPB[partType] + deadBiomass_pctMPB[partType] > 0) or (count[partType] > 0);
    if not hasStuff then exit;
    if count[partType] > 0 then
      result := intToStr(count[partType]) + ' ';
    result := result + self.nameForPartType(partType, count[partType] = 1);
    result := result + ': '
        + digitValueString(self.displayPercentForPartType(partType, kBothLiveAndDead)) + '%';
    end;
  end;

function PdStatsPanel.displayPercentForPartType(partType: smallint; livingDeadOrBoth: smallint): single;
  var
    total_pctMPB: single;
  begin
  result := 0.0;
  total_pctMPB :=
      statistics.liveBiomass_pctMPB[kStatisticsPartTypeAllVegetative]
    + statistics.deadBiomass_pctMPB[kStatisticsPartTypeAllVegetative]
    + statistics.liveBiomass_pctMPB[kStatisticsPartTypeAllReproductive]
    + statistics.deadBiomass_pctMPB[kStatisticsPartTypeAllReproductive];
  if total_pctMPB = 0.0 then exit;
  case livingDeadOrBoth of
    kLive: result := statistics.liveBiomass_pctMPB[partType];
    kDead: result := statistics.deadBiomass_pctMPB[partType];
    kBothLiveAndDead: result := statistics.liveBiomass_pctMPB[partType]
        + statistics.deadBiomass_pctMPB[partType];
    end;
  result := min(100.0, max(0.0, 100.0 * result / total_pctMPB));
  end;

function PdStatsPanel.numNonZeroPlantParts: smallint;
  var
    i, partType: smallint;
    hasStuff: boolean;
  begin
  result := 0;
  for i := 0 to kStatisticsPartTypeLast do
    begin
    partType := self.partTypeForIndex(i);
    with statistics do
      hasStuff := (liveBiomass_pctMPB[partType] + deadBiomass_pctMPB[partType] > 0) or (count[partType] > 0);
    if hasStuff then inc(result);
    end;
  end;

procedure PdStatsPanel.paint;
  var
    fullRect, minRect, maxRect: TRect;
    minText, maxText: string[30];
    percentText: string;
    i, partType, topPos: smallint;
    labelTexts: array[0..kStatisticsPartTypeLast] of ansistring;
    hasStuff: boolean;
   begin
  fullRect := getClientRect;
  self.canvas.font := self.font;
  if self.textHeight = 0 then self.calculateTextDimensions;
  if plant <> nil then
    percentText := 'Statistics for ' + plant.getName // v2.0 + ' (% of total)'
  else
    percentText := '(no plants selected)'; // v2.0
  with percentRect do
    begin
    top := fullRect.top + kTopBottomGap;
    bottom := top + self.textHeight;
    left := fullRect.left + kLeftRightGap;
    // v2.0 bold font
    self.canvas.font.style := [fsBold];
    right := left + self.canvas.textWidth(percentText);
    self.canvas.font.style := [];
    end;
  for i := 0 to kStatisticsPartTypeLast do labelTexts[i] := self.labelStringForPartType(i);
  topPos := percentRect.bottom + kBetweenGap;
  maxLabelWidth := 0;
  for i := 0 to kStatisticsPartTypeLast do labelRects[i] := rect(0, 0, 0, 0);
  for i := 0 to kStatisticsPartTypeLast do with labelRects[i] do
      begin
      left := kLeftRightGap;
      right := left + self.canvas.textWidth(labelTexts[i]);
      if right - left > maxLabelWidth then maxLabelWidth := right - left;
      top := topPos;
      if labelTexts[i] = '' then
        bottom := top
      else
        bottom := top + self.textHeight;
      topPos := topPos + (bottom - top);
      if right - left > maxLabelWidth then maxLabelWidth := right - left;
      end;
  { set all label widths equal to largest, so can right-justify them }
  for i := 0 to kStatisticsPartTypeLast do labelRects[i].right := labelRects[i].left + maxLabelWidth;
  with graphRect do
    begin
    left := kLeftRightGap + maxLabelWidth + kBetweenGap;
    right := fullRect.right - kLeftRightGap;
    top := percentRect.bottom + kBetweenGap;
    bottom := fullRect.bottom - kTopBottomGap - self.textHeight - kBetweenGap;
    end;
  minText := '0';
  with minRect do
    begin
    left := graphRect.left;
    right := left + self.canvas.textWidth(minText);
    top := graphRect.bottom;
    bottom := top + self.textHeight;
    end;
  maxText := '100 %';
  maxRect := minRect;
  with maxRect do
    begin
    right := graphRect.right;
    left := right - self.canvas.textWidth(maxText);
    end;
  with drawBitmap.canvas do
    begin
    brush.color := clBtnFace;
    pen.color := clBtnFace; // v1.4
    rectangle(0, 0, drawBitmap.width, drawBitmap.height);
    for i := 0 to kStatisticsPartTypeLast do
      if labelRects[i].bottom <= graphRect.bottom then
        with statistics do
          begin
          partType := self.partTypeForIndex(i);
          hasStuff := (liveBiomass_pctMPB[partType] + deadBiomass_pctMPB[partType] > 0) or (count[partType] > 0);
          self.drawTextLabel(labelTexts[i], labelRects[i], hasStuff, false, false);
          end;
    if plant <> nil then
      self.drawGraph;
    brush.style := bsClear;
    if plant <> nil then
      pen.color := clBtnText
    else
      pen.color := clBtnFace;
    rectangle(graphRect.left, graphRect.top, graphRect.right, graphRect.bottom);
    // v2.0 top label in bold
    self.canvas.font.style := [fsBold];
    self.drawTextLabel(percentText, percentRect, (plant <> nil), false, false);
    self.canvas.font.style := [];
    if plant <> nil then
      begin
      self.drawTextLabel(minText, minRect, true, false, false);
      self.drawTextLabel(maxText, maxRect, true, false, false);
      end;
    end;
  if drawBitmap.width > 0 then
    copyBitmapToCanvasWithGlobalPalette(drawBitmap, self.canvas, rect(0,0,0,0));
  end;

procedure PdStatsPanel.drawTextLabel(text: string; drawRect: TRect; active, drawLine, drawBox: boolean);
  var
    cText: array[0..255] of Char;
  begin
  if text <> '' then with drawBitmap.canvas do
    begin
    font := self.font;
    if active then
      font.color := clBtnText
    else
      font.color := clBtnShadow;
    strPCopy(cText, text);
    { changed DT_LEFT to DT_RIGHT to right-justify labels; ok because nothing else matters here }
    winprocs.drawText(handle, cText, strLen(cText), drawRect, DT_RIGHT);
    end;
  if drawLine then with drawBitmap.canvas do
    begin
    pen.color := clBtnShadow;
    moveTo(drawRect.left, drawRect.bottom - 2);
    lineTo(drawRect.right, drawRect.bottom - 2);
    end;
  if drawBox then with drawBitmap.canvas do
    begin
    pen.color := clBtnShadow;
    moveTo(drawRect.right + 2, drawRect.top);
    lineTo(drawRect.left - 2, drawRect.top);
    lineTo(drawRect.left - 2, drawRect.bottom - 2);
    lineTo(drawRect.right + 2, drawRect.bottom - 2);
    lineTo(drawRect.right + 2, drawRect.top);
    end;
  end;

procedure PdStatsPanel.drawGraph;
  var
    i, partType: longint;
  begin
  with drawBitmap.canvas do
    begin
    brush.style := bsSolid;
    pen.color := clBlack;
    pen.width := 1;
    pen.style := psSolid;
    for i := 0 to kStatisticsPartTypeLast do
      if labelRects[i].bottom <= graphRect.bottom then
        begin
        partType := self.partTypeForIndex(i);
        { first draw all biomass }
        brush.color := clBlack;
        self.drawBar(i, self.displayPercentForPartType(partType, kDead));
        { next draw only live biomass }
        brush.color := clLime;
        self.drawBar(i, displayPercentForPartType(partType, kLive));
        end;
    brush.style := bsClear;
    end;
  end;

procedure PdStatsPanel.drawBar(index: integer; amount_pctMPB: single);
  var
    distance: longint;
    drawRect: TRect;
  begin
  distance := graphRect.left + round(amount_pctMPB / 100.0 * (graphRect.right - graphRect.left));
  drawRect := rect(graphRect.left, labelRects[index].top, distance, labelRects[index].bottom);
  with drawRect do drawBitmap.canvas.rectangle(left, top, right, bottom);
  end;

function PdStatsPanel.nameForPartType(partType: smallint; isSingular: boolean): string;
  begin
  result := '';
  case partType of
    kStatisticsPartTypeSeedlingLeaf:
      if isSingular then result := 'seedling leaf' else result := 'seedling leaves';
    kStatisticsPartTypeLeaf:
      if isSingular then result := 'leaf' else result := 'leaves';
    kStatisticsPartTypeFemaleInflorescence:
      if isSingular then result := 'primary inflorescence' else result := 'primary inflorescences';
    kStatisticsPartTypeMaleInflorescence:
      if isSingular then result := 'secondary inflorescence' else result := 'secondary inflorescences';
    kStatisticsPartTypeFemaleFlower:
      if isSingular then result := 'primary flower' else result := 'primary flowers';
    kStatisticsPartTypeFemaleFlowerBud:
      if isSingular then result := 'primary flower bud' else result := 'primary flower buds';
    kStatisticsPartTypeMaleFlower:
      if isSingular then result := 'secondary flower' else result := 'secondary flowers';
    kStatisticsPartTypeMaleFlowerBud:
      if isSingular then result := 'secondary flower bud' else result := 'secondary flower buds';
    kStatisticsPartTypeAxillaryBud:
      if isSingular then result := 'meristem' else result := 'meristems';
    kStatisticsPartTypeFruit:
      if isSingular then result := 'ripe fruit' else result := 'ripe fruits';
    kStatisticsPartTypeStem:
      if isSingular then result := 'stem internode' else result := 'stem internodes';
    kStatisticsPartTypeUnripeFruit:
      if isSingular then result := 'unripe fruit' else result := 'unripe fruits';
    kStatisticsPartTypeFallenFruit:
      if isSingular then result := 'fallen fruit' else result := 'fallen fruits';
    kStatisticsPartTypeUnallocatedNewVegetativeBiomass: result := 'unallocated vegetative';
    kStatisticsPartTypeUnremovedDeadVegetativeBiomass: result := 'unremoved vegetative';
    kStatisticsPartTypeUnallocatedNewReproductiveBiomass: result := 'unallocated reproductive';
    kStatisticsPartTypeUnremovedDeadReproductiveBiomass: result := 'unremoved reproductive';
    kStatisticsPartTypeFallenFlower:
      if isSingular then result := 'fallen flower' else result := 'fallen flowers';
    kStatisticsPartTypeAllVegetative: result := 'vegetative parts';
    kStatisticsPartTypeAllReproductive: result := 'reproductive parts';
  else
    result := '';
  end;
  end;

function PdStatsPanel.partTypeForIndex(partType: smallint): smallint;
  begin
  result := -1;
  case partType of
    0: result := kStatisticsPartTypeAllVegetative;
    1: result := kStatisticsPartTypeAllReproductive;
    2: result := kStatisticsPartTypeAxillaryBud;
    3: result := kStatisticsPartTypeStem;
    4: result := kStatisticsPartTypeSeedlingLeaf;
    5: result := kStatisticsPartTypeLeaf;
    6: result := kStatisticsPartTypeFemaleInflorescence;
    7: result := kStatisticsPartTypeFemaleFlowerBud;
    8: result := kStatisticsPartTypeFemaleFlower;
    9: result := kStatisticsPartTypeMaleInflorescence;
    10: result := kStatisticsPartTypeMaleFlowerBud;
    11: result := kStatisticsPartTypeMaleFlower;
    12: result := kStatisticsPartTypeFallenFlower;
    13: result := kStatisticsPartTypeUnripeFruit;
    14: result := kStatisticsPartTypeFruit;
    15: result := kStatisticsPartTypeFallenFruit;
    16: result := kStatisticsPartTypeUnallocatedNewVegetativeBiomass;
    17: result := kStatisticsPartTypeUnremovedDeadVegetativeBiomass;
    18: result := kStatisticsPartTypeUnallocatedNewReproductiveBiomass;
    19: result := kStatisticsPartTypeUnremovedDeadReproductiveBiomass;
  else
    { called by paint method, so do not raise exception }
    result := 0;
  end;
  end;

end.
