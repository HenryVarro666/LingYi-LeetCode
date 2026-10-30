G = [[1, 2, -1, 3], [-1, 4, -1, -1], [5, -1, 6, 7]]


def _cell(S, i, j, v):
    if G[i][j] == -1:
        return 'red'
    if v == -1:
        return 'green'
    return None


def _dim(S, i, j, v):
    return G[i][j] == -1


def _parts_txt(S):
    parts = S.get('parts')
    if parts is None:
        return ''
    if not parts:
        return '还没有找到连通块'
    return '已找到的连通块 [数量, 和]：' + '  '.join(f'`[{c}, {s}]`' for c, s in parts)


CONFIG = dict(
    num=2852, title='所有单元格的远离程度之和', difficulty='Medium', category='网格图',
    author='yiduobo', technique='floodfill 求连通块 · 乘法原理',
    tags=['灵神题单·网格图'],
    code='''
class Solution(object):
    def sumRemoteness(self, grid):

        m = len(grid)
        n = len(grid[0])
        parts = []

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        for i in range(m):
            for j in range(n):
                if grid[i][j] != -1:
                    q = [[i, j]]
                    head, tail = 0, 1
                    s = grid[i][j]
                    grid[i][j] = -1
                    while head < tail:
                        nowx, nowy = q[head]
                        head += 1
                        for d in range(4):
                            x = nowx + dx[d]
                            y = nowy + dy[d]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] > 0:
                                s += grid[x][y]
                                q.append([x, y])
                                tail += 1
                                grid[x][y] = -1
                    
                    parts.append([len(q), s])
        
        tot_s = sum([x[1] for x in parts])
        res = 0
        for cnt, s in parts:
            res += (tot_s - s) * cnt
        
        return res
''',
    call='Solution().sumRemoteness([[1, 2, -1, 3], [-1, 4, -1, -1], [5, -1, 6, 7]])',
    expect=141,
    skip=['m = len', 'n = len', 'dx = [', 'dy = [', 'head += 1', 'for d in range(4)', 'x = nowx', 'y = nowy',
          'q.append', 'tail += 1', 'head, tail = 0, 1', 'for i in range(m)', 'for j in range(n)'],
    max_steps=78,
    views=[
        dict(type='grid', var='grid', cell=100, h=330, color=_cell, dim=_dim,
             label='grid（红 = 障碍 -1，绿 = 已被 floodfill 吃掉并改成 -1，蓝框 = 出队，粉框 = 邻居）',
             cursors=[('nowx', 'nowy', 'blue'), ('x if _line in (19, 20) else None', 'y', 'pink')]),
        dict(type='text', fn=lambda S: _parts_txt(S), h=80, size=30),
        dict(type='text', fn=lambda S: (f"`tot_s = {S['tot_s']}`：全图数值总和" if 'tot_s' in S else ''), h=60, size=30),
    ],
    watch=[('s', 's', 'cyan'), ('len(q)', 'len(q) if "q" in dir() else None', 'blue'), ('tot_s', 'tot_s', 'orange'), ('res', 'res', 'green')],
    captions={
        'parts = []': '`parts` 记录每个连通块的 `[单元格数, 数值和]`',
        'if grid[i][j] != -1': lambda S, B, r: (f'`grid[{S.i}][{S.j}] = {S.grid[S.i][S.j]}` 不是 -1 ：==新连通块的起点==，开始 floodfill'
                                                if S.grid[S.i][S.j] != -1 else
                                                f'`grid[{S.i}][{S.j}] = -1`：障碍或已访问，跳过'),
        'q = [[i, j]]': '起点入队，数组 `q` 当 BFS 队列',
        's = grid[i][j]': '`s` 累计这个连通块的数值和，先放入起点 `{s}`',
        'grid[i][j] = -1': '把起点改成 -1 ：==兼作访问标记==，不用另开 vis',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：队列不空，继续' if B.head < B.tail
                                              else f'`head == tail`：这个连通块扫完，共 `{len(S.q)}` 格，和 `{S.s}`'),
        'nowx, nowy = q[head]': '出队 `({nowx},{nowy})`，看上下左右四个邻居',
        'if x >= 0 and x < m': lambda S, B, r: (f'邻居 `({B.x},{B.y})` 越界' if not (0 <= B.x < B.m and 0 <= B.y < B.n)
                                                else (f'邻居 `({B.x},{B.y})` 的值 `{B.grid[B.x][B.y]}` > 0 → ==同一连通块，吃掉它=='
                                                      if B.grid[B.x][B.y] > 0 else
                                                      f'邻居 `({B.x},{B.y})` 的值 `{B.grid[B.x][B.y]}`：障碍或已访问 → 不扩展')),
        's += grid[x][y]': '把邻居的值并进来：`s` = `{s}`',
        'grid[x][y] = -1': '邻居入队后立刻改成 -1，避免重复入队',
        'parts.append': '连通块完成：==单元格数 {len(q)}，数值和 {s}== 存入 `parts`',
        'tot_s = sum': '`tot_s` = 所有连通块的和 = ==整张图的数值总和== `{tot_s}`',
        'res = 0': '`res` 累计答案',
        'for cnt, s in parts': lambda S, B, r: (1 / 0 if 'cnt' in B and (B.cnt, B.s) == (S.cnt, S.s)
                                                else f'取一个连通块：`cnt = {S.cnt}` 格，和 `s = {S.s}`'),
        'res += (tot_s - s) * cnt': '这个块的每格远离程度都是 `tot_s - s = {tot_s - s}`，共 `{cnt}` 格 → `res` += `{tot_s - s} × {cnt}` = =={res}==',
        'return res': '答案 `{res}`',
    },
    cards=dict(
        one_liner='远离程度只和所在连通块的数值和有关：块内每格都一样',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 网格，`-1` 是障碍，其余格子是正整数',
                 '格子的==远离程度== = 所有==到不了它==的非障碍格子的数值之和（够得着的不算）',
                 '求所有非障碍格子的远离程度之和',
                 '本视频：`[[1,2,-1,3],[-1,4,-1,-1],[5,-1,6,7]]` → `141`'],
        quote='对于其中的某个连通块，设其中有k个单元格，这些单元格的数值之和为s，那么这些单元格对最终答案产生的影响就是k * (tot_s - s)',
        quote_src='—— yiduobo 题解原文',
        idea=['同一连通块内的格子互相可达，所以远离程度==相同==：`tot_s - s`',
              '用 floodfill 找出每个连通块的格子数 `k` 和数值和 `s`',
              '最后每个块贡献 `k × (tot_s − s)`，累加即答案'],
        summary=['时间 `O(mn)`，每个格子只入队一次；空间 `O(mn)`',
                 '访问标记直接写回 `grid`（改成 -1），所以会改动输入',
                 '易错：答案可能很大，Python 不会溢出，其他语言要用 64 位',
                 '原文已是 Python 3 可运行的写法，代码未改'],
    ),
)
