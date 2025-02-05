import time
import sys
from neopixel import Neopixel

numpix = 24

pixels = Neopixel(numpix, 0, 28, "GRB")
yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

pixels.brightness(0)
pixels.show()
sys.exit()