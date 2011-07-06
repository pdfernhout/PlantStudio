
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class MoverWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    ImagePanel previewImage;
    ImagePanel leftPlantFileChangedIndicator;
    ImagePanel rightPlantFileChangedIndicator;
    SpeedButton helpButton;
    JTextField leftPlantFileNameEdit;
    JButton leftOpenClose;
    JTextField rightPlantFileNameEdit;
    JButton rightOpenClose;
    JButton newFile;
    JButton transfer;
    JButton close;
    JButton undo;
    JButton redo;
    JButton cut;
    JButton copy;
    JButton paste;
    JButton rename;
    JButton duplicate;
    JButton delete;
    JTable leftPlantList;
    JTable rightPlantList;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public MoverWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Plant Mover");
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
        this.setBounds(439, 193, 400, 373  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent event) {
                FormKeyDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.AutoScroll = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnClose = FormClose;
        
        
        this.previewImage = new ImagePanel(); // No image was set
        this.previewImage.setBounds(150, 4, 100, 71);
        
        Image leftPlantFileChangedIndicatorImage = toolkit.createImage("../resources/MoverForm_leftPlantFileChangedIndicator.png");
        this.leftPlantFileChangedIndicator = new ImagePanel(new ImageIcon(leftPlantFileChangedIndicatorImage));
        this.leftPlantFileChangedIndicator.setBounds(4, 30, 16, 16);
        
        Image rightPlantFileChangedIndicatorImage = toolkit.createImage("../resources/MoverForm_rightPlantFileChangedIndicator.png");
        this.rightPlantFileChangedIndicator = new ImagePanel(new ImageIcon(rightPlantFileChangedIndicatorImage));
        this.rightPlantFileChangedIndicator.setBounds(262, 30, 16, 16);
        
        Image helpButtonImage = toolkit.createImage("../resources/MoverForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(152, 321, 100, 24);
        
        this.leftPlantFileNameEdit = new JTextField("c:\PlantStudio\plants1.pla");
        this.leftPlantFileNameEdit.setEditable(false);
        this.leftPlantFileNameEdit.setBounds(2, 4, 140, 20);
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantFileNameEdit.AutoSelect = False;
        
        this.leftOpenClose = new JButton("Open...");
        this.leftOpenClose.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leftOpenCloseClick(event);
            }
        });
        this.leftOpenClose.setMnemonic(KeyEvent.VK_O);
        this.leftOpenClose.setBounds(24, 28, 50, 21);
        
        this.rightPlantFileNameEdit = new JTextField("c:\PlantStudio\newplants.pla");
        this.rightPlantFileNameEdit.setEditable(false);
        this.rightPlantFileNameEdit.setBounds(258, 4, 140, 20);
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantFileNameEdit.AutoSelect = False;
        
        this.rightOpenClose = new JButton("Open...");
        this.rightOpenClose.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                rightOpenCloseClick(event);
            }
        });
        this.rightOpenClose.setMnemonic(KeyEvent.VK_O);
        this.rightOpenClose.setBounds(284, 27, 50, 21);
        
        this.newFile = new JButton("New...");
        this.newFile.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                newFileClick(event);
            }
        });
        this.newFile.setMnemonic(KeyEvent.VK_N);
        this.newFile.setBounds(337, 27, 50, 21);
        
        this.transfer = new JButton("Transfer >>");
        this.transfer.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                transferClick(event);
            }
        });
        this.transfer.setMnemonic(KeyEvent.VK_T);
        this.transfer.setBounds(151, 108, 100, 21);
        
        this.close = new JButton("Quit");
        this.close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                closeClick(event);
            }
        });
        this.close.setMnemonic(KeyEvent.VK_Q);
        this.close.setBounds(151, 349, 100, 21);
        
        this.undo = new JButton("Undo duplicate");
        this.undo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                undoClick(event);
            }
        });
        this.undo.setMnemonic(KeyEvent.VK_U);
        this.undo.setBounds(151, 273, 100, 21);
        
        this.redo = new JButton("Redo last");
        this.redo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                redoClick(event);
            }
        });
        this.redo.setMnemonic(KeyEvent.VK_R);
        this.redo.setBounds(151, 297, 100, 21);
        
        this.cut = new JButton("Cut (Ctrl-X)");
        this.cut.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cutClick(event);
            }
        });
        this.cut.setMnemonic(KeyEvent.VK_C);
        this.cut.setBounds(151, 132, 100, 21);
        
        this.copy = new JButton("Copy (Ctrl-C)");
        this.copy.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyClick(event);
            }
        });
        this.copy.setMnemonic(KeyEvent.VK_O);
        this.copy.setBounds(151, 155, 100, 21);
        
        this.paste = new JButton("Paste (Ctrl-V)");
        this.paste.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                pasteClick(event);
            }
        });
        this.paste.setMnemonic(KeyEvent.VK_P);
        this.paste.setBounds(151, 179, 100, 21);
        
        this.rename = new JButton("Rename...");
        this.rename.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                renameClick(event);
            }
        });
        this.rename.setMnemonic(KeyEvent.VK_A);
        this.rename.setBounds(151, 250, 100, 21);
        
        this.duplicate = new JButton("Duplicate");
        this.duplicate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                duplicateClick(event);
            }
        });
        this.duplicate.setMnemonic(KeyEvent.VK_D);
        this.duplicate.setBounds(151, 202, 100, 21);
        
        this.delete = new JButton("Delete");
        this.delete.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                deleteClick(event);
            }
        });
        this.delete.setMnemonic(KeyEvent.VK_E);
        this.delete.setBounds(151, 226, 100, 21);
        
        this.leftPlantList = new JTable(new DefaultTableModel());
        this.leftPlantList.setBounds(4, 52, 140, 315);
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.OnEndDrag = leftPlantListEndDrag;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.OnDrawCell = leftPlantListDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.OnDblClick = leftPlantListDblClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.OnDragOver = leftPlantListDragOver;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.FixedRows = 0;
        this.leftPlantList.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent event) {
                leftPlantListKeyDown(event);
            }
        });
        this.leftPlantList.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                leftPlantListMouseDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.ColCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.DefaultRowHeight = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.ScrollBars = ssVertical;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.GridLineWidth = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftPlantList.Options = [];
        
        this.rightPlantList = new JTable(new DefaultTableModel());
        this.rightPlantList.setBounds(258, 52, 140, 317);
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.OnEndDrag = rightPlantListEndDrag;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.OnDrawCell = rightPlantListDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.OnDblClick = rightPlantListDblClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.OnDragOver = rightPlantListDragOver;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.FixedRows = 0;
        this.rightPlantList.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent event) {
                rightPlantListKeyDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.ColCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.DefaultRowHeight = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightPlantList.GridLineWidth = 0;
        this.rightPlantList.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                rightPlantListMouseDown(event);
            }
        });
        
        delphiPanel.add(previewImage);
        delphiPanel.add(leftPlantFileChangedIndicator);
        delphiPanel.add(rightPlantFileChangedIndicator);
        delphiPanel.add(helpButton);
        delphiPanel.add(leftPlantFileNameEdit);
        delphiPanel.add(leftOpenClose);
        delphiPanel.add(rightPlantFileNameEdit);
        delphiPanel.add(rightOpenClose);
        delphiPanel.add(newFile);
        delphiPanel.add(transfer);
        delphiPanel.add(close);
        delphiPanel.add(undo);
        delphiPanel.add(redo);
        delphiPanel.add(cut);
        delphiPanel.add(copy);
        delphiPanel.add(paste);
        delphiPanel.add(rename);
        delphiPanel.add(duplicate);
        delphiPanel.add(delete);
        delphiPanel.add(leftPlantList);
        delphiPanel.add(rightPlantList);
        return delphiPanel;
    }
    
        
    public void FormKeyDown(KeyEvent event) {
        System.out.println("FormKeyDown");
    }
        
    public void closeClick(ActionEvent event) {
        System.out.println("closeClick");
    }
        
    public void copyClick(ActionEvent event) {
        System.out.println("copyClick");
    }
        
    public void cutClick(ActionEvent event) {
        System.out.println("cutClick");
    }
        
    public void deleteClick(ActionEvent event) {
        System.out.println("deleteClick");
    }
        
    public void duplicateClick(ActionEvent event) {
        System.out.println("duplicateClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void leftOpenCloseClick(ActionEvent event) {
        System.out.println("leftOpenCloseClick");
    }
        
    public void leftPlantListKeyDown(KeyEvent event) {
        System.out.println("leftPlantListKeyDown");
    }
        
    public void leftPlantListMouseDown(MouseEvent event) {
        System.out.println("leftPlantListMouseDown");
    }
        
    public void newFileClick(ActionEvent event) {
        System.out.println("newFileClick");
    }
        
    public void pasteClick(ActionEvent event) {
        System.out.println("pasteClick");
    }
        
    public void redoClick(ActionEvent event) {
        System.out.println("redoClick");
    }
        
    public void renameClick(ActionEvent event) {
        System.out.println("renameClick");
    }
        
    public void rightOpenCloseClick(ActionEvent event) {
        System.out.println("rightOpenCloseClick");
    }
        
    public void rightPlantListKeyDown(KeyEvent event) {
        System.out.println("rightPlantListKeyDown");
    }
        
    public void rightPlantListMouseDown(MouseEvent event) {
        System.out.println("rightPlantListMouseDown");
    }
        
    public void transferClick(ActionEvent event) {
        System.out.println("transferClick");
    }
        
    public void undoClick(ActionEvent event) {
        System.out.println("undoClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                MoverWindow thisClass = new MoverWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
