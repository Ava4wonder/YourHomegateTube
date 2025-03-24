import googlemaps
from geopy.distance import geodesic

# Google Maps API Key
API_KEY = 'AIzaSyA6pxzzF_bf5kupi6r2ufft5Mn7KP1VNRI'
gmaps = googlemaps.Client(key=API_KEY)

# Locations
input_lat = 46.5249386
input_lon = 6.6319718
# # start_coords = (46.5249386, 6.6319718)  # Avenue de Riant-Mont 10
# start_coords = (46.5172269, 6.578294) # EPFL
# # target_coords = (46.5172269, 6.578294)  # Target location
# target_coords = (input_lat, input_lon)  # Target location

# # 1. Calculate Distance
# distance = geodesic(start_coords, target_coords).kilometers
# print(f"Distance: {distance:.2f} km")

# # 2. Travel Time
# transport_modes = ["transit", "bicycling", "walking"]
# travel_times = {}

# for mode in transport_modes:
#     directions = gmaps.directions(
#         origin=start_coords,
#         destination=target_coords,
#         mode=mode
#     )
#     travel_time = directions[0]['legs'][0]['duration']['text']
#     travel_times[mode] = travel_time

# print("Travel Times:")
# for mode, time in travel_times.items():
#     print(f"  {mode.capitalize()}: {time}")

# # 3. Living Facilities Convenience
# search_keywords = ["supermarket", "pharmacy", "school", "park", "hospital", "transit_station"]
# facilities = {}
# facilities_info = {}

# for keyword in search_keywords:
#     facilities_info[keyword] = []
#     places = gmaps.places_nearby(
#         location=start_coords,
#         radius=1000,  # Search within 1 km radius
#         keyword=keyword
#     )
#     # print(places['results'])
#     # facilities += places['results']
#     facilities[keyword] = len(places['results'])
#     facilities_info[keyword] += places['results']

# print("Living Facilities Number:")
# # for facility, count in facilities.items():
# #     print(f"  {facility.capitalize()}: {count} nearby")

# places_info = {}
# for keyword in search_keywords:
#     places_info[keyword] = []
#     for place in facilities_info[keyword]:
#         name = place.get('name')
#         types = place.get('types')
#         rating = place.get('rating')
#         user_ratings_total = place.get('user_ratings_total')
#         vicinity = place.get('vicinity')

#         places_info[keyword].append(
#             {'name': name, 
#              'types': types,
#              'rating': rating,
#              'user_ratings_total': user_ratings_total,
#              'vicinity': vicinity
#              })

# print(facilities)
# print('---')
# print("Living Facilities Detailed Info:")
# print(places_info)

    


geo_ctx = ''
    
# Google Maps API Key
API_KEY = 'AIzaSyA6pxzzF_bf5kupi6r2ufft5Mn7KP1VNRI'
gmaps = googlemaps.Client(key=API_KEY)

# # Start and target coordinates
# start_coords = (46.5172269, 6.578294)  # EPFL
# target_coords = (input_lat, input_lon)  # Input target location

# try:
#     # 1. Calculate Distance
#     distance = geodesic(start_coords, target_coords).kilometers
#     geo_ctx += f"Distance: {distance:.2f} km\n"

#     # 2. Travel Time for different modes
#     transport_modes = ["transit", "bicycling", "walking"]
#     geo_ctx += "Travel Times:\n"
#     for mode in transport_modes:
#         try:
#             directions = gmaps.directions(
#                 origin=start_coords,
#                 destination=target_coords,
#                 mode=mode
#             )
#             travel_time = directions[0]['legs'][0]['duration']['text']
#             geo_ctx += f"  {mode.capitalize()}: {travel_time}\n"
#             # 解析路线信息
#             if directions and mode == 'transit':
#                 for leg in directions[0]['legs']:
#                     for step in leg['steps']:
#                         if 'transit_details' in step:
#                             transit_details = step['transit_details']
#                             print(f"乘坐 {transit_details['line']['short_name']} {transit_details['line']['vehicle']['type']} 从 {transit_details['departure_stop']['name']} 到 {transit_details['arrival_stop']['name']}")
#                             # print(f"出发时间: {transit_details['departure_time']['text']}, 到达时间: {transit_details['arrival_time']['text']}")
#                             # print(f"行驶时间: {transit_details['duration']['text']}")
#                         else:
#                             print(step['html_instructions'])
#         except Exception as e:
#             geo_ctx += f"  {mode.capitalize()}: Error retrieving travel time ({str(e)})\n"

