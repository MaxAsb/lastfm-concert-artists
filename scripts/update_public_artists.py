#!/usr/bin/env python3
"""Update public artist names without publishing listening counts."""
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

key = os.environ['LASTFM_API_KEY']
user = os.environ['LASTFM_USER']
names = set()
for period, limit in [('7day', 20), ('1month', 30), ('3month', 20), ('12month', 10), ('overall', 10)]:
    query = urlencode({'method': 'user.gettopartists', 'user': user, 'api_key': key, 'period': period, 'limit': limit, 'format': 'json'})
    with urlopen('https://ws.audioscrobbler.com/2.0/?' + query, timeout=30) as response:
        data = json.load(response)
    if 'error' in data:
        raise RuntimeError('Last.fm returned an API error')
    names.update(a['name'] for a in data['topartists']['artist'])
if not names:
    raise RuntimeError('No Last.fm artists returned')
Path('artists.json').write_text(json.dumps(sorted(names, key=str.casefold), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Artist names updated')
