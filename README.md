# LiveSplit Stats

Reports some information and statistics gleaned from [LiveSplit](http://livesplit.org/) split (.lss) files. Only accounts for RTA (for now).

Once a file is read, you are presented with 4 options:

1. Print all the parsed information to the console
2. Print all the parsed information to the console and a .txt file
3. Display graphs showing various statistics (changes over time, segment times in PB ala splits.io)
4. Export segment times (in seconds) to a .csv
    * Option to include PB segment times, gold segment times, or both

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
    * Average time
    * Median time
    * Standard deviation
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

matplotlib

Installation:

```pip install matplotlib```