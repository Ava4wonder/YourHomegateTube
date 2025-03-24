#!/bin/bash
# Set API keys as os.env variables

export GOOGLE_MAP_API_KEY="AIzaSyAyy3SOQT2n8vDocXHDI4A8tvATYr6Xo3Q" 


# Run the Rust cargo project
cargo run &
rust_pid=$!

# Wait for a short time to ensure the Rust program has started (adjust as needed)
sleep 3

# run summary_agent python script & save summary to a text file
# python summary_agent.py

# Run the Streamlit Python script
streamlit run st_parse_result.py

# Kill the Rust process when the Streamlit script exits
kill $rust_pid