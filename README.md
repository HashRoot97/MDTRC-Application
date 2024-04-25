# MDTRC-Application

Requirements - 
  Python3
  tkinter
  numpy
  matplotlib


On the Acknowledge 5.0 - 

1. If you have already recorded the data, and saved it into the .acq file, Open the file by going to "Open a graph file" -> "Graph file on Disk" and then click Ok and browse the .acq file on the system. 
We will be using "EDA_Events.acq" file for our understanding.

Capture 4

2. After opening the file, the graph for the EDA would be displayed as shown below.

Capture 5

3. You would need two files to run your analysis on the python application which would be generated through Acknowledge 5.0 software - A txt file containing raw dump and .xls file containing the event markers data

4. To generate the txt file, Go to "File" -> "Save As". A dialog box will appear to browse the save location. In the "Save As Type" section select "Text (*.txt, *.csv)". Name the file same as the .acq file, in our case "EDA_Events.txt"

Capture 6,7

5. When you click Save, a dialog box will appear named "Write text file options". Use the following write options.

Capture 8

6. To generate the .xls file for events, go to "Display" -> "Show" -> "Event Pallette". A dialog box named "Events" would appear.

Capture 9

7.  Click on "Summarize in Journal".

Capture 10

8. A new message would appear titled "No Journal is Open", click on "Yes" to continue. If this doesn't appear an event journal is already opened. 

Capture 27

9. A new dialog box will open named "Event Journal Summary". Use the setting as highlighted below and click "Ok".

Capture 11

10. This would open a journal at the bottom as shown containing a list of events.

Capture 29

If the Journal doesn't open, go to "Display" -> "Show" -> "Journal"

Capture 12

12. On the Journal dialog at the bottom, click on the "Save" button which would open the File browser. 

Capture 13

13. While saving select the "Excel Spreadsheet (.xls)" in "Save as type" and name the file same as the text file, "EDA_Events.xls" in our case. Click on "Save"

Capture 14

14. Now you would have the two generated files named "EDA_Events.txt" and "EDA_Events.xls"

Capture 15

15. The contents of both the files is shown below - 

Capture 16, 17


Python Application Setup

1. 

How to Run - python tkinter_application.py

Application Run - 

![Model](https://raw.githubusercontent.com/HashRoot97/MDTRC-Application/tree/main/samples/application_update.png)
