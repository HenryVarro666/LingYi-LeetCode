S0, T0 = 'leet', 'code'
NC = [1 + j % 3 for j in range(26)]
PC = [1 + (j + 1) % 2 for j in range(26)]
ALPHA = 'abcdefghijklmnopqrstuvwxyz'


def _n(c):
    return ord(c) - 97 if isinstance(c, str) else c


def _idx(S):
    """当前处理的是第几对 (s[i], t[i])：这个例子里每一对都不同，用 (x, y) 反查"""
    if 'x' not in S or 'y' not in S:
        return None
    x, y = _n(S['x']), _n(S['y'])
    for i, (a, b) in enumerate(zip(S['s'], S['t'])):
        if ord(a) - 97 == x and ord(b) - 97 == y:
            return i
    return None


def _xy(S):
    """x、y 都已经转成字母表下标时返回 (x, y)，否则 None"""
    if isinstance(S.get('x'), int) and isinstance(S.get('y'), int):
        return S['x'], S['y']
    return None


def _px(S):
    return S['x'] if isinstance(S.get('x'), int) else None


def _py(S):
    return S['y'] if isinstance(S.get('y'), int) else None


def _next_arc(S, j):
    xy = _xy(S)
    if not xy or xy[0] == xy[1]:
        return False
    x, y = xy
    return (j - x) % 26 < (y - x) % 26          # x, x+1, ..., y-1（环形）


def _prev_arc(S, j):
    xy = _xy(S)
    if not xy or xy[0] == xy[1]:
        return False
    x, y = xy
    return 0 <= (x - j) % 26 < (x - y) % 26     # x, x-1, ..., y+1（环形）


def _text(S, B):
    xy = _xy(S)
    if not xy:
        return '字母表是环：`z` 的下一个是 `a`，`a` 的上一个是 `z`。向后一步花 `nextCost`，向前一步花 `previousCost`'
    x, y = xy
    if y < x:
        return f'`y = {y} < x = {x}`：向后要==绕过 z==，把 `y` 当成 `y + 26 = {y + 26}`；向前不用绕'
    if x < y:
        return f'`x = {x} < y = {y}`：向前要==绕过 a==，把 `x` 当成 `x + 26 = {x + 26}`；向后不用绕'
    return f'`x = y = {x}`：不用切换，代价 0'


def _calc(S, B, ret):
    x, y = S.x, S.y
    yy = y + 26 if y < x else y
    xx = x + 26 if x < y else x
    a = S.nxt_sum[yy] - S.nxt_sum[x]
    b = S.pre_sum[xx] - S.pre_sum[y]
    if S.ans == B.ans:  # 这一行拆成两步：先算出两个方向的代价，再取小、累加
        return (f'向后：`nxt_sum[{yy}] − nxt_sum[{x}]` = {S.nxt_sum[yy]} − {S.nxt_sum[x]} = =={a}==；'
                f'向前：`pre_sum[{xx}] − pre_sum[{y}]` = {S.pre_sum[xx]} − {S.pre_sum[y]} = =={b}==')
    pick = '向后更省' if a < b else ('向前更省' if b < a else '一样')
    return f'`min({a}, {b})` = =={min(a, b)}==（{pick}）→ `ans` = {B.ans} + {min(a, b)} = =={S.ans}=='


