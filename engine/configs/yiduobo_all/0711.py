GRID = [[1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 1, 1], [1, 1, 0, 0]]


def _color(S, i, j, v):
    vis = S.get('vis')
    if vis and (i, j) in vis and v == 1:
        return 'green'
    return None


def _inq(S):
    q = S.get('q')
    return None if q is None else [f'{a},{b}' for a, b in q]


def _rel(S):
    if S.get('_inner', {}).get('t') is None:
        return None
    return [f'{a},{b}' for a, b in S['_inner']['t']]


_TR = {25: '旋转 90°，`(x,y)→(y,h−x)`（`h−x` 修正成非负）', 28: '旋转 180°，`(x,y)→(h−x,w−y)`',
       31: '旋转 270°，`(x,y)→(w−y,x)`', 34: '横轴翻转，`(x,y)→(h−x,y)`', 37: '翻转后转 90°，`(x,y)→(y,x)`',
       40: '翻转后转 180°，`(x,y)→(x,w−y)`', 43: '翻转后转 270°，`(x,y)→(w−y,h−x)`'}


def _txt(S):
    inn = S.get('_inner', {})
    if 't' not in inn:
        return '先 BFS 找出一块连通块，再给它算一个==与旋转、翻转无关==的指纹 `key`'
    h, w = inn.get('h'), inn.get('w')
    if h is None:
        return '连通块里每个格子减去最小行、最小列 → 相对坐标 `t`'
    s = f'连通块外框：高 `h = {h}`，宽 `w = {w}`'
    if 'key' in inn:
        s += f'；当前最小 key = `{inn["key"]}`'
    return s


def _keys(S):
    return S.get('parts_set')


