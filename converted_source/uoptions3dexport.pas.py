# unit uoptions3dexport

from conversion_common import *
import uplant
import umain
import udomain
import udxfclr
import usupport
import updform
import u3dexport
import uturtle
import delphi_compatability

# const
kTransferLoad = 1
kTransferSave = 2

class TGeneric3DOptionsForm(PdForm):
    def __init__(self):
        self.drawWhichPlantsGroupBox = TGroupBox()
        self.useSelectedPlants = TRadioButton()
        self.useVisiblePlants = TRadioButton()
        self.useAllPlants = TRadioButton()
        self.otherGroupBox = TGroupBox()
        self.translatePlantsToWindowPositions = TCheckBox()
        self.dxfColorsGroupBox = TGroupBox()
        self.colorDXFFromRGB = TRadioButton()
        self.colorDXFFromOneColor = TRadioButton()
        self.wholePlantColor = TPanel()
        self.colorDXFFromPlantPartType = TRadioButton()
        self.colorsByPlantPart = TListBox()
        self.setPlantPartColor = TButton()
        self.povLimitsGroupBox = TGroupBox()
        self.Label4 = TLabel()
        self.Label5 = TLabel()
        self.minLineLengthToWrite = TEdit()
        self.minTdoScaleToWrite = TEdit()
        self.nestingGroupBox = TGroupBox()
        self.nestLeafAndPetiole = TCheckBox()
        self.nestCompoundLeaf = TCheckBox()
        self.nestInflorescence = TCheckBox()
        self.nestPedicelAndFlowerFruit = TCheckBox()
        self.nestFloralLayers = TCheckBox()
        self.commentOutUnionAtEnd = TCheckBox()
        self.layeringOption = TRadioGroup()
        self.writeColors = TCheckBox()
        self.Close = TButton()
        self.cancel = TButton()
        self.helpButton = TSpeedButton()
        self.threeDSWarningPanel = TPanel()
        self.Label6 = TLabel()
        self.plantNameAndCylinderSidesPanel = TPanel()
        self.Label2 = TLabel()
        self.Label3 = TLabel()
        self.stemCylinderFacesLabel = TLabel()
        self.sidesLabel = TLabel()
        self.lengthOfShortName = TSpinEdit()
        self.stemCylinderFaces = TSpinEdit()
        self.dxfWriteColors = TCheckBox()
        self.reorientGroupBox = TGroupBox()
        self.xRotationBeforeDraw = TSpinEdit()
        self.writePlantNumberInFrontOfName = TCheckBox()
        self.vrmlVersionRadioGroup = TRadioGroup()
        self.Label10 = TLabel()
        self.Label1 = TLabel()
        self.overallScalingFactor_pct = TSpinEdit()
        self.Label9 = TLabel()
        self.Label7 = TLabel()
        self.estimationStringGrid = TStringGrid()
        self.pressPlantsPanel = TPanel()
        self.pressPlants = TCheckBox()
        self.directionToPressPlants = TComboBox()
        self.Label8 = TLabel()
        self.makeTrianglesDoubleSided = TCheckBox()
        self.outputType = 0
        self.transferDirection = 0
        self.options = FileExport3DOptionsStructure()
        self.optionsChanged = false
        self.totalPlants = 0L
        self.totalParts = 0L
        self.totalPoints = 0L
        self.totalTriangles = 0L
        self.totalMaterials = 0L
    
    #$R *.DFM
    def FormActivate(self, Sender):
        # outputType must be set before this is called
        self.transferDirection = kTransferLoad
        if self.outputType == u3dexport.kDXF:
            self.fillPlantPartColors()
        self.transferFields()
        self.updatePredictedSizeDisplay()
    
    def CloseClick(self, Sender):
        if (self.useSelectedPlants.Checked) and (umain.MainForm.selectedPlants.Count <= 0):
            # do not let them complete action if no plants are selected
            MessageDialog("You chose \"selected\" for \"Draw which plants\", but no plants are selected." + chr(13) + "You should make another choice, or click Cancel and select some plants.", delphi_compatability.TMsgDlgType.mtError, [mbOK, ], 0)
            return
        if self.outputType == u3dexport.kLWO:
            if (self.totalPoints > u3dexport.kMax3DPoints) or (self.totalTriangles > u3dexport.kMax3DFaces):
                # do not let them complete action if too many points are selected - only for LWO which holds ALL
                # points and faces until the end of the file
                MessageDialog("You have selected too many points or triangles for this file format." + chr(13) + "A maximum of 65,536 points or triangles can be exported to one LWO file." + chr(13) + chr(13) + "You should make another choice of plants, or click Cancel and select fewer plants," + chr(13) + "or export to another format.", mtWarning, [mbOK, ], 0)
                return
        if self.outputType == u3dexport.kOBJ:
            if (self.totalPlants * (u3dexport.kExportPartLast + 1) > u3dexport.kMaxStoredMaterials):
                if MessageDialog("You have selected too many materials for this file format." + chr(13) + "The number of distinct colors will be bounded at " + IntToStr(u3dexport.kMaxStoredMaterials) + "." + chr(13) + "Some plants may refer to non-existent colors." + chr(13) + chr(13) + "To proceed anyway, click OK.", mtWarning, [mbOK, mbCancel, ], 0) == delphi_compatability.IDCANCEL:
                    # warn them if the colors list will be truncated
                    # limit of 1000 materials
                    return
        elif self.outputType == u3dexport.kLWO:
            if (self.totalPlants * (u3dexport.kExportPartLast + 1) > u3dexport.kMaxStoredMaterials):
                if MessageDialog("You have selected too many materials for this file format." + chr(13) + "The number of distinct colors will be bounded at " + IntToStr(u3dexport.kMaxStoredMaterials) + "." + chr(13) + "Some plants may refer to non-existent colors." + chr(13) + chr(13) + "To proceed anyway, click OK.", mtWarning, [mbOK, mbCancel, ], 0) == delphi_compatability.IDCANCEL:
                    # warn them if the colors list will be truncated
                    # limit of 1000 materials
                    return
        self.transferDirection = kTransferSave
        self.transferFields()
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def rearrangeItemsForOutputType(self):
        self.ClientHeight = self.otherGroupBox.Top + self.otherGroupBox.Height + 4
        self.ClientWidth = self.Close.Left + self.Close.Width + 4
        if self.outputType == u3dexport.kDXF:
            self.Caption = "Save DXF File"
            self.writeColors.Visible = false
            self.makeTrianglesDoubleSided.Top = self.writeColors.Top
            self.translatePlantsToWindowPositions.Top = self.makeTrianglesDoubleSided.Top + self.makeTrianglesDoubleSided.Height + 4
            self.otherGroupBox.Height = self.translatePlantsToWindowPositions.Top + self.translatePlantsToWindowPositions.Height + 6
            self.dxfColorsGroupBox.SetBounds(4, self.otherGroupBox.Top + self.otherGroupBox.Height + 4, self.dxfColorsGroupBox.Width, self.dxfColorsGroupBox.Height)
            self.dxfColorsGroupBox.Visible = true
            self.ClientHeight = self.dxfColorsGroupBox.Top + self.dxfColorsGroupBox.Height + 4
        elif self.outputType == u3dexport.kPOV:
            self.Caption = "Save POV Include (INC) File"
            self.plantNameAndCylinderSidesPanel.Visible = false
            self.writePlantNumberInFrontOfName.Visible = false
            self.pressPlantsPanel.Top = 16
            self.writeColors.Top = self.pressPlantsPanel.Top + self.pressPlantsPanel.Height
            self.makeTrianglesDoubleSided.Top = self.writeColors.Top + self.writeColors.Height + 4
            self.translatePlantsToWindowPositions.Top = self.makeTrianglesDoubleSided.Top + self.makeTrianglesDoubleSided.Height + 4
            self.otherGroupBox.Height = self.translatePlantsToWindowPositions.Top + self.translatePlantsToWindowPositions.Height + 6
            self.reorientGroupBox.SetBounds(4, self.drawWhichPlantsGroupBox.Top + self.drawWhichPlantsGroupBox.Height + 4, self.reorientGroupBox.Width, self.reorientGroupBox.Height)
            self.otherGroupBox.SetBounds(4, self.reorientGroupBox.Top + self.reorientGroupBox.Height + 4, self.otherGroupBox.Width, self.otherGroupBox.Height)
            self.povLimitsGroupBox.SetBounds(4, self.otherGroupBox.Top + self.otherGroupBox.Height + 4, self.povLimitsGroupBox.Width, self.povLimitsGroupBox.Height)
            self.povLimitsGroupBox.Visible = true
            self.nestingGroupBox.SetBounds(4, self.povLimitsGroupBox.Top + self.povLimitsGroupBox.Height + 4, self.nestingGroupBox.Width, self.nestingGroupBox.Height)
            self.nestingGroupBox.Visible = true
            self.ClientHeight = self.nestingGroupBox.Top + self.nestingGroupBox.Height + 4
            self.layeringOption.Visible = false
        elif self.outputType == u3dexport.k3DS:
            self.Caption = "Save 3DS File"
            self.threeDSWarningPanel.SetBounds(4, self.otherGroupBox.Top + self.otherGroupBox.Height + 4, self.threeDSWarningPanel.Width, self.threeDSWarningPanel.Height)
            self.threeDSWarningPanel.Visible = true
            self.ClientHeight = self.threeDSWarningPanel.Top + self.threeDSWarningPanel.Height + 4
        elif self.outputType == u3dexport.kOBJ:
            self.Caption = "Save WaveFront OBJ File (ASCII)"
        elif self.outputType == u3dexport.kVRML:
            self.Caption = "Save VRML File"
            self.layeringOption.Visible = false
            self.reorientGroupBox.SetBounds(4, self.drawWhichPlantsGroupBox.Top + self.drawWhichPlantsGroupBox.Height + 4, self.reorientGroupBox.Width, self.reorientGroupBox.Height)
            self.otherGroupBox.SetBounds(4, self.reorientGroupBox.Top + self.reorientGroupBox.Height + 4, self.otherGroupBox.Width, self.otherGroupBox.Height)
            self.vrmlVersionRadioGroup.SetBounds(4, self.otherGroupBox.Top + self.otherGroupBox.Height + 4, self.vrmlVersionRadioGroup.Width, self.vrmlVersionRadioGroup.Height)
            self.vrmlVersionRadioGroup.Visible = true
            self.nestingGroupBox.SetBounds(4, self.vrmlVersionRadioGroup.Top + self.vrmlVersionRadioGroup.Height + 4, self.nestingGroupBox.Width, self.nestingGroupBox.Height)
            self.commentOutUnionAtEnd.Visible = false
            self.nestingGroupBox.Height = self.nestInflorescence.Top + self.nestInflorescence.Height + 6
            self.nestingGroupBox.Visible = true
            self.ClientHeight = self.nestingGroupBox.Top + self.nestingGroupBox.Height + 4
        elif self.outputType == u3dexport.kLWO:
            self.Caption = "Save Lightwave LWO File"
    
    def transferFields(self):
        oldExportType = 0
        
        if self.transferDirection == kTransferLoad:
            if self.options.exportType == udomain.kIncludeSelectedPlants:
                # options that work for all types
                self.useSelectedPlants.Checked = true
            elif self.options.exportType == udomain.kIncludeVisiblePlants:
                self.useVisiblePlants.Checked = true
            elif self.options.exportType == udomain.kIncludeAllPlants:
                self.useAllPlants.Checked = true
        else:
            oldExportType = self.options.exportType
            if self.useSelectedPlants.Checked:
                self.options.exportType = udomain.kIncludeSelectedPlants
            elif self.useVisiblePlants.Checked:
                self.options.exportType = udomain.kIncludeVisiblePlants
            elif self.useAllPlants.Checked:
                self.options.exportType = udomain.kIncludeAllPlants
            if (oldExportType != self.options.exportType):
                self.optionsChanged = true
        self.options.layeringOption = self.transferRadioGroup(self.layeringOption, self.options.layeringOption)
        self.options.stemCylinderFaces = self.transferSmallintSpinEditBox(self.stemCylinderFaces, self.options.stemCylinderFaces)
        self.options.lengthOfShortName = self.transferSmallintSpinEditBox(self.lengthOfShortName, self.options.lengthOfShortName)
        self.options.xRotationBeforeDraw = self.transferSmallintSpinEditBox(self.xRotationBeforeDraw, self.options.xRotationBeforeDraw)
        self.options.translatePlantsToWindowPositions = self.transferCheckBox(self.translatePlantsToWindowPositions, self.options.translatePlantsToWindowPositions)
        self.options.writePlantNumberInFrontOfName = self.transferCheckBox(self.writePlantNumberInFrontOfName, self.options.writePlantNumberInFrontOfName)
        self.options.writeColors = self.transferCheckBox(self.writeColors, self.options.writeColors)
        self.options.overallScalingFactor_pct = self.transferSmallintSpinEditBox(self.overallScalingFactor_pct, self.options.overallScalingFactor_pct)
        self.options.pressPlants = self.transferCheckBox(self.pressPlants, self.options.pressPlants)
        self.options.directionToPressPlants = self.transferComboBox(self.directionToPressPlants, self.options.directionToPressPlants)
        self.options.makeTrianglesDoubleSided = self.transferCheckBox(self.makeTrianglesDoubleSided, self.options.makeTrianglesDoubleSided)
        # nothing yet
        if self.outputType == u3dexport.kDXF:
            # options for specific types
            # do after general one to override
            self.options.writeColors = self.transferCheckBox(self.dxfWriteColors, self.options.writeColors)
            if self.transferDirection == kTransferLoad:
                self.dxfWriteColorsClick(self)
            self.options.dxf_whereToGetColors = self.transferRadioButton(self.colorDXFFromRGB, self.options.dxf_whereToGetColors, u3dexport.kColorDXFFromRGB)
            self.options.dxf_whereToGetColors = self.transferRadioButton(self.colorDXFFromOneColor, self.options.dxf_whereToGetColors, u3dexport.kColorDXFFromOneColor)
            self.options.dxf_whereToGetColors = self.transferRadioButton(self.colorDXFFromPlantPartType, self.options.dxf_whereToGetColors, u3dexport.kColorDXFFromPlantPartType)
            self.wholePlantColor.Color = u3dexport.dxfColors[self.options.dxf_wholePlantColorIndex]
            if self.transferDirection == kTransferLoad:
                self.colorsByPlantPart.Invalidate()
        elif self.outputType == u3dexport.kPOV:
            self.options.pov_minLineLengthToWrite = self.transferSingleEditBox(self.minLineLengthToWrite, self.options.pov_minLineLengthToWrite)
            self.options.pov_minTdoScaleToWrite = self.transferSingleEditBox(self.minTdoScaleToWrite, self.options.pov_minTdoScaleToWrite)
            self.options.pov_commentOutUnionAtEnd = self.transferCheckBox(self.commentOutUnionAtEnd, self.options.pov_commentOutUnionAtEnd)
            self.options.nest_Inflorescence = self.transferCheckBox(self.nestInflorescence, self.options.nest_Inflorescence)
            self.options.nest_LeafAndPetiole = self.transferCheckBox(self.nestLeafAndPetiole, self.options.nest_LeafAndPetiole)
            self.options.nest_CompoundLeaf = self.transferCheckBox(self.nestCompoundLeaf, self.options.nest_CompoundLeaf)
            self.options.nest_PedicelAndFlowerFruit = self.transferCheckBox(self.nestPedicelAndFlowerFruit, self.options.nest_PedicelAndFlowerFruit)
            self.options.nest_FloralLayers = self.transferCheckBox(self.nestFloralLayers, self.options.nest_FloralLayers)
        elif self.outputType == u3dexport.k3DS:
            pass
            # nothing special
        elif self.outputType == u3dexport.kOBJ:
            pass
            # nothing special
        elif self.outputType == u3dexport.kVRML:
            self.options.nest_Inflorescence = self.transferCheckBox(self.nestInflorescence, self.options.nest_Inflorescence)
            self.options.nest_LeafAndPetiole = self.transferCheckBox(self.nestLeafAndPetiole, self.options.nest_LeafAndPetiole)
            self.options.nest_CompoundLeaf = self.transferCheckBox(self.nestCompoundLeaf, self.options.nest_CompoundLeaf)
            self.options.nest_PedicelAndFlowerFruit = self.transferCheckBox(self.nestPedicelAndFlowerFruit, self.options.nest_PedicelAndFlowerFruit)
            self.options.nest_FloralLayers = self.transferCheckBox(self.nestFloralLayers, self.options.nest_FloralLayers)
            self.options.vrml_version = self.transferRadioGroup(self.vrmlVersionRadioGroup, self.options.vrml_version)
        elif self.outputType == u3dexport.kLWO:
            pass
    
    def updatePredictedSizeDisplay(self):
        i = 0L
        plant = PdPlant()
        plantsString = ""
        estimatedBytes = 0L
        
        self.totalPlants = 0
        self.totalPoints = 0
        self.totalTriangles = 0
        self.totalParts = 0
        self.totalMaterials = 0
        if udomain.domain.plantManager.plants.Count > 0:
            for i in range(0, udomain.domain.plantManager.plants.Count):
                plant = uplant.PdPlant(udomain.domain.plantManager.plants.Items[i])
                if plant == None:
                    continue
                if (self.useSelectedPlants.Checked) and (not umain.MainForm.isSelected(plant)):
                    continue
                if (self.useVisiblePlants.Checked) and (plant.hidden):
                    continue
                plant.countPlantPartsFor3DOutput(self.outputType, StrToIntDef(self.stemCylinderFaces.Text, 20))
                self.totalPoints = self.totalPoints + plant.total3DExportPoints
                self.totalTriangles = self.totalTriangles + plant.total3DExportTriangles
                self.totalParts = self.totalParts + plant.totalPlantParts
                self.totalMaterials = self.totalMaterials + plant.total3DExportMaterials
                self.totalPlants += 1
        estimatedBytes = self.estimateBytes(udomain.domain.plantManager.plants.Count, self.totalParts, self.totalPoints, self.totalTriangles)
        # in MB
        self.options.fileSize = 1.0 * estimatedBytes / (1024 * 1024)
        self.estimationStringGrid.Cells[0, 0] = " plants"
        self.estimationStringGrid.Cells[0, 1] = " " + IntToStr(self.totalPlants)
        self.estimationStringGrid.ColWidths[0] = 36
        self.estimationStringGrid.Cells[1, 0] = " parts"
        self.estimationStringGrid.Cells[1, 1] = " " + IntToStr(self.totalParts)
        self.estimationStringGrid.ColWidths[1] = 36
        self.estimationStringGrid.Cells[2, 0] = " points"
        self.estimationStringGrid.Cells[2, 1] = " " + IntToStr(self.totalPoints)
        self.estimationStringGrid.ColWidths[2] = 44
        self.estimationStringGrid.Cells[3, 0] = " polygons"
        self.estimationStringGrid.Cells[3, 1] = " " + IntToStr(self.totalTriangles)
        # polygons is the longest word
        self.estimationStringGrid.ColWidths[3] = 50
        self.estimationStringGrid.Cells[4, 0] = " colors"
        self.estimationStringGrid.Cells[4, 1] = " " + IntToStr(self.totalMaterials)
        self.estimationStringGrid.Cells[5, 0] = " size"
        self.estimationStringGrid.ColWidths[5] = 64
        if self.options.fileSize > 1.0:
            self.estimationStringGrid.Cells[5, 1] = " " + FloatToStrF(self.options.fileSize, UNRESOLVED.ffFixed, 7, 2) + " MB"
        else:
            self.estimationStringGrid.Cells[5, 1] = " " + IntToStr(intround(self.options.fileSize * 1024)) + " K"
        self.translatePlantsToWindowPositions.Visible = (self.totalPlants > 1)
    
    def estimateBytes(self, numPlants, numParts, numPoints, numTriangles):
        result = 0L
        if self.outputType == u3dexport.kDXF:
            result = numPoints * 250
        elif self.outputType == u3dexport.kPOV:
            result = numPlants * 25 + numParts * 25 + numTriangles * 150
        elif self.outputType == u3dexport.k3DS:
            result = numPlants * 48 + numParts * 48 + numPoints * 24 + numTriangles * 24
        elif self.outputType == u3dexport.kOBJ:
            result = numPlants * 100 + numParts * 100 + numPoints * 50 + numTriangles * 50
        elif self.outputType == u3dexport.kVRML:
            result = numPlants * 100 + numParts * 100 + numPoints * 80 + numTriangles * 80
        elif self.outputType == u3dexport.kLWO:
            result = numPlants * 600 + numParts * 100 + numPoints * 20 + numTriangles * 20
        else :
            raise GeneralException.create("Problem: Invalid 3d export type for size estimation.")
        return result
    
    def fillPlantPartColors(self):
        i = 0
        firstPlant = PdPlant()
        
        self.colorsByPlantPart.Clear()
        if (udomain.domain == None) or (udomain.domain.plantManager == None) or (udomain.domain.plantManager.plants.Count < 0):
            # use first plant to get DXF part type names - there must be at least one plant to bring up this form
            return
        firstPlant = uplant.PdPlant(udomain.domain.plantManager.plants[0])
        if firstPlant == None:
            return
        for i in range(0, u3dexport.kExportPartLast + 1):
            self.colorsByPlantPart.Items.Add(u3dexport.longNameForDXFPartType(i))
    
    def colorsByPlantPartDrawItem(self, Control, index, Rect, State):
        selected = false
        colorRect = TRect()
        remainderRect = TRect()
        cText = [0] * (range(0, 255 + 1) + 1)
        
        if delphi_compatability.Application.terminated:
            return
        if (self.colorsByPlantPart.Items.Count <= 0) or (index < 0) or (index > self.colorsByPlantPart.Items.Count - 1):
            return
        selected = (delphi_compatability.TOwnerDrawStateType.odSelected in State)
        # set up rectangles 
        colorRect = Rect
        colorRect.Right = colorRect.Left + self.colorsByPlantPart.ItemHeight
        remainderRect = Rect
        remainderRect.Left = remainderRect.Left + self.colorsByPlantPart.ItemHeight
        # fill first box with white, rest with clHighlight if selected 
        self.colorsByPlantPart.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        self.colorsByPlantPart.Canvas.Brush.Color = u3dexport.dxfColors[self.options.dxf_plantPartColorIndexes[index]]
        self.colorsByPlantPart.Canvas.FillRect(colorRect)
        self.colorsByPlantPart.Canvas.Font = self.colorsByPlantPart.Font
        if selected:
            self.colorsByPlantPart.Canvas.Brush.Color = UNRESOLVED.clHighlight
            self.colorsByPlantPart.Canvas.Font.Color = UNRESOLVED.clHighlightText
        else:
            self.colorsByPlantPart.Canvas.Brush.Color = delphi_compatability.clWindow
            self.colorsByPlantPart.Canvas.Font.Color = UNRESOLVED.clBtnText
        self.colorsByPlantPart.Canvas.FillRect(remainderRect)
        UNRESOLVED.strPCopy(cText, self.colorsByPlantPart.Items[index])
        # margin for text 
        remainderRect.Left = remainderRect.Left + 5
        UNRESOLVED.winprocs.drawText(self.colorsByPlantPart.Canvas.Handle, cText, len(cText), remainderRect, delphi_compatability.DT_LEFT)
    
    def wholePlantColorMouseUp(self, Sender, Button, Shift, X, Y):
        colorForm = TChooseDXFColorForm()
        response = 0
        
        colorForm = udxfclr.TChooseDXFColorForm().create(self)
        if colorForm == None:
            raise GeneralException.create("Problem: Could not create color window.")
        try:
            colorForm.colorIndex = self.options.dxf_wholePlantColorIndex
            response = colorForm.ShowModal()
            if response == mrOK:
                self.options.dxf_wholePlantColorIndex = colorForm.colorIndex
                self.wholePlantColor.Color = u3dexport.dxfColors[self.options.dxf_wholePlantColorIndex]
                self.wholePlantColor.Invalidate()
                self.optionsChanged = true
        finally:
            colorForm.free
            colorForm = None
    
    def setPlantPartColorClick(self, Sender):
        colorForm = TChooseDXFColorForm()
        response = 0
        firstColorIndex = TColorRef()
        i = 0
        
        firstColorIndex = -1
        if self.colorsByPlantPart.Items.Count > 0:
            for i in range(0, self.colorsByPlantPart.Items.Count):
                if self.colorsByPlantPart.Selected[i]:
                    if firstColorIndex == -1:
                        firstColorIndex = self.options.dxf_plantPartColorIndexes[i]
        if firstColorIndex < 0:
            return
        colorForm = udxfclr.TChooseDXFColorForm().create(self)
        if colorForm == None:
            raise GeneralException.create("Problem: Could not create color window.")
        try:
            colorForm.colorIndex = firstColorIndex
            response = colorForm.ShowModal()
            if response == mrOK:
                if self.colorsByPlantPart.Items.Count > 0:
                    for i in range(0, self.colorsByPlantPart.Items.Count):
                        if self.colorsByPlantPart.Selected[i]:
                            self.options.dxf_plantPartColorIndexes[i] = colorForm.colorIndex
                self.colorsByPlantPart.Invalidate()
                self.optionsChanged = true
        finally:
            colorForm.free
            colorForm = None
    
    def colorsByPlantPartDblClick(self, Sender):
        self.setPlantPartColorClick(self)
    
    def transferRadioButton(self, radioButton, value, radioIndex):
        if self.transferDirection == kTransferLoad:
            if value == radioIndex:
                radioButton.Checked = true
        elif self.transferDirection == kTransferSave:
            if (radioButton.Checked) and (value != radioIndex):
                self.optionsChanged = true
            if radioButton.Checked:
                value = radioIndex
        return value
    
    def transferCheckBox(self, checkBox, value):
        if self.transferDirection == kTransferLoad:
            checkBox.Checked = value
        elif self.transferDirection == kTransferSave:
            if value != checkBox.Checked:
                self.optionsChanged = true
            value = checkBox.Checked
        return value
    
    def transferColor(self, colorPanel, value):
        raise "method transferColor had assigned to var parameter value not added to return; fixup manually"
        if self.transferDirection == kTransferLoad:
            colorPanel.Color = value
        elif self.transferDirection == kTransferSave:
            if value != colorPanel.Color:
                self.optionsChanged = true
            value = colorPanel.Color
    
    def transferSmallintSpinEditBox(self, editBox, value):
        if self.transferDirection == kTransferLoad:
            editBox.Text = IntToStr(value)
        elif self.transferDirection == kTransferSave:
            if value != StrToIntDef(editBox.Text, 0):
                self.optionsChanged = true
            value = StrToIntDef(editBox.Text, 0)
        return value
    
    def transferRadioGroup(self, radioGroup, value):
        if self.transferDirection == kTransferLoad:
            radioGroup.ItemIndex = value
        elif self.transferDirection == kTransferSave:
            if value != radioGroup.ItemIndex:
                self.optionsChanged = true
            value = radioGroup.ItemIndex
        return value
    
    def transferComboBox(self, comboBox, value):
        if self.transferDirection == kTransferLoad:
            comboBox.ItemIndex = value
        elif self.transferDirection == kTransferSave:
            if value != comboBox.ItemIndex:
                self.optionsChanged = true
            value = comboBox.ItemIndex
        return value
    
    def transferSingleEditBox(self, editBox, value):
        newValue = 0.0
        
        if self.transferDirection == kTransferLoad:
            editBox.Text = usupport.valueString(value)
        elif self.transferDirection == kTransferSave:
            try:
                newValue = StrToFloat(editBox.Text)
            except:
                newValue = value
            if newValue != value:
                self.optionsChanged = true
            value = newValue
        return value
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Exporting_3D_models_in_general")
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
    def useSelectedPlantsClick(self, Sender):
        self.updatePredictedSizeDisplay()
    
    def useVisiblePlantsClick(self, Sender):
        self.updatePredictedSizeDisplay()
    
    def useAllPlantsClick(self, Sender):
        self.updatePredictedSizeDisplay()
    
    def stemCylinderFacesChange(self, Sender):
        value = 0
        
        value = StrToIntDef(self.stemCylinderFaces.Text, 5)
        if value < udomain.kMinOutputCylinderFaces:
            value = udomain.kMinOutputCylinderFaces
        if value > udomain.kMaxOutputCylinderFaces:
            value = udomain.kMaxOutputCylinderFaces
        self.stemCylinderFaces.Text = IntToStr(value)
        self.updatePredictedSizeDisplay()
    
    def dxfWriteColorsClick(self, Sender):
        self.colorDXFFromRGB.Visible = self.dxfWriteColors.Checked
        self.colorDXFFromOneColor.Visible = self.dxfWriteColors.Checked
        self.wholePlantColor.Visible = self.dxfWriteColors.Checked
        self.colorDXFFromPlantPartType.Visible = self.dxfWriteColors.Checked
        self.colorsByPlantPart.Visible = self.dxfWriteColors.Checked
        self.setPlantPartColor.Visible = self.dxfWriteColors.Checked
    
