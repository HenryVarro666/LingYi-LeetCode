PTS = [[1, 0], [2, 0], [3, 0], [0, 1], [2, 1], [1, 3], [2, 3], [4, 3]]


def _row(S):
    """当前正在枚举的那一行的 y（由 c 和 s 反推；循环外返回 None）"""
    cnt, c = S.get('cnt'), S.get('c')
    if cnt is None or c is None or 's' not in S:
        return None
    s, pre = S['s'], 0
    for y, cc in cnt.items():
        k = cc * (cc - 1) // 2
        if cc == c and (pre == s and S.get('_line') != 9 or pre + k == s and S.get('_line') == 9):
            return y
        pre += k
    return None


def _done_rows(S):
    cnt, cur = S.get('cnt'), _row(S)
    if cnt is None or 's' not in S:
        return set()
    if cur is None:
        return set(cnt) if S.get('_line', 0) >= 6 and 'c' in S else set()
    out = set()
    for y in cnt:
        if y == cur:
            break
        out.add(y)
    return out


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    cv.text((x0 + 18, y0 + 4), '平面上的点（每一行 = 一条水平线；黄 = 当前行，绿 = 已枚举的“左边”）', 22, T['muted'], bold=True)
    xs = [p[0] for p in PTS]
    ys = sorted({p[1] for p in PTS})
    gx0, gx1 = x0 + 150, x1 - 260
    gy0, gy1 = y0 + 70, y1 - 45
    ymin, ymax = min(ys), max(ys)
    xmin, xmax = min(xs), max(xs)

    def X(v):
        return gx0 + (v - xmin) / max(1, xmax - xmin) * (gx1 - gx0)

    def Y(v):
        return gy1 - (v - ymin) / max(1, ymax - ymin) * (gy1 - gy0)

    cur, done = _row(S), _done_rows(S)
    cnt = S.get('cnt') or {}
    for yv in ys:
        c = T['yellow'] if yv == cur else T['green'] if yv in done else T['border']
        cv.line([(gx0 - 40, Y(yv)), (gx1 + 40, Y(yv))], c, 3 if c != T['border'] else 2)
        cv.text((x0 + 30, Y(yv)), f'y = {yv}', 24, c if c != T['border'] else T['muted'], anchor='lm', bold=True)
        if yv in cnt:
            n = cnt[yv]
            cv.text((gx1 + 60, Y(yv)), f'{n} 点 → {n * (n - 1) // 2} 条边', 24,
                    c if c != T['border'] else T['muted'], anchor='lm', bold=True)
    for px, py in PTS:
        c = T['yellow'] if py == cur else T['green'] if py in done else T['blue']
        r = 13
        cv.d.ellipse((X(px) - r, Y(py) - r, X(px) + r, Y(py) + r), fill=c)


def _formula(S):
    if 'k' not in S:
        return '在同一行选 2 个点 = 一条水平边；两条==不同行==的水平边 = 一个梯形'
    return f"`ans += s × k` → 之前所有行的 `{S['s'] if S.get('_line') != 9 else S['s'] - S['k']}` 条边 × 本行 `{S['k']}` 条边"


CONFIG = dict(
    num=3623, title='统计梯形的数目 I', difficulty='Medium', category='哈希',
    author='灵茶山艾府', technique='枚举右，维护左 · 乘法原理',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def countTrapezoids(self, points: List[List[int]]) -> int:
        MOD = 1_000_000_007
        cnt = Counter(p[1] for p in points)  # 统计每一行（水平线）有多少个点
        ans = s = 0
        for c in cnt.values():
            k = c * (c - 1) // 2
            ans += s * k
            s += k
        return ans % MOD
''',
    call=f'Solution().countTrapezoids({PTS})',
    expect=15,
    views=[
        dict(type='custom', draw=_draw, h=420),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='map', var='cnt', label='cnt：行号 y → 这一行的点数', h=130, fmt=lambda k, v: f'y={k}: {v}'),
    ],
    watch=['c', ('k', 'k', 'yellow'), ('s', 's', 'green'), ('ans', 'ans', 'pink')],
    captions={
        'MOD = ': '答案对 `10^9+7` 取模（最后再取，Python 不会溢出）',
        'cnt = Counter': '只关心纵坐标：`cnt = {dict(cnt)}`',
        'ans = s = 0': '`s` = 之前遍历过的行一共有多少条水平边（==维护左==）',
        'for c in cnt.values()': lambda S, B, r: ('所有行都枚举完毕 → 结束循环' if S.s == sum(v * (v - 1) // 2 for v in S.cnt.values())
                                                  else f'枚举下一行（==枚举右==）：这一行有 `c = {S.c}` 个点'),
        'k = c * (c - 1) // 2': '从 {c} 个点里选 2 个：`k = {c}×{c-1}/2` = =={k}== 条水平边',
        'ans += s * k': '本行的边当顶边、之前行的边当底边：`{B.s} × {k}` = {B.s * k} 个梯形，`ans` = =={ans}==',
        's += k': '本行的 {k} 条边加入“左边”：`s` = =={s}==',
        'return ans % MOD': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='每行选 2 点成一条水平边；两条不同行的边配成一个梯形',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['给 `n` 个互不相同的点 `points[i] = [x, y]`',
                 '==水平梯形==：至少有一对边平行于 x 轴的凸四边形',
                 '统计任选 4 点能组成多少个水平梯形，对 `10^9+7` 取模',
                 '示例：`[[1,0],[2,0],[3,0],[2,2],[3,2]]` → `3`；本视频 8 个点 → `15`'],
        quote='枚举每一行，设这一行有 k 条水平边，那么另外一条边就是==之前遍历过的行的边数 s==。根据乘法原理，一共可以组成 s·k 个水平梯形。⚠另外一条边不能是其余所有行，这会导致重复计算。',
        quote_src='—— 灵茶山艾府题解',
        idea=['一行有 `c` 个点 → `c(c-1)/2` 条水平边（顶边或底边）',
              '枚举右（当前行），维护左（之前所有行的边数 `s`）：`ans += s * k`',
              '只和==之前的行==配对，每对行恰好算一次，不会重复'],
        summary=['时间 `O(n)`，空间 `O(n)`（哈希表）',
                 '易错：和“其余所有行”配对会把每个梯形==算两次==',
                 '最坏答案约 `n^4/64 ≈ 1.6×10^18`，不超过 64 位，循环中无需取模（Java/C++ 要用 long）',
                 '同类模板：枚举右维护左，如 1. 两数之和、两两配对计数'],
    ),
)
