import tkinter as tk
from tkinter import ttk
import json, os

class RecipeFinder:
    def __init__(self, master):
        self.master = master
        self.master.title("Recipe Finder by Mathilda Braun")
        self.dir_name = os.path.dirname(os.path.realpath(__file__))
        print(self.dir_name)
    
        
        try:
            loaded = os.open(f"{self.dir_name}/RecipeFinder/Recipes",0)
            print(loaded)
            with open(f"{self.dir_name}/RecipeFinder/settings.json", mode="r", encoding="utf-8") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.settings = {
                "language": "German"
                }
            os.makedirs(f"{self.dir_name}/RecipeFinder/Recipes/Pictures")
            with open(f"{self.dir_name}/RecipeFinder/settings.json", mode="w", encoding="utf-8") as f:
                self.settings = json.dump(self.settings, f, indent=4)

        sidebars = tk.Canvas(self.master, width=150)
        sidebars.pack(side=tk.RIGHT, fill=tk.Y)
        search = sidebars.create_text(30, 0, text="Suche",angle=90)
        home = sidebars.create_text(60, 0, text="Homepage",angle=90)
        favorits = sidebars.create_text(90, 0, text="Favoriten",angle=90)
        last = sidebars.create_text(120, 0, text="Zuletzt",angle=90)
        create = sidebars.create_text(150, 0, text="Erstellen",angle=90)
        def update_position(event):
            neue_hoehe = event.height
            sidebars.coords(search, 30-10, neue_hoehe / 2)
            sidebars.coords(home, 60-10, neue_hoehe / 2)
            sidebars.coords(favorits, 90-10, neue_hoehe / 2)
            sidebars.coords(last, 120-10, neue_hoehe / 2)
            sidebars.coords(create, 150-10, neue_hoehe / 2)
        sidebars.bind("<Configure>", update_position)

        




    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    recipefinder = RecipeFinder(root)
    recipefinder.run()
