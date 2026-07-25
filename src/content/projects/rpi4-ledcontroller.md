---
title: RPi4 LED Controller
description: An MQTT-controlled LED strip animation system, running the lights around a 3D printer.
order: 3
featured: false
status: Finished
tags:
  - Rust
  - MQTT
  - Embedded
  - IoT
links:
  - label: GitHub
    url: https://github.com/Minigrim0/rpi4-ledcontroller
---

Controls an LED strip wrapped around a 3D printer, running on a Raspberry Pi 4. It listens on an
MQTT channel for commands and plays back animations on request, so lighting state (idle, printing,
error, done) can be driven from whatever else is watching the printer without touching the
controller itself.

Finished and in daily use, with room to grow the animation set.
