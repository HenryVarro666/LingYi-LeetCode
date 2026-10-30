CONFIG = dict(
    num=1561, title='你可以获得的最大硬币数目', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='排序 · 隔一个取一个',
    tags=['贪心与思维', '从最小/最大开始贪心', '难度分 1406'],
    code='''
class Solution:
    def maxCoins(self, piles: List[int]) -> int:
        piles.sort()
        return sum(piles[len(piles)//3::2])
''',
    call='Solution().maxCoins([2,4,1,2,7,8])',
    expect=9,
    views=[
        dict(type='array', var='piles', label='piles（升序）', h=260,
             color=lambda S, i, v: ('pink' if i < len(S['piles']) // 3 else ('green' if (i - len(S['piles']) // 3) % 2 == 0 else 'blue')) if S['_line'] >= 4 else None),
        dict(type='text', fn=lambda S: ('粉 = Bob 拿走的最少 `n/3` 堆，绿 = 我拿的，蓝 = Alice 拿的' if S['_line'] >= 4 else '先按数量从小到大排序'), size=24),
    ],
    watch=[('piles', 'piles', 'blue')],
    captions={
        'piles.sort': '排序：`{piles}`。Bob 总拿最少的，先把最小的 `n/3` 堆给他',
        'return sum': lambda S, B, r: f'从下标 `{len(S.piles)//3}` 开始隔一个取：`{S.piles[len(S.piles)//3::2]}` → 和 =={r}==',
    },
    cards=dict(
        after=[dict(heading='为什么这样分最优', lines=['每轮三堆：最大给 Alice、次大给我、最小给 Bob', '例 `[1,2,2,4,7,8]`：第一轮 (2,7,8)，我拿 7', '第二轮 (1,2,4)，我拿 2，共 9', '升序下标 `n/3` 起隔一个取：`2, 7`，同一个答案']),
               dict(heading='两种等价写法', lines=['降序后取下标 `1,3,5,...,2m-1`（`m = n/3`）', '升序后取下标 `m, m+2, ..., n-2`', '切片 `piles[m::2]` 正好覆盖']) ],
        one_liner='最少的给 Bob，剩下的我取次大，Alice 取最大',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['`3n` 堆硬币，每轮选 3 堆：Alice 取最多，我取第二多，Bob 取最少',
                 '求我最多能拿多少硬币',
                 '示例：`[2,4,1,2,7,8]` → `9`（7 + 2）'],
        quote='由于 Bob 总是最后取，每一轮，我们可以把（剩余硬币堆中的）最少的那一堆硬币给 Bob。',
        quote_src='—— 灵茶山艾府题解',
        idea=['Alice 先取，我们取不到最大值，但能取到次大值',
              '第三大的给 Alice，我们取第四大，依此类推',
              '降序取下标 `1,3,5,...`；升序就是从 `n/3` 起隔一个取'],
        summary=['时间 `O(n log n)`，空间 `O(1)`',
                 '升序写法：`piles[len(piles)//3::2]`，起点是 `n/3`',
                 '降序写法：取下标 `1,3,5,...,2m-1`，`m = n/3`',
                 '相似题：3457 吃披萨'],
    ),
)
