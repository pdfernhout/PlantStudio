// unit Ubitmap
//$R-
//for MemFree which has incorrect second param when long size

from conversion_common import *;
import umain;
import ufiler;
import delphi_compatability;

public boolean RequiresPalette(TBitmap bitmap) {
    result = false;
    result = false;
    switch (bitmap.PixelFormat) {
        case delphi_compatability.TPixelFormat.pf1bit:
            result = true;
            break;
        case delphi_compatability.TPixelFormat.pf4bit:
            result = true;
            break;
        case delphi_compatability.TPixelFormat.pf8bit:
            result = true;
            break;
    return result;
}

public void CopyBitmapToClipboard(TBitmap bitmap) {
    pointer image = new pointer();
    pointer header = new pointer();
    THandle imageHandle = new THandle();
    THandle handleSet = new THandle();
    int headerSize = 0;
    dword imageSize = new dword();
    boolean clipboardOpen = false;
    
    header = null;
    image = null;
    imageHandle = 0;
    clipboardOpen = false;
    handleSet = 0;
    UNRESOLVED.GetDIBSizes(bitmap.Handle, headerSize, imageSize);
    try {
        imageHandle = UNRESOLVED.GlobalAlloc(UNRESOLVED.GMEM_MOVEABLE || UNRESOLVED.GMEM_DDESHARE, headerSize + imageSize);
        try {
            header = UNRESOLVED.GlobalLock(imageHandle);
            image = UNRESOLVED.Pointer(header + headerSize);
            if (!UNRESOLVED.GetDIB(bitmap.Handle, bitmap.Palette, header.PDF_FIX_POINTER_ACCESS, image.PDF_FIX_POINTER_ACCESS)) {
                throw new GeneralException.create("Problem creating picture for clipboard: " + UNRESOLVED.SysErrorMessage(UNRESOLVED.GetLastError));
            }
            clipboardOpen = UNRESOLVED.OpenClipboard(delphi_compatability.Application.MainForm.Handle);
            if (clipboardOpen) {
                UNRESOLVED.EmptyClipboard;
                handleSet = UNRESOLVED.SetClipboardData(UNRESOLVED.CF_DIB, imageHandle);
                if (handleSet == 0) {
                    throw new GeneralException.create("Problem copying picture to clipboard: " + UNRESOLVED.SysErrorMessage(UNRESOLVED.GetLastError));
                }
                UNRESOLVED.CloseClipboard;
            }
        } finally {
            // the clipboard wants the handle to be unlocked
            UNRESOLVED.GlobalUnlock(imageHandle);
        }
    } catch (Exception e) {
        // we are not supposed to free this handle unless there is a problem, because
        // the clipboard takes ownership of it
        UNRESOLVED.GlobalFree(imageHandle);
        throw new Exception();
    }
}

public long BitmapMemorySize(TBitmap bitmap) {
    result = 0;
    int headerSize = 0;
    dword imageSize = new dword();
    
    UNRESOLVED.GetDIBSizes(bitmap.Handle, headerSize, imageSize);
    result = bitmap.instanceSize + headerSize + imageSize;
    return result;
}

public void PrintBitmap(TBitmap bitmap, TRect drawRect) {
    pointer image = new pointer();
    pointer header = new pointer();
    THandle imageHandle = new THandle();
    THandle handleSet = new THandle();
    int headerSize = 0;
    int printResult = 0;
    dword imageSize = new dword();
    boolean clipboardOpen = false;
    
    header = null;
    image = null;
    imageHandle = 0;
    clipboardOpen = false;
    handleSet = 0;
    UNRESOLVED.GetDIBSizes(bitmap.Handle, headerSize, imageSize);
    try {
        imageHandle = UNRESOLVED.GlobalAlloc(UNRESOLVED.GMEM_MOVEABLE || UNRESOLVED.GMEM_DDESHARE, headerSize + imageSize);
        try {
            header = UNRESOLVED.GlobalLock(imageHandle);
            image = UNRESOLVED.Pointer(header + headerSize);
            if (!UNRESOLVED.GetDIB(bitmap.Handle, bitmap.Palette, header.PDF_FIX_POINTER_ACCESS, image.PDF_FIX_POINTER_ACCESS)) {
                throw new GeneralException.create("Problem creating picture for printing: " + UNRESOLVED.SysErrorMessage(UNRESOLVED.GetLastError));
            }
            printResult = UNRESOLVED.StretchDIBits(UNRESOLVED.Printer.canvas.handle, drawRect.Left, drawRect.Top, drawRect.Right - drawRect.Left, drawRect.Bottom - drawRect.Top, 0, 0, bitmap.Width, bitmap.Height, image, delphi_compatability.TBitmapInfo(header.PDF_FIX_POINTER_ACCESS), delphi_compatability.DIB_RGB_COLORS, delphi_compatability.SRCCOPY);
            if (printResult == UNRESOLVED.GDI_ERROR) {
                throw new GeneralException.create("Problem printing picture: " + UNRESOLVED.SysErrorMessage(UNRESOLVED.GetLastError));
            }
        } finally {
            UNRESOLVED.GlobalUnlock(imageHandle);
        }
    } finally {
        UNRESOLVED.GlobalFree(imageHandle);
    }
}


class PdBitmap extends TBitmap {
    
    //not overriden because not based on streamable object
    //subclassed to get at protected streaming functions!
    public void streamUsingFiler(PdFiler filer) {
        if (filer.isReading()) {
            this.ReadData(filer.stream);
        } else if (filer.isWriting()) {
            this.WriteData(filer.stream);
        }
    }
    
}
class PdPaintBoxWithPalette extends TPaintBox {
    
    public HPALETTE GetPalette() {
        result = new HPALETTE();
        result = umain.MainForm.paletteImage.Picture.Bitmap.Palette;
        return result;
    }
    
}
