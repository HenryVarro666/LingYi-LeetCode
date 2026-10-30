def _txt(S):
    if 'cnt' in S and 'i' in S and S.get('_line', 0) in (10, 11) and 'l' in S:
        l, r, i, k = S['l'], S['r'], S['i'], S['k']
        return (f"最小值 `nums[{i}]={S['nums'][i]}`，边界开区间 `({l}, {r})`：含它且长度 ≤ {k} 的子数组 ==`{S['cnt']}`== 个")
    if 'st' in S and 'r' in S:
        return f"枚举右边界 `r = {S['r']}`，栈内维护单调递增的下标（栈底 -1 是哨兵）"
    return '先算最小值的贡献；再把数组取反，复用同一份代码算最大值的贡献'


CONFIG = dict(
    num=3430, title='最多 K 个元素的子数组的最值之和', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='单调栈 + 容斥计数（贡献法）',
    tags=['难度分 2645'],
    code='''
class Solution:
    def sumSubarrayMins(self, nums: List[int], k: int) -> int:
        count = lambda m: (m * 2 - k + 1) * k // 2 if m > k else (m + 1) * m // 2
        ans = 0
        st = [-1]
        for r, x in enumerate(nums + [-inf]):
            while len(st) > 1 and nums[st[-1]] >= x:
                i = st.pop()
                l = st[-1]
                cnt = count(r - l - 1) - count(i - l - 1) - count(r - i - 1)
                ans += nums[i] * cnt
            st.append(r)
        return ans

    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        ans = self.sumSubarrayMins(nums, k)
        ans -= self.sumSubarrayMins([-x for x in nums], k)
        return ans
''',
    call='Solution().minMaxSubarraySum([3,1,2], 2)',
    expect=19,
    skip=['count = lambda'],
    max_steps=90,
    views=[
        dict(type='text', h=44, fn=_txt),
        dict(type='array', var='nums', h=150, pointers={'r': 'blue', 'i': 'pink'},
             window=(lambda S: S['l'] + 1 if S.get('_line') in (9, 10, 11) and 'l' in S else None,
                     lambda S: S['r'] - 1 if S.get('_line') in (9, 10, 11) and 'r' in S else None),
             color=lambda S, j, v: 'pink' if S.get('_line') in (8, 9, 10, 11) and S.get('i') == j else None),
        dict(type='stack', var='st', h=100, fmt=lambda i: str(i)),
    ],
    watch=['r', 'x', 'i', 'l', ('cnt', 'cnt', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'while len(st) > 1': lambda S, B, ret: (
            f"栈顶 `nums[{S['st'][-1]}]` = {S['nums'][S['st'][-1]]} `>= {S['x']}`：==成立==，它的右边界就是 `r = {S['r']}`，弹出结算"
            if len(S['st']) > 1 and S['nums'][S['st'][-1]] >= S['x'] else
            ('只剩哨兵 -1，不再弹' if len(S['st']) <= 1 else f"栈顶 `nums[{S['st'][-1]}]` = {S['nums'][S['st'][-1]]} 小于 `{S['x']}` → 停止弹栈")),
        'i = st.pop()': '弹出 `i = {i}`：`nums[{i}] = {nums[i]}` 作为最小值，左边界 `l = st[-1]` 是下一个栈顶',
        'l = st[-1]': '左边界 `l = {l}`，右边界 `r = {r}`：开区间 `({l}, {r})` 里 `nums[{i}]` 最小',
        'cnt = count': '容斥：整段 `count({r-l-1})` 减去只在左半 `count({i-l-1})` 和只在右半 `count({r-i-1})` = =={cnt}==',
        'ans += nums[i]': '贡献 = 最小值 `{nums[i]}` × 个数 `{cnt}`，`ans = {ans}`',
        'st.append(r)': '`r = {r}` 入栈',
        13: '这一轮算完，返回 `{ans}`',
        18: '最小值之和 − 取反数组的最小值之和（= 最大值之和）：返回 `{ans}`',
        'ans = self.sumSubarrayMins(nums, k)': '`ans` = 所有长度 ≤ k 的子数组「最小值」之和 = {ans}',
        'ans -= self.sumSubarrayMins': '已得最小值之和 `{ans}`；对取反数组再算一遍，结果是最大值之和的相反数，所以要相减',
    },
    cards=dict(
        one_liner='枚举最小值的贡献；取反数组，同一份代码再算最大值',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['求长度不超过 `k` 的所有子数组中，==最大值 + 最小值==的总和',
                 '示例：`nums=[1,2,3], k=2` → `20`',
                 '视频用 `[3,1,2], k=2` 演示，答案 `19`'],
        quote='包含 x 的长度至多为 k 的子数组个数，等于：开区间 (L,R) 中的所有长度至多为 k 的子数组个数，减去开区间 (L,i) 中的……，减去开区间 (i,R) 中的……',
        quote_src='—— 灵茶山艾府题解 第二种计算方法',
        idea=['单调栈弹出 `i` 时，左右边界 `(l, r)` 就确定了',
              '含 `nums[i]` 的子数组 = 整段 − 只在左半 − 只在右半，每段用 `count(m)` 数「长度 ≤ k」的个数',
              '`m ≤ k` 时是 `m(m+1)/2`；`m > k` 时是 `(2m−k+1)k/2`',
              '最大值把数组取反就行：`ans -= 取反后的最小值和`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：弹栈条件用 `>=`，相等元素只算一次；末尾补 `-inf` 把栈清空',
                 '灵神另一种写法：直接分类讨论左端点，用等差数列求和（题解「第一种」）',
                 '前置题：907 子数组的最小值之和'],
    ),
)
