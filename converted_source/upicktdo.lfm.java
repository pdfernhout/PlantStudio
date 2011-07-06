
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class PickTdoWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JTable grid;
    JButton Close;
    JButton cancel;
    JPanel libraryGroupBox;
    ImagePanel fileChangedImage;
    SpeedButton sectionTdosChangeLibrary;
    JTextField libraryFileName;
    JButton apply;
    JButton newTdo;
    JButton editTdo;
    JButton mover;
    JButton copyTdo;
    JButton deleteTdo;
    JComboBox tdos;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public PickTdoWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Choose a 3D object");
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
        this.setBounds(511, 210, 406, 377  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnClose = FormClose;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/PickTdoForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(334, 245, 60, 21);
        
        this.grid = new JTable(new DefaultTableModel());
        this.grid.setBounds(4, 28, 323, 263);
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.OnDrawCell = gridDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.OnSelectCell = gridSelectCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.FixedRows = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.DefaultColWidth = 60;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.RowCount = 20;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.DefaultRowHeight = 64;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.ScrollBars = ssVertical;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.OnDblClick = gridDblClick;
        //  --------------- UNHANDLED ATTRIBUTE: this.grid.Options = [];
        
        this.Close = new JButton("OK");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.getRootPane().setDefaultButton(this.Close);
        this.Close.setBounds(334, 4, 60, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setBounds(334, 27, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        Image fileChangedImageImage = toolkit.createImage("../resources/PickTdoForm_fileChangedImage.png");
        this.fileChangedImage = new ImagePanel(new ImageIcon(fileChangedImageImage));
        this.fileChangedImage.setBounds(8, 24, 16, 16);
        
        Image sectionTdosChangeLibraryImage = toolkit.createImage("../resources/PickTdoForm_sectionTdosChangeLibrary.png");
        this.sectionTdosChangeLibrary = new SpeedButton("Change...", new ImageIcon(sectionTdosChangeLibraryImage));
        this.sectionTdosChangeLibrary.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                sectionTdosChangeLibraryClick(event);
            }
        });
        this.sectionTdosChangeLibrary.setMnemonic(KeyEvent.VK_C);
        this.sectionTdosChangeLibrary.setBounds(228, 19, 85, 25);
        
        this.libraryFileName = new JTextField("");
        this.libraryFileName.setEditable(false);
        this.libraryFileName.setBounds(30, 22, 193, 22);
        
        this.libraryGroupBox = new JPanel(null);
        // -- this.libraryGroupBox.setLayout(new BoxLayout(this.libraryGroupBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.libraryGroupBox.border = new TitledBorder(""Current library"");
        this.libraryGroupBox.add(fileChangedImage);
        this.libraryGroupBox.add(sectionTdosChangeLibrary);
        this.libraryGroupBox.add(libraryFileName);
        this.libraryGroupBox.setBounds(4, 297, 321, 52);
        
        this.apply = new JButton("Apply");
        this.apply.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                applyClick(event);
            }
        });
        this.apply.setMnemonic(KeyEvent.VK_A);
        this.apply.setBounds(334, 63, 59, 21);
        
        this.newTdo = new JButton("New...");
        this.newTdo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                newTdoClick(event);
            }
        });
        this.newTdo.setMnemonic(KeyEvent.VK_N);
        this.newTdo.setBounds(334, 99, 59, 21);
        
        this.editTdo = new JButton("Edit...");
        this.editTdo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                editTdoClick(event);
            }
        });
        this.editTdo.setMnemonic(KeyEvent.VK_E);
        this.editTdo.setBounds(334, 123, 59, 21);
        
        this.mover = new JButton("Mover...");
        this.mover.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                moverClick(event);
            }
        });
        this.mover.setMnemonic(KeyEvent.VK_M);
        this.mover.setBounds(334, 208, 59, 21);
        
        this.copyTdo = new JButton("Copy...");
        this.copyTdo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyTdoClick(event);
            }
        });
        this.copyTdo.setMnemonic(KeyEvent.VK_C);
        this.copyTdo.setBounds(334, 147, 59, 21);
        
        this.deleteTdo = new JButton("Delete");
        this.deleteTdo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                deleteTdoClick(event);
            }
        });
        this.deleteTdo.setMnemonic(KeyEvent.VK_D);
        this.deleteTdo.setBounds(334, 173, 59, 19);
        
        this.tdos = new JComboBox(new DefaultComboBoxModel());
        this.tdos.setBounds(4, 2, 323, 22);
        //  --------------- UNHANDLED ATTRIBUTE: this.tdos.Style = csDropDownList;
        //  --------------- UNHANDLED ATTRIBUTE: this.tdos.DropDownCount = 12;
        //  --------------- UNHANDLED ATTRIBUTE: this.tdos.OnChange = tdosChange;
        //  --------------- UNHANDLED ATTRIBUTE: this.tdos.ItemHeight = 14;
        
        delphiPanel.add(helpButton);
        delphiPanel.add(grid);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        delphiPanel.add(libraryGroupBox);
        delphiPanel.add(apply);
        delphiPanel.add(newTdo);
        delphiPanel.add(editTdo);
        delphiPanel.add(mover);
        delphiPanel.add(copyTdo);
        delphiPanel.add(deleteTdo);
        delphiPanel.add(tdos);
        return delphiPanel;
    }
    
        
    public void CloseClick(ActionEvent event) {
        System.out.println("CloseClick");
    }
        
    public void applyClick(ActionEvent event) {
        System.out.println("applyClick");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void copyTdoClick(ActionEvent event) {
        System.out.println("copyTdoClick");
    }
        
    public void deleteTdoClick(ActionEvent event) {
        System.out.println("deleteTdoClick");
    }
        
    public void editTdoClick(ActionEvent event) {
        System.out.println("editTdoClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void moverClick(ActionEvent event) {
        System.out.println("moverClick");
    }
        
    public void newTdoClick(ActionEvent event) {
        System.out.println("newTdoClick");
    }
        
    public void sectionTdosChangeLibraryClick(ActionEvent event) {
        System.out.println("sectionTdosChangeLibraryClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                PickTdoWindow thisClass = new PickTdoWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
