from common import *

#Useage:
#        import PrintBordersWindow
#        window = PrintBordersWindow.PrintBordersWindow()
#        window.visible = 1

class PrintBordersWindow(JFrame):
    def __init__(self, title='Print Border'):
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
        self.setBounds(616, 226, 274, 103  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = [biSystemMenu]
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        
        self.printBorderColorInnerLabel = JLabel('color', font=buttonFont)
        self.printBorderColorInnerLabel.setBounds(25, 27, 24, 14)
        self.printBorderColorOuterLabel = JLabel('color', font=buttonFont)
        self.printBorderColorOuterLabel.setBounds(25, 78, 24, 14)
        self.printBorderWidthInnerLabel = JLabel('thickness (pixels)', font=buttonFont)
        self.printBorderWidthInnerLabel.setBounds(77, 27, 85, 14)
        self.printBorderWidthOuterLabel = JLabel('thickness (pixels)', font=buttonFont)
        self.printBorderWidthOuterLabel.setBounds(77, 78, 85, 14)
        self.helpButtonImage = toolkit.createImage("../resources/PrintBordersForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(211, 63, 60, 21)
        self.Close = JButton('OK', actionPerformed=self.CloseClick, font=buttonFont, margin=buttonMargin)
        self.Close.setBounds(211, 4, 60, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setBounds(211, 27, 60, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.printBorderInner = JCheckBox('Draw inner border', actionPerformed=self.printBorderInnerClick, font=buttonFont, margin=buttonMargin)
        self.printBorderInner.setBounds(3, 5, 118, 17)
        self.printBorderOuter = JCheckBox('Draw outer border', actionPerformed=self.printBorderOuterClick, font=buttonFont, margin=buttonMargin)
        self.printBorderOuter.setBounds(3, 58, 112, 17)
        self.printBorderColorInner = JPanel(layout=None)
        # -- self.printBorderColorInner.setLayout(BoxLayout(self.printBorderColorInner, BoxLayout.Y_AXIS))
        self.printBorderColorInner.setBounds(53, 26, 15, 15)
        self.printBorderColorInner.mouseReleased = self.printBorderColorInnerMouseUp
        self.printBorderColorOuter = JPanel(layout=None)
        # -- self.printBorderColorOuter.setLayout(BoxLayout(self.printBorderColorOuter, BoxLayout.Y_AXIS))
        self.printBorderColorOuter.setBounds(53, 77, 15, 15)
        self.printBorderColorOuter.mouseReleased = self.printBorderColorOuterMouseUp
        # -- supposed to be a spin edit, not yet fuly implemented
        self.printBorderWidthInner = JSpinner(SpinnerNumberModel(0, 0, 0, 1))
        self.printBorderWidthInner.setBounds(163, 22, 39, 22)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.printBorderWidthOuter = JSpinner(SpinnerNumberModel(0, 0, 0, 1))
        self.printBorderWidthOuter.setBounds(163, 73, 39, 22)
        contentPane.add(self.printBorderColorInnerLabel)
        contentPane.add(self.printBorderColorOuterLabel)
        contentPane.add(self.printBorderWidthInnerLabel)
        contentPane.add(self.printBorderWidthOuterLabel)
        contentPane.add(self.helpButton)
        contentPane.add(self.Close)
        contentPane.add(self.cancel)
        contentPane.add(self.printBorderInner)
        contentPane.add(self.printBorderOuter)
        contentPane.add(self.printBorderColorInner)
        contentPane.add(self.printBorderColorOuter)
        contentPane.add(self.printBorderWidthInner)
        contentPane.add(self.printBorderWidthOuter)
        
    def CloseClick(self, event):
        print "CloseClick"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def printBorderColorInnerMouseUp(self, event):
        print "printBorderColorInnerMouseUp"
        
    def printBorderColorOuterMouseUp(self, event):
        print "printBorderColorOuterMouseUp"
        
    def printBorderInnerClick(self, event):
        print "printBorderInnerClick"
        
    def printBorderOuterClick(self, event):
        print "printBorderOuterClick"
        
if __name__ == "__main__":
    window = PrintBordersWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
