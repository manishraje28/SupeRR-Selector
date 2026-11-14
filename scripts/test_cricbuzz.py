import urllib.request
import re

url = 'https://www.cricbuzz.com/profiles/10209/heinrich-klaasen'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=8) as r:
        html = r.read().decode('utf-8')
        imgs = re.findall(r'https://static\.cricbuzz\.com/a/img/v1/[^\s"\'<>]+', html)
        print('Cricbuzz images for Klaasen:', imgs)
except Exception as e:
    print('Error:', e)
