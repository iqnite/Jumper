"""
Preferences for the Jumper game. You can edit these values to adjust the playing experience.
"""

WIDTH: int = 750  # Width of the game window
HEIGHT: int = 250  # Height of the game window
TOPLEFT_X: int = 50  # X position of the player
TOPLEFT_Y: int = HEIGHT - 100  # Y position of the player at the beginning
PLAYER_SIZE: int = 60  # Manually insert the size of the player image (px)
ENEMY_SIZE: int = 25  # Manually insert the size of the enemy image (px)
GROUND: int = round(TOPLEFT_Y + (PLAYER_SIZE / 2))  # The minimum height for items
PLAYER_ASSETS: list = [
    "assets/3.png",
    "assets/4.png",
]  # Animation pictures for the player
ENEMY_ASSETS: list = [
    "assets/1.png",
    "assets/6.png",
]  # Animation pictures for the enemies
PARTICLE_ASSETS: list = ["assets/star0.png"]  # Picture for the stars
BACKGROUND: str = "black"  # Background color
JUMP_SOUND: str = "assets/jump.wav"  # Sound to play when the player jumps
DIE_SOUND: str = "assets/die.wav"  # Sound to play when the player hits an enemy
MUSIC: str = "assets/loop.mp3"  # Background music
SCOREBOARD: str = "jumper.scores"  # File where the high scores are stored
MUSIC_VOL: float = 0.2  # Volume of the background music
BOOST: int = -15  # The height the player should be able to jump to
SPEED: float = -5  # Movement speed
GRAVITY: int = 1  # Falling speed increase
GAP: float = 200  # The minimum distance between enemies
ENEMY_CHANCE: int = (
    10  # The lower this value, the higher the chance that an enemy appears
)
PARTICLE_CHANCE: int = (
    5  # The lower this value, the higher the chance that a star appears
)
MAX_ENEMIES: int = 5  # The maximum amount of enemies on the screen
MAX_ENEMY_HEIGHT: int = (
    HEIGHT - BOOST - GROUND
)  # The maximum heigth where enemies spawn
MIN_FPS: float = 60  # Minimum frames per second
MAX_FPS: float = 180  # Maximum frames per second
FPS_INCREASE: float = 0.5  # The game gets faster by this value at every round
ANIM_DELAY: float = (
    0.1  # Delay between animation frames (will be multiplied automatically by the current FPS)
)
JUMP_KEY: list = ["<space>", "<Up>", "<Button-1>"]  # Bindings to jump
PAUSE_KEY: list = ["<Escape>", "<p>", "<Button-3>"]  # Bindings to pause
