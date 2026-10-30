def _info(S):
    if 'x' not in S:
        return '`f[c]` = 凑出金额 `c` 的最少硬币数，`inf` 表示凑不出'
    c = S.get('c')
    if c is None:
        return f'当前硬币 `x = {S["x"]}`：完全背包，==c 正序==（可重复使用）'
    return f'`f[{c}] = min(f[{c}], f[{c} − {S["x"]}] + 1)`'


def _fmt(v):
    return v


CONFIG = dict(
    num='LCR 103', title='零钱兑换', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='完全背包 · 最少硬币数',
    tags=[],
    code='''
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        f = [0] + [inf] * amount
        for x in coins:
            for c in range(x, amount + 1):
                f[c] = min(f[c], f[c - x] + 1)
        ans = f[amount]
        return ans if ans < inf else -1
''',
    call='Solution().coinChange([1, 2, 5], 8)',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='array', var='f', label='f[c]：凑出 c 的最少硬币数（蓝 = c，粉 = c − x）', h=260, cell=84,
             pointers={'c': 'blue', 'c - x': 'pink'},
             color=lambda S, i, v: ('blue' if i == S.get('c') else 'pink' if 'x' in S and 'c' in S and i == S['c'] - S['x'] else None)),
    ],
    watch=[('x', 'x', 'purple'), ('c', 'c', 'blue'), ('amount', 'amount', 'yellow'), ('ans', 'ans', 'green')],
    captions={
        'f = [0] + [inf] * amount': '`f[0] = 0`：凑 0 元要 0 枚；其余先设为 `inf`（凑不出）',
        'for x in coins': lambda S, B, r: (f'考虑硬币 `x = {S.x}`，它可以用无限次' if S.x != B.get('x') or B.get('c') is None else '所有硬币都处理完了'),
        'for c in range': lambda S, B, r: (f'`c` 从 `{S.x}` ==正序==到 `{S.amount}`：`f[c - x]` 可能已经用过 `x`，正好表示再用一枚' if S.c == S.x
                                           else '`c` 正序继续'),
        'f[c] = min': lambda S, B, r: (f'`f[{S.c}] = min({B.f[S.c]}, f[{S.c} − {S.x}] + 1 = {S.f[S.c - S.x] + 1})` = =={S.f[S.c]}=='),
        'ans = f[amount]': '`ans = f[{amount}] = {ans}`',
        'return ans if': lambda S, B, r: (f'`ans = {S.ans}` 有限 → 返回 =={r}==' if r != -1 else '`ans` 还是 `inf` → 凑不出，返回 ==-1=='),
    },
    cards=dict(
        one_liner='每种硬币可无限用：完全背包，c 正序',
        complexity='时间 `O(n·amount)`，空间 `O(amount)`',
        problem=['给不同面额的硬币 `coins` 和总金额 `amount`，求凑成总金额所需最少硬币数，凑不出返回 `-1`',
                 '每种硬币数量无限',
                 '示例：`coins = [1,2,5]`, `amount = 11` → `3`；本视频：`amount = 8` → `3`（5+2+1）'],
        quote='f = [0] + [inf] * amount ……  f[c] = min(f[c], f[c - x] + 1)',
        quote_src='—— 灵茶山艾府题解代码（四、空间优化：一个数组）',
        idea=['记忆化搜索 `dfs(i, c)`：不选第 i 种，或选一枚后仍在第 i 种（可重复）',
              '1:1 翻译成递推，再把第一维滚动掉，得到一维 `f`',
              '完全背包 ==c 正序==：`f[c - x]` 已含当前硬币，正好是「再选一枚」'],
        summary=['时间 `O(n·amount)`，空间 `O(amount)`',
                 '易错：初值 `f[0] = 0`，其余 `inf`；最后要判 `inf` 返回 -1',
                 '易错：完全背包 c 正序；0-1 背包才倒序',
                 '题解还有记忆化搜索、二维递推、两个数组三种写法，本视频演示最终一维写法'],
    ),
)
