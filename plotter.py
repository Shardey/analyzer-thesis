import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import json, os
import numpy as np

def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 2),  
                    textcoords="offset points",
                    ha='center', va='bottom', rotation=0)
        
#####
#
# overview_plot(dir,data,round,metric)
#
# dir    : Directory of the main result data repository, used for the savefile name
# data   : The array of data to be plotted
# round  : Name of the round, used for labels.
# metric : the metric being plotted, used for labels
#
# Plots overview of the metric from data [maxes, means, medians, mins]
       
 
def overview_plot(dir,data,round,metric):    
    labels = []
    for count,line in enumerate(data[0]):
        labels.append(str(count) + ' fails')
    x = np.arange(len(labels))  # the label locations
    width = 0.20  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width*3/2, data[0], width, label='Max')
    rects2 = ax.bar(x - width/2, data[1], width, label='Mean')
    rects3 = ax.bar(x + width/2, data[2], width, label='Median')
    rects4 = ax.bar(x + width*3/2, data[3], width, label='Min')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(metric)
    ax.set_xlabel('Amount of failed unit tests')
    ax.set_title('Overview of ' + metric + ' in the round ' + round)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    autolabel(rects1,ax)
    autolabel(rects2,ax)
    autolabel(rects3,ax)
    autolabel(rects4,ax)

    fig.tight_layout()
    savefile = dir + '/plots/' + round + '/overall_' + round + '_' + metric
    plt.savefig(savefile)
    plt.close()

#####
# overall_metric_data(dir,metric)
#
# dir: the directory with the data
# metric: name of the metric being collected
#
# Reads multimetric results from a directory and compiles overall metrics data
# This result is used to plot out an overview of one round, consisting of the results for each individual amount of errors in
#
# If more than 10 unit tests, files may not be in numerical order and ALL metrics will be screwed. TODO!

def overall_metric_data(dir,metric):
    data,mins,maxes,means,medians = [],[],[],[],[]
    for filename in os.listdir(dir):
        with open(os.path.join(dir, filename), 'r') as f: # open all result files and add their contents to data
            data.append(json.load(f))
            
    for line in data: # combine mins,maxes,means,medians data from all result files
        maxes.append(line['stats']['max'][metric])
        means.append(line['stats']['mean'][metric])
        medians.append(line['stats']['median'][metric])
        mins.append(line['stats']['min'][metric])

    return np.round([maxes,means,medians,mins],2) #round to 2 decimals

#####
# distribution(metric,fie)
#
# metric: The metric the distribution array is to be created of
# file  : Filename of the result group
#
# Creates a sorted array of the distribution of metric values over one file (the metric results 
# of one round of submissions with X errors on one task)
#
#

def distribution(metric,file):
    with open(file, 'r') as f:
        data = json.load(f)       
        distribution = list()
        for x in data['files']: # Individual submission data is stored in data['files']
            distribution.append(data['files'][x][metric])
    distribution.sort()
    return distribution

######
# histo_plot(dir,buckets,metric,round)
#
# dir       : Directory containing the json data files (*datadump*-analysis/metrics/*round*/results/)
# buckets   : How many buckets the histogram spreads the data in
# metric    : Which metric is being drawn
# round     : Name of the exercise round
#
# Plots one big histogram, side by side for all fail groups for one round

def histo_plot(dir,buckets,metric,round):
    fig,ax = plt.subplots()

    number_of_files = len(os.listdir(dir))
    data = [[] for i in range(number_of_files)]
    labels = [[] for i in range(number_of_files)]

    ax.set_title('Histogram distribution plot with ' + str(buckets) + ' buckets. \nRound: ' + round + ' Metric: ' + metric)
    ax.set_ylabel('Amount of submissions')
    ax.set_xlabel(metric)
   
    for i,file in enumerate(os.listdir(dir)):
        filename = dir + '/'+ file # Name of one result file
        data[i] = distribution(metric, filename)
        labels[i] = str(i) + ' (subs: ' + str(len(data[i])) + ')'
    
    ax.hist(data,buckets,label=labels,alpha = 0.5,histtype='bar')

    ax.legend(loc='upper right',title='Unit test fails')
 
    savefile = dir + '../../../plots/' + round + '/Overall_Histo_' + str(buckets) + '_' + round + '_' + metric
    plt.savefig(savefile)
    plt.close()

    
    

######
# abc_data(file)
#
# file: The filename for which ABC data is collected
#
# Collects ABC metric data from one file. Calculates the vector explosion field with the center point
# being the endpoint of the median vector. Returns a triple list.

def abc_data(file):
    abc_data = [[] for i in range(3)] # three lists

    with open(file, 'r') as f:
        data = json.load(f)       
        avg_a = data['stats']['median']['ABC_Assignments']
        avg_b = data['stats']['median']['ABC_Branches']
        avg_c = data['stats']['median']['ABC_Conditionals']
        for x in data['files']: # Individual submission data is stored in data['files']
            temp_a = data['files'][x]['ABC_Assignments'] - avg_a
            temp_b = data['files'][x]['ABC_Branches'] - avg_b
            temp_c = data['files'][x]['ABC_Conditionals'] - avg_c
            
            abc_data[0].append(temp_a)
            abc_data[1].append(temp_b)
            abc_data[2].append(temp_c)
    
    return abc_data

######
# abc_plot(dir,round)
#
# dir   : Directory where the .json data files are (*-analysis/metrics/*round*/results)
# round : Name of the round
#
# Plot the ABC data in a vector explosion field with the origin being the median ABC vector
# Takes in one round of exercises, containing multiple files with one file each for X amount of unit test failures

