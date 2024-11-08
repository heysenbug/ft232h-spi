# Adafruit FT232H SPI

Simple test to send and receive a byte using FT232H as SPI master


## Prerequisites

You can find the full installation guide [here](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/setup)

### Python Environment

ft232-spi has been tested with python 3.12
```
git clone https://github.com/heysenbug/ft232-spi
cd ft232-spi
python3 -m venv venv
. venv/bin/activate
```

### Pyftdi

Full instructions for to install pyftdi are (here)[https://github.com/eblot/pyftdi/blob/master/pyftdi/doc/installation.rst]
Included below are snippets

```
pip install pyftdi
```

#### Mac OSX

```
brew install libusb
```

#### Linux

```
sudo apt-get install libusb-1.0

# Add udev rules
cat << EOF > /etc/udev/rules.d/11-ftdi.rules
# FT232AM/FT232BM/FT232R
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6001", GROUP="plugdev", MODE="0664"
# FT2232C/FT2232D/FT2232H
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6010", GROUP="plugdev", MODE="0664"
# FT4232/FT4232H
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6011", GROUP="plugdev", MODE="0664"
# FT232H
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6014", GROUP="plugdev", MODE="0664"
# FT230X/FT231X/FT234X
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6015", GROUP="plugdev", MODE="0664"
# FT4232HA
SUBSYSTEM=="usb", ATTR{idVendor}=="0403", ATTR{idProduct}=="6048", GROUP="plugdev", MODE="0664"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger
```

If you user isn't part of the `plugdev` group already
```
sudo adduser $USER plugdev
newgrp plugdev
```

### Circuit Python

```
pip install adafruit-blinka
```

## Test Circuit Python

You'll have to export `BLINKA_FT232H` to siganl circuitpython that we have this device
```
export BLINKA_FT232H=1
```

Launch python interactive shell and execute the following commands
```
python
```

You'll see the SPI related pins printed out
```
import board
dir(board)
```

Query FTDI devices attached
```
from pyftdi.ftdi import Ftdi
Ftdi().open_from_url('ftdi:///?')
```

If none are detection then check the main guide for troublshooting instrcutions