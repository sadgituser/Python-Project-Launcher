#Imports
import json
import time
import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from tkinter import font, filedialog
from pathlib import Path
import webbrowser
import os
import ctypes
from ctypes import wintypes
from PIL import Image, ImageTk
from app_card import AppCard

#Open Etsy URL (for image)
def openEtsyURL(event):
    webbrowser.open_new("https://theprintedcraftuk.etsy.com")


#Initialise root window
root = tk.Tk()
root.title("Python App Switcher")
root.geometry("800x750+150+150")
root.minsize(800, 750)
root.configure(bg="#000000", takefocus=True)

# Configure the 2 columns to center content horizontally
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

#Initialise root window fonts
titleFont = font.Font(family="IBM Plex Mono", size=30, underline=True, weight="bold")
descriptionFont = font.Font(family="IBM Plex Mono", size=12, weight="normal")

#Title label at the top of the page
titleLabel = tk.Label(root,
    text="Python App Switcher!",
    font=titleFont,
    bg="#000000",
    fg="#00FF00",
    width="20",
    anchor="center"
)
titleLabel.grid(row=0, column=0, columnspan=2, pady=(10, 10))

#Description label of program
descriptionLabel = tk.Label(root,
    text="This is my Python app for switching between different apps. Enjoy!",
    font=descriptionFont,
    bg="#000000",
    fg="#00FF00",
    anchor="center",
    justify="center"
)
descriptionLabel.grid(row=1, column=0, columnspan=2, pady=10)

#Image Paths and Image Initialisation
photo1_image_path = Path(__file__).parent / "Assets" / "photo1.png"
hackClubLogo = tk.PhotoImage(file=photo1_image_path)
photo3_image_path = Path(__file__).parent / "Assets" / "photo3.png"
myLogo = tk.PhotoImage(file=photo3_image_path)
photo4_image_path = Path(__file__).parent / "Assets" / "photo4.png"
photo5_image_path = Path(__file__).parent / "Assets" / "photo5.png"
mainIcon = tk.PhotoImage(file=photo5_image_path)

root.iconphoto(True, mainIcon)

#What do launch buttons do?
def launch_etsy():
    webbrowser.open_new("https://theprintedcraftuk.etsy.com")

def launch_app2():
    webbrowser.open_new("https://www.youtube.com/watch?v=a7Lq6ZlSqys")

imported_app_filepath_variable = StringVar()
# Tracks the path of the icon extracted from the selected .exe
extracted_icon_path_variable = StringVar(value=str(photo4_image_path))

# Helper function to extract an icon directly from a Windows .exe resource using ExtractIconExW
def extract_exe_icon(exe_path, save_path):
    shell32 = ctypes.windll.shell32
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    
    hIconLarge = wintypes.HICON()
    hIconSmall = wintypes.HICON()
    
    # ExtractIconExW extracts icons directly from the executable file resources
    res = shell32.ExtractIconExW(str(exe_path), 0, ctypes.byref(hIconLarge), ctypes.byref(hIconSmall), 1)
    
    # Pick whichever icon handle was successfully extracted
    hIcon = hIconLarge.value if hIconLarge.value else hIconSmall.value
    if not res or not hIcon:
        return False
        
    # Create compatible device context and bitmap to render the icon
    hdc = user32.GetDC(None)
    hdcmem = gdi32.CreateCompatibleDC(hdc)
    hbm = gdi32.CreateCompatibleBitmap(hdc, 32, 32)
    gdi32.SelectObject(hdcmem, hbm)
    
    user32.DrawIconEx(hdcmem, 0, 0, hIcon, 32, 32, 0, None, 0x0003) # DI_NORMAL
    
    class BITMAPINFOHEADER(ctypes.Structure):
        _fields_ = [
            ("biSize", wintypes.DWORD),
            ("biWidth", wintypes.LONG),
            ("biHeight", wintypes.LONG),
            ("biPlanes", wintypes.WORD),
            ("biBitcount", wintypes.WORD),
            ("biCompression", wintypes.DWORD),
            ("biSizeImage", wintypes.DWORD),
            ("biPelsPerMeter", wintypes.LONG),
            ("biPelsPerMeterY", wintypes.LONG),
            ("biClrUsed", wintypes.DWORD),
            ("biClrImportant", wintypes.DWORD)
        ]
        
    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = 32
    bmi.biHeight = -32  # Top-down
    bmi.biPlanes = 1
    bmi.biBitcount = 32
    bmi.biCompression = 0
    
    buf = ctypes.create_string_buffer(32 * 32 * 4)
    gdi32.GetDIBits(hdcmem, hbm, 0, 32, buf, ctypes.byref(bmi), 0)
    
    user32.ReleaseDC(None, hdc)
    gdi32.DeleteObject(hbm)
    gdi32.DeleteDC(hdcmem)
    
    # Clean up icon handles
    if hIconLarge.value:
        user32.DestroyIcon(hIconLarge.value)
    if hIconSmall.value:
        user32.DestroyIcon(hIconSmall.value)
    
    # Convert buffer to PIL Image and save as PNG
    img = Image.frombuffer("RGBA", (32, 32), buf, "raw", "BGRA", 0, 1)
    img.save(save_path, "PNG")
    return True

