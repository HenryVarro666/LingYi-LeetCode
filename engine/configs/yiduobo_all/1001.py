def _lit(S, i, j):
    n = S['N']
    return (S['row'].get(i, 0) > 0 or S['col'].get(j, 0) > 0
            or S['left'].get(i - j + n, 0) > 0 or S['right'].get(i + j, 0) > 0)


def _grid(S):
    if 'lamp_set' not in S or 'row' not in S:
        return None
    n = S['N']
    return [['灯' if (i, j) in S['lamp_set'] else '' for j in range(n)] for i in range(n)]


def _gcolor(S, i, j, v):
    if v:
        return 'yellow'
    if 'row' in S and _lit(S, i, j):
        return 'cyan'
    return None


def _txt(S):
    if 'row' not in S:
        return '`N × N` 网格，灯照亮所在行、列和两条对角线'
    return '黄 = 亮着的灯，蓝 = 被照亮的格子；询问格用黄框，邻居格用粉框'


def _qcap(S, B, r):
    x, y, n = S.x, S.y, S.N
    a = (S.row.get(x, 0), S.col.get(y, 0), S.left.get(x - y + n, 0), S.right.get(x + y, 0))
    why = [t for t, c in zip(('行', '列', '\\ 对角线', '/ 对角线'), a) if c > 0]
    if why:
        return f'询问 `({x},{y})`：{"、".join(why)}上有亮灯 → ==被照亮==，`res` 记 1'
    return f'询问 `({x},{y})`：行、列、两条对角线上都没有亮灯 → ==没被照亮==，`res` 记 0'


def _nb(S, B, r):
    xx, yy = S.xx, S.yy
    if (xx, yy) in S.lamp_set:
        return f'邻居 `({xx},{yy})` 有亮灯 → ==要关掉==，先从 `lamp_set` 移除'
    return f'邻居 `({xx},{yy})` 没有亮灯（或在界外）→ 不用管'


