import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

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
            pixels = resized_image.getdata()
            new_pixels = []
            for pixel in pixels:
                if pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240:
                    new_pixels.append((0, 0, 0, 0))
                else:
                    new_pixels.append(pixel)
            resized_image.putdata(new_pixels)
            self.tk_image = ImageTk.PhotoImage(resized_image)

        # Create widgets in frame
        self.logo_label = tk.Label(self.frame, image=self.tk_image, bg="#000000")
        self.logo_label.grid(row=0, column=0, pady=5)

        self.desc_label = tk.Label(self.frame, text=description_text, fg="#00FF00", bg="#000000", wraplength=150)
        self.desc_label.grid(row=1, column=0, pady=5)

        self.button = tk.Button(self.frame, text="Launch App!", command=launch_command, bg="#00FF00", fg="#000000")
        self.button.grid(row=2, column=0, pady=5)

    def place_card(self, row_num, col_num):
        # Put container on main grid
        self.frame.grid(row=row_num, column=col_num, padx=20, pady=10)