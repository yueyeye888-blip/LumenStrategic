import os

css_content = """body, html {
  margin: 0; padding: 0; width: 100%; height: 100%;
  background: #020408; color: #ffffff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  overflow-x: hidden;
}
* { box-sizing: border-box; }

#world-canvas {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  z-index: 0; pointer-events: none;
  background: radial-gradient(circle at 50% 50%, #040812 0%, #000000 100%);
}

.navbar {
  position: fixed; top: 0; width: 100%; height: 100px;
  display: flex; justify-content: space-between; align-items: center;
  padding: 0 5%; z-index: 100;
  background: rgba(4, 8, 18, 0.5); backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.logo {
  font-size: 32px; font-weight: 800; color: #fff; text-decoration: none;
  letter-spacing: 1px; display: flex; align-items: center; gap: 10px;
}
.logo-icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #f9d976 0%, #e9b646 100%);
  border-radius: 8px; display: flex; align-items: center; justify-content: center;
  color: #000; font-size: 24px; font-weight: 900;
}

.nav-links { display: flex; gap: 30px; list-style: none; margin: 0; padding: 0;}
.nav-links a {
  color: #fff; text-decoration: none; font-size: 15px; font-weight: 500;
  letter-spacing: 1px; transition: color 0.3s ease; text-transform: uppercase;
}
.nav-links a:hover { color: #cf9e51; text-shadow: 0 0 15px rgba(212, 175, 55, 0.6); }

.hero {
  position: relative; z-index: 10; height: 100vh;
  display: flex; flex-direction: column; justify-content: center;
  align-items: center; text-align: center;
}
.title-main {
  font-size: 96px; font-weight: 800; letter-spacing: -2px; margin-bottom: 10px;
  color: #ffffff; text-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), 0 0 20px rgba(255,255,255,0.1);
}
.title-sub {
  font-size: 28px; font-weight: 500; letter-spacing: 3px;
  text-transform: uppercase; margin-top: 10px;
}
.highlight-gold {
  background: linear-gradient(135deg, #f9d976 0%, #e9b646 50%, #f9d976 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 15px rgba(212, 175, 55, 0.3));
}

.content-section {
  padding: 120px 20px; position: relative; z-index: 10;
  background: rgba(4, 8, 18, 0.6); backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px); border-top: 1px solid rgba(255, 255, 255, 0.03);
}
.dark-bg { background: rgba(2, 4, 10, 0.85); }
.container { max-width: 1200px; margin: 0 auto; }
.text-center { text-align: center; }

.section-title { font-size: 52px; font-weight: 800; margin-bottom: 15px; text-align: center; letter-spacing: -1px; }
.section-subtitle {
  text-align: center; color: #cf9e51; font-size: 18px; margin-bottom: 70px;
  letter-spacing: 1px; text-transform: uppercase; font-weight: 600;
}

.grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 30px; }
.card {
  background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px; padding: 50px 40px; transition: all 0.4s ease; text-align: center;
}
.card:hover {
  background: rgba(212, 175, 55, 0.05); border-color: rgba(212, 175, 55, 0.4);
  transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}
.card-icon { font-size: 42px; margin-bottom: 25px; }
.card-title { font-size: 24px; color: #ffffff; margin-bottom: 20px; font-weight: 700; }
.card-text { color: #94a3b8; line-height: 1.8; font-size: 16px; }

/* Stats box for About */
.about-stats { display: flex; justify-content: center; gap: 40px; margin-top: 50px; flex-wrap: wrap; }
.stat-box { 
  background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); 
  padding: 30px; border-radius: 16px; min-width: 200px; text-align: center;
}
.stat-number { font-size: 42px; font-weight: 800; color: #cf9e51; margin-bottom: 10px; }
.stat-label { color: #94a3b8; font-size: 16px; text-transform: uppercase; letter-spacing: 1px; }

/* Enhanced Criteria List */
.criteria-content {
  background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.05);
  border-radius: 20px; padding: 50px; box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}
.criteria-item {
  display: flex; align-items: flex-start; margin-bottom: 30px;
  padding-bottom: 30px; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.criteria-item:last-child { margin-bottom: 0; padding-bottom: 0; border-bottom: none; }
.criteria-number { 
  font-size: 32px; font-weight: 800; color: #cf9e51; opacity: 0.5;
  margin-right: 30px; min-width: 50px;
}
.criteria-label { font-size: 22px; color: #fff; font-weight: 600; margin-bottom: 8px; }
.criteria-text p { color: #94a3b8; margin: 0; font-size: 16px; line-height: 1.6; }

/* Form Styles */
.form-container {
  max-width: 800px; margin: 0 auto; background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 50px;
}
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.form-group { margin-bottom: 20px; text-align: left; }
.form-group label { display: block; margin-bottom: 8px; color: #e2e8f0; font-size: 14px; font-weight: 500; }
.form-group input, .form-group textarea {
  width: 100%; padding: 15px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px; color: #fff; font-size: 16px; font-family: 'Inter', sans-serif;
  transition: border-color 0.3s, box-shadow 0.3s;
}
.form-group input:focus, .form-group textarea:focus {
  outline: none; border-color: #cf9e51; box-shadow: 0 0 10px rgba(212,175,55,0.2);
}
.submit-btn {
  width: 100%; padding: 18px; 
  background: linear-gradient(135deg, #f9d976 0%, #e9b646 100%);
  border: none; border-radius: 8px; color: #020408; font-size: 18px; font-weight: 700;
  cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
}
.submit-btn:hover {
  transform: translateY(-2px); box-shadow: 0 10px 20px rgba(212,175,55,0.3);
}
.form-note { text-align: center; color: #64748b; font-size: 14px; margin-top: 15px; }

/* Footer */
footer {
  background: #020408; padding: 60px 40px 40px; 
  border-top: 1px solid rgba(255, 255, 255, 0.05); position: relative; z-index: 10;
}
.footer-content {
  display: flex; justify-content: space-between; max-width: 1200px; margin: 0 auto 40px;
  flex-wrap: wrap; gap: 40px;
}
.footer-col h4 { color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600; }
.footer-col p, .footer-col a { color: #64748b; margin: 5px 0; font-size: 15px; text-decoration: none; }
.footer-col a:hover { color: #cf9e51; }
.footer-bottom {
  text-align: center; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05);
  color: #475569; font-size: 14px;
}

@media (max-width: 768px) {
  .title-main { font-size: 64px; }
  .form-row { grid-template-columns: 1fr; }
  .footer-content { flex-direction: column; }
}
"""

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fluxium - Market Making & Liquidity Solutions</title>
    <link rel="stylesheet" href="css/main.css?v=28">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    
    <canvas id="world-canvas"></canvas>

    <nav class="navbar">
        <a href="#" class="logo" style="text-decoration: none; display: flex; align-items: center; gap: 10px;">
            <div class="logo-icon" style="width: 40px; height: 40px; background: linear-gradient(135deg, #f9d976 0%, #e9b646 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #000; font-size: 24px; font-weight: 900;">F</div>
            <span style="font-size: 32px; font-weight: 800; color: #fff; letter-spacing: 1px;">Fluxium</span>
        </a>
        <ul class="nav-links">
            <li><a href="#about">About</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#criteria">Criteria</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>

    <main class="hero">
        <span class="title-main">Fluxium</span>
        <span class="title-sub highlight-gold">Market Making & Liquidity Solutions</span>
    </main>

    <section id="about" class="content-section">
        <div class="container">
            <h2 class="section-title">Why Fluxium</h2>
            <div class="section-subtitle">Professional Market Making Infrastructure</div>
            <div style="max-width: 800px; margin: 0 auto; text-align: center; color: #94a3b8; font-size: 18px; line-height: 1.8;">
                <p style="margin-bottom: 20px;">Fluxium Capital operates from the Cayman Islands with strategic partnerships across Singapore and Asia-Pacific. Our team is composed of seasoned professionals from top-tier A-share securities firms, public fund managers, and global hedge funds.</p>
                <p>We specialize in delivering execution-oriented liquidity solutions through proprietary capital and battle-tested quantitative trading infrastructure.</p>
            </div>
            
            <div class="about-stats">
              <div class="stat-box">
                <div class="stat-number">Tier-1</div>
                <div class="stat-label">Market Participants</div>
              </div>
              <div class="stat-box">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Trading Operations</div>
              </div>
              <div class="stat-box">
                <div class="stat-number">$100M+</div>
                <div class="stat-label">Daily Liquidity</div>
              </div>
            </div>
        </div>
    </section>

    <section id="services" class="content-section dark-bg">
        <div class="container">
            <h2 class="section-title">Core Services</h2>
            <div class="section-subtitle">Your All-In-One Market Making Engine</div>
            
            <div class="grid-3">
                <div class="card">
                    <div class="card-icon">⚡</div>
                    <h3 class="card-title">Spot & Derivatives Arbitrage</h3>
                    <p class="card-text">Optimize market structure and promote healthy price discovery across exchange protocols.</p>
                </div>
                
                <div class="card">
                    <div class="card-icon">📊</div>
                    <h3 class="card-title">High-Frequency Two-Sided Quoting</h3>
                    <p class="card-text">Build resilient liquidity walls capable of absorbing large orders and market shocks.</p>
                </div>
                
                <div class="card">
                    <div class="card-icon">📈</div>
                    <h3 class="card-title">Perpetual Futures & Volatility Trading</h3>
                    <p class="card-text">Maintain healthy funding rate environments while capturing structured volatility premium.</p>
                </div>
            </div>
        </div>
    </section>

    <section id="criteria" class="content-section">
        <div class="container">
            <h2 class="section-title">Partnership Criteria</h2>
            <div class="section-subtitle">What We Look For</div>
            
            <div class="criteria-content" style="max-width: 900px; margin: 0 auto;">
                <div class="criteria-item">
                    <div class="criteria-number">01</div>
                    <div class="criteria-text">
                        <div class="criteria-label">Listing Status</div>
                        <p>Currently listed on Binance (both spot and perpetual futures)</p>
                    </div>
                </div>
                <div class="criteria-item">
                    <div class="criteria-number">02</div>
                    <div class="criteria-text">
                        <div class="criteria-label">Token Structure</div>
                        <p>Holder concentration >90%</p>
                    </div>
                </div>
                <div class="criteria-item">
                    <div class="criteria-number">03</div>
                    <div class="criteria-text">
                        <div class="criteria-label">Capital Allocation</div>
                        <p>$10M - $30M USDT dedicated per project from our Singapore partner</p>
                    </div>
                </div>
                <div class="criteria-item">
                    <div class="criteria-number">04</div>
                    <div class="criteria-text">
                        <div class="criteria-label">Track Record</div>
                        <p>Recognized leader in active market operations on Binance. Detailed case studies available under NDA.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="contact" class="content-section dark-bg">
        <div class="container text-center">
            <h2 class="section-title">Get In Touch</h2>
            <div class="section-subtitle" style="margin-bottom: 40px;">We invite qualified project leaders to Singapore for confidential consultation.</div>
            
            <div class="form-container">
                <form class="contact-form" id="contact-form" onsubmit="event.preventDefault(); alert('Application submitted successfully!');">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Project Name & Website *</label>
                            <input type="text" name="project_name" required>
                        </div>
                        <div class="form-group">
                            <label>Contact Email *</label>
                            <input type="email" name="contact_email" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Project Brief / Deck Link *</label>
                        <input type="text" name="project_brief" required>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label>Listing Status & Timeline *</label>
                            <input type="text" name="listing_status" placeholder="Spot/Perpetual details" required>
                        </div>
                        <div class="form-group">
                            <label>Circulating Supply & Token Structure *</label>
                            <input type="text" name="token_structure" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label>Target Markets & Key KPIs *</label>
                        <textarea name="target_markets" rows="4" required></textarea>
                    </div>
                    
                    <button type="submit" class="submit-btn" style="width: 100%; padding: 18px; background: linear-gradient(135deg, #f9d976 0%, #e9b646 100%); border: none; border-radius: 8px; color: #020408; font-size: 18px; font-weight: 700; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; margin-top: 10px;">Submit Application</button>
                    <p class="form-note" style="text-align: center; color: #64748b; font-size: 14px; margin-top: 15px;">We'll respond within 24-48 business hours.</p>
                </form>
            </div>
        </div>
    </section>

    <footer>
        <div class="footer-content" style="display: flex; justify-content: space-between; max-width: 1200px; margin: 0 auto 40px; flex-wrap: wrap; gap: 40px;">
            <div class="footer-col" style="text-align: left;">
                <h4 style="color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600;">Fluxium Capital</h4>
                <p style="color: #64748b; margin: 5px 0; font-size: 15px;">Registered in Cayman Islands</p>
                <p style="color: #64748b; margin: 5px 0; font-size: 15px;"><strong>Regional Base:</strong> Singapore</p>
            </div>
            <div class="footer-col" style="text-align: left;">
                <h4 style="color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600;">Contact</h4>
                <p><a href="mailto:fluxiumhann@gmail.com" style="color: #64748b; text-decoration: none; font-size: 15px;">fluxiumhann@gmail.com</a></p>
            </div>
            <div class="footer-col" style="text-align: left;">
                <h4 style="color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600;">Social</h4>
                <p><a href="#" style="color: #64748b; text-decoration: none; font-size: 15px;">LinkedIn</a></p>
                <p><a href="#" style="color: #64748b; text-decoration: none; font-size: 15px;">Twitter</a></p>
                <p><a href="#" style="color: #64748b; text-decoration: none; font-size: 15px;">Discord</a></p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2024 Fluxium Capital. All rights reserved.</p>
            <p style="margin-top: 5px; color: #334155; font-size: 12px;">Disclaimer: This website is for informational purposes only. Nothing herein constitutes an offer to sell or buy any product or service.</p>
        </div>
    </footer>

    <!-- App Scripts -->
    <script src="js/main.js?v=28"></script>
</body>
</html>
"""

import os
with open('/Users/xingxiu/Desktop/Fluxium网站/css/main.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

with open('/Users/xingxiu/Desktop/Fluxium网站/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Files successfully written to disk!")
