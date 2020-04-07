# google-earth-grid
a very basic Google Earth kml generator

Usage:

```
./makegrid.py -h
usage: makegrid.py [-h] [-l] input output

positional arguments:
  input             csv input file
  output            kml output file

optional arguments:
  -h, --help        show this help message and exit
  -l, --linestring  Connect dots
```

Example:

```
./makegrid.py input.csv output.kml
```
