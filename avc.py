import math
from tkinter import *  # библиотека интерфейса

root = Tk()  # создание окна
root.geometry("350x450")  # размер калькулятора
root.title("калькулятор")  # меняем название на калькулятор
root.config(background="silver")  # задаем цвет
expression = ""  # хранит общее расположенние в строке

result = StringVar()
expression_field = Entry(textvariable=result)
expression_field.grid(columnspan=4, ipadx=105)  # создаем поле ввода


def press_num(num):  # функция при нажатии на кнопку
    global expression  # получаем доступ к переменной вне функции и можем ее изменять
    expression += str(num)
    result.set(expression)


def equal_press():  # подсчитываем результат после равно
    try:  # что нужно попробывать сделать функции
        global expression
        total = str(eval(expression))  # подсчитываем и переводим в числовоем значение, храним результат expression
        result.set(total)  # устанавливаем значение total
        expression = total  # записывается новое значение или дописываем новое значение total
    except:
        result.set("error")  # если произошла какая то ошибка
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
    total = str(eval(expression) * multiplication // 1)  # переводим в строку
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


button1 = Button(text="1", height=3, width=8, command=lambda: press_num(1))  # задаем и увеличивыем кнопку
button1.grid(row=5, column=0)  # расположем кнопку

button2 = Button(text="2", height=3, width=8, command=lambda: press_num(2))  # задаем и увеличивыем кнопку
button2.grid(row=5, column=1)  # расположем кнопку

button3 = Button(text="3", height=3, width=8, command=lambda: press_num(3))  # задаем и увеличивыем кнопку
button3.grid(row=5, column=2)  # расположем кнопку

button4 = Button(text="4", height=3, width=8, command=lambda: press_num(4))  # задаем и увеличивыем кнопку
button4.grid(row=4, column=0)  # расположем кнопку

button5 = Button(text="5", height=3, width=8, command=lambda: press_num(5))  # задаем и увеличивыем кнопку
button5.grid(row=4, column=1)  # расположем кнопку

button6 = Button(text="6", height=3, width=8, command=lambda: press_num(6))  # задаем и увеличивыем кнопку
button6.grid(row=4, column=2)  # расположем кнопку

button7 = Button(text="7", height=3, width=8, command=lambda: press_num(7))  # задаем и увеличивыем кнопку
button7.grid(row=3, column=0)  # расположем кнопку

button8 = Button(text="8", height=3, width=8, command=lambda: press_num(8))  # задаем и увеличивыем кнопку
button8.grid(row=3, column=1)  # расположем кнопку

button9 = Button(text="9", height=3, width=8, command=lambda: press_num(9))  # задаем и увеличивыем кнопку
button9.grid(row=3, column=2)  # расположем кнопку

plus = Button(text="+", height=3, width=8, command=lambda: press_num("+"))  # задаем и увеличивыем кнопку
plus.grid(row=5, column=3)  # расположем кнопку

button0 = Button(text="0", height=3, width=12, command=lambda: press_num(0))  # задаем и увеличивыем кнопку
button0.grid(row=6, column=0)  # расположем кнопку

minus = Button(text="-", height=3, width=8, command=lambda: press_num("-"))  # задаем и увеличивыем кнопку
minus.grid(row=4, column=3)  # расположем кнопку

equal = Button(text="=", height=3, width=8, command=equal_press)  # задаем и увеличивыем кнопку
equal.grid(row=6, column=2)  # расположем кнопку

umn = Button(text="*", height=3, width=8, command=lambda: press_num("*"))  # задаем и увеличивыем кнопку
umn.grid(row=3, column=3)  # расположем кнопку

dele = Button(text="/", height=3, width=8, command=lambda: press_num("/"))  # задаем и увеличивыем кнопку
dele.grid(row=2, column=3)  # расположем кнопку

toch = Button(text=".", height=3, width=8, command=lambda: press_num("."))  # задаем и увеличивыем кнопку
toch.grid(row=6, column=1)  # расположем кнопку

"""rub_to_dol = Button(text="R/D", height=1, width=7, command=lambda: convertor(0.01))  # переводим из рубля в доллар
rub_to_dol.grid(row=7, column=0)  # расположем кнопку

dol_to_rub = Button(text="D/R", height=1, width=7, command=lambda: convertor(100))  # переводим из рубля в доллар
dol_to_rub.grid(row=7, column=1)  # расположем кнопку"""

coins = ["Rub to Dollar(Курс:100р-1 доллар)", "Dollar to Rub(Курс:100р-1 доллар)",
         "Rub to Euro(Курс:110р-1 евро)", "Euro to Rub(Курс:110р-1 евро)"]  # создаем массив с валютными парами
list_of_coins = Listbox(width=34, height=4, listvariable=coins)
# список монет и выберание нужной валютной пары, задаем ширину и высоту
list_of_coins.grid(row=7, column=0)

convert = Button(text="convert", height=3, width=8, command=convertor)  # подключаем кнопку конверт
convert.grid(row=8, column=0)
# добавляем кнопку по нажатию которой будет происходить перевод и будет проверка значения который хранится в списке

sqrt = Button(text="√", height=3, width=8, command=sqrt_exp)
sqrt.grid(row=2, column=2)  # расположем кнопку

sqr = Button(text="x^2", height=3, width=8, command=sqr_exp)
sqr.grid(row=2, column=1)  # расположем кнопку

reset = Button(text="C  ", height=3, width=8, command=reset)  # создаем кнопку сброса значения
reset.grid(row=2, column=0)  # расположем кнопку

root.mainloop()  # выводим калькулятор на экран
