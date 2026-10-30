NUMS = [2, 3, 6]
N = len(NUMS)


def _cell(S, r, c, v):
    s, i, j = S.get('s'), S.get('i'), S.get('j')
    line = S.get('_line', 0)
    if s is None or i is None or line not in (8, 12, 13):
        return None
    if r == s and c == i:
        return 'yellow'
    if j is not None and line in (11, 12) and s >> j & 1 and (r, c) == (s ^ (1 << j), j):
        return 'green'
    return None


def _formula(S):
    s, i, j = S.get('s'), S.get('i'), S.get('j')
    if s is None or i is None or S.get('_line', 0) not in (8, 12, 13):
        return '`f[S][i]` = 可选下标集合为 S、上一个数下标为 i 时的排列数'
    if S.get('_line', 0) in (11, 12) and j is not None and s >> j & 1:
        return f'`f[{s:0{N}b}][{i}] += f[{s ^ (1 << j):0{N}b}][{j}]`（选 `nums[{j}]` = {NUMS[j]} 接在 {NUMS[i]} 后面）'
    return f'正在算 `f[{s:0{N}b}][{i}]`：上一个数是 `nums[{i}]` = {NUMS[i]}'


def _cap_if(S, B, ret):
    pre, x = S.pre, S.x
    ok = (pre % x == 0 or x % pre == 0)
    inset = S.s >> S.j & 1
    if not inset:
        return f'下标 `{S.j}` 不在 S 里（已经填过），不能再选'
    if ok:
        return f'`{pre}` 和 `{x}` 有倍数关系（`{max(pre, x)} % {min(pre, x)} = 0`）→ ==可以相邻==，累加子状态'
    return f'`{pre}` 与 `{x}` 谁也不整除谁 → ==不能相邻==，跳过'


CONFIG = dict(
    num=2741, title='特别的排列', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='排列型状压 DP（1:1 翻译成递推）',
    tags=['灵神题单·动态规划', '难度分 2021'],
    code='''
class Solution:
    def specialPerm(self, nums: List[int]) -> int:
        n = len(nums)
        u = (1 << n) - 1
        f = [[0] * n for _ in range(u)]
        f[0] = [1] * n
        for s in range(1, u):
            for i, pre in enumerate(nums):
                if s >> i & 1:
                    continue
                for j, x in enumerate(nums):
                    if s >> j & 1 and (pre % x == 0 or x % pre == 0):
                        f[s][i] += f[s ^ (1 << j)][j]
        return sum(f[u ^ (1 << i)][i] for i in range(n)) % 1_000_000_007
''',
    call=f'Solution().specialPerm({NUMS})',
    expect=2,
    skip=['for j, x in enumerate', 'if s >> i & 1', 'f = [[0] * n', 'continue'],
    max_steps=60,
    views=[
        dict(type='text', fn=_formula, size=24, h=70),
        dict(type='array', var='nums', label='nums（下标 j 对应二进制第 j 位，从右数）', h=280, cell=90,
             pointers={'i': 'blue', 'j': 'pink'}),
        dict(type='table', var='f', label='f[S][i]：行 = 剩余可选下标集合 S（二进制），列 = 上一个数的下标 i', h=390, cell=70,
             rows=lambda S: [f'{k:0{N}b}' for k in range(2 ** N - 1)], cols=lambda S: [f'{k}' for k in range(N)],
             color=_cell),
    ],
    watch=[('s', 's', 'yellow'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('pre', 'pre', 'blue'), ('x', 'x', 'pink')],
    captions={
        'n = len(nums)': '`n = {n}`',
        'u = (1 << n) - 1': '全集 `U = {u}`（二进制 `{u:0{n}b}`）：每一位表示一个下标还能不能选',
        'f = [[0] * n': '`f[S][i]` 对应 `dfs(S, i)`，共 `2^n - 1` 行、`n` 列',
        'f[0] = [1] * n': '边界：`S = ∅`，所有数都选完了，找到一个特别排列 → `f[0][i] = 1`',
        'for s in range': lambda S, B, r: (f'`S = {S.s:0{S.n}b}`：子状态 `S ^ {{j}}` 比 `S` 小，所以 ==S 从小到大==枚举' if S.get('s') != B.get('s')
                                           else '所有 S 都算完了'),
        'for i, pre': lambda S, B, r: ('`i` 都枚举完了，换下一个 S' if S.get('i') == B.get('i') and S.get('s') == B.get('s') else f'`i = {S.i}` 在 S 里：S 里是还没选的数，而 `i` 要是==上一个已填的数== → 跳过'
                                      if S.s >> S.i & 1 else f'上一个数的下标 `i = {S.i}`（`pre = {S.pre}`），它不在 S 中，继续算'),
        'if s >> j & 1 and': _cap_if,
        'f[s][i] += f[s ^': '`f[{s:0{n}b}][{i}] += f[{s ^ (1 << j):0{n}b}][{j}]` → =={f[s][i]}==（下一个填 `nums[{j}]`，剩下集合去掉 j）',
        'return sum': '答案 = 各起点 `f[U \\ {{i}}][i]` 之和 = =={ret}==（再取模）',
    },
    cards=dict(
        one_liner='用「可选集合 + 上一个数」当状态',
        complexity='时间 `O(n^2 · 2^n)`，空间 `O(n · 2^n)`',
        problem=['`nums` 里 `n` 个互不相同的正整数，排列相邻两数必须==一个整除另一个==',
                 '返回特别排列的个数，对 `10^9 + 7` 取模',
                 '示例：`nums = [2,3,6]` → `2`（`[3,6,2]` 和 `[2,6,3]`）'],
        quote='相比 526，本题需要额外知道上一个选的数的下标是多少，因此要多一个参数。定义 dfs(S,i) 表示在可以选的下标集合为 S，上一个选的数的下标是 i 时，可以构造出多少个特别排列。',
        quote_src='—— 灵茶山艾府题解（一、记忆化搜索）',
        idea=['`nums[i]` 值域很大，所以用==下标集合==当二进制状态',
              '`f[S][i] = Σ f[S \\ {j}][j]`：枚举下一个选的 `j`，要求与 `nums[i]` 有倍数关系',
              '边界 `f[∅][i] = 1`；答案是各起点 `f[U \\ {i}][i]` 之和'],
        summary=['时间 `O(n^2 2^n)` = 状态数 `O(n 2^n)` × 转移 `O(n)`',
                 '易错：`i` 是已用的数，==不能在 S 中==；`j` 必须在 S 中',
                 '题解还给了 `@cache` 记忆化写法；随机数据下很多状态到不了，记忆化更快',
                 '同类题：526 优美的排列（排列型 ①，相邻无关）'],
    ),
)
