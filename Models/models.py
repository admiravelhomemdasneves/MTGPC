class Deck:
    def __init__(self, deck_id, deck_name, deck_list):
        self.deck_id = deck_id
        self.deck_name = deck_name
        self.card_list = deck_list

    def delete_card(self, v_card):
        for card in self.card_list:
            if card == v_card:
                if card.quantity > 1:
                    card.decrease_quantity()
                elif card.quantity <= 1:
                    self.card_list.remove(card)

    def add_card(self, v_card):
        new_card = v_card

        for card in self.card_list:
            if new_card.name == card.name:
                card.add_quantity()
                return

        self.card_list.append(new_card)

    def get_total_cost(self):
        total_cost = 0

        for card in self.card_list:
            try:
                total_cost += float(card.card_price) * float(card.quantity)
            except:
                pass

        return total_cost

    def get_nr_cards(self):
        nr_cards = 0

        for card in self.card_list:
            nr_cards += int(card.quantity)

        return nr_cards


class Card:
    def __init__(self, quantity, id, name, image, image_url, card_price, card_type, second_face_name, second_face_image,
                 second_face_image_url, second_face_card_type):
        self.quantity = quantity
        self.id = id
        self.name = name
        self.image = image
        self.image_url = image_url
        self.card_price = card_price
        self.card_type = card_type
        self.second_face_name = second_face_name
        self.second_face_image = second_face_image
        self.second_face_image_url = second_face_image_url
        self.second_face_card_type = second_face_card_type

    def add_quantity(self):
        self.quantity += 1

    def decrease_quantity(self):
        self.quantity -= 1
