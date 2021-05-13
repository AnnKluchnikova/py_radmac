import json
import numpy as np
import tkinter as Tk
import datetime as dt
import tkinter.ttk as ttk
import matplotlib.dates as md
from itertools import groupby
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
  FigureCanvasTkAgg, NavigationToolbar2Tk)

class StartPagePlote(Tk.Frame):
# 
  def _axs1_get_data(self):
  # 
    data = self.request()
    timestamps = list(int(time['timestamp']) for time in data)

    hist_data = [dt.datetime.fromtimestamp(ts) for ts in timestamps]
    hist_data.sort()

    counter = {i:hist_data.count(i) for i in hist_data}
    line_data = [0, ]
    for key, val in counter.items():
      if (line_data[0] == 0):
        line_data.clear()
        line_data.append(val)
      else:
        line_data.append(val+ line_data[len(line_data) - 1])
    # print(line_data)

    return hist_data
  # 

  def axs1_update(self):
  # 
    n_bins = 24

    os_x = self._axs1_get_data()
    self.axs1.clear()
    self.axs1.set_title('New unique MAC addresses', fontsize=20)
    self.axs1.set_ylabel('MAC Quantity', fontsize=15)
    self.axs1.set_xlabel('Data', fontsize=15)
    n, bins, patches = self.axs1.hist(os_x, bins = n_bins)

    self.fig.autofmt_xdate(rotation = 10)
    tm_form = md.DateFormatter('%d/%m %H:%M')
    self.axs1.xaxis.set_major_formatter(tm_form)

    for i in range(len(patches)):
      patches[i].set_facecolor(plt.cm.viridis(n[i]/max(n)))
  # 

  def animate(self, val):
  # 
    self.axs1_update()
  # 

  def __init__(self, parent, main):
    Tk.Frame.__init__(self, parent)

    self.request = main._data_request

    self.configure(width = 0.5 * parent.winfo_screenwidth(),\
                   height = 0.5 * parent.winfo_screenheight())

    self.fig = plt.Figure()
    self.axs1 = self.fig.add_subplot(121)

    # self.axs2 = self.fig.add_subplot(222)
    # self.axs2 = self.fig.add_subplot(224)

    canvas = FigureCanvasTkAgg(self.fig, master=self)
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, self)
    toolbar.update()

    canvas._tkcanvas.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=True)

    self.ani = FuncAnimation(self.fig, self.animate, interval = 10000)
# 

# class RushHourPlot()
# # 
#   def __init__(self, parent):
# # 