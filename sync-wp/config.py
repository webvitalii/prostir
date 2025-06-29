from pathlib import Path

# Site configuration
SITE_URL = "https://prostir.info/bienvenue"

# Get the project root directory (parent of sync-wp)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Output directory relative to project root
OUTPUT_DIR = PROJECT_ROOT / "sites" / "bienvenue"
