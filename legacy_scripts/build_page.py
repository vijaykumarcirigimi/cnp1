import os
import re
from bs4 import BeautifulSoup

LIBRARY_DIR = r"c:\Users\Vijay\OneDrive\Documents\CNP\Library"
OUTPUT_FILE = r"c:\Users\Vijay\OneDrive\Documents\CNP\assessment-development-centers.html"

# This array dictates the sequence of sections explicitly corresponding to the S01-S24 plan
SECTIONS = [
    ("edstellar-hero-classic-split.html", "S01"),
    ("edstellar-definitional-intro.html", "S02"),
    ("edstellar-challenges-section-with-image.html", "S03"),
    ("edstellar-stats-card-grid.html", "S04"),
    ("edstellar-three-pillars-cards.html", "S05"),
    ("edstellar-services-option-b.html", "S06"),
    ("edstellar-service-explained-in-detail-option-with-image.html", "S07"),
    ("edstellar-detailed-explanation-of-service-with-image-and-accordion.html", "S08"),
    ("edstellar-service-explained-in-detail-option-with-image.html", "S09"),
    ("edstellar-process-vertical-stepper.html", "S10"), # wait, docx S10 was development centers -> process-vertical-stepper
    ("edstellar-outcomes-horizontal-tabs.html", "S11"), # virtual/hybrid AC -> horizontal-tabs
    ("edstellar-industries-selectable-tiles.html", "S12"), # assessor training
    ("edstellar-differentiators-option-a.html", "S13"), # approach
    ("edstellar-success-stories-light-version-with-image.html", "S14"), # outcomes
    ("edstellar-testimonials-section-with-small-user-thumbnail.html", "S15"), # industries
    ("edstellar-logo-wall.html", "S16"), # why choose
    ("edstellar-faq-section.html", "S17"), # case studies (wait, S17 is Case Studies, but uses FAQ module? Or FAQ uses FAQ?)
]

# Wait, the mapping in the docx text file:
# 02 edstellar-hero-classic-split.html
# 03 edstellar-definitional-intro.html
# 04 edstellar-challenges-section-with-image.html
# 05 edstellar-stats-card-grid.html
# 06 edstellar-three-pillars-cards.html
# 07 edstellar-services-option-b.html
# 08 edstellar-service-explained-in-detail-option-with-image.html
# 09 edstellar-detailed-explanation-of-service-with-image-and-accordion.html
# 10 edstellar-service-explained-in-detail-option-with-image.html
# 11 edstellar-process-vertical-stepper.html
# 12 edstellar-outcomes-horizontal-tabs.html
# 13 edstellar-industries-selectable-tiles.html
# 14 edstellar-differentiators-option-a.html
# 15 edstellar-success-stories-light-version-with-image.html
# 16 edstellar-testimonials-section-with-small-user-thumbnail.html
# 17 edstellar-logo-wall.html
# 18 edstellar-faq-section.html
# 19 edstellar-download-asset-option-c.html
# 20 edstellar-cta-banner-lime.html
# 21 edstellar-form-section.html
# 22 edstellar-connected-services-navy-scroll.html
# 23 edstellar-resources-section.html
# 24 edstellar-footer.html

# Let's write a script that just reads all templates, extracts their CSS, and concatenates their bodies into one file.
# We will do EXACT string replacements on the final concatenated string.

def build_page():
    templates = [
        "edstellar-hero-classic-split.html",
        "edstellar-definitional-intro.html",
        "edstellar-challenges-section-with-image.html",
        "edstellar-stats-card-grid.html",
        "edstellar-three-pillars-cards.html",
        "edstellar-services-option-b.html",
        "edstellar-service-explained-in-detail-option-with-image.html",
        "edstellar-detailed-explanation-of-service-with-image-and-accordion.html",
        "edstellar-service-explained-in-detail-option-with-image.html",
        "edstellar-process-vertical-stepper.html",
        "edstellar-outcomes-horizontal-tabs.html",
        "edstellar-industries-selectable-tiles.html",
        "edstellar-differentiators-option-a.html",
        "edstellar-success-stories-light-version-with-image.html",
        "edstellar-testimonials-section-with-small-user-thumbnail.html",
        "edstellar-logo-wall.html",
        "edstellar-faq-section.html",
        "edstellar-download-asset-option-c.html",
        "edstellar-cta-banner-lime.html",
        "edstellar-form-section.html",
        "edstellar-connected-services-navy-scroll.html",
        "edstellar-resources-section.html",
        "edstellar-footer.html"
    ]

    styles = set()
    body_content = []

    # Helper to parse and extract
    for tpl in templates:
        path = os.path.join(LIBRARY_DIR, tpl)
        if not os.path.exists(path):
            print(f"Warning: {tpl} not found")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Extract styles
        for style in soup.find_all('style'):
            styles.add(style.string)
            
        # Extract the main section logic
        for body in soup.find_all('body'):
            # Some templates have scripts, let's keep them if they are inside body
            inner_html = "".join([str(c) for c in body.contents])
            # Append a comment block to identify section
            body_content.append(f"<!-- Section: {tpl} -->\n{inner_html}")

    final_styles = "\n".join(styles)
    merged_body = "\n".join(body_content)

    final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assessment and Development Center Consulting | Edstellar</title>
    <meta name="description" content="Design and deploy competency-based assessment centers and development centers with Edstellar's consulting expertise.">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
{final_styles}
    </style>
</head>
<body>
{merged_body}
</body>
</html>"""

    # Do brute-force text replacements to map content
    # S01: Hero
    final_html = final_html.replace("Learning and Development<br>\n          <span class=\"accent\">Consulting Services</span>", "Assessment and Development Center<br>\n          <span class=\"accent\">Consulting</span>")
    final_html = final_html.replace("Transfer of expertise, not dependency", "Validated competency frameworks mapped to role-specific success profiles")
    final_html = final_html.replace("Custom L&D frameworks built for your industry", "Behavioral simulation exercises with predictive validity of r = 0.51+")
    final_html = final_html.replace("Trusted by Fortune 500 enterprises", "Assessment center programs deployed across 30+ industries globally")
    final_html = final_html.replace("Schedule a Free L&D Consultation", "Talk to an Assessment Center Consultant")
    final_html = final_html.replace("View Our Methodology", "Download the Assessment Center Design Toolkit")
    
    # Write the file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == "__main__":
    build_page()
