G0 = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]


def _row(S):
    g, row = S.get('grid'), S.get('row')
    if g is None or row is None:
        return None
    for r, rw in enumerate(g):
        if rw is row:
            return r
    return None


def _gcol(S, i, j, v):
    if v == 1:
        return 'purple'
    return None


def _ac(S, i, v):
    j = S.get('j')
    if j is None or S.get('_line', 0) < 11:
        return None
    if i == j + 1:
        return 'yellow'
    if i == j:
        return 'green'
    return None


def _text(S):
    j, x = S.get('j'), S.get('x')
    if j is None or x is None or S.get('_line', 0) < 11:
        return '`f0[j+1]`：从右边来到格子；`f1[j+1]`：从下边来到；紫色格 = 镜子'
    r = _row(S)
    if x == 0:
        return f'格子 `({r},{j})` 空：`f0 = f1 = f0[j] + f1[j+1]`（左 + 上），无论从哪来都能继续'
    return f'格子 `({r},{j})` 是镜子：右边来 → 反射到上边 `f1[j+1]`；下边来 → 反射到左边 `f0[j]`'


CONFIG = dict(
    num=3665, title='统计镜子反射路径数目', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='网格 DP + 方向状态（滚动数组）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1883'],
    code='''
class Solution:
    def uniquePaths(self, grid: List[List[int]]) -> int:
        MOD = 1_000_000_007
        n = len(grid[0])
        # 2*(n+1) 比 (n+1)*2 快（可以对比 Python3 写法二）
        f0 = [0] * (n + 1)
        f1 = [0] * (n + 1)
        f0[1] = f1[1] = 1
        for row in grid:
            for j, x in enumerate(row):
                if x == 0:
                    f0[j + 1] = (f0[j] + f1[j + 1]) % MOD
                    f1[j + 1] = f0[j + 1]
                else:
                    f0[j + 1] = f1[j + 1]
                    f1[j + 1] = f0[j]
        return f0[n]
''',
    call=f'Solution().uniquePaths({G0})',
    expect=5,
    max_steps=60,
    skip=['MOD =', 'n = len', '# 2*', 'for row in grid', 'for j, x in', 'f1 = [0]'],
    views=[
        dict(type='grid', var='grid', label='grid（紫 = 镜子，黄框 = 当前格子）', h=210, cell=64,
             color=_gcol, cursors=[(lambda S: _row(S), 'j', 'yellow', '')]),
        dict(type='text', fn=_text, size=21, h=55),
        dict(type='array', var='f0', label='f0[j+1]：从右边来到当前格的方案数（黄 = 正在算，绿 = 左边 f0[j]）', h=130, cell=80, color=_ac),
        dict(type='array', var='f1', label='f1[j+1]：从下边来到当前格的方案数', h=130, cell=80, color=_ac),
    ],
    watch=[('j', 'j', 'blue'), ('x', 'x', 'purple'), ('f0', 'f0', 'green'), ('f1', 'f1', 'pink')],
    captions={
        'f0 = [0]': '`f0[j+1]`：==从右边==来到这格、倒着走回起点的方案数',
        'f1 = [0]': '`f1[j+1]`：==从下边==来到这格的方案数',
        'f0[1] = f1[1] = 1': '起点只有 1 种（原地不动），方向无所谓，所以 `f0[1] = f1[1] = 1`；其余 0 = 出界',
        'if x == 0': lambda S, B, r: ('没有镜子，随便走' if S.x == 0 else '有镜子（`\\` 摆放），方向会被改变'),
        'f0[j + 1] = (f0[j] + f1[j + 1])': '没镜子：往左 `f0[{j}] = {B.f0[j]}`，往上 `f1[{j+1}] = {B.f1[j+1]}`，加法原理 → `f0[{j+1}]` = =={f0[j+1]}==',
        'f1[j + 1] = f0[j + 1]': '没镜子时从哪来都一样，`f1[{j+1}] = f0[{j+1}] = {f1[j+1]}`',
        'f0[j + 1] = f1[j + 1]': '有镜子，==从右边来 → 反射到上边==：`f0[{j+1}] = f1[{j+1}] = {f0[j+1]}`',
        'f1[j + 1] = f0[j]': '有镜子，==从下边来 → 反射到左边==：`f1[{j+1}] = f0[{j}] = {f1[j+1]}`（左边格子 `f0[j]` 已算完）',
        'return f0[n]': '终点没有镜子，`f0[n]` = `f1[n]`，答案 `{ret}`',
    },
    cards=dict(
        one_liner='倒着走，记下「从哪边来」，镜子决定下一步去哪',
        complexity='时间 `O(mn)`，空间 `O(n)`',
        problem=['机器人从左上走到右下，只能右/下；格子 1 是镜子',
                 '向右进镜子会被转向下、向下进镜子会被转向右，出界则路径无效',
                 '示例：`[[0,1,0],[0,0,1],[1,0,0]]` → `5`，对 `10^9+7` 取模'],
        quote='所以当我们到达格子 (i,j) 时，还需要知道是从哪边来的，从而决定下一步去哪。因此，在 62 题的基础上，增加一个参数 k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['和 62 题一样从终点倒着回起点；`k = 0` 表示从右边来，`k = 1` 从下边来',
              '没镜子：往左、往上两种互斥，相加；有镜子：右边来 → 去上边，下边来 → 去左边',
              '递推加一圈虚拟行列表示出界；再去掉行维度变成两个一维数组'],
        summary=['时间 `O(mn)`，空间优化后 `O(n)`',
                 '易错：镜子格要==先改 `f0[j+1]`、再改 `f1[j+1]`==，前者要用 `f1[j+1]` 的旧值',
                 '没镜子时才取模；`f0[1] = f1[1] = 1` 初始化省去起点特判',
                 '原文还有记忆化搜索和三维递推写法，这里演示空间优化版'],
    ),
)
