def _bin(x):
    return format(x, 'b')


def _info(S):
    if 'x' not in S or 'l' not in S:
        return '要找的是值 `second ^ first` 的子串；0 ≤ 10^9 < 2^30，所以子串长度只看 30 位以内'
    if S.get('_line') in (12, 13, 14):
        return f"从 `l = {S['l']}` 开头的子串 `s[{S['l']}..{S['r']}]`：x = `{_bin(S['x'])}` = =={S['x']}=="
    return f"枚举左端点 `l = {S['l']}`，`s[l] = '{S['c']}'`"


def _ans(S):
    if S.get('_line') == 17:
        m, qs = S['m'], S['queries']
        return '；'.join(f"`{a}^{b}={a ^ b}` → {m.get(a ^ b, (-1, -1))}" for a, b in qs)
    return ''


CONFIG = dict(
    num=2564, title='子字符串异或查询', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='预处理 30 位以内子串 · 哈希表',
    tags=['灵神题单', '位运算', '难度分 1959'],
    code='''
class Solution:
    def substringXorQueries(self, s: str, queries: List[List[int]]) -> List[List[int]]:
        n, m = len(s), {}
        if (i := s.find('0')) >= 0:
            m[0] = (i, i)

        for l, c in enumerate(s):
            if c == '0':
                continue
            x = 0
            for r in range(l, min(l + 30, n)):
                x = (x << 1) | (ord(s[r]) & 1)
                if x not in m:
                    m[x] = (l, r)

        NOT_FOUND = (-1, -1)
        return [m.get(x ^ y, NOT_FOUND) for x, y in queries]
''',
    call='Solution().substringXorQueries("1011", [[0,5],[1,2],[4,4],[0,8]])',
    expect=[(0, 2), (2, 3), (1, 1), (-1, -1)],
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='string', var='s', h=190, pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), label='s'),
        dict(type='map', var='m', h=300, fmt=lambda k, v: f'{_bin(k)} = {k}  →  {v}', label='m：子串的值 → (最早 left, right)'),
        dict(type='text', fn=_ans, size=24, h=60),
    ],
    watch=['l', 'r', ('x', 'x', 'yellow'), 'i'],
    captions={
        "s.find('0')": '先处理 0：`s` 里第一个 `0` 在下标 `{i}`（没有则 `i = -1`）',
        'm[0] =': '值 0 只需记第一个 `0` 的位置：`m[0] = ({i}, {i})`，这样下面只枚举以 `1` 开头的子串',
        'for l, c in enumerate': lambda S, B, r: ('每个左端点都枚举完了，预处理结束' if B.get('l') == S.l and 'l' in B else f"枚举左端点 `l = {S.l}`，`s[l] = {S.c!r}`"),
        "if c == '0'": lambda S, B, r: (f"`s[{S.l}] = '0'` → 值 0 已经记过，不用再枚举这个起点，`continue`" if S.c == '0' else f"`s[{S.l}] = '1'` → 以 1 开头，往右枚举子串"),
        'x = 0': '从 `l = {l}` 重新开始累计子串的值，`x = 0`',
        'for r in range': lambda S, B, r: ('右端点到头了，这个起点结束' if B.get('r') == S.r and B.get('x') != 0 else f"右端点 `r = {S.r}`：最多看 `min(l+30, n)` 位，因为 `10^9 < 2^30`"),
        'x = (x << 1)': lambda S, B, r: f"`x` 左移一位再接上 `s[{S.r}]`：`{B.get('x')}` → =={S.x}==（二进制 {_bin(S.x)}）",
        'if x not in m': lambda S, B, r: (f'`x = {S.x}` 还不在 `m` 里 → 这是它第一次出现（`l` 最小）' if S.x not in S.m else f'`x = {S.x}` 已经记过，保留更早的 `left`，不更新'),
        'm[x] = (l, r)': '记下 `m[{x}] = ({l}, {r})`：值 `{x}` 对应的子串是 `s[{l}..{r}]`',
        16: '找不到时的答案 `(-1, -1)`',
        17: '`val ^ first = second` 两边异或 `first` → `val = first ^ second`；每个查询 `O(1)` 查表 → =={ret}==',
    },
    skip=[],
    max_steps=75,
    cards=dict(
        one_liner='val = first ^ second，预处理 30 位内的子串，查表',
        complexity='时间 `O(n log U + q)`，空间 `O(n log U)`',
        problem=['二进制串 `s`，每个查询 `[first, second]`：找最短子串，使其十进制值 `val` 满足 `val ^ first == second`',
                 '多个答案取 `left` 最小的；找不到返回 `[-1, -1]`',
                 '示例：`s="101101", [[0,5],[1,2]]` → `[[0,2],[2,3]]`；本视频 `s="1011"`'],
        quote='把等式 val ⊕ first = second 两边同时异或 first，得到 val = second ⊕ first，所以问题等价于在 s 中找到值为 second ⊕ first 的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['异或两边同时异或 `first`：==`val = first ^ second`==，查询变成“找一个数”',
              '`10^9 < 2^30`：只需预处理长度 ≤ 30 的子串，记每个值第一次出现的 `(l, r)`',
              '`0` 单独处理：记第一个 `0`，其余只枚举以 `1` 开头的子串，更快'],
        summary=['时间 `O(n log U + q)`，空间 `O(n log U)`，`U` 是查询值的上限',
                 '易错：`x not in m` 才记录，保证 `left` 最小',
                 '以 `0` 开头的子串不用枚举：单独记 `m[0]`；前导零只会让子串更长',
                 '`ord(s[r]) & 1` 把字符 `0/1` 转成数字 0/1',
                 '同类：把“查询条件”先化简成“找某个值”，再哈希预处理'],
    ),
)
