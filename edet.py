import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
from tkcalendar import Calendar
import pdfkit as pdf
import pandas as pd
import os
from fpdf import FPDF
import csv
import webbrowser
from PIL import Image,ImageTk
from tkinter import filedialog


root = Tk()
root.title('Cafeteria Management')
root.geometry('800x800')
root.iconbitmap('favicon.ico')
root.configure(bg='#145DA0')

# create a database
conn = sqlite3.connect('edet.db')
# cursor
c = conn.cursor()


#create ttables
# c.execute(""" CREATE TABLE students(
#         matric integer NOT NULL PRIMARY KEY,
#         firstname text,
#         surname text,
#         dept text,
#         gender text,
#         hostel text,
#         pic text
#
# )
# """)
#
# c.execute(""" CREATE TABLE cafe(
#         matric integer,
#         firstname text,
#         surname text,
#         meal text,
#         date DATE,
#         time text
#
# )""")

def browse():
    filename = filedialog.askopenfilename(initialdir='C:/Users/NHS_CHRIS013/Pictures', title='Select a picture', filetypes=(("png files","*.png"),("jpg files","*.jpg")))
    pic_entry.insert(END,filename)

def filterdate():
    info = sqlite3.connect('edet.db')
    d1 = str(cal1.get_date())
    d2 = str(cal2.get_date())

    boss = f'SELECT * FROM cafe WHERE date between "{d1}" AND "{d2}"'

    df = pd.read_sql_query(boss, info)
    newdf = df.copy()
    df.to_html("df.html", classes='table table-striped text-center', justify='center')
    datafr = pd.DataFrame({
        'Matric': newdf.matric,
        'Firstname': newdf.firstname,
        'Surname': newdf.surname,
        'Meal': newdf.meal,
        'Date': newdf.date,
        'Time': newdf.time
    })
    datafr.to_csv('data.csv')

    # attempting to use FPDF to create a better pdf file
    with open('data.csv', newline='') as f:
        reader = csv.reader(f)

        sdf = FPDF()
        sdf.add_page()
        page_width = sdf.w - 2 * sdf.l_margin

        sdf.set_font('Helvetica', 'B', 14.0)
        sdf.image('au.jpg', 95, 0, w=20, h=18)

        sdf.cell(page_width, 20, 'Cafeteria Data', align='C')
        sdf.ln(8)
        sdf.set_font('Helvetica', 'i', 10.0)
        sdf.cell(page_width, 20, f'From - {d1} To - {d2}', align='C')

        sdf.ln(12)

        sdf.set_font('Courier', 'i', 12)
        col_width = page_width / 7
        sdf.ln(3)

        th = sdf.font_size

        for row in reader:
            print(row)
            sdf.cell(col_width, th, str(row[0]), border=1)
            sdf.cell(col_width, th, row[1], border=1)
            sdf.cell(col_width, th, row[2], border=1)
            sdf.cell(col_width, th, row[3], border=1)
            sdf.cell(col_width, th, row[4], border=1)
            sdf.cell(col_width, th, row[5], border=1)
            sdf.cell(col_width, th, row[6], border=1)
            sdf.ln(th)

        sdf.ln(10)
        sdf.set_font('Times', '', 10.0)
        sdf.cell(page_width, 0.0, '- End of report -', align='C')
        sdf.ln(8)
        sdf.cell(page_width, 0.0, f'- Produced on {datetime.today().strftime("%B %d, %Y")} -', align='C')
        sdf.ln(8)
        sdf.cell(page_width, 0.0, f'- Powered by Kufopo -', align='C')
        sdf.output('C:/Users/NHS_CHRIS013/Documents/Cafeteria.pdf', 'F')
        webbrowser.open('C:/Users/NHS_CHRIS013/Documents/Cafeteria.pdf')

    options = {
        'minimum-font-size': "30",
    }
    filname = 'edetdata.pdf'
    load = "C:/Users/NHS_CHRIS013/Documents"
    pdf.from_file("df.html", os.path.join(load, filname), options=options)
    webbrowser.open(os.path.join(load, filname))
    info.commit()
    info.close()
    messagebox.showinfo('Pdf file created. ', 'Check The Document Folder.\nor wait for your browser to open it')


