#Imports
import random
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
    increment_stat("etsy_about_clicks")
    webbrowser.open_new("https://theprintedcraftuk.etsy.com")

current_bg = "#000000"
current_fg="#00FF00"


#Initialise root window
root = tk.Tk()
root.title("Python App Switcher")
root.geometry("800x750+150+150")
root.minsize(800, 750)

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
    bg=current_bg,
    fg=current_fg,
    width="20",
    anchor="center"
)
titleLabel.grid(row=0, column=0, columnspan=2, pady=(10, 10))

#Description label of program
descriptionLabel = tk.Label(root,
    text="This is my Python app for switching between different apps. Enjoy!",
    font=descriptionFont,
    bg=current_bg,
    fg=current_fg,
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
    increment_stat("etsy_root_clicks")
    increment_stat("apps_opened")
    webbrowser.open_new("https://theprintedcraftuk.etsy.com")

def launch_app2():
    increment_stat("rickrolls")
    increment_stat("apps_opened")
    webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

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
    imported_file_path = filedialog.askopenfilename(
        title="Select a File for the App!", 
        filetypes=[("Windows Executable Files", "*.exe"), ("URL Links", "*.url"), ("All Files", "*.*")]
    )
    if imported_file_path:
        print("File selected:", imported_file_path)
        imported_app_filepath_variable.set(imported_file_path)
        
        assets_dir = Path(__file__).parent / "Assets"
        assets_dir.mkdir(exist_ok=True)
        unique_icon_name = f"icon_{int(time.time())}.png"
        temp_icon_path = assets_dir / unique_icon_name
        
        success = extract_exe_icon(imported_file_path, temp_icon_path)
        if success:
            extracted_icon_path_variable.set(str(temp_icon_path))
            print("Successfully extracted .exe icon to:", temp_icon_path)
        else:
            print("Could not extract icon automatically. Please choose a custom icon image.")
            custom_icon_path = filedialog.askopenfilename(
                title="Select a custom icon image for this app",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.ico")]
            )
            if custom_icon_path:
                extracted_icon_path_variable.set(custom_icon_path)
                print("Using custom icon:", custom_icon_path)
            else:
                extracted_icon_path_variable.set(str(photo4_image_path))

CONFIG_FILE = Path(__file__).parent / "apps_config.json"

default_stats = {
    "colour_changes": 0,
    "switches_added": 0,
    "switches_removed": 0,
    "apps_opened": 0,
    "etsy_root_clicks": 0,
    "etsy_about_clicks": 0,
    "rickrolls": 0,
    "about_me_opened": 0,
    "stats_opened": 0,
    "dev_checks": 0
}

current_stats = default_stats.copy()

def save_apps():
    data_to_save = {
        "theme": {"bg": current_bg, "fg": current_fg},
        "stats": current_stats,
        "apps": []
    }
    for app in apps_inventory:
        img_path = app["path"]
        if img_path == myLogo:
            img_str = str(Path(__file__).parent / "Assets" / "photo3.png")
        else:
            img_str = str(img_path)

        data_to_save["apps"].append({
            "path": img_str,
            "desc": app["desc"],
            "target": app["target"],
            "type": app["type"],
            "protected": app.get("protected", False)
        })
    with open(CONFIG_FILE, "w") as f:
        json.dump(data_to_save, f, indent=4)

def increment_stat(stat_key):
    global current_stats
    current_stats[stat_key] = current_stats.get(stat_key, 0) + 1
    save_apps()

def load_apps():
    global current_fg, current_bg, current_stats
    
    # Define complete default structure including theme and apps
    default_data = {
        "theme": {"bg": "#000000", "fg": "#00FF00"},
        "stats": default_stats,
        "apps": [
            {
                "path": str(Path(__file__).parent / "Assets" / "photo3.png"),
                "desc": "My Etsy Shop. Check it out!",
                "target": "https://theprintedcraftuk.etsy.com",
                "type": "url",
                "protected": True
            },
            {
                "path": str(photo4_image_path),
                "desc": "App 2!",
                "target": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "type": "url",
                "protected": True
            }
        ]
    }

    # If the config file doesn't exist, create it automatically with defaults
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_data, f, indent=4)

    try:
        with open(CONFIG_FILE, "r") as f:
            content = json.load(f)

        # Handle backward compatibility if an old list-only file exists
        if isinstance(content, dict):
            saved_data = content.get("apps", default_data["apps"])
            theme_data = content.get("theme", {})
            current_stats = content.get("stats", default_stats.copy())

            current_bg = theme_data.get("bg", "#000000")
            current_fg = theme_data.get("fg", "#00FF00")
            root.config(bg=current_bg)
            titleLabel.configure(bg=current_bg, fg=current_fg)
            descriptionLabel.configure(bg=current_bg, fg=current_fg)
        else:
            saved_data = content

        loaded_inventory = []
        for item in saved_data:
            target = item["target"]
            app_type = item["type"]
            protected = item.get("protected", False)
            raw_path = item["path"]

            if "photo3.png" in str(raw_path):
                path_val = myLogo
                act = launch_etsy
            elif "dQw4w9WgXcQ" in target:
                path_val = Path(raw_path)
                act=launch_app2
            else:
                path_val = Path(raw_path)
                if app_type == "url":
                    act = lambda u=target: (increment_stat("apps_opened"), webbrowser.open_new(u))
                elif app_type == "exe":
                    act = lambda p=target: (increment_stat("apps_opened"), os.startfile(p))
                else:
                    act = launch_app2

            loaded_inventory.append({
                "path": path_val,
                "desc": item["desc"],
                "action": act,
                "target": target,
                "type": app_type,
                "protected": protected
            })
        return loaded_inventory
    except Exception as e:
        print(f"Error loading config: {e}")
        return []

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

        # PASS THE CURRENT THEME COLORS TO THE APP CARD HERE:
        card = AppCard(
            parent_window=root,
            image_path=app_data["path"],
            description_text=app_data["desc"],
            launch_command=app_data["action"],
            bg_color=current_bg,
            fg_color=current_fg
        )
        card.place_card(row_num=row_num, col_num=col_num)


