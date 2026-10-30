CONFIG = dict(
    num=1748, title='唯一元素的和', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='字典计数', tags=[],
    code='''
class Solution(object):
    def sumOfUnique(self, nums):

        num_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1

        res = 0
        for num, cnt in num_dict.items():
            if cnt == 1:
                res += num
        
        return res
''',
    call='Solution().sumOfUnique([1,2,3,2,5,5,7])',
    expect=11,
    views=[
        dict(type='array', var='nums', pointers={}, cell=80, h=200,
             color=lambda S, i, v: 'yellow' if S.get('num') == v and S['_line'] <= 6 else None),
        dict(type='map', var='num_dict', label='num_dict（数 → 出现次数）', h=300,
             fmt=lambda k, v: f'{k}: {v}'),
    ],
    watch=['num', 'cnt', ('res', 'res', 'green')],
    captions={
        'num_dict = {}': '`num_dict` 记录每个数出现的次数',
        'for num in nums': '依次取 `{num}`',
        'num_dict[num] = num_dict.get': '`{num}` 的次数 +1，没出现过就从 0 开始：`num_dict[{num}] = {num_dict[num]}`',
        'res = 0': '`res` 累加只出现 1 次的数',
        'for num, cnt in num_dict.items()': '遍历字典：`{num}` 出现了 `{cnt}` 次',
        'if cnt == 1': lambda S, B, r: (f'`{S.num}` 只出现 1 次 → 是唯一元素，要加' if S.cnt == 1 else f'`{S.num}` 出现 {S.cnt} 次 → 不唯一，跳过'),
        'res += num': '`res = {B.res} + {num} = {res}`',
        'return res': '唯一元素之和 `{res}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='先数一遍次数，再把次数为 1 的数加起来',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['整数数组 `nums`，其中只出现一次的元素称为唯一元素',
                 '返回所有唯一元素之和',
                 '示例：`[1,2,3,2]` → `4`；本视频 `[1,2,3,2,5,5,7]` → `11`'],
        quote='比较基础的题目。利用dict统计每个元素出现的次数，然后将其中只出现一次的元素相加即可。',
        quote_src='—— yiduobo 题解原文',
        idea=['第一遍：用字典 `get(num, 0) + 1` 统计次数',
              '第二遍：遍历字典，次数为 1 的累加',
              '2 和 5 出现了两次，不算；1、3、7 相加得 11'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：累加的是数的值，不是次数',
                 '`dict.get(key, 0)` 省去判断是否存在',
                 '原文代码无需修改，直接运行（原文已是 `.items()`）'],
    ),
)
