CONFIG = dict(
    num=1671, title='得到山形数组的最少删除次数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='前后缀分解 + 两遍 LIS',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1913'],
    code='''
class Solution:
    def minimumMountainRemovals(self, nums: List[int]) -> int:
        n = len(nums)
        suf = [0] * n
        g = []
        for i in range(n - 1, 0, -1):
            x = nums[i]
            j = bisect_left(g, x)
            if j == len(g):
                g.append(x)
            else:
                g[j] = x
            suf[i] = j + 1  # 从 nums[i] 开始的最长严格递减子序列的长度

        mx = 0  # 最长山形子序列的长度
        g = []
        for i, x in enumerate(nums):
            j = bisect_left(g, x)
            if j == len(g):
                g.append(x)
            else:
                g[j] = x
            pre = j + 1  # 在 nums[i] 结束的最长严格递增子序列的长度
            if pre >= 2 and suf[i] >= 2:
                mx = max(mx, pre + suf[i] - 1)  # 减去重复的 nums[i]
        return n - mx
''',
    call='Solution().minimumMountainRemovals([1,3,2,4,1])',
    expect=1,
    skip=['x = nums[i]', 'n = len', 'suf = [0]', 'g = []', 'mx = 0'],
    max_steps=110,
    views=[
        dict(type='text', size=25, h=60, fn=lambda S: (
            f"第二遍（左→右）：`nums[{S['i']}]` 当峰顶，山长 = `pre + suf[{S['i']}] - 1`" if 'pre' in S and S.get('_line', 0) >= 20 else
            ('第二遍：从左到右做 LIS，得到 `pre`，并枚举峰顶' if 'mx' in S else
             ('第一遍：从右往左做 LIS，得到 `suf[i]`（i 开头的最长递减子序列）' if 'i' in S else '山形 = 递增 + 递减：枚举峰顶')))),
        dict(type='array', var='nums', label='nums', h=170, cell=88, pointers={'i': 'blue'},
             color=lambda S, k, v: 'yellow' if k == S.get('i') else None),
        dict(type='array', var='g', label='g（LIS 的最小结尾）', h=150, cell=88,
             color=lambda S, k, v: 'green' if k == S.get('j') else None),
        dict(type='array', var='suf', label='suf（从 i 开始的最长递减长度）', h=150, cell=88,
             color=lambda S, k, v: 'cyan' if k == S.get('i') and v else None),
    ],
    watch=['i', 'x', 'j', 'pre', ('mx', 'mx', 'green')],
    captions={
        'for i in range(n - 1': lambda S, B, r: ('第一遍结束，`suf` 已算好（`suf[0]` 不用，峰顶不能在两端）' if 'i' in B and B.i == 1 else f'第一遍：从右往左，`nums[{S.i}] = {S.nums[S.i]}`；反过来看，递减子序列就是递增子序列' if 'i' in S else '第一遍：从右往左遍历。反过来看，递减子序列就是递增子序列'),
        'g.append(x)': '`g` 追加 `{x}`：LIS 变长',
        'g[j] = x': '`g[{j}] = {x}`',
        'j = bisect_left': '在 `g` 里二分找第一个 `>= {x}` 的位置 `j = {j}`',
        'if j == len(g)': lambda S, B, r: (f"`j = {S.j}` 等于长度：`{S.x}` 比所有结尾都大 → 追加" if S.j == len(S.g) else f"`j = {S.j}` 在 `g` 内：`{S.x}` 替换 `g[{S.j}]`，结尾更小更好"),
        'suf[i] = j + 1': '`suf[{i}] = j + 1 = {j+1}`：从 `nums[{i}]` 开始最长严格递减子序列长 `{j+1}`',
        'for i, x in enumerate': lambda S, B, r: ('第二遍遍历结束，答案 = `n - mx`' if 'i' in B and 'mx' in B and B.i == S.i and 'pre' in B else f'第二遍：从左往右，`nums[{S.i}] = {S.x}` 当作峰顶候选'),
        'pre = j + 1': '`pre = j + 1 = {j+1}`：以 `nums[{i}]` 结尾的最长严格递增子序列长',
        'if pre >= 2': lambda S, B, r: (f"`pre = {S.pre}`，`suf[{S.i}] = {S.suf[S.i]}`：两边都 >= 2 → 峰顶左右都有数，==是有效山峰==" if S.pre >= 2 and S.suf[S.i] >= 2 else f"`pre = {S.pre}`，`suf[{S.i}] = {S.suf[S.i]}`：有一边只有它自己 → ==不能当峰顶=="),
        'mx = max': '山长 `{pre} + {suf[i]} - 1 = {pre + suf[i] - 1}`（峰顶算了两次要减 1），`mx = {mx}`',
        'return n - mx': '最长山形子序列 `{mx}`，删除 `{n} - {mx} = {n - mx}` 个',
    },
    cards=dict(
        one_liner='删得最少 = 留下的山形子序列最长：枚举峰顶，前后缀各做一遍 LIS',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['删除最少的数，使数组变成「先严格递增再严格递减」的山形，峰顶左右都得有数',
                 '示例：`[2,1,1,5,6,2,3,1]` → `3`',
                 '本视频：`[1,3,2,4,1]` → `1`（删掉 `2`，留下 `[1,3,4,1]`）'],
        quote='山形子序列可以看成一个严格递增子序列，拼接一个严格递减子序列。注意本题要求峰顶左右两侧必须有数字，所以在 pre[i] >= 2 且 suf[i] >= 2 的情况下……',
        quote_src='—— 灵茶山艾府题解',
        idea=['`pre[i]`：以 `nums[i]` 结尾的最长严格递增子序列；`suf[i]`：以 `nums[i]` 开头的最长严格递减子序列',
              '以 `nums[i]` 为峰顶：山长 `pre[i] + suf[i] - 1`，重复的峰顶减一次',
              '`suf` 从右往左做 LIS，`pre` 的计算和取最大值合并，省一个数组'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '易错：`pre >= 2` 且 `suf >= 2`，否则山峰一侧为空，不合法',
                 '前后缀分解：先预处理一侧，再扫另一侧边算边更新答案',
                 '题解还给了更简洁的写法：把 LIS 封成函数 `lis`，对 `nums` 和 `nums[::-1]` 各调用一次'],
    ),
)
