from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import tkinter as tk
import numpy as np
from scipy.ndimage import gaussian_filter1d
import pandas as pd
import matplotlib.lines as mlines

def parse_data(file_path="./data/EDA_Events2.txt", events_file ="./data/Events.xls"):
    # file = os.listdir(file_path)
    dataframe = pd.read_excel(events_file, engine='xlrd')
    events = np.asarray(dataframe[2:-1]['Unnamed: 1'])
    parsed_events = []
    # exit()
    for ev in events:
        time, _ = ev.split(' ')
        if _ == 'min':
            parsed_events.append(float(time)*60*1000*2)
        else:
            parsed_events.append(float(time)*1000*2)
    parsed_events = np.asarray(parsed_events, dtype=np.int32)
    print(parsed_events)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines = [line[:-1] for line in lines]
    lines = lines[10:]
    parsed_data = []
    indexes = []
    index = 0
    for line in lines:
        indexes.append(index)
        parsed_data.append(float(line.split('\t')[1]))
        index += 0.5
    parsed_data = np.asarray(parsed_data, dtype=np.float32)
    indexes = np.asarray(indexes, dtype=np.int32)
    return parsed_data, indexes, parsed_events


def plot_data(ax, canvas, indexes, parsed_data, events):
    avg = np.average(parsed_data)
    print(parsed_data.shape)
    gaus = gaussian_filter1d(parsed_data, 6)
    ax.axhline(y=avg, ls='--', color='blue')
    red_square = mlines.Line2D([], [], color='red', marker='s', linestyle='None',
                          markersize=10, label='Red squares')
    ax.plot(indexes, parsed_data,'-rs', markevery=events, label='EDA Data')
    ax.plot(indexes, gaus,':', label='Gaussian Smoothened')
    ax.legend(loc="upper left")
    canvas.draw()

def apply_high_low(data, entry_from, indexes):
    filt = entry_from.get()
    en_from, en_to = filt.split(",")
    en_from, en_to = int(en_from), int(en_to)
    new_data = data[data>en_from]
    new_data = new_data[new_data<en_to]
    new_indexes = np.asarray([i for i in range(len(new_data))])

    return new_data, new_indexes

def plot_filtered(fig2, ax2, canvas2, new_data, new_indexes):
    ax2.clear()
    ax2.set_title('Filtered Data')
    ax2.set_xlabel('Time')
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
    en_from, en_to = int(en_from), int(en_to)
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
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Value')
    ax2.plot(new_indexes, parsed_data, label='EDA Filter')
    ax2.plot(new_indexes, gaus, label='Gaussian Smoothened')
    red_square = mlines.Line2D([], [], color='red', marker='s', linestyle='None',
                          markersize=10, label='Red squares')
    ax2.legend(loc="upper left", )

    canvas2.draw()

def main():

    parsed_data, indexes, events = parse_data()

    root = tk.Tk()
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    ax.set_title('Original Data with Event Markers')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')

    ax2.set_title('Filtered Data')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Value')

    frame = tk.Frame(root)
    frame_top = tk.Frame(root, width=100, height=50)
    frame_bottom = tk.Frame(root)
    frame_events = tk.Frame(root)
    label = tk.Label(frame_top, text="MDTRC Data Analysis Application")
    label.config(font=("Helvetica", 32))
    label.grid(row=0, column=0)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=1, column=0)

    canvas2 = FigureCanvasTkAgg(fig2, master=frame)
    canvas2.get_tk_widget().grid(row=1, column=2)

    tk.Button(frame_bottom, text="Plot Data", command=lambda: plot_data(ax, canvas, indexes, parsed_data, events)).grid(row=0, column=1, padx=0, pady=10)

    # label_high_low = tk.Label(frame_bottom, text="High Low Pass Filter Range (Format=x,y) : ")
    # label_high_low.config(font=("Helvetica", 10))
    # label_high_low.grid(row=1, column=0)

    entry_high_low= tk.Entry(frame_bottom, width= 40)
    entry_high_low.focus_set()
    entry_high_low.grid(row=1, column=2)

    # label_time = tk.Label(frame_bottom, text="Time Filter Range (Format=x,y) : ")
    # label_time.config(font=("Helvetica", 10))
    # label_time.grid(row=2, column=0)

    entry_time= tk.Entry(frame_bottom, width= 40)
    entry_time.focus_set()
    entry_time.grid(row=2, column=2)

    var1 = tk.IntVar()
    var2 = tk.IntVar()
    c1 = tk.Checkbutton(frame_bottom, text='High Low Pass Filter',variable=var1, onvalue=1, offvalue=0, command=lambda: high_low_filter(fig2, ax2, canvas2, indexes, parsed_data, entry_high_low, var1, var2))
    c1.grid(row=1, column=1, pady=10)
    c2 = tk.Checkbutton(frame_bottom, text='Time Filter',variable=var2, onvalue=1, offvalue=0, command=lambda: time_filter(fig2, ax2, canvas2, indexes, parsed_data, entry_time, var1, var2))
    c2.grid(row=2, column=1, pady=10)

    # tk.Button(frame_bottom, text="High Low Pass Filter", command=lambda: high_low_filter(fig2, ax2, canvas2, indexes, parsed_data, entry_high_low)).grid(row=1, column=2, pady=10)
    # tk.Button(frame_bottom, text="Time Filter", command=lambda: time_filter(fig2, ax2, canvas2, indexes, parsed_data, entry_time)).grid(row=2, column=2, pady=10)

    # scroll_bar = tk.Scrollbar(frame_events)
    # scroll_bar.grid(row=0, column=0)
    # text_area = tk.Text(frame_events)
    # text_area.grid(row=0, column=0)

    frame_top.grid()
    frame.grid()
    frame_bottom.grid()

    root.mainloop()


if __name__ == "__main__":
    main()