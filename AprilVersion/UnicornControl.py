import unicornhat as uh

uh.set_layout(uh.HAT)
uh.brightness(0.5)
uh.rotation(270)
width,height=uh.get_shape()

leftArrow = [
     "   X    "
    ,"  XX    "
    ," XXXXXXX"
    ,"XXXXXXXX"
    ," XXXXXXX"
    ,"  XX    "
    ,"   X    "
    ,"b    b  "
    ]
rightArrow = [
     "    X   "
    ,"    XX  "
    ,"XXXXXXX "
    ,"XXXXXXXX"
    ,"XXXXXXX "
    ,"    XX  "
    ,"    X   "
    ,"    bb  "
    ]

dleftArrow = [
     "XXXXXX  "
    ,"XXXXXXX "
    ,"XXXXX   "
    ,"XX XXX  "
    ," X  XXX "
    ,"     XXX"
    ,"      XX"
    ," b   b  "
    ]

drightArrow = [
     "  XXXXXX"
    ," XXXXXXX"
    ,"   XXXXX"
    ,"  XXX XX"
    ," XXX  X "
    ,"XXX     "
    ,"XX      "
    ,"   b b  "
    ]

straightArrow = [
     "   XX   "
    ,"  XXXX  "
    ," XXXXXX "
    ,"XXXXXXXX"
    ,"  XXXX  "
    ,"  XXXX  "
    ,"  XXXX  "
    ,"  b  b  "
    ]

noGatesImg = [
     "rr    rr"
    ," rr  rr "
    ,"  rrrr  "
    ,"   rr   "
    ,"  rrrr  "
    ," rr  rr "
    ,"rr    rr"
    ,"     bb "
    ]

def displayArrow(pic):
    for h in range(height):
        for w in range(width):
            chr = pic[h][w]
            if chr == ' ':
                uh.set_pixel(w, h, 0, 0, 0)
            elif chr == 'b':
                uh.set_pixel(w,h,0,0,255)
            elif chr == 'r':
                uh.set_pixel(w,h,255,0,0)
            else:
                uh.set_pixel(w, h, 0, 255, 0)
    uh.show()

def left():
    displayArrow(dleftArrow)
    print("Left")

def hleft():
    displayArrow(leftArrow)
    print("Hard left")
    
def right():
    displayArrow(drightArrow)
    print("Right")

def hright():
    displayArrow(rightArrow)
    print("Hard right")
    
def straight():
    uh.rotation(270)
    displayArrow(straightArrow)
    print("Straight")
def noGates():
    displayArrow(noGatesImg)
    print("No Gates")