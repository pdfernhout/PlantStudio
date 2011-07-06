// unit Updform

from conversion_common import *;
import uhints;
import delphi_compatability;


class PdForm extends TForm {
    
    public void create(TComponent anOwner) {
        super.create(anOwner);
        uhints.makeAllFormComponentsHaveHints(this);
    }
    
}
