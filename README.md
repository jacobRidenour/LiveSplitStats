# LiveSplit Stats

Reports some information and statistics gleaned from [LiveSplit](http://livesplit.org/) split (.lss) files. Only accounts for RTA (for now).

Once a file is read, the script will:

1. Create a folder in the parent directory of the script to store the results.
2. Write all the parsed information to a .txt file
3. Output graphs showing various statistics (std deviation, above average rate, segment duration over time)
4. (TODO) Export segment times (in seconds) to a .csv

Parsed information
* Game Name
* Category Name
* Layout Path
* Timer Offset
* Runs Started
* Runs Finished
* Segment information (see below)

Segment information
* Name
* Split time in PB
* Segment time in PB
* Best time (gold), which attempt, on what date/time
* Worst time, which attempt, on what date/time
* Calculations:
    * Average time (weighted)
    * Median time (weighted)
    * Standard deviation (weighted)
    * Percentage of runs that completed that segment

Other information
* Sum of Best segments
* Total runtime (sum of all completed segments)
* Total playtime (includes runs that reset before first segment was finished)

Graphs
* Line graph: segment duration over time for each segment
* Bar graph: standard deviation for each segment
* Bar graph: percentage of above average segments
* Bar graph: possible time save in PB
* Line graph: Run duration over time

# Dependencies

matplotlib, numpy

Installation:

```pip install matplotlib numpy```

# Usage

Enter the path to your .lss file. The script will do the rest.

# Known Issues

Does not properly account for times when splits are skipped. Currently for segment graphs will filter segments that are >= 1.75x the average time for that segment (not good for short splits)
Above average calculation probably needs adjustment.