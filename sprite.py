# Template for sprite items

from tkinter import Canvas
from math import sqrt
from time import sleep


class Sprite:
    def __init__(self, stage: Canvas, x: int, y: int, costumes: list, start_health: float = 1):
        self.stage = stage
        self.health = start_health
        self.costumes = costumes
        self.c = 0
        self.id = stage.create_image(x, y, image=costumes[self.c])

    def pos(self, f: int): return self.stage.coords(self.id)[f]

    # Property is to avoid the () every time the position is called and to make the code look cleaner
    # The "setter" functions don't really set the position, they change it by the given s value
    @property
    def x(self): return self.pos(0)

    @x.setter
    def x(self, s): self.stage.move(self.id, s, 0)

    @property
    def y(self): return self.pos(1)

    @y.setter
    def y(self, s): self.stage.move(self.id, 0, s)

    @property
    def costume(self): return self.c

    @costume.setter
    def costume(self, new: int):
        self.c = new
        self.stage.itemconfig(self.id, image=self.costumes[self.c])

    def distance(self, other): return sqrt(
        ((self.x - other.x) ** 2)
        +
        ((self.y - other.y) ** 2)
    )

    def say(self, text, delay: float = 0):
        if text == None:
            self.stage.delete(self.speech)
        else:
            self.speech = self.stage.create_text(
                self.x+20, self.y-50, font="Roboto 10", fill="white")
            display = ""
            for i in text:
                display += i
                self.stage.itemconfig(self.speech, text=display)
                self.stage.update()
                sleep(delay)

    def animate(self):
        try:
            self.costume += 1
        except:
            self.costume = 0
