def _inf():
    parts = []
    for b in range(0, 4):
        r = list(range(max(10 * b, 1), 10 * b + 10))
        parts += r if b % 2 == 0 else r[::-1]
    return ''.join(map(str, parts))


INF = _inf()
K = 11


def _s(S):
    return INF[:K + 8]


def _col(S, i, v):
    return 'yellow' if i == K - 1 else None


def _text(S):
    if 'p10' not in S:
        return f'无限字符串开头：`{INF[:30]}……`，要找第 `k = {K}` 位（黄色格）'
    k, p, ln = S['k'], S['p10'], S['length']
    if 'x' not in S:
        return f'`length={ln}` 的数从 `{p}` 起，共 `{p * 9}` 个，占 `{p * 9 * ln}` 位；当前 `k={k}`'
    x = S['x']
    if 'b' not in S:
        return f'第 `k` 位落在 `length={ln}` 的第 `{(k - 1) // ln + 1}` 个数：`x = {x}`'
    return f'`x={x}`，块号 `b = {S["b"]}`；要取它的第 `(k-1) % length = {(k - 1) % ln}` 位（从 0）'


CONFIG = dict(
    num=4022, title='无限字符串里第 K 个数字', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='按位数递减 k + 对称数字',
    tags=['灵神题单', '难度分 1915'],
    code='''
class Solution(object):
    def kthDigit(self, k):

        p10 = 1
        length = 1

        while k > p10 * 9 * length:
            k -= p10 * 9 * length
            p10 *= 10
            length += 1

        x = (k - 1) // length + p10
        b = x // 10
        if b % 2 == 1:
            x = x + 9 - (x % 10) * 2
        return int(str(x)[(k - 1) % length])
''',
    call='Solution().kthDigit(11)',
    expect=9,
    views=[
        dict(type='text', fn=_text, h=120, size=28),
        dict(type='string', var=_s, color=_col, h=200, cell=36, label='无限字符串的前缀（黄 = 第 k 位）'),
    ],
    watch=['k', ('p10', 'p10'), ('length', 'length', 'blue'), ('x', 'x', 'green'), ('b', 'b', 'pink')],
    captions={
        'p10 = 1': '`p10 = 1`：当前位数的最小数 `10^(length-1)`',
        'length = 1': '从 1 位数开始：`length = 1`',
        'while k >': '`length={length}` 的数共占 `{p10}×9×{length} = {p10 * 9 * length}` 位，`k = {k}`：{"k 更大，答案不在这一段" if k > p10 * 9 * length else "k 不超过这一段，答案就在这里"}',
        'k -= p10': '整段扣掉：`k` → {k}',
        'p10 *= 10': '`p10 = {p10}`',
        'length += 1': '`length = {length}`',
        'x = (k - 1)': '`x = (k-1)//length + p10 = {(k - 1) // length} + {p10}` = =={x}==（还没考虑奇偶块）',
        'b = x // 10': '块号 `b = x // 10 = {b}`',
        'if b % 2': '`b = {b}`：{"奇数块，倒序排列" if b % 2 == 1 else "偶数块，正序，x 不变"}',
        'x = x + 9': '个位 d 换成 `9-d`：`x + 9 - 2d` = =={x}==',
        'return': '`str({x})[(k-1) % length]` = `str({x})[{(k - 1) % length}]` = =={ret}==',
    },
    cards=dict(
        one_liner='先找位数，再找第几个数，最后按奇偶块对称翻转',
        complexity='时间 `O(log k)`，空间 `O(1)`',
        problem=['正整数按 10 个一块拼接：偶数块递增，奇数块 ==递减==',
                 '开头 `1..9`、`19..10`、`20..29`、`39..30`……',
                 '求第 `k` 位（下标从 1 开始），示例 `k = 11` → `9`'],
        quote='若b为偶数，那么字符串中的第x个数字就是x自身，反之，则需要将x的最低位变为对称的数字，即使用9减去这个最低位。',
        quote_src='—— yiduobo 题解原文',
        idea=['`length` 位数共 `10^(length-1)·9` 个，占 `·length` 位；`k` 比它大就整段减去',
              '位数确定后，`(k-1)//length + p10` 就是目标数 `x`',
              '`b = x // 10` 为奇数 → 个位 `d` 变 `9-d`，再取 `(k-1) % length` 位'],
        after=[dict(heading='验算 k = 11', lines=['1 位数占 9 位：`k = 11 - 9 = 2`，`length = 2`',
                                                  '`x = (2-1)//2 + 10 = 10`，`b = 1` 奇数',
                                                  '`x = 10 + 9 - 0 = 19`',
                                                  '`"19"[1]` → `9`'])],
        summary=['时间 `O(log k)`，空间 `O(1)`',
                 '易错：`k` 从 1 开始，所以用 `(k - 1)`',
                 '易错：循环条件是 `k > p10*9*length`（不含等号）',
                 '原文已是整数除法 `//`，仅删去了类型说明文档字符串',
                 '`k` 范围到 `10^15`，Python 大整数不会溢出'],
    ),
)
