CONFIG = dict(
    num=3706, title='不同单词间的最大距离 II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='先看两端，再扫中间',
    tags=[],
    code='''
class Solution(object):
    def maxDistance(self, words):
        
        if words[0] != words[-1]:
            return len(words)
        
        res = 0
        for index in range(1, len(words) - 1):
            if words[index] != words[0]:
                res = max(res, index + 1, len(words) - index)
        
        return res
''',
    call="Solution().maxDistance(['a','a','b','a','a','a'])",
    expect=4,
    views=[
        dict(type='array', var='words', label='words（距离 = 下标差 + 1）', cell=100, h=230,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if S.get('index') == i else None),
        dict(type='text', h=90, size=30,
             fn=lambda S: (f"`index = {S['index']}`：和两端不同时，距离 `max({S['index']+1}, {len(S['words'])-S['index']})`" if 'index' in S and S['words'][S['index']] != S['words'][0] else '')),
    ],
    watch=['index', ('res', 'res', 'green')],
    captions={
        'if words[0] != words[-1]': '两端是否不同：`{words[0]!r}` vs `{words[-1]!r}` → ' + '{"不同，整个数组就是最远一对" if words[0] != words[-1] else "相同，答案只能靠中间的元素"}',
        'return len(words)': '两端不同，距离为 `len(words) = {ret}`，不可能更大',
        'res = 0': '两端相同：先假设没有不同的元素，`res = 0`',
        'for index': '检查中间元素 `index = {index}`：`{words[index]!r}`',
        'if words[index] != words[0]': '`{words[index]!r}` 与两端 `{words[0]!r}` ' + '{"不同 → 它可以和某一端配对" if words[index] != words[0] else "相同，无法产生距离"}',
        'res = max': '它与左端距离 `{index}+1`，与右端距离 `{len(words)}−{index}`，取大的更新 → `res` = =={res}==',
        'return res': '返回 `{res}`；全部相同时就是 0',
    },
    cards=dict(
        one_liner='两端不同就是整段；两端相同，就找中间一个和两端都不同的元素',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串数组 `words`，求两个不同单词下标之差 `+1` 的最大值',
                 '所有单词都相同则返回 `0`；长度可达 `10^5`',
                 '本视频：`[a,a,b,a,a,a]` → `4`'],
        quote='可以直接照搬之前3696题的处理方法，先检测两端的字符串是否相同，若是，再检测中部是否存在不同与两端的字符串。',
        quote_src='—— yiduobo 题解原文',
        idea=['两端不同：首尾配对，距离 `len(words)`，已是最大',
              '两端相同：任何最远的不同对必有一端在数组端点，另一端是中间不同的元素',
              '中间元素 `index` 与左端距离 `index+1`，与右端距离 `n-index`，取较大值'],
        summary=['时间 `O(n)`，空间 `O(1)`，比暴力 `O(n^2)` 快得多',
                 '两端相同时，中间不同的元素对两端都不同，所以两种距离都要比',
                 '全部相同则 `res` 保持 0',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改；题面库里缺失，按文章与题意撰写'],
    ),
)
