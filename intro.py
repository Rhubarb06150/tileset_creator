import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, ttk, colorchooser
from tkinter.colorchooser import askcolor
from PIL import Image,ImageTk
import os,PIL,webbrowser,urllib.request,requests
from bs4 import BeautifulSoup
import pyautogui
import cv2 as cv2
from cv2 import *
import numpy as np


colors_to_rm=[]

import cv2 as cv2
from cv2 import *
import numpy as np

liste_images=[]
liste_images_rip=[]

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
        if item[0] == color_[0] and item[1] == color_[1] and item[2] == color_[2]:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(image)

def eyedropper_win(image,color_attr):
    
    liste_labels=[]
    liste_labels_t=[]

    empty__ = Image.new('RGBA', (32,32), (0,0,0,0))
    empty__.save('C:/tmp/empty__.png')
    empty__=ImageTk.PhotoImage(Image.open('C:/tmp/empty__.png'))

    master=Toplevel()
    master.title('Color picker')

    master.iconbitmap('icon.ico')
    master.geometry('512x256')
    master.resizable(False,False)

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

    def add_color(color_attr):

        if color_ not in color_attr:
            if len(color_attr)==5:
                msg=messagebox.showerror(title='Error',message="Can't add more than 5 colors to remove!")
            else:
                color_attr.append(color_)
                liste_labels[len(color_attr)-1].configure(bg=color_)
                liste_labels_t[len(color_attr)-1].configure(text=color_)

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

    def clear_colors(color_attr):

        global colors_to_rm

        if color_attr != []:
            msg=messagebox.askyesno(title='Warning!',message='Do you want to clear all colors?')
            if msg:
                for label in liste_labels:
                    label.configure(bg='#f0f0f0')
                for label in liste_labels_t:
                    label.configure(text='')
                msg=messagebox.showinfo(title='Cleared',message="All colors were cleared")
                master.destroy()
                colors_to_rm=[]
                
    for i in range(len(color_attr)):
        liste_labels[i].configure(bg=color_attr[i])
        liste_labels_t[i].configure(text=color_attr[i])


    def confirm_f():

        msg=messagebox.askyesno(title='Color remove',message='Do you want to remove selected colors from the tileset?')
        if msg:
            if color_attr!=[]:
                master.destroy()
                msg=messagebox.showinfo(title='Colors removed!',message='The selected colors were removed :)')
            else:
                msg=messagebox.showerror(title='Error!',message='No colors to remove!')

    color_add.configure(command=lambda:add_color(color_attr))
    color_clear.configure(command=lambda:clear_colors(color_attr))

    zoom_plus=Button(master,text='+',command=lambda:zoom('up'),borderwidth=1)
    zoom_less=Button(master,text='-',command=lambda:zoom('down'),borderwidth=1)
    zoom_plus.place(x=274,y=230)
    zoom_less.place(x=260,y=230)

    base_image.bind('<Button-1>',lambda event:change_square())

    master.mainloop()

def upload():
    global liste_images
    liste_images=[]
    filename = filedialog.askopenfilenames()
    if filename!='':
        fichier.configure(text=('Files: '+str(filename)))
    for i in filename:
        liste_images.append(i)
    aff_size()

def upload_rip():
    global liste_images_rip
    filename = filedialog.askopenfilename()
    if filename!='':
        files_.configure(text=('File: '+str(filename)))
    if filename!='':
        liste_images_rip=[]
        liste_images_rip.append(filename)
        x_tile.set('0')
        y_tile.set('0')
        rip('show_f')
        im=Image.open(liste_images_rip[0])
        files_.bind('<Button-1>',lambda event:im.show())
        files_.configure(cursor='hand2')

bg_color='#ffffff'
def change_color():
    global bg_color
    colors = askcolor(title="Choix de la couleur de fond")
    bg_color=(colors[1])

def hex_to_rgb(hex):
  hex=hex.replace('#','')
  rgb = []
  for i in (0, 2, 4):
    decimal = int(hex[i:i+2], 16)
    rgb.append(decimal)
  
  return tuple(rgb)

