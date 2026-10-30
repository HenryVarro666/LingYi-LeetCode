S0 = 'FW'
N = len(S0)
NAMES = 'FWE'


def _both(S):
    if 'f' not in S:
        return None
    i = S.get('i', -1)
    prev = S['f'][max(i, 0)]
    cur = S['f'][i + 1] if i >= 0 else S['f'][0]
    if i < 0:
        return [list(r) + [0, 0, 0] for r in prev]
    return [list(p) + list(c) for p, c in zip(prev, cur)]


def _rows(S):
    return [str(j - N) for j in range(2 * N + 1)]


def _txt(S):
    if 'i' not in S:
        return '`f[i][j+n][ban]`：前 `i` 回合、得分差 `j`、上一回合出了 `ban` 时，Bob 获胜的方案数'
    i = S['i']
    if 'j' not in S or 'ban' not in S:
        return f'第 `{i}` 回合，Alice 出 `{S0[i]}`，Bob 得分差 `j` 从 `{-i}` 到 `{N - i - 1}`'
    if 'k' in S and 'x' in S and S.get('_line') in (21, 25):
        k, x = S['k'], S['x']
        return f'Alice 出 `{NAMES[x]}`，Bob 出 `{NAMES[k]}`：`(k − x) % 3 = {(k - x) % 3}`（1 = Bob 赢，2 = Alice 赢，0 = 平）'
    return f'当前状态：`j = {S["j"]}`，Bob 上一轮不能出 `{NAMES[S["ban"]]}`'


def _col(S, r, c, v):
    if 'i' not in S or 'j' not in S or 'ban' not in S or S.get('_line', 0) < 14:
        return None
    if c >= 3:
        return 'yellow' if r == S['j'] + N and c - 3 == S['ban'] else None
    if 'k' in S and 'score' in S and S.get('_line') in (25, 26) and r == S['j'] + S['score'] + N and c == S['k']:
        return 'blue'
    return None


