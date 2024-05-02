from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import numpy as np
from scipy.ndimage import gaussian_filter1d
import pandas as pd
import matplotlib.lines as mlines
from tkinter import filedialog
from matplotlib.ticker import FormatStrFormatter
import tkinter.scrolledtext as scrolledtext
import customtkinter
import os
from tkinter import messagebox
from tkinter import ttk
from matplotlib.figure import Figure

# Global variables
parsed_data = []
indexes = []
events = []
list_var = []
events_names = []
events_parsed, file_loaded = False, False
filename = ""

class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set, width=100, height=1000)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(200)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = tk.Frame(canvas, height=1080)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


def error_box(message):
    messagebox.showerror('Error', message)

def parse_data(text_events):
    global filename, parsed_data, indexes, events, list_var, events_names
    # file = os.listdir(file_path)
    events_file = filename.split('.')[0] + '.xls'
    if not os.path.exists(events_file):
        error_box('Excel Events file does not exist in the same path as text file')
        return [], [], []
    # print(events_file)
    dataframe = pd.read_excel(events_file, engine='xlrd')
    # print(dataframe[2:-1])
    try:
        events = np.asarray(dataframe[2:-1]['Unnamed: 1'])
        events_names = np.asarray(dataframe[2:-1]['Unnamed: 4'])
    except:
        error_box('Error in parsing the excel file. Incorrect format')
        return [], [], []
    parsed_events = []
    # exit()
    for ev in events:
        time, _ = ev.split(' ')
        if _ == 'min':
            parsed_events.append(float(time)*60*1000*2)
        else:
            parsed_events.append(float(time)*1000*2)
    parsed_events = np.asarray(parsed_events, dtype=np.int32)
    events = parsed_events
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [line[:-1] for line in lines]
    if not lines[7] == 'min	CH2	CH13	CH14	':
        error_box('Error in parsing the text file. Incorrect format')
        return [], [], []
    lines = lines[10:]
    parsed_data = []
    indexes = []
    index = 0
    for line in lines:
        indexes.append(index)
        parsed_data.append(float(line.split('\t')[2]))
        index += 0.5
    parsed_data = np.asarray(parsed_data, dtype=np.float32)
    indexes = np.asarray(indexes, dtype=np.int32)
    num_events = len(events)
    insert_check_button_event(num_events, text_events, events, events_names)
    return parsed_data, indexes, events

def plot_data(ax, canvas, indexes, parsed_data):
    global events
    avg = np.average(parsed_data)
    print(parsed_data.shape)
    gaus = gaussian_filter1d(parsed_data, 6)
    ax.axhline(y=avg, ls='--', color='blue')
    red_square = mlines.Line2D([], [], color='red', marker='s', linestyle='None',
                          markersize=10, label='Red squares')
    print('plotting events - ', events)
    ax.plot(indexes, parsed_data,'-rs', markevery=events, label='EDA Data')
    ax.plot(indexes, gaus,':', label='Gaussian Smoothened')
    ax.legend(loc="upper left")
    canvas.draw()

def apply_high_low(data, entry_from, indexes):
    filt = entry_from.get()
    en_from, en_to = filt.split(",")
    en_from, en_to = float(en_from), float(en_to)
    new_data = data[data>en_from]
    new_data = new_data[new_data<en_to]
    new_indexes = np.asarray([i for i in range(len(new_data))])

    return new_data, new_indexes

def plot_filtered(fig2, ax2, canvas2, new_data, new_indexes):
    ax2.clear()
    ax2.set_title('Filtered Data')
    ax2.set_xlabel('Time (msec)')
    ax2.set_ylabel('Value')
    
    ax2.plot(new_indexes, new_data, label='EDA Filter')
    ax2.legend(loc="upper left")
    canvas2.draw()

def high_low_filter(fig2, ax2, canvas2, indexes, parsed_data, entry_from, var1, var2):
    if var1.get() == 0:
        ax2.clear()
        canvas2.draw()
        return
    new_data, new_indexes = apply_high_low(parsed_data, entry_from, indexes)
    plot_filtered(fig2, ax2, canvas2, new_data, new_indexes)

