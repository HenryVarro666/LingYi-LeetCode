NUMS = [1, 8, 1]
N = len(NUMS)
# 代码行号：14 for i / 15 if s>>i&1 / 17 for j / 18 if ... is_square / 19 f[s][i] += / 23-24 求和 / 27-30 去重


def _cell(S, r, c, v):
    s, i, j = S.get('s'), S.get('i'), S.get('j')
    line = S.get('_line', 0)
    if line in (14, 15, 17, 18, 19) and s is not None and i is not None:
        if (r, c) == (s, i):
            return 'yellow'
        if line in (18, 19) and j is not None and s >> j & 1 and (r, c) == (s ^ (1 << j), j):
            return 'green'
    if line in (23, 24) and S.get('i') is not None and (r, c) == (S['u'] ^ (1 << S['i']), S['i']):
        return 'yellow'
    return None


def _formula(S):
    line = S.get('_line', 0)
    s, i, j = S.get('s'), S.get('i'), S.get('j')
    if line in (18, 19) and None not in (s, i, j) and s >> j & 1:
        a, b = NUMS[i], NUMS[j]
        return f'`{a} + {b} = {a + b}`' + ('，是完全平方数 → 可以填' if int((a + b) ** 0.5) ** 2 == a + b else '，不是完全平方数 → 不能填')
    if line >= 26 and 'cnt' in S:
        return f'已算出 `ans` = {S.get("ans")}；重复数字互换会算重，要除以各数出现次数的阶乘'
    return '`f[S][i]` = 剩余可选下标集合 S、上一个数下标 i 时的合法排列数'


def _cap_if(S, B, ret):
    s, i, j = S.s, S.i, S.j
    if not s >> j & 1:
        return f'下标 `{j}` 已经填过（不在 S 里），不能再选'
    t = NUMS[i] + NUMS[j]
    if int(t ** 0.5) ** 2 == t:
        return f'`nums[{i}] + nums[{j}] = {NUMS[i]} + {NUMS[j]} = {t}` ==是完全平方数== → 可以接'
    return f'`{NUMS[i]} + {NUMS[j]} = {t}` 不是完全平方数 → 不能相邻'


CONFIG = dict(
    num=996, title='平方数组的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='排列型状压 DP（递推）+ 去重',
    tags=['灵神题单·动态规划'],
    setup='from math import isqrt',
    code='''
class Solution:
    def numSquarefulPerms(self, nums: list[int]) -> int:
        # 判断 x 是否为完全平方数
        def is_square(x: int) -> bool:
            rt = isqrt(x)
            return rt * rt == x

        n = len(nums)
        f = [[0] * n for _ in range(1 << n)]
        f[0] = [1] * n

        u = (1 << n) - 1
        for s in range(1, u):
            for i in range(n):
                if s >> i & 1:  # i 是填过的数的下标，不能在 s 中
                    continue
                for j in range(n):
                    if s >> j & 1 and is_square(nums[i] + nums[j]):
                        f[s][i] += f[s ^ (1 << j)][j]

        ans = 0
        # 枚举排列的第一个数的下标
        for i in range(n):
            ans += f[u ^ (1 << i)][i]

        # 去重
        cnt = defaultdict(int)
        for x in nums:
            cnt[x] += 1
            ans //= cnt[x]  # 比如 nums 有 3 个 x，这里会 /1 再 /2 再 /3，从而实现 /(3!)

        return ans
''',
    call=f'Solution().numSquarefulPerms({NUMS})',
    expect=1,
    skip=['rt = isqrt', 'return rt * rt', 'def is_square', 'n = len(nums)', 'for j in range(n)', 'continue', 'cnt = defaultdict', 'for x in nums', 'if s >> i & 1'],
    max_steps=64,
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var='nums', label='nums（下标 j 对应二进制第 j 位）', h=260, cell=90, pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='table', var='f', label='f[S][i]：行 = 剩余可选下标集合 S（二进制），列 = 上一个数的下标 i', h=400, cell=70,
             rows=lambda S: [f'{k:0{N}b}' for k in range(2 ** N)], cols=lambda S: [f'{k}' for k in range(N)],
             color=_cell),
    ],
    watch=[('s', 's', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'f = [[0] * n': '`f[S][i]` 与 `dfs(S, i)` 定义一样；共 `2^n` 行',
        'f[0] = [1] * n': '边界：`S = ∅` 表示全部填完，找到一个合法排列 → `f[0][i] = 1`',
        'u = (1 << n) - 1': '全集 `U = {u}`（二进制 `{u:0{n}b}`）',
        'for s in range': lambda S, B, r: (f'`S = {S.s:0{S.n}b}`：子状态比 S 小，所以 ==S 从小到大==枚举'
                                           if S.get('s') != B.get('s') else '所有 S 都算完了，下面求各起点之和'),
        'for i in range(n):': lambda S, B, r: (
            ('`i` 枚举完了' if S.get('i') == B.get('i') and S.get('s') == B.get('s') else
             f'`i = {S.i}`：它在 S 里 → 它是还没填的数，不能当"上一个数"，跳过' if S.s >> S.i & 1 else
             f'枚举上一个数的下标 `i = {S.i}`') if S.get('_line') == 14 else
            ('起点枚举完了' if S.get('i') == B.get('i') and S.get('ans') == B.get('ans') else f'第一个数选 `i = {S.i}`')),
        'if s >> j & 1 and': _cap_if,
        'f[s][i] += f[s ^': '`f[{s:0{n}b}][{i}] += f[{s ^ (1 << j):0{n}b}][{j}]` → =={f[s][i]}==（下一个填 `nums[{j}]`）',
        'ans += f[u': '第一个数选下标 `{i}`：`ans += f[{u ^ (1 << i):0{n}b}][{i}]` → =={ans}==',
        'cnt[x] += 1': '数字 `{x}` 出现了 `{cnt[x]}` 次',
        'ans //= cnt[x]': '去重：`ans //= {cnt[x]}` → =={ans}==（相同数字互换算成了不同排列）',
        'return ans': '去重后的答案 = =={ret}==',
    },
    cards=dict(
        one_liner='状压 DP 数排列，最后除以重复数的阶乘',
        complexity='时间 `O(n^2 · 2^n)`，空间 `O(n · 2^n)`',
        problem=['相邻两数之和都是==完全平方数==的数组叫平方数组',
                 '给定 `nums`，返回其中有多少种不同的排列是平方数组',
                 '示例：`nums = [1,17,8]` → `2`；`[2,2,2]` → `1`（本视频用 `[1,8,1]` 演示去重）'],
        quote='枚举 S 中的下标 j，如果 nums[i]+nums[j] 是完全平方数，那么可以选 nums[j]。……本题 nums 可能有重复的元素，我们还需要去重。',
        quote_src='—— 灵茶山艾府题解（二、状态定义与状态转移方程）',
        idea=['`dfs(S, i)`：剩余可选下标集合 `S`、上一个数下标 `i` 时的合法排列数',
              '`f[S][i] = Σ f[S \\ {j}][j]`，`j ∈ S` 且 `nums[i]+nums[j]` 是完全平方数',
              '按下标算排列会把相同数字当成不同的，最后除以每种数出现次数的阶乘'],
        summary=['时间 `O(n^2 2^n)` = 状态 `O(n 2^n)` × 转移 `O(n)`',
                 '易错：`i` 不能在 `S` 中；`ans //= cnt[x]` 依次除 1、2、3 才是除 `3!`',
                 '题解主推是 `@cache` 记忆化搜索，递推是它的 1:1 翻译，这里演示递推',
                 '同类题：2741 特别的排列（把平方换成倍数）'],
    ),
)
