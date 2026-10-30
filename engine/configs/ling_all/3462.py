CONFIG = dict(
    num=3462, title='提取至多 K 个元素的最大总和', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='每行取最大再全局取最大',
    tags=['贪心', '排序', '难度分 1416'],
    code='''
class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        a = []
        for row, limit in zip(grid, limits):
            row.sort(reverse=True)
            a += row[:limit]

        a.sort(reverse=True)
        return sum(a[:k])
''',
    call='Solution().maxSum([[5,3,7,1],[8,2,6,4],[9,0,2,1]], [2,1,2], 4)',
    expect=29,
    views=[
        dict(type='grid', var='grid', h=250, cell=70,
             color=lambda S, i, j, v: 'green' if 'a' in S and j < S['limits'][i] and sum(S['limits'][:i + 1]) <= len(S['a']) else None),
        dict(type='array', var='a', h=130, label='候选 a'),
        dict(type='text', fn=lambda S: f"取前 `{S['k']}` 大求和：==" + ' + '.join(str(x) for x in S['a'][:S['k']]) + '==' if 'a' in S and S.get('_line', 0) >= 8 else '', size=28),
    ],
    watch=['limit', ('k', 'k', 'blue')],
    captions={
        'a = []': '`a` 收集每行「必取」的候选数',
        'row.sort': '没有负数，取越多越好 → 先把这一行从大到小排：`{row}`',
        'a += row[:limit]': '这一行最多取 `{limit}` 个，当然取最大的 `{limit}` 个：`{row[:limit]}`，`a` = {a}',
        'a.sort': '候选里再从大到小排：`a` = {a}',
        'return sum': '总共只能取 `{k}` 个，取最大的 `{k}` 个：`{a[:k]}` → =={ret}==',
    },
    cards=dict(
        one_liner='每行先取最大的 limit 个，再从中取最大的 k 个',
        complexity='时间 `O(mn log(mn))`，空间 `O(mn)`',
        problem=['矩阵 `grid`，第 `i` 行最多取 `limits[i]` 个数，总共最多取 `k` 个',
                 '求取出元素的最大和',
                 '示例：`[[1,2],[3,4]]`，`limits=[1,2]`，`k=2` → `7`'],
        quote='本题没有负数，所以每排都可以取恰好 limits[i] 个数。为了最大化元素和，每排取最大的 limits[i] 个数。然后再取这些数中最大的 k 个数，求和即为答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['数都 ≥ 0，多取不吃亏，所以每行都用满额度',
              '行内只会用到最大的 `limit` 个，其余不可能入选',
              '候选合并后，全局最大的 `k` 个就是答案'],
        summary=['时间 `O(mn log(mn))`，用快速选择可到 `O(mn)`',
                 '前提是没有负数，所以不必凑够 `k` 个也不会亏',
                 '`k` 不超过 `sum(limits)`，切片 `a[:k]` 不会不够',
                 '专题：贪心 §1.1 从最小/最大开始贪心'],
    ),
)
