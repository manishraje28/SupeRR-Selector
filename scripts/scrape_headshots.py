import urllib.request
import re
import json

teams = [
    "rajasthan-royals",
    "sunrisers-hyderabad",
    "chennai-super-kings",
    "delhi-capitals",
    "mumbai-indians",
    "kolkata-knight-riders",
    "punjab-kings",
    "gujarat-titans",
    "lucknow-super-giants",
    "royal-challengers-bengaluru"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
found = {}

for team in teams:
    url = f"https://www.iplt20.com/teams/{team}/squad"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8')
            # Look for player cards: name and headshot image
            # Pattern in IPL squad page: class="ih-p-img" ... src="..." or data-src="..."
            # or img with IPLHeadshot
            matches = re.findall(r'<img[^>]+src="([^"]+IPLHeadshot[^"]+)"[^>]*alt="([^"]+)"', html)
            if not matches:
                matches = re.findall(r'<img[^>]*alt="([^"]+)"[^>]+src="([^"]+IPLHeadshot[^"]+)"', html)
                matches = [(m[1], m[0]) for m in matches]
            
            # Alternative: find any IPLHeadshot URL
            raw_shots = re.findall(r'(https://[^\s"\'<>]*(?:IPLHeadshot|player-headshot)[^\s"\'<>]*)', html)
            print(f"Team {team}: found {len(matches)} paired headshots, {len(raw_shots)} raw headshot URLs")
            for url, name in matches:
                found[name.strip()] = url
    except Exception as e:
        print(f"Error {team}: {e}")

print(f"Total mapped players: {len(found)}")
with open("outputs/scraped_ipl_headshots.json", "w") as f:
    json.dump(found, f, indent=2)
