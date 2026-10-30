def _cand(S, B, ret):
    j, pile, f = S.j, S.pile, B.f
    n = len(pile)
    parts = [f'`f[{j - w - 1}]+{pile[w]}`={f[j - w - 1] + pile[w]}' for w in range(min(n, j))]
    return f'容量 `{j}`：不选这栈保留 `f[{j}]={f[j]}`；取 w+1 个：' + '，'.join(parts) + f' → `f[{j}]` 更新为 =={S.f[j]}=='


CONFIG = dict(
    num=2218, title='从栈中取出 K 个硬币的最大面值和', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='分组背包（空间优化）',
    tags=['灵神题单', '动态规划', '难度分 2158'],
    code='''
class Solution:
    def maxValueOfCoins(self, piles: List[List[int]], k: int) -> int:
        f = [0] * (k + 1)
        sum_n = 0
        for pile in piles:
            n = len(pile)
            for i in range(1, n):
                pile[i] += pile[i - 1]  # 提前计算 pile 的前缀和
            sum_n = min(sum_n + n, k)
            for j in range(sum_n, 0, -1):  # 优化：j 从前 i 个栈的大小之和开始枚举
                # w 从 0 开始，物品体积为 w+1
                f[j] = max(f[j], max(f[j - w - 1] + pile[w] for w in range(min(n, j))))
        return f[k]
''',
    call='Solution().maxValueOfCoins([[1,100,3],[7,8,9],[5,2]], 4)',
    expect=116,
    views=[
        dict(type='text', fn=lambda S: ('当前栈前缀和：' + ', '.join(f'取{i+1}个={v}' for i, v in enumerate(S['pile']))) if 'pile' in S else '每栈只能取顶部前缀；前缀和后每栈 = 一组物品，至多选一个', size=24, h=60),
        dict(type='text', fn=lambda S: f"piles（前缀和就地改写）= {S['piles']}", size=22, h=50),
        dict(type='array', var='f', label='f[j]：取 j 枚的最大面值', h=230, pointers={'j': 'blue'},
             color=lambda S, i, v: 'yellow' if S.get('j') == i and S.get('_line') in (11,) else None),
    ],
    watch=['k', 'sum_n', 'n', 'j', ('f[k]', 'f[k]', 'green')],
    captions={
        'f = [0] * (k + 1)': '`f[j]` 表示取 `j` 枚硬币能得到的最大面值和，初始全 0',
        'pile[i] += pile[i - 1]': '`pile[{i}]` 变成前缀和 `{pile[i]}`：从栈顶连取 {i+1} 个的总面值',
        'sum_n = min': '前面的栈一共最多 `{sum_n}` 枚，比它大的 `j` 凑不出来 → 上界 `sum_n = {sum_n}`',
        'for j in range': '倒序枚举容量 `j`，这样 `f[j - w - 1]` 还是上一个栈的旧值（和 0-1 背包一样）',
        'f[j] = max': _cand,
        'return f[k]': '恰好取 `{k}` 枚硬币，最大面值和 ==`{f[k]}`==',
    },
    cards=dict(
        one_liner='每个栈取一个前缀：前缀和当物品，分组背包',
        complexity='时间 `O(Lk)`，空间 `O(k)`',
        problem=['`n` 个硬币栈，每次从某个栈顶取一枚，恰好取 `k` 枚',
                 '求钱包里面值之和最大是多少',
                 '示例：`[[1,100,3],[7,8,9]], k=2` → `101`；视频用 `[[1,100,3],[7,8,9],[5,2]], k=4`'],
        quote='对每个栈求前缀和 s，其中 s[w] 表示一个体积为 w+1，价值为 s[w] 的物品。问题转化成：从 n 个物品组中选物品，每组至多选一个物品（可以不选）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['栈只能从顶取，所以一个栈里选的一定是==前缀==', '前缀和 = 价值，取的个数 = 体积，每栈至多选一个 → ==分组背包==',
              '去掉第一维，`j` 倒序枚举；`j` 只从前面栈大小之和 `sum_n` 开始，省时间'],
        summary=['时间 `O(Lk)`，`L` 为所有栈大小之和；空间 `O(k)`',
                 '易错：`j` 必须倒序，否则同一栈会被选多次',
                 '`w` 从 0 开始，体积是 `w+1`；`range(min(n, j))` 防止越界',
                 '灵神还给了记忆化搜索和 1:1 递推两种写法，本视频演示空间优化版'],
    ),
)
