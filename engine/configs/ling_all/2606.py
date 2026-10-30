def _txt(S):
    if 'c' not in S or S.get('_line') not in (6, 7):
        return '`f` = 以当前字符结尾的最大子数组和；字母先换成价值（红 = 负，绿 = 正）'
    return f'字符 `{S["c"]}` 价值 `{_val(S, S["c"])}`；`f = max(f_旧, 0) + 价值` = =={S["f"]}==，`ans` = =={S["ans"]}=='


def _val(S, ch):
    return S['mapping'].get(ch, ord(ch) - 96)


CONFIG = dict(
    num=2606, title='找到最大开销的子字符串', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='最大子数组和',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1422'],
    code='''
class Solution:
    def maximumCostSubstring(self, s: str, chars: str, vals: List[int]) -> int:
        mapping = dict(zip(chars, vals))
        ans = f = 0
        for c in s:
            f = max(f, 0) + mapping.get(c, ord(c) - ord('a') + 1)
            ans = max(ans, f)
        return ans
''',
    call="Solution().maximumCostSubstring('abdaab', 'd', [-5])",
    expect=4,
    views=[
        dict(type='string', var='s', label='s（红 = 价值为负，绿 = 价值为正）', h=190, cell=90,
             color=lambda S, i, v: ('red' if _val(S, v) < 0 else 'green') if 'mapping' in S else None),
        dict(type='map', var='mapping', label='mapping（chars 里字符的特殊价值）', h=110, fmt=lambda k, v: f'{k}: {v}'),
        dict(type='text', fn=_txt, size=26, h=80),
    ],
    watch=['c', ('f', 'f', 'blue'), ('ans', 'ans', 'green')],
    captions={
        'mapping = dict': '`mapping = {mapping}`：不在里面的字母，价值是字母表位置',
        'ans = f = 0': '`ans = f = 0`：空串开销为 0，所以答案至少是 0',
        'for c in s': '轮到字符 `{c}`，价值 `{mapping.get(c, ord(c) - 96)}`',
        'f = max': lambda S, B, r: f"`f = max({B.f}, 0) + {S.mapping.get(S.c, ord(S.c) - 96)}` = =={S.f}==：" + ('前面和为负，==不接==，从当前字符重新开始' if B.f < 0 else '前面和不为负，==接上=='),
        'ans = max': '`ans = max({B.ans}, {f}) = {ans}`',
        'return ans': '最大开销 = =={ret}==',
    },
    cards=dict(
        one_liner='字母换成数字，就是最大子数组和',
        complexity='时间 `O(n+|Σ|)`，空间 `O(|Σ|)`',
        problem=['每个字母有价值：不在 `chars` 里就是字母表位置，否则取 `vals`',
                 '子串开销 = 价值之和，空串为 0，求最大开销',
                 '示例：`s="adaa", chars="d", vals=[-1000]` → `2`'],
        quote='题目相当于求 a 的 53. 最大子数组和（允许子数组为空）。定义 f[i] 为以 a[i] 结尾的最大子数组和，考虑是否接在以 a[i-1] 结尾的最大子数组之后。',
        quote_src='—— 灵茶山艾府题解',
        idea=['接：`f[i] = f[i-1] + a[i]`；不接：`f[i] = a[i]`',
              '合并成 `f[i] = max(f[i-1], 0) + a[i]`，答案取 `max(f)`',
              '`f` 只依赖前一个，用一个变量滚动即可'],
        summary=['时间 `O(n+|Σ|)`，空间 `O(|Σ|)`',
                 '`ans` 初值 0，对应允许空子串',
                 '另有写法二：先建 26 个字母的完整映射表，再套同样的 DP'],
    ),
)
