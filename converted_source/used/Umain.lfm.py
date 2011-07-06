from common import *

#Useage:
#        import MainWindow
#        window = MainWindow.MainWindow()
#        window.visible = 1

class MainWindow(JFrame):
    def __init__(self, title='MainForm'):
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
        self.setBounds(297, 117, 715, 496  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.Menu = MainMenu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.OnShow = FormShow
        self.keyTyped = self.FormKeyPress
        self.keyPressed = self.FormKeyDown
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        #  --------------- UNHANDLED ATTRIBUTE: self.OnDestroy = FormDestroy
        self.keyReleased = self.FormKeyUp
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poDefaultPosOnly
        #  --------------- UNHANDLED ATTRIBUTE: self.OnClose = FormClose
        #  --------------- UNHANDLED ATTRIBUTE: self.OnResize = FormResize
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        self.visible = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.OnActivate = FormActivate
        #  --------------- UNHANDLED ATTRIBUTE: self.AutoScroll = False
        
        self.paletteImageImage = toolkit.createImage("../resources/MainForm_paletteImage.png")
        self.paletteImage = ImagePanel(ImageIcon(self.paletteImageImage))
        self.paletteImage.setBounds(147, 167, 2, 2)
        self.paletteImage.visible = 0
        self.visibleBitmapImage = toolkit.createImage("../resources/MainForm_visibleBitmap.png")
        self.visibleBitmap = ImagePanel(ImageIcon(self.visibleBitmapImage))
        self.visibleBitmap.setBounds(46, 220, 16, 16)
        self.visibleBitmap.visible = 0
        self.paramPanelOpenArrowImageImage = toolkit.createImage("../resources/MainForm_paramPanelOpenArrowImage.png")
        self.paramPanelOpenArrowImage = ImagePanel(ImageIcon(self.paramPanelOpenArrowImageImage))
        self.paramPanelOpenArrowImage.setBounds(85, 222, 13, 13)
        self.paramPanelOpenArrowImage.visible = 0
        self.paramPanelClosedArrowImageImage = toolkit.createImage("../resources/MainForm_paramPanelClosedArrowImage.png")
        self.paramPanelClosedArrowImage = ImagePanel(ImageIcon(self.paramPanelClosedArrowImageImage))
        self.paramPanelClosedArrowImage.setBounds(105, 222, 13, 13)
        self.paramPanelClosedArrowImage.visible = 0
        self.fileChangedImageImage = toolkit.createImage("../resources/MainForm_fileChangedImage.png")
        self.fileChangedImage = ImagePanel(ImageIcon(self.fileChangedImageImage))
        self.fileChangedImage.setBounds(11, 248, 16, 16)
        self.fileChangedImage.visible = 0
        self.fileNotChangedImageImage = toolkit.createImage("../resources/MainForm_fileNotChangedImage.png")
        self.fileNotChangedImage = ImagePanel(ImageIcon(self.fileNotChangedImageImage))
        self.fileNotChangedImage.setBounds(31, 248, 16, 16)
        self.fileNotChangedImage.visible = 0
        self.unregisteredExportReminderImage = toolkit.createImage("../resources/MainForm_unregisteredExportReminder.png")
        self.unregisteredExportReminder = ImagePanel(ImageIcon(self.unregisteredExportReminderImage))
        self.unregisteredExportReminder.setBounds(66, 220, 17, 16)
        self.unregisteredExportReminder.visible = 0
        self.plantBitmapsGreenImageImage = toolkit.createImage("../resources/MainForm_plantBitmapsGreenImage.png")
        self.plantBitmapsGreenImage = ImagePanel(ImageIcon(self.plantBitmapsGreenImageImage))
        self.plantBitmapsGreenImage.setBounds(70, 248, 16, 16)
        self.plantBitmapsGreenImage.visible = 0
        self.noPlantBitmapsImageImage = toolkit.createImage("../resources/MainForm_noPlantBitmapsImage.png")
        self.noPlantBitmapsImage = ImagePanel(ImageIcon(self.noPlantBitmapsImageImage))
        self.noPlantBitmapsImage.setBounds(51, 248, 16, 16)
        self.noPlantBitmapsImage.visible = 0
        self.plantBitmapsYellowImageImage = toolkit.createImage("../resources/MainForm_plantBitmapsYellowImage.png")
        self.plantBitmapsYellowImage = ImagePanel(ImageIcon(self.plantBitmapsYellowImageImage))
        self.plantBitmapsYellowImage.setBounds(90, 248, 16, 16)
        self.plantBitmapsYellowImage.visible = 0
        self.plantBitmapsRedImageImage = toolkit.createImage("../resources/MainForm_plantBitmapsRedImage.png")
        self.plantBitmapsRedImage = ImagePanel(ImageIcon(self.plantBitmapsRedImageImage))
        self.plantBitmapsRedImage.setBounds(110, 248, 16, 16)
        self.plantBitmapsRedImage.visible = 0
        self.posingLineColorLabel = JLabel('Line color', font=buttonFont)
        self.posingLineColorLabel.setBounds(50, 29, 47, 14)
        self.posingFrontfaceColorLabel = JLabel('3D Object front face color', font=buttonFont)
        self.posingFrontfaceColorLabel.setBounds(50, 49, 125, 14)
        self.posingBackfaceColorLabel = JLabel('3D Object back face color', font=buttonFont)
        self.posingBackfaceColorLabel.setBounds(50, 71, 125, 14)
        self.posingChangeColors = JCheckBox('Change this part''s colors', actionPerformed=self.changeSelectedPose, font=buttonFont, margin=buttonMargin)
        self.posingChangeColors.setBounds(4, 6, 144, 17)
        self.posingChangeAllColorsAfter = JCheckBox('and above', actionPerformed=self.changeSelectedPose, font=buttonFont, margin=buttonMargin)
        self.posingChangeAllColorsAfter.setBounds(146, 6, 73, 17)
        self.posingLineColor = JPanel(layout=None)
        # -- self.posingLineColor.setLayout(BoxLayout(self.posingLineColor, BoxLayout.Y_AXIS))
        self.posingLineColor.setBounds(26, 25, 20, 20)
        self.posingLineColor.mouseReleased = self.posingLineColorMouseUp
        self.posingFrontfaceColor = JPanel(layout=None)
        # -- self.posingFrontfaceColor.setLayout(BoxLayout(self.posingFrontfaceColor, BoxLayout.Y_AXIS))
        self.posingFrontfaceColor.setBounds(26, 47, 20, 20)
        self.posingFrontfaceColor.mouseReleased = self.posingFrontfaceColorMouseUp
        self.posingBackfaceColor = JPanel(layout=None)
        # -- self.posingBackfaceColor.setLayout(BoxLayout(self.posingBackfaceColor, BoxLayout.Y_AXIS))
        self.posingBackfaceColor.setBounds(26, 69, 20, 20)
        self.posingBackfaceColor.mouseReleased = self.posingBackfaceColorMouseUp
        self.posingColorsPanel = JPanel(layout=None)
        # -- self.posingColorsPanel.setLayout(BoxLayout(self.posingColorsPanel, BoxLayout.Y_AXIS))
        self.posingColorsPanel.add(self.posingLineColorLabel)
        self.posingColorsPanel.add(self.posingFrontfaceColorLabel)
        self.posingColorsPanel.add(self.posingBackfaceColorLabel)
        self.posingColorsPanel.add(self.posingChangeColors)
        self.posingColorsPanel.add(self.posingChangeAllColorsAfter)
        self.posingColorsPanel.add(self.posingLineColor)
        self.posingColorsPanel.add(self.posingFrontfaceColor)
        self.posingColorsPanel.add(self.posingBackfaceColor)
        self.posingColorsPanel.setBounds(476, 500, 229, 93)
        self.posingColorsPanel.visible = 0
        self.horizontalSplitter = JPanel(layout=None)
        # -- self.horizontalSplitter.setLayout(BoxLayout(self.horizontalSplitter, BoxLayout.Y_AXIS))
        self.horizontalSplitter.setBounds(8, 168, 130, 4)
        #  --------------- UNHANDLED ATTRIBUTE: self.horizontalSplitter.Cursor = crVSplit
        self.horizontalSplitter.mouseMoved = self.horizontalSplitterMouseMove
        self.horizontalSplitter.mouseDragged = self.horizontalSplitterMouseMove
        self.horizontalSplitter.mouseReleased = self.horizontalSplitterMouseUp
        self.horizontalSplitter.mousePressed = self.horizontalSplitterMouseDown
        self.verticalSplitter = JPanel(layout=None)
        # -- self.verticalSplitter.setLayout(BoxLayout(self.verticalSplitter, BoxLayout.Y_AXIS))
        self.verticalSplitter.setBounds(0, 2, 4, 169)
        #  --------------- UNHANDLED ATTRIBUTE: self.verticalSplitter.Cursor = crHSplit
        self.verticalSplitter.mouseMoved = self.verticalSplitterMouseMove
        self.verticalSplitter.mouseDragged = self.verticalSplitterMouseMove
        self.verticalSplitter.mouseReleased = self.verticalSplitterMouseUp
        self.verticalSplitter.mousePressed = self.verticalSplitterMouseDown
        self.dragCursorModeImage = toolkit.createImage("../resources/MainForm_dragCursorMode.png")
        self.dragCursorMode = SpeedButton(ImageIcon(self.dragCursorModeImage), actionPerformed=self.dragCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.dragCursorMode.setBounds(6, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.dragCursorMode.GroupIndex = 1
        self.magnifyCursorModeImage = toolkit.createImage("../resources/MainForm_magnifyCursorMode.png")
        self.magnifyCursorMode = SpeedButton(ImageIcon(self.magnifyCursorModeImage), actionPerformed=self.magnifyCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.magnifyCursorMode.setBounds(81, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.magnifyCursorMode.GroupIndex = 1
        self.scrollCursorModeImage = toolkit.createImage("../resources/MainForm_scrollCursorMode.png")
        self.scrollCursorMode = SpeedButton(ImageIcon(self.scrollCursorModeImage), actionPerformed=self.scrollCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.scrollCursorMode.setBounds(31, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.scrollCursorMode.GroupIndex = 1
        self.rotateCursorModeImage = toolkit.createImage("../resources/MainForm_rotateCursorMode.png")
        self.rotateCursorMode = SpeedButton(ImageIcon(self.rotateCursorModeImage), actionPerformed=self.rotateCursorModeClick, font=buttonFont, margin=buttonMargin)
        self.rotateCursorMode.setBounds(56, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.rotateCursorMode.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.rotateCursorMode.GroupIndex = 1
        self.centerDrawingImage = toolkit.createImage("../resources/MainForm_centerDrawing.png")
        self.centerDrawing = SpeedButton('Scale to Fit', ImageIcon(self.centerDrawingImage), actionPerformed=self.centerDrawingClick, font=buttonFont, margin=buttonMargin)
        self.centerDrawing.setBounds(214, 4, 88, 25)
        self.viewFreeFloatingImage = toolkit.createImage("../resources/MainForm_viewFreeFloating.png")
        self.viewFreeFloating = SpeedButton(ImageIcon(self.viewFreeFloatingImage), 1, actionPerformed=self.viewFreeFloatingClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.viewFreeFloating.setBounds(319, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.viewFreeFloating.GroupIndex = 5
        self.viewOneOnlyImage = toolkit.createImage("../resources/MainForm_viewOneOnly.png")
        self.viewOneOnly = SpeedButton(ImageIcon(self.viewOneOnlyImage), actionPerformed=self.viewOneOnlyClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.viewOneOnly.setBounds(346, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.viewOneOnly.GroupIndex = 5
        self.drawingAreaOnTopImage = toolkit.createImage("../resources/MainForm_drawingAreaOnTop.png")
        self.drawingAreaOnTop = SpeedButton(ImageIcon(self.drawingAreaOnTopImage), actionPerformed=self.drawingAreaOnTopClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.drawingAreaOnTop.setBounds(387, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.drawingAreaOnTop.GroupIndex = 6
        self.drawingAreaOnSideImage = toolkit.createImage("../resources/MainForm_drawingAreaOnSide.png")
        self.drawingAreaOnSide = SpeedButton(ImageIcon(self.drawingAreaOnSideImage), actionPerformed=self.drawingAreaOnSideClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.drawingAreaOnSide.setBounds(415, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.drawingAreaOnSide.GroupIndex = 6
        self.posingSelectionCursorModeImage = toolkit.createImage("../resources/MainForm_posingSelectionCursorMode.png")
        self.posingSelectionCursorMode = SpeedButton(ImageIcon(self.posingSelectionCursorModeImage), actionPerformed=self.posingSelectionCursorModeClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.posingSelectionCursorMode.setBounds(106, 4, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingSelectionCursorMode.GroupIndex = 1
        self.magnificationPercent = JComboBox(DefaultComboBoxModel())
        self.magnificationPercent.setBounds(147, 6, 60, 22)
        self.magnificationPercent.focusLost = self.magnificationPercentExit
        #  --------------- UNHANDLED ATTRIBUTE: self.magnificationPercent.Text = '100%'
        self.magnificationPercent.getModel().addElement("12%")
        self.magnificationPercent.getModel().addElement("25%")
        self.magnificationPercent.getModel().addElement("50%")
        self.magnificationPercent.getModel().addElement("75%")
        self.magnificationPercent.getModel().addElement("100%")
        self.magnificationPercent.getModel().addElement("150%")
        self.magnificationPercent.getModel().addElement("200%")
        self.magnificationPercent.getModel().addElement("300%")
        self.magnificationPercent.getModel().addElement("400%")
        self.magnificationPercent.getModel().addElement("500%")
        self.magnificationPercent.getModel().addElement("600%")
        self.magnificationPercent.getModel().addElement("700%")
        self.magnificationPercent.getModel().addElement("800%")
        self.magnificationPercent.getModel().addElement("900%")
        self.magnificationPercent.getModel().addElement("1000%")
        self.magnificationPercent.mouseClicked = self.magnificationPercentClick
        #  --------------- UNHANDLED ATTRIBUTE: self.magnificationPercent.ItemHeight = 14
        self.toolbarPanel = JPanel(layout=None)
        # -- self.toolbarPanel.setLayout(BoxLayout(self.toolbarPanel, BoxLayout.Y_AXIS))
        self.toolbarPanel.add(self.dragCursorMode)
        self.toolbarPanel.add(self.magnifyCursorMode)
        self.toolbarPanel.add(self.scrollCursorMode)
        self.toolbarPanel.add(self.rotateCursorMode)
        self.toolbarPanel.add(self.centerDrawing)
        self.toolbarPanel.add(self.viewFreeFloating)
        self.toolbarPanel.add(self.viewOneOnly)
        self.toolbarPanel.add(self.drawingAreaOnTop)
        self.toolbarPanel.add(self.drawingAreaOnSide)
        self.toolbarPanel.add(self.posingSelectionCursorMode)
        self.toolbarPanel.add(self.magnificationPercent)
        self.toolbarPanel.setBounds(6, 3, 453, 33)
        #  ------- UNHANDLED TYPE TPaintBox: progressPaintBox 
        #  --------------- UNHANDLED ATTRIBUTE: self.progressPaintBox.Top = 114
        #  --------------- UNHANDLED ATTRIBUTE: self.progressPaintBox.Height = 3
        #  --------------- UNHANDLED ATTRIBUTE: self.progressPaintBox.Width = 85
        #  --------------- UNHANDLED ATTRIBUTE: self.progressPaintBox.OnPaint = progressPaintBoxPaint
        #  --------------- UNHANDLED ATTRIBUTE: self.progressPaintBox.Left = 48
        self.plantFileChangedImageImage = toolkit.createImage("../resources/MainForm_plantFileChangedImage.png")
        self.plantFileChangedImage = ImagePanel(ImageIcon(self.plantFileChangedImageImage))
        self.plantFileChangedImage.setBounds(6, 108, 16, 16)
        self.plantBitmapsIndicatorImageImage = toolkit.createImage("../resources/MainForm_plantBitmapsIndicatorImage.png")
        self.plantBitmapsIndicatorImage = ImagePanel(ImageIcon(self.plantBitmapsIndicatorImageImage))
        self.plantBitmapsIndicatorImage.setBounds(28, 107, 16, 16)
        self.plantBitmapsIndicatorImage.mouseClicked = self.plantBitmapsIndicatorImageClick
        self.plantListDrawGrid = JTable(DefaultTableModel())
        self.plantListDrawGrid.setBounds(4, 4, 137, 103)
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.OnDragOver = plantListDrawGridDragOver
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.ColCount = 1
        self.plantListDrawGrid.mouseReleased = self.plantListDrawGridMouseUp
        self.plantListDrawGrid.mousePressed = self.plantListDrawGridMouseDown
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.OnDrawCell = plantListDrawGridDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.DefaultDrawing = False
        self.plantListDrawGrid.keyPressed = self.plantListDrawGridKeyDown
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.GridLineWidth = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.DefaultRowHeight = 16
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.OnEndDrag = plantListDrawGridEndDrag
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.ScrollBars = ssVertical
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.OnDblClick = plantListDrawGridDblClick
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.DefaultColWidth = 200
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.RowCount = 10
        #  --------------- UNHANDLED ATTRIBUTE: self.plantListDrawGrid.FixedCols = 0
        self.plantListPanel = JPanel(layout=None)
        # -- self.plantListPanel.setLayout(BoxLayout(self.plantListPanel, BoxLayout.Y_AXIS))
        # FIX UNHANDLED TYPE -- self.plantListPanel.add(self.progressPaintBox)
        self.plantListPanel.add(self.plantFileChangedImage)
        self.plantListPanel.add(self.plantBitmapsIndicatorImage)
        self.plantListPanel.add(self.plantListDrawGrid)
        self.plantListPanel.setBounds(8, 36, 147, 127)
        self.Sections_FlowersPrimaryImage = toolkit.createImage("../resources/MainForm_Sections_FlowersPrimary.png")
        self.Sections_FlowersPrimary = ImagePanel(ImageIcon(self.Sections_FlowersPrimaryImage))
        self.Sections_FlowersPrimary.setBounds(40, 42, 32, 32)
        self.Sections_GeneralImage = toolkit.createImage("../resources/MainForm_Sections_General.png")
        self.Sections_General = ImagePanel(ImageIcon(self.Sections_GeneralImage))
        self.Sections_General.setBounds(4, 4, 32, 32)
        self.Sections_InflorPrimaryImage = toolkit.createImage("../resources/MainForm_Sections_InflorPrimary.png")
        self.Sections_InflorPrimary = ImagePanel(ImageIcon(self.Sections_InflorPrimaryImage))
        self.Sections_InflorPrimary.setBounds(112, 42, 32, 32)
        self.Sections_MeristemsImage = toolkit.createImage("../resources/MainForm_Sections_Meristems.png")
        self.Sections_Meristems = ImagePanel(ImageIcon(self.Sections_MeristemsImage))
        self.Sections_Meristems.setBounds(40, 4, 32, 32)
        self.Sections_LeavesImage = toolkit.createImage("../resources/MainForm_Sections_Leaves.png")
        self.Sections_Leaves = ImagePanel(ImageIcon(self.Sections_LeavesImage))
        self.Sections_Leaves.setBounds(112, 4, 32, 32)
        self.Sections_RootTopImage = toolkit.createImage("../resources/MainForm_Sections_RootTop.png")
        self.Sections_RootTop = ImagePanel(ImageIcon(self.Sections_RootTopImage))
        self.Sections_RootTop.setBounds(112, 78, 32, 32)
        self.Sections_FruitImage = toolkit.createImage("../resources/MainForm_Sections_Fruit.png")
        self.Sections_Fruit = ImagePanel(ImageIcon(self.Sections_FruitImage))
        self.Sections_Fruit.setBounds(4, 78, 32, 32)
        self.Sections_InflorSecondaryImage = toolkit.createImage("../resources/MainForm_Sections_InflorSecondary.png")
        self.Sections_InflorSecondary = ImagePanel(ImageIcon(self.Sections_InflorSecondaryImage))
        self.Sections_InflorSecondary.setBounds(76, 78, 32, 32)
        self.Sections_InternodesImage = toolkit.createImage("../resources/MainForm_Sections_Internodes.png")
        self.Sections_Internodes = ImagePanel(ImageIcon(self.Sections_InternodesImage))
        self.Sections_Internodes.setBounds(76, 4, 32, 32)
        self.Sections_SeedlingLeavesImage = toolkit.createImage("../resources/MainForm_Sections_SeedlingLeaves.png")
        self.Sections_SeedlingLeaves = ImagePanel(ImageIcon(self.Sections_SeedlingLeavesImage))
        self.Sections_SeedlingLeaves.setBounds(4, 42, 32, 32)
        self.Sections_FlowersSecondaryImage = toolkit.createImage("../resources/MainForm_Sections_FlowersSecondary.png")
        self.Sections_FlowersSecondary = ImagePanel(ImageIcon(self.Sections_FlowersSecondaryImage))
        self.Sections_FlowersSecondary.setBounds(40, 78, 32, 32)
        self.Sections_FlowersPrimaryAdvancedImage = toolkit.createImage("../resources/MainForm_Sections_FlowersPrimaryAdvanced.png")
        self.Sections_FlowersPrimaryAdvanced = ImagePanel(ImageIcon(self.Sections_FlowersPrimaryAdvancedImage))
        self.Sections_FlowersPrimaryAdvanced.setBounds(76, 42, 32, 32)
        self.Sections_OrthogonalImage = toolkit.createImage("../resources/MainForm_Sections_Orthogonal.png")
        self.Sections_Orthogonal = ImagePanel(ImageIcon(self.Sections_OrthogonalImage))
        self.Sections_Orthogonal.setBounds(4, 114, 32, 32)
        self.sectionImagesPanel = JPanel(layout=None)
        # -- self.sectionImagesPanel.setLayout(BoxLayout(self.sectionImagesPanel, BoxLayout.Y_AXIS))
        self.sectionImagesPanel.add(self.Sections_FlowersPrimary)
        self.sectionImagesPanel.add(self.Sections_General)
        self.sectionImagesPanel.add(self.Sections_InflorPrimary)
        self.sectionImagesPanel.add(self.Sections_Meristems)
        self.sectionImagesPanel.add(self.Sections_Leaves)
        self.sectionImagesPanel.add(self.Sections_RootTop)
        self.sectionImagesPanel.add(self.Sections_Fruit)
        self.sectionImagesPanel.add(self.Sections_InflorSecondary)
        self.sectionImagesPanel.add(self.Sections_Internodes)
        self.sectionImagesPanel.add(self.Sections_SeedlingLeaves)
        self.sectionImagesPanel.add(self.Sections_FlowersSecondary)
        self.sectionImagesPanel.add(self.Sections_FlowersPrimaryAdvanced)
        self.sectionImagesPanel.add(self.Sections_Orthogonal)
        self.sectionImagesPanel.setBounds(2, 272, 149, 177)
        self.sectionImagesPanel.visible = 0
        self.plantsAsTextMemo = JTextArea(10, 10)
        self.plantsAsTextMemo.setBounds(4, 460, 151, 27)
        self.plantsAsTextMemo.visible = 0
        self.animatingLabel = JLabel('Animating! Press space bar to stop.', font=buttonFont)
        self.animatingLabel.setBounds(5, 415, 197, 14)
        self.animatingLabel.visible = 0
        self.lifeCycleGraphImage = ImagePanel() # No image was set
        self.lifeCycleGraphImage.setBounds(36, 20, 213, 25)
        self.timeLabel = JLabel('time (days)', font=buttonFont)
        self.timeLabel.setBounds(104, 48, 54, 14)
        self.selectedPlantNameLabel = JLabel('Selected plant', font=buttonFont)
        self.selectedPlantNameLabel.setBounds(10, 4, 78, 14)
        self.maxSizeAxisLabel = JLabel('%max', font=buttonFont)
        self.maxSizeAxisLabel.setBounds(4, 24, 30, 14)
        self.daysAndSizeLabel = JLabel('days, 26% max size', font=buttonFont)
        self.daysAndSizeLabel.setBounds(89, 8, 98, 14)
        self.ageAndSizeLabel = JLabel('Age', font=buttonFont)
        self.ageAndSizeLabel.setBounds(10, 6, 20, 14)
        self.animateGrowthImage = toolkit.createImage("../resources/MainForm_animateGrowth.png")
        self.animateGrowth = SpeedButton('Animate', ImageIcon(self.animateGrowthImage), actionPerformed=self.animateGrowthClick, font=buttonFont, margin=buttonMargin)
        self.animateGrowth.setBounds(194, 2, 72, 23)
        self.lifeCycleDaysEdit = JTextField('100', 10)
        self.lifeCycleDaysEdit.setBounds(36, 2, 29, 21)
        self.lifeCycleDaysEdit.focusLost = self.lifeCycleDaysEditExit
        self.lifeCycleDaysSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.lifeCycleDaysSpinImage = toolkit.createImage("../resources/MainForm_lifeCycleDaysSpin.png")
        self.lifeCycleDaysSpin.upIcon = ImageIcon(self.lifeCycleDaysSpinImage)
        self.lifeCycleDaysSpinImage = toolkit.createImage("../resources/MainForm_lifeCycleDaysSpin.png")
        self.lifeCycleDaysSpin.downIcon = ImageIcon(self.lifeCycleDaysSpinImage)
        self.lifeCycleDaysSpin.setBounds(66, 2, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.lifeCycleDaysSpin.FocusControl = lifeCycleDaysEdit
        #  --------------- UNHANDLED ATTRIBUTE: self.lifeCycleDaysSpin.OnUpClick = lifeCycleDaysSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.lifeCycleDaysSpin.OnDownClick = lifeCycleDaysSpinDownClick
        self.lifeCycleEditPanel = JPanel(layout=None)
        # -- self.lifeCycleEditPanel.setLayout(BoxLayout(self.lifeCycleEditPanel, BoxLayout.Y_AXIS))
        self.lifeCycleEditPanel.add(self.daysAndSizeLabel)
        self.lifeCycleEditPanel.add(self.ageAndSizeLabel)
        self.lifeCycleEditPanel.add(self.animateGrowth)
        self.lifeCycleEditPanel.add(self.lifeCycleDaysEdit)
        self.lifeCycleEditPanel.add(self.lifeCycleDaysSpin)
        self.lifeCycleEditPanel.setBounds(6, 64, 269, 29)
        self.lifeCycleDragger = JPanel(layout=None)
        # -- self.lifeCycleDragger.setLayout(BoxLayout(self.lifeCycleDragger, BoxLayout.Y_AXIS))
        self.lifeCycleDragger.setBounds(168, 24, 4, 17)
        #  --------------- UNHANDLED ATTRIBUTE: self.lifeCycleDragger.Cursor = crHSplit
        self.lifeCycleDragger.mouseMoved = self.lifeCycleDraggerMouseMove
        self.lifeCycleDragger.mouseDragged = self.lifeCycleDraggerMouseMove
        self.lifeCycleDragger.mouseReleased = self.lifeCycleDraggerMouseUp
        self.lifeCycleDragger.mousePressed = self.lifeCycleDraggerMouseDown
        self.lifeCyclePanel = JPanel(layout=None)
        # -- self.lifeCyclePanel.setLayout(BoxLayout(self.lifeCyclePanel, BoxLayout.Y_AXIS))
        self.lifeCyclePanel.add(self.lifeCycleGraphImage)
        self.lifeCyclePanel.add(self.timeLabel)
        self.lifeCyclePanel.add(self.selectedPlantNameLabel)
        self.lifeCyclePanel.add(self.maxSizeAxisLabel)
        self.lifeCyclePanel.add(self.lifeCycleEditPanel)
        self.lifeCyclePanel.add(self.lifeCycleDragger)
        self.lifeCyclePanel.setBounds(4, 318, 277, 95)
        self.lifeCyclePanel.visible = 0
        self.statsScrollBox = JPanel(layout=None)
        self.statsScrollBox.setBounds(284, 334, 261, 23)
        self.statsScrollBox.visible = 0
        #  ------- UNHANDLED TYPE TTabSet: tabSet 
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Font.Charset = DEFAULT_CHARSET
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.OnChange = tabSetChange
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Font.Style = []
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Font.Height = -11
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Top = 433
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.TabIndex = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Height = 21
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Tabs.Strings = [' Arrangement', ' Parameters', ' Age', ' Posing', ' Stats', ' Note']
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Width = 437
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.DitherBackground = False
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Font.Name = 'Arial'
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Font.Color = clWindowText
        #  --------------- UNHANDLED ATTRIBUTE: self.tabSet.Left = 4
        self.parametersPlantName = JLabel('Parameters for xx', font=buttonFont)
        self.parametersPlantName.setBounds(8, 8, 99, 14)
        self.parametersScrollBox = JPanel(layout=None)
        self.parametersScrollBox.setBounds(8, 44, 265, 23)
        self.sectionsComboBox = JComboBox(DefaultComboBoxModel())
        self.sectionsComboBox.setBounds(10, 20, 263, 40)
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionsComboBox.Style = csOwnerDrawFixed
        self.sectionsComboBox.getModel().addElement("General")
        self.sectionsComboBox.getModel().addElement("Etc")
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionsComboBox.OnDrawItem = sectionsComboBoxDrawItem
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionsComboBox.OnChange = sectionsComboBoxChange
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionsComboBox.ItemHeight = 34
        self.parametersPanel = JPanel(layout=None)
        # -- self.parametersPanel.setLayout(BoxLayout(self.parametersPanel, BoxLayout.Y_AXIS))
        self.parametersPanel.add(self.parametersPlantName)
        self.parametersPanel.add(self.parametersScrollBox)
        self.parametersPanel.add(self.sectionsComboBox)
        self.parametersPanel.setBounds(4, 240, 277, 73)
        self.parametersPanel.visible = 0
        self.xRotationLabel = JLabel('X', font=buttonFont)
        self.xRotationLabel.setBounds(59, 177, 7, 14)
        self.yRotationLabel = JLabel('Y', font=buttonFont)
        self.yRotationLabel.setBounds(123, 177, 8, 14)
        self.zRotationLabel = JLabel('Z', font=buttonFont)
        self.zRotationLabel.setBounds(188, 177, 7, 14)
        self.resetRotationsImage = toolkit.createImage("../resources/MainForm_resetRotations.png")
        self.resetRotations = SpeedButton('Reset Rotations', ImageIcon(self.resetRotationsImage), actionPerformed=self.resetRotationsClick, font=buttonFont, margin=buttonMargin)
        self.resetRotations.setBounds(66, 200, 109, 25)
        self.rotationLabel = JLabel('Rotation', font=buttonFont)
        self.rotationLabel.setBounds(11, 176, 39, 14)
        self.sizingLabel = JLabel('Size', font=buttonFont)
        self.sizingLabel.setBounds(29, 104, 21, 14)
        self.drawingScalePixelsPerMmLabel = JLabel('pixels/mm', font=buttonFont)
        self.drawingScalePixelsPerMmLabel.setBounds(126, 104, 47, 14)
        self.packPlantsImage = toolkit.createImage("../resources/MainForm_packPlants.png")
        self.packPlants = SpeedButton('Pack', ImageIcon(self.packPlantsImage), actionPerformed=self.packPlantsClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.packPlants.setBounds(188, 58, 65, 25)
        self.locationLabel = JLabel('Location', font=buttonFont)
        self.locationLabel.setBounds(9, 34, 41, 14)
        self.xLocationLabel = JLabel('X', font=buttonFont)
        self.xLocationLabel.setBounds(57, 35, 7, 14)
        self.yLocationLabel = JLabel('Y', font=buttonFont)
        self.yLocationLabel.setBounds(134, 35, 8, 14)
        self.locationPixelsLabel = JLabel('pixels', font=buttonFont)
        self.locationPixelsLabel.setBounds(209, 35, 28, 14)
        self.arrangementPlantName = JLabel('(no plants selected)', font=buttonFont)
        self.arrangementPlantName.setBounds(4, 4, 110, 14)
        self.alignTopsImage = toolkit.createImage("../resources/MainForm_alignTops.png")
        self.alignTops = SpeedButton(ImageIcon(self.alignTopsImage), actionPerformed=self.alignTopsClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.alignTops.setBounds(66, 58, 25, 25)
        self.alignBottomsImage = toolkit.createImage("../resources/MainForm_alignBottoms.png")
        self.alignBottoms = SpeedButton(ImageIcon(self.alignBottomsImage), actionPerformed=self.alignBottomsClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.alignBottoms.setBounds(95, 58, 25, 25)
        self.alignLeftImage = toolkit.createImage("../resources/MainForm_alignLeft.png")
        self.alignLeft = SpeedButton(ImageIcon(self.alignLeftImage), actionPerformed=self.alignLeftClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.alignLeft.setBounds(123, 58, 25, 25)
        self.alignRightImage = toolkit.createImage("../resources/MainForm_alignRight.png")
        self.alignRight = SpeedButton(ImageIcon(self.alignRightImage), actionPerformed=self.alignRightClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.alignRight.setBounds(152, 58, 25, 25)
        self.makeEqualWidthImage = toolkit.createImage("../resources/MainForm_makeEqualWidth.png")
        self.makeEqualWidth = SpeedButton('Equal Width', ImageIcon(self.makeEqualWidthImage), actionPerformed=self.makeEqualWidthClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.makeEqualWidth.setBounds(62, 128, 89, 25)
        self.makeEqualHeightImage = toolkit.createImage("../resources/MainForm_makeEqualHeight.png")
        self.makeEqualHeight = SpeedButton('Equal Height', ImageIcon(self.makeEqualHeightImage), actionPerformed=self.makeEqualHeightClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.makeEqualHeight.setBounds(154, 128, 89, 25)
        self.xRotationEdit = JTextField('-360', 10, caretUpdate=self.xRotationEditChange)
        self.xRotationEdit.setBounds(69, 174, 30, 21)
        self.xRotationEdit.focusLost = self.xRotationEditExit
        self.xRotationSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.xRotationSpinImage = toolkit.createImage("../resources/MainForm_xRotationSpin.png")
        self.xRotationSpin.upIcon = ImageIcon(self.xRotationSpinImage)
        self.xRotationSpinImage = toolkit.createImage("../resources/MainForm_xRotationSpin.png")
        self.xRotationSpin.downIcon = ImageIcon(self.xRotationSpinImage)
        self.xRotationSpin.setBounds(99, 175, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.xRotationSpin.OnUpClick = xRotationSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.xRotationSpin.OnDownClick = xRotationSpinDownClick
        self.yRotationEdit = JTextField('-360', 10, caretUpdate=self.yRotationEditChange)
        self.yRotationEdit.setBounds(133, 174, 30, 21)
        self.yRotationEdit.focusLost = self.yRotationEditExit
        self.yRotationSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.yRotationSpinImage = toolkit.createImage("../resources/MainForm_yRotationSpin.png")
        self.yRotationSpin.upIcon = ImageIcon(self.yRotationSpinImage)
        self.yRotationSpinImage = toolkit.createImage("../resources/MainForm_yRotationSpin.png")
        self.yRotationSpin.downIcon = ImageIcon(self.yRotationSpinImage)
        self.yRotationSpin.setBounds(164, 175, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.yRotationSpin.OnUpClick = yRotationSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.yRotationSpin.OnDownClick = yRotationSpinDownClick
        self.zRotationEdit = JTextField('-360', 10, caretUpdate=self.zRotationEditChange)
        self.zRotationEdit.setBounds(198, 174, 30, 21)
        self.zRotationEdit.focusLost = self.zRotationEditExit
        self.zRotationSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.zRotationSpinImage = toolkit.createImage("../resources/MainForm_zRotationSpin.png")
        self.zRotationSpin.upIcon = ImageIcon(self.zRotationSpinImage)
        self.zRotationSpinImage = toolkit.createImage("../resources/MainForm_zRotationSpin.png")
        self.zRotationSpin.downIcon = ImageIcon(self.zRotationSpinImage)
        self.zRotationSpin.setBounds(229, 175, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.zRotationSpin.OnUpClick = zRotationSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.zRotationSpin.OnDownClick = zRotationSpinDownClick
        self.drawingScaleEdit = JTextField('1.0', 10)
        self.drawingScaleEdit.setBounds(61, 100, 43, 22)
        self.drawingScaleEdit.focusLost = self.drawingScaleEditExit
        self.drawingScaleSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.drawingScaleSpinImage = toolkit.createImage("../resources/MainForm_drawingScaleSpin.png")
        self.drawingScaleSpin.upIcon = ImageIcon(self.drawingScaleSpinImage)
        self.drawingScaleSpinImage = toolkit.createImage("../resources/MainForm_drawingScaleSpin.png")
        self.drawingScaleSpin.downIcon = ImageIcon(self.drawingScaleSpinImage)
        self.drawingScaleSpin.setBounds(105, 101, 15, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.drawingScaleSpin.FocusControl = drawingScaleEdit
        #  --------------- UNHANDLED ATTRIBUTE: self.drawingScaleSpin.OnUpClick = drawingScaleSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.drawingScaleSpin.OnDownClick = drawingScaleSpinDownClick
        self.xLocationEdit = JTextField('-360', 10)
        self.xLocationEdit.setBounds(66, 32, 40, 21)
        self.xLocationEdit.focusLost = self.xLocationEditExit
        self.xLocationSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.xLocationSpinImage = toolkit.createImage("../resources/MainForm_xLocationSpin.png")
        self.xLocationSpin.upIcon = ImageIcon(self.xLocationSpinImage)
        self.xLocationSpinImage = toolkit.createImage("../resources/MainForm_xLocationSpin.png")
        self.xLocationSpin.downIcon = ImageIcon(self.xLocationSpinImage)
        self.xLocationSpin.setBounds(108, 33, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.xLocationSpin.OnUpClick = xLocationSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.xLocationSpin.OnDownClick = xLocationSpinDownClick
        self.yLocationEdit = JTextField('-360', 10)
        self.yLocationEdit.setBounds(144, 32, 40, 21)
        self.yLocationEdit.focusLost = self.yLocationEditExit
        self.yLocationSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.yLocationSpinImage = toolkit.createImage("../resources/MainForm_yLocationSpin.png")
        self.yLocationSpin.upIcon = ImageIcon(self.yLocationSpinImage)
        self.yLocationSpinImage = toolkit.createImage("../resources/MainForm_yLocationSpin.png")
        self.yLocationSpin.downIcon = ImageIcon(self.yLocationSpinImage)
        self.yLocationSpin.setBounds(187, 33, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.yLocationSpin.OnUpClick = yLocationSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.yLocationSpin.OnDownClick = yLocationSpinDownClick
        self.rotationsPanel = JPanel(layout=None)
        # -- self.rotationsPanel.setLayout(BoxLayout(self.rotationsPanel, BoxLayout.Y_AXIS))
        self.rotationsPanel.add(self.xRotationLabel)
        self.rotationsPanel.add(self.yRotationLabel)
        self.rotationsPanel.add(self.zRotationLabel)
        self.rotationsPanel.add(self.resetRotations)
        self.rotationsPanel.add(self.rotationLabel)
        self.rotationsPanel.add(self.sizingLabel)
        self.rotationsPanel.add(self.drawingScalePixelsPerMmLabel)
        self.rotationsPanel.add(self.packPlants)
        self.rotationsPanel.add(self.locationLabel)
        self.rotationsPanel.add(self.xLocationLabel)
        self.rotationsPanel.add(self.yLocationLabel)
        self.rotationsPanel.add(self.locationPixelsLabel)
        self.rotationsPanel.add(self.arrangementPlantName)
        self.rotationsPanel.add(self.alignTops)
        self.rotationsPanel.add(self.alignBottoms)
        self.rotationsPanel.add(self.alignLeft)
        self.rotationsPanel.add(self.alignRight)
        self.rotationsPanel.add(self.makeEqualWidth)
        self.rotationsPanel.add(self.makeEqualHeight)
        self.rotationsPanel.add(self.xRotationEdit)
        self.rotationsPanel.add(self.xRotationSpin)
        self.rotationsPanel.add(self.yRotationEdit)
        self.rotationsPanel.add(self.yRotationSpin)
        self.rotationsPanel.add(self.zRotationEdit)
        self.rotationsPanel.add(self.zRotationSpin)
        self.rotationsPanel.add(self.drawingScaleEdit)
        self.rotationsPanel.add(self.drawingScaleSpin)
        self.rotationsPanel.add(self.xLocationEdit)
        self.rotationsPanel.add(self.xLocationSpin)
        self.rotationsPanel.add(self.yLocationEdit)
        self.rotationsPanel.add(self.yLocationSpin)
        self.rotationsPanel.setBounds(6, 6, 273, 231)
        self.rotationsPanel.visible = 0
        self.noteLabel = JLabel('Note for daisy', font=buttonFont)
        self.noteLabel.setBounds(8, 8, 76, 14)
        self.noteEditImage = toolkit.createImage("../resources/MainForm_noteEdit.png")
        self.noteEdit = SpeedButton('Edit', ImageIcon(self.noteEditImage), actionPerformed=self.noteEditClick, font=buttonFont, margin=buttonMargin)
        self.noteEdit.setMnemonic(KeyEvent.VK_D)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.noteEdit.setBounds(182, 4, 54, 25)
        self.noteMemo = JTextArea(10, 10)
        self.noteMemo.setBounds(12, 30, 237, 15)
        #  --------------- UNHANDLED ATTRIBUTE: self.noteMemo.HideSelection = False
        self.noteMemo.editable = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.noteMemo.ScrollBars = ssVertical
        #  --------------- UNHANDLED ATTRIBUTE: self.noteMemo.WantReturns = False
        self.notePanel = JPanel(layout=None)
        # -- self.notePanel.setLayout(BoxLayout(self.notePanel, BoxLayout.Y_AXIS))
        self.notePanel.add(self.noteLabel)
        self.notePanel.add(self.noteEdit)
        scroller = JScrollPane(self.noteMemo)
        scroller.setBounds(12, 30, 237, 15)
        self.notePanel.add(scroller)
        self.notePanel.setBounds(286, 360, 258, 48)
        self.notePanel.visible = 0
        self.posingPlantName = JLabel('Posing for plant x', font=buttonFont)
        self.posingPlantName.setBounds(4, 4, 96, 14)
        self.posedPartsLabel = JLabel('Posed parts', font=buttonFont)
        self.posedPartsLabel.setBounds(4, 26, 58, 14)
        self.posingHighlightImage = toolkit.createImage("../resources/MainForm_posingHighlight.png")
        self.posingHighlight = SpeedButton(ImageIcon(self.posingHighlightImage), actionPerformed=self.posingHighlightClick, font=buttonFont, margin=buttonMargin)
        self.posingHighlight.setBounds(170, 18, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingHighlight.GroupIndex = 101
        self.posingGhostImage = toolkit.createImage("../resources/MainForm_posingGhost.png")
        self.posingGhost = SpeedButton(ImageIcon(self.posingGhostImage), actionPerformed=self.posingGhostClick, font=buttonFont, margin=buttonMargin)
        self.posingGhost.setBounds(199, 18, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingGhost.GroupIndex = 102
        self.posingNotShownImage = toolkit.createImage("../resources/MainForm_posingNotShown.png")
        self.posingNotShown = SpeedButton(ImageIcon(self.posingNotShownImage), actionPerformed=self.posingNotShownClick, font=buttonFont, margin=buttonMargin)
        self.posingNotShown.setBounds(228, 18, 25, 25)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingNotShown.GroupIndex = 103
        self.selectedPartLabel = JLabel('Part 999 (inflorescence)', font=buttonFont)
        self.selectedPartLabel.setBounds(5, 48, 117, 14)
        self.posingPosePartImage = toolkit.createImage("../resources/MainForm_posingPosePart.png")
        self.posingPosePart = SpeedButton('Pose', ImageIcon(self.posingPosePartImage), actionPerformed=self.posingPosePartClick, font=buttonFont, margin=buttonMargin)
        self.posingPosePart.setMnemonic(KeyEvent.VK_P)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.posingPosePart.setBounds(5, 64, 58, 22)
        self.posingUnposePartImage = toolkit.createImage("../resources/MainForm_posingUnposePart.png")
        self.posingUnposePart = SpeedButton('Unpose', ImageIcon(self.posingUnposePartImage), actionPerformed=self.posingUnposePartClick, font=buttonFont, margin=buttonMargin)
        self.posingUnposePart.setMnemonic(KeyEvent.VK_U)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.posingUnposePart.setBounds(68, 64, 69, 22)
        self.posingXRotationLabel = JLabel('X', font=buttonFont)
        self.posingXRotationLabel.setBounds(17, 68, 7, 14)
        self.posingYRotationLabel = JLabel('Y', font=buttonFont)
        self.posingYRotationLabel.setBounds(82, 68, 8, 14)
        self.posingZRotationLabel = JLabel('Z', font=buttonFont)
        self.posingZRotationLabel.setBounds(147, 68, 7, 14)
        self.posingScaleMultiplierPercent = JLabel('% ', font=buttonFont)
        self.posingScaleMultiplierPercent.setBounds(179, 121, 13, 14)
        self.posingScaleMultiplierLabel = JLabel('3D object scale by', font=buttonFont)
        self.posingScaleMultiplierLabel.setBounds(24, 119, 89, 14)
        self.posingLengthMultiplierPercent = JLabel('% ', font=buttonFont)
        self.posingLengthMultiplierPercent.setBounds(179, 144, 13, 14)
        self.posingLengthMultiplierLabel = JLabel('line length by', font=buttonFont)
        self.posingLengthMultiplierLabel.setBounds(50, 143, 63, 14)
        self.posingWidthMultiplierPercent = JLabel('% ', font=buttonFont)
        self.posingWidthMultiplierPercent.setBounds(179, 167, 13, 14)
        self.posingWidthMultiplierLabel = JLabel('line width by', font=buttonFont)
        self.posingWidthMultiplierLabel.setBounds(52, 166, 61, 14)
        self.hideExtraLabel = JLabel('(up to the next posed part with dependents)', font=buttonFont)
        self.hideExtraLabel.setBounds(26, 23, 213, 14)
        self.rotationDegreesLabel = JLabel('degrees', font=buttonFont)
        self.rotationDegreesLabel.setBounds(208, 67, 40, 14)
        self.posingMultiplyScaleAllPartsAfterLabel = JLabel('with dependents', font=buttonFont)
        self.posingMultiplyScaleAllPartsAfterLabel.setBounds(44, 205, 81, 14)
        self.posingHidePart = JCheckBox('Hide this part and all parts that depend on it', actionPerformed=self.changeSelectedPose, font=buttonFont, margin=buttonMargin)
        self.posingHidePart.setBounds(8, 6, 233, 17)
        self.posingXRotationEdit = JTextField('0', 10, caretUpdate=self.changeSelectedPose)
        self.posingXRotationEdit.setBounds(27, 65, 30, 21)
        self.posingXRotationEdit.focusLost = self.changeSelectedPose
        self.posingXRotationSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.posingXRotationSpinImage = toolkit.createImage("../resources/MainForm_posingXRotationSpin.png")
        self.posingXRotationSpin.upIcon = ImageIcon(self.posingXRotationSpinImage)
        self.posingXRotationSpinImage = toolkit.createImage("../resources/MainForm_posingXRotationSpin.png")
        self.posingXRotationSpin.downIcon = ImageIcon(self.posingXRotationSpinImage)
        self.posingXRotationSpin.setBounds(58, 66, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingXRotationSpin.FocusControl = posingXRotationEdit
        #  --------------- UNHANDLED ATTRIBUTE: self.posingXRotationSpin.OnUpClick = posingRotationSpinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.posingXRotationSpin.OnDownClick = posingRotationSpinDown
        self.posingYRotationEdit = JTextField('0', 10, caretUpdate=self.changeSelectedPose)
        self.posingYRotationEdit.setBounds(92, 65, 30, 21)
        self.posingYRotationEdit.focusLost = self.changeSelectedPose
        self.posingYRotationSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.posingYRotationSpinImage = toolkit.createImage("../resources/MainForm_posingYRotationSpin.png")
        self.posingYRotationSpin.upIcon = ImageIcon(self.posingYRotationSpinImage)
        self.posingYRotationSpinImage = toolkit.createImage("../resources/MainForm_posingYRotationSpin.png")
        self.posingYRotationSpin.downIcon = ImageIcon(self.posingYRotationSpinImage)
        self.posingYRotationSpin.setBounds(123, 66, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingYRotationSpin.FocusControl = posingYRotationEdit
        #  --------------- UNHANDLED ATTRIBUTE: self.posingYRotationSpin.OnUpClick = posingRotationSpinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.posingYRotationSpin.OnDownClick = posingRotationSpinDown
        self.posingZRotationEdit = JTextField('0', 10, caretUpdate=self.changeSelectedPose)
        self.posingZRotationEdit.setBounds(157, 65, 30, 21)
        self.posingZRotationEdit.focusLost = self.changeSelectedPose
        self.posingZRotationSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.posingZRotationSpinImage = toolkit.createImage("../resources/MainForm_posingZRotationSpin.png")
        self.posingZRotationSpin.upIcon = ImageIcon(self.posingZRotationSpinImage)
        self.posingZRotationSpinImage = toolkit.createImage("../resources/MainForm_posingZRotationSpin.png")
        self.posingZRotationSpin.downIcon = ImageIcon(self.posingZRotationSpinImage)
        self.posingZRotationSpin.setBounds(189, 65, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingZRotationSpin.FocusControl = posingZRotationEdit
        #  --------------- UNHANDLED ATTRIBUTE: self.posingZRotationSpin.OnUpClick = posingRotationSpinUp
        #  --------------- UNHANDLED ATTRIBUTE: self.posingZRotationSpin.OnDownClick = posingRotationSpinDown
        self.posingAddExtraRotation = JCheckBox('Add an extra rotation to this part of', actionPerformed=self.changeSelectedPose, font=buttonFont, margin=buttonMargin)
        self.posingAddExtraRotation.setBounds(8, 45, 209, 17)
        self.posingMultiplyScale = JCheckBox('Multiply this part''s', actionPerformed=self.changeSelectedPose, font=buttonFont, margin=buttonMargin)
        self.posingMultiplyScale.setBounds(8, 96, 110, 17)
        self.posingMultiplyScaleAllPartsAfter = JCheckBox('Keep doing this up to the next posed part', actionPerformed=self.changeSelectedPose, font=buttonFont, margin=buttonMargin)
        self.posingMultiplyScaleAllPartsAfter.setBounds(26, 189, 225, 17)
        self.posingScaleMultiplierEdit = JTextField('0', 10, caretUpdate=self.changeSelectedPose)
        self.posingScaleMultiplierEdit.setBounds(118, 116, 40, 21)
        self.posingScaleMultiplierEdit.focusLost = self.changeSelectedPose
        self.posingScaleMultiplierSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.posingScaleMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingScaleMultiplierSpin.png")
        self.posingScaleMultiplierSpin.upIcon = ImageIcon(self.posingScaleMultiplierSpinImage)
        self.posingScaleMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingScaleMultiplierSpin.png")
        self.posingScaleMultiplierSpin.downIcon = ImageIcon(self.posingScaleMultiplierSpinImage)
        self.posingScaleMultiplierSpin.setBounds(160, 117, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingScaleMultiplierSpin.FocusControl = posingScaleMultiplierEdit
        #  --------------- UNHANDLED ATTRIBUTE: self.posingScaleMultiplierSpin.OnUpClick = posingScaleMultiplierSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.posingScaleMultiplierSpin.OnDownClick = posingScaleMultiplierSpinDownClick
        self.posingLengthMultiplierEdit = JTextField('0', 10, caretUpdate=self.changeSelectedPose)
        self.posingLengthMultiplierEdit.setBounds(118, 140, 40, 21)
        self.posingLengthMultiplierEdit.focusLost = self.changeSelectedPose
        self.posingLengthMultiplierSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.posingLengthMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingLengthMultiplierSpin.png")
        self.posingLengthMultiplierSpin.upIcon = ImageIcon(self.posingLengthMultiplierSpinImage)
        self.posingLengthMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingLengthMultiplierSpin.png")
        self.posingLengthMultiplierSpin.downIcon = ImageIcon(self.posingLengthMultiplierSpinImage)
        self.posingLengthMultiplierSpin.setBounds(160, 141, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingLengthMultiplierSpin.FocusControl = posingLengthMultiplierEdit
        #  --------------- UNHANDLED ATTRIBUTE: self.posingLengthMultiplierSpin.OnUpClick = posingScaleMultiplierSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.posingLengthMultiplierSpin.OnDownClick = posingScaleMultiplierSpinDownClick
        self.posingWidthMultiplierEdit = JTextField('0', 10, caretUpdate=self.changeSelectedPose)
        self.posingWidthMultiplierEdit.setBounds(118, 164, 40, 21)
        self.posingWidthMultiplierEdit.focusLost = self.changeSelectedPose
        self.posingWidthMultiplierSpin = SpinButton('FIX_ME', font=buttonFont, margin=buttonMargin)
        self.posingWidthMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingWidthMultiplierSpin.png")
        self.posingWidthMultiplierSpin.upIcon = ImageIcon(self.posingWidthMultiplierSpinImage)
        self.posingWidthMultiplierSpinImage = toolkit.createImage("../resources/MainForm_posingWidthMultiplierSpin.png")
        self.posingWidthMultiplierSpin.downIcon = ImageIcon(self.posingWidthMultiplierSpinImage)
        self.posingWidthMultiplierSpin.setBounds(160, 165, 15, 19)
        #  --------------- UNHANDLED ATTRIBUTE: self.posingWidthMultiplierSpin.FocusControl = posingWidthMultiplierEdit
        #  --------------- UNHANDLED ATTRIBUTE: self.posingWidthMultiplierSpin.OnUpClick = posingScaleMultiplierSpinUpClick
        #  --------------- UNHANDLED ATTRIBUTE: self.posingWidthMultiplierSpin.OnDownClick = posingScaleMultiplierSpinDownClick
        self.posingDetailsPanel = JPanel(layout=None)
        # -- self.posingDetailsPanel.setLayout(BoxLayout(self.posingDetailsPanel, BoxLayout.Y_AXIS))
        self.posingDetailsPanel.add(self.posingXRotationLabel)
        self.posingDetailsPanel.add(self.posingYRotationLabel)
        self.posingDetailsPanel.add(self.posingZRotationLabel)
        self.posingDetailsPanel.add(self.posingScaleMultiplierPercent)
        self.posingDetailsPanel.add(self.posingScaleMultiplierLabel)
        self.posingDetailsPanel.add(self.posingLengthMultiplierPercent)
        self.posingDetailsPanel.add(self.posingLengthMultiplierLabel)
        self.posingDetailsPanel.add(self.posingWidthMultiplierPercent)
        self.posingDetailsPanel.add(self.posingWidthMultiplierLabel)
        self.posingDetailsPanel.add(self.hideExtraLabel)
        self.posingDetailsPanel.add(self.rotationDegreesLabel)
        self.posingDetailsPanel.add(self.posingMultiplyScaleAllPartsAfterLabel)
        self.posingDetailsPanel.add(self.posingHidePart)
        self.posingDetailsPanel.add(self.posingXRotationEdit)
        self.posingDetailsPanel.add(self.posingXRotationSpin)
        self.posingDetailsPanel.add(self.posingYRotationEdit)
        self.posingDetailsPanel.add(self.posingYRotationSpin)
        self.posingDetailsPanel.add(self.posingZRotationEdit)
        self.posingDetailsPanel.add(self.posingZRotationSpin)
        self.posingDetailsPanel.add(self.posingAddExtraRotation)
        self.posingDetailsPanel.add(self.posingMultiplyScale)
        self.posingDetailsPanel.add(self.posingMultiplyScaleAllPartsAfter)
        self.posingDetailsPanel.add(self.posingScaleMultiplierEdit)
        self.posingDetailsPanel.add(self.posingScaleMultiplierSpin)
        self.posingDetailsPanel.add(self.posingLengthMultiplierEdit)
        self.posingDetailsPanel.add(self.posingLengthMultiplierSpin)
        self.posingDetailsPanel.add(self.posingWidthMultiplierEdit)
        self.posingDetailsPanel.add(self.posingWidthMultiplierSpin)
        self.posingDetailsPanel.setBounds(4, 90, 252, 230)
        self.posingDetailsPanel.visible = 0
        self.posedPlantParts = JComboBox(DefaultComboBoxModel())
        self.posedPlantParts.setBounds(65, 20, 103, 22)
        #  --------------- UNHANDLED ATTRIBUTE: self.posedPlantParts.Style = csDropDownList
        #  --------------- UNHANDLED ATTRIBUTE: self.posedPlantParts.OnChange = posedPlantPartsChange
        #  --------------- UNHANDLED ATTRIBUTE: self.posedPlantParts.ItemHeight = 14
        self.posingPanel = JPanel(layout=None)
        # -- self.posingPanel.setLayout(BoxLayout(self.posingPanel, BoxLayout.Y_AXIS))
        self.posingPanel.add(self.posingPlantName)
        self.posingPanel.add(self.posedPartsLabel)
        self.posingPanel.add(self.posingHighlight)
        self.posingPanel.add(self.posingGhost)
        self.posingPanel.add(self.posingNotShown)
        self.posingPanel.add(self.selectedPartLabel)
        self.posingPanel.add(self.posingPosePart)
        self.posingPanel.add(self.posingUnposePart)
        self.posingPanel.add(self.posingDetailsPanel)
        self.posingPanel.add(self.posedPlantParts)
        self.posingPanel.setBounds(284, 6, 261, 326)
        self.posingPanel.visible = 0
        self.plantFocusPanel = JPanel(layout=None)
        # -- self.plantFocusPanel.setLayout(BoxLayout(self.plantFocusPanel, BoxLayout.Y_AXIS))
        self.plantFocusPanel.add(self.animatingLabel)
        self.plantFocusPanel.add(self.lifeCyclePanel)
        self.plantFocusPanel.add(self.statsScrollBox)
        # FIX UNHANDLED TYPE -- self.plantFocusPanel.add(self.tabSet)
        self.plantFocusPanel.add(self.parametersPanel)
        self.plantFocusPanel.add(self.rotationsPanel)
        self.plantFocusPanel.add(self.notePanel)
        self.plantFocusPanel.add(self.posingPanel)
        self.plantFocusPanel.setBounds(158, 38, 550, 457)
        
        self.MainMenu = JMenuBar()
        self.setJMenuBar(self.MainMenu)

        self.MenuFile = self.createMenu("File", "F", self.MainMenu)
        self.MenuFileNewAction = createAction(self.MenuFileNewClick, "New", None, self.MenuFile, KeyEvent.VK_N, None, None, "standard")
        self.MenuFileOpenAction = createAction(self.MenuFileOpenClick, "Open...", None, self.MenuFile, KeyEvent.VK_O, None, None, "standard")
        self.MenuFileReopen = JMenu("Reopen")
        self.MenuFileReopen.setMnemonic(KeyEvent.VK_R)
        self.MenuFile.add(self.MenuFileReopen)
        self.Recent0Action = createAction(self.Recent0Click, "0", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent0Action.menuItem.visible = 0
        self.Recent1Action = createAction(self.Recent0Click, "1", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent1Action.menuItem.visible = 0
        self.Recent2Action = createAction(self.Recent0Click, "2", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent2Action.menuItem.visible = 0
        self.Recent3Action = createAction(self.Recent0Click, "3", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent3Action.menuItem.visible = 0
        self.Recent4Action = createAction(self.Recent0Click, "4", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent4Action.menuItem.visible = 0
        self.Recent5Action = createAction(self.Recent0Click, "5", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent5Action.menuItem.visible = 0
        self.Recent6Action = createAction(self.Recent0Click, "6", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent6Action.menuItem.visible = 0
        self.Recent7Action = createAction(self.Recent0Click, "7", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent7Action.menuItem.visible = 0
        self.Recent8Action = createAction(self.Recent0Click, "8", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent8Action.menuItem.visible = 0
        self.Recent9Action = createAction(self.Recent0Click, "9", None, self.MenuFileReopen, None, None, None, "standard")
        self.Recent9Action.menuItem.visible = 0
        self.MenuFileCloseAction = createAction(self.MenuFileCloseClick, "Close", None, self.MenuFile, KeyEvent.VK_C, None, None, "standard")
        self.MenuFile.addSeparator()
        self.MenuFileSaveAction = createAction(self.MenuFileSaveClick, "Save", None, self.MenuFile, KeyEvent.VK_S, None, None, "standard")
        self.MenuFileSaveAsAction = createAction(self.MenuFileSaveAsClick, "Save As...", None, self.MenuFile, KeyEvent.VK_A, None, None, "standard")
        self.MenuFile.addSeparator()
        self.MenuFileExport = JMenu("Export")
        self.MenuFileExport.setMnemonic(KeyEvent.VK_E)
        self.MenuFile.add(self.MenuFileExport)
        self.MenuPlantExportTo3DSAction = createAction(self.MenuPlantExportTo3DSClick, "3DS...", None, self.MenuFileExport, KeyEvent.VK_3, None, None, "standard")
        self.MenuPlantExportToLWOAction = createAction(self.MenuPlantExportToLWOClick, "LWO...", None, self.MenuFileExport, KeyEvent.VK_L, None, None, "standard")
        self.MenuPlantExportToOBJAction = createAction(self.MenuPlantExportToOBJClick, "OBJ...", None, self.MenuFileExport, KeyEvent.VK_O, None, None, "standard")
        self.MenuPlantExportToDXFAction = createAction(self.MenuPlantExportToDXFClick, "DXF...", None, self.MenuFileExport, KeyEvent.VK_D, None, None, "standard")
        self.MenuPlantExportToPOVAction = createAction(self.MenuPlantExportToPOVClick, "POV INC...", None, self.MenuFileExport, KeyEvent.VK_V, None, None, "standard")
        self.MenuPlantExportToVRMLAction = createAction(self.MenuPlantExportToVRMLClick, "VRML...", None, self.MenuFileExport, KeyEvent.VK_R, None, None, "standard")
        self.MenuFileExport.addSeparator()
        self.MenuFileSaveDrawingAsAction = createAction(self.MenuFileSaveDrawingAsClick, "Bitmap...", None, self.MenuFileExport, KeyEvent.VK_B, None, None, "standard")
        self.MenuFileSaveJPEGAction = createAction(self.MenuFileSaveJPEGClick, "JPEG...", None, self.MenuFileExport, KeyEvent.VK_J, None, None, "standard")
        group = ButtonGroup()
        self.MenuFileMakePainterNozzleAction = createAction(self.MenuFileMakePainterNozzleClick, "Nozzle/Tube Bitmap...", None, self.MenuFileExport, KeyEvent.VK_N, None, None, "radiobutton")
        group.add(self.MenuFileMakePainterNozzleAction.menuItem)
        self.MenuFileMakePainterAnimationAction = createAction(self.MenuFileMakePainterAnimationClick, "Animation Files...", None, self.MenuFileExport, KeyEvent.VK_A, None, None, "standard")
        self.MenuFileMove = JMenu("Move")
        self.MenuFileMove.setMnemonic(KeyEvent.VK_M)
        self.MenuFile.add(self.MenuFileMove)
        self.MenuFilePlantMoverAction = createAction(self.MenuFilePlantMoverClick, "Plant Mover...", None, self.MenuFileMove, KeyEvent.VK_P, None, None, "standard")
        self.MenuFileTdoMoverAction = createAction(self.MenuFileTdoMoverClick, "3D Object Mover...", None, self.MenuFileMove, KeyEvent.VK_3, None, None, "standard")
        self.Reconcile3DObjects1Action = createAction(self.Reconcile3DObjects1Click, "Reconcile 3D Objects...", None, self.MenuFileMove, KeyEvent.VK_R, None, None, "standard")
        self.MenuFile.addSeparator()
        self.MenuFilePrintDrawingAction = createAction(self.MenuFilePrintDrawingClick, "Print Picture...", None, self.MenuFile, KeyEvent.VK_P, None, None, "standard")
        self.MenuFile.addSeparator()
        self.MenuFileExitAction = createAction(self.MenuFileExitClick, "Exit", None, self.MenuFile, KeyEvent.VK_X, None, None, "standard")
        
        self.MenuEdit = self.createMenu("Edit", "E", self.MainMenu)
        self.MenuEditUndoAction = createAction(self.MenuEditUndoClick, "Undo", None, self.MenuEdit, KeyEvent.VK_U, None, None, "standard")
        self.MenuEditRedoAction = createAction(self.MenuEditRedoClick, "Redo", None, self.MenuEdit, KeyEvent.VK_R, None, None, "standard")
        self.UndoMenuEditUndoRedoListAction = createAction(self.UndoMenuEditUndoRedoListClick, "Undo/Redo List...", None, self.MenuEdit, KeyEvent.VK_L, None, None, "standard")
        self.MenuEdit.addSeparator()
        self.MenuEditCutAction = createAction(self.MenuEditCutClick, "Cut", None, self.MenuEdit, KeyEvent.VK_C, None, None, "standard")
        self.MenuEditCopyAction = createAction(self.MenuEditCopyClick, "Copy", None, self.MenuEdit, KeyEvent.VK_O, None, None, "standard")
        self.MenuEditPasteAction = createAction(self.MenuEditPasteClick, "Paste", None, self.MenuEdit, KeyEvent.VK_P, None, None, "standard")
        self.MenuEditDeleteAction = createAction(self.MenuEditDeleteClick, "Delete", None, self.MenuEdit, KeyEvent.VK_D, None, None, "standard")
        self.MenuEditDuplicateAction = createAction(self.MenuEditDuplicateClick, "Duplicate", None, self.MenuEdit, KeyEvent.VK_A, None, None, "standard")
        self.MenuEdit.addSeparator()
        self.MenuEditCopyDrawingAction = createAction(self.MenuEditCopyDrawingClick, "Copy Picture", None, self.MenuEdit, KeyEvent.VK_I, None, None, "standard")
        self.MenuEditCopyAsTextAction = createAction(self.MenuEditCopyAsTextClick, "Copy To Text", None, self.MenuEdit, KeyEvent.VK_T, None, None, "standard")
        self.MenuEditPasteAsTextAction = createAction(self.MenuEditPasteAsTextClick, "Paste From Text", None, self.MenuEdit, KeyEvent.VK_F, None, None, "standard")
        self.MenuEdit.addSeparator()
        self.MenuEditPreferencesAction = createAction(self.MenuEditPreferencesClick, "Preferences...", None, self.MenuEdit, KeyEvent.VK_E, None, None, "standard")
        
        self.MenuPlant = self.createMenu("Plant", "P", self.MainMenu)
        self.MenuPlantNewAction = createAction(self.MenuPlantNewClick, "Create New...", None, self.MenuPlant, KeyEvent.VK_N, None, None, "standard")
        self.MenuPlantNewUsingLastWizardSettingsAction = createAction(self.MenuPlantNewUsingLastWizardSettingsClick, "Create Same as Last", None, self.MenuPlant, KeyEvent.VK_L, None, None, "standard")
        self.MenuPlant.addSeparator()
        self.MenuPlantBreedAction = createAction(self.MenuPlantBreedClick, "Breed", None, self.MenuPlant, KeyEvent.VK_B, None, None, "standard")
        self.MenuPlantMakeTimeSeriesAction = createAction(self.MenuPlantMakeTimeSeriesClick, "Make Time Series", None, self.MenuPlant, KeyEvent.VK_T, None, None, "standard")
        self.MenuPlant.addSeparator()
        self.MenuPlantRandomizeAction = createAction(self.MenuPlantRandomizeClick, "Randomize", None, self.MenuPlant, KeyEvent.VK_R, None, None, "standard")
        self.MenuPlantZeroRotationsAction = createAction(self.MenuPlantZeroRotationsClick, "Reset Rotations", None, self.MenuPlant, KeyEvent.VK_S, None, None, "standard")
        self.MenuPlantAnimateAction = createAction(self.MenuPlantAnimateClick, "Animate through Life Cycle", None, self.MenuPlant, KeyEvent.VK_A, None, None, "standard")
        self.MenuPlant.addSeparator()
        self.MenuPlantRenameAction = createAction(self.MenuPlantRenameClick, "Rename...", None, self.MenuPlant, KeyEvent.VK_E, None, None, "standard")
        self.MenuPlantEditNoteAction = createAction(self.MenuPlantEditNoteClick, "Edit Note...", None, self.MenuPlant, KeyEvent.VK_D, None, None, "standard")
        
        self.MenuLayout = self.createMenu("Layout", "L", self.MainMenu)
        self.MenuLayoutSelectAllAction = createAction(self.MenuLayoutSelectAllClick, "Select All", None, self.MenuLayout, KeyEvent.VK_A, None, None, "standard")
        self.MenuLayoutDeselectAction = createAction(self.MenuLayoutDeselectClick, "Select None", None, self.MenuLayout, KeyEvent.VK_N, None, None, "standard")
        self.MenuLayout.addSeparator()
        self.MenuLayoutScaleToFitAction = createAction(self.MenuLayoutScaleToFitClick, "Scale to Fit", None, self.MenuLayout, KeyEvent.VK_F, None, None, "standard")
        self.MenuLayoutAlign = JMenu("Align")
        self.MenuLayoutAlign.setMnemonic(KeyEvent.VK_L)
        self.MenuLayout.add(self.MenuLayoutAlign)
        self.MenuLayoutAlignTopsAction = createAction(self.MenuLayoutAlignTopsClick, "Tops", None, self.MenuLayoutAlign, KeyEvent.VK_T, None, None, "standard")
        self.MenuLayoutAlignBottomsAction = createAction(self.MenuLayoutAlignBottomsClick, "Bottoms", None, self.MenuLayoutAlign, KeyEvent.VK_B, None, None, "standard")
        self.MenuLayoutAlignLeftSidesAction = createAction(self.MenuLayoutAlignLeftSidesClick, "Left Sides", None, self.MenuLayoutAlign, KeyEvent.VK_L, None, None, "standard")
        self.MenuLayoutAlignRightSidesAction = createAction(self.MenuLayoutAlignRightSidesClick, "Right Sides", None, self.MenuLayoutAlign, KeyEvent.VK_R, None, None, "standard")
        self.MenuLayoutMakeBouquetAction = createAction(self.MenuLayoutMakeBouquetClick, "Make into Bouquet", None, self.MenuLayoutAlign, KeyEvent.VK_Q, None, None, "standard")
        self.MenuLayoutSize = JMenu("Size")
        self.MenuLayoutSize.setMnemonic(KeyEvent.VK_Z)
        self.MenuLayout.add(self.MenuLayoutSize)
        self.MenuLayoutSizeSameWidthAction = createAction(self.MenuLayoutSizeSameWidthClick, "Equal Width", None, self.MenuLayoutSize, KeyEvent.VK_W, None, None, "standard")
        self.MenuLayoutSizeSameHeightAction = createAction(self.MenuLayoutSizeSameHeightClick, "Equal Height", None, self.MenuLayoutSize, KeyEvent.VK_H, None, None, "standard")
        self.MenuLayoutPackAction = createAction(self.MenuLayoutPackClick, "Pack", None, self.MenuLayout, KeyEvent.VK_P, None, None, "standard")
        self.MenuLayout.addSeparator()
        self.MenuLayoutBringForwardAction = createAction(self.MenuLayoutBringForwardClick, "Bring Forward", None, self.MenuLayout, KeyEvent.VK_R, None, None, "standard")
        self.MenuLayoutSendBackAction = createAction(self.MenuLayoutSendBackClick, "Send Back", None, self.MenuLayout, KeyEvent.VK_B, None, None, "standard")
        self.MenuLayout.addSeparator()
        self.MenuLayoutShowAction = createAction(self.MenuLayoutShowClick, "Show", None, self.MenuLayout, KeyEvent.VK_S, None, None, "standard")
        self.MenuLayoutHideAction = createAction(self.MenuLayoutHideClick, "Hide", None, self.MenuLayout, KeyEvent.VK_H, None, None, "standard")
        self.MenuLayoutHideOthersAction = createAction(self.MenuLayoutHideOthersClick, "Hide Others", None, self.MenuLayout, KeyEvent.VK_O, None, None, "standard")
        
        self.MenuOptions = self.createMenu("Options", "O", self.MainMenu)
        self.MenuOptionsDrawAs = JMenu("Draw Using")
        self.MenuOptionsDrawAs.setMnemonic(KeyEvent.VK_D)
        self.MenuOptions.add(self.MenuOptionsDrawAs)
        group = ButtonGroup()
        self.MenuOptionsFastDrawAction = createAction(self.MenuOptionsFastDrawClick, "Bounding Boxes", None, self.MenuOptionsDrawAs, KeyEvent.VK_B, None, None, "radiobutton")
        group.add(self.MenuOptionsFastDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsFastDraw.GroupIndex = 1
        self.MenuOptionsMediumDrawAction = createAction(self.MenuOptionsMediumDrawClick, "Wire Frames", None, self.MenuOptionsDrawAs, KeyEvent.VK_W, None, None, "radiobutton")
        group.add(self.MenuOptionsMediumDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsMediumDraw.GroupIndex = 1
        self.MenuOptionsBestDrawAction = createAction(self.MenuOptionsBestDrawClick, "Solids", None, self.MenuOptionsDrawAs, KeyEvent.VK_S, None, None, "radiobutton")
        group.add(self.MenuOptionsBestDrawAction.menuItem)
        self.MenuOptionsBestDrawAction.setChecked(1)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsBestDraw.GroupIndex = 1
        self.MenuOptionsCustomDrawAction = createAction(self.MenuOptionsCustomDrawClick, "Custom...", None, self.MenuOptionsDrawAs, KeyEvent.VK_C, None, None, "radiobutton")
        group.add(self.MenuOptionsCustomDrawAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsCustomDraw.GroupIndex = 1
        self.MenuLayoutView = JMenu("View What Plants")
        self.MenuLayoutView.setMnemonic(KeyEvent.VK_V)
        self.MenuOptions.add(self.MenuLayoutView)
        group = ButtonGroup()
        self.MenuLayoutViewFreeFloatingAction = createAction(self.MenuLayoutViewFreeFloatingClick, "All Plants", None, self.MenuLayoutView, KeyEvent.VK_A, None, None, "radiobutton")
        group.add(self.MenuLayoutViewFreeFloatingAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuLayoutViewFreeFloating.GroupIndex = 2
        self.MenuLayoutViewOnePlantAtATimeAction = createAction(self.MenuLayoutViewOnePlantAtATimeClick, "One Plant at a Time", None, self.MenuLayoutView, KeyEvent.VK_O, None, None, "radiobutton")
        group.add(self.MenuLayoutViewOnePlantAtATimeAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuLayoutViewOnePlantAtATime.GroupIndex = 2
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuLayoutView.GroupIndex = 1
        self.MenuLayoutDrawingAreaOn = JMenu("Place Drawing Area")
        self.MenuLayoutDrawingAreaOn.setMnemonic(KeyEvent.VK_A)
        self.MenuOptions.add(self.MenuLayoutDrawingAreaOn)
        group = ButtonGroup()
        self.MenuLayoutHorizontalOrientationAction = createAction(self.MenuLayoutHorizontalOrientationClick, "On Top", None, self.MenuLayoutDrawingAreaOn, KeyEvent.VK_T, None, None, "radiobutton")
        group.add(self.MenuLayoutHorizontalOrientationAction.menuItem)
        self.MenuLayoutHorizontalOrientationAction.setChecked(1)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuLayoutHorizontalOrientation.GroupIndex = 3
        self.MenuLayoutVerticalOrientationAction = createAction(self.MenuLayoutVerticalOrientationClick, "On Left Side", None, self.MenuLayoutDrawingAreaOn, KeyEvent.VK_L, None, None, "radiobutton")
        group.add(self.MenuLayoutVerticalOrientationAction.menuItem)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuLayoutVerticalOrientation.GroupIndex = 3
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuLayoutDrawingAreaOn.GroupIndex = 1
        self.MenuOptionsDrawRectangles = JMenu("Draw Rectangles")
        self.MenuOptionsDrawRectangles.setMnemonic(KeyEvent.VK_R)
        self.MenuOptions.add(self.MenuOptionsDrawRectangles)
        self.MenuOptionsShowSelectionRectanglesAction = createAction(self.MenuOptionsShowSelectionRectanglesClick, "Around Selected Plants", None, self.MenuOptionsDrawRectangles, KeyEvent.VK_S, None, None, "checkbox")
        self.MenuOptionsShowSelectionRectanglesAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsShowSelectionRectangles.GroupIndex = 1
        self.MenuOptionsShowBoundsRectanglesAction = createAction(self.MenuOptionsShowBoundsRectanglesClick, "Around All Plants", None, self.MenuOptionsDrawRectangles, KeyEvent.VK_A, None, None, "checkbox")
        self.MenuOptionsShowBoundsRectanglesAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsShowBoundsRectangles.GroupIndex = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsDrawRectangles.GroupIndex = 1
        self.MenuOptionsPosing = JMenu("Posing")
        self.MenuOptionsPosing.setMnemonic(KeyEvent.VK_P)
        self.MenuOptions.add(self.MenuOptionsPosing)
        self.MenuOptionsHighlightPosedPartsAction = createAction(self.MenuOptionsHighlightPosedPartsClick, "Highlight Posed Parts", None, self.MenuOptionsPosing, KeyEvent.VK_H, None, None, "checkbox")
        self.MenuOptionsHighlightPosedPartsAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsHighlightPosedParts.GroupIndex = 1
        self.MenuOptionsGhostHiddenPartsAction = createAction(self.MenuOptionsGhostHiddenPartsClick, "Ghost Hidden Parts", None, self.MenuOptionsPosing, KeyEvent.VK_G, None, None, "checkbox")
        self.MenuOptionsGhostHiddenPartsAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsGhostHiddenParts.GroupIndex = 1
        self.MenuOptionsHidePosingAction = createAction(self.MenuOptionsHidePosingClick, "Ignore All Posing", None, self.MenuOptionsPosing, KeyEvent.VK_I, None, None, "checkbox")
        self.MenuOptionsHidePosingAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsHidePosing.GroupIndex = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsPosing.GroupIndex = 1
        self.MenuOptionsHints = JMenu("Hints")
        self.MenuOptionsHints.setMnemonic(KeyEvent.VK_H)
        self.MenuOptions.add(self.MenuOptionsHints)
        self.MenuOptionsShowLongButtonHintsAction = createAction(self.MenuOptionsShowLongButtonHintsClick, "Show Long Button Hints", None, self.MenuOptionsHints, KeyEvent.VK_H, None, None, "checkbox")
        self.MenuOptionsShowLongButtonHintsAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsShowLongButtonHints.GroupIndex = 1
        self.MenuOptionsShowParameterHintsAction = createAction(self.MenuOptionsShowParameterHintsClick, "Show Parameter Hints", None, self.MenuOptionsHints, KeyEvent.VK_M, None, None, "checkbox")
        self.MenuOptionsShowParameterHintsAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsShowParameterHints.GroupIndex = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsHints.GroupIndex = 1
        self.MenuOptions.addSeparator()
        #  --------------- UNHANDLED ATTRIBUTE: self.N17.GroupIndex = 1
        self.MenuOptionsUsePlantBitmapsAction = createAction(self.MenuOptionsUsePlantBitmapsClick, "Use Plant Bitmaps", None, self.MenuOptions, KeyEvent.VK_B, None, None, "checkbox")
        self.MenuOptionsUsePlantBitmapsAction.setChecked(0)
        #  --------------- UNHANDLED ATTRIBUTE: self.MenuOptionsUsePlantBitmaps.GroupIndex = 1
        
        self.MenuWindow = self.createMenu("Window", "W", self.MainMenu)
        self.MenuWindowBreederAction = createAction(self.MenuWindowBreederClick, "Breeder", None, self.MenuWindow, KeyEvent.VK_B, None, None, "standard")
        self.MenuWindowTimeSeriesAction = createAction(self.MenuWindowTimeSeriesClick, "Time Series", None, self.MenuWindow, KeyEvent.VK_T, None, None, "standard")
        self.MenuWindow.addSeparator()
        self.MenuWindowNumericalExceptionsAction = createAction(self.MenuWindowNumericalExceptionsClick, "Messages", None, self.MenuWindow, KeyEvent.VK_M, None, None, "standard")
        
        self.MenuHelp = self.createMenu("Help", "H", self.MainMenu)
        self.MenuHelpTopicsAction = createAction(self.MenuHelpTopicsClick, "Help Topics", None, self.MenuHelp, KeyEvent.VK_T, None, None, "standard")
        self.MenuHelpSuperSpeedTourAction = createAction(self.MenuHelpSuperSpeedTourClick, "Super-Speed Tour", None, self.MenuHelp, KeyEvent.VK_S, None, None, "standard")
        self.MenuHelpTutorialAction = createAction(self.MenuHelpTutorialClick, "Tutorial", None, self.MenuHelp, KeyEvent.VK_U, None, None, "standard")
        self.MenuHelp.addSeparator()
        self.MenuHelpRegisterAction = createAction(self.MenuHelpRegisterClick, "Register...", None, self.MenuHelp, KeyEvent.VK_R, None, None, "standard")
        self.MenuHelp.addSeparator()
        self.MenuHelpAboutAction = createAction(self.MenuHelpAboutClick, "About PlantStudio", None, self.MenuHelp, KeyEvent.VK_A, None, None, "standard")
        
        #  --------------- UNHANDLED ATTRIBUTE: self.MainMenu.Top = 179
        #  --------------- UNHANDLED ATTRIBUTE: self.MainMenu.Left = 34
        
        self.PlantPopupMenu = JPopupMenu()
        self.PopupMenuRandomizeAction = createAction(self.PopupMenuRandomizeClick, "Randomize", None, self.PlantPopupMenu, KeyEvent.VK_R, None, None, "standard")
        self.PlantPopupMenu.addSeparator()
        self.PopupMenuCutAction = createAction(self.PopupMenuCutClick, "Cut", None, self.PlantPopupMenu, KeyEvent.VK_C, None, None, "standard")
        self.PopupMenuCopyAction = createAction(self.PopupMenuCopyClick, "Copy", None, self.PlantPopupMenu, KeyEvent.VK_O, None, None, "standard")
        self.PopupMenuPasteAction = createAction(self.PopupMenuPasteClick, "Paste", None, self.PlantPopupMenu, KeyEvent.VK_P, None, None, "standard")
        self.PlantPopupMenu.addSeparator()
        self.PopupMenuRenameAction = createAction(self.PopupMenuRenameClick, "Rename...", None, self.PlantPopupMenu, KeyEvent.VK_N, None, None, "standard")
        self.PopupMenuEditNoteAction = createAction(self.PopupMenuEditNoteClick, "Edit Note...", None, self.PlantPopupMenu, KeyEvent.VK_E, None, None, "standard")
        self.PopupMenuAnimateAction = createAction(self.PopupMenuAnimateClick, "Animate", None, self.PlantPopupMenu, KeyEvent.VK_A, None, None, "standard")
        self.PopupMenuBreedAction = createAction(self.PopupMenuBreedClick, "Breed", None, self.PlantPopupMenu, KeyEvent.VK_B, None, None, "standard")
        self.PopupMenuMakeTimeSeriesAction = createAction(self.PopupMenuMakeTimeSeriesClick, "Make Time Series", None, self.PlantPopupMenu, KeyEvent.VK_T, None, None, "standard")
        self.PopupMenuZeroRotationsAction = createAction(self.PopupMenuZeroRotationsClick, "Reset Rotations", None, self.PlantPopupMenu, KeyEvent.VK_S, None, None, "standard")
        #  --------------- UNHANDLED ATTRIBUTE: self.PlantPopupMenu.Top = 179
        #  --------------- UNHANDLED ATTRIBUTE: self.PlantPopupMenu.AutoPopup = False
        #  --------------- UNHANDLED ATTRIBUTE: self.PlantPopupMenu.Left = 122
        #  ------- UNHANDLED TYPE TPrintDialog: PrintDialog 
        #  --------------- UNHANDLED ATTRIBUTE: self.PrintDialog.Top = 179
        #  --------------- UNHANDLED ATTRIBUTE: self.PrintDialog.Left = 4
        #  ------- UNHANDLED TYPE TTimer: animateTimer 
        #  --------------- UNHANDLED ATTRIBUTE: self.animateTimer.Interval = 100
        #  --------------- UNHANDLED ATTRIBUTE: self.animateTimer.Enabled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.animateTimer.OnTimer = animateTimerTimer
        #  --------------- UNHANDLED ATTRIBUTE: self.animateTimer.Top = 212
        #  --------------- UNHANDLED ATTRIBUTE: self.animateTimer.Left = 7
        
        self.paramPopupMenu = JPopupMenu()
        self.paramPopupMenuExpandAction = createAction(self.paramPopupMenuExpandClick, "Expand Panel", None, self.paramPopupMenu, KeyEvent.VK_E, None, None, "standard")
        self.paramPopupMenuCollapseAction = createAction(self.paramPopupMenuCollapseClick, "Collapse Panel", None, self.paramPopupMenu, KeyEvent.VK_C, None, None, "standard")
        self.paramPopupMenu.addSeparator()
        self.paramPopupMenuExpandAllInSectionAction = createAction(self.paramPopupMenuExpandAllInSectionClick, "Expand All Panels in This Section", None, self.paramPopupMenu, KeyEvent.VK_X, None, None, "standard")
        self.paramPopupMenuCollapseAllInSectionAction = createAction(self.paramPopupMenuCollapseAllInSectionClick, "Collapse All Panels in This Section", None, self.paramPopupMenu, KeyEvent.VK_O, None, None, "standard")
        self.paramPopupMenu.addSeparator()
        self.paramPopupMenuCopyNameAction = createAction(self.paramPopupMenuCopyNameClick, "Copy Parameter Name", None, self.paramPopupMenu, KeyEvent.VK_N, None, None, "standard")
        self.paramPopupMenu.addSeparator()
        self.paramPopupMenuHelpAction = createAction(self.paramPopupMenuHelpClick, "Go to Help for This Type of Parameter Panel", None, self.paramPopupMenu, KeyEvent.VK_H, None, None, "standard")
        self.sectionPopupMenuHelpAction = createAction(self.sectionPopupMenuHelpClick, "Go to Help for This Parameter Section", None, self.paramPopupMenu, KeyEvent.VK_S, None, None, "standard")
        #  --------------- UNHANDLED ATTRIBUTE: self.paramPopupMenu.Top = 179
        #  --------------- UNHANDLED ATTRIBUTE: self.paramPopupMenu.Left = 63
        self.lifeCyclePanel.addMouseListener(MenuPopupMouseListener(self.PlantPopupMenu))
        self.parametersScrollBox.addMouseListener(MenuPopupMouseListener(self.paramPopupMenu))
        contentPane.add(self.paletteImage)
        contentPane.add(self.visibleBitmap)
        contentPane.add(self.paramPanelOpenArrowImage)
        contentPane.add(self.paramPanelClosedArrowImage)
        contentPane.add(self.fileChangedImage)
        contentPane.add(self.fileNotChangedImage)
        contentPane.add(self.unregisteredExportReminder)
        contentPane.add(self.plantBitmapsGreenImage)
        contentPane.add(self.noPlantBitmapsImage)
        contentPane.add(self.plantBitmapsYellowImage)
        contentPane.add(self.plantBitmapsRedImage)
        contentPane.add(self.posingColorsPanel)
        contentPane.add(self.horizontalSplitter)
        contentPane.add(self.verticalSplitter)
        contentPane.add(self.toolbarPanel)
        contentPane.add(self.plantListPanel)
        contentPane.add(self.sectionImagesPanel)
        scroller = JScrollPane(self.plantsAsTextMemo)
        scroller.setBounds(4, 460, 151, 27)
        contentPane.add(scroller)
        contentPane.add(self.plantFocusPanel)
        
    def None(self, event):
        print "None"
        
    def FormKeyDown(self, event):
        print "FormKeyDown"
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def FormKeyUp(self, event):
        print "FormKeyUp"
        
    def MenuEditCopyAsTextClick(self, event):
        print "MenuEditCopyAsTextClick"
        
    def MenuEditCopyClick(self, event):
        print "MenuEditCopyClick"
        
    def MenuEditCopyDrawingClick(self, event):
        print "MenuEditCopyDrawingClick"
        
    def MenuEditCutClick(self, event):
        print "MenuEditCutClick"
        
    def MenuEditDeleteClick(self, event):
        print "MenuEditDeleteClick"
        
    def MenuEditDuplicateClick(self, event):
        print "MenuEditDuplicateClick"
        
    def MenuEditPasteAsTextClick(self, event):
        print "MenuEditPasteAsTextClick"
        
    def MenuEditPasteClick(self, event):
        print "MenuEditPasteClick"
        
    def MenuEditPreferencesClick(self, event):
        print "MenuEditPreferencesClick"
        
    def MenuEditRedoClick(self, event):
        print "MenuEditRedoClick"
        
    def MenuEditUndoClick(self, event):
        print "MenuEditUndoClick"
        
    def MenuFileCloseClick(self, event):
        print "MenuFileCloseClick"
        
    def MenuFileExitClick(self, event):
        print "MenuFileExitClick"
        
    def MenuFileMakePainterAnimationClick(self, event):
        print "MenuFileMakePainterAnimationClick"
        
    def MenuFileMakePainterNozzleClick(self, event):
        print "MenuFileMakePainterNozzleClick"
        
    def MenuFileNewClick(self, event):
        print "MenuFileNewClick"
        
    def MenuFileOpenClick(self, event):
        print "MenuFileOpenClick"
        
    def MenuFilePlantMoverClick(self, event):
        print "MenuFilePlantMoverClick"
        
    def MenuFilePrintDrawingClick(self, event):
        print "MenuFilePrintDrawingClick"
        
    def MenuFileSaveAsClick(self, event):
        print "MenuFileSaveAsClick"
        
    def MenuFileSaveClick(self, event):
        print "MenuFileSaveClick"
        
    def MenuFileSaveDrawingAsClick(self, event):
        print "MenuFileSaveDrawingAsClick"
        
    def MenuFileSaveJPEGClick(self, event):
        print "MenuFileSaveJPEGClick"
        
    def MenuFileTdoMoverClick(self, event):
        print "MenuFileTdoMoverClick"
        
    def MenuHelpAboutClick(self, event):
        print "MenuHelpAboutClick"
        
    def MenuHelpRegisterClick(self, event):
        print "MenuHelpRegisterClick"
        
    def MenuHelpSuperSpeedTourClick(self, event):
        print "MenuHelpSuperSpeedTourClick"
        
    def MenuHelpTopicsClick(self, event):
        print "MenuHelpTopicsClick"
        
    def MenuHelpTutorialClick(self, event):
        print "MenuHelpTutorialClick"
        
    def MenuLayoutAlignBottomsClick(self, event):
        print "MenuLayoutAlignBottomsClick"
        
    def MenuLayoutAlignLeftSidesClick(self, event):
        print "MenuLayoutAlignLeftSidesClick"
        
    def MenuLayoutAlignRightSidesClick(self, event):
        print "MenuLayoutAlignRightSidesClick"
        
    def MenuLayoutAlignTopsClick(self, event):
        print "MenuLayoutAlignTopsClick"
        
    def MenuLayoutBringForwardClick(self, event):
        print "MenuLayoutBringForwardClick"
        
    def MenuLayoutDeselectClick(self, event):
        print "MenuLayoutDeselectClick"
        
    def MenuLayoutHideClick(self, event):
        print "MenuLayoutHideClick"
        
    def MenuLayoutHideOthersClick(self, event):
        print "MenuLayoutHideOthersClick"
        
    def MenuLayoutHorizontalOrientationClick(self, event):
        print "MenuLayoutHorizontalOrientationClick"
        
    def MenuLayoutMakeBouquetClick(self, event):
        print "MenuLayoutMakeBouquetClick"
        
    def MenuLayoutPackClick(self, event):
        print "MenuLayoutPackClick"
        
    def MenuLayoutScaleToFitClick(self, event):
        print "MenuLayoutScaleToFitClick"
        
    def MenuLayoutSelectAllClick(self, event):
        print "MenuLayoutSelectAllClick"
        
    def MenuLayoutSendBackClick(self, event):
        print "MenuLayoutSendBackClick"
        
    def MenuLayoutShowClick(self, event):
        print "MenuLayoutShowClick"
        
    def MenuLayoutSizeSameHeightClick(self, event):
        print "MenuLayoutSizeSameHeightClick"
        
    def MenuLayoutSizeSameWidthClick(self, event):
        print "MenuLayoutSizeSameWidthClick"
        
    def MenuLayoutVerticalOrientationClick(self, event):
        print "MenuLayoutVerticalOrientationClick"
        
    def MenuLayoutViewFreeFloatingClick(self, event):
        print "MenuLayoutViewFreeFloatingClick"
        
    def MenuLayoutViewOnePlantAtATimeClick(self, event):
        print "MenuLayoutViewOnePlantAtATimeClick"
        
    def MenuOptionsBestDrawClick(self, event):
        print "MenuOptionsBestDrawClick"
        
    def MenuOptionsCustomDrawClick(self, event):
        print "MenuOptionsCustomDrawClick"
        
    def MenuOptionsFastDrawClick(self, event):
        print "MenuOptionsFastDrawClick"
        
    def MenuOptionsGhostHiddenPartsClick(self, event):
        print "MenuOptionsGhostHiddenPartsClick"
        
    def MenuOptionsHidePosingClick(self, event):
        print "MenuOptionsHidePosingClick"
        
    def MenuOptionsHighlightPosedPartsClick(self, event):
        print "MenuOptionsHighlightPosedPartsClick"
        
    def MenuOptionsMediumDrawClick(self, event):
        print "MenuOptionsMediumDrawClick"
        
    def MenuOptionsShowBoundsRectanglesClick(self, event):
        print "MenuOptionsShowBoundsRectanglesClick"
        
    def MenuOptionsShowLongButtonHintsClick(self, event):
        print "MenuOptionsShowLongButtonHintsClick"
        
    def MenuOptionsShowParameterHintsClick(self, event):
        print "MenuOptionsShowParameterHintsClick"
        
    def MenuOptionsShowSelectionRectanglesClick(self, event):
        print "MenuOptionsShowSelectionRectanglesClick"
        
    def MenuOptionsUsePlantBitmapsClick(self, event):
        print "MenuOptionsUsePlantBitmapsClick"
        
    def MenuPlantAnimateClick(self, event):
        print "MenuPlantAnimateClick"
        
    def MenuPlantBreedClick(self, event):
        print "MenuPlantBreedClick"
        
    def MenuPlantEditNoteClick(self, event):
        print "MenuPlantEditNoteClick"
        
    def MenuPlantExportTo3DSClick(self, event):
        print "MenuPlantExportTo3DSClick"
        
    def MenuPlantExportToDXFClick(self, event):
        print "MenuPlantExportToDXFClick"
        
    def MenuPlantExportToLWOClick(self, event):
        print "MenuPlantExportToLWOClick"
        
    def MenuPlantExportToOBJClick(self, event):
        print "MenuPlantExportToOBJClick"
        
    def MenuPlantExportToPOVClick(self, event):
        print "MenuPlantExportToPOVClick"
        
    def MenuPlantExportToVRMLClick(self, event):
        print "MenuPlantExportToVRMLClick"
        
    def MenuPlantMakeTimeSeriesClick(self, event):
        print "MenuPlantMakeTimeSeriesClick"
        
    def MenuPlantNewClick(self, event):
        print "MenuPlantNewClick"
        
    def MenuPlantNewUsingLastWizardSettingsClick(self, event):
        print "MenuPlantNewUsingLastWizardSettingsClick"
        
    def MenuPlantRandomizeClick(self, event):
        print "MenuPlantRandomizeClick"
        
    def MenuPlantRenameClick(self, event):
        print "MenuPlantRenameClick"
        
    def MenuPlantZeroRotationsClick(self, event):
        print "MenuPlantZeroRotationsClick"
        
    def MenuWindowBreederClick(self, event):
        print "MenuWindowBreederClick"
        
    def MenuWindowNumericalExceptionsClick(self, event):
        print "MenuWindowNumericalExceptionsClick"
        
    def MenuWindowTimeSeriesClick(self, event):
        print "MenuWindowTimeSeriesClick"
        
    def PopupMenuAnimateClick(self, event):
        print "PopupMenuAnimateClick"
        
    def PopupMenuBreedClick(self, event):
        print "PopupMenuBreedClick"
        
    def PopupMenuCopyClick(self, event):
        print "PopupMenuCopyClick"
        
    def PopupMenuCutClick(self, event):
        print "PopupMenuCutClick"
        
    def PopupMenuEditNoteClick(self, event):
        print "PopupMenuEditNoteClick"
        
    def PopupMenuMakeTimeSeriesClick(self, event):
        print "PopupMenuMakeTimeSeriesClick"
        
    def PopupMenuPasteClick(self, event):
        print "PopupMenuPasteClick"
        
    def PopupMenuRandomizeClick(self, event):
        print "PopupMenuRandomizeClick"
        
    def PopupMenuRenameClick(self, event):
        print "PopupMenuRenameClick"
        
    def PopupMenuZeroRotationsClick(self, event):
        print "PopupMenuZeroRotationsClick"
        
    def Recent0Click(self, event):
        print "Recent0Click"
        
    def Reconcile3DObjects1Click(self, event):
        print "Reconcile3DObjects1Click"
        
    def UndoMenuEditUndoRedoListClick(self, event):
        print "UndoMenuEditUndoRedoListClick"
        
    def alignBottomsClick(self, event):
        print "alignBottomsClick"
        
    def alignLeftClick(self, event):
        print "alignLeftClick"
        
    def alignRightClick(self, event):
        print "alignRightClick"
        
    def alignTopsClick(self, event):
        print "alignTopsClick"
        
    def animateGrowthClick(self, event):
        print "animateGrowthClick"
        
    def centerDrawingClick(self, event):
        print "centerDrawingClick"
        
    def changeSelectedPose(self, event):
        print "changeSelectedPose"
        
    def dragCursorModeClick(self, event):
        print "dragCursorModeClick"
        
    def drawingAreaOnSideClick(self, event):
        print "drawingAreaOnSideClick"
        
    def drawingAreaOnTopClick(self, event):
        print "drawingAreaOnTopClick"
        
    def drawingScaleEditExit(self, event):
        print "drawingScaleEditExit"
        
    def horizontalSplitterMouseDown(self, event):
        print "horizontalSplitterMouseDown"
        
    def horizontalSplitterMouseMove(self, event):
        print "horizontalSplitterMouseMove"
        
    def horizontalSplitterMouseUp(self, event):
        print "horizontalSplitterMouseUp"
        
    def lifeCycleDaysEditExit(self, event):
        print "lifeCycleDaysEditExit"
        
    def lifeCycleDraggerMouseDown(self, event):
        print "lifeCycleDraggerMouseDown"
        
    def lifeCycleDraggerMouseMove(self, event):
        print "lifeCycleDraggerMouseMove"
        
    def lifeCycleDraggerMouseUp(self, event):
        print "lifeCycleDraggerMouseUp"
        
    def magnificationPercentClick(self, event):
        print "magnificationPercentClick"
        
    def magnificationPercentExit(self, event):
        print "magnificationPercentExit"
        
    def magnifyCursorModeClick(self, event):
        print "magnifyCursorModeClick"
        
    def makeEqualHeightClick(self, event):
        print "makeEqualHeightClick"
        
    def makeEqualWidthClick(self, event):
        print "makeEqualWidthClick"
        
    def noteEditClick(self, event):
        print "noteEditClick"
        
    def packPlantsClick(self, event):
        print "packPlantsClick"
        
    def paramPopupMenuCollapseAllInSectionClick(self, event):
        print "paramPopupMenuCollapseAllInSectionClick"
        
    def paramPopupMenuCollapseClick(self, event):
        print "paramPopupMenuCollapseClick"
        
    def paramPopupMenuCopyNameClick(self, event):
        print "paramPopupMenuCopyNameClick"
        
    def paramPopupMenuExpandAllInSectionClick(self, event):
        print "paramPopupMenuExpandAllInSectionClick"
        
    def paramPopupMenuExpandClick(self, event):
        print "paramPopupMenuExpandClick"
        
    def paramPopupMenuHelpClick(self, event):
        print "paramPopupMenuHelpClick"
        
    def plantBitmapsIndicatorImageClick(self, event):
        print "plantBitmapsIndicatorImageClick"
        
    def plantListDrawGridKeyDown(self, event):
        print "plantListDrawGridKeyDown"
        
    def plantListDrawGridMouseDown(self, event):
        print "plantListDrawGridMouseDown"
        
    def plantListDrawGridMouseUp(self, event):
        print "plantListDrawGridMouseUp"
        
    def posingBackfaceColorMouseUp(self, event):
        print "posingBackfaceColorMouseUp"
        
    def posingFrontfaceColorMouseUp(self, event):
        print "posingFrontfaceColorMouseUp"
        
    def posingGhostClick(self, event):
        print "posingGhostClick"
        
    def posingHighlightClick(self, event):
        print "posingHighlightClick"
        
    def posingLineColorMouseUp(self, event):
        print "posingLineColorMouseUp"
        
    def posingNotShownClick(self, event):
        print "posingNotShownClick"
        
    def posingPosePartClick(self, event):
        print "posingPosePartClick"
        
    def posingSelectionCursorModeClick(self, event):
        print "posingSelectionCursorModeClick"
        
    def posingUnposePartClick(self, event):
        print "posingUnposePartClick"
        
    def resetRotationsClick(self, event):
        print "resetRotationsClick"
        
    def rotateCursorModeClick(self, event):
        print "rotateCursorModeClick"
        
    def scrollCursorModeClick(self, event):
        print "scrollCursorModeClick"
        
    def sectionPopupMenuHelpClick(self, event):
        print "sectionPopupMenuHelpClick"
        
    def verticalSplitterMouseDown(self, event):
        print "verticalSplitterMouseDown"
        
    def verticalSplitterMouseMove(self, event):
        print "verticalSplitterMouseMove"
        
    def verticalSplitterMouseUp(self, event):
        print "verticalSplitterMouseUp"
        
    def viewFreeFloatingClick(self, event):
        print "viewFreeFloatingClick"
        
    def viewOneOnlyClick(self, event):
        print "viewOneOnlyClick"
        
    def xLocationEditExit(self, event):
        print "xLocationEditExit"
        
    def xRotationEditChange(self, event):
        print "xRotationEditChange"
        
    def xRotationEditExit(self, event):
        print "xRotationEditExit"
        
    def yLocationEditExit(self, event):
        print "yLocationEditExit"
        
    def yRotationEditChange(self, event):
        print "yRotationEditChange"
        
    def yRotationEditExit(self, event):
        print "yRotationEditExit"
        
    def zRotationEditChange(self, event):
        print "zRotationEditChange"
        
    def zRotationEditExit(self, event):
        print "zRotationEditExit"
        
if __name__ == "__main__":
    window = MainWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
