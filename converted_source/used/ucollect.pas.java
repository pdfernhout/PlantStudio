// unit Ucollect

from conversion_common import *;
import ufiler;
import delphi_compatability;

public void addToListIfAbsent(TList list, TObject item) {
    if (item == null) {
        return;
    }
    if (list.IndexOf(item) < 0) {
        list.Add(item);
    }
}


class TListCollection extends TList {
    
    //note this should be virtual in TList but it isn't
    public void clear() {
        int i = 0;
        TObject temp = new TObject();
        
        if (this.Count > 0) {
            for (i = 0; i <= this.Count - 1; i++) {
                temp = this.Items[i];
                this.Items[i] = null;
                temp.free;
            }
        }
        super.clear();
    }
    
    public void clearPointersWithoutDeletingObjects() {
        int i = 0;
        
        if (this.Count > 0) {
            for (i = 0; i <= this.Count - 1; i++) {
                this.Items[i] = null;
            }
        }
        super.clear();
    }
    
    public void Destroy() {
        //pdf - clear will be called twice since inherited destroy also clears - but minor problem
        this.clear();
        super.Destroy();
    }
    
    public void ForEach(TForEachProc proc, TObject data) {
        int i = 0;
        
        if (this.Count > 0) {
            for (i = 0; i <= this.Count - 1; i++) {
                proc(this.Items[i], data);
            }
        }
    }
    
    public TObject FirstThat(TFirstLastFunc testFunc, TObject data) {
        result = new TObject();
        int i = 0;
        
        result = null;
        if (this.Count > 0) {
            for (i = 0; i <= this.Count - 1; i++) {
                if (testFunc(this.Items[i], data)) {
                    result = this.Items[i];
                    break;
                }
            }
        }
        return result;
    }
    
    public TObject LastThat(TFirstLastFunc testFunc, TObject data) {
        result = new TObject();
        int i = 0;
        
        result = null;
        if (this.Count > 0) {
            for (i = this.Count - 1; i >= 0; i--) {
                if (testFunc(this.Items[i], data)) {
                    result = this.Items[i];
                    break;
                }
            }
        }
        return result;
    }
    
    public void streamUsingFiler(PdFiler filer, PdStreamableObjectClass classForCreating) {
        long countOnStream = 0;
        long i = 0;
        PdStreamableObject streamableObject = new PdStreamableObject();
        
        if (filer.isReading()) {
            this.clear();
            countOnStream = filer.streamLongint(countOnStream);
            if (countOnStream > 0) {
                this.SetCapacity(countOnStream);
                for (i = 0; i <= countOnStream - 1; i++) {
                    streamableObject = classForCreating.create;
                    streamableObject.streamUsingFiler(filer);
                    this.Add(streamableObject);
                }
            }
            //filer is writing or counting
        } else {
            countOnStream = this.Count;
            countOnStream = filer.streamLongint(countOnStream);
            if (countOnStream > 0) {
                for (i = 0; i <= countOnStream - 1; i++) {
                    streamableObject = ufiler.PdStreamableObject(this.Items[i]);
                    streamableObject.streamUsingFiler(filer);
                }
            }
        }
    }
    
}
// functions for global clipboard transfer, not using
//    procedure copyToClipboard(classForCreating: PdStreamableObjectClass; format: word);
//    procedure getFromClipboard(classForCreating: PdStreamableObjectClass; format: word);
//
//procedure TListCollection.copyToClipboard(classForCreating: PdStreamableObjectClass; format: word);
//  var
//    memoryStream: TMemoryStream;
//    filer: PdFiler;
//    handleToBuffer: THandle;
//    pointerToBuffer: Pointer;
//  begin
//  memoryStream := TMemoryStream.create;
//  filer := PdFiler.createWithStream(memoryStream);
//  try
//    filer.setToWritingMode;
//    self.streamUsingFiler(filer, classForCreating);
//    handleToBuffer := GlobalAlloc(GMEM_MOVEABLE, memoryStream.size);
//    try
//      pointerToBuffer := GlobalLock(handleToBuffer);
//      try
//        System.Move(memoryStream.memory^, pointerToBuffer^, memoryStream.size);
//        Clipboard.setAsHandle(format, handleToBuffer);
//      finally
//        GlobalUnlock(handleToBuffer);
//      end;
//    except
//      GlobalFree(handleToBuffer);
//      raise;
//    end;
//  finally
//    memoryStream.free;
//    filer.free;
//  end;
//end;
//
//procedure TListCollection.getFromClipboard(classForCreating: PdStreamableObjectClass; format: word);
//  var
//    memoryStream : TMemoryStream;
//    filer: PdFiler;
//    handleToBuffer: THandle;
//    pointerToBuffer: Pointer;
//  begin
//  handleToBuffer := Clipboard.GetAsHandle(format);
//  if handleToBuffer <> 0 then begin
//    pointerToBuffer := GlobalLock(handleToBuffer);
//    if pointerToBuffer <> nil then begin
//      try
//        memoryStream := TMemoryStream.Create;
//        try
//          memoryStream.writeBuffer(pointerToBuffer^, GlobalSize(handleToBuffer));
//          memoryStream.position := 0;
//          filer := PdFiler.createWithStream(memoryStream);
//          filer.setToReadingMode;
//          self.streamUsingFiler(filer, classForCreating);
//        finally
//          memoryStream.free;
//          filer.free;
//        end;
//      finally
//        GlobalUnlock(handleToBuffer);
//      end;
//    end;
//  end;
//end;
//
