# Port of Earth Grid Research scripts

These are scripts from [Earth Grid Research](https://montalk.net/science/115/earth-grid-research) ([archive](https://web.archive.org/web/20200921223946/https://montalk.net/science/115/earth-grid-research)) - written in 2006 in python 2, and are now ported to python 3.

The scripts were partially refactored and improved - there are still many vestiges of python 2 15 year old code.

Upon request added shortcuts that avoid prompts:

```
python3 GoogleEarth_bearing.py -o bearing.kml -c "cube,1,2,3"
python3 GoogleEarth_bearing.py -o bearing -c "cube,1,2,3"
python3 GoogleEarth_bearing.py -c "cube,1,2,3"
```

And for the 2nd script, with the same variations as above:
```
python3 GoogleEarth_coord.py -o coord.kml -c "cube,1,2,3,4"
```

And then you can feed it csv files:

```
python3 GoogleEarth_coord.py -i input_coord_sample.csv
python3 GoogleEarth_bearing.py -i input_bearing_sample.csv
```
see the sample files in the repo, the format is:

* for `GoogleEarth_coord.py`: `shape,lat1,lon1,lat2,lon2,outfile`
* for `GoogleEarth_bearing.py`: `shape,lat1,lon1,bear,outfile`

See:

```
python3 GoogleEarth_bearing.py -h
python3 GoogleEarth_coord.py -h
```
for full help info.


