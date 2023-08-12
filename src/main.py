# Imports
import os

# Locals
from lssParser import *
from lssGraphs import *

# TODO:
# fix best segment and worst segment parsing
# add .txt output
# graphs
# add .csv output with options

# prompts the user for a .lss file, then directs them on what to do with the parsed info (choose_option())
def main():
    while True:
        try:
            lss_file = input('Enter the path to a valid .lss file (or "q" to quit): ')
            # check if user wants to quit
            if lss_file.lower() == 'q' or lss_file.lower() == 'quit':
                break
            # make sure it's a .lss file
            if not lss_file.lower().endswith('.lss'):
                raise ValueError('Invalid file format. File must be of type .lss')
            else:
                # check first two lines 
                with open(lss_file, 'r') as file:
                    header = [file.readline() for _ in range(2)]
                    if not header[0].startswith('ï»¿<?xml version="1.0" encoding="UTF-8"?>'):
                        raise ValueError('Invalid XML version header')
                    if not header[1].strip().startswith('<Run version='):
                        raise ValueError('Missing <Run> tag.')
                result = open_lss_file(lss_file)
                if result:
                    split_data = read_lss_file(result)
                    
                    # call new options function, let user choose what they want to do with the data
                    choose_option(split_data)
                else:
                    print('Failed to open', lss_file)
                    
        except (FileNotFoundError, ET.ParseError, ValueError) as e:
            print(f'Error: {e}')

# prompts the user on what to do with parsed .lss data
def choose_option(split_data):
    
    print_menu = lambda: print('\nChoose from 1 of the following options:\n'
                            '1 - print statistics and data parsed from the .lss file\n'
                            '2 - print statistics and data parsed from the .lss file, output results to text file\n'
                            '3 - show graphs based on statistics and data parsed from the .lss file\n'
                            '4 - output PB split times to a .csv file\n'
                            '[Q] Return to previous Menu [O] Show options\n')
    print_menu()
    while True:
        try:
            choice = input('Enter your choice: ')
            if choice.lower() == 'q' or choice.lower() == 'quit':
                break
            if choice.lower() == 'o' or choice.lower() == 'options':
                print_menu()
            elif choice == '1':
                print_parsed_info(split_data, False)
            elif choice == '2':
                print_parsed_info(split_data, True)
            elif choice == '3':
                show_graphs(split_data)
            elif choice == '4':
                print()
            else:
                 raise ValueError
        except ValueError as e:
            print(f'Error: choice must be in range [1, 4], enter "q" to choose another file.')
    
# prints data collected and calculated from the .lss file. if write_to_file flag is set, outputs to text file too.
def print_parsed_info(split_data, write_to_file):
    if write_to_file:
        while True:
            file_path = input('Enter the name of the output file (including extension): ')
            
            # if user just entered a file name, place output in script directory
            if not os.path.isabs(file_path):
                file_path = os.path.join(os.getcwd(), file_path)
                
            # make sure path is valid
            if os.path.exists(os.path.dirname(file_path)):
                print('Output written to', file_path)
                break
            else:
                print('Invalid path. Please provide a valid path or a file name.')

        with open(file_path, 'w') as file:
            file.write(f'Game Name:      {split_data.game_name}\n')
            file.write(f'Category Name:  {split_data.category_name}\n')
            file.write(f'Layout Path:    {split_data.layout_path}\n')
            file.write(f'Timer Offset:   {split_data.timer_offset}\n')
            file.write(f'Runs Started:   {split_data.runs_started}\n')
            file.write(f'Runs Finished:  {split_data.runs_finished}\n')
            file.write(f'Total Runtime:  {split_data.total_runtime}\n')
            file.write(f'Total Playtime: {split_data.total_playtime}\n')
            file.write('\nSegments\n')
            
            for index, current_segment in enumerate(split_data.segments, start=1):
                file.write(f'{index}. {current_segment.name}\n')
                file.write(f'    - Split Time (PB):    {current_segment.split_time_pb}\n')
                file.write(f'    - Segment Time (PB):  {current_segment.segment_pb}\n')
                file.write(f'    - Best Time:          {current_segment.segment_gold.time}, on attempt {current_segment.segment_gold.id}, which started on {current_segment.segment_gold.run_date} at {current_segment.segment_gold.run_time}.\n')
                file.write(f'    - Worst Time:         {current_segment.segment_worst.time}, on attempt {current_segment.segment_worst.id}, which started on {current_segment.segment_worst.run_date} at {current_segment.segment_worst.run_time}.\n')
                file.write(f'    - Average Time:       {current_segment.stats.average}\n')
                file.write(f'    - Median Time:        {current_segment.stats.median}\n')
                file.write(f'    - Std Deviation:      {current_segment.stats.stdev}\n')
                file.write(f'    - Possible Time Save: {current_segment.possible_time_save}\n')
                file.write(f'    - This segment is completed {current_segment.stats.finished_rate} of the time.\n')
                file.write(f'    - This segment is above average {current_segment.stats.decent_rate} of the time.\n\n')
        
    print(f'Game Name:      {split_data.game_name}')
    print(f'Category Name:  {split_data.category_name}')
    print(f'Layout Path:    {split_data.layout_path}')
    print(f'Timer Offset:   {split_data.timer_offset}')
    print(f'Runs Started:   {split_data.runs_started}')
    print(f'Runs Finished:  {split_data.runs_finished}')
    print(f'Total Runtime:  {split_data.total_runtime}')
    print(f'Total Playtime: {split_data.total_playtime}')
    print('\nSegments')
    
    for index, current_segment in enumerate(split_data.segments, start=1):
        print(f'{index}. {current_segment.name}')
        print(f'    - Split Time (PB):    {current_segment.split_time_pb}')
        print(f'    - Segment Time (PB):  {current_segment.segment_pb}')
        print(f'    - Best Time:          {current_segment.segment_gold.time}, on attempt {current_segment.segment_gold.id}, which started on {current_segment.segment_gold.run_date} at {current_segment.segment_gold.run_time}.')
        print(f'    - Worst Time:         {current_segment.segment_worst.time}, on attempt {current_segment.segment_worst.id}, which started on {current_segment.segment_worst.run_date} at {current_segment.segment_worst.run_time}.')
        print(f'    - Average Time:       {current_segment.stats.average}')
        print(f'    - Median Time:        {current_segment.stats.median}')
        print(f'    - Std Deviation:      {current_segment.stats.stdev}')
        print(f'    - Possible Time Save: {current_segment.possible_time_save}')
        print(f'    - This segment is completed {current_segment.stats.finished_rate} of the time.')
        print(f'    - This segment is above average {current_segment.stats.decent_rate} of the time.\n')

