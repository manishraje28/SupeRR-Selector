import os
import re
import json
import time
import urllib.request
import urllib.parse

PLAYERS = [
    # Top Batters
    ("Heinrich Klaasen", "heinrich_klaasen.jpg", "Sunrisers Hyderabad"),
    ("Abhishek Sharma", "abhishek_sharma.jpg", "Sunrisers Hyderabad"),
    ("Tristan Stubbs", "tristan_stubbs.jpg", "Delhi Capitals"),
    ("Tim David", "tim_david.jpg", "Mumbai Indians"),
    ("Pathum Nissanka", "pathum_nissanka.jpg", "Sri Lanka"),
    ("Prabhsimran Singh", "prabhsimran_singh.jpg", "Punjab Kings"),
    ("Akeal Hosein", "akeal_hosein.jpg", "West Indies"),
    ("Kusal Mendis", "kusal_mendis.jpg", "Sri Lanka"),
    ("Glenn Phillips", "glenn_phillips.jpg", "Sunrisers Hyderabad"),
    
    # Top Bowlers
    ("Shaheen Afridi", "shaheen_afridi.jpg", "Pakistan"),
    ("Matheesha Pathirana", "matheesha_pathirana.jpg", "Chennai Super Kings"),
    ("Abrar Ahmed", "abrar_ahmed.jpg", "Pakistan"),
    ("Jamie Overton", "jamie_overton.jpg", "England"),
    ("Nathan Ellis", "nathan_ellis.jpg", "Punjab Kings"),
    ("Gudakesh Motie", "gudakesh_motie.jpg", "West Indies"),
    ("Mujeeb Ur Rahman", "mujeeb_ur_rahman.jpg", "Kolkata Knight Riders"),
    ("Bhuvneshwar Kumar", "bhuvneshwar_kumar.jpg", "Sunrisers Hyderabad"),
    ("Mitchell Santner", "mitchell_santner.jpg", "Chennai Super Kings"),
    ("Mohammad Wasim", "mohammad_wasim.jpg", "Pakistan"),
    ("Sufiyan Muqeem", "sufiyan_muqeem.jpg", "Pakistan"),
    
    # Rajasthan Royals Core
    ("Sanju Samson", "sanju_samson.jpg", "Rajasthan Royals"),
    ("Riyan Parag", "riyan_parag.jpg", "Rajasthan Royals"),
    ("Dhruv Jurel", "dhruv_jurel.jpg", "Rajasthan Royals"),
    ("Shimron Hetmyer", "shimron_hetmyer.jpg", "Rajasthan Royals"),
    ("Sandeep Sharma", "sandeep_sharma.jpg", "Rajasthan Royals"),
    ("Trent Boult", "trent_boult.jpg", "Rajasthan Royals"),
    ("Yuzvendra Chahal", "yuzvendra_chahal.jpg", "Rajasthan Royals"),
]

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public", "players")
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def search_cricinfo_image(player_name):
    query = f"{player_name} espncricinfo player profile"
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8")
            # find cricinfo player url
            match = re.search(r'espncricinfo\.com/cricketers/([a-z0-9\-]+)-(\d+)', html)
            if not match:
                match = re.search(r'espncricinfo\.com/player/([a-z0-9\-]+)-(\d+)', html)
            if match:
                slug, pid = match.groups()
                profile_url = f"https://www.espncricinfo.com/cricketers/{slug}-{pid}"
                req_p = urllib.request.Request(profile_url, headers=HEADERS)
                time.sleep(0.5)
                with urllib.request.urlopen(req_p, timeout=8) as resp_p:
                    p_html = resp_p.read().decode("utf-8")
                    img_match = re.search(r'(https://img1\.hscicdn\.com/image/upload/[^"\']+\.(?:png|jpg|jpeg))', p_html)
                    if img_match:
                        return img_match.group(1)
    except Exception as e:
        print(f"Error searching cricinfo for {player_name}: {e}")
    return None

def download_file(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        with open(dest, "wb") as f:
            f.write(resp.read())

def run():
    print(f"Checking images in {OUT_DIR}...")
    success = 0
    for name, fname, team in PLAYERS:
        dest = os.path.join(OUT_DIR, fname)
        if os.path.exists(dest) and os.path.getsize(dest) > 5000:
            print(f"[OK] {name} already exists ({os.path.getsize(dest)} bytes)")
            success += 1
            continue
        print(f"Searching image for {name} ({team})...")
        img_url = search_cricinfo_image(name)
        if img_url:
            try:
                download_file(img_url, dest)
                print(f"[SUCCESS] Downloaded {name} -> {fname} ({os.path.getsize(dest)} bytes)")
                success += 1
            except Exception as e:
                print(f"[ERROR] Failed downloading {img_url}: {e}")
        else:
            print(f"[NOT FOUND] Could not find photo for {name}")
        time.sleep(1.0)
    print(f"Finished: {success}/{len(PLAYERS)} images ready.")

if __name__ == "__main__":
    run()
