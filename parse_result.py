from typing import List, Dict
import rich
from rich import print
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.console import Console


import json

try:
    with open('search_results.json', 'r') as f:
        data = json.load(f)
        print(data)
except FileNotFoundError:
    print("The JSON file was not found.")
except json.JSONDecodeError:
    print("There was an error decoding the JSON data.")
# data = {
#     "Search results": {
#         "Paginated": {
#             "from": 0,
#             "max_from": 20,
#             "results": [
#                 {
#                     "id": "4001758933",
#                     "listing": {
#                         "address": {
#                             "country": "CH",
#                             "geo_coordinates": {
#                                 "latitude": 47.374151781735,
#                                 "longitude": 8.539632302293
#                             },
#                             "locality": "Zürich",
#                             "postal_code": "8001",
#                             "region": "ZH",
#                             "street": "obere Zäune"
#                         },
#                         "categories": ["Apartment", "AtticFlat"],
#                         "characteristics": {
#                             "living_space": 75,
#                             "number_of_rooms": 2.5
#                         },
#                         "id": "4001758933",
#                         "lister": {
#                             "phone": None
#                         },
#                         "localization": {
#                             "de": {
#                                 "attachments": [
#                                     {
#                                         "t": "IMAGE",
#                                         "url": "https://media2.homegate.ch/listings/v2/hgonif/4001758933/image/f4814dc0d2c2bf4b859de9d3b15f29b2.jpg",
#                                         "file": "69600e14af.jpeg"
#                                     },
#                                 ],
#                                 "text": {
#                                     "title": "Rarität in der Altstadt: Charmante loftartige Dachwohnung mit sehr grosser privater Terrasse"
#                                 }
#                             }
#                         },
#                         "offer_type": "RENT",
#                         "prices": {
#                             "rent": {
#                                 "interval": "MONTH",
#                                 "net": 3900,
#                                 "gross": 4150,
#                                 "extra": 250
#                             },
#                             "currency": "CHF",
#                             "buy": {
#                                 "interval": None,
#                                 "net": None,
#                                 "gross": None,
#                                 "extra": None
#                             }
#                         }
#                     }
#                 },
#             ],
#             "size": 20,
#             "total": 36
#         }
#     }
# }


def parse_real_estate(estate: Dict) -> Dict:
    address_info = estate["listing"]["address"]
    full_address = f"{address_info.get('street', '')}, {address_info.get('postal_code', '')} {address_info.get('locality', '')}, {address_info.get('country', '')}"

    categories = ", ".join(estate["listing"]["categories"])
    living_space = estate["listing"]["characteristics"].get("living_space")
    if living_space is not None:
        living_space = str(living_space)
    rooms = estate["listing"]["characteristics"].get("number_of_rooms")
    if rooms is not None:
        rooms = str(rooms)
    offer_type = estate["listing"]["offer_type"]
    rent_info = estate["listing"]["prices"].get("rent")
    rent = f"{rent_info.get('net')} (net) {rent_info.get('gross')} (gross) {rent_info.get('extra')} extra" if rent_info else "N/A"
    currency = estate["listing"]["prices"].get("currency")

    images = [att["url"] for att in estate["listing"]["localization"].get("de", {}).get("attachments", []) if att["t"] == "IMAGE"]

    return {
        "id": estate["id"],
        "address": full_address,
        "categories": categories,
        "living_space": living_space,
        "rooms": rooms,
        "offer_type": offer_type,
        "rent": rent,
        "currency": currency,
        "images": images
    }


parsed_data = []
for estate in data["Search results"]["Paginated"]["results"]:
    parsed_estate = parse_real_estate(estate)
    parsed_data.append(parsed_estate)

console = Console()
cards = []
for index, details in enumerate(parsed_data):
    table = Table(show_header=False, box=None)
    table.add_row("ID:", details["id"])
    table.add_row("Address:", details["address"])
    table.add_row("Categories:", details["categories"])
    table.add_row("Living Space:", details["living_space"])
    table.add_row("Rooms:", details["rooms"])
    table.add_row("Offer Type:", details["offer_type"])
    table.add_row("Rent:", details["rent"])
    table.add_row("Currency:", details["currency"])

    image_previews = []
    for img in details["images"][:3]:
        image_previews.append(f"[image]{img}[/image]")
    images_panel = Panel("\n".join(image_previews), title="Images", expand=False)

    card = Panel.fit(Columns([table, images_panel]), title=f"Real Estate {details['id']}", border_style="green")
    cards.append(card)

console.print(*cards, sep="\n\n")

for item in parsed_data:
    print(item)