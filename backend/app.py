import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, Response, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'lumen_strategic_secret_key_2026'
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
        
        # 创建管理员表
        c.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        
        # 如果没有管理员，则创建默认管理员
        c.execute('SELECT COUNT(*) FROM admins')
        if c.fetchone()[0] == 0:
            c.execute('INSERT INTO admins (username, password) VALUES (?, ?)',
                      ('admin', generate_password_hash('lumen2026')))
        conn.commit()

# 账号密码验证
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
            <div class="mt-5 text-center">
                <a href="/register" class="text-sm text-yellow-600 hover:text-yellow-500 font-medium transition-colors">没有账号？注册新管理员 &rarr;</a>
            </div>
        </div>
        <div class="bg-gray-50 px-6 py-4 border-t border-gray-100 text-center">
            <p class="text-xs text-gray-500">此系统限制授权访问。未经许可，请勿尝试登录。</p>
        </div>
    </div>
</body>
</html>
"""



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
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM submissions ORDER BY submit_time DESC')
        rows = c.fetchall()

    html_template = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lumen Strategic - 数据中心</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body { background-color: #f3f4f6; }
        .glass-panel { background: #ffffff; border: 1px solid #e5e7eb; }
        .table-row { transition: all 0.2s ease; }
        .table-row:hover { background-color: #f8fafc; transform: translateY(-1px); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
        .truncate-custom { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; white-space: normal; }
    </style>
</head>
<body class="text-gray-800 font-sans antialiased min-h-screen flex flex-col">
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
                    <span class="text-gray-300 text-sm font-medium">管理员工作台</span>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-bold text-gray-900">合作申请数据中心</h1>
            <div class="text-sm text-gray-500 bg-white px-4 py-2 border border-gray-200 rounded-lg shadow-sm">共收集到 <span id="rowCount" class="font-bold text-gray-900 text-lg">{{ rows|length }}</span> 份意向</div>
        </div>

        <!-- Toolbar (Filters & Search) -->
        <div class="glass-panel p-4 rounded-xl shadow-sm mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="flex-1 w-full md:w-1/3">
                <div class="relative">
                    <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                        <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                    </span>
                    <input type="text" id="searchInput" class="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:bg-white transition-all shadow-sm" placeholder="搜索姓名、邮箱或诉求详情...">
                </div>
            </div>
            
            <div class="flex gap-4 w-full md:w-auto">
                <select id="typeFilter" class="w-full md:w-auto py-2 px-3 border border-gray-200 bg-gray-50 focus:bg-white rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 shadow-sm transition-all">
                    <option value="">全部投资人类型</option>
                    <option value="individual">个人投资者</option>
                    <option value="institution">机构投资者</option>
                    <option value="corporate">企业客户</option>
                </select>
                <select id="interestFilter" class="w-full md:w-auto py-2 px-3 border border-gray-200 bg-gray-50 focus:bg-white rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 shadow-sm transition-all">
                    <option value="">全部关注方向</option>
                    <option value="crypto">加密货币/Web3</option>
                    <option value="forex">外汇交易</option>
                    <option value="equity">全球股市</option>
                    <option value="custom">定制化资管方案</option>
                </select>
            </div>
        </div>

        <!-- Data Table -->
        <div class="glass-panel overflow-hidden shadow-sm rounded-xl">
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200" id="dataTable">
                    <thead class="bg-gray-50">
                        <tr>
                            <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">提交时间</th>
                            <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">客户身份</th>
                            <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">投资意向</th>
                            <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider">预计规模</th>
                            <th scope="col" class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider w-1/3">核心诉求</th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200" id="tableBody">
                        {% for r in rows %}
                        <tr class="table-row data-item">
                            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {{ r['submit_time'] }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="font-bold text-gray-900 search-target">{{ r['name'] }}</div>
                                <div class="text-sm text-blue-500 hover:text-blue-700 search-target mt-0.5"><a href="mailto:{{ r['email'] }}">{{ r['email'] }}</a></div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2.5 py-1 inline-flex text-xs leading-5 font-semibold rounded-md bg-indigo-50 text-indigo-700 type-val border border-indigo-100" data-val="{{ r['investor_type'] }}">
                                    {% if r['investor_type'] == 'individual' %}个人投资者{% elif r['investor_type'] == 'institution' %}机构投资者{% elif r['investor_type'] == 'corporate' %}企业客户{% else %}{{ r['investor_type'] }}{% endif %}
                                </span>
                                <div class="text-sm text-gray-600 mt-1.5 font-medium interest-val" data-val="{{ r['interest'] }}">
                                    {% if r['interest'] == 'crypto' %}加密货币 & Web3{% elif r['interest'] == 'forex' %}外汇交易{% elif r['interest'] == 'equity' %}全球股市{% elif r['interest'] == 'custom' %}定制方案{% else %}{{ r['interest'] }}{% endif %}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-emerald-600">
                                {{ r['investment_size'] }}
                            </td>
                            <td class="px-6 py-4 text-sm text-gray-600 search-target" title="{{ r['needs'] }}">
                                <div class="truncate-custom leading-relaxed">
                                    {{ r['needs'] }}
                                </div>
                            </td>
                        </tr>
                        {% else %}
                        <tr id="emptyRow">
                            <td colspan="5" class="px-6 py-16 text-center text-gray-400">
                                <svg class="mx-auto h-12 w-12 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                                </svg>
                                <h3 class="mt-4 text-sm font-medium text-gray-900">暂无数据</h3>
                                <p class="mt-1 text-sm text-gray-500">当前还没有任何客户提交合作申请。</p>
                            </td>
                        </tr>
                        {% endfor %}
                        <tr id="noResultRow" style="display: none;">
                            <td colspan="5" class="px-6 py-16 text-center text-gray-400">
                                <h3 class="mt-2 text-sm font-medium text-gray-900">未找到匹配的结果</h3>
                                <p class="mt-1 text-sm text-gray-500">请尝试更换搜索词或重置筛选条件。</p>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const searchInput = document.getElementById('searchInput');
            const typeFilter = document.getElementById('typeFilter');
            const interestFilter = document.getElementById('interestFilter');
            const rows = document.querySelectorAll('.data-item');
            const noResultRow = document.getElementById('noResultRow');
            const rowCount = document.getElementById('rowCount');

            function filterData() {
                const searchTerm = searchInput.value.toLowerCase();
                const typeTerm = typeFilter.value.toLowerCase();
                const interestTerm = interestFilter.value.toLowerCase();
                
                let visibleCount = 0;

                rows.forEach(row => {
                    let textMatch = false;
                    const searchTargets = row.querySelectorAll('.search-target');
                    searchTargets.forEach(el => {
                        if (el.textContent.toLowerCase().includes(searchTerm)) {
                            textMatch = true;
                        }
                    });

                    const typeVal = row.querySelector('.type-val')?.getAttribute('data-val') || '';
                    const interestVal = row.querySelector('.interest-val')?.getAttribute('data-val') || '';

                    const typeMatch = (typeTerm === '' || typeVal.toLowerCase() === typeTerm);
                    const interestMatch = (interestTerm === '' || interestVal.toLowerCase() === interestTerm);

                    if (textMatch && typeMatch && interestMatch) {
                        row.style.display = '';
                        visibleCount++;
                    } else {
                        row.style.display = 'none';
                    }
                });

                rowCount.textContent = visibleCount;
                if (visibleCount === 0 && rows.length > 0) {
                    noResultRow.style.display = '';
                } else {
                    noResultRow.style.display = 'none';
                }
            }

            searchInput.addEventListener('input', filterData);
            typeFilter.addEventListener('change', filterData);
            interestFilter.addEventListener('change', filterData);
        });
    </script>
</body>
</html>
"""
    return render_template_string(html_template, rows=rows)

if __name__ == '__main__':
    init_db()
    # 这里的 5000 是端口号，部署到服务器上时可以保持不变
    app.run(host='0.0.0.0', port=5000, debug=True)
