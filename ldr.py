import machine
import utime

ldr = machine.ADC(26)

while True:
	print(ldr.read_u16())
	utime.sleep(1)