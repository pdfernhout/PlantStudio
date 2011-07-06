from common import *

#Useage:
#        import SplashWindow
#        window = SplashWindow.SplashWindow()
#        window.visible = 1

class SplashWindow(JFrame):
    def __init__(self, title='FIX WINDOW TITLE'):
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
        self.setBounds(349, 213, 379, 269  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = []
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsNone
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        self.keyTyped = self.FormKeyPress
        self.keyPressed = self.FormKeyDown
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        self.mousePressed = self.FormMouseDown
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        self.mouseClicked = self.FormClick
        
        self.splashImage256ColorsImage = toolkit.createImage("../resources/SplashForm_splashImage256Colors.png")
        self.splashImage256Colors = ImagePanel(ImageIcon(self.splashImage256ColorsImage))
        self.splashImage256Colors.setBounds(0, 0, 382, 270)
        self.splashImage256Colors.visible = 0
        self.splashImage256Colors.mouseClicked = self.splashImage256ColorsClick
        self.versionLabel = JLabel('version 0.1', font=buttonFont)
        self.versionLabel.setBounds(13, 81, 68, 16)
        self.versionLabel.mouseClicked = self.controlClick
        self.loadingLabel = JLabel('Registered to:', font=buttonFont)
        self.loadingLabel.setBounds(33, 107, 88, 16)
        self.loadingLabel.mouseClicked = self.controlClick
        self.codeLabel = JLabel('Name', font=buttonFont)
        self.codeLabel.setBounds(127, 107, 37, 16)
        self.codeLabel.visible = 0
        self.codeLabel.mouseClicked = self.controlClick
        self.splashImageTrueColorImage = toolkit.createImage("../resources/SplashForm_splashImageTrueColor.png")
        self.splashImageTrueColor = ImagePanel(ImageIcon(self.splashImageTrueColorImage))
        self.splashImageTrueColor.setBounds(109, -167, 382, 270)
        self.splashImageTrueColor.visible = 0
        self.splashImageTrueColor.mouseClicked = self.splashImage256ColorsClick
        self.closeImage = toolkit.createImage("../resources/SplashForm_close.png")
        self.close = SpeedButton(ImageIcon(self.closeImage), actionPerformed=self.closeClick, font=buttonFont, margin=buttonMargin)
        self.close.setBounds(274, 134, 92, 29)
        #  --------------- UNHANDLED ATTRIBUTE: self.close.Flat = True
        self.close.visible = 0
        self.supportButtonImage = toolkit.createImage("../resources/SplashForm_supportButton.png")
        self.supportButton = SpeedButton(ImageIcon(self.supportButtonImage), actionPerformed=self.supportButtonClick, font=buttonFont, margin=buttonMargin)
        self.supportButton.setBounds(274, 171, 92, 26)
        #  --------------- UNHANDLED ATTRIBUTE: self.supportButton.Flat = True
        self.supportButton.visible = 0
        contentPane.add(self.splashImage256Colors)
        contentPane.add(self.versionLabel)
        contentPane.add(self.loadingLabel)
        contentPane.add(self.codeLabel)
        contentPane.add(self.splashImageTrueColor)
        contentPane.add(self.close)
        contentPane.add(self.supportButton)
        
    def FormClick(self, event):
        print "FormClick"
        
    def FormKeyDown(self, event):
        print "FormKeyDown"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def FormMouseDown(self, event):
        print "FormMouseDown"
        
    def closeClick(self, event):
        print "closeClick"
        
    def controlClick(self, event):
        print "controlClick"
        
    def splashImage256ColorsClick(self, event):
        print "splashImage256ColorsClick"
        
    def supportButtonClick(self, event):
        print "supportButtonClick"
        
if __name__ == "__main__":
    window = SplashWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
