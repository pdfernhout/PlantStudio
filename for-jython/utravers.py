# unit Utravers

from conversion_common import *
import delphi_compatability
import u3dexport
import umath

"""
import ubreedr
import utimeser
import umain
import uintern
import udebug
import usupport
import ufiler
import upart
import uplant
"""

# const
kTraverseNone = 0
kTraverseLeft = 1
kTraverseRight = 2
kTraverseNext = 3
kTraverseDone = 4
kActivityNone = 0
kActivityNextDay = 1
kActivityDemandVegetative = 2
kActivityDemandReproductive = 3
kActivityGrowVegetative = 4
kActivityGrowReproductive = 5
kActivityStartReproduction = 6
kActivityFindPlantPartAtPosition = 7
kActivityDraw = 8
kActivityReport = 9
kActivityStream = 10
kActivityFree = 11
kActivityVegetativeBiomassThatCanBeRemoved = 12
kActivityRemoveVegetativeBiomass = 13
kActivityReproductiveBiomassThatCanBeRemoved = 14
kActivityRemoveReproductiveBiomass = 15
kActivityGatherStatistics = 16
kActivityStandingDeadBiomassThatCanBeRemoved = 17
kActivityRemoveStandingDeadBiomass = 18
kActivityCountPlantParts = 19
kActivityFindPartForPartID = 20
kActivityCountTotalMemoryUse = 21
kActivityCalculateBiomassForGravity = 22
kActivityCountPointsAndTrianglesFor3DExport = 23

# const
kStatisticsPartTypeSeedlingLeaf = 0
kStatisticsPartTypeLeaf = 1
kStatisticsPartTypeFemaleInflorescence = 2
kStatisticsPartTypeMaleInflorescence = 3
kStatisticsPartTypeFemaleFlower = 4
kStatisticsPartTypeFemaleFlowerBud = 5
kStatisticsPartTypeMaleFlower = 6
kStatisticsPartTypeMaleFlowerBud = 7
kStatisticsPartTypeAxillaryBud = 8
kStatisticsPartTypeFruit = 9
kStatisticsPartTypeStem = 10
kStatisticsPartTypeUnripeFruit = 11
kStatisticsPartTypeFallenFruit = 12
kStatisticsPartTypeUnallocatedNewVegetativeBiomass = 13
kStatisticsPartTypeUnremovedDeadVegetativeBiomass = 14
kStatisticsPartTypeUnallocatedNewReproductiveBiomass = 15
kStatisticsPartTypeUnremovedDeadReproductiveBiomass = 16
kStatisticsPartTypeFallenFlower = 17
kStatisticsPartTypeAllVegetative = 18
kStatisticsPartTypeAllReproductive = 19
kStatisticsPartTypeLast = 19

# var
cancelDrawing = False
worstNStressColor = UnassignedColor
worstPStressColor = UnassignedColor
worstDeadColor = UnassignedColor

# -------------------------------------------------------------------------- linear growth functions 
def linearGrowthWithFactorResult(current, optimal, minDays, growthFactor):
    result = 0.0
    amountNeeded = 0.0
    maxPossible = 0.0
    
    result = 0.0
    try:
        amountNeeded = optimal - current
        maxPossible = umath.safedivExcept(optimal, minDays, optimal)
        amountNeeded = umath.max(0.0, umath.min(amountNeeded, maxPossible))
        result = amountNeeded * growthFactor
    except Exception, e:
        usupport.messageForExceptionType(e, "linearGrowthWithFactorResult")
    return result

def linearGrowthWithFactor(current, optimal, minDays, growthFactor):
    amountNeeded = 0.0
    maxPossible = 0.0
    
    try:
        amountNeeded = optimal - current
        maxPossible = umath.safedivExcept(optimal, minDays, optimal)
        amountNeeded = umath.max(0.0, umath.min(amountNeeded, maxPossible))
        current = current + amountNeeded * growthFactor
    except Exception, e:
        usupport.messageForExceptionType(e, "linearGrowthWithFactor")
    return current

