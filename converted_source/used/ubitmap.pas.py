# unit Ubitmap
#$R-
#for MemFree which has incorrect second param when long size

from conversion_common import *
import umain
import ufiler
import delphi_compatability

def RequiresPalette(bitmap):
    result = false
    result = false
    if bitmap.PixelFormat == delphi_compatability.TPixelFormat.pf1bit:
        result = true
    elif bitmap.PixelFormat == delphi_compatability.TPixelFormat.pf4bit:
        result = true
    elif bitmap.PixelFormat == delphi_compatability.TPixelFormat.pf8bit:
        result = true
    return result

def CopyBitmapToClipboard(bitmap):
    image = pointer()
    header = pointer()
    imageHandle = THandle()
    handleSet = THandle()
    headerSize = 0
    imageSize = dword()
    clipboardOpen = false
    
    header = None
    image = None
    imageHandle = 0
    clipboardOpen = false
    handleSet = 0
    UNRESOLVED.GetDIBSizes(bitmap.Handle, headerSize, imageSize)
    try:
        imageHandle = UNRESOLVED.GlobalAlloc(UNRESOLVED.GMEM_MOVEABLE or UNRESOLVED.GMEM_DDESHARE, headerSize + imageSize)
        try:
            header = UNRESOLVED.GlobalLock(imageHandle)
            image = UNRESOLVED.Pointer(header + headerSize)
            if not UNRESOLVED.GetDIB(bitmap.Handle, bitmap.Palette, header.PDF_FIX_POINTER_ACCESS, image.PDF_FIX_POINTER_ACCESS):
                raise GeneralException.create("Problem creating picture for clipboard: " + UNRESOLVED.SysErrorMessage(UNRESOLVED.GetLastError))
            clipboardOpen = UNRESOLVED.OpenClipboard(delphi_compatability.Application.MainForm.Handle)
            if clipboardOpen:
                UNRESOLVED.EmptyClipboard
                handleSet = UNRESOLVED.SetClipboardData(UNRESOLVED.CF_DIB, imageHandle)
                if handleSet == 0:
                    raise GeneralException.create("Problem copying picture to clipboard: " + UNRESOLVED.SysErrorMessage(UNRESOLVED.GetLastError))
                UNRESOLVED.CloseClipboard
        finally:
            # the clipboard wants the handle to be unlocked
            UNRESOLVED.GlobalUnlock(imageHandle)
    except:
        # we are not supposed to free this handle unless there is a problem, because
        # the clipboard takes ownership of it
        UNRESOLVED.GlobalFree(imageHandle)
        raise

def BitmapMemorySize(bitmap):
    result = 0L
    headerSize = 0
    imageSize = dword()
    
    UNRESOLVED.GetDIBSizes(bitmap.Handle, headerSize, imageSize)
    result = bitmap.instanceSize + headerSize + imageSize
    return result

def PrintBitmap(bitmap, drawRect):
    image = pointer()
    header = pointer()
    imageHandle = THandle()
    handleSet = THandle()
    headerSize = 0
    printResult = 0
    imageSize = dword()
    clipboardOpen = false
    
    header = None
    image = None
    imageHandle = 0
    clipboardOpen = false
    handleSet = 0
    UNRESOLVED.GetDIBSizes(bitmap.Handle, headerSize, imageSize)
    try:
        imageHandle = UNRESOLVED.GlobalAlloc(UNRESOLVED.GMEM_MOVEABLE or UNRESOLVED.GMEM_DDESHARE, headerSize + imageSize)
        try:
            header = UNRESOLVED.GlobalLock(imageHandle)
            image = UNRESOLVED.Pointer(header + headerSize)
            if not UNRESOLVED.GetDIB(bitmap.Handle, bitmap.Palette, header.PDF_FIX_POINTER_ACCESS, image.PDF_FIX_POINTER_ACCESS):
                raise GeneralException.create("Problem creating picture for printing: " + UNRESOLVED.SysErrorMessage(UNRESOLVED.GetLastError))
            printResult = UNRESOLVED.StretchDIBits(UNRESOLVED.Printer.canvas.handle, drawRect.Left, drawRect.Top, drawRect.Right - drawRect.Left, drawRect.Bottom - drawRect.Top, 0, 0, bitmap.Width, bitmap.Height, image, delphi_compatability.TBitmapInfo(header.PDF_FIX_POINTER_ACCESS), delphi_compatability.DIB_RGB_COLORS, delphi_compatability.SRCCOPY)
            if printResult == UNRESOLVED.GDI_ERROR:
                raise GeneralException.create("Problem printing picture: " + UNRESOLVED.SysErrorMessage(UNRESOLVED.GetLastError))
        finally:
            UNRESOLVED.GlobalUnlock(imageHandle)
    finally:
        UNRESOLVED.GlobalFree(imageHandle)

class PdBitmap(TBitmap):
    def __init__(self):
        pass
    
    #not overriden because not based on streamable object
    #subclassed to get at protected streaming functions!
    def streamUsingFiler(self, filer):
        if filer.isReading():
            self.ReadData(filer.stream)
        elif filer.isWriting():
            self.WriteData(filer.stream)
    
class PdPaintBoxWithPalette(TPaintBox):
    def __init__(self):
        pass
    
    def GetPalette(self):
        result = HPALETTE()
        result = umain.MainForm.paletteImage.Picture.Bitmap.Palette
        return result
    
