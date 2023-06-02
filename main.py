'''
Brick jumper
Philipp D.
May 2023
v0.2
'''


import tkinter as tk
from math import sqrt
from random import randint
from settings import *
from time import sleep
from tkinter.messagebox import askretrycancel, askyesno, showinfo
from tkinter.simpledialog import askstring


# Template for sprite items
class Sprite:
    def __init__(self, stage: tk.Canvas, x: int, y: int, costumes: list, start_health: float = 1):
        self.stage = stage
        self.health = start_health
        self.costumes = costumes
        self.c = 0
        self.id = stage.create_image(x, y, image=costumes[self.c])
        '''self.id = stage.create_rectangle(
            x, y, x + size, y + size, fill=color, outline="")'''

    def pos(self, f: int): return self.stage.coords(self.id)[f]

    # Property is to avoid the () every time the position is called and to make the code look cleaner
    # The "setter" functions don't really set the position, they change it by the given s value
    # Source: RealPython.com
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

    # Thanks to Pythagoras
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
                self.x+PLAYER_SIZE/2, self.y-PLAYER_SIZE/2-10, font="Roboto 10", fill="white")
            display = ""
            for i in text:
                display += i
                self.stage.itemconfig(self.speech, text=display)
                self.stage.update()
                sleep(delay)


# Figure controlled by the player
class Player (Sprite):
    def __init__(self, stage: tk.Canvas):
        super().__init__(stage, TOPLEFT_X, TOPLEFT_Y, PLAYER_COSTUMES)
        for i in JUMP_KEY:
            stage.bind_all(i, self.jump)
        self.fall = 1

    # Simulate gravity
    def sim(self):
        self.y = self.fall
        self.fall = 1 if self.y > GROUND else self.fall + GRAVITY
        while self.y > GROUND:
            self.y = -1

    def jump(self, event=None):
        if self.y == GROUND:  # Check if sprite is on the ground, to avoid air jumps
            self.fall = BOOST

    def animate(self):
        try:
            self.costume += 1
        except:
            self.costume = 0

# Toplevel class with game window


