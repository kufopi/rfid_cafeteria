import sqlite3
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
import pandas as pd
from fpdf import FPDF
import csv
import webbrowser
from tkinter import filedialog
from time import sleep

root = Tk()
root.title('Cafeteria Management Report')
root.geometry('600x400')
root.iconbitmap('favicon.ico')
root.configure(bg='#fbe7c6')

# create a database
conn = sqlite3.connect('edet.db')
# cursor
c = conn.cursor()


def studrec():
    conn = sqlite3.connect('edet.db')
    c = conn.cursor()
    record_identity = identity.get()
    if record_identity == '':
        messagebox.showerror('Empty Student ID','Please enter a valid student ID')
    else:
        d1 = cal1.get_date()
        d2 = cal2.get_date()
        d11 = datetime.strptime(d1, "%d/%m/%Y")
        d111 = d11.strftime("%Y-%m-%d")
        d22 = datetime.strptime(d2, "%d/%m/%Y")
        d222 = d22.strftime("%Y-%m-%d")
        c.execute("SELECT firstname, surname FROM students WHERE matric=" + record_identity)
        name_record = c.fetchone()

        boss = f"SELECT * FROM cafe WHERE matric={record_identity} AND date >= '{d111}' AND date <= '{d222}'"

        df = pd.read_sql_query(boss, conn)
        newdf = df.copy()
        datafr = pd.DataFrame({
            'Matric': newdf.matric,
            'Firstname': newdf.firstname,
            'Surname': newdf.surname,
            'Meal': newdf.meal,
            'Date': newdf.date,
            'Time': newdf.time
        })
        datafr.index = datafr.index + 1
        datafr.to_csv('studentcafe.csv')

        # attempting to use FPDF to create a better pdf file
        with open('studentcafe.csv', newline='') as f:
            reader = csv.reader(f)

            sdf = FPDF()
            sdf.add_page()
            page_width = sdf.w - 2 * sdf.l_margin

            sdf.set_font('Helvetica', 'B', 14.0)
            sdf.image('au.jpg', 95, 0, w=20, h=18)

            sdf.cell(page_width, 20, f"{name_record[1]} {name_record[0]}'s Cafe Data", align='C')
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
            sdf.output(f"C:/Users/NHS_CHRIS013/Documents/{name_record[0]}_{name_record[1]}'s Data.pdf", 'F')
            webbrowser.open(f"C:/Users/NHS_CHRIS013/Documents/{name_record[0]}_{name_record[1]}'s Data.pdf")

    conn.commit()
    conn.close()



def melo():
    conn = sqlite3.connect('edet.db')
    c = conn.cursor()
    record_identity = identity.get()
    if record_identity == '':
        pass
    else:
        d1 = cal1.get_date()
        d2 = cal2.get_date()
        d11 = datetime.strptime(d1, "%d/%m/%Y")
        d111 = d11.strftime("%Y-%m-%d")
        d22 = datetime.strptime(d2, "%d/%m/%Y")
        d222 = d22.strftime("%Y-%m-%d")

        que = "SELECT COUNT(*) FROM cafe WHERE matric=? AND date >=? AND date <=?"
        params = (record_identity, d111, d222)
        c.execute(que, params)
        record_count = c.fetchone()

        countmessage = Label(root, text=f'This person has been served {record_count[0]} time(s) between {d1} and {d2}',
                             font='Gulim 11 bold')
        countmessage.grid(row=21, column=0, columnspan=2)
        root.after(3000, lambda: countmessage.destroy())
    conn.commit()
    conn.close()


def updat():
    conn = sqlite3.connect('edet.db')
    c = conn.cursor()
    record_identity = identity.get()

    c.execute(""" UPDATE students SET
    matric =:matric,
    firstname= :firstname,
    surname = :surname,
    dept = :dept,
    gender =:gender,
    hostel = :hostel,
    pic = :pic
    
    WHERE matric = :matrix
    """,
              {'matric': matric_entry.get(),
               'firstname': fname_entry.get(),
               'surname': sname_entry.get(),
               'dept': choose.get(),
               'gender': gender_choice.get(),
               'hostel': hostel_choice.get(),
               'pic': pic_entry.get(),
               'matrix': record_identity
               })

    conn.commit()
    conn.close()
    sleep(2)
    editor.destroy()


