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
animation_speed = 0.05
# SPEED OF CARS is "car_speed" times as fast as a pedestrian:
car_speed = 6
# LENGTH OF TRAM
tram_length = 8


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


def speed(agent):
    xspeed = 0
    yspeed = 0
    if agent.cordx < agent.endx:
        xspeed = 1
    if agent.cordx > agent.endx:
        xspeed = -1
    if agent.cordy < agent.endy:
        yspeed = 1
    if agent.cordy > agent.endy:
        yspeed = -1
    return xspeed, yspeed


def spawn_ped(walkers, i):
    # K: Start- und Endkoordinaten gemäss entsprechenden Agent-Quellen
    # S: Pedestrian(Weg)
    if i % random.randint(10, 40) == 0:
        walkers.append(Pedestrian("crosswalk_L_L"))
    if i % random.randint(50, 60) == 0:
        walkers.append(Pedestrian("crosswalk_L_R"))

    if i % random.randint(10, 40) == 0:
        walkers.append(Pedestrian("crosswalk_M_L"))
    if i % random.randint(10, 40) == 0:
        walkers.append(Pedestrian("crosswalk_M_R"))

    if i % random.randint(10, 40) == 0:
        walkers.append(Pedestrian("crosswalk_U_U"))
    if i % random.randint(10, 40) == 0:
        walkers.append(Pedestrian("crosswalk_U_B"))

    if i % random.randint(20, 40) == 0:
        walkers.append(Pedestrian("crosswalk_B_U"))
    if i % random.randint(20, 120) == 0:
        walkers.append(Pedestrian("crosswalk_B_B"))


def spawn_cars(drivers, i):
    # K: Start- und Endkoordinaten gemäss entsprechenden Agent-Quellen
    # S: Car(Weg)
    if i % random.randint(2, 5) == 0:
        drivers.append(Driver("car_L"))
    if i % random.randint(3, 4) == 0:
        drivers.append(Driver("car_R"))


def spawn_tram_raster(tram, str, raster):
    # Spawns the new tram in Raster and on Window
    agent = tram[-1]
    if str == 'vertical':
        for n in range(0, tram_length):
            # Spawn in Raster and on Window, vertically
            raster[agent.cordy_last + n * agent.yspeed][agent.cordx_last] = 3
            agent.tram_list.append(
                window.create_rectangle(agent.cordx * size + 3, (agent.cordy_last + n * agent.yspeed) * size,
                                        (agent.cordx + 1) * size + 2, (agent.cordy_last + n * agent.yspeed + 1) * size,
                                        fill='blue'))
    if str == 'horizontal':
        for n in range(0, tram_length):
            # Spawn in Raster and on Window, horizontally
            raster[agent.cordy_last][agent.cordx_last + n * agent.xspeed] = 3
            agent.tram_list.append(
                window.create_rectangle((agent.cordx_last + n * agent.xspeed) * size + 3, agent.cordy * size,
                                        (agent.cordx_last + n * agent.xspeed + 1) * size + 2, (agent.cordy + 1) * size,
                                        fill='blue'))


def spawn_tram(tram, i, raster):
    # K: Start- und Endkoordinaten gemäss entsprechenden Agent-Quellen
    # S: Tram(Weg)

    if i % 120 == 0:
        tram.append(Tram("6_Uni"))
        spawn_tram_raster(tram, "vertical", raster)

    if (i + 100) % 120 == 0:
        tram.append(Tram("6_Polybahn"))
        spawn_tram_raster(tram, "horizontal", raster)

    if (i + 80) % 120 == 0:
        tram.append(Tram("9_Uni"))
        spawn_tram_raster(tram, "vertical", raster)

    if (i + 60) % 120 == 0:
        tram.append(Tram("9_Haldenbach"))
        spawn_tram_raster(tram, "vertical", raster)

    if (i + 40) % 120 == 0:
        tram.append(Tram("10_Haldenbach"))
        spawn_tram_raster(tram, "vertical", raster)

    if (i + 20) % 120 == 0:
        tram.append(Tram("10_Polybahn"))
        spawn_tram_raster(tram, "horizontal", raster)


