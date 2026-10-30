NUMS = [1, 0, 1, 0, 0, 1]


def _wl(S):
    if 'now' not in S:
        return None
    i = S.get('index')
    return 0 if i is None else i - S['s'] + 1


def _wr(S):
    if 'now' not in S:
        return None
    i = S.get('index')
    return S['s'] - 1 if i is None else i


CONFIG = dict(
    num=2134, title='最少交换次数来组合所有的 1 II', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='数组拼接 · 定长滑窗',
    tags=['灵神题单·滑动窗口与双指针', '难度分 1748'],
    code='''
class Solution(object):
    def minSwaps(self, nums):

        n = len(nums)
        s = sum(nums)
        nums.extend(nums)

        now = sum(nums[:s])
        res = s - now
        for index in range(s, n - 1 + s):
            now += nums[index] - nums[index - s]
            res = min(res, s - now)

        return res
''',
    call=f'Solution().minSwaps({NUMS!r})',
    expect=1,
    views=[
        dict(type='array', var='nums', label='nums（已拼接成两遍；框 = 长为 s 的窗口）', pointers={'index': 'blue'},
             window=(_wl, _wr), cell=76, h=230,
             color=lambda S, i, v: 'green' if v == 1 else None),
        dict(type='text', h=100, size=30,
             fn=lambda S: (f"窗口里 `{S['now']}` 个 1，有 `{S['s'] - S['now']}` 个 0 要换；目前最少 `{S['res']}` 次" if 'res' in S
                           else '窗口里的 0 越少，交换越少')),
    ],
    watch=[('s', 's', 'orange'), ('index', 'index', 'blue'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'n = len(nums)': '`n = {n}` 是原数组长度',
        's = sum(nums)': '`s = {s}`：共 {s} 个 1，要聚进一个长为 `s` 的区间',
        'nums.extend(nums)': '把数组复制拼在末尾，==环形变成普通数组==：`{nums}`',
        'now = sum(nums[:s])': '第一个窗口 `nums[:{s}]` 里有 `now = {now}` 个 1',
        'res = s - now': '这个窗口有 `{s} − {now} = {res}` 个 0，要换 `{res}` 次',
        'for index in range': lambda S, B, ret: (f'窗口右端新元素 `nums[{S.index}] = {S.nums[S.index]}`' if 'index' not in B or S.index != B.index else '窗口都扫完了'),
        'now += nums[index]': '加进 `nums[{index}] = {nums[index]}`，减去 `nums[{index - s}] = {nums[index - s]}` → `now = {now}`',
        'res = min': '`res = min({B.res}, {s} − {now}) = {res}`：0 越少换得越少',
        'return res': '最少交换 `{res}` 次',
    },
    cards=dict(
        one_liner='所有的 1 聚进长为 s 的区间，区间里 0 越少越好',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['环形二进制数组，交换任意两个位置，把所有 `1` 聚到一起',
                 '求最少交换次数',
                 f'本视频：`nums = {NUMS}` → `1`'],
        quote='设数组中所有1的数量为k，那么最终所有的1会被聚集到一个长度为k的区间中，也就是说需要找到一个长度为k的区间，其中0的数量尽量少。',
        quote_src='—— yiduobo 题解原文',
        idea=['典型的定长滑动窗口，窗口里 0 的个数 = `s − now`',
              '环形的处理：这里选==把数组复制一份拼在末尾==',
              '窗口右移：加进新元素，减去离开的元素'],
        summary=['时间 `O(n)`，空间 `O(n)`（多了一份拷贝）',
                 '环形还可以不拷贝，用下标对 `n` 取模',
                 '`range(s, n - 1 + s)` 保证窗口起点不超过 `n - 1`',
                 '若数组里没有 1，`s = 0`，窗口为空，返回 0；这里也能正常处理',
                 '注意 `nums.extend` 会修改传入的数组'],
    ),
)