# Build the initial grid
refresh_app_grid()


def apply_theme(bg_hex, fg_hex):
    global current_bg, current_fg
    current_bg = bg_hex
    current_fg = fg_hex
    
    # Root window only takes bg (fg is invalid for Tk root)
    root.configure(bg=current_bg, takefocus=True)
    
    # Update main labels
    titleLabel.configure(bg=current_bg, fg=current_fg)
    descriptionLabel.configure(bg=current_bg, fg=current_fg)
    
    # Refresh the grid so any recreated cards match the theme
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
    removeAppWindow.geometry("650x250+50+50")
    removeAppWindow.resizable(False, False)
    removeAppWindow.transient(root)
    removeAppWindow.columnconfigure(0, weight=1)
    removeAppWindow.configure(bg=current_bg, takefocus=True)

    removeAppTitleLabel = Label(removeAppWindow,
        text="Remove an App",
        font=smallWindowTitleFont,
        bg=current_bg,
        fg=current_fg,
        width=15
    )
    removeAppTitleLabel.grid(row=0, column=0, pady=7)

    removeAppDescriptionLabel = Label(removeAppWindow,
        text="Enter the exact description of the app you want to remove below. " \
        "(Note: Default apps cannot be removed!)",
        font=smallWindowDescriptionFont,
        bg=current_bg,
        fg=current_fg,
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
        increment_stat("switches_removed")
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
        bg=current_fg,
        fg=current_bg,
        command=executeRemoveApp
    )
    removeAppButton.grid(row=3, pady=9)


