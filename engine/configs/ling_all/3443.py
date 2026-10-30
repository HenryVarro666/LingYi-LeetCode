S0 = 'NSWWEW'
K = 3
DIR = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}


def _pos(i):
    """执行完 s[0..i] 后（不修改）的位置列表，含原点"""
    pts = [(0, 0)]
    for c in S0[:i + 1]:
        dx, dy = DIR[c]
        pts.append((pts[-1][0] + dx, pts[-1][1] + dy))
    return pts


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '不修改时走过的路径（黄 = 当前位置，灰 = 原点）', 22, T['muted'], bold=True)
    n = len(S0)
    i = S.get('i', -1)
    full = _pos(n - 1)
    xs = [p[0] for p in full]
    ys = [p[1] for p in full]
    lx, hx, ly, hy = min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1
    cell = min(110, (x1 - x0 - 60) / (hx - lx), (y1 - y0 - 90) / (hy - ly))
    ox = x0 + 30 + ((x1 - x0 - 60) - cell * (hx - lx)) / 2
    oy = y0 + 56 + ((y1 - y0 - 90) - cell * (hy - ly)) / 2

    def P(p):
        return (ox + (p[0] - lx) * cell, oy + (hy - p[1]) * cell)

    for gx in range(lx, hx + 1):
        cv.line([P((gx, ly)), P((gx, hy))], T['border'], 1)
    for gy in range(ly, hy + 1):
        cv.line([P((lx, gy)), P((hx, gy))], T['border'], 1)
    done = i
    if S.get('_line') == 9 or (S.get('_line') in (5, 6, 7, 8) and (S.get('x'), S.get('y')) == _pos(i)[-1]):
        done = i + 1
    path = _pos(done - 1) if done > 0 else [(0, 0)]
    if len(path) > 1:
        cv.line([P(p) for p in path], T['blue'], 5)
    ox_, oy_ = P((0, 0))
    cv.rect((ox_ - 9, oy_ - 9, ox_ + 9, oy_ + 9), fill=T['dim'], r=9)
    cv.text((ox_ - 14, oy_ + 12), '原点', 18, T['muted'], anchor='ra')
    cx, cy = P(path[-1])
    cv.rect((cx - 12, cy - 12, cx + 12, cy + 12), fill=T['yellow'], r=12)
    if 'x' in S and 'y' in S:
        cv.text((x1 - 24, y1 - 30), f"位置 ({S['x']}, {S['y']})  距离 |x|+|y| = {abs(S['x']) + abs(S['y'])}", 22, T['yellow'], anchor='ra', bold=True)


def _br(S, ch, what):
    if S.c == ch:
        return f'`c = {ch}` {what} → 位置 `({S.x}, {S.y})`'
    return f'`c = {S.c}` 不是 `{ch}`，看下一个分支'


def _text(S):
    if 'i' not in S or 'x' not in S or S.get('_line') != 9:
        return '每多一次修改，距离最多 ==+2==；但总距离不会超过已走的步数 `i+1`'
    a = abs(S['x']) + abs(S['y'])
    k = S['k']
    return f'`min(|x|+|y|+2k, i+1)` = `min({a} + {2 * k}, {S["i"] + 1})` = =={min(a + 2 * k, S["i"] + 1)}=='


CONFIG = dict(
    num=3443, title='K 次修改后的最大曼哈顿距离', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='模拟 + min(当前距离+2k, 步数)',
    tags=['曼哈顿距离与切比雪夫距离', '难度分 1856'],
    code='''
class Solution:
    def maxDistance(self, s: str, k: int) -> int:
        ans = x = y = 0
        for i, c in enumerate(s):
            if c == 'N': y += 1
            elif c == 'S': y -= 1
            elif c == 'E': x += 1
            else: x -= 1
            ans = max(ans, min(abs(x) + abs(y) + k * 2, i + 1))
        return ans
''',
    call=f'Solution().maxDistance({S0!r}, {K})',
    expect=6,
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前处理的字符）', h=150, cell=80, pointers={'i': 'blue'},
             color=lambda S, k, v: 'blue' if k == S.get('i') else None),
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_text, size=26, h=70),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'cyan'), ('y', 'y', 'orange'), ('k', 'k', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = x = y = 0': '`ans` 是答案，`(x, y)` 是==不修改==时的当前位置，起点原点',
        'for i, c in enumerate': lambda S, B, r: ('`s` 的字符都处理完，循环结束' if B.get('i') == S.i and 'ans' in B else f'处理第 `{S.i}` 个字符 `{S.c}`：走完它，一共走了 `{S.i + 1}` 步'),
        5: lambda S, B, r: _br(S, 'N', '向北：`y` 加 1'),
        6: lambda S, B, r: _br(S, 'S', '向南：`y` 减 1'),
        7: lambda S, B, r: _br(S, 'E', '向东：`x` 加 1'),
        8: '`W` 向西：`x` 减 1 → 位置 `({x}, {y})`',
        9: lambda S, B, r: f'每改一次，距离 ==+2==：`{abs(S.x)+abs(S.y)}+{2*S.k}`；但不会超过步数 `{S.i+1}` → 取较小 `{min(abs(S.x) + abs(S.y) + S.k * 2, S.i + 1)}`，`ans` = =={S.ans}==',
        'return ans': '所有前缀里最大的曼哈顿距离 =={ret}==',
    },
    cards=dict(
        one_liner='每修改一次距离 +2，但不会超过走过的步数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 由 `N/S/E/W` 组成，表示在网格上的移动',
                 '最多改 `k` 个字符，求过程中离原点的最大曼哈顿距离',
                 '示例：`s = "NSWWEW", k = 3` → `6`'],
        quote='所以每操作一次，曼哈顿距离都会增大 2。但这不会超过移动的次数，即 i+1。',
        quote_src='—— 灵茶山艾府题解（方法二）',
        idea=['把一步改成朝远离原点的方向，距离 `+2`（少一步反向、多一步同向）',
              '所以走完 `s[i]` 后，最远 = `min(|x|+|y| + 2k, i+1)`',
              '`i+1` 是上限：步数只有这么多，不可能走得更远'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`k` 不必一次用完：`min` 的上限 `i+1` 自动处理了改不动的情况',
                 '方法一：分别算横纵坐标，`d = min(a, b, k)`，横纵共用 `k`',
                 '同类：曼哈顿距离与切比雪夫距离题单（§7.3）'],
    ),
)
