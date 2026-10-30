G0 = [[5, 2, 4], [3, 0, 5]]
K0 = 3


def _row(S):
    g, row = S.get('grid'), S.get('row')
    if g is None or row is None:
        return None
    for r, rw in enumerate(g):
        if rw is row:
            return r
    return None


def _fc(S, r, c, v):
    j, s, ns = S.get('j'), S.get('s'), S.get('new_s')
    if j is None or S.get('_line', 0) < 10:
        return None
    if S.get('_line') == 13:
        return 'yellow' if r == j + 1 else None
    if s is not None and (r, c) == (j + 1, s) and S.get('_line', 0) >= 12:
        return 'yellow'
    if ns is not None:
        if (r, c) == (j + 1, ns):
            return 'blue'
        if (r, c) == (j, ns):
            return 'green'
    return None


def _text(S):
    j, s, x = S.get('j'), S.get('s'), S.get('x')
    if j is None or x is None or s is None:
        return '`f[j+1][s]`：倒着走，已走路径和（不含当前格）模 `k` 为 `s` 时，走回起点的方案数；初始 `f[1][0] = 1`'
    ns = S.get('new_s', (s + x) % K0)
    return f'格子值 `x = {x}`：已走和模 `k` 为 `s = {s}`，加上本格后，上/左邻要查 `({s} + {x}) % {K0} = {ns}` 这一列'


CONFIG = dict(
    num=2435, title='矩阵中和能被 K 整除的路径', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='网格 DP + 路径和模 k（滚动数组）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1952'],
    code='''
class Solution:
    def numberOfPaths(self, grid: List[List[int]], k: int) -> int:
        MOD = 1_000_000_007
        m, n = len(grid), len(grid[0])
        f = [[0] * k for _ in range(n + 1)]
        f[1][0] = 1
        new_f = [0] * k  # 避免在循环内反复创建 list
        for row in grid:
            for j, x in enumerate(row):
                for s in range(k):
                    new_s = (s + x) % k
                    new_f[s] = (f[j + 1][new_s] + f[j][new_s]) % MOD
                f[j + 1][:] = new_f  # 把 new_f 复制到 f[j+1] 中
        return f[n][0]
''',
    call=f'Solution().numberOfPaths({G0}, {K0})',
    expect=1,
    max_steps=80,
    skip=['MOD = ', 'm, n = ', 'for row in grid', 'for j, x in', 'for s in range', 'new_s = '],
    views=[
        dict(type='grid', var='grid', label='grid（黄框 = 当前格子）', h=150, cell=60,
             cursors=[(lambda S: _row(S), 'j', 'yellow', '')]),
        dict(type='text', fn=_text, size=21, h=55),
        dict(type='table', var='f', label='f[j+1][s]（行 = 列号 j，列 = s）：黄 = 正在算，蓝 = 上方，绿 = 左边', h=290, cell=70,
             rows=lambda S: [f'j={r - 1}' for r in range(len(S['f']))] if 'f' in S else [],
             cols=lambda S: [f's={c}' for c in range(K0)], color=_fc),
        dict(type='array', var='new_f', label='new_f（本格结果的暂存区，算完整体拷贝回 f[j+1]）', h=130, cell=70,
             color=lambda S, i, v: 'yellow' if S.get('s') == i and S.get('_line') == 12 else None),
    ],
    watch=[('j', 'j', 'blue'), ('x', 'x', 'yellow'), ('s', 's', 'pink'), ('new_s', 'new_s', 'purple')],
    captions={
        'f = [[0]': '`f[j+1][s]`：==倒着走==，已走过的路径和（不含当前格）模 `k` 为 `s` 时，从当前格走回起点的方案数',
        'f[1][0] = 1': '虚拟起点 `(-1, 0)`：倒着走到这里时，路径和模 `k` 为 `0` 才算一条合法路径 → 只有 `f[1][0] = 1`',
        'new_f = [0]': '`new_f` 先暂存本格的结果，避免提前覆盖 `f[j+1][·]`',
        'new_f[s] = ': '`s = {s}`：加上本格 `x = {x}` → 传给上/左邻的余数 `new_s = ({s}+{x})%{k} = {new_s}`；`new_f[{s}] = 上 f[{j+1}][{new_s}] ({B.f[j+1][new_s]}) + 左 f[{j}][{new_s}] ({f[j][new_s]})` = =={new_f[s]}==',
        'f[j + 1][:] = new_f': '这格的 `k` 个状态都算完，整体拷贝回 `f[{j+1}]` = {f[j+1]}',
        'return f[n][0]': '终点 `s = 0`：倒着走时路径和从 0 开始，答案 `f[n][0]` = =={ret}==',
    },
    cards=dict(
        one_liner='在 62 题的基础上，多记一个「路径和模 k」',
        complexity='时间 `O(mnk)`，空间 `O(nk)`',
        problem=['`m×n` 网格，从左上走到右下，每步向下或向右',
                 '统计路径上元素和能被 `k` 整除的路径数，对 `10^9+7` 取余',
                 '示例：`[[5,2,4],[3,0,5],[0,7,2]], k=3` → `2`'],
        quote='把 s 定义成从终点 (m-1,n-1) 走到 (i,j) 的前一个位置的路径和模 k（意思是路径和不包括 grid[i][j]）。设 newS=(s+grid[i][j]) mod k，继续移动，计算方案数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['62 题再加一维 `s`：路径和模 `k`（中途取模不影响最终余数）',
              '原文写法二从终点倒着走：`s` 是已走路径和，走到本格后变成 `(s + x) % k` 传给上/左邻',
              '去掉行维度，用 `new_f` 暂存，避免没算完就覆盖'],
        summary=['时间 `O(mnk)` = 状态数 × `O(1)` 转移，空间 `O(nk)`',
                 '易错：倒着走时 `new_s = (s + x) % k`，别写成减；每个格子先算完全部 `s` 再覆盖',
                 '用 `f[1][0] = 1` 的虚拟起点省去边界特判',
                 '原文另有记忆化搜索（两种写法）、三维递推和 `new_f` 新建列表的空间优化写法'],
    ),
)
