# unit Uhints

from conversion_common import *
import umakeht
import uwinsliders
import utdoedit
import upicktdo
import uwizard
import usliders
import umain
import uppanel
import usupport
import ucollect
import delphi_compatability

# from utab2asp.pas - these are the component types that have hints
#type
#componentConstants = (TButton, TBitBtn, TSpeedButton,
#  TCheckBox, TRadioButton, TRadioGroup,
#  TListBox, TComboBox,
#  TEdit, TMemo,
#  TPanel, THeader, TGroupBox, TScrollBox,
#  TImage, TShape, TPaintBox,
#  TSpinEdit,
#  TTabSet,
#  KfWinSlider,
#  TDrawGrid,
#  PdTdoPaintBox);
#  
def makeAllFormComponentsHaveHints(aForm):
    i = 0L
    component = TComponent()
    
    if aForm.ComponentCount > 0:
        for i in range(0, aForm.ComponentCount):
            component = aForm.Components[i]
            if (component.__class__ is delphi_compatability.TButton) or (component.__class__ is delphi_compatability.TBitBtn) or (component.__class__ is delphi_compatability.TSpeedButton) or (component.__class__ is delphi_compatability.TCheckBox) or (component.__class__ is delphi_compatability.TRadioButton) or (component.__class__ is delphi_compatability.TRadioGroup) or (component.__class__ is delphi_compatability.TListBox) or (component.__class__ is delphi_compatability.TComboBox) or (component.__class__ is delphi_compatability.TEdit) or (component.__class__ is delphi_compatability.TMemo) or (component.__class__ is delphi_compatability.TPanel) or (component.__class__ is UNRESOLVED.THeader) or (component.__class__ is delphi_compatability.TGroupBox) or (component.__class__ is delphi_compatability.TScrollBox) or (component.__class__ is delphi_compatability.TImage) or (component.__class__ is delphi_compatability.TShape) or (component.__class__ is delphi_compatability.TPaintBox) or (component.__class__ is delphi_compatability.TSpinEdit) or (component.__class__ is UNRESOLVED.TTabSet) or (component.__class__ is uwinsliders.KfWinSlider) or (component.__class__ is delphi_compatability.TDrawGrid) or (component.__class__ is utdoedit.PdTdoPaintBox):
                delphi_compatability.TControl(component).ShowHint = true

class PdHint(TObject):
    def __init__(self):
        self.formClassName = ""
        self.componentName = ""
        self.shortHint = ""
        self.longHint = ""
    
    def make(self, aFormClassName, aComponentName, aShortHint, aLongHint):
        self.create
        self.formClassName = aFormClassName
        self.componentName = aComponentName
        self.shortHint = aShortHint
        self.longHint = aLongHint
        return self
    
class PdHintManager(TObject):
    def __init__(self):
        self.hints = TListCollection()
    
    # --------------------------------------------------------------------- PdHintManager 
    def create(self):
        self.hints = ucollect.TListCollection().Create()
        return self
    
    def destroy(self):
        self.hints.free
        self.hints = None
    
    def hintForComponentName(self, HintInfo, wantLongHint, showParameterHint):
        result = ""
        component = TComponent()
        owner = TComponent()
        parameterPanel = PdParameterPanel()
        
        result = ""
        if delphi_compatability.Application.terminated:
            return result
        if self.hints == None:
            return result
        owner = None
        component = delphi_compatability.TComponent(HintInfo.HintControl)
        if component == None:
            raise GeneralException.create("Problem: Nil component in method PdHintManager.hintForComponentName.")
        owner = component.Owner
        if owner == None:
            raise GeneralException.create("Problem: Component has nil owner in method PdHintManager.hintForComponentName.")
        # if parameter panel (or slider on it), show hint for parameter pointed to by panel 
        parameterPanel = None
        if (owner.__class__ is umain.TMainForm) and (component.__class__ is uppanel.PdParameterPanel):
            parameterPanel = component as uppanel.PdParameterPanel
        elif (owner.__class__ is uppanel.PdParameterPanel) and (component.__class__ is usliders.KfSlider):
            parameterPanel = usliders.KfSlider(component).Parent as uppanel.PdParameterPanel
        if parameterPanel != None:
            if parameterPanel.param != None:
                if not showParameterHint:
                    return result
                result = parameterPanel.param.getHint()
                result = self.cleanUpHint(HintInfo, result, true)
            return result
        if (owner.__class__ is uwizard.TWizardForm) and (component.__class__ is delphi_compatability.TDrawGrid):
            # show hints for tdos in wizard 
            result = uwizard.TWizardForm(owner).hintForTdosDrawGridAtPoint(component, HintInfo.CursorPos, HintInfo.CursorRect)
            result = self.cleanUpHint(HintInfo, result, false)
            return result
        if (owner.__class__ is upicktdo.TPickTdoForm) and (component.__class__ is delphi_compatability.TDrawGrid):
            # show hints for tdos in tdo chooser 
            result = upicktdo.TPickTdoForm(owner).hintForTdosDrawGridAtPoint(component, HintInfo.CursorPos, HintInfo.CursorRect)
            result = self.cleanUpHint(HintInfo, result, false)
            return result
        # otherwise look up non-parameter hint from hint list 
        result = self.quickSimpleHint(component, wantLongHint)
        if UNRESOLVED.copy(result, 1, 1) == "?":
            result = UNRESOLVED.copy(result, 2, len(result) - 1)
            result = self.referredHint(owner.className, result, wantLongHint)
        result = self.cleanUpHint(HintInfo, result, false)
        return result
    
    def quickSimpleHint(self, component, wantLongHint):
        result = ""
        i = 0L
        hint = PdHint()
        owner = TComponent()
        ownerClassName = ""
        
        result = ""
        owner = component.Owner
        if owner == None:
            raise GeneralException.create("Problem: Component has nil owner in method PdHintManager.quickSimpleHint.")
        if self.hints.Count > 0:
            for i in range(0, self.hints.Count):
                hint = PdHint(self.hints.Items[i])
                # check both form class and component name,
                #        so only components in one form need be uniquely named 
                ownerClassName = owner.className
                if (uppercase(hint.formClassName) == uppercase(ownerClassName)) and (uppercase(hint.componentName) == uppercase(component.Name)):
                    if wantLongHint:
                        result = hint.longHint
                    else:
                        result = hint.shortHint
                    if result == "(none)":
                        result = ""
                    break
        return result
    
    def referredHint(self, ownerName, componentName, wantLongHint):
        result = ""
        i = 0L
        hint = PdHint()
        
        result = ""
        if self.hints.Count > 0:
            for i in range(0, self.hints.Count):
                hint = PdHint(self.hints.Items[i])
                if (uppercase(hint.formClassName) == uppercase(ownerName)) and (uppercase(hint.componentName) == uppercase(componentName)):
                    if wantLongHint:
                        # check both form class and component name,
                        #        so only components in one form need be uniquely named 
                        result = hint.longHint
                    else:
                        result = hint.shortHint
                    if result == "(none)":
                        result = ""
                    break
        return result
    
    def cleanUpHint(self, HintInfo, hintStr, isParameterHint):
        if hintStr == "(none)":
            hintStr = ""
        # v2.0
        hintStr = usupport.trimQuotesFromFirstAndLast(hintStr)
        if isParameterHint:
            HintInfo.HintColor = delphi_compatability.clAqua
        return hintStr
    
    def makeHints(self):
        umakeht.CreateHints1(self)
        umakeht.CreateHints2(self)
    
    def clearHints(self):
        self.hints.clear()
    
    def addHint(self, aHint):
        if aHint != None:
            self.hints.Add(aHint)
    
