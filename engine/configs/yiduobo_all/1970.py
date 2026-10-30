ROW, COL = 3, 2
CELLS = [[1, 1], [2, 1], [3, 2], [2, 2], [1, 2], [3, 1]]
DAY = [[0] * COL for _ in range(ROW)]
for _d, (_r, _c) in enumerate(CELLS):
    DAY[_r - 1][_c - 1] = _d + 1          # 第 d+1 天变成水（图上显示的数字）
TOP, BOT = 0, ROW * COL + 1               # 超级节点 s = 0，t = row*col+1；格子编号 (x-1)*col+y（从 1 开始）


def _root(fa, x):
    while fa[x] != x:
        x = fa[x]
    return x


def _fa(S):
    fa = S.get('self.fa')
    return list(fa) if fa is not None else None


def _island(S, i, j):
    used = S.get('used')
    if used is None:
        return False
    v = i * COL + j + 1
    if v in used:
        return True
    return 'nowx' in S and 'nowy' in S and S['nowx'] == i + 1 and S['nowy'] == j + 1


def _gcolor(S, i, j, v):
    if not _island(S, i, j):
        return None
    fa = S['self.fa']
    rt = _root(fa, i * COL + j + 1)
    if rt == _root(fa, TOP) and rt == _root(fa, BOT):
        return 'yellow'
    if rt == _root(fa, TOP):
        return 'cyan'
    if rt == _root(fa, BOT):
        return 'orange'
    return 'green'


def _gdim(S, i, j, v):
    return 'used' in S and not _island(S, i, j)


def _atcolor(S, i, v):
    if i == TOP:
        return 'cyan'
    if i == BOT:
        return 'orange'
    return None


def _cur(S):
    if 'nowx' not in S:
        return None
    return (S['nowx'] - 1, S['nowy'] - 1)


def _conn(S):
    fa = S.get('self.fa')
    if fa is None or 'used' not in S:
        return ''
    same = _root(fa, TOP) == _root(fa, BOT)
    st = '==已连通==' if same else '还没连通'
    return f"超级节点 `0`（最上层）与 `{BOT}`（最下层）：{st}"


