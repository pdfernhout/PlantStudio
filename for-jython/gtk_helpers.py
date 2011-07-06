##########################  GUI helper functions ############################
# GTK version

import pygtk
pygtk.require('2.0')
import gtk

###### MAIN WINDOW AND PACKING SIMPLE WIDGETS #############

def MakeWindow(name, x=500, y=500):
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_default_size(x, y)
    window.set_title(name)
    window.connect("destroy", gtk.main_quit)
    return window
    
def ShowWindow(window):
    # according to: http://gtk.php.net/manual1/en/html/gtk.gtkwidget.method.show_all.html 
    # "The extent to which it 'sees' children is system-dependant"
    # window.show_all()
    window.show()
        
def MakeButton(box, name, clickedMethod, data=None):
    button = gtk.Button(name)
    if clickedMethod:
        if data == None:
            button.connect("clicked", clickedMethod)
        else:
            button.connect("clicked", clickedMethod, data)             
    box.pack_start(button, False, True, 2)
    button.show()
    return button

def MakeVerticalBox(parent, homogeneous=False):
    vbox = gtk.VBox(homogeneous, 2)
    if parent.__class__ is gtk.Window:
        parent.add(vbox)
    else:
        parent.pack_start(vbox, False, True, 2) 
    vbox.show()
    return vbox    
             
def MakeHorizontalBox(parent, homogeneous=True):
    hbox = gtk.HBox(homogeneous, 2)
    if parent.__class__ is gtk.Window:
        parent.add(hbox)
    else:
        parent.pack_start(hbox, False, True, 2)
    hbox.show()
    return hbox
            
def PackBox(box, widget, expand=1, border=2):
    box.pack_start(widget, expand=expand, fill=True, padding=2)
    widget.show()
    
def InvalidateWidget(widget):
    widget.queue_draw()
    
################# LIST #################

import gobject

def MakeList(parent, title, selectionChangedMethod):
    scrolled_window = gtk.ScrolledWindow()
    #scrolled_window.set_usize(250, 150)
    if parent.__class__ is gtk.Window:
        parent.add(scrolled_window)
    else:
        parent.pack_start(scrolled_window, True, True, 2)
    scrolled_window.show()
    
    store = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)
    treeview = gtk.TreeView(store)
    column = gtk.TreeViewColumn(title)
    treeview.append_column(column)
    cell = gtk.CellRendererText()
    column.pack_start(cell, True)
    column.add_attribute(cell, 'text', 0)
         
    scrolled_window.add_with_viewport(treeview)
    treeview.show()
    if selectionChangedMethod:
        treeview.connect("cursor-changed", selectionChangedMethod)
    return treeview
    
def FillList(list, nameValuePairs):
    store = list.get_model()
    store.clear()
    for name, value in nameValuePairs:
        iter = store.append()
        store.set_value(iter, 0, name)
        store.set_value(iter, 1, value)
        
def GetListSelection(list, index=0):
    path, column = list.get_cursor()
    if path == None:
        return None
    store = list.get_model()
    treeiter = store.get_iter(path)
    result = store.get_value(treeiter, index)
    return result

############# GRID ###################


    
############### DIALOGS ###############

def AskYesNoDialog(parent, question, title=None):
    if title == None:
        title = question
    msgbox = gtk.MessageDialog(parent, buttons=gtk.BUTTONS_YES_NO, flags=gtk.DIALOG_MODAL, type=gtk.MESSAGE_QUESTION, message_format=question)
    msgbox.set_title(title)
    result = msgbox.run()
    msgbox.destroy()
    if result == gtk.RESPONSE_YES:
        return True
    else:
        return False
    
# example fileTypes = ["*.bmp", "*.png"]
def ChooseFile(parent, fileTypesName="Data", fileTypes=None):
    dialog = gtk.FileChooserDialog("Open..",
                               parent,
                               gtk.FILE_CHOOSER_ACTION_OPEN,
                               (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    
    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    dialog.add_filter(filter)
    
    if fileTypes:
        filter = gtk.FileFilter()
        filter.set_name(fileTypesName)
        for fileType in fileTypes:
            filter.add_pattern(fileType)
            #filter.add_mime_type("image/png")
        dialog.add_filter(filter)
        dialog.set_filter(filter)
    
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        result = dialog.get_filename()
    elif response == gtk.RESPONSE_CANCEL:
        result = None
    dialog.destroy()
    return result

############# DRAWING #####################

def delphi_to_gdk_color(window, value):
    b = (value & 0xff0000) >> 8
    g = (value & 0x00ff00)
    r = (value & 0x0000ff) << 8
    #gtkColor = map.alloc_color("red") # light red
    #gtkColor = gtk.gdk.Color(r, g, b) # DOESN"T WORK
    if window.__class__ != gtk.gdk.Pixmap:
        map = window.get_colormap()
        gtkColor = map.alloc_color(r, g, b)
    else:
        window = window.widget
        #gtkColor = gtk.gdk.Color(r, g, b)
        map = window.get_colormap()
        gtkColor = map.alloc_color(r, g, b)
    return gtkColor

def DrawRectangle(widget, gc, rect, penWidth, penColor, brushColor, filled=1):
    gc.set_line_attributes(penWidth, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)
    gc.set_fill(gtk.gdk.SOLID)
    penColor = delphi_to_gdk_color(widget, penColor)
    brushColor = delphi_to_gdk_color(widget, brushColor)
    gc.set_foreground(brushColor)
    widget.draw_rectangle(gc, filled, rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top)

def MeasureTextWidth(widget, gc, text):
    # PDF PORT FIX THIS!!!!
    return len(text) * 12

def MeasureTextHeight(widget, gc, text):
    # PDF PORT FIX THIS!!!!
    return 12

def DrawText(widget, gc, textDrawRect, text, font, brushColor):
    brushColor = delphi_to_gdk_color(widget, brushColor)
    # deprecated -- should use pango layout
    # http://www.moeraki.com/pygtktutorial/pygtk2tutorial/sec-DrawingMethods.html
    gc.set_foreground(brushColor)
    widget.draw_text(font, gc, textDrawRect.left, textDrawRect.top, text)
