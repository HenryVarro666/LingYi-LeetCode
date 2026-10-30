PR = '2357'
MOD = 10 ** 9 + 7


def _cp(s, j):
    n = len(s)
    return j == 0 or j == n or (s[j - 1] not in PR and s[j] in PR)


# 注意：第 19、20 行会调用 can_partition，步骤结束时的“当前帧”是它，里面的 j 是参数，
# 所以第 19 行里看到的是 j-l，第 20 行里是 j。这里换算回外层的 j / sum。
def _live(S):
    return 'i' in S and 'sum' in S and S.get('_line') in (19, 20)


def _J(S):
    return S['j'] + S['l'] if S['_line'] == 19 else S['j']


def _SUM(S):
    j = _J(S)
    if S['_line'] == 19 and _cp(S['s'], j - S['l']):
        return (S['sum'] + S['f'][S['i'] - 1][j - S['l']]) % MOD
    return S['sum']


def _scolor(S, idx, v):
    return 'green' if v in PR else None


def _cell(S, r, c, v):
    if not _live(S):
        return None
    i, j, l = S['i'], _J(S), S['l']
    if r == i and c == j:
        return 'yellow'
    if r == i - 1 and c == j - l and _cp(S['s'], j - l):
        return 'blue'
    return None


def _formula(S):
    if not _live(S):
        return '`f[i][j]`：前 `j` 个字符分成 `i` 段的方案数；绿色 = 质数数字'
    i, j, l = S['i'], _J(S), S['l']
    return f"第 `{i}` 段：`j = {j}`，`j' = j-l = {j-l}`；`sum` = 合法分割点 `j'` 的 `f[{i-1}][j']` 之和 = =={_SUM(S)}=="


def _cap19(S, B, ret):
    i, j, l = B['i'], B['j'], B['l']
    jp = j - l
    if _cp(B['s'], jp):
        new = (B['sum'] + B['f'][i - 1][jp]) % MOD
        return f"`j' = j-l = {jp}` 是合法分割点 → `sum += f[{i-1}][{jp}]`：`{B['sum']} + {B['f'][i-1][jp]}` = =={new}==（`j'` 与 `j` 同步右移）"
    return f"`j' = j-l = {jp}` 不是合法分割点（要前非质数、后质数）→ `sum` 不变，仍为 {B['sum']}"


def _cap20(S, B, ret):
    i, j = B['i'], B['j']
    if _cp(B['s'], j):
        return f"`j = {j}` 是合法分割点 → `f[{i}][{j}] = sum` = =={B['sum']}==（以 `j` 结尾的第 `{i}` 段有这么多种切法）"
    return f"`j = {j}` 不是合法分割点（`s[{j-1}]` 非质数且 `s[{j}]` 质数才行）→ `f[{i}][{j}]` 保持 0"


CONFIG = dict(
    num=2478, title='完美分割的方案数', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='划分型 DP + 前缀和（双指针）优化',
    tags=['灵神题单', '动态规划', '难度分 2344'],
    code='''
class Solution:
    def beautifulPartitions(self, s: str, k: int, l: int) -> int:
        MOD = 10 ** 9 + 7
        def is_prime(c: str) -> bool:
            return c in "2357"
        # 判断是否可以在 j-1 和 j 之间分割（开头和末尾也算）
        def can_partition(j: int) -> bool:
            return j == 0 or j == n or not is_prime(s[j - 1]) and is_prime(s[j])

        n = len(s)
        if k * l > n or not is_prime(s[0]) or is_prime(s[-1]):  # 剪枝
            return 0
        f = [[0] * (n + 1) for _ in range(k + 1)]
        f[0][0] = 1
        for i in range(1, k + 1):
            sum = 0
            # 优化：枚举的起点和终点需要给前后的子串预留出足够的长度
            for j in range(i * l, n - (k - i) * l + 1):
                if can_partition(j - l): sum = (sum + f[i - 1][j - l]) % MOD  # j'=j-l 双指针
                if can_partition(j): f[i][j] = sum
        return f[k][n]
''',
    call='Solution().beautifulPartitions("23542185131", 3, 2)',
    expect=3,
    views=[
        dict(type='string', var='s', label='s（绿 = 质数数字；分割点 j 在 s[j-1] 与 s[j] 之间）', h=190, cell=60,
             color=_scolor),
        dict(type='table', var='f', label='f[i][j]：前 j 个字符分成 i 段的方案数（黄 = 正在算，蓝 = f[i-1][j-l]）',
             h=240, cell=80, color=_cell),
        dict(type='text', fn=_formula, size=26, h=60),
    ],
    watch=['i', ('j', lambda S: _J(S) if _live(S) else '-', 'pink'), ('sum', lambda S: _SUM(S) if _live(S) else '-', 'yellow'), ('l', 'l', 'blue')],
    captions={
        'MOD =': '答案对 `10^9+7` 取模',
        'n = len': '`n = {n}`',
        'if k * l > n': lambda S, B, ret: (f"剪枝：`s[0]={S['s'][0]}` 必须是质数，`s[-1]={S['s'][-1]}` 必须不是质数，总长至少 `k*l = {S['k']*S['l']}` ≤ {S['n']} → 都满足，继续"),
        'f = [[0]': '`f[i][j]` 表示前 `j` 个字符分成 `i` 段的方案数',
        'f[0][0] = 1': '空串分成 0 段算 ==1 种方案==，所以下标整体后移一位',
        'for i in range': lambda S, B, ret: ('`i` 枚举完毕，答案在 `f[k][n]`' if B.get('i') == S['i'] else f"开始计算分成 =={S['i']}== 段"),
        'sum = 0': '`sum` 记录第 `i-1` 段所有合法结束位置的方案数之和，清零',
        'if can_partition(j - l)': _cap19,
        'if can_partition(j): f[i][j]': _cap20,
        'return f[k][n]': '答案 `f[{k}][{n}]` = =={f[k][n]}==',
    },
    max_steps=44,
    skip=['for j in range', 'MOD =', 'n = len', 'return c in', 'return j == 0', 'def '],
    cards=dict(
        one_liner='每段要求质数开头、非质数结尾，只有特定位置能当分割点',
        complexity='时间 `O(k(n-kl))`，空间 `O(kn)`',
        problem=['数字串 `s` 分成 `k` 段，每段长度 `≥ l`，首字符是质数 `2357`，尾字符不是质数',
                 '求完美分割的方案数，对 `10^9+7` 取模',
                 '本视频：示例 1：`s="23542185131"`，`k=3`，`l=2` → `3`'],
        quote='定义 j 为分割点，等价于 s[j] 不是质数且 s[j+1] 是质数。……我们可以从小到大同时遍历 j\' 和 j，一边更新 sum，一边计算 f[i][j]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f[i][j]`：前 `j` 个字符分成 `i` 段；只有「前一个不是质数、后一个是质数」的位置才能切',
              '`j` 是分割点时，`f[i][j]` = 所有满足 `j - j\' ≥ l` 的分割点 `j\'` 的 `f[i-1][j\']` 之和',
              '`j\' = j - l` 随 `j` 一起右移，一边累加 `sum` 一边填表，省掉内层枚举'],
        summary=['时间 `O(k(n-kl))`，空间 `O(kn)`，可用滚动数组降到 `O(n)`',
                 '`f[0][0] = 1`：空串算一种方案，所以下标整体后移一位',
                 '`j` 的范围给前后各段预留 `l` 的长度；开头必须质数、结尾必须非质数，不满足直接返回 0',
                 '相似题：1977. 划分数字的方案数'],
    ),
)
