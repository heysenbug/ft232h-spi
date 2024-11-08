import board
import busio
import digitalio
import time

# Initialize the FT232H SPI interface
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.C0)  # Chip select, can be any GPIO
cs.direction = digitalio.Direction.OUTPUT

def spi_init():
    # Set up SPI settings
    cs.value = True  # Chip select inactive (high)
    spi.try_lock()
    spi.configure(baudrate=200000, phase=0, polarity=0)
    spi.unlock()

def send_data(data):
    """Function to send data via SPI to nRF9160"""
    # Convert data to bytes if it’s not already
    if isinstance(data, str):
        data = data.encode()  # Convert string to bytes

    # Ensure SPI is locked for data transaction
    bytes_read = bytearray(1)
    spi.try_lock()
    cs.value = False  # Activate chip select (low)
    spi.write(data)  # Write data to nRF
    ret = spi.readinto(bytes_read)
    cs.value = True   # Deactivate chip select (high)
    spi.unlock()
    print(f'<- TX: {int.from_bytes(data)}')
    print(f'-> RX: {int.from_bytes(bytes_read)}')

    return bytes_read

def send_loop():
    print("Executing main loop")
    buf = bytearray([0x01])
    while True:
        buf = send_data(buf)
        buf[0] = (buf[0] + 1) % 256
        time.sleep(1)


if __name__ == '__main__':
    print("Initializing SPI")
    spi_init()
    send_loop()