def apply_time_filter(data, entry_from, indexes):
    filt = entry_from.get()
    en_from, en_to = filt.split(",")
    en_from, en_to = int(en_from), int(en_to)*2
    new_data = data[en_from:en_to]
    gaus = gaussian_filter1d(new_data, 6)
    # print(parsed_data)
    new_indexes = np.asarray([i for i in range(len(new_data))])
    return new_data, new_indexes, gaus

def time_filter(fig2, ax2, canvas2, indexes, parsed_data, entry_from, var1, var2):
    if var2.get() == 0:
        ax2.clear()
        canvas2.draw()
        return
    parsed_data, new_indexes, gaus = apply_time_filter(parsed_data, entry_from, indexes)
    ax2.clear()
    ax2.set_title('Filtered Data')
    ax2.set_xlabel('Time (msec)')
    ax2.set_ylabel('Value')
    ax2.plot(new_indexes, parsed_data, label='EDA Filter')
    ax2.plot(new_indexes, gaus, label='Gaussian Smoothened')
    ax2.legend(loc="upper left", )

    canvas2.draw()

def apply_filters(fig2, ax2, canvas2, entry_high_low, entry_time, var1, var2):
    global parsed_data, indexes
    if var1.get() == 1 and var2.get() == 1:
        print('Applied both filters')
        new_data, new_indexes, gaus = apply_time_filter(parsed_data, entry_time, indexes)
        new_data, new_indexes =  apply_high_low(new_data, entry_high_low, new_indexes)
        plot_filtered(fig2, ax2, canvas2, new_data, new_indexes)
    elif var1.get() == 1 and var2.get() == 0:
        print('Only applied high low filter filter')
        new_data,new_indexes =  apply_high_low(parsed_data, entry_high_low, indexes)
        plot_filtered(fig2, ax2, canvas2, new_data, new_indexes)
    elif var1.get() == 0 and var2.get() == 1:
        print('Only apply time filter')
        new_data, new_indexes, gaus = apply_time_filter(parsed_data, entry_time, indexes)
        plot_filtered(fig2, ax2, canvas2, new_data, new_indexes)
    else:
        print('Applied no filter')
        return

def browse_file(text_events, var):
    global filename, parsed_data, indexes, events
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"), ("all files", "*.*")))
    print(filename)
    var.set(filename)
    parsed_data, indexes, events = parse_data(text_events)

def insert_check_button_event(num_events, text_events, events, events_names):
    global list_var
    for r in range(num_events):
        var = tk.IntVar()
        check_ = tk.Checkbutton(text_events, text=f'Event - {r} - {events_names[r]}', variable=var, bd=4, font=('Helvetica', 10), bg='white')
        list_var.append(var)
        text_events.window_create('end', window=check_)
        text_events.insert('end', '\n')
    print(events)
    text_events.config(state = "disabled")

def plot_events(fig3, ax3, canvas3):
    global list_var, parsed_data, events
    # threshold = entry.get()
    threshold = 2000
    ind = 0
    data = []
    indexes = []
    for val in list_var:
        # print('Status of event : ', val.get())
        event = events[ind]
        if val.get() == 1:
            indexes.append([i for i in range(event-threshold, event+threshold)])
            data.append(parsed_data[event-threshold:event+threshold])
        ind += 1
    print('Amount of events to be plotted : ', len(data))
    ax3.clear()
    ax3.set_title('Multiple Events Graph')
    ax3.set_xlabel('Time (msec)')
    ax3.set_ylabel('Value')

    new_indexes = [i for i in range(threshold*2)]
    for i in range(len(data)):
        ax3.plot(new_indexes, data[i])
        canvas3.draw()


