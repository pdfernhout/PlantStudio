# const
clBlack = 0x000000
clMaroon = 0x000080
clGreen = 0x008000
clOlive = 0x008080
clNavy = 0x800000
clPurple = 0x800080
clTeal = 0x808000
clGray = 0x808080
clSilver = 0xC0C0C0
clRed = 0x0000FF
clLime = 0x00FF00
clYellow = 0x00FFFF
clBlue = 0xFF0000
clFuchsia = 0xFF00FF
clAqua = 0xFFFF00
clLtGray = 0xC0C0C0
clDkGray = 0x808080
clWhite = 0xFFFFFF
clCream = 0xF0FBFF
clNone = 0x1FFFFFFF
# PDF LOOK AT __ ISSUE OF clDefault BEING LONGER?
clDefault = 0x20000000
clWindow = 0x808080
clWindowFrame = 0x808080

# PDF FIX MAYBE -- empty color -- was TColor
EmptyColor = clBlack

class TPoint:
    def __init__(self, x=0L, y=0L):
        self.X = x
        self.Y = y

class TRect:
    def __init__(self, left=0L, top=0L, right=0L, bottom=0L):
        self.Left = left
        self.Top = top
        self.Right = right
        self.Bottom = bottom
        
# PDF PORT __ SHOUDL REALLY FIX THIS
MaxLongInt = 10000000L