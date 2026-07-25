---
title: Home Display
description: A weather and bus-timing display running on a Raspberry Pi 3 B+ with a touchscreen.
order: 2
featured: false
status: Finished
tags:
  - Rust
  - Ratatui
  - Embedded
links:
  - label: GitHub
    url: https://github.com/Minigrim0/HomeDisplay
---

A small always-on display at home showing local weather and upcoming bus timings, running on a
Raspberry Pi 3 B+ with a touchscreen.

The first version used Tauri with the matchbox window manager to keep things lightweight, but it
tended to freeze after a few hours of uptime. It got rebuilt on ratatui instead — a terminal UI
runs happily forever on a Pi and skips the whole windowing-stack failure mode entirely.

Finished and running, though there's always room to add more panels.
