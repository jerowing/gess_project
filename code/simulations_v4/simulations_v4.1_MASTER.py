# -*- coding: utf-8 -*-
from tkinter import *
from numpy import *
import random
import time
from PIL import ImageTk, Image
import csv

""" ---------------------------------------------- GLOBAL VARIABLES --------------------------------------------- """

# Height/Width of window:
LENGTH = 1000
# Squares horizontally/vertically:
units = 100
# Sidelength of squares:
size = LENGTH / units
# SPEED OF ANIMATION:
animation_speed = 0.01
maxspeed = True

# SPEED OF CARS is "car_speed" times as fast as a pedestrian:
car_speed = 6
# LENGTH OF TRAM
tram_length = 8

# Trafficlight: complete iteration time; green-light-time for cars
variante_ampeln = True
light_phase = 40
car_phase = 25

# Variance of time of the day:
# [1 = 08:00]
# [2 = 12:00]
# [3 = 17:00]
# [4 = 20:00]
variante_zeiten = 1

# TIME DISPLAY
t_s = 0
t_min = 0
t_h = 0

# PEDESTRIANS WAITING
waiting_ped = {'time_t': 0, 'crosswalk_L_L': 0, 'crosswalk_L_R': 0,
               'crosswalk_M_L': 0, 'crosswalk_M_R': 0, 'crosswalk_U_U': 0,
               'crosswalk_U_B': 0, 'crosswalk_B_U': 0, 'crosswalk_B_B': 0,
               'cars_L': 0, 'cars_R': 0}

waiting_ped2 = {'time': waiting_ped['time_t'],
                'crosswalk_L': waiting_ped['crosswalk_L_R'] + waiting_ped['crosswalk_L_L'],
                'crosswalk_R': waiting_ped['crosswalk_M_L'] + waiting_ped['crosswalk_M_R'],
                'crosswalk_U': waiting_ped['crosswalk_U_U'] + waiting_ped['crosswalk_U_B'],
                'crosswalk_B': waiting_ped['crosswalk_B_B'] + waiting_ped['crosswalk_B_U'],
                'cars_L': waiting_ped['cars_L'], 'cars_R': waiting_ped['cars_R']}


""" ---------------------------------------------- FUNCTION DECLARATIONS ---------------------------------------- """

