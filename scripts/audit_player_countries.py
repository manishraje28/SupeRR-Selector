import json

with open('frontend/data/analytics_data.json') as f:
    d = json.load(f)

print("=== BATTERS AUDIT (Top 30) ===")
for b in d['batters'][:30]:
    print(f"{b['name']:25} | Country: {b['country']:15} | Code: {b.get('country_code', ''):5} | Franchise: {b.get('franchise_label', ''):30}")

print("\n=== BOWLERS AUDIT (Top 30) ===")
for bw in d['bowlers'][:30]:
    print(f"{bw['name']:25} | Country: {bw['country']:15} | Code: {bw.get('country_code', ''):5} | Franchise: {bw.get('franchise_label', ''):30}")
