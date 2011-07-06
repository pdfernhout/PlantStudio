# unit ucustdrw

from conversion_common import *
import usupport
import udomain
import updform
import delphi_compatability

# const
kTransferLoad = 1
kTransferSave = 2

class TCustomDrawOptionsForm(PdForm):
    def __init__(self):
        self.helpButton = TSpeedButton()
        self.Close = TButton()
        self.cancel = TButton()
        self.GroupBox1 = TGroupBox()
        self.sortPolygons = TCheckBox()
        self.sortTdosAsOneItem = TCheckBox()
        self.GroupBox2 = TGroupBox()
        self.lineContrastIndexLabel = TLabel()
        self.fillPolygons = TCheckBox()
        self.drawLinesBetweenPolygons = TCheckBox()
        self.lineContrastIndex = TSpinEdit()
        self.GroupBox3 = TGroupBox()
        self.draw3DObjects = TCheckBox()
        self.drawStems = TCheckBox()
        self.draw3DObjectsAsBoundingRectsOnly = TCheckBox()
        self.options = DomainOptionsStructure()
        self.transferDirection = 0
        self.optionsChanged = false
    
    #$R *.DFM
    def FormActivate(self, Sender):
        self.transferDirection = kTransferLoad
        self.transferFields()
        # interactions
        self.drawLinesBetweenPolygons.Enabled = self.fillPolygons.Checked
        self.lineContrastIndex.Enabled = self.drawLinesBetweenPolygons.Enabled and self.drawLinesBetweenPolygons.Checked
        self.lineContrastIndexLabel.Enabled = self.lineContrastIndex.Enabled
        self.sortTdosAsOneItem.Enabled = self.sortPolygons.Checked
        self.draw3DObjectsAsBoundingRectsOnly.Enabled = self.draw3DObjects.Checked
    
    def CloseClick(self, Sender):
        self.transferDirection = kTransferSave
        self.transferFields()
        self.ModalResult = mrOK
    
    def cancelClick(self, Sender):
        self.ModalResult = mrCancel
    
    def transferFields(self):
        self.options.drawStems = self.transferCheckBox(self.drawStems, self.options.drawStems)
        self.options.draw3DObjects = self.transferCheckBox(self.draw3DObjects, self.options.draw3DObjects)
        self.options.draw3DObjectsAsBoundingRectsOnly = self.transferCheckBox(self.draw3DObjectsAsBoundingRectsOnly, self.options.draw3DObjectsAsBoundingRectsOnly)
        self.options.fillPolygons = self.transferCheckBox(self.fillPolygons, self.options.fillPolygons)
        self.options.drawLinesBetweenPolygons = self.transferCheckBox(self.drawLinesBetweenPolygons, self.options.drawLinesBetweenPolygons)
        self.options.lineContrastIndex = self.transferSmallintSpinEditBox(self.lineContrastIndex, self.options.lineContrastIndex)
        self.options.sortPolygons = self.transferCheckBox(self.sortPolygons, self.options.sortPolygons)
        self.options.sortTdosAsOneItem = self.transferCheckBox(self.sortTdosAsOneItem, self.options.sortTdosAsOneItem)
    
    def transferCheckBox(self, checkBox, value):
        if self.transferDirection == kTransferLoad:
            checkBox.Checked = value
        elif self.transferDirection == kTransferSave:
            if value != checkBox.Checked:
                self.optionsChanged = true
            value = checkBox.Checked
        return value
    
    def transferSmallintSpinEditBox(self, editBox, value):
        if self.transferDirection == kTransferLoad:
            editBox.Text = IntToStr(value)
        elif self.transferDirection == kTransferSave:
            if value != StrToIntDef(editBox.Text, 0):
                self.optionsChanged = true
            value = StrToIntDef(editBox.Text, 0)
        return value
    
    def draw3DObjectsClick(self, Sender):
        self.draw3DObjectsAsBoundingRectsOnly.Enabled = self.draw3DObjects.Checked
    
    def fillPolygonsClick(self, Sender):
        # and (not drawWithOpenGL.checked);
        self.drawLinesBetweenPolygons.Enabled = (self.fillPolygons.Checked)
        self.lineContrastIndex.Enabled = self.drawLinesBetweenPolygons.Enabled and self.drawLinesBetweenPolygons.Checked
        self.lineContrastIndexLabel.Enabled = self.lineContrastIndex.Enabled
    
    def drawLinesBetweenPolygonsClick(self, Sender):
        self.lineContrastIndex.Enabled = self.drawLinesBetweenPolygons.Enabled and self.drawLinesBetweenPolygons.Checked
        self.lineContrastIndexLabel.Enabled = self.lineContrastIndex.Enabled
    
    def sortPolygonsClick(self, Sender):
        self.sortTdosAsOneItem.Enabled = self.sortPolygons.Checked
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Changing_the_drawing_speed")
    
    def FormKeyPress(self, Sender, Key):
        Key = usupport.makeEnterWorkAsTab(self, self.ActiveControl, Key)
        return Key
    
#
#procedure TOptionsForm.drawWithOpenGLClick(Sender: TObject);
#  begin
#  //drawLinesBetweenPolygons.enabled := (fillPolygons.checked) and (not drawWithOpenGL.checked);
#  //sortPolygons.enabled := not drawWithOpenGL.checked;
#  end;
#