def iterate(list, raster):
    # A whole list gets updated => Each agent in that list gets to move (order: from first to last)
    # Returns if list is empty or not (True:= Empty)
    entities = len(list)
    iterator = 0

    # In case the list is empty
    if entities == 0:
        return True

    if isinstance(list[iterator], Tram):
        while iterator < entities:
            agent = list[iterator]
            finished = move_tram(agent, raster)
            if finished:
                # DELETES AGENT when he has arrived at destination
                # => Raster-entries gets set to 0, tram_list & List-entry get deleted, List-Length (entities) gets shorter by -1
                if agent.xspeed_last == 0:
                    for i in range(0, tram_length):
                        raster[agent.cordy_last + i * agent.yspeed_last][agent.cordx_last] = 0
                        window.delete(agent.tram_list[i])
                else:
                    for i in range(0, tram_length):
                        raster[agent.cordy_last][agent.cordx_last + i * agent.xspeed_last] = 0
                        window.delete(agent.tram_list[i])
                del (list[iterator])
                entities -= 1
            else:
                iterator += 1
    else:
        while iterator < entities:
            agent = list[iterator]
            finished = move(agent, raster)
            if finished:
                # DELETES AGENT when he has arrived at destination
                # => Raster-entry gets set to 0, Shape & List-entry get deleted, List-Length (entities) gets shorter by -1
                raster[agent.cordy][agent.cordx] = 0
                window.delete(agent.shape)
                del (list[iterator])
                entities -= 1
            else:
                iterator += 1
    return False


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

        # K: Determine Direction/Speed of agent
        self.xspeed, self.yspeed = speed(self)

        self.shape = window.create_oval(self.cordx * size + 3, self.cordy * size, self.cordx * size + size + 2,
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

        # K: Determine Direction/Speed of agent
        self.xspeed, self.yspeed = speed(self)

        self.shape = window.create_rectangle(self.cordx * size + 3, self.cordy * size, self.cordx * size + size + 2,
                                             self.cordy * size + size, fill='magenta')


class Tram:
    def __init__(self, number):
        # K: Initialisierung ggf ergänzen mit Startkoordinaten
        # K: Initialisiert ein Objekt der Klasse

        # Variable declaration:
        # The following trams stop at Eth/Universitätsspital:
        # 6, 9, 10
        # They either drive in the direction of 1. Polybahn, 2. Haldenbach or 3. Uni (Universität Zürich)

        # K: Dictionary für X-STARTkoordinate des Trams
        self.startposx = {
            '6_Uni': 65,
            '6_Polybahn': tram_length - 1,
            '9_Uni': 65,
            '9_Haldenbach': 64,
            '10_Haldenbach': 64,
            '10_Polybahn': tram_length - 1,
        }

        # K: Dictionary für Y-STARTkoordinate des Trams
        self.startposy = {
            '6_Uni': 99 - tram_length + 1,
            '6_Polybahn': 44,
            '9_Uni': 99 - tram_length + 1,
            '9_Haldenbach': tram_length - 1,
            '10_Haldenbach': tram_length - 1,
            '10_Polybahn': 44,
        }

        # K: Dictionary für X-STARTkoordinate des letzten Tramwaggons
        self.startposx_end = {
            '6_Uni': 65,
            '6_Polybahn': 0,
            '9_Uni': 65,
            '9_Haldenbach': 64,
            '10_Haldenbach': 64,
            '10_Polybahn': 0,
        }

        # K: Dictionary für Y-ENDkoordinate des letzten Tramwaggons
        self.startposy_end = {
            '6_Uni': 99,
            '6_Polybahn': 44,
            '9_Uni': 99,
            '9_Haldenbach': 0,
            '10_Haldenbach': 0,
            '10_Polybahn': 44,
        }

        # K: Dictionary für X-Middlekoordinate des Trams
        self.middleposx = {
            '6_Uni': 65,
            '6_Polybahn': 64,
            '9_Uni': 'no',
            '9_Haldenbach': 'no',
            '10_Haldenbach': 64,
            '10_Polybahn': 65,
        }

        # K: Dictionary für Y-Middlekoordinate des Cars
        self.middleposy = {
            '6_Uni': 43,
            '6_Polybahn': 44,
            '9_Uni': 'no',
            '9_Haldenbach': 'no',
            '10_Haldenbach': 43,
            '10_Polybahn': 44,
        }

        # K: Dictionary für X-ENDkoordinate des Trams
        self.endposx = {
            '6_Uni': 0,
            '6_Polybahn': 64,
            '9_Uni': 65,
            '9_Haldenbach': 64,
            '10_Haldenbach': 0,
            '10_Polybahn': 65,
        }

        # K: Dictionary für Y-ENDkoordinate des Trams
        self.endposy = {
            '6_Uni': 43,
            '6_Polybahn': 99,
            '9_Uni': 0,
            '9_Haldenbach': 99,
            '10_Haldenbach': 43,
            '10_Polybahn': 0,
        }

        # Saves agents number
        self.number = number

        # K: Start und Endpunkt wird zugeordnet, indem im entsprechenden dicionary der Wert ausgelesen wird
        self.startx = self.startposx[number]
        self.starty = self.startposy[number]
        self.startx_end = self.startposx_end[number]
        self.starty_end = self.startposy_end[number]
        # If change in direction => middleposition is an integer
        if self.middleposx[number] == "no":
            self.endx = self.endposx[number]
            self.endy = self.endposy[number]
        else:
            self.endx = self.middleposx[number]
            self.endy = self.middleposy[number]

        # K: Position of Agent
        self.cordx = self.startx
        self.cordy = self.starty
        self.cordx_last = self.startx_end
        self.cordy_last = self.starty_end

        # K: Determine Direction/Speed of agent
        self.xspeed, self.yspeed = speed(self)
        self.xspeed_last = self.xspeed
        self.yspeed_last = self.yspeed

        # K: Create a list of Tram Waggons; first waggon of tram at tram_list[-1] and last waggon at tram_list[0]
        self.tram_list = []

def rotlicht(number, matrix):

    if number == 0:
        #Keine Ampeln, alle Ampeln auf Grün
        return matrix
    if number == 1:
        matrix[40][33] = 3
        matrix[45][35] = 3
        #Fussgänger müssen warten
        #Matrix[x][y] = 3 für alle x,y welche direkt vor dem Fussgängerstreifen liegen aus Fussgänger sicht
        return matrix
    if number == 2:
        return matrix
        #Autos müssen warten:
        #matrix[x][y] = 4 für alle x,y Koordinaten, welche sich direkt vor Fussgängerstreifen befinden aus Sicht von Autofahrern

def move(agent, matrix):
    # Speichert die momentanen Koordinaten (old) sowie die Zukünftigen(new)
    xn_old = agent.cordx
    xn_new = agent.cordx + agent.xspeed
    ym_old = agent.cordy
    ym_new = agent.cordy + agent.yspeed

    # Falls die new-Koordinate in der Matrix unbesetzt ist, darf der Agent ein Feld weiter. Ansonsten bleibt er stehen.
    if matrix[ym_new][xn_new] == 0:
        matrix[ym_old][xn_old] = 0
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


def move_tram(agent, matrix):
    # Speichert Tram-Nummer
    number = agent.number

    # Returns True if Agent is at endposition & Changes speed if FIRST WAGGON is at the middleposition
    if agent.cordx == agent.endx and agent.cordy == agent.endy:
        if agent.cordx == agent.middleposx[number] and agent.cordy == agent.middleposy[number]:
            agent.endx = agent.endposx[number]
            agent.endy = agent.endposy[number]
            agent.xspeed, agent.yspeed = speed(agent)
        else:
            return True

    # Speichert die momentanen Koordinaten (old) sowie die Zukünftigen(new)
    xn_last = agent.cordx_last
    xn_new = agent.cordx + agent.xspeed
    ym_last = agent.cordy_last
    ym_new = agent.cordy + agent.yspeed

    # Changes speed if LAST WAGGON is at the middleposition
    if agent.cordx_last == agent.middleposx[number] and agent.cordy_last == agent.middleposy[number]:
        agent.endx_last = agent.endposx[number]
        agent.endy_last = agent.endposy[number]
        xspeed = 0
        yspeed = 0
        if agent.cordx_last < agent.endx_last:
            xspeed = 1
        if agent.cordx_last > agent.endx_last:
            xspeed = -1
        if agent.cordy_last < agent.endy_last:
            yspeed = 1
        if agent.cordy_last > agent.endy_last:
            yspeed = -1
        agent.xspeed_last = xspeed
        agent.yspeed_last = yspeed

    # Falls die new-Koordinate in der Matrix unbesetzt ist, darf der Agent ein Feld weiter. Ansonsten bleibt er stehen.
    if matrix[ym_new][xn_new] == 0:
        matrix[ym_last][xn_last] = 0
        matrix[ym_new][xn_new] = 3
        agent.cordx = xn_new
        agent.cordy = ym_new
        agent.cordx_last = xn_last + agent.xspeed_last
        agent.cordy_last = ym_last + agent.yspeed_last
        window.delete(agent.tram_list[0])
        del (agent.tram_list[0])
        agent.tram_list.append(window.create_rectangle(agent.cordx * size + 3, (agent.cordy) * size,
                                                       agent.cordx * size + size + 2,
                                                       (agent.cordy + 1) * size, fill='blue'))
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

# Variables, Arrays, Matrix for iteration
t_display = 0
walkers = []
drivers = []
tram = []
raster = initialize_gitter()

for i in range(9999):
    # Creates new agents in the lists (including random startingpoints)
    spawn_tram(tram, i, raster)
    spawn_ped(walkers, i)
    spawn_cars(drivers, i)

    # Updates Time in display window
    t_display += 1
    t_str = str(t_display)
    print_time(t_str)

    raster = rotlicht(1,raster)
    # Iterate all agents for one time period
    iterate(walkers, raster)
    i = 1
    while i <= car_speed:
        if i % 2: # Trams sind halb so schnell wie autos
            iterate(tram, raster)
        iterate(drivers, raster)

        tk.update()
        time.sleep(animation_speed)
        i += 1


tk.mainloop