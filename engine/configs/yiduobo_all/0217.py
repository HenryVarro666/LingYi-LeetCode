CONFIG = dict(
    num=217, title='存在重复元素', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='set 去重查找',
    tags=[],
    code='''
class Solution(object):
    def containsDuplicate(self, nums):

        num_set = set()
        for num in nums:
            if num in num_set:
                return True
            num_set.add(num)

        return False
''',
    call='Solution().containsDuplicate([3,1,4,5,9,2,1])',
    expect=True,
    views=[
        dict(type='array', var='nums', h=200,
             color=lambda S, i, v: 'blue' if 'num' in S and v == S['num'] else None),
        dict(type='set', var='num_set', h=260, fmt=lambda x: str(x)),
    ],
    watch=[('num', 'num', 'blue'), ('num_set', 'sorted(num_set)', 'green')],
    captions={
        'num_set = set()': '新建集合 `num_set`，用来放见过的数',
        'for num in nums': '取出这一个数 `num = {num}`',
        'if num in num_set': lambda S, B, r: (f'`{S.num}` 在 `num_set` 里 → ==重复出现==' if S.num in S.num_set
                                              else f'`{S.num}` 不在集合里 → 第一次见'),
        'return True': '集合里已有这个数，说明出现了两次 → 返回 `True`',
        'num_set.add(num)': '第一次见，把 `{num}` 记进集合',
        'return False': '整个数组扫完没有重复 → 返回 `False`',
    },
    cards=dict(
        one_liner='用 set 记录出现过的数，再来一次就是重复',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['判断数组里是否有任何值出现 ==至少两次==',
                 '有重复返回 `True`，全都不同返回 `False`',
                 '本视频：`[3,1,4,5,9,2,1]` → `True`'],
        quote='比较基础的题目，排序后查找或者使用树、哈希表之类的都行，我在这里用的set。',
        quote_src='—— yiduobo 题解原文',
        idea=['原文提到几种办法：排序后看相邻、用树、用哈希表',
              '这里选 set：查找和插入平均 `O(1)`',
              '每个数先查后存，查到就说明之前放过'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '排序法空间更省，但要 `O(n log n)`',
                 '原文为 Python 2 风格，只是 `class Solution(object)`，在 Python 3 中可直接运行'],
    ),
)
