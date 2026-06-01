import os
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
    '无法验证您的访问权限。\n'
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
