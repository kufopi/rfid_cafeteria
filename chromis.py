from tkinter import *
from tkinter import messagebox
from datetime import datetime
from tkinter import ttk
from tkcalendar import Calendar
import pdfkit as pdf
import unicodedata
import os
from fpdf import FPDF
import csv
import webbrowser
from PIL import Image,ImageTk
from tkinter import filedialog
import mysql.connector
import pandas as pd
import humanize
from num2words import num2words


def report():
    d1 = cal1.get_date()
    d2 = cal2.get_date()

    d11 = datetime.strptime(d1, "%d/%m/%Y")
    d111 = d11.strftime("%Y-%m-%d")
    d22 = datetime.strptime(d2, "%d/%m/%Y")
    d222 = d22.strftime("%Y-%m-%d")
    lati = d11.strftime("%b %d, %Y")
    si = d22.strftime("%b %d, %Y")

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database= 'supermarket1'
    )

    sql = f"select A.DATENEW, B.UNITS, C.PRICEBUY, B.PRICE from receipts A, ticketlines B, products C, payments D where A.DATENEW BETWEEN '{d111}' AND '{d222}' and A.ID=B.TICKET" + " and B.PRODUCT=C.ID and D.RECEIPT=A.ID and D.PAYMENT='cash' order BY DATENEW"
    gangta = pd.read_sql(sql,mydb)
    gangta['DATENEW'] = pd.to_datetime(gangta['DATENEW']).dt.date

    gangta['Total_Cost'] = gangta['UNITS'] * gangta['PRICEBUY']
    gangta['Total_Sale'] = gangta['UNITS'] * gangta['PRICE']
    gangta['Profit'] = gangta['Total_Sale'] - gangta['Total_Cost']
    tc = gangta['Total_Cost'].sum()
    ts = gangta['Total_Sale'].sum()
    tu = gangta['UNITS'].sum()
    tp = gangta['Profit'].sum()

    tt = gangta.groupby(['DATENEW'])[['Total_Cost', 'Total_Sale', 'UNITS','Profit']].apply(sum)  # Solution
    newdf = tt.copy()
    datafr = pd.DataFrame({
        #'Date': newdf.DATENEW,
        'Total_Cost': newdf.Total_Cost,
        'Total Sale': newdf.Total_Sale,
        'Units': newdf.UNITS,
        'Profit': newdf.Profit,

    })
    # datafr.index = datafr.index + 1
    datafr.to_csv('data.csv')
    with open('data.csv', newline='') as f:
        reader = csv.reader(f)

        sdf = FPDF()

        sdf.add_page()
        page_width = sdf.w - 2 * sdf.l_margin

        sdf.set_font('Helvetica', 'B', 14.0)
        sdf.image('au.jpg', 95, 0, w=20, h=18)

        sdf.cell(page_width, 20, 'SuperMarket Sales Data', align='C')
        sdf.ln(8)
        sdf.set_font('Helvetica', 'i', 10.0)
        sdf.cell(page_width, 20, f'From - {lati} To - {si}', align='C')

        sdf.ln(12)

        sdf.set_font('Courier', 'BI', 14)
        col_width = page_width / 5
        sdf.ln(3)

        th = sdf.font_size

        for row in reader:
            print(row)
            sdf.cell(col_width, th, str(row[0]), border=1)

            sdf.cell(col_width, th, row[1], border=1,align='C')
            sdf.cell(col_width, th, row[2], border=1,align='C')
            sdf.cell(col_width, th, row[3], border=1,align='C')
            sdf.cell(col_width, th, row[4], border=1,align='C')
            sdf.set_font('Helvetica', '', 12)

            sdf.ln(th)

        # txt = u'\u20a6'
        # # # utxt = unicode('txt', 'utf-8')
        # stxt = txt.decode('iso-8859-1')

        sdf.ln(10)
        sdf.add_font('ArialUnicode', fname='Arial-Unicode-Regular.ttf', uni=True)
        sdf.set_font('ArialUnicode', '', size=14)
        sdf.set_text_color(255,99,71)
        sdf.cell(col_width,th,'Grand Total',border='B',align='R')

        sdf.cell(col_width, th, f" \u20a6 {humanize.intcomma(tc)}", border='L',align='C')

        sdf.cell(col_width, th, f" \u20a6 {humanize.intcomma(ts)}",border='L',align='C')
        sdf.cell(col_width, th, f"{tu}", border='L',align='C')

        sdf.cell(col_width, th, f" \u20a6 {humanize.intcomma(tp)}", border='L',align='C')
        sdf.set_font('Helvetica', '', 12)
        sdf.ln(10)
        sdf.cell(page_width,0,f'Total Sale in Words: {num2words(ts).title()} naira only')
        sdf.ln(7)
        sdf.cell(page_width, 0, f'Total Profit in Words: {num2words(tp).title()} naira only')
        sdf.ln(15)
        sdf.set_text_color(147, 58, 23)
        sdf.add_font('Amigos Regular', fname='Amigos 400.ttf', uni=True)
        sdf.set_font('Amigos Regular', '', size=12)
        # sdf.set_font('Times', '', 10.0)
        sdf.cell(page_width, 0.0, '- End of report -', align='C')
        sdf.ln(18)

        #sdf.add_font('FreeSans', fname='font/FreeSans.ttf', uni=True)
        sdf.set_font('Times', '', 14.0)

        sdf.cell(page_width, 0.0, '- --------------- -')
        sdf.ln(4)
        sdf.cell(page_width, 0.0, 'Store Manager')
        sdf.ln(8)

        sdf.add_font('Amigos Regular', fname='Amigos 400.ttf', uni=True)
        sdf.set_font('Amigos Regular', '', size=12)

        sdf.cell(page_width, 0.0, f'- Produced on {datetime.today().strftime("%B %d, %Y")} -', align='C')
        sdf.ln(8)
        sdf.cell(page_width, 0.0, f'- Powered by Kufopo -', align='C')
        sdf.output('C:/Users/NHS_CHRIS013/Documents/Supermarket.pdf', 'F')
        webbrowser.open('C:/Users/NHS_CHRIS013/Documents/Supermarket.pdf')

    mydb.close()
    messagebox.showinfo('PDF Created. ', 'Check The Document Folder.\nor wait for your browser to open it')





root = Tk()
root.title('Esther Adeleke Supermarket Management')
root.geometry('600x400')
root.iconbitmap('favicon.ico')
root.configure(bg='#fbe7c6')

data_butt = Button(root, text='Generate Report', bg='#A0E7E5',  font='Tahoma', command=report)
data_butt.grid(row=4, column=0, padx=15, pady=10, ipadx=50)


now_now = datetime.now()
year = now_now.year
month = now_now.month
day = now_now.day

cal1 = Calendar(root, selectmode='day', year=year, month=month, day=day,locale='en_UK' )
cal2 = Calendar(root, selectmode='day', year=year, month=month, day=day + 1,locale='en_UK')
print(f'this month {type(month)}')
print(cal1.get_date())
print(type(cal1.get_date()))
print(unicodedata.lookup("NAIRA SIGN"))



startLbl = Label(root, text='Start Date', font='Gulim')
stopLbl = Label(root, text='End Date', font='Arial')

startLbl.grid(row=6, column=0, sticky=W + E)
stopLbl.grid(row=6, column=1, sticky=W + E)

cal1.grid(row=8, column=0, padx=20, pady=10, sticky=W)
cal2.grid(row=8, column=1, sticky=E, padx=40)

root.mainloop()