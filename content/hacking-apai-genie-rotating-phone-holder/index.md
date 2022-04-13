+++
title = "Hacking the Apai Genie Rotating Phone Holder"
date = 2021-05-04
draft = true

[taxonomies]
tags = ["teardown", "apai", "genie", "rotating", "phone", "holder", "qmcx",
        "trackercamera"]
categories = ["teardown", "electronics"]
+++

Desperate for some new hardware to hack, I came across this 360° rotating camera
mount while shopping. It is a bluetooth connected and app controlled phone holder,
meant to be used for face tracking.

All of the smarts are done in the app - featuring tensorflow face model
recognition, tracking, etc.

I, of course, never wanted to use the app - so instead of launching the app, I
copied it to my computer and disassembled it. In this article I will go through
my discoveries about how it communicates with the device.

<!-- more --> 

## Product information

{{ thumbnailed_image(path='hacking-apai-genie-rotating-phone-holder/360-grader-tracker.jpg') }}

The device itself is massively rebranded, but I think they all rely on the same
mobile application, which seems to be developed by a company called "qmxc"
(qmxc.com is referenced all over in their sources.)

Here's a couple of product listings for the device:


