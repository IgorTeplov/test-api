"""File with configuration generator for flask."""

import json
import uuid
from pathlib import Path


def create_configs():
    """Create a configuration file if the file does not exist."""
    if not (Path.cwd()/'config.json').is_file():
        with open('config.json', 'w') as jfile:
            json.dump({'SECRET_KEY': str(uuid.uuid4())}, jfile)
