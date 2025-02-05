import sys
import PicoRobotics
import utime

while True:
    try:
        board = PicoRobotics.KitronikPicoRobotics()

        board.motorOn(1,"r",100)
        print("started motor")
        utime.sleep_ms(1000)
        board.motorOff(1)
        print("stopped motor")
        utime.sleep_ms(1000)
    except OSError as e:
        print('Failed to start motor:', e)
        sys.exit()