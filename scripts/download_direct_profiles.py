import urllib.request
import re
import os
import time

PROFILES = [
    ("tristan_stubbs.jpg", "https://www.cricbuzz.com/profiles/18790/tristan-stubbs"),
    ("tim_david.jpg", "https://www.cricbuzz.com/profiles/13170/tim-david"),
    ("riyan_parag.jpg", "https://www.cricbuzz.com/profiles/12305/riyan-parag"),
    ("dhruv_jurel.jpg", "https://www.cricbuzz.com/profiles/14418/dhruv-jurel"),
    ("nathan_ellis.jpg", "https://www.cricbuzz.com/profiles/14358/nathan-ellis"),
    ("jamie_overton.jpg", "https://www.cricbuzz.com/profiles/8597/jamie-overton"),
    ("gudakesh_motie.jpg", "https://www.cricbuzz.com/profiles/10183/gudakesh-motie"),
    ("mujeeb_ur_rahman.jpg", "https://www.cricbuzz.com/profiles/13010/mujeeb-ur-rahman"),
    ("mitchell_santner.jpg", "https://www.cricbuzz.com/profiles/9692/mitchell-santner"),
    ("sandeep_sharma.jpg", "https://www.cricbuzz.com/profiles/8181/sandeep-sharma"),
    ("glenn_phillips.jpg", "https://www.cricbuzz.com/profiles/10660/glenn-phillips"),
    ("pathum_nissanka.jpg", "https://www.cricbuzz.com/profiles/13769/pathum-nissanka"),
    ("prabhsimran_singh.jpg", "https://www.cricbuzz.com/profiles/14101/prabhsimran-singh"),
    ("akeal_hosein.jpg", "https://www.cricbuzz.com/profiles/8991/akeal-hosein"),
    ("kusal_mendis.jpg", "https://www.cricbuzz.com/profiles/10200/kusal-mendis"),
    ("mohammad_wasim.jpg", "https://www.cricbuzz.com/profiles/16597/mohammad-wasim-jr"),
]

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public", "players")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

for fname, url in PROFILES:
    dest = os.path.join(OUT_DIR, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print(f"[EXISTS] {fname}")
        continue
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8')
            matches = re.findall(r'(https://static\.cricbuzz\.com/a/img/v1/i1/c\d+/i\.jpg\?d=high(?:&amp;|&)p=det)', html)
            if matches:
                img_url = matches[0].replace('&amp;', '&')
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=8) as r:
                    with open(dest, 'wb') as f:
                        f.write(r.read())
                print(f"[SUCCESS] Downloaded {fname} ({os.path.getsize(dest)} bytes)")
            else:
                print(f"[NO MATCH] {fname} on {url}")
    except Exception as e:
        print(f"[ERROR] {fname} ({url}): {e}")
    time.sleep(0.5)

print("Finished checking profiles.")