def spawning_frequency(variante_zeiten):
    if variante_zeiten == 1:
        # 08:00 [Chance, Amount] of Pedestrians/Cars spawned (per second)
        amount_ped = {'crosswalk_L_L': [20, 2], 'crosswalk_L_R': [20, 1],
                      'crosswalk_M_L': [25, 2], 'crosswalk_M_R': [15, 1], 'crosswalk_U_U': [25, 2],
                      'crosswalk_U_B': [15, 1], 'crosswalk_B_U': [10, 1], 'crosswalk_B_B': [10, 1]}
        amount_car = {'car_L': [10, 2], 'car_R': [10, 2]}

    if variante_zeiten == 2:
        # 12:00 [Chance, Amount] of Pedestrians/Cars spawned (per second)
        amount_ped = {'crosswalk_L_L': [15, 1], 'crosswalk_L_R': [15, 1],
                      'crosswalk_M_L': [10, 2], 'crosswalk_M_R': [10, 2], 'crosswalk_U_U': [15, 2],
                      'crosswalk_U_B': [15, 2], 'crosswalk_B_U': [10, 1], 'crosswalk_B_B': [10, 1]}
        amount_car = {'car_L': [25, 2], 'car_R': [25, 2]}

    if variante_zeiten == 3:
        # 17:00 [Chance, Amount] of Pedestrians/Cars spawned (per second)
        amount_ped = {'crosswalk_L_L': [15, 1], 'crosswalk_L_R': [15, 1],
                      'crosswalk_M_L': [10, 2], 'crosswalk_M_R': [10, 2], 'crosswalk_U_U': [15, 2],
                      'crosswalk_U_B': [15, 2], 'crosswalk_B_U': [10, 1], 'crosswalk_B_B': [10, 1]}
        amount_car = {'car_L': [25, 2], 'car_R': [25, 2]}

    if variante_zeiten == 4:
        # 20:00 [Chance, Amount] of Pedestrians/Cars spawned (per second)
        amount_ped = {'crosswalk_L_L': [15, 1], 'crosswalk_L_R': [15, 1],
                      'crosswalk_M_L': [10, 2], 'crosswalk_M_R': [10, 2], 'crosswalk_U_U': [15, 2],
                      'crosswalk_U_B': [15, 2], 'crosswalk_B_U': [10, 1], 'crosswalk_B_B': [10, 1]}
        amount_car = {'car_L': [10, 2], 'car_R': [10, 2]}

    return amount_ped, amount_car


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
    for k in range(0, amount_ped["crosswalk_L_L"][1]):
        if random.randint(1, 101) <= amount_ped["crosswalk_L_L"][0]:
            walkers.append(Pedestrian("crosswalk_L_L"))

    for k in range(0, amount_ped["crosswalk_L_R"][1]):
        if random.randint(1, 101) <= amount_ped["crosswalk_L_R"][0]:
            walkers.append(Pedestrian("crosswalk_L_R"))

    for k in range(0, amount_ped["crosswalk_M_L"][1]):
        if random.randint(1, 101) <= amount_ped["crosswalk_M_L"][0]:
            walkers.append(Pedestrian("crosswalk_M_L"))

    for k in range(0, amount_ped["crosswalk_M_R"][1]):
        if random.randint(1, 101) <= amount_ped["crosswalk_M_R"][0]:
            walkers.append(Pedestrian("crosswalk_M_R"))

    for k in range(0, amount_ped["crosswalk_U_U"][1]):
        if random.randint(1, 101) <= amount_ped["crosswalk_U_U"][0]:
            walkers.append(Pedestrian("crosswalk_U_U"))

    for k in range(0, amount_ped["crosswalk_U_B"][1]):
        if random.randint(1, 101) <= amount_ped["crosswalk_U_B"][0]:
            walkers.append(Pedestrian("crosswalk_U_B"))

    for k in range(0, amount_ped["crosswalk_B_U"][1]):
        if random.randint(1, 101) <= amount_ped["crosswalk_B_U"][0]:
            walkers.append(Pedestrian("crosswalk_B_U"))

    for k in range(0, amount_ped["crosswalk_B_B"][1]):
        if random.randint(1, 101) <= amount_ped["crosswalk_B_B"][0]:
            walkers.append(Pedestrian("crosswalk_B_B"))


