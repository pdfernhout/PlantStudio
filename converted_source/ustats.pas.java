// unit Ustats

from conversion_common import *;
import ubmpsupport;
import uppanel;
import delphi_compatability;

// const
kLive = 0;
kDead = 1;
kBothLiveAndDead = 2;


// const
kMinGraphWidth = 50;



class PdStatsPanel extends PdParameterPanel {
    public TBitmap drawBitmap;
    public PdPlantStatistics statistics;
    public TRect graphRect;
    public TRect percentRect;
    public  labelRects;
    public short maxLabelWidth;
    
    public void create(TComponent anOwner) {
        super.create(anOwner);
        this.plant = null;
        this.PopupMenu = null;
        this.drawBitmap = delphi_compatability.TBitmap().Create();
        this.statistics = UNRESOLVED.PdPlantStatistics.create;
        this.ParentFont = true;
        this.OnMouseUp = this.doMouseUp;
        this.OnKeyDown = this.doKeyDown;
        this.TabStop = true;
        this.Enabled = true;
        this.selectedItemIndex = uppanel.kItemNone;
        this.BevelInner = UNRESOLVED.bvNone;
        this.BevelOuter = UNRESOLVED.bvNone;
        this.updateHint();
    }
    
    public void updateHint() {
        if (UNRESOLVED.domain.options.showLongHintsForButtons) {
            this.Hint = "Parts of the plant showing counts and percent of total biomass taken up by" + " each plant part. You can't change anything here; it is for display only." + " See the help system for details.";
        } else {
            this.Hint = "";
        }
        this.ShowHint = true;
    }
    
    public void destroy() {
        this.drawBitmap.free;
        this.drawBitmap = null;
        this.statistics.free;
        this.statistics = null;
        super.destroy();
    }
    
    public int maxSelectedItemIndex() {
        result = 0;
        result = uppanel.kItemNone;
        return result;
    }
    
    public int collapsedHeight() {
        result = 0;
        result = this.textHeight + uppanel.kTopBottomGap;
        return result;
    }
    
    public void collapseOrExpand(int y) {
        pass
        // do nothing 
    }
    
    public void updatePlant(PdPlant newPlant) {
        if (this.plant != newPlant) {
            this.plant = newPlant;
            this.updateCurrentValue(0);
        }
    }
    
    public void updatePlantValues() {
        this.updateCurrentValue(0);
        // NOT refresh 
        this.Repaint();
    }
    
    public void updateCurrentValue() {
        this.statistics.zeroAllFields;
        this.Enabled = false;
        if (this.plant == null) {
            return;
        }
        this.plant.getPlantStatistics(this.statistics);
        this.Enabled = true;
        this.updateDisplay();
    }
    
    public void updateDisplay() {
        if (this.plant == null) {
            return;
        }
        this.Invalidate();
    }
    
    public void resizeElements() {
        TRect fullRect = new TRect();
        
        if (this.textHeight == 0) {
            this.calculateTextDimensions();
        }
        if (this.maxLabelWidth == 0) {
            this.paint();
        }
        fullRect = Rect(0, 0, kMinGraphWidth + this.maxLabelWidth + uppanel.kLeftRightGap * 2 + uppanel.kBetweenGap, (this.numNonZeroPlantParts() + 2) * this.textHeight + uppanel.kTopBottomGap * 2 + uppanel.kBetweenGap * 2);
        this.ClientHeight = UNRESOLVED.intMax(0, UNRESOLVED.intMax(UNRESOLVED.rHeight(fullRect), this.Parent.ClientHeight));
        this.ClientWidth = UNRESOLVED.intMax(0, UNRESOLVED.intMax(UNRESOLVED.rWidth(fullRect), this.Parent.ClientWidth));
        try {
            this.drawBitmap.Width = this.ClientWidth;
            this.drawBitmap.Height = this.ClientHeight;
        } catch (Exception e) {
            this.drawBitmap.Width = 1;
            this.drawBitmap.Height = 1;
        }
        this.updateDisplay();
    }
    
