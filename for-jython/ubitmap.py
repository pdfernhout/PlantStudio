# unit Ubitmap

from common import *

from conversion_common import *
import usupport
import delphi_compatability
from swing_helpers import *

"""
import umain
import ufiler
import delphi_compatability
"""

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

#PDF PORT class PdBitmap(TBitmap):
class PdBitmap:
    def __init__(self):
        self.pixmap = None
        self.Width = 0
        self.Height = 0
        self.Transparent = True
        self.TransparentColor = delphi_compatability.clWhite # udomain.domain.options.backgroundColor
        
    def updateForChanges(self, widget):
        if self.Width == 0 or self.Height == 0:
            self.pixmap = None
            return
        #default_visual = gtk.gdk.visual_get_system()
        #self.pixmap = gtk.gdk.Pixmap(None, self.Width, self.Height, depth=default_visual.depth)
        self.pixmap = gtk.gdk.Pixmap(widget, self.Width, self.Height, depth=-1)
        """
        self.pixbuf = gtk.gdk.Pixbuf(colorspace=gtk.gdk.COLORSPACE_RGB, has_alpha=True, bits_per_sample=8, width=self.Width, height=self.Height)
        if self.Transparent:
            # PDF PORT IMPROVE
            # not sure how to do this without making a copy
            r = usupport.GetRValue(self.TransparentColor)
            g = usupport.GetRValue(self.TransparentColor)
            b = usupport.GetRValue(self.TransparentColor)
            self.pixbuf = self.pixbuf.add_alpha(True, chr(r), chr(g), chr(b))
        """
        
    def Fill(self, gc, color):
        if self.pixmap:
            rect = Rect(0, 0, self.Width, self.Height)
            DrawRectangle(self.pixmap, gc, rect, 1, color, color, filled=1)
            #self.pixmap.fill(color)
        
    #not overriden because not based on streamable object
    #subclassed to get at protected streaming functions!
    def streamUsingFiler(self, filer):
        if filer.isReading():
            self.ReadData(filer.stream)
        elif filer.isWriting():
            self.WriteData(filer.stream)
    
# PDF PORT class PdPaintBoxWithPalette(TPaintBox):
class PdPaintBoxWithPalette:
    def __init__(self):
        pass
    
    def GetPalette(self):
        result = HPALETTE()
        result = umain.MainForm.paletteImage.Picture.Bitmap.Palette
        return result
    
