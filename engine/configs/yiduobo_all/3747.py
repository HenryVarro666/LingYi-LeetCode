N0 = 1203


def _cur(S):
    if 'd' not in S:
        return None
    return len(str(S['n'])) if S['n'] > 0 else 0


def _digits(S):
    return str(N0)


def _info(S):
    if 'p9' not in S:
        return f'`n = {N0}`：答案 = 长度 `1..m-1` 的纯 1~9 数 + 长度 `m` 且 `≤ n` 的纯 1~9 数'
    z = '，已发现 0' if S.get('zero') else ''
    return f'`res = {S["res"]}`（短数个数），`full = {S["full"]}`（同长个数）{z}'


CONFIG = dict(
    num=3747, title='统计移除零后不同整数的数目', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='按位拆解 · 短数 + 同长数',
    tags=['数位 DP', '难度分 1848'],
    code='''
class Solution(object):
    def countDistinct(self, n):
        p9 = 1
        res = 0
        full = 0
        zero = False
        while n:
            d = n % 10
            if d > 0:
                full += (d - 1) * p9
            else:
                full = 0
                zero = True

            p9 *= 9
            n //= 10
            if n > 0:
                res += p9

        if not zero:
            full += 1
        return res + full
''',
    call=f'Solution().countDistinct({N0})',
    expect=900,
    views=[
        dict(type='string', var=_digits, label=f'n = {N0}：从个位向最高位逐位分离', h=230, cell=100,
             pointers={_cur: 'pink'}, pointer_labels={_cur: '当前位 d'},
             color=lambda S, k, v: 'red' if v == '0' else None),
        dict(type='text', fn=_info, size=26, h=70),
    ],
    watch=[('n', 'n', 'blue'), ('d', 'd', 'pink'), ('p9', 'p9', 'purple'), ('full', 'full', 'green'),
           ('res', 'res', 'yellow'), ('zero', 'zero', 'red')],
    captions={
        'p9 = 1': '`p9` 记 9 的幂：下一位以下有几位可以随便填 1~9',
        'res = 0': '`res`：长度 1 到 m-1 的纯 1~9 数的个数',
        'full = 0': lambda S, B, r: ('`full`：长度恰为 m、不超过 n 的纯 1~9 数的个数' if 'zero' not in S
                                      else '`d = 0`：这一位取 0 就不合法，低位算出的 `full` 全部作废 → 清零'),
        'zero = False': '`zero` 标记 n 里有没有 0，最后决定要不要把 n 本身算进去',
        'while n': lambda S, B, r: (f'`n = {S.n}`，还有数位没拆' if S.n else '`n = 0`，数位拆完了'),
        'd = n % 10': '`n % 10` 取出末位 `d = {d}`',
        'if d > 0': lambda S, B, r: (f'`d = {S.d} > 0`：可以参与计数' if S.d > 0 else '`d = 0`：不能是 0，要作废低位结果'),
        'full += (d - 1) * p9': '这一位取 `1..d-1` 共 `{d - 1}` 种，低位 `{p9}` 种随便填 → `full = {full}`',
        'zero = True': '标记 n 中有 0：n 本身不是纯 1~9 数',
        'p9 *= 9': '位数多一位，`p9 = {p9}`',
        'n //= 10': '去掉末位，`n = {n}`',
        'res += p9': '还有更高位 → 存在更短的数：`res += {p9}` → `res = {res}`',
        'if not zero': lambda S, B, r: ('n 里没有 0：n 自己也合法，`full += 1`' if not S.zero
                                         else 'n 里有 0：n 本身不算，不加 1'),
        'return': '`res + full` = `{res} + {full}` = =={ret}==',
    },
    cards=dict(
        one_liner='答案 = 短数的个数 + 同长且不超过 n 的纯 1~9 数个数',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`1..n` 每个数删掉所有 `0`，问记下的数里有多少个不同',
                 '示例：`n = 10` → 1~9 和 1，不同的有 `9` 个',
                 '本视频：`n = 1203` → `900`'],
        quote='长度在1到m - 1之间的，仅由1到9组成的数的个数；长度为m，仅由1到9组成，且大小不超过n的数的个数。',
        quote_src='—— yiduobo 题解原文',
        idea=['短数：长度为 `k` 有 `9^k` 个，`9 + 9^2 + ...` 在拆位时顺手累加到 `res`',
              '同长数：从高位逐位定，`(a[i] - 1) * 9^(后面位数)` 累加到 `full`',
              '高位出现 0，其后的式子全作废（`full = 0`）；n 无 0 则 n 本身再加 1'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '遇到 0 要把 `full` 清零，但 `res` 不受影响',
                 '`zero` 标记决定最后是否 `+1`（n 本身是否合法）',
                 '原文本来就是 `//=`，无需改动 Python 2 写法',
                 '对比灵神：他用 `ans` 一个变量，最低位不减 1；这里用 `+1` 补 n 本身'],
    ),
)
