# unit ubmpsupport

from conversion_common import *
"""
import umain
"""
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

def fillBitmap(gc, bitmap, color):
    if bitmap == None:
        return
    bitmap.Fill(gc, color)

def copyBitmapToCanvasWithGlobalPalette(gc, bitmap, aCanvas, aRect):
    aCanvas.draw_drawable(gc, bitmap.pixmap, 0, 0, aRect.left, aRect.top, aRect.right - aRect.left, aRect.bottom - aRect.top)
    return

    ## UNUSED
    oldPalette = HPALETTE()
    wholeRect = TRect()
    needPalette = False
    
    oldPalette = 0
    needPalette = screenColorModeIs256ColorsOrLess()
    if needPalette:
        oldPalette = UNRESOLVED.selectPalette(aCanvas.Handle, umain.MainForm.paletteImage.Picture.Bitmap.Palette, False)
        UNRESOLVED.realizePalette(aCanvas.Handle)
    wholeRect = Rect(0, 0, bitmap.Width, bitmap.Height)
    if (aRect.Left != 0) or (aRect.Right != 0) or (aRect.Top != 0) or (aRect.Bottom != 0):
        aCanvas.CopyRect(aRect, bitmap.Canvas, wholeRect)
    else:
        aCanvas.CopyRect(wholeRect, bitmap.Canvas, wholeRect)
    if needPalette:
        UNRESOLVED.selectPalette(aCanvas.Handle, oldPalette, True)
        UNRESOLVED.realizePalette(aCanvas.Handle)

def screenColorModeIs256ColorsOrLess():
    # PDF PORT __ PUT IN DEFAULT FOR TESTING __ PROBABL OK THOUGH
    return False
    result = False
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

