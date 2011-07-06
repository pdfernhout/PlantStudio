// unit Uparams

from conversion_common import *;
import udomain;
import umakepm;
import uunits;
import usection;
import usupport;
import ucollect;
import delphi_compatability;

// const
kFieldUndefined = 0;
kFieldFloat = 1;
kFieldSmallint = 2;
kFieldColor = 3;
kFieldBoolean = 4;
kFieldThreeDObject = 5;
kFieldEnumeratedList = 6;
kFieldHeader = 7;
kFieldLongint = 8;
kIndexTypeUndefined = 0;
kIndexTypeNone = 1;
kIndexTypeSCurve = 3;
kTransferTypeUndefined = 0;
kTransferTypeMFD = 1;
kTransferTypeGetSetSCurve = 2;
kTransferTypeObject3D = 3;
kNotArray = -1;



// FieldType 
//note: the longint type is NOT for use for parameters (in param panels or breeding).
//     if you want to use a longint for a parameter, you have to
//     update the breeding method and the method that creates param panels. the smallint panel will not
//     work correctly with a longint as it is now (but you could subclass it if you need one).
// IndexType - for arrays 
// transferType - how data is transferred to and from model object 
//mfd is short for MoveFieldData
class PdParameter extends TObject {
    public short fieldNumber;
    public String fieldID;
    public String name;
    public short fieldType;
    public short indexType;
    public short unitSet;
    public short unitModel;
    public short unitMetric;
    public short unitEnglish;
    public float lowerBoundOriginal;
    public float upperBoundOriginal;
    public String defaultValueStringOriginal;
    public boolean cannotOverride;
    public boolean isOverridden;
    public float lowerBoundOverride;
    public float upperBoundOverride;
    public String defaultValueStringOverride;
    public boolean regrow;
    public boolean readOnly;
    public String accessString;
    public short transferType;
    public String hint;
    public boolean valueHasBeenReadForCurrentPlant;
    public boolean collapsed;
    public String originalSectionName;
    
    //must be whole string to allow for tdos
    // v2.1
    // ---------------------------------------------------------- PdParameter 
    public void create() {
        this.collapsed = true;
    }
    
    public void make(short aFieldNumber, String aFieldID, String aName, short aFieldType, short anIndexType, short aUnitSet, short aUnitModel, short aUnitMetric, short aUnitEnglish, float aLowerBound, float anUpperBound, String aDefaultValueString, boolean aRegrow, boolean aReadOnly, String anAccessString, short aTransferType, String aHint) {
        this.create();
        this.fieldNumber = aFieldNumber;
        this.fieldID = UNRESOLVED.copy(aFieldID, 1, 80);
        this.name = UNRESOLVED.copy(aName, 1, 80);
        this.fieldType = aFieldType;
        // v2.0 headers can have hints
        this.hint = aHint;
        if (this.fieldType == kFieldHeader) {
        }
        this.indexType = anIndexType;
        this.unitSet = aUnitSet;
        this.unitModel = aUnitModel;
        this.unitMetric = aUnitMetric;
        this.unitEnglish = aUnitEnglish;
        this.lowerBoundOriginal = aLowerBound;
        this.upperBoundOriginal = anUpperBound;
        this.defaultValueStringOriginal = aDefaultValueString;
        this.regrow = aRegrow;
        this.readOnly = aReadOnly;
        this.accessString = UNRESOLVED.copy(anAccessString, 1, 80);
        this.transferType = aTransferType;
        //hint := aHint;
    }
    