def import_app_file():
    imported_file_path = filedialog.askopenfilename(title="Select a File for the App!", filetypes=[("Windows Executable Files", "*.exe")])
    if imported_file_path:
        print("File selected:", imported_file_path)
        imported_app_filepath_variable.set(imported_file_path)
        
        # Create a unique icon filename using current timestamp so icons don't clash
        assets_dir = Path(__file__).parent / "Assets"
        assets_dir.mkdir(exist_ok=True)
        unique_icon_name = f"icon_{int(time.time())}.png"
        temp_icon_path = assets_dir / unique_icon_name
        
        success = extract_exe_icon(imported_file_path, temp_icon_path)
        if success:
            extracted_icon_path_variable.set(str(temp_icon_path))
            print("Successfully extracted .exe icon to:", temp_icon_path)
        else:
            print("Could not extract icon, using default.")
            extracted_icon_path_variable.set(str(photo4_image_path))

CONFIG_FILE = Path(__file__).parent / "apps_config.json"

def save_apps():
    data_to_save = []
    for app in apps_inventory:
        img_path = app["path"]
        if img_path == myLogo:
            img_str = str(Path(__file__).parent / "Assets" / "photo3.png")
        else:
            img_str = str(img_path)

        data_to_save.append({
            "path": img_str,
            "desc": app["desc"],
            "target": app["target"],
            "type": app["type"],
            "protected": app.get("protected", False)
        })
    with open(CONFIG_FILE, "w") as f:
        json.dump(data_to_save, f, indent=4)

def load_apps():
    default_apps = [
        {
            "path": myLogo,
            "desc": "My Etsy Shop. Check it out!",
            "action": launch_etsy,
            "target": "https://theprintedcraftuk.etsy.com",
            "type": "url",
            "protected": True
        },
        {
            "path": photo4_image_path,
            "desc": "App 2!",
            "action": launch_app2,
            "target": "https://www.youtube.com/watch?v=a7Lq6ZlSqys",
            "type": "url",
            "protected": True
        }
    ]

    if not CONFIG_FILE.exists():
        return default_apps

    try:
        with open(CONFIG_FILE, "r") as f:
            saved_data = json.load(f)

        loaded_inventory = []
        for item in saved_data:
            target = item["target"]
            app_type = item["type"]
            protected = item.get("protected", False)

            if app_type == "url":
                act = lambda u=target: webbrowser.open_new(u)
            elif app_type == "exe":
                act = lambda path=target: os.startfile(path)
            else:
                act = launch_app2

            loaded_inventory.append({
                "path": Path(item["path"]),
                "desc": item["desc"],
                "action": act,
                "target": target,
                "type": app_type,
                "protected": protected
            })
        return loaded_inventory
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_apps

apps_inventory = load_apps()