CONFIG = dict(
    num=711, title='不同岛屿的数量II', difficulty='Hard', category='网格图',
    author='yiduobo', technique='连通块相对坐标 · 8 种变换取最小 key',
    tags=['灵神题单'],
    code='''
class Solution(object):
    def numDistinctIslands2(self, grid):

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        vis = set()
        parts_set = set()

        def encode(q):
            min_x, min_y = q[0]
            for x, y in q[1:]:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
            
            t = []
            h = w = 0
            for x, y in q:
                t.append([x - min_x, y - min_y])
                h = max(h, x - min_x)
                w = max(w, y - min_y)
            
            key = '|'.join([str(x) + ',' + str(y) for x, y in sorted(t)])

            tmp = [[y, h - x] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[h - x, w - y] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[w - y, x] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[h - x, y] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[y, x] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[x, w - y] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            tmp = [[w - y, h - x] for x, y in t]
            key = min(key, '|'.join([str(x) + ',' + str(y) for x, y in sorted(tmp)]))

            return key

        m = len(grid)
        n = len(grid[0])
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and (i, j) not in vis:
                    vis.add((i, j))
                    q = [[i, j]]
                    head, tail = 0, 1
                    while head < tail:
                        nowx, nowy = q[head]
                        head += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if 0 <= x < m and 0 <= y < n and grid[x][y] == 1 and (x, y) not in vis:
                                q.append([x, y])
                                vis.add((x, y))
                                tail += 1
                    
                    key = encode(q)
                    parts_set.add(key)
        
        return len(parts_set)
''',
    call=f'Solution().numDistinctIslands2({GRID})',
    expect=2,
    skip=['dx = [', 'dy = [', 'vis = set()', 'parts_set = set()', 'm = len', 'n = len', 'for i in range(m)',
          'for j in range(n)', 'head += 1', 'for index in range(4)', 'x = nowx', 'y = nowy', 'tail += 1',
          'vis.add((x, y))', 'q.append([x, y])', 'min_x, min_y = q[0]', 'min_x = min', 'min_y = min',
          'for x, y in q[1:]', 'for x, y in q:', 'tmp = [[', 'h = w = 0', 'h = max', 'w = max', 't = []'],
    max_steps=52,
    views=[
        dict(type='grid', var='grid', label='grid（绿 = 已划入某个连通块；蓝框 = 当前出队格）', cell=84, h=330,
             color=_color, cursors=[('nowx', 'nowy', 'blue'), ('i if _line in (51, 52, 53) else None', 'j', 'yellow')]),
        dict(type='array', var=_inq, label='q（当前连通块的格子）', cell=70, h=140),
        dict(type='text', fn=_txt, size=26, h=90),
        dict(type='set', var=_keys, label='parts_set（已有的岛屿指纹）', fmt=lambda x: x, font=22, h=170),
    ],
    watch=[('i', 'i'), ('j', 'j'), ('len(q)', 'len(q)', 'blue'), ('len(parts_set)', 'len(parts_set)', 'green')],
    captions={
        'if grid[i][j] == 1 and (i, j) not in vis': lambda S, B, r: (
            f'`({S.i},{S.j})` 是陆地且没访问过 → ==新连通块的起点==' if S.grid[S.i][S.j] == 1 and (S.i, S.j) not in S.vis
            else f'`({S.i},{S.j})` 是水或已属于某个连通块，跳过'),
        'q = [[i, j]]': '从 `({i},{j})` 开始 BFS，`q` 收集整个连通块',
        'while head < tail': lambda S, B, r: (f'队列还有格子（`head = {S.head} < tail = {S.tail}`）' if S.head < S.tail
                                              else f'`head == tail`：连通块收集完毕，共 `{len(S.q)}` 格'),
        'nowx, nowy = q[head]': '取出 `({nowx},{nowy})`，看它四个方向的邻居',
        'if 0 <= x < m and': lambda S, B, r: (f'邻居 `({S.x},{S.y})` 是未访问的陆地 → 加入连通块'
                                              if 0 <= S.x < S.m and 0 <= S.y < S.n and S.grid[S.x][S.y] == 1 and (S.x, S.y) not in S.vis
                                              else f'邻居 `({S.x},{S.y})` 不是未访问的陆地（越界 / 水 / 已访问），不加'),
        'key = encode(q)': '连通块收齐，调用 `encode` 算它的指纹',
        'parts_set.add(key)': lambda S, B, r: f'指纹 `{S.key}` 放进集合；集合大小 ==`{len(S.parts_set)}`==',
        'def encode': '进入 encode：旋转、翻转后相同的岛要得到同一个 key',
        "key = '|'.join": lambda S, B, r: f'原始朝向的 key：排序后的相对坐标 `{S.key}`',
        'key = min(': lambda S, B, r: (
            f'{_TR[S["_line"]]}：key 更小 → 取它 `{S.key}`' if S.key != B.key
            else f'{_TR[S["_line"]]}：key 不比 `{S.key}` 小，最小 key 不变'),
        'return key': '8 种姿态里字典序最小的 key 就是这座岛的指纹：`{key}`',
        'return len': '集合里共有 `{len(parts_set)}` 种指纹 → 答案 `{len(parts_set)}`',
    },
    cards=dict(
        one_liner='8 种旋转、翻转各算一个 key，取最小的当岛屿指纹',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['`grid` 中 1 是陆地，相连的 1 构成岛屿',
                 '两座岛经==旋转（90 / 180 / 270°）或翻转==后能重合，也算相同',
                 '示例：`[[1,1,0,0],[1,0,0,1],[0,0,1,1],[1,1,0,0]]`',
                 '→ `2`（两个 L 形旋转后相同，另一个是横条）'],
        quote='接下来，对(col, h - row)进行同样的90度旋转，得到(h - row, w - col)，就是(row, col)旋转180度得到的结果了。',
        quote_src='—— yiduobo 题解原文',
        idea=['减去最小行列得相对坐标，记外框高 `h`、宽 `w`',
              '旋转 90° 是 `(r,c) → (c, h−r)`，再转两次得 180°、270°',
              '翻转一次，再转三次，共 8 种姿态，各自排序拼成字符串，取最小'],
        summary=['时间 `O(mn log(mn))`：每格要排序 8 次，空间 `O(mn)`',
                 '易错：每次变换后都要重新 `sorted`，否则同一形状会得到不同 key',
                 '易错：变换后要用 `h − x`、`w − y` 修正成非负坐标',
                 '对比第 694 题：694 只需平移，用 DFS 序列即可；本题多了旋转翻转，只能老实哈希',
                 '原文代码是 Python 3 可运行的写法，未做修改'],
    ),
)
