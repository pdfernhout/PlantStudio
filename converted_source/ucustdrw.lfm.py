from common import *

#Useage:
#        import CustomDrawOptionsWindow
#        window = CustomDrawOptionsWindow.CustomDrawOptionsWindow()
#        window.visible = 1

class CustomDrawOptionsWindow(JFrame):
    def __init__(self, title='Custom Draw Options'):
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
        self.setBounds(618, 244, 290, 217  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.helpButtonImage = toolkit.createImage("../resources/CustomDrawOptionsForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(227, 63, 61, 25)
        self.Close = JButton('OK', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.Close.setMnemonic(KeyEvent.VK_O)
        self.Close.setBounds(228, 4, 60, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(228, 27, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.sortPolygons = JCheckBox('Sort polygons', actionPerformed=self.sortPolygonsClick, font=buttonFont, margin=buttonMargin)
        self.sortPolygons.setMnemonic(KeyEvent.VK_R)
        self.sortPolygons.setBounds(10, 14, 97, 17)
        self.sortTdosAsOneItem = JCheckBox('Sort 3D objects as one item', font=buttonFont, margin=buttonMargin)
        self.sortTdosAsOneItem.setMnemonic(KeyEvent.VK_N)
        self.sortTdosAsOneItem.setBounds(10, 32, 157, 17)
        self.GroupBox1 = JPanel(layout=None)
        # -- self.GroupBox1.setLayout(BoxLayout(self.GroupBox1, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox1.border = TitledBorder("'Sorting'")
        self.GroupBox1.add(self.sortPolygons)
        self.GroupBox1.add(self.sortTdosAsOneItem)
        self.GroupBox1.setBounds(4, 158, 219, 55)
        self.fillPolygons = JCheckBox('Fill polygons', actionPerformed=self.fillPolygonsClick, font=buttonFont, margin=buttonMargin)
        self.fillPolygons.setMnemonic(KeyEvent.VK_P)
        self.fillPolygons.setBounds(10, 16, 97, 17)
        self.drawLinesBetweenPolygons = JCheckBox('Draw lines between polygons', actionPerformed=self.drawLinesBetweenPolygonsClick, font=buttonFont, margin=buttonMargin)
        self.drawLinesBetweenPolygons.setMnemonic(KeyEvent.VK_L)
        self.drawLinesBetweenPolygons.setBounds(10, 32, 167, 17)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.lineContrastIndex = JSpinner(SpinnerNumberModel(10, 0, 10, 1))
        self.lineContrastIndex.setBounds(10, 51, 40, 22)
        self.lineContrastIndexLabel = JLabel('Line contrast index (0-10)', displayedMnemonic=KeyEvent.VK_C, labelFor=self.lineContrastIndex, font=buttonFont)
        self.lineContrastIndexLabel.setBounds(55, 54, 125, 14)
        self.GroupBox2 = JPanel(layout=None)
        # -- self.GroupBox2.setLayout(BoxLayout(self.GroupBox2, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox2.border = TitledBorder("'Filling'")
        self.GroupBox2.add(self.fillPolygons)
        self.GroupBox2.add(self.drawLinesBetweenPolygons)
        self.GroupBox2.add(self.lineContrastIndex)
        self.GroupBox2.add(self.lineContrastIndexLabel)
        self.GroupBox2.setBounds(4, 76, 219, 81)
        self.draw3DObjects = JCheckBox('Draw 3D objects', actionPerformed=self.draw3DObjectsClick, font=buttonFont, margin=buttonMargin)
        self.draw3DObjects.setMnemonic(KeyEvent.VK_3)
        self.draw3DObjects.setBounds(8, 32, 117, 17)
        self.drawStems = JCheckBox('Draw stems', font=buttonFont, margin=buttonMargin)
        self.drawStems.setMnemonic(KeyEvent.VK_S)
        self.drawStems.setBounds(8, 15, 97, 17)
        self.draw3DObjectsAsBoundingRectsOnly = JCheckBox('Draw 3D object bounding boxes only', font=buttonFont, margin=buttonMargin)
        self.draw3DObjectsAsBoundingRectsOnly.setMnemonic(KeyEvent.VK_B)
        self.draw3DObjectsAsBoundingRectsOnly.setBounds(8, 49, 203, 17)
        self.GroupBox3 = JPanel(layout=None)
        # -- self.GroupBox3.setLayout(BoxLayout(self.GroupBox3, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.GroupBox3.border = TitledBorder("'Drawing'")
        self.GroupBox3.add(self.draw3DObjects)
        self.GroupBox3.add(self.drawStems)
        self.GroupBox3.add(self.draw3DObjectsAsBoundingRectsOnly)
        self.GroupBox3.setBounds(4, 4, 219, 72)
        contentPane.add(self.helpButton)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        contentPane.add(self.GroupBox1)
        contentPane.add(self.GroupBox2)
        contentPane.add(self.GroupBox3)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def draw3DObjectsClick(self, event):
        print "draw3DObjectsClick"
        
    def drawLinesBetweenPolygonsClick(self, event):
        print "drawLinesBetweenPolygonsClick"
        
    def fillPolygonsClick(self, event):
        print "fillPolygonsClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def sortPolygonsClick(self, event):
        print "sortPolygonsClick"
        
if __name__ == "__main__":
    window = CustomDrawOptionsWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
