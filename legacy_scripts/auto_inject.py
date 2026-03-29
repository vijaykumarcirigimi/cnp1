import os
from bs4 import BeautifulSoup

INPUT_FILE = r"c:\Users\Vijay\OneDrive\Documents\CNP\assessment-development-centers.html"
OUTPUT_FILE = r"c:\Users\Vijay\OneDrive\Documents\CNP\assessment-development-centers.html"

def inject():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    def get_section(idx, filename):
        comments = soup.find_all(string=lambda text: text and filename in text and "Section:" in text)
        if len(comments) > idx:
            # return the div/section immediately following the comment
            node = comments[idx].next_element
            while node and getattr(node, 'name', None) is None:
                node = node.next_element
            return node
        return None

    # S09: High-Potential Identification Centers (Uses edstellar-service-explained-in-detail-option-with-image.html, index 1 because S07 used it too)
    s09 = get_section(1, "edstellar-service-explained-in-detail-option-with-image.html")
    if s09:
        h2 = s09.find('h2')
        if h2: h2.string = "High-Potential Identification Centers"
        p_lead = s09.find('p', class_='sub')
        if not p_lead: p_lead = s09.find('p')
        if p_lead: p_lead.string = "Every organization has talent that outperforms expectations, but performance alone does not predict potential. Research consistently shows that only 1 in 7 high performers is also a high-potential leader. Edstellar's high-potential identification consulting service objectively evaluates the cognitive, motivational, and behavioral factors."
        
        h3s = s09.find_all('h3')
        if len(h3s) >= 2:
            h3s[0].string = "High-Potential Assessment Criteria Design"
            h3s[1].string = "Structured HiPo Assessment Programs"
        ps = s09.find_all('p')
        # skip first p which might be lead
        if len(ps) >= 3:
            ps[1].string = "We define the specific dimensions that distinguish high-potential talent in your organizational context. Beyond generic models, we calibrate criteria across four evidence-based domains."
            ps[2].string = "We design and deploy multi-method assessment programs that combine cognitive ability testing, personality and motivation inventories, learning agility exercises, structured behavioral interviews, and simulation-based exercises."

    # S10: Development Centers (Uses edstellar-process-vertical-stepper.html)
    s10 = get_section(0, "edstellar-process-vertical-stepper.html")
    if s10:
        h2 = s10.find('h2')
        if h2:
            h2.clear()
            h2.append(BeautifulSoup("<span class='accent'>Development</span> <span class='dark'>Centers</span>", "html.parser"))
        ps = s10.find_all('p')
        if len(ps) > 0:
            ps[0].string = "Assessment centers tell you where talent stands. Development centers tell talent where to grow. While assessment centers focus on producing objective evaluation data for organizational decision-making, development centers use the same simulation-based methodology with a fundamentally different purpose: generating rich, behaviorally specific developmental feedback that accelerates individual leadership growth."
            
        h4s = s10.find_all('h4')
        if len(h4s) >= 3:
            h4s[0].string = "Developmental Simulation Design"
            h4s[1].string = "Individualized Development Plan (IDP) Creation"
            h4s[2].string = "Coaching Integration and Follow-Through"

    # S11: Virtual and Hybrid Assessment Centers (Uses edstellar-outcomes-horizontal-tabs.html)
    s11 = get_section(0, "edstellar-outcomes-horizontal-tabs.html")
    if s11:
        h2 = s11.find('h2')
        if h2: h2.string = "Virtual and Hybrid Assessment Centers"
        p_lead = s11.find('p')
        if p_lead: p_lead.string = "The shift to distributed workforces has permanently changed how organizations assess talent. Virtual assessment centers are no longer a pandemic workaround but a strategic capability that enables organizations to evaluate talent across geographies, reduce assessment logistics costs by up to 60%, and deliver candidate experiences that consistently earn satisfaction ratings above 85%."
        
        tabs = s11.select('.tab-label')
        if tabs and len(tabs) >= 3:
            tabs[0].string = "Digital Platform Design"
            tabs[1].string = "Virtual Simulation Adaptation"
            tabs[2].string = "Remote Assessor Protocols"

    # S12: Assessor Training and Capability Transfer (Uses edstellar-industries-selectable-tiles.html)
    s12 = get_section(0, "edstellar-industries-selectable-tiles.html")
    if s12:
        h2 = s12.find('h2')
        if h2: h2.string = "Assessor Training and Capability Transfer"
        p_sub = s12.find('p')
        if p_sub: p_sub.string = "The quality of an assessment center is only as good as the quality of its assessors. Research consistently shows that assessor training is the single most significant factor influencing assessment center validity. Edstellar's assessor training builds your organization's internal capacity to design, deploy, and evaluate assessment centers independently."
        
        tiles = s12.select('.tile-name')
        if tiles and len(tiles) >= 4:
            tiles[0].string = "Assessor Certification"
            tiles[1].string = "Observation Training"
            tiles[2].string = "Administration"
            tiles[3].string = "Continuous Calibration"

    # S13: Approach (Uses edstellar-differentiators-option-a.html)
    s13 = get_section(0, "edstellar-differentiators-option-a.html")
    if s13:
        h2 = s13.find('h2')
        if h2: h2.string = "Our Approach to Assessment and Development Center Consulting"
        p_sub = s13.find('p')
        if p_sub: p_sub.string = "Edstellar follows a proven five-phase methodology that takes organizations from ad hoc talent evaluation to a structured, validated assessment and development center capability."
        
        diff_h4s = s13.find_all('h4')
        if len(diff_h4s) >= 5:
            diff_h4s[0].string = "PHASE 1: Discover"
            diff_h4s[1].string = "PHASE 2: Design"
            diff_h4s[2].string = "PHASE 3: Pilot"
            diff_h4s[3].string = "PHASE 4: Deploy"
            diff_h4s[4].string = "PHASE 5: Sustain"

    # S14: Outcomes & Deliverables (Uses edstellar-success-stories-light-version-with-image.html)
    s14 = get_section(0, "edstellar-success-stories-light-version-with-image.html")
    if s14:
        h2 = s14.find('h2')
        if h2: h2.string = "Outcomes & Deliverables"
        p_quote = s14.find('p', class_='quote')
        if p_quote: p_quote.string = "Each engagement delivers tangible, reusable assets that your organization owns and operates independently. These are the concrete deliverables your talent team retains and uses to make better talent decisions every day."

    # S15: Industries We Serve (Uses edstellar-testimonials-section-with-small-user-thumbnail.html)
    s15 = get_section(0, "edstellar-testimonials-section-with-small-user-thumbnail.html")
    if s15:
        h2 = s15.find('h2')
        if h2: h2.string = "Assessment and Development Centers Across Industries"
        p_desc = s15.find('p')
        if p_desc: p_desc.string = "Every industry has unique leadership challenges, regulatory requirements, and competency demands that shape how assessment and development centers must be designed. Edstellar adapts our assessment center methodology to your industry's talent landscape."
        names = s15.find_all('h4')
        if len(names) >= 2:
            names[0].string = "Financial Services & Banking"
            names[1].string = "Technology & SaaS"

    # S16: Why Choose Edstellar (Uses edstellar-logo-wall.html)
    s16 = get_section(0, "edstellar-logo-wall.html")
    if s16:
        h2 = s16.find('h2')
        if h2: h2.string = "Why Choose Edstellar for Assessment Center Consulting?"

    # S17: FAQ (Uses edstellar-faq-section.html)
    s17 = get_section(0, "edstellar-faq-section.html")
    if s17:
        h2 = s17.find('h2')
        if h2: h2.string = "Frequently Asked Questions About Assessment and Development Centers"
        q_texts = s17.select('.faq-question h3')
        if q_texts and len(q_texts) >= 3:
            q_texts[0].string = "What is the difference between an assessment center and a development center?"
            q_texts[1].string = "How long does a typical assessment center take to design and deploy?"
            q_texts[2].string = "What types of exercises are used in an assessment center?"

    # S18 to S24: Download Asset, CTA, Form, Connected Services, Resources, Footer
    # Applying simple header replacements
    s18 = get_section(0, "edstellar-download-asset-option-c.html")
    if s18:
        h2 = s18.find('h2')
        if h2: h2.string = "Assessment Center Design Toolkit"
    
    s19 = get_section(0, "edstellar-cta-banner-lime.html")
    if s19:
        h2 = s19.find('h2')
        if h2: h2.string = "Ready to Build an Assessment Center That Actually Predicts Leadership Success?"
    
    s20 = get_section(0, "edstellar-form-section.html")
    if s20:
        h2 = s20.find('h2')
        if h2: h2.string = "Let's Design Your Assessment and Development Center"
    
    s21 = get_section(0, "edstellar-connected-services-navy-scroll.html")
    if s21:
        h2 = s21.find('h2')
        if h2: h2.string = "Explore Related Consulting Services"

    s22 = get_section(0, "edstellar-resources-section.html")
    if s22:
        h2 = s22.find('h2')
        if h2: h2.string = "Assessment and Development Center Insights"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Injected S09 through S24 successfully.")

if __name__ == "__main__":
    inject()
