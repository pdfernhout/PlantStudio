from common import *

#Useage:
#        import OptionsWindow
#        window = OptionsWindow.OptionsWindow()
#        window.visible = 1

class OptionsWindow(JFrame):
    def __init__(self, title='PlantStudio Preferences'):
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
        self.setBounds(279, 188, 450, 247  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = [biSystemMenu]
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.ActiveControl = cancel
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        
        self.helpButtonImage = toolkit.createImage("../resources/OptionsForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(386, 63, 61, 25)
        self.Close = JButton('OK', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.Close.setMnemonic(KeyEvent.VK_O)
        self.Close.setBounds(386, 4, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.Close.DragCursor = crHandPoint
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(386, 27, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.optionsNotebook = JTabbedPane()
        
        self.page1 = JPanel(layout=None)
        self.backgroundColor = JPanel(layout=None)
        # -- self.backgroundColor.setLayout(BoxLayout(self.backgroundColor, BoxLayout.Y_AXIS))
        self.backgroundColor.setBounds(9, 17, 20, 20)
        self.backgroundColor.mouseReleased = self.backgroundColorMouseUp
        self.backgroundColorLabel = JLabel('Background color behind plants', displayedMnemonic=KeyEvent.VK_B, labelFor=self.backgroundColor, font=buttonFont)
        self.backgroundColorLabel.setBounds(34, 20, 152, 14)
        self.showPlantDrawingProgress = JCheckBox('Show drawing progress', font=buttonFont, margin=buttonMargin)
        self.showPlantDrawingProgress.setMnemonic(KeyEvent.VK_S)
        self.showPlantDrawingProgress.setBounds(9, 69, 161, 17)
        self.transparentColor = JPanel(layout=None)
        # -- self.transparentColor.setLayout(BoxLayout(self.transparentColor, BoxLayout.Y_AXIS))
        self.transparentColor.setBounds(9, 43, 20, 20)
        self.transparentColor.mouseReleased = self.transparentColorMouseUp
        self.transparentColorLabel = JLabel('Transparent color for overlaying plants if using plant bitmaps', displayedMnemonic=KeyEvent.VK_T, labelFor=self.transparentColor, font=buttonFont)
        self.transparentColorLabel.setBounds(34, 46, 292, 14)
        self.wholeProgramBox = JPanel(layout=None)
        # -- self.wholeProgramBox.setLayout(BoxLayout(self.wholeProgramBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.wholeProgramBox.border = TitledBorder("' Whole program '")
        self.wholeProgramBox.add(self.backgroundColor)
        self.wholeProgramBox.add(self.backgroundColorLabel)
        self.wholeProgramBox.add(self.showPlantDrawingProgress)
        self.wholeProgramBox.add(self.transparentColor)
        self.wholeProgramBox.add(self.transparentColorLabel)
        self.wholeProgramBox.setBounds(4, 94, 362, 95)
        self.page1.add(self.wholeProgramBox)
        self.customDrawOptions = JButton('Change Custom Drawing Options...', actionPerformed=self.customDrawOptionsClick, font=buttonFont, margin=buttonMargin)
        self.customDrawOptions.setMnemonic(KeyEvent.VK_W)
        self.customDrawOptions.setBounds(8, 54, 202, 21)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.memoryLimitForPlantBitmaps_MB = JSpinner(SpinnerNumberModel(200, 1, 200, 1))
        self.memoryLimitForPlantBitmaps_MB.setBounds(8, 24, 47, 23)
        self.memoryLimitLabel = JLabel('Upper limit on memory devoted to plant bitmaps (1-200 MB)', displayedMnemonic=KeyEvent.VK_U, labelFor=self.memoryLimitForPlantBitmaps_MB, font=buttonFont)
        self.memoryLimitLabel.setBounds(60, 29, 282, 14)
        self.mainWindowDrawingOptionsBox = JPanel(layout=None)
        # -- self.mainWindowDrawingOptionsBox.setLayout(BoxLayout(self.mainWindowDrawingOptionsBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.mainWindowDrawingOptionsBox.border = TitledBorder("' Main window '")
        self.mainWindowDrawingOptionsBox.add(self.customDrawOptions)
        self.mainWindowDrawingOptionsBox.add(self.memoryLimitForPlantBitmaps_MB)
        self.mainWindowDrawingOptionsBox.add(self.memoryLimitLabel)
        self.mainWindowDrawingOptionsBox.setBounds(4, 4, 362, 85)
        self.page1.add(self.mainWindowDrawingOptionsBox)
        self.optionsNotebook.addTab('Drawing', None, self.page1)
        
        self.page2 = JPanel(layout=None)
        self.firstSelectionRectangleColor = JPanel(layout=None)
        # -- self.firstSelectionRectangleColor.setLayout(BoxLayout(self.firstSelectionRectangleColor, BoxLayout.Y_AXIS))
        self.firstSelectionRectangleColor.setBounds(8, 18, 20, 20)
        self.firstSelectionRectangleColor.mouseReleased = self.firstSelectionRectangleColorMouseUp
        self.firstSelectionRectangleColorLabel = JLabel('Rectangle color for focused plant', displayedMnemonic=KeyEvent.VK_F, labelFor=self.firstSelectionRectangleColor, font=buttonFont)
        self.firstSelectionRectangleColorLabel.setBounds(32, 21, 161, 14)
        self.multiSelectionRectangleColor = JPanel(layout=None)
        # -- self.multiSelectionRectangleColor.setLayout(BoxLayout(self.multiSelectionRectangleColor, BoxLayout.Y_AXIS))
        self.multiSelectionRectangleColor.setBounds(8, 40, 20, 20)
        self.multiSelectionRectangleColor.mouseReleased = self.multiSelectionRectangleColorMouseUp
        self.multiSelectionRectangleColorLabel = JLabel('Rectangle color for other selected plants', displayedMnemonic=KeyEvent.VK_O, labelFor=self.multiSelectionRectangleColor, font=buttonFont)
        self.multiSelectionRectangleColorLabel.setBounds(32, 43, 196, 14)
        self.GroupBox1 = JPanel(layout=None)
        # -- self.GroupBox1.setLayout(BoxLayout(self.GroupBox1, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox1.border = TitledBorder("' Main window '")
        self.GroupBox1.add(self.firstSelectionRectangleColor)
        self.GroupBox1.add(self.firstSelectionRectangleColorLabel)
        self.GroupBox1.add(self.multiSelectionRectangleColor)
        self.GroupBox1.add(self.multiSelectionRectangleColorLabel)
        self.GroupBox1.setBounds(4, 4, 362, 69)
        self.page2.add(self.GroupBox1)
        self.optionsNotebook.addTab('Selecting', None, self.page2)
        
        self.page3 = JPanel(layout=None)
        self.pasteRectSizeLabel = JLabel(' Width and height of plant pasted from text (50-500 pixels)', displayedMnemonic=KeyEvent.VK_P, font=buttonFont)
        self.pasteRectSizeLabel.setBounds(67, 114, 280, 14)
        self.resizeRectSizeLabel = JLabel(' Width and height of resizing square (2-20 pixels)', displayedMnemonic=KeyEvent.VK_S, font=buttonFont)
        self.resizeRectSizeLabel.setBounds(67, 146, 238, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.rotationIncrement = JSpinner(SpinnerNumberModel(1, 1, 100, 1))
        self.rotationIncrement.setBounds(8, 19, 53, 23)
        self.rotationIncrementLabel = JLabel('Rotation change with arrow or mouse click (1-100 degrees)', displayedMnemonic=KeyEvent.VK_R, labelFor=self.rotationIncrement, font=buttonFont)
        self.rotationIncrementLabel.setBounds(67, 24, 289, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.nudgeDistance = JSpinner(SpinnerNumberModel(1, 1, 100, 1))
        self.nudgeDistance.setBounds(8, 49, 53, 23)
        self.nudgeDistanceLabel = JLabel('Distance plant moves with Control-arrow key (0-100 pixels)', displayedMnemonic=KeyEvent.VK_M, labelFor=self.nudgeDistance, font=buttonFont)
        self.nudgeDistanceLabel.setBounds(67, 54, 288, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.resizeKeyUpMultiplierPercent = JSpinner(SpinnerNumberModel(100, 100, 200, 10))
        self.resizeKeyUpMultiplierPercent.setBounds(8, 80, 53, 23)
        self.resizeDistanceLabel = JLabel('Size increase with Control-Shift-up-arrow key (100-200%)', displayedMnemonic=KeyEvent.VK_I, labelFor=self.resizeKeyUpMultiplierPercent, font=buttonFont)
        self.resizeDistanceLabel.setBounds(67, 84, 284, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.pasteRectSize = JSpinner(SpinnerNumberModel(100, 50, 500, 10))
        self.pasteRectSize.setBounds(8, 110, 53, 23)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.resizeRectSize = JSpinner(SpinnerNumberModel(2, 2, 20, 1))
        self.resizeRectSize.setBounds(8, 140, 53, 23)
        self.GroupBox2 = JPanel(layout=None)
        # -- self.GroupBox2.setLayout(BoxLayout(self.GroupBox2, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox2.border = TitledBorder("' Main window '")
        self.GroupBox2.add(self.pasteRectSizeLabel)
        self.GroupBox2.add(self.resizeRectSizeLabel)
        self.GroupBox2.add(self.rotationIncrement)
        self.GroupBox2.add(self.rotationIncrementLabel)
        self.GroupBox2.add(self.nudgeDistance)
        self.GroupBox2.add(self.nudgeDistanceLabel)
        self.GroupBox2.add(self.resizeKeyUpMultiplierPercent)
        self.GroupBox2.add(self.resizeDistanceLabel)
        self.GroupBox2.add(self.pasteRectSize)
        self.GroupBox2.add(self.resizeRectSize)
        self.GroupBox2.setBounds(4, 4, 362, 176)
        self.page3.add(self.GroupBox2)
        self.optionsNotebook.addTab('Editing', None, self.page3)
        
        self.page4 = JPanel(layout=None)
        self.ghostingColor = JPanel(layout=None)
        # -- self.ghostingColor.setLayout(BoxLayout(self.ghostingColor, BoxLayout.Y_AXIS))
        self.ghostingColor.setBounds(8, 20, 20, 20)
        self.ghostingColor.mouseReleased = self.ghostingColorMouseUp
        self.Label9 = JLabel('Ghosting color', displayedMnemonic=KeyEvent.VK_G, labelFor=self.ghostingColor, font=buttonFont)
        self.Label9.setBounds(32, 23, 70, 14)
        self.nonHiddenPosedColor = JPanel(layout=None)
        # -- self.nonHiddenPosedColor.setLayout(BoxLayout(self.nonHiddenPosedColor, BoxLayout.Y_AXIS))
        self.nonHiddenPosedColor.setBounds(8, 43, 20, 20)
        self.nonHiddenPosedColor.mouseReleased = self.nonHiddenPosedColorMouseUp
        self.Label10 = JLabel('Highlighting color for all posed plant parts', displayedMnemonic=KeyEvent.VK_H, labelFor=self.nonHiddenPosedColor, font=buttonFont)
        self.Label10.setBounds(32, 45, 198, 14)
        self.selectedPosedColor = JPanel(layout=None)
        # -- self.selectedPosedColor.setLayout(BoxLayout(self.selectedPosedColor, BoxLayout.Y_AXIS))
        self.selectedPosedColor.setBounds(8, 66, 20, 20)
        self.selectedPosedColor.mouseReleased = self.selectedPosedColorMouseUp
        self.Label3 = JLabel('Highlighting color for selected posed plant part', displayedMnemonic=KeyEvent.VK_S, labelFor=self.selectedPosedColor, font=buttonFont)
        self.Label3.setBounds(32, 69, 223, 14)
        self.GroupBox4 = JPanel(layout=None)
        # -- self.GroupBox4.setLayout(BoxLayout(self.GroupBox4, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox4.border = TitledBorder("' Main window '")
        self.GroupBox4.add(self.ghostingColor)
        self.GroupBox4.add(self.Label9)
        self.GroupBox4.add(self.nonHiddenPosedColor)
        self.GroupBox4.add(self.Label10)
        self.GroupBox4.add(self.selectedPosedColor)
        self.GroupBox4.add(self.Label3)
        self.GroupBox4.setBounds(4, 5, 362, 97)
        self.page4.add(self.GroupBox4)
        self.optionsNotebook.addTab('Posing', None, self.page4)
        
        self.page5 = JPanel(layout=None)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.undoLimit = JSpinner(SpinnerNumberModel(1, 1, 1000, 1))
        self.undoLimit.setBounds(8, 20, 53, 23)
        self.undoLimitLabel = JLabel('Number of actions to keep in undo list (1-1000 actions)', displayedMnemonic=KeyEvent.VK_N, labelFor=self.undoLimit, font=buttonFont)
        self.undoLimitLabel.setBounds(66, 23, 263, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.undoLimitOfPlants = JSpinner(SpinnerNumberModel(1, 1, 500, 1))
        self.undoLimitOfPlants.setBounds(8, 48, 53, 23)
        self.undoLimitOfPlantsLabel = JLabel('Number of plants to keep in undo list (1-500 plants)', displayedMnemonic=KeyEvent.VK_P, labelFor=self.undoLimitOfPlants, font=buttonFont)
        self.undoLimitOfPlantsLabel.setBounds(66, 51, 245, 14)
        self.GroupBox5 = JPanel(layout=None)
        # -- self.GroupBox5.setLayout(BoxLayout(self.GroupBox5, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox5.border = TitledBorder("' Whole program '")
        self.GroupBox5.add(self.undoLimit)
        self.GroupBox5.add(self.undoLimitLabel)
        self.GroupBox5.add(self.undoLimitOfPlants)
        self.GroupBox5.add(self.undoLimitOfPlantsLabel)
        self.GroupBox5.setBounds(4, 4, 362, 81)
        self.page5.add(self.GroupBox5)
        self.optionsNotebook.addTab('Undoing', None, self.page5)
        
        self.page6 = JPanel(layout=None)
        self.useMetricUnits = JCheckBox('Default to metric units instead of English in parameter panels', font=buttonFont, margin=buttonMargin)
        self.useMetricUnits.setMnemonic(KeyEvent.VK_D)
        self.useMetricUnits.setBounds(8, 20, 319, 17)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.parametersFontSize = JSpinner(SpinnerNumberModel(8, 6, 20, 1))
        self.parametersFontSize.setBounds(8, 43, 53, 23)
        self.parametersFontSizeLabel = JLabel('Font size for parameter panels (6-20)', displayedMnemonic=KeyEvent.VK_P, labelFor=self.parametersFontSize, font=buttonFont)
        self.parametersFontSizeLabel.setBounds(66, 48, 181, 14)
        self.GroupBox6 = JPanel(layout=None)
        # -- self.GroupBox6.setLayout(BoxLayout(self.GroupBox6, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox6.border = TitledBorder("' Main window '")
        self.GroupBox6.add(self.useMetricUnits)
        self.GroupBox6.add(self.parametersFontSize)
        self.GroupBox6.add(self.parametersFontSizeLabel)
        self.GroupBox6.setBounds(4, 4, 362, 75)
        self.page6.add(self.GroupBox6)
        self.Label1 = JLabel('This applies only when long button or parameter hints are on.', font=buttonFont)
        self.Label1.setBounds(64, 110, 295, 14)
        self.openMostRecentFileAtStart = JCheckBox('Open most recent file at start', font=buttonFont, margin=buttonMargin)
        self.openMostRecentFileAtStart.setMnemonic(KeyEvent.VK_F)
        self.openMostRecentFileAtStart.setBounds(8, 20, 237, 17)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.pauseBeforeHint = JSpinner(SpinnerNumberModel(100, 0, 100, 1))
        self.pauseBeforeHint.setBounds(7, 61, 53, 23)
        self.pauseBeforeHintLabel = JLabel('Show hint after mouse is still for (0-100 seconds)', displayedMnemonic=KeyEvent.VK_S, labelFor=self.pauseBeforeHint, font=buttonFont)
        self.pauseBeforeHintLabel.setBounds(64, 66, 240, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.pauseDuringHint = JSpinner(SpinnerNumberModel(100, 0, 100, 5))
        self.pauseDuringHint.setBounds(7, 87, 53, 23)
        self.pauseDuringHintLabel = JLabel('Remove hint after (0-100 seconds)', displayedMnemonic=KeyEvent.VK_R, labelFor=self.pauseDuringHint, font=buttonFont)
        self.pauseDuringHintLabel.setBounds(64, 92, 169, 14)
        self.ignoreWindowSettingsInFile = JCheckBox('Ignore window settings (top/side, one/many) saved in file', font=buttonFont, margin=buttonMargin)
        self.ignoreWindowSettingsInFile.setMnemonic(KeyEvent.VK_I)
        self.ignoreWindowSettingsInFile.setBounds(8, 39, 313, 17)
        self.GroupBox7 = JPanel(layout=None)
        # -- self.GroupBox7.setLayout(BoxLayout(self.GroupBox7, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox7.border = TitledBorder("' Whole program '")
        self.GroupBox7.add(self.Label1)
        self.GroupBox7.add(self.openMostRecentFileAtStart)
        self.GroupBox7.add(self.pauseBeforeHint)
        self.GroupBox7.add(self.pauseBeforeHintLabel)
        self.GroupBox7.add(self.pauseDuringHint)
        self.GroupBox7.add(self.pauseDuringHintLabel)
        self.GroupBox7.add(self.ignoreWindowSettingsInFile)
        self.GroupBox7.setBounds(4, 84, 362, 133)
        self.page6.add(self.GroupBox7)
        self.optionsNotebook.addTab('Miscellaneous', None, self.page6)
        
        self.optionsNotebook.setBounds(0, 0, 379, 247)
        #  --------------- UNHANDLED ATTRIBUTE: self.optionsNotebook.PageIndex = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.optionsNotebook.TabsPerRow = 5
        #  --------------- UNHANDLED ATTRIBUTE: self.optionsNotebook.TabFont.Color = clBtnText
        #  --------------- UNHANDLED ATTRIBUTE: self.optionsNotebook.TabFont.Charset = DEFAULT_CHARSET
        #  --------------- UNHANDLED ATTRIBUTE: self.optionsNotebook.TabFont.Style = []
        #  --------------- UNHANDLED ATTRIBUTE: self.optionsNotebook.TabFont.Name = 'Arial'
        #  --------------- UNHANDLED ATTRIBUTE: self.optionsNotebook.TabFont.Height = -11
        self.drawWithOpenGL = JCheckBox('Draw using OpenGL', font=buttonFont, margin=buttonMargin)
        self.drawWithOpenGL.setBounds(413, 266, 149, 17)
        self.drawWithOpenGL.visible = 0
        self.Image1Image = toolkit.createImage("../resources/OptionsForm_Image1.png")
        self.Image1 = ImagePanel(ImageIcon(self.Image1Image))
        self.Image1.setBounds(3, 2, 31, 47)
        self.Image1.mouseClicked = self.Image1Click
        self.Panel1 = JPanel(layout=None)
        # -- self.Panel1.setLayout(BoxLayout(self.Panel1, BoxLayout.Y_AXIS))
        self.Panel1.add(self.Image1)
        self.Panel1.setBounds(397, 164, 38, 54)
        contentPane.add(self.helpButton)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        contentPane.add(self.optionsNotebook)
        contentPane.add(self.drawWithOpenGL)
        contentPane.add(self.Panel1)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def Image1Click(self, event):
        print "Image1Click"
        
    def backgroundColorMouseUp(self, event):
        print "backgroundColorMouseUp"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def customDrawOptionsClick(self, event):
        print "customDrawOptionsClick"
        
    def firstSelectionRectangleColorMouseUp(self, event):
        print "firstSelectionRectangleColorMouseUp"
        
    def ghostingColorMouseUp(self, event):
        print "ghostingColorMouseUp"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def multiSelectionRectangleColorMouseUp(self, event):
        print "multiSelectionRectangleColorMouseUp"
        
    def nonHiddenPosedColorMouseUp(self, event):
        print "nonHiddenPosedColorMouseUp"
        
    def selectedPosedColorMouseUp(self, event):
        print "selectedPosedColorMouseUp"
        
    def transparentColorMouseUp(self, event):
        print "transparentColorMouseUp"
        
if __name__ == "__main__":
    window = OptionsWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