#Initialise 'About Me' window (function)
def openAboutMeWindow():
    increment_stat("about_me_opened")
    aboutMeWindow = Toplevel(root)
    aboutMeWindow.title("About Me")
    aboutMeWindow.geometry("650x375+50+50")
    aboutMeWindow.resizable(False, False)
    aboutMeWindow.transient(root)
    aboutMeWindow.columnconfigure(0, weight=1)
    aboutMeWindow.configure(bg=current_bg, takefocus=True)
    
    aboutMeTitleLabel = Label(aboutMeWindow,
        text="About Me!",
        font=smallWindowTitleFont,
        bg=current_bg,
        fg=current_fg,
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
        bg=current_bg,
        fg=current_fg,
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
    newAppWindow.configure(bg=current_bg, takefocus=True)
    
    newAppTitleLabel = Label(newAppWindow,
        text="Add A New App",
        font=smallWindowTitleFont,
        bg=current_bg,
        fg=current_fg,
        width=15
    )
    newAppTitleLabel.grid(row=0, column=0, pady=7)

    newAppDescriptionLabel = Label(newAppWindow,
        text="Here you can add new apps to the switcher! Fill out the fields to get started! " \
        "Enter the App Description in the white entry field and select the file using Import File!",
        font=smallWindowDescriptionFont,
        bg=current_bg,
        fg=current_fg,
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
        bg=current_fg,
        fg=current_bg
    )
    import_file_button.grid(row=3, pady=9)

    def createNewUserApp():
        increment_stat("switches_added")
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
        bg=current_fg,
        fg=current_bg,
        command=createNewUserApp
    )
    createNewAppButton.grid(row=4, pady=9)


