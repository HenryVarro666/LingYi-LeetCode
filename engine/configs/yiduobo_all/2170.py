CONFIG = dict(
    num=2170, title='使数组变成交替数组的最少操作数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='奇偶位分别取众数 · 冲突时分类讨论',
    tags=['贪心算法', '思维题', '难度分 1663'],
    code='''
class Solution(object):
    def minimumOperations(self, nums):

        n = len(nums)
        if n == 1:
            return 0

        odd = {}
        even = {}
        for index, num in enumerate(nums):
            if index % 2 == 0:
                even[num] = even.get(num, 0) + 1
            else:
                odd[num] = odd.get(num, 0) + 1
        
        odd_info = sorted(odd.items(), key=lambda d:d[1], reverse=True)
        even_info = sorted(even.items(), key=lambda d:d[1], reverse=True)
        odd_cnt = n // 2
        even_cnt = (n + 1) // 2

        if odd_info[0][0] != even_info[0][0]:
            return n - odd_info[0][1] - even_info[0][1]
        elif len(odd_info) == 1:
            if len(even_info) == 1:
                return odd_cnt
            else:
                return even_cnt - even_info[1][1]
        elif len(even_info) == 1:
            return odd_cnt - odd_info[1][1]
        else:
            return min(n - odd_info[0][1] - even_info[1][1], n - odd_info[1][1] - even_info[0][1])
''',
    call='Solution().minimumOperations([1,2,2,2,2])',
    expect=2,
    views=[
        dict(type='array', var='nums', h=190, label='nums（蓝 = 偶数位，粉 = 奇数位）', pointers={'index': 'yellow'},
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink'),
        dict(type='map', var='even', h=150, label='even：偶数位上各数出现次数', fmt=lambda k, v: f'{k} : {v}'),
        dict(type='map', var='odd', h=150, label='odd：奇数位上各数出现次数', fmt=lambda k, v: f'{k} : {v}'),
        dict(type='text', size=30, h=70, fn=lambda S: (f"偶数位最多 `{S['even_info'][0][0]}`×{S['even_info'][0][1]}，奇数位最多 `{S['odd_info'][0][0]}`×{S['odd_info'][0][1]}" if 'even_info' in S and 'odd_info' in S else '')),
    ],
    watch=['n', 'index', 'odd_cnt', 'even_cnt', 'odd_info', 'even_info'],
    captions={
        'if n == 1': lambda S, B, ret: '只有一个数：已经是交替数组，==不用操作==' if S.n == 1 else f'`n = {S.n}` 不是 1，继续往下',
        'if index % 2 == 0': lambda S, B, ret: f"下标 `{S.index}` 是" + ('偶数位' if S.index % 2 == 0 else '奇数位'),
        'even[num] =': '偶数位上 `{num}` 的次数 → =={even[num]}==',
        'odd[num] =': '奇数位上 `{num}` 的次数 → =={odd[num]}==',
        'odd_info = sorted': '奇数位按出现次数从大到小排：`{odd_info}`',
        'even_info = sorted': '偶数位按出现次数从大到小排：`{even_info}`',
        'odd_cnt = ': '奇数位共 `odd_cnt = {odd_cnt}` 个',
        'even_cnt = ': '偶数位共 `even_cnt = {even_cnt}` 个（长度为奇数时比奇数位多一个）',
        'if odd_info[0][0] != even_info': lambda S, B, ret: (f"两边的最多数 `{S.odd_info[0][0]}` 和 `{S.even_info[0][0]}`" + (' 不同：各自保留自己的众数就行' if S.odd_info[0][0] != S.even_info[0][0] else ' ==相同==：不能同时保留，要分类讨论')),
        'elif len(odd_info) == 1': lambda S, B, ret: ('奇数位上所有数都相同' if len(S.odd_info) == 1 else '奇数位上至少有两种数'),
        'if len(even_info) == 1': lambda S, B, ret: ('偶数位上所有数也都相同：整个数组是同一种数，改掉奇数位（奇数位不多于偶数位）' if len(S.even_info) == 1 else '偶数位上至少有两种数：奇数位不动，偶数位改成次多的数'),
        'return even_cnt - even_info[1][1]': '奇数位保持，偶数位保留次多的 `{even_info[1][0]}`（{even_info[1][1]} 个）：`{even_cnt} - {even_info[1][1]}` = =={ret}==',
        'return odd_cnt': '整个数组是同一种数：改掉奇数位，`{ret}` 次',
        'return odd_cnt - odd_info[1][1]': '偶数位保持，奇数位保留次多的：`{odd_cnt} - {odd_info[1][1]}` = =={ret}==',
        'return n - odd_info[0][1] - even_info[0][1]': '各留各的众数：`{n} - {odd_info[0][1]} - {even_info[0][1]}` = =={ret}==',
        'return min(': '两边都有第二选择：一边留众数、另一边留次多，两种方案取小 = =={ret}==',
    },
    cards=dict(
        one_liner='奇偶位各取出现最多的数；撞车就退一步取次多',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['交替数组：`nums[i-2] == nums[i]`，且相邻两数不相等',
                 '一次操作可把任一位改成任意正整数，求变成交替数组的最少操作数',
                 '示例：`[1,2,2,2,2]` → `2`，改成 `[1,2,1,2,1]`'],
        quote='为了使得操作次数最少，那么就应该分别选择奇数位以及偶数位上出现次数最多的数作为变换的目标。',
        quote_src='—— yiduobo 题解',
        idea=['把数按奇偶位分开，各自统计次数并从大到小排序成 `odd_info`、`even_info`',
              '两边最多的数不同：各取众数，操作数 `n - odd_info[0][1] - even_info[0][1]`',
              '两边最多的数相同：不能都留，分四种情况，退而取==次多的数==',
              '一边全相同时只能改另一边；两边都有选择时，取两种方案较小者'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`',
                 '`n == 1` 要先特判，否则 `odd_info[0]` 会越界',
                 '偶数位个数是 `(n + 1) // 2`，奇数位是 `n // 2`，整个数组同一种数时选改奇数位',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`（`odd_cnt`、`even_cnt` 两处）'],
    ),
)
