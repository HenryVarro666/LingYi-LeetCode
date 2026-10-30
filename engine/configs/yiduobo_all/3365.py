S0, T0, K0 = 'aabbccbbaacc', 'bbaaccaabbcc', 6
L0 = len(S0) // K0
PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'orange']


def _blk(S, i, v):
    return PAL[(i // L0) % 6]


CONFIG = dict(
    num=3365, title='重排子字符串以形成目标字符串', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='切成 k 块 · 排序比较',
    tags=['灵神题单', '贪心与思维', '难度分 1514'],
    code='''
class Solution(object):
    def isPossibleToRearrange(self, s, t, k):
        
        n = len(s)
        length = n // k

        parts_s = []
        parts_t = []
        for index in range(k):
            parts_s.append(s[index * length : (index + 1) * length])
            parts_t.append(t[index * length : (index + 1) * length])
        
        return sorted(parts_s) == sorted(parts_t)
''',
    call=f'Solution().isPossibleToRearrange("{S0}", "{T0}", {K0})',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（同色 = 同一块）', color=_blk, cell=60),
        dict(type='string', var='t', label='t', color=_blk, cell=60),
        dict(type='array', var='parts_s', label='parts_s', cell=100),
        dict(type='array', var='parts_t', label='parts_t', cell=100),
    ],
    watch=['n', ('length', 'length', 'blue'), ('index', 'index', 'pink')],
    captions={
        'length = n // k': '块数固定为 `k`，所以每块长 `length = {n} // {k} = {length}`',
        'parts_s = []': '`parts_s` 用来装 s 切出来的 k 个子串',
        'parts_t = []': '`parts_t` 装 t 切出来的子串',
        'for index in range(k)': lambda S, B, r: (f"切第 `{S.index}` 块：下标 `{S.index * S.length}` 到 `{(S.index + 1) * S.length - 1}`" if S.index != B.get('index') or 'index' not in B else '`k` 块都切完了'),
        'parts_s.append': 's 的第 `{index}` 块 `"{parts_s[-1]}"` 放进 `parts_s`',
        'parts_t.append': 't 的第 `{index}` 块 `"{parts_t[-1]}"` 放进 `parts_t`',
        'return': '把块当成整数一样==排序再比较==：`{sorted(parts_s)}` 对 `{sorted(parts_t)}` → `{ret}`',
    },
    cards=dict(
        one_liner='把子串当成数组元素：重排能否相等，排序一比就知道',
        complexity='时间 `O(n log k)`，空间 `O(n)`',
        problem=['`s` 与 `t` 互为字母异位词，能否把 `s` 切成 `k` 个等长子串，重排后拼成 `t`',
                 '示例：`s = "abcd"`，`t = "cdab"`，`k = 2` → `true`',
                 '本视频：`k = 6`，每块长 2'],
        quote='如果给出的是两个长度为k的整数数组，问能否将第一个数组重新排列后变为第二个数组，对于这个问题使用排序或者哈希表就可以轻松解决。',
        quote_src='—— yiduobo 题解原文',
        idea=['长度相同 → 切法唯一：每 `n // k` 个字符一块',
              't 也按同样位置切成 k 块，问题变成两个“块数组”能否重排相等',
              '把块当独立元素，排序后逐个比较即可'],
        result='排序后两边都是 `["aa","aa","bb","bb","cc","cc"]` → True ✓',
        summary=['时间 `O(n log k)`，空间 `O(n)`',
                 '易错：块长是 `n // k`，不是 `k`',
                 '也可以用哈希表计数代替排序',
                 '对比灵神：灵神用 `Counter` 统计块，这里先切成列表再排序'],
    ),
)