CONFIG = dict(
    num=1970, title='你能穿过矩阵的最后一天', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='倒推加陆地 · 并查集 + 超级节点',
    tags=['灵神题单·网格图', '灵神题单·常用数据结构', '难度分 2124'],
    code='''
class Solution(object):
    def latestDayToCross(self, row, col, cells):

        self.fa = list(range(row * col + 2))
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        cells.reverse()
        used = set()
        res = row * col
        for nowx, nowy in cells:
            for index in range(4):
                x = nowx + dx[index]
                y = nowy + dy[index]
                if x > 0 and x <= row and y > 0 and y <= col and (x - 1) * col + y in used:
                    self.union((x - 1) * col + y, (nowx - 1) * col + nowy)
            
            if nowx == 1:
                self.union(0, (nowx - 1) * col + nowy)
            
            if nowx == row:
                self.union((nowx - 1) * col + nowy, row * col + 1)
            
            res -= 1
            if self.find(0) == row * col + 1:
                return res
    
            used.add((nowx - 1) * col + nowy)

    def find(self, x):
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        
        return self.fa[x]
    
    def union(self, x, y):
        fa_x = self.find(x)
        fa_y = self.find(y)
        if fa_x < fa_y:
            self.fa[fa_x] = fa_y
        else:
            self.fa[fa_y] = fa_x
''',
    call=f'Solution().latestDayToCross({ROW}, {COL}, {CELLS})',
    expect=2,
    skip=['dx = [', 'dy = [', 'for index in range(4)', 'x = nowx', 'y = nowy', 'if self.fa[x] != x',
          'return self.fa[x]', 'fa_x = self.find', 'fa_y = self.find', 'self.fa = list'],
    max_steps=85,
    views=[
        dict(type='grid', var=lambda S: DAY, cell=96, h=330, color=_gcolor, dim=_gdim,
             label='数字=第几天被淹；暗=仍是水；绿=陆地；青=连上边；橙=连下边；黄=上下已通',
             cursors=[('(nowx - 1) if "nowx" in dir() else None', '(nowy - 1) if "nowy" in dir() else None', 'pink')]),
        dict(type='array', var=_fa, cell=64, h=170, color=_atcolor,
             label='self.fa（下标 = (x-1)*col+y；0 = 最上层 s 青，7 = 最下层 t 橙）'),
        dict(type='text', fn=_conn, h=60, size=28),
    ],
    watch=[('res', 'res', 'green'), ('(nowx, nowy)', '(nowx, nowy) if "nowx" in dir() else None', 'pink')],
    captions={
        'self.fa = list(range': '`fa[i] = i`：每个格子自成一个集合。多出的 `0` 和 `row*col+1` 是==超级节点== s、t',
        'cells.reverse()': '==把 cells 倒过来==：原来是“一块陆地变水”，倒着就是“一块水变陆地”',
        'used = set()': '`used` 记录已经变回陆地的格子编号',
        'res = row * col': '`res` 从 `row*col` 开始，每处理一块就减 1，表示“对应的是第几天”',
        'for nowx, nowy in cells': lambda S, B, r_: (1 / 0 if 'nowx' in B and 'nowx' in S and (B.nowx, B.nowy) == (S.nowx, S.nowy)
                                                       else f'一开始全是水，现在把 `({S.nowx},{S.nowy})` 变成陆地（行列从 1 开始）'),
        'if x > 0 and x <= row': lambda S, B, r_: (f'邻居 `({B.x},{B.y})` 越界' if not (0 < B.x <= B.row and 0 < B.y <= B.col)
                                                   else (f'邻居 `({B.x},{B.y})` 已经是陆地 → ==合并=='
                                                         if (B.x - 1) * B.col + B.y in B.used else
                                                         f'邻居 `({B.x},{B.y})` 还是水 → ==不能连==')),
        'self.union((x - 1) * col + y': '把 `({B.nowx},{B.nowy})` 与相邻的陆地 `({B.x},{B.y})` 合并到一个集合',
        'if nowx == 1': lambda S, B, r_: ('`nowx = 1`：在最上层 → 与超级节点 s（`0`）相连' if B.nowx == 1
                                           else f'`nowx = {B.nowx}`：不在最上层'),
        'self.union(0,': '最上层的陆地和 s 合并：之后只要看 s 能不能连到 t',
        'if nowx == row': lambda S, B, r_: (f'`nowx = {B.nowx} = row`：在最下层 → 与超级节点 t 相连' if B.nowx == B.row
                                             else f'`nowx = {B.nowx}`：不在最下层'),
        'self.union((nowx - 1) * col + nowy, row * col + 1)': '最下层的陆地和 t 合并',
        'res -= 1': '`res = {res}`：倒着往回走了一天',
        'if self.find(0)': lambda S, B, r_: (f's 的代表元 `{_root(S.self.fa, 0)}` == t 的代表元 → ==s、t 连通=='
                                             f'：这一天还走得通 → 返回 `res`'
                                             if _root(S.self.fa, 0) == _root(S.self.fa, S.row * S.col + 1)
                                             else 's 和 t 还没连通，继续把下一块水变回陆地'),
        'return res': '倒推第一次走通：答案 `res = {res}`（这块陆地再变成水之前，是最后一次走通）',
        'used.add': '`({nowx},{nowy})` 加入 `used`，以后它是别人的陆地邻居',
        'self.fa[x] = self.find(self.fa[x])': '`fa[{B.x}] = {B.self.fa[B.x]}` 不是自己 → 先递归找到代表元，再==路径压缩==',
        'if fa_x < fa_y': lambda S, B, r_: (f'`{S.x}` 和 `{S.y}` 的代表元都是 `{S.fa_x}`，已在同一集合'
                                            if S.fa_x == S.fa_y else
                                            f'两个集合的代表元：`{S.fa_x}` 和 `{S.fa_y}`，==小的挂到大的下面=='),
        'self.fa[fa_x] = fa_y': '`fa[{fa_x}] = {fa_y}`：合并完成',
        'self.fa[fa_y] = fa_x': lambda S, B, r_: ('代表元相同，自己指自己，什么也没变' if S.fa_x == S.fa_y
                                                  else '`fa[{0}] = {1}`：合并完成'.format(S.fa_y, S.fa_x)),
    },
    cards=dict(
        one_liner='倒着把水变回陆地，用并查集 + 两个超级节点判通',
        complexity='时间 `O(mn · α)` ≈ `O(mn)`，空间 `O(mn)`',
        problem=['`row × col` 的矩阵，第 `i` 天 `cells[i]` 这格陆地变成水（行列从 1 开始）',
                 '求==最后一天==仍能只走陆地、从最上一行走到最下一行',
                 '本视频：`3×2`，`cells = [[1,1],[2,1],[3,2],[2,2],[1,2],[3,1]]` → `2`'],
        quote='一开始认为地图上全是水域，然后按照输入相反的顺序，将某些水域变成陆地。若某一块水域变成陆地之后可以走通了，那么反过来说明在这块陆地变成水域之前，这是最后一次走通的机会。',
        quote_src='—— yiduobo 题解原文',
        idea=['先想到二分答案 + BFS，`O(mn log(mn))`；再想到==倒推==更好',
              '变陆地时，用并查集把它和四周已有的陆地合并',
              '怕每次枚举首行、末行太慢：设两个==超级节点== s、t',
              '首行陆地连 s，末行陆地连 t，只需判断 `find(0) == find(row*col+1)`'],
        summary=['时间约 `O(mn)`，空间 `O(mn)`',
                 '`res` 从 `row*col` 开始，处理一块减 1，倒着返回的就是天数',
                 '易错：格子编号 `(x-1)*col+y` 从 1 开始，0 留给 s，`row*col+1` 是 t',
                 '原文为 Python 2 写法：`self.fa = range(...)` 在 Python 3 里不是列表，已改为 `list(range(...))`',
                 '`cells.reverse()` 会改动输入列表'],
    ),
)
