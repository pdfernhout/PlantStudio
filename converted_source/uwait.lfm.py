from common import *

#Useage:
#        import WaitWindow
#        window = WaitWindow.WaitWindow()
#        window.visible = 1

class WaitWindow(JFrame):
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
        self.setBounds(388, 293, 339, 54  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = []
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsNone
        
        self.messageLabel = JLabel('saving file...', font=buttonFont)
        self.messageLabel.setBounds(76, 19, 58, 14)
        #  --------------- UNHANDLED ATTRIBUTE: self.messageLabel.Alignment = taCenter
        self.Image1Image = toolkit.createImage("../resources/WaitForm_Image1.png")
        self.Image1 = ImagePanel(ImageIcon(self.Image1Image))
        self.Image1.setBounds(4, 4, 64, 44)
        self.Panel1 = JPanel(layout=None)
        # -- self.Panel1.setLayout(BoxLayout(self.Panel1, BoxLayout.Y_AXIS))
        self.Panel1.add(self.messageLabel)
        self.Panel1.add(self.Image1)
        self.Panel1.setBounds(0, 0, 339, 54)
        contentPane.add(self.Panel1)
        
if __name__ == "__main__":
    window = WaitWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
