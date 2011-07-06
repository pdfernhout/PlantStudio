// unit upicktdo

from conversion_common import *;
import utdomove;
import utdoedit;
import updform;
import delphi_compatability;


class TPickTdoForm extends PdForm {
    public TDrawGrid grid;
    public TButton Close;
    public TButton cancel;
    public TButton newTdo;
    public TGroupBox libraryGroupBox;
    public TImage fileChangedImage;
    public TEdit libraryFileName;
    public TButton apply;
    public TSpeedButton helpButton;
    public TSpeedButton sectionTdosChangeLibrary;
    public TButton editTdo;
    public TButton mover;
    public TButton copyTdo;
    public TButton deleteTdo;
    public TComboBox tdos;
    public PdParameter param;
    public KfObject3D originalTdo;
    public boolean tdoSelectionChanged;
    public boolean libraryChanged;
    public boolean editedTdo;
    public boolean internalChange;
    
    //$R *.DFM
    public boolean initializeWithTdoParameterAndPlantName(KfObject3d aTdo, PdParameter aParam, String aName) {
        result = false;
        // returns false if user canceled action
        result = true;
        if (!this.readTdosFromFile()) {
            MessageDialog("You cannot change or edit this 3D object" + chr(13) + "until you choose a 3D object library.", mtWarning, {mbOK, }, 0);
            result = false;
            return result;
        }
        this.libraryFileName.Text = UNRESOLVED.domain.defaultTdoLibraryFileName;
        this.libraryFileName.SelStart = len(this.libraryFileName.Text);
        this.originalTdo = aTdo;
        if (this.originalTdo == null) {
            throw new GeneralException.create("Problem: Nil 3D object in method TPickTdoForm.initializeWithTdoParameterAndPlantName.");
        }
        this.param = aParam;
        if (this.param == null) {
            throw new GeneralException.create("Problem: Nil parameter in method TPickTdoForm.initializeWithTdoParameterAndPlantName.");
        }
        this.Caption = this.param.name + " for " + aName;
        return result;
    }
    
    public void FormActivate(TObject Sender) {
        this.selectTdoBasedOn(this.originalTdo);
    }
    
    public void selectTdoBasedOn(KfObject3D aTdo) {
        int indexToSelect = 0;
        int i = 0;
        KfObject3D tdo = new KfObject3D();
        
        // assumes initialize already called and tdos already in list
        indexToSelect = -1;
        if (this.tdos.Items.Count > 0) {
            for (i = 0; i <= this.tdos.Items.Count - 1; i++) {
                tdo = UNRESOLVED.KfObject3d(this.tdos.Items.Objects[i]);
                if (tdo.isSameAs(aTdo)) {
                    indexToSelect = i;
                    break;
                }
            }
        }
        if (indexToSelect < 0) {
            if (MessageDialog("This 3D object is not in the current library." + chr(13) + "Its name or shape is different from the 3D objects in the list." + chr(13) + chr(13) + "Do you want to add this 3D object to the library?", mtWarning, {mbYes, mbNo, }, 0) == delphi_compatability.IDNO) {
                return;
            }
            tdo = UNRESOLVED.KfObject3D.create;
            tdo.copyFrom(aTdo);
            this.tdos.Items.AddObject(tdo.name, tdo);
            this.grid.RowCount = this.tdos.Items.Count / this.grid.ColCount + 1;
            this.libraryGroupBox.Caption = "The current library has " + IntToStr(this.tdos.Items.Count) + " object(s)";
            this.setLibraryChanged(true);
            indexToSelect = this.tdos.Items.Count - 1;
        }
        if (indexToSelect >= 0) {
            this.selectTdoAtIndex(indexToSelect);
        }
    }
    
