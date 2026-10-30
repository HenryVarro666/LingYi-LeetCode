CONFIG = dict(
    num=3825, title='按位与结果非零的最长上升子序列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='枚举比特位 + LIS 二分',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1846'],
    code='''
class Solution:
    def longestSubsequence(self, nums: List[int]) -> int:
        ans = 0
        w = max(nums).bit_length()
        for i in range(w):
            bit = 1 << i
            # 300. 最长递增子序列
            f = []
            for x in nums:
                if x & bit == 0:  # x 二进制的第 i 位是 0
                    continue
                j = bisect_left(f, x)
                if j < len(f):
                    f[j] = x
                else:
                    f.append(x)
            ans = max(ans, len(f))
        return ans
''',
    call='Solution().longestSubsequence([2,3,6,1,5,4])',
    expect=3,
    views=[
        dict(type='text', size=26, h=60, fn=lambda S: (f"只留二进制第 `{S['i']}` 位是 1 的数（灰色 = 被排除）" if 'bit' in S else '枚举 AND 结果里为 1 的那一位')),
        dict(type='array', var='nums', label='nums', h=190, cell=96,
             dim=lambda S, i, v: 'bit' in S and v & S['bit'] == 0,
             color=lambda S, i, v: 'yellow' if 'x' in S and 'bit' in S and v == S['x'] and S.get('_line') in (10, 11, 12, 13, 14, 15) and v & S['bit'] else None),
        dict(type='array', var='f', label='f（耐心排序：f[j] = 长 j+1 的递增子序列的最小结尾）', h=190, cell=96,
             color=lambda S, i, v: 'green' if i == S.get('j') else None),
    ],
    watch=[('i（比特位）', 'i', 'blue'), 'bit', 'x', 'j', ('ans', 'ans', 'green')],
    captions={
        'w = max': '最大数 `{max(nums)}` 的二进制长 `w = {w}`：只需枚举低 `{w}` 位',
        'bit = 1': '这一轮要求：子序列所有数的第 `{i}` 位都是 1，掩码 `bit = {bit}`',
        'f = []': '每个比特位重新开始：对筛出来的数做一遍 LIS',
        'for x in nums': '看 `x = {x}`',
        'if x & bit == 0': lambda S, B, r: (f"`{S.x} & {S.bit} = {S.x & S.bit}`：第 {S.i} 位是 0 → ==这个数不能选==，跳过" if S.x & S.bit == 0 else f"`{S.x} & {S.bit} = {S.x & S.bit}`：第 {S.i} 位是 1 → 可以参与 LIS"),
        'continue': '跳过，不放进 `f`',
        'j = bisect_left': '二分找 `f` 里第一个 `>= {x}` 的位置：`j = {j}`（严格递增，所以用 bisect_left）',
        'if j < len': lambda S, B, r: (f"`j = {S.j} < {len(S.f)}`：`{S.x}` 能把 f[{S.j}] 变小 → ==替换==" if S.j < len(S.f) else f"`j = {S.j}` 等于长度：`{S.x}` 比所有结尾都大 → ==接在后面=="),
        'f[j] = x': '`f[{j}] = {x}`：同长度的子序列，结尾越小越好，以后更容易接上',
        'f.append(x)': '`f` 变长一位：LIS 长度 = `{len(f)}`',
        'ans = max': '这一位的 LIS 长 `{len(f)}`，`ans = max({B.ans}, {len(f)}) = {ans}`',
        'return ans': '所有比特位里最长的是 `{ans}`',
    },
    cards=dict(
        one_liner='AND 非零 = 某一位全是 1：枚举这一位，再做 LIS',
        complexity='时间 `O(n log n log U)`，空间 `O(n)`',
        problem=['求 `nums` 里「按位 AND 结果非零」的最长严格递增子序列的长度',
                 '示例：`[5,4,7]` → `2`（`5 AND 7 = 5`）',
                 '本视频：`[2,3,6,1,5,4]` → `3`'],
        quote='题目要求子序列的 AND 结果非零，也就是说，AND 结果的某个比特位一定是 1。枚举这个比特位。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 AND 结果里为 1 的那一位 `i`：子序列里每个数的第 `i` 位都必须是 1',
              '所以只留第 `i` 位是 1 的数，变成一道普通的 ==300. 最长递增子序列==',
              '`n` 到 `10^5`，LIS 要用「`bisect_left` + 维护最小结尾」的二分写法'],
        summary=['时间 `O(n log n log U)`，`U = max(nums)`，空间 `O(n)`',
                 '严格递增 → 用 `bisect_left`；允许相等才用 `bisect_right`',
                 '每一位都要重新清空 `f`',
                 '也可以只枚举所有元素 OR 里为 1 的位'],
    ),
)
