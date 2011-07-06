
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.table.*;
// import common.*;

public class BreedingOptionsWindow extends JFrame {
    private static final long serialVersionUID = 1L;
    ImagePanel upImage;
    ImagePanel downImage;
    SpeedButton helpButton;
    JButton ok;
    JButton cancel;
    JTabbedPane breedingOptions;
    JPanel page1;
    JPanel GroupBox1;
    JLabel Label4;
    JSpinner thumbnailWidth;
    JLabel Label1;
    JSpinner thumbnailHeight;
    JLabel Label2;
    JPanel GroupBox2;
    JSpinner plantsPerGeneration;
    JLabel Label3;
    JSpinner maxGenerations;
    JLabel Label6;
    JSpinner percentMaxAge;
    JLabel Label7;
    JSpinner maxPartsPerPlant_thousands;
    JLabel Label9;
    JLabel Label8;
    JPanel GroupBox3;
    JSpinner numTimeSeriesStages;
    JLabel Label5;
    JCheckBox updateTimeSeriesPlantsOnParameterChange;
    JPanel page2;
    JLabel mutationAmountLabel;
    JLabel mutationZero;
    JLabel mutationOneHundred;
    SpeedButton mutationShowSections;
    JSlider mutationSlider;
    JLabel mutationLabel;
    JList mutationSections;
    JButton mutationSelectAll;
    JButton mutationSelectNone;
    JPanel page3;
    JLabel weightAmountLabel;
    JLabel weightZero;
    JLabel weightOneHundred;
    SpeedButton weightShowSections;
    JSlider weightSlider;
    JLabel weightLabel;
    JButton weightSelectAll;
    JButton weightSelectNone;
    JList weightSections;
    JPanel page4;
    JLabel nonNumericLabel;
    JLabel firstPlantIfEqualLabel;
    JRadioButton alwaysCopyFromFirstPlant;
    JRadioButton alwaysCopyFromSecondPlant;
    JRadioButton copyRandomlyBasedOnWeights;
    JRadioButton copyBasedOnWeightsIfEqualFirstPlant;
    JRadioButton copyBasedOnWeightsIfEqualSecondPlant;
    JRadioButton copyBasedOnWeightsIfEqualChooseRandomly;
    JPanel page5;
    SpeedButton changeTdoLibrary;
    JCheckBox treatColorsAsNumbers;
    JCheckBox chooseTdosRandomly;
    JTextField currentTdoLibraryFileName;
    public JPanel mainContentPane;
    public JPanel delphiPanel;
    
