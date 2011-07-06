// unit uwizard

from conversion_common import *;
import umain;
import updcom;
import utravers;
import usupport;
import uturtle;
import udomain;
import ubitmap;
import utdo;
import ucollect;
import uplant;
import delphi_compatability;

// const
kMeristem_AlternateOrOpposite = 1;
kMeristem_BranchIndex = 2;
kMeristem_SecondaryBranching = 3;
kMeristem_BranchAngle = 4;
kInternode_Curviness = 5;
kInternode_Length = 6;
kLeaves_Scale = 7;
kLeaves_PetioleLength = 8;
kLeaves_Angle = 9;
kLeaflets_Number = 10;
kLeaflets_Shape = 11;
kLeaflets_Spread = 12;
kFlowers_NumPetals = 13;
kFlowers_Scale = 14;
kInflorDraw_NumFlowers = 15;
kInflorDraw_Shape = 16;
kInflorPlace_NumApical = 17;
kInflorPlace_NumAxillary = 18;
kInflorPlace_ApicalStalkLength = 19;
kInflorPlace_AxillaryStalkLength = 20;
kFruit_NumSections = 21;
kFruit_Scale = 22;
kInternode_Thickness = 23;
kInflorDraw_Thickness = 24;


// const
kStart = 0;
kMeristems = 1;
kInternodes = 2;
kLeaves = 3;
kCompoundLeaves = 4;
kInflorescencesPlacement = 5;
kInflorescences = 6;
kFlowers = 7;
kFruit = 8;
kFinish = 9;
kLastPanel = 9;
kReloadVariables = true;
kDontReloadVariables = false;


// const
kPreviewSize = 110;



// group indexes 
class TWizardForm extends PdForm {
    public TNotebook wizardNotebook;
    public TButton cancel;
    public TButton back;
    public TButton next;
    public TLabel panelMeristemsLabel;
    public TLabel panelInternodesLabel;
    public TLabel panelLeavesLabel;
    public TLabel panelInflorDrawingLabel;
    public TLabel branchingLabel;
    public TLabel leavesAlternateOppositeLabel;
    public TLabel branchAngleLabel;
    public TLabel secondaryBranchingLabel;
    public TLabel curvinessLabel;
    public TLabel internodeLengthLabel;
    public TLabel leafTdosLabel;
    public TLabel leafScaleLabel;
    public TLabel leafAngleLabel;
    public TLabel petioleLengthLabel;
    public TLabel finishLabelFirst;
    public TEdit newPlantName;
    public TLabel finishLabelSecond;
    public TLabel finishLabelThird;
    public TLabel panelFinishLabel;
    public TLabel panelStartLabel;
    public TLabel introLabelThird;
    public TLabel panelFlowersLabel;
    public TLabel petalTdosLabel;
    public TLabel petalScaleLabel;
    public TLabel petalsNumberLabel;
    public TLabel fruitTdoLabel;
    public TLabel fruitSectionsNumberLabel;
    public TLabel fruitScaleLabel;
    public TLabel panelFruitsLabel;
    public TLabel inflorFlowersLabel;
    public TLabel inflorShapeLabel;
    public TLabel panelInflorPlacementLabel;
    public TLabel apicalInflorsNumberLabel;
    public TLabel axillaryInflorsNumberLabel;
    public TLabel apicalStalkLabel;
    public TLabel axillaryStalkLabel;
    public TLabel introLabelFirst;
    public TImage apicalInflorExtraImage;
    public TImage axillaryInflorExtraImage;
    public TPanel previewPanel;
    public TSpeedButton internodesVeryShort;
    public TSpeedButton internodesShort;
    public TSpeedButton internodesMedium;
    public TSpeedButton internodesLong;
    public TSpeedButton internodesVeryLong;
    public TSpeedButton curvinessNone;
    public TSpeedButton curvinessLittle;
    public TSpeedButton curvinessSome;
    public TSpeedButton curvinessVery;
    public TSpeedButton leavesAlternate;
    public TSpeedButton leavesOpposite;
    public TSpeedButton branchNone;
    public TSpeedButton branchLittle;
    public TSpeedButton branchMedium;
    public TSpeedButton branchLot;
    public TSpeedButton secondaryBranchingYes;
    public TSpeedButton secondaryBranchingNo;
    public TSpeedButton branchAngleSmall;
    public TSpeedButton branchAngleMedium;
    public TSpeedButton branchAngleLarge;
    public TImage arrowLeavesAlternateOpposite;
    public TImage arrowBranching;
    public TImage arrowSecondaryBranching;
    public TImage arrowBranchAngle;
    public TImage arrowCurviness;
    public TImage arrowInternodeLength;
    public TImage arrowLeafScale;
    public TSpeedButton leafScaleTiny;
    public TSpeedButton leafScaleSmall;
    public TSpeedButton leafScaleMedium;
    public TSpeedButton leafScaleLarge;
    public TSpeedButton leafScaleHuge;
    public TImage arrowLeafAngle;
    public TSpeedButton leafAngleSmall;
    public TSpeedButton leafAngleMedium;
    public TSpeedButton leafAngleLarge;
    public TImage arrowPetioleLength;
    public TSpeedButton petioleVeryShort;
    public TSpeedButton petioleShort;
    public TSpeedButton petioleMedium;
    public TSpeedButton petioleLong;
    public TSpeedButton petioleVeryLong;
    public TImage arrowLeafTdos;
    public TSpeedButton petalsOne;
    public TSpeedButton petalsThree;
    public TSpeedButton petalsFour;
    public TSpeedButton petalsFive;
    public TSpeedButton petalsTen;
    public TSpeedButton petalScaleTiny;
    public TSpeedButton petalScaleSmall;
    public TSpeedButton petalScaleMedium;
    public TSpeedButton petalScaleLarge;
    public TSpeedButton petalScaleHuge;
    public TImage arrowPetalTdos;
    public TImage arrowPetalsNumber;
    public TImage arrowPetalScale;
    public TImage arrowInflorFlowers;
    public TImage arrowInflorShape;
    public TSpeedButton inflorFlowersOne;
    public TSpeedButton inflorFlowersTwo;
    public TSpeedButton inflorFlowersThree;
    public TSpeedButton inflorFlowersFive;
    public TSpeedButton inflorFlowersTen;
    public TSpeedButton inflorFlowersTwenty;
    public TSpeedButton inflorShapeSpike;
    public TSpeedButton inflorShapeRaceme;
    public TSpeedButton inflorShapePanicle;
    public TSpeedButton inflorShapeUmbel;
    public TSpeedButton inflorShapeHead;
    public TSpeedButton apicalInflorsNone;
    public TSpeedButton apicalInflorsOne;
    public TSpeedButton apicalInflorsTwo;
    public TSpeedButton apicalInflorsThree;
    public TSpeedButton apicalInflorsFive;
    public TImage arrowApicalInflorsNumber;
    public TSpeedButton axillaryInflorsNone;
    public TSpeedButton axillaryInflorsThree;
    public TSpeedButton axillaryInflorsFive;
    public TSpeedButton axillaryInflorsTen;
    public TSpeedButton axillaryInflorsTwenty;
    public TImage arrowAxillaryInflorsNumber;
    public TSpeedButton apicalStalkVeryShort;
    public TSpeedButton apicalStalkShort;
    public TSpeedButton apicalStalkMedium;
    public TSpeedButton apicalStalkLong;
    public TSpeedButton apicalStalkVeryLong;
    public TImage arrowApicalStalk;
    public TImage arrowAxillaryStalk;
    public TSpeedButton axillaryStalkVeryShort;
    public TSpeedButton axillaryStalkShort;
    public TSpeedButton axillaryStalkMedium;
    public TSpeedButton axillaryStalkLong;
    public TSpeedButton axillaryStalkVeryLong;
    public TImage arrowFruitTdo;
    public TImage arrowFruitSectionsNumber;
    public TImage arrowFruitScale;
    public TSpeedButton fruitSectionsOne;
    public TSpeedButton fruitSectionsThree;
    public TSpeedButton fruitSectionsFour;
    public TSpeedButton fruitSectionsFive;
    public TSpeedButton fruitSectionsTen;
    public TSpeedButton fruitScaleTiny;
    public TSpeedButton fruitScaleSmall;
    public TSpeedButton fruitScaleMedium;
    public TSpeedButton fruitScaleLarge;
    public TSpeedButton fruitScaleHuge;
    public TLabel introLabelSecond;
    public TLabel panelCompoundLeavesLabel;
    public TImage arrowLeaflets;
    public TLabel leafletsLabel;
    public TLabel leafletsShapeLabel;
    public TImage arrowLeafletsShape;
    public TSpeedButton leafletsOne;
    public TSpeedButton leafletsThree;
    public TSpeedButton leafletsFour;
    public TSpeedButton leafletsFive;
    public TSpeedButton leafletsSeven;
    public TSpeedButton leafletsPinnate;
    public TSpeedButton leafletsPalmate;
    public TImage arrowLeafletsSpacing;
    public TLabel leafletSpacingLabel;
    public TSpeedButton leafletSpacingClose;
    public TSpeedButton leafletSpacingMedium;
    public TSpeedButton leafletSpacingFar;
    public TDrawGrid leafTdosDraw;
    public TDrawGrid petalTdosDraw;
    public TDrawGrid sectionTdosDraw;
    public TButton defaultChoices;
    public TImage arrowInternodeWidth;
    public TLabel internodeWidthLabel;
    public TSpeedButton internodeWidthVeryThin;
    public TSpeedButton internodeWidthThin;
    public TSpeedButton internodeWidthMedium;
    public TSpeedButton internodeWidthThick;
    public TSpeedButton internodeWidthVeryThick;
    public TSpeedButton inflorShapeCluster;
    public TImage arrowInflorThickness;
    public TLabel inflorThicknessLabel;
    public TSpeedButton inflorWidthVeryThin;
    public TSpeedButton inflorWidthThin;
    public TSpeedButton inflorWidthMedium;
    public TSpeedButton inflorWidthThick;
    public TSpeedButton inflorWidthVeryThick;
    public TImage arrowPetalColor;
    public TLabel petalColorLabel;
    public TPanel petalColor;
    public TLabel fruitColorLabel;
    public TPanel fruitColor;
    public TImage arrowFruitColor;
    public TPanel hiddenPicturesPanel;
    public TImage startPageImage;
    public TImage meristemsPageImage;
    public TImage internodesPageImage;
    public TImage leavesPageImage;
    public TImage compoundLeavesPageImage;
    public TImage flowersPageImage;
    public TImage inflorDrawPageImage;
    public TImage inflorPlacePageImage;
    public TImage fruitsPageImage;
    public TImage finishPageImage;
    public TLabel fruitColorExplainLabel;
    public TLabel flowerColorExplainLabel;
    public TImage arrowShowFruits;
    public TLabel showFruitsLabel;
    public TRadioButton showFruitsYes;
    public TRadioButton showFruitsNo;
    public TLabel previewLabel;
    public TButton randomizePlant;
    public TImage inflorDrawPageImageDisabled;
    public TImage flowersPageImageDisabled;
    public TImage fruitsPageImageDisabled;
    public TSpeedButton turnLeft;
    public TSpeedButton turnRight;
    public TBevel bottomBevel;
    public TLabel longHintsSuggestionLabel;
    public TLabel Label1;
    public TLabel Label2;
    public TLabel Label3;
    public TLabel Label4;
    public TLabel Label5;
    public TLabel Label6;
    public TLabel Label7;
    public TLabel Label8;
    public TLabel Label9;
    public TLabel Label10;
    public TDrawGrid progressDrawGrid;
    public TLabel Label11;
    public TLabel Label12;
    public TSpeedButton helpButton;
    public TSpeedButton changeTdoLibrary;
    public TLabel sectionTdoSelectedLabel;
    public TLabel petalTdoSelectedLabel;
    public TLabel leafTdoSelectedLabel;
    public TImage startPicture;
    public PdPlant plant;
    public TListCollection tdos;
    public boolean plantHasInflorescences;
    public boolean tdoSelectionChanged;
    public boolean askedToSaveOptions;
    public PdPaintBoxWithPalette previewPaintBox;
    
