#Python app switcher
#Imports
import tkinter as tk
from tkinter.ttk import *
from tkinter import font
from pathlib import Path

#Initialise root window
root = tk.Tk()
root.title("Python App Switcher")
root.geometry("800x600+150+150")
root.resizable(False, False)
root.configure(bg="#000000", takefocus=True)

# Configure the root grid to center content horizontally
root.columnconfigure(0, weight=1)

#Initialise fonts
titleFont = font.Font(family="IBM Plex Mono", size=30, underline=True, weight="bold")
descriptionFont = font.Font(family="IBM Plex Mono", size=12, weight="normal")

#Title label at the top of the page
titleLabel = tk.Label(root,
    text="Python App Switcher!",
    font=titleFont,
    bg="#000000",
    fg="#00FF00",
    width="20"
)
titleLabel.grid(row=0, column=0, pady=(10, 10)) # Row 0, centered, added vertical padding

#Description label of program
descriptionLabel = tk.Label(root,
    text="This is my Python app for switching between different apps. Enjoy!",
    font=descriptionFont,
    bg="#000000",
    fg="#00FF00"
)
descriptionLabel.grid(row=1, column=0, pady=10) # Row 1, centered

#Putting up an image of the Etsy Shop logo - placeholder
image_path = Path(__file__).parent / "Assets" / "photo3.png"
myLogo = tk.PhotoImage(file=image_path)
myLogo_label = tk.Label(root, image=myLogo)
myLogo_label.grid(row=2, column=0, pady=10) # Row 2, centered

#Launch App Button
launchAppButton = tk.Button(root,
    text="Launch App",
    command=None,
    bg="#00FF00",
    fg="#000000",
    activebackground="#000000",
    activeforeground="#00FF00"
)
launchAppButton.grid(row=3, column=0, pady=20) # Row 3, centered

#Initialising menubar
menubar = tk.Menu(root)

#Add 'File' menu to the menubar - placeholder
fileMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Add New Switch", command=None)
fileMenu.add_separator()
fileMenu.add_command(label="Remove Switches", command=None)

#Smaller fonts for 'About Me' window
aboutMeTitleFont = font.Font(family="IBM Plex Mono", size=14, weight="bold", underline=True)
aboutMeDescriptionFont = font.Font(family="IBM Plex Mono", size=8)

#Initialise 'About Me' window (function)
def openAboutMeWindow():
    #Start and configure 'About Me' window
    aboutMeWindow = tk.Toplevel(root)
    aboutMeWindow.title("About Me")
    aboutMeWindow.geometry("300x200+50+50")
    aboutMeWindow.resizable(False, False)
    aboutMeWindow.transient(root)
    aboutMeWindow.columnconfigure(0, weight=1)
    aboutMeWindow.configure(bg="#000000", takefocus=True)
    
    #About Me Title
    aboutMeTitleLabel = tk.Label(aboutMeWindow,
        text="About Me!",
        font=aboutMeTitleFont,
        bg="#000000",
        fg="#00FF00",
        width=10
    )
    aboutMeTitleLabel.grid(row=0, column=0, pady=5)

    #About Me Title
    aboutMeDescriptionLabel = tk.Label(aboutMeWindow,
        text="A little about myself. I am a 15 year old making small projects for fun. " \
        "This project was for the Terra Hackclub (https://terra.hackclub.com) project! " \
        "It is honestly quite fun, and I really enjoy making cool fun things for little fun projects like these. " \
        "My GitHub is at (https://github.com/sadgituser) where you can find many more of my projects! " \
        "Currently there is nowhere that you can support my work, but you can check out my Etsy shop at (https://theprintedcraftuk.etsy.com)! " \
        "Enjoy the app switcher, I hope that you find use in it! ",
        font=aboutMeDescriptionFont,
        bg="#000000",
        fg="#00FF00",
        width=16,
        wraplength=275,
        justify="left"
    )
    aboutMeDescriptionLabel.grid(row=1, pady=5, sticky="EW")


#Add 'About Me' menu to menubar - placeholder
aboutMeMenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="About Me", menu=aboutMeMenu)
aboutMeMenu.add_command(label="More About Me (Popup Window)", command=openAboutMeWindow)


root.config(menu=menubar)
root.mainloop()
