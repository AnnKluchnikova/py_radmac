import analyzer_func as func
import gc

# ==============================[Внешний класс]=================================

class DataAnalyzer():
# 
  def __init__(self, analyz_serv_conn, analyz_win_conn, log):
  # 
    self.serv_conn = analyz_serv_conn
    self.win_conn = analyz_win_conn
    self.log = log
    self.oui_base = None
    self.mac_base = None
  # 

  def _update_other_info(self, index, element, location):
  # 
    j = 0
    get_loc = False
    other = self.mac_base[index]['other']

    # Ищем в списке нужный объект локации
    while j < len(other):
    # 
      if (other[j]['location'] == location):
        get_loc = True
        break

      j += 1
    # 

    # Если о локации уже есть информация, то обновляем ее...
    if (get_loc == True):
    # 
      # TODO Что если у ТД будет сбито время?
      current = int(element['timestamp'])
      first = int(other[j]['first_time'])
      last = int(other[j]['last_time'])

      if (current > last):
      # 
        other[j].update({'last_time': element['timestamp']})

        # Увеличиваем счетчик появлений в локации
        reps = other[j]['reps_count'] + 1
        other[j].update({'reps_count': reps})
      # 
      else:
        # TODO Что если у ТД будет сбито время?
        return
    # 
    else:
    # 
    # ...иначе добавляем новую запись о локации
      ssid = element['ssid']
      other = dict(
              location = location,
              first_time = element['timestamp'],
              last_time = element['timestamp'],
              reps_count = 1,
              ssid = list([ssid]) if (ssid != "") else list()
            )
      mac_base[index]['other'].append(other)
    # 
  # 

  def _filter(self, element):
  # 
    ret = False
    status = "unconfirmed"
    org = "unknown"

    # Проверка на гловабльную/локальную уникальность
    oktet = int(element['mac'][0:2], 16)
    if (oktet & 2 == 2):
        return ret, status, org

    # Поиск производителя
    mac_id = element['mac'][0:8]

    for oui in self.oui_base:
    # 
      if(mac_id == oui['hex']):
      # 
        ret = True
        org = oui['org']
        break
      # 
    # 

    # Смотрим тип пакета
    mask = int(element['type_bitmask'])
    if (mask & 4 == 4):
    # 
      if(ret == True):
        status = "confirmed"
      else:
        ret == True
    # 

    return ret, status, org
  # 

  def _parser(self, new_data):
  # 
    repit_c = 0
    unique_c = 0

    # Сравниваем элементы двух коллекций
    for element in new_data['probe_requests']:
    # 
      is_not_uniq = False
      index = 0

      # Отфильтровываем адреса (сгенерированные MAC)
      ret, status, org = self._filter(element)
      if (ret == False):
        continue

      # Сравниваем адрес с имеющейся базой и обновляем данные
      while index < len(self.mac_base):
      # 
        if (element['mac'] == self.mac_base[index]['mac']):
        # 
          # Обновить статус
          if (self.mac_base[index]['status'] == "unconfirmed"):
            self.mac_base[index].update({'status': status})

          # Занести данные об организации
          if (self.mac_base[index]['vendor'] == "unknown"):
            self.mac_base[index].update({'vendor': org})

          # Обновить маску пакетов
          self.mac_base[index]['type_bitmask'] = \
            self.mac_base[index]['type_bitmask'] | element['type_bitmask']

          # Обновить дополнительную информацию
          self._update_other_info(index, element, new_data['ap_name'])

          repit_c += 1
          is_not_uniq = True
          break
        # 

        index += 1
      # 

      if (is_not_uniq == False):
      # 
        unique_c += 1
        # Дополнительная информация о клиенте: места посещения,
        # время пребывания в каждом из них, обращения к ТД по SSID
        try:
          ssid = element['ssid']
        except KeyError:
          ssid = ""

        other = [{
                  'location': new_data['ap_name'],
                  'first_time': element['timestamp'],
                  'last_time': element['timestamp'],
                  'reps_count': 1,
                  'ssid': list([ssid]) if (ssid != "") else list()
                }]

        # Первая запись уникального адреса
        unique = dict(
                      mac = element['mac'],
                      timestamp = element['timestamp'],
                      type_bitmask = element['type_bitmask'],
                      status = status,
                      vendor = org,
                      other = other
                    )

        self.mac_base.append(unique)
      # 
    # 

    if (unique_c != 0):
    # 
      self.log._print(self.log.INFO, f"{unique_c} new addresses detected: ")
      return True
    # 
    elif (repit_c != 0):
      return True

    return False
  # 

  def _main_loop(self):
  # 
    try:
    # 
      while True:
      # 
        while True:
        # 
          if (self.win_conn.poll() == True):
          # 
            msg = self.win_conn.recv()

            self.log._print(self.log.DEBAG, f"analyzer: [MSG] {msg[0]}")

            if (msg[0] == "MACDB REQV"):
              self.win_conn.send(["MACDB", self.mac_base])
          # 

          if (self.serv_conn.poll() == True):
          # 
            msg = self.serv_conn.recv()

            self.log._print(self.log.DEBAG, f"analyzer: [MSG] {msg[0]}")

            if (msg[0] == "ANALYZ"):
              # self.log._print(self.log.DEBAG, "analyz: msg from server: \n {}".\
              #         format(func.debag_json_print(msg[1])))
              break
            else:
              gc.collect()
          # 
        # 

        if (self._parser(msg[1]) == True):
          func._save_mac_base(self.mac_base, self.mac_f_path)
          # self.win_conn.send(["MACDB", self.mac_base])

        gc.collect()
      # 
    # 
    except KeyboardInterrupt:
      pass
  # 

  # ---------------------[Методы для внешнего использования]--------------------

  def run(self):
  # 
    self.oui_base = func._get_oui_base(self.log)
    if self.oui_base is None:
      return

    self.mac_base, self.mac_f_path = func._get_mac_base()
    if self.mac_base is None:
      return

    self._main_loop()
  # 

  # ----------------------------------------------------------------------------
# 

# ==============================================================================