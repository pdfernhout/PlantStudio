# unit Uplant


# const
kGenderMale = 0
kGenderFemale = 1
kCompoundLeafPinnate = 0
kCompoundLeafPalmate = 1
kArrangementAlternate = 0
kArrangementOpposite = 1
kStageFlowerBud = 1
kStageOpenFlower = 2
kStageUnripeFruit = 3
kStageRipeFruit = 4
kPartTypeNone = 0
kPartTypeFlowerFruit = 1
kPartTypeInflorescence = 2
kPartTypeMeristem = 3
kPartTypePhytomer = 4
kPartTypeLeaf = 5
kDirectionLeft = 0
kDirectionRight = 1
kGetField = 0
kSetField = 1
kPlantNameLength = 80
kCheckForUnreadParams = True
kDontCheckForUnreadParams = False
kConsiderDomainScale = True
kDontConsiderDomainScale = False
kDrawNow = True
kDontDrawNow = False
kMutation = 0
kWeight = 1
kMaxBreedingSections = 20
kFromFirstPlant = 0
kFromSecondPlant = 1
kFromProbabilityBasedOnWeightsForSection = 2
kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant = 3
kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant = 4
kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly = 5
kPlantAsTextStartString = "start PlantStudio plant"
kPlantAsTextEndString = "end PlantStudio plant"
kStartNoteString = "=== start note"
kEndNoteString = "=== end note"
kInMainWindow = True
kNotInMainWindow = False
kBud = 0
kPistils = 1
kStamens = 2
kFirstPetals = 3
kSecondPetals = 4
kThirdPetals = 5
kFourthPetals = 6
kFifthPetals = 7
kSepals = 8
kHighestFloralPartConstant = kSepals
kDrawNoBud = 0
kDrawSingleTdoBud = 1
kDrawOpeningFlower = 2
kNotExactAge = False
kExactAge = True

# record
class BreedingAndTimeSeriesOptionsStructure:
    def __init__(self):
        self.mutationStrengths = [0] * (kMaxBreedingSections + 1)
        self.firstPlantWeights = [0] * (kMaxBreedingSections + 1)
        self.getNonNumericalParametersFrom = 0
        self.mutateAndBlendColorValues = True
        self.chooseTdosRandomlyFromCurrentLibrary = False
        self.percentMaxAge = 0.5
        self.plantsPerGeneration = 5
        self.variationType = 0
        self.thumbnailWidth = 32
        self.thumbnailHeight = 32
        self.maxGenerations = 30
        self.numTimeSeriesStages = 0
        
# PDF PORT __ MOVED DOWN HERE DUE TO CONFLICT WHEN LAODIGN DOMAIN>???

import copy

from conversion_common import *
import delphi_compatability
import urandom
import umath
import ubitmap
import ucollect
import utdo
import usupport
import uamendmt
import uparams
import utransfr
import utravers
import umerist
import udomain
import udebug
import ubmpsupport
import uturtle

"""
import ucursor
import utimeser
import usection
import uclasses
import uintern
import upart
import u3dexport
import umain
import ufiler
"""


# v2.0
# record
class TdoParamsStructure:
    def __init__(self):
        self.object3D = None
        self.xRotationBeforeDraw = 0.0
        self.yRotationBeforeDraw = 0.0
        self.zRotationBeforeDraw = 0.0
        self.faceColor = UnassignedColor
        self.backfaceColor = UnassignedColor
        self.alternateFaceColor = UnassignedColor
        self.alternateBackfaceColor = UnassignedColor
        self.scaleAtFullSize = 0.0
        self.repetitions = 0
        self.radiallyArranged = False
        self.pullBackAngle = 0.0

# alternate colors used only for fruit, so far - ripe vs. unripe
# params->start 
# access->pGeneral 
# record
class ParamsGeneral:
    def __init__(self):
        self.randomSway = 0.0
        self.startingSeedForRandomNumberGenerator = 0
        self.numApicalInflors = 0
        self.numAxillaryInflors = 0
        self.lineDivisions = 0
        self.isDicot = False
        self.maleFlowersAreSeparate = False
        self.ageAtMaturity = 0
        self.growthSCurve = umath.SCurveStructure()
        self.ageAtWhichFloweringStarts = 0
        self.fractionReproductiveAllocationAtMaturity_frn = 0.0
        self.wiltingPercent = 0.0
        self.phyllotacticRotationAngle = 0.0

#was longint, but want it in a param panel
#NA
#not using yet
# access->pLeaf 
# record
class ParamsLeaf:
    def __init__(self):
        self.leafTdoParams = TdoParamsStructure()
        self.stipuleTdoParams = TdoParamsStructure()
        self.sCurveParams = umath.SCurveStructure()
        self.petioleColor = UnassignedColor
        self.optimalBiomass_pctMPB = 0.0
        self.optimalFractionOfOptimalBiomassAtCreation_frn = 0.0
        self.minDaysToGrow = 0
        self.maxDaysToGrow = 0
        self.petioleLengthAtOptimalBiomass_mm = 0.0
        self.petioleWidthAtOptimalBiomass_mm = 0.0
        self.petioleAngle = 0.0
        self.compoundRachisToPetioleRatio = 0.0
        self.compoundPinnateOrPalmate = 0
        self.compoundNumLeaflets = 0
        self.compoundCurveAngleAtStart = 0.0
        self.compoundCurveAngleAtFullSize = 0.0
        self.fractionOfLiveBiomassWhenAbscisses_frn = 0.0
        self.petioleTaperIndex = 0
        self.compoundPinnateLeafletArrangement = 0

#ENUM
# access->pSeedlingLeaf 
# record
class ParamsSeedlingLeaf:
    def __init__(self):
        self.leafTdoParams = TdoParamsStructure()
        self.nodesOnStemWhenFallsOff = 0

# access->pInternode 
# record
class ParamsInternode:
    def __init__(self):
        self.faceColor = UnassignedColor
        self.backfaceColor = UnassignedColor
        self.curvingIndex = 0.0
        self.firstInternodeCurvingIndex = 0.0
        self.minFractionOfOptimalInitialBiomassToCreateInternode_frn = 0.0
        self.minDaysToCreateInternode = 0
        self.maxDaysToCreateInternodeIfOverMinFraction = 0
        self.optimalFinalBiomass_pctMPB = 0.0
        self.canRecoverFromStuntingDuringCreation = False
        self.minDaysToAccumulateBiomass = 0
        self.maxDaysToAccumulateBiomass = 0
        self.minDaysToExpand = 0
        self.maxDaysToExpand = 0
        self.lengthAtOptimalFinalBiomassAndExpansion_mm = 0.0
        self.lengthMultiplierDueToBiomassAccretion = 0.0
        self.lengthMultiplierDueToExpansion = 0.0
        self.widthAtOptimalFinalBiomassAndExpansion_mm = 0.0
        self.widthMultiplierDueToBiomassAccretion = 0.0
        self.widthMultiplierDueToExpansion = 0.0
        self.lengthMultiplierDueToBolting = 0.0
        self.minDaysToBolt = 0
        self.maxDaysToBolt = 0

# creation 
# growth and expansion 
# bolting 
# access->pFlower 
#kBud = 0; kPistil = 1; kStamens = 2; kFirstPetals = 3; kSecondPetals = 4; kThirdPetals = 5; kSepals = 6;
# record
class ParamsFlower:
    def __init__(self):
        self.tdoParams = [] # was: kBud..kSepals
        for i in range(0, kSepals + 1):
            self.tdoParams.append(TdoParamsStructure())
        self.budDrawingOption = 0
        self.optimalBiomass_pctMPB = 0.0
        self.minFractionOfOptimalInitialBiomassToCreateFlower_frn = 0.0
        self.minDaysToCreateFlowerBud = 0
        self.maxDaysToCreateFlowerBudIfOverMinFraction = 0
        self.minFractionOfOptimalBiomassToOpenFlower_frn = 0.0
        self.minDaysToOpenFlower = 0
        self.minDaysToGrow = 0
        self.maxDaysToGrowIfOverMinFraction = 0
        self.minDaysBeforeSettingFruit = 0
        self.daysBeforeDrop = 0
        self.minFractionOfOptimalBiomassToCreateFruit_frn = 0.0
        self.numPistils = 0
        self.styleLength_mm = 0.0
        self.styleWidth_mm = 0.0
        self.styleTaperIndex = 0
        self.styleColor = UnassignedColor
        self.numStamens = 0
        self.filamentLength_mm = 0.0
        self.filamentWidth_mm = 0.0
        self.filamentTaperIndex = 0
        self.filamentColor = UnassignedColor

# access->pInflor 
# record
class ParamsInflorescence:
    def __init__(self):
        self.bractTdoParams = TdoParamsStructure()
        self.optimalBiomass_pctMPB = 0.0
        self.minFractionOfOptimalBiomassToCreateInflorescence_frn = 0.0
        self.minDaysToCreateInflorescence = 0
        self.maxDaysToCreateInflorescenceIfOverMinFraction = 0
        self.minFractionOfOptimalBiomassToMakeFlowers_frn = 0.0
        self.minDaysToGrow = 0
        self.maxDaysToGrow = 0
        self.peduncleLength_mm = 0.0
        self.internodeLength_mm = 0.0
        self.internodeWidth_mm = 0.0
        self.pedicelLength_mm = 0.0
        self.pedicelAngle = 0.0
        self.branchAngle = 0.0
        self.angleBetweenInternodes = 0.0
        self.peduncleAngleFromVegetativeStem = 0.0
        self.apicalStalkAngleFromVegetativeStem = 0.0
        self.terminalStalkLength_mm = 0.0
        self.numFlowersPerBranch = 0
        self.numFlowersOnMainBranch = 0
        self.daysToAllFlowersCreated = 0
        self.numBranches = 0
        self.branchesAreAlternate = False
        self.isHead = False
        self.isTerminal = False
        self.flowersDrawTopToBottom = False
        self.flowersSpiralOnStem = False
        self.stalkColor = UnassignedColor
        self.pedicelColor = UnassignedColor
        self.pedicelTaperIndex = 0

# access->pAxillaryBud 
# record
class ParamsAxillaryBud:
    def __init__(self):
        self.tdoParams = TdoParamsStructure()

# access->pMeristem 
# record
class ParamsMeristem:
    def __init__(self):
        self.branchingIndex = 0.0
        self.branchingDistance = 0.0
        self.branchingAngle = 0.0
        self.determinateProbability = 0.0
        self.branchingIsSympodial = False
        self.branchingAndLeafArrangement = 0
        self.secondaryBranchingIsAllowed = False

# access->pFruit 
# record
class ParamsFruit:
    def __init__(self):
        self.tdoParams = TdoParamsStructure()
        self.sCurveParams = umath.SCurveStructure()
        self.optimalBiomass_pctMPB = 0.0
        self.minDaysToGrow = 0
        self.maxDaysToGrow = 0
        self.stalkStrengthIndex = 0.0
        self.daysToRipen = 0

# access->pRoot 
# record
class ParamsRoot:
    def __init__(self):
        self.tdoParams = TdoParamsStructure()
        self.showsAboveGround = False

# const
kExtraForRootTopProblem = 2

def cancelOutOppositeAmounts(amountAdded, amountTakenAway):
    if (amountAdded > 0.0) and (amountTakenAway > 0.0):
        if amountAdded == amountTakenAway:
            amountAdded = 0.0
            amountTakenAway = 0.0
        elif amountAdded > amountTakenAway:
            amountAdded = amountAdded - amountTakenAway
            amountTakenAway = 0.0
        else:
            amountTakenAway = amountTakenAway - amountAdded
            amountAdded = 0.0
    return amountAdded, amountTakenAway

