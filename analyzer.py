import os, glob, sys, csv
from os import listdir
import grouper, plotter
import multimetric.multimetric as mm

            
#####
# main()
#
# The main control sequence for the whole Analyzer project
# Needs exactly one command line argument, the name of the directory where all the data is located.
# Will write out data in the folder <directory>-analysis/. Overwrites if it existed.

def main():
    if len(sys.argv) != 2:
        print('Wrong number of arguments to Analyzer')
        print('Usage: Analyzer <directory>')
        print('<directory> is the path to the data directory')
        print('All output will be saved in the directory <directory>-analysis>')
        exit()

    dir = sys.argv[1]
    
    if not os.path.isdir(dir):
        print('Error:: Directory does not exist: \"' + dir + '\"')
        exit()

    print('Starting Analyzer on the directory: ' + dir)
    
    directory_contents = os.listdir(dir) # All subdirectories in target base directory, each contains a round of exercise submissions
    round_list = []

    for item in directory_contents: # Each subdirectory contains one round of submissions
        if os.path.isdir(dir + '/' + item):
            round_list.append(item)

    grouper.create_dirs(dir,round_list) # Build the directory structure for writing the result files
    
    print('Analyzing round: ')
    for i,round in enumerate(round_list): # Run the sorter for every round of exercises
        print('... ' + round)
        sorted_rounds = grouper.grouper(dir,round,i) # grouper.grouper also prints out statistical data about submission numbers to stdout TODO: to an excel file
        grouper.sort_to_files(dir,sorted_rounds,round)
        
        # Run multimetric for each result file 
        directory = dir + '-analysis/metrics/' + round + '/filelists/'
        metric_input_files = os.listdir(directory)
        for file in metric_input_files:
            pathed_filename = directory + file
            mm.mm_interface(pathed_filename)

    # Plot everything!
    plotter.plotter(dir + '-analysis')
    print('Analyzer done. Results are found in the directory ' + dir + '-analysis/')
    
if __name__ == "__main__":
    main()