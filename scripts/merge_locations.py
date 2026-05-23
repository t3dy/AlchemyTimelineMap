#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge enhanced locations into seed_data.json"""

import json
from pathlib import Path

seed_path = Path(__file__).parent.parent / "data" / "seed_data.json"
enhanced_path = Path(__file__).parent.parent / "data" / "locations_enhanced.json"

# Read both files
with open(seed_path, 'r', encoding='utf-8') as f:
    seed_data = json.load(f)

with open(enhanced_path, 'r', encoding='utf-8') as f:
    enhanced_data = json.load(f)

# Replace locations array
seed_data['locations'] = enhanced_data['locations']

# Write back
with open(seed_path, 'w', encoding='utf-8') as f:
    json.dump(seed_data, f, indent=2, ensure_ascii=False)

print(f"Updated seed_data.json with {len(seed_data['locations'])} enhanced locations")