def spawn_cars(drivers, i):
    # K: Start- und Endkoordinaten gemäss entsprechenden Agent-Quellen
    # S: Car(Weg)
    for k in range(0, amount_car["car_L"][1]):
        if random.randint(1, 101) <= amount_car["car_L"][0]:
            drivers.append(Driver("car_L"))

    for k in range(0, amount_car["car_R"][1]):
        if random.randint(1, 101) <= amount_car["car_R"][0]:
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
    if i != 0:
        if i % 720 == 0:
            tram.append(Tram("6_Uni"))
            spawn_tram_raster(tram, "vertical", raster)

        if (i + 600) % 720 == 0:
            tram.append(Tram("6_Polybahn"))
            spawn_tram_raster(tram, "horizontal", raster)

        if (i + 480) % 720 == 0:
            tram.append(Tram("9_Uni"))
            spawn_tram_raster(tram, "vertical", raster)

        if (i + 360) % 720 == 0:
            tram.append(Tram("9_Haldenbach"))
            spawn_tram_raster(tram, "vertical", raster)

        if (i + 240) % 720 == 0:
            tram.append(Tram("10_Haldenbach"))
            spawn_tram_raster(tram, "vertical", raster)

        if (i + 120) % 720 == 0:
            tram.append(Tram("10_Polybahn"))
            spawn_tram_raster(tram, "horizontal", raster)
    else:
        tram.append(Tram("6_Uni"))
        spawn_tram_raster(tram, "vertical", raster)


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

        self.class_ = "Pedestrian"

        # K: Stores Path of Pedestrian
        self.path = path

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

        self.class_ = 'Driver'

        # K: Dictionary für X-STARTkoordinate des Cars
        self.startposx = {
            'car_L': 63,
            'car_R': 66,
        }

        # K: Dictionary für Y-STARTkoordinate des Cars
        self.startposy = {
            'car_L': 0,
            'car_R': 99,
        }

        self.middleposx = {
            'car_L': 63,
            'car_R': 66,
        }

        self.middleposy = {
            'car_L': 42,
            'car_R': 42,
        }

        # K: Dictionary für X-ENDkoordinate des Cars
        self.endposx = {
            'car_L': 63,
            'car_R': 66,
        }

        # K: Dictionary für Y-ENDkoordinate des Cars
        self.endposy = {
            'car_L': 99,
            'car_R': 0,
        }

        self.path = path

        # K: Start und Endpunkt
        self.startx = self.startposx[path]
        self.starty = self.startposy[path]
        if random.randint(0, 30) == 5:
            self.endx = self.middleposx[path]
            self.endy = self.middleposy[path]
        else:
            self.endx = self.endposx[path]
            self.endy = self.endposy[path]

        # K: Position of Agent
        self.cordx = self.startx
        self.cordy = self.starty

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

        self.class_ = "Tram"

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
        matrix[41][33] = 0
        matrix[45][35] = 0
        matrix[41][56] = 0
        matrix[45][58] = 0
        matrix[39][62] = 0
        matrix[37][67] = 0
        matrix[69][62] = 0
        matrix[67][67] = 0
        matrix[42][36] = 0
        matrix[42][59] = 0
        matrix[36][63] = 0
        matrix[40][66] = 0
        matrix[70][66] = 0
        matrix[66][63] = 0
        return matrix
    if number == 1:
        matrix[41][33] = 4
        matrix[45][35] = 4
        # crosswalk2
        matrix[41][56] = 4
        matrix[45][58] = 4
        # crosswalk3
        matrix[39][62] = 4
        matrix[37][67] = 4
        # crosswalk4
        matrix[69][62] = 4
        matrix[67][67] = 4

        # Fussgänger müssen warten
        # Matrix[x][y] = 3 für alle x,y welche direkt vor dem Fussgängerstreifen liegen aus Fussgänger sicht
        return matrix
    if number == 2:
        # crosswalk1:
        matrix[42][36] = 5
        # crosswalk
        matrix[42][59] = 5
        # crosswalk3
        matrix[36][63] = 5
        matrix[40][66] = 5
        # crosswalk
        matrix[70][66] = 5
        matrix[66][63] = 5
        return matrix


def move(agent, matrix):
    # Speichert die momentanen Koordinaten (old) sowie die Zukünftigen(new)
    xn_old = agent.cordx
    xn_new = agent.cordx + agent.xspeed
    ym_old = agent.cordy
    ym_new = agent.cordy + agent.yspeed

    # Falls die new-Koordinate in der Matrix unbesetzt ist, darf der Agent ein Feld weiter. Ansonsten bleibt er stehen.
    if matrix[ym_new][xn_new] == 0:
        if matrix[ym_old][xn_old] <= 3:
            # Ampeln dürfen nicht überschrieben werden
            matrix[ym_old][xn_old] = 0
        if isinstance(agent, Driver):
            matrix[ym_new][xn_new] = 2
        if isinstance(agent, Pedestrian):
            matrix[ym_new][xn_new] = 1
        agent.cordx = xn_new
        agent.cordy = ym_new
        window.move(agent.shape, agent.xspeed * size, agent.yspeed * size)

    if agent.class_ == 'Pedestrian' and agent.starty == agent.cordy and agent.startx == agent.cordx:
        waiting_ped[agent.path] += 1

    # Returns True if Car is at Endposition or Changes speed if it is at the middleposition
    if isinstance(agent, Driver):
        if agent.cordx == agent.endx and agent.cordy == agent.endy:
            if agent.cordx == agent.middleposx[agent.path] and agent.cordy == agent.middleposy[agent.path]:
                agent.endx = 0
                agent.endy = 42
                agent.xspeed, agent.yspeed = speed(agent)
            else:
                return True

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


