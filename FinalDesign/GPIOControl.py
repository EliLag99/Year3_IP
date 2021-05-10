import RPi.GPIO as gpio

HR = 19
R = 13
S = 6
L = 5
HL = 0

ON = 10
NG = 9
NA = 11

gpio.setmode(gpio.BCM)
gpio.setup(0, gpio.OUT)
gpio.setup(5, gpio.OUT)
gpio.setup(6, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
gpio.setup(10, gpio.OUT)
gpio.setup(9, gpio.OUT)
gpio.setup(11, gpio.OUT)

def reset():
    gpio.output(HR, gpio.LOW)
    gpio.output(R, gpio.LOW)
    gpio.output(S, gpio.LOW)
    gpio.output(L, gpio.LOW)
    gpio.output(HL, gpio.LOW)
    gpio.output(NG, gpio.LOW)
    gpio.output(NA, gpio.LOW)

def hleft():
    reset()
    gpio.output(HL, gpio.HIGH)
def left():
    reset()
    gpio.output(L, gpio.HIGH)
def straight():
    reset()
    gpio.output(S, gpio.HIGH)
def right():
    reset()
    gpio.output(R, gpio.HIGH)
def hright():
    reset()
    gpio.output(HR, gpio.HIGH)
def noGates():
    reset()
    gpio.output(NG, gpio.HIGH)
def on():
    gpio.output(ON, gpio.HIGH)
def off():
    gpio.output(ON, gpio.LOW)