def aff_size():

    global smb3
    global sens
    global upscale

    hauteur=0
    largeur=0
    try:
        if sens.get()=='Vertical':
            for i in range(len(liste_images)):
                with Image.open(liste_images[i]) as ima:
                    w, h = ima.size
                    ima_w=int(w)
                    hauteur+=h
                    if ima_w >= largeur:
                        largeur=ima_w
            if smb3.get()==1:
                hauteur=hauteur*2
        else:
            for i in range(len(liste_images)):
                with Image.open(liste_images[i]) as ima:
                    w, h = ima.size
                    ima_h=int(h)
                    largeur+=w
                    if ima_h >= hauteur:
                        hauteur=ima_h
            if smb3.get()==1:
                largeur=largeur*2
        if upscale.get()=='x2':
            hauteur,largeur=hauteur*2,largeur*2
        elif upscale.get()=='x4':
            hauteur,largeur=hauteur*4,largeur*4
        elif upscale.get()=='x8':
            hauteur,largeur=hauteur*8,largeur*8
        elif upscale.get()=='x16':
            hauteur,largeur=hauteur*16,largeur*16
        elif upscale.get()=='x32':
            hauteur,largeur=hauteur*32,largeur*32
        elif upscale.get()=='x64':
            hauteur,largeur=hauteur*64,largeur*64
        hauteur_.configure(text=('Height: '+str(hauteur)+'px'))
        largeur_.configure(text=('Width: '+str(largeur)+'px'))
    except:
        hauteur_.configure(text=('Height: NONE'))
        largeur_.configure(text=('Width: NONE'))

