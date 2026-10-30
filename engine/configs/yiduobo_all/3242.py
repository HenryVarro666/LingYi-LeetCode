CONFIG = dict(
    num=3242, title='设计相邻元素求和服务', difficulty='Easy', category='设计',
    author='yiduobo', technique='哈希定位 + 缓存结果',
    tags=[],
    code='''
class NeighborSum(object):

    def __init__(self, grid):
        n = len(grid)
        self.n = n
        self.pos = [[] for _ in range(n * n)]
        self.grid = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                self.grid[i].append(grid[i][j])
                self.pos[grid[i][j]] = (i, j)
        self.adj_sum = [None] * (n * n)
        self.diag_sum = [None] * (n * n)

    def calc(self, x, y, t):
        if t == 0:
            dx = [0, 1, 0, -1]
            dy = [1, 0, -1, 0]
        else:
            dx = [-1, -1, 1, 1]
            dy = [-1, 1, -1, 1]
        
        s = 0
        for d in range(4):
            xx = x + dx[d]
            yy = y + dy[d]
            if 0 <= xx < self.n and 0 <= yy < self.n:
                s += self.grid[xx][yy]
        
        return s

    def adjacentSum(self, value):
        if self.adj_sum[value] is None:
            x, y = self.pos[value]
            self.adj_sum[value] = self.calc(x, y, 0)
        
        return self.adj_sum[value]

    def diagonalSum(self, value):
        
        if self.diag_sum[value] is None:
            x, y = self.pos[value]
            self.diag_sum[value] = self.calc(x, y, 1)
        
        return self.diag_sum[value]
''',
    call='''ns = NeighborSum([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
[ns.adjacentSum(1), ns.adjacentSum(4), ns.diagonalSum(4), ns.diagonalSum(8), ns.adjacentSum(4)]''',
    expect=[6, 16, 16, 4, 16],
    views=[
        dict(type='text', h=70, fn=lambda S: (
            f"查询 `value = {S['value']}`：位置 `pos[{S['value']}]` → 缓存 `{S.get('adj_sum') if False else ''}`" if False else
            ('`pos[v]` 记坐标，`adj_sum` / `diag_sum` 缓存结果，`None` = 还没算过'))),
        dict(type='grid', var='self.grid', cursors=[('i', 'j', 'yellow', '(i,j)'), ('x', 'y', 'orange', '(x,y)'), ('xx', 'yy', 'cyan', '')], h=260),
        dict(type='array', var='self.adj_sum', label='adj_sum（上下左右）', h=130, cell=60),
        dict(type='array', var='self.diag_sum', label='diag_sum（斜角）', h=130, cell=60),
    ],
    watch=[('value', 'value', 'green'), 'x', 'y', 't', 'd', 's'],
    captions={
        6: '`pos[v]`：元素值 `v` 在网格里的 ==坐标==，用来 O(1) 定位',
        11: '元素 `{grid[i][j]}` 在 `({i}, {j})`，记进 `pos`',
        12: '两张缓存表：`adj_sum`（上下左右）、`diag_sum`（斜角），`None` 表示没算过',
        16: lambda S, B, r: '`t = 0` → 用上下左右四个方向' if S.t == 0 else '`t = 1` → 用四个斜角方向',
        24: '枚举第 `{d}` 个方向，邻居坐标 `({x + dx[d]}, {y + dy[d]})`',
        27: lambda S, B, r: (f'邻居 `({S.xx}, {S.yy})` 在网格内 → 累加' if 0 <= S.xx < S.n and 0 <= S.yy < S.n
                                                else f'邻居 `({S.xx}, {S.yy})` 越界 → 不算'),
        28: '累加邻居 `{self.grid[xx][yy]}`，`s` = =={s}==',
        30: '这个元素的邻居和是 =={ret}==',
        33: lambda S, B, r: (f'`adj_sum[{S.value}]` 还是 `None` → ==没算过==，要现算' if S.self.adj_sum[S.value] is None
                                                          else f'`adj_sum[{S.value}]` 已有 `{S.self.adj_sum[S.value]}` → ==命中缓存==，直接返回'),
        41: lambda S, B, r: (f'`diag_sum[{S.value}]` 还是 `None` → ==没算过==，要现算' if S.self.diag_sum[S.value] is None
                                                           else f'`diag_sum[{S.value}]` 已有 `{S.self.diag_sum[S.value]}` → ==命中缓存==，直接返回'),
        34: '查 `pos` 得到 `{value}` 的坐标 `({x}, {y})`',
        42: '查 `pos` 得到 `{value}` 的坐标 `({x}, {y})`',
        35: '调用 `calc(x, y, 0)` 算出邻居和，存进 `adj_sum[{value}]`',
        43: '调用 `calc(x, y, 1)` 算出斜角和，存进 `diag_sum[{value}]`',
        37: '`adjacentSum({value})` = =={ret}==',
        45: '`diagonalSum({value})` = =={ret}==',
    },
    skip=[17, 18, 20, 21, 23, 25, 26],
    max_steps=60,
    cards=dict(
        one_liner='先用坐标表定位元素，再把算过的结果缓存起来',
        complexity='初始化 `O(n²)`，每个查询首次 `O(1)`（只看 4 个邻居），空间 `O(n²)`',
        problem=['`n × n` 网格，元素互不相同，范围 `0..n²-1`',
                 '`adjacentSum(v)`：左右上下四个邻居之和；`diagonalSum(v)`：四个斜角之和',
                 '示例：`[[0,1,2],[3,4,5],[6,7,8]]`，`adjacentSum(1)=6`'],
        quote='需要能高效定位到value，也就是说需要使用一个哈希表记录每个元素值所在的坐标。',
        quote_src='—— yiduobo 题解原文',
        idea=['查询都是按元素值 `value` 来的，所以先建 `pos`：值 → 坐标',
              '再用 `adj_sum`、`diag_sum` 两张表缓存，避免同一个 `value` 反复计算',
              '没缓存就按坐标看 4 个方向（`calc`，`t` 区分上下左右 / 斜角），缓存了直接返回'],
        summary=['初始化 `O(n²)`；每个 `value` 每种查询只算一次，之后 `O(1)`',
                 '易错点：邻居要判断 `0 <= xx < n and 0 <= yy < n`；`calc` 里 `t` 决定方向表',
                 '对比灵神：灵神在初始化时一次算完所有元素，yiduobo 是懒计算 + 缓存',
                 '原文已是 Python 3 可运行写法，代码未改动'],
    ),
)
