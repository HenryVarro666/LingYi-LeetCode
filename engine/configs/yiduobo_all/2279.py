CONFIG = dict(
    num=2279, title='装满石头的背包的最大数量', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='按剩余空间排序后遍历填充',
    tags=['灵神题单', '贪心与思维', '难度分 1249'],
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
    call='Solution().maximumBags([10,2,2,7,5,6], [2,2,0,6,1,6], 9)',
    expect=5,
    views=[
        dict(type='text', fn=lambda S: f"石头还剩 ==`{S['additionalRocks']}`== 块，已装满 `{S['res']}` 个背包" if 'res' in S else f"额外石头 `{S['additionalRocks']}` 块"),
        dict(type='array', var='capacity', label='capacity', h=130),
        dict(type='array', var='rocks', label='rocks', h=130),
        dict(type='array', var=lambda S: sorted(S['capacity'][k] - S['rocks'][k] for k in range(len(S['capacity']))),
             label='剩余空间（排序后）', h=190, pointers={'res': 'pink'},
             color=lambda S, i, v: 'green' if i < S.get('res', 0) else None),
    ],
    watch=[('additionalRocks', 'additionalRocks', 'yellow'), ('res', 'res', 'green'), 'space'],
    captions={
        'res = 0': '`res` 记录装满的背包数',
        'for space in sorted': '剩余空间排好序后，轮到空间为 `{space}` 的背包',
        'if additionalRocks < space': '石头 `{additionalRocks}` vs 空间 `{space}`：' + '{"不够装满 → 后面更大的也不行，退出" if additionalRocks < space else "够，装满它"}',
        'break': '剩余空间从小到大，这个都装不满，==后面更不行==',
        'res += 1': '装满一个：`res` → =={res}==',
        'additionalRocks -= space': '用掉 `{space}` 块，石头还剩 `{additionalRocks}`',
        'return res': '最多装满 `{res}` 个背包',
    },
    cards=dict(
        one_liner='谁离装满最近，先填谁',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`capacity[i]` 为背包容量，`rocks[i]` 为已装石头，另有 `additionalRocks` 块石头',
                 '石头可放入任意背包，求最多装满几个',
                 '本视频：`[10,2,2,7,5,6]`, `[2,2,0,6,1,6]`, 额外 `9` 块 → `5`'],
        quote='由于背包的权重都是一样的，因此在这里就应该优先填满剩余空间小的背包，这样才能使得最终被填满的背包最多。',
        quote_src='—— yiduobo 题解原文',
        idea=['每个背包的价值一样（装满就算 1 个）',
              '所以花最少石头装满的背包最划算',
              '按剩余空间排序，一趟遍历直到石头不够'],
        summary=['时间 `O(n log n)`，空间 `O(n)`（排序产生新列表）',
                 '易错点：`additionalRocks < space` 才退出，刚好相等还能装满',
                 '代码本身已是 Python 3 可运行写法，无需改动'],
    ),
)
