# Dependencies
import matplotlib.pyplot as plt

# Imports
from datetime import timedelta, datetime

# Locals
from lssParser import time_to_seconds, seconds_to_time

# creates graphs for each segment, showing their duration over time
def get_segment_duration_graphs(split_data):
    graphs_segment_duration = {}
    # Prepare graphs: segment duration over time
    for current_segment in split_data.segments:
        if not current_segment.segment_history:
            continue
        
        segment_id = [int(key) for key in current_segment.segment_history.keys()]
        segment_time = [time_to_seconds(value) for value in current_segment.segment_history.values()]
        
        plt.figure()
        plt.plot(segment_id, segment_time)
        plt.title(current_segment.name)
        plt.xlabel('Run')
        plt.ylabel('Segment Time')
        
        # convert segment times to timedelta objects
        segment_time_as_timedelta = [timedelta(seconds=time) for time in segment_time]
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(timedelta(seconds=x)))) 
        
        # store current plot in the dictionary
        title = f'Segment length over time for {current_segment.name}'
        graphs_segment_duration[title] = plt.gcf()
        
    return graphs_segment_duration

# creates 4 graphs:
# * Bar graph: standard deviation for each segment
# * Bar graph: percentage of above average segments
# * Bar graph: possible time save in PB
# * Line graph: Run duration over time
def get_graphs(split_data, segment_names):
    graphs = []
    
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
            
        # convert y-axis to timedelta
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(timedelta(seconds=x))))
        
        plt.xticks(rotation=45)
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
        
        for i, percentage in enumerate(above_average_percentages):
            plt.text(i, percentage+1, f'{percentage:.2f}', ha='center')
            
        plt.xticks(rotation=45)
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

        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(timedelta(seconds=x))))

        plt.xticks(rotation=45)
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
        
        run_time_as_timedelta = [timedelta(seconds=time) for time in run_times]
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(timedelta(seconds=x)))) 
        
        #plt.xticks(rotation=45)
        plt.tight_layout()
        
        graphs.append(plt.gcf())
        
    return graphs