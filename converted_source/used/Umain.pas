unit Umain;

interface

uses
  SysUtils, WinTypes, WinProcs, Messages, Classes, Graphics, Controls,
  Forms, Dialogs, Menus, StdCtrls, ExtCtrls, Buttons, Tabs,
  updform, ucommand, uplant, usliders, ucollect, uppanel, ustats, usection,
  UWinSliders, udomain, Grids, usupport, u3dexport, ubitmap, Spin, ComCtrls;

const
  kCursorModeSelectDrag = 0; kCursorModeMagnify = 1; kCursorModeScroll = 2; kCursorModeRotate = 3; kCursorModePosingSelect = 4;
  kMinWidthOnScreen = 100; kMinHeightOnScreen = 100;
  kDrawNow = true; kDontDrawYet = false;
  kScaleAndMove = true; kJustMove = false;
  kAlwaysMove = true; kOnlyMoveIfOffTheScreen = false;

var
  plantFileChanged: boolean;
  
type
  TMainForm = class(PdForm)
    MainMenu: TMainMenu;
    MenuFile: TMenuItem;
    MenuFileNew: TMenuItem;
    MenuFileOpen: TMenuItem;
    MenuFileClose: TMenuItem;
    N1: TMenuItem;
    MenuFileSave: TMenuItem;
    MenuFileSaveAs: TMenuItem;
    N2: TMenuItem;
    MenuFileExit: TMenuItem;
    MenuEdit: TMenuItem;
    MenuEditUndo: TMenuItem;
    MenuEditRedo: TMenuItem;
    N3: TMenuItem;
    MenuEditCut: TMenuItem;
    MenuEditCopy: TMenuItem;
    MenuEditPaste: TMenuItem;
    MenuHelp: TMenuItem;
    MenuHelpTopics: TMenuItem;
    MenuHelpAbout: TMenuItem;
    MenuPlant: TMenuItem;
    MenuFilePlantMover: TMenuItem;
    MenuPlantRename: TMenuItem;
    MenuPlantBreed: TMenuItem;
    MenuPlantRandomize: TMenuItem;
    MenuPlantNew: TMenuItem;
    N7: TMenuItem;
    toolbarPanel: TPanel;
    dragCursorMode: TSpeedButton;
    magnifyCursorMode: TSpeedButton;
    scrollCursorMode: TSpeedButton;
    horizontalSplitter: TPanel;
    verticalSplitter: TPanel;
    paletteImage: TImage;
    MenuEditPreferences: TMenuItem;
    visibleBitmap: TImage;
    PlantPopupMenu: TPopupMenu;
    MenuFileSaveDrawingAs: TMenuItem;
    MenuFilePrintDrawing: TMenuItem;
    MenuEditCopyDrawing: TMenuItem;
    PopupMenuCut: TMenuItem;
    PopupMenuCopy: TMenuItem;
    PopupMenuPaste: TMenuItem;
    N6: TMenuItem;
    MenuEditDelete: TMenuItem;
    N5: TMenuItem;
    PrintDialog: TPrintDialog;
    sectionImagesPanel: TPanel;
    Sections_FlowersPrimary: TImage;
    Sections_General: TImage;
    Sections_InflorPrimary: TImage;
    Sections_Meristems: TImage;
    Sections_Leaves: TImage;
    Sections_RootTop: TImage;
    Sections_Fruit: TImage;
    Sections_InflorSecondary: TImage;
    Sections_Internodes: TImage;
    Sections_SeedlingLeaves: TImage;
    Sections_FlowersSecondary: TImage;
    PopupMenuRename: TMenuItem;
    PopupMenuRandomize: TMenuItem;
    PopupMenuBreed: TMenuItem;
    rotateCursorMode: TSpeedButton;
    MenuPlantExportToDXF: TMenuItem;
    MenuPlantMakeTimeSeries: TMenuItem;
    MenuWindow: TMenuItem;
    MenuWindowBreeder: TMenuItem;
    MenuWindowTimeSeries: TMenuItem;
    N12: TMenuItem;
    MenuWindowNumericalExceptions: TMenuItem;
    animateTimer: TTimer;
    MenuPlantAnimate: TMenuItem;
    centerDrawing: TSpeedButton;
    MenuOptions: TMenuItem;
    MenuOptionsShowLongButtonHints: TMenuItem;
    MenuOptionsShowParameterHints: TMenuItem;
    MenuOptionsShowSelectionRectangles: TMenuItem;
    paramPanelOpenArrowImage: TImage;
    paramPanelClosedArrowImage: TImage;
    plantListPanel: TPanel;
    progressPaintBox: TPaintBox;
    plantFocusPanel: TPanel;
    lifeCyclePanel: TPanel;
    lifeCycleGraphImage: TImage;
    timeLabel: TLabel;
    selectedPlantNameLabel: TLabel;
    lifeCycleEditPanel: TPanel;
    daysAndSizeLabel: TLabel;
    ageAndSizeLabel: TLabel;
    lifeCycleDaysEdit: TEdit;
    lifeCycleDaysSpin: TSpinButton;
    lifeCycleDragger: TPanel;
    statsScrollBox: TScrollBox;
    tabSet: TTabSet;
    parametersPanel: TPanel;
    parametersScrollBox: TScrollBox;
    PopupMenuMakeTimeSeries: TMenuItem;
    PopupMenuAnimate: TMenuItem;
    MenuLayout: TMenuItem;
    MenuLayoutSelectAll: TMenuItem;
    MenuLayoutDeselect: TMenuItem;
    MenuLayoutHide: TMenuItem;
    MenuLayoutHideOthers: TMenuItem;
    MenuLayoutShow: TMenuItem;
    N18: TMenuItem;
    MenuLayoutBringForward: TMenuItem;
    MenuLayoutSendBack: TMenuItem;
    N19: TMenuItem;
    MenuLayoutHorizontalOrientation: TMenuItem;
    MenuLayoutVerticalOrientation: TMenuItem;
    MenuLayoutScaleToFit: TMenuItem;
    MenuLayoutViewOnePlantAtATime: TMenuItem;
    MenuLayoutMakeBouquet: TMenuItem;
    maxSizeAxisLabel: TLabel;
    plantFileChangedImage: TImage;
    fileChangedImage: TImage;
    fileNotChangedImage: TImage;
    plantListDrawGrid: TDrawGrid;
    MenuEditDuplicate: TMenuItem;
    N8: TMenuItem;
    MenuPlantNewUsingLastWizardSettings: TMenuItem;
    N4: TMenuItem;
    paramPopupMenu: TPopupMenu;
    paramPopupMenuHelp: TMenuItem;
    N15: TMenuItem;
    paramPopupMenuExpand: TMenuItem;
    paramPopupMenuCollapse: TMenuItem;
    AfterRegisterMenuSeparator: TMenuItem;
    MenuFileTdoMover: TMenuItem;
    animateGrowth: TSpeedButton;
    MenuFileMakePainterNozzle: TMenuItem;
    unregisteredExportReminder: TImage;
    MenuFileMakePainterAnimation: TMenuItem;
    N17: TMenuItem;
    N13: TMenuItem;
    MenuHelpRegister: TMenuItem;
    MenuHelpSuperSpeedTour: TMenuItem;
    MenuHelpTutorial: TMenuItem;
    MenuEditCopyAsText: TMenuItem;
    plantsAsTextMemo: TMemo;
    MenuEditPasteAsText: TMenuItem;
    N16: TMenuItem;
    MenuOptionsFastDraw: TMenuItem;
    MenuOptionsMediumDraw: TMenuItem;
    MenuOptionsBestDraw: TMenuItem;
    MenuOptionsCustomDraw: TMenuItem;
    MenuOptionsUsePlantBitmaps: TMenuItem;
    plantBitmapsIndicatorImage: TImage;
    plantBitmapsGreenImage: TImage;
    noPlantBitmapsImage: TImage;
    plantBitmapsYellowImage: TImage;
    plantBitmapsRedImage: TImage;
    animatingLabel: TLabel;
    N22: TMenuItem;
    MenuPlantZeroRotations: TMenuItem;
    PopupMenuZeroRotations: TMenuItem;
    rotationsPanel: TPanel;
    xRotationLabel: TLabel;
    xRotationEdit: TEdit;
    xRotationSpin: TSpinButton;
    yRotationLabel: TLabel;
    yRotationEdit: TEdit;
    yRotationSpin: TSpinButton;
    zRotationLabel: TLabel;
    zRotationEdit: TEdit;
    zRotationSpin: TSpinButton;
    resetRotations: TSpeedButton;
    rotationLabel: TLabel;
    magnificationPercent: TComboBox;
    N10: TMenuItem;
    Reconcile3DObjects1: TMenuItem;
    notePanel: TPanel;
    noteMemo: TMemo;
    noteLabel: TLabel;
    noteEdit: TSpeedButton;
    PopupMenuEditNote: TMenuItem;
    MenuPlantEditNote: TMenuItem;
    N25: TMenuItem;
    paramPopupMenuCopyName: TMenuItem;
    MenuPlantExportToPOV: TMenuItem;
    MenuFileExport: TMenuItem;
    Recent0: TMenuItem;
    Recent1: TMenuItem;
    Recent2: TMenuItem;
    Recent3: TMenuItem;
    Recent4: TMenuItem;
    MenuFileReopen: TMenuItem;
    Recent5: TMenuItem;
    Recent6: TMenuItem;
    Recent7: TMenuItem;
    Recent8: TMenuItem;
    Recent9: TMenuItem;
    viewFreeFloating: TSpeedButton;
    viewOneOnly: TSpeedButton;
    MenuOptionsDrawAs: TMenuItem;
    drawingAreaOnTop: TSpeedButton;
    drawingAreaOnSide: TSpeedButton;
    MenuLayoutDrawingAreaOn: TMenuItem;
    MenuLayoutView: TMenuItem;
    MenuLayoutViewFreeFloating: TMenuItem;
    Sections_FlowersPrimaryAdvanced: TImage;
    sizingLabel: TLabel;
    drawingScaleEdit: TEdit;
    drawingScaleSpin: TSpinButton;
    drawingScalePixelsPerMmLabel: TLabel;
    packPlants: TSpeedButton;
    locationLabel: TLabel;
    xLocationLabel: TLabel;
    xLocationEdit: TEdit;
    xLocationSpin: TSpinButton;
    yLocationLabel: TLabel;
    yLocationEdit: TEdit;
    yLocationSpin: TSpinButton;
    locationPixelsLabel: TLabel;
    arrangementPlantName: TLabel;
    alignTops: TSpeedButton;
    alignBottoms: TSpeedButton;
    alignLeft: TSpeedButton;
    alignRight: TSpeedButton;
    makeEqualWidth: TSpeedButton;
    makeEqualHeight: TSpeedButton;
    MenuLayoutAlign: TMenuItem;
    MenuLayoutAlignTops: TMenuItem;
    MenuLayoutAlignBottoms: TMenuItem;
    MenuLayoutAlignLeftSides: TMenuItem;
    MenuLayoutAlignRightSides: TMenuItem;
    MenuLayoutSize: TMenuItem;
    MenuLayoutSizeSameHeight: TMenuItem;
    MenuLayoutSizeSameWidth: TMenuItem;
    MenuLayoutPack: TMenuItem;
    parametersPlantName: TLabel;
    MenuPlantExportTo3DS: TMenuItem;
    N9: TMenuItem;
    posingPanel: TPanel;
    posingPlantName: TLabel;
    MenuOptionsGhostHiddenParts: TMenuItem;
    posingDetailsPanel: TPanel;
    posingXRotationLabel: TLabel;
    posingYRotationLabel: TLabel;
    posingZRotationLabel: TLabel;
    posingScaleMultiplierPercent: TLabel;
    posingHidePart: TCheckBox;
    posingXRotationEdit: TEdit;
    posingXRotationSpin: TSpinButton;
    posingYRotationEdit: TEdit;
    posingYRotationSpin: TSpinButton;
    posingZRotationEdit: TEdit;
    posingZRotationSpin: TSpinButton;
    posingAddExtraRotation: TCheckBox;
    posingMultiplyScale: TCheckBox;
    MenuOptionsHighlightPosedParts: TMenuItem;
    MenuOptionsPosing: TMenuItem;
    N20: TMenuItem;
    N21: TMenuItem;
    MenuFileMove: TMenuItem;
    posingScaleMultiplierLabel: TLabel;
    posingLengthMultiplierPercent: TLabel;
    posingLengthMultiplierLabel: TLabel;
    posingWidthMultiplierPercent: TLabel;
    posingWidthMultiplierLabel: TLabel;
    posingMultiplyScaleAllPartsAfter: TCheckBox;
    MenuOptionsShowBoundsRectangles: TMenuItem;
    MenuOptionsDrawRectangles: TMenuItem;
    MenuOptionsHints: TMenuItem;
    MenuFileSaveJPEG: TMenuItem;
    posingScaleMultiplierEdit: TEdit;
    posingScaleMultiplierSpin: TSpinButton;
    posingLengthMultiplierEdit: TEdit;
    posingLengthMultiplierSpin: TSpinButton;
    posingWidthMultiplierEdit: TEdit;
    posingWidthMultiplierSpin: TSpinButton;
    MenuOptionsHidePosing: TMenuItem;
    UndoMenuEditUndoRedoList: TMenuItem;
    MenuPlantExportToOBJ: TMenuItem;
    MenuPlantExportToVRML: TMenuItem;
    MenuPlantExportToLWO: TMenuItem;
    sectionsComboBox: TComboBox;
    paramPopupMenuExpandAllInSection: TMenuItem;
    paramPopupMenuCollapseAllInSection: TMenuItem;
    N11: TMenuItem;
    hideExtraLabel: TLabel;
    rotationDegreesLabel: TLabel;
    posingColorsPanel: TPanel;
    posingLineColorLabel: TLabel;
    posingFrontfaceColorLabel: TLabel;
    posingBackfaceColorLabel: TLabel;
    posingChangeColors: TCheckBox;
    posingChangeAllColorsAfter: TCheckBox;
    posingLineColor: TPanel;
    posingFrontfaceColor: TPanel;
    posingBackfaceColor: TPanel;
    posingSelectionCursorMode: TSpeedButton;
    posedPartsLabel: TLabel;
    posedPlantParts: TComboBox;
    posingHighlight: TSpeedButton;
    posingGhost: TSpeedButton;
    posingNotShown: TSpeedButton;
    selectedPartLabel: TLabel;
    posingPosePart: TSpeedButton;
    posingUnposePart: TSpeedButton;
    posingMultiplyScaleAllPartsAfterLabel: TLabel;
    sectionPopupMenuHelp: TMenuItem;
    Sections_Orthogonal: TImage;
    procedure FormCreate(Sender: TObject);
    procedure FormResize(Sender: TObject);
    procedure horizontalSplitterMouseDown(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure horizontalSplitterMouseMove(Sender: TObject;
      Shift: TShiftState; X, Y: Integer);
    procedure horizontalSplitterMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure verticalSplitterMouseDown(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure verticalSplitterMouseMove(Sender: TObject;
      Shift: TShiftState; X, Y: Integer);
    procedure verticalSplitterMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure MenuFileNewClick(Sender: TObject);
    procedure MenuFileOpenClick(Sender: TObject);
    procedure MenuFileCloseClick(Sender: TObject);
    procedure MenuFileSaveClick(Sender: TObject);
    procedure MenuFileSaveAsClick(Sender: TObject);
    procedure MenuFileExitClick(Sender: TObject);
    procedure drawingPaintBoxPaint(Sender: TObject);
    procedure MenuEditPreferencesClick(Sender: TObject);       
    procedure MenuEditUndoClick(Sender: TObject);
    procedure MenuEditRedoClick(Sender: TObject);
    procedure FormClose(Sender: TObject; var Action: TCloseAction);
    procedure dragCursorModeClick(Sender: TObject);
    procedure magnifyCursorModeClick(Sender: TObject);
    procedure scrollCursorModeClick(Sender: TObject);        
    procedure FormKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);                                            
    procedure FormKeyUp(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure lifeCycleDraggerMouseDown(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure lifeCycleDraggerMouseMove(Sender: TObject;
      Shift: TShiftState; X, Y: Integer);
    procedure lifeCycleDraggerMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure lifeCycleDaysEditExit(Sender: TObject);
    procedure lifeCycleDaysSpinUpClick(Sender: TObject);
    procedure lifeCycleDaysSpinDownClick(Sender: TObject);
    procedure MenuEditCopyDrawingClick(Sender: TObject);
    procedure MenuEditCutClick(Sender: TObject);
    procedure MenuEditCopyClick(Sender: TObject);
    procedure MenuEditPasteClick(Sender: TObject);
    procedure MenuPlantRenameClick(Sender: TObject);
    procedure PopupMenuCutClick(Sender: TObject);
    procedure PopupMenuCopyClick(Sender: TObject);
    procedure PopupMenuPasteClick(Sender: TObject);
    procedure MenuEditDeleteClick(Sender: TObject);
    procedure MenuPlantNewClick(Sender: TObject);
    procedure MenuPlantRandomizeClick(Sender: TObject);
    procedure MenuHelpAboutClick(Sender: TObject);
    procedure MenuFilePrintDrawingClick(Sender: TObject);
    procedure MenuFileSaveDrawingAsClick(Sender: TObject);
    procedure tabSetChange(Sender: TObject; NewTab: Integer;
      var AllowChange: Boolean);
    procedure PopupMenuRenameClick(Sender: TObject);
    procedure PopupMenuRandomizeClick(Sender: TObject);
    procedure PopupMenuBreedClick(Sender: TObject);
    procedure MenuPlantBreedClick(Sender: TObject);
    procedure FormDestroy(Sender: TObject);
    procedure magnifyPlusClick(Sender: TObject);
    procedure magnifyMinusClick(Sender: TObject);
    procedure centerDrawingClick(Sender: TObject);
    procedure xRotationEditExit(Sender: TObject);
    procedure xRotationSpinUpClick(Sender: TObject);
    procedure xRotationSpinDownClick(Sender: TObject);
    procedure yRotationEditExit(Sender: TObject);
    procedure yRotationSpinUpClick(Sender: TObject);
    procedure yRotationSpinDownClick(Sender: TObject);
    procedure zRotationEditExit(Sender: TObject);
    procedure zRotationSpinUpClick(Sender: TObject);
    procedure zRotationSpinDownClick(Sender: TObject);
    procedure resetRotationsClick(Sender: TObject);
    procedure xRotationEditChange(Sender: TObject);
    procedure yRotationEditChange(Sender: TObject);
    procedure zRotationEditChange(Sender: TObject);
    procedure MenuFilePlantMoverClick(Sender: TObject);
    procedure rotateCursorModeClick(Sender: TObject);
    procedure MenuPlantExportToDXFClick(Sender: TObject);
    procedure MenuPlantMakeTimeSeriesClick(Sender: TObject);
    procedure FormKeyPress(Sender: TObject; var Key: Char);
    procedure MenuWindowBreederClick(Sender: TObject);
    procedure MenuWindowTimeSeriesClick(Sender: TObject);
    procedure MenuWindowNumericalExceptionsClick(Sender: TObject);
    procedure animateGrowthClick(Sender: TObject);
    procedure animateTimerTimer(Sender: TObject);
    procedure MenuPlantAnimateClick(Sender: TObject);
    procedure progressPaintBoxPaint(Sender: TObject);
    procedure MenuOptionsShowSelectionRectanglesClick(Sender: TObject);
    procedure MenuOptionsShowLongButtonHintsClick(Sender: TObject);
    procedure MenuOptionsShowParameterHintsClick(Sender: TObject);
    procedure PopupMenuHideAllOthersClick(Sender: TObject);
    procedure PopupMenuHideClick(Sender: TObject);
    procedure PopupMenuShowClick(Sender: TObject);
    procedure PopupMenuMakeTimeSeriesClick(Sender: TObject);
    procedure PopupMenuAnimateClick(Sender: TObject);
    procedure MenuLayoutSelectAllClick(Sender: TObject);
    procedure MenuLayoutDeselectClick(Sender: TObject);
    procedure MenuLayoutShowClick(Sender: TObject);
    procedure MenuLayoutHideClick(Sender: TObject);
    procedure MenuLayoutHideOthersClick(Sender: TObject);
    procedure MenuLayoutScaleToFitClick(Sender: TObject);
    procedure MenuLayoutBringForwardClick(Sender: TObject);
    procedure MenuLayoutSendBackClick(Sender: TObject);
    procedure MenuLayoutHorizontalOrientationClick(Sender: TObject);
    procedure MenuLayoutVerticalOrientationClick(Sender: TObject);
    procedure MenuLayoutViewOnePlantAtATimeClick(Sender: TObject);
    procedure MenuLayoutMakeBouquetClick(Sender: TObject);
    procedure plantListDrawGridDrawCell(Sender: TObject; Col, Row: Integer;
      Rect: TRect; State: TGridDrawState);
    procedure plantListDrawGridMouseDown(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure plantListDrawGridDragOver(Sender, Source: TObject; X, Y: Integer;
      State: TDragState; var Accept: Boolean);
    procedure plantListDrawGridEndDrag(Sender, Target: TObject; X, Y: Integer);
    procedure plantListDrawGridKeyDown(Sender: TObject; var Key: Word;
      Shift: TShiftState);
    procedure MenuEditDuplicateClick(Sender: TObject);
    procedure MenuPlantNewUsingLastWizardSettingsClick(Sender: TObject);
    procedure MenuHelpTopicsClick(Sender: TObject);
    procedure sectionPopupMenuHelpClick(Sender: TObject);
    procedure paramPopupMenuHelpClick(Sender: TObject);
    procedure paramPopupMenuExpandClick(Sender: TObject);
    procedure paramPopupMenuCollapseClick(Sender: TObject);
    procedure MenuFileTdoMoverClick(Sender: TObject);
    procedure plantListDrawGridMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure MenuFileMakePainterNozzleClick(Sender: TObject);
    procedure MenuFileMakePainterAnimationClick(Sender: TObject);
    procedure MenuHelpRegisterClick(Sender: TObject);
    procedure MenuHelpSuperSpeedTourClick(Sender: TObject);
    procedure MenuHelpTutorialClick(Sender: TObject);
    procedure MenuEditCopyAsTextClick(Sender: TObject);
    procedure MenuEditPasteAsTextClick(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure MenuOptionsFastDrawClick(Sender: TObject);
    procedure MenuOptionsMediumDrawClick(Sender: TObject);
    procedure MenuOptionsBestDrawClick(Sender: TObject);
    procedure MenuOptionsCustomDrawClick(Sender: TObject);
    procedure magnificationPercentClick(Sender: TObject);
    procedure magnificationPercentExit(Sender: TObject);
    procedure plantListDrawGridDblClick(Sender: TObject);
    procedure MenuOptionsUsePlantBitmapsClick(Sender: TObject);
    procedure MenuPlantZeroRotationsClick(Sender: TObject);
    procedure PopupMenuZeroRotationsClick(Sender: TObject);
    procedure plantBitmapsIndicatorImageClick(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure Reconcile3DObjects1Click(Sender: TObject);
    procedure noteEditClick(Sender: TObject);
    procedure MenuPlantEditNoteClick(Sender: TObject);
    procedure PopupMenuEditNoteClick(Sender: TObject);
    procedure NotePopupMenuCopyClick(Sender: TObject);
    procedure NotePopupMenuEditClick(Sender: TObject);
    procedure NotePopupMenuSelectAllClick(Sender: TObject);
    procedure paramPopupMenuCopyNameClick(Sender: TObject);
    procedure MenuPlantExportToPOVClick(Sender: TObject);
    procedure Recent0Click(Sender: TObject);
    procedure drawingAreaOnTopClick(Sender: TObject);
    procedure drawingAreaOnSideClick(Sender: TObject);
    procedure viewFreeFloatingClick(Sender: TObject);
    procedure viewOneOnlyClick(Sender: TObject);
    procedure MenuLayoutViewFreeFloatingClick(Sender: TObject);
    procedure drawingScaleSpinDownClick(Sender: TObject);
    procedure drawingScaleSpinUpClick(Sender: TObject);
    procedure drawingScaleEditExit(Sender: TObject);
    procedure packPlantsClick(Sender: TObject);
    procedure alignTopsClick(Sender: TObject);
    procedure alignBottomsClick(Sender: TObject);
    procedure alignLeftClick(Sender: TObject);
    procedure alignRightClick(Sender: TObject);
    procedure makeEqualWidthClick(Sender: TObject);
    procedure makeEqualHeightClick(Sender: TObject);
    procedure MenuLayoutAlignTopsClick(Sender: TObject);
    procedure MenuLayoutAlignBottomsClick(Sender: TObject);
    procedure MenuLayoutAlignLeftSidesClick(Sender: TObject);
    procedure MenuLayoutAlignRightSidesClick(Sender: TObject);
    procedure MenuLayoutSizeSameWidthClick(Sender: TObject);
    procedure MenuLayoutSizeSameHeightClick(Sender: TObject);
    procedure MenuLayoutPackClick(Sender: TObject);
    procedure xLocationEditExit(Sender: TObject);
    procedure yLocationEditExit(Sender: TObject);
    procedure xLocationSpinDownClick(Sender: TObject);
    procedure xLocationSpinUpClick(Sender: TObject);
    procedure yLocationSpinDownClick(Sender: TObject);
    procedure yLocationSpinUpClick(Sender: TObject);
    procedure MenuPlantExportTo3DSClick(Sender: TObject);
    procedure MenuOptionsGhostHiddenPartsClick(Sender: TObject);
    procedure posedPlantPartsChange(Sender: TObject);
    procedure posingPosePartClick(Sender: TObject);
    procedure posingUnposePartClick(Sender: TObject);
    procedure posingBackfaceColorMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure changeSelectedPose(Sender: TObject);
    procedure posingFrontfaceColorMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure posingLineColorMouseUp(Sender: TObject;
      Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure MenuOptionsHighlightPosedPartsClick(Sender: TObject);
    procedure MenuOptionsShowBoundsRectanglesClick(Sender: TObject);
    procedure MenuFileSaveJPEGClick(Sender: TObject);
    procedure posingScaleMultiplierSpinDownClick(Sender: TObject);
    procedure posingScaleMultiplierSpinUpClick(Sender: TObject);
    procedure posingRotationSpinUp(Sender: TObject);
    procedure posingRotationSpinDown(Sender: TObject);
    procedure MenuOptionsHidePosingClick(Sender: TObject);
    procedure UndoMenuEditUndoRedoListClick(Sender: TObject);
    procedure MenuPlantExportToOBJClick(Sender: TObject);
    procedure MenuPlantExportToVRMLClick(Sender: TObject);
    procedure MenuPlantExportToLWOClick(Sender: TObject);
    procedure sectionsComboBoxDrawItem(Control: TWinControl;
      Index: Integer; Rect: TRect; State: TOwnerDrawState);
    procedure sectionsComboBoxChange(Sender: TObject);
    procedure paramPopupMenuExpandAllInSectionClick(Sender: TObject);
    procedure paramPopupMenuCollapseAllInSectionClick(Sender: TObject);
    procedure posingHighlightClick(Sender: TObject);
    procedure posingGhostClick(Sender: TObject);
    procedure posingNotShownClick(Sender: TObject);
    procedure posingSelectionCursorModeClick(Sender: TObject);
  private
    { Private declarations }
    procedure WMGetMinMaxInfo(var MSG: Tmessage);  message WM_GetMinMaxInfo;
    procedure WMQueryEndSession(var message: TWMQueryEndSession); message WM_QueryEndSession;
    procedure WMDropFiles(var Msg: TWMDropFiles); message WM_DROPFILES;
  public
    { Public declarations }
    { dependent objects }
    drawingBitmap: TBitmap;
    commandList: PdCommandList;
    drawingPaintBox: PdPaintBoxWithPalette;
    statsPanel: PdStatsPanel;
    { general }
    invalidDrawingRect: TRect;
    internalChange, inFormCreation, inFileOpen: boolean;
    lastSaveProceeded: boolean;
    resizingAtStart: boolean;
    { plant handling }
    plants: TListCollection;
    selectedPlants: TList;
    numPlantsInClipboard: smallint;
    lastSingleClickPlantIndex: integer;
    justDoubleClickedOnDrawGrid: boolean;
    { selecting plants with rubber banding }
    rubberBanding, rubberBandNeedToRedraw: boolean;
    rubberBandStartDragPoint, rubberBandLastDrawPoint: TPoint;
    { drawing and progress }
    drawing: boolean;
    animateCommand: PdCommand;
    drawProgressMax: longint;
    { mouse movement }
    cursorModeForDrawing: smallint;
    actionInProgress, mouseMoveActionInProgress: boolean;
    lifeCycleDragging, lifeCycleDraggingNeedToRedraw: boolean;
    lifeCycleDraggingStartPos, lifeCycleDraggingLastDrawPos: smallint;
    cursorPosInDrawingPaintBox: TPoint;
    { resizing and splitting }
    horizontalSplitterDragging, verticalSplitterDragging: boolean;
    horizontalSplitterNeedToRedraw, verticalSplitterNeedToRedraw: boolean;
    horizontalSplitterStartPos, verticalSplitterStartPos: integer;
    horizontalSplitterLastDrawPos, verticalSplitterLastDrawPos: integer;
    lastWidth, lastHeight: integer;
    { hints }
		hintX, hintY: integer;
    hintActive: boolean;
    lastHintString: string;
    { parameters panel }
    backTabbingInParametersPanel: boolean;
    selectedParameterPanel: PdParameterPanel;
    // posings panel
    selectedPlantPartID, mouseDownSelectedPlantPartID: longint;
    selectedPlantPartType, mouseDownSelectedPlantPartType: string;
    { file menu }
    procedure openFile(fileNameWithPath: string);
    procedure setPlantFileChanged(fileChanged: boolean);
    function askForSaveAndProceed: boolean;
    function cleanUpBeforeExit: boolean;
    function storeIniFile: boolean;
    { edit menu }
    procedure copySelectedPlantsToClipboard;
    procedure fillBitmapForExport(bitmapForExport: TBitmap; options: BitmapOptionsStructure);
    procedure pastePlantsFromClipboard;
    function standardPastePosition: TPoint;
    { plant menu }
    { help menu }
    { updating }
    procedure updateForNoPlantFile;
    procedure updateForPlantFile;
    procedure updateForChangedExportCount;
    function captionForFile: string;
    procedure updateHintPauseForOptions;
    procedure updateForChangeToDomainOptions;
    procedure updateForChangeToDrawOptions;
    procedure updateForRegistrationChange;
    procedure updateMenusForChangeToViewingOption;
    procedure updateForChangeToOrientation;
    procedure updateForChangeToPlantList;
    procedure moveUpOrDownWithKeyInPlantList(indexAfterMove: smallint);
    procedure updateForChangeToPlantSelections;
    procedure updateForPossibleChangeToDrawing;
    procedure updateLifeCyclePanelForFirstSelectedPlant;
    procedure updateRightSidePanelForFirstSelectedPlant;
    procedure updateRightSidePanelForFirstSelectedPlantWithTab(newTab: integer);
    procedure updateForRenamingPlant(aPlant: PdPlant);
    procedure updateForChangeToPlantNote(aPlant: PdPlant);
    procedure updateForChangeToPlantRotations;
    procedure updateForChangeToSelectedPlantsDrawingScale;
    procedure updateForChangeToSelectedPlantsLocation;
    function textColorToRepresentPlantSelection(payAttentionToMultiSelect: boolean): TColorRef;
    procedure updatePlantNameLabel(tabIndex: smallint);
    { menu updating }
    procedure updateMenusForUndoRedo;
    procedure updateMenusForChangedPlantFile;
    procedure updateMenusForChangedPlantList;
    procedure updateMenusForChangedSelectedPlants;
    procedure updatePasteMenuForClipboardContents;
    procedure updateSectionPopupMenuForSectionChange;
    procedure updateParamPopupMenuForParamSelectionChange;
    { drawing }
    procedure changeViewingOptionTo(aNewOption: smallint);
    function upperLeftMostPlantBoundsRectPoint_mm: TPoint;
    function lowerRightMostPlantBoundsRectPoint_mm: TPoint;
    procedure invalidateSelectedPlantRectangles;
    procedure invalidateDrawingRect(aRect: TRect);
    procedure invalidateEntireDrawing;
    procedure recalculateAllPlantBoundsRects(drawNow: boolean);
    procedure recalculateSelectedPlantsBoundsRects(drawNow: boolean);
    procedure recalculateAllPlantBoundsRectsForOffsetChange;
    procedure redrawEverything;
    procedure shrinkAllPlantBitmaps;
    procedure paintDrawing(immediate: boolean);
    procedure copyDrawingBitmapToPaintBox;
    procedure showDrawProgress(amount: longint);
    procedure startDrawProgress(maximum: longint);
    procedure finishDrawProgress;
    { command list management }
    procedure clearCommandList;
    procedure doCommand(command: PdCommand);
    function makeMouseCommand(var point: TPoint; shift: TShiftState): PdCommand;
    { called by commands }
    procedure hideOrShowSomePlants(plantList: TList; hideList: TList; hide: boolean; drawNow: boolean);
    procedure fitVisiblePlantsInDrawingArea(drawNow: boolean; scaleAsWellAsMove: boolean; alwaysMove: boolean);
    { rubber banding }
    procedure selectPlantsInRubberBandBox;
    procedure drawRubberBandBox(newPoint: TPoint);
    procedure undrawRubberBandBox;
    procedure drawOrUndrawRubberBandBox;
    { selected plants list }
    function focusedPlant: PdPlant;
    function focusedPlantIndex: smallint;
    function firstUnfocusedPlant: PdPlant;
    function firstSelectedPlantInList: PdPlant;
    function lastSelectedPlantInList: PdPlant;
    procedure deselectAllPlantsButFirst;
    procedure selectFirstPlantInPlantList;
    procedure showOnePlantExclusively(drawNow: boolean);
    procedure deselectAllPlants;
    procedure redrawFocusedPlantOnly(drawNow: boolean);
    procedure addSelectedPlant(aPlant: PdPlant; insertIndex: smallint);
    procedure removeSelectedPlant(aPlant: PdPlant);
    function isSelected(plant: PdPlant): boolean;
    function isFocused(plant: PdPlant): boolean;
    { list box }
    procedure moveSelectedPlantsUp;
    procedure moveSelectedPlantsDown;
    { mouse handling in drawing }
    procedure PaintBoxMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure PaintBoxMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
    procedure PaintBoxMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
    procedure PaintBoxEndDrag(Sender, Target: TObject; X, Y: Integer);
    procedure PaintBoxDragOver(Sender, Source: TObject; X, Y: Integer; State: TDragState; var Accept: Boolean);
    procedure selectPlantAtPoint(aPoint: TPoint; shift: boolean);
    procedure selectPlantAtIndex(Shift: TShiftState; index: Integer);
    function twoListsAreIdentical(firstList, secondList: TList): boolean;
    procedure nudgeSelectedPlantsByKey(key: word);
    procedure nudgeSelectedPlantsByPixelsAndDirection(pixels: integer; direction: smallint);
    procedure resizeSelectedPlantsByKey(key: word);
    procedure resizeSelectedPlantsWithMultiplierOrNewAmount(multiplier, newAmount_pixelsPerMm: single);
    procedure alignSelectedPlants(alignDirection: smallint);
    { hint handling }
    procedure DoShowHint(var HintStr: ansistring; var CanShow: Boolean; var HintInfo: THintInfo);
    function hintForPlantAtPoint(aPoint: TPoint): string;
    { popup menu commands }
    { toolbar }
    procedure changeMagnificationWithoutClick;
    function magnifyScaleForText(aText: string): single;
    function magnifyOrReduce(newScale_PixelsPerMm: single; point_pixels: TPoint; drawNow: boolean): TPoint;
    procedure checkRotationEditAgainstBounds(edit: TEdit);
    procedure changeSelectedPlantRotations(edit: TEdit; rotateDirection, changeInRotation: smallint);
    { tab set }
    function lifeCycleShowing: boolean;
    function rotationsShowing: boolean;
    function parametersShowing: boolean;
    function statsShowing: boolean;
    function noteShowing: boolean;
    function posingShowing: boolean;
    { life cycle panel drawing and mouse handling }
    procedure redrawLifeCycleGraph;
    procedure drawSCurveOrCheckForError(aCanvas: TCanvas; aRect: TRect; draw: boolean; var failed: boolean);
    procedure changeSelectedPlantAges(newAge: smallint);
    procedure resizeParametersPanel;
    procedure placeLifeCycleDragger;
    function drawLifeCycleDraggerLine(pos: integer): integer;
    procedure undrawLifeCycleDraggerLine;
    { parameters panel }
    procedure loadSectionsIntoListBox;
    function currentSection: PdSection;
    function sectionPictureForSectionName(aName: string): TPicture;
    function sectionHelpIDForSectionName(aName: string): string;
    procedure enteringAParameterPanel(aPanel: PdParameterPanel);
    procedure leavingAParameterPanel(aPanel: PdParameterPanel);
    procedure repositionParameterPanels;
    procedure collapseOrExpandParameterPanelsUntilNextHeader(headerPanel: PdParameterPanel);
    procedure collapseOrExpandAllParameterPanelsInCurrentSection(doWhat: smallint);
    procedure updateParameterValuesWithUpdateListForPlant(aPlant: PdPlant; updateList: TListCollection);
    procedure updateParameterPanelsForSectionChange;
    procedure updateParametersPanelForFirstSelectedPlant;
    function paramHelpIDForParamPanel(panel: PdParameterPanel): string;
    // stats panel
    procedure updateStatisticsPanelForFirstSelectedPlant;
    // rotations panel
    procedure updateRotationsPanelForFirstSelectedPlant;
    // note panel
    procedure updateNoteForFirstSelectedPlant;
    // posing panel
    procedure updatePosingForFirstSelectedPlant;
    procedure updatePosingForSelectedPlantPart;
    function partDescriptionForIDAndType(id: longint; typeName: string): string;
    function partIDForFullDescription(aString: string): longint;
    function partTypeForFullDescription(aString: string): string;
    function selectedPartIDInAmendedPartsList: longint;
    function selectedPartTypeInAmendedPartsList: string;
    procedure updatePoseInfo;
    procedure updateForDependenciesWithinPoseInfo;
    procedure addAmendedPartToList(partID: longint; partType: string);
    procedure removeAmendedPartFromList(partID: longint; partType: string);
    procedure redrawAllPlantsInViewWithAmendments;
    procedure spinPoseRotationBy(sender: TObject; amount: integer);
    procedure spinScaleMultiplierBy(sender: TObject; amount: integer);
    { resizing }
    procedure resizePanelsToVerticalSplitter;
    procedure resizePanelsToHorizontalSplitter;
    procedure resizePlantListPanel;
    procedure resizePlantFocusPanel;
    procedure resizeDrawingBitmapIfNecessary;
    { splitting }
    function drawHorizontalSplitterLine(pos: integer): integer;
    function drawVerticalSplitterLine(pos: integer): integer;
    procedure undrawHorizontalSplitterLine;
    procedure undrawVerticalSplitterLine;
    { palette stuff }
		function GetPalette: HPALETTE; override;
		function PaletteChanged(Foreground: Boolean): Boolean; override;
    { animation }
    procedure startAnimation;
    procedure stopAnimation;
    procedure enableOrDisableAllForms(enable: boolean);
    { export }
    function getBitmapCopySavePrintOptions(copySavePrintType: smallint): integer;
    function getNozzleOptions: integer;
    procedure fillBitmapForPainterNozzle(bitmapForExport: TBitmap);
    function getAnimationOptions: integer;
    procedure writeAnimationFilesWithFileSpec(startFileName: string);
    procedure showWelcomeForm;
    // plant bitmaps
    function screenBytesPerPixel: single;
    function bytesInPlantBitmaps(plantToExclude: PdPlant): longint;
    function roomForPlantBitmap(plant: PdPlant; bytesForThisPlant: longint): boolean;
    procedure exceptionResizingPlantBitmap;
    procedure updateForChangeToPlantBitmaps;
    procedure stopUsingPlantBitmaps;
    procedure startUsingPlantBitmaps;
    procedure updateFileMenuForOtherRecentFiles; // v1.60
    procedure loadPlantFileAtStartup;
    procedure ExportToGeneric3DType(outputType: smallint);
    function enoughRoomToSaveFile(tempFileName, fileDescriptor: string; fileSizeNeeded_MB: single): boolean; //v2.1
    function checkForUnregisteredExportCountOverMaxReturnTrueIfAbort: boolean;
    procedure incrementUnregisteredExportCount;
    end;

var
  MainForm: TMainForm;

implementation

{$R *.DFM}

uses ClipBrd, Printers, Jpeg,
  ucursor, uoptions, updcom, umath, usplash, uparams, uplantmn,
  upp_boo, upp_col, upp_int, upp_lis, upp_rea, upp_scv, upp_tdo, upp_hed, ubreedr, uwait, umover,
  uturtle, utimeser, uwizard, udebug, ubmpopt, utdomove, uwelcome, unozzle, uanimate,
  uabout, uregister, ucustdrw, unoted, ShellAPI, uoptions3dexport, uamendmt, uundo, ubmpsupport;

const
  kBetweenGap = 4;
  kSplitterDragToTopMinPixels = 100;
  kSplitterDragToBottomMinPixelsInHorizMode = 160; kSplitterDragToBottomMinPixelsInVertMode = 60;
  kSplitterDragToLeftMinPixels = 100;
  kSplitterDragToRightMinPixels = 260;
  kPlantListChanged = true; kPlantListNotChanged = false;
  kHintRange = 1;
  kMaxHintRangeForLargeAreas = 50; {in each direction, so box is 100 x 100}
  kTabRotations = 0; kTabParameters = 1; kTabLifeCycle = 2; kTabPosing = 3; kTabStatistics = 4; kTabNote = 5; kTabHighest = 5;
  kMaxMagnificationToTypeIn = 10000;
  kEnableAllForms = true; kDisableAllForms = false;
  kDrawAllPlants = true; kDrawOnlySelectedPlants = false;
  kExpand = 0; kCollapse = 1; kExpandOrCollapse = 2;

var 
  pictureFileSaveAttemptsThisSession: smallint;
  nozzleFileSaveAttemptsThisSession: smallint;
  exportTo3DFileSaveAttemptsThisSession: array[1..k3DExportTypeLast] of smallint;

procedure TMainForm.FormCreate(Sender: TObject);
  var
    tempBoundsRect: TRect;    
  begin
  cursor_startWait;
  try
  Application.helpFile := extractFilePath(application.exeName) + 'PlantStudio.hlp';
  Application.onActivate := self.FormActivate;
  if domain = nil then
    raise Exception.create('Problem: Nil domain in method TMainForm.FormCreate.');
  // domain must exist when this is created; use this pointer to shorten code
  plants := domain.plantManager.plants;
  self.updateForRegistrationChange;
  { turn off panel bevels }
  plantListPanel.bevelOuter := bvNone;
  plantFocusPanel.bevelOuter := bvNone;
  plantListDrawGrid.dragCursor := crDragPlant;
  { save height and width for resizing use }
  lastWidth := self.clientWidth;
  lastHeight := self.clientHeight;
  inFormCreation := true;
  { application options }
  Application.OnShowHint := DoShowHint;
  // cfk played with menu hints - to use menu hints, respond to this and display the hint in a window or status panel
  // Application.OnHint := DoMenuHint;    
  Application.showHint := true;
  { creation of dependent objects and setting them up }
  selectedPlants := TList.create;
  commandList := PdCommandList.create;
  commandList.setNewUndoLimit(Domain.options.undoLimit);
  commandList.setNewObjectUndoLimit(domain.options.undoLimitOfPlants);
  drawingPaintBox := PdPaintBoxWithPalette.create(self);
  with drawingPaintBox do
    begin
    parent := self;
    onPaint := self.drawingPaintBoxPaint;
    onMouseDown := self.PaintBoxMouseDown;
    onMouseMove := self.PaintBoxMouseMove;
    onMouseUp := self.PaintBoxMouseUp;
    onEndDrag := self.PaintBoxEndDrag;
    onDragOver := self.PaintBoxDragOver;
    dragCursor := crDragPlant;
    popupMenu := PlantPopupMenu;
    end;
  drawingBitmap := TBitmap.create;
  statsPanel := PdStatsPanel.create(self);
  statsPanel.parent := statsScrollBox;
  statsPanel.parentFont := false;
  { hints }
  hintActive := false;
  lastHintString := '';
  { intial settings of stored info }
  tabSet.tabIndex := kTabRotations;
  dragCursorMode.down := true;
  { loading info }
  self.loadSectionsIntoListBox;
  { updating }
  case domain.options.drawSpeed of
    kDrawFast: MenuOptionsFastDraw.checked := true;
    kDrawMedium: MenuOptionsMediumDraw.checked := true;
    kDrawBest: MenuOptionsBestDraw.checked := true;
    kDrawCustom: MenuOptionsCustomDraw.checked := true;
    end;
  self.updateMenusForUndoRedo;
  self.updatePasteMenuForClipboardContents;
  if sectionsComboBox.items.count > 0 then
    begin
    sectionsComboBox.itemIndex := 0;
    self.updateParameterPanelsForSectionChange;
    end;
  rotationsPanel.visible := true; //v2.0
  setPixelFormatBasedOnScreenForBitmap(drawingBitmap);
  { set size and splitters as saved in domain }
  { keep window on screen - left corner of title bar }
  tempBoundsRect := domain.mainWindowRect;
  with tempBoundsRect do
    if (left <> 0) or (right <> 0) or (top <> 0) or (bottom <> 0) then
      begin
      if left > screen.width - kMinWidthOnScreen then left := screen.width - kMinWidthOnScreen;
      if top > screen.height - kMinHeightOnScreen then top := screen.height - kMinHeightOnScreen;
      self.setBounds(left, top, right, bottom);
      end;
  if domain.horizontalSplitterPos > 0 then
    horizontalSplitter.top := domain.horizontalSplitterPos
  else
    horizontalSplitter.top := self.clientHeight div 2;
  if domain.verticalSplitterPos > 0 then
    verticalSplitter.left := domain.verticalSplitterPos
  else
    verticalSplitter.left := self.clientWidth div 3;
  finally
    cursor_stopWait;
  end;
  end;

procedure TMainForm.loadPlantFileAtStartup;
  begin
  cursor_startWait;
  try
  { if file loaded at startup, update for it, else act as if they picked new }
  if domain.plantFileLoaded then
    begin
    startWaitMessage('Drawing...');
    try
      self.updateForPlantFile;
    finally
      stopWaitMessage;
    end;
    end
  else
    self.MenuFileNewClick(self);
  if splashForm <> nil then splashForm.hide;
  self.updateForChangeToDomainOptions;
  self.updateFileMenuForOtherRecentFiles;
  self.selectedPlantPartID := -1;
  inFormCreation := false;
  finally
    cursor_stopWait;
  end;
  end;

procedure TMainForm.FormActivate(Sender: TObject);
  begin
  if Application.terminated then exit;
  MenuEditPasteAsText.enabled := (Clipboard.hasFormat(CF_TEXT)) and (domain.plantFileLoaded);
  end;

procedure TMainForm.showWelcomeForm;
  var
    welcomeForm: TWelcomeForm;
  begin
  if domain.options.hideWelcomeForm then exit;
  welcomeForm := TWelcomeForm.create(Application);
  try
    if welcomeForm.showModal <> mrCancel then
      begin
      case welcomeForm.whatToDo of
        kReadSuperSpeedTour: Application.helpJump('Super-Speed_Tour');
        kReadTutorial: Application.helpJump('Tutorial');
        kMakeNewPlant: self.MenuPlantNewClick(self);
        kOpenPlantLibrary:
          begin
          if domain.plantFileName = '' then
            domain.plantFileName := ExtractFilePath(Application.exeName);
          self.MenuFileOpenClick(self);
          end;
        kStartUsingProgram: ;
        end;
      end;
    domain.options.hideWelcomeForm := welcomeForm.hideWelcomeForm.checked;
  finally
    welcomeForm.free;
    welcomeForm := nil;
  end;
  end;

procedure TMainForm.FormDestroy(Sender: TObject);
  begin
  commandList.free;
  commandList := nil;
  drawingBitmap.free;
  drawingBitmap := nil;
  selectedPlants.free;                                       
  selectedPlants := nil;
  { don't free statsPanel because we are the owner }
  end;

{ ------------------------------------------------------------------------- *file menu }
procedure TMainForm.MenuFileNewClick(Sender: TObject);
  begin
	if not self.askForSaveAndProceed then exit;
  domain.resetForNoPlantFile;
  self.updateForNoPlantFile;
  domain.resetForEmptyPlantFile;
  self.updateForPlantFile;
  // new v1.4 reset to 100% magnification on new file
  magnificationPercent.text := '100%';
  self.changeMagnificationWithoutClick;
  end;

procedure TMainForm.WMDropFiles(var Msg: TWMDropFiles);
  var
    CFileName: array[0..MAX_PATH] of Char;
  begin
  try
    if DragQueryFile(Msg.Drop, 0, CFileName, MAX_PATH) > 0 then
    begin
      if pos('.PLA', upperCase(CFileName)) <= 0 then exit;
	    if not self.askForSaveAndProceed then exit;
      self.openFile(CFileName);
      Msg.Result := 0;
    end;
  finally
    DragFinish(Msg.Drop);
  end;
  end;

procedure TMainForm.MenuFileOpenClick(Sender: TObject);
	var
    fileNameWithPath: string;
	begin
	if not self.askForSaveAndProceed then exit;
  fileNameWithPath := getFileOpenInfo(kFileTypePlant, domain.plantFileName, 'Choose a plant file');
  if fileNameWithPath = '' then exit;
  self.openFile(fileNameWithPath);
  end;

procedure TMainForm.openFile(fileNameWithPath: string);
  begin
  domain.resetForNoPlantFile;
  self.updateForNoPlantFile;
  try
    self.inFileOpen := true;
    try
      startWaitMessage('Opening ' + extractFileName(fileNameWithPath));
  	  Domain.load(fileNameWithPath);
    except
      on E: Exception do
        begin
        stopWaitMessage;
  		  ShowMessage(E.message);
  		  ShowMessage('Could not load file ' + fileNameWithPath);
    	  exit;
        end;
	  end;
    self.updateForPlantFile;
    stopWaitMessage;
  finally
    self.inFileOpen := false;
  end;
	end;

procedure TMainForm.MenuFileCloseClick(Sender: TObject);
  begin
  if not self.askForSaveAndProceed then exit;
  domain.resetForNoPlantFile;
  self.updateForPlantFile;
  end;

function TMainForm.askForSaveAndProceed: boolean; // returns false if user canceled leaving
  var
    messageBoxResult: integer;
  begin
  result := true;
  if not plantFileChanged then exit;
  {cfk fix - put help context in - for all messageDlgs }
  messageBoxResult := MessageDlg('Save changes to ' + extractFileName(domain.plantFileName) + '?',
      mtConfirmation, mbYesNoCancel, 0);
  case messageBoxResult of
    IDCANCEL: result := false;
    IDYES:
    	begin
      self.MenuFileSaveClick(Self);
      result := self.lastSaveProceeded;
      end;
    IDNO: result := true;
    else
      begin
      ShowMessage('Error with save request dialog.');
      result := true;
      end;
    end;
  end;

procedure TMainForm.MenuFileSaveClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
  begin
  if pos(upperCase(kUnsavedFileName), upperCase(ExtractFileName(Domain.plantFileName))) > 0 then
    begin
    self.MenuFileSaveAsClick(self);
    exit;
    end;
  lastSaveProceeded := getFileSaveInfo(kFileTypePlant, kDontAskForFileName, Domain.plantFileName, fileInfo);
  if not lastSaveProceeded then exit;
  try
    startFileSave(fileInfo);
    startWaitMessage('Saving ' + extractFileName(fileInfo.newFile) + '...');
    Domain.save(fileInfo.tempFile);
    fileInfo.writingWasSuccessful := true;
  finally
    stopWaitMessage;
    cleanUpAfterFileSave(fileInfo);
    self.setPlantFileChanged(false);
    domain.updateRecentFileNames(fileInfo.newFile);
    self.clearCommandList;
  end;
	end;

procedure TMainForm.setPlantFileChanged(fileChanged: boolean);
  begin
  plantFileChanged := fileChanged;
  if plantFileChangedImage <> nil then
    begin
    if plantFileChanged then
      plantFileChangedImage.picture := fileChangedImage.picture
    else
      plantFileChangedImage.picture := fileNotChangedImage.picture;
    plantFileChangedImage.invalidate;
    plantFileChangedImage.refresh;
    end;
  end;

procedure TMainForm.MenuFileSaveAsClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
	begin
  lastSaveProceeded := getFileSaveInfo(kFileTypePlant, kAskForFileName, Domain.plantFileName, fileInfo);
  if not lastSaveProceeded then exit;
  try
    startFileSave(fileInfo);
    startWaitMessage('Saving ' + extractFileName(fileInfo.newFile) + '...');
    Domain.save(fileInfo.tempFile);
    fileInfo.writingWasSuccessful := true;
  finally
    stopWaitMessage;
    cleanUpAfterFileSave(fileInfo);
    self.setPlantFileChanged(false);
    self.clearCommandList;
  end;
  Domain.plantFileName := fileInfo.newFile;
  Domain.lastOpenedPlantFileName := Domain.plantFileName;
  domain.updateRecentFileNames(Domain.lastOpenedPlantFileName);
  self.caption := self.captionForFile;
	end;

procedure TMainForm.MenuFilePlantMoverClick(Sender: TObject);
  var
  	mover: TMoverForm;
    response: integer;
  begin
  if plantFileChanged then
    begin
    response := MessageDlg('Do you want to save your changes to '
        + extractFileName(domain.plantFileName)
        + chr(13) + 'before you use the plant mover?',
        mtConfirmation, mbYesNoCancel, 0);
    case response of
      idCancel: exit;
      idYes: self.menuFileSaveClick(self);
      idNo: ;
      end;
    end;
  mover := TMoverForm.create(self);
  if mover = nil then
    raise Exception.create('Problem: Could not create plant mover window.');
  try
    mover.showModal;
    self.updatePasteMenuForClipboardContents; {in case mover copied something}
    if mover.changedCurrentPlantFile then
      begin
      if mover.untitledDomainFileSavedAs <> '' then
        domain.plantFileName := mover.untitledDomainFileSavedAs;
      { cfk fix put help context in }
      response := messageDlg('The current plant file has changed.' + chr(13)
          + 'Do you want to reload the changed file?',
          mtConfirmation, [mbYes, mbNo], 0);
      if response = idYes then
        begin
        try
          startWaitMessage('Opening ' + extractFileName(domain.plantFileName));
          self.updateForNoPlantFile;
  	      domain.load(domain.plantFileName);
        except
          on E: Exception do
            begin
            stopWaitMessage;
  		      ShowMessage(E.message);
  		      ShowMessage('Could not load file ' + domain.plantFileName + '.');
    	      exit;
            end;
	      end;
        self.updateForPlantFile;
        stopWaitMessage;
        end;
      end;
  finally
    mover.free;
    mover := nil;
  end;
  end;

procedure TMainForm.MenuFileTdoMoverClick(Sender: TObject);
  var
  	mover: TTdoMoverForm;
  begin
  mover := TTdoMoverForm.create(self);
  if mover = nil then
    raise Exception.create('Problem: Could not create 3D object mover window.');
  try
    mover.showModal;
  finally
    mover.free;
    mover := nil;
  end;
  end;

procedure TMainForm.WMQueryEndSession(var message: TWMQueryEndSession);
  begin
  inherited;
	if not self.askForSaveAndProceed then
    message.result := 0  // prevents windows from shutting down
  else if not self.cleanUpBeforeExit then
    message.result := 0;
  end;

procedure TMainForm.MenuFileExitClick(Sender: TObject);
  begin
	if not self.askForSaveAndProceed then
    exit
  else if not self.cleanUpBeforeExit then
    exit;
  Application.terminate;
  end;

procedure TMainForm.FormClose(Sender: TObject; var Action: TCloseAction);
  begin
  { same as exit, but can't call exit because we have to set the action flag }
	if not self.askForSaveAndProceed then
    action := caNone
  else if not self.cleanUpBeforeExit then
    action := caNone;
  end;

function TMainForm.cleanUpBeforeExit: boolean; // returns false if user cancels quit
  var
  	response: integer;
    okayToQuit: boolean;
    randomNumber, lowerLimit, upperLimit: extended;
  begin
  result := true;
  domain.mainWindowRect := rect(left, top, width, height);
  domain.horizontalSplitterPos := horizontalSplitter.top;
  domain.verticalSplitterPos := verticalSplitter.left;
  with BreederForm do
    domain.breederWindowRect := rect(left, top, width, height);
  with TimeSeriesForm do
    domain.timeSeriesWindowRect := rect(left, top, width, height);
  with DebugForm do
    domain.debugWindowRect := rect(left, top, width, height);
  if domain.useIniFile then
    begin
    okayToQuit := self.storeIniFile;
    if not okayToQuit then
      begin
      result := false;
      exit;
      end;
    end;
  lowerLimit := 1.0 / 24.0; // start putting up reminder after one hour
  if (not domain.registered) and (domain.accumulatedUnregisteredTime > lowerLimit) then
    begin
    Randomize;
    randomNumber := random;
    // v2 changed this - used to get to saturation after 24 hrs, changed to 12 - more reminding
    upperLimit := min(domain.accumulatedUnregisteredTime / (12.0 / 24.0), 0.9); // almost always after 12 hrs
    if (randomNumber < upperLimit) then
      begin
      aboutForm.initializeWithWhetherClosingProgram(true);
      response := aboutForm.showModal;
      self.updateForRegistrationChange;
      if response = mrCancel then
        begin
        result := false;
        exit;
        end;
      end;
    end;
  { have to clear out parameter panels before leaving, for some reason was making program crash
    but only if tdo components existed at the time of leaving the program. this works for now,
    but it would be better to understand why it was happening. }
  self.sectionsComboBox.itemIndex := -1;
  self.updateParameterPanelsForSectionChange;
  Application.helpCommand(HELP_QUIT, 0);
  end;

function TMainForm.storeIniFile: boolean;
  var
    fileSavedOK, choseAnotherFileName: boolean;
    buttonPressed: Word;
    saveDialog: TSaveDialog;
  begin
  result := true;
  fileSavedOK := false;
  choseAnotherFileName := false;
  while not fileSavedOK do
    begin
    try
      domain.storeProfileInformation;
      fileSavedOK := true;
    except
      fileSavedOK := false;
    end;
  	if not fileSavedOK then
    	begin
      buttonPressed := MessageDlg('Could not save settings to ' + chr(13) + chr(13)
        + '  ' + domain.iniFileName + chr(13) + chr(13)
        + 'Would you like to save them to another file?', mtError, mbYesNoCancel, 0);
      case buttonPressed of
        IDYES:
          begin
          saveDialog := TSaveDialog.create(application);
          try
            with saveDialog do
              begin
              fileName := domain.iniFileName;
              filter := 'Ini files (*.ini)|*.ini|All files (*.*)|*.*';
              defaultExt := 'ini';
              options := options + [ofPathMustExist, ofOverwritePrompt, ofHideReadOnly, ofNoReadOnlyReturn];
              end;
            result := saveDialog.execute;
            if result then
              begin
              domain.iniFileName := saveDialog.fileName;
              choseAnotherFileName := true;
              end;
          finally
            saveDialog.free;
          end;
          if not result then exit;
          end;
        IDNO: exit;
        IDCANCEL: begin result := false; exit; end;
        end;
    	end;
    end;
  if fileSavedOK and choseAnotherFileName then
    ShowMessage('Your settings have been saved in ' + chr(13) + chr(13)
        + '  ' + domain.iniFileName + chr(13) + chr(13)
        + 'But PlantStudio will load the original settings file again at startup.' + chr(13)
        + 'To use this settings file at startup, search in the help system' + chr(13)
        + 'for "alternate settings file".');
  end;

{ ---------------------------------------------------------------------------- *edit menu }
procedure TMainForm.MenuEditUndoClick(Sender: TObject);
  begin
  commandList.undoLast;
  { commands handle updating if it has to do with plant list, so only update drawing part here }
  self.updateForPossibleChangeToDrawing;
	end;

procedure TMainForm.UndoMenuEditUndoRedoListClick(Sender: TObject);
  var
  	undoRedoListForm: TUndoRedoListForm;
    response: integer;
    newCommand: PdCommand;
    i: integer;
  begin
  undoRedoListForm := TUndoRedoListForm.create(self);
  if undoRedoListForm = nil then
    raise Exception.create('Problem: Could not create undo/redo list window.');
  try
    undoRedoListForm.initializeWithCommandList(self.commandList);
    response := undoRedoListForm.showModal;
    if response = mrOK then
      try
        self.enableOrDisableAllForms(kDisableAllForms);
        startWaitMessage('Multiple undo/redo in progress; please wait...');
        if undoRedoListForm.undoToIndex >= 0 then
          begin
          for i := 0 to undoRedoListForm.undoToIndex do
            commandList.undoLast;
          end
        else if undoRedoListForm.redoToIndex >= 0 then
          begin
          for i := 0 to undoRedoListForm.redoToIndex do
            commandList.redoLast;
          end;
      finally
        self.updateForPossibleChangeToDrawing;
        stopWaitMessage;
        self.enableOrDisableAllForms(kEnableAllForms);
      end;
  finally
    undoRedoListForm.free;
  end;
  end;

procedure TMainForm.MenuEditRedoClick(Sender: TObject);
	begin
  commandList.redoLast;
  self.updateForPossibleChangeToDrawing;
	end;

procedure TMainForm.MenuEditCutClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdRemoveCommand.createWithListOfPlantsAndClipboardFlag(selectedPlants, kCopyToClipboard);
  self.doCommand(newCommand); {command calls copy, which enables paste menu item}
  end;

procedure TMainForm.MenuEditCopyClick(Sender: TObject);
  begin
  self.copySelectedPlantsToClipboard;
  end;

procedure TMainForm.MenuEditCopyAsTextClick(Sender: TObject);
  var
    i: integer;
    plant: PdPlant;
  begin
  if selectedPlants.count > 0 then
    begin
    Clipboard.clear;
    plantsAsTextMemo.clear;
    for i := 0 to selectedPlants.count - 1 do
      begin
      plant := PdPlant(selectedPlants.items[i]);
      if plant = nil then continue;
      plant.writeToMainFormMemoAsText;
      end;
    plantsAsTextMemo.selectAll;
    plantsAsTextMemo.cutToClipboard;
    end;
  end;

procedure TMainForm.MenuEditPasteAsTextClick(Sender: TObject);
  var
    fakeTextFile: TextFile;
    plant: PdPlant;
    newPlants: TList;
    newCommand: PdCommand;
    aLine, secondLine, plantName: string;
    i, startLine, endLine: smallint;
  begin
  newPlants := nil;
  if not Clipboard.hasFormat(CF_TEXT) then
    begin
    MessageDlg('The clipboard has no text in it.', mtError, [mbOK], 0);
    exit;
    end;
  plantsAsTextMemo.clear;
  plantsAsTextMemo.pasteFromClipboard;
  if plantsAsTextMemo.lines.count <= 0 then
    begin
    MessageDlg('The clipboard has no text in it.', mtError, [mbOK], 0);
    exit;
    end;
  startLine := -1;
  endLine := -1;
  for i := 0 to plantsAsTextMemo.lines.count - 1 do
    if pos(kPlantAsTextStartString, plantsAsTextMemo.lines.strings[i]) > 0 then
      begin
      startLine := i;
      break;
      end;
  for i := plantsAsTextMemo.lines.count - 1 downto 0 do
    if pos(kPlantAsTextEndString, plantsAsTextMemo.lines.strings[i]) > 0 then
      begin
      endLine := i;
      break;
      end;
  if startLine < 0 then
    begin
    plantsAsTextMemo.clear;
    MessageDlg('The clipboard has text in it, but no plants.' + chr(13) + chr(13)
      + 'I can''t find a starting line for a plant text description.' + chr(13)
      + 'It should have "' + kPlantAsTextStartString + '" in it.' + chr(13) + chr(13)
      + 'If you copied the text for a plant,' + chr(13)
      +  'make sure the first line is selected and copy it again.', mtError, [mbOK], 0);
    exit;
    end;
  if endLine < 0 then
    begin
    plantsAsTextMemo.clear;
    MessageDlg('The clipboard has text in it, but no plants.' + chr(13) + chr(13)
      + 'I can''t find an ending line for a plant text description.' + chr(13)
      + 'It should have "' + kPlantAsTextEndString + '" in it.' + chr(13) + chr(13)
      + 'If you copied the text for a plant,' + chr(13)
      + 'make sure the whole plant is selected and copy it again.', mtError, [mbOK], 0);
    exit;
    end;
  newPlants := TList.create;
  try
  i := startLine;   // since startLine and endLine are comments, we can read them
  while i <= endLine do
    begin
    aLine := plantsAsTextMemo.lines.strings[i];
    inc(i);
    if trim(aLine) = '' then continue;    // v1.60final ignore blank lines
    if pos(';', aLine) = 1 then continue;
    if pos('[', aLine) = 1 then
      begin
      checkVersionNumberInPlantNameLine(aLine);
      plant := PdPlant.create;
      plantName := stringBeyond(aLine, '[');
      plantName := stringUpTo(plantName, ']');
      plant.setName(plantName + ' from text');
      domain.parameterManager.setAllReadFlagsToFalse;
      plant.readingFromMemo := true;
      try
        // v1.60final fixed cutting off plant at blank line (was changed in file read in v1.3)
        while (pos(kPlantAsTextEndString, aLine) <= 0) and (i <= endLine) do // aLine <> '' do
          begin
          aLine := plantsAsTextMemo.lines.strings[i];
          inc(i);
          if pos(';', aLine) = 1 then continue;
          if trim(aLine) = '' then continue;
          // added v1.6b1 to accommodate paste from text with note
          if pos(upperCase(kStartNoteString), upperCase(aLine)) > 0 then
            begin
            plant.noteLines.clear;
            while i <= plantsAsTextMemo.lines.count - 1 do
              begin
              aLine := plantsAsTextMemo.lines.strings[i];
              inc(i);
              if (pos(upperCase(kEndNoteString), upperCase(aLine)) > 0) and (plant.noteLines.count < 5000) then
                break
              else if pos(';', aLine) = 1 then
                continue
              else
                plant.noteLines.add(aLine);
              end;
            end;
          // end added v1.6b1
          plant.readingMemoLine := i;
          plant.readLineAndTdoFromPlantFile(aLine, fakeTextFile);
          if i <> plant.readingMemoLine then
            i := plant.readingMemoLine;
          end;
      finally
        plant.readingFromMemo := false;
        plant.readingMemoLine := -1;
      end;
      plant.finishLoadingOrDefaulting(kCheckForUnreadParams);
      // cfk change v1.3 make plant fit into 100x100 box with paste from text, because
      // the scale always seems to be way off from what is being used; this way it always
      // looks okay when it pastes
      with domain.options do
        plant.drawPreviewIntoCache(Point(pasteRectSize, pasteRectSize), kDontConsiderDomainScale, kDontDrawNow);
      newPlants.add(plant);
      end;
    end;
    newCommand := PdPasteCommand.createWithListOfPlantsAndOldSelectedList(newPlants, self.selectedPlants);
    self.doCommand(newCommand);
  finally
    {command has another list, so we need to free this one; command will free plants if paste is undone}
    newPlants.free;
  end;
  end;

function TMainForm.getBitmapCopySavePrintOptions(copySavePrintType: smallint): integer;
  var
    bitmapOptionsForm: TBitmapOptionsForm;
  begin
  result := mrCancel;
  bitmapOptionsForm := TBitmapOptionsForm.create(self);
  if bitmapOptionsForm = nil then
    raise Exception.create('Problem: Could not create copy/save/print options window.');
  try
    bitmapOptionsForm.initializeWithTypeAndOptions(copySavePrintType, domain.bitmapOptions);
    result := bitmapOptionsForm.showModal;
    domain.bitmapOptions := bitmapOptionsForm.options;
  finally
    bitmapOptionsForm.free;
  end;
  end;

procedure TMainForm.MenuEditCopyDrawingClick(Sender: TObject);
  var
    bitmapForExport: TBitmap;
  begin
  if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort then exit;
  if (domain = nil) or (domain.plantManager = nil) or (plants.count <= 0) then exit;
  if self.getBitmapCopySavePrintOptions(kCopyingDrawing) = mrOK then
    begin
    bitmapForExport := TBitmap.create;
    try
      self.fillBitmapForExport(bitmapForExport, domain.bitmapOptions);
      CopyBitmapToClipboard(bitmapForExport);
    finally
      bitmapForExport.free;
      if (not domain.registered) then self.incrementUnregisteredExportCount;
    end;
    end;
  end;

procedure TMainForm.MenuFileSaveDrawingAsClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
    bitmapForExport: TBitmap;
    suggestedFileName: string;
	begin
  if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort then exit;
  if (domain = nil) or (domain.plantManager = nil) or (plants.count <= 0) then exit;
  if self.getBitmapCopySavePrintOptions(kSavingDrawingToBmp) = mrCancel then exit;
  inc(pictureFileSaveAttemptsThisSession);
  suggestedFileName := 'picture' + intToStr(pictureFileSaveAttemptsThisSession) + '.bmp';
  if not getFileSaveInfo(kFileTypeBitmap, kAskForFileName, suggestedFileName, fileInfo) then exit;
  bitmapForExport := TBitmap.create;
  try
    startFileSave(fileInfo);
    startWaitMessage('Saving ' + extractFileName(fileInfo.newFile) + '...');
    self.fillBitmapForExport(bitmapForExport, domain.bitmapOptions);
    if not RequiresPalette(bitmapForExport) then
      begin
      bitmapForExport.releasePalette;
      bitmapForExport.ignorePalette := true;
      end;
    bitmapForExport.saveToFile(fileInfo.tempFile);
    fileInfo.writingWasSuccessful := true;
  finally
    bitmapForExport.free;
    stopWaitMessage;
    cleanUpAfterFileSave(fileInfo);
  end;
  end;

procedure TMainForm.MenuFileSaveJPEGClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
    bitmapForExport: TBitmap;
    jpegForExport: TJPEGImage;
    suggestedFileName: string;
	begin
  if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort then exit;
  if (domain = nil) or (domain.plantManager = nil) or (plants.count <= 0) then exit;
  if self.getBitmapCopySavePrintOptions(kSavingDrawingToJpeg) = mrCancel then exit;
  inc(pictureFileSaveAttemptsThisSession);
  suggestedFileName := 'picture' + intToStr(pictureFileSaveAttemptsThisSession) + '.jpg';
  if not getFileSaveInfo(kFileTypeJPEG, kAskForFileName, suggestedFileName, fileInfo) then exit;
  bitmapForExport := TBitmap.create;
  jpegForExport := TJPEGImage.create;
  try
    startFileSave(fileInfo);
    startWaitMessage('Saving ' + extractFileName(fileInfo.newFile) + '...');
    self.fillBitmapForExport(bitmapForExport, domain.bitmapOptions);
    if not RequiresPalette(bitmapForExport) then
      begin
      bitmapForExport.releasePalette;                  
      bitmapForExport.ignorePalette := true;
      end;
    jpegForExport.assign(bitmapForExport);
    jpegForExport.pixelFormat := jf24Bit; // no option here
    // we ask for compression, they want quality, so we switch here
    jpegForExport.compressionQuality := TJPEGQualityRange(100 - domain.bitmapOptions.jpegCompressionRatio);
    jpegForExport.saveToFile(fileInfo.tempFile);
    fileInfo.writingWasSuccessful := true;
  finally
    bitmapForExport.free;
    jpegForExport.free;
    stopWaitMessage;
    cleanUpAfterFileSave(fileInfo);
  end;
  end;

procedure TMainForm.MenuFilePrintDrawingClick(Sender: TObject);
  var
    printRect_pixels: TRect;
    bitmapForExport: TBitmap;
    xResolution_pixelsPerInch, yResolution_pixelsPerInch: single;
    printOffsetX_px, printOffsetY_px: integer;
  begin
  if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort then exit;
  if (domain = nil) or (domain.plantManager = nil) or (plants.count <= 0) then exit;
  if self.getBitmapCopySavePrintOptions(kPrintingDrawing) = mrCancel then exit;
  bitmapForExport := TBitmap.create;
  try
    with domain.bitmapOptions do
      begin
      self.fillBitmapForExport(bitmapForExport, domain.bitmapOptions);
      Printer.Title := 'PlantStudio Picture';
      Printer.beginDoc;
      xResolution_pixelsPerInch := GetDeviceCaps(Printer.Handle, LogPixelsX);
      yResolution_pixelsPerInch := GetDeviceCaps(Printer.Handle, LogPixelsY);
      with printRect_pixels do
        begin
        printOffsetX_px := GetDeviceCaps(Printer.Handle, PhysicalOffsetX);
        printOffsetY_px := GetDeviceCaps(Printer.Handle, PhysicalOffsetY);
        left := round(printLeftMargin_in * xResolution_pixelsPerInch) - printOffsetX_px;
        top := round(printTopMargin_in * yResolution_pixelsPerInch) - printOffsetY_px;
        right := left + round(printWidth_in * xResolution_pixelsPerInch);
        bottom := top + round(printHeight_in * yResolution_pixelsPerInch);
        end;
      inflateRect(printRect_pixels, -borderThickness, -borderThickness);
      PrintBitmap(bitmapForExport, printRect_pixels);
      // border
      with Printer.Canvas do
        begin
        brush.style := bsClear;
        if printBorderInner then
          begin
          pen.color := printBorderColorInner;
          pen.width := printBorderWidthInner;
          with printRect_pixels do
            rectangle(left, top, right, bottom);
          end;
        if printBorderOuter then
          begin
          pen.color := printBorderColorOuter;
          pen.width := printBorderWidthOuter;
          with printRect_pixels do
            rectangle(left - borderGap, top - borderGap, right + borderGap, bottom + borderGap);
          end;
        end;
      Printer.endDoc;
    end;
  finally
    bitmapForExport.free;
    if (not domain.registered) then self.incrementUnregisteredExportCount;
  end;
  end;

procedure TMainForm.copySelectedPlantsToClipboard;
  begin
  if selectedPlants.count <= 0 then exit;
  domain.plantManager.copyPlantsInListToPrivatePlantClipboard(selectedPlants);
  domain.plantManager.setCopiedFromMainWindowFlagInClipboardPlants;
  self.updatePasteMenuForClipboardContents;
  end;

procedure TMainForm.fillBitmapForExport(bitmapForExport: TBitmap; options: BitmapOptionsStructure);
  var
    combinedBoundsRect, rectToDrawIn, unregRect: TRect;
    xMultiplier, yMultiplier, scaleMultiplier: single;
    plantPartsToDraw: longint;
    plantsToDraw: TList;
    excludeInvisiblePlants, excludeNonSelectedPlants: boolean;
  begin
  if (bitmapForExport = nil) or (domain = nil) or (application.terminated) then exit;
  plantsToDraw := nil;
  // set up according to domain options
  with options do
    begin
    bitmapForExport.pixelFormat := colorType;
    excludeInvisiblePlants := true;
    excludeNonSelectedPlants := false;
    case exportType of
      kIncludeSelectedPlants:
        begin
        plantsToDraw := self.selectedPlants;
        excludeInvisiblePlants := true;
        excludeNonSelectedPlants := true;
        combinedBoundsRect := domain.plantManager.combinedPlantBoundsRects(self.selectedPlants,
            excludeInvisiblePlants, excludeNonSelectedPlants);
        end;
      kIncludeVisiblePlants:
        begin
        plantsToDraw := plants;
        excludeInvisiblePlants := true;
        excludeNonSelectedPlants := false;
        combinedBoundsRect := domain.plantManager.combinedPlantBoundsRects(self.selectedPlants,
            excludeInvisiblePlants, excludeNonSelectedPlants);
        end;
      kIncludeAllPlants:
        begin
        plantsToDraw := plants;
        excludeInvisiblePlants := false;
        excludeNonSelectedPlants := false;
        combinedBoundsRect := domain.plantManager.combinedPlantBoundsRects(self.selectedPlants,
            excludeInvisiblePlants, excludeNonSelectedPlants);
        end;
      kIncludeDrawingAreaContents:
        begin
        plantsToDraw := plants;
        excludeInvisiblePlants := true;
        excludeNonSelectedPlants := false;
        combinedBoundsRect := rect(0, 0, drawingBitmap.width, drawingBitmap.height);
        end;
      end;
    rectToDrawIn := rect(0, 0, width_pixels, height_pixels);
    end;
  if (plantsToDraw = nil) or (plantsToDraw.count <= 0) then exit;
  bitmapForExport.palette := CopyPalette(paletteImage.picture.bitmap.palette);
  xMultiplier := safedivExcept(1.0 * rWidth(rectToDrawIn), 1.0 * rWidth(combinedBoundsRect), 1.0);
  yMultiplier := safedivExcept(1.0 * rHeight(rectToDrawIn), 1.0 * rHeight(combinedBoundsRect), 1.0);
  scaleMultiplier := min(xMultiplier, yMultiplier);
  try
    cursor_startWait;
    resizeBitmap(bitmapForExport,
      Point(round(rWidth(combinedBoundsRect) * scaleMultiplier),
      round(rHeight(combinedBoundsRect) * scaleMultiplier)));
    domain.drawingToMakeCopyBitmap := true;
    domain.temporarilyHideSelectionRectangles := true;
    domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm := domain.plantDrawScale_PixelsPerMm
        * scaleMultiplier;
    domain.plantDrawOffsetWhenDrawingCopy_mm := domain.plantDrawOffset_mm;
    if options.exportType <> kIncludeDrawingAreaContents then
      begin
      domain.plantDrawOffsetWhenDrawingCopy_mm.x := domain.plantDrawOffsetWhenDrawingCopy_mm.x
        - safedivExcept(1.0 * combinedBoundsRect.left, domain.plantDrawScale_PixelsPerMm, 0);
      domain.plantDrawOffsetWhenDrawingCopy_mm.y := domain.plantDrawOffsetWhenDrawingCopy_mm.y
        - safedivExcept(1.0 * combinedBoundsRect.top, domain.plantDrawScale_PixelsPerMm, 0);
      end;
    fillBitmap(bitmapForExport, domain.options.backgroundColor);
    plantPartsToDraw := 0;
    if domain.options.showPlantDrawingProgress then
      plantPartsToDraw := Domain.plantManager.totalPlantPartCountInInvalidRect(plantsToDraw, combinedBoundsRect,
          excludeInvisiblePlants, excludeNonSelectedPlants);
    try
      drawing := true;
      if domain.options.showPlantDrawingProgress then
        self.startDrawProgress(plantPartsToDraw);
      // leave out openGL for now, put in later when you get bitmap drawing working
      domain.plantManager.drawOnInvalidRect(bitmapForExport.canvas, plantsToDraw, combinedBoundsRect,
          excludeInvisiblePlants, excludeNonSelectedPlants);
    finally
      drawing := false;
      if domain.options.showPlantDrawingProgress then
        self.finishDrawProgress;
    end;
    if not domain.registered then with unregisteredExportReminder do
      begin
      scaleMultiplier := max(1.0, scaleMultiplier);
      unregRect := Rect(1, 1, round(width * scaleMultiplier) + 1, round(height * scaleMultiplier) + 1);
      bitmapForExport.canvas.stretchDraw(unregRect, picture.bitmap);
      end;
  finally
    cursor_stopWait;
    domain.temporarilyHideSelectionRectangles := false;
    domain.drawingToMakeCopyBitmap := false;
    domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm := 1.0;
    domain.plantDrawOffsetWhenDrawingCopy_mm := setSinglePoint(0, 0);
  end;
  end;

procedure TMainForm.MenuEditPasteClick(Sender: TObject);
  begin
  self.pastePlantsFromClipboard;
  end;

procedure TMainForm.pastePlantsFromClipboard;
  var
    newPlants: TList;
    newCommand: PdCommand;
  begin
  newPlants := nil;
  if domain.plantManager.privatePlantClipboard.count <= 0 then exit;
  newPlants := TList.create;
  try
    domain.plantManager.pastePlantsFromPrivatePlantClipboardToList(newPlants);
    newCommand := PdPasteCommand.createWithListOfPlantsAndOldSelectedList(newPlants, self.selectedPlants);
    self.doCommand(newCommand);
  finally
    {command has another list, so we need to free this one; command will free plants if paste is undone}
    newPlants.free;
  end;
  end;

function TMainForm.standardPastePosition: TPoint;
  begin
  result := Point(drawingPaintBox.width div 2, 3 * drawingPaintBox.height div 4);
  end;

procedure TMainForm.MenuEditDeleteClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdRemoveCommand.createWithListOfPlantsAndClipboardFlag(selectedPlants, kDontCopyToClipboard);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuEditDuplicateClick(Sender: TObject);
  var
    newCommand: PdCommand;
	begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdDuplicateCommand.createWithListOfPlants(selectedPlants);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuEditPreferencesClick(Sender: TObject);
  var
  	optionsForm: TOptionsForm;
    response: integer;
    newCommand: PdCommand;
  begin
  optionsForm := TOptionsForm.create(self);
  if optionsForm = nil then
    raise Exception.create('Problem: Could not create preferences window.');
  try
    optionsForm.options := domain.options;
    response := optionsForm.showModal;
  if (response = mrOK) and (optionsForm.optionsChanged) then
    begin
    newCommand := PdChangeDomainOptionsCommand.createWithOptions(optionsForm.options);
    self.doCommand(newCommand);
    end;
  finally
    optionsForm.free;
    optionsForm := nil;
  end;
  end;

{ ---------------------------------------------------------------------------- *plant menu }
procedure TMainForm.MenuPlantNewClick(Sender: TObject);
  var
    newCommand: PdCommand;
    wizardForm: TWizardForm;
    response: integer;
    newPlantFromWizard: PdPlant;
  begin
  try
    cursor_startWait;
    // on slower computer wizard takes a long time to come up
    startWaitMessage('Starting the plant wizard...');
    wizardForm := TWizardForm.create(self);
  finally
    stopWaitMessage;
    cursor_stopWait;
  end;
  if wizardForm = nil then
    raise Exception.create('Problem: Could not create wizard window.');
  try
    response := wizardForm.showModal;
  if response = mrOK then
    begin
    if wizardForm.plant = nil then
      raise Exception.create('Problem: New wizard plant is nil.');
    newPlantFromWizard := PdPlant.create;
    wizardForm.plant.copyTo(newPlantFromWizard);
    newCommand := PdNewCommand.createWithWizardPlantAndOldSelectedList(newPlantFromWizard, self.selectedPlants);
    self.doCommand(newCommand);
    { command will free newPlantFromWizard }
    end;
  finally
    wizardForm.free;
    wizardForm := nil;
  end;
  end;

procedure TMainForm.MenuPlantNewUsingLastWizardSettingsClick(Sender: TObject);
  var
    newCommand: PdCommand;
    wizardForm: TWizardForm;
    newPlantFromWizard: PdPlant;
  begin
  // use wizard form to make a new plant using the current settings, but don't show the form
  // this is a sloppy way of doing this, but using the settings to set plant params is embedded in the form.
  try
    cursor_startWait;
    startWaitMessage('Making new plant...');
    wizardForm := TWizardForm.create(self);
  finally
    cursor_stopWait;
  end;
  newPlantFromWizard := PdPlant.create;
  try
    if wizardForm = nil then
      raise Exception.create('Problem: Could not create plant from last wizard settings.');
    if wizardForm.plant = nil then
      raise Exception.create('Problem: Could not create plant from last wizard settings (nil plant).');
    wizardForm.setPlantVariables;
    wizardForm.plant.copyTo(newPlantFromWizard);
    newPlantFromWizard.setAge(newPlantFromWizard.pGeneral.ageAtMaturity);
    newCommand := PdNewCommand.createWithWizardPlantAndOldSelectedList(newPlantFromWizard, self.selectedPlants);
    self.doCommand(newCommand);
    { command will free newPlantFromWizard }
  finally
    wizardForm.free;
    wizardForm := nil;
    stopWaitMessage;
  end;
  end;

procedure TMainForm.MenuPlantRenameClick(Sender: TObject);
  var
    newName: ansistring;
    response: Boolean;
    newCommand: PdCommand;
    plant: PdPlant;
  begin
  plant := self.focusedPlant;
  if plant = nil then exit;
  newName := plant.getName;
  response := inputQuery('Rename plant', 'Enter a new name for ' + plant.getName, newName);
  if response then
  	begin
    newCommand := PdRenameCommand.createWithPlantAndNewName(plant, newName);
    self.doCommand(newCommand);
    end;
  end;

procedure TMainForm.MenuPlantRandomizeClick(Sender: TObject);
  var
    newCommand: PdCommand;
	begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdRandomizeCommand.createWithListOfPlants(selectedPlants);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuPlantZeroRotationsClick(Sender: TObject);
	begin
  self.resetRotationsClick(self);
  end;

procedure TMainForm.MenuPlantBreedClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  { check if there is room in the breeder - this command will make two new generations }
  if BreederForm.selectedRow >= domain.breedingAndTimeSeriesOptions.maxGenerations - 2 then
    BreederForm.fullWarning
  else
    begin
    newCommand := PdBreedFromParentsCommand.createWithInfo(BreederForm.generations,
      self.focusedPlant, self.firstUnFocusedPlant, -1,
      domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, kCreateFirstGeneration);
    self.doCommand(newCommand);
    end;
  end;

procedure TMainForm.MenuPlantMakeTimeSeriesClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdMakeTimeSeriesCommand.createWithNewPlant(self.focusedPlant);
  self.doCommand(newCommand);
  end;

function TMainForm.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort: boolean;
  begin
  result := false;
  if (domain.totalUnregisteredExportsAtThisMoment >= kMaxUnregExportsAllowed)
      and (domain.unregisteredExportCountThisSession >= kMaxUnregExportsPerSessionAfterMaxReached) then
    begin
    MessageDlg(
        'Thank you for evaluating PlantStudio!' + chr(13)
        + chr(13)
        + 'You have exported PlantStudio output at least '
            + intToStr(kMaxUnregExportsAllowed) + ' times' + chr(13)
        + 'since installing it for evaluation,'
            + ' and ' + intToStr(kMaxUnregExportsPerSessionAfterMaxReached) + ' times this session.' + chr(13)
        + chr(13)                                                          
        + 'To export more output without registering,' + chr(13)
        + 'simply close and restart the program.' + chr(13)
        + chr(13)
        + 'To remove this restriction, purchase a registration code,' + chr(13)
        + 'then enter it into the Help-Register window' + chr(13)
        + 'to register your copy of PlantStudio.' 
       , mtInformation, [mbOK], 0);
    result := true;
    self.MenuHelpRegisterClick(self);
    end;
  end;

procedure TMainForm.incrementUnregisteredExportCount;
  begin
  inc(domain.unregisteredExportCountThisSession);
  if domain.totalUnregisteredExportsAtThisMoment = kMaxUnregExportsAllowed then
    begin
    domain.unregisteredExportCountBeforeThisSession :=
        domain.unregisteredExportCountBeforeThisSession + domain.unregisteredExportCountThisSession;
    domain.unregisteredExportCountThisSession := 0;
    end;
  self.updateForChangedExportCount;
  end;

// v2.1 separated this out and added call in animation saving
// it is the same otherwise except for the padding
function TMainForm.enoughRoomToSaveFile(tempFileName, fileDescriptor: string; fileSizeNeeded_MB: single): boolean;
  var
    driveLetter: string;
    driveNumber: smallint;
    fileMegaBytesAvailable: single;
  begin
  result := true;
  driveLetter := upperCase(copy(ExtractFileDrive(tempFileName), 1, 1));
  driveNumber := ord(driveLetter[1]) - ord('A') + 1;
  fileMegaBytesAvailable := 1.0 * diskFree(driveNumber) / (1024 * 1024);
  // if there are too many bytes available, the integer wraps around and goes negative, so ignore this case
  if fileMegaBytesAvailable >= 0 then
    begin
    // pad size needed in case estimate is slightly off  // v2.1
    if fileMegaBytesAvailable < fileSizeNeeded_MB * 1.1 then
      begin
      showMessage('Not enough space to save ' + fileDescriptor + ' file(s) ('
        + digitValueString(fileSizeNeeded_MB) + ' MB needed, '
        + digitValueString(fileMegaBytesAvailable) + ' MB available).' + chr(13)
        + 'Choose another option or make more space available.');
      result := false;
      end;
    end;
  end;

procedure TMainForm.ExportToGeneric3DType(outputType: smallint);
  var
    fileInfo: SaveFileNamesStructure;
    optionsForm: TGeneric3DOptionsForm;
    tempOptions: FileExport3DOptionsStructure;
    response, fileType: smallint;
    suggestedFileName, fileDescriptor: string;
    optionsChanged, excludeInvisiblePlants, excludeNonSelectedPlants: boolean;
    newCommand: PdCommand;
  begin
  if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort then exit;
  response := mrCancel;
  optionsChanged := false;
  optionsForm := TGeneric3DOptionsForm.create(self);
  if optionsForm = nil then
    raise Exception.create('Problem: Could not create 3D export options window.');
  try
    optionsForm.outputType := outputType;
    optionsForm.rearrangeItemsForOutputType;
    optionsForm.options := domain.exportOptionsFor3D[outputType];
    response := optionsForm.showModal;
    tempOptions := optionsForm.options;
    optionsChanged := optionsForm.optionsChanged;
  finally
    optionsForm.free;
    optionsForm := nil;
  end;
  if response <> mrOK then exit;
  fileType := fileTypeFor3DExportType(outputType);
  fileDescriptor := nameStringForFileType(fileType);
  inc(exportTo3DFileSaveAttemptsThisSession[outputType]);
  suggestedFileName := 'plants' + intToStr(exportTo3DFileSaveAttemptsThisSession[outputType])
      + '.' + extensionForFileType(fileType);
  if not getFileSaveInfo(fileType, kAskForFileName, suggestedFileName, fileInfo) then
    begin
    if optionsChanged then
      begin
      if messageDlg(fileDescriptor + ' export stopped.' + chr(13) + chr(13)
        + 'Do you want to save the changes you made' + chr(13)
        + 'to the ' + fileDescriptor + ' export options?', mtConfirmation, [mbYes, mbNo], 0) = IDYES then
        begin
        newCommand := PdChangeDomain3DOptionsCommand.createWithOptionsAndType(tempOptions, outputType);
        self.doCommand(newCommand);
        end;
      end;
    exit;
    end;
  if not enoughRoomToSaveFile(fileInfo.tempFile, fileDescriptor, tempOptions.fileSize) then exit;
  if optionsChanged then
    begin
    newCommand := PdChangeDomain3DOptionsCommand.createWithOptionsAndType(tempOptions, outputType);
    self.doCommand(newCommand);
    end;
  try
    startFileSave(fileInfo);
    if outputType = kPOV then
      fileInfo.newFile := replacePunctuationWithUnderscores(stringUpTo(extractFileName(fileInfo.newFile), '.')) + '.inc';
    startWaitMessage('Saving ' + extractFileName(fileInfo.newFile) + '...');
    excludeInvisiblePlants := false;
    excludeNonSelectedPlants := false;
    case tempOptions.exportType of
      kIncludeSelectedPlants:
        begin
        excludeInvisiblePlants := true;
        excludeNonSelectedPlants := true;
        end;
      kIncludeVisiblePlants:
        excludeInvisiblePlants := true;
      end;
    domain.plantManager.write3DOutputFileToFileName(self.selectedPlants,
      excludeInvisiblePlants, excludeNonSelectedPlants, fileInfo.tempFile, outputType);
    fileInfo.writingWasSuccessful := true;
  finally
    stopWaitMessage;
    cleanUpAfterFileSave(fileInfo);
  end;
end;

procedure TMainForm.MenuPlantExportToDXFClick(Sender: TObject);
  begin
  self.ExportToGeneric3DType(kDXF);
  end;

procedure TMainForm.MenuPlantExportTo3DSClick(Sender: TObject);
  begin
  self.ExportToGeneric3DType(k3DS);
  end;

procedure TMainForm.MenuPlantExportToOBJClick(Sender: TObject);
  begin
  self.ExportToGeneric3DType(kOBJ);
  end;

procedure TMainForm.MenuPlantExportToPOVClick(Sender: TObject);
  begin
  self.ExportToGeneric3DType(kPOV);
  end;

procedure TMainForm.MenuPlantExportToVRMLClick(Sender: TObject);
  begin
  self.ExportToGeneric3DType(kVRML);
  end;

procedure TMainForm.MenuPlantExportToLWOClick(Sender: TObject);
  begin
  self.ExportToGeneric3DType(kLWO);
  end;

{ -------------------------------------------------------------------------- *layout menu }
procedure TMainForm.MenuLayoutSelectAllClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdSelectOrDeselectAllCommand.createWithListOfPlants(selectedPlants);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutDeselectClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdSelectOrDeselectAllCommand.createWithListOfPlants(selectedPlants);
  (newCommand as PdSelectOrDeselectAllCommand).deselect := true;
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuFileMakePainterNozzleClick(Sender: TObject);
  var
    fileInfo: SaveFileNamesStructure;
    bitmapForExport: TBitmap;
    suggestedFileName: string;
  begin
  if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort then exit;
  if (domain = nil) or (domain.plantManager = nil) or (plants.count <= 0) then exit;
  if self.getNozzleOptions = mrCancel then exit;
  if domain.nozzleOptions.cellCount <= 0 then exit;
  inc(nozzleFileSaveAttemptsThisSession);
  suggestedFileName := 'nozzle' + intToStr(nozzleFileSaveAttemptsThisSession) + ' ' +
    intToStr(domain.nozzleOptions.cellSize.x) + 'x' + intToStr(domain.nozzleOptions.cellSize.y)
    + 'x' + intToStr(domain.nozzleOptions.cellCount) + '.bmp';
  if not getFileSaveInfo(kFileTypeBitmap, kAskForFileName, suggestedFileName, fileInfo) then exit;
  bitmapForExport := TBitmap.create;
  try
    startFileSave(fileInfo);
    startWaitMessage('Saving ' + extractFileName(fileInfo.newFile) + '...');
    self.fillBitmapForPainterNozzle(bitmapForExport);
    bitmapForExport.saveToFile(fileInfo.tempFile);
    fileInfo.writingWasSuccessful := true;
  finally
    bitmapForExport.free;
    stopWaitMessage;
    cleanUpAfterFileSave(fileInfo);
  end;
  end;

function TMainForm.getNozzleOptions: integer;
  var
    nozzleOptionsForm: TNozzleOptionsForm;
  begin
  result := mrCancel;
  nozzleOptionsForm := TNozzleOptionsForm.create(self);
  if nozzleOptionsForm = nil then
    raise Exception.create('Problem: Could not create nozzle options window.');
  try
    nozzleOptionsForm.initializeWithOptions(domain.nozzleOptions);
    result := nozzleOptionsForm.showModal;
    domain.nozzleOptions := nozzleOptionsForm.options;
  finally
    nozzleOptionsForm.free;
  end;
  end;

procedure TMainForm.fillBitmapForPainterNozzle(bitmapForExport: TBitmap);
  var
    plantsToDraw: TList;
    oldBackgroundColor: TColorRef;
    i: smallint;
    plant: PdPlant;
    oldPlantScale, scaleMultiplier: single;
    scaledPlantSize: TPoint;
  begin
  if (bitmapForExport = nil) or (domain = nil) or (application.terminated) then exit;
  plantsToDraw := nil;
  oldBackgroundColor := domain.options.backgroundColor;
  with domain.nozzleOptions do
    begin
    bitmapForExport.pixelFormat := colorType;
    if exportType = kIncludeSelectedPlants then
      plantsToDraw := self.selectedPlants
    else
      plantsToDraw := self.plants;
    if (plantsToDraw = nil) or (plantsToDraw.count <= 0) then exit;
    try
      cursor_startWait;
      resizeBitmap(bitmapForExport, Point(round(cellSize.x * plantsToDraw.count), cellSize.y));
      scaleMultiplier := safedivExcept(1.0 * resolution_pixelsPerInch, 1.0 * Screen.pixelsPerInch, 1.0);
      // v1.4 changed 0.8 to 0.9 because fitting algorithm works better now
      scaleMultiplier := scaleMultiplier * 0.9; // extra margin to make sure plants fit
      domain.options.backgroundColor := domain.nozzleOptions.backgroundColor;
      fillBitmap(bitmapForExport, domain.nozzleOptions.backgroundColor);
      for i := 0 to plantsToDraw.count - 1 do
        begin
        plant := PdPlant(plantsToDraw.items[i]);
        scaledPlantSize := Point(round(rWidth(plant.boundsRect_pixels) * scaleMultiplier),
          round(rHeight(plant.boundsRect_pixels) * scaleMultiplier));
        oldPlantScale := plant.drawingScale_PixelsPerMm;
        try
          plant.fixedPreviewScale := false;  // v1.4
          plant.fixedDrawPosition := false;  // v1.4
          plant.drawPreviewIntoCache(scaledPlantSize, kDontConsiderDomainScale, kDrawNow);
          bitmapForExport.canvas.draw(i * cellSize.x, 0, plant.previewCache);
          plant.shrinkPreviewCache;
        finally
          plant.drawingScale_PixelsPerMm := oldPlantScale;
          plant.recalculateBounds(kDrawNow);
        end;
        end;
    finally
      cursor_stopWait;
      domain.options.backgroundColor := oldBackgroundColor;
    end;
    end;
  end;

procedure TMainForm.MenuFileMakePainterAnimationClick(Sender: TObject);
  var
    saveDialog: TSaveDialog;
    sizeNeeded_MB: single;
  begin
  if self.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort then exit;
  if (domain = nil) or (domain.plantManager = nil) or (plants.count <= 0) then exit;
  if focusedPlant = nil then exit;
  if self.getAnimationOptions = mrCancel then exit;
  if domain.animationOptions.frameCount <= 0 then exit;
  saveDialog := TSaveDialog.create(application);
  try
    with saveDialog do
      begin
      title := 'Choose a file name (numbers will be added)';
      fileName := focusedPlant.getName + '.bmp';
      filter := 'Bitmap files (*.bmp)|*.bmp';
      defaultExt := 'bmp';
      options := options + [ofPathMustExist, ofOverwritePrompt, ofHideReadOnly, ofNoReadOnlyReturn];
      end;
    if saveDialog.execute then
      begin
      sizeNeeded_MB := 1.0 * domain.animationOptions.fileSize / (1024 * 1024);
      if not enoughRoomToSaveFile(saveDialog.fileName, 'animation', sizeNeeded_MB) then exit;
      cursor_startWait;
      startWaitMessage('Starting...');
      try
        self.writeAnimationFilesWithFileSpec(stringUpTo(saveDialog.fileName, '.') + ' ');
      finally
        cursor_stopWait;
        stopWaitMessage;
      end;
      end;
  finally
    saveDialog.free;
  end;
  end;

procedure setPlantCharacteristicsForAnimationFrame(plant: PdPlant; frame: smallint);
  begin
  if plant = nil then exit;
  with domain.animationOptions do
    begin
    if animateBy = kAnimateByAge then
      begin
      if frame <= 0 then
        plant.setAge(1)
      else if frame >= frameCount - 1 then
        plant.setAge(plant.pGeneral.ageAtMaturity)
      else
        plant.setAge(ageIncrement * frame);
      end
    else if animateBy = kAnimateByXRotation then
      begin
      if frameCount > 1 then
        plant.xRotation := xRotationIncrement * frame;
      end;
    end;
  end;

procedure TMainForm.writeAnimationFilesWithFileSpec(startFileName: string);
  var
    plant: PdPlant;
    oldXRotation, scaleMultiplier, minScale, oldScale: single;
    oldAge, i: smallint;
    saveFileName: string;
    unregRect: TRect;
    bestPosition: TPoint;
    widestWidth, tallestHeight: longint;
  begin
  if focusedPlant = nil then exit;
  plant := focusedPlant;
  oldXRotation := plant.xRotation;
  oldAge := plant.age;
  oldScale := plant.drawingScale_PixelsPerMm;
  with domain.animationOptions do
  try
    plant.previewCache.pixelFormat := colorType;
    // draw plant for all frames, get min drawing scale
    plant.fixedPreviewScale := false;
    plant.fixedDrawPosition := false;
    minScale := 0;
    for i := 0 to frameCount - 1 do
      begin
      setPlantCharacteristicsForAnimationFrame(plant, i);
      plant.drawPreviewIntoCache(scaledSize, kDontConsiderDomainScale, kDontDrawNow);
      if (i = 1) or (plant.drawingScale_PixelsPerMm < minScale) then
          minScale := plant.drawingScale_PixelsPerMm;
      end;
    // draw plant for all frames, get common draw position
    plant.drawingScale_PixelsPerMm := minScale;
    plant.fixedPreviewScale := true;
    widestWidth := 0;
    tallestHeight := 0;
    for i := 0 to frameCount - 1 do
      begin
      setPlantCharacteristicsForAnimationFrame(plant, i);
      plant.drawPreviewIntoCache(scaledSize, kDontConsiderDomainScale, kDontDrawNow);
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
    // now really draw
    plant.drawPositionIfFixed := bestPosition;
    plant.fixedDrawPosition := true;
    for i := 0 to frameCount - 1 do
      begin
      saveFileName := startFileName;
      if i+1 < 100 then saveFileName := saveFileName + '0';
      if i+1 < 10 then saveFileName := saveFileName + '0';
      saveFileName := saveFileName + intToStr(i+1) + '.bmp';
      startWaitMessage('Saving ' + extractFileName(saveFileName) + '...');
      setPlantCharacteristicsForAnimationFrame(plant, i);
      plant.drawPreviewIntoCache(scaledSize, kDontConsiderDomainScale, kDrawNow);
      if not domain.registered then with unregisteredExportReminder do
        begin
        scaleMultiplier := safedivExcept(1.0 * resolution_pixelsPerInch, 1.0 * Screen.pixelsPerInch, 1.0);
        scaleMultiplier := max(1.0, scaleMultiplier);
        unregRect := Rect(1, 1, round(width * scaleMultiplier) + 1, round(height * scaleMultiplier) + 1);
        plant.previewCache.canvas.stretchDraw(unregRect, picture.bitmap);
        end;
      plant.previewCache.saveToFile(saveFileName);
    end;
    // clean up for next time
    plant.fixedPreviewScale := false;
    plant.fixedDrawPosition := false;
  finally
    plant.shrinkPreviewCache;
    plant.fixedPreviewScale := false;
    plant.xRotation := oldXRotation;
    plant.drawingScale_PixelsPerMm := oldScale;
    plant.setAge(oldAge);
    plant.recalculateBounds(kDrawNow);
  end;
  end;

function TMainForm.getAnimationOptions: integer;
  var
    animationOptionsForm: TAnimationFilesOptionsForm;
  begin
  result := mrCancel;
  if focusedPlant = nil then exit;
  animationOptionsForm := TAnimationFilesOptionsForm.create(self);
  if animationOptionsForm = nil then
    raise Exception.create('Problem: Could not create animation options window.');
  try
    animationOptionsForm.initializeWithOptionsAndPlant(domain.animationOptions, focusedPlant);
    result := animationOptionsForm.showModal;
    domain.animationOptions := animationOptionsForm.options;
  finally
    animationOptionsForm.free;
  end;
  end;

procedure TMainForm.MenuLayoutShowClick(Sender: TObject);
  var
    newCommand: PdCommand;
    atLeastOnePlantIsHidden: boolean;
    i: smallint;
	begin
  if selectedPlants.count <= 0 then exit;
  { make sure at least one plant is hidden }
  atLeastOnePlantIsHidden := false;
  for i := 0 to selectedPlants.count - 1 do
    if PdPlant(selectedPlants.items[i]).hidden then
      begin
      atLeastOnePlantIsHidden := true;
      break;
      end;
  if not atLeastOnePlantIsHidden then exit;
  newCommand := PdHideOrShowCommand.createWithListOfPlantsAndHideOrShow(selectedPlants, kShow);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutHideClick(Sender: TObject);
  var
    newCommand: PdCommand;
    atLeastOnePlantIsShowing: boolean;
    i: smallint;
	begin
  if selectedPlants.count <= 0 then exit;
  { make sure at least one plant is showing }
  atLeastOnePlantIsShowing := false;
  for i := 0 to selectedPlants.count - 1 do
    if not PdPlant(selectedPlants.items[i]).hidden then
      begin
      atLeastOnePlantIsShowing := true;
      break;
      end;
  if not atLeastOnePlantIsShowing then exit;
  newCommand := PdHideOrShowCommand.createWithListOfPlantsAndHideOrShow(selectedPlants, kHide);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutHideOthersClick(Sender: TObject);
  var
    booleansList: TListCollection;
    newCommand: PdCommand;
    i: smallint;
    plant: PdPlant;
  begin
  if selectedPlants.count <= 0 then exit;
  booleansList := TListCollection.create;
  for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    booleansList.add(PdBooleanValue.createWithBoolean(not isSelected(plant)));
    end;
  try
    newCommand := PdHideOrShowCommand.createWithListOfPlantsAndListOfHides(plants, booleansList);
    self.doCommand(newCommand);
  finally
    booleansList.free;
  end;
  end;

procedure TMainForm.MenuLayoutMakeBouquetClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 1 then exit;
  newCommand := PdDragCommand.createWithListOfPlantsAndNewPoint(selectedPlants,
      self.focusedPlant.basePoint_pixels);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutScaleToFitClick(Sender: TObject);
  begin
  self.centerDrawingClick(self);
  end;

procedure TMainForm.changeViewingOptionTo(aNewOption: smallint);
  var
    newCommand: PdCommand;
  begin
  if (aNewOption = kViewPlantsInMainWindowOneAtATime) and (selectedPlants.count <= 0) then
    begin
    if plants.count < 0 then exit;
    self.selectedPlants.add(plants.items[0]);
    self.updateForChangeToPlantSelections;
    end;
  newCommand := PdChangeMainWindowViewingOptionCommand.createWithListOfPlantsAndSelectedPlantsAndNewOption(
      plants, self.selectedPlants, aNewOption);
  self.doCommand(newCommand);
  MenuLayoutMakeBouquet.enabled := (selectedPlants.count > 1) and (not domain.viewPlantsInMainWindowOnePlantAtATime);
  end;

procedure TMainForm.MenuLayoutViewOnePlantAtATimeClick(Sender: TObject);
  begin
  if domain.options.mainWindowViewMode <> kViewPlantsInMainWindowOneAtATime then
    self.changeViewingOptionTo(kViewPlantsInMainWindowOneAtATime);
  end;

procedure TMainForm.viewOneOnlyClick(Sender: TObject);
  begin
  self.MenuLayoutViewOnePlantAtATimeClick(self);
  end;

procedure TMainForm.MenuLayoutViewFreeFloatingClick(Sender: TObject);
  begin
  if domain.options.mainWindowViewMode <> kViewPlantsInMainWindowFreeFloating then
    self.changeViewingOptionTo(kViewPlantsInMainWindowFreeFloating);
  end;

procedure TMainForm.viewFreeFloatingClick(Sender: TObject);
  begin
  self.MenuLayoutViewFreeFloatingClick(self);
  end;

procedure TMainForm.MenuLayoutBringForwardClick(Sender: TObject);
  var
    newCommand: PdCommand;
	begin
  if selectedPlants.count <= 0 then exit;
  { don't do if you can't go forward any more }
  if plants.indexOf(firstSelectedPlantInList) <= 0 then exit;
  newCommand := PdSendBackwardOrForwardCommand.createWithBackwardOrForward(kBringForward);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutSendBackClick(Sender: TObject);
  var
    newCommand: PdCommand;
	begin
  if selectedPlants.count <= 0 then exit;
  { don't do if you can't go backward any more }
  if plants.indexOf(lastSelectedPlantInList) >= plants.count - 1 then exit;
  newCommand := PdSendBackwardOrForwardCommand.createWithBackwardOrForward(kSendBackward);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutHorizontalOrientationClick(Sender: TObject);
  var newCommand: PdCommand;
  begin
  if domain.options.mainWindowOrientation <> kMainWindowOrientationHorizontal then
    begin
    newCommand := PdChangeMainWindowOrientationCommand.createWithNewOrientation(kMainWindowOrientationHorizontal);
    self.doCommand(newCommand);
    end;
  end;

procedure TMainForm.MenuLayoutVerticalOrientationClick(Sender: TObject);
  var newCommand: PdCommand;
  begin
  if domain.options.mainWindowOrientation <> kMainWindowOrientationVertical then
    begin
    newCommand := PdChangeMainWindowOrientationCommand.createWithNewOrientation(kMainWindowOrientationVertical);
    self.doCommand(newCommand);
    end;
  end;

procedure TMainForm.drawingAreaOnTopClick(Sender: TObject);
  begin
  self.MenuLayoutHorizontalOrientationClick(self);
  end;

procedure TMainForm.drawingAreaOnSideClick(Sender: TObject);
  begin
  self.MenuLayoutVerticalOrientationClick(self);
  end;

{ --------------------------------------------------------------------------- *options menu }
procedure TMainForm.MenuOptionsFastDrawClick(Sender: TObject);
  var oldSpeed: smallint;
  begin
  oldSpeed := domain.options.drawSpeed;
  domain.options.drawSpeed := kDrawFast;
  MenuOptionsFastDraw.checked := true;
  BreederForm.BreederMenuOptionsFastDraw.checked := true;
  TimeSeriesForm.TimeSeriesMenuOptionsFastDraw.checked := true;
  if oldSpeed <> domain.options.drawSpeed then
    self.updateForChangeToDrawOptions;
  end;

procedure TMainForm.MenuOptionsMediumDrawClick(Sender: TObject);
  var oldSpeed: smallint;
  begin
  oldSpeed := domain.options.drawSpeed;
  domain.options.drawSpeed := kDrawMedium;
  MenuOptionsMediumDraw.checked := true;
  BreederForm.BreederMenuOptionsMediumDraw.checked := true;
  TimeSeriesForm.TimeSeriesMenuOptionsMediumDraw.checked := true;
  if oldSpeed <> domain.options.drawSpeed then
    self.updateForChangeToDrawOptions;
  end;

procedure TMainForm.MenuOptionsBestDrawClick(Sender: TObject);
  var oldSpeed: smallint;
  begin
  oldSpeed := domain.options.drawSpeed;
  domain.options.drawSpeed := kDrawBest;
  MenuOptionsBestDraw.checked := true;
  BreederForm.BreederMenuOptionsBestDraw.checked := true;
  TimeSeriesForm.TimeSeriesMenuOptionsBestDraw.checked := true;
  if oldSpeed <> domain.options.drawSpeed then
    self.updateForChangeToDrawOptions;
  end;

procedure TMainForm.MenuOptionsCustomDrawClick(Sender: TObject);
  var
    customDrawForm: TCustomDrawOptionsForm;
    newCommand: PdCommand;
    response: integer;
    lastDrawSpeed: smallint;
  begin
  lastDrawSpeed := domain.options.drawSpeed;
  domain.options.drawSpeed := kDrawCustom;
  MenuOptionsCustomDraw.checked := true;
  BreederForm.BreederMenuOptionsCustomDraw.checked := true;
  TimeSeriesForm.TimeSeriesMenuOptionsCustomDraw.checked := true;
  customDrawForm := TCustomDrawOptionsForm.create(self);
  if customDrawForm = nil then
    raise Exception.create('Problem: Could not create 3D object mover window.');
  try
    customDrawForm.options := domain.options;
    response := customDrawForm.showModal;
    newCommand := nil;
    if (response = mrOK) and (customDrawForm.optionsChanged) then
      begin
      newCommand := PdChangeDomainOptionsCommand.createWithOptions(customDrawForm.options);
      self.doCommand(newCommand);
      end
    else
      begin
      if lastDrawSpeed <> kDrawCustom then
        // escape just escapes changing options in dialog, not setting to custom, should still redraw
        // v1.4 change UNLESS it was custom before.
        self.updateForChangeToDrawOptions;
      end;
  finally
    customDrawForm.free;
    customDrawForm := nil;
  end;
  end;

procedure TMainForm.MenuOptionsUsePlantBitmapsClick(Sender: TObject);
  begin
  if domain.options.cachePlantBitmaps then
    self.stopUsingPlantBitmaps
  else
    self.startUsingPlantBitmaps;
  self.updateForChangeToPlantBitmaps;
  self.updateForPossibleChangeToDrawing;  
  end;

procedure TMainForm.plantBitmapsIndicatorImageClick(Sender: TObject);
  begin
  if (not domain.options.cachePlantBitmaps) and (MenuOptionsUsePlantBitmaps.enabled) then
    self.MenuOptionsUsePlantBitmapsClick(self);
  end;

procedure TMainForm.MenuOptionsShowSelectionRectanglesClick(Sender: TObject);
  begin
  MenuOptionsShowSelectionRectangles.checked := not MenuOptionsShowSelectionRectangles.checked;
  domain.options.showSelectionRectangle := MenuOptionsShowSelectionRectangles.checked;
  self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.MenuOptionsShowBoundsRectanglesClick(Sender: TObject);
  begin
  MenuOptionsShowBoundsRectangles.checked := not MenuOptionsShowBoundsRectangles.checked;
  domain.options.showBoundsRectangle := MenuOptionsShowBoundsRectangles.checked;
  self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.MenuOptionsGhostHiddenPartsClick(Sender: TObject);
  begin
  MenuOptionsGhostHiddenParts.checked := not MenuOptionsGhostHiddenParts.checked;
  domain.options.showGhostingForHiddenParts := MenuOptionsGhostHiddenParts.checked;
  internalChange := true;
  posingGhost.down := domain.options.showGhostingForHiddenParts;
  internalChange := false;
  self.redrawEverything; // cannot just redraw plants because bounds rects may have changed
  end;

procedure TMainForm.MenuOptionsHighlightPosedPartsClick(Sender: TObject);
  begin
  MenuOptionsHighlightPosedParts.checked := not MenuOptionsHighlightPosedParts.checked;
  domain.options.showHighlightingForNonHiddenPosedParts := MenuOptionsHighlightPosedParts.checked;
  internalChange := true;
  posingHighlight.down := domain.options.showHighlightingForNonHiddenPosedParts;
  internalChange := false;
  self.redrawAllPlantsInViewWithAmendments;
  end;

procedure TMainForm.MenuOptionsHidePosingClick(Sender: TObject);
  begin
  MenuOptionsHidePosing.checked := not MenuOptionsHidePosing.checked;
  domain.options.showPosingAtAll := not MenuOptionsHidePosing.checked;
  internalChange := true;
  posingNotShown.down := not domain.options.showPosingAtAll;
  internalChange := false;
  self.redrawEverything; // cannot just redraw plants because bounds rects may have changed
  end;

procedure TMainForm.posingHighlightClick(Sender: TObject);
  begin                                   
  if internalChange then exit;
  domain.options.showHighlightingForNonHiddenPosedParts := not domain.options.showHighlightingForNonHiddenPosedParts;
  MenuOptionsHighlightPosedParts.checked := domain.options.showHighlightingForNonHiddenPosedParts;
  posingHighlight.down := domain.options.showHighlightingForNonHiddenPosedParts;
  self.redrawAllPlantsInViewWithAmendments;
  end;
                                                                     
procedure TMainForm.posingGhostClick(Sender: TObject);
  begin
  if internalChange then exit;
  domain.options.showGhostingForHiddenParts := not domain.options.showGhostingForHiddenParts;
  MenuOptionsGhostHiddenParts.checked := domain.options.showGhostingForHiddenParts;
  posingGhost.down := domain.options.showGhostingForHiddenParts;
  self.redrawEverything; // cannot just redraw plants because bounds rects may have changed
  end;

procedure TMainForm.posingNotShownClick(Sender: TObject);
  begin
  if internalChange then exit;
  domain.options.showPosingAtAll := not domain.options.showPosingAtAll;
  MenuOptionsHidePosing.checked := not domain.options.showPosingAtAll;
  posingNotShown.down := not domain.options.showPosingAtAll;
  self.redrawEverything; // cannot just redraw plants because bounds rects may have changed
  end;

procedure TMainForm.MenuOptionsShowLongButtonHintsClick(Sender: TObject);
  begin
  MenuOptionsShowLongButtonHints.checked := not MenuOptionsShowLongButtonHints.checked;
  domain.options.showLongHintsForButtons := MenuOptionsShowLongButtonHints.checked;
  self.updateHintPauseForOptions;
  self.updateForChangeToPlantBitmaps; // shows different hint
  end;

procedure TMainForm.MenuOptionsShowParameterHintsClick(Sender: TObject);
  begin
  MenuOptionsShowParameterHints.checked := not MenuOptionsShowParameterHints.checked;
  domain.options.showHintsForParameters := MenuOptionsShowParameterHints.checked;
  self.updateHintPauseForOptions;
  end;

{ --------------------------------------------------------------------------- *window menu }
procedure TMainForm.MenuWindowBreederClick(Sender: TObject);
  begin
  BreederForm.show;
  BreederForm.bringToFront;
  if BreederForm.windowState = wsMinimized then BreederForm.windowState := wsNormal;
  end;

procedure TMainForm.MenuWindowTimeSeriesClick(Sender: TObject);
  begin
  TimeSeriesForm.show;
  TimeSeriesForm.bringToFront;
  if TimeSeriesForm.windowState = wsMinimized then TimeSeriesForm.windowState := wsNormal;
  end;

procedure TMainForm.MenuWindowNumericalExceptionsClick(Sender: TObject);
  begin
  DebugForm.show;
  DebugForm.bringToFront;
  if DebugForm.windowState = wsMinimized then DebugForm.windowState := wsNormal;
  end;

{ ---------------------------------------------------------------------------- *help menu }
procedure TMainForm.MenuHelpTopicsClick(Sender: TObject);
  begin
  application.helpCommand(HELP_FINDER, 0);
  end;

procedure TMainForm.MenuHelpAboutClick(Sender: TObject);
  begin
  if domain.registered then
    begin
    if splashForm = nil then exit;
    splashForm.showLoadingString('Registered to:');//domain.registrationName);
    splashForm.showCodeString(domain.registrationName);//domain.registrationCode);
    splashForm.close.visible := true;
    splashForm.supportButton.visible := true;
    splashForm.showModal;
    end
  else
    begin
    if aboutForm = nil then exit;
    aboutForm.initializeWithWhetherClosingProgram(false);
    aboutForm.showModal;
    self.updateForRegistrationChange;
    end;
  end;

procedure TMainForm.MenuHelpRegisterClick(Sender: TObject);
  begin
  RegistrationForm.showModal;
  self.updateForRegistrationChange;
  end;

procedure TMainForm.updateForRegistrationChange;
  begin
  MenuHelpRegister.visible := not domain.registered;
  AfterRegisterMenuSeparator.visible := not domain.registered;
  self.caption := self.captionForFile;
  end;

procedure TMainForm.MenuHelpSuperSpeedTourClick(Sender: TObject);
  begin
  application.helpJump('Super-Speed_Tour');  
  end;

procedure TMainForm.MenuHelpTutorialClick(Sender: TObject);
  begin
  application.helpJump('Tutorial');
  end;

{ ---------------------------------------------------------------------------- *progress showing }
procedure TMainForm.progressPaintBoxPaint(Sender: TObject);
  begin
  with progressPaintBox.canvas do
    begin
    brush.color := clBtnFace;
    pen.style := psClear;
    rectangle(0, 0, progressPaintBox.width, progressPaintBox.height);
    end;
  end;

procedure TMainForm.startDrawProgress(maximum: longint);
  begin
  drawProgressMax := maximum;
  progressPaintBox.invalidate;
  progressPaintBox.refresh;
  end;

const kProgressBarColor = clBlue;
procedure TMainForm.showDrawProgress(amount: longint);
  var
    progress: longint;
  begin
  if not drawing then exit;
  if (not animateTimer.enabled) and (not domain.options.showPlantDrawingProgress) then exit;
  if animateTimer.enabled then exit;
  if drawProgressMax <> 0 then
    progress := round((1.0 * progressPaintBox.width * amount) / (drawProgressMax * 1.0))
  else
    progress := 0;
  if progress > 0 then with progressPaintBox.canvas do
    begin
    brush.color := kProgressBarColor;
    pen.style := psClear;
    rectangle(0, 0, progress, progressPaintBox.height);
    end;
  end;

procedure TMainForm.finishDrawProgress;
  begin
  progressPaintBox.invalidate;
  progressPaintBox.refresh;
  end;

{ ---------------------------------------------------------------------------- *updating }
procedure TMainForm.updateForNoPlantFile;
  begin
  selectedPlants.clear;
  plantListDrawGrid.invalidate;
  self.clearCommandList;
  self.caption := self.captionForFile;
  self.updateRightSidePanelForFirstSelectedPlant;
  self.redrawEverything;
  self.updateMenusForChangedPlantFile;
  end;

procedure TMainForm.redrawEverything;
  begin
  self.recalculateAllPlantBoundsRects(kDrawNow);
  self.invalidateEntireDrawing;
  self.updateForPossibleChangeToDrawing;
  end;

function TMainForm.captionForFile: string;
  var numLeft: smallint;
  begin
  if (not domain.plantFileLoaded) or (domain.plantFileName = '') then
    result := Application.title + ' - no file'
  else
    begin
    result := Application.title + ' - ' + stringUpTo(ExtractFileName(domain.plantFileName), '.');
    if not domain.registered then
      begin
      // before pool runs out
      if domain.totalUnregisteredExportsAtThisMoment < kMaxUnregExportsAllowed then
        begin
        numLeft := intMax(0, kMaxUnregExportsAllowed - domain.totalUnregisteredExportsAtThisMoment);
        if numLeft = 1 then
          result := result + ' [unregistered - ' + intToStr(numLeft) + ' export left in evaluation]'
        else
          result := result + ' [unregistered - ' + intToStr(numLeft) + ' exports left in evaluation]';
        end
      else // after pool runs out, fixed number per session
        begin
        numLeft := intMax(0, kMaxUnregExportsPerSessionAfterMaxReached - domain.unregisteredExportCountThisSession);
        if numLeft <= 0 then
          result := result + ' [unregistered - NO exports left this session]'
        else if numLeft = 1 then
          result := result + ' [unregistered - ' + intToStr(numLeft) + ' export left this session]'
        else
          result := result + ' [unregistered - ' + intToStr(numLeft) + ' exports left this session]';
        end;
      end
    else if plants.count <= 0 then
      result := result + ' (no plants)'
    else if plants.count = 1 then
      result := result + ' (1 plant)'
    else
      result := result + ' (' + intToStr(plants.count) + ' plants)';
    end;
  end;

procedure TMainForm.updateForPlantFile;
  var
    plant: PdPlant;
    i: integer;
  begin
  internalChange := true;
  if not domain.plantFileLoaded then
    self.updateForNoPlantFile
  else
    begin
    self.caption := self.captionForFile;
    self.updateForChangeToPlantList;
    self.updateMenusForChangedPlantFile;
    selectedPlants.clear;
    magnificationPercent.text := intToStr(round(domain.plantDrawScale_PixelsPerMm * 100.0)) + '%';
    // v2.0 load and save window orientation (top or side)
    if domain.plantManager.mainWindowOrientation <> domain.options.mainWindowOrientation then
      begin
      domain.options.mainWindowOrientation := domain.plantManager.mainWindowOrientation;
      self.updateForChangeToOrientation;
      end;
    // v2.0 load and save plant hidden and selected flags
    if plants.count > 0 then
      begin
      for i := 0 to plants.count - 1 do
        begin
        plant := PdPlant(plants.items[i]);
        if plant.selectedWhenLastSaved then
          selectedPlants.add(plant);
        end;                               
      if selectedPlants.count <= 0 then
        selectedPlants.add(PdPlant(plants.items[0]));
      self.updateForChangeToPlantSelections;
      end;
    // deal with possibly changed viewing mode (one/many)
    if domain.viewPlantsInMainWindowOnePlantAtATime then
      self.showOnePlantExclusively(kDontDrawYet);
    viewOneOnly.down := domain.viewPlantsInMainWindowOnePlantAtATime;
    if domain.plantManager.fitInVisibleAreaForConcentrationChange then
      begin
      self.fitVisiblePlantsInDrawingArea(kDrawNow, kScaleAndMove, kAlwaysMove);
      domain.plantManager.fitInVisibleAreaForConcentrationChange := false;
      end
    else
      begin
      self.fitVisiblePlantsInDrawingArea(kDrawNow, kJustMove, kOnlyMoveIfOffTheScreen);
      self.redrawEverything;
      end;
    end;
  // v2.0 switch to select/drag mode - sometimes it seems to get broken - this will fix it - not unreasonable to do
  self.cursorModeForDrawing := kCursorModeSelectDrag;
  dragCursorMode.down := true;
  internalChange := false;
  end;

procedure TMainForm.updateHintPauseForOptions;
  begin
  Application.HintPause := longint(domain.options.pauseBeforeHint * 1000);
  if domain.options.showLongHintsForButtons or domain.options.showHintsForParameters then
    Application.HintHidePause := domain.options.pauseDuringHint * 1000
  else
    Application.HintHidePause := 2500;
  statsPanel.updateHint;
  end;

procedure TMainForm.updateForChangedExportCount;
  begin
  self.caption := self.captionForFile;
  end;

procedure TMainForm.updateForChangeToDomainOptions;
  begin
  internalChange := true;
  // fonts
  self.font.size := domain.options.parametersFontSize;  // v1.6b1 -- fix for large fonts problem
  parametersScrollBox.font.size := domain.options.parametersFontSize;
  parametersScrollBox.invalidate;
  // viewing option
  MenuLayoutMakeBouquet.enabled := (selectedPlants.count > 1) and (not domain.viewPlantsInMainWindowOnePlantAtATime);
  self.updateMenusForChangeToViewingOption;
  // drawing
  MenuOptionsUsePlantBitmaps.checked := domain.options.cachePlantBitmaps;
  // showing optional things
  MenuOptionsShowSelectionRectangles.checked := domain.options.showSelectionRectangle;
  MenuOptionsShowBoundsRectangles.checked := domain.options.showBoundsRectangle;
  MenuOptionsShowLongButtonHints.checked := domain.options.showLongHintsForButtons;
  MenuOptionsShowParameterHints.checked := domain.options.showHintsForParameters;
  // posing
  MenuOptionsGhostHiddenParts.checked := domain.options.showGhostingForHiddenParts;
  posingGhost.down := domain.options.showGhostingForHiddenParts;
  MenuOptionsHighlightPosedParts.checked := domain.options.showHighlightingForNonHiddenPosedParts;
  posingHighlight.down := domain.options.showHighlightingForNonHiddenPosedParts;
  MenuOptionsHidePosing.checked := not domain.options.showPosingAtAll;
  posingNotShown.down := not domain.options.showPosingAtAll;
  // vertical/horizontal
  MenuLayoutHorizontalOrientation.checked := domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal;
  MenuLayoutVerticalOrientation.checked := domain.options.mainWindowOrientation = kMainWindowOrientationVertical;
  drawingAreaOnTop.down := domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal;
  drawingAreaOnSide.down := domain.options.mainWindowOrientation = kMainWindowOrientationVertical;
  internalChange := false;
  // hint, undo
  self.updateHintPauseForOptions;
  commandList.setNewUndoLimit(domain.options.undoLimit);
  commandList.setNewObjectUndoLimit(domain.options.undoLimitOfPlants);
  if BreederForm <> nil then
    BreederForm.updateForChangeToDomainOptions;
  if TimeSeriesForm <> nil then
    TimeSeriesForm.updateForChangeToDomainOptions;
  if self.lifeCycleShowing then
    self.updateLifeCyclePanelForFirstSelectedPlant; {because max drawing scale might have changed}
  if not inFormCreation then
    self.redrawEverything;
  self.updateForChangeToPlantBitmaps; // in case max changed
  end;

procedure TMainForm.updateForChangeToDrawOptions;
  begin
  self.redrawEverything;
  if BreederForm <> nil then
    begin
    if (BreederForm.visible) and (BreederForm.windowState <> wsMinimized) then
      BreederForm.redrawPlants(kDontConsiderIfPreviewCacheIsUpToDate)
    else
      BreederForm.needToRedrawFromChangeToDrawOptions := true;
    end;
  if TimeSeriesForm <> nil then
    begin
    if (TimeSeriesForm.visible) and (TimeSeriesForm.windowState <> wsMinimized) then
      TimeSeriesForm.redrawPlants
    else
      TimeSeriesForm.needToRedrawFromChangeToDrawOptions := true;
    end;
  end;

procedure TMainForm.updateMenusForChangeToViewingOption;
  begin
  MenuLayoutViewOnePlantAtATime.checked := domain.viewPlantsInMainWindowOnePlantAtATime;
  MenuLayoutViewFreeFloating.checked := domain.viewPlantsInMainWindowFreeFloating;
  viewOneOnly.down := domain.viewPlantsInMainWindowOnePlantAtATime;
  viewFreeFloating.down := domain.viewPlantsInMainWindowFreeFloating;
  end;

procedure TMainForm.updateForChangeToOrientation;
  begin
  MenuLayoutHorizontalOrientation.checked := domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal;
  MenuLayoutVerticalOrientation.checked := domain.options.mainWindowOrientation = kMainWindowOrientationVertical;

  drawingAreaOnTop.down := domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal;
  drawingAreaOnSide.down := domain.options.mainWindowOrientation = kMainWindowOrientationVertical;
  self.resize;
  end;

procedure TMainForm.moveUpOrDownWithKeyInPlantList(indexAfterMove: smallint);
  var
    newList: TList;
    newCommand: PdCommand;
  begin
  { loop around }
  if indexAfterMove > plants.count - 1 then
    indexAfterMove := 0;
  if indexAfterMove < 0 then
    indexAfterMove := plants.count - 1;
  if (indexAfterMove >= 0) and (indexAfterMove <= plants.count - 1) then
    begin
    newList := TList.create;
    try
      newList.add(plants.items[indexAfterMove]);
      newCommand := PdChangeSelectedPlantsCommand.createWithOldListOfPlantsAndNewList(self.selectedPlants, newList);
      self.doCommand(newCommand);
    finally
      newList.free;
    end;
    end;
  end;

procedure TMainForm.updateForChangeToPlantSelections;
  begin
  if domain.options.showSelectionRectangle then
    self.copyDrawingBitmapToPaintBox;
  plantListDrawGrid.repaint;
  self.selectedPlantPartID := -1; // must be done BEFORE updating so it picks it up
  self.updateRightSidePanelForFirstSelectedPlant;
  self.updateMenusForChangedSelectedPlants;
  // reset for posing because posing works only on focused plant
  // don't do if reading file in
  if not internalChange then
    self.redrawAllPlantsInViewWithAmendments; // if change selected plant, must redraw to remove red color
  end;

procedure TMainForm.invalidateSelectedPlantRectangles;
  var
    i: smallint;
    plant: PdPlant;
  begin
  if selectedPlants.count > 0 then
    for i := 0 to selectedPlants.count - 1 do
      begin
      plant := PdPlant(selectedPlants.items[i]);
      if plant <> nil then
        self.invalidateDrawingRect(plant.boundsRect_pixels);
      end;
  end;

procedure TMainForm.updateForChangeToPlantList;
  var
    plant: PdPlant;
    i: smallint;
    plantsToRemove: TList;
	begin
  if Application.terminated then exit;
  if (domain = nil) or (domain.plantManager = nil) then exit;
  self.caption := self.captionForFile;
  plantListDrawGrid.rowCount := plants.count;
  plantListDrawGrid.invalidate;
  { selected plants list - make sure no pointers are invalid }
  plantsToRemove := TList.create;
  try
    if selectedPlants.count > 0 then for i := 0 to selectedPlants.count - 1 do
      begin
      plant := PdPlant(selectedPlants.items[i]);
      if plants.indexOf(plant) < 0 then
        plantsToRemove.add(plant);
      end;
    if plantsToRemove.count > 0 then for i := 0 to plantsToRemove.count - 1 do
      begin
      plant := PdPlant(plantsToRemove.items[i]);
      selectedPlants.remove(plant);
      end;
  finally
    plantsToRemove.free;
  end;
  if domain.viewPlantsInMainWindowOnePlantAtATime then
    self.showOnePlantExclusively(kDrawNow);
  self.updateRightSidePanelForFirstSelectedPlant;
  self.updateForPossibleChangeToDrawing;
  self.updateMenusForChangedPlantList;
  end;

procedure TMainForm.updateForPossibleChangeToDrawing;
  begin
  self.updateMenusForUndoRedo;
  with invalidDrawingRect do
    if (top <> 0) or (left <> 0) or (bottom <> 0) or (right <> 0) then
      self.paintDrawing(kDrawNow);
  end;

procedure TMainForm.recalculateAllPlantBoundsRects(drawNow: boolean);
  var
    i: smallint;
    plant: PdPlant;
    showProgress: boolean;
    plantPartsToDraw, partsDrawn: longint;
  begin
  if plants.count <= 0 then exit;
  plantPartsToDraw := 0;
  showProgress := drawNow and domain.options.cachePlantBitmaps and domain.options.showPlantDrawingProgress;
  if showProgress then
    plantPartsToDraw := Domain.plantManager.totalPlantPartCountInInvalidRect(plants,
      Rect(0, 0, drawingBitmap.width, drawingBitmap.height),
      kExcludeInvisiblePlants, kIncludeNonSelectedPlants);
  partsDrawn := 0;
  try
    cursor_startWait;
    drawing := true;
    if showProgress then self.startDrawProgress(plantPartsToDraw);
    for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      plant.plantPartsDrawnAtStart := partsDrawn;
      plant.recalculateBounds(drawNow);
      partsDrawn := partsDrawn + plant.totalPlantParts;
      end;
  finally
    cursor_stopWait;
    drawing := false;
    if showProgress then self.finishDrawProgress;
  end;
  end;

procedure TMainForm.recalculateSelectedPlantsBoundsRects(drawNow: boolean);
  var
    i: smallint;
    plant: PdPlant;
    showProgress: boolean;
    plantPartsToDraw, partsDrawn: longint;
  begin
  if selectedPlants.count <= 0 then exit;
  plantPartsToDraw := 0;
  showProgress := drawNow and domain.options.cachePlantBitmaps and domain.options.showPlantDrawingProgress;
  if showProgress then
    plantPartsToDraw := Domain.plantManager.totalPlantPartCountInInvalidRect(selectedPlants,
      Rect(0, 0, drawingBitmap.width, drawingBitmap.height),
      kExcludeInvisiblePlants, kIncludeNonSelectedPlants);
  partsDrawn := 0;
  try
    cursor_startWait;
    drawing := true;
    if showProgress then self.startDrawProgress(plantPartsToDraw);
    for i := 0 to selectedPlants.count - 1 do
      begin
      plant := PdPlant(selectedPlants.items[i]);
      plant.plantPartsDrawnAtStart := partsDrawn;
      plant.recalculateBounds(drawNow);
      partsDrawn := partsDrawn + plant.totalPlantParts;
      end;
  finally
    cursor_stopWait;
    drawing := false;
    if showProgress then self.finishDrawProgress;
  end;
  end;

procedure TMainForm.shrinkAllPlantBitmaps;
  var
    i: smallint;
  begin
  if plants.count > 0 then for i := 0 to plants.count - 1 do
    PdPlant(plants.items[i]).shrinkPreviewCache;
  self.updateForChangeToPlantBitmaps;
  end;

procedure TMainForm.recalculateAllPlantBoundsRectsForOffsetChange;
  var
    i: smallint;
    plant: PdPlant;
  begin
  for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    plant.recalculateBoundsForOffsetChange;
    end;
  end;

procedure TMainForm.updateForRenamingPlant(aPlant: PdPlant);
  var i: smallint;
  begin
  plantListDrawGrid.invalidate;
  for i := 0 to kTabHighest do self.updatePlantNameLabel(i);
  end;

procedure TMainForm.updateForChangeToPlantNote(aPlant: PdPlant);
  var start : integer;
  begin
  start := noteMemo.selStart;
  noteMemo.clear;
  if aPlant = nil then exit;
  internalChange := true;
  if self.focusedPlant <> nil then
    noteMemo.lines.addStrings(aPlant.noteLines);
  noteMemo.selStart := start;
  internalChange := false;
  end;

{ ---------------------------------------------------------------------------- *menu updating }
procedure TMainForm.updateMenusForUndoRedo;
	begin
  if commandList.isUndoEnabled then
  	begin
    MenuEditUndo.enabled := true;
    MenuEditUndo.caption := '&Undo ' + CommandList.undoDescription;
    end
  else
  	begin
    MenuEditUndo.enabled := false;
    MenuEditUndo.caption := 'Can''t undo';
    end;
  if commandList.isRedoEnabled then
  	begin
    MenuEditRedo.enabled := true;
    MenuEditRedo.caption := '&Redo ' + CommandList.redoDescription;
    end
  else
  	begin
    MenuEditRedo.enabled := false;
    MenuEditRedo.caption := 'Can''t redo';
    end;
  UndoMenuEditUndoRedoList.enabled := (commandList.isUndoEnabled) or (commandList.isRedoEnabled);
  if BreederForm <> nil then with BreederForm do
    begin
    BreederMenuUndo.enabled := MenuEditUndo.enabled;
    BreederMenuUndo.caption := MenuEditUndo.caption;
    BreederMenuRedo.enabled := MenuEditRedo.enabled;
    BreederMenuRedo.caption := MenuEditRedo.caption;
    BreederMenuUndoRedoList.enabled := UndoMenuEditUndoRedoList.enabled;
    end;
  if TimeSeriesForm <> nil then with TimeSeriesForm do
    begin
    TimeSeriesMenuUndo.enabled := MenuEditUndo.enabled;
    TimeSeriesMenuUndo.caption := MenuEditUndo.caption;
    TimeSeriesMenuRedo.enabled := MenuEditRedo.enabled;
    TimeSeriesMenuRedo.caption := MenuEditRedo.caption;
    TimeSeriesMenuUndoRedoList.enabled := UndoMenuEditUndoRedoList.enabled;
    end;
  end;

procedure TMainForm.updateMenusForChangedPlantFile;
  begin
  MenuFileClose.enabled := domain.plantFileLoaded;
  MenuPlantNew.enabled := domain.plantFileLoaded;
  MenuPlantNewUsingLastWizardSettings.enabled := domain.plantFileLoaded;
  MenuLayoutViewFreeFloating.enabled := domain.plantFileLoaded;
    viewFreeFloating.enabled := domain.plantFileLoaded;
  MenuLayoutViewOnePlantAtATime.enabled := domain.plantFileLoaded;
    viewOneOnly.enabled := domain.plantFileLoaded;
  MenuLayoutHorizontalOrientation.enabled := domain.plantFileLoaded;
    drawingAreaOnTop.enabled := domain.plantFileLoaded;
  MenuLayoutVerticalOrientation.enabled := domain.plantFileLoaded;
    drawingAreaOnSide.enabled := domain.plantFileLoaded;
  self.updateMenusForChangedPlantList;
  self.updatePasteMenuForClipboardContents;
  end;

procedure TMainForm.updateMenusForChangedPlantList;
  var
    havePlants: boolean;
  begin
  havePlants := (plants.count > 0);
  MenuFileSave.enabled := havePlants;
  MenuFileSaveAs.enabled := havePlants;
  MenuFileSaveDrawingAs.enabled := havePlants;
  MenuFilePrintDrawing.enabled := havePlants;
  MenuLayoutSelectAll.enabled := havePlants;
  MenuEditCopyDrawing.enabled := havePlants;
  MenuLayoutScaleToFit.enabled := havePlants;
  MenuFileMakePainterNozzle.enabled := havePlants;
  MenuPlantExportToDXF.enabled := havePlants;
  MenuPlantExportToPOV.enabled := havePlants;
  MenuPlantExportTo3DS.enabled := havePlants;
  MenuFileSaveJPEG.enabled := havePlants;
  MenuPlantExportToLWO.enabled := havePlants;
  MenuPlantExportToOBJ.enabled := havePlants;
  MenuPlantExportToVRML.enabled := havePlants;
  if not havePlants then
    self.dragCursorModeClick(self);
  toolbarPanel.enabled := havePlants;
  dragCursorMode.enabled := havePlants;
  magnifyCursorMode.enabled := havePlants;
  scrollCursorMode.enabled := havePlants;
  rotateCursorMode.enabled := havePlants;
  posingSelectionCursorMode.enabled := havePlants;
  centerDrawing.enabled := havePlants;
  magnificationPercent.enabled := havePlants;
  self.updateMenusForChangedSelectedPlants;
  end;

procedure TMainForm.updateMenusForChangedSelectedPlants;
  var
    haveSelectedPlants, haveMoreThanOneSelectedPlant: boolean;
  begin
  haveSelectedPlants := (selectedPlants.count > 0);
  haveMoreThanOneSelectedPlant := (selectedPlants.count > 1);
  MenuEditCut.enabled := haveSelectedPlants; PopupMenuCut.enabled := haveSelectedPlants;
  MenuEditCopy.enabled := haveSelectedPlants; PopupMenuCopy.enabled := haveSelectedPlants;
  MenuEditCopyAsText.enabled := haveSelectedPlants;
  MenuEditPasteAsText.enabled := (Clipboard.hasFormat(CF_TEXT)) and (domain.plantFileLoaded);
  MenuEditDelete.enabled := haveSelectedPlants;
  MenuEditDuplicate.enabled := haveSelectedPlants;
  MenuPlantRename.enabled := haveSelectedPlants; PopupMenuRename.enabled := haveSelectedPlants;
  MenuPlantEditNote.enabled := haveSelectedPlants; PopupMenuEditNote.enabled := haveSelectedPlants; // v1.4
  noteEdit.enabled := haveSelectedPlants; // v1.4
  MenuPlantRandomize.enabled := haveSelectedPlants; PopupMenuRandomize.enabled := haveSelectedPlants;
  MenuPlantZeroRotations.enabled := haveSelectedPlants; PopupMenuZeroRotations.enabled := haveSelectedPlants;
  MenuPlantBreed.enabled := haveSelectedPlants; PopupMenuBreed.enabled := haveSelectedPlants;
  MenuPlantMakeTimeSeries.enabled := haveSelectedPlants; PopupMenuMakeTimeSeries.enabled := haveSelectedPlants;
  MenuPlantAnimate.enabled := haveSelectedPlants; PopupMenuAnimate.enabled := haveSelectedPlants;
  MenuLayoutSelectAll.enabled := (plants.count > 0) and (selectedPlants.count < plants.count);
  MenuLayoutDeselect.enabled := haveSelectedPlants;
  MenuFileMakePainterAnimation.enabled := haveSelectedPlants;
  MenuLayoutHide.enabled := haveSelectedPlants;
  MenuLayoutShow.enabled := haveSelectedPlants;
  MenuLayoutHideOthers.enabled := (haveMoreThanOneSelectedPlant)
    and (not domain.viewPlantsInMainWindowOnePlantAtATime)
    and (selectedPlants.count < plants.count);
  MenuLayoutMakeBouquet.enabled := haveMoreThanOneSelectedPlant and not domain.viewPlantsInMainWindowOnePlantAtATime;
  MenuLayoutBringForward.enabled := haveSelectedPlants and (selectedPlants.count < plants.count);
  MenuLayoutSendBack.enabled := haveSelectedPlants and (selectedPlants.count < plants.count);
  // location
  xLocationEdit.enabled := haveSelectedPlants;
  xLocationSpin.enabled := haveSelectedPlants;
  yLocationEdit.enabled := haveSelectedPlants;
  yLocationSpin.enabled := haveSelectedPlants;
  // rotation
  xRotationEdit.enabled := haveSelectedPlants;
  xRotationSpin.enabled := haveSelectedPlants;
  yRotationEdit.enabled := haveSelectedPlants;
  yRotationSpin.enabled := haveSelectedPlants;
  zRotationEdit.enabled := haveSelectedPlants;
  zRotationSpin.enabled := haveSelectedPlants;
  resetRotations.enabled := haveSelectedPlants;
  // drawing scale
  drawingScaleEdit.enabled := haveSelectedPlants;
  drawingScaleSpin.enabled := haveSelectedPlants;
  // alignment
  alignTops.enabled := haveMoreThanOneSelectedPlant;
  alignBottoms.enabled := haveMoreThanOneSelectedPlant;
  alignLeft.enabled := haveMoreThanOneSelectedPlant;
  alignRight.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutAlign.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutAlignTops.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutAlignBottoms.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutAlignLeftSides.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutAlignRightSides.enabled := haveMoreThanOneSelectedPlant;
  // size
  makeEqualWidth.enabled := haveMoreThanOneSelectedPlant;
  makeEqualHeight.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutSize.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutSizeSameWidth.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutSizeSameHeight.enabled := haveMoreThanOneSelectedPlant;
  // pack
  packPlants.enabled := haveMoreThanOneSelectedPlant;
  MenuLayoutPack.enabled := haveMoreThanOneSelectedPlant;
  end;

procedure TMainForm.updatePasteMenuForClipboardContents;
  begin
  MenuEditPaste.enabled := (domain.plantManager.privatePlantClipboard.count > 0);
  PopupMenuPaste.enabled := MenuEditPaste.enabled;
  if BreederForm <> nil then BreederForm.updatePasteMenuForClipboardContents;
  if TimeSeriesForm <> nil then TimeSeriesForm.updatePasteMenuForClipboardContents;
  end;

procedure TMainForm.updateSectionPopupMenuForSectionChange;
  var
    haveSection: boolean;
  begin
  haveSection := self.currentSection <> nil;
  sectionPopupMenuHelp.enabled := haveSection;
  end;

procedure TMainForm.updateParamPopupMenuForParamSelectionChange;
  var
    haveSection: boolean;
    haveParam: boolean;
  begin
  haveSection := self.currentSection <> nil;
  paramPopupMenuExpandAllInSection.enabled := haveSection;
  paramPopupMenuCollapseAllInSection.enabled := haveSection;
  haveParam := self.selectedParameterPanel <> nil;
  paramPopupMenuHelp.enabled := haveParam;
  paramPopupMenuExpand.enabled := haveParam;
  paramPopupMenuCollapse.enabled := haveParam;
  end;

{ ---------------------------------------------------------------------------- *drawing }
procedure TMainForm.invalidateDrawingRect(aRect: TRect);
  var
    newRect: TRect;
	begin
  newRect := invalidDrawingRect;
  unionRect(newRect, newRect, aRect);
  invalidDrawingRect := newRect;
  end;

procedure TMainForm.invalidateEntireDrawing;
	begin
  invalidDrawingRect := rect(0, 0, drawingBitmap.width, drawingBitmap.height);
	end;

procedure TMainForm.paintDrawing(immediate: boolean);
  var
    plantPartsToDraw: longint;
    showProgress: boolean;
	begin
  if Application.terminated then exit;
  plantPartsToDraw := 0;
  showProgress := domain.options.showPlantDrawingProgress and (not domain.options.cachePlantBitmaps);
  with invalidDrawingRect do
    if (top <> 0) or (left <> 0) or (bottom <> 0) or (right <> 0) then
      begin
      try
        if not mouseMoveActionInProgress then cursor_startWait;
        intersectClipRect(drawingBitmap.canvas.handle, left, top, right, bottom);
        fillBitmap(drawingBitmap, domain.options.backgroundColor);
        if showProgress then
          plantPartsToDraw := Domain.plantManager.totalPlantPartCountInInvalidRect(selectedPlants, invalidDrawingRect,
            kExcludeInvisiblePlants, kIncludeNonSelectedPlants);
        try
          drawing := true;
          if showProgress then self.startDrawProgress(plantPartsToDraw);
            domain.plantManager.drawOnInvalidRect(drawingBitmap.canvas, selectedPlants, invalidDrawingRect,
                kExcludeInvisiblePlants, kIncludeNonSelectedPlants);
        finally
          drawing := false;
          if showProgress then self.finishDrawProgress;
        end;
        if (immediate) then
          self.copyDrawingBitmapToPaintBox;
      finally
        if not mouseMoveActionInProgress then cursor_stopWait;
        invalidDrawingRect := bounds(0,0,0,0);
      end;
      end;      
	end;

procedure TMainForm.drawingPaintBoxPaint(Sender: TObject);
	begin
  self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.copyDrawingBitmapToPaintBox;
  var
    drawSelectionRects, drawBoundingRects, includePlant: boolean;
    i: smallint;
    plant: PdPlant;
    aRect, insetOneRect, intersection: TRect;
    intersectResult: longbool;
    oldPalette: HPALETTE;
  begin
  if Application.terminated then exit;
  if (domain = nil) or (plants = nil) then exit;
  aRect := Rect(0, 0, drawingBitmap.width, drawingBitmap.height);
  // use an inset rect to avoid flicker in the boundary rectangle
  insetOneRect := rect(1, 1, drawingBitmap.width - 1, drawingBitmap.height - 1);
  with drawingPaintBox.canvas do
    begin
    oldPalette := 0;
    oldPalette := selectPalette(handle, MainForm.paletteImage.picture.bitmap.palette, false);
    realizePalette(handle);
    copyRect(insetOneRect, drawingBitmap.canvas, insetOneRect);
    brush.style := bsClear;
    pen.width := 1;
    drawBoundingRects := (domain.options.showBoundsRectangle) and (not domain.viewPlantsInMainWindowOnePlantAtATime)
        and (not domain.temporarilyHideSelectionRectangles);
    if (drawBoundingRects) and (plants.count > 0) then
      begin
      pen.color := clSilver;
      for i := 0 to plants.count - 1 do
        begin
        plant := PdPlant(plants.items[i]);
        if not plant.hidden then
          with plant.boundsRect_pixels do rectangle(left, top, right, bottom);
        end;
      end;
    drawSelectionRects := (domain.options.showSelectionRectangle) and (not domain.viewPlantsInMainWindowOnePlantAtATime)
        and (not domain.temporarilyHideSelectionRectangles);
    if (drawSelectionRects) and (plants.count > 0) then for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      includePlant := false;
      intersectResult := IntersectRect(intersection, plant.boundsRect_pixels, aRect);
      includePlant := includePlant or intersectResult;
      includePlant := includePlant and not plant.hidden;
      if not includePlant then continue;
      if isFocused(plant) then
        begin
        pen.color := domain.options.firstSelectionRectangleColor;
        with plant.boundsRect_pixels do rectangle(left, top, right, bottom);
        if cursorModeForDrawing = kCursorModeSelectDrag then
          begin
          brush.color := pen.color;
          with plant.resizingRect do rectangle(left, top, right, bottom);
          brush.style := bsClear;
          end;
        end
      else if isSelected(plant) then
        begin
        pen.color := domain.options.multiSelectionRectangleColor;
        with plant.boundsRect_pixels do rectangle(left, top, right, bottom);
        end;
      end;
    pen.color := clBtnText;
    rectangle(0, 0, drawingPaintBox.width, drawingPaintBox.height);
    selectPalette(handle, oldPalette, true);
    realizePalette(handle);
    end;
  end;
{ ---------------------------------------------------------------------------- *bitmaps for plants }
function TMainForm.screenBytesPerPixel: single;
  var screenDC: HDC;
  begin
  screenDC := GetDC(0);
  try
    result := (GetDeviceCaps(screenDC, BITSPIXEL) * GetDeviceCaps(screenDC, PLANES));
    result := result / 8.0;
  finally
    ReleaseDC(0, screenDC);
  end;
  end;

function TMainForm.bytesInPlantBitmaps(plantToExclude: PdPlant): longint;
  var
    bytesInBitmap: longint;
    bytesPerPixel: single;
    i: smallint;
    plant: PdPlant;
  begin
  result := 0;
  bytesPerPixel := self.screenBytesPerPixel;
  if plants.count > 0 then for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    if plant.hidden then continue;
    // plant that is asking should not be counted, since it is looking to resize and lose the old size
    if plant = plantToExclude then continue;
    bytesInBitmap := round(plant.previewCache.width * plant.previewCache.height * bytesPerPixel);
    result := result + bytesInBitmap;
    end;
  end;

function TMainForm.roomForPlantBitmap(plant: PdPlant; bytesForThisPlant: longint): boolean;
  var
    bytesAlreadyNotIncludingThisPlant, bytesLimit: longint;
    megabytesTried: single;
  begin
  bytesAlreadyNotIncludingThisPlant := self.bytesInPlantBitmaps(plant);
  bytesLimit := domain.options.memoryLimitForPlantBitmaps_MB * 1024 * 1024;
  result := bytesAlreadyNotIncludingThisPlant + bytesForThisPlant < bytesLimit;
  if not result then
    begin
    megabytesTried := (bytesAlreadyNotIncludingThisPlant + bytesForThisPlant) / (1024 * 1024);
    showMessage('The total size of plant bitmaps (' + floatToStrF(megabytesTried, ffFixed, 7, 1) + ') has exceeded '
      + 'the memory limit of ' + intToStr(domain.options.memoryLimitForPlantBitmaps_MB) + ' megabytes.' + chr(13)
      + 'All plant bitmaps have been dropped and plants will be drawn directly on the window.' + chr(13)
      + 'To use plant bitmaps again, choose Use Plant Bitmaps from the Options menu.' + chr(13) + chr(13)
      + 'If you have more free memory, your memory limit is set too low.' + chr(13)
      + 'To increase the memory limit, choose Preferences from the Edit menu.' + chr(13)
      + 'Click Help in the Preferences window for details.');
    self.stopUsingPlantBitmaps;
    end;
  end;

procedure TMainForm.exceptionResizingPlantBitmap;
  begin
    showMessage('An exception occurred while resizing a plant bitmap. ' + chr(13)
      + 'All plant bitmaps have been dropped and plants will be drawn directly on the window.' + chr(13) 
      + 'To use plant bitmaps again, choose Use Plant Bitmaps from the Options menu.' + chr(13) + chr(13)
      + 'This exception means that your memory limit is set too high for the available memory.' + chr(13)
      + 'To decrease the memory limit, choose Preferences from the Edit menu.' + chr(13)
      + 'Click Help in the Preferences window for details.');
    self.stopUsingPlantBitmaps;
  end;

procedure TMainForm.updateForChangeToPlantBitmaps;
  var
    aString: string;
    bytesInUse: longint;
    megabytesInUse: single;
  begin
  if domain.options.showLongHintsForButtons then
    aString := 'Plant bitmaps are used to speed up drawing by caching each plant into a separate '
      + 'bitmap in memory. Plant bitmaps are turned '
  else
    aString := 'Plant bitmaps are turned ';
  bytesInUse := 0;
  megabytesInUse := 0;
  if domain.options.cachePlantBitmaps then
    begin
    bytesInUse := self.bytesInPlantBitmaps(nil);
    megabytesInUse := bytesInUse / (1024 * 1024);
    aString := aString + 'ON and are using ' + floatToStrF(megabytesInUse, ffFixed, 7, 1)
      + ' out of ' + intToStr(domain.options.memoryLimitForPlantBitmaps_MB) + ' MB of memory.';
    end
  else
    aString := aString + 'OFF.';
  if domain.options.showLongHintsForButtons then
    begin
    if not domain.options.cachePlantBitmaps then
      aString := aString + ' You can turn plant bitmaps on using the Options menu.'
    else
      aString := aString +
        ' You can change the amount of memory dedicated to plant bitmaps in the Preferences window.';
    end;
  if plantBitmapsIndicatorImage <> nil then
    begin
    if domain.options.cachePlantBitmaps then
      begin
      if megabytesInUse / domain.options.memoryLimitForPlantBitmaps_MB <= 0.5 then
        plantBitmapsIndicatorImage.picture := plantBitmapsGreenImage.picture
      else if megabytesInUse / domain.options.memoryLimitForPlantBitmaps_MB <= 0.8 then
        plantBitmapsIndicatorImage.picture := plantBitmapsYellowImage.picture
      else 
        plantBitmapsIndicatorImage.picture := plantBitmapsRedImage.picture;
      end
    else
      plantBitmapsIndicatorImage.picture := noPlantBitmapsImage.picture;
    plantBitmapsIndicatorImage.hint := aString;
    end;
  end;

procedure TMainForm.stopUsingPlantBitmaps;
  begin
  domain.options.cachePlantBitmaps := false;
  MenuOptionsUsePlantBitmaps.checked := domain.options.cachePlantBitmaps;
  self.shrinkAllPlantBitmaps;
  self.invalidateEntireDrawing;
  end;

procedure TMainForm.startUsingPlantBitmaps;
  begin
  domain.options.cachePlantBitmaps := true;
  MenuOptionsUsePlantBitmaps.checked := domain.options.cachePlantBitmaps;
  self.recalculateAllPlantBoundsRects(kDrawNow);
  self.invalidateEntireDrawing;
  end;

{ ---------------------------------------------------------------------------- *command list management }
procedure TMainForm.clearCommandList;
  begin
  commandList.free;
  commandList := nil;
  commandList := PdCommandList.create;
  self.updateMenusForUndoRedo;
  end;

procedure TMainForm.doCommand(command: PdCommand);
	begin
  commandList.doCommand(command);
  self.updateForPossibleChangeToDrawing;
  end;

{ ------------------------------------------------------------------------------- *called by commands }
procedure TMainForm.hideOrShowSomePlants(plantList: TList; hideList: TList; hide: boolean; drawNow: boolean);
  var
    redrawRect: TRect;
    i: smallint;
    plant: PdPlant;
  begin
  if (plantList = nil) or (plantList.count <= 0) then exit;
  redrawRect := bounds(0,0,0,0);
  for i := 0 to plantList.count - 1 do
    begin
    plant := PdPlant(plantList.items[i]);
    if (hideList <> nil) and (hideList.count > 0) then
      plant.hidden := PdBooleanValue(hideList.items[i]).saveBoolean
    else
      plant.hidden := hide;
    plant.recalculateBounds(kDrawNow); // magnification might have changed
    unionRect(redrawRect, redrawRect, plant.boundsRect_pixels);
    end;
  self.invalidateDrawingRect(redrawRect);
  plantListDrawGrid.invalidate;
  if drawNow then
    self.updateForPossibleChangeToDrawing;
  end;

const
  kScaleToFitMargin = 10;
  kOffscreenMargin = 20;

procedure TMainForm.fitVisiblePlantsInDrawingArea(drawNow: boolean;
    scaleAsWellAsMove: boolean; alwaysMove: boolean);
  var
    upperLeft_mm, lowerRight_mm, size_mm, offScreenUpperLeft_mm, offScreenLowerRight_mm: TPoint;
    xScale_pixelsPerMm, yScale_pixelsPerMm, newScale_pixelsPerMm, marginOffset_mm: single;
    i: smallint;
    plant: PdPlant;
    allPlantsAreOffscreen: boolean;
  begin
  if plants.count <= 0 then exit;
  for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    if not plant.hidden then
      plant.recalculateBounds(kDontDrawYet);
    end;
  upperLeft_mm := self.upperLeftMostPlantBoundsRectPoint_mm;
  lowerRight_mm := self.lowerRightMostPlantBoundsRectPoint_mm;
  size_mm := Point(lowerRight_mm.x - upperLeft_mm.x, lowerRight_mm.y - upperLeft_mm.y);
  // move domain offset so all plants begin within drawing area
  if alwaysMove then
    allPlantsAreOffscreen := false
  else
    begin
    // determine if all plants are out of the drawing area and so must be moved
    offScreenUpperLeft_mm.x := round(kOffscreenMargin / domain.plantManager.plantDrawScale_pixelsPerMm);
    offScreenUpperLeft_mm.y := round(kOffscreenMargin / domain.plantManager.plantDrawScale_pixelsPerMm);
    offScreenLowerRight_mm.x := round((drawingPaintBox.width - kOffscreenMargin) / domain.plantManager.plantDrawScale_pixelsPerMm);
    offScreenLowerRight_mm.y := round((drawingPaintBox.height - kOffscreenMargin) / domain.plantManager.plantDrawScale_pixelsPerMm);
    allPlantsAreOffscreen := (lowerRight_mm.x <= offScreenUpperLeft_mm.x) or (lowerRight_mm.y <= offScreenUpperLeft_mm.y)
      or (upperLeft_mm.x >= offScreenLowerRight_mm.x) or (upperLeft_mm.y >= offScreenLowerRight_mm.y);
    end;
  if scaleAsWellAsMove then
    begin
    xScale_pixelsPerMm := safedivExcept(1.0 * drawingPaintBox.width - 1.0 * kScaleToFitMargin * 2, size_mm.x, 0);
    yScale_pixelsPerMm := safedivExcept(1.0 * drawingPaintBox.height - 1.0 * kScaleToFitMargin * 2, size_mm.y, 0);
    newScale_pixelsPerMm := min(xScale_pixelsPerMm, yScale_pixelsPerMm);
    end
  else
    newScale_pixelsPerMm := 0;
  if alwaysMove or allPlantsAreOffscreen then
    begin
    marginOffset_mm := safedivExcept(1.0 * kScaleToFitMargin, newScale_pixelsPerMm, 0);
    domain.plantManager.plantDrawOffset_mm := setSinglePoint(-upperLeft_mm.x + marginOffset_mm,
      -upperLeft_mm.y + marginOffset_mm);
    end;
  // calculate new scale to fit all plants in drawing area and apply
  if (scaleAsWellAsMove) and (newScale_pixelsPerMm <> 0.0) then
    self.magnifyOrReduce(newScale_pixelsPerMm, Point(0, 0), drawNow);
  end;

{ ------------------------------------------------------------------------------- *selected plants list }
procedure TMainForm.selectPlantAtPoint(aPoint: TPoint; shift: boolean);
  var
   newCommand: PdCommand;
   newList: TList;
   plant: PdPlant;
   i: smallint;
  begin
  plant := domain.plantManager.findPlantAtPoint(aPoint);
  newList := TList.create;
  try
    if (shift) and (selectedPlants.count > 0) then
      for i := 0 to selectedPlants.count - 1 do
        newList.add(selectedPlants.items[i]);
    if newList.indexOf(plant) >= 0 then
      newList.remove(plant)
    else if plant <> nil then
      newList.add(plant);
    if not self.twoListsAreIdentical(self.selectedPlants, newList) then
      begin
      newCommand := PdChangeSelectedPlantsCommand.createWithOldListOfPlantsAndNewList(self.selectedPlants, newList);
      self.doCommand(newCommand);
      end;
  finally
    newList.free;
  end;
  end;

procedure TMainForm.selectPlantAtIndex(Shift: TShiftState; index: Integer);
  var
   newCommand: PdCommand;
   newList: TList;
   i: smallint;
   plant: PdPlant;
	begin
  if application.terminated then exit;
  if plants.count <= 0 then exit;
  if (index < 0) then
    begin
    if selectedPlants.count <= 0 then exit;
    newList := TList.create;
    try
      newCommand := PdChangeSelectedPlantsCommand.createWithOldListOfPlantsAndNewList(self.selectedPlants, newList);
      self.doCommand(newCommand);
    finally
      newList.free;
    end;
    exit;
    end;
  plant := PdPlant(plants.items[index]);
  if plant = nil then exit;
  newList := TList.create;
  try
    if (ssCtrl in shift) then
      begin
      if selectedPlants.count > 0 then for i := 0 to selectedPlants.count - 1 do
        newList.add(selectedPlants.items[i]);
      if newList.indexOf(plant) >= 0 then
        newList.remove(plant)
      else
        newList.add(plant);
      end
    else if (ssShift in shift) then
      begin
      if selectedPlants.count > 0 then for i := 0 to selectedPlants.count - 1 do
        newList.add(selectedPlants.items[i]);
      if (lastSingleClickPlantIndex >= 0) and (lastSingleClickPlantIndex <= plants.count - 1)
          and (lastSingleClickPlantIndex <> index) then
        begin
        if lastSingleClickPlantIndex < index then
          begin
          for i := lastSingleClickPlantIndex to index do
            if newList.indexOf(plants.items[i]) < 0 then
              newList.add(plants.items[i]);
          end
        else if lastSingleClickPlantIndex > index then
          begin
          for i := lastSingleClickPlantIndex downto index do
            if newList.indexOf(plants.items[i]) < 0 then
              newList.add(plants.items[i]);
          end;
        end;
      end
    else
      begin
      if isSelected(plant) then
        begin
        if selectedPlants.count > 0 then for i := 0 to selectedPlants.count - 1 do
          newList.add(selectedPlants.items[i]);
        end
      else
        begin
        newList.add(plant);
        lastSingleClickPlantIndex := index;
        end;
      end;
    if not self.twoListsAreIdentical(self.selectedPlants, newList) then
      begin
      newCommand := PdChangeSelectedPlantsCommand.createWithOldListOfPlantsAndNewList(self.selectedPlants, newList);
      self.doCommand(newCommand);
      end;
  finally
    newList.free;
  end;
	end;

function TMainForm.twoListsAreIdentical(firstList, secondList: TList): boolean;
  var
    i: longint;
  begin
  result := false;
  if (firstList = nil) or (secondList = nil) then exit;
  if firstList.count <> secondList.count then exit;
  if firstList.count <= 0 then exit;
  for i := 0 to firstList.count - 1 do
    if firstList.items[i] <> secondList.items[i] then
      exit;
  result := true;
  end;

procedure TMainForm.deselectAllPlants;
  begin
  selectedPlants.clear;
  self.updateForChangeToPlantSelections;
  end;

procedure TMainForm.deselectAllPlantsButFirst;
  var
    firstPlant: PdPlant;
  begin
  if selectedPlants.count <= 0 then exit;
  firstPlant := self.focusedPlant;
  selectedPlants.clear;
  selectedPlants.add(firstPlant);
  self.updateForChangeToPlantSelections;
  end;

procedure TMainForm.selectFirstPlantInPlantList;
  begin
  if plants.count <= 0 then exit;
  selectedPlants.clear;
  selectedPlants.add(plants.items[0]);
  self.updateForChangeToPlantSelections;
  end;

procedure TMainForm.showOnePlantExclusively(drawNow: boolean);
  var
    booleansList: TListCollection;
    i: smallint;
    plant, firstPlant: PdPlant;
  begin
  booleansList := nil;
  firstPlant := self.focusedPlant;
  try
    cursor_startWait;
    booleansList := TListCollection.create;
    for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      if plant <> nil then
        booleansList.add(PdBooleanValue.createWithBoolean(not (plant = firstPlant)));
      end;
    self.hideOrShowSomePlants(plants, booleansList, false, kDontDrawYet);
    self.fitVisiblePlantsInDrawingArea(kDontDrawYet, kScaleAndMove, kAlwaysMove);
    if firstPlant <> nil then
      begin
      firstPlant.recalculateBounds(kDrawNow); // must draw now because bitmap could be wrong
      self.invalidateDrawingRect(firstPlant.boundsRect_pixels);
      end;
    if drawNow then
      self.updateForPossibleChangeToDrawing;
  finally
    booleansList.free;
    cursor_stopWait;
  end;
  end;

procedure TMainForm.redrawFocusedPlantOnly(drawNow: boolean);
  var
    firstPlant: PdPlant;
  begin
  firstPlant := self.focusedPlant;
  if firstPlant <> nil then
    begin
    firstPlant.recalculateBounds(kDrawNow);
    self.invalidateDrawingRect(firstPlant.boundsRect_pixels);
    end;
  if drawNow then
    self.updateForPossibleChangeToDrawing;
  end;

procedure TMainForm.addSelectedPlant(aPlant: PdPlant; insertIndex: smallint);
  begin
  if (insertIndex >= 0) and (insertIndex <= selectedPlants.count - 1) then
    self.selectedPlants.insert(insertIndex, aPlant)
  else
    self.selectedPlants.add(aPlant);
  self.invalidateDrawingRect(aPlant.boundsRect_pixels);
  end;

procedure TMainForm.removeSelectedPlant(aPlant: PdPlant);
  begin
  self.invalidateDrawingRect(aPlant.boundsRect_pixels);
  self.selectedPlants.remove(aPlant);
  end;

function TMainForm.isSelected(plant: PdPlant): boolean;
  begin
  result := false;
  if (selectedPlants = nil) or (selectedPlants.count <= 0) then exit;
  result := selectedPlants.indexOf(plant) >= 0;
  end;

function TMainForm.isFocused(plant: PdPlant): boolean;
  begin
  result := false;
  if plant = nil then exit;
  if (selectedPlants = nil) or (selectedPlants.count <= 0) then exit;
  result := selectedPlants.indexOf(plant) = 0;
  end;

function TMainForm.focusedPlant: PdPlant;
  begin
  result := nil;
  if selectedPlants.count > 0 then
    result := PdPlant(selectedPlants.items[0]);
  end;

function TMainForm.focusedPlantIndex: smallint;
  begin
  result := -1;
  if selectedPlants.count > 0 then
    result := plants.indexOf(PdPlant(selectedPlants.items[0]));
  end;

function TMainForm.firstUnfocusedPlant: PdPlant;
  begin
  result := nil;
  if selectedPlants.count > 1 then
    result := PdPlant(selectedPlants.items[1]);
  end;

function TMainForm.firstSelectedPlantInList: PdPlant;
  var
    i: smallint;
    plant: PdPlant;
  begin
  result := nil;
  if plants.count > 0 then for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    if isSelected(plant) then
      begin
      result := plant;
      exit;
      end;
    end;
  end;

function TMainForm.lastSelectedPlantInList: PdPlant;
  var
    i: smallint;
    plant: PdPlant;
  begin
  result := nil;
  if plants.count > 0 then for i := plants.count - 1 downto 0 do
    begin
    plant := PdPlant(plants.items[i]);
    if isSelected(plant) then
      begin
      result := plant;
      exit;
      end;
    end;
  end;

{ ------------------------------------------------------------------------------------- *list of plants }
procedure TMainForm.plantListDrawGridDrawCell(Sender: TObject; Col, Row: Integer;
  Rect: TRect; State: TGridDrawState);
  var
	  plant: PdPlant;
    selected: boolean;
    visibleRect, remainderRect: TRect;
    cText: array[0..255] of Char;
  begin
  if Application.terminated then exit;
  plantListDrawGrid.canvas.brush.color := plantListDrawGrid.color;
  plantListDrawGrid.canvas.fillRect(rect);
  if (plants.count <= 0) or (row < 0) or (row > plants.count - 1) then exit;
  { set up plant pointer }
  plant := PdPlant(plants.items[row]);
  if plant = nil then exit;
  selected := isSelected(plant);
  { set up rectangles }
  visibleRect := rect;
  visibleRect.right := visibleRect.left + plantListDrawGrid.defaultRowHeight;
  remainderRect := rect;
  remainderRect.left := remainderRect.left + rWidth(visibleRect);
  { fill first box with white, rest with clHighlight if selected }
  with plantListDrawGrid.canvas do
    begin
    brush.style := bsSolid;
    brush.color := plantListDrawGrid.color;
    fillRect(visibleRect);
    if not plant.hidden then
      draw(visibleRect.left + (visibleRect.right - visibleRect.left) div 2
          - visibleBitmap.picture.bitmap.width div 2, rect.top, visibleBitmap.picture.bitmap);
    font := plantListDrawGrid.font;
    if selected then
      begin
      brush.color := clHighlight;
      font.color := clHighlightText;
      end
    else
      begin
      brush.color := plantListDrawGrid.color;
      font.color := clBtnText;
      end;
    fillRect(remainderRect);
    strPCopy(cText, plant.getName);
    remainderRect.left := remainderRect.left + 5; { margin for text }
    winprocs.drawText(handle, cText, strLen(cText), remainderRect, DT_LEFT);
    if plant = self.focusedPlant then
      drawFocusRect(rect);
    end;
  end;

procedure TMainForm.plantListDrawGridMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
	var
    col, row: integer;
    plant: PdPlant;
    hideList: TList;
    newCommand: PdCommand;
	begin
  if plants.count <= 0 then exit;
  if button = mbRight then exit;
  if justDoubleClickedOnDrawGrid then
    begin
    justDoubleClickedOnDrawGrid := false;
    exit;
    end
  else
    justDoubleClickedOnDrawGrid := false;
  plantListDrawGrid.mouseToCell(x, y, col, row);
  self.selectPlantAtIndex(shift, row); // does updating in command
  if (x <= 16) and (row >= 0) and (row <= plants.count - 1) then
    begin
    plant := PdPlant(plants.items[row]);
    if plant = nil then exit;
    hideList := TList.create;
    try
      hideList.add(plant);
      newCommand := PdHideOrShowCommand.createWithListOfPlantsAndHideOrShow(hideList, not plant.hidden);
      self.doCommand(newCommand);
    finally
      hideList.free;
    end;
    end;
  if x > 16 then
    plantListDrawGrid.beginDrag(false);
  end;

procedure TMainForm.plantListDrawGridMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    popupPositionInScreenCoords: TPoint;
  begin
  if button = mbRight then
    begin
    popupPositionInScreenCoords := plantListDrawGrid.clientToScreen(Point(x,y));
    plantPopupMenu.popup(popupPositionInScreenCoords.x, popupPositionInScreenCoords.y);
    end;
  end;

procedure TMainForm.plantListDrawGridDragOver(Sender, Source: TObject; X,
  Y: Integer; State: TDragState; var Accept: Boolean);
  begin
  accept := (source <> nil) and (sender <> nil)
     and ((BreederForm <> nil) and (source = BreederForm.plantsDrawGrid)
           or (TimeSeriesForm <> nil) and (source = TimeSeriesForm.grid));
  end;

procedure TMainForm.plantListDrawGridEndDrag(Sender, Target: TObject; X,
  Y: Integer);
  begin
  if application.terminated then exit;
  if (target <> nil) and (target is TDrawGrid) then
    begin
    if self.focusedPlant <> nil then
      begin
      if ((target as TDrawGrid).owner is TBreederForm) then
        BreederForm.copyPlantToPoint(self.focusedPlant, x, y)
      else if ((target as TDrawGrid).owner is TTimeSeriesForm) then
        TimeSeriesForm.copyPlantToPoint(self.focusedPlant, x, y);
      end;
    end;
  end;

procedure TMainForm.plantListDrawGridDblClick(Sender: TObject);
  begin
  self.MenuPlantRenameClick(self);
  plantListDrawGrid.endDrag(false);
  justDoubleClickedOnDrawGrid := true;
  end;

procedure TMainForm.moveSelectedPlantsUp;
  var
    i: smallint;
    plant: PdPlant;
  begin
  if plants.count > 1 then
    begin
    i := 1;  { start at 1 because you can't move first one up any more }
    while i <= plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      if isSelected(plant) then
        plants.move(i, i - 1);
      inc(i);
      end;
    end;
  self.invalidateSelectedPlantRectangles;
  self.updateForPossibleChangeToDrawing;
  plantListDrawGrid.invalidate;
  end;

procedure TMainForm.moveSelectedPlantsDown;
  var
    i: smallint;
    plant: PdPlant;
  begin
  if plants.count > 1 then
    begin
    i := plants.count - 2;  { start at next to last one because you can't move last one down any more }
    while i >= 0 do
      begin
      plant := PdPlant(plants.items[i]);
      if isSelected(plant) then
        plants.move(i, i + 1);
      dec(i);
      end;
    end;
  self.invalidateSelectedPlantRectangles;
  self.updateForPossibleChangeToDrawing;
  plantListDrawGrid.invalidate;
  end;

procedure TMainForm.plantListDrawGridKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  case key of
    vk_down, vk_right:
      if (ssShift in shift) then
        begin
        key := 0; {swallow key}
        self.MenuLayoutSendBackClick(self);
        end
      else
        begin
        key := 0;
        self.moveUpOrDownWithKeyInPlantList(focusedPlantIndex + 1);
        end;
    vk_up, vk_left:
      if (ssShift in shift) then
        begin
        key := 0; {swallow key}
        self.MenuLayoutBringForwardClick(self);
        end
     else  
        begin
        key := 0;
        self.moveUpOrDownWithKeyInPlantList(focusedPlantIndex - 1);
        end;
    vk_return:
        begin
        key := 0;
        self.MenuPlantRenameClick(self);
        end;
    end;
  end;

{ -------------------------------------------------------------------------- *mouse handling in drawing }
procedure TMainForm.PaintBoxMouseDown(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    newCommand: PdCommand;
    anchorPoint: TPoint;
    plantClickedOn: PdPlant;
  begin
  if application.terminated then exit;
  if plants.count <= 0 then exit;
  if actionInProgress then
    // error somewhere - user did weird things with mouse buttons - teminate action...
    try
      self.PaintBoxMouseUp(sender, button, shift, x, y);
    finally
      actionInProgress := false;
    end;
  case cursorModeForDrawing of
    kCursorModeSelectDrag:
      begin
      if Button = mbRight then exit;
      plantClickedOn := nil;
      plantClickedOn := domain.plantManager.findPlantAtPoint(Point(x, y));
      if plantClickedOn = nil then
        begin
        if domain.viewPlantsInMainWindowOnePlantAtATime then exit;
        rubberBanding := true;
        rubberBandStartDragPoint := Point(x, y);
        rubberBandLastDrawPoint := Point(x, y);
        rubberBandNeedToRedraw := true;
        exit; // select command made in mouse up
        end
      else
        begin
        actionInProgress := true;
        if (not plantClickedOn.pointIsInResizingRect(Point(x, y)))
            and ((not isSelected(plantClickedOn)) or (ssShift in shift)) then
          begin
          self.selectPlantAtPoint(Point(x, y), (ssShift in shift) and (not (ssCtrl in shift)));
          self.updateForPossibleChangeToDrawing;
          end;
        end;
      end;
    kCursorModeScroll: ;
    kCursorModeMagnify:
      begin
      rubberBanding := true;
      rubberBandStartDragPoint := Point(x, y);
      rubberBandLastDrawPoint := Point(x, y);
      rubberBandNeedToRedraw := true;
      end;
    kCursorModeRotate: ;
    kCursorModePosingSelect:
      begin
      if domain.options.drawSpeed <> kDrawBest then
        begin
        if MessageDlg('To pose a plant, you need the "Draw Using" option set to "Solids."' + chr(13) + chr(13)
          + 'Do you want to change it?', mtConfirmation, [mbYes, mbNo], 0) = IDYES then
          self.MenuOptionsBestDrawClick(self);
        exit;
        end;
      if tabSet.tabIndex <> kTabPosing then tabSet.tabIndex := kTabPosing;    
      plantClickedOn := nil;
      plantClickedOn := domain.plantManager.findPlantAtPoint(Point(x, y));
      if isFocused(plantClickedOn) then
        plantClickedOn.getInfoForPlantPartAtPoint(Point(x, y),
            self.mouseDownSelectedPlantPartID, self.mouseDownSelectedPlantPartType)
      else
        self.mouseDownSelectedPlantPartID := -1;
      if mouseDownSelectedPlantPartID = selectedPlantPartID then exit;
      end;
    end;
  anchorPoint := Point(x, y);
  commandList.rightButtonDown := (Button = mbRight) or (ssShift in shift); // makes shift-click work as right-click
  newCommand := self.makeMouseCommand(anchorPoint, shift);
  if newCommand <> nil then
    actionInProgress := commandList.mouseDown(newCommand, anchorPoint)
  else
    actionInProgress := false;
  if actionInProgress then
    self.updateForPossibleChangeToDrawing;
	end;

procedure TMainForm.PaintBoxMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
  var
    shouldCancelHint: boolean;
    plantClickedOn: PdPlant;
    aRect: TRect;
  begin
  if application.terminated then exit;
  if plants.count <= 0 then exit;
  // show cursor that tells you you can resize plant when mouse is in resize rect, but only in select mode
  if cursorModeForDrawing = kCursorModeSelectDrag then
    begin
    screen.cursor := crDefault;
    plantClickedOn := domain.plantManager.findPlantAtPoint(Point(x, y));
    if (domain.options.showSelectionRectangle)
       and (plantClickedOn <> nil)
       and (plantClickedOn = self.focusedPlant)
       and (plantClickedOn.pointIsInResizingRect(Point(x, y))) then
            screen.cursor := crSizeNS;
    end;
  // show hint for plant mouse is over
  if not actionInProgress then
    begin
    shouldCancelHint := false;
    if hintActive and ((x < hintX - kHintRange) or (x > hintX + kHintRange) or
      (y < hintY - kHintRange) or (y > hintY + kHintRange)) then
      begin
      if self.hintForPlantAtPoint(Point(x,y)) <> lastHintString then
        shouldCancelHint := true;
      if self.actionInProgress then
        shouldCancelHint := true;
      if ((x < hintX - kMaxHintRangeForLargeAreas) or (x > hintX + kMaxHintRangeForLargeAreas) or
        (y < hintY - kMaxHintRangeForLargeAreas) or (y > hintY + kMaxHintRangeForLargeAreas)) then
        shouldCancelHint := true;
      if shouldCancelHint then
        begin
        Application.cancelHint;
        hintActive := false;
        end;
      end;
    end;
  // continue rubber banding - could be done in either select or magnify mode
  if rubberBanding then
    begin
    self.undrawRubberBandBox;
    self.drawRubberBandBox(Point(x, y));
    exit;
    end;
  // continue action started in mouse down
  if actionInProgress then
    begin
    commandList.mouseMove(Point(x, y));
    if commandList.didMouseMove(Point(x, y)) then
      mouseMoveActionInProgress := true;
	  self.updateForPossibleChangeToDrawing;
    end;
	end;

procedure TMainForm.PaintBoxMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    popupPositionInScreenCoords: TPoint;
	begin
  if application.terminated then exit;
  if plants.count <= 0 then exit;
  // show popup menu but only if in select/drag mode
  if (Button = mbRight) and (cursorModeForDrawing = kCursorModeSelectDrag) then
    begin
    popupPositionInScreenCoords := clientToScreen(Point(x,y));
    plantPopupMenu.popup(popupPositionInScreenCoords.x, popupPositionInScreenCoords.y);
    exit;
    end;
  // finish rubber banding if doing that, could be in select or magnify mode
  if rubberBanding then
    begin
    rubberBanding := false;
    self.undrawRubberBandBox;
    if cursorModeForDrawing = kCursorModeSelectDrag then
      begin
      self.selectPlantsInRubberBandBox;
      exit;
      end;
    end;
  // finish action in progress
  try
    if actionInProgress then
      begin
      commandList.mouseUp(Point(x, y));
      actionInProgress := false;
      end;
    mouseMoveActionInProgress := false;
    self.updateForPossibleChangeToDrawing;
  finally
    // clear out all mouse settings
    screen.cursor := crDefault;
    mouseMoveActionInProgress := false;
    commandList.rightButtonDown := false;
    actionInProgress := false;
  end;
	end;

procedure TMainForm.PaintBoxDragOver(Sender, Source: TObject; X, Y: Integer; State: TDragState; var Accept: Boolean);
   begin
   accept := (source <> nil) and (sender <> nil)
      and ((BreederForm <> nil) and (source = BreederForm.plantsDrawGrid)
      or (TimeSeriesForm <> nil) and (source = TimeSeriesForm.grid));
   end;

procedure TMainForm.PaintBoxEndDrag(Sender, Target: TObject; X, Y: Integer);
  var
    plantClickedOn: PdPlant;
  begin
  if application.terminated then exit;
  if (target <> nil) and (target is TDrawGrid) then
    begin
    plantClickedOn := nil;
    plantClickedOn := domain.plantManager.findPlantAtPoint(commandList.anchorPoint);
    if plantClickedOn <> nil then
      begin
      if ((target as TDrawGrid).owner is TBreederForm) then
        BreederForm.copyPlantToPoint(plantClickedOn, x, y)
      else if ((target as TDrawGrid).owner is TTimeSeriesForm) then
        TimeSeriesForm.copyPlantToPoint(plantClickedOn, x, y);
      end;
    { command undoes itself when it starts the drag }
    end;
  end;

function TMainForm.makeMouseCommand(var point: TPoint; shift: TShiftState): PdCommand;
	begin         
  result := nil;
  case cursorModeForDrawing of
    kCursorModeSelectDrag:
      begin
      if (ssShift in shift) and (ssCtrl in shift) then
        begin
        result := nil;
        commandList.anchorPoint := point;
        self.drawingPaintBox.beginDrag(true);
        end
      else if (ssCtrl in shift) then
        result := PdDuplicateCommand.createWithListOfPlants(selectedPlants)
      else if (focusedPlant <> nil) and (focusedPlant.pointIsInResizingRect(point)) then
        begin
        screen.cursor := crSizeNS;
        result := PdResizePlantsCommand.createWithListOfPlants(selectedPlants);
        end
      else
        result := PdDragCommand.createWithListOfPlants(selectedPlants);
      end;
    kCursorModeScroll:
      result := PdScrollCommand.create;
    kCursorModeMagnify:
      // to zoom out, can do right button or shift
      if (commandList.rightButtonDown) then
        begin
        screen.cursor := crMagMinus;
        result := PdChangeMagnificationCommand.create;
        (result as PdChangeMagnificationCommand).shift := true;
        end
      else
        begin
        result := PdChangeMagnificationCommand.create;
        (result as PdChangeMagnificationCommand).shift := (ssShift in shift);
        end;
    kCursorModeRotate:
      begin
      if commandList.rightButtonDown then
        screen.cursor := crSizeWE;
      result := PdRotateCommand.createWithListOfPlants(selectedPlants);
      end;
    kCursorModePosingSelect:
      begin
      result := PdSelectPosingPartCommand.createWithPlantAndPartIDsAndTypes(focusedPlant,
          self.mouseDownSelectedPlantPartID, self.selectedPlantPartID,
          self.mouseDownSelectedPlantPartType, self.selectedPlantPartType);
      end;
    end;
  end;

{ ----------------------------------------------------------------------- *rubber banding }
procedure TMainForm.selectPlantsInRubberBandBox;
  var
    rubberBandRect: TRect;
    newList: TList;
    newCommand: PdCommand;
  begin
  newList := TList.create;
  try
    rubberBandRect := Rect(
      intMin(rubberBandStartDragPoint.x, rubberBandLastDrawPoint.x),
      intMin(rubberBandStartDragPoint.y, rubberBandLastDrawPoint.y),
      intMax(rubberBandStartDragPoint.x, rubberBandLastDrawPoint.x),
      intMax(rubberBandStartDragPoint.y, rubberBandLastDrawPoint.y));
    domain.plantManager.fillListWithPlantsInRectangle(rubberBandRect, newList);
    if not self.twoListsAreIdentical(self.selectedPlants, newList) then
      begin
      newCommand := PdChangeSelectedPlantsCommand.createWithOldListOFPlantsAndNewList(self.selectedPlants, newList);
      self.doCommand(newCommand);
      end;
  finally
    newList.free;
  end;
  end;

procedure TMainForm.drawRubberBandBox(newPoint: TPoint);
  begin
  rubberBandLastDrawPoint := newPoint;
  self.drawOrUndrawRubberBandBox;
  self.rubberBandNeedToRedraw := true;
  end;

procedure TMainForm.undrawRubberBandBox;
  begin
  if not self.rubberBandNeedToRedraw then exit;
  self.drawOrUndrawRubberBandBox;
  self.rubberBandNeedToRedraw := false;
  end;

procedure TMainForm.drawOrUndrawRubberBandBox;
  var
    theDC: HDC;
    drawRect: TRect;
  begin
  theDC := getDC(0);
  drawRect := Rect(
      self.clientOrigin.x + drawingPaintBox.left + rubberBandStartDragPoint.x,
      self.clientOrigin.y + drawingPaintBox.top + rubberBandStartDragPoint.y,
      self.clientOrigin.x + drawingPaintBox.left + rubberBandLastDrawPoint.x,
      self.clientOrigin.y + drawingPaintBox.top + rubberBandLastDrawPoint.y);
  with drawRect do
    begin
    patBlt(theDC, left, top, right - left, 1, dstInvert);
    patBlt(theDC, right, top, 1, bottom - top, dstInvert);
    patBlt(theDC, left, bottom, right - left, 1, dstInvert);
    patBlt(theDC, left, top, 1, bottom - top, dstInvert);
    end;
  releaseDC(0, theDC);
  end;

{ ------------------------------------------------------------------------------------ *hint handling }
procedure TMainForm.DoShowHint(var HintStr: ansistring; var CanShow: Boolean; var HintInfo: THintInfo);
  begin
  hintInfo.hintPos := hintInfo.hintControl.clientToScreen(Point(HintInfo.CursorPos.x + 20, HintInfo.CursorPos.y + 20));
  hintInfo.hintMaxWidth := 200;
  if HintInfo.HintControl = drawingPaintBox then
    begin
    if not actionInProgress then
      begin
  	  HintStr := self.hintForPlantAtPoint(HintInfo.CursorPos);
      lastHintString := HintStr;
      hintActive := true;
      hintX := HintInfo.CursorPos.x;
      hintY := HintInfo.CursorPos.y;
      end
    end                          
  else
    begin
    if (Domain <> nil) and (Domain.hintManager <> nil) then
      hintStr := Domain.hintManager.hintForComponentName(hintInfo, domain.options.showLongHintsForButtons,
          domain.options.showHintsForParameters);
    if (hintStr = '') and (hintInfo.hintControl.showHint) then
      hintStr := hintInfo.hintControl.hint;
    end;
  end;

function TMainForm.hintForPlantAtPoint(aPoint: TPoint): string;
  var
    plant: PdPlant;
  begin
  result := '';
  plant := nil;
  plant := domain.plantManager.findPlantAtPoint(aPoint);
  if plant <> nil then
    result := plant.getHint(aPoint);  // v1.60 final
  // extra hint if over resizing rect on focused plant in select/drag mode
  if (cursorModeForDrawing = kCursorModeSelectDrag)
    and (domain.options.showLongHintsForButtons)
    and (domain.options.showSelectionRectangle)
    and (plant <> nil)
    and (plant = self.focusedPlant)
    and (plant.pointIsInResizingRect(aPoint)) then
    result := result + ': Click here and drag up or down to resize all selected plants.';
  end;

{ -------------------------------------------------------------------------------- *popup menu commands }
procedure TMainForm.PopupMenuCutClick(Sender: TObject);
  begin
  self.MenuEditCutClick(self);
  end;

procedure TMainForm.PopupMenuCopyClick(Sender: TObject);
  begin
  self.MenuEditCopyClick(self);
  end;

procedure TMainForm.PopupMenuPasteClick(Sender: TObject);
  begin
  self.MenuEditPasteClick(self);
  end;

procedure TMainForm.PopupMenuRenameClick(Sender: TObject);
  begin
  self.MenuPlantRenameClick(self);
  end;

procedure TMainForm.PopupMenuRandomizeClick(Sender: TObject);
  begin
  self.MenuPlantRandomizeClick(self);
  end;

procedure TMainForm.PopupMenuHideAllOthersClick(Sender: TObject);
  begin
  self.MenuLayoutHideOthersClick(self);
  end;

procedure TMainForm.PopupMenuBreedClick(Sender: TObject);
  begin
  self.MenuPlantBreedClick(self);
  end;

procedure TMainForm.PopupMenuHideClick(Sender: TObject);
  begin
  self.MenuLayoutHideClick(self);
  end;

procedure TMainForm.PopupMenuShowClick(Sender: TObject);
  begin
  self.MenuLayoutShowClick(self);
  end;

procedure TMainForm.PopupMenuMakeTimeSeriesClick(Sender: TObject);
  begin
  self.MenuPlantMakeTimeSeriesClick(self);
  end;

procedure TMainForm.PopupMenuZeroRotationsClick(Sender: TObject);
  begin
  self.MenuPlantZeroRotationsClick(self);
  end;

procedure TMainForm.PopupMenuAnimateClick(Sender: TObject);
  begin
  self.MenuPlantAnimateClick(self);
  end;

procedure TMainForm.paramPopupMenuExpandAllInSectionClick(Sender: TObject);
  begin
  if self.currentSection <> nil then
    self.collapseOrExpandAllParameterPanelsInCurrentSection(kExpand);
  end;

procedure TMainForm.paramPopupMenuCollapseAllInSectionClick(Sender: TObject);
  begin
  if self.currentSection <> nil then
    self.collapseOrExpandAllParameterPanelsInCurrentSection(kCollapse);
  end;

procedure TMainForm.sectionPopupMenuHelpClick(Sender: TObject);
  var
    section: PdSection;
    helpID: string;
  begin
  section := self.currentSection;
  if section = nil then exit;
  helpID := self.sectionHelpIDForSectionName(section.getName);
  if helpID <> '' then
    application.helpJump(helpID);
  end;

procedure TMainForm.paramPopupMenuCopyNameClick(Sender: TObject);  // new v1.4
  var textToCopy, newText: string;
  begin
  if self.selectedParameterPanel = nil then exit;
  if self.currentSection <> nil then
    textToCopy := currentSection.getName + ': '
  else
    textToCopy := '';
  textToCopy := textToCopy + selectedParameterPanel.caption;
  // v2.1 deal with orthogonal sections
  if found('[', textToCopy) then
    begin
    newText := stringUpTo(stringBeyond(textToCopy, '['), ']');
    newText := newText + ': ' + trim(stringUpTo(stringBeyond(textToCopy, ':'), '['));
    textToCopy := newText;
    end;
  Clipboard.asText := textToCopy;
  end;

procedure TMainForm.paramPopupMenuHelpClick(Sender: TObject);
  var
    helpID: string;
  begin
  helpID := self.paramHelpIDForParamPanel(self.selectedParameterPanel);
  if helpID <> '' then
    application.helpJump(helpID);
  end;

procedure TMainForm.paramPopupMenuExpandClick(Sender: TObject);
  begin
  if self.selectedParameterPanel <> nil then
    begin
    self.selectedParameterPanel.expand;
    self.repositionParameterPanels;
    end;
  end;

procedure TMainForm.paramPopupMenuCollapseClick(Sender: TObject);
  begin
  if self.selectedParameterPanel <> nil then
    begin
    self.selectedParameterPanel.collapse;
    self.repositionParameterPanels;
    end;
  end;

{ ------------------------------------------------------------------------------------ *toolbar }
procedure TMainForm.dragCursorModeClick(Sender: TObject);
  begin
  drawingPaintBox.cursor := crArrow;
  self.cursorModeForDrawing := kCursorModeSelectDrag;
  if domain.options.showSelectionRectangle then
    self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.magnifyCursorModeClick(Sender: TObject);
  begin
  drawingPaintBox.cursor := crMagPlus;
  self.cursorModeForDrawing := kCursorModeMagnify;
  if domain.options.showSelectionRectangle then
    self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.posingSelectionCursorModeClick(Sender: TObject);
  begin
  tabSet.tabIndex := kTabPosing;
  drawingPaintBox.cursor := crPosingSelect;
  self.cursorModeForDrawing := kCursorModePosingSelect;
  if domain.options.showSelectionRectangle then
    self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.scrollCursorModeClick(Sender: TObject);
  begin
  drawingPaintBox.cursor := crScroll;
  self.cursorModeForDrawing := kCursorModeScroll;
  if domain.options.showSelectionRectangle then
    self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.rotateCursorModeClick(Sender: TObject);
  begin
  drawingPaintBox.cursor := crRotate;
  self.cursorModeForDrawing := kCursorModeRotate;
  if domain.options.showSelectionRectangle then
    self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.centerDrawingClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdCenterDrawingCommand.create;
  self.doCommand(newCommand);
  end;

procedure TMainForm.magnificationPercentClick(Sender: TObject);
  var newScale: single;
  begin
  newScale := self.magnifyScaleForText(magnificationPercent.text);
  if (newScale <> domain.plantDrawScale_PixelsPerMm) then
    self.changeMagnificationWithoutClick;
  end;

procedure TMainForm.magnificationPercentExit(Sender: TObject);
  var newScale: single;
  begin
  newScale := self.magnifyScaleForText(magnificationPercent.text);
  if (newScale <> domain.plantDrawScale_PixelsPerMm) then
    self.changeMagnificationWithoutClick;
  end;

procedure TMainForm.magnifyPlusClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdChangeMagnificationCommand.createWithNewScaleAndPoint(
      domain.plantDrawScale_PixelsPerMm * 1.5,
      Point(drawingPaintBox.width div 2, drawingPaintBox.height div 2));
  self.doCommand(newCommand);
  end;

procedure TMainForm.magnifyMinusClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  newCommand := PdChangeMagnificationCommand.createWithNewScaleAndPoint(
      domain.plantDrawScale_PixelsPerMm * 0.75,
      Point(drawingPaintBox.width div 2, drawingPaintBox.height div 2));
  self.doCommand(newCommand);
  end;

procedure TMainForm.changeMagnificationWithoutClick;
  var
    newCommand: PdCommand;
  begin
  newCommand := PdChangeMagnificationCommand.createWithNewScaleAndPoint(
      self.magnifyScaleForText(magnificationPercent.text),
      Point(drawingPaintBox.width div 2, drawingPaintBox.height div 2));
  self.doCommand(newCommand);
  end;

function TMainForm.magnifyScaleForText(aText: string): single;
  var intResult, oldIntResult: integer;
  begin
  result := 1.0;
  try
    oldIntResult := round(domain.plantDrawScale_PixelsPerMm * 100.0);
    intResult := strToIntDef(stringUpTo(aText, '%'), -1);
    if (intResult <= 0) then
      begin
      intResult := oldIntResult;
      magnificationPercent.text := intToStr(intResult) + '%';
      end;
    if intResult > kMaxMagnificationToTypeIn then
      begin
      intResult := kMaxMagnificationToTypeIn;
      magnificationPercent.text := intToStr(intResult) + '%';
      end;
    result := intResult / 100.0;
  except
    result := 1.0;
  end;
  end;

function TMainForm.magnifyOrReduce(newScale_PixelsPerMm: single; point_pixels: TPoint; drawNow: boolean): TPoint;
  var
    oldOffset_mm, pointInOldScale_mm, pointInNewScale_mm, newOffset_mm: SinglePoint;
    oldScale_PixelsPerMm: single;
  begin
  self.recalculateAllPlantBoundsRects(kDontDrawYet);
  oldScale_PixelsPerMm := domain.plantDrawScale_PixelsPerMm;
  oldOffset_mm := domain.plantDrawOffset_mm;
  pointInOldScale_mm := setSinglePoint(round(point_pixels.x / oldScale_PixelsPerMm),
      round(point_pixels.y / oldScale_PixelsPerMm));
  pointInNewScale_mm := setSinglePoint(round(point_pixels.x / newScale_PixelsPerMm),
      round(point_pixels.y / newScale_PixelsPerMm));
  newOffset_mm := setSinglePoint(oldOffset_mm.x + pointInNewScale_mm.x - pointInOldScale_mm.x,
    oldOffset_mm.y + pointInNewScale_mm.y - pointInOldScale_mm.y);
  domain.plantManager.plantDrawScale_PixelsPerMm := round(newScale_PixelsPerMm * 100.0) / 100.0;
  domain.plantManager.plantDrawOffset_mm := newOffset_mm;
  if drawNow then
    self.redrawEverything;
  magnificationPercent.text := intToStr(round(domain.plantDrawScale_PixelsPerMm * 100.0)) + '%';
  end;

function TMainForm.upperLeftMostPlantBoundsRectPoint_mm: TPoint;
  var
	  plant: PdPlant;
    i: smallint;
    topLeft_mm: TPoint;
    initialized: boolean;
	begin
  result := Point(0, 0);
  initialized := false;
  if plants.count > 0 then for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    if plant.hidden then continue;
    with domain do
      begin
      topLeft_mm.x := round(plant.boundsRect_pixels.left / plantDrawScale_PixelsPerMm - plantDrawOffset_mm.x);
      topLeft_mm.y := round(plant.boundsRect_pixels.top / plantDrawScale_PixelsPerMm - plantDrawOffset_mm.y);
      end;
    if not initialized then
      begin
      result := topLeft_mm;
      initialized := true;
      end
    else
      begin
      if (topLeft_mm.x < result.x) then result.x := topLeft_mm.x;
      if (topLeft_mm.y < result.y) then result.y := topLeft_mm.y;
      end;
    end;
  end;

function TMainForm.lowerRightMostPlantBoundsRectPoint_mm: TPoint;
  var
	  plant: PdPlant;
    i: smallint;
    bottomRight_mm: TPoint;
    initialized: boolean;
	begin
  result := Point(0, 0);
  initialized := false;
  if plants.count > 0 then for i := 0 to plants.count - 1 do
    begin
    plant := PdPlant(plants.items[i]);
    if plant.hidden then continue;
    with domain do
      begin
      bottomRight_mm.x := round(plant.boundsRect_pixels.right / plantDrawScale_PixelsPerMm - plantDrawOffset_mm.x);
      bottomRight_mm.y := round(plant.boundsRect_pixels.bottom / plantDrawScale_PixelsPerMm - plantDrawOffset_mm.y);
      end;
    if not initialized then
      begin
      result := bottomRight_mm;
      initialized := true;
      end
    else
      begin
      if (bottomRight_mm.x > result.x) then result.x := bottomRight_mm.x;
      if (bottomRight_mm.y > result.y) then result.y := bottomRight_mm.y;
      end;
    end;
  end;

procedure TMainForm.xLocationEditExit(Sender: TObject);
  var
    increment, oldXLocation, newXLocation: integer;
    direction: smallint;
  begin
  if focusedPlant = nil then exit;
  oldXLocation := focusedPlant.basePoint_pixels.x;
  newXLocation := strToIntDef(xLocationEdit.text, oldXLocation);
  if newXLocation <> oldXLocation then
    begin
    increment := newXLocation - oldXLocation;
    if increment > 0 then direction := kRight else direction := kLeft;
    self.nudgeSelectedPlantsByPixelsAndDirection(increment, direction);
    end
  end;

procedure TMainForm.yLocationEditExit(Sender: TObject);
  var
    increment, oldYLocation, newYLocation: integer;
    direction: smallint;
  begin
  if focusedPlant = nil then exit;
  oldYLocation := focusedPlant.basePoint_pixels.y;
  newYLocation := strToIntDef(yLocationEdit.text, oldYLocation);
  if newYLocation <> oldYLocation then
    begin
    increment := newYLocation - oldYLocation;
    if increment > 0 then direction := kDown else direction := kUp;
    self.nudgeSelectedPlantsByPixelsAndDirection(increment, direction);
    end
  end;

procedure TMainForm.xLocationSpinDownClick(Sender: TObject);
  begin
  self.nudgeSelectedPlantsByPixelsAndDirection(domain.options.nudgeDistance, kLeft);
  end;

procedure TMainForm.xLocationSpinUpClick(Sender: TObject);
  begin
  self.nudgeSelectedPlantsByPixelsAndDirection(domain.options.nudgeDistance, kRight);
  end;

procedure TMainForm.yLocationSpinDownClick(Sender: TObject);
  begin
  self.nudgeSelectedPlantsByPixelsAndDirection(domain.options.nudgeDistance, kUp);
  end;

procedure TMainForm.yLocationSpinUpClick(Sender: TObject);
  begin
  self.nudgeSelectedPlantsByPixelsAndDirection(domain.options.nudgeDistance, kDown);
  end;

procedure TMainForm.xRotationEditChange(Sender: TObject);
  begin
  self.checkRotationEditAgainstBounds(xRotationEdit);
  end;

procedure TMainForm.yRotationEditChange(Sender: TObject);
  begin
  self.checkRotationEditAgainstBounds(yRotationEdit);
  end;

procedure TMainForm.zRotationEditChange(Sender: TObject);
  begin
  self.checkRotationEditAgainstBounds(zRotationEdit);
  end;

procedure TMainForm.checkRotationEditAgainstBounds(edit: TEdit);
  var
    newRotation, oldRotation: smallint;
  begin
  if internalChange then exit;
  newRotation := strToIntDef(edit.text, 0);
  oldRotation := newRotation;
  if newRotation < -360 then newRotation := 360 - (abs(newRotation) - 360);
  if newRotation > 360 then newRotation := -360 + (newRotation - 360);
  if newRotation <> oldRotation then
    begin
    internalChange := true;
    edit.text := intToStr(newRotation);
    internalChange := false;
    end;
  end;

procedure TMainForm.xRotationEditExit(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(xRotationEdit, kRotateX, 0);
  end;

procedure TMainForm.xRotationSpinUpClick(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(xRotationEdit, kRotateX, domain.options.rotationIncrement);
  end;

procedure TMainForm.xRotationSpinDownClick(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(xRotationEdit, kRotateX, -domain.options.rotationIncrement);
  end;

procedure TMainForm.yRotationEditExit(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(yRotationEdit, kRotateY, 0);
  end;

procedure TMainForm.yRotationSpinUpClick(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(yRotationEdit, kRotateY, domain.options.rotationIncrement);
  end;

procedure TMainForm.yRotationSpinDownClick(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(yRotationEdit, kRotateY, -domain.options.rotationIncrement);
  end;

procedure TMainForm.zRotationEditExit(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(zRotationEdit, kRotateZ, 0);
  end;

procedure TMainForm.zRotationSpinUpClick(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(zRotationEdit, kRotateZ, domain.options.rotationIncrement);
  end;

procedure TMainForm.zRotationSpinDownClick(Sender: TObject);
  begin
  self.changeSelectedPlantRotations(zRotationEdit, kRotateZ, -domain.options.rotationIncrement);
  end;

procedure TMainForm.changeSelectedPlantRotations(edit: TEdit; rotateDirection, changeInRotation: smallint);
  var
    newRotation: smallint;
    newCommand: PdCommand;
  begin
  if internalChange then exit;
  newRotation := strToIntDef(edit.text, 0) + changeInRotation;
  edit.text := intToStr(newRotation);
  self.checkRotationEditAgainstBounds(edit); { need this? }
  newRotation := strToIntDef(edit.text, 0);  { in case changed }
  if self.focusedPlant = nil then exit; {should be disabled, but}
  newCommand := PdRotateCommand.createWithListOfPlantsDirectionAndNewRotation(selectedPlants, rotateDirection,
    newRotation);
  self.doCommand(newCommand);
  end;

procedure TMainForm.resetRotationsClick(Sender: TObject);
  var
    newCommand: PdCommand;
    i: smallint;
    plant: PdPlant;
    allRotationsAreZero: boolean;
	begin
  if selectedPlants.count <= 0 then exit;
  { don't do if none of the selected plants have rotations other than zero }
  allRotationsAreZero := true;
  for i := 0 to selectedPlants.count - 1 do
      begin
      plant := PdPlant(selectedPlants.items[i]);
      if (plant.xRotation <> 0) or (plant.yRotation <> 0) or (plant.zRotation <> 0) then
        begin
        allRotationsAreZero := false;
        break;
        end;
      end;
  if allRotationsAreZero then exit;
  newCommand := PdResetRotationsCommand.createWithListOfPlants(selectedPlants);
  self.doCommand(newCommand);
  end;

procedure TMainForm.drawingScaleEditExit(Sender: TObject);
  var oldValue, newValue: single;
  begin
  if self.focusedPlant = nil then exit;
  oldValue := self.focusedPlant.drawingScale_pixelsPerMm;
  try
    newValue := strToFloat(drawingScaleEdit.text);
  except
    newValue := oldValue;
  end;
  if newValue <> oldValue then
    self.resizeSelectedPlantsWithMultiplierOrNewAmount(0, newValue);
  end;

procedure TMainForm.drawingScaleSpinUpClick(Sender: TObject);
  var resizeMultiplier: single;
  begin
  if self.focusedPlant = nil then exit;
  resizeMultiplier := domain.options.resizeKeyUpMultiplierPercent / 100.0;
  self.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0);
  end;

procedure TMainForm.drawingScaleSpinDownClick(Sender: TObject);
  var resizeMultiplier: single;
  begin
  if self.focusedPlant = nil then exit;
  resizeMultiplier := safedivExcept(1.0, domain.options.resizeKeyUpMultiplierPercent / 100.0, 0.9);
  self.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0);
  end;

procedure TMainForm.makeEqualWidthClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdResizePlantsToSameWidthOrHeightCommand.createWithListOfPlantsAndNewWidthOrHeight(self.selectedPlants,
    rWidth(focusedPlant.boundsRect_pixels), 0, kChangeWidth);
  self.doCommand(newCommand);
  end;

procedure TMainForm.makeEqualHeightClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdResizePlantsToSameWidthOrHeightCommand.createWithListOfPlantsAndNewWidthOrHeight(self.selectedPlants,
    0, rHeight(focusedPlant.boundsRect_pixels), kChangeHeight);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutSizeSameWidthClick(Sender: TObject);
  begin
  self.makeEqualWidthClick(self);
  end;

procedure TMainForm.MenuLayoutSizeSameHeightClick(Sender: TObject);
  begin
  self.makeEqualHeightClick(self);
  end;

procedure TMainForm.alignTopsClick(Sender: TObject);
  begin
  self.alignSelectedPlants(kUp);
  end;

procedure TMainForm.alignBottomsClick(Sender: TObject);
  begin
  self.alignSelectedPlants(kDown);
  end;

procedure TMainForm.alignLeftClick(Sender: TObject);
  begin
  self.alignSelectedPlants(kLeft);
  end;

procedure TMainForm.alignRightClick(Sender: TObject);
  begin
  self.alignSelectedPlants(kRight);
  end;

procedure TMainForm.alignSelectedPlants(alignDirection: smallint);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 1 then exit;
  newCommand := PdAlignPlantsCommand.createWithListOfPlantsRectAndDirection(self.selectedPlants,
      focusedPlant.boundsRect_pixels, alignDirection);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutAlignTopsClick(Sender: TObject);
  begin
  self.alignTopsClick(self);
  end;

procedure TMainForm.MenuLayoutAlignBottomsClick(Sender: TObject);
  begin
  self.alignBottomsClick(self);
  end;

procedure TMainForm.MenuLayoutAlignLeftSidesClick(Sender: TObject);
  begin
  self.alignLeftClick(self);
  end;

procedure TMainForm.MenuLayoutAlignRightSidesClick(Sender: TObject);
  begin
  self.alignRightClick(self);
  end;

procedure TMainForm.packPlantsClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 1 then exit;
  newCommand := PdPackPlantsCommand.createWithListOfPlantsAndFocusRect(self.selectedPlants,
      focusedPlant.boundsRect_pixels);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuLayoutPackClick(Sender: TObject);
  begin
  self.packPlantsClick(self);
  end;

procedure TMainForm.FormKeyDown(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  { pressing any key will stop animation }
  if animateTimer.enabled then
    begin
    key := 0;
    self.stopAnimation;
    end;
  { hold down control and shift and press arrow keys - resize current plants }
  if (ssCtrl in shift) and (ssShift in shift) then
    begin
    if (key = VK_LEFT) or (key = VK_RIGHT) or (key = VK_UP) or (KEY = VK_DOWN) then
      begin
      self.resizeSelectedPlantsByKey(key);
      key := 0;
      end;
    end
  { hold down control and press arrow keys - shift current plants }
  else if (ssCtrl in shift) then
    begin
    if (key = VK_LEFT) or (key = VK_RIGHT) or (key = VK_UP) or (KEY = VK_DOWN) then
      begin
      self.nudgeSelectedPlantsByKey(key);
      key := 0;
      end
    end
  { hold down shift - do magnification as minus }
  else if (key = VK_Shift) then
    begin
    if cursorModeForDrawing = kCursorModeMagnify then
      drawingPaintBox.cursor := crMagMinus;
    end;
  end;

procedure TMainForm.nudgeSelectedPlantsByKey(key: word);
  var
    direction: smallint;
  begin
  if selectedPlants.count <= 0 then exit;
  case key of
    VK_LEFT: direction := kLeft;
    VK_RIGHT: direction := kRight;
    VK_UP: direction := kUp;
    VK_DOWN: direction := kDown;
    else
      exit;
    end;
  self.nudgeSelectedPlantsByPixelsAndDirection(domain.options.nudgeDistance, direction);
  end;

procedure TMainForm.nudgeSelectedPlantsByPixelsAndDirection(pixels: integer; direction: smallint);
  var
    newCommand: PdCommand;
    movePoint: TPoint;
  begin
  if selectedPlants.count <= 0 then exit;
  movePoint := Point(0, 0);
  case direction of
    kUp: movePoint.y := -pixels;
    kDown: movePoint.y := pixels;
    kLeft: movePoint.x := -pixels;
    kRight: movePoint.x := pixels;
    end;
  newCommand := PdDragCommand.createWithListOfPlantsAndDragOffset(self.selectedPlants, movePoint);
  self.doCommand(newCommand);
  end;

procedure TMainForm.resizeSelectedPlantsByKey(key: word);
  var
    resizeMultiplier: single;
  begin
  if selectedPlants.count <= 0 then exit;
  if (key = VK_LEFT) or (key = VK_UP) then
    resizeMultiplier := domain.options.resizeKeyUpMultiplierPercent / 100.0
  else if (key = VK_RIGHT) or (key = VK_DOWN) then
    resizeMultiplier := safedivExcept(1.0, domain.options.resizeKeyUpMultiplierPercent / 100.0, 0.9)
  else
    exit;
  self.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0);
  end;

procedure TMainForm.resizeSelectedPlantsWithMultiplierOrNewAmount(multiplier, newAmount_pixelsPerMm: single);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  if multiplier <> 0 then
    newCommand := PdResizePlantsCommand.createWithListOfPlantsAndMultiplier(self.selectedPlants, multiplier)
  else
    newCommand := PdResizePlantsCommand.createWithListOfPlantsAndNewValue(self.selectedPlants, newAmount_pixelsPerMm);
  self.doCommand(newCommand);
  end;

procedure TMainForm.FormKeyPress(Sender: TObject; var Key: Char);
  begin
  makeEnterWorkAsTab(self, activeControl, key);
  { pressing any key will stop animation }
  if animateTimer.enabled then
    begin
    key := chr(0);
    self.stopAnimation;
    end;
  end;

procedure TMainForm.FormKeyUp(Sender: TObject; var Key: Word; Shift: TShiftState);
  begin
  { pressing any key will stop animation }
  if animateTimer.enabled then
    begin
    key := 0;
    self.stopAnimation;
    end;
  { let up shift or control - go back to plus magnification }
  if (key = VK_Shift) then
    begin
    if cursorModeForDrawing = kCursorModeMagnify then
      drawingPaintBox.cursor := crMagPlus;
    end;
  end;

{ ------------------------------------------------------------------------------------ *tab set }
function TMainForm.lifeCycleShowing: boolean;
  begin
  result := (tabSet.tabIndex = kTabLifeCycle);
  end;

function TMainForm.rotationsShowing: boolean;
  begin
  result := (tabSet.tabIndex = kTabRotations);
  end;

function TMainForm.parametersShowing: boolean;
  begin
  result := (tabSet.tabIndex = kTabParameters);
  end;

function TMainForm.statsShowing: boolean;
  begin
  result := (tabSet.tabIndex = kTabStatistics);
  end;

function TMainForm.noteShowing: boolean;
  begin
  result := (tabSet.tabIndex = kTabNote);
  end;

function TMainForm.posingShowing: boolean;
  begin
  result := (tabSet.tabIndex = kTabPosing);
  end;

procedure TMainForm.tabSetChange(Sender: TObject; NewTab: Integer; var AllowChange: Boolean);
  begin
  lifeCyclePanel.visible := (newTab = kTabLifeCycle);
  rotationsPanel.visible := (newTab = kTabRotations);
  parametersPanel.visible := (newTab = kTabParameters);
  statsScrollBox.visible := (newTab = kTabStatistics);
  notePanel.visible := (newTab = kTabNote);
  posingPanel.visible := (newTab = kTabPosing);
  self.updateRightSidePanelForFirstSelectedPlantWithTab(newTab);
  end;

procedure TMainForm.updateRightSidePanelForFirstSelectedPlant;
  begin
  { set tab font colors - pay attention to multiple selections }
  // v2.0 removed this
//  tabSet.font.color := self.textColorToRepresentPlantSelection(true);
//  tabSet.invalidate;
  self.updateRightSidePanelForFirstSelectedPlantWithTab(tabSet.tabIndex);
  end;

procedure TMainForm.updateRightSidePanelForFirstSelectedPlantWithTab(newTab: integer);
  begin
  case newTab of
    kTabLifeCycle: self.updateLifeCyclePanelForFirstSelectedPlant;
    kTabRotations: self.updateRotationsPanelForFirstSelectedPlant;
    kTabParameters: self.updateParametersPanelForFirstSelectedPlant;
    kTabStatistics: self.updateStatisticsPanelForFirstSelectedPlant;
    kTabNote: self.updateNoteForFirstSelectedPlant;
    kTabPosing: self.updatePosingForFirstSelectedPlant;
    end;
  end;

function TMainForm.textColorToRepresentPlantSelection(payAttentionToMultiSelect: boolean): TColorRef;
  begin
  if self.focusedPlant <> nil then
    begin
    if payAttentionToMultiSelect then
      begin
      if selectedPlants.count <= 1 then
        result := clBtnText
      else
        result := clBlue;  // v2.0  was clRed
      end
    else
      result := clBtnText;
    end
  else
    result := clGray;
  end;

procedure TMainForm.updateForChangeToPlantRotations;
  var
    firstPlant: PdPlant;
  begin
  firstPlant := self.focusedPlant;
  if firstPlant <> nil then
    begin
    xRotationEdit.text := intToStr(round(firstPlant.xRotation));
    yRotationEdit.text := intToStr(round(firstPlant.yRotation));
    zRotationEdit.text := intToStr(round(firstPlant.zRotation));
    end
  else
    begin
    xRotationEdit.text := '';
    yRotationEdit.text := '';
    zRotationEdit.text := '';
    end;
  xRotationEdit.refresh;
  yRotationEdit.refresh;
  zRotationEdit.refresh;
  end;

procedure TMainForm.updateForChangeToSelectedPlantsDrawingScale;
  var
    firstPlant: PdPlant;
  begin
  firstPlant := self.focusedPlant;
  if firstPlant <> nil then
    drawingScaleEdit.text := digitValueString(firstPlant.drawingScale_pixelsPerMm)
  else
    drawingScaleEdit.text := '';
  drawingScaleEdit.refresh;
  end;

procedure TMainForm.updateForChangeToSelectedPlantsLocation;
  var
    firstPlant: PdPlant;
  begin
  firstPlant := self.focusedPlant;
  if firstPlant <> nil then
    begin
    xLocationEdit.text := digitValueString(firstPlant.basePoint_pixels.x);
    yLocationEdit.text := digitValueString(firstPlant.basePoint_pixels.y);
    end
  else
    begin
    xLocationEdit.text := '';
    yLocationEdit.text := '';
    end;
  xLocationEdit.refresh;
  yLocationEdit.refresh;
  end;

{ ------------------------------------------------------- *life cycle panel drawing and mouse handling }
procedure TMainForm.updateLifeCyclePanelForFirstSelectedPlant;
  var
    firstPlant: PdPlant;
  begin
  self.updatePlantNameLabel(kTabLifeCycle);
  firstPlant := self.focusedPlant;
  lifeCycleDaysEdit.enabled := firstPlant <> nil;
  lifeCycleDaysSpin.enabled := firstPlant <> nil;
  lifeCycleDragger.enabled := firstPlant <> nil;
  animateGrowth.enabled := firstPlant <> nil;
  timeLabel.font.color := self.textColorToRepresentPlantSelection(false);
  maxSizeAxisLabel.font.color := timeLabel.font.color;
  ageAndSizeLabel.font.color := timeLabel.font.color;
  daysAndSizeLabel.font.color := timeLabel.font.color;
  if firstPlant <> nil then {special case}
    lifeCycleDragger.color := clRed
  else
    lifeCycleDragger.color := clGray;
  { reset red dragger panel }
  self.placeLifeCycleDragger;
  { set life cycle days in edit }
  if firstPlant <> nil then
    lifeCycleDaysEdit.text := intToStr(firstPlant.age)
  else
    lifeCycleDaysEdit.text := '0';
  { set % size label}
  if firstPlant <> nil then
    daysAndSizeLabel.caption := 'days, ' + intToStr(round(firstPlant.totalBiomass_pctMPB)) + '% max size'
  else
    daysAndSizeLabel.caption := '';
  self.placeLifeCycleDragger;
  self.redrawLifeCycleGraph;
  end;

procedure TMainForm.updatePlantNameLabel(tabIndex: smallint);
  var
    firstPlant: PdPlant;
    labelToChange: TLabel;
    payAttentionToOtherPlants: boolean;
    prefix: string;
    handlingDifferently: boolean;
  begin
  firstPlant := self.focusedPlant;
  payAttentionToOtherPlants := true;
  handlingDifferently := false;
  prefix := '';
  labelToChange := nil;
  case tabIndex of
    kTabRotations:
      begin
      labelToChange := arrangementPlantName;
      prefix := 'Arrangement for ';
      end;
    kTabParameters:
      begin
      labelToChange := parametersPlantName;
      prefix := 'Parameters for ';
      end;
    kTabLifeCycle:
      begin
      labelToChange := selectedPlantNameLabel;
      prefix := 'Life cycle for ';
      end;
    kTabPosing:
      begin
      labelToChange := posingPlantName;
      payAttentionToOtherPlants := false;
      prefix := 'Posing for ';
      end;
    kTabStatistics:
      begin
      handlingDifferently := true;
      statsPanel.updatePlant(firstPlant);
      end;
    kTabNote:
      begin
      labelToChange := noteLabel;
      payAttentionToOtherPlants := false;
      prefix := 'Note for ';
      end;
    end;
  if (handlingDifferently) or (labelToChange = nil) then exit;
  if firstPlant <> nil then
    begin
    labelToChange.caption := prefix + firstPlant.getName;
    if (payAttentionToOtherPlants) and (selectedPlants.count > 1) then
      labelToChange.caption := labelToChange.caption  + ' (and other plants)';
    end
  else
    labelToChange.caption := '(no plants selected)';
  labelToChange.font.color := self.textColorToRepresentPlantSelection(payAttentionToOtherPlants);
  end;

procedure TMainForm.animateGrowthClick(Sender: TObject);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdAnimatePlantCommand.createWithListOfPlants(selectedPlants);
  self.doCommand(newCommand);
  end;

procedure TMainForm.MenuPlantAnimateClick(Sender: TObject);
  begin
  self.animateGrowthClick(self);
  end;

procedure TMainForm.startAnimation;
  begin
  { called by animate command, which also sets up the pointer for the timer to call }
  { disable all non-modal forms }
  self.activeControl := plantListDrawGrid; // keeps space bar from affecting magnification
  self.enableOrDisableAllForms(kDisableAllForms);
  { add warning about disabled forms }
  animatingLabel.visible := true;
  tabSet.visible := false;
  { start timer }
  animateTimer.enabled := true;
  end;

procedure TMainForm.animateTimerTimer(Sender: TObject);
  begin
  if self.animateCommand <> nil then
    PdAnimatePlantCommand(animateCommand).animateOneDay;
  end;

procedure TMainForm.stopAnimation;
  begin
  { called by animate command or self (if user clicks in drawing area or presses a key) }
  { stop timer }
  animateTimer.enabled := false;
  { nil out pointer }
  animateCommand := nil;
  { re-enable everything }
  self.enableOrDisableAllForms(kEnableAllForms);
  { remove warning about disabled forms }
  animatingLabel.visible := false;
  tabSet.visible := true;
  { if there were selection rectangles before, put them back }
  if domain.options.showSelectionRectangle then
    self.copyDrawingBitmapToPaintBox;
  end;

procedure TMainForm.enableOrDisableAllForms(enable: boolean);
  begin
  { cfk note: put any new NON-MODAL forms here }
  self.enabled := enable;
  BreederForm.enabled := enable;
  TimeSeriesForm.enabled := enable;
  DebugForm.enabled := enable;
  end;

procedure TMainForm.lifeCycleDaysEditExit(Sender: TObject);
  var
    newAge: smallint;
    plant: PdPlant;
  begin
  plant := self.focusedPlant;
  if plant = nil then exit;
  newAge := strToIntDef(lifeCycleDaysEdit.text, 0);
  if newAge = plant.age then exit;
  if newAge > plant.pGeneral.ageAtMaturity then
    begin
    newAge := self.focusedPlant.pGeneral.ageAtMaturity;
    lifeCycleDaysEdit.text := intToStr(newAge);
    end;
  self.changeSelectedPlantAges(newAge);
  end;

procedure TMainForm.lifeCycleDaysSpinUpClick(Sender: TObject);
  var
    newAge: smallint;
  begin
  if self.focusedPlant = nil then exit;
  newAge := intMin(strToIntDef(lifeCycleDaysEdit.text, 0) + 1, self.focusedPlant.pGeneral.ageAtMaturity);
  newAge := intMax(0, newAge);
  lifeCycleDaysEdit.text := intToStr(newAge);
  self.changeSelectedPlantAges(newAge);
  end;

procedure TMainForm.lifeCycleDaysSpinDownClick(Sender: TObject);
  var
    newAge: smallint;
  begin
  if self.focusedPlant = nil then exit;
  newAge := intMin(strToIntDef(lifeCycleDaysEdit.text, 0) - 1, self.focusedPlant.pGeneral.ageAtMaturity);
  newAge := intMax(0, newAge);
  lifeCycleDaysEdit.text := intToStr(newAge);
  self.changeSelectedPlantAges(newAge);
  end;

procedure TMainForm.lifeCycleDraggerMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  if self.focusedPlant <> nil then
    begin
    self.lifeCycleDragging := true;
    self.lifeCycleDraggingStartPos := x;
    self.lifeCycleDraggingLastDrawPos := -1;
    self.lifeCycleDraggingNeedToRedraw := true;
    end;
  end;

procedure TMainForm.lifeCycleDraggerMouseMove(Sender: TObject;
  Shift: TShiftState; X, Y: Integer);
  begin
  if lifeCycleDragging and
    (lifeCycleDragger.left + x >= lifeCycleGraphImage.left)
      and (lifeCycleDragger.left + x < lifeCycleGraphImage.left + lifeCycleGraphImage.width) then
      begin
      self.undrawLifeCycleDraggerLine;
      self.lifeCycleDraggingLastDrawPos := self.drawLifeCycleDraggerLine(x);
      end;
  end;

procedure TMainForm.lifeCycleDraggerMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    firstPlant: PdPlant;
    newAge: smallint;
  begin
  if lifeCycleDragging then
    begin
    self.undrawLifeCycleDraggerLine;
    lifeCycleDragger.left := lifeCycleDragger.left - (lifeCycleDraggingStartPos - x);
    if lifeCycleDragger.left < lifeCycleGraphImage.left then
      lifeCycleDragger.left := lifeCycleGraphImage.left;
    if lifeCycleDragger.left + lifeCycleDragger.width > lifeCycleGraphImage.left + lifeCycleGraphImage.width then
      lifeCycleDragger.left := lifeCycleGraphImage.left + lifeCycleGraphImage.width - lifeCycleDragger.width;
    firstPlant := self.focusedPlant;
    if firstPlant = nil then
      raise Exception.create('Problem: First plant is nil during drag in method TMainForm.lifeCycleDraggerMouseUp.');
    if (lifeCycleGraphImage.width - lifeCycleDragger.width) <> 0 then
      newAge := round(firstPlant.pGeneral.ageAtMaturity *
        (lifeCycleDragger.left -  lifeCycleGraphImage.left) / (lifeCycleGraphImage.width - lifeCycleDragger.width))
    else
      newAge := 0;
    self.changeSelectedPlantAges(newAge);
  	self.resizePanelsToVerticalSplitter;
    self.lifeCycleDragging := false;
    end;
  end;

function TMainForm.drawLifeCycleDraggerLine(pos: integer): integer;
  var
    theDC: HDC;
  begin
  theDC := getDC(0);
  result := self.clientOrigin.x + plantFocusPanel.left + lifeCyclePanel.left + lifeCycleDragger.left + pos + 2;
  patBlt(theDC, result, self.clientOrigin.y + plantFocusPanel.top + lifeCyclePanel.top + lifeCycleDragger.top, 1,
      lifeCycleDragger.height, dstInvert);
  releaseDC(0, theDC);
  self.lifeCycleDraggingNeedToRedraw := true;
  end;

procedure TMainForm.undrawLifeCycleDraggerLine;
  var theDC: HDC;
  begin
  if not self.lifeCycleDraggingNeedToRedraw then exit;
  theDC := getDC(0);
  patBlt(theDC, self.lifeCycleDraggingLastDrawPos,
    self.clientOrigin.y + plantFocusPanel.top + lifeCyclePanel.top + lifeCycleDragger.top, 1,
    lifeCycleDragger.height, dstInvert);
  releaseDC(0, theDC);
  self.lifeCycleDraggingNeedToRedraw := false;
  end;

procedure TMainForm.changeSelectedPlantAges(newAge: smallint);
  var
    newCommand: PdCommand;
  begin
  if selectedPlants.count <= 0 then exit;
  newCommand := PdChangePlantAgeCommand.createWithListOfPlantsAndNewAge(selectedPlants, newAge);
  self.doCommand(newCommand);  
  end;

procedure TMainForm.redrawLifeCycleGraph;
  var
    sCurveError: boolean;
  begin
  with lifeCycleGraphImage do
    begin
    picture.bitmap.canvas.brush.color := clBtnFace;
    picture.bitmap.canvas.rectangle(0, 0, clientWidth, clientHeight);
    self.drawSCurveOrCheckForError(picture.bitmap.canvas, bounds(0, 0, clientWidth, clientHeight), true, sCurveError);
    end;
  if sCurveError and (self.focusedPlant <> nil)
    then
      { error - do something, should be caught by parameter panel }
      // PDF PORT -- put in NIL
      NIL;
  end;

procedure TMainForm.drawSCurveOrCheckForError(aCanvas: TCanvas; aRect: TRect; draw: boolean; var failed: boolean);
  var
    firstPlant: PdPlant;
    i: integer;
    x, y: single;
    thisPoint: TPoint;
    curve: SCurveStructure;
    numPoints: integer;
  begin
  firstPlant := self.focusedPlant;
  if firstPlant = nil then exit;
  failed := true;
  numPoints := 100;
  { assumes that zero does NOT fall between x1 and x2, though one of these could be zero }
  curve.x1 := firstPlant.pGeneral.growthSCurve.x1;
  curve.y1 := firstPlant.pGeneral.growthSCurve.y1;
  curve.x2 := firstPlant.pGeneral.growthSCurve.x2;
  curve.y2 := firstPlant.pGeneral.growthSCurve.y2;
  try
    calcSCurveCoeffsWithResult(curve, failed);
    if failed then exit;
    for i := 0 to numPoints - 1 do
      begin
      x := 0.0; { delphi 2.0 wants this }
      y := 0.0;
      try
        x := 1.0 * i / numPoints;
      except
        exit;
      end;
      y := scurveWithResult(x, curve.c1, curve.c2, failed);
      if failed then exit;
      if draw then
        begin
        thisPoint.x := aRect.left + round(x * (aRect.right - aRect.left));
        thisPoint.y := aRect.top + round((1.0 - y) * (aRect.bottom - aRect.top));
        if i = 0 then
          aCanvas.moveTo(thisPoint.x, thisPoint.y)
        else
          aCanvas.lineTo(thisPoint.x, thisPoint.y);
        end;
      end;
  except
    exit;
  end;                                                 
  failed := false;
  end;

{ ----------------------------------------------------------------------------- *parameters panel }
procedure TMainForm.sectionsComboBoxDrawItem(Control: TWinControl;
  Index: Integer; Rect: TRect; State: TOwnerDrawState);
  var
	  section: PdSection;
    sectionPicture: TPicture;
    selected: boolean;
    textDrawRect: TRect;
    cText: array[0..255] of Char;
  begin
  if Application.terminated then exit;
  if (sectionsComboBox.items.count <= 0) or (index < 0) or (index > sectionsComboBox.items.count - 1) then exit;
  selected := (odSelected in state);
  { set up section pointer }
  section := sectionsComboBox.items.objects[index] as PdSection;
  if section = nil then exit;
   with sectionsComboBox.canvas do
    begin
    brush.style := bsSolid;
    font := sectionsComboBox.font;
    if selected then
      begin
      brush.color := clHighlight;
      font.color := clHighlightText;
      end
    else
      begin
      brush.color := sectionsComboBox.color;
      font.color := clBtnText;
      end;
    fillRect(rect);
    textDrawRect := rect;
    textDrawRect.left := textDrawRect.left + 4;
    textDrawRect.top := textDrawRect.top + (textDrawRect.bottom - textDrawRect.top) div 2 - (textHeight('W') div 2);
    sectionPicture := self.sectionPictureForSectionName(section.getName);
    if sectionPicture <> nil then draw(rect.left + 4, rect.top, sectionPicture.graphic);
    textDrawRect.left := textDrawRect.left + 32 + 4;
    strPCopy(cText, sectionsComboBox.items[index]);
    winprocs.drawText(handle, cText, strLen(cText), textDrawRect, DT_LEFT);
    end;
  end;

procedure TMainForm.sectionsComboBoxChange(Sender: TObject);
  begin
  if Application.terminated then exit;
  self.updateParameterPanelsForSectionChange;
  self.updateSectionPopupMenuForSectionChange;
  end;

procedure TMainForm.loadSectionsIntoListBox;
  var
    section: PdSection;
    i, indexOfPrimaryInflors: smallint;
  begin
  if (domain = nil) or (domain.sectionManager = nil) then exit;
  sectionsComboBox.clear;
  if domain.sectionManager.sections.count > 0 then
    for i := 0 to domain.sectionManager.sections.count - 1 do
      begin
      section := PdSection(domain.sectionManager.sections.items[i]);
      if section.showInParametersWindow then
        begin
        // kludge to get around necessary ordering of new advanced floral section
        // advanced floral params are at end of file, but want to show them
        // in the list before inflorescences
        // WATCH OUT: change this code if you change the names of the sections
        if section.name = 'Primary flowers, advanced' then
          begin
          indexOfPrimaryInflors := sectionsComboBox.items.indexOf('Primary inflorescences');
          sectionsComboBox.items.insertObject(indexOfPrimaryInflors, section.name, section);
          end
        else
          sectionsComboBox.items.addObject(section.name, section);
        end;
      end;
  // v2.1 add orthogonal sections
  if domain.sectionManager.orthogonalSections.count > 0 then
    for i := 0 to domain.sectionManager.orthogonalSections.count - 1 do
      begin
      section := PdSection(domain.sectionManager.orthogonalSections.items[i]);
      if section.showInParametersWindow then
          sectionsComboBox.items.addObject(section.name, section);
      end;
  end;

function TMainForm.currentSection: PdSection;
  begin
  result := nil;
  with sectionsComboBox do
    begin
    if (items.count <= 0) or (itemIndex < 0) or (itemIndex > items.count - 1) then exit;
    result := PdSection(items.objects[itemIndex]);
    end;
  end;

function TMainForm.sectionPictureForSectionName(aName: string): TPicture;
  var
    image: TImage;
  begin
  result := nil;
  if aName = '(no section)' then exit;
  image := nil;
  aName :=  lowerCase(aName);
  if found('general', aName) then image := Sections_General
  else if found('meris', aName) then image := Sections_Meristems
  else if found('inter', aName) then image := Sections_Internodes
  else if found('seed', aName) then image := Sections_SeedlingLeaves
  else if found('lea', aName) then image := Sections_Leaves {must be below seedling leaves}
  else if found('flow', aName) and found('primary', aName) and found('advanced', aName) then image := Sections_FlowersPrimaryAdvanced
  else if found('flow', aName) and found('primary', aName) then image := Sections_FlowersPrimary
  else if found('inflo', aName) and found('primary', aName) then image := Sections_InflorPrimary
  else if found('fruit', aName) then image := Sections_Fruit
  else if found('flow', aName) and found('secondary', aName) then image := Sections_FlowersSecondary
  else if found('inflo', aName) and found('secondary', aName) then image := Sections_InflorSecondary
  else if found('root', aName) then image := Sections_RootTop
  // v2.1 otherwise assume it is an orthogonal section
  else image := Sections_Orthogonal;
  if image <> nil then
    result := image.picture;
  end;

function TMainForm.sectionHelpIDForSectionName(aName: string): string;
  begin
  result := '';
  if aName = '(no section)' then exit;
  aName :=  lowerCase(aName);
  { trying to be flexible about possible name changes here }
  if found('general', aName) then result := 'General_parameters'
  else if found('meris', aName) then result := 'Meristem_parameters'
  else if found('inter', aName) then result := 'Internode_parameters'
  else if found('first', aName) then result := 'First_leaf_parameters'
  else if found('lea', aName) then result := 'Leaf_parameters' {must be below seedling leaves}
  else if found('advanced', aName) then result := 'Advanced_flower_parameters' // must be above flower params
  else if found('flow', aName) then result := 'Flower_parameters'
  else if found('inflo', aName) then result := 'Inflorescence_parameters'
  else if found('fruit', aName) then result := 'Fruit_parameters'
  else if found('root', aName) then result := 'Root_top_parameters'
  { add more sections here if any are added to the params file }
  // v2.1 otherwise assume it is an orthogonal section
  else result := 'Transverse_parameter_sections';
  end;

procedure TMainForm.updateParameterPanelsForSectionChange;
  var
	  paramPanel, oldParamPanel: PdParameterPanel;
	  section: PdSection;
    parameter: PdParameter;
	  i: smallint;        
  begin
  try
  cursor_startWait;
  { clear out any earlier panels }
  self.selectedParameterPanel := nil;
  if parametersScrollBox.controlCount > 0 then
	  while parametersScrollBox.controlCount > 0 do
  	  begin
      { this is the only valid time to free a component owned by something - after it has
        been removed from the component list (owned objects) of the owner }
      oldParamPanel := PdParameterPanel(parametersScrollBox.controls[0]);
      self.removeComponent(oldParamPanel);
      oldParamPanel.parent := nil;
      oldParamPanel.free;
      end;
  { make new panels for the current section }
  if sectionsComboBox.itemIndex < 0 then exit;
  section := sectionsComboBox.items.objects[sectionsComboBox.itemIndex] as PdSection;
  if section.numSectionItems > 0 then for i := 0 to section.numSectionItems - 1 do
    begin
    parameter := domain.parameterManager.parameterForFieldNumber(section.sectionItems[i]);
    if parameter = nil then continue;
    paramPanel := nil;
    case parameter.fieldType of
      kFieldHeader: paramPanel := PdHeaderParameterPanel.createForParameter(self, parameter);
      kFieldEnumeratedList: paramPanel := PdListParameterPanel.createForParameter(self, parameter);
      kFieldThreeDObject: paramPanel := PdTdoParameterPanel.createForParameter(self, parameter);
      kFieldColor: paramPanel := PdColorParameterPanel.createForParameter(self, parameter);
      kFieldSmallint: paramPanel := PdSmallintParameterPanel.createForParameter(self, parameter);
      kFieldFloat:
        begin
        if parameter.indexCount <= 1 then
          paramPanel := PdRealParameterPanel.createForParameter(self, parameter)
        else if parameter.indexType = kIndexTypeSCurve then
          paramPanel := PdSCurveParameterPanel.createForParameter(self, parameter);
        end;
      kFieldBoolean: paramPanel := PdBooleanParameterPanel.createForParameter(self, parameter);
      else
        raise Exception.create('Problem: Unsupported parameter type in method TMainForm.updateParameterPanelsForSectionChange.');
        { note that the longint type is used to store plant positions, but should not be used
          for parameter panels }
      end;
    if paramPanel <> nil then
      begin
    	paramPanel.parent := parametersScrollBox;
    	paramPanel.tabOrder := {9 +} i;
    	paramPanel.calculateTextDimensions;
    	paramPanel.calculateHeight;
      // v2.1 add original section name to params in orthogonal sections
      if (parameter.originalSectionName <> section.name) and not (paramPanel is PdHeaderParameterPanel) then
        paramPanel.caption := paramPanel.caption + ' [' + parameter.originalSectionName + ']';
      end;
    end;
  self.updateParametersPanelForFirstSelectedPlant;
  self.repositionParameterPanels;
  finally
  cursor_stopWait;
  end;
  end;

function TMainForm.paramHelpIDForParamPanel(panel: PdParameterPanel): string;
  begin
  result := '';
  if panel = nil then exit;
  if panel is PdHeaderParameterPanel then result := 'Using_header_parameter_panels'
  else if (panel is PdSmallintParameterPanel) or (panel is PdRealParameterPanel) then
    result := 'Using_number_parameter_panels'
  else if panel is PdSCurveParameterPanel then result := 'Using_S_curve_parameter_panels'
  else if panel is PdBooleanParameterPanel then result := 'Using_yes/no_parameter_panels'
  else if panel is PdListParameterPanel then result := 'Using_list_parameter_panels'
  else if panel is PdColorParameterPanel then result := 'Using_color_parameter_panels'
  else if panel is PdTdoParameterPanel then result := 'Using_3D_object_parameter_panels';
  end;

procedure TMainForm.updateParametersPanelForFirstSelectedPlant;
  var
    i: integer;
    paramPanel: PdParameterPanel;
  begin  
  self.updatePlantNameLabel(kTabParameters);
  if parametersScrollBox.controlCount > 0 then
  	for i := 0 to parametersScrollBox.controlCount - 1 do
      if parametersScrollBox.controls[i] is PdParameterPanel then
     		begin
      	paramPanel := parametersScrollBox.controls[i] as PdParameterPanel;
      	{panels check if the new plant is different from current one}
        paramPanel.updatePlant(self.focusedPlant);
      	end;
  self.repositionParameterPanels;
  end;

procedure TMainForm.enteringAParameterPanel(aPanel: PdParameterPanel);
  begin
  self.selectedParameterPanel := aPanel;
  { update menu items and other things }
  end;

procedure TMainForm.leavingAParameterPanel(aPanel: PdParameterPanel);
  begin
  self.selectedParameterPanel := nil;
  { update menu items and other things }
  end;

procedure TMainForm.repositionParameterPanels;
  var
    i, lastPos, totalMaxWidth, panelMaxWidth, panelMinWidth, requestedWidth: integer;
    windowLock: boolean;
    paramPanel: PdParameterPanel;
    oldPosition: integer;
  begin
  if Application.terminated then exit;
  if parametersScrollBox.controlCount > 0 then
    begin
    totalMaxWidth := 0;
    lastPos := 0;
    oldPosition := parametersScrollBox.vertScrollBar.position;
    parametersScrollBox.vertScrollBar.position := 0;
    windowLock := lockWindowUpdate(self.handle);
    requestedWidth := parametersScrollBox.clientWidth;
    for i := 0 to parametersScrollBox.controlCount - 1 do
      begin
      paramPanel := PdParameterPanel(parametersScrollBox.controls[i]);
      paramPanel.left := 0;
      paramPanel.top := lastPos;
      paramPanel.calculateTextDimensions;
      panelMaxWidth := paramPanel.maxWidth;
      panelMinWidth := paramPanel.minWidth(requestedWidth);
      if panelMaxWidth <= requestedWidth then
        paramPanel.width := panelMaxWidth
      else
        begin
        if panelMinWidth = -1 then
          paramPanel.width := requestedWidth
        else
          paramPanel.width := panelMinWidth;
        end;
      paramPanel.calculateHeight;
      lastPos := lastPos + paramPanel.height;
      if paramPanel.width > totalMaxWidth then
        totalMaxWidth := paramPanel.width;
      end;
    lastPos := 0;
    for i := 0 to parametersScrollBox.controlCount - 1 do
      begin
      paramPanel := PdParameterPanel(parametersScrollBox.controls[i]);
      paramPanel.top := lastPos;
      // cfk change v2.0 final - can't remember why we had a max width - looks better this way
      // paramPanel.width := totalMaxWidth;   // was this
      paramPanel.width := parametersScrollBox.width - 20; // changed to
      paramPanel.calculateHeight;
      paramPanel.resizeElements;
      lastPos := lastPos + paramPanel.height;
      end;
    parametersScrollBox.vertScrollBar.position := oldPosition;
    if windowLock then lockWindowUpdate(0);
    end;
  end;            

procedure TMainForm.collapseOrExpandParameterPanelsUntilNextHeader(headerPanel: PdParameterPanel);
  var
    collapsing: boolean;
    paramPanel: PdParameterPanel;
    i: smallint;
  begin
  collapsing := false;
  internalChange := true;
  if parametersScrollBox.controlCount > 0 then for i := 0 to parametersScrollBox.controlCount - 1 do
    begin
    paramPanel := PdParameterPanel(parametersScrollBox.controls[i]);
    if paramPanel = headerPanel then
      collapsing := true
    else if collapsing and (paramPanel is PdHeaderParameterPanel) then
      collapsing := false
    else if collapsing then
      begin
      if headerPanel.param.collapsed then
        paramPanel.expand
      else
        paramPanel.collapse;
      end;
    end;
  internalChange := false;
  self.repositionParameterPanels;
  end;

procedure TMainForm.collapseOrExpandAllParameterPanelsInCurrentSection(doWhat: smallint);
  var
    section: PdSection;
    paramPanel: PdParameterPanel;
    i: smallint;
  begin
  internalChange := true;
  if sectionsComboBox.itemIndex < 0 then exit;
  section := sectionsComboBox.items.objects[sectionsComboBox.itemIndex] as PdSection;
  if section = nil then exit;
  case doWhat of
    kExpand: section.expanded := true;
    kCollapse: section.expanded := false;
    kExpandOrCollapse: section.expanded := not section.expanded;
    end;
  if parametersScrollBox.controlCount > 0 then for i := 0 to parametersScrollBox.controlCount - 1 do
    begin
    paramPanel := PdParameterPanel(parametersScrollBox.controls[i]);
    if section.expanded then paramPanel.expand else paramPanel.collapse;
    end;
  internalChange := false;
  self.repositionParameterPanels;
  end;

procedure TMainForm.updateParameterValuesWithUpdateListForPlant(aPlant: PdPlant; updateList: TListCollection);
  var
    i: longint;
    paramPanel: PdParameterPanel;
    updateEvent: PdPlantUpdateEvent;
    needToUpdateWholePlant: boolean;
	begin
  if aPlant <> self.focusedPlant then exit;
  if updateList.count <= 0 then exit;
  { first look to see if the whole plant needs updated - if any do, update it }
  { this is for side effects in GWI - left in just in case we need it later }
  needToUpdateWholePlant := false;
  for i := 0 to updateList.count - 1 do
    begin
    updateEvent := PdPlantUpdateEvent(updateList.items[i]);
    if (updateEvent.plant <> nil) and (updateEvent.plant.wholePlantUpdateNeeded) then
      begin
      needToUpdateWholePlant := true;
      updateEvent.plant.wholePlantUpdateNeeded := false;
      end;
    end;
  if needToUpdateWholePlant then
    begin
    self.updateParametersPanelForFirstSelectedPlant;
    exit;
    end;
  { if not updating everything, update based on list }
  { tell all components to look at list to see if they need updating }
  if parametersScrollBox.controlCount > 0 then
  	for i := 0 to parametersScrollBox.controlCount - 1 do
      if parametersScrollBox.controls[i] is PdParameterPanel then
     		begin
      	paramPanel := parametersScrollBox.Controls[i] as PdParameterPanel;
      	{ components check if use models and fields in list }
        paramPanel.updateFromUpdateEventList(updateList);
      	end;
  end;

procedure TMainForm.updateStatisticsPanelForFirstSelectedPlant;
  begin
  if Application.terminated then exit;
  if statsPanel = nil then exit;
  statsPanel.updatePlant(self.focusedPlant);
  statsPanel.updatePlantValues;
  end;

procedure TMainForm.updateNoteForFirstSelectedPlant;
  var selStart: integer;
  begin
  if Application.terminated then exit;
  if notePanel = nil then exit;
  if noteMemo = nil then exit;
  self.updatePlantNameLabel(kTabNote);
  self.updateForChangeToPlantNote(self.focusedPlant);
  end;

procedure TMainForm.noteEditClick(Sender: TObject);
  var
    newCommand: PdCommand;
  	noteForm: TNoteEditForm;
    commandLines: TStringList;
  begin
  if focusedPlant = nil then exit;
  noteForm := TNoteEditForm.create(self);
  if noteForm = nil then
    raise Exception.create('Problem: Could not create note edit window.');
  try
    noteForm.noteEditMemo.lines.addStrings(focusedPlant.noteLines);
    noteForm.caption := 'Edit note for ' + focusedPlant.getName;
    if noteForm.showModal <> mrCancel then
      begin
      commandLines := TStringList.create;  // command will take ownership of this and free it if necessary
      commandLines.addStrings(noteForm.noteEditMemo.lines);
      newCommand := PdEditNoteCommand.createWithPlantAndNewTStrings(focusedPlant, commandLines);
      self.doCommand(newCommand);
      end;
  finally
    noteForm.free;
    noteForm := nil;
  end;
  end;

procedure TMainForm.NotePopupMenuCopyClick(Sender: TObject);
  begin
  noteMemo.copyToClipboard;
  end;

procedure TMainForm.NotePopupMenuEditClick(Sender: TObject);
  begin
  self.noteEditClick(self);
  end;

procedure TMainForm.NotePopupMenuSelectAllClick(Sender: TObject);
  begin
  noteMemo.selectAll;
  end;

procedure TMainForm.MenuPlantEditNoteClick(Sender: TObject);
  begin
  self.noteEditClick(self);
  end;

procedure TMainForm.PopupMenuEditNoteClick(Sender: TObject);
  begin
  self.noteEditClick(self);
  end;

procedure TMainForm.updateRotationsPanelForFirstSelectedPlant;
  var color: TColorRef;
  begin
  self.updatePlantNameLabel(kTabRotations);
  color := self.textColorToRepresentPlantSelection(false);
  // location
  locationLabel.font.color := color;
  xLocationLabel.font.color := color;
  yLocationLabel.font.color := color;
  locationPixelsLabel.font.color := color;
  // size
  sizingLabel.font.color := color;
  drawingScalePixelsPerMmLabel.font.color := color;
  // rotation
  rotationLabel.font.color := color;
  xRotationLabel.font.color := color;
  yRotationLabel.font.color := color;
  zRotationLabel.font.color := color;
  // other updates
  self.updateForChangeToPlantRotations;
  self.updateForChangeToSelectedPlantsDrawingScale;
  self.updateForChangeToSelectedPlantsLocation;
  end;

{ ------------------------------------------------------------------------------------- *posing - updating }
const kSelectNoPosedPartString = '< Select None >';

procedure TMainForm.updatePosingForFirstSelectedPlant;
  var
    i: integer;
    amendment: PdPlantDrawingAmendment;
    partString: string;
  begin
  internalChange := true;
  posedPartsLabel.font.color := self.textColorToRepresentPlantSelection(false);
  selectedPartLabel.font.color := self.textColorToRepresentPlantSelection(false);
  posingPosePart.enabled := false;
  posingUnposePart.enabled := false;
  // called when plant changes
  posedPlantParts.clear;
  self.updatePlantNameLabel(kTabPosing);
  if focusedPlant = nil then
    begin
    posedPlantParts.text := '';
    posedPlantParts.enabled := false;
    end
  else
    begin
    posedPlantParts.enabled := true;
    // load list of parts with amendments
    if focusedPlant.amendments.count <= 0 then
      self.selectedPlantPartID := -1
    else
      begin
      for i := 0 to focusedPlant.amendments.count - 1 do
        begin
        amendment := PdPlantDrawingAmendment(focusedPlant.amendments.items[i]);
        partString := self.partDescriptionForIDAndType(amendment.partID, amendment.typeOfPart);
        if posedPlantParts.items.indexOf(partString) < 0 then
          posedPlantParts.items.add(partString);
        end;
      posedPlantParts.items.add(kSelectNoPosedPartString);
      end;
    end;
  internalChange := false;
  self.updatePosingForSelectedPlantPart;
  end;

const kNoPartSelected = 'Selected part: (none)';

procedure TMainForm.updatePosingForSelectedPlantPart;
  var
    partString: string;
    index: smallint;
  // PDF PORT -- removed semicolon from after begin
  begin                                
  internalChange := true;
  // called when selected part changes
  if focusedPlant = nil then
    begin
    self.selectedPlantPartID := -1;
    self.selectedPlantPartType := '';
    selectedPartLabel.caption := kNoPartSelected;
    end;
  if self.selectedPlantPartID >= 0 then
    begin
    partString := partDescriptionForIDAndType(selectedPlantPartID, selectedPlantPartType);
    selectedPartLabel.caption := 'Selected part: ' + partString;
    index := posedPlantParts.items.indexOf(partString);
    if index >= 0 then
      posedPlantParts.itemIndex := index
    else
      posedPlantParts.itemIndex := -1;
    end
  else
    begin
    posedPlantParts.itemIndex := -1;
    selectedPartLabel.caption := kNoPartSelected;
    end;
  posingPosePart.enabled := not (selectedPartLabel.caption = kNoPartSelected);
  posingUnPosePart.enabled := false;
  internalChange := false;
  self.updatePoseInfo;
  end;

procedure TMainForm.updatePoseInfo;
  var
    amendment: PdPlantDrawingAmendment;
    partID: longint;
  begin
  internalChange := true;
  amendment := nil;
  partID := self.selectedPartIDInAmendedPartsList;
  if partID >= 0 then
    amendment := focusedPlant.amendmentForPartID(partID);
  posingPosePart.enabled := (not (selectedPartLabel.caption = kNoPartSelected)) and (amendment = nil);
  posingUnPosePart.enabled := (not (selectedPartLabel.caption = kNoPartSelected)) and (not (amendment = nil));
  posingDetailsPanel.visible := amendment <> nil;
  if (amendment <> nil) then with amendment do
    begin
    posingHidePart.checked := hide;
    (*
    posingChangeColors.checked := changeColors;
    posingFrontfaceColor.color := faceColor;
    posingBackfaceColor.color := BackfaceColor;
    posingLineColor.color := lineColor;
    posingChangeAllColorsAfter.checked := propagateColors;
    *)
    posingAddExtraRotation.checked := addRotations;
    posingXRotationEdit.text := intToStr(round(xRotation));
    posingYRotationEdit.text := intToStr(round(yRotation));
    posingZRotationEdit.text := intToStr(round(zRotation));
    posingMultiplyScale.checked := multiplyScale;
    posingMultiplyScaleAllPartsAfter.checked := propagateScale;
    posingScaleMultiplierEdit.text := intToStr(scaleMultiplier_pct);
    posingLengthMultiplierEdit.text := intToStr(lengthMultiplier_pct);
    posingWidthMultiplierEdit.text := intToStr(widthMultiplier_pct);
    end;
  internalChange := false;
  self.updateForDependenciesWithinPoseInfo;
  end;

procedure enableOrDisableSet(aLabel: TLabel; anEdit: TEdit; aSpin: TSpinButton; anExtraLabel: TLabel; enable: boolean);
  begin
  if aLabel <> nil then aLabel.enabled := enable;
  if anEdit <> nil then anEdit.enabled := enable;
  if aSpin <> nil then aSpin.visible := enable;
  if anExtraLabel <> nil then anExtraLabel.enabled := enable;
  end;

procedure TMainForm.updateForDependenciesWithinPoseInfo;
  begin
  internalChange := true;
  posingChangeAllColorsAfter.enabled := posingChangeColors.checked;
  posingMultiplyScaleAllPartsAfter.enabled := posingMultiplyScale.checked;
  posingMultiplyScaleAllPartsAfterLabel.enabled := posingMultiplyScaleAllPartsAfter.enabled;
  (*
  posingLineColor.visible := posingChangeColors.checked;
  posingLineColorLabel.enabled := posingChangeColors.checked;
  posingFrontfaceColor.visible := posingChangeColors.checked;
  posingFrontfaceColorLabel.enabled := posingChangeColors.checked;
  posingBackfaceColor.visible := posingChangeColors.checked;
  posingBackfaceColorLabel.enabled := posingChangeColors.checked;
  *)
  enableOrDisableSet(posingXRotationLabel, posingXRotationEdit, posingXRotationSpin, nil, posingAddExtraRotation.checked);
  enableOrDisableSet(posingYRotationLabel, posingYRotationEdit, posingYRotationSpin, nil, posingAddExtraRotation.checked);
  enableOrDisableSet(posingZRotationLabel, posingZRotationEdit, posingZRotationSpin, nil, posingAddExtraRotation.checked);
  rotationDegreesLabel.enabled := posingAddExtraRotation.checked;
  enableOrDisableSet(posingScaleMultiplierLabel, posingScaleMultiplierEdit, posingScaleMultiplierSpin,
    posingScaleMultiplierPercent, posingMultiplyScale.checked);
  enableOrDisableSet(posingLengthMultiplierLabel, posingLengthMultiplierEdit, posingLengthMultiplierSpin,
    posingLengthMultiplierPercent, posingMultiplyScale.checked);
  enableOrDisableSet(posingWidthMultiplierLabel, posingWidthMultiplierEdit, posingWidthMultiplierSpin,
    posingWidthMultiplierPercent, posingMultiplyScale.checked);
  internalChange := false;
  end;

procedure TMainForm.redrawAllPlantsInViewWithAmendments;
  var
    i: smallint;
    plant: PdPlant;
  begin
  if plants.count > 0 then
    for i := 0 to plants.count - 1 do
      begin
      plant := PdPlant(plants.items[i]);
      if (plant <> nil) and (plant.amendments <> nil) and (plant.amendments.count > 0) then
        begin
        plant.recalculateBounds(kDrawNow);
        self.invalidateDrawingRect(plant.boundsRect_pixels);
        end;
      end;
  self.updateForPossibleChangeToDrawing;
  end;

{ ------------------------------------------------------------------------------------- *posing - interface }
procedure TMainForm.posedPlantPartsChange(Sender: TObject);
  var newCommand: PdCommand;
  begin
  if internalChange then exit;
  if posedPlantParts.itemIndex = posedPlantParts.items.count - 1 then
    newCommand := PdSelectPosingPartCommand.createWithPlantAndPartIDsAndTypes(focusedPlant,
      -1, self.selectedPlantPartID,
      '', self.selectedPlantPartType)
  else
    newCommand := PdSelectPosingPartCommand.createWithPlantAndPartIDsAndTypes(focusedPlant,
      self.selectedPartIDInAmendedPartsList, self.selectedPlantPartID,
      self.selectedPartTypeInAmendedPartsList, self.selectedPlantPartType);
  self.doCommand(newCommand);
  end;

procedure TMainForm.posingFrontfaceColorMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  posingFrontfaceColor.color := domain.getColorUsingCustomColors(posingFrontfaceColor.color);
  self.changeSelectedPose(posingFrontfaceColor);
  end;

procedure TMainForm.posingBackfaceColorMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  posingBackfaceColor.color := domain.getColorUsingCustomColors(posingBackfaceColor.color);
  self.changeSelectedPose(posingBackfaceColor);
  end;

procedure TMainForm.posingLineColorMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  posingLineColor.color := domain.getColorUsingCustomColors(posingLineColor.color);
  self.changeSelectedPose(posingLineColor);
  end;

procedure TMainForm.posingRotationSpinUp(Sender: TObject);
  begin
  if (sender <> nil) and (sender is TSpinButton) then
    self.spinPoseRotationBy((sender as TSpinButton).focusControl, domain.options.rotationIncrement);
  end;

procedure TMainForm.posingRotationSpinDown(Sender: TObject);
  begin
  if (sender <> nil) and (sender is TSpinButton) then
    self.spinPoseRotationBy((sender as TSpinButton).focusControl, -domain.options.rotationIncrement);
  end;

procedure TMainForm.spinPoseRotationBy(sender: TObject; amount: integer);
  var
    newRotation, oldRotation: smallint;
  begin
  if (sender <> nil) and (sender is TEdit) then
    begin
    newRotation := strToIntDef((Sender as TEdit).text, 0);
    oldRotation := newRotation;
    newRotation := newRotation + amount;
    if newRotation < -360 then newRotation := 360 - (abs(newRotation) - 360);
    if newRotation > 360 then newRotation := -360 + (newRotation - 360);
    if newRotation <> oldRotation then
      (Sender as TEdit).text := intToStr(newRotation);
    end;
  end;

procedure TMainForm.posingScaleMultiplierSpinUpClick(Sender: TObject);
  begin
  if (sender <> nil) and (sender is TSpinButton) then
    self.spinScaleMultiplierBy((sender as TSpinButton).focusControl, domain.options.resizeKeyUpMultiplierPercent - 100);
  end;

procedure TMainForm.posingScaleMultiplierSpinDownClick(Sender: TObject);
  begin
  if (sender <> nil) and (sender is TSpinButton) then
    self.spinScaleMultiplierBy((sender as TSpinButton).focusControl, -(domain.options.resizeKeyUpMultiplierPercent - 100));
  end;

procedure TMainForm.spinScaleMultiplierBy(sender: TObject; amount: integer);
  var
    newValue, oldValue: smallint;
  begin
  if (sender <> nil) and (sender is TEdit) then
    begin
    newValue := strToIntDef((Sender as TEdit).text, 0);
    oldValue := newValue;
    newValue := newValue + amount;
    if newValue < 0 then newValue := 0;
    if newValue > 1000 then newValue := 1000;
    if newValue <> oldValue then
      (Sender as TEdit).text := intToStr(newValue);
    end;
  end;

{ ------------------------------------------------------------------------------------- *posing - commands }
procedure TMainForm.changeSelectedPose(Sender: TObject);
  var
    newCommand: PdCommand;
    newAmendment: PdPlantDrawingAmendment;
    partID: longint;
    currentAmendment: PdPlantDrawingAmendment;
    field: string;
  begin
  if internalChange then exit;
  self.updateForDependenciesWithinPoseInfo;
  if focusedPlant = nil then exit;
  newAmendment := PdPlantDrawingAmendment.create; // command will take ownership of this and free it if necessary
  partID := self.selectedPartIDInAmendedPartsList;
  currentAmendment := focusedPlant.amendmentForPartID(partID);
  if currentAmendment = nil then exit;
  if (sender = posingHidePart) then field := 'hide'
    else if (sender = posingAddExtraRotation) then field := 'rotate'
    else if ((sender = posingXRotationEdit) or (sender = posingXRotationSpin)) then field := 'X rotation'
    else if ((sender = posingYRotationEdit) or (sender = posingYRotationSpin)) then field := 'Y rotation'
    else if ((sender = posingZRotationEdit) or (sender = posingZRotationSpin)) then field := 'Z rotation'
    else if (sender = posingMultiplyScale) then field := 'scale'
    else if (sender = posingMultiplyScaleAllPartsAfter) then field := 'scale above'
    else if ((sender = posingScaleMultiplierEdit) or (sender = posingScaleMultiplierSpin)) then field := '3D object scale'
    else if ((sender = posingLengthMultiplierEdit) or (sender = posingLengthMultiplierSpin)) then field := 'line length'
    else if ((sender = posingWidthMultiplierEdit) or (sender = posingWidthMultiplierSpin)) then field := 'line width'
    else field := '';

    (*   cfk if bring back color finish these
    posingChangeColors: TCheckBox;
    posingChangeAllColorsAfter: TCheckBox;
    posingLineColor: TPanel;
    posingFrontfaceColor: TPanel;
    posingBackfaceColor: TPanel;
    posingLineColorLabel: TLabel;
    posingFrontfaceColorLabel: TLabel;
    posingBackfaceColorLabel: TLabel;
    *)
         
  with newAmendment do
    begin
    partID := self.partIDForFullDescription(posedPlantParts.text);
    typeOfPart := self.partTypeForFullDescription(posedPlantParts.text);
    hide := posingHidePart.checked;
    (*
    changeColors := posingChangeColors.checked;
    faceColor := posingFrontfaceColor.color;
    backfaceColor := posingBackfaceColor.color;
    lineColor := posingLineColor.color;
    propagateColors := posingChangeAllColorsAfter.checked;
    *)
    addRotations := posingAddExtraRotation.checked;
    xRotation := intMax(-360, intMin(360, strToIntDef(posingXRotationEdit.text, round(currentAmendment.xRotation))));
    yRotation := intMax(-360, intMin(360, strToIntDef(posingYRotationEdit.text, round(currentAmendment.yRotation))));
    zRotation := intMax(-360, intMin(360, strToIntDef(posingZRotationEdit.text, round(currentAmendment.zRotation))));
    multiplyScale := posingMultiplyScale.checked;
    propagateScale :=  posingMultiplyScaleAllPartsAfter.checked;
    scaleMultiplier_pct := intMax(0, intMin(1000, strToIntDef(posingScaleMultiplierEdit.text, currentAmendment.scaleMultiplier_pct)));
    lengthMultiplier_pct := intMax(0, intMin(1000, strToIntDef(posingLengthMultiplierEdit.text, currentAmendment.lengthMultiplier_pct)));
    widthMultiplier_pct := intMax(0, intMin(1000, strToIntDef(posingWidthMultiplierEdit.text, currentAmendment.widthMultiplier_pct)));
    end;
  newCommand := PdEditAmendmentCommand.createWithPlantAndAmendmentAndField(focusedPlant, newAmendment, field);
  self.doCommand(newCommand);
  end;

procedure TMainForm.posingPosePartClick(Sender: TObject);
  var
    newCommand: PdCommand;
    newAmendment: PdPlantDrawingAmendment;
  begin
  if focusedPlant = nil then exit;
  if self.selectedPlantPartID < 0 then exit;
  if focusedPlant.amendmentForPartID(self.selectedPlantPartID) <> nil then exit; // only one amendment per part id
  newAmendment := PdPlantDrawingAmendment.create; // command will take ownership of this and free it if necessary
  newAmendment.partID := self.selectedPlantPartID;
  newAmendment.typeOfPart := self.selectedPlantPartType;
  newCommand := PdCreateAmendmentCommand.createWithPlantAndAmendment(focusedPlant, newAmendment);
  self.doCommand(newCommand);
  end;

procedure TMainForm.posingUnposePartClick(Sender: TObject);
  var
    newCommand: PdCommand;
    amendment: PdPlantDrawingAmendment;
  begin
  if focusedPlant = nil then exit;
  amendment := focusedPlant.amendmentForPartID(self.selectedPartIDInAmendedPartsList);
  if amendment = nil then exit;
  newCommand := PdDeleteAmendmentCommand.createWithPlantAndAmendment(focusedPlant, amendment);
  self.doCommand(newCommand);
  end;

procedure TMainForm.addAmendedPartToList(partID: longint; partType: string);
  var
    newString: string;
    selectNoneIndex, indexToSave: smallint;
  begin
  newString := MainForm.partDescriptionForIDAndType(partID, partType);
  posedPlantParts.items.add(newString);
  indexToSave := posedPlantParts.items.count - 1;
  // add "select none" to end - move down if already there
  selectNoneIndex := posedPlantParts.items.indexOf(kSelectNoPosedPartString);
  if selectNoneIndex >= 0 then posedPlantParts.items.delete(selectNoneIndex);
  posedPlantParts.items.add(kSelectNoPosedPartString);
  posedPlantParts.itemIndex := indexToSave;
  self.updatePosingForSelectedPlantPart;
  end;

procedure TMainForm.removeAmendedPartFromList(partID: longint; partType: string);
  var
    oldString: string;
    index, oldItemIndex: integer;
  begin
  oldItemIndex := posedPlantParts.itemIndex;
  oldString := self.partDescriptionForIDAndType(partID, partType);
  index := posedPlantParts.items.indexOf(oldString);
  if index >= 0 then posedPlantParts.items.delete(index);
  if oldItemIndex <= posedPlantParts.items.count - 1 then posedPlantParts.itemIndex := oldItemIndex;
  self.updatePosingForSelectedPlantPart;
  end;

{ ------------------------------------------------------------------------------------- *posing - supporting }
function TMainForm.partDescriptionForIDAndType(id: longint; typeName: string): string;
  begin
  result := intToStr(id) + ' (' + typeName + ')';
  end;

function TMainForm.partIDForFullDescription(aString: string): longint;
  begin
  result := strToIntDef(stringUpTo(aString, ' ('), -1);
  end;

function TMainForm.partTypeForFullDescription(aString: string): string;
  begin
  result := '';
  if length(aString) <= 0 then exit;
  result := stringBeyond(aString, '(');
  result := stringUpTo(result, ')');
  end;

function TMainForm.selectedPartIDInAmendedPartsList: longint;
  begin
  result := -1;
  if (focusedPlant = nil) or (posedPlantParts.items.count <= 0) or (posedPlantParts.itemIndex < 0) then
    exit;
  result := self.partIDForFullDescription(posedPlantParts.items[posedPlantParts.itemIndex]);
  end;

function TMainForm.selectedPartTypeInAmendedPartsList: string;
  begin
  result := '';
  if (focusedPlant = nil) or (posedPlantParts.items.count <= 0) or (posedPlantParts.itemIndex < 0) then
    exit;
  result := self.partTypeForFullDescription(posedPlantParts.items[posedPlantParts.itemIndex]);
  end;

{ ------------------------------------------------------------------------------------- *resizing }
procedure TMainForm.FormResize(Sender: TObject);
  var
    newTop, newLeft, newWidth, newHeight, splitterWidthOrHeight: smallint;
    windowLock: boolean;
  begin
  if Application.terminated then exit;
  if self.WindowState = wsMinimized then exit;
  if domain = nil then exit;
  if drawingBitmap = nil then exit;
  if selectedPlants = nil then exit; 
  horizontalSplitter.visible := false;
  verticalSplitter.visible := false;
  plantListPanel.visible := false;
  plantFocusPanel.visible := false;
  windowLock := lockWindowUpdate(self.handle);
  with toolbarPanel do setBounds(0, 0, self.clientWidth, height);
  splitterWidthOrHeight := verticalSplitter.width; {assumes they are equal, I have at 4 now}
  if lastHeight <> 0 then 
    newTop := round(1.0 * horizontalSplitter.top * clientHeight / lastHeight)
  else
    newTop := clientHeight div 2;
  newTop := intMax(0, intMin(self.clientHeight - 1, newTop));
  newHeight := intMax(0, self.clientHeight - newTop - splitterWidthOrHeight);
  if lastWidth <> 0 then
    newLeft := round(1.0 * verticalSplitter.left * clientWidth / lastWidth)
  else
    newLeft := clientWidth div 2;
  newLeft := intMax(0, intMin(self.clientWidth - 1, newLeft));
  newWidth := intMax(0, self.clientWidth - newLeft - splitterWidthOrHeight);
  if domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal then
    begin
    with horizontalSplitter do setBounds(0, newTop, self.clientWidth, height);
    with verticalSplitter do setBounds(newLeft, newTop + horizontalSplitter.height, width, newHeight);
    end
  else if domain.options.mainWindowOrientation = kMainWindowOrientationVertical then
    begin
    with verticalSplitter do setBounds(newLeft, toolbarPanel.height, width,
        intMax(0, self.clientHeight - toolbarPanel.height));
    with horizontalSplitter do setBounds(newLeft + verticalSplitter.width, newTop, newWidth, height);
    end;
  { resize images and panels }
  self.resizePanelsToHorizontalSplitter;
  self.resizePanelsToVerticalSplitter;
  lastHeight := self.clientHeight;
  lastWidth := self.clientWidth;
  if windowLock then lockWindowUpdate(0);
  horizontalSplitter.visible := true;
  verticalSplitter.visible := true;
  plantListPanel.visible := true;
  plantFocusPanel.visible := true;
  end;

procedure TMainForm.resizePanelsToVerticalSplitter;
  var
    newLeft, newWidth, newTop, newHeight: smallint;
  begin
  newLeft := verticalSplitter.left + verticalSplitter.width;
  newWidth := intMax(0, self.clientWidth - newLeft);
  newTop := horizontalSplitter.top + horizontalSplitter.height;
  newHeight := intMax(0, self.clientHeight - newTop);
  if domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal then
    begin
    with plantListPanel do setBounds(0, newTop, verticalSplitter.left, newHeight);
    with plantFocusPanel do setBounds(newLeft, newTop, newWidth, newHeight);
    end
  else if domain.options.mainWindowOrientation = kMainWindowOrientationVertical then
    begin
    with plantListPanel do setBounds(newLeft, toolbarPanel.height, newWidth,
      horizontalSplitter.top - toolbarPanel.height);
    with plantFocusPanel do setBounds(newLeft, newTop, newWidth, newHeight);
    with horizontalSplitter do setBounds(newLeft, top, newWidth, height); {don't change top here}
    with drawingPaintBox do setBounds(0, toolbarPanel.height, newLeft,
        intMax(0, self.clientHeight - toolbarPanel.height));
    self.resizeDrawingBitmapIfNecessary;
    end;
  self.resizePlantListPanel;
  self.resizePlantFocusPanel;
  end;

procedure TMainForm.resizePanelsToHorizontalSplitter;
  var
    newLeft, newWidth, newTop, newHeight: smallint;
  begin
  newLeft := verticalSplitter.left + verticalSplitter.width;
  newWidth := intMax(0, self.clientWidth - newLeft);
  newTop := horizontalSplitter.top + horizontalSplitter.height;
  newHeight := intMax(0, self.clientHeight - newTop);
  if domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal then
    begin
    with plantListPanel do setBounds(0, newTop, verticalSplitter.left, newHeight);
    with verticalSplitter do setBounds(left, newTop, width, newHeight); {don't change left here}
    with plantFocusPanel do setBounds(newLeft, newTop, newWidth, newHeight);
    with drawingPaintBox do setBounds(0, toolBarPanel.height, self.clientWidth,
        intMax(0, horizontalSplitter.top - toolBarPanel.height));
    self.resizeDrawingBitmapIfNecessary;
    end
  else if domain.options.mainWindowOrientation = kMainWindowOrientationVertical then
    begin
    with plantListPanel do setBounds(newLeft, toolbarPanel.height, newWidth,
      horizontalSplitter.top - toolbarPanel.height);
    with plantFocusPanel do setBounds(newLeft, newTop, newWidth, newHeight);
    end;
  self.resizePlantListPanel;
  self.resizePlantFocusPanel;
  end;

procedure TMainForm.resizeDrawingBitmapIfNecessary;
  var bitmapWasMadeBigger: boolean;
  begin
  if (drawingBitmap.width <> drawingPaintBox.width) or (drawingBitmap.height <> drawingPaintBox.height) then
    begin
    // if have to make bitmap larger, redraw all plants in case some were not drawing before
    // because they were off the bitmap
    bitmapWasMadeBigger := (drawingPaintBox.width > drawingBitmap.width) or (drawingPaintBox.height > drawingBitmap.height);
    resizeBitmap(drawingBitmap, Point(drawingPaintBox.width, drawingPaintBox.height));
    if not inFormCreation then
      begin
      if bitmapWasMadeBigger then
        self.recalculateAllPlantBoundsRects(kDontDrawYet);
      self.invalidateEntireDrawing;
      self.updateForPossibleChangeToDrawing;
      end;
    end;
  end;

procedure TMainForm.resizePlantListPanel;
  begin
  with plantListDrawGrid do setBounds(0, 0, plantListPanel.width,
    plantListPanel.height - plantFileChangedImage.height - kBetweenGap * 2);
    plantListDrawGrid.defaultColWidth := plantListDrawGrid.clientWidth;
  with plantFileChangedImage do
    setBounds(kBetweenGap, plantListDrawGrid.top + plantListDrawGrid.height + kBetweenGap, width, height);
  with plantBitmapsIndicatorImage do
    setBounds(plantFileChangedImage.left + plantFileChangedImage.width + kBetweenGap,
        plantFileChangedImage.top, width, height);
  with progressPaintBox do setBounds(
    plantBitmapsIndicatorImage.left + plantBitmapsIndicatorImage.width + kBetweenGap,
    plantBitmapsIndicatorImage.top + plantBitmapsIndicatorImage.height div 2 - height div 2,
    plantListPanel.width - plantFileChangedImage.width
        - plantBitmapsIndicatorImage.width - kBetweenGap * 4, height);
  end;

procedure TMainForm.resizePlantFocusPanel;
  var newTop: integer;
  begin
  { tab set }
  with tabSet do setBounds(0, plantFocusPanel.height - height, plantFocusPanel.width, height);
  with animatingLabel do setBounds(intMax(0, plantFocusPanel.width - width - kBetweenGap), // v1.4 change
    plantFocusPanel.height - height - kBetweenGap, width, height);
  { life cycle panel }
  with lifeCyclePanel do setBounds(0, 0, plantFocusPanel.width, intMax(0, plantFocusPanel.height - tabSet.height));
  lifeCycleEditPanel.height := animateGrowth.height + kBetweenGap * 2 - 2; // v1.4 change - 2
  with lifeCycleEditPanel do setBounds(1, intMax(0, lifeCyclePanel.height - height - 1),
    lifeCyclePanel.width - 2, height);  // v1.4 change +1, -1, -2
  // rotations panel
  with rotationsPanel do setBounds(0, 0, lifeCyclePanel.width, lifeCyclePanel.height);
  // posing panel
  with posingPanel do setBounds(0, 0, lifeCyclePanel.width, lifeCyclePanel.height);
  newTop := posingPlantName.top + posingPlantName.height + kBetweenGap;
  with posingNotShown do setBounds(posingPanel.width - width - kBetweenGap, newTop, width, height);
  with posingGhost do setBounds(posingNotShown.left - width - kBetweenGap, newTop, width, height);
  with posingHighlight do setBounds(posingGhost.left - width - kBetweenGap, newTop, width, height);
  newTop := posingNotShown.top + posingNotShown.height + kBetweenGap;
  with posedPartsLabel do setBounds(kBetweenGap,
      newTop + (posedPlantParts.height div 2 - height div 2), width, height);
  with posedPlantParts do setBounds(
      posedPartsLabel.left + posedPartsLabel.width + kBetweenGap, newTop,
      intMax(10, posingPanel.width - posedPartsLabel.width - kBetweenGap * 3), height);
  newTop := posedPlantParts.top + posedPlantParts.height + kBetweenGap;
  with selectedPartLabel do setBounds(kBetweenGap,
    newTop + (posingUnposePart.height div 2 - height div 2), width, height); // fix later
  newTop := selectedPartLabel.top + selectedPartLabel.height + kBetweenGap;
  with posingPosePart do setBounds(kBetweenGap, newTop, width, height);
  with posingUnposePart do setBounds(posingPosePart.left + posingPosePart.width + kBetweenGap, newTop, width, height);
  newTop := posingUnposePart.top + posingUnposePart.height + kBetweenGap;
  with posingDetailsPanel do setBounds(0, newTop, lifeCyclePanel.width,
    intMax(230, lifeCyclePanel.height - newTop));
  { lifeCycleEditPanel }
  with lifeCycleDaysEdit do setBounds(ageAndSizeLabel.width + kBetweenGap * 2, kBetweenGap, width, height);
  with lifeCycleDaysSpin do setBounds(lifeCycleDaysEdit.left + lifeCycleDaysEdit.width,
    kBetweenGap + lifeCycleDaysEdit.height div 2 - height div 2, width, height);
  with ageAndSizeLabel do setBounds(kBetweenGap,
      intMax(0, lifeCycleDaysEdit.top + lifeCycleDaysEdit.height div 2 - height div 2), width, height);
  with daysAndSizeLabel do setBounds(lifeCycleDaysSpin.left + lifeCycleDaysSpin.width + kBetweenGap,
      intMax(0, lifeCycleDaysEdit.top + lifeCycleDaysEdit.height div 2 - height div 2), width, height);
  with animateGrowth do setBounds(lifeCycleEditPanel.width - width - kBetweenGap,
      lifeCycleDaysEdit.top, width, height);
  { above lifeCycleEditPanel }
  with timeLabel do setBounds(intMax(0, lifeCyclePanel.width div 2 - width div 2),
    intMax(0, lifeCycleEditPanel.top - height - kBetweenGap), width, height);
  with lifeCycleGraphImage do setBounds(kBetweenGap + maxSizeAxisLabel.width + kBetweenGap,
    intMax(1, selectedPlantNameLabel.top + selectedPlantNameLabel.height + kBetweenGap),
    intMax(1, lifeCyclePanel.width - maxSizeAxisLabel.width - kBetweenGap * 3),
    intMax(1, timeLabel.top - selectedPlantNameLabel.height - kBetweenGap * 2));
  with maxSizeAxisLabel do setBounds(kBetweenGap,
    intMax(0, lifeCycleGraphImage.top + lifeCycleGraphImage.height div 2 - height div 2),
    width, height);
  with selectedPlantNameLabel do setBounds(kBetweenGap, kBetweenGap, width, height);
 // with selectedPlantNameLabel do setBounds(lifeCycleGraphImage.left, kBetweenGap, width, height);
  if (lifeCycleGraphImage.picture.bitmap.width <> lifeCycleGraphImage.width)
      or (lifeCycleGraphImage.picture.bitmap.height <> lifeCycleGraphImage.height) then
    resizeBitmap(lifeCycleGraphImage.picture.bitmap, Point(lifeCycleGraphImage.width, lifeCycleGraphImage.height));
  self.placeLifeCycleDragger;
  self.redrawLifeCycleGraph;
  self.resizeParametersPanel;
  { stats scroll box }
  with statsScrollBox do setBounds(0, 0, plantFocusPanel.width, intMax(0, plantFocusPanel.height - tabSet.height));
  statsPanel.resizeElements;
  with notePanel do setBounds(0, 0, plantFocusPanel.width, intMax(0, plantFocusPanel.height - tabSet.height));
  with noteLabel do setBounds(kBetweenGap, kBetweenGap, width, height);
    //kBetweenGap + noteEdit.height div 2 - height div 2, width, height);
  with noteEdit do setBounds(intMax(0, notePanel.width - width - kBetweenGap), kBetweenGap, width, height);
  with noteMemo do setBounds(0, noteEdit.height + kBetweenGap * 2, notePanel.width,
    intMax(0, notePanel.height - noteEdit.height - kBetweenGap * 2));
  end;

procedure TMainForm.resizeParametersPanel;
  var newTop: smallint;
  begin
  with parametersPanel do setBounds(0, 0, plantFocusPanel.width, intMax(0, plantFocusPanel.height - tabSet.height));
  with parametersPlantName do setBounds(kBetweenGap, kBetweenGap, width, height);
  with sectionsComboBox do setBounds(kBetweenGap, parametersPlantName.top + parametersPlantName.height + kBetweenGap,
      parametersPanel.width - kBetweenGap * 2, height);
  newTop := sectionsComboBox.top + sectionsComboBox.height + kBetweenGap;
  with parametersScrollBox do setBounds(0, sectionsComboBox.top + sectionsComboBox.height + kBetweenGap,
      parametersPanel.width, parametersPanel.height - newTop);
  self.repositionParameterPanels;
  end;

procedure TMainForm.placeLifeCycleDragger;
  var
    firstPlant: PdPlant;
    fractionOfMaxAge: single;
  begin
  firstPlant := self.focusedPlant;
  fractionOfMaxAge := 0.0;
  if firstPlant <> nil then
    try
      fractionOfMaxAge := firstPlant.age / firstPlant.pGeneral.ageAtMaturity;
    except
      fractionOfMaxAge := 0.0;
    end;
  with lifeCycleDragger do setBounds(
      lifeCycleGraphImage.left + round((lifeCycleGraphImage.width - lifeCycleDragger.width) * fractionOfMaxAge),
      lifeCycleGraphImage.top + 1, width, lifeCycleGraphImage.height - 2);
  end;

procedure TMainForm.WMGetMinMaxInfo(var MSG: Tmessage);
  begin
  inherited;
  with PMinMaxInfo(MSG.lparam)^ do
    begin
    ptMinTrackSize.x := 300;
    ptMinTrackSize.y := 300;
    end;
  end;

{ ------------------------------------------------------------------------------------- *splitting }
procedure TMainForm.horizontalSplitterMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  self.horizontalSplitterDragging := true;
  self.horizontalSplitterStartPos := y;
  self.horizontalSplitterLastDrawPos := -1;
  self.horizontalSplitterNeedToRedraw := true;
  end;

procedure TMainForm.horizontalSplitterMouseMove(Sender: TObject; Shift: TShiftState; X, Y: Integer);
  var
    bottomLimit: integer;
  begin
  if domain = nil then exit;
  if domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal then
    bottomLimit := kSplitterDragToBottomMinPixelsInHorizMode
  else if domain.options.mainWindowOrientation = kMainWindowOrientationVertical then
    bottomLimit := kSplitterDragToBottomMinPixelsInVertMode
  else
    bottomLimit := kSplitterDragToBottomMinPixelsInHorizMode;
  if self.horizontalSplitterDragging and
    (horizontalSplitter.top + y >= kSplitterDragToTopMinPixels)
      and (horizontalSplitter.top + y < self.clientHeight - bottomLimit) then
      begin
      self.undrawHorizontalSplitterLine;
      self.horizontalSplitterLastDrawPos := self.drawHorizontalSplitterLine(y);
      end;
  end;

procedure TMainForm.horizontalSplitterMouseUp(Sender: TObject; Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  var
    bottomLimit: integer;
  begin
  if domain = nil then exit;
  if domain.options.mainWindowOrientation = kMainWindowOrientationHorizontal then
    bottomLimit := kSplitterDragToBottomMinPixelsInHorizMode
  else if domain.options.mainWindowOrientation = kMainWindowOrientationVertical then
    bottomLimit := kSplitterDragToBottomMinPixelsInVertMode
  else
    bottomLimit := kSplitterDragToBottomMinPixelsInHorizMode;
  if self.horizontalSplitterDragging then
    begin
    self.undrawHorizontalSplitterLine;
    horizontalSplitter.top := horizontalSplitter.top - (horizontalSplitterStartPos - y);
    if horizontalSplitter.top < kSplitterDragToTopMinPixels then
      horizontalSplitter.top := kSplitterDragToTopMinPixels;
    if horizontalSplitter.top > self.clientHeight - bottomLimit then
      horizontalSplitter.top := self.clientHeight - bottomLimit;
  	self.resizePanelsToHorizontalSplitter;
    self.horizontalSplitterDragging := false;
    end;
  end;

function TMainForm.drawHorizontalSplitterLine(pos: integer): integer;
  var theDC: HDC;
  begin
  theDC := getDC(0);
  result := self.clientOrigin.y + horizontalSplitter.top + pos + 2;
  patBlt(theDC, self.clientOrigin.x + horizontalSplitter.left, result,
      horizontalSplitter.width, 1, dstInvert);
  releaseDC(0, theDC);
  self.horizontalSplitterNeedToRedraw := true;
  end;

procedure TMainForm.undrawHorizontalSplitterLine;
  var theDC: HDC;
  begin
  if not self.horizontalSplitterNeedToRedraw then exit;
  theDC := getDC(0);
  patBlt(theDC, self.clientOrigin.x + horizontalSplitter.left,
      self.horizontalSplitterLastDrawPos, horizontalSplitter.width, 1, dstInvert);
  releaseDC(0, theDC);
  self.horizontalSplitterNeedToRedraw := false;
  end;

procedure TMainForm.verticalSplitterMouseDown(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  self.verticalSplitterDragging := true;
  self.verticalSplitterStartPos := x;
  self.verticalSplitterLastDrawPos := -1;
  self.verticalSplitterNeedToRedraw := true;
  end;

procedure TMainForm.verticalSplitterMouseMove(Sender: TObject;
  Shift: TShiftState; X, Y: Integer);
  begin
  if self.verticalSplitterDragging and
    (verticalSplitter.left + x >= kSplitterDragToLeftMinPixels)
      and (verticalSplitter.left + x < self.clientWidth - kSplitterDragToRightMinPixels) then
      begin
      self.undrawVerticalSplitterLine;
      self.verticalSplitterLastDrawPos := self.drawVerticalSplitterLine(x);
      end;
  end;

procedure TMainForm.verticalSplitterMouseUp(Sender: TObject;
  Button: TMouseButton; Shift: TShiftState; X, Y: Integer);
  begin
  if self.verticalSplitterDragging then
    begin
    self.undrawVerticalSplitterLine;
    verticalSplitter.left := verticalSplitter.left - (verticalSplitterStartPos - x);
    if verticalSplitter.left < kSplitterDragToLeftMinPixels then
      verticalSplitter.left := kSplitterDragToLeftMinPixels;
    if verticalSplitter.left > self.clientWidth - kSplitterDragToRightMinPixels then
      verticalSplitter.left := self.clientWidth - kSplitterDragToRightMinPixels;
  	self.resizePanelsToVerticalSplitter;
    self.verticalSplitterDragging := false;
    end;
  end;

function TMainForm.drawVerticalSplitterLine(pos: integer): integer;
  var
    theDC: HDC;
  begin
  theDC := getDC(0);
  result := self.clientOrigin.x + verticalSplitter.left + pos + 2;
  patBlt(theDC, result, self.clientOrigin.y + verticalSplitter.top, 1,
      verticalSplitter.height, dstInvert);
  releaseDC(0, theDC);
  self.verticalSplitterNeedToRedraw := true;
  end;

procedure TMainForm.undrawVerticalSplitterLine;
  var theDC: HDC;
  begin
  if not self.verticalSplitterNeedToRedraw then exit;
  theDC := getDC(0);
  patBlt(theDC, self.verticalSplitterLastDrawPos,
    self.clientOrigin.y + verticalSplitter.top, 1, verticalSplitter.height, dstInvert);
  releaseDC(0, theDC);
  self.verticalSplitterNeedToRedraw := false;
  end;

{ ----------------------------------------------------------------------------- *palette stuff }
function TMainForm.GetPalette: HPALETTE;
  begin
  result := paletteImage.picture.bitmap.palette;
  end;

{overriden because paint box will not update correctly}
{makes window take first priority for palettes}
function TMainForm.PaletteChanged(Foreground: Boolean): Boolean;
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
      and (drawingPaintBox <> nil) then
        begin
        setPixelFormatBasedOnScreenForBitmap(drawingBitmap);
    	  drawingPaintBox.invalidate;
        end;
    if statsPanel <> nil then
      statsPanel.invalidate;
    selectPalette(DC, oldPalette, True);
    realizePalette(DC);
    releaseDC(windowHandle, DC);
  	end;
  result := inherited paletteChanged(foreground);
	end;

procedure TMainForm.FormShow(Sender: TObject);
  begin
  DragAcceptFiles(Handle, True);
  end;

// v1.11
procedure TMainForm.Reconcile3DObjects1Click(Sender: TObject);
  var
    response, numTdosAdded: integer;
  begin
  numTdosAdded := 0;
  // ask if want to save file first
  if plantFileChanged then
    begin
    response := MessageDlg('Do you want to save your changes to '
        + extractFileName(domain.plantFileName)
        + chr(13) + 'before you reconcile its 3D objects'
        + chr(13) + 'with those in the current 3D object file?',
        mtConfirmation, mbYesNoCancel, 0);
    case response of
      idCancel: exit;
      idYes: self.menuFileSaveClick(self);
      idNo: ;
      end;
    end;
  if not domain.checkForExistingDefaultTdoLibrary then exit;
  if messageDlg(
    'You are about to add any 3D objects in the current plant file' + chr(13) + chr(13)
    + '    (' + domain.plantFileName + ')' + chr(13) + chr(13)
    + 'that are not already in the current 3D object library' + chr(13) + chr(13)
    + '    (' + domain.defaultTdoLibraryFileName + ')' + chr(13) + chr(13)
    +'into that library. Do you want to go ahead?'
    , mtConfirmation, [mbYes, mbNo], 0) = IDYES then
    begin
    numTdosAdded := domain.plantManager.reconcileFileWithTdoLibrary(
        domain.plantFileName, domain.defaultTdoLibraryFileName);
    if numTdosAdded <= 0 then
      messageDlg(
      'All the 3D objects in the current plant file' + chr(13) + chr(13)
      + '    (' + domain.plantFileName + ')' + chr(13) + chr(13)
      + 'were already in the current 3D object library' + chr(13) + chr(13)
      + '    (' + domain.defaultTdoLibraryFileName + ').'
      , mtInformation, [mbOK], 0)
    else
      messageDlg(
      intToStr(numTdosAdded) + ' 3D objects from the current plant file' + chr(13) + chr(13)
      + '    (' + domain.plantFileName + ')' + chr(13) + chr(13)
      + 'were copied to the current 3D object library' + chr(13) + chr(13)
      + '    (' + domain.defaultTdoLibraryFileName + ').'
      , mtInformation, [mbOK], 0);
    end;
  end;
// end v1.11

// v1.60 recent files menu
// PDF PORT removed empty parens
procedure TMainForm.updateFileMenuForOtherRecentFiles;
  var
    i, numSet: smallint;
    shortcutString: string;
    atLeastOneFileNameExists, showThis: boolean;
  begin
  with domain.options do
    begin
    atLeastOneFileNameExists := false;
    numSet := 0;
    for i := 0 to kMaxRecentFiles - 1 do
      begin
      if numSet+1 = 10 then
        shortcutString := '1&0'
      else
        shortcutString := '&' + intToStr(numSet+1);
      MenuFileReopen.items[i].caption := shortcutString + ' ' + recentFiles[kMaxRecentFiles-1-i];
      showThis := (recentFiles[kMaxRecentFiles-1-i] <> '') and (fileExists(recentFiles[kMaxRecentFiles-1-i]));
      MenuFileReopen.items[i].visible := showThis;
      if showThis then inc(numSet);
      if not atLeastOneFileNameExists then atLeastOneFileNameExists := showThis;
      end;
    end;
  MenuFileReopen.enabled := atLeastOneFileNameExists;
  end;

// v1.60 recent files menu
procedure TMainForm.Recent0Click(Sender: TObject);
  var index: smallint;
  begin
  index := kMaxRecentFiles - 1 - MenuFileReopen.indexOf(sender as TMenuItem);
  if not fileExists(domain.options.recentFiles[index]) then
    begin
    MessageDlg('Cannot find the file' + chr(13) + domain.options.recentFiles[index] + '.', mtError, [mbOK], 0);
    exit;
    end;
	if not self.askForSaveAndProceed then exit;
  self.openFile(domain.options.recentFiles[index]);
  end;

end.
