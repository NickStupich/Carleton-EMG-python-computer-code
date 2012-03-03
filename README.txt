The backend code that runs on a PC

Deals with talking to the Fez Mini Microcontroller over Bluetooth, compiling data back together, and doing some data processing with it.  Right now got 3 main parts:

Binary Classification: Determine if any of the input muscles are determined to be on or off

Continuous Interpolation: Determine what percentage of max any muscle is being used

Gesture Recognition: Determine if 'gestures' of a fairly short time period (~0.5 seconds) are being performed.