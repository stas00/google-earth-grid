# google-earth-grid

This ia a very basic [Google Earth](https://earth.google.com/) kml file generator

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

* The expected input file uses a comma-separated CSV-format file with one line per single location:

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

* By default the output kml will use `My Grid` as the project name. You can override this with `-n "My name"` in the command line.