def plot_single_event(entry_event, ax, canvas, slider, slider2, var, min_data, max_data):

    left_cutoff = int(slider.get())
    right_cutoff = int(slider2.get())

    print(left_cutoff, right_cutoff)

    global list_var, parsed_data, events, events_names
    event_id = entry_event.get()
    event_id = int(event_id)
    ind = 0
    data = []
    indexes = []
    event = events[event_id]
    indexes.append([i for i in range(event-left_cutoff, event+right_cutoff)])
    data.append(parsed_data[event-left_cutoff:event+right_cutoff])
    print('Amount of events to be plotted : ', len(data))
    
    ax.clear()
    ax.set_title('Event ' + str(event_id) + ' Analysis')
    ax.set_xlabel('Time (msec)')
    ax.set_ylabel('Value')
    ax.axvline(x=event)
    ax.plot(indexes[0], data[0])
    min_data.set(str(np.min(data[0])))
    max_data.set(str(np.max(data[0])))
    canvas.draw()

    var.set('Events Title : ' + events_names[event_id])

def create_events_window(root):
    window = tk.Toplevel(root)
    window.title('Single Event Analysis')

    fig = Figure(figsize=(5, 4), dpi=90)
    ax = fig.add_subplot(111)
    ax.set_xlabel('Time (msec)')
    ax.set_ylabel('Value')

    frame = tk.Frame(window)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)

    toolbar_frame = tk.Frame(window)
    toolbar_frame.grid(row=0, column=0, sticky="ew")
    NavigationToolbar2Tk(canvas, toolbar_frame)

    var = tk.StringVar()
    var.set(' ')
    title_label = tk.Label(frame, textvariable=var, font='Helvetica')
    title_label.grid(row=1, column=0, columnspan=2)

    tk.Label(frame, text="Event Number").grid(row=3, column=0)

    entry_event= tk.Entry(frame, width= 40)
    entry_event.focus_set()
    entry_event.grid(row=3, column=1)

    tk.Label(frame, text="Left Cutoff").grid(row=4, column=0)

    slider = customtkinter.CTkSlider(frame, from_=0, to=5000)
    slider.grid(row=5, column=0)
    slider_label = customtkinter.CTkLabel(frame, text=slider.get())
    slider_label.grid(row=6, column=0)
    slider.bind('<ButtonRelease-1>', command=lambda a:[slider_label.configure(text=int(slider.get()))])

    tk.Label(frame, text="Right Cutoff").grid(row=4, column=1)

    slider2 = customtkinter.CTkSlider(frame, from_=0, to=5000)
    slider2.grid(row=5, column=1)
    slider_label2 = customtkinter.CTkLabel(frame, text=slider2.get())
    slider_label2.grid(row=6, column=1)
    slider2.bind('<ButtonRelease-1>', command=lambda a:[slider_label2.configure(text=int(slider2.get()))])

    min_data = tk.StringVar()
    min_data.set("-")
    max_data = tk.StringVar()
    max_data.set("-")
    tk.Button(frame, text='Plot Event', command=lambda: plot_single_event(entry_event, ax, canvas, slider, slider2, var, min_data, max_data)).grid(row=7, column=1)

    tk.Label(frame, text='Absolute Minimum : ').grid(row=8, column=0)
    tk.Label(frame, text='Absolute Maximum : ').grid(row=8, column=1)

    abs_min = tk.Label(frame, textvariable=min_data)
    abs_max = tk.Label(frame, textvariable=max_data)

    abs_min.grid(row=9, column=0)
    abs_max.grid(row=9, column=1)
    frame.grid()

