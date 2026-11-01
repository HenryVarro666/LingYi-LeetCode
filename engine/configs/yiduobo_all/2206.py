CONFIG = dict(
    num=2206, title='将数组划分成相等数对', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='字典统计次数 · 检查是否全为偶数',
    tags=[],
    code='''
class Solution(object):
    def divideArray(self, nums):

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        for cnt in num_dict.values():
            if cnt % 2 == 1:
                return False

        return True
''',
    call='Solution().divideArray([3, 2, 3, 2, 2, 2])',
    expect=True,
    views=[
        dict(type='array', var='nums', label='nums', cell=90, h=170),
        dict(type='map', var='num_dict', label='num_dict（数 → 出现次数）', fmt=lambda k, v: f'{k}: {v}', h=150, font=34),
        dict(type='text', fn=lambda S: (f"次数 `cnt = {S['cnt']}` → " + ('==奇数，无法配对==' if S['cnt'] % 2 else '偶数，可以配对')) if 'cnt' in S else '', size=30),
    ],
    watch=[('num', 'num', 'blue'), ('cnt', 'cnt', 'orange')],
    captions={
        'num_dict = {}': '`num_dict` 记录每个数出现的次数',
        'for num in nums': '看下一个数 `num = {num}`',
        'num_dict[num] =': '`num_dict[{num}]` = {num_dict[num]}（出现次数加一）',
        'for cnt in num_dict.values()': '看下一种数的出现次数 `cnt = {cnt}`',
        'if cnt % 2 == 1': lambda S, B, ret: (f'`{S.cnt} % 2 == 1` → ==奇数次，剩一个配不成对=='
                                              if S.cnt % 2 == 1 else f'`{S.cnt} % 2 == 0` → 偶数次，能两两配对'),
        'return False': '有数出现奇数次 → 无法划分，返回 `False`',
        'return True': '每种数出现次数都是偶数 → ==可以划分==，返回 `True`',
    },
    cards=dict(
        one_liner='每种数的出现次数都是偶数，就能两两配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 有 `2n` 个整数，要划分成 `n` 个数对，每个数对里两个数相等',
                 '能划分返回 `true`，否则 `false`',
                 '示例：`[3,2,3,2,2,2]` → `true`；`[1,2,3,4]` → `false`'],
        quote='当每种数出现的次数都为偶数次时，就可以完成划分，否则就不能。',
        quote_src='—— yiduobo 题解原文',
        idea=['数对里两个数相等 ⇒ 某种数的个数必须是偶数', '先一趟遍历数出每种数的次数', '再检查所有次数，只要有一个奇数就返回 `False`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：`dict.get(num, 0)` 给没出现过的数一个默认次数 0',
                 '只要有一个奇数次就能立刻返回 False，不必检查后面的'],
    ),
)
