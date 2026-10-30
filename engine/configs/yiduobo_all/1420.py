def _fi(S):
    try:
        return S['f'][S['i']]
    except Exception:
        return None


def _cell(S, r, c, v):
    if 'j' in S and 'c' in S and r == S['j'] and c == S['c']:
        return 'yellow'
    return 'green' if v else None


def _upd(S, B, ret):
    i, j, c = S.i, S.j, S.c
    if i == 0:
        return f'第一个数：任选 `{j}` 作为目前的最大值，必然产生 1 次比较 → `f[0][{j}][{c}] = 1`'
    return (f'`f[{i}][{j}][{c}] = f[{i-1}][{j}][{c}]×{j} + prefix_s[{c-1}]` = {S.f[i-1][j][c]}×{j} + {S.prefix_s[c-1]} '
            f'= =={S.f[i][j][c]}==（取 mod 前）')


def _pre(S, B, ret):
    i, j, c = S.i, S.j, S.c
    if i == 0:
        return '第一个位置之前没有数，累加的是 `f[-1]`（全 0 的占位行）→ 还是 0'
    return f'`prefix_s[{c-1}]` 累加进 `f[{i-1}][{j}][{c-1}]` = {S.f[i-1][j][c-1]}：给下一个更大的 j 当「之前都小于它」的方案数 → {S.prefix_s[c-1]}'


CONFIG = dict(
    num=1420, title='生成数组', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[长度][最大值][cost] · 前缀和优化',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def numOfArrays(self, n, m, k):

        mod = 10 ** 9 + 7

        f = [[[0] * (k + 1) for _ in range(m + 1)] for _ in range(n + 1)]
        for i in range(n):
            prefix_s = [0] * (k + 1)
            for j in range(1, m + 1):
                for c in range(1, min(i + 2, k + 1)):
                    if i == 0:
                        f[i][j][c] = 1
                    else:
                        f[i][j][c] = (f[i - 1][j][c] * j % mod + prefix_s[c - 1]) % mod
                    
                    prefix_s[c - 1] = (prefix_s[c - 1] + f[i - 1][j][c - 1]) % mod

        res = 0
        for j in range(1, m + 1):
            res = (res + f[n - 1][j][k]) % mod
        
        return res
''',
    call='Solution().numOfArrays(3, 3, 2)',
    expect=12,
    views=[
        dict(type='grid', var=_fi, label='f[i][j][c]：长度 i+1，最大值 j，cost 为 c 的数组数（行 = 最大值 j，列 = cost c）', cell=76, h=330,
             rows=[0, 1, 2, 3], cols=[0, 1, 2], color=_cell),
        dict(type='array', var='prefix_s', label='prefix_s[c]：已枚举的更小最大值 j′ 的 f[i−1][j′][c] 之和', cell=84, h=170,
             color=lambda S, i, v: 'cyan' if 'c' in S and i == S['c'] - 1 else None),
        dict(type='text', fn=lambda S: (f"长度 =={S['i'] + 1}== · 最大值 =={S['j']}== · cost =={S['c']}==" if 'c' in S and 'j' in S and 'i' in S else ''), h=50),
    ],
    watch=['i', 'j', 'c', ('res', 'res', 'green')],
    captions={
        'mod = 10': '答案要对 `10^9+7` 取模',
        'f = [[[0]': '`f[i][j][c]`：长度为 `i+1`、最大值为 `j`、搜索代价为 `c` 的数组数目',
        'prefix_s = [0]': '第 `{i}` 个位置：`prefix_s` 清零，边枚举 `j` 边累计「更小最大值」的方案',
        19: lambda S, B, r: ('`j` 全部枚举完' if 'j' in B and B.j == S.j and 'res' in B and B.res == S.res else f'枚举最大值 `j = {S.j}`'),
        9: lambda S, B, r: ('`j` 全部枚举完' if 'c' in B and B.j == S.j else f'枚举当前最大值 `j = {S.j}`，再枚举 cost `c`'),
        'if i == 0': lambda S, B, r: '长度为 1 的数组' if S.i == 0 else '长度大于 1，要考虑最后一位有两种可能',
        'f[i][j][c] = 1': _upd,
        'f[i][j][c] = (f[i - 1]': _upd,
        'prefix_s[c - 1] = ': _pre,
        'res = 0': '`res` 累加最大值为 `1..m`、cost 为 `k` 的数组数',
        'res = (res': '`res += f[{n - 1}][{j}][{k}]` = {f[n-1][j][k]} → =={res}==',
        'return res': '长度 `n`、最多 `m`、代价恰好 `k` 的数组共 =={res}== 个',
    },
    skip=['for i in range', 'for c in range'],
    max_steps=52,
    cards=dict(
        one_liner='记住当前最大值和已有 cost，最后一位只有两种可能',
        complexity='时间 `O(nmk)`，空间 `O(nmk)`',
        problem=['数组长度 `n`，每个数在 `[1, m]`；扫描时每遇到新的最大值，`cost` 加 1',
                 '求恰好 `cost = k` 的数组有多少个，答案对 `10^9+7` 取模',
                 '示例：`n=3, m=3, k=2` → `12`'],
        quote='令f[i][j][c]表示长度为i + 1，其中最大值为j，且已经使用题目代码段算法中cost为c的数组的数目。',
        quote_src='—— yiduobo 题解',
        idea=['最后一位是 `j`、前面都比它小：产生一次比较，`c` 增 1 → 对 `f[i−1][j′][c−1]`（`j′<j`）求和',
              '最后一位 ≤ `j`、前面已有 `j`：不增加 cost，最后一位有 `j` 种选法 → `f[i−1][j][c] × j`',
              '前者是关于 `j` 的前缀和，枚举 `j` 时顺便累加，省掉一层循环'],
        summary=['时间 `O(nmk)`，空间 `O(nmk)`',
                 '`i=0` 时直接设 1；`c` 的上界是 `min(i+1, k)`',
                 '`prefix_s` 要在每个 `i` 开头清零，并且「先用后加」：用的是比当前 `j` 更小的最大值',
                 '同类：带「当前最大值」状态的计数 DP'],
    ),
)
