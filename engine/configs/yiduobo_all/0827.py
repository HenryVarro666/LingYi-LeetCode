_PAL = ['green', 'pink', 'purple', 'cyan', 'orange']


def _col(S, i, j, v):
    c = S.get('color')
    if c is None or c[i][j] is None:
        return None
    return _PAL[c[i][j] % len(_PAL)]


CONFIG = dict(
    num=827, title='最大人工岛', difficulty='Hard', category='网格图',
    author='yiduobo', technique='BFS 染色 + 统计相邻颜色',
    tags=['灵神题单', '网格图', '难度分 1934'],
    code='''
class Solution(object):
    def largestIsland(self, grid):

        m = len(grid)
        n = len(grid[0])
        color = [[None] * n for _ in range(m)]
        now = 0
        q = []
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
        cnt = []
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and color[i][j] is None:
                    q = [[i, j]]
                    l = 0
                    r = 1
                    color[i][j] = now
                    while l < r:
                        nowx, nowy = q[l]
                        l += 1
                        for index in range(4):
                            x = nowx + dx[index]
                            y = nowy + dy[index]
                            if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1 and color[x][y] is None:
                                color[x][y] = now
                                q.append([x, y])
                                r += 1

                    cnt.append(r)    
                    now += 1
        
        if now == 0:
            return 1
        res = max(cnt)
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 0:
                    linked_set = set()
                    for index in range(4):
                        x = i + dx[index]
                        y = j + dy[index]
                        if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:
                            linked_set.add(color[x][y])
                    
                    res = max(res, sum(cnt[x] for x in linked_set) + 1)
        
        return res
''',
    call='Solution().largestIsland([[1,1,0],[1,0,1],[0,0,0]])',
    expect=5,
    skip=['m = len', 'n = len', 'color = [[', 'q = []', 'dx = [', 'dy = [', 'cnt = []', 'for i in range', 'for j in range',
          'l += 1', 'r += 1', 'for index in range', 'x = nowx', 'y = nowy', 'x = i + dx', 'y = j + dy', 'l = 0', 'r = 1', 'q.append', 14],
    max_steps=90,
    views=[
        dict(type='grid', var='grid', label='grid（同色 = 同一个岛；黄框 = 正在看的格子）', cell=92, h=300,
             color=_col, cursors=[('i', 'j', 'yellow', '')]),
        dict(type='array', var='cnt', label='cnt（下标 = 颜色编号，值 = 岛面积）', cell=70, h=130),
        dict(type='set', var=lambda S: S.get('linked_set') if S['_line'] >= 37 else None, label='linked_set（周围的颜色，自动去重）', h=110),
        dict(type='text', h=60, fn=lambda S: (f"BFS 队列 `{S['q']}`，已出队 `{S['l']}` 个" if 'q' in S and 'l' in S and S['_line'] <= 29 and S['_line'] >= 19 else '')),
    ],
    watch=[('now', 'now', 'cyan'), ('res', "res if 'res' in _inner else None", 'green')],
    captions={
        'q = [[i, j]]': '`({i},{j})` 是陆地且没染色 → ==新的岛==：起点入队，用颜色 `{now}` 开始 BFS',
        'color[i][j] = now': '起点染成 `{now}`',
        'while l < r': lambda S, B, r: (f'`l = {B.l} < r = {B.r}`：队里还有格子' if B.l < B.r else f'`l = r = {B.r}`：整个岛染完了，面积就是 `r = {B.r}`'),
        'nowx, nowy = q[l]': '出队 `({nowx},{nowy})`，去看它的四个邻居',
        'if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1 and color': lambda S, B, r: (
            f'邻居 `({S.x},{S.y})` 出界' if not (0 <= S.x < S.m and 0 <= S.y < S.n)
            else (f'邻居 `({S.x},{S.y})` 是陆地且没染色 → ==染色并入队==' if S.grid[S.x][S.y] == 1 and S.color[S.x][S.y] is None
                  else f'邻居 `({S.x},{S.y})` 是水或已染色 → 不扩展')),
        'color[x][y] = now': '`({x},{y})` 染成 `{now}`，入队',
        'cnt.append(r)': '队列最终大小 `r = {r}` 就是这个岛的面积：`cnt` 追加 `{r}`',
        'now += 1': '下一个岛用颜色 `{now}`',
        'if now == 0': lambda S, B, r: '没有任何岛 → 整个图是水，填一格得 1' if B.now == 0 else '`now = {}`：有岛，继续'.format(B.now),
        'res = max(cnt)': '先取最大的现有岛 `{res}`：不填也可能是答案（比如没有水）',
        'if grid[i][j] == 0': lambda S, B, r: (f'`({S.i},{S.j})` 是水 → 试着把它填成陆地' if S.grid[S.i][S.j] == 0 else f'`({S.i},{S.j})` 已是陆地 → 跳过'),
        'linked_set = set()': '用集合收集周围的颜色，==同色只记一次==',
        'if x >= 0 and x < m and y >= 0 and y < n and grid[x][y] == 1:': lambda S, B, r: (
            f'邻居 `({S.x},{S.y})` 出界' if not (0 <= S.x < S.m and 0 <= S.y < S.n)
            else (f'邻居 `({S.x},{S.y})` 是陆地，颜色 `{S.color[S.x][S.y]}` → ==记下==' if S.grid[S.x][S.y] == 1 else f'邻居 `({S.x},{S.y})` 是水 → 不管')),
        'linked_set.add': lambda S, B, r: (f'颜色 `{S.color[S.x][S.y]}` 已在集合里 → ==去重，不重复加面积==，`{S.linked_set}`' if S.color[S.x][S.y] in B.linked_set
                                           else f'颜色 `{S.color[S.x][S.y]}` 加入集合：`{S.linked_set}`'),
        'res = max(res': lambda S, B, r: (f'`linked_set = {S.linked_set or "空集"}`：面积 = ' + ''.join(f'`{S.cnt[c]}` + ' for c in sorted(S.linked_set)) + f'1（填的这格） = =={sum(S.cnt[c] for c in S.linked_set) + 1}==，`res = {S.res}`'),
        'return res': '最大岛屿面积 `{res}`',
    },
    cards=dict(
        one_liner='先给每个岛染色并记面积，再看每个水格能连起哪些颜色',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`n x n` 的 0/1 网格，最多把一个 0 变成 1',
                 '求操作后最大的岛屿面积',
                 '示例：`[[1,1,0],[1,0,1],[0,0,0]]` → `5`'],
        quote='首先，将初始地图上连续的部分通过bfs进行染色，并统计当前颜色格子的数量。接下来遍历每个空白的格子，检测这个格子能连接哪些颜色，计算这些颜色格子的总数，再加上表示空白格子的1。',
        quote_src='—— yiduobo 题解原文',
        idea=['BFS 一片一片染色，队列最终大小 `r` 就是面积',
              '只填一格，不需要并查集（对比 803 打砖块）',
              '每个水格：周围颜色放进集合去重，面积相加再 +1'],
        summary=['时间 `O(mn)`，空间 `O(mn)`',
                 '两个特殊情况：全是水返回 1（`now == 0`）；没有水时答案是最大岛（`res = max(cnt)` 初值）',
                 '易错：同一个岛从两个方向相邻，必须用集合去重',
                 '原文是 Python 2 风格写法，但无需改动，代码未改',
                 '对比灵神：灵神 DFS 把岛编号直接写回 grid，yiduobo 用单独的 color 数组'],
    ),
)
