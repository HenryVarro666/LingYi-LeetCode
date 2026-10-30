import math


def _cand(S):
    i, j, f, v = S['i'], S['j'], S['f'], S['v']
    return [(k, f[i][k] + f[k][j] + v[i] * v[j] * v[k]) for k in range(i + 1, j)]


def _active(S):
    return S.get('_line') in (7, 8) and 'j' in S and 'i' in S and S['j'] >= S['i'] + 2


def _color(S, r, c, val):
    if not _active(S):
        return None
    i, j = S['i'], S['j']
    cand = _cand(S)
    best = min(cand, key=lambda t: t[1])[0]
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i, best), (best, j)):
        return 'green'
    if any((r, c) in ((i, k), (k, j)) for k, _ in cand):
        return 'blue'
    return None


def _formula(S):
    if not _active(S):
        return '`f[i][j]` = 顶点 `i`~`j` 与边 `(i,j)` 围成的多边形的最低得分；`i` 倒序、`j` 正序'
    i, j, v = S['i'], S['j'], S['v']
    cand = _cand(S)
    s = '，'.join(f'k={k}: {x}' for k, x in cand)
    return f'三角形 `(i,k,j)` 乘积 + 两边子多边形，各 k 的总分：{s} → 最小 =={min(x for _, x in cand)}=='


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    v = S['v']
    n = len(v)
    R = min(x1 - x0 - 160, y1 - y0 - 150) / 2
    cx, cy = (x0 + x1) / 2, y0 + 80 + R
    cv.text((x0 + 18, y0 + 4), '多边形（顶点 = 下标:值；黄边 = (i,j)，绿 = 最优的三角形）', 22, T['muted'], bold=True)
    pts = []
    for t in range(n):
        a = -math.pi / 2 + 2 * math.pi * t / n
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    cv.line(pts + [pts[0]], T['border'], 4)
    act = _active(S)
    if 'i' in S and 'j' in S and S['j'] < n:
        i, j = S['i'], S['j']
        if act:
            cand = _cand(S)
            best = min(cand, key=lambda t: t[1])[0]
            cv.poly([pts[i], pts[best], pts[j]], (88, 120, 70))
            cv.line([pts[i], pts[best], pts[j], pts[i]], T['green'], 5)
        cv.line([pts[i], pts[j]], T['yellow'], 7)
    for t, (X, Y) in enumerate(pts):
        hot = 'i' in S and 'j' in S and t in (S['i'], S['j']) and S['j'] < n
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=T['yellow'] if hot else T['panel2'], outline=T['border'], r=30)
        cv.text((X, Y), v[t], 30, T['bg'] if hot else T['text'], anchor='mm', bold=True)
        ox = (X - cx) / max(R, 1) * 44
        oy = (Y - cy) / max(R, 1) * 44
        cv.text((X + ox, Y + oy), str(t), 22, T['dim'], anchor='mm', mono=True)


CONFIG = dict(
    num=1039, title='多边形三角剖分的最低得分', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='区间 DP（1:1 翻译成递推）',
    tags=['灵神题单', '动态规划', '难度分 2130'],
    code='''
class Solution:
    def minScoreTriangulation(self, v: List[int]) -> int:
        n = len(v)
        f = [[0] * n for _ in range(n)]
        for i in range(n - 3, -1, -1):
            for j in range(i + 2, n):
                f[i][j] = min(f[i][k] + f[k][j] + v[i] * v[j] * v[k]
                              for k in range(i + 1, j))
        return f[0][-1]
''',
    call='Solution().minScoreTriangulation([1,3,1,4,1,5])',
    expect=13,
    skip=['for j in range', 'for k in range(i + 1, j))'],
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_formula, size=24, h=90),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 候选，绿 = 最优的顶点 k）', h=400, cell=64,
             rows=lambda S: [str(k) for k in range(len(S['v']))], cols=lambda S: [str(k) for k in range(len(S['v']))],
             color=_color),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('n', 'n')],
    captions={
        'n = len(v)': '`n = {n}` 个顶点；凸 n 边形剖分一定是 `n − 2` 个三角形',
        'f = [[0]': '`f[i][j]` 对应 `dfs(i, j)`；`f[i][i+1] = 0`：只有两个点，组不成三角形',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：`f[i][k]` 要用 `f[k][j]`（k > i）→ ==i 从大到小== 枚举' if S.get('i') != B.get('i')
                                           else '所有区间都算完了'),
        'f[i][j] = min': lambda S, B, r: ((f'`j = {S.j}`：边 `({S.i},{S.j})` 一定在某个三角形里，枚举它的第三个顶点 `k` = {S.i+1}~{S.j-1}，'
                                           f'得分 `v[i]·v[j]·v[k]` + 两边子多边形 `f[i][k] + f[k][j]`') if S.f[S.i][S.j] == 0
                                          else f'取最小的 `k`：`f[{S.i}][{S.j}]` = =={S.f[S.i][S.j]}=='),
        'return f[0][-1]': '边 `0-{n-1}` 固定在某个三角形里，不用「断环成链」：答案 `f[0][{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='固定边 0-(n-1)，枚举它所在三角形的第三个顶点 k',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['凸 `n` 边形，顶点按顺时针有数值 `values[i]`',
                 '把它剖成 `n − 2` 个三角形，每个三角形的得分 = ==三个顶点的乘积==，求总分最小值',
                 '示例：`values = [1,3,1,4,1,5]` → `13`'],
        quote='无论如何旋转多边形，无论从哪条边开始计算，得到的结果都是一样的，那么不妨就从 0-(n-1) 这条边开始计算。',
        quote_src='—— 灵茶山艾府题解（答疑）',
        idea=['`dfs(i, j)`：顶点 `i`~`j` 与边 `(i,j)` 围成的多边形的最低得分',
              '边 `(i,j)` 必在某个三角形里，枚举第三个顶点 `k`：得分 `v[i]·v[j]·v[k]`，剩下两个小多边形继续递归',
              '`f[i][j] = min(f[i][k] + f[k][j] + v[i]·v[j]·v[k])`；`i` 倒序、`j` 正序'],
        summary=['时间 `O(n^3)`：状态 `O(n^2)` × 枚举 `k` 的 `O(n)`',
                 '易错：`i` 从 `n-3` 开始，`j` 从 `i+2` 开始（`j = i+1` 是边界 0）',
                 '灵神题解先讲 `@cache` 记忆化搜索，这里演示的是它 1:1 翻译的递推',
                 '同类区间 DP：1547 切棍子的最小成本、1000 合并石头'],
    ),
)
