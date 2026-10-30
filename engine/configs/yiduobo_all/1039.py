import math


def _active(S):
    return S.get('_line') in (10, 11) and 'cut_pos' in S and 'j' in S


def _val(S):
    i, j, k, v = S['i'], S['j'], S['cut_pos'], S['values']
    f = S['f']
    return f[i][k] + f[k][j] + v[i] * v[j] * v[k]


def _color(S, r, c, val):
    if not _active(S):
        return None
    i, j, k = S['i'], S['j'], S['cut_pos']
    if (r, c) == (i, j):
        return 'yellow'
    if (r, c) in ((i, k), (k, j)):
        return 'blue'
    return None


def _formula(S):
    if not _active(S):
        if 'l' in S and 'j' in S:
            return f'区间长度 `l = {S["l"]}`：先算短的区间，再算长的区间'
        return '`f[i][j]` = 点 `i`~`j` 这段连续的点，加上边 `(i,j)` 形成的多边形的最低得分'
    i, j, k, v = S['i'], S['j'], S['cut_pos'], S['values']
    f = S['f']
    return (f'三角形 `({i},{k},{j})`：`f[{i}][{k}] + f[{k}][{j}] + {v[i]}×{v[j]}×{v[k]}` = '
            f'`{f[i][k]} + {f[k][j]} + {v[i] * v[j] * v[k]}` = =={_val(S)}==')


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    v = S['values']
    n = len(v)
    R = min(x1 - x0 - 160, y1 - y0 - 150) / 2
    cx, cy = (x0 + x1) / 2, y0 + 80 + R
    cv.text((x0 + 18, y0 + 4), '多边形（黄边 = (i,j)，绿 = 当前尝试的三角形 i-cut_pos-j）', 22, T['muted'], bold=True)
    pts = []
    for t in range(n):
        a = -math.pi / 2 + 2 * math.pi * t / n
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    cv.line(pts + [pts[0]], T['border'], 4)
    live = 'i' in S and 'j' in S and S['j'] < n
    if live:
        i, j = S['i'], S['j']
        if _active(S):
            k = S['cut_pos']
            cv.poly([pts[i], pts[k], pts[j]], (88, 120, 70))
            cv.line([pts[i], pts[k], pts[j], pts[i]], T['green'], 5)
        cv.line([pts[i], pts[j]], T['yellow'], 7)
    for t, (X, Y) in enumerate(pts):
        hot = live and t in (S['i'], S['j'])
        cut = live and _active(S) and t == S['cut_pos']
        cv.rect((X - 30, Y - 30, X + 30, Y + 30), fill=T['yellow'] if hot else (T['green'] if cut else T['panel2']),
                outline=T['border'], r=30)
        cv.text((X, Y), v[t], 30, T['bg'] if (hot or cut) else T['text'], anchor='mm', bold=True)
        ox = (X - cx) / max(R, 1) * 44
        oy = (Y - cy) / max(R, 1) * 44
        cv.text((X + ox, Y + oy), str(t), 22, T['dim'], anchor='mm', mono=True)


