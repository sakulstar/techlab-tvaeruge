import time
from neopixel import Neopixel

numpix = 24

pixels = Neopixel(numpix, 0, 28, "GRB")
yellow = (255, 100, 0)
orange = (255, 50, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
while True:
	pixels.brightness(100)
	pixels.fill(orange)
	pixels.show()
	time.sleep(1)
	pixels.fill(red)
	pixels.show()
	time.sleep(1)