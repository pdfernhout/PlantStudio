from common import *

#Useage:
#        import BitmapOptionsWindow
#        window = BitmapOptionsWindow.BitmapOptionsWindow()
#        window.visible = 1

class BitmapOptionsWindow(JFrame):
    def __init__(self, title='Picture export options'):
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
        self.setBounds(416, 120, 475, 378  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = [biSystemMenu]
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.helpButtonImage = toolkit.createImage("../resources/BitmapOptionsForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(413, 63, 60, 21)
        self.Close = JButton('OK', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.Close.setBounds(413, 4, 60, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(413, 29, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.sizeLabel = JLabel('Size (inches)', font=buttonFont)
        self.sizeLabel.setBounds(203, 13, 64, 14)
        self.printWidthLabel = JLabel('width', font=buttonFont)
        self.printWidthLabel.setBounds(220, 35, 27, 14)
        self.printHeightLabel = JLabel('height', font=buttonFont)
        self.printHeightLabel.setBounds(307, 33, 29, 14)
        self.marginsLabel = JLabel('Margins (inches)', font=buttonFont)
        self.marginsLabel.setBounds(205, 61, 81, 14)
        self.printLeftMarginLabel = JLabel('left', font=buttonFont)
        self.printLeftMarginLabel.setBounds(220, 79, 15, 14)
        self.printTopMarginLabel = JLabel('top', font=buttonFont)
        self.printTopMarginLabel.setBounds(220, 105, 15, 14)
        self.printRightMarginLabel = JLabel('right', font=buttonFont)
        self.printRightMarginLabel.setBounds(307, 79, 21, 14)
        self.printBottomMarginLabel = JLabel('bottom', font=buttonFont)
        self.printBottomMarginLabel.setBounds(307, 105, 32, 14)
        self.wholePageImage = ImagePanel() # No image was set
        self.wholePageImage.setBounds(10, 20, 137, 79)
        self.printPreserveAspectRatio = JCheckBox('Maintain aspect ratio', actionPerformed=self.printPreserveAspectRatioClick, font=buttonFont, margin=buttonMargin)
        self.printPreserveAspectRatio.setBounds(252, 128, 129, 17)
        self.printWidthEdit = JTextField("", 10)
        self.printWidthEdit.setBounds(249, 29, 36, 22)
        self.printWidthEdit.focusLost = self.exitEditBox
        self.printWidthEdit.putClientProperty("tag", 1)
        self.printWidthSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.printWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printWidthSpin.png")
        self.printWidthSpin.upIcon = ImageIcon(self.printWidthSpinImage)
        self.printWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printWidthSpin.png")
        self.printWidthSpin.downIcon = ImageIcon(self.printWidthSpinImage)
        self.printWidthSpin.setBounds(287, 30, 16, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.printWidthSpin.FocusControl = printWidthEdit
        self.printWidthSpin.putClientProperty("tag", 10)
        #  --------------- UNHANDLED ATTRIBUTE: self.printWidthSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.printWidthSpin.OnDownClick = spinDown
        self.printHeightEdit = JTextField("", 10)
        self.printHeightEdit.setBounds(342, 29, 36, 22)
        self.printHeightEdit.focusLost = self.exitEditBox
        self.printHeightEdit.putClientProperty("tag", 1)
        self.printHeightSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.printHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printHeightSpin.png")
        self.printHeightSpin.upIcon = ImageIcon(self.printHeightSpinImage)
        self.printHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printHeightSpin.png")
        self.printHeightSpin.downIcon = ImageIcon(self.printHeightSpinImage)
        self.printHeightSpin.setBounds(380, 30, 16, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.printHeightSpin.FocusControl = printHeightEdit
        self.printHeightSpin.putClientProperty("tag", 10)
        #  --------------- UNHANDLED ATTRIBUTE: self.printHeightSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.printHeightSpin.OnDownClick = spinDown
        self.printLeftMarginEdit = JTextField("", 10)
        self.printLeftMarginEdit.setBounds(249, 77, 36, 22)
        self.printLeftMarginEdit.focusLost = self.exitEditBox
        self.printLeftMarginEdit.putClientProperty("tag", 1)
        self.printTopMarginEdit = JTextField("", 10)
        self.printTopMarginEdit.setBounds(249, 101, 36, 22)
        self.printTopMarginEdit.focusLost = self.exitEditBox
        self.printTopMarginEdit.putClientProperty("tag", 1)
        self.printLeftMarginSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.printLeftMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printLeftMarginSpin.png")
        self.printLeftMarginSpin.upIcon = ImageIcon(self.printLeftMarginSpinImage)
        self.printLeftMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printLeftMarginSpin.png")
        self.printLeftMarginSpin.downIcon = ImageIcon(self.printLeftMarginSpinImage)
        self.printLeftMarginSpin.setBounds(287, 78, 16, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.printLeftMarginSpin.FocusControl = printLeftMarginEdit
        self.printLeftMarginSpin.putClientProperty("tag", 10)
        #  --------------- UNHANDLED ATTRIBUTE: self.printLeftMarginSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.printLeftMarginSpin.OnDownClick = spinDown
        self.printTopMarginSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.printTopMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printTopMarginSpin.png")
        self.printTopMarginSpin.upIcon = ImageIcon(self.printTopMarginSpinImage)
        self.printTopMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printTopMarginSpin.png")
        self.printTopMarginSpin.downIcon = ImageIcon(self.printTopMarginSpinImage)
        self.printTopMarginSpin.setBounds(287, 102, 16, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.printTopMarginSpin.FocusControl = printTopMarginEdit
        self.printTopMarginSpin.putClientProperty("tag", 10)
        #  --------------- UNHANDLED ATTRIBUTE: self.printTopMarginSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.printTopMarginSpin.OnDownClick = spinDown
        self.printRightMarginEdit = JTextField("", 10)
        self.printRightMarginEdit.setBounds(342, 75, 36, 22)
        self.printRightMarginEdit.focusLost = self.exitEditBox
        self.printRightMarginEdit.putClientProperty("tag", 1)
        self.printBottomMarginEdit = JTextField("", 10)
        self.printBottomMarginEdit.setBounds(342, 101, 36, 22)
        self.printBottomMarginEdit.focusLost = self.exitEditBox
        self.printBottomMarginEdit.putClientProperty("tag", 1)
        self.printRightMarginSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.printRightMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printRightMarginSpin.png")
        self.printRightMarginSpin.upIcon = ImageIcon(self.printRightMarginSpinImage)
        self.printRightMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printRightMarginSpin.png")
        self.printRightMarginSpin.downIcon = ImageIcon(self.printRightMarginSpinImage)
        self.printRightMarginSpin.setBounds(380, 76, 16, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.printRightMarginSpin.FocusControl = printRightMarginEdit
        self.printRightMarginSpin.putClientProperty("tag", 10)
        #  --------------- UNHANDLED ATTRIBUTE: self.printRightMarginSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.printRightMarginSpin.OnDownClick = spinDown
        self.printBottomMarginSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.printBottomMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printBottomMarginSpin.png")
        self.printBottomMarginSpin.upIcon = ImageIcon(self.printBottomMarginSpinImage)
        self.printBottomMarginSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_printBottomMarginSpin.png")
        self.printBottomMarginSpin.downIcon = ImageIcon(self.printBottomMarginSpinImage)
        self.printBottomMarginSpin.setBounds(380, 102, 16, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.printBottomMarginSpin.FocusControl = printBottomMarginEdit
        self.printBottomMarginSpin.putClientProperty("tag", 10)
        #  --------------- UNHANDLED ATTRIBUTE: self.printBottomMarginSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.printBottomMarginSpin.OnDownClick = spinDown
        self.printImagePanel = JPanel(layout=None)
        # -- self.printImagePanel.setLayout(BoxLayout(self.printImagePanel, BoxLayout.Y_AXIS))
        self.printImagePanel.setBounds(20, 28, 25, 24)
        self.printBox = JPanel(layout=None)
        # -- self.printBox.setLayout(BoxLayout(self.printBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.printBox.border = TitledBorder("'Printing options'")
        self.printBox.add(self.sizeLabel)
        self.printBox.add(self.printWidthLabel)
        self.printBox.add(self.printHeightLabel)
        self.printBox.add(self.marginsLabel)
        self.printBox.add(self.printLeftMarginLabel)
        self.printBox.add(self.printTopMarginLabel)
        self.printBox.add(self.printRightMarginLabel)
        self.printBox.add(self.printBottomMarginLabel)
        self.printBox.add(self.wholePageImage)
        self.printBox.add(self.printPreserveAspectRatio)
        self.printBox.add(self.printWidthEdit)
        self.printBox.add(self.printWidthSpin)
        self.printBox.add(self.printHeightEdit)
        self.printBox.add(self.printHeightSpin)
        self.printBox.add(self.printLeftMarginEdit)
        self.printBox.add(self.printTopMarginEdit)
        self.printBox.add(self.printLeftMarginSpin)
        self.printBox.add(self.printTopMarginSpin)
        self.printBox.add(self.printRightMarginEdit)
        self.printBox.add(self.printBottomMarginEdit)
        self.printBox.add(self.printRightMarginSpin)
        self.printBox.add(self.printBottomMarginSpin)
        self.printBox.add(self.printImagePanel)
        self.printBox.setBounds(0, 225, 409, 150)
        self.sizePixelsLabel = JLabel('Size (pixels)', font=buttonFont)
        self.sizePixelsLabel.setBounds(203, 62, 60, 14)
        self.sizeInchesLabel = JLabel('Size (inches)', font=buttonFont)
        self.sizeInchesLabel.setBounds(203, 18, 64, 14)
        self.inchWidthLabel = JLabel('width', font=buttonFont)
        self.inchWidthLabel.setBounds(220, 38, 27, 14)
        self.inchHeightLabel = JLabel('height', font=buttonFont)
        self.inchHeightLabel.setBounds(307, 38, 29, 14)
        self.pixelWidthLabel = JLabel('width', font=buttonFont)
        self.pixelWidthLabel.setBounds(220, 82, 27, 14)
        self.pixelHeightLabel = JLabel('height', font=buttonFont)
        self.pixelHeightLabel.setBounds(307, 82, 29, 14)
        self.inchWidthEdit = JTextField("", 10)
        self.inchWidthEdit.setBounds(249, 34, 36, 22)
        self.inchWidthEdit.focusLost = self.exitEditBox
        self.inchWidthEdit.putClientProperty("tag", 1)
        self.inchHeightEdit = JTextField("", 10)
        self.inchHeightEdit.setBounds(342, 34, 36, 22)
        self.inchHeightEdit.focusLost = self.exitEditBox
        self.inchHeightEdit.putClientProperty("tag", 1)
        self.colorType = JComboBox(DefaultComboBoxModel())
        self.colorType.setBounds(30, 36, 155, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.colorType.Style = csOwnerDrawFixed
        #  --------------- UNHANDLED ATTRIBUTE: self.colorType.OnChange = colorTypeChange
        self.colorType.getModel().addElement("From screen")
        self.colorType.getModel().addElement("2 colors (1-bit)")
        self.colorType.getModel().addElement("16 colors (4-bit)")
        self.colorType.getModel().addElement("256 colors (8-bit)")
        self.colorType.getModel().addElement("32768 colors (15-bit)")
        self.colorType.getModel().addElement("65536 colors (16-bit)")
        self.colorType.getModel().addElement("16 million colors (24-bit)")
        self.colorType.getModel().addElement("4.3 billion colors (32-bit)")
        #  --------------- UNHANDLED ATTRIBUTE: self.colorType.OnDrawItem = colorTypeDrawItem
        #  --------------- UNHANDLED ATTRIBUTE: self.colorType.ItemHeight = 13
        self.colorsLabel = JLabel('Color depth', displayedMnemonic=KeyEvent.VK_D, labelFor=self.colorType, font=buttonFont)
        self.colorsLabel.setBounds(10, 18, 55, 14)
        self.resolutionEdit = JTextField("", 10)
        self.resolutionEdit.setBounds(30, 80, 36, 22)
        self.resolutionEdit.focusLost = self.exitEditBox
        self.resolutionLabel = JLabel('Resolution (pixels/inch)', displayedMnemonic=KeyEvent.VK_R, labelFor=self.resolutionEdit, font=buttonFont)
        self.resolutionLabel.setBounds(10, 64, 112, 14)
        self.pixelWidthEdit = JTextField("", 10)
        self.pixelWidthEdit.setBounds(249, 78, 36, 22)
        self.pixelWidthEdit.focusLost = self.exitEditBox
        self.pixelHeightEdit = JTextField("", 10)
        self.pixelHeightEdit.setBounds(342, 78, 36, 22)
        self.pixelHeightEdit.focusLost = self.exitEditBox
        self.resolutionSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.resolutionSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_resolutionSpin.png")
        self.resolutionSpin.upIcon = ImageIcon(self.resolutionSpinImage)
        self.resolutionSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_resolutionSpin.png")
        self.resolutionSpin.downIcon = ImageIcon(self.resolutionSpinImage)
        self.resolutionSpin.setBounds(68, 81, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.resolutionSpin.FocusControl = resolutionEdit
        self.resolutionSpin.putClientProperty("tag", 1000)
        #  --------------- UNHANDLED ATTRIBUTE: self.resolutionSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.resolutionSpin.OnDownClick = spinDown
        self.pixelWidthSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.pixelWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_pixelWidthSpin.png")
        self.pixelWidthSpin.upIcon = ImageIcon(self.pixelWidthSpinImage)
        self.pixelWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_pixelWidthSpin.png")
        self.pixelWidthSpin.downIcon = ImageIcon(self.pixelWidthSpinImage)
        self.pixelWidthSpin.setBounds(287, 79, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.pixelWidthSpin.FocusControl = pixelWidthEdit
        self.pixelWidthSpin.putClientProperty("tag", 1000)
        #  --------------- UNHANDLED ATTRIBUTE: self.pixelWidthSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.pixelWidthSpin.OnDownClick = spinDown
        self.pixelHeightSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.pixelHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_pixelHeightSpin.png")
        self.pixelHeightSpin.upIcon = ImageIcon(self.pixelHeightSpinImage)
        self.pixelHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_pixelHeightSpin.png")
        self.pixelHeightSpin.downIcon = ImageIcon(self.pixelHeightSpinImage)
        self.pixelHeightSpin.setBounds(380, 79, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.pixelHeightSpin.FocusControl = pixelHeightEdit
        self.pixelHeightSpin.putClientProperty("tag", 1000)
        #  --------------- UNHANDLED ATTRIBUTE: self.pixelHeightSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.pixelHeightSpin.OnDownClick = spinDown
        self.inchHeightSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.inchHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_inchHeightSpin.png")
        self.inchHeightSpin.upIcon = ImageIcon(self.inchHeightSpinImage)
        self.inchHeightSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_inchHeightSpin.png")
        self.inchHeightSpin.downIcon = ImageIcon(self.inchHeightSpinImage)
        self.inchHeightSpin.setBounds(380, 35, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.inchHeightSpin.FocusControl = inchHeightEdit
        self.inchHeightSpin.putClientProperty("tag", 10)
        #  --------------- UNHANDLED ATTRIBUTE: self.inchHeightSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.inchHeightSpin.OnDownClick = spinDown
        self.inchWidthSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.inchWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_inchWidthSpin.png")
        self.inchWidthSpin.upIcon = ImageIcon(self.inchWidthSpinImage)
        self.inchWidthSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_inchWidthSpin.png")
        self.inchWidthSpin.downIcon = ImageIcon(self.inchWidthSpinImage)
        self.inchWidthSpin.setBounds(287, 35, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.inchWidthSpin.FocusControl = inchWidthEdit
        self.inchWidthSpin.putClientProperty("tag", 10)
        #  --------------- UNHANDLED ATTRIBUTE: self.inchWidthSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.inchWidthSpin.OnDownClick = spinDown
        self.preserveAspectRatio = JCheckBox('Maintain aspect ratio', actionPerformed=self.preserveAspectRatioClick, font=buttonFont, margin=buttonMargin)
        self.preserveAspectRatio.setBounds(249, 108, 127, 17)
        self.jpgCompressionEdit = JTextField("", 10)
        self.jpgCompressionEdit.setBounds(31, 123, 36, 22)
        self.jpgCompressionEdit.focusLost = self.exitEditBox
        self.jpgCompressionEdit.visible = 0
        self.jpgCompressionSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.jpgCompressionSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_jpgCompressionSpin.png")
        self.jpgCompressionSpin.upIcon = ImageIcon(self.jpgCompressionSpinImage)
        self.jpgCompressionSpinImage = toolkit.createImage("../resources/BitmapOptionsForm_jpgCompressionSpin.png")
        self.jpgCompressionSpin.downIcon = ImageIcon(self.jpgCompressionSpinImage)
        self.jpgCompressionSpin.setBounds(69, 124, 15, 19)
        self.jpgCompressionSpin.visible = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.jpgCompressionSpin.FocusControl = jpgCompressionEdit
        self.jpgCompressionSpin.putClientProperty("tag", 100)
        #  --------------- UNHANDLED ATTRIBUTE: self.jpgCompressionSpin.OnUpClick = spinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.jpgCompressionSpin.OnDownClick = spinDown
        self.jpgCompressionLabel = JLabel('JPEG compression (1 least - 100 most)', displayedMnemonic=KeyEvent.VK_C, labelFor=self.resolutionEdit, font=buttonFont)
        self.jpgCompressionLabel.setBounds(10, 107, 187, 14)
        self.jpgCompressionLabel.visible = 0
        self.outputBox = JPanel(layout=None)
        # -- self.outputBox.setLayout(BoxLayout(self.outputBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.outputBox.border = TitledBorder("'Output options'")
        self.outputBox.add(self.sizePixelsLabel)
        self.outputBox.add(self.sizeInchesLabel)
        self.outputBox.add(self.inchWidthLabel)
        self.outputBox.add(self.inchHeightLabel)
        self.outputBox.add(self.pixelWidthLabel)
        self.outputBox.add(self.pixelHeightLabel)
        self.outputBox.add(self.inchWidthEdit)
        self.outputBox.add(self.inchHeightEdit)
        self.outputBox.add(self.colorType)
        self.outputBox.add(self.colorsLabel)
        self.outputBox.add(self.resolutionEdit)
        self.outputBox.add(self.resolutionLabel)
        self.outputBox.add(self.pixelWidthEdit)
        self.outputBox.add(self.pixelHeightEdit)
        self.outputBox.add(self.resolutionSpin)
        self.outputBox.add(self.pixelWidthSpin)
        self.outputBox.add(self.pixelHeightSpin)
        self.outputBox.add(self.inchHeightSpin)
        self.outputBox.add(self.inchWidthSpin)
        self.outputBox.add(self.preserveAspectRatio)
        self.outputBox.add(self.jpgCompressionEdit)
        self.outputBox.add(self.jpgCompressionSpin)
        self.outputBox.add(self.jpgCompressionLabel)
        self.outputBox.setBounds(0, 90, 409, 133)
        self.printSetup = JButton('Printer...', actionPerformed=self.printSetupClick, font=buttonFont, margin=buttonMargin)
        self.printSetup.setMnemonic(KeyEvent.VK_P)
        self.printSetup.setBounds(413, 318, 60, 21)
        self.useSelectedPlants = JRadioButton('selected', actionPerformed=self.selectionChoiceClick, font=buttonFont, margin=buttonMargin)
        self.useSelectedPlants.setMnemonic(KeyEvent.VK_L)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useSelectedPlants)
        self.useSelectedPlants.setBounds(8, 15, 66, 17)
        self.useAllPlants = JRadioButton('all', actionPerformed=self.selectionChoiceClick, font=buttonFont, margin=buttonMargin)
        self.useAllPlants.setMnemonic(KeyEvent.VK_A)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useAllPlants)
        self.useAllPlants.setBounds(8, 49, 36, 17)
        self.useDrawingAreaContents = JRadioButton('drawing area', actionPerformed=self.selectionChoiceClick, font=buttonFont, margin=buttonMargin)
        self.useDrawingAreaContents.setMnemonic(KeyEvent.VK_W)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useDrawingAreaContents)
        self.useDrawingAreaContents.setBounds(8, 66, 93, 17)
        self.useVisiblePlants = JRadioButton('visible', actionPerformed=self.selectionChoiceClick, font=buttonFont, margin=buttonMargin)
        self.useVisiblePlants.setMnemonic(KeyEvent.VK_V)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useVisiblePlants)
        self.useVisiblePlants.setBounds(8, 32, 54, 17)
        self.plantsBox = JPanel(layout=None)
        # -- self.plantsBox.setLayout(BoxLayout(self.plantsBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.plantsBox.border = TitledBorder("'Draw which plants?'")
        self.plantsBox.add(self.useSelectedPlants)
        self.plantsBox.add(self.useAllPlants)
        self.plantsBox.add(self.useDrawingAreaContents)
        self.plantsBox.add(self.useVisiblePlants)
        self.plantsBox.setBounds(0, 2, 109, 89)
        self.borders = JButton('Border...', actionPerformed=self.bordersClick, font=buttonFont, margin=buttonMargin)
        self.borders.setMnemonic(KeyEvent.VK_B)
        self.borders.setBounds(413, 342, 60, 21)
        self.selectedImageInfoLabel = JLabel('Selection: 465 x 252 pixels, 12.4 x 3.1 inches', font=buttonFont)
        self.selectedImageInfoLabel.setBounds(7, 8, 218, 14)
        self.screenInfoLabel = JLabel('Screen: 96 pixels/inch, 2534243 colors (24-bit)', font=buttonFont)
        self.screenInfoLabel.setBounds(7, 26, 226, 14)
        self.printerOrFileTypeInfoLabel = JLabel('Printer:  300 x 300 pixels per inch, Portrait', font=buttonFont)
        self.printerOrFileTypeInfoLabel.setBounds(7, 45, 201, 14)
        self.memoryUseInfoLabel = JLabel('Memory use: 365 K', font=buttonFont)
        self.memoryUseInfoLabel.setBounds(7, 63, 93, 14)
        self.currentStuffPanel = JPanel(layout=None)
        # -- self.currentStuffPanel.setLayout(BoxLayout(self.currentStuffPanel, BoxLayout.Y_AXIS))
        self.currentStuffPanel.add(self.selectedImageInfoLabel)
        self.currentStuffPanel.add(self.screenInfoLabel)
        self.currentStuffPanel.add(self.printerOrFileTypeInfoLabel)
        self.currentStuffPanel.add(self.memoryUseInfoLabel)
        self.currentStuffPanel.setBounds(111, 7, 298, 84)
        self.suggestPrintSize = JButton('Suggest', actionPerformed=self.suggestPrintSizeClick, font=buttonFont, margin=buttonMargin)
        self.suggestPrintSize.setMnemonic(KeyEvent.VK_U)
        self.suggestPrintSize.setBounds(413, 246, 60, 21)
        self.printCenter = JButton('Center', actionPerformed=self.printCenterClick, font=buttonFont, margin=buttonMargin)
        self.printCenter.setMnemonic(KeyEvent.VK_E)
        self.printCenter.setBounds(413, 270, 60, 21)
        self.printUseWholePage = JButton('Fill page', actionPerformed=self.printUseWholePageClick, font=buttonFont, margin=buttonMargin)
        self.printUseWholePage.setMnemonic(KeyEvent.VK_F)
        self.printUseWholePage.setBounds(413, 294, 60, 21)
        #  ------- UNHANDLED TYPE TPrintDialog: PrintDialog 
        #  --------------- UNHANDLED ATTRIBUTE: self.PrintDialog.Top = 136
        #  --------------- UNHANDLED ATTRIBUTE: self.PrintDialog.Left = 431
        contentPane.add(self.helpButton)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        contentPane.add(self.printBox)
        contentPane.add(self.outputBox)
        contentPane.add(self.printSetup)
        contentPane.add(self.plantsBox)
        contentPane.add(self.borders)
        contentPane.add(self.currentStuffPanel)
        contentPane.add(self.suggestPrintSize)
        contentPane.add(self.printCenter)
        contentPane.add(self.printUseWholePage)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def bordersClick(self, event):
        print "bordersClick"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def exitEditBox(self, event):
        print "exitEditBox"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def preserveAspectRatioClick(self, event):
        print "preserveAspectRatioClick"
        
    def printCenterClick(self, event):
        print "printCenterClick"
        
    def printPreserveAspectRatioClick(self, event):
        print "printPreserveAspectRatioClick"
        
    def printSetupClick(self, event):
        print "printSetupClick"
        
    def printUseWholePageClick(self, event):
        print "printUseWholePageClick"
        
    def selectionChoiceClick(self, event):
        print "selectionChoiceClick"
        
    def suggestPrintSizeClick(self, event):
        print "suggestPrintSizeClick"
        
if __name__ == "__main__":
    window = BitmapOptionsWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
