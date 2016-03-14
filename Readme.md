#FBX models rendered to SVG format using Python  
####This program reads a directory of FBX files and renders each of them in a simple webpage in an SVG format.
This is the report for the second Tools and Middleware's assignment. Initially, this project started individually by David Barbera but was joined later on by Mircea Catana who offered insights in different ways of using Python bindings to read .fbx files to extract the minimum information to render the model efficiently.

##The Program  
The final version of the program uses Pythong Bindings to extract information about the polygons in each mesh for an .fbx file. This approach offears the possiblity to render the resulting information using the *"polygon points"*-feature of the SVG format, allowing a one-to-one translation from on format to the other and resulting in a nicer display than other approaches tried previously. 

The code responsible for the extraction of polygons is the following:  
```python  
def extractPolygons(node):
    mesh =  node.GetMesh()
    if not mesh:
        print "not mesh"
    else:
        for i in range(mesh.GetPolygonCount()):
            numVertices = mesh.GetPolygonSize(i)
            polygonVertices = []
            fbxVertices = []
           
            for k in range(numVertices):
                fbxVertices.append(mesh.GetControlPointAt(mesh.GetPolygonVertex(i,k)))
                newVertex = [0 for x in range(3)]
                polygonVertices.append(newVertex)
                for h in range(3):
                    polygonVertices[k][h] = fbxVertices[k][h]
            polygons.append(polygonVertices)
            
    for i in range(node.GetChildCount()):
            extractPolygons(node.GetChild(i))
```  
*Comments:*  First, for each node detects if it corresponds to a mesh or not. Second, for each mesh detects the number of polygons. Then, for each polygon obtain its vertices and adds them into a list of vertices: one list per polygon. Each polygon is then added to a list of polygons,i.e., *polygons*, which becomes a list of lists. All vectors have dimension 3.

The advantage of this method is that allows for mofularity: once we have extracted all the polygons we don't need the .fbx file anymore and we can just work on the list of lists, *polygons*. Since *polygons* is ultimately a list of lists of vertices, we can apply transformations using matrices directly into this data structure. To achieve an isometric view, I used the followint transformations:
```python  
	#Reset transformations
        camera = SomeMaths.id3()

        #Transformations
        camera = SomeMaths.RotateZ(45*rads,camera)
        camera = SomeMaths.RotateX(45*rads,camera)
```  
Where camera is 3x3 matrix.  
I made the module *SomeMaths* to organize the code and separate the maths-related functions from the rest of the code. With *SomeMaths* the following operations are supported:  
- Rotations (about each axis) via 3x3 matrix
- Scaling via 3x3 matrix
- Product of Matrix 3x3 per Vector of dimension 3
- Create, reset matrix to Id matrix 3x3  

Once, transformations has been done I tackled the issue that different models comming from.fbx files have different sizes. Therefore, in order to fit our rendering into an SVG-canvas we might need to scale it. To that purpose, the list *boundaries* contains the dimension of width and height int the following format [maxX,minX,maxY,minY]. This is the code:  
```python  
def sceneBoundaries():
        maxX = 0
        minX = 0
        maxY = 0
        minY = 0

        for poly in polygons:
            for vertex in poly:
                if(vertex[0] > maxX):
                    maxX = vertex[0]
                if(vertex[0] < minX): 
                    minX = vertex[0]
                if(vertex[1] > maxY):
                    maxY = vertex[1]
                if(vertex[1] < minY):
                    minY = vertex[1]

        boundaries = []
        boundaries.append(maxX)
        boundaries.append(minX)
        boundaries.append(maxY)
        boundaries.append(minY)

        return boundaries
```  
Once the scaling factor has been calculated with the *calculateFactor()* using the list *boundaries* then and only then I applied the regarding scaling transformation to the list *polygons*. 

In order to render our polygons in SVG, the best approah suggested by Mircea is to order all the vertices using the z-component ("depth") and render them back to front. This process is achieved by matching each polygon by its middle vertex and sorting all the middle vertices from far to near, one to one with our *polygons* list.
Here is the code:  
```python
def sortPolygons():
    #Sort polygons from back to front, sorting z component of middle point of each polygon from large to small.
    middles = []
    for poly in polygons:
        numVertices = len(poly)
        cz = 0
        for i in range(numVertices):
            cz += poly[i][2]
        cz = cz/numVertices

        middles.append(cz)

    for i in range(0, len(polygons)-1):
        for j in range(i, len(polygons)):
            if (middles[j] < middles[i]):
                temp = middles[i]
                middles[i] = middles[j]
                middles[j] = temp
                temp = polygons[i]
                polygons[i] = polygons[j]
                polygons[j] = temp
``` 
*Note:* So far polygons of any number of sides have been considered as I found some .fbx models using pentagons as a polygon, not only triangles and quads which are usually the most common ones.  

The following is an example of models rendered using two different approaches:

![alt text](https://github.com/DavidBarbera/ToolsAndMiddleware/blob/master/FBX_Web/report/TeaPot.png "Tea Pot Solid")

![alt text](https://github.com/DavidBarbera/ToolsAndMiddleware/blob/master/FBX_Web/report/TeaPotLines.png "Tea Pot Lines")




	



