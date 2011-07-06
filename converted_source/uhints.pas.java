// unit Uhints

from conversion_common import *;
import umakeht;
import uwinsliders;
import utdoedit;
import upicktdo;
import usliders;
import uppanel;
import delphi_compatability;

// from utab2asp.pas - these are the component types that have hints
//type
//componentConstants = (TButton, TBitBtn, TSpeedButton,
//  TCheckBox, TRadioButton, TRadioGroup,
//  TListBox, TComboBox,
//  TEdit, TMemo,
//  TPanel, THeader, TGroupBox, TScrollBox,
//  TImage, TShape, TPaintBox,
//  TSpinEdit,
//  TTabSet,
//  KfWinSlider,
//  TDrawGrid,
//  PdTdoPaintBox);
//  
public void makeAllFormComponentsHaveHints(TForm aForm) {
    long i = 0;
    TComponent component = new TComponent();
    
    if (aForm.ComponentCount > 0) {
        for (i = 0; i <= aForm.ComponentCount - 1; i++) {
            component = aForm.Components[i];
            if ((component instanceof delphi_compatability.TButton) || (component instanceof delphi_compatability.TBitBtn) || (component instanceof delphi_compatability.TSpeedButton) || (component instanceof delphi_compatability.TCheckBox) || (component instanceof delphi_compatability.TRadioButton) || (component instanceof delphi_compatability.TRadioGroup) || (component instanceof delphi_compatability.TListBox) || (component instanceof delphi_compatability.TComboBox) || (component instanceof delphi_compatability.TEdit) || (component instanceof delphi_compatability.TMemo) || (component instanceof delphi_compatability.TPanel) || (component instanceof UNRESOLVED.THeader) || (component instanceof delphi_compatability.TGroupBox) || (component instanceof delphi_compatability.TScrollBox) || (component instanceof delphi_compatability.TImage) || (component instanceof delphi_compatability.TShape) || (component instanceof delphi_compatability.TPaintBox) || (component instanceof delphi_compatability.TSpinEdit) || (component instanceof UNRESOLVED.TTabSet) || (component instanceof uwinsliders.KfWinSlider) || (component instanceof delphi_compatability.TDrawGrid) || (component instanceof utdoedit.PdTdoPaintBox)) {
                delphi_compatability.TControl(component).ShowHint = true;
            }
        }
    }
}


class PdHint extends TObject {
    public String formClassName;
    public String componentName;
    public String shortHint;
    public String longHint;
    
    public void make(String aFormClassName, String aComponentName, String aShortHint, String aLongHint) {
        this.create;
        this.formClassName = aFormClassName;
        this.componentName = aComponentName;
        this.shortHint = aShortHint;
        this.longHint = aLongHint;
    }
    
}
class PdHintManager extends TObject {
    public TListCollection hints;
    
    // --------------------------------------------------------------------- PdHintManager 
    public void create() {
        this.hints = UNRESOLVED.TListCollection.create;
    }
    
    public void destroy() {
        this.hints.free;
        this.hints = null;
    }
    
