unit uwizard;

interface

uses
  Windows, Messages, SysUtils, Classes, Graphics, Controls, Forms, Dialogs,
  Buttons, StdCtrls, ExtCtrls, uplant, FileCtrl, Gauges, Grids,
  updform, ucollect, utdo, ComCtrls, ubitmap;

const
  { group indexes }
  kMeristem_AlternateOrOpposite = 1;
  kMeristem_BranchIndex = 2;
  kMeristem_SecondaryBranching = 3;
  kMeristem_BranchAngle = 4;
  kInternode_Curviness = 5;
  kInternode_Length = 6;
  kLeaves_Scale = 7;
  kLeaves_PetioleLength = 8;
  kLeaves_Angle = 9;
  kLeaflets_Number = 10;
  kLeaflets_Shape = 11;
  kLeaflets_Spread = 12;
  kFlowers_NumPetals = 13;
  kFlowers_Scale = 14;
  kInflorDraw_NumFlowers = 15;
  kInflorDraw_Shape = 16;
  kInflorPlace_NumApical = 17;
  kInflorPlace_NumAxillary = 18;
  kInflorPlace_ApicalStalkLength = 19;
  kInflorPlace_AxillaryStalkLength = 20;
  kFruit_NumSections = 21;
  kFruit_Scale = 22;
  kInternode_Thickness = 23;
  kInflorDraw_Thickness = 24;

