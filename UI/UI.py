from tkinter import ttk
import tkinter as tk
import ctypes
from PIL import Image, ImageTk
from requestsAPI import requestsAPI
from Models import models
from Utils import utils


class FullscreenBackgroundWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.min_width = 600
        self.min_height = 600
        self.screen_resolution = str(self.width)+'x'+str(self.height)
        self.root = tk.Tk()
        self.root.title("MTG Price Checker or How I Tried to Drop Java and Love Python")
        self.root.iconbitmap("mtgpc.ico")
        self.root.geometry(self.screen_resolution)
        self.root.state("zoomed")

        # Create resources necessary for the app's functions
        self.requests = requestsAPI.Requests()
        self.deck = models.Deck(0, 'New Deck', [])
        
        # Load background image
        self.background_path = "background.jpg"  # Change the path to your image file
        self.background_image = Image.open(self.background_path)
        self.background_photo = None
        self.background_label = None

        # Create canvas for background image
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # Create menus
        self.create_menus()

        # Bind canvas to window resizing
        self.canvas.bind("<Configure>", self.resize_background)

        # Run Window
        self.run()

    def create_menus(self):
        # Create Menus
        self.frame_preview_menu = tk.Frame(self.canvas, borderwidth=6)
        self.frame_preview_menu.place(rely=0, relwidth=0.2, relheight=0.5)
        self.preview_menu = PreviewMenu(self.frame_preview_menu, self)

        self.frame_search_menu = tk.Frame(self.canvas)
        self.frame_search_menu.place(rely=0.5, relwidth=0.2, relheight=0.5)
        self.search_menu = SearchMenu(self.frame_search_menu, self)

        self.frame_decklist_menu = tk.Frame(self.canvas)
        self.frame_decklist_menu.place(relx=0.8, relwidth=0.2, relheight=1)
        self.decklist_menu = DecklistMenu(self.frame_decklist_menu, self)

        self.frame_info_menu = tk.Frame(self.canvas)
        self.frame_info_menu.place(relx=0.2, relwidth=0.6, relheight=0.13)
        self.info_menu = InfoMenu(self.frame_info_menu, self)

        self.frame_buttons_menu = tk.Frame(self.canvas)
        self.frame_buttons_menu.place(
            relx=0.2, rely=0.95, relwidth=0.6, relheight=0.05)
        self.buttons_menu = ButtonsMenu(self.frame_buttons_menu, self)

        # self.frame_statistics_menu = tk.Frame(self.canvas, bg='white')
        # self.frame_statistics_menu.place(relx=0.25, rely=0.2, relwidth=0.55, relheight=0.6)

    def resize_background(self, *args):
        # Resize background image to match window dimensions
        self.user32 = ctypes.windll.user32

        if self.user32.GetSystemMetrics(0) < self.min_width:
            self.window_width = self.min_width
        else:
            self.window_width = self.user32.GetSystemMetrics(0)

        if self.user32.GetSystemMetrics(1) < self.min_height:
            self.window_height = self.min_height
        else:
            self.window_height = self.user32.GetSystemMetrics(1)

        self.background_image = self.background_image.resize(
            (self.window_width, self.window_height), Image.ANTIALIAS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        if self.background_label:
            self.canvas.delete(self.background_label)

        self.background_label = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_photo)

        if self.decklist_menu.decklist_selection != None:
            for card in self.deck.card_list:
                if (str(card.quantity)+'x '+str(card.name)) == self.decklist_menu.decklist_selection:
                    self.decklist_menu.set_card_image(card.image)

    def run(self):
        self.resize_background()
        self.root.mainloop()


class InfoMenu:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent

        self.deck_name = self.parent.deck.deck_name
        self.nr_cards = str(self.parent.deck.get_nr_cards())
        self.total_cost = str(self.parent.deck.get_total_cost())

        self.basic_info_frame = tk.Frame(self.root)
        self.basic_info_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.deck_name_label = tk.Label(
            self.basic_info_frame, text='Deck name:   '+self.parent.deck.deck_name, anchor='w') #bg='yellow'
        self.deck_name_label.place(
            relx=0, rely=0.1, relwidth=0.5, relheight=0.15)

        self.nr_cards_label = tk.Label(
            self.basic_info_frame, text='Nr of cards:   '+self.nr_cards, anchor='w') #bg = 'orange'
        self.nr_cards_label.place(
            relx=0, rely=0.25, relwidth=0.5, relheight=0.15)
        
        self.total_cost_label = tk.Label(
            self.basic_info_frame, text='Deck\'s Total Cost:   '+self.total_cost, anchor='w') #bg = 'yellow'
        self.total_cost_label.place(
            relx=0, rely=0.4, relwidth=0.5, relheight=0.15)
        
    def update_data(self):
        self.deck_name = self.parent.deck.deck_name
        self.nr_cards = str(self.parent.deck.get_nr_cards())
        self.total_cost = str(self.parent.deck.get_total_cost())
        self.deck_name_label.config(text='Deck name:   '+self.deck_name)
        self.nr_cards_label.config(text='Nr of cards:   '+self.nr_cards)
        self.total_cost_label.config(text='Deck\'s Total Cost:   ' + str("{:.2f}".format(float(self.total_cost))) + '€')


