# unit Uparams

from conversion_common import *
import udomain
import umakepm
import uunits
import usection
import usupport
import uexcept
import ucollect
import delphi_compatability

# const
kFieldUndefined = 0
kFieldFloat = 1
kFieldSmallint = 2
kFieldColor = 3
kFieldBoolean = 4
kFieldThreeDObject = 5
kFieldEnumeratedList = 6
kFieldHeader = 7
kFieldLongint = 8
kIndexTypeUndefined = 0
kIndexTypeNone = 1
kIndexTypeSCurve = 3
kTransferTypeUndefined = 0
kTransferTypeMFD = 1
kTransferTypeGetSetSCurve = 2
kTransferTypeObject3D = 3
kNotArray = -1

# FieldType 
#note: the longint type is NOT for use for parameters (in param panels or breeding).
#     if you want to use a longint for a parameter, you have to
#     update the breeding method and the method that creates param panels. the smallint panel will not
#     work correctly with a longint as it is now (but you could subclass it if you need one).
# IndexType - for arrays 
# transferType - how data is transferred to and from model object 
#mfd is short for MoveFieldData
class PdParameter(TObject):
    def __init__(self):
        self.fieldNumber = 0
        self.fieldID = ""
        self.name = ""
        self.fieldType = 0
        self.indexType = 0
        self.unitSet = 0
        self.unitModel = 0
        self.unitMetric = 0
        self.unitEnglish = 0
        self.lowerBoundOriginal = 0.0
        self.upperBoundOriginal = 0.0
        self.defaultValueStringOriginal = ""
        self.cannotOverride = false
        self.isOverridden = false
        self.lowerBoundOverride = 0.0
        self.upperBoundOverride = 0.0
        self.defaultValueStringOverride = ""
        self.regrow = false
        self.readOnly = false
        self.accessString = ""
        self.transferType = 0
        self.hint = ""
        self.valueHasBeenReadForCurrentPlant = false
        self.collapsed = false
        self.originalSectionName = ""
    
    #must be whole string to allow for tdos
    # v2.1
    # ---------------------------------------------------------- PdParameter 
    def create(self):
        self.collapsed = true
        return self
    
    def make(self, aFieldNumber, aFieldID, aName, aFieldType, anIndexType, aUnitSet, aUnitModel, aUnitMetric, aUnitEnglish, aLowerBound, anUpperBound, aDefaultValueString, aRegrow, aReadOnly, anAccessString, aTransferType, aHint):
        self.create()
        self.fieldNumber = aFieldNumber
        self.fieldID = UNRESOLVED.copy(aFieldID, 1, 80)
        self.name = UNRESOLVED.copy(aName, 1, 80)
        self.fieldType = aFieldType
        # v2.0 headers can have hints
        self.hint = aHint
        if self.fieldType == kFieldHeader:
            return self
        self.indexType = anIndexType
        self.unitSet = aUnitSet
        self.unitModel = aUnitModel
        self.unitMetric = aUnitMetric
        self.unitEnglish = aUnitEnglish
        self.lowerBoundOriginal = aLowerBound
        self.upperBoundOriginal = anUpperBound
        self.defaultValueStringOriginal = aDefaultValueString
        self.regrow = aRegrow
        self.readOnly = aReadOnly
        self.accessString = UNRESOLVED.copy(anAccessString, 1, 80)
        self.transferType = aTransferType
        #hint := aHint;
        return self
    
    def indexCount(self):
        result = 0
        result = 1
        if self.indexType == kIndexTypeUndefined:
            result = 1
        elif self.indexType == kIndexTypeNone:
            result = 1
        elif self.indexType == kIndexTypeSCurve:
            result = 4
        else :
            raise GeneralException.create("Problem: Unexpected index type in method PdParameter.indexCount.")
        return result
    
    def getName(self):
        result = ""
        result = self.name
        return result
    
    def setName(self, newName):
        self.name = UNRESOLVED.copy(newName, 1, 80)
    
    def lowerBound(self):
        result = 0.0
        if (not self.cannotOverride) and (self.isOverridden):
            result = self.lowerBoundOverride
        else:
            result = self.lowerBoundOriginal
        return result
    
    def upperBound(self):
        result = 0.0
        if (not self.cannotOverride) and (self.isOverridden):
            result = self.upperBoundOverride
        else:
            result = self.upperBoundOriginal
        return result
    
    def defaultValueString(self):
        result = ""
        if (not self.cannotOverride) and (self.isOverridden):
            result = self.defaultValueStringOverride
        else:
            result = self.defaultValueStringOriginal
        return result
    
    def getHint(self):
        result = ""
        result = self.hint
        return result
    
