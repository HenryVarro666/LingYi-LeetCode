N0 = 7406


def _cur(S):
    if 'pow9' not in S or 'd' not in S:
        return None
    return len(str(S['n'])) if S['n'] > 0 else 0


def _digits(S):
    return str(N0)


def _info(S):
    if 'pow9' not in S:
        return f'`n = {N0}`：统计 1..n 中==不含 0==的整数个数（去掉 0 后不同的数 = 不含 0 的数）'
    if 'd' not in S:
        return '从个位开始，一位一位拆 `n`'
    return f'已处理低位的合法个数 `ans = {S["ans"]}`，下一位的权重 `pow9 = {S["pow9"]}`'


CONFIG = dict(
    num=3747, title='统计移除零后不同整数的数目', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='数位 DP · 从低到高数不含 0 的数',
    tags=['数位 DP', '难度分 1848'],
    code='''
class Solution:
    def countDistinct(self, n: int) -> int:
        ans = 0
        pow9 = 1
        while n > 0:
            n, d = divmod(n, 10)
            if d == 0:
                ans = 0
            else:
                if pow9 > 1:
                    d -= 1
                ans += d * pow9
            pow9 *= 9
        return ans + (pow9 - 9) // 8
''',
    call=f'Solution().countDistinct({N0})',
    expect=5436,
    views=[
        dict(type='string', var=_digits, label=f'n = {N0} 的十进制数位（个位在右，从右往左处理）', h=230, cell=100, pointers={_cur: 'pink'}, pointer_labels={_cur: '当前位 d'},
             color=lambda S, k, v: 'red' if v == '0' else None),
        dict(type='text', fn=_info, size=26, h=70),
    ],
    watch=[('n', 'n', 'blue'), ('d', 'd', 'pink'), ('pow9', 'pow9', 'purple'), ('ans', 'ans', 'green')],
    captions={
        'n, d = divmod': '`divmod(n, 10)`：拆出末位 `d = {d}`，剩下 `n = {n}`',
        'if d == 0': lambda S, B, r: (f'`d = 0`：这一位只能填 0，不合法 → 低位凑出的方案全作废' if S.d == 0
                                      else f'`d = {S.d} ≠ 0`：这一位可以填 1..9'),
        3: '`ans` 累计「长为 m 且 ≤ n」的不含 0 整数个数，从低位往高位累加',
        8: '低位已数出的「长为 m 且 ≤ n」的方案==全部清零==：高位有 0，这些数都含 0',
        'd -= 1': '不是最低位：这一位填 `1..d-1`，共 `d-1 = {d}` 种；填 d 本身留给更高位继续约束',
        'ans += d * pow9': '这一位 `{d}` 种选择 × 后面各位随便填 `{pow9}` 种 → `ans = {ans}`',
        'pow9 *= 9': '再往高一位，权重 `pow9 = 9^k` 乘 9 → {pow9}',
        'while n > 0': lambda S, B, r: (f'`n = {S.n} > 0`，还有高位没处理' if S.n > 0 else '`n = 0`，所有数位处理完'),
        'return': '再加上长度小于 m 的不含 0 的整数：`9^1+...+9^(m-1) = (9^m - 9) / 8 = {(pow9 - 9) // 8}`，答案 =={ret}==',
    },
    cards=dict(
        one_liner='去掉 0 后不同的数 = 不含 0 的数，按位数分类数一数',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`1..n` 中每个数删掉所有 `0` 后记下来，问有多少个不同的数',
                 '示例：`n = 10` → 记下 1..9 和 1，共 `9` 个；`n ≤ 10^15`',
                 '本视频：`n = 7406` → `5436`'],
        quote='题目让我们计算去掉 0 后的不同整数个数，也就是不含 0 的整数个数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['长度小于 `m` 的不含 0 整数：每位 1..9 随便填，共 `(9^m − 9) / 8` 个',
              '长度为 `m` 且 `≤ n`：含 0 的去掉 0 后变短，已被上面统计过',
              '从低到高遍历，遇到 `0` 就把「长为 m」的方案数置零'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '最低位可以等于 `d`（所以不减 1），其余位只能填 `1..d-1` 再靠更高位约束',
                 '遇到数位 0：`ans` 必须清零，不能 break，因为高位还要继续累加',
                 '优化前写法从高到低遍历、遇 0 直接 break；还可以套数位 DP 模板'],
    ),
)
