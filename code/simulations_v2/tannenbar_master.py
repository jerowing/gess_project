from tkinter import *
import random
import time

# K: Inspiration zu grossen Teilen aus der Playlist:
# https://www.youtube.com/watch?v=lc8NNJgeVjI&index=12&list=PLsk-HSGFjnaGe7sS_4VpZoEtZF2VoWtoR

# K: globale Variabeln deklarieren
# K: width, height und size hier initialisieren, damit sie später von überall aufgerufen werden können.
WIDTH = 1000
HEIGHT = 1000
units = 100 # setzt Feinheit der Koordinaten fest
size = WIDTH / units


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
    def __init__(self, color):
        # K: Initialisierung ggf ergänzen mit Startkoordinaten
        # K: Initialisiert ein Objekt der Klasse
        self.cordx = 3
        self.cordy = 0
        self.xspeed = 0
        self.yspeed = 1
        self.shape = window.create_oval(self.cordx * size, self.cordy * size, self.cordx * size + size,
                                        self.cordy * size + size, fill=color)


class Driver:
    def __init__(self, color):
        # K: Initialisierung ggf ergänzen mit Startkoordinaten
        # K: Initialisiert ein Objekt der Klasse
        self.cordx = random.randint(1, units)
        self.cordy = random.randint(1, units)
        self.xspeed = 1
        self.yspeed = 0
        self.shape = window.create_rectangle(self.cordx * size, self.cordy * size, self.cordx * size + size,
                                             self.cordy * size + size, fill=color)


def move(agent, matrix):
    # K: Bewegt ein Objekt im Fenster
    window.move(agent.shape, agent.xspeed * size, agent.yspeed * size)

    # Berechnet Koordinaten im Koordinatensystem
    agent.cordx += agent.xspeed
    agent.cordy += agent.yspeed
    x = agent.cordx
    y = agent.cordy

    # K: Verhindert, dass Bälle den Rahmen verlassen
    if y >= (units) or y < 0:
        agent.yspeed = -agent.yspeed
    if x >= (units - 1) or x < 0:
        agent.xspeed = -agent.xspeed

    # Füllt Position in die Matrix
    if (x >= units) or (x < 0) or (y >= units) or (y < 0):
        # Ist es möglich, dass Bälle den Rahmen verlassen?
        outofrange = 1
    else:
        if matrix[x][y] == 0:
            if isinstance(agent, Driver):
                matrix[x][y] = 2
            if isinstance(agent, Pedestrian):
                matrix[x][y] = 1
        else:
            #Macht Zug rückgängig, so dass sich der Agent nicht bewegt
            agent.cordx -= agent.xspeed
            agent.cordy -= agent.yspeed
            window.move(agent.shape, -agent.xspeed * size, - agent.yspeed * size)


###
# Beginn "Main function"
###

# K: öffnet neues Fenster und initialisiert Koordinatenraster
tk = Tk()
window = Canvas(tk, width=WIDTH, height=HEIGHT)
schachbrett(window)
tk.title("simulation_try1")
window.pack()

walkers = []
drivers = []
for i in range(30):
    # Füllt n*3 Bälle in Liste
    # K: startkoordinaten so verteilt, dass sie "zufällig" im Raum verteilt sind zu beginn
    # S: Ball(farbe, startkoordinaten)
    walkers.append(Pedestrian("green"))
    walkers.append(Pedestrian("magenta"))
    walkers.append(Pedestrian("yellow"))
    drivers.append(Driver("red"))
    # balls.append(Ball("green", 0))
    # balls.append(Ball("black", 0))

raster_new = initialize_gitter()
raster_old = initialize_gitter()
while True:
    # K: lässt Ball im Fenster herumfliegen, so dass er an den Wänden abprallt
    # balls.append(Ball("magenta", 100))
    # balls.append(Ball("blue", 100))
    for ped in walkers:
        move(ped, raster_new)
    for car in drivers:
        move(car, raster_new)
    tk.update()
    #print_matrix(raster_old)
    raster_new  = initialize_gitter()
    raster_old = raster_new

    # schnelligkeit der Animation wird hier festgelegt
    time.sleep(0.1)


tk.mainloop
