+++
title = "Teardown of the Xiaomi Aqara Temperature, Humidity and Pressure sensor"
date = 2020-04-23

[taxonomies]
tags = ["teardown", "xiaomi", "aqara", "temperature", "pressure", "humidity", "sensor"]
categories = ["teardown", "electronics"]
+++

Let's take a quick peak at what makes the Xiaomi Aqara Temperature sensor tick,
and get an overview of some of the available test pads

<!-- more --> 

## Product information

The Aqara Temperature, Humidity and Pressure sensor is a small battery-powered
Zigbee sensor that sends periodic information to a central Zigbee hub.

The official claim is that this device will run off of a single CR2032 battery
for up to 2 years.

{{
  thumbnailed_image(path='aqara-temperature-humidity-pressure-sensor-teardown/pictures/aqara-temperature-front.jpg')
  }}

## Opening the clam shell

The unit is held together with plastic clips in a clam-shell construction. The
easiest way to get it apart that I've found is to use a box knife on one of the
corners to get some leverage, and then use a thin metal prying tool to break it
open.

{{
  thumbnailed_image(path='aqara-temperature-humidity-pressure-sensor-teardown/pictures/prying-open.jpg')
  }}

The unit is comprised of 4 parts - the clam shells, a button and the PCB.

{{
  thumbnailed_image(path='aqara-temperature-humidity-pressure-sensor-teardown/pictures/parts.jpg')
  }}

## PCB close-ups

I saved images of each side of the PCB

{{
  thumbnailed_image(path='aqara-temperature-humidity-pressure-sensor-teardown/pictures/front-pcb.png')
  }}

{{
  thumbnailed_image(path='aqara-temperature-humidity-pressure-sensor-teardown/pictures/back-pcb.png')
  }}

The main microcontroller is an [NXP JN5169][1] which contains a 32-bit RISC
processor, 512 kB embedded flash, 32 kB RAM and 4 kB EEPROM memory.

The temperature/humidity sensor is an [Sensiron SHT30][2] which has a typical
%RH resolution of ±2 at 10-90% RH and ±0.3°C in the range of 0-65°C

{{
  thumbnailed_image(path='aqara-temperature-humidity-pressure-sensor-teardown/pictures/sht30.jpg')
  }}

Since the SHT30 doesn't feature integrated pressure sensing, there's also this
`6A2` sensor which I haven't been able to identify.

{{
  thumbnailed_image(path='aqara-temperature-humidity-pressure-sensor-teardown/pictures/ga2.jpg')
  }}

### Tracing out some test pads

I went ahead and traced out some of the many test pads on the PCB, including the
ones needed to put it into serial programming mode. I haven't attempted to see
if it's possible to do so, so I don't know if it's locked or not.

I made an annotated image with the pads I identified after a quick 5 minute
tracing:

{{
  thumbnailed_image(path='aqara-temperature-humidity-pressure-sensor-teardown/pictures/front-pcb-annotated.jpg')
  }}


[1]:
https://www.nxp.com/products/wireless/zigbee/zigbee-and-ieee802-15-4-wireless-microcontroller-with-512-kb-flash-32-kb-ram:JN5169
[2]:
https://www.sensirion.com/en/environmental-sensors/humidity-sensors/digital-humidity-sensors-for-various-applications/
