echo off
pushd dist
dType="unstructured"
xyz= "..\src\acrtocgns\3d_unstru\lid_unstr_small.xyz"
hyb= "..\src\acrtocgns\3d_unstru\lid_unstr_small.hyb"
loc= "..\src\acrtocgns\3d_unstru\lid_unstr_small.inp"

JAVA_HOME=/usr/local/jdk1.8.0
${JAVA_HOME}/bin/java -Djava.library.path=../src/;lib/* -jar AcrTocgns.jar ${dType} ${xyz} ${hyb} ${loc}
popd 
