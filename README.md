# google-earth-grid

This is a very basic [Google Earth](https://earth.google.com/) kml file generator

Usage:

```
./makegrid.py -h
usage: makegrid.py [-h] [-l] [-n NAME] input [output]

positional arguments:
  input                 csv input file
  output                kml output file (optional)

optional arguments:
  -h, --help            show this help message and exit
  -l, --linestring      connect dots
  -n NAME, --name NAME  project name
```

Example:

```
./makegrid.py input.csv
```

Command line arguments:

* The required input file is expected to be a comma-separated CSV file, where each record is a single location as follows (no header):

   ```
   Site Name,Longitude,Latitude
   ```

   For example:

   ```
   A,-62.26,-2.68
   B,-61.40,-12.07
   C,-48.74,-8.26
   ```

* Unless explicitly specified, the output filename is derived from the input filename, by replacing `.csv` with `.kml`, and adding `-l` to basename if `-l` option is used.

   Warning: if the output file already exists, it will get silently overwritten with the new output.

* By default the output kml will use the input filename (sans the extension) as the project name. You can override this with `-n "My name"` in the command line.

## port of Earth Grid Research scripts

And here is a [port](./port) of Earth Grid Research scripts circa 2006 to python 3.
