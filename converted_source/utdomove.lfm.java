
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class TdoMoverWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    ImagePanel previewImage;
    ImagePanel leftTdoFileChangedIndicator;
    ImagePanel rightTdoFileChangedIndicator;
    SpeedButton helpButton;
    JTextField leftTdoFileNameEdit;
    JButton leftOpenClose;
    JTextField rightTdoFileNameEdit;
    JButton rightOpenClose;
    JButton newFile;
    JButton transfer;
    JButton undo;
    JButton redo;
    JButton rename;
    JButton duplicate;
    JButton delete;
    JTable leftTdoList;
    JTable rightTdoList;
    JButton editTdo;
    JButton close;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public TdoMoverWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("3D Object Mover");
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
        this.setBounds(388, 235, 404, 310  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.AutoScroll = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnClose = FormClose;
        
        
        this.previewImage = new ImagePanel(); // No image was set
        this.previewImage.setBounds(152, 4, 100, 60);
        this.previewImage.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                previewImageMouseUp(event);
            }
        });
        
        Image leftTdoFileChangedIndicatorImage = toolkit.createImage("../resources/TdoMoverForm_leftTdoFileChangedIndicator.png");
        this.leftTdoFileChangedIndicator = new ImagePanel(new ImageIcon(leftTdoFileChangedIndicatorImage));
        this.leftTdoFileChangedIndicator.setBounds(8, 30, 16, 16);
        
        Image rightTdoFileChangedIndicatorImage = toolkit.createImage("../resources/TdoMoverForm_rightTdoFileChangedIndicator.png");
        this.rightTdoFileChangedIndicator = new ImagePanel(new ImageIcon(rightTdoFileChangedIndicatorImage));
        this.rightTdoFileChangedIndicator.setBounds(294, 30, 16, 16);
        
        Image helpButtonImage = toolkit.createImage("../resources/TdoMoverForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(152, 264, 100, 21);
        
        this.leftTdoFileNameEdit = new JTextField("c:\PlantStudio\plants1.pla");
        this.leftTdoFileNameEdit.setEditable(false);
        this.leftTdoFileNameEdit.setBounds(4, 4, 140, 20);
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoFileNameEdit.AutoSelect = False;
        
        this.leftOpenClose = new JButton("Open...");
        this.leftOpenClose.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leftOpenCloseClick(event);
            }
        });
        this.leftOpenClose.setMnemonic(KeyEvent.VK_O);
        this.leftOpenClose.setBounds(30, 26, 50, 21);
        
        this.rightTdoFileNameEdit = new JTextField("c:\PlantStudio\newplants.pla");
        this.rightTdoFileNameEdit.setEditable(false);
        this.rightTdoFileNameEdit.setBounds(257, 4, 140, 20);
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoFileNameEdit.AutoSelect = False;
        
        this.rightOpenClose = new JButton("Open...");
        this.rightOpenClose.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                rightOpenCloseClick(event);
            }
        });
        this.rightOpenClose.setMnemonic(KeyEvent.VK_O);
        this.rightOpenClose.setBounds(280, 28, 50, 21);
        
        this.newFile = new JButton("New...");
        this.newFile.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                newFileClick(event);
            }
        });
        this.newFile.setMnemonic(KeyEvent.VK_N);
        this.newFile.setBounds(345, 28, 50, 21);
        
        this.transfer = new JButton("Transfer >>");
        this.transfer.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                transferClick(event);
            }
        });
        this.transfer.setMnemonic(KeyEvent.VK_T);
        this.transfer.setBounds(152, 76, 100, 21);
        
        this.undo = new JButton("Undo duplicate");
        this.undo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                undoClick(event);
            }
        });
        this.undo.setMnemonic(KeyEvent.VK_U);
        this.undo.setBounds(152, 171, 100, 21);
        
        this.redo = new JButton("Redo last");
        this.redo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                redoClick(event);
            }
        });
        this.redo.setMnemonic(KeyEvent.VK_R);
        this.redo.setBounds(152, 195, 100, 21);
        
        this.rename = new JButton("Rename...");
        this.rename.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                renameClick(event);
            }
        });
        this.rename.setMnemonic(KeyEvent.VK_A);
        this.rename.setBounds(152, 148, 100, 21);
        
        this.duplicate = new JButton("Duplicate");
        this.duplicate.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                duplicateClick(event);
            }
        });
        this.duplicate.setMnemonic(KeyEvent.VK_D);
        this.duplicate.setBounds(152, 100, 100, 21);
        
        this.delete = new JButton("Delete");
        this.delete.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                deleteClick(event);
            }
        });
        this.delete.setMnemonic(KeyEvent.VK_E);
        this.delete.setBounds(152, 124, 100, 21);
        
        this.leftTdoList = new JTable(new DefaultTableModel());
        this.leftTdoList.setBounds(-24, 54, 140, 333);
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.OnEndDrag = leftTdoListEndDrag;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.OnDrawCell = leftTdoListDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.OnDblClick = leftTdoListDblClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.OnDragOver = leftTdoListDragOver;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.FixedRows = 0;
        this.leftTdoList.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent event) {
                leftTdoListKeyDown(event);
            }
        });
        this.leftTdoList.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                leftTdoListMouseDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.ColCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.DefaultRowHeight = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.ScrollBars = ssVertical;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.GridLineWidth = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.leftTdoList.Options = [];
        
        this.rightTdoList = new JTable(new DefaultTableModel());
        this.rightTdoList.setBounds(259, 62, 140, 245);
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.OnEndDrag = rightTdoListEndDrag;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.OnDrawCell = rightTdoListDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.OnDblClick = rightTdoListDblClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.OnDragOver = rightTdoListDragOver;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.FixedRows = 0;
        this.rightTdoList.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyPressed(java.awt.event.KeyEvent event) {
                rightTdoListKeyDown(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.ColCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.DefaultRowHeight = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.rightTdoList.GridLineWidth = 0;
        this.rightTdoList.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                rightTdoListMouseDown(event);
            }
        });
        
        this.editTdo = new JButton("Edit");
        this.editTdo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                editTdoClick(event);
            }
        });
        this.editTdo.setMnemonic(KeyEvent.VK_I);
        this.editTdo.setBounds(153, 219, 100, 21);
        
        this.close = new JButton("Quit");
        this.close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                closeClick(event);
            }
        });
        this.close.setMnemonic(KeyEvent.VK_Q);
        this.close.setBounds(152, 288, 100, 21);
        
        delphiPanel.add(previewImage);
        delphiPanel.add(leftTdoFileChangedIndicator);
        delphiPanel.add(rightTdoFileChangedIndicator);
        delphiPanel.add(helpButton);
        delphiPanel.add(leftTdoFileNameEdit);
        delphiPanel.add(leftOpenClose);
        delphiPanel.add(rightTdoFileNameEdit);
        delphiPanel.add(rightOpenClose);
        delphiPanel.add(newFile);
        delphiPanel.add(transfer);
        delphiPanel.add(undo);
        delphiPanel.add(redo);
        delphiPanel.add(rename);
        delphiPanel.add(duplicate);
        delphiPanel.add(delete);
        delphiPanel.add(leftTdoList);
        delphiPanel.add(rightTdoList);
        delphiPanel.add(editTdo);
        delphiPanel.add(close);
        return delphiPanel;
    }
    
        
    public void closeClick(ActionEvent event) {
        System.out.println("closeClick");
    }
        
    public void deleteClick(ActionEvent event) {
        System.out.println("deleteClick");
    }
        
    public void duplicateClick(ActionEvent event) {
        System.out.println("duplicateClick");
    }
        
    public void editTdoClick(ActionEvent event) {
        System.out.println("editTdoClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void leftOpenCloseClick(ActionEvent event) {
        System.out.println("leftOpenCloseClick");
    }
        
    public void leftTdoListKeyDown(KeyEvent event) {
        System.out.println("leftTdoListKeyDown");
    }
        
    public void leftTdoListMouseDown(MouseEvent event) {
        System.out.println("leftTdoListMouseDown");
    }
        
    public void newFileClick(ActionEvent event) {
        System.out.println("newFileClick");
    }
        
    public void previewImageMouseUp(MouseEvent event) {
        System.out.println("previewImageMouseUp");
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
        
    public void rightTdoListKeyDown(KeyEvent event) {
        System.out.println("rightTdoListKeyDown");
    }
        
    public void rightTdoListMouseDown(MouseEvent event) {
        System.out.println("rightTdoListMouseDown");
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
                TdoMoverWindow thisClass = new TdoMoverWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