def openCustomiseWindow():
    customiseWindow = Toplevel(root)
    customiseWindow.title("Customise Colours")
    customiseWindow.geometry("700x650+50+50")
    customiseWindow.resizable(False, False)
    customiseWindow.transient(root)
    customiseWindow.columnconfigure(0, weight=1)
    customiseWindow.configure(bg=current_bg, takefocus=True)
   
    customiseWindowTitleLabel = Label(customiseWindow,
        text="Customise Colours!",
        font=smallWindowTitleFont,
        bg=current_bg,
        fg=current_fg,
        width=20
    )
    customiseWindowTitleLabel.grid(row=0, column=0, pady=5)
    
    customiseWindowDescriptionLabel = Label(customiseWindow,
        text="Here you can change the colours of the whole window!",
        font=smallWindowDescriptionFont,
        bg=current_bg,
        fg=current_fg,
        width=16,
        wraplength=625,
        justify="left"
    )
    customiseWindowDescriptionLabel.grid(row=1, pady=7, sticky="EW")

    themes_frame = Frame(customiseWindow, bg=current_bg)
    themes_frame.grid(row=2, column=0, pady=20)

    def set_theme(bg, fg):
        increment_stat("colour_changes")
        apply_theme(bg, fg)
        save_apps()

    #Buttons
    matrix_btn = Button(themes_frame, text="Matrix Green", command=lambda: set_theme("#000000", "#00FF00"), bg="#00FF00", fg="#000000", font=smallWindowButtonFont)
    matrix_btn.grid(row=0, column=0, padx=8)
    
    cyber_btn = Button(themes_frame, text="Cyberpunk Pink", command=lambda: set_theme("#000000", "#FF00FF"), bg="#FF00FF", fg="#000000", font=smallWindowButtonFont)
    cyber_btn.grid(row=0, column=1, padx=8, pady=10)
    
    amber_btn = Button(themes_frame, text="Retro Amber", command=lambda: set_theme("#000000", "#FFB000"), bg="#FFB000", fg="#000000", font=smallWindowButtonFont)
    amber_btn.grid(row=0, column=2, padx=8, pady=10)

    ice_btn = Button(themes_frame, text="Ice Blue", command=lambda: set_theme("#000000", "#00D2FF"), bg="#00D2FF", fg="#000000", font=smallWindowButtonFont)
    ice_btn.grid(row=0, column=3, padx=8, pady=10)

    grey_btn = Button(themes_frame, text="Sad Grey", command=lambda: set_theme("#000000", "#89827C"), bg="#89827C", fg="#000000", font=smallWindowButtonFont)
    grey_btn.grid(row=0, column=4, padx=8, pady=10)

    anger_btn = Button(themes_frame, text="Angry Red", command=lambda: set_theme("#000000", "#FF0000"), bg="#FF0000", fg="#000000", font=smallWindowButtonFont)
    anger_btn.grid(row=1, column=0, padx=8, pady=10)

    contemplative_blue_btn = Button(themes_frame, text="Contemplative Blue", command=lambda: set_theme("#000000", "#0B3F83"), bg="#0B3F83", fg="#000000", font=smallWindowButtonFont)
    contemplative_blue_btn.grid(row=1, column=1, padx=8, pady=10)

    chill_btn = Button(themes_frame, text="Chill Lilac", command=lambda: set_theme("#000000", "#A47DAB"), bg="#A47DAB", fg="#000000", font=smallWindowButtonFont)
    chill_btn.grid(row=1, column=2, padx=8, pady=10)

    vivid_btn = Button(themes_frame, text="Vivid Yellow", command=lambda: set_theme("#000000", "#FFFF00"), bg="#FFFF00", fg="#000000", font=smallWindowButtonFont)
    vivid_btn.grid(row=1, column=3, padx=8, pady=10)

    moss_btn = Button(themes_frame, text="Moss", command=lambda: set_theme("#000000", "#636B2F"), bg="#636B2F", fg="#000000", font=smallWindowButtonFont)
    moss_btn.grid(row=1, column=4, padx=8, pady=10)

    eclipse_btn = Button(themes_frame, text="Eclipse Blue", command=lambda: set_theme("#000000", "#272757"), bg="#272757", fg="#000000", font=smallWindowButtonFont)
    eclipse_btn.grid(row=2, column=0, padx=8, pady=10)

    forest_btn = Button(themes_frame, text="Lush Forest Green", command=lambda: set_theme("#000000", "#2E6F40"), bg="#2E6F40", fg="#000000", font=smallWindowButtonFont)
    forest_btn.grid(row=2, column=1, padx=8, pady=10)

    spice_btn = Button(themes_frame, text="Spiced Red", command=lambda: set_theme("#000000", "#9B1313"), bg="#9B1313", fg="#000000", font=smallWindowButtonFont)
    spice_btn.grid(row=2, column=2, padx=8, pady=10)

    chocolate_btn = Button(themes_frame, text="Lush Forest Green", command=lambda: set_theme("#000000", "#38240D"), bg="#38240D", fg="#000000", font=smallWindowButtonFont)
    chocolate_btn.grid(row=2, column=3, padx=8, pady=10)

    ink_btn = Button(themes_frame, text="Seaside Blue", command=lambda: set_theme("#000000", "#6D8196"), bg="#6D8196", fg="#000000", font=smallWindowButtonFont)
    ink_btn.grid(row=2, column=4, padx=8, pady=10)

    gold_btn = Button(themes_frame, text="Metallic Gold", command=lambda: set_theme("#000000", "#D4AF37"), bg="#D4AF37", fg="#000000", font=smallWindowButtonFont)
    gold_btn.grid(row=3, column=0, padx=8, pady=10)

    silver_btn = Button(themes_frame, text="Sterling Silver", command=lambda: set_theme("#000000", "#C0C0C0"), bg="#C0C0C0", fg="#000000", font=smallWindowButtonFont)
    silver_btn.grid(row=3, column=1, padx=8, pady=10)

    lavender_btn = Button(themes_frame, text="Lavender Dream", command=lambda: set_theme("#000000", "#9B59B6"), bg="#9B59B6", fg="#000000", font=smallWindowButtonFont)
    lavender_btn.grid(row=3, column=2, padx=8, pady=10)

    coral_btn = Button(themes_frame, text="Sunset Coral", command=lambda: set_theme("#000000", "#FF6B6B"), bg="#FF6B6B", fg="#000000", font=smallWindowButtonFont)
    coral_btn.grid(row=3, column=3, padx=8, pady=10)

    turquoise_btn = Button(themes_frame, text="Bright Turquoise", command=lambda: set_theme("#000000", "#1ABC9C"), bg="#1ABC9C", fg="#000000", font=smallWindowButtonFont)
    turquoise_btn.grid(row=3, column=4, padx=8, pady=10)

    sunset_btn = Button(themes_frame, text="Sunset Orange", command=lambda: set_theme("#000000", "#E67E22"), bg="#E67E22", fg="#000000", font=smallWindowButtonFont)
    sunset_btn.grid(row=4, column=0, padx=8, pady=10)

    neon_purple_btn = Button(themes_frame, text="Neon Purple", command=lambda: set_theme("#000000", "#BD00FF"), bg="#BD00FF", fg="#000000", font=smallWindowButtonFont)
    neon_purple_btn.grid(row=4, column=1, padx=8, pady=10)

    royal_blue_btn = Button(themes_frame, text="Royal Blue", command=lambda: set_theme("#000000", "#3498DB"), bg="#3498DB", fg="#000000", font=smallWindowButtonFont)
    royal_blue_btn.grid(row=4, column=2, padx=8, pady=10)

    rose_btn = Button(themes_frame, text="Rose Pink", command=lambda: set_theme("#000000", "#FF69B4"), bg="#FF69B4", fg="#000000", font=smallWindowButtonFont)
    rose_btn.grid(row=4, column=3, padx=8, pady=10)

    yellow_btn = Button(themes_frame, text="Electric Yellow", command=lambda: set_theme("#000000", "#F1C40F"), bg="#F1C40F", fg="#000000", font=smallWindowButtonFont)
    yellow_btn.grid(row=4, column=4, padx=8, pady=10)

    teal_btn = Button(themes_frame, text="Deep Teal", command=lambda: set_theme("#000000", "#008080"), bg="#008080", fg="#000000", font=smallWindowButtonFont)
    teal_btn.grid(row=5, column=0, padx=8, pady=10)

    plum_btn = Button(themes_frame, text="Rich Plum", command=lambda: set_theme("#000000", "#8E44AD"), bg="#8E44AD", fg="#000000", font=smallWindowButtonFont)
    plum_btn.grid(row=5, column=1, padx=8, pady=10)

    brick_btn = Button(themes_frame, text="Brick Red", command=lambda: set_theme("#000000", "#C0392B"), bg="#C0392B", fg="#000000", font=smallWindowButtonFont)
    brick_btn.grid(row=5, column=2, padx=8, pady=10)

    slate_btn = Button(themes_frame, text="Slate Blue", command=lambda: set_theme("#000000", "#5D6D7E"), bg="#5D6D7E", fg="#000000", font=smallWindowButtonFont)
    slate_btn.grid(row=5, column=3, padx=8, pady=10)

    peach_btn = Button(themes_frame, text="Warm Peach", command=lambda: set_theme("#000000", "#FFAB91"), bg="#FFAB91", fg="#000000", font=smallWindowButtonFont)
    peach_btn.grid(row=5, column=4, padx=8, pady=10)

    cyan_btn = Button(themes_frame, text="Neon Cyan", command=lambda: set_theme("#000000", "#00FFFF"), bg="#00FFFF", fg="#000000", font=smallWindowButtonFont)
    cyan_btn.grid(row=6, column=0, padx=8, pady=10)

    magenta_btn = Button(themes_frame, text="Deep Magenta", command=lambda: set_theme("#000000", "#D81B60"), bg="#D81B60", fg="#000000", font=smallWindowButtonFont)
    magenta_btn.grid(row=6, column=1, padx=8, pady=10)

    bronze_btn = Button(themes_frame, text="Antique Bronze", command=lambda: set_theme("#000000", "#CD7F32"), bg="#CD7F32", fg="#000000", font=smallWindowButtonFont)
    bronze_btn.grid(row=6, column=2, padx=8, pady=10)

    orchid_btn = Button(themes_frame, text="Light Orchid", command=lambda: set_theme("#000000", "#DA70D6"), bg="#DA70D6", fg="#000000", font=smallWindowButtonFont)
    orchid_btn.grid(row=6, column=3, padx=8, pady=10)

    periwinkle_btn = Button(themes_frame, text="Soft Periwinkle", command=lambda: set_theme("#000000", "#CCCCFF"), bg="#CCCCFF", fg="#000000", font=smallWindowButtonFont)
    periwinkle_btn.grid(row=6, column=4, padx=8, pady=10)

    emerald_btn = Button(themes_frame, text="Emerald Green", command=lambda: set_theme("#000000", "#2ECC71"), bg="#2ECC71", fg="#000000", font=smallWindowButtonFont)
    emerald_btn.grid(row=7, column=0, padx=8, pady=10)

    steel_btn = Button(themes_frame, text="Steel Blue", command=lambda: set_theme("#000000", "#4682B4"), bg="#4682B4", fg="#000000", font=smallWindowButtonFont)
    steel_btn.grid(row=7, column=1, padx=8, pady=10)

    burnt_orange_btn = Button(themes_frame, text="Burnt Orange", command=lambda: set_theme("#000000", "#CC5500"), bg="#CC5500", fg="#000000", font=smallWindowButtonFont)
    burnt_orange_btn.grid(row=7, column=2, padx=8, pady=10)

    amethyst_btn = Button(themes_frame, text="Amethyst", command=lambda: set_theme("#000000", "#9966CC"), bg="#9966CC", fg="#000000", font=smallWindowButtonFont)
    amethyst_btn.grid(row=7, column=3, padx=8, pady=10)

    khaki_btn = Button(themes_frame, text="Khaki Gold", command=lambda: set_theme("#000000", "#F0E68C"), bg="#F0E68C", fg="#000000", font=smallWindowButtonFont)
    khaki_btn.grid(row=7, column=4, padx=8, pady=10)

    marine_btn = Button(themes_frame, text="Marine Blue", command=lambda: set_theme("#000000", "#000080"), bg="#000080", fg="#000000", font=smallWindowButtonFont)
    marine_btn.grid(row=8, column=0, padx=8, pady=10)

    crimson_btn = Button(themes_frame, text="Crimson Red", command=lambda: set_theme("#000000", "#DC143C"), bg="#DC143C", fg="#000000", font=smallWindowButtonFont)
    crimson_btn.grid(row=8, column=1, padx=8, pady=10)

    olive_btn = Button(themes_frame, text="Dark Olive", command=lambda: set_theme("#000000", "#556B2F"), bg="#556B2F", fg="#000000", font=smallWindowButtonFont)
    olive_btn.grid(row=8, column=2, padx=8, pady=10)

    slate_grey_btn = Button(themes_frame, text="Slate Grey", command=lambda: set_theme("#000000", "#708090"), bg="#708090", fg="#000000", font=smallWindowButtonFont)
    slate_grey_btn.grid(row=8, column=3, padx=8, pady=10)

    hot_pink_btn = Button(themes_frame, text="Hot Pink", command=lambda: set_theme("#000000", "#FF1493"), bg="#FF1493", fg="#000000", font=smallWindowButtonFont)
    hot_pink_btn.grid(row=8, column=4, padx=8, pady=10)

    dodger_btn = Button(themes_frame, text="Dodger Blue", command=lambda: set_theme("#000000", "#1E90FF"), bg="#1E90FF", fg="#000000", font=smallWindowButtonFont)
    dodger_btn.grid(row=9, column=0, padx=8, pady=10)

    dark_orchid_btn = Button(themes_frame, text="Dark Orchid", command=lambda: set_theme("#000000", "#9932CC"), bg="#9932CC", fg="#000000", font=smallWindowButtonFont)
    dark_orchid_btn.grid(row=9, column=1, padx=8, pady=10)

    forest_moss_btn = Button(themes_frame, text="Forest Moss", command=lambda: set_theme("#000000", "#228B22"), bg="#228B22", fg="#000000", font=smallWindowButtonFont)
    forest_moss_btn.grid(row=9, column=2, padx=8, pady=10)

    salmon_btn = Button(themes_frame, text="Light Salmon", command=lambda: set_theme("#000000", "#FA8072"), bg="#FA8072", fg="#000000", font=smallWindowButtonFont)
    salmon_btn.grid(row=9, column=3, padx=8, pady=10)

    goldenrod_btn = Button(themes_frame, text="Goldenrod", command=lambda: set_theme("#000000", "#DAA520"), bg="#DAA520", fg="#000000", font=smallWindowButtonFont)
    goldenrod_btn.grid(row=9, column=4, padx=8, pady=10)

    chocolate_brown_btn = Button(themes_frame, text="Chocolate Brown", command=lambda: set_theme("#000000", "#D2691E"), bg="#D2691E", fg="#000000", font=smallWindowButtonFont)
    chocolate_brown_btn.grid(row=10, column=0, padx=8, pady=10)

    slate_blue_btn = Button(themes_frame, text="Medium Slate Blue", command=lambda: set_theme("#000000", "#7B68EE"), bg="#7B68EE", fg="#000000", font=smallWindowButtonFont)
    slate_blue_btn.grid(row=10, column=1, padx=8, pady=10)

    dark_turquoise_btn = Button(themes_frame, text="Dark Turquoise", command=lambda: set_theme("#000000", "#00CED1"), bg="#00CED1", fg="#000000", font=smallWindowButtonFont)
    dark_turquoise_btn.grid(row=10, column=2, padx=8, pady=10)

    lime_green_btn = Button(themes_frame, text="Lime Green", command=lambda: set_theme("#000000", "#32CD32"), bg="#32CD32", fg="#000000", font=smallWindowButtonFont)
    lime_green_btn.grid(row=10, column=3, padx=8, pady=10)

    tomato_btn = Button(themes_frame, text="Tomato Red", command=lambda: set_theme("#000000", "#FF6347"), bg="#FF6347", fg="#000000", font=smallWindowButtonFont)
    tomato_btn.grid(row=10, column=4, padx=8, pady=10)


