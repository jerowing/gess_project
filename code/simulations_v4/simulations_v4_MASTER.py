# -*- coding: utf-8 -*-
from tkinter import *
from numpy import *
import random
import time
from PIL import ImageTk, Image

# K: GLOBAL VARIABLES
# Height/Width of window:
LENGTH = 1000
# Squares horizontally/vertically:
units = 100
# Sidelength of squares:
size = LENGTH / units
# SPEED OF ANIMATION:
animation_speed = 1
# SPEED OF CARS is "car_speed" times as fast as a pedestrian:
car_speed = 4


# Malt Raster für Koordinatensystem (don't touch!!)
def schachbrett(canvas):
    for x in range(LENGTH):
        canvas.create_line(size * x, 0, size * x, LENGTH, fill="#476042")
    for y in range(LENGTH):
        canvas.create_line(0, size * y, LENGTH, size * y, fill="#476042")


def initialize_gitter():
    # Initialisiert Koordinatenmatrix mit Nullen-Einträgen
    matrix = array(zeros((units, units)), dtype=int)
    return matrix


def print_matrix(matrix):
    # K: Funktioniert nur für Matrizen mit Höhe height
    # K: Grenze so anpassen, dass beliebige Matrizen verwendet werden können?
    print("Matrixprinter at time: ", t_display)
    print(matrix)


def spawn_ped(walkers, i):
    # K: Start- und Endkoordinaten gemäss entsprechenden Agent-Quellen
    # S: Pedestrian(Weg)
    if i % random.randint(1, 4) == 0:
        walkers.append(Pedestrian("crosswalk_L_L"))
    if i % random.randint(50, 60) == 0:
        walkers.append(Pedestrian("crosswalk_L_R"))

    if i % random.randint(10, 20) == 0:
        walkers.append(Pedestrian("crosswalk_M_L"))
    if i % random.randint(8, 12) == 0:
        walkers.append(Pedestrian("crosswalk_M_R"))

    if i % random.randint(4, 6) == 0:
        walkers.append(Pedestrian("crosswalk_U_U"))
    if i % random.randint(5, 10) == 0:
        walkers.append(Pedestrian("crosswalk_U_B"))

    if i % random.randint(20, 40) == 0:
        walkers.append(Pedestrian("crosswalk_B_U"))
    if i % random.randint(20, 120) == 0:
        walkers.append(Pedestrian("crosswalk_B_B"))


def spawn_cars(drivers, i):
    # K: Start- und Endkoordinaten gemäss entsprechenden Agent-Quellen
    # S: Car(Weg)
    if i % random.randint(5, 20) == 0:
        drivers.append(Driver("car_L"))
    if i % random.randint(4, 9) == 0:
        drivers.append(Driver("car_R"))


def iterate(list, matrix):
    # A whole list gets updated => Each agent in that list gets to move (order: from first to last)
    entities = len(list)
    iterator = 0
    while iterator < entities:
        finished = move(list[iterator], matrix)
        if finished:
            window.delete(list[iterator].shape)
            del (list[iterator])
            entities -= 1
        else:
            iterator += 1
    return matrix


class Pedestrian:
    def __init__(self, path):
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

        self.shape = window.create_oval(self.cordx * size, self.cordy * size, self.cordx * size + size,
                                        self.cordy * size + size, fill='green')


