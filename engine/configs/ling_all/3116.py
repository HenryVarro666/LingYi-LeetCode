def _amounts(S):
    m = S.get('m')
    return list(range(1, m + 1)) if m else []


def _hit(S, i, v):
    return any(v % x == 0 for x in S['a'])


def _cnt_text(S):
    m = S.get('m')
    if m is None or 'cnt' not in S:
        return '二分猜答案 `m`：数一数 ≤ m 的金额有几个，够 `k` 个就说明 m 不小'
    ok = S['cnt'] >= S['k']
    return f"猜 `m = {m}`：容斥算得 ≤ m 的金额共 ==`{S['cnt']}`== 个，`k = {S['k']}` → " + ('==够了==' if ok else '==不够==')


CONFIG = dict(
    num=3116, title='单面值组合的第 K 小金额', difficulty='Hard', category='二分算法',
    author='灵茶山艾府', technique='二分答案 + 容斥原理（子集 lcm）',
    tags=['数学算法', '难度分 2387'],
    setup='lcm = math.lcm',
    code='''
class Solution:
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        a = []
        coins.sort()  # 排序后，能整除 x 的数都在 a 中
        for x in coins:
            if all(x % y for y in a):
                a.append(x)

        subset_lcm = [1] * (1 << len(a))
        for i, x in enumerate(a):
            bit = 1 << i
            for mask in range(bit):
                # 刷表法 DP，在 lcm(mask) 的基础上添加 coins[i]
                subset_lcm[bit | mask] = lcm(subset_lcm[mask], x)

        def check(m: int) -> bool:
            cnt = 0
            for i in range(1, len(subset_lcm)):  # 枚举所有非空子集
                cnt += m // subset_lcm[i] if i.bit_count() % 2 else -(m // subset_lcm[i])
            return cnt >= k

        return bisect_left(range(a[0] * k), True, k, key=check)
''',
    call='Solution().findKthSmallest([4, 6, 3], 7)',
    expect=15,
    views=[
        dict(type='array', var='coins', label='coins（排序后，橙 = 被丢掉）', h=120, cell=58,
             color=lambda S, i, v: 'orange' if v not in S.get('a', []) and i < len(S['coins']) and 'a' in S and S.get('_line', 0) > 7 else None),
        dict(type='array', var='a', label='a：留下的面额', h=120, cell=58),
        dict(type='array', var='subset_lcm', label='subset_lcm[mask]：下标是子集的二进制表示', h=165, cell=58,
             pointers={'(i if _line < 16 else None)': 'blue'},
             color=lambda S, i, v: 'green' if i == S.get('i') and S.get('_line', 0) > 18 else None),
        dict(type='array', var=_amounts, label='金额 1..m（绿 = 能被某个硬币凑出）', h=150, cell=50, index=False,
             color=lambda S, i, v: 'green' if _hit(S, i, v) else None),
        dict(type='text', fn=_cnt_text, size=26, h=90),
    ],
    watch=['k', 'm', 'i', ('cnt', 'cnt', 'green')],
    captions={
        'coins.sort()': '先排序：小的在前，后面才能判断「是不是前面某个数的倍数」',
        'if all(x % y for y in a)': lambda S, B, r: (f'`{S.x}` 对 a 里每个 y 都有 `x % y ≠ 0` → ==是，是新的独立面额==' if all(S.x % y for y in S.a)
                                                    else f'`{S.x}` 是 a 里某个数的倍数 → 它能凑的金额别人都能凑，==丢掉=='),
        'a.append(x)': '`{x}` 不是别人的倍数 → 放进 `a`，现在 a = {a}',
        'subset_lcm = [1]': '`a` 有 {len(a)} 个数 → 子集共 `2^{len(a)}` 个，用二进制 mask 表示；空集的 lcm 记为 1',
        'subset_lcm[bit | mask] =': '`mask` 的子集再加上 `{x}` → 新子集 `{bit | mask}`，`lcm = lcm({subset_lcm[mask]}, {x}) = {subset_lcm[bit | mask]}`',
        'cnt += m //': lambda S, B, r: (
            f"子集 `{S.i}` 有 {S.i.bit_count()} 个数，lcm = {S.subset_lcm[S.i]}：≤ {S.m} 的公倍数有 `{S.m // S.subset_lcm[S.i]}` 个，"
            + ('奇数个 → ==加上==' if S.i.bit_count() % 2 else '偶数个 → ==减掉==（容斥去重）')
            + f'，`cnt` = {S.cnt}'),
        'return cnt >= k': '`cnt = {cnt}`，`k = {k}` → ==`{cnt >= k}`==：{"m 够大，答案 ≤ m，二分区间往左缩" if cnt >= k else "m 太小，答案 > m，二分区间往右缩"}',
        'return bisect_left': '在 `[k, {a[0] * k})` 上二分：找最小的 `m` 使 `check(m)` 为真（下面每一轮是一次猜测）',
    },
    skip=['for i in range(1, len(subset_lcm))', 'cnt = 0', 'bit = 1 << i', 'for mask in range(bit)', 'for i, x in enumerate(a)', 'for x in coins'],
    max_steps=90,
    cards=dict(
        one_liner='第 k 小 = 最小的 m，使得 ≤ m 的金额至少 k 个',
        complexity='时间 `O(2^t (log M + log mk))`，空间 `O(2^t)`',
        problem=['给出若干面额的硬币，每次只能用==同一种==面额，金额是它的倍数',
                 '所有硬币能凑出的金额合起来，求第 `k` 小的金额',
                 '示例：`coins=[3,6,9], k=3` → `9`；本视频：`[4,6,3], k=7` → `15`'],
        quote='第 k 小等价于：求最小的 m，满足 ≤ m 的数至少有 k 个。',
        quote_src='—— 灵茶山艾府题解',
        idea=['m 越大，≤ m 的金额越多 → 有单调性，==二分猜答案==',
              '≤ m 中面额 x 的倍数有 `m // x` 个，但公倍数会重复算 → ==容斥原理==',
              '枚举非空子集 T，贡献 `(-1)^(|T|-1) · m // lcm(T)`，lcm 用刷表法预处理'],
        after=[dict(heading='三种写法', lines=[
            '优化前：check 里现算子集 lcm，lcm 超过 m 就 break',
            '优化一：预处理 `subset_lcm`，check 只做加减',
            '优化二（本视频）：先删掉别人的倍数，子集数大大减少'])],
        summary=['二分区间 `[k, min·k)`：k-1 一定不行，`min(coins)·k` 一定可行',
                 '二分出的答案一定是某个硬币的倍数（反证法）',
                 '`a` 最多留下约 13 个数，`2^t` 可以接受',
                 '`bit_count()` 判断子集大小的奇偶，决定加还是减'],
    ),
)
