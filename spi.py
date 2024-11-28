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
    spi.configure(baudrate=100000, phase=0, polarity=0)
    spi.unlock()

def send_data_nrf9160(data):
    """Function to send data via SPI to nRF9160"""
    # Convert data to bytes if it’s not already
    if isinstance(data, str):
        data = data.encode()  # Convert string to bytes

    # Ensure SPI is locked for data transaction
    bytes_read = bytearray(1)
    spi.try_lock()
    cs.value = False  # Activate chip select (low)
    time.sleep(0.1)  # Small delay for CS setup

    spi.write(data)  # Write data to nRF
    spi.readinto(bytes_read)

    time.sleep(0.1)  # Small delay before CS release
    cs.value = True   # Deactivate chip select (high)
    spi.unlock()

    print(f'<- TX: {int.from_bytes(data)}')
    print(f'-> RX: {int.from_bytes(bytes_read)}')

    return bytes_read

def send_data_panda(data):
    '''Function to get version string from panda through SPI'''
    # Prepare the data
    tx_buf = data
    rx_buf = bytearray(24)
    if isinstance(data, str):
        tx_buf = data.encode(encoding='ascii')

    # Prepare SPI for transfer
    spi.try_lock()
    cs.value = False
    time.sleep(0.1)  # Small delay for CS setup

    # Write/read data
    spi.write(tx_buf)
    time.sleep(0.01)
    spi.readinto(rx_buf)

    time.sleep(0.1)  # Small delay before CS release
    cs.value = True
    spi.unlock()

    print(f'TX: {[hex(byte) for byte in tx_buf]}')
    print(f'RX: {[hex(byte) for byte in rx_buf]}')


def send_loop_nrf9160():
    print("Executing main loop")
    buf = bytearray(1)
    while True:
        send_data_nrf9160(buf)
        input('Press Any Key to send another frame')

def send_loop_panda():
    print("Executing main loop")
    buf = "VERSION".encode(encoding='ascii')
    while True:
        send_data_panda(buf)
        key = input('Press Any Key to send another frame or q to quit [continue]: ')
        if key == 'q':
            return


if __name__ == '__main__':
    print("Initializing SPI")
    spi_init()
    send_loop_panda()
    # send_loop_nrf9160()
    print('DONE.')