# aspects->stop 
class PdPlant:
    # graphical 
    # parameters 
    # all vars following don't need to be saved in the plant file (but should be copied when streaming) 
    # pointers 
    # biomass and flowering 
    # v1.6b1
    # accounting variables 
    # used in parameter changes 
    # -------------------------------------------------------------------------------------- creation/destruction 
    def __init__(self):
        self.name = ""
        self.age = 0
        self.basePoint_mm = SinglePoint()
        self.xRotation = 0.0
        self.yRotation = 0.0
        self.zRotation = 0.0
        self.drawingScale_PixelsPerMm = 1.0
        self.previewCache = ubitmap.PdBitmap()
        self.drawingIntoPreviewCache = False
        self.previewCacheUpToDate = False
        self.randomNumberGenerator = urandom.PdRandom()
        self.breedingGenerator = urandom.PdRandom()
        self.pGeneral = ParamsGeneral()
        self.pMeristem = ParamsMeristem()
        self.pInternode = ParamsInternode()
        self.pLeaf = ParamsLeaf()
        self.pSeedlingLeaf = ParamsSeedlingLeaf()
        self.pAxillaryBud = ParamsAxillaryBud()
        self.pInflor = [ParamsInflorescence(), ParamsInflorescence()]
        self.pFlower = [ParamsFlower(), ParamsFlower()]
        self.pFruit = ParamsFruit()
        self.pRoot = ParamsRoot()
        self.selectedWhenLastSaved = False
        self.hidden = False
        self.computeBounds = False
        self.fixedPreviewScale = False
        self.justCopiedFromMainWindow = False
        self.fixedDrawPosition = False
        self.drawPositionIfFixed = delphi_compatability.TPoint()
        self.normalBoundsRect_pixels = delphi_compatability.TRect()
        self.indexWhenRemoved = 0
        self.selectedIndexWhenRemoved = 0
        self.needToRecalculateColors = False
        self.ageOfYoungestPhytomer = 0
        self.writingToMemo = False
        self.readingFromMemo = False
        self.readingMemoLine = 0L
        self.useBestDrawingForPreview = False
        self.turtle = None
        self.firstPhytomer = None
        self.totalBiomass_pctMPB = 0.0
        self.reproBiomass_pctMPB = 0.0
        self.shootBiomass_pctMPB = 0.0
        self.changeInShootBiomassToday_pctMPB = 0.0
        self.changeInReproBiomassToday_pctMPB = 0.0
        self.ageAtWhichFloweringStarted = 0
        self.floweringHasStarted = False
        self.totalPlantParts = 0L
        self.partsCreated = 0L
        self.total3DExportPoints = 0L
        self.total3DExportTriangles = 0L
        self.total3DExportMaterials = 0L
        self.unallocatedNewVegetativeBiomass_pctMPB = 0.0
        self.unremovedDeadVegetativeBiomass_pctMPB = 0.0
        self.unallocatedNewReproductiveBiomass_pctMPB = 0.0
        self.unremovedDeadReproductiveBiomass_pctMPB = 0.0
        self.unremovedStandingDeadBiomass_pctMPB = 0.0
        self.numApicalActiveReproductiveMeristemsOrInflorescences = 0L
        self.numAxillaryActiveReproductiveMeristemsOrInflorescences = 0L
        self.numApicalInactiveReproductiveMeristems = 0L
        self.numAxillaryInactiveReproductiveMeristems = 0L
        self.wholePlantUpdateNeeded = False
        self.plantPartsDrawnAtStart = 0L
        self.changingWholeSCurves = False
        self.noteLines = []
        self.amendments = ucollect.TListCollection() 
        self.totalMemoryUsed_K = 0.0
    
        #self.initializeCache(self.previewCache)
        self.breedingGenerator.setSeed(self.breedingGenerator.randomSeedFromTime())
        self.initialize3DObjects()
                
        # not using the internode water expansion code this version, meaningless, no water stress, need these
        # these twos mean internodes are hard-coded to increase in width and height twice (from defaults in params.tab)
        self.pInternode.lengthMultiplierDueToBiomassAccretion = 2.0
        self.pInternode.widthMultiplierDueToBiomassAccretion = 2.0
        self.pInternode.lengthMultiplierDueToExpansion = 1.0
        self.pInternode.widthMultiplierDueToExpansion = 1.0
        
    def makeCopy(self):
        return copy.deepcopy(self)
    
    def initialize3DObjects(self):
        partType = 0
        
        # i think it is best to create these at plant creation, then read into existing ones. 
        self.pSeedlingLeaf.leafTdoParams.object3D = utdo.KfObject3D()
        self.pLeaf.leafTdoParams.object3D = utdo.KfObject3D()
        self.pLeaf.stipuleTdoParams.object3D = utdo.KfObject3D()
        self.pInflor[kGenderFemale].bractTdoParams.object3D = utdo.KfObject3D()
        self.pInflor[kGenderMale].bractTdoParams.object3D = utdo.KfObject3D()
        for partType in range(0, kHighestFloralPartConstant + 1):
            self.pFlower[kGenderFemale].tdoParams[partType].object3D = utdo.KfObject3D()
            self.pFlower[kGenderMale].tdoParams[partType].object3D = utdo.KfObject3D()
        self.pAxillaryBud.tdoParams.object3D = utdo.KfObject3D()
        self.pFruit.tdoParams.object3D = utdo.KfObject3D()
        self.pRoot.tdoParams.object3D = utdo.KfObject3D()
    
    def freeAllDrawingPlantParts(self):
        if (self.firstPhytomer != None):
            traverser = utravers.PdTraverser().createWithPlant(self)
            traverser.traverseWholePlant(utravers.kActivityFree)
            self.firstPhytomer = None
            # v1.6b1
            self.partsCreated = 0
    
    def initializeCache(self, widget, cache):
        # giving the cache a tiny size at creation forces it to create its canvas etc
        # without this there is a nil pointer at streaming which causes a problem
        cache.Width = 1
        cache.Height = 1
        cache.Transparent = True
        cache.TransparentColor = udomain.domain.options.backgroundColor
        cache.updateForChanges(widget)
    
    def free3DObjects(self):
        partType = 0
        
        self.pSeedlingLeaf.leafTdoParams.object3D.free
        self.pSeedlingLeaf.leafTdoParams.object3D = None
        self.pLeaf.leafTdoParams.object3D.free
        self.pLeaf.leafTdoParams.object3D = None
        self.pLeaf.stipuleTdoParams.object3D.free
        self.pLeaf.stipuleTdoParams.object3D = None
        self.pInflor[kGenderFemale].bractTdoParams.object3D.free
        self.pInflor[kGenderFemale].bractTdoParams.object3D = None
        self.pInflor[kGenderMale].bractTdoParams.object3D.free
        self.pInflor[kGenderMale].bractTdoParams.object3D = None
        for partType in range(0, kHighestFloralPartConstant + 1):
            self.pFlower[kGenderFemale].tdoParams[partType].object3D.free
            self.pFlower[kGenderFemale].tdoParams[partType].object3D = None
            self.pFlower[kGenderMale].tdoParams[partType].object3D.free
            self.pFlower[kGenderMale].tdoParams[partType].object3D = None
        self.pAxillaryBud.tdoParams.object3D.free
        self.pAxillaryBud.tdoParams.object3D = None
        self.pFruit.tdoParams.object3D.free
        self.pFruit.tdoParams.object3D = None
        self.pRoot.tdoParams.object3D.free
        self.pRoot.tdoParams.object3D = None
    
    def getName(self):
        result = ""
        result = self.name
        return result
    
    def setName(self, newName):
        self.name = newName[:kPlantNameLength]
    
    # ----------------------------------------------------------------------------------------- age management 
    def regrow(self):
        self.setAge(self.age)
    
    def reset(self):
        self.age = 0
        self.freeAllDrawingPlantParts()
        self.totalBiomass_pctMPB = 0.0
        self.reproBiomass_pctMPB = 0.0
        self.shootBiomass_pctMPB = 0.0
        self.changeInShootBiomassToday_pctMPB = 0.0
        self.changeInReproBiomassToday_pctMPB = 0.0
        self.floweringHasStarted = False
        self.totalPlantParts = 0
        self.ageAtWhichFloweringStarted = 0
        self.numApicalActiveReproductiveMeristemsOrInflorescences = 0
        self.numAxillaryActiveReproductiveMeristemsOrInflorescences = 0
        self.numApicalInactiveReproductiveMeristems = 0
        self.numAxillaryInactiveReproductiveMeristems = 0
        self.unallocatedNewVegetativeBiomass_pctMPB = 0.0
        self.unremovedDeadVegetativeBiomass_pctMPB = 0.0
        self.unallocatedNewReproductiveBiomass_pctMPB = 0.0
        self.unremovedDeadReproductiveBiomass_pctMPB = 0.0
        self.unremovedStandingDeadBiomass_pctMPB = 0.0
        self.ageOfYoungestPhytomer = 0
        self.needToRecalculateColors = True
        self.randomNumberGenerator.setSeedFromSmallint(self.pGeneral.startingSeedForRandomNumberGenerator)
    
    def setAge(self, newAge):
        newAge = umath.intMax(0, umath.intMin(self.pGeneral.ageAtMaturity, newAge))
        Cursor_StartWait()
        try:
            self.reset()
            while self.age < newAge:
                self.nextDay()
        finally:
            Cursor_StopWait()
    
    # ---------------------------------------------------------------------------------------  drawing and graphics 
    def draw(self):
        utravers.cancelDrawing = False
        if (self.turtle == None):
            raise GeneralException.create("Problem: Nil turtle in method PdPlant.draw.")
        if self.turtle.drawingSurface.drawingContext != None:
            pass
            # PDF PORT _ NOT REQUIRED?
            #self.turtle.drawingSurface.pane.Brush.Style = delphi_compatability.TFPBrushStyle.bsSolid
            #self.turtle.drawingSurface.pane.Pen.Style = delphi_compatability.TFPPenStyle.psSolid
        self.turtle.setLineColor(delphi_compatability.clGreen)
        self.turtle.push()
        self.turtle.rotateZ(64)
        self.turtle.rotateX(self.xRotation * 256 / 360)
        # convert here from 360 degrees to 256 turtle degrees 
        self.turtle.rotateY(self.yRotation * 256 / 360)
        self.turtle.rotateZ(self.zRotation * 256 / 360)
        self.turtle.drawingSurface.lineColor = delphi_compatability.clGreen
        if (self.firstPhytomer != None):
            traverser = utravers.PdTraverser().createWithPlant(self)
            traverser.plantPartsDrawnAtStart = self.plantPartsDrawnAtStart
            # if not drawing 3D objects, probably drawing just to get bounds
            traverser.showDrawingProgress = self.turtle.drawOptions.draw3DObjects
            traverser.traverseWholePlant(utravers.kActivityDraw)
        self.turtle.pop()
        # recalculating colors occurs during drawing of leaves and internodes if necessary 
        self.needToRecalculateColors = False
    
    def countPlantParts(self):
        traverser = PdTraverser()
        
        self.totalPlantParts = 0
        if (self.firstPhytomer != None):
            traverser = utravers.PdTraverser().createWithPlant(self)
            try:
                traverser.traverseWholePlant(utravers.kActivityCountPlantParts)
                self.totalPlantParts = traverser.totalPlantParts
            finally:
                traverser.free
                traverser = None
    
    def countPlantPartsFor3DOutput(self, outputType, stemCylinderFaces):
        traverser = PdTraverser()
        i = 0
        
        if (self.firstPhytomer != None):
            traverser = utravers.PdTraverser().createWithPlant(self)
            try:
                traverser.traverseWholePlant(utravers.kActivityCountPointsAndTrianglesFor3DExport)
                self.totalPlantParts = traverser.totalPlantParts
                if outputType == u3dexport.kPOV:
                    # POV does not use polygon cylinders for lines; it draws them directly
                    self.total3DExportPoints = traverser.total3DExportPointsIn3DObjects + traverser.total3DExportStemSegments * self.pGeneral.lineDivisions * 2
                    self.total3DExportTriangles = traverser.total3DExportTrianglesIn3DObjects
                else :
                    # for every output type that uses cylinders made of triangles
                    self.total3DExportPoints = traverser.total3DExportPointsIn3DObjects + (traverser.total3DExportStemSegments * (self.pGeneral.lineDivisions + 1) * stemCylinderFaces)
                    self.total3DExportTriangles = traverser.total3DExportTrianglesIn3DObjects + (traverser.total3DExportStemSegments * self.pGeneral.lineDivisions * stemCylinderFaces * 2)
                # this is only important for LWO and OBJ, but people will like to see it anyway
                self.total3DExportMaterials = 0
                for i in range(0, u3dexport.kExportPartLast + 1):
                    if traverser.exportTypeCounts[i] > 0:
                        self.total3DExportMaterials += 1
            finally:
                traverser.free
                traverser = None
    
    def calculateTotalMemorySize(self):
        result = 0.0
        traverser = PdTraverser()
        
        result = self.instanceSize / 1024.0
        result = result + self.hangingObjectsMemoryUse_K()
        result = result + self.tdoMemoryUse_K()
        if self.previewCache != None:
            # preview cache
            result = result + ubitmap.BitmapMemorySize(self.previewCache) / 1024.0
        self.totalMemoryUsed_K = result
        if (self.firstPhytomer != None):
            # plant parts
            traverser = utravers.PdTraverser().createWithPlant(self)
            try:
                traverser.traverseWholePlant(utravers.kActivityCountTotalMemoryUse)
                result = result + traverser.totalMemorySize / 1024.0
                self.totalMemoryUsed_K = result
            finally:
                traverser.free
                traverser = None
        return result
    
    def hangingObjectsMemoryUse_K(self):
        result = 0.0
        i = 0
        
        result = 0
        if self.randomNumberGenerator != None:
            # random number generators
            result = result + self.randomNumberGenerator.instanceSize / 1024.0
        if self.breedingGenerator != None:
            result = result + self.breedingGenerator.instanceSize / 1024.0
        if self.noteLines:
            # note -- estimate at forty characetrs per line
            result = result + (len(self.noteLines.instanceSize) * 40) / 1024.0
        if self.amendments != None:
            # amendments
            result = result + self.amendments.instanceSize / 1024.0
            for amendment in rself.amendments:
                result = result + amendment.instanceSize / 1024.0
        return result
    
    def tdoMemoryUse_K(self):
        result = 0.0
        partType = 0
        
        # tdos
        result = 0
        result = result + self.pSeedlingLeaf.leafTdoParams.object3D.totalMemorySize() / 1024.0
        result = result + self.pLeaf.leafTdoParams.object3D.totalMemorySize() / 1024.0
        result = result + self.pLeaf.stipuleTdoParams.object3D.totalMemorySize() / 1024.0
        result = result + self.pInflor[kGenderFemale].bractTdoParams.object3D.totalMemorySize() / 1024.0
        result = result + self.pInflor[kGenderMale].bractTdoParams.object3D.totalMemorySize() / 1024.0
        for partType in range(0, kHighestFloralPartConstant + 1):
            result = result + self.pFlower[kGenderFemale].tdoParams[partType].object3D.totalMemorySize() / 1024.0
            result = result + self.pFlower[kGenderMale].tdoParams[partType].object3D.totalMemorySize() / 1024.0
        result = result + self.pAxillaryBud.tdoParams.object3D.totalMemorySize() / 1024.0
        result = result + self.pFruit.tdoParams.object3D.totalMemorySize() / 1024.0
        result = result + self.pRoot.tdoParams.object3D.totalMemorySize() / 1024.0
        return result
    
    def drawOn(self, destCanvas):
        self.turtle = uturtle.KfTurtle.defaultStartUsing()
        try:
            self.turtle.drawingSurface.pane = destCanvas
            self.setTurtleDrawOptionsForNormalDraw(self.turtle)
            # must be after pane and draw options set 
            self.turtle.reset()
            self.turtle.setScale_pixelsPerMm(self.realDrawingScale_pixelsPerMm())
            self.turtle.drawingSurface.foreColor = delphi_compatability.clGreen
            self.turtle.drawingSurface.backColor = delphi_compatability.clRed
            self.turtle.drawingSurface.lineColor = delphi_compatability.clBlue
            realBasePoint_pixels = self.basePoint_pixels()
            self.turtle.xyz(realBasePoint_pixels.X, realBasePoint_pixels.Y, 0)
            self.turtle.resetBoundsRect(realBasePoint_pixels)
            try:
                if self.turtle.drawOptions.sortPolygons:
                    self.turtle.drawingSurface.recordingStart()
                    self.draw()
                    self.turtle.drawingSurface.recordingStop()
                    self.turtle.drawingSurface.recordingDraw()
                    self.turtle.drawingSurface.clearTriangles()
                else:
                    self.draw()
                if (self.computeBounds) and (not udomain.domain.drawingToMakeCopyBitmap):
                    self.setBoundsRect_pixels(self.getTurtleBoundsRect())
                    self.enforceMinimumBoundsRect()
                    self.expandBoundsRectForLineWidth()
            except Exception, e:
                usupport.messageForExceptionType(e, "PdPlant.drawOn")
        finally:
            uturtle.KfTurtle.defaultStopUsing()
            self.turtle = None
    
    def setTurtleDrawOptionsForNormalDraw(self, turtle):
        if turtle == None:
            return
        turtle.drawOptions.circlePoints = False
        if udomain.domain.options.drawSpeed == udomain.kDrawFast:
            turtle.drawOptions.draw3DObjects = True
            turtle.drawOptions.draw3DObjectsAsRects = True
            turtle.drawOptions.drawStems = True
            turtle.drawOptions.wireFrame = True
            turtle.drawOptions.sortPolygons = False
            turtle.drawOptions.sortTdosAsOneItem = False
        elif udomain.domain.options.drawSpeed == udomain.kDrawMedium:
            turtle.drawOptions.draw3DObjects = True
            turtle.drawOptions.draw3DObjectsAsRects = False
            turtle.drawOptions.drawStems = True
            turtle.drawOptions.wireFrame = True
            turtle.drawOptions.sortPolygons = False
            turtle.drawOptions.sortTdosAsOneItem = False
        elif udomain.domain.options.drawSpeed == udomain.kDrawBest:
            turtle.drawOptions.draw3DObjects = True
            turtle.drawOptions.draw3DObjectsAsRects = False
            turtle.drawOptions.drawStems = True
            turtle.drawOptions.wireFrame = False
            turtle.drawOptions.sortPolygons = True
            turtle.drawOptions.sortTdosAsOneItem = True
            turtle.drawOptions.drawLines = True
            turtle.drawOptions.lineContrastIndex = 3
        elif udomain.domain.options.drawSpeed == udomain.kDrawCustom:
            turtle.drawOptions.draw3DObjects = udomain.domain.options.draw3DObjects
            turtle.drawOptions.draw3DObjectsAsRects = udomain.domain.options.draw3DObjectsAsBoundingRectsOnly
            turtle.drawOptions.drawStems = udomain.domain.options.drawStems
            turtle.drawOptions.wireFrame = not udomain.domain.options.fillPolygons
            turtle.drawOptions.sortPolygons = udomain.domain.options.sortPolygons
            turtle.drawOptions.sortTdosAsOneItem = udomain.domain.options.sortTdosAsOneItem
            turtle.drawOptions.drawLines = udomain.domain.options.drawLinesBetweenPolygons
            turtle.drawOptions.lineContrastIndex = udomain.domain.options.lineContrastIndex
    
    def resizingRect(self):
        theRect = self.boundsRect_pixels()
        result = delphi_compatability.TRect(theRect.Right - udomain.domain.options.resizeRectSize, theRect.Top, theRect.Right, theRect.Top + udomain.domain.options.resizeRectSize)
        if result.Left < theRect.Left:
            result.Left = theRect.Left
        if result.Top < theRect.Top:
            result.Top = theRect.Top
        return result
    
    def pointIsInResizingRect(self, point):
        result = False
        theRect = self.resizingRect()
        result = (Point.x >= theRect.Left) and (Point.x <= theRect.Right) and (Point.y >= theRect.Top) and (Point.y <= theRect.Bottom)
        return result
    
    def recalculateBoundsForOffsetChange(self):
        self.fakeDrawToGetBounds()
        if self.hidden:
            return
        if udomain.domain.options.cachePlantBitmaps:
            drawingRect = delphi_compatability.TRect(0, 0, umain.MainForm.drawingPaintBox.Width, umain.MainForm.drawingPaintBox.Height)
            intersectResult = delphi_compatability.IntersectRect(intersectRect_pixels, self.boundsRect_pixels(), drawingRect)
            if (intersectResult) and (not self.hidden) and (self.previewCache.Width < 5):
                self.recalculateBounds(kDrawNow)
    
    #procedure drawOnUsingOpenGL(turtle: KfTurtle; selected, firstSelected: boolean);
    def recalculateBounds(self, drawNow, widget):
        self.fakeDrawToGetBounds()
        if not udomain.domain.options.cachePlantBitmaps:
            if self.previewCache.Width > 5:
                self.shrinkPreviewCache()
                umain.MainForm.updateForChangeToPlantBitmaps()
            return
        if not drawNow:
            return
        if self.hidden:
            self.shrinkPreviewCache()
            umain.MainForm.updateForChangeToPlantBitmaps()
            return
        drawingRect = Rect(0, 0, umain.MainForm.drawingPaintBox.Width, umain.MainForm.drawingPaintBox.Height)
        # on opening file at first, force redraw of cache because drawingPaintBox size might be wrong
        intersectResult = umain.MainForm.inFormCreation or umain.MainForm.inFileOpen or delphi_compatability.IntersectRect(intersectRect_pixels, self.boundsRect_pixels(), drawingRect)
        if not intersectResult:
            self.shrinkPreviewCache()
            umain.MainForm.updateForChangeToPlantBitmaps()
            return
        bytesThisBitmapWillBe = intround(usupport.rWidth(self.boundsRect_pixels()) * usupport.rHeight(self.boundsRect_pixels()) * umain.MainForm.screenBytesPerPixel())
        if not umain.MainForm.roomForPlantBitmap(self, bytesThisBitmapWillBe):
            return
        oldBasePoint = self.basePoint_pixels()
        try:
            self.setBasePoint_pixels(Point(self.basePoint_pixels().X - self.boundsRect_pixels().Left, self.basePoint_pixels().Y - self.boundsRect_pixels().Top))
            self.resizeCacheIfNecessary(self.previewCache, Point(usupport.rWidth(self.boundsRect_pixels()), usupport.rHeight(self.boundsRect_pixels())), kInMainWindow)
            self.previewCache.TransparentColor = udomain.domain.options.transparentColor
            self.previewCache.updateForChanges(widget)
            ubmpsupport.fillBitmap(self.previewCache, udomain.domain.options.transparentColor)
            # showing progress here is mainly for really complicated plants; most plants won't need it
            showProgress = (not umain.MainForm.drawing) and (udomain.domain.options.showPlantDrawingProgress)
            if showProgress:
                self.plantPartsDrawnAtStart = 0
                self.countPlantParts()
                showProgress = self.totalPlantParts > 50
                if showProgress:
                    umain.MainForm.startDrawProgress(self.totalPlantParts)
            try:
                self.computeBounds = True
                self.drawOn(self.previewCache.Canvas)
            finally:
                self.computeBounds = False
                if showProgress:
                    umain.MainForm.finishDrawProgress()
        finally:
            # have to fake draw again to reset bounds rect
            self.setBasePoint_pixels(oldBasePoint)
            self.fakeDrawToGetBounds()
    
    def fakeDrawToGetBounds(self):
        self.computeBounds = True
        self.turtle = uturtle.KfTurtle.defaultStartUsing()
        try:
            self.turtle.drawingSurface.pane = None
            self.turtle.drawOptions.drawStems = False
            self.turtle.drawOptions.draw3DObjects = False
            # must be after pane and draw options set 
            self.turtle.reset()
            self.turtle.setScale_pixelsPerMm(self.realDrawingScale_pixelsPerMm())
            self.turtle.xyz(self.basePoint_pixels().X, self.basePoint_pixels().Y, 0)
            self.turtle.resetBoundsRect(self.basePoint_pixels())
            try:
                self.draw()
            except Exception, e:
                usupport.messageForExceptionType(e, "PdPlant.fakeDrawToGetBounds")
            self.setBoundsRect_pixels(self.getTurtleBoundsRect())
            self.enforceMinimumBoundsRect()
            self.expandBoundsRectForLineWidth()
        finally:
            uturtle.KfTurtle.defaultStopUsing()
            self.turtle = None
            self.computeBounds = False
    
    def drawIntoCache(self, gc, cache, size, considerDomainScale, immediate):
        changed = False
        self.resizeCacheIfNecessary(cache, size, kNotInMainWindow)
        if immediate:
            ubmpsupport.fillBitmap(gc, cache, udomain.domain.options.backgroundColor)
        self.turtle = uturtle.KfTurtle.defaultStartUsing()
        try:
            # set starting values 
            self.turtle.drawingSurface.setDrawingContext((cache.pixmap, gc))
            if not self.fixedPreviewScale:
                self.drawingScale_PixelsPerMm = 10.0
                drawPosition = delphi_compatability.TPoint(cache.Width / 2, cache.Height - 5)
                # 1. draw to figure scale to center boundsRect in cache size 
                self.setTurtleUpForPreviewScratch(self.drawingScale_PixelsPerMm, drawPosition)
                #nothing-messes up paint
                try:
                    self.draw()
                except:
                    pass
                self.setBoundsRect_pixels(self.getTurtleBoundsRect())
                # now change the scale to make the boundsRect fit the drawRect 
                drawnWidth = usupport.rWidth(self.boundsRect_pixels())
                drawnHeight = usupport.rHeight(self.boundsRect_pixels())
                if (drawnWidth > 0) and (drawnHeight > 0):
                    newScaleX = umath.safedivExcept(self.drawingScale_PixelsPerMm * size.X, drawnWidth, 0.1)
                    if considerDomainScale:
                        newScaleX = umath.safedivExcept(newScaleX, udomain.domain.plantDrawScale_PixelsPerMm(), newScaleX)
                    else:
                        newScaleX = newScaleX * 0.9
                    newScaleY = umath.safedivExcept(self.drawingScale_PixelsPerMm * size.Y, drawnHeight, 0.1)
                    if considerDomainScale:
                        newScaleY = umath.safedivExcept(newScaleY, udomain.domain.plantDrawScale_PixelsPerMm(), newScaleY)
                    else:
                        newScaleY = newScaleY * 0.9
                    self.drawingScale_PixelsPerMm = umath.min(newScaleX, newScaleY)
                    changed = self.drawingScale_PixelsPerMm != 1.0
            if not self.fixedDrawPosition:
                # draw to find drawPosition that will center new boundsrect in cache 
                drawPosition = delphi_compatability.TPoint(cache.Width / 2, cache.Height - 5)
                self.setTurtleUpForPreviewScratch(self.drawingScale_PixelsPerMm, drawPosition)
                #nothing-messes up paint
                try:
                    self.draw()
                except:
                    pass
                self.setBoundsRect_pixels(self.getTurtleBoundsRect())
                bestLeft = cache.Width / 2 - usupport.rWidth(self.boundsRect_pixels()) / 2
                bestTop = cache.Height / 2 - usupport.rHeight(self.boundsRect_pixels()) / 2
                drawPosition.X = drawPosition.X - (self.boundsRect_pixels().Left - bestLeft)
                drawPosition.Y = drawPosition.Y - (self.boundsRect_pixels().Top - bestTop)
                self.drawPositionIfFixed = drawPosition
                # assume it will always have to be moved
                changed = True
            else:
                drawPosition = self.drawPositionIfFixed
            if (self.fixedPreviewScale or self.fixedDrawPosition or changed) and (immediate):
                # final drawing 
                ubmpsupport.fillBitmap(gc, cache, udomain.domain.options.backgroundColor)
                self.setTurtleUpForPreview(self.drawingScale_PixelsPerMm, drawPosition)
                #nothing-messes up paint
                try:
                    self.draw()
                except:
                    # PDF PORT ADDED RAISE FOR TESTING
                    raise
                    pass
        finally:
            #self.previewCacheUpToDate := True;
            uturtle.KfTurtle.defaultStopUsing()
            self.turtle = None
            self.useBestDrawingForPreview = False
    
    def drawPreviewIntoCache(self, gc, size, considerDomainScale, immediate):
        try:
            self.drawingIntoPreviewCache = True
            self.drawIntoCache(gc, self.previewCache, size, considerDomainScale, immediate)
            self.previewCacheUpToDate = True
        finally:
            self.drawingIntoPreviewCache = False
    
    def calculateDrawingScaleToFitSize(self, size):
        self.drawPreviewIntoCache(size, kConsiderDomainScale, kDontDrawNow)
        self.shrinkPreviewCache()
    
    def calculateDrawingScaleToLookTheSameWithDomainScale(self):
        self.drawingScale_PixelsPerMm = umath.safedivExcept(self.drawingScale_PixelsPerMm, udomain.domain.plantManager.plantDrawScale_PixelsPerMm, 0)
    
    def shrinkPreviewCache(self):
        if self.previewCache == None:
            # this is to save memory after using the preview cache 
            return
        if (self.previewCache.Width > 5) or (self.previewCache.Height > 5):
            self.previewCache = ubitmap.PdBitmap()
            self.previewCache.Width = 1
            self.previewCache.Height = 1
            self.previewCache.Transparent = True
            self.previewCache.TransparentColor = udomain.domain.options.backgroundColor
            self.previewCache.updateForChanges()
    
    def resizeCacheIfNecessary(self, cache, size, inMainWindow):
        if (size.X <= 0) or (size.Y <= 0):
            return
        # special code to make sure pictures come out all right on 256-color monitors.
        # setting the bitmap pixel format to 24-bit and giving it the global palette stops
        # it from dithering and gets the nearest colors from the palette when drawing.
        # you also need to realize the palette anytime you bitblt (copyRect) from this
        # bitmap to a display surface (timage, paint box, draw grid, etc).
        # use the global function copyBitmapToCanvasWithGlobalPalette in umain.
        ubmpsupport.setPixelFormatBasedOnScreenForBitmap(cache)
        if (cache.Width != size.X) or (cache.Height != size.Y):
            try:
                # end special code
                cache.Width = size.X
                cache.Height = size.Y
                cache.updateForChanges()
                if (inMainWindow) and (cache == self.previewCache):
                    umain.MainForm.updateForChangeToPlantBitmaps()
            except:
                # PDF PORT ADDED RAISE FOR TESTING
                raise
                cache.Width = 1
                cache.Height = 1
                if (inMainWindow) and (cache == self.previewCache):
                    umain.MainForm.exceptionResizingPlantBitmap()
                else:
                    ShowMessage("Problem creating bitmap; probably not enough memory.")
    
    def getTurtleBoundsRect(self):
        result = self.turtle.boundsRect()
        if self.pRoot.showsAboveGround:
            result.Bottom = result.Bottom + kExtraForRootTopProblem
        return result
    
    def setTurtleUpForPreviewScratch(self, scale, drawPosition):
        if self.turtle == None:
            return
        self.turtle.drawOptions.sortPolygons = False
        self.turtle.drawOptions.drawLines = False
        self.turtle.drawOptions.wireFrame = True
        self.turtle.drawOptions.drawStems = False
        self.turtle.drawOptions.draw3DObjects = False
        self.turtle.drawOptions.circlePoints = False
        # must be after pane and draw options set 
        self.turtle.reset()
        self.turtle.setScale_pixelsPerMm(scale)
        self.turtle.xyz(drawPosition.X, drawPosition.Y, 0)
        self.turtle.resetBoundsRect(drawPosition)
    
    def setTurtleUpForPreview(self, scale, drawPosition):
        if self.turtle == None:
            return
        if not self.useBestDrawingForPreview:
            self.setTurtleDrawOptionsForNormalDraw(self.turtle)
        else:
            # this is only for the wizard
            self.turtle.drawOptions.sortPolygons = True
            self.turtle.drawOptions.sortTdosAsOneItem = True
            self.turtle.drawOptions.drawLines = True
            self.turtle.drawOptions.lineContrastIndex = 3
            self.turtle.drawOptions.wireFrame = False
            self.turtle.drawOptions.drawStems = True
            self.turtle.drawOptions.draw3DObjects = True
            self.turtle.drawOptions.draw3DObjectsAsRects = False
            self.turtle.drawOptions.circlePoints = False
        # must be after pane and draw options set 
        self.turtle.reset()
        self.turtle.drawingSurface.foreColor = delphi_compatability.clGreen
        self.turtle.drawingSurface.backColor = delphi_compatability.clRed
        self.turtle.drawingSurface.lineColor = delphi_compatability.clBlue
        self.turtle.setScale_pixelsPerMm(scale)
        self.turtle.xyz(drawPosition.X, drawPosition.Y, 0)
        self.turtle.resetBoundsRect(drawPosition)
    
    def getHint(self, point):
        result = self.getName()
        if (umain.MainForm.cursorModeForDrawing == umain.kCursorModePosingSelect) and (umain.MainForm.focusedPlant() == self):
            plantPart = self.findPlantPartAtPositionByTestingPolygons(Point)
            if (plantPart != None) and (plantPart.__class__ is upart.PdPlantPart):
                result = plantPart.getFullName()
        return result
    
    def findPlantPartAtPositionByTestingPolygons(self, point):
        result = TObject()
        turtle = KfTurtle()
        partID = 0L
        
        result = None
        # if you give it no drawing surface pane, everything happens but the actual drawing
        self.drawOn(None)
        turtle = uturtle.KfTurtle.defaultStartUsing()
        if turtle == None:
            return result
        if turtle.drawingSurface == None:
            return result
        try:
            partID = turtle.drawingSurface.plantPartIDForPoint(Point)
            if partID >= 0:
                result = self.plantPartForPartID(partID)
        finally:
            uturtle.KfTurtle.defaultStopUsing()
        return result
    
    def realDrawingScale_pixelsPerMm(self):
        result = 0.0
        if udomain.domain.drawingToMakeCopyBitmap:
            result = self.drawingScale_PixelsPerMm * udomain.domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm
        else:
            result = self.drawingScale_PixelsPerMm * udomain.domain.plantDrawScale_PixelsPerMm()
        return result
    
    def basePoint_pixels(self):
        result = delphi_compatability.TPoint()
        if not udomain.domain.drawingToMakeCopyBitmap:
            result.X = intround((self.basePoint_mm.x + udomain.domain.plantDrawOffset_mm().x) * udomain.domain.plantDrawScale_PixelsPerMm())
            result.Y = intround((self.basePoint_mm.y + udomain.domain.plantDrawOffset_mm().y) * udomain.domain.plantDrawScale_PixelsPerMm())
        else:
            result.X = intround((self.basePoint_mm.x + udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.x) * udomain.domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm)
            result.Y = intround((self.basePoint_mm.y + udomain.domain.plantDrawOffsetWhenDrawingCopy_mm.y) * udomain.domain.plantDrawScaleWhenDrawingCopy_PixelsPerMm)
        return result
    
    def setBasePoint_pixels(self, aPoint_pixels):
        self.basePoint_mm.x = umath.safedivExcept(aPoint_pixels.X, udomain.domain.plantDrawScale_PixelsPerMm(), 0) - udomain.domain.plantDrawOffset_mm().x
        self.basePoint_mm.y = umath.safedivExcept(aPoint_pixels.Y, udomain.domain.plantDrawScale_PixelsPerMm(), 0) - udomain.domain.plantDrawOffset_mm().y
    
    def setBoundsRect_pixels(self, aRect_pixels):
        self.normalBoundsRect_pixels = aRect_pixels
    
    def boundsRect_pixels(self):
        result = copy.copy(self.normalBoundsRect_pixels)
        return result
    
    def enforceMinimumBoundsRect(self):
        theRect = self.boundsRect_pixels()
        if ((theRect.Right - theRect.Left) < 1):
            theRect.Left = self.basePoint_pixels().X
            theRect.Right = theRect.Left + 1
        if ((theRect.Bottom - theRect.Top) < 1):
            theRect.Bottom = self.basePoint_pixels().Y
            theRect.Top = theRect.Bottom - 1
    
    def expandBoundsRectForLineWidth(self):
        extra = intround(self.maximumLineWidth() * self.realDrawingScale_pixelsPerMm()) + 1
        theRect = self.boundsRect_pixels()
        UNRESOLVED.inflateRect(theRect, extra, extra)
        self.setBoundsRect_pixels(theRect)
    
    def maximumLineWidth(self):
        result = 0.0
        result = 0.0
        if self.pLeaf.petioleWidthAtOptimalBiomass_mm > result:
            result = self.pLeaf.petioleWidthAtOptimalBiomass_mm
        if self.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm > result:
            result = self.pInternode.widthAtOptimalFinalBiomassAndExpansion_mm
        if self.pInflor[kGenderMale].internodeWidth_mm > result:
            result = self.pInflor[kGenderMale].internodeWidth_mm
        if self.pInflor[kGenderFemale].internodeWidth_mm > result:
            result = self.pInflor[kGenderFemale].internodeWidth_mm
        return result
    
    def moveBy(self, delta_pixels):
        delta_mm = SinglePoint()
        theRect = self.boundsRect_pixels()
        theRect.Left = theRect.Left + delta_pixels.X
        theRect.Right = theRect.Right + delta_pixels.X
        theRect.Top = theRect.Top + delta_pixels.Y
        theRect.Bottom = theRect.Bottom + delta_pixels.Y
        delta_mm.x = umath.safedivExcept(delta_pixels.X, udomain.domain.plantDrawScale_PixelsPerMm(), 0)
        delta_mm.y = umath.safedivExcept(delta_pixels.Y, udomain.domain.plantDrawScale_PixelsPerMm(), 0)
        self.basePoint_mm.x = self.basePoint_mm.x + delta_mm.x
        self.basePoint_mm.y = self.basePoint_mm.y + delta_mm.y
    
    def moveTo(self, aPoint_pixels):
        oldBasePoint_pixels = self.basePoint_pixels()
        theRect = self.boundsRect_pixels()
        theRect.Left = theRect.Left + aPoint_pixels.X - oldBasePoint_pixels.X
        theRect.Right = theRect.Right + aPoint_pixels.X - oldBasePoint_pixels.X
        theRect.Top = theRect.Top + aPoint_pixels.Y - oldBasePoint_pixels.Y
        theRect.Bottom = theRect.Bottom + aPoint_pixels.Y - oldBasePoint_pixels.Y
        self.setBasePoint_pixels(aPoint_pixels)
    
    def includesPoint(self, aPoint):
        result = False
        result = self.boundsRectIncludesPoint(aPoint, self.boundsRect_pixels(), True)
        return result
    
    def boundsRectIncludesPoint(self, aPoint, boundsRect, checkResizeRect):
        result = False
        xPixel = 0L
        yPixel = 0L
        i = 0L
        
        result = delphi_compatability.PtInRect(boundsRect, aPoint)
        if result and udomain.domain.options.cachePlantBitmaps:
            if checkResizeRect and delphi_compatability.PtInRect(self.resizingRect(), aPoint):
                result = True
            else:
                xPixel = aPoint.X - boundsRect.Left
                yPixel = aPoint.Y - boundsRect.Top
                result = self.pointColorMatch(xPixel, yPixel)
                if (not result) and (udomain.domain.options.cachePlantBitmaps):
                    for i in range(0, 8):
                        if self.pointColorAdjacentMatch(xPixel, yPixel, i):
                            result = True
                            return result
        return result
    
    def pointInBoundsRect(self, aPoint):
        result = False
        result = delphi_compatability.PtInRect(self.normalBoundsRect_pixels, aPoint)
        return result
    
    def pointColorMatch(self, xPixel, yPixel):
        result = False
        testPixelColor = TColor()
        
        testPixelColor = self.previewCache.Canvas.Pixels[xPixel, yPixel]
        result = testPixelColor != udomain.domain.options.transparentColor
        return result
    
    def pointColorAdjacentMatch(self, xPixel, yPixel, position):
        result = False
        testPixelColor = TColor()
        x = 0L
        y = 0L
        
        x = xPixel
        y = yPixel
        if position == 0:
            # 0 1 2
            # 3 x 4
            # 5 6 7
            x = xPixel - 1
            y = yPixel - 1
        elif position == 1:
            x = xPixel + 0
            y = yPixel - 1
        elif position == 2:
            x = xPixel + 1
            y = yPixel - 1
        elif position == 3:
            x = xPixel - 1
            y = yPixel + 0
        elif position == 4:
            # point x := xPixel + 0; y := yPixel + 0; this is the point already tested
            x = xPixel + 1
            y = yPixel + 0
        elif position == 5:
            x = xPixel - 1
            y = yPixel + 1
        elif position == 6:
            x = xPixel + 0
            y = yPixel + 1
        elif position == 7:
            x = xPixel + 1
            y = yPixel + 1
        testPixelColor = self.previewCache.Canvas.Pixels[x, y]
        result = testPixelColor != udomain.domain.options.transparentColor
        return result
    
    def saveToGlobal3DOutputFile(self, indexOfPlant, translate, rectWithAllPlants, outputType, aTurtle):
        remPoints = [None] * 4
        remWidth = 0.0
        fileExportSurface = KfFileExportSurface()
        relativeBasePoint_mm = SinglePoint()
        i = 0
        fixRotation = 0
        
        if self.firstPhytomer == None:
            return
        self.turtle = aTurtle
        if self.turtle == None:
            GeneralException.create("Problem: Nil turtle in PdPlant.saveToGlobal3DOutputFile.")
        fileExportSurface = self.turtle.fileExportSurface()
        if self.turtle == None:
            GeneralException.create("Problem: Nil export surface in PdPlant.saveToGlobal3DOutputFile.")
        self.setUpTurtleFor3DOutput()
        if translate:
            relativeBasePoint_mm.x = umath.safedivExcept(self.basePoint_pixels().X - rectWithAllPlants.Left, udomain.domain.plantDrawScale_PixelsPerMm(), 0) - udomain.domain.plantDrawOffset_mm().x
            relativeBasePoint_mm.y = umath.safedivExcept(self.basePoint_pixels().Y - rectWithAllPlants.Top, udomain.domain.plantDrawScale_PixelsPerMm(), 0) - udomain.domain.plantDrawOffset_mm().y
            if outputType != u3dexport.kPOV:
                # move plant to translate, except for for POV, where you translate and scale afterward
                self.turtle.xyz(relativeBasePoint_mm.x, relativeBasePoint_mm.y, 0)
            else:
                fileExportSurface.setTranslationForCurrentPlant(translate, relativeBasePoint_mm.x, relativeBasePoint_mm.y)
        self.turtle.writingTo = outputType
        fileExportSurface.startPlant(self.name, indexOfPlant)
        if outputType == u3dexport.k3DS:
            for i in range(0, u3dexport.kExportPartLast + 1):
                # for 3DS need to write out all colors in front especially; must be done before reminder
                fileExportSurface.writeMaterialDescription(i, self.colorForDXFPartType(i))
            if not udomain.domain.registered:
                fileExportSurface.writeMaterialDescription(-1, UNRESOLVED.rgb(100, 100, 100))
        if outputType == u3dexport.kDXF:
            # these rotations are to fix consistent misrotations - the option sits on top of them
            # comes out sideways
            fixRotation = 64
        elif outputType == u3dexport.kPOV:
            # okay
            fixRotation = 0
        elif outputType == u3dexport.k3DS:
            # comes out sideways
            fixRotation = 64
        elif outputType == u3dexport.kOBJ:
            # okay
            fixRotation = 0
        elif outputType == u3dexport.kVRML:
            # okay
            fixRotation = 0
        elif outputType == u3dexport.kLWO:
            # comes out upside down
            fixRotation = 128
        else :
            raise GeneralException.create("Problem: Invalid export type in PdPlant.saveToGlobal3DOutputFile.")
        self.turtle.rotateX(fixRotation)
        # this is a user-specified turn on top of the default
        self.turtle.rotateX(udomain.domain.exportOptionsFor3D[outputType].xRotationBeforeDraw * 256.0 / 360.0)
        if not udomain.domain.registered:
            remWidth = self.realDrawingScale_pixelsPerMm() * 5.0
            self.turtle.push()
            self.turtle.moveInMillimeters(remWidth / 2)
            self.turtle.rotateY(64)
            self.turtle.moveInMillimeters(remWidth / 2)
            remPoints[0] = self.turtle.position()
            self.turtle.rotateY(64)
            self.turtle.moveInMillimeters(remWidth)
            remPoints[1] = self.turtle.position()
            self.turtle.rotateY(64)
            self.turtle.moveInMillimeters(remWidth)
            remPoints[2] = self.turtle.position()
            self.turtle.rotateY(64)
            self.turtle.moveInMillimeters(remWidth)
            remPoints[3] = self.turtle.position()
            self.turtle.pop()
            fileExportSurface.writeRegistrationReminder(remPoints[0], remPoints[1], remPoints[2], remPoints[3])
        self.draw()
        fileExportSurface.endPlant()
    
    def setUpTurtleFor3DOutput(self):
        self.turtle.drawOptions.sortPolygons = False
        self.turtle.drawOptions.drawLines = False
        self.turtle.drawOptions.lineContrastIndex = 0
        self.turtle.drawOptions.wireFrame = False
        self.turtle.drawOptions.drawStems = True
        self.turtle.drawOptions.draw3DObjects = True
        self.turtle.drawOptions.draw3DObjectsAsRects = False
        self.turtle.drawOptions.circlePoints = False
        # must be after pane and draw options set 
        self.turtle.reset()
        self.turtle.setScale_pixelsPerMm(self.realDrawingScale_pixelsPerMm())
        self.turtle.drawingSurface.foreColor = delphi_compatability.clGreen
        self.turtle.drawingSurface.backColor = delphi_compatability.clRed
        self.turtle.drawingSurface.lineColor = delphi_compatability.clBlue
        self.turtle.xyz(0, 0, 0)
        self.turtle.resetBoundsRect(Point(0, 0))
    
    # ----------------------------------------------------------------------------------  i/o and data transfer 
    def defaultAllParameters(self):
        for param in udomain.domain.parameterManager.parameters:
            if param.fieldType != uparams.kFieldHeader:
                self.defaultParameter(param, kDontCheckForUnreadParams)
        self.finishLoadingOrDefaulting(kDontCheckForUnreadParams)
    
    def defaultParameter(self, param, writeDebugMessage):
        if param == None:
            return
        if param.fieldType == uparams.kFieldBoolean:
            tempBoolean = usupport.strToBool(param.defaultValueString())
            tempBoolean = self.transferField(kSetField, tempBoolean, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldSmallint:
            tempSmallint = StrToIntDef(usupport.stringUpTo(param.defaultValueString(), " "), 0)
            tempSmallint = self.transferField(kSetField, tempSmallint, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldEnumeratedList:
            tempSmallint = StrToIntDef(usupport.stringUpTo(param.defaultValueString(), " "), 0)
            tempSmallint = self.transferField(kSetField, tempSmallint, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldLongint:
            tempLongint = StrToIntDef(param.defaultValueString(), 0)
            tempLongint = self.transferField(kSetField, tempLongint, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldColor:
            tempColorRef = usupport.rgbStringToColor(param.defaultValueString())
            tempColorRef = self.transferField(kSetField, tempColorRef, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldFloat:
            if param.indexType == uparams.kIndexTypeSCurve:
                #this is the only array
                self.changingWholeSCurves = True
                tempSCurve = umath.stringToSCurve(param.defaultValueString())
                self.transferWholeSCurve(kSetField, tempSCurve, param.fieldNumber, param.fieldType, False, None)
                self.changingWholeSCurves = False
            else:
                succesful, tempFloat = usupport.boundForString(param.defaultValueString(), uparams.kFieldFloat)
                tempFloat = self.transferField(kSetField, tempFloat, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldThreeDObject:
            tempTdo = utdo.KfObject3D()
            tempTdo.readFromInputString(param.defaultValueString(), utdo.kAdjustForOrigin)
            tempTdo = self.transferField(kSetField, tempTdo, param.fieldNumber, param.fieldType, 0, False, None)
        if writeDebugMessage:
            udebug.DebugPrint("Plant <" + self.name + "> parameter <" + param.name + "> defaulted to <" + param.defaultValueString() + ">")
    
    def writeToMainFormMemoAsText(self):
        fakeTextFile = TextFile()
        
        self.writingToMemo = True
        try:
            self.writeToPlantFile(fakeTextFile)
        finally:
            self.writingToMemo = False
    
    def writeLine(self, plantFile, aString):
        if self.writingToMemo:
            umain.MainForm.plantsAsTextMemo.Lines.Add(aString)
        else:
            writeln(plantFile, aString)
    
    def writeToPlantFile(self, plantFile):
        tempSCurve = umath.SCurveStructure()
        
        if umain.MainForm != None:
            # v2.0 saving selection state in main window
            self.selectedWhenLastSaved = umain.MainForm.isSelected(self)
        else:
            self.selectedWhenLastSaved = False
        start = " ["
        stop = "] ="
        # v2.0
        self.writeLine(plantFile, "[" + self.name + "] " + kPlantAsTextStartString + " <v2.0>")
        if self.noteLines:
            self.writeLine(plantFile, kStartNoteString)
            for noteLine in self.noteLines:
                self.writeLine(plantFile, noteLine)
            self.writeLine(plantFile, kEndNoteString)
        if len(udomain.domain.sectionManager.sections) > 0:
            for section in udomain.domain.sectionManager.sections:
                if section == None:
                    continue
                # write out section header with name 
                self.writeLine(plantFile, "; ------------------------- " + section.getName())
                for j in range(0, section.numSectionItems):
                    # write out params 
                    param = udomain.domain.parameterManager.parameterForFieldNumber(section.sectionItems[j])
                    if param == None:
                        continue
                    if param.fieldType == uparams.kFieldHeader:
                        pass
                    elif param.fieldType == uparams.kFieldBoolean:
                        #skip
                        tempBoolean = self.transferField(kGetField, tempBoolean, param.fieldNumber, param.fieldType, 0, False, None)
                        self.writeLine(plantFile, param.name + start + param.fieldID + stop + usupport.boolToStr(tempBoolean))
                    elif param.fieldType == uparams.kFieldSmallint:
                        tempSmallint = self.transferField(kGetField, tempSmallint, param.fieldNumber, param.fieldType, 0, False, None)
                        self.writeLine(plantFile, param.name + start + param.fieldID + stop + IntToStr(tempSmallint))
                    elif param.fieldType == uparams.kFieldEnumeratedList:
                        tempSmallint = self.transferField(kGetField, tempSmallint, param.fieldNumber, param.fieldType, 0, False, None)
                        self.writeLine(plantFile, param.name + start + param.fieldID + stop + IntToStr(tempSmallint))
                    elif param.fieldType == uparams.kFieldLongint:
                        tempLongint = self.transferField(kGetField, tempLongint, param.fieldNumber, param.fieldType, 0, False, None)
                        self.writeLine(plantFile, param.name + start + param.fieldID + stop + IntToStr(tempLongint))
                    elif param.fieldType == uparams.kFieldColor:
                        tempColorRef = self.transferField(kGetField, tempColorRef, param.fieldNumber, param.fieldType, 0, False, None)
                        self.writeLine(plantFile, param.name + start + param.fieldID + stop + IntToStr(tempColorRef))
                    elif param.fieldType == uparams.kFieldFloat:
                        if param.indexType == uparams.kIndexTypeSCurve:
                            #this is the only array
                            self.transferWholeSCurve(kGetField, tempSCurve, param.fieldNumber, param.fieldType, False, None)
                            self.writeLine(plantFile, param.name + start + param.fieldID + stop + umath.sCurveToString(tempSCurve))
                        else:
                            tempFloat = self.transferField(kGetField, tempFloat, param.fieldNumber, param.fieldType, 0, False, None)
                            self.writeLine(plantFile, param.name + start + param.fieldID + stop + usupport.digitValueString(tempFloat))
                    elif param.fieldType == uparams.kFieldThreeDObject:
                        tempTdo = utdo.KfObject3D()
                        tempTdo = self.transferField(kGetField, tempTdo, param.fieldNumber, param.fieldType, 0, False, None)
                        self.writeLine(plantFile, param.name + start + param.fieldID + stop + tempTdo.name)
                        if self.writingToMemo:
                            tempTdo.writeToMemo(umain.MainForm.plantsAsTextMemo)
                        else:
                            tempTdo.writeToFileStream(plantFile, utdo.kEmbeddedInPlant)

        for amendment in self.amendments:
            if self.writingToMemo:
                amendment.writeToMemo(umain.MainForm.plantsAsTextMemo)
            else:
                amendment.writeToTextFile(plantFile)
        #v2.0
        self.writeLine(plantFile, "; ------------------------- " + kPlantAsTextEndString + " " + self.getName() + " <v2.0>")
        self.writeLine(plantFile, "")
    
    def readLineAndTdoFromPlantFile(self, aLine, plantFile):        
        if string_match(kStartNoteString, aLine) > 0:
            # read note if this line starts it
            # this only will happen if in file
            self.noteLines = []
            noteLine = readln(plantFile)
            while noteLine != None:
                # PDF -- seemed like a strange check so removed -- maybe should be "OR" and not?
                if string_match(kEndNoteString, noteLine): # and (len(self.noteLines) < 5000):
                    break
                else:
                    self.noteLines.append(noteLine)
                noteLine = readln(plantFile)
            # added v2.0, no use reading other stuff when finished with note
            return
        if string_match(uamendmt.kStartAmendmentString, aLine) > 0:
            # read amendment if line is an amendment - v2.0
            newAmendment = uamendmt.PdPlantDrawingAmendment()
            if self.readingFromMemo:
                self.readingMemoLine = newAmendment.readFromMemo(umain.MainForm.plantsAsTextMemo, self.readingMemoLine)
            else:
                newAmendment.readFromTextFile(plantFile)
            self.addAmendment(newAmendment)
            return
        if (not string_match("[", aLine, find=1)) or (not string_match("=", aLine, find=1)):
            if self.readingFromMemo:
                # v2.0 fix lines broken before [ or = (does NOT fix lines broken within strings)
                # this has to come AFTER we deal with notes and amendments; it applies to parameters only
                secondLine = umain.MainForm.plantsAsTextMemo.Lines.Strings[self.readingMemoLine]
            else:
                secondLine = usupport.tolerantReadln(plantFile, secondLine)
            self.readingMemoLine += 1
            udebug.DebugPrint("plant <" + self.name + "> line <" + aLine + "> merged with <" + secondLine + ">")
            aLine = aLine + " " + secondLine
        nameAndFieldID = usupport.stringUpTo(aLine, "=")
        fieldID = usupport.stringBeyond(nameAndFieldID, "[")
        fieldID = usupport.stringUpTo(fieldID, "]")
        if string_match("header", fieldID):
            return
        paramValue = usupport.stringBeyond(aLine, "=")
        
        # search for pararmeter information
        found = False
        parameters = udomain.domain.parameterManager.parameters
        for param in parameters:
            if param == None:
                return
            if param.fieldID == fieldID:
                found = True
                break 
        if not found:
            return
        
        if param.fieldType == uparams.kFieldHeader:
            pass
        elif param.fieldType == uparams.kFieldBoolean:
            #skip
            tempBoolean = usupport.strToBool(paramValue)
            tempBoolean = self.transferField(kSetField, tempBoolean, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldSmallint:
            tempSmallint = StrToIntDef(paramValue, 0)
            if (param.lowerBound() != 0) or (param.upperBound() != 0):
                if tempSmallint < intround(param.lowerBound()):
                    # if both bounds are zero, it means not to check them 
                    tempSmallint = intround(param.lowerBound())
                if tempSmallint > intround(param.upperBound()):
                    tempSmallint = intround(param.upperBound())
            tempSmallint = self.transferField(kSetField, tempSmallint, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldEnumeratedList:
            tempSmallint = StrToIntDef(paramValue, 0)
            if (param.lowerBound() != 0) or (param.upperBound() != 0):
                if tempSmallint < intround(param.lowerBound()):
                    # if both bounds are zero, it means not to check them 
                    tempSmallint = intround(param.lowerBound())
                if tempSmallint > intround(param.upperBound()):
                    tempSmallint = intround(param.upperBound())
            tempSmallint = self.transferField(kSetField, tempSmallint, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldLongint:
            tempLongint = StrToIntDef(paramValue, 0)
            if (param.lowerBound() != 0) or (param.upperBound() != 0):
                if tempLongint < intround(param.lowerBound()):
                    # if both bounds are zero, it means not to check them 
                    tempLongint = intround(param.lowerBound())
                if tempLongint > intround(param.upperBound()):
                    tempLongint = intround(param.upperBound())
            if param.fieldNumber == utransfr.kStateBasePointY:
                tempLongint = tempLongint
            tempLongint = self.transferField(kSetField, tempLongint, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldColor:
            tempColorRef = StrToIntDef(paramValue, 0)
            tempColorRef = self.transferField(kSetField, tempColorRef, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldFloat:
            if param.indexType == uparams.kIndexTypeSCurve:
                #this is the only array
                self.changingWholeSCurves = True
                tempSCurve = umath.stringToSCurve(paramValue)
                if (tempSCurve.x1 <= 0.0) or (tempSCurve.y1 <= 0.0) or (tempSCurve.x2 <= 0.0) or (tempSCurve.y2 <= 0.0) or (tempSCurve.x1 >= 1.0) or (tempSCurve.y1 >= 1.0) or (tempSCurve.x2 >= 1.0) or (tempSCurve.y2 >= 1.0):
                    # bound s curve
                    # all s curve values (x and y) must be between 0 and 1 EXCLUSIVE
                    # if not in this range, set whole curve to reasonable values
                    # instead of raising exception, just hard-code whole curve to acceptable values
                    # don't use Parameters.tab default in case that was read in wrong also
                    tempSCurve.x1 = 0.25
                    tempSCurve.y1 = 0.1
                    tempSCurve.x2 = 0.65
                    tempSCurve.y2 = 0.85
                self.transferWholeSCurve(kSetField, tempSCurve, param.fieldNumber, param.fieldType, False, None)
                self.changingWholeSCurves = False
            else:
                succesful, tempFloat = usupport.boundForString(paramValue, uparams.kFieldFloat)
                if string_match("Drawing scale", param.name):
                    tempTdo = None
                if (param.lowerBound() != 0) or (param.upperBound() != 0):
                    if tempFloat < param.lowerBound():
                        # if both bounds are zero, it means not to check them 
                        tempFloat = param.lowerBound()
                    if tempFloat > param.upperBound():
                        tempFloat = param.upperBound()
                tempFloat = self.transferField(kSetField, tempFloat, param.fieldNumber, param.fieldType, 0, False, None)
        elif param.fieldType == uparams.kFieldThreeDObject:
            tempTdo = utdo.KfObject3D()
            tempTdo.setName(usupport.trimLeftAndRight(paramValue))
            if self.readingFromMemo:
                self.readingMemoLine = tempTdo.readFromMemo(umain.MainForm.plantsAsTextMemo, self.readingMemoLine)
            else:
                tempTdo.readFromFileStream(plantFile, utdo.kEmbeddedInPlant)
            tempTdo = self.transferField(kSetField, tempTdo, param.fieldNumber, param.fieldType, 0, False, None)

        param.valueHasBeenReadForCurrentPlant = True
    
    def finishLoadingOrDefaulting(self, checkForUnreadParams):
        if checkForUnreadParams:
            parameters = udomain.domain.parameterManager.parameters
            for param in parameters:
                if (not param.valueHasBeenReadForCurrentPlant) and (param.fieldType != uparams.kFieldHeader):
                    self.defaultParameter(param, checkForUnreadParams)
        self.pGeneral.ageAtWhichFloweringStarts = umath.intMin(self.pGeneral.ageAtWhichFloweringStarts, self.pGeneral.ageAtMaturity)
        self.age = umath.intMin(self.age, self.pGeneral.ageAtMaturity)
        umath.calcSCurveCoeffs(self.pGeneral.growthSCurve)
        umath.calcSCurveCoeffs(self.pFruit.sCurveParams)
        umath.calcSCurveCoeffs(self.pLeaf.sCurveParams)
        self.regrow()
    
    def editTransferField(self, d, value, fieldID, fieldType, fieldIndex, regrow):
        if fieldType == uparams.kFieldHeader:
            return value
        if (d == kGetField):
            value = self.transferField(d, value, fieldID, fieldType, fieldIndex, regrow, None)
        else:
            updateList = ucollect.TListCollection()
            value = self.transferField(d, value, fieldID, fieldType, fieldIndex, regrow, updateList)
            if len(updateList) > 0:
                umain.MainForm.updateParameterValuesWithUpdateListForPlant(self, updateList)
                if (udomain.domain.options.updateTimeSeriesPlantsOnParameterChange) and (utimeser.TimeSeriesForm != None):
                    utimeser.TimeSeriesForm.updatePlantsFromParent(self)

        if (d == kSetField) and regrow:
            self.regrow()
        return value
    
    def transferField(self, d, v, fieldID, ft, index, regrow, updateList):
        if ft == uparams.kFieldHeader:
            return v
        v = self.directTransferField(d, v, fieldID, ft, index, updateList)
        if d == kSetField:
            if fieldID == utransfr.kFruitSCurve:
                if not self.changingWholeSCurves:
                    # cfk fix: should be not allowing to change these to values that don't work 
                    umath.calcSCurveCoeffs(self.pFruit.sCurveParams)
            elif fieldID == utransfr.kGeneralGrowthSCurve:
                if not self.changingWholeSCurves:
                    umath.calcSCurveCoeffs(self.pGeneral.growthSCurve)
            elif fieldID == utransfr.kLeafSCurve:
                if not self.changingWholeSCurves:
                    umath.calcSCurveCoeffs(self.pLeaf.sCurveParams)
            elif fieldID == utransfr.kGeneralAgeAtMaturity:
                if (self.age > v):
                    self.setAge(v)
            if (ft == uparams.kFieldColor):
                self.needToRecalculateColors = True
        return v
    
    def directTransferField(self, d, v, fieldID, ft, index, updateList):
        if fieldID <= 200:
            # switch-over point is hard-coded and must be identical to that set in PlantStudio Utility program
            # that generates utransfr.pas
            v = utransfr.Plant_directTransferField(self, v, d, fieldID, ft, index, updateList)
        else:
            v = utransfr.Plant_directTransferField_SecondPart(self, v, d, fieldID, ft, index, updateList)
        if updateList != None:
            self.addToUpdateList(fieldID, updateList)
        return v
    
    def addToUpdateList(self, fieldID, updateList):
        updateEvent = PdPlantUpdateEvent()
        
        if updateList == None:
            return
        updateEvent = PdPlantUpdateEvent.create
        updateEvent.plant = self
        updateEvent.fieldID = fieldID
        updateList.Add(updateEvent)
    
    def fillEnumStringList(self, list, fieldID, hasRadioButtons):
        if fieldID == utransfr.kLeafCompoundPinnateOrPalmate:
            # assumes list being given to it is empty 
            list.Add("pinnate (feather-like)")
            list.Add("palmate (hand-like)")
            hasRadioButtons = True
        elif fieldID == utransfr.kMeristemAndLeafArrangement:
            list.Add("alternate (one per node)")
            list.Add("opposite (two per node)")
            hasRadioButtons = True
        elif fieldID == utransfr.kLeafCompoundPinnateArrangement:
            list.Add("alternate")
            list.Add("opposite")
            hasRadioButtons = True
        elif fieldID == utransfr.kFlowerFemaleBudOption:
            list.Add("no bud")
            list.Add("single 3D object bud (old style)")
            list.Add("unfolding flower (new style)")
            hasRadioButtons = True
        elif fieldID == utransfr.kFlowerMaleBudOption:
            list.Add("no bud")
            list.Add("single 3D object bud (old style)")
            list.Add("unfolding flower (new style)")
            hasRadioButtons = True
        else :
            raise GeneralException.create("Problem: Unknown field for plant string list " + IntToStr(fieldID) + " in method PdPlant.fillEnumStringList.")
        return hasRadioButtons
    
    def transferObject3D(self, direction, myTdo, otherTdo):
        if (myTdo == None) or (otherTdo == None):
            # assumption: both tdos exist 
            raise GeneralException.create("Problem: Nil 3D object in method PdPlant.transferObject3D.")
        if direction == kSetField:
            myTdo.copyFrom(otherTdo)
        else:
            otherTdo.copyFrom(myTdo)
    
    def transferWholeSCurve(self, direction, value, fieldNumber, fieldType, regrow, updateList):
        value.x1 = self.transferField(direction, value.x1, fieldNumber, fieldType, 0, regrow, updateList)
        value.y1 = self.transferField(direction, value.y1, fieldNumber, fieldType, 1, regrow, updateList)
        value.x2 = self.transferField(direction, value.x2, fieldNumber, fieldType, 2, regrow, updateList)
        value.y2 = self.transferField(direction, value.y2, fieldNumber, fieldType, 3, regrow, updateList)
    
    def MFD(self, objectValue, value, fieldType, direction):
        if direction == kGetField:
            if fieldType == uparams.kFieldFloat:
                #MFD = MoveFieldData
                value = objectValue
            elif fieldType == uparams.kFieldSmallint:
                value = objectValue
            elif fieldType == uparams.kFieldLongint:
                value = objectValue
            elif fieldType == uparams.kFieldColor:
                value = objectValue
            elif fieldType == uparams.kFieldBoolean:
                value = objectValue
            elif fieldType == uparams.kFieldEnumeratedList:
                value = objectValue
            else :
                raise GeneralException.create("Problem: Unsupported transfer from field " + IntToStr(fieldType) + " in method PdPlant.MFD.")
        elif direction == kSetField:
            if fieldType == uparams.kFieldFloat:
                objectValue = value
            elif fieldType == uparams.kFieldSmallint:
                objectValue = value
            elif fieldType == uparams.kFieldLongint:
                objectValue = value
            elif fieldType == uparams.kFieldColor:
                objectValue = value
            elif fieldType == uparams.kFieldBoolean:
                objectValue = value
            elif fieldType == uparams.kFieldEnumeratedList:
                objectValue = value
            else :
                raise GeneralException.create("Problem: Unsupported transfer to field " + IntToStr(fieldType) + " in method PdPlant.MFD.")
        return objectValue, value
    
    # ------------------------------------------------------------------------------- breeding 
    def useBreedingOptionsAndPlantsToSetParameters(self, options, firstPlant, secondPlant, tdos):
        if firstPlant == None:
            return
        saveAge = self.age
        self.reset()
        for sectionIndex in range(0, len(udomain.domain.sectionManager.sections)):
            section = udomain.domain.sectionManager.sections[sectionIndex]
            if section == None:
                continue
            for paramIndex in range(0, section.numSectionItems):
                param = udomain.domain.parameterManager.parameterForFieldNumber(section.sectionItems[paramIndex])
                if (param == None) or (param.fieldType == uparams.kFieldHeader):
                    continue
                #case
                if param.fieldType == uparams.kFieldBoolean:
                    #non-numeric
                    firstBoolean = False
                    firstBoolean = firstPlant.transferField(kGetField, firstBoolean, param.fieldNumber, param.fieldType, 0, False, None)
                    if secondPlant == None:
                        newBoolean = firstBoolean
                    else:
                        secondBoolean = False
                        secondBoolean = secondPlant.transferField(kGetField, secondBoolean, param.fieldNumber, param.fieldType, 0, False, None)
                        if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) == kFromFirstPlant:
                            newBoolean = firstBoolean
                        else:
                            newBoolean = secondBoolean
                    newBoolean = self.transferField(kSetField, newBoolean, param.fieldNumber, param.fieldType, 0, False, None)
                elif param.fieldType == uparams.kFieldSmallint:
                    #numeric
                    newInteger = 0
                    firstInteger = 0
                    firstInteger = firstPlant.transferField(kGetField, firstInteger, param.fieldNumber, param.fieldType, 0, False, None)
                    if secondPlant == None:
                        newInteger = firstInteger
                    else:
                        secondInteger = 0
                        secondInteger = secondPlant.transferField(kGetField, secondInteger, param.fieldNumber, param.fieldType, 0, False, None)
                        if firstInteger == secondInteger:
                            newInteger = firstInteger
                        else:
                            weight = options.firstPlantWeights[sectionIndex] / 100.0
                            newInteger = intround(firstInteger * weight + secondInteger * (1.0 - weight))
                    # extra limit on mutation to stop exceptions
                    stdDev = 0.5 * newInteger * options.mutationStrengths[sectionIndex] / 100.0
                    newInteger = intround(self.breedingGenerator.randomNormalWithStdDev(newInteger * 1.0, stdDev))
                    newInteger = intround(umath.min(param.upperBound(), umath.max(param.lowerBound(), 1.0 * newInteger)))
                    newInteger = self.transferField(kSetField, newInteger, param.fieldNumber, param.fieldType, 0, False, None)
                elif param.fieldType == uparams.kFieldLongint:
                    pass
                elif param.fieldType == uparams.kFieldEnumeratedList:
                    # the only numeric fields so far are the plant's position x and y (which is redone anyway)
                    #            and the random number seed, which shouldn't really be bred anyway, so we will do nothing
                    #            here. if you want to add longint parameters later, you will have to copy the smallint stuff
                    #            to put here. 
                    #non-numeric
                    firstInteger = 0
                    firstInteger = firstPlant.transferField(kGetField, firstInteger, param.fieldNumber, param.fieldType, 0, False, None)
                    if secondPlant == None:
                        newInteger = firstInteger
                    else:
                        secondInteger = 0
                        secondInteger = secondPlant.transferField(kGetField, secondInteger, param.fieldNumber, param.fieldType, 0, False, None)
                        if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) == kFromFirstPlant:
                            newInteger = firstInteger
                        else:
                            newInteger = secondInteger
                    newInteger = self.transferField(kSetField, newInteger, param.fieldNumber, param.fieldType, 0, False, None)
                elif param.fieldType == uparams.kFieldColor:
                    #numeric if option is set, otherwise non-numeric
                    firstColor = None
                    secondColor = None
                    firstColor = firstPlant.transferField(kGetField, firstColor, param.fieldNumber, param.fieldType, 0, False, None)
                    if secondPlant == None:
                        newColor = firstColor
                    else:
                        secondColor = secondPlant.transferField(kGetField, secondColor, param.fieldNumber, param.fieldType, 0, False, None)
                        if not options.mutateAndBlendColorValues:
                            if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) == kFromFirstPlant:
                                newColor = firstColor
                            else:
                                newColor = secondColor
                    if options.mutateAndBlendColorValues:
                        newColor = self.blendAndMutateColors(options, sectionIndex, (secondPlant != None), firstColor, secondColor)
                    newColor = self.transferField(kSetField, newColor, param.fieldNumber, param.fieldType, 0, False, None)
                elif param.fieldType == uparams.kFieldFloat:
                    if param.indexType == uparams.kIndexTypeSCurve:
                        firstSCurve = umath.SCurveStructure()
                        secondSCurve = umath.SCurveStructure()
                        # considering s curve non-numeric, too much trouble to make sure it is all right, and there are only two 
                        self.changingWholeSCurves = True
                        firstPlant.transferWholeSCurve(kGetField, firstSCurve, param.fieldNumber, param.fieldType, False, None)
                        if secondPlant == None:
                            newSCurve = firstSCurve
                        else:
                            secondPlant.transferWholeSCurve(kGetField, secondSCurve, param.fieldNumber, param.fieldType, False, None)
                            if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) == kFromFirstPlant:
                                newSCurve = firstSCurve
                            else:
                                newSCurve = secondSCurve
                        self.transferWholeSCurve(kSetField, newSCurve, param.fieldNumber, param.fieldType, False, None)
                        self.changingWholeSCurves = False
                        #plain float - numeric
                    else:
                        # newFloat := 0.0001;  v2.0 removed this
                        firstFloat = 0.0
                        firstFloat = firstPlant.transferField(kGetField, firstFloat, param.fieldNumber, param.fieldType, 0, False, None)
                        if secondPlant == None:
                            newFloat = firstFloat
                        else:
                            secondFloat = 0.0
                            secondFloat = secondPlant.transferField(kGetField, secondFloat, param.fieldNumber, param.fieldType, 0, False, None)
                            if firstFloat == secondFloat:
                                newFloat = firstFloat
                            else:
                                weight = options.firstPlantWeights[sectionIndex] / 100.0
                                newFloat = firstFloat * weight + secondFloat * (1.0 - weight)
                        # extra limit on mutation to stop exceptions
                        stdDev = 0.5 * newFloat * options.mutationStrengths[sectionIndex] / 100.0
                        newFloat = self.breedingGenerator.randomNormalWithStdDev(newFloat * 1.0, stdDev)
                        newFloat = umath.min(param.upperBound(), umath.max(param.lowerBound(), newFloat))
                        # for now, don't let float get to zero because it causes problems 
                        # newFloat := max(0.0001, newFloat);  v2.0 removed this to enable breeding with no variation
                        newFloat = self.transferField(kSetField, newFloat, param.fieldNumber, param.fieldType, 0, False, None)
                elif param.fieldType == uparams.kFieldThreeDObject:
                    #non-numeric
                    firstTdo = utdo.KfObject3D()
                    secondTdo = utdo.KfObject3D()
                    newTdo = utdo.KfObject3D()

                    firstTdo = firstPlant.transferField(kGetField, firstTdo, param.fieldNumber, param.fieldType, 0, False, None)
                    if secondPlant == None:
                        newTdo.copyFrom(firstTdo)
                    else:
                        secondTdo = secondPlant.transferField(kGetField, secondTdo, param.fieldNumber, param.fieldType, 0, False, None)
                        if not options.chooseTdosRandomlyFromCurrentLibrary:
                            if self.pickPlantToCopyNonNumericalParameterFrom(options, sectionIndex) == kFromFirstPlant:
                                newTdo.copyFrom(firstTdo)
                            else:
                                newTdo.copyFrom(secondTdo)
                        else:
                            randomTdo = self.tdoRandomlyPickedFromCurrentLibrary(tdos)
                            if randomTdo != None:
                                newTdo.copyFrom(randomTdo)
                    if options.chooseTdosRandomlyFromCurrentLibrary:
                        randomTdo = self.tdoRandomlyPickedFromCurrentLibrary(tdos)
                        if randomTdo != None:
                            newTdo.copyFrom(randomTdo)
                    newTdo = self.transferField(kSetField, newTdo, param.fieldNumber, param.fieldType, 0, False, None)
                else:
                    # note that longints are not handled here - they are used only for position information
                    #            and not for normal parameters 
                    raise GeneralException.create("Problem: Invalid parameter type in method PdPlant.useBreedingOptionsAndPlantsToSetParameters.")
                #param loop
            #section loop
        self.finishLoadingOrDefaulting(kDontCheckForUnreadParams)
        self.setAge(saveAge)
    
    def pickPlantToCopyNonNumericalParameterFrom(self, options, sectionIndex):
        result = 0
        result = kFromFirstPlant
        if options.getNonNumericalParametersFrom == kFromFirstPlant:
            result = kFromFirstPlant
        elif options.getNonNumericalParametersFrom == kFromSecondPlant:
            result = kFromSecondPlant
        elif options.getNonNumericalParametersFrom == kFromProbabilityBasedOnWeightsForSection:
            if self.breedingGenerator.zeroToOne() < options.firstPlantWeights[sectionIndex] / 100.0:
                result = kFromFirstPlant
            else:
                result = kFromSecondPlant
        elif options.getNonNumericalParametersFrom == kFromPlantWithGreaterWeightForSectionIfEqualFirstPlant:
            if options.firstPlantWeights[sectionIndex] >= 50:
                result = kFromFirstPlant
            else:
                result = kFromSecondPlant
        elif options.getNonNumericalParametersFrom == kFromPlantWithGreaterWeightForSectionIfEqualSecondPlant:
            if options.firstPlantWeights[sectionIndex] > 50:
                result = kFromFirstPlant
            else:
                result = kFromSecondPlant
        elif options.getNonNumericalParametersFrom == kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly:
            if options.firstPlantWeights[sectionIndex] > 50:
                result = kFromFirstPlant
            elif options.firstPlantWeights[sectionIndex] < 50:
                #50/50
                result = kFromSecondPlant
            else:
                if self.breedingGenerator.zeroToOne() <= 0.5:
                    result = kFromFirstPlant
                else:
                    result = kFromSecondPlant
        return result
    
    def blendAndMutateColors(self, options, sectionIndex, haveSecondPlant, firstColor, secondColor):
        result = UnassignedColor
        weight = 0.0
        stdDevAsFractionOfMean = 0.0
        firstColorAsFloat = 0.0
        secondColorAsFloat = 0.0
        resultAsFloat = 0.0
        mutationStrengthToUse = 0.0
        
        firstColorAsFloat = firstColor
        resultAsFloat = firstColorAsFloat
        if haveSecondPlant:
            secondColorAsFloat = secondColor
            weight = options.firstPlantWeights[sectionIndex] / 100.0
            resultAsFloat = firstColorAsFloat * weight + secondColorAsFloat * (1.0 - weight)
        # v2.0 can mutate colors separately from other parameters - if other params not zero, go with that,
        # if other params zero, and mutating colors, use low mutation for colors only
        mutationStrengthToUse = 0
        if options.mutationStrengths[sectionIndex] > 0:
            mutationStrengthToUse = options.mutationStrengths[sectionIndex]
        elif options.mutateAndBlendColorValues:
            mutationStrengthToUse = udomain.kLowMutation
        stdDevAsFractionOfMean = mutationStrengthToUse / 100.0
        # for colors, reduce std dev to 10% of for other things, because the numbers are so huge 
        stdDevAsFractionOfMean = stdDevAsFractionOfMean * 0.1
        resultAsFloat = self.breedingGenerator.randomNormalWithStdDev(resultAsFloat, resultAsFloat * stdDevAsFractionOfMean)
        result = intround(resultAsFloat)
        return result
    
    def tdoRandomlyPickedFromCurrentLibrary(self, tdos):
        result = None
        if tdos == None:
            return result
        if len(tdos) <= 0:
            return result
        index = umath.intMax(0, umath.intMin(len(tdos) - 1, intround(self.breedingGenerator.zeroToOne() * len(tdos))))
        result = tdos[index]
        return result
    
    # -------------------------------------------------------------------------------  data transfer for binary copy 
    def classAndVersionInformation(self, cvir):
        cvir.classNumber = uclasses.kPdPlant
        cvir.versionNumber = 2
        cvir.additionNumber = 0
    
    def streamDataWithFiler(self, filer, cvir):
        tdoSeedlingLeaf = KfObject3d()
        tdoLeaf = KfObject3d()
        tdoStipule = KfObject3d()
        tdoAxillaryBud = KfObject3d()
        tdoInflorBractFemale = KfObject3d()
        tdoInflorBractMale = KfObject3d()
        tdoFruit = KfObject3d()
        tdoRoot = KfObject3d()
        femaleFlowerTdos = [None] * (kHighestFloralPartConstant + 1)
        maleFlowerTdos = [None] * (kHighestFloralPartConstant + 1)
        traverser = PdTraverser()
        hasFirstPhytomer = False
        partType = 0
        
        PdStreamableObject.streamDataWithFiler(self, filer, cvir)
        self.name = filer.streamShortString(self.name)
        self.age = filer.streamSmallint(self.age)
        filer.streamSinglePoint(self.basePoint_mm)
        self.xRotation = filer.streamSingle(self.xRotation)
        self.yRotation = filer.streamSingle(self.yRotation)
        self.zRotation = filer.streamSingle(self.zRotation)
        self.drawingScale_PixelsPerMm = filer.streamSingle(self.drawingScale_PixelsPerMm)
        filer.streamRect(self.normalBoundsRect_pixels)
        self.hidden = filer.streamBoolean(self.hidden)
        self.justCopiedFromMainWindow = filer.streamBoolean(self.justCopiedFromMainWindow)
        self.indexWhenRemoved = filer.streamSmallint(self.indexWhenRemoved)
        self.selectedIndexWhenRemoved = filer.streamSmallint(self.selectedIndexWhenRemoved)
        if filer.isReading():
            # save pointers to 3d objects if reading because they will get written over during streaming of structures 
            tdoSeedlingLeaf = self.pSeedlingLeaf.leafTdoParams.object3D
            tdoLeaf = self.pLeaf.leafTdoParams.object3D
            tdoStipule = self.pLeaf.stipuleTdoParams.object3D
            tdoInflorBractFemale = self.pInflor[kGenderFemale].bractTdoParams.object3D
            tdoInflorBractMale = self.pInflor[kGenderMale].bractTdoParams.object3D
            for partType in range(0, kHighestFloralPartConstant + 1):
                femaleFlowerTdos[partType] = self.pFlower[kGenderFemale].tdoParams[partType].object3D
                maleFlowerTdos[partType] = self.pFlower[kGenderMale].tdoParams[partType].object3D
            tdoAxillaryBud = self.pAxillaryBud.tdoParams.object3D
            tdoFruit = self.pFruit.tdoParams.object3D
            tdoRoot = self.pRoot.tdoParams.object3D
        else:
            tdoSeedlingLeaf = None
            tdoLeaf = None
            tdoStipule = None
            tdoInflorBractFemale = None
            tdoInflorBractMale = None
            for partType in range(0, kHighestFloralPartConstant + 1):
                femaleFlowerTdos[partType] = None
                maleFlowerTdos[partType] = None
            tdoAxillaryBud = None
            tdoFruit = None
            tdoRoot = None
        self.pGeneral = filer.streamBytes(self.pGeneral, FIX_sizeof(self.pGeneral))
        self.pMeristem = filer.streamBytes(self.pMeristem, FIX_sizeof(self.pMeristem))
        self.pInternode = filer.streamBytes(self.pInternode, FIX_sizeof(self.pInternode))
        self.pLeaf = filer.streamBytes(self.pLeaf, FIX_sizeof(self.pLeaf))
        self.pSeedlingLeaf = filer.streamBytes(self.pSeedlingLeaf, FIX_sizeof(self.pSeedlingLeaf))
        self.pAxillaryBud = filer.streamBytes(self.pAxillaryBud, FIX_sizeof(self.pAxillaryBud))
        self.pInflor[kGenderMale] = filer.streamBytes(self.pInflor[kGenderMale], FIX_sizeof(self.pInflor))
        self.pInflor[kGenderFemale] = filer.streamBytes(self.pInflor[kGenderFemale], FIX_sizeof(self.pInflor))
        self.pFlower[kGenderMale] = filer.streamBytes(self.pFlower[kGenderMale], FIX_sizeof(self.pFlower))
        self.pFlower[kGenderFemale] = filer.streamBytes(self.pFlower[kGenderFemale], FIX_sizeof(self.pFlower))
        self.pFruit = filer.streamBytes(self.pFruit, FIX_sizeof(self.pFruit))
        self.pRoot = filer.streamBytes(self.pRoot, FIX_sizeof(self.pRoot))
        if filer.isReading():
            # reset pointers if reading and stream 3d objects 
            self.pSeedlingLeaf.leafTdoParams.object3D = tdoSeedlingLeaf
        self.pSeedlingLeaf.leafTdoParams.object3D.streamUsingFiler(filer)
        if filer.isReading():
            self.pLeaf.leafTdoParams.object3D = tdoLeaf
        self.pLeaf.leafTdoParams.object3D.streamUsingFiler(filer)
        if filer.isReading():
            self.pLeaf.stipuleTdoParams.object3D = tdoStipule
        self.pLeaf.stipuleTdoParams.object3D.streamUsingFiler(filer)
        if filer.isReading():
            self.pInflor[kGenderFemale].bractTdoParams.object3D = tdoInflorBractFemale
        self.pInflor[kGenderFemale].bractTdoParams.object3D.streamUsingFiler(filer)
        if filer.isReading():
            self.pInflor[kGenderMale].bractTdoParams.object3D = tdoInflorBractMale
        self.pInflor[kGenderMale].bractTdoParams.object3D.streamUsingFiler(filer)
        for partType in range(0, kHighestFloralPartConstant + 1):
            if filer.isReading():
                self.pFlower[kGenderFemale].tdoParams[partType].object3D = femaleFlowerTdos[partType]
            self.pFlower[kGenderFemale].tdoParams[partType].object3D.streamUsingFiler(filer)
            if filer.isReading():
                self.pFlower[kGenderMale].tdoParams[partType].object3D = maleFlowerTdos[partType]
            self.pFlower[kGenderMale].tdoParams[partType].object3D.streamUsingFiler(filer)
        if filer.isReading():
            self.pAxillaryBud.tdoParams.object3D = tdoAxillaryBud
        self.pAxillaryBud.tdoParams.object3D.streamUsingFiler(filer)
        if filer.isReading():
            self.pFruit.tdoParams.object3D = tdoFruit
        self.pFruit.tdoParams.object3D.streamUsingFiler(filer)
        if filer.isReading():
            self.pRoot.tdoParams.object3D = tdoRoot
        self.pRoot.tdoParams.object3D.streamUsingFiler(filer)
        self.randomNumberGenerator.streamUsingFiler(filer)
        self.breedingGenerator.streamUsingFiler(filer)
        # biomass info 
        self.totalBiomass_pctMPB = filer.streamSingle(self.totalBiomass_pctMPB)
        self.reproBiomass_pctMPB = filer.streamSingle(self.reproBiomass_pctMPB)
        self.changeInShootBiomassToday_pctMPB = filer.streamSingle(self.changeInShootBiomassToday_pctMPB)
        self.changeInReproBiomassToday_pctMPB = filer.streamSingle(self.changeInReproBiomassToday_pctMPB)
        self.unallocatedNewVegetativeBiomass_pctMPB = filer.streamSingle(self.unallocatedNewVegetativeBiomass_pctMPB)
        self.unremovedDeadVegetativeBiomass_pctMPB = filer.streamSingle(self.unremovedDeadVegetativeBiomass_pctMPB)
        self.unallocatedNewReproductiveBiomass_pctMPB = filer.streamSingle(self.unallocatedNewReproductiveBiomass_pctMPB)
        self.unremovedDeadReproductiveBiomass_pctMPB = filer.streamSingle(self.unremovedDeadReproductiveBiomass_pctMPB)
        self.unremovedStandingDeadBiomass_pctMPB = filer.streamSingle(self.unremovedStandingDeadBiomass_pctMPB)
        self.numApicalActiveReproductiveMeristemsOrInflorescences = filer.streamLongint(self.numApicalActiveReproductiveMeristemsOrInflorescences)
        self.numAxillaryActiveReproductiveMeristemsOrInflorescences = filer.streamLongint(self.numAxillaryActiveReproductiveMeristemsOrInflorescences)
        self.numApicalInactiveReproductiveMeristems = filer.streamLongint(self.numApicalInactiveReproductiveMeristems)
        self.numAxillaryInactiveReproductiveMeristems = filer.streamLongint(self.numAxillaryInactiveReproductiveMeristems)
        self.ageOfYoungestPhytomer = filer.streamSmallint(self.ageOfYoungestPhytomer)
        self.needToRecalculateColors = filer.streamBoolean(self.needToRecalculateColors)
        self.ageAtWhichFloweringStarted = filer.streamSmallint(self.ageAtWhichFloweringStarted)
        self.floweringHasStarted = filer.streamBoolean(self.floweringHasStarted)
        self.totalPlantParts = filer.streamLongint(self.totalPlantParts)
        # plant parts 
        traverser = None
        if filer.isReading():
            hasFirstPhytomer = filer.streamBoolean(hasFirstPhytomer)
            if self.firstPhytomer != None:
                #don't want to create if not written
                self.freeAllDrawingPlantParts()
            if hasFirstPhytomer:
                self.firstPhytomer = None
                self.firstPhytomer = uintern.PdInternode()
                if self.firstPhytomer != None:
                    uintern.PdInternode(self.firstPhytomer).plant = self
                else:
                    raise GeneralException.create("Problem: Could not create first internode in method PdPlant.streamDataWithFiler.")
        elif filer.isWriting():
            hasFirstPhytomer = self.firstPhytomer != None
            hasFirstPhytomer = filer.streamBoolean(hasFirstPhytomer)
        if hasFirstPhytomer:
            traverser = utravers.PdTraverser().createWithPlant(self)
            try:
                traverser.filer = filer
                traverser.traverseWholePlant(utravers.kActivityStream)
            finally:
                traverser.free
        self.previewCache.streamUsingFiler(filer)
        if filer.isReading():
            umath.calcSCurveCoeffs(self.pFruit.sCurveParams)
            umath.calcSCurveCoeffs(self.pGeneral.growthSCurve)
            umath.calcSCurveCoeffs(self.pLeaf.sCurveParams)
        self.amendments.streamUsingFiler(filer, uamendmt.PdPlantDrawingAmendment)
    
    # --------------------------------------------------------------------------------  command-related 
    def randomize(self):
        seed = 0
        breedingSeed = 0L
        anXRotation = 0.0
        
        seed = self.randomNumberGenerator.randomSmallintSeedFromTime()
        breedingSeed = self.breedingGenerator.randomSeedFromTime()
        anXRotation = self.randomNumberGenerator.zeroToOne() * 360.0
        self.randomizeWithSeedsAndXRotation(seed, breedingSeed, anXRotation)
    
    def randomizeWithSeedsAndXRotation(self, generalSeed, breedingSeed, anXRotation):
        self.pGeneral.startingSeedForRandomNumberGenerator = generalSeed
        self.breedingGenerator.setSeed(breedingSeed)
        self.xRotation = anXRotation
        self.regrow()
        # tell main window to update in case showing parameter panel 
        # if this is a breeder plant, it will create the update list, but the main window won't
        # recognize the plant pointer. this is extra memory use, but i'd have to pass a boolean all
        # over to stop it, and the list only has one item
        updateList = ucollect.TListCollection()
        updateEvent = PdPlantUpdateEvent()

        updateEvent.plant = self
        #hard-coded
        updateEvent.fieldID = utransfr.kGeneralStartingSeedForRandomNumberGenerator
        updateList.Add(updateEvent)
        # PDF PORT COMMENTED OUT FOR TESTING __ PUT BACK
        #### PUT BACK: umain.MainForm.updateParameterValuesWithUpdateListForPlant(self, updateList)

    # ------------------------------------------------------------------------------------  next day and traverser 
    def nextDay(self):
        try:
            # calculate overall biomass change using s curve 
            #print " plant age ageAtMaturity", self.name, self.age, self.pGeneral.ageAtMaturity
            fractionToMaturity_frn = umath.safedivExcept(self.age, self.pGeneral.ageAtMaturity, 0)
            newTotalBiomass_pctMPB = umath.max(0.0, umath.min(100.0, 100.0 * umath.scurve(fractionToMaturity_frn, self.pGeneral.growthSCurve.c1, self.pGeneral.growthSCurve.c2)))
            changeInTotalBiomassTodayAsPercentOfMPB_pct = newTotalBiomass_pctMPB - self.totalBiomass_pctMPB
            self.totalBiomass_pctMPB = newTotalBiomass_pctMPB
            if self.floweringHasStarted:
                # divide up change into shoot and fruit, make changes to total shoot/fruit 
                fractionReproBiomassToday_frn = umath.max(0, self.pGeneral.fractionReproductiveAllocationAtMaturity_frn * umath.safedivExcept(self.age - self.ageAtWhichFloweringStarted, self.pGeneral.ageAtMaturity - self.ageAtWhichFloweringStarted, 0))
                newReproBiomass_pctMPB = fractionReproBiomassToday_frn * self.totalBiomass_pctMPB
                self.changeInReproBiomassToday_pctMPB = newReproBiomass_pctMPB - self.reproBiomass_pctMPB
                self.reproBiomass_pctMPB = newReproBiomass_pctMPB
                # rest goes to shoots 
                newShootBiomass_pctMPB = self.totalBiomass_pctMPB - self.reproBiomass_pctMPB
                self.changeInShootBiomassToday_pctMPB = newShootBiomass_pctMPB - self.shootBiomass_pctMPB
                self.shootBiomass_pctMPB = newShootBiomass_pctMPB
            else:
                self.changeInReproBiomassToday_pctMPB = 0.0
                self.changeInShootBiomassToday_pctMPB = changeInTotalBiomassTodayAsPercentOfMPB_pct
                self.shootBiomass_pctMPB = self.totalBiomass_pctMPB
            if self.shootBiomass_pctMPB + self.reproBiomass_pctMPB > 100.0:
                self.shootBiomass_pctMPB = self.shootBiomass_pctMPB
            traverser = utravers.PdTraverser().createWithPlant(self)
            try:
                if (self.firstPhytomer == None):
                    #If first day, create first phytomer. Assume seed reserves are placed into this phytomer.
                    firstMeristem = umerist.PdMeristem().newWithPlant(self)
                    self.firstPhytomer = firstMeristem.createFirstPhytomer()
                    if self.firstPhytomer == None:
                        #Must tell firstPhytomer to recalculate internode angle because it did not know it was the
                        #      first phytomer until after drawing plant got this pointer back.
                        return
                    self.firstPhytomer.setAsFirstPhytomer()
                    # reduce changeInShootBiomassToday_pctMPB for amount used to make first phytomer 
                    self.changeInShootBiomassToday_pctMPB = self.changeInShootBiomassToday_pctMPB - firstMeristem.optimalInitialPhytomerBiomass_pctMPB()
                if not self.floweringHasStarted and (self.age >= self.pGeneral.ageAtWhichFloweringStarts):
                    # decide if flowering has started using params 
                    self.floweringHasStarted = True
                    self.ageAtWhichFloweringStarted = self.age
                    # tell all meristems to switch over 
                    traverser.traverseWholePlant(utravers.kActivityStartReproduction)
                self.allocateOrRemoveBiomassWithTraverser(traverser)
                if self.firstPhytomer != None:
                    traverser.ageOfYoungestPhytomer = delphi_compatability.MaxLongInt
                else:
                    traverser.ageOfYoungestPhytomer = 0
                traverser.traverseWholePlant(utravers.kActivityNextDay)
                self.ageOfYoungestPhytomer = traverser.ageOfYoungestPhytomer
                self.age += 1
            finally:
                self.needToRecalculateColors = True
        except Exception, e:
            raise
            usupport.messageForExceptionType(e, "PdPlant.nextDay")
    
    def allocateOrRemoveBiomassWithTraverser(self, traverserProxy):
        if self.firstPhytomer == None:
            return
        traverser = traverserProxy
        if traverser == None:
            return
        if self.changeInShootBiomassToday_pctMPB > 0:
            # set addition and reduction from changes, and add in amounts rolled over from yesterday 
            shootAddition_pctMPB = self.changeInShootBiomassToday_pctMPB + self.unallocatedNewVegetativeBiomass_pctMPB
            self.unallocatedNewVegetativeBiomass_pctMPB = 0.0
            shootReduction_pctMPB = 0.0
        else:
            shootReduction_pctMPB = self.changeInShootBiomassToday_pctMPB + self.unremovedDeadVegetativeBiomass_pctMPB
            self.unremovedDeadVegetativeBiomass_pctMPB = 0.0
            shootAddition_pctMPB = 0.0
        if self.changeInReproBiomassToday_pctMPB > 0:
            reproAddition_pctMPB = self.changeInReproBiomassToday_pctMPB + self.unallocatedNewReproductiveBiomass_pctMPB
            self.unallocatedNewReproductiveBiomass_pctMPB = 0.0
            reproReduction_pctMPB = 0.0
        else:
            reproReduction_pctMPB = self.changeInReproBiomassToday_pctMPB + self.unremovedDeadReproductiveBiomass_pctMPB
            self.unremovedDeadReproductiveBiomass_pctMPB = 0.0
            reproAddition_pctMPB = 0.0
        # see if amounts can cancel out to any extent 
        shootAddition_pctMPB, shootReduction_pctMPB = cancelOutOppositeAmounts(shootAddition_pctMPB, shootReduction_pctMPB)
        reproAddition_pctMPB, reproReduction_pctMPB = cancelOutOppositeAmounts(reproAddition_pctMPB, reproReduction_pctMPB)
        if shootAddition_pctMPB > 0.0:
            # allocate new shoot biomass 
            self.unallocatedNewVegetativeBiomass_pctMPB = self.allocateOrRemoveParticularBiomass(shootAddition_pctMPB, self.unallocatedNewVegetativeBiomass_pctMPB, utravers.kActivityDemandVegetative, utravers.kActivityGrowVegetative, traverser)
        if shootReduction_pctMPB > 0.0:
            # remove dead shoot biomass 
            self.unremovedDeadVegetativeBiomass_pctMPB = self.allocateOrRemoveParticularBiomass(shootReduction_pctMPB, self.unremovedDeadVegetativeBiomass_pctMPB, utravers.kActivityVegetativeBiomassThatCanBeRemoved, utravers.kActivityRemoveVegetativeBiomass, traverser)
        if reproAddition_pctMPB > 0.0:
            # allocate new fruit biomass 
            self.unallocatedNewReproductiveBiomass_pctMPB = self.allocateOrRemoveParticularBiomass(reproAddition_pctMPB, self.unallocatedNewReproductiveBiomass_pctMPB, utravers.kActivityDemandReproductive, utravers.kActivityGrowReproductive, traverser)
        if reproReduction_pctMPB > 0.0:
            # remove dead fruit biomass 
            self.unremovedDeadReproductiveBiomass_pctMPB = self.allocateOrRemoveParticularBiomass(reproReduction_pctMPB, self.unremovedDeadReproductiveBiomass_pctMPB, utravers.kActivityReproductiveBiomassThatCanBeRemoved, utravers.kActivityRemoveReproductiveBiomass, traverser)
    
    def allocateOrRemoveParticularBiomass(self, biomassToAddOrRemove_pctMPB, undistributedBiomass_pctMPB, askingMode, tellingMode, traverserProxy):
        try:
            traverser = traverserProxy
            if traverser == None:
                return undistributedBiomass_pctMPB
            traverser.traverseWholePlant(askingMode)
            totalDemandOrAvailableBiomass_pctMPB = traverser.total
            if totalDemandOrAvailableBiomass_pctMPB > 0.0:
                if biomassToAddOrRemove_pctMPB > totalDemandOrAvailableBiomass_pctMPB:
                    undistributedBiomass_pctMPB = biomassToAddOrRemove_pctMPB - totalDemandOrAvailableBiomass_pctMPB
                    traverser.fractionOfPotentialBiomass = 1.0
                else:
                    traverser.fractionOfPotentialBiomass = umath.safedivExcept(biomassToAddOrRemove_pctMPB, totalDemandOrAvailableBiomass_pctMPB, 0)
                traverser.traverseWholePlant(tellingMode)
            else:
                # no demand 
                undistributedBiomass_pctMPB = undistributedBiomass_pctMPB + biomassToAddOrRemove_pctMPB
        except Exception, e:
            # PDF PORT TEMP ADDED RAISE
            raise
            usupport.messageForExceptionType(e, "PdPlant.allocateOrRemoveParticularBiomass")
        return undistributedBiomass_pctMPB
    
    def getPlantStatistics(self, statisticsProxy):
        statistics = PdPlantStatistics()
        traverser = PdTraverser()
        
        statistics = utravers.PdPlantStatistics(statisticsProxy)
        if statistics == None:
            return
        traverser = utravers.PdTraverser().createWithPlant(self)
        try:
            traverser.statistics = statistics
            traverser.traverseWholePlant(utravers.kActivityGatherStatistics)
        finally:
            traverser.free
        # set undistributed amounts in statistics 
        statistics.liveBiomass_pctMPB[utravers.kStatisticsPartTypeUnallocatedNewVegetativeBiomass] = self.unallocatedNewVegetativeBiomass_pctMPB
        statistics.deadBiomass_pctMPB[utravers.kStatisticsPartTypeUnremovedDeadVegetativeBiomass] = self.unremovedDeadVegetativeBiomass_pctMPB
        statistics.liveBiomass_pctMPB[utravers.kStatisticsPartTypeUnallocatedNewReproductiveBiomass] = self.unallocatedNewReproductiveBiomass_pctMPB
        statistics.deadBiomass_pctMPB[utravers.kStatisticsPartTypeUnremovedDeadReproductiveBiomass] = self.unremovedDeadReproductiveBiomass_pctMPB
    
    def report(self):
        traverser = PdTraverser()
        
        if (self.firstPhytomer != None):
            udebug.DebugPrint("---------------------- Start plant report")
            traverser = utravers.PdTraverser().createWithPlant(self)
            try:
                traverser.traverseWholePlant(utravers.kActivityReport)
            finally:
                traverser.free
            udebug.DebugPrint("---------------------- End plant report")
    
    # --------------------------------------------------------------------------------------------- amendments 
    def amendmentForPartID(self, partID):
        result = None
        for amendment in self.amendments:
            if (amendment.partID == partID):
                result = amendment
                return result
        return result
    
    def addAmendment(self, newAmendment):
        self.amendments.Add(newAmendment)
    
    def removeAmendment(self, oldAmendment):
        self.amendments.Remove(oldAmendment)
    
    def removeAllAmendments(self):
        self.amendments = ucollect.TListCollection()
    
    def clearPointersToAllAmendments(self):
        self.amendments.clear()
    
    def restoreAmendmentPointersToList(self, aList):
        if (aList != None):
            for item in aList:
                self.addAmendment(item)
    
    def plantPartForPartID(self, partID):
        result = TObject()
        traverser = PdTraverser()
        
        result = None
        if (self.firstPhytomer != None):
            traverser = utravers.PdTraverser().createWithPlant(self)
            try:
                traverser.foundPlantPart = None
                traverser.partID = partID
                traverser.traverseWholePlant(utravers.kActivityFindPartForPartID)
                result = traverser.foundPlantPart
            finally:
                traverser.free
        return result
    
    def getInfoForPlantPartAtPoint(self, point, partID, partType):
        partID = -1
        partType = ""
        part = self.findPlantPartAtPositionByTestingPolygons(Point)
        if part == None:
            return partID, partType
        partID = part.partID
        partType = part.getName()
        return partID, partType
    
    def colorForDXFPartType(self, index):
        result = UnassignedColor
        if index == u3dexport.kExportPartMeristem:
            result = self.pAxillaryBud.tdoParams.faceColor
        elif index == u3dexport.kExportPartInternode:
            result = self.pInternode.faceColor
        elif index == u3dexport.kExportPartSeedlingLeaf:
            result = self.pSeedlingLeaf.leafTdoParams.faceColor
        elif index == u3dexport.kExportPartLeaf:
            result = self.pLeaf.leafTdoParams.faceColor
        elif index == u3dexport.kExportPartFirstPetiole:
            result = self.pLeaf.petioleColor
        elif index == u3dexport.kExportPartPetiole:
            result = self.pLeaf.petioleColor
        elif index == u3dexport.kExportPartLeafStipule:
            result = self.pLeaf.stipuleTdoParams.faceColor
        elif index == u3dexport.kExportPartInflorescenceStalkFemale:
            result = self.pInflor[kGenderFemale].stalkColor
        elif index == u3dexport.kExportPartInflorescenceInternodeFemale:
            result = self.pInflor[kGenderFemale].stalkColor
        elif index == u3dexport.kExportPartInflorescenceBractFemale:
            result = self.pInflor[kGenderFemale].bractTdoParams.faceColor
        elif index == u3dexport.kExportPartInflorescenceStalkMale:
            result = self.pInflor[kGenderMale].stalkColor
        elif index == u3dexport.kExportPartInflorescenceInternodeMale:
            result = self.pInflor[kGenderMale].stalkColor
        elif index == u3dexport.kExportPartInflorescenceBractMale:
            result = self.pInflor[kGenderMale].bractTdoParams.faceColor
        elif index == u3dexport.kExportPartPedicelFemale:
            result = self.pInflor[kGenderFemale].pedicelColor
        elif index == u3dexport.kExportPartFlowerBudFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kBud].faceColor
        elif index == u3dexport.kExportPartStyleFemale:
            result = self.pFlower[kGenderFemale].styleColor
        elif index == u3dexport.kExportPartStigmaFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kPistils].faceColor
        elif index == u3dexport.kExportPartFilamentFemale:
            result = self.pFlower[kGenderFemale].filamentColor
        elif index == u3dexport.kExportPartAntherFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kStamens].faceColor
        elif index == u3dexport.kExportPartFirstPetalsFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kFirstPetals].faceColor
        elif index == u3dexport.kExportPartSecondPetalsFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kSecondPetals].faceColor
        elif index == u3dexport.kExportPartThirdPetalsFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kThirdPetals].faceColor
        elif index == u3dexport.kExportPartFourthPetalsFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kFourthPetals].faceColor
        elif index == u3dexport.kExportPartFifthPetalsFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kFifthPetals].faceColor
        elif index == u3dexport.kExportPartSepalsFemale:
            result = self.pFlower[kGenderFemale].tdoParams[kSepals].faceColor
        elif index == u3dexport.kExportPartPedicelMale:
            result = self.pInflor[kGenderMale].pedicelColor
        elif index == u3dexport.kExportPartFlowerBudMale:
            result = self.pFlower[kGenderMale].tdoParams[kBud].faceColor
        elif index == u3dexport.kExportPartFilamentMale:
            result = self.pFlower[kGenderMale].filamentColor
        elif index == u3dexport.kExportPartAntherMale:
            result = self.pFlower[kGenderMale].tdoParams[kStamens].faceColor
        elif index == u3dexport.kExportPartFirstPetalsMale:
            result = self.pFlower[kGenderMale].tdoParams[kFirstPetals].faceColor
        elif index == u3dexport.kExportPartSepalsMale:
            result = self.pFlower[kGenderMale].tdoParams[kSepals].faceColor
        elif index == u3dexport.kExportPartUnripeFruit:
            result = self.pFruit.tdoParams.alternateFaceColor
        elif index == u3dexport.kExportPartRipeFruit:
            result = self.pFruit.tdoParams.faceColor
        elif index == u3dexport.kExportPartRootTop:
            result = self.pRoot.tdoParams.faceColor
        else :
            raise GeneralException.create("Problem: Invalid part type in method colorForDXFPartType.")
        return result
    
