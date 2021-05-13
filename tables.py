import tkinter as Tk        # Бибиотека для оконного приложения
import tkinter.ttk as ttk   # Библиотека виджетов для окна

import window_func as func   # Собственная библиотека с доп.функциями

import time

class MacTableFrame(Tk.Frame):
  def __init__(self, parent, main):
    Tk.Frame.__init__(self, parent)

    self.configure(width = 0.5 * parent.winfo_screenwidth(),\
                   height = 0.5 * parent.winfo_screenheight())

    table = UniqueMacTable(self, main)
    table.pack(fill = Tk.BOTH, expand = True)

    # Обновление таблицы происходит только по нажатию кнопки
    update = Tk.Button(self, bg = '#FFB6C1', text = 'Update', width = 20,\
                        command = lambda: table.update_table(main))
    update.pack(side = Tk.LEFT, anchor = Tk.S)

class UniqueMacTable(ttk.Treeview):
# 
  def _get_mac_table_data(self, request):
  # 
    data = request()
    headings, rows = func._parser_to_mac_table(data)
    return headings, rows
  # 

  def __init__(self, parent, main):
    super().__init__(parent)

    # Тег для определение цвета закраски вставляемой строки
    self.tag_configure('bg_87CEEB', background = '#87CEEB')
    self.tag_configure('bg_FA8072', background = '#FA8072')

    headings, rows = self._get_mac_table_data(main._data_request)

    self.configure(columns = headings, show = 'headings')

    for column in headings:
    # 
      if (column != 'Vendor'):
        self.heading(column,text = column, anchor = Tk.CENTER)
        self.column(column, anchor = Tk.CENTER)
    # 

    self.heading(column,text = column, anchor = Tk.CENTER, command=lambda: \
                       self._treeview_sort_column(self, column, False))
    self.column(column, anchor = Tk.CENTER)

    for row in rows:
      self.insert('', Tk.END, values = tuple(row))

    # Установим прокрутку таблицы по двум осям
    yscroll = Tk.Scrollbar(self, command = self.yview)
    self.configure(yscrollcommand = yscroll.set)
    yscroll.pack(side = Tk.RIGHT, fill = Tk.Y)
    self.pack(expand = Tk.YES, fill = Tk.BOTH)

    xscroll = Tk.Scrollbar(self, orient = Tk.HORIZONTAL)
    xscroll.config(command = self.xview)
    self.configure(xscrollcommand = xscroll.set)
    xscroll.pack(side = Tk.BOTTOM, fill=Tk.X)
    self.pack()
  # 

  # Переопределение метода insert() для раскраски строк таблицы
  def insert(self, parent_node, index, **kwargs):
  # 
    item = super().insert(parent_node, index, **kwargs)

    values = kwargs.get('values', None)

    if values:
    # 
      if (values[3] == 'unconfirmed'):
        super().item(item, tag = 'bg_87CEEB')
      elif (values[4] == 'unknown'):
        super().item(item, tag = 'bg_FA8072')
    # 

    return item
  # 

  def _treeview_sort_column(self, tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    tv.heading(col, command=lambda: \
               self._treeview_sort_column(tv, col, not reverse))

  def _delete_table(self):
  # 
    for i in self.get_children():
      self.delete(i)
  # 

  def update_table(self, main):
  # 
    headings, rows = self._get_mac_table_data(main._data_request)
    self._delete_table()

    for row in rows:
      self.insert('', Tk.END, values = tuple(row))

    self.update()
  # 
# 