    //$R *.DFM
    // panels 
    // -------------------------------------------------------------------------------------------- creation/destruction 
    public void create(TComponent AOwner) {
        short i = 0;
        
        super.create(AOwner);
        this.leafTdoSelectedLabel.Caption = "";
        this.petalTdoSelectedLabel.Caption = "";
        this.sectionTdoSelectedLabel.Caption = "";
        this.previewPaintBox = ubitmap.PdPaintBoxWithPalette().Create(this);
        this.previewPaintBox.Parent = this.previewPanel;
        this.previewPaintBox.Align = delphi_compatability.TAlign.alClient;
        this.previewPaintBox.OnPaint = this.previewPaintBoxPaint;
        // initialize default plant 
        this.plant = uplant.PdPlant().create();
        this.plant.defaultAllParameters();
        this.plant.setName("New plant " + IntToStr(updcom.numPlantsCreatedThisSession + 1));
        updcom.numPlantsCreatedThisSession += 1;
        this.newPlantName.Text = this.plant.getName();
        // initialize tdos 
        this.tdos = ucollect.TListCollection().Create();
        this.readTdosFromFile();
        if (udomain.domain != null) {
            for (i = 1; i <= udomain.kMaxWizardQuestions; i++) {
                // load info from domain on choices 
                this.setDownButtonForGroupIndexFromName(i, udomain.domain.options.wizardChoices[i]);
            }
        }
        if (udomain.domain.options.wizardShowFruit) {
            // handle radio button choice separately 
            this.showFruitsYes.Checked = true;
        } else {
            this.showFruitsNo.Checked = true;
        }
        // colors are handled separately 
        this.petalColor.Color = udomain.domain.options.wizardColors[1];
        this.fruitColor.Color = udomain.domain.options.wizardColors[2];
        if (!this.selectFirstTdoInDrawGridWithStringInName(this.leafTdosDraw, udomain.domain.options.wizardTdoNames[1])) {
            // tdo choices are handled separately - if not found use defaults by type 
            this.selectFirstTdoInDrawGridWithStringInName(this.leafTdosDraw, "leaf");
        }
        if (!this.selectFirstTdoInDrawGridWithStringInName(this.petalTdosDraw, udomain.domain.options.wizardTdoNames[2])) {
            this.selectFirstTdoInDrawGridWithStringInName(this.petalTdosDraw, "petal");
        }
        if (!this.selectFirstTdoInDrawGridWithStringInName(this.sectionTdosDraw, udomain.domain.options.wizardTdoNames[3])) {
            this.selectFirstTdoInDrawGridWithStringInName(this.sectionTdosDraw, "section");
        }
        this.updateForButtonInteractions();
    }
    
    public void FormCreate(TObject Sender) {
        this.startPicture.Picture.Bitmap.Palette = UNRESOLVED.CopyPalette(umain.MainForm.paletteImage.Picture.Bitmap.Palette);
        this.wizardNotebook.Invalidate();
        // assumes there is no border
        this.progressDrawGrid.DefaultColWidth = this.progressDrawGrid.Width / this.progressDrawGrid.ColCount;
        this.progressDrawGrid.Width = this.progressDrawGrid.DefaultColWidth * this.progressDrawGrid.ColCount;
        this.progressDrawGrid.DefaultRowHeight = this.progressDrawGrid.Height;
        this.setPageIndex(0);
        this.updateProgress();
    }
    
    public void destroy() {
        this.plant.free;
        this.plant = null;
        this.tdos.free;
        this.tdos = null;
        super.destroy();
    }
    
