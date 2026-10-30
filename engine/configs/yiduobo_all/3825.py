CONFIG = dict(
    num=3825, title='按位与结果非零的最长上升子序列', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='枚举二进制位 + 贪心二分 LIS',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1846'],
    code='''
class Solution(object):
    def longestSubsequence(self, nums):
        
        ma = max(nums)
        p2 = [1]
        while p2[-1] < ma:
            p2.append(p2[-1] + p2[-1])
        
        res = 0
        for v in p2:
            f = []
            for x in nums:
                if (x & v) == v:
                    if not f or f[-1] < x:
                        f.append(x)
                    else:
                        left = 0
                        right = len(f) - 1
                        while left < right:
                            mid = (left + right) // 2
                            if f[mid] < x:
                                left = mid + 1
                            else:
                                right = mid
                        f[left] = x
            
            res = max(res, len(f))
        
        return res
''',
    call='Solution().longestSubsequence([2,3,6,1,5,4])',
    expect=3,
    views=[
        dict(type='text', size=26, h=60, fn=lambda S: (f"当前位掩码 `v = {S['v']}`：只看 `x & v == v` 的数" if 'v' in S else '先造出 1,2,4,8… 这些二进制位')),
        dict(type='array', var='nums', label='nums', h=180, cell=96,
             dim=lambda S, i, v: 'v' in S and v & S['v'] != S['v'],
             color=lambda S, i, v: 'yellow' if 'x' in S and 'v' in S and v == S['x'] and v & S['v'] == S['v'] and S.get('_line', 0) >= 14 else None),
        dict(type='array', var='f', label='f（贪心：f[k] = 长 k+1 的上升子序列的最小结尾）', h=180, cell=96,
             pointers={'left': 'blue', 'right': 'pink', 'mid': 'yellow'}),
        dict(type='array', var='p2', label='p2（所有候选二进制位）', h=130, cell=70),
    ],
    watch=['v', 'x', 'left', 'right', 'mid', ('res', 'res', 'green')],
    skip=['ma = max', 'p2 = [1]'],
    captions={
        'p2.append': '`p2` 追加 `{p2[-1]}`：二进制每一位对应一个数 `1 << k`',
        'for v in p2': '这一轮要求子序列所有数都含位 `v = {v}`',
        'f = []': '对筛出的数，用「贪心 + 二分」求最长上升子序列',
        'if (x & v) == v': lambda S, B, r: (f"`{S.x} & {S.v} = {S.x & S.v}` 等于 `v` → 这一位是 1，==留下==" if S.x & S.v == S.v else f"`{S.x} & {S.v} = {S.x & S.v}` 不等于 `v` → 这一位是 0，==跳过=="),
        'if not f or f[-1] < x': lambda S, B, r: (f"`{S.x}` 比 `f` 末尾 `{S.f[-1]}` 大 → 直接接在后面" if S.f and S.f[-1] < S.x else (f"`f` 为空，直接放入" if not S.f else f"`{S.x}` 不比末尾 `{S.f[-1]}` 大 → 要在 f 里找位置替换")),
        'f.append(x)': '`f` 变长：长度 `{len(f)}`',
        'left = 0': '二分找第一个 `>= {x}` 的位置：`left = 0`',
        'right = len': '`right = len(f) - 1 = {right}`：在 `f` 上二分',
        'mid = (left': '`mid = {mid}`，`f[{mid}] = {f[mid]}`',
        'if f[mid] < x': lambda S, B, r: (f"`f[{S.mid}] = {S.f[S.mid]} < {S.x}` → 答案在右边，`left = mid + 1`" if S.f[S.mid] < S.x else f"`f[{S.mid}] = {S.f[S.mid]} >= {S.x}` → 答案在 mid 或左边，`right = mid`"),
        'left = mid + 1': '`left` → {left}',
        'right = mid': '`right` → {right}',
        'f[left] = x': '用 `{x}` 替换 `f[{left}]`：长度相同，结尾更小更好',
        'res = max': '这一位的最长长度 `{len(f)}`，`res = max({B.res}, {len(f)}) = {res}`',
        'return res': '所有位里最长的是 `{res}`',
    },
    cards=dict(
        one_liner='AND 非零，说明某个二进制位上全是 1',
        complexity='时间 `O(n log n log U)`，空间 `O(n)`',
        problem=['在 `nums` 里找按位与结果非零的最长严格递增子序列，返回长度',
                 '`n <= 10^5`，`nums[i] <= 10^9`，二进制不超过 30 位',
                 '本视频：`[2,3,6,1,5,4]` → `3`'],
        quote='子序列中的元素按位与结果非零，说明至少存在一个二进制位，子序列中的所有元素在这个位上都为1。',
        quote_src='—— yiduobo 题解原文',
        idea=['元素不超过 30 位：逐位遍历，把该位为 1 的元素提取出来',
              '对提取出的数组做「贪心 + 二分」的最长上升子序列，更新答案',
              '作者把二分手写在循环里，判断条件用 `(x & v) == v`'],
        summary=['时间 `O(n log n log U)`，空间 `O(n)`',
                 '`f[-1] < x` 才能直接追加：严格递增，相等要替换',
                 '手写二分找第一个 `>= x` 的位置，等价于 `bisect_left`',
                 '原文为 Python 2 风格，但已用 `//`，代码无需改动'],
    ),
)
