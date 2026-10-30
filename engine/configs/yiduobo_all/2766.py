CONFIG = dict(
    num=2766, title='重新放置石块', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='集合记录位置 · 移除起点加入终点',
    tags=[],
    code='''
class Solution(object):
    def relocateMarbles(self, nums, moveFrom, moveTo):
        pos = set(nums)
        for f, t in zip(moveFrom, moveTo):
            pos.remove(f)
            pos.add(t)

        return sorted(list(pos))
''',
    call='Solution().relocateMarbles([1,1,3,3,6], [1,3], [2,2])',
    expect=[2, 6],
    views=[
        dict(type='array', var='nums', label='nums（初始位置，可能重复）', h=170),
        dict(type='array', var=lambda S: [f'{a}→{b}' for a, b in zip(S['moveFrom'], S['moveTo'])], label='每次操作 f→t（蓝 = 正在做的）', h=170,
             color=lambda S, i, v: 'blue' if 'f' in S and v == f"{S['f']}→{S['t']}" else None),
        dict(type='set', var='pos', label='pos：当前有石块的位置', h=260, fmt=lambda x: str(x)),
    ],
    watch=[('f', 'f', 'blue'), ('t', 't', 'pink')],
    captions={
        'pos = set(nums)': '`nums` 里有重复位置，转成集合自动合并：`pos = {pos}`',
        'for f, t in zip': lambda S, B, r: ('所有移动都处理完了' if 'f' in B and S.f == B.f and S.t == B.t
                                            else f'这次移动：`{S.f}` → `{S.t}`'),
        'pos.remove(f)': '把 `{f}` 从集合中移除：这个位置的石块都要走了',
        'pos.add(t)': '把 `{t}` 加入集合：`{t}` 处现在有石块了 → `pos = {pos}`',
        'return sorted': '排序后返回 `{sorted(list(pos))}`',
    },
    cards=dict(
        one_liner='只记「哪些位置有石块」，移动就是删起点、加终点',
        complexity='时间 `O(n log n + m)`，空间 `O(n)`',
        problem=['`nums` 是石块位置，按顺序把 `moveFrom[i]` 处所有石块移到 `moveTo[i]`',
                 '返回最后有石块的位置（升序）',
                 '示例：`[1,1,3,3]`，`[1,3]→[2,2]` → `[2]`；本视频用 `[1,1,3,3,6]`'],
        quote='使用集合记录当前有石块的位置，接下来对于每次移动操作，只需将moveFrom中的位置从集合中移除，然后将moveTo中的位置加入到集合中就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['集合天然去重，同一位置的多块石头只算一个位置',
              '每次操作：`remove(f)`、`add(t)`',
              '最后把集合转列表排序'],
        summary=['时间 `O(n log n + m)`，空间 `O(n)`',
                 '`add(t)` 在 `remove(f)` 之后：`f == t` 时位置不会丢',
                 '代码与原文一致，无需改动',
                 '对比灵神：思路相同；灵神强调「不关心每个位置有几块」，yiduobo 直接给出集合操作'],
    ),
)
