CONFIG = dict(
    num=811, title='子域名访问计数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表 · 从后往前拼子域名',
    code='''
class Solution:
    def subdomainVisits(self, cpdomains):

        domain_dict = {}
        for cpdomain in cpdomains:
            cnt, domain = cpdomain.split(' ')
            parts = domain.split('.')
            cnt = int(cnt)
            n = len(parts)
            now = parts[n - 1]
            domain_dict[now] = domain_dict.get(now, 0) + cnt
            for index in range(n - 2, -1, -1):
                now = parts[index] + '.' + now
                domain_dict[now] = domain_dict.get(now, 0) + cnt
        
        return [str(value) + ' ' + key for key, value in domain_dict.items()]
''',
    call="Solution().subdomainVisits(['9001 discuss.leetcode.com', '5 leetcode.com'])",
    expect=['9006 com', '9006 leetcode.com', '9001 discuss.leetcode.com'],
    views=[
        dict(type='text', h=110, size=26,
             fn=lambda S: '  |  '.join(('==' + c + '==' if c == S.get('cpdomain') else c) for c in S['cpdomains'])),
        dict(type='array', var='parts', label='parts（按 . 切开的各段）', cell=190, h=260, font=22,
             pointers={'index': 'pink'}),
        dict(type='map', var='domain_dict', label='domain_dict（域名 → 访问次数）', fmt=lambda k, v: f"{k}: {v}", font=24, h=260),
    ],
    watch=[('cnt', 'cnt', 'orange'), ('now', 'now', 'blue'), ('index', 'index', 'pink')],
    captions={
        'domain_dict = {}': '`domain_dict`：每个（子）域名累计的访问次数',
        'for cpdomain in cpdomains': lambda S, B, r: (f"处理一条记录 `{S.cpdomain!r}`" if 'cpdomain' not in B or S.cpdomain != B.cpdomain else '所有记录都处理完了'),
        'cnt, domain': '空格切开：访问次数 `{cnt}`，域名 `{domain}`',
        'parts = domain': '按 `.` 切开：`{parts}`',
        'cnt = int(cnt)': '`cnt` 转成整数 `{cnt}`',
        'n = len(parts)': '域名一共 `{n}` 段',
        'now = parts[n - 1]': '先取最后一段 `{now}`，它是最短的子域名（顶级域名）',
        'domain_dict[now] = domain_dict.get(now, 0) + cnt': '`{now}` 累计 `{B.domain_dict.get(now, 0)} + {cnt}` = =={domain_dict[now]}==',
        'for index in range': lambda S, B, r: ('从倒数第二段开始，从后往前一段一段拼' if S.now == S.parts[-1] else '这条域名的所有后缀都加完了' if S.now == S.domain else '继续往前拼一段'),
        'now = parts[index]': '前面拼上 `{parts[index]}.`，得到子域名 `{now}`',
        'return': '把每个域名和次数拼成 `"次数 域名"`，一共 `{len(domain_dict)}` 项',
    },
    cards=dict(
        one_liner='一个域名的所有后缀都算访问，从后往前拼，用 dict 累计',
        complexity='时间 `O(总段数²)`（每次拼接复制字符串），空间 `O(总段数)`',
        problem=['`"9001 discuss.leetcode.com"` 表示该域名被访问 9001 次，它的所有父域名（`leetcode.com`、`com`）也被访问 9001 次',
                 '把所有记录汇总，返回每个（子）域名的总访问次数，格式 `"次数 域名"`',
                 '本视频：`["9001 discuss.leetcode.com", "5 leetcode.com"]`'],
        quote='用点来分割域名的各个部分，然后从后往前逐个组合并使用dict统计出现次数即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`"discuss.leetcode.com"` 切成 `["discuss","leetcode","com"]`',
              '从最后一段开始：`com` → `leetcode.com` → `discuss.leetcode.com`，每个都加上 `cnt`',
              '`domain_dict.get(now, 0) + cnt`：没出现过按 0 算，不会 KeyError'],
        summary=['时间约 `O(总段数²)`，域名很短所以可以接受',
                 '易错：每个后缀都要累加，别只统计完整域名',
                 '易错：从后往前拼（`parts[index] + "." + now`），顺序反了就不是后缀',
                 '原文为 Python 2 风格（`class Solution(object)`），这里只改成 `class Solution`'],
    ),
)