    public String labelStringForPartType(short index) {
        result = "";
        short partType = 0;
        boolean hasStuff = false;
        
        result = "";
        //FIX unresolved WITH expression: self.statistics
        partType = this.partTypeForIndex(index);
        //FIX unresolved WITH expression: self.statistics
        hasStuff = (UNRESOLVED.liveBiomass_pctMPB[partType] + UNRESOLVED.deadBiomass_pctMPB[partType] > 0) || (UNRESOLVED.count[partType] > 0);
        if (!hasStuff) {
            return result;
        }
        if (UNRESOLVED.count[partType] > 0) {
            result = IntToStr(UNRESOLVED.count[partType]) + " ";
        }
        result = result + this.nameForPartType(partType, UNRESOLVED.count[partType] == 1);
        result = result + ": " + UNRESOLVED.digitValueString(this.displayPercentForPartType(partType, kBothLiveAndDead)) + "%";
        return result;
    }
    
    public float displayPercentForPartType(short partType, short livingDeadOrBoth) {
        result = 0.0;
        float total_pctMPB = 0.0;
        
        result = 0.0;
        total_pctMPB = this.statistics.liveBiomass_pctMPB[UNRESOLVED.kStatisticsPartTypeAllVegetative] + this.statistics.deadBiomass_pctMPB[UNRESOLVED.kStatisticsPartTypeAllVegetative] + this.statistics.liveBiomass_pctMPB[UNRESOLVED.kStatisticsPartTypeAllReproductive] + this.statistics.deadBiomass_pctMPB[UNRESOLVED.kStatisticsPartTypeAllReproductive];
        if (total_pctMPB == 0.0) {
            return result;
        }
        switch (livingDeadOrBoth) {
            case kLive:
                result = this.statistics.liveBiomass_pctMPB[partType];
                break;
            case kDead:
                result = this.statistics.deadBiomass_pctMPB[partType];
                break;
            case kBothLiveAndDead:
                result = this.statistics.liveBiomass_pctMPB[partType] + this.statistics.deadBiomass_pctMPB[partType];
                break;
        result = UNRESOLVED.min(100.0, UNRESOLVED.max(0.0, 100.0 * result / total_pctMPB));
        return result;
    }
    
    public short numNonZeroPlantParts() {
        result = 0;
        short i = 0;
        short partType = 0;
        boolean hasStuff = false;
        
        result = 0;
        for (i = 0; i <= UNRESOLVED.kStatisticsPartTypeLast; i++) {
            partType = this.partTypeForIndex(i);
            //FIX unresolved WITH expression: self.statistics
            hasStuff = (UNRESOLVED.liveBiomass_pctMPB[partType] + UNRESOLVED.deadBiomass_pctMPB[partType] > 0) || (UNRESOLVED.count[partType] > 0);
            if (hasStuff) {
                result += 1;
            }
        }
        return result;
    }
    
    public void paint() {
        TRect fullRect = new TRect();
        TRect minRect = new TRect();
        TRect maxRect = new TRect();
        String minText = "";
        String maxText = "";
        String percentText = "";
        short i = 0;
        short partType = 0;
        short topPos = 0;
         labelTexts = [0] * (range(0, UNRESOLVED.kStatisticsPartTypeLast + 1) + 1);
        boolean hasStuff = false;
        
        fullRect = this.GetClientRect();
        this.Canvas.Font = this.Font;
        if (this.textHeight == 0) {
            this.calculateTextDimensions();
        }
        if (this.plant != null) {
            // v2.0 + ' (% of total)'
            percentText = "Statistics for " + this.plant.getName;
        } else {
            // v2.0
            percentText = "(no plants selected)";
        }
        this.percentRect.Top = fullRect.Top + uppanel.kTopBottomGap;
        this.percentRect.Bottom = this.percentRect.Top + this.textHeight;
        this.percentRect.Left = fullRect.Left + uppanel.kLeftRightGap;
        // v2.0 bold font
        this.Canvas.Font.Style = {UNRESOLVED.fsBold, };
        this.percentRect.Right = this.percentRect.Left + this.Canvas.TextWidth(percentText);
        this.Canvas.Font.Style = {};
        for (i = 0; i <= UNRESOLVED.kStatisticsPartTypeLast; i++) {
            labelTexts[i] = this.labelStringForPartType(i);
        }
        topPos = this.percentRect.Bottom + uppanel.kBetweenGap;
        this.maxLabelWidth = 0;
        for (i = 0; i <= UNRESOLVED.kStatisticsPartTypeLast; i++) {
            this.labelRects[i] = Rect(0, 0, 0, 0);
        }
        for (i = 0; i <= UNRESOLVED.kStatisticsPartTypeLast; i++) {
            this.labelRects[i].Left = uppanel.kLeftRightGap;
            this.labelRects[i].Right = this.labelRects[i].Left + this.Canvas.TextWidth(labelTexts[i]);
            if (this.labelRects[i].Right - this.labelRects[i].Left > this.maxLabelWidth) {
                this.maxLabelWidth = this.labelRects[i].Right - this.labelRects[i].Left;
            }
            this.labelRects[i].Top = topPos;
            if (labelTexts[i] == "") {
                this.labelRects[i].Bottom = this.labelRects[i].Top;
            } else {
                this.labelRects[i].Bottom = this.labelRects[i].Top + this.textHeight;
            }
            topPos = topPos + (this.labelRects[i].Bottom - this.labelRects[i].Top);
            if (this.labelRects[i].Right - this.labelRects[i].Left > this.maxLabelWidth) {
                this.maxLabelWidth = this.labelRects[i].Right - this.labelRects[i].Left;
            }
        }
        for (i = 0; i <= UNRESOLVED.kStatisticsPartTypeLast; i++) {
            // set all label widths equal to largest, so can right-justify them 
            this.labelRects[i].Right = this.labelRects[i].Left + this.maxLabelWidth;
        }
        this.graphRect.Left = uppanel.kLeftRightGap + this.maxLabelWidth + uppanel.kBetweenGap;
        this.graphRect.Right = fullRect.Right - uppanel.kLeftRightGap;
        this.graphRect.Top = this.percentRect.Bottom + uppanel.kBetweenGap;
        this.graphRect.Bottom = fullRect.Bottom - uppanel.kTopBottomGap - this.textHeight - uppanel.kBetweenGap;
        minText = "0";
        minRect.Left = this.graphRect.Left;
        minRect.Right = minRect.Left + this.Canvas.TextWidth(minText);
        minRect.Top = this.graphRect.Bottom;
        minRect.Bottom = minRect.Top + this.textHeight;
        maxText = "100 %";
        maxRect = minRect;
        maxRect.Right = this.graphRect.Right;
        maxRect.Left = maxRect.Right - this.Canvas.TextWidth(maxText);
        this.drawBitmap.Canvas.Brush.Color = UNRESOLVED.clBtnFace;
        // v1.4
        this.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnFace;
        this.drawBitmap.Canvas.Rectangle(0, 0, this.drawBitmap.Width, this.drawBitmap.Height);
        for (i = 0; i <= UNRESOLVED.kStatisticsPartTypeLast; i++) {
            if (this.labelRects[i].Bottom <= this.graphRect.Bottom) {
                //FIX unresolved WITH expression: self.statistics
                partType = this.partTypeForIndex(i);
                hasStuff = (UNRESOLVED.liveBiomass_pctMPB[partType] + UNRESOLVED.deadBiomass_pctMPB[partType] > 0) || (UNRESOLVED.count[partType] > 0);
                this.drawTextLabel(labelTexts[i], this.labelRects[i], hasStuff, false, false);
            }
        }
        if (this.plant != null) {
            this.drawGraph();
        }
        this.drawBitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
        if (this.plant != null) {
            this.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnText;
        } else {
            this.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnFace;
        }
        this.drawBitmap.Canvas.Rectangle(this.graphRect.Left, this.graphRect.Top, this.graphRect.Right, this.graphRect.Bottom);
        // v2.0 top label in bold
        this.Canvas.Font.Style = {UNRESOLVED.fsBold, };
        this.drawTextLabel(percentText, this.percentRect, (this.plant != null), false, false);
        this.Canvas.Font.Style = {};
        if (this.plant != null) {
            this.drawTextLabel(minText, minRect, true, false, false);
            this.drawTextLabel(maxText, maxRect, true, false, false);
        }
        if (this.drawBitmap.Width > 0) {
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(this.drawBitmap, this.Canvas, Rect(0, 0, 0, 0));
        }
    }
    
    public void drawTextLabel(String text, TRect drawRect, boolean active, boolean drawLine, boolean drawBox) {
         cText = [0] * (range(0, 255 + 1) + 1);
        
        if (text != "") {
            this.drawBitmap.Canvas.Font = this.Font;
            if (active) {
                this.drawBitmap.Canvas.Font.Color = UNRESOLVED.clBtnText;
            } else {
                this.drawBitmap.Canvas.Font.Color = UNRESOLVED.clBtnShadow;
            }
            UNRESOLVED.strPCopy(cText, text);
            // changed DT_LEFT to DT_RIGHT to right-justify labels; ok because nothing else matters here 
            UNRESOLVED.winprocs.drawText(this.drawBitmap.Canvas.Handle, cText, len(cText), drawRect, delphi_compatability.DT_RIGHT);
        }
        if (drawLine) {
            this.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
            this.drawBitmap.Canvas.MoveTo(drawRect.Left, drawRect.Bottom - 2);
            this.drawBitmap.Canvas.LineTo(drawRect.Right, drawRect.Bottom - 2);
        }
        if (drawBox) {
            this.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnShadow;
            this.drawBitmap.Canvas.MoveTo(drawRect.Right + 2, drawRect.Top);
            this.drawBitmap.Canvas.LineTo(drawRect.Left - 2, drawRect.Top);
            this.drawBitmap.Canvas.LineTo(drawRect.Left - 2, drawRect.Bottom - 2);
            this.drawBitmap.Canvas.LineTo(drawRect.Right + 2, drawRect.Bottom - 2);
            this.drawBitmap.Canvas.LineTo(drawRect.Right + 2, drawRect.Top);
        }
    }
    
    public void drawGraph() {
        long i = 0;
        long partType = 0;
        
        this.drawBitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid;
        this.drawBitmap.Canvas.Pen.Color = delphi_compatability.clBlack;
        this.drawBitmap.Canvas.Pen.Width = 1;
        this.drawBitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid;
        for (i = 0; i <= UNRESOLVED.kStatisticsPartTypeLast; i++) {
            if (this.labelRects[i].Bottom <= this.graphRect.Bottom) {
                partType = this.partTypeForIndex(i);
                // first draw all biomass 
                this.drawBitmap.Canvas.Brush.Color = delphi_compatability.clBlack;
                this.drawBar(i, this.displayPercentForPartType(partType, kDead));
                // next draw only live biomass 
                this.drawBitmap.Canvas.Brush.Color = delphi_compatability.clLime;
                this.drawBar(i, this.displayPercentForPartType(partType, kLive));
            }
        }
        this.drawBitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
    }
    
    public void drawBar(int index, float amount_pctMPB) {
        long distance = 0;
        TRect drawRect = new TRect();
        
        distance = this.graphRect.Left + intround(amount_pctMPB / 100.0 * (this.graphRect.Right - this.graphRect.Left));
        drawRect = Rect(this.graphRect.Left, this.labelRects[index].Top, distance, this.labelRects[index].Bottom);
        this.drawBitmap.Canvas.Rectangle(drawRect.Left, drawRect.Top, drawRect.Right, drawRect.Bottom);
    }
    
    public String nameForPartType(short partType, boolean isSingular) {
        result = "";
        result = "";
        switch (partType) {
            case UNRESOLVED.kStatisticsPartTypeSeedlingLeaf:
                if (isSingular) {
                    result = "seedling leaf";
                } else {
                    result = "seedling leaves";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeLeaf:
                if (isSingular) {
                    result = "leaf";
                } else {
                    result = "leaves";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeFemaleInflorescence:
                if (isSingular) {
                    result = "primary inflorescence";
                } else {
                    result = "primary inflorescences";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeMaleInflorescence:
                if (isSingular) {
                    result = "secondary inflorescence";
                } else {
                    result = "secondary inflorescences";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeFemaleFlower:
                if (isSingular) {
                    result = "primary flower";
                } else {
                    result = "primary flowers";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeFemaleFlowerBud:
                if (isSingular) {
                    result = "primary flower bud";
                } else {
                    result = "primary flower buds";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeMaleFlower:
                if (isSingular) {
                    result = "secondary flower";
                } else {
                    result = "secondary flowers";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeMaleFlowerBud:
                if (isSingular) {
                    result = "secondary flower bud";
                } else {
                    result = "secondary flower buds";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeAxillaryBud:
                if (isSingular) {
                    result = "meristem";
                } else {
                    result = "meristems";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeFruit:
                if (isSingular) {
                    result = "ripe fruit";
                } else {
                    result = "ripe fruits";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeStem:
                if (isSingular) {
                    result = "stem internode";
                } else {
                    result = "stem internodes";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeUnripeFruit:
                if (isSingular) {
                    result = "unripe fruit";
                } else {
                    result = "unripe fruits";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeFallenFruit:
                if (isSingular) {
                    result = "fallen fruit";
                } else {
                    result = "fallen fruits";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeUnallocatedNewVegetativeBiomass:
                result = "unallocated vegetative";
                break;
            case UNRESOLVED.kStatisticsPartTypeUnremovedDeadVegetativeBiomass:
                result = "unremoved vegetative";
                break;
            case UNRESOLVED.kStatisticsPartTypeUnallocatedNewReproductiveBiomass:
                result = "unallocated reproductive";
                break;
            case UNRESOLVED.kStatisticsPartTypeUnremovedDeadReproductiveBiomass:
                result = "unremoved reproductive";
                break;
            case UNRESOLVED.kStatisticsPartTypeFallenFlower:
                if (isSingular) {
                    result = "fallen flower";
                } else {
                    result = "fallen flowers";
                }
                break;
            case UNRESOLVED.kStatisticsPartTypeAllVegetative:
                result = "vegetative parts";
                break;
            case UNRESOLVED.kStatisticsPartTypeAllReproductive:
                result = "reproductive parts";
                break;
            default:
                result = "";
                break;
        return result;
    }
    
    public short partTypeForIndex(short partType) {
        result = 0;
        result = -1;
        switch (partType) {
            case 0:
                result = UNRESOLVED.kStatisticsPartTypeAllVegetative;
                break;
            case 1:
                result = UNRESOLVED.kStatisticsPartTypeAllReproductive;
                break;
            case 2:
                result = UNRESOLVED.kStatisticsPartTypeAxillaryBud;
                break;
            case 3:
                result = UNRESOLVED.kStatisticsPartTypeStem;
                break;
            case 4:
                result = UNRESOLVED.kStatisticsPartTypeSeedlingLeaf;
                break;
            case 5:
                result = UNRESOLVED.kStatisticsPartTypeLeaf;
                break;
            case 6:
                result = UNRESOLVED.kStatisticsPartTypeFemaleInflorescence;
                break;
            case 7:
                result = UNRESOLVED.kStatisticsPartTypeFemaleFlowerBud;
                break;
            case 8:
                result = UNRESOLVED.kStatisticsPartTypeFemaleFlower;
                break;
            case 9:
                result = UNRESOLVED.kStatisticsPartTypeMaleInflorescence;
                break;
            case 10:
                result = UNRESOLVED.kStatisticsPartTypeMaleFlowerBud;
                break;
            case 11:
                result = UNRESOLVED.kStatisticsPartTypeMaleFlower;
                break;
            case 12:
                result = UNRESOLVED.kStatisticsPartTypeFallenFlower;
                break;
            case 13:
                result = UNRESOLVED.kStatisticsPartTypeUnripeFruit;
                break;
            case 14:
                result = UNRESOLVED.kStatisticsPartTypeFruit;
                break;
            case 15:
                result = UNRESOLVED.kStatisticsPartTypeFallenFruit;
                break;
            case 16:
                result = UNRESOLVED.kStatisticsPartTypeUnallocatedNewVegetativeBiomass;
                break;
            case 17:
                result = UNRESOLVED.kStatisticsPartTypeUnremovedDeadVegetativeBiomass;
                break;
            case 18:
                result = UNRESOLVED.kStatisticsPartTypeUnallocatedNewReproductiveBiomass;
                break;
            case 19:
                result = UNRESOLVED.kStatisticsPartTypeUnremovedDeadReproductiveBiomass;
                break;
            default:
                // called by paint method, so do not raise exception 
                result = 0;
                break;
        return result;
    }
    
}
