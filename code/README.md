# Code Folder 

This is our code folder. When running the python script, make sure that you DO NOT CHANGE THE FOLDER STRUCTURE. Otherwise, the script will not find the images it needs to import.

# Reproducibility

Our simulations are based on a single python program which can be opened , edit,and run with various Python Environments. 
We used the following packages: tkinter, numpy, random, time, PIL, csv


**Light Test instructions**:
Please ensure that you have installed all of the packages mentioned above, the program doesn't work without them.
These instructions will reproduce the results presented in chapter 7.2 of our report.

Open and run the file "simulation_final.py" in a python editor of your choice.
The different scenarios of our simulations can be changed in code lines 18, 23, 24.

Set the parameter variante_zeiten = 2 (Line 18)
Set the parameter variante_ampeln = False (Line 22)

Run the simulation for a first time and obey what happens.

Now set the following parameters: 
variante_ampeln = True (Line 22)
light_phase = 40 (Line 23)
car_phase = 25 (Line 24)

Run the simulation for a second time and obey again.

According to our results there shouldn't appear any congestions that don't solve up by itself. The amount of pedestrians waiting should be small. In the second run one can obey that the amount of waiting pedestrians increases steadily.


**Full Test instructions**:

Open the file "simulation_final.py" in a python editor of your choice.
Set the variable maxspeed = True (Line 30).
The different scenarios of our simulations can be changed in code lines 18, 23, 24.

To realize any kind of traffic light chagne the length of a traffic light period in line 23. The red light time for the cars can be changed in line 24. 
In our simulation we used the following parameters: light phase = 40 and varied the values for car_pase = {15, 20, 25}. Feel free to invent your own version of the traffic light.

For each version of the traffic light run the simulation (With all four parameters for variante_zeiten (Line 28) and rename the file "values.csv" with an appropriate title (the file values.csv will be overwritten as soon as the next simulation starts!).


We used gnuplot to create our graphs. You can use the following script to produce our graphs (renamed our file as "simulation1.csv":
Open the terminal and run the following commands in the directory you have stored your files.

#"convert the .csv file to .dat format"
sed "s/,/ /g" simulation1.csv > simulation1.dat

now start gnuplot and run the following commands: 
#global settings
set terminal pngcairo  transparent enhanced size 1200, 800 
set output 'simulation1.png'
set key bmargin left inside noreverse enhanced autotitle
set key left
set style increment default
set samples 800, 800
set title "Simple Plots" 
set title  font ",20" norotate
set title font ",15"
set xrange [ * : * ] noreverse writeback
set x2range [ * : * ] noreverse writeback
set yrange [ * : * ] noreverse writeback
set y2range [ * : * ] noreverse writeback
set zrange [ * : * ] noreverse writeback
set cbrange [ * : * ] noreverse writeback
set xlabel "time passed [s]"
set ylabel "number of agents"

#settings for the individual graphs

set title "Simulation1 Title"
plot 'values1.dat' using 0:6 with impulses title "cars_U" lt rgb "cyan" lw 3, 'values1.dat' using 0:7 with impulses title "cars_B" lt rgb "orange" lw 2, 'values1.dat' using 0:3 with lines title "crosswalk_M" lt rgb "red" lw 2, 'values1.dat' using 0:4 with lines title "crosswalk_U" lt rgb "blue" lw 2, 'values1.dat' using 0:2 with lines title "crosswalk_L" lt rgb "green" lw 2, 'values1.dat' using 0:5 with lines title "crosswalk_B" lt rgb "black" lw 2 
