def _hi(S, k):
    """tables: highlight the subset indices being written / compared"""
    if 'j' in S and 'i' in S and S.get('u') is not None and S['_line'] >= 54:
        return {S['i']: 'blue', S['j']: 'pink'}
    if 'high_bit' in S.get('_inner', {}) and 'mask' in S.get('_inner', {}):
        return {S['high_bit'] | S['mask']: 'yellow'}
    return {}


def _col(S, i, v):
    return _hi(S, 0).get(i)


def _bits(v, w):
    return format(v, f'0{w}b')


def _txt(S):
    nums = S['nums']
    w = max(nums).bit_length() if nums else 1
    if 'j' in S and 'i' in S and S['_line'] >= 54 and 'sub_or' in S:
        i, j = S['i'], S['j']
        B = [x for k, x in enumerate(nums) if i >> k & 1]
        Sset = [x for k, x in enumerate(nums) if j >> k & 1]
        bound = S['sub_and'][i] + S['sub_or'][j] * 2 - S['sub_xor'][j]
        return (f"B = `{B}`，AND(B) = `{S['sub_and'][i]}`；剩余 S = `{Sset}`，XOR(S) = `{S['sub_xor'][j]}`，OR(S) = `{S['sub_or'][j]}`\n"
                f"上界 = `{S['sub_and'][i]} + 2×{S['sub_or'][j]} − {S['sub_xor'][j]}` = ==`{bound}`==，当前 ans = ==`{S['ans']}`==")
    inner = S.get('_inner', {})
    bs = None
    if 'self' in inner and hasattr(inner['self'], 'b'):
        bs = inner['self'].b
    elif 'b' in inner and hasattr(inner['b'], 'b'):
        bs = inner['b'].b
    elif isinstance(inner.get('b'), list):
        bs = inner['b']
    if bs is not None and S['_line'] < 54:
        basis = '　'.join(f"b[{k}]=`{_bits(v, w)}`" for k, v in enumerate(bs) if v) or '（空）'
        return f"线性基：{basis}"
    return '枚举 B 的子集；剩下的 S 拆成 A、C，只关心 XOR(A)+XOR(C) 的最大值'


