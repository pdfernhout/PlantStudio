# unit umainsupport

from conversion_common import *
import usplash
import uwait
import udomain
import ucursor
import usupport
import umain
import delphi_compatability

def loadPlantFileAtStartup():
    ucursor.cursor_startWait()
    try:
        if udomain.domain.plantFileLoaded:
            # if file loaded at startup, update for it, else act as if they picked new 
            uwait.startWaitMessage("Drawing...")
            try:
                umain.MainForm.updateForPlantFile()
            finally:
                uwait.stopWaitMessage()
        else:
            umain.MainForm.MenuFileNewClick(umain.MainForm)
        if usplash.splashForm != None:
            usplash.splashForm.Hide()
        umain.MainForm.updateForChangeToDomainOptions()
        umain.MainForm.updateFileMenuForOtherRecentFiles()
        umain.MainForm.selectedPlantPartID = -1
        umain.MainForm.inFormCreation = false
    finally:
        ucursor.cursor_stopWait()

