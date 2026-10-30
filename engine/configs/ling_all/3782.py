N = 11
_STATES = [list(range(1, N + 1))]
while len(_STATES[-1]) > 1:
    _STATES.append(_STATES[-1][::2][::-1])


def _r(S):
    d = S.get('d')
    if d is None:
        return 0
    r = abs(d).bit_length() - 1
    if S['_line'] == 6:
        r -= 1
    return min(r, len(_STATES) - 1)


def _seq(S):
    return _STATES[_r(S)]


def _dim(S, i, v):
    return S['_line'] in (4, 5, 6) and i % 2 == 1 and len(_seq(S)) > 1


def _col(S, i, v):
    return 'blue' if 'start' in S and v == S['start'] else None


def _top(S):
    d = S.get('d')
    if d is None:
        return ''
    return f"公差 `d = {d}`：" + ('正，序列从小到大' if d > 0 else '负，序列已被反转（从大到小）') + f'；公差绝对值 = 2^{abs(d).bit_length() - 1}'


CONFIG = dict(
    num=3782, title='交替删除操作后最后剩下的整数', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='等差数列模拟 · 反转',
    tags=['灵神题单', '位运算', '难度分 2074'],
    code='''
class Solution:
    def lastInteger(self, n: int) -> int:
        start = d = 1  # 等差数列的首项和公差
        while n > 1:
            start += (n - 2 + n % 2) * d
            d *= -2
            n = (n + 1) // 2
        return start
''',
    call='Solution().lastInteger(11)',
    expect=11,
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='array', var=_seq, label='当前序列（蓝 = start 首项，灰 = 本轮要删的奇数下标）', cell=84, h=300,
             dim=_dim, color=_col),
    ],
    watch=[('n', 'n', 'pink'), ('start', 'start', 'blue'), ('d', 'd', 'yellow')],
    captions={
        'start = d = 1': '初始是 `1..n`：首项 `start = 1`，公差 `d = 1`',
        'while n > 1': lambda S, B, r: (f'`n = {S.n} > 1`：还没剩一个，继续操作' if S.n > 1 else '`n = 1`：只剩一个数，结束'),
        'start += ': lambda S, B, r: (f'`n = {B.n}` 是奇数：最后一个数一定保留，新首项 = 原末项 `start + (n-1)·d` → =={S.start}=='
                                      if B.n % 2 else
                                      f'`n = {B.n}` 是偶数：最后一个被删，倒数第二个保留，新首项 = `start + (n-2)·d` → =={S.start}=='),
        'd *= -2': '隔一个删一个 → 公差翻倍；反转序列 → 公差变号：`d` = {B.d} × (−2) = =={d}==',
        'n = (n + 1) // 2': '删掉 `floor(n/2)` 个，剩 `ceil(n/2)` 个：`n` = {B.n} → =={n}==',
        'return start': '只剩一项，它就是 `start` = =={start}==',
    },
    cards=dict(
        one_liner='剩下的永远是等差数列，只维护首项和公差',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['`1..n` 排成一列，交替执行：从左隔一个删一个、从右隔一个删一个',
                 '直到只剩一个数，求它',
                 '示例：`n = 8` → `3`；本视频 `n = 11` → `11`'],
        quote='每次操作，删除所有奇数下标数字……公差初始为 d=1，每次操作把 d 乘以 −2。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每次删奇数下标，剩 `ceil(n/2)` 个，仍是等差数列；每次后把序列==反转==，下次依旧从左删',
              '`n` 奇数：末项保留 → 新首项 `start + (n-1)d`；`n` 偶数：倒数第二项保留 → `start + (n-2)d`',
              '公差翻倍并变号：`d *= -2`'],
        result='4 轮操作后只剩 `11`，与 `((n-1) & 0xAAA…) + 1` 的位运算结果一致 ✓',
        after=[dict(heading='方法二：位运算 O(1)', lines=[
            '改成从 0 开始 `0..n-1`：答案二进制的奇数位（第 1,3,5… 位）一定是 0',
            '偶数位（第 2,4,6… 位）和 `n-1` 的对应位相同',
            '`return ((n - 1) & 0xAAAAAAAAAAAAAAA) + 1`'])],
        summary=['时间 `O(log n)`，空间 `O(1)`；n 可达 10^15，不能真的模拟序列',
                 '==用操作前的 n 和 d== 算新首项，所以 `start` 要先于 `d`、`n` 更新',
                 '奇偶判断：`n - 2 + n % 2` 同时覆盖两种情况',
                 '相似题：390. 消除游戏'],
    ),
)