def register():
    top = Toplevel()
    top.title('Showing Records')
    top.geometry('700x200')
    top.iconbitmap('favicon.ico')

    main_frame = Frame(top)
    main_frame.pack(fill=BOTH, expand=1)

    my_canvas = Canvas(main_frame, bg='#D0F0C0')
    my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

    second_frame = Frame(my_canvas)
    my_canvas.create_window((0, 0), window=second_frame, anchor='nw')

    info = sqlite3.connect('edet.db')
    cinfo = info.cursor()
    cinfo.execute("SELECT * from cafe ORDER BY date")
    records = cinfo.fetchall()
    result = ''
    for rec in records:
        result += f'{rec[0]} - {rec[2].upper()} {rec[1]} was served {rec[3]} on {rec[4]} \n'
    notice_label = Label(second_frame, text=result, bg='#D0F0C0', font='Century 14')
    notice_label.pack()

    info.commit()
    info.close()


def query():
    conn = sqlite3.connect('edet.db')
    # cursor
    c = conn.cursor()

    c.execute(" SELECT *, oid from students")
    records = c.fetchall()
    result = ''
    for rec in records:
        result += f'{rec[0]} belongs to {rec[2].upper()} {rec[1]} Dept:{rec[3]} \n'

    board_label = Label(root, text=result)
    board_label.grid(row=8, column=0, columnspan=2)

    conn.commit()
    # close conn
    conn.close()


def test(event):
    conn = sqlite3.connect('edet.db')
    # cursor
    #SELECT "Record exists" where EXISTS(SELECT 1 FROM CAFE WHERE matric = 155 AND meal='Breakfast' AND date ='16/03/2022')
    c = conn.cursor()
    me = test_entry.get()
    if test_entry.get() == '':
        messagebox.showerror(title='Empty Textbox', message='Sorry Student Matric cannot be EMPTY')

    c.execute(" SELECT *, oid from students WHERE matric=" + test_entry.get())
    records = c.fetchone()
    if records is None:
        messagebox.showerror(title='Not Registered', message='Sorry this Matric Number isn\'t registered \n'
                                                             'Contact Mr Edet of the ICT Unit')
        test_entry.delete(0,END)
    else:

        print(records)

        result = f'{records[2].upper()} {records[1]}'
        photo = ImageTk.PhotoImage(Image.open(records[6]).resize((100,120), Image.ANTIALIAS))


        print(result)
        print(photo)
        student_label = Label(image=photo)
        student_label.image=photo
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

        #c.execute(f"SELECT 'You have been served' where EXISTS(SELECT 1 FROM CAFE WHERE matric ={me} and meal='{meal.get()}' and date ='{dt_string}')")  THE DATE FORMAT HAS CHAGED OOH
        queryy = "SELECT 'You have been served' where EXISTS(SELECT 1 FROM CAFE WHERE matric =? and meal=? and date =?)"
        params = (me,meal.get(),dt_string)
        c.execute(queryy,params)
        opinion=c.fetchone()

        print(f'this is the opinion--- {opinion}')
        if opinion is None:
            c.execute("INSERT INTO cafe VALUES( :matric, :firstname, :surname, :meal, :date, :time)",
                      {
                          'matric': me,
                          'firstname': records[1],
                          'surname': records[2],
                          'meal': meal.get(),
                          'date': dt_string,
                          'time': timerec
                      }
                      )
        else:
            messagebox.showerror(title='Service Rendered', message=f'Sorry! This Student has been served {meal.get()} already today')

        conn.commit()
        # close conn
        conn.close()


def submit():
    conn = sqlite3.connect('edet.db')
    # cursor
    c = conn.cursor()

    # insert into table student
    c.execute("INSERT INTO students VALUES(:matric, :fname, :sname, :dept, :gender, :hostel, :pic)",
              {
                  'matric': matric_entry.get(),
                  'fname': fname_entry.get(),
                  'sname': sname_entry.get(),
                  'dept': choose.get(),
                  'gender': gender_entry.get(),
                  'hostel': hostel_entry.get(),
                  'pic':pic_entry.get()
              }
              )

    conn.commit()
    # close conn
    conn.close()
    matric_entry.delete(0, END)
    fname_entry.delete(0, END)
    sname_entry.delete(0, END)
    gender_entry.delete(0, END)
    hostel_entry.delete(0, END)
    pic_entry.delete(0,END)


depart = ['Mass Comm', 'Anatomy', 'Biochemistry', 'Civil Eng', 'History', 'Law']