def print_time(s_i, min_i, h_i):
    """
    Updates the current time displayed in the window
        Input: s, min, h as integers
    """
    time_label = Label(window, text="Time elapsed: ")
    time_label.place(x=50, y=50)
    if s_i < 10:
        s = '0' + str(s_i)
    else:
        s = str(s_i)
    if min_i < 10:
        minute = '0' + str(min_i)
    else:
        minute = str(min_i)
    if h_i < 10:
        h = '0' + str(h_i)
    else:
        h = str(h_i)
    current_time = Label(window, text=(h, ':', minute, ':', s))
    current_time.place(x=145, y=50)


def draw_lights(number):
    """
    Draws traffic lights in Canvas:
     1 = pedestrians WAIT
     2 = pedestrians GO
    """
    if number == 1:
        light_ped_b = PhotoImage(file='lights/red_bottom.gif')
        light_ped_t = PhotoImage(file='lights/red_top.gif')
        light_ped_r = PhotoImage(file='lights/red_right.gif')
        light_ped_l = PhotoImage(file='lights/red_left.gif')

        cwp_l_l = Label(window, image=light_ped_b)
        cwp_l_l.place(x=310, y=375)
        cwp_l_r = Label(window, image=light_ped_t)
        cwp_l_r.place(x=365, y=460)
        cwp_m_l = Label(window, image=light_ped_b)
        cwp_m_l.place(x=540, y=375)
        cwp_m_r = Label(window, image=light_ped_t)
        cwp_m_r.place(x=595, y=460)
        cwp_u_r = Label(window, image=light_ped_l)
        cwp_u_r.place(x=675, y=345)
        cwp_u_l = Label(window, image=light_ped_r)
        cwp_u_l.place(x=595, y=401)
        cwp_b_r = Label(window, image=light_ped_l)
        cwp_b_r.place(x=675, y=645)
        cwp_b_l = Label(window, image=light_ped_r)
        cwp_b_l.place(x=590, y=701)

    if number == 2:
        light_ped_b = PhotoImage(file='lights/green_bottom.gif')
        light_ped_t = PhotoImage(file='lights/green_top.gif')
        light_ped_r = PhotoImage(file='lights/green_right.gif')
        light_ped_l = PhotoImage(file='lights/green_left.gif')

        cwp_l_l = Label(window, image=light_ped_b)
        cwp_l_l.place(x=310, y=375)
        cwp_l_r = Label(window, image=light_ped_t)
        cwp_l_r.place(x=365, y=460)
        cwp_m_l = Label(window, image=light_ped_b)
        cwp_m_l.place(x=540, y=375)
        cwp_m_r = Label(window, image=light_ped_t)
        cwp_m_r.place(x=595, y=460)
        cwp_u_r = Label(window, image=light_ped_l)
        cwp_u_r.place(x=675, y=345)
        cwp_u_l = Label(window, image=light_ped_r)
        cwp_u_l.place(x=595, y=401)
        cwp_b_r = Label(window, image=light_ped_l)
        cwp_b_r.place(x=675, y=645)
        cwp_b_l = Label(window, image=light_ped_r)
        cwp_b_l.place(x=590, y=701)


