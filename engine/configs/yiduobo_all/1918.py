CONFIG = dict(
    num=1918, title='第K小的子数组和', difficulty='Medium', category='二分算法',
    author='yiduobo', technique='二分答案 + 滑动窗口计数',
    tags=['灵神题单·滑动窗口与双指针', '灵神题单·二分算法'],
    code='''
class Solution(object):
    def kthSmallestSubarraySum(self, nums, k):
        left = min(nums)
        right = sum(nums)
        n = len(nums)

        while left < right:
            mid = (left + right) // 2
            bound = 0
            now = 0
            while bound < n and now + nums[bound] <= mid:
                now += nums[bound]
                bound += 1

            cnt = bound
            for index, v in enumerate(nums):
                now -= v
                if bound < index:
                    bound = index
                while bound < n and now + nums[bound] <= mid:
                    now += nums[bound]
                    bound += 1
                cnt += bound - index - 1

            if cnt < k:
                left = mid + 1
            else:
                right = mid

        return left
''',
    call='Solution().kthSmallestSubarraySum([2,1,3], 4)',
    expect=3,
    views=[
        dict(type='array', var='nums', h=230, label='nums：蓝 = 当前窗口 [起点, bound)',
             pointers={'bound': 'pink'},
             window=('(index + 1 if 16 <= _line <= 24 else 0)', 'bound - 1'),
             color=lambda S, i, v: 'blue' if 'bound' in S and ((S['index'] + 1 if 16 <= S['_line'] <= 24 else 0) <= i < S['bound']) else None),
        dict(type='text', fn=lambda S: f"二分区间 `[{S['left']}, {S['right']}]`，`mid = {S['mid']}`" if 'mid' in S else f"二分区间 `[{S['left']}, {S['right']}]`" if 'left' in S and 'right' in S else ''),
        dict(type='text', fn=lambda S: (f"循环里：窗口起点是 `index + 1 = {S['index'] + 1}`，`cnt += bound - index - 1` 数的就是以它为左端点的个数" if 16 <= S['_line'] <= 24 else '') if 'index' in S else ''),
        dict(type='text', fn=lambda S: f"窗口和 `now = {S['now']}`，目前 `和 <= mid` 的子数组共 ==`{S['cnt']}`== 个（要和 `k = {S['k']}` 比）" if 'cnt' in S else ''),
    ],
    max_steps=48,
    skip=['n = len(nums)', 'bound += 1'],
    watch=['left', 'right', ('mid', 'mid', 'yellow'), ('now', 'now', 'cyan'), ('bound', 'bound', 'pink'), ('cnt', 'cnt', 'green')],
    captions={
        'left = min(nums)': '答案至少是最小的单个元素：`left = {left}`',
        'right = sum(nums)': '答案至多是整个数组之和：`right = {right}`',
        'mid = ': '猜一个子数组和 `mid = ({B.left} + {B.right}) // 2 = {mid}`，数一数有多少子数组和 `<= mid`',
        'bound = 0': '`bound`：窗口右边界（开区间），先从 0 开始',
        'now = 0': '`now` 是窗口 `nums[index:bound]` 的和',
        'while bound < n and now + nums[bound] <= mid': lambda S, B, r: (
            f'再加 `nums[{S.bound}]` 后和为 `{S.now + S.nums[S.bound]}`，没超过 `mid = {S.mid}` → 窗口还能右扩'
            if (S.bound < S.n and S.now + S.nums[S.bound] <= S.mid)
            else ('`bound` 到头了，不能再扩' if S.bound >= S.n else f'再加 `nums[{S.bound}]` 会变成 `{S.now + S.nums[S.bound]}` > `mid = {S.mid}` → 停下')),
        'now += nums[bound]': '吞进 `nums[{bound}]`：`now = {now}`，`bound` 随后右移一格',
        'bound += 1': '`bound` → {bound}',
        'cnt = bound': '左端点为 0 时，右端点可以取 `0..bound-1`，共 `bound = {bound}` 个子数组和不超过 `mid`',
        'for index, v': '`index = {index}`：这一轮统计以 `index + 1` 为左端点的子数组',
        'now -= v': '窗口左端点右移一格，扔掉 `{v}`：`now = {now}`（现在窗口是 `nums[{index + 1}:bound]`）',
        'if bound < index': lambda S, B, r: ('窗口已空（`bound` 落后了），把 `bound` 拉回 `index`；`now` 暂时是负数，下一步会补回' if S.bound < S.index else '`bound` 不会回退：因为数全是正数，左端点右移后右边界只增不减'),
        'bound = index': '`bound = {bound}`',
        'cnt += bound - index - 1': '以 `{index + 1}` 为左端点：右端点可取 `{index + 1}..{bound - 1}`，共 `{bound} - {index} - 1` = =={bound - index - 1}== 个 → `cnt = {cnt}`',
        'if cnt < k': lambda S, B, r: (f'`cnt = {S.cnt} < k = {S.k}`：和 `<= {S.mid}` 的子数组不够 k 个 → 第 k 小一定更大' if S.cnt < S.k
                                         else f'`cnt = {S.cnt} >= k = {S.k}`：第 k 小的和不会超过 `{S.mid}` → 答案在左半边（含 mid）'),
        'left = mid + 1': '`left = {left}`：舍掉 `<= mid` 的部分',
        'right = mid': '`right = {right}`：`mid` 可能就是答案，所以保留',
        'return left': '`left == right`，第 {k} 小的子数组和 = =={left}==',
    },
    cards=dict(
        one_liner='二分「子数组和」的值，用滑动窗口数有几个不超过它',
        complexity='时间 `O(n log S)`（`S` 为数组总和），空间 `O(1)`',
        problem=['给定正整数数组 `nums` 和 `k`，求所有非空子数组之和里第 `k` 小的',
                 '示例：`[2,1,3], k=4`：子数组和排序为 `1,2,3,3,4,6`，第 4 小是 `3`'],
        quote='通过二分来寻找这个子数组和。对于当前二分到的数组和mid，计算所有子数组中有多少个子数组之和小于等于mid，然后通过这个数目与k的大小对比来调整二分的上下界。',
        quote_src='—— yiduobo 题解',
        idea=['子数组有 `O(n^2)` 个，不能全排序，改二分答案',
              '数都是正数 → 左端点右移，右边界 `bound` 只会右移，一趟滑窗就能数清个数',
              '`cnt < k` 说明 mid 太小；否则答案 `<= mid`'],
        summary=['时间 `O(n log S)`：二分 `log S` 轮，每轮滑窗 `O(n)`',
                 '前提是元素为正数，窗口和才单调，`bound` 才不会回退',
                 '二分写成 `left < right`，`cnt >= k` 时 `right = mid`，避免死循环',
                 '原文为 Python 2 写法，`(left + right) / 2` 是整数除法，已改为 `//`'],
    ),
)
