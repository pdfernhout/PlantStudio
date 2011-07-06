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
class PdSection(TObject):
    def __init__(self):
        self.numSectionItems = 0
        self.sectionItems = [0] * (range(0, kMaxSectionItems + 1) + 1)
        self.name = ""
        self.showInParametersWindow = false
        self.expanded = false
        self.isOrthogonal = false
    
    # v2.1
    # ----------------------------------------------------------------- PdSection 
    def addSectionItem(self, newSectionItem):
        self.numSectionItems += 1
        self.sectionItems[self.numSectionItems - 1] = newSectionItem
    
    def getName(self):
        result = ""
        result = self.name
        return result
    
    def setName(self, newName):
        self.name = newName
    
class PdSectionManager(TObject):
    def __init__(self):
        self.sections = TListCollection()
        self.orthogonalSections = TListCollection()
    
    # ----------------------------------------------------------------- PdSectionManager 
    def create(self):
        TObject.create(self)
        self.sections = ucollect.TListCollection().Create()
        # v2.1
        self.orthogonalSections = ucollect.TListCollection().Create()
        return self
    
    def destroy(self):
        self.sections.free
        self.sections = None
        # v2.1
        self.orthogonalSections.free
        self.orthogonalSections = None
        TObject.destroy(self)
    
    def addSection(self, aName):
        result = PdSection()
        section = PdSection()
        
        section = PdSection.create
        section.name = aName
        self.sections.Add(section)
        result = section
        return result
    
    # v2.1
    def addOrthogonalSection(self, aName):
        result = PdSection()
        section = PdSection()
        i = 0
        
        section = PdSection.create
        section.name = aName
        self.orthogonalSections.Add(section)
        # put in one header param so they can easily open and close all the items
        #header type
        udomain.domain.parameterManager.addParameterForSection(section.name, "", uparams.PdParameter().make(1000 + self.orthogonalSections.Count, "header", section.name, 7, 0, 0, 0, 0, 0, 0.00000000, 0.00000000, "", false, false, "", 0, "These parameters can also be found in other (main) sections, but you may want to look at together here."))
        result = section
        return result
    
    def sectionForName(self, aName):
        result = PdSection()
        i = 0
        section = PdSection()
        
        result = None
        if self.sections.Count > 0:
            for i in range(0, self.sections.Count):
                section = PdSection(self.sections.Items[i])
                if aName == section.name:
                    result = section
                    return result
        if self.orthogonalSections.Count > 0:
            for i in range(0, self.orthogonalSections.Count):
                # v2.1
                section = PdSection(self.orthogonalSections.Items[i])
                if aName == section.name:
                    result = section
                    return result
        return result
    
    # v2.1 override changed to use section and parameter name
    def parameterForSectionAndName(self, aSectionName, aParameterName):
        result = PdParameter()
        i = 0
        j = 0
        fieldNumber = 0
        section = PdSection()
        parameter = PdParameter()
        
        result = None
        if aSectionName == "":
            # a stab at backward compatibility - if no section name, try to find param anyway
            parameter = None
            parameter = udomain.domain.parameterManager.parameterForName(aParameterName)
            if parameter != None:
                result = parameter
                return result
        elif self.sections.Count > 0:
            for i in range(0, self.sections.Count):
                section = PdSection(self.sections.Items[i])
                if aSectionName == section.name:
                    for j in range(0, section.numSectionItems):
                        fieldNumber = section.sectionItems[j]
                        parameter = None
                        parameter = udomain.domain.parameterManager.parameterForFieldNumber(fieldNumber)
                        if (parameter != None) and (parameter.name == aParameterName):
                            result = parameter
                            return result
        return result
    
