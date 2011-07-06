
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class CustomDrawOptionsWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JButton Close;
    JButton cancel;
    JPanel GroupBox1;
    JCheckBox sortPolygons;
    JCheckBox sortTdosAsOneItem;
    JPanel GroupBox2;
    JCheckBox fillPolygons;
    JCheckBox drawLinesBetweenPolygons;
    JSpinner lineContrastIndex;
    JLabel lineContrastIndexLabel;
    JPanel GroupBox3;
    JCheckBox draw3DObjects;
    JCheckBox drawStems;
    JCheckBox draw3DObjectsAsBoundingRectsOnly;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public CustomDrawOptionsWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Custom Draw Options");
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
        this.setBounds(618, 244, 290, 217  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent event) {
                FormKeyPress(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnActivate = FormActivate;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/CustomDrawOptionsForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(227, 63, 61, 25);
        
        this.Close = new JButton("OK");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.Close.setMnemonic(KeyEvent.VK_O);
        this.Close.setBounds(228, 4, 60, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(228, 27, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.sortPolygons = new JCheckBox("Sort polygons");
        this.sortPolygons.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                sortPolygonsClick(event);
            }
        });
        this.sortPolygons.setMnemonic(KeyEvent.VK_R);
        this.sortPolygons.setBounds(10, 14, 97, 17);
        
        this.sortTdosAsOneItem = new JCheckBox("Sort 3D objects as one item");
        this.sortTdosAsOneItem.setMnemonic(KeyEvent.VK_N);
        this.sortTdosAsOneItem.setBounds(10, 32, 157, 17);
        
        this.GroupBox1 = new JPanel(null);
        // -- this.GroupBox1.setLayout(new BoxLayout(this.GroupBox1, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox1.border = new TitledBorder(""Sorting"");
        this.GroupBox1.add(sortPolygons);
        this.GroupBox1.add(sortTdosAsOneItem);
        this.GroupBox1.setBounds(4, 158, 219, 55);
        
        this.fillPolygons = new JCheckBox("Fill polygons");
        this.fillPolygons.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                fillPolygonsClick(event);
            }
        });
        this.fillPolygons.setMnemonic(KeyEvent.VK_P);
        this.fillPolygons.setBounds(10, 16, 97, 17);
        
        this.drawLinesBetweenPolygons = new JCheckBox("Draw lines between polygons");
        this.drawLinesBetweenPolygons.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                drawLinesBetweenPolygonsClick(event);
            }
        });
        this.drawLinesBetweenPolygons.setMnemonic(KeyEvent.VK_L);
        this.drawLinesBetweenPolygons.setBounds(10, 32, 167, 17);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.lineContrastIndex = new JSpinner(SpinnerNumberModel(10, 0, 10, 1));
        this.lineContrastIndex.setBounds(10, 51, 40, 22);
        
        this.lineContrastIndexLabel = new JLabel("Line contrast index (0-10)", displayedMnemonic=KeyEvent.VK_C, labelFor=this.lineContrastIndex);
        this.lineContrastIndexLabel.setBounds(55, 54, 125, 14);
        
        this.GroupBox2 = new JPanel(null);
        // -- this.GroupBox2.setLayout(new BoxLayout(this.GroupBox2, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox2.border = new TitledBorder(""Filling"");
        this.GroupBox2.add(fillPolygons);
        this.GroupBox2.add(drawLinesBetweenPolygons);
        this.GroupBox2.add(lineContrastIndex);
        this.GroupBox2.add(lineContrastIndexLabel);
        this.GroupBox2.setBounds(4, 76, 219, 81);
        
        this.draw3DObjects = new JCheckBox("Draw 3D objects");
        this.draw3DObjects.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                draw3DObjectsClick(event);
            }
        });
        this.draw3DObjects.setMnemonic(KeyEvent.VK_3);
        this.draw3DObjects.setBounds(8, 32, 117, 17);
        
        this.drawStems = new JCheckBox("Draw stems");
        this.drawStems.setMnemonic(KeyEvent.VK_S);
        this.drawStems.setBounds(8, 15, 97, 17);
        
        this.draw3DObjectsAsBoundingRectsOnly = new JCheckBox("Draw 3D object bounding boxes only");
        this.draw3DObjectsAsBoundingRectsOnly.setMnemonic(KeyEvent.VK_B);
        this.draw3DObjectsAsBoundingRectsOnly.setBounds(8, 49, 203, 17);
        
        this.GroupBox3 = new JPanel(null);
        // -- this.GroupBox3.setLayout(new BoxLayout(this.GroupBox3, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox3.border = new TitledBorder(""Drawing"");
        this.GroupBox3.add(draw3DObjects);
        this.GroupBox3.add(drawStems);
        this.GroupBox3.add(draw3DObjectsAsBoundingRectsOnly);
        this.GroupBox3.setBounds(4, 4, 219, 72);
        
        delphiPanel.add(helpButton);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        delphiPanel.add(GroupBox1);
        delphiPanel.add(GroupBox2);
        delphiPanel.add(GroupBox3);
        return delphiPanel;
    }
    
        
    public void CloseClick(ActionEvent event) {
        System.out.println("CloseClick");
    }
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void draw3DObjectsClick(ActionEvent event) {
        System.out.println("draw3DObjectsClick");
    }
        
    public void drawLinesBetweenPolygonsClick(ActionEvent event) {
        System.out.println("drawLinesBetweenPolygonsClick");
    }
        
    public void fillPolygonsClick(ActionEvent event) {
        System.out.println("fillPolygonsClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void sortPolygonsClick(ActionEvent event) {
        System.out.println("sortPolygonsClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                CustomDrawOptionsWindow thisClass = new CustomDrawOptionsWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
