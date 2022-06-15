from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title('Chrisland Millennium University')
root.iconbitmap('R.ico')

img1= ImageTk.PhotoImage(Image.open('png/002-hen.png'))
img2= ImageTk.PhotoImage(Image.open('png/003-seal.png'))
img3= ImageTk.PhotoImage(Image.open('png/006-parrot.png'))
img4= ImageTk.PhotoImage(Image.open('png/015-monkey.png'))
img5= ImageTk.PhotoImage(Image.open('png/009-walrus.png'))
img6= ImageTk.PhotoImage(Image.open('png/019-jellyfish.png'))
img7= ImageTk.PhotoImage(Image.open('png/024-kiwi.png'))

frame= LabelFrame(root, text="Zoo Animals, we love...", padx=8, pady=8)

imageList= [img1,img2,img3,img4,img5,img6,img7]

myLabel= Label(image=img1)
myLabel.grid(row=0,column=0,columnspan=3)
count=1
status = Label(root, text=f'Image {count} of {len(imageList)}',bd=1, relief=SUNKEN)


def regress(number):
    global myLabel, btn_forward, btn_back, status

    myLabel.grid_forget()
    myLabel = Label(image=imageList[number - 1])
    btn_forward = Button(root, text='>>>', bg='#ffff99', command=lambda: march(number + 1))
    btn_back = Button(root, text='<<<', bg='#f0dc82', command=lambda: regress(number - 1))
    # count =count -1
    status = Label(root, text=f'Image {number} of {len(imageList)}',bd=1, relief=SUNKEN, anchor=W)

    if number == 1:
        btn_back = Button(root, text='<<<', state=DISABLED)

    myLabel.grid(row=0, column=0, columnspan=3)
    btn_back.grid(row=1, column=0)
    btn_forward.grid(row=1, column=2,pady=10)
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)


def march(number):
    global myLabel,btn_forward,btn_back,status

    myLabel.grid_forget()
    myLabel=Label(image=imageList[number-1])
    btn_forward= Button(root,text='>>>',bg='#ffff99',command= lambda :march(number+1))
    btn_back= Button(root, text='<<<',bg='#f0dc82', command=lambda :regress(number-1))
    # count=count +1
    status = Label(root, text=f'Image {number} of {len(imageList)}',bd=1, relief=SUNKEN,anchor=E)

    if number==len(imageList):
        btn_forward = Button(root, text='>>>', state=DISABLED)

    myLabel.grid(row=0,column=0,columnspan=3)
    btn_back.grid(row=1, column=0)
    btn_forward.grid(row=1, column=2, pady=10)
    status.grid(row=2, column=0, columnspan=3, sticky=W+E)
    #btn_exit.grid(row=1, column=1)
    print(f'len of loist {len(imageList)}')

    print(f'number right now {number}')

btn_back = Button(root,text="<<",bg='#f0dc82')
btn_forward = Button(root,text=">>",bg='#ffff99', command=lambda :march(2))
btn_exit =Button(root, text='Quit', command=root.quit, bg='#de3163')

btn_back.grid(row=1, column=0)
btn_forward.grid(row=1, column=2,pady=10)
btn_exit.grid(row=1, column=1)
status.grid(row=2, column=0, columnspan=3, sticky=W+E)

root.mainloop()



