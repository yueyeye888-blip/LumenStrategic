# -*- coding: utf-8 -*-
import os
import re

# Edit i18n
with open("js/i18n.js", "r", encoding="utf-8") as f:
    i18n = f.read()

i18n = i18n.replace(
    '"hero-sub": { en: "STRATEGIC CAPITAL MANAGEMENT & ALTERNATIVE INVESTMENT SOLUTIONS", zh: "STRATEGIC CAPITAL MANAGEMENT & ALTERNATIVE INVESTMENT SOLUTIONS" }',
    '"hero-sub": { en: "STRATEGIC CAPITAL MANAGEMENT & ALTERNATIVE INVESTMENT SOLUTIONS", zh: "战略资本管理与另类投资解决方案" }'
)

new_card2_main = '''    "srv-card2-main-t": { en: "Public Market Strategies", zh: "二级市场投资" },
    "srv-card2-main-p": { en: "Structured around highly liquid public markets, building a multi-strategy framework integrating systematic and active approaches to capture cross-market, cross-cycle structural opportunities.", zh_html: "围绕高流动性公开市场，构建系统化与主动型相结合的多策略投资框架，在风险可控的前提下捕捉跨市场、跨周期的结构性机会。" },
'''
if '"srv-card2-main-t"' not in i18n:
    i18n = i18n.replace('"srv-card2-t":', new_card2_main + '    "srv-card2-t":')

with open("js/i18n.js", "w", encoding="utf-8") as f:
    f.write(i18n)

# Edit HTML
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update logo string
html = re.sub(
    r'<span style="font-size:20px.*?LUMEN<br><span[^>]*>STRATEGIC CAPITAL</span></span>',
    '<span style="font-size:22px; font-weight:800; color:#fff; letter-spacing:1px; font-family:\\\'Inter\\\',sans-serif; text-align:left; line-height:1.2; display:flex; gap:6px;">LUMEN <span style="color:#f9d976;">STRATEGIC</span></span>',
    html,
    flags=re.DOTALL
)

# 2. Update hero subtitle
html = re.sub(
    r'<span class="title-sub highlight-gold"[^>]*>.*?</span>',
    '<span class="title-sub highlight-gold" style="font-size: 24px; max-width:800px; line-height: 1.4;" data-i18n="hero-sub">STRATEGIC CAPITAL MANAGEMENT & ALTERNATIVE INVESTMENT SOLUTIONS</span>',
    html,
    count=1
)

# 3. Update Services Section layout
start_tag = '<div class="grid-3">'
end_tag = 'data-i18n="srv-note"></p>'

start_idx = html.find(start_tag)
end_idx = html.find(end_tag, start_idx) + len(end_tag)

if start_idx != -1 and end_idx != -1:
    new_cards_html = """<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px;">
                <!-- Card 1: Private Market Updates -->
                <div class="card" style="display: flex; flex-direction: column;">
                    <div class="card-icon">
                        <svg class="service-icon-svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="url(#grad-arb)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 5px;">
                            <defs><linearGradient id="grad-arb" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f9d976"/><stop offset="100%" stop-color="#e9b646"/></linearGradient></defs>
                            <circle cx="12" cy="12" r="9" stroke-dasharray="12 8" class="anim-spin-slow" stroke-width="1.2" stroke-opacity="0.4"/>
                            <path d="M7 10 L12 5 L17 10" stroke-width="2.5" class="anim-float-up"/>
                            <path d="M7 14 L12 19 L17 14" stroke-width="2.5" class="anim-float-down"/>
                        </svg>
                    </div>
                    <h3 class="card-title" data-i18n="srv-card1-t" style="color: #f9d976;">Private Market Investments</h3>
                    <p class="card-text" data-i18n="srv-card1-p" style="flex-grow: 1; text-align: left;"></p>
                </div>
                
                <!-- Card 2: Public Market Strategies (Nested) -->
                <div class="card" style="display: flex; flex-direction: column; background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(249, 217, 118, 0.4);">
                    <div class="card-icon">
                        <svg class="service-icon-svg" width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="url(#grad-hf)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 5px;">
                            <defs><linearGradient id="grad-hf" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f9d976"/><stop offset="100%" stop-color="#e9b646"/></linearGradient></defs>
                            <rect x="4" y="14" width="4" height="6" class="anim-bar-1" fill="url(#grad-hf)" fill-opacity="0.2"/>
                            <rect x="10" y="6" width="4" height="14" class="anim-bar-2" fill="url(#grad-hf)" fill-opacity="0.2"/>
                            <rect x="16" y="10" width="4" height="10" class="anim-bar-3" fill="url(#grad-hf)" fill-opacity="0.2"/>
                        </svg>
                    </div>
                    <h3 class="card-title" data-i18n="srv-card2-main-t" style="color: #f9d976;">Public Market Strategies</h3>
                    <p class="card-text" data-i18n="srv-card2-main-p" style="text-align: left;"></p>
                    
                    <div style="display: grid; grid-template-columns: 1fr; gap: 15px; margin-top: 25px;">
                        <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; transition: transform 0.2s;" onmouseover="this.style.borderColor='rgba(249,217,118,0.4)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                            <h4 style="color: #fff; font-size: 16px; margin: 0 0 10px 0; font-weight: 600; text-align: left;" data-i18n="srv-card2-t">Systematic Quantitative Strategies</h4>
                            <p style="color: #94a3b8; font-size: 14px; margin: 0; line-height: 1.6; text-align: left;" data-i18n="srv-card2-p"></p>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; transition: transform 0.2s;" onmouseover="this.style.borderColor='rgba(249,217,118,0.4)'" onmouseout="this.style.borderColor='rgba(255,255,255,0.08)'">
                            <h4 style="color: #fff; font-size: 16px; margin: 0 0 10px 0; font-weight: 600; text-align: left;" data-i18n="srv-card3-t">Active Trading Strategies</h4>
                            <p style="color: #94a3b8; font-size: 14px; margin: 0; line-height: 1.6; text-align: left;" data-i18n="srv-card3-p"></p>
                        </div>
                    </div>
                </div>
            </div>
            <p style="text-align:center; color:#64748b; font-size:13px; margin-top:50px; padding:0 20px;" data-i18n="srv-note"></p>"""
    
    html = html[:start_idx] + new_cards_html + html[end_idx:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
