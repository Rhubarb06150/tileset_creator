import pyautogui
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, ttk, colorchooser
from tkinter.colorchooser import askcolor
from PIL import Image,ImageTk

color=''
color_=''

liste_labels=[]
liste_couleurs=[]
liste_labels_t=[]

def eyedropper_win(image):

    global liste_labels
    global liste_couleurs
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
        label.place(x=270,y=(50+(i*40)))
        label_=Label(master,text='')
        label_.place(x=310,y=(60+(i*40)))

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

        global liste_couleurs
        global liste_labels
        global liste_labels_t

        if color_ not in liste_couleurs:
            liste_couleurs.append(color_)
            liste_labels[len(liste_couleurs)-1].configure(bg=color_)
            liste_labels_t[len(liste_couleurs)-1].configure(text=color_)

    def clear_colors():

        global liste_couleurs
        global liste_labels_t
        global liste_labels
        if liste_couleurs != []:
            msg=messagebox.askyesno(title='Warning!',message='Do you want to clear all colors?')

            if msg:

                for label in liste_labels:
                    label.configure(bg='#ffffff')
                for label in liste_labels_t:
                    label.configure(text='')
                liste_couleurs=[]

    color_add.configure(command=lambda:add_color())
    color_clear.configure(command=lambda:clear_colors())
        

    base_image.bind('<Button-1>',lambda event:change_square())

    master.mainloop()