matric_entry = Entry(root, width=40, font='Georgia 14')
matric_label = Label(root, text="Matric: ")
matric_label.grid(row=0, column=0, padx=20, pady=20)

matric_entry.grid(row=0, column=1, padx=20, pady=20)

fname_entry = Entry(root, width=40, font='Georgia 14')
fname_label = Label(root, text="First Name: ")
fname_label.config(bg='#7FFF00')
fname_label.grid(row=1, column=0, padx=20)
fname_entry.grid(row=1, column=1, padx=20)

sname_entry = Entry(root, width=40, font='Georgia 14')
sname_label = Label(root, text="Surname: ")
sname_label.grid(row=2, column=0, padx=20)
sname_entry.grid(row=2, column=1, padx=20)

choose = StringVar()
choose.set(depart[2])
dept_entry = OptionMenu(root, choose, *depart)  # remembr to use choose.get() to grab
dept_entry.configure(bg='#D8BFD8')
dept_label = Label(root, text="Dept: ")
dept_label.grid(row=3, column=0, padx=20)
dept_entry.grid(row=3, column=1, padx=20)

gender_entry = Entry(root, width=40)
gender_label = Label(root, text="Gender: ")
gender_label.grid(row=4, column=0, padx=20)
gender_entry.grid(row=4, column=1, padx=20)

hostel_entry = Entry(root, width=40)
hostel_label = Label(root, text="Hostel: ")
hostel_label.grid(row=5, column=0, padx=20)
hostel_entry.grid(row=5, column=1, padx=20)

pic_entry = Entry(root, width=40, font='Ubuntu 12')
pic_butt = Button(root,text='Browse', command=browse,font='Ubuntu 10',bg='#d9dddc')
pic_butt.grid(row=6, column=0, padx=20)
pic_entry.grid(row=6, column=1, padx=20)

# record button
rec_butt = Button(root, text="Submit record", command=submit, bg='#F9E29C', font='Mistral')
rec_butt.grid(row=7, column=0, columnspan=2, padx=5, pady=5, ipadx=80)

# query_butt = Button(root, text="Query Database", command=query, bg='#73C2FB', font='DotumChe')
# query_butt.grid(row=7, column=0, columnspan=2, padx=15, pady=10, ipadx=50)

test_entry = Entry(root, width=38, font='Georgia 16')
test_entry.bind('<Return>', test)
test_entry.grid(row=8, column=1, pady=10)
matric_label = Label(root, text='Student Matric:')
matric_label.grid(row=8, column=0, padx=20)



quit_butt = Button(root, text="Exit Program", command=root.destroy, bg='#FA8072', font='Tahoma')
quit_butt.grid(row=12, column=0, columnspan=2, padx=10, pady=10, ipadx=50)

meal = StringVar(value='Lunch')
meal_bbutt = Radiobutton(root, text='Breakfast', variable=meal, value='Breakfast', font='Gautami 12 bold')
meal_lbutt = Radiobutton(root, text='Lunch', variable=meal, value='Lunch', font='Adobe 12 bold')
meal_sbutt = Radiobutton(root, text='Supper', variable=meal, value='Supper', font='Eccentric 12 bold')

meal_bbutt.grid(row=13, column=0)
meal_lbutt.grid(row=14, column=0,ipadx=50, columnspan=2)
meal_sbutt.grid(row=13, column=1, sticky=E, padx=50)

data_butt = Button(root, text='Show records', bg='#c5e384', command=register)
data_butt.grid(row=15, column=0, columnspan=2, padx=15, pady=10, ipadx=50)

data_butt = Button(root, text='date filter', bg='#c5e384', command=filterdate)
data_butt.grid(row=16, column=0, columnspan=2, padx=15, pady=10, ipadx=50)

cal1 = Calendar(root, selectmode='day', year=2022, month=3, day=2, locale='en_UK')
cal2 = Calendar(root, selectmode='day', year=2022, month=3, day=10, locale='en_UK')

startLbl = Label(root, text='Start Date', font='Gulim')
stopLbl = Label(root, text='End Date', font='Arial')

startLbl.grid(row=17, column=0, sticky=W)
stopLbl.grid(row=17, column=1, sticky=E)

cal1.grid(row=18, column=0, padx=5, pady=10, sticky=E)
cal2.grid(row=18, column=1, sticky=E)

# commit changes
conn.commit()
# close conn
conn.close()

root.mainloop()
