GR = [[0, 1, -1], [1, 0, -1], [1, 1, 1]]
PH2 = 39  # first line of the second (inverted-triangle) loop


def _fl(S, d=0):
    f, fl = S.get('f'), S.get('flag')
    if f is None or fl is None:
        return None
    return f[fl ^ d]


def _sent(S, B, r=None):
    return None


def _gc(S, r, c, v):
    if v == -1:
        return 'red'
    return None


def _cur_c(S, a, b, v):
    if 'k' in S and S.get('_line', 0) >= 14 and (a, b) == (S['j'], S['k']):
        return 'yellow'
    return None


def _pre_c(S, a, b, v):
    if 'k' in S and S.get('_line', 0) >= 14:
        j, k = S['j'], S['k']
        if (a, b) in ((j, k), (j - 1, k - 1), (j, k - 1), (j - 1, k)):
            return 'blue'
    return None


def _chk(S, B, r):
    i, j, k, g = S.i, S.j, S.k, S.grid
    a, b = g[i - j][j], g[i - k][k]
    head = f'左路径在 `({i-j},{j})` = `{a}`，右路径在 `({i-k},{k})` = `{b}`：'
    if a == -1 or b == -1:
        return head + '有荆棘 → 状态保持 `-1`（到不了），跳过'
    return head + '都能走' + ('，两条路径重合，樱桃只算一次' if j == k else '')


def _tmp(S, B, r):
    i, j, k = S.i, S.j, S.k
    base = '正三角' if S._line < PH2 else '倒三角'
    tail = f'：`tmp = {S.tmp}`' + ('，所有来源都到不了 → 这个状态保持 `-1`' if S.tmp == -1 else '')
    t = S.get('_line')
    if t == 24:
        return '`j = k = 0`：两条路径都在最左，只能从上一层最左的格子下来' + tail
    if t == 26:
        return '`j = 0`、`k = i`：左路径在最左、右路径在最右，各自只有一个来源' + tail
    if t == 28:
        return '`j = 0`、`k` 在中间：右路径有两个来源，取较大' + tail
    if t == 30:
        return '`j = i`：两条路径都在最右，只有一个来源' + tail
    if t == 32:
        return '`k = i`：右路径在最右只有一个来源，左路径有两个' + tail
    if S._line < PH2:
        return '正三角中间的格子：两条路径各 2 个来源，共 4 种，取最大' + tail
    return '倒三角里每个格子都能从上一层的两个位置下来：4 种来源取最大' + tail