    public int indexCount() {
        result = 0;
        result = 1;
        switch (this.indexType) {
            case kIndexTypeUndefined:
                result = 1;
                break;
            case kIndexTypeNone:
                result = 1;
                break;
            case kIndexTypeSCurve:
                result = 4;
                break;
            default:
                throw new GeneralException.create("Problem: Unexpected index type in method PdParameter.indexCount.");
                break;
        return result;
    }
    
    public String getName() {
        result = "";
        result = this.name;
        return result;
    }
    
    public void setName(String newName) {
        this.name = UNRESOLVED.copy(newName, 1, 80);
    }
    
    public float lowerBound() {
        result = 0.0;
        if ((!this.cannotOverride) && (this.isOverridden)) {
            result = this.lowerBoundOverride;
        } else {
            result = this.lowerBoundOriginal;
        }
        return result;
    }
    
    public float upperBound() {
        result = 0.0;
        if ((!this.cannotOverride) && (this.isOverridden)) {
            result = this.upperBoundOverride;
        } else {
            result = this.upperBoundOriginal;
        }
        return result;
    }
    
    public String defaultValueString() {
        result = "";
        if ((!this.cannotOverride) && (this.isOverridden)) {
            result = this.defaultValueStringOverride;
        } else {
            result = this.defaultValueStringOriginal;
        }
        return result;
    }
    
    public String getHint() {
        result = "";
        result = this.hint;
        return result;
    }
    
}
class PdParameterManager extends TObject {
    public TListCollection parameters;
    
    // ---------------------------------------------------- PdParameterManager 
    public void create() {
        super.create();
        this.parameters = ucollect.TListCollection().Create();
    }
    
    public void destroy() {
        this.parameters.free;
        this.parameters = null;
        super.destroy();
    }
    
    public void addParameter(PdParameter newParameter) {
        if (newParameter != null) {
            this.parameters.Add(newParameter);
        }
    }
    
    public void addParameterForSection(String sectionName, String orthogonalSectionName, PdParameter newParameter) {
        PdSection section = new PdSection();
        
        section = null;
        section = udomain.domain.sectionManager.sectionForName(sectionName);
        if (section == null) {
            section = udomain.domain.sectionManager.addSection(sectionName);
            // the 'no section' section is hidden from the parameters window but we still want the section for writing out 
            section.showInParametersWindow = !(uppercase(sectionName) == uppercase("(no section)"));
        }
        this.addParameter(newParameter);
        if (section != null) {
            newParameter.originalSectionName = sectionName;
            section.addSectionItem(newParameter.fieldNumber);
        }
        // v2.1 orthogonal sections
        // limitation - each param can only have one orthogonal section specified
        // if want to add more later, use delimiter and parse
        orthogonalSectionName = trim(orthogonalSectionName);
        if (orthogonalSectionName != "") {
            section = null;
            section = udomain.domain.sectionManager.sectionForName(orthogonalSectionName);
            if (section == null) {
                section = udomain.domain.sectionManager.addOrthogonalSection(orthogonalSectionName);
                section.showInParametersWindow = true;
                section.isOrthogonal = true;
            }
            if (section != null) {
                section.addSectionItem(newParameter.fieldNumber);
            }
        }
    }
    
