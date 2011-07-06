// unit umainsupport

from conversion_common import *;
import udomain;
import usupport;
import umain;
import delphi_compatability;

public void loadPlantFileAtStartup() {
    UNRESOLVED.cursor_startWait;
    try {
        if (udomain.domain.plantFileLoaded) {
            // if file loaded at startup, update for it, else act as if they picked new 
            UNRESOLVED.startWaitMessage("Drawing...");
            try {
                umain.MainForm.updateForPlantFile();
            } finally {
                UNRESOLVED.stopWaitMessage;
            }
        } else {
            umain.MainForm.MenuFileNewClick(umain.MainForm);
        }
        if (UNRESOLVED.splashForm != null) {
            UNRESOLVED.splashForm.hide;
        }
        umain.MainForm.updateForChangeToDomainOptions();
        umain.MainForm.updateFileMenuForOtherRecentFiles();
        umain.MainForm.selectedPlantPartID = -1;
        umain.MainForm.inFormCreation = false;
    } finally {
        UNRESOLVED.cursor_stopWait;
    }
}


