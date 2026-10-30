G0 = [[7, 5, 7], [5, 1, 5], [7, 5, 7]]
CODE = '''
class Solution(object):
    def minOperations(self, grid, k):
        

        m = len(grid)
        n = len(grid[0])

        f = [[0] * (n + 2) for _ in range(m + 2)]

        mi = max([max(row) for row in grid])
        target = None
        for i in range(m):
            for j in range(n):
                x2, y2 = i + 1, j + 1
                x1 = max(0, x2 - k)
                y1 = max(0, y2 - k)

                f[x2][y2] = f[x2][y2 - 1] + f[x2 - 1][y2] - f[x2 - 1][y2 - 1]
                v = f[x2][y2] - f[x1][y2] - f[x2][y1] + f[x1][y1]
                d = -v - grid[i][j]

                if (i % k > 0 or j  % k > 0) and i < m // k * k and j < n // k * k:    
                    if d < 0:
                        return -1

                    if i + k <= m and j + k <= n:
                        f[x2][y2] += d
                    elif d != 0:
                        return -1
                
                elif i + k <= m and j + k <= n:
                    mi = max(mi, -d)
                    f[x2][y2] += d
                elif target is None:
                    target = -d
                elif target != -d:
                    return -1

        if target is None:
            target = mi
        elif target < mi:
            return -1
        
        tot = 0
        for i in range(m):
            for j in range(n):
                tot += target - grid[i][j]
        
        return tot // (k * k)
'''
_ls = CODE.split('\n')


def _ln(sub, nth=1):
    return [k for k, t in enumerate(_ls, 0) if sub in t][nth - 1]


L_IF1 = _ln('if (i % k > 0')
L_DNEG = _ln('if d < 0')
L_IN = _ln('if i + k <= m and j + k <= n:', 1)
L_ELIF2 = _ln('elif d != 0')
L_MAIN = _ln('elif i + k <= m and j + k <= n:')
L_MI = _ln('mi = max(mi, -d)')
L_TNONE = _ln('elif target is None')
L_TNE = _ln('elif target != -d')
L_AFTER = next(k for k, s in enumerate(_ls, 0) if s.strip() == 'if target is None:')
L_V = _ln('v = f[x2]')
L_FADD = _ln('f[x2][y2] = f[x2][y2 - 1]')


def _kind(S):
    i, j, k, m, n = S['i'], S['j'], S['k'], S['m'], S['n']
    if (i % k > 0 or j % k > 0) and i < m // k * k and j < n // k * k:
        return 'A'
    if i + k <= m and j + k <= n:
        return 'B'
    return 'C'


def _txt(S):
    if 'd' not in S or 'i' not in S or S.get('_line', 0) < L_V or S['_line'] >= L_AFTER:
        return '`target` 是最终的统一值；从左上到右下逐格修正，每格只能由「以它为左上角的 k×k」来改'
    i, j = S['i'], S['j']
    kd = _kind(S)
    d = S['d']
    if kd == 'A':
        return f'(`{i}`,`{j}`) 前面已有修正盖到它：修正值 `{d}`（不含 target）→ ==必须 ≥ 0=='
    if kd == 'B':
        return f'(`{i}`,`{j}`) 是 k×k 的左上角：修正值 = `target {"+" if d >= 0 else "−"} {abs(d)}`，要求 `target ≥ {-d}`'
    return f'(`{i}`,`{j}`) 在边界，没法再当左上角：必须 `target = {-d}`'


def _gcolor(S, i, j, v):
    if 'x1' not in S or S.get('_line', 0) < L_V or S['_line'] >= L_AFTER:
        return None
    if (i, j) == (S['i'], S['j']):
        return 'yellow'
    if S['x1'] <= i + 1 - 0 <= S['x2'] and S['y1'] <= j + 1 <= S['y2'] and i + 1 > S['x1'] and j + 1 > S['y1']:
        return 'blue'
    return None


def _fcolor(S, i, j, v):
    if 'x1' not in S or S.get('_line', 0) < L_FADD or S['_line'] >= L_AFTER:
        return None
    x1, x2, y1, y2 = S['x1'], S['x2'], S['y1'], S['y2']
    if (i, j) == (x2, y2):
        return 'yellow'
    if S['_line'] >= L_V:
        if (i, j) in ((x1, y2), (x2, y1)):
            return 'pink'
        if (i, j) == (x1, y1):
            return 'blue'
    return None


