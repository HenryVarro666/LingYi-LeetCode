CONFIG = dict(
    num=2279, title='装满石头的背包的最大数量', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='按剩余空间从小到大装（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1249'],
    code='''
class Solution:
    def maximumBags(self, capacity: List[int], rocks: List[int], additionalRocks: int) -> int:
        ans = 0
        for i in range(len(capacity)):
            capacity[i] -= rocks[i]
        capacity.sort()  # 先装剩余最小的
        for leftSpace in capacity:
            if leftSpace > additionalRocks:  # 无法装满，那后续也无法装满（因为排序了）
                break  # 直接退出
            ans += 1
            additionalRocks -= leftSpace
        return ans
''',
    call='Solution().maximumBags([2,3,4,5,9], [1,2,4,4,3], 3)',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: f"额外石头还剩 ==`{S['additionalRocks']}`== 块，已装满 `{S['ans']}` 个背包"),
        dict(type='array', var='rocks', label='rocks（已装）', h=140),
        dict(type='array', var='capacity', label='capacity（先变成剩余空间，排序后从小到大装）', h=190,
             pointers={'ans': 'pink'},
             color=lambda S, i, v: ('blue' if S.get('_line', 0) <= 5 and i == S.get('i') else 'green' if S.get('_line', 0) >= 7 and i < S.get('ans', 0) else None)),
    ],
    watch=[('additionalRocks', 'additionalRocks', 'yellow'), ('ans', 'ans', 'green'), 'leftSpace'],
    captions={
        'ans = 0': '`ans` 记录装满的背包数',
        'capacity[i] -= rocks[i]': '背包 `{i}` 还差 `{capacity[i]}` 块才满：`capacity[{i}] = {capacity[i]}`',
        'capacity.sort()': '先装剩余最小的：排序后 `{capacity}`',
        'for leftSpace in capacity': '轮到剩余空间 `{leftSpace}` 的背包',
        'if leftSpace >': '剩余 `{leftSpace}` vs 手上石头 `{additionalRocks}`：' + '{"装不满，后面更大也装不满 → 退出" if leftSpace > additionalRocks else "够装，装满它"}',
        'break': '空间只会越来越大，==后面都装不满== → 直接退出',
        'ans += 1': '装满一个：`ans` → =={ans}==',
        'additionalRocks -= leftSpace': '用掉 `{leftSpace}` 块，石头还剩 `{additionalRocks}`',
        'return ans': '最多装满 `{ans}` 个背包',
    },
    cards=dict(
        one_liner='先把剩余空间最小的背包装满',
        complexity='时间 `O(n log n)`，空间 `O(1)`（原地排序）',
        problem=['`capacity[i]` 是背包容量，`rocks[i]` 是已装石头数，另有 `additionalRocks` 块石头可放进任意背包',
                 '求最多能装满几个背包',
                 '示例：`capacity=[2,3,4,5,9]`, `rocks=[1,2,4,4,3]`, 额外 `3` 块 → `4`'],
        quote='先装剩余最小的；无法装满，那后续也无法装满（因为排序了），直接退出。',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['每个背包装满需要 `capacity - rocks` 块，先把它算出来',
              '石头一样，当然先填需求小的，这样能满足的背包最多',
              '排序后一旦某个装不满，后面更大的更装不满'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python',
                 '时间 `O(n log n)`，空间 `O(1)`',
                 '易错点：要先把容量减掉已装的，再排序',
                 '剩余空间为 0 的背包不用石头，也计入答案',
                 '同类：从最小/最大开始贪心'],
    ),
)
