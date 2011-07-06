// unit Uexcept

from conversion_common import *;
import delphi_compatability;

public void FailNil(TObject anObject) {
    if (anObject == null) {
        throw new GeneralException.create("Problem: Not enough memory to carry out that operation.");
    }
}

public void FailNilPtr(Pointer aPointer) {
    if (aPointer == null) {
        throw new GeneralException.create("Problem: Not enough memory to carry out that operation.");
    }
}

public void FailNilPChar("UNFINISHED_FIX_THIS_PCHAR_INIT" aPointer) {
    if (aPointer == null) {
        throw new GeneralException.create("Problem: Not enough memory to carry out that operation.");
    }
}