    public String hintForComponentName(THintInfo HintInfo, boolean wantLongHint, boolean showParameterHint) {
        result = "";
        TComponent component = new TComponent();
        TComponent owner = new TComponent();
        PdParameterPanel parameterPanel = new PdParameterPanel();
        
        result = "";
        if (delphi_compatability.Application.terminated) {
            return result;
        }
        if (this.hints == null) {
            return result;
        }
        owner = null;
        component = delphi_compatability.TComponent(HintInfo.HintControl);
        if (component == null) {
            throw new GeneralException.create("Problem: Nil component in method PdHintManager.hintForComponentName.");
        }
        owner = component.Owner;
        if (owner == null) {
            throw new GeneralException.create("Problem: Component has nil owner in method PdHintManager.hintForComponentName.");
        }
        // if parameter panel (or slider on it), show hint for parameter pointed to by panel 
        parameterPanel = null;
        if ((owner instanceof UNRESOLVED.TMainForm) && (component instanceof uppanel.PdParameterPanel)) {
            parameterPanel = (uppanel.PdParameterPanel)component;
        } else if ((owner instanceof uppanel.PdParameterPanel) && (component instanceof usliders.KfSlider)) {
            parameterPanel = (uppanel.PdParameterPanel)usliders.KfSlider(component).Parent;
        }
        if (parameterPanel != null) {
            if (parameterPanel.param != null) {
                if (!showParameterHint) {
                    return result;
                }
                result = parameterPanel.param.getHint;
                result = this.cleanUpHint(HintInfo, result, true);
            }
            return result;
        }
        if ((owner instanceof UNRESOLVED.TWizardForm) && (component instanceof delphi_compatability.TDrawGrid)) {
            // show hints for tdos in wizard 
            result = UNRESOLVED.TWizardForm(owner).hintForTdosDrawGridAtPoint(component, HintInfo.CursorPos, HintInfo.CursorRect);
            result = this.cleanUpHint(HintInfo, result, false);
            return result;
        }
        if ((owner instanceof upicktdo.TPickTdoForm) && (component instanceof delphi_compatability.TDrawGrid)) {
            // show hints for tdos in tdo chooser 
            result = upicktdo.TPickTdoForm(owner).hintForTdosDrawGridAtPoint(component, HintInfo.CursorPos, HintInfo.CursorRect);
            result = this.cleanUpHint(HintInfo, result, false);
            return result;
        }
        // otherwise look up non-parameter hint from hint list 
        result = this.quickSimpleHint(component, wantLongHint);
        if (UNRESOLVED.copy(result, 1, 1) == "?") {
            result = UNRESOLVED.copy(result, 2, len(result) - 1);
            result = this.referredHint(owner.className, result, wantLongHint);
        }
        result = this.cleanUpHint(HintInfo, result, false);
        return result;
    }
    
    public String quickSimpleHint(TComponent component, boolean wantLongHint) {
        result = "";
        long i = 0;
        PdHint hint = new PdHint();
        TComponent owner = new TComponent();
        String ownerClassName = "";
        
        result = "";
        owner = component.Owner;
        if (owner == null) {
            throw new GeneralException.create("Problem: Component has nil owner in method PdHintManager.quickSimpleHint.");
        }
        if (this.hints.count > 0) {
            for (i = 0; i <= this.hints.count - 1; i++) {
                hint = PdHint(this.hints.items[i]);
                // check both form class and component name,
                //        so only components in one form need be uniquely named 
                ownerClassName = owner.className;
                if ((uppercase(hint.formClassName) == uppercase(ownerClassName)) && (uppercase(hint.componentName) == uppercase(component.Name))) {
                    if (wantLongHint) {
                        result = hint.longHint;
                    } else {
                        result = hint.shortHint;
                    }
                    if (result == "(none)") {
                        result = "";
                    }
                    break;
                }
            }
        }
        return result;
    }
    
    public String referredHint(String ownerName, String componentName, boolean wantLongHint) {
        result = "";
        long i = 0;
        PdHint hint = new PdHint();
        
        result = "";
        if (this.hints.count > 0) {
            for (i = 0; i <= this.hints.count - 1; i++) {
                hint = PdHint(this.hints.items[i]);
                if ((uppercase(hint.formClassName) == uppercase(ownerName)) && (uppercase(hint.componentName) == uppercase(componentName))) {
                    if (wantLongHint) {
                        // check both form class and component name,
                        //        so only components in one form need be uniquely named 
                        result = hint.longHint;
                    } else {
                        result = hint.shortHint;
                    }
                    if (result == "(none)") {
                        result = "";
                    }
                    break;
                }
            }
        }
        return result;
    }
    
    public void cleanUpHint(THintInfo HintInfo, String hintStr, boolean isParameterHint) {
        if (hintStr == "(none)") {
            hintStr = "";
        }
        // v2.0
        hintStr = UNRESOLVED.trimQuotesFromFirstAndLast(hintStr);
        if (isParameterHint) {
            HintInfo.HintColor = delphi_compatability.clAqua;
        }
        return hintStr;
    }
    
    public void makeHints() {
        umakeht.CreateHints1(this);
        umakeht.CreateHints2(this);
    }
    
    public void clearHints() {
        this.hints.clear;
    }
    
    public void addHint(PdHint aHint) {
        if (aHint != null) {
            this.hints.add(aHint);
        }
    }
    
}
