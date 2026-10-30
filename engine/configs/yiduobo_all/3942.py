CONFIG = dict(
    num=3942, title='排序排列的最少操作数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='定位 0 · 检测两段 ±1 连续', tags=['灵神题单', '难度分 1855'],
    code='''
class Solution(object):
    def minOperations(self, nums):
        
        n = len(nums)
        if n == 1:
            return 0
        
        p = -1
        for index in range(n):
            if nums[index] == 0:
                p = index
                break

        if nums[(p - 1 + n) % n] == n - 1:
            delta = 1
        elif nums[(p + 1) % n] == n - 1:
            delta = -1
        else:
            return -1

        if delta == 1:
            offset = 0
        else:
            offset = 1

        for index in range(p - 1 + offset):
            if nums[index] + delta != nums[index + 1]:
                return -1
        
        for index in range(p + offset, n - 1):
            if nums[index] + delta != nums[index + 1]:
                return -1

        return min(p + 1 - delta, n - p + 1 + delta)
''',
    call='Solution().minOperations([1,0,4,3,2])',
    expect=3,
    skip=['for index'],
    views=[
        dict(type='array', var='nums', pointers={'p': 'pink', 'index': 'blue'}, h=330, cell=100),
        dict(type='text', fn=lambda S: ('0 的位置 `p = %d`，方向 `delta = %d`（+1 递增，-1 递减），第一段长度 `p+offset`' % (S['p'], S['delta']) if 'offset' in S
                                        else '0 的位置 `p = %d`，方向 `delta = %d`（+1 递增，-1 递减）' % (S['p'], S['delta']) if 'delta' in S
                                        else '先找 `0` 的位置，再看它左边还是右边挨着 `n-1`' if 'p' not in S or S['p'] < 0 else '0 的位置 `p = %d`' % S['p']), size=26, h=120),
    ],
    watch=['n', ('p', 'p', 'pink'), ('delta', 'delta', 'yellow'), ('offset', 'offset', 'cyan'), ('index', 'index', 'blue')],
    captions={
        'n = len': '`n = {n}`',
        'if n == 1': '`n = {n}`，不是只有 1 个元素的特例，继续',
        'p = -1': '`p` 用来记录 `0` 的下标',
        'if nums[index] == 0': lambda S, B, r: (f'`nums[{S.index}] = 0` → 找到了' if S.nums[S.index] == 0 else f'`nums[{S.index}] = {S.nums[S.index]}` 不是 0'),
        'p = index': '`0` 在下标 `p = {p}`',
        'break': '找到就停',
        'if nums[(p - 1 + n) % n] == n - 1': lambda S, B, r: (f'0 左边（环形）是 `{S.nums[(S.p - 1 + S.n) % S.n]}` = n-1：整体按 +1 递增（旋转过的）' if S.nums[(S.p - 1 + S.n) % S.n] == S.n - 1
                                                                else f'0 左边是 `{S.nums[(S.p - 1 + S.n) % S.n]}`，不是 n-1，看右边'),
        'elif nums[(p + 1) % n] == n - 1': lambda S, B, r: (f'0 右边（环形）是 `{S.nums[(S.p + 1) % S.n]}` = n-1：整体按 -1 递减（旋转过的）' if S.nums[(S.p + 1) % S.n] == S.n - 1
                                                              else '0 两边都不是 n-1 → 不可能排好序'),
        'delta = 1': '`delta = 1`：期望相邻差 +1',
        'delta = -1': '`delta = -1`：期望相邻差 -1',
        'return -1': '检测失败：不是两段连续的环 → 返回 `-1`',
        'if delta == 1': '`delta = {delta}`',
        'offset = 0': '递增时 0 属于后一段，第一段长 `p`：`offset = 0`',
        'offset = 1': '递减时 0 属于前一段，第一段长 `p+1`：`offset = 1`',
        'if nums[index] + delta != nums[index + 1]': lambda S, B, r: (('第一段：' if S.index < S.p + S.offset else '第二段：') + f'`{S.nums[S.index]} + ({S.delta})` = `{S.nums[S.index] + S.delta}`，下一个是 `{S.nums[S.index + 1]}`：'
                                                                      + ('相等，连续 ✓' if S.nums[S.index] + S.delta == S.nums[S.index + 1] else '不相等 → 不行')),
        'return min': '左旋方案 `p + 1 - delta` = `{p + 1 - delta}`；反转方案 `n - p + 1 + delta` = `{n - p + 1 + delta}` → 取最小 =={min(p + 1 - delta, n - p + 1 + delta)}==',
    },
    cards=dict(
        one_liner='找到 0，看它挨着谁，判断是不是两段连续的环',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`nums` 是 `0` 到 `n-1` 的排列，可以「整体反转」或「左旋一位」',
                 '求排成递增的最少操作数，做不到返回 `-1`',
                 '本视频示例：`[1,0,4,3,2]` → `3`'],
        quote='如果将nums视为首尾相连，那么题目中的两种操作都不会影响到数组元素间的相邻关系。',
        quote_src='—— yiduobo 题解原文',
        idea=['先找 `0` 的下标 `p`；`0` 左边（环形）是 `n-1` → 递增环，右边是 `n-1` → 递减环',
              '用 `delta = ±1` 统一两种情况：检查两段内部相邻差都是 `delta`',
              '递增时第一段长 `p`，递减时 0 属于前一段，所以用 `offset` 调整',
              '答案是两种做法的较小者：`min(p+1-delta, n-p+1+delta)`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`[0, 1]` 这样的数组要当作递增，所以先判断左边再判断右边',
                 '易错：递减时 0 属于第一段，第一段长度是 `p+1`，要用 `offset`',
                 '对比灵神：灵神数下降点，yiduobo 先定位 0 再验证 ±1 连续',
                 '原文已是 Python 3 可运行写法，代码无需改动'],
    ),
)
