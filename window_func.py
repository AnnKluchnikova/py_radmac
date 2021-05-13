from datetime import datetime as Dt   # Работа с unix временем

def _parser_to_mac_table(data):
# 
  rows = list()

  # Создаем заголовки
  headings = ('MAC address', 'Time',
              'Messages', 'Status', 'Vendor')

  # Собираем данные в нужную форму
  for record in data:
  # 
      mac, time, mask, status, org, noneed = record.values()
      time = Dt.fromtimestamp(int(time)).strftime('%m/%d/%Y, %H:%M:%S')

      msg = None
      if (mask & 2 == 2):
      # 
          msg = "probe"
      # 
      if (mask & 1 == 1):
      # 
          msg = (msg + "/assoc" if msg is not None else "assoc")
      # 
      if (mask & 4 == 4):
      # 
          msg = (msg + "/data" if msg is not None else "data")
      # 

      value = [mac, time, msg, status, org]
      rows.append(value)
  # 

  rows = tuple(rows)

  return headings, rows
# 