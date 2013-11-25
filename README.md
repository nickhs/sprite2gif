# Sprite to Gifs

Convert sprites to gifs using ImageMagick and this handy python script.

## Install

1. Download Script
2. Install ImageMagick on your machine

	On OSX:

    	brew install imagemagick

	On Ubuntu/Debian:

    	sudo apt-get install imagemagick

## Example

    python sprite2gif.py example/sprite.png
    # Output now in example/sprite.gif

## Use

You can specify the output file and the dimensions of the sprites if necessary:

    python sprite2gif.py infile outfile dimensions

Dimension must be two integers seperated by an `x`. Such as `2x2` or `1x5`.
