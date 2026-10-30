G1 = [[1, 1, 0, 1], [0, 1, 0, 0], [1, 0, 0, 1]]
G2 = [[1, 1, 0, 1], [0, 1, 0, 1], [1, 0, 0, 0]]


def _islands(g):
    # 只用于着色：求 grid2 的每个格子属于哪个岛屿
    m, n = len(g), len(g[0])
    comp = {}
    for i in range(m):
        for j in range(n):
            if g[i][j] == 1 and (i, j) not in comp:
                st, cells = [(i, j)], []
                comp[(i, j)] = cells
                while st:
                    a, b = st.pop()
                    cells.append((a, b))
                    for da, db in ((1, 0), (0, 1), (-1, 0), (0, -1)):
                        x, y = a + da, b + db
                        if 0 <= x < m and 0 <= y < n and g[x][y] == 1 and (x, y) not in comp:
                            comp[(x, y)] = cells
                            st.append((x, y))
    return comp


COMP = _islands(G2)


def _in_q(S, i, j):
    return 'q' in S and [i, j] in S['q']


def _bfs_on(S):
    return S.get('_line') in range(13, 33) and 'q' in S


def _g2_color(S, i, j, v):
    used = S.get('used')
    if v == 1 and _bfs_on(S) and _in_q(S, i, j):
        return 'orange' if S.get('flag') is False else 'yellow'
    if v != 1 or used is None or not used[i][j]:
        if S.get('_line') == 22 and v == 1 and abs(i - S['nowx']) + abs(j - S['nowy']) == 1:
            return 'purple'
        return None
    if _bfs_on(S) and _in_q(S, i, j):
        return 'orange' if S.get('flag') is False else 'yellow'
    ok = all(G1[a][b] == 1 for a, b in COMP[(i, j)])
    return 'green' if ok else 'pink'


def _g1_color(S, i, j, v):
    if _bfs_on(S) and _in_q(S, i, j):
        return 'green' if v == 1 else 'red'
    return None


def _cur(S):
    if S.get('_line') in (22,) and 'nowx' in S:
        return S['nowx'], S['nowy']
    if S.get('_line') in (28, 32) and 'x' in S:
        return S['x'], S['y']
    if 'i' in S and 'j' in S:
        return S['i'], S['j']
    return None, None


def _q_items(S):
    q = S.get('q')
    if q is None:
        return None
    return [f'({a},{b})' for a, b in q]


def _text(S):
    if 'flag' not in S or not _bfs_on(S):
        return f"子岛屿数 `res = {S.get('res', 0)}`（绿 = 子岛屿，粉 = 不是）"
    if S['flag']:
        return '当前岛屿 `flag = True`：目前每个格子在 grid1 里==都是 1=='
    return '当前岛屿 `flag = False`：有格子在 grid1 里是水 → ==不是子岛屿=='


def _outer(S, B, ret):
    i, j = S['i'], S['j']
    if S['grid2'][i][j] == 0:
        return f'`({i},{j})` 是水，跳过'
    if S['used'][i][j]:
        return f'`({i},{j})` 已经被之前的 bfs 访问过，跳过'
    return f'`({i},{j})` 是==没访问过的陆地== → 从这里开始一次新的 bfs'


def _pop(S, B, ret):
    x, y = S['nowx'], S['nowy']
    return f'队首出队 `({x},{y})`，看它==上下左右==四个格子（紫 = 待扩展的陆地）'


def _append(S, B, ret):
    x, y = S['x'], S['y']
    g = S['grid1'][x][y]
    tail = '在 grid1 里也是陆地' if g == 1 else '但在 grid1 里是==水=='
    return f'`({x},{y})` 界内、是陆地、没访问过 → 入队并标记 used；{tail}'


def _while(S, B, ret):
    if S['l'] < S['r']:
        return f'队列里还有 `r − l = {S["r"] - S["l"]}` 个格子没扩展'
    k = len(S['q'])
    return f'队列空了：这次 bfs 触达的 {k} 个格子就是==一个岛屿=='


