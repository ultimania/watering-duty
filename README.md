# sense-and-water
This image is to establish automatic watering system to plant by Raspberry Pi.

# Prerequisites
* Raspberry Pi
* i2c is available, which means below.
  * Below lines are added to /boot/config.txt
    * dtparam=i2c1=on
    * dtparam=spi=on
    * device_tree_param=i2c1=on
    * device_tree_param=spi=on
  * i2c_bcm2835 and i2c-dev modules are loaded.
* GPIO is available.
  * 4 of BCM is 7th pin on board.

# To build image
sudo docker build -t sense-and-water-image .

# To run container
sudo docker run -dit --device=/dev/i2c-1:/dev/i2c-1 --device=/dev/gpiomem:/dev/gpiomem sense-and-water-image
