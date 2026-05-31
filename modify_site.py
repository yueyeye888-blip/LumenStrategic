# -*- coding: utf-8 -*-
import re
import os

# 1. Update js/i18n.js
i18n_content = """const translations = {
    "nav-about": { en: "About Us", zh: "关于我们" },
    "nav-services": { en: "Core Strategies", zh: "核心策略" },
    "nav-criteria": { en: "Partnership Criteria", zh: "合作准入" },
    "nav-contact": { en: "Contact Us", zh: "联系我们" },
    
    "hero-title": { en: "Lumen Strategic<br>Capital PTE. LTD.", zh_html: "Lumen Strategic<br>Capital PTE. LTD.", en_html: "Lumen Strategic<br>Capital PTE. LTD.", zh: "Lumen Strategic Capital PTE. LTD." },
    "hero-sub": { en: "STRATEGIC CAPITAL MANAGEMENT & ALTERNATIVE INVESTMENT SOLUTIONS", zh: "STRATEGIC CAPITAL MANAGEMENT & ALTERNATIVE INVESTMENT SOLUTIONS" },
    "hero-desc": { en: "We are a Singapore-based licensed fund management company, dedicated to providing qualified investors and professional institutions with cross-market, cross-cycle asset allocation and alternative investment solutions.", zh: "我们是一家位于新加坡的持牌基金管理公司，专注于为合格投资人与专业机构提供跨市场、跨周期的资产配置与另类投资解决方案。" },
    "hero-btn": { en: "Schedule a Consultation", zh: "预约沟通" },
    
    "about-title": { en: "Why Lumen Strategic", zh: "为什么选择Lumen Strategic" },
    "about-sub": { en: "Institutional frameworks for capital management, long-term discipline across cycles", zh: "以机构化框架管理资本，以长期纪律穿越周期" },
    "about-p1": { en: "Based in Singapore, Lumen Strategic Capital PTE. LTD. provides fund services centered on primary market investments and secondary market strategic allocations for qualified investors and professional institutions.", zh: "Lumen Strategic Capital PTE. LTD. 立足新加坡，面向合格投资人与专业机构，提供以一级市场投资和二级市场策略配置为核心的基金服务。" },
    "about-p2": { en: "Our team possesses extensive experience in fund management, capital markets, and cross-asset allocation, having managed and allocated over $800 million in institutional capital. We adhere to risk control, strategic discipline, and compliance processes at our core, building robust, transparent, and sustainable investment partnerships.", zh: "我们的团队拥有丰富的基金管理、资本市场与跨资产配置经验，曾参与管理及配置超过8亿美元规模的机构资金。我们坚持以风险控制、策略纪律和合规流程为核心，为投资人构建稳健、透明、可持续的投资合作关系。" },
    
    "stat-lbl-1": { en: "Singapore Licensed<br>Fund Management Company", zh_html: "LFMC<br>新加坡持牌基金管理主体", en_html: "Singapore Licensed<br>Fund Management Company", zh: "新加坡持牌基金管理主体" },
    "stat-lbl-2": { en: "Team's past institutional capital<br>management & allocation experience", zh_html: "团队过往机构资金<br>管理与配置经验", en_html: "Team's past institutional capital<br>management & allocation experience", zh: "团队过往机构资金管理与配置经验" },
    "stat-lbl-3": { en: "Covering primary and secondary<br>market asset strategies", zh_html: "覆盖一级市场、二级市场<br>的资产策略", en_html: "Covering primary and secondary<br>market asset strategies", zh: "覆盖一级市场、二级市场的资产策略" },

    "srv-title": { en: "Core Businesses", zh: "核心业务" },
    "srv-sub": { en: "A comprehensive fund management platform covering primary market growth opportunities and secondary market strategy allocation", zh: "覆盖一级市场成长机会与二级市场策略配置的综合基金管理平台" },
    
    "srv-card1-t": { en: "Private Market Investments", zh: "一级市场投资" },
    "srv-card1-p": { en: "Focusing on emerging industry trends with long-term growth potential, including Artificial Intelligence, computing infrastructure, and new financial infrastructure.<br><br>Through industry research, project screening, due diligence, and portfolio management, we seek high-quality assets with technical barriers, commercialization potential, and long-term value creation capabilities.<br><br><span style='color:#f9d976; font-size:14px; font-weight:600;'>AI / Computing Infrastructure / New Finance</span>", zh_html: "聚焦具备长期增长潜力的新兴产业方向，包括人工智能、算力基础设施与新金融基础设施等领域。<br><br>我们通过行业研究、项目筛选、尽职调查与组合管理，寻找具备技术壁垒、商业化潜力和长期价值创造能力的优质资产。<br><br><span style='color:#f9d976; font-size:14px; font-weight:600;'>AI / Computing Infrastructure / New Finance</span>" },
    
    "srv-card2-t": { en: "Systematic Quantitative Strategies", zh: "系统化量化策略" },
    "srv-card2-p": { en: "Based on multi-market data, quantitative models, and a disciplined trading framework to identify relative value opportunities and structural return sources.<br><br>This strategy emphasizes model-driven execution, diversified allocation, risk budgeting, and continuous drawdown control, making it suitable as a robust strategy module in the fund portfolio.", zh_html: "基于多市场数据、量化模型与纪律化交易框架，识别市场中的相对价值机会与结构性收益来源。<br><br>该策略强调模型驱动、分散配置、风险预算与持续回撤控制，适合作为基金组合中的稳健型策略模块。" },
    
    "srv-card3-t": { en: "Active Trading Strategies", zh: "主动策略" },
    "srv-card3-p": { en: "Leveraging our team's long-term experience in capital markets, trade execution, and risk management, we actively allocate based on market trends, asset pricing, liquidity changes, and volatility structures.<br><br>The strategy focuses on flexible execution, dynamic position management, and risk hedging to seek more resilient return performance across different market environments.", zh_html: "依托团队在资本市场、交易执行与风险管理方面的长期经验，围绕市场趋势、资产定价、流动性变化与波动结构进行主动配置。<br><br>该策略注重灵活执行、动态仓位管理与风险对冲，在不同市场环境下寻求更具弹性的收益表现。" },
    "srv-note": { en: "* This strategy is only available to eligible professional investors; specific risks, fees, and return distributions are subject to formal documentation.", zh: "* 该策略仅面向符合条件的专业投资人，具体风险、费用与收益分配以正式文件为准。" },

    "crit-title": { en: "Partnership Criteria", zh: "合作准入" },
    "crit-sub": { en: "We seek long-term, compliant, and risk-aware qualified investment partners", zh: "我们寻找长期、合规、具备风险认知的合格投资伙伴" },
    "crit-lbl-1": { en: "Qualified Investors", zh: "合格投资人身份" },
    "crit-p-1": { en: "Only available to qualified investors, institutional investors, or professional investors meeting relevant Singapore regulatory requirements.", zh: "仅面向符合新加坡相关法规要求的合格投资人、机构投资人或专业投资人。" },
    "crit-lbl-2": { en: "Clear Source of Funds", zh: "清晰的资金来源" },
    "crit-p-2": { en: "Investors must cooperate to complete KYC, AML, identity verification, and source of wealth checks.", zh: "投资人需配合完成 KYC、AML、身份核验及资金来源审查。" },
    "crit-lbl-3": { en: "Matching Investment Horizon", zh: "匹配的投资周期" },
    "crit-p-3": { en: "We value medium to long-term collaborative relationships. Investment horizons, liquidity needs, and strategy characteristics must align.", zh: "我们更重视中长期合作关系，投资周期、流动性需求与策略特征需保持一致。" },
    "crit-lbl-4": { en: "Capital Risk Awareness", zh: "非保本风险认知" },
    "crit-p-4": { en: "All products are non-principal-protected investments with no promise of fixed, minimum, or risk-free returns.", zh: "所有产品均为非保本投资，不承诺固定收益、最低收益或无风险回报。" },
    "crit-lbl-5": { en: "Reasonable Return Expectations", zh: "合理的收益预期" },
    "crit-p-5": { en: "Strategy performance is subject to market environments, asset quality, execution, and risk events. Past performance is not indicative of future returns.", zh: "策略表现受市场环境、资产质量、执行情况及风险事件影响，历史表现不代表未来收益。" },
    "crit-lbl-6": { en: "Long-term Resource Synergy", zh: "长期资源协同" },
    "crit-p-6": { en: "Beyond capital collaboration, we welcome partners who can provide synergies in industry, projects, institutional resources, or market networks.", zh: "除资金合作外，我们也欢迎能够在产业、项目、机构资源或市场网络方面形成协同的合作伙伴。" },

    "cnt-title": { en: "Get In Touch", zh: "联系我们" },
    "cnt-sub": { en: "Welcome qualified investors and professional institutions to schedule a 1-on-1 consultation", zh: "欢迎合格投资人与专业机构与我们预约一对一沟通" },
    "cnt-desc": { en: "If you wish to learn more about Lumen Strategic Capital's fund products, strategy frameworks, or partnership onboarding processes, please fill out the information below. We will contact you within 24 to 48 business hours.", zh: "如您希望了解Lumen Strategic Capital的基金产品、策略框架或合作准入流程，请填写以下信息。我们将在24至48个工作小时内与您联系。" },
    
    "frm-l1": { en: "Name / Institution Name *", zh: "姓名 / 机构名称 *" },
    "frm-l2": { en: "Contact Email *", zh: "联系邮箱 *" },
    "frm-l3": { en: "Investor Type *", zh: "投资人类型 *" },
    "frm-type-op1": { en: "Qualified Individual Investor", zh: "合格个人投资人" },
    "frm-type-op2": { en: "Family Office", zh: "家族办公室" },
    "frm-type-op3": { en: "Fund / Asset Manager", zh: "基金 / 资管机构" },
    "frm-type-op4": { en: "Corporate / Industrial Capital", zh: "企业 / 产业资本" },
    "frm-type-op5": { en: "Other", zh: "其他" },
    "frm-l4": { en: "Areas of Interest *", zh: "关注方向 *" },
    "frm-int-op1": { en: "Primary Market Investments", zh: "一级市场投资" },
    "frm-int-op2": { en: "Systematic Quantitative Strategies", zh: "系统化量化策略" },
    "frm-int-op3": { en: "Active Multi-Asset Strategies", zh: "主动多资产策略" },
    "frm-int-op4": { en: "Comprehensive Allocation Solutions", zh: "综合配置方案" },
    "frm-l5": { en: "Expected Investment Size (USD)", zh: "预计投资规模 (单位：美元)" },
    "frm-l6": { en: "Investment Horizon & Partnership Needs *", zh: "投资周期与合作诉求 *" },
    "frm-btn": { en: "Submit Application", zh: "提交合作申请" },
    "frm-note": { en: "Submission of information does not constitute a subscription application. All partnerships require investor suitability assessments, KYC/AML reviews, and the signing of formal documents.", zh: "提交信息不构成认购申请。所有合作均需完成投资人适当性评估、KYC/AML 审查及正式文件签署。" },
    
    "ft-1": { en: "Singapore-based Licensed Fund Management Company<br>Fund management for qualified investors and professional institutions.", zh_html: "Singapore-based Licensed Fund Management Company<br>面向合格投资人与专业机构的基金管理", en_html: "Singapore-based Licensed Fund Management Company<br>Fund management for qualified investors and professional institutions." },
    "ft-3": { en: "Contact", zh: "联系方式" },
    "ft-nav": { en: "Navigation", zh: "导航" },
    "ft-legal": { en: "This website is for general informational purposes only and does not constitute an offer, invitation, recommendation, or solicitation for any securities, fund shares, collective investment schemes, or other financial products. Any fund products or investment strategies are exclusively available to qualified investors, institutional investors, or professional investors meeting the requirements of relevant laws and regulations.<br>Investments involve risks; past performance does not represent future results. Any target returns, historical performance, or strategy expectations do not constitute a commitment to fixed returns, minimum returns, principal protection, or risk-free outcomes. Investors should read the relevant fund documents and seek independent legal, tax, and financial advice based on their own circumstances before making any investment decisions.", zh_html: "本网站内容仅供一般信息参考，不构成任何证券、基金份额、集体投资计划或其他金融产品的要约、邀请、建议或招揽。任何基金产品或投资策略仅面向符合相关法律法规要求的合格投资人、机构投资人或专业投资人。<br>投资涉及风险，过往表现不代表未来结果。任何目标收益、历史表现或策略预期均不构成固定收益、最低收益、保本或无风险承诺。投资人应在作出任何投资决定前，阅读相关基金文件，并根据自身情况寻求独立的法律、税务及财务建议。" },
    "ft-copy": { en: "© 2026 Lumen Strategic Capital PTE. LTD. All rights reserved.", zh: "© 2026 Lumen Strategic Capital PTE. LTD. All rights reserved." }
};

let currentLang = "zh";

window.toggleLanguage = function() {
    currentLang = currentLang === "en" ? "zh" : "en";
    
    const enBtn = document.getElementById("lang-en-btn");
    const zhBtn = document.getElementById("lang-zh-btn");
    
    if (enBtn && zhBtn) {
        enBtn.style.color = currentLang === "en" ? "#fff" : "rgba(255,255,255,0.5)";
        enBtn.style.fontWeight = currentLang === "en" ? "700" : "400";
        zhBtn.style.color = currentLang === "zh" ? "#fff" : "rgba(255,255,255,0.5)";
        zhBtn.style.fontWeight = currentLang === "zh" ? "700" : "400";
    }

    const elements = document.querySelectorAll("[data-i18n]");
    elements.forEach(el => {
        const key = el.getAttribute("data-i18n");
        if(translations[key]) {
            if(el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.tagName === "SELECT") {
                el.placeholder = translations[key][currentLang];
            }
            if(translations[key][currentLang + "_html"]) {
                el.innerHTML = translations[key][currentLang + "_html"];
            } else if (translations[key][currentLang]) {
                if (el.tagName !== "INPUT" && el.tagName !== "TEXTAREA" && el.tagName !== "SELECT") {
                    if (el.tagName === "OPTION") {
                        el.innerText = translations[key][currentLang];
                    } else {
                        el.innerText = translations[key][currentLang];
                    }
                }
            }
        }
    });

    const options = document.querySelectorAll("option[data-i18n]");
    options.forEach(opt => {
        const key = opt.getAttribute("data-i18n");
        if(translations[key] && translations[key][currentLang]) {
            opt.innerText = translations[key][currentLang];
        }
    });
};

document.addEventListener("DOMContentLoaded", () => {
    // initialize language to zh
    currentLang = "en"; // will flip to zh
    toggleLanguage();
});
"""

