
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class BitmapOptionsWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JButton Close;
    JButton cancel;
    JPanel printBox;
    JLabel sizeLabel;
    JLabel printWidthLabel;
    JLabel printHeightLabel;
    JLabel marginsLabel;
    JLabel printLeftMarginLabel;
    JLabel printTopMarginLabel;
    JLabel printRightMarginLabel;
    JLabel printBottomMarginLabel;
    ImagePanel wholePageImage;
    JCheckBox printPreserveAspectRatio;
    JTextField printWidthEdit;
    SpinButton printWidthSpin;
    JTextField printHeightEdit;
    SpinButton printHeightSpin;
    JTextField printLeftMarginEdit;
    JTextField printTopMarginEdit;
    SpinButton printLeftMarginSpin;
    SpinButton printTopMarginSpin;
    JTextField printRightMarginEdit;
    JTextField printBottomMarginEdit;
    SpinButton printRightMarginSpin;
    SpinButton printBottomMarginSpin;
    JPanel printImagePanel;
    JPanel outputBox;
    JLabel sizePixelsLabel;
    JLabel sizeInchesLabel;
    JLabel inchWidthLabel;
    JLabel inchHeightLabel;
    JLabel pixelWidthLabel;
    JLabel pixelHeightLabel;
    JTextField inchWidthEdit;
    JTextField inchHeightEdit;
    JComboBox colorType;
    JLabel colorsLabel;
    JTextField resolutionEdit;
    JLabel resolutionLabel;
    JTextField pixelWidthEdit;
    JTextField pixelHeightEdit;
    SpinButton resolutionSpin;
    SpinButton pixelWidthSpin;
    SpinButton pixelHeightSpin;
    SpinButton inchHeightSpin;
    SpinButton inchWidthSpin;
    JCheckBox preserveAspectRatio;
    JTextField jpgCompressionEdit;
    SpinButton jpgCompressionSpin;
    JLabel jpgCompressionLabel;
    JButton printSetup;
    JPanel plantsBox;
    JRadioButton useSelectedPlants;
    JRadioButton useAllPlants;
    JRadioButton useDrawingAreaContents;
    JRadioButton useVisiblePlants;
    JButton borders;
    JPanel currentStuffPanel;
    JLabel selectedImageInfoLabel;
    JLabel screenInfoLabel;
    JLabel printerOrFileTypeInfoLabel;
    JLabel memoryUseInfoLabel;
    JButton suggestPrintSize;
    JButton printCenter;
    JButton printUseWholePage;
    // UNHANDLED_TYPE PrintDialog;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public BitmapOptionsWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Picture export options");
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
        this.setBounds(416, 120, 475, 378  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [biSystemMenu];
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
        
        
        Image helpButtonImage = toolkit.createImage("../resources/BitmapOptionsForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(413, 63, 60, 21);
        
        this.Close = new JButton("OK");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.Close.setBounds(413, 4, 60, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(413, 29, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.sizeLabel = new JLabel("Size (inches)");
        this.sizeLabel.setBounds(203, 13, 64, 14);
        
        this.printWidthLabel = new JLabel("width");
        this.printWidthLabel.setBounds(220, 35, 27, 14);
        
        this.printHeightLabel = new JLabel("height");
        this.printHeightLabel.setBounds(307, 33, 29, 14);
        
        this.marginsLabel = new JLabel("Margins (inches)");
        this.marginsLabel.setBounds(205, 61, 81, 14);
        
        this.printLeftMarginLabel = new JLabel("left");
        this.printLeftMarginLabel.setBounds(220, 79, 15, 14);
        
        this.printTopMarginLabel = new JLabel("top");
        this.printTopMarginLabel.setBounds(220, 105, 15, 14);
        
        this.printRightMarginLabel = new JLabel("right");
        this.printRightMarginLabel.setBounds(307, 79, 21, 14);
        
        this.printBottomMarginLabel = new JLabel("bottom");
        this.printBottomMarginLabel.setBounds(307, 105, 32, 14);
        
        this.wholePageImage = new ImagePanel(); // No image was set
        this.wholePageImage.setBounds(10, 20, 137, 79);
        
        this.printPreserveAspectRatio = new JCheckBox("Maintain aspect ratio");
        this.printPreserveAspectRatio.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                printPreserveAspectRatioClick(event);
            }
        });
        this.printPreserveAspectRatio.setBounds(252, 128, 129, 17);
        
        this.printWidthEdit = new JTextField("");
        this.printWidthEdit.setBounds(249, 29, 36, 22);
        this.printWidthEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.printWidthEdit.putClientProperty("tag", 1);
        
        this.printWidthSpin = new SpinButton("FIX_ME");
        Image printWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printWidthSpin.png");
        this.printWidthSpin.setUpIcon(new ImageIcon(printWidthSpinImage));
        this.printWidthSpin.setDownIcon(new ImageIcon(printWidthSpinImage));
        this.printWidthSpin.setBounds(287, 30, 16, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.printWidthSpin.FocusControl = printWidthEdit;
        this.printWidthSpin.putClientProperty("tag", 10);
        //  --------------- UNHANDLED ATTRIBUTE: this.printWidthSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.printWidthSpin.OnDownClick = spinDown;
        
        this.printHeightEdit = new JTextField("");
        this.printHeightEdit.setBounds(342, 29, 36, 22);
        this.printHeightEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.printHeightEdit.putClientProperty("tag", 1);
        
        this.printHeightSpin = new SpinButton("FIX_ME");
        Image printHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printHeightSpin.png");
        this.printHeightSpin.setUpIcon(new ImageIcon(printHeightSpinImage));
        this.printHeightSpin.setDownIcon(new ImageIcon(printHeightSpinImage));
        this.printHeightSpin.setBounds(380, 30, 16, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.printHeightSpin.FocusControl = printHeightEdit;
        this.printHeightSpin.putClientProperty("tag", 10);
        //  --------------- UNHANDLED ATTRIBUTE: this.printHeightSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.printHeightSpin.OnDownClick = spinDown;
        
        this.printLeftMarginEdit = new JTextField("");
        this.printLeftMarginEdit.setBounds(249, 77, 36, 22);
        this.printLeftMarginEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.printLeftMarginEdit.putClientProperty("tag", 1);
        
        this.printTopMarginEdit = new JTextField("");
        this.printTopMarginEdit.setBounds(249, 101, 36, 22);
        this.printTopMarginEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.printTopMarginEdit.putClientProperty("tag", 1);
        
        this.printLeftMarginSpin = new SpinButton("FIX_ME");
        Image printLeftMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printLeftMarginSpin.png");
        this.printLeftMarginSpin.setUpIcon(new ImageIcon(printLeftMarginSpinImage));
        this.printLeftMarginSpin.setDownIcon(new ImageIcon(printLeftMarginSpinImage));
        this.printLeftMarginSpin.setBounds(287, 78, 16, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.printLeftMarginSpin.FocusControl = printLeftMarginEdit;
        this.printLeftMarginSpin.putClientProperty("tag", 10);
        //  --------------- UNHANDLED ATTRIBUTE: this.printLeftMarginSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.printLeftMarginSpin.OnDownClick = spinDown;
        
        this.printTopMarginSpin = new SpinButton("FIX_ME");
        Image printTopMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printTopMarginSpin.png");
        this.printTopMarginSpin.setUpIcon(new ImageIcon(printTopMarginSpinImage));
        this.printTopMarginSpin.setDownIcon(new ImageIcon(printTopMarginSpinImage));
        this.printTopMarginSpin.setBounds(287, 102, 16, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.printTopMarginSpin.FocusControl = printTopMarginEdit;
        this.printTopMarginSpin.putClientProperty("tag", 10);
        //  --------------- UNHANDLED ATTRIBUTE: this.printTopMarginSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.printTopMarginSpin.OnDownClick = spinDown;
        
        this.printRightMarginEdit = new JTextField("");
        this.printRightMarginEdit.setBounds(342, 75, 36, 22);
        this.printRightMarginEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.printRightMarginEdit.putClientProperty("tag", 1);
        
        this.printBottomMarginEdit = new JTextField("");
        this.printBottomMarginEdit.setBounds(342, 101, 36, 22);
        this.printBottomMarginEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.printBottomMarginEdit.putClientProperty("tag", 1);
        
        this.printRightMarginSpin = new SpinButton("FIX_ME");
        Image printRightMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printRightMarginSpin.png");
        this.printRightMarginSpin.setUpIcon(new ImageIcon(printRightMarginSpinImage));
        this.printRightMarginSpin.setDownIcon(new ImageIcon(printRightMarginSpinImage));
        this.printRightMarginSpin.setBounds(380, 76, 16, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.printRightMarginSpin.FocusControl = printRightMarginEdit;
        this.printRightMarginSpin.putClientProperty("tag", 10);
        //  --------------- UNHANDLED ATTRIBUTE: this.printRightMarginSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.printRightMarginSpin.OnDownClick = spinDown;
        
        this.printBottomMarginSpin = new SpinButton("FIX_ME");
        Image printBottomMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printBottomMarginSpin.png");
        this.printBottomMarginSpin.setUpIcon(new ImageIcon(printBottomMarginSpinImage));
        this.printBottomMarginSpin.setDownIcon(new ImageIcon(printBottomMarginSpinImage));
        this.printBottomMarginSpin.setBounds(380, 102, 16, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.printBottomMarginSpin.FocusControl = printBottomMarginEdit;
        this.printBottomMarginSpin.putClientProperty("tag", 10);
        //  --------------- UNHANDLED ATTRIBUTE: this.printBottomMarginSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.printBottomMarginSpin.OnDownClick = spinDown;
        
        this.printImagePanel = new JPanel(null);
        // -- this.printImagePanel.setLayout(new BoxLayout(this.printImagePanel, BoxLayout.Y_AXIS));
        this.printImagePanel.setBounds(20, 28, 25, 24);
        
        this.printBox = new JPanel(null);
        // -- this.printBox.setLayout(new BoxLayout(this.printBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.printBox.border = new TitledBorder(""Printing options"");
        this.printBox.add(sizeLabel);
        this.printBox.add(printWidthLabel);
        this.printBox.add(printHeightLabel);
        this.printBox.add(marginsLabel);
        this.printBox.add(printLeftMarginLabel);
        this.printBox.add(printTopMarginLabel);
        this.printBox.add(printRightMarginLabel);
        this.printBox.add(printBottomMarginLabel);
        this.printBox.add(wholePageImage);
        this.printBox.add(printPreserveAspectRatio);
        this.printBox.add(printWidthEdit);
        this.printBox.add(printWidthSpin);
        this.printBox.add(printHeightEdit);
        this.printBox.add(printHeightSpin);
        this.printBox.add(printLeftMarginEdit);
        this.printBox.add(printTopMarginEdit);
        this.printBox.add(printLeftMarginSpin);
        this.printBox.add(printTopMarginSpin);
        this.printBox.add(printRightMarginEdit);
        this.printBox.add(printBottomMarginEdit);
        this.printBox.add(printRightMarginSpin);
        this.printBox.add(printBottomMarginSpin);
        this.printBox.add(printImagePanel);
        this.printBox.setBounds(0, 225, 409, 150);
        
        this.sizePixelsLabel = new JLabel("Size (pixels)");
        this.sizePixelsLabel.setBounds(203, 62, 60, 14);
        
        this.sizeInchesLabel = new JLabel("Size (inches)");
        this.sizeInchesLabel.setBounds(203, 18, 64, 14);
        
        this.inchWidthLabel = new JLabel("width");
        this.inchWidthLabel.setBounds(220, 38, 27, 14);
        
        this.inchHeightLabel = new JLabel("height");
        this.inchHeightLabel.setBounds(307, 38, 29, 14);
        
        this.pixelWidthLabel = new JLabel("width");
        this.pixelWidthLabel.setBounds(220, 82, 27, 14);
        
        this.pixelHeightLabel = new JLabel("height");
        this.pixelHeightLabel.setBounds(307, 82, 29, 14);
        
        this.inchWidthEdit = new JTextField("");
        this.inchWidthEdit.setBounds(249, 34, 36, 22);
        this.inchWidthEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.inchWidthEdit.putClientProperty("tag", 1);
        
        this.inchHeightEdit = new JTextField("");
        this.inchHeightEdit.setBounds(342, 34, 36, 22);
        this.inchHeightEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.inchHeightEdit.putClientProperty("tag", 1);
        
        this.colorType = new JComboBox(new DefaultComboBoxModel());
        this.colorType.setBounds(30, 36, 155, 19);
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
        //  --------------- UNHANDLED ATTRIBUTE: this.colorType.OnDrawItem = colorTypeDrawItem;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorType.ItemHeight = 13;
        
        this.colorsLabel = new JLabel("Color depth", displayedMnemonic=KeyEvent.VK_D, labelFor=this.colorType);
        this.colorsLabel.setBounds(10, 18, 55, 14);
        
        this.resolutionEdit = new JTextField("");
        this.resolutionEdit.setBounds(30, 80, 36, 22);
        this.resolutionEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        
        this.resolutionLabel = new JLabel("Resolution (pixels/inch)", displayedMnemonic=KeyEvent.VK_R, labelFor=this.resolutionEdit);
        this.resolutionLabel.setBounds(10, 64, 112, 14);
        
        this.pixelWidthEdit = new JTextField("");
        this.pixelWidthEdit.setBounds(249, 78, 36, 22);
        this.pixelWidthEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        
        this.pixelHeightEdit = new JTextField("");
        this.pixelHeightEdit.setBounds(342, 78, 36, 22);
        this.pixelHeightEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        
        this.resolutionSpin = new SpinButton("FIX_ME");
        Image resolutionSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_resolutionSpin.png");
        this.resolutionSpin.setUpIcon(new ImageIcon(resolutionSpinImage));
        this.resolutionSpin.setDownIcon(new ImageIcon(resolutionSpinImage));
        this.resolutionSpin.setBounds(68, 81, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.resolutionSpin.FocusControl = resolutionEdit;
        this.resolutionSpin.putClientProperty("tag", 1000);
        //  --------------- UNHANDLED ATTRIBUTE: this.resolutionSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.resolutionSpin.OnDownClick = spinDown;
        
        this.pixelWidthSpin = new SpinButton("FIX_ME");
        Image pixelWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_pixelWidthSpin.png");
        this.pixelWidthSpin.setUpIcon(new ImageIcon(pixelWidthSpinImage));
        this.pixelWidthSpin.setDownIcon(new ImageIcon(pixelWidthSpinImage));
        this.pixelWidthSpin.setBounds(287, 79, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.pixelWidthSpin.FocusControl = pixelWidthEdit;
        this.pixelWidthSpin.putClientProperty("tag", 1000);
        //  --------------- UNHANDLED ATTRIBUTE: this.pixelWidthSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.pixelWidthSpin.OnDownClick = spinDown;
        
        this.pixelHeightSpin = new SpinButton("FIX_ME");
        Image pixelHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_pixelHeightSpin.png");
        this.pixelHeightSpin.setUpIcon(new ImageIcon(pixelHeightSpinImage));
        this.pixelHeightSpin.setDownIcon(new ImageIcon(pixelHeightSpinImage));
        this.pixelHeightSpin.setBounds(380, 79, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.pixelHeightSpin.FocusControl = pixelHeightEdit;
        this.pixelHeightSpin.putClientProperty("tag", 1000);
        //  --------------- UNHANDLED ATTRIBUTE: this.pixelHeightSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.pixelHeightSpin.OnDownClick = spinDown;
        
        this.inchHeightSpin = new SpinButton("FIX_ME");
        Image inchHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_inchHeightSpin.png");
        this.inchHeightSpin.setUpIcon(new ImageIcon(inchHeightSpinImage));
        this.inchHeightSpin.setDownIcon(new ImageIcon(inchHeightSpinImage));
        this.inchHeightSpin.setBounds(380, 35, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.inchHeightSpin.FocusControl = inchHeightEdit;
        this.inchHeightSpin.putClientProperty("tag", 10);
        //  --------------- UNHANDLED ATTRIBUTE: this.inchHeightSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.inchHeightSpin.OnDownClick = spinDown;
        
        this.inchWidthSpin = new SpinButton("FIX_ME");
        Image inchWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_inchWidthSpin.png");
        this.inchWidthSpin.setUpIcon(new ImageIcon(inchWidthSpinImage));
        this.inchWidthSpin.setDownIcon(new ImageIcon(inchWidthSpinImage));
        this.inchWidthSpin.setBounds(287, 35, 15, 19);
        //  --------------- UNHANDLED ATTRIBUTE: this.inchWidthSpin.FocusControl = inchWidthEdit;
        this.inchWidthSpin.putClientProperty("tag", 10);
        //  --------------- UNHANDLED ATTRIBUTE: this.inchWidthSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.inchWidthSpin.OnDownClick = spinDown;
        
        this.preserveAspectRatio = new JCheckBox("Maintain aspect ratio");
        this.preserveAspectRatio.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                preserveAspectRatioClick(event);
            }
        });
        this.preserveAspectRatio.setBounds(249, 108, 127, 17);
        
        this.jpgCompressionEdit = new JTextField("");
        this.jpgCompressionEdit.setBounds(31, 123, 36, 22);
        this.jpgCompressionEdit.addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent event) {
                exitEditBox(event);
            }
        });
        this.jpgCompressionEdit.setVisible(false);
        
        this.jpgCompressionSpin = new SpinButton("FIX_ME");
        Image jpgCompressionSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_jpgCompressionSpin.png");
        this.jpgCompressionSpin.setUpIcon(new ImageIcon(jpgCompressionSpinImage));
        this.jpgCompressionSpin.setDownIcon(new ImageIcon(jpgCompressionSpinImage));
        this.jpgCompressionSpin.setBounds(69, 124, 15, 19);
        this.jpgCompressionSpin.setVisible(false);
        //  --------------- UNHANDLED ATTRIBUTE: this.jpgCompressionSpin.FocusControl = jpgCompressionEdit;
        this.jpgCompressionSpin.putClientProperty("tag", 100);
        //  --------------- UNHANDLED ATTRIBUTE: this.jpgCompressionSpin.OnUpClick = spinUp;
        //  --------------- UNHANDLED ATTRIBUTE: this.jpgCompressionSpin.OnDownClick = spinDown;
        
        this.jpgCompressionLabel = new JLabel("JPEG compression (1 least - 100 most)", displayedMnemonic=KeyEvent.VK_C, labelFor=this.resolutionEdit);
        this.jpgCompressionLabel.setBounds(10, 107, 187, 14);
        this.jpgCompressionLabel.setVisible(false);
        
        this.outputBox = new JPanel(null);
        // -- this.outputBox.setLayout(new BoxLayout(this.outputBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.outputBox.border = new TitledBorder(""Output options"");
        this.outputBox.add(sizePixelsLabel);
        this.outputBox.add(sizeInchesLabel);
        this.outputBox.add(inchWidthLabel);
        this.outputBox.add(inchHeightLabel);
        this.outputBox.add(pixelWidthLabel);
        this.outputBox.add(pixelHeightLabel);
        this.outputBox.add(inchWidthEdit);
        this.outputBox.add(inchHeightEdit);
        this.outputBox.add(colorType);
        this.outputBox.add(colorsLabel);
        this.outputBox.add(resolutionEdit);
        this.outputBox.add(resolutionLabel);
        this.outputBox.add(pixelWidthEdit);
        this.outputBox.add(pixelHeightEdit);
        this.outputBox.add(resolutionSpin);
        this.outputBox.add(pixelWidthSpin);
        this.outputBox.add(pixelHeightSpin);
        this.outputBox.add(inchHeightSpin);
        this.outputBox.add(inchWidthSpin);
        this.outputBox.add(preserveAspectRatio);
        this.outputBox.add(jpgCompressionEdit);
        this.outputBox.add(jpgCompressionSpin);
        this.outputBox.add(jpgCompressionLabel);
        this.outputBox.setBounds(0, 90, 409, 133);
        
        this.printSetup = new JButton("Printer...");
        this.printSetup.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                printSetupClick(event);
            }
        });
        this.printSetup.setMnemonic(KeyEvent.VK_P);
        this.printSetup.setBounds(413, 318, 60, 21);
        
        this.useSelectedPlants = new JRadioButton("selected");
        this.useSelectedPlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                selectionChoiceClick(event);
            }
        });
        this.useSelectedPlants.setMnemonic(KeyEvent.VK_L);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        ButtonGroup group = new ButtonGroup();
        group.add(this.useSelectedPlants);
        this.useSelectedPlants.setBounds(8, 15, 66, 17);
        
        this.useAllPlants = new JRadioButton("all");
        this.useAllPlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                selectionChoiceClick(event);
            }
        });
        this.useAllPlants.setMnemonic(KeyEvent.VK_A);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.useAllPlants);
        this.useAllPlants.setBounds(8, 49, 36, 17);
        
        this.useDrawingAreaContents = new JRadioButton("drawing area");
        this.useDrawingAreaContents.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                selectionChoiceClick(event);
            }
        });
        this.useDrawingAreaContents.setMnemonic(KeyEvent.VK_W);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.useDrawingAreaContents);
        this.useDrawingAreaContents.setBounds(8, 66, 93, 17);
        
        this.useVisiblePlants = new JRadioButton("visible");
        this.useVisiblePlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                selectionChoiceClick(event);
            }
        });
        this.useVisiblePlants.setMnemonic(KeyEvent.VK_V);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.useVisiblePlants);
        this.useVisiblePlants.setBounds(8, 32, 54, 17);
        
        this.plantsBox = new JPanel(null);
        // -- this.plantsBox.setLayout(new BoxLayout(this.plantsBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.plantsBox.border = new TitledBorder(""Draw which plants?"");
        this.plantsBox.add(useSelectedPlants);
        this.plantsBox.add(useAllPlants);
        this.plantsBox.add(useDrawingAreaContents);
        this.plantsBox.add(useVisiblePlants);
        this.plantsBox.setBounds(0, 2, 109, 89);
        
        this.borders = new JButton("Border...");
        this.borders.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                bordersClick(event);
            }
        });
        this.borders.setMnemonic(KeyEvent.VK_B);
        this.borders.setBounds(413, 342, 60, 21);
        
        this.selectedImageInfoLabel = new JLabel("Selection: 465 x 252 pixels, 12.4 x 3.1 inches");
        this.selectedImageInfoLabel.setBounds(7, 8, 218, 14);
        
        this.screenInfoLabel = new JLabel("Screen: 96 pixels/inch, 2534243 colors (24-bit)");
        this.screenInfoLabel.setBounds(7, 26, 226, 14);
        
        this.printerOrFileTypeInfoLabel = new JLabel("Printer:  300 x 300 pixels per inch, Portrait");
        this.printerOrFileTypeInfoLabel.setBounds(7, 45, 201, 14);
        
        this.memoryUseInfoLabel = new JLabel("Memory use: 365 K");
        this.memoryUseInfoLabel.setBounds(7, 63, 93, 14);
        
        this.currentStuffPanel = new JPanel(null);
        // -- this.currentStuffPanel.setLayout(new BoxLayout(this.currentStuffPanel, BoxLayout.Y_AXIS));
        this.currentStuffPanel.add(selectedImageInfoLabel);
        this.currentStuffPanel.add(screenInfoLabel);
        this.currentStuffPanel.add(printerOrFileTypeInfoLabel);
        this.currentStuffPanel.add(memoryUseInfoLabel);
        this.currentStuffPanel.setBounds(111, 7, 298, 84);
        
        this.suggestPrintSize = new JButton("Suggest");
        this.suggestPrintSize.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                suggestPrintSizeClick(event);
            }
        });
        this.suggestPrintSize.setMnemonic(KeyEvent.VK_U);
        this.suggestPrintSize.setBounds(413, 246, 60, 21);
        
        this.printCenter = new JButton("Center");
        this.printCenter.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                printCenterClick(event);
            }
        });
        this.printCenter.setMnemonic(KeyEvent.VK_E);
        this.printCenter.setBounds(413, 270, 60, 21);
        
        this.printUseWholePage = new JButton("Fill page");
        this.printUseWholePage.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                printUseWholePageClick(event);
            }
        });
        this.printUseWholePage.setMnemonic(KeyEvent.VK_F);
        this.printUseWholePage.setBounds(413, 294, 60, 21);
        
        //  ------- UNHANDLED TYPE TPrintDialog: PrintDialog 
        //  --------------- UNHANDLED ATTRIBUTE: this.PrintDialog.Top = 136;
        //  --------------- UNHANDLED ATTRIBUTE: this.PrintDialog.Left = 431;
        
        delphiPanel.add(helpButton);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        delphiPanel.add(printBox);
        delphiPanel.add(outputBox);
        delphiPanel.add(printSetup);
        delphiPanel.add(plantsBox);
        delphiPanel.add(borders);
        delphiPanel.add(currentStuffPanel);
        delphiPanel.add(suggestPrintSize);
        delphiPanel.add(printCenter);
        delphiPanel.add(printUseWholePage);
        return delphiPanel;
    }
    
        
    public void CloseClick(ActionEvent event) {
        System.out.println("CloseClick");
    }
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void bordersClick(ActionEvent event) {
        System.out.println("bordersClick");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void exitEditBox(FocusEvent event) {
        System.out.println("exitEditBox");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void preserveAspectRatioClick(ActionEvent event) {
        System.out.println("preserveAspectRatioClick");
    }
        
    public void printCenterClick(ActionEvent event) {
        System.out.println("printCenterClick");
    }
        
    public void printPreserveAspectRatioClick(ActionEvent event) {
        System.out.println("printPreserveAspectRatioClick");
    }
        
    public void printSetupClick(ActionEvent event) {
        System.out.println("printSetupClick");
    }
        
    public void printUseWholePageClick(ActionEvent event) {
        System.out.println("printUseWholePageClick");
    }
        
    public void selectionChoiceClick(ActionEvent event) {
        System.out.println("selectionChoiceClick");
    }
        
    public void suggestPrintSizeClick(ActionEvent event) {
        System.out.println("suggestPrintSizeClick");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                BitmapOptionsWindow thisClass = new BitmapOptionsWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
