def _free(S):
    c = S.get('cost')
    if c is None or c != sorted(c, reverse=True):
        return set()
    return set(range(2, len(c), 3))


CONFIG = dict(
    num=2144, title='打折购买糖果的最小开销', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='从大到小 · 买二送一',
    tags=['贪心与思维', '难度分 1261'],
    code='''
class Solution:
    def minimumCost(self, cost: list[int]) -> int:
        cost.sort(reverse=True)
        return sum(cost) - sum(cost[2::3])  # 买两个送一个
''',
    call='Solution().minimumCost([6,5,7,9,2,2])',
    expect=23,
    views=[
        dict(type='array', var='cost', label='cost（从大到小排序后，每三个一组：买、买、送）', h=230, cell=100,
             color=lambda S, i, v: 'green' if i in _free(S) else None),
        dict(type='text', h=110, size=30,
             fn=lambda S: (f"总价 `{sum(S['cost'])}`，免费的是 `cost[2::3]` = `{S['cost'][2::3]}`，和为 `{sum(S['cost'][2::3])}`"
                           if S['cost'] == sorted(S['cost'], reverse=True) else '先从大到小排序')),
    ],
    watch=[],
    captions={
        'cost.sort(reverse=True)': '从大到小排序：`{cost}`。最贵的两个只能==自己买==',
        'return sum(cost)': '买两个送一个：下标 2、5、8…… 的糖果免费，它们是 `{cost[2::3]}`；总价 `{sum(cost)}` − 免费 `{sum(cost[2::3])}` = `{ret}`',
    },
    max_steps=20,
    cards=dict(
        after=[dict(heading='为什么上界能取到', lines=['排序后每三个一组：`a1, a2` 买，`a3` 免费', '`a3 <= a2 <= a1`，满足免费的限制', '所以免费的价格和恰好 = `a3 + a6 + ...`', '上界和构造相等 → 贪心正确'])],
        one_liner='总开销 = 总价 − 免费糖果价格和，让免费的尽量贵',
        complexity='时间 `O(n log n)`，空间 `O(1)`',
        problem=['买两个糖果可以免费得一个，免费的价格 ==不超过买的两个中较小者==',
                 '求拿到所有糖果的最小总开销',
                 '本视频：`cost = [6,5,7,9,2,2]` → `23`'],
        quote='总开销 = 所有糖果的价格和 - 免费糖果的价格和。……最小化总开销，等价于最大化免费糖果的价格和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一个免费的 `f1` 之前必须买了两个不小于它的，所以 `f1 <= a3`（第三大）',
              '第二个免费的前面至少有 5 个不小于它的，所以 `f2 <= a6`，依此类推 `fi <= a3i`',
              '上界可以取到：从大到小，买二送一'],
        summary=['时间 `O(n log n)`，瓶颈是排序；空间 `O(1)`（忽略排序栈）',
                 '`cost[2::3]` 就是排名第 3、6、9…… 大的糖果',
                 '糖果不足 3 个时，切片为空，全部要买（如 `[5,5]` → 10）',
                 '写法二：升序排序后从末尾每次取两个，跳过一个，思路相同'],
    ),
)