def create():

    global bg_color
    global smb3
    global upscale
    global folder_selected

    if folder_selected=='':
        if not os.path.exists('tilesets'):
            os.mkdir('tilesets/')
            os.listdir()
            msg=messagebox.showinfo(title='Hey',message="'tilesets/' folder wasn't found so folder was created to prevent any problems")

    try:
        with Image.open(liste_images[0]) as ima:
            w, h = ima.size
        if transparent.get()==1:
            img = Image.new('RGBA', (h,w), (0,0,0,0))
        else:
            img = Image.new('RGB', (h,w), bg_color)
        a=0
        
        if sens.get() == 'Vertical':
            if smb3.get() == 1:
                img = img.resize(((w,((len(liste_images)*h)*2))))
                for i in liste_images:
                    with Image.open(str(i)) as ima:
                        img_=ima.copy()
                        img.paste(ima,(0,h*a),mask=ima)
                    a+=1
                for i in liste_images:
                    with Image.open(str(i)) as ima:
                        ima=ima.transpose(method=Image.FLIP_LEFT_RIGHT)
                        img_=ima.copy()
                        img.paste(ima,(0,h*a),mask=ima)
                    a+=1
            else:
                img = img.resize(((w,(len(liste_images)*h))))
                for i in liste_images:
                    with Image.open(str(i)) as ima:
                        img_=ima.copy()
                        img.paste(ima,(0,h*a),mask=ima)
                    a+=1
            if upscale.get()=='x2':
                img=img.resize((w*2,h*a*2),Image.NEAREST)
            if upscale.get()=='x4':
                img=img.resize((w*4,h*a*4),Image.NEAREST)
            if upscale.get()=='x8':
                img=img.resize((w*8,h*a*8),Image.NEAREST)
            if upscale.get()=='x16':
                img=img.resize((w*16,h*a*16),Image.NEAREST)
            if upscale.get()=='x32':
                img=img.resize((w*32,h*a*32),Image.NEAREST)
            if upscale.get()=='x64':
                img=img.resize((w*64,h*a*64),Image.NEAREST)
        else:
            if smb3.get() == 1:
                img = img.resize(((((len(liste_images)*w)*2),h)))
                for i in liste_images:
                    with Image.open(str(i)) as ima:
                        img_=ima.copy()
                        img.paste(ima,(w*a,0),mask=ima)
                    a+=1
                for i in liste_images:
                    with Image.open(str(i)) as ima:
                        ima=ima.transpose(method=Image.FLIP_LEFT_RIGHT)
                        img_=ima.copy()
                        img.paste(ima,(w*a,0),mask=ima)
                    a+=1
            else:
                img = img.resize((((len(liste_images)*w),h)))
                for i in liste_images:
                    with Image.open(str(i)) as ima:
                        img_=ima.copy()
                        img.paste(ima,(w*a,0),mask=ima)
                    a+=1
            if upscale.get()=='x2':
                img=img.resize((w*2*a,h*2),Image.NEAREST)
            if upscale.get()=='x4':
                img=img.resize((w*4*a,h*4),Image.NEAREST)
            if upscale.get()=='x8':
                img=img.resize((w*8*a,h*8),Image.NEAREST)
            if upscale.get()=='x16':
                img=img.resize((w*16*a,h*16),Image.NEAREST)
            if upscale.get()=='x32':
                img=img.resize((w*32*a,h*32),Image.NEAREST)
            if upscale.get()=='x64':
                img=img.resize((w*64*a,h*64),Image.NEAREST)
        try:
            if folder_selected != '':
                if os.path.exists(folder_selected+'/'+str(filename.get())+format.get()):
                    ask=messagebox.askyesno(title='Tileset already exist!',message=('An file named '+filename.get()+format.get()+' already exists, do you want to replace it?'))
                    if ask:
                        img.save(folder_selected+'/'+str(filename.get())+format.get())
                        msg=messagebox.showinfo(title='Succes!',message=("Your tileset has been created\n as "+filename.get()+format.get()))
                else:
                    img.save(folder_selected+'/'+str(filename.get())+format.get())
                    msg=messagebox.showinfo(title='Succes!',message=("Your tileset has been created\n as "+filename.get()+format.get()))
            else:
                if os.path.exists('tilesets/'+str(filename.get())+format.get()):
                    ask=messagebox.askyesno(title='Tileset already exist!',message=('An file named '+filename.get()+format.get()+' already exists, do you want to replace it?'))
                    if ask:
                        img.save('tilesets/'+str(filename.get())+format.get())
                        msg=messagebox.showinfo(title='Succes!',message=("Your tileset has been created\n as "+str(filename.get())+format.get()))
                else:
                    img.save('tilesets/'+str(filename.get())+format.get())
                    msg=messagebox.showinfo(title='Succes!',message=("Your tileset has been created\n as "+str(filename.get())+format.get()))
        except:
            if folder_selected != '':
                if os.path.exists(folder_selected+'/tileset'+format.get()):
                    ask=messagebox.askyesno(title='Tileset already exist!',message=('An file named tileset'+format.get()+' already exists, do you want to replace it?'))
                    if ask:
                        img.save(folder_selected+'/tileset'+format.get())
                        msg=messagebox.showinfo(title='Hey',message="The filename was empty or contained illegal characters\nso your sheet were named 'tileset"+format.get()+"'")
                else:
                    img.save(folder_selected+'/tileset'+format.get())
                    msg=messagebox.showinfo(title='Hey',message="The filename was empty or contained illegal characters\nso your sheet were named 'tileset"+format.get()+"'")
            else:
                if os.path.exists('tilesets/tileset'+format.get()):
                    ask=messagebox.askyesno(title='Tileset already exist!',message=('An file named tileset'+format.get()+' already exists, do you want to replace it?'))
                    if ask:
                        img.save('tilesets/tileset'+format.get())
                        msg=messagebox.showinfo(title='Hey',message="The filename was empty or contained illegal characters\nso your sheet were named 'tileset"+format.get()+"'")
                else:
                    img.save('tilesets/tileset'+format.get())
                    msg=messagebox.showinfo(title='Hey',message="The filename was empty or contained illegal characters\nso your sheet were named 'tileset"+format.get()+"'")
    except:
        msg=messagebox.showerror(title='Error',message="An error as occured! \n\n(please verify that you've been\nupload your images.)")

