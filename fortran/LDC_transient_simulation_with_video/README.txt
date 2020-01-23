this is the LDC simulation for Re10000, main motive is to create a video
of the transient simulation

makefile can be used to initiate the computation

it will make two directories and dump the contours of timestep needed
the frequency of dump can be adjusted with inner and outer loop iterations

current simulation is set to use the following data

Re=10000
L and W  = 0.1
MXN = 129X129
dtmax = 0.0053
dt_chosen = 5.0e-4
Uplate = 0.14604
one Cycle time  = 2.73 secs
sim time chosen = 12s

plot break at each 50th step
plot intervals = 0.025 s of sim time

no of plots 480


after simulation complete, copy the renamer python script within velocity and pressure directories
to rename the files for sorting purpose

to create the movie, install ffmpeg and use following command

ffmpeg -f image2 -r 20 -pattern_type glob -i '*.png' output.mp4
