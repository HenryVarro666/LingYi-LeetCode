NUMS = [1, 0, 1, 0, 0, 1]


def _wl(S):
    i = S.get('i')
    if i is None:
        return None
    return max(0, i - S['k'] + 1)


CONFIG = dict(
    num=2134, title='最少交换次数来组合所有的 1 II', difficulty='Medium', category='滑动窗口与双指针',
    author='灵茶山艾府', technique='环形定长滑窗 · 窗口内 1 最多',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1748'],
    code='''
class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        k = sum(nums)  # 1 的个数
        if k == 0:  # 没有 1，无需交换
            return 0

        n = len(nums)
        max1 = cnt1 = 0
        for i in range(n + k - 1):
            # 1. 进入窗口
            cnt1 += nums[i % n]
            if i < k - 1:  # 窗口大小不足 k
                continue
            # 2. 更新答案
            max1 = max(max1, cnt1)
            # 3. 离开窗口，为下一个循环做准备
            cnt1 -= nums[i - k + 1]  # 由于我们保证 i < n+k-1，所以 i-k+1 < n，无需取模
        return k - max1
''',
    call=f'Solution().minSwaps({NUMS!r})',
    expect=1,
    views=[
        dict(type='array', var=lambda S: S['nums'] * 2, label='nums 接两遍（下标 ≥ n 就是绕回开头，框 = 长为 k 的窗口）',
             pointers={'i': 'blue'}, window=(_wl, 'i'), cell=76, h=230,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"窗口里 `{S['cnt1']}` 个 1 → 需要换 `{S['k']} − {S['cnt1']} = {S['k'] - S['cnt1']}` 次；目前最多 `{S['max1']}` 个 1"
                           if 'max1' in S else '窗口内的 0 越少，换进来的 1 越少')),
    ],
    watch=[('k', 'k', 'orange'), ('i', 'i', 'blue'), ('cnt1', 'cnt1', 'cyan'), ('max1', 'max1', 'green')],
    captions={
        'k = sum(nums)': '一共 `k = {k}` 个 1，它们最终要挤进一个==长为 k 的窗口==',
        'if k == 0': '`k = {k}`：有 1，继续',
        'n = len(nums)': '`n = {n}`，环形：下标 ≥ n 就取模绕回',
        'max1 = cnt1 = 0': '`cnt1` 窗口里 1 的个数；`max1` 是它的最大值',
        'for i in range': lambda S, B, ret: (f'窗口右端点 `i = {S.i}`（对应 `nums[{S.i % S.n}]`）' if 'i' not in B or S.i != B.i else '所有窗口枚举完（第 n+k−1 个以后和第一个重复）'),
        'cnt1 += nums[i % n]': '`nums[{i % n}] = {nums[i % n]}` 进入窗口 → `cnt1 = {cnt1}`',
        'if i < k - 1': lambda S, B, ret: (f'`i = {S.i} < k − 1 = {S.k - 1}`：窗口还没满 k 个' if S.i < S.k - 1
                                          else f'`i = {S.i} ≥ k − 1`：窗口 `[{S.i - S.k + 1}, {S.i}]` 正好 k 个'),
        'continue': '先继续扩大窗口',
        'max1 = max': '`max1 = max({B.max1}, {cnt1}) = {max1}`：窗口里 1 越多，要换的 0 越少',
        'cnt1 -= nums': '`nums[{i - k + 1}] = {nums[i - k + 1]}` 离开窗口 → `cnt1 = {cnt1}`',
        'return k - max1': '窗口里的 0 最少 `{k} − {max1} = {k - max1}` 个，每个 0 换一次 → ==答案 {k - max1}==',
    },
    cards=dict(
        one_liner='k 个 1 要挤进长为 k 的窗口：窗口里有几个 0 就换几次',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['环形二进制数组（首尾相邻），交换任意两个位置的值',
                 '求把所有 `1` 聚到一起的==最少交换次数==',
                 f'本视频：`nums = {NUMS}` → `1`'],
        quote='题目让我们在环形数组 nums 中找到一个长为 k 的子数组，把这个子数组变成全 1 子数组。子数组中有多少个 0，就需要交换多少次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`k` = 1 的总数；目标窗口长度也是 `k`',
              '求 0 的最小个数 ⇔ 求 1 的==最大个数==（统计 1 更方便），答案 `k − max1`',
              '环形：窗口右端点枚举到 `n+k−2`，下标取模 `i % n`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：`k == 0` 要特判，否则窗口大小为 0',
                 '`range(n + k - 1)`：再往后的窗口与第一个窗口重复',
                 '离开窗口的下标 `i-k+1 < n`，所以不用取模'],
    ),
)