def rip(ty):
    b=0
    try:

        if ty=='rip':
            img=Image.open(liste_images_rip[0])
            if folder_selected=='':
                if not os.path.exists('tilesets/tiles'):
                    os.mkdir('tilesets/')
                    os.mkdir('tilesets/tiles')
                    os.listdir()
                    msg=messagebox.showinfo(title='Hey',message="'tilesets/tiles/' folder wasn't found so folders were created to prevent any problems")

            hauteur=0
            largeur=0
            h, w=img.size
            img2=img.crop((16,16,32,32))

            x=0
            y=0
            t_o=0
            t_s=0

            t_o=int(((tile_offset.get()).replace('x','')).replace('p',''))
            x_o=int(((x_tile_offset.get()).replace('x','')).replace('p',''))
            y_o=int(((y_tile_offset.get()).replace('x','')).replace('p',''))
            t_s=int(((tile_size.get()).replace('x','')).replace('p',''))
            a=0
            
            row=0
            
            y=y_o
            column=0
            if int(s_columns.get()) > 1:
                b_o=(160+t_o)*int(s_columns.get())
            else:
                b_o=0
            if columns.get()!='All':
                max_col=int(columns.get())
            else:
                max_col=1000
            if rows.get()!='All':
                max_row=int(rows.get())
            else:
                max_row=1000
            fin=False
            x=x_o+b_o
            cur_col=0

            if tile_name.get()=='':
                tile_name.insert(0,'tile-')

            while True:

                if (x+160)<=h:

                    img2=img.crop((x,y,(x+160),(y+144)))

                else:

                    fin=True
                    y+=144+t_o
                    x=x_o+b_o
                    cur_col=0
                    row+=1

                if (y+144)>=w:

                    cur_col=0
                    y=((144*row)+(row*t_o)+y_o)
                    x=x_o+b_o
                    row+=1
                    for i in range(100):

                        img2=img.crop((x,y,x+160,y+144))
                        img2=img2.resize(((160*(int(_upscale.get().replace('x','')))),(144*(int(_upscale.get().replace('x',''))))),Image.NEAREST)
                        
                        if i == 0:
                            if (max_col != 1000 and max_col != column):
                                if max_col!=1:
                                    if folder_selected=='':
                                        os.remove('tilesets/tiles/'+str(tile_name.get())+str(a+1)+".png")
                                        a-=1
                                    else:
                                        os.remove(folder_selected+"/"+str(tile_name.get())+str(a+1)+".png")
                                        a-=1
                    
                        if folder_selected=='':
                            img2.save('tilesets/tiles/'+str(tile_name.get())+str(a+1)+'.png')
                            if colors_to_rm!=[]:
                                for e in colors_to_rm:
                                    rm_color(str(e).replace('#',''),'tilesets/tiles/'+str(tile_name.get())+str(a+1)+'.png')
                            extrema = Image.open('tilesets/tiles/'+str(tile_name.get())+str(a+1)+'.png').convert("L").getextrema()
                            if extrema == ((0,0)):
                                os.remove('tilesets/tiles/'+str(tile_name.get())+str(a+1)+".png")
                                a-=1
                        else:
                            img2.save(folder_selected+'/'+str(tile_name.get())+str(a+1)+'.png')
                            if colors_to_rm!=[]:
                                for e in colors_to_rm:
                                    rm_color(str(e).replace('#',''),folder_selected+'/'+str(tile_name.get())+str(a+1)+'.png')
                            extrema = Image.open(folder_selected+'/'+str(tile_name.get())+str(a+1)+'.png').convert("L").getextrema()
                            if extrema == ((0,0)):
                                os.remove(folder_selected+"/"+str(tile_name.get())+str(a+1)+".png")
                                a-=1
                        
                        x+=160+t_o
                        a+=1
                        b+=1
                        cur_col+=1
                        if i+1 == max_col or i == column:
                            break
                    break
                if  cur_col >= max_col:
                    cur_col=0
                    y+=144+t_o
                    x=x_o+b_o
                    row+=1
                if row >= max_row:
                    break
                if not fin:
                    column+=1
                img2=img.crop((x,y,(x+160),(y+144)))
                img2=img2.resize(((160*(int(_upscale.get().replace('x','')))),(144*(int(_upscale.get().replace('x',''))))),Image.NEAREST)
                if folder_selected=='':
                    img2.save('tilesets/tiles/'+str(tile_name.get())+str(a+1)+'.png')
                    if colors_to_rm!=[]:
                        for e in colors_to_rm:
                            rm_color(str(e).replace('#',''),'tilesets/tiles/'+str(tile_name.get())+str(a+1)+'.png')
                    extrema = Image.open('tilesets/tiles/'+str(tile_name.get())+str(a+1)+'.png').convert("L").getextrema()
                    if extrema == ((0,0)):
                        os.remove("tilesets/tiles/"+str(tile_name.get())+str(a+1)+".png")
                        a-=1
                else:
                    img2.save(folder_selected+'/'+str(tile_name.get())+str(a+1)+'.png')
                    if colors_to_rm!=[]:
                        for e in colors_to_rm:
                            rm_color(str(e).replace('#',''),folder_selected+'/'+str(tile_name.get())+str(a+1)+'.png')
                    extrema = Image.open(folder_selected+'/'+str(tile_name.get())+str(a+1)+'.png').convert("L").getextrema()
                    if extrema == ((0,0)):
                        os.remove(folder_selected+"/"+str(tile_name.get())+str(a+1)+".png")
                        a-=1
                cur_col+=1
                x+=160+t_o
                a+=1
                b+=1
                if (b+1)%200 == 0:
                    msg=messagebox.askyesno(title='Warning!',message=(str(b+1)+' tiles (excluding empty tiles) were generated, \ndo you want to continue?'))
                    if not msg:
                        break
                print(row)
            
            msg=messagebox.showinfo(title='Succes!',message=('Successfully generated '+str(a)+' tiles :)'))

        elif ty=='show_f':

            if preview_e.get()==1:

                img=Image.open(liste_images_rip[0])

                hauteur=0
                largeur=0
                h, w=img.size
                img2=img.crop((16,16,32,32))

                x=0
                y=0
                t_o=0
                t_s=0

                t_o=int(((tile_offset.get()).replace('x','')).replace('p',''))
                x_o=int(((x_tile_offset.get()).replace('x','')).replace('p',''))
                y_o=int(((y_tile_offset.get()).replace('x','')).replace('p',''))
                t_s=int(((tile_size.get()).replace('x','')).replace('p',''))

                if int(s_columns.get()) > 1:
                    b_o=(t_s+t_o)*int(s_columns.get())
                else:
                    b_o=0
                x_o+=b_o
                a=0

                x=x=(t_s*int(x_tile.get()))+x_o
                y=y=(t_s*int(y_tile.get()))+y_o
                column=0
                fin=False

                off_x=t_o*int(x_tile.get())
                off_y=t_o*int(y_tile.get())

                img2=img.crop((x+off_x,y+off_y,(x+t_s+off_x),(y+t_s+off_y)))
                img2=img2.resize((64,64),Image.NEAREST)
                img2.save('C:/tmp/tile_preview.png')

                path='C:/tmp/tile_preview.png'
                img3 = ImageTk.PhotoImage(Image.open(path))
                preview_.configure(image=img3,borderwidth=0)
                preview_.im=img3
                
            else:

                empty_ = Image.new('RGBA', (64,64), (0,0,0,0))
                empty_.save('C:/tmp/empty.png')
                path='C:/tmp/empty.png'
                em = ImageTk.PhotoImage(Image.open(path))
                preview_.configure(image=em,borderwidth=0)
                preview_.im=em


    except Exception as error:
        msg=messagebox.showerror(title='Error',message="An error as occured! \n\n(please verify that you've been\nupload your images.)")
        print(error)

