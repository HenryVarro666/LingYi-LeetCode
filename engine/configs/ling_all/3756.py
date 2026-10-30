def _t(S):
    if 'l' not in S or 'r' not in S:
        return '`pre_num[i]`：前 i 位里「非零数字」连起来的数；`sum_non_zero[i]`：前 i 位非零个数'
    l, r = S['l'], S['r']
    if 'length' not in S or S.get('_line') is None:
        return f'查询 `[{l}, {r}]`'
    length = S['length']
    p = S['pre_num']
    if 'x' not in S or S['_line'] < 16:
        return f'子串 `s[{l}..{r - 1}]` 里有 ==`{length}`== 个非零数字'
    return (f'`x = pre_num[{r}] − pre_num[{l}] × 10^{length}` = `{p[r]} − {p[l]} × {10 ** length}` = ==`{S["x"]}`==')


def _col(S, i, v):
    if 'l' in S and 'r' in S and '_line' in S and S['_line'] >= 13:
        if S['l'] <= i < S['r']:
            return 'green' if v != '0' else None
    return None


CONFIG = dict(
    num=3756, title='连接非零数字并乘以其数字和 II', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='数字和前缀和 + 前缀数字相减',
    tags=['灵神题单·常用数据结构', '灵神题单·字符串', '难度分 1968'],
    setup='''
MOD = 1_000_000_007
MAX_N = 100_001

# 预处理 10 的幂
pow10 = [1] * MAX_N
for i in range(1, MAX_N):
    pow10[i] = (pow10[i - 1] * 10) % MOD
''',
    code='''
class Solution:
    def sumAndMultiply(self, s: str, queries: List[List[int]]) -> List[int]:
        n = len(s)
        sum_d = [0] * (n + 1)         # s 的前缀和
        pre_num = [0] * (n + 1)       # s 的前缀对应的数字（模 MOD）
        sum_non_zero = [0] * (n + 1)  # s 的前缀中的非零数字个数
        for i, d in enumerate(map(int, s)):
            sum_d[i + 1] = sum_d[i] + d
            pre_num[i + 1] = (pre_num[i] * 10 + d) % MOD if d else pre_num[i]
            sum_non_zero[i + 1] = sum_non_zero[i] + (d > 0)

        ans = []
        for l, r in queries:
            r += 1  # 避免下面多次计算 r+1
            length = sum_non_zero[r] - sum_non_zero[l]
            x = pre_num[r] - pre_num[l] * pow10[length]
            ans.append(x * (sum_d[r] - sum_d[l]) % MOD)
        return ans
''',
    call="Solution().sumAndMultiply('10203004', [[0, 7], [1, 3], [4, 6]])",
    expect=[12340, 4, 9],
    views=[
        dict(type='text', fn=_t),
        dict(type='string', var='s', pointers={'i': 'blue'}, window=('l', 'r - 1'), color=_col, label='s', h=150),
        dict(type='array', var='sum_d', label='sum_d', h=120),
        dict(type='array', var='pre_num', label='pre_num', h=120),
        dict(type='array', var='sum_non_zero', label='非零数', h=120),
        dict(type='array', var='ans', label='ans', cell=100, h=170),
    ],
    watch=[('i', 'i', 'blue'), ('d', 'd', 'cyan'), ('length', 'length', 'orange'), ('x', 'x', 'green')],
    skip=['n = len(s)', 'sum_d = [0]', 'pre_num = [0]', 'sum_non_zero = [0]', 'ans = []'],
    captions={
        'for i, d in enumerate': '处理第 `{i}` 位数字 `d = {d}`',
        'sum_d[i + 1] =': '数字和前缀和：`sum_d[{i + 1}] = sum_d[{i}] + {d}` = `{sum_d[i + 1]}`（0 加了不影响和）',
        'pre_num[i + 1] =': lambda S, B, r: (f'`d = {S.d}` 非零：前缀数字 `pre_num[{S.i}] × 10 + {S.d}` → `{S.pre_num[S.i + 1]}`，==接在末尾=='
                                            if S.d else f'`d = 0`：不参与连接，`pre_num[{S.i + 1}]` 直接沿用 `{S.pre_num[S.i + 1]}`'),
        'sum_non_zero[i + 1] =': '非零数字个数前缀和：`{sum_non_zero[i + 1]}`（它代替 `r − l + 1`，因为 0 已经被删掉）',
        'for l, r in queries': '查询 `[{l}, {r}]`',
        'r += 1': '`r` 改成开区间右端 `{r}`，后面写 `pre[r]` 就是前 `r` 位',
        'length =': '子串 `s[{l}..{r - 1}]` 的非零数字个数 `sum_non_zero[{r}] − sum_non_zero[{l}]` = ==`{length}`==',
        'x = pre_num[r]': '前 `{l}` 位的数字要==往左挪 `{length}` 位==（乘 `10^{length}`）再减掉 → `x = {x}`',
        'ans.append': '答案 `x × 数字和`：数字和 = `sum_d[{r}] − sum_d[{l}]` = `{sum_d[r] - sum_d[l]}` → `{ans[-1]}`（取模）',
    },
    cards=dict(
        one_liner='数字和用前缀和；非零数字连成的数，用「前缀数字 − 前缀 × 10^个数」切出来',
        complexity='预处理 `O(n)`，每次查询 `O(1)`，空间 `O(n)`',
        problem=['给数字串 `s`，每次查询 `[l, r]`：把子串里的==非零数字==按顺序连成整数 `x`',
                 '答案是 `x × (x 的数位和)`，对 `10^9 + 7` 取模',
                 '示例：`s = "10203004"`，`[[0,7],[1,3],[4,6]]` → `[12340, 4, 9]`'],
        quote='子串 [l,r] 对应的数字为 preNum[r+1] - preNum[l] · 10^(r-l+1)……这意味着我们还需要计算子串中的非零字符个数，代替上式中的 r-l+1。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先想没有 0：`12345` 里切出 `34` = `1234 − 12 × 10^2`',
              '有 0 就把 0 当成不存在：`pre_num` 遇 0 不变，指数换成「非零个数」',
              '数位和里 0 不贡献，直接对 `s` 做前缀和'],
        summary=['时间 `O(n + q)`，空间 `O(n)`；`pow10` 预处理放在类外（视频里提前算好，没有逐行演示）',
                 '中途取模会让 `x` 变成负数，Python 的 `%` 保证结果非负；别的语言要 `+ MOD`',
                 '`length` 是非零个数，不是 `r − l`',
                 '相似题：2156 查找给定哈希值的子串（前缀哈希）'],
    ),
)