class Game (tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.username = askstring(title="Welcome!",
                                  prompt="What's your name?")

    # Main loop
    def loop(self):
        while not closed:
            self.c = tk.Canvas(self.master, width=WIDTH,
                               height=HEIGHT, background="black")
            self.c.pack(fill="both", expand=True)
            self.c.create_line(
                0, GROUND + (PLAYER_SIZE / 2), WIDTH, GROUND + (PLAYER_SIZE / 2), fill="white")
            self.score_display = self.c.create_text(
                MID_X, 20, font="Helvetica", fill="white")
            self.Cube = Player(self.c)
            self.enemies = []
            self.particles = []
            self.fps = MIN_FPS
            self.score = 0
            self.c.focus()  # Jump to the window
            runs = 0
            for i in PAUSE_KEY:
                self.c.bind_all(i, self.pause)

            # The game starts here
            while (self.Cube.health > 0) and (not closed):
                self.c.update()  # Refresh the screen
                if runs == 0:
                    self.Cube.animate()
                    runs += 1
                elif runs >= ANIM_RATE:
                    runs = 0
                self.Cube.sim()
                self.make_enemy()
                self.tick_enemies()
                self.make_particle()
                self.tick_particles()
                if self.fps < MAX_FPS:
                    self.fps += FPS_INCREASE
                sleep(1/self.fps)

            # Game over
            self.Cube.say("@!#?@!", 1/MIN_FPS)
            Score.top(SCOREBOARD, self.username, self.score)
            rank = None
            for k in Score.get(SCOREBOARD):
                if str(self.username) in k:
                    rank = Score.get(SCOREBOARD).index(k) + 1
                    break
            top_score = Score.get(SCOREBOARD)[0]
            prompt = askretrycancel(
                title="Game over",
                message=f"Your score: {self.score}\nYour rank: #{rank}\nHigh score: {top_score}")
            if not prompt:
                handle_close()
            self.c.destroy()

    def make_enemy(self):
        if (randint(0, ENEMY_CHANCE) == 0) and (len(self.enemies) < MAX_ENEMIES):
            if len(self.enemies) > 0:
                if not (self.enemies[-1].x <= WIDTH - GAP):
                    return
        else:
            return
        self.enemies.append(
            Sprite(self.c, WIDTH, GROUND-randint(0, MAX_ENEMY_HEIGHT), ENEMY_COSTUMES))

    def make_particle(self):
        if randint(0, PARTICLE_CHANCE) == 0:
            self.particles.append(Sprite(self.c, WIDTH, randint(
                0, GROUND), PARTICLE_COSTUMES))

    def tick_particles(self):
        for j in self.particles:
            j.x = SPEED
            if j.x <= 0:
                self.c.delete(self.particles[0].id)
                del self.particles[0]

    def tick_enemies(self):
        for i in self.enemies:
            i.x = SPEED
            if self.Cube.distance(i) <= abs(PLAYER_SIZE + ENEMY_SIZE) / 2:
                self.Cube.health -= 1
            if i.x <= 0:
                self.c.delete(self.enemies[0].id)
                del self.enemies[0]
                self.score += 1
                self.c.itemconfig(self.score_display,
                                  text=f"Score: {self.score}")

    def pause(self, event=None):
        prompt = askyesno(title="Game paused",
                          message="Click on 'Yes' to resume game, 'No' to exit the game.")
        if not prompt:
            handle_close()


# Functions for score management
class Score:
    @staticmethod  # Doesn't require "self" parameter
    def sort(lst):
        if len(lst) < 1:
            return lst

        # Clean list from invalid lines
        for l in range(len(lst)):
            try:
                if not (':' in lst[l]):
                    del lst[l]
                if lst[l] == '\n':
                    del lst[l]
            except:
                pass

        for j in range(len(lst)):
            for k in range(len(lst)-1):
                item1 = lst[k]
                item1t = float((item1.split(':')[1]))
                if k != len(lst)-1:
                    item2 = lst[k+1]
                    item2t = float((item2.split(':')[1]))
                    if item1t < item2t:
                        # Swap items
                        lst[k] = str(item2)
                        lst[k+1] = str(item1)

        # Remove duplicates
        names = []
        h = 0
        while h < len(lst):
            s = lst[h].split(":")
            if s[0] in names:
                del lst[h]
            else:
                names.append(s[0])
            h += 1
        return lst

    @staticmethod
    def top(f, n, s):
        try:
            file = open(f, 'r')
        except:
            file = open(f, 'x')
            scores = []
        else:
            scores = file.readlines()
        finally:
            if n != "" and n != None:
                scores.append(f"{n}:{s}")
            scores = Score.sort(scores)
            file = open(f, 'w')
            for i in scores:
                file.write(str(i).strip('\n') + '\n')
            file.flush()
            file.close()

    @staticmethod
    def get(f):
        try:
            fobj = open(f, 'r')
        except:
            return [""]
        else:
            lst = fobj.readlines()
            fobj.close()
            return lst


def handle_close():
    global closed
    closed = True


# Main window
closed = False
root = tk.Tk()
root.title("Jumper")
root.resizable(False, False)
Jumper = Game(root)
# Stop when the window is closed; Source: GeeksForGeeks.org
root.protocol("WM_DELETE_WINDOW", Jumper.pause)

# Thanks to Felix G.
PLAYER_COSTUMES = [tk.PhotoImage(file=i) for i in PLAYER_ASSETS]
ENEMY_COSTUMES = [tk.PhotoImage(file=i) for i in ENEMY_ASSETS]
PARTICLE_COSTUMES = [tk.PhotoImage(file=i) for i in PARTICLE_ASSETS]

if (Jumper.username == None):
    handle_close()
    quit()

showinfo(title="Jumper",
         message=f"""Hello {Jumper.username}!
Press {JUMP_KEY} to jump.
Press {PAUSE_KEY} to pause the game.
Avoid orange cubes.
Get to the top of the leaderboard!""")

Jumper.loop()

quit()