def verif_size():
    if upscale.get() == 'x16' or upscale.get() == 'x32' or upscale.get() == 'x64':
        avert.configure(text="Warning! too big upscale could lead to a crash,\n don't use big upscale if your computer can't handle it!")
    else:
        avert.configure(text="")
    aff_size()

folder_selected=''
def choose_path():
    global folder_selected
    f_s = filedialog.askdirectory()
    if f_s!='':
        folder_selected=f_s

def open_path():
    global folder_selected
    if folder_selected=='':
        path = (os.getcwd()+'/tilesets/tiles/')
        os.startfile(path)
    else:
        os.startfile(folder_selected)

def format_f():
    if format.get()!='.png':
        format_.configure(text='.jpeg and .jpg formats\ncauses a lot of quality loss')
    else:
        format_.configure(text='')

version=0.2

def update_check():
    global version
    try:
        r=requests.get("https://mcrhubarb.net/tileset_editor/")
        soup=BeautifulSoup(r.content,"html.parser")
        ver_site=soup.find("div",{"class":"ver"}).get_text()
        if float(version)!=float(ver_site):
            msg=messagebox.askyesno(title='Found!',message='An updtae is avaliable ('+str(ver_site)+'), do you want to download it?')
            if msg:
                webbrowser.open('https://github.com/Rhubarb06150/tileset_editor/')
        else:
            msg=messagebox.showinfo(title='No update found',message='The software seems to be up to date :)')
    except:
        msg=messagebox.showerror(title='Error',message="Can't check for updates, maybe you aren't connected to network :(")

