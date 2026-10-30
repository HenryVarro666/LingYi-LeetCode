CONFIG = dict(
    num=3075, title='幸福值最大化的选择方案', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 · 优先选大的',
    tags=['贪心与思维', '从最小/最大开始贪心', '难度分 1326'],
    code='''
class Solution:
    def maximumHappinessSum(self, happiness: List[int], k: int) -> int:
        happiness.sort(reverse=True)
        ans = 0
        for i, x in enumerate(happiness[:k]):
            if x <= i:
                break
            ans += x - i
        return ans
''',
    call='Solution().maximumHappinessSum([1,5,1,4,3], 4)',
    expect=9,
    views=[
        dict(type='text', fn=lambda S: (f"第 `{S['i']}` 个选走 `{S['x']}`，已被减 `{S['i']}` 次 → 实得 `max({S['x']} − {S['i']}, 0)`" if 'x' in S and 'i' in S else '先从大到小排序，只看前 k 个'), size=26),
        dict(type='array', var='happiness', pointers={'i': 'blue'}, h=260, label='happiness（降序）',
             dim=lambda S, i, v: i >= S['k'],
             color=lambda S, i, v: 'green' if 'i' in S and i < S['i'] else None),
    ],
    watch=['k', ('i', 'i', 'blue'), 'x', ('ans', 'ans', 'green')],
    captions={
        'happiness.sort': '==大的先选==：小的数反正会被减成 0，让大的少吃几次减法。排序后 `{happiness}`',
        'ans = 0': '`ans` 累计幸福值之和',
        'for i, x': '第 `{i}` 轮选 `{x}`：之前已选了 `{i}` 个孩子，它被减了 `{i}` 次',
        'if x <= i': lambda S, B, r: (f'`{S.x} <= {S.i}`：它已被减到 0，==后面更小的也是 0== → break' if S.x <= S.i
                                      else f'`{S.x} <= {S.i}` 不成立：还剩 `{S.x} − {S.i}` > 0，可以拿'),
        'ans += x - i': '`ans += {x} − {i}` → =={ans}==',
        'return ans': '最大幸福值之和 `{ans}`',
    },
    cards=dict(
        one_liner='优先选大的：小的反正会被减成 0',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`n` 个孩子有幸福值，选 `k` 轮，每选一个其余未选的幸福值减 1（最低为 0）',
                 '求选中孩子幸福值之和的最大值',
                 '示例：`[1,2,3], k=2` → `4`；本视频：`[1,5,1,4,3], k=4` → `9`'],
        quote='由于小的数减成 0 就不再减少了，优先选大的数更好。',
        quote_src='—— 灵茶山艾府题解',
        idea=['本质是选 `happiness` 最大的 `k` 个数求和',
              '顺序：大的先选。例 `2,1,1`：按 `2,1,1` 选得 2，按 `1,1,2` 只得 1',
              '第 `i` 个被选时已减 `i` 次，实得 `x − i`；`x <= i` 就可以停'],
        summary=['时间 `O(n log n)`，空间 `O(1)`（忽略排序）',
                 '易错：第 `i` 轮（从 0 开始）减的是 `i` 而不是 `i+1`',
                 '易错：`x <= i` 要 break（或取 max 0），不能加负数',
                 '原文提到：Python 的切片 `happiness[:k]` 可以用枚举代替'],
    ),
)
