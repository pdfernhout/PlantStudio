// unit Umain

from conversion_common import *;
import uamendmt;
import uwizard;
import uturtle;
import ubreedr;
import uparams;
import umath;
import updcom;
import ubitmap;
import u3dexport;
import usupport;
import udomain;
import usection;
import ucollect;
import uplant;
import ucommand;
import delphi_compatability;

// const
kCursorModeSelectDrag = 0;
kCursorModeMagnify = 1;
kCursorModeScroll = 2;
kCursorModeRotate = 3;
kCursorModePosingSelect = 4;
kMinWidthOnScreen = 100;
kMinHeightOnScreen = 100;
kDrawNow = true;
kDontDrawYet = false;
kScaleAndMove = true;
kJustMove = false;
kAlwaysMove = true;
kOnlyMoveIfOffTheScreen = false;


// var
boolean plantFileChanged = false;


// var
TMainForm MainForm = new TMainForm();


// const
kBetweenGap = 4;
kSplitterDragToTopMinPixels = 100;
kSplitterDragToBottomMinPixelsInHorizMode = 160;
kSplitterDragToBottomMinPixelsInVertMode = 60;
kSplitterDragToLeftMinPixels = 100;
kSplitterDragToRightMinPixels = 260;
kPlantListChanged = true;
kPlantListNotChanged = false;
kHintRange = 1;
kMaxHintRangeForLargeAreas = 50;
kTabRotations = 0;
kTabParameters = 1;
kTabLifeCycle = 2;
kTabPosing = 3;
kTabStatistics = 4;
kTabNote = 5;
kTabHighest = 5;
kMaxMagnificationToTypeIn = 10000;
kEnableAllForms = true;
kDisableAllForms = false;
kDrawAllPlants = true;
kDrawOnlySelectedPlants = false;
kExpand = 0;
kCollapse = 1;
kExpandOrCollapse = 2;


// var
short pictureFileSaveAttemptsThisSession = 0;
short nozzleFileSaveAttemptsThisSession = 0;
 exportTo3DFileSaveAttemptsThisSession = [0] * (range(1, u3dexport.k3DExportTypeLast + 1) + 1);


public void setPlantCharacteristicsForAnimationFrame(PdPlant plant, short frame) {
    if (plant == null) {
        return;
    }
    if (udomain.domain.animationOptions.animateBy == udomain.kAnimateByAge) {
        if (frame <= 0) {
            plant.setAge(1);
        } else if (frame >= udomain.domain.animationOptions.frameCount - 1) {
            plant.setAge(plant.pGeneral.ageAtMaturity);
        } else {
            plant.setAge(udomain.domain.animationOptions.ageIncrement * frame);
        }
    } else if (udomain.domain.animationOptions.animateBy == udomain.kAnimateByXRotation) {
        if (udomain.domain.animationOptions.frameCount > 1) {
            plant.xRotation = udomain.domain.animationOptions.xRotationIncrement * frame;
        }
    }
}

// const
kProgressBarColor = delphi_compatability.clBlue;


// const
kScaleToFitMargin = 10;
kOffscreenMargin = 20;


// const
kSelectNoPosedPartString = "< Select None >";


// const
kNoPartSelected = "Selected part: (none)";


public void enableOrDisableSet(TLabel aLabel, TEdit anEdit, TSpinButton aSpin, TLabel anExtraLabel, boolean enable) {
    if (aLabel != null) {
        aLabel.Enabled = enable;
    }
    if (anEdit != null) {
        anEdit.Enabled = enable;
    }
    if (aSpin != null) {
        aSpin.Visible = enable;
    }
    if (anExtraLabel != null) {
        anExtraLabel.Enabled = enable;
    }
}


class TMainForm extends PdForm {
    public TMainMenu MainMenu;
    public TMenuItem MenuFile;
    public TMenuItem MenuFileNew;
    public TMenuItem MenuFileOpen;
    public TMenuItem MenuFileClose;
    public TMenuItem N1;
    public TMenuItem MenuFileSave;
    public TMenuItem MenuFileSaveAs;
    public TMenuItem N2;
    public TMenuItem MenuFileExit;
    public TMenuItem MenuEdit;
    public TMenuItem MenuEditUndo;
    public TMenuItem MenuEditRedo;
    public TMenuItem N3;
    public TMenuItem MenuEditCut;
    public TMenuItem MenuEditCopy;
    public TMenuItem MenuEditPaste;
    public TMenuItem MenuHelp;
    public TMenuItem MenuHelpTopics;
    public TMenuItem MenuHelpAbout;
    public TMenuItem MenuPlant;
    public TMenuItem MenuFilePlantMover;
    public TMenuItem MenuPlantRename;
    public TMenuItem MenuPlantBreed;
    public TMenuItem MenuPlantRandomize;
    public TMenuItem MenuPlantNew;
    public TMenuItem N7;
    public TPanel toolbarPanel;
    public TSpeedButton dragCursorMode;
    public TSpeedButton magnifyCursorMode;
    public TSpeedButton scrollCursorMode;
    public TPanel horizontalSplitter;
    public TPanel verticalSplitter;
    public TImage paletteImage;
    public TMenuItem MenuEditPreferences;
    public TImage visibleBitmap;
    public TPopupMenu PlantPopupMenu;
    public TMenuItem MenuFileSaveDrawingAs;
    public TMenuItem MenuFilePrintDrawing;
    public TMenuItem MenuEditCopyDrawing;
    public TMenuItem PopupMenuCut;
    public TMenuItem PopupMenuCopy;
    public TMenuItem PopupMenuPaste;
    public TMenuItem N6;
    public TMenuItem MenuEditDelete;
    public TMenuItem N5;
    public TPrintDialog PrintDialog;
    public TPanel sectionImagesPanel;
    public TImage Sections_FlowersPrimary;
    public TImage Sections_General;
    public TImage Sections_InflorPrimary;
    public TImage Sections_Meristems;
    public TImage Sections_Leaves;
    public TImage Sections_RootTop;
    public TImage Sections_Fruit;
    public TImage Sections_InflorSecondary;
    public TImage Sections_Internodes;
    public TImage Sections_SeedlingLeaves;
    public TImage Sections_FlowersSecondary;
    public TMenuItem PopupMenuRename;
    public TMenuItem PopupMenuRandomize;
    public TMenuItem PopupMenuBreed;
    public TSpeedButton rotateCursorMode;
    public TMenuItem MenuPlantExportToDXF;
    public TMenuItem MenuPlantMakeTimeSeries;
    public TMenuItem MenuWindow;
    public TMenuItem MenuWindowBreeder;
    public TMenuItem MenuWindowTimeSeries;
    public TMenuItem N12;
    public TMenuItem MenuWindowNumericalExceptions;
    public TTimer animateTimer;
    public TMenuItem MenuPlantAnimate;
    public TSpeedButton centerDrawing;
    public TMenuItem MenuOptions;
    public TMenuItem MenuOptionsShowLongButtonHints;
    public TMenuItem MenuOptionsShowParameterHints;
    public TMenuItem MenuOptionsShowSelectionRectangles;
    public TImage paramPanelOpenArrowImage;
    public TImage paramPanelClosedArrowImage;
    public TPanel plantListPanel;
    public TPaintBox progressPaintBox;
    public TPanel plantFocusPanel;
    public TPanel lifeCyclePanel;
    public TImage lifeCycleGraphImage;
    public TLabel timeLabel;
    public TLabel selectedPlantNameLabel;
    public TPanel lifeCycleEditPanel;
    public TLabel daysAndSizeLabel;
    public TLabel ageAndSizeLabel;
    public TEdit lifeCycleDaysEdit;
    public TSpinButton lifeCycleDaysSpin;
    public TPanel lifeCycleDragger;
    public TScrollBox statsScrollBox;
    public TTabSet tabSet;
    public TPanel parametersPanel;
    public TScrollBox parametersScrollBox;
    public TMenuItem PopupMenuMakeTimeSeries;
    public TMenuItem PopupMenuAnimate;
    public TMenuItem MenuLayout;
    public TMenuItem MenuLayoutSelectAll;
    public TMenuItem MenuLayoutDeselect;
    public TMenuItem MenuLayoutHide;
    public TMenuItem MenuLayoutHideOthers;
    public TMenuItem MenuLayoutShow;
    public TMenuItem N18;
    public TMenuItem MenuLayoutBringForward;
    public TMenuItem MenuLayoutSendBack;
    public TMenuItem N19;
    public TMenuItem MenuLayoutHorizontalOrientation;
    public TMenuItem MenuLayoutVerticalOrientation;
    public TMenuItem MenuLayoutScaleToFit;
    public TMenuItem MenuLayoutViewOnePlantAtATime;
    public TMenuItem MenuLayoutMakeBouquet;
    public TLabel maxSizeAxisLabel;
    public TImage plantFileChangedImage;
    public TImage fileChangedImage;
    public TImage fileNotChangedImage;
    public TDrawGrid plantListDrawGrid;
    public TMenuItem MenuEditDuplicate;
    public TMenuItem N8;
    public TMenuItem MenuPlantNewUsingLastWizardSettings;
    public TMenuItem N4;
    public TPopupMenu paramPopupMenu;
    public TMenuItem paramPopupMenuHelp;
    public TMenuItem N15;
    public TMenuItem paramPopupMenuExpand;
    public TMenuItem paramPopupMenuCollapse;
    public TMenuItem AfterRegisterMenuSeparator;
    public TMenuItem MenuFileTdoMover;
    public TSpeedButton animateGrowth;
    public TMenuItem MenuFileMakePainterNozzle;
    public TImage unregisteredExportReminder;
    public TMenuItem MenuFileMakePainterAnimation;
    public TMenuItem N17;
    public TMenuItem N13;
    public TMenuItem MenuHelpRegister;
    public TMenuItem MenuHelpSuperSpeedTour;
    public TMenuItem MenuHelpTutorial;
    public TMenuItem MenuEditCopyAsText;
    public TMemo plantsAsTextMemo;
    public TMenuItem MenuEditPasteAsText;
    public TMenuItem N16;
    public TMenuItem MenuOptionsFastDraw;
    public TMenuItem MenuOptionsMediumDraw;
    public TMenuItem MenuOptionsBestDraw;
    public TMenuItem MenuOptionsCustomDraw;
    public TMenuItem MenuOptionsUsePlantBitmaps;
    public TImage plantBitmapsIndicatorImage;
    public TImage plantBitmapsGreenImage;
    public TImage noPlantBitmapsImage;
    public TImage plantBitmapsYellowImage;
    public TImage plantBitmapsRedImage;
    public TLabel animatingLabel;
    public TMenuItem N22;
    public TMenuItem MenuPlantZeroRotations;
    public TMenuItem PopupMenuZeroRotations;
    public TPanel rotationsPanel;
    public TLabel xRotationLabel;
    public TEdit xRotationEdit;
    public TSpinButton xRotationSpin;
    public TLabel yRotationLabel;
    public TEdit yRotationEdit;
    public TSpinButton yRotationSpin;
    public TLabel zRotationLabel;
    public TEdit zRotationEdit;
    public TSpinButton zRotationSpin;
    public TSpeedButton resetRotations;
    public TLabel rotationLabel;
    public TComboBox magnificationPercent;
    public TMenuItem N10;
    public TMenuItem Reconcile3DObjects1;
    public TPanel notePanel;
    public TMemo noteMemo;
    public TLabel noteLabel;
    public TSpeedButton noteEdit;
    public TMenuItem PopupMenuEditNote;
    public TMenuItem MenuPlantEditNote;
    public TMenuItem N25;
    public TMenuItem paramPopupMenuCopyName;
    public TMenuItem MenuPlantExportToPOV;
    public TMenuItem MenuFileExport;
    public TMenuItem Recent0;
    public TMenuItem Recent1;
    public TMenuItem Recent2;
    public TMenuItem Recent3;
    public TMenuItem Recent4;
    public TMenuItem MenuFileReopen;
    public TMenuItem Recent5;
    public TMenuItem Recent6;
    public TMenuItem Recent7;
    public TMenuItem Recent8;
    public TMenuItem Recent9;
    public TSpeedButton viewFreeFloating;
    public TSpeedButton viewOneOnly;
    public TMenuItem MenuOptionsDrawAs;
    public TSpeedButton drawingAreaOnTop;
    public TSpeedButton drawingAreaOnSide;
    public TMenuItem MenuLayoutDrawingAreaOn;
    public TMenuItem MenuLayoutView;
    public TMenuItem MenuLayoutViewFreeFloating;
    public TImage Sections_FlowersPrimaryAdvanced;
    public TLabel sizingLabel;
    public TEdit drawingScaleEdit;
    public TSpinButton drawingScaleSpin;
    public TLabel drawingScalePixelsPerMmLabel;
    public TSpeedButton packPlants;
    public TLabel locationLabel;
    public TLabel xLocationLabel;
    public TEdit xLocationEdit;
    public TSpinButton xLocationSpin;
    public TLabel yLocationLabel;
    public TEdit yLocationEdit;
    public TSpinButton yLocationSpin;
    public TLabel locationPixelsLabel;
    public TLabel arrangementPlantName;
    public TSpeedButton alignTops;
    public TSpeedButton alignBottoms;
    public TSpeedButton alignLeft;
    public TSpeedButton alignRight;
    public TSpeedButton makeEqualWidth;
    public TSpeedButton makeEqualHeight;
    public TMenuItem MenuLayoutAlign;
    public TMenuItem MenuLayoutAlignTops;
    public TMenuItem MenuLayoutAlignBottoms;
    public TMenuItem MenuLayoutAlignLeftSides;
    public TMenuItem MenuLayoutAlignRightSides;
    public TMenuItem MenuLayoutSize;
    public TMenuItem MenuLayoutSizeSameHeight;
    public TMenuItem MenuLayoutSizeSameWidth;
    public TMenuItem MenuLayoutPack;
    public TLabel parametersPlantName;
    public TMenuItem MenuPlantExportTo3DS;
    public TMenuItem N9;
    public TPanel posingPanel;
    public TLabel posingPlantName;
    public TMenuItem MenuOptionsGhostHiddenParts;
    public TPanel posingDetailsPanel;
    public TLabel posingXRotationLabel;
    public TLabel posingYRotationLabel;
    public TLabel posingZRotationLabel;
    public TLabel posingScaleMultiplierPercent;
    public TCheckBox posingHidePart;
    public TEdit posingXRotationEdit;
    public TSpinButton posingXRotationSpin;
    public TEdit posingYRotationEdit;
    public TSpinButton posingYRotationSpin;
    public TEdit posingZRotationEdit;
    public TSpinButton posingZRotationSpin;
    public TCheckBox posingAddExtraRotation;
    public TCheckBox posingMultiplyScale;
    public TMenuItem MenuOptionsHighlightPosedParts;
    public TMenuItem MenuOptionsPosing;
    public TMenuItem N20;
    public TMenuItem N21;
    public TMenuItem MenuFileMove;
    public TLabel posingScaleMultiplierLabel;
    public TLabel posingLengthMultiplierPercent;
    public TLabel posingLengthMultiplierLabel;
    public TLabel posingWidthMultiplierPercent;
    public TLabel posingWidthMultiplierLabel;
    public TCheckBox posingMultiplyScaleAllPartsAfter;
    public TMenuItem MenuOptionsShowBoundsRectangles;
    public TMenuItem MenuOptionsDrawRectangles;
    public TMenuItem MenuOptionsHints;
    public TMenuItem MenuFileSaveJPEG;
    public TEdit posingScaleMultiplierEdit;
    public TSpinButton posingScaleMultiplierSpin;
    public TEdit posingLengthMultiplierEdit;
    public TSpinButton posingLengthMultiplierSpin;
    public TEdit posingWidthMultiplierEdit;
    public TSpinButton posingWidthMultiplierSpin;
    public TMenuItem MenuOptionsHidePosing;
    public TMenuItem UndoMenuEditUndoRedoList;
    public TMenuItem MenuPlantExportToOBJ;
    public TMenuItem MenuPlantExportToVRML;
    public TMenuItem MenuPlantExportToLWO;
    public TComboBox sectionsComboBox;
    public TMenuItem paramPopupMenuExpandAllInSection;
    public TMenuItem paramPopupMenuCollapseAllInSection;
    public TMenuItem N11;
    public TLabel hideExtraLabel;
    public TLabel rotationDegreesLabel;
    public TPanel posingColorsPanel;
    public TLabel posingLineColorLabel;
    public TLabel posingFrontfaceColorLabel;
    public TLabel posingBackfaceColorLabel;
    public TCheckBox posingChangeColors;
    public TCheckBox posingChangeAllColorsAfter;
    public TPanel posingLineColor;
    public TPanel posingFrontfaceColor;
    public TPanel posingBackfaceColor;
    public TSpeedButton posingSelectionCursorMode;
    public TLabel posedPartsLabel;
    public TComboBox posedPlantParts;
    public TSpeedButton posingHighlight;
    public TSpeedButton posingGhost;
    public TSpeedButton posingNotShown;
    public TLabel selectedPartLabel;
    public TSpeedButton posingPosePart;
    public TSpeedButton posingUnposePart;
    public TLabel posingMultiplyScaleAllPartsAfterLabel;
    public TMenuItem sectionPopupMenuHelp;
    public TImage Sections_Orthogonal;
    public TBitmap drawingBitmap;
    public PdCommandList commandList;
    public PdPaintBoxWithPalette drawingPaintBox;
    public PdStatsPanel statsPanel;
    public TRect invalidDrawingRect;
    public boolean internalChange;
    public boolean inFormCreation;
    public boolean inFileOpen;
    public boolean lastSaveProceeded;
    public boolean resizingAtStart;
    public TListCollection plants;
    public TList selectedPlants;
    public short numPlantsInClipboard;
    public int lastSingleClickPlantIndex;
    public boolean justDoubleClickedOnDrawGrid;
    public boolean rubberBanding;
    public boolean rubberBandNeedToRedraw;
    public TPoint rubberBandStartDragPoint;
    public TPoint rubberBandLastDrawPoint;
    public boolean drawing;
    public PdCommand animateCommand;
    public long drawProgressMax;
    public short cursorModeForDrawing;
    public boolean actionInProgress;
    public boolean mouseMoveActionInProgress;
    public boolean lifeCycleDragging;
    public boolean lifeCycleDraggingNeedToRedraw;
    public short lifeCycleDraggingStartPos;
    public short lifeCycleDraggingLastDrawPos;
    public TPoint cursorPosInDrawingPaintBox;
    public boolean horizontalSplitterDragging;
    public boolean verticalSplitterDragging;
    public boolean horizontalSplitterNeedToRedraw;
    public boolean verticalSplitterNeedToRedraw;
    public int horizontalSplitterStartPos;
    public int verticalSplitterStartPos;
    public int horizontalSplitterLastDrawPos;
    public int verticalSplitterLastDrawPos;
    public int lastWidth;
    public int lastHeight;
    public int hintX;
    public int hintY;
    public boolean hintActive;
    public String lastHintString;
    public boolean backTabbingInParametersPanel;
    public PdParameterPanel selectedParameterPanel;
    public long selectedPlantPartID;
    public long mouseDownSelectedPlantPartID;
    public String selectedPlantPartType;
    public String mouseDownSelectedPlantPartType;
    
