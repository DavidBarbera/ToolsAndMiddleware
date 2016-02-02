import os
import FbxCommon
import math


#Globals
width = 500
height = 500

camera = [[1, 0, 0],
          [0, 1, 0],
          [0, 0, 1]]

def scale(a):
    rot = [[a, 0, 0],
          [0, a, 0],
          [0, 0, a]]

    result = [[0 for x in range(3)] for x in range(3)]

    for i in range(3):
        for j in range(3):
            result[i][j] = camera[i][0]*rot[0][j] + camera[i][1]*rot[1][j] + camera[i][2]*rot[2][j]

    for i in range(3):
        for j in range(3):
            camera[i][j] = result[i][j]

def rotateX(a):
    rot = [[1, 0, 0],
           [0, math.cos(a), -math.sin(a)],
           [0, math.sin(a), math.cos(a)]]

    result = [[0 for x in range(3)] for x in range(3)] 

    for i in range(3):
        for j in range(3):
            result[i][j] = camera[i][0]*rot[0][j] + camera[i][1]*rot[1][j] + camera[i][2]*rot[2][j]

    for i in range(3):
        for j in range(3):
            camera[i][j] = result[i][j]

def rotateY(a):
    rot = [[ math.cos(a), 0, math.sin(a)],
           [0, 1, 0],
           [-math.sin(a), 0, math.cos(a)]]

    result = [[0 for x in range(3)] for x in range(3)] 

    for i in range(3):
        for j in range(3):
            result[i][j] = camera[i][0]*rot[0][j] + camera[i][1]*rot[1][j] + camera[i][2]*rot[2][j]

    for i in range(3):
        for j in range(3):
            camera[i][j] = result[i][j]

def rotateZ(a):
    rot = [[math.cos(a), -math.sin(a),0],
           [ math.sin(a), math.cos(a),0],
           [0,0,1]]

    result = [[0 for x in range(3)] for x in range(3)] 

    for i in range(3):
        for j in range(3):
            result[i][j] = camera[i][0]*rot[0][j] + camera[i][1]*rot[1][j] + camera[i][2]*rot[2][j]

    for i in range(3):
        for j in range(3):
            camera[i][j] = result[i][j]


def get_projection(node):
    

    mesh = node.GetMesh()
  
    if not mesh:
        print("not mesh")
    else:
        for i in mesh.GetPolygonVertices():
            point = mesh.GetControlPointAt(i)
            vertex = [0 for x in range(3)]
            vertex[0] = point[0]*camera[0][0] + point[1]*camera[1][0] + point[2]*camera[2][0]
            vertex[1] = point[0]*camera[0][1] + point[1]*camera[1][1] + point[2]*camera[2][1]
            vertex[2] = point[0]*camera[0][2] + point[1]*camera[1][2] + point[2]*camera[2][2]
            f.write('%d,%d ' % (vertex[0] + width/2, height/2 - vertex[1]))    #Only 2 first components as .svg is 2D

    for i in range(node.GetChildCount()):
        
        get_projection(node.GetChild(i))

        
#Create path variables destined to create/locate .svg files
svgpath = os.getcwd()
svgpath +="\SVG_files"

#Clear SVG directory of .svg files
for file in os.listdir(svgpath):
    if file.endswith(".svg"):
        svgfile = "%s\%s" % (svgpath,file)
        print "%s removed" % (file)
        os.remove(svgfile)


#Create path variables destined to locate .fbx files
fbxpath = os.getcwd()
fbxpath +="\FBX_files"
print fbxpath

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

        scale(4)
        rotateX(45)

        svgfile = "%s\%s.svg" % (svgpath,file)
        print svgfile
        f = open(svgfile, 'w')
        if  f.errors:
            print ("Problems opening the file %s" % (svgfile))

        f.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%d" height="%d"> ' % (width,height))
        f.write('<polygon points="')
        get_projection(scene.GetRootNode())
        f.write('" stroke="darkred" stroke-width="0.2" fill="none" />')
        f.write('</svg>')
        f.close()



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