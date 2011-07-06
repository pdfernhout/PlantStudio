unit umainsupport;

interface

procedure loadPlantFileAtStartup;

implementation

uses umain, usupport, ucursor, udomain, uwait, usplash;

procedure loadPlantFileAtStartup;
  begin
  cursor_startWait;
  try
  { if file loaded at startup, update for it, else act as if they picked new }
  if domain.plantFileLoaded then
    begin
    startWaitMessage('Drawing...');
    try
      MainForm.updateForPlantFile;
    finally
      stopWaitMessage;
    end;
    end
  else
    MainForm.MenuFileNewClick(MainForm);
  if splashForm <> nil then splashForm.hide;
  MainForm.updateForChangeToDomainOptions;
  MainForm.updateFileMenuForOtherRecentFiles;
  MainForm.selectedPlantPartID := -1;
  MainForm.inFormCreation := false;
  finally
    cursor_stopWait;
  end;
  end;

end.
 