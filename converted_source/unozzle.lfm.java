
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class NozzleOptionsWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JPanel GroupBox1;
    JLabel cellCountLabel;
    JLabel cellSizeLabel;
    JLabel fileSizeLabel;
    JButton Close;
    JButton cancel;
    JPanel Panel1;
    JLabel Label4;
    JPanel GroupBox2;
    JLabel Label1;
    JPanel backgroundColorPanel;
    JLabel Label3;
    JSpinner resolutionEdit;
    JLabel resolutionLabel;
    JComboBox colorType;
    JLabel colorsLabel;
    JPanel GroupBox3;
    JRadioButton useSelectedPlants;
    JRadioButton useVisiblePlants;
    JRadioButton useAllPlants;
    // UNHANDLED_TYPE ColorDialog;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public NozzleOptionsWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Save Nozzle/Tube Bitmap");
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
        this.setBounds(521, 265, 350, 373  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.KeyPreview = True;
        this.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyTyped(java.awt.event.KeyEvent event) {
                FormKeyPress(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/NozzleOptionsForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(287, 61, 60, 21);
        
        this.cellCountLabel = new JLabel("Number of items:  5");
        this.cellCountLabel.setBounds(7, 27, 93, 14);
        
        this.cellSizeLabel = new JLabel("Nozzle/tube cell width:  345 height:  534");
        this.cellSizeLabel.setBounds(7, 11, 192, 14);
        
        this.fileSizeLabel = new JLabel("Estimated file size:  2433 K");
        this.fileSizeLabel.setBounds(7, 42, 129, 14);
        
        this.GroupBox1 = new JPanel(null);
        // -- this.GroupBox1.setLayout(new BoxLayout(this.GroupBox1, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox1.border = new TitledBorder("Untitled Group");
        this.GroupBox1.add(cellCountLabel);
        this.GroupBox1.add(cellSizeLabel);
        this.GroupBox1.add(fileSizeLabel);
        this.GroupBox1.setBounds(2, 308, 279, 64);
        
        this.Close = new JButton("Save");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.Close.setMnemonic(KeyEvent.VK_S);
        this.Close.setBounds(287, 2, 60, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(287, 25, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.ModalResult = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.Label4 = new JLabel("You are making a bitmap file to use to create a nozzle for the Painter Image Hose brush or a picture tube for Paint Shop Pro. You can use the nozzle or tube to \"spray\" your picture with plants. Click Help for instructions on using the bitmap file.");
        this.Label4.setBounds(6, 3, 261, 70);
        
        this.Panel1 = new JPanel(null);
        // -- this.Panel1.setLayout(new BoxLayout(this.Panel1, BoxLayout.Y_AXIS));
        this.Panel1.add(Label4);
        this.Panel1.setBounds(2, 2, 279, 77);
        
        this.Label1 = new JLabel("(Use a color not found in your plants.)");
        this.Label1.setBounds(55, 122, 183, 14);
        
        this.backgroundColorPanel = new JPanel(null);
        // -- this.backgroundColorPanel.setLayout(new BoxLayout(this.backgroundColorPanel, BoxLayout.Y_AXIS));
        this.backgroundColorPanel.setBounds(29, 119, 20, 20);
        this.backgroundColorPanel.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                backgroundColorPanelClick(event);
            }
        });
        
        this.Label3 = new JLabel("Background color", displayedMnemonic=KeyEvent.VK_C, labelFor=this.backgroundColorPanel);
        this.Label3.setBounds(10, 102, 85, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.resolutionEdit = new JSpinner(SpinnerNumberModel(10, 10, 10000, 10));
        this.resolutionEdit.setBounds(29, 75, 60, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.resolutionEdit.OnChange = resolutionEditChange;
        
        this.resolutionLabel = new JLabel("Resolution (pixels/inch)", displayedMnemonic=KeyEvent.VK_R, labelFor=this.resolutionEdit);
        this.resolutionLabel.setBounds(10, 60, 112, 14);
        
        this.colorType = new JComboBox(new DefaultComboBoxModel());
        this.colorType.setBounds(29, 36, 155, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.colorType.Style = csOwnerDrawFixed;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorType.OnChange = colorTypeChange;
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("From screen");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("2 colors (1-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("16 colors (4-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("256 colors (8-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("32768 colors (15-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("65536 colors (16-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("16 million colors (24-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("4.3 billion colors (32-bit)");
        //  --------------- UNHANDLED ATTRIBUTE: this.colorType.ItemHeight = 13;
        
        this.colorsLabel = new JLabel("Color depth", displayedMnemonic=KeyEvent.VK_D, labelFor=this.colorType);
        this.colorsLabel.setBounds(10, 19, 55, 14);
        
        this.GroupBox2 = new JPanel(null);
        // -- this.GroupBox2.setLayout(new BoxLayout(this.GroupBox2, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox2.border = new TitledBorder(""Nozzle/Tube options"");
        this.GroupBox2.add(Label1);
        this.GroupBox2.add(backgroundColorPanel);
        this.GroupBox2.add(Label3);
        this.GroupBox2.add(resolutionEdit);
        this.GroupBox2.add(resolutionLabel);
        this.GroupBox2.add(colorType);
        this.GroupBox2.add(colorsLabel);
        this.GroupBox2.setBounds(2, 162, 279, 147);
        
        this.useSelectedPlants = new JRadioButton("selected");
        this.useSelectedPlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelection(event);
            }
        });
        this.useSelectedPlants.setMnemonic(KeyEvent.VK_L);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        ButtonGroup group = new ButtonGroup();
        group.add(this.useSelectedPlants);
        this.useSelectedPlants.setBounds(17, 18, 66, 17);
        
        this.useVisiblePlants = new JRadioButton("visible");
        this.useVisiblePlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelection(event);
            }
        });
        this.useVisiblePlants.setMnemonic(KeyEvent.VK_V);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.useVisiblePlants);
        this.useVisiblePlants.setBounds(17, 35, 54, 17);
        
        this.useAllPlants = new JRadioButton("all");
        this.useAllPlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeSelection(event);
            }
        });
        this.useAllPlants.setMnemonic(KeyEvent.VK_A);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.useAllPlants);
        this.useAllPlants.setBounds(17, 52, 36, 17);
        
        this.GroupBox3 = new JPanel(null);
        // -- this.GroupBox3.setLayout(new BoxLayout(this.GroupBox3, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox3.border = new TitledBorder(""Draw which plants?"");
        this.GroupBox3.add(useSelectedPlants);
        this.GroupBox3.add(useVisiblePlants);
        this.GroupBox3.add(useAllPlants);
        this.GroupBox3.setBounds(2, 82, 279, 76);
        
        //  ------- UNHANDLED TYPE TColorDialog: ColorDialog 
        //  --------------- UNHANDLED ATTRIBUTE: this.ColorDialog.Top = 112;
        //  --------------- UNHANDLED ATTRIBUTE: this.ColorDialog.Left = 306;
        //  --------------- UNHANDLED ATTRIBUTE: this.ColorDialog.Ctl3D = True;
        
        delphiPanel.add(helpButton);
        delphiPanel.add(GroupBox1);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        delphiPanel.add(Panel1);
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
        
    public void backgroundColorPanelClick(MouseEvent event) {
        System.out.println("backgroundColorPanelClick");
    }
        
    public void changeSelection(ActionEvent event) {
        System.out.println("changeSelection");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                NozzleOptionsWindow thisClass = new NozzleOptionsWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
