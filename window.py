import tkinter as Tk        # Бибиотека для оконного приложения
import tkinter.ttk as ttk   # Библиотека виджетов для окна

from tables import MacTableFrame
from plotes import *

class MainWindow(Tk.Tk):
# 
  def __init__(self, win_analyz_conn, log):
    Tk.Tk.__init__(self)

    self.conn = win_analyz_conn
    self.log = log

    Tk.Tk.wm_title(self, 'RADMAC')

    self.notebook = ttk.Notebook(self)

    startpage = StartPage(self.notebook, self)
    self.notebook.add(startpage, text='startpage')

    pageone = PageOne(self.notebook, self.log)
    self.notebook.add(pageone, text='pageone')

    self.notebook.pack(side = Tk.TOP, fill = Tk.BOTH, expand = True)
    self.notebook.enable_traversal()
    self.notebook.bind("<<NotebookTabChanged>>", self._select_tab)

    self.label = ttk.Label(self)
    self.label.pack(anchor=Tk.W)

  def _select_tab(self, event):
      tab_id = self.notebook.select()
      tab_name = self.notebook.tab(tab_id, "text")
      text = "Ваш текущий выбор: {}".format(tab_name)
      self.label.config(text=text)

  def run(self):
  # 
    wwidth = self.winfo_screenwidth()
    wheight = self.winfo_screenheight()
    self.geometry('{}x{}'.format(wwidth, wheight))

    self.mainloop()
  # 

  def _data_request(self):
  # 
    while True:
    # 
      self.conn.send(["MACDB REQV", ])
      if (self.conn.poll(timeout = 1) == True):
        msg = self.conn.recv()

        if (msg[0] == "MACDB"):
          mac_base = msg[1]
          break
    # 

    return mac_base
  # 
# 

class StartPage(Tk.Frame):
# 
  def __init__(self, parent, main):
    Tk.Frame.__init__(self, parent)

    table = MacTableFrame(self, main)
    table.pack(side = Tk.BOTTOM, fill = Tk.BOTH, expand = True)
    # Функция недает изменять геометрию фрейма после вставки
    table.pack_propagate(0)

    plot = StartPagePlote(self, main)
    plot.pack(side = Tk.BOTTOM, fill = Tk.BOTH, expand = True)
    table.pack_propagate(0)
# 

class PageOne(Tk.Frame):
# 
  def __init__(self, parent, first):
    Tk.Frame.__init__(self)

    headings = tuple(['#', 'SSID'])
    rows = tuple([(1,'WOP'), (2, 'LRC')])

    reference = ttk.Treeview(self, columns = headings, show = 'headings')
    reference.pack()

    for column in headings:
    # 
      reference.heading(column, text = column, anchor = Tk.CENTER, command=lambda: \
                     self._treeview_sort_column(reference, column, False))
      reference.column(column, anchor = Tk.CENTER)
    # 

    for row in rows:
      reference.insert('', Tk.END, values = tuple(row))

  def _treeview_sort_column(self, tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: \
               self._treeview_sort_column(tv, col, not reverse))
# 