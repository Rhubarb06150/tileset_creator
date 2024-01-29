import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, ttk, colorchooser
from PIL import Image,ImageTk
import os,PIL,webbrowser,urllib.request,requests
from bs4 import BeautifulSoup
import pyautogui
import cv2
from cv2 import *
import numpy as np

def continuous_rip(master):

    master=Toplevel()
    master.geometry('480x480')
    master.title('Continuous Rip')
    master.iconbitmap('icon.ico')

    # FUNCTIONS

    def preview_rip_con():
        try:
            int(rip_w.get())
            int(rip_h.get())
            int(rip_interval.get())
            int(rip_pos_x.get())
            int(rip_pos_y.get())
            int(max_rip.get())

        except:

            res=''
            try:
                int(rip_w.get())
            except:
                res+='  -Rip width\n'
            try:
                int(rip_h.get())
            except:
                res+='  -Rip Height\n'
            try:
                int(rip_interval.get())
            except:
                res+='  -Rip interval\n'
            try:
                int(max_rip.get())
            except:
                res+='  -Number of rips\n'
            try:
                int(rip_pos_x.get())
            except:
                res+='  -Rip position X\n'
            try:
                int(rip_pos_y.get())
            except:
                res+='  -Rip position Y\n'

            msg=messagebox.showerror(title='Error',message=('please verify following entries:\n\n'+res))

    # LABELS
        
    title=Label(master,text='______ Continuous Rip ______')
    title.place(x=2,y=2)

    rip_w_l=Label(master,text='Rip width (px):')
    rip_w_l.place(x=2,y=30)
    rip_w=Entry(master,width=8)
    rip_w.place(x=96,y=30)

    rip_h_l=Label(master,text='Rip height (px):')
    rip_h_l.place(x=2,y=52)
    rip_h=Entry(master,width=8)
    rip_h.place(x=96,y=52)

    rip_interval_l=Label(master,text='Rip interval (ms):')
    rip_interval_l.place(x=2,y=74)
    rip_interval=Entry(master,width=8)
    rip_interval.place(x=96,y=74)

    max_rip_l=Label(master,text='Number of rips:')
    max_rip_l.place(x=2,y=96)
    max_rip=Entry(master,width=8)
    max_rip.place(x=96,y=96)

    rip_pos_x_l=Label(master,text='Rip position X:')
    rip_pos_x_l.place(x=2,y=118)
    rip_pos_x=Entry(master,width=8)
    rip_pos_x.place(x=96,y=118)

    rip_pos_y_l=Label(master,text='Rip position Y:')
    rip_pos_y_l.place(x=2,y=140)
    rip_pos_y=Entry(master,width=8)
    rip_pos_y.place(x=96,y=140)

    preview_l=Label(master,text='Preview:')
    preview_l.place(x=180,y=30)
    img=ImageTk.PhotoImage(Image.open('no_img.png'))
    preview=Label(master,image=img,borderwidth=0)
    preview.place(x=230,y=30)
    preview.im=img

    preview_button=Button(master,text='Preview zone',command=lambda:preview_rip_con())
    preview_button.place(x=2,y=162,height=24)

    master.mainloop()

continuous_rip('master')