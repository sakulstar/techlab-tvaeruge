import network
import asyncio
import socket
import time
import random
from machine import Pin
from neopixel import Neopixel

good = [
    "banan",
    "aeble",
    "salat",
    "insekter"
]

bad = [
    "kylling",
    "oksekod"
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
random_good = "hello!"
random_bad = "fuck you"
while_loop = True

def gen_random(list, isGood):
    global random_good, random_bad
    while True:
        random_var = random.choice(list)
        
        if isGood == True and random_var != random_good:
            print("Good:", random_var, "-", random_good)
            random_bad = random_var
            return str(random_good)
        elif isGood == False and random_var != random_bad:
            print("Bad:", random_var, "-", random_bad)
            random_bad = random_var
            return str(random_bad)


def gen_question():
    good_choice = gen_random(good, True)
    bad_choice = gen_random(bad, False)

    html1 = f"""
        <div>
            <form action="./good">
                <input type="submit" value="{good_choice}" />
            </form>
        </div>
        <div>
            <form action="./bad">
                <input type="submit" value="{bad_choice}" />
            </form>
        </div>
    """
    html2 = f"""
        <div>
            <form action="./bad">
                <input type="submit" value="{bad_choice}" />
            </form>
        </div>
        <div>
            <form action="./good">
                <input type="submit" value="{good_choice}" />
            </form>
        </div>
    """

    return str(random.choice([html1, html2]))

# HTML webpage
def webpage():
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            {gen_question()}
            <form action="./good">
                <input type="submit" value="good" />
            </form>
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
        pixels = Neopixel(numpix, 0, 28, "GRB")
        pixels.brightness(10)
        pixels.fill(green)
        pixels.show()
    elif request == '/bad?':
        pixels = Neopixel(numpix, 0, 28, "GRB")
        pixels.brightness(10)
        pixels.fill(red)
        pixels.show()
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