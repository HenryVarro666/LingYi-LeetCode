N0 = 45  # 示例 n = 0b101101


def _in_rev(S):
    return 'left' not in S.get('_inner', {}) and 'self' in S.get('_inner', {}) and 'n' in S.get('_inner', {}) and S['_inner'].get('left') is None and 'm' not in S['_inner']


def _bits(S):
    return format(N0, 'b')


def _pal(S):
    if 'right' in S and 'left' in S and 'm' in S and not _in_rev(S):
        return format(S['left'] << (S['m'] // 2) | S['right'], 'b').zfill(S['m'])
    return ''


def _bcolor(S, i, v):
    m = len(bin(N0)) - 2
    if 'left' not in S:
        return None
    return 'blue' if i < m - m // 2 else None


def _pcolor(S, i, v):
    m = S.get('m', len(bin(N0)) - 2)
    return 'blue' if i < m - m // 2 else 'pink'


def _txt(S):
    inner = S.get('_inner', {})
    if _in_rev(S):
        b = format(inner['n'], '032b')
        return '32 位的 `n`：`' + ' '.join(b[i:i + 8] for i in range(0, 32, 8)) + '`'
    if 'm' not in S:
        return f'示例 `n = {N0}` = 二进制 `{bin(N0)[2:]}`'
    m = S['m']
    if 'k' not in S:
        return f'`n` 的二进制长度 `m = {m}`'
    if 'left' not in S:
        return f'二进制长度 `< {m}` 的回文数：`ans = {S["ans"]}`'
    if 'right' not in S:
        return f'`n` 的左半 `left = {bin(S["left"])[2:]}`（前 {m - m // 2} 位）'
    return f'回文数 = 左半 `{bin(S["left"])[2:]}` + 翻转后的右半 → `{_pal(S)}`，对比 `n = {bin(N0)[2:]}`'


CONFIG = dict(
    num=3677, title='统计二进制回文数字的数目', difficulty='Hard', category='动态规划',
    author='灵茶山艾府', technique='数位 DP 的数学写法 · 左半枚举',
    tags=['灵神题单·动态规划', '灵神题单·数学算法', '难度分 2223'],
    code='''
class Solution:
    def countBinaryPalindromes(self, n: int) -> int:
        if n == 0:
            return 1

        m = n.bit_length()
        k = (m - 1) // 2

        # 二进制长度小于 m
        ans = (2 << k) - 1
        if m % 2 == 0:
            ans += 1 << k

        # 二进制长度等于 m，且回文数的左半小于 n 的左半
        left = n >> (m // 2)
        ans += left - (1 << k)

        # 二进制长度等于 m，且回文数的左半等于 n 的左半
        right = self.reverseBits(left >> (m % 2)) >> (32 - m // 2)
        if left << (m // 2) | right <= n:
            ans += 1

        return ans

    # 190. 颠倒二进制位
    # https://leetcode.cn/problems/reverse-bits/
    def reverseBits(self, n: int) -> int:
        # 交换 16 位
        n = ((n >> 16) | (n << 16)) & 0xFFFFFFFF
        # 交换每个 8 位块
        n = (((n & 0xFF00FF00) >> 8) | ((n & 0x00FF00FF) << 8)) & 0xFFFFFFFF
        # 交换每个 4 位块
        n = (((n & 0xF0F0F0F0) >> 4) | ((n & 0x0F0F0F0F) << 4)) & 0xFFFFFFFF
        # 交换每个 2 位块
        n = (((n & 0xCCCCCCCC) >> 2) | ((n & 0x33333333) << 2)) & 0xFFFFFFFF
        # 交换相邻位
        n = (((n & 0xAAAAAAAA) >> 1) | ((n & 0x55555555) << 1)) & 0xFFFFFFFF
        return n
''',
    call=f'Solution().countBinaryPalindromes({N0})',
    expect=13,
    views=[
        dict(type='text', fn=_txt, size=24, h=80),
        dict(type='string', var=_bits, label='n 的二进制（蓝 = 左半，含回文中心）', cell=90, color=_bcolor, h=190),
        dict(type='string', var=_pal, label='用 n 的左半造出的回文数（蓝 = 左半，粉 = 翻转得到的右半）', cell=90, color=_pcolor, h=190),
    ],
    watch=['m', 'k', 'left', 'right', ('ans', 'ans', 'green')],
    skip=['if n == 0', 'return 1', 'if m % 2 == 0'],
    captions={
        'm = n.bit_length()': '`n = {n}` 的二进制是 `{bin(n)[2:]}`，长度 `m = {m}`',
        'k = (m - 1) // 2': '`k = (m−1)//2 = {k}`：长度 `2i−1` 和 `2i` 的回文数一样多，按两个长度一组',
        'ans = (2 << k) - 1': '长度 `< m` 的回文数：`0` 一个，长 1、2 共 `2^1` 个，长 3、4 共 `2^2` 个……累加 = `2^{k+1} − 1` = =={ans}==',
        'ans += 1 << k': lambda S, B, r: f'`m = {S.m}` 是偶数，还要加上长度 `m−1` 的回文数：`2^{S.k}` = {1 << S.k} → `ans = {S.ans}`',
        'left = n >> (m // 2)': '`n` 的左半（含回文中心）：`n >> {m//2}` = `{bin(left)[2:]}` = {left}',
        'ans += left - (1 << k)': '长度 `m` 且左半 `< left` 的回文数：左半最小 `2^k = {1<<k}`，最大 `left−1` → `{left} − {1<<k}` 个 → `ans = {ans}`',
        'right = self.reverseBits': '把左半翻转放到右半：先去掉回文中心（`m` 奇数时），32 位翻转后右移 `32 − {m//2}` 位',
        'if left << (m // 2)': lambda S, B, r: (f'左半等于 `left` 的回文数 `{bin(S.left << (S.m // 2) | S.right)[2:]}` = {S.left << (S.m // 2) | S.right} '
                                                 + ('≤' if (S.left << (S.m // 2) | S.right) <= N0 else '>') + f' `n = {N0}`' +
                                                 ('，它也满足要求 → 答案加一' if (S.left << (S.m // 2) | S.right) <= N0 else '，超过 `n` → 不计')),
        'ans += 1': '`ans = {ans}`',
        'return ans': '长度 `< m`、长度 `m` 且左半更小、左半相等且 `≤ n`，三类相加 = =={ret}==',
        '(n >> 16)': '交换高低 16 位：`n = {n:032b}`',
        '0xFF00FF00': '每个 8 位块内交换：`n = {n:032b}`',
        '0xF0F0F0F0': '每个 4 位块内交换：`n = {n:032b}`',
        '0xCCCCCCCC': '每个 2 位块内交换：`n = {n:032b}`',
        '0xAAAAAAAA': '交换相邻位：整个 32 位串完成翻转，`n = {n:032b}`',
        'return n': '`reverseBits` 返回翻转后的 32 位数',
    },
    cards=dict(
        one_liner='回文数由左半决定：左半更小的随便数，左半相等的只验一个',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['非负整数的二进制（不含前导零）正读倒读一样，就是==二进制回文数==，`0` 也算',
                 '求 `0 ≤ k ≤ n` 中二进制回文数的个数',
                 '示例：`n = 9` → `6`（`0, 1, 3, 5, 7, 9`），`n` 最大约 `10^15`'],
        quote='对于二进制长度小于 m 的回文数，其左半边可以随便填：把左半边翻转，得到右半边，把左半右半拼起来，就是一个回文数了。',
        quote_src='—— 灵茶山艾府题解',
        idea=['回文数由左半边唯一确定，所以数回文数就是数合法的左半边',
              '长度 `< m`：每个长度分别算，写法二把它们合并成等比求和',
              '长度 `= m`：左半小于 `n` 的左半都行；左半相等时造出回文数与 `n` 比大小'],
        summary=['时间 `O(1)`：这里 `reverseBits` 是固定 5 步的位运算',
                 '写法一：从高到低枚举 `n` 的每一位，是 `1` 就让回文数填 `0`，后面随便填，时间 `O(log n)`；本视频演示写法二',
                 '易错：`0` 单独算一个；最高位必须是 `1`；左半含回文中心（`m` 奇数时）',
                 '`left << (m//2) | right <= n`：`|` 优先级高于 `<=`，所以先拼再比较'],
    ),
)
