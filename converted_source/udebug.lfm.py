from common import *

#Useage:
#        import DebugWindow
#        window = DebugWindow.DebugWindow()
#        window.visible = 1

class DebugWindow(JFrame):
    def __init__(self, title='Messages'):
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
        self.setBounds(365, 308, 427, 165  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.OnDestroy = FormDestroy
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.AutoScroll = False
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poDefaultPosOnly
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        
        self.helpButtonImage = toolkit.createImage("../resources/DebugForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(364, 99, 61, 25)
        self.DebugList = JList(DefaultListModel(), fixedCellHeight=14)
        self.DebugList.setBounds(-136, -110, 497, 249)
        self.Close = JButton('Close', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.Close.setMnemonic(KeyEvent.VK_C)
        self.getRootPane().setDefaultButton(self.Close)
        self.Close.setBounds(364, 4, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.Close.Cancel = True
        self.saveListAs = JButton('Save as...', actionPerformed=self.saveListAsClick, font=buttonFont, margin=buttonMargin)
        self.saveListAs.setMnemonic(KeyEvent.VK_S)
        self.saveListAs.setBounds(365, 39, 60, 21)
        self.clearList = JButton('Clear', actionPerformed=self.clearListClick, font=buttonFont, margin=buttonMargin)
        self.clearList.setMnemonic(KeyEvent.VK_L)
        self.clearList.setBounds(364, 63, 60, 21)
        self.exceptionLabel = JLabel('On message:', font=buttonFont)
        self.exceptionLabel.setBounds(8, 5, 64, 14)
        self.showOnExceptionCheckBox = JCheckBox('appear', actionPerformed=self.showOnExceptionCheckBoxClick, font=buttonFont, margin=buttonMargin)
        self.showOnExceptionCheckBox.setMnemonic(KeyEvent.VK_A)
        self.showOnExceptionCheckBox.setBounds(83, 5, 68, 17)
        self.logToFile = JCheckBox('log to file', actionPerformed=self.logToFileClick, font=buttonFont, margin=buttonMargin)
        self.logToFile.setMnemonic(KeyEvent.VK_O)
        self.logToFile.setBounds(146, 5, 77, 17)
        self.optionsPanel = JPanel(layout=None)
        # -- self.optionsPanel.setLayout(BoxLayout(self.optionsPanel, BoxLayout.Y_AXIS))
        self.optionsPanel.add(self.exceptionLabel)
        self.optionsPanel.add(self.showOnExceptionCheckBox)
        self.optionsPanel.add(self.logToFile)
        self.optionsPanel.setBounds(0, 140, 361, 25)
        self.supportButton = JButton('Info...', actionPerformed=self.supportButtonClick, font=buttonFont, margin=buttonMargin)
        self.supportButton.setMnemonic(KeyEvent.VK_I)
        self.supportButton.setBounds(364, 133, 60, 21)
        contentPane.add(self.helpButton)
        scroller = JScrollPane(self.DebugList)
        scroller.setBounds(-136, -110, 497, 249)
        contentPane.add(scroller)
        contentPane.add(self.Close)
        contentPane.add(self.saveListAs)
        contentPane.add(self.clearList)
        contentPane.add(self.optionsPanel)
        contentPane.add(self.supportButton)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def clearListClick(self, event):
        print "clearListClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def logToFileClick(self, event):
        print "logToFileClick"
        
    def saveListAsClick(self, event):
        print "saveListAsClick"
        
    def showOnExceptionCheckBoxClick(self, event):
        print "showOnExceptionCheckBoxClick"
        
    def supportButtonClick(self, event):
        print "supportButtonClick"
        
if __name__ == "__main__":
    window = DebugWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