class PreviewMenu:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent

        self.requests = self.parent.requests
        self.card_canvas = tk.Canvas(self.root, bg='white')
        self.card_canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.card = None
        self.card_image = None
        self.display_second_face = False
        self.change_face_button = ttk.Button(self.card_canvas, text='Rotate Card', command=self.change_card_face_display_command)

    def set_card(self, card):
        if card != None:
            self.card = card
        
        if self.card.second_face_name == None:
            self.display_second_face = False

        if self.display_second_face == False:
            self.change_card_image(self.card.image)
        else:
            self.change_card_image(self.card.second_face_image)

    def change_card_image(self, card_image):
        new_image = card_image

        image_width, image_height = new_image.size
        image_ratio = image_width / image_height

        # Clean canvas
        self.card_canvas.delete("all")

        # Resize the image to fit the frame size

        canvas_size = (self.card_canvas.winfo_width() - 30,
                       int(round((self.card_canvas.winfo_width() - 30) / image_ratio)))
        resized_image = new_image.resize(canvas_size)

        # Convert the image to a format that can be displayed on a tkinter frame
        photo_image = ImageTk.PhotoImage(resized_image)

        # Set the image on the frame
        self.image_on_canvas = self.card_canvas.create_image(
            int(round(self.card_canvas.winfo_width()/2)), int(round(self.card_canvas.winfo_height()/2)), anchor=tk.CENTER, image=photo_image)

        # Need to keep a reference to the image to avoid garbage collection
        self.card_image = photo_image

        if self.card.second_face_name != None:
            self.change_face_button.place(relx=0.5, rely=0.96, relwidth=0.26, relheight=0.06, anchor=tk.CENTER)
        else:
            self.change_face_button.place_forget()
            self.display_second_face = False

    def change_card_face_display_command(self):
        if self.display_second_face == False:
            self.display_second_face = True
        else:
            self.display_second_face = False

        self.set_card(None)


class SearchMenu:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.preview_menu = parent.preview_menu

        self.requests = self.parent.requests
        self.selection = None
        self.card_selected = None

        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(root, textvariable=self.input_var)
        self.input_entry.place(relx=0.025, rely=0.05,
                               relwidth=0.65, relheight=0.06)
        self.input_entry.bind(
            '<FocusOut>', lambda *args: self.get_card_suggestions())
        self.input_entry.bind(
            '<Return>', lambda event: self.get_card_suggestions())

        # Create a button with a magnifying glass icon
        search_button = ttk.Button(
            root, command=self.get_card_suggestions, text='Search')
        search_button.place(
            relx=0.685, rely=0.05, relwidth=0.29, relheight=0.06)

        self.suggestions_box = tk.Listbox(root, exportselection=False)
        self.suggestions_box.place(
            relx=0.025, rely=0.12, relwidth=0.95, relheight=0.79)

        # Bind the listbox to the select_suggestion() function
        self.suggestions_box.bind(
            '<<ListboxSelect>>', self.select_suggestion)

        self.addtodeck_button = ttk.Button(
            root, text='Add Card To Deck', command=self.add_to_deck_command)
        self.addtodeck_button.place(
            relx=0.05, rely=0.92, relwidth=0.9, relheight=0.06)

    def add_to_deck_command(self):
        self.parent.deck.add_card(self.card_selected)
        self.parent.decklist_menu.update_data()

    # Function to fetch card suggestions from Scryfall API
    def get_card_suggestions(self):
        # Get the text entered in the search box
        search_text = self.input_var.get()
        if len(search_text) >= 3:
            # Call the get_card_autocomplete() function of ScryfallAPI class
            suggestions = self.requests.get_card_autocomplete(search_text)

            # Update the suggestions in the listbox
            self.suggestions_box.delete(0, tk.END)
            for suggestion in suggestions['data']:
                self.suggestions_box.insert(tk.END, suggestion)

    # Function to display image on the preview menu
    def set_card_image(self, card):
        #card_image = self.requests.get_card_image(cardname)
        self.preview_menu.set_card(card)

    # Function to handle selection from the suggestions listbox
    def select_suggestion(self, *args):
        # Get the selected suggestion from the listbox
        if self.selection != self.suggestions_box.get(self.suggestions_box.curselection()):
            self.selection = self.suggestions_box.get(self.suggestions_box.curselection())
            self.card_selected = self.requests.get_card_by_name(self.get_selected_card())
            self.set_card_image(self.card_selected)

    # Class Function that returns the selected suggestion
    def get_selected_card(self):
        return self.selection
    
    def set_selected_card(self, selected_card):
        self.card_selected = selected_card
        self.input_var.set(str(selected_card.name))
        self.selection = selected_card.name


