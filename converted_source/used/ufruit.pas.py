# unit ufruit

from conversion_common import *
import uclasses
import u3dexport
import uturtle
import usupport
import udebug
import utravers
import ufiler
import utdo
import uplant
import umath
import upart
import delphi_compatability

# const
kDrawFlowerAsOpening = true
kDontDrawFlowerAsOpening = false
kLine = true
kNotLine = false

# const
kDrawTDOOpen = true
kDrawTDOClosed = false

#  kBud = 0; kPistil = 1; kStamens = 2; kFirstPetals = 3; kSecondPetals = 4; kThirdPetals = 5; kSepals = 6;
class PdFlowerFruit(PdPlantPart):
    def __init__(self):
        self.propFullSize = 0.0
        self.stage = 0
        self.hasBeenDrawn = false
        self.daysAccumulatingFruitBiomass = 0L
        self.daysOpen = 0L
    
    def initializeGender(self, aPlant, aGender):
        self.initialize(aPlant)
        self.gender = aGender
        self.propFullSize = 0.0
        self.liveBiomass_pctMPB = 0.0
        self.deadBiomass_pctMPB = 0.0
        self.biomassDemand_pctMPB = 0.0
        self.stage = uplant.kStageFlowerBud
        self.hasBeenDrawn = false
    
    def getName(self):
        result = ""
        result = "flower/fruit"
        return result
    
    def nextDay(self):
        anthesisLoss_pctMPB = 0.0
        biomassToMakeFruit_pctMPB = 0.0
        minDaysWithOptimalBiomass = false
        maxDaysWithMinFraction = false
        
        if self.hasFallenOff:
            return
        try:
            PdPlantPart.nextDay(self)
            if self.stage == uplant.kStageFlowerBud:
                if ((self.liveBiomass_pctMPB >= self.plant.pFlower[self.gender].minFractionOfOptimalBiomassToOpenFlower_frn * self.plant.pFlower[self.gender].optimalBiomass_pctMPB) or (self.age > self.plant.pFlower[self.gender].maxDaysToGrowIfOverMinFraction)) and (self.age > self.plant.pFlower[self.gender].minDaysToOpenFlower):
                    #if over required fraction of optimal or over max days to grow, open bud
                    self.stage = uplant.kStageOpenFlower
                    self.daysOpen = 0
            elif self.stage == uplant.kStageOpenFlower:
                #if over optimal or over min fraction to create fruit and over max days to grow, set fruit
                self.daysOpen += 1
                if self.daysOpen > self.plant.pFlower[self.gender].daysBeforeDrop:
                    self.hasFallenOff = true
                elif self.gender != uplant.kGenderMale:
                    if self.age > self.plant.pFlower[self.gender].minDaysBeforeSettingFruit:
                        # limit on time to set fruit (as opposed to grow) if want to keep flowers on plant longer
                        # upper limit on growth; must be at least as old as minDaysToGrow unless there is optimal biomass
                        minDaysWithOptimalBiomass = (self.age > self.plant.pFlower[self.gender].minDaysToGrow) and (self.liveBiomass_pctMPB >= self.plant.pFlower[self.gender].optimalBiomass_pctMPB)
                        # lower limit on growth; if don't have enough to make fruit, give up after max days and make anyway
                        biomassToMakeFruit_pctMPB = self.plant.pFlower[self.gender].minFractionOfOptimalBiomassToCreateFruit_frn * self.plant.pFlower[self.gender].optimalBiomass_pctMPB
                        maxDaysWithMinFraction = (self.age > self.plant.pFlower[self.gender].maxDaysToGrowIfOverMinFraction) or (self.liveBiomass_pctMPB >= biomassToMakeFruit_pctMPB)
                        if maxDaysWithMinFraction or minDaysWithOptimalBiomass:
                            self.stage = uplant.kStageUnripeFruit
                            self.daysAccumulatingFruitBiomass = 0
                            # flower biomass drops off, 50% goes into developing fruit (ovary) 
                            # choice of 50% is arbitrary - could be parameter in future depending on size of flower parts/ovary 
                            anthesisLoss_pctMPB = self.liveBiomass_pctMPB * 0.5
                            self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - anthesisLoss_pctMPB
                            self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + anthesisLoss_pctMPB
                            self.propFullSize = (umath.min(1.0, umath.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFruit.optimalBiomass_pctMPB, 0.0)))
            elif self.stage == uplant.kStageUnripeFruit:
                if (self.stage == uplant.kStageUnripeFruit) and (self.daysAccumulatingFruitBiomass >= self.plant.pFruit.daysToRipen):
                    self.stage = uplant.kStageRipeFruit
                self.daysAccumulatingFruitBiomass += 1
            elif self.stage == uplant.kStageRipeFruit:
                if (self.stage == uplant.kStageUnripeFruit) and (self.daysAccumulatingFruitBiomass >= self.plant.pFruit.daysToRipen):
                    self.stage = uplant.kStageRipeFruit
                self.daysAccumulatingFruitBiomass += 1
        except Exception, e:
            usupport.messageForExceptionType(e, "PdFlowerFruit.nextDay")
    
    def traverseActivity(self, mode, traverserProxy):
        traverser = PdTraverser()
        newPropFullSize = 0.0
        newBiomass_pctMPB = 0.0
        newOptimalBiomass_pctMPB = 0.0
        biomassToRemove_pctMPB = 0.0
        fractionOfMaxAge_frn = 0.0
        
        PdPlantPart.traverseActivity(self, mode, traverserProxy)
        traverser = utravers.PdTraverser(traverserProxy)
        if traverser == None:
            return
        if self.hasFallenOff and (mode != utravers.kActivityStream) and (mode != utravers.kActivityFree) and (mode != utravers.kActivityGatherStatistics):
            return
        try:
            if mode == utravers.kActivityNone:
                pass
            elif mode == utravers.kActivityNextDay:
                self.nextDay()
            elif mode == utravers.kActivityDemandVegetative:
                pass
            elif mode == utravers.kActivityDemandReproductive:
                if self.stage == uplant.kStageFlowerBud:
                    # has no vegetative demand 
                    # accum. biomass for flower 
                    self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, self.plant.pFlower[self.gender].optimalBiomass_pctMPB, self.plant.pFlower[self.gender].minDaysToGrow)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                elif self.stage == uplant.kStageOpenFlower:
                    # has no vegetative demand 
                    # accum. biomass for flower 
                    self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, self.plant.pFlower[self.gender].optimalBiomass_pctMPB, self.plant.pFlower[self.gender].minDaysToGrow)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                elif self.stage == uplant.kStageUnripeFruit:
                    if self.daysAccumulatingFruitBiomass > self.plant.pFruit.maxDaysToGrow:
                        # accum. biomass for fruit 
                        self.biomassDemand_pctMPB = 0.0
                    else:
                        fractionOfMaxAge_frn = umath.safedivExcept(self.daysAccumulatingFruitBiomass + 1, self.plant.pFruit.maxDaysToGrow, 0.0)
                        newPropFullSize = umath.max(0.0, umath.min(1.0, umath.scurve(fractionOfMaxAge_frn, self.plant.pFruit.sCurveParams.c1, self.plant.pFruit.sCurveParams.c2)))
                        newOptimalBiomass_pctMPB = newPropFullSize * self.plant.pFruit.optimalBiomass_pctMPB
                        self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, newOptimalBiomass_pctMPB, 1)
                        traverser.total = traverser.total + self.biomassDemand_pctMPB
                elif self.stage == uplant.kStageRipeFruit:
                    if self.daysAccumulatingFruitBiomass > self.plant.pFruit.maxDaysToGrow:
                        # accum. biomass for fruit 
                        self.biomassDemand_pctMPB = 0.0
                    else:
                        fractionOfMaxAge_frn = umath.safedivExcept(self.daysAccumulatingFruitBiomass + 1, self.plant.pFruit.maxDaysToGrow, 0.0)
                        newPropFullSize = umath.max(0.0, umath.min(1.0, umath.scurve(fractionOfMaxAge_frn, self.plant.pFruit.sCurveParams.c1, self.plant.pFruit.sCurveParams.c2)))
                        newOptimalBiomass_pctMPB = newPropFullSize * self.plant.pFruit.optimalBiomass_pctMPB
                        self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, newOptimalBiomass_pctMPB, 1)
                        traverser.total = traverser.total + self.biomassDemand_pctMPB
            elif mode == utravers.kActivityGrowVegetative:
                pass
            elif mode == utravers.kActivityGrowReproductive:
                # cannot grow vegetatively 
                #Allocate portion of total new biomass based on this demand over total demand.
                newBiomass_pctMPB = self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + newBiomass_pctMPB
                if self.stage == uplant.kStageFlowerBud:
                    self.propFullSize = (umath.min(1.0, umath.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFlower[self.gender].optimalBiomass_pctMPB, 0.0)))
                elif self.stage == uplant.kStageOpenFlower:
                    self.propFullSize = (umath.min(1.0, umath.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFlower[self.gender].optimalBiomass_pctMPB, 0.0)))
                elif self.stage == uplant.kStageUnripeFruit:
                    self.propFullSize = (umath.min(1.0, umath.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFruit.optimalBiomass_pctMPB, 0.0)))
                elif self.stage == uplant.kStageRipeFruit:
                    self.propFullSize = (umath.min(1.0, umath.safedivExcept(self.totalBiomass_pctMPB(), self.plant.pFruit.optimalBiomass_pctMPB, 0.0)))
            elif mode == utravers.kActivityStartReproduction:
                pass
            elif mode == utravers.kActivityFindPlantPartAtPosition:
                if umath.pointsAreCloseEnough(traverser.point, self.position()):
                    # can't switch because has no vegetative mode 
                    traverser.foundPlantPart = self
                    traverser.finished = true
            elif mode == utravers.kActivityDraw:
                pass
            elif mode == utravers.kActivityReport:
                pass
            elif mode == utravers.kActivityStream:
                pass
            elif mode == utravers.kActivityFree:
                pass
            elif mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved:
                pass
            elif mode == utravers.kActivityRemoveVegetativeBiomass:
                pass
            elif mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                # inflorescence should handle telling flowers to draw 
                #streaming called by inflorescence
                # free called by inflorescence 
                # none 
                # do nothing 
                traverser.total = traverser.total + self.liveBiomass_pctMPB
            elif mode == utravers.kActivityRemoveReproductiveBiomass:
                if self.liveBiomass_pctMPB <= 0.0:
                    return
                biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
                if self.liveBiomass_pctMPB <= 0.0:
                    if (self.stage == uplant.kStageUnripeFruit) or (self.stage == uplant.kStageRipeFruit):
                        self.hasFallenOff = true
            elif mode == utravers.kActivityGatherStatistics:
                if self.stage == uplant.kStageFlowerBud:
                    if self.gender == uplant.kGenderMale:
                        if self.hasFallenOff:
                            self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFlower)
                        else:
                            self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeMaleFlowerBud)
                    else:
                        if self.hasFallenOff:
                            self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFlower)
                        else:
                            self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFemaleFlowerBud)
                elif self.stage == uplant.kStageOpenFlower:
                    if self.gender == uplant.kGenderMale:
                        if self.hasFallenOff:
                            self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFlower)
                        else:
                            self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeMaleFlower)
                    else:
                        if self.hasFallenOff:
                            self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFlower)
                        else:
                            self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFemaleFlower)
                elif self.stage == uplant.kStageUnripeFruit:
                    if self.hasFallenOff:
                        self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFruit)
                    else:
                        self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeUnripeFruit)
                elif self.stage == uplant.kStageRipeFruit:
                    if self.hasFallenOff:
                        self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFallenFruit)
                    else:
                        self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeFruit)
                else :
                    raise GeneralException.create("Problem: Invalid fruit stage in method PdFlowerFruit.traverseActivity.")
                self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllReproductive)
            elif mode == utravers.kActivityCountPlantParts:
                pass
            elif mode == utravers.kActivityFindPartForPartID:
                pass
            elif mode == utravers.kActivityCountTotalMemoryUse:
                traverser.totalMemorySize += self.instanceSize
            elif mode == utravers.kActivityCalculateBiomassForGravity:
                pass
            elif mode == utravers.kActivityCountPointsAndTrianglesFor3DExport:
                self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser)
            else :
                raise GeneralException.create("Problem: Unhandled mode for plant draw activity in method PdFlowerFruit.traverseActivity.")
        except Exception, e:
            usupport.messageForExceptionType(e, "PdFlowerFruit.traverseActivity")
    
    def report(self):
        PdPlantPart.report(self)
        # DebugPrint(' flower/fruit, age '  + IntToStr(age) + ' biomass '  + floatToStr(self.liveBiomass_pctMPB));
    
    def dxfIndexForFloralLayerType(self, aType, line):
        result = 0
        result = 0
        if aType == uplant.kBud:
            result = u3dexport.kExportPartFlowerBudFemale
        elif aType == uplant.kPistils:
            if line:
                result = u3dexport.kExportPartStyleFemale
            else:
                result = u3dexport.kExportPartStigmaFemale
        elif aType == uplant.kStamens:
            if line:
                result = u3dexport.kExportPartFilamentFemale
            else:
                result = u3dexport.kExportPartAntherFemale
        elif aType == uplant.kFirstPetals:
            result = u3dexport.kExportPartFirstPetalsFemale
        elif aType == uplant.kSecondPetals:
            result = u3dexport.kExportPartSecondPetalsFemale
        elif aType == uplant.kThirdPetals:
            result = u3dexport.kExportPartThirdPetalsFemale
        elif aType == uplant.kFourthPetals:
            result = u3dexport.kExportPartFourthPetalsFemale
        elif aType == uplant.kFifthPetals:
            result = u3dexport.kExportPartFifthPetalsFemale
        elif aType == uplant.kSepals:
            result = u3dexport.kExportPartSepalsFemale
        return result
    
    def draw(self):
        scale = 0.0
        length = 0.0
        width = 0.0
        turtle = KfTurtle()
        
        if (self.plant.turtle == None):
            return
        turtle = self.plant.turtle
        self.boundsRect = Rect(0, 0, 0, 0)
        if self.hasFallenOff:
            return
        turtle.push()
        self.determineAmendmentAndAlsoForChildrenIfAny()
        if self.hiddenByAmendment():
            turtle.pop()
            return
        else:
            self.applyAmendmentRotations()
        try:
            if self.stage == uplant.kStageFlowerBud:
                if self.plant.pFlower[self.gender].budDrawingOption == uplant.kDrawNoBud:
                    # kDrawNoBud = 0; kDrawSingleTdoBud = 1; kDrawOpeningFlower = 2;
                    return
                elif self.plant.pFlower[self.gender].budDrawingOption == uplant.kDrawSingleTdoBud:
                    scale = ((self.plant.pFlower[self.gender].tdoParams[uplant.kBud].scaleAtFullSize / 100.0) * self.propFullSize)
                    turtle.rotateX(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kBud].xRotationBeforeDraw))
                    turtle.rotateY(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kBud].yRotationBeforeDraw))
                    turtle.rotateZ(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kBud].zRotationBeforeDraw))
                    self.drawCircleOfTdos(self.plant.pFlower[self.gender].tdoParams[uplant.kBud].object3D, self.plant.pFlower[self.gender].tdoParams[uplant.kBud].faceColor, self.plant.pFlower[self.gender].tdoParams[uplant.kBud].backfaceColor, self.plant.pFlower[self.gender].tdoParams[uplant.kBud].pullBackAngle, scale, self.plant.pFlower[self.gender].tdoParams[uplant.kBud].repetitions, self.plant.pFlower[self.gender].tdoParams[uplant.kBud].radiallyArranged, kDrawTDOClosed, u3dexport.kExportPartFlowerBudFemale)
                elif self.plant.pFlower[self.gender].budDrawingOption == uplant.kDrawOpeningFlower:
                    self.drawFlower(kDrawFlowerAsOpening)
            elif self.stage == uplant.kStageOpenFlower:
                self.drawFlower(kDontDrawFlowerAsOpening)
            elif self.stage == uplant.kStageUnripeFruit:
                # ripe color is regular color; alternate color is unripe color
                scale = ((self.plant.pFruit.tdoParams.scaleAtFullSize / 100.0) * self.propFullSize)
                turtle.rotateX(self.angleWithSway(self.plant.pFruit.tdoParams.xRotationBeforeDraw))
                turtle.rotateY(self.angleWithSway(self.plant.pFruit.tdoParams.yRotationBeforeDraw))
                turtle.rotateZ(self.angleWithSway(self.plant.pFruit.tdoParams.zRotationBeforeDraw))
                self.drawCircleOfTdos(self.plant.pFruit.tdoParams.object3D, self.plant.pFruit.tdoParams.alternateFaceColor, self.plant.pFruit.tdoParams.alternateBackfaceColor, self.plant.pFruit.tdoParams.pullBackAngle, scale, self.plant.pFruit.tdoParams.repetitions, self.plant.pFruit.tdoParams.radiallyArranged, kDrawTDOClosed, u3dexport.kExportPartUnripeFruit)
            elif self.stage == uplant.kStageRipeFruit:
                scale = ((self.plant.pFruit.tdoParams.scaleAtFullSize / 100.0) * self.propFullSize)
                turtle.rotateX(self.angleWithSway(self.plant.pFruit.tdoParams.xRotationBeforeDraw))
                turtle.rotateY(self.angleWithSway(self.plant.pFruit.tdoParams.yRotationBeforeDraw))
                turtle.rotateZ(self.angleWithSway(self.plant.pFruit.tdoParams.zRotationBeforeDraw))
                self.drawCircleOfTdos(self.plant.pFruit.tdoParams.object3D, self.plant.pFruit.tdoParams.faceColor, self.plant.pFruit.tdoParams.backfaceColor, self.plant.pFruit.tdoParams.pullBackAngle, scale, self.plant.pFruit.tdoParams.repetitions, self.plant.pFruit.tdoParams.radiallyArranged, kDrawTDOClosed, u3dexport.kExportPartRipeFruit)
            self.hasBeenDrawn = true
            turtle.pop()
        except Exception, e:
            usupport.messageForExceptionType(e, "PdFlowerFruit.draw")
    
    def drawFlower(self, drawAsOpening):
        turtle = KfTurtle()
        angle = 0.0
        scale = 0.0
        layerType = 0
        
        if (self.plant.turtle == None):
            return
        turtle = self.plant.turtle
        self.drawPistilsAndStamens(drawAsOpening)
        for layerType in range(uplant.kFirstPetals, uplant.kSepals + 1):
            turtle.push()
            scale = ((self.plant.pFlower[self.gender].tdoParams[layerType].scaleAtFullSize / 100.0) * self.propFullSize)
            angle = self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle)
            if drawAsOpening:
                angle = angle * self.propFullSize * 2
                if angle > self.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle:
                    angle = self.plant.pFlower[self.gender].tdoParams[layerType].pullBackAngle
            turtle.rotateX(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[layerType].xRotationBeforeDraw))
            turtle.rotateY(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[layerType].yRotationBeforeDraw))
            turtle.rotateZ(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[layerType].zRotationBeforeDraw))
            self.drawCircleOfTdos(self.plant.pFlower[self.gender].tdoParams[layerType].object3D, self.plant.pFlower[self.gender].tdoParams[layerType].faceColor, self.plant.pFlower[self.gender].tdoParams[layerType].backfaceColor, angle, scale, self.plant.pFlower[self.gender].tdoParams[layerType].repetitions, self.plant.pFlower[self.gender].tdoParams[layerType].radiallyArranged, kDrawTDOOpen, self.dxfIndexForFloralLayerType(layerType, kNotLine))
            turtle.pop()
    
    def drawPistilsAndStamens(self, drawAsOpening):
        scale = 0.0
        length = 0.0
        width = 0.0
        angle = 0.0
        turtle = KfTurtle()
        i = 0
        turnPortion = 0
        leftOverDegrees = 0
        addThisTime = 0
        addition = 0.0
        carryOver = 0.0
        
        if (self.plant.turtle == None):
            return
        turtle = self.plant.turtle
        turtle.push()
        if (self.plant.pFlower[self.gender].numPistils > 0):
            if ((self.plant.pFlower[self.gender].styleLength_mm > 0) and (self.plant.pFlower[self.gender].styleWidth_mm > 0)) or (self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].scaleAtFullSize > 0):
                turtle.ifExporting_startNestedGroupOfPlantParts("pistils", "Pistils", u3dexport.kNestingTypeFloralLayers)
            turnPortion = 256 / self.plant.pFlower[self.gender].numPistils
            leftOverDegrees = 256 - turnPortion * self.plant.pFlower[self.gender].numPistils
            if leftOverDegrees > 0:
                addition = umath.safedivExcept(leftOverDegrees, self.plant.pFlower[self.gender].numPistils, 0)
            else:
                addition = 0
            carryOver = 0
            for i in range(0, self.plant.pFlower[self.gender].numPistils):
                turtle.push()
                if (self.plant.pFlower[self.gender].styleLength_mm > 0) and (self.plant.pFlower[self.gender].styleWidth_mm > 0):
                    len = umath.max(0.0, self.propFullSize * self.plant.pFlower[self.gender].styleLength_mm)
                    width = umath.max(0.0, self.propFullSize * self.plant.pFlower[self.gender].styleWidth_mm)
                    angle = self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].pullBackAngle)
                    if drawAsOpening:
                        angle = angle * self.propFullSize
                    self.drawStemSegment(len, width, angle, 0, self.plant.pFlower[self.gender].styleColor, self.plant.pFlower[self.gender].styleTaperIndex, self.dxfIndexForFloralLayerType(uplant.kPistils, kLine), upart.kDontUseAmendment)
                scale = ((self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].scaleAtFullSize / 100.0) * self.propFullSize)
                turtle.rotateX(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].xRotationBeforeDraw))
                turtle.rotateY(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].yRotationBeforeDraw))
                turtle.rotateZ(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].zRotationBeforeDraw))
                self.drawCircleOfTdos(self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].object3D, self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].faceColor, self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].backfaceColor, 0, scale, self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].repetitions, self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].radiallyArranged, kDrawTDOOpen, self.dxfIndexForFloralLayerType(uplant.kPistils, kNotLine))
                turtle.pop()
                addThisTime = trunc(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                turtle.rotateX(turnPortion + addThisTime)
            if ((self.plant.pFlower[self.gender].styleLength_mm > 0) and (self.plant.pFlower[self.gender].styleWidth_mm > 0)) or (self.plant.pFlower[self.gender].tdoParams[uplant.kPistils].scaleAtFullSize > 0):
                turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeFloralLayers)
        turtle.pop()
        # stamens
        turtle.push()
        if self.plant.pFlower[self.gender].numStamens > 0:
            if ((self.plant.pFlower[self.gender].filamentLength_mm > 0) and (self.plant.pFlower[self.gender].filamentWidth_mm > 0)) or (self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].scaleAtFullSize > 0):
                if self.gender == uplant.kGenderFemale:
                    turtle.ifExporting_startNestedGroupOfPlantParts("primary stamens", "1Stamens", u3dexport.kNestingTypeFloralLayers)
                else:
                    turtle.ifExporting_startNestedGroupOfPlantParts("secondary stamens", "2Stamens", u3dexport.kNestingTypeFloralLayers)
            turnPortion = 256 / self.plant.pFlower[self.gender].numStamens
            leftOverDegrees = 256 - turnPortion * self.plant.pFlower[self.gender].numStamens
            if leftOverDegrees > 0:
                addition = umath.safedivExcept(leftOverDegrees, self.plant.pFlower[self.gender].numStamens, 0)
            else:
                addition = 0
            carryOver = 0
            for i in range(0, self.plant.pFlower[self.gender].numStamens):
                turtle.push()
                if (self.plant.pFlower[self.gender].filamentLength_mm > 0) and (self.plant.pFlower[self.gender].filamentWidth_mm > 0):
                    len = umath.max(0.0, self.propFullSize * self.plant.pFlower[self.gender].filamentLength_mm)
                    width = umath.max(0.0, self.propFullSize * self.plant.pFlower[self.gender].filamentWidth_mm)
                    angle = self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].pullBackAngle)
                    if drawAsOpening:
                        angle = angle * self.propFullSize
                    self.drawStemSegment(len, width, angle, 0, self.plant.pFlower[self.gender].filamentColor, self.plant.pFlower[self.gender].filamentTaperIndex, self.dxfIndexForFloralLayerType(uplant.kStamens, kLine), upart.kDontUseAmendment)
                scale = ((self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].scaleAtFullSize / 100.0) * self.propFullSize)
                turtle.rotateX(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].xRotationBeforeDraw))
                turtle.rotateY(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].yRotationBeforeDraw))
                turtle.rotateZ(self.angleWithSway(self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].zRotationBeforeDraw))
                self.drawCircleOfTdos(self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].object3D, self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].faceColor, self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].backfaceColor, 0, scale, self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].repetitions, self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].radiallyArranged, kDrawTDOOpen, self.dxfIndexForFloralLayerType(uplant.kStamens, kNotLine))
                turtle.pop()
                addThisTime = trunc(addition + carryOver)
                carryOver = carryOver + addition - addThisTime
                if carryOver < 0:
                    carryOver = 0
                turtle.rotateX(turnPortion + addThisTime)
            if ((self.plant.pFlower[self.gender].filamentLength_mm > 0) and (self.plant.pFlower[self.gender].filamentWidth_mm > 0)) or (self.plant.pFlower[self.gender].tdoParams[uplant.kStamens].scaleAtFullSize > 0):
                turtle.ifExporting_endNestedGroupOfPlantParts(u3dexport.kNestingTypeFloralLayers)
        turtle.pop()
    
    def countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(self, traverser):
        numLines = 0
        
        if traverser == None:
            return
        if self.propFullSize <= 0:
            return
        if self.hasFallenOff:
            return
        if self.stage == uplant.kStageFlowerBud:
            if self.plant.pFlower[self.gender].budDrawingOption == uplant.kDrawNoBud:
                pass
            elif self.plant.pFlower[self.gender].budDrawingOption == uplant.kDrawSingleTdoBud:
                if self.plant.pFlower[self.gender].tdoParams[uplant.kBud].scaleAtFullSize > 0:
                    traverser.total3DExportPointsIn3DObjects += self.plant.pFlower[self.gender].tdoParams[uplant.kBud].object3D.pointsInUse * self.plant.pFlower[self.gender].tdoParams[uplant.kBud].repetitions
                    traverser.total3DExportTrianglesIn3DObjects += self.plant.pFlower[self.gender].tdoParams[uplant.kBud].object3D.triangles.Count * self.plant.pFlower[self.gender].tdoParams[uplant.kBud].repetitions
                    self.addExportMaterial(traverser, u3dexport.kExportPartFlowerBudFemale, u3dexport.kExportPartFlowerBudMale)
            elif self.plant.pFlower[self.gender].budDrawingOption == uplant.kDrawOpeningFlower:
                self.addFloralPartsCountsToTraverser(traverser)
        elif self.stage == uplant.kStageOpenFlower:
            self.addFloralPartsCountsToTraverser(traverser)
        elif self.stage == uplant.kStageUnripeFruit:
            if self.plant.pFruit.tdoParams.scaleAtFullSize > 0:
                traverser.total3DExportPointsIn3DObjects += self.plant.pFruit.tdoParams.object3D.pointsInUse * self.plant.pFruit.tdoParams.repetitions
                traverser.total3DExportTrianglesIn3DObjects += self.plant.pFruit.tdoParams.object3D.triangles.Count * self.plant.pFruit.tdoParams.repetitions
                if self.stage == uplant.kStageUnripeFruit:
                    self.addExportMaterial(traverser, u3dexport.kExportPartUnripeFruit, -1)
                else:
                    self.addExportMaterial(traverser, u3dexport.kExportPartRipeFruit, -1)
        elif self.stage == uplant.kStageRipeFruit:
            if self.plant.pFruit.tdoParams.scaleAtFullSize > 0:
                traverser.total3DExportPointsIn3DObjects += self.plant.pFruit.tdoParams.object3D.pointsInUse * self.plant.pFruit.tdoParams.repetitions
                traverser.total3DExportTrianglesIn3DObjects += self.plant.pFruit.tdoParams.object3D.triangles.Count * self.plant.pFruit.tdoParams.repetitions
                if self.stage == uplant.kStageUnripeFruit:
                    self.addExportMaterial(traverser, u3dexport.kExportPartUnripeFruit, -1)
                else:
                    self.addExportMaterial(traverser, u3dexport.kExportPartRipeFruit, -1)
        # pedicel handled by inflorescence
    
    def addFloralPartsCountsToTraverser(self, traverser):
        partType = 0
        
        for partType in range(uplant.kPistils, uplant.kSepals + 1):
            if self.plant.pFlower[self.gender].tdoParams[partType].scaleAtFullSize > 0:
                if partType == uplant.kPistils:
                    traverser.total3DExportPointsIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numPistils
                    traverser.total3DExportTrianglesIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numPistils
                    self.addExportMaterial(traverser, u3dexport.kExportPartStyleFemale, -1)
                    self.addExportMaterial(traverser, u3dexport.kExportPartStigmaFemale, -1)
                elif partType == uplant.kStamens:
                    traverser.total3DExportPointsIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numStamens
                    traverser.total3DExportTrianglesIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numStamens
                    self.addExportMaterial(traverser, u3dexport.kExportPartFilamentFemale, u3dexport.kExportPartFilamentMale)
                    self.addExportMaterial(traverser, u3dexport.kExportPartAntherFemale, u3dexport.kExportPartAntherMale)
                else:
                    traverser.total3DExportPointsIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.pointsInUse * self.plant.pFlower[self.gender].tdoParams[partType].repetitions
                    traverser.total3DExportTrianglesIn3DObjects += self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * self.plant.pFlower[self.gender].tdoParams[partType].repetitions
                    if partType == uplant.kFirstPetals:
                        self.addExportMaterial(traverser, u3dexport.kExportPartFirstPetalsFemale, u3dexport.kExportPartFirstPetalsMale)
                    elif partType == uplant.kSecondPetals:
                        self.addExportMaterial(traverser, u3dexport.kExportPartSecondPetalsFemale, -1)
                    elif partType == uplant.kThirdPetals:
                        self.addExportMaterial(traverser, u3dexport.kExportPartThirdPetalsFemale, -1)
                    elif partType == uplant.kFourthPetals:
                        self.addExportMaterial(traverser, u3dexport.kExportPartFourthPetalsFemale, -1)
                    elif partType == uplant.kFifthPetals:
                        self.addExportMaterial(traverser, u3dexport.kExportPartFifthPetalsFemale, -1)
                    elif partType == uplant.kSepals:
                        self.addExportMaterial(traverser, u3dexport.kExportPartSepalsFemale, u3dexport.kExportPartSepalsMale)
    
    def triangleCountInFloralParts(self):
        result = 0
        partType = 0
        
        result = 0
        for partType in range(uplant.kPistils, uplant.kSepals + 1):
            if self.plant.pFlower[self.gender].tdoParams[partType].scaleAtFullSize > 0:
                if partType == uplant.kPistils:
                    result = result + self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numPistils
                elif partType == uplant.kStamens:
                    result = result + self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * self.plant.pFlower[self.gender].tdoParams[partType].repetitions * self.plant.pFlower[self.gender].numStamens
                else:
                    result = result + self.plant.pFlower[self.gender].tdoParams[partType].object3D.triangles.Count * self.plant.pFlower[self.gender].tdoParams[partType].repetitions
        return result
    
    def tdoToSortLinesWith(self):
        result = KfObject3D()
        result = None
        if self.plant == None:
            return result
        if self.hasFallenOff:
            return result
        if self.stage == uplant.kStageFlowerBud:
            result = self.plant.pFlower[self.gender].tdoParams[uplant.kBud].object3D
        elif self.stage == uplant.kStageOpenFlower:
            result = self.plant.pFlower[self.gender].tdoParams[uplant.kFirstPetals].object3D
        elif self.stage == uplant.kStageUnripeFruit:
            result = self.plant.pFruit.tdoParams.object3D
        elif self.stage == uplant.kStageRipeFruit:
            result = self.plant.pFruit.tdoParams.object3D
        return result
    
    def drawCircleOfTdos(self, tdo, faceColor, backfaceColor, pullBackAngle, scale, numParts, partsArranged, open, dxfIndex):
        turtle = KfTurtle()
        i = 0
        minZ = 0.0
        turnPortion = 0
        leftOverDegrees = 0
        addThisTime = 0
        addition = 0.0
        carryOver = 0.0
        
        try:
            if (scale <= 0.0):
                # v1.3
                # v1.3
                return
            turtle = self.plant.turtle
            if (turtle == None):
                return
            turtle.push()
            minZ = 0
            if (partsArranged) and (numParts > 0):
                turtle.ifExporting_startPlantPart(self.longNameForDXFPartConsideringGenderEtc(dxfIndex), self.shortNameForDXFPartConsideringGenderEtc(dxfIndex))
                turnPortion = 256 / numParts
                leftOverDegrees = 256 - turnPortion * numParts
                if leftOverDegrees > 0:
                    addition = umath.safedivExcept(leftOverDegrees, numParts, 0)
                else:
                    addition = 0
                carryOver = 0
                for i in range(1, numParts + 1):
                    addThisTime = trunc(addition + carryOver)
                    carryOver = carryOver + addition - addThisTime
                    if carryOver < 0:
                        carryOver = 0
                    turtle.rotateX(turnPortion + addThisTime)
                    turtle.push()
                    #aligns object as stored in the file to way should draw on plant
                    turtle.rotateZ(-64)
                    if open:
                        #pulls petal up to plane of stalk (is perpendicular)
                        turtle.rotateY(32)
                    turtle.rotateX(pullBackAngle)
                    if tdo != None:
                        self.draw3DObject(tdo, scale, faceColor, backfaceColor, dxfIndex)
                        if i == 1:
                            minZ = tdo.zForSorting
                        elif tdo.zForSorting < minZ:
                            minZ = tdo.zForSorting
                    turtle.pop()
                if tdo != None:
                    tdo.zForSorting = minZ
                turtle.ifExporting_endPlantPart()
            else:
                turtle.push()
                if (self.stage == uplant.kStageUnripeFruit) or (self.stage == uplant.kStageRipeFruit):
                    turtle.rotateZ(-64)
                else:
                    #pulls petal up to plane of stalk (is perpendicular)
                    turtle.rotateZ(-pullBackAngle)
                if tdo != None:
                    self.draw3DObject(tdo, scale, faceColor, backfaceColor, dxfIndex)
                turtle.pop()
            turtle.pop()
        except Exception, e:
            usupport.messageForExceptionType(e, "PdFlowerFruit.drawCircleOfTdos")
    
    def partType(self):
        result = 0
        result = uplant.kPartTypeFlowerFruit
        return result
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdFlowerFruit
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        PdPlantPart.streamDataWithFiler(self, filer, cvir)
        self.propFullSize = filer.streamSingle(self.propFullSize)
        self.stage = filer.streamSmallint(self.stage)
        self.hasBeenDrawn = filer.streamBoolean(self.hasBeenDrawn)
        self.daysAccumulatingFruitBiomass = filer.streamLongint(self.daysAccumulatingFruitBiomass)
        self.daysOpen = filer.streamLongint(self.daysOpen)
    
# cfk remember this 
# ---------------------------------------------------------------------- wilting/falling down 
#procedure PdFlowerFruit.dragDownFromWeight;
#  begin
#  end; 
#procedure PdFlowerFruit.dragDownFromWeight;
#  var
#    fractionOfOptimalFruitWeight_frn: single;
#    angle: integer;
#  begin
#  if (plant.turtle = nil) then exit;
#  fractionOfOptimalFruitWeight_frn := safedivExcept(liveBiomass_pctMPB, plant.pFruit.optimalBiomass_pctMPB, 0.0);
#  angle := round(abs(plant.turtle.angleZ + 32) * fractionOfOptimalFruitWeight_frn
#      * min(1.0, max(0.0, 100 - plant.pFruit.stalkStrengthIndex) / 100.0));
#  angle := -angle;
#  if plant.turtle.angleZ > -32 then
#    angle := -angle;
#  plant.turtle.rotateZ(angle);
#  end;  