    public String fieldTypeName(int fieldType) {
        result = "";
        switch (fieldType) {
            case kFieldUndefined:
                result = "Undefined";
                break;
            case kFieldFloat:
                result = "Single";
                break;
            case kFieldSmallint:
                result = "Smallint";
                break;
            case kFieldColor:
                result = "Color";
                break;
            case kFieldBoolean:
                result = "Boolean";
                break;
            case kFieldThreeDObject:
                result = "3D object";
                break;
            case kFieldEnumeratedList:
                result = "List of choices";
                break;
            case kFieldLongint:
                result = "Longint";
                break;
            default:
                result = "not in list";
                break;
        return result;
    }
    
    public String indexTypeName(int indexType) {
        result = "";
        switch (indexType) {
            case kIndexTypeUndefined:
                result = "Undefined";
                break;
            case kIndexTypeNone:
                result = "None";
                break;
            case kIndexTypeSCurve:
                result = "S curve";
                break;
            default:
                result = "not in list";
                break;
        return result;
    }
    
    public PdParameter parameterForIndex(long index) {
        result = new PdParameter();
        result = this.parameters.Items[index];
        return result;
    }
    
    public void clearParameters() {
        this.parameters.clear();
    }
    
    public void setAllReadFlagsToFalse() {
        short i = 0;
        
        if (this.parameters.Count > 0) {
            for (i = 0; i <= this.parameters.Count - 1; i++) {
                PdParameter(this.parameters.Items[i]).valueHasBeenReadForCurrentPlant = false;
            }
        }
    }
    
    public PdParameter parameterForFieldNumber(long fieldNumber) {
        result = new PdParameter();
        short i = 0;
        PdParameter parameter = new PdParameter();
        
        result = null;
        if (this.parameters.Count > 0) {
            for (i = 0; i <= this.parameters.Count - 1; i++) {
                parameter = PdParameter(this.parameters.Items[i]);
                if (fieldNumber == parameter.fieldNumber) {
                    result = parameter;
                    return result;
                }
            }
        }
        throw new GeneralException.create("Problem: Parameter not found for field number " + IntToStr(fieldNumber) + " in method PdParameterManager.parameterForFieldNumber.");
        return result;
    }
    
    public PdParameter parameterForFieldID(String fieldID) {
        result = new PdParameter();
        short i = 0;
        PdParameter parameter = new PdParameter();
        
        result = null;
        if (this.parameters.Count > 0) {
            for (i = 0; i <= this.parameters.Count - 1; i++) {
                parameter = PdParameter(this.parameters.Items[i]);
                if (trim(uppercase(fieldID)) == trim(uppercase(parameter.fieldID))) {
                    result = parameter;
                    return result;
                }
            }
        }
        throw new GeneralException.create("Problem: Parameter not found for field ID " + fieldID + " in method PdParameterManager.parameterForFieldID.");
        return result;
    }
    
    public PdParameter parameterForName(String name) {
        result = new PdParameter();
        short i = 0;
        PdParameter parameter = new PdParameter();
        
        result = null;
        if (this.parameters.Count > 0) {
            for (i = 0; i <= this.parameters.Count - 1; i++) {
                parameter = PdParameter(this.parameters.Items[i]);
                if (trim(uppercase(name)) == trim(uppercase(parameter.name))) {
                    result = parameter;
                    return result;
                }
            }
        }
        throw new GeneralException.create("Problem: Parameter not found for name " + name + " in method PdParameterManager.parameterForName.");
        return result;
    }
    
    public int parameterIndexForFieldNumber(long fieldNumber) {
        result = 0;
        short i = 0;
        PdParameter parameter = new PdParameter();
        
        result = 0;
        if (this.parameters.Count > 0) {
            for (i = 0; i <= this.parameters.Count - 1; i++) {
                parameter = PdParameter(this.parameters.Items[i]);
                if (fieldNumber == parameter.fieldNumber) {
                    result = i;
                    return result;
                }
            }
        }
        throw new GeneralException.create("Problem: Parameter index not found for field number " + IntToStr(fieldNumber) + " in method PdParameterManager.parameterIndexForFieldNumber.");
        return result;
    }
    
    public int parameterIndexForFieldID(String fieldID) {
        result = 0;
        short i = 0;
        PdParameter parameter = new PdParameter();
        
        result = 0;
        if (this.parameters.Count > 0) {
            for (i = 0; i <= this.parameters.Count - 1; i++) {
                parameter = PdParameter(this.parameters.Items[i]);
                if (trim(uppercase(fieldID)) == trim(uppercase(parameter.fieldID))) {
                    result = i;
                    return result;
                }
            }
        }
        throw new GeneralException.create("Problem: Parameter index not found for field ID " + fieldID + " in method PdParameterManager.parameterIndexForFieldID.");
        return result;
    }
    
    public void makeParameters() {
        umakepm.CreateParameters(this);
        umakepm.CreateParameters_SecondHalf(this);
    }
    
}