def linearGrowthResult(current, optimal, minDays):
    result = 0.0
    amountNeeded = 0.0
    maxPossible = 0.0
    
    result = 0.0
    try:
        amountNeeded = optimal - current
        maxPossible = umath.safedivExcept(optimal, minDays, optimal)
        amountNeeded = umath.max(0.0, umath.min(amountNeeded, maxPossible))
        result = amountNeeded
    except Exception, e:
        usupport.messageForExceptionType(e, "linearGrowthResult")
    return result

def linearGrowth(current, optimal, minDays):
    amountNeeded = 0.0
    maxPossible = 0.0
    
    try:
        amountNeeded = optimal - current
        maxPossible = umath.safedivExcept(optimal, minDays, optimal)
        amountNeeded = umath.max(0.0, umath.min(amountNeeded, maxPossible))
        current = current + amountNeeded
    except Exception, e:
        usupport.messageForExceptionType(e, "linearGrowth")
    return current

# meristems
class PdPlantStatistics:
    def __init__(self):
        self.count = [0] * (kStatisticsPartTypeLast + 1)
        self.liveBiomass_pctMPB = [0.0] * (kStatisticsPartTypeLast + 1)
        self.deadBiomass_pctMPB = [0.0] * (kStatisticsPartTypeLast + 1)
    
    # ---------------------------------------------------------------------------------- statistics object 
    def zeroAllFields(self):
        for i in range(0, kStatisticsPartTypeLast + 1):
            self.count[i] = 0
            self.liveBiomass_pctMPB[i] = 0.0
            self.deadBiomass_pctMPB[i] = 0.0
    
    def totalBiomass_pctMPB(self):
        result = 0.0
        for i in range(0, kStatisticsPartTypeLast + 1):
            result = result + self.liveBiomass_pctMPB[i]
            result = result + self.deadBiomass_pctMPB[i]
        return result
    
