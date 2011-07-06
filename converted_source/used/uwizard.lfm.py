from common import *

#Useage:
#        import WizardWindow
#        window = WizardWindow.WizardWindow()
#        window.visible = 1

class WizardWindow(JFrame):
    def __init__(self, title='Plant Wizard'):
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
        self.setBounds(294, 114, 569, 299  + 80) # extra for title bar and menu
        #  --------------- UNHANDLED ATTRIBUTE: self.TextHeight = 14
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderIcons = [biSystemMenu]
        #  --------------- UNHANDLED ATTRIBUTE: self.Scaled = False
        #  --------------- UNHANDLED ATTRIBUTE: self.KeyPreview = True
        self.keyTyped = self.FormKeyPress
        #  --------------- UNHANDLED ATTRIBUTE: self.PixelsPerInch = 96
        #  --------------- UNHANDLED ATTRIBUTE: self.Position = poScreenCenter
        #  --------------- UNHANDLED ATTRIBUTE: self.BorderStyle = bsDialog
        #  --------------- UNHANDLED ATTRIBUTE: self.OnCreate = FormCreate
        #  --------------- UNHANDLED ATTRIBUTE: self.OnClose = FormClose
        
        #  ------- UNHANDLED TYPE TBevel: bottomBevel 
        #  --------------- UNHANDLED ATTRIBUTE: self.bottomBevel.Top = 269
        #  --------------- UNHANDLED ATTRIBUTE: self.bottomBevel.Height = 5
        #  --------------- UNHANDLED ATTRIBUTE: self.bottomBevel.Width = 609
        #  --------------- UNHANDLED ATTRIBUTE: self.bottomBevel.Shape = bsTopLine
        #  --------------- UNHANDLED ATTRIBUTE: self.bottomBevel.Left = -16
        self.helpButtonImage = toolkit.createImage("../resources/WizardForm_helpButton.png")
        self.helpButton = SpeedButton('Help', ImageIcon(self.helpButtonImage), actionPerformed=self.helpButtonClick, font=buttonFont, margin=buttonMargin)
        self.helpButton.setMnemonic(KeyEvent.VK_H)
        self.helpButton.setBounds(2, 276, 55, 21)
        self.changeTdoLibrary = SpeedButton('3D Objects...', actionPerformed=self.changeTdoLibraryClick, font=buttonFont, margin=buttonMargin)
        self.changeTdoLibrary.setMnemonic(KeyEvent.VK_3)
        self.changeTdoLibrary.setBounds(113, 276, 74, 21)
        self.wizardNotebook = JTabbedPane(stateChanged=self.wizardNotebookPageChanged)
        
        self.page1 = JPanel(layout=None)
        self.panelStartLabel = JLabel(' Welcome to the Plant Wizard!', font=buttonFont)
        self.panelStartLabel.setBounds(176, 16, 162, 14)
        self.page1.add(self.panelStartLabel)
        self.introLabelThird = JLabel('Click the Next button to start, or click Cancel to stop. Once you start, you can click the Back button to go back and change your choices, or you can click Cancel at any time.', font=buttonFont)
        self.introLabelThird.setBounds(178, 159, 328, 42)
        self.page1.add(self.introLabelThird)
        self.introLabelFirst = JLabel('This wizard will help you create a new plant by asking you some simple questions. ', font=buttonFont)
        self.introLabelFirst.setBounds(178, 41, 289, 27)
        self.page1.add(self.introLabelFirst)
        self.introLabelSecond = JLabel('These 10 panels contain about 25 questions based on the most important of the 400 or so parameters that define a plant.', font=buttonFont)
        self.introLabelSecond.setBounds(178, 82, 308, 31)
        self.page1.add(self.introLabelSecond)
        self.longHintsSuggestionLabel = JLabel('Note: If you are using the wizard for the first time, we recommend turning on the ''Long Button Hints''. Each wizard question has a hint.', font=buttonFont)
        self.longHintsSuggestionLabel.setBounds(176, 215, 322, 28)
        self.page1.add(self.longHintsSuggestionLabel)
        self.startPictureImage = toolkit.createImage("../resources/WizardForm_startPicture.png")
        self.startPicture = ImagePanel(ImageIcon(self.startPictureImage))
        self.startPicture.setBounds(15, 37, 150, 178)
        self.page1.add(self.startPicture)
        self.wizardNotebook.addTab('Start', None, self.page1)
        
        self.page2 = JPanel(layout=None)
        self.panelMeristemsLabel = JLabel('Meristems', font=buttonFont)
        self.panelMeristemsLabel.setBounds(4, 4, 61, 14)
        self.page2.add(self.panelMeristemsLabel)
        self.branchingLabel = JLabel('How much should the plant branch?', font=buttonFont)
        self.branchingLabel.setBounds(24, 154, 174, 14)
        self.page2.add(self.branchingLabel)
        self.leavesAlternateOppositeLabel = JLabel('How should leaves and branches be arranged?', font=buttonFont)
        self.leavesAlternateOppositeLabel.setBounds(24, 62, 231, 14)
        self.page2.add(self.leavesAlternateOppositeLabel)
        self.branchAngleLabel = JLabel(' What angle should branches make with the stem?', font=buttonFont)
        self.branchAngleLabel.setBounds(286, 154, 243, 14)
        self.page2.add(self.branchAngleLabel)
        self.secondaryBranchingLabel = JLabel('Should secondary branching (off branches) occur?', font=buttonFont)
        self.secondaryBranchingLabel.setBounds(288, 62, 250, 14)
        self.page2.add(self.secondaryBranchingLabel)
        self.leavesAlternateImage = toolkit.createImage("../resources/WizardForm_leavesAlternate.png")
        self.leavesAlternate = SpeedButton('alternate', ImageIcon(self.leavesAlternateImage), 1, font=buttonFont, margin=buttonMargin)
        self.leavesAlternate.setBounds(24, 77, 65, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leavesAlternate.Layout = blGlyphTop
        self.leavesAlternate.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.leavesAlternate.GroupIndex = 1
        self.page2.add(self.leavesAlternate)
        self.leavesOppositeImage = toolkit.createImage("../resources/WizardForm_leavesOpposite.png")
        self.leavesOpposite = SpeedButton('opposite', ImageIcon(self.leavesOppositeImage), font=buttonFont, margin=buttonMargin)
        self.leavesOpposite.setBounds(89, 77, 63, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leavesOpposite.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.leavesOpposite.GroupIndex = 1
        self.page2.add(self.leavesOpposite)
        self.branchNoneImage = toolkit.createImage("../resources/WizardForm_branchNone.png")
        self.branchNone = SpeedButton('none', ImageIcon(self.branchNoneImage), 1, actionPerformed=self.branchNoneClick, font=buttonFont, margin=buttonMargin)
        self.branchNone.setBounds(24, 170, 43, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchNone.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.branchNone.GroupIndex = 2
        self.page2.add(self.branchNone)
        self.branchLittleImage = toolkit.createImage("../resources/WizardForm_branchLittle.png")
        self.branchLittle = SpeedButton('a little', ImageIcon(self.branchLittleImage), actionPerformed=self.branchLittleClick, font=buttonFont, margin=buttonMargin)
        self.branchLittle.setBounds(66, 170, 49, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchLittle.Layout = blGlyphTop
        self.branchLittle.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchLittle.GroupIndex = 2
        self.page2.add(self.branchLittle)
        self.branchMediumImage = toolkit.createImage("../resources/WizardForm_branchMedium.png")
        self.branchMedium = SpeedButton('medium', ImageIcon(self.branchMediumImage), actionPerformed=self.branchMediumClick, font=buttonFont, margin=buttonMargin)
        self.branchMedium.setBounds(114, 170, 60, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchMedium.Layout = blGlyphTop
        self.branchMedium.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchMedium.GroupIndex = 2
        self.page2.add(self.branchMedium)
        self.branchLotImage = toolkit.createImage("../resources/WizardForm_branchLot.png")
        self.branchLot = SpeedButton('a lot', ImageIcon(self.branchLotImage), actionPerformed=self.branchLotClick, font=buttonFont, margin=buttonMargin)
        self.branchLot.setBounds(173, 170, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchLot.Layout = blGlyphTop
        self.branchLot.putClientProperty("tag", 3)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchLot.GroupIndex = 2
        self.page2.add(self.branchLot)
        self.secondaryBranchingYesImage = toolkit.createImage("../resources/WizardForm_secondaryBranchingYes.png")
        self.secondaryBranchingYes = SpeedButton('yes', ImageIcon(self.secondaryBranchingYesImage), font=buttonFont, margin=buttonMargin)
        self.secondaryBranchingYes.setBounds(288, 77, 49, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.secondaryBranchingYes.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.secondaryBranchingYes.GroupIndex = 3
        self.page2.add(self.secondaryBranchingYes)
        self.secondaryBranchingNoImage = toolkit.createImage("../resources/WizardForm_secondaryBranchingNo.png")
        self.secondaryBranchingNo = SpeedButton('no', ImageIcon(self.secondaryBranchingNoImage), 1, font=buttonFont, margin=buttonMargin)
        self.secondaryBranchingNo.setBounds(337, 77, 44, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.secondaryBranchingNo.Layout = blGlyphTop
        self.secondaryBranchingNo.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.secondaryBranchingNo.GroupIndex = 3
        self.page2.add(self.secondaryBranchingNo)
        self.branchAngleSmallImage = toolkit.createImage("../resources/WizardForm_branchAngleSmall.png")
        self.branchAngleSmall = SpeedButton('small', ImageIcon(self.branchAngleSmallImage), 1, font=buttonFont, margin=buttonMargin)
        self.branchAngleSmall.setBounds(288, 170, 47, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchAngleSmall.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.branchAngleSmall.GroupIndex = 4
        self.page2.add(self.branchAngleSmall)
        self.branchAngleMediumImage = toolkit.createImage("../resources/WizardForm_branchAngleMedium.png")
        self.branchAngleMedium = SpeedButton('medium', ImageIcon(self.branchAngleMediumImage), font=buttonFont, margin=buttonMargin)
        self.branchAngleMedium.setBounds(334, 170, 59, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchAngleMedium.Layout = blGlyphTop
        self.branchAngleMedium.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchAngleMedium.GroupIndex = 4
        self.page2.add(self.branchAngleMedium)
        self.branchAngleLargeImage = toolkit.createImage("../resources/WizardForm_branchAngleLarge.png")
        self.branchAngleLarge = SpeedButton('large', ImageIcon(self.branchAngleLargeImage), font=buttonFont, margin=buttonMargin)
        self.branchAngleLarge.setBounds(390, 170, 43, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchAngleLarge.Layout = blGlyphTop
        self.branchAngleLarge.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.branchAngleLarge.GroupIndex = 4
        self.page2.add(self.branchAngleLarge)
        self.arrowLeavesAlternateOppositeImage = toolkit.createImage("../resources/WizardForm_arrowLeavesAlternateOpposite.png")
        self.arrowLeavesAlternateOpposite = ImagePanel(ImageIcon(self.arrowLeavesAlternateOppositeImage))
        self.arrowLeavesAlternateOpposite.setBounds(12, 62, 8, 16)
        self.page2.add(self.arrowLeavesAlternateOpposite)
        self.arrowBranchingImage = toolkit.createImage("../resources/WizardForm_arrowBranching.png")
        self.arrowBranching = ImagePanel(ImageIcon(self.arrowBranchingImage))
        self.arrowBranching.setBounds(12, 154, 8, 16)
        self.page2.add(self.arrowBranching)
        self.arrowSecondaryBranchingImage = toolkit.createImage("../resources/WizardForm_arrowSecondaryBranching.png")
        self.arrowSecondaryBranching = ImagePanel(ImageIcon(self.arrowSecondaryBranchingImage))
        self.arrowSecondaryBranching.setBounds(274, 60, 8, 16)
        self.page2.add(self.arrowSecondaryBranching)
        self.arrowBranchAngleImage = toolkit.createImage("../resources/WizardForm_arrowBranchAngle.png")
        self.arrowBranchAngle = ImagePanel(ImageIcon(self.arrowBranchAngleImage))
        self.arrowBranchAngle.setBounds(274, 152, 8, 16)
        self.page2.add(self.arrowBranchAngle)
        self.Label1 = JLabel('Meristems are buds from which leaves and branches grow. Where they develop and what they produce has a big effect on plant shape. Meristems form at the growing ends of plant stems (apexes) and in the angles between leaf and stem (axils).', font=buttonFont)
        self.Label1.setBounds(12, 18, 509, 42)
        self.page2.add(self.Label1)
        self.Label11 = JLabel('For each question, click on one of the big buttons under the question to make your choice.', font=buttonFont)
        self.Label11.setBounds(75, 248, 433, 14)
        self.page2.add(self.Label11)
        self.wizardNotebook.addTab('Meristems', None, self.page2)
        
        self.page3 = JPanel(layout=None)
        self.panelInternodesLabel = JLabel('Internodes', font=buttonFont)
        self.panelInternodesLabel.setBounds(4, 4, 61, 14)
        self.page3.add(self.panelInternodesLabel)
        self.curvinessLabel = JLabel('How curvy should the plant stem be?', font=buttonFont)
        self.curvinessLabel.setBounds(24, 58, 180, 14)
        self.page3.add(self.curvinessLabel)
        self.internodeLengthLabel = JLabel('How long should internodes be?', font=buttonFont)
        self.internodeLengthLabel.setBounds(24, 150, 156, 14)
        self.page3.add(self.internodeLengthLabel)
        self.internodesVeryShortImage = toolkit.createImage("../resources/WizardForm_internodesVeryShort.png")
        self.internodesVeryShort = SpeedButton('very short', ImageIcon(self.internodesVeryShortImage), font=buttonFont, margin=buttonMargin)
        self.internodesVeryShort.setBounds(24, 167, 60, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesVeryShort.Layout = blGlyphTop
        self.internodesVeryShort.toolTipText = 'very short'
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesVeryShort.GroupIndex = 6
        self.page3.add(self.internodesVeryShort)
        self.internodesShortImage = toolkit.createImage("../resources/WizardForm_internodesShort.png")
        self.internodesShort = SpeedButton('short', ImageIcon(self.internodesShortImage), font=buttonFont, margin=buttonMargin)
        self.internodesShort.setBounds(83, 167, 41, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesShort.Layout = blGlyphTop
        self.internodesShort.toolTipText = 'short'
        self.internodesShort.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesShort.GroupIndex = 6
        self.page3.add(self.internodesShort)
        self.internodesMediumImage = toolkit.createImage("../resources/WizardForm_internodesMedium.png")
        self.internodesMedium = SpeedButton('medium', ImageIcon(self.internodesMediumImage), 1, font=buttonFont, margin=buttonMargin)
        self.internodesMedium.setBounds(123, 167, 51, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesMedium.Layout = blGlyphTop
        self.internodesMedium.toolTipText = 'medium'
        self.internodesMedium.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesMedium.GroupIndex = 6
        self.page3.add(self.internodesMedium)
        self.internodesLongImage = toolkit.createImage("../resources/WizardForm_internodesLong.png")
        self.internodesLong = SpeedButton('long', ImageIcon(self.internodesLongImage), font=buttonFont, margin=buttonMargin)
        self.internodesLong.setBounds(173, 167, 36, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesLong.Layout = blGlyphTop
        self.internodesLong.toolTipText = 'long'
        self.internodesLong.putClientProperty("tag", 3)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesLong.GroupIndex = 6
        self.page3.add(self.internodesLong)
        self.internodesVeryLongImage = toolkit.createImage("../resources/WizardForm_internodesVeryLong.png")
        self.internodesVeryLong = SpeedButton('very long', ImageIcon(self.internodesVeryLongImage), font=buttonFont, margin=buttonMargin)
        self.internodesVeryLong.setBounds(208, 167, 61, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesVeryLong.Layout = blGlyphTop
        self.internodesVeryLong.toolTipText = 'very long'
        self.internodesVeryLong.putClientProperty("tag", 4)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodesVeryLong.GroupIndex = 6
        self.page3.add(self.internodesVeryLong)
        self.curvinessNoneImage = toolkit.createImage("../resources/WizardForm_curvinessNone.png")
        self.curvinessNone = SpeedButton('none', ImageIcon(self.curvinessNoneImage), font=buttonFont, margin=buttonMargin)
        self.curvinessNone.setBounds(24, 78, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.curvinessNone.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.curvinessNone.GroupIndex = 5
        self.page3.add(self.curvinessNone)
        self.curvinessLittleImage = toolkit.createImage("../resources/WizardForm_curvinessLittle.png")
        self.curvinessLittle = SpeedButton('a little', ImageIcon(self.curvinessLittleImage), 1, font=buttonFont, margin=buttonMargin)
        self.curvinessLittle.setBounds(68, 78, 54, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.curvinessLittle.Layout = blGlyphTop
        self.curvinessLittle.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.curvinessLittle.GroupIndex = 5
        self.page3.add(self.curvinessLittle)
        self.curvinessSomeImage = toolkit.createImage("../resources/WizardForm_curvinessSome.png")
        self.curvinessSome = SpeedButton('some', ImageIcon(self.curvinessSomeImage), font=buttonFont, margin=buttonMargin)
        self.curvinessSome.setBounds(121, 78, 42, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.curvinessSome.Layout = blGlyphTop
        self.curvinessSome.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.curvinessSome.GroupIndex = 5
        self.page3.add(self.curvinessSome)
        self.curvinessVeryImage = toolkit.createImage("../resources/WizardForm_curvinessVery.png")
        self.curvinessVery = SpeedButton('a lot', ImageIcon(self.curvinessVeryImage), font=buttonFont, margin=buttonMargin)
        self.curvinessVery.setBounds(162, 78, 47, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.curvinessVery.Layout = blGlyphTop
        self.curvinessVery.putClientProperty("tag", 3)
        #  --------------- UNHANDLED ATTRIBUTE: self.curvinessVery.GroupIndex = 5
        self.page3.add(self.curvinessVery)
        self.arrowCurvinessImage = toolkit.createImage("../resources/WizardForm_arrowCurviness.png")
        self.arrowCurviness = ImagePanel(ImageIcon(self.arrowCurvinessImage))
        self.arrowCurviness.setBounds(12, 56, 8, 16)
        self.page3.add(self.arrowCurviness)
        self.arrowInternodeLengthImage = toolkit.createImage("../resources/WizardForm_arrowInternodeLength.png")
        self.arrowInternodeLength = ImagePanel(ImageIcon(self.arrowInternodeLengthImage))
        self.arrowInternodeLength.setBounds(12, 151, 8, 16)
        self.page3.add(self.arrowInternodeLength)
        self.arrowInternodeWidthImage = toolkit.createImage("../resources/WizardForm_arrowInternodeWidth.png")
        self.arrowInternodeWidth = ImagePanel(ImageIcon(self.arrowInternodeWidthImage))
        self.arrowInternodeWidth.setBounds(288, 56, 8, 16)
        self.page3.add(self.arrowInternodeWidth)
        self.internodeWidthLabel = JLabel('How thick should internodes be?', font=buttonFont)
        self.internodeWidthLabel.setBounds(302, 58, 158, 14)
        self.page3.add(self.internodeWidthLabel)
        self.internodeWidthVeryThinImage = toolkit.createImage("../resources/WizardForm_internodeWidthVeryThin.png")
        self.internodeWidthVeryThin = SpeedButton('very thin', ImageIcon(self.internodeWidthVeryThinImage), font=buttonFont, margin=buttonMargin)
        self.internodeWidthVeryThin.setBounds(302, 78, 57, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthVeryThin.Layout = blGlyphTop
        self.internodeWidthVeryThin.toolTipText = 'very short'
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthVeryThin.GroupIndex = 23
        self.page3.add(self.internodeWidthVeryThin)
        self.internodeWidthThinImage = toolkit.createImage("../resources/WizardForm_internodeWidthThin.png")
        self.internodeWidthThin = SpeedButton('thin', ImageIcon(self.internodeWidthThinImage), 1, font=buttonFont, margin=buttonMargin)
        self.internodeWidthThin.setBounds(358, 78, 38, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthThin.Layout = blGlyphTop
        self.internodeWidthThin.toolTipText = 'short'
        self.internodeWidthThin.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthThin.GroupIndex = 23
        self.page3.add(self.internodeWidthThin)
        self.internodeWidthMediumImage = toolkit.createImage("../resources/WizardForm_internodeWidthMedium.png")
        self.internodeWidthMedium = SpeedButton('medium', ImageIcon(self.internodeWidthMediumImage), font=buttonFont, margin=buttonMargin)
        self.internodeWidthMedium.setBounds(395, 78, 48, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthMedium.Layout = blGlyphTop
        self.internodeWidthMedium.toolTipText = 'medium'
        self.internodeWidthMedium.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthMedium.GroupIndex = 23
        self.page3.add(self.internodeWidthMedium)
        self.internodeWidthThickImage = toolkit.createImage("../resources/WizardForm_internodeWidthThick.png")
        self.internodeWidthThick = SpeedButton('thick', ImageIcon(self.internodeWidthThickImage), font=buttonFont, margin=buttonMargin)
        self.internodeWidthThick.setBounds(442, 78, 37, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthThick.Layout = blGlyphTop
        self.internodeWidthThick.toolTipText = 'long'
        self.internodeWidthThick.putClientProperty("tag", 3)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthThick.GroupIndex = 23
        self.page3.add(self.internodeWidthThick)
        self.internodeWidthVeryThickImage = toolkit.createImage("../resources/WizardForm_internodeWidthVeryThick.png")
        self.internodeWidthVeryThick = SpeedButton('very thick', ImageIcon(self.internodeWidthVeryThickImage), font=buttonFont, margin=buttonMargin)
        self.internodeWidthVeryThick.setBounds(478, 78, 58, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthVeryThick.Layout = blGlyphTop
        self.internodeWidthVeryThick.toolTipText = 'very long'
        self.internodeWidthVeryThick.putClientProperty("tag", 4)
        #  --------------- UNHANDLED ATTRIBUTE: self.internodeWidthVeryThick.GroupIndex = 23
        self.page3.add(self.internodeWidthVeryThick)
        self.Label2 = JLabel('Internodes are portions of plant stem between leaves. They determine how tall or short, straight or viney, and stiff or flexible a plant will be.', font=buttonFont)
        self.Label2.setBounds(12, 22, 395, 28)
        self.page3.add(self.Label2)
        self.wizardNotebook.addTab('Internodes', None, self.page3)
        
        self.page4 = JPanel(layout=None)
        self.panelLeavesLabel = JLabel('Leaves', font=buttonFont)
        self.panelLeavesLabel.setBounds(4, 4, 40, 14)
        self.page4.add(self.panelLeavesLabel)
        self.leafTdosLabel = JLabel(' What 3D object should be used to draw leaves?', font=buttonFont)
        self.leafTdosLabel.setBounds(22, 60, 235, 14)
        self.page4.add(self.leafTdosLabel)
        self.leafScaleLabel = JLabel('How big should a full-sized leaf be drawn?', font=buttonFont)
        self.leafScaleLabel.setBounds(24, 169, 208, 14)
        self.page4.add(self.leafScaleLabel)
        self.leafAngleLabel = JLabel(' What angle should each leaf make with the stem?', font=buttonFont)
        self.leafAngleLabel.setBounds(300, 169, 242, 14)
        self.page4.add(self.leafAngleLabel)
        self.petioleLengthLabel = JLabel('How long should the petiole (leaf stalk) be?', font=buttonFont)
        self.petioleLengthLabel.setBounds(302, 60, 208, 14)
        self.page4.add(self.petioleLengthLabel)
        self.arrowLeafScaleImage = toolkit.createImage("../resources/WizardForm_arrowLeafScale.png")
        self.arrowLeafScale = ImagePanel(ImageIcon(self.arrowLeafScaleImage))
        self.arrowLeafScale.setBounds(12, 167, 8, 16)
        self.page4.add(self.arrowLeafScale)
        self.leafScaleTinyImage = toolkit.createImage("../resources/WizardForm_leafScaleTiny.png")
        self.leafScaleTiny = SpeedButton('tiny', ImageIcon(self.leafScaleTinyImage), font=buttonFont, margin=buttonMargin)
        self.leafScaleTiny.setBounds(24, 185, 37, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleTiny.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleTiny.GroupIndex = 7
        self.page4.add(self.leafScaleTiny)
        self.leafScaleSmallImage = toolkit.createImage("../resources/WizardForm_leafScaleSmall.png")
        self.leafScaleSmall = SpeedButton('small', ImageIcon(self.leafScaleSmallImage), font=buttonFont, margin=buttonMargin)
        self.leafScaleSmall.setBounds(60, 185, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleSmall.Layout = blGlyphTop
        self.leafScaleSmall.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleSmall.GroupIndex = 7
        self.page4.add(self.leafScaleSmall)
        self.leafScaleMediumImage = toolkit.createImage("../resources/WizardForm_leafScaleMedium.png")
        self.leafScaleMedium = SpeedButton('medium', ImageIcon(self.leafScaleMediumImage), 1, font=buttonFont, margin=buttonMargin)
        self.leafScaleMedium.setBounds(104, 185, 59, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleMedium.Layout = blGlyphTop
        self.leafScaleMedium.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleMedium.GroupIndex = 7
        self.page4.add(self.leafScaleMedium)
        self.leafScaleLargeImage = toolkit.createImage("../resources/WizardForm_leafScaleLarge.png")
        self.leafScaleLarge = SpeedButton('large', ImageIcon(self.leafScaleLargeImage), font=buttonFont, margin=buttonMargin)
        self.leafScaleLarge.setBounds(162, 185, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleLarge.Layout = blGlyphTop
        self.leafScaleLarge.putClientProperty("tag", 3)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleLarge.GroupIndex = 7
        self.page4.add(self.leafScaleLarge)
        self.leafScaleHugeImage = toolkit.createImage("../resources/WizardForm_leafScaleHuge.png")
        self.leafScaleHuge = SpeedButton('huge', ImageIcon(self.leafScaleHugeImage), font=buttonFont, margin=buttonMargin)
        self.leafScaleHuge.setBounds(206, 185, 47, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleHuge.Layout = blGlyphTop
        self.leafScaleHuge.putClientProperty("tag", 4)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafScaleHuge.GroupIndex = 7
        self.page4.add(self.leafScaleHuge)
        self.arrowLeafAngleImage = toolkit.createImage("../resources/WizardForm_arrowLeafAngle.png")
        self.arrowLeafAngle = ImagePanel(ImageIcon(self.arrowLeafAngleImage))
        self.arrowLeafAngle.setBounds(288, 167, 8, 16)
        self.page4.add(self.arrowLeafAngle)
        self.leafAngleSmallImage = toolkit.createImage("../resources/WizardForm_leafAngleSmall.png")
        self.leafAngleSmall = SpeedButton('small', ImageIcon(self.leafAngleSmallImage), font=buttonFont, margin=buttonMargin)
        self.leafAngleSmall.setBounds(302, 185, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafAngleSmall.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.leafAngleSmall.GroupIndex = 9
        self.page4.add(self.leafAngleSmall)
        self.leafAngleMediumImage = toolkit.createImage("../resources/WizardForm_leafAngleMedium.png")
        self.leafAngleMedium = SpeedButton('medium', ImageIcon(self.leafAngleMediumImage), 1, font=buttonFont, margin=buttonMargin)
        self.leafAngleMedium.setBounds(346, 185, 59, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafAngleMedium.Layout = blGlyphTop
        self.leafAngleMedium.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafAngleMedium.GroupIndex = 9
        self.page4.add(self.leafAngleMedium)
        self.leafAngleLargeImage = toolkit.createImage("../resources/WizardForm_leafAngleLarge.png")
        self.leafAngleLarge = SpeedButton('large', ImageIcon(self.leafAngleLargeImage), font=buttonFont, margin=buttonMargin)
        self.leafAngleLarge.setBounds(404, 185, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafAngleLarge.Layout = blGlyphTop
        self.leafAngleLarge.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafAngleLarge.GroupIndex = 9
        self.page4.add(self.leafAngleLarge)
        self.arrowPetioleLengthImage = toolkit.createImage("../resources/WizardForm_arrowPetioleLength.png")
        self.arrowPetioleLength = ImagePanel(ImageIcon(self.arrowPetioleLengthImage))
        self.arrowPetioleLength.setBounds(288, 58, 8, 16)
        self.page4.add(self.arrowPetioleLength)
        self.petioleVeryShortImage = toolkit.createImage("../resources/WizardForm_petioleVeryShort.png")
        self.petioleVeryShort = SpeedButton('very short', ImageIcon(self.petioleVeryShortImage), font=buttonFont, margin=buttonMargin)
        self.petioleVeryShort.setBounds(302, 76, 57, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleVeryShort.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleVeryShort.GroupIndex = 8
        self.page4.add(self.petioleVeryShort)
        self.petioleShortImage = toolkit.createImage("../resources/WizardForm_petioleShort.png")
        self.petioleShort = SpeedButton('short', ImageIcon(self.petioleShortImage), font=buttonFont, margin=buttonMargin)
        self.petioleShort.setBounds(358, 76, 43, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleShort.Layout = blGlyphTop
        self.petioleShort.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleShort.GroupIndex = 8
        self.page4.add(self.petioleShort)
        self.petioleMediumImage = toolkit.createImage("../resources/WizardForm_petioleMedium.png")
        self.petioleMedium = SpeedButton('medium', ImageIcon(self.petioleMediumImage), 1, font=buttonFont, margin=buttonMargin)
        self.petioleMedium.setBounds(400, 76, 50, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleMedium.Layout = blGlyphTop
        self.petioleMedium.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleMedium.GroupIndex = 8
        self.page4.add(self.petioleMedium)
        self.petioleLongImage = toolkit.createImage("../resources/WizardForm_petioleLong.png")
        self.petioleLong = SpeedButton('long', ImageIcon(self.petioleLongImage), font=buttonFont, margin=buttonMargin)
        self.petioleLong.setBounds(449, 76, 42, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleLong.Layout = blGlyphTop
        self.petioleLong.putClientProperty("tag", 3)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleLong.GroupIndex = 8
        self.page4.add(self.petioleLong)
        self.petioleVeryLongImage = toolkit.createImage("../resources/WizardForm_petioleVeryLong.png")
        self.petioleVeryLong = SpeedButton('very long', ImageIcon(self.petioleVeryLongImage), font=buttonFont, margin=buttonMargin)
        self.petioleVeryLong.setBounds(490, 76, 55, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleVeryLong.Layout = blGlyphTop
        self.petioleVeryLong.putClientProperty("tag", 4)
        #  --------------- UNHANDLED ATTRIBUTE: self.petioleVeryLong.GroupIndex = 8
        self.page4.add(self.petioleVeryLong)
        self.arrowLeafTdosImage = toolkit.createImage("../resources/WizardForm_arrowLeafTdos.png")
        self.arrowLeafTdos = ImagePanel(ImageIcon(self.arrowLeafTdosImage))
        self.arrowLeafTdos.setBounds(12, 58, 8, 16)
        self.page4.add(self.arrowLeafTdos)
        self.Label4 = JLabel('PlantStudio draws leaves using a "3D object" that represents a 3D leaf shape. The 3D object is drawn bigger as the leaf grows. Leaves are connected to the plant by a stalk called a petiole.', font=buttonFont)
        self.Label4.setBounds(12, 22, 527, 28)
        self.page4.add(self.Label4)
        self.leafTdoSelectedLabel = JLabel('leafTdoSelectedLabel', font=buttonFont)
        self.leafTdoSelectedLabel.setBounds(24, 148, 104, 14)
        self.page4.add(self.leafTdoSelectedLabel)
        self.leafTdosDraw = JTable(DefaultTableModel())
        self.leafTdosDraw.setBounds(24, 76, 250, 69)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.OnDrawCell = leafTdosDrawDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.RowCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.DefaultColWidth = 40
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.ColCount = 20
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.DefaultRowHeight = 50
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.ScrollBars = ssHorizontal
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.OnSelectCell = leafTdosDrawSelectCell
        #  --------------- UNHANDLED ATTRIBUTE: self.leafTdosDraw.Options = [goVertLine, goHorzLine]
        self.page4.add(self.leafTdosDraw)
        self.wizardNotebook.addTab('Leaves', None, self.page4)
        
        self.page5 = JPanel(layout=None)
        self.panelCompoundLeavesLabel = JLabel('Compound leaves', font=buttonFont)
        self.panelCompoundLeavesLabel.setBounds(4, 4, 100, 14)
        self.page5.add(self.panelCompoundLeavesLabel)
        self.arrowLeafletsImage = toolkit.createImage("../resources/WizardForm_arrowLeaflets.png")
        self.arrowLeaflets = ImagePanel(ImageIcon(self.arrowLeafletsImage))
        self.arrowLeaflets.setBounds(12, 72, 8, 16)
        self.page5.add(self.arrowLeaflets)
        self.leafletsLabel = JLabel('How many leaflets should make up each leaf?', font=buttonFont)
        self.leafletsLabel.setBounds(24, 74, 222, 14)
        self.page5.add(self.leafletsLabel)
        self.leafletsShapeLabel = JLabel(' What shape should the compound leaves take?', font=buttonFont)
        self.leafletsShapeLabel.setBounds(22, 159, 231, 14)
        self.page5.add(self.leafletsShapeLabel)
        self.arrowLeafletsShapeImage = toolkit.createImage("../resources/WizardForm_arrowLeafletsShape.png")
        self.arrowLeafletsShape = ImagePanel(ImageIcon(self.arrowLeafletsShapeImage))
        self.arrowLeafletsShape.setBounds(12, 157, 8, 16)
        self.page5.add(self.arrowLeafletsShape)
        self.leafletsOneImage = toolkit.createImage("../resources/WizardForm_leafletsOne.png")
        self.leafletsOne = SpeedButton('one (simple)', ImageIcon(self.leafletsOneImage), 1, actionPerformed=self.leafletsOneClick, font=buttonFont, margin=buttonMargin)
        self.leafletsOne.setBounds(24, 90, 69, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsOne.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsOne.GroupIndex = 10
        self.page5.add(self.leafletsOne)
        self.leafletsThreeImage = toolkit.createImage("../resources/WizardForm_leafletsThree.png")
        self.leafletsThree = SpeedButton('three', ImageIcon(self.leafletsThreeImage), actionPerformed=self.leafletsThreeClick, font=buttonFont, margin=buttonMargin)
        self.leafletsThree.setBounds(92, 90, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsThree.Layout = blGlyphTop
        self.leafletsThree.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsThree.GroupIndex = 10
        self.page5.add(self.leafletsThree)
        self.leafletsFourImage = toolkit.createImage("../resources/WizardForm_leafletsFour.png")
        self.leafletsFour = SpeedButton('four', ImageIcon(self.leafletsFourImage), actionPerformed=self.leafletsFourClick, font=buttonFont, margin=buttonMargin)
        self.leafletsFour.setBounds(136, 90, 46, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsFour.Layout = blGlyphTop
        self.leafletsFour.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsFour.GroupIndex = 10
        self.page5.add(self.leafletsFour)
        self.leafletsFiveImage = toolkit.createImage("../resources/WizardForm_leafletsFive.png")
        self.leafletsFive = SpeedButton('five', ImageIcon(self.leafletsFiveImage), actionPerformed=self.leafletsFiveClick, font=buttonFont, margin=buttonMargin)
        self.leafletsFive.setBounds(181, 90, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsFive.Layout = blGlyphTop
        self.leafletsFive.putClientProperty("tag", 3)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsFive.GroupIndex = 10
        self.page5.add(self.leafletsFive)
        self.leafletsSevenImage = toolkit.createImage("../resources/WizardForm_leafletsSeven.png")
        self.leafletsSeven = SpeedButton('seven', ImageIcon(self.leafletsSevenImage), actionPerformed=self.leafletsSevenClick, font=buttonFont, margin=buttonMargin)
        self.leafletsSeven.setBounds(225, 90, 47, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsSeven.Layout = blGlyphTop
        self.leafletsSeven.putClientProperty("tag", 4)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsSeven.GroupIndex = 10
        self.page5.add(self.leafletsSeven)
        self.leafletsPinnateImage = toolkit.createImage("../resources/WizardForm_leafletsPinnate.png")
        self.leafletsPinnate = SpeedButton('pinnate', ImageIcon(self.leafletsPinnateImage), 1, font=buttonFont, margin=buttonMargin)
        self.leafletsPinnate.setBounds(24, 175, 71, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsPinnate.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsPinnate.GroupIndex = 11
        self.page5.add(self.leafletsPinnate)
        self.leafletsPalmateImage = toolkit.createImage("../resources/WizardForm_leafletsPalmate.png")
        self.leafletsPalmate = SpeedButton('palmate', ImageIcon(self.leafletsPalmateImage), font=buttonFont, margin=buttonMargin)
        self.leafletsPalmate.setBounds(94, 175, 60, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsPalmate.Layout = blGlyphTop
        self.leafletsPalmate.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletsPalmate.GroupIndex = 11
        self.page5.add(self.leafletsPalmate)
        self.arrowLeafletsSpacingImage = toolkit.createImage("../resources/WizardForm_arrowLeafletsSpacing.png")
        self.arrowLeafletsSpacing = ImagePanel(ImageIcon(self.arrowLeafletsSpacingImage))
        self.arrowLeafletsSpacing.setBounds(288, 72, 8, 16)
        self.page5.add(self.arrowLeafletsSpacing)
        self.leafletSpacingLabel = JLabel('How spread out should the leaflets be?', font=buttonFont)
        self.leafletSpacingLabel.setBounds(300, 74, 190, 14)
        self.page5.add(self.leafletSpacingLabel)
        self.leafletSpacingCloseImage = toolkit.createImage("../resources/WizardForm_leafletSpacingClose.png")
        self.leafletSpacingClose = SpeedButton('close', ImageIcon(self.leafletSpacingCloseImage), font=buttonFont, margin=buttonMargin)
        self.leafletSpacingClose.setBounds(300, 90, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletSpacingClose.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletSpacingClose.GroupIndex = 12
        self.page5.add(self.leafletSpacingClose)
        self.leafletSpacingMediumImage = toolkit.createImage("../resources/WizardForm_leafletSpacingMedium.png")
        self.leafletSpacingMedium = SpeedButton('medium', ImageIcon(self.leafletSpacingMediumImage), 1, font=buttonFont, margin=buttonMargin)
        self.leafletSpacingMedium.setBounds(344, 90, 59, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletSpacingMedium.Layout = blGlyphTop
        self.leafletSpacingMedium.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletSpacingMedium.GroupIndex = 12
        self.page5.add(self.leafletSpacingMedium)
        self.leafletSpacingFarImage = toolkit.createImage("../resources/WizardForm_leafletSpacingFar.png")
        self.leafletSpacingFar = SpeedButton('far', ImageIcon(self.leafletSpacingFarImage), font=buttonFont, margin=buttonMargin)
        self.leafletSpacingFar.setBounds(402, 90, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletSpacingFar.Layout = blGlyphTop
        self.leafletSpacingFar.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.leafletSpacingFar.GroupIndex = 12
        self.page5.add(self.leafletSpacingFar)
        self.Label5 = JLabel('A compound leaf is a leaf made up of two or more small parts called leaflets. The leaflets look like small whole leaves, but they always fit together in the same pattern for all the leaves on the plant (usually). A leaf without leaflets is a simple leaf.', font=buttonFont)
        self.Label5.setBounds(12, 22, 531, 42)
        self.page5.add(self.Label5)
        self.wizardNotebook.addTab('Compound leaves', None, self.page5)
        
        self.page6 = JPanel(layout=None)
        self.panelInflorPlacementLabel = JLabel('Inflorescence placement', font=buttonFont)
        self.panelInflorPlacementLabel.setBounds(4, 4, 137, 14)
        self.page6.add(self.panelInflorPlacementLabel)
        self.apicalInflorsNumberLabel = JLabel('How many apical inflorescences should there be?', font=buttonFont)
        self.apicalInflorsNumberLabel.setBounds(24, 87, 242, 14)
        self.page6.add(self.apicalInflorsNumberLabel)
        self.axillaryInflorsNumberLabel = JLabel('How many axillary inflorescences should there be?', font=buttonFont)
        self.axillaryInflorsNumberLabel.setBounds(308, 87, 248, 14)
        self.page6.add(self.axillaryInflorsNumberLabel)
        self.apicalStalkLabel = JLabel('How long should their primary stems be?', font=buttonFont)
        self.apicalStalkLabel.setBounds(24, 171, 197, 14)
        self.page6.add(self.apicalStalkLabel)
        self.axillaryStalkLabel = JLabel('How long should their primary stems be?', font=buttonFont)
        self.axillaryStalkLabel.setBounds(308, 171, 197, 14)
        self.page6.add(self.axillaryStalkLabel)
        self.apicalInflorExtraImageImage = toolkit.createImage("../resources/WizardForm_apicalInflorExtraImage.png")
        self.apicalInflorExtraImage = ImagePanel(ImageIcon(self.apicalInflorExtraImageImage))
        self.apicalInflorExtraImage.setBounds(24, 55, 16, 16)
        self.page6.add(self.apicalInflorExtraImage)
        self.axillaryInflorExtraImageImage = toolkit.createImage("../resources/WizardForm_axillaryInflorExtraImage.png")
        self.axillaryInflorExtraImage = ImagePanel(ImageIcon(self.axillaryInflorExtraImageImage))
        self.axillaryInflorExtraImage.setBounds(308, 53, 16, 16)
        self.page6.add(self.axillaryInflorExtraImage)
        self.apicalInflorsNoneImage = toolkit.createImage("../resources/WizardForm_apicalInflorsNone.png")
        self.apicalInflorsNone = SpeedButton('none', ImageIcon(self.apicalInflorsNoneImage), 1, actionPerformed=self.apicalInflorsNoneClick, font=buttonFont, margin=buttonMargin)
        self.apicalInflorsNone.setBounds(24, 104, 41, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsNone.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsNone.GroupIndex = 17
        self.page6.add(self.apicalInflorsNone)
        self.apicalInflorsOneImage = toolkit.createImage("../resources/WizardForm_apicalInflorsOne.png")
        self.apicalInflorsOne = SpeedButton('one', ImageIcon(self.apicalInflorsOneImage), actionPerformed=self.apicalInflorsOneClick, font=buttonFont, margin=buttonMargin)
        self.apicalInflorsOne.setBounds(64, 104, 39, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsOne.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsOne.GroupIndex = 17
        self.page6.add(self.apicalInflorsOne)
        self.apicalInflorsTwoImage = toolkit.createImage("../resources/WizardForm_apicalInflorsTwo.png")
        self.apicalInflorsTwo = SpeedButton('two', ImageIcon(self.apicalInflorsTwoImage), actionPerformed=self.apicalInflorsTwoClick, font=buttonFont, margin=buttonMargin)
        self.apicalInflorsTwo.setBounds(102, 104, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsTwo.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsTwo.GroupIndex = 17
        self.page6.add(self.apicalInflorsTwo)
        self.apicalInflorsThreeImage = toolkit.createImage("../resources/WizardForm_apicalInflorsThree.png")
        self.apicalInflorsThree = SpeedButton('three', ImageIcon(self.apicalInflorsThreeImage), actionPerformed=self.apicalInflorsThreeClick, font=buttonFont, margin=buttonMargin)
        self.apicalInflorsThree.setBounds(146, 104, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsThree.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsThree.GroupIndex = 17
        self.page6.add(self.apicalInflorsThree)
        self.apicalInflorsFiveImage = toolkit.createImage("../resources/WizardForm_apicalInflorsFive.png")
        self.apicalInflorsFive = SpeedButton('five', ImageIcon(self.apicalInflorsFiveImage), actionPerformed=self.apicalInflorsFiveClick, font=buttonFont, margin=buttonMargin)
        self.apicalInflorsFive.setBounds(190, 104, 40, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsFive.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalInflorsFive.GroupIndex = 17
        self.page6.add(self.apicalInflorsFive)
        self.arrowApicalInflorsNumberImage = toolkit.createImage("../resources/WizardForm_arrowApicalInflorsNumber.png")
        self.arrowApicalInflorsNumber = ImagePanel(ImageIcon(self.arrowApicalInflorsNumberImage))
        self.arrowApicalInflorsNumber.setBounds(12, 85, 8, 16)
        self.page6.add(self.arrowApicalInflorsNumber)
        self.axillaryInflorsNoneImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsNone.png")
        self.axillaryInflorsNone = SpeedButton('none', ImageIcon(self.axillaryInflorsNoneImage), 1, actionPerformed=self.axillaryInflorsNoneClick, font=buttonFont, margin=buttonMargin)
        self.axillaryInflorsNone.setBounds(308, 104, 41, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsNone.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsNone.GroupIndex = 18
        self.page6.add(self.axillaryInflorsNone)
        self.axillaryInflorsThreeImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsThree.png")
        self.axillaryInflorsThree = SpeedButton('three', ImageIcon(self.axillaryInflorsThreeImage), actionPerformed=self.axillaryInflorsThreeClick, font=buttonFont, margin=buttonMargin)
        self.axillaryInflorsThree.setBounds(348, 104, 44, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsThree.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsThree.GroupIndex = 18
        self.page6.add(self.axillaryInflorsThree)
        self.axillaryInflorsFiveImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsFive.png")
        self.axillaryInflorsFive = SpeedButton('five', ImageIcon(self.axillaryInflorsFiveImage), actionPerformed=self.axillaryInflorsFiveClick, font=buttonFont, margin=buttonMargin)
        self.axillaryInflorsFive.setBounds(391, 104, 43, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsFive.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsFive.GroupIndex = 18
        self.page6.add(self.axillaryInflorsFive)
        self.axillaryInflorsTenImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsTen.png")
        self.axillaryInflorsTen = SpeedButton('ten', ImageIcon(self.axillaryInflorsTenImage), actionPerformed=self.axillaryInflorsTenClick, font=buttonFont, margin=buttonMargin)
        self.axillaryInflorsTen.setBounds(433, 104, 44, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsTen.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsTen.GroupIndex = 18
        self.page6.add(self.axillaryInflorsTen)
        self.axillaryInflorsTwentyImage = toolkit.createImage("../resources/WizardForm_axillaryInflorsTwenty.png")
        self.axillaryInflorsTwenty = SpeedButton('twenty', ImageIcon(self.axillaryInflorsTwentyImage), actionPerformed=self.axillaryInflorsTwentyClick, font=buttonFont, margin=buttonMargin)
        self.axillaryInflorsTwenty.setBounds(476, 104, 51, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsTwenty.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryInflorsTwenty.GroupIndex = 18
        self.page6.add(self.axillaryInflorsTwenty)
        self.arrowAxillaryInflorsNumberImage = toolkit.createImage("../resources/WizardForm_arrowAxillaryInflorsNumber.png")
        self.arrowAxillaryInflorsNumber = ImagePanel(ImageIcon(self.arrowAxillaryInflorsNumberImage))
        self.arrowAxillaryInflorsNumber.setBounds(294, 85, 8, 16)
        self.page6.add(self.arrowAxillaryInflorsNumber)
        self.apicalStalkVeryShortImage = toolkit.createImage("../resources/WizardForm_apicalStalkVeryShort.png")
        self.apicalStalkVeryShort = SpeedButton('very short', ImageIcon(self.apicalStalkVeryShortImage), font=buttonFont, margin=buttonMargin)
        self.apicalStalkVeryShort.setBounds(24, 188, 64, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkVeryShort.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkVeryShort.GroupIndex = 19
        self.page6.add(self.apicalStalkVeryShort)
        self.apicalStalkShortImage = toolkit.createImage("../resources/WizardForm_apicalStalkShort.png")
        self.apicalStalkShort = SpeedButton('short', ImageIcon(self.apicalStalkShortImage), font=buttonFont, margin=buttonMargin)
        self.apicalStalkShort.setBounds(87, 188, 38, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkShort.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkShort.GroupIndex = 19
        self.page6.add(self.apicalStalkShort)
        self.apicalStalkMediumImage = toolkit.createImage("../resources/WizardForm_apicalStalkMedium.png")
        self.apicalStalkMedium = SpeedButton('medium', ImageIcon(self.apicalStalkMediumImage), 1, font=buttonFont, margin=buttonMargin)
        self.apicalStalkMedium.setBounds(125, 188, 52, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkMedium.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkMedium.GroupIndex = 19
        self.page6.add(self.apicalStalkMedium)
        self.apicalStalkLongImage = toolkit.createImage("../resources/WizardForm_apicalStalkLong.png")
        self.apicalStalkLong = SpeedButton('long', ImageIcon(self.apicalStalkLongImage), font=buttonFont, margin=buttonMargin)
        self.apicalStalkLong.setBounds(177, 188, 39, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkLong.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkLong.GroupIndex = 19
        self.page6.add(self.apicalStalkLong)
        self.apicalStalkVeryLongImage = toolkit.createImage("../resources/WizardForm_apicalStalkVeryLong.png")
        self.apicalStalkVeryLong = SpeedButton('very long', ImageIcon(self.apicalStalkVeryLongImage), font=buttonFont, margin=buttonMargin)
        self.apicalStalkVeryLong.setBounds(215, 188, 57, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkVeryLong.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.apicalStalkVeryLong.GroupIndex = 19
        self.page6.add(self.apicalStalkVeryLong)
        self.arrowApicalStalkImage = toolkit.createImage("../resources/WizardForm_arrowApicalStalk.png")
        self.arrowApicalStalk = ImagePanel(ImageIcon(self.arrowApicalStalkImage))
        self.arrowApicalStalk.setBounds(12, 169, 8, 16)
        self.page6.add(self.arrowApicalStalk)
        self.arrowAxillaryStalkImage = toolkit.createImage("../resources/WizardForm_arrowAxillaryStalk.png")
        self.arrowAxillaryStalk = ImagePanel(ImageIcon(self.arrowAxillaryStalkImage))
        self.arrowAxillaryStalk.setBounds(294, 169, 8, 16)
        self.page6.add(self.arrowAxillaryStalk)
        self.axillaryStalkVeryShortImage = toolkit.createImage("../resources/WizardForm_axillaryStalkVeryShort.png")
        self.axillaryStalkVeryShort = SpeedButton('very short', ImageIcon(self.axillaryStalkVeryShortImage), font=buttonFont, margin=buttonMargin)
        self.axillaryStalkVeryShort.setBounds(308, 188, 60, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkVeryShort.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkVeryShort.GroupIndex = 20
        self.page6.add(self.axillaryStalkVeryShort)
        self.axillaryStalkShortImage = toolkit.createImage("../resources/WizardForm_axillaryStalkShort.png")
        self.axillaryStalkShort = SpeedButton('short', ImageIcon(self.axillaryStalkShortImage), font=buttonFont, margin=buttonMargin)
        self.axillaryStalkShort.setBounds(367, 188, 40, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkShort.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkShort.GroupIndex = 20
        self.page6.add(self.axillaryStalkShort)
        self.axillaryStalkMediumImage = toolkit.createImage("../resources/WizardForm_axillaryStalkMedium.png")
        self.axillaryStalkMedium = SpeedButton('medium', ImageIcon(self.axillaryStalkMediumImage), 1, font=buttonFont, margin=buttonMargin)
        self.axillaryStalkMedium.setBounds(406, 188, 50, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkMedium.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkMedium.GroupIndex = 20
        self.page6.add(self.axillaryStalkMedium)
        self.axillaryStalkLongImage = toolkit.createImage("../resources/WizardForm_axillaryStalkLong.png")
        self.axillaryStalkLong = SpeedButton('long', ImageIcon(self.axillaryStalkLongImage), font=buttonFont, margin=buttonMargin)
        self.axillaryStalkLong.setBounds(455, 188, 40, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkLong.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkLong.GroupIndex = 20
        self.page6.add(self.axillaryStalkLong)
        self.axillaryStalkVeryLongImage = toolkit.createImage("../resources/WizardForm_axillaryStalkVeryLong.png")
        self.axillaryStalkVeryLong = SpeedButton('very long', ImageIcon(self.axillaryStalkVeryLongImage), font=buttonFont, margin=buttonMargin)
        self.axillaryStalkVeryLong.setBounds(494, 188, 57, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkVeryLong.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.axillaryStalkVeryLong.GroupIndex = 20
        self.page6.add(self.axillaryStalkVeryLong)
        self.Label3 = JLabel('Apical inflorescences are at the ends (apexes) of plant stems.', font=buttonFont)
        self.Label3.setBounds(42, 53, 157, 28)
        self.page6.add(self.Label3)
        self.Label6 = JLabel('An inflorescence holds flowers and fruits on a plant. Since most plants have hermaphroditic flowers (with both male and female parts), the wizard creates only primary (female or hermaphroditic) flowers.', font=buttonFont)
        self.Label6.setBounds(12, 22, 540, 28)
        self.page6.add(self.Label6)
        self.Label7 = JLabel('Axillary inflorescences are in the angles between leaf and stem (axils).', font=buttonFont)
        self.Label7.setBounds(330, 53, 182, 28)
        self.page6.add(self.Label7)
        self.wizardNotebook.addTab('Inflorescence placement', None, self.page6)
        
        self.page7 = JPanel(layout=None)
        self.panelInflorDrawingLabel = JLabel('Inflorescence drawing', font=buttonFont)
        self.panelInflorDrawingLabel.setBounds(4, 4, 124, 14)
        self.page7.add(self.panelInflorDrawingLabel)
        self.inflorFlowersLabel = JLabel('How many flowers should each inflorescence have?', font=buttonFont)
        self.inflorFlowersLabel.setBounds(26, 59, 257, 14)
        self.page7.add(self.inflorFlowersLabel)
        self.inflorShapeLabel = JLabel(' What shape should each inflorescence have?', font=buttonFont)
        self.inflorShapeLabel.setBounds(24, 146, 225, 14)
        self.page7.add(self.inflorShapeLabel)
        self.arrowInflorFlowersImage = toolkit.createImage("../resources/WizardForm_arrowInflorFlowers.png")
        self.arrowInflorFlowers = ImagePanel(ImageIcon(self.arrowInflorFlowersImage))
        self.arrowInflorFlowers.setBounds(12, 57, 8, 16)
        self.page7.add(self.arrowInflorFlowers)
        self.arrowInflorShapeImage = toolkit.createImage("../resources/WizardForm_arrowInflorShape.png")
        self.arrowInflorShape = ImagePanel(ImageIcon(self.arrowInflorShapeImage))
        self.arrowInflorShape.setBounds(12, 144, 8, 16)
        self.page7.add(self.arrowInflorShape)
        self.inflorFlowersOneImage = toolkit.createImage("../resources/WizardForm_inflorFlowersOne.png")
        self.inflorFlowersOne = SpeedButton('one', ImageIcon(self.inflorFlowersOneImage), actionPerformed=self.inflorFlowersOneClick, font=buttonFont, margin=buttonMargin)
        self.inflorFlowersOne.setBounds(24, 76, 36, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersOne.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersOne.GroupIndex = 15
        self.page7.add(self.inflorFlowersOne)
        self.inflorFlowersTwoImage = toolkit.createImage("../resources/WizardForm_inflorFlowersTwo.png")
        self.inflorFlowersTwo = SpeedButton('two', ImageIcon(self.inflorFlowersTwoImage), actionPerformed=self.inflorFlowersTwoClick, font=buttonFont, margin=buttonMargin)
        self.inflorFlowersTwo.setBounds(59, 76, 39, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersTwo.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersTwo.GroupIndex = 15
        self.page7.add(self.inflorFlowersTwo)
        self.inflorFlowersThreeImage = toolkit.createImage("../resources/WizardForm_inflorFlowersThree.png")
        self.inflorFlowersThree = SpeedButton('three', ImageIcon(self.inflorFlowersThreeImage), 1, actionPerformed=self.inflorFlowersThreeClick, font=buttonFont, margin=buttonMargin)
        self.inflorFlowersThree.setBounds(97, 76, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersThree.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersThree.GroupIndex = 15
        self.page7.add(self.inflorFlowersThree)
        self.inflorFlowersFiveImage = toolkit.createImage("../resources/WizardForm_inflorFlowersFive.png")
        self.inflorFlowersFive = SpeedButton('five', ImageIcon(self.inflorFlowersFiveImage), actionPerformed=self.inflorFlowersFiveClick, font=buttonFont, margin=buttonMargin)
        self.inflorFlowersFive.setBounds(141, 76, 40, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersFive.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersFive.GroupIndex = 15
        self.page7.add(self.inflorFlowersFive)
        self.inflorFlowersTenImage = toolkit.createImage("../resources/WizardForm_inflorFlowersTen.png")
        self.inflorFlowersTen = SpeedButton('ten', ImageIcon(self.inflorFlowersTenImage), actionPerformed=self.inflorFlowersTenClick, font=buttonFont, margin=buttonMargin)
        self.inflorFlowersTen.setBounds(180, 76, 40, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersTen.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersTen.GroupIndex = 15
        self.page7.add(self.inflorFlowersTen)
        self.inflorFlowersTwentyImage = toolkit.createImage("../resources/WizardForm_inflorFlowersTwenty.png")
        self.inflorFlowersTwenty = SpeedButton('twenty', ImageIcon(self.inflorFlowersTwentyImage), actionPerformed=self.inflorFlowersTwentyClick, font=buttonFont, margin=buttonMargin)
        self.inflorFlowersTwenty.setBounds(219, 76, 50, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersTwenty.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorFlowersTwenty.GroupIndex = 15
        self.page7.add(self.inflorFlowersTwenty)
        self.inflorShapeSpikeImage = toolkit.createImage("../resources/WizardForm_inflorShapeSpike.png")
        self.inflorShapeSpike = SpeedButton('spike', ImageIcon(self.inflorShapeSpikeImage), font=buttonFont, margin=buttonMargin)
        self.inflorShapeSpike.setBounds(24, 163, 42, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeSpike.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeSpike.GroupIndex = 16
        self.page7.add(self.inflorShapeSpike)
        self.inflorShapeRacemeImage = toolkit.createImage("../resources/WizardForm_inflorShapeRaceme.png")
        self.inflorShapeRaceme = SpeedButton('raceme', ImageIcon(self.inflorShapeRacemeImage), 1, font=buttonFont, margin=buttonMargin)
        self.inflorShapeRaceme.setBounds(65, 163, 57, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeRaceme.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeRaceme.GroupIndex = 16
        self.page7.add(self.inflorShapeRaceme)
        self.inflorShapePanicleImage = toolkit.createImage("../resources/WizardForm_inflorShapePanicle.png")
        self.inflorShapePanicle = SpeedButton('panicle', ImageIcon(self.inflorShapePanicleImage), font=buttonFont, margin=buttonMargin)
        self.inflorShapePanicle.setBounds(122, 163, 50, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapePanicle.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapePanicle.GroupIndex = 16
        self.page7.add(self.inflorShapePanicle)
        self.inflorShapeUmbelImage = toolkit.createImage("../resources/WizardForm_inflorShapeUmbel.png")
        self.inflorShapeUmbel = SpeedButton('umbel', ImageIcon(self.inflorShapeUmbelImage), font=buttonFont, margin=buttonMargin)
        self.inflorShapeUmbel.setBounds(171, 163, 48, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeUmbel.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeUmbel.GroupIndex = 16
        self.page7.add(self.inflorShapeUmbel)
        self.inflorShapeClusterImage = toolkit.createImage("../resources/WizardForm_inflorShapeCluster.png")
        self.inflorShapeCluster = SpeedButton('cluster', ImageIcon(self.inflorShapeClusterImage), font=buttonFont, margin=buttonMargin)
        self.inflorShapeCluster.setBounds(218, 163, 47, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeCluster.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeCluster.GroupIndex = 16
        self.page7.add(self.inflorShapeCluster)
        self.inflorShapeHeadImage = toolkit.createImage("../resources/WizardForm_inflorShapeHead.png")
        self.inflorShapeHead = SpeedButton('head', ImageIcon(self.inflorShapeHeadImage), font=buttonFont, margin=buttonMargin)
        self.inflorShapeHead.setBounds(264, 163, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeHead.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorShapeHead.GroupIndex = 16
        self.page7.add(self.inflorShapeHead)
        self.arrowInflorThicknessImage = toolkit.createImage("../resources/WizardForm_arrowInflorThickness.png")
        self.arrowInflorThickness = ImagePanel(ImageIcon(self.arrowInflorThicknessImage))
        self.arrowInflorThickness.setBounds(294, 57, 8, 16)
        self.page7.add(self.arrowInflorThickness)
        self.inflorThicknessLabel = JLabel('How thick should each inflorescence stem be?', font=buttonFont)
        self.inflorThicknessLabel.setBounds(308, 59, 226, 14)
        self.page7.add(self.inflorThicknessLabel)
        self.inflorWidthVeryThinImage = toolkit.createImage("../resources/WizardForm_inflorWidthVeryThin.png")
        self.inflorWidthVeryThin = SpeedButton('very thin', ImageIcon(self.inflorWidthVeryThinImage), font=buttonFont, margin=buttonMargin)
        self.inflorWidthVeryThin.setBounds(308, 76, 56, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthVeryThin.Layout = blGlyphTop
        self.inflorWidthVeryThin.toolTipText = 'very short'
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthVeryThin.GroupIndex = 24
        self.page7.add(self.inflorWidthVeryThin)
        self.inflorWidthThinImage = toolkit.createImage("../resources/WizardForm_inflorWidthThin.png")
        self.inflorWidthThin = SpeedButton('thin', ImageIcon(self.inflorWidthThinImage), 1, font=buttonFont, margin=buttonMargin)
        self.inflorWidthThin.setBounds(364, 76, 36, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthThin.Layout = blGlyphTop
        self.inflorWidthThin.toolTipText = 'short'
        self.inflorWidthThin.putClientProperty("tag", 1)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthThin.GroupIndex = 24
        self.page7.add(self.inflorWidthThin)
        self.inflorWidthMediumImage = toolkit.createImage("../resources/WizardForm_inflorWidthMedium.png")
        self.inflorWidthMedium = SpeedButton('medium', ImageIcon(self.inflorWidthMediumImage), font=buttonFont, margin=buttonMargin)
        self.inflorWidthMedium.setBounds(400, 76, 49, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthMedium.Layout = blGlyphTop
        self.inflorWidthMedium.toolTipText = 'medium'
        self.inflorWidthMedium.putClientProperty("tag", 2)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthMedium.GroupIndex = 24
        self.page7.add(self.inflorWidthMedium)
        self.inflorWidthThickImage = toolkit.createImage("../resources/WizardForm_inflorWidthThick.png")
        self.inflorWidthThick = SpeedButton('thick', ImageIcon(self.inflorWidthThickImage), font=buttonFont, margin=buttonMargin)
        self.inflorWidthThick.setBounds(448, 76, 37, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthThick.Layout = blGlyphTop
        self.inflorWidthThick.toolTipText = 'long'
        self.inflorWidthThick.putClientProperty("tag", 3)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthThick.GroupIndex = 24
        self.page7.add(self.inflorWidthThick)
        self.inflorWidthVeryThickImage = toolkit.createImage("../resources/WizardForm_inflorWidthVeryThick.png")
        self.inflorWidthVeryThick = SpeedButton('very thick', ImageIcon(self.inflorWidthVeryThickImage), font=buttonFont, margin=buttonMargin)
        self.inflorWidthVeryThick.setBounds(484, 76, 59, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthVeryThick.Layout = blGlyphTop
        self.inflorWidthVeryThick.toolTipText = 'very long'
        self.inflorWidthVeryThick.putClientProperty("tag", 4)
        #  --------------- UNHANDLED ATTRIBUTE: self.inflorWidthVeryThick.GroupIndex = 24
        self.page7.add(self.inflorWidthVeryThick)
        self.Label8 = JLabel('Inflorescences can have a large variety of shapes, a few of which are shown here. We extend the true meaning of "inflorescence" a bit to use an inflorescence when there is only one flower. ', font=buttonFont)
        self.Label8.setBounds(12, 22, 485, 28)
        self.page7.add(self.Label8)
        self.wizardNotebook.addTab('Inflorescences', None, self.page7)
        
        self.page8 = JPanel(layout=None)
        self.panelFlowersLabel = JLabel('Flowers', font=buttonFont)
        self.panelFlowersLabel.setBounds(8, 4, 45, 14)
        self.page8.add(self.panelFlowersLabel)
        self.petalTdosLabel = JLabel(' What 3D object should be used for a flower petal?', font=buttonFont)
        self.petalTdosLabel.setBounds(22, 60, 246, 14)
        self.page8.add(self.petalTdosLabel)
        self.petalScaleLabel = JLabel('How big should a flower petal be drawn?', font=buttonFont)
        self.petalScaleLabel.setBounds(302, 60, 201, 14)
        self.page8.add(self.petalScaleLabel)
        self.petalsNumberLabel = JLabel('How many flower petals should a flower have?', font=buttonFont)
        self.petalsNumberLabel.setBounds(24, 170, 231, 14)
        self.page8.add(self.petalsNumberLabel)
        self.petalsOneImage = toolkit.createImage("../resources/WizardForm_petalsOne.png")
        self.petalsOne = SpeedButton('one', ImageIcon(self.petalsOneImage), font=buttonFont, margin=buttonMargin)
        self.petalsOne.setBounds(24, 187, 37, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsOne.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsOne.GroupIndex = 13
        self.page8.add(self.petalsOne)
        self.petalsThreeImage = toolkit.createImage("../resources/WizardForm_petalsThree.png")
        self.petalsThree = SpeedButton('three', ImageIcon(self.petalsThreeImage), font=buttonFont, margin=buttonMargin)
        self.petalsThree.setBounds(60, 187, 42, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsThree.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsThree.GroupIndex = 13
        self.page8.add(self.petalsThree)
        self.petalsFourImage = toolkit.createImage("../resources/WizardForm_petalsFour.png")
        self.petalsFour = SpeedButton('four', ImageIcon(self.petalsFourImage), font=buttonFont, margin=buttonMargin)
        self.petalsFour.setBounds(101, 187, 40, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsFour.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsFour.GroupIndex = 13
        self.page8.add(self.petalsFour)
        self.petalsFiveImage = toolkit.createImage("../resources/WizardForm_petalsFive.png")
        self.petalsFive = SpeedButton('five', ImageIcon(self.petalsFiveImage), 1, font=buttonFont, margin=buttonMargin)
        self.petalsFive.setBounds(140, 187, 37, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsFive.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsFive.GroupIndex = 13
        self.page8.add(self.petalsFive)
        self.petalsTenImage = toolkit.createImage("../resources/WizardForm_petalsTen.png")
        self.petalsTen = SpeedButton('ten', ImageIcon(self.petalsTenImage), font=buttonFont, margin=buttonMargin)
        self.petalsTen.setBounds(176, 187, 36, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsTen.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalsTen.GroupIndex = 13
        self.page8.add(self.petalsTen)
        self.petalScaleTinyImage = toolkit.createImage("../resources/WizardForm_petalScaleTiny.png")
        self.petalScaleTiny = SpeedButton('tiny', ImageIcon(self.petalScaleTinyImage), font=buttonFont, margin=buttonMargin)
        self.petalScaleTiny.setBounds(302, 76, 43, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleTiny.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleTiny.GroupIndex = 14
        self.page8.add(self.petalScaleTiny)
        self.petalScaleSmallImage = toolkit.createImage("../resources/WizardForm_petalScaleSmall.png")
        self.petalScaleSmall = SpeedButton('small', ImageIcon(self.petalScaleSmallImage), 1, font=buttonFont, margin=buttonMargin)
        self.petalScaleSmall.setBounds(344, 76, 47, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleSmall.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleSmall.GroupIndex = 14
        self.page8.add(self.petalScaleSmall)
        self.petalScaleMediumImage = toolkit.createImage("../resources/WizardForm_petalScaleMedium.png")
        self.petalScaleMedium = SpeedButton('medium', ImageIcon(self.petalScaleMediumImage), font=buttonFont, margin=buttonMargin)
        self.petalScaleMedium.setBounds(390, 76, 58, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleMedium.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleMedium.GroupIndex = 14
        self.page8.add(self.petalScaleMedium)
        self.petalScaleLargeImage = toolkit.createImage("../resources/WizardForm_petalScaleLarge.png")
        self.petalScaleLarge = SpeedButton('large', ImageIcon(self.petalScaleLargeImage), font=buttonFont, margin=buttonMargin)
        self.petalScaleLarge.setBounds(447, 76, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleLarge.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleLarge.GroupIndex = 14
        self.page8.add(self.petalScaleLarge)
        self.petalScaleHugeImage = toolkit.createImage("../resources/WizardForm_petalScaleHuge.png")
        self.petalScaleHuge = SpeedButton('huge', ImageIcon(self.petalScaleHugeImage), font=buttonFont, margin=buttonMargin)
        self.petalScaleHuge.setBounds(491, 76, 46, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleHuge.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.petalScaleHuge.GroupIndex = 14
        self.page8.add(self.petalScaleHuge)
        self.arrowPetalTdosImage = toolkit.createImage("../resources/WizardForm_arrowPetalTdos.png")
        self.arrowPetalTdos = ImagePanel(ImageIcon(self.arrowPetalTdosImage))
        self.arrowPetalTdos.setBounds(12, 58, 8, 16)
        self.page8.add(self.arrowPetalTdos)
        self.arrowPetalsNumberImage = toolkit.createImage("../resources/WizardForm_arrowPetalsNumber.png")
        self.arrowPetalsNumber = ImagePanel(ImageIcon(self.arrowPetalsNumberImage))
        self.arrowPetalsNumber.setBounds(12, 169, 8, 16)
        self.page8.add(self.arrowPetalsNumber)
        self.arrowPetalScaleImage = toolkit.createImage("../resources/WizardForm_arrowPetalScale.png")
        self.arrowPetalScale = ImagePanel(ImageIcon(self.arrowPetalScaleImage))
        self.arrowPetalScale.setBounds(288, 58, 8, 16)
        self.page8.add(self.arrowPetalScale)
        self.arrowPetalColorImage = toolkit.createImage("../resources/WizardForm_arrowPetalColor.png")
        self.arrowPetalColor = ImagePanel(ImageIcon(self.arrowPetalColorImage))
        self.arrowPetalColor.setBounds(288, 173, 8, 16)
        self.page8.add(self.arrowPetalColor)
        self.petalColorLabel = JLabel(' What color should flowers be drawn?', font=buttonFont)
        self.petalColorLabel.setBounds(300, 173, 187, 14)
        self.page8.add(self.petalColorLabel)
        self.flowerColorExplainLabel = JLabel('Click in the square to change the color.', font=buttonFont)
        self.flowerColorExplainLabel.setBounds(352, 211, 187, 14)
        self.page8.add(self.flowerColorExplainLabel)
        self.Label9 = JLabel('Like leaves, flowers are drawn using a 3D object. But here the 3D object represents only one petal of the flower. A number of petals is drawn rotated around a center to produce what looks like a flower.', font=buttonFont)
        self.Label9.setBounds(12, 22, 511, 28)
        self.page8.add(self.Label9)
        self.petalTdoSelectedLabel = JLabel('petalTdoSelectedLabel', font=buttonFont)
        self.petalTdoSelectedLabel.setBounds(24, 148, 109, 14)
        self.page8.add(self.petalTdoSelectedLabel)
        self.petalTdosDraw = JTable(DefaultTableModel())
        self.petalTdosDraw.setBounds(24, 76, 250, 69)
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.OnDrawCell = petalTdosDrawDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.RowCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.DefaultColWidth = 40
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.ColCount = 20
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.DefaultRowHeight = 50
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.ScrollBars = ssHorizontal
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.OnSelectCell = petalTdosDrawSelectCell
        #  --------------- UNHANDLED ATTRIBUTE: self.petalTdosDraw.Options = [goVertLine, goHorzLine]
        self.page8.add(self.petalTdosDraw)
        self.petalColor = JPanel(layout=None)
        # -- self.petalColor.setLayout(BoxLayout(self.petalColor, BoxLayout.Y_AXIS))
        self.petalColor.setBounds(302, 197, 41, 41)
        self.petalColor.mouseReleased = self.petalColorMouseUp
        self.page8.add(self.petalColor)
        self.wizardNotebook.addTab('Flowers', None, self.page8)
        
        self.page9 = JPanel(layout=None)
        self.fruitTdoLabel = JLabel(' What 3D object should be used to draw each fruit section?', font=buttonFont)
        self.fruitTdoLabel.setBounds(22, 77, 287, 14)
        self.page9.add(self.fruitTdoLabel)
        self.fruitSectionsNumberLabel = JLabel('How many fruit sections should be used to draw the fruit?', font=buttonFont)
        self.fruitSectionsNumberLabel.setBounds(24, 187, 282, 14)
        self.page9.add(self.fruitSectionsNumberLabel)
        self.fruitScaleLabel = JLabel('How big should fruit sections be drawn?', font=buttonFont)
        self.fruitScaleLabel.setBounds(328, 77, 197, 14)
        self.page9.add(self.fruitScaleLabel)
        self.panelFruitsLabel = JLabel('Fruits', font=buttonFont)
        self.panelFruitsLabel.setBounds(4, 4, 32, 14)
        self.page9.add(self.panelFruitsLabel)
        self.arrowFruitTdoImage = toolkit.createImage("../resources/WizardForm_arrowFruitTdo.png")
        self.arrowFruitTdo = ImagePanel(ImageIcon(self.arrowFruitTdoImage))
        self.arrowFruitTdo.setBounds(12, 75, 8, 16)
        self.page9.add(self.arrowFruitTdo)
        self.arrowFruitSectionsNumberImage = toolkit.createImage("../resources/WizardForm_arrowFruitSectionsNumber.png")
        self.arrowFruitSectionsNumber = ImagePanel(ImageIcon(self.arrowFruitSectionsNumberImage))
        self.arrowFruitSectionsNumber.setBounds(12, 185, 8, 16)
        self.page9.add(self.arrowFruitSectionsNumber)
        self.arrowFruitScaleImage = toolkit.createImage("../resources/WizardForm_arrowFruitScale.png")
        self.arrowFruitScale = ImagePanel(ImageIcon(self.arrowFruitScaleImage))
        self.arrowFruitScale.setBounds(316, 75, 8, 16)
        self.page9.add(self.arrowFruitScale)
        self.fruitSectionsOneImage = toolkit.createImage("../resources/WizardForm_fruitSectionsOne.png")
        self.fruitSectionsOne = SpeedButton('one', ImageIcon(self.fruitSectionsOneImage), font=buttonFont, margin=buttonMargin)
        self.fruitSectionsOne.setBounds(24, 203, 41, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsOne.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsOne.GroupIndex = 21
        self.page9.add(self.fruitSectionsOne)
        self.fruitSectionsThreeImage = toolkit.createImage("../resources/WizardForm_fruitSectionsThree.png")
        self.fruitSectionsThree = SpeedButton('three', ImageIcon(self.fruitSectionsThreeImage), font=buttonFont, margin=buttonMargin)
        self.fruitSectionsThree.setBounds(64, 203, 43, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsThree.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsThree.GroupIndex = 21
        self.page9.add(self.fruitSectionsThree)
        self.fruitSectionsFourImage = toolkit.createImage("../resources/WizardForm_fruitSectionsFour.png")
        self.fruitSectionsFour = SpeedButton('four', ImageIcon(self.fruitSectionsFourImage), font=buttonFont, margin=buttonMargin)
        self.fruitSectionsFour.setBounds(106, 203, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsFour.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsFour.GroupIndex = 21
        self.page9.add(self.fruitSectionsFour)
        self.fruitSectionsFiveImage = toolkit.createImage("../resources/WizardForm_fruitSectionsFive.png")
        self.fruitSectionsFive = SpeedButton('five', ImageIcon(self.fruitSectionsFiveImage), 1, font=buttonFont, margin=buttonMargin)
        self.fruitSectionsFive.setBounds(148, 203, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsFive.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsFive.GroupIndex = 21
        self.page9.add(self.fruitSectionsFive)
        self.fruitSectionsTenImage = toolkit.createImage("../resources/WizardForm_fruitSectionsTen.png")
        self.fruitSectionsTen = SpeedButton('ten', ImageIcon(self.fruitSectionsTenImage), font=buttonFont, margin=buttonMargin)
        self.fruitSectionsTen.setBounds(192, 203, 40, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsTen.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitSectionsTen.GroupIndex = 21
        self.page9.add(self.fruitSectionsTen)
        self.fruitScaleTinyImage = toolkit.createImage("../resources/WizardForm_fruitScaleTiny.png")
        self.fruitScaleTiny = SpeedButton('tiny', ImageIcon(self.fruitScaleTinyImage), font=buttonFont, margin=buttonMargin)
        self.fruitScaleTiny.setBounds(328, 93, 41, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleTiny.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleTiny.GroupIndex = 22
        self.page9.add(self.fruitScaleTiny)
        self.fruitScaleSmallImage = toolkit.createImage("../resources/WizardForm_fruitScaleSmall.png")
        self.fruitScaleSmall = SpeedButton('small', ImageIcon(self.fruitScaleSmallImage), 1, font=buttonFont, margin=buttonMargin)
        self.fruitScaleSmall.setBounds(368, 93, 43, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleSmall.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleSmall.GroupIndex = 22
        self.page9.add(self.fruitScaleSmall)
        self.fruitScaleMediumImage = toolkit.createImage("../resources/WizardForm_fruitScaleMedium.png")
        self.fruitScaleMedium = SpeedButton('medium', ImageIcon(self.fruitScaleMediumImage), font=buttonFont, margin=buttonMargin)
        self.fruitScaleMedium.setBounds(410, 93, 56, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleMedium.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleMedium.GroupIndex = 22
        self.page9.add(self.fruitScaleMedium)
        self.fruitScaleLargeImage = toolkit.createImage("../resources/WizardForm_fruitScaleLarge.png")
        self.fruitScaleLarge = SpeedButton('large', ImageIcon(self.fruitScaleLargeImage), font=buttonFont, margin=buttonMargin)
        self.fruitScaleLarge.setBounds(465, 93, 45, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleLarge.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleLarge.GroupIndex = 22
        self.page9.add(self.fruitScaleLarge)
        self.fruitScaleHugeImage = toolkit.createImage("../resources/WizardForm_fruitScaleHuge.png")
        self.fruitScaleHuge = SpeedButton('huge', ImageIcon(self.fruitScaleHugeImage), font=buttonFont, margin=buttonMargin)
        self.fruitScaleHuge.setBounds(509, 93, 40, 60)
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleHuge.Layout = blGlyphTop
        #  --------------- UNHANDLED ATTRIBUTE: self.fruitScaleHuge.GroupIndex = 22
        self.page9.add(self.fruitScaleHuge)
        self.fruitColorLabel = JLabel(' What color should fruits be drawn?', font=buttonFont)
        self.fruitColorLabel.setBounds(326, 187, 174, 14)
        self.page9.add(self.fruitColorLabel)
        self.arrowFruitColorImage = toolkit.createImage("../resources/WizardForm_arrowFruitColor.png")
        self.arrowFruitColor = ImagePanel(ImageIcon(self.arrowFruitColorImage))
        self.arrowFruitColor.setBounds(316, 185, 8, 16)
        self.page9.add(self.arrowFruitColor)
        self.fruitColorExplainLabel = JLabel('Click in the square to change the color.', font=buttonFont)
        self.fruitColorExplainLabel.setBounds(374, 227, 187, 14)
        self.page9.add(self.fruitColorExplainLabel)
        self.arrowShowFruitsImage = toolkit.createImage("../resources/WizardForm_arrowShowFruits.png")
        self.arrowShowFruits = ImagePanel(ImageIcon(self.arrowShowFruitsImage))
        self.arrowShowFruits.setBounds(12, 53, 8, 16)
        self.page9.add(self.arrowShowFruits)
        self.showFruitsLabel = JLabel('Do you want to see fruits on your plant?', font=buttonFont)
        self.showFruitsLabel.setBounds(24, 55, 195, 14)
        self.page9.add(self.showFruitsLabel)
        self.Label10 = JLabel('Fruits are drawn like flowers, but with a portion of the fruit (a "fruit section") rotated around instead of a petal. For many plants you will not be interested in the fruit, so you can turn fruits off entirely.', font=buttonFont)
        self.Label10.setBounds(12, 22, 496, 28)
        self.page9.add(self.Label10)
        self.sectionTdoSelectedLabel = JLabel('sectionTdoSelectedLabel', font=buttonFont)
        self.sectionTdoSelectedLabel.setBounds(24, 166, 121, 14)
        self.page9.add(self.sectionTdoSelectedLabel)
        self.sectionTdosDraw = JTable(DefaultTableModel())
        self.sectionTdosDraw.setBounds(24, 93, 250, 69)
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.OnDrawCell = sectionTdosDrawDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.RowCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.DefaultColWidth = 40
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.ColCount = 20
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.DefaultRowHeight = 50
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.ScrollBars = ssHorizontal
        self.sectionTdosDraw.mouseMoved = self.sectionTdosDrawMouseMove
        self.sectionTdosDraw.mouseDragged = self.sectionTdosDrawMouseMove
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.FixedCols = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.OnSelectCell = sectionTdosDrawSelectCell
        #  --------------- UNHANDLED ATTRIBUTE: self.sectionTdosDraw.Options = [goVertLine, goHorzLine]
        self.page9.add(self.sectionTdosDraw)
        self.fruitColor = JPanel(layout=None)
        # -- self.fruitColor.setLayout(BoxLayout(self.fruitColor, BoxLayout.Y_AXIS))
        self.fruitColor.setBounds(328, 213, 41, 41)
        self.fruitColor.mouseReleased = self.fruitColorMouseUp
        self.page9.add(self.fruitColor)
        self.showFruitsYes = JRadioButton('yes', actionPerformed=self.showFruitsYesClick, font=buttonFont, margin=buttonMargin)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.showFruitsYes)
        self.showFruitsYes.setBounds(226, 53, 53, 17)
        self.page9.add(self.showFruitsYes)
        self.showFruitsNo = JRadioButton('no', actionPerformed=self.showFruitsNoClick, font=buttonFont, margin=buttonMargin)
        # ----- manually fix radio button group by putting multiple buttons in the same group
        group = ButtonGroup()
        group.add(self.showFruitsNo)
        self.showFruitsNo.setBounds(270, 53, 45, 17)
        self.page9.add(self.showFruitsNo)
        self.wizardNotebook.addTab('Fruit', None, self.page9)
        
        self.page10 = JPanel(layout=None)
        self.finishLabelFirst = JLabel('You have finished designing your new plant. You can name your new plant here, or just keep this name.', font=buttonFont)
        self.finishLabelFirst.setBounds(12, 46, 263, 28)
        self.page10.add(self.finishLabelFirst)
        self.finishLabelSecond = JLabel('Now click Finish to place your plant in the main window, or click Cancel to stop without creating a plant, or click Back to change your choices.', font=buttonFont)
        self.finishLabelSecond.setBounds(12, 107, 236, 42)
        self.page10.add(self.finishLabelSecond)
        self.finishLabelThird = JLabel('Once your plant is made, you can fine-tune the parameters that define your plant in the Parameters panel in the main window. ', font=buttonFont)
        self.finishLabelThird.setBounds(12, 189, 229, 42)
        self.page10.add(self.finishLabelThird)
        self.panelFinishLabel = JLabel('Congratulations!', font=buttonFont)
        self.panelFinishLabel.setBounds(12, 20, 91, 14)
        self.page10.add(self.panelFinishLabel)
        self.previewLabel = JLabel('Preview', font=buttonFont)
        self.previewLabel.setBounds(405, 6, 40, 14)
        self.page10.add(self.previewLabel)
        self.turnLeftImage = toolkit.createImage("../resources/WizardForm_turnLeft.png")
        self.turnLeft = SpeedButton(ImageIcon(self.turnLeftImage), actionPerformed=self.turnLeftClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.turnLeft.setBounds(444, 237, 25, 25)
        self.page10.add(self.turnLeft)
        self.turnRightImage = toolkit.createImage("../resources/WizardForm_turnRight.png")
        self.turnRight = SpeedButton(ImageIcon(self.turnRightImage), actionPerformed=self.turnRightClick, font=buttonFont, margin=buttonMargin)
        # ----- NumGlyphs was 2. Should split image file manually and use setPressedIcon(Icon)
        self.turnRight.setBounds(469, 237, 25, 25)
        self.page10.add(self.turnRight)
        self.Label12 = JLabel('You can also click on the pictures below to return to any of the wizard panels.', font=buttonFont)
        self.Label12.setBounds(12, 156, 243, 28)
        self.page10.add(self.Label12)
        self.newPlantName = JTextField('New plant', 10)
        self.newPlantName.setBounds(12, 78, 237, 22)
        self.page10.add(self.newPlantName)
        self.previewPanel = JPanel(layout=None)
        # -- self.previewPanel.setLayout(BoxLayout(self.previewPanel, BoxLayout.Y_AXIS))
        self.previewPanel.setBounds(299, 22, 251, 213)
        self.page10.add(self.previewPanel)
        self.randomizePlant = JButton('Randomize', actionPerformed=self.randomizePlantClick, font=buttonFont, margin=buttonMargin)
        self.randomizePlant.setMnemonic(KeyEvent.VK_R)
        self.randomizePlant.setBounds(365, 237, 74, 25)
        self.page10.add(self.randomizePlant)
        self.wizardNotebook.addTab('Finish', None, self.page10)
        
        self.wizardNotebook.setBounds(0, 0, 569, 267)
        #  --------------- UNHANDLED ATTRIBUTE: self.wizardNotebook.PageIndex = 9
        self.cancel = JButton('Cancel', actionPerformed=self.cancelClick, font=buttonFont, margin=buttonMargin)
        self.cancel.setMnemonic(KeyEvent.VK_C)
        self.cancel.setBounds(518, 276, 50, 21)
        self.back = JButton('< Back', actionPerformed=self.backClick, font=buttonFont, margin=buttonMargin)
        self.back.setMnemonic(KeyEvent.VK_B)
        self.back.setBounds(414, 276, 50, 21)
        self.next = JButton('Next >', actionPerformed=self.nextClick, font=buttonFont, margin=buttonMargin)
        self.next.setMnemonic(KeyEvent.VK_N)
        self.next.setBounds(466, 276, 50, 21)
        self.defaultChoices = JButton('Defaults', actionPerformed=self.defaultChoicesClick, font=buttonFont, margin=buttonMargin)
        self.defaultChoices.setMnemonic(KeyEvent.VK_D)
        self.defaultChoices.setBounds(60, 276, 50, 21)
        self.startPageImageImage = toolkit.createImage("../resources/WizardForm_startPageImage.png")
        self.startPageImage = ImagePanel(ImageIcon(self.startPageImageImage))
        self.startPageImage.setBounds(12, 8, 20, 20)
        self.meristemsPageImageImage = toolkit.createImage("../resources/WizardForm_meristemsPageImage.png")
        self.meristemsPageImage = ImagePanel(ImageIcon(self.meristemsPageImageImage))
        self.meristemsPageImage.setBounds(36, 8, 20, 20)
        self.internodesPageImageImage = toolkit.createImage("../resources/WizardForm_internodesPageImage.png")
        self.internodesPageImage = ImagePanel(ImageIcon(self.internodesPageImageImage))
        self.internodesPageImage.setBounds(68, 8, 20, 20)
        self.leavesPageImageImage = toolkit.createImage("../resources/WizardForm_leavesPageImage.png")
        self.leavesPageImage = ImagePanel(ImageIcon(self.leavesPageImageImage))
        self.leavesPageImage.setBounds(100, 8, 20, 20)
        self.compoundLeavesPageImageImage = toolkit.createImage("../resources/WizardForm_compoundLeavesPageImage.png")
        self.compoundLeavesPageImage = ImagePanel(ImageIcon(self.compoundLeavesPageImageImage))
        self.compoundLeavesPageImage.setBounds(132, 8, 20, 20)
        self.flowersPageImageImage = toolkit.createImage("../resources/WizardForm_flowersPageImage.png")
        self.flowersPageImage = ImagePanel(ImageIcon(self.flowersPageImageImage))
        self.flowersPageImage.setBounds(220, 4, 20, 20)
        self.inflorDrawPageImageImage = toolkit.createImage("../resources/WizardForm_inflorDrawPageImage.png")
        self.inflorDrawPageImage = ImagePanel(ImageIcon(self.inflorDrawPageImageImage))
        self.inflorDrawPageImage.setBounds(192, 8, 20, 20)
        self.inflorPlacePageImageImage = toolkit.createImage("../resources/WizardForm_inflorPlacePageImage.png")
        self.inflorPlacePageImage = ImagePanel(ImageIcon(self.inflorPlacePageImageImage))
        self.inflorPlacePageImage.setBounds(168, 8, 20, 20)
        self.fruitsPageImageImage = toolkit.createImage("../resources/WizardForm_fruitsPageImage.png")
        self.fruitsPageImage = ImagePanel(ImageIcon(self.fruitsPageImageImage))
        self.fruitsPageImage.setBounds(248, 4, 20, 20)
        self.finishPageImageImage = toolkit.createImage("../resources/WizardForm_finishPageImage.png")
        self.finishPageImage = ImagePanel(ImageIcon(self.finishPageImageImage))
        self.finishPageImage.setBounds(276, 4, 20, 20)
        self.inflorDrawPageImageDisabledImage = toolkit.createImage("../resources/WizardForm_inflorDrawPageImageDisabled.png")
        self.inflorDrawPageImageDisabled = ImagePanel(ImageIcon(self.inflorDrawPageImageDisabledImage))
        self.inflorDrawPageImageDisabled.setBounds(188, 32, 20, 20)
        self.flowersPageImageDisabledImage = toolkit.createImage("../resources/WizardForm_flowersPageImageDisabled.png")
        self.flowersPageImageDisabled = ImagePanel(ImageIcon(self.flowersPageImageDisabledImage))
        self.flowersPageImageDisabled.setBounds(216, 32, 20, 20)
        self.fruitsPageImageDisabledImage = toolkit.createImage("../resources/WizardForm_fruitsPageImageDisabled.png")
        self.fruitsPageImageDisabled = ImagePanel(ImageIcon(self.fruitsPageImageDisabledImage))
        self.fruitsPageImageDisabled.setBounds(248, 32, 20, 20)
        self.hiddenPicturesPanel = JPanel(layout=None)
        # -- self.hiddenPicturesPanel.setLayout(BoxLayout(self.hiddenPicturesPanel, BoxLayout.Y_AXIS))
        self.hiddenPicturesPanel.add(self.startPageImage)
        self.hiddenPicturesPanel.add(self.meristemsPageImage)
        self.hiddenPicturesPanel.add(self.internodesPageImage)
        self.hiddenPicturesPanel.add(self.leavesPageImage)
        self.hiddenPicturesPanel.add(self.compoundLeavesPageImage)
        self.hiddenPicturesPanel.add(self.flowersPageImage)
        self.hiddenPicturesPanel.add(self.inflorDrawPageImage)
        self.hiddenPicturesPanel.add(self.inflorPlacePageImage)
        self.hiddenPicturesPanel.add(self.fruitsPageImage)
        self.hiddenPicturesPanel.add(self.finishPageImage)
        self.hiddenPicturesPanel.add(self.inflorDrawPageImageDisabled)
        self.hiddenPicturesPanel.add(self.flowersPageImageDisabled)
        self.hiddenPicturesPanel.add(self.fruitsPageImageDisabled)
        self.hiddenPicturesPanel.setBounds(18, 406, 325, 57)
        self.hiddenPicturesPanel.visible = 0
        self.progressDrawGrid = JTable(DefaultTableModel())
        self.progressDrawGrid.setBounds(190, 276, 220, 21)
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.ColCount = 10
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.BorderStyle = bsNone
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.OnDrawCell = progressDrawGridDrawCell
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.DefaultDrawing = False
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.TabStop = False
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.GridLineWidth = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.DefaultRowHeight = 20
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.OnSelectCell = progressDrawGridSelectCell
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.FixedRows = 0
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.ScrollBars = ssNone
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.Options = [goFixedVertLine, goFixedHorzLine, goHorzLine]
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.DefaultColWidth = 20
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.RowCount = 1
        #  --------------- UNHANDLED ATTRIBUTE: self.progressDrawGrid.FixedCols = 0
        contentPane.add(self.helpButton)
        contentPane.add(self.changeTdoLibrary)
        contentPane.add(self.wizardNotebook)
        contentPane.add(self.cancel)
        contentPane.add(self.back)
        contentPane.add(self.next)
        contentPane.add(self.defaultChoices)
        contentPane.add(self.hiddenPicturesPanel)
        contentPane.add(self.progressDrawGrid)
        
    def FormKeyPress(self, event):
        print "FormKeyPress"
        
    def apicalInflorsFiveClick(self, event):
        print "apicalInflorsFiveClick"
        
    def apicalInflorsNoneClick(self, event):
        print "apicalInflorsNoneClick"
        
    def apicalInflorsOneClick(self, event):
        print "apicalInflorsOneClick"
        
    def apicalInflorsThreeClick(self, event):
        print "apicalInflorsThreeClick"
        
    def apicalInflorsTwoClick(self, event):
        print "apicalInflorsTwoClick"
        
    def axillaryInflorsFiveClick(self, event):
        print "axillaryInflorsFiveClick"
        
    def axillaryInflorsNoneClick(self, event):
        print "axillaryInflorsNoneClick"
        
    def axillaryInflorsTenClick(self, event):
        print "axillaryInflorsTenClick"
        
    def axillaryInflorsThreeClick(self, event):
        print "axillaryInflorsThreeClick"
        
    def axillaryInflorsTwentyClick(self, event):
        print "axillaryInflorsTwentyClick"
        
    def backClick(self, event):
        print "backClick"
        
    def branchLittleClick(self, event):
        print "branchLittleClick"
        
    def branchLotClick(self, event):
        print "branchLotClick"
        
    def branchMediumClick(self, event):
        print "branchMediumClick"
        
    def branchNoneClick(self, event):
        print "branchNoneClick"
        
    def cancelClick(self, event):
        print "cancelClick"
        
    def changeTdoLibraryClick(self, event):
        print "changeTdoLibraryClick"
        
    def defaultChoicesClick(self, event):
        print "defaultChoicesClick"
        
    def fruitColorMouseUp(self, event):
        print "fruitColorMouseUp"
        
    def helpButtonClick(self, event):
        print "helpButtonClick"
        
    def inflorFlowersFiveClick(self, event):
        print "inflorFlowersFiveClick"
        
    def inflorFlowersOneClick(self, event):
        print "inflorFlowersOneClick"
        
    def inflorFlowersTenClick(self, event):
        print "inflorFlowersTenClick"
        
    def inflorFlowersThreeClick(self, event):
        print "inflorFlowersThreeClick"
        
    def inflorFlowersTwentyClick(self, event):
        print "inflorFlowersTwentyClick"
        
    def inflorFlowersTwoClick(self, event):
        print "inflorFlowersTwoClick"
        
    def leafletsFiveClick(self, event):
        print "leafletsFiveClick"
        
    def leafletsFourClick(self, event):
        print "leafletsFourClick"
        
    def leafletsOneClick(self, event):
        print "leafletsOneClick"
        
    def leafletsSevenClick(self, event):
        print "leafletsSevenClick"
        
    def leafletsThreeClick(self, event):
        print "leafletsThreeClick"
        
    def nextClick(self, event):
        print "nextClick"
        
    def petalColorMouseUp(self, event):
        print "petalColorMouseUp"
        
    def randomizePlantClick(self, event):
        print "randomizePlantClick"
        
    def sectionTdosDrawMouseMove(self, event):
        print "sectionTdosDrawMouseMove"
        
    def showFruitsNoClick(self, event):
        print "showFruitsNoClick"
        
    def showFruitsYesClick(self, event):
        print "showFruitsYesClick"
        
    def turnLeftClick(self, event):
        print "turnLeftClick"
        
    def turnRightClick(self, event):
        print "turnRightClick"
        
    def wizardNotebookPageChanged(self, event):
        print "wizardNotebookPageChanged"
        
if __name__ == "__main__":
    window = WizardWindow()
    window.visible = 1
    window.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE)
