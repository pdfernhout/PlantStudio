from common import *

#Useage:
#        import UndoRedoListWindow
#        window = UndoRedoListWindow.UndoRedoListWindow()
#        window.visible = 1

class UndoRedoListWindow(JFrame):
    def __init__(self, title='Undo/Redo List'):
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
        self.setBounds(384, 254, 467, 255  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 13
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.AutoScroll = False
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poDefaultPosOnly
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.OnClose = FormClose
        
        self.helpButtonImage = toolkit.createImage("../resources/UndoRedoListForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(385, 69, 80, 25)
        self.undoListLabel = JLabel('Things you can Undo', displayedMnemonic=KeyEvent.VK_U, font=buttonFont)
        self.undoListLabel.setBounds(4, 4, 102, 13)
        self.redoListLabel = JLabel('Things you can Redo', displayedMnemonic=KeyEvent.VK_R, font=buttonFont)
        self.redoListLabel.setBounds(4, 122, 102, 13)
        self.OK = JButton('Undo/Redo', actionPerformed=self.OKClick, font=buttonFont, margin=buttonMargin)
        self.OK.setMnemonic(KeyEvent.VK_D)
        self.OK.setBounds(385, 4, 80, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(385, 30, 80, 21)
        self.undoList = JList(DefaultListModel(), mouseClicked=self.regulateListSelections, fixedCellHeight=13)
        self.undoList.setBounds(4, 20, 375, 97)
        #  --------------- UNHANDLED ATTRIBUTE: self.undoList.MultiSelect = True
        self.redoList = JList(DefaultListModel(), mouseClicked=self.regulateListSelections, fixedCellHeight=13)
        self.redoList.setBounds(4, 140, 373, 107)
        #  --------------- UNHANDLED ATTRIBUTE: self.redoList.MultiSelect = True
        contentPane.add(self.helpButton)
        contentPane.add(self.undoListLabel)
        contentPane.add(self.redoListLabel)
        contentPane.add(self.OK)
        contentPane.add(self.cancel)
        scroller = JScrollPane(self.undoList)
        scroller.setBounds(4, 20, 375, 97)
        contentPane.add(scroller)
        scroller = JScrollPane(self.redoList)
        scroller.setBounds(4, 140, 373, 107)
        contentPane.add(scroller)
        
    def OKClick(self, event):
        print "OKClick"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def regulateListSelections(self, event):
        print "regulateListSelections"
        
if __name__ == "__main__":
    window = UndoRedoListWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