CONFIG = dict(
    num=3630, title='划分数组得到最大异或运算和与运算之和', difficulty='Hard', category='位运算',
    author='灵茶山艾府', technique='枚举 B + 线性基 + 最优性剪枝',
    tags=['灵神题单·位运算', '位运算 · 七、线性基', '难度分 2744'],
    code='''
# 线性基模板
class XorBasis:
    def __init__(self, n: int):
        self.b = [0] * n

    def insert(self, x: int) -> None:
        b = self.b
        while x:
            i = x.bit_length() - 1  # x 的最高位
            if b[i] == 0:  # x 和之前的基是线性无关的
                b[i] = x  # 新增一个基，最高位为 i
                return
            x ^= b[i]  # 保证参与 max_xor 的基的最高位是互不相同的，方便我们贪心
        # 正常循环结束，此时 x=0，说明一开始的 x 可以被已有基表出，不是一个线性无关基

    def max_xor(self) -> int:
        b = self.b
        res = 0
        # 从高到低贪心：越高的位，越必须是 1
        # 由于每个位的基至多一个，所以每个位只需考虑异或一个基，若能变大，则异或之
        for i in range(len(b) - 1, -1, -1):
            if res ^ b[i] > res:
                res ^= b[i]
        return res

class Solution:
    def maximizeXorAndXor(self, nums: List[int]) -> int:
        n = len(nums)
        sz = max(nums).bit_length()

        # 多算一个子集 OR，用于剪枝
        u = 1 << n
        sub_and = [0] * u
        sub_xor = [0] * u
        sub_or = [0] * u
        sub_and[0] = -1
        for i, x in enumerate(nums):
            high_bit = 1 << i
            for mask in range(high_bit):
                sub_and[high_bit | mask] = sub_and[mask] & x
                sub_xor[high_bit | mask] = sub_xor[mask] ^ x
                sub_or[high_bit | mask] = sub_or[mask] | x
        sub_and[0] = 0

        def max_xor2(sub: int) -> int:
            b = XorBasis(sz)
            xor = sub_xor[sub]
            for i, x in enumerate(nums):
                if sub >> i & 1:
                    b.insert(x & ~xor)
            return xor + b.max_xor() * 2

        ans = 0
        for i in range(u):
            j = (u - 1) ^ i
            if sub_and[i] + sub_or[j] * 2 - sub_xor[j] > ans:  # 有机会让 ans 变得更大
                ans = max(ans, sub_and[i] + max_xor2(j))
        return ans
''',
    call='Solution().maximizeXorAndXor([2, 3])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（第 k 个数对应掩码的第 k 位；下表列 = 子集掩码）', h=170),
        dict(type='grid', var=lambda S: [S['sub_and'], S['sub_xor'], S['sub_or']] if 'sub_or' in S else None,
             label='每个子集（列 = 掩码）的 AND / XOR / OR', rows=['AND', 'XOR', 'OR'], cols=lambda S: [f'{m}={m:0{len(S["nums"])}b}' for m in range(len(S['sub_and']))] if 'sub_and' in S else [],
             color=lambda S, i, j, v: _hi(S, 0).get(j), h=250),
        dict(type='text', fn=_txt, size=25, h=160),
    ],
    watch=[('u', 'u', 'cyan'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'for mask in range(high_bit)': '已有子集 `0..{high_bit - 1}` 各自加上 `nums[{i}]`，得到子集 `{high_bit}..{2 * high_bit - 1}`',
        'sub_and[0] = -1': '空集的 AND 先设为 `-1`（全 1），这样 `-1 & x = x`，递推才对',
        'sub_and[high_bit | mask] =': '子集 `{high_bit | mask}` = 子集 `{mask}` 加上 `nums[{i}] = {x}`：AND → `{sub_and[high_bit | mask]}`',
        'sub_xor[high_bit | mask] =': 'XOR → `{sub_xor[high_bit | mask]}`',
        'sub_or[high_bit | mask] =': 'OR → `{sub_or[high_bit | mask]}`（多算它，为了剪枝）',
        'sub_and[0] = 0': '空集 AND 定义为 0，改回来',
        'j = (u - 1) ^ i': '`i` 当作 B，补集 `j = {j}` 就是要拆成 A、C 的 S',
        'if sub_and[i] + sub_or[j] * 2': lambda S, B, r: (
            f"上界 `AND(B) + 2·OR(S) − XOR(S)` = `{S.sub_and[S.i]} + 2×{S.sub_or[S.j]} − {S.sub_xor[S.j]}` = {S.sub_and[S.i] + S.sub_or[S.j] * 2 - S.sub_xor[S.j]}，"
            + (f"> `ans = {S.ans}` → ==有机会变大，细算==" if S.sub_and[S.i] + S.sub_or[S.j] * 2 - S.sub_xor[S.j] > S.ans
               else f"≤ `ans = {S.ans}` → ==不可能变大，跳过线性基==")),
        'ans = max(ans, sub_and[i] + max_xor2(j))': '调用 `max_xor2(j)`：先算 S 拆成 A、C 的最大 `XOR(A)+XOR(C)`，再加 `AND(B)` 去更新 `ans`',
        'for i in range(len(b) - 1': '从高位到低位看基 `b[i]`',
        'return res': '`max_xor` = ==`{res}`==',
        12: '新增了基，这个数处理完：结束 `insert`',
        'xor = sub_xor[sub]': '`xor = XOR(S) = {xor}`：这些位上 A 与 C 的异或和之和恒为 1，贡献固定',
        'b.insert(x & ~xor)': '只保留偶数个 1 的位：插入 `x & ~xor = {x & ~xor}`',
        'return xor + b.max_xor() * 2': '`XOR(S) + 2·max_xor` = `{xor} + 2×{b.max_xor()}` = =={xor + b.max_xor() * 2}==',
        'b[i] = x': '新增基：`b[{i}] = {x}`',
        'x ^= b[i]': '用基消去最高位 → `x = {x}`',
        'if res ^ b[i] > res': '`res ^ b[{i}] = {res ^ b[i]}` vs `res = {res}`：更大才异或',
        'return ans': '答案 = ==`{ans}`==',
    },
    skip=['sub_and[0] = -1', 'high_bit = 1 << i', 'b = self.b', 'res = 0', 'b = XorBasis(sz)', 'n = len(nums)', 'sz = max(nums)'],
    max_steps=100,
    cards=dict(
        one_liner='枚举 B，剩下的 A、C 化成线性基求最大异或',
        complexity='时间 `O(n·2^n·log U)`，空间 `O(2^n + log U)`',
        problem=['把 `nums` 划成三个可空子序列 `A、B、C`，最大化 `XOR(A) + AND(B) + XOR(C)`',
                 '空序列的 XOR 和 AND 都按 0 算',
                 '示例：`[2,3]` → `5`（A=[3]，B=[2]，C=[]）；`[1,3,2]` → `6`'],
        quote='枚举 nums 的子集作为 B，这样我们只需专注 XOR 的问题。',
        quote_src='—— 灵茶山艾府题解',
        idea=['枚举 B 后，剩余 S 拆成 A、C：`XOR(A)+XOR(C) = XOR(S) + 2·XOR(A\')`',
              '奇数个 1 的位贡献恒为 1；偶数个 1 的位才可能贡献 2，把 S 里其他位清零得 S\'，在 S\' 上做线性基最大异或',
              '剪枝：上界 `AND(B) + 2·OR(S) − XOR(S)` 不超过 `ans` 就跳过线性基'],
        after=[dict(heading='优化前后', lines=[
            '优化前：对每个子集 B 都跑一次线性基，`ans = max(sub_and[i] + max_xor2(...))`',
            '优化后：多预处理子集 OR，用上界剪枝，大多数 B 不必再算线性基'])],
        summary=['时间 `O(n·2^n·log U)`，空间 `O(2^n + log U)`',
                 '`sub_and[0]` 先设 `-1` 做递推，之后改回 `0`（空集 AND 定义为 0）',
                 '线性基只对「偶数个 1 的位」建：`x & ~xor`',
                 '易错点：答案是 `XOR(S) + 2·最大异或`，别漏掉 `XOR(S)` 这一项',
                 '同类题：3681 子序列最大 XOR 值（线性基模板）'],
    ),
)
