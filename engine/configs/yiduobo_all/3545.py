CONFIG = dict(
    num=3545, title='不同字符数量最多为 K 时的最少删除数', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='哈希表计数 · 保留前 k 多',
    tags=['灵神题单', '从最小/最大开始贪心', '难度分 1211'],
    code='''
class Solution(object):
    def minDeletion(self, s, k):
        
        freq = {}
        for char in s:
            freq[char] = freq.get(char, 0) + 1
        
        return len(s) - sum(sorted(freq.values(), reverse=True)[:k])
''',
    call='Solution().minDeletion("aabcbbd", 2)',
    expect=2,
    views=[
        dict(type='string', var='s', label='s', h=170),
        dict(type='map', var='freq', label='freq：每种字符出现次数', h=300),
        dict(type='text', size=32, h=120,
             fn=lambda S: (lambda t: f"次数从大到小 `{t}`，保留前 `{S['k']}` 个 = {sum(t[:S['k']])}，删掉 ==`{len(S['s']) - sum(t[:S['k']])}`==")(sorted(S['freq'].values(), reverse=True)) if 'freq' in S and S['_line'] == 8 else ''),
    ],
    watch=[('k', 'k', 'blue'), ('char', 'char', 'yellow')],
    captions={
        'freq = {}': '先准备哈希表 `freq`，统计每种字符出现几次',
        'for char in s': '取下一个字符 `{char}`',
        'freq[char] =': '`freq[{char!r}]` 变成 =={freq[char]}==',
        'return len(s)': '保留出现次数最多的 `{k}` 种，其余全删：`{len(s)} − {sum(sorted(freq.values(), reverse=True)[:k])}` = =={ret}==',
    },
    cards=dict(
        one_liner='保留出现次数最多的 k 种字符，其余全删',
        complexity='时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
        problem=['删去一些字符，使剩下的不同字符数 `<= k`',
                 '求最少需要删掉多少个字符',
                 '本视频：`s="aabcbbd"`，`k=2` → `2`'],
        quote='题目要求删去尽量少的字符，那么就应该保留出现次数最多的k种字符，于是可以先一趟遍历，使用哈希表统计每种字符出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['一趟遍历，用哈希表数出每种字符的次数',
              '次数从大到小排序，前 `k` 个就是要保留的',
              '总长度减去保留的字符数，就是删除数'],
        summary=['时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
                 '`[:k]` 在种类数不足 k 时取全部，结果为 0',
                 '对比灵神：灵神升序排序后切掉前面的求和；yiduobo 降序取前 k 再用总长相减',
                 '原文为 Python 2 风格，无需改动即可运行'],
    ),
)
