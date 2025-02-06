import network
import asyncio
import socket
import time
import random
from machine import Pin, UART
from neopixel import Neopixel
from dfplayer import Player

good = [
    "banan",
    "aeble",
    "salat",
    "insekter"
]

bad = [
    "kylling",
    "oksekod",
]

# wifi
ssid = 'lo-def173'
password = 'starhotspot'

# on board LED
led = machine.Pin('LED', machine.Pin.OUT)

# Vars
numpix = 24
green = (0, 255, 0)
red = (255, 0, 0)

# dfplayer
pico_uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
pico_busy = Pin(28)
player = Player(uart=pico_uart0, busy_pin = pico_busy, volume=1.0)

def led_color(color):
    pixels = Neopixel(numpix, 0, 28, "GRB")
    pixels.brightness(10)
    pixels.fill(color)
    pixels.show()

def play_sound(sound1, sound2):
    player.awaitconfig()
    player.awaitvolume()
    player.play(sound1, sound2)


def gen_question():
    html1 = f"""
        <div>
            <form action="./good" style="margin-right: 0.25rem;">
                <input class="qustion_btn" type="submit" value="{random.choice(good)}" />
            </form>
        </div>
        <div>
            <form action="./bad">
                <input class="qustion_btn" type="submit" value="{random.choice(bad)}" />
            </form>
        </div>
    """
    html2 = f"""
        <div>
            <form action="./bad" style="margin-right: 0.25rem;">
                <input class="qustion_btn" type="submit" value="{random.choice(bad)}" />
            </form>
        </div>
        <div>
            <form action="./good">
                <input class="qustion_btn" type="submit" value="{random.choice(good)}" />
            </form>
        </div>
    """

    return str(random.choice([html1, html2]))

# HTML webpage
def webpage():
    style = """
    <style>
        .main_div {
            flex-direction: row; 
            display: flex;
            position: fixed;
            top: 50%;
            left: 50%;
            -webkit-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
        } 
        .qustion_btn {
            padding-left: 2rem; 
            padding-right: 2rem; 
            padding-bottom: 1rem; 
            padding-top: 1rem;
            background: white;
            border-radius: 0.75rem;
            border: 0rem;
        }
    </style>
    """

    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            {style}
        </head>
        <body style="--tw-bg-opacity: 1; background-color: rgba(245, 158, 11, var(--tw-bg-opacity));">
            <div class="main_div">
                {gen_question()}
            <div>
        </body>
        </html>
        """
    return str(html)

# init wifi
def init_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Connect to your network
    wlan.connect(ssid, password)
    # Wait for Wi-Fi connection
    connection_timeout = 10
    while connection_timeout > 0:
        print(wlan.status())
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        print('Waiting for Wi-Fi connection...')
        time.sleep(1)
    # Check if connection is successful
    if wlan.status() != 3:
        print('Failed to connect to Wi-Fi')
        return False
    else:
        print('Connection successful!')
        network_info = wlan.ifconfig()
        print('IP address:', network_info[0])
        return True

# async function to handle client requests
async def handle_client(reader, writer):
    global state
    
    print("Client connected")
    request_line = await reader.readline()
    print('Request:', request_line)
    
    # skip HTTP request headers
    while await reader.readline() != b"\r\n":
        pass
    
    request = str(request_line, 'utf-8').split()[1]
    print('Request:', request)
    
    # process request and update vars
    if request == '/good?':
        led_color(green)
        play_sound(1,1)
    elif request == '/bad?':
        led_color(red)
        play_sound(1,8)
    elif request == '/ledOn?':
        print('led on')
        led.value(1)
    elif request == '/ledOff?':
        print('led off')
        led.value(0)

    # generate HTML response
    response = webpage()  

    # send HTTP response and disconnect client
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)
    await writer.drain()
    await writer.wait_closed()
    print('Client Disconnected')
    
async def blink_led():
    while True:
        led.value(1)
        await asyncio.sleep(2)
        led.value(0)
        await asyncio.sleep(2)

async def main():    
    if not init_wifi(ssid, password):
        print('Exiting program.')
        return
    
    # Start the server and run the event loop
    print('Setting up server')
    server = asyncio.start_server(handle_client, "0.0.0.0", 80)
    asyncio.create_task(server)
    #asyncio.create_task(blink_led())

    while True:
        await asyncio.sleep(5)
        

# init event loop
loop = asyncio.get_event_loop()
# create task to run main func
loop.create_task(main())

try:
    # run event loop forever
    loop.run_forever()
except Exception as e:
    print('Error occured: ', e)
    led.value(0)
except KeyboardInterrupt:
    print('Program Interrupted by the user')
    led.value(0)