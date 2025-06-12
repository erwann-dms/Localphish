import os

PHISH_PAGES_DIR = "phish_pages"

def list_campaigns():
    return [d for d in os.listdir(PHISH_PAGES_DIR) if os.path.isdir(os.path.join(PHISH_PAGES_DIR, d))]
