from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import tkinter as tk
import numpy as np
import os

def parse_data(file_path="./EDA_Sample.txt"):
    # file = os.listdir(file_path)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    lines = [line[:-1] for line in lines]
    lines = lines[10:]
    parsed_data = []
    indexes = []
    index = 0
    for line in lines:
        indexes.append(index)
        parsed_data.append(float(line.split(',')[1]))
        index += 1
    parsed_data = np.asarray(parsed_data, dtype=np.float32)
    indexes = np.asarray(indexes, dtype=np.int32)
    avg = np.average(parsed_data)
    return parsed_data, indexes 


def plot_data(ax, canvas, indexes, parsed_data):
    avg = np.average(parsed_data)
    ax.axhline(y=avg, ls='--', color='Green')
    ax.plot(indexes, parsed_data)
    canvas.draw()

def high_low_filter(ax2, canvas2, indexes, parsed_data, entry_from):
    filt = entry_from.get()
    en_from, en_to = filt.split(",")
    en_from, en_to = int(en_from), int(en_to)
    new_data = parsed_data[parsed_data>en_from]
    new_data = new_data[new_data<en_to]
    new_indexes = np.asarray([i for i in range(len(new_data))])
    ax2.plot(new_indexes, new_data)
    canvas2.draw()

def time_filter(ax2, canvas2, indexes, parsed_data, entry_from):
    filt = entry_from.get()
    en_from, en_to = filt.split(",")
    en_from, en_to = int(en_from), int(en_to)
    parsed_data = parsed_data[en_from:en_to]
    # print(parsed_data)
    new_indexes = np.asarray([i for i in range(len(parsed_data))])
    ax2.plot(new_indexes, parsed_data)
    canvas2.draw()

def main():
    root = tk.Tk()
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()

    frame = tk.Frame(root)
    label = tk.Label(text="MDTRC Sample Application")
    label.config(font=("Courier", 32))
    label.pack()

    label2 = tk.Label(text="Original Data")
    label2.config(font=("Courier", 20))
    label2.pack()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack()

    canvas2 = FigureCanvasTkAgg(fig2, master=frame)
    canvas2.get_tk_widget().pack()

    entry_from= tk.Entry(frame, width= 40)
    entry_from.focus_set()
    entry_from.pack()

    parsed_data, indexes = parse_data()
    frame.pack()

    tk.Button(frame, text="Plot Data", command=lambda: plot_data(ax, canvas, indexes, parsed_data)).pack(pady=10)
    tk.Button(frame, text="High Low Pass Filter", command=lambda: high_low_filter(ax2, canvas2, indexes, parsed_data, entry_from)).pack(pady=10)
    tk.Button(frame, text="Time Filter", command=lambda: time_filter(ax2, canvas2, indexes, parsed_data, entry_from)).pack(pady=10)


    root.mainloop()


if __name__ == "__main__":
    main()