import udrawingsurface
    
from swing_helpers import *

from java.awt.geom import Line2D
from java.awt import BasicStroke

class SwingDrawingSurface(udrawingsurface.KfDrawingSurface):
    def drawingContextDrawSolidLine(self, x1, y1, x2, y2, width, color):
        window, gc = self.drawingContext
        theColor = delphi_to_gdk_color(window, color)
        gc.color = theColor
        #gc.set_fill(gtk.gdk.SOLID)
        #gc.set_line_attributes(width, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)
        #gc.drawLine(x1, y1, x2, y2)
        line = Line2D.Double(x1, y1, x2, y2)
        gc.setStroke(BasicStroke(width))
        gc.draw(line)
        #gc.drawLine(x1, y1, x2, y2)

    def drawingContextDrawTriangle(self, points, interiorColor, edgeColor, edgeWidth, drawFilled, vertextPointColor=None):
        window, gc = self.drawingContext
        theEdgeColor = delphi_to_gdk_color(window, edgeColor)
        
        polygon = Polygon()
        for i in range(0, 3):
            point = points[i]
            polygon.addPoint(point.X, point.Y)
                   
        #gc.set_line_attributes(edgeWidth, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_BUTT, gtk.gdk.JOIN_MITER)
       
        if drawFilled:
            gtkInteriorColor = delphi_to_gdk_color(window, interiorColor)
            gc.color = gtkInteriorColor
            gc.fillPolygon(polygon)
            if interiorColor != edgeColor:
                gc.color = gtkEdgeColor
                gc.drawPolygon(polygon)
        else:
            gc.color = gtkEdgeColor
            gc.drawPolygon(polygon)
        
        if vertextPointColor != None:
            gtkVertextPointColor = delphi_to_gdk_color(window, vertextPointColor)
            radius = self.circlePointRadius
            gc.color = gtkVertextPointColor
            for i in range(0, 3):
                point = points[i]
                gc.fillOval(point.X - radius, point.Y - radius, point.X + radius, point.Y + radius)

