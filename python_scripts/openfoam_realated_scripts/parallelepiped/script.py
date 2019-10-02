######################################################
# BlockMeshDict Generator for Parallelepiped Objects #
######################################################
import numpy as np
from copy import copy as cp

# getting user inputs
tmp1,tmp2,tmp3 = input("Enter minimum corner coordinates : Xmin, Ymin, Zmin : ").split(",")
Xmin = float(tmp1); Ymin = float(tmp2); Zmin = float(tmp3)

tmp1,tmp2,tmp3 = input("Enter maximum corner coordinates : Xmin, Ymin, Zmin : ").split(",")
Xmax = float(tmp1); Ymax = float(tmp2); Zmax = float(tmp3)

tmp1,tmp2,tmp3 = input("Enter a corner vertex coordinates that acts as starting point of Flow Vector : X, Y, Z : ").split(",")
Xi = float(tmp1); Yi = float(tmp2); Zi = float(tmp3)

tmp1,tmp2,tmp3 = input("Enter a corner vertex coordinates that acts as ending point of Flow Vector : X, Y, Z : ").split(",")
Xo = float(tmp1); Yo = float(tmp2); Zo = float(tmp3)

# creating coordinates of the parallelepiped object
c0 = np.array([Xmin, Ymin, Zmin])
c1 = np.array([Xmin, Ymin, Zmax])
c2 = np.array([Xmax, Ymin, Zmax])
c3 = np.array([Xmax, Ymin, Zmin])
c4 = np.array([Xmin, Ymax, Zmin])
c5 = np.array([Xmin, Ymax, Zmax])
c6 = np.array([Xmax, Ymax, Zmax])
c7 = np.array([Xmax, Ymax, Zmin])

# determining inlet and outlet vertex number
clists = [c0,c1,c2,c3,c4,c5,c6,c7]

for i in range(np.shape(clists)[0]):
    if ([Xi,Yi,Zi] == clists[i]).all():
        IV = cp(i)
    if ([Xo,Yo,Zo] == clists[i]).all():
        OV = cp(i)
#
try:
    IV
except NameError:
    raise NameError("Starting point of Flow Vector is not a corner point!!")

try:
    OV
except NameError:
    raise NameError("Ending point of Flow Vector is not a corner point!!")

# determining face numbers for inlet outlet and walls
facelists = np.array([[0,1,2,3],
             [4,5,6,7],
             [1,2,6,5],
             [2,6,7,3],
             [3,0,4,7],
             [0,1,5,4]])

WALLS = []
for lis in facelists:
    if (IV == lis).any() and (OV != lis).all():
        INLET = cp(lis)
    elif (OV == lis).any() and (IV != lis).all():
        OUTLET = cp(lis)
    else:
        WALLS.append(lis)

# creating blockMeshDict file
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
fid.writelines("    ("+str(c0[0])+" "+str(c0[1])+" "+str(c0[2])+" ) // 0\n")
fid.writelines("    ("+str(c1[0])+" "+str(c1[1])+" "+str(c1[2])+" ) // 1\n")
fid.writelines("    ("+str(c2[0])+" "+str(c2[1])+" "+str(c2[2])+" ) // 2\n")
fid.writelines("    ("+str(c3[0])+" "+str(c3[1])+" "+str(c3[2])+" ) // 3\n")
fid.writelines("    ("+str(c4[0])+" "+str(c4[1])+" "+str(c4[2])+" ) // 4\n")
fid.writelines("    ("+str(c5[0])+" "+str(c5[1])+" "+str(c5[2])+" ) // 5\n")
fid.writelines("    ("+str(c6[0])+" "+str(c6[1])+" "+str(c6[2])+" ) // 6\n")
fid.writelines("    ("+str(c7[0])+" "+str(c7[1])+" "+str(c7[2])+" ) // 7\n")
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
fid.writelines("    inlet\n")
fid.writelines("    {\n")
fid.writelines("        type patch;\n")
fid.writelines("        faces\n")
fid.writelines("        (\n")
fid.writelines("            ("+str(INLET[0])+" "+str(INLET[1])+" "+str(INLET[2])+" "+str(INLET[3])+")\n")
fid.writelines("        );\n")
fid.writelines("    }\n")
fid.writelines("    outlet\n")
fid.writelines("    {\n")
fid.writelines("        type patch;\n")
fid.writelines("        faces\n")
fid.writelines("        (\n")
fid.writelines("            ("+str(OUTLET[0])+" "+str(OUTLET[1])+" "+str(OUTLET[2])+" "+str(OUTLET[3])+")\n")
fid.writelines("        );\n")
fid.writelines("    }\n")
fid.writelines("    walls\n")
fid.writelines("    {\n")
fid.writelines("        type wall;\n")
fid.writelines("        faces\n")
fid.writelines("        (\n")
fid.writelines("            ("+str(WALLS[0][0])+" "+str(WALLS[0][1])+" "+str(WALLS[0][2])+" "+str(WALLS[0][3])+")\n")
fid.writelines("            ("+str(WALLS[1][0])+" "+str(WALLS[1][1])+" "+str(WALLS[1][2])+" "+str(WALLS[1][3])+")\n")
fid.writelines("            ("+str(WALLS[2][0])+" "+str(WALLS[2][1])+" "+str(WALLS[2][2])+" "+str(WALLS[2][3])+")\n")
fid.writelines("            ("+str(WALLS[3][0])+" "+str(WALLS[3][1])+" "+str(WALLS[3][2])+" "+str(WALLS[3][3])+")\n")
fid.writelines("        );\n")
fid.writelines("    }\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("// ************************************************************************* //\n")
fid.close()

print("\n Block Mesh dictionary is successfuly written")

