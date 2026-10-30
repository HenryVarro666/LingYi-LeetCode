CODE = '''
class Solution:
    def minCost(self, grid: list[list[int]], k: int) -> int:
        m, n = len(grid), len(grid[0])
        d = [[inf] * n for _ in range(m)]
        u = [[inf] * n for _ in range(m)]
        r = [[inf] * n for _ in range(m)]
        l = [[inf] * n for _ in range(m)]
        d[0][0] = r[0][0] = grid[0][0]
        ans = inf

        # 第一轮循环，把状态从 (0,0) 更新到第一行和第一列
        # 第二轮循环，把状态从第一行向下更新到其余行，从第一列向右更新到其余列，这样就算出了转向 1 次的所有情况
        # ……
        for _ in range(k + 1):
            # 原地转向
            for di, ui, ri, li in zip(d, u, r, l):
                for j, t in enumerate(zip(di, ui, ri, li)):
                    di[j] = ui[j] = ri[j] = li[j] = min(t)

            # 向下
            for i in range(1, m):
                for j, x in enumerate(grid[i]):
                    d[i][j] = min(d[i][j], d[i - 1][j] + x)

            # 向上
            for i in range(m - 2, -1, -1):
                for j, x in enumerate(grid[i]):
                    u[i][j] = min(u[i][j], u[i + 1][j] + x)

            # 向右
            for row, ri in zip(grid, r):
                for j in range(1, n):
                    ri[j] = min(ri[j], ri[j - 1] + row[j])

            # 向左
            for row, li in zip(grid, l):
                for j in range(n - 2, -1, -1):
                    li[j] = min(li[j], li[j + 1] + row[j])

            ans = min(ans, d[-1][-1], r[-1][-1])

        return -1 if ans == inf else ans
'''
GRID = [[2, 7, 3], [1, 4, 5]]
_L = CODE.strip('\n').splitlines()


def _ln(s):
    return next(i + 1 for i, t in enumerate(_L) if s in t)


