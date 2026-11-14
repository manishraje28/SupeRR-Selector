import urllib.request
import urllib.parse
import json
import re
import time
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "public", "players")

def get_ddg_image(query):
    # Step 1: get token vqd
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}&iax=images&ia=images"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8')
            vqd_match = re.search(r'vqd=([0-9\-]+)', html)
            if not vqd_match:
                vqd_match = re.search(r'vqd="([0-9\-]+)"', html)
            if not vqd_match:
                return None
            vqd = vqd_match.group(1)
            
            # Step 2: call i.js endpoint
            img_url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,&p=1"
            req_i = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(req_i, timeout=5) as resp_i:
                data = json.loads(resp_i.read().decode('utf-8'))
                results = data.get("results", [])
                for r in results:
                    img = r.get("image")
                    if img and (img.endswith(".jpg") or img.endswith(".png")):
                        return img
    except Exception as e:
        print(f"Error {query}: {e}")
    return None

test = get_ddg_image("Heinrich Klaasen cricketer portrait")
print("Test result:", test)
