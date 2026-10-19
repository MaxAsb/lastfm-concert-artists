#!/usr/bin/env python3
"""Update public artist names without publishing listening counts."""
import json
import os
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import time

key = os.environ['LASTFM_API_KEY']
user = os.environ['LASTFM_USER']
names = set()
for period, limit in [('7day', 20), ('1month', 30), ('3month', 20), ('12month', 10), ('overall', 10)]:
    query = urlencode({'method': 'user.gettopartists', 'user': user, 'api_key': key, 'period': period, 'limit': limit, 'format': 'json'})
    for attempt in range(5):
        try:
            with urlopen('https://ws.audioscrobbler.com/2.0/?' + query, timeout=30) as response:
                data = json.load(response)
            break
        except HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 4:
                raise RuntimeError('Last.fm request failed (HTTP ' + str(error.code) + ')') from None
        except (URLError, TimeoutError):
            if attempt == 4:
                raise RuntimeError('Last.fm network request failed') from None
        time.sleep((2, 4, 8, 16)[attempt])
    if 'error' in data:
        raise RuntimeError('Last.fm returned an API error')
    names.update(a['name'] for a in data['topartists']['artist'])
if not names:
    raise RuntimeError('No Last.fm artists returned')
Path('artists.json').write_text(json.dumps(sorted(names, key=str.casefold), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Artist names updated')
