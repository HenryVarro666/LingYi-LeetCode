def _row(name, label, note=''):
    def f(S):
        if name not in S:
            return ''
        v = S[name]
        return f'{label} = `{v:06b}`  ({v}){note}'
    return dict(type='text', fn=f, size=30, h=58)


def _prod(S):
    if S.get('_line', 0) < 27 or 'ax' not in S:
        return ''
    return f'ax × bx = {S["ax"]} × {S["bx"]} = =={S["ax"] * S["bx"]}==，取模得 {S["ax"] * S["bx"] % 1000000007}'


CONFIG = dict(
    num=2939, title='最大异或乘积', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='和为定值 · 基本不等式分配',
    tags=['位运算', '贪心与思维', '难度分 2128'],
    code='''
class Solution:
    def maximumXorProduct(self, a: int, b: int, n: int) -> int:
        if a < b:
            a, b = b, a  # 保证 a >= b

        mask = (1 << n) - 1
        ax = a & ~mask  # 第 n 位及其左边，无法被 x 影响，先算出来
        bx = b & ~mask
        a &= mask  # 低于第 n 位，能被 x 影响
        b &= mask

        left = a ^ b  # 可分配：a XOR x 和 b XOR x 一个是 1 另一个是 0
        one = mask ^ left  # 无需分配：a XOR x 和 b XOR x 均为 1
        ax |= one  # 先加到异或结果中
        bx |= one

        # 现在要把 left 分配到 ax 和 bx 中
        # 根据基本不等式（均值定理），分配后应当使 ax 和 bx 尽量接近，乘积才能尽量大
        if left > 0 and ax == bx:
            # 尽量均匀分配，例如把 1111 分成 1000 和 0111
            high_bit = 1 << (left.bit_length() - 1)
            ax |= high_bit
            left ^= high_bit
        # 如果 a & ~mask 更大，则应当全部分给 bx（注意最上面保证了 a>=b）
        bx |= left

        return ax * bx % 1_000_000_007
''',
    call='Solution().maximumXorProduct(5, 12, 4)',
    expect=98,
    views=[
        _row('a', 'a    '), _row('b', 'b    '), _row('mask', 'mask '),
        _row('ax', 'ax   ', '  ← 目标：a^x'), _row('bx', 'bx   ', '  ← 目标：b^x'),
        _row('one', 'one  ', '  两边都是 1'), _row('left', 'left ', '  待分配'),
        dict(type='text', fn=_prod, size=30, h=60),
    ],
    watch=['a', 'b', 'n', 'ax', 'bx', 'left'],
    captions={
        'if a < b': lambda S, B, r: ('`{S.a} < {S.b}`：要交换，之后 a ≥ b'.format(S=S) if S.a < S.b else '`a ≥ b`：不用交换'),
        'mask = ': '`mask = (1 << {n}) - 1 = {mask:b}`：x 只能改低 {n} 位',
        'ax = a & ~mask': '高于第 n 位的部分 x 改不了：`ax = {ax:b}`',
        'bx = b & ~mask': '`bx = {bx:b}`',
        'a &= mask': '`a` 只剩低 n 位：`{a:b}`',
        'b &= mask': '`b` 只剩低 n 位：`{b:b}`',
        'left = a ^ b': '`a ^ b = {left:b}`：这些位一个 1 一个 0，无论 x 怎么取 1 的个数不变——==可分配==',
        'one = mask': '其余位 a、b 相同，x 取反就能让两边都是 1：`one = {one:b}`',
        'ax |= one': '两边先各加上 `one`：`ax = {ax:b}`',
        'bx |= one': '`bx = {bx:b}`，此时 ax + bx 的可分配部分之和是定值 `{left}`',
        'if left > 0': lambda S, B, r: (f'`left = {S.left:b} > 0` 且 `ax == bx`（{S.ax} == {S.bx}）→ 要分配：和一定，越接近乘积越大' if S.left > 0 and S.ax == S.bx
                                       else '不需要均分：高位已经让 ax 更大，余下全给 bx'),
        'high_bit =': '均值定理：把 left 的最高位给 ax，其余给 bx：`high_bit = {high_bit:b}`',
        'ax |= high_bit': '`ax = {ax:b}`（{ax}）',
        'left ^= high_bit': '剩下的 `left = {left:b}`',
        'bx |= left': '剩下的全给 bx：`bx = {bx:b}`（{bx}）',
        'return': '`{ax} × {bx} = {ax * bx}`，取模后 =={ret}==',
    },
    cards=dict(
        one_liner='可分配的位和为定值，分得越均匀乘积越大',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['给 `a`、`b`、`n`，选 `0 ≤ x < 2^n`',
                 '求 `(a XOR x) × (b XOR x)` 的最大值，对 `10^9+7` 取模',
                 '示例：`a=12, b=5, n=4` → `98`（x=2）'],
        quote='ax 和 bx 之和是一个定值！根据基本不等式（均值定理），在和为定值的前提下，要让乘积尽量大，应当让 ax 与 bx 尽量接近。',
        quote_src='—— 灵茶山艾府题解',
        idea=['a、b 相同的位：x 取反，两边都是 1，==先拿下==',
              'a、b 不同的位：一个 1 一个 0，是「可分配」的位，和是定值',
              '最高的可分配位给 ax，其余给 bx，最接近；高位 a 更大时全给 bx'],
        summary=['时间、空间 `O(1)`（位数最多 50）',
                 '先交换保证 `a ≥ b`；高于 n 位的部分 x 改不了，先分出来',
                 '易错：只有 `ax == bx` 时才均分，否则 bx 拿全部 left',
                 '取模放在最后：先算大整数乘积再 `% (10^9+7)`，Python 不会溢出'],
    ),
)