class PdTraverser:
    def __init__(self):
        self.plant = None
        self.filer = None
        self.currentPhytomer = None
        self.point = delphi_compatability.TPoint()
        self.total = 0.0
        self.fractionOfPotentialBiomass = 0.0
        self.ageOfYoungestPhytomer = 0L
        self.mode = 0
        self.finished = False
        self.foundPlantPart = None
        #PDF PORT NOT USED? self.foundList = TList()
        self.statistics = PdPlantStatistics()
        self.totalPlantParts = 0L
        self.total3DExportPointsIn3DObjects = 0L
        self.total3DExportTrianglesIn3DObjects = 0L
        self.total3DExportStemSegments = 0L
        self.showDrawingProgress = False
        self.plantPartsDrawnAtStart = 0L
        self.partID = 0L
        self.totalMemorySize = 0L
        self.exportTypeCounts = [0] * (u3dexport.kExportPartLast + 1)
    
    # ---------------------------------------------------------------------------------- traversing object 
    def createWithPlant(self, thePlant):
        self.plant = thePlant
        return self
    
    def beginTraversal(self, aMode):
        self.mode = aMode
        self.currentPhytomer = self.plant.firstPhytomer
        self.total = 0.0
        self.finished = False
        self.foundPlantPart = None
        self.totalPlantParts = 0
        if self.currentPhytomer != None:
            self.currentPhytomer.traversingDirection = kTraverseLeft
            self.currentPhytomer.traverseActivity(self.mode, self)
            #reset afterwards in case read in differently
            self.currentPhytomer.traversingDirection = kTraverseLeft
    
    def traverseWholePlant(self, aMode):
        self.beginTraversal(aMode)
        self.traversePlant(0)
    
    def traversePlant(self, traversalCount):
        if (self.currentPhytomer == None):
            return
        phytomerTraversing = self.currentPhytomer
        i = 0
        while i <= traversalCount:
            if self.finished:
                return
            if phytomerTraversing.traversingDirection == kTraverseLeft:
                phytomerTraversing.traversingDirection += 1
                if phytomerTraversing.leftBranchPlantPart != None:
                    if (self.mode == kActivityDraw):
                        self.plant.turtle.push()
                    phytomerTraversing.leftBranchPlantPart.traverseActivity(self.mode, self)
                    if (phytomerTraversing.leftBranchPlantPart.isPhytomer()):
                        phytomerTraversing = phytomerTraversing.leftBranchPlantPart
                        phytomerTraversing.traversingDirection = kTraverseLeft
                    elif (self.mode == kActivityDraw):
                        self.plant.turtle.pop()
            elif phytomerTraversing.traversingDirection == kTraverseRight:
                phytomerTraversing.traversingDirection += 1
                if phytomerTraversing.rightBranchPlantPart != None:
                    if (self.mode == kActivityDraw):
                        self.plant.turtle.push()
                    phytomerTraversing.rightBranchPlantPart.traverseActivity(self.mode, self)
                    if (phytomerTraversing.rightBranchPlantPart.isPhytomer()):
                        phytomerTraversing = phytomerTraversing.rightBranchPlantPart
                        phytomerTraversing.traversingDirection = kTraverseLeft
                    elif (self.mode == kActivityDraw):
                        self.plant.turtle.pop()
            elif phytomerTraversing.traversingDirection == kTraverseNext:
                phytomerTraversing.traversingDirection += 1
                if phytomerTraversing.nextPlantPart != None:
                    if (self.mode == kActivityDraw):
                        self.plant.turtle.push()
                        self.plant.turtle.rotateX(self.plant.pGeneral.phyllotacticRotationAngle * 256 / 360)
                    phytomerTraversing.nextPlantPart.traverseActivity(self.mode, self)
                    if (phytomerTraversing.nextPlantPart.isPhytomer()):
                        phytomerTraversing = phytomerTraversing.nextPlantPart
                        phytomerTraversing.traversingDirection = kTraverseLeft
                    elif (self.mode == kActivityDraw):
                        self.plant.turtle.pop()
            elif phytomerTraversing.traversingDirection == kTraverseDone:
                phytomerTraversing.traversingDirection = kTraverseNone
                lastPhytomer = phytomerTraversing
                phytomerTraversing = phytomerTraversing.phytomerAttachedTo
                if (self.mode == kActivityFree):
                    if phytomerTraversing != None:
                        if (phytomerTraversing.traversingDirection == kTraverseLeft + 1):
                            phytomerTraversing.leftBranchPlantPart = None
                        elif (phytomerTraversing.traversingDirection == kTraverseRight + 1):
                            phytomerTraversing.rightBranchPlantPart = None
                        elif (phytomerTraversing.traversingDirection == kTraverseNext + 1):
                            phytomerTraversing.nextPlantPart = None
                if phytomerTraversing == None:
                    break
                if (self.mode == kActivityDraw):
                    #special drawing stuff - if returning from left or right branch draw, pop turtle
                    #	if (phytomerTraversing.traversingDirection = kTraverseLeft + 1)
                    #           or (phytomerTraversing.traversingDirection =  kTraverseRight + 1)  then 
                    self.plant.turtle.pop()
                if (self.mode == kActivityCalculateBiomassForGravity):
                    phytomerTraversing.traverseActivity(self.mode, self)
            elif phytomerTraversing.traversingDirection == kTraverseNone:
                raise GeneralException.create("Problem: kTraverseNone encountered in method PdTraverser.traversePlant.")
            if (traversalCount != 0):
                i += 1
            if (self.mode == kActivityDraw) and (self.showDrawingProgress):
                if self.totalPlantParts % 4 != 0:
                    continue
                # PDF PORT __ REMOPRARILY REMOVED FOR TESTING FIX
                #if (umain.MainForm != None) and (umain.MainForm.drawing):
                #    umain.MainForm.showDrawProgress(self.plantPartsDrawnAtStart + self.totalPlantParts)
    
