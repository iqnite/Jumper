"""
Main game
"""

import sys
import tkinter as tk
from random import randint
from time import sleep
from tkinter.messagebox import askretrycancel, askyesno, showinfo, showerror
from tkinter.simpledialog import askstring

# Integrity checks
try:
    from settings import (
        WIDTH,
        HEIGHT,
        TOPLEFT_X,
        TOPLEFT_Y,
        PLAYER_SIZE,
        PLAYER_ASSETS,
        ENEMY_ASSETS,
        PARTICLE_ASSETS,
        ENEMY_SIZE,
        BOOST,
        SPEED,
        GRAVITY,
        GAP,
        ANIM_DELAY,
        ENEMY_CHANCE,
        MAX_ENEMY_HEIGHT,
        PARTICLE_CHANCE,
        MAX_ENEMIES,
        MIN_FPS,
        MAX_FPS,
        FPS_INCREASE,
        JUMP_KEY,
        PAUSE_KEY,
        SCOREBOARD,
        GROUND,
        JUMP_SOUND,
        DIE_SOUND,
        MUSIC,
        MUSIC_VOL,
        BACKGROUND,
    )
except NameError:
    showerror(
        title="Error",
        message="Configuration file corrupted. Try downloading the game again.",
    )
    sys.exit()
except ModuleNotFoundError:
    showerror(
        title="Error",
        message="Configuration file not found. Try downloading the game again.",
    )
    sys.exit()

try:
    from pygame import mixer

    mixer.init()
    JUMPSFX = mixer.Sound(JUMP_SOUND)
    DIESFX = mixer.Sound(DIE_SOUND)
    mixer.music.load(MUSIC)
except FileNotFoundError:
    showerror(
        title="Error",
        message="Could not load audio. Check that the specified sound files have the correct path.",
    )
    sys.exit()
except ModuleNotFoundError:
    showerror(
        title="Error",
        message="No Pygame installation found. Try running 'pip3 install pygame' in your terminal.",
    )
    sys.exit()

try:
    import score
    from sprite import Sprite
except ModuleNotFoundError:
    showerror(
        title="Error", message="Could not load modules. Try downloading the game again."
    )
    sys.exit()


# Figure controlled by the player
class Player(Sprite):
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

    def jump(self, *_):
        if self.y == GROUND:  # Check if sprite is on the ground, to avoid air jumps
            self.fall = BOOST
            JUMPSFX.play()


