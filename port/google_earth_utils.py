import math

# rotate xyz coordinates ccw around north pole, z axis
def rotateZ(function, thetaZ):
   
    for i in range(len(function)):

        x=function[i][0]
        y=function[i][1]
        z=function[i][2]

        function[i][0]=x*math.cos(thetaZ)-y*math.sin(thetaZ)
        function[i][1]=x*math.sin(thetaZ)+y*math.cos(thetaZ)
        function[i][2]=z

    return function


# rotate xyz coordinates ccw around 0 N 0 E, x-axis
def rotateX(function, thetaX):
   
    for i in range(len(function)):

        x=function[i][0]
        y=function[i][1]
        z=function[i][2]

        function[i][0]=x
        function[i][1]=y*math.cos(thetaX)-z*math.sin(thetaX)
        function[i][2]=y*math.sin(thetaX)+z*math.cos(thetaX)

    return function


# rotate xyz coordinates ccw around 0 N 90 E, y axis

def rotateY(function, thetaY):
   
    for i in range(len(function)):

        x=function[i][0]
        y=function[i][1]
        z=function[i][2]

        function[i][0]=x*math.cos(thetaY)+z*math.sin(thetaY)
        function[i][1]=y
        function[i][2]=-x*math.sin(thetaY)+z*math.cos(thetaY)

    return function


# get bearing, angle from true north between lock point and header point
def bearing(lat1, lon1, lat2, lon2, thetaY):
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
def coordinates(function, count, coordinatelongitude, coordinatelatitude, output):
    
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


def get_shape(name, caller):

    # Golden Ratio

    p=(1+math.sqrt(5))/2

    # xyz coordinates of vertices of platonic shapes
    shapes = dict(
        dodecahedron=[[0,1/p,p],[0,-1/p,-p],[0,-1/p,p],[0,1/p,-p],
                      [1/p,p,0],[-1/p,-p,0],[-1/p,p,0],[1/p,-p,0],
                      [p,0,1/p],[-p,0,-1/p],[-p,0,1/p],[p,0,-1/p],
                      [1,1,1],[-1,-1,-1],[-1,1,1],[-1,-1,1],
                      [-1,1,-1],[1,-1,-1],[1,-1,1],[1,1,-1]],

        icosahedron=[[0,1,p],[0,-1,-p],[0,-1,p],[0,1,-p],
                     [1,p,0],[-1,-p,0],[-1,p,0],[1,-p,0],
                     [p,0,1],[-p,0,-1],[-p,0,1],[p,0,-1]],

        cube=[[1,1,1],[-1,-1,-1],[-1,1,1],[-1,-1,1],
              [-1,1,-1],[1,-1,-1],[1,-1,1],[1,1,-1]],

        tetrahedron=[[1,1,1],[-1,-1,1],[-1,1,-1],[1,-1,-1]],

        octahedron=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],


        cuboctahedron=[[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0],
                       [1,0,1],[-1,0,-1],[1,0,-1],[-1,0,1],
                       [0,1,1],[0,-1,-1],[0,1,-1],[0,-1,1]],


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
                      [1/p,-1,-p],[1/p,-1,p],[1/p,1,-p],[-1/p,1,p]],
        )

    
    # default the vertex of a shape toward true north
    thetaY=math.radians(20.9051574479)
    thetaX=math.radians(180)
    shapes["dodecahedron"]=rotateX(rotateY(shapes["dodecahedron"], thetaY), thetaX)
    shapes["beckerhagens"]=rotateX(rotateY(shapes["beckerhagens"], thetaY), thetaX)

    thetaY=math.radians(35.26439)
    thetaZ=math.radians(-45)
    thetaX=math.radians(180)
    shapes["tetrahedron"]=rotateY(rotateZ(shapes["tetrahedron"], thetaZ), thetaY)

    shapes["cube"]=rotateX(rotateY(rotateZ(shapes["cube"], thetaZ), thetaY), thetaX)

    thetaY=math.radians(31.717474)
    shapes["icosahedron"]=rotateX(rotateY(shapes["icosahedron"], thetaY), thetaX)

    thetaY=math.radians(45)
    # Tom: This difference is intentional due to the peculiarities of the geometry (squares and triangles).
    value=54.735610317 if caller == "coord" else 35.2643897
    thetaX=math.radians(value)
    shapes["cuboctahedron"]=rotateX(rotateY(shapes["cuboctahedron"], thetaY), thetaX)

    smallest = dict(
        cube=71,
        tetrahedron=110,
        octahedron=91,
        cuboctahedron=61,
        icosahedron=64,
        dodecahedron=43,
        beckerhagens=91, # Make "91" smaller to reduce number of lines in becker-hagens grid.
    )
    
    if name not in shapes:
        raise ValueError(f"don't know of {name}, only have {shapes.keys()}")
    
    return shapes[name], smallest[name]

