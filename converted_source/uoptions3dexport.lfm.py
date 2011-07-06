from common import *

#Useage:
#        import Generic3DOptionsWindow
#        window = Generic3DOptionsWindow.Generic3DOptionsWindow()
#        window.visible = 1

class Generic3DOptionsWindow(JFrame):
    def __init__(self, title='3D Export Options'):
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
        self.setBounds(245, 119, 576, 529  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.helpButtonImage = toolkit.createImage("../resources/Generic3DOptionsForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(290, 64, 60, 21)
        self.translatePlantsToWindowPositions = JCheckBox('Translate plants to match window positions', font=buttonFont, margin=buttonMargin)
        self.translatePlantsToWindowPositions.setMnemonic(KeyEvent.VK_T)
        self.translatePlantsToWindowPositions.setBounds(10, 151, 245, 17)
        self.writeColors = JCheckBox('Write colors', font=buttonFont, margin=buttonMargin)
        self.writeColors.setMnemonic(KeyEvent.VK_C)
        self.writeColors.setBounds(10, 115, 101, 17)
        self.Label3 = JLabel('characters (1-60)', font=buttonFont)
        self.Label3.setBounds(151, 7, 86, 14)
        self.sidesLabel = JLabel('sides (3-20)', font=buttonFont)
        self.sidesLabel.setBounds(200, 35, 59, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.lengthOfShortName = JSpinner(SpinnerNumberModel(3, 1, 60, 1))
        self.lengthOfShortName.setBounds(99, 3, 45, 23)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.stemCylinderFaces = JSpinner(SpinnerNumberModel(3, 3, 20, 1))
        self.stemCylinderFaces.setBounds(153, 30, 45, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.stemCylinderFaces.OnChange = stemCylinderFacesChange
        self.Label2 = JLabel('Limit plant name to', displayedMnemonic=KeyEvent.VK_N, labelFor=self.stemCylinderFaces, font=buttonFont)
        self.Label2.setBounds(5, 7, 88, 14)
        self.stemCylinderFacesLabel = JLabel('Draw stems as cylinders with', displayedMnemonic=KeyEvent.VK_Y, labelFor=self.stemCylinderFaces, font=buttonFont)
        self.stemCylinderFacesLabel.setBounds(5, 35, 145, 14)
        self.plantNameAndCylinderSidesPanel = JPanel(layout=None)
        # -- self.plantNameAndCylinderSidesPanel.setLayout(BoxLayout(self.plantNameAndCylinderSidesPanel, BoxLayout.Y_AXIS))
        self.plantNameAndCylinderSidesPanel.add(self.Label3)
        self.plantNameAndCylinderSidesPanel.add(self.sidesLabel)
        self.plantNameAndCylinderSidesPanel.add(self.lengthOfShortName)
        self.plantNameAndCylinderSidesPanel.add(self.stemCylinderFaces)
        self.plantNameAndCylinderSidesPanel.add(self.Label2)
        self.plantNameAndCylinderSidesPanel.add(self.stemCylinderFacesLabel)
        self.plantNameAndCylinderSidesPanel.setBounds(6, 16, 261, 56)
        self.writePlantNumberInFrontOfName = JCheckBox('Write plant number in front of name', font=buttonFont, margin=buttonMargin)
        self.writePlantNumberInFrontOfName.setMnemonic(KeyEvent.VK_U)
        self.writePlantNumberInFrontOfName.setBounds(10, 96, 219, 17)
        self.Label8 = JLabel('dimension', font=buttonFont)
        self.Label8.setBounds(154, 11, 48, 14)
        self.pressPlants = JCheckBox('"Press" plants in', font=buttonFont, margin=buttonMargin)
        self.pressPlants.setMnemonic(KeyEvent.VK_E)
        self.pressPlants.setBounds(8, 8, 99, 17)
        self.directionToPressPlants = JComboBox(DefaultComboBoxModel())
        self.directionToPressPlants.setBounds(108, 3, 41, 22)
        #  --------------- UNHANDLED ATTRIBUTE: self.directionToPressPlants.Style = csDropDownList
        self.directionToPressPlants.getModel().addElement("x")
        self.directionToPressPlants.getModel().addElement("y")
        self.directionToPressPlants.getModel().addElement("z")
        #  --------------- UNHANDLED ATTRIBUTE: self.directionToPressPlants.ItemHeight = 14
        self.pressPlantsPanel = JPanel(layout=None)
        # -- self.pressPlantsPanel.setLayout(BoxLayout(self.pressPlantsPanel, BoxLayout.Y_AXIS))
        self.pressPlantsPanel.add(self.Label8)
        self.pressPlantsPanel.add(self.pressPlants)
        self.pressPlantsPanel.add(self.directionToPressPlants)
        self.pressPlantsPanel.setBounds(2, 69, 273, 28)
        self.makeTrianglesDoubleSided = JCheckBox('Double polygons on 3D objects', font=buttonFont, margin=buttonMargin)
        self.makeTrianglesDoubleSided.setMnemonic(KeyEvent.VK_D)
        self.makeTrianglesDoubleSided.setBounds(10, 133, 181, 17)
        self.otherGroupBox = JPanel(layout=None)
        # -- self.otherGroupBox.setLayout(BoxLayout(self.otherGroupBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.otherGroupBox.border = TitledBorder("' Other options '")
        self.otherGroupBox.add(self.translatePlantsToWindowPositions)
        self.otherGroupBox.add(self.writeColors)
        self.otherGroupBox.add(self.plantNameAndCylinderSidesPanel)
        self.otherGroupBox.add(self.writePlantNumberInFrontOfName)
        self.otherGroupBox.add(self.pressPlantsPanel)
        self.otherGroupBox.add(self.makeTrianglesDoubleSided)
        self.otherGroupBox.setBounds(4, 232, 280, 175)
        self.colorDXFFromRGB = JRadioButton('use front-face RGB colors', font=buttonFont, margin=buttonMargin)
        self.colorDXFFromRGB.setMnemonic(KeyEvent.VK_R)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.colorDXFFromRGB)
        self.colorDXFFromRGB.setBounds(9, 35, 232, 17)
        self.colorDXFFromOneColor = JRadioButton('use this one color         for all plant parts', font=buttonFont, margin=buttonMargin)
        self.colorDXFFromOneColor.setMnemonic(KeyEvent.VK_N)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.colorDXFFromOneColor)
        self.colorDXFFromOneColor.setBounds(9, 56, 244, 15)
        self.wholePlantColor = JPanel(layout=None)
        # -- self.wholePlantColor.setLayout(BoxLayout(self.wholePlantColor, BoxLayout.Y_AXIS))
        self.wholePlantColor.setBounds(119, 56, 16, 14)
        self.wholePlantColor.mouseReleased = self.wholePlantColorMouseUp
        self.colorDXFFromPlantPartType = JRadioButton('use colors based on type of part', font=buttonFont, margin=buttonMargin)
        self.colorDXFFromPlantPartType.setMnemonic(KeyEvent.VK_B)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.colorDXFFromPlantPartType)
        self.colorDXFFromPlantPartType.setBounds(9, 77, 182, 15)
        self.colorsByPlantPart = JList(DefaultListModel(), fixedCellHeight=16)
        self.colorsByPlantPart.setBounds(27, 95, 247, 52)
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsByPlantPart.Style = lbOwnerDrawFixed
        self.colorsByPlantPart.getModel().addElement("Meristems")
        self.colorsByPlantPart.getModel().addElement("Internodes")
        self.colorsByPlantPart.getModel().addElement("Leaves")
        self.colorsByPlantPart.getModel().addElement("First leaves")
        self.colorsByPlantPart.getModel().addElement("Flowers (F)")
        self.colorsByPlantPart.getModel().addElement("Flowers (M)")
        self.colorsByPlantPart.getModel().addElement("Inflor. (F)")
        self.colorsByPlantPart.getModel().addElement("Inflor. (M)")
        self.colorsByPlantPart.getModel().addElement("Fruit")
        self.colorsByPlantPart.getModel().addElement("Root top")
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsByPlantPart.MultiSelect = True
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsByPlantPart.OnDrawItem = colorsByPlantPartDrawItem
        #  --------------- UNHANDLED ATTRIBUTE: self.colorsByPlantPart.OnDblClick = colorsByPlantPartDblClick
        self.setPlantPartColor = JButton('Set...', actionPerformed=self.setPlantPartColorClick, font=buttonFont, margin=buttonMargin)
        self.setPlantPartColor.setMnemonic(KeyEvent.VK_S)
        self.setPlantPartColor.setBounds(221, 71, 53, 22)
        self.dxfWriteColors = JCheckBox('Write colors', actionPerformed=self.dxfWriteColorsClick, font=buttonFont, margin=buttonMargin)
        self.dxfWriteColors.setMnemonic(KeyEvent.VK_C)
        self.dxfWriteColors.setBounds(10, 16, 101, 17)
        self.dxfColorsGroupBox = JPanel(layout=None)
        # -- self.dxfColorsGroupBox.setLayout(BoxLayout(self.dxfColorsGroupBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.dxfColorsGroupBox.border = TitledBorder("' Colors '")
        self.dxfColorsGroupBox.add(self.colorDXFFromRGB)
        self.dxfColorsGroupBox.add(self.colorDXFFromOneColor)
        self.dxfColorsGroupBox.add(self.wholePlantColor)
        self.dxfColorsGroupBox.add(self.colorDXFFromPlantPartType)
        scroller = JScrollPane(self.colorsByPlantPart)
        scroller.setBounds(27, 95, 247, 52)
        self.dxfColorsGroupBox.add(scroller)
        self.dxfColorsGroupBox.add(self.setPlantPartColor)
        self.dxfColorsGroupBox.add(self.dxfWriteColors)
        self.dxfColorsGroupBox.setBounds(290, 91, 280, 152)
        self.dxfColorsGroupBox.visible = 0
        self.minLineLengthToWrite = JTextField("", 10)
        self.minLineLengthToWrite.setBounds(17, 19, 51, 22)
        self.Label4 = JLabel('Keep lines at least this long (mm)', displayedMnemonic=KeyEvent.VK_K, labelFor=self.minLineLengthToWrite, font=buttonFont)
        self.Label4.setBounds(72, 23, 158, 14)
        self.minTdoScaleToWrite = JTextField("", 10)
        self.minTdoScaleToWrite.setBounds(17, 45, 51, 22)
        self.Label5 = JLabel('Keep 3D objects of at least this scale', displayedMnemonic=KeyEvent.VK_3, labelFor=self.minTdoScaleToWrite, font=buttonFont)
        self.Label5.setBounds(72, 49, 179, 14)
        self.povLimitsGroupBox = JPanel(layout=None)
        # -- self.povLimitsGroupBox.setLayout(BoxLayout(self.povLimitsGroupBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.povLimitsGroupBox.border = TitledBorder("' Limit small lines and 3D objects '")
        self.povLimitsGroupBox.add(self.minLineLengthToWrite)
        self.povLimitsGroupBox.add(self.Label4)
        self.povLimitsGroupBox.add(self.minTdoScaleToWrite)
        self.povLimitsGroupBox.add(self.Label5)
        self.povLimitsGroupBox.setBounds(290, 449, 280, 74)
        self.povLimitsGroupBox.visible = 0
        self.nestLeafAndPetiole = JCheckBox('leaves with petioles', font=buttonFont, margin=buttonMargin)
        self.nestLeafAndPetiole.setMnemonic(KeyEvent.VK_P)
        self.nestLeafAndPetiole.setBounds(17, 18, 122, 17)
        self.nestCompoundLeaf = JCheckBox('compound leaves', font=buttonFont, margin=buttonMargin)
        self.nestCompoundLeaf.setMnemonic(KeyEvent.VK_C)
        self.nestCompoundLeaf.setBounds(17, 37, 119, 17)
        self.nestInflorescence = JCheckBox('inflorescences', font=buttonFont, margin=buttonMargin)
        self.nestInflorescence.setMnemonic(KeyEvent.VK_I)
        self.nestInflorescence.setBounds(17, 55, 97, 17)
        self.nestPedicelAndFlowerFruit = JCheckBox('flowers with pedicels', font=buttonFont, margin=buttonMargin)
        self.nestPedicelAndFlowerFruit.setMnemonic(KeyEvent.VK_F)
        self.nestPedicelAndFlowerFruit.setBounds(142, 18, 130, 17)
        self.nestFloralLayers = JCheckBox('pistils and stamens', font=buttonFont, margin=buttonMargin)
        self.nestFloralLayers.setMnemonic(KeyEvent.VK_M)
        self.nestFloralLayers.setBounds(142, 36, 118, 17)
        self.commentOutUnionAtEnd = JCheckBox('Comment out union of plants at end', font=buttonFont, margin=buttonMargin)
        self.commentOutUnionAtEnd.setMnemonic(KeyEvent.VK_U)
        self.commentOutUnionAtEnd.setBounds(17, 77, 207, 18)
        self.nestingGroupBox = JPanel(layout=None)
        # -- self.nestingGroupBox.setLayout(BoxLayout(self.nestingGroupBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.nestingGroupBox.border = TitledBorder("' Nest '")
        self.nestingGroupBox.add(self.nestLeafAndPetiole)
        self.nestingGroupBox.add(self.nestCompoundLeaf)
        self.nestingGroupBox.add(self.nestInflorescence)
        self.nestingGroupBox.add(self.nestPedicelAndFlowerFruit)
        self.nestingGroupBox.add(self.nestFloralLayers)
        self.nestingGroupBox.add(self.commentOutUnionAtEnd)
        self.nestingGroupBox.setBounds(290, 246, 280, 100)
        self.nestingGroupBox.visible = 0
        #  ------- UNHANDLED TYPE TRadioGroup: layeringOption 
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.Caption = ' Group by '
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.Ctl3D = True
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.ParentCtl3D = False
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.Top = 81
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.Height = 75
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.Width = 280
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.TabOrder = 5
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.Items.Strings = ['&whole plant', '&type of plant part', 'individual plant &part']
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.ItemIndex = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.layeringOption.Left = 4
        self.Close = JButton('Save', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.Close.setMnemonic(KeyEvent.VK_S)
        self.Close.setBounds(290, 4, 60, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(290, 27, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.Label6 = JLabel('Note: This version of the 3DS export function does not import equally well to all 3D programs. See the help system for tips on improving 3DS compatibility.', font=buttonFont)
        self.Label6.setBounds(7, 4, 265, 42)
        self.threeDSWarningPanel = JPanel(layout=None)
        # -- self.threeDSWarningPanel.setLayout(BoxLayout(self.threeDSWarningPanel, BoxLayout.Y_AXIS))
        self.threeDSWarningPanel.add(self.Label6)
        self.threeDSWarningPanel.setBounds(290, 394, 280, 52)
        self.threeDSWarningPanel.visible = 0
        self.Label10 = JLabel('degrees (-180 to 180)', font=buttonFont)
        self.Label10.setBounds(124, 19, 106, 14)
        self.Label1 = JLabel('Rotate by', font=buttonFont)
        self.Label1.setBounds(10, 19, 46, 14)
        self.Label9 = JLabel('percent (1-10,000)', font=buttonFont)
        self.Label9.setBounds(124, 45, 91, 14)
        self.Label7 = JLabel('Scale by', font=buttonFont)
        self.Label7.setBounds(10, 45, 42, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.xRotationBeforeDraw = JSpinner(SpinnerNumberModel(0, -180, 180, 5))
        self.xRotationBeforeDraw.setBounds(62, 15, 57, 23)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.overallScalingFactor_pct = JSpinner(SpinnerNumberModel(10000, 1, 10000, 5))
        self.overallScalingFactor_pct.setBounds(62, 41, 57, 23)
        self.reorientGroupBox = JPanel(layout=None)
        # -- self.reorientGroupBox.setLayout(BoxLayout(self.reorientGroupBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.reorientGroupBox.border = TitledBorder("' Reorient '")
        self.reorientGroupBox.add(self.Label10)
        self.reorientGroupBox.add(self.Label1)
        self.reorientGroupBox.add(self.Label9)
        self.reorientGroupBox.add(self.Label7)
        self.reorientGroupBox.add(self.xRotationBeforeDraw)
        self.reorientGroupBox.add(self.overallScalingFactor_pct)
        self.reorientGroupBox.setBounds(4, 158, 281, 70)
        self.useSelectedPlants = JRadioButton('selected plants', actionPerformed=self.useSelectedPlantsClick, font=buttonFont, margin=buttonMargin)
        self.useSelectedPlants.setMnemonic(KeyEvent.VK_L)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useSelectedPlants)
        self.useSelectedPlants.setBounds(8, 16, 96, 17)
        self.useVisiblePlants = JRadioButton('visible plants', actionPerformed=self.useVisiblePlantsClick, font=buttonFont, margin=buttonMargin)
        self.useVisiblePlants.setMnemonic(KeyEvent.VK_V)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useVisiblePlants)
        self.useVisiblePlants.setBounds(107, 16, 82, 17)
        self.useAllPlants = JRadioButton('all plants', actionPerformed=self.useAllPlantsClick, font=buttonFont, margin=buttonMargin)
        self.useAllPlants.setMnemonic(KeyEvent.VK_A)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useAllPlants)
        self.useAllPlants.setBounds(206, 16, 65, 17)
        #  ------- UNHANDLED TYPE TStringGrid: estimationStringGrid 
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.ParentCtl3D = False
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Top = 35
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Font.Name = 'Arial'
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Width = 270
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.ColCount = 6
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.ColWidths = ['', '', '', '', '', '']
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.DefaultRowHeight = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.FixedRows = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Font.Height = -11
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.ParentFont = False
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.ScrollBars = ssNone
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Options = [goFixedVertLine, goFixedHorzLine, goDrawFocusSelected]
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Font.Color = clBlue
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Left = 5
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Font.Charset = DEFAULT_CHARSET
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Font.Style = []
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Ctl3D = False
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Color = clBtnFace
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.DefaultColWidth = 42
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.Height = 35
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.RowCount = 3
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.TabOrder = 3
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.FixedColor = clBtnHighlight
        #  --------------- UNHANDLED ATTRIBUTE: self.estimationStringGrid.FixedCols = 0
        self.drawWhichPlantsGroupBox = JPanel(layout=None)
        # -- self.drawWhichPlantsGroupBox.setLayout(BoxLayout(self.drawWhichPlantsGroupBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.drawWhichPlantsGroupBox.border = TitledBorder("' Include '")
        self.drawWhichPlantsGroupBox.add(self.useSelectedPlants)
        self.drawWhichPlantsGroupBox.add(self.useVisiblePlants)
        self.drawWhichPlantsGroupBox.add(self.useAllPlants)
        # FIX UNHANDLED TYPE -- self.drawWhichPlantsGroupBox.add(self.estimationStringGrid)
        self.drawWhichPlantsGroupBox.setBounds(4, 4, 280, 76)
        #  ------- UNHANDLED TYPE TRadioGroup: vrmlVersionRadioGroup 
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Caption = ' Version '
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.ParentCtl3D = False
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Top = 351
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Ctl3D = True
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Height = 38
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Width = 280
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.TabOrder = 10
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Items.Strings = ['VRML &1.0', 'VRML &2.0 (VRML 97)']
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.ItemIndex = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Visible = False
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Columns = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.vrmlVersionRadioGroup.Left = 290
        contentPane.add(self.helpButton)
        contentPane.add(self.otherGroupBox)
        contentPane.add(self.dxfColorsGroupBox)
        contentPane.add(self.povLimitsGroupBox)
        contentPane.add(self.nestingGroupBox)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        contentPane.add(self.threeDSWarningPanel)
        contentPane.add(self.reorientGroupBox)
        contentPane.add(self.drawWhichPlantsGroupBox)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def dxfWriteColorsClick(self, event):
        print "dxfWriteColorsClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def setPlantPartColorClick(self, event):
        print "setPlantPartColorClick"
        
    def useAllPlantsClick(self, event):
        print "useAllPlantsClick"
        
    def useSelectedPlantsClick(self, event):
        print "useSelectedPlantsClick"
        
    def useVisiblePlantsClick(self, event):
        print "useVisiblePlantsClick"
        
    def wholePlantColorMouseUp(self, event):
        print "wholePlantColorMouseUp"
        
if __name__ == "__main__":
    window = Generic3DOptionsWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
