import re

with open('/Users/xingxiu/Desktop/Fluxium网站/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the whole nav-links block to include the layout container and language toggle.
new_nav = """        <div style="display: flex; align-items: center; gap: 30px;">
            <ul class="nav-links">
                <li><a href="#about" data-i18n="nav-about">About</a></li>
                <li><a href="#services" data-i18n="nav-services">Services</a></li>
                <li><a href="#criteria" data-i18n="nav-criteria">Criteria</a></li>
                <li><a href="#contact" data-i18n="nav-contact">Contact</a></li>
            </ul>
            <div id="langToggle" style="cursor:pointer; padding: 6px 14px; border: 1px solid rgba(249, 217, 118, 0.3); border-radius: 20px; color: #f9d976; font-size: 13px; font-weight: 500; display:flex; gap:6px; align-items:center; transition: all 0.3s; user-select: none; background: rgba(0,0,0,0.3);" onclick="toggleLanguage()">
                <span id="lang-en-btn" style="color:#fff; font-weight:700;">EN</span> 
                <span style="opacity:0.3; margin:0 2px;">|</span> 
                <span id="lang-zh-btn" style="color:rgba(255,255,255,0.5);">中</span>
            </div>
        </div>"""
html = re.sub(r'<ul class="nav-links">.*?</ul>', new_nav, html, flags=re.DOTALL)

# 2. Inject data-i18n attributes
replacements = [
    (r'<span class="title-main"(.*?)>Fluxium</span>', r'<span class="title-main"\1 data-i18n="hero-title">Fluxium</span>'),
    (r'<span class="title-sub highlight-gold"(.*?)>Market Making &amp; Liquidity Solutions</span>', r'<span class="title-sub highlight-gold"\1 data-i18n="hero-sub">Market Making &amp; Liquidity Solutions</span>'),
    (r'We provide institutional-grade liquidity for digital asset markets through quantitative trading and advanced market infrastructure.', r'<span data-i18n="hero-desc">We provide institutional-grade liquidity for digital asset markets through quantitative trading and advanced market infrastructure.</span>'),
    (r'Partner With Us', r'<span data-i18n="hero-btn">Partner With Us</span>'),
    
    (r'<h2 class="section-title">Why Fluxium</h2>', r'<h2 class="section-title" data-i18n="about-title">Why Fluxium</h2>'),
    (r'<div class="section-subtitle">Professional Market Making Infrastructure</div>', r'<div class="section-subtitle" data-i18n="about-sub">Professional Market Making Infrastructure</div>'),
    (r'Fluxium Capital operates from the Cayman Islands with strategic partnerships across Singapore and Asia-Pacific. Our team is composed of seasoned professionals from top-tier A-share securities firms, public fund managers, and global hedge funds.', r'<span data-i18n="about-p1">Fluxium Capital operates from the Cayman Islands with strategic partnerships across Singapore and Asia-Pacific. Our team is composed of seasoned professionals from top-tier A-share securities firms, public fund managers, and global hedge funds.</span>'),
    (r'We specialize in delivering execution-oriented liquidity solutions through proprietary capital and battle-tested quantitative trading infrastructure.', r'<span data-i18n="about-p2">We specialize in delivering execution-oriented liquidity solutions through proprietary capital and battle-tested quantitative trading infrastructure.</span>'),
    
    (r'<div class="stat-label">Market Participants</div>', r'<div class="stat-label" data-i18n="stat-lbl-1">Market Participants</div>'),
    (r'<div class="stat-label">Trading Operations</div>', r'<div class="stat-label" data-i18n="stat-lbl-2">Trading Operations</div>'),
    (r'<div class="stat-label">Daily Liquidity</div>', r'<div class="stat-label" data-i18n="stat-lbl-3">Daily Liquidity</div>'),

    (r'<h2 class="section-title">Core Services</h2>', r'<h2 class="section-title" data-i18n="srv-title">Core Services</h2>'),
    (r'<div class="section-subtitle">Your All-In-One Market Making Engine</div>', r'<div class="section-subtitle" data-i18n="srv-sub">Your All-In-One Market Making Engine</div>'),
    
    (r'<h3 class="card-title">Spot &amp; Derivatives Arbitrage</h3>', r'<h3 class="card-title" data-i18n="srv-card1-t">Spot &amp; Derivatives Arbitrage</h3>'),
    (r'Optimize market structure and promote healthy price discovery across exchange protocols.', r'<span data-i18n="srv-card1-p">Optimize market structure and promote healthy price discovery across exchange protocols.</span>'),
    
    (r'<h3 class="card-title">High-Frequency Two-Sided Quoting</h3>', r'<h3 class="card-title" data-i18n="srv-card2-t">High-Frequency Two-Sided Quoting</h3>'),
    (r'Build resilient liquidity walls capable of absorbing large orders and market shocks.', r'<span data-i18n="srv-card2-p">Build resilient liquidity walls capable of absorbing large orders and market shocks.</span>'),
    
    (r'<h3 class="card-title">Perpetual Futures &amp; Volatility Trading</h3>', r'<h3 class="card-title" data-i18n="srv-card3-t">Perpetual Futures &amp; Volatility Trading</h3>'),
    (r'Maintain healthy funding rate environments while capturing structured volatility premium.', r'<span data-i18n="srv-card3-p">Maintain healthy funding rate environments while capturing structured volatility premium.</span>'),

    (r'<h2 class="section-title">Partnership Criteria</h2>', r'<h2 class="section-title" data-i18n="crit-title">Partnership Criteria</h2>'),
    (r'<div class="section-subtitle">What We Look For</div>', r'<div class="section-subtitle" data-i18n="crit-sub">What We Look For</div>'),
    
    (r'<div class="criteria-label">Exchange Perpetual/Futures</div>', r'<div class="criteria-label" data-i18n="crit-lbl-1">Exchange Perpetual/Futures</div>'),
    (r'<p>Binance spot and perpetual/futures resources.</p>', r'<p data-i18n="crit-p-1">Binance spot and perpetual/futures resources.</p>'),
    
    (r'<div class="criteria-label">Market Making</div>', r'<div class="criteria-label" data-i18n="crit-lbl-2">Market Making</div>'),
    (r'<p>Projects needing professional liquidity support.</p>', r'<p data-i18n="crit-p-2">Projects needing professional liquidity support.</p>'),
    
    (r'<div class="criteria-label">Listing Preparation</div>', r'<div class="criteria-label" data-i18n="crit-lbl-3">Listing Preparation</div>'),
    (r'<p>Projects preparing for exchange listing.</p>', r'<p data-i18n="crit-p-3">Projects preparing for exchange listing.</p>'),
    
    (r'<div class="criteria-label">Capital &amp; Track Record</div>', r'<div class="criteria-label" data-i18n="crit-lbl-4">Capital &amp; Track Record</div>'),
    (r'<p>\$10M – \$30M USDT per project from our Singapore partner.<br>Experienced in active market operations on Binance \(case studies available under NDA\).</p>', r'<p data-i18n="crit-lbl-4">$10M – $30M USDT per project from our Singapore partner.<br>Experienced in active market operations on Binance (case studies available under NDA).</p>'),

    (r'<h2 class="section-title">Get In Touch</h2>', r'<h2 class="section-title" data-i18n="cnt-title">Get In Touch</h2>'),
    (r'We invite qualified project leaders to Singapore for confidential consultation.', r'<span data-i18n="cnt-sub">We invite qualified project leaders to Singapore for confidential consultation.</span>'),
    
    (r'<label>Project Name &amp; Website \*</label>', r'<label data-i18n="frm-l1">Project Name &amp; Website *</label>'),
    (r'<label>Contact Email \*</label>', r'<label data-i18n="frm-l2">Contact Email *</label>'),
    (r'<label>Project Brief / Deck Link \*</label>', r'<label data-i18n="frm-l3">Project Brief / Deck Link *</label>'),
    (r'<label>Listing Status &amp; Timeline \*</label>', r'<label data-i18n="frm-l4">Listing Status &amp; Timeline *</label>'),
    (r'<label>Circulating Supply &amp; Token Structure \*</label>', r'<label data-i18n="frm-l5">Circulating Supply &amp; Token Structure *</label>'),
    (r'<label>Target Markets &amp; Key KPIs \*</label>', r'<label data-i18n="frm-l6">Target Markets &amp; Key KPIs *</label>'),
    (r'Submit Application', r'<span data-i18n="frm-btn">Submit Application</span>'),
    (r'We\'ll respond within 24-48 business hours.', r'<span data-i18n="frm-note">We\'ll respond within 24-48 business hours.</span>'),
    
    (r'Registered in Cayman Islands', r'<span data-i18n="ft-1">Registered in Cayman Islands</span>'),
    (r'<strong>Regional Base:</strong> Singapore', r'<span data-i18n="ft-2"><strong>Regional Base:</strong> Singapore</span>'),
    (r'<h4 style="color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600;">Contact</h4>', r'<h4 style="color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600;" data-i18n="ft-3">Contact</h4>'),
    (r'Disclaimer: This website is for informational purposes only. Nothing herein constitutes an offer to sell or buy any product or service.', r'<span data-i18n="ft-4">Disclaimer: This website is for informational purposes only. Nothing herein constitutes an offer to sell or buy any product or service.</span>')
]

for pat, repl in replacements:
    html = re.sub(pat, repl, html)

# Inject i18n.js before closing body
if '<script src="js/i18n.js">' not in html:
    html = html.replace('</body>', '    <script src="js/i18n.js"></script>\n</body>')

with open('/Users/xingxiu/Desktop/Fluxium网站/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("INJECTION SUCCESS")
