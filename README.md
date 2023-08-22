# LiveSplit Stats

Reports some information and statistics gleaned from [LiveSplit](http://livesplit.org/) split (.lss) files. Only accounts for RTA (for now).

Much of this information is already parsed or calculated by LiveSplit, but this also offers:
* A visualization of run duration over time (much like [splits.io](https://splits.io))
* A visualization of segment duration over time
* A visualization of time save in your PB
* A visualization of standard deviation for each segment

Once a file is read, the script will:

1. Create a folder in the parent directory of the script to store the results.
2. Write all the parsed information to a .txt file
3. Output graphs showing various statistics (std deviation, decent segment rate, segment duration over time)
4. Export PB segment times, gold times, split times to a CSV, and history for each segment to CSVs

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
    * Standard deviation (weighted with a focus on most recent 50% of times)
    * Percentage of runs that completed that segment

Other information
* Sum of Best segments
* Total runtime (sum of all completed segments)
* Total playtime (includes runs that reset before first segment was finished)

Graphs
* Line graph: segment duration over time for each segment
* Bar graph: standard deviation for each segment
* Bar graph: percentage of decent segments (within 3% of gold)
* Bar graph: possible time save in PB
* Line graph: Run duration over time

# Dependencies

matplotlib, numpy

Installation:

```pip install matplotlib numpy```

# Usage

Run the script liveSplitStats.py.

Enter the path to your .lss file. The script will do the rest.

# Keep in Mind

* Likely to be inaccurate if you've rearranged splits
* Results are weighted but may be slightly less useful if e.g. you converted your old any% splits to 100% splits or changed a route without changing the splits
