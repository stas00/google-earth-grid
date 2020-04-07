#!/usr/bin/env python3

import sys, os.path, csv, argparse

def make_point(name, c1, c2):
    return f"""
    <Placemark>
      <Name>{name}</Name>
      <Icon><href>root://icons/palette-3.png</href><y>96</y><w>32</w><h>32</h></Icon>
      <Point><coordinates>{c1},{c2}</coordinates></Point>
    </Placemark>
"""

def make_line(points):
    # add ",0" for altitude
    text = "\n".join([f"{x[0]},{x[1]},0" for x in points])
    return f"""
    <Placemark>
      <Name>Line</Name>
      <styleUrl>#archaeo</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>{text}</coordinates>
      </LineString>
    </Placemark>
"""

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--linestring', action="store_true", help="Connect dots")
parser.add_argument('input',  help='csv input file')
parser.add_argument('output', help='kml output file')
args = parser.parse_args()

data = []
with open(args.input) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        data.append(row)
        line_count += 1
    print(f'Processed {line_count} lines.')

points = []
polygon_points = []
for row in data:
    points.append(make_point(*row))
    polygon_points.append([row[1], row[2]])
    #print(f' {row[0]}: {row[1]} {row[2]}')

# add the first point as last to complete the polygon
polygon_points.append(polygon_points[0])

out = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
  <Document>
    <name>Experiment 2</name>
{"".join(points)}
{make_line(polygon_points)}
  </Document>

</kml>
"""

print(f"Generating {args.output}")
with open(args.output, "w") as f: f.write(out)