CONFIG = dict(
    num=741, title='摘樱桃', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='一左一右两条路径 · 正三角 + 倒三角 DP',
    tags=['灵神题单', '网格图 DP'],
    code='''
class Solution(object):
    def cherryPickup(self, grid):

        N = len(grid)
        f = [[[-1] * N for _ in range(N)] for _ in range(2)]
        f[0][0][0] = grid[0][0]
        flag = 0

        for i in range(1, N):
            flag ^= 1
            for j in range(i + 1):
                for k in range(j, i + 1):
                    f[flag][j][k] = -1
                    if grid[i - j][j] == -1 or grid[i - k][k] == -1:
                        continue

                    if j == k:
                        add = grid[i - j][j]
                    else:
                        add = grid[i - j][j] + grid[i - k][k]

                    if j == 0:
                        if k == 0:
                            tmp = f[1 - flag][j][k]
                        elif k == i:
                            tmp = f[1 - flag][j][k - 1]
                        else:
                            tmp = max(f[1 - flag][j][k], f[1 - flag][j][k - 1])
                    elif j == i:
                        tmp = f[1 - flag][j - 1][k - 1]
                    elif k == i:
                        tmp = max(f[1 - flag][j][k - 1], f[1 - flag][j - 1][k - 1])
                    else:
                        tmp = max(f[1 - flag][j][k], f[1 - flag][j - 1][k - 1], f[1 - flag][j][k - 1], f[1 - flag][j - 1][k])
                    
                    if tmp != -1:
                        f[flag][j][k] = tmp + add
        
        for i in range(N, N + N - 1):
            flag ^= 1
            for j in range(i - N + 1, N):
                for k in range(j, N):
                    f[flag][j][k] = -1
                    if grid[i - j][j] == -1 or grid[i - k][k] == -1:
                        continue
                    
                    if j == k:
                        add = grid[i - j][j]
                    else:
                        add = grid[i - j][j] + grid[i - k][k]
                    
                    tmp = max(f[1 - flag][j][k], f[1 - flag][j - 1][k - 1], f[1 - flag][j][k - 1], f[1 - flag][j - 1][k])
                    
                    if tmp != -1:
                        f[flag][j][k] = tmp + add

        return max(f[flag][-1][-1], 0)
''',
    call=f'Solution().cherryPickup({GR})',
    expect=5,
    skip=['for j in range', 'for k in range', 'f[flag][j][k] = -1', 'continue', 'if j == k', 'add = grid', 'if j == 0', 'if k == 0',
          'elif k == i', 'elif j == i', 'else:', 'if tmp != -1'],
    views=[
        dict(type='grid', var='grid', label='grid（红 = 荆棘；蓝 = 左路径 (i-j, j)，粉 = 右路径 (i-k, k)）', cell=60, h=210,
             color=_gc, cursors=[('i - j', 'j', 'blue', ''), ('i - k', 'k', 'pink', '')]),
        dict(type='table', var=lambda S: _fl(S, 1), label='f[1-flag]：上一层（蓝 = 可能的来源）', cell=56, h=200,
             rows=['j=0', 'j=1', 'j=2'], cols=['k=0', 'k=1', 'k=2'], color=_pre_c),
        dict(type='table', var=lambda S: _fl(S, 0), label='f[flag]：这一层（黄 = 正在算，-1 = 到不了）', cell=56, h=200,
             rows=['j=0', 'j=1', 'j=2'], cols=['k=0', 'k=1', 'k=2'], color=_cur_c),
    ],
    watch=[('i', 'i'), ('flag', 'flag'), ('j', 'j', 'blue'), ('k', 'k', 'pink'), ('add', 'add'), ('tmp', 'tmp')],
    captions={
        'N = len': '`N = {N}`',
        'f = [[[-1]': '`f[flag][j][k]`：走了 `i` 步，左路径在这一层第 `j` 个、右路径在第 `k` 个位置时的最多樱桃；`-1` = 到不了；`flag` 在两层间滚动',
        'f[0][0][0] =': '第 0 步：两条路径都在 `(0,0)`，`f[0][0][0] = {f[0][0][0]}`',
        'flag = 0': '`flag = 0`：先读第 0 层',
        'for i in range(1, N)': lambda S, B, r: (f'正三角：走了 `{S.i}` 步，这一层有 `{S.i + 1}` 个位置' if S.i != B.get('i') else '正三角（前 N-1 层）完成'),
        'for i in range(N, N + N - 1)': lambda S, B, r: (f'倒三角：走了 `{S.i}` 步，位置越来越少' if S.i != B.get('i') else '倒三角完成'),
        'flag ^= 1': '`flag` 翻转：这层写 `f[{flag}]`，上一层读 `f[{1 - flag}]`',
        'if grid[i - j][j] == -1': _chk,
        'tmp = ': _tmp,
        'f[flag][j][k] = tmp + add': '`f[{flag}][{j}][{k}] = {tmp} + {add}` = =={f[flag][j][k]}==',
        'return max': '最后一层最后一个状态就是终点 → 和 `0` 取大：=={ret}==',
    },
    cards=dict(
        one_liner='回来的路径等价于再出发一次：一左一右两条路径同步下行',
        complexity='时间 `O(N^3)`，空间 `O(N^2)`',
        problem=['`N × N` 网格：`1` 樱桃，`0` 空，`-1` 荆棘',
                 '从 `(0,0)` 到 `(N-1,N-1)` 再返回，摘过的樱桃变 `0`',
                 '示例：`[[0,1,-1],[1,0,-1],[1,1,1]]` → `5`'],
        quote='换言之，最终的答案必然可以写成一左一右两条路径的形式。又注意到向上的路径虽然描述是要求从终点往上返回起点，但是实际上从起点出发往下走到终点是完全等价的。',
        quote_src='—— yiduobo 题解原文',
        idea=['来回两条路径可能重合、但不会交叉（交叉总能换成不交叉）',
              '把地图转 45 度：一个正三角加一个倒三角，两条路径每步在同一层',
              '`f[i][j][k]`：走 `i` 步，左在第 `j` 个、右在第 `k` 个；`j == k` 时樱桃只算一次'],
        summary=['时间 `O(N^3)`，空间 `O(N^2)`（`flag` 做 01 滚动）',
                 '易错：正三角边界要分 `j = 0`、`k = i` 等情况；倒三角每格都有两个来源',
                 '`-1` 表示不可达，最后要和 `0` 取最大',
                 '原文本身可直接在 Python 3 运行，代码未改',
                 '对比灵神：灵神按 `t = i + j` 统一成一个三重循环 + `-inf`；yiduobo 把正三角和倒三角分开写'],
    ),
)