def refresh_app_grid():
    for widget in root.grid_slaves():
        info = widget.grid_info()
        if int(info.get("row", 0)) >= 2:
            widget.destroy()

    window_width = root.winfo_width()
    if window_width <= 1:
        max_cols = 2  
    elif window_width < 500:
        max_cols = 1
    else:
        max_cols = max(2, window_width // 350)

    for i in range(10):
        root.columnconfigure(i, weight=0)
    for i in range(max_cols):
        root.columnconfigure(i, weight=1)

    titleLabel.grid(row=0, column=0, columnspan=max_cols, pady=(10, 10), sticky="EW")
    descriptionLabel.grid(row=1, column=0, columnspan=max_cols, pady=10, sticky="EW")

    for index, app_data in enumerate(apps_inventory):
        row_num = 2 + (index // max_cols)
        col_num = index % max_cols

        img_path = app_data["path"]
        if img_path != myLogo and not isinstance(img_path, Path):
            img_path = Path(img_path)

        card = AppCard(
            parent_window=root,
            image_path=app_data["path"],
            description_text=app_data["desc"],
            launch_command=app_data["action"]
        )
        card.place_card(row_num=row_num, col_num=col_num)

# Build the initial grid
refresh_app_grid()

#Smaller fonts for small windows
smallWindowTitleFont = font.Font(family="IBM Plex Mono", size=20, weight="bold", underline=True)
smallWindowDescriptionFont = font.Font(family="IBM Plex Mono", size=14)
smallWindowButtonFont = font.Font(family="IBM Plex Mono", size=10, underline=True, weight="bold")
smallWindowEntryFont = font.Font(family="IBM Plex Mono", size=12)

def openRemoveAppWindow():
    global userRemoveAppEntry
    userRemoveAppEntry = StringVar()

    removeAppWindow = Toplevel(root)
    removeAppWindow.title("Remove App")
    removeAppWindow.geometry("650x375+50+50")
    removeAppWindow.resizable(False, False)
    removeAppWindow.transient(root)
    removeAppWindow.columnconfigure(0, weight=1)
    removeAppWindow.configure(bg="#000000", takefocus=True)

    removeAppTitleLabel = Label(removeAppWindow,
        text="Remove an App",
        font=smallWindowTitleFont,
        bg="#000000",
        fg="#00FF00",
        width=15
    )
    removeAppTitleLabel.grid(row=0, column=0, pady=7)

    removeAppDescriptionLabel = Label(removeAppWindow,
        text="Enter the exact description of the app you want to remove below. " \
        "(Note: Default apps cannot be removed!)",
        font=smallWindowDescriptionFont,
        bg="#000000",
        fg="#00FF00",
        width=16,
        wraplength=625,
        justify="left"
    )
    removeAppDescriptionLabel.grid(row=1, pady=8, sticky="EW")

    removeAppDescriptionTextEntry = Entry(removeAppWindow,
        bg="#FFFFFF",
        fg="#000000",
        font=smallWindowEntryFont,
        justify="left",
        textvariable=userRemoveAppEntry
    )
    removeAppDescriptionTextEntry.grid(row=2, pady=9)

    def executeRemoveApp():
        target_desc = userRemoveAppEntry.get().strip()
        global apps_inventory

        found = False
        for app in apps_inventory:
            if app["desc"] == target_desc:
                found = True
                if app.get("protected", False):
                    print("Action Denied: Cannot remove protected default app!")
                    removeAppWindow.destroy()
                    return
                
                apps_inventory.remove(app)
                save_apps()
                refresh_app_grid()
                print(f"Successfully removed app: {target_desc}")
                break
        
        if not found:
            print(f"No app found with description: {target_desc}")

        removeAppWindow.destroy()

    removeAppButton = Button(removeAppWindow,
        text="REMOVE APP",
        font=smallWindowButtonFont,
        bg="#00FF00",
        fg="#000000",
        command=executeRemoveApp
    )
    removeAppButton.grid(row=3, pady=9)


#Initialise 'About Me' window (function)
def openAboutMeWindow():
    aboutMeWindow = Toplevel(root)
    aboutMeWindow.title("About Me")
    aboutMeWindow.geometry("650x375+50+50")
    aboutMeWindow.resizable(False, False)
    aboutMeWindow.transient(root)
    aboutMeWindow.columnconfigure(0, weight=1)
    aboutMeWindow.configure(bg="#000000", takefocus=True)
    
    aboutMeTitleLabel = Label(aboutMeWindow,
        text="About Me!",
        font=smallWindowTitleFont,
        bg="#000000",
        fg="#00FF00",
        width=10
    )
    aboutMeTitleLabel.grid(row=0, column=0, pady=5)

    aboutMeDescriptionLabel = Label(aboutMeWindow,
        text="A little about myself. I am a 15 year old making small projects for fun. " \
        "This project was for the Terra Hackclub (https://terra.hackclub.com) project! " \
        "It is honestly quite fun, and I really enjoy making cool fun things for little fun projects like these. " \
        "My GitHub is at (https://github.com/sadgituser) where you can find many more of my projects! " \
        "Currently there is nowhere that you can support my work, but you can check out my Etsy shop at (https://theprintedcraftuk.etsy.com)! " \
        "Enjoy the app switcher, I hope that you find use in it! ",
        font=smallWindowDescriptionFont,
        bg="#000000",
        fg="#00FF00",
        width=16,
        wraplength=625,
        justify="left"
    )
    aboutMeDescriptionLabel.grid(row=1, pady=7, sticky="EW")

    myLogo_descriptionLabel = Label(aboutMeWindow, image=myLogo, cursor="hand2")
    myLogo_descriptionLabel.grid(row=2, column=0, pady=10)
    myLogo_descriptionLabel.bind("<Button-1>", openEtsyURL)

#Initialise 'Add New App' window (function)
def openNewAppWindow():
    global userNewAppEntry
    global imported_app_filepath_variable
    global extracted_icon_path_variable

    userNewAppEntry = StringVar()

    newAppWindow = Toplevel(root)
    newAppWindow.title("Add New App")
    newAppWindow.geometry("650x375+50+50")
    newAppWindow.resizable(False, False)
    newAppWindow.transient(root)
    newAppWindow.columnconfigure(0, weight=1)
    newAppWindow.configure(bg="#000000", takefocus=True)
    
    newAppTitleLabel = Label(newAppWindow,
        text="Add A New App",
        font=smallWindowTitleFont,
        bg="#000000",
        fg="#00FF00",
        width=15
    )
    newAppTitleLabel.grid(row=0, column=0, pady=7)

    newAppDescriptionLabel = Label(newAppWindow,
        text="Here you can add new apps to the switcher! Fill out the fields to get started! " \
        "Enter the App Description in the white entry field and select the file using Import File!",
        font=smallWindowDescriptionFont,
        bg="#000000",
        fg="#00FF00",
        width=16,
        wraplength=625,
        justify="left"
    )
    newAppDescriptionLabel.grid(row=1, pady=8, sticky="EW")

    createNewAppDescriptionTextEntry = Entry(newAppWindow,
        bg="#FFFFFF",
        fg="#000000",
        font=smallWindowEntryFont,
        justify="left",
        textvariable=userNewAppEntry
    )
    createNewAppDescriptionTextEntry.grid(row=2, pady=9)

    import_file_button = Button(newAppWindow,
        text="Import File",
        command=import_app_file,
        font=smallWindowButtonFont,
        bg="#00FF00",
        fg="#000000"
    )
    import_file_button.grid(row=3, pady=9)

    def createNewUserApp():
        desc = userNewAppEntry.get()
        filepath = imported_app_filepath_variable.get()
        icon_path = extracted_icon_path_variable.get()
        
        if not filepath:
            print("No file selected!")
            return

        def run_user_app():
            try:
                os.startfile(filepath)
            except Exception as e:
                print(f"Error launching app: {e}")

        # Append new app to inventory with persistent metadata
        new_app_data = {
            "path": Path(icon_path),
            "desc": desc,
            "action": run_user_app,
            "target": filepath,
            "type": "exe"
        }
        apps_inventory.append(new_app_data)
        
        # Save updated inventory to disk immediately
        save_apps()
        
        # Calculate row and column indices for 2-per-row layout dynamically
        new_index = len(apps_inventory) - 1
        row_num = 2 + (new_index // 2)
        col_num = new_index % 2

        card = AppCard(
            parent_window=root,
            image_path=Path(icon_path),
            description_text=desc,
            launch_command=run_user_app
        )
        card.place_card(row_num=row_num, col_num=col_num)
        
        newAppWindow.destroy()

    createNewAppButton = Button(newAppWindow,
        text="CREATE APP!",
        font=smallWindowButtonFont,
        bg="#00FF00",
        fg="#000000",
        command=createNewUserApp
    )
    createNewAppButton.grid(row=4, pady=9)

#Initialising the menubar
menubar = Menu(root)

fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Add New Switch/App", command=openNewAppWindow)
fileMenu.add_separator()
fileMenu.add_command(label="Remove Switches/Apps", command=openRemoveAppWindow)

aboutMeMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About Me", menu=aboutMeMenu)
aboutMeMenu.add_command(label="About Me (Popup Window)", command=openAboutMeWindow)

root.config(menu=menubar)
root.bind("<Configure>", lambda e: root.after(100, refresh_app_grid) if e.widget == root else None)
root.mainloop()
