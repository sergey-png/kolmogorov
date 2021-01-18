import math
import os
import subprocess
import sys

import pylab
from scipy import stats

from base import *


# use command to generate .exe file: pyinstaller --name="MyApplication" --windowed --onefile main.py

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Здесь прописываем событие нажатия на кнопку
        self.ui.earse.clicked.connect(self.earse_b)  # кнопка Стереть все данные +
        self.ui.start.clicked.connect(self.start_b)  # кнопка Старт +
        self.ui.read.clicked.connect(self.read_b)  # кнопка Считать данные из файла +
        self.ui.show_1.clicked.connect(self.show_1)  # кнопка Показать входные данные +
        self.ui.draw_graph.clicked.connect(self.draw_plots)  # кнопка Построить график +
        self.ui.openfile.clicked.connect(self.openfile)  # кнопка Открыть файл в текстовом редакторе +
        self.ui.save.clicked.connect(self.savefile)  # кнопка Сохранить данные в LOG-файл +
        self.ui.calculate.clicked.connect(self.calculate_all)  # кнопка Провести расчет +

    def earse_b(self):
        global massive_input, alpha, average_1, average_2, number, mess_empire, mess_teor, max_minus, critical, LOG_FILE
        self.ui.earse.setEnabled(False)
        self.ui.start.setEnabled(True)
        self.ui.read.setEnabled(False)
        self.ui.show_1.setEnabled(False)
        self.ui.calculate.setEnabled(False)
        massive_input = []
        alpha = float()
        average_1 = float()
        average_2 = float()
        number = int()
        mess_teor = []  #
        mess_empire = []  #
        max_minus = float()
        critical = float()
        LOG_FILE = str()
        self.ui.a0.setText('...')
        self.ui.a1.setText('...')
        self.ui.a2.setText('...')
        self.ui.a3.setText('...')
        self.ui.a4.setText('...')
        self.ui.a5.setText('...')
        self.ui.a6.setText('...')
        self.ui.a7.setText('...')
        self.ui.draw_graph.setEnabled(False)
        self.ui.save.setEnabled(False)
        self.ui.openfile.setEnabled(False)
        self.ui.draw_graph.setEnabled(False)

    def start_b(self):
        self.ui.textBrowser.setText(
            "Старт программы!\n\nЗдесь будет выводиться полезная информация\n\nЧтобы начать, нужно расположить файл в "
            "папке с программой и ввести его название, или ввести полный путь к файлу")
        self.ui.start.setEnabled(False)
        self.ui.earse.setEnabled(True)
        self.ui.read.setEnabled(True)

    def read_b(self):
        global massive_input, LOG_FILE
        try:
            filename = str(self.ui.filename.text())
            file = open(filename, "r")
            massive_input = list(map(float, file.read().split()))
            massive_input.sort()
            LOG_FILE += 'Дана выборка:\n' + str(massive_input) + '\n'
            self.ui.textBrowser.setText("Файл успешно прочитан!")
            self.ui.read.setEnabled(False)
            self.ui.show_1.setEnabled(True)
            self.ui.calculate.setEnabled(True)
            file.close()
        except:
            self.ui.textBrowser.setText("Error!\n\nПроверьте правильность написания пути или имени файла\n\nБез "
                                        "указания полного пути файл должен находиться в папке с программой\n\nТакже "
                                        "возможна ошибка, если дробное число написано через запятую. Проставьте точки "
                                        "как разделитель целой и дробной частей")

    def show_1(self):
        global massive_input
        self.ui.textBrowser.setText("Входные данные:\n\n" + str(massive_input) + "\n\nОстальные действия доступны")

    def openfile(self):
        try:
            filename = str(self.ui.filename_2.text())
            path = os.getcwd() + "\\" + filename
            subprocess.Popen(('start', path), shell=True)
        except:
            self.ui.textBrowser.setText("Error!\n\nНе удалось открыть файл\n\nПроверьте правильность имени файла, "
                                        "а также присутствие файла в папке с программой")

    def savefile(self):
        global LOG_FILE
        filename = self.ui.filename_2.text()
        file = open(filename, 'w')
        file.writelines(LOG_FILE)
        file.close()
        self.ui.textBrowser.setText("LOG-file СОХРАНЕН!\n\nМожно продолжать пользоваться программой")
        self.ui.openfile.setEnabled(True)

    def draw_plots(self):
        global massive_input, mess_teor, mess_empire
        pylab.plot(massive_input, mess_teor)
        pylab.plot(massive_input, mess_empire)
        pylab.xlabel("Выборка")
        pylab.ylabel("Теоретическая и эмпирическая функции")
        pylab.show()
        self.ui.textBrowser.setText("Вывод графика функции...")

    def calculate_all(self):
        global massive_input, alpha
        try:
            alpha = str_to_float(self.ui.alpha.text())
            self.ui.textBrowser.setText('Всё заполнено верно! Производятся вычисления...')
            self.ui.calculate.setEnabled(False)
            begin_calc(self)
        except:
            self.ui.textBrowser.setText("Error!\n\nЭто точно число?")


