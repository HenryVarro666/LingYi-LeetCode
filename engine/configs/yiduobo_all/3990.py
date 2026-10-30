R0, C0 = 17, 17


def _crop(S):
    f = S['f']
    return [row[C0:] for row in f[R0:]]


def _top(S):
    if 'k' not in S:
        return ''
    if 'x' not in S:
        return f"目标 `k = {S['k']}`：从终点 `(24,24)` 倒推，先放 `f[24][24] = k`"
    return f"当前 `k = {S['k']}`，正在构造的位置 `(x, y) = ({S['x']}, {S['y']})`（下图只截取右下角 8×8，行列从 {R0} 起）"


CONFIG = dict(
    num=3990, title='创建一个恰好有 K 条路径的网格图 II', difficulty='Hard', category='贪心算法',
    author='yiduobo', technique='倒推 · 乘 2 与加 1',
    tags=['贪心与思维', '构造题'],
    code='''
class Solution(object):
    def createGrid(self, k):
        
        f = [[0] * 25 for _ in range(25)]
        f[-1][-1] = k

        x, y = 24, 24
        flag = True
        while k > 1:
            if k % 2 == 0:
                k //= 2
                f[x - 1][y] = k
                f[x][y - 1] = k
                f[x - 1][y - 1] = k
                x -= 1
                y -= 1
            elif flag:
                for r in range(x):
                    f[r][y] = 1
                k -= 1
                f[x][y - 1] = k
                f[x][y - 2] = k
                y -= 2
                flag = not flag
            else:
                for c in range(y):
                    f[x][c] = 1
                k -= 1
                f[x - 1][y] = k
                f[x - 2][y] = k
                x -= 2
                flag = not flag

        f[x - 1][y] = 1
        x -= 2
        y -= 2
        for r in range(x, 25):
            f[r][y] = 1
        for c in range(y, 25):
            f[x][c] = 1

        res = []
        for line in f[x:]:
            t = []
            for index in range(y, 25):
                if line[index] > 0:
                    t.append('.')
                else:
                    t.append('#')

            res.append(''.join(t))
            
        return res
''',
    call='Solution().createGrid(7)',
    expect=['.......', '.#.###.', '.#..##.', '.#..##.', '.##.##.', '.....#.', '.##....'],
    skip=['f = [[0]', 'for r in range(x)', 'f[r][y] = 1', 'for c in range(y)', 'f[x][c] = 1', 'x -= 1', 'y -= 1',
          'f[x][y - 2] = k', 'f[x - 2][y] = k', 'f[x - 1][y - 1] = k', 'f[x][y - 1] = k', 'f[x - 1][y] = k',
          't = []', 'for index in range', 't.append', 'if line[index]', 'for r in range(x, 25)', 'for c in range(y, 25)',
          'x -= 2', 'y -= 2'],
    views=[
        dict(type='text', fn=_top),
        dict(type='grid', var=_crop, h=420, cell=52, label='f（f[i][j] = 走到该格的路径数，0 = 墙）',
             rows=list(range(R0, 25)), cols=list(range(C0, 25)),
             color=lambda S, i, j, v: 'green' if v and v > 0 else None,
             cursors=[(lambda S: S['x'] - R0 if 'x' in S else None, lambda S: S['y'] - C0 if 'y' in S else None, 'yellow', '(x,y)')]),
        dict(type='grid', var='res', h=240, cell=44, label='res（. 可走，# 墙）',
             color=lambda S, i, j, v: 'green' if v == '.' else None),
    ],
    watch=[('k', 'k', 'yellow'), ('x', 'x', 'blue'), ('y', 'y', 'pink'), ('flag', 'flag', 'cyan')],
    captions={
        'f[-1][-1] = k': '终点 `f[24][24] = k = {k}`：`f` 记录“走到这一格的路径数”，从终点往回倒推',
        'x, y = 24, 24': '`(x, y)` 是当前要产生 `k` 条路径的格子，从右下角开始',
        'flag = True': '`flag` 轮流决定“加 1”这条贴边路径从上方还是从左方分出，让网格保持圆润',
        'while k > 1': lambda S, B, r: (f'`k = {S.k} > 1`：还没倒推到 1，继续' if S.k > 1 else '`k = 1`：倒推到头了，只剩一条路'),
        'if k % 2 == 0': lambda S, B, r: (f'`k = {S.k}` 是偶数 → 乘法器：放一个 2×2 空地，路径数 ×2' if S.k % 2 == 0 else f'`k = {S.k}` 是奇数 → 不能整除 2，要先 `-1`（加法器）'),
        'k //= 2': '偶数：`k` 减半为 `{k}`，左上方三格（`f[x-1][y]`、`f[x][y-1]`、`f[x-1][y-1]`）都是 `{k}`：2×2 空地使路径数 ==翻倍==，倒回去就是 `{k} × 2`',
                'elif flag': lambda S, B, r: ('`flag = True`：这次“加 1”从==上方==分出（整列贴边的 1）' if S.flag else '`flag = False`：这次“加 1”从==左方==分出（整行贴边的 1）'),
        'k -= 1': lambda S, B, r: (f'先把这一列 `f[0..{S.x-1}][{S.y}]` 全设为 1：贴边一路走下来的那条路，提供“加 1”；`k` 减 1，剩下 `k = {S.k}` 交给前面构造' if S.flag else f'先把这一行 `f[{S.x}][0..{S.y-1}]` 全设为 1：贴边走过来的那条路，提供“加 1”；`k` 减 1，剩下 `k = {S.k}` 交给前面构造'),
                'flag = not flag': '`flag` 取反：下一次“加 1”换另一个方向 → `{flag}`',
        'f[x - 1][y] = 1': 'k 倒推到 1：起点处放 `1`，接上贴边的路',
        'res = []': '`f` 里非 0 的格子 → `.`，0 → `#`；只截取用到的右下角区域 `f[x:]`、`y` 列起',
        'for line in f[x:]': '取 `f` 的下一行（只截取用到的区域），转成 `.` / `#`',
        'res.append': '这一行转成字符串 `{"".join(t)}`，加入 `res`',
        'return res': '拼好返回：左上到右下恰好 `7` 条路径',
    },
    cards=dict(
        one_liner='倒推：偶数用 2×2 乘 2，奇数先减 1，用贴边的路补 1',
        complexity='时间 `O(log k)`（常数个 25×25 的操作），空间 `O(1)`',
        problem=['构造由 `.`/`#` 组成、长宽 ≤ 25 的网格，只能向右或向下走',
                 '从左上到右下恰好有 `k` 条路径（`1 ≤ k ≤ 1000`）',
                 '本视频：`k = 7`，得到 7×7 的网格'],
        quote='乘法器是天然就有的……加法器可以认为是路径一分为二，分别计算后汇总。……一个最直观的想法就是乘以2与加1的组合。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k` 偶：`k = (k/2) × 2`，一个 2×2 的点矩阵就是“×2”的乘法器',
              '`k` 奇：`k = (k-1) + 1`，贴边画一条全 1 的路，用 `#` 限行，提供“+1”',
              '只加在一个方向会让网格扁平、超过 25 列：用 `flag` 轮流从上方、左方提供 +1',
              '从 `k` 倒推到 1，从右下往左上放，非 0 的格子是 `.`，0 是 `#`'],
        summary=['时间 `O(log k)`，空间 `O(1)`（固定 25×25 的 `f`）',
                 '易错：`flag` 要在每次“加 1”后取反，否则网格会扁平超宽',
                 '易错：奇数先 `k -= 1`，再放 `f[..] = k`，最后才补上那条 1',
                 '原文已是 Python 3 可运行的写法（`//` 与 `range`），未作修改',
                 '对比灵神：灵神按二进制位一次性铺好；yiduobo 用倒推与乘 2 加 1'],
    ),
)