# prompts the user to show a number of graphs:
# * Line graph: segment duration over time for each segment
# * Bar graph: standard deviation for each segment
# * Bar graph: percentage of above average segments
# * Bar graph: possible time save in PB
# * Line graph: Run duration over time
def show_graphs(split_data):
    segment_names = []
    graphs = []
    
    # get list of all segment names
    for current_segment in split_data.segments:
        segment_names.append(current_segment.name)
    
    # dictionary to store all of the segment duration graphs
    graphs_segment_duration = {}
    
    # list to store the other graphs
    graphs = get_graphs(split_data, segment_names)
    
    # Get choice from user    
    print_menu = lambda: print('\nStatistical Plot Choices\n'
                                '1 - Line graph - segment duration over time (for a given segment)\n'
                                '2 - Bar graph - standard deviation of all segments\n'
                                '3 - Bar graph - percentage of above average segments\n'
                                '4 - Bar graph - possible time save in PB\n'
                                '5 - Line graph - run duration over time\n'
                                '[Q] Return to previous Menu [O] Show options\n')
    
    print_menu()
    while True:
        try:
            choice = input('Enter your choice: ')
            if choice.lower() == 'q' or choice.lower() == 'quit':
                for graph in graphs:
                    plt.close(graph)
                break
            elif choice.lower() == 'o' or choice.lower() == 'options':
                print_menu()
            # Segment duration over time
            elif choice == '1':
                graphs_segment_duration = get_segment_duration_graphs(split_data)
                keys_list = list(graphs_segment_duration.keys())
                for index in range(len(segment_names)):
                    print(f'{index+1}. {segment_names[index]}')
                while True:
                    try:
                        new_choice = input('Enter the number for the segment you would like to see statistics for (or "q" to go back): ')
                        if new_choice.lower() == 'q' or new_choice.lower() == 'quit':
                            break
                        elif int(new_choice) < 1 or int(new_choice) > len(keys_list):
                            raise IndexError
                        else:
                            graphs_segment_duration[keys_list[int(new_choice)-1]].show()
                    except IndexError as e:
                        print(f'Error: choice must be in range [1, {len(segment_names)}]')
                for key in keys_list:
                    graphs_segment_duration[key].close()
            # Standard deviation for all segments
            elif choice == '2':
                graphs[0].show()
                graphs = get_graphs(split_data, segment_names)
            # Percent of the time that segments are above average
            elif choice == '3':
                graphs[1].show()
                graphs = get_graphs(split_data, segment_names)
            # Possible time save in PB
            elif choice == '4':
                graphs[2].show()
                graphs = get_graphs(split_data, segment_names)
            # Run duration over time
            elif choice == '5':
                graphs[3].show()
                graphs = get_graphs(split_data, segment_names)
            else:
                raise ValueError
        except ValueError as e:
            print(f'Error: choice must be in range [1, 5].')

if __name__ == '__main__':
    main()
