program PlantStudio;

uses
  Forms,
  Ucollect in 'UCOLLECT.PAS',
  Udomain in 'UDOMAIN.PAS',
  Ufruit in 'UFRUIT.PAS',
  Uhints in 'UHINTS.PAS',
  Uinflor in 'UINFLOR.PAS',
  Uintern in 'UINTERN.PAS',
  Uleaf in 'ULEAF.PAS',
  Umerist in 'UMERIST.PAS',
  Uparams in 'UPARAMS.PAS',
  Uplant in 'UPLANT.PAS',
  Uplantmn in 'UPLANTMN.PAS',
  Usection in 'USECTION.PAS',
  Usliders in 'USLIDERS.PAS',
  Usupport in 'USUPPORT.PAS',
  Utravers in 'UTRAVERS.PAS',
  Uturtle in 'UTURTLE.PAS',
  Utdo in 'UTDO.PAS',
  Urandom in 'URANDOM.PAS',
  Usstream in 'USSTREAM.PAS',
  Umath in 'UMATH.PAS',
  uunits in 'UUNITS.PAS',
  Udebug in 'UDEBUG.PAS' {DebugForm},
  Updform in 'UPDFORM.PAS',
  utransfr in 'UTRANSFR.PAS',
  ucursor in 'UCURSOR.PAS',
  Ufiler in 'UFILER.PAS',
  Uclasses in 'UCLASSES.PAS',
  Uoptions in 'UOPTIONS.PAS' {OptionsForm},
  Ucommand in 'UCOMMAND.PAS',
  Updcom in 'UPDCOM.PAS',
  Usplash in 'USPLASH.PAS' {SplashForm},
  Upp_hed in 'UPP_HED.PAS',
  Upp_col in 'UPP_COL.PAS',
  Upp_int in 'UPP_INT.PAS',
  Upp_lis in 'UPP_LIS.PAS',
  Upp_rea in 'UPP_REA.PAS',
  Upp_scv in 'UPP_SCV.PAS',
  Upp_tdo in 'UPP_TDO.PAS',
  Uppanel in 'UPPANEL.PAS',
  Ustats in 'USTATS.PAS',
  Ubrdopt in 'UBRDOPT.PAS' {BreedingOptionsForm},
  Uwait in 'UWAIT.PAS' {WaitForm},
  Uexcept in 'UEXCEPT.PAS',
  Ubreedr in 'UBREEDR.PAS' {BreederForm},
  Ubitmap in 'UBITMAP.PAS',
  Ugener in 'UGENER.PAS',
  Umover in 'UMOVER.PAS' {MoverForm},
  Utdoedit in 'UTDOEDIT.PAS' {TdoEditorForm},
  Udxfclr in 'UDXFCLR.PAS' {ChooseDXFColorForm},
  utimeser in 'utimeser.pas' {TimeSeriesForm},
  uwizard in 'uwizard.pas' {WizardForm},
  upp_boo in 'Upp_boo.pas',
  upart in 'Upart.pas',
  ubmpopt in 'ubmpopt.pas' {BitmapOptionsForm},
  uborders in 'uborders.pas' {PrintBordersForm},
  uwelcome in 'uwelcome.pas' {WelcomeForm},
  Umain in 'Umain.pas' {MainForm},
  upicktdo in 'upicktdo.pas' {PickTdoForm},
  utdomove in 'utdomove.pas' {TdoMoverForm},
  unozzle in 'unozzle.pas' {NozzleOptionsForm},
  uanimate in 'uanimate.pas' {AnimationFilesOptionsForm},
  uabout in 'uabout.pas' {AboutForm},
  uregister in 'uregister.pas' {RegistrationForm},
  ucustdrw in 'ucustdrw.pas' {CustomDrawOptionsForm},
  URegisterSupport in 'Register\PlantStudio Register\URegisterSupport.pas',
  umakepm in 'umakepm.pas',
  umakeht in 'umakeht.pas',
  unoted in 'unoted.pas' {NoteEditForm},
  uprginfo in 'uprginfo.pas' {ProgramInfoForm},
  uamendmt in 'uamendmt.pas',
  Dialogs,
  SysUtils,
  Uundo in 'Uundo.pas' {UndoRedoListForm},
  U3dexport in 'U3dexport.pas',
  Udrawingsurface in 'Udrawingsurface.pas',
  U3dsupport in 'U3dsupport.pas',
  uoptions3dexport in 'uoptions3dexport.pas' {Generic3DOptionsForm},
  ubmpsupport in 'ubmpsupport.pas';

{$R *.RES}
var
  successfulCreation: boolean;
  year, month, day: word;

  begin                          

  splashForm := nil;
  Domain := nil;
  MainForm := nil;
  
  Application.Title := 'PlantStudio';

  splashForm := TSplashForm.create(Application);
  splashForm.show;
  splashForm.update;
  splashForm.bringToFront;  

  Application.Title := 'PlantStudio';
  Application.HelpFile := 'Plantstudio.hlp';
  successfulCreation := PdDomain.createDefault;

  if successfulCreation then
    begin
    Application.CreateForm(TMainForm, MainForm);
  Application.CreateForm(TDebugForm, DebugForm);
  Application.CreateForm(TBreederForm, BreederForm);
  Application.CreateForm(TWaitForm, WaitForm);
  Application.CreateForm(TTimeSeriesForm, TimeSeriesForm);
  Application.CreateForm(TAboutForm, AboutForm);
  Application.CreateForm(TRegistrationForm, RegistrationForm);
  SplashForm.hide;
    MainForm.loadPlantFileAtStartup;
    MainForm.showWelcomeForm;
    Application.Run;
    end;

PdDomain.destroyDefault;
KfTurtle.defaultFree;
splashForm.hide;
splashForm.free;
end.
