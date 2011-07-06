unit ubmpsupport;

interface

uses Windows, Graphics, Classes;

procedure resizeBitmap(bitmap: TBitmap; newSize: TPoint);
procedure fillBitmap(bitmap: TBitmap; color: TColor);
procedure copyBitmapToCanvasWithGlobalPalette(bitmap: TBitmap; aCanvas: TCanvas; aRect: TRect);
function screenColorModeIs256ColorsOrLess: boolean;
procedure setPixelFormatBasedOnScreenForBitmap(bitmap: TBitmap);

implementation

uses umain;

procedure resizeBitmap(bitmap: TBitmap; newSize: TPoint);
  begin
  if bitmap = nil then exit;
  with bitmap do
    try
      width := newSize.x;
      height := newSize.y;
    except
      width := 1;
      height := 1;
    end;
  end;

procedure fillBitmap(bitmap: TBitmap; color: TColor);
  begin
  if bitmap = nil then exit;
  with bitmap.canvas do
    begin
    brush.color := color;
    fillRect(rect(0, 0, bitmap.width, bitmap.height));
    end;
  end;

procedure copyBitmapToCanvasWithGlobalPalette(bitmap: TBitmap; aCanvas: TCanvas; aRect: TRect);
  var
    oldPalette: HPALETTE;
    wholeRect: TRect;
    needPalette: boolean;
  begin
  oldPalette := 0;
  needPalette := screenColorModeIs256ColorsOrLess;
  if needPalette then
    begin
    oldPalette := selectPalette(aCanvas.handle, MainForm.paletteImage.picture.bitmap.palette, false);
    realizePalette(aCanvas.handle);
    end;
  wholeRect := Rect(0, 0, bitmap.width, bitmap.height);
  with aRect do if (left <> 0) or (right <> 0) or (top <> 0) or (bottom <> 0) then
    aCanvas.copyRect(aRect, bitmap.canvas, wholeRect)
  else
    aCanvas.copyRect(wholeRect, bitmap.canvas, wholeRect);
  if needPalette then
    begin
    selectPalette(aCanvas.handle, oldPalette, true);
    realizePalette(aCanvas.handle);
    end;
  end;

function screenColorModeIs256ColorsOrLess: boolean;
  var
    screenDC: HDC;
    screenColorBits: integer;
  begin
  result := false;
  screenDC := GetDC(0);
  try
    screenColorBits := (GetDeviceCaps(screenDC, BITSPIXEL) * GetDeviceCaps(screenDC, PLANES));
  finally
    ReleaseDC(0, screenDC);
  end;
  result := (screenColorBits = 1) or (screenColorBits = 4) or (screenColorBits = 8);
  end;

procedure setPixelFormatBasedOnScreenForBitmap(bitmap: TBitmap);
  begin
  if bitmap = nil then exit;
  if screenColorModeIs256ColorsOrLess then
    begin
    bitmap.pixelFormat := pf8bit;
    bitmap.palette := CopyPalette(MainForm.paletteImage.picture.bitmap.palette);
    end;
  end;

end.
 