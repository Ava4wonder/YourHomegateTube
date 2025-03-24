# HomegateTube
Generate a read-friendly properties search report within a single html or pdf with rich information, for each property item it includes info:
- Square, room number, (net) rent cost/month of this property
- Distance between this property to your source location
- Transit/Bicycle/Walk time cost
- Explicit Transit route and time cost
- Accessibilities (supermarket, pharmacy, school, park, hospital, transit_station) 
- Street view images around this property

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
