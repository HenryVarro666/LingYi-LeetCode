NUMS, TARGET = [3, 1, 2, 4], 6

CONFIG = dict(
    num=2915, title='和为目标值的最长子序列的长度', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='恰好装满型 0-1 背包（倒序 + 时间优化）',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1659'],
    code='''
class Solution:
    def lengthOfLongestSubsequence(self, nums: List[int], target: int) -> int:
        f = [0] + [-inf] * target
        s = 0
        for x in nums:
            s = min(s + x, target)
            for j in range(s, x - 1, -1):
                t = f[j - x] + 1
                if t > f[j]:  # 手写 max 效率更高
                    f[j] = t
        return f[-1] if f[-1] > 0 else -1
''',
    call=f'Solution().lengthOfLongestSubsequence({NUMS}, {TARGET})',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前物品 x）', h=170, cell=90,
             color=lambda S, i, v: 'blue' if 'x' in S and v == S['x'] else None),
        dict(type='array', var='f', label='f[j]：和恰好为 j 的子序列最长长度（-inf = 凑不出）', h=230, cell=90,
             pointers={'j': 'pink'},
             color=lambda S, i, v: ('green' if i == S.get('j') and S.get('_line', 0) == 10 else
                                    'cyan' if 'j' in S and 'x' in S and i == S['j'] - S['x'] and S.get('_line', 0) in (8, 9) else None)),
        dict(type='text', h=60, size=26,
             fn=lambda S: (f"f[{S['j']}] = max(f[{S['j']}], f[{S['j']-S['x']}] + 1) = max({S['f'][S['j']]}, {S['f'][S['j']-S['x']]} + 1)"
                           if 'j' in S and 'x' in S and S['j'] >= S['x'] else '`f[j]`：选 `x` 则从 `f[j-x]` 转移，长度 +1')),
    ],
    watch=[('x', 'x', 'blue'), ('s', 's', 'orange'), ('j', 'j', 'pink'), 't', ('f[-1]', 'f[-1]', 'green')],
    skip=['s = 0'],
    max_steps=70,
    captions={
        'f = [0]': '`f[j]` = 和恰好为 `j` 的子序列最长长度：`f[0] = 0`（空序列），其余 `-inf`（还凑不出）',
        
        'for x in nums': lambda S, B, r: (f'物品 `x = {S.x}`：每个数选或不选' if 'x' in S and S.x != B.get('x') or S.get('s') != B.get('s') else '所有数处理完'),
        's = min': '前面所有数之和最多 `{s}`（不超过 target）→ `j` 只需枚举到 `{s}`，后面的 `f` 必是 `-inf`',
        'for j in range': lambda S, B, r: ((f'`j = {S.j}`：==倒序==，保证 `f[{S.j - S.x}]` 还是上一轮的值（每个数只选一次）' if S.j == S.s else f'`j = {S.j}`') if 'j' in S and S.j != B.get('j')
                                          else '这个数处理完，进入下一个数'),
        't = f[j - x]': '选 `x = {x}`：从 `f[{j - x}] = {f[j - x]}` 转移，长度 +1 → `t = {t}`',
        'if t > f[j]': lambda S, B, r: (f'`t = {S.t}` > `f[{S.j}] = {S.f[S.j]}` → 选 `x` 更长，更新' if S.t > S.f[S.j]
                                        else f'`t = {S.t}` ≤ `f[{S.j}] = {S.f[S.j]}` → 不选更好（或 `-inf`），不变'),
        'f[j] = t': '`f[{j}] = {t}`',
        'return': lambda S, B, r: (f'`f[-1] = f[{S.target}] = {S.f[-1]}` > 0 → 答案 `{r}`' if r > 0 else '`f[-1]` 还是 `-inf` → 凑不出，返回 `-1`'),
    },
    cards=dict(
        one_liner='恰好装满的 0-1 背包：f[j] 存最长长度，j 倒序',
        complexity='时间 `O(n·target)`，空间 `O(target)`',
        problem=['给一个正整数数组 `nums` 和 `target`，求和恰好为 `target` 的子序列的==最大长度==',
                 '不存在则返回 `-1`',
                 '示例：`nums = [4,1,3,2,1,5], target = 7` → `4`；本视频用 `[3,1,2,4], target = 6` → `3`'],
        quote='本题是恰好装满型 0-1 背包，……用 -∞ 表示不合法的状态，从而保证 max 不会取到不合法的状态。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, j)` = 前 `i` 个数里和恰为 `j` 的最长子序列：选 / 不选两种',
              '1:1 翻译成递推，再把 `i` 这一维滚掉，`j` ==倒序==枚举',
              '时间优化：前缀和 `s` 之外的 `f[j]` 必为 `-inf`，`j` 只枚举到 `s`'],
        summary=['时间 `O(n·target)`，空间 `O(target)`',
                 '易错：`f` 初始 `f[0] = 0`、其余 `-inf`，别全填 0（0 表示「和为 j 且长度 0」不成立）',
                 '易错：`j` 必须倒序，否则同一个数会被选多次（变成完全背包）',
                 '返回前要判断 `f[-1] > 0`，否则返回 `-1`',
                 '原文还有记忆化搜索、二维递推写法，这里演示最后的时间优化写法'],
    ),
)
