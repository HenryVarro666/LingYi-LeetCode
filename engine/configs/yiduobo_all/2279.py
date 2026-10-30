CONFIG = dict(
    num=2279, title='装满石头的背包的最大数量', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='按剩余空间从小到大填',
    tags=['灵神题单', '从最小/最大开始贪心', '难度分 1249'],
    code='''
class Solution(object):
    def maximumBags(self, capacity, rocks, additionalRocks):

        res = 0
        for space in sorted([capacity[index] - rocks[index] for index in range(len(capacity))]):
            if additionalRocks < space:
                break
            res += 1
            additionalRocks -= space
        
        return res
''',
    call='Solution().maximumBags([2,3,4,5,9], [1,2,4,4,5], 4)',
    expect=4,
    views=[
        dict(type='array', var='capacity', label='capacity（容量）', h=150),
        dict(type='array', var='rocks', label='rocks（已装）', h=150),
        dict(type='array', var="sorted([capacity[i] - rocks[i] for i in range(len(capacity))])", label='剩余空间 space 从小到大（还需要放几块）', h=200,
             color=lambda S, i, v: ('green' if 'res' in S and i < S['res'] else 'blue' if 'space' in S and i == S['res'] else None),
             dim=lambda S, i, v: 'res' in S and i > S['res']),
        dict(type='text', size=32, h=110,
             fn=lambda S: f"手里还剩 additionalRocks = ==`{S['additionalRocks']}`==，已装满 `{S['res']}` 个" if 'res' in S else ''),
    ],
    watch=[('space', 'space', 'blue'), ('additionalRocks', 'additionalRocks', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记装满了几个背包；先算出每个背包的剩余空间并排序',
        'for space in sorted': '取下一个最小的剩余空间 `space = {space}`',
        'if additionalRocks < space': lambda S, B, r: (f'手里 `{S.additionalRocks}` < 需要 `{S.space}`：这个都填不满，更大的更不行 → ==break==' if S.additionalRocks < S.space else f'手里 `{S.additionalRocks}` >= 需要 `{S.space}`：够填满'),
        'res += 1': '填满一个：`res` → =={res}==',
        'additionalRocks -= space': '用掉 `{space}` 块：还剩 `{B.additionalRocks}` − `{space}` = =={additionalRocks}==',
        'return res': '最多能装满 =={res}== 个背包',
    },
    cards=dict(
        one_liner='先填剩余空间最小的背包，能填满的个数最多',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`capacity[i]` 是容量，`rocks[i]` 是已装石头数',
                 '再给 `additionalRocks` 块石头，可放进任意背包',
                 '求最多能装满几个背包；本视频 `→ 4`'],
        quote='由于背包的权重都是一样的，因此在这里就应该优先填满剩余空间小的背包，这样才能使得最终被填满的背包最多。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个背包「装满」价值一样，都算 1 个',
              '所以谁需要的石头少就先填谁',
              '剩余空间排序，一趟扣减，不够就停'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（存剩余空间列表）',
                 '不够填就 `break`：后面的空间只会更大',
                 '剩余空间为 0 的背包本来就是满的，会被直接计入',
                 '原文为 Python 2 风格，无需改动即可运行'],
    ),
)
