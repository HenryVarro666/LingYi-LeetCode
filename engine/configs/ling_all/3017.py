def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    n, x, y = S.get('n'), S.get('x'), S.get('y')
    if n is None or x is None or y is None:
        return
    cv.text((x0 + 18, y0 + 4), '街道：1~n 连成一条线，x 与 y 之间多一条捷径', 24, T['muted'], bold=True)
    L, R = x0 + 60, x1 - 60
    cy = y0 + 150
    step = (R - L) / max(1, n - 1)

    def X(h):
        return L + (h - 1) * step
    cv.line([(X(1), cy), (X(n), cy)], T['border'], 3)
    if x < y:
        mid = (X(x) + X(y)) / 2
        cv.line([(X(x), cy - 6), (X(x), cy - 60), (X(y), cy - 60), (X(y), cy - 6)], T['purple'], 4)
        cv.text((mid, cy - 66), '捷径', 20, T['purple'], anchor='mb', bold=True)
    i = S.get('i') if S.get('_line') is not None else None
    for h in range(1, n + 1):
        c = T['yellow'] if h == i else (T['purple'] if h in (x, y) else (125, 133, 145))
        cv.circle((X(h), cy), 22, fill=c) if hasattr(cv, 'circle') else cv.rect((X(h) - 22, cy - 22, X(h) + 22, cy + 22), fill=c, r=22)
        cv.text((X(h), cy), h, 24, T['bg'], anchor='mm', bold=True)


def _top(S):
    if 'i' not in S:
        return '先让 `x < y`；若 `x + 1 >= y`，捷径没用，答案是 `2(n−i)`'
    i, x, y = S['i'], S['x'], S['y']
    if i <= x:
        return f'`i = {i} ≤ x`：房子 i 在捷径左边，右边的房子分三段到达'
    if i < (x + y) // 2:
        return f'`x < i = {i} < (x+y)//2`：i 在环里偏左，同样分三段'
    return f'`i = {i}` 偏右：它到右侧房子不用捷径，直接 `[1, n−i]`'


