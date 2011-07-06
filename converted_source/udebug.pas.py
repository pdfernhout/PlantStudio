# unit Udebug

from conversion_common import *
import umain
import uprginfo
import umath
import usupport
import udomain
import updform
import delphi_compatability

# var
DebugForm = TDebugForm()

#$R *.DFM
def DebugPrint(aMessage):
    if DebugForm != None:
        DebugForm.print(aMessage)

# const
kBetweenGap = 4

class TDebugForm(PdForm):
    def __init__(self):
        self.DebugList = TListBox()
        self.Close = TButton()
        self.saveListAs = TButton()
        self.clearList = TButton()
        self.optionsPanel = TPanel()
        self.exceptionLabel = TLabel()
        self.showOnExceptionCheckBox = TCheckBox()
        self.logToFile = TCheckBox()
        self.helpButton = TSpeedButton()
        self.supportButton = TButton()
        self.outputFile = TextFile()
        self.logging = false
    
    def FormCreate(self, Sender):
        tempBoundsRect = TRect()
        
        # keep window on screen - left corner of title bar 
        tempBoundsRect = udomain.domain.debugWindowRect
        if (tempBoundsRect.Left != 0) or (tempBoundsRect.Right != 0) or (tempBoundsRect.Top != 0) or (tempBoundsRect.Bottom != 0):
            if tempBoundsRect.Left > delphi_compatability.Screen.Width - umain.kMinWidthOnScreen:
                tempBoundsRect.Left = delphi_compatability.Screen.Width - umain.kMinWidthOnScreen
            if tempBoundsRect.Top > delphi_compatability.Screen.Height - umain.kMinHeightOnScreen:
                tempBoundsRect.Top = delphi_compatability.Screen.Height - umain.kMinHeightOnScreen
            self.SetBounds(tempBoundsRect.Left, tempBoundsRect.Top, tempBoundsRect.Right, tempBoundsRect.Bottom)
        self.showOnExceptionCheckBox.Checked = udomain.domain.options.showWindowOnException
        self.logToFile.Checked = udomain.domain.options.logToFileOnException
        # this will make the list box create a horizontal scroll bar 
        UNRESOLVED.sendMessage(self.DebugList.Handle, UNRESOLVED.LB_SETHORIZONTALEXTENT, 1000, 0)
    
    def FormDestroy(self, Sender):
        self.stopLogging()
    
    def startLogging(self, fileName):
        dateString = ""
        
        if self.logging:
            return
        AssignFile(self.outputFile, fileName)
        if not FileExists(fileName):
            # v1.5
            usupport.setDecimalSeparator()
            Rewrite(self.outputFile)
        else:
            # v1.5
            usupport.setDecimalSeparator()
            UNRESOLVED.append(self.outputFile)
            dateString = UNRESOLVED.formatDateTime("m/d/yyyy, h:m am/pm", UNRESOLVED.now)
            writeln(self.outputFile, "---- log start (" + dateString + ") ----")
        self.logging = true
    
    def stopLogging(self):
        if not self.logging:
            return
        writeln(self.outputFile, "---- log stop ----")
        CloseFile(self.outputFile)
        self.logging = false
    
    def saveExceptionListToFile(self, fileName):
        i = 0L
        
        AssignFile(self.outputFile, fileName)
        # v1.5
        usupport.setDecimalSeparator()
        Rewrite(self.outputFile)
        try:
            if self.DebugList.Items.Count > 0:
                for i in range(0, self.DebugList.Items.Count):
                    writeln(self.outputFile, self.DebugList.Items[i])
        finally:
            CloseFile(self.outputFile)
    
    def printNested(self, level, aString):
        i = 0L
        prefix = ansistring()
        
        if level > 40:
            level = 40
        prefix = ""
        if level > 0:
            for i in range(1, level + 1):
                UNRESOLVED.AppendStr(prefix, "..")
        self.print(prefix + aString)
    
    def print(self, aString):
        if self.logging:
            writeln(self.outputFile, aString)
            Flush(self.outputFile)
        if udomain.domain.options.showWindowOnException:
            self.Visible = true
            self.BringToFront()
        if self.DebugList.Items.Count > 1000:
            self.DebugList.Items.Clear()
        try:
            self.DebugList.Items.Add(aString)
        except EOutOfResources:
            self.DebugList.Items.Clear()
        self.DebugList.ItemIndex = self.DebugList.Items.Count - 1
        self.DebugList.Invalidate()
        self.DebugList.Refresh()
    
    def clear(self):
        self.Visible = false
        self.DebugList.Items.Clear()
    
    def CloseClick(self, Sender):
        self.Visible = false
    
    def saveListAsClick(self, Sender):
        fileInfo = SaveFileNamesStructure()
        
        if self.DebugList.Items.Count <= 0:
            return
        if not usupport.getFileSaveInfo(usupport.kFileTypeExceptionList, usupport.kAskForFileName, "pstudio.nex", fileInfo):
            return
        try:
            self.saveExceptionListToFile(fileInfo.tempFile)
            fileInfo.writingWasSuccessful = true
        finally:
            usupport.cleanUpAfterFileSave(fileInfo)
    
    def clearListClick(self, Sender):
        if self.DebugList.Items.Count <= 0:
            return
        self.DebugList.Items.Clear()
    
    def helpButtonClick(self, Sender):
        delphi_compatability.Application.HelpJump("Numerical_exceptions")
    
    def FormResize(self, Sender):
        if delphi_compatability.Application.terminated:
            return
        self.Close.Left = self.ClientWidth - self.Close.Width - kBetweenGap
        self.saveListAs.Left = self.Close.Left
        self.clearList.Left = self.Close.Left
        self.helpButton.Left = self.Close.Left
        self.supportButton.Left = self.Close.Left
        self.DebugList.SetBounds(kBetweenGap, kBetweenGap, self.Close.Left - kBetweenGap * 2, umath.intMax(0, self.ClientHeight - self.optionsPanel.Height - kBetweenGap * 3))
        self.optionsPanel.SetBounds(kBetweenGap, umath.intMax(0, self.ClientHeight - self.optionsPanel.Height - kBetweenGap), self.Close.Left - kBetweenGap * 2, self.optionsPanel.Height)
    
    def WMGetMinMaxInfo(self, MSG):
        PdForm.WMGetMinMaxInfo(self)
        # FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 350
        UNRESOLVED.ptMinTrackSize.y = 190
    
    def logToFileClick(self, Sender):
        udomain.domain.options.logToFileOnException = self.logToFile.Checked
        if not self.logging:
            self.startLogging(ExtractFilePath(delphi_compatability.Application.exeName) + "errors.nex")
        else:
            self.stopLogging()
        self.logging = self.logToFile.Checked
    
    def showOnExceptionCheckBoxClick(self, Sender):
        udomain.domain.options.showWindowOnException = self.showOnExceptionCheckBox.Checked
    
    def supportButtonClick(self, Sender):
        infoForm = TProgramInfoForm()
        
        infoForm = uprginfo.TProgramInfoForm().create(delphi_compatability.Application)
        try:
            infoForm.ShowModal()
        finally:
            infoForm.free
            infoForm = None
    
