GRID = [[1, 1, 0], [0, 1, 1], [0, 0, 1]]


def _gcolor(S, i, j, v):
    if 'linked' not in S or v != 1:
        return None
    n = len(S['grid'][0])
    k = i * n + j
    if (i + j) % 2 == 0:
        if 'p' in S and k in S['p'].values():
            return 'green'
        return 'blue'
    if 'p' in S and k in S['p']:
        return 'green'
    return 'pink'


def _ftxt(S):
    if 'p' not in S:
        return '偶数格 `(i+j)%2==0` 是左侧（蓝），奇数格是右侧（粉）；相邻的 1 连成一条边'
    n = len(S['grid'][0])
    if 'left' in S and 'res' in S:
        return f"当前匹配数 `res = {S['res']}`；p 记录「右端点 → 配对的左端点」（编号 = i×{n}+j）"
    return ''


CONFIG = dict(
    num=2123, title='使矩阵中的1互不相邻的最小操作数', difficulty='Hard', category='图论算法',
    author='yiduobo', technique='二分图最大匹配（匈牙利算法）',
    tags=['图论算法', '动态规划'],
    code='''
class Solution(object):
    def minimumOperations(self, grid):

        linked = {}
        m = len(grid)
        n = len(grid[0])

        for i in range(m):
            for j in range(n):
                if (i + j) % 2 == 0 and grid[i][j] == 1:
                    left = i * n + j
                    if left not in linked:
                        linked[left] = []

                    if i > 0 and grid[i - 1][j] == 1:
                        linked[left].append(left - n)
                    if i < m - 1 and grid[i + 1][j] == 1:
                        linked[left].append(left + n)
                    if j > 0 and grid[i][j - 1] == 1:
                        linked[left].append(left - 1)
                    if j < n - 1 and grid[i][j + 1] == 1:
                        linked[left].append(left + 1)

        p = {}
        def match(left):
            for right in linked[left]:
                if right not in vis:
                    vis.add(right)
                    if right not in p or match(p[right]):
                        p[right] = left
                        return True
            return False

        res = 0
        for left in linked:
            vis = set()
            if match(left):
                res += 1
        
        return res
''',
    call=f'Solution().minimumOperations({GRID})',
    expect=2,
    skip=['linked = {}', 'm = len', 'n = len', 'for i in range', 'for j in range', 'if left not in linked',
          'linked[left] = []', 'p = {}', 'def match', 'if i > 0 and', 'if i < m - 1 and', 'if j > 0 and', 'if j < n - 1 and', 'if (i + j) % 2'],
    views=[
        dict(type='grid', var='grid', label='grid（蓝 = 左侧偶数格的 1，粉 = 右侧奇数格的 1，绿 = 已匹配）', cell=90, h=260,
             color=_gcolor, cursors=[('i if _line < 34 else None', 'j', 'yellow')]),
        dict(type='map', var='linked', label='linked：左端点 → 相邻的右端点（编号 = i×n+j）', h=170,
             fmt=lambda k, v: f'{k} → {v}'),
        dict(type='map', var='p', label='p：右端点 → 配对的左端点', h=130, fmt=lambda k, v: f'{k} ← {v}'),
        dict(type='set', var='vis', label='vis：本轮已尝试过的右端点', h=100, fmt=lambda x: str(x)),
    ],
    watch=['left', 'right', ('res', 'res', 'green'), ('p', 'p')],
    captions={
        'left = i * n + j': '左侧点 `({i},{j})` 编号 `left = {left}`',
        'linked[left].append(left - n)': '上邻居也是 1：连边 `{left} — {left - n}`',
        'linked[left].append(left + n)': '下邻居也是 1：连边 `{left} — {left + n}`',
        'linked[left].append(left - 1)': '左邻居也是 1：连边 `{left} — {left - 1}`',
        'linked[left].append(left + 1)': '右邻居也是 1：连边 `{left} — {left + 1}`',
        'for right in linked[left]': '`left = {left}` 依次尝试相邻的右端点 `right = {right}`',
        'if right not in vis': lambda S, B, r: (f'`right = {S.right}` 本轮没试过，可以尝试' if S.right not in S.vis
                                                 else f'`right = {S.right}` 本轮试过了，跳过'),
        'vis.add(right)': '标记 `{right}` 已访问，避免本轮重复走',
        'if right not in p or match(p[right])': lambda S, B, r: ((f'`{S.right}` 还没配对 → 直接占用' if S.right not in S.p
                                                                 else f'`{S.right}` 已配给 `{S.p[S.right]}` → ==递归让它换一个==')),
        'p[right] = left': '配对成功：`{right}` ← `{left}`',
        'return True': '找到增广路，这一轮匹配数 +1',
        'return False': '所有相邻点都不行，没找到增广路',
        'vis = set()': '换一个左端点 `{left}`：vis 清空，重新找增广路',
        'if match(left)': '调用 `match({left})`：为这个左端点找一条增广路',
        'res += 1': '`res = {res}`',
        'return res': '最大匹配 `{res}` = 最小点覆盖（König 定理）= ==最少操作数 {res}==',
    },
    cards=dict(
        one_liner='相邻的 1 连边成二分图，最少删点 = 最大匹配',
        complexity='时间 `O(V·E)`，空间 `O(V+E)`',
        problem=['`0/1` 矩阵，一次操作可把一个 `1` 变成 `0`',
                 '要让矩阵中==没有两个 1 上下左右相邻==，求最少操作数',
                 '本视频：`[[1,1,0],[0,1,1],[0,0,1]]` → `2`'],
        quote='对于棋盘位于(i, j)位置的位置，可以根据i + j的奇偶性将这些位置分为左右两侧，可以发现若两个位置相邻，那么这两个位置对应的点必然分处图的两侧。',
        quote_src='—— yiduobo 题解原文',
        idea=['每对相邻的 1 是一条边，要删最少的点覆盖所有边：==最小点覆盖==',
              '按 `i+j` 奇偶分左右两侧，相邻格必在两侧 → 二分图',
              'König 定理：最小点覆盖 = 最大匹配，跑一遍匈牙利算法'],
        summary=['时间 `O(V·E)`，空间 `O(V+E)`',
                 '只从偶数格建边，每条边只建一次',
                 '`vis` 每个左端点重置一次；`match` 递归让已配对的左端点换伴',
                 '原文为 Python 2 风格，代码未改，可直接在 Python 3 运行'],
    ),
)
