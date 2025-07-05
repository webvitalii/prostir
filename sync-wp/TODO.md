# TODO

* Config screen
* Sync categories
* Sync menues
* Sync media
* Do not update file if no changes done (or if date is the same)

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