with open("js/i18n.js", "w", encoding="utf-8") as f:
    f.write(i18n_content)

# 2. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update title
html = re.sub(r'<title>.*?</title>', '<title>Lumen Strategic Capital</title>', html)

# Update Logo (replace img with stylised text component)
html = re.sub(
    r'<img src="logo_processed.png"[^>]*>', 
    '<span style="font-size:20px; font-weight:800; color:#fff; letter-spacing:1px; font-family:\'Inter\',sans-serif; text-align:left; line-height:1.2;">LUMEN<br><span style="font-size:11px; color:#f9d976; letter-spacing:1.5px; font-weight:600;">STRATEGIC CAPITAL</span></span>', 
    html
)

# Hero subtitle sizing
html = html.replace('class="title-sub highlight-gold" style="font-size: 36px;', 'class="title-sub highlight-gold" style="font-size: 24px; max-width:800px;')

# Stats update numbers
html = html.replace('<div class="stat-number">Tier-1</div>', '<div class="stat-number">LFMC</div>')
html = html.replace('<div class="stat-number">24/7</div>', '<div class="stat-number" style="font-size:38px; line-height:1.2;">US$800M+</div>')
html = html.replace('<div class="stat-number">$100M+</div>', '<div class="stat-number" style="font-size:32px; line-height:1.2;">Multi-<br>Strategy</div>')

