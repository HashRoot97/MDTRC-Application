# MDTRC Data Analysis Application

A tool to analyse the EDA data captured using BIOPAC and Acknowledge 5.0 with the various events using various visualizations.

<img src="./samples/Sample_main4.png">

## Requirements - 
  Window 11 

  Python 3.11.9
  
  BIOPAC
  
  Acknowledge 5.0
  
  Resolution compatible - 1920x1080


## On the Acknowledge 5.0 - 

1. If you have already recorded the data, and saved it into the .acq file, Open the file by going to "Open a graph file" -> "Graph file on Disk" and then click Ok and browse the .acq file on the system. 
We will be using "EDA_Events.acq" file for our understanding.

<img src="./samples/Capture4.PNG">

2. After opening the file, the graph for the EDA would be displayed as shown below.

<img src="./samples/Capture5.PNG">

3. You would need two files to run your analysis on the python application which would be generated through Acknowledge 5.0 software - A txt file containing raw dump and .xls file containing the event markers data

4. To generate the txt file, Go to "File" -> "Save As". A dialog box will appear to browse the save location. In the "Save As Type" section select "Text (*.txt, *.csv)". Name the file same as the .acq file, in our case "EDA_Events.txt"

<img src="./samples/Capture6.png">
<img src="./samples/Capture7.png">

5. When you click Save, a dialog box will appear named "Write text file options". Use the following write options.

<img src="./samples/Capture8.PNG">

6. To generate the .xls file for events, go to "Display" -> "Show" -> "Event Pallette". A dialog box named "Events" would appear.

<img src="./samples/Capture9.png">

7.  Click on "Summarize in Journal".

<img src="./samples/Capture10.png">

8. A new message would appear titled "No Journal is Open", click on "Yes" to continue. If this doesn't appear an event journal is already opened. 

<img src="./samples/Capture27.PNG">

9. A new dialog box will open named "Event Journal Summary". Use the setting as highlighted below and click "Ok".

<img src="./samples/Capture11.PNG">

10. This would open a journal at the bottom as shown containing a list of events.

<img src="./samples/Capture29.PNG">

If the Journal doesn't open, go to "Display" -> "Show" -> "Journal"

<img src="./samples/Capture12.png">

12. On the Journal dialog at the bottom, click on the "Save" button which would open the File browser. 

<img src="./samples/Capture13.PNG">

13. While saving select the "Excel Spreadsheet (.xls)" in "Save as type" and name the file same as the text file, "EDA_Events.xls" in our case. Click on "Save"

<img src="./samples/Capture14.png">

14. Now you would have the two generated files named "EDA_Events.txt" and "EDA_Events.xls"

<img src="./samples/Capture15.PNG">

15. The contents of both the files is shown below - 

<img src="./samples/Capture32.png">
<img src="./samples/Capture33.png"> 

If the header of the text file does not match, replace the following header - 

EDA_Events.acq

0.5 msec/sample

2 channels

PPG, X, PPGED-R

Volts

EDA, Y, PPGED-R

microsiemens

16. Place both the text and xls files in one folder, preferably inside the python application folder named "data".

## Python Application Setup

1. Install Python 3.11.9

2. Activate the python package installer pip, if not done already.

3. Open the terminal and execute the following command to install the required python packages - 
  pip install matplotlib tk numpy scipy pandas customtkinter xlrd

4. In the terminal, go to the folder where the code is kept.

5. Run the following command to run the application - 
  python tkinter_application.py

6. Once the application opens, click on "Open File". Browse the path where both text file and .xls file have been stored which were extracted from the Acknowledge 5.0. Click on the text file to open.

<img src="./samples/Sample2.png">

7. For our demonstration, we will be using "EDA_Events.xls" and "EDA_Events.txt" generated which are placed under the "data" folder.

8. The "No File Selected" label would be updated to File location and the events list would be populated once the data has been successfully loaded.

## Features of the Application 

1. Plot whole data with event markers - The whole of data can be plotted and analyzed by clicking on the "Plot Data" button. The graph titled "Original Data Graph with Event Markers" will be plotted. The various utility tools like zooming and navigating are placed above the same graph.

<img src="./samples/Sample4.png">

2. Filtered Data - Two filters have been provided namely "Gaussian Filter" and "Time Filter". The input to the gaussian filter is the sigma for the filter, example - 40 (sigma - 40). The input to the "Time Filter" is the from and to time stamp in msec seperated by a comma, example - 0,100000 (for time stamp between 0msec and 100000msec) Tick the appropriate filter and enter the threshold in the following manner - 

After this, click on "Apply Filters" button and the "Filtered Data Graph" will be populated with the filtered data.

<img src="./samples/Sample53.png">

3. Events list - The events list contains the list of events with their names for reference.

<img src="./samples/Sample6.png">

4. Multiple Event Graph - Multiple events can be superimposed and plotted on the same graph for analysis between events. Tick the required events in the Events list and click on "Plot Selected Events". Doing so would plot each selected event for 3000 msec on the "Multiple Events Graph" plot.

<img src="./samples/Sample7.png">

5. Single Event Analyzer - Single Event Analyzer is used to analyze islotaed events and display and dump statistics about it. It can also apply various filters like moving average filter and Gaussian filter to the input signal . Enter the event number in the "Event number" input box provided (refer the Events list), and select the msec left and right cutoff to dispay the graph of the event. The maximum seek for the left and right part is 10,000 msec. Additionally to display the filtered signals as well, use the checkboxes for the moving average filter and Gaussian filter accordingly. The input to moving average filter needs to be provided as the window size of the moving average, example - 100 (for moving average of 100 msec). The input to gaussian filter needs to be provided as the sigma for the filtering, example - 40 (for sigma = 40). After selecting these parameters, click on "Plot Event & Analyze". The appropriate signals will be plotted.

<img src="./samples/Sample51.png">

6. Analyzer Journal - This feature can be used to dump the statistics into a text file for a single event analysis. After clicking the "Plot Event & Analysis" from the Single Event Analyzer, the user can click on "Add to Journal". This button would add the current selected events analysis parameters like "Absolute minimum" and "Absolute maximum" to the Journal text box. After the journal entry has been added, the user can dump the journal into a text file. Use the button "Dump Journal to File" for doing so.

<img src="./samples/Sample52.png">