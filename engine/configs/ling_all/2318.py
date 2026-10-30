N = 4
GOOD = [[k + 1 for k in range(6) if k != j and gcd(k + 1, j + 1) == 1] for j in range(6)]


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') != 8:
        return None
    if (r, c) == (i, j):
        return 'yellow'
    if r == i - 1 and c != j and (c + 1) in GOOD[j]:
        return 'blue'
    if r == i - 2 and c == j:
        return 'pink'
    return None


def _txt(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line') != 8:
        return '`f[i][j]`：长为 i、最后一个数是 j+1 的合法序列数；转移要减去“前前一个也是 j+1”的'
    ks = GOOD[j]
    return f'数字 ==`{j + 1}`== 的上一个数可选 `{ks}`，共 `{len(ks)}` 个'


def _cap(S, B, ret):
    i, j = S.i, S.j
    ks = GOOD[j]
    done = S.f[i][j] != 0 or B.f[i][j] != 0
    v = sum(S.f[i - 1][k - 1] for k in ks)
    if i == 2:
        if not done:
            return f'`f[2][{j}]`（最后一个数是 `{j + 1}`）：第 1 个数可选 `{ks}` → 求和 `{v}`；`f[0]` 全是 0，没有要减的'
        return f'`f[2][{j}]` = =={S.f[2][j]}==：和 `{j + 1}` 互质且不同的数有 {len(ks)} 个'
    t = S.f[2][j] - (1 if i > 3 else 0)
    if not done:
        return (f'`f[{i}][{j}]`（最后一个数是 `{j + 1}`）：上一个数可选 `{ks}`，求和 `{v}`；'
                f'再减 `({S.f[2][j]} − {1 if i > 3 else 0}) × f[{i - 2}][{j}]` = `{t * S.f[i - 2][j]}`')
    return f'`f[{i}][{j}] = {v} − {t * S.f[i - 2][j]}` = =={S.f[i][j]}=='


CONFIG = dict(
    num=2318, title='不同骰子序列的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='二维 DP：上一个数 + 容斥修正',
    tags=['难度分 2090'],
    code='''
class Solution:
    def distinctSequences(self, n: int) -> int:
        MOD, MX = 10 ** 9 + 7, 5
        f = [[0] * 6 for _ in range(MX + 1)]
        f[1] = [1] * 6
        for i in range(2, MX):
            for j in range(6):
                f[i][j] = (sum(f[i - 1][k] for k in range(6) if k != j and gcd(k + 1, j + 1) == 1)
                           - (f[2][j] - (i > 3)) * f[i - 2][j]) % MOD
        return sum(f[n]) % MOD
''',
    call=f'Solution().distinctSequences({N})',
    expect=184,
    skip=['for j in range(6)', '- (f[2][j]'],
    max_steps=34,
    views=[
        dict(type='text', size=26, h=90, fn=_txt),
        dict(type='table', var='f', label='f[i][j]（黄 = 算，蓝 = 上一个数，粉 = 要减的 f[i-2][j]）',
             h=430, cell=92, rows=lambda S: [f'i={k}' for k in range(len(S['f']))], cols=['1', '2', '3', '4', '5', '6'], color=_cell),
    ],
    watch=[('i', 'i', 'yellow'), ('j', 'j', 'pink'), ('n', 'n', 'blue')],
    captions={
        'MOD, MX': '`MX` 是预处理的最大长度：原题解是 `10^4 + 1`，为了演示这里改成 `5`（n = 4 够用）',
        'f = [[0] * 6': '`f[i][j]`：序列长度 `i`，最后一个数是 `j + 1` 的合法序列数，6 个数 → 6 列',
        'f[1] = [1] * 6': '长度为 1 的序列：每个数都行，各 `1` 种',
        'for i in range': lambda S, B, r: ('`i = {}`：只依赖 `f[i-1]` 和 `f[i-2]`，按长度从小到大算'.format(S.i) if S.get('i') != B.get('i')
                                           else '预处理完成，`f[n]` 里 6 个数相加就是答案'),
        'f[i][j] = (sum': _cap,
        'return sum(f[n])': '把长度 `{n}` 时最后一个数为 1~6 的方案数加起来：==`{ret}`==',
    },
    cards=dict(
        one_liner='f[i][j] 只记最后一个数，容斥减掉“前前一个相同”的序列',
        complexity='时间 `O(n·m^2)`，空间 `O(n·m)`，这里 `m = 6`',
        problem=['掷 6 面骰子 `n` 次，要求相邻两数 ==互质==（gcd = 1）',
                 '相等的两个数下标差必须 `> 2`',
                 '求合法序列总数，对 `10^9 + 7` 取模；示例 `n = 4` → `184`'],
        quote='原因在于前前一个元素不能为 4，而我们在计算 f[i-1][1/3/5] 时，它的前一个元素是可以为 4 的。',
        quote_src='—— 灵茶山艾府题解（方法二：二维 DP）',
        idea=['朴素转移 `f[i][j] = Σ f[i-1][k]`（`k ≠ j` 且互质）会多算：前前一个也是 `j` 的序列',
              '每个 `k` 减一份 `f[i-2][j]`，又会多减“第 i-3 个数是 k”的，这部分恰好又是一份 `f[i-2][j]` → 加回去',
              '合并后：`f[i][j] = Σ f[i-1][k] − (f[2][j] − 1) · f[i-2][j]`；`i = 3` 时没有第 i-3 个数，不用加回'],
        summary=['时间 `O(n·m^2)`，空间 `O(n·m)`；`f[2][j]` 恰好等于求和的项数',
                 '易错：`i = 3` 的边界要用 `(i > 3)` 去掉加回的一份；取模后别忘了 `% MOD` 防负数',
                 '原文预处理写在类外面（`MX = 10 ** 4 + 1`）；为了能逐行演示，把它挪进函数并把 `MX` 改成 `5`，递推式逐字照搬',
                 '方法一是三维 `f[i][last][last2]`，更直观但 `O(n·m^3)`'],
    ),
)
