+++
title = "Building my very own reflow oven"
date = 2019-11-03
draft = true

[taxonomies]
tags = ["smd", "reflow", "oven"]
categories = ["electronics"]
+++

In this article I will discuss the build process of my very own reflow oven for [reflow-soldering][1] surface mounted components on my future PCBs.

<!-- more -->

## Components

To get started, I had to acquire the necessary parts:

* Small and cheap oven
* Thermocouple to monitor the temperature
* Thermocouple-to-Digital converter to convert the reading to digital data
* Solid state relay to electronically control the power cycle
* Micro-controller module of some sort

### Choosing the parts

Since this is going to be the cheapest possible build, being the cheapskate that I am, I will buy from a wide variety of sources.

#### Finding the cheapest oven

Since I live in Denmark, sourcing a cheap oven is going to be quite harder than compared to, for example, the US.

After going through the catalogs from the usual large hardware stores and supermarkets (or “hypermarkets” as they like to call themselves) with no good results, I tried searching on [PriceRunner][2] which is a product indexing site that indexes inventories for over 7000 shops.

I ended up settling for a small Royal Series 16 liter oven at the price of 200 DKK ($30 USD) + 100 DKK shipping ($15 USD) = 300 DKK ($45 USD) total.

{{ thumbnailed_image(path='building-reflow-oven/IMG_20191104_053613.jpg')}}


[1]: https://en.wikipedia.org/wiki/Reflow_soldering
[2]: https://www.pricerunner.dk/