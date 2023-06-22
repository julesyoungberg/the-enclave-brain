# the-enclave-brain

This repo contains code for controlling "The Enclave" art installation. This is the piece that ties everything together and orchestrates the evolution of the experience. It takes input from the controller, calculates the current state, and sends messages to other programs to keep everything in sync.

## input

Input is taken from the controller as MIDI signals over USB.

## output

Output is OSC signals for triggering scenes.

## setup

```
python3 -m pip install -r requirements.txt
```

## run

```
python3 main.py
```