type
  TWizardForm = class(PdForm)
    wizardNotebook: TNotebook;
    cancel: TButton;
    back: TButton;
    next: TButton;
    panelMeristemsLabel: TLabel;
    panelInternodesLabel: TLabel;
    panelLeavesLabel: TLabel;
    panelInflorDrawingLabel: TLabel;
    branchingLabel: TLabel;
    leavesAlternateOppositeLabel: TLabel;
    branchAngleLabel: TLabel;
    secondaryBranchingLabel: TLabel;
    curvinessLabel: TLabel;
    internodeLengthLabel: TLabel;
    leafTdosLabel: TLabel;
    leafScaleLabel: TLabel;
    leafAngleLabel: TLabel;
    petioleLengthLabel: TLabel;
    finishLabelFirst: TLabel;
    newPlantName: TEdit;
    finishLabelSecond: TLabel;
    finishLabelThird: TLabel;
    panelFinishLabel: TLabel;
    panelStartLabel: TLabel;
    introLabelThird: TLabel;
    panelFlowersLabel: TLabel;
    petalTdosLabel: TLabel;
    petalScaleLabel: TLabel;
    petalsNumberLabel: TLabel;
    fruitTdoLabel: TLabel;
    fruitSectionsNumberLabel: TLabel;
    fruitScaleLabel: TLabel;
    panelFruitsLabel: TLabel;
    inflorFlowersLabel: TLabel;
    inflorShapeLabel: TLabel;
    panelInflorPlacementLabel: TLabel;
    apicalInflorsNumberLabel: TLabel;
    axillaryInflorsNumberLabel: TLabel;
    apicalStalkLabel: TLabel;
    axillaryStalkLabel: TLabel;
    introLabelFirst: TLabel;
    apicalInflorExtraImage: TImage;
    axillaryInflorExtraImage: TImage;
    previewPanel: TPanel;
    internodesVeryShort: TSpeedButton;
    internodesShort: TSpeedButton;
    internodesMedium: TSpeedButton;
    internodesLong: TSpeedButton;
    internodesVeryLong: TSpeedButton;
    curvinessNone: TSpeedButton;
    curvinessLittle: TSpeedButton;
    curvinessSome: TSpeedButton;
    curvinessVery: TSpeedButton;
    leavesAlternate: TSpeedButton;
    leavesOpposite: TSpeedButton;
    branchNone: TSpeedButton;
    branchLittle: TSpeedButton;
    branchMedium: TSpeedButton;
    branchLot: TSpeedButton;
    secondaryBranchingYes: TSpeedButton;
    secondaryBranchingNo: TSpeedButton;
    branchAngleSmall: TSpeedButton;
    branchAngleMedium: TSpeedButton;
    branchAngleLarge: TSpeedButton;
    arrowLeavesAlternateOpposite: TImage;
    arrowBranching: TImage;
    arrowSecondaryBranching: TImage;
    arrowBranchAngle: TImage;
    arrowCurviness: TImage;
    arrowInternodeLength: TImage;
    arrowLeafScale: TImage;
    leafScaleTiny: TSpeedButton;
    leafScaleSmall: TSpeedButton;
    leafScaleMedium: TSpeedButton;
    leafScaleLarge: TSpeedButton;
    leafScaleHuge: TSpeedButton;
    arrowLeafAngle: TImage;
    leafAngleSmall: TSpeedButton;
    leafAngleMedium: TSpeedButton;
    leafAngleLarge: TSpeedButton;
    arrowPetioleLength: TImage;
    petioleVeryShort: TSpeedButton;
    petioleShort: TSpeedButton;
    petioleMedium: TSpeedButton;
    petioleLong: TSpeedButton;
    petioleVeryLong: TSpeedButton;
    arrowLeafTdos: TImage;
    petalsOne: TSpeedButton;
    petalsThree: TSpeedButton;
    petalsFour: TSpeedButton;
    petalsFive: TSpeedButton;
    petalsTen: TSpeedButton;
    petalScaleTiny: TSpeedButton;
    petalScaleSmall: TSpeedButton;
    petalScaleMedium: TSpeedButton;
    petalScaleLarge: TSpeedButton;
    petalScaleHuge: TSpeedButton;
    arrowPetalTdos: TImage;
    arrowPetalsNumber: TImage;
    arrowPetalScale: TImage;
    arrowInflorFlowers: TImage;
    arrowInflorShape: TImage;
    inflorFlowersOne: TSpeedButton;
    inflorFlowersTwo: TSpeedButton;
    inflorFlowersThree: TSpeedButton;
    inflorFlowersFive: TSpeedButton;
    inflorFlowersTen: TSpeedButton;
    inflorFlowersTwenty: TSpeedButton;
    inflorShapeSpike: TSpeedButton;
    inflorShapeRaceme: TSpeedButton;
    inflorShapePanicle: TSpeedButton;
    inflorShapeUmbel: TSpeedButton;
    inflorShapeHead: TSpeedButton;
    apicalInflorsNone: TSpeedButton;
    apicalInflorsOne: TSpeedButton;
    apicalInflorsTwo: TSpeedButton;
    apicalInflorsThree: TSpeedButton;
    apicalInflorsFive: TSpeedButton;
    arrowApicalInflorsNumber: TImage;
    axillaryInflorsNone: TSpeedButton;
    axillaryInflorsThree: TSpeedButton;
    axillaryInflorsFive: TSpeedButton;
    axillaryInflorsTen: TSpeedButton;
    axillaryInflorsTwenty: TSpeedButton;
    arrowAxillaryInflorsNumber: TImage;
    apicalStalkVeryShort: TSpeedButton;
    apicalStalkShort: TSpeedButton;
    apicalStalkMedium: TSpeedButton;
    apicalStalkLong: TSpeedButton;
    apicalStalkVeryLong: TSpeedButton;
    arrowApicalStalk: TImage;
    arrowAxillaryStalk: TImage;
    axillaryStalkVeryShort: TSpeedButton;
    axillaryStalkShort: TSpeedButton;
    axillaryStalkMedium: TSpeedButton;
    axillaryStalkLong: TSpeedButton;
    axillaryStalkVeryLong: TSpeedButton;
    arrowFruitTdo: TImage;
    arrowFruitSectionsNumber: TImage;
    arrowFruitScale: TImage;
    fruitSectionsOne: TSpeedButton;
    fruitSectionsThree: TSpeedButton;
    fruitSectionsFour: TSpeedButton;
    fruitSectionsFive: TSpeedButton;
    fruitSectionsTen: TSpeedButton;
    fruitScaleTiny: TSpeedButton;
    fruitScaleSmall: TSpeedButton;
    fruitScaleMedium: TSpeedButton;
    fruitScaleLarge: TSpeedButton;
    fruitScaleHuge: TSpeedButton;
    introLabelSecond: TLabel;
    panelCompoundLeavesLabel: TLabel;
    arrowLeaflets: TImage;
    leafletsLabel: TLabel;
    leafletsShapeLabel: TLabel;
    arrowLeafletsShape: TImage;
    leafletsOne: TSpeedButton;
    leafletsThree: TSpeedButton;
    leafletsFour: TSpeedButton;
    leafletsFive: TSpeedButton;
    leafletsSeven: TSpeedButton;
    leafletsPinnate: TSpeedButton;
    leafletsPalmate: TSpeedButton;
    arrowLeafletsSpacing: TImage;
    leafletSpacingLabel: TLabel;
    leafletSpacingClose: TSpeedButton;
    leafletSpacingMedium: TSpeedButton;
    leafletSpacingFar: TSpeedButton;
    leafTdosDraw: TDrawGrid;
    petalTdosDraw: TDrawGrid;
    sectionTdosDraw: TDrawGrid;
    defaultChoices: TButton;
    arrowInternodeWidth: TImage;
    internodeWidthLabel: TLabel;
    internodeWidthVeryThin: TSpeedButton;
    internodeWidthThin: TSpeedButton;
    internodeWidthMedium: TSpeedButton;
    internodeWidthThick: TSpeedButton;
    internodeWidthVeryThick: TSpeedButton;
    inflorShapeCluster: TSpeedButton;
    arrowInflorThickness: TImage;
    inflorThicknessLabel: TLabel;
    inflorWidthVeryThin: TSpeedButton;
    inflorWidthThin: TSpeedButton;
    inflorWidthMedium: TSpeedButton;
    inflorWidthThick: TSpeedButton;
    inflorWidthVeryThick: TSpeedButton;
    arrowPetalColor: TImage;
    petalColorLabel: TLabel;
    petalColor: TPanel;
    fruitColorLabel: TLabel;
    fruitColor: TPanel;
    arrowFruitColor: TImage;
    hiddenPicturesPanel: TPanel;
    startPageImage: TImage;
    meristemsPageImage: TImage;
    internodesPageImage: TImage;
    leavesPageImage: TImage;
    compoundLeavesPageImage: TImage;
    flowersPageImage: TImage;
    inflorDrawPageImage: TImage;
    inflorPlacePageImage: TImage;
    fruitsPageImage: TImage;
    finishPageImage: TImage;
    fruitColorExplainLabel: TLabel;
    flowerColorExplainLabel: TLabel;
    arrowShowFruits: TImage;
    showFruitsLabel: TLabel;
    showFruitsYes: TRadioButton;
    showFruitsNo: TRadioButton;
    previewLabel: TLabel;
    randomizePlant: TButton;
    inflorDrawPageImageDisabled: TImage;
    flowersPageImageDisabled: TImage;
    fruitsPageImageDisabled: TImage;
    turnLeft: TSpeedButton;
    turnRight: TSpeedButton;
    bottomBevel: TBevel;
    longHintsSuggestionLabel: TLabel;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    Label6: TLabel;
    Label7: TLabel;
    Label8: TLabel;
    Label9: TLabel;
    Label10: TLabel;
    progressDrawGrid: TDrawGrid;
    Label11: TLabel;
    Label12: TLabel;
    helpButton: TSpeedButton;
    changeTdoLibrary: TSpeedButton;
    sectionTdoSelectedLabel: TLabel;
    petalTdoSelectedLabel: TLabel;
    leafTdoSelectedLabel: TLabel;
    startPicture: TImage;
    procedure cancelClick(Sender: TObject);
    procedure backClick(Sender: TObject);
    procedure nextClick(Sender: TObject);
    procedure wizardNotebookPageChanged(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure progressDrawGridDrawCell(Sender: TObject; Col, Row: Longint;
      Rect: TRect; State: TGridDrawState);
    procedure progressDrawGridSelectCell(Sender: TObject; Col,
      Row: Longint; var CanSelect: Boolean);
    procedure defaultChoicesClick(Sender: TObject);
    procedure leafTdosDrawDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure petalTdosDrawDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure changeTdoLibraryClick(Sender: TObject);
    procedure sectionTdosDrawDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure petalColorMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure fruitColorMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure branchNoneClick(Sender: TObject);
    procedure branchLittleClick(Sender: TObject);
    procedure branchMediumClick(Sender: TObject);
    procedure branchLotClick(Sender: TObject);
    procedure leafletsOneClick(Sender: TObject);
    procedure leafletsThreeClick(Sender: TObject);
    procedure leafletsFourClick(Sender: TObject);
    procedure leafletsFiveClick(Sender: TObject);
    procedure leafletsSevenClick(Sender: TObject);
    procedure apicalInflorsNoneClick(Sender: TObject);
    procedure apicalInflorsOneClick(Sender: TObject);
    procedure apicalInflorsTwoClick(Sender: TObject);
    procedure apicalInflorsThreeClick(Sender: TObject);
    procedure apicalInflorsFiveClick(Sender: TObject);
    procedure axillaryInflorsNoneClick(Sender: TObject);
    procedure axillaryInflorsThreeClick(Sender: TObject);
    procedure axillaryInflorsFiveClick(Sender: TObject);
    procedure axillaryInflorsTenClick(Sender: TObject);
    procedure axillaryInflorsTwentyClick(Sender: TObject);
    procedure showFruitsYesClick(Sender: TObject);
    procedure showFruitsNoClick(Sender: TObject);
    procedure inflorFlowersOneClick(Sender: TObject);
    procedure inflorFlowersTwoClick(Sender: TObject);
    procedure inflorFlowersThreeClick(Sender: TObject);
    procedure inflorFlowersFiveClick(Sender: TObject);
    procedure inflorFlowersTenClick(Sender: TObject);
    procedure inflorFlowersTwentyClick(Sender: TObject);
    procedure randomizePlantClick(Sender: TObject);
    procedure leafTdosDrawSelectCell(Sender: TObject; Col, Row: Integer;
      var CanSelect: Boolean);
    procedure petalTdosDrawSelectCell(Sender: TObject; Col, Row: Integer;
      var CanSelect: Boolean);
    procedure sectionTdosDrawSelectCell(Sender: TObject; Col, Row: Integer;
      var CanSelect: Boolean);
    procedure turnLeftClick(Sender: TObject);
    procedure turnRightClick(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure helpButtonClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure sectionTdosDrawMouseMove(Sender: TObject; Shift: TShiftState;
      X, Y: Integer);
  private
    { Private declarations }
  public
    { Public declarations }
    plant: PdPlant;
    tdos: TListCollection;
    plantHasInflorescences: boolean;
    tdoSelectionChanged: boolean;
    askedToSaveOptions: boolean;
    previewPaintBox: PdPaintBoxWithPalette;
    constructor create(AOwner: TComponent); override;
    destructor destroy; override;
    procedure loadNewTdoLibrary;
    procedure readTdosFromFile;
    function tdoForIndex(index: smallint): KfObject3D;
    procedure updateProgress;
    procedure setPlantVariables;
    procedure finishForMeristems;
    procedure finishForInternodes;
    procedure finishForLeaves;
    procedure finishForCompoundLeaves;
    procedure finishForFlowers;
    procedure finishForInflorescences;
    procedure finishForInflorescencePlacement;
    procedure finishForFruit;
    procedure setDownButtonForGroupIndexFromName(aGroupIndex: smallint; aName: string);
    function downButtonNameForGroupIndex(aGroupIndex: smallint): string;
    procedure drawCellInTdoDrawGrid(grid: TDrawGrid; column: smallint; selected: boolean; rect: TRect);
    function hintForTdosDrawGridAtPoint(aComponent: TComponent; aPoint: TPoint; var cursorRect: TRect): string;
    function selectFirstTdoInDrawGridWithStringInName(grid: TDrawGrid; aString: string): boolean;
    function bitmapForProgressPage(page: smallint): TBitmap;
    procedure updateForButtonInteractions;
    procedure drawPreview(reloadVariables: boolean);
    procedure saveOptionsToDomain;
    function optionsHaveChanged: boolean;
    procedure setPageIndex(newIndex: smallint);
    procedure showTdoNameInLabel(index: smallint; aLabel: TLabel);
    procedure previewPaintBoxPaint(Sender: TObject);
  end;

implementation

{$R *.DFM}

uses udomain, uturtle, usupport, utravers, updcom, ucursor, umain, ubmpsupport;

const
  { panels }
  kStart = 0;
  kMeristems = 1;
  kInternodes = 2;
  kLeaves = 3;
  kCompoundLeaves = 4;
  kInflorescencesPlacement = 5;
  kInflorescences = 6;
  kFlowers = 7;
  kFruit = 8;
  kFinish = 9;
  kLastPanel = 9;
  kReloadVariables = true; kDontReloadVariables = false;

{ -------------------------------------------------------------------------------------------- creation/destruction }
constructor TWizardForm.create(AOwner: TComponent);
  var
    i: smallint;
  begin
  inherited create(AOwner);
  leafTdoSelectedLabel.caption := '';
  petalTdoSelectedLabel.caption := '';
  sectionTdoSelectedLabel.caption := '';
  previewPaintBox := PdPaintBoxWithPalette.create(self);
  with previewPaintBox do
    begin
    parent := previewPanel;
    align := alClient;
    onPaint := self.previewPaintBoxPaint;
    end;
  { initialize default plant }
  plant := PdPlant.create;
  plant.defaultAllParameters;
  plant.setName('New plant ' + intToStr(numPlantsCreatedThisSession + 1));
  inc(numPlantsCreatedThisSession);
  newPlantName.text := plant.getName;
  { initialize tdos }
  tdos := TListCollection.create;
  self.readTdosFromFile;
  { load info from domain on choices }
  if domain <> nil then
    for i := 1 to kMaxWizardQuestions do
      self.setDownButtonForGroupIndexFromName(i, domain.options.wizardChoices[i]);
  { handle radio button choice separately }
  if domain.options.wizardShowFruit then
    showFruitsYes.checked := true
  else
    showFruitsNo.checked := true;
  { colors are handled separately }
  petalcolor.color := domain.options.wizardColors[1];
  fruitcolor.color := domain.options.wizardColors[2];
  { tdo choices are handled separately - if not found use defaults by type }
  if not self.selectFirstTdoInDrawGridWithStringInName(leafTdosDraw, domain.options.wizardTdoNames[1]) then
    self.selectFirstTdoInDrawGridWithStringInName(leafTdosDraw, 'leaf');
  if not self.selectFirstTdoInDrawGridWithStringInName(petalTdosDraw, domain.options.wizardTdoNames[2]) then
    self.selectFirstTdoInDrawGridWithStringInName(petalTdosDraw, 'petal');
  if not self.selectFirstTdoInDrawGridWithStringInName(sectionTdosDraw, domain.options.wizardTdoNames[3]) then
    self.selectFirstTdoInDrawGridWithStringInName(sectionTdosDraw, 'section');
  self.updateForButtonInteractions;
  end;

const kPreviewSize = 110;

procedure TWizardForm.FormCreate(Sender: TObject);
  begin
  startPicture.picture.bitmap.palette := CopyPalette(MainForm.paletteImage.picture.bitmap.palette);
  wizardNotebook.invalidate;
  with progressDrawGrid do
    begin
    // assumes there is no border
    defaultColWidth := width div colCount;
    width := defaultColWidth * colCount;
    defaultRowHeight := height;
    end;
  self.setPageIndex(0);
  self.updateProgress;
  end;

destructor TWizardForm.destroy;
  begin
  plant.free;
  plant := nil;
  tdos.free;
  tdos := nil;
  inherited destroy;
  end;

{ -------------------------------------------------------------------------------------------- *tdos }
function TWizardForm.hintForTdosDrawGridAtPoint(aComponent: TComponent; aPoint: TPoint; var cursorRect: TRect): string;
  var
    grid: TDrawGrid;
    col, row: integer;
    tdo: KfObject3D;
  begin
  result := '';
  if (aComponent = nil) or (not (aComponent is TDrawGrid)) then exit;
  grid := aComponent as TDrawGrid;
  grid.mouseToCell(aPoint.x, aPoint.y, col, row);
  if grid = progressDrawGrid then
    begin
    case col of
      kStart: result := 'start';
      kMeristems: result := 'meristems';
      kInternodes: result := 'internodes';
      kLeaves: result := 'leaves';
      kCompoundLeaves: result := 'compound leaves';
      kFlowers: result := 'flowers';
      kInflorescences: result := 'inflorescence drawing';
      kInflorescencesPlacement: result := 'inflorescence placement';
      kFruit: result := 'fruit';
      kFinish: result := 'finish';
      end;
    end
  else
    begin
    tdo := self.tdoForIndex(col);
    if tdo = nil then exit;
    result := tdo.getName;
    end;
  { change hint if cursor moves out of the current item's rectangle }
  cursorRect := grid.cellRect(col, row);
  end;

procedure TWizardForm.changeTdoLibraryClick(Sender: TObject);
  begin
  self.loadNewTdoLibrary;
  leafTdosDraw.invalidate;
  petalTdosDraw.invalidate;
  sectionTdosDraw.invalidate;
  end;

procedure TWizardForm.loadNewTdoLibrary;
   var
    fileNameWithPath: string;
  begin
  fileNameWithPath := getFileOpenInfo(kFileTypeTdo, domain.defaultTdoLibraryFileName,
      'Choose a 3D object library (tdo) file');
  if fileNameWithPath = '' then exit;
  domain.defaultTdoLibraryFileName := fileNameWithPath;
  self.readTdosFromFile;
  end;

procedure TWizardForm.readTdosFromFile;
  var
    newTdo: KfObject3D;
    inputFile: TextFile;
  begin
  tdos.clear;
  if domain = nil then exit;
  if not domain.checkForExistingDefaultTdoLibrary then
    begin
    messageDlg('Because you didn''t choose a 3D object library, you will only' + chr(13)
      + 'be able to use a default 3D object on your new plant.' + chr(13) + chr(13)
      + 'You can also choose a 3D object library' + chr(13)
      + 'by clicking the 3D Objects button in the wizard.',
      mtWarning, [mbOk], 0);
    exit;
    end;
  assignFile(inputFile, domain.defaultTdoLibraryFileName);
  try
    setDecimalSeparator; // v1.5
    reset(inputFile);
    while not eof(inputFile) do
      begin
      newTdo := KfObject3D.create;
      newTdo.readFromFileStream(inputFile, kInTdoLibrary);
      tdos.add(newTdo);
      end;
  finally
    closeFile(inputFile);
    leafTdosDraw.colCount := tdos.count;
    petalTdosDraw.colCount := tdos.count;
    sectionTdosDraw.colCount := tdos.count;
  end;
  end;

function TWizardForm.tdoForIndex(index: smallint): KfObject3D;
  begin
  result := nil;
  if (index >= 0) and (index <= tdos.count - 1) then
    result := KfObject3D(tdos.items[index]);
  end;

procedure TWizardForm.leafTdosDrawDrawCell(Sender: TObject; Col,
  Row: Integer; Rect: TRect; State: TGridDrawState);
  begin
  self.drawCellInTdoDrawGrid(leafTdosDraw, col, gdSelected in state, rect);
  end;

procedure TWizardForm.petalTdosDrawDrawCell(Sender: TObject; Col,
  Row: Integer; Rect: TRect; State: TGridDrawState);
  begin
  self.drawCellInTdoDrawGrid(petalTdosDraw, col, gdSelected in state, rect);
  end;

procedure TWizardForm.sectionTdosDrawDrawCell(Sender: TObject; Col,
  Row: Integer; Rect: TRect; State: TGridDrawState);
  begin
  self.drawCellInTdoDrawGrid(sectionTdosDraw, col, gdSelected in state, rect);
  end;

procedure TWizardForm.drawCellInTdoDrawGrid(grid: TDrawGrid; column: smallint; selected: boolean; rect: TRect);
  var
    tdo: KfObject3d;
    turtle: KfTurtle;
    bestPoint: TPoint;
  begin
  if not selected then
    begin
    grid.canvas.brush.color := clWhite;
    grid.canvas.font.color := clBtnText;
    end
  else
    begin
    grid.canvas.brush.color := clHighlight;
    grid.canvas.font.color := clHighlightText;
    end;
  grid.canvas.fillRect(rect);
  tdo := nil;
  tdo := self.tdoForIndex(column);
  if tdo = nil then exit;
  { draw tdo }
  turtle := KfTurtle.defaultStartUsing;
  try
    turtle.drawingSurface.pane := grid.canvas;
    turtle.setDrawOptionsForDrawingTdoOnly;
    turtle.reset; { must be after pane and draw options set }
    bestPoint := tdo.bestPointForDrawingAtScale(turtle, Point(rect.left, rect.top), Point(rWidth(rect), rHeight(rect)), 0.2);
    turtle.xyz(bestPoint.x, bestPoint.y, 0);
    //turtle.xyz(rect.left + (rect.right - rect.left) div 2, rect.bottom - 5, 0);
    turtle.drawingSurface.recordingStart;
    tdo.draw(turtle, 0.2, '', '', 0, 0);//15);
    turtle.drawingSurface.recordingStop;
    turtle.drawingSurface.recordingDraw;
    turtle.drawingSurface.clearTriangles;
  finally
    KfTurtle.defaultStopUsing;
  end;
  end;

{ ---------------------------------------------------------------------------------------- interactions }
procedure TWizardForm.updateForButtonInteractions;
  var
    hadInflors: boolean;
  begin
  { do all of these at once, because then you can do them after loading options at startup
    (it doesn't take very long) }
  { meristems }
  arrowSecondaryBranching.visible := not branchNone.down;
  secondaryBranchingLabel.enabled := not branchNone.down;
  secondaryBranchingYes.enabled := not branchNone.down;
  secondaryBranchingNo.enabled := not branchNone.down;
  arrowBranchAngle.visible := not branchNone.down;
  branchAngleLabel.enabled := not branchNone.down;
  branchAngleSmall.enabled := not branchNone.down;
  branchAngleMedium.enabled := not branchNone.down;
  branchAngleLarge.enabled := not branchNone.down;
  { internodes }
  { leaves }
  { compound leaves }
  arrowLeafletsShape.visible := not leafletsOne.down;
  leafletsShapeLabel.enabled := not leafletsOne.down;
  leafletsPinnate.enabled := not leafletsOne.down;
  leafletsPalmate.enabled := not leafletsOne.down;
  arrowLeafletsSpacing.visible := not leafletsOne.down;
  leafletSpacingLabel.enabled := not leafletsOne.down;
  leafletSpacingClose.enabled := not leafletsOne.down;
  leafletSpacingMedium.enabled := not leafletsOne.down;
  leafletSpacingFar.enabled := not leafletsOne.down;
  { inflor placement }
  hadInflors := self.plantHasInflorescences;
  self.plantHasInflorescences := (not apicalInflorsNone.down) or (not axillaryInflorsNone.down);
  if hadInflors <> self.plantHasInflorescences then
    begin
    progressDrawGrid.invalidate;
    end;
  arrowApicalStalk.visible := not apicalInflorsNone.down;
  apicalStalkLabel.enabled := not apicalInflorsNone.down;
  apicalStalkVeryShort.enabled := not apicalInflorsNone.down;
  apicalStalkShort.enabled := not apicalInflorsNone.down;
  apicalStalkMedium.enabled := not apicalInflorsNone.down;
  apicalStalkLong.enabled := not apicalInflorsNone.down;
  apicalStalkVeryLong.enabled := not apicalInflorsNone.down;
  arrowAxillaryStalk.visible := not axillaryInflorsNone.down;
  axillaryStalkLabel.enabled := not axillaryInflorsNone.down;
  axillaryStalkVeryShort.enabled := not axillaryInflorsNone.down;
  axillaryStalkShort.enabled := not axillaryInflorsNone.down;
  axillaryStalkMedium.enabled := not axillaryInflorsNone.down;
  axillaryStalkLong.enabled := not axillaryInflorsNone.down;
  axillaryStalkVeryLong.enabled := not axillaryInflorsNone.down;
  { inflor drawing }
  arrowInflorShape.visible := not inflorFlowersOne.down;
  inflorShapeLabel.enabled := not inflorFlowersOne.down;
  inflorShapeSpike.enabled := not inflorFlowersOne.down;
  inflorShapeRaceme.enabled := not inflorFlowersOne.down;
  inflorShapePanicle.enabled := not inflorFlowersOne.down;
  inflorShapeUmbel.enabled := not inflorFlowersOne.down;
  inflorShapeCluster.enabled := not inflorFlowersOne.down;
  inflorShapeHead.enabled := not inflorFlowersOne.down;
  { flowers }
  { fruit }
  arrowFruitTdo.visible := not showFruitsNo.checked;
  fruitTdoLabel.enabled := not showFruitsNo.checked;
  sectionTdosDraw.visible := not showFruitsNo.checked;
  sectionTdoSelectedLabel.visible := not showFruitsNo.checked;
  arrowFruitSectionsNumber.visible := not showFruitsNo.checked;
  fruitSectionsNumberLabel.enabled := not showFruitsNo.checked;
  fruitSectionsOne.enabled := not showFruitsNo.checked;
  fruitSectionsThree.enabled := not showFruitsNo.checked;
  fruitSectionsFour.enabled := not showFruitsNo.checked;
  fruitSectionsFive.enabled := not showFruitsNo.checked;
  fruitSectionsTen.enabled := not showFruitsNo.checked;
  arrowFruitScale.visible := not showFruitsNo.checked;
  fruitScaleLabel.enabled := not showFruitsNo.checked;
  fruitScaleTiny.enabled := not showFruitsNo.checked;
  fruitScaleSmall.enabled := not showFruitsNo.checked;
  fruitScaleMedium.enabled := not showFruitsNo.checked;
  fruitScaleLarge.enabled := not showFruitsNo.checked;
  fruitScaleHuge.enabled := not showFruitsNo.checked;
  arrowFruitColor.visible := not showFruitsNo.checked;
  fruitColorLabel.enabled := not showFruitsNo.checked;
  fruitColor.visible := not showFruitsNo.checked;
  fruitColorExplainLabel.enabled := not showFruitsNo.checked;
  end;

procedure TWizardForm.branchNoneClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.branchLittleClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.branchMediumClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.branchLotClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.leafletsOneClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.leafletsThreeClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.leafletsFourClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.leafletsFiveClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.leafletsSevenClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.inflorFlowersOneClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.inflorFlowersTwoClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.inflorFlowersThreeClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.inflorFlowersFiveClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.inflorFlowersTenClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.inflorFlowersTwentyClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.apicalInflorsNoneClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.apicalInflorsOneClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.apicalInflorsTwoClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.apicalInflorsThreeClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.apicalInflorsFiveClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.axillaryInflorsNoneClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.axillaryInflorsThreeClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.axillaryInflorsFiveClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.axillaryInflorsTenClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.axillaryInflorsTwentyClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.showFruitsYesClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

procedure TWizardForm.showFruitsNoClick(Sender: TObject);
  begin
  self.updateForButtonInteractions;
  end;

{ -------------------------------------------------------------------------------------------- transfer }
procedure TWizardForm.defaultChoicesClick(Sender: TObject);
  begin
  if MessageDlg(
      'Are you sure you want to set all the wizard choices to defaults?'
      + chr(13) + chr(13) + 'This action is not undoable.',
      mtConfirmation, [mbYes, mbNo], 0) = IDNO then exit;
  self.setDownButtonForGroupIndexFromName(kMeristem_AlternateOrOpposite, 'leavesAlternate');
  self.setDownButtonForGroupIndexFromName(kMeristem_BranchIndex, 'branchNone');
  self.setDownButtonForGroupIndexFromName(kInternode_Curviness, 'curvinessLittle');
  self.setDownButtonForGroupIndexFromName(kInternode_Length, 'internodesMedium');
  self.setDownButtonForGroupIndexFromName(kInternode_Thickness, 'internodeWidthThin');
  self.setDownButtonForGroupIndexFromName(kLeaves_Scale, 'leafScaleMedium');
  self.setDownButtonForGroupIndexFromName(kLeaves_PetioleLength, 'petioleMedium');
  self.setDownButtonForGroupIndexFromName(kLeaves_Angle, 'leafAngleMedium');
  self.setDownButtonForGroupIndexFromName(kLeaflets_Number, 'leafletsOne');
  self.setDownButtonForGroupIndexFromName(kInflorPlace_NumApical, 'apicalInflorsNone');
  self.setDownButtonForGroupIndexFromName(kInflorPlace_NumAxillary, 'axillaryInflorsNone');
  self.updateForButtonInteractions;
  if wizardNotebook.pageIndex = kLastPanel then
    self.drawPreview(kReloadVariables);
  end;

function TWizardForm.selectFirstTdoInDrawGridWithStringInName(grid: TDrawGrid; aString: string): boolean;
  var
    indexToSelect, i: smallint;
    tdo: KfObject3D;
    gridRect: TGridRect;
  begin
  { returns true if a tdo was selected }
  result := false;
  indexToSelect := -1;
  if tdos.count > 0 then for i := 0 to tdos.count - 1 do
    begin
    tdo := KfObject3D(tdos.items[i]);
    if tdo = nil then exit;
    if pos(upperCase(aString), upperCase(tdo.getName)) > 0 then
        begin
        indexToSelect := i;
        result := true;
        break;
        end;
    end;
  if indexToSelect >= 0 then
    begin
    gridRect.left := indexToSelect;
    gridRect.right := indexToSelect;
    gridRect.top := 0;
    gridRect.bottom := 0;
    grid.selection := gridRect;
    grid.leftCol := indexToSelect;
    if grid = leafTdosDraw then
      self.showTdoNameInLabel(indexToSelect, leafTdoSelectedLabel)
    else if grid = petalTdosDraw then
      self.showTdoNameInLabel(indexToSelect, petalTdoSelectedLabel)
    else if grid = sectionTdosDraw then
      self.showTdoNameInLabel(indexToSelect, sectionTdoSelectedLabel);
    end;
  end;

procedure TWizardForm.setPlantVariables;
  begin
  if plant = nil then exit;
  plant.defaultAllParameters;
  { set variables in plant based on options }
  self.finishForMeristems;
  self.finishForInternodes;
  self.finishForLeaves;
  self.finishForCompoundLeaves;
  self.finishForInflorescencePlacement;
  self.finishForInflorescences;
  self.finishForFlowers;
  self.finishForFruit;
  plant.setName(newPlantName.text);
  plant.setAge(plant.pGeneral.ageAtMaturity);
  end;

procedure TWizardForm.saveOptionsToDomain;
  var
    i: smallint;
  begin
  for i := 1 to kMaxWizardQuestions do
    domain.options.wizardChoices[i] := self.downButtonNameForGroupIndex(i);
  { handle radio button choice separately }
  domain.options.wizardShowFruit := showFruitsYes.checked;
  domain.options.wizardColors[1] := petalcolor.color;
  domain.options.wizardColors[2] := fruitcolor.color;
  with plant.pLeaf.leafTdoParams do
    if object3D <> nil then
      domain.options.wizardTdoNames[1] := object3D.getName;
  // cfk do first petal only in wizard, right?
  with plant.pFlower[kGenderFemale].tdoParams[kFirstPetals] do
    if object3D <> nil then
      domain.options.wizardTdoNames[2] := object3D.getName;
  with plant.pFruit.tdoParams do
    if object3D <> nil then
      domain.options.wizardTdoNames[3] := object3D.getName;
  end;

function TWizardForm.optionsHaveChanged: boolean;
  var
    i: smallint;
    downButtonName: string;
  begin
  result := false;
  for i := 1 to kMaxWizardQuestions do
    begin
    downButtonName := self.downButtonNameForGroupIndex(i);
    if domain.options.wizardChoices[i] <> '' then
      result := result or (domain.options.wizardChoices[i] <> downButtonName);
    end;
  result := result or (domain.options.wizardShowFruit <> showFruitsYes.checked);
  result := result or (domain.options.wizardColors[1] <> petalcolor.color);
  result := result or (domain.options.wizardColors[2] <> fruitcolor.color);
  result := result or tdoSelectionChanged;
  end;

procedure TWizardForm.setDownButtonForGroupIndexFromName(aGroupIndex: smallint; aName: string);
  var
    i: smallint;
    button: TSpeedButton;
  begin
  if aName = '' then exit;
  if self.componentCount > 0 then
    for i := 0 to self.componentCount - 1 do
      begin
      if not (self.components[i] is TSpeedButton) then continue;
      button := self.components[i] as TSpeedButton;
      if button.groupIndex = aGroupIndex then
        begin
        if button.name = aName then
          begin
          { only one can be down, so can exit when one is down }
          button.down := true;
          exit;
          end;
        end;
      end;
  end;

function TWizardForm.downButtonNameForGroupIndex(aGroupIndex: smallint): string;
  var
    i: smallint;
    button: TSpeedButton;
  begin
  result := '';
  if self.componentCount > 0 then
    for i := 0 to self.componentCount - 1 do
      begin
      if not (self.components[i] is TSpeedButton) then continue;
      button := self.components[i] as TSpeedButton;
      if (button.groupIndex = aGroupIndex) and (button.enabled) then  // if not enabled, don't want to match
        begin
        if button.down then
          begin
          { only one can be down, so can exit when one is down }
          result := button.name;
          exit;
          end;
        end;
      end;
  end;

procedure TWizardForm.finishForMeristems;
  begin
  with plant.pMeristem do
    begin
    { alternate/opposite }
    if leavesAlternate.enabled then
      begin
      if leavesAlternate.down then
        branchingAndLeafArrangement := kArrangementAlternate
      else
        branchingAndLeafArrangement := kArrangementOpposite;
      end;
    { branching index }
    if branchNone.enabled then
      if branchNone.down then branchingIndex := 0
      else if branchLittle.down then branchingIndex := 10
      else if branchMedium.down then branchingIndex := 30
      else if branchLot.down then branchingIndex := 80;
    { secondary branching }
    if secondaryBranchingYes.enabled then secondaryBranchingIsAllowed := secondaryBranchingYes.down;
    { branch angle }
    if branchAngleSmall.enabled then
      if branchAngleSmall.down then branchingAngle := 20
      else if branchAngleMedium.down then branchingAngle := 40
      else if branchAngleLarge.down then branchingAngle := 60;
    end;
  end;

procedure TWizardForm.finishForInternodes;
  begin
  with plant.pInternode do
    begin
    { curviness }
    if curvinessNone.enabled then
      if curvinessNone.down then
        begin
        curvingIndex := 0;
        firstInternodeCurvingIndex := 0;
        end
      else if curvinessLittle.down then
        begin
        curvingIndex := 10;
        firstInternodeCurvingIndex := 5;
        end
      else if curvinessSome.down then
        begin
        curvingIndex := 30;
        firstInternodeCurvingIndex := 10;
        end
      else if curvinessVery.down then
        begin
        curvingIndex := 50;
        firstInternodeCurvingIndex := 20;
        end;
    { length }
    if internodesVeryShort.enabled then
      if internodesVeryShort.down then lengthAtOptimalFinalBiomassAndExpansion_mm := 1
      else if internodesShort.down then lengthAtOptimalFinalBiomassAndExpansion_mm := 10
      else if internodesMedium.down then lengthAtOptimalFinalBiomassAndExpansion_mm := 15
      else if internodesLong.down then lengthAtOptimalFinalBiomassAndExpansion_mm := 25
      else if internodesVeryLong.down then lengthAtOptimalFinalBiomassAndExpansion_mm := 50;
    { width }
    if internodeWidthVeryThin.enabled then
      if internodeWidthVeryThin.down then widthAtOptimalFinalBiomassAndExpansion_mm := 0.5
      else if internodeWidthThin.down then widthAtOptimalFinalBiomassAndExpansion_mm := 1
      else if internodeWidthMedium.down then widthAtOptimalFinalBiomassAndExpansion_mm := 2
      else if internodeWidthThick.down then widthAtOptimalFinalBiomassAndExpansion_mm := 3
      else if internodeWidthVeryThick.down then widthAtOptimalFinalBiomassAndExpansion_mm := 10;
    end;
  end;

procedure TWizardForm.finishForLeaves;
  var
    tdo: KfObject3D;
  begin
  with plant.pLeaf do
    begin
    { scale }
    if leafScaleTiny.enabled then
      if leafScaleTiny.down then leafTdoParams.scaleAtFullSize := 5
      else if leafScaleSmall.down then leafTdoParams.scaleAtFullSize := 20
      else if leafScaleMedium.down then leafTdoParams.scaleAtFullSize := 40
      else if leafScaleLarge.down then leafTdoParams.scaleAtFullSize := 60
      else if leafScaleHuge.down then leafTdoParams.scaleAtFullSize := 100;
    { petiole length }
    if petioleVeryShort.enabled then
      if petioleVeryShort.down then petioleLengthAtOptimalBiomass_mm := 1
      else if petioleShort.down then petioleLengthAtOptimalBiomass_mm := 10
      else if petioleMedium.down then petioleLengthAtOptimalBiomass_mm := 20
      else if petioleLong.down then petioleLengthAtOptimalBiomass_mm := 30
      else if petioleVeryLong.down then petioleLengthAtOptimalBiomass_mm := 60;
    { petiole angle }
    if leafAngleSmall.enabled then
      if leafAngleSmall.down then petioleAngle := 20
      else if leafAngleMedium.down then petioleAngle := 40
      else if leafAngleLarge.down then petioleAngle := 60;
    { tdo }
    if leafTdosDraw.visible then
      begin
      tdo := self.tdoForIndex(leafTdosDraw.selection.left);
      if (tdo <> nil) and (plant.pLeaf.leafTdoParams.object3D <> nil) then plant.pLeaf.leafTdoParams.object3D.copyFrom(tdo);
      end;
    end;
  end;

procedure TWizardForm.finishForCompoundLeaves;
  begin
  with plant.pLeaf do
    begin
    { num leaflets }
    if leafletsOne.enabled then
      if leafletsOne.down then compoundNumLeaflets := 1
      else if leafletsThree.down then compoundNumLeaflets := 3
      else if leafletsFour.down then compoundNumLeaflets := 4
      else if leafletsFive.down then compoundNumLeaflets := 5
      else if leafletsSeven.down then compoundNumLeaflets := 7;
    { shape }
    if leafletsPinnate.enabled then
      if leafletsPinnate.down then compoundPinnateOrPalmate := kCompoundLeafPinnate
      else if leafletsPalmate.down then compoundPinnateOrPalmate := kCompoundLeafPalmate;
    { spread }
    if leafletSpacingClose.enabled then
      if leafletSpacingClose.down then compoundRachisToPetioleRatio := 10.0
      else if leafletSpacingMedium.down then compoundRachisToPetioleRatio := 30.0
      else if leafletSpacingFar.down then compoundRachisToPetioleRatio := 50.0;
    end;
  end;

procedure TWizardForm.finishForInflorescencePlacement;
  begin
  with plant.pGeneral do
    begin
    { num apical inflors }
    if apicalInflorsNone.enabled then
      if apicalInflorsNone.down then numApicalInflors := 0
      else if apicalInflorsOne.down then numApicalInflors := 1
      else if apicalInflorsTwo.down then numApicalInflors := 2
      else if apicalInflorsThree.down then numApicalInflors := 3
      else if apicalInflorsFive.down then numApicalInflors := 5;
    { num axillary inflors }
    if axillaryInflorsNone.enabled then
      if axillaryInflorsNone.down then numAxillaryInflors := 0
      else if axillaryInflorsThree.down then numAxillaryInflors := 3
      else if axillaryInflorsFive.down then numAxillaryInflors := 5
      else if axillaryInflorsTen.down then numAxillaryInflors := 10
      else if axillaryInflorsTwenty.down then numAxillaryInflors := 20;
    // if no flowers, set age to allocate at max
    if apicalInflorsNone.enabled and apicalInflorsNone.down
      and axillaryInflorsNone.enabled and axillaryInflorsNone.down then
        ageAtWhichFloweringStarts := ageAtMaturity + 1
      else
        ageAtWhichFloweringStarts := round(ageAtMaturity * 0.6);
    end;
  with plant.pInflor[kGenderFemale] do
    begin
    { apical stalk }
    if apicalStalkVeryShort.enabled then
      if apicalStalkVeryShort.down then terminalStalkLength_mm := 1
      else if apicalStalkShort.down then terminalStalkLength_mm := 10
      else if apicalStalkMedium.down then terminalStalkLength_mm := 30
      else if apicalStalkLong.down then terminalStalkLength_mm := 50
      else if apicalStalkVeryLong.down then terminalStalkLength_mm := 100;
    { axillary stalk (peduncle) }
    if axillaryStalkVeryShort.enabled then
      if axillaryStalkVeryShort.down then peduncleLength_mm := 1
      else if axillaryStalkShort.down then peduncleLength_mm := 5
      else if axillaryStalkMedium.down then peduncleLength_mm := 10
      else if axillaryStalkLong.down then peduncleLength_mm := 15
      else if axillaryStalkVeryLong.down then peduncleLength_mm := 40;
    end;
  end;

procedure TWizardForm.finishForInflorescences;
  var numFlowers: smallint;
  begin
  if not plantHasInflorescences then exit;
  with plant.pInflor[kGenderFemale] do
    begin
    { num flowers }
    numFlowers := 0;
    if inflorFlowersOne.enabled then
      if inflorFlowersOne.down then numFlowers := 1
      else if inflorFlowersTwo.down then numFlowers := 2
      else if inflorFlowersThree.down then numFlowers := 3
      else if inflorFlowersFive.down then numFlowers := 5
      else if inflorFlowersTen.down then numFlowers := 10
      else if inflorFlowersTwenty.down then numFlowers := 20;
    numFlowersOnMainBranch := numFlowers;
    numFlowersPerBranch := 0;
    numBranches := 0;
    { shape }
    if inflorShapeSpike.enabled then
    if inflorShapeSpike.down then
      begin
      numFlowersOnMainBranch := numFlowers;
      numFlowersPerBranch := 0;
      numBranches := 0;
      pedicelLength_mm := 1;
      pedicelAngle := 30;
      internodeLength_mm := 10;
      flowersSpiralOnStem := true;
      end
    else if inflorShapeRaceme.down then
      begin
      numFlowersOnMainBranch := numFlowers;
      numFlowersPerBranch := 0;
      numBranches := 0;
      pedicelLength_mm := 20;
      pedicelAngle := 45;
      internodeLength_mm := 10;
      flowersSpiralOnStem := true;
      end
    else if inflorShapePanicle.down then
      begin
      case numFlowers of
        1: begin
          numFlowersOnMainBranch := 1;
          numFlowersPerBranch := 0;
          numBranches := 0;
          end;
        2: begin
          numFlowersOnMainBranch := 0;
          numFlowersPerBranch := 1;
          numBranches := 2;
          end;
        3: begin
          numFlowersOnMainBranch := 1;
          numFlowersPerBranch := 1;
          numBranches := 2;
          end;
        5: begin
          numFlowersOnMainBranch := 1;
          numFlowersPerBranch := 2;
          numBranches := 2;
          end;
        10: begin
          numFlowersOnMainBranch := 1;
          numFlowersPerBranch := 3;
          numBranches := 3;
          end;
        20: begin
          numFlowersOnMainBranch := 4;
          numFlowersPerBranch := 4;
          numBranches := 4;
          end;
        end;
      pedicelLength_mm := 15;
      pedicelAngle := 30;
      branchAngle := 35;
      branchesAreAlternate := true;
      internodeLength_mm := 7;
      flowersSpiralOnStem := true;
      end
    else if inflorShapeUmbel.down then
      begin
      numFlowersOnMainBranch := 0;
      numFlowersPerBranch := 1;
      numBranches := numFlowers;
      pedicelLength_mm := 20;
      pedicelAngle := 20;
      internodeLength_mm := 0.0;
      flowersSpiralOnStem := true;
      end
    else if inflorShapeCluster.down then
      begin
      numFlowersOnMainBranch := 0;
      numFlowersPerBranch := 1;
      numBranches := numFlowers;
      flowersSpiralOnStem := true;
      internodeLength_mm := 3;
      pedicelLength_mm := 1;
      pedicelAngle := 25;
     end
    else if inflorShapeHead.down then
      begin
      numFlowersOnMainBranch := numFlowers;
      numFlowersPerBranch := 0;
      numBranches := 0;
      pedicelLength_mm := 10;
      pedicelAngle := 0;
      internodeLength_mm := 10;
      isHead := true;
      flowersSpiralOnStem := false;
      end;
    { width }
    if inflorWidthVeryThin.enabled then
      if inflorWidthVeryThin.down then internodeWidth_mm := 0.5
      else if inflorWidthThin.down then internodeWidth_mm := 1
      else if inflorWidthMedium.down then internodeWidth_mm := 2
      else if inflorWidthThick.down then internodeWidth_mm := 3
      else if inflorWidthVeryThick.down then internodeWidth_mm := 10;
    end;
  end;

procedure TWizardForm.finishForFlowers;
  var
    tdo: KfObject3D;
  begin
  if not plantHasInflorescences then exit;
  with plant.pFlower[kGenderFemale].tdoParams[kFirstPetals] do
    begin
    if petalsOne.enabled then
      // cfk only first petals for wizard?
      if petalsOne.down then repetitions := 1
      else if petalsThree.down then repetitions := 3
      else if petalsFour.down then repetitions := 4
      else if petalsFive.down then repetitions := 5
      else if petalsTen.down then repetitions := 10;
    if petalScaleTiny.enabled then
      if petalScaleTiny.down then scaleAtFullSize := 4
      else if petalScaleSmall.down then scaleAtFullSize := 10
      else if petalScaleMedium.down then scaleAtFullSize := 20
      else if petalScaleLarge.down then scaleAtFullSize := 30
      else if petalScaleHuge.down then scaleAtFullSize := 60;
    if petalcolor.visible then
      begin
      faceColor := petalcolor.color;
      backfaceColor := darkerColor(faceColor);
      plant.pFlower[kGenderFemale].tdoParams[kBud].faceColor := faceColor;
      plant.pFlower[kGenderFemale].tdoParams[kBud].backfaceColor := backfaceColor;
      end;
    if petalTdosDraw.visible then
      begin
      tdo := self.tdoForIndex(petalTdosDraw.selection.left);
      // cfk first petals again
      if (tdo <> nil) and (object3D <> nil) then
        object3D.copyFrom(tdo);
      end;
    end;
  end;

procedure TWizardForm.finishForFruit;
  var
    tdo: KfObject3D;
  begin
  if not plantHasInflorescences then exit;
  with plant.pFruit.tdoParams do
    begin
    if showFruitsNo.enabled then
      begin
      if showFruitsNo.checked then
        plant.pFlower[kGenderFemale].minDaysBeforeSettingFruit := 200
      else
        plant.pFlower[kGenderFemale].minDaysBeforeSettingFruit := 3;
      end;
    { num sections }
    if fruitSectionsOne.enabled then
      if fruitSectionsOne.down then repetitions := 1
      else if fruitSectionsThree.down then repetitions := 3
      else if fruitSectionsFour.down then repetitions := 4
      else if fruitSectionsFive.down then repetitions := 5
      else if fruitSectionsTen.down then repetitions := 10;
    { scale }
    if fruitScaleTiny.enabled then
      if fruitScaleTiny.down then scaleAtFullSize := 4
      else if fruitScaleSmall.down then scaleAtFullSize := 10
      else if fruitScaleMedium.down then scaleAtFullSize := 20
      else if fruitScaleLarge.down then scaleAtFullSize := 30
      else if fruitScaleHuge.down then scaleAtFullSize := 60;
    if fruitcolor.visible then
      begin
      faceColor := fruitcolor.color;
      backFaceColor := darkerColor(faceColor);
      alternateFaceColor := faceColor;
      alternateBackFaceColor := backFaceColor;
      end;
    if sectionTdosDraw.visible then
      begin
      tdo := self.tdoForIndex(sectionTdosDraw.selection.left);
      if (tdo <> nil) and (object3D <> nil) then object3D.copyFrom(tdo);
      end;
    end;
  end;

{ ------------------------------------------------------------------------------------------- *preview }
procedure TWizardForm.drawPreview(reloadVariables: boolean);
  begin
  if plant = nil then exit;
  if reloadVariables then
    self.setPlantVariables;
  { always update cache in case any params have changed }
  try
    cursor_startWait;
    plant.useBestDrawingForPreview := true; // want nice drawing here, only case
    plant.drawPreviewIntoCache(Point(previewPaintBox.width, previewPaintBox.height), kDontConsiderDomainScale, kDrawNow);
    plant.previewCache.transparent := false;
  finally
    cursor_stopWait;
  end;
  previewPaintBox.invalidate;
  end;

procedure TWizardForm.previewPaintBoxPaint(Sender: TObject);
	begin
  if (plant <> nil) and (plant.previewCache <> nil) then
    copyBitmapToCanvasWithGlobalPalette(plant.previewCache, previewPaintBox.canvas, rect(0,0,0,0));
  end;

procedure TWizardForm.randomizePlantClick(Sender: TObject);
  begin
  plant.randomize;
  self.drawPreview(kDontReloadVariables);
  end;

procedure TWizardForm.turnLeftClick(Sender: TObject);
  begin
  if plant = nil then exit;
  plant.xRotation := plant.xRotation - 10;
  if plant.xRotation < -360 then plant.xRotation := 360;
  self.drawPreview(kDontReloadVariables);
  end;

procedure TWizardForm.turnRightClick(Sender: TObject);
  begin
  if plant = nil then exit;
  plant.xRotation := plant.xRotation + 10;
  if plant.xRotation > 360 then plant.xRotation := -360;
  self.drawPreview(kDontReloadVariables);
  end;

{ -------------------------------------------------------------------------------------------- buttons/notebook }
procedure TWizardForm.setPageIndex(newIndex: smallint);
  begin
  wizardNotebook.pageIndex := newIndex;
  end;

procedure TWizardForm.backClick(Sender: TObject);
  begin
  if wizardNotebook.pageIndex > 0 then
    begin
    if wizardNotebook.pageIndex = kFinish then
      begin
      if plantHasInflorescences then
        self.setPageIndex(kFruit)
      else
        self.setPageIndex(kInflorescencesPlacement);
      end
    else
      self.setPageIndex(wizardNotebook.pageIndex - 1);
    end;
  self.updateProgress;
  end;

procedure TWizardForm.nextClick(Sender: TObject);
  begin
  if wizardNotebook.pageIndex < kLastPanel then
    begin
    if wizardNotebook.pageIndex = kInflorescencesPlacement then
      begin
      if plantHasInflorescences then
        self.setPageIndex(kInflorescences)
      else
        self.setPageIndex(kFinish);
      end
    else
      self.setPageIndex(wizardNotebook.pageIndex + 1);
    self.updateProgress;
    end
  else
    begin
    self.setPlantVariables;
    self.saveOptionsToDomain;
    plant.shrinkPreviewCache;
    modalResult := mrOK;
    end;
  end;

procedure TWizardForm.cancelClick(Sender: TObject);
  begin
  modalResult := mrCancel;
  end;

procedure TWizardForm.FormClose(Sender: TObject; var Action: TCloseAction);
  var
    response: integer;
  begin
  // same as cancel, but if they click cancel on dialog, we must change action
  if (self.optionsHaveChanged) and (modalResult = mrCancel) then
    begin
    response := messageDlg('Do you want to save the changes you made' + chr(13)
          + 'to the wizard options?', mtConfirmation, [mbYes, mbNo, mbCancel], 0);
    case response of
      IDYES: begin self.saveOptionsToDomain; action := caFree; end;
      IDNO: action := caFree;
      IDCANCEL: action := caNone;
      end;
    end;
  end;

procedure TWizardForm.updateProgress;
  begin
  progressDrawGrid.invalidate;
  progressDrawGrid.refresh;
  if wizardNotebook.pageIndex = kLastPanel then
    begin
    previewPaintBox.visible := false;
    application.processMessages;
    self.drawPreview(kReloadVariables);
    previewPaintBox.visible := true;
    end;
  end;

procedure TWizardForm.progressDrawGridDrawCell(Sender: TObject; Col,
  Row: Longint; Rect: TRect; State: TGridDrawState);
  var
    bitmap: TBitmap;
    bitmapRect: TRect;
  begin
  with progressDrawGrid.canvas do
    begin
    brush.color := clBtnFace; // need this to make bitmaps come on as transparent
    pen.style := psClear;
    fillRect(rect);
    bitmap := self.bitmapForProgressPage(col);
    with bitmapRect do
      begin
      left := rect.left + rWidth(rect) div 2 - bitmap.width div 2;
      right := left + bitmap.width;
      top := rect.top + rHeight(rect) div 2 - bitmap.height div 2;
      bottom := top + bitmap.height;
      end;
    if bitmap <> nil then
      draw(bitmapRect.left, bitmapRect.top, bitmap);
    if col = wizardNotebook.pageIndex then
      begin
      pen.color := clRed;
      pen.style := psSolid;
      brush.style := bsClear;
      with rect do rectangle(left, top, right, bottom);
      end;
    end;
  end;

function TWizardForm.bitmapForProgressPage(page: smallint): TBitmap;
  begin
  result := nil;
  case page of
    kStart: result := startPageImage.picture.bitmap;
    kMeristems: result := meristemsPageImage.picture.bitmap;
    kInternodes: result := internodesPageImage.picture.bitmap;
    kLeaves: result := leavesPageImage.picture.bitmap;
    kCompoundLeaves: result := compoundLeavesPageImage.picture.bitmap;
    kInflorescencesPlacement: result := inflorPlacePageImage.picture.bitmap;
    kInflorescences:
      if plantHasInflorescences then
        result := inflorDrawPageImage.picture.bitmap
      else
        result := inflorDrawPageImageDisabled.picture.bitmap;
    kFlowers:
      if plantHasInflorescences then
        result := flowersPageImage.picture.bitmap
      else
        result := flowersPageImageDisabled.picture.bitmap;
    kFruit:
      if plantHasInflorescences then
        result := fruitsPageImage.picture.bitmap
      else
        result := fruitsPageImageDisabled.picture.bitmap;
    kFinish: result := finishPageImage.picture.bitmap;
    end;
  end;

procedure TWizardForm.progressDrawGridSelectCell(Sender: TObject; Col, Row: Longint; var CanSelect: Boolean);
  begin
  if ((col = kInflorescences) or (col = kFlowers) or (col = kFruit)) and (not plantHasInflorescences) then
    canSelect := false
  else
    begin
    self.setPageIndex(col);
    self.updateProgress;
    end;
  end;

procedure TWizardForm.wizardNotebookPageChanged(Sender: TObject);
  begin
  case wizardNotebook.pageIndex of
    0:
      begin
      back.enabled := false;
      next.enabled := true;
      next.caption := '&Next >';
      end;
    kLastPanel:
      begin
      back.enabled := true;
      next.caption := '&Finish';
      end;
    else
      begin
      back.enabled := true;
      next.enabled := true;
      next.caption := '&Next >';
      end;
    end;
  end;

procedure TWizardForm.petalColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  petalColor.color := domain.getColorUsingCustomColors(petalColor.color);
  end;

procedure TWizardForm.fruitColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  fruitColor.color := domain.getColorUsingCustomColors(fruitColor.color);
  end;

procedure TWizardForm.leafTdosDrawSelectCell(Sender: TObject; Col,
  Row: Integer; var CanSelect: Boolean);
  begin
  if (col <> leafTdosDraw.selection.left) then
    begin
    tdoSelectionChanged := true;
    self.showTdoNameInLabel(col, leafTdoSelectedLabel);
    end;
  end;

procedure TWizardForm.petalTdosDrawSelectCell(Sender: TObject; Col,
  Row: Integer; var CanSelect: Boolean);
  begin
  if (col <> petalTdosDraw.selection.left) then
    begin
    tdoSelectionChanged := true;
    self.showTdoNameInLabel(col, petalTdoSelectedLabel);
    end;
  end;

procedure TWizardForm.sectionTdosDrawSelectCell(Sender: TObject; Col,
  Row: Integer; var CanSelect: Boolean);
  begin
  if (col <> sectionTdosDraw.selection.left) then
    begin
    tdoSelectionChanged := true;
    self.showTdoNameInLabel(col, sectionTdoSelectedLabel);
    end;
  end;

procedure TWizardForm.sectionTdosDrawMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
  //var col, row: integer;
  begin
  //sectionTdosDraw.mouseToCell(x, y, col, row);
  //if (col <> sectionTdosDraw.selection.left) then
  //  self.showTdoNameInLabel(col, sectionTdoSelectedLabel);
  end;

procedure TWizardForm.showTdoNameInLabel(index: smallint; aLabel: TLabel);
  var tdo: KfObject3D;
  begin
  tdo := nil;
  if (index >= 0) and (index <= tdos.count - 1) then
    tdo := KfObject3D(tdos.items[index]);
  if tdo <> nil then
    aLabel.caption := tdo.getName
  else
    aLabel.caption := '';
  end;

procedure TWizardForm.helpButtonClick(Sender: TObject);
  begin
  application.helpJump('Making_a_new_plant_with_the_wizard');
  end;

procedure TWizardForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  end;

end.
