import os
from bs4 import BeautifulSoup
import re

INPUT_FILE = r"c:\Users\Vijay\OneDrive\Documents\CNP\assessment-development-centers.html"
OUTPUT_FILE = r"c:\Users\Vijay\OneDrive\Documents\CNP\assessment-development-centers.html"

def inject():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    # Finding sections using comments we injected
    sections = []
    for comment in soup.find_all(string=lambda text: isinstance(text, str) and text.strip().startswith("Section:")):
        sections.append(comment.parent)
        
    # Wait, the comment is a child of body, we need to iterate body contents to find bounded section nodes, 
    # but beautifulsoup doesn't easily group siblings by preceding comment.
    # Instead, let's use global selector indices.

    # S05: Three Pillars (edstellar-three-pillars-cards.html is the 5th template)
    # Let's find all h2 tags. They are somewhat unique per section.
    # The string we replace relies on original template boilerplate text.
    
    # We will just write a function to replace text by finding generic headers.
    def replace_by_regex(pattern, new_html):
        node = soup.find(string=re.compile(pattern))
        if node:
            node.replace_with(BeautifulSoup(new_html, "html.parser"))
            return True
        return False

    # This is much easier!
    
    # S05: Three Pillars
    replace_by_regex("The 3 core pillars of our approach", "Design. Deploy. Develop. The Three Pillars of Assessment Excellence.")
    replace_by_regex("We deliver comprehensive solutions that cover strategy, execution, and continuous improvement.", "Effective talent assessment is not a single event but an integrated system. Edstellar's assessment and development center consulting practice connects three pillars: rigorous design that ensures every exercise measures what matters, seamless deployment that delivers a world-class participant experience, and developmental integration that transforms assessment data into accelerated leadership growth.")
    
    replace_by_regex("Diagnostic & Strategy", "PILLAR 1: Design")
    replace_by_regex("We assess your current environment, identify gaps, and architect a comprehensive blueprint for success.", "Build the assessment architecture from the ground up. We design competency frameworks mapped to role-specific success profiles, create behaviorally anchored simulation exercises, select and validate psychometric instruments, develop assessor rating guides, and engineer the scoring methodology.")
    
    replace_by_regex("Implementation & Rollout", "PILLAR 2: Deploy")
    replace_by_regex("Our specialists work alongside your team to execute the plan with precision, ensuring minimal disruption.", "Execute assessment and development centers with precision. We manage end-to-end logistics, deliver in-person, virtual, or hybrid assessment experiences, coordinate certified assessor panels, facilitate simulation exercises, and produce same-day participant feedback.")
    
    replace_by_regex("Optimization & Growth", "PILLAR 3: Develop")
    replace_by_regex("Post-deployment, we establish feedback loops and optimize processes for sustained, long-term impact.", "Connect assessment insights to development action. We translate competency scores into individualized development plans, design targeted learning interventions for identified gaps, integrate assessment data with succession planning, and build internal assessor capability.")

    # S06: Our Services (6 Tiles) edstellar-services-option-b.html
    replace_by_regex("Key Focus Areas", "Our Assessment and Development Center Consulting Services")
    replace_by_regex("We offer targeted capabilities designed to address the most critical aspects of your transformation journey.", "Edstellar delivers six integrated assessment center consulting solutions that take organizations from subjective talent decisions to evidence-based assessment infrastructure. Each service can be engaged independently or as part of a comprehensive assessment center transformation.")
    
    srv_names = [
        "Competency Framework and Assessment Design",
        "Leadership Assessment Centers",
        "High-Potential Identification Centers",
        "Development Centers",
        "Virtual and Hybrid Assessment Centers",
        "Assessor Training and Capability Transfer"
    ]
    srv_desc = [
        "Architect the competency models, behavioral indicators, simulation exercises, and scoring systems that form the foundation of every assessment and development center.",
        "Deploy structured, multi-method assessment centers that evaluate senior and emerging leaders against validated competency frameworks.",
        "Design and execute assessment programs that objectively identify high-potential talent across your organization. Move beyond manager nominations.",
        "Shift the lens from selection to growth. Our development center consulting services use the same simulation-based methodology as assessment centers but focus on generating rich developmental feedback.",
        "Design and deploy technology-enabled assessment centers that deliver the rigor of in-person evaluation through digital platforms.",
        "Build your organization's internal assessment center capability. We train and certify your HR professionals, business leaders, and talent management teams as qualified assessors."
    ]
    
    # finding tab names: "Strategic Planning" etc.
    pills = soup.select('.ed-pill')
    if pills:
        for i in range(min(6, len(srv_names))):
            pills[i].string = srv_names[i]
            
    # S07 Service Deep-Dive 1
    replace_by_regex("Service Detail Block One", "Competency Framework and Assessment Design")
    replace_by_regex("We provide an in-depth capability that transforms how your organisation operates.", "Every effective assessment center begins with a rigorous competency framework that defines what good looks like for each target role.")
    
    s7_f1 = "Competency Model Development"
    s7_d1 = "We conduct structured job analyses, stakeholder interviews, and strategic alignment workshops to identify the 6 to 10 competencies that differentiate high performance in each target role."
    s7_f2 = "Behavioral Simulation Exercise Design"
    s7_d2 = "We design custom simulation exercises that create realistic opportunities for participants to demonstrate target competencies under conditions that mirror actual job demands."
    
    replace_by_regex("Core Capability Feature One", s7_f1)
    replace_by_regex("Detailed explanation of the first major feature of this service offering goes here.", s7_d1)
    replace_by_regex("Core Capability Feature Two", s7_f2)
    replace_by_regex("Detailed explanation of the second major feature of this service offering goes here.", s7_d2)
    
    # S08 Service Deep-Dive 2 edstellar-detailed-explanation-of-service-with-image-and-accordion.html
    replace_by_regex("Comprehensive Solution Overview", "Leadership Assessment Centers")
    replace_by_regex("This service module expands on the overarching proposition, diving into specific mechanical capabilities.", "Selecting the right leaders is the highest-stakes talent decision any organization makes. Edstellar's leadership assessment center consulting deploys structured, multi-method evaluation programs.")
    
    replace_by_regex("Feature Capability One", "Executive Assessment Centers")
    replace_by_regex("Description of the first accordion feature goes here detailing how it works.", "Full-day, high-fidelity assessment programs for senior leadership roles, including C-suite, VP, and director-level positions. Participants navigate a series of interconnected simulations.")
    
    replace_by_regex("Feature Capability Two", "Emerging Leader Assessment Programs")
    replace_by_regex("Description of the second accordion feature goes here detailing how it adds value.", "Half-day to full-day assessment programs designed for mid-level managers being considered for their first senior leadership role.")
    
    replace_by_regex("Feature Capability Three", "Promotion Readiness Evaluation")
    replace_by_regex("Description of the third accordion feature goes here detailing the outcome.", "Targeted assessment programs that evaluate internal candidates for specific leadership vacancies.")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("Injected S05 to S08 successfully.")

if __name__ == "__main__":
    inject()
