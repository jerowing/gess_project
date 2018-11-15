# -*- coding: utf-8 -*-
from tkinter import *
import random
import time
from PIL import ImageTk, Image


# K: Inspiration zu grossen Teilen aus der Playlist:
# https://www.youtube.com/watch?v=lc8NNJgeVjI&index=12&list=PLsk-HSGFjnaGe7sS_4VpZoEtZF2VoWtoR

# K: globale Variabeln deklarieren
# K: width, height und size hier initialisieren, damit sie später von überall aufgerufen werden können.
WIDTH = 1000
HEIGHT = 1000
units = 100  # setzt Feinheit der Koordinaten fest
size = WIDTH / units
t_display = 0.1    # Time displayed in window


# Malt Raster für Koordinatensystem (don't touch!!)
def schachbrett(canvas):
    count = units
    for x in range(WIDTH):
        canvas.create_line(WIDTH / count * x, 0, WIDTH / count * x, HEIGHT, fill="#476042")
    for y in range(HEIGHT):
        canvas.create_line(0, HEIGHT / count * y, WIDTH, HEIGHT / count * y, fill="#476042")


# TODO: Funktion, welche Richtung wechselt sobald zwei Objekte crashen
# Meine Idee (Jérôme): Array erstellen und Koordinaten eintragen, welche besetzt sind
# so muss nicht jedes Objekt mit allen anderen Objekten abgeglichen werden.

# TODO: Funktion, welche einem Objekt ein Ziel mitgibt und Objekt so steuert, dass es sich richtung Zielkoordinaten bewegt
# Problem: Wie definieren wir Koordinaten eines Objektes? (Momentan ist Objekt über 4 "Randpunkte" definiert
# Meine Idee (Jérôme): Erste Version -> anhalten sobald Zielkoordinaten erreicht
# Später: gezielt richtung Ziel bewegen





def initialize_gitter():
    # Initialisiert Koordinatenmatrix mit Nullen-Einträgen
    matrix = [[0 for x in range(units)] for y in range(units)]
    return matrix


def print_matrix(matrix):
    # K: Funktioniert nur für Matrizen mit Höhe height
    # K: Grenze so anpassen, dass beliebige Matrizen verwendet werden können?
    print("Matrixprinter")
    # print("width ", len(matrix[0]), "height ", len(matrix))
    for i in range(len(matrix)):
        print(matrix[i])


class Pedestrian:
    def __init__(self, path):
        # K: Initialisierung ggf ergänzen mit Startkoordinaten
        # K: Initialisiert ein Objekt der Klasse

        # Variable declaration for Crosswalks
        #    crosswalk_L_L  very left crosswalk (see map) and left lane
        #    crosswalk_L_R  very left crosswalk / right lane
        #    crosswalk_M_L  middle crosswalk / left lane
        #    crosswalk_M_R  middle crosswalk / right lane
        #    crosswalk_U_U  upper crosswalk / upper lane
        #    crosswalk_U_B  upper crosswalk / bottom lane
        #    crosswalk_B_U  bottom crosswalk / upper lane
        #    crosswalk_B_B  bottom crosswalk / bottom lane

        # K: Dictionary für x-Startkoordinate des Fussgängers
        self.startposx = {
            'crosswalk_L_L': 33,
            'crosswalk_L_R': 35,
            'crosswalk_M_L': 56,
            'crosswalk_M_R': 58,
            'crosswalk_U_U': 69,
            'crosswalk_U_B': 59,
            'crosswalk_B_U': 69,
            'crosswalk_B_B': 59
        }

        # K: Dictionary für y-Startkoordinate des Fussgängers
        self.startposy = {
            'crosswalk_L_L': 38,
            'crosswalk_L_R': 48,
            'crosswalk_M_L': 38,
            'crosswalk_M_R': 48,
            'crosswalk_U_U': 37,
            'crosswalk_U_B': 39,
            'crosswalk_B_U': 67,
            'crosswalk_B_B': 69
        }

        # K: Dictionary für x-Endkoordinate des Fussgängers
        self.endposx = {
            'crosswalk_L_L': 33,
            'crosswalk_L_R': 35,
            'crosswalk_M_L': 56,
            'crosswalk_M_R': 58,
            'crosswalk_U_U': 59,
            'crosswalk_U_B': 69,
            'crosswalk_B_U': 59,
            'crosswalk_B_B': 69
        }

        # K: Dictionary für y-Endkoordinate des Fussgängers
        self.endposy = {
            'crosswalk_L_L': 48,
            'crosswalk_L_R': 38,
            'crosswalk_M_L': 48,
            'crosswalk_M_R': 38,
            'crosswalk_U_U': 37,
            'crosswalk_U_B': 39,
            'crosswalk_B_U': 67,
            'crosswalk_B_B': 69
        }

        # K: Start und Endpunkt wird zugeordnet, indem im entsprechenden dicionary der Wert ausgelesen wird
        self.startx = self.startposx[path]
        self.starty = self.startposy[path]
        self.endx = self.endposx[path]
        self.endy = self.endposy[path]

        # K: Position of Agent
        self.cordx = self.startx
        self.cordy = self.starty

        #self.xspeed = random.randint(-1, 1)
        #self.yspeed = random.randint(-1, 1)

        self.shape = window.create_oval(self.cordx * size, self.cordy * size, self.cordx * size + size,
                                        self.cordy * size + size, fill='green')


