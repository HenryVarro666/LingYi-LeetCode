C0 = [[3, 1], [2, 2], [0, 0], [5, 3], [1, 1], [5, 4], [6, 5], [4, 4]]
K0 = 1
KP = C0[K0]


def _status(p):
    x, y = p
    if (x, y) == tuple(KP):
        return 'k'
    if (x < KP[0] and y < KP[1]) or (x > KP[0] and y > KP[1]):
        return 'cand'
    return 'out'


def _cur(S):
    if S.get('_line', 0) >= 7 and S.get('x') is not None and S.get('y') is not None and S.get('_line', 0) <= 13 and S.get('_line', 0) != 14:
        return (S['x'], S['y'])
    return None


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    pts = [tuple(p) for p in S['coordinates']]
    cur = _cur(S)
    cv.text((x0 + 18, y0 + 4), '平面上的点（黄 = coordinates[k]，绿/蓝区 = 可选，灰 = 排除，白圈 = 已处理）', 22, T['muted'], bold=True)
    cw, ch = 62, 36
    gx0, gy0 = x0 + 70, y0 + 50
    W, H = 7 * cw, 6 * ch
    cv.rect((gx0, gy0 + H - KP[1] * ch, gx0 + KP[0] * cw, gy0 + H), fill=T['green'], alpha=40)
    cv.rect((gx0 + (KP[0] + 1) * cw, gy0, gx0 + W, gy0 + H - (KP[1] + 1) * ch), fill=T['blue'], alpha=40)
    cv.line([(gx0, gy0 + H), (gx0 + W, gy0 + H)], T['border'], 2)
    cv.line([(gx0, gy0), (gx0, gy0 + H)], T['border'], 2)
    for i in range(7):
        cv.text((gx0 + i * cw + cw / 2, gy0 + H + 6), i, 18, T['dim'], anchor='mt', mono=True)
    for j in range(6):
        cv.text((gx0 - 8, gy0 + H - j * ch - ch / 2), j, 18, T['dim'], anchor='rm', mono=True)
    cv.text((gx0 + W + 10, gy0 + H), 'x', 20, T['dim'], anchor='lb')
    cv.text((gx0, gy0 - 22), 'y', 20, T['dim'], anchor='lb')
    order = {p: i for i, p in enumerate(pts)}
    done = set()
    if cur is not None:
        for p in pts[:order[cur]]:
            if _status(p) == 'cand':
                done.add(p)
    elif S.get('_line', 0) >= 14:
        done = {p for p in pts if _status(p) == 'cand'}
    for p in pts:
        px, py = p
        cx, cy = gx0 + px * cw + cw / 2, gy0 + H - py * ch - ch / 2
        st = _status(p)
        fill = T['yellow'] if st == 'k' else (T['cyan'] if st == 'cand' else (70, 76, 86))
        if p == cur:
            fill = T['pink']
        cv.rect((cx - 17, cy - 17, cx + 17, cy + 17), fill=fill, r=17, outline=T['text'] if p in done else None, width=3)
    # 排序后的序列
    ys = y0 + 50 + H + 56
    cv.text((x0 + 18, ys - 30), 'coordinates（排序后：x 升序，x 相同 y 降序）', 22, T['muted'], bold=True)
    n = len(pts)
    cell = min(112, (x1 - x0 - 40) / n)
    sx = x0 + 20 + ((x1 - x0 - 40) - cell * n) / 2
    for i, p in enumerate(pts):
        X = sx + i * cell
        st = _status(p)
        fill = T['yellow'] if st == 'k' else (T['panel2'] if st == 'cand' else (46, 52, 62))
        cv.rect((X + 3, ys, X + cell - 3, ys + 60), fill=fill, r=8, outline=T['pink'] if p == cur else T['border'], width=5 if p == cur else 1)
        col = T['bg'] if st == 'k' else (T['text'] if st == 'cand' else T['dim'])
        cv.text((X + cell / 2, ys + 30), f'({p[0]},{p[1]})', 22, col, anchor='mm', bold=True, mono=True)


