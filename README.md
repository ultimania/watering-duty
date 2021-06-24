# sense-and-water
This image is to establish automatic watering system to plant by Raspberry Pi.

# Prerequisites
* Raspberry Pi
* i2c is available, which means below.
  * Below lines are added to /boot/config.txt
    * dtparam=i2c1=on
    * dtparam=spi=on
  * i2c_bcm2835 and i2c-dev modules are loaded.
* GPIO is available.
  * 4 of BCM is 7th pin on board.
* Below packages are available.
  * Adafruit-ADS1x15 (by python3-pip)
  * python3-rpi.gpio (by apt if you want to run on docker container)

# To build image
sudo docker build -t sense-and-water-image .

# To run container
sudo docker run -dit --device=/dev/i2c-1:/dev/i2c-1 --device=/dev/gpiomem:/dev/gpiomem sense-and-water-image
