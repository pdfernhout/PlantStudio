from common import *

#Useage:
#        import TemplateMoverWindow
#        window = TemplateMoverWindow.TemplateMoverWindow()
#        window.visible = 1

class TemplateMoverWindow(JFrame):
    def __init__(self, title='Template Mover'):
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
        self.setBounds(320, 203, 589, 348  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.leftTemplatesList = JList(DefaultListModel(), mouseClicked=self.leftTemplatesListClick, fixedCellHeight=16)
        self.leftTemplatesList.setBounds(4, 56, 235, 290)
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTemplatesList.IntegralHeight = True
        self.rightTemplatesList = JList(DefaultListModel(), mouseClicked=self.rightTemplatesListClick, fixedCellHeight=16)
        self.rightTemplatesList.setBounds(266, 56, 235, 290)
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTemplatesList.IntegralHeight = True
        self.Done = JButton('Done', actionPerformed=self.DoneClick, font=buttonFont, margin=buttonMargin)
        self.Done.setMnemonic(KeyEvent.VK_D)
        self.getRootPane().setDefaultButton(self.Done)
        self.Done.setBounds(505, 6, 80, 24)
        #  --------------- UNHANDLED ATTRIBUTE: self.Done.Cancel = True
        self.CopyTemplate = JButton('Copy...', actionPerformed=self.CopyTemplateClick, font=buttonFont, margin=buttonMargin)
        self.CopyTemplate.setMnemonic(KeyEvent.VK_C)
        self.CopyTemplate.setBounds(505, 86, 80, 24)
        self.DeleteTemplate = JButton('Delete', actionPerformed=self.DeleteTemplateClick, font=buttonFont, margin=buttonMargin)
        self.DeleteTemplate.setMnemonic(KeyEvent.VK_D)
        self.DeleteTemplate.setBounds(505, 116, 80, 24)
        self.ObjectTypeToShow = JComboBox(DefaultComboBoxModel())
        self.ObjectTypeToShow.setBounds(10, 364, 77, 24)
        #  --------------- UNHANDLED ATTRIBUTE: self.ObjectTypeToShow.Style = csDropDownList
        self.ObjectTypeToShow.getModel().addElement("Bag")
        self.ObjectTypeToShow.getModel().addElement("Soil Type")
        self.ObjectTypeToShow.getModel().addElement("Climate")
        self.ObjectTypeToShow.getModel().addElement("Cultivar")
        self.ObjectTypeToShow.getModel().addElement("Pesticide Type")
        #  --------------- UNHANDLED ATTRIBUTE: self.ObjectTypeToShow.ItemHeight = 16
        self.ObjectTypeToShow.visible = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.ObjectTypeToShow.TabStop = False
        self.helpButtonImage = toolkit.createImage("../resources/TemplateMoverForm_helpButton.png")
        self.helpButton = JButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.helpButton.setBounds(505, 236, 80, 24)
        self.renameTemplate = JButton('Rename...', actionPerformed=self.renameTemplateClick, font=buttonFont, margin=buttonMargin)
        self.renameTemplate.setMnemonic(KeyEvent.VK_R)
        self.renameTemplate.setBounds(505, 56, 80, 24)
        self.Import = JButton('Import...', font=buttonFont, margin=buttonMargin)
        self.Import.setBounds(10, 390, 80, 24)
        self.Import.visible = 0
        self.Export = JButton('Export...', font=buttonFont, margin=buttonMargin)
        self.Export.setBounds(10, 416, 80, 24)
        self.Export.visible = 0
        self.copyLeftToRightImage = toolkit.createImage("../resources/TemplateMoverForm_copyLeftToRight.png")
        self.copyLeftToRight = JButton(ImageIcon(self.copyLeftToRightImage), actionPerformed=self.copyLeftToRightClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.copyLeftToRight.setBounds(241, 183, 22, 22)
        self.copyLeftToRight.toolTipText = 'Copy from left to right'
        self.copyRightToLeftImage = toolkit.createImage("../resources/TemplateMoverForm_copyRightToLeft.png")
        self.copyRightToLeft = JButton(ImageIcon(self.copyRightToLeftImage), actionPerformed=self.copyRightToLeftClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.copyRightToLeft.setBounds(241, 211, 22, 22)
        self.copyRightToLeft.toolTipText = 'Copy from right to left'
        self.chooseFontImage = toolkit.createImage("../resources/TemplateMoverForm_chooseFont.png")
        self.chooseFont = JButton('Font', ImageIcon(self.chooseFontImage), actionPerformed=self.chooseFontClick, font=buttonFont, margin=buttonMargin)
        self.chooseFont.setMnemonic(KeyEvent.VK_F)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.chooseFont.setBounds(505, 146, 80, 24)
        self.chooseFont.toolTipText = 'Change font'
        self.leftTemplatesFileNameEdit = JTextField("", 10, editable=0)
        self.leftTemplatesFileNameEdit.setBounds(4, 4, 233, 24)
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTemplatesFileNameEdit.TabStop = False
        self.leftTemplatesFileOpen = JButton('Open...', actionPerformed=self.leftTemplatesFileOpenClick, font=buttonFont, margin=buttonMargin)
        self.leftTemplatesFileOpen.setBounds(3, 29, 61, 25)
        self.leftTemplatesFileNew = JButton('New...', actionPerformed=self.leftTemplatesFileNewClick, font=buttonFont, margin=buttonMargin)
        self.leftTemplatesFileNew.setBounds(64, 29, 59, 25)
        self.leftTemplatesFileSave = JButton('Save', actionPerformed=self.leftTemplatesFileSaveClick, font=buttonFont, margin=buttonMargin)
        self.leftTemplatesFileSave.setBounds(122, 29, 43, 25)
        self.rightTemplatesFileNameEdit = JTextField("", 10, editable=0)
        self.rightTemplatesFileNameEdit.setBounds(268, 4, 233, 24)
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTemplatesFileNameEdit.TabStop = False
        self.rightTemplatesFileOpen = JButton('Open...', actionPerformed=self.rightTemplatesFileOpenClick, font=buttonFont, margin=buttonMargin)
        self.rightTemplatesFileOpen.setBounds(268, 29, 57, 25)
        self.rightTemplatesFileNew = JButton('New...', actionPerformed=self.rightTemplatesFileNewClick, font=buttonFont, margin=buttonMargin)
        self.rightTemplatesFileNew.setBounds(325, 29, 65, 25)
        self.rightTemplatesFileSave = JButton('Save', actionPerformed=self.rightTemplatesFileSaveClick, font=buttonFont, margin=buttonMargin)
        self.rightTemplatesFileSave.setBounds(390, 29, 43, 25)
        self.leftTemplatesFileSaveAs = JButton('Save as ...', actionPerformed=self.leftTemplatesFileSaveAsClick, font=buttonFont, margin=buttonMargin)
        self.leftTemplatesFileSaveAs.setBounds(164, 29, 73, 25)
        self.rightTemplatesFileSaveAs = JButton('Save as...', actionPerformed=self.rightTemplatesFileSaveAsClick, font=buttonFont, margin=buttonMargin)
        self.rightTemplatesFileSaveAs.setBounds(432, 29, 69, 25)
        self.exportText = JButton('Export...', actionPerformed=self.exportTextClick, font=buttonFont, margin=buttonMargin)
        self.exportText.setMnemonic(KeyEvent.VK_E)
        self.exportText.setBounds(505, 176, 80, 24)
        self.importText = JButton('Import...', actionPerformed=self.importTextClick, font=buttonFont, margin=buttonMargin)
        self.importText.setMnemonic(KeyEvent.VK_I)
        self.importText.setBounds(505, 206, 80, 24)
        #  ------- UNHANDLED TYPE TFontDialog: FontDialog1 
        #  --------------- UNHANDLED ATTRIBUTE: self.FontDialog1.MinFontSize = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.FontDialog1.Font.Style = []
        #  --------------- UNHANDLED ATTRIBUTE: self.FontDialog1.MaxFontSize = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.FontDialog1.Top = 364
        #  --------------- UNHANDLED ATTRIBUTE: self.FontDialog1.Font.Name = 'System'
        #  --------------- UNHANDLED ATTRIBUTE: self.FontDialog1.Font.Height = -13
        #  --------------- UNHANDLED ATTRIBUTE: self.FontDialog1.Font.Color = clWindowText
        #  --------------- UNHANDLED ATTRIBUTE: self.FontDialog1.Left = 104
        scroller = JScrollPane(self.leftTemplatesList)
        scroller.setBounds(4, 56, 235, 290)
        contentPane.add(scroller)
        scroller = JScrollPane(self.rightTemplatesList)
        scroller.setBounds(266, 56, 235, 290)
        contentPane.add(scroller)
        contentPane.add(self.Done)
        contentPane.add(self.CopyTemplate)
        contentPane.add(self.DeleteTemplate)
        contentPane.add(self.ObjectTypeToShow)
        contentPane.add(self.helpButton)
        contentPane.add(self.renameTemplate)
        contentPane.add(self.Import)
        contentPane.add(self.Export)
        contentPane.add(self.copyLeftToRight)
        contentPane.add(self.copyRightToLeft)
        contentPane.add(self.chooseFont)
        contentPane.add(self.leftTemplatesFileNameEdit)
        contentPane.add(self.leftTemplatesFileOpen)
        contentPane.add(self.leftTemplatesFileNew)
        contentPane.add(self.leftTemplatesFileSave)
        contentPane.add(self.rightTemplatesFileNameEdit)
        contentPane.add(self.rightTemplatesFileOpen)
        contentPane.add(self.rightTemplatesFileNew)
        contentPane.add(self.rightTemplatesFileSave)
        contentPane.add(self.leftTemplatesFileSaveAs)
        contentPane.add(self.rightTemplatesFileSaveAs)
        contentPane.add(self.exportText)
        contentPane.add(self.importText)
        
    def CopyTemplateClick(self, event):
        print "CopyTemplateClick"
        
    def DeleteTemplateClick(self, event):
        print "DeleteTemplateClick"
        
    def DoneClick(self, event):
        print "DoneClick"
        
    def chooseFontClick(self, event):
        print "chooseFontClick"
        
    def copyLeftToRightClick(self, event):
        print "copyLeftToRightClick"
        
    def copyRightToLeftClick(self, event):
        print "copyRightToLeftClick"
        
    def exportTextClick(self, event):
        print "exportTextClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def importTextClick(self, event):
        print "importTextClick"
        
    def leftTemplatesFileNewClick(self, event):
        print "leftTemplatesFileNewClick"
        
    def leftTemplatesFileOpenClick(self, event):
        print "leftTemplatesFileOpenClick"
        
    def leftTemplatesFileSaveAsClick(self, event):
        print "leftTemplatesFileSaveAsClick"
        
    def leftTemplatesFileSaveClick(self, event):
        print "leftTemplatesFileSaveClick"
        
    def leftTemplatesListClick(self, event):
        print "leftTemplatesListClick"
        
    def renameTemplateClick(self, event):
        print "renameTemplateClick"
        
    def rightTemplatesFileNewClick(self, event):
        print "rightTemplatesFileNewClick"
        
    def rightTemplatesFileOpenClick(self, event):
        print "rightTemplatesFileOpenClick"
        
    def rightTemplatesFileSaveAsClick(self, event):
        print "rightTemplatesFileSaveAsClick"
        
    def rightTemplatesFileSaveClick(self, event):
        print "rightTemplatesFileSaveClick"
        
    def rightTemplatesListClick(self, event):
        print "rightTemplatesListClick"
        
if __name__ == "__main__":
    window = TemplateMoverWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
