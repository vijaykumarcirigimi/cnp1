import os
import re
from bs4 import BeautifulSoup

INPUT_FILE = r"c:\Users\Vijay\OneDrive\Documents\CNP\assessment-development-centers.html"
OUTPUT_FILE = r"c:\Users\Vijay\OneDrive\Documents\CNP\assessment-development-centers.html"

def inject():
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # S01 (Hero) was partially replaced in build_page.py, but let's make sure
    # It has breadcrumb changes, we skip to S02

    # S02: Definitional Intro
    lbl = soup.find(string=re.compile("Understanding the Topic"))
    if lbl: lbl.replace_with("Understanding the Discipline")
    h2 = soup.find(string=re.compile("What Is \[Service Name\] Consulting\?"))
    if h2: h2.replace_with("What Are Assessment and Development Centers?")
    
    lead = soup.select_one('.wio-lead')
    if lead:
        lead.clear()
        lead.append(BeautifulSoup("Assessment and development centers are structured, multi-method evaluation processes that use realistic job simulations, behavioral exercises, psychometric assessments, and trained assessor observation to objectively measure an individual's competencies, leadership potential, and readiness for current or future roles. An <strong>assessment center</strong> is a selection-focused process that evaluates candidates against validated competency models to inform hiring, promotion, and succession decisions. Participants engage in exercises that mirror real workplace challenges, including in-basket prioritization tasks, leaderless group discussions, role-play scenarios, fact-finding exercises, case study analyses, and structured presentations, while certified assessors score observed behaviors against predetermined behavioral anchors.", "html.parser"))
        
    p2_list = soup.select('.wio-body p')
    if len(p2_list) > 1:
        p2_list[1].clear()
        p2_list[1].append(BeautifulSoup("A <strong>development center</strong> shifts the focus from selection to growth, using the same simulation-based methodology but with the primary goal of generating rich developmental feedback, identifying competency gaps, and producing individualized development plans that accelerate leadership readiness. Together, assessment and development centers create a closed-loop talent system where objective evaluation informs targeted development, and development outcomes are validated through subsequent assessment.", "html.parser"))

    # S03: Challenges (Challenges image list)
    s_lbl = soup.find(string=re.compile("What we solve"))
    if s_lbl: s_lbl.replace_with("The Problem: Why Traditional Talent Decisions Fail")
    
    chal_h2 = soup.select_one('.section-inner > h2')
    if chal_h2:
        chal_h2.clear()
        chal_h2.append(BeautifulSoup("<span class='accent'>The Challenge:</span> <span class='dark'>Why Organisations Make the Wrong Talent Bets</span>", "html.parser"))
        
    chal_sub = soup.select_one('.section-inner > .sub')
    if chal_sub:
        chal_sub.clear()
        chal_sub.append("Most enterprises invest heavily in leadership pipelines yet continue to make talent decisions based on gut instinct, past performance in unrelated roles, and subjective manager opinions.")
        
    chal_num = soup.select_one('.img-stat .num')
    if chal_num: chal_num.string = "60%"
    chal_label = soup.select_one('.img-stat .label')
    if chal_label: chal_label.string = "of new managers fail within the first 24 months of promotion"
    
    pain_items = soup.select('.pain-item')
    pain_texts = [
        ("Gut-Feel Promotion Decisions", "Promotion decisions are made based on tenure, personal relationships, or performance in the current role rather than objective evaluation of readiness for the next role.", "60% of new managers fail within the first 24 months"),
        ("Hidden High-Potential Talent Goes Unrecognized", "Without structured high-potential identification processes, organizations default to visibility bias. Employees who are vocal, politically savvy, or based at headquarters get recognized.", "Only 1 in 7 high-potential employees is correctly identified"),
        ("No Objective Baseline for Development Investment", "Organizations spend millions on leadership development programs without first assessing where each leader actually stands. Development becomes a one-size-fits-all curriculum.", "Companies waste an estimated 40% of leadership development spend"),
        ("Succession Plans Built on Assumptions, Not Evidence", "Succession plans list names without validated readiness data. When a critical role opens unexpectedly, the organization discovers its successors lack competencies.", "65% of companies report their succession plans are ineffective"),
        ("Inconsistent Assessment Standards Across Business Units", "Different hiring managers, different business units, and different geographies apply different standards when evaluating talent.", "3x more inconsistency in talent ratings without standardization"),
        ("Bias Undermines Diversity in Leadership Pipelines", "Unstructured talent decisions amplify unconscious bias. Gender, ethnicity, communication style, and educational background disproportionately influence subjective evaluations.", "Structured assessments reduce adverse impact by up to 50%")
    ]
    for i, p in enumerate(pain_items):
        if i < len(pain_texts):
            h4 = p.select_one('h4')
            if h4: h4.string = pain_texts[i][0]
            txt = p.select_one('p')
            if txt: txt.string = pain_texts[i][1]
            tag = p.select_one('.pain-tag')
            if tag:
                # Keep the dot
                tag.clear()
                tag.append(BeautifulSoup("<span class='dot'></span> " + pain_texts[i][2], "html.parser"))

    chal_cta = soup.select_one('.bottom-cta p')
    if chal_cta:
        chal_cta.clear()
        chal_cta.append(BeautifulSoup("Stop guessing who your next leaders are. <strong>Start assessing with science.</strong>", "html.parser"))

    # S04: Stats Card Grid
    stat_nums = soup.select('.stat-card .stat-number')
    stat_lbls = soup.select('.stat-card .stat-label')
    nt = [("$10.7", "B"), ("0.51", ""), ("54", "%"), ("78", "%")]
    lt = ["Global talent assessment services market in 2026", "Predictive validity coefficient for assessment centers", "ROI achieved from objective assessment tools", "of HR professionals report that structured assessments have improved quality of hires"]
    for i in range(len(stat_nums)):
        if i < len(nt):
            stat_nums[i].clear()
            stat_nums[i].append(BeautifulSoup(nt[i][0] + f"<span class='symbol'>{nt[i][1]}</span>", "html.parser"))
            stat_lbls[i].string = lt[i]

    # S05: Three Pillars
    p_h2 = soup.find(string=re.compile("What We Do"))
    if p_h2: p_h2.replace_with("Design. Deploy. Develop. The Three Pillars of Assessment Excellence.")
    pillars = soup.select('.pillar-card') # wait, I don't know the class, we will find by looking at headers in the HTML
    h3_tags = soup.find_all(lambda tag: tag.name == 'h3' and "Pillar" not in tag.text and tag.parent.name == 'div')
    
    # We will write out the modified HTML and save it
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print("Injected S02, S03, S04 successfully.")

if __name__ == "__main__":
    inject()
