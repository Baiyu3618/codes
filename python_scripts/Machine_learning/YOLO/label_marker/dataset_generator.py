#########################################
# YOLO dataset Y data generation script #
#########################################
import numpy as np
import pandas as pd

# reading the dataset
fid = pd.read_csv("DataSet.csv")

# setting up parameters
nx = 3                          # grid cell size
ny = 3
nAnchor = 2                     # bo of anchor boxes
nParams = 5                     # no of yolo parameters : Pc bx by bw bh

# initializing ydata
images = fid["image"].unique()

ydata = np.zeros([len(images),nx,ny,nAnchor*nParams])

# ydata construction begin
count = 0
for img in images:
    # reading datasets containing same image
    tmp = fid[fid["image"] == img]

    # going through individual entries
    for i in range(tmp.shape[0]):
        # determining centroid
        xc = np.mean([tmp["x1"].iloc[i], tmp["x2"].iloc[i]])
        yc = np.mean([tmp["y1"].iloc[i], tmp["y2"].iloc[i]])

        # creating bins
        xbins = np.linspace(0,tmp["width"].iloc[i],nx+1)
        ybins = np.linspace(0,tmp["height"].iloc[i],ny+1)

        # getting grid location
        xloc = np.digitize(xc,xbins) - 1
        yloc = np.digitize(yc,ybins) - 1

        # calculating box width and box height
        box_width = tmp["width"].iloc[i]/nx
        box_height = tmp["height"].iloc[i]/ny

        # calculating relative centroid
        bx = (xc - xbins[xloc])/box_width
        by = (yc - ybins[yloc])/box_height

        # calculating crop width and height
        bw = (tmp["x2"].iloc[i] - tmp["x1"].iloc[i])/box_width
        bh = (tmp["y2"].iloc[i] - tmp["y1"].iloc[i])/box_height

        # updating ydata
        if ydata[count, xloc, yloc, 0] != 0: # Pc 1st anchor
            if ydata[count, xloc, yloc, 5] != 0: # Pc 2nd anchor
                print("Error!, insufficient Anchorbox count!")
                print("Increase Anchorbox count or increase grid size")
                print("Error image: ",tmp["image"].iloc[i])
                continue
            ydata[count, xloc,yloc, 5] = 1 # registering object presence
            ydata[count, xloc,yloc, 6] = bx # box centroid x
            ydata[count, xloc,yloc, 7] = by # box centroid y
            ydata[count, xloc,yloc, 8] = bw # box width
            ydata[count, xloc,yloc, 9] = bh # box height
        else:
            ydata[count, xloc,yloc, 0] = 1 # registering object presence
            ydata[count, xloc,yloc, 1] = bx # box centroid x
            ydata[count, xloc,yloc, 2] = by # box centroid y
            ydata[count, xloc,yloc, 3] = bw # box width
            ydata[count, xloc,yloc, 4] = bh # box height
    #
    count += 1