    // -------------------------------------------------------------------------------------------- *tdos 
    public String hintForTdosDrawGridAtPoint(TComponent aComponent, TPoint aPoint, TRect cursorRect) {
        raise "method hintForTdosDrawGridAtPoint had assigned to var parameter cursorRect not added to return; fixup manually"
        result = "";
        TDrawGrid grid = new TDrawGrid();
        int col = 0;
        int row = 0;
        KfObject3D tdo = new KfObject3D();
        
        result = "";
        if ((aComponent == null) || (!(aComponent instanceof delphi_compatability.TDrawGrid))) {
            return result;
        }
        grid = (delphi_compatability.TDrawGrid)aComponent;
        col, row = grid.MouseToCell(aPoint.X, aPoint.Y, col, row);
        if (grid == this.progressDrawGrid) {
            switch (col) {
                case kStart:
                    result = "start";
                    break;
                case kMeristems:
                    result = "meristems";
                    break;
                case kInternodes:
                    result = "internodes";
                    break;
                case kLeaves:
                    result = "leaves";
                    break;
                case kCompoundLeaves:
                    result = "compound leaves";
                    break;
                case kFlowers:
                    result = "flowers";
                    break;
                case kInflorescences:
                    result = "inflorescence drawing";
                    break;
                case kInflorescencesPlacement:
                    result = "inflorescence placement";
                    break;
                case kFruit:
                    result = "fruit";
                    break;
                case kFinish:
                    result = "finish";
                    break;
        } else {
            tdo = this.tdoForIndex(col);
            if (tdo == null) {
                return result;
            }
            result = tdo.getName();
        }
        // change hint if cursor moves out of the current item's rectangle 
        cursorRect = grid.CellRect(col, row);
        return result;
    }
    
    public void changeTdoLibraryClick(TObject Sender) {
        this.loadNewTdoLibrary();
        this.leafTdosDraw.Invalidate();
        this.petalTdosDraw.Invalidate();
        this.sectionTdosDraw.Invalidate();
    }
    
    public void loadNewTdoLibrary() {
        String fileNameWithPath = "";
        
        fileNameWithPath = usupport.getFileOpenInfo(usupport.kFileTypeTdo, udomain.domain.defaultTdoLibraryFileName, "Choose a 3D object library (tdo) file");
        if (fileNameWithPath == "") {
            return;
        }
        udomain.domain.defaultTdoLibraryFileName = fileNameWithPath;
        this.readTdosFromFile();
    }
    
    public void readTdosFromFile() {
        KfObject3D newTdo = new KfObject3D();
        TextFile inputFile = new TextFile();
        
        this.tdos.clear();
        if (udomain.domain == null) {
            return;
        }
        if (!udomain.domain.checkForExistingDefaultTdoLibrary()) {
            MessageDialog("Because you didn't choose a 3D object library, you will only" + chr(13) + "be able to use a default 3D object on your new plant." + chr(13) + chr(13) + "You can also choose a 3D object library" + chr(13) + "by clicking the 3D Objects button in the wizard.", mtWarning, {mbOK, }, 0);
            return;
        }
        AssignFile(inputFile, udomain.domain.defaultTdoLibraryFileName);
        try {
            // v1.5
            usupport.setDecimalSeparator();
            Reset(inputFile);
            while (!UNRESOLVED.eof(inputFile)) {
                newTdo = utdo.KfObject3D().create();
                newTdo.readFromFileStream(inputFile, utdo.kInTdoLibrary);
                this.tdos.Add(newTdo);
            }
        } finally {
            CloseFile(inputFile);
            this.leafTdosDraw.ColCount = this.tdos.Count;
            this.petalTdosDraw.ColCount = this.tdos.Count;
            this.sectionTdosDraw.ColCount = this.tdos.Count;
        }
    }
    
    public KfObject3D tdoForIndex(short index) {
        result = new KfObject3D();
        result = null;
        if ((index >= 0) && (index <= this.tdos.Count - 1)) {
            result = utdo.KfObject3D(this.tdos.Items[index]);
        }
        return result;
    }
    
    public void leafTdosDrawDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        this.drawCellInTdoDrawGrid(this.leafTdosDraw, Col, UNRESOLVED.gdSelected in State, Rect);
    }
    