#     # 3. Living Facilities Convenience
#     search_keywords = ["supermarket", "pharmacy", "school", "park", "hospital", "transit_station"]
#     geo_ctx += "Living Facilities Number:\n"
#     for keyword in search_keywords:
#         try:
#             places = gmaps.places_nearby(
#                 location=start_coords,
#                 radius=1000,  # 1 km radius
#                 keyword=keyword
#             )
#             count = len(places['results'])
#             geo_ctx += f"  {keyword.capitalize()}: {count} nearby\n"
            
#             # Add detailed info
#             geo_ctx += f"  {keyword.capitalize()} Details:\n"
#             for place in places['results']:
#                 name = place.get('name', 'N/A')
#                 rating = place.get('rating', 'N/A')
#                 vicinity = place.get('vicinity', 'N/A')
#                 geo_ctx += f"    - {name} (Rating: {rating}, Vicinity: {vicinity})\n"
#         except Exception as e:
#             geo_ctx += f"  {keyword.capitalize()}: Error retrieving facilities ({str(e)})\n"

# except Exception as e:
#     geo_ctx += f"Error calculating geo context: {str(e)}\n"

# print(geo_ctx)


# import requests

# # Google Maps API Key
# # Coordinates of the point
# latitude = 46.5172269
# longitude = 6.578294

# # Output folder for images
# output_folder = "streetview_images"

# # Ensure the folder exists
# import os
# os.makedirs(output_folder, exist_ok=True)

# # Generate images for different headings
# headings = [0, 90, 180, 270]  # North, East, South, West
# pitch = 0  # Default pitch

# for heading in headings:
#     # Construct the Street View API URL
#     url = f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={latitude},{longitude}&heading={heading}&pitch={pitch}&key={API_KEY}"
    
#     # Download the image
#     response = requests.get(url)
#     image_path = os.path.join(output_folder, f"streetview_heading_{heading}.jpg")
#     with open(image_path, 'wb') as f:
#         f.write(response.content)

# ----------------------------------------------------------
# import requests
# from PIL import Image
# from io import BytesIO
# location = "46.5249386,6.6319718"
# size="640x480"
# url = f"https://maps.googleapis.com/maps/api/streetview"
# parameters = {
#     "location": location,
#     "size": size,
#     "fov": 180, 
#     "heading": 0,
#     "pitch": 0,
#     "key": API_KEY
# }
    
# # 发送请求
# response = requests.get(url, params=parameters)

# # print(response.status_code)
# # print(response.text)
# image = Image.open(BytesIO(response.content))
# # 保存图片
# image.save("street_view_image.jpg")

# # print("All images generated.")
# ----------------------------------------------------------
import streamlit as st

# Google Maps API Key
# API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

# Set the initial latitude and longitude
latitude = 46.5172269
longitude = 6.578294

# Street View settings
heading = 90  # Camera angle (0 = North)
pitch = 0     # Vertical angle (-90 to 90)
fov = 90      # Field of view (default: 90)

# Generate the Street View URL
street_view_url = f"https://www.google.com/maps/embed/v1/streetview?location={latitude},{longitude}&heading={heading}&pitch={pitch}&fov={fov}&key={API_KEY}"

# Embed the Street View in Streamlit
st.markdown("### Interactive Google Maps Street View")
st.components.v1.iframe(street_view_url, width=800, height=600)




