
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class Generic3DOptionsWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JPanel otherGroupBox;
    JCheckBox translatePlantsToWindowPositions;
    JCheckBox writeColors;
    JPanel plantNameAndCylinderSidesPanel;
    JLabel Label3;
    JLabel sidesLabel;
    JSpinner lengthOfShortName;
    JSpinner stemCylinderFaces;
    JLabel Label2;
    JLabel stemCylinderFacesLabel;
    JCheckBox writePlantNumberInFrontOfName;
    JPanel pressPlantsPanel;
    JLabel Label8;
    JCheckBox pressPlants;
    JComboBox directionToPressPlants;
    JCheckBox makeTrianglesDoubleSided;
    JPanel dxfColorsGroupBox;
    JRadioButton colorDXFFromRGB;
    JRadioButton colorDXFFromOneColor;
    JPanel wholePlantColor;
    JRadioButton colorDXFFromPlantPartType;
    JList colorsByPlantPart;
    JButton setPlantPartColor;
    JCheckBox dxfWriteColors;
    JPanel povLimitsGroupBox;
    JTextField minLineLengthToWrite;
    JLabel Label4;
    JTextField minTdoScaleToWrite;
    JLabel Label5;
    JPanel nestingGroupBox;
    JCheckBox nestLeafAndPetiole;
    JCheckBox nestCompoundLeaf;
    JCheckBox nestInflorescence;
    JCheckBox nestPedicelAndFlowerFruit;
    JCheckBox nestFloralLayers;
    JCheckBox commentOutUnionAtEnd;
    // UNHANDLED_TYPE layeringOption;
    JButton Close;
    JButton cancel;
    JPanel threeDSWarningPanel;
    JLabel Label6;
    JPanel reorientGroupBox;
    JLabel Label10;
    JLabel Label1;
    JLabel Label9;
    JLabel Label7;
    JSpinner xRotationBeforeDraw;
    JSpinner overallScalingFactor_pct;
    JPanel drawWhichPlantsGroupBox;
    JRadioButton useSelectedPlants;
    JRadioButton useVisiblePlants;
    JRadioButton useAllPlants;
    // UNHANDLED_TYPE estimationStringGrid;
    // UNHANDLED_TYPE vrmlVersionRadioGroup;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public Generic3DOptionsWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("3D Export Options");
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
        this.setBounds(245, 119, 576, 529  + 80); // extra for title bar and menu
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
        
        
        Image helpButtonImage = toolkit.createImage("../resources/Generic3DOptionsForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(290, 64, 60, 21);
        
        this.translatePlantsToWindowPositions = new JCheckBox("Translate plants to match window positions");
        this.translatePlantsToWindowPositions.setMnemonic(KeyEvent.VK_T);
        this.translatePlantsToWindowPositions.setBounds(10, 151, 245, 17);
        
        this.writeColors = new JCheckBox("Write colors");
        this.writeColors.setMnemonic(KeyEvent.VK_C);
        this.writeColors.setBounds(10, 115, 101, 17);
        
        this.Label3 = new JLabel("characters (1-60)");
        this.Label3.setBounds(151, 7, 86, 14);
        
        this.sidesLabel = new JLabel("sides (3-20)");
        this.sidesLabel.setBounds(200, 35, 59, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.lengthOfShortName = new JSpinner(SpinnerNumberModel(3, 1, 60, 1));
        this.lengthOfShortName.setBounds(99, 3, 45, 23);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.stemCylinderFaces = new JSpinner(SpinnerNumberModel(3, 3, 20, 1));
        this.stemCylinderFaces.setBounds(153, 30, 45, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.stemCylinderFaces.OnChange = stemCylinderFacesChange;
        
        this.Label2 = new JLabel("Limit plant name to", displayedMnemonic=KeyEvent.VK_N, labelFor=this.stemCylinderFaces);
        this.Label2.setBounds(5, 7, 88, 14);
        
        this.stemCylinderFacesLabel = new JLabel("Draw stems as cylinders with", displayedMnemonic=KeyEvent.VK_Y, labelFor=this.stemCylinderFaces);
        this.stemCylinderFacesLabel.setBounds(5, 35, 145, 14);
        
        this.plantNameAndCylinderSidesPanel = new JPanel(null);
        // -- this.plantNameAndCylinderSidesPanel.setLayout(new BoxLayout(this.plantNameAndCylinderSidesPanel, BoxLayout.Y_AXIS));
        this.plantNameAndCylinderSidesPanel.add(Label3);
        this.plantNameAndCylinderSidesPanel.add(sidesLabel);
        this.plantNameAndCylinderSidesPanel.add(lengthOfShortName);
        this.plantNameAndCylinderSidesPanel.add(stemCylinderFaces);
        this.plantNameAndCylinderSidesPanel.add(Label2);
        this.plantNameAndCylinderSidesPanel.add(stemCylinderFacesLabel);
        this.plantNameAndCylinderSidesPanel.setBounds(6, 16, 261, 56);
        
        this.writePlantNumberInFrontOfName = new JCheckBox("Write plant number in front of name");
        this.writePlantNumberInFrontOfName.setMnemonic(KeyEvent.VK_U);
        this.writePlantNumberInFrontOfName.setBounds(10, 96, 219, 17);
        
        this.Label8 = new JLabel("dimension");
        this.Label8.setBounds(154, 11, 48, 14);
        
        this.pressPlants = new JCheckBox("\"Press\" plants in");
        this.pressPlants.setMnemonic(KeyEvent.VK_E);
        this.pressPlants.setBounds(8, 8, 99, 17);
        
        this.directionToPressPlants = new JComboBox(new DefaultComboBoxModel());
        this.directionToPressPlants.setBounds(108, 3, 41, 22);
        //  --------------- UNHANDLED ATTRIBUTE: this.directionToPressPlants.Style = csDropDownList;
        ((DefaultComboBoxModel)this.directionToPressPlants.getModel()).addElement("x");
        ((DefaultComboBoxModel)this.directionToPressPlants.getModel()).addElement("y");
        ((DefaultComboBoxModel)this.directionToPressPlants.getModel()).addElement("z");
        //  --------------- UNHANDLED ATTRIBUTE: this.directionToPressPlants.ItemHeight = 14;
        
        this.pressPlantsPanel = new JPanel(null);
        // -- this.pressPlantsPanel.setLayout(new BoxLayout(this.pressPlantsPanel, BoxLayout.Y_AXIS));
        this.pressPlantsPanel.add(Label8);
        this.pressPlantsPanel.add(pressPlants);
        this.pressPlantsPanel.add(directionToPressPlants);
        this.pressPlantsPanel.setBounds(2, 69, 273, 28);
        
        this.makeTrianglesDoubleSided = new JCheckBox("Double polygons on 3D objects");
        this.makeTrianglesDoubleSided.setMnemonic(KeyEvent.VK_D);
        this.makeTrianglesDoubleSided.setBounds(10, 133, 181, 17);
        
        this.otherGroupBox = new JPanel(null);
        // -- this.otherGroupBox.setLayout(new BoxLayout(this.otherGroupBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.otherGroupBox.border = new TitledBorder("" Other options "");
        this.otherGroupBox.add(translatePlantsToWindowPositions);
        this.otherGroupBox.add(writeColors);
        this.otherGroupBox.add(plantNameAndCylinderSidesPanel);
        this.otherGroupBox.add(writePlantNumberInFrontOfName);
        this.otherGroupBox.add(pressPlantsPanel);
        this.otherGroupBox.add(makeTrianglesDoubleSided);
        this.otherGroupBox.setBounds(4, 232, 280, 175);
        
        this.colorDXFFromRGB = new JRadioButton("use front-face RGB colors");
        this.colorDXFFromRGB.setMnemonic(KeyEvent.VK_R);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        ButtonGroup group = new ButtonGroup();
        group.add(this.colorDXFFromRGB);
        this.colorDXFFromRGB.setBounds(9, 35, 232, 17);
        
        this.colorDXFFromOneColor = new JRadioButton("use this one color         for all plant parts");
        this.colorDXFFromOneColor.setMnemonic(KeyEvent.VK_N);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.colorDXFFromOneColor);
        this.colorDXFFromOneColor.setBounds(9, 56, 244, 15);
        
        this.wholePlantColor = new JPanel(null);
        // -- this.wholePlantColor.setLayout(new BoxLayout(this.wholePlantColor, BoxLayout.Y_AXIS));
        this.wholePlantColor.setBounds(119, 56, 16, 14);
        this.wholePlantColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                wholePlantColorMouseUp(event);
            }
        });
        
        this.colorDXFFromPlantPartType = new JRadioButton("use colors based on type of part");
        this.colorDXFFromPlantPartType.setMnemonic(KeyEvent.VK_B);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.colorDXFFromPlantPartType);
        this.colorDXFFromPlantPartType.setBounds(9, 77, 182, 15);
        
        this.colorsByPlantPart = new JList(new DefaultListModel());
        this.colorsByPlantPart.setFixedCellHeight(16);
        this.colorsByPlantPart.setBounds(27, 95, 247, 52);
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsByPlantPart.Style = lbOwnerDrawFixed;
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Meristems");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Internodes");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Leaves");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("First leaves");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Flowers (F)");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Flowers (M)");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Inflor. (F)");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Inflor. (M)");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Fruit");
        ((DefaultComboBoxModel)this.colorsByPlantPart.getModel()).addElement("Root top");
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsByPlantPart.MultiSelect = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsByPlantPart.OnDrawItem = colorsByPlantPartDrawItem;
        //  --------------- UNHANDLED ATTRIBUTE: this.colorsByPlantPart.OnDblClick = colorsByPlantPartDblClick;
        
        this.setPlantPartColor = new JButton("Set...");
        this.setPlantPartColor.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                setPlantPartColorClick(event);
            }
        });
        this.setPlantPartColor.setMnemonic(KeyEvent.VK_S);
        this.setPlantPartColor.setBounds(221, 71, 53, 22);
        
        this.dxfWriteColors = new JCheckBox("Write colors");
        this.dxfWriteColors.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                dxfWriteColorsClick(event);
            }
        });
        this.dxfWriteColors.setMnemonic(KeyEvent.VK_C);
        this.dxfWriteColors.setBounds(10, 16, 101, 17);
        
        this.dxfColorsGroupBox = new JPanel(null);
        // -- this.dxfColorsGroupBox.setLayout(new BoxLayout(this.dxfColorsGroupBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.dxfColorsGroupBox.border = new TitledBorder("" Colors "");
        this.dxfColorsGroupBox.add(colorDXFFromRGB);
        this.dxfColorsGroupBox.add(colorDXFFromOneColor);
        this.dxfColorsGroupBox.add(wholePlantColor);
        this.dxfColorsGroupBox.add(colorDXFFromPlantPartType);
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(27, 95, 247, 52);;
        scroller1.setViewportView(colorsByPlantPart);
        this.dxfColorsGroupBox.add(scroller1);
        this.dxfColorsGroupBox.add(setPlantPartColor);
        this.dxfColorsGroupBox.add(dxfWriteColors);
        this.dxfColorsGroupBox.setBounds(290, 91, 280, 152);
        this.dxfColorsGroupBox.setVisible(false);
        
        this.minLineLengthToWrite = new JTextField("");
        this.minLineLengthToWrite.setBounds(17, 19, 51, 22);
        
        this.Label4 = new JLabel("Keep lines at least this long (mm)", displayedMnemonic=KeyEvent.VK_K, labelFor=this.minLineLengthToWrite);
        this.Label4.setBounds(72, 23, 158, 14);
        
        this.minTdoScaleToWrite = new JTextField("");
        this.minTdoScaleToWrite.setBounds(17, 45, 51, 22);
        
        this.Label5 = new JLabel("Keep 3D objects of at least this scale", displayedMnemonic=KeyEvent.VK_3, labelFor=this.minTdoScaleToWrite);
        this.Label5.setBounds(72, 49, 179, 14);
        
        this.povLimitsGroupBox = new JPanel(null);
        // -- this.povLimitsGroupBox.setLayout(new BoxLayout(this.povLimitsGroupBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.povLimitsGroupBox.border = new TitledBorder("" Limit small lines and 3D objects "");
        this.povLimitsGroupBox.add(minLineLengthToWrite);
        this.povLimitsGroupBox.add(Label4);
        this.povLimitsGroupBox.add(minTdoScaleToWrite);
        this.povLimitsGroupBox.add(Label5);
        this.povLimitsGroupBox.setBounds(290, 449, 280, 74);
        this.povLimitsGroupBox.setVisible(false);
        
        this.nestLeafAndPetiole = new JCheckBox("leaves with petioles");
        this.nestLeafAndPetiole.setMnemonic(KeyEvent.VK_P);
        this.nestLeafAndPetiole.setBounds(17, 18, 122, 17);
        
        this.nestCompoundLeaf = new JCheckBox("compound leaves");
        this.nestCompoundLeaf.setMnemonic(KeyEvent.VK_C);
        this.nestCompoundLeaf.setBounds(17, 37, 119, 17);
        
        this.nestInflorescence = new JCheckBox("inflorescences");
        this.nestInflorescence.setMnemonic(KeyEvent.VK_I);
        this.nestInflorescence.setBounds(17, 55, 97, 17);
        
        this.nestPedicelAndFlowerFruit = new JCheckBox("flowers with pedicels");
        this.nestPedicelAndFlowerFruit.setMnemonic(KeyEvent.VK_F);
        this.nestPedicelAndFlowerFruit.setBounds(142, 18, 130, 17);
        
        this.nestFloralLayers = new JCheckBox("pistils and stamens");
        this.nestFloralLayers.setMnemonic(KeyEvent.VK_M);
        this.nestFloralLayers.setBounds(142, 36, 118, 17);
        
        this.commentOutUnionAtEnd = new JCheckBox("Comment out union of plants at end");
        this.commentOutUnionAtEnd.setMnemonic(KeyEvent.VK_U);
        this.commentOutUnionAtEnd.setBounds(17, 77, 207, 18);
        
        this.nestingGroupBox = new JPanel(null);
        // -- this.nestingGroupBox.setLayout(new BoxLayout(this.nestingGroupBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.nestingGroupBox.border = new TitledBorder("" Nest "");
        this.nestingGroupBox.add(nestLeafAndPetiole);
        this.nestingGroupBox.add(nestCompoundLeaf);
        this.nestingGroupBox.add(nestInflorescence);
        this.nestingGroupBox.add(nestPedicelAndFlowerFruit);
        this.nestingGroupBox.add(nestFloralLayers);
        this.nestingGroupBox.add(commentOutUnionAtEnd);
        this.nestingGroupBox.setBounds(290, 246, 280, 100);
        this.nestingGroupBox.setVisible(false);
        
        //  ------- UNHANDLED TYPE TRadioGroup: layeringOption 
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.Caption = ' Group by ';
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.Ctl3D = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.ParentCtl3D = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.Top = 81;
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.Height = 75;
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.Width = 280;
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.TabOrder = 5;
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.Items.Strings = ['&whole plant', '&type of plant part', 'individual plant &part'];
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.ItemIndex = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.layeringOption.Left = 4;
        
        this.Close = new JButton("Save");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.Close.setMnemonic(KeyEvent.VK_S);
        this.Close.setBounds(290, 4, 60, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(290, 27, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.Label6 = new JLabel("Note: This version of the 3DS export function does not import equally well to all 3D programs. See the help system for tips on improving 3DS compatibility.");
        this.Label6.setBounds(7, 4, 265, 42);
        
        this.threeDSWarningPanel = new JPanel(null);
        // -- this.threeDSWarningPanel.setLayout(new BoxLayout(this.threeDSWarningPanel, BoxLayout.Y_AXIS));
        this.threeDSWarningPanel.add(Label6);
        this.threeDSWarningPanel.setBounds(290, 394, 280, 52);
        this.threeDSWarningPanel.setVisible(false);
        
        this.Label10 = new JLabel("degrees (-180 to 180)");
        this.Label10.setBounds(124, 19, 106, 14);
        
        this.Label1 = new JLabel("Rotate by");
        this.Label1.setBounds(10, 19, 46, 14);
        
        this.Label9 = new JLabel("percent (1-10,000)");
        this.Label9.setBounds(124, 45, 91, 14);
        
        this.Label7 = new JLabel("Scale by");
        this.Label7.setBounds(10, 45, 42, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.xRotationBeforeDraw = new JSpinner(SpinnerNumberModel(0, -180, 180, 5));
        this.xRotationBeforeDraw.setBounds(62, 15, 57, 23);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.overallScalingFactor_pct = new JSpinner(SpinnerNumberModel(10000, 1, 10000, 5));
        this.overallScalingFactor_pct.setBounds(62, 41, 57, 23);
        
        this.reorientGroupBox = new JPanel(null);
        // -- this.reorientGroupBox.setLayout(new BoxLayout(this.reorientGroupBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.reorientGroupBox.border = new TitledBorder("" Reorient "");
        this.reorientGroupBox.add(Label10);
        this.reorientGroupBox.add(Label1);
        this.reorientGroupBox.add(Label9);
        this.reorientGroupBox.add(Label7);
        this.reorientGroupBox.add(xRotationBeforeDraw);
        this.reorientGroupBox.add(overallScalingFactor_pct);
        this.reorientGroupBox.setBounds(4, 158, 281, 70);
        
        this.useSelectedPlants = new JRadioButton("selected plants");
        this.useSelectedPlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                useSelectedPlantsClick(event);
            }
        });
        this.useSelectedPlants.setMnemonic(KeyEvent.VK_L);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.useSelectedPlants);
        this.useSelectedPlants.setBounds(8, 16, 96, 17);
        
        this.useVisiblePlants = new JRadioButton("visible plants");
        this.useVisiblePlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                useVisiblePlantsClick(event);
            }
        });
        this.useVisiblePlants.setMnemonic(KeyEvent.VK_V);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.useVisiblePlants);
        this.useVisiblePlants.setBounds(107, 16, 82, 17);
        
        this.useAllPlants = new JRadioButton("all plants");
        this.useAllPlants.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                useAllPlantsClick(event);
            }
        });
        this.useAllPlants.setMnemonic(KeyEvent.VK_A);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.useAllPlants);
        this.useAllPlants.setBounds(206, 16, 65, 17);
        
        //  ------- UNHANDLED TYPE TStringGrid: estimationStringGrid 
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.ParentCtl3D = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Top = 35;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Font.Name = 'Arial';
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Width = 270;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.ColCount = 6;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.ColWidths = ['', '', '', '', '', ''];
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.DefaultRowHeight = 16;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.FixedRows = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Font.Height = -11;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.ParentFont = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.ScrollBars = ssNone;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Options = [goFixedVertLine, goFixedHorzLine, goDrawFocusSelected];
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Font.Color = clBlue;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Left = 5;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Font.Charset = DEFAULT_CHARSET;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Font.Style = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Ctl3D = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Color = clBtnFace;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.DefaultColWidth = 42;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.Height = 35;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.RowCount = 3;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.TabOrder = 3;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.FixedColor = clBtnHighlight;
        //  --------------- UNHANDLED ATTRIBUTE: this.estimationStringGrid.FixedCols = 0;
        
        this.drawWhichPlantsGroupBox = new JPanel(null);
        // -- this.drawWhichPlantsGroupBox.setLayout(new BoxLayout(this.drawWhichPlantsGroupBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.drawWhichPlantsGroupBox.border = new TitledBorder("" Include "");
        this.drawWhichPlantsGroupBox.add(useSelectedPlants);
        this.drawWhichPlantsGroupBox.add(useVisiblePlants);
        this.drawWhichPlantsGroupBox.add(useAllPlants);
        // FIX UNHANDLED TYPE -- this.drawWhichPlantsGroupBox.add(this.estimationStringGrid);
        this.drawWhichPlantsGroupBox.setBounds(4, 4, 280, 76);
        
        //  ------- UNHANDLED TYPE TRadioGroup: vrmlVersionRadioGroup 
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Caption = ' Version ';
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.ParentCtl3D = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Top = 351;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Ctl3D = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Height = 38;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Width = 280;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.TabOrder = 10;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Items.Strings = ['VRML &1.0', 'VRML &2.0 (VRML 97)'];
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.ItemIndex = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Visible = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Columns = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.vrmlVersionRadioGroup.Left = 290;
        
        delphiPanel.add(helpButton);
        delphiPanel.add(otherGroupBox);
        delphiPanel.add(dxfColorsGroupBox);
        delphiPanel.add(povLimitsGroupBox);
        delphiPanel.add(nestingGroupBox);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        delphiPanel.add(threeDSWarningPanel);
        delphiPanel.add(reorientGroupBox);
        delphiPanel.add(drawWhichPlantsGroupBox);
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
        
    public void dxfWriteColorsClick(ActionEvent event) {
        System.out.println("dxfWriteColorsClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void setPlantPartColorClick(ActionEvent event) {
        System.out.println("setPlantPartColorClick");
    }
        
    public void useAllPlantsClick(ActionEvent event) {
        System.out.println("useAllPlantsClick");
    }
        
    public void useSelectedPlantsClick(ActionEvent event) {
        System.out.println("useSelectedPlantsClick");
    }
        
    public void useVisiblePlantsClick(ActionEvent event) {
        System.out.println("useVisiblePlantsClick");
    }
        
    public void wholePlantColorMouseUp(MouseEvent event) {
        System.out.println("wholePlantColorMouseUp");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                Generic3DOptionsWindow thisClass = new Generic3DOptionsWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
