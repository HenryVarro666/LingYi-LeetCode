def _phase(S):
    i = S.get('i')
    if i is None:
        return '`f[j]` = 当前这些骰子（每面 0 ~ k−1）掷出和为 `j` 的方案数'
    mj = S.get('max_j')
    if mj is None:
        return f'第 `{i}` 个骰子：先把 `f` 变成前缀和，再相邻错开 `k` 位相减'
    return f'第 `{i}` 个骰子：`f[j]` = 前 `{i - 1}` 个骰子的结果，在 `0 ~ {mj}` 范围内更新'


def _formula(S):
    j, k, ln = S.get('j'), S.get('k'), S.get('_line')
    if j is None or ln not in (10, 12):
        return '先对 `f` 求前缀和 `s`，再让 `f[j] = s[j] - s[j-k]`（窗口宽 `k`）'
    if ln == 10:
        return f'前缀和：`s[{j}] = s[{j - 1}] + f[{j}]`'
    return f'`f[{j}]` = `s[{j}] − s[{j - k}]`：掷出 0 ~ k−1 的 `k` 种情况之和'


CONFIG = dict(
    num=1155, title='掷骰子等于目标和的方法数', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='分组背包 · 前缀和优化',
    tags=['灵神核心路线', '灵神题单·动态规划', '难度分 1654'],
    code='''
class Solution:
    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        if not (n <= target <= n * k):
            return 0  # 无法组成 target
        MOD = 10 ** 9 + 7
        f = [1] + [0] * (target - n)
        for i in range(1, n + 1):
            max_j = min(i * (k - 1), target - n)  # i 个骰子至多掷出 i*(k-1)
            for j in range(1, max_j + 1):
                f[j] += f[j - 1]  # 原地计算 f 的前缀和
            for j in range(max_j, k - 1, -1):
                f[j] = (f[j] - f[j - k]) % MOD  # f[j] 是两个前缀和的差
        return f[-1]
''',
    call='Solution().numRollsToTarget(3, 4, 8)',
    expect=12,
    views=[
        dict(type='text', fn=_phase, size=26, h=60),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='array', var='f', label='f[j]：掷出的数字都减 1 后，和恰为 j 的方案数', h=300, cell=100,
             pointers={'j': 'blue'},
             dim=lambda S, i, v: i > S.get('max_j', 99),
             color=lambda S, i, v: 'green' if i == len(S['f']) - 1 else None),
    ],
    watch=[('i', 'i', 'blue'), ('max_j', 'max_j', 'cyan'), ('j', 'j', 'pink'), ('目标 f[-1]', 'f[-1]', 'green')],
    captions={
        'if not (n <= target': '`{n} <= {target} <= {n * k}`？每个骰子至少 1、至多 k，和必须落在这个范围',
        'MOD = ': '答案取模 `{MOD}`',
        'f = [1]': '每个骰子的数字都先减 1（0 ~ k−1），目标和变成 `target - n = {target - n}`；`f[0] = 1`：没有骰子、和为 0 有 1 种',
        'for i in range': lambda S, B, r: (f'开始掷第 `{S.i}` 个骰子' if S.i != B.get('i') else f'`{S.i}` 个骰子都掷完了'),
        'max_j = ': '`max_j = min({i} * {k - 1}, {target - n})` = =={max_j}==：`{i}` 个骰子至多掷出 `{i * (k - 1)}`，更大的 j 方案数必为 0',
        'f[j] += f[j - 1]': '`f[{j}] += f[{j - 1}]` → =={f[j]}==：`f[0..{j}]` 的前缀和',
        'f[j] = (f[j] - f[j - k])': '`f[{j}] = s[{j}] - s[{j - k}]` = `{B.f[j]} - {B.f[j - k]}` = =={f[j]}==：只保留最近 `{k}` 种掷法的和',
        'return f[-1]': '`f[target - n] = f[{target - n}]` = =={ret}==',
    },
    cards=dict(
        one_liner='枚举掷出几 → 一段区间求和 → 前缀和 O(1)',
        complexity='时间 `O(n·(target-n))`，空间 `O(target-n)`',
        problem=['`n` 个骰子，每个有 `k` 个面（1 到 `k`），掷出点数和恰好为 `target` 的方案数，对 `10^9+7` 取模',
                 '示例：`n=2, k=6, target=7` → `6`',
                 '本视频：`n=3, k=4, target=8` → `12`'],
        quote='把每个骰子掷出的数字都提一个 1 出来……原地计算 f 的前缀和；f[j] 是两个前缀和的差。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`dfs(i, j)`：枚举最后一个骰子掷出 x，累加 `dfs(i-1, j-x)`',
              '每个骰子数字 −1，就不用讨论 `j<0`，目标和变成 `target - n`',
              '`f[i][j]` 是 `f[i-1]` 上一段长 `k` 的窗口和 → 前缀和相减 `O(1)` 得到',
              '用 `f[j] += f[j-1]` 原地做前缀和，`j` 倒序相减，一维数组即可'],
        summary=['时间 `O(n·(target-n))`，空间 `O(target-n)`',
                 '易错：先判断 `n <= target <= n*k`；减 1 后目标和是 `target - n`',
                 '易错：相减要倒序，否则 `f[j-k]` 已被改成差分值',
                 '题解前面还有：暴力递归 → 记忆化 → 二维递推 `O(nk(target-n))` 的写法，本视频是最终优化版'],
    ),
)
