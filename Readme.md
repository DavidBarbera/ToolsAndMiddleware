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
*Comments:*  First, for each node detects if it corresponds to a mesh or not. Second, for each mesh detects the number of polygons. Then, for each polygon obtain its vertices and appends them into a list of vertices: one list for each polygon. Each polygon is then appended to a list of polygons,i.e., *polygons*, which is a list of lists.



