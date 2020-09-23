# Port of Earth Grid Research scripts

These are scripts from [Earth Grid Research](https://montalk.net/science/115/earth-grid-research) ([archive](https://web.archive.org/web/20200921223946/https://montalk.net/science/115/earth-grid-research)) - written in 2006 in python 2, and are now ported to python 3.

I did just the bare minimum to make the scripts work under python 3.

Upon request added shortcuts that avoid prompts:

```
python3 GoogleEarth_bearing.py bearing.kml -c "cube,1,2,3"
python3 GoogleEarth_coord.py coord.kml -c "cube,1,2,3,4"
```
See:

```
python3 GoogleEarth_bearing.py -h
python3 GoogleEarth_coord.py -h
```
for full help info.


