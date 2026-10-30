G = [[1, 2, 3], [3, 1, 2]]


def _draw(cv, S, B, box, T):
    x0, y0, x1, y1 = box
    f = S.get('f')
    cv.text((x0 + 18, y0 + 4), 'f[i][j]：走到 (i, j) 时所有可能的异或值（黄 = 正在处理，绿 = 刚加入的值）', 22, T['muted'], bold=True)
    if f is None:
        return
    m, n = len(f), len(f[0])
    cw = min(250, (x1 - x0 - 40) / n)
    ch = min(150, (y1 - y0 - 70) / m)
    sx = x0 + 20 + ((x1 - x0 - 40) - cw * n) / 2
    sy = y0 + 50
    I = S['_inner']
    ci, cj = I.get('i'), I.get('j')
    bf = B.get('f')
    for i in range(m):
        for j in range(n):
            X, Y = sx + j * cw, sy + i * ch
            cur = (i, j) == (ci, cj)
            new = bf is not None and set(f[i][j]) != set(bf[i][j])
            cv.rect((X + 3, Y + 3, X + cw - 3, Y + ch - 3), fill=T['panel2'], r=8,
                    outline=T['yellow'] if cur else (T['green'] if new else T['border']), width=4 if (cur or new) else 1)
            cv.text((X + 12, Y + 8), f'grid={G[i][j]}', 18, T['dim'], mono=True)
            vals = sorted(f[i][j])
            cv.text((X + cw / 2, Y + ch / 2 + 10), '{' + ','.join(map(str, vals)) + '}' if vals else '{}', 28 if len(vals) < 5 else 22,
                    T['green'] if new else T['text'], anchor='mm', bold=True)


CONFIG = dict(
    num=3882, title='网格图中最小异或路径', difficulty='Medium', category='网格图',
    author='yiduobo', technique='DP：f[i][j] 存异或值集合',
    tags=['灵神核心路线', '灵神题单·网格图', '难度分 1771'],
    code='''
class Solution(object):
    def minCost(self, grid):

        m = len(grid)
        n = len(grid[0])

        f = [[set() for _ in range(n)] for _ in range(m)]
        f[0][0].add(grid[0][0])
        for i in range(m):
            for j in range(n):
                for v in f[i][j]:
                    if i + 1 < m:
                        f[i + 1][j].add(v ^ grid[i + 1][j])
                    if j + 1 < n:
                        f[i][j + 1].add(v ^ grid[i][j + 1])

        res = None
        for v in f[-1][-1]:
            if res is None or res > v:
                res = v
        return res
''',
    call=f'Solution().minCost({G})',
    expect=0,
    skip=['for j in range', 'm = len', 'n = len'],
    views=[
        dict(type='custom', draw=_draw, h=330),
        dict(type='set', var=lambda S: S['f'][-1][-1] if 'f' in S else None, label='f[-1][-1]（终点的所有异或值）', h=110),
    ],
    watch=[('i', "_inner.get('i')", 'blue'), ('j', "_inner.get('j')", 'pink'), ('v', "_inner.get('v')", 'purple'),
           ('res', 'res', 'green')],
    captions={
        'f = [[set()': '每个格子一个集合 `f[i][j]`，装「走到这里」的==所有可能异或值==',
        'f[0][0].add': '起点只有一个值：`f[0][0] = {{{grid[0][0]}}}`',
        'for v in f[i][j]': lambda S, B, r: (f"`f[{S['i']}][{S['j']}]` 里的值都向外扩展完了"
                                             if 'v' in B and (B['i'], B['j'], B['v']) == (S['i'], S['j'], S['v'])
                                             else f"取出 `f[{S['i']}][{S['j']}]` 里的一个值 `v = {S['v']}`"),
        'if i + 1 < m': lambda S, B, r: (f"能向下：`({S['i'] + 1},{S['j']})` 在网格内" if S['i'] + 1 < len(S['grid'])
                                         else '已经在最后一行，不能向下'),
        'f[i + 1][j].add': '向下走：`v ^ grid[{i + 1}][{j}]` = `{v} ^ {grid[i + 1][j]}` = =={v ^ grid[i + 1][j]}==，加入 `f[{i + 1}][{j}]`',
        'if j + 1 < n': lambda S, B, r: (f"能向右：`({S['i']},{S['j'] + 1})` 在网格内" if S['j'] + 1 < len(S['grid'][0])
                                         else '已经在最右列，不能向右'),
        'f[i][j + 1].add': '向右走：`v ^ grid[{i}][{j + 1}]` = `{v} ^ {grid[i][j + 1]}` = =={v ^ grid[i][j + 1]}==，加入 `f[{i}][{j + 1}]`',
        'res = None': '终点集合里挑最小值，先 `res = None`',
        'for v in f[-1][-1]': '枚举终点 `f[-1][-1]` 里的每个异或值',
        'if res is None or': lambda S, B, r: (f"`res` 还没有值 → 先取 `{S['v']}`" if B.get('res') is None
                                             else f"`res = {B['res']}` 与 `v = {S['v']}`：" + ('更大 → ==更新为 v==' if B['res'] > S['v'] else '不更小 → 保持')),
        'res = v': '`res` 更新为 =={res}==',
        'return res': '终点所有路径里最小的异或值是 =={res}==',
    },
    max_steps=110,
    cards=dict(
        one_liner='异或不能只留最小值，所以每个格子存下所有可能的异或结果',
        complexity='时间约 `O(mn·U)`，空间 `O(mn·U)`（`U = 1024`）',
        problem=['`m × n` 的网格，从左上角走到右下角，只能向右或向下',
                 '路径代价 = 路上所有格子值的==按位异或==，求最小代价',
                 '示例：`[[1,2],[3,4]]` → `6`；本视频：`[[1,2,3],[3,1,2]]` → `0`'],
        quote='不能沿用之前f[i][j]表示走到(i, j)的最小路径值，因为路径值是通过异或操作计算得到的，上一步的最小可能无法得到这一步的最小。',
        quote_src='—— yiduobo 题解原文',
        idea=['普通路径和 DP 只留最小值；异或没有这个性质',
              '值域只有 `0 ~ 1023` → 干脆==把所有可能的异或值都存下来==',
              '`f[i][j]` 里每个 `v` 向下、向右各推出一个新值 `v ^ grid[..]`'],
        summary=['最后答案是 `f[-1][-1]` 里的最小值',
                 '易错：起点要先放入 `grid[0][0]`，不是 0',
                 '边界：`i + 1 < m`、`j + 1 < n` 才能转移',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改',
                 '对比灵神：他倒着 DFS + `vis` 去重，这里是正向「集合 DP」'],
    ),
)
