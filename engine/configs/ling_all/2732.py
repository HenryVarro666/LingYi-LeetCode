GRID = [[1, 1, 1, 0], [0, 1, 1, 1], [1, 0, 1, 1], [0, 0, 0, 1]]


def _b(x, n=4):
    return format(x, f'0{n}b')


def _mask_txt(S):
    if 'f' not in S:
        return '每一行当成二进制数（第 j 列 = 第 j 位）；只需找 ==AND 为 0== 的两行'
    ln = S.get('_line')
    n = len(S['grid'][0])
    if 'u' in S and 's' in S:
        s = S['s']
        u = S['u']
        return f'`s = {_b(s, n)}`，补集 `{_b(u ^ s, n)}`：`f[s] = {S["f"][s]}`，`f[补集] = {S["f"][u ^ s]}`'
    if 'mask' in S and 'i' in S:
        return f'第 {S["i"]} 行 → `mask = {_b(S["mask"], n)}`'
    return '`f[s]`：在 s 的子集里出现过的行号（取最大），-1 = 没有'


CONFIG = dict(
    num=2732, title='找到矩阵中的好子集', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='二进制 + SOS DP（只看 1~2 行）',
    tags=['贪心与思维', '难度分 2240'],
    code='''
class Solution:
    def goodSubsetofBinaryMatrix(self, grid: List[List[int]]) -> List[int]:
        n = len(grid[0])
        f = [-1] * (1 << n)
        for i, row in enumerate(grid):
            mask = 0
            for j, x in enumerate(row):
                mask |= x << j
            if mask == 0:
                return [i]
            f[mask] = i

        u = (1 << n) - 1
        for b in range(n):
            for s in range(1, u):
                if (s >> b & 1) == 0:
                    continue
                i = f[s] = max(f[s], f[s ^ (1 << b)])
                if i < 0:
                    continue
                j = f[u ^ s]
                if j >= 0:
                    return sorted((i, j))
        return []
''',
    call=f'Solution().goodSubsetofBinaryMatrix({GRID})',
    expect=[0, 3],
    skip=['for j, x in enumerate(row)', 'continue'],
    views=[
        dict(type='grid', var='grid', label='grid（每行 = 一个二进制数，列 j = 第 j 位）', h=230, cell=70,
             color=lambda S, r, c, v: ('yellow' if S.get('_line', 0) <= 12 and 'mask' in S and r == S.get('i') else None)),
        dict(type='array', var='f', label='f[s]：s 的子集里出现过的行号（下标 = 二进制 s 的值）', h=230, cell=60,
             pointers={'s': 'blue', 'u ^ s': 'pink'}),
        dict(type='text', fn=_mask_txt, size=28, h=90),
    ],
    watch=[('i', 'i', 'blue'), ('mask', 'mask'), ('b', 'b', 'orange'), ('s', 's', 'blue'), ('j', 'j', 'pink')],
    captions={
        'n = len(grid[0])': '列数 `n = {n}`，行的状态最多 `2^n = {2**n}` 种',
        'f = [-1]': '`f` 先全填 `-1`：还没有任何一行',
        'for i, row in enumerate': lambda S, B, r: (f'读第 `{S.i}` 行 `{S.row}`' if 'row' in S and S.get('i') != B.get('i') else '所有行都读完了'),
        'mask = 0': '`mask` 清零，准备把这一行压成二进制数',
        'mask |= x << j': '第 `{j}` 列是 `{x}` → `mask = {mask}`',
        'if mask == 0': lambda S, B, r: ('全 0 的一行 → 单独一行就是好子集' if S.mask == 0
                                          else f'`mask = {S.mask} ≠ 0`：这一行不是全 0，继续'),
        'f[mask] = i': '状态 `{mask}` 对应第 `{i}` 行：`f[{mask}] = {i}`',
        'u = (1 << n) - 1': '`u = {u}` 是全集（所有列）。两行 AND 为 0 ⇔ 一行是另一行补集的子集',
        'for b in range(n)': '==SOS DP 外层枚举位 `b`==：把 `f[s]` 扩展成「s 的所有子集里的最大行号」',
        'for s in range(1, u)': '枚举非空真子集 `s`',
        'if (s >> b & 1) == 0': lambda S, B, r: (f'`s = {S.s}` 第 {S.b} 位是 1，可以从 `s ^ (1<<b)` 转移' if (S.s >> S.b & 1)
                                                  else f'`s = {S.s}` 第 {S.b} 位是 0，跳过'),
        'i = f[s] = max': '`f[{s}] = max(f[{s}], f[{s ^ (1 << b)}])` = =={f[s]}==：把去掉第 {b} 位的子集也算进来',
        'if i < 0': lambda S, B, r: ('`f[s] < 0`：s 的子集里没有任何一行，下一个' if S.i < 0
                                      else f'`f[s] = {S.i}`：s 的某个子集是第 {S.i} 行'),
        'j = f[u ^ s]': '看补集 `{u ^ s}`：`f[{u ^ s}] = {j}`',
        'if j >= 0': lambda S, B, r: (f'补集那边也有行（第 {S.j} 行）→ ==两行不相交，AND = 0==' if S.j >= 0
                                       else '补集里没有行，继续找'),
        'return sorted': '好子集是第 `{i}`、`{j}` 行，题目要求==升序== → `{ret}`',
        'return []': '一对都没找到 → 没有好子集，返回 `[]`',
    },
    max_steps=90,
    cards=dict(
        one_liner='n ≤ 5：好子集只需看 1 行或 2 行，两行 AND 为 0',
        complexity='时间 `O(mn + n·2^n)`，空间 `O(2^n)`',
        problem=['二进制矩阵 `grid`，选若干行，使==每列的和 ≤ 行数的一半（向下取整）==',
                 '返回任意一个好子集的行下标（升序），没有就返回空数组',
                 '本视频：4 行 4 列 `[[1,1,1,0],[0,1,1,1],[1,0,1,1],[0,0,0,1]]` → `[0,3]`'],
        quote='所以如果不存在小于 4 行的答案，那么也不会存在 ≥ 4 行的答案。……只需考虑答案为 1 行或者 2 行的情况。',
        quote_src='—— 灵茶山艾府题解',
        idea=['1 行：必须全 0；2 行：同列至多一个 1，==AND 等于 0==；3 行等价于 2 行',
              '性质：行数 ≥ 4 时 1 的个数最少的行至多 n/2 个 1，推出矛盾，所以不用考虑',
              '方法三：SOS DP 求 `f[s]`，枚举 `s` 与补集，两边都有行就找到答案'],
        summary=['时间 `O(mn + n·2^n)`，空间 `O(2^n)`',
                 '易错：返回前要 `sorted`，题目要求行下标升序',
                 '易错：全 0 行要先单独判断，`mask == 0` 直接返回 `[i]`',
                 '主写法是方法三（SOS DP）；方法一用哈希表两重循环，方法二枚举补集的子集 `O(3^n)`',
                 '同类：SOS DP 题单 §9.6，如 3670'],
    ),
)
