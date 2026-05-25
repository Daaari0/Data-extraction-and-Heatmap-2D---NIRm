# -*- coding: utf-8 -*-
"""
First version on April 2023
Created on Mon May 25 13:39:16 2026

@author: dario
"""

# ==============================================================================
# FILENAME STRUCTURE REQUIREMENT:
# For this script to work properly, your raw .xls microscope files must follow 
# this exact naming convention using underscores:
#
#   [X-Value]_[Y-Value]_[GroupLabel].xls
#
# Examples: 
#   1.5_2.0_Control.xls
#   0.0_5.5_Treated.xls
# ==============================================================================

import xlrd, datetime
from statistics import mean, stdev
from tkinter import filedialog
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

filename, x, y, labels, date = [], [], [], [], []
average, deviation, delta_time, filename_cut, label = [], [], [], [], []
j = 0

file_name_saved = 'output'

global DATA

# allows to create a matrix of data. 
def init_list_of_objects(size): 
    list_of_objects = list()
    for i in range(0, size):
        list_of_objects.append(list()) 
    return list_of_objects

def getData(filename):
    workbook = xlrd.open_workbook(adress + filename) 
    worksheet = workbook.sheet_by_index(0) 
    DATA['date'].append(worksheet.cell(0, 1).value)  
    
    # Dynamically loops from row 10 to the absolute end of the available data rows
    for i in range(10, worksheet.nrows):
        DATA['signal'][j].append(float(worksheet.cell(i, 2).value))

# given an array with data, it does the maths for average and deviation
def Statistics(data): 
    average.append(mean(data))
    deviation.append(stdev(data))

def delta_time_f(date):
    time_secs = []
    for i in range(len(date)):         
        whole_date = date[i].split(' ') 
        time = whole_date[1] 
        h, m, s = time.split(':') 
        time_secs.append(int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())) 
        delta_time.append(time_secs[i] - time_secs[0]) 

def SaveFinalData(average, deviation, filename, date, delta_time, x, y, folder, save_dir):       
    header = 'date\tdelta_time\tfilename\tx\ty\taverage\tdeviation' 
    units = ' \ts\t \t \tmV\tmV'
    
    file = open(save_dir + '/' + folder + ' ' + file_name_saved + ".txt", "w") 
    file.write('\n' + header + '\n' + units + '\n')
    file.close() 
    
    file = open(save_dir + '/' + folder + ' ' + file_name_saved + ".txt", "a") 
    for i in range(len(average)):
        file.write(str(date[i]) + '\t' + str(delta_time[i]) + '\t' + str(filename[i]) + '\t' + str(x[i]) + '\t' + str(y[i]) + '\t' + str(average[i]) + '\t' + str(deviation[i]) + '\n') 
    file.close()
    print('\n>Ouput file saved. \t Move it or it may be overwritten!')

def Choice(x, y, average, signal, filename, label, folder, save_dir):
    choice = input('\n\t Wanna save the raw data? Say y/n\t')
    if choice == 'y' or choice == 'Y':
        SaveRawData(x, y, average, signal, filename, label, folder, save_dir)
    elif choice == 'n' or choice == 'N':
        print('\nChosen to NOT save the raw data.\n\t\tExiting...')
    else:
        print('\nTyped something else.\n\tSaving anyway the raw data...')
        SaveRawData(x, y, average, signal, filename, label, folder, save_dir)

def SaveRawData(x, y, average, signal, filename, label, folder, save_dir):       
    header = 'filename\tx\ty\taverage\tSignal array -->' 
    units = ' \tmm\tmm\tmV\tmV' 

    file = open(save_dir + '/' + folder + ' ' + 'RAW_DATA' + ' ' + label + ".txt", "w") 
    file.write('\n' + header + '\n' + units + '\n')
    file.close() 
    
    file = open(save_dir + '/' + folder + ' ' + 'RAW_DATA' + ' ' + label + ".txt", "a") 
    for i in range(len(average)):
        file.write(str(filename[i]) + '\t' + str(x[i]) + '\t' + str(y[i]) + '\t' + str(average[i]) + '\t' + ('  '.join(signal[i])) + '\n')
    file.close()
    print('\nOuput file saved. \t Move it or it may be overwriteen!')


