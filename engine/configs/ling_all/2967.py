import bisect as _bs


def _gen():
    out = []
    base = 1
    while base <= 10000:
        for i in range(base, base * 10):
            s = str(i)
            out.append(int(s + s[::-1][1:]))
        if base <= 1000:
            for i in range(base, base * 10):
                s = str(i)
                out.append(int(s + s[::-1]))
        base *= 10
    return out


PAL = _gen()


def _med(S):
    n = len(S['nums'])
    return (n - 1) // 2, n // 2


def _t_top(S):
    if 'n' not in S:
        return '先把 `nums` 排序：为了找==中位数==；所有数变成中位数，距离和最小'
    lo, hi = _med(S)
    a = S['nums']
    msg = f'中位数范围 `nums[{lo}] = {a[lo]}` ~ `nums[{hi}] = {a[hi]}`'
    if 'i' in S and 'target' not in S:
        i = S['i']
        msg += f'；二分得 `pal[{i}] = {PAL[i]}`（第一个 ≥ {a[lo]} 的回文数）'
    return msg


def _t_pal(S):
    if 'i' not in S:
        return '回文数表 `pal` 已预处理好（升序）：只需要在中位数附近找最近的回文数'
    i = S['i']
    if i == 0:
        return f'`pal[0] = {PAL[0]}`'
    return f'`pal[{i-1}] = {PAL[i-1]}`   |   ==`pal[{i}] = {PAL[i]}`==   |   `pal[{i+1}] = {PAL[i+1]}`'


def _t_cost(S):
    if 'target' not in S:
        return ''
    t = S['target']
    parts = ' + '.join(str(abs(x - t)) for x in S['nums'])
    return f'变成 `{t}`：`{parts}` = =={sum(abs(x - t) for x in S["nums"])}=='


def _color(S, i, v):
    if 'n' not in S:
        return None
    lo, hi = _med(S)
    return 'yellow' if lo <= i <= hi else None


def _cmp(S, B, ret):
    lo, hi = _med(S)
    p, m = PAL[S['i']], S['nums'][hi]
    if p <= m:
        return f'`pal[i] = {p} ≤ nums[{hi}] = {m}`：回文数正好落在中位数范围内 → 它就是最优目标'
    return f'`pal[i] = {p} > nums[{hi}] = {m}`：回文数在中位数右边，取不到中位数 → 还要比较左边的 `pal[i-1] = {PAL[S["i"]-1]}`'


CONFIG = dict(
    num=2967, title='使数组成为等数数组的最小代价', difficulty='Medium', category='数学算法',
    author='灵茶山艾府', technique='中位数贪心 + 二分回文数',
    tags=['灵神题单·数学算法', '灵神题单·贪心与思维', '难度分 2116'],
    code='''
# 严格按顺序从小到大生成所有回文数（不用字符串转换）
pal = []
base = 1
while base <= 10000:
    # 生成奇数长度回文数
    for i in range(base, base * 10):
        x = i
        t = i // 10
        while t:
            x = x * 10 + t % 10
            t //= 10
        pal.append(x)
    # 生成偶数长度回文数
    if base <= 1000:
        for i in range(base, base * 10):
            x = t = i
            while t:
                x = x * 10 + t % 10
                t //= 10
            pal.append(x)
    base *= 10
pal.append(1_000_000_001)  # 哨兵，防止下面代码中的 i 下标越界

class Solution:
    def minimumCost(self, nums: List[int]) -> int:
        # 注：排序只是为了找中位数，如果用快速选择算法，可以做到 O(n)
        nums.sort()

        # 返回 nums 中的所有数变成 pal[i] 的总代价
        def cost(i: int) -> int:
            target = pal[i]
            return sum(abs(x - target) for x in nums)

        n = len(nums)
        i = bisect_left(pal, nums[(n - 1) // 2])  # 二分找中位数右侧最近的回文数
        if pal[i] <= nums[n // 2]:  # 回文数在中位数范围内
            return cost(i)  # 直接变成 pal[i]
        return min(cost(i - 1), cost(i))  # 枚举离中位数最近的两个回文数 pal[i-1] 和 pal[i]
''',
    call='Solution().minimumCost([10, 12, 13, 14, 15])',
    expect=11,
    views=[
        dict(type='text', fn=_t_top, size=30, h=70),
        dict(type='array', var='nums', color=_color, h=200, label='nums（黄 = 中位数）'),
        dict(type='text', fn=_t_pal, size=34, h=90),
        dict(type='text', fn=_t_cost, size=34, h=90),
    ],
    watch=['n', 'i', ('target', 'target', 'orange'), ('pal[i]', 'PAL_I', 'cyan')] if False else ['n', 'i', ('target', 'target', 'orange')],
    skip=['def cost'],
    captions={
        'nums.sort()': '先排序，为了取==中位数==：`nums = {nums}`',
        'n = len(nums)': '`n = {n}`，中位数下标 `(n-1)//2 = {(n-1)//2}`、`n//2 = {n//2}`',
        'i = bisect_left': '二分找第一个 `>= {nums[(n-1)//2]}` 的回文数，位置 `i = {i}`，即中位数==右侧最近==的回文数',
        'if pal[i] <=': _cmp,
        'return cost(i)  #': '回文数落在中位数范围里，变成它代价最小 → 直接 `cost(i)`',
        'return min(cost': '回文数取不到中位数：最优在==中位数左右各最近==的两个回文数里，取代价小的',
        'target = pal[i]': '目标数 `target = pal[{i}] = {target}`',
        'return sum(': '所有数变成 `{target}` 的总操作数 = =={ret}==',
    },
    cards=dict(
        one_liner='全部变成中位数最省；取不到就找离中位数最近的回文数',
        complexity='时间 `O(n log n + log U)`，空间 `O(1)`（预处理不计）',
        problem=['每次操作把某个数 `+1` 或 `-1`，要让所有数变成==同一个正回文数==',
                 '求最少操作次数',
                 '示例：`[10,12,13,14,15]` → `11`（都变成 11）'],
        quote='将 a 的所有元素变为 a 的**中位数**是最优的。……本题回文数可能取不到中位数，我们可以找离中位数最近的数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['预处理 `10^9` 内全部回文数：==枚举左半边==，反转拼回去，奇偶长度各一次',
              '距离和是凸函数：目标离中位数越近代价越小',
              '二分找中位数右侧最近的回文数 `pal[i]`，再看左边的 `pal[i-1]`，取较小代价'],
        summary=['时间 `O(n log n)`（排序可用快速选择降到 `O(n)`），预处理和回文数表不计',
                 '偶数长度时中位数是一段区间 `[nums[(n-1)//2], nums[n//2]]`，回文数落在其中直接用',
                 '回文数表末尾加哨兵 `10^9+1`，防止 `pal[i]` 越界',
                 '预处理在引擎里先于追踪执行，视频只演示 `minimumCost` 本身',
                 '思考题：564. 寻找最近的回文数'],
    ),
)