def main():

    root = tk.Tk()
    root.title('MDTRC Data Analysis Application')
    #Main Graph

    frame = tk.Frame(root)

    fig = Figure(figsize=(5, 4), dpi=90)
    ax = fig.add_subplot(111)
    ax.set_title('Original Data Graph with Event Markers')
    ax.set_xlabel('Time (msec)')
    ax.set_ylabel('Value')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=1, column=0)


    fig2 = Figure(figsize=(5, 4), dpi=90)
    ax2 = fig2.add_subplot(111)
    ax2.set_title('Filtered Data Graph')
    ax2.set_xlabel('Index')
    ax2.set_ylabel('Value')

    canvas2 = FigureCanvasTkAgg(fig2, master=frame)
    canvas2.get_tk_widget().grid(row=1, column=1, columnspan=3)

    tk.Button(frame, text='Plot Data', command=lambda: plot_data(ax, canvas, indexes, parsed_data)).grid(row=2, column=0, padx=0, pady=5)
    entry_high_low= tk.Entry(frame, width= 40)
    entry_high_low.focus_set()
    entry_high_low.grid(row=2, column=1)

    entry_time= tk.Entry(frame, width= 40)
    entry_time.focus_set()
    entry_time.grid(row=3, column=1)

    var1 = tk.IntVar()
    var2 = tk.IntVar()
    c1 = tk.Checkbutton(frame, text='High Low Pass Filter',variable=var1, onvalue=1, offvalue=0)
    c1.grid(row=2, column=3, pady=2)
    c2 = tk.Checkbutton(frame, text='Time Filter',variable=var2, onvalue=1, offvalue=0)
    c2.grid(row=3, column=3, pady=2)

    tk.Button(frame, text='Apply Filters', command=lambda: apply_filters(fig2, ax2, canvas2, entry_high_low, entry_time, var1, var2)).grid(row=4, column=1, pady=5)

    toolbar_frame = tk.Frame()
    toolbar_frame.grid(row=0, column=0, sticky="ew")
    NavigationToolbar2Tk(canvas, toolbar_frame)

    # Events List

    frame_events = tk.Frame(root)

    label = tk.Label(frame_events, text='Events List')
    label.config(font=('Helvetica', 15))
    label.grid(row=0, column=0)

    scroll_text = scrolledtext.ScrolledText(frame_events, height=20, width=50)
    scroll_text.grid(row=1, column=0, padx=5)

    # Toolbar

    menu = tk.Menu(root)
    submenu = tk.Menu(menu)
    menu.add_cascade(label='File', menu=submenu)
    submenu.add_command(label='Open File', command=lambda: browse_file(scroll_text, var))
    submenu.add_command(label='Quit')
    menu.add_cascade(label='Help')
    root.config(menu=menu)

    # Multiple Events plot

    fig3 = Figure(figsize=(5, 4), dpi=90)
    ax3 = fig3.add_subplot(111)
    ax3.set_title('Multiple Events Graph')
    ax3.set_xlabel('Index')
    ax3.set_ylabel('Value')

    canvas3 = FigureCanvasTkAgg(fig3, master=frame_events)
    canvas3.get_tk_widget().grid(row=1, column=1)

    tk.Button(frame_events, text='Plot Selected Events', command=lambda: plot_events(fig3, ax3, canvas3)).grid(row=2, column=0)
    tk.Button(frame_events, text='Analyze Single Events', command=lambda: create_events_window(root)).grid(row=3, column=0, pady=5)

    # Footer
    var = tk.StringVar()
    var.set("No File Selected")
    status = tk.Label(frame_events, text="No file selected", bd=1, relief='sunken', textvariable=var)
    status.grid(row=4, column=0, columnspan=3, sticky='w,e')

    frame.grid(row=1, column=0) 
    frame_events.grid(row=3, column=0)

    root.mainloop()


    # Single Events Analysis

    # window = tk.Toplevel(root)
    # fig4, ax4 = plt.subplots()
    # frame_single = tk.Frame(root)
    # canvas4 = FigureCanvasTkAgg(fig4, master=frame_single)
    # canvas4.get_tk_widget().grid(row=3, column=0, columnspan=2, padx=10)

    # tk.Label(frame_single, text="Event Number").grid(row=2, column=0)

    # entry_event= tk.Entry(frame_single, width= 40)
    # entry_event.focus_set()
    # entry_event.grid(row=2, column=1)

    # toolbar_frame = tk.Frame(root)
    # toolbar_frame.grid(row=0, column=1, sticky="ew")
    # NavigationToolbar2Tk(canvas4, toolbar_frame)

    # tk.Label(frame_single, text="Left Cutoff").grid(row=4, column=0)
    # slider = customtkinter.CTkSlider(frame_single, from_=0, to=5000)
    # slider.grid(row=5, column=0)
    # slider_label = customtkinter.CTkLabel(frame_single, text=slider.get())
    # slider_label.grid(row=6, column=0)
    # slider.bind('<ButtonRelease-1>', command=lambda a:[slider_label.configure(text=int(slider.get()))])

    # tk.Label(frame_single, text="Right Cutoff").grid(row=4, column=1)
    # slider2 = customtkinter.CTkSlider(frame_single, from_=0, to=5000)
    # slider2.grid(row=5, column=1)
    # slider_label2 = customtkinter.CTkLabel(frame_single, text=slider2.get())
    # slider_label2.grid(row=6, column=1)
    # slider2.bind('<ButtonRelease-1>', command=lambda a:[slider_label2.configure(text=int(slider2.get()))])

    # tk.Button(frame_single, text='Plot Event', command=lambda: plot_single_event(entry_event, ax4, canvas4, slider, slider2)).grid(row=7, column=1)


    # frame_top = tk.Frame(root, width=100, height=50)
    # frame_graphs = VerticalScrolledFrame(root)
    # frame_graphs = tk.Frame(root, width=100, height=800)
    # label = tk.Label(frame_top, text='')
    # label.config(font=('Helvetica', 32))
    # label.grid(row=0, column=0)

    # tk.Button(frame_bottom, text='Browse Data File', command=lambda: browse_file(text_events, var)).grid(row=0, column=0, padx=0, pady=10)

    # tk.Scrollbar(frame_events, orient = 'vertical').grid(row=0, column=1)

    # scroll_bar_events = tk.Scrollbar(frame)
    # scroll_bar_events.grid(row=1, column=2)
    # get_multiple_graphs(frame_graphs, number_graphs, [])

    # label = tk.Label(frame, text='Events List')
    # label.config(font=('Helvetica', 15))
    # label.grid(row=0, column=1)

    # text_events = tk.Text(frame, bg='SystemButtonFace')
    # text_events.grid(row=1, column=1)
    # text_events.configure(yscrollcommand=scroll_bar_events.set)
    # scroll_bar_events.configure(command=text_events.yview)

    # parse_events('./data/Events.xls')


    # root.grid_rowconfigure(0, weight=1)
    # root.grid_columnconfigure(0, weight=2, uniform="group1")
    # root.grid_columnconfigure(1, weight=1, uniform="group1")

    # frame_top.grid(row=0, column=0)

