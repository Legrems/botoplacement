from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from PIL import Image
import math
import random

from find_place import *

class Position():
    def __init__(self, x, y = ''):
        self.x = x
        if y == '':
            self.y = self.x
        else:
            self.y = y

    def moyenne(self, pos):
        return Position((self.x + pos.x) / 2, (self.y + pos.y) / 2)

    def box(self, pos):
        return (self.x, self.y, pos.x, pos.y)

def newImage(filepath):
    print(filepath)

    image = PhotoImage(file = filepath)

    print('{}x{}'.format(image.width(), image.height()))
    image = image.subsample(1, 1)

    gifdict[filepath] = image
    
    #image_label = Label(window, image = image)
    #image_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
    canva.create_image(0, 0, anchor = NW, image = image)
    canva.config(height = image.height(), width = image.width())

    window.title('Image {}x{}'.format(image.height(), image.width()))
    print(gifdict)

def rawList(filepath):
    formatted = open("formatted.py", "w")
    file = open(filepath, 'r')
    read = file.read()
    file.close()

    line = read.split('\n')
    print(line)

    formatted.write('teams = [\n')
    j = 0
    for i in line:
        j += 1
        i = i[5:][::-1][14:][::-1]
        t = i.split('/')
        nbmax = int(t[-1])
        t = t[::-1][1].split(' ')
        nbplaced = int(t[-1])
        team = i[:i.find('has')-1]
        if team == '':
            team = 'ALONE'
        print('{}: {} / {}'.format(team, nbplaced, nbmax))
        formatted.write('\t[{:>2}, {:>2}, "{}"],\n'.format(j, nbmax, team))
    formatted.write(']')
    formatted.close()
    print('formatted.py writted, format done !')

def openImage():
    filepath = tkinter.filedialog.askopenfilename(title = 'Open the plan', filetypes = [('png files','.png'), ('all files','.*')])
    newImage(filepath)

def openRawList():
    filepath = tkinter.filedialog.askopenfilename(title = 'Open raw list', filetypes = [('txt files','.txt'), ('all files','.*')])
    rawList(filepath) 

def closeImage():
    canva.delete(ALL)
    gifdict = {}
    window.title('Image')

def Apropos():
    tkinter.messagebox.showinfo("A propos","Placement @ Gremaud Loïc v0.1.1447E2")

def createLine(plane):
    offset = Position(30, 30)
    ligneW = math.floor((720 - 2 * offset.x) / len(plane))
    ligneH = math.floor((960 - 2 * offset.y) / 34)
    ligneW = min(ligneW, ligneH)
    print(ligneW)
    ligneW = 20
    for i in range(len(plane)):
        for j in range(len(plane[i][1:])):
            for k in range(plane[i][j + 1][0]):
                print('{} - {} - {}'.format(i,j,k))
                posa = Position(offset.x + ligneW * plane[i][0], offset.y + ligneW * k)
                posb = Position(posa.x + ligneW, posa.y + ligneW)
                posm = posb.moyenne(posa)
                canva.create_rectangle(posa.box(posb))
                #canva.create_text(posm.x, posm.y, text = 'X')
        
def clic(event):
    global DETECTION_CLIC

    if last_event and last_event[-1][1] == event.x and last_event[-1][2] == event.y:
        last_event[-1][0] = 'double click'
        print('Position du double click : ({}, {})'.format(event.x, event.y))
        doubleclick(event)
    else:
        last_event.append(['click', event.x, event.y])
        print('Position du click : ({}, {})'.format(event.x, event.y))
    #print(last_event)

def doubleclick(event):
    for i in gifdict:
        image = Image.open(i)
        print(image.getpixel((event.x, event.y)))
        getBoxWithColor(event.x, event.y)

def new(event):
    dragged.append(canva.create_rectangle(event.x, event.y, event.x + 10, event.y + 10, width = 2))
    print('Created new rectangle !')

def drag(event):
    if dragged != []:
        oldPos = canva.coords(dragged[-1])
        print(oldPos)
        canva.coords(dragged[-1], oldPos[0], oldPos[1], event.x, event.y)

def getBoxWithColor(x, y):
    canva.delete('boxed')
    for i in gifdict:
        image = Image.open(i)
        color = image.getpixel((x, y))
        idx = [0,0,0,0]
        for i in range(len(idx)):
            exit = False
            while not exit:
                if color == image.getpixel((x + idx[0] * (i == 0) - idx[1] * (i == 1), y + idx[2] * (i == 2) - idx[3] * (i == 3))):
                    idx = [idx[j] + 1 * (i == j) for j in range(len(idx))]
                else:
                    exit = True
        print(idx)
        canva.create_rectangle(x - idx[1], y - idx[3], x + idx[0], y + idx[2], width=2, tags='boxed')
    getAllTable(idx[0] + idx[1], idx[2] + idx[3])

def getAllTable(w, l):
    global gifdict
    for i in gifdict: 
        doWhatYouHaveToDo(i, [w + 1, l + 1, 0])
    gifdict = {}
    newImage('res.png')

def openWindow(event):
    t = tkinter.Toplevel()
    t.wm_title("Window")
    l = tkinter.Label(t, text="This is window")
    l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    mb = Menu(t)
    mp = Menu(mb, tearoff=0)
    mp.add_command(label="Import raw list", command=Apropos)
    mb.add_cascade(label="Player", menu=mp)

    t.config(menu = mb)

window = Tk()
window.title('Gestionnaire de placement')

menubar = Menu(window)

menufile = Menu(menubar, tearoff=0)
menufile.add_command(label="Ouvrir une image", command=openImage)
menufile.add_command(label="Fermer l'image", command=closeImage)
menufile.add_command(label="Quitter", command=window.destroy)
menubar.add_cascade(label="Fichier", menu=menufile)

menuhelp = Menu(menubar, tearoff=0)
menuhelp.add_command(label="A propos", command=Apropos)
menubar.add_cascade(label="Aide", menu=menuhelp)

menuplayer = Menu(menubar, tearoff=0)
menuplayer.add_command(label="Import raw list", command=openRawList)
menubar.add_cascade(label="Player", menu=menuplayer)

window.config(menu = menubar)

gifdict = {}
last_event = []

w = 480
h = 360

canva = Canvas(window, width=w, height=h, bg='white')
#createLine(plan)

dragged = []
table = []

canva.bind('<Button-1>', clic)
canva.bind('<Button-3>', new)
canva.bind('<B1-Motion>', drag)

canva.pack()

window.mainloop()