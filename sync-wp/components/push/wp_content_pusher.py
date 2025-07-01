import requests
import json
import base64
from pathlib import Path
from config import SITE_URL, OUTPUT_DIR

class WPContentPusher:
    def __init__(self, site_url=None, output_dir=None):
        # Use centralized config with fallback options
        self.site_url = site_url or SITE_URL
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = OUTPUT_DIR
            
    def push_items(self, content_type, username, password, auth_method="basic"):
        """
        Push content from local JSON files to WordPress site via REST API
        
        Args:
            content_type (str): Type of content to push ("posts" or "pages")
            username (str): WordPress username for authentication
            password (str): WordPress password/app password for authentication
            auth_method (str): Authentication method: "basic" or "application"
            
        Returns:
            tuple: (count of items pushed, folder path where files were read from)
        """
        folder = self.output_dir / content_type
        
        if not folder.exists():
            raise Exception(f"Source folder {folder} does not exist")
            
        endpoint = f"{self.site_url}/wp-json/wp/v2/{content_type}"
        
        # Prepare authentication headers
        auth_string = f"{username}:{password}"
        auth_header = base64.b64encode(auth_string.encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/json"
        }
        
        # For debugging authentication
        print(f"Using authentication method: {auth_method}")
        # Don't print the actual credentials, just indicate we're using them
        print(f"Authorization header set (credentials hidden)")
        
        # Get all JSON files from the directory
        json_files = list(folder.glob("*.json"))
        
        if not json_files:
            raise Exception(f"No JSON files found in {folder}")
            
        pushed_count = 0
        
        for file_path in json_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = json.load(f)
                
                # Extract the ID if it exists in the JSON
                item_id = content.get("id")
                
                if item_id:
                    # Update existing item
                    update_url = f"{endpoint}/{item_id}"
                    
                    # Remove fields that shouldn't be sent in update
                    for field in ["_links", "guid", "date", "date_gmt", 
                                 "modified", "modified_gmt", "type", "status"]:
                        if field in content:
                            del content[field]
                    
                    # WordPress REST API expects different format for updates
                    # Extract the actual content from the "rendered" format
                    prepared_content = {}
                    
                    # Handle title
                    if "title" in content and "rendered" in content["title"]:
                        prepared_content["title"] = content["title"]["rendered"]
                    
                    # Handle content
                    if "content" in content and "rendered" in content["content"]:
                        prepared_content["content"] = content["content"]["rendered"]
                    
                    # Handle excerpt
                    if "excerpt" in content and "rendered" in content["excerpt"]:
                        prepared_content["excerpt"] = content["excerpt"]["rendered"]
                    
                    # Copy other fields
                    for field in content:
                        if field not in ["title", "content", "excerpt"]:
                            prepared_content[field] = content[field]
                    
                    # Print what we're updating for debugging
                    print(f"Updating {content_type} with ID: {item_id}")
                    print(f"Update URL: {update_url}")
                    print(f"Content to be sent: {prepared_content.keys()}")
                    
                    response = requests.post(
                        update_url,
                        json=prepared_content,
                        headers=headers
                    )
                    
                    if response.status_code not in [200, 201]:
                        raise Exception(f"Error updating {file_path.name}: {response.status_code} - {response.text}")
                else:
                    # Create new item
                    # For new content, prepare it similarly
                    prepared_content = {}
                    
                    # Handle title
                    if "title" in content and "rendered" in content["title"]:
                        prepared_content["title"] = content["title"]["rendered"]
                    
                    # Handle content
                    if "content" in content and "rendered" in content["content"]:
                        prepared_content["content"] = content["content"]["rendered"]
                    
                    # Handle excerpt
                    if "excerpt" in content and "rendered" in content["excerpt"]:
                        prepared_content["excerpt"] = content["excerpt"]["rendered"]
                    
                    # Copy other fields
                    for field in content:
                        if field not in ["title", "content", "excerpt"]:
                            prepared_content[field] = content[field]
                    
                    response = requests.post(
                        endpoint,
                        json=prepared_content,
                        headers=headers
                    )
                    
                    if response.status_code not in [200, 201]:
                        raise Exception(f"Error creating {file_path.name}: {response.status_code} - {response.text}")
                
                pushed_count += 1
                
            except Exception as e:
                raise Exception(f"Error processing {file_path.name}: {str(e)}")
        
        return pushed_count, folder