    //$R *.DFM
    //in each direction, so box is 100 x 100
    public void FormCreate(TObject Sender) {
        TRect tempBoundsRect = new TRect();
        
        UNRESOLVED.cursor_startWait;
        try {
            delphi_compatability.Application.helpFile = ExtractFilePath(delphi_compatability.Application.exeName) + "PlantStudio.hlp";
            delphi_compatability.Application.OnActivate = this.FormActivate;
            if (udomain.domain == null) {
                throw new GeneralException.create("Problem: Nil domain in method TMainForm.FormCreate.");
            }
            // domain must exist when this is created; use this pointer to shorten code
            this.plants = udomain.domain.plantManager.plants;
            this.updateForRegistrationChange();
            // turn off panel bevels 
            this.plantListPanel.BevelOuter = UNRESOLVED.bvNone;
            this.plantFocusPanel.BevelOuter = UNRESOLVED.bvNone;
            this.plantListDrawGrid.DragCursor = UNRESOLVED.crDragPlant;
            // save height and width for resizing use 
            this.lastWidth = this.clientWidth;
            this.lastHeight = this.clientHeight;
            this.inFormCreation = true;
            // application options 
            delphi_compatability.Application.OnShowHint = this.DoShowHint;
            // cfk played with menu hints - to use menu hints, respond to this and display the hint in a window or status panel
            // Application.OnHint := DoMenuHint;    
            delphi_compatability.Application.ShowHint = true;
            // creation of dependent objects and setting them up 
            this.selectedPlants = delphi_compatability.TList().Create();
            this.commandList = ucommand.PdCommandList().create();
            this.commandList.setNewUndoLimit(udomain.domain.options.undoLimit);
            this.commandList.setNewObjectUndoLimit(udomain.domain.options.undoLimitOfPlants);
            this.drawingPaintBox = ubitmap.PdPaintBoxWithPalette().Create(this);
            this.drawingPaintBox.Parent = this;
            this.drawingPaintBox.OnPaint = this.drawingPaintBoxPaint;
            this.drawingPaintBox.OnMouseDown = this.PaintBoxMouseDown;
            this.drawingPaintBox.OnMouseMove = this.PaintBoxMouseMove;
            this.drawingPaintBox.OnMouseUp = this.PaintBoxMouseUp;
            this.drawingPaintBox.OnEndDrag = this.PaintBoxEndDrag;
            this.drawingPaintBox.OnDragOver = this.PaintBoxDragOver;
            this.drawingPaintBox.DragCursor = UNRESOLVED.crDragPlant;
            this.drawingPaintBox.PopupMenu = this.PlantPopupMenu;
            this.drawingBitmap = delphi_compatability.TBitmap().Create();
            this.statsPanel = UNRESOLVED.PdStatsPanel.create(this);
            this.statsPanel.parent = this.statsScrollBox;
            this.statsPanel.parentFont = false;
            // hints 
            this.hintActive = false;
            this.lastHintString = "";
            // intial settings of stored info 
            this.tabSet.tabIndex = kTabRotations;
            this.dragCursorMode.Down = true;
            // loading info 
            this.loadSectionsIntoListBox();
            switch (udomain.domain.options.drawSpeed) {
                case udomain.kDrawFast:
                    // updating 
                    this.MenuOptionsFastDraw.checked = true;
                    break;
                case udomain.kDrawMedium:
                    this.MenuOptionsMediumDraw.checked = true;
                    break;
                case udomain.kDrawBest:
                    this.MenuOptionsBestDraw.checked = true;
                    break;
                case udomain.kDrawCustom:
                    this.MenuOptionsCustomDraw.checked = true;
                    break;
            this.updateMenusForUndoRedo();
            this.updatePasteMenuForClipboardContents();
            if (this.sectionsComboBox.Items.Count > 0) {
                this.sectionsComboBox.ItemIndex = 0;
                this.updateParameterPanelsForSectionChange();
            }
            //v2.0
            this.rotationsPanel.Visible = true;
            UNRESOLVED.setPixelFormatBasedOnScreenForBitmap(this.drawingBitmap);
            // set size and splitters as saved in domain 
            // keep window on screen - left corner of title bar 
            tempBoundsRect = udomain.domain.mainWindowRect;
            if ((tempBoundsRect.Left != 0) || (tempBoundsRect.Right != 0) || (tempBoundsRect.Top != 0) || (tempBoundsRect.Bottom != 0)) {
                if (tempBoundsRect.Left > delphi_compatability.Screen.Width - kMinWidthOnScreen) {
                    tempBoundsRect.Left = delphi_compatability.Screen.Width - kMinWidthOnScreen;
                }
                if (tempBoundsRect.Top > delphi_compatability.Screen.Height - kMinHeightOnScreen) {
                    tempBoundsRect.Top = delphi_compatability.Screen.Height - kMinHeightOnScreen;
                }
                this.setBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom);
            }
            if (udomain.domain.horizontalSplitterPos > 0) {
                this.horizontalSplitter.Top = udomain.domain.horizontalSplitterPos;
            } else {
                this.horizontalSplitter.Top = this.clientHeight / 2;
            }
            if (udomain.domain.verticalSplitterPos > 0) {
                this.verticalSplitter.Left = udomain.domain.verticalSplitterPos;
            } else {
                this.verticalSplitter.Left = this.clientWidth / 3;
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void loadPlantFileAtStartup() {
        UNRESOLVED.cursor_startWait;
        try {
            if (udomain.domain.plantFileLoaded) {
                // if file loaded at startup, update for it, else act as if they picked new 
                UNRESOLVED.startWaitMessage("Drawing...");
                try {
                    this.updateForPlantFile();
                } finally {
                    UNRESOLVED.stopWaitMessage;
                }
            } else {
                this.MenuFileNewClick(this);
            }
            if (UNRESOLVED.splashForm != null) {
                UNRESOLVED.splashForm.hide;
            }
            this.updateForChangeToDomainOptions();
            this.updateFileMenuForOtherRecentFiles();
            this.selectedPlantPartID = -1;
            this.inFormCreation = false;
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void FormActivate(TObject Sender) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        this.MenuEditPasteAsText.enabled = (UNRESOLVED.Clipboard.hasFormat(UNRESOLVED.CF_TEXT)) && (udomain.domain.plantFileLoaded);
    }
    
    public void showWelcomeForm() {
        TWelcomeForm welcomeForm = new TWelcomeForm();
        
        if (udomain.domain.options.hideWelcomeForm) {
            return;
        }
        welcomeForm = UNRESOLVED.TWelcomeForm.create(delphi_compatability.Application);
        try {
            if (welcomeForm.showModal != mrCancel) {
                switch (welcomeForm.whatToDo) {
                    case UNRESOLVED.kReadSuperSpeedTour:
                        delphi_compatability.Application.HelpJump("Super-Speed_Tour");
                        break;
                    case UNRESOLVED.kReadTutorial:
                        delphi_compatability.Application.HelpJump("Tutorial");
                        break;
                    case UNRESOLVED.kMakeNewPlant:
                        this.MenuPlantNewClick(this);
                        break;
                    case UNRESOLVED.kOpenPlantLibrary:
                        if (udomain.domain.plantFileName == "") {
                            udomain.domain.plantFileName = ExtractFilePath(delphi_compatability.Application.exeName);
                        }
                        this.MenuFileOpenClick(this);
                        break;
                    case UNRESOLVED.kStartUsingProgram:
                        break;
            }
            udomain.domain.options.hideWelcomeForm = welcomeForm.hideWelcomeForm.checked;
        } finally {
            welcomeForm.free;
            welcomeForm = null;
        }
    }
    
    public void FormDestroy(TObject Sender) {
        this.commandList.free;
        this.commandList = null;
        this.drawingBitmap.free;
        this.drawingBitmap = null;
        this.selectedPlants.free;
        this.selectedPlants = null;
        // don't free statsPanel because we are the owner 
    }
    
    // ------------------------------------------------------------------------- *file menu 
    public void MenuFileNewClick(TObject Sender) {
        if (!this.askForSaveAndProceed()) {
            return;
        }
        udomain.domain.resetForNoPlantFile();
        this.updateForNoPlantFile();
        udomain.domain.resetForEmptyPlantFile();
        this.updateForPlantFile();
        // new v1.4 reset to 100% magnification on new file
        this.magnificationPercent.Text = "100%";
        this.changeMagnificationWithoutClick();
    }
    
    public void WMDropFiles(TWMDropFiles Msg) {
         CFileName = [0] * (range(0, UNRESOLVED.MAX_PATH + 1) + 1);
        
        try {
            if (UNRESOLVED.DragQueryFile(Msg.Drop, 0, CFileName, UNRESOLVED.MAX_PATH) > 0) {
                if (UNRESOLVED.pos(".PLA", uppercase(CFileName)) <= 0) {
                    return;
                }
                if (!this.askForSaveAndProceed()) {
                    return;
                }
                this.openFile(CFileName);
                Msg.Result = 0;
            }
        } finally {
            UNRESOLVED.DragFinish(Msg.Drop);
        }
    }
    
    public void MenuFileOpenClick(TObject Sender) {
        String fileNameWithPath = "";
        
        if (!this.askForSaveAndProceed()) {
            return;
        }
        fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypePlant, udomain.domain.plantFileName, "Choose a plant file");
        if (fileNameWithPath == "") {
            return;
        }
        this.openFile(fileNameWithPath);
    }
    
    // dependent objects 
    // general 
    // plant handling 
    // selecting plants with rubber banding 
    // drawing and progress 
    // mouse movement 
    // resizing and splitting 
    // hints 
    // parameters panel 
    // posings panel
    // file menu 
    public void openFile(String fileNameWithPath) {
        udomain.domain.resetForNoPlantFile();
        this.updateForNoPlantFile();
        try {
            this.inFileOpen = true;
            try {
                UNRESOLVED.startWaitMessage("Opening " + ExtractFileName(fileNameWithPath));
                udomain.domain.load(fileNameWithPath);
            } catch (Exception E) {
                UNRESOLVED.stopWaitMessage;
                ShowMessage(E.message);
                ShowMessage("Could not load file " + fileNameWithPath);
                return;
            }
            this.updateForPlantFile();
            UNRESOLVED.stopWaitMessage;
        } finally {
            this.inFileOpen = false;
        }
    }
    
    public void MenuFileCloseClick(TObject Sender) {
        if (!this.askForSaveAndProceed()) {
            return;
        }
        udomain.domain.resetForNoPlantFile();
        this.updateForPlantFile();
    }
    
    // returns false if user canceled leaving
    public boolean askForSaveAndProceed() {
        result = false;
        int messageBoxResult = 0;
        
        result = true;
        if (!plantFileChanged) {
            return result;
        }
        //cfk fix - put help context in - for all messageDlgs 
        messageBoxResult = MessageDialog("Save changes to " + ExtractFileName(udomain.domain.plantFileName) + "?", mtConfirmation, mbYesNoCancel, 0);
        switch (messageBoxResult) {
            case delphi_compatability.IDCANCEL:
                result = false;
                break;
            case delphi_compatability.IDYES:
                this.MenuFileSaveClick(this);
                result = this.lastSaveProceeded;
                break;
            case delphi_compatability.IDNO:
                result = true;
                break;
            default:
                ShowMessage("Error with save request dialog.");
                result = true;
                break;
        return result;
    }
    
    public void MenuFileSaveClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        
        if (UNRESOLVED.pos(uppercase(udomain.kUnsavedFileName), uppercase(ExtractFileName(udomain.domain.plantFileName))) > 0) {
            this.MenuFileSaveAsClick(this);
            return;
        }
        this.lastSaveProceeded = usupport.getFileSaveInfo(usupport.kFileTypePlant, usupport.kDontAskForFileName, udomain.domain.plantFileName, fileInfo);
        if (!this.lastSaveProceeded) {
            return;
        }
        try {
            usupport.startFileSave(fileInfo);
            UNRESOLVED.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...");
            udomain.domain.save(fileInfo.tempFile);
            fileInfo.writingWasSuccessful = true;
        } finally {
            UNRESOLVED.stopWaitMessage;
            usupport.cleanUpAfterFileSave(fileInfo);
            this.setPlantFileChanged(false);
            udomain.domain.updateRecentFileNames(fileInfo.newFile);
            this.clearCommandList();
        }
    }
    
    public void setPlantFileChanged(boolean fileChanged) {
        plantFileChanged = fileChanged;
        if (this.plantFileChangedImage != null) {
            if (plantFileChanged) {
                this.plantFileChangedImage.Picture = this.fileChangedImage.Picture;
            } else {
                this.plantFileChangedImage.Picture = this.fileNotChangedImage.Picture;
            }
            this.plantFileChangedImage.Invalidate();
            this.plantFileChangedImage.Refresh();
        }
    }
    
    public void MenuFileSaveAsClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        
        this.lastSaveProceeded = usupport.getFileSaveInfo(usupport.kFileTypePlant, usupport.kAskForFileName, udomain.domain.plantFileName, fileInfo);
        if (!this.lastSaveProceeded) {
            return;
        }
        try {
            usupport.startFileSave(fileInfo);
            UNRESOLVED.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...");
            udomain.domain.save(fileInfo.tempFile);
            fileInfo.writingWasSuccessful = true;
        } finally {
            UNRESOLVED.stopWaitMessage;
            usupport.cleanUpAfterFileSave(fileInfo);
            this.setPlantFileChanged(false);
            this.clearCommandList();
        }
        udomain.domain.plantFileName = fileInfo.newFile;
        udomain.domain.lastOpenedPlantFileName = udomain.domain.plantFileName;
        udomain.domain.updateRecentFileNames(udomain.domain.lastOpenedPlantFileName);
        this.caption = this.captionForFile();
    }
    
    public void MenuFilePlantMoverClick(TObject Sender) {
        TMoverForm mover = new TMoverForm();
        int response = 0;
        
        if (plantFileChanged) {
            response = MessageDialog("Do you want to save your changes to " + ExtractFileName(udomain.domain.plantFileName) + chr(13) + "before you use the plant mover?", mtConfirmation, mbYesNoCancel, 0);
            switch (response) {
                case delphi_compatability.IDCANCEL:
                    return;
                    break;
                case delphi_compatability.IDYES:
                    this.MenuFileSaveClick(this);
                    break;
                case delphi_compatability.IDNO:
                    break;
        }
        mover = UNRESOLVED.TMoverForm.create(this);
        if (mover == null) {
            throw new GeneralException.create("Problem: Could not create plant mover window.");
        }
        try {
            mover.showModal;
            //in case mover copied something
            this.updatePasteMenuForClipboardContents();
            if (mover.changedCurrentPlantFile) {
                if (mover.untitledDomainFileSavedAs != "") {
                    udomain.domain.plantFileName = mover.untitledDomainFileSavedAs;
                }
                // cfk fix put help context in 
                response = MessageDialog("The current plant file has changed." + chr(13) + "Do you want to reload the changed file?", mtConfirmation, {mbYes, mbNo, }, 0);
                if (response == delphi_compatability.IDYES) {
                    try {
                        UNRESOLVED.startWaitMessage("Opening " + ExtractFileName(udomain.domain.plantFileName));
                        this.updateForNoPlantFile();
                        udomain.domain.load(udomain.domain.plantFileName);
                    } catch (Exception E) {
                        UNRESOLVED.stopWaitMessage;
                        ShowMessage(E.message);
                        ShowMessage("Could not load file " + udomain.domain.plantFileName + ".");
                        return;
                    }
                    this.updateForPlantFile();
                    UNRESOLVED.stopWaitMessage;
                }
            }
        } finally {
            mover.free;
            mover = null;
        }
    }
    
    public void MenuFileTdoMoverClick(TObject Sender) {
        TTdoMoverForm mover = new TTdoMoverForm();
        
        mover = UNRESOLVED.TTdoMoverForm.create(this);
        if (mover == null) {
            throw new GeneralException.create("Problem: Could not create 3D object mover window.");
        }
        try {
            mover.showModal;
        } finally {
            mover.free;
            mover = null;
        }
    }
    
    public void WMQueryEndSession(TWMQueryEndSession message) {
        super.WMQueryEndSession();
        if (!this.askForSaveAndProceed()) {
            // prevents windows from shutting down
            message.result = 0;
        } else if (!this.cleanUpBeforeExit()) {
            message.result = 0;
        }
    }
    
    public void MenuFileExitClick(TObject Sender) {
        if (!this.askForSaveAndProceed()) {
            return;
        } else if (!this.cleanUpBeforeExit()) {
            return;
        }
        delphi_compatability.Application.Terminate();
    }
    
    public void FormClose(TObject Sender, TCloseAction Action) {
        if (!this.askForSaveAndProceed()) {
            // same as exit, but can't call exit because we have to set the action flag 
            Action = delphi_compatability.TCloseAction.caNone;
        } else if (!this.cleanUpBeforeExit()) {
            Action = delphi_compatability.TCloseAction.caNone;
        }
    }
    
    // returns false if user cancels quit
    public boolean cleanUpBeforeExit() {
        result = false;
        int response = 0;
        boolean okayToQuit = false;
        double randomNumber = 0.0;
        double lowerLimit = 0.0;
        double upperLimit = 0.0;
        
        result = true;
        udomain.domain.mainWindowRect = Rect(UNRESOLVED.left, UNRESOLVED.top, UNRESOLVED.width, UNRESOLVED.height);
        udomain.domain.horizontalSplitterPos = this.horizontalSplitter.Top;
        udomain.domain.verticalSplitterPos = this.verticalSplitter.Left;
        udomain.domain.breederWindowRect = Rect(UNRESOLVED.left, UNRESOLVED.top, UNRESOLVED.width, UNRESOLVED.height);
        //FIX unresolved WITH expression: UNRESOLVED.TimeSeriesForm
        udomain.domain.timeSeriesWindowRect = Rect(UNRESOLVED.left, UNRESOLVED.top, UNRESOLVED.width, UNRESOLVED.height);
        //FIX unresolved WITH expression: UNRESOLVED.DebugForm
        udomain.domain.debugWindowRect = Rect(UNRESOLVED.left, UNRESOLVED.top, UNRESOLVED.width, UNRESOLVED.height);
        if (udomain.domain.useIniFile) {
            okayToQuit = this.storeIniFile();
            if (!okayToQuit) {
                result = false;
                return result;
            }
        }
        // start putting up reminder after one hour
        lowerLimit = 1.0 / 24.0;
        if ((!udomain.domain.registered) && (udomain.domain.accumulatedUnregisteredTime > lowerLimit)) {
            UNRESOLVED.Randomize;
            randomNumber = UNRESOLVED.random;
            // v2 changed this - used to get to saturation after 24 hrs, changed to 12 - more reminding
            // almost always after 12 hrs
            upperLimit = umath.min(udomain.domain.accumulatedUnregisteredTime / (12.0 / 24.0), 0.9);
            if ((randomNumber < upperLimit)) {
                UNRESOLVED.aboutForm.initializeWithWhetherClosingProgram(true);
                response = UNRESOLVED.aboutForm.showModal;
                this.updateForRegistrationChange();
                if (response == mrCancel) {
                    result = false;
                    return result;
                }
            }
        }
        // have to clear out parameter panels before leaving, for some reason was making program crash
        //    but only if tdo components existed at the time of leaving the program. this works for now,
        //    but it would be better to understand why it was happening. 
        this.sectionsComboBox.ItemIndex = -1;
        this.updateParameterPanelsForSectionChange();
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_QUIT, 0);
        return result;
    }
    
    public boolean storeIniFile() {
        result = false;
        boolean fileSavedOK = false;
        boolean choseAnotherFileName = false;
        byte buttonPressed = 0;
        TSaveDialog saveDialog = new TSaveDialog();
        
        result = true;
        fileSavedOK = false;
        choseAnotherFileName = false;
        while (!fileSavedOK) {
            try {
                udomain.domain.storeProfileInformation();
                fileSavedOK = true;
            } catch (Exception e) {
                fileSavedOK = false;
            }
            if (!fileSavedOK) {
                buttonPressed = MessageDialog("Could not save settings to " + chr(13) + chr(13) + "  " + udomain.domain.iniFileName + chr(13) + chr(13) + "Would you like to save them to another file?", delphi_compatability.TMsgDlgType.mtError, mbYesNoCancel, 0);
                switch (buttonPressed) {
                    case delphi_compatability.IDYES:
                        saveDialog = delphi_compatability.TSaveDialog().Create(delphi_compatability.Application);
                        try {
                            saveDialog.FileName = udomain.domain.iniFileName;
                            saveDialog.Filter = "Ini files (*.ini)|*.ini|All files (*.*)|*.*";
                            saveDialog.DefaultExt = "ini";
                            saveDialog.Options = saveDialog.Options + {delphi_compatability.TOpenOption.ofPathMustExist, delphi_compatability.TOpenOption.ofOverwritePrompt, delphi_compatability.TOpenOption.ofHideReadOnly, delphi_compatability.TOpenOption.ofNoReadOnlyReturn, };
                            result = saveDialog.Execute();
                            if (result) {
                                udomain.domain.iniFileName = saveDialog.FileName;
                                choseAnotherFileName = true;
                            }
                        } finally {
                            saveDialog.free;
                        }
                        if (!result) {
                            return result;
                        }
                        break;
                    case delphi_compatability.IDNO:
                        return result;
                        break;
                    case delphi_compatability.IDCANCEL:
                        result = false;
                        return result;
                        break;
            }
        }
        if (fileSavedOK && choseAnotherFileName) {
            ShowMessage("Your settings have been saved in " + chr(13) + chr(13) + "  " + udomain.domain.iniFileName + chr(13) + chr(13) + "But PlantStudio will load the original settings file again at startup." + chr(13) + "To use this settings file at startup, search in the help system" + chr(13) + "for \"alternate settings file\".");
        }
        return result;
    }
    
    // ---------------------------------------------------------------------------- *edit menu 
    public void MenuEditUndoClick(TObject Sender) {
        this.commandList.undoLast();
        // commands handle updating if it has to do with plant list, so only update drawing part here 
        this.updateForPossibleChangeToDrawing();
    }
    
    public void UndoMenuEditUndoRedoListClick(TObject Sender) {
        TUndoRedoListForm undoRedoListForm = new TUndoRedoListForm();
        int response = 0;
        PdCommand newCommand = new PdCommand();
        int i = 0;
        
        undoRedoListForm = UNRESOLVED.TUndoRedoListForm.create(this);
        if (undoRedoListForm == null) {
            throw new GeneralException.create("Problem: Could not create undo/redo list window.");
        }
        try {
            undoRedoListForm.initializeWithCommandList(this.commandList);
            response = undoRedoListForm.showModal;
            if (response == mrOK) {
                try {
                    this.enableOrDisableAllForms(kDisableAllForms);
                    UNRESOLVED.startWaitMessage("Multiple undo/redo in progress; please wait...");
                    if (undoRedoListForm.undoToIndex >= 0) {
                        for (i = 0; i <= undoRedoListForm.undoToIndex; i++) {
                            this.commandList.undoLast();
                        }
                    } else if (undoRedoListForm.redoToIndex >= 0) {
                        for (i = 0; i <= undoRedoListForm.redoToIndex; i++) {
                            this.commandList.redoLast();
                        }
                    }
                } finally {
                    this.updateForPossibleChangeToDrawing();
                    UNRESOLVED.stopWaitMessage;
                    this.enableOrDisableAllForms(kEnableAllForms);
                }
            }
        } finally {
            undoRedoListForm.free;
        }
    }
    
    public void MenuEditRedoClick(TObject Sender) {
        this.commandList.redoLast();
        this.updateForPossibleChangeToDrawing();
    }
    
    public void MenuEditCutClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdRemoveCommand().createWithListOfPlantsAndClipboardFlag(this.selectedPlants, updcom.kCopyToClipboard);
        //command calls copy, which enables paste menu item
        this.doCommand(newCommand);
    }
    
    public void MenuEditCopyClick(TObject Sender) {
        this.copySelectedPlantsToClipboard();
    }
    
    public void MenuEditCopyAsTextClick(TObject Sender) {
        int i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.selectedPlants.Count > 0) {
            UNRESOLVED.Clipboard.clear;
            this.plantsAsTextMemo.Clear();
            for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                plant = uplant.PdPlant(this.selectedPlants.Items[i]);
                if (plant == null) {
                    continue;
                }
                plant.writeToMainFormMemoAsText();
            }
            this.plantsAsTextMemo.SelectAll();
            this.plantsAsTextMemo.CutToClipboard();
        }
    }
    
    public void MenuEditPasteAsTextClick(TObject Sender) {
        TextFile fakeTextFile = new TextFile();
        PdPlant plant = new PdPlant();
        TList newPlants = new TList();
        PdCommand newCommand = new PdCommand();
        String aLine = "";
        String secondLine = "";
        String plantName = "";
        short i = 0;
        short startLine = 0;
        short endLine = 0;
        
        newPlants = null;
        if (!UNRESOLVED.Clipboard.hasFormat(UNRESOLVED.CF_TEXT)) {
            MessageDialog("The clipboard has no text in it.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            return;
        }
        this.plantsAsTextMemo.Clear();
        this.plantsAsTextMemo.PasteFromClipboard();
        if (this.plantsAsTextMemo.Lines.Count <= 0) {
            MessageDialog("The clipboard has no text in it.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            return;
        }
        startLine = -1;
        endLine = -1;
        for (i = 0; i <= this.plantsAsTextMemo.Lines.Count - 1; i++) {
            if (UNRESOLVED.pos(uplant.kPlantAsTextStartString, this.plantsAsTextMemo.Lines.Strings[i]) > 0) {
                startLine = i;
                break;
            }
        }
        for (i = this.plantsAsTextMemo.Lines.Count - 1; i >= 0; i--) {
            if (UNRESOLVED.pos(uplant.kPlantAsTextEndString, this.plantsAsTextMemo.Lines.Strings[i]) > 0) {
                endLine = i;
                break;
            }
        }
        if (startLine < 0) {
            this.plantsAsTextMemo.Clear();
            MessageDialog("The clipboard has text in it, but no plants." + chr(13) + chr(13) + "I can't find a starting line for a plant text description." + chr(13) + "It should have \"" + uplant.kPlantAsTextStartString + "\" in it." + chr(13) + chr(13) + "If you copied the text for a plant," + chr(13) + "make sure the first line is selected and copy it again.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            return;
        }
        if (endLine < 0) {
            this.plantsAsTextMemo.Clear();
            MessageDialog("The clipboard has text in it, but no plants." + chr(13) + chr(13) + "I can't find an ending line for a plant text description." + chr(13) + "It should have \"" + uplant.kPlantAsTextEndString + "\" in it." + chr(13) + chr(13) + "If you copied the text for a plant," + chr(13) + "make sure the whole plant is selected and copy it again.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            return;
        }
        newPlants = delphi_compatability.TList().Create();
        try {
            // since startLine and endLine are comments, we can read them
            i = startLine;
            while (i <= endLine) {
                aLine = this.plantsAsTextMemo.Lines.Strings[i];
                i += 1;
                if (trim(aLine) == "") {
                    // v1.60final ignore blank lines
                    continue;
                }
                if (UNRESOLVED.pos(";", aLine) == 1) {
                    continue;
                }
                if (UNRESOLVED.pos("[", aLine) == 1) {
                    UNRESOLVED.checkVersionNumberInPlantNameLine(aLine);
                    plant = uplant.PdPlant().create();
                    plantName = usupport.stringBeyond(aLine, "[");
                    plantName = usupport.stringUpTo(plantName, "]");
                    plant.setName(plantName + " from text");
                    udomain.domain.parameterManager.setAllReadFlagsToFalse();
                    plant.readingFromMemo = true;
                    try {
                        while ((UNRESOLVED.pos(uplant.kPlantAsTextEndString, aLine) <= 0) && (i <= endLine)) {
                            // v1.60final fixed cutting off plant at blank line (was changed in file read in v1.3)
                            // aLine <> '' do
                            aLine = this.plantsAsTextMemo.Lines.Strings[i];
                            i += 1;
                            if (UNRESOLVED.pos(";", aLine) == 1) {
                                continue;
                            }
                            if (trim(aLine) == "") {
                                continue;
                            }
                            if (UNRESOLVED.pos(uppercase(uplant.kStartNoteString), uppercase(aLine)) > 0) {
                                // added v1.6b1 to accommodate paste from text with note
                                plant.noteLines.Clear();
                                while (i <= this.plantsAsTextMemo.Lines.Count - 1) {
                                    aLine = this.plantsAsTextMemo.Lines.Strings[i];
                                    i += 1;
                                    if ((UNRESOLVED.pos(uppercase(uplant.kEndNoteString), uppercase(aLine)) > 0) && (plant.noteLines.Count < 5000)) {
                                        break;
                                    } else if (UNRESOLVED.pos(";", aLine) == 1) {
                                        continue;
                                    } else {
                                        plant.noteLines.Add(aLine);
                                    }
                                }
                            }
                            // end added v1.6b1
                            plant.readingMemoLine = i;
                            plant.readLineAndTdoFromPlantFile(aLine, fakeTextFile);
                            if (i != plant.readingMemoLine) {
                                i = plant.readingMemoLine;
                            }
                        }
                    } finally {
                        plant.readingFromMemo = false;
                        plant.readingMemoLine = -1;
                    }
                    plant.finishLoadingOrDefaulting(uplant.kCheckForUnreadParams);
                    // cfk change v1.3 make plant fit into 100x100 box with paste from text, because
                    // the scale always seems to be way off from what is being used; this way it always
                    // looks okay when it pastes
                    plant.drawPreviewIntoCache(Point(udomain.domain.options.pasteRectSize, udomain.domain.options.pasteRectSize), uplant.kDontConsiderDomainScale, uplant.kDontDrawNow);
                    newPlants.Add(plant);
                }
            }
            newCommand = updcom.PdPasteCommand().createWithListOfPlantsAndOldSelectedList(newPlants, this.selectedPlants);
            this.doCommand(newCommand);
        } finally {
            //command has another list, so we need to free this one; command will free plants if paste is undone
            newPlants.free;
        }
    }
    
    // export 
    public int getBitmapCopySavePrintOptions(short copySavePrintType) {
        result = 0;
        TBitmapOptionsForm bitmapOptionsForm = new TBitmapOptionsForm();
        
        result = mrCancel;
        bitmapOptionsForm = UNRESOLVED.TBitmapOptionsForm.create(this);
        if (bitmapOptionsForm == null) {
            throw new GeneralException.create("Problem: Could not create copy/save/print options window.");
        }
        try {
            bitmapOptionsForm.initializeWithTypeAndOptions(copySavePrintType, udomain.domain.bitmapOptions);
            result = bitmapOptionsForm.showModal;
            udomain.domain.bitmapOptions = bitmapOptionsForm.options;
        } finally {
            bitmapOptionsForm.free;
        }
        return result;
    }
    
    public void MenuEditCopyDrawingClick(TObject Sender) {
        TBitmap bitmapForExport = new TBitmap();
        
        if (this.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort()) {
            return;
        }
        if ((udomain.domain == null) || (udomain.domain.plantManager == null) || (this.plants.Count <= 0)) {
            return;
        }
        if (this.getBitmapCopySavePrintOptions(UNRESOLVED.kCopyingDrawing) == mrOK) {
            bitmapForExport = delphi_compatability.TBitmap().Create();
            try {
                this.fillBitmapForExport(bitmapForExport, udomain.domain.bitmapOptions);
                ubitmap.CopyBitmapToClipboard(bitmapForExport);
            } finally {
                bitmapForExport.free;
                if ((!udomain.domain.registered)) {
                    this.incrementUnregisteredExportCount();
                }
            }
        }
    }
    
    public void MenuFileSaveDrawingAsClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        TBitmap bitmapForExport = new TBitmap();
        String suggestedFileName = "";
        
        if (this.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort()) {
            return;
        }
        if ((udomain.domain == null) || (udomain.domain.plantManager == null) || (this.plants.Count <= 0)) {
            return;
        }
        if (this.getBitmapCopySavePrintOptions(UNRESOLVED.kSavingDrawingToBmp) == mrCancel) {
            return;
        }
        pictureFileSaveAttemptsThisSession += 1;
        suggestedFileName = "picture" + IntToStr(pictureFileSaveAttemptsThisSession) + ".bmp";
        if (!usupport.getFileSaveInfo(usupport.kFileTypeBitmap, usupport.kAskForFileName, suggestedFileName, fileInfo)) {
            return;
        }
        bitmapForExport = delphi_compatability.TBitmap().Create();
        try {
            usupport.startFileSave(fileInfo);
            UNRESOLVED.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...");
            this.fillBitmapForExport(bitmapForExport, udomain.domain.bitmapOptions);
            if (!ubitmap.RequiresPalette(bitmapForExport)) {
                bitmapForExport.ReleasePalette();
                bitmapForExport.ignorePalette = true;
            }
            bitmapForExport.SaveToFile(fileInfo.tempFile);
            fileInfo.writingWasSuccessful = true;
        } finally {
            bitmapForExport.free;
            UNRESOLVED.stopWaitMessage;
            usupport.cleanUpAfterFileSave(fileInfo);
        }
    }
    
    public void MenuFileSaveJPEGClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        TBitmap bitmapForExport = new TBitmap();
        TJPEGImage jpegForExport = new TJPEGImage();
        String suggestedFileName = "";
        
        if (this.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort()) {
            return;
        }
        if ((udomain.domain == null) || (udomain.domain.plantManager == null) || (this.plants.Count <= 0)) {
            return;
        }
        if (this.getBitmapCopySavePrintOptions(UNRESOLVED.kSavingDrawingToJpeg) == mrCancel) {
            return;
        }
        pictureFileSaveAttemptsThisSession += 1;
        suggestedFileName = "picture" + IntToStr(pictureFileSaveAttemptsThisSession) + ".jpg";
        if (!usupport.getFileSaveInfo(usupport.kFileTypeJPEG, usupport.kAskForFileName, suggestedFileName, fileInfo)) {
            return;
        }
        bitmapForExport = delphi_compatability.TBitmap().Create();
        jpegForExport = UNRESOLVED.TJPEGImage.create;
        try {
            usupport.startFileSave(fileInfo);
            UNRESOLVED.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...");
            this.fillBitmapForExport(bitmapForExport, udomain.domain.bitmapOptions);
            if (!ubitmap.RequiresPalette(bitmapForExport)) {
                bitmapForExport.ReleasePalette();
                bitmapForExport.ignorePalette = true;
            }
            jpegForExport.assign(bitmapForExport);
            // no option here
            jpegForExport.pixelFormat = UNRESOLVED.jf24Bit;
            // we ask for compression, they want quality, so we switch here
            jpegForExport.compressionQuality = UNRESOLVED.TJPEGQualityRange(100 - udomain.domain.bitmapOptions.jpegCompressionRatio);
            jpegForExport.saveToFile(fileInfo.tempFile);
            fileInfo.writingWasSuccessful = true;
        } finally {
            bitmapForExport.free;
            jpegForExport.free;
            UNRESOLVED.stopWaitMessage;
            usupport.cleanUpAfterFileSave(fileInfo);
        }
    }
    
    public void MenuFilePrintDrawingClick(TObject Sender) {
        TRect printRect_pixels = new TRect();
        TBitmap bitmapForExport = new TBitmap();
        float xResolution_pixelsPerInch = 0.0;
        float yResolution_pixelsPerInch = 0.0;
        int printOffsetX_px = 0;
        int printOffsetY_px = 0;
        
        if (this.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort()) {
            return;
        }
        if ((udomain.domain == null) || (udomain.domain.plantManager == null) || (this.plants.Count <= 0)) {
            return;
        }
        if (this.getBitmapCopySavePrintOptions(UNRESOLVED.kPrintingDrawing) == mrCancel) {
            return;
        }
        bitmapForExport = delphi_compatability.TBitmap().Create();
        try {
            this.fillBitmapForExport(bitmapForExport, udomain.domain.bitmapOptions);
            UNRESOLVED.Printer.Title = "PlantStudio Picture";
            UNRESOLVED.Printer.beginDoc;
            xResolution_pixelsPerInch = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSX);
            yResolution_pixelsPerInch = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, delphi_compatability.LOGPIXELSY);
            printOffsetX_px = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PhysicalOffsetX);
            printOffsetY_px = UNRESOLVED.GetDeviceCaps(UNRESOLVED.Printer.Handle, UNRESOLVED.PhysicalOffsetY);
            printRect_pixels.Left = intround(udomain.domain.bitmapOptions.printLeftMargin_in * xResolution_pixelsPerInch) - printOffsetX_px;
            printRect_pixels.Top = intround(udomain.domain.bitmapOptions.printTopMargin_in * yResolution_pixelsPerInch) - printOffsetY_px;
            printRect_pixels.Right = printRect_pixels.Left + intround(udomain.domain.bitmapOptions.printWidth_in * xResolution_pixelsPerInch);
            printRect_pixels.Bottom = printRect_pixels.Top + intround(udomain.domain.bitmapOptions.printHeight_in * yResolution_pixelsPerInch);
            UNRESOLVED.inflateRect(printRect_pixels, -udomain.domain.bitmapOptions.borderThickness, -udomain.domain.bitmapOptions.borderThickness);
            ubitmap.PrintBitmap(bitmapForExport, printRect_pixels);
            //FIX unresolved WITH expression: UNRESOLVED.Printer.Canvas
            // border
            UNRESOLVED.brush.style = delphi_compatability.TFPBrushStyle.bsClear;
            if (udomain.domain.bitmapOptions.printBorderInner) {
                UNRESOLVED.pen.color = udomain.domain.bitmapOptions.printBorderColorInner;
                UNRESOLVED.pen.width = udomain.domain.bitmapOptions.printBorderWidthInner;
                UNRESOLVED.rectangle(printRect_pixels.Left, printRect_pixels.Top, printRect_pixels.Right, printRect_pixels.Bottom);
            }
            if (udomain.domain.bitmapOptions.printBorderOuter) {
                UNRESOLVED.pen.color = udomain.domain.bitmapOptions.printBorderColorOuter;
                UNRESOLVED.pen.width = udomain.domain.bitmapOptions.printBorderWidthOuter;
                UNRESOLVED.rectangle(printRect_pixels.Left - udomain.domain.bitmapOptions.borderGap, printRect_pixels.Top - udomain.domain.bitmapOptions.borderGap, printRect_pixels.Right + udomain.domain.bitmapOptions.borderGap, printRect_pixels.Bottom + udomain.domain.bitmapOptions.borderGap);
            }
            UNRESOLVED.Printer.endDoc;
        } finally {
            bitmapForExport.free;
            if ((!udomain.domain.registered)) {
                this.incrementUnregisteredExportCount();
            }
        }
    }
    
    // edit menu 
    public void copySelectedPlantsToClipboard() {
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        udomain.domain.plantManager.copyPlantsInListToPrivatePlantClipboard(this.selectedPlants);
        udomain.domain.plantManager.setCopiedFromMainWindowFlagInClipboardPlants;
        this.updatePasteMenuForClipboardContents();
    }
    
    public void fillBitmapForExport(TBitmap bitmapForExport, BitmapOptionsStructure options) {
        TRect combinedBoundsRect = new TRect();
        TRect rectToDrawIn = new TRect();
        TRect unregRect = new TRect();
        float xMultiplier = 0.0;
        float yMultiplier = 0.0;
        float scaleMultiplier = 0.0;
        long plantPartsToDraw = 0;
        TList plantsToDraw = new TList();
        boolean excludeInvisiblePlants = false;
        boolean excludeNonSelectedPlants = false;
        
        if ((bitmapForExport == null) || (udomain.domain == null) || (delphi_compatability.Application.terminated)) {
            return;
        }
        plantsToDraw = null;
        // set up according to domain options
        bitmapForExport.PixelFormat = options.colorType;
        excludeInvisiblePlants = true;
        excludeNonSelectedPlants = false;
        switch (options.exportType) {
            case udomain.kIncludeSelectedPlants:
                plantsToDraw = this.selectedPlants;
                excludeInvisiblePlants = true;
                excludeNonSelectedPlants = true;
                combinedBoundsRect = udomain.domain.plantManager.combinedPlantBoundsRects(this.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants);
                break;
            case udomain.kIncludeVisiblePlants:
                plantsToDraw = this.plants;
                excludeInvisiblePlants = true;
                excludeNonSelectedPlants = false;
                combinedBoundsRect = udomain.domain.plantManager.combinedPlantBoundsRects(this.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants);
                break;
            case udomain.kIncludeAllPlants:
                plantsToDraw = this.plants;
                excludeInvisiblePlants = false;
                excludeNonSelectedPlants = false;
                combinedBoundsRect = udomain.domain.plantManager.combinedPlantBoundsRects(this.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants);
                break;
            case udomain.kIncludeDrawingAreaContents:
                plantsToDraw = this.plants;
                excludeInvisiblePlants = true;
                excludeNonSelectedPlants = false;
                combinedBoundsRect = Rect(0, 0, this.drawingBitmap.Width, this.drawingBitmap.Height);
                break;
        rectToDrawIn = Rect(0, 0, options.width_pixels, options.height_pixels);
        if ((plantsToDraw == null) || (plantsToDraw.Count <= 0)) {
            return;
        }
        bitmapForExport.Palette = UNRESOLVED.CopyPalette(this.paletteImage.Picture.Bitmap.Palette);
        xMultiplier = umath.safedivExcept(1.0 * usupport.rWidth(rectToDrawIn), 1.0 * usupport.rWidth(combinedBoundsRect), 1.0);
        yMultiplier = umath.safedivExcept(1.0 * usupport.rHeight(rectToDrawIn), 1.0 * usupport.rHeight(combinedBoundsRect), 1.0);
        scaleMultiplier = umath.min(xMultiplier, yMultiplier);
        try {
            UNRESOLVED.cursor_startWait;
            UNRESOLVED.resizeBitmap(bitmapForExport, Point(intround(usupport.rWidth(combinedBoundsRect) * scaleMultiplier), intround(usupport.rHeight(combinedBoundsRect) * scaleMultiplier)));
            udomain.domain.drawingToMakeCopyBitmap = true;
            udomain.domain.temporarilyHideSelectionRectangles = true;
            udomain.domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm() * scaleMultiplier;
            udomain.domain.plantDrawOffsetWhenDrawingCopy_mm = udomain.domain.plantDrawOffset_mm();
            if (options.exportType != udomain.kIncludeDrawingAreaContents) {
                udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.x = udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.x - umath.safedivExcept(1.0 * combinedBoundsRect.Left, udomain.domain.plantDrawScale_PixelsPerMm(), 0);
                udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.y = udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.y - umath.safedivExcept(1.0 * combinedBoundsRect.Top, udomain.domain.plantDrawScale_PixelsPerMm(), 0);
            }
            UNRESOLVED.fillBitmap(bitmapForExport, udomain.domain.options.backgroundColor);
            plantPartsToDraw = 0;
            if (udomain.domain.options.showPlantDrawingProgress) {
                plantPartsToDraw = udomain.domain.plantManager.totalPlantPartCountInInvalidRect(plantsToDraw, combinedBoundsRect, excludeInvisiblePlants, excludeNonSelectedPlants);
            }
            try {
                this.drawing = true;
                if (udomain.domain.options.showPlantDrawingProgress) {
                    this.startDrawProgress(plantPartsToDraw);
                }
                // leave out openGL for now, put in later when you get bitmap drawing working
                udomain.domain.plantManager.drawOnInvalidRect(bitmapForExport.Canvas, plantsToDraw, combinedBoundsRect, excludeInvisiblePlants, excludeNonSelectedPlants);
            } finally {
                this.drawing = false;
                if (udomain.domain.options.showPlantDrawingProgress) {
                    this.finishDrawProgress();
                }
            }
            if (!udomain.domain.registered) {
                scaleMultiplier = umath.max(1.0, scaleMultiplier);
                unregRect = Rect(1, 1, intround(this.unregisteredExportReminder.Width * scaleMultiplier) + 1, intround(this.unregisteredExportReminder.Height * scaleMultiplier) + 1);
                bitmapForExport.Canvas.StretchDraw(unregRect, this.unregisteredExportReminder.Picture.Bitmap);
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
            udomain.domain.temporarilyHideSelectionRectangles = false;
            udomain.domain.drawingToMakeCopyBitmap = false;
            udomain.domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm = 1.0;
            udomain.domain.plantDrawOffsetWhenDrawingCopy_mm = usupport.setSinglePoint(0, 0);
        }
    }
    
    public void MenuEditPasteClick(TObject Sender) {
        this.pastePlantsFromClipboard();
    }
    
    public void pastePlantsFromClipboard() {
        TList newPlants = new TList();
        PdCommand newCommand = new PdCommand();
        
        newPlants = null;
        if (udomain.domain.plantManager.privatePlantClipboard.count <= 0) {
            return;
        }
        newPlants = delphi_compatability.TList().Create();
        try {
            udomain.domain.plantManager.pastePlantsFromPrivatePlantClipboardToList(newPlants);
            newCommand = updcom.PdPasteCommand().createWithListOfPlantsAndOldSelectedList(newPlants, this.selectedPlants);
            this.doCommand(newCommand);
        } finally {
            //command has another list, so we need to free this one; command will free plants if paste is undone
            newPlants.free;
        }
    }
    
    public TPoint standardPastePosition() {
        result = new TPoint();
        result = Point(this.drawingPaintBox.Width / 2, 3 * this.drawingPaintBox.Height / 4);
        return result;
    }
    
    public void MenuEditDeleteClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdRemoveCommand().createWithListOfPlantsAndClipboardFlag(this.selectedPlants, updcom.kDontCopyToClipboard);
        this.doCommand(newCommand);
    }
    
    public void MenuEditDuplicateClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdDuplicateCommand().createWithListOfPlants(this.selectedPlants);
        this.doCommand(newCommand);
    }
    
    public void MenuEditPreferencesClick(TObject Sender) {
        TOptionsForm optionsForm = new TOptionsForm();
        int response = 0;
        PdCommand newCommand = new PdCommand();
        
        optionsForm = UNRESOLVED.TOptionsForm.create(this);
        if (optionsForm == null) {
            throw new GeneralException.create("Problem: Could not create preferences window.");
        }
        try {
            optionsForm.options = udomain.domain.options;
            response = optionsForm.showModal;
            if ((response == mrOK) && (optionsForm.optionsChanged)) {
                newCommand = updcom.PdChangeDomainOptionsCommand().createWithOptions(optionsForm.options);
                this.doCommand(newCommand);
            }
        } finally {
            optionsForm.free;
            optionsForm = null;
        }
    }
    
    // ---------------------------------------------------------------------------- *plant menu 
    public void MenuPlantNewClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        TWizardForm wizardForm = new TWizardForm();
        int response = 0;
        PdPlant newPlantFromWizard = new PdPlant();
        