    public BreedingOptionsWindow() {
        super();
        this.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE); // HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        initialize();
    }
    
    private void initialize() {
        this.setSize(new Dimension(705, 325));
        this.setContentPane(getMainContentPane());
        this.setTitle("Breeding and Time Series Options");
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
        this.setBounds(320, 263, 418, 330  + 80); // extra for title bar and menu
        //  --------------- UNHANDLED ATTRIBUTE: this.TextHeight = 14;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderIcons = [biSystemMenu];
        //  --------------- UNHANDLED ATTRIBUTE: this.Scaled = False;
        //  --------------- UNHANDLED ATTRIBUTE: this.PixelsPerInch = 96;
        //  --------------- UNHANDLED ATTRIBUTE: this.Position = poScreenCenter;
        //  --------------- UNHANDLED ATTRIBUTE: this.BorderStyle = bsDialog;
        //  --------------- UNHANDLED ATTRIBUTE: this.OnCreate = FormCreate;
        
        
        Image upImageImage = toolkit.createImage("../resources/BreedingOptionsForm_upImage.png");
        this.upImage = new ImagePanel(new ImageIcon(upImageImage));
        this.upImage.setBounds(452, 116, 16, 16);
        this.upImage.setVisible(false);
        
        Image downImageImage = toolkit.createImage("../resources/BreedingOptionsForm_downImage.png");
        this.downImage = new ImagePanel(new ImageIcon(downImageImage));
        this.downImage.setBounds(452, 92, 16, 16);
        this.downImage.setVisible(false);
        
        Image helpButtonImage = toolkit.createImage("../resources/BreedingOptionsForm_helpButton.png");
        this.helpButton = new SpeedButton("Help", new ImageIcon(helpButtonImage));
        this.helpButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                helpButtonClick(event);
            }
        });
        this.helpButton.setMnemonic(KeyEvent.VK_H);
        this.helpButton.setBounds(356, 63, 60, 25);
        
        this.ok = new JButton("OK");
        this.ok.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                okClick(event);
            }
        });
        this.getRootPane().setDefaultButton(this.ok);
        this.ok.setBounds(356, 4, 60, 21);
        
        this.cancel = new JButton("Cancel");
        this.cancel.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                cancelClick(event);
            }
        });
        this.cancel.setBounds(356, 27, 60, 21);
        //  --------------- UNHANDLED ATTRIBUTE: this.cancel.Cancel = True;
        
        this.breedingOptions = new JTabbedPane();
        
        this.page1 = new JPanel(null);
        this.Label4 = new JLabel("Size of plant thumbnails");
        this.Label4.setBounds(10, 19, 114, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.thumbnailWidth = new JSpinner(SpinnerNumberModel(30, 30, 200, 5));
        this.thumbnailWidth.setBounds(29, 39, 53, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.thumbnailWidth.OnChange = thumbnailWidthChange;
        
        this.Label1 = new JLabel("width (30-200)", displayedMnemonic=KeyEvent.VK_W, labelFor=this.thumbnailWidth);
        this.Label1.setBounds(89, 43, 72, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.thumbnailHeight = new JSpinner(SpinnerNumberModel(30, 30, 200, 5));
        this.thumbnailHeight.setBounds(171, 39, 53, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.thumbnailHeight.OnChange = thumbnailHeightChange;
        
        this.Label2 = new JLabel("height (30-200)", displayedMnemonic=KeyEvent.VK_H, labelFor=this.thumbnailHeight);
        this.Label2.setBounds(231, 43, 74, 14);
        
        this.GroupBox1 = new JPanel(null);
        // -- this.GroupBox1.setLayout(new BoxLayout(this.GroupBox1, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox1.border = new TitledBorder("" Breeder and time series window "");
        this.GroupBox1.add(Label4);
        this.GroupBox1.add(thumbnailWidth);
        this.GroupBox1.add(Label1);
        this.GroupBox1.add(thumbnailHeight);
        this.GroupBox1.add(Label2);
        this.GroupBox1.setBounds(4, 4, 334, 71);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.plantsPerGeneration = new JSpinner(SpinnerNumberModel(5, 1, 100, 1));
        this.plantsPerGeneration.setBounds(10, 20, 51, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.plantsPerGeneration.OnChange = plantsPerGenerationChange;
        
        this.Label3 = new JLabel("Plants to create per generation (1-100)", displayedMnemonic=KeyEvent.VK_C, labelFor=this.plantsPerGeneration);
        this.Label3.setBounds(68, 24, 187, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.maxGenerations = new JSpinner(SpinnerNumberModel(50, 20, 500, 10));
        this.maxGenerations.setBounds(10, 49, 51, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.maxGenerations.OnChange = maxGenerationsChange;
        
        this.Label6 = new JLabel("Maximum breeder generations (20-500)", displayedMnemonic=KeyEvent.VK_M, labelFor=this.maxGenerations);
        this.Label6.setBounds(68, 53, 190, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.percentMaxAge = new JSpinner(SpinnerNumberModel(100, 1, 100, 1));
        this.percentMaxAge.setBounds(10, 83, 51, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.percentMaxAge.OnChange = percentMaxAgeChange;
        
        this.Label7 = new JLabel("Age of breeder plants (as % of maximum)", displayedMnemonic=KeyEvent.VK_A, labelFor=this.percentMaxAge);
        this.Label7.setBounds(68, 87, 202, 14);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.maxPartsPerPlant_thousands = new JSpinner(SpinnerNumberModel(1, 1, 100, 1));
        this.maxPartsPerPlant_thousands.setBounds(10, 113, 51, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.maxPartsPerPlant_thousands.OnChange = maxPartsPerPlant_thousandsChange;
        
        this.Label9 = new JLabel("Maximum parts per breeder plant (1-100 thousand)", displayedMnemonic=KeyEvent.VK_X, labelFor=this.maxPartsPerPlant_thousands);
        this.Label9.setBounds(68, 117, 245, 14);
        
        this.Label8 = new JLabel("(to avoid running out of memory)", labelFor=this.maxGenerations);
        this.Label8.setBounds(79, 67, 157, 14);
        
        this.GroupBox2 = new JPanel(null);
        // -- this.GroupBox2.setLayout(new BoxLayout(this.GroupBox2, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox2.border = new TitledBorder("" Breeder "");
        this.GroupBox2.add(plantsPerGeneration);
        this.GroupBox2.add(Label3);
        this.GroupBox2.add(maxGenerations);
        this.GroupBox2.add(Label6);
        this.GroupBox2.add(percentMaxAge);
        this.GroupBox2.add(Label7);
        this.GroupBox2.add(maxPartsPerPlant_thousands);
        this.GroupBox2.add(Label9);
        this.GroupBox2.add(Label8);
        this.GroupBox2.setBounds(4, 78, 334, 144);
        
        // -- supposed to be a spin edit, not yet fuly implemented
        this.numTimeSeriesStages = new JSpinner(SpinnerNumberModel(5, 1, 100, 1));
        this.numTimeSeriesStages.setBounds(10, 17, 51, 23);
        //  --------------- UNHANDLED ATTRIBUTE: this.numTimeSeriesStages.OnChange = numTimeSeriesStagesChange;
        
        this.Label5 = new JLabel("Stages to show (1-100)", displayedMnemonic=KeyEvent.VK_S, labelFor=this.numTimeSeriesStages);
        this.Label5.setBounds(68, 22, 116, 14);
        
        this.updateTimeSeriesPlantsOnParameterChange = new JCheckBox("Update time series when change plant parameter");
        this.updateTimeSeriesPlantsOnParameterChange.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                updateTimeSeriesPlantsOnParameterChangeClick(event);
            }
        });
        this.updateTimeSeriesPlantsOnParameterChange.setMnemonic(KeyEvent.VK_T);
        this.updateTimeSeriesPlantsOnParameterChange.setBounds(10, 46, 267, 17);
        
        this.GroupBox3 = new JPanel(null);
        // -- this.GroupBox3.setLayout(new BoxLayout(this.GroupBox3, BoxLayout.Y_AXIS));
        // -- supposed to be group box
        this.GroupBox3.border = new TitledBorder("" Time series "");
        this.GroupBox3.add(numTimeSeriesStages);
        this.GroupBox3.add(Label5);
        this.GroupBox3.add(updateTimeSeriesPlantsOnParameterChange);
        this.GroupBox3.setBounds(4, 226, 334, 69);
        
        this.page1.add(GroupBox1);
        this.page1.add(GroupBox2);
        this.page1.add(GroupBox3);
        this.breedingOptions.addTab("General", null, this.page1);
        
        
        this.page2 = new JPanel(null);
        this.mutationAmountLabel = new JLabel("50%");
        this.mutationAmountLabel.setBounds(8, 32, 22, 14);
        
        this.mutationZero = new JLabel("0");
        this.mutationZero.setBounds(48, 32, 6, 14);
        
        this.mutationOneHundred = new JLabel("100");
        this.mutationOneHundred.setBounds(294, 32, 18, 14);
        
        Image mutationShowSectionsImage = toolkit.createImage("../resources/BreedingOptionsForm_mutationShowSections.png");
        this.mutationShowSections = new SpeedButton("Sections", new ImageIcon(mutationShowSectionsImage));
        this.mutationShowSections.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                mutationShowSectionsClick(event);
            }
        });
        this.mutationShowSections.setMnemonic(KeyEvent.VK_S);
        this.mutationShowSections.setBounds(10, 58, 79, 24);
        
        this.mutationSlider = new JSlider();
        this.mutationSlider.setBounds(60, 32, 233, 13);
        //  --------------- UNHANDLED ATTRIBUTE: this.mutationSlider.CurrentValue = 0;
        this.mutationSlider.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseMoved(java.awt.event.MouseEvent event) {
                mutationSliderMouseMove(event);
            }
        });
        this.mutationSlider.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent event) {
                mutationSliderMouseMove(event);
            }
        });
        this.mutationSlider.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                mutationSliderMouseUp(event);
            }
        });
        this.mutationSlider.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyReleased(java.awt.event.KeyEvent event) {
                mutationSliderKeyUp(event);
            }
        });
        this.mutationSlider.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                mutationSliderMouseDown(event);
            }
        });
        
        this.mutationLabel = new JLabel("Mutation strength (as percent of mean values)", displayedMnemonic=KeyEvent.VK_M, labelFor=this.mutationSlider);
        this.mutationLabel.setBounds(8, 12, 223, 14);
        
        this.mutationSections = new JList(new DefaultListModel());
        this.mutationSections.setFixedCellHeight(16);
        this.mutationSections.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                mutationSectionsClick(event);
            }
        });
        this.mutationSections.setBounds(95, 58, 230, 240);
        //  --------------- UNHANDLED ATTRIBUTE: this.mutationSections.Style = lbOwnerDrawFixed;
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("General: 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Meristems: 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Internodes: 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Leaves: 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("First leaves: 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Flowers (F): 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Flowers (M): 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Inflorescences (F): 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Inflorescences (M): 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Fruit: 50%");
        ((DefaultComboBoxModel)this.mutationSections.getModel()).addElement("Root top: 50%");
        //  --------------- UNHANDLED ATTRIBUTE: this.mutationSections.MultiSelect = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.mutationSections.OnDrawItem = mutationSectionsDrawItem;
        
        this.mutationSelectAll = new JButton("Select all");
        this.mutationSelectAll.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                mutationSelectAllClick(event);
            }
        });
        this.mutationSelectAll.setMnemonic(KeyEvent.VK_A);
        this.mutationSelectAll.setBounds(10, 94, 80, 24);
        
        this.mutationSelectNone = new JButton("Select none");
        this.mutationSelectNone.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                mutationSelectNoneClick(event);
            }
        });
        this.mutationSelectNone.setMnemonic(KeyEvent.VK_N);
        this.mutationSelectNone.setBounds(10, 122, 80, 24);
        
        this.page2.add(mutationAmountLabel);
        this.page2.add(mutationZero);
        this.page2.add(mutationOneHundred);
        this.page2.add(mutationShowSections);
        this.page2.add(mutationSlider);
        this.page2.add(mutationLabel);
        JScrollPane scroller1 = new JScrollPane();
        scroller1.setBounds(95, 58, 230, 240);;
        scroller1.setViewportView(mutationSections);
        this.page2.add(scroller1);
        this.page2.add(mutationSelectAll);
        this.page2.add(mutationSelectNone);
        this.breedingOptions.addTab("Mutation", null, this.page2);
        
        
        this.page3 = new JPanel(null);
        this.weightAmountLabel = new JLabel("50%");
        this.weightAmountLabel.setBounds(11, 32, 22, 14);
        
        this.weightZero = new JLabel("0");
        this.weightZero.setBounds(46, 32, 6, 14);
        
        this.weightOneHundred = new JLabel("100");
        this.weightOneHundred.setBounds(290, 32, 18, 14);
        
        Image weightShowSectionsImage = toolkit.createImage("../resources/BreedingOptionsForm_weightShowSections.png");
        this.weightShowSections = new SpeedButton("Sections", new ImageIcon(weightShowSectionsImage));
        this.weightShowSections.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                weightShowSectionsClick(event);
            }
        });
        this.weightShowSections.setMnemonic(KeyEvent.VK_S);
        this.weightShowSections.setBounds(10, 59, 81, 24);
        
        this.weightSlider = new JSlider();
        this.weightSlider.setBounds(56, 35, 229, 9);
        //  --------------- UNHANDLED ATTRIBUTE: this.weightSlider.CurrentValue = 0;
        this.weightSlider.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseMoved(java.awt.event.MouseEvent event) {
                weightSliderMouseMove(event);
            }
        });
        this.weightSlider.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseDragged(java.awt.event.MouseEvent event) {
                weightSliderMouseMove(event);
            }
        });
        this.weightSlider.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseReleased(java.awt.event.MouseEvent event) {
                weightSliderMouseUp(event);
            }
        });
        this.weightSlider.addKeyListener(new java.awt.event.KeyAdapter() {
            public void keyReleased(java.awt.event.KeyEvent event) {
                weightSliderKeyUp(event);
            }
        });
        this.weightSlider.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent event) {
                weightSliderMouseDown(event);
            }
        });
        
        this.weightLabel = new JLabel("Relative weight of first parent", displayedMnemonic=KeyEvent.VK_W, labelFor=this.weightSlider);
        this.weightLabel.setBounds(9, 12, 143, 14);
        
        this.weightSelectAll = new JButton("Select all");
        this.weightSelectAll.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                weightSelectAllClick(event);
            }
        });
        this.weightSelectAll.setMnemonic(KeyEvent.VK_A);
        this.weightSelectAll.setBounds(10, 95, 80, 24);
        
        this.weightSelectNone = new JButton("Select none");
        this.weightSelectNone.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                weightSelectNoneClick(event);
            }
        });
        this.weightSelectNone.setMnemonic(KeyEvent.VK_N);
        this.weightSelectNone.setBounds(10, 123, 80, 24);
        
        this.weightSections = new JList(new DefaultListModel());
        this.weightSections.setFixedCellHeight(16);
        this.weightSections.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseClicked(java.awt.event.MouseEvent event) {
                weightSectionsClick(event);
            }
        });
        this.weightSections.setBounds(95, 59, 230, 240);
        //  --------------- UNHANDLED ATTRIBUTE: this.weightSections.Style = lbOwnerDrawFixed;
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("General: 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Meristems: 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Internodes: 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Leaves: 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("First leaves: 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Flowers (F): 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Flowers (M): 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Inflorescences (F): 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Inflorescences (M): 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Fruit: 50%");
        ((DefaultComboBoxModel)this.weightSections.getModel()).addElement("Root top: 50%");
        //  --------------- UNHANDLED ATTRIBUTE: this.weightSections.MultiSelect = True;
        //  --------------- UNHANDLED ATTRIBUTE: this.weightSections.OnDrawItem = weightSectionsDrawItem;
        
        this.page3.add(weightAmountLabel);
        this.page3.add(weightZero);
        this.page3.add(weightOneHundred);
        this.page3.add(weightShowSections);
        this.page3.add(weightSlider);
        this.page3.add(weightLabel);
        this.page3.add(weightSelectAll);
        this.page3.add(weightSelectNone);
        JScrollPane scroller2 = new JScrollPane();
        scroller2.setBounds(95, 59, 230, 240);;
        scroller2.setViewportView(weightSections);
        this.page3.add(scroller2);
        this.breedingOptions.addTab("Blending", null, this.page3);
        
        
        this.page4 = new JPanel(null);
        this.nonNumericLabel = new JLabel(" Where to get non-numeric parameters");
        this.nonNumericLabel.setBounds(17, 31, 186, 14);
        
        this.firstPlantIfEqualLabel = new JLabel("get from parent with higher weight; if 50/50,");
        this.firstPlantIfEqualLabel.setBounds(29, 117, 212, 14);
        
        this.alwaysCopyFromFirstPlant = new JRadioButton("get from first parent");
        this.alwaysCopyFromFirstPlant.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                alwaysCopyFromFirstPlantClick(event);
            }
        });
        this.alwaysCopyFromFirstPlant.setMnemonic(KeyEvent.VK_F);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        ButtonGroup group = new ButtonGroup();
        group.add(this.alwaysCopyFromFirstPlant);
        this.alwaysCopyFromFirstPlant.setBounds(29, 51, 168, 17);
        
        this.alwaysCopyFromSecondPlant = new JRadioButton("get from second parent");
        this.alwaysCopyFromSecondPlant.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                alwaysCopyFromSecondPlantClick(event);
            }
        });
        this.alwaysCopyFromSecondPlant.setMnemonic(KeyEvent.VK_S);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.alwaysCopyFromSecondPlant);
        this.alwaysCopyFromSecondPlant.setBounds(29, 73, 194, 17);
        
        this.copyRandomlyBasedOnWeights = new JRadioButton("choose randomly using weights as probabilities");
        this.copyRandomlyBasedOnWeights.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyRandomlyBasedOnWeightsClick(event);
            }
        });
        this.copyRandomlyBasedOnWeights.setMnemonic(KeyEvent.VK_W);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.copyRandomlyBasedOnWeights);
        this.copyRandomlyBasedOnWeights.setBounds(29, 95, 258, 17);
        this.copyRandomlyBasedOnWeights.putClientProperty("tag", 1);
        
        this.copyBasedOnWeightsIfEqualFirstPlant = new JRadioButton("get from the first parent");
        this.copyBasedOnWeightsIfEqualFirstPlant.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyBasedOnWeightsIfEqualFirstPlantClick(event);
            }
        });
        this.copyBasedOnWeightsIfEqualFirstPlant.setMnemonic(KeyEvent.VK_I);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.copyBasedOnWeightsIfEqualFirstPlant);
        this.copyBasedOnWeightsIfEqualFirstPlant.setBounds(49, 139, 237, 17);
        
        this.copyBasedOnWeightsIfEqualSecondPlant = new JRadioButton("get from the second parent");
        this.copyBasedOnWeightsIfEqualSecondPlant.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyBasedOnWeightsIfEqualSecondPlantClick(event);
            }
        });
        this.copyBasedOnWeightsIfEqualSecondPlant.setMnemonic(KeyEvent.VK_E);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.copyBasedOnWeightsIfEqualSecondPlant);
        this.copyBasedOnWeightsIfEqualSecondPlant.setBounds(49, 161, 237, 17);
        
        this.copyBasedOnWeightsIfEqualChooseRandomly = new JRadioButton("choose randomly");
        this.copyBasedOnWeightsIfEqualChooseRandomly.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                copyBasedOnWeightsIfEqualChooseRandomlyClick(event);
            }
        });
        this.copyBasedOnWeightsIfEqualChooseRandomly.setMnemonic(KeyEvent.VK_R);
        // ----- manually fix radio button group by putting multiple buttons in the same group
        group.add(this.copyBasedOnWeightsIfEqualChooseRandomly);
        this.copyBasedOnWeightsIfEqualChooseRandomly.setBounds(49, 183, 237, 17);
        
        this.page4.add(nonNumericLabel);
        this.page4.add(firstPlantIfEqualLabel);
        this.page4.add(alwaysCopyFromFirstPlant);
        this.page4.add(alwaysCopyFromSecondPlant);
        this.page4.add(copyRandomlyBasedOnWeights);
        this.page4.add(copyBasedOnWeightsIfEqualFirstPlant);
        this.page4.add(copyBasedOnWeightsIfEqualSecondPlant);
        this.page4.add(copyBasedOnWeightsIfEqualChooseRandomly);
        this.breedingOptions.addTab("Non-numeric", null, this.page4);
        
        
        this.page5 = new JPanel(null);
        Image changeTdoLibraryImage = toolkit.createImage("../resources/BreedingOptionsForm_changeTdoLibrary.png");
        this.changeTdoLibrary = new SpeedButton("Change...", new ImageIcon(changeTdoLibraryImage));
        this.changeTdoLibrary.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                changeTdoLibraryClick(event);
            }
        });
        this.changeTdoLibrary.setMnemonic(KeyEvent.VK_C);
        this.changeTdoLibrary.setBounds(257, 80, 84, 24);
        
        this.treatColorsAsNumbers = new JCheckBox("mutate and blend colors as numbers");
        this.treatColorsAsNumbers.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                treatColorsAsNumbersClick(event);
            }
        });
        this.treatColorsAsNumbers.setMnemonic(KeyEvent.VK_C);
        this.treatColorsAsNumbers.setBounds(15, 31, 218, 17);
        
        this.chooseTdosRandomly = new JCheckBox("choose 3D objects randomly from current library");
        this.chooseTdosRandomly.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent event) {
                chooseTdosRandomlyClick(event);
            }
        });
        this.chooseTdosRandomly.setMnemonic(KeyEvent.VK_O);
        this.chooseTdosRandomly.setBounds(15, 61, 258, 17);
        
        this.currentTdoLibraryFileName = new JTextField("currentTdoLibraryFileName");
        this.currentTdoLibraryFileName.setEditable(false);
        this.currentTdoLibraryFileName.setBounds(34, 83, 217, 22);
        
        this.page5.add(changeTdoLibrary);
        this.page5.add(treatColorsAsNumbers);
        this.page5.add(chooseTdosRandomly);
        this.page5.add(currentTdoLibraryFileName);
        this.breedingOptions.addTab("Colors and 3D objects", null, this.page5);
        
        
        this.breedingOptions.add(page1);
        this.breedingOptions.add(page2);
        this.breedingOptions.add(page3);
        this.breedingOptions.add(page4);
        this.breedingOptions.add(page5);
        this.breedingOptions.setBounds(0, 0, 351, 330);
        //  --------------- UNHANDLED ATTRIBUTE: this.breedingOptions.TabFont.Style = [];
        //  --------------- UNHANDLED ATTRIBUTE: this.breedingOptions.TabFont.Color = clBlack;
        //  --------------- UNHANDLED ATTRIBUTE: this.breedingOptions.TabFont.Charset = DEFAULT_CHARSET;
        //  --------------- UNHANDLED ATTRIBUTE: this.breedingOptions.TabFont.Name = 'Arial';
        //  --------------- UNHANDLED ATTRIBUTE: this.breedingOptions.TabFont.Height = -11;
        
        delphiPanel.add(upImage);
        delphiPanel.add(downImage);
        delphiPanel.add(helpButton);
        delphiPanel.add(ok);
        delphiPanel.add(cancel);
        delphiPanel.add(breedingOptions);
        return delphiPanel;
    }
    
        
    public void alwaysCopyFromFirstPlantClick(ActionEvent event) {
        System.out.println("alwaysCopyFromFirstPlantClick");
    }
        
    public void alwaysCopyFromSecondPlantClick(ActionEvent event) {
        System.out.println("alwaysCopyFromSecondPlantClick");
    }
        
    public void cancelClick(ActionEvent event) {
        System.out.println("cancelClick");
    }
        
    public void changeTdoLibraryClick(ActionEvent event) {
        System.out.println("changeTdoLibraryClick");
    }
        
    public void chooseTdosRandomlyClick(ActionEvent event) {
        System.out.println("chooseTdosRandomlyClick");
    }
        
    public void copyBasedOnWeightsIfEqualChooseRandomlyClick(ActionEvent event) {
        System.out.println("copyBasedOnWeightsIfEqualChooseRandomlyClick");
    }
        
    public void copyBasedOnWeightsIfEqualFirstPlantClick(ActionEvent event) {
        System.out.println("copyBasedOnWeightsIfEqualFirstPlantClick");
    }
        
    public void copyBasedOnWeightsIfEqualSecondPlantClick(ActionEvent event) {
        System.out.println("copyBasedOnWeightsIfEqualSecondPlantClick");
    }
        
    public void copyRandomlyBasedOnWeightsClick(ActionEvent event) {
        System.out.println("copyRandomlyBasedOnWeightsClick");
    }
        
    public void helpButtonClick(ActionEvent event) {
        System.out.println("helpButtonClick");
    }
        
    public void mutationSectionsClick(MouseEvent event) {
        System.out.println("mutationSectionsClick");
    }
        
    public void mutationSelectAllClick(ActionEvent event) {
        System.out.println("mutationSelectAllClick");
    }
        
    public void mutationSelectNoneClick(ActionEvent event) {
        System.out.println("mutationSelectNoneClick");
    }
        
    public void mutationShowSectionsClick(ActionEvent event) {
        System.out.println("mutationShowSectionsClick");
    }
        
    public void mutationSliderKeyUp(KeyEvent event) {
        System.out.println("mutationSliderKeyUp");
    }
        
    public void mutationSliderMouseDown(MouseEvent event) {
        System.out.println("mutationSliderMouseDown");
    }
        
    public void mutationSliderMouseMove(MouseEvent event) {
        System.out.println("mutationSliderMouseMove");
    }
        
    public void mutationSliderMouseUp(MouseEvent event) {
        System.out.println("mutationSliderMouseUp");
    }
        
    public void okClick(ActionEvent event) {
        System.out.println("okClick");
    }
        
    public void treatColorsAsNumbersClick(ActionEvent event) {
        System.out.println("treatColorsAsNumbersClick");
    }
        
    public void updateTimeSeriesPlantsOnParameterChangeClick(ActionEvent event) {
        System.out.println("updateTimeSeriesPlantsOnParameterChangeClick");
    }
        
    public void weightSectionsClick(MouseEvent event) {
        System.out.println("weightSectionsClick");
    }
        
    public void weightSelectAllClick(ActionEvent event) {
        System.out.println("weightSelectAllClick");
    }
        
    public void weightSelectNoneClick(ActionEvent event) {
        System.out.println("weightSelectNoneClick");
    }
        
    public void weightShowSectionsClick(ActionEvent event) {
        System.out.println("weightShowSectionsClick");
    }
        
    public void weightSliderKeyUp(KeyEvent event) {
        System.out.println("weightSliderKeyUp");
    }
        
    public void weightSliderMouseDown(MouseEvent event) {
        System.out.println("weightSliderMouseDown");
    }
        
    public void weightSliderMouseMove(MouseEvent event) {
        System.out.println("weightSliderMouseMove");
    }
        
    public void weightSliderMouseUp(MouseEvent event) {
        System.out.println("weightSliderMouseUp");
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                BreedingOptionsWindow thisClass = new BreedingOptionsWindow();
                thisClass.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
                thisClass.setVisible(true);
            }
        });
    }

}
