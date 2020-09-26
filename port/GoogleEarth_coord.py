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

coordinate=[]
coordinatelatitude=[]
coordinatelongitude=[]
count=[]
countsize=0

# Golden Ratio

p=(1+math.sqrt(5))/2

# xyz coordinates of vertices of platonic shapes

dodecahedron=[[0,1/p,p],[0,-1/p,-p],[0,-1/p,p],[0,1/p,-p],
              [1/p,p,0],[-1/p,-p,0],[-1/p,p,0],[1/p,-p,0],
              [p,0,1/p],[-p,0,-1/p],[-p,0,1/p],[p,0,-1/p],
              [1,1,1],[-1,-1,-1],[-1,1,1],[-1,-1,1],
              [-1,1,-1],[1,-1,-1],[1,-1,1],[1,1,-1]]

icosahedron=[[0,1,p],[0,-1,-p],[0,-1,p],[0,1,-p],
             [1,p,0],[-1,-p,0],[-1,p,0],[1,-p,0],
             [p,0,1],[-p,0,-1],[-p,0,1],[p,0,-1]]

cube=[[1,1,1],[-1,-1,-1],[-1,1,1],[-1,-1,1],
      [-1,1,-1],[1,-1,-1],[1,-1,1],[1,1,-1]]

tetrahedron=[[1,1,1],[-1,-1,1],[-1,1,-1],[1,-1,-1]]

octahedron=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]]


cuboctahedron=[[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0],
               [1,0,1],[-1,0,-1],[1,0,-1],[-1,0,1],
               [0,1,1],[0,-1,-1],[0,1,-1],[0,-1,1]]


beckerhagens=[[0,1/p,p],[0,-1/p,-p],[0,-1/p,p],[0,1/p,-p],
              [1/p,p,0],[-1/p,-p,0],[-1/p,p,0],[1/p,-p,0],
              [p,0,1/p],[-p,0,-1/p],[-p,0,1/p],[p,0,-1/p],
              [1,1,1],[-1,-1,-1],[-1,1,1],[-1,-1,1],
              [-1,1,-1],[1,-1,-1],[1,-1,1],[1,1,-1],
              [0,-p,1],[0,p,-1],[0,-p,-1],[0,p,1],
              [1,0,p],[-1,0,-p],[-1,0,p],[1,0,-p],
              [p,-1,0],[-p,1,0],[-p,-1,0],[p,1,0],
              [2,0,0],[-2,0,0],[0,2,0],[0,-2,0],[0,0,2],[0,0,-2],
              [p,1/p,1],[-p,-1/p,-1],[-p,-1/p,1],[-p,1/p,-1],
              [p,-1/p,-1],[p,-1/p,1],[p,1/p,-1],[-p,1/p,1],
              [1,p,1/p],[-1,-p,-1/p],[-1,-p,1/p],[-1,p,-1/p],
              [1,-p,-1/p],[1,-p,1/p],[1,p,-1/p],[-1,p,1/p],
              [1/p,1,p],[-1/p,-1,-p],[-1/p,-1,p],[-1/p,1,-p],
              [1/p,-1,-p],[1/p,-1,p],[1/p,1,-p],[-1/p,1,p]]


# rotate xyz coordinates ccw around north pole, z axis

def rotateZ(function):
   
    for i in range(len(function)):

        x=function[i][0]
        y=function[i][1]
        z=function[i][2]

        function[i][0]=x*math.cos(thetaZ)-y*math.sin(thetaZ)
        function[i][1]=x*math.sin(thetaZ)+y*math.cos(thetaZ)
        function[i][2]=z

    return function


# rotate xyz coordinates ccw around 0 N 0 E, x-axis

def rotateX(function):
   
    for i in range(len(function)):

        x=function[i][0]
        y=function[i][1]
        z=function[i][2]

        function[i][0]=x
        function[i][1]=y*math.cos(thetaX)-z*math.sin(thetaX)
        function[i][2]=y*math.sin(thetaX)+z*math.cos(thetaX)

    return function


# rotate xyz coordinates ccw around 0 N 90 E, y axis

def rotateY(function):
   
    for i in range(len(function)):

        x=function[i][0]
        y=function[i][1]
        z=function[i][2]

        function[i][0]=x*math.cos(thetaY)+z*math.sin(thetaY)
        function[i][1]=y
        function[i][2]=-x*math.sin(thetaY)+z*math.cos(thetaY)

    return function


# get bearing, angle from true north between lock point and header point

def bearing(lat1,lon1,lat2,lon2):
    lat1=math.radians(lat1)
    lon1=math.radians(lon1)
    lat2=math.radians(lat2)
    lon2=math.radians(lon2)
    
    y=math.sin(lon2-lon1)*math.cos(lat2)
    x=math.cos(lat1)*math.sin(lat2)-math.sin(lat1)*math.cos(lat2)*math.cos(lon2-lon1)

    if y>0:
        if x>0:
            thetaY=math.atan(y/x)
        elif x<0:
            thetaY=-math.pi-math.atan(-y/x)
        else:
            thetaY=math.pi/2
    elif y<0:
        if x>0:
            thetaY=-math.atan(-y/x)
        elif x<0:
            thetaY=math.atan(y/x)+math.pi
        else:
            thetaY=math.pi*3/2
    else:
        if x>0:
            thetaY=0
        elif x<0:
            thetaY=-math.pi
        else:
            thetaY=0
    return math.degrees(thetaY)
    



