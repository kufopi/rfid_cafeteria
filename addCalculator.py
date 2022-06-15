import time
from tkinter import *

root=Tk()

root.title('Add Calculator')
e = Entry(root, width=40, borderwidth=4)
e.grid(row = 0, column=0, columnspan=3, padx=5, pady=10)

dummy,val, sec=0,1,1

def butt(number):
    #e.delete(0,END)
    curr = e.get()
    e.delete(0, END)
    e.insert(0,str(curr)+str(number))

def plus():
    un_numbre= e.get()
    e.delete(0, END)
    global dummy
    dummy = int(dummy)+ int(un_numbre)
    #time.sleep(1)
    print(f'this is the summation {dummy}')




def equate():
    if math =='division':
        seconder = e.get()
        ans = num/float(seconder)
        e.delete(0,END)
        e.insert(0, ans)
    elif math =='multi':
        seconder = e.get()
        ans = num * int(seconder)
        e.delete(0, END)
        e.insert(0, ans)




def clear():
    e.delete(0, END)
    global  dummy
    dummy= 0


def divi():
    un_numbre = e.get()
    if int(un_numbre) != 0:
        global  num,mag
        global  math
        math= 'division'
        num = int(un_numbre)
        e.delete(0,END)


    else:
        e.insert(0,'Error committed!')


def mult():
    un_numbre = e.get()
    global math,num
    math = 'multi'
    num = int(un_numbre)
    e.delete(0, END)

btn0 = Button(root, text = '0', padx=48, pady=24,command=lambda : butt(0))
btn1 = Button(root, text = '1', padx=48, pady=24,command=lambda : butt(1))
btn2 = Button(root, text = '2', padx=48, pady=24,command=lambda : butt(2))
btn3 = Button(root, text = '3', padx=48, pady=24,command=lambda : butt(3))
btn4 = Button(root, text = '4', padx=48, pady=24,command=lambda : butt(4))
btn5 = Button(root, text = '5', padx=48, pady=24,command=lambda : butt(5))
btn6 = Button(root, text = '6', padx=48, pady=24,command=lambda : butt(6))
btn7 = Button(root, text = '7', padx=48, pady=24,command=lambda : butt(7))
btn8 = Button(root, text = '8', padx=48, pady=24,command=lambda : butt(8))
btn9 = Button(root, text = '9', padx=48, pady=24,command=lambda : butt(9))

btnplus = Button(root, text='+', padx=48, pady=24,command=plus)
btnequals = Button(root, text='=', padx=48, pady=24,command=equate,bg='white')
btnmult = Button(root, text='X', padx=48, pady=24,command=mult,bg='purple')
btndivi = Button(root, text='/', padx=48, pady=24,command=divi,bg='pink')
btnclear  = Button(root, text='CLEAR', padx=34, pady=24,command=clear, bg='turquoise')

btn1.grid(row=1, column=0)
btn2.grid(row=1, column=1)
btn3.grid(row=1, column=2)

btn4.grid(row=2, column=0)
btn5.grid(row=2, column=1)
btn6.grid(row=2, column=2)

btn7.grid(row=3, column=0)
btn8.grid(row=3, column=1)
btn9.grid(row=3, column=2)

btn0.grid(row=4, column=0)
btnplus.grid(row=4,column=1)
btnequals.grid(row=4,column=2)

btnclear.grid(row=5,column=0)
btnmult.grid(row=5,column=1)
btndivi.grid(row=5,column=2)



root.mainloop()