    public void selectTdoAtIndex(short indexToSelect) {
        TGridRect gridRect = new TGridRect();
        int lastRow = 0;
        
        this.chooseTdoFromList(indexToSelect);
        if ((indexToSelect < 0) || (indexToSelect > this.tdos.Items.Count - 1)) {
            gridRect.left = -1;
            gridRect.top = -1;
        } else {
            gridRect.left = indexToSelect % this.grid.ColCount;
            gridRect.top = indexToSelect / this.grid.ColCount;
        }
        gridRect.right = gridRect.left;
        gridRect.bottom = gridRect.top;
        this.grid.Selection = gridRect;
        // keep selection in view
        lastRow = this.grid.TopRow + this.grid.VisibleRowCount - 1;
        if (gridRect.top > lastRow) {
            this.grid.TopRow = this.grid.TopRow + (gridRect.top - lastRow);
        }
    }
    
    public KfObject3D selectedTdo() {
        result = new KfObject3D();
        int index = 0;
        
        result = null;
        index = this.grid.Selection.top * this.grid.ColCount + this.grid.Selection.left;
        if ((index >= 0) && (index <= this.tdos.Items.Count - 1)) {
            result = (UNRESOLVED.KfObject3D)UNRESOLVED.TObject(this.tdos.Items.Objects[index]);
        }
        return result;
    }
    
    public void chooseTdoFromList(short index) {
        if ((index >= 0) && (index <= this.tdos.Items.Count - 1)) {
            this.tdos.ItemIndex = index;
        }
    }
    
    public void CloseClick(TObject Sender) {
        if ((this.tdoSelectionChanged || this.editedTdo) && (this.selectedTdo() != null)) {
            this.applyClick(this);
        }
        this.ModalResult = mrOK;
    }
    
    public void cancelClick(TObject Sender) {
        this.ModalResult = mrCancel;
    }
    
    public void applyClick(TObject Sender) {
        if (this.selectedTdo() != null) {
            UNRESOLVED.MainForm.doCommand(UNRESOLVED.PdChangeTdoValueCommand.createCommandWithListOfPlants(UNRESOLVED.MainForm.selectedPlants, this.selectedTdo(), this.param.fieldNumber, this.param.regrow));
        }
    }
    
    public void loadNewTdoLibrary() {
        String fileNameWithPath = "";
        
        fileNameWithPath = UNRESOLVED.getFileOpenInfo(UNRESOLVED.kFileTypeTdo, UNRESOLVED.domain.defaultTdoLibraryFileName, "Choose a 3D object library (tdo) file");
        if (fileNameWithPath == "") {
            return;
        }
        UNRESOLVED.domain.defaultTdoLibraryFileName = fileNameWithPath;
        this.readTdosFromFile();
    }
    
    public boolean readTdosFromFile() {
        result = false;
        KfObject3D newTdo = new KfObject3D();
        TextFile inputFile = new TextFile();
        
        // returns false if file could not be found and user canceled finding another
        result = true;
        this.tdos.Clear();
        if (UNRESOLVED.domain == null) {
            return result;
        }
        if (!UNRESOLVED.domain.checkForExistingDefaultTdoLibrary) {
            result = false;
            return result;
        }
        AssignFile(inputFile, UNRESOLVED.domain.defaultTdoLibraryFileName);
        try {
            // v1.5
            UNRESOLVED.setDecimalSeparator;
            Reset(inputFile);
            while (!UNRESOLVED.eof(inputFile)) {
                newTdo = UNRESOLVED.KfObject3D.create;
                newTdo.readFromFileStream(inputFile, UNRESOLVED.kInTdoLibrary);
                this.tdos.Items.AddObject(newTdo.name, newTdo);
            }
        } finally {
            CloseFile(inputFile);
            this.grid.RowCount = this.tdos.Items.Count / this.grid.ColCount + 1;
            this.libraryGroupBox.Caption = "The current library has " + IntToStr(this.tdos.Items.Count) + " object(s)";
        }
        return result;
    }
    
