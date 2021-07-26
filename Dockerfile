FROM    raspbian/stretch:latest

RUN			\
			apt -y update && \
			apt -y upgrade && \
			# Install general packages
			apt -y install python3 python3-pip python3-rpi.gpio && \
			pip3 install adafruit-ads1x15 requests

ENTRYPOINT	python3 /opt/water.py
