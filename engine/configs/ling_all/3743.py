def _arr(S):
    return S['prices'] if 'prices' in S else S['nums']


def _cur(S):
    if 'prices' in S and 'p' in S and S['p'] in S['prices']:
        return S['prices'].index(S['p'])
    return None


CONFIG = dict(
    num=3743, title='循环划分的最大得分', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='断环成链 + 买卖股票状态机',
    tags=['状态机 DP', '难度分 3125'],
    code='''
# 手写 max 更快
fmax = lambda a, b: b if b > a else a

class Solution:
    # 3573. 买卖股票的最佳时机 V
    def maximumProfit(self, prices: List[int], k: int) -> int:
        f = [[-inf] * 3 for _ in range(k + 2)]
        for j in range(1, k + 2):
            f[j][0] = 0
        for p in prices:
            for j in range(k + 1, 0, -1):
                f[j][0] = fmax(f[j][0], fmax(f[j][1] + p, f[j][2] - p))
                f[j][1] = fmax(f[j][1], f[j - 1][0] - p)
                f[j][2] = fmax(f[j][2], f[j - 1][0] + p)
        return f[-1][0]

    def maximumScore(self, nums: List[int], k: int) -> int:
        max_i = nums.index(max(nums))
        ans1 = self.maximumProfit(nums[max_i:] + nums[:max_i], k)  # nums[max_i] 是第一个数
        ans2 = self.maximumProfit(nums[max_i + 1:] + nums[:max_i + 1], k)  # nums[max_i] 是最后一个数
        return fmax(ans1, ans2)
''',
    call='Solution().maximumScore([2, 5, 1], 1)',
    expect=4,
    skip=['for j in range(1, k + 2)', 'f[j][0] = 0', 'for j in range(k + 1, 0, -1)', 'f = [[-inf]', 'for p in prices'],
    max_steps=50,
    views=[
        dict(type='array', var=_arr, label='当前处理的数组（断环后的链）', h=170, cell=90,
             pointers={'_p': 'blue'} if False else {},
             color=lambda S, i, v: 'blue' if i == _cur(S) else None),
        dict(type='table', var='f', label='f[j][0/1/2]：最多 j-1 段，0 空闲 / 1 持最小值 / 2 持最大值',
             h=330, cell=96, cols=['空闲', '持小', '持大'],
             rows=lambda S: [f'j={j}' for j in range(len(S['f']))] if 'f' in S and isinstance(S['f'], list) and S['f'] and isinstance(S['f'][0], list) else []),
    ],
    watch=[('max_i', 'max_i', 'orange'), ('p', 'p', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'purple'), ('ans1', 'ans1', 'green'), ('ans2', 'ans2', 'green')],
    captions={
        'max_i = nums.index': '找最大值的下标 `max_i = {max_i}`（值 `{nums[max_i]}`）：==最优划分里它一定在某段的最左或最右==，所以环可以在它旁边断开',
        'ans1 = ': '在 `max_i` 左边断开：最大值排第一个，得到链 `nums[max_i:] + nums[:max_i]`，交给股票 DP',
        'ans2 = ': '在 `max_i` 右边断开：最大值排最后一个，再算一遍链上的最大得分',
        'f[j][0] = fmax(f[j][0]': '空闲态：要么保持，要么平仓 —— 持最小值则卖出 `+{p}`，持最大值则还券 `-{p}`；`f[{j}][0]` = {f[j][0]}',
        'f[j][1] = fmax': '把 `{p}` 当作子数组的最小值（低买）：从 `j-1` 段的空闲态扣掉 `{p}`；`f[{j}][1]` = {f[j][1]}',
        'f[j][2] = fmax': '把 `{p}` 当作子数组的最大值（高借）：从 `j-1` 段的空闲态加上 `{p}`；`f[{j}][2]` = {f[j][2]}',
        'return f[-1][0]': '至多 k 段的最大得分 `{ret}`（`j` 倒序遍历，所以一维滚动安全）',
        'return fmax(ans1, ans2)': '两种断法取较大：`max({ans1}, {ans2})` = =={ret}==',
    },
    cards=dict(
        one_liner='最大值贴边断环，再套股票买卖状态机',
        complexity='时间 `O(nk)`，空间 `O(k)`',
        problem=['循环数组 `nums`，划分成==最多 k 段==连续子数组（可环绕）',
                 '每段得分 = 最大值 − 最小值，求总得分最大值',
                 '示例：`[1,2,3,3]`，`k=2` → `3`（`[2,3]` + `[3,1]`）',
                 '本视频：`[2,5,1]`，`k=1` → `4`'],
        quote='所以一定存在一个最优划分方案，其中 M 在某个子数组的最左边或者最右边。换句话说，我们可以把环形数组在 (i-1,i) 处断开，或者在 (i,i+1) 处断开，转化成非环形的问题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最大值 `M` 所在子数组：把多余元素分给邻居不会更差 → `M` 必在段端',
              '于是在 `M` 前或后断环，两种结果取最大',
              '一段的极差 = 低买高卖 或 高借低还；至多 k 段 = 至多 k 次交易，即 3573 题'],
        summary=['时间 `O(nk)`，空间 `O(k)`',
                 '断环两次：`M` 排第一个、`M` 排最后一个，缺一不可',
                 '`j` 要倒序遍历，否则 `f[j-1]` 已被本轮改写',
                 '`f[j][0]` 里 `j` 从 1 起，所以数组开 `k+2` 行，答案取 `f[-1][0]`',
                 '最大值有多个时任取一个即可'],
    ),
)
