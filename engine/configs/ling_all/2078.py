COLORS = [4, 4, 4, 2, 4, 3, 4, 4]


def _col(S, i, v):
    if 'c' not in S:
        return None
    n = len(S['colors'])
    if i in (0, n - 1):
        return 'blue'
    if v != S['c']:
        return 'orange'
    return None


def _txt(S):
    if 'c' not in S:
        return '蓝 = 两端（颜色都是 c）；橙 = 颜色 ≠ c 的房子'
    n = len(S['colors'])
    parts = [f'两端颜色 `c = {S["c"]}`']
    if 'r' in S:
        parts.append(f'房子 0 ↔ r：距离 `{S["r"]}`')
    if 'l' in S:
        parts.append(f'l ↔ 房子 n−1：距离 `{n - 1 - S["l"]}`')
    return '；'.join(parts)


CONFIG = dict(
    num=2078, title='两栋颜色不同且距离最远的房子', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='脑筋急转弯 · 端点必参与',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def maxDistance(self, colors: List[int]) -> int:
        n = len(colors)
        c = colors[0]
        if c != colors[-1]:
            return n - 1

        # 找最右边的颜色不等于 c 的房子
        # 题目保证至少有两栋颜色不同的房子
        r = n - 2
        while colors[r] == c:
            r -= 1

        # 找最左边的颜色不等于 c 的房子
        l = 1
        while colors[l] == c:
            l += 1

        return max(r, n - 1 - l)
''',
    call=f'Solution().maxDistance({COLORS})',
    expect=5,
    views=[
        dict(type='array', var='colors', label='colors', pointers={'l': 'green', 'r': 'pink'},
             color=_col, cell=96, h=300),
        dict(type='text', fn=_txt, size=30, h=110),
    ],
    watch=['n', ('c', 'c', 'blue'), ('l', 'l', 'green'), ('r', 'r', 'pink')],
    captions={
        'c = colors[0]': '记 `c = colors[0] = {c}`',
        'if c != colors[-1]': lambda S, B, ret: (f'两端颜色不同 → 直接选两端，距离 `n − 1`' if S.c != S.colors[-1]
                                                 else f'`colors[0] = colors[-1] = {S.c}`：两端同色，不能直接选两端'),
        'return n - 1': '两端颜色不同，答案就是最大可能距离 `{ret}`',
        'r = n - 2': '最大距离中==房子 0 或 n−1 必然参与==；对房子 0，另一栋越靠右越好，从 `r = {r}` 往左找',
        'while colors[r] == c': lambda S, B, ret: (f'`colors[{S.r}] = {S.colors[S.r]} = c`，和房子 0 同色，继续往左' if S.colors[S.r] == S.c
                                                   else f'`colors[{S.r}] = {S.colors[S.r]} ≠ c`：找到了，房子 0 和 {S.r} 距离 `{S.r}`'),
        'r -= 1': '`r` → {r}',
        'l = 1': '对房子 n−1，另一栋越靠左越好，从 `l = 1` 往右找',
        'while colors[l] == c': lambda S, B, ret: (f'`colors[{S.l}] = {S.colors[S.l]} = c`，和房子 n−1 同色，继续往右' if S.colors[S.l] == S.c
                                                   else f'`colors[{S.l}] = {S.colors[S.l]} ≠ c`：找到了，距离 `n − 1 − l = {S.n - 1 - S.l}`'),
        'l += 1': '`l` → {l}',
        'return max': '`max({r}, {n - 1 - l})` = =={ret}==',
    },
    cards=dict(
        one_liner='最远的一对里，必然有一栋是两端的房子',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`colors[i]` 是第 i 栋房子的颜色，求两栋==颜色不同==的房子的最大距离 `abs(i − j)`',
                 '示例：`[1,1,1,6,1,1,1]` → `3`；`[1,8,3,8,3]` → `4`',
                 '本视频：`[4,4,4,2,4,3,4,4]` → `5`'],
        quote='如果 colors[i] ≠ c，那么 j 必然是离 i 最远的 0 或者 n−1（这两栋房子的颜色与房子 i 不同）。这意味着，==0 或者 n−1 必然参与最大距离的计算==。',
        quote_src='—— 灵茶山艾府题解',
        idea=['两端颜色不同：答案直接是 `n − 1`',
              '两端同色 `c`：最优的一对中颜色不是 c 的那栋，配离它最远的端点',
              '房子 0 配最右的非 c 房子 `r`，房子 n−1 配最左的非 c 房子 `l`，取 `max(r, n−1−l)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`while` 不会越界：题目保证至少有两栋颜色不同的房子',
                 '关键结论：最远对一定包含端点，不必 `O(n^2)` 枚举',
                 '同类：§5.2 脑筋急转弯'],
    ),
)