class Driver:
    def __init__(self, color):
        # K: Initialisierung ggf ergänzen mit Startkoordinaten
        # K: Initialisiert ein Objekt der Klasse

        # K: Start und Endpunkt
        self.startx =  random.randint(1,units)
        self.starty = random.randint(1,units)
        self.endx = random.randint(1,units)
        self.endy = random.randint(1,units)

        # K: Position of Agent
        self.cordx= self.startx
        self.cordy= self.starty

        self.xspeed = 0
        self.yspeed = 0
        self.shape = window.create_rectangle(self.cordx * size, self.cordy * size, self.cordx * size + size,
                                             self.cordy * size + size, fill='magenta')


def move(agent, matrix):

    # K: Berechnet Koordinaten im Koordinatensystem
    if agent.cordx<agent.endx:
        agent.cordx += 1
        agent.xspeed = 1

    if agent.cordx>agent.endx:
        agent.cordx -= 1
        agent.xspeed = -1

    if agent.cordx==agent.endx:
        agent.xspeed= 0

    if agent.cordy<agent.endy:
        agent.cordy += 1
        agent.yspeed = 1

    if agent.cordy>agent.endy:
        agent.cordy -= 1
        agent.yspeed = -1

    if agent.cordy==agent.endy:
        agent.yspeed=0

    # K: Bewegt ein Objekt im Fenster
    window.move(agent.shape, agent.xspeed * size, agent.yspeed * size)


    # Berechnet Koordinaten im Koordinatensystem
    x = agent.cordx
    y = agent.cordy

    # K: Verhindert, dass Bälle den Rahmen verlassen
    if y >= (units - 1) or y <= 0:
        agent.yspeed = -agent.yspeed
    if x >= (units - 1) or x <= 0:
        agent.xspeed = -agent.xspeed

    # Füllt Position in die Matrix
    if (x >= units) or (x < 0) or (y >= units) or (y < 0):
        # Ist es möglich, dass Bälle den Rahmen verlassen?
        outofrange = 1
    else:
        matrix[x][y] += 1
        return matrix


def print_time(t):
    """ updates the current time displayed in the window"""
    current_time = Label(window, text=t)
    current_time.place(x=105, y=WIDTH-50)


# ------------------------------------------ Beginn "Main function" -------------------------------------------


# K: öffnet neues Fenster und initialisiert Koordinatenraster
tk = Tk()
window = Canvas(tk, width=WIDTH, height=HEIGHT)
schachbrett(window)
tk.title("simulation_try1")
window.pack()

# K: Time display box
time_label = Label(window, text="Time elapsed: ")
time_label.place(x=10, y=WIDTH - 50)

# K: sets the map in the background
img = Image.open('map.gif')
backgr = ImageTk.PhotoImage(img)
canvas_img = window.create_image(503, 500, image=backgr)


walkers = []
drivers = []



for i in range(9999):
    # Füllt n*3 Bälle in Liste
    # K: Start- und Endkoordinaten gemäss entsprechenden Agent-Quellen
    # S: Pedestrian(Weg)
    if i%random.randint(99,100) == 0:
        walkers.append(Pedestrian("crosswalk_L_L"))
    if i%random.randint(50,60) == 0:
        walkers.append(Pedestrian("crosswalk_L_R"))

    if i%random.randint(100,200) == 0:
        walkers.append(Pedestrian("crosswalk_M_L"))
    if i%random.randint(100,150) == 0:
        walkers.append(Pedestrian("crosswalk_M_R"))

    if i%random.randint(100,200) == 0:
        walkers.append(Pedestrian("crosswalk_U_U"))
    if i%random.randint(900,1000) == 0:
        walkers.append(Pedestrian("crosswalk_U_B"))

    if i%random.randint(20,40) == 0:
        walkers.append(Pedestrian("crosswalk_B_U"))
    if i%random.randint(80,120) == 0:
        walkers.append(Pedestrian("crosswalk_B_B"))

    if i%random.randint(80,1000) == 0:
        drivers.append(Driver("red"))

    # Updates Time in display window
    t_display += 1
    t_str = str(t_display)
    print_time(t_str)

    # K: lässt Ball im Fenster herumfliegen, so dass er an den Wänden abprallt
    # balls.append(Ball("magenta", 100))
    # balls.append(Ball("blue", 100))
    raster = initialize_gitter()
    for ped in walkers:
        move(ped, raster)
    for car in drivers:
        move(car, raster)
    tk.update()




'''for i in range(9999):
    # Füllt n*3 Bälle in Liste
    # K: Start- und Endkoordinaten gemäss entsprechenden Agent-Quellen
    # S: Pedestrian(Weg)
    if i%7 == 0:
        walkers.append(Pedestrian("crosswalk_L_L"))
    if i%3 == 0:
        walkers.append(Pedestrian("crosswalk_L_R"))
    if i%9 == 0:
        walkers.append(Pedestrian("crosswalk_M_L"))
    if i%12 == 0:
        walkers.append(Pedestrian("crosswalk_M_R"))
    if i%99 == 0:
        drivers.append(Driver("red"))
    # balls.append(Ball("green", 0))
    # balls.append(Ball("black", 0))

while True:
    # Updates Time in display window
    t_display += 1
    t_str = str(t_display)
    print_time(t_str)

    # K: lässt Ball im Fenster herumfliegen, so dass er an den Wänden abprallt
    # balls.append(Ball("magenta", 100))
    # balls.append(Ball("blue", 100))
    raster = initialize_gitter()
    for ped in walkers:
        move(ped, raster)
    for car in drivers:
        move(car, raster)
    tk.update()'''

    # schnelligkeit der Animation wird hier festgelegt

    # print_matrix(raster)

tk.mainloop