default_stats = {
    "colour_changes": 0,
    "switches_added": 0,
    "switches_removed": 0,
    "apps_opened": 0,
    "etsy_root_clicks": 0,
    "etsy_about_clicks": 0,
    "rickrolls": 0,
    "about_me_opened": 0,
    "stats_opened": 0  # <--- NEW STAT
}

def openStatsWindow():
    # Increment stat as soon as window opens
    increment_stat("stats_opened")

    statsWindow = Toplevel(root)
    statsWindow.title("Fun Stats Window!")
    statsWindow.geometry("600x550+50+50")
    statsWindow.resizable(False, False)
    statsWindow.transient(root)
    statsWindow.columnconfigure(0, weight=1)
    statsWindow.configure(bg=current_bg, takefocus=True)

    statsTitleLabel = Label(statsWindow,
        text="Switcher Stats!",
        font=smallWindowTitleFont,
        bg=current_bg,
        fg=current_fg,
        width=25
    )
    statsTitleLabel.grid(row=0, column=0, pady=(15, 5))

    statsDescLabel = Label(statsWindow,
        text="Here is a breakdown of your activity and usage statistics on this app:",
        font=smallWindowDescriptionFont,
        bg=current_bg,
        fg=current_fg
    )
    statsDescLabel.grid(row=1, column=0, pady=(0, 15))

    stats_frame = Frame(statsWindow, bg=current_bg)
    stats_frame.grid(row=2, column=0, padx=20, pady=10, sticky="EW")
    stats_frame.columnconfigure(0, weight=1)
    stats_frame.columnconfigure(1, weight=1)

    display_metrics = [
        ("Total Apps/Links Opened:", current_stats.get("apps_opened", 0)),
        ("Switches Added:", current_stats.get("switches_added", 0)),
        ("Switches Removed:", current_stats.get("switches_removed", 0)),
        ("Times Theme Colour Changed:", current_stats.get("colour_changes", 0)),
        ("Times About Me Opened:", current_stats.get("about_me_opened", 0)),
        ("Times Stats Window Opened:", current_stats.get("stats_opened", 0)),
        ("Times Checked on Dev:", current_stats.get("dev_checks", 0)),
        ("Etsy Clicks (Main Window):", current_stats.get("etsy_root_clicks", 0)),
        ("Etsy Clicks (About Me Window):", current_stats.get("etsy_about_clicks", 0)),
        ("Times YouTube Opened:", current_stats.get("rickrolls", 0)),
    ]

    for idx, (label_text, val) in enumerate(display_metrics):
        lbl = Label(stats_frame, text=label_text, font=smallWindowDescriptionFont, bg=current_bg, fg=current_fg, anchor="w")
        lbl.grid(row=idx, column=0, sticky="W", pady=4, padx=10) # Fixed px -> padx

        val_lbl = Label(stats_frame, text=str(val), font=smallWindowButtonFont, bg=current_bg, fg=current_fg, anchor="e")
        val_lbl.grid(row=idx, column=1, sticky="E", pady=4, padx=10) # Fixed px -> padx

    closeBtn = Button(statsWindow,
        text="CLOSE DASHBOARD",
        bg=current_fg,
        fg=current_bg,
        font=smallWindowButtonFont,
        command=statsWindow.destroy # Fixed parentheses destroy() -> destroy
    )
    closeBtn.grid(row=3, column=0, pady=20) # Fixed gris -> grid

