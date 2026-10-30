M0 = [[1, 0, 1], [2, 2, 1], [3, 0, 0], [5, 2, 2], [6, 0, 2], [8, 1, 0], [9, 2, 0]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    moles = S['moles']
    n = len(moles)
    f = S.get('f') or [0] * n
    i, j, p = S.get('i'), S.get('j'), S.get('p')
    # 左：3x3 地图
    cs = 96
    mx, my = x0 + 20, y0 + 60
    cv.text((x0 + 20, y0 + 4), '3×3 地图（锤子起点 (1,1)）', 22, T['muted'], bold=True)
    for a in range(3):
        for b in range(3):
            X, Y = mx + b * cs, my + a * cs
            fill = (52, 58, 70)
            if (a, b) == (1, 1):
                fill = (66, 74, 90)
            cv.rect((X + 3, Y + 3, X + cs - 3, Y + cs - 3), fill=fill, r=10)
            cv.text((X + 8, Y + 6), f'({a},{b})', 16, T['dim'], mono=True)
    if i is not None and 0 <= i < n:
        t, a, b = moles[i]
        cx, cy = mx + b * cs + cs / 2, my + a * cs + cs / 2
        cv.rect((mx + b * cs + 3, my + a * cs + 3, mx + b * cs + cs - 3, my + a * cs + cs - 3), outline=T['blue'], width=5, r=10)
        cv.text((cx, cy + 6), f'#{i}', 30, T['blue'], anchor='mm', bold=True)
        if j is not None and 0 <= j < i and S.get('_line', 0) >= 20:
            tj, aj, bj = moles[j]
            cv.rect((mx + bj * cs + 3, my + aj * cs + 3, mx + bj * cs + cs - 3, my + aj * cs + cs - 3), outline=T['pink'], width=5, r=10)
            cv.text((mx + bj * cs + cs / 2, my + aj * cs + cs / 2 + 30), f'#{j}', 24, T['pink'], anchor='mm', bold=True)
            cv.arrow((mx + bj * cs + cs / 2, my + aj * cs + cs / 2), (cx, cy), T['pink'], 3)
    # 右：地鼠列表
    lx = mx + 3 * cs + 40
    cv.text((lx, y0 + 4), '地鼠（按时间排序）', 22, T['muted'], bold=True)
    for r, c in enumerate(['#', '时间', '位置', 'f']):
        cv.text((lx + [10, 70, 170, 290][r], y0 + 44), c, 20, T['dim'], bold=True)
    rh = min(54, (y1 - y0 - 112) / n)
    for k, (t, a, b) in enumerate(moles):
        y = y0 + 82 + k * rh
        col = T['blue'] if k == i else (T['pink'] if k == j and S.get('_line', 0) >= 20 else None)
        if p is not None and k == p:
            cv.rect((lx - 6, y, lx + 340, y + rh - 4), outline=T['cyan'], width=2, r=6)
        elif col:
            cv.rect((lx - 6, y, lx + 340, y + rh - 4), outline=col, width=3, r=6)
        fg = col or T['text']
        cv.text((lx + 10, y + rh / 2 - 2), k, 22, fg, anchor='lm', bold=True, mono=True)
        cv.text((lx + 70, y + rh / 2 - 2), f't={t}', 22, fg, anchor='lm', mono=True)
        cv.text((lx + 170, y + rh / 2 - 2), f'({a},{b})', 22, fg, anchor='lm', mono=True)
        done = k <= (i if i is not None else -1)
        cv.text((lx + 290, y + rh / 2 - 2), f[k] if done else '·', 24, T['green'] if done and f[k] > 0 else T['muted'], anchor='lm', bold=True, mono=True)
    if p is not None and 0 <= p < n:
        cv.text((lx + 360, y0 + 82 + p * rh + rh / 2 - 2), '← p', 20, T['cyan'], anchor='lm', bold=True)


def _info(S):
    i = S.get('i')
    if i is None:
        return '`f[i]` = 一定要打第 `i` 只时，最多能打到几只（0 = 打不到）'
    t, x, y = S['moles'][i]
    return f'第 {i} 只：时间 `t={t}`，位置 `({x},{y})`；`p={S.get("p")}`，`ma={S.get("ma")}`'


CONFIG = dict(
    num='LCP 57', title='打地鼠', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='按时间 DP + 4 秒窗口优化',
    tags=[],
    code='''
class Solution(object):
    def getMaximumNumber(self, moles):

        n = len(moles)
        moles.sort(key=lambda d:d[0])
        f = [0] * n
        p = 0
        ma = 0
        for i in range(n):
            t, x, y = moles[i]
            while t - moles[p][0] >= 4:
                ma = max(ma, f[p])
                p += 1
                
            if p > 0:
                f[i] = ma + 1
            elif abs(x - 1) + abs(y - 1) <= t:
                f[i] = 1

            for j in range(i - 1, p - 1, -1):
                if f[j] > 0 and abs(x - moles[j][1]) + abs(y - moles[j][2]) <= t - moles[j][0]:
                    f[i] = max(f[i], f[j] + 1)

        return max(f)
''',
    call=f'Solution().getMaximumNumber({M0!r})',
    expect=4,
    views=[
        dict(type='text', fn=_info, size=24, h=60),
        dict(type='custom', draw=_draw, h=470),
    ],
    watch=[('i', lambda S: S.get('i', ''), 'blue'), ('j', lambda S: S.get('j', ''), 'pink'),
           ('p', lambda S: S.get('p', ''), 'cyan'), ('ma', lambda S: S.get('ma', ''), 'orange'),
           ('f[i]', lambda S: S['f'][S['i']] if 'f' in S and 'i' in S else '', 'green')],
    captions={
        'moles.sort': '地鼠按出现时间从小到大排序：时间顺序就是 DP 的顺序',
        'f = [0] * n': '`f[i]`：==一定要打第 i 只==时，前 i+1 只里最多能打到几只，0 表示打不到',
        'ma = 0': '`p`：最小的、时间差不到 4 秒的下标；`ma`：`f[0..p-1]` 的最大值',
        't, x, y = moles[i]': '看第 `{i}` 只：`t={t}`，位置 `({x},{y})`',
        'while t - moles[p][0] >= 4': lambda S, B, r: (
            f'第 `{S.p}` 只比它早 `{S.t - S.moles[S.p][0]} ≥ 4` 秒：地图只有 3×3，4 秒内哪都能走到 → 不用再看距离，只记最大 `f`'
            if S.t - S.moles[S.p][0] >= 4 else f'第 `{S.p}` 仅早 `{S.t - S.moles[S.p][0]}` 秒（< 4），窗口左端 `p={S.p}` 不动'),
        'ma = max(ma, f[p])': '把 `f[{p}]` 并进前缀最大值：`ma = {ma}`，窗口左端 `p` 右移到 {p + 1}',
        'f[i] = ma + 1': '4 秒以前一定赶得上，接在最优的后面：`f[{i}] = ma + 1 = {f[i]}`',
        'elif abs(x - 1)': lambda S, B, r: (
            f'之前一只没打过：起点 (1,1) 到 ({S.x},{S.y}) 曼哈顿距离 `{abs(S.x - 1) + abs(S.y - 1)}` ≤ `t = {S.t}` → 赶得上，`f[{S.i}] = 1`'
            if abs(S.x - 1) + abs(S.y - 1) <= S.t else f'曼哈顿距离 `{abs(S.x - 1) + abs(S.y - 1)}` > `t = {S.t}` → 起点赶不上，`f[{S.i}] = 0`'),
        'if f[j] > 0 and abs': lambda S, B, r: (
            f'枚举最近 4 秒内的第 `{S.j}` 只：距离 `{abs(S.x - S.moles[S.j][1]) + abs(S.y - S.moles[S.j][2])}`，时间差 `{S.t - S.moles[S.j][0]}`'
            + ('，==来得及==' if (S.f[S.j] > 0 and abs(S.x - S.moles[S.j][1]) + abs(S.y - S.moles[S.j][2]) <= S.t - S.moles[S.j][0])
               else '，==来不及（或 j 本身打不到）==')),
        'f[i] = max(f[i], f[j] + 1)': '接在第 `{j}` 只后面：`f[{i}] = max(旧值, f[{j}] + 1)` = =={f[i]}==',
        'return max(f)': '`f` 里最大的就是答案：最多打到 =={ret}== 只',
    },
    skip=['n = len(moles)', 'p = 0', 'p += 1', 18, 'for i in range', 'for j in range'],
    max_steps=85,
    cards=dict(
        one_liner='按时间排序做 DP；4 秒前的地鼠不用比距离，只记最大值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['3×3 的地图，锤子从 (1,1) 出发，每秒可移动一格（或不动）',
                 '`moles[i] = [time, x, y]`：第 time 秒地鼠在 (x,y) 冒头，只停这一秒',
                 '每秒只能打一只，求最多能打到几只；示例结果 `4`'],
        quote='注意到本题中地图大小仅为3 * 3，换言之，在4秒内锤子一定可以从地图中的任意位置移动到另一个位置。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[i]`：一定打第 `i` 只时最多能打几只；先判断起点能否赶到，再枚举上一只 `j`',
              '`j` 满足 `曼哈顿距离 ≤ 时间差` 才赶得上，朴素是 `O(n²)`',
              '时间差 ≥ 4 的 `j` 一定赶得上，只保留 `ma`；只枚举最近 4 秒内的地鼠'],
        summary=['时间 `O(n)`：窗口内至多 4×3×3 = 36 只，常数很小；空间 `O(n)`',
                 '易错点：必须先 `moles.sort`；`f[j] > 0` 才能接在 `j` 后面',
                 '把同一时刻的地鼠合并，窗口内只剩 3 个状态，可再优化（原文省略了）',
                 '原文本身是 Python 3 兼容写法，没有修改；题面是按题意重述的'],
    ),
)
