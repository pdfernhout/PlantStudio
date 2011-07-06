unit Updform;

interface

uses Forms, Classes;

type

PdForm = class(TForm)
  public
  constructor create(anOwner: TComponent); override;
  end;

implementation

uses uhints;

constructor PdForm.create(anOwner: TComponent);
  begin
  inherited create(anOwner);
  MakeAllFormComponentsHaveHints(self);
  end;

end.
 