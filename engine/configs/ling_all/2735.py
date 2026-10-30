CONFIG = dict(
    num=2735, title='收集巧克力', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='枚举操作次数 + 环形子数组最小值',
    tags=[],
    code='''
class Solution:
    def minCost(self, nums: List[int], x: int) -> int:
        n = len(nums)
        s = list(range(0, n * x, x))  # s[k] 统计操作 k 次的总成本
        for i, mn in enumerate(nums):  # 子数组左端点
            for j in range(i, n + i):  # 子数组右端点（把数组视作环形的）
                mn = min(mn, nums[j % n])  # 维护从 nums[i] 到 nums[j] 的最小值
                s[j - i] += mn  # 累加操作 j-i 次的花费
        return min(s)
''',
    call='Solution().minCost([20,1,15], 5)',
    expect=13,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 左端点 i，粉 = 右端点 j % n）', h=200,
             pointers={'i': 'blue', 'j % n': 'pink'}),
        dict(type='array', var='s', label='s[k]：操作 k 次的总成本（先含操作费 k·x，再累加各巧克力的最小买价）', h=200,
             pointers={'j - i': 'green'}),
        dict(type='text', fn=lambda S: f"当前：左端点 `i={S['i']}`，操作 `{S['j']-S['i']}` 次，买第 {S['i']} 号巧克力最便宜花 ==`{S['mn']}`==" if 'j' in S and 'mn' in S and 'i' in S else ''),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('mn', 'mn', 'green'), 's'],
    captions={
        's = list(range': '`s[k]` 先放操作 k 次的操作费 `k·x`：`s = {s}`，之后只需往里加买巧克力的钱',
        'for i, mn in enumerate': lambda S, B, r: ('所有左端点都枚举完了' if 'i' in B and S.i == B.i and S.mn == B.mn and S.i == len(S.nums) - 1 and S.j == S.n + S.i - 1 and B.j == S.j
                                                  else f'枚举子数组左端点 `i = {S.i}`：第 `i` 类巧克力，起始最小值 `mn = {S.mn}`'),
        'for j in range': lambda S, B, r: (f'`i = {S.i}` 的这一圈走完了' if 'j' in B and S.j == B.j
                                           else f'右端点 `j = {S.j}`：操作 `{S.j - S.i}` 次后，第 `i` 类巧克力的位置轮到 `nums[{S.j % S.n}]`'),
        'mn = min': '操作 `{j - i}` 次内能买的最低价：`min({B.mn}, nums[{j % n}])` = =={mn}==',
        's[j - i] += mn': '把这块巧克力的最优花费 `{mn}` 加到 `s[{j - i}]`：`s[{j - i}] = {s[j - i]}`',
        'return min(s)': '每个操作次数的总成本都算完：`s = {s}`，取最小 ==`{min(s)}`==',
    },
    cards=dict(
        one_liner='枚举操作次数 k，每块巧克力取环形窗口里最便宜的买',
        complexity='时间 `O(n²)`，空间 `O(n)`',
        problem=['`nums[i]` 是收集第 `i` 类巧克力的成本；每次操作花 `x`，所有类型 `i → (i+1) mod n`',
                 '求收集全部类型的最小总成本',
                 '示例：`nums=[20,1,15], x=5` → `13`（操作 2 次，每块都花 1）'],
        quote='把 mn 加到 s[j-i] 中，这是因为长为 j-i+1 的子数组恰好对应着操作 j-i 次时要计算的子数组。',
        quote_src='—— 灵茶山艾府题解',
        idea=['操作 k 次后，第 `i` 块巧克力可以在 `nums[i..i+k]`（环形）里挑最便宜的买',
              '二重循环枚举左端点 `i` 和右端点 `j`，边走边维护区间最小值 `mn`',
              '`mn` 累加进 `s[j-i]`，最后对所有操作次数取 `min(s)`'],
        summary=['时间 `O(n²)`，空间 `O(n)`；不用预处理所有子数组最小值的二维表',
                 '`s` 初值 `range(0, n*x, x)` 里已经带上了操作费 `k·x`',
                 '右端点 `j` 走到 `n+i-1`，用 `j % n` 把数组当环',
                 '操作 `n` 次等于没操作，所以 k 只枚举到 `n-1`'],
    ),
)