class PdParameterManager(TObject):
    def __init__(self):
        self.parameters = TListCollection()
    
    # ---------------------------------------------------- PdParameterManager 
    def create(self):
        TObject.create(self)
        self.parameters = ucollect.TListCollection().Create()
        return self
    
    def destroy(self):
        self.parameters.free
        self.parameters = None
        TObject.destroy(self)
    
    def addParameter(self, newParameter):
        if newParameter != None:
            self.parameters.Add(newParameter)
    
    def addParameterForSection(self, sectionName, orthogonalSectionName, newParameter):
        section = PdSection()
        
        section = None
        section = udomain.domain.sectionManager.sectionForName(sectionName)
        if section == None:
            section = udomain.domain.sectionManager.addSection(sectionName)
            # the 'no section' section is hidden from the parameters window but we still want the section for writing out 
            section.showInParametersWindow = not (uppercase(sectionName) == uppercase("(no section)"))
        self.addParameter(newParameter)
        if section != None:
            newParameter.originalSectionName = sectionName
            section.addSectionItem(newParameter.fieldNumber)
        # v2.1 orthogonal sections
        # limitation - each param can only have one orthogonal section specified
        # if want to add more later, use delimiter and parse
        orthogonalSectionName = trim(orthogonalSectionName)
        if orthogonalSectionName != "":
            section = None
            section = udomain.domain.sectionManager.sectionForName(orthogonalSectionName)
            if section == None:
                section = udomain.domain.sectionManager.addOrthogonalSection(orthogonalSectionName)
                section.showInParametersWindow = true
                section.isOrthogonal = true
            if section != None:
                section.addSectionItem(newParameter.fieldNumber)
    
    def fieldTypeName(self, fieldType):
        result = ""
        if fieldType == kFieldUndefined:
            result = "Undefined"
        elif fieldType == kFieldFloat:
            result = "Single"
        elif fieldType == kFieldSmallint:
            result = "Smallint"
        elif fieldType == kFieldColor:
            result = "Color"
        elif fieldType == kFieldBoolean:
            result = "Boolean"
        elif fieldType == kFieldThreeDObject:
            result = "3D object"
        elif fieldType == kFieldEnumeratedList:
            result = "List of choices"
        elif fieldType == kFieldLongint:
            result = "Longint"
        else :
            result = "not in list"
        return result
    
    def indexTypeName(self, indexType):
        result = ""
        if indexType == kIndexTypeUndefined:
            result = "Undefined"
        elif indexType == kIndexTypeNone:
            result = "None"
        elif indexType == kIndexTypeSCurve:
            result = "S curve"
        else :
            result = "not in list"
        return result
    
    def parameterForIndex(self, index):
        result = PdParameter()
        result = self.parameters.Items[index]
        return result
    
    def clearParameters(self):
        self.parameters.clear()
    
    def setAllReadFlagsToFalse(self):
        i = 0
        
        if self.parameters.Count > 0:
            for i in range(0, self.parameters.Count):
                PdParameter(self.parameters.Items[i]).valueHasBeenReadForCurrentPlant = false
    
    def parameterForFieldNumber(self, fieldNumber):
        result = PdParameter()
        i = 0
        parameter = PdParameter()
        
        result = None
        if self.parameters.Count > 0:
            for i in range(0, self.parameters.Count):
                parameter = PdParameter(self.parameters.Items[i])
                if fieldNumber == parameter.fieldNumber:
                    result = parameter
                    return result
        raise GeneralException.create("Problem: Parameter not found for field number " + IntToStr(fieldNumber) + " in method PdParameterManager.parameterForFieldNumber.")
        return result
    
    def parameterForFieldID(self, fieldID):
        result = PdParameter()
        i = 0
        parameter = PdParameter()
        
        result = None
        if self.parameters.Count > 0:
            for i in range(0, self.parameters.Count):
                parameter = PdParameter(self.parameters.Items[i])
                if trim(uppercase(fieldID)) == trim(uppercase(parameter.fieldID)):
                    result = parameter
                    return result
        raise GeneralException.create("Problem: Parameter not found for field ID " + fieldID + " in method PdParameterManager.parameterForFieldID.")
        return result
    
    def parameterForName(self, name):
        result = PdParameter()
        i = 0
        parameter = PdParameter()
        
        result = None
        if self.parameters.Count > 0:
            for i in range(0, self.parameters.Count):
                parameter = PdParameter(self.parameters.Items[i])
                if trim(uppercase(name)) == trim(uppercase(parameter.name)):
                    result = parameter
                    return result
        raise GeneralException.create("Problem: Parameter not found for name " + name + " in method PdParameterManager.parameterForName.")
        return result
    
    def parameterIndexForFieldNumber(self, fieldNumber):
        result = 0
        i = 0
        parameter = PdParameter()
        
        result = 0
        if self.parameters.Count > 0:
            for i in range(0, self.parameters.Count):
                parameter = PdParameter(self.parameters.Items[i])
                if fieldNumber == parameter.fieldNumber:
                    result = i
                    return result
        raise GeneralException.create("Problem: Parameter index not found for field number " + IntToStr(fieldNumber) + " in method PdParameterManager.parameterIndexForFieldNumber.")
        return result
    
    def parameterIndexForFieldID(self, fieldID):
        result = 0
        i = 0
        parameter = PdParameter()
        
        result = 0
        if self.parameters.Count > 0:
            for i in range(0, self.parameters.Count):
                parameter = PdParameter(self.parameters.Items[i])
                if trim(uppercase(fieldID)) == trim(uppercase(parameter.fieldID)):
                    result = i
                    return result
        raise GeneralException.create("Problem: Parameter index not found for field ID " + fieldID + " in method PdParameterManager.parameterIndexForFieldID.")
        return result
    
    def makeParameters(self):
        umakepm.CreateParameters(self)
        umakepm.CreateParameters_SecondHalf(self)
    
