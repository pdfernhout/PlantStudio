
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class OptionsWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    SpeedButton helpButton;
    JButton Close;
    JButton cancel;
    JTabbedPane optionsNotebook;
    JPanel page1;
    JPanel wholeProgramBox;
    JPanel backgroundColor;
    JLabel backgroundColorLabel;
    JCheckBox showPlantDrawingProgress;
    JPanel transparentColor;
    JLabel transparentColorLabel;
    JPanel mainWindowDrawingOptionsBox;
    JButton customDrawOptions;
    JSpinner memoryLimitForPlantBitmaps_MB;
    JLabel memoryLimitLabel;
    JPanel page2;
    JPanel GroupBox1;
    JPanel firstSelectionRectangleColor;
    JLabel firstSelectionRectangleColorLabel;
    JPanel multiSelectionRectangleColor;
    JLabel multiSelectionRectangleColorLabel;
    JPanel page3;
    JPanel GroupBox2;
    JLabel pasteRectSizeLabel;
    JLabel resizeRectSizeLabel;
    JSpinner rotationIncrement;
    JLabel rotationIncrementLabel;
    JSpinner nudgeDistance;
    JLabel nudgeDistanceLabel;
    JSpinner resizeKeyUpMultiplierPercent;
    JLabel resizeDistanceLabel;
    JSpinner pasteRectSize;
    JSpinner resizeRectSize;
    JPanel page4;
    JPanel GroupBox4;
    JPanel ghostingColor;
    JLabel Label9;
    JPanel nonHiddenPosedColor;
    JLabel Label10;
    JPanel selectedPosedColor;
    JLabel Label3;
    JPanel page5;
    JPanel GroupBox5;
    JSpinner undoLimit;
    JLabel undoLimitLabel;
    JSpinner undoLimitOfPlants;
    JLabel undoLimitOfPlantsLabel;
    JPanel page6;
    JPanel GroupBox6;
    JCheckBox useMetricUnits;
    JSpinner parametersFontSize;
    JLabel parametersFontSizeLabel;
    JPanel GroupBox7;
    JLabel Label1;
    JCheckBox openMostRecentFileAtStart;
    JSpinner pauseBeforeHint;
    JLabel pauseBeforeHintLabel;
    JSpinner pauseDuringHint;
    JLabel pauseDuringHintLabel;
    JCheckBox ignoreWindowSettingsInFile;
    JCheckBox drawWithOpenGL;
    JPanel Panel1;
    ImagePanel Image1;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public OptionsWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("PlantStudio Preferences");
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
        this.setBounds(279, 188, 450, 247  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [biSystemMenu];
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.ActiveControl = cancel;
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
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        
        
        Image helpButtonImage = toolkit.createImage("../resources/OptionsForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(386, 63, 61, 25);
        
        this.Close = new JButton("OK");
        this.Close.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                CloseClick(event);
            }
        });
        this.Close.setMnemonic(KeyEvent.VK_O);
        this.Close.setBounds(386, 4, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.Close.DragCursor = crHandPoint;
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(386, 27, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.optionsNotebook = new JTabbedPane();
        
        this.page1 = new JPanel(null);
        this.backgroundColor = new JPanel(null);
        // -- this.backgroundColor.setLayout(new BoxLayout(this.backgroundColor, BoxLayout.Y_AXIS));
        this.backgroundColor.setBounds(9, 17, 20, 20);
        this.backgroundColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                backgroundColorMouseUp(event);
            }
        });
        
        this.backgroundColorLabel = new JLabel("Background color behind plants", displayedMnemonic=KeyEvent.VK_B, labelFor=this.backgroundColor);
        this.backgroundColorLabel.setBounds(34, 20, 152, 14);
        
        this.showPlantDrawingProgress = new JCheckBox("Show drawing progress");
        this.showPlantDrawingProgress.setMnemonic(KeyEvent.VK_S);
        this.showPlantDrawingProgress.setBounds(9, 69, 161, 17);
        
        this.transparentColor = new JPanel(null);
        // -- this.transparentColor.setLayout(new BoxLayout(this.transparentColor, BoxLayout.Y_AXIS));
        this.transparentColor.setBounds(9, 43, 20, 20);
        this.transparentColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                transparentColorMouseUp(event);
            }
        });
        
        this.transparentColorLabel = new JLabel("Transparent color for overlaying plants if using plant bitmaps", displayedMnemonic=KeyEvent.VK_T, labelFor=this.transparentColor);
        this.transparentColorLabel.setBounds(34, 46, 292, 14);
        
        this.wholeProgramBox = new JPanel(null);
        // -- this.wholeProgramBox.setLayout(new BoxLayout(this.wholeProgramBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.wholeProgramBox.border = new TitledBorder("" Whole program "");
        this.wholeProgramBox.add(backgroundColor);
        this.wholeProgramBox.add(backgroundColorLabel);
        this.wholeProgramBox.add(showPlantDrawingProgress);
        this.wholeProgramBox.add(transparentColor);
        this.wholeProgramBox.add(transparentColorLabel);
        this.wholeProgramBox.setBounds(4, 94, 362, 95);
        
        this.customDrawOptions = new JButton("Change Custom Drawing Options...");
        this.customDrawOptions.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                customDrawOptionsClick(event);
            }
        });
        this.customDrawOptions.setMnemonic(KeyEvent.VK_W);
        this.customDrawOptions.setBounds(8, 54, 202, 21);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.memoryLimitForPlantBitmaps_MB = new JSpinner(SpinnerNumberModel(200, 1, 200, 1));
        this.memoryLimitForPlantBitmaps_MB.setBounds(8, 24, 47, 23);
        
        this.memoryLimitLabel = new JLabel("Upper limit on memory devoted to plant bitmaps (1-200 MB)", displayedMnemonic=KeyEvent.VK_U, labelFor=this.memoryLimitForPlantBitmaps_MB);
        this.memoryLimitLabel.setBounds(60, 29, 282, 14);
        
        this.mainWindowDrawingOptionsBox = new JPanel(null);
        // -- this.mainWindowDrawingOptionsBox.setLayout(new BoxLayout(this.mainWindowDrawingOptionsBox, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.mainWindowDrawingOptionsBox.border = new TitledBorder("" Main window "");
        this.mainWindowDrawingOptionsBox.add(customDrawOptions);
        this.mainWindowDrawingOptionsBox.add(memoryLimitForPlantBitmaps_MB);
        this.mainWindowDrawingOptionsBox.add(memoryLimitLabel);
        this.mainWindowDrawingOptionsBox.setBounds(4, 4, 362, 85);
        
        this.page1.add(wholeProgramBox);
        this.page1.add(mainWindowDrawingOptionsBox);
        this.optionsNotebook.addTab("Drawing", null, this.page1);
        
        
        this.page2 = new JPanel(null);
        this.firstSelectionRectangleColor = new JPanel(null);
        // -- this.firstSelectionRectangleColor.setLayout(new BoxLayout(this.firstSelectionRectangleColor, BoxLayout.Y_AXIS));
        this.firstSelectionRectangleColor.setBounds(8, 18, 20, 20);
        this.firstSelectionRectangleColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                firstSelectionRectangleColorMouseUp(event);
            }
        });
        
        this.firstSelectionRectangleColorLabel = new JLabel("Rectangle color for focused plant", displayedMnemonic=KeyEvent.VK_F, labelFor=this.firstSelectionRectangleColor);
        this.firstSelectionRectangleColorLabel.setBounds(32, 21, 161, 14);
        
        this.multiSelectionRectangleColor = new JPanel(null);
        // -- this.multiSelectionRectangleColor.setLayout(new BoxLayout(this.multiSelectionRectangleColor, BoxLayout.Y_AXIS));
        this.multiSelectionRectangleColor.setBounds(8, 40, 20, 20);
        this.multiSelectionRectangleColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                multiSelectionRectangleColorMouseUp(event);
            }
        });
        
        this.multiSelectionRectangleColorLabel = new JLabel("Rectangle color for other selected plants", displayedMnemonic=KeyEvent.VK_O, labelFor=this.multiSelectionRectangleColor);
        this.multiSelectionRectangleColorLabel.setBounds(32, 43, 196, 14);
        
        this.GroupBox1 = new JPanel(null);
        // -- this.GroupBox1.setLayout(new BoxLayout(this.GroupBox1, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox1.border = new TitledBorder("" Main window "");
        this.GroupBox1.add(firstSelectionRectangleColor);
        this.GroupBox1.add(firstSelectionRectangleColorLabel);
        this.GroupBox1.add(multiSelectionRectangleColor);
        this.GroupBox1.add(multiSelectionRectangleColorLabel);
        this.GroupBox1.setBounds(4, 4, 362, 69);
        
        this.page2.add(GroupBox1);
        this.optionsNotebook.addTab("Selecting", null, this.page2);
        
        
        this.page3 = new JPanel(null);
        this.pasteRectSizeLabel = new JLabel(" Width and height of plant pasted from text (50-500 pixels)", displayedMnemonic=KeyEvent.VK_P);
        this.pasteRectSizeLabel.setBounds(67, 114, 280, 14);
        
        this.resizeRectSizeLabel = new JLabel(" Width and height of resizing square (2-20 pixels)", displayedMnemonic=KeyEvent.VK_S);
        this.resizeRectSizeLabel.setBounds(67, 146, 238, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.rotationIncrement = new JSpinner(SpinnerNumberModel(1, 1, 100, 1));
        this.rotationIncrement.setBounds(8, 19, 53, 23);
        
        this.rotationIncrementLabel = new JLabel("Rotation change with arrow or mouse click (1-100 degrees)", displayedMnemonic=KeyEvent.VK_R, labelFor=this.rotationIncrement);
        this.rotationIncrementLabel.setBounds(67, 24, 289, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.nudgeDistance = new JSpinner(SpinnerNumberModel(1, 1, 100, 1));
        this.nudgeDistance.setBounds(8, 49, 53, 23);
        
        this.nudgeDistanceLabel = new JLabel("Distance plant moves with Control-arrow key (0-100 pixels)", displayedMnemonic=KeyEvent.VK_M, labelFor=this.nudgeDistance);
        this.nudgeDistanceLabel.setBounds(67, 54, 288, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.resizeKeyUpMultiplierPercent = new JSpinner(SpinnerNumberModel(100, 100, 200, 10));
        this.resizeKeyUpMultiplierPercent.setBounds(8, 80, 53, 23);
        
        this.resizeDistanceLabel = new JLabel("Size increase with Control-Shift-up-arrow key (100-200%)", displayedMnemonic=KeyEvent.VK_I, labelFor=this.resizeKeyUpMultiplierPercent);
        this.resizeDistanceLabel.setBounds(67, 84, 284, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.pasteRectSize = new JSpinner(SpinnerNumberModel(100, 50, 500, 10));
        this.pasteRectSize.setBounds(8, 110, 53, 23);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.resizeRectSize = new JSpinner(SpinnerNumberModel(2, 2, 20, 1));
        this.resizeRectSize.setBounds(8, 140, 53, 23);
        
        this.GroupBox2 = new JPanel(null);
        // -- this.GroupBox2.setLayout(new BoxLayout(this.GroupBox2, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox2.border = new TitledBorder("" Main window "");
        this.GroupBox2.add(pasteRectSizeLabel);
        this.GroupBox2.add(resizeRectSizeLabel);
        this.GroupBox2.add(rotationIncrement);
        this.GroupBox2.add(rotationIncrementLabel);
        this.GroupBox2.add(nudgeDistance);
        this.GroupBox2.add(nudgeDistanceLabel);
        this.GroupBox2.add(resizeKeyUpMultiplierPercent);
        this.GroupBox2.add(resizeDistanceLabel);
        this.GroupBox2.add(pasteRectSize);
        this.GroupBox2.add(resizeRectSize);
        this.GroupBox2.setBounds(4, 4, 362, 176);
        
        this.page3.add(GroupBox2);
        this.optionsNotebook.addTab("Editing", null, this.page3);
        
        
        this.page4 = new JPanel(null);
        this.ghostingColor = new JPanel(null);
        // -- this.ghostingColor.setLayout(new BoxLayout(this.ghostingColor, BoxLayout.Y_AXIS));
        this.ghostingColor.setBounds(8, 20, 20, 20);
        this.ghostingColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                ghostingColorMouseUp(event);
            }
        });
        
        this.Label9 = new JLabel("Ghosting color", displayedMnemonic=KeyEvent.VK_G, labelFor=this.ghostingColor);
        this.Label9.setBounds(32, 23, 70, 14);
        
        this.nonHiddenPosedColor = new JPanel(null);
        // -- this.nonHiddenPosedColor.setLayout(new BoxLayout(this.nonHiddenPosedColor, BoxLayout.Y_AXIS));
        this.nonHiddenPosedColor.setBounds(8, 43, 20, 20);
        this.nonHiddenPosedColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                nonHiddenPosedColorMouseUp(event);
            }
        });
        
        this.Label10 = new JLabel("Highlighting color for all posed plant parts", displayedMnemonic=KeyEvent.VK_H, labelFor=this.nonHiddenPosedColor);
        this.Label10.setBounds(32, 45, 198, 14);
        
        this.selectedPosedColor = new JPanel(null);
        // -- this.selectedPosedColor.setLayout(new BoxLayout(this.selectedPosedColor, BoxLayout.Y_AXIS));
        this.selectedPosedColor.setBounds(8, 66, 20, 20);
        this.selectedPosedColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                selectedPosedColorMouseUp(event);
            }
        });
        
        this.Label3 = new JLabel("Highlighting color for selected posed plant part", displayedMnemonic=KeyEvent.VK_S, labelFor=this.selectedPosedColor);
        this.Label3.setBounds(32, 69, 223, 14);
        
        this.GroupBox4 = new JPanel(null);
        // -- this.GroupBox4.setLayout(new BoxLayout(this.GroupBox4, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox4.border = new TitledBorder("" Main window "");
        this.GroupBox4.add(ghostingColor);
        this.GroupBox4.add(Label9);
        this.GroupBox4.add(nonHiddenPosedColor);
        this.GroupBox4.add(Label10);
        this.GroupBox4.add(selectedPosedColor);
        this.GroupBox4.add(Label3);
        this.GroupBox4.setBounds(4, 5, 362, 97);
        
        this.page4.add(GroupBox4);
        this.optionsNotebook.addTab("Posing", null, this.page4);
        
        
        this.page5 = new JPanel(null);
        // -- supposed to be a spin edit, not yet fuly implemented
        this.undoLimit = new JSpinner(SpinnerNumberModel(1, 1, 1000, 1));
        this.undoLimit.setBounds(8, 20, 53, 23);
        
        this.undoLimitLabel = new JLabel("Number of actions to keep in undo list (1-1000 actions)", displayedMnemonic=KeyEvent.VK_N, labelFor=this.undoLimit);
        this.undoLimitLabel.setBounds(66, 23, 263, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.undoLimitOfPlants = new JSpinner(SpinnerNumberModel(1, 1, 500, 1));
        this.undoLimitOfPlants.setBounds(8, 48, 53, 23);
        
        this.undoLimitOfPlantsLabel = new JLabel("Number of plants to keep in undo list (1-500 plants)", displayedMnemonic=KeyEvent.VK_P, labelFor=this.undoLimitOfPlants);
        this.undoLimitOfPlantsLabel.setBounds(66, 51, 245, 14);
        
        this.GroupBox5 = new JPanel(null);
        // -- this.GroupBox5.setLayout(new BoxLayout(this.GroupBox5, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox5.border = new TitledBorder("" Whole program "");
        this.GroupBox5.add(undoLimit);
        this.GroupBox5.add(undoLimitLabel);
        this.GroupBox5.add(undoLimitOfPlants);
        this.GroupBox5.add(undoLimitOfPlantsLabel);
        this.GroupBox5.setBounds(4, 4, 362, 81);
        
        this.page5.add(GroupBox5);
        this.optionsNotebook.addTab("Undoing", null, this.page5);
        
        
        this.page6 = new JPanel(null);
        this.useMetricUnits = new JCheckBox("Default to metric units instead of English in parameter panels");
        this.useMetricUnits.setMnemonic(KeyEvent.VK_D);
        this.useMetricUnits.setBounds(8, 20, 319, 17);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.parametersFontSize = new JSpinner(SpinnerNumberModel(8, 6, 20, 1));
        this.parametersFontSize.setBounds(8, 43, 53, 23);
        
        this.parametersFontSizeLabel = new JLabel("Font size for parameter panels (6-20)", displayedMnemonic=KeyEvent.VK_P, labelFor=this.parametersFontSize);
        this.parametersFontSizeLabel.setBounds(66, 48, 181, 14);
        
        this.GroupBox6 = new JPanel(null);
        // -- this.GroupBox6.setLayout(new BoxLayout(this.GroupBox6, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox6.border = new TitledBorder("" Main window "");
        this.GroupBox6.add(useMetricUnits);
        this.GroupBox6.add(parametersFontSize);
        this.GroupBox6.add(parametersFontSizeLabel);
        this.GroupBox6.setBounds(4, 4, 362, 75);
        
        this.Label1 = new JLabel("This applies only when long button or parameter hints are on.");
        this.Label1.setBounds(64, 110, 295, 14);
        
        this.openMostRecentFileAtStart = new JCheckBox("Open most recent file at start");
        this.openMostRecentFileAtStart.setMnemonic(KeyEvent.VK_F);
        this.openMostRecentFileAtStart.setBounds(8, 20, 237, 17);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.pauseBeforeHint = new JSpinner(SpinnerNumberModel(100, 0, 100, 1));
        this.pauseBeforeHint.setBounds(7, 61, 53, 23);
        
        this.pauseBeforeHintLabel = new JLabel("Show hint after mouse is still for (0-100 seconds)", displayedMnemonic=KeyEvent.VK_S, labelFor=this.pauseBeforeHint);
        this.pauseBeforeHintLabel.setBounds(64, 66, 240, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.pauseDuringHint = new JSpinner(SpinnerNumberModel(100, 0, 100, 5));
        this.pauseDuringHint.setBounds(7, 87, 53, 23);
        
        this.pauseDuringHintLabel = new JLabel("Remove hint after (0-100 seconds)", displayedMnemonic=KeyEvent.VK_R, labelFor=this.pauseDuringHint);
        this.pauseDuringHintLabel.setBounds(64, 92, 169, 14);
        
        this.ignoreWindowSettingsInFile = new JCheckBox("Ignore window settings (top/side, one/many) saved in file");
        this.ignoreWindowSettingsInFile.setMnemonic(KeyEvent.VK_I);
        this.ignoreWindowSettingsInFile.setBounds(8, 39, 313, 17);
        
        this.GroupBox7 = new JPanel(null);
        // -- this.GroupBox7.setLayout(new BoxLayout(this.GroupBox7, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox7.border = new TitledBorder("" Whole program "");
        this.GroupBox7.add(Label1);
        this.GroupBox7.add(openMostRecentFileAtStart);
        this.GroupBox7.add(pauseBeforeHint);
        this.GroupBox7.add(pauseBeforeHintLabel);
        this.GroupBox7.add(pauseDuringHint);
        this.GroupBox7.add(pauseDuringHintLabel);
        this.GroupBox7.add(ignoreWindowSettingsInFile);
        this.GroupBox7.setBounds(4, 84, 362, 133);
        
        this.page6.add(GroupBox6);
        this.page6.add(GroupBox7);
        this.optionsNotebook.addTab("Miscellaneous", null, this.page6);
        
        
        this.optionsNotebook.add(page1);
        this.optionsNotebook.add(page2);
        this.optionsNotebook.add(page3);
        this.optionsNotebook.add(page4);
        this.optionsNotebook.add(page5);
        this.optionsNotebook.add(page6);
        this.optionsNotebook.setBounds(0, 0, 379, 247);
        //  --------------- UNHANDLED ATTRIBUTE: this.optionsNotebook.PageIndex = 2;
        //  --------------- UNHANDLED ATTRIBUTE: this.optionsNotebook.TabsPerRow = 5;
        //  --------------- UNHANDLED ATTRIBUTE: this.optionsNotebook.TabFont.Color = clBtnText;
        //  --------------- UNHANDLED ATTRIBUTE: this.optionsNotebook.TabFont.Charset = DEFAULT_CHARSET;
        //  --------------- UNHANDLED ATTRIBUTE: this.optionsNotebook.TabFont.Style = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.optionsNotebook.TabFont.Name = 'Arial';
        //  --------------- UNHANDLED ATTRIBUTE: this.optionsNotebook.TabFont.Height = -11;
        
        this.drawWithOpenGL = new JCheckBox("Draw using OpenGL");
        this.drawWithOpenGL.setBounds(413, 266, 149, 17);
        this.drawWithOpenGL.setVisible(false);
        
        Image Image1Image = toolkit.createImage("../resources/OptionsForm_Image1.png");
        this.Image1 = new ImagePanel(new ImageIcon(Image1Image));
        this.Image1.setBounds(3, 2, 31, 47);
        this.Image1.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                Image1Click(event);
            }
        });
        
        this.Panel1 = new JPanel(null);
        // -- this.Panel1.setLayout(new BoxLayout(this.Panel1, BoxLayout.Y_AXIS));
        this.Panel1.add(Image1);
        this.Panel1.setBounds(397, 164, 38, 54);
        
        delphiPanel.add(helpButton);
        delphiPanel.add(Close);
        delphiPanel.add(cancel);
        delphiPanel.add(optionsNotebook);
        delphiPanel.add(drawWithOpenGL);
        delphiPanel.add(Panel1);
        return delphiPanel;
    }
    
        
    public void CloseClick(ActionEvent event) {
        System.out.println("CloseClick");
    }
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void Image1Click(MouseEvent event) {
        System.out.println("Image1Click");
    }
        
    public void backgroundColorMouseUp(MouseEvent event) {
        System.out.println("backgroundColorMouseUp");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void customDrawOptionsClick(ActionEvent event) {
        System.out.println("customDrawOptionsClick");
    }
        
    public void firstSelectionRectangleColorMouseUp(MouseEvent event) {
        System.out.println("firstSelectionRectangleColorMouseUp");
    }
        
    public void ghostingColorMouseUp(MouseEvent event) {
        System.out.println("ghostingColorMouseUp");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void multiSelectionRectangleColorMouseUp(MouseEvent event) {
        System.out.println("multiSelectionRectangleColorMouseUp");
    }
        
    public void nonHiddenPosedColorMouseUp(MouseEvent event) {
        System.out.println("nonHiddenPosedColorMouseUp");
    }
        
    public void selectedPosedColorMouseUp(MouseEvent event) {
        System.out.println("selectedPosedColorMouseUp");
    }
        
    public void transparentColorMouseUp(MouseEvent event) {
        System.out.println("transparentColorMouseUp");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                OptionsWindow thisClass = new OptionsWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
