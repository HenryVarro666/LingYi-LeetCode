def _t(S):
    if 'x' not in S or 'y' not in S:
        return '`ss` 数位和前缀 · `v` 非零数字连成的前缀数（模） · `non_zero` 非零个数 · `p10` 10 的幂'
    x, y = S['x'], S['y']
    if S['_line'] < 21:
        return f'查询 `[{x}, {y}]`：`s[{x}..{y}]` 里取出非零数字'
    if 'dv' not in S or S['_line'] < 23:
        return f'数位和 `ds = ss[{y + 1}] − ss[{x}]` = =={S.get("ds")}=='
    k = S['non_zero'][y + 1] - S['non_zero'][x]
    return f'`dv = v[{y + 1}] − v[{x}] × 10^{k}` = ==`{S["dv"]}`==，答案 `ds × dv`'


def _col(S, i, v):
    if 'x' in S and 'y' in S and S.get('_line', 0) >= 21 and S['x'] <= i <= S['y']:
        return 'green' if v != '0' else None
    return None


CONFIG = dict(
    num=3756, title='连接非零数字并乘以其数字和 II', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='数位和前缀 + 取模前缀数 + 非零个数',
    tags=['灵神题单·常用数据结构', '灵神题单·字符串', '难度分 1968'],
    code='''
class Solution(object):
    def sumAndMultiply(self, s, queries):
        
        ss = [0]
        v = [0]
        p10 = [1]
        non_zero = [0]
        mod = 10 ** 9 + 7
        for c in s:
            d = int(c)
            ss.append((ss[-1] + d) % mod)
            p10.append(p10[-1] * 10 % mod)
            if c != '0':
                v.append((v[-1] * 10 + d) % mod)
                non_zero.append(non_zero[-1] + 1)
            else:
                v.append(v[-1])
                non_zero.append(non_zero[-1])

        res = []
        for x, y in queries:
            ds = (ss[y + 1] - ss[x] + mod) % mod
            dv = (v[y + 1] - v[x] * p10[non_zero[y + 1] - non_zero[x]] % mod + mod) % mod
            res.append(ds * dv % mod)
        return res
''',
    call="Solution().sumAndMultiply('10203004', [[0, 7], [1, 3], [4, 6]])",
    expect=[12340, 4, 9],
    views=[
        dict(type='text', fn=_t),
        dict(type='string', var='s', pointers={'x': 'pink', 'y': 'purple'}, window=('x', 'y'), color=_col, label='s', h=150),
        dict(type='array', var='ss', label='ss', h=115),
        dict(type='array', var='v', label='v', h=115),
        dict(type='array', var='non_zero', label='非零数', h=115),
        dict(type='array', var='res', label='res', cell=100, h=170),
    ],
    watch=[('c', 'c', 'blue'), ('x', 'x', 'pink'), ('y', 'y', 'purple'), ('ds', 'ds', 'orange'), ('dv', 'dv', 'green')],
    skip=['ss = [0]', 'v = [0]', 'p10 = [1]', 'non_zero = [0]', 'mod = 10', 'res = []', 'd = int(c)', 'p10.append'],
    captions={
        'for c in s': '扫描字符 `{c}`，同时维护数位和、前缀数、非零个数',
        'ss.append': '`ss` 数位和前缀：加上 `{c}`（0 不影响和）→ `{ss[-1]}`',
        "if c != '0'": lambda S, B, r: (f'`{S.c}` 不是 0 → 要接到前缀数字的末尾' if S.c != '0' else '`0` 要被去掉 → 前缀数字和非零个数都不变'),
        'v.append((v[-1] * 10': '前缀数 `v` 乘 10 再加 `{d}` → `{v[-1]}`，非零个数同时 +1',
        'non_zero.append(non_zero[-1] + 1)': '`non_zero` +1 → `{non_zero[-1]}`',
        'v.append(v[-1])': '遇到 0：`v` 沿用 `{v[-1]}`，不接任何东西',
        'non_zero.append(non_zero[-1])': '遇到 0：`non_zero` 也不变 → `{non_zero[-1]}`',
        'for x, y in queries': '查询 `[{x}, {y}]`',
        'ds =': '数位和：`ss[{y + 1}] − ss[{x}]` = ==`{ds}`==（加 `mod` 防负数）',
        'dv =': '`v[{y + 1}] − v[{x}] × 10^(非零个数 {non_zero[y + 1] - non_zero[x]})`：先把前缀数左移再减，只剩子串里的非零数字 → ==`{dv}`==',
        'res.append': '答案 `ds × dv` = `{ds} × {dv}` → `{res[-1]}`',
    },
    cards=dict(
        one_liner='用「前缀减前缀乘 10 的幂」切出子串数，幂要按非零个数算',
        complexity='预处理 `O(n)`，每次查询 `O(1)`，空间 `O(n)`',
        problem=['数字串 `s` 和查询 `[x, y]`：把子串里的 `0` 去掉，剩下的数字连成整数',
                 '答案 = 这个整数 × 它的数位和，对 `10^9 + 7` 取模',
                 '示例：`s = "10203004"`，`[[0,7],[1,3],[4,6]]` → `[12340, 4, 9]`'],
        quote='如果不考虑0，那么s[left: right + 1]，就可以认为是s[:right + 1] - s[:left] * 10^(right - left + 1)，例如12345中的34，可以认为是1234 - 12 * 10^2。',
        quote_src='—— yiduobo 题解原文',
        idea=['数位和：0 不影响和，对整个 `s` 做前缀和就行',
              '前缀数太大存不下 → 记录它对 `10^9 + 7` 取模的结果 `v`',
              '遇到 `0` 就不更新 `v`，指数改用非零个数 `non_zero` 之差'],
        summary=['时间 `O(n + q)`，空间 `O(n)`',
                 '减法后要 `+ mod` 再取模，防止出现负数',
                 '`p10` 要按「非零个数」查，不是 `y − x + 1`',
                 '对比灵神：这里把 `10` 的幂在同一趟循环里递推出来，灵神是类外预处理',
                 '原文是 Python 2 风格写法，这份代码本身可直接在 Python 3 运行，未做修改'],
    ),
)
