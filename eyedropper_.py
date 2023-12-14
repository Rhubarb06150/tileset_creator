import pyautogui
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, ttk, colorchooser
from tkinter.colorchooser import askcolor
from PIL import Image,ImageTk
import cv2 as cv2
from cv2 import *
import numpy as np

color=''
color_=''
zo=1

liste_labels=[]
liste_labels_t=[]

def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    
    return tuple(rgb)

def rm_color(color,image):
    color_=hex_to_rgb(color)
    img = Image.open(image)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []

    for item in datas:
        if item[0] == 0 and item[1] == 64 and item[2] == 128:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(image)



def eyedropper_win(image,colors_to_rm):

    print(colors_to_rm)

    global liste_labels
    global liste_labels_t

    empty__ = Image.new('RGBA', (32,32), (0,0,0,0))
    empty__.save('C:/tmp/empty__.png')
    empty__=ImageTk.PhotoImage(Image.open('C:/tmp/empty__.png'))

    master=Toplevel()
    master.title('Color picker')
    master.iconbitmap('icon.ico')
    master.geometry('512x256')

    color_hover=Label(master,image=empty__,border=2,relief='solid')
    color_hover.place(x=334,y=4)
    color_hover_=Label(master,text='Color picked:')
    color_hover_.place(x=258,y=10)

    color_add=Button(master,text='Add color',borderwidth=1)
    color_add.place(x=376,y=10)

    color_clear=Button(master,text='Clear colors',borderwidth=1)
    color_clear.place(x=440,y=10)

    for i in range(5):

        label=Label(master,image=empty__,relief='solid',border=2)
        label.place(x=270,y=(40+(i*34)))
        label_=Label(master,text='')
        label_.place(x=310,y=(50+(i*34)))

        liste_labels.append(label)
        liste_labels_t.append(label_)

    base_image=Label(master,borderwidth=0)
    base_image.place(x=0,y=0)
    img_= Image.open(image)
    img_=img_.crop((0,0,128,128))
    img_=img_.resize((256,256),Image.NEAREST)
    img_.save('C:/tmp/color_template.png')
    img = ImageTk.PhotoImage(Image.open('C:/tmp/color_template.png'))
    base_image.configure(image=img,borderwidth=0,cursor='tcross')
    base_image.im=img

    def change_square():

        run_eyedropper()
        hover_color()

    def hover_color():

        img = ImageTk.PhotoImage(Image.open('C:/tmp/color_template.png'))
        color_hover.configure(bg=color_)
        color_hover.im=img

    def run_eyedropper():

        global color
        global color_
        img = pyautogui.screenshot()
        color = img.getpixel(pyautogui.position())
        color_=('#{0:02x}{1:02x}{2:02x}'.format(*color))

    def add_color():

        global liste_labels
        global liste_labels_t

        if color_ not in colors_to_rm:
            colors_to_rm.append(color_)
            liste_labels[len(colors_to_rm)-1].configure(bg=color_)
            liste_labels_t[len(colors_to_rm)-1].configure(text=color_)

    def zoom(dir):
        global zo
        if dir=='up':
            zo+=1
        else:
            zo-=1
        if zo==0:
            zo=1
        if zo==5:
            zo=4
        x,y=128/zo,128/zo
        img_= Image.open(image)
        img_=img_.crop((0,0,x,y))
        img_=img_.resize((256,256),Image.NEAREST)
        img_.save('C:/tmp/color_template.png')
        img = ImageTk.PhotoImage(Image.open('C:/tmp/color_template.png'))
        base_image.configure(image=img,borderwidth=0,cursor='tcross')
        base_image.im=img

    def clear_colors():

        global liste_labels_t
        global liste_labels

        if colors_to_rm != []:
            msg=messagebox.askyesno(title='Warning!',message='Do you want to clear all colors?')

            if msg:

                for label in liste_labels:
                    label.configure(bg='#ffffff')
                for label in liste_labels_t:
                    label.configure(text='')
                colors_to_rm=[]

    def confirm_f():

        msg=messagebox.askyesno(title='Color remove',message='Do you want to remove selected colors from the tileset?')
        if msg:
            if colors_to_rm!=[]:
                for couleur in colors_to_rm:
                    colors_to_rm.append(couleur)
                master.destroy()
                msg=messagebox.showinfo(title='Colors removed!',message='The selected colors were removed :)')
            else:
                msg=messagebox.showerror(title='Error!',message='No colors to remove!')

    color_add.configure(command=lambda:add_color())
    color_clear.configure(command=lambda:clear_colors())

    zoom_plus=Button(master,text='+',command=lambda:zoom('up'),borderwidth=1)
    zoom_less=Button(master,text='-',command=lambda:zoom('down'),borderwidth=1)
    zoom_plus.place(x=274,y=230)
    zoom_less.place(x=260,y=230)
    confirm=Button(master,text='Remove colors',borderwidth=1,command=lambda:confirm_f())
    confirm.place(x=300,y=230)

    base_image.bind('<Button-1>',lambda event:change_square())
    def place():

        global liste_labels
        global liste_labels_t

        if colors_to_rm!=[]:
            for i in range(len(colors_to_rm)):
                co=colors_to_rm[i]
                liste_labels[i].configure(bg=co)
                liste_labels_t[i].configure(text=co)

    place()

    master.mainloop()