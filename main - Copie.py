import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog, ttk, colorchooser
from tkinter.colorchooser import askcolor
import PIL
from PIL import Image

liste_images=[]
def upload():
    global liste_images
    liste_images=[]
    filename = filedialog.askopenfilenames()
    fichier.configure(text=('Fichier: '+str(filename)))
    for i in filename:
        liste_images.append(i)

bg_color='#ffffff'
def change_color():
    global bg_color
    colors = askcolor(title="Choix de la couleur de fond")
    bg_color=(colors[1])

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
        
        if frame_skip.get()=='0':
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
                    img.save(folder_selected+'/'+str(filename.get())+format.get())
                    msg=messagebox.showinfo(title='Succes!',message=("Your tileset has been created\n as "+str(filename.get())+format.get()))
                else:
                    img.save('tilesets/'+str(filename.get())+format.get())
                    msg=messagebox.showinfo(title='Succes!',message=("Your tileset has been created\n as "+str(filename.get())+format.get()))
            except:
                if folder_selected != '':
                    img.save(folder_selected+'/tileset'+format.get())
                    msg=messagebox.showinfo(title='Hey',message="The filename was empty or contained illegal characters\nso your sheet were named 'tileset"+format.get()+"'")
                else:
                    img.save('tilesets/tileset'+format.get())
                    msg=messagebox.showinfo(title='Hey',message="The filename was empty or contained illegal characters\nso your sheet were named 'tileset"+format.get()+"'")
    except:
        msg=messagebox.showerror(title='Error',message="An error as occured! \n\n(please verify that you've been\nupload your images.)")

def verif_size():
    if upscale.get() == 'x16' or upscale.get() == 'x32' or upscale.get() == 'x64':
        avert.configure(text="Warning! too big upscale could lead to a crash,\n don't use big upscale if your computer can't handle it!")
    else:
        avert.configure(text="")

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
root.title('Tileset Creator')
root.resizable(False,False)
try:
    root.iconbitmap('icon.ico')
except:
    b=""
title=Label(text='Tileset Creator by Rhubarb06150')
title.place(x=2,y=2)

fichier=Label(text='Files: none')
fichier.place(x=2,y=20)

button = tk.Button(root, text='Upload images', command=upload,borderwidth=1)
button.place(x=2,y=42)

smb3=IntVar()
smb3_=Checkbutton(text='SMB3 Style',variable=smb3,onvalue=1,offvalue=0)
smb3_.place(x=77,y=70)

liste_sens=['Vertical','Horizontal']
sens=ttk.Combobox(values=liste_sens,width=9,state='readonly')
sens.set('Vertical')
sens.place(x=2,y=72)

liste_upscale=['x1','x2','x4','x8','x16','x32','x64']
upscale=ttk.Combobox(values=liste_upscale,width=3,state='readonly')
upscale.place(x=140,y=44)
upscale.set('x1')
upscale_=Label(text='Upscale:')
upscale_.place(x=90,y=44)
avert=Label()
avert.place(x=184,y=44)
upscale.bind("<<ComboboxSelected>>", lambda event:verif_size())

color=Button(text='Bakcground color',command=change_color,borderwidth=1)
color.place(x=2,y=122)

transparent=IntVar()

transparent_=Checkbutton(text='Transparent background',onvalue=1,offvalue=0,variable=transparent)
transparent_.place(x=105,y=123)

filename_=Label(text='Name of file: ')
filename_.place(x=2,y=100)
liste_format=['.png','.jpeg','.jpg']
format=ttk.Combobox(values=liste_format,state='readolny',width=5)
format.place(x=200,y=100)
format.set('.png')
format_=Label()
format_.place(x=254,y=100)
filename=Entry(width=20,justify='right')
filename.place(x=75,y=100)
format.bind("<<ComboboxSelected>>", lambda event:format_f())

liste_fs=[]
for i in range(100):
    liste_fs.append(str(i))

frame_skip=ttk.Combobox(values=liste_fs,state='readonly',width=3)
frame_skip.place(x=125,y=160)
frame_skip.set('0')
frame_skip_=Label(text='Frame skip:')
frame_skip_.place(x=55,y=160)

path=Button(text='Choose output folder',command=choose_path)
path.place(x=2,y=450)
path_=Label(text='Path: none (current directory)')
path_.place(x=128,y=452)

final=Button(command=create,borderwidth=1,text='Create')
final.place(x=10,y=160)

root.mainloop()