
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class AnimationFilesOptionsWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JButton Close;
    JButton cancel;
    JPanel Panel1;
    JLabel fileNumberLabel;
    JLabel animationSizeLabel;
    JLabel fileSizeLabel;
    JPanel Panel2;
    JLabel Label4;
    JLabel focusedPlantName;
    JLabel Label5;
    JPanel GroupBox1;
    JLabel Label1;
    JLabel resolutionLabel;
    JLabel incrementLabel;
    JLabel plantMaxAgeLabel;
    JRadioButton animateByAge;
    JRadioButton animateByXRotation;
    JSpinner incrementEdit;
    JSpinner resolution;
    JComboBox colorType;
    JLabel colorsLabel;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public AnimationFilesOptionsWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Save Animation Files");
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
        this.setBounds(500, 298, 328, 364  + 80); // extra for title bar and menu
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
        
        
        Image helpButtonImage = toolkit.createImage("../resources/AnimationFilesOptionsForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(265, 62, 60, 21);
        
        this.Close = new JButton("Save");
        this.Close.setMnemonic(KeyEvent.VK_S);
        this.Close.setBounds(265, 2, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.Close.ModalResult = 1;
        
        this.cancel = new JButton("Cancel");
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(265, 25, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.ModalResult = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.fileNumberLabel = new JLabel("Number of files:  5");
        this.fileNumberLabel.setBounds(8, 26, 88, 14);
        
        this.animationSizeLabel = new JLabel("Animation size:  243 x 232");
        this.animationSizeLabel.setBounds(8, 8, 127, 14);
        
        this.fileSizeLabel = new JLabel("Estimated total file size:  25343 K");
        this.fileSizeLabel.setBounds(8, 44, 158, 14);
        
        this.Panel1 = new JPanel(null);
        // -- this.Panel1.setLayout(new BoxLayout(this.Panel1, BoxLayout.Y_AXIS));
        this.Panel1.add(fileNumberLabel);
        this.Panel1.add(animationSizeLabel);
        this.Panel1.add(fileSizeLabel);
        this.Panel1.setBounds(2, 296, 259, 66);
        
        this.Label4 = new JLabel("You are creating numbered animation files from the focused plant");
        this.Label4.setBounds(6, 5, 231, 28);
        
        this.focusedPlantName = new JLabel("sunflower");
        this.focusedPlantName.setBounds(24, 34, 50, 14);
        
        this.Label5 = new JLabel("for use in an animation programs. Click Help for instructions on using the numbered files.");
        this.Label5.setBounds(7, 49, 213, 28);
        
        this.Panel2 = new JPanel(null);
        // -- this.Panel2.setLayout(new BoxLayout(this.Panel2, BoxLayout.Y_AXIS));
        this.Panel2.add(Label4);
        this.Panel2.add(focusedPlantName);
        this.Panel2.add(Label5);
        this.Panel2.setBounds(2, 2, 259, 82);
        
        this.Label1 = new JLabel("Animate by changing");
        this.Label1.setBounds(8, 20, 101, 14);
        
        this.resolutionLabel = new JLabel("Resolution (pixels/inch)", displayedMnemonic=KeyEvent.VK_R);
        this.resolutionLabel.setBounds(8, 160, 112, 14);
        
        this.incrementLabel = new JLabel("Rotation increment between frames (degrees)", displayedMnemonic=KeyEvent.VK_F);
        this.incrementLabel.setBounds(8, 76, 223, 14);
        
        this.plantMaxAgeLabel = new JLabel("Maximum age = 100");
        this.plantMaxAgeLabel.setBounds(85, 97, 95, 14);
        
        this.animateByAge = new JRadioButton("plant age");
        this.animateByAge.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                animateByAgeClick(event);
            }
        });
        this.animateByAge.setMnemonic(KeyEvent.VK_A);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        ButtonGroup group = new ButtonGroup();
        group.add(this.animateByAge);
        this.animateByAge.setBounds(20, 35, 113, 17);
        
        this.animateByXRotation = new JRadioButton("X rotation");
        this.animateByXRotation.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                animateByXRotationClick(event);
            }
        });
        this.animateByXRotation.setMnemonic(KeyEvent.VK_X);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.animateByXRotation);
        this.animateByXRotation.setBounds(20, 53, 113, 17);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.incrementEdit = new JSpinner(SpinnerNumberModel(0, -360, 360, 1));
        this.incrementEdit.setBounds(20, 94, 61, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.incrementEdit.OnChange = incrementEditChange;
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.resolution = new JSpinner(SpinnerNumberModel(10, 10, 10000, 10));
        this.resolution.setBounds(20, 177, 61, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.resolution.OnChange = resolutionChange;
        
        this.colorType = new JComboBox(new DefaultComboBoxModel());
        this.colorType.setBounds(20, 137, 155, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.colorType.Style = csOwnerDrawFixed;
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("From screen");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("2 colors (1-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("16 colors (4-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("256 colors (8-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("32768 colors (15-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("65536 colors (16-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("16 million colors (24-bit)");
        ((DefaultComboBoxModel)this.colorType.getModel()).addElement("4.3 billion colors (32-bit)");
        //  --------------- UNHANDLED ATTRIBUTE: this.colorType.OnChange = colorTypeChange;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorType.ItemHeight = 13;
        
        this.colorsLabel = new JLabel("Color depth", displayedMnemonic=KeyEvent.VK_D, labelFor=this.colorType);
        this.colorsLabel.setBounds(8, 120, 55, 14);
        
        this.GroupBox1 = new JPanel(null);
        // -- this.GroupBox1.setLayout(new BoxLayout(this.GroupBox1, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox1.border = new TitledBorder(""Animation options"");
        this.GroupBox1.add(Label1);
        this.GroupBox1.add(resolutionLabel);
        this.GroupBox1.add(incrementLabel);
        this.GroupBox1.add(plantMaxAgeLabel);
        this.GroupBox1.add(animateByAge);
        this.GroupBox1.add(animateByXRotation);
        this.GroupBox1.add(incrementEdit);
        this.GroupBox1.add(resolution);
        this.GroupBox1.add(colorType);
        this.GroupBox1.add(colorsLabel);
        this.GroupBox1.setBounds(2, 86, 259, 207);
        
        delphiPanel.add(helpButton);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        delphiPanel.add(Panel1);
        delphiPanel.add(Panel2);
        delphiPanel.add(GroupBox1);
        return delphiPanel;
    }
    
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void animateByAgeClick(ActionEvent event) {
        System.out.println("animateByAgeClick");
    }
        
    public void animateByXRotationClick(ActionEvent event) {
        System.out.println("animateByXRotationClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                AnimationFilesOptionsWindow thisClass = new AnimationFilesOptionsWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
