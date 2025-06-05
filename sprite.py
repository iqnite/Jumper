"""
Template for sprite items
"""

from tkinter import Canvas
from math import sqrt
from time import sleep


class Sprite:
    def __init__(
        self, stage: Canvas, x: int, y: int, costumes: list, start_health: float = 1
    ):
        self.stage = stage
        self.health = start_health
        self.costumes = costumes
        self.costume_number = 0
        self.id = stage.create_image(x, y, image=costumes[self.costume_number])
        self.speech = None

    def pos(self, f: int):
        return self.stage.coords(self.id)[f]

    # The "setter" functions don't really set the position, they change it by the given s value
    @property
    def x(self):
        return self.pos(0)

    @x.setter
    def x(self, s):
        self.stage.move(self.id, s, 0)

    @property
    def y(self):
        return self.pos(1)

    @y.setter
    def y(self, s):
        self.stage.move(self.id, 0, s)

    @property
    def costume(self):
        return self.costume_number

    @costume.setter
    def costume(self, new: int):
        self.costume_number = new
        self.stage.itemconfig(self.id, image=self.costumes[self.costume_number])

    def distance(self, other):
        return sqrt(((self.x - other.x) ** 2) + ((self.y - other.y) ** 2))

    def say(self, text, delay: float = 0):
        if text is None:
            if self.speech:
                self.stage.delete(self.speech)
            return
        self.speech = self.stage.create_text(
            self.x + 20, self.y - 50, font="Roboto 10", fill="white"
        )
        display = ""
        for i in text:
            display += i
            self.stage.itemconfig(self.speech, text=display)
            self.stage.update()
            sleep(delay)

    def animate(self):
        try:
            self.costume += 1
        except IndexError:
            self.costume = 0
