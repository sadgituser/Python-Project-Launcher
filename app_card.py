import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from pathlib import Path
from collections import deque

class AppCard:
    def __init__ (self, parent_window, image_path, description_text, launch_command):
        
        # Local Frame Container
        self.frame = tk.Frame(parent_window, bg="#000000")

        # Check FIRST if image_path is already a tk.PhotoImage object (like myLogo)
        if isinstance(image_path, tk.PhotoImage):
            self.tk_image = image_path
        else:
            # Otherwise, process file paths normally with PIL
            img_path = Path(image_path)
            raw_image = Image.open(img_path)
            resized_image = raw_image.resize((100, 100)).convert("RGBA")
            
            # Flood-fill background removal starting from the outer corners
            width, height = resized_image.size
            pixels = resized_image.load()
            
            def is_white(p):
                return p[0] > 240 and p[1] > 240 and p[2] > 240

            visited = set()
            queue = deque()
            
            # Start flood-fill from all 4 corners of the image
            for x, y in [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]:
                if is_white(pixels[x, y]):
                    queue.append((x, y))
                    visited.add((x, y))
                    
            while queue:
                cx, cy = queue.popleft()
                pixels[cx, cy] = (0, 0, 0, 0)  # Make transparent
                
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            if is_white(pixels[nx, ny]):
                                queue.append((nx, ny))

            self.tk_image = ImageTk.PhotoImage(resized_image)

        # Create widgets in frame
        self.logo_label = tk.Label(self.frame, image=self.tk_image, bg="#000000")
        self.logo_label.image = self.tk_image  # Prevent garbage collection
        self.logo_label.grid(row=0, column=0, pady=5)

        self.desc_label = tk.Label(self.frame, text=description_text, fg="#00FF00", bg="#000000", wraplength=150)
        self.desc_label.grid(row=1, column=0, pady=5)

        smallWindowButtonFont = font.Font(family="IBM Plex Mono", size=10, underline=True, weight="bold")

        self.button = tk.Button(self.frame, text="LAUNCH APP!", command=launch_command, bg="#00FF00", fg="#000000", font=smallWindowButtonFont)
        self.button.grid(row=2, column=0, pady=5)

    def place_card(self, row_num, col_num):
        # Put container on main grid
        self.frame.grid(row=row_num, column=col_num, padx=20, pady=10)
        