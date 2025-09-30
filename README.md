# vna-monitor
## Summary
Continuous runtime monitor for the nanoVNA-F V2 using the PyVISA library

## Test Setup
Power Raspberry Pi 5 with 27W USB-C power supply
Connect nanoVNA-F V2 to Raspberry Pi via USB
Turn on nanoVNA-F V2 switch to power the unit
ssh into the Raspberry Pi 5 (unit I am using is 192.168.1.112)

## Running
source ~/py_envs/bin/activate
python3 vnaMonitor.py
