from lssHelper import *
from lss import *  

# Opens a .lss file and returns the root of the XML tree if valid
def open_lss_file(file_path):
    try:
        tree = ET.parse(file_path)
        file_root = tree.getroot()
        return file_root
    except (FileNotFoundError, ET.ParseError) as e:
        print(f'Error: {e}')

# reads the .lss file starting at the top of the tree,
# stores retrieved values and calculated values in lss() data structure
# data structure defined in lss.py 
def read_lss_file(root, folder_path):
    split_file = lss()
    #split_file.segments = []
        
    # get basic info about the splits
    split_file.output_dir = folder_path
    split_file.game_name = root.findtext('GameName', default='')
    split_file.category_name = root.findtext('CategoryName', default='')
    split_file.layout_path = root.findtext('LayoutPath', default='')
    split_file.timer_offset = root.findtext('Offset', default='')
    split_file.runs_started = count_attempts(root)
    split_file.runs_finished = count_runs_finished(root)
    split_file.total_playtime = get_total_playtime(root.find('AttemptHistory'))
    split_file.finished_run_times = get_finished_runs(root.find('AttemptHistory'))
    
    # variables to track sum of best and total splits time
    sum_of_best = 0.0
    total_runtime = 0.0
    
    # track previous split time to get segment time in PB
    previous_split_time_seconds = 0.0
    
    # <Segment> parsing
    # Organization:
    # <Segment>
    #  <Name>
    #  <Icon>
    #  <SplitTimes>
    #   <SplitTime name="Personal Best">
    #  <BestSegmentTime>
    #  <SegmentHistory>
    #   <Time id="number">
    #    <RealTime>
    file_segments = root.findall('.//Segment')
    for index, segment in enumerate(file_segments, start=1):
        # initialize segment_data() struct to hold segment info
        current_segment = segment_data()
        
        # get <Segment><Name>
        current_segment.name = segment.findtext('Name', default='')
        
        # get <Segment><SplitTimes><SplitTime name="Personal Best"><RealTime>
        current_segment.split_time_pb = get_splittime_pb(segment.find('SplitTimes'), 'Personal Best')
        
        # get <Segment><BestSegmentTime><RealTime>
        current_segment.segment_gold.time = get_real_time(segment.find('BestSegmentTime'))
        
        # gold segment may have been edited or added manually, i.e. not tracked
        manual_gold = False
        
        # calculate segment time in PB - only split times are there by default
        current_segment.segment_pb = None
        # for the first split only, segment time is the same as split time
        if index == 1:
            current_segment.segment_pb = current_segment.split_time_pb
            previous_split_time_seconds = time_to_seconds(current_segment.split_time_pb)
        else:
            pb_segment_seconds = time_to_seconds(current_segment.split_time_pb)
            pb_segment_time_seconds = pb_segment_seconds - previous_split_time_seconds
            current_segment.segment_pb = seconds_to_time(pb_segment_time_seconds)
            previous_split_time_seconds = pb_segment_seconds
        
        # associates time id="number" with RealTime
        segment_history = make_dictionary(segment.find('SegmentHistory'))
        
        # remove times that don't have a RealTime component
        empty_keys = [key for key, value in segment_history.items() if not value]
        for key in empty_keys:
            segment_history.pop(key)
        
        current_segment.segment_history = segment_history
        
        # update sum of best and total runtime
        sum_of_best += time_to_seconds(current_segment.segment_gold.time)
        total_runtime += get_segment_sum(segment_history)
                    
        # find the attempt whose time matches the best segment time & the date/time for that run
        current_segment.segment_gold.id = get_gold_id(segment_history, current_segment.segment_gold.time)
        if current_segment.segment_gold.id == '':
            manual_gold = True
        
        if not manual_gold:
            best_segment_date_time = get_attempt_date(current_segment.segment_gold.id, root)
            if best_segment_date_time != '':
                current_segment.segment_gold.run_date = best_segment_date_time[0]
                current_segment.segment_gold.run_time = best_segment_date_time[1]
            else:
                current_segment.segment_gold.run_date = '?'
                current_segment.segment_gold.run_time = '?'
        else:
            current_segment.segment_gold.run_date = '?'
            current_segment.segment_gold.run_time = '?'
        
        current_segment.possible_time_save = seconds_to_time(time_to_seconds(current_segment.segment_pb) - time_to_seconds(current_segment.segment_gold.time))
        
        # handle the case where the split was skipped in PB
        if time_to_seconds(current_segment.possible_time_save) > time_to_seconds(current_segment.segment_pb):
            current_segment.possible_time_save = seconds_to_time(0)
        
        # find the worst segment info (must be found manually)
        worst_segment_info = get_worst_time(segment_history)
        current_segment.segment_worst.id = worst_segment_info[0]
        current_segment.segment_worst.time = worst_segment_info[1]
        worst_segment_date_time = get_attempt_date(current_segment.segment_worst.id, root)
        if worst_segment_date_time != '':
            current_segment.segment_worst.run_date = worst_segment_date_time[0]
            current_segment.segment_worst.run_time = worst_segment_date_time[1]
        else:
            current_segment.segment_worst.run_date = '?'
            current_segment.segment_worst.run_time = '?'
        
        # calculate segment statistics: average, median, standard deviation
        current_segment.stats.average = get_weighted_average_time(segment_history)
        current_segment.stats.median = get_weighted_median_time(segment_history)
        current_segment.stats.stdev = get_weighted_std_dev(segment_history)
                
        # percentage of times segment was finished : total runs started
        current_segment.stats.finished_rate = get_percent_finished(split_file.runs_started, segment_history)
        
        # percentage that this segment was above average
        current_segment.stats.decent_rate = get_above_average_rate(segment_history)

        split_file.segments.append(current_segment)
    
    
    split_file.sob = seconds_to_time(sum_of_best)
    split_file.total_runtime = seconds_to_time(total_runtime)
    return split_file
    