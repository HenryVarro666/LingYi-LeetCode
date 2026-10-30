GRID = [[1, 3, 3], [2, 5, 4], [4, 3, 5]]


def _layer(t_off):
    def fn(S):
        if 'f' not in S or 't' not in S or S['t'] + t_off < 0:
            return [[None] * 3 for _ in range(3)]
        t = S['t'] + t_off
        return [[S['f'][x][y][t] for y in range(3)] for x in range(3)]
    return fn


def _cur(S):
    return S.get('_line') in range(24, 40) and 'x' in S and 'y' in S


def _gcolor(S, i, j, v):
    if _cur(S) and (i, j) == (S['x'], S['y']):
        return 'yellow'
    return None


def _text(S):
    if 't' not in S:
        return '`f[x][y][t]`：恰好传送 `t` 次走到 `(x,y)` 的最小成本（None = 到不了）；先按值从大到小处理传送，再处理普通走'
    ln = S.get('_line', 0)
    if ln in (23, 24, 25, 26, 27, 28, 29, 30, 31):
        return f"第 ==t {S['t']}== 层：从上一层传送过来。`best` 是值 >= 当前值的格子里，上一层的最小成本" + (f"，现在 `best = {S['best']}`" if 'best' in S else '')
    return f"第 ==t {S['t']}== 层：本层内普通走：`min(上, 左) + grid[x][y]`；传送来的结果已经写进本层"


CONFIG = dict(
    num=3651, title='带传送的最小路径成本', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[x][y][t] 三维 DP + 按值排序的前缀最优',
    tags=['灵神题单', '动态规划', '难度分 2411'],
    code='''
class Solution(object):
    def minCost(self, grid, k):
        
        m = len(grid)
        n = len(grid[0])

        f = [[[None] * (k + 1) for _ in range(n)] for _ in range(m)]
        f[0][0][0] = 0
        position = []
        for i in range(m):
            for j in range(n):
                position.append((grid[i][j], i, j))
        position.sort(key=lambda d:-d[0])

        res = None
        for t in range(k + 1):
            if t != 0:
                p = 0
                best = None
                for v, x, y in position:
                    while p < len(position) and position[p][0] == v:
                        _, pre_x, pre_y = position[p]
                        if best is None or best > f[pre_x][pre_y][t - 1]:
                            best = f[pre_x][pre_y][t - 1]
                        p += 1
                    f[x][y][t] = best
            
            for x in range(m):
                for y in range(n):
                    best = None
                    if x > 0 and f[x - 1][y][t] is not None:
                        best = f[x - 1][y][t] + grid[x][y]
                    if y > 0 and f[x][y - 1][t] is not None:
                        if best is None or best > f[x][y - 1][t] + grid[x][y]:
                            best = f[x][y - 1][t] + grid[x][y]
                    
                    if best is not None and (f[x][y][t] is None or f[x][y][t] > best):
                        f[x][y][t] = best
            
            if f[-1][-1][t] is not None:
                if res is None or res > f[-1][-1][t]:
                    res = f[-1][-1][t]
        
        return res
''',
    call=f'Solution().minCost({GRID}, 1)',
    expect=7,
    skip=['m = len', 'n = len', 'f = [[[None]', 'position = []', 'for i in range(m)', 'for j in range(n)',
          'position.append', 'position.sort', 'res = None', 'for v, x, y in position', 'while p < len',
          'p = 0', 'p += 1', '_, pre_x', 'for x in range(m)', 'for y in range(n)', 'best = None',
          'if x > 0 and f', 'if y > 0 and f', 'if best is None or best > f[x][y - 1]', 'if best is None or best > f[pre_x]', 'if best is not None and'],
    max_steps=90,
    views=[
        dict(type='text', fn=_text, h=70),
        dict(type='grid', var='grid', color=_gcolor, h=180, cell=70, cursors=[]),
        dict(type='table', var=_layer(-1), label='上一层 f[·][·][t-1]（传送来源）', h=180, cell=60),
        dict(type='table', var=_layer(0), label='本层 f[·][·][t]', cursors=[('x', 'y', 'yellow', '')], h=180, cell=60),
    ],
    watch=[('t', 't', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'pink'), ('best', 'best', 'yellow'), ('res', 'res', 'green')],
    captions={
        'f[0][0][0] = 0': '起点：传送 0 次、成本 0',
        'for t in range': lambda S, B, r: (f"处理第 `t = {S['t']}` 层：恰好传送 `{S['t']}` 次" if B.get('t') != S.get('t') or 't' not in B else '所有层处理完'),
        'if t != 0': lambda S, B, r: ('`t = 0` 没有传送来源，跳过传送这一步' if S.t == 0 else '`t > 0`：先处理==传送==，再处理普通走（顺序不能反）'),
        24: '值 `{v}` 这一档的格子 `({pre_x},{pre_y})` 上一层成本更小 → `best` 更新为 =={best}==',
        26: '格子 `({x},{y})`：所有值 >= `{grid[x][y]}` 的格子都已并入 `best` → 传送到这里成本 `{best}`',
        32: '从上面来：`{f[x-1][y][t]} + {grid[x][y]}` = =={best}==',
        35: '从左边来 `{f[x][y-1][t]} + {grid[x][y]}` 更小 → `best` = =={best}==',
        38: '格子 `({x},{y})`：普通走 `best = {best}`，和传送来的比，取更小 → `f[{x}][{y}][{t}]` = =={f[x][y][t]}==',
        'if f[-1][-1][t] is not None': lambda S, B, r: (f"第 `{S.t}` 层终点成本 `{S.f[-1][-1][S.t]}`，用它更新答案" if S.f[-1][-1][S.t] is not None else '本层终点不可达'),
        'res = f[-1][-1][t]': '`res` 更新为 =={res}==',
        'return res': '最小成本 `{res}`',
    },
    cards=dict(
        one_liner='把传送次数 t 编进状态，传送用「值从大到小的前缀最优」',
        complexity='时间 `O(mn log(mn) + k·mn)`，空间 `O(k·mn)`',
        problem=['网格从左上走到右下，只能右/下，成本是目标格的值',
                 '可传送到值不大于当前格的任意格，成本 0，最多 `k` 次',
                 '本视频：`[[1,3,3],[2,5,4],[4,3,5]], k=1` → `7`'],
        quote='如果能按照grid从大到小的顺序来进行状态转移，那么问题就变成了前缀最大值，只需一趟遍历就可以解决了。',
        quote_src='—— yiduobo 题解原文',
        idea=['没有传送：`f[i][j] = min(f[i-1][j], f[i][j-1]) + grid[i][j]`；再加一维 `t`',
              '传送：`f[x][y][t]` 可由所有 `grid >= grid[x][y]` 的 `f[·][·][t-1]` 转来',
              '把格子按值从大到小排，边扫边维护 `best`，同值一档先并入再赋值'],
        summary=['时间 `O(mn log(mn) + k·mn)`，空间 `O(k·mn)`',
                 '易错：同一层要先传送、后普通走；反过来会出现一次传送却多算一次',
                 '`None` 表示到不了，比较前必须判空',
                 '对比灵神：灵神用 `suf_min_f[x]` 数组按值域做后缀最小；yiduobo 排序后扫一遍 `best`'],
    ),
)
