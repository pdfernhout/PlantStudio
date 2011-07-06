# unit ubmpsupport

from conversion_common import *
import umain
import delphi_compatability

def resizeBitmap(bitmap, newSize):
    if bitmap == None:
        return
    try:
        bitmap.Width = newSize.X
        bitmap.Height = newSize.Y
    except:
        bitmap.Width = 1
        bitmap.Height = 1

def fillBitmap(bitmap, color):
    if bitmap == None:
        return
    bitmap.Canvas.Brush.Color = bitmap.Canvas.Color
    bitmap.Canvas.FillRect(Rect(0, 0, bitmap.Width, bitmap.Height))

def copyBitmapToCanvasWithGlobalPalette(bitmap, aCanvas, aRect):
    oldPalette = HPALETTE()
    wholeRect = TRect()
    needPalette = false
    
    oldPalette = 0
    needPalette = screenColorModeIs256ColorsOrLess()
    if needPalette:
        oldPalette = UNRESOLVED.selectPalette(aCanvas.Handle, umain.MainForm.paletteImage.Picture.Bitmap.Palette, false)
        UNRESOLVED.realizePalette(aCanvas.Handle)
    wholeRect = Rect(0, 0, bitmap.Width, bitmap.Height)
    if (aRect.Left != 0) or (aRect.Right != 0) or (aRect.Top != 0) or (aRect.Bottom != 0):
        aCanvas.CopyRect(aRect, bitmap.Canvas, wholeRect)
    else:
        aCanvas.CopyRect(wholeRect, bitmap.Canvas, wholeRect)
    if needPalette:
        UNRESOLVED.selectPalette(aCanvas.Handle, oldPalette, true)
        UNRESOLVED.realizePalette(aCanvas.Handle)

def screenColorModeIs256ColorsOrLess():
    result = false
    screenDC = HDC()
    screenColorBits = 0
    
    result = false
    screenDC = UNRESOLVED.GetDC(0)
    try:
        screenColorBits = (UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.BITSPIXEL) * UNRESOLVED.GetDeviceCaps(screenDC, delphi_compatability.PLANES))
    finally:
        UNRESOLVED.ReleaseDC(0, screenDC)
    result = (screenColorBits == 1) or (screenColorBits == 4) or (screenColorBits == 8)
    return result

def setPixelFormatBasedOnScreenForBitmap(bitmap):
    if bitmap == None:
        return
    if screenColorModeIs256ColorsOrLess():
        bitmap.PixelFormat = delphi_compatability.TPixelFormat.pf8bit
        bitmap.Palette = UNRESOLVED.CopyPalette(umain.MainForm.paletteImage.Picture.Bitmap.Palette)

