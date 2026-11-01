def _col(S, i, j, v):
    if v == 0:
        return None
    if 'used' in S and i * len(S['land'][0]) + j in S['used']:
        for r1, c1, r2, c2 in S.get('res', []):
            if r1 <= i <= r2 and c1 <= j <= c2:
                return 'blue'
        return 'green'
    return None


CONFIG = dict(
    num=1992, title='找到所有的农场组', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='floodfill（BFS）· 队首队尾即答案',
    tags=['灵神题单', '贪心与思维', '难度分 1539'],
    code='''
class Solution(object):
    def findFarmland(self, land):

        m = len(land)
        n = len(land[0])

        res = []
        used = set()
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                if land[i][j] == 1 and i * n + j not in used:
                    q = [[i, j]]
                    used.add(i * n + j)
                    l = 0
                    r = 1
                    while l < r:
                        for nowx, nowy in q[l : r]:
                            for index in range(4):
                                x = nowx + dx[index]
                                y = nowy + dy[index]
                                if x >= 0 and x < m and y >= 0 and y < n and x * n + y not in used and land[x][y] == 1:
                                    used.add(x * n + y)
                                    q.append([x, y])
                    
                        l, r = r, len(q)
                    
                    res.append([q[0][0], q[0][1], q[-1][0], q[-1][1]])
        
        return res
''',
    call='Solution().findFarmland([[1,0,0],[0,1,1],[0,1,1]])',
    expect=[[0,0,0,0],[1,1,2,2]],
    views=[
        dict(type='grid', var='land', label='land（绿 = 已入队，蓝 = 已记录，粉框 = 邻居）', cell=96, h=380,
             color=_col, cursors=[('i', 'j', 'yellow'), ('x', 'y', 'pink')]),
        dict(type='text', fn=lambda S: f"队列 `q` = `{S['q']}`" if 'q' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('l', 'l'), ('r', 'r'), ('res', 'res', 'green')],
    max_steps=110,
    skip=['dx = ', 'dy = ', 'm = len', 'n = len', 'x = nowx', 'y = nowy', 'q.append', 'r = 1', 'l = 0', 'for index'],
    captions={
        'if land[i][j] == 1 and': lambda S, B, r: (f"`({S.i},{S.j})` 是森林 → 跳过" if S.land[S.i][S.j] == 0 else
                                                  f"`({S.i},{S.j})` 是农场但已在某个农场组里 → 跳过" if S.i * S.n + S.j in S.used else
                                                  f"`({S.i},{S.j})` 是农场且没访问过 → 发现新农场组，从这里 BFS"),
        'q = [[i, j]]': '队列从左上角 `[{i}, {j}]` 开始：==队首就是农场组左上角==；`q[l:r]` 是当前一层',
        'for nowx, nowy': '取出这一层的格子 `({nowx}, {nowy})`',
        'if x >= 0': lambda S, B, r: (f"邻居 `({S.x},{S.y})` 在界内、未访问、是农场 → 入队" if 0 <= S.x < S.m and 0 <= S.y < S.n and S.x * S.n + S.y not in B.used and S.land[S.x][S.y] == 1
                                      else f"邻居 `({S.x},{S.y})` 越界 / 已访问 / 是森林 → 不入队"),
        'used.add(x * n + y)': '邻居入队并标记已访问：`q` 末尾加入 `[{x}, {y}]`',
        'l, r = r, len(q)': '这一层处理完：下一层是 `q[{l}:{r}]`',
        'res.append': 'BFS 从左上角开始、在右下角结束 → ==队首 `{q[0]}`、队尾 `{q[-1]}`== 就是答案：`{res[-1]}`',
        'return res': '所有农场组：`{res}`',
    },
    cards=dict(
        one_liner='矩形农场组做 BFS：队首是左上角，队尾是右下角',
        complexity='时间 `O(nm)`，空间 `O(nm)`',
        problem=['`land` 里 1 是农场，农场组都是互不相邻的矩形',
                 '返回每个农场组的左上角与右下角 `[r1,c1,r2,c2]`',
                 '示例：`[[1,0,0],[0,1,1],[0,1,1]]` → `[[0,0,0,0],[1,1,2,2]]`'],
        quote='对每一块农场组的bfs都是从农场组的左上角开始，而bfs必然于农场组的右下角结束，这也就意味着队列首尾的位置恰好就是题目要找的答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目保证是标准矩形且互不相邻，用经典 floodfill 找连通块',
              '按行扫描先碰到的一定是左上角，BFS 分层向右下扩展',
              '最后入队的是右下角，不用再算边界'],
        summary=['时间 `O(nm)`，空间 `O(nm)`（`used` 与队列）',
                 '用 `i * n + j` 把二维坐标压成一个整数放进 `set`',
                 '易错点：`q[l:r]` 是当前层，进入下一层要 `l, r = r, len(q)`',
                 '原文为 Python 2 风格，仅为 Python 3 运行，代码无需改动'],
    ),
)
