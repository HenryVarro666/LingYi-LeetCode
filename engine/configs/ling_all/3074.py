CONFIG = dict(
    num=3074, title='重新分装苹果', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='先装大箱子',
    tags=['贪心与思维', '从最小/最大开始贪心', '难度分 1198'],
    code='''
class Solution:
    def minimumBoxes(self, apple: List[int], capacity: List[int]) -> int:
        s = sum(apple)  # 把所有苹果堆在一起
        capacity.sort(reverse=True)  # 先装大箱子，再装小箱子
        for i, x in enumerate(capacity):
            s -= x
            if s <= 0:  # 所有苹果都装入了箱子
                return i + 1  # 从 0 到 i 有 i+1 个箱子
''',
    call='Solution().minimumBoxes([3,2,4,1], [2,5,1,4,3])',
    expect=3,
    views=[
        dict(type='array', var='apple', label='apple（包裹）', h=170),
        dict(type='array', var='capacity', label='capacity（箱子，降序后逐个装）', pointers={'i': 'blue'}, h=250,
             color=lambda S, i, v: ('green' if 'i' in S and i <= S['i'] else None),
             dim=lambda S, i, v: 'i' in S and i > S['i']),
        dict(type='text', fn=lambda S: (f"还剩 ==`{S['s']}`== 个苹果没装" if S['s'] > 0 else f"苹果装完了，用了 ==`{S['i'] + 1}`== 个箱子") if 'i' in S else (f"苹果总数 `s = {S['s']}`" if 's' in S else ''), size=34, h=110),
    ],
    watch=[('s', 's', 'yellow'), ('i', 'i', 'blue'), ('x', 'x', 'cyan')],
    captions={
        's = sum(apple)': '同一包裹的苹果能拆开装 → 不用管包裹，==总数 `{s}`== 一堆就行',
        'capacity.sort': '想少用箱子就先用大的：容量排成 `{capacity}`',
        's -= x': '装进第 `{i}` 个箱子（容量 `{x}`）：还剩 `{B.s}` − `{x}` = =={s}==',
        's <= 0': lambda S, B, r: (f'`s = {S.s} <= 0`：苹果全装完了 → 停' if S.s <= 0 else f'`s = {S.s} > 0`：还有苹果，换下一个更小的箱子'),
        'return i + 1': '下标 0 到 `{i}` 共 `{i+1}` 个箱子 → 返回 =={i+1}==',
    },
    cards=dict(
        one_liner='苹果能拆开装，那就先把最大的箱子用掉',
        complexity='时间 `O(n+m log m)`，空间 `O(1)`',
        problem=['`n` 个包裹装着 `apple[i]` 个苹果，`m` 个箱子容量 `capacity[i]`',
                 '同一个包裹的苹果可以放进不同箱子，求最少用几个箱子',
                 '本视频：`apple=[3,2,4,1]`，`capacity=[2,5,1,4,3]` → `3`'],
        quote='既然同一个包裹中的苹果可以分装到不同的箱子中，那就先把所有苹果堆在一起，然后一个个地装箱。为了少用箱子，要先装大箱子，再装小箱子。',
        quote_src='—— 灵茶山艾府题解',
        idea=['包裹边界没意义，只剩一个数：苹果总数 `s`',
              '容量降序排好，一个个减掉：`s` 减到 `<= 0` 就是答案',
              '大箱子优先，用的个数一定最少'],
        summary=['时间 `O(n+m log m)`，主要是排序，空间 `O(1)`',
                 '题目保证装得下，所以循环里一定会返回',
                 '返回 `i + 1`：下标从 0 开始，别忘了加 1',
                 '同类：从最大/最小开始贪心（灵神贪心题单 §1.1）'],
    ),
)