    public void petalTdosDrawDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        this.drawCellInTdoDrawGrid(this.petalTdosDraw, Col, UNRESOLVED.gdSelected in State, Rect);
    }
    
    public void sectionTdosDrawDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        this.drawCellInTdoDrawGrid(this.sectionTdosDraw, Col, UNRESOLVED.gdSelected in State, Rect);
    }
    
    public void drawCellInTdoDrawGrid(TDrawGrid grid, short column, boolean selected, TRect rect) {
        KfObject3d tdo = new KfObject3d();
        KfTurtle turtle = new KfTurtle();
        TPoint bestPoint = new TPoint();
        
        if (!selected) {
            grid.Canvas.Brush.Color = delphi_compatability.clWhite;
            grid.Canvas.Font.Color = UNRESOLVED.clBtnText;
        } else {
            grid.Canvas.Brush.Color = UNRESOLVED.clHighlight;
            grid.Canvas.Font.Color = UNRESOLVED.clHighlightText;
        }
        grid.Canvas.FillRect(Rect);
        tdo = null;
        tdo = this.tdoForIndex(column);
        if (tdo == null) {
            return;
        }
        // draw tdo 
        turtle = uturtle.KfTurtle.defaultStartUsing();
        try {
            turtle.drawingSurface.pane = grid.Canvas;
            turtle.setDrawOptionsForDrawingTdoOnly();
            // must be after pane and draw options set 
            turtle.reset();
            bestPoint = tdo.bestPointForDrawingAtScale(turtle, Point(Rect.left, Rect.top), Point(usupport.rWidth(Rect), usupport.rHeight(Rect)), 0.2);
            turtle.xyz(bestPoint.X, bestPoint.Y, 0);
            //turtle.xyz(rect.left + (rect.right - rect.left) div 2, rect.bottom - 5, 0);
            turtle.drawingSurface.recordingStart();
            //15);
            tdo.draw(turtle, 0.2, "", "", 0, 0);
            turtle.drawingSurface.recordingStop();
            turtle.drawingSurface.recordingDraw();
            turtle.drawingSurface.clearTriangles();
        } finally {
            uturtle.KfTurtle.defaultStopUsing();
        }
    }
    
    // ---------------------------------------------------------------------------------------- interactions 
    public void updateForButtonInteractions() {
        boolean hadInflors = false;
        
        // do all of these at once, because then you can do them after loading options at startup
        //    (it doesn't take very long) 
        // meristems 
        this.arrowSecondaryBranching.Visible = !this.branchNone.Down;
        this.secondaryBranchingLabel.Enabled = !this.branchNone.Down;
        this.secondaryBranchingYes.Enabled = !this.branchNone.Down;
        this.secondaryBranchingNo.Enabled = !this.branchNone.Down;
        this.arrowBranchAngle.Visible = !this.branchNone.Down;
        this.branchAngleLabel.Enabled = !this.branchNone.Down;
        this.branchAngleSmall.Enabled = !this.branchNone.Down;
        this.branchAngleMedium.Enabled = !this.branchNone.Down;
        this.branchAngleLarge.Enabled = !this.branchNone.Down;
        // internodes 
        // leaves 
        // compound leaves 
        this.arrowLeafletsShape.Visible = !this.leafletsOne.Down;
        this.leafletsShapeLabel.Enabled = !this.leafletsOne.Down;
        this.leafletsPinnate.Enabled = !this.leafletsOne.Down;
        this.leafletsPalmate.Enabled = !this.leafletsOne.Down;
        this.arrowLeafletsSpacing.Visible = !this.leafletsOne.Down;
        this.leafletSpacingLabel.Enabled = !this.leafletsOne.Down;
        this.leafletSpacingClose.Enabled = !this.leafletsOne.Down;
        this.leafletSpacingMedium.Enabled = !this.leafletsOne.Down;
        this.leafletSpacingFar.Enabled = !this.leafletsOne.Down;
        // inflor placement 
        hadInflors = this.plantHasInflorescences;
        this.plantHasInflorescences = (!this.apicalInflorsNone.Down) || (!this.axillaryInflorsNone.Down);
        if (hadInflors != this.plantHasInflorescences) {
            this.progressDrawGrid.Invalidate();
        }
        this.arrowApicalStalk.Visible = !this.apicalInflorsNone.Down;
        this.apicalStalkLabel.Enabled = !this.apicalInflorsNone.Down;
        this.apicalStalkVeryShort.Enabled = !this.apicalInflorsNone.Down;
        this.apicalStalkShort.Enabled = !this.apicalInflorsNone.Down;
        this.apicalStalkMedium.Enabled = !this.apicalInflorsNone.Down;
        this.apicalStalkLong.Enabled = !this.apicalInflorsNone.Down;
        this.apicalStalkVeryLong.Enabled = !this.apicalInflorsNone.Down;
        this.arrowAxillaryStalk.Visible = !this.axillaryInflorsNone.Down;
        this.axillaryStalkLabel.Enabled = !this.axillaryInflorsNone.Down;
        this.axillaryStalkVeryShort.Enabled = !this.axillaryInflorsNone.Down;
        this.axillaryStalkShort.Enabled = !this.axillaryInflorsNone.Down;
        this.axillaryStalkMedium.Enabled = !this.axillaryInflorsNone.Down;
        this.axillaryStalkLong.Enabled = !this.axillaryInflorsNone.Down;
        this.axillaryStalkVeryLong.Enabled = !this.axillaryInflorsNone.Down;
        // inflor drawing 
        this.arrowInflorShape.Visible = !this.inflorFlowersOne.Down;
        this.inflorShapeLabel.Enabled = !this.inflorFlowersOne.Down;
        this.inflorShapeSpike.Enabled = !this.inflorFlowersOne.Down;
        this.inflorShapeRaceme.Enabled = !this.inflorFlowersOne.Down;
        this.inflorShapePanicle.Enabled = !this.inflorFlowersOne.Down;
        this.inflorShapeUmbel.Enabled = !this.inflorFlowersOne.Down;
        this.inflorShapeCluster.Enabled = !this.inflorFlowersOne.Down;
        this.inflorShapeHead.Enabled = !this.inflorFlowersOne.Down;
        // flowers 
        // fruit 
        this.arrowFruitTdo.Visible = !this.showFruitsNo.Checked;
        this.fruitTdoLabel.Enabled = !this.showFruitsNo.Checked;
        this.sectionTdosDraw.Visible = !this.showFruitsNo.Checked;
        this.sectionTdoSelectedLabel.Visible = !this.showFruitsNo.Checked;
        this.arrowFruitSectionsNumber.Visible = !this.showFruitsNo.Checked;
        this.fruitSectionsNumberLabel.Enabled = !this.showFruitsNo.Checked;
        this.fruitSectionsOne.Enabled = !this.showFruitsNo.Checked;
        this.fruitSectionsThree.Enabled = !this.showFruitsNo.Checked;
        this.fruitSectionsFour.Enabled = !this.showFruitsNo.Checked;
        this.fruitSectionsFive.Enabled = !this.showFruitsNo.Checked;
        this.fruitSectionsTen.Enabled = !this.showFruitsNo.Checked;
        this.arrowFruitScale.Visible = !this.showFruitsNo.Checked;
        this.fruitScaleLabel.Enabled = !this.showFruitsNo.Checked;
        this.fruitScaleTiny.Enabled = !this.showFruitsNo.Checked;
        this.fruitScaleSmall.Enabled = !this.showFruitsNo.Checked;
        this.fruitScaleMedium.Enabled = !this.showFruitsNo.Checked;
        this.fruitScaleLarge.Enabled = !this.showFruitsNo.Checked;
        this.fruitScaleHuge.Enabled = !this.showFruitsNo.Checked;
        this.arrowFruitColor.Visible = !this.showFruitsNo.Checked;
        this.fruitColorLabel.Enabled = !this.showFruitsNo.Checked;
        this.fruitColor.Visible = !this.showFruitsNo.Checked;
        this.fruitColorExplainLabel.Enabled = !this.showFruitsNo.Checked;
    }
    
    public void branchNoneClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void branchLittleClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void branchMediumClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void branchLotClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void leafletsOneClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void leafletsThreeClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void leafletsFourClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void leafletsFiveClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void leafletsSevenClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void inflorFlowersOneClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void inflorFlowersTwoClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void inflorFlowersThreeClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void inflorFlowersFiveClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void inflorFlowersTenClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void inflorFlowersTwentyClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void apicalInflorsNoneClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void apicalInflorsOneClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void apicalInflorsTwoClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void apicalInflorsThreeClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void apicalInflorsFiveClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void axillaryInflorsNoneClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void axillaryInflorsThreeClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void axillaryInflorsFiveClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void axillaryInflorsTenClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void axillaryInflorsTwentyClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void showFruitsYesClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    public void showFruitsNoClick(TObject Sender) {
        this.updateForButtonInteractions();
    }
    
    // -------------------------------------------------------------------------------------------- transfer 
    public void defaultChoicesClick(TObject Sender) {
        if (MessageDialog("Are you sure you want to set all the wizard choices to defaults?" + chr(13) + chr(13) + "This action is not undoable.", mtConfirmation, {mbYes, mbNo, }, 0) == delphi_compatability.IDNO) {
            return;
        }
        this.setDownButtonForGroupIndexFromName(kMeristem_AlternateOrOpposite, "leavesAlternate");
        this.setDownButtonForGroupIndexFromName(kMeristem_BranchIndex, "branchNone");
        this.setDownButtonForGroupIndexFromName(kInternode_Curviness, "curvinessLittle");
        this.setDownButtonForGroupIndexFromName(kInternode_Length, "internodesMedium");
        this.setDownButtonForGroupIndexFromName(kInternode_Thickness, "internodeWidthThin");
        this.setDownButtonForGroupIndexFromName(kLeaves_Scale, "leafScaleMedium");
        this.setDownButtonForGroupIndexFromName(kLeaves_PetioleLength, "petioleMedium");
        this.setDownButtonForGroupIndexFromName(kLeaves_Angle, "leafAngleMedium");
        this.setDownButtonForGroupIndexFromName(kLeaflets_Number, "leafletsOne");
        this.setDownButtonForGroupIndexFromName(kInflorPlace_NumApical, "apicalInflorsNone");
        this.setDownButtonForGroupIndexFromName(kInflorPlace_NumAxillary, "axillaryInflorsNone");
        this.updateForButtonInteractions();
        if (this.wizardNotebook.PageIndex == kLastPanel) {
            this.drawPreview(kReloadVariables);
        }
    }
    
    public boolean selectFirstTdoInDrawGridWithStringInName(TDrawGrid grid, String aString) {
        result = false;
        short indexToSelect = 0;
        short i = 0;
        KfObject3D tdo = new KfObject3D();
        TGridRect gridRect = new TGridRect();
        
        // returns true if a tdo was selected 
        result = false;
        indexToSelect = -1;
        if (this.tdos.Count > 0) {
            for (i = 0; i <= this.tdos.Count - 1; i++) {
                tdo = utdo.KfObject3D(this.tdos.Items[i]);
                if (tdo == null) {
                    return result;
                }
                if (UNRESOLVED.pos(uppercase(aString), uppercase(tdo.getName())) > 0) {
                    indexToSelect = i;
                    result = true;
                    break;
                }
            }
        }
        if (indexToSelect >= 0) {
            gridRect.left = indexToSelect;
            gridRect.right = indexToSelect;
            gridRect.top = 0;
            gridRect.bottom = 0;
            grid.Selection = gridRect;
            grid.LeftCol = indexToSelect;
            if (grid == this.leafTdosDraw) {
                this.showTdoNameInLabel(indexToSelect, this.leafTdoSelectedLabel);
            } else if (grid == this.petalTdosDraw) {
                this.showTdoNameInLabel(indexToSelect, this.petalTdoSelectedLabel);
            } else if (grid == this.sectionTdosDraw) {
                this.showTdoNameInLabel(indexToSelect, this.sectionTdoSelectedLabel);
            }
        }
        return result;
    }
    
    public void setPlantVariables() {
        if (this.plant == null) {
            return;
        }
        this.plant.defaultAllParameters();
        // set variables in plant based on options 
        this.finishForMeristems();
        this.finishForInternodes();
        this.finishForLeaves();
        this.finishForCompoundLeaves();
        this.finishForInflorescencePlacement();
        this.finishForInflorescences();
        this.finishForFlowers();
        this.finishForFruit();
        this.plant.setName(this.newPlantName.Text);
        this.plant.setAge(this.plant.pGeneral.ageAtMaturity);
    }
    
    public void saveOptionsToDomain() {
        short i = 0;
        
        for (i = 1; i <= udomain.kMaxWizardQuestions; i++) {
            udomain.domain.options.wizardChoices[i] = this.downButtonNameForGroupIndex(i);
        }
        // handle radio button choice separately 
        udomain.domain.options.wizardShowFruit = this.showFruitsYes.Checked;
        udomain.domain.options.wizardColors[1] = this.petalColor.Color;
        udomain.domain.options.wizardColors[2] = this.fruitColor.Color;
        if (this.plant.pLeaf.leafTdoParams.object3D != null) {
            udomain.domain.options.wizardTdoNames[1] = this.plant.pLeaf.leafTdoParams.object3D.getName();
        }
        if (this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].object3D != null) {
            // cfk do first petal only in wizard, right?
            udomain.domain.options.wizardTdoNames[2] = this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].object3D.getName();
        }
        if (this.plant.pFruit.tdoParams.object3D != null) {
            udomain.domain.options.wizardTdoNames[3] = this.plant.pFruit.tdoParams.object3D.getName();
        }
    }
    
    public boolean optionsHaveChanged() {
        result = false;
        short i = 0;
        String downButtonName = "";
        
        result = false;
        for (i = 1; i <= udomain.kMaxWizardQuestions; i++) {
            downButtonName = this.downButtonNameForGroupIndex(i);
            if (udomain.domain.options.wizardChoices[i] != "") {
                result = result || (udomain.domain.options.wizardChoices[i] != downButtonName);
            }
        }
        result = result || (udomain.domain.options.wizardShowFruit != this.showFruitsYes.Checked);
        result = result || (udomain.domain.options.wizardColors[1] != this.petalColor.Color);
        result = result || (udomain.domain.options.wizardColors[2] != this.fruitColor.Color);
        result = result || this.tdoSelectionChanged;
        return result;
    }
    
    public void setDownButtonForGroupIndexFromName(short aGroupIndex, String aName) {
        short i = 0;
        TSpeedButton button = new TSpeedButton();
        
        if (aName == "") {
            return;
        }
        if (this.componentCount > 0) {
            for (i = 0; i <= this.componentCount - 1; i++) {
                if (!(this.components[i] instanceof delphi_compatability.TSpeedButton)) {
                    continue;
                }
                button = (delphi_compatability.TSpeedButton)this.components[i];
                if (button.GroupIndex == aGroupIndex) {
                    if (button.Name == aName) {
                        // only one can be down, so can exit when one is down 
                        button.Down = true;
                        return;
                    }
                }
            }
        }
    }
    
    public String downButtonNameForGroupIndex(short aGroupIndex) {
        result = "";
        short i = 0;
        TSpeedButton button = new TSpeedButton();
        
        result = "";
        if (this.componentCount > 0) {
            for (i = 0; i <= this.componentCount - 1; i++) {
                if (!(this.components[i] instanceof delphi_compatability.TSpeedButton)) {
                    continue;
                }
                button = (delphi_compatability.TSpeedButton)this.components[i];
                if ((button.GroupIndex == aGroupIndex) && (button.Enabled)) {
                    if (button.Down) {
                        // if not enabled, don't want to match
                        // only one can be down, so can exit when one is down 
                        result = button.Name;
                        return result;
                    }
                }
            }
        }
        return result;
    }
    
    public void finishForMeristems() {
        if (this.leavesAlternate.Enabled) {
            if (this.leavesAlternate.Down) {
                // alternate/opposite 
                this.plant.pMeristem.branchingAndLeafArrangement = uplant.kArrangementAlternate;
            } else {
                this.plant.pMeristem.branchingAndLeafArrangement = uplant.kArrangementOpposite;
            }
        }
        if (this.branchNone.Enabled) {
            if (this.branchNone.Down) {
                // branching index 
                this.plant.pMeristem.branchingIndex = 0;
            } else if (this.branchLittle.Down) {
                this.plant.pMeristem.branchingIndex = 10;
            } else if (this.branchMedium.Down) {
                this.plant.pMeristem.branchingIndex = 30;
            } else if (this.branchLot.Down) {
                this.plant.pMeristem.branchingIndex = 80;
            }
        }
        if (this.secondaryBranchingYes.Enabled) {
            // secondary branching 
            this.plant.pMeristem.secondaryBranchingIsAllowed = this.secondaryBranchingYes.Down;
        }
        if (this.branchAngleSmall.Enabled) {
            if (this.branchAngleSmall.Down) {
                // branch angle 
                this.plant.pMeristem.branchingAngle = 20;
            } else if (this.branchAngleMedium.Down) {
                this.plant.pMeristem.branchingAngle = 40;
            } else if (this.branchAngleLarge.Down) {
                this.plant.pMeristem.branchingAngle = 60;
            }
        }
    }
    
    public void finishForInternodes() {
        if (this.curvinessNone.Enabled) {
            if (this.curvinessNone.Down) {
                // curviness 
                this.plant.pInternode.curvingIndex = 0;
                this.plant.pInternode.firstInternodeCurvingIndex = 0;
            } else if (this.curvinessLittle.Down) {
                this.plant.pInternode.curvingIndex = 10;
                this.plant.pInternode.firstInternodeCurvingIndex = 5;
            } else if (this.curvinessSome.Down) {
                this.plant.pInternode.curvingIndex = 30;
                this.plant.pInternode.firstInternodeCurvingIndex = 10;
            } else if (this.curvinessVery.Down) {
                this.plant.pInternode.curvingIndex = 50;
                this.plant.pInternode.firstInternodeCurvingIndex = 20;
            }
        }
        if (this.internodesVeryShort.Enabled) {
            if (this.internodesVeryShort.Down) {
                // length 
                this.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 1;
            } else if (this.internodesShort.Down) {
                this.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 10;
            } else if (this.internodesMedium.Down) {
                this.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 15;
            } else if (this.internodesLong.Down) {
                this.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 25;
            } else if (this.internodesVeryLong.Down) {
                this.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm = 50;
            }
        }
        if (this.internodeWidthVeryThin.Enabled) {
            if (this.internodeWidthVeryThin.Down) {
                // width 
                this.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 0.5;
            } else if (this.internodeWidthThin.Down) {
                this.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 1;
            } else if (this.internodeWidthMedium.Down) {
                this.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 2;
            } else if (this.internodeWidthThick.Down) {
                this.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 3;
            } else if (this.internodeWidthVeryThick.Down) {
                this.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm = 10;
            }
        }
    }
    
    public void finishForLeaves() {
        KfObject3D tdo = new KfObject3D();
        
        if (this.leafScaleTiny.Enabled) {
            if (this.leafScaleTiny.Down) {
                // scale 
                this.plant.pLeaf.leafTdoParams.scaleAtFullSize = 5;
            } else if (this.leafScaleSmall.Down) {
                this.plant.pLeaf.leafTdoParams.scaleAtFullSize = 20;
            } else if (this.leafScaleMedium.Down) {
                this.plant.pLeaf.leafTdoParams.scaleAtFullSize = 40;
            } else if (this.leafScaleLarge.Down) {
                this.plant.pLeaf.leafTdoParams.scaleAtFullSize = 60;
            } else if (this.leafScaleHuge.Down) {
                this.plant.pLeaf.leafTdoParams.scaleAtFullSize = 100;
            }
        }
        if (this.petioleVeryShort.Enabled) {
            if (this.petioleVeryShort.Down) {
                // petiole length 
                this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 1;
            } else if (this.petioleShort.Down) {
                this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 10;
            } else if (this.petioleMedium.Down) {
                this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 20;
            } else if (this.petioleLong.Down) {
                this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 30;
            } else if (this.petioleVeryLong.Down) {
                this.plant.pLeaf.petioleLengthAtOptimalBiomass_mm = 60;
            }
        }
        if (this.leafAngleSmall.Enabled) {
            if (this.leafAngleSmall.Down) {
                // petiole angle 
                this.plant.pLeaf.petioleAngle = 20;
            } else if (this.leafAngleMedium.Down) {
                this.plant.pLeaf.petioleAngle = 40;
            } else if (this.leafAngleLarge.Down) {
                this.plant.pLeaf.petioleAngle = 60;
            }
        }
        if (this.leafTdosDraw.Visible) {
            // tdo 
            tdo = this.tdoForIndex(this.leafTdosDraw.Selection.left);
            if ((tdo != null) && (this.plant.pLeaf.leafTdoParams.object3D != null)) {
                this.plant.pLeaf.leafTdoParams.object3D.copyFrom(tdo);
            }
        }
    }
    
    public void finishForCompoundLeaves() {
        if (this.leafletsOne.Enabled) {
            if (this.leafletsOne.Down) {
                // num leaflets 
                this.plant.pLeaf.compoundNumLeaflets = 1;
            } else if (this.leafletsThree.Down) {
                this.plant.pLeaf.compoundNumLeaflets = 3;
            } else if (this.leafletsFour.Down) {
                this.plant.pLeaf.compoundNumLeaflets = 4;
            } else if (this.leafletsFive.Down) {
                this.plant.pLeaf.compoundNumLeaflets = 5;
            } else if (this.leafletsSeven.Down) {
                this.plant.pLeaf.compoundNumLeaflets = 7;
            }
        }
        if (this.leafletsPinnate.Enabled) {
            if (this.leafletsPinnate.Down) {
                // shape 
                this.plant.pLeaf.compoundPinnateOrPalmate = uplant.kCompoundLeafPinnate;
            } else if (this.leafletsPalmate.Down) {
                this.plant.pLeaf.compoundPinnateOrPalmate = uplant.kCompoundLeafPalmate;
            }
        }
        if (this.leafletSpacingClose.Enabled) {
            if (this.leafletSpacingClose.Down) {
                // spread 
                this.plant.pLeaf.compoundRachisToPetioleRatio = 10.0;
            } else if (this.leafletSpacingMedium.Down) {
                this.plant.pLeaf.compoundRachisToPetioleRatio = 30.0;
            } else if (this.leafletSpacingFar.Down) {
                this.plant.pLeaf.compoundRachisToPetioleRatio = 50.0;
            }
        }
    }
    
    public void finishForInflorescencePlacement() {
        if (this.apicalInflorsNone.Enabled) {
            if (this.apicalInflorsNone.Down) {
                // num apical inflors 
                this.plant.pGeneral.numApicalInflors = 0;
            } else if (this.apicalInflorsOne.Down) {
                this.plant.pGeneral.numApicalInflors = 1;
            } else if (this.apicalInflorsTwo.Down) {
                this.plant.pGeneral.numApicalInflors = 2;
            } else if (this.apicalInflorsThree.Down) {
                this.plant.pGeneral.numApicalInflors = 3;
            } else if (this.apicalInflorsFive.Down) {
                this.plant.pGeneral.numApicalInflors = 5;
            }
        }
        if (this.axillaryInflorsNone.Enabled) {
            if (this.axillaryInflorsNone.Down) {
                // num axillary inflors 
                this.plant.pGeneral.numAxillaryInflors = 0;
            } else if (this.axillaryInflorsThree.Down) {
                this.plant.pGeneral.numAxillaryInflors = 3;
            } else if (this.axillaryInflorsFive.Down) {
                this.plant.pGeneral.numAxillaryInflors = 5;
            } else if (this.axillaryInflorsTen.Down) {
                this.plant.pGeneral.numAxillaryInflors = 10;
            } else if (this.axillaryInflorsTwenty.Down) {
                this.plant.pGeneral.numAxillaryInflors = 20;
            }
        }
        if (this.apicalInflorsNone.Enabled && this.apicalInflorsNone.Down && this.axillaryInflorsNone.Enabled && this.axillaryInflorsNone.Down) {
            // if no flowers, set age to allocate at max
            this.plant.pGeneral.ageAtWhichFloweringStarts = this.plant.pGeneral.ageAtMaturity + 1;
        } else {
            this.plant.pGeneral.ageAtWhichFloweringStarts = intround(this.plant.pGeneral.ageAtMaturity * 0.6);
        }
        if (this.apicalStalkVeryShort.Enabled) {
            if (this.apicalStalkVeryShort.Down) {
                // apical stalk 
                this.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 1;
            } else if (this.apicalStalkShort.Down) {
                this.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 10;
            } else if (this.apicalStalkMedium.Down) {
                this.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 30;
            } else if (this.apicalStalkLong.Down) {
                this.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 50;
            } else if (this.apicalStalkVeryLong.Down) {
                this.plant.pInflor[uplant.kGenderFemale].terminalStalkLength_mm = 100;
            }
        }
        if (this.axillaryStalkVeryShort.Enabled) {
            if (this.axillaryStalkVeryShort.Down) {
                // axillary stalk (peduncle) 
                this.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 1;
            } else if (this.axillaryStalkShort.Down) {
                this.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 5;
            } else if (this.axillaryStalkMedium.Down) {
                this.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 10;
            } else if (this.axillaryStalkLong.Down) {
                this.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 15;
            } else if (this.axillaryStalkVeryLong.Down) {
                this.plant.pInflor[uplant.kGenderFemale].peduncleLength_mm = 40;
            }
        }
    }
    
    public void finishForInflorescences() {
        short numFlowers = 0;
        
        if (!this.plantHasInflorescences) {
            return;
        }
        // num flowers 
        numFlowers = 0;
        if (this.inflorFlowersOne.Enabled) {
            if (this.inflorFlowersOne.Down) {
                numFlowers = 1;
            } else if (this.inflorFlowersTwo.Down) {
                numFlowers = 2;
            } else if (this.inflorFlowersThree.Down) {
                numFlowers = 3;
            } else if (this.inflorFlowersFive.Down) {
                numFlowers = 5;
            } else if (this.inflorFlowersTen.Down) {
                numFlowers = 10;
            } else if (this.inflorFlowersTwenty.Down) {
                numFlowers = 20;
            }
        }
        this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = numFlowers;
        this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0;
        this.plant.pInflor[uplant.kGenderFemale].numBranches = 0;
        if (this.inflorShapeSpike.Enabled) {
            if (this.inflorShapeSpike.Down) {
                // shape 
                this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = numFlowers;
                this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0;
                this.plant.pInflor[uplant.kGenderFemale].numBranches = 0;
                this.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 1;
                this.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 30;
                this.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 10;
                this.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true;
            } else if (this.inflorShapeRaceme.Down) {
                this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = numFlowers;
                this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0;
                this.plant.pInflor[uplant.kGenderFemale].numBranches = 0;
                this.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 20;
                this.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 45;
                this.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 10;
                this.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true;
            } else if (this.inflorShapePanicle.Down) {
                switch (numFlowers) {
                    case 1:
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 1;
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0;
                        this.plant.pInflor[uplant.kGenderFemale].numBranches = 0;
                        break;
                    case 2:
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 0;
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 1;
                        this.plant.pInflor[uplant.kGenderFemale].numBranches = 2;
                        break;
                    case 3:
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 1;
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 1;
                        this.plant.pInflor[uplant.kGenderFemale].numBranches = 2;
                        break;
                    case 5:
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 1;
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 2;
                        this.plant.pInflor[uplant.kGenderFemale].numBranches = 2;
                        break;
                    case 10:
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 1;
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 3;
                        this.plant.pInflor[uplant.kGenderFemale].numBranches = 3;
                        break;
                    case 20:
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 4;
                        this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 4;
                        this.plant.pInflor[uplant.kGenderFemale].numBranches = 4;
                        break;
                this.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 15;
                this.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 30;
                this.plant.pInflor[uplant.kGenderFemale].branchAngle = 35;
                this.plant.pInflor[uplant.kGenderFemale].branchesAreAlternate = true;
                this.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 7;
                this.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true;
            } else if (this.inflorShapeUmbel.Down) {
                this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 0;
                this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 1;
                this.plant.pInflor[uplant.kGenderFemale].numBranches = numFlowers;
                this.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 20;
                this.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 20;
                this.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 0.0;
                this.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true;
            } else if (this.inflorShapeCluster.Down) {
                this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = 0;
                this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 1;
                this.plant.pInflor[uplant.kGenderFemale].numBranches = numFlowers;
                this.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = true;
                this.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 3;
                this.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 1;
                this.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 25;
            } else if (this.inflorShapeHead.Down) {
                this.plant.pInflor[uplant.kGenderFemale].numFlowersOnMainBranch = numFlowers;
                this.plant.pInflor[uplant.kGenderFemale].numFlowersPerBranch = 0;
                this.plant.pInflor[uplant.kGenderFemale].numBranches = 0;
                this.plant.pInflor[uplant.kGenderFemale].pedicelLength_mm = 10;
                this.plant.pInflor[uplant.kGenderFemale].pedicelAngle = 0;
                this.plant.pInflor[uplant.kGenderFemale].internodeLength_mm = 10;
                this.plant.pInflor[uplant.kGenderFemale].isHead = true;
                this.plant.pInflor[uplant.kGenderFemale].flowersSpiralOnStem = false;
            }
        }
        if (this.inflorWidthVeryThin.Enabled) {
            if (this.inflorWidthVeryThin.Down) {
                // width 
                this.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 0.5;
            } else if (this.inflorWidthThin.Down) {
                this.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 1;
            } else if (this.inflorWidthMedium.Down) {
                this.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 2;
            } else if (this.inflorWidthThick.Down) {
                this.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 3;
            } else if (this.inflorWidthVeryThick.Down) {
                this.plant.pInflor[uplant.kGenderFemale].internodeWidth_mm = 10;
            }
        }
    }
    
    public void finishForFlowers() {
        KfObject3D tdo = new KfObject3D();
        
        if (!this.plantHasInflorescences) {
            return;
        }
        if (this.petalsOne.Enabled) {
            if (this.petalsOne.Down) {
                // cfk only first petals for wizard?
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 1;
            } else if (this.petalsThree.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 3;
            } else if (this.petalsFour.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 4;
            } else if (this.petalsFive.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 5;
            } else if (this.petalsTen.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].repetitions = 10;
            }
        }
        if (this.petalScaleTiny.Enabled) {
            if (this.petalScaleTiny.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 4;
            } else if (this.petalScaleSmall.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 10;
            } else if (this.petalScaleMedium.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 20;
            } else if (this.petalScaleLarge.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 30;
            } else if (this.petalScaleHuge.Down) {
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].scaleAtFullSize = 60;
            }
        }
        if (this.petalColor.Visible) {
            this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].faceColor = this.petalColor.Color;
            this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].backfaceColor = usupport.darkerColor(this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].faceColor);
            this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kBud].faceColor = this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].faceColor;
            this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kBud].backfaceColor = this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].backfaceColor;
        }
        if (this.petalTdosDraw.Visible) {
            tdo = this.tdoForIndex(this.petalTdosDraw.Selection.left);
            if ((tdo != null) && (this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].object3D != null)) {
                // cfk first petals again
                this.plant.pFlower[uplant.kGenderFemale].tdoParams[uplant.kFirstPetals].object3D.copyFrom(tdo);
            }
        }
    }
    
    public void finishForFruit() {
        KfObject3D tdo = new KfObject3D();
        
        if (!this.plantHasInflorescences) {
            return;
        }
        if (this.showFruitsNo.Enabled) {
            if (this.showFruitsNo.Checked) {
                this.plant.pFlower[uplant.kGenderFemale].minDaysBeforeSettingFruit = 200;
            } else {
                this.plant.pFlower[uplant.kGenderFemale].minDaysBeforeSettingFruit = 3;
            }
        }
        if (this.fruitSectionsOne.Enabled) {
            if (this.fruitSectionsOne.Down) {
                // num sections 
                this.plant.pFruit.tdoParams.repetitions = 1;
            } else if (this.fruitSectionsThree.Down) {
                this.plant.pFruit.tdoParams.repetitions = 3;
            } else if (this.fruitSectionsFour.Down) {
                this.plant.pFruit.tdoParams.repetitions = 4;
            } else if (this.fruitSectionsFive.Down) {
                this.plant.pFruit.tdoParams.repetitions = 5;
            } else if (this.fruitSectionsTen.Down) {
                this.plant.pFruit.tdoParams.repetitions = 10;
            }
        }
        if (this.fruitScaleTiny.Enabled) {
            if (this.fruitScaleTiny.Down) {
                // scale 
                this.plant.pFruit.tdoParams.scaleAtFullSize = 4;
            } else if (this.fruitScaleSmall.Down) {
                this.plant.pFruit.tdoParams.scaleAtFullSize = 10;
            } else if (this.fruitScaleMedium.Down) {
                this.plant.pFruit.tdoParams.scaleAtFullSize = 20;
            } else if (this.fruitScaleLarge.Down) {
                this.plant.pFruit.tdoParams.scaleAtFullSize = 30;
            } else if (this.fruitScaleHuge.Down) {
                this.plant.pFruit.tdoParams.scaleAtFullSize = 60;
            }
        }
        if (this.fruitColor.Visible) {
            this.plant.pFruit.tdoParams.faceColor = this.fruitColor.Color;
            this.plant.pFruit.tdoParams.backfaceColor = usupport.darkerColor(this.plant.pFruit.tdoParams.faceColor);
            this.plant.pFruit.tdoParams.alternateFaceColor = this.plant.pFruit.tdoParams.faceColor;
            this.plant.pFruit.tdoParams.alternateBackfaceColor = this.plant.pFruit.tdoParams.backfaceColor;
        }
        if (this.sectionTdosDraw.Visible) {
            tdo = this.tdoForIndex(this.sectionTdosDraw.Selection.left);
            if ((tdo != null) && (this.plant.pFruit.tdoParams.object3D != null)) {
                this.plant.pFruit.tdoParams.object3D.copyFrom(tdo);
            }
        }
    }
    
    // ------------------------------------------------------------------------------------------- *preview 
    public void drawPreview(boolean reloadVariables) {
        if (this.plant == null) {
            return;
        }
        if (reloadVariables) {
            this.setPlantVariables();
        }
        try {
            // always update cache in case any params have changed 
            UNRESOLVED.cursor_startWait;
            // want nice drawing here, only case
            this.plant.useBestDrawingForPreview = true;
            this.plant.drawPreviewIntoCache(Point(this.previewPaintBox.Width, this.previewPaintBox.Height), uplant.kDontConsiderDomainScale, umain.kDrawNow);
            this.plant.previewCache.Transparent = false;
        } finally {
            UNRESOLVED.cursor_stopWait;
        }
        this.previewPaintBox.Invalidate();
    }
    
    public void previewPaintBoxPaint(TObject Sender) {
        if ((this.plant != null) && (this.plant.previewCache != null)) {
            UNRESOLVED.copyBitmapToCanvasWithGlobalPalette(this.plant.previewCache, this.previewPaintBox.Canvas, Rect(0, 0, 0, 0));
        }
    }
    
    public void randomizePlantClick(TObject Sender) {
        this.plant.randomize();
        this.drawPreview(kDontReloadVariables);
    }
    
    public void turnLeftClick(TObject Sender) {
        if (this.plant == null) {
            return;
        }
        this.plant.xRotation = this.plant.xRotation - 10;
        if (this.plant.xRotation < -360) {
            this.plant.xRotation = 360;
        }
        this.drawPreview(kDontReloadVariables);
    }
    
    public void turnRightClick(TObject Sender) {
        if (this.plant == null) {
            return;
        }
        this.plant.xRotation = this.plant.xRotation + 10;
        if (this.plant.xRotation > 360) {
            this.plant.xRotation = -360;
        }
        this.drawPreview(kDontReloadVariables);
    }
    
    // -------------------------------------------------------------------------------------------- buttons/notebook 
    public void setPageIndex(short newIndex) {
        this.wizardNotebook.PageIndex = newIndex;
    }
    
    public void backClick(TObject Sender) {
        if (this.wizardNotebook.PageIndex > 0) {
            if (this.wizardNotebook.PageIndex == kFinish) {
                if (this.plantHasInflorescences) {
                    this.setPageIndex(kFruit);
                } else {
                    this.setPageIndex(kInflorescencesPlacement);
                }
            } else {
                this.setPageIndex(this.wizardNotebook.PageIndex - 1);
            }
        }
        this.updateProgress();
    }
    
    public void nextClick(TObject Sender) {
        if (this.wizardNotebook.PageIndex < kLastPanel) {
            if (this.wizardNotebook.PageIndex == kInflorescencesPlacement) {
                if (this.plantHasInflorescences) {
                    this.setPageIndex(kInflorescences);
                } else {
                    this.setPageIndex(kFinish);
                }
            } else {
                this.setPageIndex(this.wizardNotebook.PageIndex + 1);
            }
            this.updateProgress();
        } else {
            this.setPlantVariables();
            this.saveOptionsToDomain();
            this.plant.shrinkPreviewCache();
            UNRESOLVED.modalResult = mrOK;
        }
    }
    
    public void cancelClick(TObject Sender) {
        UNRESOLVED.modalResult = mrCancel;
    }
    
    public void FormClose(TObject Sender, TCloseAction Action) {
        int response = 0;
        
        if ((this.optionsHaveChanged()) && (UNRESOLVED.modalResult == mrCancel)) {
            // same as cancel, but if they click cancel on dialog, we must change action
            response = MessageDialog("Do you want to save the changes you made" + chr(13) + "to the wizard options?", mtConfirmation, {mbYes, mbNo, mbCancel, }, 0);
            switch (response) {
                case delphi_compatability.IDYES:
                    this.saveOptionsToDomain();
                    Action = delphi_compatability.TCloseAction.caFree;
                    break;
                case delphi_compatability.IDNO:
                    Action = delphi_compatability.TCloseAction.caFree;
                    break;
                case delphi_compatability.IDCANCEL:
                    Action = delphi_compatability.TCloseAction.caNone;
                    break;
        }
    }
    
    public void updateProgress() {
        this.progressDrawGrid.Invalidate();
        this.progressDrawGrid.Refresh();
        if (this.wizardNotebook.PageIndex == kLastPanel) {
            this.previewPaintBox.Visible = false;
            delphi_compatability.Application.ProcessMessages();
            this.drawPreview(kReloadVariables);
            this.previewPaintBox.Visible = true;
        }
    }
    
    public void progressDrawGridDrawCell(TObject Sender, long Col, long Row, TRect Rect, TGridDrawState State) {
        TBitmap bitmap = new TBitmap();
        TRect bitmapRect = new TRect();
        
        // need this to make bitmaps come on as transparent
        this.progressDrawGrid.Canvas.Brush.Color = UNRESOLVED.clBtnFace;
        this.progressDrawGrid.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear;
        this.progressDrawGrid.Canvas.FillRect(Rect);
        bitmap = this.bitmapForProgressPage(Col);
        bitmapRect.Left = Rect.left + usupport.rWidth(Rect) / 2 - bitmap.Width / 2;
        bitmapRect.Right = bitmapRect.Left + bitmap.Width;
        bitmapRect.Top = Rect.top + usupport.rHeight(Rect) / 2 - bitmap.Height / 2;
        bitmapRect.Bottom = bitmapRect.Top + bitmap.Height;
        if (bitmap != null) {
            this.progressDrawGrid.Canvas.Draw(bitmapRect.Left, bitmapRect.Top, bitmap);
        }
        if (Col == this.wizardNotebook.PageIndex) {
            this.progressDrawGrid.Canvas.Pen.Color = delphi_compatability.clRed;
            this.progressDrawGrid.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid;
            this.progressDrawGrid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
            //FIX unresolved WITH expression: Rect
            this.progressDrawGrid.Canvas.Rectangle(UNRESOLVED.left, UNRESOLVED.top, UNRESOLVED.right, UNRESOLVED.bottom);
        }
    }
    
    public TBitmap bitmapForProgressPage(short page) {
        result = new TBitmap();
        result = null;
        switch (page) {
            case kStart:
                result = this.startPageImage.Picture.Bitmap;
                break;
            case kMeristems:
                result = this.meristemsPageImage.Picture.Bitmap;
                break;
            case kInternodes:
                result = this.internodesPageImage.Picture.Bitmap;
                break;
            case kLeaves:
                result = this.leavesPageImage.Picture.Bitmap;
                break;
            case kCompoundLeaves:
                result = this.compoundLeavesPageImage.Picture.Bitmap;
                break;
            case kInflorescencesPlacement:
                result = this.inflorPlacePageImage.Picture.Bitmap;
                break;
            case kInflorescences:
                if (this.plantHasInflorescences) {
                    result = this.inflorDrawPageImage.Picture.Bitmap;
                } else {
                    result = this.inflorDrawPageImageDisabled.Picture.Bitmap;
                }
                break;
            case kFlowers:
                if (this.plantHasInflorescences) {
                    result = this.flowersPageImage.Picture.Bitmap;
                } else {
                    result = this.flowersPageImageDisabled.Picture.Bitmap;
                }
                break;
            case kFruit:
                if (this.plantHasInflorescences) {
                    result = this.fruitsPageImage.Picture.Bitmap;
                } else {
                    result = this.fruitsPageImageDisabled.Picture.Bitmap;
                }
                break;
            case kFinish:
                result = this.finishPageImage.Picture.Bitmap;
                break;
        return result;
    }
    
    public void progressDrawGridSelectCell(TObject Sender, long Col, long Row, boolean CanSelect) {
        if (((Col == kInflorescences) || (Col == kFlowers) || (Col == kFruit)) && (!this.plantHasInflorescences)) {
            CanSelect = false;
        } else {
            this.setPageIndex(Col);
            this.updateProgress();
        }
        return CanSelect;
    }
    
    public void wizardNotebookPageChanged(TObject Sender) {
        switch (this.wizardNotebook.PageIndex) {
            case 0:
                this.back.Enabled = false;
                this.next.Enabled = true;
                this.next.Caption = "&Next >";
                break;
            case kLastPanel:
                this.back.Enabled = true;
                this.next.Caption = "&Finish";
                break;
            default:
                this.back.Enabled = true;
                this.next.Enabled = true;
                this.next.Caption = "&Next >";
                break;
    }
    
    public void petalColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.petalColor.Color = udomain.domain.getColorUsingCustomColors(this.petalColor.Color);
    }
    
    public void fruitColorMouseUp(TObject Sender, TMouseButton Button, TShiftState Shift, int X, int Y) {
        this.fruitColor.Color = udomain.domain.getColorUsingCustomColors(this.fruitColor.Color);
    }
    
    public void leafTdosDrawSelectCell(TObject Sender, int Col, int Row, boolean CanSelect) {
        if ((Col != this.leafTdosDraw.Selection.left)) {
            this.tdoSelectionChanged = true;
            this.showTdoNameInLabel(Col, this.leafTdoSelectedLabel);
        }
        return CanSelect;
    }
    
    public void petalTdosDrawSelectCell(TObject Sender, int Col, int Row, boolean CanSelect) {
        if ((Col != this.petalTdosDraw.Selection.left)) {
            this.tdoSelectionChanged = true;
            this.showTdoNameInLabel(Col, this.petalTdoSelectedLabel);
        }
        return CanSelect;
    }
    
    public void sectionTdosDrawSelectCell(TObject Sender, int Col, int Row, boolean CanSelect) {
        if ((Col != this.sectionTdosDraw.Selection.left)) {
            this.tdoSelectionChanged = true;
            this.showTdoNameInLabel(Col, this.sectionTdoSelectedLabel);
        }
        return CanSelect;
    }
    
    public void sectionTdosDrawMouseMove(TObject Sender, TShiftState Shift, int X, int Y) {
        pass
        //var col, row: integer;
        //sectionTdosDraw.mouseToCell(x, y, col, row);
        //if (col <> sectionTdosDraw.selection.left) then
        //  self.showTdoNameInLabel(col, sectionTdoSelectedLabel);
    }
    
    public void showTdoNameInLabel(short index, TLabel aLabel) {
        KfObject3D tdo = new KfObject3D();
        
        tdo = null;
        if ((index >= 0) && (index <= this.tdos.Count - 1)) {
            tdo = utdo.KfObject3D(this.tdos.Items[index]);
        }
        if (tdo != null) {
            aLabel.Caption = tdo.getName();
        } else {
            aLabel.Caption = "";
        }
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Making_a_new_plant_with_the_wizard");
    }
    
    public void FormKeyPress(TObject Sender, char Key) {
        Key = usupport.makeEnterWorkAsTab(this, UNRESOLVED.activeControl, Key);
        return Key;
    }
    
}
