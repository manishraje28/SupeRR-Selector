import urllib.request
import urllib.parse
import json
import re
import os
import time

TARGETS = [
    ("Abhishek Sharma", "abhishek_sharma.jpg"),
    ("Tristan Stubbs", "tristan_stubbs.jpg"),
    ("Shaheen Afridi", "shaheen_afridi.jpg"),
    ("Matheesha Pathirana", "matheesha_pathirana.jpg"),
    ("Tim David", "tim_david.jpg"),
    ("Dhruv Jurel", "dhruv_jurel.jpg"),
    ("Riyan Parag", "riyan_parag.jpg"),
    ("Nathan Ellis", "nathan_ellis.jpg"),
    ("Jamie Overton", "jamie_overton.jpg"),
    ("Gudakesh Motie", "gudakesh_motie.jpg"),
    ("Mujeeb Ur Rahman", "mujeeb_ur_rahman.jpg"),
    ("Mitchell Santner", "mitchell_santner.jpg"),
    ("Mohammad Wasim", "mohammad_wasim.jpg"),
    ("Sufiyan Muqeem", "sufiyan_muqeem.jpg"),
    ("Pathum Nissanka", "pathum_nissanka.jpg"),
    ("Prabhsimran Singh", "prabhsimran_singh.jpg"),
    ("Akeal Hosein", "akeal_hosein.jpg"),
    ("Kusal Mendis", "kusal_mendis.jpg"),
    ("Sandeep Sharma", "sandeep_sharma.jpg"),
    ("Glenn Phillips", "glenn_phillips.jpg"),
]

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public", "players")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def search_cricbuzz_profile(name):
    # Try searching duckduckgo html for cricbuzz profile
    q = f"{name} site:cricbuzz.com/profiles"
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8')
            match = re.search(r'cricbuzz\.com/profiles/(\d+)/([a-z0-9\-]+)', html)
            if match:
                pid, slug = match.groups()
                return f"https://www.cricbuzz.com/profiles/{pid}/{slug}"
    except Exception as e:
        print(f"DDG search error for {name}: {e}")
    return None

def extract_cricbuzz_image(profile_url):
    try:
        req = urllib.request.Request(profile_url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8')
            # Look for player headshot in cricbuzz profile
            # e.g. https://static.cricbuzz.com/a/img/v1/i1/c.../i.jpg?d=high&amp;p=det
            matches = re.findall(r'(https://static\.cricbuzz\.com/a/img/v1/i1/c\d+/i\.jpg\?d=high(?:&amp;|&)p=det)', html)
            if matches:
                return matches[0].replace('&amp;', '&')
            # Fallback to any static.cricbuzz headshot
            fallbacks = re.findall(r'(https://static\.cricbuzz\.com/a/img/v1/i1/c\d+/[a-z0-9\-]+\.jpg)', html)
            if fallbacks:
                return fallbacks[0]
    except Exception as e:
        print(f"Profile error {profile_url}: {e}")
    return None

for name, fname in TARGETS:
    dest = os.path.join(OUT_DIR, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print(f"[EXISTS] {fname}")
        continue
    print(f"Looking up {name}...")
    purl = search_cricbuzz_profile(name)
    if purl:
        print(f"Found profile {purl}")
        img_url = extract_cricbuzz_image(purl)
        if img_url:
            try:
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=8) as r:
                    with open(dest, 'wb') as f:
                        f.write(r.read())
                print(f"[SAVED] {fname} ({os.path.getsize(dest)} bytes)")
            except Exception as e:
                print(f"Download error {img_url}: {e}")
        else:
            print(f"No image found on profile {purl}")
    else:
        print(f"No cricbuzz profile found for {name}")
    time.sleep(1.0)