CONFIG = dict(
    num=1905, title='统计子岛屿', difficulty='Medium', category='图论',
    author='yiduobo', technique='floodfill（bfs）时顺便检查 grid1',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def countSubIslands(self, grid1, grid2):
        m = len(grid1)
        n = len(grid1[0])

        used = [[False] * n for _ in range(m)]
        res = 0
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        for i in range(m):
            for j in range(n):
                if grid2[i][j] == 1 and not used[i][j]:
                    q = [[i, j]]
                    used[i][j] = True
                    if grid1[i][j] == 1:
                        flag = True
                    else:
                        flag = False
                    l = 0
                    r = 1
                    while l < r:
                        nowx, nowy = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid2[x][y] == 1 and not used[x][y]:
                                q.append([x, y])
                                used[x][y] = True
                                r += 1
                                if grid1[x][y] == 0:
                                    flag = False

                    if flag:
                        res += 1

        return res
''',
    call=f'Solution().countSubIslands({G1!r}, {G2!r})',
    expect=2,
    views=[
        dict(type='text', fn=_text, h=56),
        dict(type='grid', var='grid2', label='grid2（黄 = 当前岛屿，绿 = 子岛屿，粉 = 不是子岛屿）', cell=70,
             color=_g2_color, cursors=[(lambda S: _cur(S)[0], lambda S: _cur(S)[1], 'cyan')], h=250),
        dict(type='grid', var='grid1', label='grid1（当前岛屿对应位置：绿 = 陆地，红 = 水）', cell=70,
             color=_g1_color, cursors=[(lambda S: _cur(S)[0], lambda S: _cur(S)[1], 'cyan')], h=250),
        dict(type='array', var=_q_items, label='q（bfs 队列，暗 = 已出队，l = 队首）', cell=96,
             pointers={'l': 'blue'}, dim=lambda S, k, v: k < S['l'] if 'l' in S else False, h=150),
    ],
    watch=[('flag', 'flag', 'yellow'), ('res', 'res', 'green')],
    skip=[3, 4, 6, 7, 8, 10, 11, 14, 15, 19, 20, 23, 24, 25, 26, 27, 29, 30, 31],
    captions={
        'dy = [0, 1, 0, -1]': '`dx`、`dy`：上下左右四个方向；`used` 记录 grid2 里访问过的格子',
        'if grid2[i][j] == 1 and not used': _outer,
        'q = [[i, j]]': '起点 `({i},{j})` 入队，标记已访问',
        16: '起点在 grid1 里是陆地 → 先假设是子岛屿：`flag = True`',
        18: '起点在 grid1 里就是水 → `flag = False`',
        'while l < r': _while,
        'nowx, nowy = q[l]': _pop,
        'q.append([x, y])': _append,
        32: '`grid1[{x}][{y}] == 0`：这个格子在 grid1 里是水 → ==`flag = False`==',
        'if flag:': lambda S, B, ret: ('`flag = True`：岛屿每个格子在 grid1 里都是 1 → ==是子岛屿=='
                                       if S['flag'] else '`flag = False` → 不是子岛屿，不计数'),
        'res += 1': '子岛屿个数 `res` → =={res}==',
        'return res': 'grid2 扫描完毕，子岛屿共 =={ret}== 个',
    },
    cards=dict(
        one_liner='floodfill 找 grid2 的岛屿，顺便检查每个格子在 grid1 里是不是 1',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['两个 `m × n` 的 0/1 矩阵：1 是陆地，0 是水，岛屿是四联通的 1',
                 'grid2 的岛屿若被 grid1 的==同一个岛屿完全包含==，就叫子岛屿',
                 '返回 grid2 中子岛屿的数目',
                 '本视频：3 × 4 的小例子，答案是 `2`'],
        quote='最简单的想法的就是判断grid2中各个岛屿的每个格子在grid1中是否都是1。恰好floodfill将遍历grid2中的每个格子，那么这个判断就可以==在floodfill执行的过程中顺便进行==。',
        quote_src='—— yiduobo 题解原文',
        idea=['逐格扫描 grid2：遇到没访问过的陆地，就从它开始 bfs，触达的格子就是一个岛屿',
              '`flag` 记录这个岛屿的格子在 grid1 里是否==全是 1==',
              'bfs 中发现某格子在 grid1 是 0 → `flag = False`；bfs 结束时 `flag` 为真就计数'],
        summary=['时间 `O(mn)`：每个格子最多入队一次；空间 `O(mn)`（used + 队列）',
                 '为什么全是 1 就够了？grid1 里四联通的 1 必属于==同一个==岛屿',
                 '易错：发现水也不能提前停止 bfs，否则剩下的格子会被当成新岛屿',
                 '队列用数组 + 头指针 `l` 模拟，`r` 是队尾（入队个数）',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
