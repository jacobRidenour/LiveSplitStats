# Dependencies
import matplotlib.pyplot as plt
import numpy as np

# Imports
from datetime import timedelta, datetime
from lssHelper import get_weighted_average_time, time_to_seconds
import re

# Locals
from lssParser import time_to_seconds, seconds_to_time

def clean_segment_name(segment):
    cleaned_name = re.sub(r'[\\/:"*?<>|]+', '', segment)
    return cleaned_name

# creates graphs for each segment, showing their duration over time
def get_segment_duration_graphs(split_data, folder_path):
    graphs_segment_duration = {}
    # Prepare graphs: segment duration over time
    for current_segment in split_data.segments:
        if not current_segment.segment_history:
            continue
        
        segment_times = [time_to_seconds(value) for value in current_segment.segment_history.values()]
        
        # Calculate the 90th percentile
        #percentile_97 = np.percentile(segment_times, 97)
        #average_time = time_to_seconds(get_weighted_average_time(current_segment.segment_history))
        
        # Filter out values beyond the 90th percentile
        #filtered_segment_times = [time for time in segment_times if time <= percentile_97]
        
        segment_id = [int(key) for key in current_segment.segment_history.keys()][:len(segment_times)]
        
        plt.rcParams['figure.figsize'] = (10.67, 8)  # roughly 1024x768 at 96 dpi
        plt.figure()
        plt.plot(segment_id, segment_times)
        plt.title(current_segment.name)
        plt.xlabel('Run')
        plt.ylabel('Segment Time')
        
        # convert segment times to timedelta objects
        segment_time_as_timedelta = [timedelta(seconds=time) for time in segment_times]
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(timedelta(seconds=x)))) 
        
        # store current plot in the dictionary
        title = f'Segment length over time for {current_segment.name}'
        graphs_segment_duration[title] = plt.gcf()

    
    for index, (key, figure) in enumerate(graphs_segment_duration.items()):
        segment_name = split_data.segments[index].name
        cleaned_segment_name = clean_segment_name(segment_name)
        filename = f'{folder_path}\\graph_segment{index}_{cleaned_segment_name}.png'
        figure.savefig(filename)
        plt.close(figure)
    
    return graphs_segment_duration

# creates 4 graphs:
# * Bar graph: standard deviation for each segment
# * Bar graph: percentage of above average segments
# * Bar graph: possible time save in PB
# * Line graph: Run duration over time
def get_graphs(split_data, segment_names, folder_path):
    graphs = []
    names = ['stdev', 'decent_segs', 'possible_time_save', 'runs_over_time']
    #output all graphs to folder_path
    
    # Prepare graph: standard deviation of all segments
    std_dev_values = []
    segment_times_as_timedelta = []
    
    for _ in range(1):
        for current_segment in split_data.segments:
            if not current_segment.segment_history:
                continue
            
            std_dev_values.append(time_to_seconds(current_segment.stats.stdev))
            segment_times_as_timedelta.append(timedelta(seconds=time_to_seconds(current_segment.stats.stdev)))
        
        # make bar graph
        plt.figure()
        plt.bar(segment_names, std_dev_values, color='blue')
        plt.title('Standard Deviation for Each Segment')
        plt.xlabel('Segment')
        plt.ylabel('Standard Deviation')
        plt.rcParams['figure.figsize'] = (10.67, 8) # roughly 1024x768 at 96 dpi
            
        # convert y-axis to timedelta
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(timedelta(seconds=x))))
        
        plt.xticks(rotation=90)
        plt.tight_layout()
    
        # add to graphs list
        graphs.append(plt.gcf())
    
    # Prepare graph: percentage of above average segments
    above_average_percentages = [float(segment.stats.decent_rate.rstrip('%')) for segment in split_data.segments]
    
    for _ in range(1):
        plt.figure()
        plt.bar(segment_names, above_average_percentages, color='green')
        plt.title('Rate of Above Average Segments')
        plt.xlabel('Segment')
        plt.ylabel('Above Average Rate')
        plt.rcParams['figure.figsize'] = (10.67, 8) # roughly 1024x768 at 96 dpi
        
        for i, percentage in enumerate(above_average_percentages):
            plt.text(i, percentage+1, f'{percentage:.2f}', ha='center')
            
        plt.xticks(rotation=90)
        plt.tight_layout()
        
        graphs.append(plt.gcf())

    # Prepare graph: possible time save in PB
    for _ in range(1):
        possible_time_saves = [segment.possible_time_save for segment in split_data.segments]
        possible_time_saves_seconds = [time_to_seconds(time) for time in possible_time_saves]
        possible_time_saves_timedelta = [timedelta(seconds=time) for time in possible_time_saves_seconds]

        # Create the bar graph
        plt.figure()
        plt.bar(segment_names, possible_time_saves_seconds, color='blue')
        plt.title('Possible Time Save in PB')
        plt.xlabel('Segment')
        plt.ylabel('Possible Time Save')
        plt.rcParams['figure.figsize'] = (10.67, 8) # roughly 1024x768 at 96 dpi

        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(timedelta(seconds=x))))

        plt.xticks(rotation=90)
        plt.tight_layout()

        graphs.append(plt.gcf())
        
    # Prepare graph: run duration over time
    for _ in range(1):
        run_ids = [int(key) for key in split_data.finished_run_times.keys()]
        run_times = [time_to_seconds(value) for value in split_data.finished_run_times.values()]
        
        #real_time_seconds = [time_to_seconds(rt) for rt in split_data.finished_run_times.values()]
        #real_time_timedeltas = [timedelta(seconds=seconds) for seconds in real_time_seconds]
        #run_ids = list(split_data.finished_run_times.keys())
        
        # Create the graph
        plt.figure()
        plt.plot(run_ids, run_times, marker='o')
        plt.title('Run Duration Over Time')
        plt.ylabel('Real Time')
        plt.rcParams['figure.figsize'] = (10.67, 8) # roughly 1024x768 at 96 dpi
        
        run_time_as_timedelta = [timedelta(seconds=time) for time in run_times]
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(timedelta(seconds=x)))) 
        
        #plt.xticks(rotation=90)
        plt.tight_layout()
        
        graphs.append(plt.gcf())
    
    index = 0
    for graph in graphs:
        filename = f'{folder_path}\\graph_{names[index]}.png'
        graph.savefig(filename)
        index += 1
        plt.close(graph)
       
    return graphs