#---------------------------- main -----------------------------
input('\n\nPress ENTER to select the folder with the data')
folder = filedialog.askdirectory(initialdir="/")  
print('\n>Folder selected:\n' + folder)
adress = folder + '\\' 

files = glob(adress + '*.xls') 

signal = init_list_of_objects(len(files)) 
DATA = dict(filename=filename, x=x, y=y, signal=signal, labels=labels, date=date) 

print('\n>Reading following files:')
for i in range(len(files)):  
    DATA['filename'].append(files[i].split(folder + '\\')[1])
    DATA['x'].append(filename[i].split('_')[0]) 
    DATA['y'].append(filename[i].split('_')[1]) 
    
    label = filename[i].split('_')[2].split('.')[0]
    if label not in DATA['labels']:
        DATA['labels'].append(label) 
        
    print(filename[i])
    getData(DATA['filename'][i]) 
    Statistics(DATA['signal'][i])
    j += 1 
    
filename_cut = DATA['x'].copy()
delta_time_f(date)
folder_name = folder.split('/')

input('\nPress ENTER to select the folder where you want to SAVE the outputs')
save_destination = filedialog.askdirectory(initialdir=folder)

SaveFinalData(average, deviation, DATA['filename'], DATA['date'], delta_time, DATA['x'], DATA['y'], folder_name[-1], save_destination) 

# --- PLOT PART - and saving RAW DATA ---
count = 0
for i in range(len(filename_cut)):
    if filename_cut[i].isalpha():   
        count = count + 1   

for label in DATA['labels']:
    print('\n\tPlotting graph for label \"' + label + '\" data set...')
    input('\n\t\tPress ENTER')
    x, y, z = [], [], []
    num = ''
    values_str = init_list_of_objects(len(files))
    filename2 = []
    k = 0

    for i in range(len(filename_cut) - count):
        if label in filename[i]:
            filename2.append(filename[i])
            x.append(float(filename_cut[i]))   
            z.append(float(average[i]))
            y.append(float(DATA['y'][i]))
            for j in range(len(DATA['signal'][i])):
                num = DATA['signal'][i][j]
                values_str[k].append(str(num))
            k += 1

    # --- HEATMAP GRID CONVERSION ---
    x_unique = np.sort(np.unique(x))
    y_unique = np.sort(np.unique(y))

    signal_grid = np.full((len(y_unique), len(x_unique)), np.nan)
    log_signal_grid = np.full_like(signal_grid, np.nan)

    for xi, yi, zi in zip(x, y, z):
        x_idx = np.where(x_unique == xi)[0][0]
        y_idx = np.where(y_unique == yi)[0][0]
        signal_grid[y_idx, x_idx] = zi
        if zi > 0:
            log_signal_grid[y_idx, x_idx] = np.log10(zi)

    extent_bounds = [x_unique.min(), x_unique.max(), y_unique.min(), y_unique.max()]

    # Original Signal Heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(signal_grid, extent=extent_bounds, origin='lower', aspect='auto', cmap='viridis')
    plt.colorbar(label='Signal Intensity (mV)')
    plt.ylabel('y (mm)')
    plt.xlabel('x (mm)')
    plt.title('Heatmap\nLabel: ' + label)
    plt.tight_layout()
    plt.show()

    # Log10 Signal Heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(log_signal_grid, extent=extent_bounds, origin='lower', aspect='auto', cmap='viridis')
    plt.colorbar(label='log10(Signal)')
    plt.ylabel('y (mm)')
    plt.xlabel('x (mm)')
    plt.title('Log10 Heatmap\nLabel: ' + label)
    plt.tight_layout()
    plt.show()

    Choice(x, y, z, values_str, filename2, label, folder_name[-1], save_destination)