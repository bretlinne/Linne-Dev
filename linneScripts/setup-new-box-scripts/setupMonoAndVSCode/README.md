# Setup Mono or VSCode on POSIX-based OS
<img src="https://github.com/bretlinne/Linne-Dev-Prod/blob/master/resources/pico8.png" alt="drawing" width="64"/> 

[Pico-8 Website](https://www.lexaloffle.com/pico-8.php "Go get Pico-8--only $15!")

## Table of Contents
* [Purpose](#Purpose)
* [Usage](#Usage)
* [Background](#Background)
* [Why](#Why)

## Purpose
This script downloads and installs the latest version of Microsoft Visual Studio Code

## Usage
1) Download the repo
2) Test it using `python pico8-png-to-hex.py ./p8Test.png`
3) it should spit out a string like so: `0123456789abcdef`
4) this would be copied and then pasted into the Pico-8 for usage in 
...a draw function.  I've included an example draw function in the HELP
...and an example of how to build a data structure to store this data.

The executable: `pico8-png-to-hex.py`

support files:

| Filename              | Purpose                                  |
| --------------------- |:----------------------------------------:|
| **pngGraphicMethods.py**  | contains all graphic methods and classes |
| **linneXtermColors.py**   | defines colors for making nice output    |
| **getch.py**              | provides faster UX                       |
| **p8Help.py**             | all text and function for -h             |
| **p8Test.png**        | a test .png                              |

## Background
The Pico-8 is a fantasy console and IDE.  It emulates a console like a GameBoy 
color which **_could_** have existed in the 90's or so, but was never actually 
created.  This system is **very** restrained in its capabilities.  

* only 16 colors
* only 256 8x8 tiles of sprite storage
* only 7 input buttons (d-pad, buttonX, button Z, and a start button)
* whole thing is restrained to 32Kb of memory per game!

Within these limits, a great deal can be done and it's a fantastic little game engine
to learn to build games or prototype ideas.

## Why?
facilitate easy setup for VSCode and Mono
