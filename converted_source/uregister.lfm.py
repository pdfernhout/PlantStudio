from common import *

#Useage:
#        import RegistrationWindow
#        window = RegistrationWindow.RegistrationWindow()
#        window.visible = 1

class RegistrationWindow(JFrame):
    def __init__(self, title='PlantStudio Registration'):
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
        self.setBounds(296, 154, 436, 255  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCloseQuery = FormCloseQuery
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        
        self.Label11 = JLabel('Enter your registration name and personalized registration code below, EXACTLY as they appear in the confirmation you received.', font=buttonFont)
        self.Label11.setBounds(8, 129, 320, 28)
        self.Label1 = JLabel('To purchase a registration code, go to our web site at:', font=buttonFont)
        self.Label1.setBounds(8, 11, 263, 14)
        self.Label2 = JLabel('and follow the directions there.', font=buttonFont)
        self.Label2.setBounds(8, 53, 150, 14)
        self.Label5 = JLabel('(Clicking ''Open browser'' may not work depending on your system setup. If it doesn''t, open your browser yourself, copy the address above, and paste it into the address area of your browser.)', font=buttonFont)
        self.Label5.setBounds(8, 77, 322, 42)
        self.Label6 = JLabel('Then click here ----->', font=buttonFont)
        self.Label6.setBounds(65, 231, 102, 14)
        self.registrationNameEdit = JTextField("", 10)
        self.registrationNameEdit.setBounds(101, 7, 222, 22)
        self.Label3 = JLabel('Registration Name', displayedMnemonic=KeyEvent.VK_N, labelFor=self.registrationNameEdit, font=buttonFont)
        self.Label3.setBounds(8, 9, 87, 14)
        #  --------------- UNHANDLED ATTRIBUTE: self.Label3.Alignment = taRightJustify
        self.registrationCodeEdit = JTextField("", 10)
        self.registrationCodeEdit.setBounds(101, 31, 222, 22)
        self.Label4 = JLabel('Registration Code', displayedMnemonic=KeyEvent.VK_D, labelFor=self.registrationCodeEdit, font=buttonFont)
        self.Label4.setBounds(10, 33, 85, 14)
        #  --------------- UNHANDLED ATTRIBUTE: self.Label4.Alignment = taRightJustify
        self.Panel1 = JPanel(layout=None)
        # -- self.Panel1.setLayout(BoxLayout(self.Panel1, BoxLayout.Y_AXIS))
        self.Panel1.add(self.registrationNameEdit)
        self.Panel1.add(self.Label3)
        self.Panel1.add(self.registrationCodeEdit)
        self.Panel1.add(self.Label4)
        self.Panel1.setBounds(8, 159, 328, 59)
        self.orderPageEdit = JTextField('http://www.kurtz-fernhout.com/order.htm', 10, editable=0)
        self.orderPageEdit.setBounds(8, 29, 220, 22)
        self.openBrowser = JButton('Open browser', actionPerformed=self.openBrowserClick, font=buttonFont, margin=buttonMargin)
        self.openBrowser.setMnemonic(KeyEvent.VK_O)
        self.openBrowser.setBounds(234, 29, 87, 21)
        self.close = JButton('Close', actionPerformed=self.closeClick, font=buttonFont, margin=buttonMargin)
        self.close.setMnemonic(KeyEvent.VK_C)
        self.close.setBounds(343, 4, 90, 21)
        self.readLicense = JButton('Read License', actionPerformed=self.readLicenseClick, font=buttonFont, margin=buttonMargin)
        self.readLicense.setMnemonic(KeyEvent.VK_L)
        self.readLicense.setBounds(343, 67, 90, 21)
        self.moreInfo = JButton('Why Register?', actionPerformed=self.moreInfoClick, font=buttonFont, margin=buttonMargin)
        self.moreInfo.setMnemonic(KeyEvent.VK_W)
        self.moreInfo.setBounds(343, 40, 90, 23)
        self.registerMe = JButton('Register Me!', actionPerformed=self.registerMeClick, font=buttonFont, margin=buttonMargin)
        self.registerMe.setMnemonic(KeyEvent.VK_R)
        self.registerMe.setBounds(169, 227, 109, 21)
        self.PrintButton = JButton('Print', actionPerformed=self.PrintButtonClick, font=buttonFont, margin=buttonMargin)
        self.PrintButton.setMnemonic(KeyEvent.VK_P)
        self.PrintButton.setBounds(343, 103, 90, 21)
        self.PrintButton.visible = 0
        self.thankYou = JTextArea(10, 10)
        self.thankYou.setBounds(344, 234, 333, 250)
        self.thankYou.editable = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.thankYou.ScrollBars = ssVertical
        #  ------- UNHANDLED TYPE TPrintDialog: PrintDialog 
        #  --------------- UNHANDLED ATTRIBUTE: self.PrintDialog.Top = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.PrintDialog.Left = 308
        contentPane.add(self.Label11)
        contentPane.add(self.Label1)
        contentPane.add(self.Label2)
        contentPane.add(self.Label5)
        contentPane.add(self.Label6)
        contentPane.add(self.Panel1)
        contentPane.add(self.orderPageEdit)
        contentPane.add(self.openBrowser)
        contentPane.add(self.close)
        contentPane.add(self.readLicense)
        contentPane.add(self.moreInfo)
        contentPane.add(self.registerMe)
        contentPane.add(self.PrintButton)
        scroller = JScrollPane(self.thankYou)
        scroller.setBounds(344, 234, 333, 250)
        contentPane.add(scroller)
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def PrintButtonClick(self, event):
        print "PrintButtonClick"
        
    def closeClick(self, event):
        print "closeClick"
        
    def moreInfoClick(self, event):
        print "moreInfoClick"
        
    def openBrowserClick(self, event):
        print "openBrowserClick"
        
    def readLicenseClick(self, event):
        print "readLicenseClick"
        
    def registerMeClick(self, event):
        print "registerMeClick"
        
if __name__ == "__main__":
    window = RegistrationWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
