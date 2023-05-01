from urllib.request import urlopen
from PIL import Image
from Models import models
import requests


class Requests:
    def __init__(self):
        self.scryfall_url = "https://api.scryfall.com"

    def get_card_autocomplete(self, query):
        """
        Fetches card autocomplete suggestions from Scryfall API based on the given query.
        """
        self.endpoint = f'/cards/autocomplete?q={query}'
        self.url = self.scryfall_url + self.endpoint

        try:
            self.response = requests.get(self.url)
            self.response.raise_for_status()
            return self.response.json()
        except requests.exceptions.HTTPError as e:
            print(f'Error fetching card suggestions: {e}')
            return None

    def get_card_image_url(self, card_name, face):
        # Replace the spaces in the card name with '+' to use in the API URL
        card_name = card_name.replace(' ', '+')

        self.endpoint = f'/cards/named?fuzzy={card_name}'
        self.url = self.scryfall_url + self.endpoint
        
        # Make a GET request to the Scryfall API
        self.response = requests.get(self.url)

        # Check if the request was successful
        if self.response.status_code == 200:
            if "card_faces" in self.response.json():
                self.image_url = self.response.json()["card_faces"][int(face)]["image_uris"]["normal"]
            else:
                self.image_url = self.response.json()['image_uris']['normal']
                return self.image_url
        else:
            # If the request failed, print an error message
            print(f"Error {self.response.status_code}: {self.response.reason}")

    def get_card_image(self, card_name, face):
        self.image_url = self.get_card_image_url(card_name, face)
        self.image = Image.open(urlopen(self.image_url))
        return self.image

    def get_card_image_by_url(self, image_url):
        image = Image.open(urlopen(image_url))
        return image

    def get_card_id(self, card_name):
        # Set up the API endpoint URL with the card name as a query parameter
        self.card_name = card_name
        self.card_name = self.card_name.replace(' ', '+')

        self.endpoint = f'/cards/named?exact={self.card_name}'
        self.url = self.scryfall_url + self.endpoint

        # Send the API request
        response = requests.get(self.url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            card_data = response.json()

            # Extract the card ID from the response data
            card_id = card_data.get('id')

            # Return the card ID
            return card_id
        else:
            # If the request was not successful, raise an exception
            raise Exception(
                f'Request failed with status code {response.status_code}')

    def get_card_by_name(self, v_card_name):
        # Set up the API endpoint URL with the card name as a query parameter
        self.card_name = v_card_name
        self.card_name = self.card_name.replace(' ', '+')

        self.endpoint = f'/cards/named?exact={self.card_name}'
        self.url = self.scryfall_url + self.endpoint

        # Send the API request
        response = requests.get(self.url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            card_data = response.json()

            card_quantity = 1
            card_id = card_data.get('id')
            card_price = str(card_data["prices"]["eur"])

            if "card_faces" in card_data:
                try:
                    #Code that may raise an error
                    self.get_card_image_by_url(card_data["card_faces"][0]["image_uris"]["normal"])
                except:
                    #code to run if error is raised
                    card_name = card_data['name']
                    card_image = self.get_card_image_by_url(card_data['image_uris']['normal'])
                    card_image_url = card_data['image_uris']['normal']
                    card_type = card_data['type_line']
                    second_name = None
                    second_image = None
                    second_image_url = None
                    second_type = None
                else:
                    #code to run if no error is raised
                    card_name = card_data["card_faces"][0]['name']
                    card_image = self.get_card_image_by_url(card_data["card_faces"][0]["image_uris"]["normal"])
                    card_image_url = card_data["card_faces"][0]["image_uris"]["normal"]
                    card_type = card_data["card_faces"][0]['type_line']
                    second_name = card_data["card_faces"][1]['name']
                    second_image = self.get_card_image_by_url(card_data["card_faces"][1]["image_uris"]["normal"])
                    second_image_url = card_data["card_faces"][1]["image_uris"]["normal"]
                    second_type = card_data["card_faces"][1]['type_line']
            else:
                card_name = card_data['name']
                card_image = self.get_card_image_by_url(card_data['image_uris']['normal'])
                card_image_url = card_data['image_uris']['normal']
                card_type = card_data['type_line']
                second_name = None
                second_image = None
                second_image_url = None
                second_type = None
            
            card = models.Card(
                id=card_id,
                quantity=card_quantity,
                name=card_name,
                image=card_image,
                image_url=card_image_url,
                card_price=card_price,
                card_type=card_type,
                second_face_name=second_name,
                second_face_image=second_image,
                second_face_image_url=second_image_url,
                second_face_card_type=second_type)

            # Return the card
            return card
        else:
            # If the request was not successful, raise an exception
            raise Exception(
                f'Request failed with status code {response.status_code}')
        
    def get_card_name_by_id(self, card_id):
        # Set up the API endpoint URL with the card ID as a path parameter
        self.endpoint = f'/cards/{card_id}'
        self.url = self.scryfall_url + self.endpoint

        # Send the API request
        response = requests.get(self.url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            card_data = response.json()

            # Extract the card name from the response data
            card_name = card_data.get('name')

            # Return the card name
            return card_name
        else:
            # If the request was not successful, raise an exception
            raise Exception(
                f'Request failed with status code {response.status_code}')
