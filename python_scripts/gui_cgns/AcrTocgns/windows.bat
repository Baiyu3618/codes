echo off
pushd dist
set dType="unstructured"
set xyz= "/home/ramkumar/Desktop/Working_Directory/Anupravaha/Problem_12_slice/41X20X81/hybrid/P_12_geom_41X20X81.xyz"
set hyb= "/home/ramkumar/Desktop/Working_Directory/Anupravaha/Problem_12_slice/41X20X81/hybrid/P_12_geom_41X20X81.hyb"
set loc= "/home/ramkumar/Desktop/Working_Directory/Anupravaha/Problem_12_slice/41X20X81/hybrid/P_12_geom_41X20X81.loc"

C:\jdk1.8.0\bin\java.exe -Djava.library.path=..\src\;lib\* -jar AcrTocgns.jar %dType% %xyz% %hyb% %loc%
popd 
cmd /k