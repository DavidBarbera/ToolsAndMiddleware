import os
import FbxCommon
import math
import SomeMaths


#Globals
width = 500
height = 500
rads = 3.1415/180
polygons = []
maxX = 0
minX = 0
maxY = 0
minY = 0

camera = [[1, 0, 0],
          [0, 1, 0],
          [0, 0, 1]]


def fbxBoundaries(node,camera,maxX,minX,maxY,minY):

    mesh = node.GetMesh()
  
    if not mesh:
        print("not mesh")
    else:
        for i in mesh.GetPolygonVertices():
            point = mesh.GetControlPointAt(i)
            vertex = [0 for x in range(3)]
            vectorPoint = [0 for x in range(3)]
            for j in range(3):
                vectorPoint[j] = point[j]
            vertex = SomeMaths.MatrixVector3Product( camera, vectorPoint)
            if(vertex[0] > maxX):
                maxX = vertex[0]
            if(vertex[0] < minX): 
                minX = vertex[0]
            if(vertex[1] > maxY):
                maxY = vertex[0]
            if(vertex[1] < minY):
                minY = vertex[0]
            

    for i in range(node.GetChildCount()):
        
        fbxBoundaries(node.GetChild(i),camera,maxX,minX,maxY,minY)

def createPolygons(node,camera):
    print camera
    mesh =  node.GetMesh()
    if not mesh:
        print "not mesh"
    else:
        for i in range(mesh.GetPolygonCount()):
            numVertices = mesh.GetPolygonSize(i)
            
            if numVertices == 3:
                newv1= [0 for x in range(3)]
                newv2= [0 for x in range(3)]
                newv3= [0 for x in range(3)]

                fbxv1 = mesh.GetControlPointAt(mesh.GetPolygonVertex(i,0))
                fbxv2 = mesh.GetControlPointAt(mesh.GetPolygonVertex(i,1))
                fbxv3 = mesh.GetControlPointAt(mesh.GetPolygonVertex(i,2))

                for h in range(3):
                    newv1[h]=fbxv1[h]
                    newv2[h]=fbxv2[h]
                    newv3[h]=fbxv3[h]

                newv1 = SomeMaths.MatrixVector3Product(camera,newv1)
                newv2 = SomeMaths.MatrixVector3Product(camera,newv2)
                newv3 = SomeMaths.MatrixVector3Product(camera,newv3)

                triangle = [ newv1, newv2, newv3 ]
                polygons.append(triangle)


            elif numVertices == 4:
                newv1= [0 for x in range(3)]
                newv2= [0 for x in range(3)]
                newv3= [0 for x in range(3)]
                newv4= [0 for x in range(3)]

                fbxv1 = mesh.GetControlPointAt(mesh.GetPolygonVertex(i,0))
                fbxv2 = mesh.GetControlPointAt(mesh.GetPolygonVertex(i,1))
                fbxv3 = mesh.GetControlPointAt(mesh.GetPolygonVertex(i,2))
                fbxv4 = mesh.GetControlPointAt(mesh.GetPolygonVertex(i,3))

                for h in range(3):
                    newv1[h] = fbxv1[h]
                    newv2[h] = fbxv2[h]
                    newv3[h] = fbxv3[h]
                    newv4[h] = fbxv4[h]

                newv1 = SomeMaths.MatrixVector3Product(camera,newv1)
                newv2 = SomeMaths.MatrixVector3Product(camera,newv2)
                newv3 = SomeMaths.MatrixVector3Product(camera,newv3)
                newv4 = SomeMaths.MatrixVector3Product(camera,newv4)

                quad = [ newv1, newv2, newv3, newv4 ]
                polygons.append(quad)

            else:
                print ("Error! : Number of vertices of polygon %d: %d" % (i,numVertices))
    for i in range(node.GetChildCount()):
        createPolygons(node.GetChild(i),camera)

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

def calculateFactor(maxX,minX,maxY,minY):
      
        fbxHeight = maxY- minY
        fbxWidth = maxX - minX
        fbxXcenter = fbxWidth/2
        fbxYcenter = fbxHeight/2
        heightFactor = fbxHeight/height
        widthFactor = fbxWidth/width
        factor = max(heightFactor,widthFactor)

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

        camera = [[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]]
        print camera
        
        camera = SomeMaths.RotateX(45*rads,camera)
        print camera
        
        maxX = 0
        minX = 0
        maxY = 0
        minY = 0
        fbxBoundaries(scene.GetRootNode(),camera,maxX,minX,maxY,minY)
        factor = calculateFactor(maxX,minX,maxY,minY)
        print factor
        camera = SomeMaths.Scale(factor,camera)
        print camera
     
        createPolygons(scene.GetRootNode(),camera)
        sortPolygons()

        #print polygons

        svgfile = "%s\%s.svg" % (svgpath,file)
        print svgfile

        f = open(svgfile, 'w')
        if  f.errors:
                print ("Problems opening the file %s" % (svgfile))
        #SVG header
        f.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%d" height="%d"> ' % (width,height))
        color = 30
        if len(polygons) == 0:
             print "Error!: polygons lenght = 0"
        else:
            colorIncrement = 69.0/len(polygons)
        xCenter = width - 300
        yCenter = height - 200
        for poly in polygons:
            if len(poly) == 3:
                v1 = poly[0]
                v2 = poly[1]
                v3 = poly[2]

                f.write('<polygon points="')
                f.write('%d,%d %d,%d %d,%d' % (v1[0]+xCenter, yCenter-v1[1], v2[0]+xCenter, yCenter-v2[1], v3[0]+xCenter, yCenter-v3[1]))
                f.write('" style="fill:#%d%d00;stroke:none"/>' % (color,color   ))

            elif len(poly) == 4:
                v1 = poly[0]
                v2 = poly[1]
                v3 = poly[2]
                v4 = poly[3]

                f.write('<polygon points="')
                f.write('%d,%d %d,%d %d,%d %d,%d' % (v1[0]+xCenter, yCenter-v1[1], v2[0]+xCenter, yCenter-v2[1], v3[0]+xCenter, yCenter-v3[1], v4[0]+xCenter, yCenter-v4[1]))
                f.write('" style="fill:#%d%d00;stroke:none"/>' % (color,color))

            else:
                print("Error!:Polygon %d has size: %d" % (poly,len(poly)) )

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

    for file in os.listdir(svgpath):
     if file.endswith(".svg"):
         print svgpath
         svgfile = "%s\%s" % (svgpath,file)
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


