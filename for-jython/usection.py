# unit Usection

from conversion_common import *
import udebug
import udomain
import uparams
import ucollect
import delphi_compatability

# const
kMaxSectionItems = 200

# v2.0 increased
# v2.1
# ----------------------------------------------------------------- PdSection 
class PdSection:
    def __init__(self):
        self.numSectionItems = 0
        self.sectionItems = [0] * (kMaxSectionItems + 1)
        self.name = ""
        self.showInParametersWindow = False
        self.expanded = False
        self.isOrthogonal = False

    def addSectionItem(self, newSectionItem):
        self.numSectionItems += 1
        self.sectionItems[self.numSectionItems - 1] = newSectionItem
    
    def getName(self):
        result = ""
        result = self.name
        return result
    
    def setName(self, newName):
        self.name = newName
 
# ----------------------------------------------------------------- PdSectionManager    
class PdSectionManager:
    def __init__(self):
        self.sections = ucollect.TListCollection()
        # v2.1
        self.orthogonalSections = ucollect.TListCollection()
    
    def addSection(self, aName):
        section = PdSection()
        section.name = aName
        self.sections.Add(section)
        result = section
        return result
    
    # v2.1
    def addOrthogonalSection(self, aName):
        section = PdSection()
        section.name = aName
        self.orthogonalSections.Add(section)
        # put in one header param so they can easily open and close all the items
        #header type
        udomain.domain.parameterManager.addParameterForSection(section.name, "", uparams.PdParameter().make(1000 + len(self.orthogonalSections), "header", section.name, 7, 0, 0, 0, 0, 0, 0.00000000, 0.00000000, "", False, False, "", 0, "These parameters can also be found in other (main) sections, but you may want to look at together here."))
        result = section
        return result
    
    def sectionForName(self, aName):
        result = None
        for section in self.sections:
            if aName == section.name:
                result = section
                return result
        for section in self.orthogonalSections:
            # v2.1
            if aName == section.name:
                result = section
                return result
        return result
    
    # v2.1 override changed to use section and parameter name
    def parameterForSectionAndName(self, aSectionName, aParameterName):
        result = None
        if aSectionName == "":
            # a stab at backward compatibility - if no section name, try to find param anyway
            parameter = udomain.domain.parameterManager.parameterForName(aParameterName)
            if parameter != None:
                result = parameter
                return result
        else:
            for section in self.sections:
                if aSectionName == section.name:
                    for j in range(0, section.numSectionItems):
                        fieldNumber = section.sectionItems[j]
                        parameter = udomain.domain.parameterManager.parameterForFieldNumber(fieldNumber)
                        if (parameter != None) and (parameter.name == aParameterName):
                            result = parameter
                            return result
        return result
    
