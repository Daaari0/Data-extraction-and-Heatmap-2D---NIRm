# 2D Data Extraction & Heatmap Generation

It extracts, analyzes, and plots spatial data acquired from the oscilloscope Promax OD-606. The script reads raw data from multiple .xls files, calculates descriptive statistics, normalizes acquisition time deltas, maps data onto an ordered 2D spatial coordinate system, and generates both linear-scale and Log10-scale signal intensity heatmaps.
---
## Prerequisites & Dependencies
The script relies on a few data parsing and scientific visualization libraries. Ensure you have them installed prior to running the analyzer:
```bash
pip install xlrd numpy matplotlib
```
Note: The xlrd library is explicitly used to read legacy Excel configurations (`.xls`). Standard Microsoft formats (`.xlsx`) cannot be treated by this script.
---

## File Naming Requirement (CRITICAL)
For the automated parser to correctly extract spatial map positions, individual raw data files must follow this exact underscore-separated naming convention:

`[X-Coordinate]_[Y-Coordinate]_[GroupLabel].xls`

> **Examples:**
•	1.5_2.0_Control.xls (X = 1.5, Y = 2.0, Group/Label = Control)
•	0.0_5.5_Treated.xls (X = 0.0, Y = 5.5, Group/Label = Treated)
---
## Input Data Format
Inside each .xls microscope workbook, the data structure must align with the following index expectations:
1.	Acquisition Timestamp: Located at cell B1 (row index 0, column index 1).
2.	Signal Array Data: Collected down column C (column index 2), beginning at Row 11 (row index 10) and continuing down to the final populated row of data.
## Usage
1.	Execute the script
2.	Select Input Data: A native file window will open. Click ENTER in your terminal and select the folder directory hosting your raw .xls files.
3.	Select Save Location: Another file window will prompt you to select a target directory where processing results, log sheets, and summary documents will be outputted.
4.	Interactive Heatmap Loop: The terminal will notify you when processing groups are found. Press ENTER inside the terminal to cycle through graphs.
5.	Raw Output Choice: After closing a dataset heatmap window, choose y or n in the terminal prompt to determine if full un-averaged matrix signals should be saved alongside statistical files.
## Outputs Generated
Every analysis execution yields tab-delimited, format-optimized text files structured for direct implementation into secondary plotting programs like Origin or Excel:
1. Summary Statistics ([FolderName] output.txt)
Contains a row-by-row profile of each micro-coordinate measured:
- date: Original string stamp of data acquisition.
- delta_time: Normalized time in seconds from the first recorded coordinate file ($t_0 = 0$ s).
- filename: The parsed workbook file tracking name.
- x & y: Millimeter stage bounds.
- average & deviation: Extracted voltage signal metrics (expressed in mV).
2. Full Matrix Raw Output ([FolderName] RAW_DATA [GroupLabel].txt)
Optional output storing structural records alongside the complete dimensional data trace:
- Columns list metadata parameters (filename, x, y, average).
-	Followed by the complete collection of raw readings linked to that coordinate space, separated by dual spaces.
