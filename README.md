# BCI Projects

# Hybrid BCI Wheelchair

**Enjoy life again.**

A brain-computer interface (BCI) that lets people who cannot move their body freely control a wheelchair and a built-in tablet using only their brain signals.

## The goal

Many elderly people and people with severe motor disabilities depend on others for everyday things, like moving around, calling for help, or listening to music. This project aims to give that control back to them.

The final system is:
1. A slim EEG headband (not a heavy lab cap)
2. A wheelchair with a tablet that appears on demand
3. Apps controlled by looking at flickering targets on screen: chat, music, emergency call, and later movies, notes, and games

Design principle: it should look as little "medical" as possible.

## How it works

The system uses two brain signals together (a hybrid BCI):

1. **SSVEP**: when you look at something flickering at a certain frequency (for example 8 Hz), your visual cortex produces brain waves at that same frequency. The system detects which target you are looking at.
2. **P300**: a small brain response that appears about 300 ms after something you are paying attention to flashes.

Combining both makes the selection more accurate and faster than using either one alone.

Pipeline:
EEG board → reader → preprocessing (filtering, artifact removal) → classification (SVM for P300, TRCA for SSVEP) → fusion → app action

Main reference: Bai et al. 2023, FERC hybrid speller (PMC10050351).

## Hardware

1. FreeBCI-WiFi-8-I EEG board (8 channels, ADS1299, ESP32-S3, up to 2000 Hz)
2. Gold cup electrodes with conductive gel
3. Target computer: Raspberry Pi mounted on the wheelchair

## Repository structure

reader/       Python reader that streams raw EEG from the board over WiFi

More folders (pipeline, stimulus, UI) will be added as each part is tested on real hardware.

## Progress

- [x] Stage 0: board streams data through the vendor software
- [x] Stage 1: own Python reader streams data over WiFi without vendor software
- [ ] Stage 2: convert to microvolts and save recordings
- [ ] Stage 3: signal checks with electrodes (blinks, alpha waves)
- [ ] Stage 4: connect the processing and classification pipeline to live data
- [ ] Stage 5: SSVEP app interface running on Raspberry Pi
- [ ] Stage 6: wheelchair control

## Author

Htet Pai (テッパイ), iU Tokyo