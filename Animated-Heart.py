import tkinter as tk
from PIL import ImageFilter
import math
import random
from PIL import Image, ImageDraw, ImageTk
# import pygame  # Uncomment to enable music

# --- SETTINGS ---
WIDTH, HEIGHT = 600, 600
BG_COLOR = "black"
HEART_COLOR = (255, 0, 0, 100)  # RGBA for transparency (for glow)

# Initialize Tkinter
root = tk.Tk()
root.title("Enhanced Heart Animation")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg=BG_COLOR)

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR, highlightthickness=0)
canvas.pack()

# --- (Optional) Music ---
# pygame.init()
# pygame.mixer.music.load("your_music_file.mp3")
# pygame.mixer.music.play(-1)

# --- Function to create heart shape ---
def heart_points(scale=1.0):
    points = []
    for t in range(0, 360, 1):
        angle = math.radians(t)
        x = 16 * math.sin(angle)**3
        y = 13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle)
        points.append((WIDTH//2 + x * scale, HEIGHT//2 - y * scale))
    return points

# --- Create glowing heart image with Pillow ---
def create_glow_heart(scale):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    points = heart_points(scale)
    draw.polygon(points, fill=HEART_COLOR)
    blurred = img.filter(ImageFilter.BLUR)
    return ImageTk.PhotoImage(blurred)

# --- Floating hearts ---
floating_hearts = []

def spawn_floating_heart():
    x = random.randint(100, WIDTH - 100)
    y = HEIGHT + 30
    size = random.uniform(0.5, 1.2)
    speed = random.uniform(1, 3)
    floating_hearts.append({"x": x, "y": y, "size": size, "speed": speed})
    root.after(500, spawn_floating_heart)

# --- Main animation ---
scale = 10
direction = 1
glow_image = None

def animate():
    global scale, direction, glow_image

    canvas.delete("all")

    # Update pulsing scale
    scale += 0.2 * direction
    if scale >= 11 or scale <= 9:
        direction *= -1

    # Create and draw glowing heart
    glow_image = create_glow_heart(scale)
    canvas.create_image(0, 0, anchor=tk.NW, image=glow_image)

    # Draw floating hearts
    for heart in floating_hearts:
        heart["y"] -= heart["speed"]
        size = heart["size"]
        points = []
        for t in range(0, 360, 10):
            angle = math.radians(t)
            x = 16 * math.sin(angle)**3
            y = 13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle)
            points.append((heart["x"] + x * size, heart["y"] - y * size))
        canvas.create_polygon(points, fill="pink", outline="", smooth=True)

    # Remove hearts that are off-screen
    floating_hearts[:] = [h for h in floating_hearts if h["y"] > -30]

    root.after(30, animate)

# Start everything
spawn_floating_heart()
animate()
root.mainloop()
