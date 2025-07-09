# TODO

* Config screen
* Sync categories
* Sync menues
* Sync media
* Do not update file if no changes done (or if date is the same)
* Pull media files with media item

# Add new content types: https://prostir.info/bienvenue/wp-json/
* users - WordPress users
* taxonomies - Custom taxonomies
* post_types - Custom post types
* post_statuses - Draft, published, private, etc.
* revisions - Post and page revisions
* settings - WordPress site settings
* themes - Installed themes
* plugins - Installed plugins
* blocks - Gutenberg blocks
* menus - Navigation menus
* menu-items - Individual menu items
* products - WooCommerce products
* orders - WooCommerce orders
* customers - WooCommerce customers
* content_type - Custom content types {site_url}/wp-json/wp/v2/{content_type} (comma separated text field)


# Future Features

## backup_database

```python
def backup_database(self):
    """Backup WordPress database"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"
    self.run_wp_cli(['db', 'export', backup_file])
    return backup_file
```
## search_replace

```python
def update_urls(self, old_url: str, new_url: str):
    """Update URLs in WordPress database"""
    self.run_wp_cli(['search-replace', old_url, new_url])
```