def edit():
    global editor
    editor = Tk()
    editor.title('Update A Record')
    editor.iconbitmap('favicon.ico')
    editor.geometry("400x600")

    depart = ['Mass Comm', 'Anatomy', 'Biochemistry', 'Civil Eng', 'History', 'Law', 'Biz Admin', 'Pub Health',
              'Nursing']
    gender = ['F', 'M']
    hostel = ['OBO', 'Alice', 'Iyalode', 'Serubawon', 'Boys', 'Girls']

    conn = sqlite3.connect('edet.db')
    c = conn.cursor()
    record_identity = identity.get()
    if record_identity == '':
        messagebox.showerror('Empty Student ID','Please enter a valid student ID')
    else:
        c.execute("SELECT * FROM students WHERE matric =" + record_identity)
        record_values = c.fetchall()

        def browse():
            filename = filedialog.askopenfilename(initialdir='C:/Users/NHS_CHRIS013/Pictures', title='Select a picture',
                                                  filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
            pic_entry.insert(END, filename)

        # global Variable so they can be accessed by another method
        global matric_entry, fname_entry
        global sname_entry, dept_entry
        global gender_entry, hostel_entry
        global pic_entry, choose, gender_choice, hostel_choice

        matric_entry = Entry(editor, width=20, font='Georgia 12')
        matric_label = Label(editor, text="Matric: ")
        matric_label.grid(row=0, column=0, padx=10, pady=20)
        matric_entry.grid(row=0, column=1, padx=10, pady=20)

        fname_entry = Entry(editor, width=20, font='Georgia 12')
        fname_label = Label(editor, text="First Name: ")
        fname_label.grid(row=1, column=0, padx=10)
        fname_entry.grid(row=1, column=1, padx=10)

        sname_entry = Entry(editor, width=20, font='Georgia 12')
        sname_label = Label(editor, text="Surname: ")
        sname_label.grid(row=2, column=0, padx=10)
        sname_entry.grid(row=2, column=1, padx=10)

        choose = StringVar(editor)
        choose.set(depart[2])
        dept_entry = OptionMenu(editor, choose, *depart)  # remembr to use choose.get() to grab
        dept_entry.configure(bg='#D8BFD8')
        dept_label = Label(editor, text="Department: ")
        dept_label.grid(row=3, column=0, padx=20)
        dept_entry.grid(row=3, column=1, padx=20)

        gender_choice = StringVar(editor)
        gender_choice.set(gender[0])
        gender_entry = OptionMenu(editor, gender_choice, *gender)
        gender_label = Label(editor, text="Gender: ")
        gender_label.grid(row=4, column=0, padx=20)
        gender_entry.grid(row=4, column=1, padx=20)

        hostel_choice = StringVar(editor)
        hostel_choice.set(hostel[2])
        hostel_entry = OptionMenu(editor, hostel_choice, *hostel)
        hostel_label = Label(editor, text="Hostel: ")
        hostel_label.grid(row=5, column=0, padx=20)
        hostel_entry.grid(row=5, column=1, padx=20)

        pic_entry = Entry(editor, width=20, font='Ubuntu 12')
        pic_butt = Button(editor, text='Browse', command=browse, font='Ubuntu 10', bg='#d9dddc')
        pic_butt.grid(row=6, column=0, padx=20)
        pic_entry.grid(row=6, column=1, padx=20)

        # loop and insert
        for rec in record_values:
            matric_entry.insert(0, rec[0])
            fname_entry.insert(0, rec[1])
            sname_entry.insert(0, rec[2])
            dept_entry = OptionMenu(editor, choose.set(rec[3]), *depart)
            OptionMenu(editor, gender_choice.set(rec[4]), *gender)
            OptionMenu(editor, hostel_choice.set(rec[5]), *hostel)
            pic_entry.insert(0, rec[6])

        up_butt = Button(editor, text="Update", command=updat, font='Tahoma')
        up_butt.grid(row=7, column=0, columnspan=2, padx=15, pady=10, ipadx=50)


def filterdate():
    info = sqlite3.connect('edet.db')
    d1 = cal1.get_date()
    d2 = cal2.get_date()
    d11 = datetime.strptime(d1, "%d/%m/%Y")
    d111 = d11.strftime("%Y-%m-%d")
    d22 = datetime.strptime(d2, "%d/%m/%Y")
    d222 = d22.strftime("%Y-%m-%d")

    print(cal1.get_date())
    print(type(cal1.get_date()))

    boss = f"SELECT * FROM cafe WHERE date >= '{d111}' AND date <= '{d222}'"

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
    datafr.index = datafr.index + 1
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
    info.commit()
    info.close()
    messagebox.showinfo('PDF Created. ', 'Check The Document Folder.\nor wait for your browser to open it')


data_butt = Button(root, text='General Report', bg='#A0E7E5', command=filterdate, font='Tahoma')
data_butt.grid(row=16, column=0, padx=15, pady=10, ipadx=50)

studrec_butt = Button(root, text='Student Report', bg='#e7a0a2', command=studrec, font='Tahoma')
studrec_butt.grid(row=16, column=1, padx=15, pady=10, ipadx=50)

now_now = datetime.now()
year = now_now.year
month = now_now.month
day = now_now.day

cal1 = Calendar(root, selectmode='day', year=year, month=month, day=day, locale='en_UK')
cal2 = Calendar(root, selectmode='day', year=year, month=month, day=day + 1, locale='en_UK')
print(f'this month {type(month)}')

startLbl = Label(root, text='Start Date', font='Gulim')
stopLbl = Label(root, text='End Date', font='Arial')

startLbl.grid(row=17, column=0, sticky=W + E)
stopLbl.grid(row=17, column=1, sticky=W + E)

cal1.grid(row=18, column=0, padx=20, pady=10, sticky=W)
cal2.grid(row=18, column=1, sticky=E, padx=40)

idLabel = Label(root, text='Student ID', font='Gulim')
idLabel.grid(row=19, column=0)

identity = Entry(root, width=20, font='Georgia 13')
identity.grid(row=19, column=1, pady=5)

edit_butt = Button(root, text='Edit Record', bg='#e7c6fb', command=edit, font='Tahoma')
edit_butt.grid(row=20, column=0, padx=15, pady=10, ipadx=50)

count_butt = Button(root, text='Service Counter', bg='#c6dafb', command=melo, font='Tahoma')
count_butt.grid(row=20, column=1, padx=15, pady=10, ipadx=50)

# commit changes
conn.commit()
# close conn
conn.close()

root.mainloop()