CONFIG = dict(
    num=3288, title='最长上升路径的长度', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排序 + LIS 二分',
    tags=['灵神题单·动态规划', '难度分 2450'],
    code='''
class Solution:
    def maxPathLength(self, coordinates: List[List[int]], k: int) -> int:
        kx, ky = coordinates[k]
        coordinates.sort(key=lambda p: (p[0], -p[1]))

        g = []
        for x, y in coordinates:
            if x < kx and y < ky or x > kx and y > ky:
                j = bisect_left(g, y)
                if j < len(g):
                    g[j] = y
                else:
                    g.append(y)
        return len(g) + 1  # 算上 coordinates[k]
''',
    call=f'Solution().maxPathLength({C0!r}, {K0})',
    expect=5,
    max_steps=70,
    views=[
        dict(type='custom', draw=_draw, h=440),
        dict(type='array', var='g', label='g：长度 j+1 的上升序列的最小结尾 y', h=180, cell=90,
             pointers={'j if 10 <= _line <= 13 else None': 'blue'},
             color=lambda S, i, v: 'yellow' if S.get('j') is not None and i == S['j'] and S.get('_line') in (11, 13) else None),
    ],
    watch=[('kx,ky', '(kx, ky)', 'yellow'), ('x,y', '(x, y)', 'pink'), ('j', 'j', 'blue'), ('len(g)', 'len(g)', 'green')],
    captions={
        'kx, ky = ': '必须经过的点 `(kx, ky) = ({kx}, {ky})`：比它小的接在前面，比它大的接在后面',
        'coordinates.sort': '路径是==点集的选择，不是子序列==，所以能排序：按 `x` 升序；`x` 相同按 `y` ==降序==，这样同一个 `x` 至多选一个 `y`',
        'g = []': '`g` 只存 y，用 LIS 的二分贪心：排序后 x 已经有序，只要 y 严格上升就行',
        'for x, y in coordinates': lambda S, B, r: (f'看下一个点 `({S.x}, {S.y})`' if S.get('x') != B.get('x') or S.get('y') != B.get('y') else '所有点都看完了'),
        'if x < kx and y < ky': lambda S, B, r: (f'`({S.x}, {S.y})` 在 `({S.kx}, {S.ky})` 左下 或 右上 → ==可选==' if (S.x < S.kx and S.y < S.ky) or (S.x > S.kx and S.y > S.ky)
                                                  else (f'`({S.x}, {S.y})` 就是 `coordinates[k]` 本身，最后再 `+1` 算上它 → ==跳过==' if (S.x, S.y) == (S.kx, S.ky)
                                                        else f'`({S.x}, {S.y})` 和 `({S.kx}, {S.ky})` 不能同在一条上升路径上 → ==跳过==')),
        'j = bisect_left': '`bisect_left(g, {y})` = {j}：`g` 里第一个 `>= {y}` 的位置（严格上升，所以用 left）',
        'if j < len(g)': lambda S, B, r: (f'`j = {S.j} < len(g) = {len(S.g)}` → `y` 不超过 `g[{S.j}]`，可以==替换== `g[{S.j}]`' if S.j < len(S.g)
                                         else f'`j = {S.j} = len(g)` → `y` 比所有结尾都大'),
        'g[j] = y': lambda S, B, r: f'`g[{S.j}] = {B.g[S.j]}` 换成 `{S.y}`：同样长度，结尾更小，后面更容易接 → {S.g}',
        'g.append(y)': '`g` 末尾加入 `{y}`：上升序列变长 → {g}',
        'return len(g)': '`g` 长度 = `{len(g)}`（不含 k 点），再算上 `coordinates[k]` → =={ret}==',
    },
    cards=dict(
        one_liner='排序后，只对左下和右上的点做一次 LIS',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`coordinates` 里选点，`x` 和 `y` 都严格递增的序列叫上升序列',
                 '求包含 `coordinates[k]` 的最长上升路径长度',
                 '示例：`[[3,1],[2,2],[4,1],[0,0],[5,3]]`，`k=1` → `3`',
                 '本视频用 8 个点，`k=1`，点 `(2,2)` → `5`'],
        quote='仔细读题：我们要选的并不是 coordinates 的子序列，所以可以排序。按照 x 从小到大排序，问题变成计算 y 的 LIS。',
        quote_src='—— 灵茶山艾府题解',
        idea=['排序后，`x` 小的在前，只需要 `y` 严格递增',
              '`x` 相同的点按 `y` ==从大到小==排，LIS 里同一个 `x` 至多选一个',
              '只保留 `x<kx 且 y<ky`（接在前）或 `x>kx 且 y>ky`（接在后）的点，一起做 LIS',
              '左边这些点的 `y` 都小于右边这些，所以一次 LIS 就拼成了经过 `k` 的路径'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：同 `x` 要按 `y` 降序；否则一个 `x` 会被选两次',
                 '`bisect_left` 对应严格递增；非严格要用 `bisect_right`',
                 '最后 `+1` 把 `coordinates[k]` 自己算上',
                 '思考题：对每个 `k` 都求答案，可预处理每个点结尾/开头的 LIS'],
    ),
)
