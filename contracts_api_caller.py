import requests
import json

def get_all_releases():
    base_url = "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search?publishedFrom=2024-01-01T00:00:00&publishedTo=2024-11-05T23:00:00"
    headers = {"Accept": "application/json"}
    all_releases = []
    next_url = base_url
    page = 1

    while next_url:
        try:
            print(f"Fetching page {page}...")
            response = requests.get(next_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                releases = data.get("releases", [])
                all_releases.extend(releases)
                
                # Get next page URL if it exists
                next_url = data.get("links", {}).get("next")
                page += 1
            else:
                print(f"Failed to get data: Status code {response.status_code}")
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            break
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            break
            
    return all_releases

try:
    # Get all releases
    print("Starting data collection...")
    all_releases = get_all_releases()
    print(f"Total releases collected: {len(all_releases)}")
    
    # Filter for active tenders where classification.id starts with either 45 or 71
    filtered_data = {
        "releases": [
            release for release in all_releases
            if (release.get("tender", {}).get("classification", {}).get("id", "").startswith(("45", "71")) and
                release.get("tender", {}).get("status") == "active")
        ]
    }
    
    # Save filtered data to JSON file
    with open('filtered_contracts.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=4, ensure_ascii=False)
        
    print("\nFiltered data successfully saved to filtered_contracts.json")
    print(f"Total releases before filtering: {len(all_releases)}")
    print(f"Total releases after filtering: {len(filtered_data['releases'])}")
    
    # Print first few matching IDs for verification
    if filtered_data['releases']:
        print("\nFirst few matching active tenders:")
        for release in filtered_data['releases'][:5]:
            class_id = release.get("tender", {}).get("classification", {}).get("id")
            title = release.get("tender", {}).get("title", "No title")
            status = release.get("tender", {}).get("status")
            print(f"ID: {class_id} - Status: {status} - Title: {title}")
    
except Exception as e:
    print(f"An error occurred: {e}")