# ---------------------------- Глобальные переменные -----------------------------
massive_input = []
alpha = float()
average_1 = float()
average_2 = float()
number = int()
mess_teor = []
mess_empire = []
max_minus = float()
critical = float()
LOG_FILE = str()


# ---------------------------- Глобальные переменные -----------------------------


def str_to_float(string):
    if string.count(',') >= 1:
        string = string.replace(',', '.')
    return round(float(string), 4)


def begin_calc(self):
    average_counter(self)  # Подсчитываем все "средние" значения
    teoretic_func()  # Подсчет теоретической функции
    empiric_func()  # Подсчет эмпирической функции
    max_minus_func(self)  # Подсчет максимальной разницы в функциях
    compare(self)


def average_counter(self):
    global number, average_1, average_2, LOG_FILE
    #  Среднее арифметическое

    number = len(massive_input)
    average_1 = round(sum(massive_input) / number, 4)
    self.ui.a0.setText(str(number))
    self.ui.a1.setText(str(average_1))
    LOG_FILE += "\nНайдем среднее арифметическое при размере выборки N = " + str(number) + " и оно равно = " + str(
        average_1)
    #  Среднее квадратическое отклонение
    summa_tmp = 0.0
    for i in range(number):
        summa_tmp += (average_1 - massive_input[i]) ** 2
    average_2 = round(((1 / (number - 1)) * summa_tmp) ** 0.5, 4)
    self.ui.a2.setText(str(average_2))
    LOG_FILE += "\n\nНайдем среднее квадратическое отклонение = " + str(average_2) + "\n\n"


def teoretic_func():
    global massive_input, number, mess_teor, average_1, average_2, LOG_FILE
    # Функция Лапласа табличная = stats.norm.cdf(x) - 0.5
    # Вычисление всех значений для теоретической функции
    for i in range(number):
        tmp = (massive_input[i] - average_1) / average_2
        mess_teor.append(round(stats.norm.cdf(tmp), 4))
    LOG_FILE += "Значения теоретической функции:\n\n" + str(mess_teor) + "\n\n"


def empiric_func():
    global number, mess_empire, LOG_FILE
    for k in range(number):
        mess_empire.append(round((k + 1) / number, 4))
    LOG_FILE += "Значения эмпирической функции: \n\n" + str(mess_empire) + "\n\n"


def max_minus_func(self):
    global mess_teor, mess_empire, number, max_minus, critical, LOG_FILE
    max_minus = -1.0
    for i in range(number):
        tmp = abs(mess_teor[i] - mess_empire[i])
        if max_minus <= tmp:
            max_minus = tmp
    max_minus *= number ** 0.5
    max_minus = round(max_minus, 4)
    self.ui.a3.setText(str(max_minus))
    # Вычисление критического значения статистики
    critical = round(((-math.log(alpha / 2)) / 2) ** 0.5, 4)
    self.ui.a4.setText(str(critical))
    LOG_FILE += "Найдем наибольшее отклонение = " + str(max_minus) + "\nЗатем вычисляем значение критерия: " + str(
        critical) + "\n\n"


def compare(self):
    global max_minus, critical, alpha, LOG_FILE
    if max_minus <= critical:
        self.ui.a5.setText("<=")
        self.ui.a6.setText(str(alpha))
        self.ui.a7.setText("соответствует")
        LOG_FILE += "Проведем исследование:\nТак как наибольшее отклонение МЕНЬШЕ критического значения статистики, " \
                    "то распределение можно считать нормальным на уровне значимости " + str(alpha) + "\n\nКОНЕЦ " \
                                                                                                     "LOG-ФАЙЛА "
    else:
        self.ui.a5.setText(">")
        self.ui.a6.setText(str(alpha))
        self.ui.a7.setText("не соответствует")
        LOG_FILE += "Проведем исследование:\nТак как наибольшее отклонение БОЛЬШЕ критического значения статистики, " \
                    "то распределение не является нормальным на уровне значимости " + str(alpha) + \
                    "\n\nКОНЕЦ LOG-ФАЙЛА "
    self.ui.draw_graph.setEnabled(True)
    self.ui.save.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
