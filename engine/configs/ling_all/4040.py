def _fv(v):
    return '∞' if v == inf else str(v)


def _item(S):
    x, a, i = S.get('x'), S.get('a'), S.get('i')
    if x is None or i is None or a is None:
        return ''
    ln = S.get('_line', 0)
    if ln in (11, 13) and x << a <= i:
        return f'乘法物品：体积 `{x}<<{a}` = ==`{x << a}`==，价值（操作次数）= ==`{a}`=='
    if ln in (18, 20) and a > 0 and x >> a <= i:
        return f'除法物品：体积 `{x}>>{a}` = ==`{x >> a}`==，价值（操作次数）= ==`{a}`=='
    return ''


def _fcolor(S, k, v):
    i, x, a = S.get('i'), S.get('x'), S.get('a')
    if i is None:
        return None
    if k == i:
        return 'yellow'
    ln = S.get('_line', 0)
    if a is not None and x is not None:
        if ln in (12, 13, 14):
            src = i - (x << a)
            if k == src and src >= 0:
                return 'blue'
        if ln in (17, 18, 19):
            src = i - (x >> a)
            if k == src and src >= 0:
                return 'blue'
    return None


CONFIG = dict(
    num=4040, title='构造子集和的最少操作次数 I', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='分组背包',
    tags=[],
    code='''
class Solution:
    def minOperations(self, nums: list[int], sum: int) -> int:
        f = [0] + [inf] * sum

        for x in nums:
            w = x.bit_length()  # x 的二进制长度
            for i in range(sum, 0, -1):
                # 回想一下，0-1 背包是选或不选，状态转移方程为 f[i] = min(f[i], f[i-物品体积] + 物品价值)
                # 本题是分组背包，要枚举选哪个物品（枚举乘了 a 次或者除了 a 次）
                a = 0
                while x << a <= i:
                    # 物品体积为 x<<a，价值为 a
                    f[i] = min(f[i], f[i - (x << a)] + a)
                    a += 1

                # 从小到大枚举 x>>a，方便在 x>>a > i 时跳出循环
                a = w - 1
                while a > 0 and x >> a <= i:
                    # 物品体积为 x>>a，价值为 a
                    f[i] = min(f[i], f[i - (x >> a)] + a)
                    a -= 1

        return -1 if f[sum] == inf else f[sum]
''',
    call='Solution().minOperations([5, 6], 4)',
    expect=3,
    skip=['a = 0', 'a += 1', 'a -= 1', 'w = x.bit_length', 'a = w - 1', 'for i in range'],
    max_steps=100,
    views=[
        dict(type='array', var='nums', pointers={'x': 'blue'}, label='nums', h=130, cell=90,
             color=lambda S, k, v: 'blue' if S.get('x') == v else None),
        dict(type='array', var='f', label='f[i]：恰好凑出体积 i 的最少操作次数（∞ = 凑不出）', h=240, cell=96,
             pointers={'i': 'pink'}, color=_fcolor),
        dict(type='text', fn=_item, size=26, h=60),
    ],
    watch=['x', ('i', 'i', 'pink'), 'a', ('f[i]', "f[i] if 'i' in dir() else ''", 'green')],
    captions={
        'f = [0]': '`f[0] = 0`：凑出 0 不需要操作；其余先设为 ∞（`f` 长度 `sum + 1` = {len(f)}）',
        'for x in nums': lambda S, B, r: (f'处理第 {S.nums.index(S.x) + 1} 组：`x = {S.x}`，它能变成 `x<<a`（乘 a 次）或 `x>>a`（除 a 次）' if 'i' not in B or B.get('x') != S.x else '所有组都处理完了'),
        'while x << a <= i': lambda S, B, r: (f'容量 `i = {S.i}`（倒序，保证每组至多选一个）：`{S.x} << {S.a} = {S.x << S.a}` ≤ `i`，乘法物品放得下，试试' if S.x << S.a <= S.i else f'容量 `i = {S.i}`（倒序，保证每组至多选一个）：`{S.x} << {S.a} = {S.x << S.a}` > `i`，乘法物品放不下；改枚举除法物品（`a` 从大到小，体积从小到大）'),
        'f[i] = min(f[i], f[i - (x << a)]': lambda S, B, r: f'乘 `{S.a}` 次：体积 `{S.x << S.a}`，`f[{S.i}] = min({_fv(B.f[S.i])}, f[{S.i - (S.x << S.a)}] + {S.a})` = =={_fv(S.f[S.i])}==',
        'while a > 0 and x >> a': lambda S, B, r: (f'`{S.x} >> {S.a} = {S.x >> S.a}` ≤ `i = {S.i}`：这个除法物品放得下，试试' if S.a > 0 and S.x >> S.a <= S.i else '除法物品枚举完（或已放不下），这个 `i` 处理完毕'),
        'f[i] = min(f[i], f[i - (x >> a)]': lambda S, B, r: f'除 `{S.a}` 次：体积 `{S.x >> S.a}`，`f[{S.i}] = min({_fv(B.f[S.i])}, f[{S.i - (S.x >> S.a)}] + {S.a})` = =={_fv(S.f[S.i])}==',
        'return -1': lambda S, B, r: (f'`f[{S.sum}] = {_fv(S.f[S.sum])}`，凑得出 → 最少操作 =={S.f[S.sum]}== 次' if S.f[S.sum] != inf else '`f[sum]` 仍是 ∞：凑不出，返回 -1'),
    },
    cards=dict(
        one_liner='每个数是一组物品：乘 a 次或除 a 次，每组至多选一个',
        complexity='时间 `O(n·sum·(log sum + log U))`，空间 `O(sum)`',
        problem=['一次操作把某元素 `x` 变成 `2x` 或 `floor(x/2)`，且每个元素先乘后除',
                 '求最少操作次数，使某个子集的和恰好等于 `sum`，否则返回 -1',
                 '示例：`nums=[10,2], sum=13` → `3`；本视频：`[5,6], sum=4` → `3`（5→1 两次，6→3 一次）'],
        quote='由于先乘再除没有意义，所以只需考虑只有乘法操作，或者只有除法操作。……这是标准的分组背包问题。分组背包只需在 0-1 背包的基础上，把「选或不选」改成「枚举选这一组内的哪个物品，或者一个都不选」。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个 `x` 只会变成 `x·2^a`（不超过 sum）或 `floor(x/2^a)`，物品个数只有 `O(log)`',
              '物品体积 = 变成的值，价值 = 操作次数 `a`；每组至多选一个',
              '`f[i]` = 凑出恰好 `i` 的最小操作数，`i` 倒序枚举，组内枚举选哪个物品'],
        summary=['时间 `O(n·sum·(log sum + log U))`，空间 `O(sum)`',
                 '`f[0] = 0`，其余是 ∞，最后 `f[sum]` 是 ∞ 就返回 -1',
                 '`i` 要倒序：不然同一组里会被选多次',
                 '体积 `x>>a` 从小到大枚举（`a` 从 `w-1` 往下），超过 `i` 就能跳出',
                 '本例只用到除法物品；乘法物品（如 `[10,2]` 里 2→8）在 `x<<a <= i` 循环里枚举。题解另有记忆化搜索写法 `dfs(i, s)`'],
    ),
)
