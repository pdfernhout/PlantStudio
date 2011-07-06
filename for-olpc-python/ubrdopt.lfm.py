from common import *

#Useage:
#        import BreedingOptionsWindow
#        window = BreedingOptionsWindow.BreedingOptionsWindow()
#        window.visible = 1

class BreedingOptionsWindow(JFrame):
    def __init__(self, title='Breeding and Time Series Options'):
        JFrame.__init__(self, title, windowClosing=self.OnClose)
        self.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE) # HIDE_ON_CLOSE DO_NOTHING_ON_CLOSE
        self.BuildWindow()
        
    def OnClose(self, event):
        print "Closed"
        
    # a menu is top item on the menu bar and can be pulled down for a list of menu items
    def createMenu(self, name, mnemonic=None, menuBar = None):
        menu = JMenu(name)
        if mnemonic:
            menu.setMnemonic(mnemonic)
        if menuBar:
            menuBar.add(menu)
        return menu
        
    def BuildWindow(self):
        toolkit = java.awt.Toolkit.getDefaultToolkit()
        contentPane = self.getContentPane()
        contentPane.setLayout(None)
        # -- contentPane.setLayout(BoxLayout(contentPane, BoxLayout.Y_AXIS))
        buttonFont = Font("Arial Narrow", Font.PLAIN, 9)
        buttonMargin = Insets(1, 1, 1, 1)
        self.setBounds(320, 263, 418, 330  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = [biSystemMenu]
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        
        self.upImageImage = toolkit.createImage("../resources/BreedingOptionsForm_upImage.png")
        self.upImage = ImagePanel(ImageIcon(self.upImageImage))
        self.upImage.setBounds(452, 116, 16, 16)
        self.upImage.visible = 0
        self.downImageImage = toolkit.createImage("../resources/BreedingOptionsForm_downImage.png")
        self.downImage = ImagePanel(ImageIcon(self.downImageImage))
        self.downImage.setBounds(452, 92, 16, 16)
        self.downImage.visible = 0
        self.helpButtonImage = toolkit.createImage("../resources/BreedingOptionsForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(356, 63, 60, 25)
        self.ok = JButton('OK', actionPerformed=self.okClick, font=buttonFont, margin=buttonMargin)
        self.getRootPane().setDefaultButton(self.ok)
        self.ok.setBounds(356, 4, 60, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setBounds(356, 27, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.breedingOptions = JTabbedPane()
        
        self.page1 = JPanel(layout=None)
        self.Label4 = JLabel('Size of plant thumbnails', font=buttonFont)
        self.Label4.setBounds(10, 19, 114, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.thumbnailWidth = JSpinner(SpinnerNumberModel(30, 30, 200, 5))
        self.thumbnailWidth.setBounds(29, 39, 53, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.thumbnailWidth.OnChange = thumbnailWidthChange
        self.Label1 = JLabel('width (30-200)', displayedMnemonic=KeyEvent.VK_W, labelFor=self.thumbnailWidth, font=buttonFont)
        self.Label1.setBounds(89, 43, 72, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.thumbnailHeight = JSpinner(SpinnerNumberModel(30, 30, 200, 5))
        self.thumbnailHeight.setBounds(171, 39, 53, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.thumbnailHeight.OnChange = thumbnailHeightChange
        self.Label2 = JLabel('height (30-200)', displayedMnemonic=KeyEvent.VK_H, labelFor=self.thumbnailHeight, font=buttonFont)
        self.Label2.setBounds(231, 43, 74, 14)
        self.GroupBox1 = JPanel(layout=None)
        # -- self.GroupBox1.setLayout(BoxLayout(self.GroupBox1, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox1.border = TitledBorder("' Breeder and time series window '")
        self.GroupBox1.add(self.Label4)
        self.GroupBox1.add(self.thumbnailWidth)
        self.GroupBox1.add(self.Label1)
        self.GroupBox1.add(self.thumbnailHeight)
        self.GroupBox1.add(self.Label2)
        self.GroupBox1.setBounds(4, 4, 334, 71)
        self.page1.add(self.GroupBox1)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.plantsPerGeneration = JSpinner(SpinnerNumberModel(5, 1, 100, 1))
        self.plantsPerGeneration.setBounds(10, 20, 51, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.plantsPerGeneration.OnChange = plantsPerGenerationChange
        self.Label3 = JLabel('Plants to create per generation (1-100)', displayedMnemonic=KeyEvent.VK_C, labelFor=self.plantsPerGeneration, font=buttonFont)
        self.Label3.setBounds(68, 24, 187, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.maxGenerations = JSpinner(SpinnerNumberModel(50, 20, 500, 10))
        self.maxGenerations.setBounds(10, 49, 51, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.maxGenerations.OnChange = maxGenerationsChange
        self.Label6 = JLabel('Maximum breeder generations (20-500)', displayedMnemonic=KeyEvent.VK_M, labelFor=self.maxGenerations, font=buttonFont)
        self.Label6.setBounds(68, 53, 190, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.percentMaxAge = JSpinner(SpinnerNumberModel(100, 1, 100, 1))
        self.percentMaxAge.setBounds(10, 83, 51, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.percentMaxAge.OnChange = percentMaxAgeChange
        self.Label7 = JLabel('Age of breeder plants (as % of maximum)', displayedMnemonic=KeyEvent.VK_A, labelFor=self.percentMaxAge, font=buttonFont)
        self.Label7.setBounds(68, 87, 202, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.maxPartsPerPlant_thousands = JSpinner(SpinnerNumberModel(1, 1, 100, 1))
        self.maxPartsPerPlant_thousands.setBounds(10, 113, 51, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.maxPartsPerPlant_thousands.OnChange = maxPartsPerPlant_thousandsChange
        self.Label9 = JLabel('Maximum parts per breeder plant (1-100 thousand)', displayedMnemonic=KeyEvent.VK_X, labelFor=self.maxPartsPerPlant_thousands, font=buttonFont)
        self.Label9.setBounds(68, 117, 245, 14)
        self.Label8 = JLabel('(to avoid running out of memory)', labelFor=self.maxGenerations, font=buttonFont)
        self.Label8.setBounds(79, 67, 157, 14)
        self.GroupBox2 = JPanel(layout=None)
        # -- self.GroupBox2.setLayout(BoxLayout(self.GroupBox2, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox2.border = TitledBorder("' Breeder '")
        self.GroupBox2.add(self.plantsPerGeneration)
        self.GroupBox2.add(self.Label3)
        self.GroupBox2.add(self.maxGenerations)
        self.GroupBox2.add(self.Label6)
        self.GroupBox2.add(self.percentMaxAge)
        self.GroupBox2.add(self.Label7)
        self.GroupBox2.add(self.maxPartsPerPlant_thousands)
        self.GroupBox2.add(self.Label9)
        self.GroupBox2.add(self.Label8)
        self.GroupBox2.setBounds(4, 78, 334, 144)
        self.page1.add(self.GroupBox2)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.numTimeSeriesStages = JSpinner(SpinnerNumberModel(5, 1, 100, 1))
        self.numTimeSeriesStages.setBounds(10, 17, 51, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.numTimeSeriesStages.OnChange = numTimeSeriesStagesChange
        self.Label5 = JLabel('Stages to show (1-100)', displayedMnemonic=KeyEvent.VK_S, labelFor=self.numTimeSeriesStages, font=buttonFont)
        self.Label5.setBounds(68, 22, 116, 14)
        self.updateTimeSeriesPlantsOnParameterChange = JCheckBox('Update time series when change plant parameter', actionPerformed=self.updateTimeSeriesPlantsOnParameterChangeClick, font=buttonFont, margin=buttonMargin)
        self.updateTimeSeriesPlantsOnParameterChange.setMnemonic(KeyEvent.VK_T)
        self.updateTimeSeriesPlantsOnParameterChange.setBounds(10, 46, 267, 17)
        self.GroupBox3 = JPanel(layout=None)
        # -- self.GroupBox3.setLayout(BoxLayout(self.GroupBox3, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox3.border = TitledBorder("' Time series '")
        self.GroupBox3.add(self.numTimeSeriesStages)
        self.GroupBox3.add(self.Label5)
        self.GroupBox3.add(self.updateTimeSeriesPlantsOnParameterChange)
        self.GroupBox3.setBounds(4, 226, 334, 69)
        self.page1.add(self.GroupBox3)
        self.breedingOptions.addTab('General', None, self.page1)
        
        self.page2 = JPanel(layout=None)
        self.mutationAmountLabel = JLabel('50%', font=buttonFont)
        self.mutationAmountLabel.setBounds(8, 32, 22, 14)
        self.page2.add(self.mutationAmountLabel)
        self.mutationZero = JLabel('0', font=buttonFont)
        self.mutationZero.setBounds(48, 32, 6, 14)
        self.page2.add(self.mutationZero)
        self.mutationOneHundred = JLabel('100', font=buttonFont)
        self.mutationOneHundred.setBounds(294, 32, 18, 14)
        self.page2.add(self.mutationOneHundred)
        self.mutationShowSectionsImage = toolkit.createImage("../resources/BreedingOptionsForm_mutationShowSections.png")
        self.mutationShowSections = SpeedButton('Sections', ImageIcon(self.mutationShowSectionsImage), actionPerformed=self.mutationShowSectionsClick, font=buttonFont, margin=buttonMargin)
        self.mutationShowSections.setMnemonic(KeyEvent.VK_S)
        self.mutationShowSections.setBounds(10, 58, 79, 24)
        self.page2.add(self.mutationShowSections)
        self.mutationSlider = JSlider()
        self.mutationSlider.setBounds(60, 32, 233, 13)
        #  --------------- UNHANDLED ATTRIBUTE: self.mutationSlider.CurrentValue = 0
        self.mutationSlider.mouseMoved = self.mutationSliderMouseMove
        self.mutationSlider.mouseDragged = self.mutationSliderMouseMove
        self.mutationSlider.mouseReleased = self.mutationSliderMouseUp
        self.mutationSlider.keyReleased = self.mutationSliderKeyUp
        self.mutationSlider.mousePressed = self.mutationSliderMouseDown
        self.page2.add(self.mutationSlider)
        self.mutationLabel = JLabel('Mutation strength (as percent of mean values)', displayedMnemonic=KeyEvent.VK_M, labelFor=self.mutationSlider, font=buttonFont)
        self.mutationLabel.setBounds(8, 12, 223, 14)
        self.page2.add(self.mutationLabel)
        self.mutationSections = JList(DefaultListModel(), mouseClicked=self.mutationSectionsClick, fixedCellHeight=16)
        self.mutationSections.setBounds(95, 58, 230, 240)
        #  --------------- UNHANDLED ATTRIBUTE: self.mutationSections.Style = lbOwnerDrawFixed
        self.mutationSections.getModel().addElement("General: 50%")
        self.mutationSections.getModel().addElement("Meristems: 50%")
        self.mutationSections.getModel().addElement("Internodes: 50%")
        self.mutationSections.getModel().addElement("Leaves: 50%")
        self.mutationSections.getModel().addElement("First leaves: 50%")
        self.mutationSections.getModel().addElement("Flowers (F): 50%")
        self.mutationSections.getModel().addElement("Flowers (M): 50%")
        self.mutationSections.getModel().addElement("Inflorescences (F): 50%")
        self.mutationSections.getModel().addElement("Inflorescences (M): 50%")
        self.mutationSections.getModel().addElement("Fruit: 50%")
        self.mutationSections.getModel().addElement("Root top: 50%")
        #  --------------- UNHANDLED ATTRIBUTE: self.mutationSections.MultiSelect = True
        #  --------------- UNHANDLED ATTRIBUTE: self.mutationSections.OnDrawItem = mutationSectionsDrawItem
        scroller = JScrollPane(self.mutationSections)
        scroller.setBounds(95, 58, 230, 240)
        self.page2.add(scroller)
        self.mutationSelectAll = JButton('Select all', actionPerformed=self.mutationSelectAllClick, font=buttonFont, margin=buttonMargin)
        self.mutationSelectAll.setMnemonic(KeyEvent.VK_A)
        self.mutationSelectAll.setBounds(10, 94, 80, 24)
        self.page2.add(self.mutationSelectAll)
        self.mutationSelectNone = JButton('Select none', actionPerformed=self.mutationSelectNoneClick, font=buttonFont, margin=buttonMargin)
        self.mutationSelectNone.setMnemonic(KeyEvent.VK_N)
        self.mutationSelectNone.setBounds(10, 122, 80, 24)
        self.page2.add(self.mutationSelectNone)
        self.breedingOptions.addTab('Mutation', None, self.page2)
        
        self.page3 = JPanel(layout=None)
        self.weightAmountLabel = JLabel('50%', font=buttonFont)
        self.weightAmountLabel.setBounds(11, 32, 22, 14)
        self.page3.add(self.weightAmountLabel)
        self.weightZero = JLabel('0', font=buttonFont)
        self.weightZero.setBounds(46, 32, 6, 14)
        self.page3.add(self.weightZero)
        self.weightOneHundred = JLabel('100', font=buttonFont)
        self.weightOneHundred.setBounds(290, 32, 18, 14)
        self.page3.add(self.weightOneHundred)
        self.weightShowSectionsImage = toolkit.createImage("../resources/BreedingOptionsForm_weightShowSections.png")
        self.weightShowSections = SpeedButton('Sections', ImageIcon(self.weightShowSectionsImage), actionPerformed=self.weightShowSectionsClick, font=buttonFont, margin=buttonMargin)
        self.weightShowSections.setMnemonic(KeyEvent.VK_S)
        self.weightShowSections.setBounds(10, 59, 81, 24)
        self.page3.add(self.weightShowSections)
        self.weightSlider = JSlider()
        self.weightSlider.setBounds(56, 35, 229, 9)
        #  --------------- UNHANDLED ATTRIBUTE: self.weightSlider.CurrentValue = 0
        self.weightSlider.mouseMoved = self.weightSliderMouseMove
        self.weightSlider.mouseDragged = self.weightSliderMouseMove
        self.weightSlider.mouseReleased = self.weightSliderMouseUp
        self.weightSlider.keyReleased = self.weightSliderKeyUp
        self.weightSlider.mousePressed = self.weightSliderMouseDown
        self.page3.add(self.weightSlider)
        self.weightLabel = JLabel('Relative weight of first parent', displayedMnemonic=KeyEvent.VK_W, labelFor=self.weightSlider, font=buttonFont)
        self.weightLabel.setBounds(9, 12, 143, 14)
        self.page3.add(self.weightLabel)
        self.weightSelectAll = JButton('Select all', actionPerformed=self.weightSelectAllClick, font=buttonFont, margin=buttonMargin)
        self.weightSelectAll.setMnemonic(KeyEvent.VK_A)
        self.weightSelectAll.setBounds(10, 95, 80, 24)
        self.page3.add(self.weightSelectAll)
        self.weightSelectNone = JButton('Select none', actionPerformed=self.weightSelectNoneClick, font=buttonFont, margin=buttonMargin)
        self.weightSelectNone.setMnemonic(KeyEvent.VK_N)
        self.weightSelectNone.setBounds(10, 123, 80, 24)
        self.page3.add(self.weightSelectNone)
        self.weightSections = JList(DefaultListModel(), mouseClicked=self.weightSectionsClick, fixedCellHeight=16)
        self.weightSections.setBounds(95, 59, 230, 240)
        #  --------------- UNHANDLED ATTRIBUTE: self.weightSections.Style = lbOwnerDrawFixed
        self.weightSections.getModel().addElement("General: 50%")
        self.weightSections.getModel().addElement("Meristems: 50%")
        self.weightSections.getModel().addElement("Internodes: 50%")
        self.weightSections.getModel().addElement("Leaves: 50%")
        self.weightSections.getModel().addElement("First leaves: 50%")
        self.weightSections.getModel().addElement("Flowers (F): 50%")
        self.weightSections.getModel().addElement("Flowers (M): 50%")
        self.weightSections.getModel().addElement("Inflorescences (F): 50%")
        self.weightSections.getModel().addElement("Inflorescences (M): 50%")
        self.weightSections.getModel().addElement("Fruit: 50%")
        self.weightSections.getModel().addElement("Root top: 50%")
        #  --------------- UNHANDLED ATTRIBUTE: self.weightSections.MultiSelect = True
        #  --------------- UNHANDLED ATTRIBUTE: self.weightSections.OnDrawItem = weightSectionsDrawItem
        scroller = JScrollPane(self.weightSections)
        scroller.setBounds(95, 59, 230, 240)
        self.page3.add(scroller)
        self.breedingOptions.addTab('Blending', None, self.page3)
        
        self.page4 = JPanel(layout=None)
        self.nonNumericLabel = JLabel(' Where to get non-numeric parameters', font=buttonFont)
        self.nonNumericLabel.setBounds(17, 31, 186, 14)
        self.page4.add(self.nonNumericLabel)
        self.firstPlantIfEqualLabel = JLabel('get from parent with higher weight; if 50/50,', font=buttonFont)
        self.firstPlantIfEqualLabel.setBounds(29, 117, 212, 14)
        self.page4.add(self.firstPlantIfEqualLabel)
        self.alwaysCopyFromFirstPlant = JRadioButton('get from first parent', actionPerformed=self.alwaysCopyFromFirstPlantClick, font=buttonFont, margin=buttonMargin)
        self.alwaysCopyFromFirstPlant.setMnemonic(KeyEvent.VK_F)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.alwaysCopyFromFirstPlant)
        self.alwaysCopyFromFirstPlant.setBounds(29, 51, 168, 17)
        self.page4.add(self.alwaysCopyFromFirstPlant)
        self.alwaysCopyFromSecondPlant = JRadioButton('get from second parent', actionPerformed=self.alwaysCopyFromSecondPlantClick, font=buttonFont, margin=buttonMargin)
        self.alwaysCopyFromSecondPlant.setMnemonic(KeyEvent.VK_S)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.alwaysCopyFromSecondPlant)
        self.alwaysCopyFromSecondPlant.setBounds(29, 73, 194, 17)
        self.page4.add(self.alwaysCopyFromSecondPlant)
        self.copyRandomlyBasedOnWeights = JRadioButton('choose randomly using weights as probabilities', actionPerformed=self.copyRandomlyBasedOnWeightsClick, font=buttonFont, margin=buttonMargin)
        self.copyRandomlyBasedOnWeights.setMnemonic(KeyEvent.VK_W)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.copyRandomlyBasedOnWeights)
        self.copyRandomlyBasedOnWeights.setBounds(29, 95, 258, 17)
        self.copyRandomlyBasedOnWeights.putClientProperty("tag", 1)
        self.page4.add(self.copyRandomlyBasedOnWeights)
        self.copyBasedOnWeightsIfEqualFirstPlant = JRadioButton('get from the first parent', actionPerformed=self.copyBasedOnWeightsIfEqualFirstPlantClick, font=buttonFont, margin=buttonMargin)
        self.copyBasedOnWeightsIfEqualFirstPlant.setMnemonic(KeyEvent.VK_I)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.copyBasedOnWeightsIfEqualFirstPlant)
        self.copyBasedOnWeightsIfEqualFirstPlant.setBounds(49, 139, 237, 17)
        self.page4.add(self.copyBasedOnWeightsIfEqualFirstPlant)
        self.copyBasedOnWeightsIfEqualSecondPlant = JRadioButton('get from the second parent', actionPerformed=self.copyBasedOnWeightsIfEqualSecondPlantClick, font=buttonFont, margin=buttonMargin)
        self.copyBasedOnWeightsIfEqualSecondPlant.setMnemonic(KeyEvent.VK_E)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.copyBasedOnWeightsIfEqualSecondPlant)
        self.copyBasedOnWeightsIfEqualSecondPlant.setBounds(49, 161, 237, 17)
        self.page4.add(self.copyBasedOnWeightsIfEqualSecondPlant)
        self.copyBasedOnWeightsIfEqualChooseRandomly = JRadioButton('choose randomly', actionPerformed=self.copyBasedOnWeightsIfEqualChooseRandomlyClick, font=buttonFont, margin=buttonMargin)
        self.copyBasedOnWeightsIfEqualChooseRandomly.setMnemonic(KeyEvent.VK_R)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.copyBasedOnWeightsIfEqualChooseRandomly)
        self.copyBasedOnWeightsIfEqualChooseRandomly.setBounds(49, 183, 237, 17)
        self.page4.add(self.copyBasedOnWeightsIfEqualChooseRandomly)
        self.breedingOptions.addTab('Non-numeric', None, self.page4)
        
        self.page5 = JPanel(layout=None)
        self.changeTdoLibraryImage = toolkit.createImage("../resources/BreedingOptionsForm_changeTdoLibrary.png")
        self.changeTdoLibrary = SpeedButton('Change...', ImageIcon(self.changeTdoLibraryImage), actionPerformed=self.changeTdoLibraryClick, font=buttonFont, margin=buttonMargin)
        self.changeTdoLibrary.setMnemonic(KeyEvent.VK_C)
        self.changeTdoLibrary.setBounds(257, 80, 84, 24)
        self.page5.add(self.changeTdoLibrary)
        self.treatColorsAsNumbers = JCheckBox('mutate and blend colors as numbers', actionPerformed=self.treatColorsAsNumbersClick, font=buttonFont, margin=buttonMargin)
        self.treatColorsAsNumbers.setMnemonic(KeyEvent.VK_C)
        self.treatColorsAsNumbers.setBounds(15, 31, 218, 17)
        self.page5.add(self.treatColorsAsNumbers)
        self.chooseTdosRandomly = JCheckBox('choose 3D objects randomly from current library', actionPerformed=self.chooseTdosRandomlyClick, font=buttonFont, margin=buttonMargin)
        self.chooseTdosRandomly.setMnemonic(KeyEvent.VK_O)
        self.chooseTdosRandomly.setBounds(15, 61, 258, 17)
        self.page5.add(self.chooseTdosRandomly)
        self.currentTdoLibraryFileName = JTextField('currentTdoLibraryFileName', 10, editable=0)
        self.currentTdoLibraryFileName.setBounds(34, 83, 217, 22)
        self.page5.add(self.currentTdoLibraryFileName)
        self.breedingOptions.addTab('Colors and 3D objects', None, self.page5)
        
        self.breedingOptions.setBounds(0, 0, 351, 330)
        #  --------------- UNHANDLED ATTRIBUTE: self.breedingOptions.TabFont.Style = []
        #  --------------- UNHANDLED ATTRIBUTE: self.breedingOptions.TabFont.Color = clBlack
        #  --------------- UNHANDLED ATTRIBUTE: self.breedingOptions.TabFont.Charset = DEFAULT_CHARSET
        #  --------------- UNHANDLED ATTRIBUTE: self.breedingOptions.TabFont.Name = 'Arial'
        #  --------------- UNHANDLED ATTRIBUTE: self.breedingOptions.TabFont.Height = -11
        contentPane.add(self.upImage)
        contentPane.add(self.downImage)
        contentPane.add(self.helpButton)
        contentPane.add(self.ok)
        contentPane.add(self.cancel)
        contentPane.add(self.breedingOptions)
        
    def alwaysCopyFromFirstPlantClick(self, event):
        print "alwaysCopyFromFirstPlantClick"
        
    def alwaysCopyFromSecondPlantClick(self, event):
        print "alwaysCopyFromSecondPlantClick"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def changeTdoLibraryClick(self, event):
        print "changeTdoLibraryClick"
        
    def chooseTdosRandomlyClick(self, event):
        print "chooseTdosRandomlyClick"
        
    def copyBasedOnWeightsIfEqualChooseRandomlyClick(self, event):
        print "copyBasedOnWeightsIfEqualChooseRandomlyClick"
        
    def copyBasedOnWeightsIfEqualFirstPlantClick(self, event):
        print "copyBasedOnWeightsIfEqualFirstPlantClick"
        
    def copyBasedOnWeightsIfEqualSecondPlantClick(self, event):
        print "copyBasedOnWeightsIfEqualSecondPlantClick"
        
    def copyRandomlyBasedOnWeightsClick(self, event):
        print "copyRandomlyBasedOnWeightsClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def mutationSectionsClick(self, event):
        print "mutationSectionsClick"
        
    def mutationSelectAllClick(self, event):
        print "mutationSelectAllClick"
        
    def mutationSelectNoneClick(self, event):
        print "mutationSelectNoneClick"
        
    def mutationShowSectionsClick(self, event):
        print "mutationShowSectionsClick"
        
    def mutationSliderKeyUp(self, event):
        print "mutationSliderKeyUp"
        
    def mutationSliderMouseDown(self, event):
        print "mutationSliderMouseDown"
        
    def mutationSliderMouseMove(self, event):
        print "mutationSliderMouseMove"
        
    def mutationSliderMouseUp(self, event):
        print "mutationSliderMouseUp"
        
    def okClick(self, event):
        print "okClick"
        
    def treatColorsAsNumbersClick(self, event):
        print "treatColorsAsNumbersClick"
        
    def updateTimeSeriesPlantsOnParameterChangeClick(self, event):
        print "updateTimeSeriesPlantsOnParameterChangeClick"
        
    def weightSectionsClick(self, event):
        print "weightSectionsClick"
        
    def weightSelectAllClick(self, event):
        print "weightSelectAllClick"
        
    def weightSelectNoneClick(self, event):
        print "weightSelectNoneClick"
        
    def weightShowSectionsClick(self, event):
        print "weightShowSectionsClick"
        
    def weightSliderKeyUp(self, event):
        print "weightSliderKeyUp"
        
    def weightSliderMouseDown(self, event):
        print "weightSliderMouseDown"
        
    def weightSliderMouseMove(self, event):
        print "weightSliderMouseMove"
        
    def weightSliderMouseUp(self, event):
        print "weightSliderMouseUp"
        
if __name__ == "__main__":
    window = BreedingOptionsWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
