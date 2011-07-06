
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class UndoRedoListWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JLabel undoListLabel;
    JLabel redoListLabel;
    JButton OK;
    JButton cancel;
    JList undoList;
    JList redoList;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public UndoRedoListWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Undo/Redo List");
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
        this.setBounds(384, 254, 467, 255  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 13;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnResize = FormResize;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.AutoScroll = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poDefaultPosOnly;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnClose = FormClose;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/UndoRedoListForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(385, 69, 80, 25);
        
        this.undoListLabel = new JLabel("Things you can Undo", displayedMnemonic=KeyEvent.VK_U);
        this.undoListLabel.setBounds(4, 4, 102, 13);
        
        this.redoListLabel = new JLabel("Things you can Redo", displayedMnemonic=KeyEvent.VK_R);
        this.redoListLabel.setBounds(4, 122, 102, 13);
        
        this.OK = new JButton("Undo/Redo");
        this.OK.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                OKClick(event);
            }
        });
        this.OK.setMnemonic(KeyEvent.VK_D);
        this.OK.setBounds(385, 4, 80, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(385, 30, 80, 21);
        
        this.undoList = new JList(new DefaultListModel());
        this.undoList.setFixedCellHeight(13);
        this.undoList.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                regulateListSelections(event);
            }
        });
        this.undoList.setBounds(4, 20, 375, 97);
        //  --------------- UNHANDLED ATTRIBUTE: this.undoList.MultiSelect = True;
        
        this.redoList = new JList(new DefaultListModel());
        this.redoList.setFixedCellHeight(13);
        this.redoList.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                regulateListSelections(event);
            }
        });
        this.redoList.setBounds(4, 140, 373, 107);
        //  --------------- UNHANDLED ATTRIBUTE: this.redoList.MultiSelect = True;
        
        delphiPanel.add(helpButton);
        delphiPanel.add(undoListLabel);
        delphiPanel.add(redoListLabel);
        delphiPanel.add(OK);
        delphiPanel.add(cancel);
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(4, 20, 375, 97);;
        scroller1.setViewportView(undoList);
        delphiPanel.add(scroller1);
        JScrollPane scroller2 = new JScrollPane();
        scroller2.setBounds(4, 140, 373, 107);;
        scroller2.setViewportView(redoList);
        delphiPanel.add(scroller2);
        return delphiPanel;
    }
    
        
    public void OKClick(ActionEvent event) {
        System.out.println("OKClick");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void regulateListSelections(MouseEvent event) {
        System.out.println("regulateListSelections");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                UndoRedoListWindow thisClass = new UndoRedoListWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