CONFIG = dict(
    num=3320, title='统计能获胜的出招序列数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='多维 DP：从右往左 1:1 递推',
    tags=['灵神题单', '多维 DP', '难度分 2153'],
    code='''
class Solution:
    def countWinningSequences(self, s: str) -> int:
        MOD = 1_000_000_007
        n = len(s)
        f = [[[0] * 3 for _ in range(n * 2 + 1)] for _ in range(n + 1)]
        for j in range(n + 1, n * 2 + 1):
            f[0][j] = [1] * 3

        mp = {'F': 0, 'W': 1, 'E': 2}
        pow2 = 1
        for i, c in enumerate(s):
            x = mp[c]
            pow2 = pow2 * 2 % MOD
            for j in range(-i, n - i):
                for ban in range(3):
                    if j > i + 1:
                        f[i + 1][j + n][ban] = pow2
                        continue
                    res = 0
                    for k in range(3):
                        if i == n - 1 or k != ban:
                            score = (k - x) % 3
                            if score == 2:
                                score = -1
                            res += f[i][j + score + n][k]
                    f[i + 1][j + n][ban] = res % MOD
        return f[n][n][0]
''',
    call=f'Solution().countWinningSequences({S0!r})',
    expect=2,
    max_steps=50,
    skip=['MOD = 1_000', 'n = len(s)', 'mp = {', 'x = mp[c]', 'for j in range', 'for ban in range', 'for k in range', 'res = 0',
          'if score == 2', 'score = -1', 'score = (k - x)'],
    views=[
        dict(type='text', fn=_txt, size=22, h=60),
        dict(type='string', var='s', label='s：Alice 的出招（i = 当前回合）', cell=80, pointers={'i': 'blue'}, h=170),
        dict(type='table', var=_both, label='左 = f[i]（上一层，蓝 = 这步用到的格子）　右 = f[i+1]（正在算，黄 = 当前状态）', h=420, cell=70,
             rows=_rows, cols=lambda S: ['旧' + c for c in NAMES] + ['新' + c for c in NAMES], color=_col),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ban', 'ban', 'orange'), ('k', 'k', 'yellow'), 'score', 'res'],
    captions={
        'f = [[[0]': '`f[i+1][j+n][ban]` 对应 `dfs(i, j, ban)`：`j` 加上 `n` 避免下标为负，共 `2n+1` 行',
        'f[0][j] = [1]': '`j > n` 说明 Bob 已经领先得多，后面怎么出都赢 → 方案数 1',
        'pow2 = 1': '`pow2` 记 `2^(i+1)`',
        'pow2 = pow2 * 2': '`pow2 = 2^{i+1}`：剩下 `{i+1}` 回合每回合在两个生物里选',
        'for i, c in enumerate': lambda S, B, r: (f'`i = {S.i}`：Alice 出 `{S.c}`，由 `f[{S.i}]` 推出 `f[{S.i + 1}]`' if S.get('i') != B.get('i') else '所有回合都推完了'),
        'if j > i + 1': lambda S, B, r: (f'`j = {S.j} > i + 1 = {S.i + 1}`：就算后面全输也赢 → ==必胜==' if S.j > S.i + 1 else f'`j = {S.j} ≤ i + 1`：还不能确定，要枚举 Bob 这回合出什么'),
        'f[i + 1][j + n][ban] = pow2': '必胜：剩 `{i+1}` 回合各有 2 种选法 → `f = {pow2}`',
        'if i == n - 1 or k != ban': lambda S, B, r: (f'Bob 这回合出 `{NAMES[S.k]}`：{"`i = n−1` 是最后一回合（从右往左最先处理），没有 ban 限制" if S.i == S.n - 1 else ("和上一回合 `" + NAMES[S.ban] + "` 不同 → 可以" if S.k != S.ban else "和上一回合相同 → ==不允许==")}'),
        'res += f[i][j + score + n][k]': lambda S, B, r: (f'`({S.k} − {S.x}) % 3 = {(S.k - S.x) % 3}` → 得分 `{S.score}`（{"Bob 赢" if S.score == 1 else "Alice 赢" if S.score == -1 else "平"}）→ 差变成 `j + score = {S.j + S.score}`，累加 `f[{S.i}][{S.j + S.score + S.n}][{NAMES[S.k]}] = {S.f[S.i][S.j + S.score + S.n][S.k]}` → `res = {S.res}`'),
        'f[i + 1][j + n][ban] = res': '`f[{i+1}][{j + n}][{ban}] = res % MOD` = =={f[i+1][j+n][ban]}==',
        'return f[n][n][0]': '答案 `f[n][n][0]`：`n` 回合、得分差 0、没有限制 → =={ret}==',
    },
    cards=dict(
        one_liner='从右往左：记「得分差」和「上一回合不能出什么」',
        complexity='时间 `O(n^2 K^2)`（`K = 3`），空间 `O(n^2 K)`',
        problem=['Alice 的出招序列 `s` 已知，Bob ==不能连续两回合出同一种==',
                 '火龙胜地精、水蛇胜火龙、地精胜水蛇；Bob 总分严格更高才算赢',
                 '数出 Bob 能获胜的不同出招序列，对 `10^9 + 7` 取余；示例 `"FFF"` → `3`',
                 '本视频演示 `s = "FW"` → `2`'],
        quote='方便把递归翻译成递推，==从右往左==思考。……我们需要在递归过程中跟踪：当前回合 i、==我们与对手的得分之差 j==、前一回合我们召唤的生物 ban。',
        quote_src='—— 灵茶山艾府题解',
        idea=['状态 `dfs(i, j, ban)`：只记==得分差==，不用分别记两人得分',
              '枚举这回合出 `k ≠ ban`，`score = (k − s[i]) % 3`，`2` 当作 `−1`',
              '剪枝：`-j > i` 必败；`j > i + 1` 必胜，直接给 `2^(i+1)`'],
        summary=['时间 `O(n^2 K^2)`：状态 `n^2 K` 个，每个枚举 `K` 种出招',
                 '易错：得分差可能为负，下标要加 `n`；`j` 的范围是 `[-i, n-i-1]`',
                 '易错：最后一轮（`i == n-1`）Bob 没有 `ban` 限制，所以用 `i == n - 1 or k != ban`',
                 '灵神题解先写了 `@cache` 记忆化搜索，本视频演示的是 1:1 翻译成的递推',
                 '同类：状态机 DP 与多维 DP 题单里的题'],
    ),
)