# Services extra note
cards_end = html.find('</section>', html.find('class="grid-3"'))
html = html[:cards_end] + '<p style="text-align:center; color:#64748b; font-size:14px; margin-top:50px; padding:0 20px;" data-i18n="srv-note"></p>\n        </div>\n    ' + html[cards_end:]

# Criteria items (replace 4 with 6)
crit_block = """
                <div class="criteria-item">
                    <div class="criteria-number">01</div>
                    <div class="criteria-text">
                        <div class="criteria-label" data-i18n="crit-lbl-1"></div>
                        <p data-i18n="crit-p-1"></p>
                    </div>
                </div>
                <div class="criteria-item">
                    <div class="criteria-number">02</div>
                    <div class="criteria-text">
                        <div class="criteria-label" data-i18n="crit-lbl-2"></div>
                        <p data-i18n="crit-p-2"></p>
                    </div>
                </div>
                <div class="criteria-item">
                    <div class="criteria-number">03</div>
                    <div class="criteria-text">
                        <div class="criteria-label" data-i18n="crit-lbl-3"></div>
                        <p data-i18n="crit-p-3"></p>
                    </div>
                </div>
                <div class="criteria-item">
                    <div class="criteria-number">04</div>
                    <div class="criteria-text">
                        <div class="criteria-label" data-i18n="crit-lbl-4"></div>
                        <p data-i18n="crit-p-4"></p>
                    </div>
                </div>
                <div class="criteria-item">
                    <div class="criteria-number">05</div>
                    <div class="criteria-text">
                        <div class="criteria-label" data-i18n="crit-lbl-5"></div>
                        <p data-i18n="crit-p-5"></p>
                    </div>
                </div>
                <div class="criteria-item">
                    <div class="criteria-number">06</div>
                    <div class="criteria-text">
                        <div class="criteria-label" data-i18n="crit-lbl-6"></div>
                        <p data-i18n="crit-p-6"></p>
                    </div>
                </div>
"""
html = re.sub(r'<div class="criteria-content" style="max-width: 900px; margin: 0 auto;">.*?</div>\s*</div>\s*</section>', '<div class="criteria-content" style="max-width: 900px; margin: 0 auto;">' + crit_block + '</div>\n        </div>\n    </section>', html, flags=re.DOTALL)

