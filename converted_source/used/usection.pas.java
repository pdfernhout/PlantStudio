// unit Usection

from conversion_common import *;
import udomain;
import uparams;
import ucollect;
import delphi_compatability;

// const
kMaxSectionItems = 200;



// v2.0 increased
class PdSection extends TObject {
    public short numSectionItems;
    public  sectionItems;
    public String name;
    public boolean showInParametersWindow;
    public boolean expanded;
    public boolean isOrthogonal;
    
    // v2.1
    // ----------------------------------------------------------------- PdSection 
    public void addSectionItem(short newSectionItem) {
        this.numSectionItems += 1;
        this.sectionItems[this.numSectionItems - 1] = newSectionItem;
    }
    
    public String getName() {
        result = "";
        result = this.name;
        return result;
    }
    
    public void setName(String newName) {
        this.name = newName;
    }
    
}
class PdSectionManager extends TObject {
    public TListCollection sections;
    public TListCollection orthogonalSections;
    
    // ----------------------------------------------------------------- PdSectionManager 
    public void create() {
        super.create();
        this.sections = ucollect.TListCollection().Create();
        // v2.1
        this.orthogonalSections = ucollect.TListCollection().Create();
    }
    
    public void destroy() {
        this.sections.free;
        this.sections = null;
        // v2.1
        this.orthogonalSections.free;
        this.orthogonalSections = null;
        super.destroy();
    }
    
    public PdSection addSection(String aName) {
        result = new PdSection();
        PdSection section = new PdSection();
        
        section = PdSection.create;
        section.name = aName;
        this.sections.Add(section);
        result = section;
        return result;
    }
    
    // v2.1
    public PdSection addOrthogonalSection(String aName) {
        result = new PdSection();
        PdSection section = new PdSection();
        short i = 0;
        
        section = PdSection.create;
        section.name = aName;
        this.orthogonalSections.Add(section);
        // put in one header param so they can easily open and close all the items
        //header type
        udomain.domain.parameterManager.addParameterForSection(section.name, "", uparams.PdParameter().make(1000 + this.orthogonalSections.Count, "header", section.name, 7, 0, 0, 0, 0, 0, 0.00000000, 0.00000000, "", false, false, "", 0, "These parameters can also be found in other (main) sections, but you may want to look at together here."));
        result = section;
        return result;
    }
    
    public PdSection sectionForName(String aName) {
        result = new PdSection();
        short i = 0;
        PdSection section = new PdSection();
        
        result = null;
        if (this.sections.Count > 0) {
            for (i = 0; i <= this.sections.Count - 1; i++) {
                section = PdSection(this.sections.Items[i]);
                if (aName == section.name) {
                    result = section;
                    return result;
                }
            }
        }
        if (this.orthogonalSections.Count > 0) {
            for (i = 0; i <= this.orthogonalSections.Count - 1; i++) {
                // v2.1
                section = PdSection(this.orthogonalSections.Items[i]);
                if (aName == section.name) {
                    result = section;
                    return result;
                }
            }
        }
        return result;
    }
    
    // v2.1 override changed to use section and parameter name
    public PdParameter parameterForSectionAndName(String aSectionName, String aParameterName) {
        result = new PdParameter();
        short i = 0;
        short j = 0;
        short fieldNumber = 0;
        PdSection section = new PdSection();
        PdParameter parameter = new PdParameter();
        
        result = null;
        if (aSectionName == "") {
            // a stab at backward compatibility - if no section name, try to find param anyway
            parameter = null;
            parameter = udomain.domain.parameterManager.parameterForName(aParameterName);
            if (parameter != null) {
                result = parameter;
                return result;
            }
        } else if (this.sections.Count > 0) {
            for (i = 0; i <= this.sections.Count - 1; i++) {
                section = PdSection(this.sections.Items[i]);
                if (aSectionName == section.name) {
                    for (j = 0; j <= section.numSectionItems - 1; j++) {
                        fieldNumber = section.sectionItems[j];
                        parameter = null;
                        parameter = udomain.domain.parameterManager.parameterForFieldNumber(fieldNumber);
                        if ((parameter != null) && (parameter.name == aParameterName)) {
                            result = parameter;
                            return result;
                        }
                    }
                }
            }
        }
        return result;
    }
    
}
