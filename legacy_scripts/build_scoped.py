import os
import cssutils
import logging
from bs4 import BeautifulSoup

cssutils.log.setLevel(logging.CRITICAL)

LIBRARY_DIR = r"c:\Users\Vijay\OneDrive\Documents\CNP\Library"
OUTPUT_FILE = r"c:\Users\Vijay\OneDrive\Documents\CNP\assessment-development-centers.html"

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

def scope_selectorList(selectorList, scope_id):
    for selector in selectorList:
        text = selector.selectorText
        if text.startswith(':root') or text.startswith('body') or text.startswith('html'):
            selector.selectorText = text.replace(':root', f'#{scope_id}').replace('body', f'#{scope_id}').replace('html', f'#{scope_id}')
        else:
            selector.selectorText = f"#{scope_id} {text}"

def build_page():
    styles = []
    body_content = []

    for idx, tpl in enumerate(templates):
        path = os.path.join(LIBRARY_DIR, tpl)
        if not os.path.exists(path):
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        
        scope_id = f"s{idx:02d}_module"
        
        # Extract and scope styles
        for style in soup.find_all('style'):
            sheet = cssutils.parseString(style.string)
            for rule in sheet:
                if rule.type == rule.STYLE_RULE:
                    scope_selectorList(rule.selectorList, scope_id)
                elif rule.type == rule.MEDIA_RULE:
                    for inner_rule in rule.cssRules:
                        if inner_rule.type == inner_rule.STYLE_RULE:
                            scope_selectorList(inner_rule.selectorList, scope_id)
            styles.append(sheet.cssText.decode('utf-8'))
            
        # Extract body
        for body in soup.find_all('body'):
            inner_html = "".join([str(c) for c in body.contents])
            body_content.append(f"""<!-- Section: {tpl} -->\n<div id="{scope_id}">\n{inner_html}\n</div>""")

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

    # Do baseline manual string replacements from before
    final_html = final_html.replace("Learning and Development<br>\n          <span class=\"accent\">Consulting Services</span>", "Assessment and Development Center<br>\n          <span class=\"accent\">Consulting</span>")
    final_html = final_html.replace("Transfer of expertise, not dependency", "Validated competency frameworks mapped to role-specific success profiles")
    final_html = final_html.replace("Custom L&D frameworks built for your industry", "Behavioral simulation exercises with predictive validity of r = 0.51+")
    final_html = final_html.replace("Trusted by Fortune 500 enterprises", "Assessment center programs deployed across 30+ industries globally")
    final_html = final_html.replace("Schedule a Free L&D Consultation", "Talk to an Assessment Center Consultant")
    final_html = final_html.replace("View Our Methodology", "Download the Assessment Center Design Toolkit")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print("Scoped HTML generated!")

if __name__ == "__main__":
    build_page()
