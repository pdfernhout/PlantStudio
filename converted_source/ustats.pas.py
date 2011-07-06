# unit Ustats

from conversion_common import *
import ubmpsupport
import udomain
import umath
import usupport
import utravers
import uppanel
import uplant
import delphi_compatability

# const
kLive = 0
kDead = 1
kBothLiveAndDead = 2

# const
kMinGraphWidth = 50

class PdStatsPanel(PdParameterPanel):
    def __init__(self):
        self.drawBitmap = TBitmap()
        self.statistics = PdPlantStatistics()
        self.graphRect = TRect()
        self.percentRect = TRect()
        self.labelRects = [0] * (range(0, utravers.kStatisticsPartTypeLast + 1) + 1)
        self.maxLabelWidth = 0
    
    def create(self, anOwner):
        PdParameterPanel.create(self, anOwner)
        self.plant = None
        self.PopupMenu = None
        self.drawBitmap = delphi_compatability.TBitmap().Create()
        self.statistics = utravers.PdPlantStatistics.create
        self.ParentFont = true
        self.OnMouseUp = self.doMouseUp
        self.OnKeyDown = self.doKeyDown
        self.TabStop = true
        self.Enabled = true
        self.selectedItemIndex = uppanel.kItemNone
        self.BevelInner = UNRESOLVED.bvNone
        self.BevelOuter = UNRESOLVED.bvNone
        self.updateHint()
        return self
    
    def updateHint(self):
        if udomain.domain.options.showLongHintsForButtons:
            self.Hint = "Parts of the plant showing counts and percent of total biomass taken up by" + " each plant part. You can't change anything here; it is for display only." + " See the help system for details."
        else:
            self.Hint = ""
        self.ShowHint = true
    
    def destroy(self):
        self.drawBitmap.free
        self.drawBitmap = None
        self.statistics.free
        self.statistics = None
        PdParameterPanel.destroy(self)
    
    def maxSelectedItemIndex(self):
        result = 0
        result = uppanel.kItemNone
        return result
    
    def collapsedHeight(self):
        result = 0
        result = self.textHeight + uppanel.kTopBottomGap
        return result
    
    def collapseOrExpand(self, y):
        pass
        # do nothing 
    
    def updatePlant(self, newPlant):
        if self.plant != newPlant:
            self.plant = newPlant
            self.updateCurrentValue(0)
    
    def updatePlantValues(self):
        self.updateCurrentValue(0)
        # NOT refresh 
        self.Repaint()
    
    def updateCurrentValue(self):
        self.statistics.zeroAllFields()
        self.Enabled = false
        if self.plant == None:
            return
        self.plant.getPlantStatistics(self.statistics)
        self.Enabled = true
        self.updateDisplay()
    
    def updateDisplay(self):
        if self.plant == None:
            return
        self.Invalidate()
    
    def resizeElements(self):
        fullRect = TRect()
        
        if self.textHeight == 0:
            self.calculateTextDimensions()
        if self.maxLabelWidth == 0:
            self.paint()
        fullRect = Rect(0, 0, kMinGraphWidth + self.maxLabelWidth + uppanel.kLeftRightGap * 2 + uppanel.kBetweenGap, (self.numNonZeroPlantParts() + 2) * self.textHeight + uppanel.kTopBottomGap * 2 + uppanel.kBetweenGap * 2)
        self.ClientHeight = umath.intMax(0, umath.intMax(usupport.rHeight(fullRect), self.Parent.ClientHeight))
        self.ClientWidth = umath.intMax(0, umath.intMax(usupport.rWidth(fullRect), self.Parent.ClientWidth))
        try:
            self.drawBitmap.Width = self.ClientWidth
            self.drawBitmap.Height = self.ClientHeight
        except:
            self.drawBitmap.Width = 1
            self.drawBitmap.Height = 1
        self.updateDisplay()
    
    def labelStringForPartType(self, index):
        result = ""
        partType = 0
        hasStuff = false
        
        result = ""
        partType = self.partTypeForIndex(index)
        hasStuff = (self.statistics.liveBiomass_pctMPB[partType] + self.statistics.deadBiomass_pctMPB[partType] > 0) or (self.statistics.count[partType] > 0)
        if not hasStuff:
            return result
        if self.statistics.count[partType] > 0:
            result = IntToStr(self.statistics.count[partType]) + " "
        result = result + self.nameForPartType(partType, self.statistics.count[partType] == 1)
        result = result + ": " + usupport.digitValueString(self.displayPercentForPartType(partType, kBothLiveAndDead)) + "%"
        return result
    
    def displayPercentForPartType(self, partType, livingDeadOrBoth):
        result = 0.0
        total_pctMPB = 0.0
        
        result = 0.0
        total_pctMPB = self.statistics.liveBiomass_pctMPB[utravers.kStatisticsPartTypeAllVegetative] + self.statistics.deadBiomass_pctMPB[utravers.kStatisticsPartTypeAllVegetative] + self.statistics.liveBiomass_pctMPB[utravers.kStatisticsPartTypeAllReproductive] + self.statistics.deadBiomass_pctMPB[utravers.kStatisticsPartTypeAllReproductive]
        if total_pctMPB == 0.0:
            return result
        if livingDeadOrBoth == kLive:
            result = self.statistics.liveBiomass_pctMPB[partType]
        elif livingDeadOrBoth == kDead:
            result = self.statistics.deadBiomass_pctMPB[partType]
        elif livingDeadOrBoth == kBothLiveAndDead:
            result = self.statistics.liveBiomass_pctMPB[partType] + self.statistics.deadBiomass_pctMPB[partType]
        result = umath.min(100.0, umath.max(0.0, 100.0 * result / total_pctMPB))
        return result
    
    def numNonZeroPlantParts(self):
        result = 0
        i = 0
        partType = 0
        hasStuff = false
        
        result = 0
        for i in range(0, utravers.kStatisticsPartTypeLast + 1):
            partType = self.partTypeForIndex(i)
            hasStuff = (self.statistics.liveBiomass_pctMPB[partType] + self.statistics.deadBiomass_pctMPB[partType] > 0) or (self.statistics.count[partType] > 0)
            if hasStuff:
                result += 1
        return result
    
    def paint(self):
        fullRect = TRect()
        minRect = TRect()
        maxRect = TRect()
        minText = ""
        maxText = ""
        percentText = ""
        i = 0
        partType = 0
        topPos = 0
        labelTexts = [0] * (range(0, utravers.kStatisticsPartTypeLast + 1) + 1)
        hasStuff = false
        
        fullRect = self.GetClientRect()
        self.Canvas.Font = self.Font
        if self.textHeight == 0:
            self.calculateTextDimensions()
        if self.plant != None:
            # v2.0 + ' (% of total)'
            percentText = "Statistics for " + self.plant.getName()
        else:
            # v2.0
            percentText = "(no plants selected)"
        self.percentRect.Top = fullRect.Top + uppanel.kTopBottomGap
        self.percentRect.Bottom = self.percentRect.Top + self.textHeight
        self.percentRect.Left = fullRect.Left + uppanel.kLeftRightGap
        # v2.0 bold font
        self.Canvas.Font.Style = [UNRESOLVED.fsBold, ]
        self.percentRect.Right = self.percentRect.Left + self.Canvas.TextWidth(percentText)
        self.Canvas.Font.Style = []
        for i in range(0, utravers.kStatisticsPartTypeLast + 1):
            labelTexts[i] = self.labelStringForPartType(i)
        topPos = self.percentRect.Bottom + uppanel.kBetweenGap
        self.maxLabelWidth = 0
        for i in range(0, utravers.kStatisticsPartTypeLast + 1):
            self.labelRects[i] = Rect(0, 0, 0, 0)
        for i in range(0, utravers.kStatisticsPartTypeLast + 1):
            self.labelRects[i].Left = uppanel.kLeftRightGap
            self.labelRects[i].Right = self.labelRects[i].Left + self.Canvas.TextWidth(labelTexts[i])
            if self.labelRects[i].Right - self.labelRects[i].Left > self.maxLabelWidth:
                self.maxLabelWidth = self.labelRects[i].Right - self.labelRects[i].Left
            self.labelRects[i].Top = topPos
            if labelTexts[i] == "":
                self.labelRects[i].Bottom = self.labelRects[i].Top
            else:
                self.labelRects[i].Bottom = self.labelRects[i].Top + self.textHeight
            topPos = topPos + (self.labelRects[i].Bottom - self.labelRects[i].Top)
            if self.labelRects[i].Right - self.labelRects[i].Left > self.maxLabelWidth:
                self.maxLabelWidth = self.labelRects[i].Right - self.labelRects[i].Left
        for i in range(0, utravers.kStatisticsPartTypeLast + 1):
            # set all label widths equal to largest, so can right-justify them 
            self.labelRects[i].Right = self.labelRects[i].Left + self.maxLabelWidth
        self.graphRect.Left = uppanel.kLeftRightGap + self.maxLabelWidth + uppanel.kBetweenGap
        self.graphRect.Right = fullRect.Right - uppanel.kLeftRightGap
        self.graphRect.Top = self.percentRect.Bottom + uppanel.kBetweenGap
        self.graphRect.Bottom = fullRect.Bottom - uppanel.kTopBottomGap - self.textHeight - uppanel.kBetweenGap
        minText = "0"
        minRect.Left = self.graphRect.Left
        minRect.Right = minRect.Left + self.Canvas.TextWidth(minText)
        minRect.Top = self.graphRect.Bottom
        minRect.Bottom = minRect.Top + self.textHeight
        maxText = "100 %"
        maxRect = minRect
        maxRect.Right = self.graphRect.Right
        maxRect.Left = maxRect.Right - self.Canvas.TextWidth(maxText)
        self.drawBitmap.Canvas.Brush.Color = UNRESOLVED.clBtnFace
        # v1.4
        self.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnFace
        self.drawBitmap.Canvas.Rectangle(0, 0, self.drawBitmap.Width, self.drawBitmap.Height)
        for i in range(0, utravers.kStatisticsPartTypeLast + 1):
            if self.labelRects[i].Bottom <= self.graphRect.Bottom:
                partType = self.partTypeForIndex(i)
                hasStuff = (self.statistics.liveBiomass_pctMPB[partType] + self.statistics.deadBiomass_pctMPB[partType] > 0) or (self.statistics.count[partType] > 0)
                self.drawTextLabel(labelTexts[i], self.labelRects[i], hasStuff, false, false)
        if self.plant != None:
            self.drawGraph()
        self.drawBitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
        if self.plant != None:
            self.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnText
        else:
            self.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnFace
        self.drawBitmap.Canvas.Rectangle(self.graphRect.Left, self.graphRect.Top, self.graphRect.Right, self.graphRect.Bottom)
        # v2.0 top label in bold
        self.Canvas.Font.Style = [UNRESOLVED.fsBold, ]
        self.drawTextLabel(percentText, self.percentRect, (self.plant != None), false, false)
        self.Canvas.Font.Style = []
        if self.plant != None:
            self.drawTextLabel(minText, minRect, true, false, false)
            self.drawTextLabel(maxText, maxRect, true, false, false)
        if self.drawBitmap.Width > 0:
            ubmpsupport.copyBitmapToCanvasWithGlobalPalette(self.drawBitmap, self.Canvas, Rect(0, 0, 0, 0))
    
    def drawTextLabel(self, text, drawRect, active, drawLine, drawBox):
        cText = [0] * (range(0, 255 + 1) + 1)
        
        if text != "":
            self.drawBitmap.Canvas.Font = self.Font
            if active:
                self.drawBitmap.Canvas.Font.Color = UNRESOLVED.clBtnText
            else:
                self.drawBitmap.Canvas.Font.Color = UNRESOLVED.clBtnShadow
            UNRESOLVED.strPCopy(cText, text)
            # changed DT_LEFT to DT_RIGHT to right-justify labels; ok because nothing else matters here 
            UNRESOLVED.winprocs.drawText(self.drawBitmap.Canvas.Handle, cText, len(cText), drawRect, delphi_compatability.DT_RIGHT)
        if drawLine:
            self.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
            self.drawBitmap.Canvas.MoveTo(drawRect.Left, drawRect.Bottom - 2)
            self.drawBitmap.Canvas.LineTo(drawRect.Right, drawRect.Bottom - 2)
        if drawBox:
            self.drawBitmap.Canvas.Pen.Color = UNRESOLVED.clBtnShadow
            self.drawBitmap.Canvas.MoveTo(drawRect.Right + 2, drawRect.Top)
            self.drawBitmap.Canvas.LineTo(drawRect.Left - 2, drawRect.Top)
            self.drawBitmap.Canvas.LineTo(drawRect.Left - 2, drawRect.Bottom - 2)
            self.drawBitmap.Canvas.LineTo(drawRect.Right + 2, drawRect.Bottom - 2)
            self.drawBitmap.Canvas.LineTo(drawRect.Right + 2, drawRect.Top)
    
    def drawGraph(self):
        i = 0L
        partType = 0L
        
        self.drawBitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
        self.drawBitmap.Canvas.Pen.Color = delphi_compatability.clBlack
        self.drawBitmap.Canvas.Pen.Width = 1
        self.drawBitmap.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        for i in range(0, utravers.kStatisticsPartTypeLast + 1):
            if self.labelRects[i].Bottom <= self.graphRect.Bottom:
                partType = self.partTypeForIndex(i)
                # first draw all biomass 
                self.drawBitmap.Canvas.Brush.Color = delphi_compatability.clBlack
                self.drawBar(i, self.displayPercentForPartType(partType, kDead))
                # next draw only live biomass 
                self.drawBitmap.Canvas.Brush.Color = delphi_compatability.clLime
                self.drawBar(i, self.displayPercentForPartType(partType, kLive))
        self.drawBitmap.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear
    
    def drawBar(self, index, amount_pctMPB):
        distance = 0L
        drawRect = TRect()
        
        distance = self.graphRect.Left + intround(amount_pctMPB / 100.0 * (self.graphRect.Right - self.graphRect.Left))
        drawRect = Rect(self.graphRect.Left, self.labelRects[index].Top, distance, self.labelRects[index].Bottom)
        self.drawBitmap.Canvas.Rectangle(drawRect.Left, drawRect.Top, drawRect.Right, drawRect.Bottom)
    
    def nameForPartType(self, partType, isSingular):
        result = ""
        result = ""
        if partType == utravers.kStatisticsPartTypeSeedlingLeaf:
            if isSingular:
                result = "seedling leaf"
            else:
                result = "seedling leaves"
        elif partType == utravers.kStatisticsPartTypeLeaf:
            if isSingular:
                result = "leaf"
            else:
                result = "leaves"
        elif partType == utravers.kStatisticsPartTypeFemaleInflorescence:
            if isSingular:
                result = "primary inflorescence"
            else:
                result = "primary inflorescences"
        elif partType == utravers.kStatisticsPartTypeMaleInflorescence:
            if isSingular:
                result = "secondary inflorescence"
            else:
                result = "secondary inflorescences"
        elif partType == utravers.kStatisticsPartTypeFemaleFlower:
            if isSingular:
                result = "primary flower"
            else:
                result = "primary flowers"
        elif partType == utravers.kStatisticsPartTypeFemaleFlowerBud:
            if isSingular:
                result = "primary flower bud"
            else:
                result = "primary flower buds"
        elif partType == utravers.kStatisticsPartTypeMaleFlower:
            if isSingular:
                result = "secondary flower"
            else:
                result = "secondary flowers"
        elif partType == utravers.kStatisticsPartTypeMaleFlowerBud:
            if isSingular:
                result = "secondary flower bud"
            else:
                result = "secondary flower buds"
        elif partType == utravers.kStatisticsPartTypeAxillaryBud:
            if isSingular:
                result = "meristem"
            else:
                result = "meristems"
        elif partType == utravers.kStatisticsPartTypeFruit:
            if isSingular:
                result = "ripe fruit"
            else:
                result = "ripe fruits"
        elif partType == utravers.kStatisticsPartTypeStem:
            if isSingular:
                result = "stem internode"
            else:
                result = "stem internodes"
        elif partType == utravers.kStatisticsPartTypeUnripeFruit:
            if isSingular:
                result = "unripe fruit"
            else:
                result = "unripe fruits"
        elif partType == utravers.kStatisticsPartTypeFallenFruit:
            if isSingular:
                result = "fallen fruit"
            else:
                result = "fallen fruits"
        elif partType == utravers.kStatisticsPartTypeUnallocatedNewVegetativeBiomass:
            result = "unallocated vegetative"
        elif partType == utravers.kStatisticsPartTypeUnremovedDeadVegetativeBiomass:
            result = "unremoved vegetative"
        elif partType == utravers.kStatisticsPartTypeUnallocatedNewReproductiveBiomass:
            result = "unallocated reproductive"
        elif partType == utravers.kStatisticsPartTypeUnremovedDeadReproductiveBiomass:
            result = "unremoved reproductive"
        elif partType == utravers.kStatisticsPartTypeFallenFlower:
            if isSingular:
                result = "fallen flower"
            else:
                result = "fallen flowers"
        elif partType == utravers.kStatisticsPartTypeAllVegetative:
            result = "vegetative parts"
        elif partType == utravers.kStatisticsPartTypeAllReproductive:
            result = "reproductive parts"
        else :
            result = ""
        return result
    
    def partTypeForIndex(self, partType):
        result = 0
        result = -1
        if partType == 0:
            result = utravers.kStatisticsPartTypeAllVegetative
        elif partType == 1:
            result = utravers.kStatisticsPartTypeAllReproductive
        elif partType == 2:
            result = utravers.kStatisticsPartTypeAxillaryBud
        elif partType == 3:
            result = utravers.kStatisticsPartTypeStem
        elif partType == 4:
            result = utravers.kStatisticsPartTypeSeedlingLeaf
        elif partType == 5:
            result = utravers.kStatisticsPartTypeLeaf
        elif partType == 6:
            result = utravers.kStatisticsPartTypeFemaleInflorescence
        elif partType == 7:
            result = utravers.kStatisticsPartTypeFemaleFlowerBud
        elif partType == 8:
            result = utravers.kStatisticsPartTypeFemaleFlower
        elif partType == 9:
            result = utravers.kStatisticsPartTypeMaleInflorescence
        elif partType == 10:
            result = utravers.kStatisticsPartTypeMaleFlowerBud
        elif partType == 11:
            result = utravers.kStatisticsPartTypeMaleFlower
        elif partType == 12:
            result = utravers.kStatisticsPartTypeFallenFlower
        elif partType == 13:
            result = utravers.kStatisticsPartTypeUnripeFruit
        elif partType == 14:
            result = utravers.kStatisticsPartTypeFruit
        elif partType == 15:
            result = utravers.kStatisticsPartTypeFallenFruit
        elif partType == 16:
            result = utravers.kStatisticsPartTypeUnallocatedNewVegetativeBiomass
        elif partType == 17:
            result = utravers.kStatisticsPartTypeUnremovedDeadVegetativeBiomass
        elif partType == 18:
            result = utravers.kStatisticsPartTypeUnallocatedNewReproductiveBiomass
        elif partType == 19:
            result = utravers.kStatisticsPartTypeUnremovedDeadReproductiveBiomass
        else :
            # called by paint method, so do not raise exception 
            result = 0
        return result
    
