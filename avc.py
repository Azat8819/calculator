import math
import os
import threading
import time
import tkinter
import tkinter.font as font
import wave
from tkinter import *  # библиотека интерфейса

import pyaudio


class VoiceRecorder():

    def __init__(self):
        self.root = tkinter.Tk()
        self.button = tkinter.Button(
            text="🎤",
            height=3, width=8, # задаем и увеличивыем кнопку
            command=self.click_handler
        )
        self.button.pack()
        self.label = tkinter.Label(text="00:00:00")
        self.label.pack()
        self.recording = False
        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
        else:
            self.recording = True
            threading.Thread(target=self.record).start()

    def record(self, i=None):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024
            # input_device_index =
        )

        frames = []
        start = time.time()

        while self.recording:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

            passed = time.time() - start
            secs = passed % 60
            mins = passed // 60
            hours = mins // 60
            self.label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        exists = True
        while exists:
            if os.path.exists(f"recordinf{i}.wav"):
                i += 1
            else:
                exists = False

        sound_file = wave.open(f"recording{i}.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()


VoiceRecorder()

root = Tk()  # создание окна
root.geometry("265x450")  # размер калькулятора
root.title("калькулятор")  # меняем название на калькулятор
root.config(background="silver")  # задаем цвет
expression = ""  # хранит общее расположенние в строке
root.resizable(False, False)  # не можем растягивать окно

result = StringVar()
result.set("0")
expression_field = Entry(root, textvariable=result, font=("Verdana", 15,), bd=12,
                         insertwidth=4, justify=RIGHT)  # интерфейс поля ввода
expression_field.pack()  # создаем поле ввода

frame = Frame(
    root,
    background="silver"
)
frame.pack(expand=True)


def press_num(num):  # функция при нажатии на кнопку
    global expression  # получаем доступ к переменной вне функции и можем ее изменять
    expression += str(num)
    result.set(expression)


def equal_press():  # подсчитываем результат после равно
    try:  # что нужно попробывать сделать функции
        global expression
        total = (eval(expression))  # подсчитываем и переводим в числовоем значение, храним результат expression
        if total % 1 == 0:
            total = int(total)  # убираем 5 == 5.0
        result.set(str(total))  # устанавливаем значение total
        expression = str(total)  # записывается новое значение или дописываем новое значение total
    except:
        result.set("Ошибка")  # если произошла какая то ошибка
        expression = ""  # обнуляем значение expression


def convertor():  # вывести значение которое выбрано пользователем
    actual_coin = list_of_coins.get(list_of_coins.curselection())  # храним значение которое выбрано В Данный момент
    multiplication = 1
    if actual_coin == coins[0]:
        multiplication = 0.01
    elif actual_coin == coins[1]:
        multiplication = 100
    elif actual_coin == coins[2]:
        multiplication = 0.009091
    elif actual_coin == coins[3]:
        multiplication = 110
    global expression
    total = str(eval(expression) * multiplication)  # переводим в строку
    result.set(total)  # устанавливаем данный результат
    expression = total


def sqrt_exp():
    global expression
    total = str(math.sqrt(eval(expression)))  # считаем корень
    result.set(total)  # устанавливаем значение total
    expression = total  # записывается новое значение или дописываем новое значение total


def sqr_exp():
    global expression
    total = str(eval(expression) * eval(expression))  # считаем квадрат
    result.set(total)  # устанавливаем значение total
    expression = total  # записывается новое значение или дописываем новое значение total


def reset():
    global expression
    total = ""
    result.set(total)  # устанавливаем значение total
    expression = total  # записывается новое значение или дописываем новое значение total


def percent1():
    global expression
    total = str(eval(expression) / 100)  # считаем  %
    result.set(total)  # устанавливаем значение total
    expression = total  # записывается новое значение или дописываем новое значение total


myFont = font.Font(family='Helvetica', size=10, weight='bold')

button1 = Button(
    frame,
    text="1", height=3, width=8, command=lambda: press_num(1))  # задаем и увеличивыем кнопку
button1.grid(row=5, column=0, padx=0, pady=0, ipadx=0, ipady=0)  # расположем кнопку

button2 = Button(
    frame,
    text="2", height=3, width=8, command=lambda: press_num(2))  # задаем и увеличивыем кнопку
button2.grid(row=5, column=1)  # расположем кнопку

button3 = Button(
    frame,
    text="3", height=3, width=8, command=lambda: press_num(3))  # задаем и увеличивыем кнопку
button3.grid(row=5, column=2)  # расположем кнопку

button4 = Button(
    frame,
    text="4", height=3, width=8, command=lambda: press_num(4))  # задаем и увеличивыем кнопку
button4.grid(row=4, column=0)  # расположем кнопку

button5 = Button(
    frame,
    text="5", height=3, width=8, command=lambda: press_num(5))  # задаем и увеличивыем кнопку
button5.grid(row=4, column=1)  # расположем кнопку

button6 = Button(
    frame,
    text="6", height=3, width=8, command=lambda: press_num(6))  # задаем и увеличивыем кнопку
button6.grid(row=4, column=2)  # расположем кнопку

button7 = Button(
    frame,
    text="7", height=3, width=8, command=lambda: press_num(7))  # задаем и увеличивыем кнопку
button7.grid(row=3, column=0)  # расположем кнопку

button8 = Button(
    frame,
    text="8", height=3, width=8, command=lambda: press_num(8))  # задаем и увеличивыем кнопку
button8.grid(row=3, column=1)  # расположем кнопку

button9 = Button(
    frame,
    text="9", height=3, width=8, command=lambda: press_num(9))  # задаем и увеличивыем кнопку
button9.grid(row=3, column=2)  # расположем кнопку

plus = Button(
    frame,
    text="+", height=3, width=8, bg="silver", command=lambda: press_num("+"))  # задаем и увеличивыем кнопку
plus.grid(row=5, column=3)  # расположем кнопку

button0 = Button(
    frame,
    text="0", height=3, width=8, command=lambda: press_num(0))  # задаем и увеличивыем кнопку
button0.grid(row=6, column=0)  # расположем кнопку

minus = Button(
    frame,
    text="—", height=3, width=8, bg="silver", command=lambda: press_num("-"))  # задаем и увеличивыем кнопку
minus.grid(row=4, column=3)  # расположем кнопку

equal = Button(
    frame,
    text="=", height=3, width=8, command=equal_press, bg="orange", fg="black")  # задаем и увеличивыем кнопку
equal.grid(row=6, column=2)  # расположем кнопку

multiply = Button(
    frame,
    text="×", height=3, width=8, bg="silver", command=lambda: press_num("*"))  # задаем и увеличивыем кнопку
multiply.grid(row=3, column=3)  # расположем кнопку

dele = Button(
    frame,
    text="÷", height=3, width=8, bg="silver", command=lambda: press_num("÷"))  # задаем и увеличивыем кнопку
dele.grid(row=2, column=3)  # расположем кнопку

toch = Button(
    frame,
    text=".", height=3, width=8, command=lambda: press_num("."))  # задаем и увеличивыем кнопку
toch.grid(row=6, column=1)  # расположем кнопку

coins = ["Rub to Dollar(Курс:100 рублей - 1 доллар)", "Dollar to Rub(Курс:100 рублей - 1 доллар)",
         "Rub to Euro(Курс:110 рублей - 1 евро)",
         "Euro to Rub(Курс:110 рублей - 1 евро)"]  # создаем массив с валютными парами
coins_variable = Variable(value=coins)  # элементы для списка конвертации
list_of_coins = Listbox(width=43, height=4, listvariable=coins_variable)  # создание списка конвертации
# список монет и выберание нужной валютной пары, задаем ширину и высоту
list_of_coins.pack()

convert = Button(text="convert", height=3, width=8, command=convertor)  # подключаем кнопку конверт
convert.pack()
# добавляем кнопку по нажатию которой будет происходить перевод и будет проверка значения который хранится в списке

sqrt = Button(
    frame,
    text="√", height=3, width=8, bg="silver", command=sqrt_exp)
sqrt.grid(row=2, column=2)  # расположем кнопку

sqr = Button(
    frame,
    text="Х²", height=3, width=8, bg="silver", command=sqr_exp)
sqr.grid(row=2, column=1)  # расположем кнопку

reset = Button(
    frame,
    text="C  ", height=3, width=8, bg="silver", command=reset)  # создаем кнопку сброса значения
reset.grid(row=2, column=0)  # расположем кнопку

percent = Button(
    frame,
    text="%", height=3, width=8, bg="silver", command=percent1)  # задаем и увеличивыем кнопку
percent.grid(row=6, column=3)  # расположем кнопку

root.mainloop()  # выводим калькулятор на экран
