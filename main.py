import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, ttk, colorchooser
from tkinter.colorchooser import askcolor
import PIL
from PIL import Image,ImageTk
import os
import cv2
liste_images=[]
liste_images_rip=[]

def upload():
    global liste_images
    liste_images=[]
    filename = filedialog.askopenfilenames()
    fichier.configure(text=('Files: '+str(filename)))
    for i in filename:
        liste_images.append(i)
    aff_size()

def upload_rip():
    global liste_images_rip
    liste_images_rip=[]
    filename = filedialog.askopenfilename()
    files_.configure(text=('File: '+str(filename)))
    liste_images_rip.append(filename)

bg_color='#ffffff'
def change_color():
    global bg_color
    colors = askcolor(title="Choix de la couleur de fond")
    bg_color=(colors[1])

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

    try:
        with Image.open(liste_images[0]) as ima:
            w, h = ima.size
        if transparent.get()==1:
            img = Image.new('RGBA', (h,w), (255,255,255,0))
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
    try:
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

        if ty=='rip':
            a=0
            x=x_o
            y=y_o
            column=0
            fin=False
            while True:
                if (x+t_s)<=h:
                    img2=img.crop((x,y,(x+t_s),(y+t_s)))
                else:
                    fin=True
                    y+=t_s+t_o
                    x=x_o
                if (y+t_s)>=w:
                    y=w-t_s+y_o
                    x=x_o
                    print('derniere ligne')
                    for i in range(column):
                        img2=img.crop((x,y,x+t_s,y+t_s))
                        img2.save('tilesets/tiles/'+str(tile_name.get())+str(a+1)+'.png')
                        x+=t_s+t_o
                        a+=1
                    break
                if not fin:
                    column+=1
                print(column)
                img2=img.crop((x,y,(x+t_s),(y+t_s)))
                img2.save('tilesets/tiles/'+str(tile_name.get())+str(a+1)+'.png')
                x+=t_s+t_o
                a+=1
                if (a+1)%200 == 0:
                    msg=messagebox.askyesno(title='Warning!',message=(str(a+1)+' tiles were generated, \ndo you want to continue?'))
                    if not msg:
                        break
    
        elif ty=='show_f':
            if preview_e.get()==1:
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
                preview_.configure(image=None,borderwidth=0)
                preview_.im=None


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
    folder_selected = filedialog.askdirectory()
    path_.configure(text=('Path: '+str(folder_selected)))

def format_f():
    if format.get()!='.png':
        format_.configure(text='.jpeg and .jpg formats\ncauses a lot of quality loss')
    else:
        format_.configure(text='')

root=Tk()
root.geometry('680x480')
root.title('Tileset Editor')
root.resizable(False,False)
try:
    root.iconbitmap('icon.ico')
except:
    b=""
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

path=Button(text='Choose output folder',command=choose_path)
path.place(x=2,y=450)
path_=Label(text='Path: none (current directory)')
path_.place(x=128,y=452)

#RIP PART
title_=Label(text='______________________ Tileset ripping ________________________')
title_.place(x=2,y=280)
rip_button=Button(text='Rip in separated files',command=lambda:rip('rip'))
rip_button.place(x=100,y=420)
files_rip=Button(text='Upload image',command=upload_rip)
files_rip.place(x=2,y=300)
files_=Label(text='Files: none')
files_.place(x=88,y=302)

tile_size_l=['4px','8px','12px','16px','24px','32px','48px','64px']
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
for i in range(100):
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
tile_name_.place(x=2,y=378)
tile_name=Entry(justify='right',width=10)
tile_name.place(x=70,y=378)
tile_name_f=Label(text='.png')
tile_name_f.place(x=134,y=378)

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

final=Button(command=create,borderwidth=1,text='Create')
final.place(x=10,y=160)

root.mainloop()