import time
from machine import Pin, UART
from dfplayer import Player

pico_uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
pico_busy = Pin(28)
player = Player(uart=pico_uart0, busy_pin = pico_busy, volume=1.0)
player.awaitconfig()
player.awaitvolume()

'''while True:
    #print("Playing? {}".format(player.playing()))
    for i in range(5):
        player.play(1,i + 1)
        time.sleep(1)
'''
player.play(1,12)
    