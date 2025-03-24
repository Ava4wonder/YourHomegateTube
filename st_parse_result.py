import googlemaps
from geopy.distance import geodesic

import time
from openai import OpenAI
MY_API_KEY = "sk-LAbGx20bvcYb8SYYgOtIn2nprsuKlHhU76XULqOtMhfRk7P0"

def kimi_request(geo_ctx):
    time.sleep(3)
    client = OpenAI(
    # api_key="sk-LAbGx20bvcYb8SYYgOtIn2nprsuKlHhU76XULqOtMhfRk7P0",  # 替换为你的API Key
    api_key=MY_API_KEY,  # 替换为你的API Key
    base_url="https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",  # 你可以选择不同的模型，如moonshot-v1-32k或moonshot-v1-128k
        messages=[
            {"role": "system", "content": "请根据如下信息, 结合这些设施在互联网中的公开信息和我关心的问题: （1）该位置与目标位置EPFL（纬度：46.5172269，经度：6.578294，）之间的距离； （2）使用不同的交通方式（包括公共交通、自行车或步行）在两个位置之间移动需要多长时间； （3）该位置的生活设施的便利性以及这些生活设施口碑如何。为我生成一份简洁但内容丰富的房屋评估报告" },
            # {"role": "user", "content": "please generate a conversation about changing appointment"}
            # {"role": "user", "content": "Could you please generate three exercises of DELF A1 level Listening Comprehension about time. Please generate both the audio script and corresponding exercises"}
            {"role": "user", "content": geo_ctx}
        ],
        temperature=0.5,
        # stream=True,
    )

    response = completion.choices[0].message.content
    return response

def generate_geo_context(input_lat, input_lon):
    geo_ctx = ''
    
    # Google Maps API Key
    API_KEY = 'AIzaSyA6pxzzF_bf5kupi6r2ufft5Mn7KP1VNRI'
    gmaps = googlemaps.Client(key=API_KEY)

    # Start and target coordinates
    # start_coords = (46.5172269, 6.578294)  # EPFL
    start_coords = (46.517247, 6.56885)
    target_coords = (input_lat, input_lon)  # Input target location

    try:
        # 1. Calculate Distance
        distance = geodesic(start_coords, target_coords).kilometers
        geo_ctx += f"Distance: {distance:.2f} km\n"

        # 2. Travel Time for different modes
        transport_modes = ["transit", "bicycling", "walking"]
        geo_ctx += "Travel Times:\n"
        for mode in transport_modes:
            try:
                directions = gmaps.directions(
                    origin=start_coords,
                    destination=target_coords,
                    mode=mode
                )
                travel_time = directions[0]['legs'][0]['duration']['text']
                geo_ctx += f"  {mode.capitalize()}: {travel_time}\n"
                if directions and mode == 'transit':
                    for leg in directions[0]['legs']:
                        for step in leg['steps']:
                            if 'transit_details' in step:
                                transit_details = step['transit_details']
                                geo_ctx += f"乘坐 {transit_details['line']['short_name']} {transit_details['line']['vehicle']['type']} 从 {transit_details['departure_stop']['name']} 到 {transit_details['arrival_stop']['name']}\n"
                                # print(f"出发时间: {transit_details['departure_time']['text']}, 到达时间: {transit_details['arrival_time']['text']}")
                                # print(f"行驶时间: {transit_details['duration']['text']}")
                            else:
                                print(step['html_instructions'])
            except Exception as e:
                geo_ctx += f"  {mode.capitalize()}: Error retrieving travel time ({str(e)})\n"

        # 3. Living Facilities Convenience
        search_keywords = ["supermarket", "pharmacy", "school", "park", "hospital", "transit_station"]
        geo_ctx += "Living Facilities Number:\n"
        for keyword in search_keywords:
            try:
                places = gmaps.places_nearby(
                    location=target_coords,
                    radius=1000,  # 1 km radius
                    keyword=keyword
                )
                count = len(places['results'])
                geo_ctx += f"  {keyword.capitalize()}: {count} nearby\n"
                
                # Add detailed info
                geo_ctx += f"  {keyword.capitalize()} Details:\n"
                for place in places['results']:
                    name = place.get('name', 'N/A')
                    rating = place.get('rating', 'N/A')
                    vicinity = place.get('vicinity', 'N/A')
                    geo_ctx += f"    - {name} (Rating: {rating}, Vicinity: {vicinity})\n"
            except Exception as e:
                geo_ctx += f"  {keyword.capitalize()}: Error retrieving facilities ({str(e)})\n"

    except Exception as e:
        geo_ctx += f"Error calculating geo context: {str(e)}\n"

    return geo_ctx





