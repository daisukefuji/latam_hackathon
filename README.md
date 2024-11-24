# latam_hackathon
a demo app for latam hackathon

In pytest, validate screenshots taken from an Android emulator via ADB using Llama 3.2.

# How to run
set environment value first
$env:SAMBANOVA_API_KEY = "your api key" # for powershell
export SAMBANOVA_API_KEY = "your api key" # for bash

python adb_screen.py
or
pytest test_android_app.py