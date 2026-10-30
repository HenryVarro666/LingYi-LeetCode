CONFIG = dict(
    num=2161, title='根据给定数字划分数组', difficulty='Medium', category='模拟',
    author='灵茶山艾府', technique='三个数组 · 稳定三路分区',
    code='''
class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        a, b, c = [], [], []
        for x in nums:
            if x < pivot:
                a.append(x)
            elif x == pivot:
                b.append(x)
            else:
                c.append(x)
        return a + b + c
''',
    call='Solution().pivotArray([9,12,5,10,14,3,10], 10)',
    expect=[9, 5, 3, 10, 10, 12, 14],
    views=[
        dict(type='array', var='nums', h=150, label='nums',
             color=lambda S, i, v: None),
        dict(type='array', var='a', h=120, label='a（小于 pivot）'),
        dict(type='array', var='b', h=120, label='b（等于 pivot）'),
        dict(type='array', var='c', h=120, label='c（大于 pivot）'),
    ],
    watch=['x', 'pivot'],
    captions={
        'a, b, c = [], [], []': '准备三个数组：小于、等于、大于 `pivot`',
        'if x < pivot': lambda S, B, r: f'`{S.x} < {S.pivot}` ' + ('成立 → 进 a' if S.x < S.pivot else '不成立'),
        'a.append': '`{x}` 比 pivot 小 → 追加到 `a`：`{a}`',
        'elif x == pivot': lambda S, B, r: f'`{S.x} == {S.pivot}` ' + ('成立 → 进 b' if S.x == S.pivot else '不成立 → 只能是大于'),
        'b.append': '`{x}` 等于 pivot → 追加到 `b`：`{b}`',
        'c.append': '`{x}` 比 pivot 大 → 追加到 `c`：`{c}`',
        'return a + b + c': '按小、等、大拼接：`{a + b + c}`',
    },
    cards=dict(
        one_liner='三个数组各管一类，按原顺序追加，最后拼起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['把 `nums` 按 `pivot` 重排：小于的在前、等于的居中、大于的在后',
                 '小于区、大于区内部==保持原来的相对顺序==',
                 '示例：`[9,12,5,10,14,3,10]`，`pivot=10` → `[9,5,3,10,10,12,14]`'],
        quote='用三个数组分别保持小于、等于和大于 pivot 的元素，最后把三个数组拼成答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['从左到右扫一遍，每个数按大小关系进对应的数组',
              '追加到末尾，天然保持原有相对顺序',
              '最后 `a + b + c` 就是答案'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '灵神提醒：本题是三路分区，但要求结果==稳定==',
                 '快速排序里常见的三路分区不稳定，不适用本题'],
    ),
)
