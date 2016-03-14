import os
import FbxCommon
import math
import SomeMaths


#Globals
width = 500
height = 500
xMargin = 25
yMargin = 25
xCenter = 0
yCenter = 0
rads = 3.1415/180
polygons = []
boundaries = []

camera = [[1, 0, 0],
          [0, 1, 0],
          [0, 0, 1]]


def resetBoundaries():
    maxX = 0
    minX = 0
    maxY = 0
    minY = 0
    


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

def sortPolygons():
    #Sort polygons from back to front, sorting z component of middle point(center) of each polygon from large to small.
    centers = []
    for poly in polygons:
        if len(poly) == 3:
            cz = (poly[0][2] + poly[1][2] + poly[2][2]) / 3.0
        else:
            cz = (poly[0][2] + poly[1][2] + poly[2][2] + poly[3][2]) / 4.0

        centers.append(cz)

    for i in range(0, len(polygons)-1):
        for j in range(i, len(polygons)):
            if (centers[j] < centers[i]):
                temp = centers[i]
                centers[i] = centers[j]
                centers[j] = temp
                temp = polygons[i]
                polygons[i] = polygons[j]
                polygons[j] = temp

def transformPolygons(matrix):
    #print "camera transform"
    #print matrix
    for poly in polygons:
        numVertices = len(poly)
        for i in range(numVertices):
                poly[i]= SomeMaths.MatrixVector3Product(matrix,poly[i])

def calculateFactor( boundaries ):
      
        fbxHeight = boundaries[2]- boundaries[3]
        fbxWidth = boundaries[0] - boundaries[1]
        fbxXcenter = fbxWidth/2
        fbxYcenter = fbxHeight/2
        heightFactor = float(fbxHeight/(height-2*yMargin))
        widthFactor = float(fbxWidth/(width-2*xMargin))
        print widthFactor, heightFactor
        factor = float( min(float(1/heightFactor),float(1/widthFactor)) - 1 )
        print factor
        return factor
       




 
def clearSVGdirectory(svgpath):
    #Clear SVG directory of .svg files
    for file in os.listdir(svgpath):
        if file.endswith(".svg"):
            svgfile = "%s\%s" % ( svgpath, file )
            print "%s removed" % ( file )
            os.remove(svgfile)


def createSVGfiles(fbxpath,svgpath):
    #Creates the svg files from each fbx file

    #in case some extension are in upper case, so we don't miss them
    fbxExtension = [".fbx",".FBX"]

    for file in os.listdir(fbxpath):
        if file.endswith(tuple(fbxExtension)):
            print(file)
            fbxfile = "%s\%s" % (fbxpath,file)
            print fbxfile
       
        sdk_manager, scene = FbxCommon.InitializeSdkObjects()

        if not FbxCommon.LoadScene(sdk_manager, scene, fbxfile):
                print("couldn't load the scene of file %s" % (fbxfile))

        #Reset transformations
        camera = SomeMaths.id3()

        #Transformations
        camera = SomeMaths.RotateZ(45*rads,camera)
        camera = SomeMaths.RotateX(45*rads,camera)
     
        extractPolygons(scene.GetRootNode())
        transformPolygons(camera)
        boundaries = sceneBoundaries()
        factor = calculateFactor(boundaries)
        camera = SomeMaths.id3()
        camera = SomeMaths.Scale(factor,camera)
        transformPolygons(camera)
        sortPolygons() #Always after all transforms have been done
        print "boundaries",
        print boundaries[0]-boundaries[1], boundaries[2]-boundaries[3]

        #print ("\n(%d,%d) (%d,%d) \n" % (maxX,minX,maxY,minY) )
        for x in boundaries:
            print x,

        print("Factor : %f \n" % factor)


        #print polygons

        svgfile = "%s\%s.svg" % (svgpath,file)
        print svgfile

        f = open(svgfile, 'w')
        if  f.errors:
                print ("Problems opening the file %s" % (svgfile))
        #SVG header
        f.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%d" height="%d" style="background: #999999"> ' % (width,height))
        color = 30
        if len(polygons) == 0:
             print "Error!: polygons lenght = 0"
        else:
            colorIncrement = 69.0/len(polygons)
        xCenter = float(width/2) # (width+xMargin)/2 # width - 300
        yCenter = float(height/2) #(height+yMargin)/2  #height - 200
        for poly in polygons:
                
                f.write('<polygon points="')
                for vertex in poly:
                    f.write( '%d,%d ' % (vertex[0]+xCenter, yCenter-vertex[1]) )
                f.write('" style="fill:#%d%d00;stroke:none"/>' % (color,color ) )
                color = color + colorIncrement
        #SVG footer
        f.write('</svg>')
        f.close()
        del polygons[:]

    
def generateWebPage(svgpath):
    f=open("index.html",'w')
    if  f.errors:
          print ("Problems opening the file index.html")

    f.write('<html>  <head><title> FBX Viewer </title></head> <body><p>An FBX viewer</p><object data=')
    path = "SVG_files"
    for file in os.listdir(svgpath):
     if file.endswith(".svg"):
         #print svgpath

         svgfile = "%s/%s" % (path,file)
         print svgfile
                #  inserting the svg file in the website
         f.write( '<img src="%s" alt="%s">' % (svgfile,file) )
         

    f.write('</object></body> </html>')
    f.close() 


####################### Code:

#Create path variables destined to create/locate .svg files
svgpath = os.getcwd()
svgpath +="\SVG_files"

#Create path variables destined to locate .fbx files
fbxpath = os.getcwd()
fbxpath +="\FBX_files"
print fbxpath


clearSVGdirectory(svgpath)
createSVGfiles(fbxpath,svgpath)
generateWebPage(svgpath)