L_TURN, L_DOWN, L_UP, L_RIGHT, L_LEFT, L_ANS = (_ln('di[j] = ui[j]'), _ln('d[i][j] = min'), _ln('u[i][j] = min'),
                                                  _ln('ri[j] = min'), _ln('li[j] = min'), _ln('ans = min(ans'))


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    grid = S.get('grid')
    if grid is None:
        return
    R, C = len(grid), len(grid[0])
    ln = S.get('_line')
    names = [('grid', 'grid（每格代价）', 'text'), ('d', 'd：最后一步向下', 'blue'), ('u', 'u：最后一步向上', 'purple'),
             ('r', 'r：最后一步向右', 'pink'), ('l', 'l：最后一步向左', 'orange')]
    cols = 3
    pw = (x1 - x0 - 20) / cols
    cell = min(70, (pw - 30) / C)
    ph = 40 + R * cell + 24
    for k, (nm, lab, c) in enumerate(names):
        g = S.get(nm)
        if g is None:
            continue
        bg = B.get(nm)
        px = x0 + 10 + (k % cols) * pw + (pw - C * cell) / 2
        py = y0 + 8 + (k // cols) * ph
        cv.text((px, py), lab, 22, T[c] if c != 'text' else T['muted'], bold=True)
        for i in range(R):
            for j in range(C):
                v = g[i][j]
                X, Y = px + j * cell, py + 36 + i * cell
                cur = False
                if ln in (L_DOWN, L_UP) and S.get('i') == i and S.get('j') == j and nm in ('grid', 'd' if ln == L_DOWN else 'u'):
                    cur = True
                if ln in (L_RIGHT, L_LEFT) and 'row' in S and S['row'] is grid[i] and S.get('j') == j and nm in ('grid', 'r' if ln == L_RIGHT else 'l'):
                    cur = True
                if ln == L_TURN and 'di' in S and S.get('j') == j and nm != 'grid' and S['di'] is S['d'][i]:
                    cur = True
                chg = nm != 'grid' and bg is not None and bg[i][j] != v
                done = ln == L_ANS and nm in ('d', 'r') and (i, j) == (R - 1, C - 1)
                fill = T['green'] if done else (T['yellow'] if cur else T['panel2'])
                cv.rect((X + 2, Y + 2, X + cell - 2, Y + cell - 2), fill=fill, r=6,
                        outline=T['yellow'] if chg else T['border'], width=4 if chg else 1)
                sv = '∞' if v == inf else str(v)
                cv.text((X + cell / 2, Y + cell / 2), sv, int(cell * 0.42), T['bg'] if (cur or done) else T['text'], anchor='mm', bold=True)


def _stat(S):
    ln = S.get('_line', 0)
    t = (S.get('_', 0) if '_' in S else None)
    head = f'第 {S["_"] + 1} 轮（已转向 {S["_"]} 次）：' if t is not None else ''
    if t is None:
        return '`d/u/r/l[i][j]`：到 `(i,j)` 且最后一步方向为 下/上/右/左 的最小代价（∞ = 到不了）'
    if ln == L_TURN:
        return head + '先原地转向：每格四个方向取 ==最小值==（转向消耗一次次数）'
    if ln in (L_DOWN, L_UP, L_RIGHT, L_LEFT):
        return head + '再直走：同方向沿着走，不消耗转向次数'
    return head + '`ans` = 终点处 d / r 的最小值'


CONFIG = dict(
    num=4046, title='至多 K 次转向的最小路径代价', difficulty='Hard', category='图论算法',
    author='灵茶山艾府', technique='分层图 DP（原地转向 + 直走）',
    code=CODE,
    call=f'Solution().minCost({GRID}, 1)',
    expect=12,
    skip=['m, n = len(grid)', 'u = [[inf]', 'r = [[inf]', 'l = [[inf]', 'for _ in range(k + 1)', 'for di, ui, ri, li in zip', 'for j, t in enumerate', 'for i in range', 'for j, x in enumerate',
          'for row, ri in zip', 'for j in range(1, n)', 'for row, li in zip', 'for j in range(n - 2'],
    views=[
        dict(type='text', fn=_stat, size=22, h=60),
        dict(type='custom', draw=_draw, h=560),
    ],
    watch=[('轮', '_', 'blue'), 'i', 'j', ('ans', 'ans', 'green')],
    max_steps=80,
    captions={
        'd = [[inf]': '`d/u/r/l` 分别记最后一步向下/上/右/左的最小代价，一开始都是 ∞',
        'd[0][0] = r[0][0]': '起点 `(0,0)` 代价 `{grid[0][0]}`，初始方向只能向下或向右',
        'ans = inf': '`ans` 取各轮终点的最小值',
        'di[j] = ui[j]': lambda S, B, r: (f'这格四个方向 `{B.t}` 全是 ∞：还到不了，保持 ∞' if min(B.t) == inf
                                          else f'这格四个方向 `{B.t}` → 都取最小值 =={min(B.t)}==：==转向就是换成别的方向==，所以取最小'),
        'd[i][j] = min': '向下：`d[{i}][{j}] = min({B.d[i][j]}, d[{i-1}][{j}] + {x})` = =={d[i][j]}==',
        'u[i][j] = min': '向上：`u[{i}][{j}] = min({B.u[i][j]}, u[{i+1}][{j}] + {x})` = =={u[i][j]}==',
        'ri[j] = min': '向右：`r[·][{j}] = min({B.ri[j]}, 左边 {ri[j-1]} + {row[j]})` = =={ri[j]}==',
        'li[j] = min': '向左：`l[·][{j}] = min({B.li[j]}, 右边 {li[j+1]} + {row[j]})` = =={li[j]}==',
        'ans = min(ans': '终点 `d = {d[-1][-1]}`，`r = {r[-1][-1]}`→ `ans = min({B.ans}, {d[-1][-1]}, {r[-1][-1]})` = =={ans}==',
        'return -1 if': '转向次数 `0..k` 的所有情况都算完，`ans = {ans}` → 返回 =={ret}==',
    },
    cards=dict(
        one_liner='转向次数当层数：每层先原地转向，再沿四个方向直走',
        complexity='时间 `O(kmn)`，空间 `O(mn)`',
        problem=['网格每格有代价，从左上走到右下，上下左右都能走，==至多转向 k 次==',
                 '路径代价是经过的格子之和（走回头路也要重复计入）',
                 '本视频：`grid=[[2,7,3],[1,4,5]], k=1` → `12`'],
        quote='走回头路要转向，会消耗 k，所以我们不会回到完全一样的状态，所以添加参数 k 后的分层图是一个有向无环图（DAG）。所以可以直接跑 DP，无需 Dijkstra。',
        quote_src='—— 灵茶山艾府题解',
        idea=['分层图：状态是（转向次数，位置，最后一步方向）；回头路必转向，所以是 DAG',
              '把移动拆成：==原地转向==（四个方向取最小）和 ==直走==（同层沿一个方向）',
              'k 这一维滚动掉：每轮先转向再直走，轮数 = 转向次数 + 1'],
        summary=['时间 `O(kmn)`，空间 `O(mn)`；每轮要 ==先转向、后直走==',
                 '直走要按方向遍历：向下从上到下，向上从下到上，向左右同理',
                 '初始只有向下和向右两个方向有值，答案只看终点的 d 和 r',
                 '同题还有 Dijkstra（四元状态堆）和记忆化搜索两种写法，这里选了最后的递推'],
    ),
)
