# CropperView
A simple script that batch crops and superviews HDzero goggles DVR files

## Why
The HDZ Goggles appears to save all DVR files in 16:9 format.

This leaves 4:3 footage with black bars on the left and right, making it unsuitable for superviewing.

In order to fix that I've been cropping the DVRs in handbrake first, before superviewing them, all manually.

This script handle both these operations automatically and in batch

## How to use
I have included most dependencies to work right out of the box on Windows.

All you need to get on your own is FFmpeg; you can get it [there](https://www.gyan.dev/ffmpeg/builds/) by simply running 'winget install ffmpeg' in your windows powershell

Then clone this repo on your computer, place your files in input_videos, and run cropperview.py --I have also made a little batch file, just double click run_cropperview.bat

A command window will appear and after completed your processed files will appear in output_files

## Dependancies / Attribution
 * [FFmpeg](https://github.com/FFmpeg/FFmpeg)
 * [Handbrake](https://github.com/HandBrake/HandBrake)
 * [Niek's Superview](https://github.com/Niek/superview)