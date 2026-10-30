_PAL = ['green', 'pink', 'purple', 'cyan', 'orange']


def _root(fa, v):
    while fa[v] != v:
        v = fa[v]
    return v


def _land(S):
    fa, m, n = S.get('fa'), S.get('m'), S.get('n')
    if fa is None or m is None:
        return None
    return [[(1 if i * n + j in fa else 0) for j in range(n)] for i in range(m)]


def _col(S, i, j, v):
    fa, n = S.get('fa'), S['n']
    if not fa or i * n + j not in fa:
        return None
    return _PAL[_root(fa, i * n + j) % len(_PAL)]


def _nb(S, B, r):
    xx, yy, m, n = S.xx, S.yy, S.m, S.n
    if not (0 <= xx < m and 0 <= yy < n):
        return f'邻居 `({xx},{yy})` 出界'
    vv = xx * n + yy
    if vv in S.fa:
        return f'邻居 `({xx},{yy})`（编号 {vv}）是陆地 → ==看是不是同一个连通块=='
    return f'邻居 `({xx},{yy})` 还是水 → 不管'


CONFIG = dict(
    num=305, title='岛屿数量II', difficulty='Hard', category='网格图',
    author='yiduobo', technique='并查集 · 加陆地时合并',
    tags=['灵神题单', '网格图'],
    code='''
class Solution(object):
    def numIslands2(self, m, n, positions):

        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]
        fa = {}

        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]

        res = []
        now = 0
        for x, y in positions:
            v = x * n + y
            if v not in fa:
                fa[v] = v
                now += 1

                for index in range(4):
                    xx = x + dx[index]
                    yy = y + dy[index]
                    if xx >= 0 and xx < m and yy >= 0 and yy < n:
                        vv = xx * n + yy
                        if vv in fa:
                            fa_vv = find(vv)
                            if fa_vv != v:
                                fa[fa_vv] = v
                                now -= 1
            res.append(now)
        
        return res
''',
    call='Solution().numIslands2(3, 3, [[0, 0], [0, 2], [0, 1], [2, 2]])',
    expect=[1, 2, 1, 2],
    skip=['dx = [', 'dy = [', 'fa = {}', 'def find', 'res = []', 'for index in range', 'xx = x + dx', 'yy = y + dy', 'vv = xx', 'now = 0', 26],
    max_steps=80,
    views=[
        dict(type='grid', var=_land, label='海面（有色 = 陆地，同色 = 同一个岛；黄框 = 这次新加的格子）', cell=88, h=290,
             color=_col, values=False, cursors=[('x', 'y', 'yellow', '')]),
        dict(type='map', var='fa', label='fa（格子编号 x*n+y → 父节点；指向自己 = 岛的代表）', h=150),
        dict(type='array', var='res', label='res（每次加陆地后的岛屿数）', cell=70, h=110),
    ],
    watch=[('now', 'now', 'cyan'), ('x,y', "(_inner.get('x'), _inner.get('y'))", 'yellow')],
    captions={
        'for x, y in positions': lambda S, B, r: (f'第 `{len(S.res) + 1}` 次：把 `({S.x},{S.y})` 变成陆地' if len(S.res) < len(S.positions)
                                                  else '`positions` 都处理完了'),
        'v = x * n + y': '格子 `({x},{y})` 编号 `v = x*n + y = {v}`，并查集里的节点就是这个编号',
        'if v not in fa': lambda S, B, r: (f'`{S.v}` 还不在 `fa` 里 → 它原来是水，真的新增陆地' if S.v not in S.fa
                                           else f'`{S.v}` 已在 `fa` 里 → 重复添加，什么都不变'),
        'fa[v] = v': '`fa[{v}] = {v}`：先自成一个新岛',
        'now += 1': '新岛 +1：`now = {now}`',
        'if xx >= 0 and xx < m': _nb,
        'fa_vv = find(vv)': '`find({vv})`：顺着 `fa` 往上找邻居所在岛的代表',
        'if fa_vv != v': lambda S, B, r: (f'邻居岛的代表 `{S.fa_vv}` ≠ 自己 `{S.v}` → 原来是两个岛，==要合并==' if S.fa_vv != S.v
                                          else f'邻居岛的代表就是 `{S.v}`（前面已经并过）→ 不用合并'),
        'fa[fa_vv] = v': '把邻居岛的代表 `{fa_vv}` 挂到 `{v}` 下：两个岛并成一个',
        'now -= 1': '两个岛合并 → 岛屿数 -1：`now = {now}`',
        'res.append(now)': '这次操作后共有 `{now}` 个岛 → `res = {res}`',
        'return res': '全部操作完成：`{res}`',
    },
    cards=dict(
        one_liner='加一块陆地就是加一个新岛，每并掉一个邻居岛就少一个',
        complexity='时间 `O(k·α(mn))`（k 为操作数），空间 `O(k)`',
        problem=['`m × n` 的网格最初全是水，依次把 `positions` 里的格子变成陆地',
                 '每次变化后，返回当前岛屿（上下左右相连的陆地）的数量',
                 '示例：`m=3, n=3`，`[[0,0],[0,2],[0,1],[2,2]]` → `[1,2,1,2]`'],
        quote='对于本题，每当一个格子转换成陆地时，若这个格子之前是水域，那么就应该将当前连通块的数量now加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['题目相当于不断往图里加边，每次问连通块数量 → 并查集',
              '新格子先 `now += 1`，再看四个邻居：是陆地且不在同一块 → 合并、`now -= 1`',
              '格子编号 `x*n + y`，并查集用字典，只存陆地'],
        summary=['时间 `O(k·α)`，不用每次重新扫整张图',
                 '易错：重复添加同一格要跳过（`v not in fa`）；同一个邻居岛不能合并两次（`fa_vv != v`）',
                 '本题是 LeetCode 会员题，题面按 yiduobo 题解和原题整理',
                 '原文是 Python 2 风格写法，但无需改动，代码未改'],
    ),
)
