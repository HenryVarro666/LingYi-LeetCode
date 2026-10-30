B1 = [2, 3, 5, 2, 3, 9]
B2 = [1, 4, 5, 1, 4, 9]


def _tail(S):
    if 'mn' not in S:
        return ''
    a = S['a']
    h = len(a) // 2
    return f"中介 `mn = {S['mn']}`，单次代价上限 `2×mn = {2 * S['mn']}`；只取前一半 `a[:{h}] = {a[:h]}`"


CONFIG = dict(
    num=2561, title='重排水果', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='抵消交集 · 排序取最小一半 · 中介交换',
    tags=['贪心与思维', '难度分 2222'],
    code='''
class Solution:
    def minCost(self, basket1: List[int], basket2: List[int]) -> int:
        cnt = defaultdict(int)
        for x, y in zip(basket1, basket2):
            cnt[x] += 1
            cnt[y] -= 1

        a = []
        for x, c in cnt.items():
            if c % 2:
                return -1
            a.extend([x] * (abs(c) // 2))

        a.sort()
        mn = min(cnt)

        return sum(min(x, mn * 2) for x in a[:len(a) // 2])
''',
    call=f'Solution().minCost({B1}, {B2})',
    expect=3,
    skip=['cnt = defaultdict'],
    views=[
        dict(type='array', var='basket1', label='basket1', cell=70, h=150),
        dict(type='array', var='basket2', label='basket2', cell=70, h=150),
        dict(type='map', var='cnt', label='cnt[v] = basket1 中个数 − basket2 中个数（交集互相抵消）', font=26, h=230,
             fmt=lambda k, v: f'{k}: {v}'),
        dict(type='array', var=lambda S: S.get('a'), label='a：需要交换的那一半元素（正负两边合在一起）', cell=70, h=150),
        dict(type='text', fn=_tail, size=26),
    ],
    watch=[('mn', 'mn', 'blue'), ('x', 'x', 'yellow'), ('c', 'c', 'pink')],
    captions={
        'cnt[x] += 1': '`basket1` 的 `{x}` 记 +1',
        'for x, y in zip': lambda S, B, r: ('两个数组都扫完了，`cnt` 里剩下的非零项就是要交换的数' if (S.get('x'), S.get('y')) == (B.get('x'), B.get('y'))
                                            else f'同时取两个篮子的第 k 个：`x = {S.x}`（basket1），`y = {S.y}`（basket2）'),
        'cnt[y] -= 1': lambda S, B, r: (f'`basket2` 的 `{S.y}` 记 −1：同一个数两边都有，==互相抵消==，`cnt[{S.y}] = 0`' if S.cnt[S.y] == 0
                                        else f'`basket2` 的 `{S.y}` 记 −1：`cnt[{S.y}] = {S.cnt[S.y]}`'),
        'a = []': '准备 `a`：收集「需要交换的那一半」',
        'for x, c in cnt.items()': lambda S, B, r: ('`cnt` 看完了，接着排序' if (S.get('x'), S.get('c')) == (B.get('x'), B.get('c'))
                                                    else f'逐个看 `cnt`：`x = {S.x}`，`c = {S.c}`（两边个数之差）'),
        'if c % 2': lambda S, B, r: (f'`c = {B.c}` 是奇数：这个数无法在两边均分 → 返回 `-1`' if B.c % 2
                                     else (f'`c = 0`：两边一样多，不用换' if B.c == 0 else f'`c = {B.c}` 是偶数：多出来的 `|c|` 个里==一半==要换到另一边')),
        'a.extend': lambda S, B, r: (f'`{S.x}` 需要交换 `|c|/2 = {abs(S.c)//2}` 个，放进 `a`：正负两边合并也不影响，只关心「要换的那一半」' if S.c else f'`{S.x}` 两边个数相同（`c = 0`），不用交换'),
        'a.sort()': '`a` 从小到大排序：`{a}`（前一半 = 两个数组里要换的数中最小的一半）',
        'mn = min(cnt)': '`mn = {mn}`：全局最小值当==中介==，交换 `a_i, b_i` 也可以各和 `mn` 换一次，代价 `2×mn`',
        'return sum': lambda S, B, r: (f'每个要换的数代价 `min(x, 2×mn)`，只累加最小的一半 `{B.a[:len(B.a)//2]}` → 总代价 =={r}==')
    },
    cards=dict(
        one_liner='去掉交集，交换的最小代价就是最小那一半数',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['两个果篮各 `n` 个水果，交换 `basket1[i]` 和 `basket2[j]` 的代价是 `min(两者)`',
                 '求让两个果篮排序后相等的最小总代价，不可能返回 `-1`',
                 '示例：`[4,2,2,2]`、`[1,4,1,2]` → `1`'],
        quote='考虑 a 中最小的数，找 b 中的哪个数交换，是最合适的？……把 a 从小到大排序，b 从大到小排序，然后交换 a_i 和 b_i。',
        quote_src='—— 灵茶山艾府题解（交换论证法）',
        idea=['先抵消交集；剩余每个数的个数差必须是偶数，一半换出去',
              '小的和大的配对，代价是 `min(a_i, b_i)`；也可借全局最小值 `mn` 当中介，代价 `2·mn`',
              '`min(a_i, b_i)` 恰好取遍 `a+b` 中最小的一半 → 拼起来排序取前一半即可'],
        summary=['时间 `O(n log n)`，空间 `O(n)`；用快速选择可做到 `O(n)`',
                 '易错：`mn` 要取两个数组的全局最小值，不是 `a` 的最小值',
                 '另一种写法：`a`、`b` 分开，`a` 升序、`b` 降序配对，累加 `min(x, y, 2·mn)`',
                 '原理：交换论证法 + 排序不等式'],
    ),
)
