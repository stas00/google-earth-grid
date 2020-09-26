#!/usr/bin/env python3


##================= PhiGrid Platonic Coordinate Generator =======================
##
## Summary: This script generates a list of coordinates for the vertices
## of platonic solids, formatted to be pasted directly into the PhiGrid
## script editor.
##
## Instructions:
## 1) Type the platonic shape
## 2) Enter the locking coordinate - what lat/lon a vertex should lock onto
## 3) Enter the alignment coordinate - toward what lat/lon the vertex otherwise 
##                                     directly north of the locking coordinate
##                                     should be rotated.
## 4) Paste the output (starting with PAB) into the PhiGrid script editor, run it.
##
##Query:       Inputs:
##------       ---------
##
##Shape?       tetrahedron, octahedron, cube, icosahedron, dodecahedron, beckerhagens
##
##Latitude?    # (for North), -# (for South)
##
##Longitude?   # (for East), -# (for West)
##
##Example:
##--------
##
##Shape? dodecahedron
##Latitude of lock coordinate? 5
##Longitude of lock coordinate? 5
##Latitude of header coordinate? 30
##Longitude of header coordinate? 31
##
##This will place one corner of the tetrahedron at 5 N 5 E and rotate its edge
##toward 30N 31E -- toward the Great Pyramids at Ghiza.
##
##===============================================================================

import math
import sys
import argparse
import csv
import os

from google_earth_utils import rotateX, rotateY, rotateZ, bearing, coordinates, get_shape

def run(shape_name, lat1, lon1, lat2, lon2, outfile):
    if not outfile.endswith(".kml"):
        outfile += ".kml"
    output = open(outfile, 'w')

    lat1=num(lat1)
    lon1=num(lon1)
    lat2=num(lat2)
    lon2=num(lon2)
        
    print(f"lat1={lat1}, lon1={lon1}, lat2={lat2}, long2={lon2} => {outfile} ")

    shape, smallest = get_shape(shape_name, "coord")
    
    # set rotational angles
    thetaX=-bearing(lat1, lon1, lat2, lon2, math.radians(45))
    thetaZ=math.radians(lon1)
    thetaY=-math.radians(lat1)

    output.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>
        <name>{outfile}</name>""")

    coordinate=[]
    coordinatelatitude=[]
    coordinatelongitude=[]
    count=[]
    countsize=0
    
    # get coordinates in Google Earth code
    coordinates(rotateZ(rotateY(rotateX(shape, thetaX), thetaY), thetaZ), count,
                coordinatelongitude, coordinatelatitude, output)

    # get lines between points in Google Earth code,
    # use alpha calculated from http://onlinemschool.com/math/library/vector/angl/
    # i.e.  use (1,1,0) and (1,0,1) as vectors if getting alpha for cuboctahedron
    # for smallest, have that be a little larger than the calculated angle. 60 -> 61 for example.

    x=0
    z=1
    a=0.0
    b=0.0
    c=0.0
    d=0.0
    separation=0

    while x < len(count):
        while z < (len(count)):

            a=coordinatelongitude[x]
            b=coordinatelatitude[x]
            c=coordinatelongitude[z]
            d=coordinatelatitude[z]
            separation=math.acos(math.sin(b*.01744)*math.sin(d*.01744)+math.cos(b*.01744)*math.cos(d*.01744)*math.cos(a*.01744-c*.01744))/.01744
            if separation < smallest:

                output.write("""

<Placemark id="khPlacemark866">
<name>""")
                output.write(str(x))
                output.write(str(z))
                output.write("""</name><styleUrl>#khStyle2481</styleUrl>
    <LineString id="khLineString867"><tessellate>1</tessellate>
    <coordinates>""")

                output.write(str(a))
                output.write(',')
                output.write(str(b))
                output.write(' ')
                output.write(str(c))
                output.write(',')
                output.write(str(d))
                output.write("""
</coordinates></LineString></Placemark>""")

            z=z+1
        z=x+2    
        x=x+1

    output.write("""</Document>
    </kml>""")

    print(f"Generated {outfile}")
    output.close()

# def num_input(q):
#     return float(input(q))

def num(v):
    return float(v)

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='kml output file (optional)')
parser.add_argument('-c', '--config', help="shape,lat1,lon1,lat2,lon2")
parser.add_argument('-i', '--infile', help='csv input file w/o header: shape,lat1,lon1,lat2,lon2,outfile (optional)')

args = parser.parse_args()

if args.infile:
    file = args.infile
    if not os.path.exists(file):
        raise ValueError(f"{file} doesn't exist")
    
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        rec_count = 0
        for row in csv_reader:
            line_count += 1
            if len(row) < 5:
                print(f"skipping invalid line {line_count+1}")
                continue
            rec_count +=1 
            shape, lat1, lon1, lat2, lon2, outfile = row
            run(shape, lat1, lon1, lat2, lon2, outfile)
        print(f'Processed {line_count} lines, {rec_count} records.')    
else:
    outfile = 'GoogleEarth_coord_out.kml'
    if args.output:
        outfile = args.output

    if args.config:
        shape,lat1,lon1,lat2,lon2 = args.config.split(",")
    else:
        # get the shape
        print('Shape: tetrahedron, octahedron, cuboctahedron, cube, icosahedron, dodecahedron, beckerhagens')
        shape = input('\nWhich Shape? ')

        # get lock coordinate
        lat1=input('Latitude of lock coordinate? ')
        lon1=input('Longitude of lock coordinate? ')
        lat2=input('Latitude of header coordinate? ')
        lon2=input('Longitude of header coordinate? ')
        
    run(shape, lat1, lon1, lat2, lon2, outfile)

