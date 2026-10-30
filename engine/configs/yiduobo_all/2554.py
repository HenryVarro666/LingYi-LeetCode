CONFIG = dict(
    num=2554, title='从一个范围内选择最多整数 I', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='集合标记 · 从小到大遍历',
    tags=['灵神题单', '从最小/最大开始贪心', '难度分 1333'],
    code='''
class Solution(object):
    def maxCount(self, banned, n, maxSum):

        ban_set = set(banned)
        s = 0
        res = 0
        for x in range(1, n + 1):
            if x not in ban_set and s + x <= maxSum:
                s += x
                res += 1

        return res
''',
    call='Solution().maxCount([1,6,5,3], 9, 13)',
    expect=3,
    views=[
        dict(type='set', var='ban_set', label='被 ban 的整数', fmt=lambda x: str(x)),
        dict(type='text', size=26, fn=lambda S: (f"已选和 `s = {S['s']}` ≤ `maxSum = {S['maxSum']}`，已选 `{S['res']}` 个" if 'res' in S else '')),
    ],
    watch=['n', ('x', 'x', 'blue'), ('s', 's', 'orange'), ('maxSum', 'maxSum', 'pink'), ('res', 'res', 'green')],
    captions={
        'ban_set = set': '把 `banned` 记进集合：`{ban_set}`',
        5: '`s` 记录已选整数的和',
        6: '`res` 记录已选个数',
        'for x in range': '一趟遍历，`x = {x}`：从小到大，每个数代价最小',
        'if x not in ban_set': lambda S, B, r: ('`{0}` 被 ban，跳过'.format(S.x) if S.x in S.ban_set
                                                 else (f'`{S.x}` 没被 ban，且 `{S.s} + {S.x} = {S.s + S.x} <= {S.maxSum}` → 选它' if S.s + S.x <= S.maxSum
                                                       else f'`{S.s} + {S.x} = {S.s + S.x} > {S.maxSum}`：超过 maxSum，不选')),
        's += x': '`s` {B.s} → =={s}==',
        'res += 1': '`res` = =={res}==',
        'return res': '最多选 `{res}` 个',
    },
    cards=dict(
        one_liner='整数都是正的，想选得多就选小的',
        complexity='时间 `O(n+m)`，空间 `O(m)`',
        problem=['从 `[1, n]` 选整数，每个至多一次，不能在 `banned` 里，和不超过 `maxSum`',
                 '求最多选几个',
                 '本视频：`banned=[1,6,5,3], n=9, maxSum=13` → `3`（2+4+7）'],
        quote='由于选择的整数都是正整数，那么为了使得选择最多的整数，就应该尽量选择数值较小的整数。',
        quote_src='—— yiduobo 题解原文',
        idea=['用集合 `ban_set` 记下被 ban 的整数',
              '从 1 到 n 一趟遍历：没被 ban 且加上后不超 `maxSum` 就选',
              '遍历完成（或和超限）为止'],
        after=[dict(heading='和灵神写法的区别', lines=['灵神额度递减，`i > maxSum` 就 break', 'yiduobo 累加 `s`，用 `s + x <= maxSum` 判断', '后者不提前停，会遍历完整个 `[1, n]`'])],
        summary=['时间 `O(n+m)`，空间 `O(m)`',
                 '易错：必须用集合判断是否被 ban，列表会退化成 `O(nm)`',
                 '易错：判断的是 `s + x <= maxSum`，不是 `s <= maxSum`',
                 '原文没有提前退出，遍历到 `n` 才结束'],
    ),
)
