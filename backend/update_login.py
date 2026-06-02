import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update imports
content = re.sub(
    r'from flask import Flask, request, jsonify, render_template_string, Response',
    r'from flask import Flask, request, jsonify, render_template_string, Response, session, redirect, url_for',
    content
)

# Insert secret key
content = re.sub(
    r'app = Flask\(__name__\)',
    r"app = Flask(__name__)\napp.secret_key = 'lumen_strategic_secret_key_2026'",
    content
)

# Remove the old authenticate function and check_auth usage inside /admin
old_auth_code = '''# 后台访问账号密码验证
def check_auth(username, password):
    # 你的后台默认账号：admin，密码：lumen2026 （你可以自己改）
    return username == 'admin' and password == 'lumen2026'

def authenticate():
    return Response(
    '无法验证您的访问权限。\\n'
    '请使用正确的账号和密码登录', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})'''

content = content.replace(old_auth_code, '''# 账号密码验证
def check_auth(username, password):
    # 你的后台默认账号：admin，密码：lumen2026 （你可以自己改）
    return username == 'admin' and password == 'lumen2026'

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lumen Strategic - 管理员登录</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body {
            background-image: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gray-900 px-6 py-8 text-center">
            <h2 class="text-2xl font-bold text-yellow-500 tracking-widest uppercase mb-2">LUMEN STRATEGIC</h2>
            <p class="text-gray-400 text-sm">系统安全访问网关</p>
        </div>
        <div class="p-8">
            {% if error %}
            <div class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm text-red-700 font-medium">{{ error }}</p>
                    </div>
                </div>
            </div>
            {% endif %}
            
            <form method="POST" action="/login" class="space-y-6">
                <div>
                    <label for="username" class="block text-sm font-medium text-gray-700 mb-1">管理员账号</label>
                    <input type="text" id="username" name="username" required autocomplete="username" class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors bg-gray-50 focus:bg-white text-gray-900" placeholder="请输入账号">
                </div>
                <div>
                    <label for="password" class="block text-sm font-medium text-gray-700 mb-1">访问密码</label>
                    <input type="password" id="password" name="password" required autocomplete="current-password" class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors bg-gray-50 focus:bg-white text-gray-900" placeholder="请输入密码">
                </div>
                <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-gray-900 bg-yellow-400 hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-all font-bold">
                    安全登录
                </button>
            </form>
        </div>
        <div class="bg-gray-50 px-6 py-4 border-t border-gray-100 text-center">
            <p class="text-xs text-gray-500">此系统限制授权访问。未经许可，请勿尝试登录。</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if check_auth(username, password):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = '账号或密码错误，请重试'
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
''')

admin_replacement = '''# 后台查看页面
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))'''

old_admin_code = '''# 后台查看页面
@app.route('/admin')
def admin():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()'''

content = content.replace(old_admin_code, admin_replacement)

# Also add a logout button to the admin dashboard nav bar
nav_replacement = '''<div class="flex items-center">
                    <span class="text-gray-300 text-sm font-medium mr-4">欢迎回来, 管理员</span>
                    <a href="/logout" class="text-sm font-medium text-gray-400 hover:text-white transition-colors bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded">退出登录</a>
                </div>'''

content = re.sub(r'<div class="flex items-center">\s*<span class="text-gray-300 text-sm font-medium">欢迎回来, 管理员</span>\s*</div>', nav_replacement, content)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
