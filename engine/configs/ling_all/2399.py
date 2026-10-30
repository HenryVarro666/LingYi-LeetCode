S0 = 'abaccb'
DIST = [1, 3, 0, 5] + [0] * 22


def _info(S):
    if 'c' not in S or 'i' not in S:
        return ''
    c, i = S['c'], S['i']
    ch = chr(c + 97)
    if S['last'][c] and S['_line'] >= 6:
        return f"字母 `{ch}`（编号 {c}）：上次位置+1 = `{S['last'][c]}`，间隔 `i − last[c]` = `{i - S['last'][c]}`，要求 `distance[{c}] = {S['distance'][c]}`"
    return f"字母 `{ch}` 编号 `{c}`，当前下标 `i = {i}`"


CONFIG = dict(
    num=2399, title='检查相同字母间的距离', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='数组记录上次出现位置',
    tags=[],
    code='''
class Solution:
    def checkDistances(self, s: str, distance: List[int]) -> bool:
        last = [0] * 26
        for i, c in enumerate(s):
            c = ord(c) - ord('a')
            if last[c] and i - last[c] != distance[c]:
                return False
            last[c] = i + 1
        return True
''',
    call=f'Solution().checkDistances({S0!r}, {DIST!r})',
    expect=True,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字母，绿 = 已记录过位置）', cell=100, h=190, pointers={'i': 'blue'},
             color=lambda S, k, v: 'green' if 'last' in S and S['last'][ord(v) - 97] and k < S.get('i', 0) else None),
        dict(type='array', var='last[:5]', label='last[0..4]（a b c d e；存 位置+1，0 = 没出现过）', cell=100, h=190,
             color=lambda S, k, v: 'pink' if 'c' in S and k == S['c'] else None),
        dict(type='text', fn=_info, size=26, h=110),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'pink'), ('last[:4]', 'last[:4]', 'green')],
    captions={
        'last = [0] * 26': '`last[c]` 记录字母 c 上次出现的位置 +1；`0` 表示还没出现过',
        'for i, c in enumerate': lambda S, B, ret: ('遍历完了，没有违反要求' if 'i' in B and S.i == B.i and S.c == B.c
                                                    else f"看 `s[{S.i}]`"),
        'c = ord(c)': '字母转成编号：`c = {c}`（a→0, b→1, c→2）',
        'if last[c] and': lambda S, B, ret: (
            f'`last[{S.c}] = 0`：第一次遇到，没法比较' if not S.last[S.c]
            else f'第二次遇到：中间字母数 `i - last[c] = {S.i} - {S.last[S.c]}` = {S.i - S.last[S.c]}，`distance[{S.c}] = {S.distance[S.c]}`，'
                 + ('==不相等 → 不是匀整串==' if S.i - S.last[S.c] != S.distance[S.c] else '相等，满足要求')),
        'return False': '有一个字母的间隔不符合，返回 `False`',
        'last[c] = i + 1': '记下位置：`last[{c}] = i + 1 = {last[c]}`（存 +1，才能用非 0 表示“出现过”）',
        'return True': '每个字母的间隔都符合，返回 `True`',
    },
    cards=dict(
        one_liner='记下每个字母上次出现的位置，再次遇到就量间隔',
        complexity='时间 `O(|Σ|+n)`，空间 `O(|Σ|)`，`|Σ| = 26`',
        problem=['`s` 中每个字母恰好出现两次，`distance[i]` 是第 i 个字母两次出现之间的==字母个数==',
                 '每个出现过的字母都要满足，才是「匀整」字符串',
                 '示例：`"abaccb"`，`distance = [1,3,0,5,…]` → `true`'],
        quote='记录 last[s[i]]=i+1，这样 last[s[i]] 是正数即表示 s[i] 出现过，此时两个字母之间的字母个数为 i-last[s[i]]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['遍历 `s`，用数组 `last` 记录每个字母上次的位置',
              '第二次遇到时：两字母间的字母数 = `i - 上次位置 - 1`',
              '存成 `i + 1`：既能用非 0 判断“出现过”，减出来的就直接是间隔'],
        result='`a`、`b`、`c` 的间隔分别是 1、3、0，全部吻合 → True ✓',
        summary=['时间 `O(|Σ|+n)`，空间 `O(|Σ|)`',
                 '易错：间隔要减 1；这里靠存 `i + 1` 抵消了',
                 '`distance` 里没出现的字母可以忽略，代码里自然不会访问到',
                 '先判断再更新 `last[c]`，顺序不能反'],
    ),
)