class Driver:
    def __init__(self, path):
        # K: Initialisierung ggf ergänzen mit Startkoordinaten
        # K: Initialisiert ein Objekt der Klasse

        # Variable declaration:
        #    car_L car      driving on the left lane -> upwards
        #    car_R car      driving on the right lane -> downwards
        #    car_left_turn   driving on the left lane until crossroad then left turn

        # K: Dictionary für X-STARTkoordinate des Cars
        self.startposx = {
            'car_L': 63,
            'car_R': 66,
            'car_left_turn': 0
        }

        # K: Dictionary für Y-STARTkoordinate des Cars
        self.startposy = {
            'car_L': 0,
            'car_R': 99,
            'car_left_turn': 0
        }

        # K: Dictionary für X-ENDkoordinate des Cars
        self.endposx = {
            'car_L': 63,
            'car_R': 66,
            'car_left_turn': 55
        }

        # K: Dictionary für Y-ENDkoordinate des Cars
        self.endposy = {
            'car_L': 99,
            'car_R': 0,
            'car_left_turn': 0
        }

        # K: Start und Endpunkt
        self.startx = self.startposx[path]
        self.starty = self.startposy[path]
        self.endx = self.endposx[path]
        self.endy = self.endposy[path]

        # K: Position of Agent
        self.cordx= self.startx
        self.cordy= self.starty

        #self.xspeed = 0
        #self.yspeed = 0
        self.shape = window.create_rectangle(self.cordx * size, self.cordy * size, self.cordx * size + size,
                                             self.cordy * size + size, fill='magenta')


def move(agent, matrix):

    # K: Berechnet Richtung (Speed) des Agents
    if agent.cordx < agent.endx:
        agent.xspeed = 1
    if agent.cordx > agent.endx:
        agent.xspeed = -1
    if agent.cordy < agent.endy:
        agent.yspeed = 1
    if agent.cordy > agent.endy:
        agent.yspeed = -1
    if agent.cordx == agent.endx:
        agent.xspeed = 0
    if agent.cordy == agent.endy:
        agent.yspeed = 0

    # Speichert die momentanen Koordinaten (old) sowie die Zukünftigen(new)
    xn_old = agent.cordx
    xn_new = agent.cordx + agent.xspeed
    ym_old = agent.cordy
    ym_new = agent.cordy + agent.yspeed

    # Falls die new-Koordinate in der Matrix unbesetzt ist, darf der Agent ein Feld weiter. Ansonsten bleibt er stehen.
    if matrix[ym_new][xn_new] != 0:
        if isinstance(agent, Driver):
            matrix[ym_old][xn_old] = 2
        if isinstance(agent, Pedestrian):
            matrix[ym_old][xn_old] = 1
    else:
        if isinstance(agent, Driver):
            matrix[ym_new][xn_new] = 2
        if isinstance(agent, Pedestrian):
            matrix[ym_new][xn_new] = 1
        agent.cordx = xn_new
        agent.cordy = ym_new
        window.move(agent.shape, agent.xspeed * size, agent.yspeed * size)

    # Returns True if Agent is at endposition
    if agent.cordx == agent.endx and agent.cordy == agent.endy:
        return True
    else:
        return False


def print_time(t):
    """ updates the current time displayed in the window"""
    current_time = Label(window, text=t)
    current_time.place(x=145, y=50)


# ------------------------------------------ Beginn "Main function" -------------------------------------------


# K: öffnet neues Fenster und initialisiert Koordinatenraster
tk = Tk()
window = Canvas(tk, width=LENGTH, height=LENGTH)
schachbrett(window)
tk.title("simulation_try1")
window.pack()

# K: Time display box
time_label = Label(window, text="Time elapsed: ")
time_label.place(x=50, y=50)

# K: sets the map in the background
img = Image.open('map_nico.gif')
backgr = ImageTk.PhotoImage(img)
canvas_img = window.create_image(503, 500, image=backgr)

# Variables
t_display = 0
walkers = []
drivers = []

for i in range(9999):
    # Creates new agents in the lists (including random startingpoints)
    spawn_ped(walkers, i)
    spawn_cars(drivers, i)

    # Updates Time in display window
    t_display += 1
    t_str = str(t_display)
    print_time(t_str)

    # Iterate all agents for one time period
    raster_new = initialize_gitter()
    raster_new = iterate(walkers, raster_new)
    i = 1
    while i <= car_speed:
        raster_new = iterate(drivers, raster_new)
        tk.update()
        time.sleep(animation_speed)
        i += 1
    raster_old = raster_new

    print_matrix(raster_new[:, 63])



tk.mainloop