import time
from machine import Pin, UART
from dfplayer import Player
from neopixel import Neopixel
import PicoRobotics

# Motor
motorIsOn = False

# Neopixel
numpix = 24

yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

val = orange

# dfplayer
pico_uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
pico_busy = Pin(28)
player = Player(uart=pico_uart0, busy_pin = pico_busy, volume=1.0)
player.awaitconfig()
player.awaitvolume()

# Neopixel initialization
pixels = Neopixel(numpix, 0, 28, "GRB")

# Main while loop
while True:
    for i in range(5):
        player.play(1,i + 1)
        pixels.brightness(25)
        pixels.fill(val)
        pixels.show()
        board = PicoRobotics.KitronikPicoRobotics()
        if motorIsOn == True:
            board.motorOff(1)
            motorIsOn = False
        else:
            motorIsOn = True
            board.motorOn(1, "r", 100)
        if val == orange:
            val = red
        else:
            val = orange
        time.sleep(1)