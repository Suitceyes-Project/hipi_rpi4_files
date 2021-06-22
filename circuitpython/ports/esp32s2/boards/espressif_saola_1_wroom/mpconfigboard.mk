USB_VID = 0x239A
USB_PID = 0x80A8
USB_PRODUCT = "Saola 1 w/WROOM"
USB_MANUFACTURER = "Espressif"

INTERNAL_FLASH_FILESYSTEM = 1
LONGINT_IMPL = MPZ

# The default queue depth of 16 overflows on release builds,
# so increase it to 32.
CFLAGS += -DCFG_TUD_TASK_QUEUE_SZ=32

CIRCUITPY_ESP_FLASH_MODE=dio
CIRCUITPY_ESP_FLASH_FREQ=40m
CIRCUITPY_ESP_FLASH_SIZE=4MB

CIRCUITPY_MODULE=wroom
