# Sync WP MD

A Python + PySide6 application to sync local files to WordPress posts, pages, categories, menus, and media.

## Features

- Select a local directory of files
- Create or update WordPress **Posts** and **Pages** from files
- Sync **Categories** and **Menus** based on front-matter or UI settings
- Upload and manage **Media** (images, files) referenced in files

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

1. Launch the UI
2. Configure WordPress site URL and credentials
3. Choose your local files directory
4. Sync content to WordPress

### URLs

* https://prostir.info/bienvenue/wp-json/wp/v2/pages/2/revisions
* https://prostir.info/bienvenue/wp-json/wp/v2/pages/2
* https://prostir.info/bienvenue/wp-json/wp/v2/pages
* https://prostir.info/bienvenue/wp-json/wp/v2/
* https://prostir.info/bienvenue/wp-json/wp/
* https://prostir.info/bienvenue/wp-json/

### Updating Content

When updating existing posts or pages:
1. Modify the content in the local JSON file
2. Update the `modified` and `modified_gmt` dates in the JSON file to the current time
3. Push the content to WordPress

This is necessary because the push operation uses the modification date to determine which content has been updated locally.

## License

MIT
