import os
import json
from pathlib import Path
from PIL import Image
from requestsAPI import requestsAPI
from Models import models
from tkinter import filedialog


class Utils:
    def save_deck(self, deck):
        # Create the MTGDB folder in My Documents if it doesn't exist
        mtgdb_folder = Path.home() / 'Saved Games' / 'MTGDB'
        mtgdb_folder.mkdir(parents=True, exist_ok=True)

        # Create a dictionary representing the deck data
        deck_data = {
            'id': deck.deck_id,
            'name': deck.deck_name,
            'decklist': [{
                'id': card.id,
                'name': card.name,
                'image': card.image_url,
                'quantity': card.quantity,
                'card_price': card.card_price,
                'card_type': card.card_type,
                'second_face_name': card.second_face_name,
                'second_face_image': card.second_face_image_url,
                'second_face_card_type': card.second_face_card_type
            } for card in deck.card_list]
        }

        # Convert the dictionary to JSON format
        deck_json = json.dumps(deck_data)

        # Save the JSON data to a text file with the same name as the deck
        deck_file = filedialog.asksaveasfilename(initialdir="C:\\Users\\andregsa\\Saved Games\\MTGDB",
                                                 title="Save Deck",
                                                 defaultextension='.json',
                                                 filetype=[("MTG Deck Builder Deck", "*.json")])

        with open(deck_file, 'w') as f:
            f.write(deck_json)

    def load_deck(self):
        file_path = filedialog.askopenfilename(initialdir="C:\\Users\\andregsa\\Saved Games\\MTGDB",
                                               title="Choose Deck",
                                               filetype=[("MTG Deck Builder Deck", "*.json")])

        # Load the deck data from the file
        with open(file_path, "r") as f:
            data = json.load(f)

        deck_name = Path(file_path).stem
        decklist = []

        for card_data in data["decklist"]:
            image = requestsAPI.Requests().get_card_image_by_url(card_data['image'])

            if card_data['second_face_image'] != None:
                second_image = requestsAPI.Requests().get_card_image_by_url(card_data['second_face_image'])
            else:
                second_image = None
            
            card = models.Card(card_data['quantity'],
                               card_data['id'],
                               card_data['name'],
                               image,
                               card_data['image'],
                               card_data['card_price'],
                               card_data['card_type'],
                               card_data['second_face_name'],
                               second_image,
                               card_data['second_face_image'],
                               card_data['second_face_card_type'])
            decklist.append(card)

        # Create the Deck object
        deck = models.Deck(data['id'], deck_name, decklist)

        return deck
