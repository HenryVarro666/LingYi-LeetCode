CONFIG = dict(
    num=2148, title='元素计数', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='一趟遍历 · 统计最大最小值个数',
    tags=[],
    code='''
class Solution(object):
    def countElements(self, nums):

        min_num = max_num = nums[0]
        min_cnt = max_cnt = 1
        for num in nums[1:]:
            if num < min_num:
                min_num = num
                min_cnt = 1
            elif num == min_num:
                min_cnt += 1
            
            if num > max_num:
                max_num = num
                max_cnt = 1
            elif num == max_num:
                max_cnt += 1
                
        if min_num == max_num:
            return 0
        else:
            return len(nums) - min_cnt - max_cnt
''',
    call='Solution().countElements([3, 1, 5, 3, 1, 5, 4])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 最小值，粉 = 最大值）', cell=90, h=230,
             pointers={'num': 'yellow'} if False else {},
             color=lambda S, i, v: ('blue' if 'min_num' in S and v == S['min_num'] else 'pink' if 'max_num' in S and v == S['max_num'] else None)
             if 'min_num' in S and S['min_num'] != S['max_num'] else None),
        dict(type='text', size=28, h=80, fn=lambda S: (f"最小值 `{S['min_num']}` 有 =={S['min_cnt']}== 个，最大值 `{S['max_num']}` 有 =={S['max_cnt']}== 个" if 'max_cnt' in S else '')),
    ],
    watch=[('num', 'num', 'yellow'), ('min_num', 'min_num', 'blue'), ('min_cnt', 'min_cnt', 'blue'),
           ('max_num', 'max_num', 'pink'), ('max_cnt', 'max_cnt', 'pink')],
    captions={
        'min_num = max_num': '先假设第一个数 `{nums[0]}` 既是最小也是最大',
        'min_cnt = max_cnt': '各出现 1 次',
        'for num in nums[1:]': lambda S, B, ret: (f'看下一个数 `{S.num}`' if S.num != B.get('num') else '遍历完了'),
        'if num < min_num': lambda S, B, ret: (f'`{S.num} < {S.min_num}`：更小的新最小值' if S.num < S.min_num else f'`{S.num}` 不比最小值 `{S.min_num}` 小'),
        'min_num = num': '最小值换成 `{min_num}`',
        'min_cnt = 1': '新的最小值，个数重置为 `1`',
        'elif num == min_num': lambda S, B, ret: (f'`{S.num} == {S.min_num}`：又遇到一个最小值' if S.num == S.min_num else f'`{S.num} ≠ {S.min_num}`'),
        'min_cnt += 1': '最小值个数 → `{min_cnt}`',
        'if num > max_num': lambda S, B, ret: (f'`{S.num} > {S.max_num}`：更大的新最大值' if S.num > S.max_num else f'`{S.num}` 不比最大值 `{S.max_num}` 大'),
        'max_num = num': '最大值换成 `{max_num}`',
        'max_cnt = 1': '新的最大值，个数重置为 `1`',
        'elif num == max_num': lambda S, B, ret: (f'`{S.num} == {S.max_num}`：又遇到一个最大值' if S.num == S.max_num else f'`{S.num} ≠ {S.max_num}`'),
        'max_cnt += 1': '最大值个数 → `{max_cnt}`',
        'if min_num == max_num': lambda S, B, ret: ('最小等于最大：所有元素都一样，没有严格更小/更大的 → 答案 0' if S.min_num == S.max_num else f'`{S.min_num} ≠ {S.max_num}`：用总数减去两端'),
        'return 0': '全部相同，返回 `0`',
        'return len': '`{len(nums)} − {min_cnt} − {max_cnt}` = =={ret}==：中间的数才有严格更小和更大的元素',
    },
    cards=dict(
        one_liner='不等于最大值、也不等于最小值的元素才满足',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['统计 `nums` 中==同时有严格更小和严格更大元素==的元素个数',
                 '示例：`[11,7,2,15]` → `2`',
                 '本视频：`[3,1,5,3,1,5,4]` → `3`'],
        quote='换言之就是问数组中不等于最大值和最小值的元素个数有多少，那么可以一趟遍历，找出数组中等于最大值和最小值的元素个数，然后用数组长度减去这两种数的个数即为最终答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['有更小又有更大 ⇔ 既不是最小值也不是最大值',
              '一趟遍历同时维护最小值/个数、最大值/个数；遇到更极端的值就重置个数',
              '答案 = 总数 − 最小值个数 − 最大值个数'],
        summary=['时间 `O(n)`，空间 `O(1)`，一次遍历',
                 '易错：所有元素相同时最小等于最大，不能相减（会减出负数），直接返回 `0`',
                 '最值可以重复出现，所以要数个数而不是只减 2',
                 '原文为 Python 2 风格，本题代码无需改动'],
    ),
)