# Form structure
form_block = """
                    <div class="form-row">
                        <div class="form-group">
                            <label data-i18n="frm-l1">Name / Institution Name *</label>
                            <input type="text" name="name" required>
                        </div>
                        <div class="form-group">
                            <label data-i18n="frm-l2">Contact Email *</label>
                            <input type="email" name="contact_email" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label data-i18n="frm-l3">Investor Type *</label>
                            <select name="investor_type" required class="select-css" style="width: 100%; padding: 16px 15px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; color: #fff; font-size: 15px; outline: none; transition: border-color 0.3s; font-family: 'Inter', sans-serif;">
                                <option value="" disabled selected data-i18n="frm-l3">Select...</option>
                                <option value="1" data-i18n="frm-type-op1">Qualified Individual Investor</option>
                                <option value="2" data-i18n="frm-type-op2">Family Office</option>
                                <option value="3" data-i18n="frm-type-op3">Fund / Asset Manager</option>
                                <option value="4" data-i18n="frm-type-op4">Corporate / Industrial Capital</option>
                                <option value="5" data-i18n="frm-type-op5">Other</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label data-i18n="frm-l4">Areas of Interest *</label>
                            <select name="interest" required class="select-css" style="width: 100%; padding: 16px 15px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; color: #fff; font-size: 15px; outline: none; transition: border-color 0.3s; font-family: 'Inter', sans-serif;">
                                <option value="" disabled selected data-i18n="frm-l4">Select...</option>
                                <option value="1" data-i18n="frm-int-op1">Primary Market Investments</option>
                                <option value="2" data-i18n="frm-int-op2">Systematic Quantitative Strategies</option>
                                <option value="3" data-i18n="frm-int-op3">Active Multi-Asset Strategies</option>
                                <option value="4" data-i18n="frm-int-op4">Comprehensive Allocation Solutions</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label data-i18n="frm-l5">Expected Investment Size (USD)</label>
                        <input type="text" name="investment_size">
                    </div>
                    
                    <div class="form-group">
                        <label data-i18n="frm-l6">Investment Horizon & Partnership Needs *</label>
                        <textarea name="needs" rows="4" required style="width: 100%; padding: 16px 15px; background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; color: #fff; font-size: 15px; outline: none; transition: border-color 0.3s; font-family: 'Inter', sans-serif; resize: vertical;"></textarea>
                    </div>
                    
                    <button type="submit" class="submit-btn" style="width: 100%; padding: 18px; background: linear-gradient(135deg, #f9d976 0%, #e9b646 100%); border: none; border-radius: 8px; color: #020408; font-size: 18px; font-weight: 700; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; margin-top: 10px;"><span data-i18n="frm-btn">Submit Application</span></button>
                    <p class="form-note" style="text-align: center; color: #64748b; font-size: 14px; margin-top: 15px;"><span data-i18n="frm-note"></span></p>
                </form>
"""
# Replace the form group from <div class="form-row"> to </form>
html = re.sub(r'<div class="form-row">.*?</form>', form_block, html, flags=re.DOTALL)

