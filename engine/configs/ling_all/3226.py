def _b(x):
    return format(x, '04b')


CONFIG = dict(
    num=3226, title='使两个整数相等的位更改次数', difficulty='Easy', category='位运算',
    author='灵茶山艾府', technique='集合论：子集判断 + 异或计数',
    tags=['灵神题单', '位运算', '难度分 1247'],
    code='''
class Solution:
    def minChanges(self, n: int, k: int) -> int:
        return -1 if n & k != k else (n ^ k).bit_count()
''',
    call='Solution().minChanges(13, 4)',
    expect=2,
    views=[
        dict(type='text', size=34, fn=lambda S: f"`n     = {_b(S['n'])}`  （{S['n']}）"),
        dict(type='text', size=34, fn=lambda S: f"`k     = {_b(S['k'])}`  （{S['k']}）"),
        dict(type='text', size=34, fn=lambda S: f"`n & k = {_b(S['n'] & S['k'])}`  " + ("==等于 k：k 是 n 的子集==" if S['n'] & S['k'] == S['k'] else "不等于 k：无法实现")),
        dict(type='text', size=34, fn=lambda S: f"`n ^ k = {_b(S['n'] ^ S['k'])}`  要去掉的 1 共 =={bin(S['n'] ^ S['k']).count('1')}== 个"),
    ],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'pink'), ('n & k', 'n & k', 'cyan'), ('n ^ k', 'n ^ k', 'orange')],
    captions={
        'return': lambda S, B, ret: (f'`n & k = {S.n & S.k}`' + (f' ==≠ k=={S.k}：k 有的 1，n 没有，改不出来 → -1' if S.n & S.k != S.k
                                     else f' 等于 k：k 是 n 的子集 → 答案是 `n ^ k = {_b(S.n ^ S.k)}` 里 1 的个数 = =={ret}==')),
    },
    cards=dict(
        one_liner='k 必须是 n 的子集；答案就是 n 比 k 多出的 1 的个数',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每次可以把 `n` 二进制里的一个 1 改成 0，问几次能把 `n` 变成 `k`',
                 '做不到就返回 `-1`',
                 '示例：`n = 13, k = 4` → `2`；`n = 14, k = 13` → `-1`'],
        quote='从集合的角度理解，每次操作相当于去掉集合 n 中的一个元素。要能把 n 变成 k，k 必须是 n 的子集。',
        quote_src='—— 灵茶山艾府题解',
        idea=['把二进制数看成集合：第 `i` 位是 1 就表示 `i` 在集合里',
              '`n & k == k`：交集是 `k`，说明 `k` 是 `n` 的子集（写法一）',
              '子集成立时，要去掉的元素个数就是 `(n ^ k).bit_count()`'],
        after=[dict(heading='无解的例子', lines=['`n = 14 = 1110`，`k = 13 = 1101`',
                                          '`n & k = 1100 = 12`，不等于 `k`',
                                          '`k` 的最低位是 1，`n` 的最低位是 0，只能删 1 不能补 1 → 返回 `-1`'])],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '先判子集再计数：`n & k != k` 时直接 `-1`',
                 'Python 里 `&` 比 `!=` 优先级高，`n & k != k` 就是 `(n & k) != k`（C++ 里要加括号）',
                 '另外两种判子集写法：`n | k != n`、`k & ~n`（非 0 则不是子集）',
                 '也可以数 `n - k` 的二进制里 1 的个数'],
    ),
)