    public void saveTdosToLibrary() {
        SaveFileNamesStructure fileInfo = new SaveFileNamesStructure();
        String suggestedName = "";
        TextFile outputFile = new TextFile();
        short i = 0;
        KfObject3D tdo = new KfObject3D();
        
        suggestedName = UNRESOLVED.domain.defaultTdoLibraryFileName;
        if (!UNRESOLVED.getFileSaveInfo(UNRESOLVED.kFileTypeTdo, UNRESOLVED.kDontAskForFileName, suggestedName, fileInfo)) {
            return;
        }
        AssignFile(outputFile, fileInfo.tempFile);
        try {
            // v1.5
            UNRESOLVED.setDecimalSeparator;
            Rewrite(outputFile);
            UNRESOLVED.startFileSave(fileInfo);
            if (this.tdos.Items.Count > 0) {
                for (i = 0; i <= this.tdos.Items.Count - 1; i++) {
                    tdo = (UNRESOLVED.KfObject3D)UNRESOLVED.TObject(this.tdos.Items.Objects[i]);
                    if (tdo == null) {
                        continue;
                    }
                    tdo.writeToFileStream(outputFile, UNRESOLVED.kInTdoLibrary);
                }
            }
            fileInfo.writingWasSuccessful = true;
        } finally {
            CloseFile(outputFile);
            UNRESOLVED.cleanUpAfterFileSave(fileInfo);
            this.setLibraryChanged(false);
        }
    }
    
    public void setLibraryChanged(boolean fileChanged) {
        this.libraryChanged = fileChanged;
        if (this.libraryChanged) {
            this.fileChangedImage.Picture = UNRESOLVED.MainForm.fileChangedImage.picture;
        } else {
            this.fileChangedImage.Picture = UNRESOLVED.MainForm.fileNotChangedImage.picture;
        }
    }
    
    public KfObject3D tdoForIndex(short index) {
        result = new KfObject3D();
        result = null;
        if ((index >= 0) && (index <= this.tdos.Items.Count - 1)) {
            result = UNRESOLVED.KfObject3D(this.tdos.Items.Objects[index]);
        }
        return result;
    }
    
    public void gridDrawCell(TObject Sender, int Col, int Row, TRect Rect, TGridDrawState State) {
        KfObject3d tdo = new KfObject3d();
        KfTurtle turtle = new KfTurtle();
        boolean selected = false;
        short index = 0;
        TBitmap bitmap = new TBitmap();
        TPoint bestPoint = new TPoint();
        
        this.grid.Canvas.Brush.Color = this.grid.Color;
        this.grid.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psClear;
        this.grid.Canvas.FillRect(Rect);
        selected = UNRESOLVED.gdSelected in State;
        tdo = null;
        index = Row * this.grid.ColCount + Col;
        tdo = this.tdoForIndex(index);
        if (tdo == null) {
            return;
        }
        // draw tdo 
        turtle = UNRESOLVED.KfTurtle.defaultStartUsing;
        bitmap = delphi_compatability.TBitmap().Create();
        try {
            bitmap.Width = this.grid.DefaultColWidth;
            bitmap.Height = this.grid.DefaultRowHeight;
        } catch (Exception e) {
            bitmap.Width = 1;
            bitmap.Height = 1;
        }
        if (!selected) {
            bitmap.Canvas.Brush.Color = delphi_compatability.clWhite;
        } else {
            bitmap.Canvas.Brush.Color = UNRESOLVED.clHighlight;
        }
        bitmap.Canvas.FillRect(UNRESOLVED.classes.Rect(0, 0, bitmap.Width, bitmap.Height));
        try {
            //grid.canvas;
            turtle.drawingSurface.pane = bitmap.Canvas;
            turtle.setDrawOptionsForDrawingTdoOnly;
            // must be after pane and draw options set 
            turtle.reset;
            // v1.6b1 added method for centering tdo
            bestPoint = tdo.bestPointForDrawingAtScale(turtle, Point(0, 0), Point(bitmap.Width, bitmap.Height), 0.3);
            turtle.xyz(bestPoint.X, bestPoint.Y, 0);
            turtle.drawingSurface.recordingStart;
            //0.15);
            tdo.draw(turtle, 0.3, "", "", 0, 0);
            turtle.drawingSurface.recordingStop;
            turtle.drawingSurface.recordingDraw;
            turtle.drawingSurface.clearTriangles;
            this.grid.Canvas.Draw(Rect.left, Rect.top, bitmap);
            this.grid.Canvas.Brush.Style = delphi_compatability.TFPBrushStyle.bsClear;
            this.grid.Canvas.Pen.Color = delphi_compatability.clSilver;
            this.grid.Canvas.Pen.Style = delphi_compatability.TFPPenStyle.psSolid;
            //FIX unresolved WITH expression: Rect
            this.grid.Canvas.Rectangle(this.Left, this.Top, UNRESOLVED.right, UNRESOLVED.bottom);
        } finally {
            UNRESOLVED.KfTurtle.defaultStopUsing;
            bitmap.free;
        }
    }
    
