unit Ubitmap;

{$R-} {for MemFree which has incorrect second param when long size}

interface

uses WinProcs, WinTypes, SysUtils, Graphics, Classes, ExtCtrls, ufiler;

type
  PdBitmap = class(TBitmap)
    public
  	procedure streamUsingFiler(filer: PdFiler); {not overriden because not based on streamable object}
    end;

  PdPaintBoxWithPalette = class(TPaintBox)
    public
		function GetPalette: HPALETTE; override;
    end;

function RequiresPalette(bitmap: TBitmap): boolean;
procedure CopyBitmapToClipboard(bitmap: TBitmap);
function BitmapMemorySize(bitmap: TBitmap): longint;
procedure PrintBitmap(bitmap: TBitmap; drawRect: TRect);

implementation

uses Forms, Dialogs, Printers, umain;

function PdPaintBoxWithPalette.GetPalette: HPALETTE;
  begin
  result := MainForm.paletteImage.picture.bitmap.palette;
  end;

{subclassed to get at protected streaming functions!}
procedure PdBitmap.streamUsingFiler(filer: PdFiler);
  begin
  if filer.isReading then
    self.readData(filer.stream)
  else if filer.isWriting then
  	self.writeData(filer.stream);
  end;

function RequiresPalette(bitmap: TBitmap): boolean;
  begin
  result := false;
  case bitmap.pixelFormat of
    pf1bit, pf4bit, pf8bit: result := true;
    end;
  end;

procedure CopyBitmapToClipboard(bitmap: TBitmap);
  var
    image, header: pointer;
    imageHandle, handleSet: THandle;
    headerSize: integer;
    imageSize: dword;
    clipboardOpen: boolean;
  begin
  header := nil;
  image := nil;
  imageHandle := 0;
  clipboardOpen := false;
  handleSet := 0;
  GetDIBSizes(bitmap.handle, headerSize, imageSize);     
  try
    imageHandle := GlobalAlloc(GMEM_MOVEABLE or GMEM_DDESHARE, headerSize + imageSize);
    try
      header := GlobalLock(imageHandle);
      image := Pointer(Longint(header) + headerSize);
      if not GetDIB(bitmap.handle, bitmap.palette, header^, image^) then
        raise Exception.create('Problem creating picture for clipboard: ' + SysErrorMessage(GetLastError));
      clipboardOpen := OpenClipboard(Application.mainForm.handle);
      if clipboardOpen then
        begin
        EmptyClipboard;
        handleSet := SetClipboardData(CF_DIB, imageHandle);
        if handleSet = 0 then
          raise Exception.create('Problem copying picture to clipboard: ' + SysErrorMessage(GetLastError));
        CloseClipboard;
        end;
    finally
      // the clipboard wants the handle to be unlocked
      GlobalUnlock(imageHandle);
    end;
  except
    // we are not supposed to free this handle unless there is a problem, because
    // the clipboard takes ownership of it
    GlobalFree(imageHandle);
    raise;
  end;
  end;

function BitmapMemorySize(bitmap: TBitmap): longint;
  var
    headerSize: integer;
    imageSize: dword;
  begin
  GetDIBSizes(bitmap.handle, headerSize, imageSize);
  result := bitmap.instanceSize + headerSize + imageSize;
  end;

procedure PrintBitmap(bitmap: TBitmap; drawRect: TRect);
  var
    image, header: pointer;
    imageHandle, handleSet: THandle;
    headerSize, printResult: integer;
    imageSize: dword;
    clipboardOpen: boolean;
  begin
  header := nil;
  image := nil;
  imageHandle := 0;
  clipboardOpen := false;
  handleSet := 0;
  GetDIBSizes(bitmap.handle, headerSize, imageSize);
  try
    imageHandle := GlobalAlloc(GMEM_MOVEABLE or GMEM_DDESHARE, headerSize + imageSize);
    try
      header := GlobalLock(imageHandle);
      image := Pointer(Longint(header) + headerSize);
      if not GetDIB(bitmap.handle, bitmap.palette, header^, image^) then
        raise Exception.create('Problem creating picture for printing: ' + SysErrorMessage(GetLastError));
      with drawRect do
        printResult := StretchDIBits(Printer.canvas.handle, left, top, right - left, bottom - top,
              0, 0, bitmap.width, bitmap.height, image, TBitmapInfo(header^), DIB_RGB_COLORS, SRCCOPY);
     if printResult = GDI_ERROR then
        raise Exception.create('Problem printing picture: ' + SysErrorMessage(GetLastError));
    finally
      GlobalUnlock(imageHandle);
    end;
  finally
    GlobalFree(imageHandle);
  end;
  end;
end.
