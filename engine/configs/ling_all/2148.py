CONFIG = dict(
    num=2148, title='元素计数', difficulty='Easy', category='数学算法',
    author='灵茶山艾府', technique='一次遍历 · 统计最小值和最大值的个数（Go 原文转写）',
    tags=[],
    code='''
class Solution:
    def countElements(self, nums: List[int]) -> int:
        min, max, cntMin, cntMax = nums[0], nums[0], 1, 1
        for v in nums[1:]:
            if v < min:
                min, cntMin = v, 1
            elif v == min:
                cntMin += 1
            if v > max:
                max, cntMax = v, 1
            elif v == max:
                cntMax += 1
        if min == max:
            return 0
        return len(nums) - cntMin - cntMax
''',
    call='Solution().countElements([3, 1, 5, 3, 1, 5, 4])',
    expect=3,
    views=[
        dict(type='array', var='nums', h=200, label='nums',
             color=lambda S, i, v: ('green' if v == S['min'] else 'pink' if v == S['max'] else None) if 'max' in S and S['min'] != S['max'] else None),
        dict(type='text', fn=lambda S: (f"最小值 ==`{S['min']}`== 出现 `{S['cntMin']}` 次，最大值 ==`{S['max']}`== 出现 `{S['cntMax']}` 次" if 'cntMax' in S else ''), size=28),
    ],
    watch=[('min', 'min', 'green'), ('cntMin', 'cntMin', 'green'), ('max', 'max', 'pink'), ('cntMax', 'cntMax', 'pink'), 'v'],
    captions={
        'min, max, cntMin, cntMax =': '先把第一个数当作最小值和最大值，各出现 `1` 次：`min = max = {min}`',
        'for v in nums': '依次看后面的数 `v = {v}`',
        'if v < min': lambda S, B, r: (f'`v = {S.v}` < `min = {S.min}`？' + ('成立，更小的数出现' if S.v < S.min else '不成立')),
        'min, cntMin = v, 1': '发现新的最小值 `{min}`，之前的最小值不再是最小：`cntMin` 重置为 `1`',
        'elif v == min': lambda S, B, r: (f'`v = {S.v}` 等于 `min = {S.min}`？' + ('==是，最小值又出现一次==' if S.v == S.min else '不是')),
        'cntMin += 1': '最小值再出现一次：`cntMin` → {cntMin}',
        'if v > max': lambda S, B, r: (f'`v = {S.v}` > `max = {S.max}`？' + ('成立，更大的数出现' if S.v > S.max else '不成立')),
        'max, cntMax = v, 1': '发现新的最大值 `{max}`：`cntMax` 重置为 `1`',
        'elif v == max': lambda S, B, r: (f'`v = {S.v}` 等于 `max = {S.max}`？' + ('==是，最大值又出现一次==' if S.v == S.max else '不是')),
        'cntMax += 1': '最大值再出现一次：`cntMax` → {cntMax}',
        'if min == max': lambda S, B, r: (f'`min = {S.min}`，`max = {S.max}`' + ('：==相等，所有数都一样，没有严格更小或更大的数，答案 0==' if S.min == S.max else '：不相等，继续')),
        'return len(nums)': '`{len(nums)} − {cntMin} − {cntMax}` = =={ret}==：扣掉最小值和最大值，剩下的数两边都有更小和更大的',
    },
    max_steps=90,
    cards=dict(
        one_liner='答案 = 总数 − 最小值个数 − 最大值个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['统计 `nums` 中==同时有更小元素和更大元素==的元素个数',
                 '示例：`[11,7,2,15]` → `2`（7 和 11）',
                 '本视频：`[3,1,5,3,1,5,4]` → `3`'],
        quote='统计 nums 的最小值的个数和最大值的个数，答案即为 nums 的长度减去这两个个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['等于最小值的数没有更小的；等于最大值的数没有更大的',
              '其余的数一定夹在中间，两边都有',
              '遍历时遇到更小（更大）的数就重置计数，相等就加一'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（变量 `min`/`max` 沿用原名）',
                 '时间 `O(n)`，空间 `O(1)`，只遍历一次',
                 '易错点：最小值和最大值相等（所有数相同）时答案是 `0`，否则会算成负数',
                 '更新最值时计数要重置为 `1`，不是 `0`'],
    ),
)