def abc_plot(dir,round):
    data = []
    medians = []
    start = []
    tempdata = []

    for file in os.listdir(dir):
        filename = dir + '/' + file
        #tempdata = abc_data(filename)
        
        abc_data    = [[] for i in range(3)] # three lists
        median_data = [[] for i in range(3)]

        with open(filename, 'r') as f:
            filedata = json.load(f)       
            avg_a = filedata['stats']['median']['ABC_Assignments']
            avg_b = filedata['stats']['median']['ABC_Branches']
            avg_c = filedata['stats']['median']['ABC_Conditionals']
            for x in filedata['files']: # Individual submission data is stored in data['files']
                temp_a = filedata['files'][x]['ABC_Assignments'] - avg_a
                temp_b = filedata['files'][x]['ABC_Branches'] - avg_b
                temp_c = filedata['files'][x]['ABC_Conditionals'] - avg_c
            
                
                abc_data[0].append(temp_a)
                abc_data[1].append(temp_b)
                abc_data[2].append(temp_c)

            median_data[0].append(avg_a)
            median_data[1].append(avg_b)
            median_data[2].append(avg_c)

        medians.append(median_data)
        data.append(abc_data)

    # data now contains one list member for each file of unit test fails, each with a triple list with A, B and C values
    
    for i,line in enumerate(data):    
        X = [0] * len(line[0])
        Y = [0] * len(line[0])
        Z = [0] * len(line[0]) #The starting points of the vectors are always [0,0,0]
        U = line[0]
        V = line[1]
        W = line[2]
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.quiver(X, Y, Z, U, V, W,arrow_length_ratio=0.1)
        ax.set_xlim([min(U)-1, max(U)+1])
        ax.set_ylim([min(V)-1, max(V)+1])
        ax.set_zlim([min(W)-1, max(W)+1])

        ax.set_xlabel('Assignment')
        ax.set_ylabel('Branch')
        ax.set_zlabel('Condition')

        ax.set_title('Metric: ABC :: Round: ' + round + ' :: Fails: ' + str(i) + ' :: Submissions: ' + str(len(line[0])) + '\nStarting point[0,0,0] = median vector: ' + str(medians[i]))
        savefile = dir + '../../../plots/' + round + '/ABC_' + round + '_' + str(i)
        plt.savefig(savefile)
        plt.close()
    

#####
# plotter(dir)
#
# dir: base directory of the whole data result package (/directory-analysis/)
#
# Plots everything in the whole Analyzer project. If you need more/different plots, add them here
# 

def plotter(dir):
    plt.rcParams.update({'figure.max_open_warning': 0}) # Stop pyplot throwing warnings about too many open plots

    print('Drawing plots for round: ')
    for round in os.listdir(dir + '/metrics'): # Rounds of exercises in the metric result directory
        print('... ' + round)
        Path(dir + '/plots/' + round ).mkdir(parents=True, exist_ok=True) # Create the plots - directory

        dirname = dir + '/metrics/' + round + '/results/'

        abc_plot(dirname, round)
        
            
        histo_plot(dirname,10,'cyclomatic_complexity',round)
        histo_plot(dirname,10,'halstead_bugprop',round)
        histo_plot(dirname,10,'halstead_difficulty',round)
        histo_plot(dirname,10,'halstead_effort',round)
        histo_plot(dirname,10,'halstead_timerequired',round)
        histo_plot(dirname,10,'halstead_volume',round)
        
        
        data = overall_metric_data((dir + '/metrics/' + round + '/results'), 'cyclomatic_complexity')  
        overview_plot(dir,data,round,'Cyclomatic Complexity')
        data = overall_metric_data((dir + '/metrics/' + round + '/results'), 'halstead_bugprop')                        
        overview_plot(dir,data,round,'Halstead Bugs')
        data = overall_metric_data((dir + '/metrics/' + round + '/results'), 'halstead_difficulty')  
        overview_plot(dir,data,round,'Halstead Difficulty')
        data = overall_metric_data((dir + '/metrics/' + round + '/results'), 'halstead_effort')
        overview_plot(dir,data,round,'Halstead Effort')
        data = overall_metric_data((dir + '/metrics/' + round + '/results'), 'halstead_timerequired')
        overview_plot(dir,data,round,'Halstead Time Required')
        data = overall_metric_data((dir + '/metrics/' + round + '/results'), 'halstead_volume')
        overview_plot(dir,data,round,'Halstead Volume')
        data = overall_metric_data((dir + '/metrics/' + round + '/results'), 'loc')               
        overview_plot(dir,data,round,'Lines of Code')
            
###
# main()
#
# Used for testing purposes during development. Analyzer calls plotter(dir) instead.
#

def main():

    abc_plot('datadump-analysis/metrics/mauno-plot/results','mauno-plot')
#    histo_plot('datadump-analysis/metrics/mauno-plot/results/',10,'cyclomatic_complexity','mauno-plot')
    
#    plotter('datadump-analysis')
    

#    dist = distribution('cyclomatic_complexity','mauno-plot/errors0result.txt')
#    histogram_plot(dist,10,'cyclomatic_complexity','mauno-plot')

#    dist = distribution('halstead_bugprop','errors0result.txt')
#    histogram_plot(dist,10,'halstead_bugprop','rainfall')

    
if __name__ == "__main__":
    main()

