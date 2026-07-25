---
title: Cook Book
description: A desktop app for loading, browsing, and creating recipes.
order: 7
featured: true
status: Work in Progress
tags:
  - Rust
  - Tauri
  - Yew
  - WASM
links:
  - label: GitHub
    url: https://github.com/Minigrim0/cook-book
---

A desktop cookbook app built with Tauri and Yew (compiled to WASM for the UI). Recipes load from
a JSON format, with display and navigation between recipes already working, plus timers on their
own page.

Still in progress: recipe import, and splitting each ingredient line into name, quantity, and
unit via regex — which turns out to be a much messier problem than it sounds and isn't working
well yet.
