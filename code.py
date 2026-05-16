import tkinter as tk
from tkinter import ttk
import json, os
from PIL import Image, ImageTk
import cairosvg # type: ignore
import io
from tkinter import messagebox, simpledialog,filedialog


class RecipeFinder:
    def __init__(self, master):

        self.DEBUG = False
        self.didIngredients = False
        self.standart_color = "#117a91"
        self.highlight_color = "#145563"
        self.dir_name = os.path.dirname(os.path.realpath(__file__))
        try:
            #dummy

            loaded = os.open(f"{self.dir_name}/RecipeFinder/Recipes",0)
            print(loaded)
            with open(f"{self.dir_name}/RecipeFinder/settings.json", mode="r", encoding="utf-8") as f:
                self.settings = json.load(f)
            with open(f"{self.dir_name}/RecipeFinder/categories.json", mode="r", encoding="utf-8") as f:
                self.categories = json.load(f)
            with open(f"{self.dir_name}/RecipeFinder/Ingredients/ingredients.json", mode="r", encoding="utf-8") as f:
                self.ingredients = json.load(f)
        except FileNotFoundError:
            if self.DEBUG:
                print("Folders not found! Creating empty structure now.")
            self.settings = {
                "language": "German"
                }
            
            os.makedirs(f"{self.dir_name}/RecipeFinder/Recipes/Pictures", exist_ok=True)
            os.makedirs(f"{self.dir_name}/RecipeFinder/Ingredients", exist_ok=True)
            with open(f"{self.dir_name}/RecipeFinder/Ingredients/ingredients.json", mode="w", encoding="utf-8") as f:
                self.ingredients = {}
                json.dump(self.ingredients, f)
            os.makedirs(f"{self.dir_name}/RecipeFinder/Pictograms", exist_ok=True)
            with open(f"{self.dir_name}/RecipeFinder/settings.json", mode="w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
            self.categories = {
                "Suppen": ["Soups", "Suppe", "Kürbissuppe", "Tomatensuppe", "Curry"], 
                "unter 20 Minuten": ["schnell", "fast", "unter 20 Minuten"], 
                "Nudelgerichte": ["Bratnudeln", "Soba", "Spaghetti", "Pasta", "Nudeln", "Eiernudeln", "Canneloni", "Nudelauflauf", "Capellini", "Farfalle", "Fettucine", "Fusilli", "Gnocchi", "Lasagne", "Linguine", "Maccheroni", "Orecchiette", "Paccheri", "Pappardelle", "Penne", "Ravioli", "Rigatoni", "Spaghettini", "Tagliatelle", "Tortellini", "Tortelloni", "Ramen", "Udon"], 
                "Aufläufe": ["Lasagne", "Gigantes", "Nudelauflauf"],
                "Desserts": ["Pudding", "Schokolade", "Marmelade", "Kuchen", "Muffin", "Muffins", "Baumkuchen", "Joghurt", "Pfannkuchen", "Faschingskrapfen"],
                "Gebratenes": ["Soba", "Bratnudeln", "Gemüsepfanne", "Pfanne", "Pfannkuchen", "Eierkuchen", "Steak", "Braten", "Pommes", "Chicken Nuggets"],
                "Reisgerichte": ["Reis", "Curry", "Vollkornreis", "Hühnerfrikassee", "Don", "Sushi"],
                "Feiertagsessen": ["Gänsebraten", "Ente", "Falscher Hase", "Lasagne"]}
            with open(f"{self.dir_name}/RecipeFinder/categories.json", mode="w", encoding="utf-8") as f:
                json.dump(self.categories, f, indent=4)
        self.master = master
        if self.DEBUG:
            print("Created Window")
        
        if self.DEBUG:
            print(f"Running in {self.dir_name}")
        
        self.master.title("Recipe Finder by Mathilda Braun")
        self.pictograms = {
            "Search": f"{self.dir_name}/RecipeFinder/Pictograms/search.svg",
            "Home": f"{self.dir_name}/RecipeFinder/Pictograms/home.svg",
            "Add": f"{self.dir_name}/RecipeFinder/Pictograms/add.svg",
            "Favorite": f"{self.dir_name}/RecipeFinder/Pictograms/favorite.svg",
            "Noodles": f"{self.dir_name}/RecipeFinder/Pictograms/noodle-bowl.svg",
            "Recent": f"{self.dir_name}/RecipeFinder/Pictograms/time.svg",
            "Image": f"{self.dir_name}/RecipeFinder/Pictograms/image.svg",
            1: f"{self.dir_name}/RecipeFinder/Pictograms/number--small--1.svg",
            2: f"{self.dir_name}/RecipeFinder/Pictograms/number--small--2.svg",
            3: f"{self.dir_name}/RecipeFinder/Pictograms/number--small--3.svg",
            4: f"{self.dir_name}/RecipeFinder/Pictograms/number--small--4.svg",
            5: f"{self.dir_name}/RecipeFinder/Pictograms/number--small--5.svg",
            "Notification": f"{self.dir_name}/RecipeFinder/Pictograms/important.svg",
            "Save": f"{self.dir_name}/RecipeFinder/Pictograms/save.svg",
            "Ingredient": f"{self.dir_name}/RecipeFinder/Pictograms/strawberry.svg",
            "Liked": f"{self.dir_name}/RecipeFinder/Pictograms/favorite--filled.svg",
            "Start": f"{self.dir_name}/RecipeFinder/Pictograms/play.svg",
        }

        for part in self.pictograms:
            self.pictograms[part] = cairosvg.svg2png(url=self.pictograms[part])
            image = Image.open(io.BytesIO(self.pictograms[part]))
            self.pictograms[part] = ImageTk.PhotoImage(image)
        self.breite = 0
        self.hoehe = 0
        
        
        self.INTERFACE = tk.Frame(self.master, width=self.breite-150,height=self.hoehe)
        self.INTERFACE.place(x=0,y=0)
        
        self.recipes = {}
        
        print(self.dir_name)
        self.update()
        

        self.master.attributes('-zoomed', True)
        if self.DEBUG:
            print("Maximised the Window succesfully!")
        
        def toggleDEBUG(event=None):
            print("Debug")
            if self.DEBUG == False:
                self.DEBUG = True
                
            else:
                self.DEBUG = False

            self.Search()
        

        if self.DEBUG:
            print(f"Settings Inhalt: {self.settings}")
            print(f"Categories Inhalt: {len(self.categories)} Kategorien erstellt")

            print(f"Settings: {self.settings}")
            print(f"Categories: {self.categories}")
        

        if self.DEBUG:
            self.INTERFACE.config(bg="green")

        sidebars = tk.Canvas(self.master, width=150)
        sidebars.pack(side=tk.RIGHT, fill=tk.Y)
        if self.DEBUG:
            sidebars.config(bg="blue")
        search = sidebars.create_text(30, 0, text="Suche",angle=90, font=("Arial",16,"bold"), tags="SEARCH")
        searchP = sidebars.create_image(0, 0, image=self.pictograms["Search"], tags="SEARCH")
        
        home = sidebars.create_text(60, 0, text="Homepage",angle=90, font=("Arial",16,"bold"),tags="HOME")
        homeP = sidebars.create_image(0, 0, image=self.pictograms["Home"],tags="HOME")
        favorits = sidebars.create_text(90, 0, text="Favoriten",angle=90, font=("Arial",16,"bold"),tags="FAVORITS")
        favoritsP = sidebars.create_image(0, 0, image=self.pictograms["Favorite"],tags="FAVORITS")
        last = sidebars.create_text(120, 0, text="Zutaten",angle=90, font=("Arial",16,"bold"),tags="INGREDIENTS")
        lastP = sidebars.create_image(0, 0, image=self.pictograms["Ingredient"],tags="INGREDIENTS")
        create = sidebars.create_text(150, 0, text="Erstellen",angle=90, font=("Arial",16,"bold"),tags="CREATE")
        createP = sidebars.create_image(0, 0, image=self.pictograms["Add"],tags="CREATE")

        sidebars.tag_bind("SEARCH", "<Button-1>", self.Search)
        sidebars.tag_bind("HOME", "<Button-1>", self.Home)
        sidebars.tag_bind("FAVORITS", "<Button-1>", self.Favorits)
        sidebars.tag_bind("INGREDIENTS", "<Button-1>", self.Ingredients)
        sidebars.tag_bind("CREATE", "<Button-1>", self.Create)

        self.master.bind("<Control-Alt-d>", toggleDEBUG)

        

        
        def update_position(event):
            neue_hoehe = event.height
            sidebars.coords(searchP,30-10, neue_hoehe / 2 + 70)
            sidebars.coords(search, 30-10, neue_hoehe / 2)
            sidebars.coords(home, 60-10, neue_hoehe / 2)
            sidebars.coords(homeP,60-10, neue_hoehe / 2 + 70)
            sidebars.coords(favorits, 90-10, neue_hoehe / 2)
            sidebars.coords(favoritsP,90-10, neue_hoehe / 2 + 70)
            sidebars.coords(last, 120-10, neue_hoehe / 2)
            sidebars.coords(lastP,120-10, neue_hoehe / 2 + 70)
            sidebars.coords(create, 150-10, neue_hoehe / 2)
            sidebars.coords(createP,150-10, neue_hoehe / 2 + 70)
        sidebars.bind("<Configure>", update_position)

        self.selected = "SEARCH"
        
        self.recipes = {}
        self.Search()
        self.images = {}
    
    def update(self):
        self.master.update_idletasks()
        self.breite = self.master.winfo_width()
        self.hoehe = self.master.winfo_height()

        self.INTERFACE.place(
            x=0,
            y=0,
            width=self.breite - 150,
            height=self.hoehe
        )

        #if self.DEBUG:
            #print(self.breite, self.hoehe)

        self.master.after(20, self.update)

    def Search(self, event=None):
        for widget in self.INTERFACE.winfo_children():
            widget.destroy()
        if self.DEBUG:
            print("SEARCH")
        self.search_var = tk.StringVar(value="Suche ein Rezept")
        self.searchEntry = ttk.Entry(self.INTERFACE, textvariable=self.search_var)
        
        self.searchEntry.grid(row=0, column=0, sticky="ew")
        original_img = cairosvg.svg2png(url=f"{self.dir_name}/RecipeFinder/Pictograms/search.svg")
        original_img = Image.open(io.BytesIO(original_img))
        
        
        # 2. Größe ändern (z. B. auf 16x16 Pixel)

        original_img= original_img.resize((16, 16)) 
        self.pictograms["Small_Search"]  = ImageTk.PhotoImage(original_img)
        searchimagecanvas = tk.Canvas(self.INTERFACE, width=20, height=20)
        searchimagecanvas.place(x="63.15c",y=0)
        searchimagecanvas.create_image(0,0,anchor="nw",image=self.pictograms["Small_Search"])

        searchimagecanvas.bind("<Button-1>", self.doTheSearch)
        if self.DEBUG:
            searchimagecanvas.config(bg="orange")
        
            self.searchEntry.config(background="red")
        self.INTERFACE.grid_columnconfigure(0, weight=1)

        buttonFrame = tk.Frame(self.INTERFACE)
        if self.DEBUG:
            buttonFrame.config(background="yellow")
        buttonFrame.grid(row=1, column=0)

        placecolumn = 0
        placerow = 1
        categoriebuttons = {}
        for category in self.categories:
            if self.DEBUG:
                print(category)
            if category == "Nudelgerichte":
                picture = self.pictograms["Noodles"]
            else:
                picture = ""
            categoriebuttons[f"{category}"] = ttk.Button(buttonFrame, text=f"{category}", image = picture, padding=15, compound="right", command=lambda categorie=category: self.opencategorie(categorie=categorie))
            categoriebuttons[f"{category}"].grid(row=placerow, column=placecolumn, padx=15, pady=20)
            placecolumn += 1
            if placecolumn == 2:
                placecolumn = 0
                placerow += 1
        if self.DEBUG:
            print(f"Buttons: {categoriebuttons}")

            

        

    def openRecipe(self, recipe):
        for widget in self.INTERFACE.winfo_children():
            widget.destroy()
        if self.DEBUG:
            print("RECIPE")

        def toggle_favorite():
            if text["Liked"] == True:
                favorite = False
            else:
                favorite = True

            with open(f"{self.dir_name}/RecipeFinder/Recipes/{recipe}.json", mode="r", encoding="utf-8") as f:
                data = json.load(f)

            data["Liked"] = favorite

            with open(f"{self.dir_name}/RecipeFinder/Recipes/{recipe}.json", mode="w", encoding="utf-8") as f:
                json.dump(data, f)

            text["Liked"] = favorite

            generateButtons()

            


        img = tk.PhotoImage(file=f"{self.dir_name}/RecipeFinder/Recipes/Pictures/{recipe}.png")
        self.recipecanvas = tk.Canvas(self.INTERFACE)
        self.scrollbar = tk.Scrollbar(self.INTERFACE, orient="vertical", command=self.recipecanvas.yview)
        self.recipecanvas.configure(yscrollcommand=self.scrollbar.set)
        
        
        try:
            with open(f"{self.dir_name}/RecipeFinder/Recipes/{recipe}.json", mode="r",encoding="utf-8") as f:
                text = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Fehler", "Ein unerwarteter Fehler ist aufgetreten! Bitte melde das den Entwicklern auf\n https://github.com/sonstantin/Recipe-finder-by-Mathilda/issues")
       
        self.scrollbar.pack(side="right", fill="y")
        self.recipecanvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.recipecanvas)
        self.recipecanvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        

        
        self.scroll_frame.bind("<Configure>", lambda e: self.recipecanvas.configure(scrollregion=self.recipecanvas.bbox("all")))
        self.recipecanvas.bind_all("<MouseWheel>", lambda e: self.recipecanvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        


        # BILD (im scroll_frame)
        label = tk.Label(self.scroll_frame, image=img)
        label.pack()
        label.image = img 

        # TITEL (jetzt im scroll_frame statt INTERFACE)
        tk.Label(self.scroll_frame, text=text["Title"], font=("Arial", 14, "bold")).pack()
        
        # BESCHREIBUNG (jetzt im scroll_frame)
        tk.Label(self.scroll_frame, text=text["Description"], pady=10).pack()

        # ZUTATEN (hier hattest du "root" stehen, sollte wohl auch in den scroll_frame)
        self.ingredients_vars = {}
        for ingredient, amount in text["Ingredients"].items():
            var = tk.BooleanVar()


            cb = tk.Checkbutton(
                self.scroll_frame,
                text=f"{ingredient} {amount}",
                variable=var
            )

            cb.pack(anchor="w", padx=20)
            self.ingredients_vars[f"{ingredient}"] = var

            

        def addToShoppingList():

            with open(f"{self.dir_name}/RecipeFinder/Recipes/{recipe}.json", mode="r", encoding="utf-8") as f:
                data = json.load(f)
            data["Done"] = True
            with open(f"{self.dir_name}/RecipeFinder/Recipes/{recipe}.json", mode="w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            for ingredient, amount in text["Ingredients"].items():
                if self.ingredients_vars[f"{ingredient}"].get() == False:
                    try:
                        self.ingredients[f"{ingredient}"] = [self.ingredients[f"{ingredient}"][0], [True, f"{amount}"]]
                    except KeyError:
                        self.ingredients[f"{ingredient}"] = [simpledialog.askstring("Kategorie", f"Welcher Kategorie würdest du {ingredient} zuordnen?")][0], [True, f"{amount}"]

                    print(self.ingredients[f"{ingredient}"])
            with open(f"{self.dir_name}/RecipeFinder/Ingredients/ingredients.json", mode="w", encoding="utf-8") as f:
                json.dump(self.ingredients, f, ensure_ascii=False, indent=4)
        def generateButtons():
            # Button auch in den scroll_frame packen!
            # Prüfen, ob die Variable existiert UND das Widget im GUI noch lebt
            if hasattr(self, "Button") and self.Button is not None and self.Button.winfo_exists():
                if text["Liked"]:
                    self.Button.config(image=self.pictograms["Liked"], text="Aus Favoriten entfernen")
                else:
                    self.Button.config(image=self.pictograms["Favorite"], text="Zu Favoriten hinzufügen")
            else:
                # Falls der Button zerstört wurde oder noch nie existierte, neu erstellen
                self.Button = tk.Button(self.scroll_frame, image=self.pictograms["Liked" if text["Liked"] else "Favorite"], 
                                        text="...", compound="left", command=toggle_favorite)
                self.Button.pack(pady=10)


        generateButtons()

        tk.Button(self.scroll_frame, text="Auf die Zutatenliste setzten", image=self.pictograms["Start"], compound="left", command=addToShoppingList).pack()

        # WICHTIG: Damit das Scrollen funktioniert
        self.scroll_frame.update_idletasks()
        self.recipecanvas.config(scrollregion=self.recipecanvas.bbox("all"))




        generateButtons()

        # Am Ende der Funktion openRecipe:
        self.INTERFACE.update_idletasks() # Wichtig: Erst alles zeichnen lassen
        region = self.recipecanvas.bbox("all")
        self.recipecanvas.config(scrollregion=region)

        



        
    
    def doTheSearch(self, event=None):
        if self.DEBUG:
            print(f"Searching for '{self.searchEntry.get()}'")
        alle_dateien = []
        
        
        
        query = self.searchEntry.get().lower().strip()
        if query == "suche ein rezept":
            return
        

        # 1. UI zurücksetzen (wie in opencategorie)
        for widget in self.INTERFACE.winfo_children():
            widget.destroy()

        
        self.searchEntry = ttk.Entry(self.INTERFACE, width=self.breite-180)
        
        self.searchEntry.pack()
        original_img = cairosvg.svg2png(url=f"{self.dir_name}/RecipeFinder/Pictograms/search.svg")
        original_img = Image.open(io.BytesIO(original_img))
        original_img = original_img.resize((16, 16)) 
        self.pictograms["Small_Search"]  = ImageTk.PhotoImage(original_img)
        searchimagecanvas = tk.Canvas(self.INTERFACE, width=20, height=20)
        searchimagecanvas.place(x="63.15c",y=0)
        searchimagecanvas.create_image(0,0,anchor="nw",image=self.pictograms["Small_Search"])

        searchimagecanvas.bind("<Button-1>", self.doTheSearch)

        # 2. Alle Dateien finden (Bilder ausschließen)
        alle_dateien = []
        path = f'{self.dir_name}/RecipeFinder/Recipes'
        for root, dirs, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                if "Pictures" not in full_path:
                    alle_dateien.append(full_path)

        # 3. Rezepte filtern, deren Titel den Suchbegriff enthält
        found_recipes = []
        for data in alle_dateien:
            try:
                with open(data, mode="r", encoding="utf-8") as f:
                    JSONData = json.load(f)
                
                # Suche im Titel (Case-Insensitive)
                if query in JSONData["Title"].lower():
                    # Bereinigung der Kategorie wie im Original
                    JSONData["Category"] = JSONData["Category"].strip()
                    found_recipes.append(JSONData)
            except Exception as e:
                if self.DEBUG: print(f"Fehler beim Laden von {data}: {e}")

        # 4. GUI Aufbau (Canvas & Scrollbar)
        self.categoriecanvas = tk.Canvas(self.INTERFACE)
        self.scrollbar = tk.Scrollbar(self.INTERFACE, orient="vertical", command=self.categoriecanvas.yview)
        self.categoriecanvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.categoriecanvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.categoriecanvas)
        self.categoriecanvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Scroll-Bereich aktualisieren, wenn sich der Frame füllt
        self.scroll_frame.bind("<Configure>", lambda e: self.categoriecanvas.configure(scrollregion=self.categoriecanvas.bbox("all")))

        self.recipe_assets = {}
        row, column = 0, 0
        current_ui_width = self.INTERFACE.winfo_width()
        if current_ui_width < 100: current_ui_width = self.breite

        # 5. Gefundene Rezepte anzeigen
        for recipe in found_recipes:
            title = recipe["Title"]
            img_path = f"{self.dir_name}/RecipeFinder/Recipes/Pictures/{title}.png"
            
            try:
                orig = Image.open(img_path)
                photo = self.get_resized_photo(orig, current_ui_width)
                
                frame = tk.Frame(self.scroll_frame, relief="solid", borderwidth=1)
                frame.grid(row=row, column=column, padx=5, pady=5)

                btn_img = tk.Button(frame, image=photo, command=lambda t=title: self.openRecipe(recipe=t))
                btn_img.pack()
                btn_img.image = photo 
                
                tk.Button(frame, text=title, font=("Arial", 14, "bold"), command=lambda t=title: self.openRecipe(recipe=t)).pack()
                if recipe["Liked"] == True:
                    tk.Button(frame, image=self.pictograms["Liked"], command=lambda t=title: self.openRecipe(recipe=t)).place(x=0, y=0)

                self.recipe_assets[title] = [orig, btn_img]

                column += 1
                if column == 3:
                    column = 0
                    row += 1
            except Exception as e:
                if self.DEBUG: print(f"Bildfehler bei {title}: {e}")






    def Home(self, event=None):
        # 1. Clear previous UI elements
        for widget in self.INTERFACE.winfo_children():
            widget.destroy()
        if self.DEBUG:
            print("HOME")

        tk.Label(self.INTERFACE, text="Für dich empfohlen:", font=("arial", 15, "bold")).pack(anchor="w", padx=10, pady=5)

        # 2. Setup Canvas and Scrollbar Components
        self.categoriecanvas = tk.Canvas(self.INTERFACE, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.INTERFACE, orient="vertical", command=self.categoriecanvas.yview)
        self.categoriecanvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.categoriecanvas.pack(side="left", fill="both", expand=True)

        # Container frame inside canvas
        self.scroll_frame = tk.Frame(self.categoriecanvas)
        
        # Create the window and keep a reference to its ID to configure width later
        canvas_window = self.categoriecanvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # --- CRITICAL SCROLL FIXES ---
        # Fix A: Update scroll region automatically when widgets are added
        self.scroll_frame.bind(
            "<Configure>", 
            lambda e: self.categoriecanvas.configure(scrollregion=self.categoriecanvas.bbox("all"))
        )
        
        # Fix B: Make sure the scroll frame expands to match the window width
        self.categoriecanvas.bind(
            "<Configure>", 
            lambda e: self.categoriecanvas.itemconfig(canvas_window, width=e.width)
        )
        # -----------------------------

        # 3. File discovery and loading (Optimized to prevent syntax token errors)
        alle_dateien = []
        path = os.path.join(self.dir_name, 'RecipeFinder', 'Recipes')
        
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                if "Pictures" in root:
                    continue
                for file in files:
                    if file.endswith('.json'):
                        alle_dateien.append(os.path.join(root, file))

        found_recipes = []
        for data in alle_dateien:
            try:
                with open(data, mode="r", encoding="utf-8") as f:
                    JSONData = json.load(f)
                
                found_recipes.append(JSONData)
                # Fixed double quote syntax error inside string dictionary access
                title_key = JSONData["Title"]
                self.recipes[title_key] = JSONData
            except (FileNotFoundError, json.JSONDecodeError):
                if self.DEBUG:
                    print(f"Fehler beim Laden von: {data}")

        # 4. Calculate Stats
        stats = {str(category): 0 for category in self.categories}

        for recipe_title, recipe_data in self.recipes.items():
            if recipe_data.get("Liked") == True:
                cat = recipe_data.get("Category")
                if cat in stats:
                    stats[cat] += 1

        self.recipe_assets = {}
        self.row = 0
        
        def show_categorie():
            column = 0
            if not stats:
                return
                
            # Find category with most likes
            biggest = max(stats, key=stats.get)
            categorie = biggest
            
            # UI Category Header
            tk.Label(self.scroll_frame, text=f"{categorie}", font=("Arial", 15, "bold")).grid(row=self.row, column=0, sticky="w", columnspan=3, pady=(10, 2))
            self.row += 1
            
            current_ui_width = self.INTERFACE.winfo_width()
            if current_ui_width < 100:
                current_ui_width = self.breite
            
            # Render recipes inside this category row layout
            for recipe_title, recipe_data in self.recipes.items():
                if recipe_data.get("Category") == categorie:
                    title = recipe_data["Title"]
                    img_path = os.path.join(self.dir_name, 'RecipeFinder', 'Recipes', 'Pictures', f"{title}.png")
                    
                    try:
                        orig = Image.open(img_path)
                        photo = self.get_resized_photo(orig, current_ui_width)
                        
                        frame = tk.Frame(self.scroll_frame, relief="solid", borderwidth=1)
                        frame.grid(row=self.row, column=column, padx=5, pady=5, sticky="nsew")

                        btn_img = tk.Button(frame, image=photo, command=lambda t=title: self.openRecipe(recipe=t))
                        btn_img.pack()
                        btn_img.image = photo 
                        
                        tk.Button(frame, text=title, font=("Arial", 14, "bold"), command=lambda t=title: self.openRecipe(recipe=t)).pack()
                        
                        if recipe_data.get("Liked") == True:
                            btn_like = tk.Button(frame, image=self.pictograms["Liked"], command=lambda t=title: self.openRecipe(recipe=t))
                            btn_like.place(x=0, y=0)
                            btn_like.image = self.pictograms["Liked"]

                        self.recipe_assets[title] = [orig, btn_img]
                    except Exception as e:
                        if self.DEBUG:
                            print(f"Error loading image for {title}: {e}")

                    column += 1
                    if column == 3:
                        column = 0
                        self.row += 1
            
            if column != 0:
                self.row += 1
                
            del stats[categorie]

        # Render loop using a copy of keys list
        for _ in list(self.categories):
            try:
                show_categorie()
            except KeyError:
                continue

        
        
    def create_recipe_card(self, parent, recipe, title, photo, orig, row, column):
        # Setting an explicit size for the card prevents Tkinter frames from collapsing
        frame = tk.Frame(parent, relief="solid", borderwidth=1, width=self.breite/2, height=self.hoehe/2)
        frame.grid(row=row, column=column, padx=5, pady=5)
        

        # Image background
        img_label = tk.Label(frame, image=photo)
        img_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Centralized action button
        btn = tk.Button(
            frame,
            text=title,
            font=("Arial", 14, "bold"),
            command=lambda t=title: self.openRecipe(recipe=t)
        )
        btn.place(relx=0.5, rely=0.8, anchor="s")

        # Overlay liked icon if applicable
        if recipe.get("Liked"):
            tk.Label(frame, image=self.pictograms["Liked"]).place(x=0, y=0)

        # Store references using unique titles to prevent Garbage Collection from wiping images
        self.recipe_assets[title] = {
            "orig": orig,
            "photo": photo,
            "label": img_label
        }

        return frame

    def Favorits(self, event=None):
        # 1. Clear previous UI elements
        for widget in self.INTERFACE.winfo_children():
            widget.destroy()

        if self.DEBUG:
            print("FAVORITS")

        # Global dictionary to retain image references across both sections
        self.recipe_assets = {}

        # Get accurate target UI width for dynamic resizing
        current_ui_width = self.INTERFACE.winfo_width()
        if current_ui_width < 100:
            current_ui_width = self.breite

        # 2. Optimization: Read files from disk EXACTLY ONCE
        favoriten_recipes = []
        neue_ideen_recipes = []
        
        recipes_path = os.path.join(self.dir_name, 'RecipeFinder', 'Recipes')

        if os.path.exists(recipes_path):
            for root, dirs, files in os.walk(recipes_path):
                # Skip checking inside the Pictures directory entirely for faster loops
                if "Pictures" in root:
                    continue
                    
                for file in files:
                    if file.endswith('.json'): # Explicitly look for data files
                        full_path = os.path.join(root, file)
                        try:
                            with open(full_path, mode="r", encoding="utf-8") as f:
                                recipe_data = json.load(f)
                            
                            # Sort into categories in memory
                            if recipe_data.get("Liked"):
                                if recipe_data.get("Done"):
                                    favoriten_recipes.append(recipe_data)
                                else:
                                    neue_ideen_recipes.append(recipe_data)
                                    
                        except Exception as e:
                            if self.DEBUG:
                                print(f"Fehler beim Laden von {file}: {e}")

        # --- Section 1: Favoriten ---
        tk.Label(self.INTERFACE, text="Deine Favoriten:", font=("Arial", 15, "bold")).grid(row=0, column=0, sticky="w", padx=10)

        fav_canvas = tk.Canvas(self.INTERFACE, height=self.hoehe/2.5)
        fav_scrollbar = tk.Scrollbar(self.INTERFACE, orient="horizontal", command=fav_canvas.xview)
        fav_canvas.configure(xscrollcommand=fav_scrollbar.set)

        fav_scrollbar.grid(row=1, column=0, sticky="ew")
        fav_canvas.grid(row=2, column=0, sticky="ew")

        fav_scroll_frame = tk.Frame(fav_canvas)
        fav_canvas.create_window((0, 0), window=fav_scroll_frame, anchor="nw")

        for idx, recipe in enumerate(favoriten_recipes):
            title = recipe["Title"]
            img_path = os.path.join(recipes_path, "Pictures", f"{title}.png")
            
            try:
                orig = Image.open(img_path)
                photo = self.get_resized_photo(orig, current_ui_width)
                self.create_recipe_card(fav_scroll_frame, recipe, title, photo, orig, 0, idx)
            except Exception as e:
                print(f"Image error for {title}: {e}")

        fav_scroll_frame.update_idletasks()
        fav_canvas.configure(scrollregion=fav_canvas.bbox("all"))


        # --- Section 2: Neue Ideen ---
        tk.Label(self.INTERFACE, text="Neue Ideen:", font=("Arial", 15, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=(15, 0))

        ideen_canvas = tk.Canvas(self.INTERFACE, height=self.hoehe/2.5)
        ideen_scrollbar = tk.Scrollbar(self.INTERFACE, orient="horizontal", command=ideen_canvas.xview)
        ideen_canvas.configure(xscrollcommand=ideen_scrollbar.set)

        ideen_scrollbar.grid(row=4, column=0, sticky="ew")
        ideen_canvas.grid(row=5, column=0, sticky="ew")

        ideen_scroll_frame = tk.Frame(ideen_canvas)
        ideen_canvas.create_window((0, 0), window=ideen_scroll_frame, anchor="nw")

        for idx, recipe in enumerate(neue_ideen_recipes):
            title = recipe["Title"]
            img_path = os.path.join(recipes_path, "Pictures", f"{title}.png")
            
            try:
                orig = Image.open(img_path)
                photo = self.get_resized_photo(orig, current_ui_width)
                self.create_recipe_card(ideen_scroll_frame, recipe, title, photo, orig, 0, idx)
            except Exception as e:
                print(f"Image error for {title}: {e}")

        ideen_scroll_frame.update_idletasks()
        ideen_canvas.configure(scrollregion=ideen_canvas.bbox("all"))

        


        
    def get_resized_photo(self, img_original, current_width):
            new_width = int(current_width / 3)
            new_width = max(new_width, 50) # Mindestbreite
            
            aspect = img_original.height / img_original.width
            new_height = int(new_width * aspect)
            
            resized = img_original.resize((new_width, new_height), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized)
    def opencategorie(self, categorie):
        
        
        

        # Widgets leeren
        for widget in self.INTERFACE.winfo_children():
            widget.destroy()
        if self.DEBUG:
            print("OPEN CATEGORY")

        alle_dateien = []
        for root, dirs, files in os.walk(f'{self.dir_name}/RecipeFinder/Recipes'):
            for file in files:
                alle_dateien.append(os.path.join(root, file))
                if "Pictures" in alle_dateien[-1]:
                    alle_dateien.pop()

        if self.DEBUG:
            print(alle_dateien)
        
        self.recipes[f"{categorie}"] = []
        for data in alle_dateien:
            with open(f"{data}", mode="r", encoding="utf-8") as f:
                JSONData = json.load(f)
            if JSONData["Category"].replace("                                ", "") == categorie:
                JSONData["Category"] = JSONData["Category"].replace("                                ", "")
                self.recipes[f"{categorie}"].append(JSONData)
        #Example Data
        #{
            #"Title": "Ramen",
            #"Description": "xyz\n",
            #"Category": "                                Suppen                                "
        #}
        
        if self.DEBUG:
            print(f"{JSONData}")
            print(f"{self.recipes}")

        
        self.categoriecanvas = tk.Canvas(self.INTERFACE)
        self.scrollbar = tk.Scrollbar(self.INTERFACE, orient="vertical", command=self.categoriecanvas.yview)
        self.categoriecanvas.configure(yscrollcommand=self.scrollbar.set)
        

        
        self.scrollbar.pack(side="right", fill="y")
        self.categoriecanvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.categoriecanvas)
        self.categoriecanvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # WICHTIG: Speicher für Originalbilder und Button-Referenzen
        self.recipe_assets = {} # Speichert { "Titel": [OriginalImage, ButtonWidget] }

        row, column = 0, 0
        # Aktuelle Breite für die Erstberechnung holen
        current_ui_width = self.INTERFACE.winfo_width() 
        if current_ui_width < 100: current_ui_width = self.breite # Fallback falls noch nicht gerendert

        for recipe in self.recipes[f"{categorie}"]:
            title = recipe["Title"]
            img_path = f"{self.dir_name}/RecipeFinder/Recipes/Pictures/{title}.png"
            
            # 1. Original laden und im Speicher behalten
            orig = Image.open(img_path)
            photo = self.get_resized_photo(orig, current_ui_width)
            
            # 2. UI Elemente erstellen
            frame = tk.Frame(self.scroll_frame, relief="solid", borderwidth=1)
            frame.grid(row=row, column=column, padx=5, pady=5)

            

            btn_img = tk.Button(frame, image=photo, command=lambda t=title: self.openRecipe(recipe=t))
            btn_img.pack()
            # Referenz im Button-Objekt speichern gegen Garbage Collection
            btn_img.image = photo 
            
            tk.Button(frame, text=title, font=("Arial", 14, "bold"), command=lambda t=title: self.openRecipe(recipe=t)).pack()
            if recipe["Liked"] == True:
                tk.Button(frame, image=self.pictograms["Liked"], command=lambda t=title: self.openRecipe(recipe=t)).place(x=0, y=0)

            # 3. Für späteres Resizing registrieren
            self.recipe_assets[title] = [orig, btn_img]

            column += 1
            if column == 3:
                column = 0
                row += 1

    

    
    def Ingredients(self, event=None):
        # 1. Wipe previous widgets cleanly
        for widget in self.INTERFACE.winfo_children():
            widget.destroy()

        if self.DEBUG:
            print("INGREDIENTS")

        # 2. Prevent stacking event traces on UI rebuilds
        if not hasattr(self, 'didIngredients') or self.didIngredients == False:
            self.search_var = tk.StringVar(value="Füge eine Zutat hinzu")
            self.didIngredients = True
        else:
            # If text is lingering, clear it out safely
            self.search_var = tk.StringVar(value="")

        # Load Shopping list configuration data safely
        shopping_list_path = os.path.join(self.dir_name, "RecipeFinder", "Ingredients", "shoppingList.json")
        ingredients_path = os.path.join(self.dir_name, "RecipeFinder", "Ingredients", "ingredients.json")
        
        try:
            with open(shopping_list_path, mode="r", encoding="utf-8") as f:
                Shopping = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            Shopping = {}

        # --- TOP SECTION: Matching Ingredients (Horizontal Scroll) ---
        tk.Label(self.INTERFACE, text="Deine Zutaten:", font=("Arial", 15, "bold")).grid(row=0, column=0, sticky="w", padx=10)

        self.ingredientcanvas = tk.Canvas(self.INTERFACE, width=self.breite-150, height=120, highlightthickness=0)
        # Fixed: Gave this its own unique instance name to prevent overwriting
        self.horiz_scrollbar = tk.Scrollbar(self.INTERFACE, orient="horizontal", command=self.ingredientcanvas.xview)
        self.ingredientcanvas.configure(xscrollcommand=self.horiz_scrollbar.set)

        self.ingredientcanvas.grid(row=2, column=0, sticky="ew", padx=10)
        self.horiz_scrollbar.grid(row=3, column=0, sticky="ew", padx=10)

        self.scroll_frame = tk.Frame(self.ingredientcanvas)
        self.ingredientcanvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Dynamic scroll calculation trigger for Top Canvas
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.ingredientcanvas.configure(scrollregion=self.ingredientcanvas.bbox("all"))
        )

        # --- BOTTOM SECTION: Shopping List (Vertical Scroll) ---
        tk.Label(self.INTERFACE, text="Einkaufsliste", font=("Arial", 15, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=(15, 2))

        # Keep layout container dimensions bounded
        self.shoppinglistcanvas = tk.Canvas(self.INTERFACE, width=self.breite-150, height=300, highlightthickness=0)
        # Fixed: Gave this its own unique instance name to prevent overwriting
        self.vert_scrollbar = tk.Scrollbar(self.INTERFACE, orient="vertical", command=self.shoppinglistcanvas.yview)
        self.shoppinglistcanvas.configure(yscrollcommand=self.vert_scrollbar.set)

        self.shoppinglistcanvas.grid(row=6, column=0, sticky="nsew", padx=10)
        self.vert_scrollbar.grid(row=6, column=1, sticky="ns")

        scroll = tk.Frame(self.shoppinglistcanvas)
        self.shoppinglistcanvas.create_window((0, 0), window=scroll, anchor="nw")

        # Dynamic scroll calculation trigger for Bottom Canvas
        scroll.bind(
            "<Configure>",
            lambda e: self.shoppinglistcanvas.configure(scrollregion=self.shoppinglistcanvas.bbox("all"))
        )

        # --- ACTION MECHANICS & CALLBACKS ---
        def checkIfMatching(*args):
            # Clear matching section UI dynamically
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()
                
            self.matchingIngredients = {}
            search_term = self.search_var.get().lower()
            
            if not search_term or search_term == "füge eine zutat hinzu":
                return

            for part, category in self.ingredients.items():
                if search_term in part.lower():
                    self.matchingIngredients[part] = category

            col_idx = 0
            for name, kategorie in self.matchingIngredients.items():
                # Check safely if item is initialized and not flagged on list
                if len(kategorie) > 1 and kategorie[1] is False:
                    # Setting reasonable heights so buttons don't clip your canvas bounds
                    tk.Button(
                        self.scroll_frame, 
                        text=name, 
                        height=2, 
                        width=18, 
                        padx=5, 
                        command=lambda i=name: addtoShoppingList(ingredient=i)
                    ).grid(row=0, column=col_idx, padx=5, pady=5, sticky="s")
                    col_idx += 1

        def addtoShoppingList(ingredient):
            notes = simpledialog.askstring("Notizen", "Willst du noch Notizen hinzufügen?")
            notes_content = notes if notes else ""
            
            # Match data mapping layout requirements safely
            self.ingredients[str(ingredient)] = [self.ingredients[str(ingredient)][0], [True, notes_content]]
            
            with open(ingredients_path, mode="w", encoding="utf-8") as f:
                json.dump(self.ingredients, f, ensure_ascii=False, indent=4)
            self.Ingredients() # Reload cleanly

        def removefromShoppingList(ingredient):
            self.ingredients[str(ingredient)] = [self.ingredients[str(ingredient)][0], False]
            
            with open(ingredients_path, mode="w", encoding="utf-8") as f:
                json.dump(self.ingredients, f, ensure_ascii=False, indent=4)
            self.Ingredients() # Reload cleanly

        # Text entry field configuration
        ingrediententry = tk.Entry(self.INTERFACE, width=40, textvariable=self.search_var)
        ingrediententry.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        
        # Trace logic binds strictly after functional callbacks initialize
        self.search_var.trace_add("write", checkIfMatching)

        # --- RENDER EINKAUFSLISTE CARDS ---
        row_idx = 0
        col_idx = 0

        for name, kategorie in self.ingredients.items():
            if isinstance(kategorie, list) and len(kategorie) > 1 and kategorie[1] != False:
                note_text = kategorie[1][1] if len(kategorie[1]) > 1 else ""
                display_label = f"{name}\n\n({note_text})" if note_text else f"{name}"
                
                tk.Button(
                    scroll, 
                    text=display_label, 
                    height=4, 
                    width=18, 
                    padx=5, 
                    pady=5,
                    wraplength=120,
                    command=lambda i=name: removefromShoppingList(ingredient=i)
                ).grid(row=row_idx, column=col_idx, padx=5, pady=5)
                
                col_idx += 1
                if col_idx == 4:
                    row_idx += 1
                    col_idx = 0
    



        

    def askforImage(self):
        
        file_path = filedialog.askopenfilename(
            filetypes=[("Alle Bilder", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp")]
        )

        if not file_path:
            return

        img = Image.open(file_path).convert("RGBA")

        # --- skalieren auf 514x514 ---
        img = img.resize((514, 514), Image.Resampling.LANCZOS)

        base = os.path.splitext(file_path)[0]
        new_path = base + ".png"

        img.save(new_path, "PNG")

        self.image = new_path
            


    def Create(self, event=None):
        RecipeIngredients = {}
        # 1. Die StringVar definieren
        self.search_var = tk.StringVar()
        self.RecipeIngredients = {}
        def checkIfMatching(*args):
            selected_item = self.tree.focus()
            print(f"Test{self.tree.item(selected_item)}")
            print(selected_item)
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            self.matchingIngredients = {}
            search_term = self.search_var.get().lower()

            for part, category in self.ingredients.items():
                if search_term in part.lower():
                    self.matchingIngredients[part] = category
            for name, kategorie in self.matchingIngredients.items():
                self.tree.insert("", "end", values=(name, kategorie[0]), text=f"{name}")
                
                if self.DEBUG:
                    print(name)
                    print(kategorie)
            
        

        def save():
            index = self.Listbox.curselection()
            if not index:
                return
            category = self.Listbox.get(index)
            self.ziel = f"{self.dir_name}/RecipeFinder/Recipes/Pictures/{self.NewRecipeTitle.get()}.png"
            with open(self.image, 'rb') as f_src:
                with open(self.ziel, 'wb') as f_dst:
                    f_dst.write(f_src.read())

            with open(f"{self.dir_name}/RecipeFinder/Recipes/{self.NewRecipeTitle.get()}.json", mode="w", encoding="utf-8") as f:
                json.dump({"Title": f"{self.NewRecipeTitle.get()}", "Description": f"{self.NewRecipe.get(1.0, "end")}", "Category": f"{category.replace(" ", "")}", "Ingredients": RecipeIngredients, "Liked": False, "Done": False}, f, indent=4,ensure_ascii=False)
            self.openRecipe(recipe=self.NewRecipeTitle.get())
        def askForCategory():
            selected_item = self.tree.focus()
            print(f"Test{self.tree.item(selected_item)}")
            selected_item = self.tree.item(selected_item)["text"]
            print(selected_item)
            newIngredient = selected_item
            
            
            if not newIngredient:
                name = self.search_var.get()
                category = simpledialog.askstring("Kategorie", f"Welcher Kategorie würdest du {name} zuordnen?")
                if category:
                    self.ingredients[name] = (category, False)
                    checkIfMatching()

                    with open(f"{self.dir_name}/RecipeFinder/Ingredients/ingredients.json", mode="w", encoding="utf-8") as f:
                        json.dump(self.ingredients, f, ensure_ascii=False, indent=4)

            elif newIngredient:
                print("NewIngredient:")
                print(newIngredient)
                RecipeIngredients[f"{newIngredient}"] = simpledialog.askstring("Beschreibung", "Willst du eine Beschreibung hinzufügen?\nFalls du willst, gib sie bitte hier ein.")


        for widget in self.INTERFACE.winfo_children():
            widget.destroy()

        recipeframe = tk.Frame(self.INTERFACE)
        ingredientframe = tk.Frame(self.INTERFACE)
        self.addIngredient = ttk.Entry(ingredientframe, width=50, textvariable=self.search_var)
        self.addIngredient.grid(row=0, column=1)

        
        self.search_var.trace_add("write", checkIfMatching)

        
        self.tree = ttk.Treeview(ingredientframe, columns=("Name", "Kategorie"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Kategorie", text="Kategorie")
        self.tree.grid(pady=20, padx=0, row=1, column=1)



        
        checkIfMatching()
        
        
        if self.DEBUG:
            recipeframe.config(bg="yellow")
            ingredientframe.config(bg="grey")
        recipeframe.grid(row=0, column=0)
        ingredientframe.grid(row=0, column=1)
        AddCategory = ttk.Button(ingredientframe, text="Zutat hinzufügen", image=self.pictograms["Add"], compound="left", command=askForCategory)
        AddCategory.grid(row=2, column=1)


        self.NewRecipeTitle = tk.Entry(recipeframe, width=40)
        self.NewRecipeTitle.grid(row=0,column=1, padx=40, pady=20)
        tk.Label(recipeframe, text="Titel eingeben", image=self.pictograms[1], compound="left").grid(row=0, column=0, padx=40,pady=20)


        tk.Label(recipeframe, text="Rezept eingeben", image=self.pictograms[2], compound="left").grid(row=1, column=0, padx=40,pady=20)
        self.NewRecipe = tk.Text(recipeframe, width=40, height=40)
        self.NewRecipe.grid(row=1,column=1, padx=40,pady=20)

        tk.Label(recipeframe, text="Bild hinzufügen", image=self.pictograms[3], compound="left").grid(row=2, column=0)
        addimagebutton = ttk.Button(recipeframe, text="Bild hinzufügen", image=self.pictograms["Image"], compound="left", command=self.askforImage)
        addimagebutton.grid(row=2,column=1, pady=20)

        tk.Label(recipeframe, text="Kategorie hinzufügen", image=self.pictograms[4], compound="left").grid(row=3, column=0)
        self.Listbox = tk.Listbox(recipeframe, highlightthickness=0, selectbackground=self.standart_color, activestyle="none", width=40)
        self.Listbox.grid(row=3, column=1)

        tk.Label(recipeframe, text="Speichern", image=self.pictograms[5], compound="left").grid(row=4, column=0, padx=40, pady=20)
        saveButton = ttk.Button(recipeframe, text="Speichern", image=self.pictograms["Save"], compound="left", command=save)
        saveButton.grid(row=4, column=1)

        for category in self.categories:
            category = category.center(70)
            self.Listbox.insert(tk.END, category)

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    recipefinder = RecipeFinder(root)
    recipefinder.run()