# generate latitude and longitude from xyz coordinates

def coordinates(function, output):
    
    for i in range(len(function)):

        x=function[i][0]
        y=function[i][1]
        z=function[i][2]
        
        theta=0
        phi=0

        if z < 0:
            theta=math.pi+math.atan(math.sqrt(x*x+y*y)/z)
        elif z == 0:
            theta=math.pi/2
        else:
            theta=math.atan(math.sqrt(x*x+y*y)/z)
        
        if x < 0 and y != 0:
            phi=math.pi+math.atan(y/x)
        elif x == 0 and y > 0:
            phi=math.pi/2
        elif x == 0 and y < 0:
            phi=math.pi*3/2
        elif y == 0 and x > 0:
            phi=0
        elif y == 0 and x < 0:
            phi=math.pi
        elif x > 0 and y <= 0:
            phi = 2*math.pi + math.atan(y/x)
        elif x == 0 and y == 0:
            phi = 888
        else:
            phi=math.atan(y/x)

        function[i][0]=theta
        function[i][1]=phi
        del function[i][2]

        theta=math.degrees(theta)
        phi=math.degrees(phi)

        latitude=90-theta
        if phi<=180:
            longitude=phi
        else:
            longitude=phi-360

        if longitude > 600:
            longitude = 0.0


        if longitude <=0:
            one=str(len(count))
            coordinatelongitude.append(longitude)
            output.write("""
            
<Placemark><name>""")
            output.write(one)
            output.write("""</name><Icon>
<href>root://icons/palette-3.png</href>
<y>96</y><w>32</w><h>32</h></Icon>
<Point><coordinates>  
            """),
            output.write(str(longitude))
            output.write(',')
        
           
        else:
            one=str(len(count))
            
            coordinatelongitude.append(longitude)
            output.write("""
            
<Placemark><name>""")
            output.write(one)             
            output.write("""</name><Icon>
<href>root://icons/palette-3.png</href>
<y>96</y><w>32</w><h>32</h></Icon>
<Point><coordinates>  
            """),
            output.write(str(longitude))
            output.write(',')
      
        if latitude <=0:
            coordinatelatitude.append(latitude)
            output.write(str(latitude))
            output.write("""
</coordinates></Point></Placemark>""")
        else:
            coordinatelatitude.append(latitude)
            output.write(str(latitude))
            output.write("""
</coordinates></Point></Placemark>""")  
        count.append(1)

# default the vertex of a shape toward true north
thetaY=math.radians(20.9051574479)
thetaX=math.radians(180)
dodecahedron=rotateX(rotateY(dodecahedron))
beckerhagens=rotateX(rotateY(beckerhagens))

thetaY=math.radians(35.26439)
thetaZ=math.radians(-45)
thetaX=math.radians(180)
tetrahedron=rotateY(rotateZ(tetrahedron))

cube=rotateX(rotateY(rotateZ(cube)))

thetaY=math.radians(31.717474)
icosahedron=rotateX(rotateY(icosahedron))

thetaY=math.radians(45)
thetaX=math.radians(54.735610317)
cuboctahedron=rotateX(rotateY(cuboctahedron))


def run(shape, lat1, lon1, lat2, lon2, outfile):
    if not outfile.endswith(".kml"):
        outfile += ".kml"
    output = open(outfile, 'w')

    lat1=num(lat1)
    lon1=num(lon1)
    lat2=num(lat2)
    lon2=num(lon2)
        
    print(f"Params: lat1={lat1}, lon1={lon1}, lat2={lat2}, long2={lon2}")

    #shape = "cube"
    shape = globals()[shape]

    # set rotational angles
    thetaX=-bearing(lat1,lon1,lat2,lon2)
    thetaZ=math.radians(lon1)
    thetaY=-math.radians(lat1)

    output.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>
        <name>{outfile}</name>""")

    # get coordinates in Google Earth code

    coordinates(rotateZ(rotateY(rotateX(shape))), output)

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

    if shape==cube:
        smallest=71

    if shape==tetrahedron:
        smallest=110

    if shape==octahedron:
        smallest=91

    if shape==cuboctahedron:
        smallest=61

    if shape==icosahedron:
        smallest=64

    if shape==dodecahedron:
        smallest=43

    if shape==beckerhagens:
        smallest=91
    # Make "91" smaller to reduce number of lines in becker-hagens grid.


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
        for row in csv_reader:
            if len(row) < 5:
                print(f"skipping invalid line {line_count}")
                continue
            line_count += 1
            shape, lat1, lon1, lat2, lon2, outfile = row
            run(shape, lat1, lon1, lat2, lon2, outfile)
        print(f'Processed {line_count} lines.')    
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