        try {
            UNRESOLVED.cursor_startWait;
            // on slower computer wizard takes a long time to come up
            UNRESOLVED.startWaitMessage("Starting the plant wizard...");
            wizardForm = uwizard.TWizardForm().create(this);
        } finally {
            UNRESOLVED.stopWaitMessage;
            UNRESOLVED.cursor_stopWait;
        }
        if (wizardForm == null) {
            throw new GeneralException.create("Problem: Could not create wizard window.");
        }
        try {
            response = wizardForm.showModal;
            if (response == mrOK) {
                if (wizardForm.plant == null) {
                    throw new GeneralException.create("Problem: New wizard plant is nil.");
                }
                newPlantFromWizard = uplant.PdPlant().create();
                wizardForm.plant.copyTo(newPlantFromWizard);
                newCommand = updcom.PdNewCommand().createWithWizardPlantAndOldSelectedList(newPlantFromWizard, this.selectedPlants);
                this.doCommand(newCommand);
                // command will free newPlantFromWizard 
            }
        } finally {
            wizardForm.free;
            wizardForm = null;
        }
    }
    
    public void MenuPlantNewUsingLastWizardSettingsClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        TWizardForm wizardForm = new TWizardForm();
        PdPlant newPlantFromWizard = new PdPlant();
        
        try {
            // use wizard form to make a new plant using the current settings, but don't show the form
            // this is a sloppy way of doing this, but using the settings to set plant params is embedded in the form.
            UNRESOLVED.cursor_startWait;
            UNRESOLVED.startWaitMessage("Making new plant...");
            wizardForm = uwizard.TWizardForm().create(this);
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
        newPlantFromWizard = uplant.PdPlant().create();
        try {
            if (wizardForm == null) {
                throw new GeneralException.create("Problem: Could not create plant from last wizard settings.");
            }
            if (wizardForm.plant == null) {
                throw new GeneralException.create("Problem: Could not create plant from last wizard settings (nil plant).");
            }
            wizardForm.setPlantVariables();
            wizardForm.plant.copyTo(newPlantFromWizard);
            newPlantFromWizard.setAge(newPlantFromWizard.pGeneral.ageAtMaturity);
            newCommand = updcom.PdNewCommand().createWithWizardPlantAndOldSelectedList(newPlantFromWizard, this.selectedPlants);
            this.doCommand(newCommand);
        } finally {
            // command will free newPlantFromWizard 
            wizardForm.free;
            wizardForm = null;
            UNRESOLVED.stopWaitMessage;
        }
    }
    
    public void MenuPlantRenameClick(TObject Sender) {
        ansistring newName = new ansistring();
        boolean response = false;
        PdCommand newCommand = new PdCommand();
        PdPlant plant = new PdPlant();
        
        plant = this.focusedPlant();
        if (plant == null) {
            return;
        }
        newName = plant.getName();
        response = InputQuery("Rename plant", "Enter a new name for " + plant.getName(), newName);
        if (response) {
            newCommand = updcom.PdRenameCommand().createWithPlantAndNewName(plant, newName);
            this.doCommand(newCommand);
        }
    }
    
    public void MenuPlantRandomizeClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdRandomizeCommand().createWithListOfPlants(this.selectedPlants);
        this.doCommand(newCommand);
    }
    
    public void MenuPlantZeroRotationsClick(TObject Sender) {
        this.resetRotationsClick(this);
    }
    
    public void MenuPlantBreedClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        if (ubreedr.BreederForm.selectedRow >= udomain.domain.breedingAndTimeSeriesOptions.maxGenerations - 2) {
            // check if there is room in the breeder - this command will make two new generations 
            ubreedr.BreederForm.fullWarning();
        } else {
            newCommand = updcom.PdBreedFromParentsCommand().createWithInfo(ubreedr.BreederForm.generations, this.focusedPlant(), this.firstUnfocusedPlant(), -1, udomain.domain.breedingAndTimeSeriesOptions.percentMaxAge / 100.0, updcom.kCreateFirstGeneration);
            this.doCommand(newCommand);
        }
    }
    
    public void MenuPlantMakeTimeSeriesClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdMakeTimeSeriesCommand().createWithNewPlant(this.focusedPlant());
        this.doCommand(newCommand);
    }
    
    public boolean checkForUnregisteredExportCountOverMaxReturnTrueIfAbort() {
        result = false;
        result = false;
        if ((udomain.domain.totalUnregisteredExportsAtThisMoment() >= udomain.kMaxUnregExportsAllowed) && (udomain.domain.unregisteredExportCountThisSession >= udomain.kMaxUnregExportsPerSessionAfterMaxReached)) {
            MessageDialog("Thank you for evaluating PlantStudio!" + chr(13) + chr(13) + "You have exported PlantStudio output at least " + IntToStr(udomain.kMaxUnregExportsAllowed) + " times" + chr(13) + "since installing it for evaluation," + " and " + IntToStr(udomain.kMaxUnregExportsPerSessionAfterMaxReached) + " times this session." + chr(13) + chr(13) + "To export more output without registering," + chr(13) + "simply close and restart the program." + chr(13) + chr(13) + "To remove this restriction, purchase a registration code," + chr(13) + "then enter it into the Help-Register window" + chr(13) + "to register your copy of PlantStudio.", mtInformation, {mbOK, }, 0);
            result = true;
            this.MenuHelpRegisterClick(this);
        }
        return result;
    }
    
    public void incrementUnregisteredExportCount() {
        udomain.domain.unregisteredExportCountThisSession += 1;
        if (udomain.domain.totalUnregisteredExportsAtThisMoment() == udomain.kMaxUnregExportsAllowed) {
            udomain.domain.unregisteredExportCountBeforeThisSession = udomain.domain.unregisteredExportCountBeforeThisSession + udomain.domain.unregisteredExportCountThisSession;
            udomain.domain.unregisteredExportCountThisSession = 0;
        }
        this.updateForChangedExportCount();
    }
    
    //v2.1
    // v2.1 separated this out and added call in animation saving
    // it is the same otherwise except for the padding
    public boolean enoughRoomToSaveFile(String tempFileName, String fileDescriptor, float fileSizeNeeded_MB) {
        result = false;
        String driveLetter = "";
        short driveNumber = 0;
        float fileMegaBytesAvailable = 0.0;
        
        result = true;
        driveLetter = uppercase(UNRESOLVED.copy(UNRESOLVED.ExtractFileDrive(tempFileName), 1, 1));
        driveNumber = ord(driveLetter[1]) - ord("A") + 1;
        fileMegaBytesAvailable = 1.0 * UNRESOLVED.diskFree(driveNumber) / (1024 * 1024);
        if (fileMegaBytesAvailable >= 0) {
            if (fileMegaBytesAvailable < fileSizeNeeded_MB * 1.1) {
                // if there are too many bytes available, the integer wraps around and goes negative, so ignore this case
                // pad size needed in case estimate is slightly off  // v2.1
                ShowMessage("Not enough space to save " + fileDescriptor + " file(s) (" + usupport.digitValueString(fileSizeNeeded_MB) + " MB needed, " + usupport.digitValueString(fileMegaBytesAvailable) + " MB available)." + chr(13) + "Choose another option or make more space available.");
                result = false;
            }
        }
        return result;
    }
    
    public void ExportToGeneric3DType(short outputType) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        TGeneric3DOptionsForm optionsForm = new TGeneric3DOptionsForm();
        FileExport3DOptionsStructure tempOptions = new FileExport3DOptionsStructure();
        short response = 0;
        short fileType = 0;
        String suggestedFileName = "";
        String fileDescriptor = "";
        boolean optionsChanged = false;
        boolean excludeInvisiblePlants = false;
        boolean excludeNonSelectedPlants = false;
        PdCommand newCommand = new PdCommand();
        
        if (this.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort()) {
            return;
        }
        response = mrCancel;
        optionsChanged = false;
        optionsForm = UNRESOLVED.TGeneric3DOptionsForm.create(this);
        if (optionsForm == null) {
            throw new GeneralException.create("Problem: Could not create 3D export options window.");
        }
        try {
            optionsForm.outputType = outputType;
            optionsForm.rearrangeItemsForOutputType;
            optionsForm.options = udomain.domain.exportOptionsFor3D[outputType];
            response = optionsForm.showModal;
            tempOptions = optionsForm.options;
            optionsChanged = optionsForm.optionsChanged;
        } finally {
            optionsForm.free;
            optionsForm = null;
        }
        if (response != mrOK) {
            return;
        }
        fileType = u3dexport.fileTypeFor3DExportType(outputType);
        fileDescriptor = usupport.nameStringForFileType(fileType);
        exportTo3DFileSaveAttemptsThisSession[outputType] += 1;
        suggestedFileName = "plants" + IntToStr(exportTo3DFileSaveAttemptsThisSession[outputType]) + "." + usupport.extensionForFileType(fileType);
        if (!usupport.getFileSaveInfo(fileType, usupport.kAskForFileName, suggestedFileName, fileInfo)) {
            if (optionsChanged) {
                if (MessageDialog(fileDescriptor + " export stopped." + chr(13) + chr(13) + "Do you want to save the changes you made" + chr(13) + "to the " + fileDescriptor + " export options?", mtConfirmation, {mbYes, mbNo, }, 0) == delphi_compatability.IDYES) {
                    newCommand = updcom.PdChangeDomain3DOptionsCommand().createWithOptionsAndType(tempOptions, outputType);
                    this.doCommand(newCommand);
                }
            }
            return;
        }
        if (!this.enoughRoomToSaveFile(fileInfo.tempFile, fileDescriptor, tempOptions.fileSize)) {
            return;
        }
        if (optionsChanged) {
            newCommand = updcom.PdChangeDomain3DOptionsCommand().createWithOptionsAndType(tempOptions, outputType);
            this.doCommand(newCommand);
        }
        try {
            usupport.startFileSave(fileInfo);
            if (outputType == u3dexport.kPOV) {
                fileInfo.newFile = usupport.replacePunctuationWithUnderscores(usupport.stringUpTo(ExtractFileName(fileInfo.newFile), ".")) + ".inc";
            }
            UNRESOLVED.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...");
            excludeInvisiblePlants = false;
            excludeNonSelectedPlants = false;
            switch (tempOptions.exportType) {
                case udomain.kIncludeSelectedPlants:
                    excludeInvisiblePlants = true;
                    excludeNonSelectedPlants = true;
                    break;
                case udomain.kIncludeVisiblePlants:
                    excludeInvisiblePlants = true;
                    break;
            udomain.domain.plantManager.write3DOutputFileToFileName(this.selectedPlants, excludeInvisiblePlants, excludeNonSelectedPlants, fileInfo.tempFile, outputType);
            fileInfo.writingWasSuccessful = true;
        } finally {
            UNRESOLVED.stopWaitMessage;
            usupport.cleanUpAfterFileSave(fileInfo);
        }
    }
    
    public void MenuPlantExportToDXFClick(TObject Sender) {
        this.ExportToGeneric3DType(u3dexport.kDXF);
    }
    
    public void MenuPlantExportTo3DSClick(TObject Sender) {
        this.ExportToGeneric3DType(u3dexport.k3DS);
    }
    
    public void MenuPlantExportToOBJClick(TObject Sender) {
        this.ExportToGeneric3DType(u3dexport.kOBJ);
    }
    
    public void MenuPlantExportToPOVClick(TObject Sender) {
        this.ExportToGeneric3DType(u3dexport.kPOV);
    }
    
    public void MenuPlantExportToVRMLClick(TObject Sender) {
        this.ExportToGeneric3DType(u3dexport.kVRML);
    }
    
    public void MenuPlantExportToLWOClick(TObject Sender) {
        this.ExportToGeneric3DType(u3dexport.kLWO);
    }
    
    // -------------------------------------------------------------------------- *layout menu 
    public void MenuLayoutSelectAllClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = updcom.PdSelectOrDeselectAllCommand().createWithListOfPlants(this.selectedPlants);
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutDeselectClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = updcom.PdSelectOrDeselectAllCommand().createWithListOfPlants(this.selectedPlants);
        ((updcom.PdSelectOrDeselectAllCommand)newCommand).deselect = true;
        this.doCommand(newCommand);
    }
    
    public void MenuFileMakePainterNozzleClick(TObject Sender) {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        TBitmap bitmapForExport = new TBitmap();
        String suggestedFileName = "";
        
        if (this.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort()) {
            return;
        }
        if ((udomain.domain == null) || (udomain.domain.plantManager == null) || (this.plants.Count <= 0)) {
            return;
        }
        if (this.getNozzleOptions() == mrCancel) {
            return;
        }
        if (udomain.domain.nozzleOptions.cellCount <= 0) {
            return;
        }
        nozzleFileSaveAttemptsThisSession += 1;
        suggestedFileName = "nozzle" + IntToStr(nozzleFileSaveAttemptsThisSession) + " " + IntToStr(udomain.domain.nozzleOptions.cellSize.X) + "x" + IntToStr(udomain.domain.nozzleOptions.cellSize.Y) + "x" + IntToStr(udomain.domain.nozzleOptions.cellCount) + ".bmp";
        if (!usupport.getFileSaveInfo(usupport.kFileTypeBitmap, usupport.kAskForFileName, suggestedFileName, fileInfo)) {
            return;
        }
        bitmapForExport = delphi_compatability.TBitmap().Create();
        try {
            usupport.startFileSave(fileInfo);
            UNRESOLVED.startWaitMessage("Saving " + ExtractFileName(fileInfo.newFile) + "...");
            this.fillBitmapForPainterNozzle(bitmapForExport);
            bitmapForExport.SaveToFile(fileInfo.tempFile);
            fileInfo.writingWasSuccessful = true;
        } finally {
            bitmapForExport.free;
            UNRESOLVED.stopWaitMessage;
            usupport.cleanUpAfterFileSave(fileInfo);
        }
    }
    
    public int getNozzleOptions() {
        result = 0;
        TNozzleOptionsForm nozzleOptionsForm = new TNozzleOptionsForm();
        
        result = mrCancel;
        nozzleOptionsForm = UNRESOLVED.TNozzleOptionsForm.create(this);
        if (nozzleOptionsForm == null) {
            throw new GeneralException.create("Problem: Could not create nozzle options window.");
        }
        try {
            nozzleOptionsForm.initializeWithOptions(udomain.domain.nozzleOptions);
            result = nozzleOptionsForm.showModal;
            udomain.domain.nozzleOptions = nozzleOptionsForm.options;
        } finally {
            nozzleOptionsForm.free;
        }
        return result;
    }
    
    public void fillBitmapForPainterNozzle(TBitmap bitmapForExport) {
        TList plantsToDraw = new TList();
        TColorRef oldBackgroundColor = new TColorRef();
        short i = 0;
        PdPlant plant = new PdPlant();
        float oldPlantScale = 0.0;
        float scaleMultiplier = 0.0;
        TPoint scaledPlantSize = new TPoint();
        
        if ((bitmapForExport == null) || (udomain.domain == null) || (delphi_compatability.Application.terminated)) {
            return;
        }
        plantsToDraw = null;
        oldBackgroundColor = udomain.domain.options.backgroundColor;
        bitmapForExport.PixelFormat = udomain.domain.nozzleOptions.colorType;
        if (udomain.domain.nozzleOptions.exportType == udomain.kIncludeSelectedPlants) {
            plantsToDraw = this.selectedPlants;
        } else {
            plantsToDraw = this.plants;
        }
        if ((plantsToDraw == null) || (plantsToDraw.Count <= 0)) {
            return;
        }
        try {
            UNRESOLVED.cursor_startWait;
            UNRESOLVED.resizeBitmap(bitmapForExport, Point(intround(udomain.domain.nozzleOptions.cellSize.X * plantsToDraw.Count), udomain.domain.nozzleOptions.cellSize.Y));
            scaleMultiplier = umath.safedivExcept(1.0 * udomain.domain.nozzleOptions.resolution_pixelsPerInch, 1.0 * delphi_compatability.Screen.PixelsPerInch, 1.0);
            // v1.4 changed 0.8 to 0.9 because fitting algorithm works better now
            // extra margin to make sure plants fit
            scaleMultiplier = scaleMultiplier * 0.9;
            udomain.domain.options.backgroundColor = udomain.domain.nozzleOptions.backgroundColor;
            UNRESOLVED.fillBitmap(bitmapForExport, udomain.domain.nozzleOptions.backgroundColor);
            for (i = 0; i <= plantsToDraw.Count - 1; i++) {
                plant = uplant.PdPlant(plantsToDraw.Items[i]);
                scaledPlantSize = Point(intround(usupport.rWidth(plant.boundsRect_pixels()) * scaleMultiplier), intround(usupport.rHeight(plant.boundsRect_pixels()) * scaleMultiplier));
                oldPlantScale = plant.drawingScale_PixelsPerMm;
                try {
                    // v1.4
                    plant.fixedPreviewScale = false;
                    // v1.4
                    plant.fixedDrawPosition = false;
                    plant.drawPreviewIntoCache(scaledPlantSize, uplant.kDontConsiderDomainScale, kDrawNow);
                    bitmapForExport.Canvas.Draw(i * udomain.domain.nozzleOptions.cellSize.X, 0, plant.previewCache);
                    plant.shrinkPreviewCache();
                } finally {
                    plant.drawingScale_PixelsPerMm = oldPlantScale;
                    plant.recalculateBounds(kDrawNow);
                }
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
            udomain.domain.options.backgroundColor = oldBackgroundColor;
        }
    }
    
    public void MenuFileMakePainterAnimationClick(TObject Sender) {
        TSaveDialog saveDialog = new TSaveDialog();
        float sizeNeeded_MB = 0.0;
        
        if (this.checkForUnregisteredExportCountOverMaxReturnTrueIfAbort()) {
            return;
        }
        if ((udomain.domain == null) || (udomain.domain.plantManager == null) || (this.plants.Count <= 0)) {
            return;
        }
        if (this.focusedPlant() == null) {
            return;
        }
        if (this.getAnimationOptions() == mrCancel) {
            return;
        }
        if (udomain.domain.animationOptions.frameCount <= 0) {
            return;
        }
        saveDialog = delphi_compatability.TSaveDialog().Create(delphi_compatability.Application);
        try {
            saveDialog.Title = "Choose a file name (numbers will be added)";
            saveDialog.FileName = this.focusedPlant().getName() + ".bmp";
            saveDialog.Filter = "Bitmap files (*.bmp)|*.bmp";
            saveDialog.DefaultExt = "bmp";
            saveDialog.Options = saveDialog.Options + {delphi_compatability.TOpenOption.ofPathMustExist, delphi_compatability.TOpenOption.ofOverwritePrompt, delphi_compatability.TOpenOption.ofHideReadOnly, delphi_compatability.TOpenOption.ofNoReadOnlyReturn, };
            if (saveDialog.Execute()) {
                sizeNeeded_MB = 1.0 * udomain.domain.animationOptions.fileSize / (1024 * 1024);
                if (!this.enoughRoomToSaveFile(saveDialog.FileName, "animation", sizeNeeded_MB)) {
                    return;
                }
                UNRESOLVED.cursor_startWait;
                UNRESOLVED.startWaitMessage("Starting...");
                try {
                    this.writeAnimationFilesWithFileSpec(usupport.stringUpTo(saveDialog.FileName, ".") + " ");
                } finally {
                    UNRESOLVED.cursor_stopWait;
                    UNRESOLVED.stopWaitMessage;
                }
            }
        } finally {
            saveDialog.free;
        }
    }
    
    public void writeAnimationFilesWithFileSpec(String startFileName) {
        PdPlant plant = new PdPlant();
        float oldXRotation = 0.0;
        float scaleMultiplier = 0.0;
        float minScale = 0.0;
        float oldScale = 0.0;
        short oldAge = 0;
        short i = 0;
        String saveFileName = "";
        TRect unregRect = new TRect();
        TPoint bestPosition = new TPoint();
        long widestWidth = 0;
        long tallestHeight = 0;
        
        if (this.focusedPlant() == null) {
            return;
        }
        plant = this.focusedPlant();
        oldXRotation = plant.xRotation;
        oldAge = plant.age;
        oldScale = plant.drawingScale_PixelsPerMm;
        try {
            plant.previewCache.PixelFormat = udomain.domain.animationOptions.colorType;
            // draw plant for all frames, get min drawing scale
            plant.fixedPreviewScale = false;
            plant.fixedDrawPosition = false;
            minScale = 0;
            for (i = 0; i <= udomain.domain.animationOptions.frameCount - 1; i++) {
                setPlantCharacteristicsForAnimationFrame(plant, i);
                plant.drawPreviewIntoCache(udomain.domain.animationOptions.scaledSize, uplant.kDontConsiderDomainScale, uplant.kDontDrawNow);
                if ((i == 1) || (plant.drawingScale_PixelsPerMm < minScale)) {
                    minScale = plant.drawingScale_PixelsPerMm;
                }
            }
            // draw plant for all frames, get common draw position
            plant.drawingScale_PixelsPerMm = minScale;
            plant.fixedPreviewScale = true;
            widestWidth = 0;
            tallestHeight = 0;
            for (i = 0; i <= udomain.domain.animationOptions.frameCount - 1; i++) {
                setPlantCharacteristicsForAnimationFrame(plant, i);
                plant.drawPreviewIntoCache(udomain.domain.animationOptions.scaledSize, uplant.kDontConsiderDomainScale, uplant.kDontDrawNow);
                if ((i == 0) || (usupport.rWidth(plant.boundsRect_pixels()) > widestWidth)) {
                    widestWidth = usupport.rWidth(plant.boundsRect_pixels());
                    bestPosition.X = plant.drawPositionIfFixed.X;
                }
                if ((i == 0) || (usupport.rHeight(plant.boundsRect_pixels()) > tallestHeight)) {
                    tallestHeight = usupport.rHeight(plant.boundsRect_pixels());
                    bestPosition.Y = plant.drawPositionIfFixed.Y;
                }
            }
            // now really draw
            plant.drawPositionIfFixed = bestPosition;
            plant.fixedDrawPosition = true;
            for (i = 0; i <= udomain.domain.animationOptions.frameCount - 1; i++) {
                saveFileName = startFileName;
                if (i + 1 < 100) {
                    saveFileName = saveFileName + "0";
                }
                if (i + 1 < 10) {
                    saveFileName = saveFileName + "0";
                }
                saveFileName = saveFileName + IntToStr(i + 1) + ".bmp";
                UNRESOLVED.startWaitMessage("Saving " + ExtractFileName(saveFileName) + "...");
                setPlantCharacteristicsForAnimationFrame(plant, i);
                plant.drawPreviewIntoCache(udomain.domain.animationOptions.scaledSize, uplant.kDontConsiderDomainScale, kDrawNow);
                if (!udomain.domain.registered) {
                    scaleMultiplier = umath.safedivExcept(1.0 * udomain.domain.animationOptions.resolution_pixelsPerInch, 1.0 * delphi_compatability.Screen.PixelsPerInch, 1.0);
                    scaleMultiplier = umath.max(1.0, scaleMultiplier);
                    unregRect = Rect(1, 1, intround(this.unregisteredExportReminder.Width * scaleMultiplier) + 1, intround(this.unregisteredExportReminder.Height * scaleMultiplier) + 1);
                    plant.previewCache.Canvas.StretchDraw(unregRect, this.unregisteredExportReminder.Picture.Bitmap);
                }
                plant.previewCache.SaveToFile(saveFileName);
            }
            // clean up for next time
            plant.fixedPreviewScale = false;
            plant.fixedDrawPosition = false;
        } finally {
            plant.shrinkPreviewCache();
            plant.fixedPreviewScale = false;
            plant.xRotation = oldXRotation;
            plant.drawingScale_PixelsPerMm = oldScale;
            plant.setAge(oldAge);
            plant.recalculateBounds(kDrawNow);
        }
    }
    
    public int getAnimationOptions() {
        result = 0;
        TAnimationFilesOptionsForm animationOptionsForm = new TAnimationFilesOptionsForm();
        
        result = mrCancel;
        if (this.focusedPlant() == null) {
            return result;
        }
        animationOptionsForm = UNRESOLVED.TAnimationFilesOptionsForm.create(this);
        if (animationOptionsForm == null) {
            throw new GeneralException.create("Problem: Could not create animation options window.");
        }
        try {
            animationOptionsForm.initializeWithOptionsAndPlant(udomain.domain.animationOptions, this.focusedPlant());
            result = animationOptionsForm.showModal;
            udomain.domain.animationOptions = animationOptionsForm.options;
        } finally {
            animationOptionsForm.free;
        }
        return result;
    }
    
    public void MenuLayoutShowClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        boolean atLeastOnePlantIsHidden = false;
        short i = 0;
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        // make sure at least one plant is hidden 
        atLeastOnePlantIsHidden = false;
        for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
            if (uplant.PdPlant(this.selectedPlants.Items[i]).hidden) {
                atLeastOnePlantIsHidden = true;
                break;
            }
        }
        if (!atLeastOnePlantIsHidden) {
            return;
        }
        newCommand = updcom.PdHideOrShowCommand().createWithListOfPlantsAndHideOrShow(this.selectedPlants, updcom.kShow);
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutHideClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        boolean atLeastOnePlantIsShowing = false;
        short i = 0;
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        // make sure at least one plant is showing 
        atLeastOnePlantIsShowing = false;
        for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
            if (!uplant.PdPlant(this.selectedPlants.Items[i]).hidden) {
                atLeastOnePlantIsShowing = true;
                break;
            }
        }
        if (!atLeastOnePlantIsShowing) {
            return;
        }
        newCommand = updcom.PdHideOrShowCommand().createWithListOfPlantsAndHideOrShow(this.selectedPlants, updcom.kHide);
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutHideOthersClick(TObject Sender) {
        TListCollection booleansList = new TListCollection();
        PdCommand newCommand = new PdCommand();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        booleansList = ucollect.TListCollection().Create();
        for (i = 0; i <= this.plants.Count - 1; i++) {
            plant = uplant.PdPlant(this.plants.Items[i]);
            booleansList.Add(updcom.PdBooleanValue().createWithBoolean(!this.isSelected(plant)));
        }
        try {
            newCommand = updcom.PdHideOrShowCommand().createWithListOfPlantsAndListOfHides(this.plants, booleansList);
            this.doCommand(newCommand);
        } finally {
            booleansList.free;
        }
    }
    
    public void MenuLayoutMakeBouquetClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 1) {
            return;
        }
        newCommand = updcom.PdDragCommand().createWithListOfPlantsAndNewPoint(this.selectedPlants, this.focusedPlant().basePoint_pixels());
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutScaleToFitClick(TObject Sender) {
        this.centerDrawingClick(this);
    }
    
    // drawing 
    public void changeViewingOptionTo(short aNewOption) {
        PdCommand newCommand = new PdCommand();
        
        if ((aNewOption == udomain.kViewPlantsInMainWindowOneAtATime) && (this.selectedPlants.Count <= 0)) {
            if (this.plants.Count < 0) {
                return;
            }
            this.selectedPlants.Add(this.plants.Items[0]);
            this.updateForChangeToPlantSelections();
        }
        newCommand = updcom.PdChangeMainWindowViewingOptionCommand().createWithListOfPlantsAndSelectedPlantsAndNewOption(this.plants, this.selectedPlants, aNewOption);
        this.doCommand(newCommand);
        this.MenuLayoutMakeBouquet.enabled = (this.selectedPlants.Count > 1) && (!udomain.domain.viewPlantsInMainWindowOnePlantAtATime());
    }
    
    public void MenuLayoutViewOnePlantAtATimeClick(TObject Sender) {
        if (udomain.domain.options.mainWindowViewMode != udomain.kViewPlantsInMainWindowOneAtATime) {
            this.changeViewingOptionTo(udomain.kViewPlantsInMainWindowOneAtATime);
        }
    }
    
    public void viewOneOnlyClick(TObject Sender) {
        this.MenuLayoutViewOnePlantAtATimeClick(this);
    }
    
    public void MenuLayoutViewFreeFloatingClick(TObject Sender) {
        if (udomain.domain.options.mainWindowViewMode != udomain.kViewPlantsInMainWindowFreeFloating) {
            this.changeViewingOptionTo(udomain.kViewPlantsInMainWindowFreeFloating);
        }
    }
    
    public void viewFreeFloatingClick(TObject Sender) {
        this.MenuLayoutViewFreeFloatingClick(this);
    }
    
    public void MenuLayoutBringForwardClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        if (this.plants.IndexOf(this.firstSelectedPlantInList()) <= 0) {
            // don't do if you can't go forward any more 
            return;
        }
        newCommand = updcom.PdSendBackwardOrForwardCommand().createWithBackwardOrForward(updcom.kBringForward);
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutSendBackClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        if (this.plants.IndexOf(this.lastSelectedPlantInList()) >= this.plants.Count - 1) {
            // don't do if you can't go backward any more 
            return;
        }
        newCommand = updcom.PdSendBackwardOrForwardCommand().createWithBackwardOrForward(updcom.kSendBackward);
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutHorizontalOrientationClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (udomain.domain.options.mainWindowOrientation != udomain.kMainWindowOrientationHorizontal) {
            newCommand = updcom.PdChangeMainWindowOrientationCommand().createWithNewOrientation(udomain.kMainWindowOrientationHorizontal);
            this.doCommand(newCommand);
        }
    }
    
    public void MenuLayoutVerticalOrientationClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (udomain.domain.options.mainWindowOrientation != udomain.kMainWindowOrientationVertical) {
            newCommand = updcom.PdChangeMainWindowOrientationCommand().createWithNewOrientation(udomain.kMainWindowOrientationVertical);
            this.doCommand(newCommand);
        }
    }
    
    public void drawingAreaOnTopClick(TObject Sender) {
        this.MenuLayoutHorizontalOrientationClick(this);
    }
    
    public void drawingAreaOnSideClick(TObject Sender) {
        this.MenuLayoutVerticalOrientationClick(this);
    }
    
    // --------------------------------------------------------------------------- *options menu 
    public void MenuOptionsFastDrawClick(TObject Sender) {
        short oldSpeed = 0;
        
        oldSpeed = udomain.domain.options.drawSpeed;
        udomain.domain.options.drawSpeed = udomain.kDrawFast;
        this.MenuOptionsFastDraw.checked = true;
        ubreedr.BreederForm.BreederMenuOptionsFastDraw.checked = true;
        UNRESOLVED.TimeSeriesForm.TimeSeriesMenuOptionsFastDraw.checked = true;
        if (oldSpeed != udomain.domain.options.drawSpeed) {
            this.updateForChangeToDrawOptions();
        }
    }
    
    public void MenuOptionsMediumDrawClick(TObject Sender) {
        short oldSpeed = 0;
        
        oldSpeed = udomain.domain.options.drawSpeed;
        udomain.domain.options.drawSpeed = udomain.kDrawMedium;
        this.MenuOptionsMediumDraw.checked = true;
        ubreedr.BreederForm.BreederMenuOptionsMediumDraw.checked = true;
        UNRESOLVED.TimeSeriesForm.TimeSeriesMenuOptionsMediumDraw.checked = true;
        if (oldSpeed != udomain.domain.options.drawSpeed) {
            this.updateForChangeToDrawOptions();
        }
    }
    
    public void MenuOptionsBestDrawClick(TObject Sender) {
        short oldSpeed = 0;
        
        oldSpeed = udomain.domain.options.drawSpeed;
        udomain.domain.options.drawSpeed = udomain.kDrawBest;
        this.MenuOptionsBestDraw.checked = true;
        ubreedr.BreederForm.BreederMenuOptionsBestDraw.checked = true;
        UNRESOLVED.TimeSeriesForm.TimeSeriesMenuOptionsBestDraw.checked = true;
        if (oldSpeed != udomain.domain.options.drawSpeed) {
            this.updateForChangeToDrawOptions();
        }
    }
    
    public void MenuOptionsCustomDrawClick(TObject Sender) {
        TCustomDrawOptionsForm customDrawForm = new TCustomDrawOptionsForm();
        PdCommand newCommand = new PdCommand();
        int response = 0;
        short lastDrawSpeed = 0;
        
        lastDrawSpeed = udomain.domain.options.drawSpeed;
        udomain.domain.options.drawSpeed = udomain.kDrawCustom;
        this.MenuOptionsCustomDraw.checked = true;
        ubreedr.BreederForm.BreederMenuOptionsCustomDraw.checked = true;
        UNRESOLVED.TimeSeriesForm.TimeSeriesMenuOptionsCustomDraw.checked = true;
        customDrawForm = UNRESOLVED.TCustomDrawOptionsForm.create(this);
        if (customDrawForm == null) {
            throw new GeneralException.create("Problem: Could not create 3D object mover window.");
        }
        try {
            customDrawForm.options = udomain.domain.options;
            response = customDrawForm.showModal;
            newCommand = null;
            if ((response == mrOK) && (customDrawForm.optionsChanged)) {
                newCommand = updcom.PdChangeDomainOptionsCommand().createWithOptions(customDrawForm.options);
                this.doCommand(newCommand);
            } else {
                if (lastDrawSpeed != udomain.kDrawCustom) {
                    // escape just escapes changing options in dialog, not setting to custom, should still redraw
                    // v1.4 change UNLESS it was custom before.
                    this.updateForChangeToDrawOptions();
                }
            }
        } finally {
            customDrawForm.free;
            customDrawForm = null;
        }
    }
    
    public void MenuOptionsUsePlantBitmapsClick(TObject Sender) {
        if (udomain.domain.options.cachePlantBitmaps) {
            this.stopUsingPlantBitmaps();
        } else {
            this.startUsingPlantBitmaps();
        }
        this.updateForChangeToPlantBitmaps();
        this.updateForPossibleChangeToDrawing();
    }
    
    public void plantBitmapsIndicatorImageClick(TObject Sender) {
        if ((!udomain.domain.options.cachePlantBitmaps) && (this.MenuOptionsUsePlantBitmaps.enabled)) {
            this.MenuOptionsUsePlantBitmapsClick(this);
        }
    }
    
    public void MenuOptionsShowSelectionRectanglesClick(TObject Sender) {
        this.MenuOptionsShowSelectionRectangles.checked = !this.MenuOptionsShowSelectionRectangles.checked;
        udomain.domain.options.showSelectionRectangle = this.MenuOptionsShowSelectionRectangles.checked;
        this.copyDrawingBitmapToPaintBox();
    }
    
    public void MenuOptionsShowBoundsRectanglesClick(TObject Sender) {
        this.MenuOptionsShowBoundsRectangles.checked = !this.MenuOptionsShowBoundsRectangles.checked;
        udomain.domain.options.showBoundsRectangle = this.MenuOptionsShowBoundsRectangles.checked;
        this.copyDrawingBitmapToPaintBox();
    }
    
    public void MenuOptionsGhostHiddenPartsClick(TObject Sender) {
        this.MenuOptionsGhostHiddenParts.checked = !this.MenuOptionsGhostHiddenParts.checked;
        udomain.domain.options.showGhostingForHiddenParts = this.MenuOptionsGhostHiddenParts.checked;
        this.internalChange = true;
        this.posingGhost.Down = udomain.domain.options.showGhostingForHiddenParts;
        this.internalChange = false;
        // cannot just redraw plants because bounds rects may have changed
        this.redrawEverything();
    }
    
    public void MenuOptionsHighlightPosedPartsClick(TObject Sender) {
        this.MenuOptionsHighlightPosedParts.checked = !this.MenuOptionsHighlightPosedParts.checked;
        udomain.domain.options.showHighlightingForNonHiddenPosedParts = this.MenuOptionsHighlightPosedParts.checked;
        this.internalChange = true;
        this.posingHighlight.Down = udomain.domain.options.showHighlightingForNonHiddenPosedParts;
        this.internalChange = false;
        this.redrawAllPlantsInViewWithAmendments();
    }
    
    public void MenuOptionsHidePosingClick(TObject Sender) {
        this.MenuOptionsHidePosing.checked = !this.MenuOptionsHidePosing.checked;
        udomain.domain.options.showPosingAtAll = !this.MenuOptionsHidePosing.checked;
        this.internalChange = true;
        this.posingNotShown.Down = !udomain.domain.options.showPosingAtAll;
        this.internalChange = false;
        // cannot just redraw plants because bounds rects may have changed
        this.redrawEverything();
    }
    
    public void posingHighlightClick(TObject Sender) {
        if (this.internalChange) {
            return;
        }
        udomain.domain.options.showHighlightingForNonHiddenPosedParts = !udomain.domain.options.showHighlightingForNonHiddenPosedParts;
        this.MenuOptionsHighlightPosedParts.checked = udomain.domain.options.showHighlightingForNonHiddenPosedParts;
        this.posingHighlight.Down = udomain.domain.options.showHighlightingForNonHiddenPosedParts;
        this.redrawAllPlantsInViewWithAmendments();
    }
    
    public void posingGhostClick(TObject Sender) {
        if (this.internalChange) {
            return;
        }
        udomain.domain.options.showGhostingForHiddenParts = !udomain.domain.options.showGhostingForHiddenParts;
        this.MenuOptionsGhostHiddenParts.checked = udomain.domain.options.showGhostingForHiddenParts;
        this.posingGhost.Down = udomain.domain.options.showGhostingForHiddenParts;
        // cannot just redraw plants because bounds rects may have changed
        this.redrawEverything();
    }
    
    public void posingNotShownClick(TObject Sender) {
        if (this.internalChange) {
            return;
        }
        udomain.domain.options.showPosingAtAll = !udomain.domain.options.showPosingAtAll;
        this.MenuOptionsHidePosing.checked = !udomain.domain.options.showPosingAtAll;
        this.posingNotShown.Down = !udomain.domain.options.showPosingAtAll;
        // cannot just redraw plants because bounds rects may have changed
        this.redrawEverything();
    }
    
    public void MenuOptionsShowLongButtonHintsClick(TObject Sender) {
        this.MenuOptionsShowLongButtonHints.checked = !this.MenuOptionsShowLongButtonHints.checked;
        udomain.domain.options.showLongHintsForButtons = this.MenuOptionsShowLongButtonHints.checked;
        this.updateHintPauseForOptions();
        // shows different hint
        this.updateForChangeToPlantBitmaps();
    }
    
    public void MenuOptionsShowParameterHintsClick(TObject Sender) {
        this.MenuOptionsShowParameterHints.checked = !this.MenuOptionsShowParameterHints.checked;
        udomain.domain.options.showHintsForParameters = this.MenuOptionsShowParameterHints.checked;
        this.updateHintPauseForOptions();
    }
    
    // --------------------------------------------------------------------------- *window menu 
    public void MenuWindowBreederClick(TObject Sender) {
        ubreedr.BreederForm.show;
        ubreedr.BreederForm.bringToFront;
        if (ubreedr.BreederForm.windowState == delphi_compatability.TWindowState.wsMinimized) {
            ubreedr.BreederForm.windowState = delphi_compatability.TWindowState.wsNormal;
        }
    }
    
    public void MenuWindowTimeSeriesClick(TObject Sender) {
        UNRESOLVED.TimeSeriesForm.show;
        UNRESOLVED.TimeSeriesForm.bringToFront;
        if (UNRESOLVED.TimeSeriesForm.windowState == delphi_compatability.TWindowState.wsMinimized) {
            UNRESOLVED.TimeSeriesForm.windowState = delphi_compatability.TWindowState.wsNormal;
        }
    }
    
    public void MenuWindowNumericalExceptionsClick(TObject Sender) {
        UNRESOLVED.DebugForm.show;
        UNRESOLVED.DebugForm.bringToFront;
        if (UNRESOLVED.DebugForm.windowState == delphi_compatability.TWindowState.wsMinimized) {
            UNRESOLVED.DebugForm.windowState = delphi_compatability.TWindowState.wsNormal;
        }
    }
    
    // ---------------------------------------------------------------------------- *help menu 
    public void MenuHelpTopicsClick(TObject Sender) {
        delphi_compatability.Application.HelpCommand(UNRESOLVED.HELP_FINDER, 0);
    }
    
    public void MenuHelpAboutClick(TObject Sender) {
        if (udomain.domain.registered) {
            if (UNRESOLVED.splashForm == null) {
                return;
            }
            //domain.registrationName);
            UNRESOLVED.splashForm.showLoadingString("Registered to:");
            //domain.registrationCode);
            UNRESOLVED.splashForm.showCodeString(udomain.domain.registrationName);
            UNRESOLVED.splashForm.close.visible = true;
            UNRESOLVED.splashForm.supportButton.visible = true;
            UNRESOLVED.splashForm.showModal;
        } else {
            if (UNRESOLVED.aboutForm == null) {
                return;
            }
            UNRESOLVED.aboutForm.initializeWithWhetherClosingProgram(false);
            UNRESOLVED.aboutForm.showModal;
            this.updateForRegistrationChange();
        }
    }
    
    public void MenuHelpRegisterClick(TObject Sender) {
        UNRESOLVED.RegistrationForm.showModal;
        this.updateForRegistrationChange();
    }
    
    public void updateForRegistrationChange() {
        this.MenuHelpRegister.visible = !udomain.domain.registered;
        this.AfterRegisterMenuSeparator.visible = !udomain.domain.registered;
        this.caption = this.captionForFile();
    }
    
    public void MenuHelpSuperSpeedTourClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Super-Speed_Tour");
    }
    
    public void MenuHelpTutorialClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Tutorial");
    }
    
    // ---------------------------------------------------------------------------- *progress showing 
    public void progressPaintBoxPaint(TObject Sender) {
        this.progressPaintBox.Canvas.Brush.Color = UNRESOLVED.clBtnFace;
        this.progressPaintBox.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear;
        this.progressPaintBox.Canvas.Rectangle(0, 0, this.progressPaintBox.Width, this.progressPaintBox.Height);
    }
    
    public void startDrawProgress(long maximum) {
        this.drawProgressMax = maximum;
        this.progressPaintBox.Invalidate();
        this.progressPaintBox.Refresh();
    }
    
    public void showDrawProgress(long amount) {
        long progress = 0;
        
        if (!this.drawing) {
            return;
        }
        if ((!this.animateTimer.enabled) && (!udomain.domain.options.showPlantDrawingProgress)) {
            return;
        }
        if (this.animateTimer.enabled) {
            return;
        }
        if (this.drawProgressMax != 0) {
            progress = intround((1.0 * this.progressPaintBox.Width * amount) / (this.drawProgressMax * 1.0));
        } else {
            progress = 0;
        }
        if (progress > 0) {
            this.progressPaintBox.Canvas.Brush.Color = kProgressBarColor;
            this.progressPaintBox.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear;
            this.progressPaintBox.Canvas.Rectangle(0, 0, progress, this.progressPaintBox.Height);
        }
    }
    
    public void finishDrawProgress() {
        this.progressPaintBox.Invalidate();
        this.progressPaintBox.Refresh();
    }
    
    // plant menu 
    // help menu 
    // updating 
    // ---------------------------------------------------------------------------- *updating 
    public void updateForNoPlantFile() {
        this.selectedPlants.Clear();
        this.plantListDrawGrid.Invalidate();
        this.clearCommandList();
        this.caption = this.captionForFile();
        this.updateRightSidePanelForFirstSelectedPlant();
        this.redrawEverything();
        this.updateMenusForChangedPlantFile();
    }
    
    public void redrawEverything() {
        this.recalculateAllPlantBoundsRects(kDrawNow);
        this.invalidateEntireDrawing();
        this.updateForPossibleChangeToDrawing();
    }
    
    public String captionForFile() {
        result = "";
        short numLeft = 0;
        
        if ((!udomain.domain.plantFileLoaded) || (udomain.domain.plantFileName == "")) {
            result = delphi_compatability.Application.Title + " - no file";
        } else {
            result = delphi_compatability.Application.Title + " - " + usupport.stringUpTo(ExtractFileName(udomain.domain.plantFileName), ".");
            if (!udomain.domain.registered) {
                if (udomain.domain.totalUnregisteredExportsAtThisMoment() < udomain.kMaxUnregExportsAllowed) {
                    // before pool runs out
                    numLeft = umath.intMax(0, udomain.kMaxUnregExportsAllowed - udomain.domain.totalUnregisteredExportsAtThisMoment());
                    if (numLeft == 1) {
                        result = result + " [unregistered - " + IntToStr(numLeft) + " export left in evaluation]";
                    } else {
                        result = result + " [unregistered - " + IntToStr(numLeft) + " exports left in evaluation]";
                    }
                    // after pool runs out, fixed number per session
                } else {
                    numLeft = umath.intMax(0, udomain.kMaxUnregExportsPerSessionAfterMaxReached - udomain.domain.unregisteredExportCountThisSession);
                    if (numLeft <= 0) {
                        result = result + " [unregistered - NO exports left this session]";
                    } else if (numLeft == 1) {
                        result = result + " [unregistered - " + IntToStr(numLeft) + " export left this session]";
                    } else {
                        result = result + " [unregistered - " + IntToStr(numLeft) + " exports left this session]";
                    }
                }
            } else if (this.plants.Count <= 0) {
                result = result + " (no plants)";
            } else if (this.plants.Count == 1) {
                result = result + " (1 plant)";
            } else {
                result = result + " (" + IntToStr(this.plants.Count) + " plants)";
            }
        }
        return result;
    }
    
    public void updateForPlantFile() {
        PdPlant plant = new PdPlant();
        int i = 0;
        
        this.internalChange = true;
        if (!udomain.domain.plantFileLoaded) {
            this.updateForNoPlantFile();
        } else {
            this.caption = this.captionForFile();
            this.updateForChangeToPlantList();
            this.updateMenusForChangedPlantFile();
            this.selectedPlants.Clear();
            this.magnificationPercent.Text = IntToStr(intround(udomain.domain.plantDrawScale_PixelsPerMm() * 100.0)) + "%";
            if (udomain.domain.plantManager.mainWindowOrientation != udomain.domain.options.mainWindowOrientation) {
                // v2.0 load and save window orientation (top or side)
                udomain.domain.options.mainWindowOrientation = udomain.domain.plantManager.mainWindowOrientation;
                this.updateForChangeToOrientation();
            }
            if (this.plants.Count > 0) {
                for (i = 0; i <= this.plants.Count - 1; i++) {
                    // v2.0 load and save plant hidden and selected flags
                    plant = uplant.PdPlant(this.plants.Items[i]);
                    if (plant.selectedWhenLastSaved) {
                        this.selectedPlants.Add(plant);
                    }
                }
                if (this.selectedPlants.Count <= 0) {
                    this.selectedPlants.Add(uplant.PdPlant(this.plants.Items[0]));
                }
                this.updateForChangeToPlantSelections();
            }
            if (udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
                // deal with possibly changed viewing mode (one/many)
                this.showOnePlantExclusively(kDontDrawYet);
            }
            this.viewOneOnly.Down = udomain.domain.viewPlantsInMainWindowOnePlantAtATime();
            if (udomain.domain.plantManager.fitInVisibleAreaForConcentrationChange) {
                this.fitVisiblePlantsInDrawingArea(kDrawNow, kScaleAndMove, kAlwaysMove);
                udomain.domain.plantManager.fitInVisibleAreaForConcentrationChange = false;
            } else {
                this.fitVisiblePlantsInDrawingArea(kDrawNow, kJustMove, kOnlyMoveIfOffTheScreen);
                this.redrawEverything();
            }
        }
        // v2.0 switch to select/drag mode - sometimes it seems to get broken - this will fix it - not unreasonable to do
        this.cursorModeForDrawing = kCursorModeSelectDrag;
        this.dragCursorMode.Down = true;
        this.internalChange = false;
    }
    
    public void updateHintPauseForOptions() {
        delphi_compatability.Application.HintPause = udomain.domain.options.pauseBeforeHint * 1000;
        if (udomain.domain.options.showLongHintsForButtons || udomain.domain.options.showHintsForParameters) {
            delphi_compatability.Application.HintHidePause = udomain.domain.options.pauseDuringHint * 1000;
        } else {
            delphi_compatability.Application.HintHidePause = 2500;
        }
        this.statsPanel.updateHint;
    }
    
    public void updateForChangedExportCount() {
        this.caption = this.captionForFile();
    }
    
    public void updateForChangeToDomainOptions() {
        this.internalChange = true;
        // fonts
        // v1.6b1 -- fix for large fonts problem
        this.font.size = udomain.domain.options.parametersFontSize;
        this.parametersScrollBox.Font.Size = udomain.domain.options.parametersFontSize;
        this.parametersScrollBox.Invalidate();
        // viewing option
        this.MenuLayoutMakeBouquet.enabled = (this.selectedPlants.Count > 1) && (!udomain.domain.viewPlantsInMainWindowOnePlantAtATime());
        this.updateMenusForChangeToViewingOption();
        // drawing
        this.MenuOptionsUsePlantBitmaps.checked = udomain.domain.options.cachePlantBitmaps;
        // showing optional things
        this.MenuOptionsShowSelectionRectangles.checked = udomain.domain.options.showSelectionRectangle;
        this.MenuOptionsShowBoundsRectangles.checked = udomain.domain.options.showBoundsRectangle;
        this.MenuOptionsShowLongButtonHints.checked = udomain.domain.options.showLongHintsForButtons;
        this.MenuOptionsShowParameterHints.checked = udomain.domain.options.showHintsForParameters;
        // posing
        this.MenuOptionsGhostHiddenParts.checked = udomain.domain.options.showGhostingForHiddenParts;
        this.posingGhost.Down = udomain.domain.options.showGhostingForHiddenParts;
        this.MenuOptionsHighlightPosedParts.checked = udomain.domain.options.showHighlightingForNonHiddenPosedParts;
        this.posingHighlight.Down = udomain.domain.options.showHighlightingForNonHiddenPosedParts;
        this.MenuOptionsHidePosing.checked = !udomain.domain.options.showPosingAtAll;
        this.posingNotShown.Down = !udomain.domain.options.showPosingAtAll;
        // vertical/horizontal
        this.MenuLayoutHorizontalOrientation.checked = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal;
        this.MenuLayoutVerticalOrientation.checked = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical;
        this.drawingAreaOnTop.Down = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal;
        this.drawingAreaOnSide.Down = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical;
        this.internalChange = false;
        // hint, undo
        this.updateHintPauseForOptions();
        this.commandList.setNewUndoLimit(udomain.domain.options.undoLimit);
        this.commandList.setNewObjectUndoLimit(udomain.domain.options.undoLimitOfPlants);
        if (ubreedr.BreederForm != null) {
            ubreedr.BreederForm.updateForChangeToDomainOptions();
        }
        if (UNRESOLVED.TimeSeriesForm != null) {
            UNRESOLVED.TimeSeriesForm.updateForChangeToDomainOptions;
        }
        if (this.lifeCycleShowing()) {
            //because max drawing scale might have changed
            this.updateLifeCyclePanelForFirstSelectedPlant();
        }
        if (!this.inFormCreation) {
            this.redrawEverything();
        }
        // in case max changed
        this.updateForChangeToPlantBitmaps();
    }
    
    public void updateForChangeToDrawOptions() {
        this.redrawEverything();
        if (ubreedr.BreederForm != null) {
            if ((ubreedr.BreederForm.visible) && (ubreedr.BreederForm.windowState != delphi_compatability.TWindowState.wsMinimized)) {
                ubreedr.BreederForm.redrawPlants(ubreedr.kDontConsiderIfPreviewCacheIsUpToDate);
            } else {
                ubreedr.BreederForm.needToRedrawFromChangeToDrawOptions = true;
            }
        }
        if (UNRESOLVED.TimeSeriesForm != null) {
            if ((UNRESOLVED.TimeSeriesForm.visible) && (UNRESOLVED.TimeSeriesForm.windowState != delphi_compatability.TWindowState.wsMinimized)) {
                UNRESOLVED.TimeSeriesForm.redrawPlants;
            } else {
                UNRESOLVED.TimeSeriesForm.needToRedrawFromChangeToDrawOptions = true;
            }
        }
    }
    
    public void updateMenusForChangeToViewingOption() {
        this.MenuLayoutViewOnePlantAtATime.checked = udomain.domain.viewPlantsInMainWindowOnePlantAtATime();
        this.MenuLayoutViewFreeFloating.checked = udomain.domain.viewPlantsInMainWindowFreeFloating();
        this.viewOneOnly.Down = udomain.domain.viewPlantsInMainWindowOnePlantAtATime();
        this.viewFreeFloating.Down = udomain.domain.viewPlantsInMainWindowFreeFloating();
    }
    
    public void updateForChangeToOrientation() {
        this.MenuLayoutHorizontalOrientation.checked = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal;
        this.MenuLayoutVerticalOrientation.checked = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical;
        this.drawingAreaOnTop.Down = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal;
        this.drawingAreaOnSide.Down = udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical;
        this.resize;
    }
    
    public void moveUpOrDownWithKeyInPlantList(short indexAfterMove) {
        TList newList = new TList();
        PdCommand newCommand = new PdCommand();
        
        if (indexAfterMove > this.plants.Count - 1) {
            // loop around 
            indexAfterMove = 0;
        }
        if (indexAfterMove < 0) {
            indexAfterMove = this.plants.Count - 1;
        }
        if ((indexAfterMove >= 0) && (indexAfterMove <= this.plants.Count - 1)) {
            newList = delphi_compatability.TList().Create();
            try {
                newList.Add(this.plants.Items[indexAfterMove]);
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(this.selectedPlants, newList);
                this.doCommand(newCommand);
            } finally {
                newList.free;
            }
        }
    }
    
    public void updateForChangeToPlantSelections() {
        if (udomain.domain.options.showSelectionRectangle) {
            this.copyDrawingBitmapToPaintBox();
        }
        this.plantListDrawGrid.Repaint();
        // must be done BEFORE updating so it picks it up
        this.selectedPlantPartID = -1;
        this.updateRightSidePanelForFirstSelectedPlant();
        this.updateMenusForChangedSelectedPlants();
        if (!this.internalChange) {
            // reset for posing because posing works only on focused plant
            // don't do if reading file in
            // if change selected plant, must redraw to remove red color
            this.redrawAllPlantsInViewWithAmendments();
        }
    }
    
    public void invalidateSelectedPlantRectangles() {
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.selectedPlants.Count > 0) {
            for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                plant = uplant.PdPlant(this.selectedPlants.Items[i]);
                if (plant != null) {
                    this.invalidateDrawingRect(plant.boundsRect_pixels());
                }
            }
        }
    }
    
    public void updateForChangeToPlantList() {
        PdPlant plant = new PdPlant();
        short i = 0;
        TList plantsToRemove = new TList();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if ((udomain.domain == null) || (udomain.domain.plantManager == null)) {
            return;
        }
        this.caption = this.captionForFile();
        this.plantListDrawGrid.RowCount = this.plants.Count;
        this.plantListDrawGrid.Invalidate();
        // selected plants list - make sure no pointers are invalid 
        plantsToRemove = delphi_compatability.TList().Create();
        try {
            if (this.selectedPlants.Count > 0) {
                for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                    plant = uplant.PdPlant(this.selectedPlants.Items[i]);
                    if (this.plants.IndexOf(plant) < 0) {
                        plantsToRemove.Add(plant);
                    }
                }
            }
            if (plantsToRemove.Count > 0) {
                for (i = 0; i <= plantsToRemove.Count - 1; i++) {
                    plant = uplant.PdPlant(plantsToRemove.Items[i]);
                    this.selectedPlants.Remove(plant);
                }
            }
        } finally {
            plantsToRemove.free;
        }
        if (udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
            this.showOnePlantExclusively(kDrawNow);
        }
        this.updateRightSidePanelForFirstSelectedPlant();
        this.updateForPossibleChangeToDrawing();
        this.updateMenusForChangedPlantList();
    }
    
    public void updateForPossibleChangeToDrawing() {
        this.updateMenusForUndoRedo();
        if ((this.invalidDrawingRect.Top != 0) || (this.invalidDrawingRect.Left != 0) || (this.invalidDrawingRect.Bottom != 0) || (this.invalidDrawingRect.Right != 0)) {
            this.paintDrawing(kDrawNow);
        }
    }
    
    public void recalculateAllPlantBoundsRects(boolean drawNow) {
        short i = 0;
        PdPlant plant = new PdPlant();
        boolean showProgress = false;
        long plantPartsToDraw = 0;
        long partsDrawn = 0;
        
        if (this.plants.Count <= 0) {
            return;
        }
        plantPartsToDraw = 0;
        showProgress = drawNow && udomain.domain.options.cachePlantBitmaps && udomain.domain.options.showPlantDrawingProgress;
        if (showProgress) {
            plantPartsToDraw = udomain.domain.plantManager.totalPlantPartCountInInvalidRect(this.plants, Rect(0, 0, this.drawingBitmap.Width, this.drawingBitmap.Height), udomain.kExcludeInvisiblePlants, udomain.kIncludeNonSelectedPlants);
        }
        partsDrawn = 0;
        try {
            UNRESOLVED.cursor_startWait;
            this.drawing = true;
            if (showProgress) {
                this.startDrawProgress(plantPartsToDraw);
            }
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                plant.plantPartsDrawnAtStart = partsDrawn;
                plant.recalculateBounds(drawNow);
                partsDrawn = partsDrawn + plant.totalPlantParts;
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
            this.drawing = false;
            if (showProgress) {
                this.finishDrawProgress();
            }
        }
    }
    
    public void recalculateSelectedPlantsBoundsRects(boolean drawNow) {
        short i = 0;
        PdPlant plant = new PdPlant();
        boolean showProgress = false;
        long plantPartsToDraw = 0;
        long partsDrawn = 0;
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        plantPartsToDraw = 0;
        showProgress = drawNow && udomain.domain.options.cachePlantBitmaps && udomain.domain.options.showPlantDrawingProgress;
        if (showProgress) {
            plantPartsToDraw = udomain.domain.plantManager.totalPlantPartCountInInvalidRect(this.selectedPlants, Rect(0, 0, this.drawingBitmap.Width, this.drawingBitmap.Height), udomain.kExcludeInvisiblePlants, udomain.kIncludeNonSelectedPlants);
        }
        partsDrawn = 0;
        try {
            UNRESOLVED.cursor_startWait;
            this.drawing = true;
            if (showProgress) {
                this.startDrawProgress(plantPartsToDraw);
            }
            for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                plant = uplant.PdPlant(this.selectedPlants.Items[i]);
                plant.plantPartsDrawnAtStart = partsDrawn;
                plant.recalculateBounds(drawNow);
                partsDrawn = partsDrawn + plant.totalPlantParts;
            }
        } finally {
            UNRESOLVED.cursor_stopWait;
            this.drawing = false;
            if (showProgress) {
                this.finishDrawProgress();
            }
        }
    }
    
    public void shrinkAllPlantBitmaps() {
        short i = 0;
        
        if (this.plants.Count > 0) {
            for (i = 0; i <= this.plants.Count - 1; i++) {
                uplant.PdPlant(this.plants.Items[i]).shrinkPreviewCache();
            }
        }
        this.updateForChangeToPlantBitmaps();
    }
    
    public void recalculateAllPlantBoundsRectsForOffsetChange() {
        short i = 0;
        PdPlant plant = new PdPlant();
        
        for (i = 0; i <= this.plants.Count - 1; i++) {
            plant = uplant.PdPlant(this.plants.Items[i]);
            plant.recalculateBoundsForOffsetChange();
        }
    }
    
    public void updateForRenamingPlant(PdPlant aPlant) {
        short i = 0;
        
        this.plantListDrawGrid.Invalidate();
        for (i = 0; i <= kTabHighest; i++) {
            this.updatePlantNameLabel(i);
        }
    }
    
    public void updateForChangeToPlantNote(PdPlant aPlant) {
        int start = 0;
        
        start = this.noteMemo.SelStart;
        this.noteMemo.Clear();
        if (aPlant == null) {
            return;
        }
        this.internalChange = true;
        if (this.focusedPlant() != null) {
            this.noteMemo.Lines.AddStrings(aPlant.noteLines);
        }
        this.noteMemo.SelStart = start;
        this.internalChange = false;
    }
    
    // menu updating 
    // ---------------------------------------------------------------------------- *menu updating 
    public void updateMenusForUndoRedo() {
        if (this.commandList.isUndoEnabled()) {
            this.MenuEditUndo.enabled = true;
            this.MenuEditUndo.caption = "&Undo " + this.commandList.undoDescription();
        } else {
            this.MenuEditUndo.enabled = false;
            this.MenuEditUndo.caption = "Can't undo";
        }
        if (this.commandList.isRedoEnabled()) {
            this.MenuEditRedo.enabled = true;
            this.MenuEditRedo.caption = "&Redo " + this.commandList.redoDescription();
        } else {
            this.MenuEditRedo.enabled = false;
            this.MenuEditRedo.caption = "Can't redo";
        }
        this.UndoMenuEditUndoRedoList.enabled = (this.commandList.isUndoEnabled()) || (this.commandList.isRedoEnabled());
        if (ubreedr.BreederForm != null) {
            ubreedr.BreederForm.BreederMenuUndo.enabled = this.MenuEditUndo.enabled;
            ubreedr.BreederForm.BreederMenuUndo.caption = this.MenuEditUndo.caption;
            ubreedr.BreederForm.BreederMenuRedo.enabled = this.MenuEditRedo.enabled;
            ubreedr.BreederForm.BreederMenuRedo.caption = this.MenuEditRedo.caption;
            ubreedr.BreederForm.BreederMenuUndoRedoList.enabled = this.UndoMenuEditUndoRedoList.enabled;
        }
        if (UNRESOLVED.TimeSeriesForm != null) {
            //FIX unresolved WITH expression: UNRESOLVED.TimeSeriesForm
            UNRESOLVED.TimeSeriesMenuUndo.enabled = this.MenuEditUndo.enabled;
            UNRESOLVED.TimeSeriesMenuUndo.caption = this.MenuEditUndo.caption;
            UNRESOLVED.TimeSeriesMenuRedo.enabled = this.MenuEditRedo.enabled;
            UNRESOLVED.TimeSeriesMenuRedo.caption = this.MenuEditRedo.caption;
            UNRESOLVED.TimeSeriesMenuUndoRedoList.enabled = this.UndoMenuEditUndoRedoList.enabled;
        }
    }
    
    public void updateMenusForChangedPlantFile() {
        this.MenuFileClose.enabled = udomain.domain.plantFileLoaded;
        this.MenuPlantNew.enabled = udomain.domain.plantFileLoaded;
        this.MenuPlantNewUsingLastWizardSettings.enabled = udomain.domain.plantFileLoaded;
        this.MenuLayoutViewFreeFloating.enabled = udomain.domain.plantFileLoaded;
        this.viewFreeFloating.Enabled = udomain.domain.plantFileLoaded;
        this.MenuLayoutViewOnePlantAtATime.enabled = udomain.domain.plantFileLoaded;
        this.viewOneOnly.Enabled = udomain.domain.plantFileLoaded;
        this.MenuLayoutHorizontalOrientation.enabled = udomain.domain.plantFileLoaded;
        this.drawingAreaOnTop.Enabled = udomain.domain.plantFileLoaded;
        this.MenuLayoutVerticalOrientation.enabled = udomain.domain.plantFileLoaded;
        this.drawingAreaOnSide.Enabled = udomain.domain.plantFileLoaded;
        this.updateMenusForChangedPlantList();
        this.updatePasteMenuForClipboardContents();
    }
    
    public void updateMenusForChangedPlantList() {
        boolean havePlants = false;
        
        havePlants = (this.plants.Count > 0);
        this.MenuFileSave.enabled = havePlants;
        this.MenuFileSaveAs.enabled = havePlants;
        this.MenuFileSaveDrawingAs.enabled = havePlants;
        this.MenuFilePrintDrawing.enabled = havePlants;
        this.MenuLayoutSelectAll.enabled = havePlants;
        this.MenuEditCopyDrawing.enabled = havePlants;
        this.MenuLayoutScaleToFit.enabled = havePlants;
        this.MenuFileMakePainterNozzle.enabled = havePlants;
        this.MenuPlantExportToDXF.enabled = havePlants;
        this.MenuPlantExportToPOV.enabled = havePlants;
        this.MenuPlantExportTo3DS.enabled = havePlants;
        this.MenuFileSaveJPEG.enabled = havePlants;
        this.MenuPlantExportToLWO.enabled = havePlants;
        this.MenuPlantExportToOBJ.enabled = havePlants;
        this.MenuPlantExportToVRML.enabled = havePlants;
        if (!havePlants) {
            this.dragCursorModeClick(this);
        }
        this.toolbarPanel.Enabled = havePlants;
        this.dragCursorMode.Enabled = havePlants;
        this.magnifyCursorMode.Enabled = havePlants;
        this.scrollCursorMode.Enabled = havePlants;
        this.rotateCursorMode.Enabled = havePlants;
        this.posingSelectionCursorMode.Enabled = havePlants;
        this.centerDrawing.Enabled = havePlants;
        this.magnificationPercent.Enabled = havePlants;
        this.updateMenusForChangedSelectedPlants();
    }
    
    public void updateMenusForChangedSelectedPlants() {
        boolean haveSelectedPlants = false;
        boolean haveMoreThanOneSelectedPlant = false;
        
        haveSelectedPlants = (this.selectedPlants.Count > 0);
        haveMoreThanOneSelectedPlant = (this.selectedPlants.Count > 1);
        this.MenuEditCut.enabled = haveSelectedPlants;
        this.PopupMenuCut.enabled = haveSelectedPlants;
        this.MenuEditCopy.enabled = haveSelectedPlants;
        this.PopupMenuCopy.enabled = haveSelectedPlants;
        this.MenuEditCopyAsText.enabled = haveSelectedPlants;
        this.MenuEditPasteAsText.enabled = (UNRESOLVED.Clipboard.hasFormat(UNRESOLVED.CF_TEXT)) && (udomain.domain.plantFileLoaded);
        this.MenuEditDelete.enabled = haveSelectedPlants;
        this.MenuEditDuplicate.enabled = haveSelectedPlants;
        this.MenuPlantRename.enabled = haveSelectedPlants;
        this.PopupMenuRename.enabled = haveSelectedPlants;
        this.MenuPlantEditNote.enabled = haveSelectedPlants;
        // v1.4
        this.PopupMenuEditNote.enabled = haveSelectedPlants;
        // v1.4
        this.noteEdit.Enabled = haveSelectedPlants;
        this.MenuPlantRandomize.enabled = haveSelectedPlants;
        this.PopupMenuRandomize.enabled = haveSelectedPlants;
        this.MenuPlantZeroRotations.enabled = haveSelectedPlants;
        this.PopupMenuZeroRotations.enabled = haveSelectedPlants;
        this.MenuPlantBreed.enabled = haveSelectedPlants;
        this.PopupMenuBreed.enabled = haveSelectedPlants;
        this.MenuPlantMakeTimeSeries.enabled = haveSelectedPlants;
        this.PopupMenuMakeTimeSeries.enabled = haveSelectedPlants;
        this.MenuPlantAnimate.enabled = haveSelectedPlants;
        this.PopupMenuAnimate.enabled = haveSelectedPlants;
        this.MenuLayoutSelectAll.enabled = (this.plants.Count > 0) && (this.selectedPlants.Count < this.plants.Count);
        this.MenuLayoutDeselect.enabled = haveSelectedPlants;
        this.MenuFileMakePainterAnimation.enabled = haveSelectedPlants;
        this.MenuLayoutHide.enabled = haveSelectedPlants;
        this.MenuLayoutShow.enabled = haveSelectedPlants;
        this.MenuLayoutHideOthers.enabled = (haveMoreThanOneSelectedPlant) && (!udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) && (this.selectedPlants.Count < this.plants.Count);
        this.MenuLayoutMakeBouquet.enabled = haveMoreThanOneSelectedPlant && !udomain.domain.viewPlantsInMainWindowOnePlantAtATime();
        this.MenuLayoutBringForward.enabled = haveSelectedPlants && (this.selectedPlants.Count < this.plants.Count);
        this.MenuLayoutSendBack.enabled = haveSelectedPlants && (this.selectedPlants.Count < this.plants.Count);
        // location
        this.xLocationEdit.Enabled = haveSelectedPlants;
        this.xLocationSpin.Enabled = haveSelectedPlants;
        this.yLocationEdit.Enabled = haveSelectedPlants;
        this.yLocationSpin.Enabled = haveSelectedPlants;
        // rotation
        this.xRotationEdit.Enabled = haveSelectedPlants;
        this.xRotationSpin.Enabled = haveSelectedPlants;
        this.yRotationEdit.Enabled = haveSelectedPlants;
        this.yRotationSpin.Enabled = haveSelectedPlants;
        this.zRotationEdit.Enabled = haveSelectedPlants;
        this.zRotationSpin.Enabled = haveSelectedPlants;
        this.resetRotations.Enabled = haveSelectedPlants;
        // drawing scale
        this.drawingScaleEdit.Enabled = haveSelectedPlants;
        this.drawingScaleSpin.Enabled = haveSelectedPlants;
        // alignment
        this.alignTops.Enabled = haveMoreThanOneSelectedPlant;
        this.alignBottoms.Enabled = haveMoreThanOneSelectedPlant;
        this.alignLeft.Enabled = haveMoreThanOneSelectedPlant;
        this.alignRight.Enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutAlign.enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutAlignTops.enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutAlignBottoms.enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutAlignLeftSides.enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutAlignRightSides.enabled = haveMoreThanOneSelectedPlant;
        // size
        this.makeEqualWidth.Enabled = haveMoreThanOneSelectedPlant;
        this.makeEqualHeight.Enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutSize.enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutSizeSameWidth.enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutSizeSameHeight.enabled = haveMoreThanOneSelectedPlant;
        // pack
        this.packPlants.Enabled = haveMoreThanOneSelectedPlant;
        this.MenuLayoutPack.enabled = haveMoreThanOneSelectedPlant;
    }
    
    public void updatePasteMenuForClipboardContents() {
        this.MenuEditPaste.enabled = (udomain.domain.plantManager.privatePlantClipboard.count > 0);
        this.PopupMenuPaste.enabled = this.MenuEditPaste.enabled;
        if (ubreedr.BreederForm != null) {
            ubreedr.BreederForm.updatePasteMenuForClipboardContents();
        }
        if (UNRESOLVED.TimeSeriesForm != null) {
            UNRESOLVED.TimeSeriesForm.updatePasteMenuForClipboardContents;
        }
    }
    
    public void updateSectionPopupMenuForSectionChange() {
        boolean haveSection = false;
        
        haveSection = this.currentSection() != null;
        this.sectionPopupMenuHelp.enabled = haveSection;
    }
    
    public void updateParamPopupMenuForParamSelectionChange() {
        boolean haveSection = false;
        boolean haveParam = false;
        
        haveSection = this.currentSection() != null;
        this.paramPopupMenuExpandAllInSection.enabled = haveSection;
        this.paramPopupMenuCollapseAllInSection.enabled = haveSection;
        haveParam = this.selectedParameterPanel != null;
        this.paramPopupMenuHelp.enabled = haveParam;
        this.paramPopupMenuExpand.enabled = haveParam;
        this.paramPopupMenuCollapse.enabled = haveParam;
    }
    
    // ---------------------------------------------------------------------------- *drawing 
    public void invalidateDrawingRect(TRect aRect) {
        TRect newRect = new TRect();
        
        newRect = this.invalidDrawingRect;
        delphi_compatability.UnionRect(newRect, newRect, aRect);
        this.invalidDrawingRect = newRect;
    }
    
    public void invalidateEntireDrawing() {
        this.invalidDrawingRect = Rect(0, 0, this.drawingBitmap.Width, this.drawingBitmap.Height);
    }
    
    public void paintDrawing(boolean immediate) {
        long plantPartsToDraw = 0;
        boolean showProgress = false;
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        plantPartsToDraw = 0;
        showProgress = udomain.domain.options.showPlantDrawingProgress && (!udomain.domain.options.cachePlantBitmaps);
        if ((this.invalidDrawingRect.Top != 0) || (this.invalidDrawingRect.Left != 0) || (this.invalidDrawingRect.Bottom != 0) || (this.invalidDrawingRect.Right != 0)) {
            try {
                if (!this.mouseMoveActionInProgress) {
                    UNRESOLVED.cursor_startWait;
                }
                UNRESOLVED.intersectClipRect(this.drawingBitmap.Canvas.Handle, this.invalidDrawingRect.Left, this.invalidDrawingRect.Top, this.invalidDrawingRect.Right, this.invalidDrawingRect.Bottom);
                UNRESOLVED.fillBitmap(this.drawingBitmap, udomain.domain.options.backgroundColor);
                if (showProgress) {
                    plantPartsToDraw = udomain.domain.plantManager.totalPlantPartCountInInvalidRect(this.selectedPlants, this.invalidDrawingRect, udomain.kExcludeInvisiblePlants, udomain.kIncludeNonSelectedPlants);
                }
                try {
                    this.drawing = true;
                    if (showProgress) {
                        this.startDrawProgress(plantPartsToDraw);
                    }
                    udomain.domain.plantManager.drawOnInvalidRect(this.drawingBitmap.Canvas, this.selectedPlants, this.invalidDrawingRect, udomain.kExcludeInvisiblePlants, udomain.kIncludeNonSelectedPlants);
                } finally {
                    this.drawing = false;
                    if (showProgress) {
                        this.finishDrawProgress();
                    }
                }
                if ((immediate)) {
                    this.copyDrawingBitmapToPaintBox();
                }
            } finally {
                if (!this.mouseMoveActionInProgress) {
                    UNRESOLVED.cursor_stopWait;
                }
                this.invalidDrawingRect = delphi_compatability.Bounds(0, 0, 0, 0);
            }
        }
    }
    
    public void drawingPaintBoxPaint(TObject Sender) {
        this.copyDrawingBitmapToPaintBox();
    }
    
    public void copyDrawingBitmapToPaintBox() {
        boolean drawSelectionRects = false;
        boolean drawBoundingRects = false;
        boolean includePlant = false;
        short i = 0;
        PdPlant plant = new PdPlant();
        TRect aRect = new TRect();
        TRect insetOneRect = new TRect();
        TRect intersection = new TRect();
        longbool intersectResult = new longbool();
        HPALETTE oldPalette = new HPALETTE();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if ((udomain.domain == null) || (this.plants == null)) {
            return;
        }
        aRect = Rect(0, 0, this.drawingBitmap.Width, this.drawingBitmap.Height);
        // use an inset rect to avoid flicker in the boundary rectangle
        insetOneRect = Rect(1, 1, this.drawingBitmap.Width - 1, this.drawingBitmap.Height - 1);
        oldPalette = 0;
        oldPalette = UNRESOLVED.selectPalette(this.drawingPaintBox.Canvas.Handle, MainForm.paletteImage.Picture.Bitmap.Palette, false);
        UNRESOLVED.realizePalette(this.drawingPaintBox.Canvas.Handle);
        this.drawingPaintBox.Canvas.CopyRect(insetOneRect, this.drawingBitmap.Canvas, insetOneRect);
        this.drawingPaintBox.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        this.drawingPaintBox.Canvas.Pen.Width = 1;
        drawBoundingRects = (udomain.domain.options.showBoundsRectangle) && (!udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) && (!udomain.domain.temporarilyHideSelectionRectangles);
        if ((drawBoundingRects) && (this.plants.Count > 0)) {
            this.drawingPaintBox.Canvas.Pen.Color = delphi_compatability.clSilver;
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (!plant.hidden) {
                    this.drawingPaintBox.Canvas.Rectangle(plant.boundsRect_pixels().Left, plant.boundsRect_pixels().Top, plant.boundsRect_pixels().Right, plant.boundsRect_pixels().Bottom);
                }
            }
        }
        drawSelectionRects = (udomain.domain.options.showSelectionRectangle) && (!udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) && (!udomain.domain.temporarilyHideSelectionRectangles);
        if ((drawSelectionRects) && (this.plants.Count > 0)) {
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                includePlant = false;
                intersectResult = delphi_compatability.IntersectRect(intersection, plant.boundsRect_pixels(), aRect);
                includePlant = includePlant || intersectResult;
                includePlant = includePlant && !plant.hidden;
                if (!includePlant) {
                    continue;
                }
                if (this.isFocused(plant)) {
                    this.drawingPaintBox.Canvas.Pen.Color = udomain.domain.options.firstSelectionRectangleColor;
                    this.drawingPaintBox.Canvas.Rectangle(plant.boundsRect_pixels().Left, plant.boundsRect_pixels().Top, plant.boundsRect_pixels().Right, plant.boundsRect_pixels().Bottom);
                    if (this.cursorModeForDrawing == kCursorModeSelectDrag) {
                        this.drawingPaintBox.Canvas.Brush.Color = this.drawingPaintBox.Canvas.Pen.Color;
                        this.drawingPaintBox.Canvas.Rectangle(plant.resizingRect().Left, plant.resizingRect().Top, plant.resizingRect().Right, plant.resizingRect().Bottom);
                        this.drawingPaintBox.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
                    }
                } else if (this.isSelected(plant)) {
                    this.drawingPaintBox.Canvas.Pen.Color = udomain.domain.options.multiSelectionRectangleColor;
                    this.drawingPaintBox.Canvas.Rectangle(plant.boundsRect_pixels().Left, plant.boundsRect_pixels().Top, plant.boundsRect_pixels().Right, plant.boundsRect_pixels().Bottom);
                }
            }
        }
        this.drawingPaintBox.Canvas.Pen.Color = UNRESOLVED.clBtnText;
        this.drawingPaintBox.Canvas.Rectangle(0, 0, this.drawingPaintBox.Width, this.drawingPaintBox.Height);
        UNRESOLVED.selectPalette(this.drawingPaintBox.Canvas.Handle, oldPalette, true);
        UNRESOLVED.realizePalette(this.drawingPaintBox.Canvas.Handle);
    }
    
    // plant bitmaps
    // ---------------------------------------------------------------------------- *bitmaps for plants 
    public float screenBytesPerPixel() {
        result = 0.0;
        HDC screenDC = new HDC();
        
        screenDC = UNRESOLVED.GetDC(0);
        try {
            result = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES));
            result = result / 8.0;
        } finally {
            UNRESOLVED.ReleaseDC(0, screenDC);
        }
        return result;
    }
    
    public long bytesInPlantBitmaps(PdPlant plantToExclude) {
        result = 0;
        long bytesInBitmap = 0;
        float bytesPerPixel = 0.0;
        short i = 0;
        PdPlant plant = new PdPlant();
        
        result = 0;
        bytesPerPixel = this.screenBytesPerPixel();
        if (this.plants.Count > 0) {
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (plant.hidden) {
                    continue;
                }
                if (plant == plantToExclude) {
                    // plant that is asking should not be counted, since it is looking to resize and lose the old size
                    continue;
                }
                bytesInBitmap = intround(plant.previewCache.Width * plant.previewCache.Height * bytesPerPixel);
                result = result + bytesInBitmap;
            }
        }
        return result;
    }
    
    public boolean roomForPlantBitmap(PdPlant plant, long bytesForThisPlant) {
        result = false;
        long bytesAlreadyNotIncludingThisPlant = 0;
        long bytesLimit = 0;
        float megabytesTried = 0.0;
        
        bytesAlreadyNotIncludingThisPlant = this.bytesInPlantBitmaps(plant);
        bytesLimit = udomain.domain.options.memoryLimitForPlantBitmaps_MB * 1024 * 1024;
        result = bytesAlreadyNotIncludingThisPlant + bytesForThisPlant < bytesLimit;
        if (!result) {
            megabytesTried = (bytesAlreadyNotIncludingThisPlant + bytesForThisPlant) / (1024 * 1024);
            ShowMessage("The total size of plant bitmaps (" + FloatToStrF(megabytesTried, UNRESOLVED.ffFixed, 7, 1) + ") has exceeded " + "the memory limit of " + IntToStr(udomain.domain.options.memoryLimitForPlantBitmaps_MB) + " megabytes." + chr(13) + "All plant bitmaps have been dropped and plants will be drawn directly on the window." + chr(13) + "To use plant bitmaps again, choose Use Plant Bitmaps from the Options menu." + chr(13) + chr(13) + "If you have more free memory, your memory limit is set too low." + chr(13) + "To increase the memory limit, choose Preferences from the Edit menu." + chr(13) + "Click Help in the Preferences window for details.");
            this.stopUsingPlantBitmaps();
        }
        return result;
    }
    
    public void exceptionResizingPlantBitmap() {
        ShowMessage("An exception occurred while resizing a plant bitmap. " + chr(13) + "All plant bitmaps have been dropped and plants will be drawn directly on the window." + chr(13) + "To use plant bitmaps again, choose Use Plant Bitmaps from the Options menu." + chr(13) + chr(13) + "This exception means that your memory limit is set too high for the available memory." + chr(13) + "To decrease the memory limit, choose Preferences from the Edit menu." + chr(13) + "Click Help in the Preferences window for details.");
        this.stopUsingPlantBitmaps();
    }
    
    public void updateForChangeToPlantBitmaps() {
        String aString = "";
        long bytesInUse = 0;
        float megabytesInUse = 0.0;
        
        if (udomain.domain.options.showLongHintsForButtons) {
            aString = "Plant bitmaps are used to speed up drawing by caching each plant into a separate " + "bitmap in memory. Plant bitmaps are turned ";
        } else {
            aString = "Plant bitmaps are turned ";
        }
        bytesInUse = 0;
        megabytesInUse = 0;
        if (udomain.domain.options.cachePlantBitmaps) {
            bytesInUse = this.bytesInPlantBitmaps(null);
            megabytesInUse = bytesInUse / (1024 * 1024);
            aString = aString + "ON and are using " + FloatToStrF(megabytesInUse, UNRESOLVED.ffFixed, 7, 1) + " out of " + IntToStr(udomain.domain.options.memoryLimitForPlantBitmaps_MB) + " MB of memory.";
        } else {
            aString = aString + "OFF.";
        }
        if (udomain.domain.options.showLongHintsForButtons) {
            if (!udomain.domain.options.cachePlantBitmaps) {
                aString = aString + " You can turn plant bitmaps on using the Options menu.";
            } else {
                aString = aString + " You can change the amount of memory dedicated to plant bitmaps in the Preferences window.";
            }
        }
        if (this.plantBitmapsIndicatorImage != null) {
            if (udomain.domain.options.cachePlantBitmaps) {
                if (megabytesInUse / udomain.domain.options.memoryLimitForPlantBitmaps_MB <= 0.5) {
                    this.plantBitmapsIndicatorImage.Picture = this.plantBitmapsGreenImage.Picture;
                } else if (megabytesInUse / udomain.domain.options.memoryLimitForPlantBitmaps_MB <= 0.8) {
                    this.plantBitmapsIndicatorImage.Picture = this.plantBitmapsYellowImage.Picture;
                } else {
                    this.plantBitmapsIndicatorImage.Picture = this.plantBitmapsRedImage.Picture;
                }
            } else {
                this.plantBitmapsIndicatorImage.Picture = this.noPlantBitmapsImage.Picture;
            }
            this.plantBitmapsIndicatorImage.Hint = aString;
        }
    }
    
    public void stopUsingPlantBitmaps() {
        udomain.domain.options.cachePlantBitmaps = false;
        this.MenuOptionsUsePlantBitmaps.checked = udomain.domain.options.cachePlantBitmaps;
        this.shrinkAllPlantBitmaps();
        this.invalidateEntireDrawing();
    }
    
    public void startUsingPlantBitmaps() {
        udomain.domain.options.cachePlantBitmaps = true;
        this.MenuOptionsUsePlantBitmaps.checked = udomain.domain.options.cachePlantBitmaps;
        this.recalculateAllPlantBoundsRects(kDrawNow);
        this.invalidateEntireDrawing();
    }
    
    // command list management 
    // ---------------------------------------------------------------------------- *command list management 
    public void clearCommandList() {
        this.commandList.free;
        this.commandList = null;
        this.commandList = ucommand.PdCommandList().create();
        this.updateMenusForUndoRedo();
    }
    
    public void doCommand(PdCommand command) {
        this.commandList.doCommand(command);
        this.updateForPossibleChangeToDrawing();
    }
    
    // called by commands 
    // ------------------------------------------------------------------------------- *called by commands 
    public void hideOrShowSomePlants(TList plantList, TList hideList, boolean hide, boolean drawNow) {
        TRect redrawRect = new TRect();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if ((plantList == null) || (plantList.Count <= 0)) {
            return;
        }
        redrawRect = delphi_compatability.Bounds(0, 0, 0, 0);
        for (i = 0; i <= plantList.Count - 1; i++) {
            plant = uplant.PdPlant(plantList.Items[i]);
            if ((hideList != null) && (hideList.Count > 0)) {
                plant.hidden = updcom.PdBooleanValue(hideList.Items[i]).saveBoolean;
            } else {
                plant.hidden = hide;
            }
            // magnification might have changed
            plant.recalculateBounds(kDrawNow);
            delphi_compatability.UnionRect(redrawRect, redrawRect, plant.boundsRect_pixels());
        }
        this.invalidateDrawingRect(redrawRect);
        this.plantListDrawGrid.Invalidate();
        if (drawNow) {
            this.updateForPossibleChangeToDrawing();
        }
    }
    
    public void fitVisiblePlantsInDrawingArea(boolean drawNow, boolean scaleAsWellAsMove, boolean alwaysMove) {
        TPoint upperLeft_mm = new TPoint();
        TPoint lowerRight_mm = new TPoint();
        TPoint size_mm = new TPoint();
        TPoint offScreenUpperLeft_mm = new TPoint();
        TPoint offScreenLowerRight_mm = new TPoint();
        float xScale_pixelsPerMm = 0.0;
        float yScale_pixelsPerMm = 0.0;
        float newScale_pixelsPerMm = 0.0;
        float marginOffset_mm = 0.0;
        short i = 0;
        PdPlant plant = new PdPlant();
        boolean allPlantsAreOffscreen = false;
        
        if (this.plants.Count <= 0) {
            return;
        }
        for (i = 0; i <= this.plants.Count - 1; i++) {
            plant = uplant.PdPlant(this.plants.Items[i]);
            if (!plant.hidden) {
                plant.recalculateBounds(kDontDrawYet);
            }
        }
        upperLeft_mm = this.upperLeftMostPlantBoundsRectPoint_mm();
        lowerRight_mm = this.lowerRightMostPlantBoundsRectPoint_mm();
        size_mm = Point(lowerRight_mm.X - upperLeft_mm.X, lowerRight_mm.Y - upperLeft_mm.Y);
        if (alwaysMove) {
            // move domain offset so all plants begin within drawing area
            allPlantsAreOffscreen = false;
        } else {
            // determine if all plants are out of the drawing area and so must be moved
            offScreenUpperLeft_mm.X = intround(kOffscreenMargin / udomain.domain.plantManager.plantDrawScale_pixelsPerMm);
            offScreenUpperLeft_mm.Y = intround(kOffscreenMargin / udomain.domain.plantManager.plantDrawScale_pixelsPerMm);
            offScreenLowerRight_mm.X = intround((this.drawingPaintBox.Width - kOffscreenMargin) / udomain.domain.plantManager.plantDrawScale_pixelsPerMm);
            offScreenLowerRight_mm.Y = intround((this.drawingPaintBox.Height - kOffscreenMargin) / udomain.domain.plantManager.plantDrawScale_pixelsPerMm);
            allPlantsAreOffscreen = (lowerRight_mm.X <= offScreenUpperLeft_mm.X) || (lowerRight_mm.Y <= offScreenUpperLeft_mm.Y) || (upperLeft_mm.X >= offScreenLowerRight_mm.X) || (upperLeft_mm.Y >= offScreenLowerRight_mm.Y);
        }
        if (scaleAsWellAsMove) {
            xScale_pixelsPerMm = umath.safedivExcept(1.0 * this.drawingPaintBox.Width - 1.0 * kScaleToFitMargin * 2, size_mm.X, 0);
            yScale_pixelsPerMm = umath.safedivExcept(1.0 * this.drawingPaintBox.Height - 1.0 * kScaleToFitMargin * 2, size_mm.Y, 0);
            newScale_pixelsPerMm = umath.min(xScale_pixelsPerMm, yScale_pixelsPerMm);
        } else {
            newScale_pixelsPerMm = 0;
        }
        if (alwaysMove || allPlantsAreOffscreen) {
            marginOffset_mm = umath.safedivExcept(1.0 * kScaleToFitMargin, newScale_pixelsPerMm, 0);
            udomain.domain.plantManager.plantDrawOffset_mm = usupport.setSinglePoint(-upperLeft_mm.X + marginOffset_mm, -upperLeft_mm.Y + marginOffset_mm);
        }
        if ((scaleAsWellAsMove) && (newScale_pixelsPerMm != 0.0)) {
            // calculate new scale to fit all plants in drawing area and apply
            this.magnifyOrReduce(newScale_pixelsPerMm, Point(0, 0), drawNow);
        }
    }
    
    // ------------------------------------------------------------------------------- *selected plants list 
    public void selectPlantAtPoint(TPoint aPoint, boolean shift) {
        PdCommand newCommand = new PdCommand();
        TList newList = new TList();
        PdPlant plant = new PdPlant();
        short i = 0;
        
        plant = udomain.domain.plantManager.findPlantAtPoint(aPoint);
        newList = delphi_compatability.TList().Create();
        try {
            if ((shift) && (this.selectedPlants.Count > 0)) {
                for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                    newList.Add(this.selectedPlants.Items[i]);
                }
            }
            if (newList.IndexOf(plant) >= 0) {
                newList.Remove(plant);
            } else if (plant != null) {
                newList.Add(plant);
            }
            if (!this.twoListsAreIdentical(this.selectedPlants, newList)) {
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(this.selectedPlants, newList);
                this.doCommand(newCommand);
            }
        } finally {
            newList.free;
        }
    }
    
    public void selectPlantAtIndex(TShiftState Shift, int index) {
        PdCommand newCommand = new PdCommand();
        TList newList = new TList();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.plants.Count <= 0) {
            return;
        }
        if ((index < 0)) {
            if (this.selectedPlants.Count <= 0) {
                return;
            }
            newList = delphi_compatability.TList().Create();
            try {
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(this.selectedPlants, newList);
                this.doCommand(newCommand);
            } finally {
                newList.free;
            }
            return;
        }
        plant = uplant.PdPlant(this.plants.Items[index]);
        if (plant == null) {
            return;
        }
        newList = delphi_compatability.TList().Create();
        try {
            if ((delphi_compatability.TShiftStateEnum.ssCtrl in Shift)) {
                if (this.selectedPlants.Count > 0) {
                    for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                        newList.Add(this.selectedPlants.Items[i]);
                    }
                }
                if (newList.IndexOf(plant) >= 0) {
                    newList.Remove(plant);
                } else {
                    newList.Add(plant);
                }
            } else if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                if (this.selectedPlants.Count > 0) {
                    for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                        newList.Add(this.selectedPlants.Items[i]);
                    }
                }
                if ((this.lastSingleClickPlantIndex >= 0) && (this.lastSingleClickPlantIndex <= this.plants.Count - 1) && (this.lastSingleClickPlantIndex != index)) {
                    if (this.lastSingleClickPlantIndex < index) {
                        for (i = this.lastSingleClickPlantIndex; i <= index; i++) {
                            if (newList.IndexOf(this.plants.Items[i]) < 0) {
                                newList.Add(this.plants.Items[i]);
                            }
                        }
                    } else if (this.lastSingleClickPlantIndex > index) {
                        for (i = this.lastSingleClickPlantIndex; i >= index; i--) {
                            if (newList.IndexOf(this.plants.Items[i]) < 0) {
                                newList.Add(this.plants.Items[i]);
                            }
                        }
                    }
                }
            } else {
                if (this.isSelected(plant)) {
                    if (this.selectedPlants.Count > 0) {
                        for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
                            newList.Add(this.selectedPlants.Items[i]);
                        }
                    }
                } else {
                    newList.Add(plant);
                    this.lastSingleClickPlantIndex = index;
                }
            }
            if (!this.twoListsAreIdentical(this.selectedPlants, newList)) {
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(this.selectedPlants, newList);
                this.doCommand(newCommand);
            }
        } finally {
            newList.free;
        }
    }
    
    public boolean twoListsAreIdentical(TList firstList, TList secondList) {
        result = false;
        long i = 0;
        
        result = false;
        if ((firstList == null) || (secondList == null)) {
            return result;
        }
        if (firstList.Count != secondList.Count) {
            return result;
        }
        if (firstList.Count <= 0) {
            return result;
        }
        for (i = 0; i <= firstList.Count - 1; i++) {
            if (firstList.Items[i] != secondList.Items[i]) {
                return result;
            }
        }
        result = true;
        return result;
    }
    
    public void deselectAllPlants() {
        this.selectedPlants.Clear();
        this.updateForChangeToPlantSelections();
    }
    
    public void deselectAllPlantsButFirst() {
        PdPlant firstPlant = new PdPlant();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        firstPlant = this.focusedPlant();
        this.selectedPlants.Clear();
        this.selectedPlants.Add(firstPlant);
        this.updateForChangeToPlantSelections();
    }
    
    public void selectFirstPlantInPlantList() {
        if (this.plants.Count <= 0) {
            return;
        }
        this.selectedPlants.Clear();
        this.selectedPlants.Add(this.plants.Items[0]);
        this.updateForChangeToPlantSelections();
    }
    
    public void showOnePlantExclusively(boolean drawNow) {
        TListCollection booleansList = new TListCollection();
        short i = 0;
        PdPlant plant = new PdPlant();
        PdPlant firstPlant = new PdPlant();
        
        booleansList = null;
        firstPlant = this.focusedPlant();
        try {
            UNRESOLVED.cursor_startWait;
            booleansList = ucollect.TListCollection().Create();
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (plant != null) {
                    booleansList.Add(updcom.PdBooleanValue().createWithBoolean(!(plant == firstPlant)));
                }
            }
            this.hideOrShowSomePlants(this.plants, booleansList, false, kDontDrawYet);
            this.fitVisiblePlantsInDrawingArea(kDontDrawYet, kScaleAndMove, kAlwaysMove);
            if (firstPlant != null) {
                // must draw now because bitmap could be wrong
                firstPlant.recalculateBounds(kDrawNow);
                this.invalidateDrawingRect(firstPlant.boundsRect_pixels());
            }
            if (drawNow) {
                this.updateForPossibleChangeToDrawing();
            }
        } finally {
            booleansList.free;
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public void redrawFocusedPlantOnly(boolean drawNow) {
        PdPlant firstPlant = new PdPlant();
        
        firstPlant = this.focusedPlant();
        if (firstPlant != null) {
            firstPlant.recalculateBounds(kDrawNow);
            this.invalidateDrawingRect(firstPlant.boundsRect_pixels());
        }
        if (drawNow) {
            this.updateForPossibleChangeToDrawing();
        }
    }
    
    public void addSelectedPlant(PdPlant aPlant, short insertIndex) {
        if ((insertIndex >= 0) && (insertIndex <= this.selectedPlants.Count - 1)) {
            this.selectedPlants.Insert(insertIndex, aPlant);
        } else {
            this.selectedPlants.Add(aPlant);
        }
        this.invalidateDrawingRect(aPlant.boundsRect_pixels());
    }
    
    public void removeSelectedPlant(PdPlant aPlant) {
        this.invalidateDrawingRect(aPlant.boundsRect_pixels());
        this.selectedPlants.Remove(aPlant);
    }
    
    public boolean isSelected(PdPlant plant) {
        result = false;
        result = false;
        if ((this.selectedPlants == null) || (this.selectedPlants.Count <= 0)) {
            return result;
        }
        result = this.selectedPlants.IndexOf(plant) >= 0;
        return result;
    }
    
    public boolean isFocused(PdPlant plant) {
        result = false;
        result = false;
        if (plant == null) {
            return result;
        }
        if ((this.selectedPlants == null) || (this.selectedPlants.Count <= 0)) {
            return result;
        }
        result = this.selectedPlants.IndexOf(plant) == 0;
        return result;
    }
    
    // selected plants list 
    public PdPlant focusedPlant() {
        result = new PdPlant();
        result = null;
        if (this.selectedPlants.Count > 0) {
            result = uplant.PdPlant(this.selectedPlants.Items[0]);
        }
        return result;
    }
    
    public short focusedPlantIndex() {
        result = 0;
        result = -1;
        if (this.selectedPlants.Count > 0) {
            result = this.plants.IndexOf(uplant.PdPlant(this.selectedPlants.Items[0]));
        }
        return result;
    }
    
    public PdPlant firstUnfocusedPlant() {
        result = new PdPlant();
        result = null;
        if (this.selectedPlants.Count > 1) {
            result = uplant.PdPlant(this.selectedPlants.Items[1]);
        }
        return result;
    }
    
    public PdPlant firstSelectedPlantInList() {
        result = new PdPlant();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        result = null;
        if (this.plants.Count > 0) {
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (this.isSelected(plant)) {
                    result = plant;
                    return result;
                }
            }
        }
        return result;
    }
    
    public PdPlant lastSelectedPlantInList() {
        result = new PdPlant();
        short i = 0;
        PdPlant plant = new PdPlant();
        
        result = null;
        if (this.plants.Count > 0) {
            for (i = this.plants.Count - 1; i >= 0; i--) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (this.isSelected(plant)) {
                    result = plant;
                    return result;
                }
            }
        }
        return result;
    }
    
    // ------------------------------------------------------------------------------------- *list of plants 
    public void plantListDrawGridDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        PdPlant plant = new PdPlant();
        boolean selected = false;
        TRect visibleRect = new TRect();
        TRect remainderRect = new TRect();
         cText = [0] * (range(0, 255 + 1) + 1);
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        this.plantListDrawGrid.Canvas.Brush.Color = this.plantListDrawGrid.Color;
        this.plantListDrawGrid.Canvas.FillRect(Rect);
        if ((this.plants.Count <= 0) || (Row < 0) || (Row > this.plants.Count - 1)) {
            return;
        }
        // set up plant pointer 
        plant = uplant.PdPlant(this.plants.Items[Row]);
        if (plant == null) {
            return;
        }
        selected = this.isSelected(plant);
        // set up rectangles 
        visibleRect = Rect;
        visibleRect.Right = visibleRect.Left + this.plantListDrawGrid.DefaultRowHeight;
        remainderRect = Rect;
        remainderRect.Left = remainderRect.Left + usupport.rWidth(visibleRect);
        // fill first box with white, rest with clHighlight if selected 
        this.plantListDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        this.plantListDrawGrid.Canvas.Brush.Color = this.plantListDrawGrid.Color;
        this.plantListDrawGrid.Canvas.FillRect(visibleRect);
        if (!plant.hidden) {
            this.plantListDrawGrid.Canvas.Draw(visibleRect.Left + (visibleRect.Right - visibleRect.Left) / 2 - this.visibleBitmap.Picture.Bitmap.Width / 2, Rect.top, this.visibleBitmap.Picture.Bitmap);
        }
        this.plantListDrawGrid.Canvas.Font = this.plantListDrawGrid.Font;
        if (selected) {
            this.plantListDrawGrid.Canvas.Brush.Color = UNRESOLVED.clHighlight;
            this.plantListDrawGrid.Canvas.Font.Color = UNRESOLVED.clHighlightText;
        } else {
            this.plantListDrawGrid.Canvas.Brush.Color = this.plantListDrawGrid.Color;
            this.plantListDrawGrid.Canvas.Font.Color = UNRESOLVED.clBtnText;
        }
        this.plantListDrawGrid.Canvas.FillRect(remainderRect);
        UNRESOLVED.strPCopy(cText, plant.getName());
        // margin for text 
        remainderRect.Left = remainderRect.Left + 5;
        UNRESOLVED.winprocs.drawText(this.plantListDrawGrid.Canvas.Handle, cText, len(cText), remainderRect, delphi_compatability.DT_LEFT);
        if (plant == this.focusedPlant()) {
            UNRESOLVED.drawFocusRect(Rect);
        }
    }
    
    public void plantListDrawGridMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        int col = 0;
        int row = 0;
        PdPlant plant = new PdPlant();
        TList hideList = new TList();
        PdCommand newCommand = new PdCommand();
        
        if (this.plants.Count <= 0) {
            return;
        }
        if (Button == delphi_compatability.TMouseButton.mbRight) {
            return;
        }
        if (this.justDoubleClickedOnDrawGrid) {
            this.justDoubleClickedOnDrawGrid = false;
            return;
        } else {
            this.justDoubleClickedOnDrawGrid = false;
        }
        col, row = this.plantListDrawGrid.MouseToCell(X, Y, col, row);
        // does updating in command
        this.selectPlantAtIndex(Shift, row);
        if ((X <= 16) && (row >= 0) && (row <= this.plants.Count - 1)) {
            plant = uplant.PdPlant(this.plants.Items[row]);
            if (plant == null) {
                return;
            }
            hideList = delphi_compatability.TList().Create();
            try {
                hideList.Add(plant);
                newCommand = updcom.PdHideOrShowCommand().createWithListOfPlantsAndHideOrShow(hideList, !plant.hidden);
                this.doCommand(newCommand);
            } finally {
                hideList.free;
            }
        }
        if (X > 16) {
            this.plantListDrawGrid.BeginDrag(false);
        }
    }
    
    public void plantListDrawGridMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint popupPositionInScreenCoords = new TPoint();
        
        if (Button == delphi_compatability.TMouseButton.mbRight) {
            popupPositionInScreenCoords = this.plantListDrawGrid.ClientToScreen(Point(X, Y));
            this.PlantPopupMenu.popup(popupPositionInScreenCoords.X, popupPositionInScreenCoords.Y);
        }
    }
    
    public void plantListDrawGridDragOver(TObject Sender, TObject Source, int X, int Y, TDragState State, boolean Accept) {
        Accept = (Source != null) && (Sender != null) && ((ubreedr.BreederForm != null) && (Source == ubreedr.BreederForm.plantsDrawGrid) || (UNRESOLVED.TimeSeriesForm != null) && (Source == UNRESOLVED.TimeSeriesForm.grid));
        return Accept;
    }
    
    public void plantListDrawGridEndDrag(TObject Sender, TObject Target, int X, int Y) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if ((Target != null) && (Target instanceof delphi_compatability.TDrawGrid)) {
            if (this.focusedPlant() != null) {
                if ((((delphi_compatability.TDrawGrid)Target).owner instanceof ubreedr.TBreederForm)) {
                    ubreedr.BreederForm.copyPlantToPoint(this.focusedPlant(), X, Y);
                } else if ((((delphi_compatability.TDrawGrid)Target).owner instanceof UNRESOLVED.TTimeSeriesForm)) {
                    UNRESOLVED.TimeSeriesForm.copyPlantToPoint(this.focusedPlant(), X, Y);
                }
            }
        }
    }
    
    public void plantListDrawGridDblClick(TObject Sender) {
        this.MenuPlantRenameClick(this);
        this.plantListDrawGrid.endDrag(false);
        this.justDoubleClickedOnDrawGrid = true;
    }
    
    // list box 
    public void moveSelectedPlantsUp() {
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.plants.Count > 1) {
            // start at 1 because you can't move first one up any more 
            i = 1;
            while (i <= this.plants.Count - 1) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (this.isSelected(plant)) {
                    this.plants.Move(i, i - 1);
                }
                i += 1;
            }
        }
        this.invalidateSelectedPlantRectangles();
        this.updateForPossibleChangeToDrawing();
        this.plantListDrawGrid.Invalidate();
    }
    
    public void moveSelectedPlantsDown() {
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.plants.Count > 1) {
            // start at next to last one because you can't move last one down any more 
            i = this.plants.Count - 2;
            while (i >= 0) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (this.isSelected(plant)) {
                    this.plants.Move(i, i + 1);
                }
                i -= 1;
            }
        }
        this.invalidateSelectedPlantRectangles();
        this.updateForPossibleChangeToDrawing();
        this.plantListDrawGrid.Invalidate();
    }
    
    public void plantListDrawGridKeyDown(TObject Sender, byte Key, TShiftState Shift) {
        switch (Key) {
            case delphi_compatability.VK_DOWN:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.MenuLayoutSendBackClick(this);
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKeyInPlantList(this.focusedPlantIndex() + 1);
                }
                break;
            case delphi_compatability.VK_RIGHT:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.MenuLayoutSendBackClick(this);
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKeyInPlantList(this.focusedPlantIndex() + 1);
                }
                break;
            case delphi_compatability.VK_UP:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.MenuLayoutBringForwardClick(this);
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKeyInPlantList(this.focusedPlantIndex() - 1);
                }
                break;
            case delphi_compatability.VK_LEFT:
                if ((delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
                    //swallow key
                    Key = 0;
                    this.MenuLayoutBringForwardClick(this);
                } else {
                    Key = 0;
                    this.moveUpOrDownWithKeyInPlantList(this.focusedPlantIndex() - 1);
                }
                break;
            case delphi_compatability.VK_RETURN:
                Key = 0;
                this.MenuPlantRenameClick(this);
                break;
        return Key;
    }
    
    // mouse handling in drawing 
    // -------------------------------------------------------------------------- *mouse handling in drawing 
    public void PaintBoxMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        PdCommand newCommand = new PdCommand();
        TPoint anchorPoint = new TPoint();
        PdPlant plantClickedOn = new PdPlant();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.plants.Count <= 0) {
            return;
        }
        if (this.actionInProgress) {
            try {
                // error somewhere - user did weird things with mouse buttons - teminate action...
                this.PaintBoxMouseUp(Sender, Button, Shift, X, Y);
            } finally {
                this.actionInProgress = false;
            }
        }
        switch (this.cursorModeForDrawing) {
            case kCursorModeSelectDrag:
                if (Button == delphi_compatability.TMouseButton.mbRight) {
                    return;
                }
                plantClickedOn = null;
                plantClickedOn = udomain.domain.plantManager.findPlantAtPoint(Point(X, Y));
                if (plantClickedOn == null) {
                    if (udomain.domain.viewPlantsInMainWindowOnePlantAtATime()) {
                        return;
                    }
                    this.rubberBanding = true;
                    this.rubberBandStartDragPoint = Point(X, Y);
                    this.rubberBandLastDrawPoint = Point(X, Y);
                    this.rubberBandNeedToRedraw = true;
                    // select command made in mouse up
                    return;
                } else {
                    this.actionInProgress = true;
                    if ((!plantClickedOn.pointIsInResizingRect(Point(X, Y))) && ((!this.isSelected(plantClickedOn)) || (delphi_compatability.TShiftStateEnum.ssShift in Shift))) {
                        this.selectPlantAtPoint(Point(X, Y), (delphi_compatability.TShiftStateEnum.ssShift in Shift) && (!(delphi_compatability.TShiftStateEnum.ssCtrl in Shift)));
                        this.updateForPossibleChangeToDrawing();
                    }
                }
                break;
            case kCursorModeScroll:
                break;
            case kCursorModeMagnify:
                this.rubberBanding = true;
                this.rubberBandStartDragPoint = Point(X, Y);
                this.rubberBandLastDrawPoint = Point(X, Y);
                this.rubberBandNeedToRedraw = true;
                break;
            case kCursorModeRotate:
                break;
            case kCursorModePosingSelect:
                if (udomain.domain.options.drawSpeed != udomain.kDrawBest) {
                    if (MessageDialog("To pose a plant, you need the \"Draw Using\" option set to \"Solids.\"" + chr(13) + chr(13) + "Do you want to change it?", mtConfirmation, {mbYes, mbNo, }, 0) == delphi_compatability.IDYES) {
                        this.MenuOptionsBestDrawClick(this);
                    }
                    return;
                }
                if (this.tabSet.tabIndex != kTabPosing) {
                    this.tabSet.tabIndex = kTabPosing;
                }
                plantClickedOn = null;
                plantClickedOn = udomain.domain.plantManager.findPlantAtPoint(Point(X, Y));
                if (this.isFocused(plantClickedOn)) {
                    this.mouseDownSelectedPlantPartID, this.mouseDownSelectedPlantPartType = plantClickedOn.getInfoForPlantPartAtPoint(Point(X, Y), this.mouseDownSelectedPlantPartID, this.mouseDownSelectedPlantPartType);
                } else {
                    this.mouseDownSelectedPlantPartID = -1;
                }
                if (this.mouseDownSelectedPlantPartID == this.selectedPlantPartID) {
                    return;
                }
                break;
        anchorPoint = Point(X, Y);
        // makes shift-click work as right-click
        this.commandList.rightButtonDown = (Button == delphi_compatability.TMouseButton.mbRight) || (delphi_compatability.TShiftStateEnum.ssShift in Shift);
        newCommand = this.makeMouseCommand(anchorPoint, Shift);
        if (newCommand != null) {
            this.actionInProgress = this.commandList.mouseDown(newCommand, anchorPoint);
        } else {
            this.actionInProgress = false;
        }
        if (this.actionInProgress) {
            this.updateForPossibleChangeToDrawing();
        }
    }
    
    public void PaintBoxMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        boolean shouldCancelHint = false;
        PdPlant plantClickedOn = new PdPlant();
        TRect aRect = new TRect();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.plants.Count <= 0) {
            return;
        }
        if (this.cursorModeForDrawing == kCursorModeSelectDrag) {
            // show cursor that tells you you can resize plant when mouse is in resize rect, but only in select mode
            delphi_compatability.Screen.Cursor = delphi_compatability.crDefault;
            plantClickedOn = udomain.domain.plantManager.findPlantAtPoint(Point(X, Y));
            if ((udomain.domain.options.showSelectionRectangle) && (plantClickedOn != null) && (plantClickedOn == this.focusedPlant()) && (plantClickedOn.pointIsInResizingRect(Point(X, Y)))) {
                delphi_compatability.Screen.Cursor = delphi_compatability.crSizeNS;
            }
        }
        if (!this.actionInProgress) {
            // show hint for plant mouse is over
            shouldCancelHint = false;
            if (this.hintActive && ((X < this.hintX - kHintRange) || (X > this.hintX + kHintRange) || (Y < this.hintY - kHintRange) || (Y > this.hintY + kHintRange))) {
                if (this.hintForPlantAtPoint(Point(X, Y)) != this.lastHintString) {
                    shouldCancelHint = true;
                }
                if (this.actionInProgress) {
                    shouldCancelHint = true;
                }
                if (((X < this.hintX - kMaxHintRangeForLargeAreas) || (X > this.hintX + kMaxHintRangeForLargeAreas) || (Y < this.hintY - kMaxHintRangeForLargeAreas) || (Y > this.hintY + kMaxHintRangeForLargeAreas))) {
                    shouldCancelHint = true;
                }
                if (shouldCancelHint) {
                    delphi_compatability.Application.CancelHint();
                    this.hintActive = false;
                }
            }
        }
        if (this.rubberBanding) {
            // continue rubber banding - could be done in either select or magnify mode
            this.undrawRubberBandBox();
            this.drawRubberBandBox(Point(X, Y));
            return;
        }
        if (this.actionInProgress) {
            // continue action started in mouse down
            this.commandList.mouseMove(Point(X, Y));
            if (this.commandList.didMouseMove(Point(X, Y))) {
                this.mouseMoveActionInProgress = true;
            }
            this.updateForPossibleChangeToDrawing();
        }
    }
    
    public void PaintBoxMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TPoint popupPositionInScreenCoords = new TPoint();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.plants.Count <= 0) {
            return;
        }
        if ((Button == delphi_compatability.TMouseButton.mbRight) && (this.cursorModeForDrawing == kCursorModeSelectDrag)) {
            // show popup menu but only if in select/drag mode
            popupPositionInScreenCoords = UNRESOLVED.clientToScreen(Point(X, Y));
            this.PlantPopupMenu.popup(popupPositionInScreenCoords.X, popupPositionInScreenCoords.Y);
            return;
        }
        if (this.rubberBanding) {
            // finish rubber banding if doing that, could be in select or magnify mode
            this.rubberBanding = false;
            this.undrawRubberBandBox();
            if (this.cursorModeForDrawing == kCursorModeSelectDrag) {
                this.selectPlantsInRubberBandBox();
                return;
            }
        }
        try {
            if (this.actionInProgress) {
                // finish action in progress
                this.commandList.mouseUp(Point(X, Y));
                this.actionInProgress = false;
            }
            this.mouseMoveActionInProgress = false;
            this.updateForPossibleChangeToDrawing();
        } finally {
            // clear out all mouse settings
            delphi_compatability.Screen.Cursor = delphi_compatability.crDefault;
            this.mouseMoveActionInProgress = false;
            this.commandList.rightButtonDown = false;
            this.actionInProgress = false;
        }
    }
    
    public void PaintBoxDragOver(TObject Sender, TObject Source, int X, int Y, TDragState State, boolean Accept) {
        Accept = (Source != null) && (Sender != null) && ((ubreedr.BreederForm != null) && (Source == ubreedr.BreederForm.plantsDrawGrid) || (UNRESOLVED.TimeSeriesForm != null) && (Source == UNRESOLVED.TimeSeriesForm.grid));
        return Accept;
    }
    
    public void PaintBoxEndDrag(TObject Sender, TObject Target, int X, int Y) {
        PdPlant plantClickedOn = new PdPlant();
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if ((Target != null) && (Target instanceof delphi_compatability.TDrawGrid)) {
            plantClickedOn = null;
            plantClickedOn = udomain.domain.plantManager.findPlantAtPoint(this.commandList.anchorPoint);
            if (plantClickedOn != null) {
                if ((((delphi_compatability.TDrawGrid)Target).owner instanceof ubreedr.TBreederForm)) {
                    ubreedr.BreederForm.copyPlantToPoint(plantClickedOn, X, Y);
                } else if ((((delphi_compatability.TDrawGrid)Target).owner instanceof UNRESOLVED.TTimeSeriesForm)) {
                    UNRESOLVED.TimeSeriesForm.copyPlantToPoint(plantClickedOn, X, Y);
                }
            }
            // command undoes itself when it starts the drag 
        }
    }
    
    public PdCommand makeMouseCommand(TPoint point, TShiftState shift) {
        result = new PdCommand();
        result = null;
        switch (this.cursorModeForDrawing) {
            case kCursorModeSelectDrag:
                if ((delphi_compatability.TShiftStateEnum.ssShift in shift) && (delphi_compatability.TShiftStateEnum.ssCtrl in shift)) {
                    result = null;
                    this.commandList.anchorPoint = Point;
                    this.drawingPaintBox.BeginDrag(true);
                } else if ((delphi_compatability.TShiftStateEnum.ssCtrl in shift)) {
                    result = updcom.PdDuplicateCommand().createWithListOfPlants(this.selectedPlants);
                } else if ((this.focusedPlant() != null) && (this.focusedPlant().pointIsInResizingRect(Point))) {
                    delphi_compatability.Screen.Cursor = delphi_compatability.crSizeNS;
                    result = updcom.PdResizePlantsCommand().createWithListOfPlants(this.selectedPlants);
                } else {
                    result = updcom.PdDragCommand().createWithListOfPlants(this.selectedPlants);
                }
                break;
            case kCursorModeScroll:
                result = updcom.PdScrollCommand().create();
                break;
            case kCursorModeMagnify:
                if ((this.commandList.rightButtonDown)) {
                    // to zoom out, can do right button or shift
                    delphi_compatability.Screen.Cursor = UNRESOLVED.crMagMinus;
                    result = updcom.PdChangeMagnificationCommand().create();
                    ((updcom.PdChangeMagnificationCommand)result).shift = true;
                } else {
                    result = updcom.PdChangeMagnificationCommand().create();
                    ((updcom.PdChangeMagnificationCommand)result).shift = (delphi_compatability.TShiftStateEnum.ssShift in shift);
                }
                break;
            case kCursorModeRotate:
                if (this.commandList.rightButtonDown) {
                    delphi_compatability.Screen.Cursor = delphi_compatability.crSizeWE;
                }
                result = updcom.PdRotateCommand().createWithListOfPlants(this.selectedPlants);
                break;
            case kCursorModePosingSelect:
                result = updcom.PdSelectPosingPartCommand().createWithPlantAndPartIDsAndTypes(this.focusedPlant(), this.mouseDownSelectedPlantPartID, this.selectedPlantPartID, this.mouseDownSelectedPlantPartType, this.selectedPlantPartType);
                break;
        return result;
    }
    
    // rubber banding 
    // ----------------------------------------------------------------------- *rubber banding 
    public void selectPlantsInRubberBandBox() {
        TRect rubberBandRect = new TRect();
        TList newList = new TList();
        PdCommand newCommand = new PdCommand();
        
        newList = delphi_compatability.TList().Create();
        try {
            rubberBandRect = Rect(umath.intMin(this.rubberBandStartDragPoint.X, this.rubberBandLastDrawPoint.X), umath.intMin(this.rubberBandStartDragPoint.Y, this.rubberBandLastDrawPoint.Y), umath.intMax(this.rubberBandStartDragPoint.X, this.rubberBandLastDrawPoint.X), umath.intMax(this.rubberBandStartDragPoint.Y, this.rubberBandLastDrawPoint.Y));
            udomain.domain.plantManager.fillListWithPlantsInRectangle(rubberBandRect, newList);
            if (!this.twoListsAreIdentical(this.selectedPlants, newList)) {
                newCommand = updcom.PdChangeSelectedPlantsCommand().createWithOldListOFPlantsAndNewList(this.selectedPlants, newList);
                this.doCommand(newCommand);
            }
        } finally {
            newList.free;
        }
    }
    
    public void drawRubberBandBox(TPoint newPoint) {
        this.rubberBandLastDrawPoint = newPoint;
        this.drawOrUndrawRubberBandBox();
        this.rubberBandNeedToRedraw = true;
    }
    
    public void undrawRubberBandBox() {
        if (!this.rubberBandNeedToRedraw) {
            return;
        }
        this.drawOrUndrawRubberBandBox();
        this.rubberBandNeedToRedraw = false;
    }
    
    public void drawOrUndrawRubberBandBox() {
        HDC theDC = new HDC();
        TRect drawRect = new TRect();
        
        theDC = UNRESOLVED.getDC(0);
        drawRect = Rect(this.clientOrigin.x + this.drawingPaintBox.Left + this.rubberBandStartDragPoint.X, this.clientOrigin.y + this.drawingPaintBox.Top + this.rubberBandStartDragPoint.Y, this.clientOrigin.x + this.drawingPaintBox.Left + this.rubberBandLastDrawPoint.X, this.clientOrigin.y + this.drawingPaintBox.Top + this.rubberBandLastDrawPoint.Y);
        UNRESOLVED.patBlt(theDC, drawRect.Left, drawRect.Top, drawRect.Right - drawRect.Left, 1, delphi_compatability.DSTINVERT);
        UNRESOLVED.patBlt(theDC, drawRect.Right, drawRect.Top, 1, drawRect.Bottom - drawRect.Top, delphi_compatability.DSTINVERT);
        UNRESOLVED.patBlt(theDC, drawRect.Left, drawRect.Bottom, drawRect.Right - drawRect.Left, 1, delphi_compatability.DSTINVERT);
        UNRESOLVED.patBlt(theDC, drawRect.Left, drawRect.Top, 1, drawRect.Bottom - drawRect.Top, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
    }
    
    // hint handling 
    // ------------------------------------------------------------------------------------ *hint handling 
    public void DoShowHint(ansistring HintStr, boolean CanShow, THintInfo HintInfo) {
        raise "method DoShowHint had assigned to var parameter HintStr not added to return; fixup manually"
        HintInfo.HintPos = HintInfo.HintControl.ClientToScreen(Point(HintInfo.CursorPos.X + 20, HintInfo.CursorPos.Y + 20));
        HintInfo.HintMaxWidth = 200;
        if (HintInfo.HintControl == this.drawingPaintBox) {
            if (!this.actionInProgress) {
                HintStr = this.hintForPlantAtPoint(HintInfo.CursorPos);
                this.lastHintString = HintStr;
                this.hintActive = true;
                this.hintX = HintInfo.CursorPos.X;
                this.hintY = HintInfo.CursorPos.Y;
            }
        } else {
            if ((udomain.domain != null) && (udomain.domain.hintManager != null)) {
                HintStr = udomain.domain.hintManager.hintForComponentName(HintInfo, udomain.domain.options.showLongHintsForButtons, udomain.domain.options.showHintsForParameters);
            }
            if ((HintStr == "") && (HintInfo.HintControl.ShowHint)) {
                HintStr = HintInfo.HintControl.Hint;
            }
        }
        return CanShow;
    }
    
    public String hintForPlantAtPoint(TPoint aPoint) {
        result = "";
        PdPlant plant = new PdPlant();
        
        result = "";
        plant = null;
        plant = udomain.domain.plantManager.findPlantAtPoint(aPoint);
        if (plant != null) {
            // v1.60 final
            result = plant.getHint(aPoint);
        }
        if ((this.cursorModeForDrawing == kCursorModeSelectDrag) && (udomain.domain.options.showLongHintsForButtons) && (udomain.domain.options.showSelectionRectangle) && (plant != null) && (plant == this.focusedPlant()) && (plant.pointIsInResizingRect(aPoint))) {
            // extra hint if over resizing rect on focused plant in select/drag mode
            result = result + ": Click here and drag up or down to resize all selected plants.";
        }
        return result;
    }
    
    // -------------------------------------------------------------------------------- *popup menu commands 
    public void PopupMenuCutClick(TObject Sender) {
        this.MenuEditCutClick(this);
    }
    
    public void PopupMenuCopyClick(TObject Sender) {
        this.MenuEditCopyClick(this);
    }
    
    public void PopupMenuPasteClick(TObject Sender) {
        this.MenuEditPasteClick(this);
    }
    
    public void PopupMenuRenameClick(TObject Sender) {
        this.MenuPlantRenameClick(this);
    }
    
    public void PopupMenuRandomizeClick(TObject Sender) {
        this.MenuPlantRandomizeClick(this);
    }
    
    public void PopupMenuHideAllOthersClick(TObject Sender) {
        this.MenuLayoutHideOthersClick(this);
    }
    
    public void PopupMenuBreedClick(TObject Sender) {
        this.MenuPlantBreedClick(this);
    }
    
    public void PopupMenuHideClick(TObject Sender) {
        this.MenuLayoutHideClick(this);
    }
    
    public void PopupMenuShowClick(TObject Sender) {
        this.MenuLayoutShowClick(this);
    }
    
    public void PopupMenuMakeTimeSeriesClick(TObject Sender) {
        this.MenuPlantMakeTimeSeriesClick(this);
    }
    
    public void PopupMenuZeroRotationsClick(TObject Sender) {
        this.MenuPlantZeroRotationsClick(this);
    }
    
    public void PopupMenuAnimateClick(TObject Sender) {
        this.MenuPlantAnimateClick(this);
    }
    
    public void paramPopupMenuExpandAllInSectionClick(TObject Sender) {
        if (this.currentSection() != null) {
            this.collapseOrExpandAllParameterPanelsInCurrentSection(kExpand);
        }
    }
    
    public void paramPopupMenuCollapseAllInSectionClick(TObject Sender) {
        if (this.currentSection() != null) {
            this.collapseOrExpandAllParameterPanelsInCurrentSection(kCollapse);
        }
    }
    
    public void sectionPopupMenuHelpClick(TObject Sender) {
        PdSection section = new PdSection();
        String helpID = "";
        
        section = this.currentSection();
        if (section == null) {
            return;
        }
        helpID = this.sectionHelpIDForSectionName(section.getName());
        if (helpID != "") {
            delphi_compatability.Application.HelpJump(helpID);
        }
    }
    
    // new v1.4
    public void paramPopupMenuCopyNameClick(TObject Sender) {
        String textToCopy = "";
        String newText = "";
        
        if (this.selectedParameterPanel == null) {
            return;
        }
        if (this.currentSection() != null) {
            textToCopy = this.currentSection().getName() + ": ";
        } else {
            textToCopy = "";
        }
        textToCopy = textToCopy + this.selectedParameterPanel.caption;
        if (usupport.found("[", textToCopy)) {
            // v2.1 deal with orthogonal sections
            newText = usupport.stringUpTo(usupport.stringBeyond(textToCopy, "["), "]");
            newText = newText + ": " + trim(usupport.stringUpTo(usupport.stringBeyond(textToCopy, ":"), "["));
            textToCopy = newText;
        }
        UNRESOLVED.Clipboard.asText = textToCopy;
    }
    
    public void paramPopupMenuHelpClick(TObject Sender) {
        String helpID = "";
        
        helpID = this.paramHelpIDForParamPanel(this.selectedParameterPanel);
        if (helpID != "") {
            delphi_compatability.Application.HelpJump(helpID);
        }
    }
    
    public void paramPopupMenuExpandClick(TObject Sender) {
        if (this.selectedParameterPanel != null) {
            this.selectedParameterPanel.expand;
            this.repositionParameterPanels();
        }
    }
    
    public void paramPopupMenuCollapseClick(TObject Sender) {
        if (this.selectedParameterPanel != null) {
            this.selectedParameterPanel.collapse;
            this.repositionParameterPanels();
        }
    }
    
    // ------------------------------------------------------------------------------------ *toolbar 
    public void dragCursorModeClick(TObject Sender) {
        this.drawingPaintBox.Cursor = delphi_compatability.crArrow;
        this.cursorModeForDrawing = kCursorModeSelectDrag;
        if (udomain.domain.options.showSelectionRectangle) {
            this.copyDrawingBitmapToPaintBox();
        }
    }
    
    public void magnifyCursorModeClick(TObject Sender) {
        this.drawingPaintBox.Cursor = UNRESOLVED.crMagPlus;
        this.cursorModeForDrawing = kCursorModeMagnify;
        if (udomain.domain.options.showSelectionRectangle) {
            this.copyDrawingBitmapToPaintBox();
        }
    }
    
    public void posingSelectionCursorModeClick(TObject Sender) {
        this.tabSet.tabIndex = kTabPosing;
        this.drawingPaintBox.Cursor = UNRESOLVED.crPosingSelect;
        this.cursorModeForDrawing = kCursorModePosingSelect;
        if (udomain.domain.options.showSelectionRectangle) {
            this.copyDrawingBitmapToPaintBox();
        }
    }
    
    public void scrollCursorModeClick(TObject Sender) {
        this.drawingPaintBox.Cursor = UNRESOLVED.crScroll;
        this.cursorModeForDrawing = kCursorModeScroll;
        if (udomain.domain.options.showSelectionRectangle) {
            this.copyDrawingBitmapToPaintBox();
        }
    }
    
    public void rotateCursorModeClick(TObject Sender) {
        this.drawingPaintBox.Cursor = UNRESOLVED.crRotate;
        this.cursorModeForDrawing = kCursorModeRotate;
        if (udomain.domain.options.showSelectionRectangle) {
            this.copyDrawingBitmapToPaintBox();
        }
    }
    
    public void centerDrawingClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = updcom.PdCenterDrawingCommand().create();
        this.doCommand(newCommand);
    }
    
    public void magnificationPercentClick(TObject Sender) {
        float newScale = 0.0;
        
        newScale = this.magnifyScaleForText(this.magnificationPercent.Text);
        if ((newScale != udomain.domain.plantDrawScale_PixelsPerMm())) {
            this.changeMagnificationWithoutClick();
        }
    }
    
    public void magnificationPercentExit(TObject Sender) {
        float newScale = 0.0;
        
        newScale = this.magnifyScaleForText(this.magnificationPercent.Text);
        if ((newScale != udomain.domain.plantDrawScale_PixelsPerMm())) {
            this.changeMagnificationWithoutClick();
        }
    }
    
    public void magnifyPlusClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = updcom.PdChangeMagnificationCommand().createWithNewScaleAndPoint(udomain.domain.plantDrawScale_PixelsPerMm() * 1.5, Point(this.drawingPaintBox.Width / 2, this.drawingPaintBox.Height / 2));
        this.doCommand(newCommand);
    }
    
    public void magnifyMinusClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        newCommand = updcom.PdChangeMagnificationCommand().createWithNewScaleAndPoint(udomain.domain.plantDrawScale_PixelsPerMm() * 0.75, Point(this.drawingPaintBox.Width / 2, this.drawingPaintBox.Height / 2));
        this.doCommand(newCommand);
    }
    
    // popup menu commands 
    // toolbar 
    public void changeMagnificationWithoutClick() {
        PdCommand newCommand = new PdCommand();
        
        newCommand = updcom.PdChangeMagnificationCommand().createWithNewScaleAndPoint(this.magnifyScaleForText(this.magnificationPercent.Text), Point(this.drawingPaintBox.Width / 2, this.drawingPaintBox.Height / 2));
        this.doCommand(newCommand);
    }
    
    public float magnifyScaleForText(String aText) {
        result = 0.0;
        int intResult = 0;
        int oldIntResult = 0;
        
        result = 1.0;
        try {
            oldIntResult = intround(udomain.domain.plantDrawScale_PixelsPerMm() * 100.0);
            intResult = StrToIntDef(usupport.stringUpTo(aText, "%"), -1);
            if ((intResult <= 0)) {
                intResult = oldIntResult;
                this.magnificationPercent.Text = IntToStr(intResult) + "%";
            }
            if (intResult > kMaxMagnificationToTypeIn) {
                intResult = kMaxMagnificationToTypeIn;
                this.magnificationPercent.Text = IntToStr(intResult) + "%";
            }
            result = intResult / 100.0;
        } catch (Exception e) {
            result = 1.0;
        }
        return result;
    }
    
    public TPoint magnifyOrReduce(float newScale_PixelsPerMm, TPoint point_pixels, boolean drawNow) {
        result = new TPoint();
        SinglePoint oldOffset_mm = new SinglePoint();
        SinglePoint pointInOldScale_mm = new SinglePoint();
        SinglePoint pointInNewScale_mm = new SinglePoint();
        SinglePoint newOffset_mm = new SinglePoint();
        float oldScale_PixelsPerMm = 0.0;
        
        this.recalculateAllPlantBoundsRects(kDontDrawYet);
        oldScale_PixelsPerMm = udomain.domain.plantDrawScale_PixelsPerMm();
        oldOffset_mm = udomain.domain.plantDrawOffset_mm();
        pointInOldScale_mm = usupport.setSinglePoint(intround(point_pixels.X / oldScale_PixelsPerMm), intround(point_pixels.Y / oldScale_PixelsPerMm));
        pointInNewScale_mm = usupport.setSinglePoint(intround(point_pixels.X / newScale_PixelsPerMm), intround(point_pixels.Y / newScale_PixelsPerMm));
        newOffset_mm = usupport.setSinglePoint(oldOffset_mm.x + pointInNewScale_mm.x - pointInOldScale_mm.x, oldOffset_mm.y + pointInNewScale_mm.y - pointInOldScale_mm.y);
        udomain.domain.plantManager.plantDrawScale_PixelsPerMm = intround(newScale_PixelsPerMm * 100.0) / 100.0;
        udomain.domain.plantManager.plantDrawOffset_mm = newOffset_mm;
        if (drawNow) {
            this.redrawEverything();
        }
        this.magnificationPercent.Text = IntToStr(intround(udomain.domain.plantDrawScale_PixelsPerMm() * 100.0)) + "%";
        return result;
    }
    
    public TPoint upperLeftMostPlantBoundsRectPoint_mm() {
        result = new TPoint();
        PdPlant plant = new PdPlant();
        short i = 0;
        TPoint topLeft_mm = new TPoint();
        boolean initialized = false;
        
        result = Point(0, 0);
        initialized = false;
        if (this.plants.Count > 0) {
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (plant.hidden) {
                    continue;
                }
                topLeft_mm.X = intround(plant.boundsRect_pixels().Left / udomain.domain.plantDrawScale_PixelsPerMm() - udomain.domain.plantDrawOffset_mm().x);
                topLeft_mm.Y = intround(plant.boundsRect_pixels().Top / udomain.domain.plantDrawScale_PixelsPerMm() - udomain.domain.plantDrawOffset_mm().y);
                if (!initialized) {
                    result = topLeft_mm;
                    initialized = true;
                } else {
                    if ((topLeft_mm.X < result.X)) {
                        result.X = topLeft_mm.X;
                    }
                    if ((topLeft_mm.Y < result.Y)) {
                        result.Y = topLeft_mm.Y;
                    }
                }
            }
        }
        return result;
    }
    
    public TPoint lowerRightMostPlantBoundsRectPoint_mm() {
        result = new TPoint();
        PdPlant plant = new PdPlant();
        short i = 0;
        TPoint bottomRight_mm = new TPoint();
        boolean initialized = false;
        
        result = Point(0, 0);
        initialized = false;
        if (this.plants.Count > 0) {
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if (plant.hidden) {
                    continue;
                }
                bottomRight_mm.X = intround(plant.boundsRect_pixels().Right / udomain.domain.plantDrawScale_PixelsPerMm() - udomain.domain.plantDrawOffset_mm().x);
                bottomRight_mm.Y = intround(plant.boundsRect_pixels().Bottom / udomain.domain.plantDrawScale_PixelsPerMm() - udomain.domain.plantDrawOffset_mm().y);
                if (!initialized) {
                    result = bottomRight_mm;
                    initialized = true;
                } else {
                    if ((bottomRight_mm.X > result.X)) {
                        result.X = bottomRight_mm.X;
                    }
                    if ((bottomRight_mm.Y > result.Y)) {
                        result.Y = bottomRight_mm.Y;
                    }
                }
            }
        }
        return result;
    }
    
    public void xLocationEditExit(TObject Sender) {
        int increment = 0;
        int oldXLocation = 0;
        int newXLocation = 0;
        short direction = 0;
        
        if (this.focusedPlant() == null) {
            return;
        }
        oldXLocation = this.focusedPlant().basePoint_pixels().X;
        newXLocation = StrToIntDef(this.xLocationEdit.Text, oldXLocation);
        if (newXLocation != oldXLocation) {
            increment = newXLocation - oldXLocation;
            if (increment > 0) {
                direction = updcom.kRight;
            } else {
                direction = updcom.kLeft;
            }
            this.nudgeSelectedPlantsByPixelsAndDirection(increment, direction);
        }
    }
    
    public void yLocationEditExit(TObject Sender) {
        int increment = 0;
        int oldYLocation = 0;
        int newYLocation = 0;
        short direction = 0;
        
        if (this.focusedPlant() == null) {
            return;
        }
        oldYLocation = this.focusedPlant().basePoint_pixels().Y;
        newYLocation = StrToIntDef(this.yLocationEdit.Text, oldYLocation);
        if (newYLocation != oldYLocation) {
            increment = newYLocation - oldYLocation;
            if (increment > 0) {
                direction = updcom.kDown;
            } else {
                direction = updcom.kUp;
            }
            this.nudgeSelectedPlantsByPixelsAndDirection(increment, direction);
        }
    }
    
    public void xLocationSpinDownClick(TObject Sender) {
        this.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, updcom.kLeft);
    }
    
    public void xLocationSpinUpClick(TObject Sender) {
        this.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, updcom.kRight);
    }
    
    public void yLocationSpinDownClick(TObject Sender) {
        this.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, updcom.kUp);
    }
    
    public void yLocationSpinUpClick(TObject Sender) {
        this.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, updcom.kDown);
    }
    
    public void xRotationEditChange(TObject Sender) {
        this.checkRotationEditAgainstBounds(this.xRotationEdit);
    }
    
    public void yRotationEditChange(TObject Sender) {
        this.checkRotationEditAgainstBounds(this.yRotationEdit);
    }
    
    public void zRotationEditChange(TObject Sender) {
        this.checkRotationEditAgainstBounds(this.zRotationEdit);
    }
    
    public void checkRotationEditAgainstBounds(TEdit edit) {
        short newRotation = 0;
        short oldRotation = 0;
        
        if (this.internalChange) {
            return;
        }
        newRotation = StrToIntDef(edit.Text, 0);
        oldRotation = newRotation;
        if (newRotation < -360) {
            newRotation = 360 - (abs(newRotation) - 360);
        }
        if (newRotation > 360) {
            newRotation = -360 + (newRotation - 360);
        }
        if (newRotation != oldRotation) {
            this.internalChange = true;
            edit.Text = IntToStr(newRotation);
            this.internalChange = false;
        }
    }
    
    public void xRotationEditExit(TObject Sender) {
        this.changeSelectedPlantRotations(this.xRotationEdit, updcom.kRotateX, 0);
    }
    
    public void xRotationSpinUpClick(TObject Sender) {
        this.changeSelectedPlantRotations(this.xRotationEdit, updcom.kRotateX, udomain.domain.options.rotationIncrement);
    }
    
    public void xRotationSpinDownClick(TObject Sender) {
        this.changeSelectedPlantRotations(this.xRotationEdit, updcom.kRotateX, -udomain.domain.options.rotationIncrement);
    }
    
    public void yRotationEditExit(TObject Sender) {
        this.changeSelectedPlantRotations(this.yRotationEdit, updcom.kRotateY, 0);
    }
    
    public void yRotationSpinUpClick(TObject Sender) {
        this.changeSelectedPlantRotations(this.yRotationEdit, updcom.kRotateY, udomain.domain.options.rotationIncrement);
    }
    
    public void yRotationSpinDownClick(TObject Sender) {
        this.changeSelectedPlantRotations(this.yRotationEdit, updcom.kRotateY, -udomain.domain.options.rotationIncrement);
    }
    
    public void zRotationEditExit(TObject Sender) {
        this.changeSelectedPlantRotations(this.zRotationEdit, updcom.kRotateZ, 0);
    }
    
    public void zRotationSpinUpClick(TObject Sender) {
        this.changeSelectedPlantRotations(this.zRotationEdit, updcom.kRotateZ, udomain.domain.options.rotationIncrement);
    }
    
    public void zRotationSpinDownClick(TObject Sender) {
        this.changeSelectedPlantRotations(this.zRotationEdit, updcom.kRotateZ, -udomain.domain.options.rotationIncrement);
    }
    
    public void changeSelectedPlantRotations(TEdit edit, short rotateDirection, short changeInRotation) {
        short newRotation = 0;
        PdCommand newCommand = new PdCommand();
        
        if (this.internalChange) {
            return;
        }
        newRotation = StrToIntDef(edit.Text, 0) + changeInRotation;
        edit.Text = IntToStr(newRotation);
        // need this? 
        this.checkRotationEditAgainstBounds(edit);
        // in case changed 
        newRotation = StrToIntDef(edit.Text, 0);
        if (this.focusedPlant() == null) {
            //should be disabled, but
            return;
        }
        newCommand = updcom.PdRotateCommand().createWithListOfPlantsDirectionAndNewRotation(this.selectedPlants, rotateDirection, newRotation);
        this.doCommand(newCommand);
    }
    
    public void resetRotationsClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        short i = 0;
        PdPlant plant = new PdPlant();
        boolean allRotationsAreZero = false;
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        // don't do if none of the selected plants have rotations other than zero 
        allRotationsAreZero = true;
        for (i = 0; i <= this.selectedPlants.Count - 1; i++) {
            plant = uplant.PdPlant(this.selectedPlants.Items[i]);
            if ((plant.xRotation != 0) || (plant.yRotation != 0) || (plant.zRotation != 0)) {
                allRotationsAreZero = false;
                break;
            }
        }
        if (allRotationsAreZero) {
            return;
        }
        newCommand = updcom.PdResetRotationsCommand().createWithListOfPlants(this.selectedPlants);
        this.doCommand(newCommand);
    }
    
    public void drawingScaleEditExit(TObject Sender) {
        float oldValue = 0.0;
        float newValue = 0.0;
        
        if (this.focusedPlant() == null) {
            return;
        }
        oldValue = this.focusedPlant().drawingScale_PixelsPerMm;
        try {
            newValue = StrToFloat(this.drawingScaleEdit.Text);
        } catch (Exception e) {
            newValue = oldValue;
        }
        if (newValue != oldValue) {
            this.resizeSelectedPlantsWithMultiplierOrNewAmount(0, newValue);
        }
    }
    
    public void drawingScaleSpinUpClick(TObject Sender) {
        float resizeMultiplier = 0.0;
        
        if (this.focusedPlant() == null) {
            return;
        }
        resizeMultiplier = udomain.domain.options.resizeKeyUpMultiplierPercent / 100.0;
        this.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0);
    }
    
    public void drawingScaleSpinDownClick(TObject Sender) {
        float resizeMultiplier = 0.0;
        
        if (this.focusedPlant() == null) {
            return;
        }
        resizeMultiplier = umath.safedivExcept(1.0, udomain.domain.options.resizeKeyUpMultiplierPercent / 100.0, 0.9);
        this.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0);
    }
    
    public void makeEqualWidthClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdResizePlantsToSameWidthOrHeightCommand().createWithListOfPlantsAndNewWidthOrHeight(this.selectedPlants, usupport.rWidth(this.focusedPlant().boundsRect_pixels()), 0, updcom.kChangeWidth);
        this.doCommand(newCommand);
    }
    
    public void makeEqualHeightClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdResizePlantsToSameWidthOrHeightCommand().createWithListOfPlantsAndNewWidthOrHeight(this.selectedPlants, 0, usupport.rHeight(this.focusedPlant().boundsRect_pixels()), updcom.kChangeHeight);
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutSizeSameWidthClick(TObject Sender) {
        this.makeEqualWidthClick(this);
    }
    
    public void MenuLayoutSizeSameHeightClick(TObject Sender) {
        this.makeEqualHeightClick(this);
    }
    
    public void alignTopsClick(TObject Sender) {
        this.alignSelectedPlants(updcom.kUp);
    }
    
    public void alignBottomsClick(TObject Sender) {
        this.alignSelectedPlants(updcom.kDown);
    }
    
    public void alignLeftClick(TObject Sender) {
        this.alignSelectedPlants(updcom.kLeft);
    }
    
    public void alignRightClick(TObject Sender) {
        this.alignSelectedPlants(updcom.kRight);
    }
    
    public void alignSelectedPlants(short alignDirection) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 1) {
            return;
        }
        newCommand = updcom.PdAlignPlantsCommand().createWithListOfPlantsRectAndDirection(this.selectedPlants, this.focusedPlant().boundsRect_pixels(), alignDirection);
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutAlignTopsClick(TObject Sender) {
        this.alignTopsClick(this);
    }
    
    public void MenuLayoutAlignBottomsClick(TObject Sender) {
        this.alignBottomsClick(this);
    }
    
    public void MenuLayoutAlignLeftSidesClick(TObject Sender) {
        this.alignLeftClick(this);
    }
    
    public void MenuLayoutAlignRightSidesClick(TObject Sender) {
        this.alignRightClick(this);
    }
    
    public void packPlantsClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 1) {
            return;
        }
        newCommand = updcom.PdPackPlantsCommand().createWithListOfPlantsAndFocusRect(this.selectedPlants, this.focusedPlant().boundsRect_pixels());
        this.doCommand(newCommand);
    }
    
    public void MenuLayoutPackClick(TObject Sender) {
        this.packPlantsClick(this);
    }
    
    public void FormKeyDown(TObject Sender, byte Key, TShiftState Shift) {
        if (this.animateTimer.enabled) {
            // pressing any key will stop animation 
            Key = 0;
            this.stopAnimation();
        }
        if ((delphi_compatability.TShiftStateEnum.ssCtrl in Shift) && (delphi_compatability.TShiftStateEnum.ssShift in Shift)) {
            if ((Key == delphi_compatability.VK_LEFT) || (Key == delphi_compatability.VK_RIGHT) || (Key == delphi_compatability.VK_UP) || (Key == delphi_compatability.VK_DOWN)) {
                // hold down control and shift and press arrow keys - resize current plants 
                this.resizeSelectedPlantsByKey(Key);
                Key = 0;
            }
            // hold down control and press arrow keys - shift current plants 
        } else if ((delphi_compatability.TShiftStateEnum.ssCtrl in Shift)) {
            if ((Key == delphi_compatability.VK_LEFT) || (Key == delphi_compatability.VK_RIGHT) || (Key == delphi_compatability.VK_UP) || (Key == delphi_compatability.VK_DOWN)) {
                this.nudgeSelectedPlantsByKey(Key);
                Key = 0;
            }
            // hold down shift - do magnification as minus 
        } else if ((Key == delphi_compatability.VK_SHIFT)) {
            if (this.cursorModeForDrawing == kCursorModeMagnify) {
                this.drawingPaintBox.Cursor = UNRESOLVED.crMagMinus;
            }
        }
        return Key;
    }
    
    public void nudgeSelectedPlantsByKey(byte key) {
        short direction = 0;
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        switch (key) {
            case delphi_compatability.VK_LEFT:
                direction = updcom.kLeft;
                break;
            case delphi_compatability.VK_RIGHT:
                direction = updcom.kRight;
                break;
            case delphi_compatability.VK_UP:
                direction = updcom.kUp;
                break;
            case delphi_compatability.VK_DOWN:
                direction = updcom.kDown;
                break;
            default:
                return;
                break;
        this.nudgeSelectedPlantsByPixelsAndDirection(udomain.domain.options.nudgeDistance, direction);
    }
    
    public void nudgeSelectedPlantsByPixelsAndDirection(int pixels, short direction) {
        PdCommand newCommand = new PdCommand();
        TPoint movePoint = new TPoint();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        movePoint = Point(0, 0);
        switch (direction) {
            case updcom.kUp:
                movePoint.Y = -pixels;
                break;
            case updcom.kDown:
                movePoint.Y = pixels;
                break;
            case updcom.kLeft:
                movePoint.X = -pixels;
                break;
            case updcom.kRight:
                movePoint.X = pixels;
                break;
        newCommand = updcom.PdDragCommand().createWithListOfPlantsAndDragOffset(this.selectedPlants, movePoint);
        this.doCommand(newCommand);
    }
    
    public void resizeSelectedPlantsByKey(byte key) {
        float resizeMultiplier = 0.0;
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        if ((key == delphi_compatability.VK_LEFT) || (key == delphi_compatability.VK_UP)) {
            resizeMultiplier = udomain.domain.options.resizeKeyUpMultiplierPercent / 100.0;
        } else if ((key == delphi_compatability.VK_RIGHT) || (key == delphi_compatability.VK_DOWN)) {
            resizeMultiplier = umath.safedivExcept(1.0, udomain.domain.options.resizeKeyUpMultiplierPercent / 100.0, 0.9);
        } else {
            return;
        }
        this.resizeSelectedPlantsWithMultiplierOrNewAmount(resizeMultiplier, 0);
    }
    
    public void resizeSelectedPlantsWithMultiplierOrNewAmount(float multiplier, float newAmount_pixelsPerMm) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        if (multiplier != 0) {
            newCommand = updcom.PdResizePlantsCommand().createWithListOfPlantsAndMultiplier(this.selectedPlants, multiplier);
        } else {
            newCommand = updcom.PdResizePlantsCommand().createWithListOfPlantsAndNewValue(this.selectedPlants, newAmount_pixelsPerMm);
        }
        this.doCommand(newCommand);
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        Key = usupport.makeEnterWorkAsTab(this, UNRESOLVED.activeControl, Key);
        if (this.animateTimer.enabled) {
            // pressing any key will stop animation 
            Key = chr(0);
            this.stopAnimation();
        }
        return Key;
    }
    
    public void FormKeyUp(TObject Sender, byte Key, TShiftState Shift) {
        if (this.animateTimer.enabled) {
            // pressing any key will stop animation 
            Key = 0;
            this.stopAnimation();
        }
        if ((Key == delphi_compatability.VK_SHIFT)) {
            if (this.cursorModeForDrawing == kCursorModeMagnify) {
                // let up shift or control - go back to plus magnification 
                this.drawingPaintBox.Cursor = UNRESOLVED.crMagPlus;
            }
        }
        return Key;
    }
    
    // tab set 
    // ------------------------------------------------------------------------------------ *tab set 
    public boolean lifeCycleShowing() {
        result = false;
        result = (this.tabSet.tabIndex == kTabLifeCycle);
        return result;
    }
    
    public boolean rotationsShowing() {
        result = false;
        result = (this.tabSet.tabIndex == kTabRotations);
        return result;
    }
    
    public boolean parametersShowing() {
        result = false;
        result = (this.tabSet.tabIndex == kTabParameters);
        return result;
    }
    
    public boolean statsShowing() {
        result = false;
        result = (this.tabSet.tabIndex == kTabStatistics);
        return result;
    }
    
    public boolean noteShowing() {
        result = false;
        result = (this.tabSet.tabIndex == kTabNote);
        return result;
    }
    
    public boolean posingShowing() {
        result = false;
        result = (this.tabSet.tabIndex == kTabPosing);
        return result;
    }
    
    public void tabSetChange(TObject Sender, int NewTab, boolean AllowChange) {
        this.lifeCyclePanel.Visible = (NewTab == kTabLifeCycle);
        this.rotationsPanel.Visible = (NewTab == kTabRotations);
        this.parametersPanel.Visible = (NewTab == kTabParameters);
        this.statsScrollBox.Visible = (NewTab == kTabStatistics);
        this.notePanel.Visible = (NewTab == kTabNote);
        this.posingPanel.Visible = (NewTab == kTabPosing);
        this.updateRightSidePanelForFirstSelectedPlantWithTab(NewTab);
        return AllowChange;
    }
    
    public void updateRightSidePanelForFirstSelectedPlant() {
        // set tab font colors - pay attention to multiple selections 
        // v2.0 removed this
        //  tabSet.font.color := self.textColorToRepresentPlantSelection(true);
        //  tabSet.invalidate;
        this.updateRightSidePanelForFirstSelectedPlantWithTab(this.tabSet.tabIndex);
    }
    
    public void updateRightSidePanelForFirstSelectedPlantWithTab(int newTab) {
        switch (newTab) {
            case kTabLifeCycle:
                this.updateLifeCyclePanelForFirstSelectedPlant();
                break;
            case kTabRotations:
                this.updateRotationsPanelForFirstSelectedPlant();
                break;
            case kTabParameters:
                this.updateParametersPanelForFirstSelectedPlant();
                break;
            case kTabStatistics:
                this.updateStatisticsPanelForFirstSelectedPlant();
                break;
            case kTabNote:
                this.updateNoteForFirstSelectedPlant();
                break;
            case kTabPosing:
                this.updatePosingForFirstSelectedPlant();
                break;
    }
    
    public TColorRef textColorToRepresentPlantSelection(boolean payAttentionToMultiSelect) {
        result = new TColorRef();
        if (this.focusedPlant() != null) {
            if (payAttentionToMultiSelect) {
                if (this.selectedPlants.Count <= 1) {
                    result = UNRESOLVED.clBtnText;
                } else {
                    // v2.0  was clRed
                    result = delphi_compatability.clBlue;
                }
            } else {
                result = UNRESOLVED.clBtnText;
            }
        } else {
            result = delphi_compatability.clGray;
        }
        return result;
    }
    
    public void updateForChangeToPlantRotations() {
        PdPlant firstPlant = new PdPlant();
        
        firstPlant = this.focusedPlant();
        if (firstPlant != null) {
            this.xRotationEdit.Text = IntToStr(intround(firstPlant.xRotation));
            this.yRotationEdit.Text = IntToStr(intround(firstPlant.yRotation));
            this.zRotationEdit.Text = IntToStr(intround(firstPlant.zRotation));
        } else {
            this.xRotationEdit.Text = "";
            this.yRotationEdit.Text = "";
            this.zRotationEdit.Text = "";
        }
        this.xRotationEdit.Refresh();
        this.yRotationEdit.Refresh();
        this.zRotationEdit.Refresh();
    }
    
    public void updateForChangeToSelectedPlantsDrawingScale() {
        PdPlant firstPlant = new PdPlant();
        
        firstPlant = this.focusedPlant();
        if (firstPlant != null) {
            this.drawingScaleEdit.Text = usupport.digitValueString(firstPlant.drawingScale_PixelsPerMm);
        } else {
            this.drawingScaleEdit.Text = "";
        }
        this.drawingScaleEdit.Refresh();
    }
    
    public void updateForChangeToSelectedPlantsLocation() {
        PdPlant firstPlant = new PdPlant();
        
        firstPlant = this.focusedPlant();
        if (firstPlant != null) {
            this.xLocationEdit.Text = usupport.digitValueString(firstPlant.basePoint_pixels().X);
            this.yLocationEdit.Text = usupport.digitValueString(firstPlant.basePoint_pixels().Y);
        } else {
            this.xLocationEdit.Text = "";
            this.yLocationEdit.Text = "";
        }
        this.xLocationEdit.Refresh();
        this.yLocationEdit.Refresh();
    }
    
    // ------------------------------------------------------- *life cycle panel drawing and mouse handling 
    public void updateLifeCyclePanelForFirstSelectedPlant() {
        PdPlant firstPlant = new PdPlant();
        
        this.updatePlantNameLabel(kTabLifeCycle);
        firstPlant = this.focusedPlant();
        this.lifeCycleDaysEdit.Enabled = firstPlant != null;
        this.lifeCycleDaysSpin.Enabled = firstPlant != null;
        this.lifeCycleDragger.Enabled = firstPlant != null;
        this.animateGrowth.Enabled = firstPlant != null;
        this.timeLabel.Font.Color = this.textColorToRepresentPlantSelection(false);
        this.maxSizeAxisLabel.Font.Color = this.timeLabel.Font.Color;
        this.ageAndSizeLabel.Font.Color = this.timeLabel.Font.Color;
        this.daysAndSizeLabel.Font.Color = this.timeLabel.Font.Color;
        if (firstPlant != null) {
            //special case
            this.lifeCycleDragger.Color = delphi_compatability.clRed;
        } else {
            this.lifeCycleDragger.Color = delphi_compatability.clGray;
        }
        // reset red dragger panel 
        this.placeLifeCycleDragger();
        if (firstPlant != null) {
            // set life cycle days in edit 
            this.lifeCycleDaysEdit.Text = IntToStr(firstPlant.age);
        } else {
            this.lifeCycleDaysEdit.Text = "0";
        }
        if (firstPlant != null) {
            // set % size label
            this.daysAndSizeLabel.Caption = "days, " + IntToStr(intround(firstPlant.totalBiomass_pctMPB)) + "% max size";
        } else {
            this.daysAndSizeLabel.Caption = "";
        }
        this.placeLifeCycleDragger();
        this.redrawLifeCycleGraph();
    }
    
    public void updatePlantNameLabel(short tabIndex) {
        PdPlant firstPlant = new PdPlant();
        TLabel labelToChange = new TLabel();
        boolean payAttentionToOtherPlants = false;
        String prefix = "";
        boolean handlingDifferently = false;
        
        firstPlant = this.focusedPlant();
        payAttentionToOtherPlants = true;
        handlingDifferently = false;
        prefix = "";
        labelToChange = null;
        switch (tabIndex) {
            case kTabRotations:
                labelToChange = this.arrangementPlantName;
                prefix = "Arrangement for ";
                break;
            case kTabParameters:
                labelToChange = this.parametersPlantName;
                prefix = "Parameters for ";
                break;
            case kTabLifeCycle:
                labelToChange = this.selectedPlantNameLabel;
                prefix = "Life cycle for ";
                break;
            case kTabPosing:
                labelToChange = this.posingPlantName;
                payAttentionToOtherPlants = false;
                prefix = "Posing for ";
                break;
            case kTabStatistics:
                handlingDifferently = true;
                this.statsPanel.updatePlant(firstPlant);
                break;
            case kTabNote:
                labelToChange = this.noteLabel;
                payAttentionToOtherPlants = false;
                prefix = "Note for ";
                break;
        if ((handlingDifferently) || (labelToChange == null)) {
            return;
        }
        if (firstPlant != null) {
            labelToChange.Caption = prefix + firstPlant.getName();
            if ((payAttentionToOtherPlants) && (this.selectedPlants.Count > 1)) {
                labelToChange.Caption = labelToChange.Caption + " (and other plants)";
            }
        } else {
            labelToChange.Caption = "(no plants selected)";
        }
        labelToChange.Font.Color = this.textColorToRepresentPlantSelection(payAttentionToOtherPlants);
    }
    
    public void animateGrowthClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdAnimatePlantCommand().createWithListOfPlants(this.selectedPlants);
        this.doCommand(newCommand);
    }
    
    public void MenuPlantAnimateClick(TObject Sender) {
        this.animateGrowthClick(this);
    }
    
    // animation 
    public void startAnimation() {
        // called by animate command, which also sets up the pointer for the timer to call 
        // disable all non-modal forms 
        // keeps space bar from affecting magnification
        this.activeControl = this.plantListDrawGrid;
        this.enableOrDisableAllForms(kDisableAllForms);
        // add warning about disabled forms 
        this.animatingLabel.Visible = true;
        this.tabSet.visible = false;
        // start timer 
        this.animateTimer.enabled = true;
    }
    
    public void animateTimerTimer(TObject Sender) {
        if (this.animateCommand != null) {
            updcom.PdAnimatePlantCommand(this.animateCommand).animateOneDay();
        }
    }
    
    public void stopAnimation() {
        // called by animate command or self (if user clicks in drawing area or presses a key) 
        // stop timer 
        this.animateTimer.enabled = false;
        // nil out pointer 
        this.animateCommand = null;
        // re-enable everything 
        this.enableOrDisableAllForms(kEnableAllForms);
        // remove warning about disabled forms 
        this.animatingLabel.Visible = false;
        this.tabSet.visible = true;
        if (udomain.domain.options.showSelectionRectangle) {
            // if there were selection rectangles before, put them back 
            this.copyDrawingBitmapToPaintBox();
        }
    }
    
    public void enableOrDisableAllForms(boolean enable) {
        // cfk note: put any new NON-MODAL forms here 
        this.enabled = enable;
        ubreedr.BreederForm.enabled = enable;
        UNRESOLVED.TimeSeriesForm.enabled = enable;
        UNRESOLVED.DebugForm.enabled = enable;
    }
    
    public void lifeCycleDaysEditExit(TObject Sender) {
        short newAge = 0;
        PdPlant plant = new PdPlant();
        
        plant = this.focusedPlant();
        if (plant == null) {
            return;
        }
        newAge = StrToIntDef(this.lifeCycleDaysEdit.Text, 0);
        if (newAge == plant.age) {
            return;
        }
        if (newAge > plant.pGeneral.ageAtMaturity) {
            newAge = this.focusedPlant().pGeneral.ageAtMaturity;
            this.lifeCycleDaysEdit.Text = IntToStr(newAge);
        }
        this.changeSelectedPlantAges(newAge);
    }
    
    public void lifeCycleDaysSpinUpClick(TObject Sender) {
        short newAge = 0;
        
        if (this.focusedPlant() == null) {
            return;
        }
        newAge = umath.intMin(StrToIntDef(this.lifeCycleDaysEdit.Text, 0) + 1, this.focusedPlant().pGeneral.ageAtMaturity);
        newAge = umath.intMax(0, newAge);
        this.lifeCycleDaysEdit.Text = IntToStr(newAge);
        this.changeSelectedPlantAges(newAge);
    }
    
    public void lifeCycleDaysSpinDownClick(TObject Sender) {
        short newAge = 0;
        
        if (this.focusedPlant() == null) {
            return;
        }
        newAge = umath.intMin(StrToIntDef(this.lifeCycleDaysEdit.Text, 0) - 1, this.focusedPlant().pGeneral.ageAtMaturity);
        newAge = umath.intMax(0, newAge);
        this.lifeCycleDaysEdit.Text = IntToStr(newAge);
        this.changeSelectedPlantAges(newAge);
    }
    
    public void lifeCycleDraggerMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        if (this.focusedPlant() != null) {
            this.lifeCycleDragging = true;
            this.lifeCycleDraggingStartPos = X;
            this.lifeCycleDraggingLastDrawPos = -1;
            this.lifeCycleDraggingNeedToRedraw = true;
        }
    }
    
    public void lifeCycleDraggerMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        if (this.lifeCycleDragging && (this.lifeCycleDragger.Left + X >= this.lifeCycleGraphImage.Left) && (this.lifeCycleDragger.Left + X < this.lifeCycleGraphImage.Left + this.lifeCycleGraphImage.Width)) {
            this.undrawLifeCycleDraggerLine();
            this.lifeCycleDraggingLastDrawPos = this.drawLifeCycleDraggerLine(X);
        }
    }
    
    public void lifeCycleDraggerMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        PdPlant firstPlant = new PdPlant();
        short newAge = 0;
        
        if (this.lifeCycleDragging) {
            this.undrawLifeCycleDraggerLine();
            this.lifeCycleDragger.Left = this.lifeCycleDragger.Left - (this.lifeCycleDraggingStartPos - X);
            if (this.lifeCycleDragger.Left < this.lifeCycleGraphImage.Left) {
                this.lifeCycleDragger.Left = this.lifeCycleGraphImage.Left;
            }
            if (this.lifeCycleDragger.Left + this.lifeCycleDragger.Width > this.lifeCycleGraphImage.Left + this.lifeCycleGraphImage.Width) {
                this.lifeCycleDragger.Left = this.lifeCycleGraphImage.Left + this.lifeCycleGraphImage.Width - this.lifeCycleDragger.Width;
            }
            firstPlant = this.focusedPlant();
            if (firstPlant == null) {
                throw new GeneralException.create("Problem: First plant is nil during drag in method TMainForm.lifeCycleDraggerMouseUp.");
            }
            if ((this.lifeCycleGraphImage.Width - this.lifeCycleDragger.Width) != 0) {
                newAge = intround(firstPlant.pGeneral.ageAtMaturity * (this.lifeCycleDragger.Left - this.lifeCycleGraphImage.Left) / (this.lifeCycleGraphImage.Width - this.lifeCycleDragger.Width));
            } else {
                newAge = 0;
            }
            this.changeSelectedPlantAges(newAge);
            this.resizePanelsToVerticalSplitter();
            this.lifeCycleDragging = false;
        }
    }
    
    public int drawLifeCycleDraggerLine(int pos) {
        result = 0;
        HDC theDC = new HDC();
        
        theDC = UNRESOLVED.getDC(0);
        result = this.clientOrigin.x + this.plantFocusPanel.Left + this.lifeCyclePanel.Left + this.lifeCycleDragger.Left + pos + 2;
        UNRESOLVED.patBlt(theDC, result, this.clientOrigin.y + this.plantFocusPanel.Top + this.lifeCyclePanel.Top + this.lifeCycleDragger.Top, 1, this.lifeCycleDragger.Height, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.lifeCycleDraggingNeedToRedraw = true;
        return result;
    }
    
    public void undrawLifeCycleDraggerLine() {
        HDC theDC = new HDC();
        
        if (!this.lifeCycleDraggingNeedToRedraw) {
            return;
        }
        theDC = UNRESOLVED.getDC(0);
        UNRESOLVED.patBlt(theDC, this.lifeCycleDraggingLastDrawPos, this.clientOrigin.y + this.plantFocusPanel.Top + this.lifeCyclePanel.Top + this.lifeCycleDragger.Top, 1, this.lifeCycleDragger.Height, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.lifeCycleDraggingNeedToRedraw = false;
    }
    
    public void changeSelectedPlantAges(short newAge) {
        PdCommand newCommand = new PdCommand();
        
        if (this.selectedPlants.Count <= 0) {
            return;
        }
        newCommand = updcom.PdChangePlantAgeCommand().createWithListOfPlantsAndNewAge(this.selectedPlants, newAge);
        this.doCommand(newCommand);
    }
    
    // life cycle panel drawing and mouse handling 
    public void redrawLifeCycleGraph() {
        boolean sCurveError = false;
        
        this.lifeCycleGraphImage.Picture.Bitmap.Canvas.Brush.Color = UNRESOLVED.clBtnFace;
        this.lifeCycleGraphImage.Picture.Bitmap.Canvas.Rectangle(0, 0, this.lifeCycleGraphImage.ClientWidth, this.lifeCycleGraphImage.ClientHeight);
        sCurveError = this.drawSCurveOrCheckForError(this.lifeCycleGraphImage.Picture.Bitmap.Canvas, delphi_compatability.Bounds(0, 0, this.lifeCycleGraphImage.ClientWidth, this.lifeCycleGraphImage.ClientHeight), true, sCurveError);
        if (sCurveError && (this.focusedPlant() != null)) {
            // error - do something, should be caught by parameter panel 
            // PDF PORT -- put in NIL
            null;
        }
    }
    
    public void drawSCurveOrCheckForError(TCanvas aCanvas, TRect aRect, boolean draw, boolean failed) {
        PdPlant firstPlant = new PdPlant();
        int i = 0;
        float x = 0.0;
        float y = 0.0;
        TPoint thisPoint = new TPoint();
        SCurveStructure curve = new SCurveStructure();
        int numPoints = 0;
        
        firstPlant = this.focusedPlant();
        if (firstPlant == null) {
            return failed;
        }
        failed = true;
        numPoints = 100;
        // assumes that zero does NOT fall between x1 and x2, though one of these could be zero 
        curve.x1 = firstPlant.pGeneral.growthSCurve.x1;
        curve.y1 = firstPlant.pGeneral.growthSCurve.y1;
        curve.x2 = firstPlant.pGeneral.growthSCurve.x2;
        curve.y2 = firstPlant.pGeneral.growthSCurve.y2;
        try {
            failed = umath.calcSCurveCoeffsWithResult(curve, failed);
            if (failed) {
                return failed;
            }
            for (i = 0; i <= numPoints - 1; i++) {
                // delphi 2.0 wants this 
                x = 0.0;
                y = 0.0;
                try {
                    x = 1.0 * i / numPoints;
                } catch (Exception e) {
                    return failed;
                }
                y = umath.scurveWithResult(x, curve.c1, curve.c2, failed);
                if (failed) {
                    return failed;
                }
                if (draw) {
                    thisPoint.X = aRect.Left + intround(x * (aRect.Right - aRect.Left));
                    thisPoint.Y = aRect.Top + intround((1.0 - y) * (aRect.Bottom - aRect.Top));
                    if (i == 0) {
                        aCanvas.MoveTo(thisPoint.X, thisPoint.Y);
                    } else {
                        aCanvas.LineTo(thisPoint.X, thisPoint.Y);
                    }
                }
            }
        } catch (Exception e) {
            return failed;
        }
        failed = false;
        return failed;
    }
    
    // ----------------------------------------------------------------------------- *parameters panel 
    public void sectionsComboBoxDrawItem(TWinControl Control, int index, TRect Rect, TOwnerDrawState State) {
        PdSection section = new PdSection();
        TPicture sectionPicture = new TPicture();
        boolean selected = false;
        TRect textDrawRect = new TRect();
         cText = [0] * (range(0, 255 + 1) + 1);
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if ((this.sectionsComboBox.Items.Count <= 0) || (index < 0) || (index > this.sectionsComboBox.Items.Count - 1)) {
            return;
        }
        selected = (delphi_compatability.TOwnerDrawStateType.odSelected in State);
        // set up section pointer 
        section = (usection.PdSection)this.sectionsComboBox.Items.Objects[index];
        if (section == null) {
            return;
        }
        this.sectionsComboBox.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        this.sectionsComboBox.Canvas.Font = this.sectionsComboBox.Font;
        if (selected) {
            this.sectionsComboBox.Canvas.Brush.Color = UNRESOLVED.clHighlight;
            this.sectionsComboBox.Canvas.Font.Color = UNRESOLVED.clHighlightText;
        } else {
            this.sectionsComboBox.Canvas.Brush.Color = this.sectionsComboBox.Color;
            this.sectionsComboBox.Canvas.Font.Color = UNRESOLVED.clBtnText;
        }
        this.sectionsComboBox.Canvas.FillRect(Rect);
        textDrawRect = Rect;
        textDrawRect.Left = textDrawRect.Left + 4;
        textDrawRect.Top = textDrawRect.Top + (textDrawRect.Bottom - textDrawRect.Top) / 2 - (this.sectionsComboBox.Canvas.TextHeight("W") / 2);
        sectionPicture = this.sectionPictureForSectionName(section.getName());
        if (sectionPicture != null) {
            this.sectionsComboBox.Canvas.Draw(Rect.left + 4, Rect.top, sectionPicture.Graphic);
        }
        textDrawRect.Left = textDrawRect.Left + 32 + 4;
        UNRESOLVED.strPCopy(cText, this.sectionsComboBox.Items[index]);
        UNRESOLVED.winprocs.drawText(this.sectionsComboBox.Canvas.Handle, cText, len(cText), textDrawRect, delphi_compatability.DT_LEFT);
    }
    
    public void sectionsComboBoxChange(TObject Sender) {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        this.updateParameterPanelsForSectionChange();
        this.updateSectionPopupMenuForSectionChange();
    }
    
    // parameters panel 
    public void loadSectionsIntoListBox() {
        PdSection section = new PdSection();
        short i = 0;
        short indexOfPrimaryInflors = 0;
        
        if ((udomain.domain == null) || (udomain.domain.sectionManager == null)) {
            return;
        }
        this.sectionsComboBox.Clear();
        if (udomain.domain.sectionManager.sections.Count > 0) {
            for (i = 0; i <= udomain.domain.sectionManager.sections.Count - 1; i++) {
                section = usection.PdSection(udomain.domain.sectionManager.sections.Items[i]);
                if (section.showInParametersWindow) {
                    if (section.name == "Primary flowers, advanced") {
                        // kludge to get around necessary ordering of new advanced floral section
                        // advanced floral params are at end of file, but want to show them
                        // in the list before inflorescences
                        // WATCH OUT: change this code if you change the names of the sections
                        indexOfPrimaryInflors = this.sectionsComboBox.Items.IndexOf("Primary inflorescences");
                        this.sectionsComboBox.Items.InsertObject(indexOfPrimaryInflors, section.name, section);
                    } else {
                        this.sectionsComboBox.Items.AddObject(section.name, section);
                    }
                }
            }
        }
        if (udomain.domain.sectionManager.orthogonalSections.Count > 0) {
            for (i = 0; i <= udomain.domain.sectionManager.orthogonalSections.Count - 1; i++) {
                // v2.1 add orthogonal sections
                section = usection.PdSection(udomain.domain.sectionManager.orthogonalSections.Items[i]);
                if (section.showInParametersWindow) {
                    this.sectionsComboBox.Items.AddObject(section.name, section);
                }
            }
        }
    }
    
    public PdSection currentSection() {
        result = new PdSection();
        result = null;
        if ((this.sectionsComboBox.Items.Count <= 0) || (this.sectionsComboBox.ItemIndex < 0) || (this.sectionsComboBox.ItemIndex > this.sectionsComboBox.Items.Count - 1)) {
            return result;
        }
        result = usection.PdSection(this.sectionsComboBox.Items.Objects[this.sectionsComboBox.ItemIndex]);
        return result;
    }
    
    public TPicture sectionPictureForSectionName(String aName) {
        result = new TPicture();
        TImage image = new TImage();
        
        result = null;
        if (aName == "(no section)") {
            return result;
        }
        image = null;
        aName = lowercase(aName);
        if (usupport.found("general", aName)) {
            image = this.Sections_General;
        } else if (usupport.found("meris", aName)) {
            image = this.Sections_Meristems;
        } else if (usupport.found("inter", aName)) {
            image = this.Sections_Internodes;
        } else if (usupport.found("seed", aName)) {
            image = this.Sections_SeedlingLeaves;
        } else if (usupport.found("lea", aName)) {
            //must be below seedling leaves
            image = this.Sections_Leaves;
        } else if (usupport.found("flow", aName) && usupport.found("primary", aName) && usupport.found("advanced", aName)) {
            image = this.Sections_FlowersPrimaryAdvanced;
        } else if (usupport.found("flow", aName) && usupport.found("primary", aName)) {
            image = this.Sections_FlowersPrimary;
        } else if (usupport.found("inflo", aName) && usupport.found("primary", aName)) {
            image = this.Sections_InflorPrimary;
        } else if (usupport.found("fruit", aName)) {
            image = this.Sections_Fruit;
        } else if (usupport.found("flow", aName) && usupport.found("secondary", aName)) {
            image = this.Sections_FlowersSecondary;
        } else if (usupport.found("inflo", aName) && usupport.found("secondary", aName)) {
            image = this.Sections_InflorSecondary;
        } else if (usupport.found("root", aName)) {
            // v2.1 otherwise assume it is an orthogonal section
            image = this.Sections_RootTop;
        } else {
            image = this.Sections_Orthogonal;
        }
        if (image != null) {
            result = image.Picture;
        }
        return result;
    }
    
    public String sectionHelpIDForSectionName(String aName) {
        result = "";
        result = "";
        if (aName == "(no section)") {
            return result;
        }
        aName = lowercase(aName);
        if (usupport.found("general", aName)) {
            // trying to be flexible about possible name changes here 
            result = "General_parameters";
        } else if (usupport.found("meris", aName)) {
            result = "Meristem_parameters";
        } else if (usupport.found("inter", aName)) {
            result = "Internode_parameters";
        } else if (usupport.found("first", aName)) {
            result = "First_leaf_parameters";
        } else if (usupport.found("lea", aName)) {
            //must be below seedling leaves
            result = "Leaf_parameters";
        } else if (usupport.found("advanced", aName)) {
            // must be above flower params
            result = "Advanced_flower_parameters";
        } else if (usupport.found("flow", aName)) {
            result = "Flower_parameters";
        } else if (usupport.found("inflo", aName)) {
            result = "Inflorescence_parameters";
        } else if (usupport.found("fruit", aName)) {
            result = "Fruit_parameters";
        } else if (usupport.found("root", aName)) {
            // add more sections here if any are added to the params file 
            // v2.1 otherwise assume it is an orthogonal section
            result = "Root_top_parameters";
        } else {
            result = "Transverse_parameter_sections";
        }
        return result;
    }
    
    public void updateParameterPanelsForSectionChange() {
        PdParameterPanel paramPanel = new PdParameterPanel();
        PdParameterPanel oldParamPanel = new PdParameterPanel();
        PdSection section = new PdSection();
        PdParameter parameter = new PdParameter();
        short i = 0;
        
        try {
            UNRESOLVED.cursor_startWait;
            // clear out any earlier panels 
            this.selectedParameterPanel = null;
            if (this.parametersScrollBox.ControlCount > 0) {
                while (this.parametersScrollBox.ControlCount > 0) {
                    // this is the only valid time to free a component owned by something - after it has
                    //        been removed from the component list (owned objects) of the owner 
                    oldParamPanel = UNRESOLVED.PdParameterPanel(this.parametersScrollBox.Controls[0]);
                    this.removeComponent(oldParamPanel);
                    oldParamPanel.parent = null;
                    oldParamPanel.free;
                }
            }
            if (this.sectionsComboBox.ItemIndex < 0) {
                // make new panels for the current section 
                return;
            }
            section = (usection.PdSection)this.sectionsComboBox.Items.Objects[this.sectionsComboBox.ItemIndex];
            if (section.numSectionItems > 0) {
                for (i = 0; i <= section.numSectionItems - 1; i++) {
                    parameter = udomain.domain.parameterManager.parameterForFieldNumber(section.sectionItems[i]);
                    if (parameter == null) {
                        continue;
                    }
                    paramPanel = null;
                    // note that the longint type is used to store plant positions, but should not be used
                    //          for parameter panels 
                    switch (parameter.fieldType) {
                        case uparams.kFieldHeader:
                            paramPanel = UNRESOLVED.PdHeaderParameterPanel.createForParameter(this, parameter);
                            break;
                        case uparams.kFieldEnumeratedList:
                            paramPanel = UNRESOLVED.PdListParameterPanel.createForParameter(this, parameter);
                            break;
                        case uparams.kFieldThreeDObject:
                            paramPanel = UNRESOLVED.PdTdoParameterPanel.createForParameter(this, parameter);
                            break;
                        case uparams.kFieldColor:
                            paramPanel = UNRESOLVED.PdColorParameterPanel.createForParameter(this, parameter);
                            break;
                        case uparams.kFieldSmallint:
                            paramPanel = UNRESOLVED.PdSmallintParameterPanel.createForParameter(this, parameter);
                            break;
                        case uparams.kFieldFloat:
                            if (parameter.indexCount() <= 1) {
                                paramPanel = UNRESOLVED.PdRealParameterPanel.createForParameter(this, parameter);
                            } else if (parameter.indexType == uparams.kIndexTypeSCurve) {
                                paramPanel = UNRESOLVED.PdSCurveParameterPanel.createForParameter(this, parameter);
                            }
                            break;
                        case uparams.kFieldBoolean:
                            paramPanel = UNRESOLVED.PdBooleanParameterPanel.createForParameter(this, parameter);
                            break;
                        default:
                            throw new GeneralException.create("Problem: Unsupported parameter type in method TMainForm.updateParameterPanelsForSectionChange.");
                            break;
                    if (paramPanel != null) {
                        paramPanel.parent = this.parametersScrollBox;
                        //9 +
                        paramPanel.tabOrder = i;
                        paramPanel.calculateTextDimensions;
                        paramPanel.calculateHeight;
                        if ((parameter.originalSectionName != section.name) && !(paramPanel instanceof UNRESOLVED.PdHeaderParameterPanel)) {
                            // v2.1 add original section name to params in orthogonal sections
                            paramPanel.caption = paramPanel.caption + " [" + parameter.originalSectionName + "]";
                        }
                    }
                }
            }
            this.updateParametersPanelForFirstSelectedPlant();
            this.repositionParameterPanels();
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
    }
    
    public String paramHelpIDForParamPanel(PdParameterPanel panel) {
        result = "";
        result = "";
        if (panel == null) {
            return result;
        }
        if (panel instanceof UNRESOLVED.PdHeaderParameterPanel) {
            result = "Using_header_parameter_panels";
        } else if ((panel instanceof UNRESOLVED.PdSmallintParameterPanel) || (panel instanceof UNRESOLVED.PdRealParameterPanel)) {
            result = "Using_number_parameter_panels";
        } else if (panel instanceof UNRESOLVED.PdSCurveParameterPanel) {
            result = "Using_S_curve_parameter_panels";
        } else if (panel instanceof UNRESOLVED.PdBooleanParameterPanel) {
            result = "Using_yes/no_parameter_panels";
        } else if (panel instanceof UNRESOLVED.PdListParameterPanel) {
            result = "Using_list_parameter_panels";
        } else if (panel instanceof UNRESOLVED.PdColorParameterPanel) {
            result = "Using_color_parameter_panels";
        } else if (panel instanceof UNRESOLVED.PdTdoParameterPanel) {
            result = "Using_3D_object_parameter_panels";
        }
        return result;
    }
    
    public void updateParametersPanelForFirstSelectedPlant() {
        int i = 0;
        PdParameterPanel paramPanel = new PdParameterPanel();
        
        this.updatePlantNameLabel(kTabParameters);
        if (this.parametersScrollBox.ControlCount > 0) {
            for (i = 0; i <= this.parametersScrollBox.ControlCount - 1; i++) {
                if (this.parametersScrollBox.Controls[i] instanceof UNRESOLVED.PdParameterPanel) {
                    paramPanel = (UNRESOLVED.PdParameterPanel)this.parametersScrollBox.Controls[i];
                    //panels check if the new plant is different from current one
                    paramPanel.updatePlant(this.focusedPlant());
                }
            }
        }
        this.repositionParameterPanels();
    }
    
    public void enteringAParameterPanel(PdParameterPanel aPanel) {
        this.selectedParameterPanel = aPanel;
        // update menu items and other things 
    }
    
    public void leavingAParameterPanel(PdParameterPanel aPanel) {
        this.selectedParameterPanel = null;
        // update menu items and other things 
    }
    
    public void repositionParameterPanels() {
        int i = 0;
        int lastPos = 0;
        int totalMaxWidth = 0;
        int panelMaxWidth = 0;
        int panelMinWidth = 0;
        int requestedWidth = 0;
        boolean windowLock = false;
        PdParameterPanel paramPanel = new PdParameterPanel();
        int oldPosition = 0;
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.parametersScrollBox.ControlCount > 0) {
            totalMaxWidth = 0;
            lastPos = 0;
            oldPosition = this.parametersScrollBox.VertScrollBar.Position;
            this.parametersScrollBox.VertScrollBar.Position = 0;
            windowLock = UNRESOLVED.lockWindowUpdate(this.handle);
            requestedWidth = this.parametersScrollBox.ClientWidth;
            for (i = 0; i <= this.parametersScrollBox.ControlCount - 1; i++) {
                paramPanel = UNRESOLVED.PdParameterPanel(this.parametersScrollBox.Controls[i]);
                paramPanel.left = 0;
                paramPanel.top = lastPos;
                paramPanel.calculateTextDimensions;
                panelMaxWidth = paramPanel.maxWidth;
                panelMinWidth = paramPanel.minWidth(requestedWidth);
                if (panelMaxWidth <= requestedWidth) {
                    paramPanel.width = panelMaxWidth;
                } else {
                    if (panelMinWidth == -1) {
                        paramPanel.width = requestedWidth;
                    } else {
                        paramPanel.width = panelMinWidth;
                    }
                }
                paramPanel.calculateHeight;
                lastPos = lastPos + paramPanel.height;
                if (paramPanel.width > totalMaxWidth) {
                    totalMaxWidth = paramPanel.width;
                }
            }
            lastPos = 0;
            for (i = 0; i <= this.parametersScrollBox.ControlCount - 1; i++) {
                paramPanel = UNRESOLVED.PdParameterPanel(this.parametersScrollBox.Controls[i]);
                paramPanel.top = lastPos;
                // cfk change v2.0 final - can't remember why we had a max width - looks better this way
                // paramPanel.width := totalMaxWidth;   // was this
                // changed to
                paramPanel.width = this.parametersScrollBox.Width - 20;
                paramPanel.calculateHeight;
                paramPanel.resizeElements;
                lastPos = lastPos + paramPanel.height;
            }
            this.parametersScrollBox.VertScrollBar.Position = oldPosition;
            if (windowLock) {
                UNRESOLVED.lockWindowUpdate(0);
            }
        }
    }
    
    public void collapseOrExpandParameterPanelsUntilNextHeader(PdParameterPanel headerPanel) {
        boolean collapsing = false;
        PdParameterPanel paramPanel = new PdParameterPanel();
        short i = 0;
        
        collapsing = false;
        this.internalChange = true;
        if (this.parametersScrollBox.ControlCount > 0) {
            for (i = 0; i <= this.parametersScrollBox.ControlCount - 1; i++) {
                paramPanel = UNRESOLVED.PdParameterPanel(this.parametersScrollBox.Controls[i]);
                if (paramPanel == headerPanel) {
                    collapsing = true;
                } else if (collapsing && (paramPanel instanceof UNRESOLVED.PdHeaderParameterPanel)) {
                    collapsing = false;
                } else if (collapsing) {
                    if (headerPanel.param.collapsed) {
                        paramPanel.expand;
                    } else {
                        paramPanel.collapse;
                    }
                }
            }
        }
        this.internalChange = false;
        this.repositionParameterPanels();
    }
    
    public void collapseOrExpandAllParameterPanelsInCurrentSection(short doWhat) {
        PdSection section = new PdSection();
        PdParameterPanel paramPanel = new PdParameterPanel();
        short i = 0;
        
        this.internalChange = true;
        if (this.sectionsComboBox.ItemIndex < 0) {
            return;
        }
        section = (usection.PdSection)this.sectionsComboBox.Items.Objects[this.sectionsComboBox.ItemIndex];
        if (section == null) {
            return;
        }
        switch (doWhat) {
            case kExpand:
                section.expanded = true;
                break;
            case kCollapse:
                section.expanded = false;
                break;
            case kExpandOrCollapse:
                section.expanded = !section.expanded;
                break;
        if (this.parametersScrollBox.ControlCount > 0) {
            for (i = 0; i <= this.parametersScrollBox.ControlCount - 1; i++) {
                paramPanel = UNRESOLVED.PdParameterPanel(this.parametersScrollBox.Controls[i]);
                if (section.expanded) {
                    paramPanel.expand;
                } else {
                    paramPanel.collapse;
                }
            }
        }
        this.internalChange = false;
        this.repositionParameterPanels();
    }
    
    public void updateParameterValuesWithUpdateListForPlant(PdPlant aPlant, TListCollection updateList) {
        long i = 0;
        PdParameterPanel paramPanel = new PdParameterPanel();
        PdPlantUpdateEvent updateEvent = new PdPlantUpdateEvent();
        boolean needToUpdateWholePlant = false;
        
        if (aPlant != this.focusedPlant()) {
            return;
        }
        if (updateList.Count <= 0) {
            return;
        }
        // first look to see if the whole plant needs updated - if any do, update it 
        // this is for side effects in GWI - left in just in case we need it later 
        needToUpdateWholePlant = false;
        for (i = 0; i <= updateList.Count - 1; i++) {
            updateEvent = uplant.PdPlantUpdateEvent(updateList.Items[i]);
            if ((updateEvent.plant != null) && (updateEvent.plant.wholePlantUpdateNeeded)) {
                needToUpdateWholePlant = true;
                updateEvent.plant.wholePlantUpdateNeeded = false;
            }
        }
        if (needToUpdateWholePlant) {
            this.updateParametersPanelForFirstSelectedPlant();
            return;
        }
        if (this.parametersScrollBox.ControlCount > 0) {
            for (i = 0; i <= this.parametersScrollBox.ControlCount - 1; i++) {
                if (this.parametersScrollBox.Controls[i] instanceof UNRESOLVED.PdParameterPanel) {
                    // if not updating everything, update based on list 
                    // tell all components to look at list to see if they need updating 
                    paramPanel = (UNRESOLVED.PdParameterPanel)this.parametersScrollBox.Controls[i];
                    // components check if use models and fields in list 
                    paramPanel.updateFromUpdateEventList(updateList);
                }
            }
        }
    }
    
    // stats panel
    public void updateStatisticsPanelForFirstSelectedPlant() {
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.statsPanel == null) {
            return;
        }
        this.statsPanel.updatePlant(this.focusedPlant());
        this.statsPanel.updatePlantValues;
    }
    
    // note panel
    public void updateNoteForFirstSelectedPlant() {
        int selStart = 0;
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.notePanel == null) {
            return;
        }
        if (this.noteMemo == null) {
            return;
        }
        this.updatePlantNameLabel(kTabNote);
        this.updateForChangeToPlantNote(this.focusedPlant());
    }
    
    public void noteEditClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        TNoteEditForm noteForm = new TNoteEditForm();
        TStringList commandLines = new TStringList();
        
        if (this.focusedPlant() == null) {
            return;
        }
        noteForm = UNRESOLVED.TNoteEditForm.create(this);
        if (noteForm == null) {
            throw new GeneralException.create("Problem: Could not create note edit window.");
        }
        try {
            noteForm.noteEditMemo.lines.addStrings(this.focusedPlant().noteLines);
            noteForm.caption = "Edit note for " + this.focusedPlant().getName();
            if (noteForm.showModal != mrCancel) {
                // command will take ownership of this and free it if necessary
                commandLines = delphi_compatability.TStringList.create;
                commandLines.AddStrings(noteForm.noteEditMemo.lines);
                newCommand = updcom.PdEditNoteCommand().createWithPlantAndNewTStrings(this.focusedPlant(), commandLines);
                this.doCommand(newCommand);
            }
        } finally {
            noteForm.free;
            noteForm = null;
        }
    }
    
    public void NotePopupMenuCopyClick(TObject Sender) {
        this.noteMemo.CopyToClipboard();
    }
    
    public void NotePopupMenuEditClick(TObject Sender) {
        this.noteEditClick(this);
    }
    
    public void NotePopupMenuSelectAllClick(TObject Sender) {
        this.noteMemo.SelectAll();
    }
    
    public void MenuPlantEditNoteClick(TObject Sender) {
        this.noteEditClick(this);
    }
    
    public void PopupMenuEditNoteClick(TObject Sender) {
        this.noteEditClick(this);
    }
    
    // rotations panel
    public void updateRotationsPanelForFirstSelectedPlant() {
        TColorRef color = new TColorRef();
        
        this.updatePlantNameLabel(kTabRotations);
        color = this.textColorToRepresentPlantSelection(false);
        // location
        this.locationLabel.Font.Color = color;
        this.xLocationLabel.Font.Color = color;
        this.yLocationLabel.Font.Color = color;
        this.locationPixelsLabel.Font.Color = color;
        // size
        this.sizingLabel.Font.Color = color;
        this.drawingScalePixelsPerMmLabel.Font.Color = color;
        // rotation
        this.rotationLabel.Font.Color = color;
        this.xRotationLabel.Font.Color = color;
        this.yRotationLabel.Font.Color = color;
        this.zRotationLabel.Font.Color = color;
        // other updates
        this.updateForChangeToPlantRotations();
        this.updateForChangeToSelectedPlantsDrawingScale();
        this.updateForChangeToSelectedPlantsLocation();
    }
    
    // posing panel
    // ------------------------------------------------------------------------------------- *posing - updating 
    public void updatePosingForFirstSelectedPlant() {
        int i = 0;
        PdPlantDrawingAmendment amendment = new PdPlantDrawingAmendment();
        String partString = "";
        
        this.internalChange = true;
        this.posedPartsLabel.Font.Color = this.textColorToRepresentPlantSelection(false);
        this.selectedPartLabel.Font.Color = this.textColorToRepresentPlantSelection(false);
        this.posingPosePart.Enabled = false;
        this.posingUnposePart.Enabled = false;
        // called when plant changes
        this.posedPlantParts.Clear();
        this.updatePlantNameLabel(kTabPosing);
        if (this.focusedPlant() == null) {
            this.posedPlantParts.Text = "";
            this.posedPlantParts.Enabled = false;
        } else {
            this.posedPlantParts.Enabled = true;
            if (this.focusedPlant().amendments.Count <= 0) {
                // load list of parts with amendments
                this.selectedPlantPartID = -1;
            } else {
                for (i = 0; i <= this.focusedPlant().amendments.Count - 1; i++) {
                    amendment = uamendmt.PdPlantDrawingAmendment(this.focusedPlant().amendments.Items[i]);
                    partString = this.partDescriptionForIDAndType(amendment.partID, amendment.typeOfPart);
                    if (this.posedPlantParts.Items.IndexOf(partString) < 0) {
                        this.posedPlantParts.Items.Add(partString);
                    }
                }
                this.posedPlantParts.Items.Add(kSelectNoPosedPartString);
            }
        }
        this.internalChange = false;
        this.updatePosingForSelectedPlantPart();
    }
    
    public void updatePosingForSelectedPlantPart() {
        String partString = "";
        short index = 0;
        
        // PDF PORT -- removed semicolon from after begin
        this.internalChange = true;
        if (this.focusedPlant() == null) {
            // called when selected part changes
            this.selectedPlantPartID = -1;
            this.selectedPlantPartType = "";
            this.selectedPartLabel.Caption = kNoPartSelected;
        }
        if (this.selectedPlantPartID >= 0) {
            partString = this.partDescriptionForIDAndType(this.selectedPlantPartID, this.selectedPlantPartType);
            this.selectedPartLabel.Caption = "Selected part: " + partString;
            index = this.posedPlantParts.Items.IndexOf(partString);
            if (index >= 0) {
                this.posedPlantParts.ItemIndex = index;
            } else {
                this.posedPlantParts.ItemIndex = -1;
            }
        } else {
            this.posedPlantParts.ItemIndex = -1;
            this.selectedPartLabel.Caption = kNoPartSelected;
        }
        this.posingPosePart.Enabled = !(this.selectedPartLabel.Caption == kNoPartSelected);
        this.posingUnposePart.Enabled = false;
        this.internalChange = false;
        this.updatePoseInfo();
    }
    
    public void updatePoseInfo() {
        PdPlantDrawingAmendment amendment = new PdPlantDrawingAmendment();
        long partID = 0;
        
        this.internalChange = true;
        amendment = null;
        partID = this.selectedPartIDInAmendedPartsList();
        if (partID >= 0) {
            amendment = this.focusedPlant().amendmentForPartID(partID);
        }
        this.posingPosePart.Enabled = (!(this.selectedPartLabel.Caption == kNoPartSelected)) && (amendment == null);
        this.posingUnposePart.Enabled = (!(this.selectedPartLabel.Caption == kNoPartSelected)) && (!(amendment == null));
        this.posingDetailsPanel.Visible = amendment != null;
        if ((amendment != null)) {
            this.posingHidePart.Checked = amendment.hide;
            //
            //    posingChangeColors.checked := changeColors;
            //    posingFrontfaceColor.color := faceColor;
            //    posingBackfaceColor.color := BackfaceColor;
            //    posingLineColor.color := lineColor;
            //    posingChangeAllColorsAfter.checked := propagateColors;
            //    
            this.posingAddExtraRotation.Checked = amendment.addRotations;
            this.posingXRotationEdit.Text = IntToStr(intround(amendment.xRotation));
            this.posingYRotationEdit.Text = IntToStr(intround(amendment.yRotation));
            this.posingZRotationEdit.Text = IntToStr(intround(amendment.zRotation));
            this.posingMultiplyScale.Checked = amendment.multiplyScale;
            this.posingMultiplyScaleAllPartsAfter.Checked = amendment.propagateScale;
            this.posingScaleMultiplierEdit.Text = IntToStr(amendment.scaleMultiplier_pct);
            this.posingLengthMultiplierEdit.Text = IntToStr(amendment.lengthMultiplier_pct);
            this.posingWidthMultiplierEdit.Text = IntToStr(amendment.widthMultiplier_pct);
        }
        this.internalChange = false;
        this.updateForDependenciesWithinPoseInfo();
    }
    
    public void updateForDependenciesWithinPoseInfo() {
        this.internalChange = true;
        this.posingChangeAllColorsAfter.Enabled = this.posingChangeColors.Checked;
        this.posingMultiplyScaleAllPartsAfter.Enabled = this.posingMultiplyScale.Checked;
        this.posingMultiplyScaleAllPartsAfterLabel.Enabled = this.posingMultiplyScaleAllPartsAfter.Enabled;
        //
        //  posingLineColor.visible := posingChangeColors.checked;
        //  posingLineColorLabel.enabled := posingChangeColors.checked;
        //  posingFrontfaceColor.visible := posingChangeColors.checked;
        //  posingFrontfaceColorLabel.enabled := posingChangeColors.checked;
        //  posingBackfaceColor.visible := posingChangeColors.checked;
        //  posingBackfaceColorLabel.enabled := posingChangeColors.checked;
        //  
        enableOrDisableSet(this.posingXRotationLabel, this.posingXRotationEdit, this.posingXRotationSpin, null, this.posingAddExtraRotation.Checked);
        enableOrDisableSet(this.posingYRotationLabel, this.posingYRotationEdit, this.posingYRotationSpin, null, this.posingAddExtraRotation.Checked);
        enableOrDisableSet(this.posingZRotationLabel, this.posingZRotationEdit, this.posingZRotationSpin, null, this.posingAddExtraRotation.Checked);
        this.rotationDegreesLabel.Enabled = this.posingAddExtraRotation.Checked;
        enableOrDisableSet(this.posingScaleMultiplierLabel, this.posingScaleMultiplierEdit, this.posingScaleMultiplierSpin, this.posingScaleMultiplierPercent, this.posingMultiplyScale.Checked);
        enableOrDisableSet(this.posingLengthMultiplierLabel, this.posingLengthMultiplierEdit, this.posingLengthMultiplierSpin, this.posingLengthMultiplierPercent, this.posingMultiplyScale.Checked);
        enableOrDisableSet(this.posingWidthMultiplierLabel, this.posingWidthMultiplierEdit, this.posingWidthMultiplierSpin, this.posingWidthMultiplierPercent, this.posingMultiplyScale.Checked);
        this.internalChange = false;
    }
    
    public void redrawAllPlantsInViewWithAmendments() {
        short i = 0;
        PdPlant plant = new PdPlant();
        
        if (this.plants.Count > 0) {
            for (i = 0; i <= this.plants.Count - 1; i++) {
                plant = uplant.PdPlant(this.plants.Items[i]);
                if ((plant != null) && (plant.amendments != null) && (plant.amendments.Count > 0)) {
                    plant.recalculateBounds(kDrawNow);
                    this.invalidateDrawingRect(plant.boundsRect_pixels());
                }
            }
        }
        this.updateForPossibleChangeToDrawing();
    }
    
    // ------------------------------------------------------------------------------------- *posing - interface 
    public void posedPlantPartsChange(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        
        if (this.internalChange) {
            return;
        }
        if (this.posedPlantParts.ItemIndex == this.posedPlantParts.Items.Count - 1) {
            newCommand = updcom.PdSelectPosingPartCommand().createWithPlantAndPartIDsAndTypes(this.focusedPlant(), -1, this.selectedPlantPartID, "", this.selectedPlantPartType);
        } else {
            newCommand = updcom.PdSelectPosingPartCommand().createWithPlantAndPartIDsAndTypes(this.focusedPlant(), this.selectedPartIDInAmendedPartsList(), this.selectedPlantPartID, this.selectedPartTypeInAmendedPartsList(), this.selectedPlantPartType);
        }
        this.doCommand(newCommand);
    }
    
    public void posingFrontfaceColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.posingFrontfaceColor.Color = udomain.domain.getColorUsingCustomColors(this.posingFrontfaceColor.Color);
        this.changeSelectedPose(this.posingFrontfaceColor);
    }
    
    public void posingBackfaceColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.posingBackfaceColor.Color = udomain.domain.getColorUsingCustomColors(this.posingBackfaceColor.Color);
        this.changeSelectedPose(this.posingBackfaceColor);
    }
    
    public void posingLineColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.posingLineColor.Color = udomain.domain.getColorUsingCustomColors(this.posingLineColor.Color);
        this.changeSelectedPose(this.posingLineColor);
    }
    
    public void posingRotationSpinUp(TObject Sender) {
        if ((Sender != null) && (Sender instanceof delphi_compatability.TSpinButton)) {
            this.spinPoseRotationBy(((delphi_compatability.TSpinButton)Sender).focusControl, udomain.domain.options.rotationIncrement);
        }
    }
    
    public void posingRotationSpinDown(TObject Sender) {
        if ((Sender != null) && (Sender instanceof delphi_compatability.TSpinButton)) {
            this.spinPoseRotationBy(((delphi_compatability.TSpinButton)Sender).focusControl, -udomain.domain.options.rotationIncrement);
        }
    }
    
    public void spinPoseRotationBy(TObject sender, int amount) {
        short newRotation = 0;
        short oldRotation = 0;
        
        if ((sender != null) && (sender instanceof delphi_compatability.TEdit)) {
            newRotation = StrToIntDef(((delphi_compatability.TEdit)sender).text, 0);
            oldRotation = newRotation;
            newRotation = newRotation + amount;
            if (newRotation < -360) {
                newRotation = 360 - (abs(newRotation) - 360);
            }
            if (newRotation > 360) {
                newRotation = -360 + (newRotation - 360);
            }
            if (newRotation != oldRotation) {
                ((delphi_compatability.TEdit)sender).text = IntToStr(newRotation);
            }
        }
    }
    
    public void posingScaleMultiplierSpinUpClick(TObject Sender) {
        if ((Sender != null) && (Sender instanceof delphi_compatability.TSpinButton)) {
            this.spinScaleMultiplierBy(((delphi_compatability.TSpinButton)Sender).focusControl, udomain.domain.options.resizeKeyUpMultiplierPercent - 100);
        }
    }
    
    public void posingScaleMultiplierSpinDownClick(TObject Sender) {
        if ((Sender != null) && (Sender instanceof delphi_compatability.TSpinButton)) {
            this.spinScaleMultiplierBy(((delphi_compatability.TSpinButton)Sender).focusControl, -(udomain.domain.options.resizeKeyUpMultiplierPercent - 100));
        }
    }
    
    public void spinScaleMultiplierBy(TObject sender, int amount) {
        short newValue = 0;
        short oldValue = 0;
        
        if ((sender != null) && (sender instanceof delphi_compatability.TEdit)) {
            newValue = StrToIntDef(((delphi_compatability.TEdit)sender).text, 0);
            oldValue = newValue;
            newValue = newValue + amount;
            if (newValue < 0) {
                newValue = 0;
            }
            if (newValue > 1000) {
                newValue = 1000;
            }
            if (newValue != oldValue) {
                ((delphi_compatability.TEdit)sender).text = IntToStr(newValue);
            }
        }
    }
    
    // ------------------------------------------------------------------------------------- *posing - commands 
    public void changeSelectedPose(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        PdPlantDrawingAmendment newAmendment = new PdPlantDrawingAmendment();
        long partID = 0;
        PdPlantDrawingAmendment currentAmendment = new PdPlantDrawingAmendment();
        String field = "";
        
        if (this.internalChange) {
            return;
        }
        this.updateForDependenciesWithinPoseInfo();
        if (this.focusedPlant() == null) {
            return;
        }
        // command will take ownership of this and free it if necessary
        newAmendment = uamendmt.PdPlantDrawingAmendment().create();
        partID = this.selectedPartIDInAmendedPartsList();
        currentAmendment = this.focusedPlant().amendmentForPartID(partID);
        if (currentAmendment == null) {
            return;
        }
        if ((Sender == this.posingHidePart)) {
            field = "hide";
        } else if ((Sender == this.posingAddExtraRotation)) {
            field = "rotate";
        } else if (((Sender == this.posingXRotationEdit) || (Sender == this.posingXRotationSpin))) {
            field = "X rotation";
        } else if (((Sender == this.posingYRotationEdit) || (Sender == this.posingYRotationSpin))) {
            field = "Y rotation";
        } else if (((Sender == this.posingZRotationEdit) || (Sender == this.posingZRotationSpin))) {
            field = "Z rotation";
        } else if ((Sender == this.posingMultiplyScale)) {
            field = "scale";
        } else if ((Sender == this.posingMultiplyScaleAllPartsAfter)) {
            field = "scale above";
        } else if (((Sender == this.posingScaleMultiplierEdit) || (Sender == this.posingScaleMultiplierSpin))) {
            field = "3D object scale";
        } else if (((Sender == this.posingLengthMultiplierEdit) || (Sender == this.posingLengthMultiplierSpin))) {
            field = "line length";
        } else if (((Sender == this.posingWidthMultiplierEdit) || (Sender == this.posingWidthMultiplierSpin))) {
            field = "line width";
        } else {
            field = "";
        }
        //   cfk if bring back color finish these
        //    posingChangeColors: TCheckBox;
        //    posingChangeAllColorsAfter: TCheckBox;
        //    posingLineColor: TPanel;
        //    posingFrontfaceColor: TPanel;
        //    posingBackfaceColor: TPanel;
        //    posingLineColorLabel: TLabel;
        //    posingFrontfaceColorLabel: TLabel;
        //    posingBackfaceColorLabel: TLabel;
        //    
        newAmendment.partID = this.partIDForFullDescription(this.posedPlantParts.Text);
        newAmendment.typeOfPart = this.partTypeForFullDescription(this.posedPlantParts.Text);
        newAmendment.hide = this.posingHidePart.Checked;
        //
        //    changeColors := posingChangeColors.checked;
        //    faceColor := posingFrontfaceColor.color;
        //    backfaceColor := posingBackfaceColor.color;
        //    lineColor := posingLineColor.color;
        //    propagateColors := posingChangeAllColorsAfter.checked;
        //    
        newAmendment.addRotations = this.posingAddExtraRotation.Checked;
        newAmendment.xRotation = umath.intMax(-360, umath.intMin(360, StrToIntDef(this.posingXRotationEdit.Text, intround(currentAmendment.xRotation))));
        newAmendment.yRotation = umath.intMax(-360, umath.intMin(360, StrToIntDef(this.posingYRotationEdit.Text, intround(currentAmendment.yRotation))));
        newAmendment.zRotation = umath.intMax(-360, umath.intMin(360, StrToIntDef(this.posingZRotationEdit.Text, intround(currentAmendment.zRotation))));
        newAmendment.multiplyScale = this.posingMultiplyScale.Checked;
        newAmendment.propagateScale = this.posingMultiplyScaleAllPartsAfter.Checked;
        newAmendment.scaleMultiplier_pct = umath.intMax(0, umath.intMin(1000, StrToIntDef(this.posingScaleMultiplierEdit.Text, currentAmendment.scaleMultiplier_pct)));
        newAmendment.lengthMultiplier_pct = umath.intMax(0, umath.intMin(1000, StrToIntDef(this.posingLengthMultiplierEdit.Text, currentAmendment.lengthMultiplier_pct)));
        newAmendment.widthMultiplier_pct = umath.intMax(0, umath.intMin(1000, StrToIntDef(this.posingWidthMultiplierEdit.Text, currentAmendment.widthMultiplier_pct)));
        newCommand = updcom.PdEditAmendmentCommand().createWithPlantAndAmendmentAndField(this.focusedPlant(), newAmendment, field);
        this.doCommand(newCommand);
    }
    
    public void posingPosePartClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        PdPlantDrawingAmendment newAmendment = new PdPlantDrawingAmendment();
        
        if (this.focusedPlant() == null) {
            return;
        }
        if (this.selectedPlantPartID < 0) {
            return;
        }
        if (this.focusedPlant().amendmentForPartID(this.selectedPlantPartID) != null) {
            // only one amendment per part id
            return;
        }
        // command will take ownership of this and free it if necessary
        newAmendment = uamendmt.PdPlantDrawingAmendment().create();
        newAmendment.partID = this.selectedPlantPartID;
        newAmendment.typeOfPart = this.selectedPlantPartType;
        newCommand = updcom.PdCreateAmendmentCommand().createWithPlantAndAmendment(this.focusedPlant(), newAmendment);
        this.doCommand(newCommand);
    }
    
    public void posingUnposePartClick(TObject Sender) {
        PdCommand newCommand = new PdCommand();
        PdPlantDrawingAmendment amendment = new PdPlantDrawingAmendment();
        
        if (this.focusedPlant() == null) {
            return;
        }
        amendment = this.focusedPlant().amendmentForPartID(this.selectedPartIDInAmendedPartsList());
        if (amendment == null) {
            return;
        }
        newCommand = updcom.PdDeleteAmendmentCommand().createWithPlantAndAmendment(this.focusedPlant(), amendment);
        this.doCommand(newCommand);
    }
    
    public void addAmendedPartToList(long partID, String partType) {
        String newString = "";
        short selectNoneIndex = 0;
        short indexToSave = 0;
        
        newString = MainForm.partDescriptionForIDAndType(partID, partType);
        this.posedPlantParts.Items.Add(newString);
        indexToSave = this.posedPlantParts.Items.Count - 1;
        // add "select none" to end - move down if already there
        selectNoneIndex = this.posedPlantParts.Items.IndexOf(kSelectNoPosedPartString);
        if (selectNoneIndex >= 0) {
            this.posedPlantParts.Items.Delete(selectNoneIndex);
        }
        this.posedPlantParts.Items.Add(kSelectNoPosedPartString);
        this.posedPlantParts.ItemIndex = indexToSave;
        this.updatePosingForSelectedPlantPart();
    }
    
    public void removeAmendedPartFromList(long partID, String partType) {
        String oldString = "";
        int index = 0;
        int oldItemIndex = 0;
        
        oldItemIndex = this.posedPlantParts.ItemIndex;
        oldString = this.partDescriptionForIDAndType(partID, partType);
        index = this.posedPlantParts.Items.IndexOf(oldString);
        if (index >= 0) {
            this.posedPlantParts.Items.Delete(index);
        }
        if (oldItemIndex <= this.posedPlantParts.Items.Count - 1) {
            this.posedPlantParts.ItemIndex = oldItemIndex;
        }
        this.updatePosingForSelectedPlantPart();
    }
    
    // ------------------------------------------------------------------------------------- *posing - supporting 
    public String partDescriptionForIDAndType(long id, String typeName) {
        result = "";
        result = IntToStr(id) + " (" + typeName + ")";
        return result;
    }
    
    public long partIDForFullDescription(String aString) {
        result = 0;
        result = StrToIntDef(usupport.stringUpTo(aString, " ("), -1);
        return result;
    }
    
    public String partTypeForFullDescription(String aString) {
        result = "";
        result = "";
        if (len(aString) <= 0) {
            return result;
        }
        result = usupport.stringBeyond(aString, "(");
        result = usupport.stringUpTo(result, ")");
        return result;
    }
    
    public long selectedPartIDInAmendedPartsList() {
        result = 0;
        result = -1;
        if ((this.focusedPlant() == null) || (this.posedPlantParts.Items.Count <= 0) || (this.posedPlantParts.ItemIndex < 0)) {
            return result;
        }
        result = this.partIDForFullDescription(this.posedPlantParts.Items[this.posedPlantParts.ItemIndex]);
        return result;
    }
    
    public String selectedPartTypeInAmendedPartsList() {
        result = "";
        result = "";
        if ((this.focusedPlant() == null) || (this.posedPlantParts.Items.Count <= 0) || (this.posedPlantParts.ItemIndex < 0)) {
            return result;
        }
        result = this.partTypeForFullDescription(this.posedPlantParts.Items[this.posedPlantParts.ItemIndex]);
        return result;
    }
    
    // ------------------------------------------------------------------------------------- *resizing 
    public void FormResize(TObject Sender) {
        short newTop = 0;
        short newLeft = 0;
        short newWidth = 0;
        short newHeight = 0;
        short splitterWidthOrHeight = 0;
        boolean windowLock = false;
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if (this.WindowState == delphi_compatability.TWindowState.wsMinimized) {
            return;
        }
        if (udomain.domain == null) {
            return;
        }
        if (this.drawingBitmap == null) {
            return;
        }
        if (this.selectedPlants == null) {
            return;
        }
        this.horizontalSplitter.Visible = false;
        this.verticalSplitter.Visible = false;
        this.plantListPanel.Visible = false;
        this.plantFocusPanel.Visible = false;
        windowLock = UNRESOLVED.lockWindowUpdate(this.handle);
        this.toolbarPanel.SetBounds(0, 0, this.clientWidth, this.toolbarPanel.Height);
        //assumes they are equal, I have at 4 now
        splitterWidthOrHeight = this.verticalSplitter.Width;
        if (this.lastHeight != 0) {
            newTop = intround(1.0 * this.horizontalSplitter.Top * UNRESOLVED.clientHeight / this.lastHeight);
        } else {
            newTop = UNRESOLVED.clientHeight / 2;
        }
        newTop = umath.intMax(0, umath.intMin(this.clientHeight - 1, newTop));
        newHeight = umath.intMax(0, this.clientHeight - newTop - splitterWidthOrHeight);
        if (this.lastWidth != 0) {
            newLeft = intround(1.0 * this.verticalSplitter.Left * UNRESOLVED.clientWidth / this.lastWidth);
        } else {
            newLeft = UNRESOLVED.clientWidth / 2;
        }
        newLeft = umath.intMax(0, umath.intMin(this.clientWidth - 1, newLeft));
        newWidth = umath.intMax(0, this.clientWidth - newLeft - splitterWidthOrHeight);
        if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal) {
            this.horizontalSplitter.SetBounds(0, newTop, this.clientWidth, this.horizontalSplitter.Height);
            this.verticalSplitter.SetBounds(newLeft, newTop + this.horizontalSplitter.Height, this.verticalSplitter.Width, newHeight);
        } else if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical) {
            this.verticalSplitter.SetBounds(newLeft, this.toolbarPanel.Height, this.verticalSplitter.Width, umath.intMax(0, this.clientHeight - this.toolbarPanel.Height));
            this.horizontalSplitter.SetBounds(newLeft + this.verticalSplitter.Width, newTop, newWidth, this.horizontalSplitter.Height);
        }
        // resize images and panels 
        this.resizePanelsToHorizontalSplitter();
        this.resizePanelsToVerticalSplitter();
        this.lastHeight = this.clientHeight;
        this.lastWidth = this.clientWidth;
        if (windowLock) {
            UNRESOLVED.lockWindowUpdate(0);
        }
        this.horizontalSplitter.Visible = true;
        this.verticalSplitter.Visible = true;
        this.plantListPanel.Visible = true;
        this.plantFocusPanel.Visible = true;
    }
    
    // resizing 
    public void resizePanelsToVerticalSplitter() {
        short newLeft = 0;
        short newWidth = 0;
        short newTop = 0;
        short newHeight = 0;
        
        newLeft = this.verticalSplitter.Left + this.verticalSplitter.Width;
        newWidth = umath.intMax(0, this.clientWidth - newLeft);
        newTop = this.horizontalSplitter.Top + this.horizontalSplitter.Height;
        newHeight = umath.intMax(0, this.clientHeight - newTop);
        if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal) {
            this.plantListPanel.SetBounds(0, newTop, this.verticalSplitter.Left, newHeight);
            this.plantFocusPanel.SetBounds(newLeft, newTop, newWidth, newHeight);
        } else if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical) {
            this.plantListPanel.SetBounds(newLeft, this.toolbarPanel.Height, newWidth, this.horizontalSplitter.Top - this.toolbarPanel.Height);
            this.plantFocusPanel.SetBounds(newLeft, newTop, newWidth, newHeight);
            //don't change top here
            this.horizontalSplitter.SetBounds(newLeft, this.horizontalSplitter.Top, newWidth, this.horizontalSplitter.Height);
            this.drawingPaintBox.SetBounds(0, this.toolbarPanel.Height, newLeft, umath.intMax(0, this.clientHeight - this.toolbarPanel.Height));
            this.resizeDrawingBitmapIfNecessary();
        }
        this.resizePlantListPanel();
        this.resizePlantFocusPanel();
    }
    
    public void resizePanelsToHorizontalSplitter() {
        short newLeft = 0;
        short newWidth = 0;
        short newTop = 0;
        short newHeight = 0;
        
        newLeft = this.verticalSplitter.Left + this.verticalSplitter.Width;
        newWidth = umath.intMax(0, this.clientWidth - newLeft);
        newTop = this.horizontalSplitter.Top + this.horizontalSplitter.Height;
        newHeight = umath.intMax(0, this.clientHeight - newTop);
        if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal) {
            this.plantListPanel.SetBounds(0, newTop, this.verticalSplitter.Left, newHeight);
            //don't change left here
            this.verticalSplitter.SetBounds(this.verticalSplitter.Left, newTop, this.verticalSplitter.Width, newHeight);
            this.plantFocusPanel.SetBounds(newLeft, newTop, newWidth, newHeight);
            this.drawingPaintBox.SetBounds(0, this.toolbarPanel.Height, this.clientWidth, umath.intMax(0, this.horizontalSplitter.Top - this.toolbarPanel.Height));
            this.resizeDrawingBitmapIfNecessary();
        } else if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical) {
            this.plantListPanel.SetBounds(newLeft, this.toolbarPanel.Height, newWidth, this.horizontalSplitter.Top - this.toolbarPanel.Height);
            this.plantFocusPanel.SetBounds(newLeft, newTop, newWidth, newHeight);
        }
        this.resizePlantListPanel();
        this.resizePlantFocusPanel();
    }
    
    public void resizeDrawingBitmapIfNecessary() {
        boolean bitmapWasMadeBigger = false;
        
        if ((this.drawingBitmap.Width != this.drawingPaintBox.Width) || (this.drawingBitmap.Height != this.drawingPaintBox.Height)) {
            // if have to make bitmap larger, redraw all plants in case some were not drawing before
            // because they were off the bitmap
            bitmapWasMadeBigger = (this.drawingPaintBox.Width > this.drawingBitmap.Width) || (this.drawingPaintBox.Height > this.drawingBitmap.Height);
            UNRESOLVED.resizeBitmap(this.drawingBitmap, Point(this.drawingPaintBox.Width, this.drawingPaintBox.Height));
            if (!this.inFormCreation) {
                if (bitmapWasMadeBigger) {
                    this.recalculateAllPlantBoundsRects(kDontDrawYet);
                }
                this.invalidateEntireDrawing();
                this.updateForPossibleChangeToDrawing();
            }
        }
    }
    
    public void resizePlantListPanel() {
        this.plantListDrawGrid.SetBounds(0, 0, this.plantListPanel.Width, this.plantListPanel.Height - this.plantFileChangedImage.Height - kBetweenGap * 2);
        this.plantListDrawGrid.DefaultColWidth = this.plantListDrawGrid.ClientWidth;
        this.plantFileChangedImage.SetBounds(kBetweenGap, this.plantListDrawGrid.Top + this.plantListDrawGrid.Height + kBetweenGap, this.plantFileChangedImage.Width, this.plantFileChangedImage.Height);
        this.plantBitmapsIndicatorImage.SetBounds(this.plantFileChangedImage.Left + this.plantFileChangedImage.Width + kBetweenGap, this.plantFileChangedImage.Top, this.plantBitmapsIndicatorImage.Width, this.plantBitmapsIndicatorImage.Height);
        this.progressPaintBox.SetBounds(this.plantBitmapsIndicatorImage.Left + this.plantBitmapsIndicatorImage.Width + kBetweenGap, this.plantBitmapsIndicatorImage.Top + this.plantBitmapsIndicatorImage.Height / 2 - this.progressPaintBox.Height / 2, this.plantListPanel.Width - this.plantFileChangedImage.Width - this.plantBitmapsIndicatorImage.Width - kBetweenGap * 4, this.progressPaintBox.Height);
    }
    
    public void resizePlantFocusPanel() {
        int newTop = 0;
        
        //FIX unresolved WITH expression: self.tabSet
        // tab set 
        UNRESOLVED.setBounds(0, this.plantFocusPanel.Height - UNRESOLVED.height, this.plantFocusPanel.Width, UNRESOLVED.height);
        // v1.4 change
        this.animatingLabel.SetBounds(umath.intMax(0, this.plantFocusPanel.Width - this.animatingLabel.Width - kBetweenGap), this.plantFocusPanel.Height - this.animatingLabel.Height - kBetweenGap, this.animatingLabel.Width, this.animatingLabel.Height);
        // life cycle panel 
        this.lifeCyclePanel.SetBounds(0, 0, this.plantFocusPanel.Width, umath.intMax(0, this.plantFocusPanel.Height - this.tabSet.height));
        // v1.4 change - 2
        this.lifeCycleEditPanel.Height = this.animateGrowth.Height + kBetweenGap * 2 - 2;
        // v1.4 change +1, -1, -2
        this.lifeCycleEditPanel.SetBounds(1, umath.intMax(0, this.lifeCyclePanel.Height - this.lifeCycleEditPanel.Height - 1), this.lifeCyclePanel.Width - 2, this.lifeCycleEditPanel.Height);
        // rotations panel
        this.rotationsPanel.SetBounds(0, 0, this.lifeCyclePanel.Width, this.lifeCyclePanel.Height);
        // posing panel
        this.posingPanel.SetBounds(0, 0, this.lifeCyclePanel.Width, this.lifeCyclePanel.Height);
        newTop = this.posingPlantName.Top + this.posingPlantName.Height + kBetweenGap;
        this.posingNotShown.SetBounds(this.posingPanel.Width - this.posingNotShown.Width - kBetweenGap, newTop, this.posingNotShown.Width, this.posingNotShown.Height);
        this.posingGhost.SetBounds(this.posingNotShown.Left - this.posingGhost.Width - kBetweenGap, newTop, this.posingGhost.Width, this.posingGhost.Height);
        this.posingHighlight.SetBounds(this.posingGhost.Left - this.posingHighlight.Width - kBetweenGap, newTop, this.posingHighlight.Width, this.posingHighlight.Height);
        newTop = this.posingNotShown.Top + this.posingNotShown.Height + kBetweenGap;
        this.posedPartsLabel.SetBounds(kBetweenGap, newTop + (this.posedPlantParts.Height / 2 - this.posedPartsLabel.Height / 2), this.posedPartsLabel.Width, this.posedPartsLabel.Height);
        this.posedPlantParts.SetBounds(this.posedPartsLabel.Left + this.posedPartsLabel.Width + kBetweenGap, newTop, umath.intMax(10, this.posingPanel.Width - this.posedPartsLabel.Width - kBetweenGap * 3), this.posedPlantParts.Height);
        newTop = this.posedPlantParts.Top + this.posedPlantParts.Height + kBetweenGap;
        // fix later
        this.selectedPartLabel.SetBounds(kBetweenGap, newTop + (this.posingUnposePart.Height / 2 - this.selectedPartLabel.Height / 2), this.selectedPartLabel.Width, this.selectedPartLabel.Height);
        newTop = this.selectedPartLabel.Top + this.selectedPartLabel.Height + kBetweenGap;
        this.posingPosePart.SetBounds(kBetweenGap, newTop, this.posingPosePart.Width, this.posingPosePart.Height);
        this.posingUnposePart.SetBounds(this.posingPosePart.Left + this.posingPosePart.Width + kBetweenGap, newTop, this.posingUnposePart.Width, this.posingUnposePart.Height);
        newTop = this.posingUnposePart.Top + this.posingUnposePart.Height + kBetweenGap;
        this.posingDetailsPanel.SetBounds(0, newTop, this.lifeCyclePanel.Width, umath.intMax(230, this.lifeCyclePanel.Height - newTop));
        // lifeCycleEditPanel 
        this.lifeCycleDaysEdit.SetBounds(this.ageAndSizeLabel.Width + kBetweenGap * 2, kBetweenGap, this.lifeCycleDaysEdit.Width, this.lifeCycleDaysEdit.Height);
        this.lifeCycleDaysSpin.SetBounds(this.lifeCycleDaysEdit.Left + this.lifeCycleDaysEdit.Width, kBetweenGap + this.lifeCycleDaysEdit.Height / 2 - this.lifeCycleDaysSpin.Height / 2, this.lifeCycleDaysSpin.Width, this.lifeCycleDaysSpin.Height);
        this.ageAndSizeLabel.SetBounds(kBetweenGap, umath.intMax(0, this.lifeCycleDaysEdit.Top + this.lifeCycleDaysEdit.Height / 2 - this.ageAndSizeLabel.Height / 2), this.ageAndSizeLabel.Width, this.ageAndSizeLabel.Height);
        this.daysAndSizeLabel.SetBounds(this.lifeCycleDaysSpin.Left + this.lifeCycleDaysSpin.Width + kBetweenGap, umath.intMax(0, this.lifeCycleDaysEdit.Top + this.lifeCycleDaysEdit.Height / 2 - this.daysAndSizeLabel.Height / 2), this.daysAndSizeLabel.Width, this.daysAndSizeLabel.Height);
        this.animateGrowth.SetBounds(this.lifeCycleEditPanel.Width - this.animateGrowth.Width - kBetweenGap, this.lifeCycleDaysEdit.Top, this.animateGrowth.Width, this.animateGrowth.Height);
        // above lifeCycleEditPanel 
        this.timeLabel.SetBounds(umath.intMax(0, this.lifeCyclePanel.Width / 2 - this.timeLabel.Width / 2), umath.intMax(0, this.lifeCycleEditPanel.Top - this.timeLabel.Height - kBetweenGap), this.timeLabel.Width, this.timeLabel.Height);
        this.lifeCycleGraphImage.SetBounds(kBetweenGap + this.maxSizeAxisLabel.Width + kBetweenGap, umath.intMax(1, this.selectedPlantNameLabel.Top + this.selectedPlantNameLabel.Height + kBetweenGap), umath.intMax(1, this.lifeCyclePanel.Width - this.maxSizeAxisLabel.Width - kBetweenGap * 3), umath.intMax(1, this.timeLabel.Top - this.selectedPlantNameLabel.Height - kBetweenGap * 2));
        this.maxSizeAxisLabel.SetBounds(kBetweenGap, umath.intMax(0, this.lifeCycleGraphImage.Top + this.lifeCycleGraphImage.Height / 2 - this.maxSizeAxisLabel.Height / 2), this.maxSizeAxisLabel.Width, this.maxSizeAxisLabel.Height);
        this.selectedPlantNameLabel.SetBounds(kBetweenGap, kBetweenGap, this.selectedPlantNameLabel.Width, this.selectedPlantNameLabel.Height);
        if ((this.lifeCycleGraphImage.Picture.Bitmap.Width != this.lifeCycleGraphImage.Width) || (this.lifeCycleGraphImage.Picture.Bitmap.Height != this.lifeCycleGraphImage.Height)) {
            // with selectedPlantNameLabel do setBounds(lifeCycleGraphImage.left, kBetweenGap, width, height);
            UNRESOLVED.resizeBitmap(this.lifeCycleGraphImage.Picture.Bitmap, Point(this.lifeCycleGraphImage.Width, this.lifeCycleGraphImage.Height));
        }
        this.placeLifeCycleDragger();
        this.redrawLifeCycleGraph();
        this.resizeParametersPanel();
        // stats scroll box 
        this.statsScrollBox.SetBounds(0, 0, this.plantFocusPanel.Width, umath.intMax(0, this.plantFocusPanel.Height - this.tabSet.height));
        this.statsPanel.resizeElements;
        this.notePanel.SetBounds(0, 0, this.plantFocusPanel.Width, umath.intMax(0, this.plantFocusPanel.Height - this.tabSet.height));
        this.noteLabel.SetBounds(kBetweenGap, kBetweenGap, this.noteLabel.Width, this.noteLabel.Height);
        //kBetweenGap + noteEdit.height div 2 - height div 2, width, height);
        this.noteEdit.SetBounds(umath.intMax(0, this.notePanel.Width - this.noteEdit.Width - kBetweenGap), kBetweenGap, this.noteEdit.Width, this.noteEdit.Height);
        this.noteMemo.SetBounds(0, this.noteEdit.Height + kBetweenGap * 2, this.notePanel.Width, umath.intMax(0, this.notePanel.Height - this.noteEdit.Height - kBetweenGap * 2));
    }
    
    public void resizeParametersPanel() {
        short newTop = 0;
        
        this.parametersPanel.SetBounds(0, 0, this.plantFocusPanel.Width, umath.intMax(0, this.plantFocusPanel.Height - this.tabSet.height));
        this.parametersPlantName.SetBounds(kBetweenGap, kBetweenGap, this.parametersPlantName.Width, this.parametersPlantName.Height);
        this.sectionsComboBox.SetBounds(kBetweenGap, this.parametersPlantName.Top + this.parametersPlantName.Height + kBetweenGap, this.parametersPanel.Width - kBetweenGap * 2, this.sectionsComboBox.Height);
        newTop = this.sectionsComboBox.Top + this.sectionsComboBox.Height + kBetweenGap;
        this.parametersScrollBox.SetBounds(0, this.sectionsComboBox.Top + this.sectionsComboBox.Height + kBetweenGap, this.parametersPanel.Width, this.parametersPanel.Height - newTop);
        this.repositionParameterPanels();
    }
    
    public void placeLifeCycleDragger() {
        PdPlant firstPlant = new PdPlant();
        float fractionOfMaxAge = 0.0;
        
        firstPlant = this.focusedPlant();
        fractionOfMaxAge = 0.0;
        if (firstPlant != null) {
            try {
                fractionOfMaxAge = firstPlant.age / firstPlant.pGeneral.ageAtMaturity;
            } catch (Exception e) {
                fractionOfMaxAge = 0.0;
            }
        }
        this.lifeCycleDragger.SetBounds(this.lifeCycleGraphImage.Left + intround((this.lifeCycleGraphImage.Width - this.lifeCycleDragger.Width) * fractionOfMaxAge), this.lifeCycleGraphImage.Top + 1, this.lifeCycleDragger.Width, this.lifeCycleGraphImage.Height - 2);
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 300;
        UNRESOLVED.ptMinTrackSize.y = 300;
    }
    
    // ------------------------------------------------------------------------------------- *splitting 
    public void horizontalSplitterMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.horizontalSplitterDragging = true;
        this.horizontalSplitterStartPos = Y;
        this.horizontalSplitterLastDrawPos = -1;
        this.horizontalSplitterNeedToRedraw = true;
    }
    
    public void horizontalSplitterMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        int bottomLimit = 0;
        
        if (udomain.domain == null) {
            return;
        }
        if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal) {
            bottomLimit = kSplitterDragToBottomMinPixelsInHorizMode;
        } else if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical) {
            bottomLimit = kSplitterDragToBottomMinPixelsInVertMode;
        } else {
            bottomLimit = kSplitterDragToBottomMinPixelsInHorizMode;
        }
        if (this.horizontalSplitterDragging && (this.horizontalSplitter.Top + Y >= kSplitterDragToTopMinPixels) && (this.horizontalSplitter.Top + Y < this.clientHeight - bottomLimit)) {
            this.undrawHorizontalSplitterLine();
            this.horizontalSplitterLastDrawPos = this.drawHorizontalSplitterLine(Y);
        }
    }
    
    public void horizontalSplitterMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        int bottomLimit = 0;
        
        if (udomain.domain == null) {
            return;
        }
        if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationHorizontal) {
            bottomLimit = kSplitterDragToBottomMinPixelsInHorizMode;
        } else if (udomain.domain.options.mainWindowOrientation == udomain.kMainWindowOrientationVertical) {
            bottomLimit = kSplitterDragToBottomMinPixelsInVertMode;
        } else {
            bottomLimit = kSplitterDragToBottomMinPixelsInHorizMode;
        }
        if (this.horizontalSplitterDragging) {
            this.undrawHorizontalSplitterLine();
            this.horizontalSplitter.Top = this.horizontalSplitter.Top - (this.horizontalSplitterStartPos - Y);
            if (this.horizontalSplitter.Top < kSplitterDragToTopMinPixels) {
                this.horizontalSplitter.Top = kSplitterDragToTopMinPixels;
            }
            if (this.horizontalSplitter.Top > this.clientHeight - bottomLimit) {
                this.horizontalSplitter.Top = this.clientHeight - bottomLimit;
            }
            this.resizePanelsToHorizontalSplitter();
            this.horizontalSplitterDragging = false;
        }
    }
    
    // splitting 
    public int drawHorizontalSplitterLine(int pos) {
        result = 0;
        HDC theDC = new HDC();
        
        theDC = UNRESOLVED.getDC(0);
        result = this.clientOrigin.y + this.horizontalSplitter.Top + pos + 2;
        UNRESOLVED.patBlt(theDC, this.clientOrigin.x + this.horizontalSplitter.Left, result, this.horizontalSplitter.Width, 1, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.horizontalSplitterNeedToRedraw = true;
        return result;
    }
    
    public void undrawHorizontalSplitterLine() {
        HDC theDC = new HDC();
        
        if (!this.horizontalSplitterNeedToRedraw) {
            return;
        }
        theDC = UNRESOLVED.getDC(0);
        UNRESOLVED.patBlt(theDC, this.clientOrigin.x + this.horizontalSplitter.Left, this.horizontalSplitterLastDrawPos, this.horizontalSplitter.Width, 1, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.horizontalSplitterNeedToRedraw = false;
    }
    
    public void verticalSplitterMouseDown(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.verticalSplitterDragging = true;
        this.verticalSplitterStartPos = X;
        this.verticalSplitterLastDrawPos = -1;
        this.verticalSplitterNeedToRedraw = true;
    }
    
    public void verticalSplitterMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        if (this.verticalSplitterDragging && (this.verticalSplitter.Left + X >= kSplitterDragToLeftMinPixels) && (this.verticalSplitter.Left + X < this.clientWidth - kSplitterDragToRightMinPixels)) {
            this.undrawVerticalSplitterLine();
            this.verticalSplitterLastDrawPos = this.drawVerticalSplitterLine(X);
        }
    }
    
    public void verticalSplitterMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        if (this.verticalSplitterDragging) {
            this.undrawVerticalSplitterLine();
            this.verticalSplitter.Left = this.verticalSplitter.Left - (this.verticalSplitterStartPos - X);
            if (this.verticalSplitter.Left < kSplitterDragToLeftMinPixels) {
                this.verticalSplitter.Left = kSplitterDragToLeftMinPixels;
            }
            if (this.verticalSplitter.Left > this.clientWidth - kSplitterDragToRightMinPixels) {
                this.verticalSplitter.Left = this.clientWidth - kSplitterDragToRightMinPixels;
            }
            this.resizePanelsToVerticalSplitter();
            this.verticalSplitterDragging = false;
        }
    }
    
    public int drawVerticalSplitterLine(int pos) {
        result = 0;
        HDC theDC = new HDC();
        
        theDC = UNRESOLVED.getDC(0);
        result = this.clientOrigin.x + this.verticalSplitter.Left + pos + 2;
        UNRESOLVED.patBlt(theDC, result, this.clientOrigin.y + this.verticalSplitter.Top, 1, this.verticalSplitter.Height, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.verticalSplitterNeedToRedraw = true;
        return result;
    }
    
    public void undrawVerticalSplitterLine() {
        HDC theDC = new HDC();
        
        if (!this.verticalSplitterNeedToRedraw) {
            return;
        }
        theDC = UNRESOLVED.getDC(0);
        UNRESOLVED.patBlt(theDC, this.verticalSplitterLastDrawPos, this.clientOrigin.y + this.verticalSplitter.Top, 1, this.verticalSplitter.Height, delphi_compatability.DSTINVERT);
        UNRESOLVED.releaseDC(0, theDC);
        this.verticalSplitterNeedToRedraw = false;
    }
    
    // palette stuff 
    // ----------------------------------------------------------------------------- *palette stuff 
    public HPALETTE GetPalette() {
        result = new HPALETTE();
        result = this.paletteImage.Picture.Bitmap.Palette;
        return result;
    }
    
    //overriden because paint box will not update correctly
    //makes window take first priority for palettes
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
            if ((UNRESOLVED.realizePalette(DC) != 0) && (!delphi_compatability.Application.terminated) && (this.drawingPaintBox != null)) {
                // if palette changed, repaint drawing 
                UNRESOLVED.setPixelFormatBasedOnScreenForBitmap(this.drawingBitmap);
                this.drawingPaintBox.Invalidate();
            }
            if (this.statsPanel != null) {
                this.statsPanel.invalidate;
            }
            UNRESOLVED.selectPalette(DC, oldPalette, true);
            UNRESOLVED.realizePalette(DC);
            UNRESOLVED.releaseDC(windowHandle, DC);
        }
        result = super.PaletteChanged(Foreground);
        return result;
    }
    
    public void FormShow(TObject Sender) {
        UNRESOLVED.DragAcceptFiles(UNRESOLVED.Handle, true);
    }
    
    // v1.11
    public void Reconcile3DObjects1Click(TObject Sender) {
        int response = 0;
        int numTdosAdded = 0;
        
        numTdosAdded = 0;
        if (plantFileChanged) {
            // ask if want to save file first
            response = MessageDialog("Do you want to save your changes to " + ExtractFileName(udomain.domain.plantFileName) + chr(13) + "before you reconcile its 3D objects" + chr(13) + "with those in the current 3D object file?", mtConfirmation, mbYesNoCancel, 0);
            switch (response) {
                case delphi_compatability.IDCANCEL:
                    return;
                    break;
                case delphi_compatability.IDYES:
                    this.MenuFileSaveClick(this);
                    break;
                case delphi_compatability.IDNO:
                    break;
        }
        if (!udomain.domain.checkForExistingDefaultTdoLibrary()) {
            return;
        }
        if (MessageDialog("You are about to add any 3D objects in the current plant file" + chr(13) + chr(13) + "    (" + udomain.domain.plantFileName + ")" + chr(13) + chr(13) + "that are not already in the current 3D object library" + chr(13) + chr(13) + "    (" + udomain.domain.defaultTdoLibraryFileName + ")" + chr(13) + chr(13) + "into that library. Do you want to go ahead?", mtConfirmation, {mbYes, mbNo, }, 0) == delphi_compatability.IDYES) {
            numTdosAdded = udomain.domain.plantManager.reconcileFileWithTdoLibrary(udomain.domain.plantFileName, udomain.domain.defaultTdoLibraryFileName);
            if (numTdosAdded <= 0) {
                MessageDialog("All the 3D objects in the current plant file" + chr(13) + chr(13) + "    (" + udomain.domain.plantFileName + ")" + chr(13) + chr(13) + "were already in the current 3D object library" + chr(13) + chr(13) + "    (" + udomain.domain.defaultTdoLibraryFileName + ").", mtInformation, {mbOK, }, 0);
            } else {
                MessageDialog(IntToStr(numTdosAdded) + " 3D objects from the current plant file" + chr(13) + chr(13) + "    (" + udomain.domain.plantFileName + ")" + chr(13) + chr(13) + "were copied to the current 3D object library" + chr(13) + chr(13) + "    (" + udomain.domain.defaultTdoLibraryFileName + ").", mtInformation, {mbOK, }, 0);
            }
        }
    }
    
    // v1.60
    // end v1.11
    // v1.60 recent files menu
    // PDF PORT removed empty parens
    public void updateFileMenuForOtherRecentFiles() {
        short i = 0;
        short numSet = 0;
        String shortcutString = "";
        boolean atLeastOneFileNameExists = false;
        boolean showThis = false;
        
        atLeastOneFileNameExists = false;
        numSet = 0;
        for (i = 0; i <= udomain.kMaxRecentFiles - 1; i++) {
            if (numSet + 1 == 10) {
                shortcutString = "1&0";
            } else {
                shortcutString = "&" + IntToStr(numSet + 1);
            }
            this.MenuFileReopen.items[i].caption = shortcutString + " " + udomain.domain.options.recentFiles[udomain.kMaxRecentFiles - 1 - i];
            showThis = (udomain.domain.options.recentFiles[udomain.kMaxRecentFiles - 1 - i] != "") && (FileExists(udomain.domain.options.recentFiles[udomain.kMaxRecentFiles - 1 - i]));
            this.MenuFileReopen.items[i].visible = showThis;
            if (showThis) {
                numSet += 1;
            }
            if (!atLeastOneFileNameExists) {
                atLeastOneFileNameExists = showThis;
            }
        }
        this.MenuFileReopen.enabled = atLeastOneFileNameExists;
    }
    
    // v1.60 recent files menu
    public void Recent0Click(TObject Sender) {
        short index = 0;
        
        index = udomain.kMaxRecentFiles - 1 - this.MenuFileReopen.indexOf((UNRESOLVED.TMenuItem)Sender);
        if (!FileExists(udomain.domain.options.recentFiles[index])) {
            MessageDialog("Cannot find the file" + chr(13) + udomain.domain.options.recentFiles[index] + ".", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            return;
        }
        if (!this.askForSaveAndProceed()) {
            return;
        }
        this.openFile(udomain.domain.options.recentFiles[index]);
    }
    
}
