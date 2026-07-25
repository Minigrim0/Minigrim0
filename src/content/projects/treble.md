---
title: Treble
description: A frontend-agnostic Rust core library for real-time audio synthesis.
order: 1
featured: true
status: Work in Progress
tags:
  - Rust
  - Audio
  - DSP
  - Real-time systems
  - CPal
links:
  - label: GitHub
    url: https://github.com/Minindustry/treble-core
---

Treble isn't a synthesizer app, it's the engine underneath one. It's a composable set of DSP
primitives — generators, envelopes, filters, and a node graph — sitting behind a lock-free,
real-time-safe audio pipeline. The same engine drops into a GUI, a CLI, or a test harness
without changes, because nothing in the core cares what's calling it.

## Thread model

Three roles run concurrently:

- **App** (caller thread) — creates the `App`, loads instruments, sends `AudioMessage`s to the
  render thread, and receives `BackendEvent`s back.
- **Render** (`audio-render` thread) — runs `system.run()` once per block, writes stereo
  samples into a ring buffer, and emits `BackendEvent`s.
- **CPAL callback** (hardware thread) — pops samples off the ring buffer and hands them to the
  sound card.

The render thread and the CPAL callback never share a lock: they only ever talk through a
lock-free ring buffer, which is the part that makes this safe to run in a real-time audio
context in the first place.

## Ring buffer

The ring buffer is a `crossbeam::queue::ArrayQueue<f32>`, holding stereo-interleaved samples
(`L, R, L, R, …`). Default capacity is 8,192 samples — about 93ms at 44.1kHz stereo. The render
thread throttles itself against a `target_latency_ms` (50ms by default) so it never races ahead
and fills the buffer past that point, which keeps command-to-sound latency low without the
render thread and the callback needing to coordinate directly.

On underrun, the callback just fills with silence and bumps a counter — no blocking, no glitches
cascading back into the render thread.

## Render pipeline

Every instrument compiles down into a `Source` node inside a single `System` graph.
`AudioGraph::compile()` assembles all loaded instruments into that one graph before playback
starts, and the render thread calls `system.run()` on it every block, draining pending
`AudioMessage`s in between. Swapping in a new graph at runtime — say, to change patches live — is
just sending `AudioMessage::Graph(GraphAudioMessage::Swap(system))`; the render thread swaps it
in atomically between blocks.

## DSP primitives

- **Generators** — a `SingleToneGenerator` is one oscillator voice (sine, square, sawtooth,
  triangle, white noise, ...) with its own frequency relation, amplitude envelope, and optional
  pitch envelope. `MultiToneGenerator` stacks several of these under a shared base frequency with
  a mix mode (sum, average, multiply, max) — this is how a single note ends up sounding like more
  than one oscillator.
- **Envelopes** — built from linear, bezier, and constant segments; `ADSREnvelope` composes four
  of them into the usual attack/decay/sustain/release shape.
- **Sources** — `MonophonicSource` (one voice, good for percussive hits like a kick or snare) and
  `PolyphonicSource` (a voice pool for melodic instruments like a keyboard).
- **Filters** — low-pass, high-pass, band-pass, gain, clipper, compressor, tremolo, delay, moving
  average, chained onto a source's output.
- **Instruments** — `Kick`, `Snare`, `HiHat`, and a polyphonic `Keyboard` ship built-in; each one
  implements a small trait (`start_note` / `stop_note` / `into_system`) so new instruments are
  just new implementations of that trait, not special cases in the engine.

## Where it stands

The engine, graph, and DSP primitives are functional and covered by CI. It's still a work in
progress — the interesting open problems right now are around richer instrument authoring and
making the graph easier to reconfigure live rather than just at load time.
