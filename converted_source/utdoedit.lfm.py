from common import *

#Useage:
#        import TdoEditorWindow
#        window = TdoEditorWindow.TdoEditorWindow()
#        window.visible = 1

class TdoEditorWindow(JFrame):
    def __init__(self, title='3D Object Editor'):
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
        self.setBounds(505, 155, 447, 383  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        self.keyTyped = self.FormKeyPress
        self.keyPressed = self.FormKeyDown
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyReleased = self.FormKeyUp
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poDefaultPosOnly
        #  --------------- UNHANDLED ATTRIBUTE: self.OnClose = FormClose
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.AutoScroll = False
        
        self.helpButtonImage = toolkit.createImage("../resources/TdoEditorForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(373, 286, 70, 23)
        self.ok = JButton('OK', actionPerformed=self.okClick, font=buttonFont, margin=buttonMargin)
        self.ok.setMnemonic(KeyEvent.VK_O)
        self.ok.setBounds(373, 4, 70, 21)
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(373, 27, 70, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.cancel.Cancel = True
        self.undoLast = JButton('Undo last', actionPerformed=self.undoLastClick, font=buttonFont, margin=buttonMargin)
        self.undoLast.setMnemonic(KeyEvent.VK_U)
        self.undoLast.setBounds(373, 100, 70, 21)
        self.redoLast = JButton('Redo last', actionPerformed=self.redoLastClick, font=buttonFont, margin=buttonMargin)
        self.redoLast.setMnemonic(KeyEvent.VK_R)
        self.redoLast.setBounds(373, 124, 70, 21)
        self.dragCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_dragCursorMode.png")
        self.dragCursorMode = SpeedButton(ImageIcon(self.dragCursorModeImage), actionPerformed=self.dragCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.dragCursorMode.setBounds(79, 3, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.dragCursorMode.GroupIndex = 1
        self.magnifyCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_magnifyCursorMode.png")
        self.magnifyCursorMode = SpeedButton(ImageIcon(self.magnifyCursorModeImage), actionPerformed=self.magnifyCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.magnifyCursorMode.setBounds(56, 3, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.magnifyCursorMode.GroupIndex = 1
        self.scrollCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_scrollCursorMode.png")
        self.scrollCursorMode = SpeedButton(ImageIcon(self.scrollCursorModeImage), actionPerformed=self.scrollCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.scrollCursorMode.setBounds(6, 3, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.scrollCursorMode.GroupIndex = 1
        self.addTrianglePointsCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_addTrianglePointsCursorMode.png")
        self.addTrianglePointsCursorMode = SpeedButton(ImageIcon(self.addTrianglePointsCursorModeImage), actionPerformed=self.addTrianglePointsCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.addTrianglePointsCursorMode.setBounds(104, 3, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.addTrianglePointsCursorMode.GroupIndex = 1
        self.removeTriangleCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_removeTriangleCursorMode.png")
        self.removeTriangleCursorMode = SpeedButton(ImageIcon(self.removeTriangleCursorModeImage), actionPerformed=self.removeTriangleCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.removeTriangleCursorMode.setBounds(129, 3, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.removeTriangleCursorMode.GroupIndex = 1
        self.flipTriangleCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_flipTriangleCursorMode.png")
        self.flipTriangleCursorMode = SpeedButton(ImageIcon(self.flipTriangleCursorModeImage), actionPerformed=self.flipTriangleCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.flipTriangleCursorMode.setBounds(155, 3, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.flipTriangleCursorMode.GroupIndex = 1
        self.rotateCursorModeImage = toolkit.createImage("../resources/TdoEditorForm_rotateCursorMode.png")
        self.rotateCursorMode = SpeedButton(ImageIcon(self.rotateCursorModeImage), actionPerformed=self.rotateCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.rotateCursorMode.setBounds(31, 3, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.rotateCursorMode.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.rotateCursorMode.GroupIndex = 1
        self.toolbarPanel = JPanel(layout=None)
        # -- self.toolbarPanel.setLayout(BoxLayout(self.toolbarPanel, BoxLayout.Y_AXIS))
        self.toolbarPanel.add(self.dragCursorMode)
        self.toolbarPanel.add(self.magnifyCursorMode)
        self.toolbarPanel.add(self.scrollCursorMode)
        self.toolbarPanel.add(self.addTrianglePointsCursorMode)
        self.toolbarPanel.add(self.removeTriangleCursorMode)
        self.toolbarPanel.add(self.flipTriangleCursorMode)
        self.toolbarPanel.add(self.rotateCursorMode)
        self.toolbarPanel.setBounds(-1, -2, 368, 32)
        self.mirrorTdoImage = toolkit.createImage("../resources/TdoEditorForm_mirrorTdo.png")
        self.mirrorTdo = SpeedButton('Mirror', ImageIcon(self.mirrorTdoImage), actionPerformed=self.mirrorTdoClick, font=buttonFont, margin=buttonMargin)
        self.mirrorTdo.setBounds(9, 5, 63, 25)
        self.reverseZValuesImage = toolkit.createImage("../resources/TdoEditorForm_reverseZValues.png")
        self.reverseZValues = SpeedButton('Reverse', ImageIcon(self.reverseZValuesImage), actionPerformed=self.reverseZValuesClick, font=buttonFont, margin=buttonMargin)
        self.reverseZValues.setBounds(75, 5, 72, 25)
        self.centerDrawingImage = toolkit.createImage("../resources/TdoEditorForm_centerDrawing.png")
        self.centerDrawing = SpeedButton('Scale to Fit', ImageIcon(self.centerDrawingImage), actionPerformed=self.centerDrawingClick, font=buttonFont, margin=buttonMargin)
        self.centerDrawing.setBounds(150, 5, 91, 25)
        self.resetRotationsImage = toolkit.createImage("../resources/TdoEditorForm_resetRotations.png")
        self.resetRotations = SpeedButton('Reset rotations', ImageIcon(self.resetRotationsImage), actionPerformed=self.resetRotationsClick, font=buttonFont, margin=buttonMargin)
        self.resetRotations.setBounds(244, 5, 115, 25)
        self.connectionPointLabel = JLabel('Connection point (1-xx)', font=buttonFont)
        self.connectionPointLabel.setBounds(65, 92, 113, 14)
        self.fillTriangles = JCheckBox('Fill triangles with solid', actionPerformed=self.fillTrianglesClick, font=buttonFont, margin=buttonMargin)
        self.fillTriangles.setMnemonic(KeyEvent.VK_I)
        self.fillTriangles.setBounds(194, 36, 136, 17)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.plantParts = JSpinner(SpinnerNumberModel(1, 1, 30, 1))
        self.plantParts.setBounds(8, 35, 51, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.plantParts.OnChange = plantPartsChange
        self.drawAsLabel = JLabel('Parts (1-30)', displayedMnemonic=KeyEvent.VK_P, labelFor=self.plantParts, font=buttonFont)
        self.drawAsLabel.setBounds(65, 39, 58, 14)
        self.drawLines = JCheckBox('Draw lines between triangles', actionPerformed=self.drawLinesClick, font=buttonFont, margin=buttonMargin)
        self.drawLines.setMnemonic(KeyEvent.VK_D)
        self.drawLines.setBounds(194, 55, 166, 17)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.circlePointSize = JSpinner(SpinnerNumberModel(1, 1, 30, 1))
        self.circlePointSize.setBounds(8, 62, 51, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.circlePointSize.OnChange = circlePointSizeChange
        self.Label1 = JLabel('Point size (1-30 pixels)', displayedMnemonic=KeyEvent.VK_S, labelFor=self.circlePointSize, font=buttonFont)
        self.Label1.setBounds(65, 66, 110, 14)
        self.mirrorHalf = JCheckBox('Show mirror image', actionPerformed=self.mirrorHalfClick, font=buttonFont, margin=buttonMargin)
        self.mirrorHalf.setMnemonic(KeyEvent.VK_M)
        self.mirrorHalf.setBounds(194, 74, 156, 17)
        # -- supposed to be a spin edit, not yet fuly implemented
        self.connectionPoint = JSpinner(SpinnerNumberModel(1, 1, 200, 1))
        self.connectionPoint.setBounds(8, 88, 51, 23)
        #  --------------- UNHANDLED ATTRIBUTE: self.connectionPoint.OnChange = connectionPointChange
        self.optionsPanel = JPanel(layout=None)
        # -- self.optionsPanel.setLayout(BoxLayout(self.optionsPanel, BoxLayout.Y_AXIS))
        self.optionsPanel.add(self.mirrorTdo)
        self.optionsPanel.add(self.reverseZValues)
        self.optionsPanel.add(self.centerDrawing)
        self.optionsPanel.add(self.resetRotations)
        self.optionsPanel.add(self.connectionPointLabel)
        self.optionsPanel.add(self.fillTriangles)
        self.optionsPanel.add(self.plantParts)
        self.optionsPanel.add(self.drawAsLabel)
        self.optionsPanel.add(self.drawLines)
        self.optionsPanel.add(self.circlePointSize)
        self.optionsPanel.add(self.Label1)
        self.optionsPanel.add(self.mirrorHalf)
        self.optionsPanel.add(self.connectionPoint)
        self.optionsPanel.setBounds(0, 264, 367, 117)
        self.verticalSplitter = JPanel(layout=None)
        # -- self.verticalSplitter.setLayout(BoxLayout(self.verticalSplitter, BoxLayout.Y_AXIS))
        self.verticalSplitter.setBounds(210, 4, 4, 276)
        #  --------------- UNHANDLED ATTRIBUTE: self.verticalSplitter.Cursor = crHSplit
        self.verticalSplitter.mouseMoved = self.verticalSplitterMouseMove
        self.verticalSplitter.mouseDragged = self.verticalSplitterMouseMove
        self.verticalSplitter.mouseReleased = self.verticalSplitterMouseUp
        self.verticalSplitter.mousePressed = self.verticalSplitterMouseDown
        self.horizontalSplitter = JPanel(layout=None)
        # -- self.horizontalSplitter.setLayout(BoxLayout(self.horizontalSplitter, BoxLayout.Y_AXIS))
        self.horizontalSplitter.setBounds(214, 140, 149, 4)
        #  --------------- UNHANDLED ATTRIBUTE: self.horizontalSplitter.Cursor = crVSplit
        self.horizontalSplitter.mouseMoved = self.horizontalSplitterMouseMove
        self.horizontalSplitter.mouseDragged = self.horizontalSplitterMouseMove
        self.horizontalSplitter.mouseReleased = self.horizontalSplitterMouseUp
        self.horizontalSplitter.mousePressed = self.horizontalSplitterMouseDown
        self.picturesPanel = JPanel(layout=None)
        # -- self.picturesPanel.setLayout(BoxLayout(self.picturesPanel, BoxLayout.Y_AXIS))
        self.picturesPanel.add(self.verticalSplitter)
        self.picturesPanel.add(self.horizontalSplitter)
        self.picturesPanel.setBounds(0, 29, 367, 235)
        self.renameTdo = JButton('Rename', actionPerformed=self.renameTdoClick, font=buttonFont, margin=buttonMargin)
        self.renameTdo.setMnemonic(KeyEvent.VK_N)
        self.renameTdo.setBounds(373, 63, 70, 21)
        self.writeToDXF = JButton('Write DXF...', actionPerformed=self.writeToDXFClick, font=buttonFont, margin=buttonMargin)
        self.writeToDXF.setMnemonic(KeyEvent.VK_X)
        self.writeToDXF.setBounds(373, 196, 70, 21)
        self.writeToPOV = JButton('Write POV...', actionPerformed=self.writeToPOVClick, font=buttonFont, margin=buttonMargin)
        self.writeToPOV.setMnemonic(KeyEvent.VK_P)
        self.writeToPOV.setBounds(373, 251, 70, 21)
        self.ReadFromDXF = JButton('Read DXF...', actionPerformed=self.ReadFromDXFClick, font=buttonFont, margin=buttonMargin)
        self.ReadFromDXF.setMnemonic(KeyEvent.VK_F)
        self.ReadFromDXF.setBounds(373, 222, 70, 23)
        self.clearTdo = JButton('Clear points', actionPerformed=self.clearTdoClick, font=buttonFont, margin=buttonMargin)
        self.clearTdo.setMnemonic(KeyEvent.VK_L)
        self.clearTdo.setBounds(373, 159, 70, 21)
        contentPane.add(self.helpButton)
        contentPane.add(self.ok)
        contentPane.add(self.cancel)
        contentPane.add(self.undoLast)
        contentPane.add(self.redoLast)
        contentPane.add(self.toolbarPanel)
        contentPane.add(self.optionsPanel)
        contentPane.add(self.picturesPanel)
        contentPane.add(self.renameTdo)
        contentPane.add(self.writeToDXF)
        contentPane.add(self.writeToPOV)
        contentPane.add(self.ReadFromDXF)
        contentPane.add(self.clearTdo)
        
    def FormKeyDown(self, event):
        print "FormKeyDown"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def FormKeyUp(self, event):
        print "FormKeyUp"
        
    def ReadFromDXFClick(self, event):
        print "ReadFromDXFClick"
        
    def addTrianglePointsCursorModeClick(self, event):
        print "addTrianglePointsCursorModeClick"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def centerDrawingClick(self, event):
        print "centerDrawingClick"
        
    def clearTdoClick(self, event):
        print "clearTdoClick"
        
    def dragCursorModeClick(self, event):
        print "dragCursorModeClick"
        
    def drawLinesClick(self, event):
        print "drawLinesClick"
        
    def fillTrianglesClick(self, event):
        print "fillTrianglesClick"
        
    def flipTriangleCursorModeClick(self, event):
        print "flipTriangleCursorModeClick"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def horizontalSplitterMouseDown(self, event):
        print "horizontalSplitterMouseDown"
        
    def horizontalSplitterMouseMove(self, event):
        print "horizontalSplitterMouseMove"
        
    def horizontalSplitterMouseUp(self, event):
        print "horizontalSplitterMouseUp"
        
    def magnifyCursorModeClick(self, event):
        print "magnifyCursorModeClick"
        
    def mirrorHalfClick(self, event):
        print "mirrorHalfClick"
        
    def mirrorTdoClick(self, event):
        print "mirrorTdoClick"
        
    def okClick(self, event):
        print "okClick"
        
    def redoLastClick(self, event):
        print "redoLastClick"
        
    def removeTriangleCursorModeClick(self, event):
        print "removeTriangleCursorModeClick"
        
    def renameTdoClick(self, event):
        print "renameTdoClick"
        
    def resetRotationsClick(self, event):
        print "resetRotationsClick"
        
    def reverseZValuesClick(self, event):
        print "reverseZValuesClick"
        
    def rotateCursorModeClick(self, event):
        print "rotateCursorModeClick"
        
    def scrollCursorModeClick(self, event):
        print "scrollCursorModeClick"
        
    def undoLastClick(self, event):
        print "undoLastClick"
        
    def verticalSplitterMouseDown(self, event):
        print "verticalSplitterMouseDown"
        
    def verticalSplitterMouseMove(self, event):
        print "verticalSplitterMouseMove"
        
    def verticalSplitterMouseUp(self, event):
        print "verticalSplitterMouseUp"
        
    def writeToDXFClick(self, event):
        print "writeToDXFClick"
        
    def writeToPOVClick(self, event):
        print "writeToPOVClick"
        
if __name__ == "__main__":
    window = TdoEditorWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
