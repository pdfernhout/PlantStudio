// unit uoptions3dexport

from conversion_common import *;
import udxfclr;
import updform;
import delphi_compatability;

// const
kTransferLoad = 1;
kTransferSave = 2;



class TGeneric3DOptionsForm extends PdForm {
    public TGroupBox drawWhichPlantsGroupBox;
    public TRadioButton useSelectedPlants;
    public TRadioButton useVisiblePlants;
    public TRadioButton useAllPlants;
    public TGroupBox otherGroupBox;
    public TCheckBox translatePlantsToWindowPositions;
    public TGroupBox dxfColorsGroupBox;
    public TRadioButton colorDXFFromRGB;
    public TRadioButton colorDXFFromOneColor;
    public TPanel wholePlantColor;
    public TRadioButton colorDXFFromPlantPartType;
    public TListBox colorsByPlantPart;
    public TButton setPlantPartColor;
    public TGroupBox povLimitsGroupBox;
    public TLabel Label4;
    public TLabel Label5;
    public TEdit minLineLengthToWrite;
    public TEdit minTdoScaleToWrite;
    public TGroupBox nestingGroupBox;
    public TCheckBox nestLeafAndPetiole;
    public TCheckBox nestCompoundLeaf;
    public TCheckBox nestInflorescence;
    public TCheckBox nestPedicelAndFlowerFruit;
    public TCheckBox nestFloralLayers;
    public TCheckBox commentOutUnionAtEnd;
    public TRadioGroup layeringOption;
    public TCheckBox writeColors;
    public TButton Close;
    public TButton cancel;
    public TSpeedButton helpButton;
    public TPanel threeDSWarningPanel;
    public TLabel Label6;
    public TPanel plantNameAndCylinderSidesPanel;
    public TLabel Label2;
    public TLabel Label3;
    public TLabel stemCylinderFacesLabel;
    public TLabel sidesLabel;
    public TSpinEdit lengthOfShortName;
    public TSpinEdit stemCylinderFaces;
    public TCheckBox dxfWriteColors;
    public TGroupBox reorientGroupBox;
    public TSpinEdit xRotationBeforeDraw;
    public TCheckBox writePlantNumberInFrontOfName;
    public TRadioGroup vrmlVersionRadioGroup;
    public TLabel Label10;
    public TLabel Label1;
    public TSpinEdit overallScalingFactor_pct;
    public TLabel Label9;
    public TLabel Label7;
    public TStringGrid estimationStringGrid;
    public TPanel pressPlantsPanel;
    public TCheckBox pressPlants;
    public TComboBox directionToPressPlants;
    public TLabel Label8;
    public TCheckBox makeTrianglesDoubleSided;
    public short outputType;
    public short transferDirection;
    public FileExport3DOptionsStructure options;
    public boolean optionsChanged;
    public long totalPlants;
    public long totalParts;
    public long totalPoints;
    public long totalTriangles;
    public long totalMaterials;
    
    //$R *.DFM
    public void FormActivate(TObject Sender) {
        // outputType must be set before this is called
        this.transferDirection = kTransferLoad;
        if (this.outputType == UNRESOLVED.kDXF) {
            this.fillPlantPartColors();
        }
        this.transferFields();
        this.updatePredictedSizeDisplay();
    }
    