def display_waiters(waiters):
    w_ll = Label(window, text=str(waiters['crosswalk_L_L']))
    w_ll.place(x=330, y=350)
    w_lr = Label(window, text=str(waiters['crosswalk_L_R']))
    w_lr.place(x=349, y=495)

    w_ml = Label(window, text=str(waiters['crosswalk_M_L']))
    w_ml.place(x=550, y=350)
    w_mr = Label(window, text=str(waiters['crosswalk_M_R']))
    w_mr.place(x=580, y=495)

    w_uu = Label(window, text=str(waiters['crosswalk_U_U']))
    w_uu.place(x=705, y=365)
    w_ub = Label(window, text=str(waiters['crosswalk_U_B']))
    w_ub.place(x=590, y=370)

    w_bu = Label(window, text=str(waiters['crosswalk_B_U']))
    w_bu.place(x=710, y=665)
    w_bb = Label(window, text=str(waiters['crosswalk_B_B']))
    w_bb.place(x=565, y=685)


def count_cars_waiting(raster, str):
    waiting_cars = 0
    if str == 'L_U':
        i = 35
        while raster[i][63] == 2:
            waiting_cars += 1
            i -= 1
    if str == 'L_B':
        i = 65
        while raster[i][63] == 2:
            waiting_cars += 1
            i -= 1
    if str == 'R_U':
        i = 42
        while raster[i][66] == 2:
            waiting_cars += 1
            i += 1
    if str == 'R_B':
        i = 71
        while raster[i][66] == 2:
            waiting_cars += 1
            i += 1
    return waiting_cars


""" ------------------------------------------ Begin "Main function" ------------------------------------------- """

# K: öffnet neues Fenster und initialisiert Koordinatenraster
tk = Tk()
window = Canvas(tk, width=LENGTH, height=LENGTH)
schachbrett(window)
tk.title("simulation_try4")
window.pack()
# K: sets the map in the background
img = Image.open('map_nico.gif')
backgr = ImageTk.PhotoImage(img)
canvas_img = window.create_image(503, 500, image=backgr)

# Variables, Arrays, Matrix for iteration
amount_ped, amount_car = spawning_frequency(variante_zeiten)
t_display = 0
walkers = []
drivers = []
tram = []
raster = initialize_gitter()

