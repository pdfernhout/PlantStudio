# unit uborders

from conversion_common import *
import usupport
import updform
import udomain
import delphi_compatability

# const
kTransferLoad = 1
kTransferSave = 2

class TPrintBordersForm(PdForm):
    def __init__(self):
        self.Close = TButton()
        self.cancel = TButton()
        self.printBorderInner = TCheckBox()
        self.printBorderOuter = TCheckBox()
        self.printBorderColorInnerLabel = TLabel()
        self.printBorderColorInner = TPanel()
        self.printBorderColorOuter = TPanel()
        self.printBorderColorOuterLabel = TLabel()
        self.printBorderWidthInnerLabel = TLabel()
        self.printBorderWidthOuterLabel = TLabel()
        self.printBorderWidthInner = TSpinEdit()
        self.printBorderWidthOuter = TSpinEdit()
        self.helpButton = TSpeedButton()
        self.options = BitmapOptionsStructure()
        self.transferDirection = 0
        self.optionsChanged = false
    
    #$R *.DFM
    def initializeWithOptions(self, anOptions):
        self.options = anOptions
        self.transferDirection = kTransferLoad
        self.transferFields()
        # simple interaction, so just put it in here
        self.printBorderColorInner.Enabled = self.printBorderInner.Checked
        self.printBorderWidthInner.Enabled = self.printBorderInner.Checked
        self.printBorderColorInnerLabel.Enabled = self.printBorderInner.Checked
        self.printBorderWidthInnerLabel.Enabled = self.printBorderInner.Checked
        self.printBorderColorOuter.Enabled = self.printBorderOuter.Checked
        self.printBorderWidthOuter.Enabled = self.printBorderOuter.Checked
        self.printBorderColorOuterLabel.Enabled = self.printBorderOuter.Checked
        self.printBorderWidthOuterLabel.Enabled = self.printBorderOuter.Checked
    
    def transferFields(self):
        self.options.printBorderInner = self.transferCheckBox(self.printBorderInner, self.options.printBorderInner)
        self.options.printBorderOuter = self.transferCheckBox(self.printBorderOuter, self.options.printBorderOuter)
        self.transferColor(self.printBorderColorInner, self.options.printBorderColorInner)
        self.transferColor(self.printBorderColorOuter, self.options.printBorderColorOuter)
        self.options.printBorderWidthInner = self.transferSmallintSpinEditBox(self.printBorderWidthInner, self.options.printBorderWidthInner)
        self.options.printBorderWidthOuter = self.transferSmallintSpinEditBox(self.printBorderWidthOuter, self.options.printBorderWidthOuter)
    
    def transferCheckBox(self, checkBox, value):
        if self.transferDirection == kTransferLoad:
            checkBox.Checked = value
        elif self.transferDirection == kTransferSave:
            if value != checkBox.Checked:
                self.optionsChanged = true
            value = checkBox.Checked
        return value
    
    def transferColor(self, colorPanel, value):
        raise "method transferColor had assigned to var parameter value not added to return; fixup manually"
        if self.transferDirection == kTransferLoad:
            colorPanel.Color = value
        elif self.transferDirection == kTransferSave:
            if value != colorPanel.Color:
                self.optionsChanged = true
            value = colorPanel.Color
    
    def transferSmallintSpinEditBox(self, editBox, value):
        if self.transferDirection == kTransferLoad:
            editBox.Text = IntToStr(value)
        elif self.transferDirection == kTransferSave:
            if value != StrToIntDef(editBox.Text, 0):
                self.optionsChanged = true
            value = StrToIntDef(editBox.Text, 0)
        return value
    
    def printBorderColorInnerMouseUp(self, Sender, Button, Shift, X, Y):
        self.printBorderColorInner.Color = udomain.domain.getColorUsingCustomColors(self.printBorderColorInner.Color)
    
    def printBorderColorOuterMouseUp(self, Sender, Button, Shift, X, Y):
        self.printBorderColorOuter.Color = udomain.domain.getColorUsingCustomColors(self.printBorderColorOuter.Color)
    
    def printBorderInnerClick(self, Sender):
        self.printBorderColorInner.Enabled = self.printBorderInner.Checked
        self.printBorderWidthInner.Enabled = self.printBorderInner.Checked
        self.printBorderColorInnerLabel.Enabled = self.printBorderInner.Checked
        self.printBorderWidthInnerLabel.Enabled = self.printBorderInner.Checked
    
    def printBorderOuterClick(self, Sender):
        self.printBorderColorOuter.Enabled = self.printBorderOuter.Checked
        self.printBorderWidthOuter.Enabled = self.printBorderOuter.Checked
        self.printBorderColorOuterLabel.Enabled = self.printBorderOuter.Checked
        self.printBorderWidthOuterLabel.Enabled = self.printBorderOuter.Checked
    
    def CloseClick(self, Sender):
        self.transferDirection = kTransferSave
        self.transferFields()
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Drawing_a_print_border")
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
