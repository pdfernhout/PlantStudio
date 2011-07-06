from common import *

#Useage:
#        import PickTdoWindow
#        window = PickTdoWindow.PickTdoWindow()
#        window.visible = 1

class PickTdoWindow(JFrame):
    def __init__(self, title='Choose a 3D object'):
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
        self.setBounds(511, 210, 406, 377  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.OnClose = FormClose
        
        self.helpButtonImage = toolkit.createImage("../resources/PickTdoForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(334, 245, 60, 21)
        self.grid = JTable(DefaultTableModel())
        self.grid.setBounds(4, 28, 323, 263)
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.OnDrawCell = gridDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.OnSelectCell = gridSelectCell
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.DefaultColWidth = 60
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.RowCount = 20
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.DefaultRowHeight = 64
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.ScrollBars = ssVertical
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.OnDblClick = gridDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.grid.Options = []
        self.Close = JButton('OK', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.getRootPane().setDefaultButton(self.Close)
        self.Close.setBounds(334, 4, 60, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setBounds(334, 27, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.fileChangedImageImage = toolkit.createImage("../resources/PickTdoForm_fileChangedImage.png")
        self.fileChangedImage = ImagePanel(ImageIcon(self.fileChangedImageImage))
        self.fileChangedImage.setBounds(8, 24, 16, 16)
        self.sectionTdosChangeLibraryImage = toolkit.createImage("../resources/PickTdoForm_sectionTdosChangeLibrary.png")
        self.sectionTdosChangeLibrary = SpeedButton('Change...', ImageIcon(self.sectionTdosChangeLibraryImage), actionPerformed=self.sectionTdosChangeLibraryClick, font=buttonFont, margin=buttonMargin)
        self.sectionTdosChangeLibrary.setMnemonic(KeyEvent.VK_C)
        self.sectionTdosChangeLibrary.setBounds(228, 19, 85, 25)
        self.libraryFileName = JTextField("", 10, editable=0)
        self.libraryFileName.setBounds(30, 22, 193, 22)
        self.libraryGroupBox = JPanel(layout=None)
        # -- self.libraryGroupBox.setLayout(BoxLayout(self.libraryGroupBox, BoxLayout.Y_AXIS))
        # -- supposed to be group box
        self.libraryGroupBox.border = TitledBorder("'Current library'")
        self.libraryGroupBox.add(self.fileChangedImage)
        self.libraryGroupBox.add(self.sectionTdosChangeLibrary)
        self.libraryGroupBox.add(self.libraryFileName)
        self.libraryGroupBox.setBounds(4, 297, 321, 52)
        self.apply = JButton('Apply', actionPerformed=self.applyClick, font=buttonFont, margin=buttonMargin)
        self.apply.setMnemonic(KeyEvent.VK_A)
        self.apply.setBounds(334, 63, 59, 21)
        self.newTdo = JButton('New...', actionPerformed=self.newTdoClick, font=buttonFont, margin=buttonMargin)
        self.newTdo.setMnemonic(KeyEvent.VK_N)
        self.newTdo.setBounds(334, 99, 59, 21)
        self.editTdo = JButton('Edit...', actionPerformed=self.editTdoClick, font=buttonFont, margin=buttonMargin)
        self.editTdo.setMnemonic(KeyEvent.VK_E)
        self.editTdo.setBounds(334, 123, 59, 21)
        self.mover = JButton('Mover...', actionPerformed=self.moverClick, font=buttonFont, margin=buttonMargin)
        self.mover.setMnemonic(KeyEvent.VK_M)
        self.mover.setBounds(334, 208, 59, 21)
        self.copyTdo = JButton('Copy...', actionPerformed=self.copyTdoClick, font=buttonFont, margin=buttonMargin)
        self.copyTdo.setMnemonic(KeyEvent.VK_C)
        self.copyTdo.setBounds(334, 147, 59, 21)
        self.deleteTdo = JButton('Delete', actionPerformed=self.deleteTdoClick, font=buttonFont, margin=buttonMargin)
        self.deleteTdo.setMnemonic(KeyEvent.VK_D)
        self.deleteTdo.setBounds(334, 173, 59, 19)
        self.tdos = JComboBox(DefaultComboBoxModel())
        self.tdos.setBounds(4, 2, 323, 22)
        #  --------------- UNHANDLED ATTRIBUTE: self.tdos.Style = csDropDownList
        #  --------------- UNHANDLED ATTRIBUTE: self.tdos.DropDownCount = 12
        #  --------------- UNHANDLED ATTRIBUTE: self.tdos.OnChange = tdosChange
        #  --------------- UNHANDLED ATTRIBUTE: self.tdos.ItemHeight = 14
        contentPane.add(self.helpButton)
        contentPane.add(self.grid)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        contentPane.add(self.libraryGroupBox)
        contentPane.add(self.apply)
        contentPane.add(self.newTdo)
        contentPane.add(self.editTdo)
        contentPane.add(self.mover)
        contentPane.add(self.copyTdo)
        contentPane.add(self.deleteTdo)
        contentPane.add(self.tdos)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def applyClick(self, event):
        print "applyClick"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def copyTdoClick(self, event):
        print "copyTdoClick"
        
    def deleteTdoClick(self, event):
        print "deleteTdoClick"
        
    def editTdoClick(self, event):
        print "editTdoClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def moverClick(self, event):
        print "moverClick"
        
    def newTdoClick(self, event):
        print "newTdoClick"
        
    def sectionTdosChangeLibraryClick(self, event):
        print "sectionTdosChangeLibraryClick"
        
if __name__ == "__main__":
    window = PickTdoWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
