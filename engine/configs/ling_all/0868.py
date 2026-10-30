def _bits(S):
    n = S.get('n')
    return bin(n)[2:] if isinstance(n, int) else ''


def _info(S):
    n = S.get('n')
    if not isinstance(n, int):
        return ''
    if n == 0:
        return '`n = 0`：所有 1 都处理完了，循环结束'
    low = n & -n
    s = f'`n = {bin(n)[2:]}`，`lowbit = {bin(low)[2:]}`，尾零个数 = {low.bit_length() - 1}'
    if 'gap' in S and S['_line'] >= 6:
        s += f'；本轮间距 `gap = {S["gap"]}`'
    return s


CONFIG = dict(
    num=868, title='二进制间距', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='lowbit 跳着数间距',
    tags=['灵神题单', '位运算', '难度分 1307'],
    code='''
class Solution:
    def binaryGap(self, n: int) -> int:
        ans = 0
        n //= (n & -n) * 2  # 去掉 n 末尾的 100..0
        while n > 0:
            gap = (n & -n).bit_length()  # n 的尾零个数加一
            ans = max(ans, gap)
            n >>= gap  # 去掉 n 末尾的 100..0
        return ans
''',
    call='Solution().binaryGap(82)',
    expect=3,
    views=[
        dict(type='text', fn=_info, h=70),
        dict(type='string', var=_bits, label='n 的二进制（高位在左）', h=300,
             color=lambda S, i, v: 'green' if v == '1' else None,
             dim=lambda S, i, v: v == '0'),
        dict(type='text', fn=lambda S: '原数 `82 = 1010010`：从右往左的间距是 ==3==（1001）和 ==2==（101）', h=70),
    ],
    watch=[('n', 'n', 'blue'), 'gap', ('ans', 'ans', 'green')],
    captions={
        'n //= (n & -n)': '`n & -n` 是 lowbit；先去掉最右边的 1 和它后面的 0（它前面没有 1，没有间距可算）：`n = {bin(n)[2:]}`',
        'while n > 0': lambda S, B, r: (f'`n = {bin(S.n)[2:]} > 0`，还有 1 没处理' if S.n > 0 else '`n = 0`：没有更多的 1 了 → 结束'),
        'gap = ': '`n & -n = {bin(n & -n)[2:]}`，bit_length 是 {gap}：==尾零个数 + 1 就是它到下一个 1 的间距== `gap = {gap}`',
        'ans = max': '`ans = max({B.ans}, {gap}) = {ans}`',
        'n >>= gap': '右移 `gap` 位，丢掉末尾的 `100..0`，下一个 1 变成最低位：`n = {bin(n)[2:]}`',
        'return ans': '最大间距 `{ans}`',
    },
    cards=dict(
        one_liner='用 lowbit 一次跳过一段 0，只关心 1 的个数',
        complexity='时间 `O(k)`（k 为 1 的个数），空间 `O(1)`',
        problem=['求 `n` 的二进制里，==相邻两个 1 之间的最大距离==，没有相邻的 1 就返回 0',
                 '例：`22 = 10110` → `2`；`8 = 1000` → `0`',
                 '本视频：`82 = 1010010` → `3`'],
        quote='去掉 n 末尾的 10，得到 10100。这一步可以先计算出 n 的 lowbit = 10，然后把 n 更新成 n / (2·lowbit)。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先去掉最右边那个 1 及其后面的 0，之后每个最低位 1 的位置就是前一个 1',
              '`(n & -n).bit_length()` = 尾零个数 + 1 = 到下一个 1 的距离',
              '每轮右移 `gap` 位，等价于去掉末尾的 `100..0`，`ans` 取最大'],
        summary=['时间 `O(k)`，k 为 n 中 1 的个数；空间 `O(1)`',
                 '起手 `n //= (n & -n) * 2` 去掉最右边的 1，不要漏掉',
                 'lowbit 的 bit_length 是尾零数加一，恰好等于间距',
                 '只有一个 1 时第一步后 n=0，直接返回 0'],
    ),
)
