GRID = [[1, 1, 0], [1, 0, 0], [0, 0, 1]]


def _cell(S, i, j, v):
    if 'p' not in S:
        return None
    if S['p'][j] == i:
        return 'green'
    if v == 1:
        return None
    return 'dim'


def _boy(S):
    """当前正在为哪个男孩找配对：最内层是 match(i)，外层最老的 i 是发起者"""
    return S['_inner'].get('i')


def _match_cap(S, B, ret):
    j, i = S.j, S.i
    if B.grid[i][j] != 1:
        return f'男孩 `{i}` 对女孩 `{j}` 没有好感（`grid[{i}][{j}] = 0`）→ 看下一个女孩'
    if B.vis[j]:
        return f'女孩 `{j}` 这一轮已经试过了（`vis[{j}]` 为真）→ 跳过，避免死循环'
    return f'男孩 `{i}` 喜欢女孩 `{j}`，且这一轮还没试过她 → 去试试'


CONFIG = dict(
    num=1820, title='最多邀请的个数', difficulty='Medium', category='图论算法',
    author='yiduobo', technique='匈牙利算法（二分图最大匹配）',
    tags=['灵神题单·图论算法', '灵神题单·动态规划'],
    code='''
class Solution(object):
    def maximumInvitations(self, grid):

        m = len(grid)
        n = len(grid[0])
        p = [None] * n

        def match(i):
            for j in range(n):
                if grid[i][j] == 1 and not vis[j]:
                    vis[j] = True
                    if p[j] is None or match(p[j]):
                        p[j] = i
                        return True
            return False

        res = 0
        for i in range(m):
            vis = [False] * n
            if match(i):
                res += 1
        
        return res
''',
    call=f'Solution().maximumInvitations({GRID})',
    expect=3,
    views=[
        dict(type='grid', var='grid', label='grid（行 = 男孩，列 = 女孩；1 = 愿意；绿 = 当前配对）', cell=84, h=300,
             rows=lambda S: [f'男{i}' for i in range(len(S['grid']))],
             cols=lambda S: [f'女{j}' for j in range(len(S['grid'][0]))],
             color=lambda S, i, j, v: ('green' if S.get('p') and S['p'][j] == i else None),
             cursors=[('_inner.get("i") if "j" in _inner else None', '_inner.get("j")', 'blue')]),
        dict(type='array', var='p', label='p[j]：女孩 j 目前配给的男孩（None = 单身）', cell=84, h=150,
             color=lambda S, i, v: 'green' if v is not None else None),
        dict(type='array', var=lambda S: S.get('vis'), label='vis[j]：本轮是否已被试探过', cell=84, h=150,
             color=lambda S, i, v: 'yellow' if v else None),
        dict(type='calls', h=170),
    ],
    watch=[('res', 'res', 'green'), 'i', 'j'],
    captions={
        'p = [None] * n': '`p[j]` 记录女孩 `j` 配给了谁，开始都是 `None`（单身）',
        'for i in range(m)': lambda S, B, r: (f'依次为每个男孩 `{S.i}` 找对象' if S.i != B.get('i', -1) or 'vis' not in B else '男孩都处理完了，循环结束'),
        'vis = [False] * n': '每个男孩重新开一张 `vis`：这一轮每个女孩最多试探一次',
        'if match(i)': lambda S, B, r: (f'男孩 `{S.i}` 配对成功 → 匹配数 +1' if r is True else
                                         f'男孩 `{S.i}` 开始找对象：调用 `match({S.i})`'),
        'for j in range(n)': '依次看每个女孩 `{j}`',
        'if grid[i][j] == 1': _match_cap,
        'vis[j] = True': '先标记女孩 `{j}` 已试探',
        'if p[j] is None': lambda S, B, r: (f'女孩 `{S.j}` 单身（`p[{S.j}] = None`）→ ==直接配对==' if B.p[S.j] is None
                                             else f'女孩 `{S.j}` 已配给男孩 `{B.p[S.j]}` → 让他 `match({B.p[S.j]})` 去换别的女孩'),
        'p[j] = i': '女孩 `{j}` 配给男孩 `{i}`：`p = {p}`',
        'return True': '配对成功，返回 `True`',
        'return False': '所有女孩都试过了，没有办法 → `False`',
        'res += 1': '又多一对：`res = {res}`',
        'return res': '最多邀请 `{res}` 对',
    },
    cards=dict(
        one_liner='男孩依次出手：女孩单身就配，否则让她的男友换人',
        complexity='时间 `O(m·n·n)`（本写法邻接矩阵，每个男孩一次 DFS 最多 `O(mn)`），空间 `O(m+n)`',
        problem=['`m` 个男孩、`n` 个女孩，`grid[i][j] = 1` 表示男孩 `i` 可以邀请女孩 `j`',
                 '每个男孩最多邀请一个女孩，每个女孩最多接受一个邀请',
                 '求最多能成功邀请的人数',
                 '本视频：`[[1,1,0],[1,0,0],[0,0,1]]` → `3`'],
        quote='非常标准的最大匹配问题，常规做法是匈牙利算法或者建图后求最大流。',
        quote_src='—— yiduobo 题解原文',
        idea=['遍历每个男孩，看他能不能配上一个女孩',
              '女孩单身：直接配对；女孩已有男友：让那个男友==另找==一个女孩，找到了就把她让出来',
              '这条“让位链”就是增广路，每次成功匹配数 +1'],
        summary=['最大匹配 = 二分图上的最大流，匈牙利算法实现简单',
                 '每个男孩开始前要重置 `vis`，否则会漏掉可行的增广路',
                 '`vis` 在同一次递归中共享，保证一轮里每个女孩只被试探一次',
                 '原文为 Python 2 风格，只删去了类型说明，代码未改动'],
    ),
)
