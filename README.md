# YourHomegateTube
Help you generate a read-friendly properties search report within a single html or pdf with rich information, for each property item it includes info:
- Square, room number, (net) rent cost/month of this property
- Distance between this property to your source location
- Transit/Bicycle/Walk time cost
- Explicit Transit route and time cost
- Accessibilities (supermarket, pharmacy, school, park, hospital, transit_station) 
- Street view images around this property

## Demo result
An example and display the top 9 pages from a 336 pages complete search report (the current version shows the info in Chinease):
<img width="591" alt="Screenshot 2025-03-25 at 3 38 30 PM" src="https://github.com/user-attachments/assets/1b480039-b11e-46dc-98b4-156a43ebfb82" />
<img width="1038" alt="Screenshot 2025-03-25 at 3 39 11 PM" src="https://github.com/user-attachments/assets/c1bf5115-9249-4ad3-9e53-e02ea7393eac" />
<img width="1044" alt="Screenshot 2025-03-25 at 3 39 27 PM" src="https://github.com/user-attachments/assets/7b54f656-167c-446f-9795-38afc922a0ba" />
<img width="1047" alt="Screenshot 2025-03-25 at 3 39 37 PM" src="https://github.com/user-attachments/assets/e8f702d8-041d-445b-9b9c-78f635ca4cf9" />
<img width="1050" alt="Screenshot 2025-03-25 at 3 39 50 PM" src="https://github.com/user-attachments/assets/0a5ae791-a2ce-4176-8587-93c93bfb57d9" />


## Setup environment
pip install requirements.txt

## Setup API keys
- Google Map API key 
- Kimi API key

## Usage 
In order to generate a html which display the houses that meet your requirements:
- Source location: `lat`, `lon`
- Maximum distance: `max_distance`
- Street view: `on`
- Summary report: `on`

Just run code:
```bash
bash run_sh.sh
```

## Disclaimer

This folder contains modified code from the `homegate-rs` project (https://github.com/denysvitali/homegate-rs) for educational purposes or private use only.

Original work is licensed under the MIT License. See the LICENSE file for details.

The library is not intended for scraping or publicly reusing data from homegate.ch without proper authorization.


## Brief Into for `homegate-rs` Project: AN UNOFFICIAL Homegate Library for Rust
<p align="center">
  <img 
    src="./docs/logo.png" 
    alt="homegate.ch logo"
    height="60"
  />
</p>

`homegate-rs` is a small library that lets you interact with the
[Homegate](https://homegate.ch) backend.   


<small>from <i><a href="https://www.homegate.ch/c/en/about-us/legal-issues/disclaimer">homegate.ch's Disclaimer page</a></i></small>
