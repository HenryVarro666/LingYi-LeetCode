PAL = ['blue', 'pink', 'green', 'purple', 'cyan', 'yellow', 'orange']


def _color(S, i, j, v):
    return PAL[v % 7] if v else None


def _qv(S):
    return [f'{a},{b}:{c}' for a, b, c in S['q']] if 'q' in S else None


def _nb(S, B, r):
    x, y = S.x, S.y
    if not (0 <= x < S.n and 0 <= y < S.m):
        return f'邻居 `({x},{y})` 越界'
    if S.res[x][y] != 0:
        return f'邻居 `({x},{y})` 已经是颜色 `{S.res[x][y]}` → 跳过'
    return f'邻居 `({x},{y})` 无色 → ==染成 `{S.c}`=='


CONFIG = dict(
    num=3905, title='多源图像渲染', difficulty='Medium', category='网格图',
    author='yiduobo', technique='多源 BFS（按颜色降序的初始队列）',
    tags=['灵神题单', '网格图', '难度分 1671'],
    code='''
class Solution(object):
    def colorGrid(self, n, m, sources):
        
        res = [[0] * m for _ in range(n)]
        q = []
        for x, y, c in sources:
            q.append((x, y, c))
            res[x][y] = c
        
        q.sort(key=lambda d:-d[2])
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        head, tail = 0, len(q)
        while head < tail:
            for nowx, nowy, c in q[head : tail]:
                for d in range(4):
                    x = nowx + dx[d]
                    y = nowy + dy[d]
                    if 0 <= x < n and 0 <= y < m and res[x][y] == 0:
                        res[x][y] = c
                        q.append((x, y, c))
        
            head, tail = tail, len(q)
        
        return res
''',
    call='Solution().colorGrid(3, 4, [[0, 0, 3], [0, 3, 5], [2, 1, 4]])',
    expect=[[3, 3, 5, 5], [3, 4, 5, 5], [4, 4, 4, 5]],
    skip=['dx = [', 'dy = [', 'for d in range(4)', 'x = nowx', 'y = nowy', 'q.append((x, y, c))', 'q = []'],
    views=[
        dict(type='grid', var='res', label='res（0 = 无色；颜色 = 数值；蓝框 = 当前扩散的格子，粉框 = 邻居）', cell=100, h=360,
             color=_color, cursors=[('nowx', 'nowy', 'blue'), ('x if _line == 20 else None', 'y', 'pink')]),
        dict(type='array', var=_qv, label='q（行,列:颜色；暗 = 已处理）', cell=130, h=190,
             dim=lambda S, i, v: i < S.get('head', 0)),
    ],
    watch=[('head', 'head', 'blue'), ('tail', 'tail')],
    captions={
        'res = [[0]': '`res` 全是 `0`，表示无色',
        8: '源点 `({x},{y})` 先染上初始颜色 `{c}`',
        'q.sort': '==按颜色从大到小排序==：同一轮里大颜色先到同一格，大的就能先染上 → `{q}`',
        'head, tail = 0': '`[head, tail)` 是当前这一轮要扩散的格子：`[{head}, {tail})`',
        'while head < tail': lambda S, B, r: (f'`head = {B.head} < tail = {B.tail}`：还有这一轮要扩散' if B.head < B.tail
                                              else '`head == tail`：没有新着色的格子了 → 结束'),
        'for nowx, nowy, c in': lambda S, B, r: ('这一轮的格子都处理完了' if B.get('nowx') == S.get('nowx') and B.get('nowy') == S.get('nowy') and B.get('c') == S.get('c')
                                                else f'取出 `({S.nowx},{S.nowy})`，颜色 `{S.c}`，向四个方向扩散'),
        'if 0 <= x < n': _nb,
        21: lambda S, B, r: f'`res[{S.x}][{S.y}] = {S.c}`：入队的同时染色，后来的小颜色看到非 0 就不会覆盖',
        'head, tail = tail': '这一轮结束：下一轮是新入队的 `[{head}, {tail})`',
        'return res': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='初始队列按颜色从大到小排好，BFS 一轮轮扩',
        complexity='时间 `O(k log k + nm)`，空间 `O(nm)`',
        problem=['`n × m` 网格，`sources` 给出初始有色的格子 `[r, c, color]`',
                 '每单位时间，有色格子同时向四邻无色格子扩散',
                 '多种颜色同一时间到达同一格 → 取==最大==颜色',
                 '本视频：`n=3, m=4`，`sources=[[0,0,3],[0,3,5],[2,1,4]]`'],
        quote='需要注意多种颜色同时到达时要取最大的颜色染色，因此在这里需要先将初始队列按照颜色从大到小进行排序，这样一来就能保证在一个扩展的轮次中，较大的颜色先与较小的颜色到达同一单元格。',
        quote_src='—— yiduobo 题解原文',
        idea=['用数组 `q` 加 `head`、`tail` 做队列，一次处理一整轮',
              '每一轮里，颜色大的源点排在前面，先抢到共同的邻居',
              '一个格子染色后不再是 `0`，后到的小颜色自然不会覆盖'],
        summary=['时间 `O(k log k + nm)`，空间 `O(nm)`',
                 '易错：排序只在最开始做一次，之后新入队的格子顺序自动继承',
                 '易错：`res[x][y] == 0` 既是未着色判断，也起 visited 的作用',
                 '原文为 Python 2 风格，代码无需改动'],
    ),
)