def place_buttons():
    update.place(x=(root.winfo_width())-107,y=(root.winfo_height())-26)
    help_.place(x=(root.winfo_width())-68,y=106)
    idea_.place(x=(root.winfo_width())-76,y=80)
    bug_report.place(x=(root.winfo_width())-77,y=54)
    path__.place(x=(root.winfo_width())-111,y=28)
    path_.place(x=(root.winfo_width())-122,y=2)

root=Tk()
root.geometry('880x480')
root.title('Tileset Editor ('+str(version)+')')
root.minsize(880,480)

try:
    root.iconbitmap('icon.ico')
except:
    ri=""
title=Label(text='_____________Tilesets / Spritesheets creation _____________')
title.place(x=2,y=2)

fichier=Label(text='Files: none')
fichier.place(x=2,y=30)

button = tk.Button(root, text='Upload images', command=upload,borderwidth=1)
button.place(x=2,y=52)

smb3=IntVar()
smb3_=tk.Checkbutton(root,text='SMB3 Style',variable=smb3,onvalue=1,offvalue=0,command=aff_size)
smb3_.place(x=77,y=80)

liste_sens=['Vertical','Horizontal']
sens=ttk.Combobox(values=liste_sens,width=9,state='readonly')
sens.set('Vertical')
sens.place(x=2,y=82)

liste_upscale=['x1','x2','x4','x8','x16','x32','x64']
upscale=ttk.Combobox(values=liste_upscale,width=3,state='readonly')
upscale.place(x=140,y=54)
upscale.set('x1')
upscale_=Label(text='Upscale:')
upscale_.place(x=90,y=54)
avert=Label()
avert.place(x=194,y=44)
upscale.bind("<<ComboboxSelected>>", lambda event:verif_size())
sens.bind("<<ComboboxSelected>>", lambda event:aff_size())

color=Button(text='Bakcground color',command=change_color,borderwidth=1)
color.place(x=2,y=132)

transparent=IntVar()
transparent_=Checkbutton(text='Transparent background',onvalue=1,offvalue=0,variable=transparent)
transparent_.place(x=105,y=133)

ts_size=Label(text='Tileset resolution (calculated if all sprites get the same size):')
ts_size.place(x=2,y=210)
hauteur_=Label(text='Height: 0px')
hauteur_.place(x=20,y=240)
largeur_=Label(text='Width: 0px')
largeur_.place(x=20,y=258)

