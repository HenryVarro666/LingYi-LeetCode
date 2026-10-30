CONFIG = dict(
    num=2563, title='统计公平数对的数目', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='排序 + 一个左指针、两个右指针',
    tags=['二分算法', '难度分 1721'],
    code='''
class Solution(object):
    def countFairPairs(self, nums, lower, upper):

        nums.sort()
        right_low = right_high = len(nums) - 1
        res = 0
        for left in range(len(nums)):
            while right_low > left and nums[left] + nums[right_low] > lower - 1:
                right_low -= 1
            while right_high > left and nums[left] + nums[right_high] > upper:
                right_high -= 1
            
            if right_high > left:
                res += right_high - left
            if right_low > left:
                res -= right_low - left
        
        return res
''',
    call='Solution().countFairPairs([0,1,7,4,4,5], 3, 6)',
    expect=6,
    views=[
        dict(type='array', var='nums', label='排序后的 nums（蓝 = left，橙 = 对应 upper，粉 = 对应 lower-1）', h=210, cell=90,
             pointers={'left': 'blue', 'right_high': 'orange', 'right_low': 'pink'}),
        dict(type='text', size=26, h=60, fn=lambda S: (f"`和 <= upper` 的对数 `{max(S['right_high']-S['left'],0)}`，减去 `和 <= lower-1` 的对数 `{max(S['right_low']-S['left'],0)}`" if 'left' in S and 'right_high' in S else '')),
    ],
    watch=[('left', 'left', 'blue'), ('right_high', 'right_high', 'orange'), ('right_low', 'right_low', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums.sort()': '先排序：`{nums}`',
        'right_low = right_high': '两个右指针都从末尾出发：`right_high` 对 `upper`，`right_low` 对 `lower - 1`',
        'for left in range': '`left` = {left}：枚举左端点',
        'while right_low > left': lambda S, B, r: (f'`{S.nums[S.left]} + {S.nums[S.right_low]} = {S.nums[S.left]+S.nums[S.right_low]}` ' + ('`> lower-1`：太大，`right_low` 还要左移' if S.right_low > S.left and S.nums[S.left] + S.nums[S.right_low] > S.lower - 1 else '停下') if S.right_low > S.left else '`right_low` 已碰到 `left`'),
        'right_low -= 1': '`right_low` → {right_low}',
        'while right_high > left': lambda S, B, r: (f'`{S.nums[S.left]} + {S.nums[S.right_high]} = {S.nums[S.left]+S.nums[S.right_high]}` ' + ('`> upper`：太大，`right_high` 还要左移' if S.right_high > S.left and S.nums[S.left] + S.nums[S.right_high] > S.upper else '停下') if S.right_high > S.left else '`right_high` 已碰到 `left`'),
        'right_high -= 1': '`right_high` → {right_high}',
        'if right_high > left': lambda S, B, r: ('`right_high` 右侧都超过上界，`(left, right_high]` 都是和 `<= upper` 的配对' if S.right_high > S.left else '`right_high` 已经落在 `left` 上，没有和 `<= upper` 的配对'),
        'res += right_high - left': '`res += {right_high} - {left}` → {res}（和 `<= upper` 的配对先全算上）',
        'if right_low > left': lambda S, B, r: ('再减去和 `<= lower-1` 的配对（它们没到 lower）' if S.right_low > S.left else '没有和 `<= lower-1` 的配对，不用减'),
        'res -= right_low - left': '`res -= {right_low} - {left}` → {res}（只剩 `lower` 到 `upper` 之间的）',
        'return res': '公平数对共 `{res}` 个',
    },
    cards=dict(
        one_liner='区间计数拆成两个「和 ≤ x」的计数相减',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['数组 `nums`，数对 `(i, j)`，`i < j` 且 `lower <= nums[i]+nums[j] <= upper`',
                 '返回这样的数对个数',
                 '示例：`[0,1,7,4,4,5]`, `lower=3`, `upper=6` → `6`'],
        quote='可以将其转化为nums[i] + nums[j] <= upper的数对数目减去nums[i] + nums[j] <= lower - 1的数对数目。',
        quote_src='—— yiduobo 题解原文',
        idea=['套用两数之和的双指针：排序后左指针逐位右移',
              '同时维护两个右指针，分别对应 `upper` 和 `lower - 1`',
              '左指针变大时，右指针只会继续左移，总共 `O(n)`'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '易错：`lower - 1`，因为统计的是 `<=`',
                 '右指针需要 `> left` 才算有效配对，否则会重复或越界',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
