def _info(S):
    if 'even_info' in S:
        f = lambda a: '、'.join(f'{k}×{c}' for k, c in a)
        return f"偶数位按次数排序：`{f(S['even_info'])}`；奇数位：`{f(S['odd_info'])}`"
    return '偶数位、奇数位各自选一个出现最多的数当目标'


CONFIG = dict(
    num=2170, title='使数组变成交替数组的最少操作数', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='奇偶分开统计，众数相同时分四种情况',
    tags=['灵神题单', '贪心算法', '难度分 1663'],
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
        dict(type='array', var='nums', label='nums（蓝 = 偶数位，粉 = 奇数位）', pointers={'index': 'yellow'},
             color=lambda S, i, v: 'blue' if i % 2 == 0 else 'pink', h=200),
        dict(type='map', var='even', label='even：偶数位上各数的次数', fmt=lambda k, v: f'{k} → {v}', h=170),
        dict(type='map', var='odd', label='odd：奇数位上各数的次数', fmt=lambda k, v: f'{k} → {v}', h=170),
        dict(type='text', fn=_info, size=28),
    ],
    watch=['n', 'odd_cnt', 'even_cnt'],
    captions={
        'n = len(nums)': '数组长度 `n` = {n}',
        'if n == 1': lambda S, B, ret: ('只有一个数，本来就是交替数组 → 返回 0' if S.n == 1 else '`n >= 2`，要分别处理奇偶位'),
        'odd = {}': '`odd` 统计奇数位上每个数出现几次',
        'even = {}': '`even` 统计偶数位上每个数出现几次',
        'if index % 2 == 0': lambda S, B, ret: f'下标 `{S.index}` 是{"==偶数位==" if S.index % 2 == 0 else "奇数位"}',
        'even[num] =': '偶数位：`even[{num}]` = {even[num]}',
        'odd[num] =': '奇数位：`odd[{num}]` = {odd[num]}',
        'odd_info =': '奇数位按次数从大到小排：`{odd_info}`',
        'even_info =': '偶数位按次数从大到小排：`{even_info}`',
        'odd_cnt =': '奇数位共 `{odd_cnt}` 个位置',
        'even_cnt =': '偶数位共 `{even_cnt}` 个位置（n 为奇数时多一个）',
        'if odd_info[0][0] !=': lambda S, B, ret: (f'两边出现最多的数：奇 `{S.odd_info[0][0]}`，偶 `{S.even_info[0][0]}` → ' + ('==不同==，各取自己最多的' if S.odd_info[0][0] != S.even_info[0][0] else '==相同==，不能同时用，要分情况')),
        'return n - odd_info[0][1] - even_info[0][1]': '保留 `{odd_info[0][1]} + {even_info[0][1]}` 个，改 `{ret}` 个',
        'elif len(odd_info) == 1': lambda S, B, ret: ('奇数位上只有一种数 → 情况 1 或 2' if len(S.odd_info) == 1 else '奇数位至少两种数，继续看偶数位'),
        'if len(even_info) == 1': lambda S, B, ret: ('偶数位也只有一种数：整个数组都是同一个数' if len(S.even_info) == 1 else '偶数位至少两种数'),
        'return odd_cnt': '全是同一个数：改掉奇数位即可（奇数位不多于偶数位）→ `{ret}`',
        'return even_cnt - even_info[1][1]': '奇数位保持，偶数位改成次多的数：`{even_cnt} − {even_info[1][1]}` = =={ret}==',
        'elif len(even_info) == 1': '偶数位只有一种数 → 情况 3（与情况 2 对称）',
        'return odd_cnt - odd_info[1][1]': '偶数位保持，奇数位改成次多的数：`{odd_cnt} − {odd_info[1][1]}` = {ret}',
        'return min(': '两种方案取小：`{ret}`',
    },
    cards=dict(
        one_liner='奇偶位各选众数；撞车时，退一步选次多的',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['交替数组：`nums[i-2] == nums[i]` 且 `nums[i-1] != nums[i]`；每次操作可改任一个数',
                 '示例：`[1,2,2,2,2]` → `2`（改成 `[1,2,1,2,1]`）'],
        quote='为了使得操作次数最少，那么就应该分别选择奇数位以及偶数位上出现次数最多的数作为变换的目标。',
        quote_src='—— yiduobo 题解原文',
        idea=['`n == 1` 是边界，直接返回 0',
              '众数不同就各取众数；相同则分四种情况',
              '一边全相同时只能改另一边；两边都有次多时，两种交叉方案取小'],
        summary=['原文为 Python 2 写法，`odd_cnt = n / 2` 与 `even_cnt = (n + 1) / 2` 已改为 `//`',
                 '时间 `O(n log n)`（排序），空间 `O(n)`',
                 '易错：全相同时选改奇数位，因为 `n` 为奇数时偶数位更多',
                 '对比灵神：灵神用 `(0, 0)` 填充统一处理四种情况，这里显式分支'],
    ),
)