class DecklistMenu:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.preview_menu = self.parent.preview_menu

        self.decklist_selection = None
        self.item = None

        self.basic_info_frame = tk.Frame(self.root) #bg='blue'
        self.basic_info_frame.place(relwidth=1, relheight=0.1)

        self.decklist_frame = tk.Frame(self.root)
        self.decklist_frame.place(rely=0.1, relwidth=1, relheight=0.9)
        
        # Create Treeview
        self.create_decklist_treeview()

        self.delete_card_button = ttk.Button(
            self.root, text='Delete Card', command=self.delete_card)
        self.delete_card_button.place(
            relx=0.03, rely=0.958, relwidth=0.94, relheight=0.032)

    def create_decklist_treeview(self):
        self.decklist_tv = ttk.Treeview(self.decklist_frame, columns=('Name', 'Quantity', 'Price'), show='headings')
        self.decklist_tv.column('Name', minwidth=30, width=60)
        self.decklist_tv.column('Quantity', minwidth=8, width=16)
        self.decklist_tv.column('Price', minwidth=8, width=16)
        self.decklist_tv.heading('Name', text='Name', anchor='w')
        self.decklist_tv.heading('Quantity', text='Quantity', anchor='w')
        self.decklist_tv.heading('Price', text='Price', anchor='w')
        self.decklist_tv.place(relx=0.03, rely=0.03, relwidth=0.94, relheight=0.918)
        self.decklist_tv.bind('<<TreeviewSelect>>', self.select_suggestion)

    def select_suggestion(self, *args):
        # Get the selected suggestion from the listbox
        self.item = self.decklist_tv.item(self.decklist_tv.selection()[0])

        for card in self.parent.deck.card_list:
            if self.item['values'][0] == card.name:
                self.set_card_image(card)
                self.parent.search_menu.set_selected_card(card)

    def set_card_image(self, card):
        self.preview_menu.set_card(card)

    def delete_card(self):
        for card in self.parent.deck.card_list:
            if self.item['values'][0] == card.name:
                self.parent.deck.delete_card(card)

        self.update_data()

    def update_decklist_box(self):
        # Update the suggestions in the listbox
        for item in self.decklist_tv.get_children():
            self.decklist_tv.delete(item)

        for card in self.parent.deck.card_list:
            self.decklist_tv.insert("", "end", values=(card.name, card.quantity, str(card.card_price+'€')))

    def update_data(self):
        self.update_decklist_box()

        # Set Selection back
        try:
            for item in self.decklist_tv.get_children():
                if self.decklist_tv.item(item)['values'][0] == self.item['values'][0]:
                    self.decklist_tv.selection_set(item)
        except:
            pass

        self.parent.info_menu.update_data()


class ButtonsMenu:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent

        self.buttons_list = []
        buttons_text = [('Save', self.save_command), ('Load',
                                                      self.load_command), ('Exit', self.exit_command)]
        buttons_width = 0.1
        buttons_height = 0.7
        buttons_spacing = 1 / len(buttons_text)
        button_x_offset = 1 / len(buttons_text) / 2

        for button in buttons_text:
            new_button = ttk.Button(
                self.root, text=button[0], command=button[1])
            new_button_x = button_x_offset + \
                (buttons_spacing*int(buttons_text.index(button)))
            new_button.place(anchor=tk.CENTER, relx=new_button_x, rely=0.5,
                             relwidth=buttons_width, relheight=buttons_height)
            self.buttons_list.append(new_button)

    def save_command(self):
        deck = self.parent.deck
        utils.Utils().save_deck(deck)

    def load_command(self):
        self.parent.deck = utils.Utils().load_deck()
        self.parent.decklist_menu.update_data()

    def exit_command(self):
        self.parent.root.destroy()