CONFIG = dict(
    num=1039, title='多边形三角剖分的最低得分', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='区间 DP（按区间长度递推）',
    tags=['灵神题单', '动态规划', '难度分 2130'],
    code='''
class Solution(object):
    def minScoreTriangulation(self, values):

        n = len(values)
        f = [[0] * n for _ in range(n)]
        for l in range(1, n):
            for i in range(n - l):
                j = i + l
                for cut_pos in range(i + 1, j):
                    if f[i][j] == 0 or f[i][j] > f[i][cut_pos] + f[cut_pos][j] + values[i] * values[j] * values[cut_pos]:
                        f[i][j] = f[i][cut_pos] + f[cut_pos][j] + values[i] * values[j] * values[cut_pos]
        
        return f[0][n - 1]
''',
    call='Solution().minScoreTriangulation([3, 1, 4, 2, 5])',
    expect=33,
    skip=['j = i + l'],
    max_steps=80,
    views=[
        dict(type='custom', draw=_draw, h=400),
        dict(type='text', fn=_formula, size=24, h=90),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 当前用到的两段）', h=400, cell=64,
             rows=lambda S: [str(k) for k in range(len(S['values']))], cols=lambda S: [str(k) for k in range(len(S['values']))],
             color=_color),
    ],
    watch=[('l', 'l', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('cut_pos', 'cut_pos', 'green')],
    captions={
        'n = len': '`n = {n}` 个点，最多 50 个，必须保证 `f[i][j]` 的点是==连续的区间==，不然状态会指数级增长',
        'f = [[0]': '`f[i][j]`：点 `i`~`j` 连续的一段，加上边 `(i,j)` 形成的多边形的最低得分；`0` 表示还没算',
        'for l in range': lambda S, B, r: (f'区间长度 `l = {S.l}`：子多边形更短，==必须先算完更短的区间==' if S.get('l') != B.get('l')
                                           else '所有区间长度都算完了'),
        'for i in range': lambda S, B, r: ('这个长度的区间都算完了' if S.get('i') == B.get('i') and S.get('l') == B.get('l')
                                           else f'`l = {S.l}`，左端 `i = {S.i}` → 右端 `j = i + l = {S.i + S.l}`'),
        'for cut_pos in range': lambda S, B, r: (
            '`i`、`j` 相邻，中间没有点 → 没有三角形，`f[i][j]` 保持 0' if S.l == 1
            else f'枚举 `cut_pos` 取 `{S.i + 1}`~`{S.j - 1}`：它与 `i`、`j` 组成三角形，先试 `cut_pos = {S.cut_pos}`' if S.f[S.i][S.j] == 0
            else f'再试下一个分割点 `cut_pos = {S.cut_pos}`' if B.get('cut_pos') != S.cut_pos
            else f'`cut_pos` 都试完了，`f[{S.i}][{S.j}]` = =={S.f[S.i][S.j]}=='),
        'if f[i][j] == 0 or': lambda S, B, r: (f'`f[{S.i}][{S.j}]` 还是 0，直接取第一个候选 `{_val(S)}`' if S.f[S.i][S.j] == 0
                                               else f'已有 `{S.f[S.i][S.j]}`，新候选 `{_val(S)}` → ' + ('更小，替换' if S.f[S.i][S.j] > _val(S) else '不更小，保留')),
        'f[i][j] = f[i][cut_pos]': '`f[{i}][{j}]` 更新为 =={f[i][j]}==（以点 `{cut_pos}` 为三角形顶点）',
        'return f[0][n - 1]': '整个多边形（边 `0-{n-1}`）最低得分 `f[0][{n-1}]` = =={ret}==',
    },
    cards=dict(
        one_liner='f[i][j] 保持区间连续，枚举边 (i,j) 对面的三角形顶点',
        complexity='时间 `O(n^3)`，空间 `O(n^2)`',
        problem=['凸 `n` 边形，顶点按顺时针有数值 `values[i]`',
                 '剖成 `n − 2` 个三角形，每个三角形得分 = ==三顶点乘积==，求总分最小值',
                 '本视频：`values = [3,1,4,2,5]` → `33`'],
        quote='在这里必须要想办法维护住多边形的区间性质，即f[i][j]表示的点i到点j必须是连续的。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[l][r]`：点 `l`~`r` 连续的一段再加边 `(l,r)` 围成的多边形的最低得分',
              '分割只能从 `i+1`~`j−1` 里选一个点 `cut_pos`，与 `i`、`j` 组成三角形，剩下 `i~cut_pos` 和 `cut_pos~j` 两块',
              '递推要先算短区间：先枚举区间长度 `l`，再枚举 `i`，由 `j = i + l` 得右端'],
        summary=['时间 `O(n^3)`，空间 `O(n^2)`',
                 '`f` 初值 0 兼作「没算过」标记：`f[i][j] == 0` 时直接取第一个候选（`values[i] > 0` 所以候选都 > 0）',
                 '`l` 从 1 开始，`l = 1` 的边没有中间点，保持 0',
                 '对比灵神：灵神 `i` 倒序、`j` 正序填表，这里是按区间长度由短到长；原文也提到记忆化搜索更方便'],
    ),
)
