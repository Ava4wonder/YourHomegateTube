// use homegate::api::search::{self, Location}; // Import search module
use homegate::api::BACKEND_URL;

use homegate::api::search::{self, Location, SearchRequest, default_search};
use homegate::models::paginated::Paginated;
use homegate::models::realestate::RealEstate;

use serde_json::to_writer_pretty;
// use std::fs::File;
use std::io::Result;

use serde_json::{to_writer, Value};
use std::fs::{File, OpenOptions};
use std::io::{self, Write};

#[tokio::main]
// async fn main() {
async fn main() -> io::Result<()> {

    // Customize the search request
    let mut from = 0;
    let size = 100; // Set to the API's maximum allowed size
    let file_path = "search_results.json";

    // Create or clear the file initially
    File::create(file_path)?;

    let mut search_request = default_search(from, size);
    search_request.from = from;
    search_request.size = size;
    // Adjust search parameters
    search_request.query.location = Location {
        latitude: 46.517247, 
        longitude: 6.56885,
        radius: 30000,
    };
    search_request.query.monthly_rent = search::FromTo { from: Some(800), to: Some(1800) };
    search_request.query.number_of_rooms = search::FromTo { from: Some(2), to: Some(5) };

    
    search_request.from = from;

    // Send the search request
    // match search::search(&search_request.query.location).await {
    match search::search(&search_request).await {
        Ok(results) => {
            // Save results to a JSON file
            // append_to_json(file_path, &results)?;

            if let Ok(mut file) = File::create("search_results.json") {
                if let Err(e) = to_writer_pretty(&mut file, &results) {
                    eprintln!("Error writing JSON: {:?}", e);
                }
            } else {
                eprintln!("Error creating file");
            }

            // Display results in a user-friendly format
            // display_results(results);

            
        }
        Err(e) => {
            eprintln!("Error during search: {:?}", e);
        }
    }


    Ok(())

}


    // // Define the search location
    // let location = Location {
    //     latitude: 46.517247,
    //     longitude: 6.56885,
    //     radius: 30000,
    // };

    // // Perform the search
    // match search::search(&location).await {
    //     Ok(results) => {
    //         if let Ok(mut file) = File::create("search_results.json") {
    //             if let Err(e) = to_writer_pretty(&mut file, &results) {
    //                 eprintln!("Error writing JSON: {:?}", e);
    //             }
    //         } else {
    //             eprintln!("Error creating file");
    //         }
    //     }
    //     // Ok(results) => {
    //     //     println!("Search results: {:?}", results);
    //     // }
    //     Err(e) => {
    //         eprintln!("Error during search: {:?}", e);
    //     }
    // }


// }
