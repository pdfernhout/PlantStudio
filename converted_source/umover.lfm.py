from common import *

#Useage:
#        import MoverWindow
#        window = MoverWindow.MoverWindow()
#        window.visible = 1

class MoverWindow(JFrame):
    def __init__(self, title='Plant Mover'):
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
        self.setBounds(439, 193, 400, 373  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        self.keyPressed = self.FormKeyDown
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.AutoScroll = False
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.OnClose = FormClose
        
        self.previewImage = ImagePanel() # No image was set
        self.previewImage.setBounds(150, 4, 100, 71)
        self.leftPlantFileChangedIndicatorImage = toolkit.createImage("../resources/MoverForm_leftPlantFileChangedIndicator.png")
        self.leftPlantFileChangedIndicator = ImagePanel(ImageIcon(self.leftPlantFileChangedIndicatorImage))
        self.leftPlantFileChangedIndicator.setBounds(4, 30, 16, 16)
        self.rightPlantFileChangedIndicatorImage = toolkit.createImage("../resources/MoverForm_rightPlantFileChangedIndicator.png")
        self.rightPlantFileChangedIndicator = ImagePanel(ImageIcon(self.rightPlantFileChangedIndicatorImage))
        self.rightPlantFileChangedIndicator.setBounds(262, 30, 16, 16)
        self.helpButtonImage = toolkit.createImage("../resources/MoverForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(152, 321, 100, 24)
        self.leftPlantFileNameEdit = JTextField('c:\PlantStudio\plants1.pla', 10, editable=0)
        self.leftPlantFileNameEdit.setBounds(2, 4, 140, 20)
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantFileNameEdit.AutoSelect = False
        self.leftOpenClose = JButton('Open...', actionPerformed=self.leftOpenCloseClick, font=buttonFont, margin=buttonMargin)
        self.leftOpenClose.setMnemonic(KeyEvent.VK_O)
        self.leftOpenClose.setBounds(24, 28, 50, 21)
        self.rightPlantFileNameEdit = JTextField('c:\PlantStudio\newplants.pla', 10, editable=0)
        self.rightPlantFileNameEdit.setBounds(258, 4, 140, 20)
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantFileNameEdit.AutoSelect = False
        self.rightOpenClose = JButton('Open...', actionPerformed=self.rightOpenCloseClick, font=buttonFont, margin=buttonMargin)
        self.rightOpenClose.setMnemonic(KeyEvent.VK_O)
        self.rightOpenClose.setBounds(284, 27, 50, 21)
        self.newFile = JButton('New...', actionPerformed=self.newFileClick, font=buttonFont, margin=buttonMargin)
        self.newFile.setMnemonic(KeyEvent.VK_N)
        self.newFile.setBounds(337, 27, 50, 21)
        self.transfer = JButton('Transfer >>', actionPerformed=self.transferClick, font=buttonFont, margin=buttonMargin)
        self.transfer.setMnemonic(KeyEvent.VK_T)
        self.transfer.setBounds(151, 108, 100, 21)
        self.close = JButton('Quit', actionPerformed=self.closeClick, font=buttonFont, margin=buttonMargin)
        self.close.setMnemonic(KeyEvent.VK_Q)
        self.close.setBounds(151, 349, 100, 21)
        self.undo = JButton('Undo duplicate', actionPerformed=self.undoClick, font=buttonFont, margin=buttonMargin)
        self.undo.setMnemonic(KeyEvent.VK_U)
        self.undo.setBounds(151, 273, 100, 21)
        self.redo = JButton('Redo last', actionPerformed=self.redoClick, font=buttonFont, margin=buttonMargin)
        self.redo.setMnemonic(KeyEvent.VK_R)
        self.redo.setBounds(151, 297, 100, 21)
        self.cut = JButton('Cut (Ctrl-X)', actionPerformed=self.cutClick, font=buttonFont, margin=buttonMargin)
        self.cut.setMnemonic(KeyEvent.VK_C)
        self.cut.setBounds(151, 132, 100, 21)
        self.copy = JButton('Copy (Ctrl-C)', actionPerformed=self.copyClick, font=buttonFont, margin=buttonMargin)
        self.copy.setMnemonic(KeyEvent.VK_O)
        self.copy.setBounds(151, 155, 100, 21)
        self.paste = JButton('Paste (Ctrl-V)', actionPerformed=self.pasteClick, font=buttonFont, margin=buttonMargin)
        self.paste.setMnemonic(KeyEvent.VK_P)
        self.paste.setBounds(151, 179, 100, 21)
        self.rename = JButton('Rename...', actionPerformed=self.renameClick, font=buttonFont, margin=buttonMargin)
        self.rename.setMnemonic(KeyEvent.VK_A)
        self.rename.setBounds(151, 250, 100, 21)
        self.duplicate = JButton('Duplicate', actionPerformed=self.duplicateClick, font=buttonFont, margin=buttonMargin)
        self.duplicate.setMnemonic(KeyEvent.VK_D)
        self.duplicate.setBounds(151, 202, 100, 21)
        self.delete = JButton('Delete', actionPerformed=self.deleteClick, font=buttonFont, margin=buttonMargin)
        self.delete.setMnemonic(KeyEvent.VK_E)
        self.delete.setBounds(151, 226, 100, 21)
        self.leftPlantList = JTable(DefaultTableModel())
        self.leftPlantList.setBounds(4, 52, 140, 315)
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.OnEndDrag = leftPlantListEndDrag
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.OnDrawCell = leftPlantListDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.OnDblClick = leftPlantListDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.OnDragOver = leftPlantListDragOver
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.FixedRows = 0
        self.leftPlantList.keyPressed = self.leftPlantListKeyDown
        self.leftPlantList.mousePressed = self.leftPlantListMouseDown
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.ColCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.DefaultRowHeight = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.ScrollBars = ssVertical
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.GridLineWidth = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.leftPlantList.Options = []
        self.rightPlantList = JTable(DefaultTableModel())
        self.rightPlantList.setBounds(258, 52, 140, 317)
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.OnEndDrag = rightPlantListEndDrag
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.OnDrawCell = rightPlantListDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.OnDblClick = rightPlantListDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.OnDragOver = rightPlantListDragOver
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.FixedRows = 0
        self.rightPlantList.keyPressed = self.rightPlantListKeyDown
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.ColCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.DefaultRowHeight = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.rightPlantList.GridLineWidth = 0
        self.rightPlantList.mousePressed = self.rightPlantListMouseDown
        contentPane.add(self.previewImage)
        contentPane.add(self.leftPlantFileChangedIndicator)
        contentPane.add(self.rightPlantFileChangedIndicator)
        contentPane.add(self.helpButton)
        contentPane.add(self.leftPlantFileNameEdit)
        contentPane.add(self.leftOpenClose)
        contentPane.add(self.rightPlantFileNameEdit)
        contentPane.add(self.rightOpenClose)
        contentPane.add(self.newFile)
        contentPane.add(self.transfer)
        contentPane.add(self.close)
        contentPane.add(self.undo)
        contentPane.add(self.redo)
        contentPane.add(self.cut)
        contentPane.add(self.copy)
        contentPane.add(self.paste)
        contentPane.add(self.rename)
        contentPane.add(self.duplicate)
        contentPane.add(self.delete)
        contentPane.add(self.leftPlantList)
        contentPane.add(self.rightPlantList)
        
    def FormKeyDown(self, event):
        print "FormKeyDown"
        
    def closeClick(self, event):
        print "closeClick"
        
    def copyClick(self, event):
        print "copyClick"
        
    def cutClick(self, event):
        print "cutClick"
        
    def deleteClick(self, event):
        print "deleteClick"
        
    def duplicateClick(self, event):
        print "duplicateClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def leftOpenCloseClick(self, event):
        print "leftOpenCloseClick"
        
    def leftPlantListKeyDown(self, event):
        print "leftPlantListKeyDown"
        
    def leftPlantListMouseDown(self, event):
        print "leftPlantListMouseDown"
        
    def newFileClick(self, event):
        print "newFileClick"
        
    def pasteClick(self, event):
        print "pasteClick"
        
    def redoClick(self, event):
        print "redoClick"
        
    def renameClick(self, event):
        print "renameClick"
        
    def rightOpenCloseClick(self, event):
        print "rightOpenCloseClick"
        
    def rightPlantListKeyDown(self, event):
        print "rightPlantListKeyDown"
        
    def rightPlantListMouseDown(self, event):
        print "rightPlantListMouseDown"
        
    def transferClick(self, event):
        print "transferClick"
        
    def undoClick(self, event):
        print "undoClick"
        
if __name__ == "__main__":
    window = MoverWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
