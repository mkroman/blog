+++
title = "X-Max V3 Pro Plus Tech Dump"
date = 2024-05-25

[taxonomies]
tags = ["teardown", "x-max", "v3 pro plus"]
categories = ["electronics", "tech dump"]
+++

I recently purchased a X-Max V3 Pro Plus vaporizer, and I was hoping I could
hack it to display a different boot logo, just for fun.

In the end, I didn't achieve my goal - but I did break it open and found some
details about the device that I couldn't find elsewhere, so this is an article
that contains a dump of the information I gathered.

<!-- more -->

## Hardware

The main MCU is a `N32G031K8Q7-1`. It is a Nations Technologies Inc. `N32G031`
series controller based on an ARM Cortex-M0 with 64KB embedded flash, 8KB SRAM
in a QFN32 (4x4mm) package.

{{ thumbnailed_image(path='x-max-v3-pro-plus-tech-dump/photos/n32g031.jpg') }}


### Pinout

The populated side of the PCB has some annotated pads that are also routed to
the other side of the PCB. The `RST` corresponds to `R` pad on the backside.

### Pinout (backside)

I tried connecting to the pads on the back as they were a bit easier to get to:

{{
    thumbnailed_image(path='x-max-v3-pro-plus-tech-dump/photos/wired-backside.jpg')
    }}

There are 5 pads - `V`, `D`, `G`, `R`, `C`.

This is what I traced them to:

| Annotation | Pin # | Function     |
| ---------- | ----- | ------------ |
| V          | -     | BAT+         |
| D          | 23    | PA23 (SWDIO) |
| G          | -     | BAT-         |
| C          | 24    | PA14 (SWCLK) |
| R          | 4     | nRST (Reset) |


## Programming

### SWD

I tried to connect a SEGGER J-Link via SWD, but it wouldn't connect:

```
J-Link>connect
Device "N32G031C8" selected.
Connecting to target via SWD
Failed to attach to CPU. Trying connect under reset.
Error occurred: Could not connect to the target device.
```

SWD may be disabled in the production units.

I wanted to try and pull the `BOOT0` pin high to put in in system memory mode,
but I couldn't find an exposed pad for it, and I didn't have a soldering tip
small enough to solder directly to the QFN chip.

## Notes

Unfortunately I didn't take any top-down pictures of the board, but I've
uploaded the uncut (sorry) video capture from my microscope if you want to take
a look.

The video can be found
[here](https://pub.rwx.im/~mk/v/x-max-v3-pro-plus-uncut-microscope-footage.m4v).

## External links

* [Product Page](https://vaporshop.pl/en/5074-2554-x-max-v3-pro-plus-420vape-vaporizer-for-herbs.html) [(archived)](https://web.archive.org/web/20240525064434/https://vaporshop.pl/en/5074-2554-x-max-v3-pro-plus-420vape-vaporizer-for-herbs.html)
* [iFixit Teardown](https://www.ifixit.com/Guide/XMAX+V3+Pro+Disassembly/157413) [(archived)](https://web.archive.org/web/20240525064807/https://www.ifixit.com/Guide/XMAX+V3+Pro+Disassembly/157413)
* [N32G031 Overview](https://www.nationstech.com/en/N32G031SIC/) [(archived)](https://web.archive.org/web/20240225155901/https://www.nationstech.com/en/N32G031SIC/)
* [N32G031
  Datasheet](https://www.nationstech.com/uploadfile/file/20220907/1662539811646982.pdf) [(archived)](https://web.archive.org/web/20240511014357/https://www.nationstech.com/uploadfile/file/20220907/1662539811646982.pdf)
