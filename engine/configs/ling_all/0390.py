def _eff(S):
    """(start, d, n) 一轮更新完成后的值（L5/L6 执行完时 d、n 还没改，这里提前算好）"""
    st, d, n, ln = S['start'], S['d'], S['n'], S['_line']
    if ln == 5:
        d, n = d * -2, n // 2
    elif ln == 6:
        n = n // 2
    return st, d, n


_zero = lambda S: 0


def _seq(S):
    if 'start' not in S or 'd' not in S:
        return list(range(1, S['n'] + 1)) if 'n' in S else []
    st, d, n = _eff(S)
    return [st + i * d for i in range(n)]


def _txt(S):
    if 'start' not in S or 'd' not in S:
        return ''
    st, d, n = _eff(S)
    return f'等差数列：首项 `{st}`，公差 `{d}`，共 `{n}` 个，末项 `{st + (n - 1) * d}`'


CONFIG = dict(
    num=390, title='消除游戏', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='等差数列 + 每次反转',
    tags=['位运算', '数学算法', '难度分 3782'],
    code='''
class Solution:
    def lastRemaining(self, n: int) -> int:
        start = d = 1  # 等差数列的首项和公差
        while n > 1:
            start += (n - 1 - n % 2) * d
            d *= -2
            n //= 2
        return start
''',
    call='Solution().lastRemaining(9)',
    expect=6,
    views=[
        dict(type='text', fn=_txt, size=30, h=70),
        dict(type='array', var=_seq, label='当前序列（每轮删偶数下标，再反转）', cell=84, h=190,
             pointers={_zero: 'blue'}, pointer_labels={_zero: 'start'}),
    ],
    watch=[('start', 'start', 'blue'), ('d', 'd', 'purple'), ('n', 'n', 'cyan')],
    captions={
        'start = d = 1': '序列 `1..n` 就是首项 `1`、公差 `1` 的等差数列，只记 `start` 和 `d`，不真的删',
        'while n > 1': lambda S, B, r: (f'`n = {S.n} > 1`，还没剩一个 → 再操作一轮' if S.n > 1 else '`n = 1`，只剩一个数 → 结束'),
        'start +=': lambda S, B, r: (
            f'`n = {B.n}` 是{"奇" if B.n % 2 else "偶"}数：'
            + ('末项被删，保留倒数第二个' if B.n % 2 else '末项一定保留')
            + f'。新首项 = 旧首项 + `({B.n}-1-{B.n % 2}) × {B.d}` = =={S.start}=='),
        'd *= -2': '隔一个留一个，公差翻倍；下轮从另一端开始 = 反转序列，所以乘 `-2`：`d = {d}`',
        'n //= 2': '每轮删掉一半（上取整），剩 `n // 2 = {n}` 个',
        'return start': '只剩一个数，就是首项 `start` = =={start}==',
    },
    cards=dict(
        one_liner='不真的删数：只维护等差数列的首项、公差、个数',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`[1..n]` 先从左往右删，再从右往左删，交替进行，直到剩一个数',
                 '每次：删第一个，然后隔一个删一个',
                 '示例：`n = 9` → `6`；`n = 1` → `1`'],
        quote='把序列==反转==，那么下次操作相当于还是从左侧开始删。序列 [8,6,4,2] 是一个首项为 8，公差为 -2 的等差数列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每轮都删偶数下标，隔项取数仍是等差数列，公差乘 `-2`（负号 = 反转）',
              '`n` 偶数：末项保留，新首项 = 末项 `start+(n-1)d`',
              '`n` 奇数：末项被删，新首项 = 倒数第二项 `start+(n-2)d`'],
        summary=['时间 `O(log n)`：每轮个数减半',
                 '易错点：`n` 奇偶决定新首项取末项还是倒数第二项，`n % 2` 刚好统一',
                 '`d` 的符号记录方向，不要漏掉负号',
                 '题解的方法二（位运算）：`((n | 0x55555555) & mask2) + 1`，`O(1)`'],
    ),
)
