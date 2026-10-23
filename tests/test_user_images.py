import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image, ImageDraw
from region_guard import RegionGuard
from disease_engine import DiseaseEngine

guard = RegionGuard()
engine = DiseaseEngine()

# Synthetic non-human items
biscuit_pack = Image.new('RGB', (450, 300), color=(210, 150, 40))
d = ImageDraw.Draw(biscuit_pack)
d.text((40, 40), 'DELICIOUS BISCUITS 100g', fill=(255, 255, 255))
d.ellipse([(140, 90), (280, 210)], fill=(180, 110, 20), outline=(255, 255, 0))

clothes_pack = Image.new('RGB', (400, 400), color=(30, 55, 110))
d2 = ImageDraw.Draw(clothes_pack)
for i in range(0, 400, 8):
    d2.line([(0, i), (400, i)], fill=(35, 65, 125), width=2)

phone_gadget = Image.new('RGB', (300, 500), color=(20, 20, 25))
d3 = ImageDraw.Draw(phone_gadget)
d3.rectangle([(20, 40), (280, 460)], fill=(15, 15, 20), outline=(80, 80, 80))
d3.text((80, 250), '12:45 PM - SMARTPHONE', fill=(200, 200, 200))

paper_doc = Image.new('RGB', (400, 500), color=(250, 250, 250))
d4 = ImageDraw.Draw(paper_doc)
for i in range(50, 450, 30):
    d4.line([(40, i), (360, i)], fill=(40, 40, 40), width=3)

test_suite = [
    ('Marie Gold / Milk Biscuit Packet Cover', r'C:\Users\ks670\OneDrive\Desktop\Expiry.jpg', 'Face & Neck', None),
    ('Demo1 Packaging Graphic', r'C:\Users\ks670\Downloads\demo1.jpg', 'Face & Neck', None),
    ('Normal Face 1', r'C:\Users\ks670\Downloads\WhatsApp Image 2026-07-07 at 2.39.55 PM.jpeg', 'Face & Neck', None),
    ('Acne Photo', r'C:\Users\ks670\OneDrive\Desktop\acne.jpg', 'Face & Neck', None),
    ('Normal Hand', r'C:\Users\ks670\Downloads\WhatsApp Image 2026-10-01 at 7.12.36 AM.jpeg', 'Hands, Palms & Nails', None),
    ('Mismatch Test 1 (Hand as Face)', r'C:\Users\ks670\Downloads\WhatsApp Image 2026-10-01 at 7.12.36 AM.jpeg', 'Face & Neck', None),
    ('Mismatch Test 2 (Face as Hand)', r'C:\Users\ks670\Downloads\WhatsApp Image 2026-07-07 at 2.39.55 PM.jpeg', 'Hands, Palms & Nails', None),
    ('Synthetic Biscuit Packet Test', None, 'Hands, Palms & Nails', biscuit_pack),
    ('Clothing Occlusion Test', None, 'Chest & Abdomen', clothes_pack),
    ('Smartphone Gadget Test', None, 'Face & Neck', phone_gadget),
    ('Paper Document Test', None, 'Hands, Palms & Nails', paper_doc),
    ('ChatGPT Image Test', r'C:\Users\ks670\Downloads\ChatGPT Image Oct 1, 2026, 02_29_44 PM.png', 'Face & Neck', None)
]

print("=" * 70)
print("DERMAVISION CLINICAL & UNIVERSAL SAFETY VALIDATION SUITE")
print("=" * 70)

for label, path, target_region, img_obj in test_suite:
    if img_obj is not None:
        img = img_obj
        fname = f"{label.replace(' ', '_').lower()}.jpg"
    elif path and os.path.exists(path):
        img = Image.open(path).convert('RGB')
        fname = os.path.basename(path)
    else:
        continue

    res_guard = guard.verify_region(img, target_region, image_filename=fname)
    print(f"\n>>> [{label}]")
    print(f"  Target Region Selected: {target_region}")
    print(f"  Guard Status: {res_guard['status']}")
    print(f"  Detected As: {res_guard['detected_region']} ({res_guard['confidence']}%)")
    print(f"  Is Valid Match: {res_guard['is_match']}")

    if res_guard['is_match']:
        res_diag = engine.diagnose(img, target_region, image_filename=fname)
        print(f"  [DIAGNOSIS EXECUTED]: {res_diag['condition']['name']} ({res_diag['confidence']}%)")
        print(f"  Top Candidates: {[c['name'] + ' (' + str(c['confidence']) + '%)' for c in res_diag['top_candidates']]}")
    else:
        print(f"  [DIAGNOSIS REFUSED - SAFETY GUARD ACTIVE]: Blocked by {res_guard['status']}")
