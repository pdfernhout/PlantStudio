from common import *

#Useage:
#        import WelcomeWindow
#        window = WelcomeWindow.WelcomeWindow()
#        window.visible = 1

class WelcomeWindow(JFrame):
    def __init__(self, title=' '):
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
        self.setBounds(375, 189, 247, 250  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = []
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.Label3 = JLabel(' What would you like to do first?', font=buttonFont)
        self.Label3.setBounds(42, 51, 155, 14)
        self.Label1 = JLabel(' Welcome to PlantStudio!', font=buttonFont)
        self.Label1.setBounds(9, 8, 136, 14)
        self.Image1Image = toolkit.createImage("../resources/WelcomeForm_Image1.png")
        self.Image1 = ImagePanel(ImageIcon(self.Image1Image))
        self.Image1.setBounds(3, 1, 241, 45)
        self.hideWelcomeForm = JCheckBox('Don''t show this window next time', font=buttonFont, margin=buttonMargin)
        self.hideWelcomeForm.setMnemonic(KeyEvent.VK_D)
        self.hideWelcomeForm.setBounds(29, 230, 190, 17)
        self.readQuickStartTipList = JButton('Read the Super-Speed Tour', actionPerformed=self.readQuickStartTipListClick, font=buttonFont, margin=buttonMargin)
        self.readQuickStartTipList.setMnemonic(KeyEvent.VK_S)
        self.readQuickStartTipList.setBounds(45, 73, 160, 25)
        self.readTutorial = JButton('Read the Tutorial', actionPerformed=self.readTutorialClick, font=buttonFont, margin=buttonMargin)
        self.readTutorial.setMnemonic(KeyEvent.VK_T)
        self.readTutorial.setBounds(45, 102, 160, 25)
        self.makeNewPlant = JButton('Make a New Plant', actionPerformed=self.makeNewPlantClick, font=buttonFont, margin=buttonMargin)
        self.makeNewPlant.setMnemonic(KeyEvent.VK_N)
        self.makeNewPlant.setBounds(45, 133, 160, 25)
        self.openPlantLibrary = JButton('Open a Plant Library', actionPerformed=self.openPlantLibraryClick, font=buttonFont, margin=buttonMargin)
        self.openPlantLibrary.setMnemonic(KeyEvent.VK_O)
        self.openPlantLibrary.setBounds(45, 162, 160, 25)
        self.startUsingProgram = JButton('Start Using the Program', actionPerformed=self.startUsingProgramClick, font=buttonFont, margin=buttonMargin)
        self.startUsingProgram.setMnemonic(KeyEvent.VK_U)
        self.startUsingProgram.setBounds(45, 191, 160, 25)
        contentPane.add(self.Label3)
        contentPane.add(self.Label1)
        contentPane.add(self.Image1)
        contentPane.add(self.hideWelcomeForm)
        contentPane.add(self.readQuickStartTipList)
        contentPane.add(self.readTutorial)
        contentPane.add(self.makeNewPlant)
        contentPane.add(self.openPlantLibrary)
        contentPane.add(self.startUsingProgram)
        
    def makeNewPlantClick(self, event):
        print "makeNewPlantClick"
        
    def openPlantLibraryClick(self, event):
        print "openPlantLibraryClick"
        
    def readQuickStartTipListClick(self, event):
        print "readQuickStartTipListClick"
        
    def readTutorialClick(self, event):
        print "readTutorialClick"
        
    def startUsingProgramClick(self, event):
        print "startUsingProgramClick"
        
if __name__ == "__main__":
    window = WelcomeWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
