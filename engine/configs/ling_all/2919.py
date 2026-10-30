NUMS = [3, 1, 0, 2, 5, 6]
K = 4


def _i(S):
    return S['nums'].index(S['x']) if 'x' in S else None


def _txt(S):
    if 'f0' not in S:
        return '`f0 / f1 / f2`：当前数的右边有 0 / 1 / 2 个连续没增大的数时，前面这些数的最小操作数'
    return f"`f0 = {S['f0']}`，`f1 = {S['f1']}`，`f2 = {S['f2']}`"


CONFIG = dict(
    num=2919, title='使数组变美的最小增量运算数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP · 递推滚动变量',
    tags=['灵神题单', '动态规划', '难度分 2031'],
    code='''
class Solution:
    def minIncrementOperations(self, nums: List[int], k: int) -> int:
        f0 = f1 = f2 = 0
        for x in nums:
            inc = f0 + max(k - x, 0)
            f0 = min(inc, f1)
            f1 = min(inc, f2)
            f2 = inc
        return f0
''',
    call=f'Solution().minIncrementOperations({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='array', var='nums', label=f'nums（k = {K}）', cell=96, h=190, pointers={'i': 'blue'},
             color=lambda S, j, v: 'blue' if j == _i(S) else None,
             dim=lambda S, j, v: _i(S) is not None and j > _i(S)),
        dict(type='array', var=lambda S: [S['f0'], S['f1'], S['f2']] if 'f0' in S else [0, 0, 0],
             label='f0 | f1 | f2', cell=120, h=200, index=False,
             color=lambda S, j, v: 'green' if S.get('_line') in (6, 7, 8) and j == S.get('_line') - 6 else None),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=[('x', 'x', 'blue'), ('inc', 'inc', 'orange'), ('f0', 'f0', 'green'), ('f1', 'f1', 'cyan'), ('f2', 'f2', 'purple')],
    captions={
        'f0 = f1 = f2 = 0': '三个状态都是 0：还没有数，不需要操作',
        'for x in nums': '看下一个数 `x = {x}`',
        'inc =': '把 `{x}` 增大到 `k = {k}`：花 `max({k} - {x}, 0)`，再加上前面右边有 0 个没增大数的状态 `f0` → ==`inc = {inc}`==',
        'f0 = min': '新的 `f0`：`x` 增大（`inc`）或不增大（沿用旧 `f1`，让 x 成为“右边多一个没增大的数”）取小 → ==`{f0}`==',
        'f1 = min': '新的 `f1`：增大 `inc`，或不增大沿用旧 `f2` → ==`{f1}`==',
        'f2 = inc': '`f2`：右边已有两个没增大的数，当前数==必须增大== → `{f2}`',
        'return f0': '最后一个数右边没有数，答案是 `f0` = =={ret}==',
    },
    cards=dict(
        one_liner='每个长为 3 的窗口必须含一个 k：连续不增大的数最多两个',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可把一个数加 1；要让所有长度 ≥ 3 的子数组最大值都 `>= k`',
                 '求最少的加 1 次数',
                 f'本视频：`nums = {NUMS}`，`k = {K}`'],
        quote='把大于 k 的元素视作 k。由于大于 3 的子数组必然包含等于 3 的子数组，问题转换成：每个长为 3 的子数组，都需要包含至少一个 k。',
        quote_src='—— 灵茶山艾府题解',
        idea=['考虑最后一个数「选或不选」：增大到 k，或者不增大',
              '`j` = 右边连续没增大的数的个数（0/1/2），到 2 时当前数一定要增大',
              '记忆化搜索 1:1 翻译成递推，再只保留 3 个变量：`f0, f1, f2`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`f0 / f1 / f2` 要用==旧值==同时更新，顺序是 f0 → f1 → f2',
                 '题解主写法是记忆化搜索 `dfs(i, j)`，视频选的是它翻译成的递推写法',
                 '同类：状态机 DP，状态记录“最近连续没选了几个”'],
    ),
)
