CONFIG = dict(
    num=2164, title='对奇偶下标分别排序', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='按奇偶下标分组排序后交替合并（Go 原文转写）', tags=[],
    code='''
class Solution:
    def sortEvenOdd(self, nums: List[int]) -> List[int]:
        a = [[], []]
        for i, v in enumerate(nums):
            a[i & 1].append(v)
        a[0].sort()
        a[1].sort(reverse=True)
        nums = nums[:0]
        for i, v in enumerate(a[0]):
            nums.append(v)
            if i < len(a[1]):
                nums.append(a[1][i])
        return nums
''',
    call='Solution().sortEvenOdd([5,2,8,1,3,9,4])',
    expect=[3, 9, 4, 2, 5, 1, 8],
    views=[
        dict(type='array', var='nums', label='nums（先是原数组；清空后逐步拼成答案）', h=170, pointers={'i': 'blue'},
             color=lambda S, i, v: ('blue' if i == S['i'] else None) if S['_line'] in (5,) else None),
        dict(type='array', var=lambda S: S['a'][0] if 'a' in S else [], label='a[0]：偶数下标的值', h=150,
             color=lambda S, i, v: 'blue' if S['_line'] >= 9 and i == S.get('i') else None),
        dict(type='array', var=lambda S: S['a'][1] if 'a' in S else [], label='a[1]：奇数下标的值', h=150,
             color=lambda S, i, v: 'pink' if S['_line'] >= 9 and i == S.get('i') else None),
    ],
    watch=[('i', 'i', 'blue'), 'v'],
    captions={
        'a = [[], []]': '`a[0]` 放偶数下标的值，`a[1]` 放奇数下标的值',
        'a[i & 1].append': '下标 `{i}`：`i & 1 = {i & 1}`，{"偶数" if i % 2 == 0 else "奇数"}下标 → 值 `{v}` 放进 `a[{i & 1}]`',
        'a[0].sort()': '偶数下标要非递减 → 从小到大排：`{a[0]}`',
        'a[1].sort': '奇数下标要非递增 → ==从大到小==排：`{a[1]}`',
        'nums = nums[:0]': '`nums` 清空，准备按顺序重新拼：偶、奇、偶、奇……',
        'nums.append(v)': '第 `{i}` 个偶数位的值 `{v}` 放进答案：`{nums}`',
        'if i < len(a[1])': lambda S, B, r: (f'偶数位比奇数位可能多一个：`{S.i} < {len(S.a[1])}` → 还有奇数位的值要放' if S.i < len(S.a[1]) else f'`{S.i} < {len(S.a[1])}` 不成立：奇数位已放完，这是多出的最后一个偶数位'),
        'nums.append(a[1][i])': '紧跟着放第 `{i}` 个奇数位的值 `{a[1][i]}`：`{nums}`',
        'return nums': '交替拼完，返回 `{ret}`',
    },
    cards=dict(
        one_liner='偶数下标一组升序，奇数下标一组降序，再交替拼回',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['奇数下标上的值按非递增排序，偶数下标上的值按非递减排序',
                 '各排各的，位置仍是原来的奇偶位',
                 '示例：`[4,1,2,3]` → `[2,3,4,1]`；本视频用 `[5,2,8,1,3,9,4]`'],
        quote='a[i&1] = append(a[i&1], v)；sort.Sort(a[0])；sort.Sort(sort.Reverse(a[1]))；然后 a[0]、a[1] 交替放回 nums。',
        quote_src='—— 灵茶山艾府题解（Go 原文）',
        idea=['`i & 1` 一步把值分到两个组：偶数下标一组，奇数下标一组',
              '偶数组正序、奇数组倒序，两组互不影响',
              '合并时先放偶数组第 `i` 个、再放奇数组第 `i` 个，偶数组长度 ≥ 奇数组'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '原文为 Go，已按原逻辑逐行转写为 Python（`sort.Reverse` 对应 `sort(reverse=True)`）',
                 '易错点：合并时要判断 `i < len(a[1])`，奇数长度时偶数组多一个',
                 '`nums = nums[:0]` 在 Go 中复用原数组；Python 里得到新空列表，效果相同'],
    ),
)
