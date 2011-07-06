// unit ubmpsupport

from conversion_common import *;
import delphi_compatability;

public void resizeBitmap(TBitmap bitmap, TPoint newSize) {
    if (bitmap == null) {
        return;
    }
    try {
        bitmap.Width = newSize.X;
        bitmap.Height = newSize.Y;
    } catch (Exception e) {
        bitmap.Width = 1;
        bitmap.Height = 1;
    }
}

public void fillBitmap(TBitmap bitmap, TColor color) {
    if (bitmap == null) {
        return;
    }
    bitmap.Canvas.Brush.Color = bitmap.Canvas.Color;
    bitmap.Canvas.FillRect(Rect(0, 0, bitmap.Width, bitmap.Height));
}

public void copyBitmapToCanvasWithGlobalPalette(TBitmap bitmap, TCanvas aCanvas, TRect aRect) {
    HPALETTE oldPalette = new HPALETTE();
    TRect wholeRect = new TRect();
    boolean needPalette = false;
    
    oldPalette = 0;
    needPalette = screenColorModeIs256ColorsOrLess();
    if (needPalette) {
        oldPalette = UNRESOLVED.selectPalette(aCanvas.Handle, UNRESOLVED.MainForm.paletteImage.picture.bitmap.palette, false);
        UNRESOLVED.realizePalette(aCanvas.Handle);
    }
    wholeRect = Rect(0, 0, bitmap.Width, bitmap.Height);
    if ((aRect.Left != 0) || (aRect.Right != 0) || (aRect.Top != 0) || (aRect.Bottom != 0)) {
        aCanvas.CopyRect(aRect, bitmap.Canvas, wholeRect);
    } else {
        aCanvas.CopyRect(wholeRect, bitmap.Canvas, wholeRect);
    }
    if (needPalette) {
        UNRESOLVED.selectPalette(aCanvas.Handle, oldPalette, true);
        UNRESOLVED.realizePalette(aCanvas.Handle);
    }
}

public boolean screenColorModeIs256ColorsOrLess() {
    result = false;
    HDC screenDC = new HDC();
    int screenColorBits = 0;
    
    result = false;
    screenDC = UNRESOLVED.GetDC(0);
    try {
        screenColorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES));
    } finally {
        UNRESOLVED.ReleaseDC(0, screenDC);
    }
    result = (screenColorBits == 1) || (screenColorBits == 4) || (screenColorBits == 8);
    return result;
}

public void setPixelFormatBasedOnScreenForBitmap(TBitmap bitmap) {
    if (bitmap == null) {
        return;
    }
    if (screenColorModeIs256ColorsOrLess()) {
        bitmap.PixelFormat = delphi_compatability.TPixelFormat.pf8bit;
        bitmap.Palette = UNRESOLVED.CopyPalette(UNRESOLVED.MainForm.paletteImage.picture.bitmap.palette);
    }
}