# Toplevel class with game window
class Game(tk.Frame):
    def __init__(self, master: tk.Tk, player_name: str):
        self.master = master
        super().__init__(self.master)
        self.pack(expand=True, fill="both")
        self.master.title("Jumper")
        self.master.iconphoto(False, PLAYER_COSTUMES[0])
        self.master.resizable(False, False)
        # Stop when the window is closed
        self.master.protocol("WM_DELETE_WINDOW", self.pause)
        self.username = player_name
        self.cube = None
        self.enemies = []
        self.particles = []
        self.score_display = None
        self.score = 0
        self.runs = 0
        self.fps = MIN_FPS
        self.canvas = None

    # Main loop
    def loop(self):
        while True:
            self.setup()
            assert self.canvas is not None
            for i in PAUSE_KEY:
                self.canvas.bind_all(i, self.pause)

            # The game starts here
            assert self.cube is not None
            mixer.music.play(-1)  # '-1' makes the sound repeat infinitely
            mixer.music.set_volume(MUSIC_VOL)
            while self.cube.health > 0:
                self.canvas.update()  # Refresh the screen
                if self.runs == 0:
                    self.cube.animate()
                    self.runs += 1
                elif self.runs >= self.fps * ANIM_DELAY:
                    self.runs = 0
                else:
                    self.runs += 1
                self.cube.sim()
                self.make_enemy()
                self.tick_enemies()
                self.make_particle()
                self.tick_particles()
                if self.fps < MAX_FPS:
                    self.fps += FPS_INCREASE
                sleep((1 / self.fps) if self.fps > 0 else 0)

            # Game over
            mixer.music.stop()
            DIESFX.play()
            self.cube.say("@!#?@!", 1 / MIN_FPS)
            score.save(SCOREBOARD, self.username, self.score)
            rank = None
            for k in score.get(SCOREBOARD):
                if str(self.username) in k:
                    rank = score.get(SCOREBOARD).index(k) + 1
                    break
            top_score = score.get(SCOREBOARD)[0]
            prompt = askretrycancel(
                title="Game over",
                message=f"Your score: {self.score}\nYour rank: #{rank}\nHigh score: {top_score}",
            )
            if not prompt:
                sys.exit()
            self.canvas.destroy()

    def setup(self):
        self.canvas = tk.Canvas(
            self.master, width=WIDTH, height=HEIGHT, background=BACKGROUND
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_line(
            0,
            GROUND + (PLAYER_SIZE / 2),
            WIDTH,
            GROUND + (PLAYER_SIZE / 2),
            fill="white",
        )
        self.score_display = self.canvas.create_text(
            WIDTH / 2, 20, font="Helvetica", fill="white"
        )
        self.cube = Player(self.canvas)
        self.enemies: list[Sprite] = []
        self.particles: list[Sprite] = []
        self.fps = MIN_FPS
        self.score = 0
        self.runs = 0
        self.canvas.focus()  # Jump to the window

    def make_enemy(self):
        assert self.canvas is not None
        if (randint(0, ENEMY_CHANCE) == 0) and (len(self.enemies) < MAX_ENEMIES):
            if len(self.enemies) > 0:
                if not self.enemies[-1].x <= WIDTH - GAP:
                    return
        else:
            return
        self.enemies.append(
            Sprite(
                self.canvas,
                WIDTH,
                GROUND - randint(0, MAX_ENEMY_HEIGHT),
                ENEMY_COSTUMES,
            )
        )

    def make_particle(self):
        assert self.canvas is not None
        if randint(0, PARTICLE_CHANCE) == 0:
            self.particles.append(
                Sprite(self.canvas, WIDTH, randint(0, GROUND), PARTICLE_COSTUMES)
            )

    def tick_particles(self):
        assert self.canvas is not None
        for particle in self.particles:
            particle.x = SPEED
            if particle.x <= 0:
                self.canvas.delete(self.particles[0].id)
                del self.particles[0]

    def tick_enemies(self):
        assert self.canvas is not None
        assert self.cube is not None
        assert self.score_display is not None
        for enemy in self.enemies:
            enemy.x = SPEED
            if self.runs == 0:
                enemy.animate()
            if self.cube.distance(enemy) <= abs(PLAYER_SIZE + ENEMY_SIZE) / 2:
                self.cube.health -= 1
            if enemy.x <= 0:
                self.canvas.delete(enemy.id)
                self.enemies.remove(enemy)
                self.score += 1
                self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")

    def pause(self, *_):
        mixer.music.pause()
        prompt = askyesno(
            title="Game paused", message="Click on 'Yes' to resume game, 'No' to exit."
        )
        if not prompt:
            sys.exit()
        mixer.music.unpause()


while True:
    if (username := askstring(title="Welcome!", prompt="What's your name?")) is None:
        sys.exit()
    elif ":" in username:
        showerror(
            title="Invalid input", message="Username cannot contain character ':'."
        )
    else:
        break

showinfo(
    title="Jumper",
    message=f"""Hello {username}!
Press {JUMP_KEY} to jump.
Press {PAUSE_KEY} to pause the game.
Avoid enemies.
Get to the top of the leaderboard!
Click 'OK' to play.""",
)

root = tk.Tk()

try:
    PLAYER_COSTUMES = [tk.PhotoImage(file=i) for i in PLAYER_ASSETS]
    ENEMY_COSTUMES = [tk.PhotoImage(file=i) for i in ENEMY_ASSETS]
    PARTICLE_COSTUMES = [tk.PhotoImage(file=i) for i in PARTICLE_ASSETS]
except FileNotFoundError:
    showerror(
        title="Error",
        message="Graphics not found.",
    )
    sys.exit()

app = Game(root, username)
app.loop()
