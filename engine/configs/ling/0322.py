import math as _m


def _fm(x):
    return '∞' if x == _m.inf else str(x)


def _f_color(S, k, v):
    if 'c' not in S or 'x' not in S:
        return 'green' if ('ans' in S and k == S['amount']) else None
    if k == S['c']:
        return 'green'
    if k == S['c'] - S['x']:
        return 'blue'
    return None


def _formula(cv, S, B, box, T):
    s = ''
    if 'ans' in S:
        s = f'`ans = f[{S["amount"]}] = {_fm(S["ans"])}`'
    elif 'c' in S and 'x' in S and 'f' in B and B.get('c') == S['c'] and B.get('x') == S['x']:
        c, x = S['c'], S['x']
        old, sel = B['f'][c], S['f'][c - x] + 1
        s = (f'`f[{c}] = min(f[{c}], f[{c - x}] + 1)` = min({_fm(old)}, {_fm(S["f"][c - x])} + 1) = '
             f'=={_fm(min(old, sel))}==')
    elif 'x' in S and 'ans' not in S:
        s = f'硬币 `{S["x"]}`：在 `f` 这面墙上==覆盖==画新的画（`c` 从 `{S["x"]}` 到 `{S["amount"]}`）'
    elif 'f' in S and 'ans' not in S:
        s = '`f[0] = 0`：金额 0 不用硬币；其余先设 ==∞==（还凑不出来）'
    if s:
        cv.rich(box[0] + 22, box[1] + 8, s, box[2] - box[0] - 44, size=28, accent=(255, 166, 87), max_lines=2,
                line_gap=1.4)


def _legend(cv, S, B, box, T):
    x, y = box[0] + 24, (box[1] + box[3]) / 2
    for c, t in [('green', 'f[c]：旧值 = 不选'), ('blue', 'f[c-x]：本轮新值，+1 = 再选一枚 x')]:
        cv.rect((x, y - 11, x + 22, y + 11), fill=T[c], r=5)
        cv.text((x + 32, y), t, 22, T['muted'], anchor='lm')
        x += 32 + cv.tlen(t, 22) + 36


def _cap_f(S, B, ret):
    c, x = S.c, S.x
    old, prev = B.f[c], S.f[c - x]
    sel = prev + 1
    if prev == _m.inf:
        return f'`f[{c - x}] = ∞`：凑不出 `{c - x}`，再加一枚 `{x}` 也凑不出 → `f[{c}]` 保持 =={_fm(S.f[c])}=='
    if sel < old:
        return f'不选：`f[{c}] = {_fm(old)}`；在 `{c - x}` 的基础上==再选一枚 {x}==：`{prev} + 1 = {sel}` → `f[{c}]` = =={sel}=='
    return f'不选：`f[{c}] = {_fm(old)}`；再选一枚 `{x}`：`{prev} + 1 = {sel}`，不更少 → 保持 =={_fm(S.f[c])}=='


CONFIG = dict(
    num=322, title='零钱兑换', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='完全背包：记忆化搜索 → 递推 → 一个数组',
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
    call='Solution().coinChange([2, 5], 9)',
    expect=3,
    views=[
        dict(type='custom', draw=_formula, h=60),
        dict(type='array', var='coins', label='coins（物品，每种无限枚）',
             color=lambda S, k, v: 'orange' if 'x' in S and v == S['x'] and 'ans' not in S else None,
             cell=96, h=170),
        dict(type='array', var='f', label='f[c] = 恰好凑出金额 c 最少要几枚', color=_f_color,
             pointers={'c': 'green', 'c - x': 'blue'}, pointer_labels={'c - x': 'c-x'}, cell=88, h=250),
        dict(type='custom', draw=_legend, h=50),
    ],
    watch=[('x', 'x', 'orange'), ('c', 'c', 'green'), ('c-x', 'c - x', 'blue'), 'amount', ('ans', 'ans', 'green')],
    skip=['for c in range'],
    captions={
        'f = [0]': '`f[0] = 0`、其余 `inf`：翻译自递归边界 `dfs(-1, 0) = 0`、`dfs(-1, c>0) = ∞`',
        'for x in coins': lambda S, B, ret: (f'硬币 `x = {S.x}`：`c < {S.x}` 时 `f[c]` 不变（赋值多余），所以 `c` 从 `{S.x}` 开始'
                                             if B.get('x') != S.x else '所有硬币都考虑完了'),
        'f[c] = min': _cap_f,
        'ans = f[amount]': '答案在 `f[amount] = f[{amount}]` = =={ans}==',
        'return ans if': '`{ans} < inf`：能凑出 → 返回 =={ret}==（`9 = 5 + 2 + 2`）；若是 ∞ 则返回 `-1`',
    },
    cards=dict(
        one_liner='硬币 = 物品、金额 = 容量、每种无限枚：完全背包求恰好装满的最少件数',
        complexity='时间 `O(n·amount)`，空间 `O(amount)`',
        problem=['硬币面额 `coins`（每种无限枚），凑出总金额 `amount` 的==最少硬币数==',
                 '凑不出来返回 `-1`',
                 '示例：`[1,2,5], 11` → `3`；演示：`coins = [2,5], amount = 9` → `3`'],
        before=[dict(heading='第一步：选或不选，写出记忆化搜索', chapter='② 思路', lines=[
            '`dfs(i, c)`：用前 `i` 种硬币恰好凑出 `c`，最少几枚',
            '不选第 `i` 种：`dfs(i-1, c)`；选一枚：`dfs(i, c - coins[i]) + 1`（==还能继续选==）',
            '边界 `i < 0`：`c == 0` 返回 0，否则 `inf`；入口 `dfs(n-1, amount)`',
            '答疑：「选一个就不再选」= 先选到 `dfs(i, c-x)`，再在那一层「不选」',
        ])],
        quote='好比在一面墙上画画，原来这面墙画的是 f[i]，现在要画一副新的画，==把原来的画覆盖掉==，新的画叫做 f[i+1]。',
        quote_src='—— 灵茶山艾府题解 · 空间优化：一个数组',
        idea_heading='第二步：1:1 翻译成递推，再压成一个数组',
        idea=['`f[i+1][c] = min(f[i][c], f[i+1][c-x] + 1)`，`f[0][0] = 0`，其余 `inf`',
              '`c < x`：`f[c] = f[c]`，原来的画不变 → ==赋值多余==，c 从 x 开始',
              '`c ≥ x`：`f[c]` 就地取材是旧画；`f[c-x]` 是==新画的内容== → `f[c] = min(f[c], f[c-x] + 1)`'],
        after=[dict(heading='另一种方法：BFS 最短路', lines=[
            '把金额当节点：从 `s` 到 `s + coins[i]` 连一条边',
            '问题变成：从 0 到 `amount` 的==最短路长度== → 一层一层 BFS',
            '两种方法都是 `O(n·amount)` 时间',
        ])],
        summary=['时间 `O(n·amount)`，空间 `O(amount)`（二维写法是 `O(n·amount)`）',
                 '`inf` 表示凑不出；`inf + 1` 仍是 `inf`，最后要==转成 -1==',
                 '一维时内层==正序==：`f[c-x]` 已是本轮新值，才能重复选同一种硬币',
                 '和 279 完全平方数是同一个模型：完全背包求最小'],
    ),
)
