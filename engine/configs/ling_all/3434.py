N0, K0 = [2, 3, 1, 3, 3, 2], 1
VALS = sorted(set(N0) - {K0})


def _f1(S):
    f1 = S.get('f1')
    if f1 is None:
        return [0 for _ in VALS]
    return [f'{v}→{f1[v]}' for v in VALS]


def _text(S):
    if 'f0' not in S:
        return '把「子数组里的某个数 `target`」整体改成 `k`：它的个数 − 子数组里 `k` 的个数 = 净增益'
    if 'max_f12' not in S:
        return ''
    return f'`f0`：==左边==的 k 的个数 {S["f0"]}；`max_f12`：当前能凑出的最大频率 {S["max_f12"]}'


def _col(S, i, v):
    x = S.get('x')
    if x is None:
        return None
    if v == K0:
        return 'green'
    if v == x:
        return 'yellow'
    return None


CONFIG = dict(
    num=3434, title='子数组操作后的最大频率', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='状态机 DP（一次遍历，f1 按值记）',
    tags=['灵神题单', '动态规划', '难度分 2094'],
    code='''
max = lambda a, b: a if a > b else b  # 手写 max 更快

class Solution:
    def maxFrequency(self, nums: List[int], k: int) -> int:
        f0 = max_f12 = 0
        f1 = [0] * 51  # 或者用 defaultdict(int)
        for x in nums:
            if x == k:
                max_f12 += 1
                f0 += 1
            else:
                f1[x] = max(f1[x], f0) + 1
                max_f12 = max(max_f12, f1[x])
        return max_f12
''',
    call=f'Solution().maxFrequency({N0!r}, {K0})',
    expect=3,
    skip=['max = lambda', 'a if a > b else b', 'f1 = [0] * 51'],
    views=[
        dict(type='array', var='nums', label='nums（绿 = k，黄 = 和当前 x 同值的数）', h=150, cell=90, color=_col),
        dict(type='array', var=_f1, label='f1[target]：把值为 target 的数变成 k，到目前最多能凑几个', h=150, cell=110, index=False),
        dict(type='text', fn=_text, size=24, h=70),
    ],
    watch=['x', ('f0', 'f0', 'blue'), ('max_f12', 'max_f12', 'green')],
    captions={
        'f0 = max_f12 = 0': '`f0`：「左」状态，只数 k 的个数；`max_f12`：「中」或「右」状态里的最大个数。都从 0 开始',
        'for x in nums': '看下一个数 `x = {x}`',
        'if x == k': lambda S, B, r: (f'`x = {S.x}` 等于 `k = {S.k}`' if S.x == S.k else f'`x = {S.x}` 不等于 `k = {S.k}`'),
        'max_f12 += 1': '`x` 就是 `k`：它在子数组外面就直接算，在「右」状态也算 → `max_f12 = {max_f12}`（不进「中」，因为里面的 k 会被改走）',
        'f0 += 1': '左边又多了一个 `k`：`f0 = {f0}`（以后任何以它为左侧的子数组都能带上它）',
        'f1[x] =': '把 `{x}` 当 target：要么接着之前的子数组（`f1[{x}] = {B.f1[x]}`），要么从这里重开、带上左边的 `f0 = {f0}`，再 +1 → `f1[{x}] = {f1[x]}`',
        'max_f12 = max(max_f12, f1[x])': '`max_f12 = max({B.max_f12}, f1[{x}] = {f1[x]})` = =={max_f12}==',
        'return max_f12': '遍历完，最大频率 =={max_f12}==',
    },
    cards=dict(
        one_liner='把子数组里的 target 全改成 k：枚举 target，状态机 DP 一次扫完',
        complexity='时间 `O(n + U)`，空间 `O(U)`',
        problem=['选一个子数组，把里面所有数加上同一个整数 `x`，求操作后 `k` 最多出现几次',
                 '示例：`nums = [2,3,1,3,3,2], k = 1` → `3`',
                 '把 `[3,1,3,3]` 整体减 2，得到 `[2,1,-1,1,1,2]`，有 3 个 1'],
        quote='考虑把子数组中等于 target 的元素都变成 k。……用状态机 DP 计算 nums[0] 到 nums[i] 最多有多少个数可以等于 k',
        quote_src='—— 灵茶山艾府题解',
        idea=['三个状态：左（只数 k）、中（只数 target，改成 k）、右（只数 k）',
              '一次遍历优化：`f1[x]` 按值记「中」的最优，其他值懒更新，不用枚举 target',
              '`x == k` 时子数组外直接加，`max_f12` 把「中」和「右」合并成一个变量'],
        summary=['时间 `O(n+U)`：`U` 是不同取值个数，本题 `U ≤ 50`',
                 '易错：子数组里的 `k` 会被改走，「中」状态不能数它',
                 '允许空子数组（初值 0），等价于不操作',
                 '灵神方法一是对每个 target 各跑一遍三状态 DP，本视频演示写法二（合并 f2 与 maxF1）'],
    ),
)
