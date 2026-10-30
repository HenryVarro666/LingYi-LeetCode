def _b(x):
    return format(x, '04b')


CONFIG = dict(
    num=3226, title='使两个整数相等的位更改次数', difficulty='Easy', category='位运算',
    author='yiduobo', technique='n&k==k 判断 + m&=m-1 数 1',
    tags=['灵神题单', '位运算', '难度分 1247'],
    code='''
class Solution(object):
    def minChanges(self, n, k):

        if (n & k) != k:
            return -1

        m = n ^ k
        res = 0
        while m:
            res += 1
            m &= m - 1

        return res
''',
    call='Solution().minChanges(13, 4)',
    expect=2,
    views=[
        dict(type='text', size=34, fn=lambda S: f"`n = {_b(S['n'])}`（{S['n']}）   `k = {_b(S['k'])}`（{S['k']}）"),
        dict(type='text', size=34, fn=lambda S: (f"`m = n ^ k = {_b(S['m'])}`（{S['m']}）" if 'm' in S else '`n & k = ' + _b(S['n'] & S['k']) + '`' + ('  等于 k' if S['n'] & S['k'] == S['k'] else '  不等于 k'))),
        dict(type='text', size=34, fn=lambda S: (f"已清掉 `res = {S['res']}` 个多余的 1" if 'res' in S else '')),
    ],
    watch=[('n', 'n', 'blue'), ('k', 'k', 'pink'), ('m', 'm', 'orange'), ('res', 'res', 'green')],
    captions={
        'if (n & k) != k': lambda S, B, r: (f'`n & k = {S.n & S.k}`，`k = {S.k}`：k 的每个 1，n 对应位也是 1，==够用== → 继续' if S.n & S.k == S.k
                                            else f'`n & k = {S.n & S.k} != k`：k 有个 1 在 n 里是 0，n 没法把 0 变成 1 → 返回 -1'),
        'm = n ^ k': '`m = n ^ k = {m:04b}`：n 比 k ==多出来的 1==，每个都要改成 0',
        'res = 0': '`res` 记录需要改的次数',
        'while m': lambda S, B, r: (f'`m = {_b(S.m)}` 不为 0，还有多余的 1' if S.m else '`m = 0`：多余的 1 清完了'),
        'res += 1': '消掉一个 1，`res` → {res}',
        'm &= m - 1': '`m & (m - 1)` 清掉最低位的 1：`{B.m:04b}` → `{m:04b}`',
        'return res': '一共 `{res}` 次',
    },
    cards=dict(
        one_liner='先判 n&k==k，再用 m&=m-1 一个个清掉多余的 1',
        complexity='时间 `O(log n)`，空间 `O(1)`',
        problem=['每一轮可以把 `n` 的某个二进制位从 1 变成 0',
                 '求把 `n` 变成 `k` 需要几轮，不可能就返回 `-1`',
                 '示例：`n = 13, k = 4` → `2`；`n = 14, k = 13` → `-1`'],
        quote='若k的二进制表示中某一位为1，且n在这一位上为0，那么无论怎么操作都无法使得n这一位变为1，这种情况下答案就是-1。从位运算的角度来说，就是n & k != k。',
        quote_src='—— yiduobo 题解原文',
        idea=['只能把 1 改成 0，所以 `k` 里的 1，`n` 里必须也有',
              '满足后，`n` 比 `k` 多的 1 就是 `m = n ^ k` 里的 1',
              '`m &= m - 1` 每次清掉最低位的 1，数几次就是答案'],
        summary=['时间 `O(log n)`，空间 `O(1)`',
                 '判断要写成 `(n & k) != k`，先算 `&` 再比较',
                 '`m &= m - 1` 每次恰好少一个 1，循环次数 = 1 的个数',
                 '原文为 Python 2 风格，但本题无需改动，代码照搬',
                 '对比灵神：灵神用 `bit_count()` 一步数出 1 的个数'],
    ),
)
