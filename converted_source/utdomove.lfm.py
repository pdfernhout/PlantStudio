from common import *

#Useage:
#        import TdoMoverWindow
#        window = TdoMoverWindow.TdoMoverWindow()
#        window.visible = 1

class TdoMoverWindow(JFrame):
    def __init__(self, title='3D Object Mover'):
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
        self.setBounds(388, 235, 404, 310  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.AutoScroll = False
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.OnClose = FormClose
        
        self.previewImage = ImagePanel() # No image was set
        self.previewImage.setBounds(152, 4, 100, 60)
        self.previewImage.mouseReleased = self.previewImageMouseUp
        self.leftTdoFileChangedIndicatorImage = toolkit.createImage("../resources/TdoMoverForm_leftTdoFileChangedIndicator.png")
        self.leftTdoFileChangedIndicator = ImagePanel(ImageIcon(self.leftTdoFileChangedIndicatorImage))
        self.leftTdoFileChangedIndicator.setBounds(8, 30, 16, 16)
        self.rightTdoFileChangedIndicatorImage = toolkit.createImage("../resources/TdoMoverForm_rightTdoFileChangedIndicator.png")
        self.rightTdoFileChangedIndicator = ImagePanel(ImageIcon(self.rightTdoFileChangedIndicatorImage))
        self.rightTdoFileChangedIndicator.setBounds(294, 30, 16, 16)
        self.helpButtonImage = toolkit.createImage("../resources/TdoMoverForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(152, 264, 100, 21)
        self.leftTdoFileNameEdit = JTextField('c:\PlantStudio\plants1.pla', 10, editable=0)
        self.leftTdoFileNameEdit.setBounds(4, 4, 140, 20)
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoFileNameEdit.AutoSelect = False
        self.leftOpenClose = JButton('Open...', actionPerformed=self.leftOpenCloseClick, font=buttonFont, margin=buttonMargin)
        self.leftOpenClose.setMnemonic(KeyEvent.VK_O)
        self.leftOpenClose.setBounds(30, 26, 50, 21)
        self.rightTdoFileNameEdit = JTextField('c:\PlantStudio\newplants.pla', 10, editable=0)
        self.rightTdoFileNameEdit.setBounds(257, 4, 140, 20)
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoFileNameEdit.AutoSelect = False
        self.rightOpenClose = JButton('Open...', actionPerformed=self.rightOpenCloseClick, font=buttonFont, margin=buttonMargin)
        self.rightOpenClose.setMnemonic(KeyEvent.VK_O)
        self.rightOpenClose.setBounds(280, 28, 50, 21)
        self.newFile = JButton('New...', actionPerformed=self.newFileClick, font=buttonFont, margin=buttonMargin)
        self.newFile.setMnemonic(KeyEvent.VK_N)
        self.newFile.setBounds(345, 28, 50, 21)
        self.transfer = JButton('Transfer >>', actionPerformed=self.transferClick, font=buttonFont, margin=buttonMargin)
        self.transfer.setMnemonic(KeyEvent.VK_T)
        self.transfer.setBounds(152, 76, 100, 21)
        self.undo = JButton('Undo duplicate', actionPerformed=self.undoClick, font=buttonFont, margin=buttonMargin)
        self.undo.setMnemonic(KeyEvent.VK_U)
        self.undo.setBounds(152, 171, 100, 21)
        self.redo = JButton('Redo last', actionPerformed=self.redoClick, font=buttonFont, margin=buttonMargin)
        self.redo.setMnemonic(KeyEvent.VK_R)
        self.redo.setBounds(152, 195, 100, 21)
        self.rename = JButton('Rename...', actionPerformed=self.renameClick, font=buttonFont, margin=buttonMargin)
        self.rename.setMnemonic(KeyEvent.VK_A)
        self.rename.setBounds(152, 148, 100, 21)
        self.duplicate = JButton('Duplicate', actionPerformed=self.duplicateClick, font=buttonFont, margin=buttonMargin)
        self.duplicate.setMnemonic(KeyEvent.VK_D)
        self.duplicate.setBounds(152, 100, 100, 21)
        self.delete = JButton('Delete', actionPerformed=self.deleteClick, font=buttonFont, margin=buttonMargin)
        self.delete.setMnemonic(KeyEvent.VK_E)
        self.delete.setBounds(152, 124, 100, 21)
        self.leftTdoList = JTable(DefaultTableModel())
        self.leftTdoList.setBounds(-24, 54, 140, 333)
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.OnEndDrag = leftTdoListEndDrag
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.OnDrawCell = leftTdoListDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.OnDblClick = leftTdoListDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.OnDragOver = leftTdoListDragOver
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.FixedRows = 0
        self.leftTdoList.keyPressed = self.leftTdoListKeyDown
        self.leftTdoList.mousePressed = self.leftTdoListMouseDown
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.ColCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.DefaultRowHeight = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.ScrollBars = ssVertical
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.GridLineWidth = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.leftTdoList.Options = []
        self.rightTdoList = JTable(DefaultTableModel())
        self.rightTdoList.setBounds(259, 62, 140, 245)
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.OnEndDrag = rightTdoListEndDrag
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.OnDrawCell = rightTdoListDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.OnDblClick = rightTdoListDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.OnDragOver = rightTdoListDragOver
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.FixedRows = 0
        self.rightTdoList.keyPressed = self.rightTdoListKeyDown
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.ColCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.DefaultRowHeight = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.rightTdoList.GridLineWidth = 0
        self.rightTdoList.mousePressed = self.rightTdoListMouseDown
        self.editTdo = JButton('Edit', actionPerformed=self.editTdoClick, font=buttonFont, margin=buttonMargin)
        self.editTdo.setMnemonic(KeyEvent.VK_I)
        self.editTdo.setBounds(153, 219, 100, 21)
        self.close = JButton('Quit', actionPerformed=self.closeClick, font=buttonFont, margin=buttonMargin)
        self.close.setMnemonic(KeyEvent.VK_Q)
        self.close.setBounds(152, 288, 100, 21)
        contentPane.add(self.previewImage)
        contentPane.add(self.leftTdoFileChangedIndicator)
        contentPane.add(self.rightTdoFileChangedIndicator)
        contentPane.add(self.helpButton)
        contentPane.add(self.leftTdoFileNameEdit)
        contentPane.add(self.leftOpenClose)
        contentPane.add(self.rightTdoFileNameEdit)
        contentPane.add(self.rightOpenClose)
        contentPane.add(self.newFile)
        contentPane.add(self.transfer)
        contentPane.add(self.undo)
        contentPane.add(self.redo)
        contentPane.add(self.rename)
        contentPane.add(self.duplicate)
        contentPane.add(self.delete)
        contentPane.add(self.leftTdoList)
        contentPane.add(self.rightTdoList)
        contentPane.add(self.editTdo)
        contentPane.add(self.close)
        
    def closeClick(self, event):
        print "closeClick"
        
    def deleteClick(self, event):
        print "deleteClick"
        
    def duplicateClick(self, event):
        print "duplicateClick"
        
    def editTdoClick(self, event):
        print "editTdoClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def leftOpenCloseClick(self, event):
        print "leftOpenCloseClick"
        
    def leftTdoListKeyDown(self, event):
        print "leftTdoListKeyDown"
        
    def leftTdoListMouseDown(self, event):
        print "leftTdoListMouseDown"
        
    def newFileClick(self, event):
        print "newFileClick"
        
    def previewImageMouseUp(self, event):
        print "previewImageMouseUp"
        
    def redoClick(self, event):
        print "redoClick"
        
    def renameClick(self, event):
        print "renameClick"
        
    def rightOpenCloseClick(self, event):
        print "rightOpenCloseClick"
        
    def rightTdoListKeyDown(self, event):
        print "rightTdoListKeyDown"
        
    def rightTdoListMouseDown(self, event):
        print "rightTdoListMouseDown"
        
    def transferClick(self, event):
        print "transferClick"
        
    def undoClick(self, event):
        print "undoClick"
        
if __name__ == "__main__":
    window = TdoMoverWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
