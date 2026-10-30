def _I(S):
    return S['_inner'].get('i')


def _txt(S):
    I = S['_inner']
    if 'i' not in I:
        return '`dfs(i, s, m, odd, empty)`：`s` = 交错和，`m` = 元素积（超过 limit 记作 limit+1）'
    sgn = '减' if I['odd'] else '加'
    sub = '空' if I['empty'] else '非空'
    return f'`i={I["i"]}`　交错和 `s={I["s"]}`　乘积 `m={I["m"]}`　选 x 时{sgn}　子序列{sub}　目标 `k={S["k"]}`，`ans={S["ans"]}`'


CONFIG = dict(
    num=3509, title='最大化交错和为 K 的子序列乘积', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='选或不选 · 记忆化暴搜（状态很少）',
    tags=['灵神题单·动态规划', '难度分 2703'],
    code='''
class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        if sum(nums) < abs(k):  # |k| 太大
            return -1

        n = len(nums)
        ans = -1

        @cache  # 当 vis 哈希表用
        def dfs(i: int, s: int, m: int, odd: bool, empty: bool) -> None:
            nonlocal ans
            if ans == limit or m > limit and ans >= 0:  # 无法让 ans 变得更大
                return

            if i == n:
                if not empty and s == k and m <= limit:  # 合法子序列
                    ans = max(ans, m)  # 用合法子序列的元素积更新答案的最大值
                return

            # 不选 x
            dfs(i + 1, s, m, odd, empty)

            # 选 x
            x = nums[i]
            dfs(i + 1, s + (-x if odd else x), min(m * x, limit + 1), not odd, False)

        dfs(0, 0, 1, False, True)
        return ans
''',
    call='Solution().maxProduct([2, 2, 3, 3], 0, 9)',
    expect=9,
    views=[
        dict(type='text', fn=_txt, h=80),
        dict(type='array', var='nums', label='nums（蓝 = 正在决定选不选的 nums[i]）', cell=70, h=140,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'},
             dim=lambda S, i, v: S['_inner'].get('i') is not None and i < S['_inner']['i']),
        dict(type='calls', h=300),
        dict(type='text', fn=lambda S: f'目标：交错和 `s = {S["k"]}`，乘积不超过 `limit = {S["limit"]}` 且尽量大　→　当前 `ans = {S["ans"]}`' if 'ans' in S else '', h=60),
    ],
    watch=[('ans', 'ans', 'green'), ('k', 'k'), ('limit', 'limit'), ('i', lambda S: S['_inner'].get('i'), 'blue'),
           ('s', lambda S: S['_inner'].get('s'), 'cyan'), ('m', lambda S: S['_inner'].get('m'), 'yellow')],
    captions={
        'if sum(nums) < abs(k)': lambda S, B, r: (f'元素和 `{sum(S.nums)}` < `|k| = {abs(S.k)}`：交错和不可能到 k → 直接 -1' if sum(S.nums) < abs(S.k)
                                                else f'元素和 `{sum(S.nums)}` ≥ `|k| = {abs(S.k)}`，k 不是离谱大，继续搜'),
        'ans = -1': '`ans = -1`：还没找到合法子序列',
        '@cache': '`@cache` 当 vis 哈希表：同一个状态只搜一次',
        'if ans == limit': lambda S, B, r: (f'`ans = {S.ans} = limit`，已经到上限，不用再搜' if S.ans == S.limit
                                            else (f'`m = {S.m} > limit` 且 `ans = {S.ans} ≥ 0`：乘积已超限，只能变成 0，而 ans 已经有解 → 剪枝'
                                                  if S.m > S.limit and S.ans >= 0 else f'`ans = {S.ans}`，`m = {S.m}`：还有希望，继续搜')),
        'if i == n': lambda S, B, r: (f'`i = {S.i} = n`：每个数都决定完了，检查这个子序列' if S.i == S.n else f'`i = {S.i} < n`：还有数没决定，继续递归'),
        'if not empty': lambda S, B, r: (f'非空，`s = {S.s} = k`，`m = {S.m} ≤ {S.limit}` → ==合法子序列=='
                                         if (not S.empty and S.s == S.k and S.m <= S.limit)
                                         else f'不合法：`s = {S.s}`（要 {S.k}），`m = {S.m}`，`empty = {S.empty}`'),
        'ans = max(ans, m)': '用合法子序列的乘积更新最大值：`ans = {ans}`（不是越大越好的 DP，而是 ==枚举所有合法的积==）',
        'dfs(i + 1, s, m, odd, empty)': '==不选== `nums[{B.i}] = {nums[B.i]}`：状态不变，只有 `i` 加 1，进入 `dfs({B.i + 1}, ...)`',
        'x = nums[i]': '准备选 `x = nums[{i}] = {x}`',
        'dfs(i + 1, s + (-x': lambda S, B, r: (f'==选== `x = {B.x}`：{"奇数位，减" if B.odd else "偶数位，加"} → `s = {B.s + (-B.x if B.odd else B.x)}`；'
                                               f'乘积 `min({B.m}×{B.x}, {B.limit + 1}) = {min(B.m * B.x, B.limit + 1)}`，奇偶翻转，进入 `dfs({B.i + 1}, ...)`'),
        'dfs(0, 0, 1': '入口：`s = 0`（加法单位元），`m = 1`（乘法单位元），子序列为空',
        'return ans': '`ans = {ans}`：交错和为 k、乘积不超过 limit 的最大乘积',
    },
    max_steps=90,
    cards=dict(
        one_liner='状态数其实很少，直接记忆化暴搜，不必强行 DP',
        complexity='时间 `O(n(nU + M log limit))`，空间同阶',
        problem=['选一个非空子序列，交错和（偶数下标加、奇数下标减）等于 `k`',
                 '在乘积 ==不超过 limit== 的前提下，让乘积最大；没有就返回 -1',
                 '示例：`nums = [2,2,3,3], k = 0, limit = 9` → `9`（选 `[3,3]`）'],
        quote='在乘积不为 0 且不超过 limit 的情况下，交错和的绝对值其实远小于 nums 的元素和！此外，150 个 [1,12] 中的数相乘，只有 394 个 ≤ 5000 的不同乘积。',
        quote_src='—— 灵茶山艾府题解',
        idea=['错误思路：dfs 返回最大乘积——像背包，小乘积和别的数相乘可能更接近 limit',
              '所以把 `(i, s, m, odd, empty)` 全作为状态；乘积超过 limit 统一记作 `limit+1`',
              '`@cache` 去重，再加三个剪枝：`sum < |k|`、`ans == limit`、`m > limit 且 ans ≥ 0`'],
        summary=['时间 `O(n(nU + M log limit))`，`M = 394` 是不超过 5000 的不同乘积个数',
                 '乘积超过 limit 记为 `limit + 1`，让状态数不爆炸；乘积为 0 时只需关心交错和',
                 '易错：不是「最大乘积」做返回值；入口是 `dfs(0, 0, 1, False, True)`',
                 '另有递推写法：用两个哈希表 `odd_s / even_s` 保存「交错和 → 乘积集合」，思路相同'],
    ),
)
