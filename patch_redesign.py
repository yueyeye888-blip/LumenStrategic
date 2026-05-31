# -*- coding: utf-8 -*-
import re

# 1. 删除 i18n 中的 AI / Computing Infrastructure / New Finance
with open("js/i18n.js", "r", encoding="utf-8") as f:
    i18n = f.read()

i18n = i18n.replace("<br><br><span style='color:#f9d976; font-size:14px; font-weight:600;'>AI / Computing Infrastructure / New Finance</span>", "")

with open("js/i18n.js", "w", encoding="utf-8") as f:
    f.write(i18n)

# 2. 重新设计核心业务板块的布局
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

start_tag = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 30px;">'
end_tag = 'data-i18n="srv-note"></p>'

start_idx = html.find(start_tag)
end_idx = html.find(end_tag, start_idx) + len(end_tag)

new_layout = """<div style="display: flex; flex-wrap: wrap; gap: 30px; justify-content: center; align-items: stretch; max-width: 1200px; margin: 0 auto;">
                
                <!-- Card 1: Private Market Updates -->
                <div style="flex: 1; min-width: 340px; display: flex; flex-direction: column; background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(255,255,255,0.06); border-radius: 20px; padding: 40px; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.3);" onmouseover="this.style.borderColor='rgba(249, 217, 118, 0.4)'; this.style.transform='translateY(-6px)'; this.style.boxShadow='0 20px 40px rgba(0,0,0,0.5)';" onmouseout="this.style.borderColor='rgba(255,255,255,0.06)'; this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 30px rgba(0,0,0,0.3)';">
                    
                    <!-- Decorative Light -->
                    <div style="position: absolute; top: -50px; right: -50px; width: 180px; height: 180px; background: radial-gradient(circle, rgba(249, 217, 118, 0.1) 0%, rgba(0,0,0,0) 70%); border-radius: 50%; pointer-events: none;"></div>
                    
                    <div style="background: rgba(0,0,0,0.4); width: 70px; height: 70px; border-radius: 18px; display: flex; align-items: center; justify-content: center; margin-bottom: 30px; border: 1px solid rgba(249, 217, 118, 0.15); box-shadow: inset 0 0 20px rgba(249,217,118,0.05);">
                        <svg class="service-icon-svg" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="url(#grad-arb)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                            <defs><linearGradient id="grad-arb" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f9d976"/><stop offset="100%" stop-color="#e9b646"/></linearGradient></defs>
                            <circle cx="12" cy="12" r="9" stroke-dasharray="12 8" class="anim-spin-slow" stroke-width="1.2" stroke-opacity="0.4"/>
                            <path d="M7 10 L12 5 L17 10" stroke-width="2.5" class="anim-float-up"/>
                            <path d="M7 14 L12 19 L17 14" stroke-width="2.5" class="anim-float-down"/>
                        </svg>
                    </div>
                    
                    <h3 data-i18n="srv-card1-t" style="color: #f9d976; font-size: 24px; margin-bottom: 20px; font-weight: 700; letter-spacing: 0.5px; text-align: left;">Private Market Investments</h3>
                    <p data-i18n="srv-card1-p" style="color: #cbd5e1; flex-grow: 1; text-align: left; font-size: 15px; line-height: 1.8; margin: 0;"></p>
                </div>
                
                <!-- Card 2: Public Market Strategies (Nested) -->
                <div style="flex: 1.4; min-width: 400px; display: flex; flex-direction: column; background: linear-gradient(145deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(255,255,255,0.06); border-radius: 20px; padding: 40px; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); position: relative; overflow: hidden; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.3);" onmouseover="this.style.borderColor='rgba(249, 217, 118, 0.4)'; this.style.transform='translateY(-6px)'; this.style.boxShadow='0 20px 40px rgba(0,0,0,0.5)';" onmouseout="this.style.borderColor='rgba(255,255,255,0.06)'; this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 30px rgba(0,0,0,0.3)';">
                    
                    <div style="position: absolute; top: -50px; left: -50px; width: 250px; height: 250px; background: radial-gradient(circle, rgba(249, 217, 118, 0.08) 0%, rgba(0,0,0,0) 70%); border-radius: 50%; pointer-events: none;"></div>
                    
                    <div style="display: flex; align-items: flex-start; gap: 25px; margin-bottom: 35px; position: relative; z-index: 1;">
                        <div style="background: rgba(0,0,0,0.4); width: 70px; height: 70px; min-width: 70px; border-radius: 18px; display: flex; align-items: center; justify-content: center; margin-bottom: 0; border: 1px solid rgba(249, 217, 118, 0.15); box-shadow: inset 0 0 20px rgba(249,217,118,0.05);">
                            <svg class="service-icon-svg" width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="url(#grad-hf)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <defs><linearGradient id="grad-hf" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#f9d976"/><stop offset="100%" stop-color="#e9b646"/></linearGradient></defs>
                                <rect x="4" y="14" width="4" height="6" class="anim-bar-1" fill="url(#grad-hf)" fill-opacity="0.2"/>
                                <rect x="10" y="6" width="4" height="14" class="anim-bar-2" fill="url(#grad-hf)" fill-opacity="0.2"/>
                                <rect x="16" y="10" width="4" height="10" class="anim-bar-3" fill="url(#grad-hf)" fill-opacity="0.2"/>
                            </svg>
                        </div>
                        <div>
                            <h3 data-i18n="srv-card2-main-t" style="color: #f9d976; font-size: 24px; margin-top: 5px; margin-bottom: 12px; font-weight: 700; letter-spacing: 0.5px; text-align: left;">Public Market Strategies</h3>
                            <p data-i18n="srv-card2-main-p" style="color: #94a3b8; text-align: left; font-size: 15px; line-height: 1.7; margin: 0;"></p>
                        </div>
                    </div>
                    
                    <!-- Sub cards -->
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-top: auto; position: relative; z-index: 1;">
                        
                        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; transition: all 0.3s; position: relative; overflow: hidden;" onmouseover="this.style.background='rgba(30, 41, 59, 0.8)'; this.style.borderColor='rgba(249,217,118,0.3)';" onmouseout="this.style.background='rgba(15, 23, 42, 0.6)'; this.style.borderColor='rgba(255,255,255,0.05)';">
                            <div style="width: 4px; height: 100%; background: linear-gradient(180deg, #f9d976 0%, transparent 100%); position: absolute; left: 0; top: 0; opacity: 0.7;"></div>
                            <h4 style="color: #fff; font-size: 17px; margin: 0 0 12px 10px; font-weight: 600; text-align: left;" data-i18n="srv-card2-t"></h4>
                            <p style="color: #cbd5e1; font-size: 14px; margin: 0 0 0 10px; line-height: 1.7; text-align: left;" data-i18n="srv-card2-p"></p>
                        </div>
                        
                        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; transition: all 0.3s; position: relative; overflow: hidden;" onmouseover="this.style.background='rgba(30, 41, 59, 0.8)'; this.style.borderColor='rgba(249,217,118,0.3)';" onmouseout="this.style.background='rgba(15, 23, 42, 0.6)'; this.style.borderColor='rgba(255,255,255,0.05)';">
                            <div style="width: 4px; height: 100%; background: linear-gradient(180deg, #e9b646 0%, transparent 100%); position: absolute; left: 0; top: 0; opacity: 0.7;"></div>
                            <h4 style="color: #fff; font-size: 17px; margin: 0 0 12px 10px; font-weight: 600; text-align: left;" data-i18n="srv-card3-t"></h4>
                            <p style="color: #cbd5e1; font-size: 14px; margin: 0 0 0 10px; line-height: 1.7; text-align: left;" data-i18n="srv-card3-p"></p>
                        </div>
                        
                    </div>
                </div>
            </div>
            <p style="text-align:center; color:#64748b; font-size:13px; margin-top:50px; padding:0 20px;" data-i18n="srv-note"></p>"""

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_layout + html[end_idx:]
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
