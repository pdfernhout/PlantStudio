from common import *

#Useage:
#        import AboutWindow
#        window = AboutWindow.AboutWindow()
#        window.visible = 1

class AboutWindow(JFrame):
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
        self.setBounds(242, 199, 483, 356  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = []
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.ActiveControl = registerIt
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.splashScreenPictureImage = toolkit.createImage("../resources/AboutForm_splashScreenPicture.png")
        self.splashScreenPicture = ImagePanel(ImageIcon(self.splashScreenPictureImage))
        self.splashScreenPicture.setBounds(2, 3, 382, 270)
        self.versionLabel = JLabel('version 2.0', font=buttonFont)
        self.versionLabel.setBounds(13, 75, 68, 16)
        self.close = JButton('Close', actionPerformed=self.closeClick, font=buttonFont, margin=buttonMargin)
        self.close.setMnemonic(KeyEvent.VK_C)
        self.close.setBounds(390, 4, 90, 21)
        self.registerIt = JButton('Register', actionPerformed=self.registerItClick, font=buttonFont, margin=buttonMargin)
        self.registerIt.setMnemonic(KeyEvent.VK_R)
        self.getRootPane().setDefaultButton(self.registerIt)
        self.registerIt.setBounds(390, 28, 90, 23)
        self.readLicense = JButton('Read License', actionPerformed=self.readLicenseClick, font=buttonFont, margin=buttonMargin)
        self.readLicense.setMnemonic(KeyEvent.VK_L)
        self.readLicense.setBounds(390, 93, 90, 21)
        self.cancel = JButton('Cancel', font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_A)
        self.cancel.setBounds(390, 129, 90, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.ModalResult = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.whyRegister = JButton('Why Register?', actionPerformed=self.whyRegisterClick, font=buttonFont, margin=buttonMargin)
        self.whyRegister.setMnemonic(KeyEvent.VK_W)
        self.getRootPane().setDefaultButton(self.whyRegister)
        self.whyRegister.setBounds(390, 66, 90, 23)
        self.noDistributeLabel = JLabel('Under no circumstances are you licensed to distribute any output or data files created using an unregistered copy of PlantStudio.', font=buttonFont)
        self.noDistributeLabel.setBounds(8, 221, 327, 28)
        self.timeWarningLabel = JLabel('If you have been using PlantStudio for ten hours or more (in total), you are legally required to register it.', font=buttonFont)
        self.timeWarningLabel.setBounds(8, 40, 320, 28)
        self.hoursLabel = JLabel('You have been evaluating PlantStudio for 8 hours.', font=buttonFont)
        self.hoursLabel.setBounds(8, 22, 242, 14)
        self.Label4 = JLabel(' We will remind you to register PlantStudio by', font=buttonFont)
        self.Label4.setBounds(8, 81, 217, 14)
        self.Label5 = JLabel('- showing you this window when you leave PlantStudio', font=buttonFont)
        self.Label5.setBounds(26, 121, 270, 14)
        self.Label6 = JLabel('- adding a little picture to your 2D output, like this: ', font=buttonFont)
        self.Label6.setBounds(26, 141, 238, 14)
        self.unregistered2DExportReminderImage = toolkit.createImage("../resources/AboutForm_unregistered2DExportReminder.png")
        self.unregistered2DExportReminder = ImagePanel(ImageIcon(self.unregistered2DExportReminderImage))
        self.unregistered2DExportReminder.setBounds(264, 140, 17, 16)
        self.Label7 = JLabel('These reminders and restrictions will disappear on registration.', font=buttonFont)
        self.Label7.setBounds(8, 187, 304, 14)
        self.Label1 = JLabel('Thank you for evaluating PlantStudio!', font=buttonFont)
        self.Label1.setBounds(8, 4, 177, 14)
        self.Label2 = JLabel('- addling a little rectangle to your 3D output, like this:', font=buttonFont)
        self.Label2.setBounds(26, 162, 249, 14)
        self.unregistered3DExportReminderImage = toolkit.createImage("../resources/AboutForm_unregistered3DExportReminder.png")
        self.unregistered3DExportReminder = ImagePanel(ImageIcon(self.unregistered3DExportReminderImage))
        self.unregistered3DExportReminder.setBounds(277, 159, 31, 21)
        self.exportRestrictionLabel = JLabel('- restricting the number of exports to 20 at first, then 2 per session', font=buttonFont)
        self.exportRestrictionLabel.setBounds(26, 101, 322, 14)
        self.registrationInfoPanel = JPanel(layout=None)
        # -- self.registrationInfoPanel.setLayout(BoxLayout(self.registrationInfoPanel, BoxLayout.Y_AXIS))
        self.registrationInfoPanel.add(self.noDistributeLabel)
        self.registrationInfoPanel.add(self.timeWarningLabel)
        self.registrationInfoPanel.add(self.hoursLabel)
        self.registrationInfoPanel.add(self.Label4)
        self.registrationInfoPanel.add(self.Label5)
        self.registrationInfoPanel.add(self.Label6)
        self.registrationInfoPanel.add(self.unregistered2DExportReminder)
        self.registrationInfoPanel.add(self.Label7)
        self.registrationInfoPanel.add(self.Label1)
        self.registrationInfoPanel.add(self.Label2)
        self.registrationInfoPanel.add(self.unregistered3DExportReminder)
        self.registrationInfoPanel.add(self.exportRestrictionLabel)
        self.registrationInfoPanel.setBounds(2, 96, 383, 257)
        self.supportButton = JButton('Program Info...', actionPerformed=self.supportButtonClick, font=buttonFont, margin=buttonMargin)
        self.supportButton.setMnemonic(KeyEvent.VK_P)
        self.supportButton.setBounds(390, 281, 91, 21)
        contentPane.add(self.splashScreenPicture)
        contentPane.add(self.versionLabel)
        contentPane.add(self.close)
        contentPane.add(self.registerIt)
        contentPane.add(self.readLicense)
        contentPane.add(self.cancel)
        contentPane.add(self.whyRegister)
        contentPane.add(self.registrationInfoPanel)
        contentPane.add(self.supportButton)
        
    def closeClick(self, event):
        print "closeClick"
        
    def readLicenseClick(self, event):
        print "readLicenseClick"
        
    def registerItClick(self, event):
        print "registerItClick"
        
    def supportButtonClick(self, event):
        print "supportButtonClick"
        
    def whyRegisterClick(self, event):
        print "whyRegisterClick"
        
if __name__ == "__main__":
    window = AboutWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
