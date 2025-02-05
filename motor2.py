import PicoRobotics
import utime

board = PicoRobotics.KitronikPicoRobotics()

while True:
    board.motorOn(1,"r",100)
    utime.sleep_ms(1000)
    board.motorOff(1)
    utime.sleep_ms(1000)