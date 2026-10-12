#Python app switcher
#Imports
import tkinter as tk
from tkinter import PhotoImage
from tkinter.ttk import *
from tkinter import font

#Initialise root window
root = tk.Tk()
root.title("Python App Switcher")
root.geometry("480x520+100+100")
root.minsize(480, 520)
root.configure(bg="#000000", takefocus=True)

#Initialise fonts
titleFont = font.Font(family="IBM Plex Mono", size=30, underline=True, weight="bold")
descriptionFont = font.Font(family="IBM Plex Mono", size=12, weight="normal")

#Title label at the top of the page
titleLabel = tk.Label(root,
    text="Python App Switcher!",
    font=titleFont,
    bg="#000000",
    fg="#00FF00",
    width="18"
).pack(anchor="center", ipadx=2, ipady=1, padx=2, pady=1)

#Description label of program
descriptionLabel = tk.Label(root,
    text="This is my Python app for switching between different apps. Enjoy!",
    font=descriptionFont,
    bg="#000000",
    fg="#00FF00"
).pack(anchor="center", padx=2, pady=15)

#Putting up an image of the Etsy Shop logo - placeholder
myLogo = PhotoImage(file="/Assets/photo3.png")
myLogo_label = tk.Label(root, myLogo).pack(anchor="center", padx=2, pady=100)

#Launch App Button
launchAppButton = tk.Button(root,
    text="Launch App",
    command=None,
    bg="#00FF00",
    fg="#000000",
    activebackground="#000000",
    activeforeground="#00FF00"
).pack(anchor="center", padx=2, pady=150)

#Initialising menubar
menubar = tk.Menu(root)

#Add 'File' menu to the menubar - placeholder
fileMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Add New Switch", command=None)
fileMenu.add_separator()
fileMenu.add_command(label="Remove Switches", command=None)


#Add 'About Me' menu to menubar - placeholder
aboutMeMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="About Me", menu=aboutMeMenu)
aboutMeMenu.add_command(label="About Me", command=None)
aboutMeMenu.add_separator()
aboutMeMenu.add_command(label="More About Me (Popup Window)", command=None)

root.config(menu=menubar)
root.mainloop()