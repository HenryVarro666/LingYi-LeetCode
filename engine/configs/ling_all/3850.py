NUMS, K = [2, 2], 1


def _I(S, k):
    return S['_inner'].get(k)


def _txt(S):
    inner = S['_inner']
    if 'e2' not in inner or 'i' not in inner:
        if 'es' in S:
            return '每个 `nums[x]` 拆成 `(x, y, z)` = 2、3、5 的个数；`k` 倒着乘除，目标是变成 1'
        return ''
    e2, e3, e5 = inner['e2'], inner['e3'], inner['e5']
    cur = f'`k` 此刻 = 2^{e2} × 3^{e3} × 5^{e5}'
    if e2 == e3 == e5 == 0:
        cur += ' = ==1=='
    return cur + ('；nums ==处理完毕==' if inner['i'] < 0 else f'；还要处理 `nums[0..{inner["i"]}]`')


CONFIG = dict(
    num=3850, title='统计结果等于 K 的序列数目', difficulty='Hard', category='链表、二叉树与回溯',
    author='灵茶山艾府', technique='质因数分解 + 记忆化搜索',
    tags=['灵神题单', '动态规划', '难度分 1965'],
    code='''
class Solution:
    # 返回 k 中的质因子 2,3,5 的个数，以及 k 是否只包含 <= 5 的质因子
    def primeFactorization(self, k: int) -> Tuple[Tuple[int, int, int], bool]:
        e2 = (k & -k).bit_length() - 1
        k >>= e2

        e3 = 0
        while k % 3 == 0:
            e3 += 1
            k //= 3

        e5 = 0
        while k % 5 == 0:
            e5 += 1
            k //= 5

        return (e2, e3, e5), k == 1

    def countSequences(self, nums: List[int], k: int) -> int:
        (e2, e3, e5), ok = self.primeFactorization(int(k))
        if not ok:  # k 有大于 5 的质因子
            return 0

        es = [self.primeFactorization(x)[0] for x in nums]

        @cache
        def dfs(i: int, e2: int, e3: int, e5: int) -> int:
            if i < 0:
                return 1 if e2 == e3 == e5 == 0 else 0

            x, y, z = es[i]
            res1 = dfs(i - 1, e2 - x, e3 - y, e5 - z)  # k 除以 nums[i]
            res2 = dfs(i - 1, e2 + x, e3 + y, e5 + z)  # k 乘以 nums[i]
            res3 = dfs(i - 1, e2, e3, e5)  # k 不变
            return res1 + res2 + res3

        return dfs(len(nums) - 1, e2, e3, e5)  # 从 k 开始，目标是变成 1
''',
    call=f'Solution().countSequences({NUMS}, {K})',
    expect=3,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 当前要决定怎么操作的 nums[i]）', cell=100,
             pointers={'i': 'blue'}, h=220),
        dict(type='text', h=90, size=28, fn=_txt),
        dict(type='calls', h=200, hide=('self', 'nums', 'k')),
    ],
    watch=['e2', 'e3', 'e5', ('x', 'x', 'green'), ('y', 'y', 'green'), ('z', 'z', 'green')],
    skip=['k >>= e2', 'e3 = 0', 'e5 = 0', 'while k % 3', 'while k % 5', 'e3 += 1', 'k //= 3', 'e5 += 1', 'k //= 5'],
    captions={
        'primeFactorization(int(k))': '先分解目标 `k = {int(B.k)}`：只能由 2、3、5 组成，因为 `nums[i] <= 6`',
        'e2 = (k & -k)': '`k & -k` 取出最低位的 1，`bit_length() - 1` 就是质因子 2 的个数：`e2 = {e2}`',
        'return (e2, e3, e5), k == 1': '2、3、5 的个数 = `({e2}, {e3}, {e5})`；除净后剩 `k = {k}` → {"==只含 2、3、5==" if ret[1] else "还有别的质因子 → 无解"}',
        'if not ok': '`ok = {ok}`：k 没有大于 5 的质因子，才可能凑出来 → 继续',
        'es = [': '每个 `nums[i]` 也拆成 2、3、5 的个数：`es = {es}`',
        'return dfs(len(nums) - 1': lambda S, B, r: (f'从 `k` 出发，==倒着==处理最后一个数：`dfs({B.i if "i" in B else len(B.nums) - 1}, {B.e2}, {B.e3}, {B.e5})`，目标是把 k 变成 1'
                                                    if 'i' in S['_inner'] else f'`dfs` 返回 `{r}`：共 {r} 种选择序列'),
        'if i < 0': lambda S, B, r: (f'`i = {S.i}`：nums 全部处理完 → 看 `({S.e2}, {S.e3}, {S.e5})` 是否全为 0' if S.i < 0
                                     else f'`i = {S.i}`：还要决定 `nums[{S.i}]` 怎么操作 → 继续'),
        'return 1 if e2 == e3 == e5 == 0': lambda S, B, r: (f'指数 `({S.e2}, {S.e3}, {S.e5})` 全为 0 → k 变成了 1 → ==找到一种合法方案==，返回 1'
                                                            if r == 1 else f'指数 `({S.e2}, {S.e3}, {S.e5})` 不全为 0 → k 没变成 1，不合法，返回 0'),
        'x, y, z = es[i]': '`nums[{i}] = {nums[i]}` 含 `{x}` 个 2、`{y}` 个 3、`{z}` 个 5',
        'res1 = dfs': lambda S, B, r: (f'k ==除以== `nums[{B.i}]`：指数各减 `({B.x},{B.y},{B.z})` → `dfs({B.i - 1}, {B.e2 - B.x}, {B.e3 - B.y}, {B.e5 - B.z})`'
                                       + ('' if S.i != B.i - 1 else '')
                                       + (f'；==记忆化命中==，直接得 `{S.res1}`' if S.i == B.i and 'res1' in S else '')),
        'res2 = dfs': lambda S, B, r: (f'k ==乘以== `nums[{B.i}]`：指数各加 `({B.x},{B.y},{B.z})` → `dfs({B.i - 1}, {B.e2 + B.x}, {B.e3 + B.y}, {B.e5 + B.z})`'
                                       + (f'；==记忆化命中==，直接得 `{S.res2}`' if S.i == B.i and 'res2' in S else '')),
        'res3 = dfs': lambda S, B, r: (f'k ==不变==（`nums[{B.i}]` 不操作）→ `dfs({B.i - 1}, {B.e2}, {B.e3}, {B.e5})`'
                                       + (f'；==记忆化命中==，直接得 `{S.res3}`' if S.i == B.i and 'res3' in S else '')),
        'return res1 + res2 + res3': '三种操作互斥，方案数相加：`{res1} + {res2} + {res3}` = =={ret}==',
    },
    cards=dict(
        one_liner='把 k 质因数分解，倒着乘除，目标是让 2、3、5 的幂次全为 0',
        complexity='时间 `O(n^4)`，空间 `O(n^4)`',
        problem=['`nums` 每个位置选一种：乘 `nums[i]`、除 `nums[i]`（有理数除法）、不变',
                 '从 `val = 1` 开始，问有多少种选择序列使最终 `val == k`',
                 '`nums[i] <= 6`，`k` 最大 `10^15`',
                 '本视频：`nums = [2, 2]`，`k = 1` → `3`'],
        quote='把分母的质因子的幂次视作负数，例如 1/8 = 2^-3。……从 k 和 n-1 开始，倒着乘除，目标是得到 1，即质因数分解中的 2,3,5 的幂次均为 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`nums[i] <= 6` 只含质因子 2、3、5：==把 val 记成三个幂次 (e2, e3, e5)==，除法就是减幂次',
              '倒着从 `k` 出发乘除，终点是 `(0, 0, 0)`，等价于 `val` 从 1 走到 k',
              '`@cache` 记忆化：不同操作可能得到同一个幂次（先乘再除 = 不变），合并后只剩 `O(n^4)` 个状态'],
        summary=['时间/空间 `O(n^4)`：`i, e2, e3, e5` 各 `O(n)` 个取值',
                 '`k` 含大于 5 的质因子时直接返回 0',
                 '乘/除/不变三种操作互斥，用加法原理相加',
                 '灵神还给了更朴素的写法：直接 `@cache` 记分数 `p/q`（`O(n^7)`）、约分后记忆化（`O(n^5 log U)`）；也可折半搜索 `O(3^(n/2))`'],
    ),
)