import streamlit as st
import json
import requests
import re


lower_value = st.number_input("Enter the lower rent price", value=800)
upper_value = st.number_input("Enter the upper rent price", value=2000)
livingSpace_thres = st.number_input("Enter the living space threshold", value=45)



try:
    with open('search_results.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("The JSON file was not found.")
    data = []


import os
import ast  # For safely converting stringified tuples back to tuples

coordinates_file_path = 'coordinates.json'

# Try to open the file and read the dictionary
if os.path.exists(coordinates_file_path):
    with open(coordinates_file_path, 'r', encoding='utf-8') as file:
        try:
            # Load the JSON file
            loaded_data = json.load(file)
            
            # Convert stringified tuple keys back to tuple keys
            coordinates_dict = {ast.literal_eval(key): value for key, value in loaded_data.items()}
        except json.JSONDecodeError:
            # If the file content is not valid JSON, initialize an empty dictionary
            coordinates_dict = {}
else:
    # If the file doesn't exist, create an empty file and initialize an empty dictionary
    with open(coordinates_file_path, 'w', encoding='utf-8') as file:
        coordinates_dict = {}
        json.dump({}, file, ensure_ascii=False, indent=4)


# 现在你可以使用coordinates_dict这个字典了
print(coordinates_dict)

# Generate Street View images
headings = [0, 45, 90, 135, 180, 225, 270]  # North, East, South, West
pitch = 0  # Default pitch
size="640x480"
API_KEY = 'AIzaSyA6pxzzF_bf5kupi6r2ufft5Mn7KP1VNRI'

from PIL import Image
from io import BytesIO

def save_street_view_images(cur_lat, cur_lon, street_view_images):
    # Define folder name based on coordinates
    folder_name = f"{cur_lat}_{cur_lon}_streetview_images"
    os.makedirs(folder_name, exist_ok=True)
    
    # Save images to the folder
    for i, (image_content, caption) in enumerate(street_view_images):
        image_path = os.path.join(folder_name, f"{caption.replace(' ', '_')}.jpg")
        with open(image_path, 'wb') as f:
            f.write(image_content)
    print(f"Images saved in folder: {folder_name}")

def load_street_view_images_from_folder(folder_name):
    images = []
    for file_name in os.listdir(folder_name):
        if file_name.endswith(".jpg"):
            with open(os.path.join(folder_name, file_name), 'rb') as f:
                images.append((f.read(), file_name.replace('_', ' ').replace('.jpg', '')))
    return images

for result in data.get('results', []):
    listing = result.get('listing', {})
    address = listing.get('address', {})
    characteristics = listing.get('characteristics', {})
    prices = listing.get('prices', {})
    localization = listing.get('localization', {}).get('de', {})
    rent_price = prices.get('rent', {}).get('gross')
    characteristics = listing.get('characteristics', {})
    living_space = characteristics.get('livingSpace')
    cur_geo_dict = address.get('geoCoordinates', 'Unknown')
    cur_lat = cur_geo_dict.get('latitude', 'Unknown')
    cur_lon = cur_geo_dict.get('longitude', 'Unknown')


    if (
        rent_price is not None
        and lower_value <= rent_price <= upper_value
        and living_space is not None
        and living_space > livingSpace_thres
    ): 
        print('here', cur_lat, cur_lon, str(cur_lat) + ',' + str(cur_lon))
        folder_name = f"{cur_lat}_{cur_lon}_streetview_images"
        if os.path.exists(folder_name):
            # Load images from the folder
            street_view_images = load_street_view_images_from_folder(folder_name)
        else:
            street_view_images = []
            for heading in headings:
                url = f"https://maps.googleapis.com/maps/api/streetview"
                parameters = {
                    "location": str(cur_lat) + ',' + str(cur_lon),
                    "size": size,
                    "fov": 180, 
                    "heading": heading,
                    "pitch": 0,
                    "key": API_KEY
                }
                # 发送请求
                response = requests.get(url, params=parameters)
                # print(response.status_code)
                # print(response.text)
                # url = f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={cur_lat},{cur_lon}&heading={heading}&pitch={pitch}&key={MY_API_KEY}"
                # response = requests.get(url)
                # if response.status_code == 200:
                # image = Image.open(BytesIO(response.content))
                street_view_images.append((response.content, f"Heading {heading}°"))
                # else:
                #     st.error(f"Failed to fetch image for heading {heading}°: {response.status_code}")
            
            # Save images to the folder
            save_street_view_images(cur_lat, cur_lon, street_view_images)

        if tuple([cur_lat, cur_lon]) in coordinates_dict:
            print('geo_ctx hit')
            geoinfo_text = coordinates_dict[tuple([cur_lat, cur_lon])]
        else:
            geo_ctx = generate_geo_context(cur_lat, cur_lon)
            # Here, you can run any Python code you want to generate the response
            geoinfo_text = kimi_request(geo_ctx)
            # print(geoinfo_text)
            coordinates_dict[tuple([cur_lat, cur_lon])] = geoinfo_text
            
        
        st.markdown(f"**{localization.get('text', {}).get('title', 'No title')}**")
        st.markdown(f"Location: {address.get('locality', 'Unknown')}, {address.get('postalCode', 'Unknown')}")
        st.markdown(f"Living Space: {characteristics.get('livingSpace', 'Unknown')} sqm, Rooms: {characteristics.get('numberOfRooms', 'Unknown')}")
        st.markdown(f"Rent: {prices.get('rent', {}).get('gross', 'Unknown')} CHF (net) per month")
        
        plain_text = re.sub(r'^#+\s*', '', geoinfo_text, flags=re.MULTILINE)
        st.write(plain_text)  # Display the value from coordinates_dict
        attachments = listing.get('localization', {}).get('de', {}).get('attachments', [])
        for attachment in attachments:
            if attachment.get('type') == 'IMAGE':
                image_url = attachment.get('url')
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        st.image(response.content, caption=attachment.get('file'))
                except requests.RequestException as e:
                    st.error(f"Error fetching image: {e}")

        # Display Street View images
        st.markdown("### Street View Images")
        for image_content, caption in street_view_images:
            st.image(image_content, caption=caption)
        
        
        # # Street View settings
        # embed_heading = 90  # Camera angle (0 = North)
        # embed_pitch = 0     # Vertical angle (-90 to 90)
        # embed_fov = 90   # Field of view (default: 90)
        # street_view_url = f"https://www.google.com/maps/embed/v1/streetview?location={cur_lat},{cur_lat}&heading={embed_heading}&pitch={embed_pitch}&fov={embed_fov}&key={API_KEY}"
        # # Embed the Street View in Streamlit
        # st.markdown("### Interactive Google Maps Street View")
        # st.components.v1.iframe(street_view_url, width=800, height=600)

        st.write("---")


# Convert tuple keys to strings for JSON serialization
# Save to JSON file
with open(coordinates_file_path, 'w', encoding='utf-8') as f:
    json.dump({str(key): value for key, value in coordinates_dict.items()}, f, ensure_ascii=False, indent=4)

    # json.dump(coordinates_dict, f, ensure_ascii=False, indent=4)