if __name__ == "__main__":
    main()

# def get_multiple_graphs_again(frame_graphs, num_graphs, data, indexes):

#     fig, axes = plt.subplots(num_graphs, 1,sharex=True,figsize=(5, 80))

#     for k in range(num_graphs):  
#         axes[k].plot(indexes[k], data[k])
        
#     canvas = FigureCanvasTkAgg(fig, master=frame_graphs.interior)
#     canvas.draw()
#     canvas.get_tk_widget().grid(row=0, column=0)


# def get_multiple_graphs(frame_graphs, num_graphs, data):

#     fig, axes = plt.subplots(5, 1,sharex=True,figsize=(5, 80))

#     t=np.linspace(0,1,1000)

#     for k in range(5):  
        
#         axes[k].plot(t,np.sin(2*np.pi*t*k))
        
#     canvas = FigureCanvasTkAgg(fig, master=frame_graphs.interior)
#     canvas.draw()
#     canvas.get_tk_widget().grid(row=0, column=0)


    # scroll_bar_events = tk.Scrollbar(frame_graphs)
    # scroll_bar_events.grid(row=0, column=1)
    # for i in range(num_graphs):
    #     fig, ax = plt.subplots()
    #     canvas = FigureCanvasTkAgg(fig, master=frame_graphs)
    #     canvas.get_tk_widget().grid(row=i, column=0)