CONFIG = dict(
    num=3361, title='两个字符串的切换距离', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='前缀和 · 字母表延长一倍变直线',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution:
    def shiftDistance(self, s: str, t: str, nextCost: List[int], previousCost: List[int]) -> int:
        nxt_sum = list(accumulate(nextCost + nextCost, initial=0))
        pre_sum = list(accumulate(previousCost + previousCost))  # 数组前面不加 0

        ans = 0
        ord_a = ord('a')
        for x, y in zip(s, t):
            x = ord(x) - ord_a
            y = ord(y) - ord_a
            ans += min(nxt_sum[y + 26 if y < x else y] - nxt_sum[x],
                       pre_sum[x + 26 if x < y else x] - pre_sum[y])
        return ans
''',
    setup=f'NC = {NC}\nPC = {PC}',
    call=f'Solution().shiftDistance({S0!r}, {T0!r}, NC, PC)',
    expect=56,
    views=[
        dict(type='text', fn=_text, h=80, size=24),
        dict(type='string', var='s', label='s（蓝 = 当前这一位）', cell=64, index=False,
             color=lambda S, k, v: 'blue' if k == _idx(S) else None, h=105),
        dict(type='string', var='t', label='t（粉 = 目标字母）', cell=64, index=False,
             color=lambda S, k, v: 'pink' if k == _idx(S) else None, h=105),
        dict(type='string', var=lambda S: ALPHA, label='字母表（x = 起点，y = 终点）', cell=32, index=True,
             pointers={_px: 'blue', _py: 'pink'}, pointer_labels={_px: 'x', _py: 'y'},
             color=lambda S, k, v: 'blue' if k == _px(S) else ('pink' if k == _py(S) else None), h=150),
        dict(type='array', var='nextCost', label='nextCost（绿 = 向后 x→y 要花的那一段）', cell=32,
             color=lambda S, j, v: 'green' if _next_arc(S, j) else None, h=120),
        dict(type='array', var='previousCost', label='previousCost（橙 = 向前 x→y 要花的那一段）', cell=32,
             color=lambda S, j, v: 'orange' if _prev_arc(S, j) else None, h=120),
    ],
    skip=['pre_sum[x + 26 if x < y else x] - pre_sum[y])'],
    watch=[('x', 'x', 'blue'), ('y', 'y', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'nxt_sum = ': '字母表是环 → 把 `nextCost` ==复制一份接在后面==，环就变成直线。`nxt_sum[k]` = 前 `k` 项之和，长 {len(nxt_sum)}',
        'pre_sum = ': '`previousCost` 同样延长一倍。前面==不加 0==：`pre_sum[k]` 就是前 `k+1` 项之和，所以向前的区间和是 `pre_sum[x] − pre_sum[y]`',
        'ans = 0': '`ans` 累计每一位的最小代价，各位置的操作互不影响',
        'ord_a = ': '`ord_a = 97`，用来把字母转成 0..25 的下标',
        'for x, y in zip': lambda S, B, r: (f"枚举第 {_idx(S)} 对：把 `s[{_idx(S)}] = '{S.x}'` 变成 `t[{_idx(S)}] = '{S.y}'`" if isinstance(S.x, str)
                                            else '`s`、`t` 都处理完了，退出循环'),
        'x = ord(x)': '`x` 转成字母表下标 → {x}',
        'y = ord(y)': '`y` 转成字母表下标 → {y}',
        'ans += min': _calc,
        'return ans': '每一位的最小代价加起来：`{ans}`',
    },
    cards=dict(
        one_liner='字母表延长一倍变成直线，两种方向的代价都是前缀和之差',
        complexity='时间 `O(n + |Σ|)`，空间 `O(|Σ|)`，`|Σ| = 26`',
        problem=['把 `s` 的每个字母切换成 `t` 的对应字母，求最少总代价',
                 '向后一步（`z` 后面是 `a`）花 `nextCost[j]`，向前一步花 `previousCost[j]`，`j` 是当前字母的下标',
                 '示例：`"leet"→"code"` 代价全是 1 → `31`；本视频换了代价数组 → `56`'],
        quote='考虑到字母表是环形的，可以把前缀和数组延长一倍，从而变成非环形的。',
        quote_src='—— 灵茶山艾府题解',
        idea=['预处理 `nextCost`、`previousCost` 的前缀和，区间代价 `O(1)` 查询',
              '向后：`x ≤ y` 时是 `nxt_sum[y] − nxt_sum[x]`；`x > y` 就把 `y` 变成 `y + 26`',
              '向前：`x ≥ y` 时是 `pre_sum[x] − pre_sum[y]`；`x < y` 就把 `x` 变成 `x + 26`',
              '每一位取两种方向的较小值，累加'],
        result='`s="leet"`、`t="code"`，本视频的代价数组下总代价 `56` ✓',
        summary=['时间 `O(n + |Σ|)`，空间 `O(|Σ|)`',
                 '易错：向后要绕圈用 `y + 26`，向前要绕圈用 `x + 26`，别写反',
                 '`pre_sum` 前面不加 0，所以下标不用加一；`nxt_sum` 前面加了 0（`initial=0`）',
                 '好处：字母表换成 `10^5` 那么大，每一位仍是 `O(1)`',
                 '同类：前缀和 + 环形数组展开成两倍'],
    ),
)
