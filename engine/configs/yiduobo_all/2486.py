def _idx(s, t, k):
    out, p = [], 0
    for i, ch in enumerate(s):
        if p < k and ch == t[p]:
            out.append(i)
            p += 1
    return out


def _s_color(S, i, v):
    if 'p' not in S:
        return None
    return 'green' if i in _idx(S['s'], S['t'], S['p']) else None


def _top(S):
    if 'n' not in S:
        return ''
    p, n, t = S['p'], S['n'], S['t']
    if p >= n:
        return f'`p = {p} = len(t)`：t 已被完整匹配'
    s = f"t 的前缀已匹配 =={p}== 个，p 指向 `t[{p}] = {t[p]}`"
    if 'char' in S and S['_line'] >= 7:
        s += f"；当前扫到 `{S['char']}`"
    return s


def _if(S, B, ret):
    char, t, p, n = S.char, S.t, S.p, S.n
    if p >= n:
        return f'`p = {p} 已不小于 n = {n}` → t 已匹配完，后面的字母都不用管'
    if t[p] == char:
        return f"`p < n` 且 `t[{p}] = {t[p]}` == `{char}` → ==匹配上了=="
    return f"`t[{p}] = {t[p]}` ≠ `{char}` → 跳过这个字母"


CONFIG = dict(
    num=2486, title='追加字符以获得子序列', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='贪心匹配 t 的前缀',
    tags=['灵神题单', '难度分 1363'],
    code='''
class Solution(object):
    def appendCharacters(self, s, t):
        
        p = 0
        n = len(t)
        for char in s:
            if p < n and t[p] == char:
                p += 1
        
        return n - p
''',
    call="Solution().appendCharacters('coaching', 'coding')",
    expect=4,
    views=[
        dict(type='text', fn=_top, h=60),
        dict(type='string', var='s', color=_s_color, label='s（绿 = 匹配上 t 前缀的字母）', h=180),
        dict(type='string', var='t', pointers={'p': 'blue'}, color=lambda S, i, v: 'green' if 'p' in S and i < S['p'] else None,
             dim=lambda S, i, v: False, label='t（箭头 p = 下一个需要匹配的字符）', h=200),
    ],
    watch=[('p', 'p', 'blue'), 'n', 'char'],
    captions={
        'p = 0': '`p` 记录下一个需要匹配的字符是 `t[p]`',
        'n = len(t)': '`n = {n}`：t 的长度',
        'for char in s': '对 s 一趟遍历，看它的子序列最多能匹配 t 的多长前缀',
        'if p < n': _if,
        'p += 1': '`p` 后移一位 → {p}',
        'return n - p': 't 里还剩 `n - p = {n} − {p}` = =={n - p}== 个字符没匹配，把它们补在 s 末尾',
    },
    cards=dict(
        one_liner='s 的子序列能吃掉 t 的前缀，剩下的补上就行',
        complexity='时间 `O(n+m)`，空间 `O(1)`',
        problem=['字符串 `s`、`t`，每次只能往 `s` 的末尾添字符',
                 '要让 `t` 变成 `s` 的子序列，最少加几个',
                 '示例：`s = coaching`，`t = coding` → `4`'],
        quote='由于只能在s的末尾添加字符，那么实际上要求的就是s的子序列能匹配t的前缀最大值，这是一个经典的贪心问题。',
        quote_src='—— yiduobo 题解原文',
        idea=['只能往末尾加 → 求 ==s 的子序列最多匹配 t 的几个前缀字符==',
              '遍历 s，用 `p` 记录 t 里下一个要匹配的位置，相等就后移',
              '遍历完，t 里 `p` 之后的字符就是要补的，答案 `n - p`'],
        summary=['时间 `O(len(s)+len(t))`，空间 `O(1)`',
                 '判断里先写 `p < n`，t 匹配完后不会访问 `t[p]` 越界',
                 '本例 `coding` 只匹配到 `co`，`d` 在 s 里找不到，所以补 4 个',
                 '原文为 Python 2 风格，本题无需改动，直接可在 Python 3 运行'],
    ),
)
