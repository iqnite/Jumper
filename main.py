# Main game

import tkinter as tk
from random import randint
from time import sleep
from tkinter.messagebox import askretrycancel, askyesno, showinfo
from tkinter.simpledialog import askstring

from score import *
from settings import *
from sprite import Sprite


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
            self.runs = 0
            for i in PAUSE_KEY:
                self.c.bind_all(i, self.pause)

            # The game starts here
            while (self.Cube.health > 0) and (not closed):
                self.c.update()  # Refresh the screen
                if self.runs == 0:
                    self.Cube.animate()
                    self.runs += 1
                elif self.runs >= self.fps*ANIM_DELAY:
                    self.runs = 0
                else:
                    self.runs += 1
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
            top(SCOREBOARD, self.username, self.score)
            rank = None
            for k in get(SCOREBOARD):
                if str(self.username) in k:
                    rank = get(SCOREBOARD).index(k) + 1
                    break
            top_score = get(SCOREBOARD)[0]
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
            if self.runs == 0:
                i.animate()
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


def handle_close():
    global closed
    closed = True


# Main window
closed = False
root = tk.Tk()
root.title("Jumper")
root.resizable(False, False)
Jumper = Game(root)
# Stop when the window is closed
root.protocol("WM_DELETE_WINDOW", Jumper.pause)

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
Avoid enemies.
Get to the top of the leaderboard!""")

Jumper.loop()

quit()
