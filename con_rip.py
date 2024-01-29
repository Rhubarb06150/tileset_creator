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

    max_rip_l=Label(master,text='Max number of rips:')
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

    # FUNCTIONS

    def preview_rip_con():
        try:
            int(rip_w.get())
            int(rip_h.get())
            int(rip_w.get())
            int(rip_w.get())
            int(rip_w.get())
            int(rip_w.get())
        except:
            msg=messagebox(title='o')

    master.mainloop()

continuous_rip('master')