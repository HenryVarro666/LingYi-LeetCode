def _x(S):
    x = S.get('x')
    if x is None or 'left' not in S:
        return ''
    n = x.bit_length()
    m = n // 2
    b = format(x, 'b')
    mid = '（奇数位：中间一位在左半里）' if n % 2 else ''
    return f"`x` = {x} = 二进制 `{b[:n - m]}`｜`{b[n - m:]}`　左半 `left` = {x >> m}{mid}"


def _cand(S):
    x, l = S.get('x'), S.get('l')
    if x is None or l is None or 'left' not in S:
        return ''
    ln = S['_line']
    if ln >= 12 and 'pal' in S:
        m = x.bit_length() // 2
        return f"左半 `l` = {l:b} → 回文数 `{S['pal']:b}` = {S['pal']}，离 x 的距离 =={abs(x - S['pal'])}=="
    return f"枚举左半 `l` = {l}（二进制 `{l:b}`）"


def _lefts(S):
    x = S.get('x')
    if x is None or 'left' not in S:
        return []
    return [S['left'] - 1, S['left'], S['left'] + 1]


CONFIG = dict(
    num=3766, title='将数字变成二进制回文数的最少操作', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='枚举回文数的左半 left-1, left, left+1',
    tags=['灵神题单', '位运算'],
    code='''
class Solution:
    def minOperations(self, nums: List[int]) -> List[int]:
        for i, x in enumerate(nums):
            res = inf
            n = x.bit_length()
            m = n // 2
            left = x >> m
            for l in range(left - 1, left + 2):
                # 左半反转到右半
                # 如果 n 是奇数，先去掉正中间的比特，再反转
                right = self.reverseBits(l >> (n % 2)) >> (32 - m)
                pal = l << m | right
                res = min(res, abs(x - pal))
            nums[i] = res
        return nums

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
    call='Solution().minOperations([6, 12])',
    expect=[1, 3],
    skip=['& 0xFFFFFFFF', 'res = inf'],
    max_steps=90,
    views=[
        dict(type='text', fn=_x, size=26),
        dict(type='array', var=_lefts, label='候选左半：left-1, left, left+1（蓝 = 当前枚举的 l）', cell=100, h=170,
             color=lambda S, i, v: 'blue' if v == S.get('l') and S['_line'] >= 8 else None),
        dict(type='text', fn=_cand, size=26),
        dict(type='array', var='nums', label='nums（原地改成答案，蓝 = 当前 i）', cell=100, h=170, pointers={'i': 'blue'}),
    ],
    watch=[('i', 'i', 'blue'), ('x', 'x', 'yellow'), ('left', 'left'), ('l', 'l', 'pink'), ('pal', 'pal', 'green'), ('res', 'res', 'cyan')],
    captions={
        'n = x.bit_length': '`x = {x}` 的二进制是 `{x:b}`，共 `n = {n}` 位',
        'm = n // 2': '`m = n // 2 = {m}`：右半有 `{m}` 位，其余是左半',
        'left = x >> m': '丢掉右半 {m} 位，得到左半 `left = {left}`（二进制 `{left:b}`）',
        'for l in range': lambda S, B, r: (f'相邻回文数的左半是连续的 → 最优回文数的左半只会是 `left-1, left, left+1` 之一，枚举 `l = {S.l}`'
                                           if S.l != B.get('l') or 'l' not in B else f'`left-1, left, left+1` 三个候选都试完了'),
        'right = self.reverseBits': '回文的右半 = 左半反转：`l = {l:b}`' + '{" 先去掉正中间的比特" if n % 2 else ""}' + ' → `right` = {right:b}（{right}）',
        'pal = l << m | right': '拼起来：左半 `{l:b}` + 右半 → 回文数 `{pal:b}` = =={pal}==',
        'res = min': '离 x 的距离 `|{x} − {pal}|` = {abs(x - pal)}，`res = min({B.res}, {abs(x - pal)})` = =={res}==',
        'nums[i] = res': '三个候选里最近的距离是 `{res}`，原地写回 `nums[{i}]`',
        30: '`reverseBits` 把 32 位整数的二进制整个颠倒（五次交换：16/8/4/2/1 位块）；右移 `32-m` 位就留下左半反转后的 `m` 位',
        'return nums': 'nums 已经全是答案：`{nums}`',
    },
    cards=dict(
        one_liner='回文数由左半决定：只需试 left-1、left、left+1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可以把一个数 `+1` 或 `-1`，求把每个 `nums[i]` 变成二进制回文数的最少次数',
                 '就是找离 `x` 最近的二进制回文数',
                 '本视频：`[6, 12]` → `[1, 3]`（6→5，12→15）'],
        quote='对于相邻的回文数，其 left 是连续的。所以最终变成的回文数的左半只会在 left-1, left, left+1 中，其余回文数一定比这三个更远。',
        quote_src='—— 灵茶山艾府题解',
        idea=['知道回文数的左半，就知道右半（左半反转）',
              '取 `x` 的左半 `left`（奇数长度时含正中间那位），枚举 `left-1, left, left+1`',
              '用 `reverseBits` 反转左半拼成回文数，取离 `x` 最近的距离'],
        result='`6 → 5`（1 步），`12 → 15`（3 步）→ `[1, 3]` ✓',
        after=[dict(heading='方法一：预处理 + 二分', lines=[
            '枚举左半，从小到大生成值域内所有二进制回文数 `palindromes`，开头放哨兵 0，末尾放哨兵 5049',
            '`bisect_left` 找到第一个 `≥ x` 的回文数 `j`，答案 `min(pal[j] - x, x - pal[j-1])`',
            '预处理 `O(√U log U)`，每次查询 `O(log U)`'])],
        summary=['时间 `O(n)`，空间 `O(1)`，与值域无关',
                 '奇数长度：先 `l >> 1` 去掉正中间的比特，再反转，否则中间位会重复',
                 '`left-1` 位数变短、`left+1` 位数变长的情况无需特判，`100…0` 与 `100…1` 已覆盖最优解',
                 '视频里省略了 `reverseBits` 内部五行的位交换，只演示它的效果',
                 '相似题：564. 寻找最近的回文数'],
    ),
)
