
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class WizardWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    // UNHANDLED_TYPE bottomBevel;
    SpeedButton helpButton;
    SpeedButton changeTdoLibrary;
    JTabbedPane wizardNotebook;
    JPanel page1;
    JLabel panelStartLabel;
    JLabel introLabelThird;
    JLabel introLabelFirst;
    JLabel introLabelSecond;
    JLabel longHintsSuggestionLabel;
    ImagePanel startPicture;
    JPanel page2;
    JLabel panelMeristemsLabel;
    JLabel branchingLabel;
    JLabel leavesAlternateOppositeLabel;
    JLabel branchAngleLabel;
    JLabel secondaryBranchingLabel;
    SpeedButton leavesAlternate;
    SpeedButton leavesOpposite;
    SpeedButton branchNone;
    SpeedButton branchLittle;
    SpeedButton branchMedium;
    SpeedButton branchLot;
    SpeedButton secondaryBranchingYes;
    SpeedButton secondaryBranchingNo;
    SpeedButton branchAngleSmall;
    SpeedButton branchAngleMedium;
    SpeedButton branchAngleLarge;
    ImagePanel arrowLeavesAlternateOpposite;
    ImagePanel arrowBranching;
    ImagePanel arrowSecondaryBranching;
    ImagePanel arrowBranchAngle;
    JLabel Label1;
    JLabel Label11;
    JPanel page3;
    JLabel panelInternodesLabel;
    JLabel curvinessLabel;
    JLabel internodeLengthLabel;
    SpeedButton internodesVeryShort;
    SpeedButton internodesShort;
    SpeedButton internodesMedium;
    SpeedButton internodesLong;
    SpeedButton internodesVeryLong;
    SpeedButton curvinessNone;
    SpeedButton curvinessLittle;
    SpeedButton curvinessSome;
    SpeedButton curvinessVery;
    ImagePanel arrowCurviness;
    ImagePanel arrowInternodeLength;
    ImagePanel arrowInternodeWidth;
    JLabel internodeWidthLabel;
    SpeedButton internodeWidthVeryThin;
    SpeedButton internodeWidthThin;
    SpeedButton internodeWidthMedium;
    SpeedButton internodeWidthThick;
    SpeedButton internodeWidthVeryThick;
    JLabel Label2;
    JPanel page4;
    JLabel panelLeavesLabel;
    JLabel leafTdosLabel;
    JLabel leafScaleLabel;
    JLabel leafAngleLabel;
    JLabel petioleLengthLabel;
    ImagePanel arrowLeafScale;
    SpeedButton leafScaleTiny;
    SpeedButton leafScaleSmall;
    SpeedButton leafScaleMedium;
    SpeedButton leafScaleLarge;
    SpeedButton leafScaleHuge;
    ImagePanel arrowLeafAngle;
    SpeedButton leafAngleSmall;
    SpeedButton leafAngleMedium;
    SpeedButton leafAngleLarge;
    ImagePanel arrowPetioleLength;
    SpeedButton petioleVeryShort;
    SpeedButton petioleShort;
    SpeedButton petioleMedium;
    SpeedButton petioleLong;
    SpeedButton petioleVeryLong;
    ImagePanel arrowLeafTdos;
    JLabel Label4;
    JLabel leafTdoSelectedLabel;
    JTable leafTdosDraw;
    JPanel page5;
    JLabel panelCompoundLeavesLabel;
    ImagePanel arrowLeaflets;
    JLabel leafletsLabel;
    JLabel leafletsShapeLabel;
    ImagePanel arrowLeafletsShape;
    SpeedButton leafletsOne;
    SpeedButton leafletsThree;
    SpeedButton leafletsFour;
    SpeedButton leafletsFive;
    SpeedButton leafletsSeven;
    SpeedButton leafletsPinnate;
    SpeedButton leafletsPalmate;
    ImagePanel arrowLeafletsSpacing;
    JLabel leafletSpacingLabel;
    SpeedButton leafletSpacingClose;
    SpeedButton leafletSpacingMedium;
    SpeedButton leafletSpacingFar;
    JLabel Label5;
    JPanel page6;
    JLabel panelInflorPlacementLabel;
    JLabel apicalInflorsNumberLabel;
    JLabel axillaryInflorsNumberLabel;
    JLabel apicalStalkLabel;
    JLabel axillaryStalkLabel;
    ImagePanel apicalInflorExtraImage;
    ImagePanel axillaryInflorExtraImage;
    SpeedButton apicalInflorsNone;
    SpeedButton apicalInflorsOne;
    SpeedButton apicalInflorsTwo;
    SpeedButton apicalInflorsThree;
    SpeedButton apicalInflorsFive;
    ImagePanel arrowApicalInflorsNumber;
    SpeedButton axillaryInflorsNone;
    SpeedButton axillaryInflorsThree;
    SpeedButton axillaryInflorsFive;
    SpeedButton axillaryInflorsTen;
    SpeedButton axillaryInflorsTwenty;
    ImagePanel arrowAxillaryInflorsNumber;
    SpeedButton apicalStalkVeryShort;
    SpeedButton apicalStalkShort;
    SpeedButton apicalStalkMedium;
    SpeedButton apicalStalkLong;
    SpeedButton apicalStalkVeryLong;
    ImagePanel arrowApicalStalk;
    ImagePanel arrowAxillaryStalk;
    SpeedButton axillaryStalkVeryShort;
    SpeedButton axillaryStalkShort;
    SpeedButton axillaryStalkMedium;
    SpeedButton axillaryStalkLong;
    SpeedButton axillaryStalkVeryLong;
    JLabel Label3;
    JLabel Label6;
    JLabel Label7;
    JPanel page7;
    JLabel panelInflorDrawingLabel;
    JLabel inflorFlowersLabel;
    JLabel inflorShapeLabel;
    ImagePanel arrowInflorFlowers;
    ImagePanel arrowInflorShape;
    SpeedButton inflorFlowersOne;
    SpeedButton inflorFlowersTwo;
    SpeedButton inflorFlowersThree;
    SpeedButton inflorFlowersFive;
    SpeedButton inflorFlowersTen;
    SpeedButton inflorFlowersTwenty;
    SpeedButton inflorShapeSpike;
    SpeedButton inflorShapeRaceme;
    SpeedButton inflorShapePanicle;
    SpeedButton inflorShapeUmbel;
    SpeedButton inflorShapeCluster;
    SpeedButton inflorShapeHead;
    ImagePanel arrowInflorThickness;
    JLabel inflorThicknessLabel;
    SpeedButton inflorWidthVeryThin;
    SpeedButton inflorWidthThin;
    SpeedButton inflorWidthMedium;
    SpeedButton inflorWidthThick;
    SpeedButton inflorWidthVeryThick;
    JLabel Label8;
    JPanel page8;
    JLabel panelFlowersLabel;
    JLabel petalTdosLabel;
    JLabel petalScaleLabel;
    JLabel petalsNumberLabel;
    SpeedButton petalsOne;
    SpeedButton petalsThree;
    SpeedButton petalsFour;
    SpeedButton petalsFive;
    SpeedButton petalsTen;
    SpeedButton petalScaleTiny;
    SpeedButton petalScaleSmall;
    SpeedButton petalScaleMedium;
    SpeedButton petalScaleLarge;
    SpeedButton petalScaleHuge;
    ImagePanel arrowPetalTdos;
    ImagePanel arrowPetalsNumber;
    ImagePanel arrowPetalScale;
    ImagePanel arrowPetalColor;
    JLabel petalColorLabel;
    JLabel flowerColorExplainLabel;
    JLabel Label9;
    JLabel petalTdoSelectedLabel;
    JTable petalTdosDraw;
    JPanel petalColor;
    JPanel page9;
    JLabel fruitTdoLabel;
    JLabel fruitSectionsNumberLabel;
    JLabel fruitScaleLabel;
    JLabel panelFruitsLabel;
    ImagePanel arrowFruitTdo;
    ImagePanel arrowFruitSectionsNumber;
    ImagePanel arrowFruitScale;
    SpeedButton fruitSectionsOne;
    SpeedButton fruitSectionsThree;
    SpeedButton fruitSectionsFour;
    SpeedButton fruitSectionsFive;
    SpeedButton fruitSectionsTen;
    SpeedButton fruitScaleTiny;
    SpeedButton fruitScaleSmall;
    SpeedButton fruitScaleMedium;
    SpeedButton fruitScaleLarge;
    SpeedButton fruitScaleHuge;
    JLabel fruitColorLabel;
    ImagePanel arrowFruitColor;
    JLabel fruitColorExplainLabel;
    ImagePanel arrowShowFruits;
    JLabel showFruitsLabel;
    JLabel Label10;
    JLabel sectionTdoSelectedLabel;
    JTable sectionTdosDraw;
    JPanel fruitColor;
    JRadioButton showFruitsYes;
    JRadioButton showFruitsNo;
    JPanel page10;
    JLabel finishLabelFirst;
    JLabel finishLabelSecond;
    JLabel finishLabelThird;
    JLabel panelFinishLabel;
    JLabel previewLabel;
    SpeedButton turnLeft;
    SpeedButton turnRight;
    JLabel Label12;
    JTextField newPlantName;
    JPanel previewPanel;
    JButton randomizePlant;
    JButton cancel;
    JButton back;
    JButton next;
    JButton defaultChoices;
    JPanel hiddenPicturesPanel;
    ImagePanel startPageImage;
    ImagePanel meristemsPageImage;
    ImagePanel internodesPageImage;
    ImagePanel leavesPageImage;
    ImagePanel compoundLeavesPageImage;
    ImagePanel flowersPageImage;
    ImagePanel inflorDrawPageImage;
    ImagePanel inflorPlacePageImage;
    ImagePanel fruitsPageImage;
    ImagePanel finishPageImage;
    ImagePanel inflorDrawPageImageDisabled;
    ImagePanel flowersPageImageDisabled;
    ImagePanel fruitsPageImageDisabled;
    JTable progressDrawGrid;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public WizardWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Plant Wizard");
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
        this.setBounds(294, 114, 569, 299  + 80); // extra for title bar and menu
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
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnClose = FormClose;
        
        
        //  ------- UNHANDLED TYPE TBevel: bottomBevel 
        //  --------------- UNHANDLED ATTRIBUTE: this.bottomBevel.Top = 269;
        //  --------------- UNHANDLED ATTRIBUTE: this.bottomBevel.Height = 5;
        //  --------------- UNHANDLED ATTRIBUTE: this.bottomBevel.Width = 609;
        //  --------------- UNHANDLED ATTRIBUTE: this.bottomBevel.Shape = bsTopLine;
        //  --------------- UNHANDLED ATTRIBUTE: this.bottomBevel.Left = -16;
        
        Image helpButtonImage = toolkit.createImage("../resources/WizardForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(2, 276, 55, 21);
        
        this.changeTdoLibrary = new SpeedButton("3D Objects...");
        this.changeTdoLibrary.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeTdoLibraryClick(event);
            }
        });
        this.changeTdoLibrary.setMnemonic(KeyEvent.VK_3);
        this.changeTdoLibrary.setBounds(113, 276, 74, 21);
        
        this.wizardNotebook = new JTabbedPane();
        this.wizardNotebook.addChangeListener(new javax.swing.event.ChangeListener() {
            public void stateChanged(javax.swing.event.ChangeEvent event) {
                wizardNotebookPageChanged(event);
            }
        });
        
        this.page1 = new JPanel(null);
        this.panelStartLabel = new JLabel(" Welcome to the Plant Wizard!");
        this.panelStartLabel.setBounds(176, 16, 162, 14);
        
        this.introLabelThird = new JLabel("Click the Next button to start, or click Cancel to stop. Once you start, you can click the Back button to go back and change your choices, or you can click Cancel at any time.");
        this.introLabelThird.setBounds(178, 159, 328, 42);
        
        this.introLabelFirst = new JLabel("This wizard will help you create a new plant by asking you some simple questions. ");
        this.introLabelFirst.setBounds(178, 41, 289, 27);
        
        this.introLabelSecond = new JLabel("These 10 panels contain about 25 questions based on the most important of the 400 or so parameters that define a plant.");
        this.introLabelSecond.setBounds(178, 82, 308, 31);
        
        this.longHintsSuggestionLabel = new JLabel("Note: If you are using the wizard for the first time, we recommend turning on the ''Long Button Hints''. Each wizard question has a hint.");
        this.longHintsSuggestionLabel.setBounds(176, 215, 322, 28);
        
        Image startPictureImage = toolkit.createImage("../resources/WizardForm_startPicture.png");
        this.startPicture = new ImagePanel(new ImageIcon(startPictureImage));
        this.startPicture.setBounds(15, 37, 150, 178);
        
        this.page1.add(panelStartLabel);
        this.page1.add(introLabelThird);
        this.page1.add(introLabelFirst);
        this.page1.add(introLabelSecond);
        this.page1.add(longHintsSuggestionLabel);
        this.page1.add(startPicture);
        this.wizardNotebook.addTab("Start", null, this.page1);
        
        
        this.page2 = new JPanel(null);
        this.panelMeristemsLabel = new JLabel("Meristems");
        this.panelMeristemsLabel.setBounds(4, 4, 61, 14);
        
        this.branchingLabel = new JLabel("How much should the plant branch?");
        this.branchingLabel.setBounds(24, 154, 174, 14);
        
        this.leavesAlternateOppositeLabel = new JLabel("How should leaves and branches be arranged?");
        this.leavesAlternateOppositeLabel.setBounds(24, 62, 231, 14);
        
        this.branchAngleLabel = new JLabel(" What angle should branches make with the stem?");
        this.branchAngleLabel.setBounds(286, 154, 243, 14);
        
        this.secondaryBranchingLabel = new JLabel("Should secondary branching (off branches) occur?");
        this.secondaryBranchingLabel.setBounds(288, 62, 250, 14);
        
        Image leavesAlternateImage = toolkit.createImage("../resources/WizardForm_leavesAlternate.png");
        this.leavesAlternate = new SpeedButton("alternate", new ImageIcon(leavesAlternateImage));
        this.leavesAlternate.setSelected(true);
        this.leavesAlternate.setBounds(24, 77, 65, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leavesAlternate.Layout = blGlyphTop;
        this.leavesAlternate.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.leavesAlternate.GroupIndex = 1;
        
        Image leavesOppositeImage = toolkit.createImage("../resources/WizardForm_leavesOpposite.png");
        this.leavesOpposite = new SpeedButton("opposite", new ImageIcon(leavesOppositeImage));
        this.leavesOpposite.setBounds(89, 77, 63, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leavesOpposite.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.leavesOpposite.GroupIndex = 1;
        
        Image branchNoneImage = toolkit.createImage("../resources/WizardForm_branchNone.png");
        this.branchNone = new SpeedButton("none", new ImageIcon(branchNoneImage));
        this.branchNone.setSelected(true);
        this.branchNone.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                branchNoneClick(event);
            }
        });
        this.branchNone.setBounds(24, 170, 43, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchNone.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.branchNone.GroupIndex = 2;
        
        Image branchLittleImage = toolkit.createImage("../resources/WizardForm_branchLittle.png");
        this.branchLittle = new SpeedButton("a little", new ImageIcon(branchLittleImage));
        this.branchLittle.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                branchLittleClick(event);
            }
        });
        this.branchLittle.setBounds(66, 170, 49, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchLittle.Layout = blGlyphTop;
        this.branchLittle.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchLittle.GroupIndex = 2;
        
        Image branchMediumImage = toolkit.createImage("../resources/WizardForm_branchMedium.png");
        this.branchMedium = new SpeedButton("medium", new ImageIcon(branchMediumImage));
        this.branchMedium.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                branchMediumClick(event);
            }
        });
        this.branchMedium.setBounds(114, 170, 60, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchMedium.Layout = blGlyphTop;
        this.branchMedium.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchMedium.GroupIndex = 2;
        
        Image branchLotImage = toolkit.createImage("../resources/WizardForm_branchLot.png");
        this.branchLot = new SpeedButton("a lot", new ImageIcon(branchLotImage));
        this.branchLot.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                branchLotClick(event);
            }
        });
        this.branchLot.setBounds(173, 170, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchLot.Layout = blGlyphTop;
        this.branchLot.putClientProperty("tag", 3);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchLot.GroupIndex = 2;
        
        Image secondaryBranchingYesImage = toolkit.createImage("../resources/WizardForm_secondaryBranchingYes.png");
        this.secondaryBranchingYes = new SpeedButton("yes", new ImageIcon(secondaryBranchingYesImage));
        this.secondaryBranchingYes.setBounds(288, 77, 49, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.secondaryBranchingYes.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.secondaryBranchingYes.GroupIndex = 3;
        
        Image secondaryBranchingNoImage = toolkit.createImage("../resources/WizardForm_secondaryBranchingNo.png");
        this.secondaryBranchingNo = new SpeedButton("no", new ImageIcon(secondaryBranchingNoImage));
        this.secondaryBranchingNo.setSelected(true);
        this.secondaryBranchingNo.setBounds(337, 77, 44, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.secondaryBranchingNo.Layout = blGlyphTop;
        this.secondaryBranchingNo.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.secondaryBranchingNo.GroupIndex = 3;
        
        Image branchAngleSmallImage = toolkit.createImage("../resources/WizardForm_branchAngleSmall.png");
        this.branchAngleSmall = new SpeedButton("small", new ImageIcon(branchAngleSmallImage));
        this.branchAngleSmall.setSelected(true);
        this.branchAngleSmall.setBounds(288, 170, 47, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchAngleSmall.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.branchAngleSmall.GroupIndex = 4;
        
        Image branchAngleMediumImage = toolkit.createImage("../resources/WizardForm_branchAngleMedium.png");
        this.branchAngleMedium = new SpeedButton("medium", new ImageIcon(branchAngleMediumImage));
        this.branchAngleMedium.setBounds(334, 170, 59, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchAngleMedium.Layout = blGlyphTop;
        this.branchAngleMedium.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchAngleMedium.GroupIndex = 4;
        
        Image branchAngleLargeImage = toolkit.createImage("../resources/WizardForm_branchAngleLarge.png");
        this.branchAngleLarge = new SpeedButton("large", new ImageIcon(branchAngleLargeImage));
        this.branchAngleLarge.setBounds(390, 170, 43, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchAngleLarge.Layout = blGlyphTop;
        this.branchAngleLarge.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.branchAngleLarge.GroupIndex = 4;
        
        Image arrowLeavesAlternateOppositeImage = toolkit.createImage("../resources/WizardForm_arrowLeavesAlternateOpposite.png");
        this.arrowLeavesAlternateOpposite = new ImagePanel(new ImageIcon(arrowLeavesAlternateOppositeImage));
        this.arrowLeavesAlternateOpposite.setBounds(12, 62, 8, 16);
        
        Image arrowBranchingImage = toolkit.createImage("../resources/WizardForm_arrowBranching.png");
        this.arrowBranching = new ImagePanel(new ImageIcon(arrowBranchingImage));
        this.arrowBranching.setBounds(12, 154, 8, 16);
        
        Image arrowSecondaryBranchingImage = toolkit.createImage("../resources/WizardForm_arrowSecondaryBranching.png");
        this.arrowSecondaryBranching = new ImagePanel(new ImageIcon(arrowSecondaryBranchingImage));
        this.arrowSecondaryBranching.setBounds(274, 60, 8, 16);
        
        Image arrowBranchAngleImage = toolkit.createImage("../resources/WizardForm_arrowBranchAngle.png");
        this.arrowBranchAngle = new ImagePanel(new ImageIcon(arrowBranchAngleImage));
        this.arrowBranchAngle.setBounds(274, 152, 8, 16);
        
        this.Label1 = new JLabel("Meristems are buds from which leaves and branches grow. Where they develop and what they produce has a big effect on plant shape. Meristems form at the growing ends of plant stems (apexes) and in the angles between leaf and stem (axils).");
        this.Label1.setBounds(12, 18, 509, 42);
        
        this.Label11 = new JLabel("For each question, click on one of the big buttons under the question to make your choice.");
        this.Label11.setBounds(75, 248, 433, 14);
        
        this.page2.add(panelMeristemsLabel);
        this.page2.add(branchingLabel);
        this.page2.add(leavesAlternateOppositeLabel);
        this.page2.add(branchAngleLabel);
        this.page2.add(secondaryBranchingLabel);
        this.page2.add(leavesAlternate);
        this.page2.add(leavesOpposite);
        this.page2.add(branchNone);
        this.page2.add(branchLittle);
        this.page2.add(branchMedium);
        this.page2.add(branchLot);
        this.page2.add(secondaryBranchingYes);
        this.page2.add(secondaryBranchingNo);
        this.page2.add(branchAngleSmall);
        this.page2.add(branchAngleMedium);
        this.page2.add(branchAngleLarge);
        this.page2.add(arrowLeavesAlternateOpposite);
        this.page2.add(arrowBranching);
        this.page2.add(arrowSecondaryBranching);
        this.page2.add(arrowBranchAngle);
        this.page2.add(Label1);
        this.page2.add(Label11);
        this.wizardNotebook.addTab("Meristems", null, this.page2);
        
        
        this.page3 = new JPanel(null);
        this.panelInternodesLabel = new JLabel("Internodes");
        this.panelInternodesLabel.setBounds(4, 4, 61, 14);
        
        this.curvinessLabel = new JLabel("How curvy should the plant stem be?");
        this.curvinessLabel.setBounds(24, 58, 180, 14);
        
        this.internodeLengthLabel = new JLabel("How long should internodes be?");
        this.internodeLengthLabel.setBounds(24, 150, 156, 14);
        
        Image internodesVeryShortImage = toolkit.createImage("../resources/WizardForm_internodesVeryShort.png");
        this.internodesVeryShort = new SpeedButton("very short", new ImageIcon(internodesVeryShortImage));
        this.internodesVeryShort.setBounds(24, 167, 60, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesVeryShort.Layout = blGlyphTop;
        this.internodesVeryShort.setToolTipText("very short");
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesVeryShort.GroupIndex = 6;
        
        Image internodesShortImage = toolkit.createImage("../resources/WizardForm_internodesShort.png");
        this.internodesShort = new SpeedButton("short", new ImageIcon(internodesShortImage));
        this.internodesShort.setBounds(83, 167, 41, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesShort.Layout = blGlyphTop;
        this.internodesShort.setToolTipText("short");
        this.internodesShort.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesShort.GroupIndex = 6;
        
        Image internodesMediumImage = toolkit.createImage("../resources/WizardForm_internodesMedium.png");
        this.internodesMedium = new SpeedButton("medium", new ImageIcon(internodesMediumImage));
        this.internodesMedium.setSelected(true);
        this.internodesMedium.setBounds(123, 167, 51, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesMedium.Layout = blGlyphTop;
        this.internodesMedium.setToolTipText("medium");
        this.internodesMedium.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesMedium.GroupIndex = 6;
        
        Image internodesLongImage = toolkit.createImage("../resources/WizardForm_internodesLong.png");
        this.internodesLong = new SpeedButton("long", new ImageIcon(internodesLongImage));
        this.internodesLong.setBounds(173, 167, 36, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesLong.Layout = blGlyphTop;
        this.internodesLong.setToolTipText("long");
        this.internodesLong.putClientProperty("tag", 3);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesLong.GroupIndex = 6;
        
        Image internodesVeryLongImage = toolkit.createImage("../resources/WizardForm_internodesVeryLong.png");
        this.internodesVeryLong = new SpeedButton("very long", new ImageIcon(internodesVeryLongImage));
        this.internodesVeryLong.setBounds(208, 167, 61, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesVeryLong.Layout = blGlyphTop;
        this.internodesVeryLong.setToolTipText("very long");
        this.internodesVeryLong.putClientProperty("tag", 4);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodesVeryLong.GroupIndex = 6;
        
        Image curvinessNoneImage = toolkit.createImage("../resources/WizardForm_curvinessNone.png");
        this.curvinessNone = new SpeedButton("none", new ImageIcon(curvinessNoneImage));
        this.curvinessNone.setBounds(24, 78, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.curvinessNone.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.curvinessNone.GroupIndex = 5;
        
        Image curvinessLittleImage = toolkit.createImage("../resources/WizardForm_curvinessLittle.png");
        this.curvinessLittle = new SpeedButton("a little", new ImageIcon(curvinessLittleImage));
        this.curvinessLittle.setSelected(true);
        this.curvinessLittle.setBounds(68, 78, 54, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.curvinessLittle.Layout = blGlyphTop;
        this.curvinessLittle.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.curvinessLittle.GroupIndex = 5;
        
        Image curvinessSomeImage = toolkit.createImage("../resources/WizardForm_curvinessSome.png");
        this.curvinessSome = new SpeedButton("some", new ImageIcon(curvinessSomeImage));
        this.curvinessSome.setBounds(121, 78, 42, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.curvinessSome.Layout = blGlyphTop;
        this.curvinessSome.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.curvinessSome.GroupIndex = 5;
        
        Image curvinessVeryImage = toolkit.createImage("../resources/WizardForm_curvinessVery.png");
        this.curvinessVery = new SpeedButton("a lot", new ImageIcon(curvinessVeryImage));
        this.curvinessVery.setBounds(162, 78, 47, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.curvinessVery.Layout = blGlyphTop;
        this.curvinessVery.putClientProperty("tag", 3);
        //  --------------- UNHANDLED ATTRIBUTE: this.curvinessVery.GroupIndex = 5;
        
        Image arrowCurvinessImage = toolkit.createImage("../resources/WizardForm_arrowCurviness.png");
        this.arrowCurviness = new ImagePanel(new ImageIcon(arrowCurvinessImage));
        this.arrowCurviness.setBounds(12, 56, 8, 16);
        
        Image arrowInternodeLengthImage = toolkit.createImage("../resources/WizardForm_arrowInternodeLength.png");
        this.arrowInternodeLength = new ImagePanel(new ImageIcon(arrowInternodeLengthImage));
        this.arrowInternodeLength.setBounds(12, 151, 8, 16);
        
        Image arrowInternodeWidthImage = toolkit.createImage("../resources/WizardForm_arrowInternodeWidth.png");
        this.arrowInternodeWidth = new ImagePanel(new ImageIcon(arrowInternodeWidthImage));
        this.arrowInternodeWidth.setBounds(288, 56, 8, 16);
        
        this.internodeWidthLabel = new JLabel("How thick should internodes be?");
        this.internodeWidthLabel.setBounds(302, 58, 158, 14);
        
        Image internodeWidthVeryThinImage = toolkit.createImage("../resources/WizardForm_internodeWidthVeryThin.png");
        this.internodeWidthVeryThin = new SpeedButton("very thin", new ImageIcon(internodeWidthVeryThinImage));
        this.internodeWidthVeryThin.setBounds(302, 78, 57, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthVeryThin.Layout = blGlyphTop;
        this.internodeWidthVeryThin.setToolTipText("very short");
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthVeryThin.GroupIndex = 23;
        
        Image internodeWidthThinImage = toolkit.createImage("../resources/WizardForm_internodeWidthThin.png");
        this.internodeWidthThin = new SpeedButton("thin", new ImageIcon(internodeWidthThinImage));
        this.internodeWidthThin.setSelected(true);
        this.internodeWidthThin.setBounds(358, 78, 38, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthThin.Layout = blGlyphTop;
        this.internodeWidthThin.setToolTipText("short");
        this.internodeWidthThin.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthThin.GroupIndex = 23;
        
        Image internodeWidthMediumImage = toolkit.createImage("../resources/WizardForm_internodeWidthMedium.png");
        this.internodeWidthMedium = new SpeedButton("medium", new ImageIcon(internodeWidthMediumImage));
        this.internodeWidthMedium.setBounds(395, 78, 48, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthMedium.Layout = blGlyphTop;
        this.internodeWidthMedium.setToolTipText("medium");
        this.internodeWidthMedium.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthMedium.GroupIndex = 23;
        
        Image internodeWidthThickImage = toolkit.createImage("../resources/WizardForm_internodeWidthThick.png");
        this.internodeWidthThick = new SpeedButton("thick", new ImageIcon(internodeWidthThickImage));
        this.internodeWidthThick.setBounds(442, 78, 37, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthThick.Layout = blGlyphTop;
        this.internodeWidthThick.setToolTipText("long");
        this.internodeWidthThick.putClientProperty("tag", 3);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthThick.GroupIndex = 23;
        
        Image internodeWidthVeryThickImage = toolkit.createImage("../resources/WizardForm_internodeWidthVeryThick.png");
        this.internodeWidthVeryThick = new SpeedButton("very thick", new ImageIcon(internodeWidthVeryThickImage));
        this.internodeWidthVeryThick.setBounds(478, 78, 58, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthVeryThick.Layout = blGlyphTop;
        this.internodeWidthVeryThick.setToolTipText("very long");
        this.internodeWidthVeryThick.putClientProperty("tag", 4);
        //  --------------- UNHANDLED ATTRIBUTE: this.internodeWidthVeryThick.GroupIndex = 23;
        
        this.Label2 = new JLabel("Internodes are portions of plant stem between leaves. They determine how tall or short, straight or viney, and stiff or flexible a plant will be.");
        this.Label2.setBounds(12, 22, 395, 28);
        
        this.page3.add(panelInternodesLabel);
        this.page3.add(curvinessLabel);
        this.page3.add(internodeLengthLabel);
        this.page3.add(internodesVeryShort);
        this.page3.add(internodesShort);
        this.page3.add(internodesMedium);
        this.page3.add(internodesLong);
        this.page3.add(internodesVeryLong);
        this.page3.add(curvinessNone);
        this.page3.add(curvinessLittle);
        this.page3.add(curvinessSome);
        this.page3.add(curvinessVery);
        this.page3.add(arrowCurviness);
        this.page3.add(arrowInternodeLength);
        this.page3.add(arrowInternodeWidth);
        this.page3.add(internodeWidthLabel);
        this.page3.add(internodeWidthVeryThin);
        this.page3.add(internodeWidthThin);
        this.page3.add(internodeWidthMedium);
        this.page3.add(internodeWidthThick);
        this.page3.add(internodeWidthVeryThick);
        this.page3.add(Label2);
        this.wizardNotebook.addTab("Internodes", null, this.page3);
        
        
        this.page4 = new JPanel(null);
        this.panelLeavesLabel = new JLabel("Leaves");
        this.panelLeavesLabel.setBounds(4, 4, 40, 14);
        
        this.leafTdosLabel = new JLabel(" What 3D object should be used to draw leaves?");
        this.leafTdosLabel.setBounds(22, 60, 235, 14);
        
        this.leafScaleLabel = new JLabel("How big should a full-sized leaf be drawn?");
        this.leafScaleLabel.setBounds(24, 169, 208, 14);
        
        this.leafAngleLabel = new JLabel(" What angle should each leaf make with the stem?");
        this.leafAngleLabel.setBounds(300, 169, 242, 14);
        
        this.petioleLengthLabel = new JLabel("How long should the petiole (leaf stalk) be?");
        this.petioleLengthLabel.setBounds(302, 60, 208, 14);
        
        Image arrowLeafScaleImage = toolkit.createImage("../resources/WizardForm_arrowLeafScale.png");
        this.arrowLeafScale = new ImagePanel(new ImageIcon(arrowLeafScaleImage));
        this.arrowLeafScale.setBounds(12, 167, 8, 16);
        
        Image leafScaleTinyImage = toolkit.createImage("../resources/WizardForm_leafScaleTiny.png");
        this.leafScaleTiny = new SpeedButton("tiny", new ImageIcon(leafScaleTinyImage));
        this.leafScaleTiny.setBounds(24, 185, 37, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleTiny.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleTiny.GroupIndex = 7;
        
        Image leafScaleSmallImage = toolkit.createImage("../resources/WizardForm_leafScaleSmall.png");
        this.leafScaleSmall = new SpeedButton("small", new ImageIcon(leafScaleSmallImage));
        this.leafScaleSmall.setBounds(60, 185, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleSmall.Layout = blGlyphTop;
        this.leafScaleSmall.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleSmall.GroupIndex = 7;
        
        Image leafScaleMediumImage = toolkit.createImage("../resources/WizardForm_leafScaleMedium.png");
        this.leafScaleMedium = new SpeedButton("medium", new ImageIcon(leafScaleMediumImage));
        this.leafScaleMedium.setSelected(true);
        this.leafScaleMedium.setBounds(104, 185, 59, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleMedium.Layout = blGlyphTop;
        this.leafScaleMedium.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleMedium.GroupIndex = 7;
        
        Image leafScaleLargeImage = toolkit.createImage("../resources/WizardForm_leafScaleLarge.png");
        this.leafScaleLarge = new SpeedButton("large", new ImageIcon(leafScaleLargeImage));
        this.leafScaleLarge.setBounds(162, 185, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleLarge.Layout = blGlyphTop;
        this.leafScaleLarge.putClientProperty("tag", 3);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleLarge.GroupIndex = 7;
        
        Image leafScaleHugeImage = toolkit.createImage("../resources/WizardForm_leafScaleHuge.png");
        this.leafScaleHuge = new SpeedButton("huge", new ImageIcon(leafScaleHugeImage));
        this.leafScaleHuge.setBounds(206, 185, 47, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleHuge.Layout = blGlyphTop;
        this.leafScaleHuge.putClientProperty("tag", 4);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafScaleHuge.GroupIndex = 7;
        
        Image arrowLeafAngleImage = toolkit.createImage("../resources/WizardForm_arrowLeafAngle.png");
        this.arrowLeafAngle = new ImagePanel(new ImageIcon(arrowLeafAngleImage));
        this.arrowLeafAngle.setBounds(288, 167, 8, 16);
        
        Image leafAngleSmallImage = toolkit.createImage("../resources/WizardForm_leafAngleSmall.png");
        this.leafAngleSmall = new SpeedButton("small", new ImageIcon(leafAngleSmallImage));
        this.leafAngleSmall.setBounds(302, 185, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafAngleSmall.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafAngleSmall.GroupIndex = 9;
        
        Image leafAngleMediumImage = toolkit.createImage("../resources/WizardForm_leafAngleMedium.png");
        this.leafAngleMedium = new SpeedButton("medium", new ImageIcon(leafAngleMediumImage));
        this.leafAngleMedium.setSelected(true);
        this.leafAngleMedium.setBounds(346, 185, 59, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafAngleMedium.Layout = blGlyphTop;
        this.leafAngleMedium.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafAngleMedium.GroupIndex = 9;
        
        Image leafAngleLargeImage = toolkit.createImage("../resources/WizardForm_leafAngleLarge.png");
        this.leafAngleLarge = new SpeedButton("large", new ImageIcon(leafAngleLargeImage));
        this.leafAngleLarge.setBounds(404, 185, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafAngleLarge.Layout = blGlyphTop;
        this.leafAngleLarge.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafAngleLarge.GroupIndex = 9;
        
        Image arrowPetioleLengthImage = toolkit.createImage("../resources/WizardForm_arrowPetioleLength.png");
        this.arrowPetioleLength = new ImagePanel(new ImageIcon(arrowPetioleLengthImage));
        this.arrowPetioleLength.setBounds(288, 58, 8, 16);
        
        Image petioleVeryShortImage = toolkit.createImage("../resources/WizardForm_petioleVeryShort.png");
        this.petioleVeryShort = new SpeedButton("very short", new ImageIcon(petioleVeryShortImage));
        this.petioleVeryShort.setBounds(302, 76, 57, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleVeryShort.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleVeryShort.GroupIndex = 8;
        
        Image petioleShortImage = toolkit.createImage("../resources/WizardForm_petioleShort.png");
        this.petioleShort = new SpeedButton("short", new ImageIcon(petioleShortImage));
        this.petioleShort.setBounds(358, 76, 43, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleShort.Layout = blGlyphTop;
        this.petioleShort.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleShort.GroupIndex = 8;
        
        Image petioleMediumImage = toolkit.createImage("../resources/WizardForm_petioleMedium.png");
        this.petioleMedium = new SpeedButton("medium", new ImageIcon(petioleMediumImage));
        this.petioleMedium.setSelected(true);
        this.petioleMedium.setBounds(400, 76, 50, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleMedium.Layout = blGlyphTop;
        this.petioleMedium.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleMedium.GroupIndex = 8;
        
        Image petioleLongImage = toolkit.createImage("../resources/WizardForm_petioleLong.png");
        this.petioleLong = new SpeedButton("long", new ImageIcon(petioleLongImage));
        this.petioleLong.setBounds(449, 76, 42, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleLong.Layout = blGlyphTop;
        this.petioleLong.putClientProperty("tag", 3);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleLong.GroupIndex = 8;
        
        Image petioleVeryLongImage = toolkit.createImage("../resources/WizardForm_petioleVeryLong.png");
        this.petioleVeryLong = new SpeedButton("very long", new ImageIcon(petioleVeryLongImage));
        this.petioleVeryLong.setBounds(490, 76, 55, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleVeryLong.Layout = blGlyphTop;
        this.petioleVeryLong.putClientProperty("tag", 4);
        //  --------------- UNHANDLED ATTRIBUTE: this.petioleVeryLong.GroupIndex = 8;
        
        Image arrowLeafTdosImage = toolkit.createImage("../resources/WizardForm_arrowLeafTdos.png");
        this.arrowLeafTdos = new ImagePanel(new ImageIcon(arrowLeafTdosImage));
        this.arrowLeafTdos.setBounds(12, 58, 8, 16);
        
        this.Label4 = new JLabel("PlantStudio draws leaves using a \"3D object\" that represents a 3D leaf shape. The 3D object is drawn bigger as the leaf grows. Leaves are connected to the plant by a stalk called a petiole.");
        this.Label4.setBounds(12, 22, 527, 28);
        
        this.leafTdoSelectedLabel = new JLabel("leafTdoSelectedLabel");
        this.leafTdoSelectedLabel.setBounds(24, 148, 104, 14);
        
        this.leafTdosDraw = new JTable(new DefaultTableModel());
        this.leafTdosDraw.setBounds(24, 76, 250, 69);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.OnDrawCell = leafTdosDrawDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.RowCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.FixedRows = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.DefaultColWidth = 40;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.ColCount = 20;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.DefaultRowHeight = 50;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.ScrollBars = ssHorizontal;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.OnSelectCell = leafTdosDrawSelectCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafTdosDraw.Options = [goVertLine, goHorzLine];
        
        this.page4.add(panelLeavesLabel);
        this.page4.add(leafTdosLabel);
        this.page4.add(leafScaleLabel);
        this.page4.add(leafAngleLabel);
        this.page4.add(petioleLengthLabel);
        this.page4.add(arrowLeafScale);
        this.page4.add(leafScaleTiny);
        this.page4.add(leafScaleSmall);
        this.page4.add(leafScaleMedium);
        this.page4.add(leafScaleLarge);
        this.page4.add(leafScaleHuge);
        this.page4.add(arrowLeafAngle);
        this.page4.add(leafAngleSmall);
        this.page4.add(leafAngleMedium);
        this.page4.add(leafAngleLarge);
        this.page4.add(arrowPetioleLength);
        this.page4.add(petioleVeryShort);
        this.page4.add(petioleShort);
        this.page4.add(petioleMedium);
        this.page4.add(petioleLong);
        this.page4.add(petioleVeryLong);
        this.page4.add(arrowLeafTdos);
        this.page4.add(Label4);
        this.page4.add(leafTdoSelectedLabel);
        this.page4.add(leafTdosDraw);
        this.wizardNotebook.addTab("Leaves", null, this.page4);
        
        
        this.page5 = new JPanel(null);
        this.panelCompoundLeavesLabel = new JLabel("Compound leaves");
        this.panelCompoundLeavesLabel.setBounds(4, 4, 100, 14);
        
        Image arrowLeafletsImage = toolkit.createImage("../resources/WizardForm_arrowLeaflets.png");
        this.arrowLeaflets = new ImagePanel(new ImageIcon(arrowLeafletsImage));
        this.arrowLeaflets.setBounds(12, 72, 8, 16);
        
        this.leafletsLabel = new JLabel("How many leaflets should make up each leaf?");
        this.leafletsLabel.setBounds(24, 74, 222, 14);
        
        this.leafletsShapeLabel = new JLabel(" What shape should the compound leaves take?");
        this.leafletsShapeLabel.setBounds(22, 159, 231, 14);
        
        Image arrowLeafletsShapeImage = toolkit.createImage("../resources/WizardForm_arrowLeafletsShape.png");
        this.arrowLeafletsShape = new ImagePanel(new ImageIcon(arrowLeafletsShapeImage));
        this.arrowLeafletsShape.setBounds(12, 157, 8, 16);
        
        Image leafletsOneImage = toolkit.createImage("../resources/WizardForm_leafletsOne.png");
        this.leafletsOne = new SpeedButton("one (simple)", new ImageIcon(leafletsOneImage));
        this.leafletsOne.setSelected(true);
        this.leafletsOne.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leafletsOneClick(event);
            }
        });
        this.leafletsOne.setBounds(24, 90, 69, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsOne.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsOne.GroupIndex = 10;
        
        Image leafletsThreeImage = toolkit.createImage("../resources/WizardForm_leafletsThree.png");
        this.leafletsThree = new SpeedButton("three", new ImageIcon(leafletsThreeImage));
        this.leafletsThree.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leafletsThreeClick(event);
            }
        });
        this.leafletsThree.setBounds(92, 90, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsThree.Layout = blGlyphTop;
        this.leafletsThree.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsThree.GroupIndex = 10;
        
        Image leafletsFourImage = toolkit.createImage("../resources/WizardForm_leafletsFour.png");
        this.leafletsFour = new SpeedButton("four", new ImageIcon(leafletsFourImage));
        this.leafletsFour.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leafletsFourClick(event);
            }
        });
        this.leafletsFour.setBounds(136, 90, 46, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsFour.Layout = blGlyphTop;
        this.leafletsFour.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsFour.GroupIndex = 10;
        
        Image leafletsFiveImage = toolkit.createImage("../resources/WizardForm_leafletsFive.png");
        this.leafletsFive = new SpeedButton("five", new ImageIcon(leafletsFiveImage));
        this.leafletsFive.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leafletsFiveClick(event);
            }
        });
        this.leafletsFive.setBounds(181, 90, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsFive.Layout = blGlyphTop;
        this.leafletsFive.putClientProperty("tag", 3);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsFive.GroupIndex = 10;
        
        Image leafletsSevenImage = toolkit.createImage("../resources/WizardForm_leafletsSeven.png");
        this.leafletsSeven = new SpeedButton("seven", new ImageIcon(leafletsSevenImage));
        this.leafletsSeven.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                leafletsSevenClick(event);
            }
        });
        this.leafletsSeven.setBounds(225, 90, 47, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsSeven.Layout = blGlyphTop;
        this.leafletsSeven.putClientProperty("tag", 4);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsSeven.GroupIndex = 10;
        
        Image leafletsPinnateImage = toolkit.createImage("../resources/WizardForm_leafletsPinnate.png");
        this.leafletsPinnate = new SpeedButton("pinnate", new ImageIcon(leafletsPinnateImage));
        this.leafletsPinnate.setSelected(true);
        this.leafletsPinnate.setBounds(24, 175, 71, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsPinnate.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsPinnate.GroupIndex = 11;
        
        Image leafletsPalmateImage = toolkit.createImage("../resources/WizardForm_leafletsPalmate.png");
        this.leafletsPalmate = new SpeedButton("palmate", new ImageIcon(leafletsPalmateImage));
        this.leafletsPalmate.setBounds(94, 175, 60, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsPalmate.Layout = blGlyphTop;
        this.leafletsPalmate.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletsPalmate.GroupIndex = 11;
        
        Image arrowLeafletsSpacingImage = toolkit.createImage("../resources/WizardForm_arrowLeafletsSpacing.png");
        this.arrowLeafletsSpacing = new ImagePanel(new ImageIcon(arrowLeafletsSpacingImage));
        this.arrowLeafletsSpacing.setBounds(288, 72, 8, 16);
        
        this.leafletSpacingLabel = new JLabel("How spread out should the leaflets be?");
        this.leafletSpacingLabel.setBounds(300, 74, 190, 14);
        
        Image leafletSpacingCloseImage = toolkit.createImage("../resources/WizardForm_leafletSpacingClose.png");
        this.leafletSpacingClose = new SpeedButton("close", new ImageIcon(leafletSpacingCloseImage));
        this.leafletSpacingClose.setBounds(300, 90, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletSpacingClose.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletSpacingClose.GroupIndex = 12;
        
        Image leafletSpacingMediumImage = toolkit.createImage("../resources/WizardForm_leafletSpacingMedium.png");
        this.leafletSpacingMedium = new SpeedButton("medium", new ImageIcon(leafletSpacingMediumImage));
        this.leafletSpacingMedium.setSelected(true);
        this.leafletSpacingMedium.setBounds(344, 90, 59, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletSpacingMedium.Layout = blGlyphTop;
        this.leafletSpacingMedium.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletSpacingMedium.GroupIndex = 12;
        
        Image leafletSpacingFarImage = toolkit.createImage("../resources/WizardForm_leafletSpacingFar.png");
        this.leafletSpacingFar = new SpeedButton("far", new ImageIcon(leafletSpacingFarImage));
        this.leafletSpacingFar.setBounds(402, 90, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletSpacingFar.Layout = blGlyphTop;
        this.leafletSpacingFar.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.leafletSpacingFar.GroupIndex = 12;
        
        this.Label5 = new JLabel("A compound leaf is a leaf made up of two or more small parts called leaflets. The leaflets look like small whole leaves, but they always fit together in the same pattern for all the leaves on the plant (usually). A leaf without leaflets is a simple leaf.");
        this.Label5.setBounds(12, 22, 531, 42);
        
        this.page5.add(panelCompoundLeavesLabel);
        this.page5.add(arrowLeaflets);
        this.page5.add(leafletsLabel);
        this.page5.add(leafletsShapeLabel);
        this.page5.add(arrowLeafletsShape);
        this.page5.add(leafletsOne);
        this.page5.add(leafletsThree);
        this.page5.add(leafletsFour);
        this.page5.add(leafletsFive);
        this.page5.add(leafletsSeven);
        this.page5.add(leafletsPinnate);
        this.page5.add(leafletsPalmate);
        this.page5.add(arrowLeafletsSpacing);
        this.page5.add(leafletSpacingLabel);
        this.page5.add(leafletSpacingClose);
        this.page5.add(leafletSpacingMedium);
        this.page5.add(leafletSpacingFar);
        this.page5.add(Label5);
        this.wizardNotebook.addTab("Compound leaves", null, this.page5);
        
        
        this.page6 = new JPanel(null);
        this.panelInflorPlacementLabel = new JLabel("Inflorescence placement");
        this.panelInflorPlacementLabel.setBounds(4, 4, 137, 14);
        
        this.apicalInflorsNumberLabel = new JLabel("How many apical inflorescences should there be?");
        this.apicalInflorsNumberLabel.setBounds(24, 87, 242, 14);
        
        this.axillaryInflorsNumberLabel = new JLabel("How many axillary inflorescences should there be?");
        this.axillaryInflorsNumberLabel.setBounds(308, 87, 248, 14);
        
        this.apicalStalkLabel = new JLabel("How long should their primary stems be?");
        this.apicalStalkLabel.setBounds(24, 171, 197, 14);
        
        this.axillaryStalkLabel = new JLabel("How long should their primary stems be?");
        this.axillaryStalkLabel.setBounds(308, 171, 197, 14);
        
        Image apicalInflorExtraImageImage = toolkit.createImage("../resources/WizardForm_apicalInflorExtraImage.png");
        this.apicalInflorExtraImage = new ImagePanel(new ImageIcon(apicalInflorExtraImageImage));
        this.apicalInflorExtraImage.setBounds(24, 55, 16, 16);
        
        Image axillaryInflorExtraImageImage = toolkit.createImage("../resources/WizardForm_axillaryInflorExtraImage.png");
        this.axillaryInflorExtraImage = new ImagePanel(new ImageIcon(axillaryInflorExtraImageImage));
        this.axillaryInflorExtraImage.setBounds(308, 53, 16, 16);
        
        Image apicalInflorsNoneImage = toolkit.createImage("../resources/WizardForm_apicalInflorsNone.png");
        this.apicalInflorsNone = new SpeedButton("none", new ImageIcon(apicalInflorsNoneImage));
        this.apicalInflorsNone.setSelected(true);
        this.apicalInflorsNone.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                apicalInflorsNoneClick(event);
            }
        });
        this.apicalInflorsNone.setBounds(24, 104, 41, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsNone.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsNone.GroupIndex = 17;
        
        Image apicalInflorsOneImage = toolkit.createImage("../resources/WizardForm_apicalInflorsOne.png");
        this.apicalInflorsOne = new SpeedButton("one", new ImageIcon(apicalInflorsOneImage));
        this.apicalInflorsOne.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                apicalInflorsOneClick(event);
            }
        });
        this.apicalInflorsOne.setBounds(64, 104, 39, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsOne.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsOne.GroupIndex = 17;
        
        Image apicalInflorsTwoImage = toolkit.createImage("../resources/WizardForm_apicalInflorsTwo.png");
        this.apicalInflorsTwo = new SpeedButton("two", new ImageIcon(apicalInflorsTwoImage));
        this.apicalInflorsTwo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                apicalInflorsTwoClick(event);
            }
        });
        this.apicalInflorsTwo.setBounds(102, 104, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsTwo.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsTwo.GroupIndex = 17;
        
        Image apicalInflorsThreeImage = toolkit.createImage("../resources/WizardForm_apicalInflorsThree.png");
        this.apicalInflorsThree = new SpeedButton("three", new ImageIcon(apicalInflorsThreeImage));
        this.apicalInflorsThree.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                apicalInflorsThreeClick(event);
            }
        });
        this.apicalInflorsThree.setBounds(146, 104, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsThree.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsThree.GroupIndex = 17;
        
        Image apicalInflorsFiveImage = toolkit.createImage("../resources/WizardForm_apicalInflorsFive.png");
        this.apicalInflorsFive = new SpeedButton("five", new ImageIcon(apicalInflorsFiveImage));
        this.apicalInflorsFive.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                apicalInflorsFiveClick(event);
            }
        });
        this.apicalInflorsFive.setBounds(190, 104, 40, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsFive.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalInflorsFive.GroupIndex = 17;
        
        Image arrowApicalInflorsNumberImage = toolkit.createImage("../resources/WizardForm_arrowApicalInflorsNumber.png");
        this.arrowApicalInflorsNumber = new ImagePanel(new ImageIcon(arrowApicalInflorsNumberImage));
        this.arrowApicalInflorsNumber.setBounds(12, 85, 8, 16);
        
        Image axillaryInflorsNoneImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsNone.png");
        this.axillaryInflorsNone = new SpeedButton("none", new ImageIcon(axillaryInflorsNoneImage));
        this.axillaryInflorsNone.setSelected(true);
        this.axillaryInflorsNone.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                axillaryInflorsNoneClick(event);
            }
        });
        this.axillaryInflorsNone.setBounds(308, 104, 41, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsNone.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsNone.GroupIndex = 18;
        
        Image axillaryInflorsThreeImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsThree.png");
        this.axillaryInflorsThree = new SpeedButton("three", new ImageIcon(axillaryInflorsThreeImage));
        this.axillaryInflorsThree.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                axillaryInflorsThreeClick(event);
            }
        });
        this.axillaryInflorsThree.setBounds(348, 104, 44, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsThree.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsThree.GroupIndex = 18;
        
        Image axillaryInflorsFiveImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsFive.png");
        this.axillaryInflorsFive = new SpeedButton("five", new ImageIcon(axillaryInflorsFiveImage));
        this.axillaryInflorsFive.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                axillaryInflorsFiveClick(event);
            }
        });
        this.axillaryInflorsFive.setBounds(391, 104, 43, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsFive.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsFive.GroupIndex = 18;
        
        Image axillaryInflorsTenImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsTen.png");
        this.axillaryInflorsTen = new SpeedButton("ten", new ImageIcon(axillaryInflorsTenImage));
        this.axillaryInflorsTen.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                axillaryInflorsTenClick(event);
            }
        });
        this.axillaryInflorsTen.setBounds(433, 104, 44, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsTen.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsTen.GroupIndex = 18;
        
        Image axillaryInflorsTwentyImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsTwenty.png");
        this.axillaryInflorsTwenty = new SpeedButton("twenty", new ImageIcon(axillaryInflorsTwentyImage));
        this.axillaryInflorsTwenty.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                axillaryInflorsTwentyClick(event);
            }
        });
        this.axillaryInflorsTwenty.setBounds(476, 104, 51, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsTwenty.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryInflorsTwenty.GroupIndex = 18;
        
        Image arrowAxillaryInflorsNumberImage = toolkit.createImage("../resources/WizardForm_arrowAxillaryInflorsNumber.png");
        this.arrowAxillaryInflorsNumber = new ImagePanel(new ImageIcon(arrowAxillaryInflorsNumberImage));
        this.arrowAxillaryInflorsNumber.setBounds(294, 85, 8, 16);
        
        Image apicalStalkVeryShortImage = toolkit.createImage("../resources/WizardForm_apicalStalkVeryShort.png");
        this.apicalStalkVeryShort = new SpeedButton("very short", new ImageIcon(apicalStalkVeryShortImage));
        this.apicalStalkVeryShort.setBounds(24, 188, 64, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkVeryShort.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkVeryShort.GroupIndex = 19;
        
        Image apicalStalkShortImage = toolkit.createImage("../resources/WizardForm_apicalStalkShort.png");
        this.apicalStalkShort = new SpeedButton("short", new ImageIcon(apicalStalkShortImage));
        this.apicalStalkShort.setBounds(87, 188, 38, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkShort.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkShort.GroupIndex = 19;
        
        Image apicalStalkMediumImage = toolkit.createImage("../resources/WizardForm_apicalStalkMedium.png");
        this.apicalStalkMedium = new SpeedButton("medium", new ImageIcon(apicalStalkMediumImage));
        this.apicalStalkMedium.setSelected(true);
        this.apicalStalkMedium.setBounds(125, 188, 52, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkMedium.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkMedium.GroupIndex = 19;
        
        Image apicalStalkLongImage = toolkit.createImage("../resources/WizardForm_apicalStalkLong.png");
        this.apicalStalkLong = new SpeedButton("long", new ImageIcon(apicalStalkLongImage));
        this.apicalStalkLong.setBounds(177, 188, 39, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkLong.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkLong.GroupIndex = 19;
        
        Image apicalStalkVeryLongImage = toolkit.createImage("../resources/WizardForm_apicalStalkVeryLong.png");
        this.apicalStalkVeryLong = new SpeedButton("very long", new ImageIcon(apicalStalkVeryLongImage));
        this.apicalStalkVeryLong.setBounds(215, 188, 57, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkVeryLong.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.apicalStalkVeryLong.GroupIndex = 19;
        
        Image arrowApicalStalkImage = toolkit.createImage("../resources/WizardForm_arrowApicalStalk.png");
        this.arrowApicalStalk = new ImagePanel(new ImageIcon(arrowApicalStalkImage));
        this.arrowApicalStalk.setBounds(12, 169, 8, 16);
        
        Image arrowAxillaryStalkImage = toolkit.createImage("../resources/WizardForm_arrowAxillaryStalk.png");
        this.arrowAxillaryStalk = new ImagePanel(new ImageIcon(arrowAxillaryStalkImage));
        this.arrowAxillaryStalk.setBounds(294, 169, 8, 16);
        
        Image axillaryStalkVeryShortImage = toolkit.createImage("../resources/WizardForm_axillaryStalkVeryShort.png");
        this.axillaryStalkVeryShort = new SpeedButton("very short", new ImageIcon(axillaryStalkVeryShortImage));
        this.axillaryStalkVeryShort.setBounds(308, 188, 60, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkVeryShort.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkVeryShort.GroupIndex = 20;
        
        Image axillaryStalkShortImage = toolkit.createImage("../resources/WizardForm_axillaryStalkShort.png");
        this.axillaryStalkShort = new SpeedButton("short", new ImageIcon(axillaryStalkShortImage));
        this.axillaryStalkShort.setBounds(367, 188, 40, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkShort.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkShort.GroupIndex = 20;
        
        Image axillaryStalkMediumImage = toolkit.createImage("../resources/WizardForm_axillaryStalkMedium.png");
        this.axillaryStalkMedium = new SpeedButton("medium", new ImageIcon(axillaryStalkMediumImage));
        this.axillaryStalkMedium.setSelected(true);
        this.axillaryStalkMedium.setBounds(406, 188, 50, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkMedium.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkMedium.GroupIndex = 20;
        
        Image axillaryStalkLongImage = toolkit.createImage("../resources/WizardForm_axillaryStalkLong.png");
        this.axillaryStalkLong = new SpeedButton("long", new ImageIcon(axillaryStalkLongImage));
        this.axillaryStalkLong.setBounds(455, 188, 40, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkLong.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkLong.GroupIndex = 20;
        
        Image axillaryStalkVeryLongImage = toolkit.createImage("../resources/WizardForm_axillaryStalkVeryLong.png");
        this.axillaryStalkVeryLong = new SpeedButton("very long", new ImageIcon(axillaryStalkVeryLongImage));
        this.axillaryStalkVeryLong.setBounds(494, 188, 57, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkVeryLong.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.axillaryStalkVeryLong.GroupIndex = 20;
        
        this.Label3 = new JLabel("Apical inflorescences are at the ends (apexes) of plant stems.");
        this.Label3.setBounds(42, 53, 157, 28);
        
        this.Label6 = new JLabel("An inflorescence holds flowers and fruits on a plant. Since most plants have hermaphroditic flowers (with both male and female parts), the wizard creates only primary (female or hermaphroditic) flowers.");
        this.Label6.setBounds(12, 22, 540, 28);
        
        this.Label7 = new JLabel("Axillary inflorescences are in the angles between leaf and stem (axils).");
        this.Label7.setBounds(330, 53, 182, 28);
        
        this.page6.add(panelInflorPlacementLabel);
        this.page6.add(apicalInflorsNumberLabel);
        this.page6.add(axillaryInflorsNumberLabel);
        this.page6.add(apicalStalkLabel);
        this.page6.add(axillaryStalkLabel);
        this.page6.add(apicalInflorExtraImage);
        this.page6.add(axillaryInflorExtraImage);
        this.page6.add(apicalInflorsNone);
        this.page6.add(apicalInflorsOne);
        this.page6.add(apicalInflorsTwo);
        this.page6.add(apicalInflorsThree);
        this.page6.add(apicalInflorsFive);
        this.page6.add(arrowApicalInflorsNumber);
        this.page6.add(axillaryInflorsNone);
        this.page6.add(axillaryInflorsThree);
        this.page6.add(axillaryInflorsFive);
        this.page6.add(axillaryInflorsTen);
        this.page6.add(axillaryInflorsTwenty);
        this.page6.add(arrowAxillaryInflorsNumber);
        this.page6.add(apicalStalkVeryShort);
        this.page6.add(apicalStalkShort);
        this.page6.add(apicalStalkMedium);
        this.page6.add(apicalStalkLong);
        this.page6.add(apicalStalkVeryLong);
        this.page6.add(arrowApicalStalk);
        this.page6.add(arrowAxillaryStalk);
        this.page6.add(axillaryStalkVeryShort);
        this.page6.add(axillaryStalkShort);
        this.page6.add(axillaryStalkMedium);
        this.page6.add(axillaryStalkLong);
        this.page6.add(axillaryStalkVeryLong);
        this.page6.add(Label3);
        this.page6.add(Label6);
        this.page6.add(Label7);
        this.wizardNotebook.addTab("Inflorescence placement", null, this.page6);
        
        
        this.page7 = new JPanel(null);
        this.panelInflorDrawingLabel = new JLabel("Inflorescence drawing");
        this.panelInflorDrawingLabel.setBounds(4, 4, 124, 14);
        
        this.inflorFlowersLabel = new JLabel("How many flowers should each inflorescence have?");
        this.inflorFlowersLabel.setBounds(26, 59, 257, 14);
        
        this.inflorShapeLabel = new JLabel(" What shape should each inflorescence have?");
        this.inflorShapeLabel.setBounds(24, 146, 225, 14);
        
        Image arrowInflorFlowersImage = toolkit.createImage("../resources/WizardForm_arrowInflorFlowers.png");
        this.arrowInflorFlowers = new ImagePanel(new ImageIcon(arrowInflorFlowersImage));
        this.arrowInflorFlowers.setBounds(12, 57, 8, 16);
        
        Image arrowInflorShapeImage = toolkit.createImage("../resources/WizardForm_arrowInflorShape.png");
        this.arrowInflorShape = new ImagePanel(new ImageIcon(arrowInflorShapeImage));
        this.arrowInflorShape.setBounds(12, 144, 8, 16);
        
        Image inflorFlowersOneImage = toolkit.createImage("../resources/WizardForm_inflorFlowersOne.png");
        this.inflorFlowersOne = new SpeedButton("one", new ImageIcon(inflorFlowersOneImage));
        this.inflorFlowersOne.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                inflorFlowersOneClick(event);
            }
        });
        this.inflorFlowersOne.setBounds(24, 76, 36, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersOne.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersOne.GroupIndex = 15;
        
        Image inflorFlowersTwoImage = toolkit.createImage("../resources/WizardForm_inflorFlowersTwo.png");
        this.inflorFlowersTwo = new SpeedButton("two", new ImageIcon(inflorFlowersTwoImage));
        this.inflorFlowersTwo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                inflorFlowersTwoClick(event);
            }
        });
        this.inflorFlowersTwo.setBounds(59, 76, 39, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersTwo.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersTwo.GroupIndex = 15;
        
        Image inflorFlowersThreeImage = toolkit.createImage("../resources/WizardForm_inflorFlowersThree.png");
        this.inflorFlowersThree = new SpeedButton("three", new ImageIcon(inflorFlowersThreeImage));
        this.inflorFlowersThree.setSelected(true);
        this.inflorFlowersThree.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                inflorFlowersThreeClick(event);
            }
        });
        this.inflorFlowersThree.setBounds(97, 76, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersThree.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersThree.GroupIndex = 15;
        
        Image inflorFlowersFiveImage = toolkit.createImage("../resources/WizardForm_inflorFlowersFive.png");
        this.inflorFlowersFive = new SpeedButton("five", new ImageIcon(inflorFlowersFiveImage));
        this.inflorFlowersFive.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                inflorFlowersFiveClick(event);
            }
        });
        this.inflorFlowersFive.setBounds(141, 76, 40, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersFive.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersFive.GroupIndex = 15;
        
        Image inflorFlowersTenImage = toolkit.createImage("../resources/WizardForm_inflorFlowersTen.png");
        this.inflorFlowersTen = new SpeedButton("ten", new ImageIcon(inflorFlowersTenImage));
        this.inflorFlowersTen.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                inflorFlowersTenClick(event);
            }
        });
        this.inflorFlowersTen.setBounds(180, 76, 40, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersTen.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersTen.GroupIndex = 15;
        
        Image inflorFlowersTwentyImage = toolkit.createImage("../resources/WizardForm_inflorFlowersTwenty.png");
        this.inflorFlowersTwenty = new SpeedButton("twenty", new ImageIcon(inflorFlowersTwentyImage));
        this.inflorFlowersTwenty.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                inflorFlowersTwentyClick(event);
            }
        });
        this.inflorFlowersTwenty.setBounds(219, 76, 50, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersTwenty.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorFlowersTwenty.GroupIndex = 15;
        
        Image inflorShapeSpikeImage = toolkit.createImage("../resources/WizardForm_inflorShapeSpike.png");
        this.inflorShapeSpike = new SpeedButton("spike", new ImageIcon(inflorShapeSpikeImage));
        this.inflorShapeSpike.setBounds(24, 163, 42, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeSpike.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeSpike.GroupIndex = 16;
        
        Image inflorShapeRacemeImage = toolkit.createImage("../resources/WizardForm_inflorShapeRaceme.png");
        this.inflorShapeRaceme = new SpeedButton("raceme", new ImageIcon(inflorShapeRacemeImage));
        this.inflorShapeRaceme.setSelected(true);
        this.inflorShapeRaceme.setBounds(65, 163, 57, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeRaceme.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeRaceme.GroupIndex = 16;
        
        Image inflorShapePanicleImage = toolkit.createImage("../resources/WizardForm_inflorShapePanicle.png");
        this.inflorShapePanicle = new SpeedButton("panicle", new ImageIcon(inflorShapePanicleImage));
        this.inflorShapePanicle.setBounds(122, 163, 50, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapePanicle.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapePanicle.GroupIndex = 16;
        
        Image inflorShapeUmbelImage = toolkit.createImage("../resources/WizardForm_inflorShapeUmbel.png");
        this.inflorShapeUmbel = new SpeedButton("umbel", new ImageIcon(inflorShapeUmbelImage));
        this.inflorShapeUmbel.setBounds(171, 163, 48, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeUmbel.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeUmbel.GroupIndex = 16;
        
        Image inflorShapeClusterImage = toolkit.createImage("../resources/WizardForm_inflorShapeCluster.png");
        this.inflorShapeCluster = new SpeedButton("cluster", new ImageIcon(inflorShapeClusterImage));
        this.inflorShapeCluster.setBounds(218, 163, 47, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeCluster.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeCluster.GroupIndex = 16;
        
        Image inflorShapeHeadImage = toolkit.createImage("../resources/WizardForm_inflorShapeHead.png");
        this.inflorShapeHead = new SpeedButton("head", new ImageIcon(inflorShapeHeadImage));
        this.inflorShapeHead.setBounds(264, 163, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeHead.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorShapeHead.GroupIndex = 16;
        
        Image arrowInflorThicknessImage = toolkit.createImage("../resources/WizardForm_arrowInflorThickness.png");
        this.arrowInflorThickness = new ImagePanel(new ImageIcon(arrowInflorThicknessImage));
        this.arrowInflorThickness.setBounds(294, 57, 8, 16);
        
        this.inflorThicknessLabel = new JLabel("How thick should each inflorescence stem be?");
        this.inflorThicknessLabel.setBounds(308, 59, 226, 14);
        
        Image inflorWidthVeryThinImage = toolkit.createImage("../resources/WizardForm_inflorWidthVeryThin.png");
        this.inflorWidthVeryThin = new SpeedButton("very thin", new ImageIcon(inflorWidthVeryThinImage));
        this.inflorWidthVeryThin.setBounds(308, 76, 56, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthVeryThin.Layout = blGlyphTop;
        this.inflorWidthVeryThin.setToolTipText("very short");
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthVeryThin.GroupIndex = 24;
        
        Image inflorWidthThinImage = toolkit.createImage("../resources/WizardForm_inflorWidthThin.png");
        this.inflorWidthThin = new SpeedButton("thin", new ImageIcon(inflorWidthThinImage));
        this.inflorWidthThin.setSelected(true);
        this.inflorWidthThin.setBounds(364, 76, 36, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthThin.Layout = blGlyphTop;
        this.inflorWidthThin.setToolTipText("short");
        this.inflorWidthThin.putClientProperty("tag", 1);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthThin.GroupIndex = 24;
        
        Image inflorWidthMediumImage = toolkit.createImage("../resources/WizardForm_inflorWidthMedium.png");
        this.inflorWidthMedium = new SpeedButton("medium", new ImageIcon(inflorWidthMediumImage));
        this.inflorWidthMedium.setBounds(400, 76, 49, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthMedium.Layout = blGlyphTop;
        this.inflorWidthMedium.setToolTipText("medium");
        this.inflorWidthMedium.putClientProperty("tag", 2);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthMedium.GroupIndex = 24;
        
        Image inflorWidthThickImage = toolkit.createImage("../resources/WizardForm_inflorWidthThick.png");
        this.inflorWidthThick = new SpeedButton("thick", new ImageIcon(inflorWidthThickImage));
        this.inflorWidthThick.setBounds(448, 76, 37, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthThick.Layout = blGlyphTop;
        this.inflorWidthThick.setToolTipText("long");
        this.inflorWidthThick.putClientProperty("tag", 3);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthThick.GroupIndex = 24;
        
        Image inflorWidthVeryThickImage = toolkit.createImage("../resources/WizardForm_inflorWidthVeryThick.png");
        this.inflorWidthVeryThick = new SpeedButton("very thick", new ImageIcon(inflorWidthVeryThickImage));
        this.inflorWidthVeryThick.setBounds(484, 76, 59, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthVeryThick.Layout = blGlyphTop;
        this.inflorWidthVeryThick.setToolTipText("very long");
        this.inflorWidthVeryThick.putClientProperty("tag", 4);
        //  --------------- UNHANDLED ATTRIBUTE: this.inflorWidthVeryThick.GroupIndex = 24;
        
        this.Label8 = new JLabel("Inflorescences can have a large variety of shapes, a few of which are shown here. We extend the true meaning of \"inflorescence\" a bit to use an inflorescence when there is only one flower. ");
        this.Label8.setBounds(12, 22, 485, 28);
        
        this.page7.add(panelInflorDrawingLabel);
        this.page7.add(inflorFlowersLabel);
        this.page7.add(inflorShapeLabel);
        this.page7.add(arrowInflorFlowers);
        this.page7.add(arrowInflorShape);
        this.page7.add(inflorFlowersOne);
        this.page7.add(inflorFlowersTwo);
        this.page7.add(inflorFlowersThree);
        this.page7.add(inflorFlowersFive);
        this.page7.add(inflorFlowersTen);
        this.page7.add(inflorFlowersTwenty);
        this.page7.add(inflorShapeSpike);
        this.page7.add(inflorShapeRaceme);
        this.page7.add(inflorShapePanicle);
        this.page7.add(inflorShapeUmbel);
        this.page7.add(inflorShapeCluster);
        this.page7.add(inflorShapeHead);
        this.page7.add(arrowInflorThickness);
        this.page7.add(inflorThicknessLabel);
        this.page7.add(inflorWidthVeryThin);
        this.page7.add(inflorWidthThin);
        this.page7.add(inflorWidthMedium);
        this.page7.add(inflorWidthThick);
        this.page7.add(inflorWidthVeryThick);
        this.page7.add(Label8);
        this.wizardNotebook.addTab("Inflorescences", null, this.page7);
        
        
        this.page8 = new JPanel(null);
        this.panelFlowersLabel = new JLabel("Flowers");
        this.panelFlowersLabel.setBounds(8, 4, 45, 14);
        
        this.petalTdosLabel = new JLabel(" What 3D object should be used for a flower petal?");
        this.petalTdosLabel.setBounds(22, 60, 246, 14);
        
        this.petalScaleLabel = new JLabel("How big should a flower petal be drawn?");
        this.petalScaleLabel.setBounds(302, 60, 201, 14);
        
        this.petalsNumberLabel = new JLabel("How many flower petals should a flower have?");
        this.petalsNumberLabel.setBounds(24, 170, 231, 14);
        
        Image petalsOneImage = toolkit.createImage("../resources/WizardForm_petalsOne.png");
        this.petalsOne = new SpeedButton("one", new ImageIcon(petalsOneImage));
        this.petalsOne.setBounds(24, 187, 37, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsOne.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsOne.GroupIndex = 13;
        
        Image petalsThreeImage = toolkit.createImage("../resources/WizardForm_petalsThree.png");
        this.petalsThree = new SpeedButton("three", new ImageIcon(petalsThreeImage));
        this.petalsThree.setBounds(60, 187, 42, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsThree.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsThree.GroupIndex = 13;
        
        Image petalsFourImage = toolkit.createImage("../resources/WizardForm_petalsFour.png");
        this.petalsFour = new SpeedButton("four", new ImageIcon(petalsFourImage));
        this.petalsFour.setBounds(101, 187, 40, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsFour.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsFour.GroupIndex = 13;
        
        Image petalsFiveImage = toolkit.createImage("../resources/WizardForm_petalsFive.png");
        this.petalsFive = new SpeedButton("five", new ImageIcon(petalsFiveImage));
        this.petalsFive.setSelected(true);
        this.petalsFive.setBounds(140, 187, 37, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsFive.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsFive.GroupIndex = 13;
        
        Image petalsTenImage = toolkit.createImage("../resources/WizardForm_petalsTen.png");
        this.petalsTen = new SpeedButton("ten", new ImageIcon(petalsTenImage));
        this.petalsTen.setBounds(176, 187, 36, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsTen.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalsTen.GroupIndex = 13;
        
        Image petalScaleTinyImage = toolkit.createImage("../resources/WizardForm_petalScaleTiny.png");
        this.petalScaleTiny = new SpeedButton("tiny", new ImageIcon(petalScaleTinyImage));
        this.petalScaleTiny.setBounds(302, 76, 43, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleTiny.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleTiny.GroupIndex = 14;
        
        Image petalScaleSmallImage = toolkit.createImage("../resources/WizardForm_petalScaleSmall.png");
        this.petalScaleSmall = new SpeedButton("small", new ImageIcon(petalScaleSmallImage));
        this.petalScaleSmall.setSelected(true);
        this.petalScaleSmall.setBounds(344, 76, 47, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleSmall.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleSmall.GroupIndex = 14;
        
        Image petalScaleMediumImage = toolkit.createImage("../resources/WizardForm_petalScaleMedium.png");
        this.petalScaleMedium = new SpeedButton("medium", new ImageIcon(petalScaleMediumImage));
        this.petalScaleMedium.setBounds(390, 76, 58, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleMedium.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleMedium.GroupIndex = 14;
        
        Image petalScaleLargeImage = toolkit.createImage("../resources/WizardForm_petalScaleLarge.png");
        this.petalScaleLarge = new SpeedButton("large", new ImageIcon(petalScaleLargeImage));
        this.petalScaleLarge.setBounds(447, 76, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleLarge.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleLarge.GroupIndex = 14;
        
        Image petalScaleHugeImage = toolkit.createImage("../resources/WizardForm_petalScaleHuge.png");
        this.petalScaleHuge = new SpeedButton("huge", new ImageIcon(petalScaleHugeImage));
        this.petalScaleHuge.setBounds(491, 76, 46, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleHuge.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalScaleHuge.GroupIndex = 14;
        
        Image arrowPetalTdosImage = toolkit.createImage("../resources/WizardForm_arrowPetalTdos.png");
        this.arrowPetalTdos = new ImagePanel(new ImageIcon(arrowPetalTdosImage));
        this.arrowPetalTdos.setBounds(12, 58, 8, 16);
        
        Image arrowPetalsNumberImage = toolkit.createImage("../resources/WizardForm_arrowPetalsNumber.png");
        this.arrowPetalsNumber = new ImagePanel(new ImageIcon(arrowPetalsNumberImage));
        this.arrowPetalsNumber.setBounds(12, 169, 8, 16);
        
        Image arrowPetalScaleImage = toolkit.createImage("../resources/WizardForm_arrowPetalScale.png");
        this.arrowPetalScale = new ImagePanel(new ImageIcon(arrowPetalScaleImage));
        this.arrowPetalScale.setBounds(288, 58, 8, 16);
        
        Image arrowPetalColorImage = toolkit.createImage("../resources/WizardForm_arrowPetalColor.png");
        this.arrowPetalColor = new ImagePanel(new ImageIcon(arrowPetalColorImage));
        this.arrowPetalColor.setBounds(288, 173, 8, 16);
        
        this.petalColorLabel = new JLabel(" What color should flowers be drawn?");
        this.petalColorLabel.setBounds(300, 173, 187, 14);
        
        this.flowerColorExplainLabel = new JLabel("Click in the square to change the color.");
        this.flowerColorExplainLabel.setBounds(352, 211, 187, 14);
        
        this.Label9 = new JLabel("Like leaves, flowers are drawn using a 3D object. But here the 3D object represents only one petal of the flower. A number of petals is drawn rotated around a center to produce what looks like a flower.");
        this.Label9.setBounds(12, 22, 511, 28);
        
        this.petalTdoSelectedLabel = new JLabel("petalTdoSelectedLabel");
        this.petalTdoSelectedLabel.setBounds(24, 148, 109, 14);
        
        this.petalTdosDraw = new JTable(new DefaultTableModel());
        this.petalTdosDraw.setBounds(24, 76, 250, 69);
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.OnDrawCell = petalTdosDrawDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.RowCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.FixedRows = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.DefaultColWidth = 40;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.ColCount = 20;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.DefaultRowHeight = 50;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.ScrollBars = ssHorizontal;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.OnSelectCell = petalTdosDrawSelectCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.petalTdosDraw.Options = [goVertLine, goHorzLine];
        
        this.petalColor = new JPanel(null);
        // -- this.petalColor.setLayout(new BoxLayout(this.petalColor, BoxLayout.Y_AXIS));
        this.petalColor.setBounds(302, 197, 41, 41);
        this.petalColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                petalColorMouseUp(event);
            }
        });
        
        this.page8.add(panelFlowersLabel);
        this.page8.add(petalTdosLabel);
        this.page8.add(petalScaleLabel);
        this.page8.add(petalsNumberLabel);
        this.page8.add(petalsOne);
        this.page8.add(petalsThree);
        this.page8.add(petalsFour);
        this.page8.add(petalsFive);
        this.page8.add(petalsTen);
        this.page8.add(petalScaleTiny);
        this.page8.add(petalScaleSmall);
        this.page8.add(petalScaleMedium);
        this.page8.add(petalScaleLarge);
        this.page8.add(petalScaleHuge);
        this.page8.add(arrowPetalTdos);
        this.page8.add(arrowPetalsNumber);
        this.page8.add(arrowPetalScale);
        this.page8.add(arrowPetalColor);
        this.page8.add(petalColorLabel);
        this.page8.add(flowerColorExplainLabel);
        this.page8.add(Label9);
        this.page8.add(petalTdoSelectedLabel);
        this.page8.add(petalTdosDraw);
        this.page8.add(petalColor);
        this.wizardNotebook.addTab("Flowers", null, this.page8);
        
        
        this.page9 = new JPanel(null);
        this.fruitTdoLabel = new JLabel(" What 3D object should be used to draw each fruit section?");
        this.fruitTdoLabel.setBounds(22, 77, 287, 14);
        
        this.fruitSectionsNumberLabel = new JLabel("How many fruit sections should be used to draw the fruit?");
        this.fruitSectionsNumberLabel.setBounds(24, 187, 282, 14);
        
        this.fruitScaleLabel = new JLabel("How big should fruit sections be drawn?");
        this.fruitScaleLabel.setBounds(328, 77, 197, 14);
        
        this.panelFruitsLabel = new JLabel("Fruits");
        this.panelFruitsLabel.setBounds(4, 4, 32, 14);
        
        Image arrowFruitTdoImage = toolkit.createImage("../resources/WizardForm_arrowFruitTdo.png");
        this.arrowFruitTdo = new ImagePanel(new ImageIcon(arrowFruitTdoImage));
        this.arrowFruitTdo.setBounds(12, 75, 8, 16);
        
        Image arrowFruitSectionsNumberImage = toolkit.createImage("../resources/WizardForm_arrowFruitSectionsNumber.png");
        this.arrowFruitSectionsNumber = new ImagePanel(new ImageIcon(arrowFruitSectionsNumberImage));
        this.arrowFruitSectionsNumber.setBounds(12, 185, 8, 16);
        
        Image arrowFruitScaleImage = toolkit.createImage("../resources/WizardForm_arrowFruitScale.png");
        this.arrowFruitScale = new ImagePanel(new ImageIcon(arrowFruitScaleImage));
        this.arrowFruitScale.setBounds(316, 75, 8, 16);
        
        Image fruitSectionsOneImage = toolkit.createImage("../resources/WizardForm_fruitSectionsOne.png");
        this.fruitSectionsOne = new SpeedButton("one", new ImageIcon(fruitSectionsOneImage));
        this.fruitSectionsOne.setBounds(24, 203, 41, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsOne.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsOne.GroupIndex = 21;
        
        Image fruitSectionsThreeImage = toolkit.createImage("../resources/WizardForm_fruitSectionsThree.png");
        this.fruitSectionsThree = new SpeedButton("three", new ImageIcon(fruitSectionsThreeImage));
        this.fruitSectionsThree.setBounds(64, 203, 43, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsThree.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsThree.GroupIndex = 21;
        
        Image fruitSectionsFourImage = toolkit.createImage("../resources/WizardForm_fruitSectionsFour.png");
        this.fruitSectionsFour = new SpeedButton("four", new ImageIcon(fruitSectionsFourImage));
        this.fruitSectionsFour.setBounds(106, 203, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsFour.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsFour.GroupIndex = 21;
        
        Image fruitSectionsFiveImage = toolkit.createImage("../resources/WizardForm_fruitSectionsFive.png");
        this.fruitSectionsFive = new SpeedButton("five", new ImageIcon(fruitSectionsFiveImage));
        this.fruitSectionsFive.setSelected(true);
        this.fruitSectionsFive.setBounds(148, 203, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsFive.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsFive.GroupIndex = 21;
        
        Image fruitSectionsTenImage = toolkit.createImage("../resources/WizardForm_fruitSectionsTen.png");
        this.fruitSectionsTen = new SpeedButton("ten", new ImageIcon(fruitSectionsTenImage));
        this.fruitSectionsTen.setBounds(192, 203, 40, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsTen.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitSectionsTen.GroupIndex = 21;
        
        Image fruitScaleTinyImage = toolkit.createImage("../resources/WizardForm_fruitScaleTiny.png");
        this.fruitScaleTiny = new SpeedButton("tiny", new ImageIcon(fruitScaleTinyImage));
        this.fruitScaleTiny.setBounds(328, 93, 41, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleTiny.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleTiny.GroupIndex = 22;
        
        Image fruitScaleSmallImage = toolkit.createImage("../resources/WizardForm_fruitScaleSmall.png");
        this.fruitScaleSmall = new SpeedButton("small", new ImageIcon(fruitScaleSmallImage));
        this.fruitScaleSmall.setSelected(true);
        this.fruitScaleSmall.setBounds(368, 93, 43, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleSmall.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleSmall.GroupIndex = 22;
        
        Image fruitScaleMediumImage = toolkit.createImage("../resources/WizardForm_fruitScaleMedium.png");
        this.fruitScaleMedium = new SpeedButton("medium", new ImageIcon(fruitScaleMediumImage));
        this.fruitScaleMedium.setBounds(410, 93, 56, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleMedium.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleMedium.GroupIndex = 22;
        
        Image fruitScaleLargeImage = toolkit.createImage("../resources/WizardForm_fruitScaleLarge.png");
        this.fruitScaleLarge = new SpeedButton("large", new ImageIcon(fruitScaleLargeImage));
        this.fruitScaleLarge.setBounds(465, 93, 45, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleLarge.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleLarge.GroupIndex = 22;
        
        Image fruitScaleHugeImage = toolkit.createImage("../resources/WizardForm_fruitScaleHuge.png");
        this.fruitScaleHuge = new SpeedButton("huge", new ImageIcon(fruitScaleHugeImage));
        this.fruitScaleHuge.setBounds(509, 93, 40, 60);
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleHuge.Layout = blGlyphTop;
        //  --------------- UNHANDLED ATTRIBUTE: this.fruitScaleHuge.GroupIndex = 22;
        
        this.fruitColorLabel = new JLabel(" What color should fruits be drawn?");
        this.fruitColorLabel.setBounds(326, 187, 174, 14);
        
        Image arrowFruitColorImage = toolkit.createImage("../resources/WizardForm_arrowFruitColor.png");
        this.arrowFruitColor = new ImagePanel(new ImageIcon(arrowFruitColorImage));
        this.arrowFruitColor.setBounds(316, 185, 8, 16);
        
        this.fruitColorExplainLabel = new JLabel("Click in the square to change the color.");
        this.fruitColorExplainLabel.setBounds(374, 227, 187, 14);
        
        Image arrowShowFruitsImage = toolkit.createImage("../resources/WizardForm_arrowShowFruits.png");
        this.arrowShowFruits = new ImagePanel(new ImageIcon(arrowShowFruitsImage));
        this.arrowShowFruits.setBounds(12, 53, 8, 16);
        
        this.showFruitsLabel = new JLabel("Do you want to see fruits on your plant?");
        this.showFruitsLabel.setBounds(24, 55, 195, 14);
        
        this.Label10 = new JLabel("Fruits are drawn like flowers, but with a portion of the fruit (a \"fruit section\") rotated around instead of a petal. For many plants you will not be interested in the fruit, so you can turn fruits off entirely.");
        this.Label10.setBounds(12, 22, 496, 28);
        
        this.sectionTdoSelectedLabel = new JLabel("sectionTdoSelectedLabel");
        this.sectionTdoSelectedLabel.setBounds(24, 166, 121, 14);
        
        this.sectionTdosDraw = new JTable(new DefaultTableModel());
        this.sectionTdosDraw.setBounds(24, 93, 250, 69);
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.OnDrawCell = sectionTdosDrawDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.RowCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.FixedRows = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.DefaultColWidth = 40;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.ColCount = 20;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.DefaultRowHeight = 50;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.ScrollBars = ssHorizontal;
        this.sectionTdosDraw.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseMoved(java.awt.event.MouseEvent event) {
                sectionTdosDrawMouseMove(event);
            }
        });
        this.sectionTdosDraw.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent event) {
                sectionTdosDrawMouseMove(event);
            }
        });
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.FixedCols = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.OnSelectCell = sectionTdosDrawSelectCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.sectionTdosDraw.Options = [goVertLine, goHorzLine];
        
        this.fruitColor = new JPanel(null);
        // -- this.fruitColor.setLayout(new BoxLayout(this.fruitColor, BoxLayout.Y_AXIS));
        this.fruitColor.setBounds(328, 213, 41, 41);
        this.fruitColor.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                fruitColorMouseUp(event);
            }
        });
        
        this.showFruitsYes = new JRadioButton("yes");
        this.showFruitsYes.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                showFruitsYesClick(event);
            }
        });
        // ----- manually fix radio button group by putting multiple buttons in the same group
        ButtonGroup group = new ButtonGroup();
        group.add(this.showFruitsYes);
        this.showFruitsYes.setBounds(226, 53, 53, 17);
        
        this.showFruitsNo = new JRadioButton("no");
        this.showFruitsNo.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                showFruitsNoClick(event);
            }
        });
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.showFruitsNo);
        this.showFruitsNo.setBounds(270, 53, 45, 17);
        
        this.page9.add(fruitTdoLabel);
        this.page9.add(fruitSectionsNumberLabel);
        this.page9.add(fruitScaleLabel);
        this.page9.add(panelFruitsLabel);
        this.page9.add(arrowFruitTdo);
        this.page9.add(arrowFruitSectionsNumber);
        this.page9.add(arrowFruitScale);
        this.page9.add(fruitSectionsOne);
        this.page9.add(fruitSectionsThree);
        this.page9.add(fruitSectionsFour);
        this.page9.add(fruitSectionsFive);
        this.page9.add(fruitSectionsTen);
        this.page9.add(fruitScaleTiny);
        this.page9.add(fruitScaleSmall);
        this.page9.add(fruitScaleMedium);
        this.page9.add(fruitScaleLarge);
        this.page9.add(fruitScaleHuge);
        this.page9.add(fruitColorLabel);
        this.page9.add(arrowFruitColor);
        this.page9.add(fruitColorExplainLabel);
        this.page9.add(arrowShowFruits);
        this.page9.add(showFruitsLabel);
        this.page9.add(Label10);
        this.page9.add(sectionTdoSelectedLabel);
        this.page9.add(sectionTdosDraw);
        this.page9.add(fruitColor);
        this.page9.add(showFruitsYes);
        this.page9.add(showFruitsNo);
        this.wizardNotebook.addTab("Fruit", null, this.page9);
        
        
        this.page10 = new JPanel(null);
        this.finishLabelFirst = new JLabel("You have finished designing your new plant. You can name your new plant here, or just keep this name.");
        this.finishLabelFirst.setBounds(12, 46, 263, 28);
        
        this.finishLabelSecond = new JLabel("Now click Finish to place your plant in the main window, or click Cancel to stop without creating a plant, or click Back to change your choices.");
        this.finishLabelSecond.setBounds(12, 107, 236, 42);
        
        this.finishLabelThird = new JLabel("Once your plant is made, you can fine-tune the parameters that define your plant in the Parameters panel in the main window. ");
        this.finishLabelThird.setBounds(12, 189, 229, 42);
        
        this.panelFinishLabel = new JLabel("Congratulations!");
        this.panelFinishLabel.setBounds(12, 20, 91, 14);
        
        this.previewLabel = new JLabel("Preview");
        this.previewLabel.setBounds(405, 6, 40, 14);
        
        Image turnLeftImage = toolkit.createImage("../resources/WizardForm_turnLeft.png");
        this.turnLeft = new SpeedButton(new ImageIcon(turnLeftImage));
        this.turnLeft.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                turnLeftClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.turnLeft.setBounds(444, 237, 25, 25);
        
        Image turnRightImage = toolkit.createImage("../resources/WizardForm_turnRight.png");
        this.turnRight = new SpeedButton(new ImageIcon(turnRightImage));
        this.turnRight.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                turnRightClick(event);
            }
        });
        // ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        this.turnRight.setBounds(469, 237, 25, 25);
        
        this.Label12 = new JLabel("You can also click on the pictures below to return to any of the wizard panels.");
        this.Label12.setBounds(12, 156, 243, 28);
        
        this.newPlantName = new JTextField("New plant");
        this.newPlantName.setBounds(12, 78, 237, 22);
        
        this.previewPanel = new JPanel(null);
        // -- this.previewPanel.setLayout(new BoxLayout(this.previewPanel, BoxLayout.Y_AXIS));
        this.previewPanel.setBounds(299, 22, 251, 213);
        
        this.randomizePlant = new JButton("Randomize");
        this.randomizePlant.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                randomizePlantClick(event);
            }
        });
        this.randomizePlant.setMnemonic(KeyEvent.VK_R);
        this.randomizePlant.setBounds(365, 237, 74, 25);
        
        this.page10.add(finishLabelFirst);
        this.page10.add(finishLabelSecond);
        this.page10.add(finishLabelThird);
        this.page10.add(panelFinishLabel);
        this.page10.add(previewLabel);
        this.page10.add(turnLeft);
        this.page10.add(turnRight);
        this.page10.add(Label12);
        this.page10.add(newPlantName);
        this.page10.add(previewPanel);
        this.page10.add(randomizePlant);
        this.wizardNotebook.addTab("Finish", null, this.page10);
        
        
        this.wizardNotebook.add(page1);
        this.wizardNotebook.add(page2);
        this.wizardNotebook.add(page3);
        this.wizardNotebook.add(page4);
        this.wizardNotebook.add(page5);
        this.wizardNotebook.add(page6);
        this.wizardNotebook.add(page7);
        this.wizardNotebook.add(page8);
        this.wizardNotebook.add(page9);
        this.wizardNotebook.add(page10);
        this.wizardNotebook.setBounds(0, 0, 569, 267);
        //  --------------- UNHANDLED ATTRIBUTE: this.wizardNotebook.PageIndex = 9;
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setMnemonic(KeyEvent.VK_C);
        this.cancel.setBounds(518, 276, 50, 21);
        
        this.back = new JButton("< Back");
        this.back.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                backClick(event);
            }
        });
        this.back.setMnemonic(KeyEvent.VK_B);
        this.back.setBounds(414, 276, 50, 21);
        
        this.next = new JButton("Next >");
        this.next.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                nextClick(event);
            }
        });
        this.next.setMnemonic(KeyEvent.VK_N);
        this.next.setBounds(466, 276, 50, 21);
        
        this.defaultChoices = new JButton("Defaults");
        this.defaultChoices.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                defaultChoicesClick(event);
            }
        });
        this.defaultChoices.setMnemonic(KeyEvent.VK_D);
        this.defaultChoices.setBounds(60, 276, 50, 21);
        
        Image startPageImageImage = toolkit.createImage("../resources/WizardForm_startPageImage.png");
        this.startPageImage = new ImagePanel(new ImageIcon(startPageImageImage));
        this.startPageImage.setBounds(12, 8, 20, 20);
        
        Image meristemsPageImageImage = toolkit.createImage("../resources/WizardForm_meristemsPageImage.png");
        this.meristemsPageImage = new ImagePanel(new ImageIcon(meristemsPageImageImage));
        this.meristemsPageImage.setBounds(36, 8, 20, 20);
        
        Image internodesPageImageImage = toolkit.createImage("../resources/WizardForm_internodesPageImage.png");
        this.internodesPageImage = new ImagePanel(new ImageIcon(internodesPageImageImage));
        this.internodesPageImage.setBounds(68, 8, 20, 20);
        
        Image leavesPageImageImage = toolkit.createImage("../resources/WizardForm_leavesPageImage.png");
        this.leavesPageImage = new ImagePanel(new ImageIcon(leavesPageImageImage));
        this.leavesPageImage.setBounds(100, 8, 20, 20);
        
        Image compoundLeavesPageImageImage = toolkit.createImage("../resources/WizardForm_compoundLeavesPageImage.png");
        this.compoundLeavesPageImage = new ImagePanel(new ImageIcon(compoundLeavesPageImageImage));
        this.compoundLeavesPageImage.setBounds(132, 8, 20, 20);
        
        Image flowersPageImageImage = toolkit.createImage("../resources/WizardForm_flowersPageImage.png");
        this.flowersPageImage = new ImagePanel(new ImageIcon(flowersPageImageImage));
        this.flowersPageImage.setBounds(220, 4, 20, 20);
        
        Image inflorDrawPageImageImage = toolkit.createImage("../resources/WizardForm_inflorDrawPageImage.png");
        this.inflorDrawPageImage = new ImagePanel(new ImageIcon(inflorDrawPageImageImage));
        this.inflorDrawPageImage.setBounds(192, 8, 20, 20);
        
        Image inflorPlacePageImageImage = toolkit.createImage("../resources/WizardForm_inflorPlacePageImage.png");
        this.inflorPlacePageImage = new ImagePanel(new ImageIcon(inflorPlacePageImageImage));
        this.inflorPlacePageImage.setBounds(168, 8, 20, 20);
        
        Image fruitsPageImageImage = toolkit.createImage("../resources/WizardForm_fruitsPageImage.png");
        this.fruitsPageImage = new ImagePanel(new ImageIcon(fruitsPageImageImage));
        this.fruitsPageImage.setBounds(248, 4, 20, 20);
        
        Image finishPageImageImage = toolkit.createImage("../resources/WizardForm_finishPageImage.png");
        this.finishPageImage = new ImagePanel(new ImageIcon(finishPageImageImage));
        this.finishPageImage.setBounds(276, 4, 20, 20);
        
        Image inflorDrawPageImageDisabledImage = toolkit.createImage("../resources/WizardForm_inflorDrawPageImageDisabled.png");
        this.inflorDrawPageImageDisabled = new ImagePanel(new ImageIcon(inflorDrawPageImageDisabledImage));
        this.inflorDrawPageImageDisabled.setBounds(188, 32, 20, 20);
        
        Image flowersPageImageDisabledImage = toolkit.createImage("../resources/WizardForm_flowersPageImageDisabled.png");
        this.flowersPageImageDisabled = new ImagePanel(new ImageIcon(flowersPageImageDisabledImage));
        this.flowersPageImageDisabled.setBounds(216, 32, 20, 20);
        
        Image fruitsPageImageDisabledImage = toolkit.createImage("../resources/WizardForm_fruitsPageImageDisabled.png");
        this.fruitsPageImageDisabled = new ImagePanel(new ImageIcon(fruitsPageImageDisabledImage));
        this.fruitsPageImageDisabled.setBounds(248, 32, 20, 20);
        
        this.hiddenPicturesPanel = new JPanel(null);
        // -- this.hiddenPicturesPanel.setLayout(new BoxLayout(this.hiddenPicturesPanel, BoxLayout.Y_AXIS));
        this.hiddenPicturesPanel.add(startPageImage);
        this.hiddenPicturesPanel.add(meristemsPageImage);
        this.hiddenPicturesPanel.add(internodesPageImage);
        this.hiddenPicturesPanel.add(leavesPageImage);
        this.hiddenPicturesPanel.add(compoundLeavesPageImage);
        this.hiddenPicturesPanel.add(flowersPageImage);
        this.hiddenPicturesPanel.add(inflorDrawPageImage);
        this.hiddenPicturesPanel.add(inflorPlacePageImage);
        this.hiddenPicturesPanel.add(fruitsPageImage);
        this.hiddenPicturesPanel.add(finishPageImage);
        this.hiddenPicturesPanel.add(inflorDrawPageImageDisabled);
        this.hiddenPicturesPanel.add(flowersPageImageDisabled);
        this.hiddenPicturesPanel.add(fruitsPageImageDisabled);
        this.hiddenPicturesPanel.setBounds(18, 406, 325, 57);
        this.hiddenPicturesPanel.setVisible(false);
        
        this.progressDrawGrid = new JTable(new DefaultTableModel());
        this.progressDrawGrid.setBounds(190, 276, 220, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.ColCount = 10;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.BorderStyle = bsNone;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.OnDrawCell = progressDrawGridDrawCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.DefaultDrawing = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.TabStop = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.GridLineWidth = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.DefaultRowHeight = 20;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.OnSelectCell = progressDrawGridSelectCell;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.FixedRows = 0;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.ScrollBars = ssNone;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.Options = [goFixedVertLine, goFixedHorzLine, goHorzLine];
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.DefaultColWidth = 20;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.RowCount = 1;
        //  --------------- UNHANDLED ATTRIBUTE: this.progressDrawGrid.FixedCols = 0;
        
        delphiPanel.add(helpButton);
        delphiPanel.add(changeTdoLibrary);
        delphiPanel.add(wizardNotebook);
        delphiPanel.add(cancel);
        delphiPanel.add(back);
        delphiPanel.add(next);
        delphiPanel.add(defaultChoices);
        delphiPanel.add(hiddenPicturesPanel);
        delphiPanel.add(progressDrawGrid);
        return delphiPanel;
    }
    
        
    public void FormKeyPress(KeyEvent event) {
        System.out.println("FormKeyPress");
    }
        
    public void apicalInflorsFiveClick(ActionEvent event) {
        System.out.println("apicalInflorsFiveClick");
    }
        
    public void apicalInflorsNoneClick(ActionEvent event) {
        System.out.println("apicalInflorsNoneClick");
    }
        
    public void apicalInflorsOneClick(ActionEvent event) {
        System.out.println("apicalInflorsOneClick");
    }
        
    public void apicalInflorsThreeClick(ActionEvent event) {
        System.out.println("apicalInflorsThreeClick");
    }
        
    public void apicalInflorsTwoClick(ActionEvent event) {
        System.out.println("apicalInflorsTwoClick");
    }
        
    public void axillaryInflorsFiveClick(ActionEvent event) {
        System.out.println("axillaryInflorsFiveClick");
    }
        
    public void axillaryInflorsNoneClick(ActionEvent event) {
        System.out.println("axillaryInflorsNoneClick");
    }
        
    public void axillaryInflorsTenClick(ActionEvent event) {
        System.out.println("axillaryInflorsTenClick");
    }
        
    public void axillaryInflorsThreeClick(ActionEvent event) {
        System.out.println("axillaryInflorsThreeClick");
    }
        
    public void axillaryInflorsTwentyClick(ActionEvent event) {
        System.out.println("axillaryInflorsTwentyClick");
    }
        
    public void backClick(ActionEvent event) {
        System.out.println("backClick");
    }
        
    public void branchLittleClick(ActionEvent event) {
        System.out.println("branchLittleClick");
    }
        
    public void branchLotClick(ActionEvent event) {
        System.out.println("branchLotClick");
    }
        
    public void branchMediumClick(ActionEvent event) {
        System.out.println("branchMediumClick");
    }
        
    public void branchNoneClick(ActionEvent event) {
        System.out.println("branchNoneClick");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void changeTdoLibraryClick(ActionEvent event) {
        System.out.println("changeTdoLibraryClick");
    }
        
    public void defaultChoicesClick(ActionEvent event) {
        System.out.println("defaultChoicesClick");
    }
        
    public void fruitColorMouseUp(MouseEvent event) {
        System.out.println("fruitColorMouseUp");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void inflorFlowersFiveClick(ActionEvent event) {
        System.out.println("inflorFlowersFiveClick");
    }
        
    public void inflorFlowersOneClick(ActionEvent event) {
        System.out.println("inflorFlowersOneClick");
    }
        
    public void inflorFlowersTenClick(ActionEvent event) {
        System.out.println("inflorFlowersTenClick");
    }
        
    public void inflorFlowersThreeClick(ActionEvent event) {
        System.out.println("inflorFlowersThreeClick");
    }
        
    public void inflorFlowersTwentyClick(ActionEvent event) {
        System.out.println("inflorFlowersTwentyClick");
    }
        
    public void inflorFlowersTwoClick(ActionEvent event) {
        System.out.println("inflorFlowersTwoClick");
    }
        
    public void leafletsFiveClick(ActionEvent event) {
        System.out.println("leafletsFiveClick");
    }
        
    public void leafletsFourClick(ActionEvent event) {
        System.out.println("leafletsFourClick");
    }
        
    public void leafletsOneClick(ActionEvent event) {
        System.out.println("leafletsOneClick");
    }
        
    public void leafletsSevenClick(ActionEvent event) {
        System.out.println("leafletsSevenClick");
    }
        
    public void leafletsThreeClick(ActionEvent event) {
        System.out.println("leafletsThreeClick");
    }
        
    public void nextClick(ActionEvent event) {
        System.out.println("nextClick");
    }
        
    public void petalColorMouseUp(MouseEvent event) {
        System.out.println("petalColorMouseUp");
    }
        
    public void randomizePlantClick(ActionEvent event) {
        System.out.println("randomizePlantClick");
    }
        
    public void sectionTdosDrawMouseMove(MouseEvent event) {
        System.out.println("sectionTdosDrawMouseMove");
    }
        
    public void showFruitsNoClick(ActionEvent event) {
        System.out.println("showFruitsNoClick");
    }
        
    public void showFruitsYesClick(ActionEvent event) {
        System.out.println("showFruitsYesClick");
    }
        
    public void turnLeftClick(ActionEvent event) {
        System.out.println("turnLeftClick");
    }
        
    public void turnRightClick(ActionEvent event) {
        System.out.println("turnRightClick");
    }
        
    public void wizardNotebookPageChanged(ChangeEvent event) {
        System.out.println("wizardNotebookPageChanged");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                WizardWindow thisClass = new WizardWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
