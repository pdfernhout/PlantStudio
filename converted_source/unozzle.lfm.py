from common import *

#Useage:
#        import NozzleOptionsWindow
#        window = NozzleOptionsWindow.NozzleOptionsWindow()
#        window.visible = 1

class NozzleOptionsWindow(JFrame):
    def __init__(self, title='Save Nozzle/Tube Bitmap'):
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
        self.setBounds(521, 265, 350, 373  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.helpButtonImage = toolkit.createImage("../resources/NozzleOptionsForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(287, 61, 60, 21)
        self.cellCountLabel = JLabel('Number of items:  5', font=buttonFont)
        self.cellCountLabel.setBounds(7, 27, 93, 14)
        self.cellSizeLabel = JLabel('Nozzle/tube cell width:  345 height:  534', font=buttonFont)
        self.cellSizeLabel.setBounds(7, 11, 192, 14)
        self.fileSizeLabel = JLabel('Estimated file size:  2433 K', font=buttonFont)
        self.fileSizeLabel.setBounds(7, 42, 129, 14)
        self.GroupBox1 = JPanel(layout=None)
        # -- self.GroupBox1.setLayout(BoxLayout(self.GroupBox1, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox1.border = TitledBorder("Untitled Group")
        self.GroupBox1.add(self.cellCountLabel)
        self.GroupBox1.add(self.cellSizeLabel)
        self.GroupBox1.add(self.fileSizeLabel)
        self.GroupBox1.setBounds(2, 308, 279, 64)
        self.Close = JButton('Save', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.Close.setMnemonic(KeyEvent.VK_S)
        self.Close.setBounds(287, 2, 60, 21)
        self.cancel = JButton('Cancel', font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(287, 25, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.ModalResult = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.Label4 = JLabel('You are making a bitmap file to use to create a nozzle for the Painter Image Hose brush or a picture tube for Paint Shop Pro. You can use the nozzle or tube to "spray" your picture with plants. Click Help for instructions on using the bitmap file.', font=buttonFont)
        self.Label4.setBounds(6, 3, 261, 70)
        self.Panel1 = JPanel(layout=None)
        # -- self.Panel1.setLayout(BoxLayout(self.Panel1, BoxLayout.Y_AXIS))
        self.Panel1.add(self.Label4)
        self.Panel1.setBounds(2, 2, 279, 77)
        self.Label1 = JLabel('(Use a color not found in your plants.)', font=buttonFont)
        self.Label1.setBounds(55, 122, 183, 14)
        self.backgroundColorPanel = JPanel(layout=None)
        # -- self.backgroundColorPanel.setLayout(BoxLayout(self.backgroundColorPanel, BoxLayout.Y_AXIS))
        self.backgroundColorPanel.setBounds(29, 119, 20, 20)
        self.backgroundColorPanel.mouseClicked = self.backgroundColorPanelClick
        self.Label3 = JLabel('Background color', displayedMnemonic=KeyEvent.VK_C, labelFor=self.backgroundColorPanel, font=buttonFont)
        self.Label3.setBounds(10, 102, 85, 14)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.resolutionEdit = JSpinner(SpinnerNumberModel(10, 10, 10000, 10))
        self.resolutionEdit.setBounds(29, 75, 60, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.resolutionEdit.OnChange = resolutionEditChange
        self.resolutionLabel = JLabel('Resolution (pixels/inch)', displayedMnemonic=KeyEvent.VK_R, labelFor=self.resolutionEdit, font=buttonFont)
        self.resolutionLabel.setBounds(10, 60, 112, 14)
        self.colorType = JComboBox(DefaultComboBoxModel())
        self.colorType.setBounds(29, 36, 155, 19)
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
        #  --------------- UNHANDLED ATTRIBUTE: self.colorType.ItemHeight = 13
        self.colorsLabel = JLabel('Color depth', displayedMnemonic=KeyEvent.VK_D, labelFor=self.colorType, font=buttonFont)
        self.colorsLabel.setBounds(10, 19, 55, 14)
        self.GroupBox2 = JPanel(layout=None)
        # -- self.GroupBox2.setLayout(BoxLayout(self.GroupBox2, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox2.border = TitledBorder("'Nozzle/Tube options'")
        self.GroupBox2.add(self.Label1)
        self.GroupBox2.add(self.backgroundColorPanel)
        self.GroupBox2.add(self.Label3)
        self.GroupBox2.add(self.resolutionEdit)
        self.GroupBox2.add(self.resolutionLabel)
        self.GroupBox2.add(self.colorType)
        self.GroupBox2.add(self.colorsLabel)
        self.GroupBox2.setBounds(2, 162, 279, 147)
        self.useSelectedPlants = JRadioButton('selected', actionPerformed=self.changeSelection, font=buttonFont, margin=buttonMargin)
        self.useSelectedPlants.setMnemonic(KeyEvent.VK_L)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useSelectedPlants)
        self.useSelectedPlants.setBounds(17, 18, 66, 17)
        self.useVisiblePlants = JRadioButton('visible', actionPerformed=self.changeSelection, font=buttonFont, margin=buttonMargin)
        self.useVisiblePlants.setMnemonic(KeyEvent.VK_V)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useVisiblePlants)
        self.useVisiblePlants.setBounds(17, 35, 54, 17)
        self.useAllPlants = JRadioButton('all', actionPerformed=self.changeSelection, font=buttonFont, margin=buttonMargin)
        self.useAllPlants.setMnemonic(KeyEvent.VK_A)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.useAllPlants)
        self.useAllPlants.setBounds(17, 52, 36, 17)
        self.GroupBox3 = JPanel(layout=None)
        # -- self.GroupBox3.setLayout(BoxLayout(self.GroupBox3, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox3.border = TitledBorder("'Draw which plants?'")
        self.GroupBox3.add(self.useSelectedPlants)
        self.GroupBox3.add(self.useVisiblePlants)
        self.GroupBox3.add(self.useAllPlants)
        self.GroupBox3.setBounds(2, 82, 279, 76)
        #  ------- UNHANDLED TYPE TColorDialog: ColorDialog 
        #  --------------- UNHANDLED ATTRIBUTE: self.ColorDialog.Top = 112
        #  --------------- UNHANDLED ATTRIBUTE: self.ColorDialog.Left = 306
        #  --------------- UNHANDLED ATTRIBUTE: self.ColorDialog.Ctl3D = True
        contentPane.add(self.helpButton)
        contentPane.add(self.GroupBox1)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        contentPane.add(self.Panel1)
        contentPane.add(self.GroupBox2)
        contentPane.add(self.GroupBox3)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def backgroundColorPanelClick(self, event):
        print "backgroundColorPanelClick"
        
    def changeSelection(self, event):
        print "changeSelection"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
if __name__ == "__main__":
    window = NozzleOptionsWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
