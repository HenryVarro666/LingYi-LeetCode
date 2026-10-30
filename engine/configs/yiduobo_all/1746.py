CONFIG = dict(
    num=1746, title='经过一次操作后的最大子数组和', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='最大子段和 + 是否已操作',
    tags=[],
    code='''
class Solution(object):
    def maxSumAfterOperation(self, nums):

        f = g = res = 0
        for num in nums:
            g = max(g + num, f + num * num)
            f = max(f + num, 0)
            res = max(res, g)

        return res
''',
    call='Solution().maxSumAfterOperation([2, -1, -4, -3])',
    expect=17,
    max_steps=40,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前元素；绿 = 已处理）', h=210, cell=110,
             pointers={'_i': 'blue'} if False else {},
             color=lambda S, i, v: ('blue' if 'num' in S and i == S['nums'].index(S['num']) else
                                    ('green' if 'num' in S and i < S['nums'].index(S['num']) else None)) if 'f' in S else None),
        dict(type='text', size=28, h=70,
             fn=lambda S: (f"`f` = 没操作过的最大子段和 = =={S['f']}==　`g` = 已操作过 = =={S['g']}==" if 'f' in S else '')),
        dict(type='text', size=28, h=70,
             fn=lambda S: (f"当前 `num` = {S['num']}，平方后 = {S['num'] * S['num']}" if 'num' in S and 'f' in S else '')),
    ],
    watch=[('num', 'num', 'blue'), ('f', 'f', 'cyan'), ('g', 'g', 'pink'), ('res', 'res', 'green')],
    captions={
        'f = g = res = 0': '`f`：以当前位置结尾、没操作过（可为空）；`g`：已操作过；`res`：答案，全部从 0 起',
        'for num in nums': lambda S, B, r: (f'处理 `num = {S.num}`' if 'num' in S else '处理完毕'),
        'g = max': '`g` 两种来源：`g + num` = {B.g} + ({num}) 延续已操作段，或 `f + num²` = {B.f} + {num * num} 把 `{num}` 平方当作操作点 → =={g}==',
        'f = max': '`f = max(f + num, 0)` = `max({B.f} + ({num}), 0)` = =={f}==：和为负就丢掉，重新从空开始（注意 `g` 已先用了旧的 f）',
        'res = max': '`res = max({B.res}, g = {g})` = =={res}==',
        'return res': '最大子数组和（恰好操作一次）= =={ret}==',
    },
    cards=dict(
        one_liner='最大子段和，多记一个「是否已经平方过」',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['对 `nums` 恰好做一次操作：把某个 `nums[i]` 换成 `nums[i] × nums[i]`',
                 '求操作后最大的非空子数组和',
                 '示例：`[2,-1,-4,-3]` → `17`（把 -4 平方：2 − 1 + 16）'],
        quote='令f[i]表示以nums[i]结尾的最大子段和，这里的子段长度可以为0。令g[i]表示以nums[i]为结尾，且已经进行过一次操作的最大子段和。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f` 是经典最大子段和，和为负就清零重来',
              '`g` 要么在旧 `g` 上继续加，要么在旧 `f` 上把当前数平方后接上',
              '每个位置都用 `g` 刷新答案'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '==先更新 g 再更新 f==：`g` 要用上一轮的 `f`',
                 '`g` 包含平方操作，所以一定是非空段；答案取 `max(g)`',
                 '`f` 允许为空（和为 0），`g` 不允许'],
    ),
)