CONFIG = dict(
    num=1001, title='网格照明', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='行/列/对角线哈希表计数',
    tags=[],
    code='''
class Solution(object):
    def gridIllumination(self, N, lamps, queries):

        lamp_set = set()
        row = {}
        col = {}
        left = {}
        right = {}

        for x, y in lamps:
            if (x, y) not in lamp_set:
                lamp_set.add((x, y))
                self.add(x, y, N, row, col, left, right, 1)
        
        res = []
        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]
        for x, y in queries:
            if row.get(x, 0) > 0 or col.get(y, 0) > 0 or left.get(x - y + N, 0) > 0 or right.get(x + y, 0) > 0:
                res.append(1)
            else:
                res.append(0)
            
            if (x, y) in lamp_set:
                lamp_set.remove((x, y))
                self.add(x, y, N, row, col, left, right, -1)

            for index in range(8):
                xx = x + dx[index]
                yy = y + dy[index]
                if (xx, yy) in lamp_set:
                    lamp_set.remove((xx, yy))
                    self.add(xx, yy, N, row, col, left, right, -1)
            
            

        return res
    
    def add(self, x, y, N, row, col, left, right, delta):
        row[x] = row.get(x, 0) + delta
        col[y] = col.get(y, 0) + delta
        left[x - y + N] = left.get(x - y + N, 0) + delta
        right[x + y] = right.get(x + y, 0) + delta
''',
    call='Solution().gridIllumination(5, [[0, 0], [4, 4]], [[1, 1], [1, 0]])',
    expect=[1, 0],
    views=[
        dict(type='text', fn=_txt),
        dict(type='grid', var=_grid, label='网格（行 x，列 y）', cursors=[('x', 'y', 'yellow', '(x,y)'), ('xx', 'yy', 'pink')],
             color=_gcolor, h=285, cell=48, rows=lambda S: list(range(S['N'])), cols=lambda S: list(range(S['N']))),
        dict(type='map', var='row', label='row：行 x → 亮灯数', h=93, font=18),
        dict(type='map', var='col', label='col：列 y → 亮灯数', h=93, font=18),
        dict(type='map', var='left', label='left：x - y + N（\\ 对角线）→ 亮灯数', h=93, font=18),
        dict(type='map', var='right', label='right：x + y（/ 对角线）→ 亮灯数', h=93, font=18),
    ],
    watch=['x', 'y', ('lamp_set', 'sorted(lamp_set)', 'yellow'), ('res', 'res', 'green')],
    skip=['row = {}', 'col = {}', 'left = {}', 'right = {}', 'dx = [', 'dy = [', 'res = []', 'for index in range(8)',
          'xx = x + dx', 'yy = y + dy[index]', 'else:'],
    max_steps=90,
    captions={
        'lamp_set = set()': '`lamp_set` 记录哪些位置的灯是开着的（同一位置的重复灯只算一盏）',
        'for x, y in lamps': lambda S, B, r: ('lamps 处理完：所有灯都登记进了四个哈希表' if 'x' in B and (S.x, S.y) == (B.x, B.y) and S.lamp_set else f'登记灯 `({S.x},{S.y})`'),
        'if (x, y) not in lamp_set': '`({x},{y})` 还没在 `lamp_set` 里吗？重复的灯不能重复计数',
        'lamp_set.add': '把 `({x},{y})` 记为开着',
        'self.add(x, y, N, row, col, left, right, 1)': '调用 `add(..., 1)`：四个哈希表对应的计数各 +1',
        'row[x] = ': '行 `{x}` 的亮灯数 → `row[{x}]` = =={row[x]}==',
        'col[y] = ': '列 `{y}` 的亮灯数 → `col[{y}]` = =={col[y]}==',
        'left[x - y + N] = ': '同一条 `\\` 对角线上 `x - y` 相同：`left[{x - y + N}]` = =={left[x - y + N]}==',
        'right[x + y] = ': '同一条 `/` 对角线上 `x + y` 相同：`right[{x + y}]` = =={right[x + y]}==',
        'for x, y in queries': lambda S, B, r: ('所有询问处理完毕' if 'y' in B and 'res' in B and len(S.res) == len(S.queries) else f'处理询问 `({S.x},{S.y})`'),
        'if row.get(x, 0) > 0': _qcap,
        'res.append(1)': '答案追加 1：`res` = {res}',
        'res.append(0)': '答案追加 0：`res` = {res}',
        'if (x, y) in lamp_set': lambda S, B, r: ('询问格上本身有灯 → 要关掉' if (S.x, S.y) in S.lamp_set else '询问格上没有灯，不用关'),
        'lamp_set.remove((x, y))': '关掉 `({x},{y})` 的灯：先从 `lamp_set` 移除',
        'self.add(x, y, N, row, col, left, right, -1)': '再调用 `add(..., -1)`：它所在行、列、两条对角线计数各 -1',
        'if (xx, yy) in lamp_set': _nb,
        'lamp_set.remove((xx, yy))': '关掉邻居灯 `({xx},{yy})`：从 `lamp_set` 移除',
        'self.add(xx, yy, N, row, col, left, right, -1)': '`add(..., -1)`：把它在四个哈希表里的计数减掉',
        'return res': '全部询问处理完，答案 `{res}`',
    },
    cards=dict(
        one_liner='灯照亮行、列、两条对角线：四个哈希表数灯',
        complexity='时间 `O(L + 9Q)`，空间 `O(L)`（L 灯数，Q 询问数）',
        problem=['`N×N` 网格，`lamps` 里的灯开着；灯照亮所在行、列和两条对角线',
                 '对每个询问 `(x, y)`：先答该格是否被照亮（1/0）',
                 '然后关掉 `(x, y)` 及其周围 8 格里的灯',
                 '示例：`N=5, lamps=[[0,0],[4,4]], queries=[[1,1],[1,0]]` → `[1,0]`'],
        quote='对于"/"这条右上到左下的对角线，同一条对角线上的灯都满足x + y相等，而对于"\\"这条左上到右下的对角线，同一条对角线上的灯则满足x - y相等。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `row`、`col`、`left`、`right` 四个哈希表，分别数每行、每列、每条对角线上亮着的灯',
              '再用 `lamp_set` 记录哪些位置的灯开着，查询时判断这四个表里有没有计数 > 0',
              '关灯时：从 `lamp_set` 删掉，并让它所在的四个计数各减 1'],
        summary=['时间 `O(L + Q)`，每个询问最多关 9 盏灯，空间 `O(L)`',
                 '易错：重复的灯只能算一盏，所以要先查 `lamp_set`',
                 '易错：`left` 的键用 `x - y + N` 避免负数；关灯时也要同步减计数',
                 '`add(delta)` 是辅助函数：开灯传 +1，关灯传 -1，四个表同步更新'],
    ),
)
