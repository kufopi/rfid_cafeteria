import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime,date
from PIL import Image, ImageTk


root = Tk()
root.title('Cafeteria Management Service')
root.geometry('700x400')
root.iconbitmap('favicon.ico')
root.configure(bg='#1e84e3')

conn = sqlite3.connect('edet.db')
# cursor
c = conn.cursor()


def test(event):
    conn = sqlite3.connect('edet.db')
    # cursor SELECT "Record exists" where EXISTS(SELECT 1 FROM CAFE WHERE matric = 155 AND meal='Breakfast' AND date
    # ='16/03/2022')
    c = conn.cursor()
    me = test_entry.get()
    if test_entry.get() == '':
        messagebox.showerror(title='Empty Textbox', message='Sorry Student Matric cannot be EMPTY')

    c.execute(" SELECT *, oid from students WHERE matric=" + test_entry.get())
    records = c.fetchone()
    if records is None:
        messagebox.showerror(title='Not Registered', message='Sorry this Matric Number isn\'t registered \n'
                                                             'Contact Mr Edet of the ICT Unit')
        test_entry.delete(0, END)
    else:

        print(records)

        result = f'{records[2].upper()} {records[1]}'
        photo = ImageTk.PhotoImage(Image.open(records[6]).resize((120, 120), Image.ANTIALIAS))

        print(result)
        print(photo)
        student_label = Label(image=photo)
        student_label.image = photo
        student_label.grid(row=9, column=1)
        test_label = Label(root, text=result)
        test_label.grid(row=9, column=0)
        test_entry.delete(0, END)
        root.after(2500, lambda: test_label.destroy())
        root.after(2500, lambda: student_label.destroy())
        now = datetime.now()
        print('now =', now)
        dt_string = now.strftime("%d/%m/%Y")
        timerec = now.strftime("%H:%M:%S")
        print(me)

        # c.execute(f"SELECT 'You have been served' where EXISTS(SELECT 1 FROM CAFE WHERE matric ={me} and meal='{
        # meal.get()}' and date ='{dt_string}')")
        queryy = "SELECT 'You have been served' where EXISTS(SELECT 1 FROM CAFE WHERE matric =? and meal=? and date =?)"
        params = (me, meal.get(), date.today())
        c.execute(queryy, params)
        opinion = c.fetchone()

        print(f'this is the opinion--- {opinion}')
        if opinion is None:
            c.execute("INSERT INTO cafe VALUES( :matric, :firstname, :surname, :meal, :date, :time)",
                      {
                          'matric': me,
                          'firstname': records[1],
                          'surname': records[2],
                          'meal': meal.get(),
                          'date': date.today(),
                          'time': timerec
                      }
                      )
        else:
            messagebox.showerror(title='Service Rendered', message=f'Sorry! This Student has been served {meal.get()},'
                                                                   f' already today')

        conn.commit()
        # close conn
        conn.close()


test_entry = Entry(root, width=38, font='Georgia 16')
test_entry.bind('<Return>', test)
test_entry.grid(row=8, column=1, pady=10)
matric_label = Label(root, text='Student Matric:')
matric_label.grid(row=8, column=0, padx=20)

quit_butt = Button(root, text="Exit Program", command=root.destroy, bg='#a05714', font='Tahoma')
quit_butt.grid(row=12, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

meal = StringVar(value='Lunch')
meal_bbutt = Radiobutton(root, text='Breakfast', variable=meal, value='Breakfast', font='Gautami 12 bold')
meal_lbutt = Radiobutton(root, text='Lunch', variable=meal, value='Lunch', font='Adobe 12 bold')
meal_sbutt = Radiobutton(root, text='Supper', variable=meal, value='Supper', font='Eccentric 12 bold')
meal_spebutt = Radiobutton(root, text='Special Meal', variable=meal, value='Special', font='Gulim 12 bold')

meal_bbutt.grid(row=13, column=0, ipadx=25)
meal_lbutt.grid(row=14, column=0, ipadx=50, columnspan=2)
meal_sbutt.grid(row=13, column=1, sticky=E, ipadx=30)
meal_spebutt.grid(row=15, column=0, ipadx=25)

# commit changes
conn.commit()
# close conn
conn.close()

root.mainloop()
