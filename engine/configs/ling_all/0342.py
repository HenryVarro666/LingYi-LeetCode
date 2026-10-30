def _info(S):
    n = S.get('n')
    if not isinstance(n, int):
        return ''
    b = f'{n:08b}' if n > 0 else str(n)
    m = '01010101'
    s = f'`n = {n} = {b}`'
    if n > 0:
        s += f'，`n & 0x55555555 = {n & 0x55555555}`'
    return s


def _bits(S):
    n = S.get('n')
    return f'{n:08b}' if isinstance(n, int) and 0 < n < 256 else ''


def _mask(S):
    return '01010101'


CONFIG = dict(
    num=342, title='4的幂', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='2 的幂 + 掩码取偶数位',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def isPowerOfFour(self, n: int) -> bool:
        return n > 0 and n & (n - 1) == 0 and n & 0x55555555 > 0
''',
    call='[Solution().isPowerOfFour(n) for n in (16, 8, 1, 5)]',
    expect=[True, False, True, False],
    views=[
        dict(type='text', fn=lambda S: '依次判断 `n = 16, 8, 1, 5`（这里只画低 8 位，真实掩码 `0x55555555` 是 32 位）', h=70),
        dict(type='string', var=_bits, label='n 的低 8 位（高位在左）', h=230, index=False,
             color=lambda S, i, v: 'green' if v == '1' else None, dim=lambda S, i, v: v == '0'),
        dict(type='string', var=_mask, label='掩码 0x55555555 的低 8 位（第 0、2、4、6 位为 1）', h=230, index=False,
             color=lambda S, i, v: 'blue' if v == '1' else None, dim=lambda S, i, v: v == '0'),
        dict(type='text', fn=_info, h=80),
    ],
    watch=[('n', 'n', 'blue')],
    captions={
        'return n > 0': lambda S, B, r: (
            f'`n = {S.n}`：`n > 0` 成立；`n & (n-1) = {S.n & (S.n - 1)}`'
            + ('，==等于 0 → 是 2 的幂==' if S.n > 0 and S.n & (S.n - 1) == 0 else '，不等于 0 → 不是 2 的幂，直接返回 False（后面不用算）')
            + (f'；再看 `n & 0x55555555 = {S.n & 0x55555555}`：'
               + ('大于 0，唯一的 1 落在偶数位 → ==是 4 的幂==' if S.n & 0x55555555 > 0 else '等于 0，唯一的 1 在奇数位 → 是 2 的幂但不是 4 的幂')
               if S.n > 0 and S.n & (S.n - 1) == 0 else '')),
    },
    cards=dict(
        one_liner='先判是 2 的幂，再看唯一的 1 落在偶数位还是奇数位',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['判断整数 `n` 是不是 4 的幂（`n == 4^x`），进阶：不用循环和递归',
                 '例：`16` → `true`，`5` → `false`，`1` → `true`',
                 '本视频依次判断 `16, 8, 1, 5`'],
        quote='取出 n 的二进制的中的从低到高第 0,2,4,6,… 位，如果其中有 1，那么 n 就是 4 的幂；否则不是。',
        quote_src='—— 灵茶山艾府题解',
        idea=['4 的幂必是 2 的幂：`n > 0 and n & (n-1) == 0`',
              '4^k 的唯一的 1 在第 0, 2, 4, … 位；2·4^k 的 1 在第 1, 3, 5, … 位',
              '与 `0x55555555`（二进制 0101…01）相与，结果 > 0 就说明 1 在偶数位'],
        after=[dict(heading='方法二：数学', lines=[
            '`4^k mod 3 = 1`，`2·4^k mod 3 = 2`（二项式定理）',
            '所以在是 2 的幂的前提下，`n % 3 == 1` 就是 4 的幂',
            '代码：`n > 0 and n & (n - 1) == 0 and n % 3 == 1`'])],
        summary=['时间、空间都是 `O(1)`',
                 '`n > 0` 不能省：`0` 和负数不是 4 的幂',
                 '`&` 优先级比 `==`、`>` 高，所以可以不加括号',
                 '本视频用方法一；方法二用 `n % 3 == 1` 代替掩码',
                 '推广：8 的幂可用 `0x49249249`，思考题'],
    ),
)
