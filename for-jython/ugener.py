# unit Ugener

from conversion_common import *
import usupport
import utdo
import umath
import udomain
import ucollect
import uplant
import delphi_compatability

# --------------------------------------------------------------------------------- PdGeneration 
class PdGeneration:
    def __init__(self):
        self.firstParent = None
        self.secondParent = None
        self.selectedPlants = ucollect.TListCollection()
        self.plants = ucollect.TListCollection()
    
    def createWithParents(self, parentOne, parentTwo, fractionOfMaxAge):
        # note: this is only used right now in the PdBreedFromParentsCommand command, so some things might not
        #    fit other situations. if you need to use it somewhere else, check that you want to do everything that
        #    is done here. 
        if parentOne != None:
            newPlant = parentOne.makeCopy()
            # v2.0
            newPlant.removeAllAmendments()
            newPlant.setAge(intround(newPlant.pGeneral.ageAtMaturity * fractionOfMaxAge))
            self.plants.Add(newPlant)
            self.firstParent = newPlant
            if self.plants.IndexOf(parentOne) >= 0:
                # only select parent if this is being done from the breeder and you have the parents already 
                self.selectedPlants.Add(self.firstParent)
        if parentTwo != None:
            newPlant = parentTwo.makeCopy()
            # v2.0
            newPlant.removeAllAmendments()
            newPlant.setAge(intround(newPlant.pGeneral.ageAtMaturity * fractionOfMaxAge))
            self.plants.Add(newPlant)
            self.secondParent = newPlant
            if self.plants.IndexOf(parentTwo) >= 0:
                # only select parent if this is being done from the breeder and you have the parents already 
                self.selectedPlants.Add(self.secondParent)
        return self
    
    def selectPlant(self, aPlant, shift):
        if shift:
            self.selectedPlants.Add(aPlant)
        else:
            self.selectedPlants.Clear()
            self.selectedPlants.Add(aPlant)
    
    def deselectAllPlants(self):
        self.selectedPlants.Clear()
    
    def firstSelectedPlant(self):
        result = None
        if len(self.selectedPlants) > 0:
            result = self.selectedPlants[0]
        return result
    
    def secondSelectedPlant(self):
        result = None
        if len(self.selectedPlants) > 1:
            result = self.selectedPlants[1]
        return result
    
    def breedFromParents(self, aFirstParent, aSecondParent, fractionOfMaxAge):
        self.firstParent = aFirstParent
        if self.firstParent == None:
            return
        if udomain.domain == None:
            return
        self.secondParent = aSecondParent
        self.plants.Clear()
        self.selectedPlants.Clear()
        tdos = None
        if (udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary) and (not udomain.domain.checkForExistingDefaultTdoLibrary()):
            MessageDialog("Because you didn't choose a 3D object library, the breeder won't be able" + chr(13) + "to randomly choose 3D objects for your breeding offspring." + chr(13) + chr(13) + "You can choose a library later by choosing Custom from the Variation menu" + chr(13) + "and choosing a 3D object library there.", mtWarning, [mbOK, ], 0)

        if udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary:
            tdos = ucollect.TListCollection()
            fileNameWithPath = udomain.domain.defaultTdoLibraryFileName
            if not FileExists(fileNameWithPath):
                udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary = False
            else:
                # cfk note: is it really ok to read the whole tdo file each time? 
                AssignFile(inputFile, fileNameWithPath)
                try:
                    # v1.5
                    usupport.setDecimalSeparator()
                    Reset(inputFile)
                    while not UNRESOLVED.eof(inputFile):
                        newTdo = utdo.KfObject3D()
                        newTdo.readFromFileStream(inputFile, utdo.kInTdoLibrary)
                        tdos.Add(newTdo)
                finally:
                    CloseFile(inputFile)
        for i in range(0, udomain.domain.breedingAndTimeSeriesOptions.plantsPerGeneration):
            newPlant = uplant.PdPlant()
            self.plants.Add(newPlant)
            newPlant.reset()
            if udomain.domain.breedingAndTimeSeriesOptions.variationType != udomain.kBreederVariationNoNumeric:
                newPlant.randomize()
            localOptions = uplant.BreedingAndTimeSeriesOptionsStructure()
            self.setLocalOptionsToDomainOptions(localOptions)
            newPlant.useBreedingOptionsAndPlantsToSetParameters(localOptions, self.firstParent, self.secondParent, tdos)
            newAge = intround(newPlant.pGeneral.ageAtMaturity * fractionOfMaxAge)
            newPlant.setAge(umath.intMin(newAge, newPlant.pGeneral.ageAtMaturity))
            # v2.0 plants take rotation angles from first parent
            newPlant.xRotation = self.firstParent.xRotation
            newPlant.yRotation = self.firstParent.yRotation
            newPlant.zRotation = self.firstParent.zRotation
    
    def setLocalOptionsToDomainOptions(self, localOptions):
        for i in range(0, uplant.kMaxBreedingSections + 1):
            # defaults
            localOptions.firstPlantWeights[i] = 50
        localOptions.getNonNumericalParametersFrom = uplant.kFromPlantWithGreaterWeightForSectionIfEqualChooseRandomly
        # copy (done separate from low/med/custom) v2.0
        localOptions.mutateAndBlendColorValues = udomain.domain.breedingAndTimeSeriesOptions.mutateAndBlendColorValues
        localOptions.chooseTdosRandomlyFromCurrentLibrary = udomain.domain.breedingAndTimeSeriesOptions.chooseTdosRandomlyFromCurrentLibrary
        if udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationLow:
            for i in range(0, uplant.kMaxBreedingSections + 1):
                localOptions.mutationStrengths[i] = udomain.kLowMutation
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationMedium:
            for i in range(0, uplant.kMaxBreedingSections + 1):
                localOptions.mutationStrengths[i] = udomain.kMediumMutation
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationHigh:
            for i in range(0, uplant.kMaxBreedingSections + 1):
                localOptions.mutationStrengths[i] = udomain.kHighMutation
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationCustom:
            localOptions = udomain.domain.breedingAndTimeSeriesOptions
        elif udomain.domain.breedingAndTimeSeriesOptions.variationType == udomain.kBreederVariationNoNumeric:
            for i in range(0, uplant.kMaxBreedingSections + 1):
                localOptions.mutationStrengths[i] = udomain.kNoMutation
    
    def plantForIndex(self, index):
        result = None
        if index < 0:
            return result
        if index > len(self.plants) - 1:
            return result
        if self.plants[index] == None:
            return result
        result = self.plants[index]
        return result
    
    def replacePlant(self, oldPlant, newPlant):
        # no freeing should be going on here 
        oldPlantIndex = self.plants.IndexOf(oldPlant)
        self.plants.Remove(oldPlant)
        if oldPlantIndex >= 0:
            self.plants.Insert(oldPlantIndex, newPlant)
        else:
            self.plants.Add(newPlant)
        newPlant.previewCacheUpToDate = False
        # do the same for the selectedPlants list 
        oldPlantIndex = self.selectedPlants.IndexOf(oldPlant)
        if oldPlantIndex >= 0:
            self.selectedPlants.Remove(oldPlant)
            self.selectedPlants.Insert(oldPlantIndex, newPlant)
    
