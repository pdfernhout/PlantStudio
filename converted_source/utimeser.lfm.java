
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class TimeSeriesWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    JTable grid;
    JPanel emptyWarningPanel;
    JLabel Label1;
    JMenuBar MainMenu1;
    JMenu TimeSeriesMenuEdit;
    JMenuItem TimeSeriesMenuUndo;
    JMenuItem TimeSeriesMenuRedo;
    JMenuItem TimeSeriesMenuUndoRedoList;
    JMenuItem N1;
    JMenuItem TimeSeriesMenuCopy;
    JMenuItem TimeSeriesMenuPaste;
    JMenuItem TimeSeriesMenuSendCopy;
    JMenuItem N3;
    JMenuItem TimeSeriesMenuBreed;
    JMenuItem N4;
    JMenuItem TimeSeriesMenuDelete;
    JMenu TimeSeriesMenuOptions;
    JMenu TimeSeriesMenuOptionsDrawAs;
    JRadioButtonMenuItem TimeSeriesMenuOptionsFastDraw;
    JRadioButtonMenuItem TimeSeriesMenuOptionsMediumDraw;
    JRadioButtonMenuItem TimeSeriesMenuOptionsBestDraw;
    JRadioButtonMenuItem TimeSeriesMenuOptionsCustomDraw;
    JMenuItem TimeSeriesMenuOptionsStages;
    JMenu TimeSeriesMenuHelp;
    JMenuItem TimeSeriesMenuHelpOnTimeSeries;
    JMenuItem N5;
    JMenuItem TimeSeriesMenuHelpTopics;
    JPopupMenu TimeSeriesPopupMenu;
    JMenuItem TimeSeriesPopupMenuCopy;
    JMenuItem TimeSeriesPopupMenuPaste;
    JMenuItem TimeSeriesPopupMenuSendCopy;
    JMenuItem N2;
    JMenuItem TimeSeriesPopupMenuBreed;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public TimeSeriesWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    public JMenuBar getMainMenu1() {
        if (MainMenu1 != null) return MainMenu1;
        this.MainMenu1 = new JMenuBar();
        this.TimeSeriesMenuEdit = new JMenu("Edit");
        this.TimeSeriesMenuEdit.setMnemonic('E');
        this.MainMenu1.add(TimeSeriesMenuEdit);
        this.TimeSeriesMenuUndo = new JMenuItem("Undo");
        this.TimeSeriesMenuUndo.setMnemonic(KeyEvent.VK_U);
        this.TimeSeriesMenuUndo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuUndoClick(event);
            }
        });
        this.TimeSeriesMenuEdit.add(TimeSeriesMenuUndo);
        
        this.TimeSeriesMenuRedo = new JMenuItem("Redo");
        this.TimeSeriesMenuRedo.setMnemonic(KeyEvent.VK_R);
        this.TimeSeriesMenuRedo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuRedoClick(event);
            }
        });
        this.TimeSeriesMenuEdit.add(TimeSeriesMenuRedo);
        
        this.TimeSeriesMenuUndoRedoList = new JMenuItem("Undo/Redo List...");
        this.TimeSeriesMenuUndoRedoList.setMnemonic(KeyEvent.VK_L);
        this.TimeSeriesMenuUndoRedoList.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuUndoRedoListClick(event);
            }
        });
        this.TimeSeriesMenuEdit.add(TimeSeriesMenuUndoRedoList);
        
        this.TimeSeriesMenuEdit.addSeparator();
        
        this.TimeSeriesMenuCopy = new JMenuItem("Copy");
        this.TimeSeriesMenuCopy.setMnemonic(KeyEvent.VK_C);
        this.TimeSeriesMenuCopy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuCopyClick(event);
            }
        });
        this.TimeSeriesMenuEdit.add(TimeSeriesMenuCopy);
        
        this.TimeSeriesMenuPaste = new JMenuItem("Paste");
        this.TimeSeriesMenuPaste.setMnemonic(KeyEvent.VK_P);
        this.TimeSeriesMenuPaste.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuPasteClick(event);
            }
        });
        this.TimeSeriesMenuEdit.add(TimeSeriesMenuPaste);
        
        this.TimeSeriesMenuSendCopy = new JMenuItem("Send Copy to Main Window");
        this.TimeSeriesMenuSendCopy.setMnemonic(KeyEvent.VK_S);
        this.TimeSeriesMenuSendCopy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuSendCopyClick(event);
            }
        });
        this.TimeSeriesMenuEdit.add(TimeSeriesMenuSendCopy);
        
        this.TimeSeriesMenuEdit.addSeparator();
        
        this.TimeSeriesMenuBreed = new JMenuItem("Breed");
        this.TimeSeriesMenuBreed.setMnemonic(KeyEvent.VK_B);
        this.TimeSeriesMenuBreed.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuBreedClick(event);
            }
        });
        this.TimeSeriesMenuEdit.add(TimeSeriesMenuBreed);
        
        this.TimeSeriesMenuEdit.addSeparator();
        
        this.TimeSeriesMenuDelete = new JMenuItem("Delete Time Series");
        this.TimeSeriesMenuDelete.setMnemonic(KeyEvent.VK_D);
        this.TimeSeriesMenuDelete.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuDeleteClick(event);
            }
        });
        this.TimeSeriesMenuEdit.add(TimeSeriesMenuDelete);
        
        
        
        this.TimeSeriesMenuOptions = new JMenu("Options");
        this.TimeSeriesMenuOptions.setMnemonic('O');
        this.MainMenu1.add(TimeSeriesMenuOptions);
        this.TimeSeriesMenuOptionsDrawAs = new JMenu("Draw Using");
        this.TimeSeriesMenuOptionsDrawAs.setMnemonic(KeyEvent.VK_D);
        this.TimeSeriesMenuOptions.add(TimeSeriesMenuOptionsDrawAs);
        this.TimeSeriesMenuOptionsDrawAs.setSelected(false);
        ButtonGroup group = new ButtonGroup();
        this.TimeSeriesMenuOptionsFastDraw = new JRadioButtonMenuItem("Bounding Boxes");
        group.add(this.TimeSeriesMenuOptionsFastDraw);
        this.TimeSeriesMenuOptionsFastDraw.setMnemonic(KeyEvent.VK_B);
        this.TimeSeriesMenuOptionsFastDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuOptionsFastDrawClick(event);
            }
        });
        this.TimeSeriesMenuOptionsDrawAs.add(TimeSeriesMenuOptionsFastDraw);
        this.TimeSeriesMenuOptionsFastDraw.setSelected(false);
        
        this.TimeSeriesMenuOptionsMediumDraw = new JRadioButtonMenuItem("Wire Frames");
        group.add(this.TimeSeriesMenuOptionsMediumDraw);
        this.TimeSeriesMenuOptionsMediumDraw.setMnemonic(KeyEvent.VK_W);
        this.TimeSeriesMenuOptionsMediumDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuOptionsMediumDrawClick(event);
            }
        });
        this.TimeSeriesMenuOptionsDrawAs.add(TimeSeriesMenuOptionsMediumDraw);
        this.TimeSeriesMenuOptionsMediumDraw.setSelected(false);
        
        this.TimeSeriesMenuOptionsBestDraw = new JRadioButtonMenuItem("Solids");
        group.add(this.TimeSeriesMenuOptionsBestDraw);
        this.TimeSeriesMenuOptionsBestDraw.setMnemonic(KeyEvent.VK_S);
        this.TimeSeriesMenuOptionsBestDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuOptionsBestDrawClick(event);
            }
        });
        this.TimeSeriesMenuOptionsDrawAs.add(TimeSeriesMenuOptionsBestDraw);
        this.TimeSeriesMenuOptionsBestDraw.setSelected(false);
        
        this.TimeSeriesMenuOptionsCustomDraw = new JRadioButtonMenuItem("Custom...");
        group.add(this.TimeSeriesMenuOptionsCustomDraw);
        this.TimeSeriesMenuOptionsCustomDraw.setMnemonic(KeyEvent.VK_C);
        this.TimeSeriesMenuOptionsCustomDraw.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuOptionsCustomDrawClick(event);
            }
        });
        this.TimeSeriesMenuOptionsDrawAs.add(TimeSeriesMenuOptionsCustomDraw);
        this.TimeSeriesMenuOptionsCustomDraw.setSelected(false);
        
        
        this.TimeSeriesMenuOptionsStages = new JMenuItem("More Options...");
        this.TimeSeriesMenuOptionsStages.setMnemonic(KeyEvent.VK_M);
        this.TimeSeriesMenuOptionsStages.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuOptionsStagesClick(event);
            }
        });
        this.TimeSeriesMenuOptions.add(TimeSeriesMenuOptionsStages);
        
        
        
        this.TimeSeriesMenuHelp = new JMenu("Help");
        this.TimeSeriesMenuHelp.setMnemonic('H');
        this.MainMenu1.add(TimeSeriesMenuHelp);
        this.TimeSeriesMenuHelpOnTimeSeries = new JMenuItem("Help on Time Series");
        this.TimeSeriesMenuHelpOnTimeSeries.setMnemonic(KeyEvent.VK_T);
        this.TimeSeriesMenuHelpOnTimeSeries.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuHelpOnTimeSeriesClick(event);
            }
        });
        this.TimeSeriesMenuHelp.add(TimeSeriesMenuHelpOnTimeSeries);
        
        this.TimeSeriesMenuHelp.addSeparator();
        
        this.TimeSeriesMenuHelpTopics = new JMenuItem("Help Topics");
        this.TimeSeriesMenuHelpTopics.setMnemonic(KeyEvent.VK_H);
        this.TimeSeriesMenuHelpTopics.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuHelpTopicsClick(event);
            }
        });
        this.TimeSeriesMenuHelp.add(TimeSeriesMenuHelpTopics);
        
        
        
        return MainMenu1;
    }
        //  --------------- UNHANDLED ATTRIBUTE: this.MainMenu1.Top = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.MainMenu1.Left = 478;
        
    public JPopupMenu getTimeSeriesPopupMenu() {
        if (TimeSeriesPopupMenu != null) return TimeSeriesPopupMenu;
        this.TimeSeriesPopupMenu = new JPopupMenu();
        this.TimeSeriesPopupMenuCopy = new JMenuItem("Copy");
        this.TimeSeriesPopupMenuCopy.setMnemonic(KeyEvent.VK_C);
        this.TimeSeriesPopupMenuCopy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesPopupMenuCopyClick(event);
            }
        });
        this.TimeSeriesPopupMenu.add(TimeSeriesPopupMenuCopy);
        
        this.TimeSeriesPopupMenuPaste = new JMenuItem("Paste");
        this.TimeSeriesPopupMenuPaste.setMnemonic(KeyEvent.VK_P);
        this.TimeSeriesPopupMenuPaste.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesPopupMenuPasteClick(event);
            }
        });
        this.TimeSeriesPopupMenu.add(TimeSeriesPopupMenuPaste);
        
        this.TimeSeriesPopupMenuSendCopy = new JMenuItem("Send Copy to Main Window");
        this.TimeSeriesPopupMenuSendCopy.setMnemonic(KeyEvent.VK_S);
        this.TimeSeriesPopupMenuSendCopy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesMenuSendCopyClick(event);
            }
        });
        this.TimeSeriesPopupMenu.add(TimeSeriesPopupMenuSendCopy);
        
        this.TimeSeriesPopupMenu.addSeparator();
        
        this.TimeSeriesPopupMenuBreed = new JMenuItem("Breed");
        this.TimeSeriesPopupMenuBreed.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                TimeSeriesPopupMenuBreedClick(event);
            }
        });
        this.TimeSeriesPopupMenu.add(TimeSeriesPopupMenuBreed);
        
        return TimeSeriesPopupMenu;
    }
        //  --------------- UNHANDLED ATTRIBUTE: this.TimeSeriesPopupMenu.Top = 38;
        //  --------------- UNHANDLED ATTRIBUTE: this.TimeSeriesPopupMenu.Left = 468;
        
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setJMenuBar(getMainMenu1());
        this.setContentPane(getMainContentPane());
        this.setTitle("Time series");
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
        this.setBounds(366, 184, 520, 119  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        //  --------------- UNHANDLED ATTRIBUTE: this.Menu = MainMenu1;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnDestroy = FormDestroy;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        
        
        this.grid = new JTable(new DefaultTableModel());
        this.grid.setBounds(8, 4, 185, 67);
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.OnEndDrag = gridEndDrag;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.OnDrawCell = gridDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.RowCount = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.OnDragOver = gridDragOver;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.FixedRows = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.ColCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.DefaultRowHeight = 64;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.FixedCols = 0;
        this.grid.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                gridMouseDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.Options = [goFixedVertLine, goFixedHorzLine];
        
        this.Label1 = new JLabel("The time series window is empty. To fill it, select a plant in the main window and choose Make Time Series from the Plant menu.");
        this.Label1.setBounds(8, 8, 221, 42);
        
        this.emptyWarningPanel = new JPanel(null);
        // -- this.emptyWarningPanel.setLayout(new BoxLayout(this.emptyWarningPanel, BoxLayout.Y_AXIS));
        this.emptyWarningPanel.add(Label1);
        this.emptyWarningPanel.setBounds(206, 10, 241, 57);
        
        this.grid.addMouseListener(new MenuPopupMouseListener(this.getTimeSeriesPopupMenu()));
        delphiPanel.add(grid);
        delphiPanel.add(emptyWarningPanel);
        return delphiPanel;
    }
    
        
    public void TimeSeriesMenuBreedClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuBreedClick");
    }
        
    public void TimeSeriesMenuCopyClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuCopyClick");
    }
        
    public void TimeSeriesMenuDeleteClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuDeleteClick");
    }
        
    public void TimeSeriesMenuHelpOnTimeSeriesClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuHelpOnTimeSeriesClick");
    }
        
    public void TimeSeriesMenuHelpTopicsClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuHelpTopicsClick");
    }
        
    public void TimeSeriesMenuOptionsBestDrawClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuOptionsBestDrawClick");
    }
        
    public void TimeSeriesMenuOptionsCustomDrawClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuOptionsCustomDrawClick");
    }
        
    public void TimeSeriesMenuOptionsFastDrawClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuOptionsFastDrawClick");
    }
        
    public void TimeSeriesMenuOptionsMediumDrawClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuOptionsMediumDrawClick");
    }
        
    public void TimeSeriesMenuOptionsStagesClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuOptionsStagesClick");
    }
        
    public void TimeSeriesMenuPasteClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuPasteClick");
    }
        
    public void TimeSeriesMenuRedoClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuRedoClick");
    }
        
    public void TimeSeriesMenuSendCopyClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuSendCopyClick");
    }
        
    public void TimeSeriesMenuUndoClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuUndoClick");
    }
        
    public void TimeSeriesMenuUndoRedoListClick(ActionEvent event) {
        System.out.println("TimeSeriesMenuUndoRedoListClick");
    }
        
    public void TimeSeriesPopupMenuBreedClick(ActionEvent event) {
        System.out.println("TimeSeriesPopupMenuBreedClick");
    }
        
    public void TimeSeriesPopupMenuCopyClick(ActionEvent event) {
        System.out.println("TimeSeriesPopupMenuCopyClick");
    }
        
    public void TimeSeriesPopupMenuPasteClick(ActionEvent event) {
        System.out.println("TimeSeriesPopupMenuPasteClick");
    }
        
    public void gridMouseDown(MouseEvent event) {
        System.out.println("gridMouseDown");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                TimeSeriesWindow thisClass = new TimeSeriesWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