    public void gridSelectCell(TObject Sender, int Col, int Row, boolean CanSelect) {
        if (this.internalChange) {
            return CanSelect;
        }
        this.tdoSelectionChanged = true;
        this.chooseTdoFromList(Row * this.grid.ColCount + Col);
        return CanSelect;
    }
    
    public void tdosChange(TObject Sender) {
        this.internalChange = true;
        this.tdoSelectionChanged = true;
        this.grid.Row = this.tdos.ItemIndex / this.grid.ColCount;
        this.grid.Col = this.tdos.ItemIndex % this.grid.ColCount;
        this.internalChange = false;
    }
    
    public String hintForTdosDrawGridAtPoint(TComponent aComponent, TPoint aPoint, TRect cursorRect) {
        raise "method hintForTdosDrawGridAtPoint had assigned to var parameter cursorRect not added to return; fixup manually"
        result = "";
        int col = 0;
        int row = 0;
        int index = 0;
        KfObject3D tdo = new KfObject3D();
        
        result = "";
        col, row = this.grid.MouseToCell(aPoint.X, aPoint.Y, col, row);
        index = row * this.grid.ColCount + col;
        tdo = this.tdoForIndex(index);
        if (tdo == null) {
            return result;
        }
        result = tdo.getName;
        // change hint if cursor moves out of the current item's rectangle 
        cursorRect = this.grid.CellRect(col, row);
        return result;
    }
    
    public void sectionTdosChangeLibraryClick(TObject Sender) {
        this.loadNewTdoLibrary();
        this.grid.Invalidate();
        this.libraryFileName.Text = UNRESOLVED.domain.defaultTdoLibraryFileName;
        this.libraryFileName.SelStart = len(this.libraryFileName.Text);
    }
    
    public void helpButtonClick(TObject Sender) {
        delphi_compatability.Application.HelpJump("Using_3D_object_parameter_panels");
    }
    
