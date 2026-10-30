def _text(S):
    if 'num' not in S:
        return '题目保证 `nums[i] ≤ 100000`：偶数位只可能是 2 位、4 位和 `100000`'
    n = S['num']
    if 10 <= n < 100:
        return f'`{n}` 在 [10, 100)：==2 位数== → 偶数位'
    if 1000 <= n < 10000:
        return f'`{n}` 在 [1000, 10000)：==4 位数== → 偶数位'
    if n == 100000:
        return f'`{n}` 恰好是 `100000`：==6 位数== → 偶数位'
    return f'`{n}` 是奇数位（1、3 或 5 位）'


def _color(S, i, v):
    if 'num' not in S:
        return None
    n = S['num']
    if (10 <= n < 100) or (1000 <= n < 10000) or n == 100000:
        return 'green' if v == n else None
    return 'pink' if v == n else None


CONFIG = dict(
    num=1295, title='统计位数为偶数的数字', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='按数值范围判断位数',
    code='''
class Solution(object):
    def findNumbers(self, nums):

        res = 0
        for num in nums:
            if (num >= 10 and num < 100) or (num >= 1000 and num < 10000) or num == 100000:
                res += 1
        return res
''',
    call='Solution().findNumbers([12, 345, 2, 6, 7896, 100000])',
    expect=3,
    views=[
        dict(type='text', fn=_text, h=90),
        dict(type='array', var='nums', color=_color, h=260, label='nums', cell=120),
    ],
    watch=['num', ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 统计偶数位数字的个数',
        'for num in nums': lambda S, B, r: ('遍历结束' if ('num' in B and B.num == S.num and S.num == S.nums[-1]) else f'取出 `num = {S.num}`'),
        'if (num >= 10': '`{num}` 落在 [10,100)、[1000,10000) 或等于 100000 吗 → {"是" if ((num >= 10 and num < 100) or (num >= 1000 and num < 10000) or num == 100000) else "否"}',
        'res += 1': '位数是偶数，`res` → {res}',
        'return res': '共 `{res}` 个偶数位数字',
    },
    cards=dict(
        one_liner='数值上限只有 100000，偶数位只有三类',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['给整数数组 `nums`，统计其中==位数为偶数==的数字个数',
                 '示例：`[12,345,2,6,7896]` → `2`',
                 '本视频：`[12,345,2,6,7896,100000]` → `3`'],
        quote='由于题目中的数字都小于等于100000，那么偶数位的数字只有两位数、四位数以及100000，一趟循环判断即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['`1 ≤ nums[i] ≤ 10^5`，所以位数最多 6 位',
              '偶数位：2 位 `[10,100)`、4 位 `[1000,10000)`，以及 6 位里唯一的 `100000`',
              '一趟遍历，落在这三类里就计数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '依赖题目的数据范围；范围变大就要改条件',
                 '`100000` 是 6 位数，容易漏掉',
                 '对比灵神：灵神每次除以 100 来判断奇偶，不依赖范围'],
    ),
)
