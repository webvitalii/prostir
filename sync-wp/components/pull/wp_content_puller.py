import requests
import json
from pathlib import Path
from config import SITE_URL, OUTPUT_DIR


class WPContentPuller:
    def __init__(self, site_url=None, output_dir=None):
        # Use centralized config with fallback options
        self.site_url = site_url or SITE_URL
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = OUTPUT_DIR

    def pull_items(self, content_type, username=None, application_password=None):
        # content_type should already be plural (posts/pages)
        endpoint = f"{self.site_url}/wp-json/wp/v2/{content_type}"
        print(f"Accessing API endpoint: {endpoint}")
        params = {"per_page": 100}
        page = 1
        items = []
        
        # Set up authentication if provided
        auth = None
        if username and application_password:
            auth = (username, application_password)
            print(f"Using application authentication with username: {username}")
        
        try:
            # Get first page
            params["page"] = page
            resp = requests.get(endpoint, params=params, auth=auth)
            print(f"Response status code: {resp.status_code}")
            
            if resp.status_code != 200:
                # If the first page fails, that's a real error
                raise Exception(f"Error fetching {content_type}: {resp.status_code}")
                
            data = resp.json()
            if data:
                items.extend(data)
                
                # Check for more pages
                total_pages = int(resp.headers.get('X-WP-TotalPages', '1'))
                print(f"Total pages: {total_pages}")
                
                # If there are more pages, fetch them
                for page in range(2, total_pages + 1):
                    params["page"] = page
                    resp = requests.get(endpoint, params=params, auth=auth)
                    print(f"Fetching page {page}/{total_pages}, status: {resp.status_code}")
                    
                    if resp.status_code == 200:
                        data = resp.json()
                        items.extend(data)
                    else:
                        print(f"Error fetching page {page}: {resp.status_code}, skipping")
                        
        except Exception as e:
            print(f"Error during pagination: {e}")
            raise
        folder = self.output_dir / content_type
        folder.mkdir(parents=True, exist_ok=True)
        for item in items:
            slug = item.get("slug") or str(item.get("id"))
            file_path = folder / f"{slug}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(item, f, ensure_ascii=False, indent=2)
        return len(items), folder
