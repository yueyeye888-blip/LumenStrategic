# -*- coding: utf-8 -*-
import os
import re

# 1. Update index.html to submit to backend API
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace old form action
html = re.sub(
    r'<form class="contact-form" id="contact-form"[^>]*>',
    '<form class="contact-form" id="contact-form" onsubmit="handleFormSubmit(event)">',
    html
)

# Add handling script
script_block = """
    <script>
        // 当你买好服务器后，请将这里的地址替换为你服务器的真实 IP 或者域名
        // 例如： "http://123.45.67.89:5000/api/submit"
        window.BACKEND_API_URL = "http://127.0.0.1:5000/api/submit";

        function handleFormSubmit(event) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // 获取下拉框的文本（而不是数字）
            const typeSelect = form.querySelector('[name="investor_type"]');
            const interestSelect = form.querySelector('[name="interest"]');
            if (typeSelect.selectedIndex > 0) data.investor_type = typeSelect.options[typeSelect.selectedIndex].text;
            if (interestSelect.selectedIndex > 0) data.interest = interestSelect.options[interestSelect.selectedIndex].text;

            const btn = form.querySelector('button[type="submit"]');
            const originalText = btn.innerText;
            btn.innerText = "Submitting...";
            btn.disabled = true;

            fetch(window.BACKEND_API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(resData => {
                alert(currentLang === 'zh' ? "合作申请提交成功！我们会尽快联系您。" : "Application submitted successfully!");
                form.reset();
            })
            .catch(err => {
                console.error(err);
                alert(currentLang === 'zh' ? "提交失败，请检查网络或稍后重试。" : "Submission failed, please try again later.");
            })
            .finally(() => {
                btn.innerText = originalText;
                btn.disabled = false;
            });
        }
    </script>
</body>"""

html = html.replace("</body>", script_block)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 2. Create backend folder and files
os.makedirs("backend", exist_ok=True)

app_py_code = """import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求，前端才能向这里发数据

DB_FILE = "submissions.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                investor_type TEXT,
                interest TEXT,
                investment_size TEXT,
                needs TEXT,
                submit_time DATETIME
            )
        ''')
        conn.commit()

# 后台访问账号密码验证
def check_auth(username, password):
    # 你的后台默认账号：admin，密码：lumen2026 （你可以自己改）
    return username == 'admin' and password == 'lumen2026'

def authenticate():
    return Response(
    '无法验证您的访问权限。\\n'
    '请使用正确的账号和密码登录', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

# 处理前端表单请求的接口
@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    
    name = data.get('name')
    email = data.get('contact_email')
    investor_type = data.get('investor_type')
    interest = data.get('interest')
    investment_size = data.get('investment_size', '')
    needs = data.get('needs', '')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with sqlite3.connect(DB_FILE) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO submissions (name, email, investor_type, interest, investment_size, needs, submit_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, investor_type, interest, investment_size, needs, now))
            conn.commit()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "message": "Submited successfully!"})

# 后台查看页面
@app.route('/admin')
def admin():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM submissions ORDER BY submit_time DESC')
        rows = c.fetchall()

    html_template = '''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <title>Lumen Strategic - 数据管理后台</title>
        <style>
            body { font-family: "PingFang SC", "Microsoft YaHei", Arial, sans-serif; margin: 30px; background: #f4f6f9; }
            h1 { color: #1e293b; border-bottom: 2px solid #cbd5e1; padding-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; background: #fff; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-radius: 8px; overflow: hidden; }
            th, td { padding: 15px 20px; border-bottom: 1px solid #e2e8f0; text-align: left; }
            th { background-color: #0f172a; color: #f9d976; font-weight: 600; }
            tr:last-child td { border-bottom: none; }
            tr:hover { background-color: #f8fafc; }
        </style>
    </head>
    <body>
        <h1>客户合作申请查询后台</h1>
        <table>
            <tr>
                <th>提交时间</th><th>姓名/机构名</th><th>邮箱</th><th>投资人类型</th><th>关注方向</th><th>预计规模</th><th>详情与诉求</th>
            </tr>
            {% for r in rows %}
            <tr>
                <td>{{ r['submit_time'] }}</td>
                <td>{{ r['name'] }}</td>
                <td><a href="mailto:{{ r['email'] }}">{{ r['email'] }}</a></td>
                <td>{{ r['investor_type'] }}</td>
                <td>{{ r['interest'] }}</td>
                <td>{{ r['investment_size'] }}</td>
                <td style="max-width: 300px; line-height: 1.5;">{{ r['needs'] }}</td>
            </tr>
            {% else %}
            <tr><td colspan="7" style="text-align: center; color: #94a3b8;">暂无提交记录</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    '''
    return render_template_string(html_template, rows=rows)

if __name__ == '__main__':
    init_db()
    # 这里的 5000 是端口号，部署到服务器上时可以保持不变
    app.run(host='0.0.0.0', port=5000, debug=True)
"""

with open("backend/app.py", "w", encoding="utf-8") as f:
    f.write(app_py_code)

req_code = """Flask==3.0.0
flask-cors==4.0.0
"""
with open("backend/requirements.txt", "w", encoding="utf-8") as f:
    f.write(req_code)

