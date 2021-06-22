import board
import busio
import digitalio
import adafruit_tlc5947
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
latch = digitalio.DigitalInOut(board.D5)
tlc5947 = adafruit_tlc5947.TLC5947(spi, latch)
tlc5947[20] = 2000

while True:
    tlc5947[5] = 0