CONFIG = dict(
    num=3017, title='按距离统计房屋对数目 II', difficulty='Hard', category='常用数据结构',
    author='灵茶山艾府', technique='分类讨论 · 差分数组',
    tags=['常用数据结构', '贪心与思维', '难度分 2709'],
    code='''
class Solution:
    def countOfPairs(self, n: int, x: int, y: int) -> List[int]:
        if x > y:
            x, y = y, x

        if x + 1 >= y:
            return list(range((n - 1) * 2, -1, -2))

        diff = [0] * (n + 1)

        def add(l: int, r: int) -> None:
            diff[l] += 2
            diff[r + 1] -= 2

        for i in range(1, n):
            if i <= x:
                k = (x + y + 1) // 2
                add(1, k - i)
                add(x - i + 2, x - i + y - k)
                add(x - i + 1, x - i + 1 + n - y)
            elif i < (x + y) // 2:
                k = i + (y - x + 1) // 2
                add(1, k - i)
                add(i - x + 2, i - x + y - k)
                add(i - x + 1, i - x + 1 + n - y)
            else:
                add(1, n - i)

        return list(accumulate(diff))[1:]
''',
    call='Solution().countOfPairs(7, 2, 6)',
    expect=[14, 18, 10, 0, 0, 0, 0],
    views=[
        dict(type='text', fn=_top, size=24, h=80),
        dict(type='custom', draw=_draw, h=250),
        dict(type='array', var='diff', pointers={'l': 'blue', 'r': 'pink'}, label='diff（差分数组，下标 = 距离）',
             color=lambda S, i, v: 'yellow' if S.get('l') is not None and S.get('r') is not None and S['l'] <= i <= S['r'] else None, h=170),
    ],
    watch=[('i', 'i', 'yellow'), 'k', ('l', 'l', 'blue'), ('r', 'r', 'pink')],
    captions={
        'if x > y': '保证 `x < y`，两者对称，交换不影响答案',
        'if x + 1 >= y': lambda S, B, r: (f'`x + 1 >= y`（{S.x}+1 vs {S.y}）：捷径不比原路更短' if S.x + 1 >= S.y else f'`{S.x} + 1 < {S.y}`：捷径能缩短距离，需要分类讨论'),
        'return list(range': '没有有效捷径：距离 d 的房屋对共 `2(n-d)` 个',
        'diff = [0]': '差分数组：`diff[d]` 最终累加成距离为 d 的房屋对数',
        'diff[l] += 2': lambda S, B, r: (f'区间 `[{S.l}, {S.r}]` 是空区间，下面两步会互相抵消' if S.l > S.r else f'区间 `[{S.l}, {S.r}]` 内每个距离多一对（有序对共 2 个）：`diff[{S.l}] += 2`'),
        'diff[r + 1] -= 2': lambda S, B, r: ('`diff[{0}] -= 2`：抵消刚才多加的，空区间不变'.format(S.r + 1) if S.l > S.r else f'区间右端的下一格抵消：`diff[{S.r+1}] -= 2`'),
        'if i <= x': lambda S, B, r: (f'`{S.i} <= {S.x}` → 成立：i 在捷径左端点或其左侧' if S.i <= S.x else f'`{S.i} <= {S.x}` 不成立'),
        'elif i < (x + y)': lambda S, B, r: (f'`{S.i} < {(S.x+S.y)//2}` → 成立：i 在环内偏左' if S.i < (S.x + S.y) // 2 else f'`{S.i} < {(S.x+S.y)//2}` 不成立：i 偏右，右边房子走原路更近'),
        'k = (x + y + 1)': '`k = {k}`：编号 `[i+1, k]` 的房子直接走过去更近，`k` 之后的走捷径更近',
        'k = i + (y': '`k = {k}`：编号 `[i+1, k]` 直接走更近，之后的绕捷径更近',
        'add(1, k - i)': '房子 `[i+1, k]`：距离是 `1 ~ {k-i}`，各 +1',
        'add(x - i + 2, x - i + y - k)': '房子 `[k+1, y-1]`：经捷径到 y 再回头，距离 `{x-i+2} ~ {x-i+y-k}`',
        'add(i - x + 2, i - x + y - k)': '房子 `[k+1, y-1]`：经捷径到 y 再回头，距离 `{i-x+2} ~ {i-x+y-k}`',
        'add(x - i + 1, x - i + 1 + n - y)': '房子 `[y, n]`：先到 x，过捷径到 y，距离 `{x-i+1} ~ {x-i+1+n-y}`',
        'add(i - x + 1, i - x + 1 + n - y)': '房子 `[y, n]`：先到 x，过捷径到 y，距离 `{i-x+1} ~ {i-x+1+n-y}`',
        'add(1, n - i)': '捷径帮不上忙：右侧房子距离 `1 ~ {n-i}`',
        'return list(accumulate': '对差分数组求前缀和，丢掉下标 0：每个距离的房屋对数 `{ret}`',
    },
    cards=dict(
        one_liner='只数 i<j，按位置分类，每类变成差分区间',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['房屋 `1..n` 排成一条线相邻相连，另有一条街连接 `x` 和 `y`',
                 '对每个 `k`，求最短距离恰为 `k` 的房屋对 `(a, b)` 个数（有序对）',
                 '示例：`n=5, x=2, y=4` → `[10,8,2,0,0]`'],
        quote='题目说 (i,j) 和 (j,i) 这两个房屋对我们都要统计，我们也可以只统计 i<j 的房屋对，最后把答案乘 2。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['固定 `i`，右边房子的距离是一段段连续整数：每段用差分数组 `+1`',
              '`i ≤ x`：分三段（直接走 / 绕捷径回头 / 越过 y），分界点 `k = (x+y+1)//2`',
              '`x < i < (x+y)//2` 同理，`i` 更靠右就不用捷径；差分里直接加 2 代替最后乘 2'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '先 `x ≤ y`；`x+1 ≥ y` 时捷径无效，直接返回 `2(n-i)`',
                 '易错点：三段区间的端点推导（`k`、`x-i+2`、`x-i+1`）要和房屋编号严格对应',
                 '灵神还给了方法一：对每个 i 先加原距离再撤销、重加，利用对称性处理右半边，更绕但同样 `O(n)`'],
    ),
)
