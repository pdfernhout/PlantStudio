import udrawingsurface
import gtk

from gtk_helpers import *
    
class GTKDrawingSurface(udrawingsurface.KfDrawingSurface):
    def drawingContextDrawSolidLine(self, x1, y1, x2, y2, width, color):
        window, gc = self.drawingContext
        gtkColor = delphi_to_gdk_color(window, color)
        gc.set_foreground(gtkColor)
        gc.set_fill(gtk.gdk.SOLID)
        gc.set_line_attributes(width, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)
        window.draw_line(gc, x1, y1, x2, y2)

    def drawingContextDrawTriangle(self, points, interiorColor, edgeColor, edgeWidth, drawFilled, vertextPointColor=None):
        window, gc = self.drawingContext
        gtkEdgeColor = delphi_to_gdk_color(window, edgeColor)
        
        gtkPoints = []
        for i in range(0, 3):
            point = points[i]
            gtkPoints.append((point.X, point.Y))
                   
        gc.set_line_attributes(edgeWidth, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)
       
        if drawFilled:
            gtkInteriorColor = delphi_to_gdk_color(window, interiorColor)
            gc.set_foreground(gtkInteriorColor)
            window.draw_polygon(gc, 1, gtkPoints)
            if interiorColor != edgeColor:
                gc.set_foreground(gtkEdgeColor)
                window.draw_polygon(gc, 0, gtkPoints)
        else:
            gc.set_foreground(gtkEdgeColor)
            window.draw_polygon(gc, 0, gtkPoints)
        
        if vertextPointColor != None:
            gtkVertextPointColor = delphi_to_gdk_color(window, vertextPointColor)
            radius = self.circlePointRadius
            gc.set_foreground(gtkVertextPointColor)
            for i in range(0, 3):
                point = points[i]
                self.pane.Ellipse(point.X - radius, point.Y - radius, point.X + radius, point.Y + radius)

