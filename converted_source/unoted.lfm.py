from common import *

#Useage:
#        import NoteEditWindow
#        window = NoteEditWindow.NoteEditWindow()
#        window.visible = 1

class NoteEditWindow(JFrame):
    def __init__(self, title='Edit note for plant'):
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
        self.setBounds(609, 214, 356, 294  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 13
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        
        self.helpButtonImage = toolkit.createImage("../resources/NoteEditForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(265, 64, 80, 21)
        self.OK = JButton('OK', font=buttonFont, margin=buttonMargin)
        self.OK.setMnemonic(KeyEvent.VK_O)
        self.OK.setBounds(265, 2, 80, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.OK.ModalResult = 1
        self.cancel = JButton('Cancel', font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(265, 25, 80, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.ModalResult = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.noteEditMemo = JTextArea(10, 10)
        self.noteEditMemo.setBounds(2, 2, 259, 261)
        #  --------------- UNHANDLED ATTRIBUTE: self.noteEditMemo.ScrollBars = ssVertical
        self.wrapLines = JCheckBox('wrap lines', actionPerformed=self.wrapLinesClick, font=buttonFont, margin=buttonMargin)
        self.wrapLines.setMnemonic(KeyEvent.VK_W)
        self.wrapLines.setBounds(272, 92, 75, 17)
        contentPane.add(self.helpButton)
        contentPane.add(self.OK)
        contentPane.add(self.cancel)
        scroller = JScrollPane(self.noteEditMemo)
        scroller.setBounds(2, 2, 259, 261)
        contentPane.add(scroller)
        contentPane.add(self.wrapLines)
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def wrapLinesClick(self, event):
        print "wrapLinesClick"
        
if __name__ == "__main__":
    window = NoteEditWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
