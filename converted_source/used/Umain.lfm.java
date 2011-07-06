
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class MainWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    ImagePanel paletteImage;
    ImagePanel visibleBitmap;
    ImagePanel paramPanelOpenArrowImage;
    ImagePanel paramPanelClosedArrowImage;
    ImagePanel fileChangedImage;
    ImagePanel fileNotChangedImage;
    ImagePanel unregisteredExportReminder;
    ImagePanel plantBitmapsGreenImage;
    ImagePanel noPlantBitmapsImage;
    ImagePanel plantBitmapsYellowImage;
    ImagePanel plantBitmapsRedImage;
    JPanel posingColorsPanel;
    JLabel posingLineColorLabel;
    JLabel posingFrontfaceColorLabel;
    JLabel posingBackfaceColorLabel;
    JCheckBox posingChangeColors;
    JCheckBox posingChangeAllColorsAfter;
    JPanel posingLineColor;
    JPanel posingFrontfaceColor;
    JPanel posingBackfaceColor;
    JPanel horizontalSplitter;
    JPanel verticalSplitter;
    JPanel toolbarPanel;
    SpeedButton dragCursorMode;
    SpeedButton magnifyCursorMode;
    SpeedButton scrollCursorMode;
    SpeedButton rotateCursorMode;
    SpeedButton centerDrawing;
    SpeedButton viewFreeFloating;
    SpeedButton viewOneOnly;
    SpeedButton drawingAreaOnTop;
    SpeedButton drawingAreaOnSide;
    SpeedButton posingSelectionCursorMode;
    JComboBox magnificationPercent;
    JPanel plantListPanel;
    // UNHANDLED_TYPE progressPaintBox;
    ImagePanel plantFileChangedImage;
    ImagePanel plantBitmapsIndicatorImage;
    JTable plantListDrawGrid;
    JPanel sectionImagesPanel;
    ImagePanel Sections_FlowersPrimary;
    ImagePanel Sections_General;
    ImagePanel Sections_InflorPrimary;
    ImagePanel Sections_Meristems;
    ImagePanel Sections_Leaves;
    ImagePanel Sections_RootTop;
    ImagePanel Sections_Fruit;
    ImagePanel Sections_InflorSecondary;
    ImagePanel Sections_Internodes;
    ImagePanel Sections_SeedlingLeaves;
    ImagePanel Sections_FlowersSecondary;
    ImagePanel Sections_FlowersPrimaryAdvanced;
    ImagePanel Sections_Orthogonal;
    JTextArea plantsAsTextMemo;
    JPanel plantFocusPanel;
    JLabel animatingLabel;
    JPanel lifeCyclePanel;
    ImagePanel lifeCycleGraphImage;
    JLabel timeLabel;
    JLabel selectedPlantNameLabel;
    JLabel maxSizeAxisLabel;
    JPanel lifeCycleEditPanel;
    JLabel daysAndSizeLabel;
    JLabel ageAndSizeLabel;
    SpeedButton animateGrowth;
    JTextField lifeCycleDaysEdit;
    SpinButton lifeCycleDaysSpin;
    JPanel lifeCycleDragger;
    JPanel statsScrollBox;
    // UNHANDLED_TYPE tabSet;
    JPanel parametersPanel;
    JLabel parametersPlantName;
    JPanel parametersScrollBox;
    JComboBox sectionsComboBox;
    JPanel rotationsPanel;
    JLabel xRotationLabel;
    JLabel yRotationLabel;
    JLabel zRotationLabel;
    SpeedButton resetRotations;
    JLabel rotationLabel;
    JLabel sizingLabel;
    JLabel drawingScalePixelsPerMmLabel;
    SpeedButton packPlants;
    JLabel locationLabel;
    JLabel xLocationLabel;
    JLabel yLocationLabel;
    JLabel locationPixelsLabel;
    JLabel arrangementPlantName;
    SpeedButton alignTops;
    SpeedButton alignBottoms;
    SpeedButton alignLeft;
    SpeedButton alignRight;
    SpeedButton makeEqualWidth;
    SpeedButton makeEqualHeight;
    JTextField xRotationEdit;
    SpinButton xRotationSpin;
    JTextField yRotationEdit;
    SpinButton yRotationSpin;
    JTextField zRotationEdit;
    SpinButton zRotationSpin;
    JTextField drawingScaleEdit;
    SpinButton drawingScaleSpin;
    JTextField xLocationEdit;
    SpinButton xLocationSpin;
    JTextField yLocationEdit;
    SpinButton yLocationSpin;
    JPanel notePanel;
    JLabel noteLabel;
    SpeedButton noteEdit;
    JTextArea noteMemo;
    JPanel posingPanel;
    JLabel posingPlantName;
    JLabel posedPartsLabel;
    SpeedButton posingHighlight;
    SpeedButton posingGhost;
    SpeedButton posingNotShown;
    JLabel selectedPartLabel;
    SpeedButton posingPosePart;
    SpeedButton posingUnposePart;
    JPanel posingDetailsPanel;
    JLabel posingXRotationLabel;
    JLabel posingYRotationLabel;
    JLabel posingZRotationLabel;
    JLabel posingScaleMultiplierPercent;
    JLabel posingScaleMultiplierLabel;
    JLabel posingLengthMultiplierPercent;
    JLabel posingLengthMultiplierLabel;
    JLabel posingWidthMultiplierPercent;
    JLabel posingWidthMultiplierLabel;
    JLabel hideExtraLabel;
    JLabel rotationDegreesLabel;
    JLabel posingMultiplyScaleAllPartsAfterLabel;
    JCheckBox posingHidePart;
    JTextField posingXRotationEdit;
    SpinButton posingXRotationSpin;
    JTextField posingYRotationEdit;
    SpinButton posingYRotationSpin;
    JTextField posingZRotationEdit;
    SpinButton posingZRotationSpin;
    JCheckBox posingAddExtraRotation;
    JCheckBox posingMultiplyScale;
    JCheckBox posingMultiplyScaleAllPartsAfter;
    JTextField posingScaleMultiplierEdit;
    SpinButton posingScaleMultiplierSpin;
    JTextField posingLengthMultiplierEdit;
    SpinButton posingLengthMultiplierSpin;
    JTextField posingWidthMultiplierEdit;
    SpinButton posingWidthMultiplierSpin;
    JComboBox posedPlantParts;
    JMenuBar MainMenu;
    JMenu MenuFile;
    JMenuItem MenuFileNew;
    JMenuItem MenuFileOpen;
    JMenu MenuFileReopen;
    JMenuItem Recent0;
    JMenuItem Recent1;
    JMenuItem Recent2;
    JMenuItem Recent3;
    JMenuItem Recent4;
    JMenuItem Recent5;
    JMenuItem Recent6;
    JMenuItem Recent7;
    JMenuItem Recent8;
    JMenuItem Recent9;
    JMenuItem MenuFileClose;
    JMenuItem N1;
    JMenuItem MenuFileSave;
    JMenuItem MenuFileSaveAs;
    JMenuItem N22;
    JMenu MenuFileExport;
    JMenuItem MenuPlantExportTo3DS;
    JMenuItem MenuPlantExportToLWO;
    JMenuItem MenuPlantExportToOBJ;
    JMenuItem MenuPlantExportToDXF;
    JMenuItem MenuPlantExportToPOV;
    JMenuItem MenuPlantExportToVRML;
    JMenuItem N9;
    JMenuItem MenuFileSaveDrawingAs;
    JMenuItem MenuFileSaveJPEG;
    JRadioButtonMenuItem MenuFileMakePainterNozzle;
    JMenuItem MenuFileMakePainterAnimation;
    JMenu MenuFileMove;
    JMenuItem MenuFilePlantMover;
    JMenuItem MenuFileTdoMover;
    JMenuItem Reconcile3DObjects1;
    JMenuItem N10;
    JMenuItem MenuFilePrintDrawing;
    JMenuItem N2;
    JMenuItem MenuFileExit;
    JMenu MenuEdit;
    JMenuItem MenuEditUndo;
    JMenuItem MenuEditRedo;
    JMenuItem UndoMenuEditUndoRedoList;
    JMenuItem N3;
    JMenuItem MenuEditCut;
    JMenuItem MenuEditCopy;
    JMenuItem MenuEditPaste;
    JMenuItem MenuEditDelete;
    JMenuItem MenuEditDuplicate;
    JMenuItem N16;
    JMenuItem MenuEditCopyDrawing;
    JMenuItem MenuEditCopyAsText;
    JMenuItem MenuEditPasteAsText;
    JMenuItem N5;
    JMenuItem MenuEditPreferences;
    JMenu MenuPlant;
    JMenuItem MenuPlantNew;
    JMenuItem MenuPlantNewUsingLastWizardSettings;
    JMenuItem N7;
    JMenuItem MenuPlantBreed;
    JMenuItem MenuPlantMakeTimeSeries;
    JMenuItem N20;
    JMenuItem MenuPlantRandomize;
    JMenuItem MenuPlantZeroRotations;
    JMenuItem MenuPlantAnimate;
    JMenuItem N21;
    JMenuItem MenuPlantRename;
    JMenuItem MenuPlantEditNote;
    JMenu MenuLayout;
    JMenuItem MenuLayoutSelectAll;
    JMenuItem MenuLayoutDeselect;
    JMenuItem N18;
    JMenuItem MenuLayoutScaleToFit;
    JMenu MenuLayoutAlign;
    JMenuItem MenuLayoutAlignTops;
    JMenuItem MenuLayoutAlignBottoms;
    JMenuItem MenuLayoutAlignLeftSides;
    JMenuItem MenuLayoutAlignRightSides;
    JMenuItem MenuLayoutMakeBouquet;
    JMenu MenuLayoutSize;
    JMenuItem MenuLayoutSizeSameWidth;
    JMenuItem MenuLayoutSizeSameHeight;
    JMenuItem MenuLayoutPack;
    JMenuItem N8;
    JMenuItem MenuLayoutBringForward;
    JMenuItem MenuLayoutSendBack;
    JMenuItem N19;
    JMenuItem MenuLayoutShow;
    JMenuItem MenuLayoutHide;
    JMenuItem MenuLayoutHideOthers;
    JMenu MenuOptions;
    JMenu MenuOptionsDrawAs;
    JRadioButtonMenuItem MenuOptionsFastDraw;
    JRadioButtonMenuItem MenuOptionsMediumDraw;
    JRadioButtonMenuItem MenuOptionsBestDraw;
    JRadioButtonMenuItem MenuOptionsCustomDraw;
    JMenu MenuLayoutView;
    JRadioButtonMenuItem MenuLayoutViewFreeFloating;
    JRadioButtonMenuItem MenuLayoutViewOnePlantAtATime;
    JMenu MenuLayoutDrawingAreaOn;
    JRadioButtonMenuItem MenuLayoutHorizontalOrientation;
    JRadioButtonMenuItem MenuLayoutVerticalOrientation;
    JMenu MenuOptionsDrawRectangles;
    JRadioButtonMenuItem MenuOptionsShowSelectionRectangles;
    JRadioButtonMenuItem MenuOptionsShowBoundsRectangles;
    JMenu MenuOptionsPosing;
    JRadioButtonMenuItem MenuOptionsHighlightPosedParts;
    JRadioButtonMenuItem MenuOptionsGhostHiddenParts;
    JRadioButtonMenuItem MenuOptionsHidePosing;
    JMenu MenuOptionsHints;
    JRadioButtonMenuItem MenuOptionsShowLongButtonHints;
    JRadioButtonMenuItem MenuOptionsShowParameterHints;
    JRadioButtonMenuItem N17;
    JRadioButtonMenuItem MenuOptionsUsePlantBitmaps;
    JMenu MenuWindow;
    JMenuItem MenuWindowBreeder;
    JMenuItem MenuWindowTimeSeries;
    JMenuItem N12;
    JMenuItem MenuWindowNumericalExceptions;
    JMenu MenuHelp;
    JMenuItem MenuHelpTopics;
    JMenuItem MenuHelpSuperSpeedTour;
    JMenuItem MenuHelpTutorial;
    JMenuItem N13;
    JMenuItem MenuHelpRegister;
    JMenuItem AfterRegisterMenuSeparator;
    JMenuItem MenuHelpAbout;
    JPopupMenu PlantPopupMenu;
    JMenuItem PopupMenuRandomize;
    JMenuItem N4;
    JMenuItem PopupMenuCut;
    JMenuItem PopupMenuCopy;
    JMenuItem PopupMenuPaste;
    JMenuItem N6;
    JMenuItem PopupMenuRename;
    JMenuItem PopupMenuEditNote;
    JMenuItem PopupMenuAnimate;
    JMenuItem PopupMenuBreed;
    JMenuItem PopupMenuMakeTimeSeries;
    JMenuItem PopupMenuZeroRotations;
    // UNHANDLED_TYPE PrintDialog;
    // UNHANDLED_TYPE animateTimer;
    JPopupMenu paramPopupMenu;
    JMenuItem paramPopupMenuExpand;
    JMenuItem paramPopupMenuCollapse;
    JMenuItem N11;
    JMenuItem paramPopupMenuExpandAllInSection;
    JMenuItem paramPopupMenuCollapseAllInSection;
    JMenuItem N15;
    JMenuItem paramPopupMenuCopyName;
    JMenuItem N25;
    JMenuItem paramPopupMenuHelp;
    JMenuItem sectionPopupMenuHelp;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public MainWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    public JMenuBar getMainMenu() {
        if (MainMenu != null) return MainMenu;
        this.MainMenu = new JMenuBar();
        this.MenuFile = new JMenu("File");
        this.MenuFile.setMnemonic('F');
        this.MainMenu.add(MenuFile);
        this.MenuFileNew = new JMenuItem("New");
        this.MenuFileNew.setMnemonic(KeyEvent.VK_N);
        this.MenuFileNew.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileNewClick(event);
            }
        });
        this.MenuFile.add(MenuFileNew);
        
        this.MenuFileOpen = new JMenuItem("Open...");
        this.MenuFileOpen.setMnemonic(KeyEvent.VK_O);
        this.MenuFileOpen.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileOpenClick(event);
            }
        });
        this.MenuFile.add(MenuFileOpen);
        
        this.MenuFileReopen = new JMenu("Reopen");
        this.MenuFileReopen.setMnemonic(KeyEvent.VK_R);
        this.MenuFile.add(MenuFileReopen);
        this.MenuFileReopen.setSelected(false);
        this.Recent0 = new JMenuItem("0");
        this.Recent0.setVisible(false);
        this.Recent0.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent0);
        
        this.Recent1 = new JMenuItem("1");
        this.Recent1.setVisible(false);
        this.Recent1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent1);
        
        this.Recent2 = new JMenuItem("2");
        this.Recent2.setVisible(false);
        this.Recent2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent2);
        
        this.Recent3 = new JMenuItem("3");
        this.Recent3.setVisible(false);
        this.Recent3.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent3);
        
        this.Recent4 = new JMenuItem("4");
        this.Recent4.setVisible(false);
        this.Recent4.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent4);
        
        this.Recent5 = new JMenuItem("5");
        this.Recent5.setVisible(false);
        this.Recent5.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent5);
        
        this.Recent6 = new JMenuItem("6");
        this.Recent6.setVisible(false);
        this.Recent6.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent6);
        
        this.Recent7 = new JMenuItem("7");
        this.Recent7.setVisible(false);
        this.Recent7.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent7);
        
        this.Recent8 = new JMenuItem("8");
        this.Recent8.setVisible(false);
        this.Recent8.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent8);
        
        this.Recent9 = new JMenuItem("9");
        this.Recent9.setVisible(false);
        this.Recent9.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Recent0Click(event);
            }
        });
        this.MenuFileReopen.add(Recent9);
        
        
        this.MenuFileClose = new JMenuItem("Close");
        this.MenuFileClose.setMnemonic(KeyEvent.VK_C);
        this.MenuFileClose.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileCloseClick(event);
            }
        });
        this.MenuFile.add(MenuFileClose);
        
        this.MenuFile.addSeparator();
        
        this.MenuFileSave = new JMenuItem("Save");
        this.MenuFileSave.setMnemonic(KeyEvent.VK_S);
        this.MenuFileSave.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileSaveClick(event);
            }
        });
        this.MenuFile.add(MenuFileSave);
        
        this.MenuFileSaveAs = new JMenuItem("Save As...");
        this.MenuFileSaveAs.setMnemonic(KeyEvent.VK_A);
        this.MenuFileSaveAs.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileSaveAsClick(event);
            }
        });
        this.MenuFile.add(MenuFileSaveAs);
        
        this.MenuFile.addSeparator();
        
        this.MenuFileExport = new JMenu("Export");
        this.MenuFileExport.setMnemonic(KeyEvent.VK_E);
        this.MenuFile.add(MenuFileExport);
        this.MenuFileExport.setSelected(false);
        this.MenuPlantExportTo3DS = new JMenuItem("3DS...");
        this.MenuPlantExportTo3DS.setMnemonic(KeyEvent.VK_3);
        this.MenuPlantExportTo3DS.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantExportTo3DSClick(event);
            }
        });
        this.MenuFileExport.add(MenuPlantExportTo3DS);
        
        this.MenuPlantExportToLWO = new JMenuItem("LWO...");
        this.MenuPlantExportToLWO.setMnemonic(KeyEvent.VK_L);
        this.MenuPlantExportToLWO.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantExportToLWOClick(event);
            }
        });
        this.MenuFileExport.add(MenuPlantExportToLWO);
        
        this.MenuPlantExportToOBJ = new JMenuItem("OBJ...");
        this.MenuPlantExportToOBJ.setMnemonic(KeyEvent.VK_O);
        this.MenuPlantExportToOBJ.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantExportToOBJClick(event);
            }
        });
        this.MenuFileExport.add(MenuPlantExportToOBJ);
        
        this.MenuPlantExportToDXF = new JMenuItem("DXF...");
        this.MenuPlantExportToDXF.setMnemonic(KeyEvent.VK_D);
        this.MenuPlantExportToDXF.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantExportToDXFClick(event);
            }
        });
        this.MenuFileExport.add(MenuPlantExportToDXF);
        
        this.MenuPlantExportToPOV = new JMenuItem("POV INC...");
        this.MenuPlantExportToPOV.setMnemonic(KeyEvent.VK_V);
        this.MenuPlantExportToPOV.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantExportToPOVClick(event);
            }
        });
        this.MenuFileExport.add(MenuPlantExportToPOV);
        
        this.MenuPlantExportToVRML = new JMenuItem("VRML...");
        this.MenuPlantExportToVRML.setMnemonic(KeyEvent.VK_R);
        this.MenuPlantExportToVRML.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantExportToVRMLClick(event);
            }
        });
        this.MenuFileExport.add(MenuPlantExportToVRML);
        
        this.MenuFileExport.addSeparator();
        
        this.MenuFileSaveDrawingAs = new JMenuItem("Bitmap...");
        this.MenuFileSaveDrawingAs.setMnemonic(KeyEvent.VK_B);
        this.MenuFileSaveDrawingAs.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileSaveDrawingAsClick(event);
            }
        });
        this.MenuFileExport.add(MenuFileSaveDrawingAs);
        
        this.MenuFileSaveJPEG = new JMenuItem("JPEG...");
        this.MenuFileSaveJPEG.setMnemonic(KeyEvent.VK_J);
        this.MenuFileSaveJPEG.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileSaveJPEGClick(event);
            }
        });
        this.MenuFileExport.add(MenuFileSaveJPEG);
        
        ButtonGroup group = new ButtonGroup();
        this.MenuFileMakePainterNozzle = new JRadioButtonMenuItem("Nozzle/Tube Bitmap...");
        group.add(this.MenuFileMakePainterNozzle);
        this.MenuFileMakePainterNozzle.setMnemonic(KeyEvent.VK_N);
        this.MenuFileMakePainterNozzle.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileMakePainterNozzleClick(event);
            }
        });
        this.MenuFileExport.add(MenuFileMakePainterNozzle);
        this.MenuFileMakePainterNozzle.setSelected(false);
        
        this.MenuFileMakePainterAnimation = new JMenuItem("Animation Files...");
        this.MenuFileMakePainterAnimation.setMnemonic(KeyEvent.VK_A);
        this.MenuFileMakePainterAnimation.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileMakePainterAnimationClick(event);
            }
        });
        this.MenuFileExport.add(MenuFileMakePainterAnimation);
        
        
        this.MenuFileMove = new JMenu("Move");
        this.MenuFileMove.setMnemonic(KeyEvent.VK_M);
        this.MenuFile.add(MenuFileMove);
        this.MenuFileMove.setSelected(false);
        this.MenuFilePlantMover = new JMenuItem("Plant Mover...");
        this.MenuFilePlantMover.setMnemonic(KeyEvent.VK_P);
        this.MenuFilePlantMover.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFilePlantMoverClick(event);
            }
        });
        this.MenuFileMove.add(MenuFilePlantMover);
        
        this.MenuFileTdoMover = new JMenuItem("3D Object Mover...");
        this.MenuFileTdoMover.setMnemonic(KeyEvent.VK_3);
        this.MenuFileTdoMover.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileTdoMoverClick(event);
            }
        });
        this.MenuFileMove.add(MenuFileTdoMover);
        
        this.Reconcile3DObjects1 = new JMenuItem("Reconcile 3D Objects...");
        this.Reconcile3DObjects1.setMnemonic(KeyEvent.VK_R);
        this.Reconcile3DObjects1.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                Reconcile3DObjects1Click(event);
            }
        });
        this.MenuFileMove.add(Reconcile3DObjects1);
        
        
        this.MenuFile.addSeparator();
        
        this.MenuFilePrintDrawing = new JMenuItem("Print Picture...");
        this.MenuFilePrintDrawing.setMnemonic(KeyEvent.VK_P);
        this.MenuFilePrintDrawing.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFilePrintDrawingClick(event);
            }
        });
        this.MenuFile.add(MenuFilePrintDrawing);
        
        this.MenuFile.addSeparator();
        
        this.MenuFileExit = new JMenuItem("Exit");
        this.MenuFileExit.setMnemonic(KeyEvent.VK_X);
        this.MenuFileExit.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuFileExitClick(event);
            }
        });
        this.MenuFile.add(MenuFileExit);
        
        
        
        this.MenuEdit = new JMenu("Edit");
        this.MenuEdit.setMnemonic('E');
        this.MainMenu.add(MenuEdit);
        this.MenuEditUndo = new JMenuItem("Undo");
        this.MenuEditUndo.setMnemonic(KeyEvent.VK_U);
        this.MenuEditUndo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditUndoClick(event);
            }
        });
        this.MenuEdit.add(MenuEditUndo);
        
        this.MenuEditRedo = new JMenuItem("Redo");
        this.MenuEditRedo.setMnemonic(KeyEvent.VK_R);
        this.MenuEditRedo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditRedoClick(event);
            }
        });
        this.MenuEdit.add(MenuEditRedo);
        
        this.UndoMenuEditUndoRedoList = new JMenuItem("Undo/Redo List...");
        this.UndoMenuEditUndoRedoList.setMnemonic(KeyEvent.VK_L);
        this.UndoMenuEditUndoRedoList.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                UndoMenuEditUndoRedoListClick(event);
            }
        });
        this.MenuEdit.add(UndoMenuEditUndoRedoList);
        
        this.MenuEdit.addSeparator();
        
        this.MenuEditCut = new JMenuItem("Cut");
        this.MenuEditCut.setMnemonic(KeyEvent.VK_C);
        this.MenuEditCut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditCutClick(event);
            }
        });
        this.MenuEdit.add(MenuEditCut);
        
        this.MenuEditCopy = new JMenuItem("Copy");
        this.MenuEditCopy.setMnemonic(KeyEvent.VK_O);
        this.MenuEditCopy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditCopyClick(event);
            }
        });
        this.MenuEdit.add(MenuEditCopy);
        
        this.MenuEditPaste = new JMenuItem("Paste");
        this.MenuEditPaste.setMnemonic(KeyEvent.VK_P);
        this.MenuEditPaste.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditPasteClick(event);
            }
        });
        this.MenuEdit.add(MenuEditPaste);
        
        this.MenuEditDelete = new JMenuItem("Delete");
        this.MenuEditDelete.setMnemonic(KeyEvent.VK_D);
        this.MenuEditDelete.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditDeleteClick(event);
            }
        });
        this.MenuEdit.add(MenuEditDelete);
        
        this.MenuEditDuplicate = new JMenuItem("Duplicate");
        this.MenuEditDuplicate.setMnemonic(KeyEvent.VK_A);
        this.MenuEditDuplicate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditDuplicateClick(event);
            }
        });
        this.MenuEdit.add(MenuEditDuplicate);
        
        this.MenuEdit.addSeparator();
        
        this.MenuEditCopyDrawing = new JMenuItem("Copy Picture");
        this.MenuEditCopyDrawing.setMnemonic(KeyEvent.VK_I);
        this.MenuEditCopyDrawing.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditCopyDrawingClick(event);
            }
        });
        this.MenuEdit.add(MenuEditCopyDrawing);
        
        this.MenuEditCopyAsText = new JMenuItem("Copy To Text");
        this.MenuEditCopyAsText.setMnemonic(KeyEvent.VK_T);
        this.MenuEditCopyAsText.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditCopyAsTextClick(event);
            }
        });
        this.MenuEdit.add(MenuEditCopyAsText);
        
        this.MenuEditPasteAsText = new JMenuItem("Paste From Text");
        this.MenuEditPasteAsText.setMnemonic(KeyEvent.VK_F);
        this.MenuEditPasteAsText.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditPasteAsTextClick(event);
            }
        });
        this.MenuEdit.add(MenuEditPasteAsText);
        
        this.MenuEdit.addSeparator();
        
        this.MenuEditPreferences = new JMenuItem("Preferences...");
        this.MenuEditPreferences.setMnemonic(KeyEvent.VK_E);
        this.MenuEditPreferences.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuEditPreferencesClick(event);
            }
        });
        this.MenuEdit.add(MenuEditPreferences);
        
        
        
        this.MenuPlant = new JMenu("Plant");
        this.MenuPlant.setMnemonic('P');
        this.MainMenu.add(MenuPlant);
        this.MenuPlantNew = new JMenuItem("Create New...");
        this.MenuPlantNew.setMnemonic(KeyEvent.VK_N);
        this.MenuPlantNew.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantNewClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantNew);
        
        this.MenuPlantNewUsingLastWizardSettings = new JMenuItem("Create Same as Last");
        this.MenuPlantNewUsingLastWizardSettings.setMnemonic(KeyEvent.VK_L);
        this.MenuPlantNewUsingLastWizardSettings.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantNewUsingLastWizardSettingsClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantNewUsingLastWizardSettings);
        
        this.MenuPlant.addSeparator();
        
        this.MenuPlantBreed = new JMenuItem("Breed");
        this.MenuPlantBreed.setMnemonic(KeyEvent.VK_B);
        this.MenuPlantBreed.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantBreedClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantBreed);
        
        this.MenuPlantMakeTimeSeries = new JMenuItem("Make Time Series");
        this.MenuPlantMakeTimeSeries.setMnemonic(KeyEvent.VK_T);
        this.MenuPlantMakeTimeSeries.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantMakeTimeSeriesClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantMakeTimeSeries);
        
        this.MenuPlant.addSeparator();
        
        this.MenuPlantRandomize = new JMenuItem("Randomize");
        this.MenuPlantRandomize.setMnemonic(KeyEvent.VK_R);
        this.MenuPlantRandomize.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantRandomizeClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantRandomize);
        
        this.MenuPlantZeroRotations = new JMenuItem("Reset Rotations");
        this.MenuPlantZeroRotations.setMnemonic(KeyEvent.VK_S);
        this.MenuPlantZeroRotations.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantZeroRotationsClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantZeroRotations);
        
        this.MenuPlantAnimate = new JMenuItem("Animate through Life Cycle");
        this.MenuPlantAnimate.setMnemonic(KeyEvent.VK_A);
        this.MenuPlantAnimate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantAnimateClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantAnimate);
        
        this.MenuPlant.addSeparator();
        
        this.MenuPlantRename = new JMenuItem("Rename...");
        this.MenuPlantRename.setMnemonic(KeyEvent.VK_E);
        this.MenuPlantRename.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantRenameClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantRename);
        
        this.MenuPlantEditNote = new JMenuItem("Edit Note...");
        this.MenuPlantEditNote.setMnemonic(KeyEvent.VK_D);
        this.MenuPlantEditNote.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuPlantEditNoteClick(event);
            }
        });
        this.MenuPlant.add(MenuPlantEditNote);
        
        
        
        this.MenuLayout = new JMenu("Layout");
        this.MenuLayout.setMnemonic('L');
        this.MainMenu.add(MenuLayout);
        this.MenuLayoutSelectAll = new JMenuItem("Select All");
        this.MenuLayoutSelectAll.setMnemonic(KeyEvent.VK_A);
        this.MenuLayoutSelectAll.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutSelectAllClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutSelectAll);
        
        this.MenuLayoutDeselect = new JMenuItem("Select None");
        this.MenuLayoutDeselect.setMnemonic(KeyEvent.VK_N);
        this.MenuLayoutDeselect.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutDeselectClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutDeselect);
        
        this.MenuLayout.addSeparator();
        
        this.MenuLayoutScaleToFit = new JMenuItem("Scale to Fit");
        this.MenuLayoutScaleToFit.setMnemonic(KeyEvent.VK_F);
        this.MenuLayoutScaleToFit.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutScaleToFitClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutScaleToFit);
        
        this.MenuLayoutAlign = new JMenu("Align");
        this.MenuLayoutAlign.setMnemonic(KeyEvent.VK_L);
        this.MenuLayout.add(MenuLayoutAlign);
        this.MenuLayoutAlign.setSelected(false);
        this.MenuLayoutAlignTops = new JMenuItem("Tops");
        this.MenuLayoutAlignTops.setMnemonic(KeyEvent.VK_T);
        this.MenuLayoutAlignTops.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutAlignTopsClick(event);
            }
        });
        this.MenuLayoutAlign.add(MenuLayoutAlignTops);
        
        this.MenuLayoutAlignBottoms = new JMenuItem("Bottoms");
        this.MenuLayoutAlignBottoms.setMnemonic(KeyEvent.VK_B);
        this.MenuLayoutAlignBottoms.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutAlignBottomsClick(event);
            }
        });
        this.MenuLayoutAlign.add(MenuLayoutAlignBottoms);
        
        this.MenuLayoutAlignLeftSides = new JMenuItem("Left Sides");
        this.MenuLayoutAlignLeftSides.setMnemonic(KeyEvent.VK_L);
        this.MenuLayoutAlignLeftSides.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutAlignLeftSidesClick(event);
            }
        });
        this.MenuLayoutAlign.add(MenuLayoutAlignLeftSides);
        
        this.MenuLayoutAlignRightSides = new JMenuItem("Right Sides");
        this.MenuLayoutAlignRightSides.setMnemonic(KeyEvent.VK_R);
        this.MenuLayoutAlignRightSides.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutAlignRightSidesClick(event);
            }
        });
        this.MenuLayoutAlign.add(MenuLayoutAlignRightSides);
        
        this.MenuLayoutMakeBouquet = new JMenuItem("Make into Bouquet");
        this.MenuLayoutMakeBouquet.setMnemonic(KeyEvent.VK_Q);
        this.MenuLayoutMakeBouquet.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutMakeBouquetClick(event);
            }
        });
        this.MenuLayoutAlign.add(MenuLayoutMakeBouquet);
        
        
        this.MenuLayoutSize = new JMenu("Size");
        this.MenuLayoutSize.setMnemonic(KeyEvent.VK_Z);
        this.MenuLayout.add(MenuLayoutSize);
        this.MenuLayoutSize.setSelected(false);
        this.MenuLayoutSizeSameWidth = new JMenuItem("Equal Width");
        this.MenuLayoutSizeSameWidth.setMnemonic(KeyEvent.VK_W);
        this.MenuLayoutSizeSameWidth.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutSizeSameWidthClick(event);
            }
        });
        this.MenuLayoutSize.add(MenuLayoutSizeSameWidth);
        
        this.MenuLayoutSizeSameHeight = new JMenuItem("Equal Height");
        this.MenuLayoutSizeSameHeight.setMnemonic(KeyEvent.VK_H);
        this.MenuLayoutSizeSameHeight.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutSizeSameHeightClick(event);
            }
        });
        this.MenuLayoutSize.add(MenuLayoutSizeSameHeight);
        
        
        this.MenuLayoutPack = new JMenuItem("Pack");
        this.MenuLayoutPack.setMnemonic(KeyEvent.VK_P);
        this.MenuLayoutPack.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutPackClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutPack);
        
        this.MenuLayout.addSeparator();
        
        this.MenuLayoutBringForward = new JMenuItem("Bring Forward");
        this.MenuLayoutBringForward.setMnemonic(KeyEvent.VK_R);
        this.MenuLayoutBringForward.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutBringForwardClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutBringForward);
        
        this.MenuLayoutSendBack = new JMenuItem("Send Back");
        this.MenuLayoutSendBack.setMnemonic(KeyEvent.VK_B);
        this.MenuLayoutSendBack.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutSendBackClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutSendBack);
        
        this.MenuLayout.addSeparator();
        
        this.MenuLayoutShow = new JMenuItem("Show");
        this.MenuLayoutShow.setMnemonic(KeyEvent.VK_S);
        this.MenuLayoutShow.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutShowClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutShow);
        
        this.MenuLayoutHide = new JMenuItem("Hide");
        this.MenuLayoutHide.setMnemonic(KeyEvent.VK_H);
        this.MenuLayoutHide.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutHideClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutHide);
        
        this.MenuLayoutHideOthers = new JMenuItem("Hide Others");
        this.MenuLayoutHideOthers.setMnemonic(KeyEvent.VK_O);
        this.MenuLayoutHideOthers.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutHideOthersClick(event);
            }
        });
        this.MenuLayout.add(MenuLayoutHideOthers);
        
        
        
        this.MenuOptions = new JMenu("Options");
        this.MenuOptions.setMnemonic('O');
        this.MainMenu.add(MenuOptions);
        this.MenuOptionsDrawAs = new JMenu("Draw Using");
        this.MenuOptionsDrawAs.setMnemonic(KeyEvent.VK_D);
        this.MenuOptions.add(MenuOptionsDrawAs);
        this.MenuOptionsDrawAs.setSelected(false);
        this.MenuOptionsFastDraw = new JRadioButtonMenuItem("Bounding Boxes");
        group.add(this.MenuOptionsFastDraw);
        this.MenuOptionsFastDraw.setMnemonic(KeyEvent.VK_B);
        this.MenuOptionsFastDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsFastDrawClick(event);
            }
        });
        this.MenuOptionsDrawAs.add(MenuOptionsFastDraw);
        this.MenuOptionsFastDraw.setSelected(false);
        
        this.MenuOptionsMediumDraw = new JRadioButtonMenuItem("Wire Frames");
        group.add(this.MenuOptionsMediumDraw);
        this.MenuOptionsMediumDraw.setMnemonic(KeyEvent.VK_W);
        this.MenuOptionsMediumDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsMediumDrawClick(event);
            }
        });
        this.MenuOptionsDrawAs.add(MenuOptionsMediumDraw);
        this.MenuOptionsMediumDraw.setSelected(false);
        
        this.MenuOptionsBestDraw = new JRadioButtonMenuItem("Solids");
        group.add(this.MenuOptionsBestDraw);
        this.MenuOptionsBestDraw.setMnemonic(KeyEvent.VK_S);
        this.MenuOptionsBestDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsBestDrawClick(event);
            }
        });
        this.MenuOptionsDrawAs.add(MenuOptionsBestDraw);
        this.MenuOptionsBestDraw.setSelected(true);
        
        this.MenuOptionsCustomDraw = new JRadioButtonMenuItem("Custom...");
        group.add(this.MenuOptionsCustomDraw);
        this.MenuOptionsCustomDraw.setMnemonic(KeyEvent.VK_C);
        this.MenuOptionsCustomDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsCustomDrawClick(event);
            }
        });
        this.MenuOptionsDrawAs.add(MenuOptionsCustomDraw);
        this.MenuOptionsCustomDraw.setSelected(false);
        
        
        this.MenuLayoutView = new JMenu("View What Plants");
        this.MenuLayoutView.setMnemonic(KeyEvent.VK_V);
        this.MenuOptions.add(MenuLayoutView);
        this.MenuLayoutView.setSelected(false);
        group = new ButtonGroup();
        this.MenuLayoutViewFreeFloating = new JRadioButtonMenuItem("All Plants");
        group.add(this.MenuLayoutViewFreeFloating);
        this.MenuLayoutViewFreeFloating.setMnemonic(KeyEvent.VK_A);
        this.MenuLayoutViewFreeFloating.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutViewFreeFloatingClick(event);
            }
        });
        this.MenuLayoutView.add(MenuLayoutViewFreeFloating);
        this.MenuLayoutViewFreeFloating.setSelected(false);
        
        this.MenuLayoutViewOnePlantAtATime = new JRadioButtonMenuItem("One Plant at a Time");
        group.add(this.MenuLayoutViewOnePlantAtATime);
        this.MenuLayoutViewOnePlantAtATime.setMnemonic(KeyEvent.VK_O);
        this.MenuLayoutViewOnePlantAtATime.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutViewOnePlantAtATimeClick(event);
            }
        });
        this.MenuLayoutView.add(MenuLayoutViewOnePlantAtATime);
        this.MenuLayoutViewOnePlantAtATime.setSelected(false);
        
        
        group = new ButtonGroup();
        this.MenuLayoutDrawingAreaOn = new JMenu("Place Drawing Area");
        this.MenuLayoutDrawingAreaOn.setMnemonic(KeyEvent.VK_A);
        this.MenuOptions.add(MenuLayoutDrawingAreaOn);
        this.MenuLayoutDrawingAreaOn.setSelected(false);
        group = new ButtonGroup();
        this.MenuLayoutHorizontalOrientation = new JRadioButtonMenuItem("On Top");
        group.add(this.MenuLayoutHorizontalOrientation);
        this.MenuLayoutHorizontalOrientation.setMnemonic(KeyEvent.VK_T);
        this.MenuLayoutHorizontalOrientation.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutHorizontalOrientationClick(event);
            }
        });
        this.MenuLayoutDrawingAreaOn.add(MenuLayoutHorizontalOrientation);
        this.MenuLayoutHorizontalOrientation.setSelected(true);
        
        this.MenuLayoutVerticalOrientation = new JRadioButtonMenuItem("On Left Side");
        group.add(this.MenuLayoutVerticalOrientation);
        this.MenuLayoutVerticalOrientation.setMnemonic(KeyEvent.VK_L);
        this.MenuLayoutVerticalOrientation.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuLayoutVerticalOrientationClick(event);
            }
        });
        this.MenuLayoutDrawingAreaOn.add(MenuLayoutVerticalOrientation);
        this.MenuLayoutVerticalOrientation.setSelected(false);
        
        
        group = new ButtonGroup();
        this.MenuOptionsDrawRectangles = new JMenu("Draw Rectangles");
        this.MenuOptionsDrawRectangles.setMnemonic(KeyEvent.VK_R);
        this.MenuOptions.add(MenuOptionsDrawRectangles);
        this.MenuOptionsDrawRectangles.setSelected(false);
        this.MenuOptionsShowSelectionRectangles = new JRadioButtonMenuItem("Around Selected Plants");
        group.add(this.MenuOptionsShowSelectionRectangles);
        this.MenuOptionsShowSelectionRectangles.setMnemonic(KeyEvent.VK_S);
        this.MenuOptionsShowSelectionRectangles.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsShowSelectionRectanglesClick(event);
            }
        });
        this.MenuOptionsDrawRectangles.add(MenuOptionsShowSelectionRectangles);
        this.MenuOptionsShowSelectionRectangles.setSelected(false);
        
        this.MenuOptionsShowBoundsRectangles = new JRadioButtonMenuItem("Around All Plants");
        group.add(this.MenuOptionsShowBoundsRectangles);
        this.MenuOptionsShowBoundsRectangles.setMnemonic(KeyEvent.VK_A);
        this.MenuOptionsShowBoundsRectangles.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsShowBoundsRectanglesClick(event);
            }
        });
        this.MenuOptionsDrawRectangles.add(MenuOptionsShowBoundsRectangles);
        this.MenuOptionsShowBoundsRectangles.setSelected(false);
        
        
        this.MenuOptionsPosing = new JMenu("Posing");
        this.MenuOptionsPosing.setMnemonic(KeyEvent.VK_P);
        this.MenuOptions.add(MenuOptionsPosing);
        this.MenuOptionsPosing.setSelected(false);
        this.MenuOptionsHighlightPosedParts = new JRadioButtonMenuItem("Highlight Posed Parts");
        group.add(this.MenuOptionsHighlightPosedParts);
        this.MenuOptionsHighlightPosedParts.setMnemonic(KeyEvent.VK_H);
        this.MenuOptionsHighlightPosedParts.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsHighlightPosedPartsClick(event);
            }
        });
        this.MenuOptionsPosing.add(MenuOptionsHighlightPosedParts);
        this.MenuOptionsHighlightPosedParts.setSelected(false);
        
        this.MenuOptionsGhostHiddenParts = new JRadioButtonMenuItem("Ghost Hidden Parts");
        group.add(this.MenuOptionsGhostHiddenParts);
        this.MenuOptionsGhostHiddenParts.setMnemonic(KeyEvent.VK_G);
        this.MenuOptionsGhostHiddenParts.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsGhostHiddenPartsClick(event);
            }
        });
        this.MenuOptionsPosing.add(MenuOptionsGhostHiddenParts);
        this.MenuOptionsGhostHiddenParts.setSelected(false);
        
        this.MenuOptionsHidePosing = new JRadioButtonMenuItem("Ignore All Posing");
        group.add(this.MenuOptionsHidePosing);
        this.MenuOptionsHidePosing.setMnemonic(KeyEvent.VK_I);
        this.MenuOptionsHidePosing.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsHidePosingClick(event);
            }
        });
        this.MenuOptionsPosing.add(MenuOptionsHidePosing);
        this.MenuOptionsHidePosing.setSelected(false);
        
        
        this.MenuOptionsHints = new JMenu("Hints");
        this.MenuOptionsHints.setMnemonic(KeyEvent.VK_H);
        this.MenuOptions.add(MenuOptionsHints);
        this.MenuOptionsHints.setSelected(false);
        this.MenuOptionsShowLongButtonHints = new JRadioButtonMenuItem("Show Long Button Hints");
        group.add(this.MenuOptionsShowLongButtonHints);
        this.MenuOptionsShowLongButtonHints.setMnemonic(KeyEvent.VK_H);
        this.MenuOptionsShowLongButtonHints.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsShowLongButtonHintsClick(event);
            }
        });
        this.MenuOptionsHints.add(MenuOptionsShowLongButtonHints);
        this.MenuOptionsShowLongButtonHints.setSelected(false);
        
        this.MenuOptionsShowParameterHints = new JRadioButtonMenuItem("Show Parameter Hints");
        group.add(this.MenuOptionsShowParameterHints);
        this.MenuOptionsShowParameterHints.setMnemonic(KeyEvent.VK_M);
        this.MenuOptionsShowParameterHints.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsShowParameterHintsClick(event);
            }
        });
        this.MenuOptionsHints.add(MenuOptionsShowParameterHints);
        this.MenuOptionsShowParameterHints.setSelected(false);
        
        
        this.MenuOptions.addSeparator();
        
        this.MenuOptionsUsePlantBitmaps = new JRadioButtonMenuItem("Use Plant Bitmaps");
        group.add(this.MenuOptionsUsePlantBitmaps);
        this.MenuOptionsUsePlantBitmaps.setMnemonic(KeyEvent.VK_B);
        this.MenuOptionsUsePlantBitmaps.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuOptionsUsePlantBitmapsClick(event);
            }
        });
        this.MenuOptions.add(MenuOptionsUsePlantBitmaps);
        this.MenuOptionsUsePlantBitmaps.setSelected(false);
        
        
        
        this.MenuWindow = new JMenu("Window");
        this.MenuWindow.setMnemonic('W');
        this.MainMenu.add(MenuWindow);
        this.MenuWindowBreeder = new JMenuItem("Breeder");
        this.MenuWindowBreeder.setMnemonic(KeyEvent.VK_B);
        this.MenuWindowBreeder.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuWindowBreederClick(event);
            }
        });
        this.MenuWindow.add(MenuWindowBreeder);
        
        this.MenuWindowTimeSeries = new JMenuItem("Time Series");
        this.MenuWindowTimeSeries.setMnemonic(KeyEvent.VK_T);
        this.MenuWindowTimeSeries.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuWindowTimeSeriesClick(event);
            }
        });
        this.MenuWindow.add(MenuWindowTimeSeries);
        
        this.MenuWindow.addSeparator();
        
        this.MenuWindowNumericalExceptions = new JMenuItem("Messages");
        this.MenuWindowNumericalExceptions.setMnemonic(KeyEvent.VK_M);
        this.MenuWindowNumericalExceptions.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuWindowNumericalExceptionsClick(event);
            }
        });
        this.MenuWindow.add(MenuWindowNumericalExceptions);
        
        
        
        this.MenuHelp = new JMenu("Help");
        this.MenuHelp.setMnemonic('H');
        this.MainMenu.add(MenuHelp);
        this.MenuHelpTopics = new JMenuItem("Help Topics");
        this.MenuHelpTopics.setMnemonic(KeyEvent.VK_T);
        this.MenuHelpTopics.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuHelpTopicsClick(event);
            }
        });
        this.MenuHelp.add(MenuHelpTopics);
        
        this.MenuHelpSuperSpeedTour = new JMenuItem("Super-Speed Tour");
        this.MenuHelpSuperSpeedTour.setMnemonic(KeyEvent.VK_S);
        this.MenuHelpSuperSpeedTour.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuHelpSuperSpeedTourClick(event);
            }
        });
        this.MenuHelp.add(MenuHelpSuperSpeedTour);
        
        this.MenuHelpTutorial = new JMenuItem("Tutorial");
        this.MenuHelpTutorial.setMnemonic(KeyEvent.VK_U);
        this.MenuHelpTutorial.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuHelpTutorialClick(event);
            }
        });
        this.MenuHelp.add(MenuHelpTutorial);
        
        this.MenuHelp.addSeparator();
        
        this.MenuHelpRegister = new JMenuItem("Register...");
        this.MenuHelpRegister.setMnemonic(KeyEvent.VK_R);
        this.MenuHelpRegister.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuHelpRegisterClick(event);
            }
        });
        this.MenuHelp.add(MenuHelpRegister);
        
        this.MenuHelp.addSeparator();
        
        this.MenuHelpAbout = new JMenuItem("About PlantStudio");
        this.MenuHelpAbout.setMnemonic(KeyEvent.VK_A);
        this.MenuHelpAbout.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                MenuHelpAboutClick(event);
            }
        });
        this.MenuHelp.add(MenuHelpAbout);
        
        
        
        return MainMenu;
    }
        //  --------------- UNHANDLED ATTRIBUTE: this.MainMenu.Top = 179;
        //  --------------- UNHANDLED ATTRIBUTE: this.MainMenu.Left = 34;
        
    public JPopupMenu getPlantPopupMenu() {
        if (PlantPopupMenu != null) return PlantPopupMenu;
        this.PlantPopupMenu = new JPopupMenu();
        this.PopupMenuRandomize = new JMenuItem("Randomize");
        this.PopupMenuRandomize.setMnemonic(KeyEvent.VK_R);
        this.PopupMenuRandomize.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuRandomizeClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuRandomize);
        
        this.PlantPopupMenu.addSeparator();
        
        this.PopupMenuCut = new JMenuItem("Cut");
        this.PopupMenuCut.setMnemonic(KeyEvent.VK_C);
        this.PopupMenuCut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuCutClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuCut);
        
        this.PopupMenuCopy = new JMenuItem("Copy");
        this.PopupMenuCopy.setMnemonic(KeyEvent.VK_O);
        this.PopupMenuCopy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuCopyClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuCopy);
        
        this.PopupMenuPaste = new JMenuItem("Paste");
        this.PopupMenuPaste.setMnemonic(KeyEvent.VK_P);
        this.PopupMenuPaste.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuPasteClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuPaste);
        
        this.PlantPopupMenu.addSeparator();
        
        this.PopupMenuRename = new JMenuItem("Rename...");
        this.PopupMenuRename.setMnemonic(KeyEvent.VK_N);
        this.PopupMenuRename.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuRenameClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuRename);
        
        this.PopupMenuEditNote = new JMenuItem("Edit Note...");
        this.PopupMenuEditNote.setMnemonic(KeyEvent.VK_E);
        this.PopupMenuEditNote.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuEditNoteClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuEditNote);
        
        this.PopupMenuAnimate = new JMenuItem("Animate");
        this.PopupMenuAnimate.setMnemonic(KeyEvent.VK_A);
        this.PopupMenuAnimate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuAnimateClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuAnimate);
        
        this.PopupMenuBreed = new JMenuItem("Breed");
        this.PopupMenuBreed.setMnemonic(KeyEvent.VK_B);
        this.PopupMenuBreed.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuBreedClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuBreed);
        
        this.PopupMenuMakeTimeSeries = new JMenuItem("Make Time Series");
        this.PopupMenuMakeTimeSeries.setMnemonic(KeyEvent.VK_T);
        this.PopupMenuMakeTimeSeries.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuMakeTimeSeriesClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuMakeTimeSeries);
        
        this.PopupMenuZeroRotations = new JMenuItem("Reset Rotations");
        this.PopupMenuZeroRotations.setMnemonic(KeyEvent.VK_S);
        this.PopupMenuZeroRotations.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                PopupMenuZeroRotationsClick(event);
            }
        });
        this.PlantPopupMenu.add(PopupMenuZeroRotations);
        
        return PlantPopupMenu;
    }
        //  --------------- UNHANDLED ATTRIBUTE: this.PlantPopupMenu.Top = 179;
        //  --------------- UNHANDLED ATTRIBUTE: this.PlantPopupMenu.AutoPopup = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.PlantPopupMenu.Left = 122;
        
    public JPopupMenu getparamPopupMenu() {
        if (paramPopupMenu != null) return paramPopupMenu;
        this.paramPopupMenu = new JPopupMenu();
        this.paramPopupMenuExpand = new JMenuItem("Expand Panel");
        this.paramPopupMenuExpand.setMnemonic(KeyEvent.VK_E);
        this.paramPopupMenuExpand.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                paramPopupMenuExpandClick(event);
            }
        });
        this.paramPopupMenu.add(paramPopupMenuExpand);
        
        this.paramPopupMenuCollapse = new JMenuItem("Collapse Panel");
        this.paramPopupMenuCollapse.setMnemonic(KeyEvent.VK_C);
        this.paramPopupMenuCollapse.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                paramPopupMenuCollapseClick(event);
            }
        });
        this.paramPopupMenu.add(paramPopupMenuCollapse);
        
        this.paramPopupMenu.addSeparator();
        
        this.paramPopupMenuExpandAllInSection = new JMenuItem("Expand All Panels in This Section");
        this.paramPopupMenuExpandAllInSection.setMnemonic(KeyEvent.VK_X);
        this.paramPopupMenuExpandAllInSection.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                paramPopupMenuExpandAllInSectionClick(event);
            }
        });
        this.paramPopupMenu.add(paramPopupMenuExpandAllInSection);
        
        this.paramPopupMenuCollapseAllInSection = new JMenuItem("Collapse All Panels in This Section");
        this.paramPopupMenuCollapseAllInSection.setMnemonic(KeyEvent.VK_O);
        this.paramPopupMenuCollapseAllInSection.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                paramPopupMenuCollapseAllInSectionClick(event);
            }
        });
        this.paramPopupMenu.add(paramPopupMenuCollapseAllInSection);
        
        this.paramPopupMenu.addSeparator();
        
        this.paramPopupMenuCopyName = new JMenuItem("Copy Parameter Name");
        this.paramPopupMenuCopyName.setMnemonic(KeyEvent.VK_N);
        this.paramPopupMenuCopyName.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                paramPopupMenuCopyNameClick(event);
            }
        });
        this.paramPopupMenu.add(paramPopupMenuCopyName);
        
        this.paramPopupMenu.addSeparator();
        
        this.paramPopupMenuHelp = new JMenuItem("Go to Help for This Type of Parameter Panel");
        this.paramPopupMenuHelp.setMnemonic(KeyEvent.VK_H);
        this.paramPopupMenuHelp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                paramPopupMenuHelpClick(event);
            }
        });
        this.paramPopupMenu.add(paramPopupMenuHelp);
        
        this.sectionPopupMenuHelp = new JMenuItem("Go to Help for This Parameter Section");
        this.sectionPopupMenuHelp.setMnemonic(KeyEvent.VK_S);
        this.sectionPopupMenuHelp.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                sectionPopupMenuHelpClick(event);
            }
        });
        this.paramPopupMenu.add(sectionPopupMenuHelp);
        
        return paramPopupMenu;
    }
        //  --------------- UNHANDLED ATTRIBUTE: this.paramPopupMenu.Top = 179;
        //  --------------- UNHANDLED ATTRIBUTE: this.paramPopupMenu.Left = 63;
        
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setJMenuBar(getMainMenu());
        this.setContentPane(getMainContentPane());
        this.setTitle("MainForm");
    }
    
    private JPanel getMainContentPane() {
        if (mainContentPane == null) {
            mainContentPane = new JPanel();
            mainContentPane.setLayout(new BorderLayout());
            mainContentPane.add(getDelphiPanel(), BorderLayout.CENTER);
        }
        return mainContentPane;
    }
    public void OnClose(ActionEvent event) {
        System.out.println("Closed");
    }
    
    public JPanel getDelphiPanel() {
        if (delphiPanel != null) return delphiPanel;
        Toolkit toolkit = java.awt.Toolkit.getDefaultToolkit();
        delphiPanel = new JPanel();
        delphiPanel.setLayout(null);
        // -- delphiPanel.setLayout(BoxLayout(contentPane, BoxLayout.Y_AXIS));
        // Font buttonFont = new Font("Arial Narrow", Font.PLAIN, 9);
        // Insets buttonMargin = new Insets(1, 1, 1, 1);
        this.setBounds(297, 117, 715, 496  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.Menu = MainMenu;
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnShow = FormShow;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent event) {
                FormKeyPress(event);
            }
        });
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent event) {
                FormKeyDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnDestroy = FormDestroy;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyReleased(java.awt.event.KeyEvent event) {
                FormKeyUp(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poDefaultPosOnly;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnClose = FormClose;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        this.setVisible(false);
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.AutoScroll = False;
        
        
        Image paletteImageImage = toolkit.createImage("../resources/MainForm_paletteImage.png");
        this.paletteImage = new ImagePanel(new ImageIcon(paletteImageImage));
        this.paletteImage.setBounds(147, 167, 2, 2);
        this.paletteImage.setVisible(false);
        
        Image visibleBitmapImage = toolkit.createImage("../resources/MainForm_visibleBitmap.png");
        this.visibleBitmap = new ImagePanel(new ImageIcon(visibleBitmapImage));
        this.visibleBitmap.setBounds(46, 220, 16, 16);
        this.visibleBitmap.setVisible(false);
        
        Image paramPanelOpenArrowImageImage = toolkit.createImage("../resources/MainForm_paramPanelOpenArrowImage.png");
        this.paramPanelOpenArrowImage = new ImagePanel(new ImageIcon(paramPanelOpenArrowImageImage));
        this.paramPanelOpenArrowImage.setBounds(85, 222, 13, 13);
        this.paramPanelOpenArrowImage.setVisible(false);
        
        Image paramPanelClosedArrowImageImage = toolkit.createImage("../resources/MainForm_paramPanelClosedArrowImage.png");
        this.paramPanelClosedArrowImage = new ImagePanel(new ImageIcon(paramPanelClosedArrowImageImage));
        this.paramPanelClosedArrowImage.setBounds(105, 222, 13, 13);
        this.paramPanelClosedArrowImage.setVisible(false);
        
        Image fileChangedImageImage = toolkit.createImage("../resources/MainForm_fileChangedImage.png");
        this.fileChangedImage = new ImagePanel(new ImageIcon(fileChangedImageImage));
        this.fileChangedImage.setBounds(11, 248, 16, 16);
        this.fileChangedImage.setVisible(false);
        
        Image fileNotChangedImageImage = toolkit.createImage("../resources/MainForm_fileNotChangedImage.png");
        this.fileNotChangedImage = new ImagePanel(new ImageIcon(fileNotChangedImageImage));
        this.fileNotChangedImage.setBounds(31, 248, 16, 16);
        this.fileNotChangedImage.setVisible(false);
        
        Image unregisteredExportReminderImage = toolkit.createImage("../resources/MainForm_unregisteredExportReminder.png");
        this.unregisteredExportReminder = new ImagePanel(new ImageIcon(unregisteredExportReminderImage));
        this.unregisteredExportReminder.setBounds(66, 220, 17, 16);
        this.unregisteredExportReminder.setVisible(false);
        
        Image plantBitmapsGreenImageImage = toolkit.createImage("../resources/MainForm_plantBitmapsGreenImage.png");
        this.plantBitmapsGreenImage = new ImagePanel(new ImageIcon(plantBitmapsGreenImageImage));
        this.plantBitmapsGreenImage.setBounds(70, 248, 16, 16);
        this.plantBitmapsGreenImage.setVisible(false);
        
        Image noPlantBitmapsImageImage = toolkit.createImage("../resources/MainForm_noPlantBitmapsImage.png");
        this.noPlantBitmapsImage = new ImagePanel(new ImageIcon(noPlantBitmapsImageImage));
        this.noPlantBitmapsImage.setBounds(51, 248, 16, 16);
        this.noPlantBitmapsImage.setVisible(false);
        
        Image plantBitmapsYellowImageImage = toolkit.createImage("../resources/MainForm_plantBitmapsYellowImage.png");
        this.plantBitmapsYellowImage = new ImagePanel(new ImageIcon(plantBitmapsYellowImageImage));
        this.plantBitmapsYellowImage.setBounds(90, 248, 16, 16);
        this.plantBitmapsYellowImage.setVisible(false);
        
        Image plantBitmapsRedImageImage = toolkit.createImage("../resources/MainForm_plantBitmapsRedImage.png");
        this.plantBitmapsRedImage = new ImagePanel(new ImageIcon(plantBitmapsRedImageImage));
        this.plantBitmapsRedImage.setBounds(110, 248, 16, 16);
        this.plantBitmapsRedImage.setVisible(false);
        
        this.posingLineColorLabel = new JLabel("Line color");
        this.posingLineColorLabel.setBounds(50, 29, 47, 14);
        
        this.posingFrontfaceColorLabel = new JLabel("3D Object front face color");
        this.posingFrontfaceColorLabel.setBounds(50, 49, 125, 14);
        
        this.posingBackfaceColorLabel = new JLabel("3D Object back face color");
        this.posingBackfaceColorLabel.setBounds(50, 71, 125, 14);
        
        this.posingChangeColors = new JCheckBox("Change this part''s colors");
        this.posingChangeColors.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingChangeColors.setBounds(4, 6, 144, 17);
        
        this.posingChangeAllColorsAfter = new JCheckBox("and above");
        this.posingChangeAllColorsAfter.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingChangeAllColorsAfter.setBounds(146, 6, 73, 17);
        
        this.posingLineColor = new JPanel(null);
        // -- this.posingLineColor.setLayout(new BoxLayout(this.posingLineColor, BoxLayout.Y_AXIS));
        this.posingLineColor.setBounds(26, 25, 20, 20);
        this.posingLineColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                posingLineColorMouseUp(event);
            }
        });
        
        this.posingFrontfaceColor = new JPanel(null);
        // -- this.posingFrontfaceColor.setLayout(new BoxLayout(this.posingFrontfaceColor, BoxLayout.Y_AXIS));
        this.posingFrontfaceColor.setBounds(26, 47, 20, 20);
        this.posingFrontfaceColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                posingFrontfaceColorMouseUp(event);
            }
        });
        
        this.posingBackfaceColor = new JPanel(null);
        // -- this.posingBackfaceColor.setLayout(new BoxLayout(this.posingBackfaceColor, BoxLayout.Y_AXIS));
        this.posingBackfaceColor.setBounds(26, 69, 20, 20);
        this.posingBackfaceColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                posingBackfaceColorMouseUp(event);
            }
        });
        
        this.posingColorsPanel = new JPanel(null);
        // -- this.posingColorsPanel.setLayout(new BoxLayout(this.posingColorsPanel, BoxLayout.Y_AXIS));
        this.posingColorsPanel.add(posingLineColorLabel);
        this.posingColorsPanel.add(posingFrontfaceColorLabel);
        this.posingColorsPanel.add(posingBackfaceColorLabel);
        this.posingColorsPanel.add(posingChangeColors);
        this.posingColorsPanel.add(posingChangeAllColorsAfter);
        this.posingColorsPanel.add(posingLineColor);
        this.posingColorsPanel.add(posingFrontfaceColor);
        this.posingColorsPanel.add(posingBackfaceColor);
        this.posingColorsPanel.setBounds(476, 500, 229, 93);
        this.posingColorsPanel.setVisible(false);
        
        this.horizontalSplitter = new JPanel(null);
        // -- this.horizontalSplitter.setLayout(new BoxLayout(this.horizontalSplitter, BoxLayout.Y_AXIS));
        this.horizontalSplitter.setBounds(8, 168, 130, 4);
        //  --------------- UNHANDLED ATTRIBUTE: this.horizontalSplitter.Cursor = crVSplit;
        this.horizontalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseMoved(java.awt.event.MouseEvent event) {
                horizontalSplitterMouseMove(event);
            }
        });
        this.horizontalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent event) {
                horizontalSplitterMouseMove(event);
            }
        });
        this.horizontalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                horizontalSplitterMouseUp(event);
            }
        });
        this.horizontalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                horizontalSplitterMouseDown(event);
            }
        });
        
        this.verticalSplitter = new JPanel(null);
        // -- this.verticalSplitter.setLayout(new BoxLayout(this.verticalSplitter, BoxLayout.Y_AXIS));
        this.verticalSplitter.setBounds(0, 2, 4, 169);
        //  --------------- UNHANDLED ATTRIBUTE: this.verticalSplitter.Cursor = crHSplit;
        this.verticalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseMoved(java.awt.event.MouseEvent event) {
                verticalSplitterMouseMove(event);
            }
        });
        this.verticalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent event) {
                verticalSplitterMouseMove(event);
            }
        });
        this.verticalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                verticalSplitterMouseUp(event);
            }
        });
        this.verticalSplitter.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                verticalSplitterMouseDown(event);
            }
        });
        
        Image dragCursorModeImage = toolkit.createImage("../resources/MainForm_dragCursorMode.png");
        this.dragCursorMode = new SpeedButton(new ImageIcon(dragCursorModeImage));
        this.dragCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                dragCursorModeClick(event);
            }
        });
        this.dragCursorMode.setBounds(6, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.dragCursorMode.GroupIndex = 1;
        
        Image magnifyCursorModeImage = toolkit.createImage("../resources/MainForm_magnifyCursorMode.png");
        this.magnifyCursorMode = new SpeedButton(new ImageIcon(magnifyCursorModeImage));
        this.magnifyCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                magnifyCursorModeClick(event);
            }
        });
        this.magnifyCursorMode.setBounds(81, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.magnifyCursorMode.GroupIndex = 1;
        
        Image scrollCursorModeImage = toolkit.createImage("../resources/MainForm_scrollCursorMode.png");
        this.scrollCursorMode = new SpeedButton(new ImageIcon(scrollCursorModeImage));
        this.scrollCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                scrollCursorModeClick(event);
            }
        });
        this.scrollCursorMode.setBounds(31, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.scrollCursorMode.GroupIndex = 1;
        
        Image rotateCursorModeImage = toolkit.createImage("../resources/MainForm_rotateCursorMode.png");
        this.rotateCursorMode = new SpeedButton(new ImageIcon(rotateCursorModeImage));
        this.rotateCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                rotateCursorModeClick(event);
            }
        });
        this.rotateCursorMode.setBounds(56, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.rotateCursorMode.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.rotateCursorMode.GroupIndex = 1;
        
        Image centerDrawingImage = toolkit.createImage("../resources/MainForm_centerDrawing.png");
        this.centerDrawing = new SpeedButton("Scale to Fit", new ImageIcon(centerDrawingImage));
        this.centerDrawing.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                centerDrawingClick(event);
            }
        });
        this.centerDrawing.setBounds(214, 4, 88, 25);
        
        Image viewFreeFloatingImage = toolkit.createImage("../resources/MainForm_viewFreeFloating.png");
        this.viewFreeFloating = new SpeedButton(new ImageIcon(viewFreeFloatingImage));
        this.viewFreeFloating.setSelected(true);
        this.viewFreeFloating.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                viewFreeFloatingClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.viewFreeFloating.setBounds(319, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.viewFreeFloating.GroupIndex = 5;
        
        Image viewOneOnlyImage = toolkit.createImage("../resources/MainForm_viewOneOnly.png");
        this.viewOneOnly = new SpeedButton(new ImageIcon(viewOneOnlyImage));
        this.viewOneOnly.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                viewOneOnlyClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.viewOneOnly.setBounds(346, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.viewOneOnly.GroupIndex = 5;
        
        Image drawingAreaOnTopImage = toolkit.createImage("../resources/MainForm_drawingAreaOnTop.png");
        this.drawingAreaOnTop = new SpeedButton(new ImageIcon(drawingAreaOnTopImage));
        this.drawingAreaOnTop.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                drawingAreaOnTopClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.drawingAreaOnTop.setBounds(387, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.drawingAreaOnTop.GroupIndex = 6;
        
        Image drawingAreaOnSideImage = toolkit.createImage("../resources/MainForm_drawingAreaOnSide.png");
        this.drawingAreaOnSide = new SpeedButton(new ImageIcon(drawingAreaOnSideImage));
        this.drawingAreaOnSide.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                drawingAreaOnSideClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.drawingAreaOnSide.setBounds(415, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.drawingAreaOnSide.GroupIndex = 6;
        
        Image posingSelectionCursorModeImage = toolkit.createImage("../resources/MainForm_posingSelectionCursorMode.png");
        this.posingSelectionCursorMode = new SpeedButton(new ImageIcon(posingSelectionCursorModeImage));
        this.posingSelectionCursorMode.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                posingSelectionCursorModeClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.posingSelectionCursorMode.setBounds(106, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingSelectionCursorMode.GroupIndex = 1;
        
        this.magnificationPercent = new JComboBox(new DefaultComboBoxModel());
        this.magnificationPercent.setBounds(147, 6, 60, 22);
        this.magnificationPercent.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                magnificationPercentExit(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.magnificationPercent.Text = '100%';
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("12%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("25%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("50%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("75%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("100%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("150%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("200%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("300%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("400%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("500%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("600%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("700%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("800%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("900%");
        ((DefaultComboBoxModel)this.magnificationPercent.getModel()).addElement("1000%");
        this.magnificationPercent.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                magnificationPercentClick(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.magnificationPercent.ItemHeight = 14;
        
        this.toolbarPanel = new JPanel(null);
        // -- this.toolbarPanel.setLayout(new BoxLayout(this.toolbarPanel, BoxLayout.Y_AXIS));
        this.toolbarPanel.add(dragCursorMode);
        this.toolbarPanel.add(magnifyCursorMode);
        this.toolbarPanel.add(scrollCursorMode);
        this.toolbarPanel.add(rotateCursorMode);
        this.toolbarPanel.add(centerDrawing);
        this.toolbarPanel.add(viewFreeFloating);
        this.toolbarPanel.add(viewOneOnly);
        this.toolbarPanel.add(drawingAreaOnTop);
        this.toolbarPanel.add(drawingAreaOnSide);
        this.toolbarPanel.add(posingSelectionCursorMode);
        this.toolbarPanel.add(magnificationPercent);
        this.toolbarPanel.setBounds(6, 3, 453, 33);
        
        //  ------- UNHANDLED TYPE TPaintBox: progressPaintBox 
        //  --------------- UNHANDLED ATTRIBUTE: this.progressPaintBox.Top = 114;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressPaintBox.Height = 3;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressPaintBox.Width = 85;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressPaintBox.OnPaint = progressPaintBoxPaint;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressPaintBox.Left = 48;
        
        Image plantFileChangedImageImage = toolkit.createImage("../resources/MainForm_plantFileChangedImage.png");
        this.plantFileChangedImage = new ImagePanel(new ImageIcon(plantFileChangedImageImage));
        this.plantFileChangedImage.setBounds(6, 108, 16, 16);
        
        Image plantBitmapsIndicatorImageImage = toolkit.createImage("../resources/MainForm_plantBitmapsIndicatorImage.png");
        this.plantBitmapsIndicatorImage = new ImagePanel(new ImageIcon(plantBitmapsIndicatorImageImage));
        this.plantBitmapsIndicatorImage.setBounds(28, 107, 16, 16);
        this.plantBitmapsIndicatorImage.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                plantBitmapsIndicatorImageClick(event);
            }
        });
        
        this.plantListDrawGrid = new JTable(new DefaultTableModel());
        this.plantListDrawGrid.setBounds(4, 4, 137, 103);
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.OnDragOver = plantListDrawGridDragOver;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.ColCount = 1;
        this.plantListDrawGrid.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                plantListDrawGridMouseUp(event);
            }
        });
        this.plantListDrawGrid.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                plantListDrawGridMouseDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.OnDrawCell = plantListDrawGridDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.DefaultDrawing = False;
        this.plantListDrawGrid.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent event) {
                plantListDrawGridKeyDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.GridLineWidth = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.DefaultRowHeight = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.OnEndDrag = plantListDrawGridEndDrag;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.FixedRows = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.ScrollBars = ssVertical;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.OnDblClick = plantListDrawGridDblClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.DefaultColWidth = 200;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.RowCount = 10;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantListDrawGrid.FixedCols = 0;
        
        this.plantListPanel = new JPanel(null);
        // -- this.plantListPanel.setLayout(new BoxLayout(this.plantListPanel, BoxLayout.Y_AXIS));
        // FIX UNHANDLED TYPE -- this.plantListPanel.add(this.progressPaintBox);
        this.plantListPanel.add(plantFileChangedImage);
        this.plantListPanel.add(plantBitmapsIndicatorImage);
        this.plantListPanel.add(plantListDrawGrid);
        this.plantListPanel.setBounds(8, 36, 147, 127);
        
        Image Sections_FlowersPrimaryImage = toolkit.createImage("../resources/MainForm_Sections_FlowersPrimary.png");
        this.Sections_FlowersPrimary = new ImagePanel(new ImageIcon(Sections_FlowersPrimaryImage));
        this.Sections_FlowersPrimary.setBounds(40, 42, 32, 32);
        
        Image Sections_GeneralImage = toolkit.createImage("../resources/MainForm_Sections_General.png");
        this.Sections_General = new ImagePanel(new ImageIcon(Sections_GeneralImage));
        this.Sections_General.setBounds(4, 4, 32, 32);
        
        Image Sections_InflorPrimaryImage = toolkit.createImage("../resources/MainForm_Sections_InflorPrimary.png");
        this.Sections_InflorPrimary = new ImagePanel(new ImageIcon(Sections_InflorPrimaryImage));
        this.Sections_InflorPrimary.setBounds(112, 42, 32, 32);
        
        Image Sections_MeristemsImage = toolkit.createImage("../resources/MainForm_Sections_Meristems.png");
        this.Sections_Meristems = new ImagePanel(new ImageIcon(Sections_MeristemsImage));
        this.Sections_Meristems.setBounds(40, 4, 32, 32);
        
        Image Sections_LeavesImage = toolkit.createImage("../resources/MainForm_Sections_Leaves.png");
        this.Sections_Leaves = new ImagePanel(new ImageIcon(Sections_LeavesImage));
        this.Sections_Leaves.setBounds(112, 4, 32, 32);
        
        Image Sections_RootTopImage = toolkit.createImage("../resources/MainForm_Sections_RootTop.png");
        this.Sections_RootTop = new ImagePanel(new ImageIcon(Sections_RootTopImage));
        this.Sections_RootTop.setBounds(112, 78, 32, 32);
        
        Image Sections_FruitImage = toolkit.createImage("../resources/MainForm_Sections_Fruit.png");
        this.Sections_Fruit = new ImagePanel(new ImageIcon(Sections_FruitImage));
        this.Sections_Fruit.setBounds(4, 78, 32, 32);
        
        Image Sections_InflorSecondaryImage = toolkit.createImage("../resources/MainForm_Sections_InflorSecondary.png");
        this.Sections_InflorSecondary = new ImagePanel(new ImageIcon(Sections_InflorSecondaryImage));
        this.Sections_InflorSecondary.setBounds(76, 78, 32, 32);
        
        Image Sections_InternodesImage = toolkit.createImage("../resources/MainForm_Sections_Internodes.png");
        this.Sections_Internodes = new ImagePanel(new ImageIcon(Sections_InternodesImage));
        this.Sections_Internodes.setBounds(76, 4, 32, 32);
        
        Image Sections_SeedlingLeavesImage = toolkit.createImage("../resources/MainForm_Sections_SeedlingLeaves.png");
        this.Sections_SeedlingLeaves = new ImagePanel(new ImageIcon(Sections_SeedlingLeavesImage));
        this.Sections_SeedlingLeaves.setBounds(4, 42, 32, 32);
        
        Image Sections_FlowersSecondaryImage = toolkit.createImage("../resources/MainForm_Sections_FlowersSecondary.png");
        this.Sections_FlowersSecondary = new ImagePanel(new ImageIcon(Sections_FlowersSecondaryImage));
        this.Sections_FlowersSecondary.setBounds(40, 78, 32, 32);
        
        Image Sections_FlowersPrimaryAdvancedImage = toolkit.createImage("../resources/MainForm_Sections_FlowersPrimaryAdvanced.png");
        this.Sections_FlowersPrimaryAdvanced = new ImagePanel(new ImageIcon(Sections_FlowersPrimaryAdvancedImage));
        this.Sections_FlowersPrimaryAdvanced.setBounds(76, 42, 32, 32);
        
        Image Sections_OrthogonalImage = toolkit.createImage("../resources/MainForm_Sections_Orthogonal.png");
        this.Sections_Orthogonal = new ImagePanel(new ImageIcon(Sections_OrthogonalImage));
        this.Sections_Orthogonal.setBounds(4, 114, 32, 32);
        
        this.sectionImagesPanel = new JPanel(null);
        // -- this.sectionImagesPanel.setLayout(new BoxLayout(this.sectionImagesPanel, BoxLayout.Y_AXIS));
        this.sectionImagesPanel.add(Sections_FlowersPrimary);
        this.sectionImagesPanel.add(Sections_General);
        this.sectionImagesPanel.add(Sections_InflorPrimary);
        this.sectionImagesPanel.add(Sections_Meristems);
        this.sectionImagesPanel.add(Sections_Leaves);
        this.sectionImagesPanel.add(Sections_RootTop);
        this.sectionImagesPanel.add(Sections_Fruit);
        this.sectionImagesPanel.add(Sections_InflorSecondary);
        this.sectionImagesPanel.add(Sections_Internodes);
        this.sectionImagesPanel.add(Sections_SeedlingLeaves);
        this.sectionImagesPanel.add(Sections_FlowersSecondary);
        this.sectionImagesPanel.add(Sections_FlowersPrimaryAdvanced);
        this.sectionImagesPanel.add(Sections_Orthogonal);
        this.sectionImagesPanel.setBounds(2, 272, 149, 177);
        this.sectionImagesPanel.setVisible(false);
        
        this.plantsAsTextMemo = new JTextArea(10, 10);
        this.plantsAsTextMemo.setBounds(4, 460, 151, 27);
        this.plantsAsTextMemo.setVisible(false);
        
        this.animatingLabel = new JLabel("Animating! Press space bar to stop.");
        this.animatingLabel.setBounds(5, 415, 197, 14);
        this.animatingLabel.setVisible(false);
        
        this.lifeCycleGraphImage = new ImagePanel(); // No image was set
        this.lifeCycleGraphImage.setBounds(36, 20, 213, 25);
        
        this.timeLabel = new JLabel("time (days)");
        this.timeLabel.setBounds(104, 48, 54, 14);
        
        this.selectedPlantNameLabel = new JLabel("Selected plant");
        this.selectedPlantNameLabel.setBounds(10, 4, 78, 14);
        
        this.maxSizeAxisLabel = new JLabel("%max");
        this.maxSizeAxisLabel.setBounds(4, 24, 30, 14);
        
        this.daysAndSizeLabel = new JLabel("days, 26% max size");
        this.daysAndSizeLabel.setBounds(89, 8, 98, 14);
        
        this.ageAndSizeLabel = new JLabel("Age");
        this.ageAndSizeLabel.setBounds(10, 6, 20, 14);
        
        Image animateGrowthImage = toolkit.createImage("../resources/MainForm_animateGrowth.png");
        this.animateGrowth = new SpeedButton("Animate", new ImageIcon(animateGrowthImage));
        this.animateGrowth.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                animateGrowthClick(event);
            }
        });
        this.animateGrowth.setBounds(194, 2, 72, 23);
        
        this.lifeCycleDaysEdit = new JTextField("100");
        this.lifeCycleDaysEdit.setBounds(36, 2, 29, 21);
        this.lifeCycleDaysEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                lifeCycleDaysEditExit(event);
            }
        });
        
        this.lifeCycleDaysSpin = new SpinButton("FIX_ME");
        Image lifeCycleDaysSpinImage = toolkit.createImage("../resources/MainForm_lifeCycleDaysSpin.png");
        this.lifeCycleDaysSpin.setUpIcon(new ImageIcon(lifeCycleDaysSpinImage));
        this.lifeCycleDaysSpin.setDownIcon(new ImageIcon(lifeCycleDaysSpinImage));
        this.lifeCycleDaysSpin.setBounds(66, 2, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.lifeCycleDaysSpin.FocusControl = lifeCycleDaysEdit;
        //  --------------- UNHANDLED ATTRIBUTE: this.lifeCycleDaysSpin.OnUpClick = lifeCycleDaysSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.lifeCycleDaysSpin.OnDownClick = lifeCycleDaysSpinDownClick;
        
        this.lifeCycleEditPanel = new JPanel(null);
        // -- this.lifeCycleEditPanel.setLayout(new BoxLayout(this.lifeCycleEditPanel, BoxLayout.Y_AXIS));
        this.lifeCycleEditPanel.add(daysAndSizeLabel);
        this.lifeCycleEditPanel.add(ageAndSizeLabel);
        this.lifeCycleEditPanel.add(animateGrowth);
        this.lifeCycleEditPanel.add(lifeCycleDaysEdit);
        this.lifeCycleEditPanel.add(lifeCycleDaysSpin);
        this.lifeCycleEditPanel.setBounds(6, 64, 269, 29);
        
        this.lifeCycleDragger = new JPanel(null);
        // -- this.lifeCycleDragger.setLayout(new BoxLayout(this.lifeCycleDragger, BoxLayout.Y_AXIS));
        this.lifeCycleDragger.setBounds(168, 24, 4, 17);
        //  --------------- UNHANDLED ATTRIBUTE: this.lifeCycleDragger.Cursor = crHSplit;
        this.lifeCycleDragger.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseMoved(java.awt.event.MouseEvent event) {
                lifeCycleDraggerMouseMove(event);
            }
        });
        this.lifeCycleDragger.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent event) {
                lifeCycleDraggerMouseMove(event);
            }
        });
        this.lifeCycleDragger.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                lifeCycleDraggerMouseUp(event);
            }
        });
        this.lifeCycleDragger.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                lifeCycleDraggerMouseDown(event);
            }
        });
        
        this.lifeCyclePanel = new JPanel(null);
        // -- this.lifeCyclePanel.setLayout(new BoxLayout(this.lifeCyclePanel, BoxLayout.Y_AXIS));
        this.lifeCyclePanel.add(lifeCycleGraphImage);
        this.lifeCyclePanel.add(timeLabel);
        this.lifeCyclePanel.add(selectedPlantNameLabel);
        this.lifeCyclePanel.add(maxSizeAxisLabel);
        this.lifeCyclePanel.add(lifeCycleEditPanel);
        this.lifeCyclePanel.add(lifeCycleDragger);
        this.lifeCyclePanel.setBounds(4, 318, 277, 95);
        this.lifeCyclePanel.setVisible(false);
        
        this.statsScrollBox = new JPanel(null);
        this.statsScrollBox.setBounds(284, 334, 261, 23);
        this.statsScrollBox.setVisible(false);
        
        //  ------- UNHANDLED TYPE TTabSet: tabSet 
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Font.Charset = DEFAULT_CHARSET;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.OnChange = tabSetChange;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Font.Style = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Font.Height = -11;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Top = 433;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.TabIndex = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Height = 21;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Tabs.Strings = [' Arrangement', ' Parameters', ' Age', ' Posing', ' Stats', ' Note'];
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Width = 437;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.DitherBackground = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Font.Name = 'Arial';
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Font.Color = clWindowText;
        //  --------------- UNHANDLED ATTRIBUTE: this.tabSet.Left = 4;
        
        this.parametersPlantName = new JLabel("Parameters for xx");
        this.parametersPlantName.setBounds(8, 8, 99, 14);
        
        this.parametersScrollBox = new JPanel(null);
        this.parametersScrollBox.setBounds(8, 44, 265, 23);
        
        this.sectionsComboBox = new JComboBox(new DefaultComboBoxModel());
        this.sectionsComboBox.setBounds(10, 20, 263, 40);
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionsComboBox.Style = csOwnerDrawFixed;
        ((DefaultComboBoxModel)this.sectionsComboBox.getModel()).addElement("General");
        ((DefaultComboBoxModel)this.sectionsComboBox.getModel()).addElement("Etc");
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionsComboBox.OnDrawItem = sectionsComboBoxDrawItem;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionsComboBox.OnChange = sectionsComboBoxChange;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionsComboBox.ItemHeight = 34;
        
        this.parametersPanel = new JPanel(null);
        // -- this.parametersPanel.setLayout(new BoxLayout(this.parametersPanel, BoxLayout.Y_AXIS));
        this.parametersPanel.add(parametersPlantName);
        this.parametersPanel.add(parametersScrollBox);
        this.parametersPanel.add(sectionsComboBox);
        this.parametersPanel.setBounds(4, 240, 277, 73);
        this.parametersPanel.setVisible(false);
        
        this.xRotationLabel = new JLabel("X");
        this.xRotationLabel.setBounds(59, 177, 7, 14);
        
        this.yRotationLabel = new JLabel("Y");
        this.yRotationLabel.setBounds(123, 177, 8, 14);
        
        this.zRotationLabel = new JLabel("Z");
        this.zRotationLabel.setBounds(188, 177, 7, 14);
        
        Image resetRotationsImage = toolkit.createImage("../resources/MainForm_resetRotations.png");
        this.resetRotations = new SpeedButton("Reset Rotations", new ImageIcon(resetRotationsImage));
        this.resetRotations.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                resetRotationsClick(event);
            }
        });
        this.resetRotations.setBounds(66, 200, 109, 25);
        
        this.rotationLabel = new JLabel("Rotation");
        this.rotationLabel.setBounds(11, 176, 39, 14);
        
        this.sizingLabel = new JLabel("Size");
        this.sizingLabel.setBounds(29, 104, 21, 14);
        
        this.drawingScalePixelsPerMmLabel = new JLabel("pixels/mm");
        this.drawingScalePixelsPerMmLabel.setBounds(126, 104, 47, 14);
        
        Image packPlantsImage = toolkit.createImage("../resources/MainForm_packPlants.png");
        this.packPlants = new SpeedButton("Pack", new ImageIcon(packPlantsImage));
        this.packPlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                packPlantsClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.packPlants.setBounds(188, 58, 65, 25);
        
        this.locationLabel = new JLabel("Location");
        this.locationLabel.setBounds(9, 34, 41, 14);
        
        this.xLocationLabel = new JLabel("X");
        this.xLocationLabel.setBounds(57, 35, 7, 14);
        
        this.yLocationLabel = new JLabel("Y");
        this.yLocationLabel.setBounds(134, 35, 8, 14);
        
        this.locationPixelsLabel = new JLabel("pixels");
        this.locationPixelsLabel.setBounds(209, 35, 28, 14);
        
        this.arrangementPlantName = new JLabel("(no plants selected)");
        this.arrangementPlantName.setBounds(4, 4, 110, 14);
        
        Image alignTopsImage = toolkit.createImage("../resources/MainForm_alignTops.png");
        this.alignTops = new SpeedButton(new ImageIcon(alignTopsImage));
        this.alignTops.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                alignTopsClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.alignTops.setBounds(66, 58, 25, 25);
        
        Image alignBottomsImage = toolkit.createImage("../resources/MainForm_alignBottoms.png");
        this.alignBottoms = new SpeedButton(new ImageIcon(alignBottomsImage));
        this.alignBottoms.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                alignBottomsClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.alignBottoms.setBounds(95, 58, 25, 25);
        
        Image alignLeftImage = toolkit.createImage("../resources/MainForm_alignLeft.png");
        this.alignLeft = new SpeedButton(new ImageIcon(alignLeftImage));
        this.alignLeft.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                alignLeftClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.alignLeft.setBounds(123, 58, 25, 25);
        
        Image alignRightImage = toolkit.createImage("../resources/MainForm_alignRight.png");
        this.alignRight = new SpeedButton(new ImageIcon(alignRightImage));
        this.alignRight.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                alignRightClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.alignRight.setBounds(152, 58, 25, 25);
        
        Image makeEqualWidthImage = toolkit.createImage("../resources/MainForm_makeEqualWidth.png");
        this.makeEqualWidth = new SpeedButton("Equal Width", new ImageIcon(makeEqualWidthImage));
        this.makeEqualWidth.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                makeEqualWidthClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.makeEqualWidth.setBounds(62, 128, 89, 25);
        
        Image makeEqualHeightImage = toolkit.createImage("../resources/MainForm_makeEqualHeight.png");
        this.makeEqualHeight = new SpeedButton("Equal Height", new ImageIcon(makeEqualHeightImage));
        this.makeEqualHeight.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                makeEqualHeightClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.makeEqualHeight.setBounds(154, 128, 89, 25);
        
        this.xRotationEdit = new JTextField("-360");
        this.xRotationEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                xRotationEditChange(event);
            }
        });
        this.xRotationEdit.setBounds(69, 174, 30, 21);
        this.xRotationEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                xRotationEditExit(event);
            }
        });
        
        this.xRotationSpin = new SpinButton("FIX_ME");
        Image xRotationSpinImage = toolkit.createImage("../resources/MainForm_xRotationSpin.png");
        this.xRotationSpin.setUpIcon(new ImageIcon(xRotationSpinImage));
        this.xRotationSpin.setDownIcon(new ImageIcon(xRotationSpinImage));
        this.xRotationSpin.setBounds(99, 175, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.xRotationSpin.OnUpClick = xRotationSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.xRotationSpin.OnDownClick = xRotationSpinDownClick;
        
        this.yRotationEdit = new JTextField("-360");
        this.yRotationEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                yRotationEditChange(event);
            }
        });
        this.yRotationEdit.setBounds(133, 174, 30, 21);
        this.yRotationEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                yRotationEditExit(event);
            }
        });
        
        this.yRotationSpin = new SpinButton("FIX_ME");
        Image yRotationSpinImage = toolkit.createImage("../resources/MainForm_yRotationSpin.png");
        this.yRotationSpin.setUpIcon(new ImageIcon(yRotationSpinImage));
        this.yRotationSpin.setDownIcon(new ImageIcon(yRotationSpinImage));
        this.yRotationSpin.setBounds(164, 175, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.yRotationSpin.OnUpClick = yRotationSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.yRotationSpin.OnDownClick = yRotationSpinDownClick;
        
        this.zRotationEdit = new JTextField("-360");
        this.zRotationEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                zRotationEditChange(event);
            }
        });
        this.zRotationEdit.setBounds(198, 174, 30, 21);
        this.zRotationEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                zRotationEditExit(event);
            }
        });
        
        this.zRotationSpin = new SpinButton("FIX_ME");
        Image zRotationSpinImage = toolkit.createImage("../resources/MainForm_zRotationSpin.png");
        this.zRotationSpin.setUpIcon(new ImageIcon(zRotationSpinImage));
        this.zRotationSpin.setDownIcon(new ImageIcon(zRotationSpinImage));
        this.zRotationSpin.setBounds(229, 175, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.zRotationSpin.OnUpClick = zRotationSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.zRotationSpin.OnDownClick = zRotationSpinDownClick;
        
        this.drawingScaleEdit = new JTextField("1.0");
        this.drawingScaleEdit.setBounds(61, 100, 43, 22);
        this.drawingScaleEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                drawingScaleEditExit(event);
            }
        });
        
        this.drawingScaleSpin = new SpinButton("FIX_ME");
        Image drawingScaleSpinImage = toolkit.createImage("../resources/MainForm_drawingScaleSpin.png");
        this.drawingScaleSpin.setUpIcon(new ImageIcon(drawingScaleSpinImage));
        this.drawingScaleSpin.setDownIcon(new ImageIcon(drawingScaleSpinImage));
        this.drawingScaleSpin.setBounds(105, 101, 15, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.drawingScaleSpin.FocusControl = drawingScaleEdit;
        //  --------------- UNHANDLED ATTRIBUTE: this.drawingScaleSpin.OnUpClick = drawingScaleSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.drawingScaleSpin.OnDownClick = drawingScaleSpinDownClick;
        
        this.xLocationEdit = new JTextField("-360");
        this.xLocationEdit.setBounds(66, 32, 40, 21);
        this.xLocationEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                xLocationEditExit(event);
            }
        });
        
        this.xLocationSpin = new SpinButton("FIX_ME");
        Image xLocationSpinImage = toolkit.createImage("../resources/MainForm_xLocationSpin.png");
        this.xLocationSpin.setUpIcon(new ImageIcon(xLocationSpinImage));
        this.xLocationSpin.setDownIcon(new ImageIcon(xLocationSpinImage));
        this.xLocationSpin.setBounds(108, 33, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.xLocationSpin.OnUpClick = xLocationSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.xLocationSpin.OnDownClick = xLocationSpinDownClick;
        
        this.yLocationEdit = new JTextField("-360");
        this.yLocationEdit.setBounds(144, 32, 40, 21);
        this.yLocationEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                yLocationEditExit(event);
            }
        });
        
        this.yLocationSpin = new SpinButton("FIX_ME");
        Image yLocationSpinImage = toolkit.createImage("../resources/MainForm_yLocationSpin.png");
        this.yLocationSpin.setUpIcon(new ImageIcon(yLocationSpinImage));
        this.yLocationSpin.setDownIcon(new ImageIcon(yLocationSpinImage));
        this.yLocationSpin.setBounds(187, 33, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.yLocationSpin.OnUpClick = yLocationSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.yLocationSpin.OnDownClick = yLocationSpinDownClick;
        
        this.rotationsPanel = new JPanel(null);
        // -- this.rotationsPanel.setLayout(new BoxLayout(this.rotationsPanel, BoxLayout.Y_AXIS));
        this.rotationsPanel.add(xRotationLabel);
        this.rotationsPanel.add(yRotationLabel);
        this.rotationsPanel.add(zRotationLabel);
        this.rotationsPanel.add(resetRotations);
        this.rotationsPanel.add(rotationLabel);
        this.rotationsPanel.add(sizingLabel);
        this.rotationsPanel.add(drawingScalePixelsPerMmLabel);
        this.rotationsPanel.add(packPlants);
        this.rotationsPanel.add(locationLabel);
        this.rotationsPanel.add(xLocationLabel);
        this.rotationsPanel.add(yLocationLabel);
        this.rotationsPanel.add(locationPixelsLabel);
        this.rotationsPanel.add(arrangementPlantName);
        this.rotationsPanel.add(alignTops);
        this.rotationsPanel.add(alignBottoms);
        this.rotationsPanel.add(alignLeft);
        this.rotationsPanel.add(alignRight);
        this.rotationsPanel.add(makeEqualWidth);
        this.rotationsPanel.add(makeEqualHeight);
        this.rotationsPanel.add(xRotationEdit);
        this.rotationsPanel.add(xRotationSpin);
        this.rotationsPanel.add(yRotationEdit);
        this.rotationsPanel.add(yRotationSpin);
        this.rotationsPanel.add(zRotationEdit);
        this.rotationsPanel.add(zRotationSpin);
        this.rotationsPanel.add(drawingScaleEdit);
        this.rotationsPanel.add(drawingScaleSpin);
        this.rotationsPanel.add(xLocationEdit);
        this.rotationsPanel.add(xLocationSpin);
        this.rotationsPanel.add(yLocationEdit);
        this.rotationsPanel.add(yLocationSpin);
        this.rotationsPanel.setBounds(6, 6, 273, 231);
        this.rotationsPanel.setVisible(false);
        
        this.noteLabel = new JLabel("Note for daisy");
        this.noteLabel.setBounds(8, 8, 76, 14);
        
        Image noteEditImage = toolkit.createImage("../resources/MainForm_noteEdit.png");
        this.noteEdit = new SpeedButton("Edit", new ImageIcon(noteEditImage));
        this.noteEdit.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                noteEditClick(event);
            }
        });
        this.noteEdit.setMnemonic(KeyEvent.VK_D);
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.noteEdit.setBounds(182, 4, 54, 25);
        
        this.noteMemo = new JTextArea(10, 10);
        this.noteMemo.setBounds(12, 30, 237, 15);
        //  --------------- UNHANDLED ATTRIBUTE: this.noteMemo.HideSelection = False;
        this.noteMemo.setEditable(false);
        //  --------------- UNHANDLED ATTRIBUTE: this.noteMemo.ScrollBars = ssVertical;
        //  --------------- UNHANDLED ATTRIBUTE: this.noteMemo.WantReturns = False;
        
        this.notePanel = new JPanel(null);
        // -- this.notePanel.setLayout(new BoxLayout(this.notePanel, BoxLayout.Y_AXIS));
        this.notePanel.add(noteLabel);
        this.notePanel.add(noteEdit);
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(12, 30, 237, 15);;
        scroller1.setViewportView(noteMemo);
        this.notePanel.add(scroller1);
        this.notePanel.setBounds(286, 360, 258, 48);
        this.notePanel.setVisible(false);
        
        this.posingPlantName = new JLabel("Posing for plant x");
        this.posingPlantName.setBounds(4, 4, 96, 14);
        
        this.posedPartsLabel = new JLabel("Posed parts");
        this.posedPartsLabel.setBounds(4, 26, 58, 14);
        
        Image posingHighlightImage = toolkit.createImage("../resources/MainForm_posingHighlight.png");
        this.posingHighlight = new SpeedButton(new ImageIcon(posingHighlightImage));
        this.posingHighlight.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                posingHighlightClick(event);
            }
        });
        this.posingHighlight.setBounds(170, 18, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingHighlight.GroupIndex = 101;
        
        Image posingGhostImage = toolkit.createImage("../resources/MainForm_posingGhost.png");
        this.posingGhost = new SpeedButton(new ImageIcon(posingGhostImage));
        this.posingGhost.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                posingGhostClick(event);
            }
        });
        this.posingGhost.setBounds(199, 18, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingGhost.GroupIndex = 102;
        
        Image posingNotShownImage = toolkit.createImage("../resources/MainForm_posingNotShown.png");
        this.posingNotShown = new SpeedButton(new ImageIcon(posingNotShownImage));
        this.posingNotShown.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                posingNotShownClick(event);
            }
        });
        this.posingNotShown.setBounds(228, 18, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingNotShown.GroupIndex = 103;
        
        this.selectedPartLabel = new JLabel("Part 999 (inflorescence)");
        this.selectedPartLabel.setBounds(5, 48, 117, 14);
        
        Image posingPosePartImage = toolkit.createImage("../resources/MainForm_posingPosePart.png");
        this.posingPosePart = new SpeedButton("Pose", new ImageIcon(posingPosePartImage));
        this.posingPosePart.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                posingPosePartClick(event);
            }
        });
        this.posingPosePart.setMnemonic(KeyEvent.VK_P);
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.posingPosePart.setBounds(5, 64, 58, 22);
        
        Image posingUnposePartImage = toolkit.createImage("../resources/MainForm_posingUnposePart.png");
        this.posingUnposePart = new SpeedButton("Unpose", new ImageIcon(posingUnposePartImage));
        this.posingUnposePart.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                posingUnposePartClick(event);
            }
        });
        this.posingUnposePart.setMnemonic(KeyEvent.VK_U);
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.posingUnposePart.setBounds(68, 64, 69, 22);
        
        this.posingXRotationLabel = new JLabel("X");
        this.posingXRotationLabel.setBounds(17, 68, 7, 14);
        
        this.posingYRotationLabel = new JLabel("Y");
        this.posingYRotationLabel.setBounds(82, 68, 8, 14);
        
        this.posingZRotationLabel = new JLabel("Z");
        this.posingZRotationLabel.setBounds(147, 68, 7, 14);
        
        this.posingScaleMultiplierPercent = new JLabel("% ");
        this.posingScaleMultiplierPercent.setBounds(179, 121, 13, 14);
        
        this.posingScaleMultiplierLabel = new JLabel("3D object scale by");
        this.posingScaleMultiplierLabel.setBounds(24, 119, 89, 14);
        
        this.posingLengthMultiplierPercent = new JLabel("% ");
        this.posingLengthMultiplierPercent.setBounds(179, 144, 13, 14);
        
        this.posingLengthMultiplierLabel = new JLabel("line length by");
        this.posingLengthMultiplierLabel.setBounds(50, 143, 63, 14);
        
        this.posingWidthMultiplierPercent = new JLabel("% ");
        this.posingWidthMultiplierPercent.setBounds(179, 167, 13, 14);
        
        this.posingWidthMultiplierLabel = new JLabel("line width by");
        this.posingWidthMultiplierLabel.setBounds(52, 166, 61, 14);
        
        this.hideExtraLabel = new JLabel("(up to the next posed part with dependents)");
        this.hideExtraLabel.setBounds(26, 23, 213, 14);
        
        this.rotationDegreesLabel = new JLabel("degrees");
        this.rotationDegreesLabel.setBounds(208, 67, 40, 14);
        
        this.posingMultiplyScaleAllPartsAfterLabel = new JLabel("with dependents");
        this.posingMultiplyScaleAllPartsAfterLabel.setBounds(44, 205, 81, 14);
        
        this.posingHidePart = new JCheckBox("Hide this part and all parts that depend on it");
        this.posingHidePart.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingHidePart.setBounds(8, 6, 233, 17);
        
        this.posingXRotationEdit = new JTextField("0");
        this.posingXRotationEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingXRotationEdit.setBounds(27, 65, 30, 21);
        this.posingXRotationEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                changeSelectedPose(event);
            }
        });
        
        this.posingXRotationSpin = new SpinButton("FIX_ME");
        Image posingXRotationSpinImage = toolkit.createImage("../resources/MainForm_posingXRotationSpin.png");
        this.posingXRotationSpin.setUpIcon(new ImageIcon(posingXRotationSpinImage));
        this.posingXRotationSpin.setDownIcon(new ImageIcon(posingXRotationSpinImage));
        this.posingXRotationSpin.setBounds(58, 66, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingXRotationSpin.FocusControl = posingXRotationEdit;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingXRotationSpin.OnUpClick = posingRotationSpinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingXRotationSpin.OnDownClick = posingRotationSpinDown;
        
        this.posingYRotationEdit = new JTextField("0");
        this.posingYRotationEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingYRotationEdit.setBounds(92, 65, 30, 21);
        this.posingYRotationEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                changeSelectedPose(event);
            }
        });
        
        this.posingYRotationSpin = new SpinButton("FIX_ME");
        Image posingYRotationSpinImage = toolkit.createImage("../resources/MainForm_posingYRotationSpin.png");
        this.posingYRotationSpin.setUpIcon(new ImageIcon(posingYRotationSpinImage));
        this.posingYRotationSpin.setDownIcon(new ImageIcon(posingYRotationSpinImage));
        this.posingYRotationSpin.setBounds(123, 66, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingYRotationSpin.FocusControl = posingYRotationEdit;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingYRotationSpin.OnUpClick = posingRotationSpinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingYRotationSpin.OnDownClick = posingRotationSpinDown;
        
        this.posingZRotationEdit = new JTextField("0");
        this.posingZRotationEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingZRotationEdit.setBounds(157, 65, 30, 21);
        this.posingZRotationEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                changeSelectedPose(event);
            }
        });
        
        this.posingZRotationSpin = new SpinButton("FIX_ME");
        Image posingZRotationSpinImage = toolkit.createImage("../resources/MainForm_posingZRotationSpin.png");
        this.posingZRotationSpin.setUpIcon(new ImageIcon(posingZRotationSpinImage));
        this.posingZRotationSpin.setDownIcon(new ImageIcon(posingZRotationSpinImage));
        this.posingZRotationSpin.setBounds(189, 65, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingZRotationSpin.FocusControl = posingZRotationEdit;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingZRotationSpin.OnUpClick = posingRotationSpinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingZRotationSpin.OnDownClick = posingRotationSpinDown;
        
        this.posingAddExtraRotation = new JCheckBox("Add an extra rotation to this part of");
        this.posingAddExtraRotation.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingAddExtraRotation.setBounds(8, 45, 209, 17);
        
        this.posingMultiplyScale = new JCheckBox("Multiply this part''s");
        this.posingMultiplyScale.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingMultiplyScale.setBounds(8, 96, 110, 17);
        
        this.posingMultiplyScaleAllPartsAfter = new JCheckBox("Keep doing this up to the next posed part");
        this.posingMultiplyScaleAllPartsAfter.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingMultiplyScaleAllPartsAfter.setBounds(26, 189, 225, 17);
        
        this.posingScaleMultiplierEdit = new JTextField("0");
        this.posingScaleMultiplierEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingScaleMultiplierEdit.setBounds(118, 116, 40, 21);
        this.posingScaleMultiplierEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                changeSelectedPose(event);
            }
        });
        
        this.posingScaleMultiplierSpin = new SpinButton("FIX_ME");
        Image posingScaleMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingScaleMultiplierSpin.png");
        this.posingScaleMultiplierSpin.setUpIcon(new ImageIcon(posingScaleMultiplierSpinImage));
        this.posingScaleMultiplierSpin.setDownIcon(new ImageIcon(posingScaleMultiplierSpinImage));
        this.posingScaleMultiplierSpin.setBounds(160, 117, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingScaleMultiplierSpin.FocusControl = posingScaleMultiplierEdit;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingScaleMultiplierSpin.OnUpClick = posingScaleMultiplierSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingScaleMultiplierSpin.OnDownClick = posingScaleMultiplierSpinDownClick;
        
        this.posingLengthMultiplierEdit = new JTextField("0");
        this.posingLengthMultiplierEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingLengthMultiplierEdit.setBounds(118, 140, 40, 21);
        this.posingLengthMultiplierEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                changeSelectedPose(event);
            }
        });
        
        this.posingLengthMultiplierSpin = new SpinButton("FIX_ME");
        Image posingLengthMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingLengthMultiplierSpin.png");
        this.posingLengthMultiplierSpin.setUpIcon(new ImageIcon(posingLengthMultiplierSpinImage));
        this.posingLengthMultiplierSpin.setDownIcon(new ImageIcon(posingLengthMultiplierSpinImage));
        this.posingLengthMultiplierSpin.setBounds(160, 141, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingLengthMultiplierSpin.FocusControl = posingLengthMultiplierEdit;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingLengthMultiplierSpin.OnUpClick = posingScaleMultiplierSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingLengthMultiplierSpin.OnDownClick = posingScaleMultiplierSpinDownClick;
        
        this.posingWidthMultiplierEdit = new JTextField("0");
        this.posingWidthMultiplierEdit.addCaretListener(new javax.swing.event.CaretListener() {
            public void caretUpdate(javax.swing.event.CaretEvent event) {
                changeSelectedPose(event);
            }
        });
        this.posingWidthMultiplierEdit.setBounds(118, 164, 40, 21);
        this.posingWidthMultiplierEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                changeSelectedPose(event);
            }
        });
        
        this.posingWidthMultiplierSpin = new SpinButton("FIX_ME");
        Image posingWidthMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingWidthMultiplierSpin.png");
        this.posingWidthMultiplierSpin.setUpIcon(new ImageIcon(posingWidthMultiplierSpinImage));
        this.posingWidthMultiplierSpin.setDownIcon(new ImageIcon(posingWidthMultiplierSpinImage));
        this.posingWidthMultiplierSpin.setBounds(160, 165, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.posingWidthMultiplierSpin.FocusControl = posingWidthMultiplierEdit;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingWidthMultiplierSpin.OnUpClick = posingScaleMultiplierSpinUpClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.posingWidthMultiplierSpin.OnDownClick = posingScaleMultiplierSpinDownClick;
        
        this.posingDetailsPanel = new JPanel(null);
        // -- this.posingDetailsPanel.setLayout(new BoxLayout(this.posingDetailsPanel, BoxLayout.Y_AXIS));
        this.posingDetailsPanel.add(posingXRotationLabel);
        this.posingDetailsPanel.add(posingYRotationLabel);
        this.posingDetailsPanel.add(posingZRotationLabel);
        this.posingDetailsPanel.add(posingScaleMultiplierPercent);
        this.posingDetailsPanel.add(posingScaleMultiplierLabel);
        this.posingDetailsPanel.add(posingLengthMultiplierPercent);
        this.posingDetailsPanel.add(posingLengthMultiplierLabel);
        this.posingDetailsPanel.add(posingWidthMultiplierPercent);
        this.posingDetailsPanel.add(posingWidthMultiplierLabel);
        this.posingDetailsPanel.add(hideExtraLabel);
        this.posingDetailsPanel.add(rotationDegreesLabel);
        this.posingDetailsPanel.add(posingMultiplyScaleAllPartsAfterLabel);
        this.posingDetailsPanel.add(posingHidePart);
        this.posingDetailsPanel.add(posingXRotationEdit);
        this.posingDetailsPanel.add(posingXRotationSpin);
        this.posingDetailsPanel.add(posingYRotationEdit);
        this.posingDetailsPanel.add(posingYRotationSpin);
        this.posingDetailsPanel.add(posingZRotationEdit);
        this.posingDetailsPanel.add(posingZRotationSpin);
        this.posingDetailsPanel.add(posingAddExtraRotation);
        this.posingDetailsPanel.add(posingMultiplyScale);
        this.posingDetailsPanel.add(posingMultiplyScaleAllPartsAfter);
        this.posingDetailsPanel.add(posingScaleMultiplierEdit);
        this.posingDetailsPanel.add(posingScaleMultiplierSpin);
        this.posingDetailsPanel.add(posingLengthMultiplierEdit);
        this.posingDetailsPanel.add(posingLengthMultiplierSpin);
        this.posingDetailsPanel.add(posingWidthMultiplierEdit);
        this.posingDetailsPanel.add(posingWidthMultiplierSpin);
        this.posingDetailsPanel.setBounds(4, 90, 252, 230);
        this.posingDetailsPanel.setVisible(false);
        
        this.posedPlantParts = new JComboBox(new DefaultComboBoxModel());
        this.posedPlantParts.setBounds(65, 20, 103, 22);
        //  --------------- UNHANDLED ATTRIBUTE: this.posedPlantParts.Style = csDropDownList;
        //  --------------- UNHANDLED ATTRIBUTE: this.posedPlantParts.OnChange = posedPlantPartsChange;
        //  --------------- UNHANDLED ATTRIBUTE: this.posedPlantParts.ItemHeight = 14;
        
        this.posingPanel = new JPanel(null);
        // -- this.posingPanel.setLayout(new BoxLayout(this.posingPanel, BoxLayout.Y_AXIS));
        this.posingPanel.add(posingPlantName);
        this.posingPanel.add(posedPartsLabel);
        this.posingPanel.add(posingHighlight);
        this.posingPanel.add(posingGhost);
        this.posingPanel.add(posingNotShown);
        this.posingPanel.add(selectedPartLabel);
        this.posingPanel.add(posingPosePart);
        this.posingPanel.add(posingUnposePart);
        this.posingPanel.add(posingDetailsPanel);
        this.posingPanel.add(posedPlantParts);
        this.posingPanel.setBounds(284, 6, 261, 326);
        this.posingPanel.setVisible(false);
        
        this.plantFocusPanel = new JPanel(null);
        // -- this.plantFocusPanel.setLayout(new BoxLayout(this.plantFocusPanel, BoxLayout.Y_AXIS));
        this.plantFocusPanel.add(animatingLabel);
        this.plantFocusPanel.add(lifeCyclePanel);
        this.plantFocusPanel.add(statsScrollBox);
        // FIX UNHANDLED TYPE -- this.plantFocusPanel.add(this.tabSet);
        this.plantFocusPanel.add(parametersPanel);
        this.plantFocusPanel.add(rotationsPanel);
        this.plantFocusPanel.add(notePanel);
        this.plantFocusPanel.add(posingPanel);
        this.plantFocusPanel.setBounds(158, 38, 550, 457);
        
        //  ------- UNHANDLED TYPE TPrintDialog: PrintDialog 
        //  --------------- UNHANDLED ATTRIBUTE: this.PrintDialog.Top = 179;
        //  --------------- UNHANDLED ATTRIBUTE: this.PrintDialog.Left = 4;
        
        //  ------- UNHANDLED TYPE TTimer: animateTimer 
        //  --------------- UNHANDLED ATTRIBUTE: this.animateTimer.Interval = 100;
        //  --------------- UNHANDLED ATTRIBUTE: this.animateTimer.Enabled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.animateTimer.OnTimer = animateTimerTimer;
        //  --------------- UNHANDLED ATTRIBUTE: this.animateTimer.Top = 212;
        //  --------------- UNHANDLED ATTRIBUTE: this.animateTimer.Left = 7;
        
        this.lifeCyclePanel.addMouseListener(new MenuPopupMouseListener(this.getPlantPopupMenu()));
        this.parametersScrollBox.addMouseListener(new MenuPopupMouseListener(this.getparamPopupMenu()));
        delphiPanel.add(paletteImage);
        delphiPanel.add(visibleBitmap);
        delphiPanel.add(paramPanelOpenArrowImage);
        delphiPanel.add(paramPanelClosedArrowImage);
        delphiPanel.add(fileChangedImage);
        delphiPanel.add(fileNotChangedImage);
        delphiPanel.add(unregisteredExportReminder);
        delphiPanel.add(plantBitmapsGreenImage);
        delphiPanel.add(noPlantBitmapsImage);
        delphiPanel.add(plantBitmapsYellowImage);
        delphiPanel.add(plantBitmapsRedImage);
        delphiPanel.add(posingColorsPanel);
        delphiPanel.add(horizontalSplitter);
        delphiPanel.add(verticalSplitter);
        delphiPanel.add(toolbarPanel);
        delphiPanel.add(plantListPanel);
        delphiPanel.add(sectionImagesPanel);
        JScrollPane scroller2 = new JScrollPane();
        scroller2.setBounds(4, 460, 151, 27);;
        scroller2.setViewportView(plantsAsTextMemo);
        delphiPanel.add(scroller2);
        delphiPanel.add(plantFocusPanel);
        return delphiPanel;
    }
    
        
    public void FormKeyDown(KeyEvent event) {
        System.out.println("FormKeyDown");
    }
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void FormKeyUp(KeyEvent event) {
        System.out.println("FormKeyUp");
    }
        
    public void MenuEditCopyAsTextClick(ActionEvent event) {
        System.out.println("MenuEditCopyAsTextClick");
    }
        
    public void MenuEditCopyClick(ActionEvent event) {
        System.out.println("MenuEditCopyClick");
    }
        
    public void MenuEditCopyDrawingClick(ActionEvent event) {
        System.out.println("MenuEditCopyDrawingClick");
    }
        
    public void MenuEditCutClick(ActionEvent event) {
        System.out.println("MenuEditCutClick");
    }
        
    public void MenuEditDeleteClick(ActionEvent event) {
        System.out.println("MenuEditDeleteClick");
    }
        
    public void MenuEditDuplicateClick(ActionEvent event) {
        System.out.println("MenuEditDuplicateClick");
    }
        
    public void MenuEditPasteAsTextClick(ActionEvent event) {
        System.out.println("MenuEditPasteAsTextClick");
    }
        
    public void MenuEditPasteClick(ActionEvent event) {
        System.out.println("MenuEditPasteClick");
    }
        
    public void MenuEditPreferencesClick(ActionEvent event) {
        System.out.println("MenuEditPreferencesClick");
    }
        
    public void MenuEditRedoClick(ActionEvent event) {
        System.out.println("MenuEditRedoClick");
    }
        
    public void MenuEditUndoClick(ActionEvent event) {
        System.out.println("MenuEditUndoClick");
    }
        
    public void MenuFileCloseClick(ActionEvent event) {
        System.out.println("MenuFileCloseClick");
    }
        
    public void MenuFileExitClick(ActionEvent event) {
        System.out.println("MenuFileExitClick");
    }
        
    public void MenuFileMakePainterAnimationClick(ActionEvent event) {
        System.out.println("MenuFileMakePainterAnimationClick");
    }
        
    public void MenuFileMakePainterNozzleClick(ActionEvent event) {
        System.out.println("MenuFileMakePainterNozzleClick");
    }
        
    public void MenuFileNewClick(ActionEvent event) {
        System.out.println("MenuFileNewClick");
    }
        
    public void MenuFileOpenClick(ActionEvent event) {
        System.out.println("MenuFileOpenClick");
    }
        
    public void MenuFilePlantMoverClick(ActionEvent event) {
        System.out.println("MenuFilePlantMoverClick");
    }
        
    public void MenuFilePrintDrawingClick(ActionEvent event) {
        System.out.println("MenuFilePrintDrawingClick");
    }
        
    public void MenuFileSaveAsClick(ActionEvent event) {
        System.out.println("MenuFileSaveAsClick");
    }
        
    public void MenuFileSaveClick(ActionEvent event) {
        System.out.println("MenuFileSaveClick");
    }
        
    public void MenuFileSaveDrawingAsClick(ActionEvent event) {
        System.out.println("MenuFileSaveDrawingAsClick");
    }
        
    public void MenuFileSaveJPEGClick(ActionEvent event) {
        System.out.println("MenuFileSaveJPEGClick");
    }
        
    public void MenuFileTdoMoverClick(ActionEvent event) {
        System.out.println("MenuFileTdoMoverClick");
    }
        
    public void MenuHelpAboutClick(ActionEvent event) {
        System.out.println("MenuHelpAboutClick");
    }
        
    public void MenuHelpRegisterClick(ActionEvent event) {
        System.out.println("MenuHelpRegisterClick");
    }
        
    public void MenuHelpSuperSpeedTourClick(ActionEvent event) {
        System.out.println("MenuHelpSuperSpeedTourClick");
    }
        
    public void MenuHelpTopicsClick(ActionEvent event) {
        System.out.println("MenuHelpTopicsClick");
    }
        
    public void MenuHelpTutorialClick(ActionEvent event) {
        System.out.println("MenuHelpTutorialClick");
    }
        
    public void MenuLayoutAlignBottomsClick(ActionEvent event) {
        System.out.println("MenuLayoutAlignBottomsClick");
    }
        
    public void MenuLayoutAlignLeftSidesClick(ActionEvent event) {
        System.out.println("MenuLayoutAlignLeftSidesClick");
    }
        
    public void MenuLayoutAlignRightSidesClick(ActionEvent event) {
        System.out.println("MenuLayoutAlignRightSidesClick");
    }
        
    public void MenuLayoutAlignTopsClick(ActionEvent event) {
        System.out.println("MenuLayoutAlignTopsClick");
    }
        
    public void MenuLayoutBringForwardClick(ActionEvent event) {
        System.out.println("MenuLayoutBringForwardClick");
    }
        
    public void MenuLayoutDeselectClick(ActionEvent event) {
        System.out.println("MenuLayoutDeselectClick");
    }
        
    public void MenuLayoutHideClick(ActionEvent event) {
        System.out.println("MenuLayoutHideClick");
    }
        
    public void MenuLayoutHideOthersClick(ActionEvent event) {
        System.out.println("MenuLayoutHideOthersClick");
    }
        
    public void MenuLayoutHorizontalOrientationClick(ActionEvent event) {
        System.out.println("MenuLayoutHorizontalOrientationClick");
    }
        
    public void MenuLayoutMakeBouquetClick(ActionEvent event) {
        System.out.println("MenuLayoutMakeBouquetClick");
    }
        
    public void MenuLayoutPackClick(ActionEvent event) {
        System.out.println("MenuLayoutPackClick");
    }
        
    public void MenuLayoutScaleToFitClick(ActionEvent event) {
        System.out.println("MenuLayoutScaleToFitClick");
    }
        
    public void MenuLayoutSelectAllClick(ActionEvent event) {
        System.out.println("MenuLayoutSelectAllClick");
    }
        
    public void MenuLayoutSendBackClick(ActionEvent event) {
        System.out.println("MenuLayoutSendBackClick");
    }
        
    public void MenuLayoutShowClick(ActionEvent event) {
        System.out.println("MenuLayoutShowClick");
    }
        
    public void MenuLayoutSizeSameHeightClick(ActionEvent event) {
        System.out.println("MenuLayoutSizeSameHeightClick");
    }
        
    public void MenuLayoutSizeSameWidthClick(ActionEvent event) {
        System.out.println("MenuLayoutSizeSameWidthClick");
    }
        
    public void MenuLayoutVerticalOrientationClick(ActionEvent event) {
        System.out.println("MenuLayoutVerticalOrientationClick");
    }
        
    public void MenuLayoutViewFreeFloatingClick(ActionEvent event) {
        System.out.println("MenuLayoutViewFreeFloatingClick");
    }
        
    public void MenuLayoutViewOnePlantAtATimeClick(ActionEvent event) {
        System.out.println("MenuLayoutViewOnePlantAtATimeClick");
    }
        
    public void MenuOptionsBestDrawClick(ActionEvent event) {
        System.out.println("MenuOptionsBestDrawClick");
    }
        
    public void MenuOptionsCustomDrawClick(ActionEvent event) {
        System.out.println("MenuOptionsCustomDrawClick");
    }
        
    public void MenuOptionsFastDrawClick(ActionEvent event) {
        System.out.println("MenuOptionsFastDrawClick");
    }
        
    public void MenuOptionsGhostHiddenPartsClick(ActionEvent event) {
        System.out.println("MenuOptionsGhostHiddenPartsClick");
    }
        
    public void MenuOptionsHidePosingClick(ActionEvent event) {
        System.out.println("MenuOptionsHidePosingClick");
    }
        
    public void MenuOptionsHighlightPosedPartsClick(ActionEvent event) {
        System.out.println("MenuOptionsHighlightPosedPartsClick");
    }
        
    public void MenuOptionsMediumDrawClick(ActionEvent event) {
        System.out.println("MenuOptionsMediumDrawClick");
    }
        
    public void MenuOptionsShowBoundsRectanglesClick(ActionEvent event) {
        System.out.println("MenuOptionsShowBoundsRectanglesClick");
    }
        
    public void MenuOptionsShowLongButtonHintsClick(ActionEvent event) {
        System.out.println("MenuOptionsShowLongButtonHintsClick");
    }
        
    public void MenuOptionsShowParameterHintsClick(ActionEvent event) {
        System.out.println("MenuOptionsShowParameterHintsClick");
    }
        
    public void MenuOptionsShowSelectionRectanglesClick(ActionEvent event) {
        System.out.println("MenuOptionsShowSelectionRectanglesClick");
    }
        
    public void MenuOptionsUsePlantBitmapsClick(ActionEvent event) {
        System.out.println("MenuOptionsUsePlantBitmapsClick");
    }
        
    public void MenuPlantAnimateClick(ActionEvent event) {
        System.out.println("MenuPlantAnimateClick");
    }
        
    public void MenuPlantBreedClick(ActionEvent event) {
        System.out.println("MenuPlantBreedClick");
    }
        
    public void MenuPlantEditNoteClick(ActionEvent event) {
        System.out.println("MenuPlantEditNoteClick");
    }
        
    public void MenuPlantExportTo3DSClick(ActionEvent event) {
        System.out.println("MenuPlantExportTo3DSClick");
    }
        
    public void MenuPlantExportToDXFClick(ActionEvent event) {
        System.out.println("MenuPlantExportToDXFClick");
    }
        
    public void MenuPlantExportToLWOClick(ActionEvent event) {
        System.out.println("MenuPlantExportToLWOClick");
    }
        
    public void MenuPlantExportToOBJClick(ActionEvent event) {
        System.out.println("MenuPlantExportToOBJClick");
    }
        
    public void MenuPlantExportToPOVClick(ActionEvent event) {
        System.out.println("MenuPlantExportToPOVClick");
    }
        
    public void MenuPlantExportToVRMLClick(ActionEvent event) {
        System.out.println("MenuPlantExportToVRMLClick");
    }
        
    public void MenuPlantMakeTimeSeriesClick(ActionEvent event) {
        System.out.println("MenuPlantMakeTimeSeriesClick");
    }
        
    public void MenuPlantNewClick(ActionEvent event) {
        System.out.println("MenuPlantNewClick");
    }
        
    public void MenuPlantNewUsingLastWizardSettingsClick(ActionEvent event) {
        System.out.println("MenuPlantNewUsingLastWizardSettingsClick");
    }
        
    public void MenuPlantRandomizeClick(ActionEvent event) {
        System.out.println("MenuPlantRandomizeClick");
    }
        
    public void MenuPlantRenameClick(ActionEvent event) {
        System.out.println("MenuPlantRenameClick");
    }
        
    public void MenuPlantZeroRotationsClick(ActionEvent event) {
        System.out.println("MenuPlantZeroRotationsClick");
    }
        
    public void MenuWindowBreederClick(ActionEvent event) {
        System.out.println("MenuWindowBreederClick");
    }
        
    public void MenuWindowNumericalExceptionsClick(ActionEvent event) {
        System.out.println("MenuWindowNumericalExceptionsClick");
    }
        
    public void MenuWindowTimeSeriesClick(ActionEvent event) {
        System.out.println("MenuWindowTimeSeriesClick");
    }
        
    public void PopupMenuAnimateClick(ActionEvent event) {
        System.out.println("PopupMenuAnimateClick");
    }
        
    public void PopupMenuBreedClick(ActionEvent event) {
        System.out.println("PopupMenuBreedClick");
    }
        
    public void PopupMenuCopyClick(ActionEvent event) {
        System.out.println("PopupMenuCopyClick");
    }
        
    public void PopupMenuCutClick(ActionEvent event) {
        System.out.println("PopupMenuCutClick");
    }
        
    public void PopupMenuEditNoteClick(ActionEvent event) {
        System.out.println("PopupMenuEditNoteClick");
    }
        
    public void PopupMenuMakeTimeSeriesClick(ActionEvent event) {
        System.out.println("PopupMenuMakeTimeSeriesClick");
    }
        
    public void PopupMenuPasteClick(ActionEvent event) {
        System.out.println("PopupMenuPasteClick");
    }
        
    public void PopupMenuRandomizeClick(ActionEvent event) {
        System.out.println("PopupMenuRandomizeClick");
    }
        
    public void PopupMenuRenameClick(ActionEvent event) {
        System.out.println("PopupMenuRenameClick");
    }
        
    public void PopupMenuZeroRotationsClick(ActionEvent event) {
        System.out.println("PopupMenuZeroRotationsClick");
    }
        
    public void Recent0Click(ActionEvent event) {
        System.out.println("Recent0Click");
    }
        
    public void Reconcile3DObjects1Click(ActionEvent event) {
        System.out.println("Reconcile3DObjects1Click");
    }
        
    public void UndoMenuEditUndoRedoListClick(ActionEvent event) {
        System.out.println("UndoMenuEditUndoRedoListClick");
    }
        
    public void alignBottomsClick(ActionEvent event) {
        System.out.println("alignBottomsClick");
    }
        
    public void alignLeftClick(ActionEvent event) {
        System.out.println("alignLeftClick");
    }
        
    public void alignRightClick(ActionEvent event) {
        System.out.println("alignRightClick");
    }
        
    public void alignTopsClick(ActionEvent event) {
        System.out.println("alignTopsClick");
    }
        
    public void animateGrowthClick(ActionEvent event) {
        System.out.println("animateGrowthClick");
    }
        
    public void centerDrawingClick(ActionEvent event) {
        System.out.println("centerDrawingClick");
    }
        
    public void changeSelectedPose(java.util.EventObject event) {
        System.out.println("changeSelectedPose");
    }
        
    public void dragCursorModeClick(ActionEvent event) {
        System.out.println("dragCursorModeClick");
    }
        
    public void drawingAreaOnSideClick(ActionEvent event) {
        System.out.println("drawingAreaOnSideClick");
    }
        
    public void drawingAreaOnTopClick(ActionEvent event) {
        System.out.println("drawingAreaOnTopClick");
    }
        
    public void drawingScaleEditExit(FocusEvent event) {
        System.out.println("drawingScaleEditExit");
    }
        
    public void horizontalSplitterMouseDown(MouseEvent event) {
        System.out.println("horizontalSplitterMouseDown");
    }
        
    public void horizontalSplitterMouseMove(MouseEvent event) {
        System.out.println("horizontalSplitterMouseMove");
    }
        
    public void horizontalSplitterMouseUp(MouseEvent event) {
        System.out.println("horizontalSplitterMouseUp");
    }
        
    public void lifeCycleDaysEditExit(FocusEvent event) {
        System.out.println("lifeCycleDaysEditExit");
    }
        
    public void lifeCycleDraggerMouseDown(MouseEvent event) {
        System.out.println("lifeCycleDraggerMouseDown");
    }
        
    public void lifeCycleDraggerMouseMove(MouseEvent event) {
        System.out.println("lifeCycleDraggerMouseMove");
    }
        
    public void lifeCycleDraggerMouseUp(MouseEvent event) {
        System.out.println("lifeCycleDraggerMouseUp");
    }
        
    public void magnificationPercentClick(MouseEvent event) {
        System.out.println("magnificationPercentClick");
    }
        
    public void magnificationPercentExit(FocusEvent event) {
        System.out.println("magnificationPercentExit");
    }
        
    public void magnifyCursorModeClick(ActionEvent event) {
        System.out.println("magnifyCursorModeClick");
    }
        
    public void makeEqualHeightClick(ActionEvent event) {
        System.out.println("makeEqualHeightClick");
    }
        
    public void makeEqualWidthClick(ActionEvent event) {
        System.out.println("makeEqualWidthClick");
    }
        
    public void noteEditClick(ActionEvent event) {
        System.out.println("noteEditClick");
    }
        
    public void packPlantsClick(ActionEvent event) {
        System.out.println("packPlantsClick");
    }
        
    public void paramPopupMenuCollapseAllInSectionClick(ActionEvent event) {
        System.out.println("paramPopupMenuCollapseAllInSectionClick");
    }
        
    public void paramPopupMenuCollapseClick(ActionEvent event) {
        System.out.println("paramPopupMenuCollapseClick");
    }
        
    public void paramPopupMenuCopyNameClick(ActionEvent event) {
        System.out.println("paramPopupMenuCopyNameClick");
    }
        
    public void paramPopupMenuExpandAllInSectionClick(ActionEvent event) {
        System.out.println("paramPopupMenuExpandAllInSectionClick");
    }
        
    public void paramPopupMenuExpandClick(ActionEvent event) {
        System.out.println("paramPopupMenuExpandClick");
    }
        
    public void paramPopupMenuHelpClick(ActionEvent event) {
        System.out.println("paramPopupMenuHelpClick");
    }
        
    public void plantBitmapsIndicatorImageClick(MouseEvent event) {
        System.out.println("plantBitmapsIndicatorImageClick");
    }
        
    public void plantListDrawGridKeyDown(KeyEvent event) {
        System.out.println("plantListDrawGridKeyDown");
    }
        
    public void plantListDrawGridMouseDown(MouseEvent event) {
        System.out.println("plantListDrawGridMouseDown");
    }
        
    public void plantListDrawGridMouseUp(MouseEvent event) {
        System.out.println("plantListDrawGridMouseUp");
    }
        
    public void posingBackfaceColorMouseUp(MouseEvent event) {
        System.out.println("posingBackfaceColorMouseUp");
    }
        
    public void posingFrontfaceColorMouseUp(MouseEvent event) {
        System.out.println("posingFrontfaceColorMouseUp");
    }
        
    public void posingGhostClick(ActionEvent event) {
        System.out.println("posingGhostClick");
    }
        
    public void posingHighlightClick(ActionEvent event) {
        System.out.println("posingHighlightClick");
    }
        
    public void posingLineColorMouseUp(MouseEvent event) {
        System.out.println("posingLineColorMouseUp");
    }
        
    public void posingNotShownClick(ActionEvent event) {
        System.out.println("posingNotShownClick");
    }
        
    public void posingPosePartClick(ActionEvent event) {
        System.out.println("posingPosePartClick");
    }
        
    public void posingSelectionCursorModeClick(ActionEvent event) {
        System.out.println("posingSelectionCursorModeClick");
    }
        
    public void posingUnposePartClick(ActionEvent event) {
        System.out.println("posingUnposePartClick");
    }
        
    public void resetRotationsClick(ActionEvent event) {
        System.out.println("resetRotationsClick");
    }
        
    public void rotateCursorModeClick(ActionEvent event) {
        System.out.println("rotateCursorModeClick");
    }
        
    public void scrollCursorModeClick(ActionEvent event) {
        System.out.println("scrollCursorModeClick");
    }
        
    public void sectionPopupMenuHelpClick(ActionEvent event) {
        System.out.println("sectionPopupMenuHelpClick");
    }
        
    public void verticalSplitterMouseDown(MouseEvent event) {
        System.out.println("verticalSplitterMouseDown");
    }
        
    public void verticalSplitterMouseMove(MouseEvent event) {
        System.out.println("verticalSplitterMouseMove");
    }
        
    public void verticalSplitterMouseUp(MouseEvent event) {
        System.out.println("verticalSplitterMouseUp");
    }
        
    public void viewFreeFloatingClick(ActionEvent event) {
        System.out.println("viewFreeFloatingClick");
    }
        
    public void viewOneOnlyClick(ActionEvent event) {
        System.out.println("viewOneOnlyClick");
    }
        
    public void xLocationEditExit(FocusEvent event) {
        System.out.println("xLocationEditExit");
    }
        
    public void xRotationEditChange(CaretEvent event) {
        System.out.println("xRotationEditChange");
    }
        
    public void xRotationEditExit(FocusEvent event) {
        System.out.println("xRotationEditExit");
    }
        
    public void yLocationEditExit(FocusEvent event) {
        System.out.println("yLocationEditExit");
    }
        
    public void yRotationEditChange(CaretEvent event) {
        System.out.println("yRotationEditChange");
    }
        
    public void yRotationEditExit(FocusEvent event) {
        System.out.println("yRotationEditExit");
    }
        
    public void zRotationEditChange(CaretEvent event) {
        System.out.println("zRotationEditChange");
    }
        
    public void zRotationEditExit(FocusEvent event) {
        System.out.println("zRotationEditExit");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                MainWindow thisClass = new MainWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
