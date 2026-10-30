CONFIG = dict(
    num=3974, title='K 个元素的最大总和', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='取最大 k 个 · 先大后小',
    tags=['贪心与思维', '排序不等式', '难度分 1263'],
    code='''
class Solution(object):
    def maxSum(self, nums, k, mul):
        
        nums.sort(reverse=True)
        res = 0
        for v in nums[:k]:
            if mul > 0:
                res += mul * v
                mul -= 1
            else:
                res += v
        
        return res
''',
    call='Solution().maxSum([3, 7, 5, 2, 4], 4, 2)',
    expect=26,
    views=[
        dict(type='array', var='nums', h=240, label='nums（降序；绿 = 已处理，灰 = 不选）',
             color=lambda S, i, v: 'green' if 'res' in S and i < min(4, 2 + 0) and False else None,
             dim=lambda S, i, v: i >= 4),
        dict(type='text', fn=lambda S: (f"`mul = {S['mul']}`：" + ('大于 0，乘上去更赚' if S['mul'] > 0 else '不大于 0，直接加')) if 'mul' in S else '', h=80),
    ],
    watch=[('v', 'v', 'yellow'), ('mul', 'mul', 'pink'), ('res', 'res', 'green')],
    captions={
        'nums.sort': '从大到小排序：`{nums}`',
        'res = 0': '`res` 是总和',
        'for v in nums[:k]': '前 `k` 个最大的数，从大到小：`v = {v}`',
        'if mul > 0': lambda S, B, r: (f'`mul = {S.mul} > 0` → 成立，乘了再加' if S.mul > 0 else f'`mul = {S.mul} > 0` → 不成立，直接加'),
        'res += mul * v': '`res += {B.mul} × {v}` → =={res}==',
        'mul -= 1': '`mul` 减 1 → {mul}',
        'res += v': 'mul 已经 ≤ 0，乘了反而更小 → 直接加 `{v}`：res = =={res}==',
        'return res': '最大总和 `{res}`',
    },
    cards=dict(
        one_liner='两点贪心：选最大的 k 个，且大的先操作',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['从 `nums` 恰好选 `k` 个，逐个处理：直接加，或乘 `mul` 再加',
                 '每处理一个，`mul` 减 1，可变成 0 或负数',
                 '本视频：`nums=[3,7,5,2,4]`，`k=4`，`mul=2` → `26`'],
        quote='先操作的较大的元素收益更大。基于以上两点，在这里就只需要对nums从大到小进行一趟排序，然后遍历前k个元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['要总和大，操作的就应该是最大的 `k` 个数（都是正数）',
              '`x` 先 `y` 后：`(x+y)·mul − y`；反过来是 `(x+y)·mul − x`，前者更大 → 大的先做',
              '`mul > 0` 就乘，否则直接加'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '只有 `mul > 0` 才减 1；`mul` 变成 0 后不再变化，直接加',
                 '`mul = 1` 时乘不乘结果相同，不影响答案',
                 '原文已是 Python 3 可运行写法，无需修改'],
    ),
)