class PdPlantUpdateEvent:
    def __init__(self):
        self.plant = None
        self.fieldID = 0
        self.fieldIndex = 0

# copied from plant manager file for testing
def checkVersionNumberInPlantNameLine(aLine):
    # assumes line given is plant start line
    # e.g., >>> [rose] start PlantStudio plant <v1.0>
    plantName = usupport.stringBetween("[", "]", aLine)
    versionNumberString = usupport.stringBetween("<", ">", aLine)
    versionNumberString = usupport.stringBetween("v", ".", versionNumberString)
    versionNumber = StrToIntDef(versionNumberString, 0)
    if versionNumber > 2:
        ShowMessage("The plant \"" + plantName + "\" has a major version number of " + IntToStr(versionNumber) + "," + chr(13) + "which is higher than this major version of PlantStudio (2)." + chr(13) + chr(13) + "That means that although I may be able to read the plant," + chr(13) + "it will probably look better in the most up-to-date version of PlantStudio," + chr(13) + "which you can get at the PlantStudio web site.")

# --------------------------------------------------------------------------------------- input/output 
class PlantLoader:
    def __init__(self):
        self.plants = ucollect.TListCollection()

    def loadPlantsFromFile(self, fileName, inPlantMover, justLoad=0):
        inputFile = TextFile()

        AssignFile(inputFile, fileName)
        try:
            # v1.5
            # PDF PORT __ commented out
            #usupport.setDecimalSeparator()
            Reset(inputFile)
            self.plants.clear()
            # defaults in case things are missing from file
            self.plantDrawOffset_mm = SinglePoint()
            self.plantDrawScale_PixelsPerMm = 1.0
            if not justLoad:
                self.mainWindowViewMode = udomain.domain.options.mainWindowViewMode
                self.mainWindowOrientation = udomain.domain.options.mainWindowOrientation
                self.showBoundsRectangle = udomain.domain.options.showBoundsRectangle
            concentratedLastTimeSaved = False
            self.fitInVisibleAreaForConcentrationChange = False
            aLine = readln(inputFile)
            while aLine != None:
                # cfk testing
                if (aLine == "") or (aLine[0] == ";"):
                    aLine = readln(inputFile)
                    continue
                if string_startsWith("offset=", aLine):
                    self.plantDrawOffset_mm = usupport.stringToSinglePoint(usupport.stringBeyond(aLine, "="))
                elif string_startsWith("scale=", aLine):
                    try:
                        self.plantDrawScale_PixelsPerMm = intround(StrToFloat(usupport.stringBeyond(aLine, "=")) * 100.0) / 100.0
                    except:
                        self.plantDrawScale_PixelsPerMm = 1.0
                elif string_startsWith("concentrated=", aLine):
                    if not justLoad:
                        concentratedLastTimeSaved = udomain.domain.viewPlantsInMainWindowOnePlantAtATime()
                        if udomain.domain.options.ignoreWindowSettingsInFile:
                            # v2.1 if ignoring settings in file, use current settings, otherwise use what is in file
                            concentratedInFile = (self.mainWindowViewMode == udomain.kViewPlantsInMainWindowOneAtATime)
                        else:
                            concentratedInFile = usupport.strToBool(usupport.stringBeyond(aLine, "="))
                        if concentratedInFile:
                            self.mainWindowViewMode = udomain.kViewPlantsInMainWindowOneAtATime
                        else:
                            self.mainWindowViewMode = udomain.kViewPlantsInMainWindowFreeFloating
                        if not inPlantMover:
                            udomain.domain.options.mainWindowViewMode = self.mainWindowViewMode
                        self.fitInVisibleAreaForConcentrationChange = concentratedInFile and not concentratedLastTimeSaved
                elif string_startsWith("orientation (top/side)=", aLine):
                    if not justLoad:
                        if not udomain.domain.options.ignoreWindowSettingsInFile:
                            # v2.1 only read if not ignoring settings in file
                            self.mainWindowOrientation = StrToInt(usupport.stringBeyond(aLine, "="))
                elif string_startsWith("boxes=", aLine):
                    self.showBoundsRectangle = usupport.strToBool(usupport.stringBeyond(aLine, "="))
                    if not justLoad:
                        if not inPlantMover:
                            udomain.domain.options.showBoundsRectangle = self.showBoundsRectangle
                        if (umain.MainForm != None) and (not umain.MainForm.inFormCreation) and (not inPlantMover):
                            umain.MainForm.updateForChangeToDomainOptions()
                            umain.MainForm.copyDrawingBitmapToPaintBox()
                elif string_startsWith("[", aLine):
                    # plant start line
                    checkVersionNumberInPlantNameLine(aLine)
                    plant = PdPlant()
                    plantName = usupport.stringBeyond(aLine, "[")
                    plantName = usupport.stringUpTo(plantName, "]")
                    plant.setName(plantName)
                    if not justLoad:
                        udomain.domain.parameterManager.setAllReadFlagsToFalse()
                    # cfk change v1.3
                    # changed reading end of plant to read "end PlantStudio plant" instead of empty line because
                    # sometimes text wrapping puts empty lines in, not a good measure of completion.
                    # now end of plant must be there to be read. could produce endless loop if no end
                    # of plant, so stop at absolute cutoff of 300 non-empty, non-comment lines (there are now 215 parameters).
                    # also stop reading if reach next plant square bracket or end of file.
                    # v2.0 increased number of params to 350 so 300 is problem, changed to 3000 to avoid this in future, oops
                    lineCount = 0
                    while (not string_match(kPlantAsTextEndString, aLine)) and (lineCount <= 3000):
                        # aLine <> '' do
                        aLine = readln(inputFile)
                        if aLine == None:
                            break
                        if (string_startsWith("[", aLine)):
                            # v1.60 reversed order of the next two lines -- fixes infinite loop when no end of plant
                            # v1.3 added check for next plant or eof
                            break
                        if (trim(aLine) == "") or (string_startsWith(";", aLine)):
                            # v1.3 added skip empty lines
                            continue
                        plant.readLineAndTdoFromPlantFile(aLine, inputFile)
                        lineCount = lineCount + 1
                    plant.finishLoadingOrDefaulting(kCheckForUnreadParams)
                    self.plants.Add(plant)
                if aLine != None and not string_startsWith("[", aLine):
                    aLine = readln(inputFile)
        finally:
            CloseFile(inputFile)
        return self.plants

if __name__ == '__main__':
    #tests
    print "test"
    p = PdPlant()
    l = PlantLoader()
    l.loadPlantsFromFile("test tree.pla", inPlantMover=1, justLoad=1)
    print l.plants.list
    print "done"
