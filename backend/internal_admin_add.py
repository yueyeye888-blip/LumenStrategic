import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 移除登录页面的注册链接
content = re.sub(r'<div class="mt-5 text-center">\s*<a href="/register".*?注册新管理员 &rarr;</a>\s*</div>', '', content, flags=re.DOTALL)

# 2. 在 Dashboard Navbar 增加“添加管理员”按钮
old_nav = '''<div class="flex items-center">
                    <span class="text-gray-300 text-sm font-medium mr-4">欢迎回来, 管理员</span>
                    <a href="/logout" class="text-sm font-medium text-gray-400 hover:text-white transition-colors bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded">退出登录</a>'''

new_nav = '''<div class="flex items-center">
                    <span class="text-gray-300 text-sm font-medium mr-4">欢迎回来, 管理员</span>
                    <a href="/register" class="text-sm font-medium text-yellow-500 hover:text-yellow-400 transition-colors mr-3 bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded border border-gray-600">添加管理员</a>
                    <a href="/logout" class="text-sm font-medium text-gray-400 hover:text-white transition-colors bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded">退出登录</a>'''

content = content.replace(old_nav, new_nav)

# 3. 替换 /register 路由以及模板
# 用正则表达式找到原有的 REGISTER_TEMPLATE ... 直到 return render_template_string(...) 结束
pattern = r'REGISTER_TEMPLATE = """(.*?)return render_template_string\(REGISTER_TEMPLATE, error=error, success=success\)'

NEW_BLOCK = '''REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lumen Strategic - 添加管理员</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 text-gray-800 font-sans antialiased min-h-screen flex flex-col">
    <!-- Navbar -->
    <nav class="bg-gray-900 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0 flex items-center text-yellow-500 font-bold text-xl tracking-widest uppercase">
                        LUMEN STRATEGIC
                    </div>
                </div>
                <div class="flex items-center">
                    <a href="/admin" class="text-sm font-medium text-gray-300 hover:text-white transition-colors mr-4">返回数据中心</a>
                    <a href="/logout" class="text-sm font-medium text-gray-400 hover:text-white transition-colors bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded">退出登录</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow w-full max-w-xl mx-auto px-4 py-12">
        <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-6 border-b border-gray-100 bg-gray-50">
                <h2 class="text-xl font-bold text-gray-900">分配管理员权限</h2>
                <p class="text-sm text-gray-500 mt-1">创建的新账号将同样拥有查看所有客户提交数据的权限</p>
            </div>
            <div class="p-6">
                {% if error %}
                <div class="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                    <p class="text-sm text-red-700 font-medium">{{ error }}</p>
                </div>
                {% endif %}
                {% if success %}
                <div class="bg-green-50 border-l-4 border-green-500 p-4 mb-6">
                    <p class="text-sm text-green-700 font-medium">{{ success }}</p>
                </div>
                {% endif %}
                
                <form method="POST" action="/register" class="space-y-5">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">新管理员账号名称</label>
                        <input type="text" name="username" required class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors bg-gray-50 focus:bg-white" placeholder="如: admin_sales">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">设置登录密码</label>
                        <input type="password" name="password" required class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500 transition-colors bg-gray-50 focus:bg-white" placeholder="密码需妥善保存">
                    </div>
                    <div class="pt-4">
                        <button type="submit" class="w-full flex justify-center py-3 px-4 rounded-lg shadow-sm text-sm font-bold text-gray-900 bg-yellow-400 hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-all">
                            确认生成账号
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </main>
</body>
</html>
"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 鉴权机制：只有已经登录的管理员才能进入此页面并添加新管理员
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            error = '账号和密码不能为空。'
        else:
            try:
                with sqlite3.connect(DB_FILE) as conn:
                    c = conn.cursor()
                    c.execute('INSERT INTO admins (username, password) VALUES (?, ?)', 
                              (username, generate_password_hash(password)))
                    conn.commit()
                success = f'账号 【{username}】 创建成功！该系统管理员现在可访问登录页进行后台维护。'
            except sqlite3.IntegrityError:
                error = '该账号名称已被占用，请更换其他名称。'
            except Exception as e:
                error = f'添加失败：{str(e)}'
                
    return render_template_string(REGISTER_TEMPLATE, error=error, success=success)'''

content = re.sub(pattern, NEW_BLOCK, content, flags=re.DOTALL)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Update internal admin logic finished")
