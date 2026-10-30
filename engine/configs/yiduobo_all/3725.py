MAT = [[2, 3], [4, 6], [3, 5]]


def _txt(S):
    if 'f' not in S:
        return ''
    I = S['_inner']
    if 'h' not in I:
        return '`f[v]`：每行各选一个数后，这些数的最大公约数恰好是 `v` 的方案数'
    if 'pre' in I and 'v' in I:
        return f"上一行的 GCD = `pre = {I['pre']}`（{I['h'][I['pre']]} 种方案），这一行选 `v = {I['v']}` → 新 GCD = `gcd({I['pre']}, {I['v']})`"
    return '`h` = 上一行结束时的 `f`；`f` 清空后重新累加'


def _fmt(k, v):
    return f'{k}: {v}'


CONFIG = dict(
    num=3725, title='统计每一行选择互质整数的方案数', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='f[v] = GCD 恰好为 v 的方案数 · 哈希表滚动',
    tags=['灵神题单', '难度分 1982'],
    setup='import copy',
    code='''
class Solution(object):
    def countCoprime(self, mat):
        
        f = {}
        for v in mat[0]:
            f[v] = f.get(v, 0) + 1
        
        def gcd(x, y):
            while y != 0:
                x, y = y, x % y
            return x

        mod = 10 ** 9 + 7
        for line in mat[1:]:
            h = copy.deepcopy(f)
            f = {}
            for v in line:
                for pre in h:
                    g = gcd(pre, v)
                    f[g] = f.get(g, 0) + h[pre]
                    if f[g] >= mod:
                        f[g] -= mod
        
        return f.get(1, 0)
''',
    call=f'Solution().countCoprime({MAT})',
    expect=7,
    views=[
        dict(type='grid', var='mat', label='mat（黄 = 正在处理的这一行 line）', cell=90, h=250,
             color=lambda S, i, j, v: 'yellow' if S.get('line') is not None and S['mat'][i] is S['line'] else None),
        dict(type='map', var='h', label='h（上一行结束时的 f：GCD → 方案数，只读）', fmt=_fmt, h=130, font=26),
        dict(type='map', var='f', label='f（当前：GCD → 方案数；黄 = 新增 / 改动）', fmt=_fmt, h=200, font=26),
        dict(type='text', h=90, size=26, fn=_txt),
    ],
    watch=[('line', 'line'), ('v', 'v', 'blue'), ('pre', 'pre', 'pink'), ('g', 'g', 'green')],
    skip=['while y != 0', 'x, y = y, x % y', 'return x', 'def gcd', 'mod = 10', 'if f[g] >= mod', 'f[g] -= mod'],
    captions={
        'for v in mat[0]': lambda S, B, r: ('第 0 行：每个数自己就是 GCD → 先放进 `f`' if 'v' not in B or S.v != B.v else '第 0 行放完，`f` = 第 0 行每个数的出现次数'),
        'f[v] = f.get(v, 0) + 1': '`f[{v}]` = {f[v]}：选 `{v}` 这一种，GCD 就是 `{v}`',
        'for line in mat[1:]': lambda S, B, r: (f'处理下一行 `line = {S.line}`：用上一行的 `f` 推出新的 `f`' if B.get('line') != S.line
                                                else '所有行都处理完了，`f` 里是 GCD → 方案数'),
        'h = copy.deepcopy(f)': '把上一行的 `f` 复制成 `h`（只读），然后清空 `f` 重新累加',
        4: '`f`：GCD → 方案数的哈希表',
        16: '`f = {{}}`：这一行的状态从空开始',
        'for v in line': lambda S, B, r: (f'这一行选 `v = {S.v}`' if S.get('v') != B.get('v') or 'pre' not in B or True and S['_inner'].get('pre') is None
                                          else '这一行的数都选完了，`f` 就是这一行的结果'),
        'for pre in h': lambda S, B, r: (f'枚举上一行的 GCD `pre = {S.pre}`（共 `{S.h[S.pre]}` 种方案）' if B.get('pre') != S.pre or B.get('v') != S.v
                                         else '上一行的状态都枚举完了'),
        'g = gcd(pre, v)': lambda S, B, r: f'新的 GCD = `gcd({B.pre}, {B.v})` = =={__import__("math").gcd(B.pre, B.v)}==（只会越算越小）',
        'f[g] = f.get(g, 0) + h[pre]': '`f[{g}]` += `h[{pre}]` = {h[pre]} → ==`{f[g]}`==：不同路径落到同一个 GCD，方案数累加（超过 `mod` 就减一次）',
        'return f.get(1, 0)': 'GCD 恰好为 1 的方案数 `f[1]` = =={ret}==',
    },
    cards=dict(
        one_liner='GCD 只会越算越小：直接把 GCD 当状态，哈希表滚动',
        complexity='时间 `O(m·n·U·log U)`，空间 `O(U)`',
        problem=['`m × n` 矩阵 `mat`，每行恰好选一个数',
                 '求选出的数 ==最大公约数为 1== 的方案数，对 `10^9+7` 取模',
                 '`m, n` 和元素值都在 1–150',
                 '本视频：`[[2,3],[4,6],[3,5]]` → `7`'],
        quote='最大公约数只会越算越小，因此无论如何选择元素，这些元素的最大公约数都将落在1到150之间，因此可以直接将最大公约数表示在状态中，利用动态规划进行求解。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f[v]`：已处理的行里每行选一个，GCD 恰好是 `v` 的方案数',
              '第 0 行：每个数 `v` 自己就是 GCD，`f[v]` 加 1',
              '之后每行：枚举上一行的 `pre` 和这一行的 `v`，`g = gcd(pre, v)`，`f[g] += h[pre]`',
              '只会出现有限的 GCD，用哈希表代替数组，只存出现过的值'],
        summary=['时间 `O(m·n·U·log U)`（`U` 为最大元素），空间 `O(U)`',
                 '易错：写 `f` 之前先复制成 `h`，再把 `f` 清空，否则会边读边写',
                 '每次累加后要处理 `mod`（这里用减法而不是取模）',
                 '对比灵神：灵神从最后一行倒着 `dfs(i, g)`，yiduobo 正着一行行推',
                 '原文已是 Python 3 可运行写法，仅在 `setup` 里补了 `import copy`'],
    ),
)
