# this script is for renaming the files in current directory
import os,glob

# getting all the filenames
files = sorted(glob.glob1(os.getcwd(),"*.png"))

# renaming files through loop
for file in files:
    # spliting the filename
    txt = file.split(".")

    # getting current id and renaming it to convention
    idname = int(txt[0])+1000

    # creating renamed file
    name = str(idname)+".png"

    # creating shell command
    cmd = "mv "+file+" "+name

    # executing shell command
    status = os.system(cmd)

print("done")
