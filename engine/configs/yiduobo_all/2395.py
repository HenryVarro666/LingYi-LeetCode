CONFIG = dict(
    num=2395, title='和相等的子数组', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希集合 · 边遍历边查',
    tags=[],
    code='''
class Solution(object):
    def findSubarrays(self, nums):

        sum_set = set()
        for index in range(1, len(nums)):
            s = nums[index - 1] + nums[index]
            if s in sum_set:
                return True
            sum_set.add(s)
        
        return False
''',
    call='Solution().findSubarrays([1, 5, 3, 4, 2])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = nums[index]，绿 = nums[index-1]）', cell=100, h=200,
             pointers={'index': 'blue'},
             color=lambda S, i, v: ('blue' if i == S['index'] else 'green' if i == S['index'] - 1 else None) if 'index' in S else None),
        dict(type='set', var='sum_set', label='sum_set（已出现过的相邻和）', fmt=lambda x: str(x), h=150),
        dict(type='text', size=28, h=100,
             fn=lambda S: (f"当前相邻和 `nums[{S['index']-1}] + nums[{S['index']}] = {S['s']}`" if 's' in S and 'index' in S else '')),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'orange')],
    captions={
        'sum_set = set()': '`sum_set` 存已经出现过的长度为 2 的子数组之和',
        'for index in range': lambda S, B, ret: ('遍历完了，没有重复' if 'index' in B and S.index == B.index
                                                 else f'从下标 1 开始，和上一个元素配对：`index = {S.index}`'),
        's = nums[index - 1]': '`{nums[index - 1]} + {nums[index]}` = =={s}==',
        'if s in sum_set': lambda S, B, ret: (f'`{S.s}` 已在 `sum_set` 中 → ==前面有一组和相同的子数组=='
                                              if S.s in S.sum_set else f'`{S.s}` 没出现过，继续'),
        'return True': '找到和相同的两个子数组，返回 `True`',
        'sum_set.add(s)': '记下这个和：`sum_set = {sorted(sum_set)}`',
        'return False': '遍历完都没有重复，返回 `False`',
    },
    cards=dict(
        one_liner='一边算相邻和，一边查哈希集合里见没见过',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断是否存在两个长为 2 的子数组和相等（起始下标不同）',
                 '示例：`[4,2,4]` → `true`；`[1,2,3,4,5]` → `false`',
                 '本视频：`[1,5,3,4,2]` → `true`'],
        quote='长度为n的数组最多也就只有n - 1组长度为2的子数组，因此可以直接暴力枚举。……使用哈希表维护已经出现过的子数组和。',
        quote_src='—— yiduobo 题解',
        idea=['长度为 2 的子数组至多 `n-1` 组，直接枚举即可',
              '从下标 1 起，当前元素与上一个元素相加得 `s`',
              '`s` 在集合里 → 找到答案；否则加入集合继续'],
        result='`1+5=6` 入集合，…，`4+2=6` 命中 → True ✓',
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：下标要从 1 开始，否则 `nums[index-1]` 会取到末尾元素',
                 '遍历完仍无重复才返回 `False`',
                 '提前返回：命中即停，不必算完全部相邻和'],
    ),
)
