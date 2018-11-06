""" TODO
- delete objects
- old/new map
- y-Axis: ok if from above?
- ongoing
"""

from tkinter import *
from numpy import *
import random
import time
from PIL import ImageTk, Image


# Height/Width of window:
LENGTH = 600
# Squares horizontally/vertically:
units = 10
# Amount of pedestrians to be spawned:
n_pedestrians = 5
# Amount of cars to be spawned:
n_cars = 5
# SPEED OF ANIMATION:
time_t = 0.2

size = LENGTH / units


# Create array of paths for pedestrians and cars
path_ped = []
path_car = []

# Create paths for pedestrians (from top to bottom)
for n in range(units):
    path_ped.append(array(zeros((units, 2)), dtype=int))
    for i in range(units):
        path_ped[n][i, 0] = int(n)
        path_ped[n][i, 1] = int(i)

# Create paths for cars (from left to right)
for n in range(units):
    path_car.append(array(zeros((units, 2)), dtype=int))
    for i in range(units):
        path_car[n][i, 0] = int(i)
        path_car[n][i, 1] = int(n)


# Create Checkers-like board (units by units)
def schachbrett(canvas):
    for x in range(units + 1):
        canvas.create_line(LENGTH / units * x, 0, LENGTH / units * x, LENGTH, fill="#476042")
    for y in range(units + 1):
        canvas.create_line(0, LENGTH / units * y, LENGTH, LENGTH / units * y, fill="#476042")


class Pedestrian:
    def __init__(self, color):
        self.path = random.randrange(1, units - 1)
        self.pos = 0
        self.cordxn = path_ped[self.path][0][0]  #XN: Koordinate der X-Achse, Spaltenkoordinate von Matrize (n)
        self.cordym = path_ped[self.path][0][1]  #YM: Koordinate der Y-Achse, Zeilenkoordinate von Matrize (m)
        self.dirxn = path_ped[self.path][1][0] - path_ped[self.path][0][0]
        self.dirym = path_ped[self.path][1][1] - path_ped[self.path][0][1]
        self.object = window.create_oval(self.cordxn * size, self.cordym * size, self.cordxn * size + size,
                                         self.cordym * size + size, fill=color)

    def direction(self):
        self.dirxn = path_ped[self.path][self.pos + 1][0] - path_ped[self.path][self.pos][0]
        self.dirym = path_ped[self.path][self.pos + 1][1] - path_ped[self.path][self.pos][1]

    def update_matrix(self, new):
        new[self.cordym][self.cordxn] = 1

    def move(self, old, new):
        if self.pos == len(path_ped) - 1:
            window.delete(self.object)
            # Show and delete agent
            return False
        elif old[path_ped[self.path][self.pos + 1][1], path_ped[self.path][self.pos + 1][0]] == 2:
            new[self.cordym, self.cordxn] = 1
            return True
        elif new[path_ped[self.path][self.pos + 1][1], path_ped[self.path][self.pos + 1][0]] != 0:
            new[self.cordym, self.cordxn] = 1
            return True
        else:
            self.direction()
            self.pos += 1
            self.cordxn = path_ped[self.path][self.pos][0]
            self.cordym = path_ped[self.path][self.pos][1]
            new[self.cordym][self.cordxn] = 1
            window.move(self.object, self.dirxn * size, self.dirym * size)
            return True


class Car:
    def __init__(self, color):
        self.path = random.randrange(1, units - 1)
        self.pos = 0
        self.cordxn = path_car[self.path][0][0]  # XN: Koordinate der X-Achse, Spaltenkoordinate von Matrize (n)
        self.cordym = path_car[self.path][0][1]  # YM: Koordinate der Y-Achse, Zeilenkoordinate von Matrize (m)
        self.dirxn = path_car[self.path][1][0] - path_ped[self.path][0][0]
        self.dirym = path_car[self.path][1][1] - path_ped[self.path][0][1]
        self.object = window.create_rectangle(self.cordxn * size, self.cordym * size,
                                              self.cordxn * size + size, self.cordym * size + size, fill=color)

    def direction(self):
        self.dirxn = path_car[self.path][self.pos + 1][0] - path_car[self.path][self.pos][0]
        self.dirym = path_car[self.path][self.pos + 1][1] - path_car[self.path][self.pos][1]

    def update_matrix(self, new):
        new[self.cordym][self.cordxn] = 2

    def move(self, old, new):
        if self.pos == len(path_car) - 1:
            window.delete(self.object)
            # Show and delete agent
            return False
        elif old[path_car[self.path][self.pos + 1][1], path_car[self.path][self.pos + 1][0]] != 0:
            new[self.cordym, self.cordxn] = 2
            return True
        elif new[path_car[self.path][self.pos + 1][1], path_car[self.path][self.pos + 1][0]] != 0:
            new[self.cordym, self.cordxn] = 2
            return True
        else:
            self.direction()
            self.pos += 1
            self.cordxn = path_car[self.path][self.pos][0]
            self.cordym = path_car[self.path][self.pos][1]
            new[self.cordym][self.cordxn] = 2
            window.move(self.object, self.dirxn * size, self.dirym * size)
            return True


# MAIN FUNCTION --------------------------------------------------------------------------------------------------------


tk = Tk()
window = Canvas(tk, width=LENGTH, height=LENGTH, )
schachbrett(window)
tk.title("INTERACTION - PEDESTRAIANS & CARS")
window.pack()
# sets the map in the background
img = Image.open('map.gif')
backgr = ImageTk.PhotoImage(img)
canvas_img = window.create_image(0, 0, image=backgr)


old_matrix = array(zeros((units, units)), dtype=int)
new_matrix = array(zeros((units, units)), dtype=int)


# Create Agents
ped = []
cars = []
for i in range(n_pedestrians):
    ped.append(Pedestrian("green"))
    ped[i].update_matrix(new_matrix)
for i in range(n_cars):
    cars.append(Car("red"))
    cars[i].update_matrix(new_matrix)
tk.update()
time.sleep(time_t)



while True:
    print(new_matrix)
    old_matrix = new_matrix
    new_matrix = array(zeros((units, units)), dtype=int)
    # SPAWN CONTINUOUSLY
    # ped.append(Pedestrian("green"))
    # cars.append(Car("red"))

    for i in ped:
        moving = i.move(old_matrix, new_matrix)
    for i in cars:
        moving = i.move(old_matrix, new_matrix)
    tk.update()

    # SPEED OF ANIMATION
    time.sleep(time_t)


tk.mainloop()
