---
title: Wave Function Collapse
description: A from-scratch implementation of the Wave Function Collapse procedural generation algorithm.
order: 6
featured: false
status: Finished
tags:
  - Python
  - Procedural Generation
links:
  - label: GitHub
    url: https://github.com/Minigrim0/WaveFunctionCollapse
---

Found a demo of Wave Function Collapse online and wanted to understand it well enough to
reproduce it — the algorithm generates locally-coherent output (textures, tilemaps, ...) by
treating generation as a constraint-propagation problem, collapsing one cell's possibilities at a
time based on its neighbors.

Finished as a self-contained implementation.