filename_=Label(text='Name of file: ')
filename_.place(x=2,y=110)
liste_format=['.png','.jpeg','.jpg']
format=ttk.Combobox(values=liste_format,state='readolny',width=5)
format.place(x=200,y=110)
format.set('.png')
format_=Label()
format_.place(x=264,y=110)
filename=Entry(width=20,justify='right')
filename.place(x=75,y=110)
format.bind("<<ComboboxSelected>>", lambda event:format_f())

liste_fs=[]
for i in range(100):
    liste_fs.append(str(i))

path_=Button(text='Choose output folder',command=choose_path,borderwidth=1)
path_.place(x=558,y=2)
path__=Button(text='Open output folder',command=open_path,borderwidth=1)
path__.place(x=569,y=28)
bug_report=Button(text='Report a bug',borderwidth=1,command=lambda:webbrowser.open('https://github.com/Rhubarb06150/tileset_editor/discussions/2'))
bug_report.place(x=603,y=54)
idea_=Button(text='Suggest idea',borderwidth=1,command=lambda:webbrowser.open('https://github.com/Rhubarb06150/tileset_editor/discussions/4'))
idea_.place(x=604,y=80)
help_=Button(text='Need help?',borderwidth=1,command=lambda:webbrowser.open('https://github.com/Rhubarb06150/tileset_editor/discussions/categories/help'))
help_.place(x=612,y=106)
update=Button(text='Check for updates',borderwidth=1,command=lambda:update_check())
update.place(x=(root.winfo_width())-105,y=132)

root.bind("<Configure>", lambda event:place_buttons())

#RIP PART
title_=Label(text='______________________ Tileset ripping ________________________')
title_.place(x=2,y=280)
rip_button=Button(text='Rip in separated files',command=lambda:rip('rip'),borderwidth=1)
rip_button.place(x=10,y=450)
files_rip=Button(text='Upload image',command=upload_rip,borderwidth=1)
files_rip.place(x=2,y=300)
files_=Label(text='Files: none')
files_.place(x=88,y=302)

tile_size_l=['4px','8px','12px','16px','24px','32px','48px','56px','64px']
tile_size=ttk.Combobox(values=tile_size_l,width=4,state='readonly')
tile_size_=Label(text='Tile size:')
tile_size_.place(x=2,y=328)
tile_size.place(x=55,y=328)

tile_offset_l=['0px','1px','2px','3px','4px','5px','6px','7px','8px']
tile_offset=ttk.Combobox(values=tile_offset_l,width=3,state='readonly')
tile_offset_=Label(text='Tile offset:')
tile_offset_.place(x=2,y=350)
tile_offset.place(x=65,y=350)

dim_offset=[]
for i in range(1025):
    dim_offset.append(str(i)+'px')
dim_tile=[]
for i in range(999):
    dim_tile.append(str(i))

x_tile_offset=ttk.Combobox(values=dim_offset,width=3,state='readonly')
x_tile_offset_=Label(text='Begin offset x:')
x_tile_offset_.place(x=110,y=326)
x_tile_offset.place(x=194,y=326)

y_tile_offset=ttk.Combobox(values=dim_offset,width=3,state='readonly')
y_tile_offset_=Label(text='Begin offset y:')
y_tile_offset_.place(x=110,y=350)
y_tile_offset.place(x=194,y=350)

tile_name_=Label(text='Tiles name:')
tile_name_.place(x=2,y=372)
tile_name=Entry(justify='right',width=10)
tile_name.place(x=70,y=372)
tile_name_f=Label(text='.png')
tile_name_f.place(x=134,y=372)

x_tile=ttk.Combobox(values=dim_tile,width=3,state='readonly')
y_tile=ttk.Combobox(values=dim_tile,width=3,state='readonly')
x_tile_=Label(text='X:')
y_tile_=Label(text='Y:')
x_tile_.place(x=240,y=334)
y_tile_.place(x=304,y=334)
x_tile.place(x=256,y=334)
y_tile.place(x=320,y=334)
x_tile.set(0)
y_tile.set(0)

preview_e=IntVar()
preview=Checkbutton(text='Tile preview',variable=preview_e,onvalue=1,offvalue=0,command=lambda:rip('show_f'))
preview.place(x=2,y=420)

