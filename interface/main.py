from tkinter import *
from tkinter.ttk import Combobox
from tkinter import scrolledtext

from IdealPIDregulator import PReg
from PIDregulator import PIDregulator
from DeltaPIDRegulator import DeltaPIDRegulator


def startProgram():
    p = 10
    ti = 1
    td = 0.2
    dt = 0.1
    maxOutput = 0
    minOutput = 0
    maxOutputRampRate = 0

    try:
        p = float(KaFld.get())
        ti = float(TiFld.get())
        td = float(TdFld.get())
        minOutput = float(minFld.get())
        maxOutput = float(maxFld.get())
        maxOutputRampRate = float(proizvMaxFld.get())
    except:
        print("Ошибка при записи значений:")
        pass

    print(combo.get())
    typePID = combo.get()
    txt.delete(1.0, END)

    if typePID == "Идеальный ПИД-регулятор":
        ireg = PReg(p, ti, td)
        ireg.setOutputLimits(minOutput, maxOutput)
        ireg.setMaxOutputRampRate(maxOutputRampRate)
    if typePID == "Параллельный ПИД-регулятор":
        reg = PIDregulator(p, ti, td)
        reg.setOutputLimits(minOutput, maxOutput)
        reg.setMaxOutputRampRate(maxOutputRampRate)
    if typePID == "Рекуррентный ПИД-регулятор":
        dreg = DeltaPIDRegulator(p, ti, td, dt)
        dreg.setOutputLimits(minOutput, maxOutput)
        dreg.setMaxOutputRampRate(maxOutputRampRate)

    k = 1.0
    up = 0
    r = 0
    y = 0
    y1 = 0
    u = 0
    T = 1.0

    print("Target\tOutput\tControl\tError\n")
    txt.insert(INSERT, "Target\tOutput\tControl\tError\n")

    for i in range(100):
        if i == 20:
            r = 1
        if typePID == "Идеальный ПИД-регулятор":
            u = ireg.getOutput(y1, r)
        if typePID == "Параллельный ПИД-регулятор":
            u = reg.getOutput(y1, r)
        if typePID == "Рекуррентный ПИД-регулятор":
            u = up + dreg.getOutput(y1, r)
            up = u

        y1 = k * dt / T * u + (T - dt) / T * y
        y = y1
        print("%3.2f\t%3.2f\t%3.2f\t%3.2f" % (r, y1, u, (r - y1)))
        str1 = f"%3.2f\t%3.2f\t%3.2f\t%3.2f\n" % (r, y1, u, (r - y1))
        txt.insert(INSERT, str1)


def exitProgram():
    exit()


root = Tk()
root.title('ПИД-регулятор')
root.geometry('700x780')
root.resizable(width=False, height=False)

KaLbl = Label(root, text="Ka:", font=("Arial Bold", 18))
KaLbl.grid(column=0, row=0)

KaFld = Entry(root, width=20)
KaFld.insert(0, "10")
KaFld.grid(column=1, row=0)

TiLbl = Label(root, text="Ti:", font=("Arial Bold", 18))
TiLbl.grid(column=0, row=1)

TiFld = Entry(root, width=20)
TiFld.insert(0, "1")
TiFld.grid(column=1, row=1)

combo = Combobox(root)
combo['values'] = ("Идеальный ПИД-регулятор", "Параллельный ПИД-регулятор", "Рекуррентный ПИД-регулятор")
combo.current(0)
combo.grid(column=2, row=1)

TdLbl = Label(root, text="Td:", font=("Arial Bold", 18))
TdLbl.grid(column=0, row=2)

TdFld = Entry(root, width=20)
TdFld.insert(0, "0.2")
TdFld.grid(column=1, row=2)

typeLbl = Label(root, text="Вид регулятора:", font=("Arial Bold", 18))
typeLbl.grid(column=2, row=0)

limitsLbl = Label(root, text="Ограничения на управления:", font=("Arial Bold", 18))
limitsLbl.grid(column=0, row=3)

minLbl = Label(root, text="min:", font=("Arial Bold", 18))
minLbl.grid(column=0, row=4)

minFld = Entry(root, width=10)
minFld.insert(0, "-1.8")
minFld.grid(column=1, row=4)

maxLbl = Label(root, text="max:", font=("Arial Bold", 18))
maxLbl.grid(column=0, row=5)

maxFld = Entry(root, width=10)
maxFld.insert(0, "1.8")
maxFld.grid(column=1, row=5)

proizvLbl = Label(root, text="Ограничение на производную:", font=("Arial Bold", 18))
proizvLbl.grid(column=0, row=6)

proizvMaxLbl = Label(root, text="max:", font=("Arial Bold", 18))
proizvMaxLbl.grid(column=0, row=7)

proizvMaxFld = Entry(root, width=10, )
proizvMaxFld.insert(0, "1")
proizvMaxFld.grid(column=1, row=7)

txt = scrolledtext.ScrolledText(root, width=40, height=32, font=("Arial Bold", 10))
txt.grid(column=0, row=8)

startBtn = Button(root, text="Старт", font=("Arial Bold", 18), command=startProgram)
startBtn.grid(column=1, row=8)

exitBtn = Button(root, text="Выход", font=("Arial Bold", 18), command=exitProgram)
exitBtn.grid(column=2, row=8)

root.mainloop()
