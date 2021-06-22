FROM		raspbian/stretch:latest

COPY		./water.py /

RUN		\
		# Update to latest
		apt -y update && \
		apt -y upgrade && \
		# Install general packages
		apt -y install python3 python3-pip python3-rpi.gpio && \
		pip3 install adafruit-ads1x15 && \
		echo "Build complete." 

ENTRYPOINT	python3 water.py
