def _bas(S):
    b = S.get('b')
    if b is None:
        return None
    return b.b if hasattr(b, 'b') else b


def _bin(v, w=3):
    return format(v, f'0{w}b')


def _txt(S):
    b = _bas(S)
    if b is None or 'nums' not in S:
        return ''
    w = max(len(b), 1)
    inner = S.get('_inner', {})
    parts = []
    if 'x' in inner:
        parts.append(f"x = `{_bin(inner['x'], w)}`")
    if 'res' in inner:
        parts.append(f"res = ==`{_bin(inner['res'], w)}`==")
    basis = '　'.join(f"b[{i}]=`{_bin(v, w)}`" for i, v in enumerate(b) if v)
    parts.append('基：' + (basis or '（空）'))
    return '　'.join(parts)


CONFIG = dict(
    num=3681, title='子序列最大 XOR 值', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='线性基 · 最高位互不相同',
    tags=['灵神题单·位运算', '位运算 · 七、线性基'],
    code='''
class XorBasis:
    # n 为值域最大值 U 的二进制长度，例如 U=1e9 时 n=30
    def __init__(self, n: int):
        self.b = [0] * n

    def insert(self, x: int) -> None:
        b = self.b
        # 从高到低遍历，保证计算 max_xor 的时候，参与 XOR 的基的最高位（或者说二进制长度）是互不相同的
        for i in range(len(b) - 1, -1, -1):
            if x >> i:  # 由于大于 i 的位都被我们异或成了 0，所以 x >> i 的结果只能是 0 或 1
                if b[i] == 0:  # x 和之前的基是线性无关的
                    b[i] = x  # 新增一个基，最高位为 i
                    return
                x ^= b[i]  # 保证每个基的二进制长度互不相同
        # 正常循环结束，此时 x=0，说明一开始的 x 可以被已有基表出，不是一个线性无关基

    def max_xor(self) -> int:
        b = self.b
        res = 0
        # 从高到低贪心：越高的位，越必须是 1
        # 由于每个位的基至多一个，所以每个位只需考虑异或一个基，若能变大，则异或之
        for i in range(len(b) - 1, -1, -1):
            if res ^ b[i] > res:  # 手写 max 更快
                res ^= b[i]
        return res

class Solution:
    def maxXorSubsequences(self, nums: List[int]) -> int:
        m = max(nums).bit_length()
        b = XorBasis(m)
        for x in nums:
            b.insert(x)
        return b.max_xor()
''',
    call='Solution().maxXorSubsequences([5, 2, 7, 3])',
    expect=7,
    views=[
        dict(type='array', var='nums', label='nums（逐个插入基）', h=190),
        dict(type='array', var=_bas, label='线性基 b[i]：最高位恰为 i 的基（0 = 还没有）', h=210,
             pointers={'i': 'pink'}, color=lambda S, i, v: 'green' if v else None),
        dict(type='text', fn=_txt, size=28, h=140),
    ],
    watch=[('m', 'm', 'cyan'), ('x', 'x', 'blue'), ('i', 'i', 'pink'), ('res', 'res', 'green')],
    captions={
        'm = max(nums).bit_length()': '最大值 `{max(nums)}` 的二进制长度是 `{m}`：基只需要 `{m}` 位',
        'self.b = [0] * n': '基数组 `b` 有 `{n}` 格，`b[i]` 存==最高位恰为 i==的基',
        'if x >> i': lambda S, B, r: (f"`x >> {S.i}` = `{S.x >> S.i}`：x 的最高位在第 `{S.i}` 位，要看这一档有没有基"
                                       if S.x >> S.i else f"`x >> {S.i}` = 0：x 没有第 `{S.i}` 位，往低位找"),
        'if b[i] == 0': lambda S, B, r: (f"`b[{S.i}] = 0`：这一档还没有基 → x 线性无关" if S.b[S.i] == 0
                                          else f"`b[{S.i}] = {S.b[S.i]}` 已有基 → 用它把 x 的第 `{S.i}` 位消掉"),
        'b[i] = x': '新增一个基：`b[{i}] = {x}`，最高位正好是第 `{i}` 位',
        'x ^= b[i]': 'x 和基异或，第 `{i}` 位被消成 0 → `x = {x}`',
        13: '新增了基，这个数处理完：结束 `insert`',
        'return b.max_xor()': '全部插入完毕，调用 `max_xor()` 做高位优先贪心',
        'return res': '最大异或和 = ==`{res}`==',
        'if res ^ b[i] > res': lambda S, B, r: (f"`res ^ b[{S.i}] = {S.res ^ S.b[S.i]}` > `res = {S.res}`：异或后更大 → 要异或"
                                                 if S.res ^ S.b[S.i] > S.res else f"`res ^ b[{S.i}] = {S.res ^ S.b[S.i]}` 不比 `res = {S.res}` 大 → 跳过"),
        'res ^= b[i]': '高位优先：`res` 变成 =={res}==',
    },
    max_steps=70,
    cards=dict(
        one_liner='选两个子序列等价于选一个：线性基求最大异或和',
        complexity='时间 `O(n log U)`，空间 `O(log U)`',
        problem=['选两个（可空、可重叠）子序列，`X`、`Y` 分别是各自元素的异或',
                 '求 `X XOR Y` 的最大值',
                 '示例：`nums = [1,2,3]` → `3`；本视频用 `[5,2,7,3]` → `7`'],
        quote='由于同一个数选奇数次等价于选一次，选偶数次等价于不选，所以还是等价于选一个子序列。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一个数异或两次抵消，所以问题变成：选一个子序列使异或和最大',
              '线性基：每个数用已有基消去最高位，剩下的非零数成为新基',
              '求最大值：从高位到低位，异或后更大就异或，每档最多一个基'],
        summary=['时间 `O(n log U)`，空间 `O(log U)`',
                 '`insert`：从高到低遍历，每个基的最高位互不相同',
                 '`max_xor`：越高的位越必须是 1，所以高位优先贪心',
                 '易错点：基的大小是 `max(nums).bit_length()`，不是 32',
                 '同类题：3630 划分数组得到最大异或运算和与运算之和'],
    ),
)
