CONFIG = dict(
    num=2357, title='使数组中所有元素都等于零', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='集合长度（0 单独扣掉）',
    tags=[],
    code='''
class Solution(object):
    def minimumOperations(self, nums):
        num_set = set(nums)
        res = len(num_set)
        if 0 in num_set:
            res -= 1
        
        return res
''',
    call='Solution().minimumOperations([1,5,0,3,5])',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums', cell=96, h=190,
             color=lambda S, i, v: 'green' if v != 0 else 'pink'),
        dict(type='set', var='num_set', label='num_set', fmt=lambda x: str(x), h=170),
        dict(type='text', h=90, size=32, fn=lambda S: f"当前 `res` = =={S['res']}==" if 'res' in S else ''),
    ],
    watch=[('num_set', 'sorted(num_set)', 'blue'), ('res', 'res', 'green')],
    captions={
        'num_set = set': '把所有数放进集合，重复的 `5` 只留一个：`{sorted(num_set)}`',
        'res = len': '集合长度 = 不同整数的个数 = =={res}==',
        'if 0 in': '集合里有 `0` 吗？{"有 → 0 不需要操作，要扣掉" if 0 in num_set else "没有，不用扣"}',
        'res -= 1': '扣掉 `0` 这一项：`res` = =={res}==',
        'return res': '返回 ==\'{res}\'==，即不同正数的个数'.replace("'", ''),
    },
    cards=dict(
        one_liner='有多少种不同的正数，就要操作多少次',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['每步选 `x ≤ 最小非零元素`，所有正数都减去 `x`',
                 '求让数组全变 0 的最少操作数',
                 '示例：`[1,5,0,3,5]` → `3`'],
        quote='数组中有多少种不同的正数就需要操作多少次，因此可以将数组中所有数都加入到集合中，集合的长度就是数组中不同整数的数目。如果0也在集合中，那么答案就是集合的长度减1。',
        quote_src='—— yiduobo 题解',
        idea=['最小的数至少要一次操作才能变 0',
              '操作后新的最小数同样至少要一次，依次类推',
              '所以答案 = 不同正数的种数；集合长度里若含 0 就减 1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错点：别把 `0` 算成一次操作',
                 '原文先建集合再单独判断 0，逻辑和 `len(set(nums) - {0})` 等价'],
    ),
)