# Add description for contact section
html = html.replace('<div class="section-subtitle" style="margin-bottom: 40px;"><span data-i18n="cnt-sub">We invite qualified project leaders to Singapore for confidential consultation.</span></div>', '<div class="section-subtitle" style="margin-bottom: 20px;"><span data-i18n="cnt-sub"></span></div><p style="text-align:center; max-width:800px; margin:0 auto; color:#94a3b8; font-size:16px; margin-bottom: 40px; line-height:1.6;" data-i18n="cnt-desc"></p>')


# Footer structure
footer_block = """
        <div class="footer-content" style="display: flex; justify-content: space-between; max-width: 1100px; margin: 0 auto 40px; flex-wrap: wrap; gap: 40px; text-align: left;">
            <div class="footer-col" style="flex: 2; min-width: 300px;">
                <h4 style="color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600;">Lumen Strategic Capital PTE. LTD.</h4>
                <p style="color: #94a3b8; margin: 5px 0; font-size: 14px; line-height: 1.6;" data-i18n="ft-1"></p>
            </div>
            <div class="footer-col" style="flex: 1; min-width: 200px;">
                <h4 style="color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600;" data-i18n="ft-3">Contact</h4>
                <p><a href="mailto:contact@lumenstrategic.com" style="color: #94a3b8; text-decoration: none; font-size: 14px;">contact@lumenstrategic.com</a></p>
                <p style="color: #94a3b8; margin: 5px 0; font-size: 14px;">Singapore</p>
            </div>
            <div class="footer-col" style="flex: 1; min-width: 150px;">
                <h4 style="color: #fff; font-size: 18px; margin-bottom: 15px; font-weight: 600;" data-i18n="ft-nav">Navigation</h4>
                <ul style="list-style:none; padding:0; margin:0; line-height:2;">
                    <li><a href="#about" style="color:#94a3b8; text-decoration:none; font-size:14px;" data-i18n="nav-about"></a></li>
                    <li><a href="#services" style="color:#94a3b8; text-decoration:none; font-size:14px;" data-i18n="nav-services"></a></li>
                    <li><a href="#criteria" style="color:#94a3b8; text-decoration:none; font-size:14px;" data-i18n="nav-criteria"></a></li>
                    <li><a href="#contact" style="color:#94a3b8; text-decoration:none; font-size:14px;" data-i18n="nav-contact"></a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom" style="border-top: 1px solid rgba(255,255,255,0.05); padding-top: 30px; text-align: left; max-width: 1100px; margin: 0 auto; padding-bottom: 20px;">
            <p style="color: #64748b; font-size: 13px; line-height: 1.6; margin-bottom: 20px;" data-i18n="ft-legal"></p>
            <p style="color: #475569; font-size: 13px;" data-i18n="ft-copy"></p>
        </div>
"""
html = re.sub(r'<div class="footer-content".*?</div>\s*</footer>', footer_block + '    </footer>', html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
