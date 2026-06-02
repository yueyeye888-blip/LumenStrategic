import re

with open('backend/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_html_template = '''html_template = """
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
"""'''

new_content = re.sub(r"html_template = '''[\s\S]*?'''", new_html_template, content)

with open('backend/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Done generating updated app.py")
