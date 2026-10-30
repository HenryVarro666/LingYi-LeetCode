CONFIG = dict(
    num=3861, title='容量最小的箱子', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='一次遍历 · 维护最小容量',
    code='''
class Solution:
    def minimumIndex(self, capacity: List[int], itemSize: int) -> int:
        min_c = inf
        ans = -1
        for i, c in enumerate(capacity):
            if itemSize <= c < min_c:
                min_c = c
                ans = i
        return ans
''',
    call='Solution().minimumIndex([6,3,5,4,5,7], 4)',
    expect=3,
    views=[
        dict(type='text', fn=lambda S: f"物品大小 `itemSize = {S['itemSize']}`，当前最小可用容量 `min_c = {S['min_c'] if 'min_c' in S and S['min_c'] != float('inf') else '∞'}`" if 'min_c' in S else f"物品大小 `itemSize = {S['itemSize']}`"),
        dict(type='array', var='capacity', pointers={'i': 'blue', 'ans': 'green'}, h=330, label='capacity',
             color=lambda S, k, v: 'green' if S.get('ans', -1) == k else None,
             dim=lambda S, k, v: v < S['itemSize']),
    ],
    watch=[('i', 'i', 'blue'), ('c', 'c', 'blue'), ('min_c', 'min_c', 'orange'), ('ans', 'ans', 'green')],
    captions={
        'min_c = inf': '`min_c`：目前找到的最小可用容量，先设为无穷大',
        'ans = -1': '`ans = -1`：还没找到能装的箱子',
        'if itemSize <= c < min_c': lambda S, B, r: (
            f'`{S.itemSize} <= {S.c} < {S.min_c}` → 成立：装得下，而且比之前的更小' if S.itemSize <= S.c < S.min_c
            else (f'`c = {S.c} < itemSize = {S.itemSize}`：装不下，跳过' if S.c < S.itemSize
                  else f'`c = {S.c} >= min_c = {S.min_c}`：能装但不比已有的小（相等时保留下标更小的），跳过')),
        'min_c = c': '更新最小可用容量：`min_c = {c}`',
        'ans = i': '记下下标：`ans = {i}`',
        'return ans': '遍历结束，容量最小的可用箱子下标是 =={ans}==',
    },
    cards=dict(
        one_liner='从左到右扫一遍，只记录目前最小的可用容量',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['`capacity[i]` 是箱子容量，物品大小 `itemSize`',
                 '`capacity[i] >= itemSize` 才能装；求装得下的箱子里容量最小的下标',
                 '容量相同取下标小的；没有就返回 `-1`',
                 '示例：`[1,5,3,7], 3` → `2`'],
        quote='从左到右遍历 capacity 的过程中，维护满足要求的最小容量，及其对应的下标。',
        quote_src='—— 灵茶山艾府题解',
        idea=['条件写成连比 `itemSize <= c < min_c`：既装得下，又严格更小',
              '用严格小于 `<`：容量相同的后者不会覆盖，自然保留下标最小的',
              '`ans` 初值 `-1`，一个都装不下时直接返回'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：比较 `c < min_c` 要用严格小于，否则相同容量会取到下标更大的',
                 '`min_c` 初值用 `inf`，保证第一个可用箱子一定能更新'],
    ),
)
