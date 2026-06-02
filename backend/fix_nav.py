import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_nav = """<div class="flex items-center">
                    <span class="text-gray-300 text-sm font-medium">管理员工作台</span>
                </div>"""

new_nav = """<div class="flex items-center">
                    <span class="text-gray-300 text-sm font-medium mr-4">管理员工作台</span>
                    <a href="/register" class="text-sm font-medium text-yellow-500 hover:text-yellow-400 transition-colors mr-3 bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded border border-gray-600">添加管理员</a>
                    <a href="/logout" class="text-sm font-medium text-gray-400 hover:text-white transition-colors bg-gray-800 hover:bg-gray-700 px-3 py-1.5 rounded">退出登录</a>
                </div>"""

# Replace in content (handling exact whitespace or general regex if needed)
content = re.sub(r'<div class="flex items-center">\s*<span class="text-gray-300 text-sm font-medium">管理员工作台</span>\s*</div>', new_nav, content)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Nav fixed")
