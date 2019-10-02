#################################################################
# Bounding box generator for OpenFOAM for given geometry in stl #
#################################################################
import numpy as np
import re
from copy import copy as cp

# file name of the geometry
file = input("Enter Filename with extension : ")

# regular expressions for getting only coordinates from file
exp1 = re.compile("\s*\w+\s[-+]?\d+\.*\d*\w*[-+]?\d*\s[-+]?\d+\.*\d*\w*[-+]?\d*\s[-+]?\d+\.*\d*\w*[-+]?\d*", re.DOTALL)
exp2 = re.compile("[-+]?\d+\.*\d*\w*[-+]?\d*")

fid = open(file,"r")

# reading the first point to get the first set of coordinates that is with geometry
print("Computing minimum and maximum coordinates ... ")
for line in fid:

    result1 = exp1.match(line) # filtering to lines that contain coordinates

    if result1:
        result2 = exp2.findall(line) # filtering to get the coordinates
        X = float(result2[0])
        Y = float(result2[1])
        Z = float(result2[2])

        break
#

Xmax = cp(X); Ymax = cp(Y); Zmax = cp(Z)
Xmin = cp(X); Ymin = cp(Y); Zmin = cp(Z)

# reading set of points and determining minimum and maximum coordinates of the geometry
for line in fid:

    result1 = exp1.match(line) # filtering to lines that contain coordinates

    if result1:
        result2 = exp2.findall(line) # filtering to get the coordinates
        X = float(result2[0])
        Y = float(result2[1])
        Z = float(result2[2])

        if X>Xmax:              # X max and min
            Xmax = cp(X)
        elif X<Xmin:
            Xmin = cp(X)
        #
        if Y>Ymax:              # Y max and min
            Ymax = cp(Y)
        elif Y<Ymin:
            Ymin = cp(Y)
        #
        if Z>Zmax:              # Z max and min
            Zmax = cp(Z)
        elif Z<Zmin:
            Zmin = cp(Z)
        #        
#
fid.close()

print("Done")

# creating bounding box blockMeshDict file
fid = open("blockMeshDict","w")
fid.writelines("/*--------------------------------*- C++ -*----------------------------------*\ \n")
fid.writelines("  =========                 |\n")
fid.writelines("  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox\n")
fid.writelines("   \\    /   O peration     | Website:  https://openfoam.org\n")
fid.writelines("    \\  /    A nd           | Version:  6\n")
fid.writelines("     \\/     M anipulation  |\n")
fid.writelines("\*---------------------------------------------------------------------------*/\n")
fid.writelines("FoamFile\n")
fid.writelines("{\n")
fid.writelines("    version     2.0;\n")
fid.writelines("    format      ascii;\n")
fid.writelines("    class       dictionary;\n")
fid.writelines("    object      blockMeshDict;\n")
fid.writelines("}\n")
fid.writelines("\n")
fid.writelines("// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n")
fid.writelines("\n")
fid.writelines("\n")
fid.writelines("convertToMeters 1;\n")
fid.writelines("\n")
fid.writelines("vertices\n")
fid.writelines("(\n")
fid.writelines("    ("+str(Xmin)+" "+str(Ymin)+" "+str(Zmin)+" ) // 0\n")
fid.writelines("    ("+str(Xmin)+" "+str(Ymin)+" "+str(Zmax)+" ) // 1\n")
fid.writelines("    ("+str(Xmax)+" "+str(Ymin)+" "+str(Zmax)+" ) // 2\n")
fid.writelines("    ("+str(Xmax)+" "+str(Ymin)+" "+str(Zmin)+" ) // 3\n")
fid.writelines("    ("+str(Xmin)+" "+str(Ymax)+" "+str(Zmin)+" ) // 4\n")
fid.writelines("    ("+str(Xmin)+" "+str(Ymax)+" "+str(Zmax)+" ) // 5\n")
fid.writelines("    ("+str(Xmax)+" "+str(Ymax)+" "+str(Zmax)+" ) // 6\n")
fid.writelines("    ("+str(Xmax)+" "+str(Ymax)+" "+str(Zmin)+" ) // 7\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("blocks\n")
fid.writelines("(\n")
fid.writelines(" hex (0 1 2 3 4 5 6 7) (10 10 10) simpleGrading (1 1 1)\n")
fid.writelines(" \n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("edges\n")
fid.writelines("(\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("boundary\n")
fid.writelines("(\n")
fid.writelines("    \n")
fid.writelines("    defaultFaces\n")
fid.writelines("    {\n")
fid.writelines("        type patch;\n")
fid.writelines("        faces\n")
fid.writelines("        (\n")
fid.writelines("            (0 1 5 4)\n")
fid.writelines("            (3 0 4 7)\n")
fid.writelines("            (2 3 7 6)\n")
fid.writelines("            (1 2 6 5)\n")
fid.writelines("            (0 1 2 3)\n")
fid.writelines("            (4 5 6 7)\n")
fid.writelines("        );\n")
fid.writelines("    }\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("// ************************************************************************* //\n")
fid.close()

print("\n Block Mesh dictionary is successfuly written")


