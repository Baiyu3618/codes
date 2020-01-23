###################################
# YOLO dataset preparation script #
###################################
from matplotlib.widgets import RectangleSelector
import matplotlib.image as img
import numpy as np
import matplotlib.pyplot as plt
import os,glob, pandas as pd


def line_select_callback(eclick, erelease):
    'eclick and erelease are the press and release events'
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    _ = os.system("echo \""+name+","+str(width)+","+str(height)+","+str(x1)+","+str(y1)+","+str(x2)+","+str(y2)+"\">> DataSet.csv")

def toggle_selector(event):
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)
#

# main function
fnames = sorted(glob.glob1(os.getcwd(),"*.jpg"))

os.system("rm -f DataSet.csv") #
os.system("echo \"image,width,height,x1,y1,x2,y2\" >> DataSet.csv")

for name in fnames:
    fig, current_ax = plt.subplots()                 # make a new plotting range

    image = img.imread(name)
    plt.imshow(image)

    height,width,_ = image.shape

    print("\n current image : ",name)

    # drawtype is 'box' or 'line' or 'none'
    toggle_selector.RS = RectangleSelector(current_ax, line_select_callback,
                                           drawtype='box', useblit=True,
                                           button=[1, 3],  # don't use middle button
                                           minspanx=5, minspany=5,
                                           spancoords='pixels',
                                           interactive=True)
    plt.connect('key_press_event', toggle_selector)
    plt.show()
