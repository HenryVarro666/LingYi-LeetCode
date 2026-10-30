def _digits(S):
    return list(S['n']) if 'n' in S else []


CONFIG = dict(
    num=1689, title='十-二进制数的最少数目', difficulty='Medium', category='贪心算法',
    author='灵茶山艾府', technique='最大数位 = 答案',
    tags=['贪心与思维', '脑筋急转弯', '难度分 1355'],
    code='''
class Solution:
    def minPartitions(self, n: str) -> int:
        return int(max(n))
''',
    call="Solution().minPartitions('82734')",
    expect=8,
    views=[
        dict(type='string', var='n', label='n 的每一位：这一位需要几个 1 就要几个数', h=240,
             color=lambda S, i, v: 'green' if v == max(S['n']) else None, dim=lambda S, i, v: v != max(S['n'])),
        dict(type='text', fn=lambda S: f"最大的数位是 `{max(S['n'])}` → 至少要 =={max(S['n'])}== 个十-二进制数" if 'n' in S else '', size=30),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return': "字符串里最大的字符是 `max(n) = '{max(n)}'`，转成整数就是答案：=={ret}==",
    },
    cards=dict(
        one_liner='答案就是 n 中最大的那个数字',
        complexity='时间 `O(|n|)`，空间 `O(1)`',
        problem=['十-二进制数：每一位只能是 0 或 1，且没有前导零',
                 '给十进制字符串 `n`，求和为 `n` 的十-二进制数最少几个',
                 '示例：`"82734"` → `8`'],
        quote='设 m 为 n 中的最大数字，那么答案为 m。构造方案为：设 n 的第 i 个数字为 n_i，那么拆分出的这 m 个数的第 i 位上，有 n_i 个 1 和 m-n_i 个 0。',
        quote_src='—— 灵茶山艾府题解',
        idea=['最大数位 `m`：这一位每个数最多贡献 1，所以至少要 `m` 个数',
              '构造：其余数位 `d` 拆成 `d` 个 1 和 `m-d` 个 0',
              '例如 `321 = 111 + 110 + 100`'],
        before=[dict(heading='先看 321', lines=['最大的数字是 3，这一位至少拆成 3 个 1', '`2 = 1 + 1 + 0`，`1 = 1 + 0 + 0`', '合起来 `321 = 111 + 110 + 100`，3 个就够'])],
        after=[dict(heading='套到 82734 上', lines=['最大数位是 8，所以答案是 8', '第 1 位 8：8 个数全取 1', '第 2 位 2：2 个取 1，6 个取 0，其余位同理'])],
        summary=['时间 `O(|n|)`，空间 `O(1)`',
                 '`max(n)` 对字符串取最大字符，数字字符的字典序和数值一致',
                 '易错点：要 `int(...)` 转成整数再返回',
                 '同类题：脑筋急转弯 · 按位独立考虑'],
    ),
)
