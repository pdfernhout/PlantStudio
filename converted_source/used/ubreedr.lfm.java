
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class BreederWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    JTable plantsDrawGrid;
    JPanel emptyWarningPanel;
    JLabel Label1;
    JPanel breederToolbarPanel;
    SpeedButton variationLow;
    SpeedButton variationMedium;
    SpeedButton variationCustom;
    SpeedButton varyColors;
    SpeedButton vary3DObjects;
    SpeedButton helpButton;
    SpeedButton variationHigh;
    SpeedButton variationNoneNumeric;
    SpeedButton breedButton;
    JMenuBar BreederMenu;
    JMenu BreederMenuEdit;
    JMenuItem BreederMenuUndo;
    JMenuItem BreederMenuRedo;
    JMenuItem BreederMenuUndoRedoList;
    JMenuItem N2;
    JMenuItem BreederMenuCopy;
    JMenuItem BreederMenuPaste;
    JMenuItem BreederMenuSendCopyToMainWindow;
    JMenu BreederMenuPlant;
    JMenuItem BreederMenuBreed;
    JMenuItem BreederMenuMakeTimeSeries;
    JMenuItem N1;
    JMenuItem BreederMenuDeleteRow;
    JMenuItem BreederMenuDeleteAll;
    JMenuItem N4;
    JMenuItem BreederMenuRandomize;
    JMenuItem BreederMenuRandomizeAll;
    JMenu BreederMenuOptions;
    JMenu BreederMenuOptionsDrawAs;
    JRadioButtonMenuItem BreederMenuOptionsFastDraw;
    JRadioButtonMenuItem BreederMenuOptionsMediumDraw;
    JRadioButtonMenuItem BreederMenuOptionsBestDraw;
    JRadioButtonMenuItem BreederMenuOptionsCustomDraw;
    JMenu BreederMenuVariation;
    JRadioButtonMenuItem BreederMenuVariationNone;
    JRadioButtonMenuItem BreederMenuVariationLow;
    JRadioButtonMenuItem BreederMenuVariationMedium;
    JRadioButtonMenuItem BreederMenuVariationHigh;
    JRadioButtonMenuItem BreederMenuVariationCustom;
    JRadioButtonMenuItem BreederMenuVaryColors;
    JRadioButtonMenuItem BreederMenuVary3DObjects;
    JMenuItem N6;
    JMenuItem BreederMenuOtherOptions;
    JMenu MenuBreederHelp;
    JMenuItem BreederMenuHelpOnBreeding;
    JMenuItem N3;
    JMenuItem BreederMenuHelpTopics;
    JPopupMenu BreederPopupMenu;
    JMenuItem BreederPopupMenuBreed;
    JMenuItem N5;
    JMenuItem BreederPopupMenuCopy;
    JMenuItem BreederPopupMenuPaste;
    JMenuItem BreederPopupMenuSendCopytoMainWindow;
    JMenuItem N7;
    JMenuItem BreederPopupMenuRandomize;
    JMenuItem BreederPopupMenuMakeTimeSeries;
    JMenuItem N8;
    JMenuItem BreederPopupMenuDeleteRow;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public BreederWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    public JMenuBar getBreederMenu() {
        if (BreederMenu != null) return BreederMenu;
        this.BreederMenu = new JMenuBar();
        this.BreederMenuEdit = new JMenu("Edit");
        this.BreederMenuEdit.setMnemonic('E');
        this.BreederMenu.add(BreederMenuEdit);
        this.BreederMenuUndo = new JMenuItem("Undo");
        this.BreederMenuUndo.setMnemonic(KeyEvent.VK_U);
        this.BreederMenuUndo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuUndoClick(event);
            }
        });
        this.BreederMenuEdit.add(BreederMenuUndo);
        
        this.BreederMenuRedo = new JMenuItem("Redo");
        this.BreederMenuRedo.setMnemonic(KeyEvent.VK_R);
        this.BreederMenuRedo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuRedoClick(event);
            }
        });
        this.BreederMenuEdit.add(BreederMenuRedo);
        
        this.BreederMenuUndoRedoList = new JMenuItem("Undo/Redo List...");
        this.BreederMenuUndoRedoList.setMnemonic(KeyEvent.VK_L);
        this.BreederMenuUndoRedoList.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuUndoRedoListClick(event);
            }
        });
        this.BreederMenuEdit.add(BreederMenuUndoRedoList);
        
        this.BreederMenuEdit.addSeparator();
        
        this.BreederMenuCopy = new JMenuItem("Copy");
        this.BreederMenuCopy.setMnemonic(KeyEvent.VK_C);
        this.BreederMenuCopy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuCopyClick(event);
            }
        });
        this.BreederMenuEdit.add(BreederMenuCopy);
        
        this.BreederMenuPaste = new JMenuItem("Paste");
        this.BreederMenuPaste.setMnemonic(KeyEvent.VK_P);
        this.BreederMenuPaste.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuPasteClick(event);
            }
        });
        this.BreederMenuEdit.add(BreederMenuPaste);
        
        this.BreederMenuSendCopyToMainWindow = new JMenuItem("Send Copy to Main Window");
        this.BreederMenuSendCopyToMainWindow.setMnemonic(KeyEvent.VK_S);
        this.BreederMenuSendCopyToMainWindow.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuSendCopyToMainWindowClick(event);
            }
        });
        this.BreederMenuEdit.add(BreederMenuSendCopyToMainWindow);
        
        
        
        this.BreederMenuPlant = new JMenu("Breed");
        this.BreederMenuPlant.setMnemonic('B');
        this.BreederMenu.add(BreederMenuPlant);
        this.BreederMenuBreed = new JMenuItem("Breed");
        this.BreederMenuBreed.setMnemonic(KeyEvent.VK_B);
        this.BreederMenuBreed.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuBreedClick(event);
            }
        });
        this.BreederMenuPlant.add(BreederMenuBreed);
        
        this.BreederMenuMakeTimeSeries = new JMenuItem("Make Time Series");
        this.BreederMenuMakeTimeSeries.setMnemonic(KeyEvent.VK_T);
        this.BreederMenuMakeTimeSeries.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuMakeTimeSeriesClick(event);
            }
        });
        this.BreederMenuPlant.add(BreederMenuMakeTimeSeries);
        
        this.BreederMenuPlant.addSeparator();
        
        this.BreederMenuDeleteRow = new JMenuItem("Delete Generation");
        this.BreederMenuDeleteRow.setMnemonic(KeyEvent.VK_G);
        this.BreederMenuDeleteRow.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuDeleteRowClick(event);
            }
        });
        this.BreederMenuPlant.add(BreederMenuDeleteRow);
        
        this.BreederMenuDeleteAll = new JMenuItem("Delete All");
        this.BreederMenuDeleteAll.setMnemonic(KeyEvent.VK_A);
        this.BreederMenuDeleteAll.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuDeleteAllClick(event);
            }
        });
        this.BreederMenuPlant.add(BreederMenuDeleteAll);
        
        this.BreederMenuPlant.addSeparator();
        
        this.BreederMenuRandomize = new JMenuItem("Randomize");
        this.BreederMenuRandomize.setMnemonic(KeyEvent.VK_R);
        this.BreederMenuRandomize.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuRandomizeClick(event);
            }
        });
        this.BreederMenuPlant.add(BreederMenuRandomize);
        
        this.BreederMenuRandomizeAll = new JMenuItem("Randomize All");
        this.BreederMenuRandomizeAll.setMnemonic(KeyEvent.VK_L);
        this.BreederMenuRandomizeAll.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuRandomizeAllClick(event);
            }
        });
        this.BreederMenuPlant.add(BreederMenuRandomizeAll);
        
        
        
        this.BreederMenuOptions = new JMenu("Options");
        this.BreederMenuOptions.setMnemonic('O');
        this.BreederMenu.add(BreederMenuOptions);
        this.BreederMenuOptionsDrawAs = new JMenu("Draw Using");
        this.BreederMenuOptionsDrawAs.setMnemonic(KeyEvent.VK_D);
        this.BreederMenuOptions.add(BreederMenuOptionsDrawAs);
        this.BreederMenuOptionsDrawAs.setSelected(false);
        ButtonGroup group = new ButtonGroup();
        this.BreederMenuOptionsFastDraw = new JRadioButtonMenuItem("Bounding Boxes");
        group.add(this.BreederMenuOptionsFastDraw);
        this.BreederMenuOptionsFastDraw.setMnemonic(KeyEvent.VK_B);
        this.BreederMenuOptionsFastDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuOptionsFastDrawClick(event);
            }
        });
        this.BreederMenuOptionsDrawAs.add(BreederMenuOptionsFastDraw);
        this.BreederMenuOptionsFastDraw.setSelected(true);
        
        this.BreederMenuOptionsMediumDraw = new JRadioButtonMenuItem("Wire Frames");
        group.add(this.BreederMenuOptionsMediumDraw);
        this.BreederMenuOptionsMediumDraw.setMnemonic(KeyEvent.VK_W);
        this.BreederMenuOptionsMediumDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuOptionsMediumDrawClick(event);
            }
        });
        this.BreederMenuOptionsDrawAs.add(BreederMenuOptionsMediumDraw);
        this.BreederMenuOptionsMediumDraw.setSelected(false);
        
        this.BreederMenuOptionsBestDraw = new JRadioButtonMenuItem("Solids");
        group.add(this.BreederMenuOptionsBestDraw);
        this.BreederMenuOptionsBestDraw.setMnemonic(KeyEvent.VK_S);
        this.BreederMenuOptionsBestDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuOptionsBestDrawClick(event);
            }
        });
        this.BreederMenuOptionsDrawAs.add(BreederMenuOptionsBestDraw);
        this.BreederMenuOptionsBestDraw.setSelected(false);
        
        this.BreederMenuOptionsCustomDraw = new JRadioButtonMenuItem("Custom...");
        group.add(this.BreederMenuOptionsCustomDraw);
        this.BreederMenuOptionsCustomDraw.setMnemonic(KeyEvent.VK_C);
        this.BreederMenuOptionsCustomDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuOptionsCustomDrawClick(event);
            }
        });
        this.BreederMenuOptionsDrawAs.add(BreederMenuOptionsCustomDraw);
        this.BreederMenuOptionsCustomDraw.setSelected(false);
        
        
        this.BreederMenuVariation = new JMenu("Vary Numbers");
        this.BreederMenuVariation.setMnemonic(KeyEvent.VK_N);
        this.BreederMenuOptions.add(BreederMenuVariation);
        this.BreederMenuVariation.setSelected(false);
        group = new ButtonGroup();
        this.BreederMenuVariationNone = new JRadioButtonMenuItem("None");
        group.add(this.BreederMenuVariationNone);
        this.BreederMenuVariationNone.setMnemonic(KeyEvent.VK_N);
        this.BreederMenuVariationNone.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuVariationNoneClick(event);
            }
        });
        this.BreederMenuVariation.add(BreederMenuVariationNone);
        this.BreederMenuVariationNone.setSelected(false);
        
        this.BreederMenuVariationLow = new JRadioButtonMenuItem("Low");
        group.add(this.BreederMenuVariationLow);
        this.BreederMenuVariationLow.setMnemonic(KeyEvent.VK_L);
        this.BreederMenuVariationLow.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuVariationLowClick(event);
            }
        });
        this.BreederMenuVariation.add(BreederMenuVariationLow);
        this.BreederMenuVariationLow.setSelected(false);
        
        this.BreederMenuVariationMedium = new JRadioButtonMenuItem("Medium");
        group.add(this.BreederMenuVariationMedium);
        this.BreederMenuVariationMedium.setMnemonic(KeyEvent.VK_M);
        this.BreederMenuVariationMedium.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuVariationMediumClick(event);
            }
        });
        this.BreederMenuVariation.add(BreederMenuVariationMedium);
        this.BreederMenuVariationMedium.setSelected(true);
        
        this.BreederMenuVariationHigh = new JRadioButtonMenuItem("High");
        group.add(this.BreederMenuVariationHigh);
        this.BreederMenuVariationHigh.setMnemonic(KeyEvent.VK_H);
        this.BreederMenuVariationHigh.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuVariationHighClick(event);
            }
        });
        this.BreederMenuVariation.add(BreederMenuVariationHigh);
        this.BreederMenuVariationHigh.setSelected(false);
        
        this.BreederMenuVariationCustom = new JRadioButtonMenuItem("Custom...");
        group.add(this.BreederMenuVariationCustom);
        this.BreederMenuVariationCustom.setMnemonic(KeyEvent.VK_C);
        this.BreederMenuVariationCustom.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuVariationCustomClick(event);
            }
        });
        this.BreederMenuVariation.add(BreederMenuVariationCustom);
        this.BreederMenuVariationCustom.setSelected(false);
        
        
        this.BreederMenuVaryColors = new JRadioButtonMenuItem("Vary Colors");
        group.add(this.BreederMenuVaryColors);
        this.BreederMenuVaryColors.setMnemonic(KeyEvent.VK_C);
        this.BreederMenuVaryColors.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuVaryColorsClick(event);
            }
        });
        this.BreederMenuOptions.add(BreederMenuVaryColors);
        this.BreederMenuVaryColors.setSelected(false);
        
        this.BreederMenuVary3DObjects = new JRadioButtonMenuItem("Vary 3D Objects");
        group.add(this.BreederMenuVary3DObjects);
        this.BreederMenuVary3DObjects.setMnemonic(KeyEvent.VK_3);
        this.BreederMenuVary3DObjects.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuVary3DObjectsClick(event);
            }
        });
        this.BreederMenuOptions.add(BreederMenuVary3DObjects);
        this.BreederMenuVary3DObjects.setSelected(false);
        
        this.BreederMenuOptions.addSeparator();
        
        this.BreederMenuOtherOptions = new JMenuItem("More Options...");
        this.BreederMenuOtherOptions.setMnemonic(KeyEvent.VK_M);
        this.BreederMenuOtherOptions.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuOtherOptionsClick(event);
            }
        });
        this.BreederMenuOptions.add(BreederMenuOtherOptions);
        
        
        
        this.MenuBreederHelp = new JMenu("Help");
        this.MenuBreederHelp.setMnemonic('H');
        this.BreederMenu.add(MenuBreederHelp);
        this.BreederMenuHelpOnBreeding = new JMenuItem("Help on Breeding");
        this.BreederMenuHelpOnBreeding.setMnemonic(KeyEvent.VK_B);
        this.BreederMenuHelpOnBreeding.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuHelpOnBreedingClick(event);
            }
        });
        this.MenuBreederHelp.add(BreederMenuHelpOnBreeding);
        
        this.MenuBreederHelp.addSeparator();
        
        this.BreederMenuHelpTopics = new JMenuItem("Help Topics");
        this.BreederMenuHelpTopics.setMnemonic(KeyEvent.VK_H);
        this.BreederMenuHelpTopics.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederMenuHelpTopicsClick(event);
            }
        });
        this.MenuBreederHelp.add(BreederMenuHelpTopics);
        
        
        
        return BreederMenu;
    }
        //  --------------- UNHANDLED ATTRIBUTE: this.BreederMenu.Top = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.BreederMenu.Left = 360;
        
    public JPopupMenu getBreederPopupMenu() {
        if (BreederPopupMenu != null) return BreederPopupMenu;
        this.BreederPopupMenu = new JPopupMenu();
        this.BreederPopupMenuBreed = new JMenuItem("Breed");
        this.BreederPopupMenuBreed.setMnemonic(KeyEvent.VK_B);
        this.BreederPopupMenuBreed.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederPopupMenuBreedClick(event);
            }
        });
        this.BreederPopupMenu.add(BreederPopupMenuBreed);
        
        this.BreederPopupMenu.addSeparator();
        
        this.BreederPopupMenuCopy = new JMenuItem("Copy");
        this.BreederPopupMenuCopy.setMnemonic(KeyEvent.VK_C);
        this.BreederPopupMenuCopy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederPopupMenuCopyClick(event);
            }
        });
        this.BreederPopupMenu.add(BreederPopupMenuCopy);
        
        this.BreederPopupMenuPaste = new JMenuItem("Paste");
        this.BreederPopupMenuPaste.setMnemonic(KeyEvent.VK_P);
        this.BreederPopupMenuPaste.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederPopupMenuPasteClick(event);
            }
        });
        this.BreederPopupMenu.add(BreederPopupMenuPaste);
        
        this.BreederPopupMenuSendCopytoMainWindow = new JMenuItem("Send Copy to Main Window");
        this.BreederPopupMenuSendCopytoMainWindow.setMnemonic(KeyEvent.VK_S);
        this.BreederPopupMenuSendCopytoMainWindow.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederPopupMenuSendCopytoMainWindowClick(event);
            }
        });
        this.BreederPopupMenu.add(BreederPopupMenuSendCopytoMainWindow);
        
        this.BreederPopupMenu.addSeparator();
        
        this.BreederPopupMenuRandomize = new JMenuItem("Randomize");
        this.BreederPopupMenuRandomize.setMnemonic(KeyEvent.VK_R);
        this.BreederPopupMenuRandomize.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederPopupMenuRandomizeClick(event);
            }
        });
        this.BreederPopupMenu.add(BreederPopupMenuRandomize);
        
        this.BreederPopupMenuMakeTimeSeries = new JMenuItem("Make Time Series");
        this.BreederPopupMenuMakeTimeSeries.setMnemonic(KeyEvent.VK_M);
        this.BreederPopupMenuMakeTimeSeries.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederPopupMenuMakeTimeSeriesClick(event);
            }
        });
        this.BreederPopupMenu.add(BreederPopupMenuMakeTimeSeries);
        
        this.BreederPopupMenu.addSeparator();
        
        this.BreederPopupMenuDeleteRow = new JMenuItem("Delete generation");
        this.BreederPopupMenuDeleteRow.setMnemonic(KeyEvent.VK_G);
        this.BreederPopupMenuDeleteRow.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                BreederPopupMenuDeleteRowClick(event);
            }
        });
        this.BreederPopupMenu.add(BreederPopupMenuDeleteRow);
        
        return BreederPopupMenu;
    }
        //  --------------- UNHANDLED ATTRIBUTE: this.BreederPopupMenu.Top = 12;
        //  --------------- UNHANDLED ATTRIBUTE: this.BreederPopupMenu.Left = 396;
        
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setJMenuBar(getBreederMenu());
        this.setContentPane(getMainContentPane());
        this.setTitle("Breeder");
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
        this.setBounds(315, 163, 427, 191  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnDestroy = FormDestroy;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.Menu = BreederMenu;
        //  --------------- UNHANDLED ATTRIBUTE: this.AutoScroll = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poDefaultPosOnly;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        
        
        this.plantsDrawGrid = new JTable(new DefaultTableModel());
        this.plantsDrawGrid.setBounds(2, 48, 345, 141);
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.OnEndDrag = plantsDrawGridEndDrag;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.OnDrawCell = plantsDrawGridDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.OnDragOver = plantsDrawGridDragOver;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.FixedRows = 0;
        this.plantsDrawGrid.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                plantsDrawGridMouseDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.RowCount = 30;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.DefaultRowHeight = 64;
        this.plantsDrawGrid.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                plantsDrawGridMouseUp(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.OnDblClick = plantsDrawGridDblClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsDrawGrid.Options = [goFixedVertLine, goFixedHorzLine, goRangeSelect];
        
        this.Label1 = new JLabel("The breeder is empty. To make some breeder plants, select a plant (or two plants) in the main window and choose Breed from the Plant menu.");
        this.Label1.setBounds(10, 8, 152, 70);
        
        this.emptyWarningPanel = new JPanel(null);
        // -- this.emptyWarningPanel.setLayout(new BoxLayout(this.emptyWarningPanel, BoxLayout.Y_AXIS));
        this.emptyWarningPanel.add(Label1);
        this.emptyWarningPanel.setBounds(362, 46, 183, 93);
        
        Image variationLowImage = toolkit.createImage("../resources/BreederForm_variationLow.png");
        this.variationLow = new SpeedButton(new ImageIcon(variationLowImage));
        this.variationLow.setSelected(true);
        this.variationLow.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                variationLowClick(event);
            }
        });
        this.variationLow.setBounds(74, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.variationLow.GroupIndex = 1;
        
        Image variationMediumImage = toolkit.createImage("../resources/BreederForm_variationMedium.png");
        this.variationMedium = new SpeedButton(new ImageIcon(variationMediumImage));
        this.variationMedium.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                variationMediumClick(event);
            }
        });
        this.variationMedium.setBounds(102, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.variationMedium.GroupIndex = 1;
        
        Image variationCustomImage = toolkit.createImage("../resources/BreederForm_variationCustom.png");
        this.variationCustom = new SpeedButton(new ImageIcon(variationCustomImage));
        this.variationCustom.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                variationCustomClick(event);
            }
        });
        this.variationCustom.setBounds(156, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.variationCustom.GroupIndex = 1;
        
        Image varyColorsImage = toolkit.createImage("../resources/BreederForm_varyColors.png");
        this.varyColors = new SpeedButton(new ImageIcon(varyColorsImage));
        this.varyColors.setSelected(true);
        this.varyColors.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                varyColorsClick(event);
            }
        });
        this.varyColors.setBounds(207, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.varyColors.GroupIndex = 2;
        
        Image vary3DObjectsImage = toolkit.createImage("../resources/BreederForm_vary3DObjects.png");
        this.vary3DObjects = new SpeedButton(new ImageIcon(vary3DObjectsImage));
        this.vary3DObjects.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                vary3DObjectsClick(event);
            }
        });
        this.vary3DObjects.setBounds(239, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.vary3DObjects.GroupIndex = 3;
        
        Image helpButtonImage = toolkit.createImage("../resources/BreederForm_helpButton.png");
        this.helpButton = new SpeedButton(new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setBounds(310, 4, 25, 25);
        
        Image variationHighImage = toolkit.createImage("../resources/BreederForm_variationHigh.png");
        this.variationHigh = new SpeedButton(new ImageIcon(variationHighImage));
        this.variationHigh.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                variationHighClick(event);
            }
        });
        this.variationHigh.setBounds(129, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.variationHigh.GroupIndex = 1;
        
        Image variationNoneNumericImage = toolkit.createImage("../resources/BreederForm_variationNoneNumeric.png");
        this.variationNoneNumeric = new SpeedButton(new ImageIcon(variationNoneNumericImage));
        this.variationNoneNumeric.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                variationNoneNumericClick(event);
            }
        });
        this.variationNoneNumeric.setBounds(47, 4, 25, 25);
        //  --------------- UNHANDLED ATTRIBUTE: this.variationNoneNumeric.GroupIndex = 1;
        
        Image breedButtonImage = toolkit.createImage("../resources/BreederForm_breedButton.png");
        this.breedButton = new SpeedButton(new ImageIcon(breedButtonImage));
        this.breedButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                breedButtonClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.breedButton.setBounds(5, 4, 25, 25);
        
        this.breederToolbarPanel = new JPanel(null);
        // -- this.breederToolbarPanel.setLayout(new BoxLayout(this.breederToolbarPanel, BoxLayout.Y_AXIS));
        this.breederToolbarPanel.add(variationLow);
        this.breederToolbarPanel.add(variationMedium);
        this.breederToolbarPanel.add(variationCustom);
        this.breederToolbarPanel.add(varyColors);
        this.breederToolbarPanel.add(vary3DObjects);
        this.breederToolbarPanel.add(helpButton);
        this.breederToolbarPanel.add(variationHigh);
        this.breederToolbarPanel.add(variationNoneNumeric);
        this.breederToolbarPanel.add(breedButton);
        this.breederToolbarPanel.setBounds(2, 10, 339, 33);
        
        this.plantsDrawGrid.addMouseListener(new MenuPopupMouseListener(this.getBreederPopupMenu()));
        delphiPanel.add(plantsDrawGrid);
        delphiPanel.add(emptyWarningPanel);
        delphiPanel.add(breederToolbarPanel);
        return delphiPanel;
    }
    
        
    public void BreederMenuBreedClick(ActionEvent event) {
        System.out.println("BreederMenuBreedClick");
    }
        
    public void BreederMenuCopyClick(ActionEvent event) {
        System.out.println("BreederMenuCopyClick");
    }
        
    public void BreederMenuDeleteAllClick(ActionEvent event) {
        System.out.println("BreederMenuDeleteAllClick");
    }
        
    public void BreederMenuDeleteRowClick(ActionEvent event) {
        System.out.println("BreederMenuDeleteRowClick");
    }
        
    public void BreederMenuHelpOnBreedingClick(ActionEvent event) {
        System.out.println("BreederMenuHelpOnBreedingClick");
    }
        
    public void BreederMenuHelpTopicsClick(ActionEvent event) {
        System.out.println("BreederMenuHelpTopicsClick");
    }
        
    public void BreederMenuMakeTimeSeriesClick(ActionEvent event) {
        System.out.println("BreederMenuMakeTimeSeriesClick");
    }
        
    public void BreederMenuOptionsBestDrawClick(ActionEvent event) {
        System.out.println("BreederMenuOptionsBestDrawClick");
    }
        
    public void BreederMenuOptionsCustomDrawClick(ActionEvent event) {
        System.out.println("BreederMenuOptionsCustomDrawClick");
    }
        
    public void BreederMenuOptionsFastDrawClick(ActionEvent event) {
        System.out.println("BreederMenuOptionsFastDrawClick");
    }
        
    public void BreederMenuOptionsMediumDrawClick(ActionEvent event) {
        System.out.println("BreederMenuOptionsMediumDrawClick");
    }
        
    public void BreederMenuOtherOptionsClick(ActionEvent event) {
        System.out.println("BreederMenuOtherOptionsClick");
    }
        
    public void BreederMenuPasteClick(ActionEvent event) {
        System.out.println("BreederMenuPasteClick");
    }
        
    public void BreederMenuRandomizeAllClick(ActionEvent event) {
        System.out.println("BreederMenuRandomizeAllClick");
    }
        
    public void BreederMenuRandomizeClick(ActionEvent event) {
        System.out.println("BreederMenuRandomizeClick");
    }
        
    public void BreederMenuRedoClick(ActionEvent event) {
        System.out.println("BreederMenuRedoClick");
    }
        
    public void BreederMenuSendCopyToMainWindowClick(ActionEvent event) {
        System.out.println("BreederMenuSendCopyToMainWindowClick");
    }
        
    public void BreederMenuUndoClick(ActionEvent event) {
        System.out.println("BreederMenuUndoClick");
    }
        
    public void BreederMenuUndoRedoListClick(ActionEvent event) {
        System.out.println("BreederMenuUndoRedoListClick");
    }
        
    public void BreederMenuVariationCustomClick(ActionEvent event) {
        System.out.println("BreederMenuVariationCustomClick");
    }
        
    public void BreederMenuVariationHighClick(ActionEvent event) {
        System.out.println("BreederMenuVariationHighClick");
    }
        
    public void BreederMenuVariationLowClick(ActionEvent event) {
        System.out.println("BreederMenuVariationLowClick");
    }
        
    public void BreederMenuVariationMediumClick(ActionEvent event) {
        System.out.println("BreederMenuVariationMediumClick");
    }
        
    public void BreederMenuVariationNoneClick(ActionEvent event) {
        System.out.println("BreederMenuVariationNoneClick");
    }
        
    public void BreederMenuVary3DObjectsClick(ActionEvent event) {
        System.out.println("BreederMenuVary3DObjectsClick");
    }
        
    public void BreederMenuVaryColorsClick(ActionEvent event) {
        System.out.println("BreederMenuVaryColorsClick");
    }
        
    public void BreederPopupMenuBreedClick(ActionEvent event) {
        System.out.println("BreederPopupMenuBreedClick");
    }
        
    public void BreederPopupMenuCopyClick(ActionEvent event) {
        System.out.println("BreederPopupMenuCopyClick");
    }
        
    public void BreederPopupMenuDeleteRowClick(ActionEvent event) {
        System.out.println("BreederPopupMenuDeleteRowClick");
    }
        
    public void BreederPopupMenuMakeTimeSeriesClick(ActionEvent event) {
        System.out.println("BreederPopupMenuMakeTimeSeriesClick");
    }
        
    public void BreederPopupMenuPasteClick(ActionEvent event) {
        System.out.println("BreederPopupMenuPasteClick");
    }
        
    public void BreederPopupMenuRandomizeClick(ActionEvent event) {
        System.out.println("BreederPopupMenuRandomizeClick");
    }
        
    public void BreederPopupMenuSendCopytoMainWindowClick(ActionEvent event) {
        System.out.println("BreederPopupMenuSendCopytoMainWindowClick");
    }
        
    public void breedButtonClick(ActionEvent event) {
        System.out.println("breedButtonClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void plantsDrawGridMouseDown(MouseEvent event) {
        System.out.println("plantsDrawGridMouseDown");
    }
        
    public void plantsDrawGridMouseUp(MouseEvent event) {
        System.out.println("plantsDrawGridMouseUp");
    }
        
    public void variationCustomClick(ActionEvent event) {
        System.out.println("variationCustomClick");
    }
        
    public void variationHighClick(ActionEvent event) {
        System.out.println("variationHighClick");
    }
        
    public void variationLowClick(ActionEvent event) {
        System.out.println("variationLowClick");
    }
        
    public void variationMediumClick(ActionEvent event) {
        System.out.println("variationMediumClick");
    }
        
    public void variationNoneNumericClick(ActionEvent event) {
        System.out.println("variationNoneNumericClick");
    }
        
    public void vary3DObjectsClick(ActionEvent event) {
        System.out.println("vary3DObjectsClick");
    }
        
    public void varyColorsClick(ActionEvent event) {
        System.out.println("varyColorsClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                BreederWindow thisClass = new BreederWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
