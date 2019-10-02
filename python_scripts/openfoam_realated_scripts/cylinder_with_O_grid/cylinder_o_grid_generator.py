###########################################
# Cylinder BlockMeshDict Generator Script #
# Python 3.7                              #
###########################################

import numpy as np
import warnings, sys

# function definitions
def norm_vec(n):
    # getting an in-plane vector, by simple manipulation
    # m = [3.0*n[0], n[1], n[2]]
    m = [n[2], 0.0, n[0]]

    # normal vector to that plane formed by n and m
    N = np.cross(n,m); N = N/np.sqrt(np.sum(N**2))

    # normal vector to the plane formed by n and N
    P = np.cross(n,N); P = P/np.sqrt(np.sum(P**2))

    return N,P

def copy_points(N,P,r,a,b,ratio):
    # inputs required, two normal vectors N & P,
    # distance to which the point has to be moved, r
    # source points, a & B

    v1 = a + r*N
    v2 = a - r*N
    v3 = a + r*P
    v4 = a - r*P

    v5 = a + ratio*r*N
    v6 = a - ratio*r*N
    v7 = a + ratio*r*P
    v8 = a - ratio*r*P

    v9 = b + r*N
    v10 = b - r*N
    v11 = b + r*P
    v12 = b - r*P

    v13 = b + ratio*r*N
    v14 = b - ratio*r*N
    v15 = b + ratio*r*P
    v16 = b - ratio*r*P

    points = [v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16]

    # arc point b/w v9 and v10 as well as v11 and v12
    v1n = v1-a; v2n = v2-a; v3n = v3-a; v4n = v4-a
    A_13n = (v1n+v3n)/np.sqrt(np.sum((v1n+v3n)**2))
    A_13 = a + r*A_13n
    A_24 = a - r*A_13n

    A_23n = (v2n + v3n)/np.sqrt(np.sum((v2n+v3n)**2))
    A_23 = a + r*A_23n
    A_41 = a - r*A_23n

    v9n = v9-b; v11n = v11-b; v10n = v10-b; v12n = v12-b
    A_911n = (v9n + v11n)/np.sqrt(np.sum((v9n+v11n)**2))
    A_911 = b + r*A_911n
    A_1012 = b - r*A_911n

    A_1110n = (v11n+v10n)/np.sqrt(np.sum((v11n+v10n)**2))
    A_1110 = b + r*A_1110n
    A_129 = b - r*A_1110n
    
    arc_points = np.array([A_13,A_24,A_23,A_41,A_911,A_1012,A_1110,A_129])
    
    return points, arc_points
#

# input axial vector
# a1 = 0.0; a2 = 1.0
# b1 = 0.0; b2 = 0.0
# c1 = 0.0; c2 = 0.0
p1 = input("Enter first point coordinates : x,y,z :")
p2 = input("Enter second point coordinates : x,y,z :")

a1,b1,c1 = p1.split(","); a1 = float(a1); b1 = float(b1); c1 = float(c1)
a2,b2,c2 = p2.split(","); a2 = float(a2); b2 = float(b2); c2 = float(c2)

a = np.array([a1,b1,c1]); b = np.array([a2,b2,c2])

A = [a2-a1, b2-b1, c2-c1]       # axial vector of cylinder

# input radius
r = float(input("Enter radius :"))

# ratio of box side along radial direction
ratio = float(input("Enter radial box size ratio : (0.1 - 0.9) :"))

# determining a normal vector to the axial vector
N,P = norm_vec(A)

points, arc_points = copy_points(N,P,r,a,b,ratio)

# # writing to a file
# fid = open("points.txt","w")

# for i in range(np.shape(points)[0]):
#     fid.writelines(str(points[i])+"\n")
# #
# fid.writelines("\n\n Arc points\n")
# for i in range(np.shape(arc_points)[0]):
#     fid.writelines(str(arc_points[i])+"\n")
# #
# fid.close()

# creating blockMeshDict file