    public void FormClose(TObject Sender, TCloseAction Action) {
        int response = 0;
        
        if (this.libraryChanged) {
            if (this.ModalResult == mrOK) {
                this.saveTdosToLibrary();
            } else if (this.ModalResult == mrCancel) {
                response = MessageDialog("Do you want to save the changes you made" + chr(13) + "to the 3D object library?", mtConfirmation, {mbYes, mbNo, mbCancel, }, 0);
                switch (response) {
                    case delphi_compatability.IDYES:
                        this.saveTdosToLibrary();
                        Action = delphi_compatability.TCloseAction.caFree;
                        break;
                    case delphi_compatability.IDNO:
                        Action = delphi_compatability.TCloseAction.caFree;
                        break;
                    case delphi_compatability.IDCANCEL:
                        Action = delphi_compatability.TCloseAction.caNone;
                        break;
            }
        }
    }
    
    public void gridDblClick(TObject Sender) {
        this.applyClick(this);
    }
    
    public void editTdoClick(TObject Sender) {
        TTdoEditorForm tdoEditorForm = new TTdoEditorForm();
        int response = 0;
        
        if (this.selectedTdo() == null) {
            return;
        }
        tdoEditorForm = utdoedit.TTdoEditorForm().create(this);
        if (tdoEditorForm == null) {
            throw new GeneralException.create("Problem: Could not create 3D object editor window.");
        }
        try {
            tdoEditorForm.initializeWithTdo(this.selectedTdo());
            response = tdoEditorForm.ShowModal();
            if (response == mrOK) {
                this.selectedTdo().copyFrom(tdoEditorForm.tdo);
                this.editedTdo = true;
                this.grid.Invalidate();
                this.setLibraryChanged(true);
                this.chooseTdoFromList(this.tdos.Items.IndexOfObject(this.selectedTdo()));
            }
        } finally {
            tdoEditorForm.free;
            tdoEditorForm = null;
        }
    }
    
    public void newTdoClick(TObject Sender) {
        TTdoEditorForm tdoEditorForm = new TTdoEditorForm();
        int response = 0;
        KfObject3D newTdo = new KfObject3D();
        String newName = "";
        
        newName = "";
        newTdo = UNRESOLVED.KfObject3D.create;
        newTdo.setName("New 3D object");
        tdoEditorForm = utdoedit.TTdoEditorForm().create(this);
        if (tdoEditorForm == null) {
            throw new GeneralException.create("Problem: Could not create 3D object editor window.");
        }
        try {
            tdoEditorForm.initializeWithTdo(newTdo);
            response = tdoEditorForm.ShowModal();
            if (response == mrOK) {
                if (newTdo.getName == "New 3D object") {
                    if (InputQuery("Name 3D object", "Enter a name for the new 3D object", newName)) {
                        newTdo.setName(newName);
                    } else {
                        newTdo.setName("Unnamed 3D object");
                    }
                }
                newTdo.copyFrom(tdoEditorForm.tdo);
                this.editedTdo = true;
                this.tdos.Items.AddObject(newTdo.name, newTdo);
                this.grid.RowCount = this.tdos.Items.Count / this.grid.ColCount + 1;
                this.selectTdoAtIndex(this.tdos.Items.Count - 1);
                this.libraryGroupBox.Caption = "The current library has " + IntToStr(this.tdos.Items.Count) + " object(s)";
                this.setLibraryChanged(true);
                this.chooseTdoFromList(this.tdos.Items.IndexOfObject(this.selectedTdo()));
            }
        } finally {
            tdoEditorForm.free;
            tdoEditorForm = null;
        }
    }
    
    public void copyTdoClick(TObject Sender) {
        KfObject3D newTdo = new KfObject3D();
        String newName = "";
        
        if (this.selectedTdo() == null) {
            return;
        }
        newName = "Copy of " + this.selectedTdo().getName;
        if (!InputQuery("Enter name for copy", "Type a name for the copy of " + this.selectedTdo().getName, newName)) {
            return;
        }
        newTdo = UNRESOLVED.KfObject3D.create;
        this.selectedTdo().copyTo(newTdo);
        newTdo.setName(newName);
        this.tdos.Items.AddObject(newTdo.name, newTdo);
        this.grid.RowCount = this.tdos.Items.Count / this.grid.ColCount + 1;
        this.selectTdoAtIndex(this.tdos.Items.Count - 1);
        this.libraryGroupBox.Caption = "The current library has " + IntToStr(this.tdos.Items.Count) + " object(s)";
        this.setLibraryChanged(true);
        this.chooseTdoFromList(this.tdos.Items.IndexOfObject(this.selectedTdo()));
    }
    
    public void deleteTdoClick(TObject Sender) {
        int oldIndex = 0;
        String nameToShow = "";
        
        if (this.selectedTdo() == null) {
            return;
        }
        nameToShow = this.selectedTdo().getName;
        if (nameToShow == "") {
            nameToShow = "[unnamed]";
        }
        if (MessageDialog("Really delete the 3D object named " + nameToShow + "?" + chr(13) + chr(13) + "(You cannot undo this action," + chr(13) + "but you can close the window and not save your changes" + chr(13) + "if you need to get this 3D object back.)", mtConfirmation, {mbYes, mbNo, }, 0) == delphi_compatability.IDNO) {
            return;
        }
        oldIndex = this.tdos.Items.IndexOfObject(this.selectedTdo());
        this.tdos.Items.Delete(oldIndex);
        this.grid.RowCount = this.tdos.Items.Count / this.grid.ColCount + 1;
        this.selectTdoAtIndex(oldIndex);
        this.libraryGroupBox.Caption = "The current library has " + IntToStr(this.tdos.Items.Count) + " object(s)";
        this.setLibraryChanged(true);
        this.chooseTdoFromList(this.tdos.Items.IndexOfObject(this.selectedTdo()));
        this.grid.Invalidate();
    }
    
    public void WMGetMinMaxInfo(Tmessage MSG) {
        super.WMGetMinMaxInfo();
        //FIX unresolved WITH expression: UNRESOLVED.PMinMaxInfo(MSG.lparam).PDF_FIX_POINTER_ACCESS
        UNRESOLVED.ptMinTrackSize.x = 404;
        // only resizes vertically
        UNRESOLVED.ptMaxTrackSize.x = 404;
        UNRESOLVED.ptMinTrackSize.y = 303;
    }
    
    public void FormResize(TObject Sender) {
        int resizeGridHeight = 0;
        int rowsToShow = 0;
        int integralGridHeight = 0;
        
        if (delphi_compatability.Application.terminated) {
            // only resizes vertically
            return;
        }
        if (this.param == null) {
            return;
        }
        if (this.originalTdo == null) {
            return;
        }
        this.tdos.SetBounds(this.tdos.Left, 4, this.tdos.Width, this.tdos.Height);
        resizeGridHeight = this.ClientHeight - this.libraryGroupBox.Height - this.tdos.Height - 4 * 4;
        rowsToShow = resizeGridHeight / this.grid.DefaultRowHeight;
        integralGridHeight = this.grid.DefaultRowHeight * rowsToShow + this.grid.GridLineWidth * (rowsToShow - 1) + 2;
        this.grid.SetBounds(this.grid.Left, this.tdos.Top + this.tdos.Height + 4, this.grid.Width, integralGridHeight);
        this.libraryGroupBox.SetBounds(this.libraryGroupBox.Left, this.ClientHeight - this.libraryGroupBox.Height - 4, this.libraryGroupBox.Width, this.libraryGroupBox.Height);
    }
    
    public void moverClick(TObject Sender) {
        TTdoMoverForm tdoMoverForm = new TTdoMoverForm();
        int response = 0;
        
        if (this.libraryChanged) {
            response = MessageDialog("Do you want to save your changes to " + ExtractFileName(UNRESOLVED.domain.defaultTdoLibraryFileName) + chr(13) + "before you use the 3D object mover?" + chr(13) + chr(13) + "If not, they will be lost.", mtConfirmation, mbYesNoCancel, 0);
            switch (response) {
                case delphi_compatability.IDCANCEL:
                    return;
                    break;
                case delphi_compatability.IDYES:
                    this.saveTdosToLibrary();
                    break;
                case delphi_compatability.IDNO:
                    break;
        }
        tdoMoverForm = utdomove.TTdoMoverForm().create(this);
        if (tdoMoverForm == null) {
            throw new GeneralException.create("Problem: Could not create 3D object mover window.");
        }
        try {
            tdoMoverForm.ShowModal();
            this.readTdosFromFile();
            this.selectTdoAtIndex(-1);
        } finally {
            tdoMoverForm.free;
            tdoMoverForm = null;
        }
    }
    
}
