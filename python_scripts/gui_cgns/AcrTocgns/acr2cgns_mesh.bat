echo off
pushd dist
set dType="unstructured"
set xyz= "Z:\home\ramkumar\Desktop\Working_Directory\gui_cgns\trial_files\trial.xyz"
set hyb= "Z:\home\ramkumar\Desktop\Working_Directory\gui_cgns\trial_files\trial.hyb"
set loc= "Z:\home\ramkumar\Desktop\Working_Directory\gui_cgns\trial_files\trial.loc"

C:\jdk1.8.0\bin\java.exe -Djava.library.path=..\src\;lib\* -jar AcrTocgns.jar %dType% %xyz% %hyb% %loc%
popd 