fid = open("blockMeshDict","w")
fid.writelines("/*--------------------------------*- C++ -*----------------------------------*\\n")
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
fid.writelines("    ("+str(points[0][0])+" "+str(points[0][1])+" "+str(points[0][2])+" ) // 0\n")
fid.writelines("    ("+str(points[1][0])+" "+str(points[1][1])+" "+str(points[1][2])+" ) // 1\n")
fid.writelines("    ("+str(points[2][0])+" "+str(points[2][1])+" "+str(points[2][2])+" ) // 2\n")
fid.writelines("    ("+str(points[3][0])+" "+str(points[3][1])+" "+str(points[3][2])+" ) // 3\n")
fid.writelines("    ("+str(points[4][0])+" "+str(points[4][1])+" "+str(points[4][2])+" ) // 4\n")
fid.writelines("    ("+str(points[5][0])+" "+str(points[5][1])+" "+str(points[5][2])+" ) // 5\n")
fid.writelines("    ("+str(points[6][0])+" "+str(points[6][1])+" "+str(points[6][2])+" ) // 6\n")
fid.writelines("    ("+str(points[7][0])+" "+str(points[7][1])+" "+str(points[7][2])+" ) // 7\n")
fid.writelines("    ("+str(points[8][0])+" "+str(points[8][1])+" "+str(points[8][2])+" ) // 8\n")
fid.writelines("    ("+str(points[9][0])+" "+str(points[9][1])+" "+str(points[9][2])+" ) // 9\n")
fid.writelines("    ("+str(points[10][0])+" "+str(points[10][1])+" "+str(points[10][2])+" ) // 10\n")
fid.writelines("    ("+str(points[11][0])+" "+str(points[11][1])+" "+str(points[11][2])+" ) // 11\n")
fid.writelines("    ("+str(points[12][0])+" "+str(points[12][1])+" "+str(points[12][2])+" ) // 12\n")
fid.writelines("    ("+str(points[13][0])+" "+str(points[13][1])+" "+str(points[13][2])+" ) // 13\n")
fid.writelines("    ("+str(points[14][0])+" "+str(points[14][1])+" "+str(points[14][2])+" ) // 14\n")
fid.writelines("    ("+str(points[15][0])+" "+str(points[15][1])+" "+str(points[15][2])+" ) // 15\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("blocks\n")
fid.writelines("(\n")
fid.writelines(" hex (0 2 6 4 8 10 14 12) (10 10 20) simpleGrading (1 1 1)\n")
fid.writelines(" hex (2 1 5 6 10 9 13 14) (10 10 20) simpleGrading (1 1 1)\n")
fid.writelines(" hex (1 3 7 5 9 11 15 13) (10 10 20) simpleGrading (1 1 1)\n")
fid.writelines(" hex (3 0 4 7 11 8 12 15) (10 10 20) simpleGrading (1 1 1)\n")
fid.writelines(" hex (4 6 5 7 12 14 13 15) (10 10 20) simpleGrading (1 1 1)\n")
fid.writelines(" \n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("edges\n")
fid.writelines("(\n")
fid.writelines(" arc 0 2 ("+str(arc_points[0][0])+" "+str(arc_points[0][1])+" "+str(arc_points[0][2])+" ) \n")
fid.writelines(" arc 1 3 ("+str(arc_points[1][0])+" "+str(arc_points[1][1])+" "+str(arc_points[1][2])+" ) \n")
fid.writelines(" arc 1 2 ("+str(arc_points[2][0])+" "+str(arc_points[2][1])+" "+str(arc_points[2][2])+" ) \n")
fid.writelines(" arc 3 0 ("+str(arc_points[3][0])+" "+str(arc_points[3][1])+" "+str(arc_points[3][2])+" ) \n")
fid.writelines(" arc 8 10 ("+str(arc_points[4][0])+" "+str(arc_points[4][1])+" "+str(arc_points[4][2])+" ) \n")
fid.writelines(" arc 9 11 ("+str(arc_points[5][0])+" "+str(arc_points[5][1])+" "+str(arc_points[5][2])+" ) \n")
fid.writelines(" arc 10 9 ("+str(arc_points[6][0])+" "+str(arc_points[6][1])+" "+str(arc_points[6][2])+" ) \n")
fid.writelines(" arc 11 8 ("+str(arc_points[7][0])+" "+str(arc_points[7][1])+" "+str(arc_points[7][2])+" ) \n")
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
fid.writelines("            (0 2 6 4)\n")
fid.writelines("            (2 1 5 6)\n")
fid.writelines("            (1 3 7 5)\n")
fid.writelines("            (3 0 4 7)\n")
fid.writelines("            (4 6 5 7)\n")
fid.writelines("        );\n")
fid.writelines("    }\n")
fid.writelines("    outlet\n")
fid.writelines("    {\n")
fid.writelines("        type patch;\n")
fid.writelines("        faces\n")
fid.writelines("        (\n")
fid.writelines("            (8 10 14 12)\n")
fid.writelines("            (10 9 13 14)\n")
fid.writelines("            (9 11 15 13)\n")
fid.writelines("            (11 8 12 15)\n")
fid.writelines("            (12 14 13 15)\n")
fid.writelines("        );\n")
fid.writelines("    }\n")
fid.writelines("    walls\n")
fid.writelines("    {\n")
fid.writelines("        type wall;\n")
fid.writelines("        faces\n")
fid.writelines("        (\n")
fid.writelines("            (0 2 10 8)\n")
fid.writelines("            (2 1 9 10)\n")
fid.writelines("            (1 3 11 9)\n")
fid.writelines("            (3 0 8 11)\n")
fid.writelines("        );\n")
fid.writelines("    }\n")
fid.writelines(");\n")
fid.writelines("\n")
fid.writelines("// ************************************************************************* //\n")
fid.close()

print("\n Block Mesh dictionary is successfuly written")
