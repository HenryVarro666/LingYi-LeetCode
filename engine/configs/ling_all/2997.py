def _x(S):
    s = reduce(xor, S['nums'])
    k = S['k']
    x = s ^ k
    return f"异或和 `s = {s:04b}`　`k = {k:04b}`　`x = s ⊕ k = ` ==%s==　1 的个数 = =={x.bit_count()}==" % f"{x:04b}"

CONFIG = dict(
    num=2997, title='使数组异或和等于 K 的最少操作次数', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='x = s⊕k 的 1 的个数',
    tags=['灵神题单', '位运算', '难度分 1525'],
    code='''
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        return (reduce(xor, nums) ^ k).bit_count()
''',
    call='Solution().minOperations([2,1,3,4], 1)',
    expect=2,
    views=[
        dict(type='array', var='nums', label='nums', h=170),
        dict(type='text', fn=_x, size=30, h=100),
    ],
    watch=['k', ('异或和 s', 'reduce(xor, nums)', 'blue'), ('x = s^k', 'reduce(xor, nums) ^ k', 'yellow')],
    captions={
        'return': lambda S, B, ret: f"`s = {reduce(xor, S['nums'])}`，`x = s ^ k = {reduce(xor, S['nums']) ^ S['k']}`（二进制 `{(reduce(xor, S['nums']) ^ S['k']):b}`）。翻转任一数的某一位，x 的这一位也跟着翻转；要让 x 变 0，每个 1 都得翻一次 → 答案 = x 的 1 的个数 = =={ret}==",
    },
    cards=dict(
        one_liner='s 要变成 k，等价于 s⊕k 要变成 0',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次操作可翻转 `nums` 中任意一个数的任意一个二进制位',
                 '求让所有数异或和等于 `k` 的最少操作次数',
                 '示例：`nums=[2,1,3,4], k=1` → `2`'],
        quote='设 x = s⊕k，我们把 nums 中的任意数字的某个比特位翻转，那么 x 的这个比特位也会翻转。要让 x=0，就必须把 x 中的每个 1 都翻转，所以 x 中的 1 的个数就是我们的操作次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`s = k` 等价于 `s ⊕ k = 0`，令 `x = s ⊕ k`',
              '翻转某个数的第 j 位，`x` 的第 j 位同步翻转',
              '`x` 里每个 1 至少要翻一次，且一次就够：答案是 `x.bit_count()`'],
        after=[dict(heading='为什么答案一定够用', lines=['x 中有 c 个 1，就在任意一个数上依次翻转这 c 个位，x 恰好归零',
                                           '少于 c 次做不到：每次操作只能改变 x 的一位',
                                           '所以下界和上界都是 `c`'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '一行：`(reduce(xor, nums) ^ k).bit_count()`',
                 '注意 `bit_count` 需要 Python 3.10+',
                 '易错：可以翻转前导 0，所以 k 的高位也能凑出来'],
    ),
)
