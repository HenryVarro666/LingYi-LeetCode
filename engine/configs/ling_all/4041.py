def _fcolor(S, i, v):
    if S.get('_line') is None or 'items' not in S or 'i' not in S:
        return None
    if i == S['i']:
        return 'yellow'
    if S.get('v') is not None and S.get('v') <= S['i'] and i == S['i'] - S['v'] and S.get('_line') in (22, 23, 24):
        return 'blue'
    return None


def _items_txt(S):
    if 'items' in S:
        return '当前这一组：' + '，'.join(f'体积 =={v}== 代价 {c}' for v, c in S['items'])
    if 'costs' in S:
        return '正在生成这一组：' + '，'.join(f'体积 =={v}== 代价 {c}' for v, c in sorted(S['costs'].items()))
    return '分组背包：每个 `x` 是一组，每组至多选一个物品'


CONFIG = dict(
    num=4041, title='构造子集和的最少操作次数 II', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='分组背包',
    code='''
class Solution:
    def minOperations(self, nums: list[int], sum: int) -> int:
        f = [0] + [inf] * sum

        for x in nums:
            # 生成这一组的所有物品，相同体积的物品，只保留价值最小的物品
            costs = defaultdict(lambda: inf)
            a = 0
            while x >> a:
                b = 0
                while x >> a << b <= sum:
                    v = x >> a << b
                    costs[v] = min(costs[v], a + b)
                    b += 1
                a += 1

            # 按照体积从小到大排序，方便跳出循环
            items = sorted(costs.items())

            for i in range(sum, 0, -1):
                for v, c in items:
                    if v > i:
                        break
                    f[i] = min(f[i], f[i - v] + c)  # 手写 min 更快，见【Python3 更快的写法】

            if f[sum] == 0:
                return 0

        return -1 if f[sum] == inf else f[sum]
''',
    call='Solution().minOperations([3, 2], 4)',
    expect=1,
    skip=['b += 1', 'a += 1', 'b = 0', 'a = 0', 'v = x >> a << b', 'for v, c in items', 'for i in range', 'for x in nums', 'if v > i', 'while x >> a:', 'costs = defaultdict', 'items = sorted'],
    views=[
        dict(type='array', var='nums', label='nums', h=160, cell=80, pointers={}, color=lambda S, i, v: 'blue' if S.get('x') == v and 'x' in S else None),
        dict(type='text', fn=_items_txt, size=24, h=90),
        dict(type='array', var='f', label='f[i]：凑出体积 i 的最少操作次数（黄 = 正在更新，蓝 = f[i-v]）', h=260, cell=80, pointers={'i': 'yellow'}, color=_fcolor,
             fmt=lambda v: '∞' if v == inf else str(v)),
    ],
    watch=['x', 'a', 'b', 'v', 'c', 'i'],
    max_steps=90,
    captions={
        'f = [0]': '`f[i]` = 恰好凑出体积 `i` 的最少操作次数；`f[0] = 0`，其余先设为 ∞',
        'costs = defaultdict': '处理 `x = {x}`：把它能变成的所有数收集到 `costs`（==体积 → 最小代价==）',
        'while x >> a:': lambda S, B, r: (f'`x >> {S.a}` = {S.x >> S.a} > 0 → 还能再除一次' if (S.x >> S.a) else f'`x >> {S.a}` = 0 → 不用再除了'),
        'while x >> a << b': lambda S, B, r: (f'先右移 {S.a} 次再左移 {S.b} 次 = `{S.x >> S.a << S.b}` ≤ sum={S.sum} → 这个数有用' if (S.x >> S.a << S.b) <= S.sum
                                             else f'`{S.x >> S.a << S.b}` > sum={S.sum} → ==再乘也只会更大==，停'),
        'costs[v] = min': '体积 `{v}` 需要 `a+b` = {a}+{b} = {a+b} 次操作；重复体积只留最小的 → `costs[{v}] = {costs[v]}`',
                'break': '物品体积 `{v} > {i}` → 放不下，后面的更大，==直接 break==',
        'f[i] = min': '体积 `{v}` ≤ `{i}`：`f[{i}] = min({B.f[i]}, f[{i}-{v}] + {c})` = =={f[i]}==',
        'if f[sum] == 0': lambda S, B, r: ('`f[sum] = 0`：不用操作就能凑出 sum → 直接返回 0' if S.f[S.sum] == 0 else f'`f[sum] = {S.f[S.sum]}`，不是 0：后面的数可能让它更小，继续下一个数'),
        'return -1 if': '`f[sum] = {f[sum]}` → 答案 =={ret}==',
    },
    cards=dict(
        one_liner='先除后乘最优，转化成分组背包：每个数是一组',
        complexity='时间 `O(n·sum·log U·log sum)`，空间 `O(sum)`',
        problem=['给 `nums` 和 `sum`，每次操作把一个数 `x` 换成 `2x` 或 `floor(x/2)`',
                 '求最少操作次数，使得某个子集的和恰好为 `sum`；做不到返回 -1',
                 '本视频：`nums=[3,2], sum=4` → `1`（3 + 1，把 2 除成 1）'],
        quote='乘法操作后面跟着除法操作是没有意义的，白白浪费操作次数。所以对于同一个数，最优操作顺序为：先执行若干次（可能零次）除法操作，再执行若干次（可能零次）乘法操作。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`x` 变成 `(x >> a) << b`，代价 `a + b`；不同的体积只有 `O(log x · log sum)` 个',
              '每个数是一组物品，==每组至多选一个==，要体积和恰好为 `sum` → 分组背包',
              '在 0-1 背包上，把「选或不选」换成「枚举选组内哪个物品」，`i` 倒序枚举'],
        summary=['时间 `O(n·sum·log U·log sum)`，空间 `O(sum)`',
                 '相同体积只留代价小的（如 6 先除后乘还是 6）',
                 '`i` 要倒序，物品按体积排序以便 break；`f[sum] == 0` 可提前返回',
                 '优化前写法是直接在 `i` 循环里枚举 `(a, b)`，这里用的是先去重再枚举的优化写法',
                 '前置：4040（只能先乘后除）、0-1 背包'],
    ),
)
