RM = [1, 1, 2, 2, 2, 3]


def _cell(S, r, c, v):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 9:
        return None
    if r == i and c == j:
        return 'yellow'
    mx = S['rollMax'][j]
    if i > mx and (r, c) == (i - mx - 1, j):
        return 'pink'
    if r == i - 1:
        return 'blue'
    return None


def _formula(S):
    i, j = S.get('i'), S.get('j')
    if i is None or j is None or S.get('_line', 0) < 9:
        return '`f[i][j]` = 掷 i+1 次、最后一个点数是 j+1 的序列数；`s[i]` = `f[i]` 之和'
    mx = S['rollMax'][j]
    if i > mx:
        return f'`f[{i}][{j}] = s[{i-1}] − (s[{i-mx-1}] − f[{i-mx-1}][{j}])`：减掉末尾连出 {mx+1} 个 {j+1} 的'
    if i == mx:
        return f'`f[{i}][{j}] = s[{i-1}] − 1`：全是 {j+1} 的那 1 种超限'
    return f'`f[{i}][{j}] = s[{i-1}]`：长度 {i+1} 还不可能超限'


CONFIG = dict(
    num=1223, title='掷骰子模拟', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='回溯 → 记忆化 → 递推 → 前缀和优化',
    tags=['其他线性 DP', '难度分 2008'],
    code='''
class Solution:
    def dieSimulator(self, n: int, rollMax: List[int]) -> int:
        MOD = 10 ** 9 + 7
        m = len(rollMax)  # 6
        f = [[0] * m for _ in range(n)]
        f[0] = [1] * m
        s = [0] * n
        s[0] = m
        for i in range(1, n):
            for j, mx in enumerate(rollMax):
                res = s[i - 1]
                if i > mx: res -= s[i - mx - 1] - f[i - mx - 1][j]
                elif i == mx: res -= 1
                f[i][j] = res % MOD
            s[i] = sum(f[i]) % MOD
        return s[-1]
''',
    call='Solution().dieSimulator(4, [1, 1, 2, 2, 2, 3])',
    expect=1072,
    skip=['for j, mx in enumerate'],
    max_steps=52,
    views=[
        dict(type='array', var='rollMax', label='rollMax（每个点数最多连续几次）', h=130, cell=70,
             pointers={'j': 'pink'}, color=lambda S, k, v: 'pink' if k == S.get('j') and S.get('_line', 0) >= 9 else None),
        dict(type='text', fn=_formula, size=24, h=60),
        dict(type='table', var='f', label='f[i][j]（黄 = 正在算，蓝 = 上一行 s[i-1]，粉 = 要扣掉的格子）', h=300, cell=70,
             rows=lambda S: [f'i={k}' for k in range(len(S['f']))], cols=lambda S: [f'点{k+1}' for k in range(6)],
             color=_cell),
        dict(type='array', var='s', label='s[i] = 长度 i+1 的合法序列总数', h=190, cell=90,
             pointers={'i': 'blue'}),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('mx', 'mx', 'pink'), ('res', 'res', 'yellow'), ('s[-1]', 's[-1]', 'green')],
    captions={
        'MOD = ': '答案要取模 `10^9 + 7`',
        'm = len': '`m = 6` 个点数',
        'f = [[0]': '`f[i][j]`：掷 `i+1` 次、最后一个点数是 `j+1` 的合法序列数',
        'f[0] = [1]': '只掷 1 次：每个点数各 1 种，没有超限的可能',
        's[0] = m': '`s[0] = 6`：长度 1 的合法序列共 6 种',
        'for i in range': lambda S, B, r: (f'`i = {S.i}`：开始算长度 `{S.i + 1}` 的序列' if S.get('i') != B.get('i') else '所有长度都算完了'),
        'res = s[i - 1]': '`res = s[{i-1}] = {res}`：先假设前面任意合法序列后面都能接 `{j+1}`',
        'if i > mx': lambda S, B, r: (f'`i = {S.i} > mx = {S.mx}`：末尾可能已连出 {S.mx} 个 {S.j + 1}，再接就超限 → 扣掉 `s[{S.i-S.mx-1}] − f[{S.i-S.mx-1}][{S.j}]` = {S.s[S.i-S.mx-1] - S.f[S.i-S.mx-1][S.j]}，`res` = =={S.res}=='
                                      if S.i > S.mx else f'`i = {S.i} ≤ mx = {S.mx}`：不满足 `i > mx`，看下一个分支'),
        'elif i == mx': lambda S, B, r: (f'`i = mx = {S.mx}`：整串全是 `{S.j + 1}` 的那 1 种会超限 → `res` 减 1 = =={S.res}=='
                                         if S.i == S.mx else f'`i = {S.i} < mx = {S.mx}`：长度不够连出 {S.mx + 1} 个，不用扣'),
        'f[i][j] = res': '`f[{i}][{j}] = {f[i][j]}`',
        's[i] = sum': '`s[{i}] = sum(f[{i}])` = =={s[i]}==：这一行总数，留给下一行用',
        'return s[-1]': '掷 `{n}` 次的合法序列共 =={ret}== 种',
    },
    cards=dict(
        one_liner='前缀和：先全接，再扣掉连出 mx+1 个的非法数',
        complexity='时间 `O(n·m)`，空间 `O(n·m)`，`m = 6`',
        problem=['掷 `n` 次骰子，连续掷出点数 `i` 的次数不能超过 `rollMax[i]`',
                 '求不同点数序列的个数，对 `10^9 + 7` 取模',
                 '示例：`n=2, rollMax=[1,1,2,2,2,3]` → `34`；本视频 `n=4` → `1072`'],
        quote='可以用**回溯**来启发思考。……在回溯中就需要知道：剩余掷骰子的次数 i、上一个骰子值 last、last 的剩余连续出现次数 left。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先写回溯 `dfs(i, last, left)`，再 `@cache`，再 1:1 翻译成递推',
              '最后优化：`left` 这一维可以去掉，改成「总数 `s` 减去非法数」',
              '非法的：末尾恰连出 `mx+1` 个 `j`，用 `s[i-mx-1] - f[i-mx-1][j]` 计数'],
        summary=['时间 `O(nm)`，`m = 6`；未优化的递推是 `O(nmS)`，`S = sum(rollMax)`',
                 '`i > mx` 与 `i == mx` 要分开：后者要扣的就是「全是 j」这 1 种',
                 '`s[i-mx-1] - f[i-mx-1][j]`：前面不能以 j 结尾，否则连出的就不止 mx+1 个',
                 '题解还有回溯、记忆化、三维递推三种写法，这里选最后的优化写法；下标从 0 开始：`f[i]` 是长度 `i+1`'],
    ),
)
