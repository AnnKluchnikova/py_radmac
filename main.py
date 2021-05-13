"""
Головная программа, которая создает потоки для трех функциональных частей:
  для сервера, импортируя как SERVER
  для анализатора, импортируя как ANALYZER
  для графической оболочки, импортируя как GUI
"""
# Команда для сборки проекта в исполняемый файл
# pyinstaller --onefile main.py

from multiprocessing import Process, Pipe      # Для многопроцессорной работы
from http_server import WebServer as SERVER    # Библиотека для работы с http-сервером
from analyzer import DataAnalyzer as ANALYZER  # Библиотека для работы с анализатором данных
from window import MainWindow as GUI           # Библиотека для графического отображения работы App

# Получение аргументов из командной строки
from sys import argv

# Собственная библиотека для управления логированием
import my_logging as lg

def server_for_wap(serv_analyz_conn, log):
# 
  server = SERVER(serv_analyz_conn, log)
  server.run(9090, '192.168.1.1') # TODO Можно задавать при запуске
# 

def app_analyzer(analyz_serv_conn, analyz_win_conn, log):
# 
  analizer = ANALYZER(analyz_serv_conn, analyz_win_conn, log)
  analizer.run()
# 

def app_window(win_analyz_conn, log):
# 
  window = GUI(win_analyz_conn, log)
  window.run()
# 

def main():
# 
  print("\nStart the app...\n")

  # Устанавливаем маску логирования
  # Если не установлено, то по умолчанию логирование выключено
  log = None

  if (len(argv) == 3):
    if (argv[1] == "--logmask"):
      log = lg._logging(int(argv[2]))
  else:
    log = lg._logging(lg.OFF)

  try:
  # 
    # Двусторонняя связь анализатора с сервером
    serv_analyz_conn, analyz_serv_conn = Pipe()
    # Двусторонняя связь анализатора с окном
    analyz_win_conn, win_analyz_conn = Pipe()

    p1 = Process(target = server_for_wap, args = (serv_analyz_conn, log))
    p2 = Process(target = app_analyzer, args = (analyz_serv_conn, analyz_win_conn, log))
    p3 = Process(target = app_window, args = (win_analyz_conn, log))
# 
    p1.start()
    p2.start()
    p3.start()

    # Надо следить, чтобы процессы работали
    # Иначе завершаем работу всей программы
    while True:
    # 
      live2 = p2.is_alive()
      live3 = p3.is_alive()

      if (live2 == False):
      # 
        log._print(log.FATAL, "The analyzer stopped working")
        if True:
          raise KeyboardInterrupt
      # 

      if (live3 == False):
      # 
        log._print(log.FATAL, "The GUI stopped working")
        if True:
          raise KeyboardInterrupt
      # 
      # else:
      #   log._print(log.DEBAG, "The GUI is alive")
    # 
  # 
  except KeyboardInterrupt:
  # 
    print("\nShutting down the app...\n")

    if(p1.is_alive() == True):
      p1.terminate()            # TODO Тут не срабатывает p1.join()
    if(p2.is_alive() == True):
      p2.terminate()            # TODO Тут не срабатывает p2.join()
    if(p3.is_alive() == True):
      p3.terminate()            # TODO ОПАСНО! Создаваемый внутри процесс может продолжать работать

    serv_analyz_conn.close()
    analyz_serv_conn.close()

    analyz_win_conn.close()
    win_analyz_conn.close()
  # 
# 

# ==============================================================================

if __name__ == '__main__':
# 
  main()
# 