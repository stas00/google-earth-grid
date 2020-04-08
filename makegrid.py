#!/usr/bin/env python3

import sys, os.path, csv, argparse

def make_point(name, c1, c2):
    return f"""
    <Placemark>
      <name>{name}</name>
      <Icon><href>root://icons/palette-3.png</href><y>96</y><w>32</w><h>32</h></Icon>
      <Point><coordinates>{c1},{c2}</coordinates></Point>
    </Placemark>
"""

def make_polygon(points):
    # add ",0" for altitude
    text = "\n".join([f"{x[0]},{x[1]},0" for x in points])
    return f"""
    <Placemark>
      <name>Line</name>
      <styleUrl>#archaeo</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>{text}</coordinates>
      </LineString>
    </Placemark>
"""

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--linestring', action="store_true", help="Connect dots")
parser.add_argument('input', help='csv input file')
parser.add_argument('output', nargs='?', help='kml output file (optional)')
args = parser.parse_args()

data = []
with open(args.input) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader: data.append(row)
print(f'Read {len(data)} points.')

points = []
polygon_points = []
for row in data:
    #print(f' {row[0]}: {row[1]} {row[2]}')
    points.append(make_point(*row))
    if args.linestring: polygon_points.append([row[1], row[2]])

polygon = ''
if args.linestring:
    # add the first point as last to complete the polygon
    polygon_points.append(polygon_points[0])
    polygon = make_polygon(polygon_points) if args.linestring else ''

out = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
  <Document>
    <name>Experiment 2</name>
{"".join(points)}
{polygon}
  </Document>

</kml>
"""

# output
if args.output is not None:
    ofn = args.output
else:
    postfix = '.kml'
    if args.linestring:
        postfix = "-l" + postfix
    ofn = args.input.lower().replace('.csv', postfix)
print(f"Generating {ofn}")
with open(ofn, "w") as f: f.write(out)