    public void CloseClick(TObject Sender) {
        if ((this.useSelectedPlants.Checked) && (UNRESOLVED.MainForm.selectedPlants.count <= 0)) {
            // do not let them complete action if no plants are selected
            MessageDialog("You chose \"selected\" for \"Draw which plants\", but no plants are selected." + chr(13) + "You should make another choice, or click Cancel and select some plants.", delphi_compatability.TMsgDlgType.mtError, {mbOK, }, 0);
            return;
        }
        if (this.outputType == UNRESOLVED.kLWO) {
            if ((this.totalPoints > UNRESOLVED.kMax3DPoints) || (this.totalTriangles > UNRESOLVED.kMax3DFaces)) {
                // do not let them complete action if too many points are selected - only for LWO which holds ALL
                // points and faces until the end of the file
                MessageDialog("You have selected too many points or triangles for this file format." + chr(13) + "A maximum of 65,536 points or triangles can be exported to one LWO file." + chr(13) + chr(13) + "You should make another choice of plants, or click Cancel and select fewer plants," + chr(13) + "or export to another format.", mtWarning, {mbOK, }, 0);
                return;
            }
        }
        switch (this.outputType) {
            case UNRESOLVED.kOBJ:
                if ((this.totalPlants * (UNRESOLVED.kExportPartLast + 1) > UNRESOLVED.kMaxStoredMaterials)) {
                    if (MessageDialog("You have selected too many materials for this file format." + chr(13) + "The number of distinct colors will be bounded at " + IntToStr(UNRESOLVED.kMaxStoredMaterials) + "." + chr(13) + "Some plants may refer to non-existent colors." + chr(13) + chr(13) + "To proceed anyway, click OK.", mtWarning, {mbOK, mbCancel, }, 0) == delphi_compatability.IDCANCEL) {
                        // warn them if the colors list will be truncated
                        // limit of 1000 materials
                        return;
                    }
                }
                break;
            case UNRESOLVED.kLWO:
                if ((this.totalPlants * (UNRESOLVED.kExportPartLast + 1) > UNRESOLVED.kMaxStoredMaterials)) {
                    if (MessageDialog("You have selected too many materials for this file format." + chr(13) + "The number of distinct colors will be bounded at " + IntToStr(UNRESOLVED.kMaxStoredMaterials) + "." + chr(13) + "Some plants may refer to non-existent colors." + chr(13) + chr(13) + "To proceed anyway, click OK.", mtWarning, {mbOK, mbCancel, }, 0) == delphi_compatability.IDCANCEL) {
                        // warn them if the colors list will be truncated
                        // limit of 1000 materials
                        return;
                    }
                }
                break;
        this.transferDirection = kTransferSave;
        this.transferFields();
        this.ModalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    public void rearrangeItemsForOutputType() {
        this.ClientHeight = this.otherGroupBox.Top + this.otherGroupBox.Height + 4;
        this.ClientWidth = this.Close.Left + this.Close.Width + 4;
        switch (this.outputType) {
            case UNRESOLVED.kDXF:
                this.Caption = "Save DXF File";
                this.writeColors.Visible = false;
                this.makeTrianglesDoubleSided.Top = this.writeColors.Top;
                this.translatePlantsToWindowPositions.Top = this.makeTrianglesDoubleSided.Top + this.makeTrianglesDoubleSided.Height + 4;
                this.otherGroupBox.Height = this.translatePlantsToWindowPositions.Top + this.translatePlantsToWindowPositions.Height + 6;
                this.dxfColorsGroupBox.SetBounds(4, this.otherGroupBox.Top + this.otherGroupBox.Height + 4, this.dxfColorsGroupBox.Width, this.dxfColorsGroupBox.Height);
                this.dxfColorsGroupBox.Visible = true;
                this.ClientHeight = this.dxfColorsGroupBox.Top + this.dxfColorsGroupBox.Height + 4;
                break;
            case UNRESOLVED.kPOV:
                this.Caption = "Save POV Include (INC) File";
                this.plantNameAndCylinderSidesPanel.Visible = false;
                this.writePlantNumberInFrontOfName.Visible = false;
                this.pressPlantsPanel.Top = 16;
                this.writeColors.Top = this.pressPlantsPanel.Top + this.pressPlantsPanel.Height;
                this.makeTrianglesDoubleSided.Top = this.writeColors.Top + this.writeColors.Height + 4;
                this.translatePlantsToWindowPositions.Top = this.makeTrianglesDoubleSided.Top + this.makeTrianglesDoubleSided.Height + 4;
                this.otherGroupBox.Height = this.translatePlantsToWindowPositions.Top + this.translatePlantsToWindowPositions.Height + 6;
                this.reorientGroupBox.SetBounds(4, this.drawWhichPlantsGroupBox.Top + this.drawWhichPlantsGroupBox.Height + 4, this.reorientGroupBox.Width, this.reorientGroupBox.Height);
                this.otherGroupBox.SetBounds(4, this.reorientGroupBox.Top + this.reorientGroupBox.Height + 4, this.otherGroupBox.Width, this.otherGroupBox.Height);
                this.povLimitsGroupBox.SetBounds(4, this.otherGroupBox.Top + this.otherGroupBox.Height + 4, this.povLimitsGroupBox.Width, this.povLimitsGroupBox.Height);
                this.povLimitsGroupBox.Visible = true;
                this.nestingGroupBox.SetBounds(4, this.povLimitsGroupBox.Top + this.povLimitsGroupBox.Height + 4, this.nestingGroupBox.Width, this.nestingGroupBox.Height);
                this.nestingGroupBox.Visible = true;
                this.ClientHeight = this.nestingGroupBox.Top + this.nestingGroupBox.Height + 4;
                this.layeringOption.Visible = false;
                break;
            case UNRESOLVED.k3DS:
                this.Caption = "Save 3DS File";
                this.threeDSWarningPanel.SetBounds(4, this.otherGroupBox.Top + this.otherGroupBox.Height + 4, this.threeDSWarningPanel.Width, this.threeDSWarningPanel.Height);
                this.threeDSWarningPanel.Visible = true;
                this.ClientHeight = this.threeDSWarningPanel.Top + this.threeDSWarningPanel.Height + 4;
                break;
            case UNRESOLVED.kOBJ:
                this.Caption = "Save WaveFront OBJ File (ASCII)";
                break;
            case UNRESOLVED.kVRML:
                this.Caption = "Save VRML File";
                this.layeringOption.Visible = false;
                this.reorientGroupBox.SetBounds(4, this.drawWhichPlantsGroupBox.Top + this.drawWhichPlantsGroupBox.Height + 4, this.reorientGroupBox.Width, this.reorientGroupBox.Height);
                this.otherGroupBox.SetBounds(4, this.reorientGroupBox.Top + this.reorientGroupBox.Height + 4, this.otherGroupBox.Width, this.otherGroupBox.Height);
                this.vrmlVersionRadioGroup.SetBounds(4, this.otherGroupBox.Top + this.otherGroupBox.Height + 4, this.vrmlVersionRadioGroup.Width, this.vrmlVersionRadioGroup.Height);
                this.vrmlVersionRadioGroup.Visible = true;
                this.nestingGroupBox.SetBounds(4, this.vrmlVersionRadioGroup.Top + this.vrmlVersionRadioGroup.Height + 4, this.nestingGroupBox.Width, this.nestingGroupBox.Height);
                this.commentOutUnionAtEnd.Visible = false;
                this.nestingGroupBox.Height = this.nestInflorescence.Top + this.nestInflorescence.Height + 6;
                this.nestingGroupBox.Visible = true;
                this.ClientHeight = this.nestingGroupBox.Top + this.nestingGroupBox.Height + 4;
                break;
            case UNRESOLVED.kLWO:
                this.Caption = "Save Lightwave LWO File";
                break;
    }
    
    public void transferFields() {
        short oldExportType = 0;
        
        if (this.transferDirection == kTransferLoad) {
            switch (this.options.exportType) {
                case UNRESOLVED.kIncludeSelectedPlants:
                    // options that work for all types
                    this.useSelectedPlants.Checked = true;
                    break;
                case UNRESOLVED.kIncludeVisiblePlants:
                    this.useVisiblePlants.Checked = true;
                    break;
                case UNRESOLVED.kIncludeAllPlants:
                    this.useAllPlants.Checked = true;
                    break;
        } else {
            oldExportType = this.options.exportType;
            if (this.useSelectedPlants.Checked) {
                this.options.exportType = UNRESOLVED.kIncludeSelectedPlants;
            } else if (this.useVisiblePlants.Checked) {
                this.options.exportType = UNRESOLVED.kIncludeVisiblePlants;
            } else if (this.useAllPlants.Checked) {
                this.options.exportType = UNRESOLVED.kIncludeAllPlants;
            }
            if ((oldExportType != this.options.exportType)) {
                this.optionsChanged = true;
            }
        }
        this.options.layeringOption = this.transferRadioGroup(this.layeringOption, this.options.layeringOption);
        this.options.stemCylinderFaces = this.transferSmallintSpinEditBox(this.stemCylinderFaces, this.options.stemCylinderFaces);
        this.options.lengthOfShortName = this.transferSmallintSpinEditBox(this.lengthOfShortName, this.options.lengthOfShortName);
        this.options.xRotationBeforeDraw = this.transferSmallintSpinEditBox(this.xRotationBeforeDraw, this.options.xRotationBeforeDraw);
        this.options.translatePlantsToWindowPositions = this.transferCheckBox(this.translatePlantsToWindowPositions, this.options.translatePlantsToWindowPositions);
        this.options.writePlantNumberInFrontOfName = this.transferCheckBox(this.writePlantNumberInFrontOfName, this.options.writePlantNumberInFrontOfName);
        this.options.writeColors = this.transferCheckBox(this.writeColors, this.options.writeColors);
        this.options.overallScalingFactor_pct = this.transferSmallintSpinEditBox(this.overallScalingFactor_pct, this.options.overallScalingFactor_pct);
        this.options.pressPlants = this.transferCheckBox(this.pressPlants, this.options.pressPlants);
        this.options.directionToPressPlants = this.transferComboBox(this.directionToPressPlants, this.options.directionToPressPlants);
        this.options.makeTrianglesDoubleSided = this.transferCheckBox(this.makeTrianglesDoubleSided, this.options.makeTrianglesDoubleSided);
        // nothing yet
        switch (this.outputType) {
            case UNRESOLVED.kDXF:
                // options for specific types
                // do after general one to override
                this.options.writeColors = this.transferCheckBox(this.dxfWriteColors, this.options.writeColors);
                if (this.transferDirection == kTransferLoad) {
                    this.dxfWriteColorsClick(this);
                }
                this.options.dxf_whereToGetColors = this.transferRadioButton(this.colorDXFFromRGB, this.options.dxf_whereToGetColors, UNRESOLVED.kColorDXFFromRGB);
                this.options.dxf_whereToGetColors = this.transferRadioButton(this.colorDXFFromOneColor, this.options.dxf_whereToGetColors, UNRESOLVED.kColorDXFFromOneColor);
                this.options.dxf_whereToGetColors = this.transferRadioButton(this.colorDXFFromPlantPartType, this.options.dxf_whereToGetColors, UNRESOLVED.kColorDXFFromPlantPartType);
                this.wholePlantColor.Color = UNRESOLVED.dxfColors[this.options.dxf_wholePlantColorIndex];
                if (this.transferDirection == kTransferLoad) {
                    this.colorsByPlantPart.Invalidate();
                }
                break;
            case UNRESOLVED.kPOV:
                this.options.pov_minLineLengthToWrite = this.transferSingleEditBox(this.minLineLengthToWrite, this.options.pov_minLineLengthToWrite);
                this.options.pov_minTdoScaleToWrite = this.transferSingleEditBox(this.minTdoScaleToWrite, this.options.pov_minTdoScaleToWrite);
                this.options.pov_commentOutUnionAtEnd = this.transferCheckBox(this.commentOutUnionAtEnd, this.options.pov_commentOutUnionAtEnd);
                this.options.nest_Inflorescence = this.transferCheckBox(this.nestInflorescence, this.options.nest_Inflorescence);
                this.options.nest_LeafAndPetiole = this.transferCheckBox(this.nestLeafAndPetiole, this.options.nest_LeafAndPetiole);
                this.options.nest_CompoundLeaf = this.transferCheckBox(this.nestCompoundLeaf, this.options.nest_CompoundLeaf);
                this.options.nest_PedicelAndFlowerFruit = this.transferCheckBox(this.nestPedicelAndFlowerFruit, this.options.nest_PedicelAndFlowerFruit);
                this.options.nest_FloralLayers = this.transferCheckBox(this.nestFloralLayers, this.options.nest_FloralLayers);
                break;
            case UNRESOLVED.k3DS:
                pass
                // nothing special
                break;
            case UNRESOLVED.kOBJ:
                pass
                // nothing special
                break;
            case UNRESOLVED.kVRML:
                this.options.nest_Inflorescence = this.transferCheckBox(this.nestInflorescence, this.options.nest_Inflorescence);
                this.options.nest_LeafAndPetiole = this.transferCheckBox(this.nestLeafAndPetiole, this.options.nest_LeafAndPetiole);
                this.options.nest_CompoundLeaf = this.transferCheckBox(this.nestCompoundLeaf, this.options.nest_CompoundLeaf);
                this.options.nest_PedicelAndFlowerFruit = this.transferCheckBox(this.nestPedicelAndFlowerFruit, this.options.nest_PedicelAndFlowerFruit);
                this.options.nest_FloralLayers = this.transferCheckBox(this.nestFloralLayers, this.options.nest_FloralLayers);
                this.options.vrml_version = this.transferRadioGroup(this.vrmlVersionRadioGroup, this.options.vrml_version);
                break;
            case UNRESOLVED.kLWO:
                break;
    }
    
    public void updatePredictedSizeDisplay() {
        long i = 0;
        PdPlant plant = new PdPlant();
        String plantsString = "";
        long estimatedBytes = 0;
        
        this.totalPlants = 0;
        this.totalPoints = 0;
        this.totalTriangles = 0;
        this.totalParts = 0;
        this.totalMaterials = 0;
        if (UNRESOLVED.domain.plantManager.plants.count > 0) {
            for (i = 0; i <= UNRESOLVED.domain.plantManager.plants.count - 1; i++) {
                plant = UNRESOLVED.PdPlant(UNRESOLVED.domain.plantManager.plants.items[i]);
                if (plant == null) {
                    continue;
                }
                if ((this.useSelectedPlants.Checked) && (!UNRESOLVED.MainForm.isSelected(plant))) {
                    continue;
                }
                if ((this.useVisiblePlants.Checked) && (plant.hidden)) {
                    continue;
                }
                plant.countPlantPartsFor3DOutput(this.outputType, StrToIntDef(this.stemCylinderFaces.Text, 20));
                this.totalPoints = this.totalPoints + plant.total3DExportPoints;
                this.totalTriangles = this.totalTriangles + plant.total3DExportTriangles;
                this.totalParts = this.totalParts + plant.totalPlantParts;
                this.totalMaterials = this.totalMaterials + plant.total3DExportMaterials;
                this.totalPlants += 1;
            }
        }
        estimatedBytes = this.estimateBytes(UNRESOLVED.domain.plantManager.plants.count, this.totalParts, this.totalPoints, this.totalTriangles);
        // in MB
        this.options.fileSize = 1.0 * estimatedBytes / (1024 * 1024);
        this.estimationStringGrid.Cells[0, 0] = " plants";
        this.estimationStringGrid.Cells[0, 1] = " " + IntToStr(this.totalPlants);
        this.estimationStringGrid.ColWidths[0] = 36;
        this.estimationStringGrid.Cells[1, 0] = " parts";
        this.estimationStringGrid.Cells[1, 1] = " " + IntToStr(this.totalParts);
        this.estimationStringGrid.ColWidths[1] = 36;
        this.estimationStringGrid.Cells[2, 0] = " points";
        this.estimationStringGrid.Cells[2, 1] = " " + IntToStr(this.totalPoints);
        this.estimationStringGrid.ColWidths[2] = 44;
        this.estimationStringGrid.Cells[3, 0] = " polygons";
        this.estimationStringGrid.Cells[3, 1] = " " + IntToStr(this.totalTriangles);
        // polygons is the longest word
        this.estimationStringGrid.ColWidths[3] = 50;
        this.estimationStringGrid.Cells[4, 0] = " colors";
        this.estimationStringGrid.Cells[4, 1] = " " + IntToStr(this.totalMaterials);
        this.estimationStringGrid.Cells[5, 0] = " size";
        this.estimationStringGrid.ColWidths[5] = 64;
        if (this.options.fileSize > 1.0) {
            this.estimationStringGrid.Cells[5, 1] = " " + FloatToStrF(this.options.fileSize, UNRESOLVED.ffFixed, 7, 2) + " MB";
        } else {
            this.estimationStringGrid.Cells[5, 1] = " " + IntToStr(intround(this.options.fileSize * 1024)) + " K";
        }
        this.translatePlantsToWindowPositions.Visible = (this.totalPlants > 1);
    }
    
    public long estimateBytes(long numPlants, long numParts, long numPoints, long numTriangles) {
        result = 0;
        switch (this.outputType) {
            case UNRESOLVED.kDXF:
                result = numPoints * 250;
                break;
            case UNRESOLVED.kPOV:
                result = numPlants * 25 + numParts * 25 + numTriangles * 150;
                break;
            case UNRESOLVED.k3DS:
                result = numPlants * 48 + numParts * 48 + numPoints * 24 + numTriangles * 24;
                break;
            case UNRESOLVED.kOBJ:
                result = numPlants * 100 + numParts * 100 + numPoints * 50 + numTriangles * 50;
                break;
            case UNRESOLVED.kVRML:
                result = numPlants * 100 + numParts * 100 + numPoints * 80 + numTriangles * 80;
                break;
            case UNRESOLVED.kLWO:
                result = numPlants * 600 + numParts * 100 + numPoints * 20 + numTriangles * 20;
                break;
            default:
                throw new GeneralException.create("Problem: Invalid 3d export type for size estimation.");
                break;
        return result;
    }
    
    public void fillPlantPartColors() {
        short i = 0;
        PdPlant firstPlant = new PdPlant();
        
        this.colorsByPlantPart.Clear();
        if ((UNRESOLVED.domain == null) || (UNRESOLVED.domain.plantManager == null) || (UNRESOLVED.domain.plantManager.plants.count < 0)) {
            // use first plant to get DXF part type names - there must be at least one plant to bring up this form
            return;
        }
        firstPlant = UNRESOLVED.PdPlant(UNRESOLVED.domain.plantManager.plants[0]);
        if (firstPlant == null) {
            return;
        }
        for (i = 0; i <= UNRESOLVED.kExportPartLast; i++) {
            this.colorsByPlantPart.Items.Add(UNRESOLVED.longNameForDXFPartType(i));
        }
    }
    
    public void colorsByPlantPartDrawItem(TWinControl Control, int index, TRect Rect, TOwnerDrawState State) {
        boolean selected = false;
        TRect colorRect = new TRect();
        TRect remainderRect = new TRect();
         cText = [0] * (range(0, 255 + 1) + 1);
        
        if (delphi_compatability.Application.terminated) {
            return;
        }
        if ((this.colorsByPlantPart.Items.Count <= 0) || (index < 0) || (index > this.colorsByPlantPart.Items.Count - 1)) {
            return;
        }
        selected = (delphi_compatability.TOwnerDrawStateType.odSelected in State);
        // set up rectangles 
        colorRect = Rect;
        colorRect.Right = colorRect.Left + this.colorsByPlantPart.ItemHeight;
        remainderRect = Rect;
        remainderRect.Left = remainderRect.Left + this.colorsByPlantPart.ItemHeight;
        // fill first box with white, rest with clHighlight if selected 
        this.colorsByPlantPart.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        this.colorsByPlantPart.Canvas.Brush.Color = UNRESOLVED.dxfColors[this.options.dxf_plantPartColorIndexes[index]];
        this.colorsByPlantPart.Canvas.FillRect(colorRect);
        this.colorsByPlantPart.Canvas.Font = this.colorsByPlantPart.Font;
        if (selected) {
            this.colorsByPlantPart.Canvas.Brush.Color = UNRESOLVED.clHighlight;
            this.colorsByPlantPart.Canvas.Font.Color = UNRESOLVED.clHighlightText;
        } else {
            this.colorsByPlantPart.Canvas.Brush.Color = delphi_compatability.clWindow;
            this.colorsByPlantPart.Canvas.Font.Color = UNRESOLVED.clBtnText;
        }
        this.colorsByPlantPart.Canvas.FillRect(remainderRect);
        UNRESOLVED.strPCopy(cText, this.colorsByPlantPart.Items[index]);
        // margin for text 
        remainderRect.Left = remainderRect.Left + 5;
        UNRESOLVED.winprocs.drawText(this.colorsByPlantPart.Canvas.Handle, cText, len(cText), remainderRect, delphi_compatability.DT_LEFT);
    }
    
    public void wholePlantColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        TChooseDXFColorForm colorForm = new TChooseDXFColorForm();
        int response = 0;
        
        colorForm = udxfclr.TChooseDXFColorForm().create(this);
        if (colorForm == null) {
            throw new GeneralException.create("Problem: Could not create color window.");
        }
        try {
            colorForm.colorIndex = this.options.dxf_wholePlantColorIndex;
            response = colorForm.ShowModal();
            if (response == mrOK) {
                this.options.dxf_wholePlantColorIndex = colorForm.colorIndex;
                this.wholePlantColor.Color = UNRESOLVED.dxfColors[this.options.dxf_wholePlantColorIndex];
                this.wholePlantColor.Invalidate();
                this.optionsChanged = true;
            }
        } finally {
            colorForm.free;
            colorForm = null;
        }
    }
    
    public void setPlantPartColorClick(TObject Sender) {
        TChooseDXFColorForm colorForm = new TChooseDXFColorForm();
        int response = 0;
        TColorRef firstColorIndex = new TColorRef();
        short i = 0;
        
        firstColorIndex = -1;
        if (this.colorsByPlantPart.Items.Count > 0) {
            for (i = 0; i <= this.colorsByPlantPart.Items.Count - 1; i++) {
                if (this.colorsByPlantPart.Selected[i]) {
                    if (firstColorIndex == -1) {
                        firstColorIndex = this.options.dxf_plantPartColorIndexes[i];
                    }
                }
            }
        }
        if (firstColorIndex < 0) {
            return;
        }
        colorForm = udxfclr.TChooseDXFColorForm().create(this);
        if (colorForm == null) {
            throw new GeneralException.create("Problem: Could not create color window.");
        }
        try {
            colorForm.colorIndex = firstColorIndex;
            response = colorForm.ShowModal();
            if (response == mrOK) {
                if (this.colorsByPlantPart.Items.Count > 0) {
                    for (i = 0; i <= this.colorsByPlantPart.Items.Count - 1; i++) {
                        if (this.colorsByPlantPart.Selected[i]) {
                            this.options.dxf_plantPartColorIndexes[i] = colorForm.colorIndex;
                        }
                    }
                }
                this.colorsByPlantPart.Invalidate();
                this.optionsChanged = true;
            }
        } finally {
            colorForm.free;
            colorForm = null;
        }
    }
    
    public void colorsByPlantPartDblClick(TObject Sender) {
        this.setPlantPartColorClick(this);
    }
    
    public void transferRadioButton(TRadioButton radioButton, short value, short radioIndex) {
        if (this.transferDirection == kTransferLoad) {
            if (value == radioIndex) {
                radioButton.Checked = true;
            }
        } else if (this.transferDirection == kTransferSave) {
            if ((radioButton.Checked) && (value != radioIndex)) {
                this.optionsChanged = true;
            }
            if (radioButton.Checked) {
                value = radioIndex;
            }
        }
        return value;
    }
    
    public void transferCheckBox(TCheckBox checkBox, boolean value) {
        if (this.transferDirection == kTransferLoad) {
            checkBox.Checked = value;
        } else if (this.transferDirection == kTransferSave) {
            if (value != checkBox.Checked) {
                this.optionsChanged = true;
            }
            value = checkBox.Checked;
        }
        return value;
    }
    
    public void transferColor(TPanel colorPanel, TColorRef value) {
        raise "method transferColor had assigned to var parameter value not added to return; fixup manually"
        if (this.transferDirection == kTransferLoad) {
            colorPanel.Color = value;
        } else if (this.transferDirection == kTransferSave) {
            if (value != colorPanel.Color) {
                this.optionsChanged = true;
            }
            value = colorPanel.Color;
        }
    }
    
    public void transferSmallintSpinEditBox(TSpinEdit editBox, short value) {
        if (this.transferDirection == kTransferLoad) {
            editBox.Text = IntToStr(value);
        } else if (this.transferDirection == kTransferSave) {
            if (value != StrToIntDef(editBox.Text, 0)) {
                this.optionsChanged = true;
            }
            value = StrToIntDef(editBox.Text, 0);
        }
        return value;
    }
    
    public void transferRadioGroup(TRadioGroup radioGroup, short value) {
        if (this.transferDirection == kTransferLoad) {
            radioGroup.ItemIndex = value;
        } else if (this.transferDirection == kTransferSave) {
            if (value != radioGroup.ItemIndex) {
                this.optionsChanged = true;
            }
            value = radioGroup.ItemIndex;
        }
        return value;
    }
    
    public void transferComboBox(TComboBox comboBox, short value) {
        if (this.transferDirection == kTransferLoad) {
            comboBox.ItemIndex = value;
        } else if (this.transferDirection == kTransferSave) {
            if (value != comboBox.ItemIndex) {
                this.optionsChanged = true;
            }
            value = comboBox.ItemIndex;
        }
        return value;
    }
    
    public void transferSingleEditBox(TEdit editBox, float value) {
        float newValue = 0.0;
        
        if (this.transferDirection == kTransferLoad) {
            editBox.Text = UNRESOLVED.valueString(value);
        } else if (this.transferDirection == kTransferSave) {
            try {
                newValue = StrToFloat(editBox.Text);
            } catch (Exception e) {
                newValue = value;
            }
            if (newValue != value) {
                this.optionsChanged = true;
            }
            value = newValue;
        }
        return value;
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Exporting_3D_models_in_general");
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        UNRESOLVED.makeEnterWorkAsTab(this, this.ActiveControl, Key);
        return Key;
    }
    
    public void useSelectedPlantsClick(TObject Sender) {
        this.updatePredictedSizeDisplay();
    }
    
    public void useVisiblePlantsClick(TObject Sender) {
        this.updatePredictedSizeDisplay();
    }
    
    public void useAllPlantsClick(TObject Sender) {
        this.updatePredictedSizeDisplay();
    }
    
    public void stemCylinderFacesChange(TObject Sender) {
        int value = 0;
        
        value = StrToIntDef(this.stemCylinderFaces.Text, 5);
        if (value < UNRESOLVED.kMinOutputCylinderFaces) {
            value = UNRESOLVED.kMinOutputCylinderFaces;
        }
        if (value > UNRESOLVED.kMaxOutputCylinderFaces) {
            value = UNRESOLVED.kMaxOutputCylinderFaces;
        }
        this.stemCylinderFaces.Text = IntToStr(value);
        this.updatePredictedSizeDisplay();
    }
    
    public void dxfWriteColorsClick(TObject Sender) {
        this.colorDXFFromRGB.Visible = this.dxfWriteColors.Checked;
        this.colorDXFFromOneColor.Visible = this.dxfWriteColors.Checked;
        this.wholePlantColor.Visible = this.dxfWriteColors.Checked;
        this.colorDXFFromPlantPartType.Visible = this.dxfWriteColors.Checked;
        this.colorsByPlantPart.Visible = this.dxfWriteColors.Checked;
        this.setPlantPartColor.Visible = this.dxfWriteColors.Checked;
    }
    
}
