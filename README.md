# google-earth-grid

This ia a very basic [Google Earth](https://earth.google.com/) kml file generator

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

The expected input file uses a comma-separated CSV-format file with one line per single location,

```
Site Name,Longitude,Latitude
```


e.g.:

```
A,-11.7992189239,-50.666666
B,-40.5555555555,-15.4333333038
C,-60.7911111111,-25.4333333318
```
