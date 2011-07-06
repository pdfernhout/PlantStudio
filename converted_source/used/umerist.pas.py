# unit umerist

from conversion_common import *
import usupport
import uclasses
import uleaf
import uinflor
import umath
import utdo
import udomain
import u3dexport
import uturtle
import udebug
import utravers
import ufiler
import uplant
import uintern
import upart
import delphi_compatability

class PdMeristem(PdPlantPart):
    def __init__(self):
        self.phytomerAttachedTo = PdInternode()
        self.daysCreatingThisPlantPart = 0L
        self.isActive = false
        self.isApical = false
        self.isReproductive = false
        self.gender = 0
    
    def newWithPlant(self, aPlant):
        self.create()
        self.InitializeWithPlant(aPlant)
        return self
    
    def destroy(self):
        if self.isReproductive:
            if self.isActive:
                if self.isApical:
                    #not isApical
                    self.plant.numApicalActiveReproductiveMeristemsOrInflorescences -= 1
                else:
                    self.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences -= 1
                #not isActive
            else:
                if self.isApical:
                    #not isApical
                    self.plant.numApicalInactiveReproductiveMeristems -= 1
                else:
                    self.plant.numAxillaryInactiveReproductiveMeristems -= 1
        PdPlantPart.destroy(self)
    
    def InitializeWithPlant(self, aPlant):
        # v1.6b1 removed inherited
        self.initialize(aPlant)
        # don't need to call any setIf... functions here because lists don't need to be changed yet 
        self.isApical = true
        self.liveBiomass_pctMPB = 0.0
        self.deadBiomass_pctMPB = 0.0
        self.biomassDemand_pctMPB = 0.0
        self.daysCreatingThisPlantPart = 0
        self.isActive = false
        self.isReproductive = false
        self.gender = uplant.kGenderFemale
        if self.plant.floweringHasStarted and (self.plant.randomNumberGenerator.zeroToOne() <= self.plant.pMeristem.determinateProbability):
            self.setIfReproductive(true)
    
    def getName(self):
        result = ""
        result = "meristem"
        return result
    
    def nextDay(self):
        try:
            PdPlantPart.nextDay(self)
            if self.isActive:
                self.daysCreatingThisPlantPart += 1
                if not self.isReproductive:
                    self.accumulateOrCreatePhytomer()
                else:
                    self.accumulateOrCreateInflorescence()
            else:
                if not self.isApical and not self.isReproductive and self.contemplateBranching():
                    self.setIfActive(true)
        except Exception, e:
            usupport.messageForExceptionType(e, "PdMeristem.nextDay")
    
    def contemplateBranching(self):
        result = false
        decisionPercent = 0.0
        randomPercent = 0.0
        firstOnBranch = PdInternode()
        
        if self.plant.pMeristem.branchingIndex == 0:
            #Decide if this meristem is going to become active and branch (start demanding photosynthate).
            #This method is called once per day to create a large pool of random tests, each with
            #very small probability, leading to a small number of occurrences with small variation.
            result = false
            return result
        if not self.plant.pMeristem.secondaryBranchingIsAllowed:
            firstOnBranch = self.phytomerAttachedTo.firstPhytomerOnBranch()
            if (firstOnBranch != self.plant.firstPhytomer):
                result = false
                return result
        if self.plant.pMeristem.branchingIndex == 100:
            result = true
            return result
        if self.phytomerAttachedTo.distanceFromApicalMeristem() < self.plant.pMeristem.branchingDistance:
            if self.plant.pMeristem.branchingDistance == 0:
                decisionPercent = self.plant.pMeristem.branchingIndex
            else:
                decisionPercent = self.plant.pMeristem.branchingIndex * umath.min(1.0, umath.max(0.0, umath.safedivExcept(self.phytomerAttachedTo.distanceFromApicalMeristem(), self.plant.pMeristem.branchingDistance, 0)))
            randomPercent = self.plant.randomNumberGenerator.randomPercent()
            result = randomPercent < decisionPercent
        else:
            decisionPercent = self.plant.pMeristem.branchingIndex
            randomPercent = self.plant.randomNumberGenerator.randomPercent()
            result = randomPercent < decisionPercent
        return result
    
    def optimalInitialPhytomerBiomass_pctMPB(self):
        result = 0.0
        result = uintern.PdInternode.optimalInitialBiomass_pctMPB(self.plant) + uleaf.PdLeaf.optimalInitialBiomass_pctMPB(self.plant)
        if self.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementOpposite:
            result = result + uleaf.PdLeaf.optimalInitialBiomass_pctMPB(self.plant)
        return result
    
    def accumulateOrCreatePhytomer(self):
        optimalInitialBiomass_pctMPB = 0.0
        minBiomassNeeded_pctMPB = 0.0
        fractionOfOptimalSize = 0.0
        shouldCreatePhytomer = false
        
        try:
            shouldCreatePhytomer = false
            optimalInitialBiomass_pctMPB = self.optimalInitialPhytomerBiomass_pctMPB()
            if (self.liveBiomass_pctMPB >= optimalInitialBiomass_pctMPB):
                shouldCreatePhytomer = true
            else:
                minBiomassNeeded_pctMPB = optimalInitialBiomass_pctMPB * self.plant.pInternode.minFractionOfOptimalInitialBiomassToCreateInternode_frn
                if (self.liveBiomass_pctMPB >= minBiomassNeeded_pctMPB) and (self.daysCreatingThisPlantPart >= self.plant.pInternode.maxDaysToCreateInternodeIfOverMinFraction):
                    shouldCreatePhytomer = true
            if shouldCreatePhytomer:
                fractionOfOptimalSize = umath.safedivExcept(self.liveBiomass_pctMPB, optimalInitialBiomass_pctMPB, 0)
                self.createPhytomer(fractionOfOptimalSize)
                self.liveBiomass_pctMPB = 0.0
                self.daysCreatingThisPlantPart = 0
        except Exception, e:
            usupport.messageForExceptionType(e, "PdMeristem.accumulateOrCreatePhytomer")
    
    def accumulateOrCreateInflorescence(self):
        optimalInitialBiomass_pctMPB = 0.0
        minBiomassNeeded_pctMPB = 0.0
        fractionOfOptimalSize = 0.0
        shouldCreateInflorescence = false
        
        try:
            if self.phytomerAttachedTo.isFirstPhytomer or not self.isReproductive or not self.isActive:
                return
            shouldCreateInflorescence = false
            optimalInitialBiomass_pctMPB = uinflor.PdInflorescence.optimalInitialBiomass_pctMPB(self.plant, self.gender)
            if (self.liveBiomass_pctMPB >= optimalInitialBiomass_pctMPB):
                shouldCreateInflorescence = true
            else:
                minBiomassNeeded_pctMPB = optimalInitialBiomass_pctMPB * self.plant.pInternode.minFractionOfOptimalInitialBiomassToCreateInternode_frn
                if (self.liveBiomass_pctMPB >= minBiomassNeeded_pctMPB) and (self.daysCreatingThisPlantPart >= self.plant.pInflor[self.gender].maxDaysToCreateInflorescenceIfOverMinFraction):
                    shouldCreateInflorescence = true
            if shouldCreateInflorescence:
                fractionOfOptimalSize = umath.safedivExcept(self.liveBiomass_pctMPB, optimalInitialBiomass_pctMPB, 0)
                self.createInflorescence(fractionOfOptimalSize)
                self.liveBiomass_pctMPB = 0.0
                self.daysCreatingThisPlantPart = 0
        except Exception, e:
            usupport.messageForExceptionType(e, "PdMeristem.accumulateOrCreateInflorescence")
    
    def traverseActivity(self, mode, traverserProxy):
        traverser = PdTraverser()
        optimalBiomass_pctMPB = 0.0
        biomassToRemove_pctMPB = 0.0
        
        PdPlantPart.traverseActivity(self, mode, traverserProxy)
        traverser = utravers.PdTraverser(traverserProxy)
        if traverser == None:
            return
        if self.hasFallenOff and (mode != utravers.kActivityStream) and (mode != utravers.kActivityFree):
            return
        try:
            if mode == utravers.kActivityNone:
                pass
            elif mode == utravers.kActivityNextDay:
                self.nextDay()
            elif mode == utravers.kActivityDemandVegetative:
                if (not self.isActive) or (self.isReproductive):
                    # return vegetative demand to create a phytomer. no demand if meristem is inactive, meristem is
                    # in reproductive mode, or if meristem is axillary and attached to the first phytomer
                    # and there is NOT sympodial branching.
                    return
                if ((not self.isApical) and (self.phytomerAttachedTo.isFirstPhytomer) and (not self.plant.pMeristem.branchingIsSympodial)):
                    return
                try:
                    optimalBiomass_pctMPB = uintern.PdInternode.optimalInitialBiomass_pctMPB(self.plant) + uleaf.PdLeaf.optimalInitialBiomass_pctMPB(self.plant)
                    if self.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementOpposite:
                        optimalBiomass_pctMPB = optimalBiomass_pctMPB + uleaf.PdLeaf.optimalInitialBiomass_pctMPB(self.plant)
                    self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, optimalBiomass_pctMPB, self.plant.pInternode.minDaysToCreateInternode)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (vegetative demand)")
            elif mode == utravers.kActivityDemandReproductive:
                if (not self.isActive) or (not self.isReproductive):
                    # return reproductive demand to create an inflorescence. no demand if meristem is inactive,
                    # if it is in vegetative mode, or if it is attached to the first phytomer.
                    return
                if (self.phytomerAttachedTo.isFirstPhytomer) and (not self.isApical):
                    return
                try:
                    self.biomassDemand_pctMPB = utravers.linearGrowthResult(self.liveBiomass_pctMPB, self.plant.pInflor[self.gender].optimalBiomass_pctMPB, self.plant.pInflor[self.gender].minDaysToCreateInflorescence)
                    traverser.total = traverser.total + self.biomassDemand_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (reproductive demand)")
            elif mode == utravers.kActivityGrowVegetative:
                if not (self.isActive):
                    #Allocate new biomass by portion of demand. A phytomer cannot be made before the minimum number
                    #      of days has passed to make one phytomer.
                    return
                if self.isReproductive:
                    return
                try:
                    self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (vegetative growth)")
            elif mode == utravers.kActivityGrowReproductive:
                if (not self.isActive) or (not self.isReproductive):
                    return
                try:
                    self.liveBiomass_pctMPB = self.liveBiomass_pctMPB + self.biomassDemand_pctMPB * traverser.fractionOfPotentialBiomass
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (reproductive growth)")
            elif mode == utravers.kActivityStartReproduction:
                self.startReproduction()
            elif mode == utravers.kActivityFindPlantPartAtPosition:
                if umath.pointsAreCloseEnough(traverser.point, self.position()):
                    traverser.foundPlantPart = self
                    traverser.finished = true
            elif mode == utravers.kActivityDraw:
                self.draw()
            elif mode == utravers.kActivityReport:
                pass
            elif mode == utravers.kActivityStream:
                pass
            elif mode == utravers.kActivityFree:
                pass
            elif mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved:
                if not self.isActive:
                    #called by phytomer
                    # free called by phytomer or inflorescence 
                    return
                if (mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved) and (self.isReproductive):
                    return
                if (mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved) and (not self.isReproductive):
                    return
                try:
                    # a meristem can lose all of its biomass 
                    traverser.total = traverser.total + self.liveBiomass_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (removal request)")
            elif mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved:
                if not self.isActive:
                    #called by phytomer
                    # free called by phytomer or inflorescence 
                    return
                if (mode == utravers.kActivityVegetativeBiomassThatCanBeRemoved) and (self.isReproductive):
                    return
                if (mode == utravers.kActivityReproductiveBiomassThatCanBeRemoved) and (not self.isReproductive):
                    return
                try:
                    # a meristem can lose all of its biomass 
                    traverser.total = traverser.total + self.liveBiomass_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (removal request)")
            elif mode == utravers.kActivityRemoveVegetativeBiomass:
                if not self.isActive:
                    return
                if (mode == utravers.kActivityRemoveVegetativeBiomass) and (self.isReproductive):
                    return
                if (mode == utravers.kActivityRemoveReproductiveBiomass) and (not self.isReproductive):
                    return
                try:
                    biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                    self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                    self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (removal)")
            elif mode == utravers.kActivityRemoveReproductiveBiomass:
                if not self.isActive:
                    return
                if (mode == utravers.kActivityRemoveVegetativeBiomass) and (self.isReproductive):
                    return
                if (mode == utravers.kActivityRemoveReproductiveBiomass) and (not self.isReproductive):
                    return
                try:
                    biomassToRemove_pctMPB = self.liveBiomass_pctMPB * traverser.fractionOfPotentialBiomass
                    self.liveBiomass_pctMPB = self.liveBiomass_pctMPB - biomassToRemove_pctMPB
                    self.deadBiomass_pctMPB = self.deadBiomass_pctMPB + biomassToRemove_pctMPB
                except Exception, e:
                    usupport.messageForExceptionType(e, "PdMeristem.traverseActivity (removal)")
            elif mode == utravers.kActivityGatherStatistics:
                self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAxillaryBud)
                if self.isReproductive:
                    self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllReproductive)
                else:
                    self.addToStatistics(traverser.statistics, utravers.kStatisticsPartTypeAllVegetative)
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
                raise GeneralException.create("Problem: Unhandled mode in method PdMeristem.traverseActivity.")
        except Exception, e:
            usupport.messageForExceptionType(e, "PdMeristem.traverseActivity")
    
    def countPointsAndTrianglesFor3DExportAndAddToTraverserTotals(self, traverser):
        if traverser == None:
            return
        if self.plant.pAxillaryBud.tdoParams.scaleAtFullSize > 0:
            traverser.total3DExportPointsIn3DObjects += self.plant.pAxillaryBud.tdoParams.object3D.pointsInUse * self.plant.pAxillaryBud.tdoParams.repetitions
            traverser.total3DExportTrianglesIn3DObjects += self.plant.pAxillaryBud.tdoParams.object3D.triangles.Count * self.plant.pAxillaryBud.tdoParams.repetitions
            self.addExportMaterial(traverser, u3dexport.kExportPartMeristem, -1)
    
    def report(self):
        PdPlantPart.report(self)
        #debugPrint('meristem, age ' + IntToStr(age) + ' biomass ' + floatToStr(liveBiomass_pctMPB));
        #DebugForm.printNested(plant.turtle.stackSize, 'meristem, age ' + IntToStr(age) + ' biomass '
        #    + floatToStr(liveBiomass_pctMPB));
    
    def createAxillaryMeristem(self, direction):
        result = PdMeristem()
        newMeristem = PdMeristem()
        
        # create new axillary meristem attached to the same phytomer as this apical meristem is attached to.
        newMeristem = PdMeristem().create()
        newMeristem.InitializeWithPlant(self.plant)
        newMeristem.setIfApical(false)
        newMeristem.phytomerAttachedTo = self.phytomerAttachedTo
        if (direction == uplant.kDirectionLeft):
            self.phytomerAttachedTo.leftBranchPlantPart = newMeristem
        else:
            self.phytomerAttachedTo.rightBranchPlantPart = newMeristem
        result = newMeristem
        return result
    
    def setIfActive(self, active):
        if self.isActive != active:
            self.isActive = active
            if self.isReproductive:
                if self.isApical:
                    if self.isActive:
                        self.plant.numApicalActiveReproductiveMeristemsOrInflorescences += 1
                        self.plant.numApicalInactiveReproductiveMeristems -= 1
                        #not isActive
                    else:
                        self.plant.numApicalInactiveReproductiveMeristems += 1
                        self.plant.numApicalActiveReproductiveMeristemsOrInflorescences -= 1
                    #not isApical
                else:
                    if self.isActive:
                        self.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences += 1
                        self.plant.numAxillaryInactiveReproductiveMeristems -= 1
                        #not isActive
                    else:
                        self.plant.numAxillaryInactiveReproductiveMeristems += 1
                        self.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences -= 1
    
    def setIfApical(self, apical):
        if self.isApical != apical:
            self.isApical = apical
            if self.isReproductive:
                if self.isActive:
                    if self.isApical:
                        self.plant.numApicalActiveReproductiveMeristemsOrInflorescences += 1
                        self.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences -= 1
                        #not isApical
                    else:
                        self.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences += 1
                        self.plant.numApicalActiveReproductiveMeristemsOrInflorescences -= 1
                    #not isActive
                else:
                    if self.isApical:
                        self.plant.numApicalInactiveReproductiveMeristems += 1
                        self.plant.numAxillaryInactiveReproductiveMeristems -= 1
                        #not isApical
                    else:
                        self.plant.numAxillaryInactiveReproductiveMeristems += 1
                        self.plant.numApicalInactiveReproductiveMeristems -= 1
    
    def setIfReproductive(self, reproductive):
        if self.isReproductive != reproductive:
            #assume can only become reproductive and not go other way
            self.isReproductive = reproductive
            if self.isActive:
                if self.isApical:
                    #not isApical
                    self.plant.numApicalActiveReproductiveMeristemsOrInflorescences += 1
                else:
                    self.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences += 1
                #not isActive
            else:
                if self.isApical:
                    #not isApical
                    self.plant.numApicalInactiveReproductiveMeristems += 1
                else:
                    self.plant.numAxillaryInactiveReproductiveMeristems += 1
    
    # create first phytomer of plant with optimal biomass. return phytomer created so plant can hold on to it.
    def createFirstPhytomer(self):
        result = PdInternode()
        result = None
        try:
            #CreatePhytomer(self.optimalInitialPhytomerBiomass_pctMPB);
            # v1.6b1 -- biomass was wrong, should be fraction
            self.createPhytomer(1.0)
            result = self.phytomerAttachedTo
            if self.plant.pGeneral.isDicot:
                result.makeSecondSeedlingLeaf(self.optimalInitialPhytomerBiomass_pctMPB())
        except Exception, e:
            usupport.messageForExceptionType(e, "PdMeristem.createFirstPhytomer")
        return result
    
    # create new inflorescence. attach new inflor to phytomer this meristem is attached to,
    # then unattach this meristem from the phytomer and tell inflor pointer to self so inflor can free self
    # when it is freed.
    def createInflorescence(self, fractionOfOptimalSize):
        newInflorescence = PdInflorescence()
        
        if self.plant.partsCreated > udomain.domain.options.maxPartsPerPlant_thousands * 1000:
            # v1.6b1
            return
        newInflorescence = uinflor.PdInflorescence().create()
        newInflorescence.initializeGenderApicalOrAxillary(self.plant, self.gender, self.isApical, fractionOfOptimalSize)
        newInflorescence.meristemThatCreatedMe = self
        newInflorescence.phytomerAttachedTo = self.phytomerAttachedTo
        if self.isApical:
            self.phytomerAttachedTo.nextPlantPart = newInflorescence
        elif self.phytomerAttachedTo.leftBranchPlantPart == self:
            self.phytomerAttachedTo.leftBranchPlantPart = newInflorescence
        elif self.phytomerAttachedTo.rightBranchPlantPart == self:
            self.phytomerAttachedTo.rightBranchPlantPart = newInflorescence
        else:
            raise GeneralException.create("Problem: Branching incorrect in method PdMeristem.createInflorescence.")
        self.phytomerAttachedTo = None
    
    def createPhytomer(self, fractionOfFullSize):
        newPhytomer = PdInternode()
        leftMeristem = PdMeristem()
        rightMeristem = PdMeristem()
        
        if self.plant.partsCreated > udomain.domain.options.maxPartsPerPlant_thousands * 1000:
            # create new phytomer. fraction of full size is the amount of biomass the meristem accumulated
            # (in the number of days it had to create a phytomer) divided by the optimal biomass of a phytomer.
            # v1.6b1
            return
        newPhytomer = uintern.PdInternode.NewWithPlantFractionOfInitialOptimalSize(self.plant, fractionOfFullSize)
        newPhytomer.phytomerAttachedTo = self.phytomerAttachedTo
        if (self.phytomerAttachedTo != None):
            if self.isApical:
                self.phytomerAttachedTo.nextPlantPart = newPhytomer
                if (self.plant.pMeristem.branchingIsSympodial):
                    self.setIfActive(false)
                # axillary 
            else:
                if self.phytomerAttachedTo.leftBranchPlantPart == self:
                    self.phytomerAttachedTo.leftBranchPlantPart = newPhytomer
                elif self.phytomerAttachedTo.rightBranchPlantPart == self:
                    self.phytomerAttachedTo.rightBranchPlantPart = newPhytomer
                else:
                    raise GeneralException.create("Problem: Branching incorrect in method PdMeristem.createPhytomer.")
                self.setIfApical(true)
            # set up pointers
            self.phytomerAttachedTo = newPhytomer
            self.phytomerAttachedTo.nextPlantPart = self
            if self.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementAlternate:
                leftMeristem = self.createAxillaryMeristem(uplant.kDirectionLeft)
                if self.plant.pMeristem.branchingIsSympodial:
                    leftMeristem.setIfActive(true)
            else:
                leftMeristem = self.createAxillaryMeristem(uplant.kDirectionLeft)
                rightMeristem = self.createAxillaryMeristem(uplant.kDirectionRight)
                if self.plant.pMeristem.branchingIsSympodial:
                    if (self.plant.randomNumberGenerator.zeroToOne() < 0.5):
                        leftMeristem.setIfActive(true)
                    else:
                        rightMeristem.setIfActive(true)
            # phytomerAttachedTo = nil (means this is first phytomer)
        else:
            self.setIfApical(true)
            self.setIfActive(not self.plant.pMeristem.branchingIsSympodial)
            # set up pointers
            self.phytomerAttachedTo = newPhytomer
            self.phytomerAttachedTo.nextPlantPart = self
            if self.plant.pMeristem.branchingIsSympodial:
                if self.plant.pMeristem.branchingAndLeafArrangement == uplant.kArrangementAlternate:
                    leftMeristem = self.createAxillaryMeristem(uplant.kDirectionLeft)
                    leftMeristem.setIfActive(true)
                else:
                    leftMeristem = self.createAxillaryMeristem(uplant.kDirectionLeft)
                    rightMeristem = self.createAxillaryMeristem(uplant.kDirectionRight)
                    if (self.plant.randomNumberGenerator.zeroToOne() < 0.5):
                        leftMeristem.setIfActive(true)
                    else:
                        rightMeristem.setIfActive(true)
    
    def draw(self):
        i = 0
        
        turtle = KfTurtle()
        scale = 0.0
        daysToFullSize = 0.0
        numParts = 0
        tdo = KfObject3D()
        minZ = 0.0
        
        if (self.plant.pAxillaryBud.tdoParams.scaleAtFullSize == 0):
            return
        #Draw meristem (only if buds are enlarged as in Brussels sprouts). Since this only very rarely happens,
        #  have these buds increase to maximum size in a constant number of days (5). Number of sections drawn
        #  (of the 3D object being rotated) is also set to a constant (5).
        turtle = self.plant.turtle
        if (turtle == None):
            return
        self.boundsRect = Rect(0, 0, 0, 0)
        if self.hiddenByAmendment():
            return
        else:
            self.applyAmendmentRotations()
        daysToFullSize = 5
        scale = (self.plant.pAxillaryBud.tdoParams.scaleAtFullSize / 100.0) * (umath.min(1.0, umath.safedivExcept(self.age, daysToFullSize, 0)))
        if self.isApical:
            return
        try:
            numParts = 5
            minZ = 0
            tdo = self.plant.pAxillaryBud.tdoParams.object3D
            turtle.ifExporting_startPlantPart(self.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartMeristem), self.longNameForDXFPartConsideringGenderEtc(u3dexport.kExportPartMeristem))
            if numParts > 0:
                for i in range(0, numParts):
                    turtle.rotateX(256 / numParts)
                    turtle.push()
                    turtle.rotateZ(-64)
                    if tdo != None:
                        turtle.rotateX(self.angleWithSway(self.plant.pAxillaryBud.tdoParams.xRotationBeforeDraw))
                        turtle.rotateY(self.angleWithSway(self.plant.pAxillaryBud.tdoParams.yRotationBeforeDraw))
                        turtle.rotateZ(self.angleWithSway(self.plant.pAxillaryBud.tdoParams.zRotationBeforeDraw))
                        self.draw3DObject(tdo, scale, self.plant.pAxillaryBud.tdoParams.faceColor, self.plant.pAxillaryBud.tdoParams.backfaceColor, u3dexport.kExportPartMeristem)
                        if i == 1:
                            minZ = tdo.zForSorting
                        elif tdo.zForSorting < minZ:
                            minZ = tdo.zForSorting
                    turtle.pop()
            if tdo != None:
                tdo.zForSorting = minZ
            turtle.ifExporting_endPlantPart()
        except Exception, e:
            usupport.messageForExceptionType(e, "PdMeristem.draw")
    
    def startReproduction(self):
        if (self.plant.randomNumberGenerator.zeroToOne() <= self.plant.pMeristem.determinateProbability):
            #Decide gender and activity based on whether the plant has hermaphroditic or separate flowers, and if
            #    hermaphroditic, female and/or male flowers are located terminally or axially.
            self.setIfReproductive(true)
        if not self.isReproductive:
            return
        self.setIfActive(false)
        self.gender = uplant.kGenderFemale
        if not self.plant.pGeneral.maleFlowersAreSeparate:
            if self.decideIfActiveHermaphroditic():
                self.gender = uplant.kGenderFemale
        else:
            if self.decideIfActiveMale():
                self.gender = uplant.kGenderMale
            if self.decideIfActiveFemale():
                self.gender = uplant.kGenderFemale
        if self.willCreateInflorescence():
            self.setIfActive(true)
    
    def decideIfActiveFemale(self):
        result = false
        #For the case of separate male and female flowers, decide if this meristem will be able to create
        #  a female inflorescence. Called by decideReproductiveGenderAndActivity.
        #If meristem is already male, then both male and female flowers are apical (or axillary).
        #  in that case, override with female only half the time.
        result = (self.isApical == self.plant.pInflor[uplant.kGenderFemale].isTerminal)
        if result and (self.gender == uplant.kGenderMale):
            result = (self.plant.randomNumberGenerator.zeroToOne() < 0.5)
        return result
    
    def decideIfActiveHermaphroditic(self):
        result = false
        #For the case of hermaphroditic flowers, decide if this meristem will be able to create
        #  a hermaphroditic inflorescence (if flowers are hermaphroditic, female parameters are used).
        #  Called by decideReproductiveGenderAndActivity.
        result = (self.isApical == self.plant.pInflor[uplant.kGenderFemale].isTerminal)
        return result
    
    def decideIfActiveMale(self):
        result = false
        #For the case of separate male and female flowers, decide if this meristem will be able to create
        #  a male inflorescence. Called by decideReproductiveGenderAndActivity.
        result = (self.isApical == self.plant.pInflor[uplant.kGenderMale].isTerminal)
        return result
    
    def partType(self):
        result = 0
        result = uplant.kPartTypeMeristem
        return result
    
    def willCreateInflorescence(self):
        result = false
        inflorProb = 0.0
        numExpected = 0.0
        numAlready = 0.0
        
        try:
            if (self.phytomerAttachedTo.isFirstPhytomer) and (not self.isApical):
                #Determine probability that this meristem will produce an inflorescence, which is
                #  number of inflorescences left to be placed on plant / number of meristems open to develop
                #  (apical meristems if flowering is apical, or axillary meristems if flowering is axillary).
                #  First phytomer on plant is for seedling leaves and cannot produce inflorescences.
                result = false
                return result
            if self.isApical:
                numExpected = self.plant.pGeneral.numApicalInflors
                numAlready = self.plant.numApicalActiveReproductiveMeristemsOrInflorescences
                inflorProb = umath.safedivExcept(numExpected - numAlready, self.plant.numApicalInactiveReproductiveMeristems, 0)
            else:
                numExpected = self.plant.pGeneral.numAxillaryInflors
                numAlready = self.plant.numAxillaryActiveReproductiveMeristemsOrInflorescences
                inflorProb = umath.safedivExcept(numExpected - numAlready, self.plant.numAxillaryInactiveReproductiveMeristems, 0)
            if (numExpected <= 3):
                #If there are only a few inflorescences on the plant, don't mess with probability; place on
                #  first few meristems.
                inflorProb = 1.0
            if (self.plant.randomNumberGenerator.zeroToOne() < inflorProb):
                #Check that the expected number of inflorescences hasn't been created already.
                result = (numAlready < numExpected)
            else:
                result = false
        except Exception, e:
            result = false
            usupport.messageForExceptionType(e, "PdMeristem.willCreateInflorescence")
        return result
    
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdMeristem
        cvir.versionNumber = 0
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        PdPlantPart.streamDataWithFiler(self, filer, cvir)
        self.daysCreatingThisPlantPart = filer.streamLongint(self.daysCreatingThisPlantPart)
        self.isActive = filer.streamBoolean(self.isActive)
        self.isApical = filer.streamBoolean(self.isApical)
        self.isReproductive = filer.streamBoolean(self.isReproductive)
        self.gender = filer.streamSmallint(self.gender)
    
