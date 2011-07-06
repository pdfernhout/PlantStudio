from common import *

#Useage:
#        import ProgramInfoWindow
#        window = ProgramInfoWindow.ProgramInfoWindow()
#        window.visible = 1

class ProgramInfoWindow(JFrame):
    def __init__(self, title='Program Information'):
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
        self.setBounds(310, 266, 450, 301  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 13
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.AutoScroll = False
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        
        self.helpButtonImage = toolkit.createImage("../resources/ProgramInfoForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(332, 135, 113, 25)
        self.Close = JButton('Close', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.Close.setMnemonic(KeyEvent.VK_C)
        self.Close.setBounds(332, 4, 113, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.Close.Cancel = True
        self.saveListAs = JButton('Save as...', actionPerformed=self.saveListAsClick, font=buttonFont, margin=buttonMargin)
        self.saveListAs.setMnemonic(KeyEvent.VK_S)
        self.saveListAs.setBounds(332, 83, 113, 21)
        self.copyToClipboard = JButton('Copy to Clipboard', actionPerformed=self.copyToClipboardClick, font=buttonFont, margin=buttonMargin)
        self.copyToClipboard.setMnemonic(KeyEvent.VK_P)
        self.copyToClipboard.setBounds(332, 55, 113, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.copyToClipboard.Cancel = True
        self.infoList = JTextArea(10, 10)
        self.infoList.setBounds(2, 2, 323, 295)
        #  --------------- UNHANDLED ATTRIBUTE: self.infoList.ScrollBars = ssVertical
        contentPane.add(self.helpButton)
        contentPane.add(self.Close)
        contentPane.add(self.saveListAs)
        contentPane.add(self.copyToClipboard)
        scroller = JScrollPane(self.infoList)
        scroller.setBounds(2, 2, 323, 295)
        contentPane.add(scroller)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def copyToClipboardClick(self, event):
        print "copyToClipboardClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def saveListAsClick(self, event):
        print "saveListAsClick"
        
if __name__ == "__main__":
    window = ProgramInfoWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
