# unit uintern

from conversion_common import *
import uamendmt
import uclasses
import uinflor
import umerist
import umath
import utdo
import u3dexport
import uturtle
import udebug
import usupport
import utravers
import ufiler
import uleaf
import uplant
import upart
import delphi_compatability

class PdInternode(PdPlantPart):
    def __init__(self):
        self.leftBranchPlantPart = PdPlantPart()
        self.rightBranchPlantPart = PdPlantPart()
        self.nextPlantPart = PdPlantPart()
        self.phytomerAttachedTo = PdInternode()
        self.leftLeaf = PdLeaf()
        self.rightLeaf = PdLeaf()
        self.internodeColor = TColorRef()
        self.internodeAngle = 0.0
        self.lengthExpansion = 0.0
        self.widthExpansion = 0.0
        self.boltingExpansion = 0.0
        self.fractionOfOptimalInitialBiomassAtCreation_frn = 0.0
        self.traversingDirection = 0
        self.isFirstPhytomer = false
        self.newBiomassForDay_pctMPB = 0.0
        self.distanceFromFirstPhytomer = 0L
    
    def NewWithPlantFractionOfInitialOptimalSize(self, aPlant, aFraction):
        result = PdInternode()
        result = self.create()
        result.InitializeFractionOfInitialOptimalSize(aPlant, aFraction)
        return result
    
    #???
    def InitializeFractionOfInitialOptimalSize(self, thePlant, aFraction):
        self.initialize(thePlant)
        #Plant sets this from outside on first phytomer.
        self.isFirstPhytomer = false
        self.calculateInternodeAngle()
        self.lengthExpansion = 1.0
        self.widthExpansion = 1.0
        self.boltingExpansion = 1.0
        self.fractionOfOptimalInitialBiomassAtCreation_frn = aFraction
        self.liveBiomass_pctMPB = aFraction * PdInternode.optimalInitialBiomass_pctMPB(self.plant)
        self.deadBiomass_pctMPB = 0.0
        self.internodeColor = self.plant.pInternode.faceColor
        self.leftLeaf = uleaf.PdLeaf.NewWithPlantFractionOfOptimalSize(self.plant, aFraction)
        if self.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementOpposite:
            self.rightLeaf = uleaf.PdLeaf.NewWithPlantFractionOfOptimalSize(self.plant, aFraction)
    
    def getName(self):
        result = ""
        result = "internode"
        return result
    
    def makeSecondSeedlingLeaf(self, aFraction):
        if self.rightLeaf == None:
            self.rightLeaf = uleaf.PdLeaf.NewWithPlantFractionOfOptimalSize(self.plant, aFraction)
        if self.rightLeaf != None:
            self.rightLeaf.isSeedlingLeaf = true
    
    def destroy(self):
        #note that if branch parts were phytomers they will have been
        #  freed and set to nil by the traverser
        self.nextPlantPart.free
        self.nextPlantPart = None
        self.leftBranchPlantPart.free
        self.leftBranchPlantPart = None
        self.rightBranchPlantPart.free
        self.rightBranchPlantPart = None
        self.leftLeaf.free
        self.leftLeaf = None
        self.rightLeaf.free
        self.rightLeaf = None
        PdPlantPart.destroy(self)
    
    def setAsFirstPhytomer(self):
        self.isFirstPhytomer = true
        if self.leftLeaf != None:
            self.leftLeaf.isSeedlingLeaf = true
        if self.rightLeaf != None:
            self.rightLeaf.isSeedlingLeaf = true
        self.calculateInternodeAngle()
    
    def determineAmendmentAndAlsoForChildrenIfAny(self):
        amendmentToPass = PdPlantDrawingAmendment()
        
        PdPlantPart.determineAmendmentAndAlsoForChildrenIfAny(self)
        if self.amendment != None:
            amendmentToPass = self.amendment
        else:
            amendmentToPass = self.parentAmendment
        if self.leftBranchPlantPart != None:
            self.leftBranchPlantPart.parentAmendment = amendmentToPass
        if self.rightBranchPlantPart != None:
            self.rightBranchPlantPart.parentAmendment = amendmentToPass
        if self.nextPlantPart != None:
            self.nextPlantPart.parentAmendment = amendmentToPass
        if self.leftLeaf != None:
            # amendment must be passed to leaves explicitly since they are not strictly speaking children
            self.leftLeaf.parentAmendment = amendmentToPass
        if self.rightLeaf != None:
            self.leftLeaf.parentAmendment = amendmentToPass
    
    def nextDay(self):
        tryExpansion = 0.0
        
        try:
            PdPlantPart.nextDay(self)
            if self.liveBiomass_pctMPB > 0:
                try:
                    # length and width expansion adjustment from new biomass (always decreases because new biomass is compact) 
                    # if liveBiomass_pctMPB is extremely small, these divisions may produce an overflow 
                    # must bound these because some accounting error is causing problems that should be fixed later 
                    tryExpansion = umath.max(0.0, umath.min(500.0, umath.safedivExcept(self.liveBiomass_pctMPB - self.newBiomassForDay_pctMPB, self.liveBiomass_pctMPB, 0) * self.lengthExpansion + umath.safedivExcept(self.newBiomassForDay_pctMPB, self.liveBiomass_pctMPB, 0) * 1.0))
                    self.lengthExpansion = tryExpansion
                except:
                    pass
                try:
                    tryExpansion = umath.max(0.0, umath.min(50.0, umath.safedivExcept(self.liveBiomass_pctMPB - self.newBiomassForDay_pctMPB, self.liveBiomass_pctMPB, 0) * self.widthExpansion + umath.safedivExcept(self.newBiomassForDay_pctMPB, self.liveBiomass_pctMPB, 0) * 1.0))
                    self.widthExpansion = tryExpansion
                except:
                    pass
                if self.plant.floweringHasStarted:
                    # not using this version
                    #    { length and width expansion increase due to water uptake }
                    #    with plant.pInternode do
                    #      if self.age <= plant.pInternode.maxDaysToExpand then
                    #        begin
                    #        linearGrowthWithFactor(self.lengthExpansion,
                    #            lengthMultiplierDueToExpansion, minDaysToExpand, 1.0); {1.0 was water stress factor}
                    #        linearGrowthWithFactor(self.widthExpansion,
                    #            widthMultiplierDueToExpansion, minDaysToExpand, 1.0);
                    #        end;
                    #    
                    #and
                    #      (plant.age - plant.ageAtWhichFloweringStarted <= plant.pInternode.maxDaysToBolt)
                    self.boltingExpansion = utravers.linearGrowthWithFactor(self.boltingExpansion, self.plant.pInternode.lengthMultiplierDueToBolting, self.plant.pInternode.minDaysToBolt, 1.0)
            self.checkIfSeedlingLeavesHaveAbscissed()
            self.calculateDistanceFromFirstPhytomer()
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInternode.nextDay")
    
    def optimalInitialBiomass_pctMPB(self, plant):
        result = 0.0
        result = umath.safedivExcept(plant.pInternode.optimalFinalBiomass_pctMPB, plant.pInternode.lengthMultiplierDueToBiomassAccretion * plant.pInternode.widthMultiplierDueToBiomassAccretion, 0)
        return result
    
    def propFullLength(self):
        result = 0.0
        result = umath.safedivExcept(self.totalBiomass_pctMPB() * self.lengthExpansion * self.boltingExpansion, self.plant.pInternode.optimalFinalBiomass_pctMPB, 0)
        return result
    
    def propFullWidth(self):
        result = 0.0
        result = umath.safedivExcept(self.totalBiomass_pctMPB() * self.widthExpansion, self.plant.pInternode.optimalFinalBiomass_pctMPB, 0)
        return result
    
    def traverseActivity(self, mode, traverserProxy):
        traverser = PdTraverser()
        biomassToRemove_pctMPB = 0.0
        targetBiomass_pctMPB = 0.0
        
        PdPlantPart.traverseActivity(self, mode, traverserProxy)
        traverser = utravers.PdTraverser(traverserProxy)
        if traverser == None:
            return
        if self.hasFallenOff and (mode != utravers.kActivityStream) and (mode != utravers.kActivityFree):
            return
        try:
            if (mode != utravers.kActivityDraw):
                if self.leftLeaf != None:
                    self.leftLeaf.traverseActivity(mode, traverser)
                if self.rightLeaf != None:
                    self.rightLeaf.traverseActivity(mode, traverser)
            if mode == utravers.kActivityNone:
                pass
            elif mode == utravers.kActivityNextDay:
                self.nextDay()
                if self.age < traverser.ageOfYoungestPhytomer:
                    traverser.ageOfYoungestPhytomer = self.age
            elif mode == utravers.kActivityDemandVegetative:
                if self.age > self.plant.pInternode.maxDaysToAccumulateBiomass:
                    self.biomassDemand_pctMPB = 0.0
                    return
                try:
                    if self.plant.pInternode.canRecoverFromStuntingDuringCreation:
                        targetBiomass_pctMPB = self.plant.pInternode.optimalFinalBiomass_pctMPB
                    else:
                        targetBiomass_pctMPB = self.plant.pInternode.optimalFinalBiomass_pctMPB * self.fractionOfOptimalInitialBiomassAtCreation_frn
                    self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, targetBiomass_pctMPB, self.plant.pInternode.minDaysToAccumulateBiomass)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdInternode.traverseActivity (vegetative demand)")
            elif mode == utravers.kActivityDemandReproductive:
                pass
            elif mode == utravers.kActivityGrowVegetative:
                if self.age > self.plant.pInternode.maxDaysToAccumulateBiomass:
                    #Return reproductive demand recursively from all reproductive meristems and fruits connected to
                    #      this phytomer. Phytomers, inflorescences, and flowers themselves have no demands.
                    return
                try:
                    self.newBiomassForDay_pctMPB = umath.max(0.0, self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass)
                    self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + self.newBiomassForDay_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdInternode.traverseActivity (vegetative growth)")
            elif mode == utravers.kActivityGrowReproductive:
                pass
            elif mode == utravers.kActivityStartReproduction:
                pass
            elif mode == utravers.kActivityFindPlantPartAtPosition:
                if umath.pointsAreCloseEnough(traverser.point, self.position()):
                    #Recurse available photosynthate allocated to reproductive growth to all plant parts.
                    #      Only meristems and fruits will incorporate it.
                    #Send signal to consider reproductive mode to all meristems on plant.
                    traverser.foundPlantPart = self
                    traverser.finished = true
            elif mode == utravers.kActivityDraw:
                self.draw()
            elif mode == utravers.kActivityReport:
                pass
            elif mode == utravers.kActivityStream:
                self.streamUsingFiler(traverser.filer)
            elif mode == utravers.kActivityFree:
                pass
            elif mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved:
                # free called by traverser 
                traverser.total = traverser.total + self.liveBiomass_pctMPB
            elif mode == utravers.kActivityRemoveVegetativeBiomass:
                biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
            elif mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                pass
            elif mode == utravers.kActivityRemoveReproductiveBiomass:
                pass
            elif mode == utravers.kActivityGatherStatistics:
                # none 
                # none 
                self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeStem)
                self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllVegetative)
            elif mode == utravers.kActivityCountPlantParts:
                pass
            elif mode == utravers.kActivityFindPartForPartID:
                pass
            elif mode == utravers.kActivityCountTotalMemoryUse:
                traverser.totalMemorySize += self.instanceSize
            elif mode == utravers.kActivityCalculateBiomassForGravity:
                if self.traversingDirection == utravers.kTraverseDone:
                    # on way up, do nothing; on way down, total up accumulated biomass
                    self.biomassOfMeAndAllPartsAboveMe_pctMPB = self.biomassOfMeAndAllPartsConnectedToMe_pctMPB() + self.biomassOfPartsImmediatelyAboveMe_pctMPB()
            elif mode == utravers.kActivityCountPointsAndTrianglesFor3DExport:
                self.countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(traverser)
            else :
                raise GeneralException.create("Problem: Unhandled mode in method PdInternode.traverseActivity.")
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInternode.traverseActivity")
    
    def countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(self, traverser):
        if traverser == None:
            return
        traverser.total3DExportStemSegments += 1
        self.addExportMaterial(traverser, u3dexport.kExportPartInternode, -1)
        if self.plant.pRoot.tdoParams.scaleAtFullSize > 0:
            self.addExportMaterial(traverser, u3dexport.kExportPartRootTop, -1)
    
    def isPhytomer(self):
        result = false
        result = true
        return result
    
    def blendColorsStrength(self, aColor, aStrength):
        if aStrength <= 0.0:
            return
        self.internodeColor = usupport.blendColors(self.internodeColor, aColor, aStrength)
    
    def setColorsToParameters(self):
        #Initialize phytomer colors at those in plant parameters, before stresses are considered.
        self.internodeColor = self.plant.pInternode.faceColor
    
    def calculateInternodeAngle(self):
        if self.isFirstPhytomer:
            if (self.plant.pInternode.firstInternodeCurvingIndex == 0):
                self.internodeAngle = 0
            else:
                self.internodeAngle = 64.0 / 100.0 * (self.plant.randomNumberGenerator.randomNormalPercent(self.plant.pInternode.firstInternodeCurvingIndex))
        else:
            if (self.plant.pInternode.curvingIndex == 0):
                self.internodeAngle = 0
            else:
                self.internodeAngle = 64.0 / 100.0 * (self.plant.randomNumberGenerator.randomNormalPercent(self.plant.pInternode.curvingIndex))
        self.internodeAngle = self.angleWithSway(self.internodeAngle)
    
    def distanceFromApicalMeristem(self):
        result = 0L
        aPhytomer = PdInternode()
        
        #Count phytomers along this apex until you reach an apical meristem or inflorescence.
        result = 0
        if (self.nextPlantPart.isPhytomer()):
            aPhytomer = PdInternode(self.nextPlantPart)
        else:
            aPhytomer = None
        while aPhytomer != None:
            result += 1
            if (aPhytomer.nextPlantPart.isPhytomer()):
                aPhytomer = PdInternode(aPhytomer.nextPlantPart)
            else:
                aPhytomer = None
        return result
    
    def calculateDistanceFromFirstPhytomer(self):
        aPhytomer = PdInternode()
        result = 0L
        
        #Count phytomers backwards along this apex until you reach the first.
        result = 0
        if self.isFirstPhytomer:
            return
        aPhytomer = self.phytomerAttachedTo
        while aPhytomer != None:
            result += 1
            aPhytomer = aPhytomer.phytomerAttachedTo
        self.distanceFromFirstPhytomer = result
    
    def firstPhytomerOnBranch(self):
        result = PdInternode()
        result = self
        while result != None:
            if (result.phytomerAttachedTo != None) and (result.phytomerAttachedTo.nextPlantPart == result):
                result = PdInternode(result.phytomerAttachedTo)
            else:
                break
        if result == self:
            result = None
        return result
    
    def biomassOfMeAndAllPartsConnectedToMe_pctMPB(self):
        result = 0.0
        result = self.totalBiomass_pctMPB()
        if self.leftLeaf != None:
            result = result + self.leftLeaf.totalBiomass_pctMPB()
        if self.rightLeaf != None:
            result = result + self.rightLeaf.totalBiomass_pctMPB()
        return result
    
    def biomassOfPartsImmediatelyAboveMe_pctMPB(self):
        result = 0.0
        result = 0
        if self.leftBranchPlantPart != None:
            result = result + self.leftBranchPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB
        if self.rightBranchPlantPart != None:
            result = result + self.rightBranchPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB
        if self.nextPlantPart != None:
            result = result + self.nextPlantPart.biomassOfMeAndAllPartsAboveMe_pctMPB
        return result
    
    def draw(self):
        turtle = KfTurtle()
        
        #Draw all parts of phytomer. Consider if the phytomer is the first (has the seedling leaves) and whether
        #    the leaves attached to this phytomer have abscissed (and are not drawn).
        turtle = self.plant.turtle
        if (turtle == None):
            return
        self.boundsRect = Rect(0, 0, 0, 0)
        if self.hiddenByAmendment():
            if self.leftLeaf != None:
                # if internode is hidden the leaves could still be drawn, if they are posed.
                # if they are themselves hidden, they will pop back out without drawing.
                self.leftLeaf.drawWithDirection(uplant.kDirectionLeft)
            if self.rightLeaf != None:
                self.rightLeaf.drawWithDirection(uplant.kDirectionRight)
            # amendment rotations handled in drawStemSegment
            return
        try:
            if self.plant.needToRecalculateColors:
                self.calculateColors()
            if (self.isFirstPhytomer) and (self.plant.pRoot.showsAboveGround):
                self.drawRootTop()
            self.drawInternode()
            if self.leftLeaf != None:
                self.leftLeaf.drawWithDirection(uplant.kDirectionLeft)
            if self.rightLeaf != None:
                self.rightLeaf.drawWithDirection(uplant.kDirectionRight)
        except Exception, e:
            usupport.messageForExceptionType(e, "PdInternode.draw")
    
    def drawInternode(self):
        length = 0.0
        width = 0.0
        zAngle = 0.0
        
        if (self.plant.turtle == None):
            return
        zAngle = self.internodeAngle
        if (self.phytomerAttachedTo != None):
            if (self.phytomerAttachedTo.leftBranchPlantPart == self):
                zAngle = zAngle + self.plant.pMeristem.branchingAngle
            elif (self.phytomerAttachedTo.rightBranchPlantPart == self):
                zAngle = zAngle + self.plant.pMeristem.branchingAngle
                self.plant.turtle.rotateX(128)
        len = umath.max(0.0, self.propFullLength() * self.plant.pInternode.lengthAtOptimalFinalBiomassAndExpansion_mm)
        width = umath.max(0.0, self.propFullWidth() * self.plant.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm)
        self.drawStemSegment(len, width, zAngle, 0, self.internodeColor, upart.kDontTaper, u3dexport.kExportPartInternode, upart.kUseAmendment)
    
    def drawRootTop(self):
        turtle = KfTurtle()
        scale = 0.0
        numParts = 0
        tdo = KfObject3D()
        minZ = 0.0
        i = 0
        
        #Draw top of root above ground, if it can be seen. Adjust size for heat unit index of plant. 
        #constant
        numParts = 5
        turtle = self.plant.turtle
        if (turtle == None):
            return
        scale = umath.safedivExcept(self.plant.age, self.plant.pGeneral.ageAtMaturity, 0) * self.plant.pRoot.tdoParams.scaleAtFullSize / 100.0
        turtle.push()
        minZ = 0
        tdo = self.plant.pRoot.tdoParams.object3D
        turtle.ifExporting_startPlantPart(self.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartRootTop), self.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartRootTop))
        if numParts > 0:
            for i in range(0, numParts):
                turtle.rotateX(256 / numParts)
                turtle.push()
                turtle.rotateZ(64)
                turtle.rotateY(-64)
                if tdo != None:
                    turtle.rotateX(self.angleWithSway(self.plant.pRoot.tdoParams.xRotationBeforeDraw))
                    turtle.rotateY(self.angleWithSway(self.plant.pRoot.tdoParams.yRotationBeforeDraw))
                    turtle.rotateZ(self.angleWithSway(self.plant.pRoot.tdoParams.zRotationBeforeDraw))
                    self.draw3DObject(tdo, scale, self.plant.pRoot.tdoParams.faceColor, self.plant.pRoot.tdoParams.backfaceColor, u3dexport.kExportPartRootTop)
                    if i == 1:
                        minZ = tdo.zForSorting
                    elif tdo.zForSorting < minZ:
                        minZ = tdo.zForSorting
                turtle.pop()
        if tdo != None:
            tdo.zForSorting = minZ
        turtle.pop()
        turtle.ifExporting_endPlantPart()
    
    def report(self):
        PdPlantPart.report(self)
        #debugPrint('internode, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
        #DebugForm.printNested(plant.turtle.stackSize, 'phytomer, age ' + IntToStr(age));
    
    def checkIfSeedlingLeavesHaveAbscissed(self):
        if (not self.isFirstPhytomer):
            #If first phytomer, only want to draw seedling leaves for some time after emergence.
            #  For monopodial plant, stop drawing seedling leaves some number of nodes after emergence (parameter).
            #  For sympodial plant, this doesn't work; use age of meristem instead; age is set as constant.
            return
        if (self.plant.pMeristem.branchingIsSympodial):
            if (self.age < 10):
                return
        else:
            if (self.distanceFromApicalMeristem() <= self.plant.pSeedlingLeaf.nodesOnStemWhenFallsOff):
                return
        if umath.safedivExcept(self.plant.age, self.plant.pGeneral.ageAtMaturity, 0) < 0.25:
            # absolute cut-off 
            return
        if self.leftLeaf != None:
            # CFK FIX - should really have removed biomass in seedling leaves from model plant 
            self.leftLeaf.hasFallenOff = true
        if self.rightLeaf != None:
            self.rightLeaf.hasFallenOff = true
    
    def partType(self):
        result = 0
        result = uplant.kPartTypePhytomer
        return result
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdInternode
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        PdPlantPart.streamDataWithFiler(self, filer, cvir)
        filer.streamColorRef(self.internodeColor)
        self.internodeAngle = filer.streamSingle(self.internodeAngle)
        self.lengthExpansion = filer.streamSingle(self.lengthExpansion)
        self.widthExpansion = filer.streamSingle(self.widthExpansion)
        self.boltingExpansion = filer.streamSingle(self.boltingExpansion)
        self.fractionOfOptimalInitialBiomassAtCreation_frn = filer.streamSingle(self.fractionOfOptimalInitialBiomassAtCreation_frn)
        self.traversingDirection = filer.streamByte(self.traversingDirection)
        self.isFirstPhytomer = filer.streamBoolean(self.isFirstPhytomer)
        self.newBiomassForDay_pctMPB = filer.streamSingle(self.newBiomassForDay_pctMPB)
        #reading or writing the plant part subobject phytomers will be done by traverser
        #for now, just need to create these objects if needed and set plant and phytomerAttachedTo
        #if it is an inflorescence - read it now
        self.streamPlantPart(filer, self.leftBranchPlantPart)
        self.streamPlantPart(filer, self.rightBranchPlantPart)
        self.streamPlantPart(filer, self.nextPlantPart)
        self.streamPlantPart(filer, upart.PdPlantPart(self.leftLeaf))
        self.streamPlantPart(filer, upart.PdPlantPart(self.rightLeaf))
    
    def streamPlantPart(self, filer, plantPart):
        raise "method streamPlantPart had assigned to var parameter plantPart not added to return; fixup manually"
        partType = 0
        
        if filer.isWriting():
            if plantPart == None:
                partType = uplant.kPartTypeNone
            else:
                partType = plantPart.partType()
            partType = filer.streamSmallint(partType)
            if partType == uplant.kPartTypeMeristem:
                plantPart.streamUsingFiler(filer)
            elif partType == uplant.kPartTypeInflorescence:
                plantPart.streamUsingFiler(filer)
            elif partType == uplant.kPartTypeLeaf:
                plantPart.streamUsingFiler(filer)
        elif filer.isReading():
            partType = filer.streamSmallint(partType)
            if partType == uplant.kPartTypeNone:
                plantPart = None
            elif partType == uplant.kPartTypeMeristem:
                plantPart = umerist.PdMeristem().create()
                plantPart.plant = self.plant
                umerist.PdMeristem(plantPart).phytomerAttachedTo = self
                plantPart.streamUsingFiler(filer)
            elif partType == uplant.kPartTypeInflorescence:
                plantPart = uinflor.PdInflorescence().create()
                plantPart.plant = self.plant
                uinflor.PdInflorescence(plantPart).phytomerAttachedTo = self
                plantPart.streamUsingFiler(filer)
            elif partType == uplant.kPartTypePhytomer:
                plantPart = PdInternode().create()
                plantPart.plant = self.plant
                PdInternode(plantPart).phytomerAttachedTo = self
                #will be streamed in by traverser
            elif partType == uplant.kPartTypeLeaf:
                plantPart = uleaf.PdLeaf().create()
                plantPart.plant = self.plant
                plantPart.streamUsingFiler(filer)
                # PDF PORT inserted semicolon
            else :
                GeneralException.create("PdInternode: unknown plant part type " + IntToStr(partType))
    
