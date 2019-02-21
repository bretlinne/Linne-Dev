# Setup Mono or VSCode on POSIX-based OS
<img src="https://github.com/bretlinne/Linne-Dev-Prod/blob/master/resources/pico8.png" alt="drawing" width="64"/> 

[Pico-8 Website](https://www.lexaloffle.com/pico-8.php "Go get Pico-8--only $15!")

<!---alternative way to display image using github markdown:--->

<!---![pico8](https://github.com/bretlinne/Linne-Dev-Prod/blob/master/resources/pico8.png)--->

## Table of Contents
* [Purpose](#Purpose)
* [Usage](#Usage)
* [Background](#Background)
* [Palette  - **IMPORTANT!**](#Palette)
* [Why](#Why)

## Purpose
This script stretches the limits of the Pico-8's graphic capabilities.  
Only 256 8x8 pixel sprite tiles can be created and stored in the IDE.  This is 
what we must use to contstruct **EVERYTHING** in the game.  

However, the draw function of the Pico-8 can also draw directly from string data
in the right format if kajiggered properly.  

**That's what this project does.**

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

## Palette
To convert a .png file to a string of hex characters the Pico-8 can understand, 
you must author it using the EXACT hexadecimal color codes which correspond to
the system's 16-color palette.  

As long as the png is authored in these specific 16 colors, this script will work.

### Pico-8 Palette

|        |        |        |        |        |        |        |        |
|:------:|:-------|:------:|:-------|:------:|:-------|:------:|:-------|
| ![](https://placehold.it/15/000000?text=+)|000000  | ![](https://placehold.it/15/1c2b53?text=+)|1c2b53  | ![](https://placehold.it/15/7f2454?text=+)|7f2454  | ![](https://placehold.it/15/008751?text=+)|008751  |
| ![](https://placehold.it/15/ab5236?text=+)|ab5236  | ![](https://placehold.it/15/60584f?text=+)|60584f  | ![](https://placehold.it/15/c3c3c6?text=+)|c3c3c6  | ![](https://placehold.it/15/fff1e9?text=+)|fff1e9  |
| ![](https://placehold.it/15/ed1b51?text=+)|ed1b51  | ![](https://placehold.it/15/faa21b?text=+)|faa21b  | ![](https://placehold.it/15/f7ec2f?text=+)|f7ec2f  | ![](https://placehold.it/15/5dbb4d?text=+)|5dbb4d  |
| ![](https://placehold.it/15/51a6dc?text=+)|51a6dc  | ![](https://placehold.it/15/83769c?text=+)|83769c  | ![](https://placehold.it/15/f176a6?text=+)|f176a6  | ![](https://placehold.it/15/fcccab?text=+)|fcccab  |

#### Download Photoshop swatch file:
[Photoshop Pico-8 Swatch File](https://drive.google.com/open?id=1CbiOMOtlxwxnVHDyOTP-InKKue_xtE3y)

Install the swatch in photoshop:

<img src="https://github.com/bretlinne/Linne-Dev-Prod/blob/master/resources/psHow01.PNG" alt="drawing" width="360"/> 
<img src="https://github.com/bretlinne/Linne-Dev-Prod/blob/master/resources/psHow02.png" alt="drawing" width="360"/> 


## Why?
facilitate easy setup for VSCode and Mono
