# unit Ucollect

from conversion_common import *
import ufiler
import delphi_compatability

def addToListIfAbsent(list, item):
    if item == None:
        return
    if list.IndexOf(item) < 0:
        list.Add(item)

class TListCollection(TList):
    def __init__(self):
        pass
    
    #note this should be virtual in TList but it isn't
    def clear(self):
        i = 0
        temp = TObject()
        
        if self.Count > 0:
            for i in range(0, self.Count):
                temp = self.Items[i]
                self.Items[i] = None
                temp.free
        TList.clear(self)
    
    def clearPointersWithoutDeletingObjects(self):
        i = 0
        
        if self.Count > 0:
            for i in range(0, self.Count):
                self.Items[i] = None
        TList.clear(self)
    
    def Destroy(self):
        #pdf - clear will be called twice since inherited destroy also clears - but minor problem
        self.clear()
        TList.Destroy(self)
    
    def ForEach(self, proc, data):
        i = 0
        
        if self.Count > 0:
            for i in range(0, self.Count):
                proc(self.Items[i], data)
    
    def FirstThat(self, testFunc, data):
        result = TObject()
        i = 0
        
        result = None
        if self.Count > 0:
            for i in range(0, self.Count):
                if testFunc(self.Items[i], data):
                    result = self.Items[i]
                    break
        return result
    
    def LastThat(self, testFunc, data):
        result = TObject()
        i = 0
        
        result = None
        if self.Count > 0:
            for i in range(self.Count - 1, 0 + 1):
                if testFunc(self.Items[i], data):
                    result = self.Items[i]
                    break
        return result
    
    def streamUsingFiler(self, filer, classForCreating):
        countOnStream = 0L
        i = 0L
        streamableObject = PdStreamableObject()
        
        if filer.isReading():
            self.clear()
            countOnStream = filer.streamLongint(countOnStream)
            if countOnStream > 0:
                self.SetCapacity(countOnStream)
                for i in range(0, countOnStream):
                    streamableObject = classForCreating.create
                    streamableObject.streamUsingFiler(filer)
                    self.Add(streamableObject)
            #filer is writing or counting
        else:
            countOnStream = self.Count
            countOnStream = filer.streamLongint(countOnStream)
            if countOnStream > 0:
                for i in range(0, countOnStream):
                    streamableObject = ufiler.PdStreamableObject(self.Items[i])
                    streamableObject.streamUsingFiler(filer)
    
# functions for global clipboard transfer, not using
#    procedure copyToClipboard(classForCreating: PdStreamableObjectClass; format: word);
#    procedure getFromClipboard(classForCreating: PdStreamableObjectClass; format: word);
#
#procedure TListCollection.copyToClipboard(classForCreating: PdStreamableObjectClass; format: word);
#  var
#    memoryStream: TMemoryStream;
#    filer: PdFiler;
#    handleToBuffer: THandle;
#    pointerToBuffer: Pointer;
#  begin
#  memoryStream := TMemoryStream.create;
#  filer := PdFiler.createWithStream(memoryStream);
#  try
#    filer.setToWritingMode;
#    self.streamUsingFiler(filer, classForCreating);
#    handleToBuffer := GlobalAlloc(GMEM_MOVEABLE, memoryStream.size);
#    try
#      pointerToBuffer := GlobalLock(handleToBuffer);
#      try
#        System.Move(memoryStream.memory^, pointerToBuffer^, memoryStream.size);
#        Clipboard.setAsHandle(format, handleToBuffer);
#      finally
#        GlobalUnlock(handleToBuffer);
#      end;
#    except
#      GlobalFree(handleToBuffer);
#      raise;
#    end;
#  finally
#    memoryStream.free;
#    filer.free;
#  end;
#end;
#
#procedure TListCollection.getFromClipboard(classForCreating: PdStreamableObjectClass; format: word);
#  var
#    memoryStream : TMemoryStream;
#    filer: PdFiler;
#    handleToBuffer: THandle;
#    pointerToBuffer: Pointer;
#  begin
#  handleToBuffer := Clipboard.GetAsHandle(format);
#  if handleToBuffer <> 0 then begin
#    pointerToBuffer := GlobalLock(handleToBuffer);
#    if pointerToBuffer <> nil then begin
#      try
#        memoryStream := TMemoryStream.Create;
#        try
#          memoryStream.writeBuffer(pointerToBuffer^, GlobalSize(handleToBuffer));
#          memoryStream.position := 0;
#          filer := PdFiler.createWithStream(memoryStream);
#          filer.setToReadingMode;
#          self.streamUsingFiler(filer, classForCreating);
#        finally
#          memoryStream.free;
#          filer.free;
#        end;
#      finally
#        GlobalUnlock(handleToBuffer);
#      end;
#    end;
#  end;
#end;
#