preview_=Label(root)
preview_.place(x=240,y=360)

x_tile_offset.set('0px')
y_tile_offset.set('0px')
tile_offset.set('0px')
tile_size.set('16px')

x_tile_offset.bind("<<ComboboxSelected>>", lambda event:rip('show_f'))
y_tile_offset.bind("<<ComboboxSelected>>", lambda event:rip('show_f'))
x_tile.bind("<<ComboboxSelected>>", lambda event:rip('show_f'))
y_tile.bind("<<ComboboxSelected>>", lambda event:rip('show_f'))
tile_offset.bind("<<ComboboxSelected>>", lambda event:rip('show_f'))
tile_size.bind("<<ComboboxSelected>>", lambda event:rip('show_f'))
y_tile.bind("<<ComboboxSelected>>", lambda event:rip('show_f'))

_upscale=ttk.Combobox(values=liste_upscale,width=3,state='readonly')
_upscale.place(x=52,y=394)
_upscale.set('x1')
_upscale_=Label(text='Upscale:')
_upscale_.place(x=2,y=394)

columns_list=['All']
for i in range(100):
    columns_list.append(str(i+1))
columns=ttk.Combobox(values=columns_list,width=3,state='readonly')
columns.place(x=426,y=334)
columns_=Label(text='Columns:')
columns_.place(x=364,y=334)
columns.set('All')

rows_list=['All']
for i in range(100):
    rows_list.append(str(i+1))
rows=ttk.Combobox(values=rows_list,width=3,state='readonly')
rows.place(x=426,y=304)
rows_=Label(text='Rows:')
rows_.place(x=364,y=304)
rows.set('All')

s_columns_list=[]
for i in range(100):
    s_columns_list.append(str(i+1))
s_columns=ttk.Combobox(values=s_columns_list,width=3,state='readonly')
s_columns.place(x=460,y=360)
s_columns_=Label(text='Starting column:')
s_columns_.place(x=364,y=360)
s_columns.set('1')
s_columns.bind("<<ComboboxSelected>>", lambda event:rip('show_f'))

bg_remove=Button(text='Background remove',borderwidth=1,command=lambda:eyedropper_win(liste_images_rip[0],colors_to_rm))
bg_remove.place(x=100,y=420)

final=Button(command=create,borderwidth=1,text='Create spritesheet')
final.place(x=50,y=170)

liste_gfx=[]
liste_nb=[]
for i in range(256):
    liste_nb.append(i+1)

liste_nb_gfx=[]
def max_gfx():
    global liste_nb_gfx
    liste_nb_gfx=[]
    for i in range(256):
        if (i+1) == int(gfx_nb.get()):
            liste_nb_gfx.append(i+1)
            break
        else:
            liste_nb_gfx.append(i+1)
    gfx_pr.configure(values=liste_nb_gfx)
    if int(gfx_pr.get())>int(gfx_nb.get()):
        gfx_pr.set(int(gfx_nb.get()))

gfx_title=Label(text='_____ GFX Expansion (Super Mario Bros. X) _____')
gfx_title.place(x=510,y=280)
gfx_nb_=Label(text='Number of GFXs:')
gfx_nb_.place(x=510,y=300)
gfx_nb=ttk.Combobox(values=liste_nb,width=5)
gfx_nb.place(x=608,y=300)
gfx_pr_=Label(text='GFX Preview:')
gfx_pr_.place(x=510,y=322)
gfx_pr=ttk.Combobox(values=liste_nb_gfx,width=5)
gfx_pr.place(x=586,y=322)
gfx_pr.set('1')
gfx_nb.set('1')

gfx_nb.bind("<<ComboboxSelected>>", lambda event:max_gfx())

if not os.path.exists('C:/tmp/'):
    os.mkdir('C:/tmp')
    msg=messagebox.showinfo(title='Hey',message="Your computer didn't have a C:/tmp/ folder so the software automatically created one, please don't delete it or it could cause issuses in the program.")

root.mainloop()