#########################################################
# GUI script for cgns converter using Tkinter in python #
# developed by Ramkumar                                 #
#########################################################
import tkinter
from tkinter import ttk,filedialog
import os,subprocess

# creating class to group all the objects
class converter(ttk.Frame):
    # creating parent function
    def __init__(self,parent,*args,**kwargs):
        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.root=parent
        self.init_gui()
        self.status_label["text"] = "Ready!"
    
    # button functions
    def xyz_selector(self):     # function to select grid file
        txt = filedialog.askopenfilename(filetypes = [("Grid Files", "*.xyz")])
        self.xyz.set(txt)
        htxt = txt[:-3]+"hyb"
        ltxt = txt[:-3]+"loc"
        ltxt_inp = txt[:-3]+"inp"
        if os.path.exists(htxt):
            self.hyb.set(htxt)      # these lines preset other hyb and loc file locations
        if os.path.exists(ltxt):
            self.loc.set(ltxt)
        elif os.path.exists(ltxt_inp):
            self.loc.set(ltxt_inp)
                                    
    def hyb_selector(self):     # function to select hybrid file
        txt = filedialog.askopenfilename(filetypes = [("Hybrid Files", "*.hyb")])
        self.hyb.set(txt)
        xtxt = txt[:-3]+"xyz"
        ltxt = txt[:-3]+"loc"
        ltxt_inp = txt[:-3]+"inp"
        if os.path.exists(xtxt):
            self.xyz.set(xtxt)      # these lines preset other file locations
        if os.path.exists(ltxt):
            self.loc.set(ltxt)
        elif os.path.exists(ltxt_inp): # takes inp if loc is missing
            self.loc.set(ltxt_inp)
                                    
    def loc_selector(self):     # function to select location file
        txt = filedialog.askopenfilename(filetypes = [("Region/Input Files", "*.loc *.inp")])
        self.loc.set(txt)
        htxt = txt[:-3]+"hyb"
        xtxt = txt[:-3]+"xyz"
        if os.path.exists(htxt):
            self.hyb.set(htxt)      # these lines preset other hyb and loc file locations
        if os.path.exists(xtxt):
            self.xyz.set(xtxt)

    def file_converter(self):   # function that invokes conversion
        if not(os.path.exists(self.xyz.get())):
            self.status_label["text"] = "Grid file is missing"
            self.status_label["fore"] = "red"
            return
        if not(os.path.exists(self.hyb.get())):
            self.status_label["text"] = "Hybrid file is missing"
            self.status_label["fore"] = "red"
            return
        if not(os.path.exists(self.loc.get())):
            self.status_label["text"] = "Regions/Input file is missing"
            self.status_label["fore"] = "red"
            return
        if not(os.path.exists("/home/ramkumar/RAMKUMAR_FILES/Codes/ram/gui_cgns/AcrTocgns")):
            self.status_label["text"] = "\"AcrTocgns\" doesn't exist in \n current working directory"
            self.status_label["fore"] = "red"
            return
        if not(os.path.exists("/home/ramkumar/RAMKUMAR_FILES/Codes/ram/gui_cgns/AcrTocgns/acr2cgns_mesh.bat")):
            self.status_label["text"] = "\"acr2cgns_mesh.bat\" file \n is missing in \"AcrTocgns\" \n directory"
            self.status_label["fore"] = "red"
            return
        
        self.status_label["text"] = "All files read successfully"
        self.status_label["fore"] = "blue"
        
        tmp = self.xyz.get()[:-3]+"cgns"
        
        if os.path.exists(tmp): # checking for previous cgns file existence
            self.status_label["text"] = "removing old cgns file"
            os.system("rm " + tmp)
        
        os.chdir("/home/ramkumar/RAMKUMAR_FILES/Codes/ram/gui_cgns/AcrTocgns")    
        fid = open("acr2cgns_mesh.bat","r")
        txt = fid.readlines()
        fid.close()
        
        txt[3] = "set xyz= \"" + self.xyz.get() + "\"\n"
        txt[4] = "set hyb= \"" + self.hyb.get() + "\"\n"
        txt[5] = "set loc= \"" + self.loc.get() + "\"\n"

        txt = txt + ["cmd /k"]  # to prevent cmd from closing after its done

        fid1 = open("windows.bat","w",newline = '\r\n')
        fid1.writelines(txt)
        fid1.close()
        
        temp = subprocess.call(("wineconsole","windows.bat")) # os.system detaches this process and doesnot wait till it completes, so only subprocess
        os.chdir("..")
    
        if os.path.exists(tmp):
            self.status_label["text"] = "File created!"
            self.status_label["fore"] = "blue"
        else:
            self.status_label["text"] = "file not created!, \n some error with core converter!"
            self.status_label["fore"] = "orange"

    # reset function definition
    def reset_call(self):
        self.status_label["text"] = "Ready!"
        self.status_label["fore"] = "blue"
        self.xyz.set("")
        self.hyb.set("")
        self.loc.set("")
            
    # gui initializer function
    def init_gui(self):

        # intermediate variables
        self.xyz = tkinter.StringVar()
        self.hyb = tkinter.StringVar()
        self.loc = tkinter.StringVar()
        
        self.root.title(string = "ACRi CGNS Converter V1.0")
        self.root.option_add('*tearOFF',"False")
        self.root.minsize(width = 470, height = 200)
        self.root.maxsize(width = 470, height = 200)

        self.grid(column = 0, row = 0, sticky='news')

        # creating the primary heading label
        ttk.Label(self, text = "\r ACR to CGNS Converter", anchor = "center").grid(column=0,row=0,columnspan=5,sticky='ew')

        # separator for title and body
        ttk.Separator(self, orient = "horizontal").grid(column = 0, row = 1, columnspan = 7, sticky = 'ew')

        # creating text entries for file addresses
        self.xyz_entry = ttk.Entry(self, width = 20, textvariable = self.xyz).grid(column = 2, row = 2)
        self.hyb_entry = ttk.Entry(self, width = 20, textvariable = self.hyb).grid(column = 2, row = 3)
        self.loc_entry = ttk.Entry(self, width = 20, textvariable = self.loc).grid(column = 2, row = 4)

        # creating labels for respective entry boxes
        ttk.Label(self, text = "Grid File Location (*.xyz)", anchor = "e").grid(column = 1, row = 2)
        ttk.Label(self, text = "Connectivity File Location (*.hyb)", anchor = "e").grid(column = 1, row = 3)
        ttk.Label(self, text = "Regions or Input File\n Location (*.loc *.inp)", anchor = "e").grid(column = 1, row = 4)

        # cover up box separator right
        ttk.Separator(self, orient = "vertical").grid(column = 4, row = 1, rowspan = 4, sticky = 'ns')

        # creating buttons for respective boxes
        self.button_xyz = ttk.Button(self, text="Locate",command=self.xyz_selector).grid(column = 3, row = 2)
        self.button_hyb = ttk.Button(self, text="Locate",command=self.hyb_selector).grid(column = 3, row = 3)
        self.button_loc = ttk.Button(self, text="Locate",command=self.loc_selector).grid(column = 3, row = 4)

        # cover up box separator left
        ttk.Separator(self, orient = "vertical").grid(column = 0, row = 1, rowspan = 4, sticky = 'ns')
        # cover up box separator bottom
        ttk.Separator(self, orient = "horizontal").grid(column = 0, row = 5, columnspan = 7, sticky = 'ew')

        # adding a status frame for getting status of output
        self.status_frame = ttk.LabelFrame(self, text = "Status", height = 10, width = 100)
        self.status_frame.grid(column = 1, row = 6,columnspan = 1, sticky = 'sw')
        self.status_label = ttk.Label(self.status_frame, text = ' ', fore = 'blue')
        self.status_label.grid(column=0,row = 0)

        # adding convert button on frame
        self.button_convert = ttk.Button(self, text="Convert",command = self.file_converter).grid(column = 2, row = 6)

        # adding reset button on frame
        self.button_reset = ttk.Button(self, text="Reset", command = self.reset_call).grid(column = 3, row = 6)

if __name__=="__main__":
    root = tkinter.Tk()
    converter(root)
    root.mainloop()