def konami_code_fun():
    increment_stat("dev_checks")

    devWindow = Toplevel(root)
    devWindow.title("Secret Dev Window :)")
    devWindow.geometry("900x200+50+50")
    devWindow.resizable(False, False)
    devWindow.transient(root)
    devWindow.columnconfigure(0, weight=1)
    devWindow.configure(bg=current_bg, takefocus=True)

    devTitleLabel = Label(devWindow,
        text="HACKER MODE ACTIVATED: FUN DEV STATUS INITIALISED",
        font=smallWindowTitleFont,
        bg=current_bg,
        fg=current_fg,
        width=70
    )
    devTitleLabel.grid(row=0, column=0, pady=(15, 10))

    statuses = [
        "Status: TESTING TESTING 123!",
        "Bug Found!",
        "Bug Removed!",
        "Code Combed Over",
        "Server Status: Up and Running",
        "Current Mood: Unhappy :(",
        "Testing Status: Error - Test not Found",
        "404 - Could not Establish Secure Connection to Cloudflare Servers!",
        "Hackclub Terra Progress: Devlog not Made!!!",
        "Undoing All Code",
        "Initialising Shutdown",
        "Executing python3.14.exe",
        "Why not? I'll Change the Code Structure",
        "camelCaseLooksLikeThis",
        "Gained SU Permissions, Entering the Mainframe Now",
        "Nebuchadnezzar Departing Now",
        "A Voice Says to You: Go Open the Dev's Etsy Shop and Buy Something",
        "Package Ordered, 9192378943 Days Until Shipment",
        "Network Disconnected (Just Kidding...)",
        "Refueling Oil"
    ]
    chosen_status = random.choice(statuses)

    devDescLabel = Label(devWindow,
        text=chosen_status,
        font=smallWindowDescriptionFont,
        bg=current_bg,
        fg=current_fg,
        wraplength=500,
        justify="center"
    )
    devDescLabel.grid(row=1, pady=20, padx=20)

    def update_status():
        if devWindow.winfo_exists():
            new_status = random.choice(statuses)
            devDescLabel.config(text=new_status)
            devWindow.after(5000, update_status)

    devWindow.after(5000, update_status)

    closeDevBtn = Button(devWindow,
        text="DON'T LEAVE ME HERE IN THIS TERMINAL!",
        bg=current_fg,
        fg=current_bg,
        font=smallWindowButtonFont,
        command=devWindow.destroy
    )
    closeDevBtn.grid(row=2, column=0, pady=15)