with open('values.csv', 'w') as f:
    w = csv.DictWriter(f, waiting_ped2.keys())
    w.writeheader()

    for i in range(1800):

        # Creates new agents in the lists (including random startingpoints)
        spawn_tram(tram, i, raster)
        spawn_ped(walkers, i)
        spawn_cars(drivers, i)

        display_waiters(waiting_ped)
        waiting_ped['time_t'] += 1
        temp_time = waiting_ped['time_t']

        # Zählt Anzahl Autos in der Warteschlange
        cars_waiting_L_U = count_cars_waiting(raster, "L_U")
        cars_waiting_L_B = count_cars_waiting(raster, "L_B")
        cars_waiting_R_U = count_cars_waiting(raster, "R_U")
        cars_waiting_R_B = count_cars_waiting(raster, "R_B")
        waiting_ped2 = {'time': waiting_ped['time_t'],
                'crosswalk_L': waiting_ped['crosswalk_L_R'] + waiting_ped['crosswalk_L_L'],
                'crosswalk_R': waiting_ped['crosswalk_M_L'] + waiting_ped['crosswalk_M_R'],
                'crosswalk_U': waiting_ped['crosswalk_U_U'] + waiting_ped['crosswalk_U_B'],
                'crosswalk_B': waiting_ped['crosswalk_B_B'] + waiting_ped['crosswalk_B_U'],
                'cars_L': cars_waiting_L_B + cars_waiting_L_U, 'cars_R': cars_waiting_R_B + cars_waiting_R_U}
        w.writerow(waiting_ped2)
        waiting_ped = {'time_t': temp_time, 'crosswalk_L_L': 0, 'crosswalk_L_R': 0,
                       'crosswalk_M_L': 0, 'crosswalk_M_R': 0, 'crosswalk_U_U': 0,
                       'crosswalk_U_B': 0, 'crosswalk_B_U': 0, 'crosswalk_B_B': 0,
                       'cars_L': 0, 'cars_M': 0, 'cars_U_U': 0, 'cars_U_B': 0,
                       'cars_B_U': 0, 'cars_B_B': 0}

        # print("Warteschlange: L_U: " + str(cars_waiting_L_U) + "  L_B: " + str(cars_waiting_L_B) + "  R_U: " +
        #     str(cars_waiting_R_U) + "  R_B: " + str(cars_waiting_R_B))

        # Updates Time in display window
        t_s += 1
        if t_s >= 60:
            t_min += 1
            t_s = 0
        if t_min >= 60:
            t_h += 1
            t_min = 0
        print_time(t_s, t_min, t_h)

        if variante_ampeln == True:
            # Activates / Deactivates Red light
            if i % light_phase == 0:
                raster = rotlicht(0, raster)
                raster = rotlicht(1, raster)
                # Setting traffic lights for when pedestrians have to wait
                light_ped_b = PhotoImage(file='lights/red_bottom.gif')
                light_ped_t = PhotoImage(file='lights/red_top.gif')
                light_ped_r = PhotoImage(file='lights/red_right.gif')
                light_ped_l = PhotoImage(file='lights/red_left.gif')

                cwp_l_l = Label(window, image=light_ped_b)
                cwp_l_l.place(x=310, y=375)
                cwp_l_r = Label(window, image=light_ped_t)
                cwp_l_r.place(x=365, y=460)
                cwp_m_l = Label(window, image=light_ped_b)
                cwp_m_l.place(x=540, y=375)
                cwp_m_r = Label(window, image=light_ped_t)
                cwp_m_r.place(x=595, y=460)
                cwp_u_r = Label(window, image=light_ped_l)
                cwp_u_r.place(x=675, y=345)
                cwp_u_l = Label(window, image=light_ped_r)
                cwp_u_l.place(x=595, y=401)
                cwp_b_r = Label(window, image=light_ped_l)
                cwp_b_r.place(x=675, y=645)
                cwp_b_l = Label(window, image=light_ped_r)
                cwp_b_l.place(x=590, y=701)

            if i % light_phase == car_phase:
                raster = rotlicht(0, raster)
                raster = rotlicht(2, raster)
                # setting traffic lights for when pedestrians can walk
                light_ped_b = PhotoImage(file='lights/green_bottom.gif')
                light_ped_t = PhotoImage(file='lights/green_top.gif')
                light_ped_r = PhotoImage(file='lights/green_right.gif')
                light_ped_l = PhotoImage(file='lights/green_left.gif')

                cwp_l_l = Label(window, image=light_ped_b)
                cwp_l_l.place(x=310, y=375)
                cwp_l_r = Label(window, image=light_ped_t)
                cwp_l_r.place(x=365, y=460)
                cwp_m_l = Label(window, image=light_ped_b)
                cwp_m_l.place(x=540, y=375)
                cwp_m_r = Label(window, image=light_ped_t)
                cwp_m_r.place(x=595, y=460)
                cwp_u_r = Label(window, image=light_ped_l)
                cwp_u_r.place(x=675, y=345)
                cwp_u_l = Label(window, image=light_ped_r)
                cwp_u_l.place(x=595, y=401)
                cwp_b_r = Label(window, image=light_ped_l)
                cwp_b_r.place(x=675, y=645)
                cwp_b_l = Label(window, image=light_ped_r)
                cwp_b_l.place(x=590, y=701)

        # Iterate all agents for one time period
        iterate(walkers, raster)
        i = 1
        while i <= car_speed:
            if i % 2:  # Trams sind halb so schnell wie autos
                iterate(tram, raster)
            iterate(drivers, raster)

            tk.update()
            if maxspeed == False:
                time.sleep(animation_speed)
            i += 1

            # print(raster[:, 42])
