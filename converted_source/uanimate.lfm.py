from common import *

#Useage:
#        import AnimationFilesOptionsWindow
#        window = AnimationFilesOptionsWindow.AnimationFilesOptionsWindow()
#        window.visible = 1

class AnimationFilesOptionsWindow(JFrame):
    def __init__(self, title='Save Animation Files'):
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
        self.setBounds(500, 298, 328, 364  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.helpButtonImage = toolkit.createImage("../resources/AnimationFilesOptionsForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(265, 62, 60, 21)
        self.Close = JButton('Save', font=buttonFont, margin=buttonMargin)
        self.Close.setMnemonic(KeyEvent.VK_S)
        self.Close.setBounds(265, 2, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.Close.ModalResult = 1
        self.cancel = JButton('Cancel', font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(265, 25, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.ModalResult = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.fileNumberLabel = JLabel('Number of files:  5', font=buttonFont)
        self.fileNumberLabel.setBounds(8, 26, 88, 14)
        self.animationSizeLabel = JLabel('Animation size:  243 x 232', font=buttonFont)
        self.animationSizeLabel.setBounds(8, 8, 127, 14)
        self.fileSizeLabel = JLabel('Estimated total file size:  25343 K', font=buttonFont)
        self.fileSizeLabel.setBounds(8, 44, 158, 14)
        self.Panel1 = JPanel(layout=None)
        # -- self.Panel1.setLayout(BoxLayout(self.Panel1, BoxLayout.Y_AXIS))
        self.Panel1.add(self.fileNumberLabel)
        self.Panel1.add(self.animationSizeLabel)
        self.Panel1.add(self.fileSizeLabel)
        self.Panel1.setBounds(2, 296, 259, 66)
        self.Label4 = JLabel('You are creating numbered animation files from the focused plant', font=buttonFont)
        self.Label4.setBounds(6, 5, 231, 28)
        self.focusedPlantName = JLabel('sunflower', font=buttonFont)
        self.focusedPlantName.setBounds(24, 34, 50, 14)
        self.Label5 = JLabel('for use in an animation programs. Click Help for instructions on using the numbered files.', font=buttonFont)
        self.Label5.setBounds(7, 49, 213, 28)
        self.Panel2 = JPanel(layout=None)
        # -- self.Panel2.setLayout(BoxLayout(self.Panel2, BoxLayout.Y_AXIS))
        self.Panel2.add(self.Label4)
        self.Panel2.add(self.focusedPlantName)
        self.Panel2.add(self.Label5)
        self.Panel2.setBounds(2, 2, 259, 82)
        self.Label1 = JLabel('Animate by changing', font=buttonFont)
        self.Label1.setBounds(8, 20, 101, 14)
        self.resolutionLabel = JLabel('Resolution (pixels/inch)', displayedMnemonic=KeyEvent.VK_R, font=buttonFont)
        self.resolutionLabel.setBounds(8, 160, 112, 14)
        self.incrementLabel = JLabel('Rotation increment between frames (degrees)', displayedMnemonic=KeyEvent.VK_F, font=buttonFont)
        self.incrementLabel.setBounds(8, 76, 223, 14)
        self.plantMaxAgeLabel = JLabel('Maximum age = 100', font=buttonFont)
        self.plantMaxAgeLabel.setBounds(85, 97, 95, 14)
        self.animateByAge = JRadioButton('plant age', actionPerformed=self.animateByAgeClick, font=buttonFont, margin=buttonMargin)
        self.animateByAge.setMnemonic(KeyEvent.VK_A)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.animateByAge)
        self.animateByAge.setBounds(20, 35, 113, 17)
        self.animateByXRotation = JRadioButton('X rotation', actionPerformed=self.animateByXRotationClick, font=buttonFont, margin=buttonMargin)
        self.animateByXRotation.setMnemonic(KeyEvent.VK_X)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.animateByXRotation)
        self.animateByXRotation.setBounds(20, 53, 113, 17)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.incrementEdit = JSpinner(SpinnerNumberModel(0, -360, 360, 1))
        self.incrementEdit.setBounds(20, 94, 61, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.incrementEdit.OnChange = incrementEditChange
        # -- supposed to be a spin edit, not yet fuly implemented
        self.resolution = JSpinner(SpinnerNumberModel(10, 10, 10000, 10))
        self.resolution.setBounds(20, 177, 61, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.resolution.OnChange = resolutionChange
        self.colorType = JComboBox(DefaultComboBoxModel())
        self.colorType.setBounds(20, 137, 155, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.colorType.Style = csOwnerDrawFixed
        self.colorType.getModel().addElement("From screen")
        self.colorType.getModel().addElement("2 colors (1-bit)")
        self.colorType.getModel().addElement("16 colors (4-bit)")
        self.colorType.getModel().addElement("256 colors (8-bit)")
        self.colorType.getModel().addElement("32768 colors (15-bit)")
        self.colorType.getModel().addElement("65536 colors (16-bit)")
        self.colorType.getModel().addElement("16 million colors (24-bit)")
        self.colorType.getModel().addElement("4.3 billion colors (32-bit)")
        #  --------------- UNHANDLED ATTRIBUTE: self.colorType.OnChange = colorTypeChange
        #  --------------- UNHANDLED ATTRIBUTE: self.colorType.ItemHeight = 13
        self.colorsLabel = JLabel('Color depth', displayedMnemonic=KeyEvent.VK_D, labelFor=self.colorType, font=buttonFont)
        self.colorsLabel.setBounds(8, 120, 55, 14)
        self.GroupBox1 = JPanel(layout=None)
        # -- self.GroupBox1.setLayout(BoxLayout(self.GroupBox1, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox1.border = TitledBorder("'Animation options'")
        self.GroupBox1.add(self.Label1)
        self.GroupBox1.add(self.resolutionLabel)
        self.GroupBox1.add(self.incrementLabel)
        self.GroupBox1.add(self.plantMaxAgeLabel)
        self.GroupBox1.add(self.animateByAge)
        self.GroupBox1.add(self.animateByXRotation)
        self.GroupBox1.add(self.incrementEdit)
        self.GroupBox1.add(self.resolution)
        self.GroupBox1.add(self.colorType)
        self.GroupBox1.add(self.colorsLabel)
        self.GroupBox1.setBounds(2, 86, 259, 207)
        contentPane.add(self.helpButton)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        contentPane.add(self.Panel1)
        contentPane.add(self.Panel2)
        contentPane.add(self.GroupBox1)
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def animateByAgeClick(self, event):
        print "animateByAgeClick"
        
    def animateByXRotationClick(self, event):
        print "animateByXRotationClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
if __name__ == "__main__":
    window = AnimationFilesOptionsWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
