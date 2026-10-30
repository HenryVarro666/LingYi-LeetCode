CONFIG = dict(
    num=3180, title='执行操作可获得的最大总奖励 I', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='去重 + 背包 + 记忆化剪枝',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1849'],
    code='''
class Solution(object):
    def maxTotalReward(self, rewardValues):

        nums = sorted(list(set(rewardValues)))
        
        ma = nums[-1]
        nums.pop()
        f = [len(nums)] * ma
        f[0] = -1
        g = [-1] * ma

        def calc(v, p):
            if f[v] <= p:
                return True
            if g[v] >= p:
                return False

            while p >= 0 and nums[p] > v:
                p -= 1

            res = False
            for index in range(p, -1, -1):
                if nums[index] * 2 <= v:
                    break
                
                if calc(v - nums[index], index - 1):
                    res = True
                    break

            if res:
                f[v] = min(f[v], p)
            else:
                g[v] = max(g[v], p)
        
            return res
        
        for v in range(ma - 1, -1, -1):
            if calc(v, len(nums) - 1):
                return v + ma
''',
    call='Solution().maxTotalReward([1,6,4,3,2])',
    expect=11,
    views=[
        dict(type='array', var='nums', label='nums（去重排序、去掉 ma 后）', h=215, cell=70,
             pointers={'p': 'blue', 'index': 'pink'}),
        dict(type='array', var='f', label='f[v]：能凑出 v 的最小前缀下标', h=205, cell=64,
             pointers={'v': 'yellow'}),
        dict(type='array', var='g', label='g[v]：确定凑不出 v 的最大前缀下标', h=150, cell=64),
        dict(type='calls', h=170),
    ],
    watch=[('ma', 'ma', 'cyan'), ('v', 'v', 'yellow'), ('p', 'p', 'blue'), ('index', 'index', 'pink'), ('res', 'res', 'green')],
    max_steps=75,
    captions={
        'nums = sorted': '奖励必须严格大于当前和，所以相同的值最多选一个 → 先去重再排序：`nums = {nums}`',
        'ma = nums[-1]': '最大值 `ma = {ma}` 一定会选（用它替换已选的最大值只会更好），先把它拿掉',
        'nums.pop()': '问题变成：从剩下的数里凑出一个 ==不超过 ma - 1== 的最大和 `v`，答案就是 `v + ma`',
        'f = [len(nums)]': '`f[v]` 初始 `{len(nums)}`（= 还不知道能凑出）；`f[0] = -1` 表示不选任何数就能凑出 0',
        'g = [-1]': '`g[v]` 初始 -1（= 还没发现凑不出）',
        'if f[v] <= p': lambda S, B, r: (f'已知前 `{S.f[S.v] + 1}` 个数就能凑出 `{S.v}`（`f[{S.v}] = {S.f[S.v]}` ≤ `p = {S.p}`）→ ==直接返回 True==' if S.f[S.v] <= S.p else f'`f[{S.v}] = {S.f[S.v]}` > `p = {S.p}`，还不能确定凑得出，往下'),
        'if g[v] >= p': lambda S, B, r: (f'已知连前 `{S.g[S.v] + 1}` 个数都凑不出 `{S.v}`（`g[{S.v}] = {S.g[S.v]}` ≥ `p = {S.p}`）→ ==直接返回 False==' if S.g[S.v] >= S.p else f'`g[{S.v}] = {S.g[S.v]}` < `p = {S.p}`，还不能确定凑不出，往下'),
        'while p >= 0': lambda S, B, r: (f'`nums[{S.p}] = {S.nums[S.p]}` > `v = {S.v}`：太大，最后选的数得 ≤ `v`，`p` 左移' if S.p >= 0 and S.nums[S.p] > S.v else (f'`nums[{S.p}] = {S.nums[S.p]}` ≤ `v = {S.v}`，`p = {S.p}` 停下' if S.p >= 0 else '没有能选的数了')),
        'res = False': '枚举「最后一个选的数」`nums[index]`，看剩下的 `v - nums[index]` 能不能凑出',
        'for index in range': '`index = {index}`，最后一个选 `nums[{index}] = {nums[index]}`',
        'if nums[index] * 2 <= v': lambda S, B, r: (f'`nums[{S.index}] × 2 = {S.nums[S.index] * 2}` ≤ `{S.v}`：它不大于剩下的和，不满足「大于当前和」，更小的数也不行 → ==剪枝 break==' if S.nums[S.index] * 2 <= S.v else f'`nums[{S.index}] × 2 = {S.nums[S.index] * 2}` > `{S.v}`，它比 `v - nums[index]` 大，合法'),
        'if calc(v - nums[index]': '递归：选了 `nums[{B.index}] = {B.nums[B.index]}`，剩下的 `{B.v - B.nums[B.index]}` 能用前 `{B.index}` 个数（下标 ≤ `{B.index - 1}`）凑出吗？',
        'res = True': '找到一种方案 → `res = True`，不用再枚举了',
        'f[v] = min': '能凑出 `{v}`：用前缀下标 `{p}` 以内就够 → `f[{v}] = {f[v]}`（以后查到 `p ≥ {f[v]}` 直接返回 True）',
        'g[v] = max': '凑不出 `{v}`：连前缀下标 `{p}` 以内都不行 → `g[{v}] = {g[v]}`（以后查到 `p ≤ {g[v]}` 直接返回 False）',
        'return res': '`calc({v}, ·)` 返回 `{ret}`',
        'for v in range(ma - 1': '从大到小试每个和 `v = {v}`，第一个能凑出的就是最大和',
        'if calc(v, len(nums) - 1)': '问：用全部 `{len(nums)}` 个数能凑出 `{B.v}` 吗？',
        'return v + ma': '最大能凑出的和 `v = {v}`，加上最大值 `ma = {ma}` → =={ret}==',
    },
    cards=dict(
        one_liner='去重、拿走最大值，再凑不超过 ma-1 的最大和',
        complexity='背包 `O(n·ma)`；本文用记忆化 + 剪枝，复杂度不好严格分析',
        problem=['`rewardValues` 长度 `n`，总奖励 `x` 初始 0；每次选一个未选的下标，若 `rewardValues[i] > x` 就把它加到 `x`',
                 '返回能得到的==最大总奖励==',
                 '示例：`[1,6,4,3,2]` → `11`（依次选 1、4、6）'],
        quote='最大值 ma 是必然会被选择的，因为如果没有选择 ma，那么对于当前的选择方案，使用 ma 去替代已选择的最大值必然是可行的，同时总奖励值也会更优。',
        quote_src='—— yiduobo 题解',
        idea=['值必须大于当前和 → 不会选相同的值，先去重排序',
              '最大值必选 → 拿走它，问题变成「用其余的数凑不超过 `ma-1` 的最大和」，即背包',
              '写成记忆化搜索 `calc(v, p)`：最后一个选的数 `> v/2` 才合法（剪枝）；`f/g` 记录最小可行前缀、最大不可行前缀'],
        summary=['`f[v]` 记「前缀越长越容易凑出」的单调性：能凑出的最小前缀、凑不出的最大前缀',
                 '易错：`nums` 要先 ==去重 + 排序==，最大值 `ma` 单独拿走；`v` 从 `ma-1` 往下找第一个能凑出的',
                 '思路等价于 0-1 背包的可达性 DP（`f[i][j]` 能否凑出 `j`），`O(n·ma)` 对本题已够',
                 '本题代码已是 Python 3 写法（只用到 `range`、`min`、`max`），无需改动'],
    ),
)
