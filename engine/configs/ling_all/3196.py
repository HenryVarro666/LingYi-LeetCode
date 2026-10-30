A0 = [1, -2, 3, 4, -1, 2]


def _ac(S, k, v):
    i = S.get('i')
    if i is None:
        return None
    if k == i:
        return 'blue'
    if k == i - 1:
        return 'pink'
    return None


def _fc(S, k, v):
    i = S.get('i')
    if i is None:
        return 'yellow' if k == 1 and S.get('_line') == 5 else None
    if S.get('_line') in (6, 7):
        if k == i + 1:
            return 'yellow'
        if k == i:
            return 'blue'
        if k == i - 1:
            return 'pink'
    return None


def _formula(S):
    i = S.get('i')
    if i is None:
        return '`f[k]` = 前 `k` 个数分段后的最大成本和；每段只需考虑长为 1（`+`）或长为 2（`+-`）'
    a, f = S['a'], S['f']
    one = f[i] + a[i]
    two = f[i - 1] + a[i - 1] - a[i]
    if S.get('_line') == 7:
        return f'长 1：`f[{i}] + a[{i}]` = =={one}==　　长 2：`f[{i-1}] + a[{i-1}] − a[{i}]` = =={two}==　→　取大'
    return f'要算 `f[{i+1}]`：`a[{i}]` 单独成段，或 `a[{i-1}], a[{i}]` 成一段'


CONFIG = dict(
    num=3196, title='最大化子数组的总成本', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP（段长只需 1 或 2）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1847'],
    code='''
class Solution:
    def maximumTotalCost(self, a: List[int]) -> int:
        n = len(a)
        f = [0] * (n + 1)
        f[1] = a[0]
        for i in range(1, n):
            f[i + 1] = max(f[i] + a[i], f[i - 1] + a[i - 1] - a[i])
        return f[n]
''',
    call=f'Solution().maximumTotalCost({A0!r})',
    expect=13,
    views=[
        dict(type='array', var='a', label='a（蓝 = a[i]，粉 = a[i-1]）', h=170, cell=80, color=_ac,
             pointers={'i': 'blue'}),
        dict(type='text', fn=_formula, size=25, h=70),
        dict(type='array', var='f', label='f[k]（黄 = 正在算 f[i+1]，蓝 = f[i]，粉 = f[i-1]）', h=190, cell=80, color=_fc),
    ],
    watch=[('i', 'i', 'blue'), ('f[i]', 'f[i]', 'blue'), ('f[i-1]', 'f[i-1]', 'pink'), ('f[n]', 'f[-1]', 'green')],
    captions={
        'n = len(a)': '`n = {n}`',
        'f = [0] * (n + 1)': '`f[0] = 0`：没有数字时成本为 0，对应递归边界 `dfs(-1) = 0`',
        'f[1] = a[0]': '只有 `a[0]` 时只能 `+a[0]`：`f[1] = {a[0]}`，对应 `dfs(0) = a[0]`',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：决定 `a[{S.i}]` 怎么分段，结果放进 `f[{S.i+1}]`' if S.get('i') != B.get('i')
                                           else '所有数都处理完了，循环结束'),
        'f[i + 1] = max': lambda S, B, r: (f'长 1 段 `+a[{S.i}]`：`{S.f[S.i]} + {S.a[S.i]}` = {S.f[S.i] + S.a[S.i]}；长 2 段 `+a[{S.i-1}] −a[{S.i}]`：'
                                           f'`{S.f[S.i-1]} + {S.a[S.i-1]} − ({S.a[S.i]})` = {S.f[S.i-1] + S.a[S.i-1] - S.a[S.i]} → 取大得 `f[{S.i+1}]` = =={S.f[S.i+1]}=='),
        'return f[n]': '`f[{n}]` 是整个数组分段后的最大成本和 = =={ret}==',
    },
    cards=dict(
        one_liner='长段能拆成长 2 和长 1，只考虑这两种段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['子数组 `a[l..r]` 的成本是 `a[l] − a[l+1] + a[l+2] − ...` 交替加减',
                 '把数组分成若干子数组，使成本之和最大',
                 '示例：`[1,-2,3,4]` → `10`（`[1,-2,3]` 和 `[4]`）'],
        quote='对于长度超过 2 的子数组，可以继续分割为长度为 2 和 1 的子数组，而不改变成本之和。',
        quote_src='—— 灵茶山艾府题解（方法一）',
        idea=['`+-+` 可拆成 `+-` 和 `+`，`+-+-` 拆成 `+-`、`+-`，所以段长只用 1 或 2',
              '`dfs(i)` = `a[0..i]` 的最大成本和，最后一段长 1 或长 2，两者取大',
              '`f` 左边插一格表示 `dfs(-1)`，`f[i+1]` 对应 `dfs(i)`'],
        summary=['时间 `O(n)`，空间 `O(n)`；`f[i+1]` 只用到 `f[i]` 和 `f[i-1]`，可滚动成两个变量 `O(1)`',
                 '易错：`f` 比 `a` 多一格；`a` 的下标不用偏移，`f` 的才偏移',
                 '题解还有方法二：状态机 DP，用「要不要变号」两个状态，不需要拆段这个性质',
                 '同类：213. 打家劫舍 II 的滚动变量、买卖股票系列状态机 DP'],
    ),
)
