import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
if 'from werkzeug.security import generate_password_hash, check_password_hash' not in content:
    content = content.replace(
        'from flask_cors import CORS',
        'from flask_cors import CORS\nfrom werkzeug.security import generate_password_hash, check_password_hash'
    )

# 2. Update init_db with new table and migration logic
old_init_db = '''def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(\'\'\'
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
        \'\'\')
        conn.commit()'''

new_init_db = '''def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute(\'\'\'
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
        \'\'\')
        
        # 创建管理员表
        c.execute(\'\'\'
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        \'\'\')
        
        # 如果没有管理员，则创建默认管理员
        c.execute('SELECT COUNT(*) FROM admins')
        if c.fetchone()[0] == 0:
            c.execute('INSERT INTO admins (username, password) VALUES (?, ?)',
                      ('admin', generate_password_hash('lumen2026')))
        conn.commit()'''

content = content.replace(old_init_db, new_init_db)

# 3. Update check_auth
old_check_auth = '''# 账号密码验证
def check_auth(username, password):
    # 你的后台默认账号：admin，密码：lumen2026 （你可以自己改）
    return username == 'admin' and password == 'lumen2026' '''

new_check_auth = '''# 账号密码验证
def check_auth(username, password):
    with sqlite3.connect(DB_FILE) as conn:
        c = conn.cursor()
        c.execute('SELECT password FROM admins WHERE username = ?', (username,))
        row = c.fetchone()
        if row and check_password_hash(row[0], password):
            return True
    return False'''

content = content.replace(old_check_auth, new_check_auth)

# 4. Insert registration link into login template
login_link = '''</button>
            </form>
            <div class="mt-5 text-center">
                <a href="/register" class="text-sm text-yellow-600 hover:text-yellow-500 font-medium transition-colors">没有账号？注册新管理员 &rarr;</a>
            </div>'''
content = content.replace('</button>\n            </form>', login_link)

# 5. Define REGISTER_TEMPLATE and /register route
REGISTER_CODE = '''

REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lumen Strategic - 注册管理员</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body {
            background-image: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        }
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gray-900 px-6 py-8 text-center relative">
            <a href="/login" class="absolute left-6 top-8 text-gray-400 hover:text-white transition-colors">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
            </a>
            <h2 class="text-2xl font-bold text-yellow-500 tracking-widest uppercase mb-2">添加管理员</h2>
            <p class="text-gray-400 text-sm">注册新的后台访问权限</p>
        </div>
        <div class="p-8">
            {% if error %}
            <div class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                <div class="flex items-center">
                    <div class="ml-3">
                        <p class="text-sm text-red-700 font-medium">{{ error }}</p>
                    </div>
                </div>
            </div>
            {% endif %}
            {% if success %}
            <div class="bg-green-50 border-l-4 border-green-500 p-4 mb-6">
                <div class="flex items-center">
                    <div class="ml-3">
                        <p class="text-sm text-green-700 font-medium">{{ success }}</p>
                    </div>
                </div>
            </div>
            {% endif %}
            
            <form method="POST" action="/register" class="space-y-5">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">新管理员账号</label>
                    <input type="text" name="username" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors bg-gray-50 focus:bg-white text-gray-900" placeholder="设置账号名称">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">设置密码</label>
                    <input type="password" name="password" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors bg-gray-50 focus:bg-white text-gray-900" placeholder="设置登录密码">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">系统邀请码</label>
                    <input type="password" name="invite_code" required class="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors bg-gray-50 focus:bg-white text-gray-900" placeholder="请输入邀请码以验证身份">
                    <p class="text-xs text-gray-500 mt-1">需输入系统分配的内部邀请码方可注册。</p>
                </div>
                <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-gray-900 bg-yellow-400 hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-all font-bold mt-6">
                    注册并生成授权
                </button>
            </form>
        </div>
    </div>
</body>
</html>
"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        invite_code = request.form.get('invite_code')
        
        # 保护机制：只有知道邀请码的人才能注册管理员
        if invite_code != 'lumen2026':
            error = '邀请码错误，您无权注册管理员账号。'
        elif not username or not password:
            error = '账号和密码不能为空。'
        else:
            try:
                with sqlite3.connect(DB_FILE) as conn:
                    c = conn.cursor()
                    c.execute('INSERT INTO admins (username, password) VALUES (?, ?)', 
                              (username, generate_password_hash(password)))
                    conn.commit()
                success = '注册成功！您现在可以返回登录页面使用新账号登录了。'
            except sqlite3.IntegrityError:
                error = '该账号已存在，请换一个用户名。'
            except Exception as e:
                error = f'注册失败：{str(e)}'
                
    return render_template_string(REGISTER_TEMPLATE, error=error, success=success)

'''

# Inject REGISTER_CODE right before the login route
content = content.replace('@app.route(\'/login\', methods=[\'GET\', \'POST\'])', REGISTER_CODE + '\n@app.route(\'/login\', methods=[\'GET\', \'POST\'])')

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Registration added cleanly!")