konami_sequence = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right", "b", "a"]
current_input = []
def check_konami(event):
    current_input.append(event.keysym)
    if len(current_input) > len(konami_sequence):
        current_input.pop(0)

    normalized_input = [k.lower() for k in current_input]
    normalized_target = [k.lower() for k in konami_sequence]

    if normalized_input == normalized_target:
        konami_code_fun()
        current_input.clear()


#Initialising the menubar and menus
menubar = Menu(root)

fileMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Switch/App Settings", menu=fileMenu)
fileMenu.add_command(label="Add New Switch/App", command=openNewAppWindow)
fileMenu.add_separator()
fileMenu.add_command(label="Remove Switches/Apps", command=openRemoveAppWindow)

customiseMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Customise", menu=customiseMenu)
customiseMenu.add_command(label="Change Colours", command=openCustomiseWindow)

statsMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Statistics", menu=statsMenu)
statsMenu.add_command(label="View Stats Dashboard", command=openStatsWindow)

aboutMeMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About Me", menu=aboutMeMenu)
aboutMeMenu.add_command(label="About Me (Popup Window)", command=openAboutMeWindow)


root.config(menu=menubar)
root.bind("<Configure>", lambda e: root.after(100, refresh_app_grid) if e.widget == root else None)
root.bind("<Key>", check_konami)
root.mainloop()