CONFIG = dict(
    num=3888, title='使所有网格元素相等的最小操作次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='从左上往右下逐格修正 + 二维前缀和',
    tags=['常用数据结构'],
    code=CODE,
    call=f'Solution().minOperations({G0}, 2)',
    expect=8,
    skip=['f[x2][y2] += d', 'v = f[x2]', 'f[x2][y2] = f[x2][y2 - 1]', 'tot += target', 'm = len', 'n = len', 'x2, y2 =', 'x1 = ', 'y1 = ', 'for i in range', 'for j in range'],
    max_steps=110,
    views=[
        dict(type='text', fn=_txt, size=24, h=70),
        dict(type='grid', var='grid', label='grid（黄 = 当前格，蓝 = 能改到它的 k×k 范围）', color=_gcolor, h=250, cell=80),
        dict(type='table', var='f', label='f：修正值（常数部分）的二维前缀和（黄 = 当前，粉蓝 = 要减掉的）', color=_fcolor, h=330, cell=56),
    ],
    watch=['k', 'i', 'j', 'v', 'd', 'target', 'mi'],
    captions={
        'f = [[0]': '`f` 是「修正值」的二维前缀和，多一圈方便减',
        'mi = max([': '`mi` = 目前已知 `target` 的下界，先取 grid 最大值 `{mi}`（只能加，不能减）',
        'target = None': '`target` 还没被确定',
        'd = -v': '`v` = 已做的修正里落在以 (`{i}`,`{j}`) 为右下角的 k×k 内的总和 = `{v}`；这格现在的值（不含 target）= `{v} + {grid[i][j]}` = `{v + grid[i][j]}`，所以修正值常数部分 `d` = =={d}=='
                  ,
        L_IF1: lambda S, B, r: {'A': '`i % k`、`j % k` 不全为 0，且不在边界：前面某次修正已盖到它 → ==修正值不含 target==',
                                'B': '(i,j) 是 k×k 块的起点（`i%k=0` 且 `j%k=0`）→ 修正值里==含有 target==',
                                'C': '在最后不足 k 的边界：不能再当左上角去修正'}[_kind(S)],
        L_DNEG: lambda S, B, r: (f'`d = {S.d} < 0`：要减小这个格子，操作只能加 → ==无解，返回 -1==' if S.d < 0
                                 else f'`d = {S.d} ≥ 0`：只需再加 `{S.d}` 次，合法'),
        L_IN: lambda S, B, r: (f'`({S.i},{S.j})` 还能放下 k×k → 真的做 `{S.d}` 次修正，记进 `f`' if S.i + S.k <= S.m and S.j + S.k <= S.n
                               else f'`({S.i},{S.j})` 放不下 k×k，没法修正'),
        L_ELIF2: lambda S, B, r: (f'`d = {S.d} != 0`：这格不能修正却还差 `{S.d}` → ==返回 -1==' if S.d != 0 else '`d = 0`：刚好不用改，没问题'),
        L_MAIN: lambda S, B, r: ('含 target 的修正值，可以主动修正' if _kind(S) == 'B' else '放不下 k×k：这格在边界，往下看它能不能定下 target'),
        L_MI: lambda S, B, r: f'这格的修正值是 `target − {-S.d}` ≥ 0 → `target ≥ {-S.d}`，`mi` 更新为 =={S.mi}==，同时把常数部分 `d` 记进 `f`',
        L_TNONE: lambda S, B, r: ('边界格不能再修正，它最终的值只能是 target' + ('：`target` 还没定，由它来定' if S.target is None else f'：`target` 已是 `{S.target}`，不用再定')),
        'target = -d': '这格没法修正 → `target = {-d}`（就是它现在的值）',
        L_TNE: lambda S, B, r: (f'`target = {S.target}` 与这格要求的 `{-S.d}` 矛盾 → ==返回 -1==' if S.target != -S.d
                                else f'这格要求 `target = {-S.d}`，与已确定的 `{S.target}` 一致，没矛盾'),
        L_AFTER: lambda S, B, r: ('没有边界格限制，`target` 取下界 `mi`' if S.target is None else f'`target = {S.target}` ≥ `mi = {S.mi}`，合法'),
        'elif target < mi': '`target = {target}` 不能小于下界 `mi = {mi}`（操作只能加）：{target} ≥ {mi}，合法',
        'tot = 0': '`tot` 累计每个格子补到 `target` 要增加多少',
        'return tot': '总共要增加 `{tot}`，每次操作加 `k×k` 个格子：`{tot} // {k*k}` = =={ret}== 次',
    },
    cards=dict(
        one_liner='设最终值 target，从左上到右下逐格修正，格格有解',
        complexity='时间 `O(mn)`，空间 `O(mn)`',
        problem=['`m × n` 的整数网格 `grid` 和整数 `k`',
                 '一次操作：选任意 `k × k` 子矩阵，所有元素 `+1`',
                 '求让整个网格==元素全相等==的最少操作次数，不可能则返回 `-1`',
                 '本视频：`[[7,5,7],[5,1,5],[7,5,7]]`，`k = 2` → `8`'],
        quote='对于(0, 0)，只能通过修改以(0, 0)为左上角，边长为k的子矩阵，才能使得(0, 0)这个单元格的元素产生变化……需要从上到下，从左到右，一个一个单元格修正过来。',
        quote_src='—— yiduobo 题解原文',
        idea=['设最终都变成 `target`；(0,0) 只有一种改法，之后每个格子都==被迫==由「以它为左上角的 k×k」来改',
              '修正值 = target − 当前值；当前值受前面修正影响，用二维前缀和 `f` 算',
              '修正值 `< 0` 或边界格对不上 → 无解；边界格直接确定 `target`，其余格子给出 `target` 的下界'],
        summary=['时间、空间 `O(mn)`',
                 '修正值只记常数部分，是否含 `target` 由位置推出：`i%k==0 且 j%k==0` 的格子含 target',
                 '易错：边界格（放不下 k×k）不能修正，要么确定 `target`，要么必须 `d == 0`',
                 '最后答案 = 所有格子补到 `target` 的差值总和 `//` `k*k`',
                 '原文为 Python 2 风格，整数除法本来就写成 `//`，代码未改'],
    ),
)
